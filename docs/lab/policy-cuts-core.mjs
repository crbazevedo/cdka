/* Finite-model reference kernels: exact algebra, floating display.
   Python Fraction oracles and proof notes are canonical. */
export function channelGeometry(probabilities) {
  if (probabilities.length !== 4 || probabilities.some(p => !(p >= 0 && p <= 1)))
    throw new Error('Four probabilities in [0,1] required');
  const [p00,p01,p10,p11] = probabilities;
  const pairs = [[p00,p10],[p00,p11],[p01,p10],[p01,p11]];
  const values = pairs.map(([x,y]) => Math.abs(y-x));
  const best = Math.max(...values);
  const winner = values.indexOf(best);
  return {fixed: [Math.abs(p00-p10), Math.abs(p01-p11)],
    envelope: best, pairs, winner, success: (1+best)/2,
    xRange: [Math.min(p00,p01),Math.max(p00,p01)],
    yRange: [Math.min(p10,p11),Math.max(p10,p11)]};
}
export function cycleProfiles(p) {
  if (!(p >= 0 && p <= .5)) throw new Error('Repair noise p in [0,1/2]');
  const results=[];
  for(let f0=0;f0<2;f0++) for(let f1=0;f1<2;f1++)
    for(let g0=0;g0<2;g0++) for(let g1=0;g1<2;g1++){
      const f=[f0,f1],g=[g0,g1];
      const q=[0,1].map(w => (g[f[w]]===w?1-p:0)+(g[1-f[w]]===w?p:0));
      results.push({f,g,q});
    }
  return results;
}
export function renewal(p,n) {
  if (!(p>=0 && p<=.5 && Number.isInteger(n) && n>=1)) throw new Error('Invalid horizon/noise');
  const balanced=(1-p)**n;
  const mean=Math.max(.5,balanced);
  return {balanced,robust:balanced,mean,seed:mean,
    crossover: p===0?Infinity:Math.log(.5)/Math.log1p(-p),
    criticalNoise: 1-Math.pow(2,-1/n),
    survivorBits:1,
    liveMass:balanced,
    robustDerivative:-n*(1-p)**(n-1),
    tau:n*p,
    envelopeProfile:balanced>=.5?[balanced,balanced]:[1,0]};
}
export function tolerance(alpha,n){
  if(!(alpha>=0&&alpha<1&&Number.isInteger(n)&&n>0))throw new Error('Invalid risk/horizon');
  return 1-(1-alpha)**(1/n);
}
