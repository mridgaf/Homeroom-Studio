cmake_minimum_required(VERSION 3.22)
project(ObjektRebuild VERSION 0.1.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_OSX_ARCHITECTURES arm64)

include(FetchContent)
FetchContent_Declare(
    JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 9.0.4
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(JUCE)

enable_testing()

add_library(objekt_dsp STATIC src/ObjektEngine.cpp)
target_include_directories(objekt_dsp PUBLIC src)
target_compile_features(objekt_dsp PUBLIC cxx_std_20)

add_executable(objekt_engine_tests tests/EngineTests.cpp)
target_link_libraries(objekt_engine_tests PRIVATE objekt_dsp)
add_test(NAME objekt_engine_tests COMMAND objekt_engine_tests)

add_executable(objekt_processor_tests tests/PluginProcessorTests.cpp src/PluginProcessor.cpp)
target_include_directories(objekt_processor_tests PRIVATE src)
target_link_libraries(objekt_processor_tests PRIVATE objekt_dsp juce::juce_audio_utils juce::juce_audio_processors)
target_compile_definitions(objekt_processor_tests PRIVATE JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0)
add_test(NAME objekt_processor_tests COMMAND objekt_processor_tests)

juce_add_plugin(ObjektRebuild
    VERSION 0.1.0
    COMPANY_NAME "Homeroom Studio"
    BUNDLE_ID "com.homeroomstudio.objektrebuild"
    IS_SYNTH TRUE
    NEEDS_MIDI_INPUT TRUE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD FALSE
    PLUGIN_MANUFACTURER_CODE HmRm
    PLUGIN_CODE ObR1
    FORMATS VST3
    PRODUCT_NAME "Objekt Rebuild"
)

target_sources(ObjektRebuild PRIVATE src/PluginProcessor.cpp src/PluginProcessor.h)
target_include_directories(ObjektRebuild PRIVATE src)
target_link_libraries(ObjektRebuild PRIVATE objekt_dsp juce::juce_audio_utils juce::juce_audio_processors)
target_compile_definitions(ObjektRebuild PRIVATE
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
)
