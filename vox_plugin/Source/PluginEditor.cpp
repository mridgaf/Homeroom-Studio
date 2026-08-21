#include "PluginEditor.h"

VoxEditor::VoxEditor (VoxProcessor& p)
    : AudioProcessorEditor (&p), proc (p)
{
    setSize (420, 180);
    startTimerHz (30);
}

void VoxEditor::paint (juce::Graphics& g)
{
    g.fillAll (juce::Colour (0xff14181f));

    g.setColour (juce::Colour (0xff4a9eff));
    g.setFont (juce::FontOptions (34.0f, juce::Font::bold));
    g.drawText ("VOX", getLocalBounds().removeFromTop (70),
                juce::Justification::centred);

    g.setColour (juce::Colours::grey);
    g.setFont (juce::FontOptions (13.0f));
    g.drawText ("Phase 1 - passthrough", 0, 66, getWidth(), 20,
                juce::Justification::centred);

    // Input level, so "is audio reaching it" is answerable by looking.
    const float peak = juce::jlimit (0.0f, 1.0f, proc.inPeak.load (std::memory_order_relaxed));
    auto meter = juce::Rectangle<int> (40, 110, getWidth() - 80, 22);
    g.setColour (juce::Colour (0xff20262f));
    g.fillRect (meter);
    g.setColour (peak > 0.98f ? juce::Colour (0xffffd23f) : juce::Colour (0xff4a9eff));
    g.fillRect (meter.withWidth (juce::roundToInt (meter.getWidth() * peak)));
}
