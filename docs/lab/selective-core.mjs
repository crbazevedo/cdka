export const number=x=>typeof x==='number'?x:x.value;
export function polynomial(coeff,x){let out=0;for(let i=coeff.length-1;i>=0;i--)out=out*x+number(coeff[i]);return out;}
export function cost(row,gate=0.01,install=0.1){return number(row.writes)+gate*number(row.gate_events??row.gate_executions)+install*row.gates;}
export function choose(rows,baseline,tolerance,gate=0.01,install=0.1){const feasible=rows.filter(r=>r.survival>=baseline-tolerance-1e-13);if(!feasible.length)return null;return feasible.reduce((a,b)=>cost(a,gate,install)<=cost(b,gate,install)?a:b);}
export function pareto(rows,gate=0.01,install=0.1){let best=-1;return [...rows].sort((a,b)=>cost(a,gate,install)-cost(b,gate,install)||b.survival-a.survival).filter(r=>{if(r.survival>best+1e-13){best=r.survival;return true;}return false;});}
export function harmlessInput(repair,three){return Boolean(repair&&three);}
