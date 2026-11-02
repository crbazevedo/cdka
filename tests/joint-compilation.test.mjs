import test from 'node:test';import assert from 'node:assert/strict';
import {DATA,channel,compile,funded,information,certifiedValue} from '../docs/lab/joint-compilation-core.mjs';
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-12,`${a} != ${b}`);
test('browser matches exact rational model fixtures',()=>{
 for(const x of DATA.fixtures.examples){const [a,b]=x.p.split('/').map(Number),p=a/(b||1);
  close(compile(p).value,x.value);close(compile(p,3,4,true).value,x.injective_value);
 }
});
test('channel mass and independence at half error',()=>{
 for(let x=0;x<4;x++){close(channel(x,.1).reduce((a,b)=>a+b,0),1);assert.deepEqual(channel(x,.5),[.25,.25,.25,.25]);}
});
test('certified envelope agrees with finite synthesis across 101 noise values',()=>{
 for(let i=0;i<=100;i++)close(compile(i/200).value,certifiedValue(i/200));
});
test('three regimes use three, two and one diagnostic classes',()=>{
 assert.equal(compile(.001).states,3);assert.equal(compile(.05).states,2);assert.equal(compile(.3).states,1);
});
test('installation reserves actual physical resources',()=>{
 const x=funded(0,4,1);assert.equal(x.best.slots,2);assert.equal(x.best.balance,3);
 for(const o of x.options)assert.equal(o.balance+o.fee,4);
 for(const f of DATA.fixtures.installed_price_one_at_zero_error)close(x.options.find(o=>o.slots===f.slots).value,f.value);
});
test('more mutual information can yield worse survival',()=>{
 const a=compile(.1),b=compile(.1,3,4,true);assert.ok(a.value>b.value);assert.ok(information(a.encoder,.1)<information(b.encoder,.1));
});
test('template limit changes noiseless optimum; there is no free fourth program',()=>{
 assert.ok(compile(0,3).value>compile(0,2).value);assert.ok(compile(0,2).value>compile(0,1).value);
 for(let L=1;L<=3;L++)assert.ok(compile(.01,L).templates<=L);
});
