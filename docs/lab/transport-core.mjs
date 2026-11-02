/* Floating browser mirror of exact Fraction proofs in diagnostic_transport.py.
   Fair hidden H and independent channels only. Not general POMDP synthesis. */
export const TABLE=[[.894557536,.945778666584],[.872081216,.6594959384]];
export const BASE=(TABLE[0][0]+TABLE[1][0])/2;
export const G=TABLE[0][1]-TABLE[0][0], LOSS=TABLE[1][0]-TABLE[1][1];
export const DEFAULT={budget:6,ticks:1,eta:.05,rho:.6,bad:.5,wear:0,drift:0,flip:0,service:.8,risk:0,driver:'flip'};
export function entropy(p){if(p===0||p===1)return 0;return -p*Math.log2(p)-(1-p)*Math.log2(1-p);}
export function evaluate(settings={},protect=false,service=false){
 const s={...DEFAULT,...settings};
 for(const k of ['rho','bad','wear','service','risk'])if(!(s[k]>=0&&s[k]<=1))throw Error(k+' out of range');
 for(const k of ['eta','drift','flip'])if(!(s[k]>=0&&s[k]<=.5))throw Error(k+' out of range');
 if(!Number.isInteger(s.ticks)||s.ticks<1||!Number.isInteger(s.budget)||s.budget<0)throw Error('integer repair count and budget required');
 if(!['flip','silent'].includes(s.driver))throw Error('unknown output driver');
 const e=(1-(1-2*s.eta)*((1-2*s.drift)*(1-2*s.flip))**s.ticks)/2;
 const retention=protect?1:(1-s.rho)**s.ticks;
 const bad=(1-(1-s.bad)*(1-s.wear)**s.ticks)*(service?1-s.service:1);
 const theta=.3*bad,U=Math.max(0,G-e*(G+LOSS));
 const cost=s.ticks+4+(protect?s.ticks:0)+(service?1:0);
 const raw=s.driver==='flip'?BASE-theta*(LOSS-G)/2+retention*(1-2*theta)*U/2:
   BASE+retention*(1-theta)*U/2;
 const value=(1-s.risk)*raw;
 return {value,gain:value-BASE,cost,feasible:s.budget>=cost,e,theta,retention,info:retention*(1-entropy(e)),U};
}
export function optimize(settings={}){
 const s={...DEFAULT,...settings};
 const options=[{name:'Sem diagnóstico',key:'skip',value:s.budget>=s.ticks?BASE:0,cost:s.ticks,feasible:s.budget>=s.ticks}];
 for(const [p,r,name,key] of [[false,false,'Diagnóstico','diagnose'],[true,false,'Proteger memória','protect+diagnose'],[false,true,'Reparar seletor','service'],[true,true,'Proteger + reparar','protect+service']]){
   options.push({name,key,...evaluate(s,p,r)});
 }
 let best=options[0];for(const o of options)if(o.feasible&&o.value>best.value+1e-14)best=o;
 return {options,best};
}
