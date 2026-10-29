#pragma once

#include <juce_audio_utils/juce_audio_utils.h>
#include "ObjektEngine.h"

class ObjektRebuildAudioProcessor final : public juce::AudioProcessor
{
public:
    ObjektRebuildAudioProcessor();
    ~ObjektRebuildAudioProcessor() override = default;

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    bool isBusesLayoutSupported(const BusesLayout& layouts) const override;
    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    const juce::String getName() const override { return "Objekt Rebuild"; }
    bool acceptsMidi() const override { return true; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 8.0; }

    int getNumPrograms() override { return 4; }
    int getCurrentProgram() override { return currentProgram; }
    void setCurrentProgram(int index) override;
    const juce::String getProgramName(int index) override;
    void changeProgramName(int, const juce::String&) override {}

    void getStateInformation(juce::MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;

    static juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout();

private:
    objekt::Params snapshotParameters() const noexcept;
    void renderSegment(juce::AudioBuffer<float>& buffer, int startSample, int numSamples, const objekt::Params& params);
    void setParameterActual(const char* id, float value);

    objekt::Engine engine;
    juce::AudioProcessorValueTreeState parameters;
    int currentProgram = 0;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(ObjektRebuildAudioProcessor)
};
