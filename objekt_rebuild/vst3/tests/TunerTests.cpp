#include "ObjektTuner.h"
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

int main(){
    constexpr double pi=3.14159265358979323846;
    for(double rate:{8000.0,44100.0,48000.0,96000.0,192000.0})
      for(double frequency:{55.0,110.0,261.625565,440.0,1000.0}){
        std::vector<float> signal(static_cast<std::size_t>(rate));
        for(std::size_t i=0;i<signal.size();++i){double phase=2*pi*frequency*i/rate;signal[i]=static_cast<float>(0.3*std::sin(phase)+0.1*std::sin(2*phase)+0.05);}
        auto result=objekt::analyzeTuning(signal.data(),signal.size(),rate,frequency);
        assert(result.valid);assert(result.confidence>0.9);assert(std::abs(result.correctionCents)<4);
      }
    std::vector<float> signal(48000);
    for(std::size_t i=0;i<signal.size();++i)signal[i]=static_cast<float>(0.3*std::sin(2*pi*445*i/48000));
    auto detuned=objekt::analyzeTuning(signal.data(),signal.size(),48000,440);
    assert(detuned.valid);assert(std::abs(detuned.correctionCents-1200*std::log2(440.0/445))<1);
    std::fill(signal.begin(),signal.end(),0);assert(!objekt::analyzeTuning(signal.data(),signal.size(),48000,440).valid);
    std::fill(signal.begin(),signal.end(),0.5f);assert(!objekt::analyzeTuning(signal.data(),signal.size(),48000,440).valid);
    std::uint32_t seed=123;
    for(auto& value:signal){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;value=static_cast<float>(seed&65535)/32768-1;}
    assert(!objekt::analyzeTuning(signal.data(),signal.size(),48000,440).valid);
    signal[8]=std::numeric_limits<float>::quiet_NaN();assert(!objekt::analyzeTuning(signal.data(),signal.size(),48000,440).valid);
    assert(!objekt::analyzeTuning(nullptr,100,48000,440).valid);
    assert(!objekt::analyzeTuning(signal.data(),10,48000,440).valid);
    std::cout<<"Tuner frequency, cents, silence/DC/noise and invalid-input checks passed\n";
}
