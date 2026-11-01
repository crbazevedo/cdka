/** CDKA T3.C: exact finite-model algebra mirrored from cdka/causal_cut.py.
 * A precommitted protection schedule cannot signal W to the controller.
 * Side-channel mode adds a durable observable copy of the initial sensor Y.
 * Not a universal theory of autonomy or proof of theorem novelty.
 */
export function h2(p){
  if(!(p>=0&&p<=1))throw Error('Probabilities must be in [0,1]');
  if(p===0||p===1)return 0;
  return -p*Math.log2(p)-(1-p)*Math.log2(1-p);
}
export function cutModel({
  cycles=2,budget=2,eta=0,rho=1,nu=0,sideChannel=false
}={}){
  if(!Number.isInteger(cycles)||cycles<1||
     !Number.isInteger(budget)||budget<0||
     !(eta>=0&&eta<=.5&&rho>=0&&rho<=1&&nu>=0&&nu<=.5))
    throw Error('Invalid physical model parameters');
  const ready=budget>=cycles;
  const protections=ready?Math.min(cycles,budget-cycles):0;
  const unprotected=cycles-protections;
  const correlation=(1-2*eta)*(1-2*nu)**cycles;
  const keep=sideChannel?1:(1-rho)**unprotected;
  const tv=ready?keep*correlation:0;
  const success=ready ? 0.5*(1+tv) : 0;
  const initialInfo=1-h2(eta);
  const futureError=(1-correlation)/2;
  const finalInfo=ready?keep*(1-h2(futureError)):0;
  return {ready,protections,unprotected,correlation,keep,tv,success,
          failure:1-success,initialInfo,finalInfo};
}
export function horizonSeries(opts={},maxH=10){
  return Array.from({length:maxH},(_,i)=>({cycles:i+1,...cutModel({...opts,cycles:i+1})}));
}
export function informationTimeline(opts={}){
  const {cycles=2,budget=2,eta=0,rho=1,nu=0,sideChannel=false}=opts;
  const ready=budget>=cycles;
  const protectedCount=ready?Math.min(cycles,budget-cycles):0;
  const points=[];
  for(let step=0;step<=cycles;step++){
    const correlation=(1-2*eta)*(1-2*nu)**step;
    const unprotected=Math.max(0,step-protectedCount);
    const keep=sideChannel?1:(1-rho)**unprotected;
    points.push({
      step,retain:keep,correlation,
      information:keep*(1-h2((1-correlation)/2)),
      viability:.5*(1+keep*correlation)
    });
  }
  return points;
}
