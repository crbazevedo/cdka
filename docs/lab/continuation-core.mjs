// Browser mirror of exact Python certificates; numbers are floating point.
import {DATA} from './continuation-data.mjs';
export {DATA};
export const partitions=[[0,0,0],[0,0,1],[0,1,0],[0,1,1],[0,1,2]];
export function evaluate(tail=.01,horizon=2,labels=[0,0,1]){
 if(!(tail>=0&&tail<=.5)||![1,2].includes(horizon)||labels.length!==3)throw Error('invalid interface');
 const ps=[tail,.5,1-tail],library=DATA.tables[String(horizon)].plans;
 const table=ps.map(p=>library.map(pi=>(p*pi.alpha[0]+(1-p)*pi.alpha[1])/3));
 let value=0;const selected={};
 for(const m of new Set(labels)){
  const scores=library.map((_,j)=>table.reduce((s,row,y)=>s+(labels[y]===m?row[j]:0),0));
  let j=0;for(let k=1;k<scores.length;k++)if(scores[k]>scores[j]+1e-15)j=k;
  selected[m]=library[j];value+=scores[j];
 }
 const full=table.reduce((s,row)=>s+Math.max(...row),0);
 return {tail,horizon,labels,value,full,loss:Math.max(0,full-value),selected,ps,library};
}
export function best(tail=.01,horizon=2,capacity=2){
 if(![1,2,3].includes(capacity))throw Error('capacity');
 let result=null;
 for(const labels of partitions)if(new Set(labels).size<=capacity){
  const next=evaluate(tail,horizon,labels);
  if(!result||next.value>result.value+1e-15)result=next;
 }
 return result;
}
export function required(tail,horizon){
 for(let k=1;k<=3;k++)if(best(tail,horizon,k).loss<1e-12)return k;
 return 3;
}
export function analyze({tail=.01,horizon=2,capacity=2,erasure=0}={}){
 if(!(erasure>=0&&erasure<=1))throw Error('erasure');
 const chosen=best(tail,horizon,capacity),constant=best(tail,horizon,1);
 const delivered=(1-erasure)*chosen.value+erasure*constant.value;
 return {...chosen,delivered,constant:constant.value,required:required(tail,horizon),
  transportedFull:(1-erasure)*chosen.full+erasure*constant.value,
  frontier:[1,2,3].map(k=>({...best(tail,horizon,k),capacity:k}))};
}
export function updateConflict(edges){
 const table=new Map();
 for(const {code,action,observation,next} of edges){
  const key=JSON.stringify([code,action,observation]);
  if(table.has(key)&&table.get(key)!==next)return true;
  table.set(key,next);
 }
 return false;
}
