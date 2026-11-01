/* CDKA Visual Lab — deterministic, dependency-free model kernels.
   Scientific statuses: B1/T1 established elementary baselines;
   T2 is an exact Gaussian illustrative model plus an asymptotic limit;
   T3–T6 are model demonstrations, NOT new theorems. */
export const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
export const binaryEntropy = p => p <= 0 || p >= 1 ? 0 :
  -p*Math.log2(p)-(1-p)*Math.log2(1-p);

function popcount(n) { let k=0; while(n) { n &= n-1; k++; } return k; }

/** Relation: rows=worlds, cols=actions, values truthy iff action safe.
    Deterministic encoder, perfect observation, one-shot robust choice. */
export function minimumCover(rows) {
  if (!rows.length) return {cover:[],k:0,bits:0,feasible:true};
  const m=rows[0].length;
  if (m > 20) throw Error('Interactive exact cover accepts at most 20 actions');
  if (!rows.every(row => row.length===m)) throw Error('Rectangular matrix required');
  let best=null;
  for (let mask=1;mask<(1<<m);mask++) {
    if(best !== null && popcount(mask)>=popcount(best)) continue;
    if(rows.every(row => row.some((safe,j)=>safe && (mask & (1<<j))))) best=mask;
  }
  if(best===null) return {cover:[],k:null,bits:null,feasible:false};
  const cover=Array.from({length:m},(_,j)=>j).filter(j=>best & (1<<j));
  return {cover,k:cover.length,bits:cover.length<2?0:Math.ceil(Math.log2(cover.length)),feasible:true};
}
export function faces(rows) {
  const n=rows.length,m=rows[0]?.length||0;
  const out=[];
  for(let mask=1;mask<(1<<n);mask++) {
    const worlds=Array.from({length:n},(_,i)=>i).filter(i=>mask&(1<<i));
    if(Array.from({length:m},(_,j)=>j).some(j=>worlds.every(i=>rows[i][j]))) out.push(worlds);
  }
  return out;
}
export function horizonGain(T) {
  return T===Infinity?1: -Math.expm1(-T);
}
export function t1({lambda=1,horizon=Infinity,boundary=1.5,neutral=false}={}) {
  if(lambda<0||!(horizon>0)||boundary<=0) throw Error('invalid T1 parameters');
  const actions=neutral?[-1,0,1]:[-1,1];
  const worlds=[-1,1];
  const maxGain=horizonGain(horizon);
  const rows=worlds.map(w=>actions.map(u=>Math.abs(lambda*w+u)*maxGain<=boundary+1e-10));
  return {worlds,actions,rows,gain:maxGain,cover:minimumCover(rows)};
}
export function t1trajectory(lambda,w,u,T=8) {
  return Array.from({length:101},(_,i)=>{
    const t=T*i/100;return [t, (lambda*w+u)*(-Math.expm1(-t))];
  });
}
// Abramowitz-Stegun erf approximation. Suitable for educational Gaussian plots.
export function erf(x) {
  const s=Math.sign(x),z=Math.abs(x),t=1/(1+0.3275911*z);
  const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-z*z);
  return s*y;
}
export function normalTail(z) {
  if(z<0) return 1-normalTail(-z);
  if(z>8) {
    const inv=1/z;
    // Mills ratio (leading asymptotic terms), avoids cancellation at large z.
    return Math.exp(-z*z/2)/Math.sqrt(2*Math.PI)*
      (inv-inv**3+3*inv**5-15*inv**7+105*inv**9);
  }
  return 0.5*(1-erf(z/Math.SQRT2));
}
export function gaussianFailure(mu,epsilon,boundary=1.5) {
  const s=Math.sqrt(epsilon);
  return clamp(normalTail((boundary-mu)/s)+normalTail((boundary+mu)/s),0,1);
}
export function gaussianRate(mu,boundary=1.5) {
  const d=Math.max(0,boundary-Math.abs(mu));
  return d*d/2;
}
export function t2({lambda=1,epsilon=0.2,c=0.3,boundary=1.5}={}) {
  if(epsilon<=0||c<=0||lambda<0) throw Error('Invalid T2 settings');
  const worlds=[-1,1],actions=[-1,1],alpha=Math.exp(-c/epsilon);
  const failure=worlds.map(w=>actions.map(u=>gaussianFailure(lambda*w+u,epsilon,boundary)));
  const rates=worlds.map(w=>actions.map(u=>gaussianRate(lambda*w+u,boundary)));
  const rows=failure.map(row=>row.map(p=>p<=alpha));
  const limiting=rates.map(row=>row.map(j=>j>c+1e-9));
  const ties=rates.some(row=>row.some(j=>Math.abs(j-c)<1e-9));
  return {worlds,actions,alpha,failure,rates,rows,limiting,ties,
          exact:minimumCover(rows),asymptotic:minimumCover(limiting)};
}
export function t3success(i,u,r,{sensorScale=2,controlScale=2,repairScale=2}={}) {
  const quality=1-0.5*Math.exp(-i/sensorScale);
  const effective=1-Math.exp(-u/controlScale);
  const maintained=1-Math.exp(-r/repairScale);
  return {success:quality*effective*maintained,quality,effective,maintained,
          information:1-binaryEntropy(1-quality)};
}
export function t3({budget=12,target=0.6,scales={}}={}) {
  if(!Number.isInteger(budget)||budget<0) throw Error('Budget must be nonnegative integer');
  const allocations=[];
  let best=null;
  for(let i=0;i<=budget;i++) for(let u=0;u<=budget-i;u++) {
    const r=budget-i-u;
    const v=t3success(i,u,r,scales);
    const a={i,u,r,...v,feasible:v.success>=target};
    allocations.push(a);
    if(!best||a.success>best.success)best=a;
  }
  return {allocations,best,feasible:allocations.some(x=>x.feasible),
          frontier:Array.from({length:budget+1},(_,b)=>{
            let max=0;
            for(let i=0;i<=b;i++)for(let u=0;u<=b-i;u++)
              max=Math.max(max,t3success(i,u,b-i-u,scales).success);
            return [b,max];
          })};
}
export function t4({horizon=7,health=1,tokens=1,q=0.95,maxHealth=3,repairGain=2}={}) {
  if(!Number.isInteger(horizon)||horizon<0||!Number.isInteger(health)||health<0||
     !Number.isInteger(tokens)||tokens<0||q<0.5||q>1)throw Error('Invalid T4');
  const cache=new Map();
  function V(h,z,r) {
    if(h===0)return {value:1,action:'done'};
    const key=[h,z,r].join(',');
    if(cache.has(key)) return cache.get(key);
    let best={value:0,action:'blind'};
    const choices=[{action:'blind',value:0.5*V(h-1,z,r).value}];
    if(z>0)choices.push({action:'sense',value:q*V(h-1,z-1,r).value});
    if(r>0&&z<maxHealth) choices.push({action:'repair',value:0.5*
      V(h-1,Math.min(maxHealth,z+repairGain),r-1).value});
    for(const choice of choices)if(choice.value>best.value+1e-12)best=choice;
    cache.set(key,best);
    return best;
  }
  const main=V(horizon,Math.min(health,maxHealth),tokens);
  const curve=Array.from({length:horizon+1},(_,h)=>
    [h,V(h,Math.min(health,maxHealth),tokens).value,
       V(h,Math.min(health,maxHealth),0).value]);
  const grid=Array.from({length:horizon},(_,j)=>{
    const h=horizon-j;
    return Array.from({length:maxHealth+1},(_,z)=>({h,z,...V(h,z,tokens)}));
  });
  return {value:main.value,first:main.action,curve,grid};
}
export function t5({impulse=1.2,gain=0.7,step=13,steps=32,actuator=1.2}={}) {
  const names=['feedback','replay','lesion'];
  const tracks={feedback:[0],replay:[0],lesion:[0]};
  const inputs={feedback:[],replay:[],lesion:[]};
  const disturbances=t=>0.12*Math.sin(t*0.52)+(t===step?impulse:0);
  const baselineActions=[];
  let reference=0;
  for(let t=0;t<steps;t++){
    const u=clamp(-gain*reference,-actuator,actuator);
    baselineActions.push(u);
    reference=0.87*reference+0.12*Math.sin(t*0.52)+u;
  }
  for(let t=0;t<steps;t++){
    for(const name of names){
      const x=tracks[name].at(-1);
      const u=name==='replay'?baselineActions[t]:
         name==='lesion'&&t>=step?0:clamp(-gain*x,-actuator,actuator);
      inputs[name].push(u);
      tracks[name].push(0.87*x+disturbances(t)+u);
    }
  }
  return {tracks,inputs,steps,step,impulse};
}
export function replicatorDerivative(p,x,{beta=2,eta=0.8,rho=1}={}) {
  return [beta*p*(1-p)*x, -rho*x+eta*(2*p-1)];
}
export function replicator({p0=0.35,x0=0.2,beta=2,eta=0.8,rho=1,T=18,dt=0.035}={}) {
  if(!(p0>0&&p0<1&&T>0&&dt>0&&beta>0&&eta>0&&rho>0))throw Error('Invalid replicator');
  // Evolve log odds z=log(p/(1-p)), NOT p directly. In p-coordinates
  // round-off near 0 or 1 destroys the identity dz/dt = beta*x.
  const sigmoid=z=>z>=0?1/(1+Math.exp(-z)):Math.exp(z)/(1+Math.exp(z));
  let z=Math.log(p0/(1-p0)),x=x0;
  const n=Math.ceil(T/dt),h=T/n;
  const points=[[0,p0,x,z]];
  const deriv=(a,b)=>[beta*b,-rho*b+eta*(2*sigmoid(a)-1)];
  for(let k=1;k<=n;k++){
    const [a,b]=deriv(z,x),
          [c,d]=deriv(z+a*h/2,x+b*h/2),
          [e,f]=deriv(z+c*h/2,x+d*h/2),
          [g,j]=deriv(z+e*h,x+f*h);
    z+=h*(a+2*c+2*e+g)/6;
    x+=h*(b+2*d+2*f+j)/6;
    points.push([k*h,sigmoid(z),x,z]);
  }
  return {points,stableA:[0,-eta/rho],stableB:[1,eta/rho],saddle:[.5,0],
          finalP:sigmoid(z),finalX:x};
}
