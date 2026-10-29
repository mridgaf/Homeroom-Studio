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
    for (int note = 48; note < 60; ++note)
        engine.noteOn(note, 0.7f);

    std::vector<float> left(512, 0.0f), right(512, 0.0f);
    engine.process(left.data(), right.data(), 512, params);
    assert(engine.activeVoiceCount() == objekt::Engine::maxVoices);
    assert(std::any_of(left.begin(), left.end(), [](float x) { return std::abs(x) > 1.0e-5f; }));

    std::cout << "Objekt engine tests passed\n";
    return 0;
}
