#pragma once

#include "ObjektEffects.h"
#include "ObjektModulation.h"
#include <array>
#include <cstddef>
#include <memory>

namespace objekt {

struct Params
{
    EffectsParams effects;
    ModulationParams modulation;
    float bpm = 120.0f, pressure = 0.0f, wheel = 0.0f;
    float master = 0.72f;
    float impact = 0.82f;
    float hardness = 0.68f;
    float noise = 0.07f;
    float modalMix = 0.78f;
    float modalDecay = 2.0f;
    float object1Mix = 0.62f;
    float object1Decay = 1.45f;
    float damping = 0.34f;
    float dispersion = 0.14f;
    float collision = 0.08f;
    float coupling = 0.10f;
    float object2Mix = 0.42f;
    float object2Decay = 1.10f;
    float width = 0.55f;
    float reverb = 0.12f;
    float exciterMix = 0.0f, exciterPan = 0.0f;
    float modalPan = 0.0f, object1Pan = 0.0f, object2Pan = 0.0f;
    float modalTune = 0.0f, object1Tune = 0.0f, object2Tune = 0.0f;
    int modalStages = 8, object1Stages = 8, object2Stages = 8;
    int modalKeyTracking = 8, object1KeyTracking = 8, object2KeyTracking = 8;
    float pickupDrive = 0.0f, pickupSymmetry = 0.0f;
    float object1Exciter = 1.0f, object1Modal = 0.12f;
    float object2Exciter = 0.2f, object2Object1 = 0.22f;
    float click = 0.0f, impactVelocity = 1.0f, noiseVelocity = 1.0f;
    float impactFrequency = 0.68f, hardnessVelocity = 0.0f;
    int noiseType = 1; // Off, White, Color, Static, Noise Pulse, Random Pulse, Pulse, LP Noise.
    float noiseRate = 8.0f, noiseColor = 0.5f;
    float noiseDelay = 0.0f, noiseAttack = 0.0f, noiseDecay = 0.18f;
    float noiseSustain = 0.0f, noiseRelease = 0.2f;
    float externalLevel = 0.0f;
    float pitchBendSemitones = 0.0f;
    int keyMode = 0; // 0 Poly, 1 Mono, 2 Legato.
    float portamento = 0.0f;
    std::array<float, 8> modalRatios {1, 2.01f, 2.98f, 4.12f, 5.43f, 6.8f, 8.21f, 9.75f};
    std::array<float, 8> modalGains {1, .78f, .62f, .5f, .39f, .31f, .24f, .18f};
    std::array<float, 8> modalDecayScales {1, 1, 1, 1, 1, 1, 1, 1};
    std::array<float, 8> object1Ratios {1, 2, 3.02f, 4.05f, 5.12f, 6.22f, 7.38f, 8.6f};
    std::array<float, 8> object2Ratios {1, 2, 3.02f, 4.05f, 5.12f, 6.22f, 7.38f, 8.6f};
    std::array<float, 8> object1Gains {1, .62f, .48f, .38f, .3f, .24f, .2f, .17f};
    std::array<float, 8> object2Gains {1, .62f, .48f, .38f, .3f, .24f, .2f, .17f};
    std::array<float, 8> object1Polarity {1, -1, 1, -1, 1, -1, 1, -1};
    std::array<float, 8> object2Polarity {1, -1, 1, -1, 1, -1, 1, -1};
};

class Engine
{
public:
    static constexpr int maxVoices = 16;

    Engine();
    ~Engine();
    Engine(Engine&&) noexcept;
    Engine& operator=(Engine&&) noexcept;
    Engine(const Engine&) = delete;
    Engine& operator=(const Engine&) = delete;

    void prepare(double sampleRate, int maximumBlockSize);
    void reset();
    void noteOn(int midiNote, float velocity);
    void noteOn(int midiNote, float velocity, const Params& params);
    void noteOff(int midiNote);
    void allNotesOff();
    void process(float* left, float* right, int numSamples, const Params& params);
    void process(float* left, float* right, int numSamples, const Params& params, const float* inputLeft, const float* inputRight);
    [[nodiscard]] int activeVoiceCount() const noexcept;

private:
    struct Impl;
    std::unique_ptr<Impl> impl;
};

} // namespace objekt
