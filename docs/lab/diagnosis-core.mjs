/* CDKA v7, browser-only numeric mirror of exact rational Python model.
   Raw physical one-step payoffs come from v6 macro_row on the same initial
   state, deadline, and absorbing-failure criterion. No physical energy
   calibration or mathematical novelty is claimed. */
export const COST={hold:0,correct:1,refresh:2,service:2};
export const PAYOFF={
  0:{hold:[.894557536,.872081216],correct:[.8863844719143731,.7171103093571584],refresh:[.945778666584,.6594959384],service:[.894557536,.872081216]},
  1:{hold:[.864602464,.842878784],correct:[.8570459975128268,.6995992929468416],refresh:[.945778666584,.6594959384],service:[.864602464,.842878784]}
};
export const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const actions=b=>Object.keys(COST).filter(a=>COST[a]<=b);
export const errorAfter=(eta,nu,age=1)=>.5*(1-(1-2*eta)*Math.pow(1-2*nu,age));
export function evaluate(s={}){
 const k=s.k??0,B=s.B??4,eta=s.eta??0,nu=s.nu??0,age=s.age??1,
  inspectionFailure=s.inspectionFailure??0,d=s.d??1,c=s.c??1,prior=s.prior??.5;
 if(![0,1].includes(k)||!Number.isInteger(B)||B<0||B>4||![eta,nu,prior,inspectionFailure].every(x=>x>=0&&x<=1)||eta>.5||nu>.5||
 !Number.isInteger(age)||age<0||!Number.isInteger(d)||d<0||!Number.isInteger(c)||c<0)
  throw Error('Invalid diagnosis configuration');
 const nuAge=(1-Math.pow(1-2*nu,age))/2;
 const initial=[1-prior,prior],joint=Array.from({length:2},()=>[0,0]);
 for(let h0=0;h0<2;h0++)for(let y=0;y<2;y++)for(let hf=0;hf<2;hf++){
  const sense=y===h0?1-eta:eta,drift=hf===h0?1-nuAge:nuAge;
  joint[hf][y]+=initial[h0]*sense*drift;
 }
 const scores=actions(B).map(a=>({a,value:PAYOFF[k][a].reduce((v,score,h)=>v+score*(joint[h][0]+joint[h][1]),0)}));
 scores.sort((a,b)=>b.value-a.value);
 const baseline=scores[0];
 const oracle=Array.from({length:2},(_,h)=>Math.max(...actions(B).map(a=>PAYOFF[k][a][h]))*(joint[h][0]+joint[h][1])).reduce((a,b)=>a+b,0);
 const available=B>=d+c ? actions(B-d-c):[];
 let diagnosis=null,policy=null;
 if(available.length){
  const perSignal=[0,1].map(y=>{
   const values=available.map(a=>({a,value:joint[0][y]*PAYOFF[k][a][0]+joint[1][y]*PAYOFF[k][a][1]}));
   values.sort((a,b)=>b.value-a.value);return values[0];
  });
  policy=perSignal.map(x=>x.a);
  diagnosis=(1-inspectionFailure)*(perSignal[0].value+perSignal[1].value);
 }
 const actual=diagnosis===null?baseline.value:Math.max(baseline.value,diagnosis);
 return {joint,baseline,oracle,diagnosis,policy,actual,gain:actual-baseline.value,
         healthError:errorAfter(eta,nu,age),remaining:B-d-c,available,
         affordable:available.includes('refresh'),
         inspect:diagnosis!==null&&diagnosis>baseline.value+1e-12};
}
export function threshold(k=0){
 const h=PAYOFF[k];const g=h.refresh[0]-h.hold[0],loss=h.hold[1]-h.refresh[1];
 return {g,loss,eta:g/(g+loss)};
}
