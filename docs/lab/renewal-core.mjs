export function propagate(c,rule,steps){
  if(!Number.isInteger(steps)||steps<0||steps>100)throw Error('Horizonte entre 0 e 100');
  const kernel=c.browser.kernels[rule];if(!kernel)throw Error('Regra desconhecida');
  let law=Array(kernel.length).fill(0);for(const [i,w]of c.browser.initial)law[i]=w;
  const curve=[law.reduce((a,b)=>a+b,0)];
  for(let t=0;t<steps;t++){const next=Array(kernel.length).fill(0);for(let i=0;i<law.length;i++)for(const[j,p]of kernel[i])next[j]+=law[i]*p;law=next;curve.push(law.reduce((a,b)=>a+b,0));}
  return{curve,law};
}
export function value(x){return typeof x==='object'&&x!==null?x.value:Number(x);}
export function namedRule(r){return{renew:'Renovar sempre',retain:'Reter os bits',after_service:'Renovar após manutenção',after_skip:'Renovar após não manter'}[r]||r;}
