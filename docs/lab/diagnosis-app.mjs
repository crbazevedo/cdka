import {evaluate,errorAfter,threshold,PAYOFF} from './diagnosis-core.mjs';
const state={k:0,B:4,eta:0,nu:0,age:1,inspectionFailure:0,d:1,c:1,prior:.5};
const ids=['k','B','eta','nu','age','inspectionFailure','d','c'];
const Q=(id)=>document.getElementById(id);
const fmt=(v,d=3)=>Number(v).toFixed(d);
const pct=(v,d=1)=>(100*v).toFixed(d)+'%';
const style={green:'#477e5e',ochre:'#ba9461',rust:'#b76d58',ink:'#254536',muted:'#809181'};
function rgb(h){return [1,3,5].map(i=>parseInt(h.slice(i,i+2),16));}
function blend(a,b,t){const A=rgb(a),B=rgb(b);const v=Math.min(1,Math.max(0,t));return `rgb(${A.map((x,i)=>Math.round(x*(1-v)+B[i]*v)).join(',')})`;}
function el(inner,W=680,H=260,label='Gráfico científico CDKA'){
 return `<svg class="graphic" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label.replaceAll('"','&quot;')}" xmlns="http://www.w3.org/2000/svg">${inner}</svg>`;
}
function renderMetrics(r){
 const data=[['Sobrevivência ótima',pct(r.actual,2),r.inspect?'com diagnóstico':'sem diagnóstico'],
  ['Ganho da informação',`+${pct(r.gain,2)}`,r.gain>1e-10?'efeito positivo':'nenhum ganho'],
  ['Erro efetivo',pct(r.healthError,1),r.affordable?'ação atualizável':'atuação limitada']];
 Q('metrics').innerHTML=data.map(([label,note,sub],i)=>`<div class="metric"><small>${label}</small><strong class="${i===1&&r.gain<1e-10?'negative':''}">${note}</strong><span>${sub}</span></div>`).join('');
}
function heatmap(){
 const W=680,H=250,L=63,R=17,T=24,B=46,n=50,m=5,pw=W-L-R,ph=H-T-B;
 let a=`<rect x="${L}" y="${T}" width="${pw}" height="${ph}" fill="#f7f8f2"/>`;
 for(let b=0;b<m;b++)for(let j=0;j<n;j++){
  const eta=(j+.5)*.5/n;
  const r=evaluate({...state,B:b,eta});
  const x=L+j*pw/n,y=T+(m-b-1)*ph/m;
  const color=blend('#eeece4',style.green,r.gain/.028);
  a+=`<rect x="${x}" y="${y}" width="${pw/n+.2}" height="${ph/m+.2}" fill="${color}" data-b="${b}" data-eta="${eta.toFixed(3)}" role="button" tabindex="0"><title>B=${b}; erro=${pct(eta)}; ganho=${pct(r.gain,2)}</title></rect>`;
 }
 for(let b=0;b<m;b++){
  const y=T+(m-b-.5)*ph/m+4;
  a+=`<text class="svglabel" x="${L-10}" y="${y}" text-anchor="end">${b}</text>`;
 }
 for(let j=0;j<=5;j++){
  const x=L+pw*j/5;
  a+=`<text class="svglabel" x="${x}" y="${T+ph+20}" text-anchor="middle">${(10*j).toFixed(0)}%</text>`;
 }
 const selectedX=L+pw*state.eta/.5;
 const selectedY=T+(m-state.B-.5)*ph/m;
 a+=`<circle cx="${selectedX}" cy="${selectedY}" r="6" fill="#b66d58" stroke="white" stroke-width="2.5" pointer-events="none"/>`;
 a+=`<text class="svglabel" x="${L+pw/2}" y="${H-3}" text-anchor="middle">Erro de diagnóstico η</text>`;
 a+=`<text class="svglabel" transform="translate(15 ${T+ph/2}) rotate(-90)" text-anchor="middle">Orçamento B</text>`;
 Q('heatmap').innerHTML=el(a,W,H,'Mapa interativo do ganho do diagnóstico por orçamento e erro');
}
function linesChart(series,{W=680,H=260,xmax=1,ymin=0,ymax=1,xlabel='',ylabel='',mark=null}={}){
 const L=55,R=15,T=21,B=44,pw=W-L-R,ph=H-T-B;
 const X=x=>L+pw*x/xmax,Y=y=>T+ph-(y-ymin)/(ymax-ymin||1)*ph;
 let out=`<rect x="${L}" y="${T}" width="${pw}" height="${ph}" fill="#fffdf8"/>`;
 for(let k=0;k<=4;k++){
  const x=L+pw*k/4,y=T+ph*k/4;
  out+=`<line class="svggrid" x1="${L}" y1="${y}" x2="${L+pw}" y2="${y}"/>`;
  out+=`<line class="svggrid" x1="${x}" y1="${T}" x2="${x}" y2="${T+ph}"/>`;
  out+=`<text class="svglabel" x="${L-9}" y="${y+3}" text-anchor="end">${fmt(ymax-(ymax-ymin)*k/4,2)}</text>`;
  out+=`<text class="svglabel" x="${x}" y="${T+ph+20}" text-anchor="middle">${fmt(xmax*k/4,2)}</text>`;
 }
 if(mark!==null){const x=X(mark);out+=`<line x1="${x}" y1="${T}" x2="${x}" y2="${T+ph}" stroke="${style.rust}" stroke-width="1.5" stroke-dasharray="4 5"/>`;}
 for(const s of series){
  const points=s.points.filter(([x,y])=>Number.isFinite(x)&&Number.isFinite(y));
  const path=points.map(([x,y],i)=>(i?'L':'M')+X(x).toFixed(2)+' '+Y(Math.max(ymin,Math.min(ymax,y))).toFixed(2)).join(' ');
  out+=`<path d="${path}" class="svgline" stroke="${s.color}" ${s.dash?'stroke-dasharray="5 4"':''}/>`;
 }
 out+=`<text class="svglabel" x="${L+pw/2}" y="${H-3}" text-anchor="middle">${xlabel}</text>`;
 out+=`<text class="svglabel" transform="translate(13 ${T+ph/2}) rotate(-90)" text-anchor="middle">${ylabel}</text>`;
 return el(out,W,H,`Gráfico ${ylabel} por ${xlabel}`);
}
function lineLegend(items){return `<div class="legend">${items.map(([label,color])=>`<span><i class="swatch" style="background:${color}"></i> ${label}</span>`).join('')}</div>`;}
function valueChart(){
 const a=[],b=[],o=[];
 for(let j=0;j<=50;j++){
  const eta=j/100,r=evaluate({...state,eta});
  a.push([eta,r.actual]);b.push([eta,r.baseline.value]);o.push([eta,r.oracle]);
 }
 const ymin=Math.min(...b.map(x=>x[1]))-.02,ymax=Math.min(1,Math.max(...o.map(x=>x[1]))+.02);
 Q('valuechart').innerHTML=linesChart([
  {points:a,color:style.green},{points:b,color:style.ochre,dash:true},{points:o,color:'#a5b5a6',dash:true}],
  {xmax:.5,ymin,ymax,xlabel:'Erro de diagnóstico η',ylabel:'P(sobreviver)',mark:state.eta})+
 lineLegend([['melhor política física',style.green],['sem diagnóstico',style.ochre],['saúde revelada gratuitamente','#a5b5a6']]);
}
function ageChart(){
 const ages=Array.from({length:9},(_,age)=>[age,evaluate({...state,age}).gain]);
 const ymax=Math.max(.002,Math.max(...ages.map(x=>x[1]))*1.3);
 Q('agechart').innerHTML=linesChart([{points:ages,color:style.green}],
 {xmax:8,ymin:0,ymax,xlabel:'Intervalos desde a leitura',ylabel:'Ganho de sobrevivência',mark:state.age})+
 `<p class="svgcaption">Referência: com ν=${pct(state.nu)}, a correlação entre leitura e saúde atual decai como (1−2ν)^t.</p>`;
}
function benchmark(){
 const bench=[
  [1,.883319376,.908929941292],[2,.8091779607700227,.8513094381825589],[3,.738694271129677,.8008554458043696]
 ];
 Q('bench').innerHTML=`<div class="benchbars">${bench.map(([n,hidden,oracle])=>`<div class="benchrow"><span>${n} época${n>1?'s':''}</span><div><div class="bartrack"><i class="barfill" style="width:${hidden*100}%"></i></div><div class="bartrack" style="margin-top:3px;height:7px"><i class="barfill oracle" style="width:${oracle*100}%"></i></div></div><strong>${pct(hidden)}</strong></div>`).join('')}</div><div class="legend"><span><i class="swatch hi"></i> política sem saúde observável</span><span><i class="swatch" style="background:#b5ab88"></i> limite com saúde visível</span></div>`;
}
function render(){for(const id of ids){Q('v-'+id).textContent=['eta','nu','inspectionFailure'].includes(id)?pct(state[id],state[id]<.01?1:0):state[id];}
 const r=evaluate(state);renderMetrics(r);heatmap();valueChart();ageChart();benchmark();}
