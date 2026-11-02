/* CDKA v6: numeric mirror of the exact Fraction reference. Known tools. */
export const COST={hold:0,correct:1,refresh:2,service:2};
export const defaults={capacity:4,harvest:1,world_flip:.1,cell_flip:.02,write_flip:.01,correction_error:[.01,.2],sensor_error:[.04,.2],actuator_failure:[.005,.03],degradation:.05,service_success:.8};
export const states=p=>Array.from({length:4*(p.capacity+1)},(_,i)=>{const block=Math.floor(i/(p.capacity+1));return [Math.floor(block/2),block%2,i%(p.capacity+1)];});
const index=(p,k,h,b)=>(2*k+h)*(p.capacity+1)+b;
const choose=(n,k)=>{let r=1;for(let j=1;j<=k;j++)r=r*(n-j+1)/j;return r;};
export function binom(n,p){return Array.from({length:n+1},(_,j)=>choose(n,j)*p**j*(1-p)**(n-j));}
export function row(p,s,a){
 const [k,h,b]=s,N=4*(p.capacity+1),r=Array(N+1).fill(0);
 if(!(a in COST)||COST[a]>b)throw Error('Ação não implementável com este orçamento');
 const damage=Array(4).fill(0);
 for(const [f,pw] of [[0,1-p.world_flip],[1,p.world_flip]]){
  const old=f?3-k:k;
  binom(old,p.cell_flip).forEach((x,i)=>binom(3-old,p.cell_flip).forEach((y,j)=>{damage[old-i+j]+=pw*x*y;}));
 }
 let after=damage;
 if(a==='correct'||a==='refresh'){
  let good=a==='correct'?damage[0]+damage[1]:1-p.sensor_error[h];
  const c=p.correction_error[h];good=good*(1-c)+(1-good)*c;
  const g=binom(3,p.write_flip),bad=binom(3,1-p.write_flip);after=g.map((x,j)=>good*x+(1-good)*bad[j]);
 }
 let hs=h===0?[1-p.degradation,p.degradation]:[0,1];
 if(a==='service')hs=[p.service_success+(1-p.service_success)*hs[0],(1-p.service_success)*hs[1]];
 const nextB=Math.min(p.capacity,b-COST[a]+p.harvest);
 for(let j=0;j<=1;j++)for(let h1=0;h1<=1;h1++)r[index(p,j,h1,nextB)]=after[j]*(1-p.actuator_failure[h])*hs[h1];
 r[N]=Math.max(0,1-r.slice(0,N).reduce((x,y)=>x+y,0));return r;
}
export function solve(p,n,allowed=Object.keys(COST)){
 if(!Number.isInteger(n)||n<0||!allowed.includes('hold'))throw Error('Horizonte e políticas inválidos');
 const ss=states(p),N=ss.length;
 const kernels=ss.map(s=>Object.fromEntries(allowed.filter(a=>COST[a]<=s[2]).map(a=>[a,row(p,s,a)])));
 let v=Array(N).fill(1);const levels=[v],policies=[Array(N).fill('done')];
 for(let h=1;h<=n;h++){
  const next=[],pi=[];
  for(let i=0;i<N;i++){
   let best=-1,chosen='hold';
   for(const [a,r] of Object.entries(kernels[i])){let value=0;for(let j=0;j<N;j++)value+=r[j]*v[j];if(value>best+1e-14){best=value;chosen=a;}}
   next.push(best);pi.push(chosen);
  }
  v=next;levels.push(v);policies.push(pi);
 }
 return {states:ss,levels,policies};
}
export function contractBound(delta,n){if(delta<0||delta>1||!Number.isInteger(n)||n<0)throw Error('Contrato inválido');return 1-(1-delta)**n;}
export const tv=(a,b)=>a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)/2;
export function calibration(p,change,n){
 const q={...p,sensor_error:p.sensor_error.map(v=>Math.min(.5,v+change))};let delta=0;
 for(const s of states(p))for(const a of Object.keys(COST).filter(a=>COST[a]<=s[2]))delta=Math.max(delta,tv(row(p,s,a),row(q,s,a)));
 const actual=solve(p,n),approx=solve(q,n);
 const gap=Math.max(...actual.levels[n].map((v,i)=>Math.abs(v-approx.levels[n][i])));
 return {delta,bound:contractBound(delta,n),gap,actual,approx};
}
