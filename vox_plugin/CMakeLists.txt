cmake_minimum_required(VERSION 3.22)
project(Vox VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_OSX_ARCHITECTURES "arm64")

add_subdirectory(JUCE)

juce_add_plugin(Vox
    COMPANY_NAME "BOTC"
    PLUGIN_MANUFACTURER_CODE BOTC
    PLUGIN_CODE Vox1
    FORMATS VST3
    VST3_CATEGORIES Fx Dynamics
    PRODUCT_NAME "Vox"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE)

target_sources(Vox PRIVATE Source/PluginProcessor.cpp Source/PluginEditor.cpp)

target_compile_definitions(Vox PUBLIC
    JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0 JUCE_VST3_CAN_REPLACE_VST2=0)

target_link_libraries(Vox PRIVATE
    juce::juce_audio_utils
    juce::juce_dsp
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags)
