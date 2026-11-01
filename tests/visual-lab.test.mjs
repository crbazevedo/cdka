import test from 'node:test';
import assert from 'node:assert/strict';
import {
  minimumCover,faces,t1,horizonGain,t2,gaussianFailure,gaussianRate,
  t3,t3success,t4,t5,replicator,replicatorDerivative
} from '../docs/lab/core.mjs';

test('B1: all 512 3x3 relations agree with independent partition encoder',()=>{
  function partitionMinimum(rows){
    if(rows.some(row=>!row.some(Boolean)))return null;
    for(let codes=1;codes<=3;codes++){
      for(let assignments=0;assignments<codes**3;assignments++){
        const a=Array.from({length:3},(_,i)=>Math.floor(assignments/codes**i)%codes);
        if(Array.from(new Set(a)).every(c=>rows[0].some((_,j)=>
          a.every((which,i)=>which!==c||rows[i][j]))))return new Set(a).size;
      }
    }
    return null;
  }
  for(let mask=0;mask<512;mask++){
    const rows=Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>!!(mask&(1<<(i*3+j)))));
    assert.equal(minimumCover(rows).k,partitionMinimum(rows),'mask '+mask);
  }
});
test('B1: pairwise compatible, not triple',()=>{
  const rows=[[true,true,false],[false,true,true],[true,false,true]];
  assert.equal(minimumCover(rows).k,2);
  const complexes=faces(rows);
  assert.equal(complexes.filter(f=>f.length===2).length,3);
  assert.equal(complexes.some(f=>f.length===3),false);
});
test('T1: exact thresholds with infinite time and discrete actions',()=>{
  for(const [l,k] of [[0,1],[.5,1],[.5001,2],[2.5,2],[2.5001,null]]){
    assert.equal(t1({lambda:l}).cover.k,k);
  }
  assert.equal(t1({lambda:1,neutral:true}).cover.k,1);
  assert.equal(t1({lambda:1,neutral:false}).cover.k,2);
});
test('T1: finite horizon shifts decision thresholds',()=>{
  const T=Math.log(2);assert.ok(Math.abs(horizonGain(T)-.5)<1e-12);
  for(const [l,k] of [[2,1],[2.01,2],[4,2],[4.01,null]]){
    assert.equal(t1({lambda:l,horizon:T}).cover.k,k);
  }
});
test('T2: Gaussian risk, monotonic and asymptotic rate',()=>{
  assert.ok(Math.abs(gaussianFailure(0,1,1.5)-0.133614)<0.001);
  assert.ok(gaussianFailure(0,.1,1.5)<gaussianFailure(0,.3,1.5));
  const mu=.6,rate=gaussianRate(mu);
  const effective=-.08*Math.log(gaussianFailure(mu,.08));
  assert.ok(Math.abs(effective-rate)<.25);
  assert.ok(t2({lambda:1,epsilon:.2,c:.3}).failure.flat().every(v=>v>=0&&v<=1));
});
test('T3: simplex allocations conserve total budget and optimum matches max',()=>{
  for(let b=0;b<=13;b++){
    const r=t3({budget:b});
    assert.equal(r.allocations.length,(b+1)*(b+2)/2);
    assert.ok(r.allocations.every(a=>a.i+a.u+a.r===b&&a.success>=0&&a.success<=1));
    assert.equal(r.best.success,Math.max(...r.allocations.map(a=>a.success)));
  }
  assert.equal(t3success(0,0,0).success,0);
});
test('T4: dynamic programming honors horizon, increased resources do not worsen value',()=>{
  for(let h=0;h<10;h++){
    const x=t4({horizon:h,health:1,tokens:2,q:.91});
    assert.ok(x.value>=0&&x.value<=1);
    assert.ok(x.value+1e-10>=t4({horizon:h,health:1,tokens:0,q:.91}).value);
    if(h>0) assert.ok(x.value<=t4({horizon:h-1,health:1,tokens:2,q:.91}).value+1e-10);
  }
});
test('T5: external replay observationally matches prior to impulse, diverges after',()=>{
  const r=t5({impulse:2,step:12,gain:.9});
  for(let k=0;k<=12;k++)assert.ok(Math.abs(r.tracks.feedback[k]-r.tracks.replay[k])<1e-11);
  assert.ok(Math.abs(r.tracks.feedback[16]-r.tracks.replay[16])>.01);
});
test('T6: replicator fixed points and accumulation of log odds',()=>{
  assert.deepEqual(replicatorDerivative(.5,0),[0,0]);
  const r=replicator({p0:.7,x0:.3});
  assert.ok(r.finalP>r.points[0][1]);
  let integral=0;const pts=r.points,beta=2;
  for(let k=1;k<pts.length;k++)
    integral+=beta*(pts[k][0]-pts[k-1][0])*(pts[k][2]+pts[k-1][2])/2;
  const change=pts.at(-1)[3]-pts[0][3];
  assert.ok(Math.abs(change-integral)<.01);
});
