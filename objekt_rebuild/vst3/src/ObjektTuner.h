#pragma once
#include <algorithm>
#include <cmath>
#include <cstddef>
#include <vector>

namespace objekt {
struct TuningResult {
    bool valid=false;
    double frequencyHz=0;
    double confidence=0;
    double correctionCents=0;
};

// Offline monophonic estimator. Call from a worker, never the audio callback.
// shortcut: estimates one periodic pitch; inharmonic objects require reference-guided tuning.
inline TuningResult analyzeTuning(const float* mono,std::size_t count,double sampleRate,double targetHz,
                                 double minHz=30,double maxHz=2000) {
    TuningResult result;
    if(!mono||count<32||!std::isfinite(sampleRate)||sampleRate<8000||sampleRate>384000
       ||!std::isfinite(targetHz)||targetHz<=0||!std::isfinite(minHz)||!std::isfinite(maxHz)
       ||minHz<10||maxHz<=minHz)return result;
    // Bound runtime independently of supplied buffer duration.
    const auto stride=static_cast<std::size_t>(std::max(1.0,std::floor(sampleRate/8000)));
    const double rate=sampleRate/static_cast<double>(stride);
    maxHz=std::min(maxHz,rate*0.25);
    if(minHz>=maxHz)return result;
    const auto n=std::min<std::size_t>(16384,count/stride);
    if(n<32)return result;
    std::vector<double> samples(n);
    double mean=0;
    for(std::size_t i=0;i<n;++i){
        double sum=0;
        for(std::size_t j=0;j<stride;++j){const auto value=mono[i*stride+j];if(!std::isfinite(value))return result;sum+=value;}
        samples[i]=sum/static_cast<double>(stride);mean+=samples[i];
    }
    mean/=static_cast<double>(n);
    double energy=0;
    for(auto& value:samples){value-=mean;energy+=value*value;}
    if(energy/static_cast<double>(n)<1e-10)return result;
    const auto first=static_cast<std::size_t>(std::max(2.0,std::floor(rate/maxHz)));
    const auto last=std::min<std::size_t>(n/3,static_cast<std::size_t>(std::ceil(rate/minHz)));
    if(last<=first+2)return result;
    std::vector<double> correlation(last+2);
    for(std::size_t lag=first-1;lag<=last+1;++lag){
        double cross=0,total=0;
        for(std::size_t i=0;i<n-lag;++i){const double a=samples[i],b=samples[i+lag];cross+=a*b;total+=a*a+b*b;}
        correlation[lag]=total>1e-20?2*cross/total:0;
    }
    double best=0;
    for(std::size_t lag=first;lag<=last;++lag)
        if(correlation[lag]>correlation[lag-1]&&correlation[lag]>=correlation[lag+1])best=std::max(best,correlation[lag]);
    result.confidence=std::clamp(best,0.0,1.0);
    if(best<0.85)return result;
    // Earliest strong periodic peak avoids selecting octave-down multiples.
    for(std::size_t lag=first;lag<=last;++lag){
        const double value=correlation[lag];
        if(value<std::max(0.85,best*0.93)||value<=correlation[lag-1]||value<correlation[lag+1])continue;
        const double a=correlation[lag-1],c=correlation[lag+1],curvature=a-2*value+c;
        const double offset=std::abs(curvature)>1e-12?std::clamp(0.5*(a-c)/curvature,-0.5,0.5):0;
        const double frequency=rate/(static_cast<double>(lag)+offset);
        if(frequency<minHz||frequency>maxHz)continue;
        result.valid=true;result.frequencyHz=frequency;result.confidence=value;
        result.correctionCents=1200*std::log2(targetHz/frequency);
        return result;
    }
    return result;
}
} // namespace objekt
