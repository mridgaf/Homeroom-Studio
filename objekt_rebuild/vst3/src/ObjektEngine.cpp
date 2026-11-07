#include "ObjektEngine.h"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <limits>
#include <vector>

namespace objekt {
namespace {
constexpr float pi = 3.14159265358979323846f;
constexpr int stages = 8;
constexpr int maximumDelaySamples = 8192;
constexpr std::array<float, stages> modalRatios { 1.0f, 2.01f, 2.98f, 4.12f, 5.43f, 6.8f, 8.21f, 9.75f };
constexpr std::array<float, stages> modalGains { 1.0f, 0.78f, 0.62f, 0.5f, 0.39f, 0.31f, 0.24f, 0.18f };
constexpr std::array<float, stages> objectRatios { 1.0f, 2.0f, 3.02f, 4.05f, 5.12f, 6.22f, 7.38f, 8.6f };
constexpr std::array<float, stages> objectGains { 1.0f, 0.62f, 0.48f, 0.38f, 0.3f, 0.24f, 0.2f, 0.17f };

float clamp01(float value) noexcept { return std::clamp(value, 0.0f, 1.0f); }
float midiHz(int note) noexcept { return 440.0f * std::pow(2.0f, (static_cast<float>(note) - 69.0f) / 12.0f); }

struct Random
{
    std::uint32_t state = 0x12345678u;
    float bipolar() noexcept
    {
        state ^= state << 13u;
        state ^= state >> 17u;
        state ^= state << 5u;
        return static_cast<float>(state & 0x00ffffffu) / 8388607.5f - 1.0f;
    }
};

struct ModalMode
{
    float y1 = 0.0f, y2 = 0.0f, coefficient = 0.0f, radius2 = 0.0f, injection = 0.0f;
};

struct DelayLine
{
    std::vector<float> data;
    int index = 0;
    float delay = 2;
    float feedback = 0.0f;
    float dampingState = 0.0f;

    void prepare()
    {
        data.assign(maximumDelaySamples, 0.0f);
    }

    void clear()
    {
        std::fill(data.begin(), data.end(), 0.0f);
        index = 0;
        dampingState = 0.0f;
    }

    float tick(float input, float damping, float collision, float polarity) noexcept
    {
        auto read = static_cast<float>(index) - delay;
        if (read < 0.0f) read += static_cast<float>(data.size());
        const auto first = static_cast<std::size_t>(read);
        const auto fraction = read - static_cast<float>(first);
        const auto delayed = data[first] + fraction * (data[(first + 1) % data.size()] - data[first]);
        dampingState = damping * dampingState + (1.0f - damping) * delayed;
        const auto driven = dampingState * feedback * polarity + input;
        data[static_cast<std::size_t>(index)] = std::tanh(driven * (1.0f + collision * 5.0f));
        if (++index >= static_cast<int>(data.size()))
            index = 0;
        return delayed;
    }
};

struct Voice
{
    bool active = false;
    bool released = false;
    int midiNote = -1;
    float velocity = 0.0f;
    float currentNote = 60.0f;
    float releaseGain = 1.0f;
    float releaseCoefficient = 1.0f;
    std::uint64_t age = 0;
    std::uint64_t serial = 0;
    double sampleRate = 48000.0;
    Modulation modulation;
    Random random;
    float noisePhase = 0.0f, noiseHeld = 0.0f, noiseFiltered = 0.0f;
    float envelopeAtRelease = 0.0f, noiseEnvelope = 0.0f;
    std::uint64_t releaseAge = 0;
    std::array<ModalMode, stages> modal;
    std::array<DelayLine, stages> object1;
    std::array<DelayLine, stages> object2;
    std::array<float, stages> previous1 {}, previous2 {};

    void prepare(double newRate)
    {
        sampleRate = newRate;
        modulation.prepare(newRate);
        releaseCoefficient = std::exp(std::log(1.0e-4f) / static_cast<float>(sampleRate * 2.0));
        for (auto& line : object1) line.prepare();
        for (auto& line : object2) line.prepare();
        stop();
    }

    void stop() noexcept
    {
        active = false;
        released = false;
        midiNote = -1;
        velocity = 0.0f;
        releaseGain = 1.0f;
        age = 0;
    }

