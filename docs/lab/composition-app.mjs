import {defaults,states,solve,calibration,contractBound} from './composition-core.mjs';
const opts={nu:.1,cell:.02,corrector:.2,horizon:10,budget:4,health:0,k:0,delta:.02};
const colors={hold:'#e3e8df',correct:'#dbe9dc',refresh:'#d8e5ec',service:'#eedec9'};
const names={hold:'manter',correct:'corrigir',refresh:'observar',service:'manutenção'};
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pct=x=>(100*x).toFixed(1).replace(/\.0$/,'')+'%';
const fmt=(x,n=4)=>x.toFixed(n).replace(/\.?0+$/,'');
const el=id=>document.getElementById(id);
function plot(lines,maxX,ylim=1){
 const W=700,H=245,L=45,R=15,T=14,B=38,pw=W-L-R,ph=H-T-B;
 const X=x=>L+pw*x/maxX,Y=y=>T+ph*(1-y/ylim);let s='';
 for(let j=0;j<=4;j++){
  const v=ylim*j/4,y=Y(v);s+=`<line x1="${L}" y1="${y}" x2="${W-R}" y2="${y}" stroke="#e3e8df"/><text x="${L-7}" y="${y+3}" text-anchor="end" fill="#76877b" font-size="10">${fmt(v,2)}</text>`;
  const x=maxX*j/4;s+=`<text x="${X(x)}" y="${H-B+17}" text-anchor="middle" fill="#76877b" font-size="10">${fmt(x,1)}</text>`;
 }
 s+=`<line x1="${X(opts.horizon)}" y1="${T}" x2="${X(opts.horizon)}" y2="${H-B}" stroke="#a0b19f" stroke-dasharray="4 5"/>`;
 for(const line of lines){const d=line.values.map((v,i)=>(i?'L':'M')+X(i).toFixed(2)+' '+Y(v).toFixed(2)).join(' ');s+=`<path d="${d}" stroke="${line.color}" fill="none" stroke-width="2.7" ${line.dash?'stroke-dasharray="5 5"':''}/>`;}
 s+=`<text x="${L+pw/2}" y="${H-3}" text-anchor="middle" fill="#76877b" font-size="10">Épocas até o prazo</text>`;
 return `<svg class="chart" role="img" aria-label="Curvas de probabilidade por horizonte" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">${s}</svg>`;
}
function draw(){
 const p={...defaults,world_flip:opts.nu,cell_flip:opts.cell,correction_error:[.01,opts.corrector]};
 const n=30,index=(2*opts.k+opts.health)*5+opts.budget;
 const full=solve(p,n),blind=solve(p,n,['hold','correct','service']),worn=solve(p,n,['hold','correct','refresh']);
 const prob=full.levels[opts.horizon][index],chosen=full.policies[opts.horizon][index];
 el('stats').innerHTML=`<div class="stat"><span>Sobrevivência em ${opts.horizon} épocas</span><strong>${pct(prob)}</strong></div><div class="stat"><span>Primeira operação</span><strong style="font-size:25px">${names[chosen]}</strong></div><div class="stat"><span>Redução exata no contrato</span><strong>80 → 20</strong></div>`;
 el('survival').innerHTML=plot([{values:full.levels.map(v=>v[index]),color:'#356b56'},{values:blind.levels.map(v=>v[index]),color:'#567c95',dash:true},{values:worn.levels.map(v=>v[index]),color:'#ae7a46',dash:true}],30);
 let grid='<table class="policy"><thead><tr><th>Sinal / saúde</th>'+[0,1,2,3,4].map(b=>'<th>b='+b+'</th>').join('')+'</tr></thead><tbody>';
 for(let k=0;k<=1;k++)for(let h=0;h<=1;h++){
  grid+=`<tr><th>${k?'discordante':'unânime'} / ${h?'degradado':'saudável'}</th>`;
  for(let b=0;b<=4;b++){const a=full.policies[opts.horizon][(2*k+h)*5+b];grid+=`<td style="background:${colors[a]}">${names[a]}</td>`;}grid+='</tr>';
 }el('policy').innerHTML=grid+'</tbody></table>';
 const cal=calibration(p,opts.delta,30),gaps=[],bounds=[];
 for(let h=0;h<=30;h++){gaps.push(Math.max(...cal.actual.levels[h].map((v,i)=>Math.abs(v-cal.approx.levels[h][i]))));bounds.push(contractBound(cal.delta,h));}
 el('bounds').innerHTML=plot([{values:gaps,color:'#567c95'},{values:bounds,color:'#a45d4a',dash:true}],30);
 el('certificate').textContent=`Desvio uniforme composto por etapa: ${fmt(cal.delta,6)}. Em ${opts.horizon} etapas, diferença máxima de valor: ${fmt(gaps[opts.horizon],6)}; limite certificado: ${fmt(bounds[opts.horizon],6)}. Não são limites de recorrência infinita.`;
}
for(const key of Object.keys(opts)){const control=el(key);control.addEventListener('input',()=>{opts[key]=Number(control.value);sync();draw();});}
function sync(){for(const [k,v] of Object.entries(opts)){el(k).value=v;el('o-'+k).textContent=['nu','cell','corrector','delta'].includes(k)?pct(v):String(v);}}
let catalog;
const statesPT={active:'ativo',parked:'estacionado',instrument:'instrumento',validated_scope:'validado no escopo',queued:'na fila'};
function renderCatalog(){
 if(!catalog)return;const text=el('search').value.toLowerCase(),status=el('filter').value;
 const matches=catalog.branches.filter(b=>(status==='all'||b.status===status)&&JSON.stringify(b).toLowerCase().includes(text));
 el('catalog-count').textContent=matches.length+' de '+catalog.branches.length+' abordagens · dois ramos ativos';
 el('branches').innerHTML=matches.map(b=>`<details><summary>${esc(b.id+' · '+b.title)}<small>${statesPT[b.status]}</small></summary><p><strong>Hipótese:</strong> ${esc(b.hypothesis)}</p><p><strong>Retomar quando:</strong> ${esc(b.reactivation_trigger)}</p><p><strong>Teste mínimo:</strong> ${esc(b.minimal_test)}</p><p><strong>Instrumentos:</strong> ${esc(b.tools.join(', '))}</p><p><strong>Gate:</strong> ${esc(b.acceptance_gate)}</p><p><strong>Alternativas:</strong> ${esc(b.fallbacks.join(', '))}</p></details>`).join('');
 el('failures').innerHTML=catalog.rejected_simplifications.map(d=>`<li><strong>${esc(d.claim)}.</strong> ${esc(d.reason)} → ${esc(d.fallbacks.join(', '))}</li>`).join('');
}
el('search').addEventListener('input',renderCatalog);el('filter').addEventListener('change',renderCatalog);
sync();draw();
const embedded=document.getElementById('catalog-data');
if(embedded){catalog=JSON.parse(embedded.textContent);renderCatalog();}
else fetch('./research-options.json').then(r=>{if(!r.ok)throw Error('Catálogo indisponível');return r.json();}).then(data=>{catalog=data;renderCatalog();}).catch(e=>{el('catalog-count').textContent=e.message;});
