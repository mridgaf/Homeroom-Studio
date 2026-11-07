#pragma once
#include <array>
#include <algorithm>
#include <cmath>

namespace objekt {
// Independent modulation model; the original device's curves remain unmeasured.
struct ModulationParams {
    enum Source { off, lfo1, lfo2, curve, macro1, macro2, velocity, key, pressure, wheel, constant, sourceCount };
    enum Target { none, pitch, impact, hardness, noise, modalLevel, modalDecay, object1Level, object1Decay,
                  object2Level, object2Decay, damping, dispersion, collision, coupling, width, targetCount };
    struct Lfo { float rate = 1.0f; int shape = 0; bool sync = false; };
    struct Bus { int source = off; int target1 = none; int target2 = none; int scale = constant; float amount1 = 0, amount2 = 0; };
    std::array<Lfo, 2> lfos {};
    std::array<float, 16> steps {};
    int stepCount = 16;
    float curveRate = 1.0f;
    bool curveSync = false;
    bool curveSmooth = false;
    std::array<float, 2> macros {};
    std::array<Bus, 8> buses {};
};
class Modulation {
public:
    using Values = std::array<float, ModulationParams::targetCount>;
    void prepare(double rate) { sampleRate = std::max(8000.0, rate); reset(); }
    void reset() { phases.fill(0); }
    Values tick(const ModulationParams& p, float bpm, float velocity, float note, float pressure, float wheel) noexcept {
        std::array<float, ModulationParams::sourceCount> sources {};
        sources[ModulationParams::constant] = 1;
        for (int i = 0; i < 2; ++i) {
            auto& phase = phases[static_cast<std::size_t>(i)];
            const auto& lfo = p.lfos[static_cast<std::size_t>(i)];
            const float x = static_cast<float>(phase);
            float value = 0;
            switch (lfo.shape) {
                case 1: value = 1 - 4 * std::abs(x - 0.5f); break;
                case 2: value = 2*x - 1; break;
                case 3: value = x < 0.5f ? 1.0f : -1.0f; break;
                default: value = std::sin(6.28318530718f*x); break;
            }
            sources[ModulationParams::lfo1+i] = value;
            advance(phase, lfo.rate, lfo.sync, bpm);
        }
        const int count = std::clamp(p.stepCount, 1, 16);
        const double step = phases[2] * count;
        const int index = std::min(count-1, static_cast<int>(step));
        const float blend = p.curveSmooth ? static_cast<float>(step-index) : 0.0f;
        sources[ModulationParams::curve] = p.steps[index]*(1-blend)+p.steps[(index+1)%count]*blend;
        advance(phases[2], p.curveRate, p.curveSync, bpm);
        sources[ModulationParams::macro1] = std::clamp(p.macros[0], -1.0f, 1.0f);
        sources[ModulationParams::macro2] = std::clamp(p.macros[1], -1.0f, 1.0f);
        sources[ModulationParams::velocity] = std::clamp(velocity, 0.0f, 1.0f);
        sources[ModulationParams::key] = std::clamp(note/127.0f, 0.0f, 1.0f);
        sources[ModulationParams::pressure] = std::clamp(pressure, 0.0f, 1.0f);
        sources[ModulationParams::wheel] = std::clamp(wheel, 0.0f, 1.0f);
        Values result {};
        for (const auto& bus : p.buses) {
            const float source = sources[std::clamp(bus.source, 0, int(ModulationParams::sourceCount)-1)]
                               * sources[std::clamp(bus.scale, 0, int(ModulationParams::sourceCount)-1)];
            if (bus.target1 > 0 && bus.target1 < ModulationParams::targetCount) result[bus.target1] += source*bus.amount1;
            if (bus.target2 > 0 && bus.target2 < ModulationParams::targetCount) result[bus.target2] += source*bus.amount2;
        }
        return result;
    }
private:
    void advance(double& phase, float rate, bool sync, float bpm) noexcept {
        const auto hz = std::clamp(rate, 0.001f, 100.0f) * (sync ? std::clamp(bpm, 1.0f, 999.0f)/60.0f : 1.0f);
        phase += hz/sampleRate;
        phase -= std::floor(phase);
    }
    double sampleRate = 48000;
    std::array<double, 3> phases {};
};
}
