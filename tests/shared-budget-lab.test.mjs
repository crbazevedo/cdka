import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {selectCase, conditionedTrace, resourceComparison, displayNumber} from '../docs/lab/shared-budget.mjs';

const data=JSON.parse(readFileSync(new URL('../docs/data/shared-budget-results.json',import.meta.url),'utf8'));

test('discrete price lookup never interpolates an uncertified point',()=>{
  assert.equal(data.cases.length,24);
  assert.equal(data.raw_complete_programs,1024);
  assert.equal(data.distinct_cost_profile_programs,336);
  assert.equal(selectCase(data,1,6,6).result.program_count,336);
  assert.throws(()=>selectCase(data,1,7,6),RangeError);
  assert.throws(()=>selectCase(data,1,6,6,'unbounded'),RangeError);
});

test('at the independently verified 84-quantum boundary work can succeed before a resource stop',()=>{
  const pair=resourceComparison(84,1,6);
  assert.equal(pair.fresh.repair,1);
  assert.equal(pair.elision.repair,1);
  assert.equal(pair.fresh.spent,84);
  assert.equal(pair.fresh.failure,'resource:write');
  assert.equal(pair.elision.failure,'resource:enable');
  assert.equal(pair.fresh.earned,0);
  assert.equal(pair.elision.earned,0);
  assert.ok(pair.fresh.conserved && pair.elision.conserved);
});

test('a saved write changes the actual successor balance, not a separate accounting ledger',()=>{
  const pair=resourceComparison(90,1,6);
  assert.equal(pair.fresh.balance,48);
  assert.equal(pair.elision.balance,53);
  assert.equal(pair.fresh.middle,1);
  assert.equal(pair.elision.middle,1);
  assert.equal(pair.fresh.spent-pair.elision.spent,5);
  assert.equal(pair.fresh.failure,null);
  assert.equal(pair.elision.failure,null);
});

test('the final task does not require a final acquisition or fictitious future credit',()=>{
  const pair=resourceComparison(84,1,6,true);
  assert.equal(pair.fresh.failure,null);
  assert.equal(pair.elision.failure,null);
  assert.equal(pair.fresh.balance,0);
  assert.equal(pair.elision.balance,0);
  assert.equal(pair.fresh.earned,0);
  assert.equal(pair.elision.spent,84);
});

test('guard, frozen entry bin, cap and integer accounting are visible at their boundaries',()=>{
  const a=resourceComparison(83,1,6),b=resourceComparison(84,1,6);
  assert.equal(a.fresh.repair,0);
  assert.equal(b.fresh.repair,1);
  assert.equal(resourceComparison(96,1,6).fresh.middle,0);
  const cap=conditionedTrace({balance:96,gate:0,write:0,gateCount:0,mode:'skip',enabled:0});
  assert.equal(cap.balance,96);
  assert.equal(cap.spilled,24);
  assert.ok(cap.conserved);
  assert.throws(()=>resourceComparison(97,1,6),RangeError);
  assert.throws(()=>resourceComparison(83.5,1,6),RangeError);
});

test('the published bounded conclusion is consistent across both endpoints and all paid-gate points',()=>{
  let paid=0,freeGains=0;
  for(const c of data.cases){
    if(c.prices.gate>0){
      paid++;
      for(const objective of ['tasks','cycles']){
        const r=c[objective];
        assert.equal(r.gain_over_best_no_enable_nand.exact,'0');
        for(const t of r.cost_at_survival_tolerance){
          assert.equal(data.enable_library[t.winner.enable].gate_count,0);
        }
      }
    }else if(c.tasks.gain_over_best_no_enable_nand.value>0)freeGains++;
  }
  assert.equal(paid,16);
  assert.equal(freeGains,2);
  assert.equal(displayNumber(selectCase(data,0,0,0).result.best_survival.survival),0.9174767896493894);
  assert.throws(()=>displayNumber({value:.9}),TypeError);
});
