import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import * as kernel from '../docs/lab/core-interfaces.mjs';

const {MODEL,U,W,DEFAULT_A,LABELS,exact,asNumber,compareExact,lawAfter,payoff,evaluateWitness,assessValues} = kernel;
const fixture = JSON.parse(readFileSync(new URL('../docs/data/core-interface-witness.json',import.meta.url),'utf8'));
const html = readFileSync(new URL('../docs/lab/core_interfaces.html',import.meta.url),'utf8');
const embedded = JSON.parse(html.match(/<script id="certified-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const near = (actual,expected) => assert.ok(Math.abs(actual-expected)<2e-14,`${actual} != ${expected}`);
const plain = value => JSON.parse(JSON.stringify(value));

test('exact arithmetic, input boundaries and finite presentation',()=>{
  assert.equal(exact('6/10'),'3/5');
  assert.equal(exact(.6),'3/5');
  assert.equal(exact('-2/-4'),'1/2');
  assert.equal(exact('1e-3'),'1/1000');
  assert.equal(exact('-0.500'),'-1/2');
  assert.equal(compareExact('1/3','333333333333333333/1000000000000000000'),1);
  for(const bad of [NaN,Infinity,-Infinity,{},null,'','not a fraction','1/0']) assert.throws(()=>evaluateWitness(bad));
  for(const bad of ['-1/1000','1001/1000']) assert.throws(()=>evaluateWitness(bad));
  const huge='1'+'0'.repeat(400);
  near(asNumber(huge+'/'+huge),1);
  assert.throws(()=>assessValues([['2','0','0']]));
  assert.throws(()=>lawAfter(['1'],MODEL.operators.R));
});

test('model and default certificate independently agree with frozen Python output',()=>{
  assert.equal(fixture.schema,'cdka.core-interface-witness/v1');
  assert.deepEqual(MODEL.states,fixture.model.states);
  assert.deepEqual(MODEL.emission,fixture.model.emission);
  assert.deepEqual(MODEL.operators,fixture.model.operators);
  assert.deepEqual(MODEL.feature,fixture.model.feature);
  assert.deepEqual(MODEL.terminal,fixture.model.terminal);
  assert.deepEqual(U,fixture.selectors.common_reset_control.kernel_U);
  assert.deepEqual(W,fixture.deterministic_policy_cover.kernel_W);
  const result=evaluateWitness();
  for(const [key,value] of Object.entries(fixture.decision_reversal)){
    if(key==='actual'||key==='false_decision'){
      for(const [field,expected] of Object.entries(value)) assert.deepEqual(result[key][field],expected,`${key}.${field}`);
    }else assert.deepEqual(result[key],value,key);
  }
  assert.deepEqual(result.full_class.actual_values,fixture.deterministic_policy_cover.actual_values);
  assert.deepEqual(result.two_step_SU,fixture.two_step_positive_control.selected_values.SU);
  assert.equal(DEFAULT_A,embedded.a);
  for(const key of ['preparations','old_signatures','actual_values','false_fresh_reconstructions','false_values']){
    assert.deepEqual(embedded[key],fixture.decision_reversal[key]);
  }
  assert.deepEqual(embedded.actual_gate,result.actual.gate.feasible_programs);
  assert.deepEqual(embedded.false_gate,result.false_decision.gate.feasible_programs);
});

test('matrix evaluations match independent affine formulas over the whole interval',()=>{
  for(let n=0;n<=40;n++){
    const a=`${n}/40`,result=evaluateWitness(a),norm=row=>row.map(exact);
    assert.deepEqual(result.full_class.actual_values,[
      norm([a,`${40-n}/40`,`${80-n}/80`,`${n}/80`]),
      norm([a,`${40-n}/40`,`${40-n}/40`,a])
    ]);
    assert.deepEqual(result.old_signatures,[exact(`${n-20}/40`),exact(`${n-20}/40`)]);
    assert.equal(result.false_prediction_gap,exact(`${n}/80`));
    assert.deepEqual(result.two_step_SU,[exact(`${40+n}/80`),exact(`${40+n}/80`)]);
    assert.deepEqual(result.old_family_contains,[true,n===0]);
    for(const law of [...result.preparations,...result.post_U]) assert.equal(payoff(law,['1','1','1']),'1');
    // U renews the output: each post-U law is an emission mixture.
    for(const law of result.post_U) assert.equal(law[0],law[1]);
  }
});

test('boundary ties and the exact joint gate remain truthful',()=>{
  const zero=evaluateWitness(0),one=evaluateWitness(1),tie=evaluateWitness('4/7');
  assert.deepEqual(zero.actual.minimax_programs,['S','U']);
  assert.deepEqual(zero.actual.maximin_programs,['S','U']);
  assert.deepEqual(zero.preparations,zero.false_fresh_reconstructions);
  assert.deepEqual(one.actual.minimax_programs,['R']);
  assert.equal(one.actual.maximin_value,'1');
  assert.deepEqual(tie.actual.minimax_programs,['R','U']);
  assert.equal(tie.actual.minimax_regret,'1/7');
  assert.deepEqual(tie.actual.maximin_programs,['R']);
  assert.deepEqual(evaluateWitness('2/3').false_decision.minimax_programs,['R','U']);
  assert.deepEqual(evaluateWitness('2/3').actual.gate.feasible_programs,['R']);
  for(let n=0;n<=60;n++){
    const result=evaluateWitness(`${n}/60`);
    const actual={R:n>=40,S:n<=12,U:n<=20};
    const reconstructed={R:n>=40,S:n<=12,U:n<=40};
    assert.deepEqual(result.actual.gate.feasible_programs,LABELS.filter(x=>actual[x]),`actual a=${n}/60`);
    assert.deepEqual(result.false_decision.gate.feasible_programs,LABELS.filter(x=>reconstructed[x]),`false a=${n}/60`);
  }
});

test('dropping W preserves the one-step objectives but not all tied identities',()=>{
  const responseR=MODEL.states.map((_,i)=>payoff(MODEL.operators.R[i]));
  const responseW=MODEL.states.map((_,i)=>payoff(W[i]));
  assert.deepEqual(responseR,['1','1','0']);
  assert.deepEqual(responseW,['1','0','0']);
  for(let n=0;n<=30;n++){
    const result=evaluateWitness(`${n}/30`);
    assert.equal(result.full_class.dominance,true);
    for(const field of ['minimax_regret','maximin_value','informed_values']){
      assert.deepEqual(result.actual[field],result.full_class.actual[field]);
    }
    assert.deepEqual(result.actual.gate.feasible_programs,result.full_class.actual.gate.feasible_programs);
  }
  const result=evaluateWitness();
  assert.deepEqual(result.actual.informed_programs[1],['R']);
  assert.deepEqual(result.full_class.actual.informed_programs[1],['R','W']);
});

test('R/S continuations retain value sufficiency despite failure of the old law family',()=>{
  const result=evaluateWitness();
  let laws=result.preparations;
  const visit=(pair,depth)=>{
    assert.equal(payoff(pair[0]),payoff(pair[1]));
    if(!depth)return;
    for(const letter of ['R','S'])visit(pair.map(law=>lawAfter(law,MODEL.operators[letter])),depth-1);
  };
  visit(laws,4);
  assert.notEqual(laws[1][0],laws[1][1]);
  assert.notEqual(payoff(lawAfter(laws[0],U)),payoff(lawAfter(laws[1],U)));
});

test('two-step and randomized controls expose the exact contract boundaries',()=>{
  const result=evaluateWitness();
  const kernels={...MODEL.operators,U,W},labels=['R','S','U','W'];
  const words=labels.flatMap(a=>labels.map(b=>a+b));
  const values=result.preparations.map(law=>words.map(word=>payoff(lawAfter(lawAfter(law,kernels[word[0]]),kernels[word[1]]))));
  const decision=assessValues(values,words);
  assert.deepEqual(words,fixture.two_step_positive_control.labels);
  assert.deepEqual(values,fixture.two_step_positive_control.actual_values);
  assert.deepEqual(decision.informed_values,['17/20','4/5']);
  assert.equal(decision.worst_regrets[words.indexOf('SU')],'1/20');
  assert.deepEqual(decision.gate.feasible_programs,['SU','WU']);
  // W is dominated only for the one-step terminal response, not before suffix U.
  assert.equal(values[0][words.indexOf('WU')],'17/20');
  assert.equal(values[0][words.indexOf('RU')],'7/10');
  // The added random program (2/3)R+(1/3)U has values 19/30 and 8/15.
  // Compare with the original informed envelope; it improves .1 to 1/15.
  near(.7-19/30,1/15);
  near(.6-8/15,1/15);
  assert.ok(1/15<asNumber(result.actual.minimax_regret));
});

function mockDocument(){
  const element=()=>({textContent:'',innerHTML:'',value:'',hidden:true,className:'',attributes:{},listeners:{},dataset:{},
    setAttribute(key,value){this.attributes[key]=value;},addEventListener(name,handler){this.listeners[name]=handler;}});
  const elements=new Map([...html.matchAll(/\bid="([^"]+)"/g)].map(match=>[match[1],element()]));
  elements.get('certified-data').textContent=JSON.stringify(embedded);
  const buttons=[...html.matchAll(/<button[^>]+data-a="([^"]+)"/g)].map(match=>Object.assign(element(),{dataset:{a:match[1]}}));
  return {getElementById:id=>elements.get(id),querySelectorAll:()=>buttons,buttons};
}

test('DOM smoke renders exact defaults, ties, endpoint controls and accessible laws',()=>{
  const doc=mockDocument(),errors=[];
  const source=html.match(/<script type="module" id="lab-script">([\s\S]*?)<\/script>/)[1]
    .replace(/^import .*?;\s*$/m,'').replace('export function mount','function mount');
  const context={...kernel,document:doc,console:{error:error=>errors.push(error)}};
  vm.createContext(context);vm.runInContext(source,context);
  const get=id=>doc.getElementById(id);
  assert.deepEqual(errors,[]);
  assert.equal(get('a-exact').textContent,'3/5');
  assert.equal(get('actual-minimax').textContent,'R');
  assert.equal(get('actual-regret').textContent,'regret = 1/10');
  assert.equal(get('false-minimax').textContent,'U');
  assert.equal(get('false-badge').textContent,'Aprovação indevida');
  assert.equal((get('laws').innerHTML.match(/role="img"/g)||[]).length,3);
  assert.match(get('laws').innerHTML,/aria-label="C · massa reunida/);
  assert.equal((get('values-body').innerHTML.match(/<tr/g)||[]).length,4);
  assert.match(get('two-step-note').textContent,/4\/5/);
  doc.buttons.find(button=>button.dataset.a==='4/7').listeners.click();
  assert.equal(get('actual-minimax').textContent,'R / U');
  assert.equal(get('a-exact').textContent,'4/7');
  get('a').value='601';get('a').listeners.input();
  assert.equal(get('a-exact').textContent,'601/1000');
  for(const button of doc.buttons){
    button.listeners.click();
    assert.ok(!/NaN|Infinity|undefined/.test(get('values-body').innerHTML+get('laws').innerHTML));
    assert.equal(button.attributes['aria-pressed'],'true');
  }
  doc.buttons[0].listeners.click();
  assert.equal(get('prediction-gap').textContent,'0');
  assert.match(get('law-explanation').textContent,/não há separação/);
});

test('page preserves the observation, horizon, cost and implementation boundaries',()=>{
  for(const phrase of ['uma operação de continuação','preparação igualmente debitada','sem receber seu nome','O(A₀) = O(B) = 0','gramática','sem alegação de realização em hardware','A escolha entre programas é determinística','um passo','não preserva todas as identidades empatadas']){
    assert.ok(html.includes(phrase),phrase);
  }
  assert.ok(html.includes('article')||html.includes('Artigo'));
  assert.ok(!/https?:\/\//.test(html),'No external fonts, scripts or trackers');
  assert.ok(!/\bfetch\s*\(/.test(html));
  assert.match(html,/<label for="a">/);
});
