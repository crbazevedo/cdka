/** Browser projection of the exact rational frontier, not a numerical optimizer. */
export function frontier(data,p,q,K){
 if(!(p>=0&&p<=.5&&q>=0&&q<=.5&&Number.isInteger(K)&&K>=0&&K<=4))throw Error('invalid domain');
 const c=data.certificate,a=c.a.value,b=c.b.value,D=c.total_margin.value,base=c.baseline.value;
 const raw=K<2?0:K<4?a*(1-p)-b*p:a*(1-p)**2-b*p*p;
 const gain=Math.max(0,(1-2*q)*raw-q*D);
 return {value:base+gain,gain,raw,usesBypass:gain<=1e-15,base};
}
export function gateProgram(K,p=0){
 if(K<2)return {encoding:[0,0,0],gates:[],truth:255};
 if(K<4||p===0)return {encoding:[1,0,0],gates:[[170,170,85],[85,204,187]],truth:187};
 return {encoding:[3,0,0],gates:[[170,170,85],[85,204,187],[187,187,68],[68,240,191]],truth:191};
}
export function runCircuit(program,m,k){
 const x=2*m+k,values=new Map([0,255,204,240,170].map(t=>[t,(t>>x)&1]));
 for(const [a,b,t]of program.gates)values.set(t,1-(values.get(a)&values.get(b)));
 return values.get(program.truth);
}
