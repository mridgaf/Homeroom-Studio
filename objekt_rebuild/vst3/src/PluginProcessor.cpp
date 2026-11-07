#include "PluginProcessor.h"

namespace {
using APF = juce::AudioParameterFloat;
using Range = juce::NormalisableRange<float>;

std::unique_ptr<juce::RangedAudioParameter> parameter(const char* id, const char* name, float low, float high, float step, float initial)
{
    return std::make_unique<APF>(juce::ParameterID { id, 1 }, name, Range { low, high, step }, initial);
}
}

ObjektRebuildAudioProcessor::ObjektRebuildAudioProcessor()
    : AudioProcessor(BusesProperties().withInput("Exciter Input", juce::AudioChannelSet::stereo(), false).withOutput("Output", juce::AudioChannelSet::stereo(), true)),
      parameters(*this, nullptr, "ObjektRebuildState", createParameterLayout())
{
}

juce::AudioProcessorValueTreeState::ParameterLayout ObjektRebuildAudioProcessor::createParameterLayout()
{
    juce::AudioProcessorValueTreeState::ParameterLayout layout;
    layout.add(parameter("master", "Master", 0.0f, 1.0f, 0.001f, 0.72f));
    layout.add(parameter("impact", "Impact", 0.0f, 1.0f, 0.001f, 0.82f));
    layout.add(parameter("hardness", "Hardness", 0.0f, 1.0f, 0.001f, 0.68f));
    layout.add(parameter("noise", "Noise", 0.0f, 1.0f, 0.001f, 0.07f));
    layout.add(parameter("modalMix", "Modal Mix", 0.0f, 1.0f, 0.001f, 0.78f));
    layout.add(parameter("modalDecay", "Modal Decay", 0.05f, 8.0f, 0.001f, 2.0f));
    layout.add(parameter("object1Mix", "Object 1 Mix", 0.0f, 1.0f, 0.001f, 0.62f));
    layout.add(parameter("object1Decay", "Object 1 Decay", 0.05f, 8.0f, 0.001f, 1.45f));
    layout.add(parameter("damping", "Damping", 0.0f, 0.98f, 0.001f, 0.34f));
    layout.add(parameter("dispersion", "Dispersion", 0.0f, 1.0f, 0.001f, 0.14f));
    layout.add(parameter("collision", "Collision", 0.0f, 1.0f, 0.001f, 0.08f));
    layout.add(parameter("coupling", "Coupling", 0.0f, 0.55f, 0.001f, 0.10f));
    layout.add(parameter("object2Mix", "Object 2 Mix", 0.0f, 1.0f, 0.001f, 0.42f));
    layout.add(parameter("object2Decay", "Object 2 Decay", 0.05f, 8.0f, 0.001f, 1.10f));
    layout.add(parameter("width", "Width", 0.0f, 1.0f, 0.001f, 0.55f));
    layout.add(parameter("reverb", "Reverb", 0.0f, 0.6f, 0.001f, 0.12f));
    const objekt::Params defaults;
    layout.add(parameter("exciterMix", "exciterMix", 0.0f, 1.0f, 0.001f, defaults.exciterMix));
    layout.add(parameter("pickupDrive", "pickupDrive", 0.0f, 1.0f, 0.001f, defaults.pickupDrive));
    layout.add(parameter("object1Exciter", "object1Exciter", 0.0f, 1.0f, 0.001f, defaults.object1Exciter));
    layout.add(parameter("object1Modal", "object1Modal", 0.0f, 1.0f, 0.001f, defaults.object1Modal));
    layout.add(parameter("object2Exciter", "object2Exciter", 0.0f, 1.0f, 0.001f, defaults.object2Exciter));
    layout.add(parameter("object2Object1", "object2Object1", 0.0f, 1.0f, 0.001f, defaults.object2Object1));
    layout.add(parameter("click", "click", 0.0f, 1.0f, 0.001f, defaults.click));
    layout.add(parameter("impactFrequency", "Impact Frequency", 0.0f, 1.0f, 0.001f, defaults.impactFrequency));
    layout.add(parameter("hardnessVelocity", "Hardness Velocity", -1.0f, 1.0f, 0.001f, defaults.hardnessVelocity));
    layout.add(parameter("impactVelocity", "impactVelocity", 0.0f, 1.0f, 0.001f, defaults.impactVelocity));
    layout.add(parameter("noiseVelocity", "noiseVelocity", 0.0f, 1.0f, 0.001f, defaults.noiseVelocity));
    layout.add(parameter("noiseColor", "noiseColor", 0.0f, 1.0f, 0.001f, defaults.noiseColor));
    layout.add(parameter("noiseSustain", "noiseSustain", 0.0f, 1.0f, 0.001f, defaults.noiseSustain));
    layout.add(parameter("externalLevel", "externalLevel", 0.0f, 1.0f, 0.001f, defaults.externalLevel));
    layout.add(parameter("exciterPan", "exciterPan", -1.0f, 1.0f, 0.001f, defaults.exciterPan));
    layout.add(parameter("modalPan", "modalPan", -1.0f, 1.0f, 0.001f, defaults.modalPan));
    layout.add(parameter("object1Pan", "object1Pan", -1.0f, 1.0f, 0.001f, defaults.object1Pan));
    layout.add(parameter("object2Pan", "object2Pan", -1.0f, 1.0f, 0.001f, defaults.object2Pan));
    layout.add(parameter("pickupSymmetry", "pickupSymmetry", -1.0f, 1.0f, 0.001f, defaults.pickupSymmetry));
    layout.add(parameter("modalTune", "modalTune", -48.0f, 48.0f, 0.001f, defaults.modalTune));
    layout.add(parameter("object1Tune", "object1Tune", -48.0f, 48.0f, 0.001f, defaults.object1Tune));
    layout.add(parameter("object2Tune", "object2Tune", -48.0f, 48.0f, 0.001f, defaults.object2Tune));
    layout.add(parameter("modalStages", "modalStages", 0.0f, 8.0f, 1.0f, defaults.modalStages));
    layout.add(parameter("object1Stages", "object1Stages", 0.0f, 8.0f, 1.0f, defaults.object1Stages));
    layout.add(parameter("object2Stages", "object2Stages", 0.0f, 8.0f, 1.0f, defaults.object2Stages));
    layout.add(parameter("modalKeyTracking", "modalKeyTracking", 0.0f, 8.0f, 1.0f, defaults.modalKeyTracking));
    layout.add(parameter("object1KeyTracking", "object1KeyTracking", 0.0f, 8.0f, 1.0f, defaults.object1KeyTracking));
    layout.add(parameter("object2KeyTracking", "object2KeyTracking", 0.0f, 8.0f, 1.0f, defaults.object2KeyTracking));
    layout.add(parameter("noiseType", "noiseType", 0.0f, 7.0f, 1.0f, defaults.noiseType));
    layout.add(parameter("noiseRate", "noiseRate", 0.01f, 20000.0f, 0.01f, defaults.noiseRate));
    layout.add(parameter("noiseDelay", "noiseDelay", 0.0f, 10.0f, 0.001f, defaults.noiseDelay));
    layout.add(parameter("noiseAttack", "noiseAttack", 0.0f, 10.0f, 0.001f, defaults.noiseAttack));
    layout.add(parameter("noiseDecay", "noiseDecay", 0.001f, 10.0f, 0.001f, defaults.noiseDecay));
    layout.add(parameter("noiseRelease", "noiseRelease", 0.001f, 10.0f, 0.001f, defaults.noiseRelease));
    layout.add(parameter("modalRatios1", "modalRatios 1", 0.01f, 32.0f, 0.001f, defaults.modalRatios[0]));
    layout.add(parameter("modalRatios2", "modalRatios 2", 0.01f, 32.0f, 0.001f, defaults.modalRatios[1]));
    layout.add(parameter("modalRatios3", "modalRatios 3", 0.01f, 32.0f, 0.001f, defaults.modalRatios[2]));
    layout.add(parameter("modalRatios4", "modalRatios 4", 0.01f, 32.0f, 0.001f, defaults.modalRatios[3]));
    layout.add(parameter("modalRatios5", "modalRatios 5", 0.01f, 32.0f, 0.001f, defaults.modalRatios[4]));
    layout.add(parameter("modalRatios6", "modalRatios 6", 0.01f, 32.0f, 0.001f, defaults.modalRatios[5]));
    layout.add(parameter("modalRatios7", "modalRatios 7", 0.01f, 32.0f, 0.001f, defaults.modalRatios[6]));
    layout.add(parameter("modalRatios8", "modalRatios 8", 0.01f, 32.0f, 0.001f, defaults.modalRatios[7]));
    layout.add(parameter("modalGains1", "modalGains 1", 0.0f, 2.0f, 0.001f, defaults.modalGains[0]));
    layout.add(parameter("modalGains2", "modalGains 2", 0.0f, 2.0f, 0.001f, defaults.modalGains[1]));
    layout.add(parameter("modalGains3", "modalGains 3", 0.0f, 2.0f, 0.001f, defaults.modalGains[2]));
    layout.add(parameter("modalGains4", "modalGains 4", 0.0f, 2.0f, 0.001f, defaults.modalGains[3]));
    layout.add(parameter("modalGains5", "modalGains 5", 0.0f, 2.0f, 0.001f, defaults.modalGains[4]));
    layout.add(parameter("modalGains6", "modalGains 6", 0.0f, 2.0f, 0.001f, defaults.modalGains[5]));
    layout.add(parameter("modalGains7", "modalGains 7", 0.0f, 2.0f, 0.001f, defaults.modalGains[6]));
    layout.add(parameter("modalGains8", "modalGains 8", 0.0f, 2.0f, 0.001f, defaults.modalGains[7]));
    layout.add(parameter("modalDecayScales1", "modalDecayScales 1", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[0]));
    layout.add(parameter("modalDecayScales2", "modalDecayScales 2", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[1]));
    layout.add(parameter("modalDecayScales3", "modalDecayScales 3", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[2]));
    layout.add(parameter("modalDecayScales4", "modalDecayScales 4", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[3]));
    layout.add(parameter("modalDecayScales5", "modalDecayScales 5", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[4]));
    layout.add(parameter("modalDecayScales6", "modalDecayScales 6", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[5]));
    layout.add(parameter("modalDecayScales7", "modalDecayScales 7", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[6]));
    layout.add(parameter("modalDecayScales8", "modalDecayScales 8", 0.05f, 8.0f, 0.001f, defaults.modalDecayScales[7]));
    layout.add(parameter("object1Ratios1", "object1Ratios 1", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[0]));
    layout.add(parameter("object1Ratios2", "object1Ratios 2", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[1]));
    layout.add(parameter("object1Ratios3", "object1Ratios 3", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[2]));
    layout.add(parameter("object1Ratios4", "object1Ratios 4", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[3]));
    layout.add(parameter("object1Ratios5", "object1Ratios 5", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[4]));
    layout.add(parameter("object1Ratios6", "object1Ratios 6", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[5]));
    layout.add(parameter("object1Ratios7", "object1Ratios 7", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[6]));
    layout.add(parameter("object1Ratios8", "object1Ratios 8", 0.01f, 32.0f, 0.001f, defaults.object1Ratios[7]));
    layout.add(parameter("object2Ratios1", "object2Ratios 1", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[0]));
    layout.add(parameter("object2Ratios2", "object2Ratios 2", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[1]));
    layout.add(parameter("object2Ratios3", "object2Ratios 3", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[2]));
    layout.add(parameter("object2Ratios4", "object2Ratios 4", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[3]));
    layout.add(parameter("object2Ratios5", "object2Ratios 5", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[4]));
    layout.add(parameter("object2Ratios6", "object2Ratios 6", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[5]));
    layout.add(parameter("object2Ratios7", "object2Ratios 7", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[6]));
    layout.add(parameter("object2Ratios8", "object2Ratios 8", 0.01f, 32.0f, 0.001f, defaults.object2Ratios[7]));
    layout.add(parameter("object1Gains1", "object1Gains 1", 0.0f, 2.0f, 0.001f, defaults.object1Gains[0]));
    layout.add(parameter("object1Gains2", "object1Gains 2", 0.0f, 2.0f, 0.001f, defaults.object1Gains[1]));
    layout.add(parameter("object1Gains3", "object1Gains 3", 0.0f, 2.0f, 0.001f, defaults.object1Gains[2]));
    layout.add(parameter("object1Gains4", "object1Gains 4", 0.0f, 2.0f, 0.001f, defaults.object1Gains[3]));
    layout.add(parameter("object1Gains5", "object1Gains 5", 0.0f, 2.0f, 0.001f, defaults.object1Gains[4]));
    layout.add(parameter("object1Gains6", "object1Gains 6", 0.0f, 2.0f, 0.001f, defaults.object1Gains[5]));
    layout.add(parameter("object1Gains7", "object1Gains 7", 0.0f, 2.0f, 0.001f, defaults.object1Gains[6]));
    layout.add(parameter("object1Gains8", "object1Gains 8", 0.0f, 2.0f, 0.001f, defaults.object1Gains[7]));
    layout.add(parameter("object2Gains1", "object2Gains 1", 0.0f, 2.0f, 0.001f, defaults.object2Gains[0]));
    layout.add(parameter("object2Gains2", "object2Gains 2", 0.0f, 2.0f, 0.001f, defaults.object2Gains[1]));
    layout.add(parameter("object2Gains3", "object2Gains 3", 0.0f, 2.0f, 0.001f, defaults.object2Gains[2]));
    layout.add(parameter("object2Gains4", "object2Gains 4", 0.0f, 2.0f, 0.001f, defaults.object2Gains[3]));
    layout.add(parameter("object2Gains5", "object2Gains 5", 0.0f, 2.0f, 0.001f, defaults.object2Gains[4]));
    layout.add(parameter("object2Gains6", "object2Gains 6", 0.0f, 2.0f, 0.001f, defaults.object2Gains[5]));
    layout.add(parameter("object2Gains7", "object2Gains 7", 0.0f, 2.0f, 0.001f, defaults.object2Gains[6]));
    layout.add(parameter("object2Gains8", "object2Gains 8", 0.0f, 2.0f, 0.001f, defaults.object2Gains[7]));
    layout.add(parameter("object1Polarity1", "object1Polarity 1", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[0]));
    layout.add(parameter("object1Polarity2", "object1Polarity 2", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[1]));
    layout.add(parameter("object1Polarity3", "object1Polarity 3", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[2]));
    layout.add(parameter("object1Polarity4", "object1Polarity 4", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[3]));
    layout.add(parameter("object1Polarity5", "object1Polarity 5", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[4]));
    layout.add(parameter("object1Polarity6", "object1Polarity 6", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[5]));
    layout.add(parameter("object1Polarity7", "object1Polarity 7", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[6]));
    layout.add(parameter("object1Polarity8", "object1Polarity 8", -1.0f, 1.0f, 2.0f, defaults.object1Polarity[7]));
    layout.add(parameter("object2Polarity1", "object2Polarity 1", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[0]));
    layout.add(parameter("object2Polarity2", "object2Polarity 2", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[1]));
    layout.add(parameter("object2Polarity3", "object2Polarity 3", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[2]));
    layout.add(parameter("object2Polarity4", "object2Polarity 4", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[3]));
    layout.add(parameter("object2Polarity5", "object2Polarity 5", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[4]));
    layout.add(parameter("object2Polarity6", "object2Polarity 6", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[5]));
    layout.add(parameter("object2Polarity7", "object2Polarity 7", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[6]));
    layout.add(parameter("object2Polarity8", "object2Polarity 8", -1.0f, 1.0f, 2.0f, defaults.object2Polarity[7]));
    layout.add(parameter("keyMode", "keyMode", 0.0f, 2.0f, 1.0f, defaults.keyMode));
    layout.add(parameter("portamento", "portamento", 0.0f, 5.0f, 0.001f, defaults.portamento));
    layout.add(parameter("effects_lowDb", "effects lowDb", -24.0f, 24.0f, 0.001f, defaults.effects.lowDb));
    layout.add(parameter("effects_midDb", "effects midDb", -24.0f, 24.0f, 0.001f, defaults.effects.midDb));
    layout.add(parameter("effects_highDb", "effects highDb", -24.0f, 24.0f, 0.001f, defaults.effects.highDb));
    layout.add(parameter("effects_makeupDb", "effects makeupDb", -24.0f, 24.0f, 0.001f, defaults.effects.makeupDb));
    layout.add(parameter("effects_lowHz", "effects lowHz", 20.0f, 20000.0f, 0.01f, defaults.effects.lowHz));
    layout.add(parameter("effects_midHz", "effects midHz", 20.0f, 20000.0f, 0.01f, defaults.effects.midHz));
    layout.add(parameter("effects_highHz", "effects highHz", 20.0f, 20000.0f, 0.01f, defaults.effects.highHz));
    layout.add(parameter("effects_ringHz", "effects ringHz", 20.0f, 20000.0f, 0.01f, defaults.effects.ringHz));
    layout.add(parameter("effects_holdHz", "effects holdHz", 20.0f, 20000.0f, 0.01f, defaults.effects.holdHz));
    layout.add(parameter("effects_midQ", "effects midQ", 0.1f, 10.0f, 0.001f, defaults.effects.midQ));
    layout.add(parameter("effects_distortionMode", "effects distortionMode", 0.0f, 5.0f, 1.0f, defaults.effects.distortionMode));
    layout.add(parameter("effects_drive", "effects drive", 1.0f, 30.0f, 0.001f, defaults.effects.drive));
    layout.add(parameter("effects_distortionMix", "effects distortionMix", 0.0f, 1.0f, 0.001f, defaults.effects.distortionMix));
    layout.add(parameter("effects_compressorMix", "effects compressorMix", 0.0f, 1.0f, 0.001f, defaults.effects.compressorMix));
    layout.add(parameter("effects_delayMix", "Delay Send", 0.0f, 1.0f, 0.001f, defaults.effects.delayMix));
    layout.add(parameter("effects_reverbMix", "Reverb Send", 0.0f, 1.0f, 0.001f, defaults.effects.reverbMix));
    layout.add(parameter("effects_earlyLevel", "effects earlyLevel", 0.0f, 1.0f, 0.001f, defaults.effects.earlyLevel));
    layout.add(parameter("effects_thresholdDb", "effects thresholdDb", -60.0f, 0.0f, 0.001f, defaults.effects.thresholdDb));
    layout.add(parameter("effects_ratio", "effects ratio", 1.0f, 20.0f, 0.001f, defaults.effects.ratio));
    layout.add(parameter("effects_attackMs", "effects attackMs", 0.1f, 200.0f, 0.001f, defaults.effects.attackMs));
    layout.add(parameter("effects_releaseMs", "effects releaseMs", 1.0f, 2000.0f, 0.001f, defaults.effects.releaseMs));
    layout.add(parameter("effects_delaySeconds", "effects delaySeconds", 0.001f, 4.0f, 0.001f, defaults.effects.delaySeconds));
    layout.add(parameter("effects_delayFeedback", "effects delayFeedback", 0.0f, 0.95f, 0.001f, defaults.effects.delayFeedback));
    layout.add(parameter("effects_delayBeats", "effects delayBeats", 0.0625f, 8.0f, 0.0625f, defaults.effects.delayBeats));
    layout.add(parameter("effects_delayPan", "effects delayPan", -1.0f, 1.0f, 0.001f, defaults.effects.delayPan));
    layout.add(parameter("effects_delaySync", "effects delaySync", 0.0f, 1.0f, 1.0f, defaults.effects.delaySync));
    layout.add(parameter("effects_pingPong", "effects pingPong", 0.0f, 1.0f, 1.0f, defaults.effects.pingPong));
    layout.add(parameter("effects_reverbDecay", "effects reverbDecay", 0.1f, 20.0f, 0.001f, defaults.effects.reverbDecay));
    layout.add(parameter("effects_reverbDamping", "effects reverbDamping", 0.0f, 0.99f, 0.001f, defaults.effects.reverbDamping));
    layout.add(parameter("effects_reverbType", "effects reverbType", 0.0f, 2.0f, 1.0f, defaults.effects.reverbType));
    layout.add(parameter("modulation_lfos0_rate", "modulation lfos 0 rate", 0.001f, 100.0f, 0.001f, defaults.modulation.lfos[0].rate));
    layout.add(parameter("modulation_lfos0_shape", "modulation lfos 0 shape", 0.0f, 3.0f, 1.0f, defaults.modulation.lfos[0].shape));
    layout.add(parameter("modulation_lfos0_sync", "modulation lfos 0 sync", 0.0f, 1.0f, 1.0f, defaults.modulation.lfos[0].sync));
    layout.add(parameter("modulation_macros0", "modulation macros 0", -1.0f, 1.0f, 0.001f, defaults.modulation.macros[0]));
    layout.add(parameter("modulation_lfos1_rate", "modulation lfos 1 rate", 0.001f, 100.0f, 0.001f, defaults.modulation.lfos[1].rate));
    layout.add(parameter("modulation_lfos1_shape", "modulation lfos 1 shape", 0.0f, 3.0f, 1.0f, defaults.modulation.lfos[1].shape));
    layout.add(parameter("modulation_lfos1_sync", "modulation lfos 1 sync", 0.0f, 1.0f, 1.0f, defaults.modulation.lfos[1].sync));
    layout.add(parameter("modulation_macros1", "modulation macros 1", -1.0f, 1.0f, 0.001f, defaults.modulation.macros[1]));
    layout.add(parameter("modulation_steps0", "modulation steps 0", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[0]));
    layout.add(parameter("modulation_steps1", "modulation steps 1", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[1]));
    layout.add(parameter("modulation_steps2", "modulation steps 2", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[2]));
    layout.add(parameter("modulation_steps3", "modulation steps 3", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[3]));
    layout.add(parameter("modulation_steps4", "modulation steps 4", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[4]));
    layout.add(parameter("modulation_steps5", "modulation steps 5", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[5]));
    layout.add(parameter("modulation_steps6", "modulation steps 6", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[6]));
    layout.add(parameter("modulation_steps7", "modulation steps 7", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[7]));
    layout.add(parameter("modulation_steps8", "modulation steps 8", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[8]));
    layout.add(parameter("modulation_steps9", "modulation steps 9", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[9]));
    layout.add(parameter("modulation_steps10", "modulation steps 10", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[10]));
    layout.add(parameter("modulation_steps11", "modulation steps 11", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[11]));
    layout.add(parameter("modulation_steps12", "modulation steps 12", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[12]));
    layout.add(parameter("modulation_steps13", "modulation steps 13", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[13]));
    layout.add(parameter("modulation_steps14", "modulation steps 14", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[14]));
    layout.add(parameter("modulation_steps15", "modulation steps 15", -1.0f, 1.0f, 0.001f, defaults.modulation.steps[15]));
    layout.add(parameter("modulation_stepCount", "modulation stepCount", 1.0f, 16.0f, 1.0f, defaults.modulation.stepCount));
    layout.add(parameter("modulation_curveRate", "modulation curveRate", 0.001f, 100.0f, 0.001f, defaults.modulation.curveRate));
    layout.add(parameter("modulation_curveSync", "modulation curveSync", 0.0f, 1.0f, 1.0f, defaults.modulation.curveSync));
    layout.add(parameter("modulation_curveSmooth", "modulation curveSmooth", 0.0f, 1.0f, 1.0f, defaults.modulation.curveSmooth));
    layout.add(parameter("modulation_buses0_source", "modulation buses 0 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[0].source));
    layout.add(parameter("modulation_buses0_scale", "modulation buses 0 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[0].scale));
    layout.add(parameter("modulation_buses0_target1", "modulation buses 0 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[0].target1));
    layout.add(parameter("modulation_buses0_target2", "modulation buses 0 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[0].target2));
    layout.add(parameter("modulation_buses0_amount1", "modulation buses 0 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[0].amount1));
    layout.add(parameter("modulation_buses0_amount2", "modulation buses 0 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[0].amount2));
    layout.add(parameter("modulation_buses1_source", "modulation buses 1 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[1].source));
    layout.add(parameter("modulation_buses1_scale", "modulation buses 1 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[1].scale));
    layout.add(parameter("modulation_buses1_target1", "modulation buses 1 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[1].target1));
    layout.add(parameter("modulation_buses1_target2", "modulation buses 1 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[1].target2));
    layout.add(parameter("modulation_buses1_amount1", "modulation buses 1 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[1].amount1));
    layout.add(parameter("modulation_buses1_amount2", "modulation buses 1 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[1].amount2));
    layout.add(parameter("modulation_buses2_source", "modulation buses 2 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[2].source));
    layout.add(parameter("modulation_buses2_scale", "modulation buses 2 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[2].scale));
    layout.add(parameter("modulation_buses2_target1", "modulation buses 2 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[2].target1));
    layout.add(parameter("modulation_buses2_target2", "modulation buses 2 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[2].target2));
    layout.add(parameter("modulation_buses2_amount1", "modulation buses 2 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[2].amount1));
    layout.add(parameter("modulation_buses2_amount2", "modulation buses 2 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[2].amount2));
    layout.add(parameter("modulation_buses3_source", "modulation buses 3 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[3].source));
    layout.add(parameter("modulation_buses3_scale", "modulation buses 3 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[3].scale));
    layout.add(parameter("modulation_buses3_target1", "modulation buses 3 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[3].target1));
    layout.add(parameter("modulation_buses3_target2", "modulation buses 3 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[3].target2));
    layout.add(parameter("modulation_buses3_amount1", "modulation buses 3 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[3].amount1));
    layout.add(parameter("modulation_buses3_amount2", "modulation buses 3 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[3].amount2));
    layout.add(parameter("modulation_buses4_source", "modulation buses 4 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[4].source));
    layout.add(parameter("modulation_buses4_scale", "modulation buses 4 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[4].scale));
    layout.add(parameter("modulation_buses4_target1", "modulation buses 4 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[4].target1));
    layout.add(parameter("modulation_buses4_target2", "modulation buses 4 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[4].target2));
    layout.add(parameter("modulation_buses4_amount1", "modulation buses 4 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[4].amount1));
    layout.add(parameter("modulation_buses4_amount2", "modulation buses 4 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[4].amount2));
    layout.add(parameter("modulation_buses5_source", "modulation buses 5 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[5].source));
    layout.add(parameter("modulation_buses5_scale", "modulation buses 5 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[5].scale));
    layout.add(parameter("modulation_buses5_target1", "modulation buses 5 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[5].target1));
    layout.add(parameter("modulation_buses5_target2", "modulation buses 5 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[5].target2));
    layout.add(parameter("modulation_buses5_amount1", "modulation buses 5 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[5].amount1));
    layout.add(parameter("modulation_buses5_amount2", "modulation buses 5 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[5].amount2));
    layout.add(parameter("modulation_buses6_source", "modulation buses 6 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[6].source));
    layout.add(parameter("modulation_buses6_scale", "modulation buses 6 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[6].scale));
    layout.add(parameter("modulation_buses6_target1", "modulation buses 6 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[6].target1));
    layout.add(parameter("modulation_buses6_target2", "modulation buses 6 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[6].target2));
    layout.add(parameter("modulation_buses6_amount1", "modulation buses 6 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[6].amount1));
    layout.add(parameter("modulation_buses6_amount2", "modulation buses 6 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[6].amount2));
    layout.add(parameter("modulation_buses7_source", "modulation buses 7 source", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[7].source));
    layout.add(parameter("modulation_buses7_scale", "modulation buses 7 scale", 0.0f, 10.0f, 1.0f, defaults.modulation.buses[7].scale));
    layout.add(parameter("modulation_buses7_target1", "modulation buses 7 target1", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[7].target1));
    layout.add(parameter("modulation_buses7_target2", "modulation buses 7 target2", 0.0f, 15.0f, 1.0f, defaults.modulation.buses[7].target2));
    layout.add(parameter("modulation_buses7_amount1", "modulation buses 7 amount1", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[7].amount1));
    layout.add(parameter("modulation_buses7_amount2", "modulation buses 7 amount2", -2.0f, 2.0f, 0.001f, defaults.modulation.buses[7].amount2));
    layout.add(parameter("bendRange", "Pitch Bend Range", 0.0f, 12.0f, 1.0f, 2.0f));
    juce::StringArray orders;
    std::array<int, 5> order {0, 1, 2, 3, 4};
    const std::array<const char*, 5> effectNames {"EQ", "Dist", "Comp", "Delay", "Reverb"};
    do {
        juce::String name;
        for (int slot : order) { if (name.isNotEmpty()) name += " > "; name += effectNames[slot]; }
        orders.add(name);
    } while (std::next_permutation(order.begin(), order.end()));
    layout.add(std::make_unique<juce::AudioParameterChoice>(juce::ParameterID {"effectOrder", 1}, "Effects Order", orders, 0));
    return layout;
}

void ObjektRebuildAudioProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
    sustainDown = false;
    pitchWheel = channelPressure = modWheel = 0;
    deferredRelease.fill(false);
    engine.prepare(sampleRate, samplesPerBlock);
}

void ObjektRebuildAudioProcessor::releaseResources()
{
    engine.reset();
}

bool ObjektRebuildAudioProcessor::isBusesLayoutSupported(const BusesLayout& layouts) const
{
    return (layouts.getMainInputChannelSet().isDisabled() || layouts.getMainInputChannelSet() == juce::AudioChannelSet::stereo() || layouts.getMainInputChannelSet() == juce::AudioChannelSet::mono())
        && layouts.getMainOutputChannelSet() == juce::AudioChannelSet::stereo();
}

objekt::Params ObjektRebuildAudioProcessor::snapshotParameters() const noexcept
{
    auto value = [this](const char* id) { return parameters.getRawParameterValue(id)->load(); };
    objekt::Params result;
    result.master = value("master");
    result.impact = value("impact");
    result.hardness = value("hardness");
    result.noise = value("noise");
    result.modalMix = value("modalMix");
    result.modalDecay = value("modalDecay");
    result.object1Mix = value("object1Mix");
    result.object1Decay = value("object1Decay");
    result.damping = value("damping");
    result.dispersion = value("dispersion");
    result.collision = value("collision");
    result.coupling = value("coupling");
    result.object2Mix = value("object2Mix");
    result.object2Decay = value("object2Decay");
    result.width = value("width");
    result.reverb = value("reverb");
    result.exciterMix = value("exciterMix");
    result.pickupDrive = value("pickupDrive");
    result.object1Exciter = value("object1Exciter");
    result.object1Modal = value("object1Modal");
    result.object2Exciter = value("object2Exciter");
    result.object2Object1 = value("object2Object1");
    result.click = value("click");
    result.impactFrequency = value("impactFrequency");
    result.hardnessVelocity = value("hardnessVelocity");
    result.impactVelocity = value("impactVelocity");
    result.noiseVelocity = value("noiseVelocity");
    result.noiseColor = value("noiseColor");
    result.noiseSustain = value("noiseSustain");
    result.externalLevel = value("externalLevel");
    result.exciterPan = value("exciterPan");
    result.modalPan = value("modalPan");
    result.object1Pan = value("object1Pan");
    result.object2Pan = value("object2Pan");
    result.pickupSymmetry = value("pickupSymmetry");
    result.modalTune = value("modalTune");
    result.object1Tune = value("object1Tune");
    result.object2Tune = value("object2Tune");
    result.modalStages = static_cast<int>(value("modalStages"));
    result.object1Stages = static_cast<int>(value("object1Stages"));
    result.object2Stages = static_cast<int>(value("object2Stages"));
    result.modalKeyTracking = static_cast<int>(value("modalKeyTracking"));
    result.object1KeyTracking = static_cast<int>(value("object1KeyTracking"));
    result.object2KeyTracking = static_cast<int>(value("object2KeyTracking"));
    result.noiseType = static_cast<int>(value("noiseType"));
    result.noiseRate = value("noiseRate");
    result.noiseDelay = value("noiseDelay");
    result.noiseAttack = value("noiseAttack");
    result.noiseDecay = value("noiseDecay");
    result.noiseRelease = value("noiseRelease");
    result.modalRatios[0] = value("modalRatios1");
    result.modalRatios[1] = value("modalRatios2");
    result.modalRatios[2] = value("modalRatios3");
    result.modalRatios[3] = value("modalRatios4");
    result.modalRatios[4] = value("modalRatios5");
    result.modalRatios[5] = value("modalRatios6");
    result.modalRatios[6] = value("modalRatios7");
    result.modalRatios[7] = value("modalRatios8");
    result.modalGains[0] = value("modalGains1");
    result.modalGains[1] = value("modalGains2");
    result.modalGains[2] = value("modalGains3");
    result.modalGains[3] = value("modalGains4");
    result.modalGains[4] = value("modalGains5");
    result.modalGains[5] = value("modalGains6");
    result.modalGains[6] = value("modalGains7");
    result.modalGains[7] = value("modalGains8");
    result.modalDecayScales[0] = value("modalDecayScales1");
    result.modalDecayScales[1] = value("modalDecayScales2");
    result.modalDecayScales[2] = value("modalDecayScales3");
    result.modalDecayScales[3] = value("modalDecayScales4");
    result.modalDecayScales[4] = value("modalDecayScales5");
    result.modalDecayScales[5] = value("modalDecayScales6");
    result.modalDecayScales[6] = value("modalDecayScales7");
    result.modalDecayScales[7] = value("modalDecayScales8");
    result.object1Ratios[0] = value("object1Ratios1");
    result.object1Ratios[1] = value("object1Ratios2");
    result.object1Ratios[2] = value("object1Ratios3");
    result.object1Ratios[3] = value("object1Ratios4");
    result.object1Ratios[4] = value("object1Ratios5");
    result.object1Ratios[5] = value("object1Ratios6");
    result.object1Ratios[6] = value("object1Ratios7");
    result.object1Ratios[7] = value("object1Ratios8");
    result.object2Ratios[0] = value("object2Ratios1");
    result.object2Ratios[1] = value("object2Ratios2");
    result.object2Ratios[2] = value("object2Ratios3");
    result.object2Ratios[3] = value("object2Ratios4");
    result.object2Ratios[4] = value("object2Ratios5");
    result.object2Ratios[5] = value("object2Ratios6");
    result.object2Ratios[6] = value("object2Ratios7");
    result.object2Ratios[7] = value("object2Ratios8");
    result.object1Gains[0] = value("object1Gains1");
    result.object1Gains[1] = value("object1Gains2");
    result.object1Gains[2] = value("object1Gains3");
    result.object1Gains[3] = value("object1Gains4");
    result.object1Gains[4] = value("object1Gains5");
    result.object1Gains[5] = value("object1Gains6");
    result.object1Gains[6] = value("object1Gains7");
    result.object1Gains[7] = value("object1Gains8");
    result.object2Gains[0] = value("object2Gains1");
    result.object2Gains[1] = value("object2Gains2");
    result.object2Gains[2] = value("object2Gains3");
    result.object2Gains[3] = value("object2Gains4");
    result.object2Gains[4] = value("object2Gains5");
    result.object2Gains[5] = value("object2Gains6");
    result.object2Gains[6] = value("object2Gains7");
    result.object2Gains[7] = value("object2Gains8");
    result.object1Polarity[0] = value("object1Polarity1");
    result.object1Polarity[1] = value("object1Polarity2");
    result.object1Polarity[2] = value("object1Polarity3");
    result.object1Polarity[3] = value("object1Polarity4");
    result.object1Polarity[4] = value("object1Polarity5");
    result.object1Polarity[5] = value("object1Polarity6");
    result.object1Polarity[6] = value("object1Polarity7");
    result.object1Polarity[7] = value("object1Polarity8");
    result.object2Polarity[0] = value("object2Polarity1");
    result.object2Polarity[1] = value("object2Polarity2");
    result.object2Polarity[2] = value("object2Polarity3");
    result.object2Polarity[3] = value("object2Polarity4");
    result.object2Polarity[4] = value("object2Polarity5");
    result.object2Polarity[5] = value("object2Polarity6");
    result.object2Polarity[6] = value("object2Polarity7");
    result.object2Polarity[7] = value("object2Polarity8");
    result.keyMode = static_cast<int>(value("keyMode"));
    result.portamento = value("portamento");
    result.effects.lowDb = value("effects_lowDb");
    result.effects.midDb = value("effects_midDb");
    result.effects.highDb = value("effects_highDb");
    result.effects.makeupDb = value("effects_makeupDb");
    result.effects.lowHz = value("effects_lowHz");
    result.effects.midHz = value("effects_midHz");
    result.effects.highHz = value("effects_highHz");
    result.effects.ringHz = value("effects_ringHz");
    result.effects.holdHz = value("effects_holdHz");
    result.effects.midQ = value("effects_midQ");
    result.effects.distortionMode = static_cast<int>(value("effects_distortionMode"));
    result.effects.drive = value("effects_drive");
    result.effects.distortionMix = value("effects_distortionMix");
    result.effects.compressorMix = value("effects_compressorMix");
    result.effects.delayMix = value("effects_delayMix");
    result.effects.reverbMix = value("effects_reverbMix");
    result.effects.earlyLevel = value("effects_earlyLevel");
    result.effects.thresholdDb = value("effects_thresholdDb");
    result.effects.ratio = value("effects_ratio");
    result.effects.attackMs = value("effects_attackMs");
    result.effects.releaseMs = value("effects_releaseMs");
    result.effects.delaySeconds = value("effects_delaySeconds");
    result.effects.delayFeedback = value("effects_delayFeedback");
    result.effects.delayBeats = value("effects_delayBeats");
    result.effects.delayPan = value("effects_delayPan");
    result.effects.delaySync = static_cast<bool>(value("effects_delaySync"));
    result.effects.pingPong = static_cast<bool>(value("effects_pingPong"));
    result.effects.reverbDecay = value("effects_reverbDecay");
    result.effects.reverbDamping = value("effects_reverbDamping");
    result.effects.reverbType = static_cast<int>(value("effects_reverbType"));
    result.modulation.lfos[0].rate = value("modulation_lfos0_rate");
    result.modulation.lfos[0].shape = static_cast<int>(value("modulation_lfos0_shape"));
    result.modulation.lfos[0].sync = static_cast<bool>(value("modulation_lfos0_sync"));
    result.modulation.macros[0] = value("modulation_macros0");
    result.modulation.lfos[1].rate = value("modulation_lfos1_rate");
    result.modulation.lfos[1].shape = static_cast<int>(value("modulation_lfos1_shape"));
    result.modulation.lfos[1].sync = static_cast<bool>(value("modulation_lfos1_sync"));
    result.modulation.macros[1] = value("modulation_macros1");
    result.modulation.steps[0] = value("modulation_steps0");
    result.modulation.steps[1] = value("modulation_steps1");
    result.modulation.steps[2] = value("modulation_steps2");
    result.modulation.steps[3] = value("modulation_steps3");
    result.modulation.steps[4] = value("modulation_steps4");
    result.modulation.steps[5] = value("modulation_steps5");
    result.modulation.steps[6] = value("modulation_steps6");
    result.modulation.steps[7] = value("modulation_steps7");
    result.modulation.steps[8] = value("modulation_steps8");
    result.modulation.steps[9] = value("modulation_steps9");
    result.modulation.steps[10] = value("modulation_steps10");
    result.modulation.steps[11] = value("modulation_steps11");
    result.modulation.steps[12] = value("modulation_steps12");
    result.modulation.steps[13] = value("modulation_steps13");
    result.modulation.steps[14] = value("modulation_steps14");
    result.modulation.steps[15] = value("modulation_steps15");
    result.modulation.stepCount = static_cast<int>(value("modulation_stepCount"));
    result.modulation.curveRate = value("modulation_curveRate");
    result.modulation.curveSync = static_cast<bool>(value("modulation_curveSync"));
    result.modulation.curveSmooth = static_cast<bool>(value("modulation_curveSmooth"));
    result.modulation.buses[0].source = static_cast<int>(value("modulation_buses0_source"));
    result.modulation.buses[0].scale = static_cast<int>(value("modulation_buses0_scale"));
    result.modulation.buses[0].target1 = static_cast<int>(value("modulation_buses0_target1"));
    result.modulation.buses[0].target2 = static_cast<int>(value("modulation_buses0_target2"));
    result.modulation.buses[0].amount1 = value("modulation_buses0_amount1");
    result.modulation.buses[0].amount2 = value("modulation_buses0_amount2");
    result.modulation.buses[1].source = static_cast<int>(value("modulation_buses1_source"));
    result.modulation.buses[1].scale = static_cast<int>(value("modulation_buses1_scale"));
    result.modulation.buses[1].target1 = static_cast<int>(value("modulation_buses1_target1"));
    result.modulation.buses[1].target2 = static_cast<int>(value("modulation_buses1_target2"));
    result.modulation.buses[1].amount1 = value("modulation_buses1_amount1");
    result.modulation.buses[1].amount2 = value("modulation_buses1_amount2");
    result.modulation.buses[2].source = static_cast<int>(value("modulation_buses2_source"));
    result.modulation.buses[2].scale = static_cast<int>(value("modulation_buses2_scale"));
    result.modulation.buses[2].target1 = static_cast<int>(value("modulation_buses2_target1"));
    result.modulation.buses[2].target2 = static_cast<int>(value("modulation_buses2_target2"));
    result.modulation.buses[2].amount1 = value("modulation_buses2_amount1");
    result.modulation.buses[2].amount2 = value("modulation_buses2_amount2");
    result.modulation.buses[3].source = static_cast<int>(value("modulation_buses3_source"));
    result.modulation.buses[3].scale = static_cast<int>(value("modulation_buses3_scale"));
    result.modulation.buses[3].target1 = static_cast<int>(value("modulation_buses3_target1"));
    result.modulation.buses[3].target2 = static_cast<int>(value("modulation_buses3_target2"));
    result.modulation.buses[3].amount1 = value("modulation_buses3_amount1");
    result.modulation.buses[3].amount2 = value("modulation_buses3_amount2");
    result.modulation.buses[4].source = static_cast<int>(value("modulation_buses4_source"));
    result.modulation.buses[4].scale = static_cast<int>(value("modulation_buses4_scale"));
    result.modulation.buses[4].target1 = static_cast<int>(value("modulation_buses4_target1"));
    result.modulation.buses[4].target2 = static_cast<int>(value("modulation_buses4_target2"));
    result.modulation.buses[4].amount1 = value("modulation_buses4_amount1");
    result.modulation.buses[4].amount2 = value("modulation_buses4_amount2");
    result.modulation.buses[5].source = static_cast<int>(value("modulation_buses5_source"));
    result.modulation.buses[5].scale = static_cast<int>(value("modulation_buses5_scale"));
    result.modulation.buses[5].target1 = static_cast<int>(value("modulation_buses5_target1"));
    result.modulation.buses[5].target2 = static_cast<int>(value("modulation_buses5_target2"));
    result.modulation.buses[5].amount1 = value("modulation_buses5_amount1");
    result.modulation.buses[5].amount2 = value("modulation_buses5_amount2");
    result.modulation.buses[6].source = static_cast<int>(value("modulation_buses6_source"));
    result.modulation.buses[6].scale = static_cast<int>(value("modulation_buses6_scale"));
    result.modulation.buses[6].target1 = static_cast<int>(value("modulation_buses6_target1"));
    result.modulation.buses[6].target2 = static_cast<int>(value("modulation_buses6_target2"));
    result.modulation.buses[6].amount1 = value("modulation_buses6_amount1");
    result.modulation.buses[6].amount2 = value("modulation_buses6_amount2");
    result.modulation.buses[7].source = static_cast<int>(value("modulation_buses7_source"));
    result.modulation.buses[7].scale = static_cast<int>(value("modulation_buses7_scale"));
    result.modulation.buses[7].target1 = static_cast<int>(value("modulation_buses7_target1"));
    result.modulation.buses[7].target2 = static_cast<int>(value("modulation_buses7_target2"));
    result.modulation.buses[7].amount1 = value("modulation_buses7_amount1");
    result.modulation.buses[7].amount2 = value("modulation_buses7_amount2");
    for (int i = 0, permutation = static_cast<int>(value("effectOrder")); i < permutation; ++i)
        std::next_permutation(result.effects.order.begin(), result.effects.order.end());
    result.pitchBendSemitones = pitchWheel * value("bendRange");
    result.pressure = channelPressure;
    result.wheel = modWheel;
    return result;
}

void ObjektRebuildAudioProcessor::renderSegment(juce::AudioBuffer<float>& buffer, int startSample, int numSamples, const objekt::Params& params)
{
    if (numSamples <= 0)
        return;
    const auto* inputLeft = getTotalNumInputChannels() > 0 ? buffer.getReadPointer(0, startSample) : nullptr;
    const auto* inputRight = getTotalNumInputChannels() > 1 ? buffer.getReadPointer(1, startSample) : inputLeft;
    engine.process(buffer.getWritePointer(0, startSample), buffer.getWritePointer(1, startSample), numSamples, params, inputLeft, inputRight);
}

void ObjektRebuildAudioProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midi)
{
    juce::ScopedNoDenormals noDenormals;
    if (getTotalNumInputChannels() == 0) buffer.clear();
    auto values = snapshotParameters();
    if (auto* playHead = getPlayHead())
        if (auto position = playHead->getPosition())
            if (auto bpm = position->getBpm())
                values.bpm = values.effects.tempo = static_cast<float>(*bpm);
    int cursor = 0;
    for (const auto metadata : midi)
    {
        const auto position = juce::jlimit(cursor, buffer.getNumSamples(), metadata.samplePosition);
        renderSegment(buffer, cursor, position - cursor, values);
        const auto message = metadata.getMessage();
        if (message.isNoteOn())
        {
            deferredRelease[static_cast<std::size_t>(message.getNoteNumber())] = false;
            engine.noteOn(message.getNoteNumber(), message.getFloatVelocity(), values);
        }
        else if (message.isNoteOff())
        {
            if (sustainDown)
                deferredRelease[static_cast<std::size_t>(message.getNoteNumber())] = true;
            else
                engine.noteOff(message.getNoteNumber());
        }
        else if (message.isController() && message.getControllerNumber() == 64)
        {
            sustainDown = message.getControllerValue() >= 64;
            if (!sustainDown)
                for (int note = 0; note < 128; ++note)
                    if (deferredRelease[static_cast<std::size_t>(note)])
                    {
                        engine.noteOff(note);
                        deferredRelease[static_cast<std::size_t>(note)] = false;
                    }
        }
        else if (message.isPitchWheel())
        {
            pitchWheel = (message.getPitchWheelValue() - 8192) / 8192.0f;
            values.pitchBendSemitones = pitchWheel * parameters.getRawParameterValue("bendRange")->load();
        }
        else if (message.isChannelPressure())
            values.pressure = channelPressure = message.getChannelPressureValue() / 127.0f;
        else if (message.isController() && message.getControllerNumber() == 1)
            values.wheel = modWheel = message.getControllerValue() / 127.0f;
        else if (message.isAllSoundOff())
        {
            engine.reset();
            deferredRelease.fill(false);
            sustainDown = false;
        }
        else if (message.isAllNotesOff())
        {
            engine.allNotesOff();
            deferredRelease.fill(false);
        }
        cursor = position;
    }
    renderSegment(buffer, cursor, buffer.getNumSamples() - cursor, values);
}

juce::AudioProcessorEditor* ObjektRebuildAudioProcessor::createEditor()
{
    return new juce::GenericAudioProcessorEditor(*this);
}

void ObjektRebuildAudioProcessor::setParameterActual(const char* id, float value)
{
    if (auto* ranged = dynamic_cast<juce::RangedAudioParameter*>(parameters.getParameter(id)))
        ranged->setValueNotifyingHost(ranged->convertTo0to1(value));
}

void ObjektRebuildAudioProcessor::setCurrentProgram(int index)
{
    currentProgram = juce::jlimit(0, getNumPrograms() - 1, index);
    for (auto* item : getParameters())
        item->setValueNotifyingHost(item->getDefaultValue());
    switch (currentProgram)
    {
        case 0: // Glass Bell
            setParameterActual("impact", 0.9f); setParameterActual("hardness", 0.78f); setParameterActual("noise", 0.025f);
            setParameterActual("modalMix", 0.92f); setParameterActual("modalDecay", 3.1f);
            setParameterActual("object1Mix", 0.34f); setParameterActual("object1Decay", 2.0f);
            setParameterActual("object2Mix", 0.18f); setParameterActual("object2Decay", 1.35f);
            setParameterActual("damping", 0.24f); setParameterActual("dispersion", 0.18f); setParameterActual("collision", 0.03f);
            setParameterActual("coupling", 0.04f); setParameterActual("width", 0.68f); setParameterActual("reverb", 0.18f);
            break;
        case 1: // Wood Mallet
            setParameterActual("impact", 0.92f); setParameterActual("hardness", 0.38f); setParameterActual("noise", 0.08f);
            setParameterActual("modalMix", 0.62f); setParameterActual("modalDecay", 0.64f);
            setParameterActual("object1Mix", 0.78f); setParameterActual("object1Decay", 0.74f);
            setParameterActual("object2Mix", 0.0f); setParameterActual("damping", 0.70f);
            setParameterActual("dispersion", 0.05f); setParameterActual("collision", 0.16f); setParameterActual("reverb", 0.08f);
            break;
        case 2: // Metal Plate
            setParameterActual("impact", 0.82f); setParameterActual("hardness", 0.90f); setParameterActual("noise", 0.11f);
            setParameterActual("modalMix", 0.64f); setParameterActual("modalDecay", 3.8f);
            setParameterActual("object1Mix", 0.82f); setParameterActual("object1Decay", 3.0f);
            setParameterActual("object2Mix", 0.52f); setParameterActual("object2Decay", 2.3f);
            setParameterActual("damping", 0.18f); setParameterActual("dispersion", 0.58f); setParameterActual("collision", 0.22f);
            setParameterActual("coupling", 0.22f); setParameterActual("width", 0.82f); setParameterActual("reverb", 0.22f);
            break;
        default: // Imaginary String
            setParameterActual("impact", 0.56f); setParameterActual("hardness", 0.50f); setParameterActual("noise", 0.24f);
            setParameterActual("modalMix", 0.36f); setParameterActual("modalDecay", 1.9f);
            setParameterActual("object1Mix", 0.88f); setParameterActual("object1Decay", 2.6f);
            setParameterActual("object2Mix", 0.68f); setParameterActual("object2Decay", 2.1f);
            setParameterActual("damping", 0.44f); setParameterActual("dispersion", 0.12f); setParameterActual("collision", 0.10f);
            setParameterActual("coupling", 0.18f); setParameterActual("width", 0.76f); setParameterActual("reverb", 0.20f);
            break;
    }
}

const juce::String ObjektRebuildAudioProcessor::getProgramName(int index)
{
    static const juce::StringArray names { "Glass Bell", "Wood Mallet", "Metal Plate", "Imaginary String" };
    return names[juce::jlimit(0, names.size() - 1, index)];
}

void ObjektRebuildAudioProcessor::getStateInformation(juce::MemoryBlock& destData)
{
    auto state = parameters.copyState();
    state.setProperty("program", currentProgram, nullptr);
    if (auto xml = state.createXml())
        copyXmlToBinary(*xml, destData);
}

void ObjektRebuildAudioProcessor::setStateInformation(const void* data, int sizeInBytes)
{
    if (auto xml = getXmlFromBinary(data, sizeInBytes))
    {
        if (xml->hasTagName(parameters.state.getType()))
        {
            auto state = juce::ValueTree::fromXml(*xml);
            currentProgram = juce::jlimit(0, getNumPrograms() - 1, static_cast<int>(state.getProperty("program", 0)));
            // Old sessions have fewer controls; missing parameters must use defaults, not the last patch.
            for (auto* item : getParameters())
                if (auto* ranged = dynamic_cast<juce::RangedAudioParameter*>(item))
                    if (!state.getChildWithProperty("id", ranged->paramID).isValid())
                    {
                        juce::ValueTree child("PARAM");
                        child.setProperty("id", ranged->paramID, nullptr);
                        child.setProperty("value", ranged->convertFrom0to1(ranged->getDefaultValue()), nullptr);
                        state.appendChild(child, nullptr);
                    }
            parameters.replaceState(state);
        }
    }
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new ObjektRebuildAudioProcessor();
}
