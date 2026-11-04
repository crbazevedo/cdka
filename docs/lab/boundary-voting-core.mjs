// Browser projections only; exact Fraction oracles generate the source certificate.
export const number=x=>x&&typeof x==='object'&&'value'in x?x.value:x;
export function profileAt(profile,g){return profile.map(row=>row.reduce((s,n,k)=>s+n*g**k*(1-g)**(row.length-1-k),0));}
export function topologyGap(g){return 2*g*(1-g)*(1-2*g)**2;}
export function voteOutput(r,table,shared=false){if(shared)return(1-r)*table[0]+r*table[7];let v=0;for(let i=0;i<8;i++){let k=((i>>2)&1)+((i>>1)&1)+(i&1);v+=r**k*(1-r)**(3-k)*table[i];}return v;}
export function value(data,channel,p,enc=[3,0,0]){let out=0;for(let y=0;y<3;y++)for(let m=0;m<4;m++){let d=((m^enc[y])&1)+(((m^enc[y])>>1)&1),w=p**d*(1-p)**(2-d);for(let k=0;k<2;k++){let r=channel[2*m+k];out+=w*((1-r)*number(data.task_payoffs[y][k][0])+r*number(data.task_payoffs[y][k][1]));}}return out;}
export function portfolio(data,{p=.01,gamma=.02,healthy=.001,success=.8}={}){if([p,gamma,healthy].some(x=>x<0||x>.5)||success<0||success>1)throw Error('Invalid probabilities');const low=profileAt(data.module_profile,healthy),single=profileAt(data.module_profile,gamma),voteBad=profileAt(data.voter_profile,gamma),voteGood=profileAt(data.voter_profile,healthy),triple=single.map(r=>voteOutput(r,voteBad)),tripleGood=single.map(r=>voteOutput(r,voteGood));const mix=(a,b)=>a.map((x,i)=>success*x+(1-success)*b[i]);return[
{id:'bypass',gates:0,service:0,label:'Comando fixo',value:number(data.portfolio[0].value)},
{id:'single',gates:4,service:0,label:'Seletor simples',value:value(data,single,p)},
{id:'single_maintained',gates:4,service:1,label:'Seletor mantido',value:value(data,mix(low,single),p)},
{id:'triple',gates:18,service:0,label:'Triplicado + votador',value:value(data,triple,p)},
{id:'triple_voter_maintained',gates:18,service:1,label:'Votador mantido',value:value(data,mix(tripleGood,triple),p)},
{id:'shared_output_voted',gates:10,service:0,label:'Mesmo sinal triplicado',value:value(data,single.map(r=>voteOutput(r,voteBad,true)),p)}];}
