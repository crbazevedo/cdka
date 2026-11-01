import {ARTICLES} from './articles.mjs';
import {minimumCover,faces,t1,t1trajectory,t2,gaussianFailure,gaussianRate,t3,
        t4,t5,replicator,replicatorDerivative,clamp} from './core.mjs';

const COLOR={moss:'#356b56',ochre:'#b87d48',rust:'#a95c4e',blue:'#567c95',
             muted:'#8c9c90',pale:'#d9e8d9',sand:'#efe1c4',danger:'#e6cbc1',
             dark:'#24372f',paper:'#fffdf8'};
const S={
 B1:{matrix:[[1,1,0],[0,1,1],[1,0,1]]},
 T1:{lambda:1,horizon:2.5,infinite:true,neutral:false},
 T2:{lambda:.9,epsilon:.24,c:.28,world:1,action:-1},
 T3:{budget:12,target:.55,sensorScale:2,repairScale:2},
 T4:{horizon:8,health:1,tokens:2,q:.92},
 T5:{impulse:1.4,gain:.7,step:13},
 T6:{p0:.35,x0:.2,beta:2,eta:.8,rho:1}
};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=(x,n=2)=>Number.isFinite(x)?Number(x).toFixed(n).replace(/\.?0+$/,''): '—';
const pct=(x,n=1)=>fmt(100*x,n)+'%';
const rgba=({r,g,b},opacity=1)=>'rgba('+r+','+g+','+b+','+opacity+')';
function hexRgb(hex){return {r:parseInt(hex.slice(1,3),16),g:parseInt(hex.slice(3,5),16),b:parseInt(hex.slice(5,7),16)};}
function blend(a,b,t){const A=hexRgb(a),B=hexRgb(b),f=clamp(t,0,1);return 'rgb('+[A.r,A.g,A.b].map((v,i)=>Math.round(v*(1-f)+[B.r,B.g,B.b][i]*f)).join(',')+')';}
function stat(label,value,desc='',risk=false){
 return '<div class="stat"><span class="stat-caption">'+esc(label)+'</span><span class="stat-number'+(risk?' risk':'')+'">'+esc(value)+'</span><span class="stat-small">'+esc(desc)+'</span></div>';
}
function statGroup(...items){return '<div class="stat-grid">'+items.join('')+'</div>';}
function labelPlot(text){return '<div class="plot-label">'+esc(text)+'</div>';}
function caption(text){return '<p class="plot-caption">'+esc(text)+'</p>';}
function legend(items){return '<div class="legend">'+items.map(([label,color])=>'<span><i style="background:'+color+'"></i>'+esc(label)+'</span>').join('')+'</div>';}
function svg(width,height,content,name='Gráfico científico interativo'){
 return '<svg class="chart-svg" viewBox="0 0 '+width+' '+height+'" role="img" aria-label="'+esc(name)+'" xmlns="http://www.w3.org/2000/svg">'+content+'</svg>';
}
function linePlot(lines,{
 xMin=0,xMax=1,yMin=0,yMax=1,w=740,h=255,xTitle='',yTitle='',
 markers=[],hLines=[],step=false
}={}){
 const L=52,R=16,T=22,B=42,pw=w-L-R,ph=h-T-B;
 const X=x=>L+(x-xMin)/(xMax-xMin||1)*pw;
 const Y=y=>T+ph-(y-yMin)/(yMax-yMin||1)*ph;
 let out='<rect x="'+L+'" y="'+T+'" width="'+pw+'" height="'+ph+'" fill="#fffdfa"/>';
 for(let k=0;k<=4;k++){
   const y=yMin+(yMax-yMin)*k/4,cy=Y(y);
   out+='<line class="grid-line" x1="'+L+'" y1="'+cy+'" x2="'+(w-R)+'" y2="'+cy+'"/>';
   out+='<text class="axis-text" x="'+(L-8)+'" y="'+(cy+3)+'" text-anchor="end">'+esc(fmt(y,2))+'</text>';
   const x=xMin+(xMax-xMin)*k/4,cx=X(x);
   out+='<line class="grid-line" x1="'+cx+'" y1="'+T+'" x2="'+cx+'" y2="'+(h-B)+'" />';
   out+='<text class="axis-text" x="'+cx+'" y="'+(h-B+17)+'" text-anchor="middle">'+esc(fmt(x,2))+'</text>';
 }
 for(const y of hLines){
   const cy=Y(y.value);
   out+='<line x1="'+L+'" y1="'+cy+'" x2="'+(w-R)+'" y2="'+cy+'" stroke="'+(y.color||COLOR.ochre)+'" stroke-dasharray="4 5" stroke-width="1.4"/>';
 }
 for(const marker of markers){
   const cx=X(marker.x);
   out+='<line x1="'+cx+'" y1="'+T+'" x2="'+cx+'" y2="'+(h-B)+'" stroke="'+(marker.color||COLOR.rust)+'" stroke-dasharray="4 5" stroke-width="1.5"/>';
   if(marker.text) out+='<text x="'+(cx+4)+'" y="'+(T+10)+'" font-size="10" fill="'+(marker.color||COLOR.rust)+'">'+esc(marker.text)+'</text>';
 }
 for(const line of lines){
   let path='';
   for(let i=0;i<line.points.length;i++){
     const [x,y]=line.points[i]; if(!Number.isFinite(x)||!Number.isFinite(y)){path='';continue;}
     path+=(i===0?'M':'L')+X(clamp(x,xMin,xMax)).toFixed(2)+' '+Y(clamp(y,yMin,yMax)).toFixed(2)+' ';
   }
   out+='<path d="'+path+'" fill="none" stroke="'+(line.color||COLOR.moss)+'" stroke-width="'+(line.width||2.7)+'" stroke-opacity="'+(line.opacity??1)+'" stroke-linejoin="round" stroke-linecap="round" '+(line.dash?'stroke-dasharray="'+line.dash+'"':'')+'/>';
 }
 out+='<line class="axis-line" x1="'+L+'" y1="'+(h-B)+'" x2="'+(w-R)+'" y2="'+(h-B)+'"/>';
 out+='<text class="axis-text" x="'+(L+pw/2)+'" y="'+(h-5)+'" text-anchor="middle">'+esc(xTitle)+'</text>';
 out+='<text class="axis-text" transform="translate(12 '+(T+ph/2)+') rotate(-90)" text-anchor="middle">'+esc(yTitle)+'</text>';
 return svg(w,h,out,'Gráfico de '+yTitle+' por '+xTitle);
}
function linkSource([name,url]){
  const adjusted=url.startsWith('../')?url.slice(3):url;
  return '<a href="'+esc(adjusted)+'" target="_blank" rel="noopener">'+esc(name)+' ↗</a>';
}
function nav(){
 document.getElementById('result-nav').innerHTML=ARTICLES.map(a=>
  '<a class="nav-item" href="#'+a.id.toLowerCase()+'" data-nav="'+a.id+'"><span class="nav-number">'+a.number+'</span><span class="nav-title">'+esc(a.title)+'<span class="nav-sub">'+esc(a.kind)+'</span></span></a>'
 ).join('');
}
const slider=(key,label,min,max,step,val)=>'<div class="control"><label for="c-'+key+'">'+esc(label)+' <output data-output="'+key+'">'+formatControl(key,val)+'</output></label><input id="c-'+key+'" aria-label="'+esc(label)+'" data-param="'+key+'" type="range" min="'+min+'" max="'+max+'" step="'+step+'" value="'+val+'"></div>';
const toggle=(key,label,checked)=>'<label class="toggle"><input type="checkbox" data-param="'+key+'" '+(checked?'checked':'')+'> '+esc(label)+'</label>';
function formatControl(key,v){
 if(key==='q'||key==='target')return pct(v,0);
 if(['lambda','epsilon','c','sensorScale','repairScale','impulse','gain','beta','eta','rho','p0','x0'].includes(key))return fmt(v,2);
 return String(v);
}
function controls(id){
const s=S[id];
switch(id){
case 'B1':
 return '<h3>Editar a relação</h3><p class="control-help">Toque cada célula para alternar se uma ação funciona em um estado. Verifique a cobertura ótima.</p>'+
 '<div class="preset-row"><button class="pill" data-preset="triangle">Pares compatíveis</button><button class="pill" data-preset="universal">Ação universal</button><button class="pill" data-preset="disjoint">Ações distintas</button></div>';
case 'T1':return '<h3>Parâmetros físicos</h3>'+
 slider('lambda','Acoplamento λ',0,4.5,.01,s.lambda)+
 slider('horizon','Horizonte T',.2,6,.1,s.horizon)+toggle('infinite','Horizonte infinito',s.infinite)+toggle('neutral','Permitir ação u=0',s.neutral)+
 '<p class="control-help">Mudanças no horizonte e nos atuadores deslocam os limiares sem alterar a estabilidade da dinâmica.</p>';
case 'T2':return '<h3>Ruído e confiabilidade</h3>'+
 slider('lambda','Acoplamento λ',0,2.8,.01,s.lambda)+
 slider('epsilon','Ruído ε',.04,1,.01,s.epsilon)+
 slider('c','Exigência c',.02,1.2,.01,s.c)+
 '<p class="control-help">Para a curva de convergência:</p>'+
 '<label class="toggle">Estado <select data-param="world"><option value="1">w=+1</option><option value="-1">w=−1</option></select></label>'+
 '<label class="toggle">Ação <select data-param="action"><option value="-1">u=−1</option><option value="1">u=+1</option></select></label>';
case 'T3':return '<h3>Recursos compartilhados</h3>'+
 slider('budget','Orçamento B',3,24,1,s.budget)+
 slider('target','Sucesso mínimo',.1,.9,.01,s.target)+
 slider('sensorScale','Custo da percepção',.5,5,.1,s.sensorScale)+
 slider('repairScale','Custo da manutenção',.5,5,.1,s.repairScale)+
 '<p class="control-help">Todos os pontos no triângulo consomem o mesmo orçamento total.</p>';
case 'T4':return '<h3>Controle sequencial</h3>'+
 slider('horizon','Passos restantes',1,12,1,s.horizon)+
 slider('health','Saúde do sensor',0,3,1,s.health)+
 slider('tokens','Reparos disponíveis',0,4,1,s.tokens)+
 slider('q','Precisão do sensor',.55,1,.01,s.q)+
 '<p class="control-help">Observar consome saúde; reparar preserva capacidade, mas expõe o controlador ao risco durante um passo.</p>';
case 'T5':return '<h3>Intervenção causal</h3>'+
 slider('impulse','Intensidade do choque',.2,3,.05,s.impulse)+
 slider('gain','Ganho do feedback',.1,1.4,.05,s.gain)+
 slider('step','Instante do choque',6,23,1,s.step)+
 '<p class="control-help">Antes do choque, replay e feedback geram as mesmas trajetórias. Depois, o feedback altera suas ações.</p>';
case 'T6':return '<h3>Seleção e ambiente</h3>'+
 slider('p0','Fração inicial A',.05,.95,.01,s.p0)+
 slider('x0','Ambiente inicial x',-1,1,.05,s.x0)+
 slider('beta','Força seletiva β',.4,4,.1,s.beta)+
 slider('eta','Retroação η',.2,1.2,.05,s.eta)+
 slider('rho','Dissipação ρ',.5,2,.05,s.rho)+
 '<p class="control-help">O retrato de fases mostra duas bacias atratoras; a razão das frequências acumula história.</p>';
default:return '';
}}
function articleView(a){
 const ix=ARTICLES.findIndex(x=>x.id===a.id),next=ARTICLES[(ix+1)%ARTICLES.length];
 return '<div class="topline"><span class="series">NOTA DE PESQUISA / '+a.number+' DE 07</span><span class="result-tag">'+esc(a.status)+'</span></div>'+
 '<h1 class="h-title">'+esc(a.title)+'</h1><p class="lead">'+esc(a.intuition)+'</p><div class="question">'+esc(a.question)+'</div>'+
 '<hr class="hairline"><div class="lab-top"><h2 class="section-title">Laboratório interativo</h2><span class="section-meta">EXPERIMENTE · OBSERVE · COMPARE</span></div>'+
 '<p class="lab-desc">'+esc(a.simulator)+'</p>'+
 '<div class="lab-grid"><section class="viz-shell" aria-label="Visualizações"><div id="viz" class="viz-inner"></div></section>'+
 '<aside class="controls" id="controls" aria-label="Parâmetros de simulação">'+controls(a.id)+'</aside></div>'+
 '<div class="reading-grid">'+
 '<section class="article-section"><h3>Por que estudar isto?</h3><p>'+esc(a.motivation)+'</p></section>'+
 '<section class="article-section"><h3>Como se conecta ao CDKA?</h3><p>'+esc(a.bigger)+'</p></section>'+
 '<section class="article-section"><h3>Definições mínimas</h3><table class="definitions"><tbody>'+a.definitions.map(([term,detail])=>'<tr><td>'+esc(term)+'</td><td>'+esc(detail)+'</td></tr>').join('')+'</tbody></table></section>'+
 '<section class="article-section"><h3>Formulação</h3><pre class="math-paper">'+esc(a.formula)+'</pre></section>'+
 '<section class="article-section"><h3>Exemplo</h3><p>'+esc(a.example)+'</p></section>'+
 '<section class="article-section"><h3>O que habilita depois?</h3><p>'+esc(a.next)+'</p></section>'+
 '</div><section class="finding"><div class="finding-label">RESULTADO / ESTADO ATUAL</div><p>'+esc(a.finding)+'</p></section>'+
 '<div class="article-section"><h3>Limites do modelo</h3><p>'+esc(a.limits)+'</p><div class="source-links">'+a.sources.map(linkSource).join('')+
 ' <a href="articles/'+a.id+'.md">Artigo em Markdown ↗</a></div></div>'+
 '<div class="article-bottom"><span class="citation-warning">Este laboratório separa demonstrações, modelos ilustrativos e conjecturas. Simular não substitui provar.</span>'+
 '<a class="nav-next" href="#'+next.id.toLowerCase()+'">Próximo: '+next.id+' ↗</a></div>';
}
function renderB1(){
const matrix=S.B1.matrix,solution=minimumCover(matrix),facets=faces(matrix);
const tri=facets.some(f=>f.length===3),pairs=facets.filter(f=>f.length===2);
const edge=(a,b)=>pairs.some(f=>f.includes(a)&&f.includes(b));
const pos=[[140,56],[66,184],[214,184]];
let triSVG='<g>'+ (tri?'<path d="M140 56L66 184L214 184Z" fill="#dcebdc" fill-opacity=".7"/>':'')+'</g>';
for(const [i,j] of [[0,1],[0,2],[1,2]])if(edge(i,j)){
 const p=pos[i],q=pos[j];triSVG+='<line x1="'+p[0]+'" y1="'+p[1]+'" x2="'+q[0]+'" y2="'+q[1]+'" stroke="'+COLOR.moss+'" stroke-width="2.3"/>';
}
for(let i=0;i<3;i++) triSVG+='<circle cx="'+pos[i][0]+'" cy="'+pos[i][1]+'" r="16" fill="'+COLOR.dark+'"/><text x="'+pos[i][0]+'" y="'+(pos[i][1]+4)+'" text-anchor="middle" fill="#fff" font-size="12">'+['A','B','C'][i]+'</text>';
triSVG+='<text x="140" y="232" text-anchor="middle" fill="#75887b" font-size="11">'+(tri?'Interseção comum às três':'Arestas não garantem interseção tripla')+'</text>';
let graph='<text x="30" y="22" font-size="11" fill="#809187">ESTADOS</text><text x="430" y="22" font-size="11" fill="#809187">AÇÕES</text>';
for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(matrix[i][j]){
 const chosen=solution.cover.includes(j),y1=50+85*i,y2=50+85*j;
 graph+='<path d="M71 '+y1+' C210 '+y1+' 250 '+y2+' 419 '+y2+'" stroke="'+(chosen?COLOR.moss:'#becabe')+'" stroke-width="'+(chosen?2.7:1.6)+'" fill="none" opacity="'+(chosen?1:.65)+'"/>';
}
for(let i=0;i<3;i++){
 graph+='<circle cx="55" cy="'+(50+85*i)+'" r="19" fill="'+COLOR.dark+'"/><text x="55" y="'+(55+85*i)+'" fill="white" font-size="13" text-anchor="middle">'+['A','B','C'][i]+'</text>';
 graph+='<circle cx="440" cy="'+(50+85*i)+'" r="19" fill="'+(solution.cover.includes(i)?COLOR.moss:'#d4ded2')+'"/><text x="440" y="'+(55+85*i)+'" fill="'+(solution.cover.includes(i)?'white':COLOR.dark)+'" font-size="13" text-anchor="middle">'+(i+1)+'</text>';
}
const matrixHtml='<table class="matrix" aria-label="Editar ações seguras"><thead><tr><th></th><th>Ação 1</th><th>Ação 2</th><th>Ação 3</th></tr></thead><tbody>'+
 matrix.map((row,i)=>'<tr><th>Estado '+['A','B','C'][i]+'</th>'+
  row.map((v,j)=>'<td><button aria-label="Estado '+['A','B','C'][i]+', ação '+(j+1)+', '+(v?'viável':'não viável')+'" class="'+(v?'yes ':'')+(solution.cover.includes(j)?'selected':'')+'" data-cell="'+i+','+j+'">'+(v?'✓':'×')+'</button></td>').join('')+'</tr>').join('')+'</tbody></table>';
return statGroup(
stat('Mensagens mínimas',solution.feasible?String(solution.k):'—',solution.feasible?'códigos distintos':'nenhuma cobertura',!solution.feasible),
stat('Memória fixa',solution.feasible?solution.bits+' bit'+(solution.bits===1?'':'s'):'—','para selecionar alguma ação'),
stat('Ação tripla',tri?'Sim':'Não',pairs.length+' pares compatíveis'))+
labelPlot('Relação entre estados e ações')+matrixHtml+
'<div class="fig-stack"><div>'+labelPlot('Cobertura ótima · arestas verdes escolhidas')+
svg(500,290,graph,'Grafo bipartido de ações seguras e cobertura mínima')+'</div>'+
'<div class="plot-divider"></div><div>'+labelPlot('Topologia de compatibilidade')+
svg(280,245,triSVG,'Complexo simplicial de compatibilidade de três estados')+'</div></div>'+
caption(solution.feasible?'Uma ação por classe de memória; cobertura '+solution.cover.map(j=>'a'+(j+1)).join(', ')+'.':'Nenhum código resolve um estado sem ação segura. A inviabilidade não se corrige com mais memória.');
}
function renderT1(){
const s=S.T1,T=s.infinite?Infinity:s.horizon,m=t1({lambda:s.lambda,horizon:T,neutral:s.neutral});
const bits=m.cover.bits===null?'inviável':m.cover.bits+' bit'+(m.cover.bits===1?'':'s');
let cells='',W=740,H=258,L=53,R=17,Top=23,B=34,nx=55,ny=21,pw=W-L-R,ph=H-Top-B;
for(let y=0;y<ny;y++)for(let x=0;x<nx;x++){
 const la=4.5*(x+.5)/nx,t=.2+5.8*(y+.5)/ny;
 const k=t1({lambda:la,horizon:t,neutral:s.neutral}).cover.k;
 const fill=k===null?'#edd3c9':k===1?'#dceadb':'#eadbbd';
 cells+='<rect x="'+(L+x*pw/nx)+'" y="'+(Top+(ny-y-1)*ph/ny)+'" width="'+(pw/nx+0.1)+'" height="'+(ph/ny+0.1)+'" fill="'+fill+'"/>';
}
const curX=L+pw*s.lambda/4.5,curY=Top+ph*(1-(s.infinite?6:.2+clamp(s.horizon-.2,0,5.8))/6);
cells+='<line x1="'+L+'" y1="'+(Top+ph)+'" x2="'+(W-R)+'" y2="'+(Top+ph)+'" stroke="#9aaa9e"/>';
for(let i=0;i<=4;i++){const px=L+pw*i/4;cells+='<text class="axis-text" x="'+px+'" y="'+(H-11)+'" text-anchor="middle">'+fmt(4.5*i/4,1)+'</text>';}
for(let i=0;i<=4;i++){const py=Top+ph*i/4;cells+='<text class="axis-text" x="'+(L-8)+'" y="'+(py+4)+'" text-anchor="end">'+fmt(6-5.8*i/4,1)+'</text>';}
cells+='<circle cx="'+curX+'" cy="'+(s.infinite?Top:Top+ph*(6-s.horizon)/5.8)+'" r="6" fill="'+COLOR.dark+'" stroke="white" stroke-width="2"/>';
cells+='<text class="axis-text" x="'+(L+pw/2)+'" y="'+(H-1)+'" text-anchor="middle">Acoplamento λ</text>';
const traj=[];
for(const w of [-1,1]) {
 const u=-w;
 traj.push({color:w===1?COLOR.moss:COLOR.ochre,points:t1trajectory(s.lambda,w,u,Math.min(9,s.infinite?8:s.horizon)),width:2.8});
}
const th=1.5;
const phase='<div>'+labelPlot('Mapa de regimes · horizonte × acoplamento')+svg(W,H,cells,'Fases de 0 bit, 1 bit e inviabilidade ao variar horizonte e lambda')+
legend([['0 bit','#dceadb'],['1 bit','#eadbbd'],['inviável','#edd3c9']])+'</div>';
return statGroup(stat('Memória mínima',bits,'para ações seguras',m.cover.k===null),
stat('Horizonte',s.infinite?'∞':fmt(s.horizon,1),'passos contínuos'),
stat('Equilíbrio','Estável','autovalor −1'))+
'<div class="fig-stack">'+phase+'<div class="plot-divider"></div><div>'+
labelPlot('Trajetórias contínuas · u=−w')+
linePlot(traj,{xMin:0,xMax:Math.min(9,s.infinite?8:s.horizon),yMin:-3.5,yMax:3.5,
xTitle:'tempo t',yTitle:'estado x(t)',hLines:[{value:th},{value:-th}]})+
legend([['w=+1',COLOR.moss],['w=−1',COLOR.ochre]])+'</div></div>'+
caption('A dinâmica não bifurca. O que salta é a compatibilidade entre os estados e as ações que satisfazem o limite de segurança.');
}
function renderT2(){
const s=S.T2,r=t2(s),wi=s.world===-1?0:1,ui=s.action===-1?0:1,mu=s.lambda*s.world+s.action,J=gaussianRate(mu);
const epsPts=[];
for(let i=0;i<=55;i++){
 const e=.045+.955*i/55;
 const p=gaussianFailure(mu,e);
 epsPts.push([e,-e*Math.log(Math.max(1e-300,p))]);
}
const limit=Array.from({length:55},(_,i)=>[.045+.955*i/54,J]);
const riskGrid='<table class="matrix matrix-sm"><thead><tr><th>Estado</th><th>u=−1</th><th>u=+1</th></tr></thead><tbody>'+
r.rows.map((row,i)=>'<tr><th>w='+(i===0?'−1':'+1')+'</th>'+row.map((ok,j)=>'<td class="'+(ok?'yes':'no')+'">'+pct(r.failure[i][j],1)+' <small>J='+fmt(r.rates[i][j],2)+'</small></td>').join('')+'</tr>').join('')+'</tbody></table>';
return statGroup(stat('Risco máximo',pct(r.alpha,1),'α=e^(−c/ε)'),
stat('Códigos · exato',r.exact.feasible?String(r.exact.k):'—',r.exact.feasible?'no ruído atual':'inviável',!r.exact.feasible),
stat('Códigos · limite',r.ties?'limite':' '+(r.asymptotic.feasible?r.asymptotic.k:'—'),r.ties?'há J=c':'ε→0',!r.asymptotic.feasible))+
'<div class="fig-stack"><div>'+labelPlot('Risco de falha por estado e intervenção')+riskGrid+'</div>'+
'<div class="plot-divider"></div><div>'+labelPlot('Convergência da taxa de grandes desvios')+
linePlot([{color:COLOR.moss,points:epsPts},{color:COLOR.ochre,points:limit,width:1.8,dash:'5 5'}],
{xMin:0,xMax:1,yMin:0,yMax:Math.max(1.2,J*1.5),xTitle:'ruído ε',yTitle:'−ε log P(falha)',markers:[{x:s.epsilon}]})+
legend([['taxa efetiva',COLOR.moss],['limite J='+fmt(J,3),COLOR.ochre]])+'</div></div>'+
caption('Ilustração Gaussiana de um único instante. O limiar assintótico exige J>c; em J=c, o expoente sozinho não classifica o risco.');
}
function renderT3(){
const s=S.T3,r=t3({budget:s.budget,target:s.target,
scales:{sensorScale:s.sensorScale,controlScale:2,repairScale:s.repairScale}});
const W=740,H=400,I=[370,45],U=[108,345],R=[632,345],B=s.budget;
let out='<path d="M'+I.join(' ')+'L'+U.join(' ')+'L'+R.join(' ')+'Z" fill="#f5f4ed" stroke="#abbcab" stroke-width="1.4"/>';
for(const a of r.allocations){
 const x=(I[0]*a.i+U[0]*a.u+R[0]*a.r)/B;
 const y=(I[1]*a.i+U[1]*a.u+R[1]*a.r)/B;
 const fill=blend('#ead4bf',COLOR.moss,a.success/.85);
 const radius=3.1+2.5*a.success;
 out+='<circle cx="'+x.toFixed(2)+'" cy="'+y.toFixed(2)+'" r="'+radius.toFixed(2)+'" fill="'+fill+'" fill-opacity=".92"'+(a.feasible?' stroke="#263f30" stroke-width=".8"':'')+'/>';
}
const best=r.best;
const bx=(I[0]*best.i+U[0]*best.u+R[0]*best.r)/B;
const by=(I[1]*best.i+U[1]*best.u+R[1]*best.r)/B;
out+='<circle cx="'+bx+'" cy="'+by+'" r="10" fill="none" stroke="'+COLOR.dark+'" stroke-width="2.7"/>';
out+='<circle cx="'+bx+'" cy="'+by+'" r="3" fill="'+COLOR.dark+'"/>';
out+='<text x="'+I[0]+'" y="'+(I[1]-20)+'" text-anchor="middle" font-size="12" fill="'+COLOR.dark+'">Percepção i</text>';
out+='<text x="'+(U[0]-7)+'" y="'+(U[1]+25)+'" text-anchor="middle" font-size="12" fill="'+COLOR.dark+'">Ação u</text>';
out+='<text x="'+(R[0]+6)+'" y="'+(R[1]+25)+'" text-anchor="middle" font-size="12" fill="'+COLOR.dark+'">Reparo r</text>';
for(let k=1;k<=4;k++){
 const t=k/5,x=U[0]*(1-t)+R[0]*t;
 out+='<text x="'+x+'" y="'+(U[1]+13)+'" fill="#819087" font-size="9" text-anchor="middle">'+fmt(t*B,0)+'</text>';
}
return statGroup(stat('Melhor chance',pct(best.success,1),'ótimo exato do modelo'),
stat('Alocação ótima',best.i+' / '+best.u+' / '+best.r,'percepção / ação / reparo'),
stat('Meta '+pct(s.target,0),r.feasible?'Atingível':'Não atingida',r.feasible?'há composição viável':'nenhuma composição',!r.feasible))+
'<div class="fig-stack"><div>'+labelPlot('Simplex de alocações · cada ponto usa B='+B)+
svg(W,H,out,'Triângulo de alocações de informação, controle e reparo')+
legend([['falha mais provável','#ead4bf'],['maior sucesso',COLOR.moss],['contorno: ≥ meta',COLOR.dark]])+'</div>'+
'<div class="plot-divider"></div><div>'+labelPlot('Fronteira ótima conforme orçamento aumenta')+
linePlot([{color:COLOR.moss,points:r.frontier}],{xMin:0,xMax:B,yMin:0,yMax:1,xTitle:'orçamento disponível',yTitle:'sucesso ótimo',
hLines:[{value:s.target}],markers:[{x:B}]})+'</div></div>'+
caption('Pontos interiores representam trade-offs reais de orçamento. Não se deve ler i como bits: o canal inferido do modelo tem I(W;Y)='+fmt(best.information,2)+' bit no ótimo.');
}
function renderT4(){
const s=S.T4,r=t4(s),maxH=s.horizon,svgW=740,svgH=290,L=55,Top=28,Cw=110,Rh=20;
let grid='<text x="20" y="18" fill="#809187" font-size="11">PASSOS RESTANTES ↓</text>';
for(let h=0;h<maxH;h++)for(let z=0;z<4;z++){
const cell=r.grid[h][z],color=cell.action==='sense'?'#d9e9d9':cell.action==='repair'?'#efdcc7':'#e7eae5';
 const x=L+z*Cw,y=Top+h*Rh;
 grid+='<rect x="'+x+'" y="'+y+'" width="'+(Cw-4)+'" height="'+(Rh-2)+'" rx="3" fill="'+color+'"/>';
 grid+='<text x="'+(x+Cw/2-2)+'" y="'+(y+13)+'" fill="#385547" font-size="10" text-anchor="middle">'+cell.action+' · '+fmt(cell.value,2)+'</text>';
}
for(let z=0;z<4;z++)grid+='<text x="'+(L+z*Cw+Cw/2)+'" y="'+(Top+maxH*Rh+14)+'" fill="#819087" font-size="10" text-anchor="middle">z='+z+'</text>';
for(let h=0;h<maxH;h++)grid+='<text x="'+(L-8)+'" y="'+(Top+h*Rh+13)+'" fill="#819087" font-size="10" text-anchor="end">'+(maxH-h)+'</text>';
const survLines=[{color:COLOR.moss,points:r.curve.map(a=>[a[0],a[1]])},
{color:COLOR.ochre,points:r.curve.map(a=>[a[0],a[2]]),dash:'5 5'}];
return statGroup(stat('Sobrevivência ótima',pct(r.value,1),'no horizonte selecionado'),
stat('Primeira decisão',r.first,'política ótima'),
stat('Reparos disponíveis',String(s.tokens),'recursos discretos'))+
'<div class="fig-stack"><div>'+labelPlot('Probabilidade de sobrevivência × horizonte')+
linePlot(survLines,{xMin:0,xMax:maxH,yMin:0,yMax:1,xTitle:'passos restantes',yTitle:'P(sobreviver)'})+
legend([['com reparo',COLOR.moss],['sem reparo',COLOR.ochre]])+'</div>'+
'<div class="plot-divider"></div><div>'+labelPlot('Mapa da política ótima · saúde do sensor × prazo')+
svg(svgW,Math.max(150,Top+maxH*Rh+29),grid,'Mapa de política ótima por saúde do sensor e horizonte')+
legend([['observar','#d9e9d9'],['reparar','#efdcc7'],['agir às cegas','#e7eae5']])+'</div></div>'+
caption('Cada célula é calculada por programação dinâmica; a política depende dos passos restantes, da saúde e dos recursos disponíveis.');
}
function renderT5(){
const s=S.T5,r=t5(s),series=[
{color:COLOR.moss,points:r.tracks.feedback.map((y,x)=>[x,y])},
{color:COLOR.blue,points:r.tracks.replay.map((y,x)=>[x,y]),dash:'5 4'},
{color:COLOR.rust,points:r.tracks.lesion.map((y,x)=>[x,y]),dash:'2 3'}];
const all=Object.values(r.tracks).flat();
const lim=Math.max(.55,...all.map(x=>Math.abs(x)*1.18));
const diff=r.tracks.feedback.map((x,i)=>[i,Math.abs(x-r.tracks.replay[i])]);
const maxdiff=Math.max(...diff.map(x=>x[1]));
return statGroup(stat('Choque inesperado',fmt(s.impulse,2),'no instante '+s.step),
stat('Maior divergência',fmt(maxdiff,2),'feedback vs replay'),
stat('Controle com ganho',fmt(s.gain,2),'u=clip(−k·x)'))+
'<div class="fig-stack"><div>'+labelPlot('Trajetórias externas · intervenção no instante '+s.step)+
linePlot(series,{xMin:0,xMax:r.steps,yMin:-lim,yMax:lim,xTitle:'tempo discreto',yTitle:'estado x',markers:[{x:s.step,text:'choque'}]})+
legend([['feedback',COLOR.moss],['replay externo',COLOR.blue],['feedback ablacionado',COLOR.rust]])+'</div>'+
'<div class="plot-divider"></div><div>'+labelPlot('Resposta causal · diferença absoluta após choque')+
linePlot([{color:COLOR.moss,points:diff}],{xMin:0,xMax:r.steps,yMin:0,yMax:Math.max(.15,maxdiff*1.1),
xTitle:'tempo discreto',yTitle:'|feedback−replay|',markers:[{x:s.step}]})+'</div></div>'+
caption('Igualdade observacional antes da perturbação não implica equivalência causal. Identificamos feedback neste experimento, não autonomia constitutiva.');
}
function renderT6(){
const s=S.T6,r=replicator(s),W=740,H=300,L=57,R=17,Top=20,B=43,pw=W-L-R,ph=H-Top-B;
const bound=Math.max(1.35,1.4*s.eta/s.rho);
const X=p=>L+p*pw,Y=x=>Top+ph-(x+bound)/(2*bound)*ph;
let portrait='<rect x="'+L+'" y="'+Top+'" width="'+pw+'" height="'+ph+'" fill="#fffdfa"/>';
for(let j=0;j<=4;j++){
 const y=-bound+2*bound*j/4,py=Y(y);
 portrait+='<line class="grid-line" x1="'+L+'" y1="'+py+'" x2="'+(W-R)+'" y2="'+py+'"/>';
 portrait+='<text class="axis-text" x="'+(L-8)+'" y="'+(py+3)+'" text-anchor="end">'+fmt(y,1)+'</text>';
 const px=L+pw*j/4;portrait+='<line class="grid-line" x1="'+px+'" y1="'+Top+'" x2="'+px+'" y2="'+(H-B)+'"/>';
 portrait+='<text class="axis-text" x="'+px+'" y="'+(H-B+16)+'" text-anchor="middle">'+fmt(j/4,2)+'</text>';
}
for(let i=1;i<=9;i++)for(let j=1;j<=7;j++){
 const p=i/10,x=-bound+2*bound*j/8;
 const [dp,dx]=replicatorDerivative(p,x,s);
 const ux=dp*pw,uy=-dx*ph/(2*bound),mag=Math.hypot(ux,uy);
 if(mag<1e-8)continue;
 const scale=12/mag,px=X(p),py=Y(x),ex=px+ux*scale,ey=py+uy*scale;
 portrait+='<line x1="'+px+'" y1="'+py+'" x2="'+ex+'" y2="'+ey+'" stroke="#b6c7b7" stroke-width="1.1"/>'+
 '<circle cx="'+ex+'" cy="'+ey+'" r="1.5" fill="#9db29f"/>';
}
const seeds=[[.18,.1],[.18,-.3],[.28,.55],[.4,-.6],[.62,-.3],[.82,-.1],[.78,.45],[.54,.35]];
for(const [p,x] of seeds){
const trace=replicator({...s,p0:p,x0:x}).points.filter((_,i)=>i%4===0);
portrait+='<path d="'+trace.map(([t,a,b],i)=>(i?'L':'M')+X(a).toFixed(2)+' '+Y(clamp(b,-bound,bound)).toFixed(2)).join(' ')+'" stroke="#b5c7bb" stroke-width="1.4" fill="none" opacity=".8"/>';
}
portrait+='<path d="'+r.points.filter((_,i)=>i%3===0).map(([t,p,x],i)=>(i?'L':'M')+X(p).toFixed(2)+' '+Y(clamp(x,-bound,bound)).toFixed(2)).join(' ')+'" stroke="'+COLOR.moss+'" stroke-width="3" fill="none"/>';
for(const [p,x,label,color] of [[0,-s.eta/s.rho,'B',COLOR.ochre],[1,s.eta/s.rho,'A',COLOR.moss],[.5,0,'S',COLOR.rust]]){
portrait+='<circle cx="'+X(p)+'" cy="'+Y(x)+'" r="5.5" fill="'+color+'" stroke="white" stroke-width="1.5"/>'+
'<text x="'+(X(p)+(p===1?-12:10))+'" y="'+(Y(x)-11)+'" font-size="11" fill="'+color+'">'+label+'</text>';
}
portrait+='<text class="axis-text" x="'+(L+pw/2)+'" y="'+(H-3)+'" text-anchor="middle">frequência de A · p</text>'+
'<text class="axis-text" transform="translate(12 '+(Top+ph/2)+') rotate(-90)" text-anchor="middle">ambiente x</text>';
const N=Math.ceil(r.points.length/250),trace=r.points.filter((_,i)=>i%N===0);
return statGroup(stat('Fração final de A',pct(r.finalP,1),'após '+fmt(r.points.at(-1)[0],0)+' unidades'),
stat('Equilíbrio central','Sela','p=0,5 · x=0'),
stat('Log-odds acumulado',fmt(r.points.at(-1)[3]-r.points[0][3],2),'integral de βx(t)'))+
'<div class="fig-stack"><div>'+labelPlot('Retrato de fases · campo vetorial, duas bacias e um ponto de sela')+
svg(W,H,portrait,'Campo de direções e trajetórias de frequências replicadoras e ambiente')+
legend([['trajetória selecionada',COLOR.moss],['outros estados iniciais','#b5c7bb'],['sela',COLOR.rust]])+'</div>'+
'<div class="plot-divider"></div><div>'+labelPlot('Evolução da população e do ambiente')+
linePlot([{color:COLOR.moss,points:trace.map(a=>[a[0],a[1]])},
{color:COLOR.ochre,points:trace.map(a=>[a[0],a[2]/(2*bound)+.5]),dash:'5 5'}],
{xMin:0,xMax:r.points.at(-1)[0],yMin:0,yMax:1,xTitle:'tempo t',yTitle:'p(t), ambiente reescalado'})+
legend([['fração A',COLOR.moss],['ambiente normalizado',COLOR.ochre]])+'</div></div>'+
caption('A composição guarda a história da vantagem seletiva, mas isso, isoladamente, não demonstra conhecimento contrafactual nem agência.');
}
const renderers={B1:renderB1,T1:renderT1,T2:renderT2,T3:renderT3,T4:renderT4,T5:renderT5,T6:renderT6};
let active='B1';
function refresh(){
 const host=document.getElementById('viz');
 if(!host)return;
 try {host.innerHTML=renderers[active]();}
 catch(error){host.innerHTML='<p role="alert">Falha na visualização: '+esc(error.message)+'</p>';console.error(error);}
}
function show(){
 const requested=(location.hash||'#b1').replace(/^#/,'').toUpperCase();
 const a=ARTICLES.find(v=>v.id===requested)||ARTICLES[0];
 active=a.id;
 document.title=a.id+' · '+a.title+' — CDKA';
 document.getElementById('main').innerHTML=articleView(a);
 document.querySelectorAll('[data-nav]').forEach(el=>{
 el.classList.toggle('active',el.dataset.nav===active);
 if(el.dataset.nav===active)el.setAttribute('aria-current','page');
 else el.removeAttribute('aria-current');
 });
 if(a.id==='T2'){
  document.querySelector('[data-param=world]').value=String(S.T2.world);
  document.querySelector('[data-param=action]').value=String(S.T2.action);
 }
 if(a.id==='T1')document.querySelector('[data-param=horizon]').disabled=S.T1.infinite;
 refresh();
 window.scrollTo({top:0,behavior:'instant'});
}
document.addEventListener('input',ev=>{
 const target=ev.target,key=target.dataset?.param;
 if(!key)return;
 const s=S[active];
 s[key]=target.type==='checkbox'?target.checked:Number(target.value);
 if(active==='T1'&&key==='infinite'){
   document.querySelector('[data-param=horizon]').disabled=s.infinite;
 }
 const output=document.querySelector('[data-output="'+key+'"]');
 if(output)output.textContent=formatControl(key,s[key]);
 refresh();
});
document.addEventListener('click',ev=>{
 const cell=ev.target.closest('[data-cell]');
 if(cell&&active==='B1'){
  const [w,a]=cell.dataset.cell.split(',').map(Number);
  S.B1.matrix[w][a]=S.B1.matrix[w][a]?0:1;refresh();return;
 }
 const preset=ev.target.closest('[data-preset]');
 if(preset&&active==='B1'){
  const m={triangle:[[1,1,0],[0,1,1],[1,0,1]],
    universal:[[1,0,0],[1,1,0],[1,0,1]],disjoint:[[1,0,0],[0,1,0],[0,0,1]]};
  S.B1.matrix=m[preset.dataset.preset].map(row=>row.slice());refresh();
 }
});
nav();window.addEventListener('hashchange',show);show();
