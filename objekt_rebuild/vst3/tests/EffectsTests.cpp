#include "ObjektEffects.h"
#include <cassert>
#include <cmath>
#include <iostream>
#include <limits>

int main() {
    objekt::Effects fx;
    fx.prepare(48000);
    objekt::EffectsParams p;
    fx.setParameters(p);
    for(int i=0;i<1000;++i) {
        float input=0.2f*std::sin(i*0.1f);
        const auto y=fx.process(input,-input);
        assert(std::abs(y[0]-input)<1e-5f);
        assert(std::abs(y[1]+input)<1e-5f);
    }
    fx.reset();p.delayMix=1;p.delaySync=true;p.delayBeats=0.5f;p.tempo=120;p.delayFeedback=0.5f;
    fx.setParameters(p);
    fx.process(0.5f,0);
    p.delayMix=0;fx.setParameters(p); // Existing echo survives send automation to zero.
    for(int i=1;i<12000;++i){auto y=fx.process(0,0);assert(std::abs(y[0])<1e-6f);assert(std::abs(y[1])<1e-6f);}
    auto first=fx.process(0,0);assert(first[0]>0.4f);assert(first[1]==0);
    for(int i=12001;i<24000;++i)fx.process(0,0);
    auto second=fx.process(0,0);assert(second[1]>0.2f);assert(second[0]==0);
    fx.reset();auto clean=fx.process(0,0);assert(clean[0]==0&&clean[1]==0);
    p={};p.reverbMix=1;fx.setParameters(p);fx.process(0.5f,0);
    p.reverbMix=0;fx.setParameters(p);float tail=0;
    for(int i=0;i<48000;++i){auto y=fx.process(0,0);tail+=std::abs(y[0])+std::abs(y[1]);}
    assert(tail>0.1f);fx.reset();
    p={};p.compressorMix=1;p.thresholdDb=-24;p.ratio=10;p.attackMs=1;
    fx.setParameters(p);std::array<float,2> compressed{};
    for(int i=0;i<48000;++i)compressed=fx.process(0.5f,0.25f);
    assert(compressed[0]<0.15f);assert(std::abs(compressed[0]-2*compressed[1])<1e-6f);
    for(float rate:{8000.0f,44100.0f,96000.0f,192000.0f})for(int mode=0;mode<6;++mode){
        fx.prepare(rate);p={};p.distortionMix=1;p.drive=30;p.distortionMode=mode;p.compressorMix=1;
        p.lowDb=24;p.midDb=-24;p.highDb=24;p.delayMix=1;p.delayFeedback=0.95f;p.reverbMix=1;p.reverbDecay=20;p.order={4,3,2,1,0};
        fx.setParameters(p);
        for(int i=0;i<24000;++i){auto y=fx.process(i<100?0.5f:0,i<100?-0.3f:0);assert(std::isfinite(y[0])&&std::isfinite(y[1]));assert(std::abs(y[0])<100&&std::abs(y[1])<100);}
    }
    p.lowDb=std::numeric_limits<float>::quiet_NaN();p.tempo=0;p.order={0,0,99,-1,4};fx.setParameters(p);
    auto safe=fx.process(std::numeric_limits<float>::infinity(),0);assert(std::isfinite(safe[0])&&std::isfinite(safe[1]));
    std::cout<<"Effects bypass, sync/pingpong, reset, compression and stability passed\n";
}
