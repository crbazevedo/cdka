import{number,compile,upperBound,causalWitness,traces}from'./faulty-core.mjs';
const $=id=>document.getElementById(id),col={g:'#356e54',b:'#567c95',r:'#ac6b54',o:'#b58b50',m:'#819183',line:'#e2e7dd'};
let data;const state={p:.01,gamma:.001,q:0,capacity:4};
const pct=(x,d=4)=>(100*x).toFixed(d)+'%';
function svg(w,h,s,aria){return `<svg class="chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${aria}">${s}</svg>`;}
function lineChart(series,ymax,selected){
 const W=720,H=245,L=53,R=18,T=20,B=38,X=x=>L+x/.02*(W-L-R),Y=y=>H-B-y/ymax*(H-T-B);let s='';
 if(Math.abs(state.p-.01)<1e-10)s+=`<rect x="${L}" y="${T}" width="${X(.01)-L}" height="${H-T-B}" fill="#edf3e7"/>`;
 for(let j=0;j<=4;j++){const y=ymax*j/4;s+=`<line x1="${L}" x2="${W-R}" y1="${Y(y)}" y2="${Y(y)}" stroke="${col.line}"/><text x="${L-8}" y="${Y(y)+4}" text-anchor="end" font-size="10" fill="${col.m}">${y.toFixed(3)}</text>`;const x=.005*j;s+=`<text x="${X(x)}" y="${H-16}" text-anchor="middle" font-size="10" fill="${col.m}">${(x*100).toFixed(1)}%</text>`;}
 for(const row of series)s+=`<path d="${row.pts.map(([x,y],i)=>(i?'L':'M')+X(x)+' '+Y(y)).join(' ')}" fill="none" stroke="${row.color}" stroke-width="2.6" ${row.dash?'stroke-dasharray="5 4"':''}/>`;
 s+=`<line x1="${X(selected)}" x2="${X(selected)}" y1="${T}" y2="${H-B}" stroke="${col.r}" stroke-dasharray="3 5"/><text x="${(L+W-R)/2}" y="${H-1}" text-anchor="middle" font-size="10" fill="${col.m}">erro por porta γ · eixo vertical: ganho em pontos percentuais</text>`;
 return svg(W,H,s,'Ganho de sobrevivência por erro de porta; área clara marca o intervalo certificado em p=1%');
}
function render(){
 for(const key of Object.keys(state))$('o-'+key).textContent=key==='capacity'?state[key]:pct(state[key],2);
 const result=compile(data,state),base=number(data.baseline);
 $('stats').innerHTML=`<div class="stat"><small>Melhor sobrevivência</small><strong>${pct(result.value)}</strong><p>${result.bypass?'comando fixo de referência':result.cost+' portas · circuito informado'}</p></div><div class="stat"><small>Ganho sobre referência</small><strong>${(100*(result.value-base)).toFixed(5)}</strong><p>pontos percentuais</p></div><div class="stat"><small>Busca física completa</small><strong>611</strong><p>canais por custo · até 4 portas</p></div>`;
 const xs=Array.from({length:31},(_,i)=>i*.02/30),s2=[],s4=[],bound=[];
 for(const g of xs){s2.push([g,100*(compile(data,{...state,gamma:g,capacity:2}).value-base)]);s4.push([g,100*(compile(data,{...state,gamma:g,capacity:4}).value-base)]);bound.push([g,100*(upperBound(data,state.p,g,state.q)-base)]);}
 const max=Math.max(.001,...bound.map(x=>x[1]))*1.1;
 $('curve').innerHTML=lineChart([{pts:bound,color:col.o,dash:true},{pts:s4,color:col.g},{pts:s2,color:col.b}],max,state.gamma);
 $('code').textContent=result.bypass?'O melhor programa não ativa o novo circuito.':'Código: '+result.encoding.map(v=>v.toString(2).padStart(2,'0')).join(' / ');
 $('netlist').innerHTML=result.circuit.gates.map(([a,b],i)=>`<div>n${i} = NAND(${wire(a)}, ${wire(b)})</div>`).join('')||'<div>Saída direta: '+wire(result.circuit.output)+'</div>';
 const certified=Math.abs(state.p-.01)<1e-10&&state.gamma<=.01;
 $('scope').textContent=certified?'O ótimo da biblioteca até 4 portas possui certificado exato para p=1%, γ∈[0,1%]. O erro comum q preserva a ordem dos programas; o bypass é comparado depois.':'Busca na biblioteca completa, exibida em ponto flutuante. Este ponto não pertence ao intervalo contínuo certificado; o código Python permite verificação racional exata.';
 const c=causalWitness(state.gamma);
 $('dependence').innerHTML=`<div class="compare"><div><small>Mesmo sinal compartilhado</small><strong>${pct(c.shared,3)}</strong><p>erro após a NAND final</p></div><div><small>Duas cópias independentes</small><strong>${pct(c.independent,3)}</strong><p>mesmas marginais antes da NAND</p></div></div>`;
 const fixed=data.same_function;let bars='';const vals=[fixed.balanced_influences,fixed.sequential_influences];
 for(let i=0;i<4;i++)for(let j=0;j<2;j++){let v=-number(vals[j].gates[i].signed_effect),y=25+i*42+j*14;bars+=`<text x="12" y="${y+9}" font-size="10" fill="${col.m}">${j===0?'porta '+i:''}</text><rect x="72" y="${y}" width="${v/.025*510}" height="10" rx="2" fill="${j===0?col.r:col.g}"/><text x="${80+v/.025*510}" y="${y+9}" font-size="9" fill="${col.m}">${v.toFixed(5)}</text>`;}
 $('influences').innerHTML=svg(720,205,bars,'Dano causado por uma única falha em cada porta, no caso fixo p=1%');
 renderTrace();
}
function wire(i){return ['0','1','m₀','m₁','k'][i]??'n'+(i-5);}
function renderTrace(){const x=Number($('trace-input').value),c=data.same_function.sequential;
 const rows=traces(c,x>>1,x%2,state.gamma);
 $('trace-table').innerHTML='<thead><tr><th>Falhas n₀…n₃</th><th>Sinais n₀…n₃</th><th>Comando</th><th>Probabilidade</th></tr></thead><tbody>'+rows.map(r=>`<tr><td>${r.errors.join(' ')}</td><td>${r.wires.slice(5).join(' ')}</td><td>${r.output?'atualizar':'manter'}</td><td>${r.probability.toPrecision(5)}</td></tr>`).join('')+'</tbody>';
}
async function main(){data=window.CDKA_FAULTY_DATA||await fetch('faulty-update-data.json').then(r=>{if(!r.ok)throw Error('Falha ao carregar certificado');return r.json();});render();
 for(const key of Object.keys(state))$(key).addEventListener('input',e=>{state[key]=Number(e.target.value);render();});$('trace-input').addEventListener('change',renderTrace);
}
main().catch(e=>{$('stats').textContent=e.message;console.error(e);});
