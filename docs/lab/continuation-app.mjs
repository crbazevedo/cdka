import {DATA,analyze,best,required} from './continuation-core.mjs';
const S={tail:.01,horizon:2,capacity:2,erasure:0};
const C=['#b87d48','#356b56','#567c95'];
const named={hold:'manter',service:'manutenção',refresh:'atualizar',correct:'corrigir'};
const fmt=(x,n=4)=>{const s=Number(x).toFixed(n);return (s.includes('.')?s.replace(/0+$/,'').replace(/\.$/,''):s).replace('.',',');};
const pct=x=>fmt(x*100,4)+'%';
const svg=(h,body,label)=>'<svg class="viz" viewBox="0 0 660 '+h+'" role="img" aria-label="'+label+'" xmlns="http://www.w3.org/2000/svg">'+body+'</svg>';
const legend=items=>'<div class="legend">'+items.map(([name,color])=>'<span><i style="background:'+color+'"></i>'+name+'</span>').join('')+'</div>';
function envelope(view){
 const L=52,R=16,T=21,B=42,W=660,H=262,pw=W-L-R,ph=H-T-B;
 const X=x=>L+x*pw,Y=y=>T+(1-y)/.6*ph;
 let out='';
 for(let i=0;i<=4;i++){
  const x=i/4,y=.4+.6*i/4;
  out+='<line x1="'+L+'" y1="'+Y(y)+'" x2="'+(W-R)+'" y2="'+Y(y)+'" stroke="#e4e8dd"/>'+
       '<text x="'+(L-8)+'" y="'+(Y(y)+4)+'" text-anchor="end" font-size="11" fill="#7b8b7d">'+fmt(100*y,0)+'%</text>'+
       '<text x="'+X(x)+'" y="'+(H-B+18)+'" text-anchor="middle" font-size="11" fill="#7b8b7d">'+fmt(x,2)+'</text>';
 }
 const t=DATA.tables[String(S.horizon)];
 t.plans.forEach((pi,i)=>{
  out+='<path d="M'+X(0)+' '+Y(pi.alpha[1])+' L'+X(1)+' '+Y(pi.alpha[0])+'" stroke="'+C[i]+'" opacity=".5" stroke-width="1.5" stroke-dasharray="4 4" fill="none"/>';
 });
 t.intervals.forEach((part,i)=>{
  const pi=t.plans.find(p=>p.id===part.id),v=x=>x*pi.alpha[0]+(1-x)*pi.alpha[1];
  out+='<path d="M'+X(part.lo)+' '+Y(v(part.lo))+' L'+X(part.hi)+' '+Y(v(part.hi))+'" stroke="'+C[i]+'" stroke-width="3.5" fill="none"/>';
 });
 for(let i=0;i<view.ps.length;i++){
  const p=view.ps[i],v=Math.max(...t.plans.map(pi=>p*pi.alpha[0]+(1-p)*pi.alpha[1]));
  out+='<line x1="'+X(p)+'" y1="'+(H-B)+'" x2="'+X(p)+'" y2="'+Y(v)+'" stroke="#8c9f8e" stroke-dasharray="2 4"/>'+
       '<circle cx="'+X(p)+'" cy="'+Y(v)+'" r="4.2" fill="#263f30" stroke="#fff" stroke-width="1.7"/>';
 }
 out+='<text x="'+(L+pw/2)+'" y="'+(H-2)+'" text-anchor="middle" font-size="11" fill="#6b7e6f">P(saúde inicial saudável | sinal) · coordenada do pesquisador</text>';
 return svg(H,out,'Envoltória de sobrevivência dos planos completos por sinal diagnóstico')+
  legend(t.plans.map((pi,i)=>['Plano '+String.fromCharCode(65+i)+': '+named[pi.first],C[i]]));
}
function frontier(view){
 const W=660,H=205,L=51,R=16,T=25,B=39,pw=W-L-R,ph=H-T-B;
 const maxLoss=Math.max(.03,...view.frontier.map(r=>100*r.loss))*1.25;
 let out='';
 for(let i=0;i<=3;i++){
  const val=maxLoss*i/3,y=T+ph*(1-val/maxLoss);
  out+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y+'" y2="'+y+'" stroke="#e4e8dd"/>'+
  '<text x="'+(L-7)+'" y="'+(y+4)+'" text-anchor="end" font-size="10" fill="#7b8b7d">'+fmt(val,3)+'</text>';
 }
 view.frontier.forEach((r,i)=>{
  const loss=100*r.loss,x=L+(i+.5)*pw/3,w=62,bar=ph*loss/maxLoss;
  out+='<rect x="'+(x-w/2)+'" y="'+(T+ph-bar)+'" width="'+w+'" height="'+Math.max(1,bar)+'" rx="3" fill="'+(r.capacity===S.capacity?'#356b56':'#cbdcca')+'"/>'+
  '<text x="'+x+'" y="'+(T+ph-bar-9)+'" text-anchor="middle" font-size="12" fill="#365744">'+fmt(loss,5)+'</text>'+
  '<text x="'+x+'" y="'+(H-B+20)+'" text-anchor="middle" font-size="11" fill="#6b7e6f">'+r.capacity+' estado'+(r.capacity===1?'':'s')+'</text>';
 });
 out+='<text x="'+(L+pw/2)+'" y="'+(H-1)+'" text-anchor="middle" font-size="10" fill="#7b8b7d">Perda em pontos percentuais · antes do apagamento adicional</text>';
 return svg(H,out,'Perda de sobrevivência por capacidade do registro diagnóstico');
}
function horizonMap(){
 const W=660,H=153,L=115,T=25,pw=525,ch=30,n=100;let out='';
 for(let row=0;row<3;row++){
  for(let i=0;i<n;i++){
   const e=.5*(i+.5)/n,k=row===2?3:required(e,row+1),fill=k===1?'#d6e7d5':k===2?'#e7d5af':'#b58265';
   out+='<rect x="'+(L+i*pw/n)+'" y="'+(T+row*ch)+'" width="'+(pw/n+.2)+'" height="'+(ch-3)+'" fill="'+fill+'"/>';
  }
  out+='<text x="'+(L-10)+'" y="'+(T+row*ch+18)+'" text-anchor="end" font-size="10" fill="#64796a">'+['Uma operação','Duas operações','Prever todos'][row]+'</text>';
 }
 const x=L+S.tail/.5*pw;
 out+='<line x1="'+x+'" x2="'+x+'" y1="'+(T-7)+'" y2="'+(T+3*ch)+'" stroke="#263f30" stroke-width="1.7"/>';
 for(let j=0;j<=5;j++)out+='<text x="'+(L+j*pw/5)+'" y="'+(H-14)+'" text-anchor="middle" font-size="10" fill="#7b8b7d">'+fmt(j/10,1)+'</text>';
 out+='<text x="'+(L+pw/2)+'" y="'+(H-1)+'" text-anchor="middle" font-size="10" fill="#7b8b7d">ε · de sinal discriminativo a sinal não informativo</text>';
 return svg(H,out,'Necessidade de estados de memória por precisão do diagnóstico e horizonte')+
 legend([['1 estado','#d6e7d5'],['2 estados','#e7d5af'],['3 estados','#b58265']]);
}
function codeTable(view){
 const planFor=p=>view.library.reduce((old,pi)=>p*pi.alpha[0]+(1-p)*pi.alpha[1] > p*old.alpha[0]+(1-p)*old.alpha[1]+1e-15?pi:old,view.library[0]);
 let out='<table><thead><tr><th>SINAL / P(SAUDÁVEL)</th><th>CÓDIGO</th><th>AGORA</th><th>SE UNÂNIME DEPOIS</th></tr></thead><tbody>';
 for(let i=0;i<3;i++){
  const chosen=view.selected[view.labels[i]],full=planFor(view.ps[i]);
  const suffix=pi=>pi.second.length?named[pi.second.find(([ob])=>ob[0]===0)[1]]:'—';
  const diff=suffix(chosen)!==suffix(full);
  out+='<tr class="'+(diff?'bad':'')+'"><td>y'+i+' · '+pct(view.ps[i])+'</td><td>M'+view.labels[i]+'</td><td>'+named[chosen.first]+'</td><td>'+suffix(chosen)+(diff?'<br><small>sem compressão: '+suffix(full)+'</small>':'')+'</td></tr>';
 }
 return out+'</tbody></table>';
}
function render(){
 const v=analyze(S),sameScenario=Math.abs(S.tail-.01)<1e-12&&S.horizon===2&&S.capacity===2;
 let insight=sameScenario?'Neste caso, toda a perda da compressão ocorre na segunda decisão. A primeira ação continua ótima em todos os sinais.':
 S.horizon===2&&Math.abs(S.tail-.15)<1e-12?'Aqui, duas operações exigem apenas um código para atingir seu ótimo. Uma operação exige dois. O objetivo de continuação mudou.':
 'A capacidade mínima indicada preserva o melhor valor deste horizonte, não todas as previsões contrafactuais nem o conhecimento de qualquer tarefa futura.';
 document.getElementById('plots').innerHTML='<div class="stats">'+
 '<div class="stat"><span>Sobrevivência entregue</span><strong>'+pct(v.delivered)+'</strong><small>após apagamento sinalizado</small></div>'+
 '<div class="stat"><span>Perda por compressão</span><strong class="warn">'+fmt(v.loss*100,4)+' pp</strong><small>antes do apagamento</small></div>'+
 '<div class="stat"><span>Códigos sem perda</span><strong>'+v.required+' estado'+(v.required===1?'':'s')+'</strong><small>diagnóstico adicional</small></div></div>'+
 '<div class="finding">'+insight+'</div>'+
 '<div class="chart-title">Planos completos · envoltória ótima</div>'+envelope(v)+
 '<p class="caption">'+DATA.tables[String(S.horizon)].enumerated+' planos físicos enumerados. Linhas tracejadas: valor de cada plano; trechos sólidos: o ótimo. O posterior é uma coordenada de análise, não um sinal concedido ao controlador.</p>'+
 '<div class="rule"></div><div class="chart-title">A memória escolhe uma continuação</div>'+codeTable(v)+
 '<p class="caption">O código persiste. Na segunda etapa, a política também lê a discordância real das células e o recurso. Nenhum histórico apagado é devolvido ao programa.</p>'+
 '<div class="rule"></div><div class="chart-title">Fronteira entre capacidade e perda</div>'+frontier(v)+
 '<div class="rule"></div><div class="chart-title">Mais horizonte não é sempre mais memória</div>'+horizonMap()+
 '<p class="caption">A linha “prever todos” exige probabilidades corretas de cada plano. As outras preservam apenas o ótimo da tarefa. Uma família crescente de tarefas, ao contrário de um horizonte substituído, nunca relaxa suas exigências.</p>';
 document.getElementById('o-tail').textContent=fmt(S.tail,3);
 document.getElementById('o-capacity').textContent=S.capacity;
 document.getElementById('o-erasure').textContent=pct(S.erasure);
}
for(const key of ['tail','horizon','capacity','erasure'])document.getElementById(key).addEventListener('input',e=>{S[key]=Number(e.target.value);render();});
for(const button of document.querySelectorAll('[data-preset]'))button.addEventListener('click',()=>{
 Object.assign(S,{tail:button.dataset.preset==='reverse' ? 0.15 : 0.01,horizon:2,capacity:button.dataset.preset==='full'?3:2,erasure:0});
 for(const key of Object.keys(S))document.getElementById(key).value=S[key];render();
});
render();
