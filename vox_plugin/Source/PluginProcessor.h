#pragma once
#include <juce_audio_processors/juce_audio_processors.h>

/** Phase 1: passthrough only. Proves a JUCE VST3 loads in Reason 12 and
    passes audio before any DSP is ported. See the Phase 2 plan. */
class VoxProcessor : public juce::AudioProcessor
{
public:
    VoxProcessor();
    ~VoxProcessor() override = default;

    void prepareToPlay (double sampleRate, int maxBlockSize) override;
    void releaseResources() override {}
    bool isBusesLayoutSupported (const BusesLayout&) const override;
    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    const juce::String getName() const override { return "Vox"; }
    bool acceptsMidi() const override  { return false; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 0.0; }

    int getNumPrograms() override { return 1; }
    int getCurrentProgram() override { return 0; }
    void setCurrentProgram (int) override {}
    const juce::String getProgramName (int) override { return "Default"; }
    void changeProgramName (int, const juce::String&) override {}

    void getStateInformation (juce::MemoryBlock&) override {}
    void setStateInformation (const void*, int) override {}

    /** Peak of the last block, for the editor. Written on the audio thread,
        read on the message thread -- atomic, never a lock. */
    std::atomic<float> inPeak { 0.0f };

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VoxProcessor)
};
