// Browser mirror; exact rational and continuum proof lives in Python.
import {DATA} from './joint-compilation-data.mjs';
export {DATA};
export function channel(x,p){
 if(!Number.isInteger(x)||x<0||x>3||!(p>=0&&p<=.5))throw Error('Invalid two-bit channel');
 return [0,1,2,3].map(r=>{const d=((x^r)&1)+(((x^r)>>1)&1);return p**d*(1-p)**(2-d);});
}
export function compile(p,L=3,balance=4,injective=false){
 if(!Number.isInteger(L)||L<1||!DATA.tables[String(balance)])throw Error('Library/balance');
 const t=DATA.tables[String(balance)],n=t.ids.length;
 let best=null;
 const rows=[0,1,2,3].map(x=>channel(x,p));
 for(let code=0;code<64;code++){
  const E=[Math.floor(code/16),Math.floor(code/4)%4,code%4];
  const states=new Set(E).size;if(injective&&states!==3)continue;
  const mass=[0,1,2,3].map(r=>t.ids.map((_,j)=>E.reduce((v,x,y)=>v+rows[x][r]*t.weighted[y][j],0)));
  for(let mask=1;mask<(1<<n);mask++){
   const subset=t.ids.map((_,i)=>i).filter(i=>mask&(1<<i));if(subset.length>L)continue;
   const choices=mass.map(row=>subset.reduce((a,b)=>row[b]>row[a]+1e-16?b:a));
   const value=choices.reduce((v,x,r)=>v+mass[r][x],0);
   const decoder=choices.map(i=>t.ids[i]),templates=new Set(decoder).size;
   if(!best||value>best.value+1e-14||
      (Math.abs(value-best.value)<1e-14&&(templates<best.templates||templates===best.templates&&states<best.states)))
    best={value,encoder:E,decoder,templates,states,balance};
  }
 }
 return best;
}
export function funded(p,B=4,price=1){
 const options=[];
 for(let L=1;L<=3;L++){
  const fee=price*(L-1),balance=B-fee;if(balance<0)continue;
  options.push({...compile(p,L,balance),slots:L,fee});
 }
 const best=options.reduce((a,b)=>b.value>a.value+1e-14?b:a);
 return {best,options};
}
export function information(E,p){
 const rows=E.map(x=>channel(x,p));
 const marginal=[0,1,2,3].map(r=>rows.reduce((v,row)=>v+row[r]/3,0));
 return rows.reduce((v,row)=>v+row.reduce((s,q,r)=>s+(q?q/3*Math.log2(q/marginal[r]):0),0),0);
}
export function certifiedValue(p){return Math.max(...DATA.phase.map(c=>c[0]+p*c[1]+p*p*c[2]));}