function assign(s){Object.assign(state,s);for(const id of ids)Q(id).value=state[id];render();}
for(const id of ids)Q(id).addEventListener('input',e=>{state[id]=Number(e.target.value);render();});
const presets={clear:{B:4,eta:0,nu:0,age:1,inspectionFailure:0,d:1,c:1,k:0},
 budget:{B:3,eta:0,nu:0,age:1,inspectionFailure:0,d:1,c:1,k:0},
 stale:{B:4,eta:.05,nu:.1,age:3,inspectionFailure:0,d:1,c:1,k:0},
 procedure:{B:4,eta:0,nu:0,age:1,inspectionFailure:.05,d:1,c:1,k:0}};
for(const button of document.querySelectorAll('[data-preset]'))button.addEventListener('click',()=>assign(presets[button.dataset.preset]));
Q('heatmap').addEventListener('click',e=>{const r=e.target.closest('[data-eta][data-b]');if(!r)return;assign({B:+r.dataset.b,eta:+r.dataset.eta});});
Q('heatmap').addEventListener('keydown',e=>{if(e.key!=='Enter'&&e.key!==' ')return;const r=e.target.closest('[data-eta][data-b]');if(!r)return;e.preventDefault();assign({B:+r.dataset.b,eta:+r.dataset.eta});});
render();
