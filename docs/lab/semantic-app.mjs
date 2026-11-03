import {rankAt,formalWords,classMap,delayedResponse,nuisanceBound} from './semantic-core.mjs';
const C={green:'#356e54',ochre:'#b68a54',rust:'#a86754',muted:'#849384',line:'#e1e6db',ink:'#233e32'};
const $=id=>document.getElementById(id);let data;
const short=n=>{const s=n.toString();return s.length<=5?s:s[0]+','+s.slice(1,3)+' × 10^'+(s.length-1);};
const name={hold:'manter',correct:'corrigir',refresh:'atualizar',service:'manutenção',prepare:'preparar',check:'verificar'};
function svg(w,h,body,aria){return `<svg class="chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${aria}" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;}
function updateClosure(){
 const key=$('library').value,h=Number($('horizon').value),m=data.plant[key],a=key==='hold'?1:4;
 $('oh').textContent=h;
 const words=formalWords(a,h),rank=rankAt(m.rank_by_word_length,h),classes=rankAt(m.classes_by_word_length,h);
 $('stats').innerHTML=`<div class="stat"><small>Palavras de comprimento ${h}</small><strong>${short(words)}</strong><p>contagem formal de comandos</p></div><div class="stat"><small>Dimensão até esse ponto</small><strong>${rank} / ${m.dimension}</strong><p>${classes} classes de estados</p></div><div class="stat"><small>Certificado completo</small><strong>${m.evaluations}</strong><p>vetores avaliados até fechar</p></div>`;
 const W=740,H=260,L=46,T=20,R=20,B=43,pw=W-L-R,ph=H-T-B,maxH=Math.max(8,h),yMax=20;
 const X=x=>L+pw*x/maxH,Y=y=>T+ph*(1-y/yMax);
 let chart='';for(let k=0;k<=4;k++){let y=5*k;chart+=`<line x1="${L}" x2="${W-R}" y1="${Y(y)}" y2="${Y(y)}" stroke="${C.line}"/><text x="${L-8}" y="${Y(y)+4}" text-anchor="end" font-size="10" fill="${C.muted}">${y}</text>`;}
 for(let k=0;k<=4;k++){let x=maxH*k/4;chart+=`<text x="${X(x)}" y="${H-B+18}" text-anchor="middle" font-size="10" fill="${C.muted}">${Number(x.toFixed(1))}</text>`;}
 const ranks=Array.from({length:maxH+1},(_,i)=>[i,rankAt(m.rank_by_word_length,i)]);
 const logs=Array.from({length:maxH+1},(_,i)=>[i,Math.log10(Number(formalWords(a,i))+1)]);
 for(const [pts,col,dash] of [[ranks,C.green,false],[logs,C.ochre,true]]){
   chart+=`<path d="${pts.map(([x,y],i)=>(i?'L':'M')+X(x)+' '+Y(y)).join(' ')}" fill="none" stroke="${col}" stroke-width="2.8" ${dash?'stroke-dasharray="6 5"':''}/>`;
 }
 chart+=`<line x1="${X(h)}" x2="${X(h)}" y1="${T}" y2="${H-B}" stroke="${C.rust}" stroke-dasharray="3 4"/><circle cx="${X(h)}" cy="${Y(rank)}" r="5" fill="${C.green}" stroke="white" stroke-width="2"/><text x="${L+pw/2}" y="${H-3}" text-anchor="middle" font-size="11" fill="${C.muted}">comprimento da composição</text>`;
 $('growth').innerHTML=svg(W,H,chart,'Crescimento das palavras formais versus estabilização do espaço de continuação');
 const groups=m.classes,cols=key==='hold'?4:5,cw=135,ch=key==='hold'?105:62,rows=Math.ceil(groups.length/cols);let blocks='';
 groups.forEach((g,j)=>{let x=12+(j%cols)*cw,y=15+Math.floor(j/cols)*ch;blocks+=`<rect x="${x}" y="${y}" rx="7" width="${cw-10}" height="${ch-10}" fill="#f0f4e9" stroke="${C.line}"/><text x="${x+8}" y="${y+14}" font-size="9" fill="${C.muted}">classe ${j+1} · ${g.length} estados</text>`;g.forEach((s,i)=>{let px=x+12+(i%10)*10,py=y+29+Math.floor(i/10)*12;blocks+=`<circle cx="${px}" cy="${py}" r="3.3" fill="${C.green}"><title>microestado ${s}</title></circle>`;});});
 $('classes').innerHTML=svg(700,rows*ch+20,blocks,'Classes finais de estados do modelo, após fechamento');
 $('witness-list').innerHTML='<h3>Palavras retidas na base</h3><div class="witnesses">'+m.basis_words.map(w=>'<div>'+(w.word.length?w.word.map(x=>name[x]||x).join(' → '):'sobrevivência atual')+'</div>').join('')+'</div>';
}
function updateTrace(){
 const word=$('sequence').value.split(','),traces=[delayedResponse(0,word),delayedResponse(1,word)],labels=['x','y','p','q'];let out='';const W=740,H=235,L=70,dx=580/word.length;
 traces.forEach((t,row)=>{let y=55+row*110;t.trace.forEach((state,i)=>{let x=L+i*dx;if(i){out+=`<line x1="${x-dx+25}" y1="${y}" x2="${x-25}" y2="${y}" stroke="${C.muted}" stroke-width="1.8"/><text x="${x-dx/2}" y="${y-15}" text-anchor="middle" font-size="11" fill="${C.muted}">${name[word[i-1]]}</text>`;}
 out+=`<circle cx="${x}" cy="${y}" r="23" fill="${state<0?C.rust:C.green}"/><text x="${x}" y="${y+5}" text-anchor="middle" font-size="15" fill="white">${state<0?'×':labels[state]}</text>`;});out+=`<text x="${W-10}" y="${y+5}" text-anchor="end" font-size="11" fill="${C.muted}">${t.survives?'vivo':'falha'}</text>`;});
 $('trace').innerHTML=svg(W,H,out,'Trajetórias de x e y sob a sequência escolhida');
 $('trace-explanation').textContent=traces[0].survives!==traces[1].survives?'A composição separa x e y: qualquer interface que preserve este teste precisa conservar essa distinção. O comando inicial, isolado, não mostrava o conflito.':'Nesta sequência, os dois resultados coincidem. Isso não prova equivalência: preparar → verificar é um teste permitido que os separa.';
}
function updateNuisance(){let b=Number($('nuisance-bits').value);$('ob').textContent=b;let v=nuisanceBound(b);$('nuisance').innerHTML=`<div class="stats"><div class="stat"><small>Estados físicos da família</small><strong>${short(v.states)}</strong><p>2 × 2<sup>${b}</sup></p></div><div class="stat"><small>Direções relevantes</small><strong>${v.rank}</strong><p>independem do fator auxiliar</p></div><div class="stat"><small>Vetores gerados no núcleo</small><strong>${v.tests}</strong><p>prova antes da expansão</p></div></div>`;}
async function start(){data=window.CDKA_SEMANTIC_DATA||await fetch('semantic-certificate.json').then(r=>{if(!r.ok)throw Error('Certificado indisponível');return r.json();});updateClosure();updateTrace();updateNuisance();
 for(const id of ['library','horizon'])$(id).addEventListener('input',updateClosure);
 $('sequence').addEventListener('input',updateTrace);$('nuisance-bits').addEventListener('input',updateNuisance);
 document.querySelectorAll('[data-tab]').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===btn));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('active',x.id==='panel-'+btn.dataset.tab));}));
}
start().catch(err=>{$('stats').textContent=err.message;console.error(err);});
