import test from 'node:test';
import assert from 'node:assert/strict';
import {channelGeometry,cycleProfiles,renewal,tolerance} from '../docs/lab/policy-cuts-core.mjs';

test('feedback can preserve distinctions while fixed modes erase',()=>{
 const g=channelGeometry([0,1,0,1]);
 assert.deepEqual(g.fixed,[0,0]);assert.equal(g.envelope,1);assert.equal(g.success,1);
 assert.equal(channelGeometry([.5,.5,.5,.5]).envelope,0);
});
test('channel extrema agree with all four deterministic rules on 625 grids',()=>{
 const grid=[0,.25,.5,.75,1];let count=0;
 for(const a of grid)for(const b of grid)for(const c of grid)for(const d of grid){
  const x=channelGeometry([a,b,c,d]);
  assert.equal(x.envelope,Math.max(Math.abs(c-a),Math.abs(d-a),Math.abs(c-b),Math.abs(d-b)));count++;
 }
 assert.equal(count,625);
});
test('all 16 cycle rules obey the physical binary channel bound',()=>{
 for(const p of [0,.1,.25,.5]){
  const rules=cycleProfiles(p);assert.equal(rules.length,16);
  rules.forEach(({q})=>assert.ok(q[0]+q[1]<=2*(1-p)+1e-12));
 }
});
test('finite-horizon objective changes at the predicted threshold',()=>{
 assert.equal(renewal(.1,6).mean,.9**6);
 assert.equal(renewal(.1,7).mean,.5);
 assert.equal(renewal(.1,10).robust,.9**10);
 assert.equal(renewal(.1,10).seed,.5);
});
test('conditional one bit does not remove failed trajectory mass',()=>{
 const v=renewal(.25,30);
 assert.equal(v.survivorBits,1);assert.ok(v.liveMass<.001);
});
test('risk tolerance gives an exact boundary',()=>{
 for(const alpha of [.01,.1,.3])for(const n of [1,2,7,20]){
  const p=tolerance(alpha,n);assert.ok(Math.abs((1-p)**n-(1-alpha))<1e-12);
 }
});
test('zero noise has no finite crossover and the profile always survives',()=>{
 const v=renewal(0,100);assert.equal(v.robust,1);assert.equal(v.crossover,Infinity);
});
test('invalid physical parameters are rejected',()=>{
 assert.throws(()=>renewal(.6,3));assert.throws(()=>renewal(.2,0));
 assert.throws(()=>channelGeometry([0,1,2,1]));assert.throws(()=>tolerance(1,5));
});
