#include "PluginProcessor.h"

#include <cassert>
#include <cmath>
#include <iostream>

int main()
{
    ObjektRebuildAudioProcessor processor;
    assert(processor.acceptsMidi());
    assert(processor.getTotalNumOutputChannels() == 2);
    processor.prepareToPlay(48000.0, 256);

    juce::AudioBuffer<float> audio(2, 256);
    juce::MidiBuffer midi;
    midi.addEvent(juce::MidiMessage::noteOn(1, 60, static_cast<juce::uint8>(110)), 0);

    float peak = 0.0f;
    for (int block = 0; block < 40; ++block)
    {
        audio.clear();
        processor.processBlock(audio, midi);
        midi.clear();
        peak = std::max(peak, audio.getMagnitude(0, audio.getNumSamples()));
        peak = std::max(peak, audio.getMagnitude(1, audio.getNumSamples()));
        for (int channel = 0; channel < audio.getNumChannels(); ++channel)
            for (int sample = 0; sample < audio.getNumSamples(); ++sample)
                assert(std::isfinite(audio.getSample(channel, sample)));
    }
    assert(peak > 1.0e-4f);
    assert(peak <= 1.0f);

    auto* impact = processor.getParameters().getUnchecked(1);
    impact->setValueNotifyingHost(0.21f);
    juce::MemoryBlock state;
    processor.getStateInformation(state);
    impact->setValueNotifyingHost(0.91f);
    processor.setStateInformation(state.getData(), static_cast<int>(state.getSize()));
    assert(std::abs(impact->getValue() - 0.21f) < 0.001f);

    // All Sound Off must silence voices and effects immediately.
    midi.addEvent(juce::MidiMessage::allSoundOff(1), 0);
    audio.clear();
    processor.processBlock(audio, midi);
    midi.clear();
    assert(audio.getMagnitude(0, audio.getNumSamples()) == 0.0f);

    // A program must sound the same regardless of the previously selected program.
    processor.setCurrentProgram(1);
    std::vector<float> woodValues;
    for (auto* item : processor.getParameters()) woodValues.push_back(item->getValue());
    processor.setCurrentProgram(2);
    processor.setCurrentProgram(1);
    for (int i = 0; i < processor.getParameters().size(); ++i)
        assert(std::abs(processor.getParameters()[i]->getValue() - woodValues[static_cast<std::size_t>(i)]) < 1.0e-6f);

    // A legacy state lacking new controls must reset those controls to their defaults.
    processor.getStateInformation(state);
    auto legacyXml = juce::AudioProcessor::getXmlFromBinary(state.getData(), static_cast<int>(state.getSize()));
    assert(legacyXml != nullptr);
    auto legacy = juce::ValueTree::fromXml(*legacyXml);
    legacy.removeChild(legacy.getChildWithProperty("id", "externalLevel"), nullptr);
    for (auto* item : processor.getParameters())
        if (auto* named = dynamic_cast<juce::AudioProcessorParameterWithID*>(item))
            if (named->paramID == "externalLevel") item->setValueNotifyingHost(1.0f);
    auto legacyState = legacy.createXml();
    juce::AudioProcessor::copyXmlToBinary(*legacyState, state);
    processor.setStateInformation(state.getData(), static_cast<int>(state.getSize()));
    for (auto* item : processor.getParameters())
        if (auto* named = dynamic_cast<juce::AudioProcessorParameterWithID*>(item))
            if (named->paramID == "externalLevel") assert(item->getValue() == item->getDefaultValue());

    // Enabled input is excitation only: a silent patch must not pass dry host audio.
    auto layout = processor.getBusesLayout();
    layout.inputBuses.set(0, juce::AudioChannelSet::stereo());
    assert(processor.setBusesLayout(layout));
    for (auto* item : processor.getParameters())
        if (auto* ranged = dynamic_cast<juce::AudioProcessorParameterWithID*>(item))
            if (ranged->paramID == "impact" || ranged->paramID == "noise" || ranged->paramID == "externalLevel")
                item->setValueNotifyingHost(0.0f);
    processor.releaseResources();
    processor.prepareToPlay(48000.0, 256);
    for (int channel = 0; channel < 2; ++channel)
        for (int sample = 0; sample < 256; ++sample) audio.setSample(channel, sample, 0.2f);
    processor.processBlock(audio, midi);
    assert(audio.getMagnitude(0, audio.getNumSamples()) == 0.0f);

    std::cout << "Objekt processor tests passed\n";
    return 0;
}
