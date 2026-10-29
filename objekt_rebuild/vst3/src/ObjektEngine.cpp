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
    int delay = 2;
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
        const auto delayed = data[static_cast<std::size_t>(index)];
        dampingState = damping * dampingState + (1.0f - damping) * delayed;
        const auto driven = dampingState * feedback * polarity + input;
        data[static_cast<std::size_t>(index)] = std::tanh(driven * (1.0f + collision * 5.0f));
        if (++index >= delay)
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
    float releaseGain = 1.0f;
    float releaseCoefficient = 1.0f;
    std::uint64_t age = 0;
    std::uint64_t serial = 0;
    double sampleRate = 48000.0;
    Random random;
    std::array<ModalMode, stages> modal;
    std::array<DelayLine, stages> object1;
    std::array<DelayLine, stages> object2;

    void prepare(double newRate)
    {
        sampleRate = newRate;
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
        velocity = clamp01(vel);
        releaseGain = 1.0f;
        age = 0;
        serial = newSerial;
        random.state = 0x9e3779b9u ^ static_cast<std::uint32_t>(note * 2654435761u) ^ static_cast<std::uint32_t>(newSerial);
        for (auto& line : object1) line.clear();
        for (auto& line : object2) line.clear();
        configure(params);
    }

    void configure(const Params& params)
    {
        const auto fundamental = midiHz(midiNote);
        for (int i = 0; i < stages; ++i)
        {
            const auto frequency = std::min(fundamental * modalRatios[static_cast<std::size_t>(i)], static_cast<float>(sampleRate * 0.46));
            const auto decay = std::clamp(params.modalDecay * std::pow(modalRatios[static_cast<std::size_t>(i)], -0.04f), 0.03f, 10.0f);
            const auto radius = std::pow(10.0f, -3.0f / (decay * static_cast<float>(sampleRate)));
            auto& mode = modal[static_cast<std::size_t>(i)];
            mode.y1 = mode.y2 = 0.0f;
            mode.coefficient = 2.0f * radius * std::cos(2.0f * pi * frequency / static_cast<float>(sampleRate));
            mode.radius2 = radius * radius;
            mode.injection = 1.0f - radius;

            const auto dispersed = std::pow(objectRatios[static_cast<std::size_t>(i)], 1.0f + params.dispersion * 0.16f);
            const auto objectFrequency = std::clamp(fundamental * dispersed, 20.0f, static_cast<float>(sampleRate * 0.43));
            const auto delay = std::clamp(static_cast<int>(std::lround(sampleRate / objectFrequency)), 2, maximumDelaySamples);
            auto configureLine = [this, delay](DelayLine& line, float decayTime)
            {
                line.delay = delay;
                line.feedback = std::pow(10.0f, -3.0f * static_cast<float>(delay) / static_cast<float>(sampleRate * std::max(0.03f, decayTime)));
            };
            configureLine(object1[static_cast<std::size_t>(i)], params.object1Decay / (1.0f + 0.035f * i));
            configureLine(object2[static_cast<std::size_t>(i)], params.object2Decay / (1.0f + 0.045f * i));
        }
    }

    void release() noexcept { released = true; }

    std::array<float, 2> render(const Params& params) noexcept
    {
        if (! active)
            return { 0.0f, 0.0f };

        const auto seconds = static_cast<float>(age) / static_cast<float>(sampleRate);
        const auto hardness = clamp01(params.hardness);
        const auto impactSeconds = 0.0015f + (1.0f - hardness) * 0.012f;
        const auto impactEnvelope = std::exp(-seconds / impactSeconds);
        const auto clickFrequency = std::min(midiHz(midiNote) * (2.0f + hardness * 5.0f), static_cast<float>(sampleRate * 0.4));
        const auto impactTone = std::sin(2.0f * pi * clickFrequency * seconds);
        const auto impact = params.impact * velocity * impactEnvelope * (0.68f * random.bipolar() + 0.32f * impactTone);
        const auto noiseEnvelope = std::exp(-seconds / 0.18f);
        const auto exciter = impact + params.noise * velocity * noiseEnvelope * random.bipolar();

        float modalLeft = 0.0f, modalRight = 0.0f, modalMono = 0.0f;
        for (int i = 0; i < stages; ++i)
        {
            auto& mode = modal[static_cast<std::size_t>(i)];
            const auto y = mode.coefficient * mode.y1 - mode.radius2 * mode.y2 + exciter * mode.injection;
            mode.y2 = mode.y1;
            mode.y1 = y;
            const auto stage = y * modalGains[static_cast<std::size_t>(i)];
            const auto pan = ((i & 1) == 0 ? -1.0f : 1.0f) * params.width * (0.12f + 0.03f * i);
            modalLeft += stage * std::sqrt(0.5f * (1.0f - pan));
            modalRight += stage * std::sqrt(0.5f * (1.0f + pan));
            modalMono += stage;
        }

        float object1Left = 0.0f, object1Right = 0.0f, object1Mono = 0.0f;
        float couplingFeed = 0.0f;
        const auto damping = std::clamp(params.damping, 0.0f, 0.98f);
        for (int i = 0; i < stages; ++i)
        {
            const auto input = exciter * objectGains[static_cast<std::size_t>(i)] + modalMono * 0.12f + couplingFeed * params.coupling;
            const auto polarity = (i & 1) == 0 ? 1.0f : -1.0f;
            const auto stage = object1[static_cast<std::size_t>(i)].tick(input, damping, params.collision, polarity);
            couplingFeed += stage * 0.08f;
            object1Mono += stage * objectGains[static_cast<std::size_t>(i)];
            const auto pan = ((i & 1) == 0 ? -1.0f : 1.0f) * params.width * (0.2f + 0.05f * i);
            object1Left += stage * std::sqrt(0.5f * (1.0f - pan));
            object1Right += stage * std::sqrt(0.5f * (1.0f + pan));
        }

        float object2Left = 0.0f, object2Right = 0.0f;
        couplingFeed = 0.0f;
        for (int i = 0; i < stages; ++i)
        {
            const auto input = exciter * 0.2f + object1Mono * objectGains[static_cast<std::size_t>(i)] * 0.22f + couplingFeed * params.coupling;
            const auto polarity = (i & 1) == 0 ? 1.0f : -1.0f;
            const auto stage = object2[static_cast<std::size_t>(i)].tick(input, std::min(0.98f, damping + 0.08f), params.collision * 0.8f, polarity);
            couplingFeed += stage * 0.08f;
            const auto pan = ((i & 1) == 0 ? 1.0f : -1.0f) * params.width * (0.22f + 0.045f * i);
            object2Left += stage * std::sqrt(0.5f * (1.0f - pan));
            object2Right += stage * std::sqrt(0.5f * (1.0f + pan));
        }

        auto left = params.modalMix * modalLeft + params.object1Mix * object1Left + params.object2Mix * object2Left;
        auto right = params.modalMix * modalRight + params.object1Mix * object1Right + params.object2Mix * object2Right;
        if (released)
        {
            releaseGain *= releaseCoefficient;
            left *= releaseGain;
            right *= releaseGain;
        }
        ++age;
        if ((released && releaseGain < 1.0e-4f) || age > static_cast<std::uint64_t>(sampleRate * 14.0))
            stop();
        return { left, right };
    }
};
} // namespace

