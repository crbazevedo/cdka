import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {defaults,row,solve,states,COST,calibration,contractBound} from '../docs/lab/composition-core.mjs';
const evidence=JSON.parse(readFileSync(new URL('../docs/lab/composition-fixtures.json',import.meta.url),'utf8'));
test('all macro kernels normalized with death and affordable actions only',()=>{
 for(const s of states(defaults))for(const a of Object.keys(COST).filter(a=>COST[a]<=s[2])){
  const r=row(defaults,s,a);assert.equal(r.length,21);assert.ok(r.every(x=>x>=0));assert.ok(Math.abs(r.reduce((a,b)=>a+b,0)-1)<1e-12);
 }
 assert.throws(()=>row(defaults,[0,0,0],'refresh'));
});
test('browser DP matches eight exact rational Python fixtures',()=>{
 for(const f of evidence.fixtures){const r=solve({...defaults,world_flip:f.world_flip},f.horizon);assert.ok(Math.abs(r.levels[f.horizon][4]-f.value)<1e-12);assert.equal(r.policies[f.horizon][4],f.first_action);}
});
test('paid new observation differs from correcting stale knowledge',()=>{
 const p={...defaults,world_flip:.2,cell_flip:0,write_flip:0,correction_error:[0,0],sensor_error:[.05,.05],actuator_failure:[0,0]};
 assert.ok(Math.abs(1-row(p,[0,0,4],'hold')[20]-.8)<1e-12);
 assert.ok(Math.abs(1-row(p,[0,0,4],'correct')[20]-.8)<1e-12);
 assert.ok(Math.abs(1-row(p,[0,0,4],'refresh')[20]-.95)<1e-12);
});
test('more declared actions cannot worsen optimum',()=>{
 const a=solve(defaults,12),b=solve(defaults,12,['hold','correct','service']);assert.ok(a.levels[12].every((v,i)=>v+1e-12>=b.levels[12][i]));
});
test('calibration inside finite-horizon certificate',()=>{
 const r=calibration(defaults,.02,10);assert.ok(Math.abs(r.delta-evidence.calibration.delta)<1e-12);assert.ok(Math.abs(r.gap-evidence.calibration.max_optimum_gap)<1e-12);assert.ok(r.gap<=r.bound);assert.ok(Math.abs(contractBound(.1,2)-.19)<1e-12);
});
test('resource and horizon affect maintenance',()=>{assert.equal(solve(defaults,1).policies[1][9],'hold');assert.equal(solve(defaults,10).policies[10][9],'service');});