    void start(int note, float vel, const Params& params, std::uint64_t newSerial)
    {
        active = true;
        released = false;
        midiNote = note;
        currentNote = static_cast<float>(note);
        velocity = clamp01(vel);
        releaseGain = 1.0f;
        age = 0;
        noisePhase = noiseHeld = noiseFiltered = noiseEnvelope = 0.0f;
        releaseAge = 0;
        serial = newSerial;
        previous1.fill(0); previous2.fill(0);
        modulation.reset();
        random.state = 0x9e3779b9u ^ static_cast<std::uint32_t>(note * 2654435761u) ^ static_cast<std::uint32_t>(newSerial);
        for (auto& line : object1) line.clear();
        for (auto& line : object2) line.clear();
        for (auto& mode : modal) mode.y1 = mode.y2 = 0.0f;
        configure(params);
    }

    void configure(const Params& params)
    {
        const auto fundamental = 440.0f * std::exp2((currentNote + params.pitchBendSemitones - 69.0f) / 12.0f);
        for (int i = 0; i < stages; ++i)
        {
            const auto frequency = std::min((i < params.modalKeyTracking ? fundamental : midiHz(60)) * std::exp2(params.modalTune / 12.0f) * std::max(.01f, params.modalRatios[static_cast<std::size_t>(i)]), static_cast<float>(sampleRate * 0.46));
            const auto decay = std::clamp(params.modalDecay * params.modalDecayScales[static_cast<std::size_t>(i)] * std::pow(std::max(.01f, params.modalRatios[static_cast<std::size_t>(i)]), -0.04f), 0.03f, 10.0f);
            const auto radius = std::pow(10.0f, -3.0f / (decay * static_cast<float>(sampleRate)));
            auto& mode = modal[static_cast<std::size_t>(i)];
            mode.coefficient = 2.0f * radius * std::cos(2.0f * pi * frequency / static_cast<float>(sampleRate));
            mode.radius2 = radius * radius;
            mode.injection = 1.0f - radius;

            auto configureLine = [this, fundamental, i, &params](DelayLine& line, float decayTime, float ratio, float tune, int tracking)
            {
                const auto dispersed = std::pow(std::max(.01f, ratio), 1.0f + params.dispersion * .16f);
                const auto frequency = std::clamp((i < tracking ? fundamental : midiHz(60)) * std::exp2(tune / 12.0f) * dispersed, 1.0f, static_cast<float>(sampleRate * .43));
                line.delay = std::clamp(static_cast<float>(sampleRate) / frequency, 2.0f, static_cast<float>(maximumDelaySamples - 1));
                line.feedback = std::pow(10.0f, -3.0f * line.delay / static_cast<float>(sampleRate * std::max(.03f, decayTime)));
            };
            configureLine(object1[i], params.object1Decay / (1 + .035f * i), params.object1Ratios[i], params.object1Tune, params.object1KeyTracking);
            configureLine(object2[i], params.object2Decay / (1 + .045f * i), params.object2Ratios[i], params.object2Tune, params.object2KeyTracking);
        }
    }

    void release() noexcept { if (!released) { released = true; releaseAge = age; envelopeAtRelease = noiseEnvelope; } }

