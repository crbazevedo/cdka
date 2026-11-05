import{propagate,value,namedRule}from'./renewal-core.mjs';
const $=x=>document.getElementById(x);let data;
const colors={renew:'#356e54',retain:'#a58045',after_service:'#a46255',after_skip:'#577e91'};
const order=['renew','after_skip','retain','after_service'];
const pct=x=>(100*x).toFixed(3).replace('.',',')+'%';
const points=x=>x.toFixed(4).replace('.',',');
function svg(w,h,s,alt){return`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${alt}" xmlns="http://www.w3.org/2000/svg">${s}</svg>`;}
function render(){const n=Number($('horizon').value),chosen=$('rule').value;$('oh').textContent=n;
 const series=Object.fromEntries(order.map(r=>[r,propagate(data,r,n).curve]));
 const selected=series[chosen].at(-1),fresh=series.renew.at(-1);
 $('score').textContent=pct(selected);$('gap').textContent=points(100*(fresh-selected))+' p.p.';
 const W=820,H=310,L=58,R=18,T=20,B=40;const lo=Math.max(0,Math.min(...order.map(r=>series[r].at(-1)))-.04);
 const X=x=>L+x/Math.max(1,n)*(W-L-R),Y=y=>T+(1-y)/(1-lo)*(H-T-B);let s='';
 for(let i=0;i<=4;i++){const y=lo+(1-lo)*i/4;s+=`<line x1="${L}" x2="${W-R}" y1="${Y(y)}" y2="${Y(y)}" stroke="#e2e6dc"/><text x="${L-9}" y="${Y(y)+4}" text-anchor="end" font-size="11" fill="#738477">${Math.round(100*y)}%</text>`;const x=n*i/4;s+=`<text x="${X(x)}" y="${H-17}" text-anchor="middle" font-size="11" fill="#738477">${Number(x.toFixed(1))}</text>`;}
 for(const r of order){const d=series[r].map((v,t)=>(t?'L':'M')+X(t).toFixed(2)+' '+Y(v).toFixed(2)).join(' ');s+=`<path d="${d}" fill="none" stroke="${colors[r]}" stroke-width="${r===chosen?3.7:2.1}" opacity="${r===chosen?1:.68}"/><circle cx="${X(n)}" cy="${Y(series[r].at(-1))}" r="${r===chosen?4.5:3}" fill="${colors[r]}"/>`;}
 s+=`<text x="${W/2}" y="${H-2}" text-anchor="middle" fill="#738477" font-size="11">ciclos concluídos</text>`;
 $('curve').innerHTML=svg(W,H,s,'Sobrevivência não normalizada de quatro políticas de memória no mesmo controlador');
 $('legend').innerHTML=order.map(r=>`<span><i style="background:${colors[r]}"></i>${namedRule(r)}</span>`).join('');
 $('table').innerHTML=order.map(r=>{const record=data.fixed_routing.find(x=>x.acquisition===r),best=data.best_per_acquisition[r];return`<tr><td>${namedRule(r)}</td><td>${pct(value(record.value))}</td><td>${pct(value(best.value))}</td></tr>`;}).join('');
 $('terminal-note').textContent=n===1?'Em um ciclo, as quatro regras empatam: a atualização só acontece depois da tarefa.':'São as mesmas portas, sensores e custos. Somente a regra de renovação mudou. A biblioteca reotimizada é mostrada separadamente abaixo.';
}
function renderTrace(){const rows=data.static_trace;
 $('trace-table').innerHTML=rows.map(r=>`<tr><td><code>${r.memory.join('')}</code></td><td>${points(value(r.initial_mass))}</td><td>${points(value(r.no_service_probability))}</td><td>${points(value(r.live_skip_mass))}</td></tr>`).join('');
 const parts=data.temporal_contributions['renew-retain'].map(value);const W=820,H=250,L=46,B=35,T=20,max=Math.max(...parts)*1.15;let s='';
 parts.forEach((v,i)=>{let x=L+i*92,y=T+(1-v/max)*(H-T-B);s+=`<rect x="${x}" y="${y}" width="53" height="${H-B-y}" rx="3" fill="#356e54"/><text x="${x+26}" y="${H-B+18}" text-anchor="middle" fill="#71816f" font-size="11">${i+1}</text><text x="${x+26}" y="${y-7}" text-anchor="middle" fill="#356e54" font-size="11">${(100*v).toFixed(3)}</text>`;});
 $('attribution').innerHTML=svg(W,H,s,'Contribuição temporal em pontos percentuais da renovação comparada à retenção');
}
async function start(){data=window.CDKA_RENEWAL_DATA||await fetch('./renewal-certificate.json').then(r=>{if(!r.ok)throw Error('Certificado ausente');return r.json();});render();renderTrace();for(const id of['horizon','rule'])$(id).addEventListener('input',render);document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('active',x.id===b.dataset.tab));}));}
start().catch(e=>{$('score').textContent=e.message;console.error(e);});
