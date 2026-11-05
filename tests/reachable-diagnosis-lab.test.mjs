import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(new URL('../docs/lab/reachable_diagnosis.html', import.meta.url), 'utf8');
const canonical = JSON.parse(readFileSync(new URL('../docs/data/reachable-diagnosis-results.json', import.meta.url), 'utf8'));
const embedded = html.match(/<script id="certified-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const source = html.match(/<script id="lab-script">([\s\S]*?)<\/script>/)[1];
const context = {document:{getElementById(id){return id === 'certified-data' ? {textContent:embedded} : null;}}};
vm.createContext(context);
vm.runInContext(source, context);
const model = context.RI;
const fixture = canonical.fixture;
const near = (actual, expected, tolerance=3e-14) => assert.ok(Math.abs(actual-expected) <= tolerance, String(actual)+' != '+String(expected));
const plain = value => JSON.parse(JSON.stringify(value));
const allowedWords = assessment => plain(assessment.allowed.map(p=>p.word));

test('offline payload matches the exact physical fixture and its contract', () => {
  assert.deepEqual(plain(model.data), {contract:canonical.contract,fixture:canonical.fixture});
  assert.equal(fixture.histories.length, 4);
  assert.equal(fixture.plans.length, 96);
  assert.equal(new Set(fixture.plans).size, 96);
  assert.deepEqual(fixture.histories, ['DD','DR','RD','RR']);
  for(const word of fixture.plans){
    assert.equal([...word].filter(x=>x!=='M').length, 4);
    assert.ok([...word].filter(x=>x==='M').length <= 1);
  }
  assert.ok(!/<script[^>]+\bsrc=/.test(html));
  assert.ok(!/\bfetch\s*\(/.test(source));
  assert.ok(!/__REACHABLE_DATA__/.test(html));
});

test('rational conversion handles large certificates without infinity division', () => {
  near(model.fraction('3/4'), .75);
  near(model.fraction('-1/4'), -.25);
  const power = '1'+'0'.repeat(400);
  near(model.fraction(power+'/'+power), 1);
  near(model.fraction(('3'+'0'.repeat(400))+'/'+('4'+'0'.repeat(400))), .75);
  assert.throws(()=>model.fraction('1/0'));
  assert.throws(()=>model.analyze(-.1));
  assert.throws(()=>model.analyze(.51));
  assert.throws(()=>model.assess(.1,-.1,.84,'DRDDM'));
  assert.throws(()=>model.assess(.1,.003,.84,'unknown'));
});

test('affine sensor display reproduces all exact zero and reference responses', () => {
  const zero = model.analyze(0), reference = model.analyze(.1);
  for(let i=0;i<fixture.histories.length;i++){
    for(let j=0;j<fixture.plans.length;j++){
      near(zero.values[i][j], model.fraction(fixture.values_sensor_zero[i][j]));
      near(reference.values[i][j], model.fraction(fixture.values[i][j]));
    }
  }
  near(reference.freeRadius, model.fraction(fixture.certificate.prediction.free_radius));
  near(reference.meanRadius, model.fraction(fixture.certificate.prediction.uniform_law_radius));
});

test('same-history regret and the two robust objectives match their certificates', () => {
  const a = model.analyze(.1), c = fixture.certificate;
  assert.equal(a.minimax.word, 'DRDDM');
  assert.equal(a.maximin.word, 'DDDDM');
  assert.equal(a.nominal.word, 'DDDDM');
  assert.equal(a.minimax.optimalAt.filter(Boolean).length, 0);
  near(a.minimax.regret, model.fraction(c.decision.minimax_regret));
  near(a.maximin.lower, model.fraction(c.decision.maximin_value));
  for(const p of a.plans){
    near(p.lower, model.fraction(c.prediction.lower[p.index]));
    near(p.upper, model.fraction(c.prediction.upper[p.index]));
    near(p.regret, model.fraction(c.decision.plan_regrets[p.index]));
    for(let i=0;i<4;i++){
      near(p.losses[i], a.oracle[i]-p.values[i]);
    }
  }
  near(a.minimax.regret,.0025321961178476887);
  near(a.minimax.lower,.8491834489516084);
  near(a.maximin.lower,.8500277369367224);
});

test('joint gates distinguish the compromise, impossibility and fidelity-first choice', () => {
  const base = model.assess(.1,.003,.84,'DRDDM');
  assert.equal(base.selectedFits, true);
  assert.deepEqual(allowedWords(base), ['DRDDM']);
  const impossible = model.assess(.1,.003,.85,'DRDDM');
  assert.equal(impossible.selectedFits, false);
  assert.deepEqual(allowedWords(impossible), []);
  const relaxed = model.assess(.1,.005,.85,'DDDDM');
  assert.equal(relaxed.selectedFits, true);
  assert.deepEqual(allowedWords(relaxed), ['DDDDM']);
  assert.equal(model.assess(.1,.003,.84,'DDDDM').selectedFits,false);
});

test('weaker acquisition shrinks regret while the absolute fidelity gate remains active', () => {
  const a0 = model.analyze(0);
  for(const eta of [0,.1,.25,.495,.5]){
    const a=model.analyze(eta),scale=1-2*eta;
    assert.equal(a.minimax.word, 'DRDDM');
    assert.equal(a.maximin.word, 'DDDDM');
    near(a.freeRadius,scale*a0.freeRadius);
    for(const p of a.plans){
      near(p.regret,scale*a0.plans[p.index].regret);
      assert.ok(p.upper <= 1-eta+3e-14);
      assert.ok(p.lower >= -3e-14);
    }
  }
  const noSignal=model.assess(.5,.003,.84,'DRDDM');
  assert.equal(noSignal.selected.regret,0);
  assert.equal(noSignal.selected.lower,.5);
  assert.equal(noSignal.allowed.length,0);
  const noTaskFloor=model.assess(.5,0,.5,'DRDDM');
  assert.equal(noTaskFloor.allowed.length,96);
});

test('acquisition and history costs are retained under a common reservation', () => {
  const reserve=fixture.costs.reservation;
  assert.equal(reserve.sensor_readings,1);
  assert.equal(reserve.installed_sensors,1);
  assert.equal(reserve.installed_nands,6);
  assert.equal(reserve.retained_cells,3);
  assert.equal(reserve.clock_intervals,9);
  for(const h of fixture.histories){
    for(const word of fixture.plans){
      const cost=fixture.costs.executed[h][word];
      const r=[...h+word].filter(x=>x==='R').length;
      const m=[...word].filter(x=>x==='M').length;
      assert.equal(cost.sensor_readings,1);
      assert.equal(cost.cell_writes,3*(1+r));
      assert.equal(cost.cell_channel_updates,3*(1+h.length+4));
      assert.equal(cost.voter_evaluations,r+m+1);
      assert.equal(cost.nand_evaluations,6*(r+m+1));
      assert.equal(cost.prepaid_service_slots,m);
      assert.equal(cost.clock_intervals,1+h.length+word.length+1);
      for(const key of Object.keys(reserve)){
        assert.ok(cost[key] <= reserve[key]);
      }
    }
  }
  const ranges=plain(model.costs('DRDDM'));
  assert.deepEqual(ranges.find(c=>c.key==='nand_evaluations'),{key:'nand_evaluations',lower:18,upper:30,reserved:48});
  assert.deepEqual(ranges.find(c=>c.key==='cell_writes'),{key:'cell_writes',lower:6,upper:12,reserved:21});
});

test('all selected plans and parameter endpoints produce finite accessible SVGs', () => {
  for(const word of fixture.plans){
    const assessment=model.assess(.1,.003,.84,word);
    for(const render of [model.valueSVG,model.scatterSVG]){
      const svg=render(assessment,340);
      assert.match(svg,/^<svg[\s\S]*<\/svg>$/);
      assert.ok(svg.includes('role="img"')&&svg.includes('<desc>'));
      assert.ok(!/NaN|Infinity|undefined/.test(svg));
    }
  }
  for(const eta of [0,.1,.5]){
    for(const delta of [0,.003,.03]){
      for(const tau of [.5,.85,.95]){
        const assessment=model.assess(eta,delta,tau,'DRDDM');
        for(const width of [340,640]){
          const svg=model.scatterSVG(assessment,width);
          assert.ok(!/NaN|Infinity|undefined/.test(svg));
          assert.ok(svg.includes('Regret máximo (p.p.)'));
          assert.equal((svg.match(/<circle data-plan=/g)||[]).length,98);
        }
      }
    }
  }
});

function mockDocument(){
  const element=()=>({
    textContent:'',innerHTML:'',value:'',clientWidth:340,attributes:{},listeners:{},
    setAttribute(name,value){this.attributes[name]=value;},
    addEventListener(name,handler){this.listeners[name]=handler;}
  });
  const elements=new Map([...html.matchAll(/\bid="([^"]+)"/g)].map(match=>[match[1],element()]));
  return {elements,getElementById(id){return elements.get(id)||null;}};
}

test('DOM smoke exercises all gates, complete-plan selection and scatter interaction', () => {
  const doc=mockDocument(),app=model.mount(doc),get=id=>doc.getElementById(id);
  assert.equal(get('plan').value,'DRDDM');
  assert.equal((get('plan').innerHTML.match(/<option /g)||[]).length,96);
  assert.equal(get('admissible-count').textContent,'1 / 96');
  assert.equal(get('selected-status').attributes['data-state'],'inside');
  assert.ok(get('values-plot').innerHTML.startsWith('<svg'));
  assert.ok(get('plans-plot').innerHTML.startsWith('<svg'));
  assert.match(get('time-scope').textContent,/9 intervalos totais/);
  assert.match(get('optimality-note').textContent,/0 de 4 históricos/);

  get('preset-impossible').listeners.click();
  assert.equal(get('tau').value,'0.85');
  assert.equal(get('admissible-count').textContent,'0 / 96');
  assert.equal(get('selected-status').attributes['data-state'],'outside');

  get('preset-relaxed').listeners.click();
  assert.equal(get('plan').value,'DDDDM');
  assert.equal(get('admissible-count').textContent,'1 / 96');
  assert.equal(get('selected-status').attributes['data-state'],'inside');

  get('preset-no-signal').listeners.click();
  assert.equal(get('eta').value,'0.5');
  assert.match(get('optimality-note').textContent,/96 planos empatam/);
  assert.equal(get('selected-status').attributes['data-state'],'outside');

  get('preset-default').listeners.click();
  get('choose-maximin').listeners.click();
  assert.equal(get('plan').value,'DDDDM');
  assert.equal(get('selected-status').attributes['data-state'],'outside');
  get('choose-minimax').listeners.click();
  assert.equal(get('plan').value,'DRDDM');
  get('plans-plot').listeners.click({target:{closest(){return {getAttribute(){return 'RDDDM';}};}}});
  assert.equal(get('plan').value,'RDDDM');
  assert.ok(!/NaN|undefined/.test(get('gate-explanation').textContent));
  app.update();
});

test('the interface explicitly preserves observational and physical scope', () => {
  assert.ok(html.includes('seu nome não é entregue ao controlador'));
  assert.ok(html.includes('Uma falha de aquisição é compartilhada pelas três cópias'));
  assert.ok(html.includes('Quatro atualizações D/R obrigatórias'));
  assert.ok(html.includes('centro calculado separadamente para cada resposta pode não corresponder'));
  assert.ok(html.includes('certificados e valores de referência usam frações exatas'));
  assert.ok(!/<(?:select|input)[^>]+id="history"/.test(html));
});
