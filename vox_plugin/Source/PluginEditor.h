#pragma once
#include "PluginProcessor.h"

/** Phase 1 editor: enough to confirm the plugin is alive and audio is
    reaching it. The BOTC-styled UI is Phase 5. */
class VoxEditor : public juce::AudioProcessorEditor,
                  private juce::Timer
{
public:
    explicit VoxEditor (VoxProcessor&);
    void paint (juce::Graphics&) override;

private:
    void timerCallback() override { repaint(); }
    VoxProcessor& proc;
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VoxEditor)
};
