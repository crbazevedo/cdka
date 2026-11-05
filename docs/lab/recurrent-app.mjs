import {DEFAULT,run,solve,traceState,work} from './recurrent-core.mjs';
const $=id=>document.getElementById(id),C={green:'#386a50',ochre:'#b48a54',rust:'#a26354',blue:'#54768b',line:'#e3e6db',text:'#4d6355'};let state={...DEFAULT};
const pct=x=>(100*x).toFixed(2)+'%',fix=(x,n=3)=>x.toFixed(n).replace(/\.?0+$/,'');
function svg(w,h,inner,label){return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">${inner}</svg>`;}
function line(lines,{h=260,xmax=state.horizon,ymin=0,ymax=1,xlabel='tarefas sucessivas',ylabel='sobrevivência',marker=null}={}){
 const W=720,L=53,R=16,T=15,B=45,pw=W-L-R,ph=h-T-B,X=x=>L+pw*x/xmax,Y=y=>T+ph*(ymax-y)/(ymax-ymin);let out='';
 for(let j=0;j<=4;j++){let y=ymin+(ymax-ymin)*j/4;out+=`<line x1="${L}" x2="${W-R}" y1="${Y(y)}" y2="${Y(y)}" stroke="${C.line}"/><text x="${L-9}" y="${Y(y)+4}" text-anchor="end" font-size="10" fill="${C.text}">${(100*y).toFixed(0)}%</text>`;let xx=xmax*j/4;out+=`<text x="${X(xx)}" y="${h-B+19}" text-anchor="middle" font-size="10" fill="${C.text}">${fix(xx,2)}</text>`;}
 for(const l of lines)out+=`<path d="${l.points.map(([x,y],i)=>(i?'L':'M')+X(x)+' '+Y(y)).join(' ')}" fill="none" stroke="${l.color}" stroke-width="${l.dash?2:3}" ${l.dash?'stroke-dasharray="5 5"':''}/>`;
 if(marker!==null)out+=`<line x1="${X(marker)}" x2="${X(marker)}" y1="${T}" y2="${h-B}" stroke="${C.rust}" stroke-dasharray="3 5"/>`;
 out+=`<text x="${L+pw/2}" y="${h-4}" text-anchor="middle" font-size="11" fill="${C.text}">${xlabel}</text>`;return svg(W,h,out,ylabel+' por '+xlabel);
}
function stats(items){return '<div class="stats">'+items.map(([a,b,c])=>`<div><small>${a}</small><strong>${b}</strong><p>${c}</p></div>`).join('')+'</div>';}
function render(){
 const best=solve(state),conditional=run(['vote','vote'],state),always=run(['service','service'],state),never=run(['skip','skip'],state);
 $('summary').innerHTML=stats([['Diagnóstico em circuito',pct(conditional.survival),'seletor também falível'],['Melhor regra sem diagnóstico',pct(best.blind.survival),'subliblioteca estacionária'],['Serviços esperados',fix(conditional.services)+' / '+fix(always.services),'diagnóstico / manter sempre']]);
 $('survival').innerHTML=line([{points:conditional.curve.map((v,i)=>[i,v]),color:C.green},{points:always.curve.map((v,i)=>[i,v]),color:C.ochre},{points:never.curve.map((v,i)=>[i,v]),color:C.rust,dash:true}]);
 $('best-rule').textContent=best.best.policy;$('gain').textContent=((best.best.survival-best.blind.survival)*100).toFixed(4)+' ponto(s) percentual(is)';
 $('ranking').innerHTML='<table><thead><tr><th>Programa em b=3 / b=4</th><th>Sobrevivência</th><th>Serviços esperados</th></tr></thead><tbody>'+best.rows.slice(0,7).map(r=>`<tr><td>${r.policy}</td><td>${pct(r.survival)}</td><td>${fix(r.services)}</td></tr>`).join('')+'</tbody></table>';
 const grid=[];for(let i=0;i<=20;i++){const d=i/40;const op={...state,diagnostic:d};grid.push([d,run(['vote','vote'],op).survival,solve(op).blind.survival]);}
 $('diagnosis').innerHTML=line([{points:grid.map(x=>[x[0],x[1]]),color:C.green},{points:grid.map(x=>[x[0],x[2]]),color:C.ochre,dash:true}],{h:235,xmax:.5,xlabel:'erro por célula do diagnóstico',ylabel:'valor no horizonte escolhido',marker:state.diagnostic});
 const cases=[[0,[0,0,0],3],[1,[0,0,0],3],[1,[1,1,1],3],[1,[1,1,1],2]],ix=Number($('source').value),src=cases[ix],t=traceState(src,state);
 $('trace').innerHTML=stats([['Saúde física — avaliador',src[0]?'degradada':'saudável','não fornecida à política'],['Memória e saldo',src[1].join('')+' · '+src[2],'entradas físicas disponíveis'],['Solicitação de manutenção',pct(t.repair),'inclui o guardião de recursos']])+`<div class="flow"><div>Débito inicial<strong>1 token</strong></div><span>→</span><div>Serviço solicitado<strong>${pct(t.repair)}</strong></div><span>→</span><div>Tarefa correta<strong>${pct(t.value)}</strong></div><span>→</span><div>Reabastecimento<strong>só após acerto</strong></div></div><div class="callout">Manter este banco muda a sobrevivência imediata em <b>${(100*t.gain).toFixed(4)} ponto(s) percentual(is)</b>. ${src[2]<3?'O programa não pode pagar pela manutenção neste estado.':'A escolha precisa equilibrar essa consequência com os recursos futuros.'}</div>`;
 $('hazard').textContent=fix(work(0,state.sensor),8);
 for(const key of ['diagnostic','drift','restore','procedure','prior'])$('o-'+key).textContent=pct(state[key]);$('o-horizon').textContent=state.horizon;
}
for(const key of ['diagnostic','drift','restore','procedure','prior','horizon'])$(key).addEventListener('input',e=>{state[key]=Number(e.target.value);render();});
$('source').addEventListener('change',render);$('reset').addEventListener('click',()=>{state={...DEFAULT};for(const k of Object.keys(DEFAULT)){const e=$(k);if(e)e.value=state[k];}render();});
for(const b of document.querySelectorAll('[data-tab]'))b.addEventListener('click',()=>{document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('active',x.id==='panel-'+b.dataset.tab));});
render();
