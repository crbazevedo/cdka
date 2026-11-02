import {DEFAULT,evaluate,optimize,BASE} from './transport-core.mjs';
const s={...DEFAULT};const ids=['budget','ticks','eta','rho','bad','service','drift','risk','driver'];
const C={green:'#356b56',red:'#a95c4e',ink:'#253d31',gray:'#8b9b8d',blue:'#567c95',line:'#e3e8dc'};
const pct=v=>(100*v).toFixed(3)+'%';const pp=v=>(100*v).toFixed(3)+' pp';const clean=x=>Number(x).toFixed(2).replace(/\.00$/,'');
const svg=(w,h,body,label)=>`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
function mix(a,b,t){const rgb=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)),A=rgb(a),B=rgb(b);return 'rgb('+A.map((x,i)=>Math.round(x*(1-t)+B[i]*t)).join(',')+')';}
function programs(r){
 const W=700,H=232,L=160,R=78,pw=W-L-R,low=.8,high=.93;
 const X=x=>L+pw*(Math.max(low,Math.min(high,x))-low)/(high-low);
 let o='';for(let j=0;j<=4;j++){const value=low+(high-low)*j/4,x=X(value);o+=`<line x1="${x}" x2="${x}" y1="9" y2="196" stroke="${C.line}"/><text x="${x}" y="220" text-anchor="middle" font-size="10" fill="${C.gray}">${(100*value).toFixed(1)}%</text>`;}
 o+=`<line x1="${X(BASE)}" x2="${X(BASE)}" y1="8" y2="195" stroke="${C.gray}" stroke-dasharray="3 5"/>`;
 r.options.forEach((a,i)=>{const y=26+i*36,col=!a.feasible?'#bdc5b9':(a.key===r.best.key?C.green:(a.value<BASE?C.red:C.blue));
 o+=`<text x="${L-9}" y="${y+4}" text-anchor="end" font-size="11" fill="${C.ink}">${a.name}</text>`;
 o+=`<line x1="${X(BASE)}" x2="${X(a.value)}" y1="${y}" y2="${y}" stroke="${col}" stroke-width="5" opacity="${a.feasible?1:.5}"/>`;
 o+=`<circle cx="${X(a.value)}" cy="${y}" r="${a.key===r.best.key?5.5:4}" fill="${col}"/><text x="${W-R+12}" y="${y+4}" font-size="10" fill="${col}">${a.feasible?pct(a.value):'B ≥ '+a.cost}</text>`;
 });return svg(W,H,o,'Sobrevivência por programa completo. Referência vertical: intervenção fixa sem diagnóstico.');
}
function heat(){
 const W=700,H=270,L=48,T=20,R=24,B=42,pw=W-L-R,ph=H-T-B,nx=41,ny=25;let o='';
 for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){
  const rho=(i+.5)/nx,bad=1-(j+.5)/ny,r=evaluate({...s,rho,bad,budget:100});
  const v=Math.max(-1,Math.min(1,r.gain/.035));const color=v<0?mix('#ede8da',C.red,-v):mix('#ede8da',C.green,v);
  o+=`<rect x="${L+i*pw/nx}" y="${T+j*ph/ny}" width="${pw/nx+.15}" height="${ph/ny+.15}" fill="${color}"><title>Apagamento ${clean(rho)}, seletor degradado ${clean(bad)}: ganho ${pp(r.gain)}</title></rect>`;
 }
 for(let i=0;i<=4;i++){const x=L+pw*i/4,y=T+ph*i/4;o+=`<text x="${x}" y="${H-24}" text-anchor="middle" font-size="10" fill="${C.gray}">${i*25}%</text><text x="${L-8}" y="${y+4}" text-anchor="end" font-size="10" fill="${C.gray}">${100-i*25}%</text>`;}
 o+=`<circle cx="${L+s.rho*pw}" cy="${T+(1-s.bad)*ph}" r="5" fill="none" stroke="white" stroke-width="2.5"/><text x="${L+pw/2}" y="${H-4}" text-anchor="middle" font-size="11" fill="${C.ink}">Probabilidade de apagar o diagnóstico por reparo</text><text transform="translate(11 ${T+ph/2}) rotate(-90)" text-anchor="middle" font-size="10" fill="${C.ink}">Seletor degradado: probabilidade</text>`;
 return svg(W,H,o,'Mapa do ganho diagnóstico versus apagamento e saúde latente do seletor.');
}
function curve(values,title,unit,color,zero=false){
 const W=700,H=182,L=48,T=21,R=24,B=35,pw=W-L-R,ph=H-T-B;
 let lo=zero?Math.min(0,...values):0,hi=Math.max(...values,zero?.1:1);if(hi-lo<.05)hi=lo+.05;
 const X=i=>L+i*pw/(values.length-1),Y=v=>T+(hi-v)/(hi-lo)*ph;
 let o=`<text x="${L}" y="12" font-size="10" fill="${C.ink}">${title}</text>`;
 for(let j=0;j<=3;j++){const v=lo+(hi-lo)*j/3,y=Y(v);o+=`<line x1="${L}" x2="${W-R}" y1="${y}" y2="${y}" stroke="${C.line}"/><text x="${L-7}" y="${y+3}" text-anchor="end" font-size="9" fill="${C.gray}">${clean(v)}</text>`;}
 if(zero)o+=`<line x1="${L}" x2="${W-R}" y1="${Y(0)}" y2="${Y(0)}" stroke="${C.red}" stroke-dasharray="4 4"/>`;
 o+=`<path d="${values.map((v,i)=>(i?'L':'M')+X(i)+','+Y(v)).join(' ')}" fill="none" stroke="${color}" stroke-width="2.5"/>`;
 for(let i=0;i<values.length;i++){o+=`<circle cx="${X(i)}" cy="${Y(values[i])}" r="2.5" fill="${color}"/><text x="${X(i)}" y="${H-17}" text-anchor="middle" font-size="9" fill="${C.gray}">${i+1}</text>`;}
 o+=`<text x="${W/2}" y="${H-2}" font-size="10" text-anchor="middle" fill="${C.gray}">Reparos entre diagnóstico e ação · ${unit}</text>`;
 return svg(W,H,o,title);
}
function render(){
 const r=optimize(s),raw=evaluate(s);
 document.getElementById('metrics').innerHTML=`<div class="metric"><small>Memória antes do seletor</small><strong>${raw.info.toFixed(3)} bit</strong></div><div class="metric"><small>Melhor sobrevivência</small><strong>${pct(r.best.value)}</strong></div><div class="metric"><small>Ganho sobre intervenção fixa</small><strong>${pp(r.best.value-(s.budget>=s.ticks?BASE:0))}</strong></div>`;
 document.getElementById('status').textContent='Programa escolhido: '+r.best.name+'. '+(r.best.key==='skip'?'O custo ou o risco do programa informado não se paga neste contrato.':'A regra usa apenas o bit físico e cabe no orçamento. Saúde oculta não é fornecida ao controlador.');
 document.getElementById('programs').innerHTML=programs(r);document.getElementById('heat').innerHTML=heat();
 const timeline=Array.from({length:10},(_,i)=>evaluate({...s,ticks:i+1,budget:100}));
 document.getElementById('delay').innerHTML=curve(timeline.map(x=>100*x.gain),'Ganho do diagnóstico, mesmo se negativo','pontos percentuais',C.green,true)+curve(timeline.map(x=>x.info),'Informação sobre saúde atual, antes da ação','bits',C.blue);
}
function sync(){for(const id of ids){document.getElementById(id).value=s[id];const o=document.getElementById('v-'+id);if(o)o.textContent=['budget','ticks'].includes(id)?s[id]:(100*s[id]).toFixed(id==='risk'?1:0)+'%';}}
for(const id of ids)document.getElementById(id).addEventListener('input',e=>{s[id]=id==='driver'?e.target.value:Number(e.target.value);sync();render();});
document.getElementById('reset').addEventListener('click',()=>{Object.assign(s,DEFAULT);sync();render();});
sync();render();
