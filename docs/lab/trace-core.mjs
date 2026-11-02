// v11: floats render formulas cross-checked with exact rational Python.
export function routeProbabilities(p){
 if(!(p>=0&&p<=.5))throw Error('p must be in [0,.5]');
 return {injective:p*(1-p),merged:p*p};
}
export function routeGain(p,margin){const r=routeProbabilities(p);return (r.injective-r.merged)*margin/3;}
export function massOf(rows){return rows.reduce((s,t)=>s+t.probability.value,0);}
export function filterTraces(rows,{outcome='all',signal='all'}={}){
 return rows.filter(t=>(outcome==='all'||t.outcome===outcome)&&(signal==='all'||t.signal_evaluator_only===Number(signal)));
}
export function runtimeColumns(t){return {word:t.readable_word,first:t.steps[0].action,
 next:t.steps[0].after==='dead'?null:[t.steps[0].after[0],t.steps[0].after[2]],
 second:t.steps.length===2?t.steps[1].action:null,outcome:t.outcome};}
