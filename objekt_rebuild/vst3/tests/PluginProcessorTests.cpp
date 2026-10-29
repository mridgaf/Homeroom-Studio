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

    std::cout << "Objekt processor tests passed\n";
    return 0;
}
