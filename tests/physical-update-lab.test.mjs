import test from'node:test';import assert from'node:assert/strict';import{readFileSync}from'node:fs';
import{frontier,gateProgram,runCircuit}from'../docs/lab/physical-update-core.mjs';
const data=JSON.parse(readFileSync('docs/lab/physical-update-data.json','utf8'));
test('browser projection matches exact Python certificates',()=>{for(const x of data.examples){assert.ok(Math.abs(frontier(data,x.p.value,x.q.value,x.gate_budget).value-x.value.value)<1e-14);}});
test('noise interval changes the minimum required circuit',()=>{assert.equal(frontier(data,.1,0,3).usesBypass,true);assert.equal(frontier(data,.1,0,4).usesBypass,false);assert.equal(frontier(data,.01,.02,4).usesBypass,true);});
test('two and four gate networks execute their full truth functions',()=>{for(const K of[0,2,4]){const g=gateProgram(K,.01);for(let m=0;m<4;m++)for(let k=0;k<2;k++)assert.equal(runCircuit(g,m,k),(g.truth>>(2*m+k))&1);}});
test('generated signal sets and continuous proof counts preserved',()=>{assert.deepEqual(data.circuit_profile.map(x=>x.functions),[5,11,23,48,91]);assert.equal(data.certificate.dominance_checks,2814);});
test('noiseless equivalence does not certify internal gate faults',()=>{assert.equal(data.gate_fault_counterexample.wire_error.value,0);assert.equal(data.gate_fault_counterexample.formula.value,.18);});
test('UI declares first-action restriction, noise model and methodology',()=>{const s=readFileSync('docs/lab/physical_update.html','utf8');assert.ok(s.includes('primeira ação'));assert.ok(s.includes('As NAND são ideais'));assert.ok(s.includes('prompt-fechamento-contextual.md'));for(const x of['p','q','K'])assert.ok(s.includes('id="'+x+'"'));});
