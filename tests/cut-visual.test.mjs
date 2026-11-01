import test from 'node:test';
import assert from 'node:assert/strict';
import {h2,cutModel,horizonSeries,informationTimeline} from '../docs/lab/cut-core.mjs';

test('T3.C hard-reset resource discontinuity',()=>{
 for(let n=1;n<=8;n++){
   assert.equal(cutModel({cycles:n,budget:n-1}).success,0);
   assert.equal(cutModel({cycles:n,budget:n,rho:1}).success,.5);
   assert.equal(cutModel({cycles:n,budget:2*n,rho:1}).success,1);
   if(n>1)assert.equal(cutModel({cycles:n,budget:2*n-1,rho:1}).success,.5);
 }
});
test('finite memory decay exact horizon samples',()=>{
 assert.equal(cutModel({cycles:3,budget:3,rho:.5}).success,.5625);
 assert.equal(cutModel({cycles:3,budget:4,rho:.5}).success,.625);
 assert.equal(cutModel({cycles:3,budget:5,rho:.5}).success,.75);
 assert.equal(cutModel({cycles:3,budget:6,rho:.5}).success,1);
});
test('physical actuator side channel restores information when memory erased',()=>{
 const s={cycles:2,budget:2,rho:1,eta:0,nu:0};
 assert.equal(cutModel({...s,sideChannel:false}).success,.5);
 assert.equal(cutModel({...s,sideChannel:false}).finalInfo,0);
 assert.equal(cutModel({...s,sideChannel:true}).success,1);
 assert.equal(cutModel({...s,sideChannel:true}).finalInfo,1);
});
test('world drift makes retained memory stale even with infinite protection',()=>{
 const s=cutModel({cycles:2,budget:4,rho:1,eta:0,nu:.1});
 assert.ok(Math.abs(s.success-.82)<1e-12);
 assert.ok(s.finalInfo<1&&s.finalInfo>0);
});
test('information reduces under stochastic repairs',()=>{
 const p=informationTimeline({cycles:5,budget:5,rho:.25,eta:.1,nu:.02});
 assert.equal(p.length,6);
 for(let i=1;i<p.length;i++)assert.ok(p[i].information<=p[i-1].information+1e-12);
});
test('sensor error and required resource are not interchangeable',()=>{
 const x=cutModel({cycles:2,budget:3,rho:.5,eta:.25,nu:0});
 assert.ok(Math.abs(x.success-.625)<1e-12);
 assert.ok(x.initialInfo>x.finalInfo);
});
test('strictly exact extreme information limits',()=>{
 assert.equal(h2(0),0);
 assert.equal(h2(.5),1);
 assert.equal(cutModel({cycles:1,budget:2,eta:.5,rho:0,nu:0}).success,.5);
 assert.equal(cutModel({cycles:1,budget:2,eta:0,rho:0,nu:.5}).success,.5);
});
test('horizon series preserves selected total physical budget',()=>{
 const r=horizonSeries({budget:3,rho:1},8);
 assert.equal(r.length,8);
 assert.equal(r[0].success,1);
 assert.equal(r[1].success,.5);
 assert.equal(r[2].success,.5);
 assert.equal(r[3].success,0);
});