    std::array<float, 2> render(const Params& params, float external) noexcept
    {
        if (! active)
            return { 0.0f, 0.0f };

        const auto glide = params.portamento > 0 ? std::exp(-1.0f / static_cast<float>(sampleRate * params.portamento)) : 0.0f;
        currentNote = static_cast<float>(midiNote) + glide * (currentNote - static_cast<float>(midiNote));
        const auto modulationValues = modulation.tick(params.modulation, params.bpm, velocity, currentNote, params.pressure, params.wheel);
        const auto modulated_impact = std::clamp(params.impact + modulationValues[ModulationParams::impact], 0.0f, 1.0f);
        const auto modulated_hardness = std::clamp(params.hardness + modulationValues[ModulationParams::hardness], 0.0f, 1.0f);
        const auto modulated_noise = std::clamp(params.noise + modulationValues[ModulationParams::noise], 0.0f, 1.0f);
        const auto modulated_modalMix = std::clamp(params.modalMix + modulationValues[ModulationParams::modalLevel], 0.0f, 1.0f);
        const auto modulated_object1Mix = std::clamp(params.object1Mix + modulationValues[ModulationParams::object1Level], 0.0f, 1.0f);
        const auto modulated_object2Mix = std::clamp(params.object2Mix + modulationValues[ModulationParams::object2Level], 0.0f, 1.0f);
        const auto modulated_damping = std::clamp(params.damping + modulationValues[ModulationParams::damping], 0.0f, .98f);
        const auto modulated_collision = std::clamp(params.collision + modulationValues[ModulationParams::collision], 0.0f, 1.0f);
        const auto modulated_coupling = std::clamp(params.coupling + modulationValues[ModulationParams::coupling], 0.0f, 0.55f);
        const auto modulated_width = std::clamp(params.width + modulationValues[ModulationParams::width], 0.0f, 1.0f);
        if ((age & 31u) == 0)
        {
            auto tuned = params;
            tuned.pitchBendSemitones += modulationValues[ModulationParams::pitch] * 12;
            tuned.modalDecay = std::clamp(params.modalDecay + modulationValues[ModulationParams::modalDecay] * 8, .03f, 10.0f);
            tuned.object1Decay = std::clamp(params.object1Decay + modulationValues[ModulationParams::object1Decay] * 8, .03f, 10.0f);
            tuned.object2Decay = std::clamp(params.object2Decay + modulationValues[ModulationParams::object2Decay] * 8, .03f, 10.0f);
            tuned.dispersion = clamp01(params.dispersion + modulationValues[ModulationParams::dispersion]);
            configure(tuned);
        }
        const auto seconds = static_cast<float>(age) / static_cast<float>(sampleRate);
        const auto hardness = clamp01(modulated_hardness + params.hardnessVelocity * (velocity - 0.5f));
        const auto impactSeconds = 0.0015f + (1.0f - clamp01(params.impactFrequency)) * 0.012f;
        const auto impactEnvelope = std::exp(-seconds / impactSeconds);
        const auto clickFrequency = std::min(midiHz(midiNote) * (2.0f + hardness * 5.0f), static_cast<float>(sampleRate * 0.4));
        const auto impactTone = std::sin(2.0f * pi * clickFrequency * seconds);
        const auto impact = modulated_impact * (1.0f - clamp01(params.impactVelocity) * (1.0f - velocity)) * impactEnvelope * (0.68f * random.bipolar() + 0.32f * impactTone);
        const auto noiseTime = seconds - std::max(0.0f, params.noiseDelay);
        if (released)
            noiseEnvelope = envelopeAtRelease * std::exp(-static_cast<float>(age - releaseAge) / static_cast<float>(sampleRate * std::max(.001f, params.noiseRelease)));
        else if (noiseTime < 0) noiseEnvelope = 0;
        else if (noiseTime < params.noiseAttack) noiseEnvelope = noiseTime / std::max(.0001f, params.noiseAttack);
        else noiseEnvelope = clamp01(params.noiseSustain) + (1 - clamp01(params.noiseSustain)) * std::exp(-(noiseTime - params.noiseAttack) / std::max(.001f, params.noiseDecay));
        noisePhase += std::clamp(params.noiseRate, .01f, static_cast<float>(sampleRate * .45)) / static_cast<float>(sampleRate);
        const bool pulse = noisePhase >= 1;
        if (pulse) { noisePhase -= 1; noiseHeld = random.bipolar(); }
        const auto white = random.bipolar();
        noiseFiltered += (.001f + clamp01(params.noiseColor) * .8f) * (white - noiseFiltered);
        float noiseSignal = white;
        switch (params.noiseType) {
            case 0: noiseSignal = 0; break;
            case 2: noiseSignal = noiseFiltered * 2; break;
            case 3: noiseSignal = noiseHeld; break;
            case 4: noiseSignal = pulse ? white : 0; break;
            case 5: noiseSignal = pulse && noiseHeld > 0 ? 1 : 0; break;
            case 6: noiseSignal = noisePhase < .5f ? 1 : -1; break;
            case 7: noiseSignal = noiseFiltered; break;
            default: break;
        }
        const auto exciter = impact + (age == 0 ? params.click * velocity : 0) + modulated_noise * (1 - clamp01(params.noiseVelocity) * (1 - velocity)) * noiseEnvelope * noiseSignal + external * params.externalLevel;

        float modalLeft = 0.0f, modalRight = 0.0f, modalMono = 0.0f;
        for (int i = 0; i < std::clamp(params.modalStages, 0, stages); ++i)
        {
            auto& mode = modal[static_cast<std::size_t>(i)];
            const auto y = mode.coefficient * mode.y1 - mode.radius2 * mode.y2 + exciter * mode.injection;
            mode.y2 = mode.y1;
            mode.y1 = y;
            const auto pickup = params.pickupDrive <= 0 ? y : (std::tanh(y * (1 + params.pickupDrive * 20) + params.pickupSymmetry) - std::tanh(params.pickupSymmetry)) / (1 + params.pickupDrive * 20);
            const auto stage = pickup * params.modalGains[i];
            const auto pan = ((i & 1) == 0 ? -1.0f : 1.0f) * modulated_width * (0.12f + 0.03f * i);
            modalLeft += stage * std::sqrt(0.5f * (1.0f - pan));
            modalRight += stage * std::sqrt(0.5f * (1.0f + pan));
            modalMono += stage;
        }

        float object1Left = 0.0f, object1Right = 0.0f, object1Mono = 0.0f;
        float couplingFeed = 0.0f;
        for (int i=0; i<std::clamp(params.object1Stages,0,stages); ++i) couplingFeed += previous1[i];
        const auto damping = std::clamp(modulated_damping, 0.0f, 0.98f);
        for (int i = 0; i < std::clamp(params.object1Stages, 0, stages); ++i)
        {
            const auto input = exciter * params.object1Gains[i] * params.object1Exciter + modalMono * params.object1Modal + (couplingFeed - previous1[i]) * modulated_coupling / 7.0f;
            const auto polarity = params.object1Polarity[i] < 0 ? -1.0f : 1.0f;
            const auto stage = object1[static_cast<std::size_t>(i)].tick(input, damping, modulated_collision, polarity);
            previous1[i] = stage;
            object1Mono += stage * params.object1Gains[i];
            const auto pan = ((i & 1) == 0 ? -1.0f : 1.0f) * modulated_width * (0.2f + 0.05f * i);
            object1Left += stage * std::sqrt(0.5f * (1.0f - pan));
            object1Right += stage * std::sqrt(0.5f * (1.0f + pan));
        }

        float object2Left = 0.0f, object2Right = 0.0f;
        couplingFeed = 0.0f;
        for (int i=0; i<std::clamp(params.object2Stages,0,stages); ++i) couplingFeed += previous2[i];
        for (int i = 0; i < std::clamp(params.object2Stages, 0, stages); ++i)
        {
            const auto input = exciter * params.object2Exciter + object1Mono * params.object2Gains[i] * params.object2Object1 + (couplingFeed - previous2[i]) * modulated_coupling / 7.0f;
            const auto polarity = params.object2Polarity[i] < 0 ? -1.0f : 1.0f;
            const auto stage = object2[static_cast<std::size_t>(i)].tick(input, std::min(0.98f, damping + 0.08f), modulated_collision * 0.8f, polarity);
            previous2[i] = stage;
            const auto pan = ((i & 1) == 0 ? 1.0f : -1.0f) * modulated_width * (0.22f + 0.045f * i);
            object2Left += stage * std::sqrt(0.5f * (1.0f - pan));
            object2Right += stage * std::sqrt(0.5f * (1.0f + pan));
        }

        auto left = params.exciterMix * exciter * std::sqrt(.5f * (1 - std::clamp(params.exciterPan, -1.0f, 1.0f))) + modulated_modalMix * modalLeft * (1 - std::max(0.0f, params.modalPan)) + modulated_object1Mix * object1Left * (1 - std::max(0.0f, params.object1Pan)) + modulated_object2Mix * object2Left * (1 - std::max(0.0f, params.object2Pan));
        auto right = params.exciterMix * exciter * std::sqrt(.5f * (1 + std::clamp(params.exciterPan, -1.0f, 1.0f))) + modulated_modalMix * modalRight * (1 + std::min(0.0f, params.modalPan)) + modulated_object1Mix * object1Right * (1 + std::min(0.0f, params.object1Pan)) + modulated_object2Mix * object2Right * (1 + std::min(0.0f, params.object2Pan));
        if (released)
        {
            releaseGain *= releaseCoefficient;
            left *= releaseGain;
            right *= releaseGain;
        }
        ++age;
        if ((released && releaseGain < 1.0e-4f) || (age > static_cast<std::uint64_t>(sampleRate * 14.0) && !(params.externalLevel > 0 && params.keyMode != 0) && params.noiseSustain <= 0))
            stop();
        return { left, right };
    }
};
} // namespace

struct Engine::Impl
{
    Effects effects;
    double sampleRate = 48000.0;
    std::array<Voice, Engine::maxVoices> voices;
    std::uint64_t serial = 0;
    std::array<std::uint64_t, 128> heldNotes {};
    std::array<float, 128> heldVelocity {};
    Params lastParams;
    std::array<std::vector<float>, 4> reverbLeft;
    std::array<std::vector<float>, 4> reverbRight;
    std::array<std::size_t, 4> reverbIndex {};
    std::array<float, 4> reverbFeedback { 0.69f, 0.72f, 0.74f, 0.76f };

