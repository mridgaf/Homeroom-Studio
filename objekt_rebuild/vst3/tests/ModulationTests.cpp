#include "ObjektModulation.h"
#include <cassert>
#include <cmath>
int main() {
    objekt::Modulation m; m.prepare(48000);
    objekt::ModulationParams p;
    p.macros[0]=0.75f;
    p.buses[0]={objekt::ModulationParams::macro1, objekt::ModulationParams::impact, objekt::ModulationParams::noise, objekt::ModulationParams::velocity, 2, -1};
    auto v=m.tick(p,120,0.5f,60,0,0);
    assert(std::abs(v[objekt::ModulationParams::impact]-0.75f)<1e-6f);
    assert(std::abs(v[objekt::ModulationParams::noise]+0.375f)<1e-6f);
    p.buses[0]={objekt::ModulationParams::lfo1,objekt::ModulationParams::pitch,0,objekt::ModulationParams::constant,1,0};
    m.reset();
    for(int i=0;i<12000;++i) m.tick(p,120,1,60,0,0);
    v=m.tick(p,120,1,60,0,0);
    assert(std::abs(v[objekt::ModulationParams::pitch]-1)<1e-5f);
    p.lfos[0].sync=true; m.reset();
    for(int i=0;i<6000;++i) m.tick(p,120,1,60,0,0);
    v=m.tick(p,120,1,60,0,0);
    assert(std::abs(v[objekt::ModulationParams::pitch]-1)<1e-5f);
    p.buses[0]={objekt::ModulationParams::curve,objekt::ModulationParams::pitch,0,objekt::ModulationParams::constant,1,0};
    p.steps[0]=0.6f; m.reset();
    assert(std::abs(m.tick(p,120,1,60,0,0)[objekt::ModulationParams::pitch]-0.6f)<1e-6f);
}
