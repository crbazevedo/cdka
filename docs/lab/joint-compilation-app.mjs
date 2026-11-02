import {DATA,channel,compile,funded,information,certifiedValue} from './joint-compilation-core.mjs';
const $=id=>document.getElementById(id);
const state={noise:.05,slots:3,budget:4,price:1,zoom:.5};
const green='#356b56',ochre='#ae794c',gray='#9da99d',ink='#253d31';
const pct=(x,d=4)=>(100*x).toFixed(d)+'%';
const word=x=>x.toString(2).padStart(2,'0');
const plan=x=>({50:'A',58:'B',42:'C'}[x]||String(x));
function svg(w,h,body,title){return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${title}" xmlns="http://www.w3.org/2000/svg"><title>${title}</title>${body}</svg>`;}
function graph(ans){
 const pos=[[350,65],[560,65],[350,235],[560,235]],used=new Set(ans.encoder);let s='';
 for(const [a,b] of [[0,1],[0,2],[1,3],[2,3]])s+=`<line x1="${pos[a][0]}" y1="${pos[a][1]}" x2="${pos[b][0]}" y2="${pos[b][1]}" stroke="#d7dfd1" stroke-width="2"/>`;
 if(ans.encoder[0]===ans.encoder[1]&&ans.encoder[2]!==ans.encoder[0]){
  const a=pos[ans.encoder[0]],b=pos[ans.encoder[2]];s+=`<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="${ochre}" stroke-dasharray="5 6" stroke-width="1.5"/>`;
 }
 const names=['Diagnóstico baixo','Diagnóstico médio','Diagnóstico alto'];
 for(let y=0;y<3;y++){
  const py=60+90*y,p=pos[ans.encoder[y]];
  s+=`<text x="12" y="${py}" font-size="13" fill="${ink}">${names[y]}</text><text x="12" y="${py+17}" font-size="10" fill="#7a8a7c">Y=${y} · mesmo sensor da v9</text>`;
  const edge=p[0]>500?`M155 ${py} C220 ${py} 210 145 290 145 C430 145 495 145 ${p[0]-25} ${p[1]}`:`M155 ${py} C220 ${py} 250 ${p[1]} ${p[0]-25} ${p[1]}`;
  s+=`<path d="${edge}" stroke="${y===2?ochre:green}" fill="none" stroke-width="${y===2?2.2:1.5}" opacity=".8"/>`;
 }
 for(let r=0;r<4;r++){
  const [x,y]=pos[r];s+=`<circle cx="${x}" cy="${y}" r="24" fill="${used.has(r)?green:'#e9ede2'}" stroke="#cfdbcc"/><text x="${x}" y="${y+5}" text-anchor="middle" font-size="14" fill="${used.has(r)?'#fff':ink}">${word(r)}</text><text x="${x}" y="${y+43}" text-anchor="middle" font-size="11" fill="${ink}">recebido → plano ${plan(ans.decoder[r])}</text>`;
 }
 s+='<text x="455" y="16" text-anchor="middle" font-size="10" fill="#7a8a7c">QUATRO ESTADOS FÍSICOS · DOIS BITS</text>';
 return svg(650,302,s,'Codificação dos três diagnósticos em dois bits físicos');
}
function curve(){
 const W=690,H=270,L=61,R=15,T=22,B=44,pw=W-L-R,ph=H-T-B;
 const ymin=.8085,ymax=.8213,xmax=state.zoom;
 const X=p=>L+p/xmax*pw,Y=v=>T+(ymax-v)/(ymax-ymin)*ph;
 let s='';
 for(let i=0;i<=4;i++){
  const y=ymin+(ymax-ymin)*i/4,x=xmax*i/4;
  s+=`<line x1="${L}" y1="${Y(y)}" x2="${W-R}" y2="${Y(y)}" stroke="#e2e6da"/><text x="${L-8}" y="${Y(y)+3}" text-anchor="end" font-size="10" fill="#7a8a7c">${pct(y,2)}</text><text x="${X(x)}" y="${H-B+19}" text-anchor="middle" font-size="10" fill="#7a8a7c">${pct(x,2)}</text>`;
 }
 const pts=[[],[],[]];
 for(let i=0;i<=85;i++){
  const p=xmax*i/85;
  pts[0].push([p,compile(p,state.slots).value]);pts[1].push([p,compile(p,state.slots,4,true).value]);pts[2].push([p,DATA.phase[2][0]]);
 }
 [green,ochre,gray].forEach((c,j)=>{
  const d=pts[j].map(([x,y],i)=>`${i?'L':'M'}${X(x).toFixed(2)},${Y(y).toFixed(2)}`).join(' ');
  s+=`<path d="${d}" fill="none" stroke="${c}" stroke-width="${j===0?2.8:1.8}" ${j?'stroke-dasharray="5 5"':''}/>`;
 });
 if(state.slots===3)for(const p of DATA.thresholds)if(p<=xmax){
  s+=`<line x1="${X(p)}" y1="${T}" x2="${X(p)}" y2="${H-B}" stroke="#b8c5b2" stroke-dasharray="3 4"/><text x="${Math.max(87,X(p)+4)}" y="16" font-size="9" fill="#697f68">${pct(p,3)}</text>`;
 }
 if(state.noise<=xmax){
  const v=compile(state.noise,state.slots).value;s+=`<circle cx="${X(state.noise)}" cy="${Y(v)}" r="4.5" fill="${green}" stroke="#fff" stroke-width="2"/>`;
 }
 s+=`<text x="${L+pw/2}" y="${H-3}" text-anchor="middle" font-size="10" fill="#697f68">Probabilidade de inversão por bit p</text>`;
 return svg(W,H,s,'Sobrevivência média por erro de transporte; curvas conjuntas e injetivas');
}
function render(){
 const a=compile(state.noise,state.slots),inj=compile(state.noise,state.slots,4,true);
 $('metrics').innerHTML=`<div><span>Sobrevivência média</span><strong>${pct(a.value,3)}</strong></div><div><span>Classes codificadas</span><strong>${a.states} / 3</strong></div><div><span>Planos utilizados</span><strong>${a.templates} / ${state.slots}</strong></div>`;
 $('graph').innerHTML=graph(a);$('curves').innerHTML=curve();
 $('information').innerHTML=`<table class="mini-table"><thead><tr><th>Projeto</th><th>I(Y;registro)</th><th>Sobrevivência</th></tr></thead><tbody><tr class="best"><td>Síntese conjunta</td><td>${information(a.encoder,state.noise).toFixed(5)} bit</td><td>${pct(a.value,4)}</td></tr><tr><td>Melhor injetivo</td><td>${information(inj.encoder,state.noise).toFixed(5)} bit</td><td>${pct(inj.value,4)}</td></tr></tbody></table>`;
 let phase=state.noise<DATA.thresholds[0]?'Preservar as três distinções é ótimo.':state.noise<DATA.thresholds[1]?'A melhor síntese funde dois diagnósticos e separa as classes em palavras opostas.':'A tabela ótima utiliza um único plano; o diagnóstico não muda a decisão.';
 if(state.slots<3)phase='Biblioteca limitada a '+state.slots+' plano(s). Os limiares globais de três planos não se aplicam automaticamente a esta restrição.';
 $('phase').textContent=phase+' Certificado contínuo: modelo físico fixo da v9, b=4, sem preço adicional de slots. '+(state.noise>state.zoom?'O ponto escolhido está fora da escala de ruído exibida.':'');
 const paid=funded(state.noise,state.budget,state.price);
 $('funded').innerHTML=`<table class="mini-table"><thead><tr><th>Slots</th><th>Instalação</th><th>Recurso restante</th><th>Sobrevivência</th></tr></thead><tbody>${paid.options.map(o=>`<tr class="${o.slots===paid.best.slots?'best':''}"><td>${o.slots}</td><td>${o.fee}</td><td>${o.balance}</td><td>${pct(o.value,4)}</td></tr>`).join('')}</tbody></table>`;
 $('o-noise').textContent=pct(state.noise,3);$('o-slots').textContent=state.slots;$('o-budget').textContent=state.budget;$('o-price').textContent=state.price;
}
for(const key of ['noise','slots','budget','price'])$(key).addEventListener('input',e=>{state[key]=Number(e.target.value);render();});
for(const b of document.querySelectorAll('[data-zoom]'))b.addEventListener('click',()=>{state.zoom=Number(b.dataset.zoom);render();});
$('reset').addEventListener('click',()=>{Object.assign(state,{noise:.05,slots:3,budget:4,price:1,zoom:.5});for(const k of ['noise','slots','budget','price'])$(k).value=state[k];render();});
render();
