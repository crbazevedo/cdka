/** Float UI mirror. Decisive certificates are exact Fractions in Python. */
export const BITS=Array.from({length:8},(_,i)=>[i>>2&1,i>>1&1,i&1]);
const GATES=[[0,1],[0,2],[1,2],[3,4],[6,6],[5,7]];
export const DEFAULT={diagnostic:.15,sensor:.02,drift:.05,restore:.8,procedure:.005,prior:.5,horizon:8};
export const MODES=['skip','service','vote','inverse'];
export const PHASES=[];for(const [v,z]of[[0,0],[0,1],[1,1]])for(let b=1;b<=4;b++)PHASES.push([v,z,b]);
const index=new Map(PHASES.map((x,i)=>[x.join(','),i]));
export function execute(bits,mask){const wires=bits.slice();GATES.forEach(([a,b],i)=>wires.push((1-(wires[a]&wires[b]))^(mask>>i&1)));return wires.at(-1);}
export function voter(bits,gamma){let p=0;for(let mask=0;mask<64;mask++){let k=mask.toString(2).replaceAll('0','').length;p+=gamma**k*(1-gamma)**(6-k)*execute(bits,mask);}return p;}
const TABLE=[.001,.02].map(g=>BITS.map(bits=>voter(bits,g)));
export function report(bits,z,e){const d=bits.filter(x=>x!==z).length;return e**d*(1-e)**(3-d);}
export function work(z,e=.02){let sum=0;for(let w=0;w<2;w++)BITS.forEach((bits,i)=>sum+=.5*report(bits,w,e)*(w?TABLE[z][i]:1-TABLE[z][i]));return sum;}
export function selection(z,bits,b,policy){if(b<3)return 0;const mode=policy[b-3];if(mode==='skip')return 0;if(mode==='service')return 1;const p=TABLE[z][BITS.findIndex(x=>x.join()==bits.join())];return mode==='vote'?p:1-p;}
export function kernel(policy,opts=DEFAULT){const x={...DEFAULT,...opts};const Q=PHASES.map(()=>Array(12).fill(0));const attempts=Array(12).fill(0);for(let i=0;i<12;i++){
 const[v,z,b]=PHASES[i];let repair=0;BITS.forEach(bits=>repair+=report(bits,v,x.diagnostic)*selection(z,bits,b,policy));attempts[i]=repair;
 for(let r=0;r<2;r++){
  const pd=r?repair:1-repair,proc=r?1-x.procedure:1,bnext=Math.min(4,b+1-2*r);
  if(!pd)continue;if(b-1-2*r<0)throw Error('negative physical budget');
  const hs=r&&z===1?[[0,x.restore],[1,1-x.restore]]:[[z,1]];
  for(const[h,ph]of hs){const mass=pd*proc*ph*work(h,x.sensor);const zs=h===0?[[0,1-x.drift],[1,x.drift]]:[[1,1]];
   for(const[z1,pz]of zs)Q[i][index.get([h,z1,bnext].join(','))]+=mass*pz;
  }
 }
}return{Q,attempts};}
export function run(policy,opts={}){const x={...DEFAULT,...opts};if(!Number.isInteger(x.horizon)||x.horizon<0||x.horizon>128)throw Error('finite horizon required');let mu=Array(12).fill(0);mu[index.get('0,0,3')]=1-x.prior;mu[index.get('1,1,3')]=x.prior;const{Q,attempts}=kernel(policy,x);const curve=[1];let services=0,completed=0,spent=1;for(let t=0;t<x.horizon;t++){
 const mass=mu.reduce((a,b)=>a+b,0),r=mu.reduce((a,b,i)=>a+b*attempts[i],0);services+=r;spent+=mass+2*r;
 const next=Array(12).fill(0);mu.forEach((p,i)=>Q[i].forEach((q,j)=>next[j]+=p*q));mu=next;const live=mu.reduce((a,b)=>a+b,0);curve.push(live);completed+=live;
}return{policy:policy.join('/'),curve,survival:curve.at(-1),services,completed,spent,law:mu,healthy:mu.reduce((p,w,i)=>p+(PHASES[i][1]===0?w:0),0)};}
export function solve(opts={}){const rows=[];for(const a of MODES)for(const b of MODES)rows.push(run([a,b],opts));rows.sort((a,b)=>b.survival-a.survival||a.policy.localeCompare(b.policy));return{best:rows[0],rows,blind:rows.filter(x=>x.policy.split('/').every(y=>['skip','service'].includes(y)))[0]};}
export function traceState(state,opts={}){const x={...DEFAULT,...opts};const[z,bits,b]=state,repair=selection(z,bits,b,['vote','vote']);const no=work(z,x.sensor),after=(1-x.procedure)*(z===0?work(0,x.sensor):x.restore*work(0,x.sensor)+(1-x.restore)*work(1,x.sensor));return{repair,no,after,value:(1-repair)*no+repair*after,gain:after-no,balanceWithout:Math.min(4,b+1),balanceWith:Math.min(4,b-1)};}
