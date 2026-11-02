import test from 'node:test';import assert from 'node:assert/strict';
import {q,ell,inflection,rstar,envelope,grid,required,harvest,produced,cycleBound} from '../docs/lab/implementability-core.mjs';
const close=(a,b,tol=1e-10)=>assert.ok(Math.abs(a-b)<tol,`${a} vs ${b}`);
test('calculus thresholds and exact cost inversion',()=>{close(rstar,1.96872832139);close(q(inflection),2-Math.SQRT2);for(const n of [1,10,100])close(n*ell(required(n,.9)/n),Math.log(.9));});
test('joint mechanism complementarity and equal split',()=>{close(produced(0,5),.5);close(produced(5,0),.5);for(let k=0;k<=50;k++)assert.ok(produced(k/10,5-k/10)<=q(5)+1e-12);});
test('known scarcity theorem and nonuniform schedule',()=>{const a=grid(4,5,.2);close(a.logValue,ell(1)+3*ell(0));assert.ok(a.logValue>4*ell(.25));});
test('finite grid optimum bounded by envelope',()=>{for(const n of [2,5,10])for(const u of [0,5,20,40]){const a=grid(n,u,.2);close(a.schedule.reduce((s,x)=>s+x,0),u*.2);assert.ok(a.logValue<=n*envelope(u*.2/n)+1e-12);}});
test('conservation of physically harvested resources',()=>{for(const h of [0,.3,1,2,4]){const a=harvest(2000,h);let spent=0;a.points.forEach(({t,spend})=>{spent+=spend;assert.ok(spent<=h*(t-1)+1e-8);});assert.ok(Math.abs(a.rate-envelope(h))<.002);}});
test('restricted selector full/zero contrast',()=>{close(cycleBound(0,.1),.5);close(cycleBound(1,.1),.9);close(cycleBound(.5,.1),.7);});