struct Engine::Impl
{
    double sampleRate = 48000.0;
    std::array<Voice, Engine::maxVoices> voices;
    std::uint64_t serial = 0;
    std::array<std::vector<float>, 4> reverbLeft;
    std::array<std::vector<float>, 4> reverbRight;
    std::array<std::size_t, 4> reverbIndex {};
    std::array<float, 4> reverbFeedback { 0.69f, 0.72f, 0.74f, 0.76f };

    void prepare(double newRate)
    {
        sampleRate = newRate;
        for (auto& voice : voices) voice.prepare(newRate);
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
    impl->clearEffects();
}

void Engine::noteOn(int midiNote, float velocity)
{
    noteOn(midiNote, velocity, Params {});
}

void Engine::noteOn(int midiNote, float velocity, const Params& params)
{
    auto* selected = static_cast<Voice*>(nullptr);
    for (auto& voice : impl->voices)
        if (! voice.active) { selected = &voice; break; }
    if (selected == nullptr)
        selected = &*std::min_element(impl->voices.begin(), impl->voices.end(), [](const Voice& a, const Voice& b) { return a.serial < b.serial; });
    selected->start(std::clamp(midiNote, 0, 127), velocity, params, ++impl->serial);
}

void Engine::noteOff(int midiNote)
{
    for (auto& voice : impl->voices)
        if (voice.active && voice.midiNote == midiNote)
            voice.release();
}

void Engine::allNotesOff()
{
    for (auto& voice : impl->voices)
        if (voice.active)
            voice.release();
}

void Engine::process(float* left, float* right, int numSamples, const Params& params)
{
    if (left == nullptr || right == nullptr || numSamples <= 0)
        return;
    for (int sample = 0; sample < numSamples; ++sample)
    {
        float sumLeft = 0.0f, sumRight = 0.0f;
        for (auto& voice : impl->voices)
        {
            const auto frame = voice.render(params);
            sumLeft += frame[0];
            sumRight += frame[1];
        }
        const auto wet = impl->reverb(sumLeft, sumRight, clamp01(params.reverb));
        left[sample] += std::tanh(wet[0] * params.master);
        right[sample] += std::tanh(wet[1] * params.master);
    }
}

int Engine::activeVoiceCount() const noexcept
{
    return static_cast<int>(std::count_if(impl->voices.begin(), impl->voices.end(), [](const Voice& voice) { return voice.active; }));
}

} // namespace objekt
