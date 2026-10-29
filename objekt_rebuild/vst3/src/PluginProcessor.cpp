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
    : AudioProcessor(BusesProperties().withOutput("Output", juce::AudioChannelSet::stereo(), true)),
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
    return layout;
}

void ObjektRebuildAudioProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
    engine.prepare(sampleRate, samplesPerBlock);
}

void ObjektRebuildAudioProcessor::releaseResources()
{
    engine.reset();
}

bool ObjektRebuildAudioProcessor::isBusesLayoutSupported(const BusesLayout& layouts) const
{
    return layouts.getMainInputChannelSet().isDisabled()
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
    return result;
}

void ObjektRebuildAudioProcessor::renderSegment(juce::AudioBuffer<float>& buffer, int startSample, int numSamples, const objekt::Params& params)
{
    if (numSamples <= 0)
        return;
    engine.process(buffer.getWritePointer(0, startSample), buffer.getWritePointer(1, startSample), numSamples, params);
}

void ObjektRebuildAudioProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midi)
{
    juce::ScopedNoDenormals noDenormals;
    buffer.clear();
    const auto values = snapshotParameters();
    int cursor = 0;
    for (const auto metadata : midi)
    {
        const auto position = juce::jlimit(cursor, buffer.getNumSamples(), metadata.samplePosition);
        renderSegment(buffer, cursor, position - cursor, values);
        const auto message = metadata.getMessage();
        if (message.isNoteOn())
            engine.noteOn(message.getNoteNumber(), message.getFloatVelocity(), values);
        else if (message.isNoteOff())
            engine.noteOff(message.getNoteNumber());
        else if (message.isAllNotesOff() || message.isAllSoundOff())
            engine.allNotesOff();
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
            currentProgram = static_cast<int>(state.getProperty("program", 0));
            parameters.replaceState(state);
        }
    }
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new ObjektRebuildAudioProcessor();
}
