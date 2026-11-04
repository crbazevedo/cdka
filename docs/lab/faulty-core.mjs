/* Floating-point rendering mirror. Exact optimization/certificates live in Python. */
export const number=x=>typeof x==='number'?x:x.value;
export function channel(profile,gamma,q=0){
 const d=profile[0].length-1;
 return profile.map(row=>q+(1-2*q)*row.reduce((v,n,k)=>v+n*gamma**k*(1-gamma)**(d-k),0));
}
export function compile(data,{p=.01,gamma=.001,q=0,capacity=4}={}){
 if(!(p>=0&&p<=.5&&gamma>=0&&gamma<=.5&&q>=0&&q<=.5)||!Number.isInteger(capacity)||capacity<0||capacity>4)throw Error('Invalid settings');
 const T=data.payoff_table.map(y=>y.map(k=>k.map(number)));
 const weights=[];let base=0;
 for(let y=0;y<3;y++){
  base+=T[y][0][0]+T[y][1][0];
  for(let e=0;e<4;e++)weights.push(Array.from({length:8},(_,x)=>{
   const bits=e^(x>>1),d=(bits&1)+((bits>>1)&1);
   return p**d*(1-p)**(2-d)*(T[y][x%2][1]-T[y][x%2][0]);
  }));
 }
 let best={value:-Infinity};
 for(const record of data.channels){
  const cost=record.circuit.gates.length;if(cost>capacity)continue;
  const h=channel(record.profile,gamma,q);let value=base;const encoding=[];
  for(let y=0;y<3;y++){
   let max=-Infinity,chosen=0;
   for(let e=0;e<4;e++){const score=weights[4*y+e].reduce((v,w,x)=>v+w*h[x],0);if(score>max+1e-16){max=score;chosen=e;}}
   value+=max;encoding.push(chosen);
  }
  if(value>best.value+1e-15||(Math.abs(value-best.value)<1e-15&&cost<best.cost))best={value,cost,encoding,circuit:record.circuit,profile:record.profile};
 }
 const baseline=number(data.baseline);return {...best,updateValue:best.value,value:Math.max(baseline,best.value),bypass:baseline>=best.value-1e-15,baseline};
}
export function upperBound(data,p,gamma,q=0){
 const T=data.payoff_table.map(y=>y.map(k=>k.map(number)));
 const a=T[0][0][0]-T[0][0][1];
 const b=T[1][0][1]-T[1][0][0]+T[2][0][1]-T[2][0][0];
 let D=0;for(const y of T)for(const k of y)D+=k[1]-k[0];
 const G=Math.max(0,a*(1-p)**2-b*p*p),e=gamma+q-2*gamma*q;
 return number(data.baseline)+Math.max(0,(1-2*e)*G-e*D);
}
export function causalWitness(g){return {shared:2*g*(1-g),independent:g+(1-2*g)*(2*g-g*g)};}
export function traces(circuit,word,k,gamma){
 const d=circuit.gates.length,result=[];
 for(let mask=0;mask<2**d;mask++){
  const wires=[0,1,word&1,word>>1,k],errors=[];
  for(let i=0;i<d;i++){const [a,b]=circuit.gates[i],e=(mask>>i)&1;errors.push(e);wires.push((1-(wires[a]&wires[b]))^e);}
  const count=errors.reduce((a,b)=>a+b,0);
  result.push({errors,wires,output:wires[circuit.output],probability:gamma**count*(1-gamma)**(d-count)});
 }return result;
}
