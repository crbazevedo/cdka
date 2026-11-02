import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {evaluate,optimize,BASE,DEFAULT} from '../docs/lab/transport-core.mjs';
const fixtures=JSON.parse(fs.readFileSync(new URL('../docs/lab/transport-fixtures.json',import.meta.url)));
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-12,`${a} != ${b}`);
test('all budget certificates agree with independent rational physical oracle',()=>{
 for(const f of fixtures.budgets){const r=optimize({budget:f.budget});assert.equal(r.best.key,f.choice);close(r.best.value,f.value_decimal);
 for(const o of r.options)if(o.feasible&&f.programs[o.key]!==undefined)close(o.value,f.programs[o.key]);}
});
test('expiry fixtures preserve nonzero information after value changes sign',()=>{
 for(const f of fixtures.expiration){const r=evaluate({budget:40,ticks:f.ticks,eta:0,rho:.2,bad:1/6});close(r.gain,f.diagnosis_net);close(r.info,f.mutual_information_bits);}
});
test('same selector fault rate different command-failure semantics',()=>{
 assert.ok(evaluate().gain<0);assert.ok(evaluate({driver:'silent'}).gain>0);
});
test('physical reservation includes corrupted actual refresh',()=>{
 assert.equal(optimize({budget:4}).best.key,'skip');assert.equal(evaluate({budget:4}).feasible,false);
 for(let n=1;n<=5;n++)assert.equal(evaluate({ticks:n,budget:30},true,true).cost,2*n+5);
});
test('protected memory plus serviced selector has monotone value for fixed costs',()=>{
 for(let k=0;k<=10;k++){
  const s={rho:k/10,bad:.5,eta:.05,budget:100};
  assert.ok(evaluate(s,true,true).value>=evaluate(s,false,false).value-1e-12);
 }
});
test('nested perfect-use limit returns v7 physical value',()=>{
 close(evaluate({eta:0,rho:0,bad:0}).value,.908929941292);close(BASE,.883319376);
});
test('upfront risky diagnostic never forces the optimal controller to use it',()=>{
 assert.ok(evaluate({risk:.2}).gain<0);close(optimize({risk:.2,budget:7}).best.value,BASE);
});
test('invalid contract rejected',()=>{
 for(const v of [{ticks:0},{rho:-1},{eta:.6},{driver:'mystery'}])assert.throws(()=>evaluate(v));
});
