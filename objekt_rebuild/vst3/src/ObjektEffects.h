#pragma once
#include <algorithm>
#include <array>
#include <cmath>
#include <vector>

namespace objekt {
struct EffectsParams {
    float lowDb=0, midDb=0, highDb=0, lowHz=250, midHz=1000, midQ=0.7f, highHz=4000;
    int distortionMode=0; // Dist, Scream, Tube, Sine, sample/hold, Ring.
    float distortionMix=0, drive=1, ringHz=100, holdHz=4000;
    float compressorMix=0, thresholdDb=-18, ratio=4, attackMs=10, releaseMs=100, makeupDb=0;
    // Delay/reverb amounts feed the send; they never mute an existing tail.
    float delayMix=0, delaySeconds=0.3f, delayFeedback=0.3f, delayBeats=0.5f, tempo=120, delayPan=0;
    bool delaySync=false, pingPong=true;
    float reverbMix=0, reverbDecay=2, reverbDamping=0.4f, earlyLevel=0.2f;
    int reverbType=0;
    std::array<int,5> order {0,1,2,3,4}; // EQ, distortion, compressor, delay, reverb.
};

// Independent effects algorithms; the original device's nonlinearities and reverbs remain unmeasured.
class Effects {
    static constexpr float pi=3.14159265358979323846f;
    static float bounded(float v,float low,float high,float fallback) noexcept { return std::isfinite(v)?std::clamp(v,low,high):fallback; }
    struct Biquad {
        float b0=1,b1=0,b2=0,a1=0,a2=0;
        std::array<float,2> z1{},z2{};
        float tick(float x,int ch) noexcept { const float y=b0*x+z1[ch]; z1[ch]=b1*x-a1*y+z2[ch]; z2[ch]=b2*x-a2*y; return y; }
        void clear() noexcept {z1={};z2={};}
        void configure(float sr,float hz,float db,float q,int type) noexcept {
            const float A=std::pow(10.0f,db/40),w=2*pi*hz/sr,c=std::cos(w),s=std::sin(w);
            const float alpha=s/(2*q),root=2*std::sqrt(A)*alpha;
            float a0;
            if(type==0) { b0=A*((A+1)-(A-1)*c+root); b1=2*A*((A-1)-(A+1)*c); b2=A*((A+1)-(A-1)*c-root); a0=(A+1)+(A-1)*c+root; a1=-2*((A-1)+(A+1)*c); a2=(A+1)+(A-1)*c-root; }
            else if(type==2) { b0=A*((A+1)+(A-1)*c+root); b1=-2*A*((A-1)+(A+1)*c); b2=A*((A+1)+(A-1)*c-root); a0=(A+1)-(A-1)*c+root; a1=2*((A-1)-(A+1)*c); a2=(A+1)-(A-1)*c-root; }
            else {b0=1+alpha*A;b1=-2*c;b2=1-alpha*A;a0=1+alpha/A;a1=-2*c;a2=1-alpha/A;}
            b0/=a0;b1/=a0;b2/=a0;a1/=a0;a2/=a0;
        }
    };
    struct Comb {
        std::vector<float> data;
        std::size_t position=0;
        float filtered=0,feedback=0.7f;
        void clear(){ std::fill(data.begin(),data.end(),0);position=0;filtered=0; }
        float tick(float x,float damping) noexcept {
            const float y=data[position]; filtered=(1-damping)*y+damping*filtered;
            data[position]=std::tanh(x+filtered*feedback);
            if(++position==data.size())position=0;
            return y;
        }
    };
    float sr=48000, envelope=0, attack=0,release=0, makeup=1,ringPhase=0,holdPhase=1, delayLength=14400;
    std::array<float,2> held{};
    std::array<Biquad,3> eq;
    std::array<std::vector<float>,2> delay;
    std::size_t delayPosition=0;
    std::array<std::array<Comb,4>,2> combs;
    EffectsParams p;
    bool prepared=false;
public:
    void prepare(double sampleRate) {
        sr=static_cast<float>(std::isfinite(sampleRate)?std::clamp(sampleRate,8000.0,192000.0):48000);
        for(auto& d:delay)d.assign(static_cast<std::size_t>(sr*4)+2,0);
        constexpr std::array<float,4> times{0.0297f,0.0371f,0.0411f,0.0437f};
        for(int ch=0;ch<2;++ch)for(int i=0;i<4;++i)combs[ch][i].data.assign(static_cast<std::size_t>(sr*times[i])+ch*17,0);
        prepared=true;reset();setParameters(p);
    }
    void reset() noexcept {
        for(auto& f:eq)f.clear();
        for(auto& d:delay)std::fill(d.begin(),d.end(),0);
        for(auto& c:combs)for(auto& f:c)f.clear();
        delayPosition=0;envelope=0;ringPhase=0;holdPhase=1;held={};
    }
    void setParameters(const EffectsParams& values) noexcept {
        p=values;
        p.lowDb=bounded(p.lowDb,-24,24,0);p.midDb=bounded(p.midDb,-24,24,0);p.highDb=bounded(p.highDb,-24,24,0);
        p.lowHz=bounded(p.lowHz,20,sr*0.45f,250);p.midHz=bounded(p.midHz,20,sr*0.45f,1000);p.highHz=bounded(p.highHz,20,sr*0.45f,3000);p.midQ=bounded(p.midQ,0.1f,10,0.7f);
        eq[0].configure(sr,p.lowHz,p.lowDb,0.7071f,0);eq[1].configure(sr,p.midHz,p.midDb,p.midQ,1);eq[2].configure(sr,p.highHz,p.highDb,0.7071f,2);
        p.distortionMode=std::clamp(p.distortionMode,0,5);p.distortionMix=bounded(p.distortionMix,0,1,0);p.drive=bounded(p.drive,1,30,1);p.ringHz=bounded(p.ringHz,0,sr*0.45f,100);p.holdHz=bounded(p.holdHz,1,sr,4000);
        p.compressorMix=bounded(p.compressorMix,0,1,0);p.thresholdDb=bounded(p.thresholdDb,-60,0,-18);p.ratio=bounded(p.ratio,1,20,4);
        p.attackMs=bounded(p.attackMs,0.1f,200,10);p.releaseMs=bounded(p.releaseMs,1,2000,100);p.makeupDb=bounded(p.makeupDb,-24,24,0);
        attack=std::exp(-1000/(sr*p.attackMs));release=std::exp(-1000/(sr*p.releaseMs));makeup=std::pow(10.0f,p.makeupDb/20);
        p.delayMix=bounded(p.delayMix,0,1,0);p.delayFeedback=bounded(p.delayFeedback,0,0.95f,0.3f);p.delaySeconds=bounded(p.delaySeconds,1/sr,4,0.3f);p.delayBeats=bounded(p.delayBeats,0.0625f,8,0.5f);p.tempo=bounded(p.tempo,20,400,120);p.delayPan=bounded(p.delayPan,-1,1,0);
        delayLength=std::clamp((p.delaySync?60*p.delayBeats/p.tempo:p.delaySeconds)*sr,1.0f,4*sr);
        p.reverbMix=bounded(p.reverbMix,0,1,0);p.reverbDecay=bounded(p.reverbDecay,0.1f,20,2);p.reverbDamping=bounded(p.reverbDamping,0,0.99f,0.4f);p.earlyLevel=bounded(p.earlyLevel,0,1,0.2f);p.reverbType=std::clamp(p.reverbType,0,2);
        for(auto& channel:combs)for(auto& c:channel)c.feedback=std::pow(0.001f,static_cast<float>(c.data.size())/(sr*p.reverbDecay));
        // Reject malformed orders as a whole so each stateful processor advances exactly once.
        std::array<bool,5> seen{};for(int id:p.order){if(id<0||id>4||seen[id]){p.order={0,1,2,3,4};break;}seen[id]=true;}
    }
    std::array<float,2> process(float left,float right) noexcept {
        std::array<float,2> x{std::isfinite(left)?left:0,std::isfinite(right)?right:0};
        if(!prepared)return x;
        for(int id:p.order) {
            if(id==0) {for(int ch=0;ch<2;++ch)for(auto& f:eq)x[ch]=f.tick(x[ch],ch);}
            else if(id==1) {
                // shortcut: distortion runs at host rate; add oversampling before claiming high-frequency parity.
                ringPhase+=p.ringHz/sr;ringPhase-=std::floor(ringPhase);
                holdPhase+=p.holdHz/sr;const bool capture=holdPhase>=1;holdPhase-=std::floor(holdPhase);
                for(int ch=0;ch<2;++ch){const float driven=x[ch]*p.drive;float y=0;
                    switch(p.distortionMode){
                        case 0:y=std::tanh(driven);break;
                        case 1:y=std::clamp(driven,-1.0f,1.0f);break;
                        case 2:y=std::tanh(driven+0.35f)-std::tanh(0.35f);break;
                        case 3:y=std::sin(driven);break;
                        case 4:if(capture)held[ch]=std::tanh(driven);y=held[ch];break;
                        case 5:y=std::tanh(driven)*std::sin(2*pi*ringPhase);break;
                    }x[ch]+=p.distortionMix*(y-x[ch]);
                }
            } else if(id==2) {
                const float peak=std::max(std::abs(x[0]),std::abs(x[1]));const float c=peak>envelope?attack:release;envelope=c*envelope+(1-c)*peak;
                const float db=20*std::log10(std::max(envelope,1.0e-12f));const float reduction=std::max(0.0f,db-p.thresholdDb)*(1-1/p.ratio);
                const float gain=std::pow(10.0f,-reduction/20)*makeup;for(auto& v:x)v*=1+p.compressorMix*(gain-1);
            } else if(id==3) {
                const auto size=delay[0].size();float read=static_cast<float>(delayPosition)-delayLength; if(read<0)read+=static_cast<float>(size);
                const auto a=static_cast<std::size_t>(read),b=(a+1)%size;const float fraction=read-static_cast<float>(a);
                std::array<float,2> wet{};for(int ch=0;ch<2;++ch)wet[ch]=delay[ch][a]+fraction*(delay[ch][b]-delay[ch][a]);
                for(int ch=0;ch<2;++ch)delay[ch][delayPosition]=std::tanh(x[ch]*p.delayMix+wet[p.pingPong?1-ch:ch]*p.delayFeedback);
                if(++delayPosition==size)delayPosition=0;
                x[0]+=wet[0]*std::sqrt(1-p.delayPan);x[1]+=wet[1]*std::sqrt(1+p.delayPan);
            } else {
                const auto dry=x;for(int ch=0;ch<2;++ch){float wet=0;for(int i=0;i<4;++i){float feed=dry[ch]*p.reverbMix;if(p.reverbType==1)feed=(0.7f*dry[ch]+0.3f*dry[1-ch])*p.reverbMix;if(p.reverbType==2)feed*=((i&1)?-1.0f:1.0f);wet+=combs[ch][i].tick(feed,p.reverbDamping)*0.25f;}x[ch]+=wet+p.earlyLevel*combs[ch][0].filtered;}
            }
        }
        for(auto& v:x)if(!std::isfinite(v))v=0;
        return x;
    }
};
} // namespace objekt
