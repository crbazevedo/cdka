import test from 'node:test';
import assert from 'node:assert/strict';
import {evaluate,errorAfter,threshold,PAYOFF} from '../docs/lab/diagnosis-core.mjs';

function close(a,b,tol=1e-12){assert.ok(Math.abs(a-b)<tol,`${a} != ${b}`);}

test('physical payoffs preserve v6 strict decision conflict',()=>{
 assert.ok(PAYOFF[0].refresh[0]>PAYOFF[0].hold[0]);
 assert.ok(PAYOFF[0].refresh[1]<PAYOFF[0].hold[1]);
});
test('exact threshold and fair-prior gain',()=>{
 close(threshold(0).eta,.19416181334107027);
 const m=evaluate({B:4,eta:0});
 close(m.baseline.value,.883319376);
 close(m.diagnosis,.908929941292);
 close(m.gain,.025610565292);
 assert.deepEqual(m.policy,['refresh','hold']);
});
test('costed selector makes perfect reading useless at B=3',()=>{
 close(evaluate({B:3,eta:0}).gain,0);
 close(evaluate({B:4,eta:0}).gain,.025610565292);
});
test('age and diagnostic procedure can erase value',()=>{
 close(errorAfter(.05,.1,1),.14);
 close(errorAfter(.05,.1,2),.212);
 assert.ok(evaluate({B:4,eta:.05,nu:.1,age:1}).gain>0);
 close(evaluate({B:4,eta:.05,nu:.1,age:2}).gain,0);
 close(evaluate({B:4,inspectionFailure:.05}).gain,0);
});
test('Bayesian value cannot exceed a fully observed health oracle at no cost',()=>{
 for(let eta=0;eta<=.5;eta+=.05)for(const B of [0,1,2,3,4]){
  const r=evaluate({B,eta});
  assert.ok(r.actual>=r.baseline.value-1e-12);
  assert.ok(r.actual<=r.oracle+1e-12);
 }
});
test('diagnosis is not assumed to provide a free resource side channel',()=>{
 for(let e=0;e<=.5;e+=.05){
  const m=evaluate({B:4,eta:e});
  assert.equal(m.remaining,2);
  assert.ok(m.policy.every(a=>['hold','correct','refresh','service'].includes(a)));
 }
});
