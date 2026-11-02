import {channelGeometry,renewal,tolerance} from './policy-cuts-core.mjs';
const state={probabilities:[0,1,0,1],noise:.1,cycles:10,alpha:.1,seed:false};
const C={ink:'#253d32',green:'#3b7459',pale:'#e5eddf',gold:'#b7814e',rust:'#ad6053',blue:'#5e7e96',muted:'#718477',line:'#dce1d6'};
const fmt=(x,d=2)=>Number.isFinite(x)?Number(x.toFixed(d)).toString().replace('.',','):'∞';
const pct=x=>x>0&&x<.0001?'<0,01%':fmt(100*x,2)+'%';
const txt=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const stat=(label,value,sub='')=>'<div class="stat"><span>'+txt(label)+'</span><b>'+txt(value)+'</b><small>'+txt(sub)+'</small></div>';
const legend=items=>'<div class="legend">'+items.map(([l,c])=>'<span><i style="background:'+c+'"></i>'+txt(l)+'</span>').join('')+'</div>';
function chartFrame(w,h,inner,label){return '<svg class="chart" viewBox="0 0 '+w+' '+h+'" role="img" aria-label="'+txt(label)+'" xmlns="http://www.w3.org/2000/svg">'+inner+'</svg>';}
function width(id){const node=document.getElementById(id);return Math.max(260,Math.min(760,(node.clientWidth||690)-46));}
function squareAxes(w,h,xTitle,yTitle){
 const L=43,R=17,T=21,B=42,pw=w-L-R,ph=h-T-B;
 const X=x=>L+x*pw,Y=y=>T+(1-y)*ph;
 let svg='';
 for(let i=0;i<=4;i++){
  const q=i/4;
  svg+='<line x1="'+X(q)+'" y1="'+T+'" x2="'+X(q)+'" y2="'+Y(0)+'" stroke="'+C.line+'"/>';
  svg+='<line x1="'+L+'" y1="'+Y(q)+'" x2="'+X(1)+'" y2="'+Y(q)+'" stroke="'+C.line+'"/>';
  svg+='<text x="'+X(q)+'" y="'+(Y(0)+17)+'" text-anchor="middle" fill="'+C.muted+'" font-size="10">'+fmt(q)+'</text>';
  svg+='<text x="'+(L-7)+'" y="'+(Y(q)+3)+'" text-anchor="end" fill="'+C.muted+'" font-size="10">'+fmt(q)+'</text>';
 }
 svg+='<text x="'+X(.5)+'" y="'+(h-4)+'" text-anchor="middle" font-size="10" fill="'+C.muted+'">'+txt(xTitle)+'</text>';
 svg+='<text transform="translate(12 '+Y(.5)+') rotate(-90)" text-anchor="middle" font-size="10" fill="'+C.muted+'">'+txt(yTitle)+'</text>';
 return {svg,X,Y,L,R,T,B};
}
function channelFigure(g){
 const w=width('channel-viz'),h=Math.min(390,Math.max(280,w*.66));
 const A=squareAxes(w,h,'P(registro novo=1 | entrada 0)','P(registro novo=1 | entrada 1)');
 let out=A.svg;
 out+='<rect x="'+A.X(g.xRange[0])+'" y="'+A.Y(g.yRange[1])+'" width="'+((g.xRange[1]-g.xRange[0])*(A.X(1)-A.X(0)))+'" height="'+((g.yRange[1]-g.yRange[0])*(A.Y(0)-A.Y(1)))+'" fill="'+C.pale+'" fill-opacity=".72" stroke="'+C.green+'" stroke-width="1.4"/>';
 out+='<path d="M'+A.X(0)+' '+A.Y(0)+' L'+A.X(1)+' '+A.Y(1)+'" stroke="'+C.muted+'" stroke-width="1.5" stroke-dasharray="5 5"/>';
 g.pairs.forEach(([x,y],i)=>{
  out+='<circle cx="'+A.X(x)+'" cy="'+A.Y(y)+'" r="'+(i===g.winner?7:5)+'" fill="'+(i===g.winner?C.green:C.gold)+'" stroke="#fff" stroke-width="1.7"><title>política '+i+' · diferença '+fmt(Math.abs(x-y),3)+'</title></circle>';
 });
 const [bx,by]=g.pairs[g.winner];
 out+='<circle cx="'+A.X(bx)+'" cy="'+A.Y(by)+'" r="11" fill="none" stroke="'+C.ink+'" stroke-width="1.4"/>';
 return chartFrame(w,h,out,'Retângulo de pares de linhas alcançáveis e políticas extremas');
}
function renderChannel(){
 const g=channelGeometry(state.probabilities);
 document.getElementById('channel-viz').innerHTML='<div class="stats">'+
 stat('Modo fixo 0',fmt(g.fixed[0],3),'coeficiente de contração')+
 stat('Modo fixo 1',fmt(g.fixed[1],3),'coeficiente de contração')+
 stat('Melhor feedback',fmt(g.envelope,3),'ações podem diferir por entrada')+'</div><div class="plot-label">Geometria exata das linhas alcançáveis</div>'+channelFigure(g)+legend([['políticas extremas',C.gold],['melhor feedback',C.green],['sinal indistinguível',C.muted]])+
 '<div class="note">Com entradas equiprováveis e perfeitamente informadas, este canal permite decodificação correta de até <b>'+pct(g.success)+'</b>. Isso não inclui risco de falha física nem restrições posteriores.</div>';
}
function survivalFigure(n,p,seed){
 const w=width('renewal-viz'),h=Math.max(260,Math.min(340,w*.53));
 const L=43,R=18,T=20,B=42,pw=w-L-R,ph=h-T-B;
 const H=Math.min(50,Math.max(15,n+5));const X=x=>L+(x-1)/(H-1)*pw,Y=y=>T+(1-y)*ph;
 let svg='';
 for(let i=0;i<=4;i++){
  const q=i/4,x=1+(H-1)*i/4;
  svg+='<line x1="'+L+'" y1="'+Y(q)+'" x2="'+X(H)+'" y2="'+Y(q)+'" stroke="'+C.line+'"/>';
  svg+='<text x="'+(L-8)+'" y="'+(Y(q)+4)+'" text-anchor="end" fill="'+C.muted+'" font-size="10">'+fmt(q)+'</text>';
  svg+='<text x="'+X(x)+'" y="'+(Y(0)+17)+'" text-anchor="middle" fill="'+C.muted+'" font-size="10">'+fmt(x,0)+'</text>';
 }
 const nc=p===0?Infinity:Math.log(.5)/Math.log1p(-p);
 if(nc>1&&nc<H)svg+='<line x1="'+X(nc)+'" y1="'+T+'" x2="'+X(nc)+'" y2="'+Y(0)+'" stroke="'+C.gold+'" stroke-dasharray="4 5"/>';
 function line(fn,color,dash=''){
  const pts=Array.from({length:161},(_,i)=>1+(H-1)*i/160);
  return '<path d="'+pts.map((x,i)=>(i?'L':'M')+X(x).toFixed(2)+' '+Y(fn(x)).toFixed(2)).join(' ')+'" fill="none" stroke="'+color+'" stroke-width="2.7" '+(dash?'stroke-dasharray="'+dash+'"':'')+'/>';
 }
 svg+=line(x=>(1-p)**x,C.green);
 svg+=line(x=>Math.max(.5,(1-p)**x),C.gold,'6 4');
 if(seed)svg+=line(x=>Math.max(.5,(1-p)**x),C.blue,'2 5');
 const val=(1-p)**n;
 svg+='<line x1="'+X(n)+'" y1="'+T+'" x2="'+X(n)+'" y2="'+Y(0)+'" stroke="'+C.muted+'" stroke-dasharray="2 5"/>';
 svg+='<circle cx="'+X(n)+'" cy="'+Y(val)+'" r="5" fill="'+C.green+'" stroke="#fff" stroke-width="1.5"/>';
 svg+='<text x="'+(L+pw/2)+'" y="'+(h-4)+'" text-anchor="middle" font-size="10" fill="'+C.muted+'">ciclos de reparo e atuação</text>';
 svg+='<text transform="translate(12 '+Y(.5)+') rotate(-90)" text-anchor="middle" font-size="10" fill="'+C.muted+'">probabilidade de sobreviver</text>';
 return chartFrame(w,h,svg,'Sobrevivência média e robusta, com e sem semente física persistente');
}
function profileFigure(v){
 const w=width('renewal-viz'),h=Math.min(350,Math.max(280,w*.55));
 const a=squareAxes(w,h,'sobrevivência no contexto 0','sobrevivência no contexto 1');
 let svg=a.svg;
 // The dashed segment is a mixture of whole policies, not a free feasible
 // set for the original bounded-memory architecture.
 svg+='<path d="M'+a.X(0)+' '+a.Y(1)+' L'+a.X(1)+' '+a.Y(0)+'" fill="none" stroke="'+C.blue+'" stroke-dasharray="5 5" stroke-width="1.4"/>';
 svg+='<path d="M'+a.X(0)+' '+a.Y(0)+' L'+a.X(1)+' '+a.Y(1)+'" fill="none" stroke="'+C.line+'" stroke-width="1.5"/>';
 for(const [x,y,color,name] of [[1,0,C.gold,'proteger somente W=0'],[0,1,C.gold,'proteger somente W=1'],[v.balanced,v.balanced,C.green,'preservação simétrica']]){
  svg+='<circle cx="'+a.X(x)+'" cy="'+a.Y(y)+'" r="6" fill="'+color+'" stroke="#fff" stroke-width="1.5"><title>'+name+'</title></circle>';
 }
 if(state.seed)svg+='<circle cx="'+a.X(.5)+'" cy="'+a.Y(.5)+'" r="6" fill="'+C.blue+'" stroke="#fff" stroke-width="1.5"><title>Mistura persistente entre programas constantes</title></circle>';
 return chartFrame(w,h,svg,'Três perfis determinísticos não dominados e mistura que exige memória adicional');
}
function renderRenewal(){
 const v=renewal(state.noise,state.cycles),allowed=tolerance(state.alpha,state.cycles);
 const robust=state.seed?v.seed:v.robust;
 const switchText=v.balanced>=.5?'A política simétrica também maximiza a média neste horizonte.':'A média é maximizada protegendo um contexto e abandonando o outro; a política simétrica continua ótima para a garantia dos dois.';
 document.getElementById('renewal-viz').innerHTML='<div class="stats">'+
 stat('Garantia para ambos',pct(robust),state.seed?'com estado persistente adicional':'sem semente externa persistente')+
 stat('Melhor média',pct(v.mean),'contextos equiprováveis')+
 stat('Erro tolerável',pct(allowed),'para risco global ≤ '+pct(state.alpha))+'</div>'+
 '<div class="plot-label">HORIZONTE × CONFIABILIDADE</div>'+survivalFigure(state.cycles,state.noise,state.seed)+
 legend([['garantia, arquitetura original',C.green],['ótimo médio',C.gold],...(state.seed?[['garantia com semente',C.blue]]:[])])+
 '<div class="note '+(v.balanced<.5?'warn':'')+'">'+switchText+'</div>'+
 '<div class="chart-divider"></div><div class="plot-label">PERFIL DE VIABILIDADE · NÃO APENAS SUA MÉDIA</div>'+profileFigure(v)+
 legend([['preservar distinção',C.green],['comprometer-se com um contexto',C.gold],['mistura exige variável persistente',C.blue]])+
 '<div class="twin"><div class="tile"><span>Na política simétrica: sobreviventes</span><strong>1 bit</strong><p>A memória dos que completaram os ciclos identifica o contexto perfeitamente.</p></div><div class="tile"><span>Na política simétrica: população inicial</span><strong>'+pct(v.liveMass)+'</strong><p>Esta é a probabilidade de continuar vivo. Renormalizar os sobreviventes esconderia as demais trajetórias.</p></div></div>'+
 '<div class="note">Escala conjunta: <b>τ = n·p = '+fmt(v.tau,3)+'</b>. Para p pequeno, a curva robusta aproxima exp(−τ). A troca de objetivo médio ocorre em τ≈ln(2), não por uma bifurcação do sistema físico.</div>';
}
function sync(){
 for(const [i,key] of ['p00','p01','p10','p11'].entries()){
  document.getElementById(key).value=state.probabilities[i];
  document.getElementById('o-'+key).textContent=fmt(state.probabilities[i],2);
 }
 for(const key of ['noise','cycles','alpha']){
  document.getElementById(key).value=state[key];
  document.getElementById('o-'+key).textContent=key==='cycles'?String(state[key]):pct(state[key]);
 }
 document.getElementById('seed').checked=state.seed;
}
for(const [i,key] of ['p00','p01','p10','p11'].entries())document.getElementById(key).addEventListener('input',e=>{state.probabilities[i]=Number(e.target.value);sync();renderChannel();});
for(const key of ['noise','cycles','alpha'])document.getElementById(key).addEventListener('input',e=>{state[key]=Number(e.target.value);sync();renderRenewal();});
document.getElementById('seed').addEventListener('change',e=>{state.seed=e.target.checked;renderRenewal();});
document.querySelectorAll('[data-channel]').forEach(b=>b.addEventListener('click',()=>{
 state.probabilities={reset:[0,1,0,1],noisy:[.1,.9,.1,.9],passive:[0,0,1,1],blind:[.5,.5,.5,.5]}[b.dataset.channel].slice();sync();renderChannel();
}));
document.querySelectorAll('[data-renewal]').forEach(b=>b.addEventListener('click',()=>{
 const x={short:[.1,3],cross:[.1,7],long:[.1,30],perfect:[0,20]}[b.dataset.renewal];
 state.noise=x[0];state.cycles=x[1];sync();renderRenewal();
}));
let resizeTimer;
window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{renderChannel();renderRenewal();},100);});
sync();renderChannel();renderRenewal();
