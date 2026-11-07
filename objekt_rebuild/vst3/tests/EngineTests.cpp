#include "ObjektEngine.h"

#include <algorithm>
#include <cassert>
#include <cmath>
#include <iostream>
#include <vector>

namespace {
float renderPeak(objekt::Engine& engine, const objekt::Params& params, int note)
{
    constexpr int block = 256;
    std::vector<float> left(block, 0.0f);
    std::vector<float> right(block, 0.0f);
    engine.noteOn(note, 0.9f, params);
    float peak = 0.0f;
    for (int pass = 0; pass < 80; ++pass)
    {
        std::fill(left.begin(), left.end(), 0.0f);
        std::fill(right.begin(), right.end(), 0.0f);
        engine.process(left.data(), right.data(), block, params);
        for (int i = 0; i < block; ++i)
        {
            assert(std::isfinite(left[i]));
            assert(std::isfinite(right[i]));
            peak = std::max({peak, std::abs(left[i]), std::abs(right[i])});
        }
    }
    engine.noteOff(note);
    return peak;
}
}

int main()
{
    objekt::Params params;
    objekt::Engine engine;
    engine.prepare(48000.0, 512);

    const auto peak = renderPeak(engine, params, 60);
    assert(peak > 1.0e-4f);
    assert(peak <= 1.0f);

    engine.reset();
    for (int note = 48; note < 70; ++note)
        engine.noteOn(note, 0.7f);

    std::vector<float> left(512, 0.0f), right(512, 0.0f);
    engine.process(left.data(), right.data(), 512, params);
    assert(engine.activeVoiceCount() == objekt::Engine::maxVoices);
    assert(std::any_of(left.begin(), left.end(), [](float x) { return std::abs(x) > 1.0e-5f; }));

    engine.reset();
    params.impact = params.noise = 0;
    params.externalLevel = 1;
    params.exciterMix = 1;
    params.modalMix = params.object1Mix = params.object2Mix = params.reverb = 0;
    engine.noteOn(60, 1, params);
    std::vector<float> input(512, .25f);
    std::fill(left.begin(), left.end(), 0);
    std::fill(right.begin(), right.end(), 0);
    engine.process(left.data(), right.data(), 512, params, input.data(), input.data());
    assert(left[0] > .01f && std::abs(left[0] - right[0]) < 1e-6f);
    engine.reset();
    params = {};
    params.keyMode = 2;
    engine.noteOn(60, 1, params);
    engine.noteOn(67, 1, params);
    assert(engine.activeVoiceCount() == 1);
    engine.noteOff(60);
    params.pitchBendSemitones = 12;
    params.modalStages = params.object1Stages = params.object2Stages = 0;
    params.exciterMix = 0;
    std::fill(left.begin(), left.end(), 0);
    std::fill(right.begin(), right.end(), 0);
    engine.process(left.data(), right.data(), 512, params);
    assert(std::all_of(left.begin(), left.end(), [](float x) { return x == 0; }));

    // Impact frequency and velocity-sensitive hardness must alter excitation independently.
    for (int control = 0; control < 2; ++control)
    {
        objekt::Engine a, b;
        a.prepare(48000, 512); b.prepare(48000, 512);
        objekt::Params baseline, altered;
        baseline.reverb = altered.reverb = 0;
        baseline.modalMix = altered.modalMix = 0;
        baseline.object1Mix = altered.object1Mix = 0;
        baseline.object2Mix = altered.object2Mix = 0;
        baseline.exciterMix = altered.exciterMix = 1;
        if (control == 0) altered.impactFrequency = 0.05f;
        else altered.hardnessVelocity = 1;
        a.noteOn(60, .2f, baseline); b.noteOn(60, .2f, altered);
        std::vector<float> l0(2048), r0(2048), l1(2048), r1(2048);
        a.process(l0.data(), r0.data(), 2048, baseline);
        b.process(l1.data(), r1.data(), 2048, altered);
        float difference = 0;
        for (int i=0;i<2048;++i) difference += std::abs(l0[i]-l1[i]);
        assert(difference > 0.01f);
    }

    // The coefficient-rate destinations must affect real audio, not only parameter state.
    for (auto target : {objekt::ModulationParams::pitch, objekt::ModulationParams::modalDecay,
                        objekt::ModulationParams::object1Decay, objekt::ModulationParams::object2Decay,
                        objekt::ModulationParams::dispersion})
    {
        objekt::Engine baseline, changed;
        baseline.prepare(48000, 512); changed.prepare(48000, 512);
        objekt::Params a, b;
        a.reverb = b.reverb = 0;
        b.modulation.buses[0].source = objekt::ModulationParams::constant;
        b.modulation.buses[0].target1 = target;
        b.modulation.buses[0].amount1 = .5f;
        baseline.noteOn(60, 1, a); changed.noteOn(60, 1, b);
        std::vector<float> l0(4096), r0(4096), l1(4096), r1(4096);
        baseline.process(l0.data(), r0.data(), 4096, a);
        changed.process(l1.data(), r1.data(), 4096, b);
        float difference = 0;
        for (std::size_t n=0; n<l0.size(); ++n) difference += std::abs(l0[n]-l1[n]);
        assert(difference > 1.0e-4f);
    }

    std::cout << "Objekt engine tests passed\n";
    return 0;
}
