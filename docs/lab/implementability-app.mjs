import {q,ell,slope,inflection,rstar,envelope,grid,required,harvest,cycleBound} from './implementability-core.mjs';
const C={green:'#376d53',orange:'#b37d49',ink:'#253d31',grid:'#e1e6da',muted:'#718375'};
const state={sigma:.35,p:.1,n:4,R:1,h:.7,beta:.9};
const fmt=(x,d=2)=>new Intl.NumberFormat('pt-BR',{maximumFractionDigits:d}).format(x);
const pc=x=>x>0&&100*x<.01?'<0,01%':fmt(100*x,2)+'%';
const metric=(a,b,c='')=>'<div class="metric"><span>'+a+'</span><strong>'+b+'</strong><small>'+c+'</small></div>';
const wrap=(w,h,s,name)=>'<svg class="chart" viewBox="0 0 '+w+' '+h+'" role="img" aria-label="'+name+'" xmlns="http://www.w3.org/2000/svg">'+s+'</svg>';
function lines(series,{xmin=0,xmax=1,ymin=0,ymax=1,xlabel='',ylabel='',markers=[],height=250}={}){
 const W=700,H=height,L=56,R=14,T=20,B=42,pw=W-L-R,ph=H-T-B;
 const X=x=>L+pw*(x-xmin)/(xmax-xmin),Y=y=>T+ph*(ymax-y)/(ymax-ymin);
 let s='';for(let k=0;k<5;k++){const x=xmin+(xmax-xmin)*k/4,y=ymin+(ymax-ymin)*k/4;
 s+='<line x1="'+X(x)+'" y1="'+T+'" x2="'+X(x)+'" y2="'+(H-B)+'" stroke="'+C.grid+'"/><line x1="'+L+'" y1="'+Y(y)+'" x2="'+(W-R)+'" y2="'+Y(y)+'" stroke="'+C.grid+'"/>'+
 '<text x="'+X(x)+'" y="'+(H-B+18)+'" text-anchor="middle" fill="'+C.muted+'" font-size="10">'+fmt(x,1)+'</text><text x="'+(L-9)+'" y="'+(Y(y)+4)+'" text-anchor="end" fill="'+C.muted+'" font-size="10">'+fmt(y,2)+'</text>';}
 for(const m of markers){const x=X(m.x);s+='<line x1="'+x+'" y1="'+T+'" x2="'+x+'" y2="'+(H-B)+'" stroke="'+(m.color||C.orange)+'" stroke-dasharray="4 5"/><text x="'+(x+4)+'" y="'+(T+11)+'" fill="'+C.muted+'" font-size="10">'+(m.label||'')+'</text>';}
 for(const a of series){s+='<path d="'+a.points.map(([x,y],i)=>(i?'L':'M')+X(x).toFixed(2)+' '+Y(y).toFixed(2)).join(' ')+'" fill="none" stroke="'+a.color+'" stroke-width="2.7" stroke-linejoin="round" '+(a.dash?'stroke-dasharray="5 5"':'')+'/>';}
 s+='<text x="'+(L+pw/2)+'" y="'+(H-2)+'" text-anchor="middle" fill="'+C.muted+'" font-size="11">'+xlabel+'</text><text transform="translate(13 '+(T+ph/2)+') rotate(-90)" text-anchor="middle" fill="'+C.muted+'" font-size="11">'+ylabel+'</text>';
 return wrap(W,H,s,ylabel+' em função de '+xlabel);
}
function rows(){
 const sigma=state.sigma,p=state.p,b=cycleBound(sigma,p);
 document.getElementById('row-stats').innerHTML=metric('Seleção contingente',fmt(sigma,2),'σ disponível')+metric('Um ciclo',pc(b),'garantia por contexto')+metric('Dez ciclos',pc(b**10),'sem semente persistente');
 const W=700,H=300,L=125,T=23,S=235,X=x=>L+S*x,Y=y=>T+S*(1-y);
 let s='<rect x="'+L+'" y="'+T+'" width="'+S+'" height="'+S+'" fill="#f3eee4" stroke="#b4c2b4"/>';
 const polygon=[[0,0],[sigma,0],[1,1-sigma],[1,1],[1-sigma,1],[0,sigma]];
 s+='<polygon points="'+polygon.map(([x,y])=>X(x)+','+Y(y)).join(' ')+'" fill="#d7e9d9" stroke="'+C.green+'" stroke-width="1.3"/>';
 s+='<path d="M'+X(0)+' '+Y(0)+' L'+X(1)+' '+Y(1)+'" stroke="#8da18e" stroke-dasharray="4 4"/>';
 const a=(1-sigma)/2,z=(1+sigma)/2;
 s+='<circle cx="'+X(a)+'" cy="'+Y(z)+'" r="5.5" fill="'+C.green+'" stroke="#fffdf8" stroke-width="2"/>';
 for(const [x,y,label]of[[0,0,'0'],[1,0,'1'],[0,1,'1']])s+='<text x="'+(X(x)-(!x?11:0))+'" y="'+(Y(y)+(y===0?17:4))+'" fill="'+C.muted+'" font-size="10">'+label+'</text>';
 s+='<text x="'+(L+S/2)+'" y="'+(H-6)+'" fill="'+C.muted+'" text-anchor="middle" font-size="11">f₀ = P(escrever 1 | m=0)</text><text transform="translate(82 '+(T+S/2)+') rotate(-90)" fill="'+C.muted+'" text-anchor="middle" font-size="11">f₁ = P(escrever 1 | m=1)</text>';
 s+='<text x="400" y="75" fill="'+C.ink+'" font-size="14">Mesmas ações marginais.</text><text x="400" y="98" fill="'+C.muted+'" font-size="12">Diferente conjunto de regras.</text><text x="400" y="150" fill="'+C.green+'" font-size="12">σ=0: somente a diagonal.</text><text x="400" y="175" fill="'+C.green+'" font-size="12">σ=1: quadrado completo.</text><text x="400" y="225" fill="'+C.muted+'" font-size="11">A seleção ideal requer duas linhas</text><text x="400" y="243" fill="'+C.muted+'" font-size="11">compatíveis com o mesmo mecanismo.</text>';
 document.getElementById('row-chart').innerHTML=wrap(W,H,s,'Região de prescrições implementáveis, limitada por contraste sigma');
}
function temporal(){
 const n=state.n,R=state.R,u=Math.round(R/.2),ans=grid(n,u,.2),uniform=n*ell(R/n),upper=n*envelope(R/n);
 document.getElementById('budget-stats').innerHTML=metric('Ótimo na malha',pc(Math.exp(ans.logValue)),'passo 0,2')+metric('Uniforme',pc(Math.exp(uniform)),'mesmo esforço total')+metric('Limite contínuo',pc(Math.exp(upper)),'envoltória superior');
 const samples=Array.from({length:121},(_,k)=>k*.05);
 document.getElementById('curvature-chart').innerHTML=lines([{color:C.green,points:samples.map(r=>[r,ell(r)])},{color:C.orange,dash:true,points:samples.map(r=>[r,envelope(r)])}],{xmax:6,ymin:-Math.LN2,ymax:0,xlabel:'esforço por ciclo r',ylabel:'log q(r)',markers:[{x:inflection,label:'inflexão'},{x:rstar,label:'tangência'}]});
 const W=700,H=190,L=52,T=22,B=35,pw=W-L-15,ph=H-T-B,ymax=Math.max(.5,...ans.schedule,R/n)*1.12,Y=y=>T+ph*(1-y/ymax);
 let s='<text x="'+L+'" y="14" fill="'+C.muted+'" font-size="11">ALOCAÇÃO ÓTIMA NA MALHA · MESMO ORÇAMENTO R='+fmt(R,1)+'</text>';
 const cw=pw/n;
 ans.schedule.forEach((r,i)=>{s+='<rect x="'+(L+i*cw+4)+'" y="'+Y(r)+'" width="'+Math.max(1,cw-8)+'" height="'+(T+ph-Y(r))+'" rx="3" fill="'+C.green+'"/><text x="'+(L+(i+.5)*cw)+'" y="'+(H-15)+'" text-anchor="middle" fill="'+C.muted+'" font-size="10">'+(i+1)+'</text><text x="'+(L+(i+.5)*cw)+'" y="'+(Y(r)-5)+'" text-anchor="middle" fill="'+C.green+'" font-size="10">'+fmt(r,1)+'</text>';});
 s+='<line x1="'+L+'" y1="'+Y(R/n)+'" x2="'+(W-15)+'" y2="'+Y(R/n)+'" stroke="'+C.orange+'" stroke-dasharray="5 4"/>';
 document.getElementById('schedule-chart').innerHTML=wrap(W,H,s,'Alocação ótima de esforço por ciclo; linha tracejada indica alocação uniforme');
}
function recurring(){
 const h=state.h,a=harvest(40,h),large=harvest(2500,h),end=a.points.at(-1);
 document.getElementById('harvest-stats').innerHTML=metric('Sobrevive 40 ciclos',pc(Math.exp(end.logSurvival)),'massa não normalizada')+metric('Taxa em 2.500 ciclos',fmt(large.rate,4),'log sobrevivência / ciclo')+metric('Limite assintótico',fmt(envelope(h),4),'negativo para h finito');
 const max=Math.max(.5,...a.points.map(v=>Math.max(v.before,v.spend)))*1.1;
 document.getElementById('harvest-chart').innerHTML=lines([{color:C.green,points:a.points.map(v=>[v.t,v.spend])},{color:C.orange,points:a.points.map(v=>[v.t,v.before]),dash:true}],{xmin:1,xmax:40,ymin:0,ymax:max,xlabel:'ciclo',ylabel:'recurso disponível / gasto'});
 document.getElementById('lifetime-chart').innerHTML=lines([{color:C.green,points:[[0,0],...a.points.map(v=>[v.t,v.logSurvival/Math.LN10])]}],{xmax:40,ymin:Math.min(-.2,end.logSurvival/Math.LN10*1.06),ymax:0,xlabel:'ciclo',ylabel:'log₁₀ P(sobreviver)'});
 document.getElementById('required').innerHTML='Para garantir '+pc(state.beta)+':<br>10 ciclos → '+fmt(required(10,state.beta),2)+'<br>100 ciclos → '+fmt(required(100,state.beta),2)+'<br><small>Esforço total mínimo na classe declarada.</small>';
}
function outputs(){for(const key of Object.keys(state)){const el=document.getElementById('o-'+key);el.textContent=key==='beta'||key==='p'?pc(state[key]):fmt(state[key],2);}}
function refresh(){outputs();rows();temporal();recurring();}
for(const key of Object.keys(state))document.getElementById(key).addEventListener('input',ev=>{state[key]=Number(ev.target.value);refresh();});
for(const [id,R] of [['scarce',1],['abundant',24]])document.getElementById(id).addEventListener('click',()=>{state.n=4;state.R=R;document.getElementById('n').value=4;document.getElementById('R').value=R;refresh();});
refresh();
