/* CDKA v4: normalized effort, not joules. No free persistent policy seed.
   Analytic bounds are distinct from integer-grid optima. */
export const q=r=>.5*(1+(-Math.expm1(-r/2))**2);
export const ell=r=>{const x=Math.exp(-r/2);return Math.log1p(-x+x*x/2);};
export const slope=r=>{const x=Math.exp(-r/2);return x*(1-x)/(2*q(r));};
export const inflection=-2*Math.log(2-Math.SQRT2);
export const curvature=r=>{const x=Math.exp(-r/2);return -x*(x*x-4*x+2)/(2*(x*x-2*x+2)**2);};
export const produced=(w,e)=>.5*(1+(-Math.expm1(-w))*(-Math.expm1(-e)));
export function tangent(){let lo=inflection,hi=4;for(let i=0;i<65;i++){const m=(lo+hi)/2;if(m*slope(m)-ell(m)-Math.LN2>0)lo=m;else hi=m;}return (lo+hi)/2;}
export const rstar=tangent();
export const envelope=r=>r<=rstar?-Math.LN2+r*slope(rstar):ell(r);
export function grid(n,units,step=.2){
 if(!Number.isInteger(n)||n<1||!Number.isInteger(units)||units<0||!(step>0))throw Error('Invalid finite grid');
 const l=Array.from({length:units+1},(_,k)=>ell(k*step));
 let v=Array(units+1).fill(-Infinity),paths=Array(units+1).fill(null);v[0]=0;paths[0]=[];
 for(let t=0;t<n;t++){const vv=[],pp=[];for(let b=0;b<=units;b++){let best=-Infinity,bk=0;for(let k=0;k<=b;k++){const z=v[b-k]+l[k];if(z>best){best=z;bk=k;}}vv[b]=best;pp[b]=[...paths[b-bk],bk];}v=vv;paths=pp;}
 return {logValue:v[units],schedule:paths[units].map(k=>k*step)};
}
export function required(n,beta){
 if(!(Number.isInteger(n)&&n>0&&beta>=2-Math.SQRT2&&beta<1))throw Error('High-reliability theorem requires beta >= 2-sqrt(2)');
 const p=-Math.expm1(Math.log(beta)/n),x=2*p/(1+Math.sqrt(1-2*p));return -2*n*Math.log(x);
}
export function harvest(n,h,e0=0){
 let balance=e0,L=0;const out=[];const target=h<rstar?rstar:h;
 for(let t=0;t<n;t++){const spend=balance+1e-12>=target?Math.min(target,balance):0;L+=ell(spend);out.push({t:t+1,before:balance,spend,logSurvival:L});balance=balance-spend+h;}
 return {points:out,rate:L/n,balance,rateBound:envelope(h+e0/n)};
}
export const cycleBound=(sigma,p)=>.5*(1+(1-2*p)*sigma);
