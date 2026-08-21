#include "PluginProcessor.h"
#include "PluginEditor.h"

VoxProcessor::VoxProcessor()
    : AudioProcessor (BusesProperties()
        .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
        .withOutput ("Output", juce::AudioChannelSet::stereo(), true))
{
}

void VoxProcessor::prepareToPlay (double, int)
{
    setLatencySamples (0);   // Phase 3 replaces this with the constant chain latency.
}

bool VoxProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
    const auto& out = layouts.getMainOutputChannelSet();
    if (out != juce::AudioChannelSet::mono() && out != juce::AudioChannelSet::stereo())
        return false;
    return layouts.getMainInputChannelSet() == out;
}

void VoxProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer&)
{
    juce::ScopedNoDenormals noDenormals;

    for (int ch = getTotalNumInputChannels(); ch < getTotalNumOutputChannels(); ++ch)
        buffer.clear (ch, 0, buffer.getNumSamples());

    inPeak.store (buffer.getMagnitude (0, buffer.getNumSamples()),
                  std::memory_order_relaxed);

    // Phase 1: audio passes through untouched.
}

juce::AudioProcessorEditor* VoxProcessor::createEditor()
{
    return new VoxEditor (*this);
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new VoxProcessor();
}
