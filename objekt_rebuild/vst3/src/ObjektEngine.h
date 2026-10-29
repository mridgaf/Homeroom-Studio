#pragma once

#include <cstddef>
#include <memory>

namespace objekt {

struct Params
{
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
};

class Engine
{
public:
    static constexpr int maxVoices = 8;

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
    [[nodiscard]] int activeVoiceCount() const noexcept;

private:
    struct Impl;
    std::unique_ptr<Impl> impl;
};

} // namespace objekt
