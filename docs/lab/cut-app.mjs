import {h2,cutModel,horizonSeries,informationTimeline} from './cut-core.mjs';

const variables=['cycles','budget','eta','rho','nu','target','sideChannel'];
const state={cycles:2,budget:2,eta:0,rho:1,nu:0,target:.9,sideChannel:false};
const colors={moss:'#356b56',pale:'#e0eddf',ochre:'#b87d48',rust:'#a95c4e',
  paper:'#fffdf8',line:'#e1e7dc',text:'#566c60',ink:'#24372f',blue:'#567c95'};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=(v,d=2)=>Number(v).toFixed(d).replace(/\.?0+$/,'');
const pct=v=>(v*100).toFixed(1).replace(/\.0$/,'')+'%';
const xy=(n,b)=>cutModel({cycles:n,budget:b,eta:state.eta,rho:state.rho,nu:state.nu,sideChannel:state.sideChannel});
function mix(a,b,t){
  const A=[1,3,5].map(i=>parseInt(a.slice(i,i+2),16)),B=[1,3,5].map(i=>parseInt(b.slice(i,i+2),16));
  return 'rgb('+A.map((x,i)=>Math.round(x*(1-t)+B[i]*t)).join(',')+')';
}
function heatmap(){
  const W=730,H=305,L=70,T=37,cw=35,ch=28;
  let out='<rect width="'+W+'" height="'+H+'" fill="#fffdf8"/>';
  out+='<text x="70" y="16" font-size="11" fill="'+colors.text+'">ORÇAMENTO FÍSICO B →</text>';
  for(let b=0;b<=16;b++)out+='<text x="'+(L+b*cw+cw/2)+'" y="'+(T-10)+'" text-anchor="middle" font-size="10" fill="'+colors.text+'">'+b+'</text>';
  for(let n=1;n<=8;n++){
    const py=T+(n-1)*ch;
    out+='<text x="'+(L-11)+'" y="'+(py+18)+'" font-size="11" text-anchor="end" fill="'+colors.text+'">'+n+'</text>';
    for(let b=0;b<=16;b++){
      const r=xy(n,b),pass=r.ready&&r.success+1e-12>=state.target;
      const color=!r.ready?'#edcebf':mix('#ede1c9','#3b795e',Math.min(1,Math.max(0,2*(r.success-.5))));
      const selected=n===state.cycles&&b===state.budget;
      const px=L+b*cw+2;
      out+='<rect data-cell-n="'+n+'" data-cell-b="'+b+'" x="'+px+'" y="'+py+'" rx="3" width="'+(cw-3)+'" height="'+(ch-3)+'" fill="'+color+'" stroke="'+(selected?colors.ink:(pass?'#6f9475':'none'))+'" stroke-width="'+(selected?2.5:0.6)+'" tabindex="0" role="button" aria-label="'+esc('n='+n+', B='+b+', sobrevivência '+pct(r.success))+'">'+
      '<title>'+esc('n='+n+' · B='+b+' · P(sucesso)='+pct(r.success)+(r.ready?'':' · atuador indisponível'))+'</title></rect>';
      if(selected)out+='<circle cx="'+(px+(cw-3)/2)+'" cy="'+(py+(ch-3)/2)+'" r="3" fill="#ffffff"/>';
    }
  }
  out+='<text x="23" y="157" text-anchor="middle" transform="rotate(-90 23 157)" font-size="10" fill="'+colors.text+'">REPAROS n</text>';
  out+='<text x="70" y="'+(H-18)+'" font-size="10" fill="'+colors.text+'">Cada célula mostra a melhor política pré-programada, sem sinais paralelos ocultos.</text>';
  return '<svg class="cut-viz cut-svg" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Mapa de viabilidade por reparos e orçamento. Clique numa célula para selecionar." xmlns="http://www.w3.org/2000/svg">'+out+'</svg>';
}
function lineChart(series,{height=260,lo=0,hi=1,xLabel='reparos obrigatórios',yLabel='probabilidade',current=state.cycles,target=state.target}={}){
  const W=730,H=height,L=53,R=17,T=18,B=43,pw=W-L-R,ph=H-T-B;
  const X=x=>L+(x/8)*pw;
  const Y=y=>T+(hi-y)/(hi-lo)*ph;
  let out='<rect x="'+L+'" y="'+T+'" width="'+pw+'" height="'+ph+'" fill="#fffdf8"/>';
  for(let j=0;j<=5;j++){
    const y=lo+(hi-lo)*j/5;
    out+='<line x1="'+L+'" y1="'+Y(y)+'" x2="'+(W-R)+'" y2="'+Y(y)+'" stroke="'+colors.line+'" />'+
    '<text x="'+(L-10)+'" y="'+(Y(y)+3)+'" text-anchor="end" font-size="10" fill="'+colors.text+'">'+fmt(y,2)+'</text>';
  }
  for(let n=1;n<=8;n++){
    const x=X(n);
    out+='<line x1="'+x+'" y1="'+T+'" x2="'+x+'" y2="'+(H-B)+'" stroke="'+colors.line+'" />'+
    '<text x="'+x+'" y="'+(H-B+17)+'" text-anchor="middle" font-size="10" fill="'+colors.text+'">'+n+'</text>';
  }
  if(target!==null){
    out+='<line x1="'+L+'" y1="'+Y(target)+'" x2="'+(W-R)+'" y2="'+Y(target)+'" stroke="'+colors.rust+'" stroke-dasharray="6 6" stroke-width="1.5"/>';
  }
  for(const item of series){
    const pts=item.values.map((value,i)=>[i+1,value]);
    const d=pts.map(([x,y],i)=>(i?'L':'M')+X(x).toFixed(2)+' '+Y(y).toFixed(2)).join(' ');
    out+='<path d="'+d+'" fill="none" stroke="'+item.color+'" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" '+(item.dashed?'stroke-dasharray="6 5"':'')+'/>';
    for(const [x,y] of pts)out+='<circle cx="'+X(x)+'" cy="'+Y(y)+'" r="'+(x===current?4.5:2.5)+'" fill="'+item.color+'" stroke="#fff" stroke-width="1.5"/>';
  }
  out+='<text x="'+(L+pw/2)+'" y="'+(H-2)+'" font-size="11" text-anchor="middle" fill="'+colors.text+'">'+esc(xLabel)+'</text>'+
  '<text transform="translate(12 '+(T+ph/2)+') rotate(-90)" text-anchor="middle" font-size="11" fill="'+colors.text+'">'+esc(yLabel)+'</text>';
  return '<svg class="cut-viz cut-svg" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Curvas de viabilidade por horizonte" xmlns="http://www.w3.org/2000/svg">'+out+'</svg>';
}
function legend(items){return '<div class="cut-key">'+items.map(([name,color])=>'<span><i style="background:'+color+'"></i>'+esc(name)+'</span>').join('')+'</div>';}
function stats(){
  const r=cutModel(state);
  const isPass=r.ready&&r.success+1e-12>=state.target;
  const warning=!r.ready?'O orçamento não restaura todos os atuadores: o controle físico é impossível.' :
    isPass?'O controlador satisfaz a meta dentro das hipóteses deste modelo.':
    'Os recursos marginais existem, mas a informação disponível na decisão não assegura a meta.';
  return '<div class="cut-info">'+
    '<div class="cut-stat"><span>Informação inicial</span><strong>'+fmt(r.initialInfo,3)+' bit</strong></div>'+
    '<div class="cut-stat"><span>Informação na decisão</span><strong>'+fmt(r.finalInfo,3)+' bit</strong></div>'+
    '<div class="cut-stat"><span>Melhor sobrevivência</span><strong class="'+(isPass?'':'danger')+'">'+pct(r.success)+'</strong></div>'+
    '</div><div class="cut-warning '+(isPass?'ready':'')+'">'+esc(warning)+
    ' <strong>'+r.protections+'/'+state.cycles+'</strong> reparos protegidos.</div>';
}
function flow(){
  const r=cutModel(state);
  return '<div class="cut-path">'+
    '<div class="cut-node"><b>Percepção inicial</b><span>'+fmt(r.initialInfo,3)+' bit disponível</span></div>'+
    '<div class="cut-arrow">→</div>'+
    '<div class="cut-node"><b>Reparo × '+state.cycles+'</b><span>'+r.unprotected+' passagem(ns) sem proteção</span></div>'+
    '<div class="cut-arrow">→</div>'+
    '<div class="cut-node"><b>Corte físico C</b><span>'+fmt(r.finalInfo,3)+' bit até o atuador</span></div>'+
    '</div><div class="cut-data">Distinguibilidade final em variação total: '+fmt(r.tv,4)+' · Correlação pós-reparo: '+fmt(r.correlation,4)+'</div>'+
    '<div class="cut-meter" aria-hidden="true"><i style="width:'+(100*r.tv)+'%"></i></div>';
}
function render(){
  const r=cutModel(state);
  const base={...state,sideChannel:false},through={...state,sideChannel:true};
  const vals1=horizonSeries(base,8).map(x=>x.success);
  const vals2=horizonSeries(through,8).map(x=>x.success);
  const timeline=informationTimeline(state);
  const after=timeline.map(x=>x.information);
  const center='<div class="cut-chart-title">Viabilidade exata · orçamento × horizonte</div>'+heatmap()+
    legend([['Atuador indisponível','#edcebf'],['Sobrevivência próxima de 50%','#ede1c9'],['Sobrevivência próxima de 100%','#3b795e']])+
    '<div class="cut-section"><div class="cut-chart-title">Quando a capacidade de decidir se perde</div>'+flow()+'</div>'+
    '<div class="cut-section"><div class="cut-chart-title">Sobrevivência por horizonte, mantendo B='+state.budget+' fixo</div>'+
    lineChart([{values:vals1,color:colors.moss},{values:vals2,color:colors.blue,dashed:true}])+
    legend([['Sem canal paralelo',colors.moss],['Com canal físico Z',colors.blue],['Meta',colors.rust]])+
    '</div><div class="cut-section"><div class="cut-chart-title">Informação fisicamente disponível após cada reparo</div>'+
    '<div class="cut-data">Sensor inicial: '+fmt(r.initialInfo,3)+' bit · Memória final: '+fmt(r.finalInfo,3)+' bit</div>'+
    '<div class="cut-timeline">'+timeline.map((p,i)=>'<div class="cut-timeline-row"><span>'+i+'</span><div class="cut-meter"><i style="width:'+(100*p.information)+'%"></i></div><strong>'+fmt(p.information,3)+'</strong></div>').join('')+'</div>'+
    '</div>';
  document.getElementById('cut-viz').innerHTML=stats()+center+
    '<p class="cut-math">Corte completo: P*(U=W) = [1+TV(P(C|W=0),P(C|W=1))]/2. A fórmula do orçamento exige proteção pré-programada, sem codificação de W nas escolhas de reparo.</p>';
}
function syncControls(){
 for(const k of variables){
  const el=document.getElementById(k);
  if(k==='sideChannel')el.checked=state[k];
  else el.value=state[k];
  const out=document.getElementById('o-'+k);
  if(out)out.textContent=['eta','rho','nu','target'].includes(k)?pct(state[k]):state[k];
 }
}
for(const id of variables){
  document.getElementById(id).addEventListener('input',e=>{
    state[id]=id==='sideChannel'?e.target.checked:Number(e.target.value);
    syncControls();render();
  });
}
document.querySelectorAll('[data-preset]').forEach(btn=>btn.addEventListener('click',()=>{
 const preset=btn.dataset.preset;
 if(preset==='hard')Object.assign(state,{cycles:2,budget:2,eta:0,rho:1,nu:0,target:.9,sideChannel:false});
 if(preset==='soft')Object.assign(state,{cycles:3,budget:4,eta:0,rho:.5,nu:0,target:.8,sideChannel:false});
 if(preset==='drift')Object.assign(state,{cycles:3,budget:6,eta:0,rho:.4,nu:.2,target:.9,sideChannel:false});
 if(preset==='bypass')Object.assign(state,{cycles:2,budget:2,eta:0,rho:1,nu:0,target:.9,sideChannel:true});
 syncControls();render();
}));
document.getElementById('cut-viz').addEventListener('click',ev=>{
 const cell=ev.target.closest('[data-cell-n][data-cell-b]');
 if(!cell)return;
 state.cycles=Number(cell.dataset.cellN);state.budget=Number(cell.dataset.cellB);
 syncControls();render();
});
document.getElementById('cut-viz').addEventListener('keydown',ev=>{
 const cell=ev.target.closest('[data-cell-n][data-cell-b]');
 if(cell && (ev.key==='Enter'||ev.key===' ')){
  ev.preventDefault();
  state.cycles=Number(cell.dataset.cellN);state.budget=Number(cell.dataset.cellB);
  syncControls();render();
 }
});
syncControls();render();
