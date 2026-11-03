import{frontier,gateProgram,runCircuit}from'./physical-update-core.mjs';
const $=x=>document.getElementById(x),color={g:'#356e54',o:'#b68a54',t:'#52685b',line:'#dce1d6',rust:'#a86754'},S={p:.01,q:0,K:4};let data;
const num=(n,d=4)=>Number(n).toFixed(d),pct=n=>(100*n).toFixed(2)+'%';
const svg=(w,h,s,label)=>`<svg class="chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">${s}</svg>`;
function draw(){
 for(const k of ['p','q','K'])$('o'+k).textContent=k==='K'?S[k]:pct(S[k]);
 const f=frontier(data,S.p,S.q,S.K),w=gateProgram(S.K,S.p);
 $('stats').innerHTML=`<div class="stat"><small>Melhor sobrevivência</small><strong>${num(100*f.value)}%</strong><p>massa original, sem renormalização</p></div><div class="stat"><small>Ganho realizável</small><strong>${num(100*f.gain)} pp</strong><p>sobre o mesmo comando fixo</p></div><div class="stat"><small>Política selecionada</small><strong>${f.usesBypass?'Fixa':w.gates.length+' portas'}</strong><p>${f.usesBypass?'não ativar a escrita':'uma atualização contingente'}</p></div>`;
 const W=740,H=260,L=62,T=20,R=15,B=40,pw=W-L-R,ph=H-T-B;const X=p=>L+p/.12*pw,Y=g=>T+ph-g/.03*ph;let s='';
 for(let i=0;i<=3;i++){const v=.01*i;s+=`<line x1="${L}" x2="${W-R}" y1="${Y(v)}" y2="${Y(v)}" stroke="${color.line}"/><text x="${L-8}" y="${Y(v)+4}" text-anchor="end" font-size="10" fill="${color.t}">${v.toFixed(2)}</text>`;}
 for(let i=0;i<=4;i++){const p=.03*i;s+=`<text x="${X(p)}" y="${H-B+16}" text-anchor="middle" font-size="10" fill="${color.t}">${(100*p).toFixed(0)}%</text>`;}
 for(const [K,c]of[[2,color.g],[4,color.o]]){const pts=Array.from({length:121},(_,i)=>[i/1000,frontier(data,i/1000,S.q,K).gain*100]);s+=`<path d="${pts.map(([x,y],i)=>(i?'L':'M')+X(x)+' '+Y(y)).join(' ')}" stroke="${c}" stroke-width="3" fill="none"/>`;}
 s+=`<line x1="${X(S.p)}" x2="${X(S.p)}" y1="${T}" y2="${H-B}" stroke="${color.rust}" stroke-dasharray="4 4"/><text x="${L+pw/2}" y="${H-2}" text-anchor="middle" font-size="11" fill="${color.t}">erro de transporte p</text>`;
 $('curve').innerHTML=svg(W,H,s,'Ganho certificado por erro de transporte e capacidade do circuito');
 let circ='';const pos=new Map([[204,[45,95]],[240,[45,175]],[170,[45,255]],[0,[45,15]],[255,[45,335]]]);
 for(const[t,label]of[[204,'m₀'],[240,'m₁'],[170,'k']]){const[x,y]=pos.get(t);circ+=`<circle cx="${x}" cy="${y}" r="16" fill="${color.g}"/><text x="${x}" y="${y+4}" text-anchor="middle" font-size="12" fill="white">${label}</text>`;}
 w.gates.forEach(([a,b,t],i)=>{const x=165+i*140,y=145+(i%2)*70;for(const input of[a,b]){const[x0,y0]=pos.get(input);circ+=`<path d="M${x0+18} ${y0}C${(x+x0)/2} ${y0} ${(x+x0)/2} ${y} ${x-32} ${y}" stroke="${color.line}" stroke-width="2" fill="none"/>`;}circ+=`<rect x="${x-32}" y="${y-19}" width="64" height="38" rx="8" fill="#eef2e8" stroke="${color.g}"/><text x="${x}" y="${y+4}" text-anchor="middle" font-size="11" fill="${color.g}">NAND</text><text x="${x}" y="${y-27}" text-anchor="middle" font-size="10" fill="${color.t}">n${i}</text>`;pos.set(t,[x+20,y]);});
 if(!w.gates.length)circ+=`<text x="230" y="170" font-size="17" fill="${color.t}">Nenhuma atualização contingente útil</text>`;
 else {const[x,y]=pos.get(w.truth);circ+=`<text x="${x+36}" y="${y+4}" font-size="13" fill="${color.g}">bit</text>`;}
 $('circuit').innerHTML=svg(800,320,circ,'Circuito físico de atualização NAND');
 $('circuit-note').textContent=f.usesBypass?'A configuração atual prefere o comando fixo. O circuito exibido é a alternativa da biblioteca, mas seu benefício não compensa o canal de escrita.':`Código dos diagnósticos: ${w.encoding.map(x=>x.toString(2).padStart(2,'0')).join(' / ')}. ${w.gates.length===4?'A redundância do registro protege a distinção mais custosa.':'Um bit diagnóstico e a observação atual bastam para esta regra.'}`;
 $('truth').innerHTML='<table><thead><tr><th>m₁m₀</th><th>Síndrome k</th><th>Bit antes do erro q</th><th>Comando</th></tr></thead><tbody>'+Array.from({length:8},(_,x)=>{const m=Math.floor(x/2),k=x%2,b=runCircuit(w,m,k);return `<tr><td>${m.toString(2).padStart(2,'0')}</td><td>${k}</td><td>${b}</td><td>${b?'Atualizar':'Manter'}</td></tr>`;}).join('')+'</tbody></table>';
}
async function init(){data=window.CDKA_UPDATE_DATA||await fetch('physical-update-data.json').then(r=>{if(!r.ok)throw Error('certificate missing');return r.json();});for(const k of['p','q','K'])$(k).addEventListener('input',e=>{S[k]=Number(e.target.value);draw();});draw();}
init().catch(e=>{$('stats').textContent=e.message;console.error(e);});
