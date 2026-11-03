/* CDKA v12 browser projections; Python certificate is the exact model oracle. */
export function rankAt(profile, horizon) {
  if(!Number.isInteger(horizon)||horizon<0)throw Error('nonnegative integer horizon');
  return profile[Math.min(horizon,profile.length-1)];
}
export function formalWords(alphabet, horizon) {
  if(!Number.isInteger(alphabet)||alphabet<1||!Number.isInteger(horizon)||horizon<0)throw Error('invalid word count');
  return BigInt(alphabet)**BigInt(horizon);
}
export function classMap(groups,n) {
  const result=Array(n).fill(-1);
  groups.forEach((g,k)=>g.forEach(i=>{if(i<0||i>=n||result[i]!==-1)throw Error('invalid partition');result[i]=k;}));
  if(result.some(x=>x<0))throw Error('partition incomplete');
  return result;
}
export function delayedResponse(start, word) {
  const map={prepare:[2,3,2,3],check:[0,1,2,-1]};let state=start;const trace=[state];
  for(const a of word){if(!(a in map))throw Error('unknown command');if(state>=0)state=map[a][state];trace.push(state);}
  return {trace,survives:state>=0?1:0};
}
export function nuisanceBound(bits){if(!Number.isInteger(bits)||bits<0)throw Error('invalid bits');return {states:2n**BigInt(bits+1),rank:2,tests:5};}
