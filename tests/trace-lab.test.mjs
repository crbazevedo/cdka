import test from 'node:test';import assert from 'node:assert/strict';
import {routeProbabilities,routeGain,massOf,filterTraces,runtimeColumns} from '../docs/lab/trace-core.mjs';
test('critical code path 9% versus 1%',()=>{const x=routeProbabilities(.1);assert.ok(Math.abs(x.injective-.09)<1e-12);assert.ok(Math.abs(x.merged-.01)<1e-12)});
test('exact gain mirror and boundaries',()=>{const m=.15123087372746724;assert.ok(Math.abs(routeGain(.1,m)-.004032823299399127)<1e-15);assert.equal(routeGain(0,m),0);assert.equal(routeGain(.5,m),0)});
test('complete mass and explicit filters',()=>{const a=[{outcome:'alive',signal_evaluator_only:0,probability:{value:.6}},{outcome:'failed',signal_evaluator_only:1,probability:{value:.4}}];assert.equal(massOf(a),1);assert.equal(massOf(filterTraces(a,{outcome:'alive'})),.6);assert.equal(filterTraces(a,{signal:'1'}).length,1)});
test('runtime projection omits original signal and hidden health',()=>{const x=runtimeColumns({readable_word:0,signal_evaluator_only:2,health_initial_evaluator_only:1,outcome:'alive',steps:[{action:'service',after:[0,1,3]},{action:'refresh'}]});assert.deepEqual(x,{word:0,first:'service',next:[0,3],second:'refresh',outcome:'alive'});assert.ok(!('health_initial_evaluator_only' in x))});
test('no hypothetical action after early failure',()=>{const x=runtimeColumns({readable_word:1,outcome:'failed',steps:[{action:'refresh',after:'dead'}]});assert.equal(x.next,null);assert.equal(x.second,null)});
test('invalid channel excluded',()=>{assert.throws(()=>routeProbabilities(-1));assert.throws(()=>routeProbabilities(.51))});