    void prepare(double newRate)
    {
        sampleRate = newRate;
        for (auto& voice : voices) voice.prepare(newRate);
        effects.prepare(newRate);
        constexpr std::array<double, 4> times { 0.0297, 0.0371, 0.0411, 0.0437 };
        for (std::size_t i = 0; i < times.size(); ++i)
        {
            const auto length = std::max<std::size_t>(2, static_cast<std::size_t>(newRate * times[i]));
            reverbLeft[i].assign(length, 0.0f);
            reverbRight[i].assign(length + 17, 0.0f);
            reverbIndex[i] = 0;
        }
    }

    void clearEffects()
    {
        effects.reset();
        for (auto& buffer : reverbLeft) std::fill(buffer.begin(), buffer.end(), 0.0f);
        for (auto& buffer : reverbRight) std::fill(buffer.begin(), buffer.end(), 0.0f);
        reverbIndex.fill(0);
    }

    std::array<float, 2> reverb(float left, float right, float amount) noexcept
    {
        float wetLeft = 0.0f, wetRight = 0.0f;
        for (std::size_t i = 0; i < reverbLeft.size(); ++i)
        {
            auto& l = reverbLeft[i];
            auto& r = reverbRight[i];
            auto indexL = reverbIndex[i] % l.size();
            auto indexR = reverbIndex[i] % r.size();
            const auto delayedL = l[indexL];
            const auto delayedR = r[indexR];
            l[indexL] = right + delayedL * reverbFeedback[i];
            r[indexR] = left + delayedR * (reverbFeedback[i] - 0.02f);
            ++reverbIndex[i];
            wetLeft += delayedL;
            wetRight += delayedR;
        }
        wetLeft *= 0.25f;
        wetRight *= 0.25f;
        return { left * (1.0f - amount) + wetLeft * amount, right * (1.0f - amount) + wetRight * amount };
    }
};

Engine::Engine() : impl(std::make_unique<Impl>()) {}
Engine::~Engine() = default;
Engine::Engine(Engine&&) noexcept = default;
Engine& Engine::operator=(Engine&&) noexcept = default;

void Engine::prepare(double sampleRate, int)
{
    impl->prepare(std::clamp(sampleRate, 8000.0, 192000.0));
}

void Engine::reset()
{
    for (auto& voice : impl->voices) voice.stop();
    impl->heldNotes.fill(0);
    impl->clearEffects();
}

void Engine::noteOn(int midiNote, float velocity)
{
    noteOn(midiNote, velocity, Params {});
}

void Engine::noteOn(int midiNote, float velocity, const Params& params)
{
    impl->lastParams = params;
    midiNote = std::clamp(midiNote, 0, 127);
    impl->heldNotes[midiNote] = impl->serial + 1;
    impl->heldVelocity[midiNote] = velocity;
    if (params.keyMode != 0)
    {
        auto& voice = impl->voices[0];
        const auto previousPitch = voice.currentNote;
        const bool wasActive = voice.active;
        for (std::size_t i = 1; i < impl->voices.size(); ++i) impl->voices[i].stop();
        if (params.keyMode == 2 && voice.active && !voice.released)
        {
            voice.midiNote = std::clamp(midiNote, 0, 127);
            voice.velocity = clamp01(velocity);
            voice.serial = ++impl->serial;
            if (params.portamento <= 0) voice.currentNote = static_cast<float>(voice.midiNote);
        }
        else
        {
            voice.start(std::clamp(midiNote, 0, 127), velocity, params, ++impl->serial);
            if (wasActive && params.portamento > 0) voice.currentNote = previousPitch;
        }
        return;
    }
    auto* selected = static_cast<Voice*>(nullptr);
    for (auto& voice : impl->voices)
        if (! voice.active) { selected = &voice; break; }
    if (selected == nullptr)
        selected = &*std::min_element(impl->voices.begin(), impl->voices.end(), [](const Voice& a, const Voice& b) { return a.serial < b.serial; });
    selected->start(std::clamp(midiNote, 0, 127), velocity, params, ++impl->serial);
}

void Engine::noteOff(int midiNote)
{
    if (midiNote < 0 || midiNote > 127) return;
    impl->heldNotes[midiNote] = 0;
    if (impl->lastParams.keyMode != 0 && impl->voices[0].midiNote == midiNote)
    {
        const auto mostRecent = std::max_element(impl->heldNotes.begin(), impl->heldNotes.end());
        if (*mostRecent != 0)
        {
            const auto note = static_cast<int>(mostRecent - impl->heldNotes.begin());
            auto& voice = impl->voices[0];
            if (impl->lastParams.keyMode == 2)
            {
                voice.midiNote = note;
                voice.velocity = clamp01(impl->heldVelocity[note]);
                return;
            }
            noteOn(note, impl->heldVelocity[note], impl->lastParams);
            return;
        }
    }
    for (auto& voice : impl->voices)
        if (voice.active && voice.midiNote == midiNote)
            voice.release();
}

void Engine::allNotesOff()
{
    impl->heldNotes.fill(0);
    for (auto& voice : impl->voices)
        if (voice.active)
            voice.release();
}

void Engine::process(float* left, float* right, int numSamples, const Params& params)
{
    process(left, right, numSamples, params, nullptr, nullptr);
}

void Engine::process(float* left, float* right, int numSamples, const Params& params, const float* inputLeft, const float* inputRight)
{
    if (left == nullptr || right == nullptr || numSamples <= 0)
        return;
    if (params.keyMode != 0 && params.externalLevel > 0 && !impl->voices[0].active)
        impl->voices[0].start(60, 1.0f, params, ++impl->serial);
    impl->effects.setParameters(params.effects);
    for (int sample = 0; sample < numSamples; ++sample)
    {
        float sumLeft = 0.0f, sumRight = 0.0f;
        for (auto& voice : impl->voices)
        {
            const auto frame = voice.render(params, .5f * ((inputLeft ? inputLeft[sample] : 0) + (inputRight ? inputRight[sample] : (inputLeft ? inputLeft[sample] : 0))));
            sumLeft += frame[0];
            sumRight += frame[1];
        }
        const auto legacy = impl->reverb(sumLeft, sumRight, clamp01(params.reverb));
        const auto wet = impl->effects.process(legacy[0], legacy[1]);
        if (inputLeft || inputRight)
        {
            left[sample] = std::tanh(wet[0] * params.master);
            right[sample] = std::tanh(wet[1] * params.master);
        }
        else
        {
            left[sample] += std::tanh(wet[0] * params.master);
            right[sample] += std::tanh(wet[1] * params.master);
        }
    }
}

int Engine::activeVoiceCount() const noexcept
{
    return static_cast<int>(std::count_if(impl->voices.begin(), impl->voices.end(), [](const Voice& voice) { return voice.active; }));
}

} // namespace objekt
