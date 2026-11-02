import test from 'node:test';
import assert from 'node:assert/strict';
import {DATA,partitions,evaluate,best,required,analyze,updateConflict} from '../docs/lab/continuation-core.mjs';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-12,`${a} != ${b}`);
test('Browser matches all exact default Python certificate values',()=>{
 for(const row of DATA.default){const x=best(.01,2,row.capacity);near(x.value,row.value);near(x.loss,row.loss);assert.deepEqual(x.labels,row.encoding);}
});
test('Horizon-specific memory can increase or decrease',()=>{
 assert.equal(required(.01,1),2);assert.equal(required(.01,2),3);
 assert.equal(required(.15,1),2);assert.equal(required(.15,2),1);
});
test('Exact hull breakpoints connect equal affine profiles',()=>{
 for(const h of [1,2]){const t=DATA.tables[String(h)];for(let i=0;i<t.plans.length-1;i++){
  const p=t.intervals[i].hi,a=t.plans[i].alpha,b=t.plans[i+1].alpha;
  near(p*a[0]+(1-p)*a[1],p*b[0]+(1-p)*b[1]);
 }}
});
test('Best physical code never performs worse when optional capacity is added',()=>{
 for(let i=0;i<=50;i++){const e=i/100;for(const h of [1,2]){
  const a=best(e,h,1).value,b=best(e,h,2).value,c=best(e,h,3).value;
  assert.ok(a<=b+1e-12&&b<=c+1e-12);
 }}
});
test('Blackwell weakening of this sensor family cannot improve value',()=>{
 for(const k of [1,2,3])for(const h of [1,2]){
  let old=Infinity;for(let i=0;i<=50;i++){const v=best(i/100,h,k).value;assert.ok(v<=old+1e-12);old=v;}
 }
});
test('Flagged erasure has the declared affine value, not noisy-driver semantics',()=>{
 const a=analyze({erasure:0}),b=analyze({erasure:.4}),c=analyze({erasure:1});
 near(b.delivered,.6*a.value+.4*c.constant);near(c.delivered,c.constant);
});
test('A decoder cannot recreate a discarded history',()=>{
 const e=[{code:0,action:'service',observation:'unanimous',next:0},
          {code:0,action:'service',observation:'unanimous',next:1}];
 assert.ok(updateConflict(e));e[1].code=1;assert.ok(!updateConflict(e));
});
test('Invalid controls and basic partition catalog',()=>{
 assert.equal(partitions.length,5);assert.throws(()=>best(.1,2,0));
 assert.throws(()=>evaluate(.7,2));assert.throws(()=>analyze({erasure:-1}));
});
