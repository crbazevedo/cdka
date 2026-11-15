import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(new URL('../docs/lab/maintenance_access.html', import.meta.url), 'utf8');
const canonical = JSON.parse(readFileSync(new URL('../docs/data/maintenance-access-results.json', import.meta.url), 'utf8'));
const embedded = html.match(/<script id="certified-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const source = html.match(/<script id="lab-script">([\s\S]*?)<\/script>/)[1];
const context = {
  document: {
    getElementById(id) { return id === 'certified-data' ? { textContent: embedded } : null; }
  }
};
vm.createContext(context);
vm.runInContext(source, context);
const model = context.MA;
const near = (actual, expected, tolerance = 3e-14) => assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} != ${expected}`);

test('offline data are identical to the exact generated 24-word artifact', () => {
  assert.deepEqual(JSON.parse(JSON.stringify(model.data)), canonical);
  assert.equal(model.data.bounded_words.length, 24);
  assert.equal(new Set(model.data.bounded_words.map(row => row.word.join(''))).size, 24);
  for (const row of model.data.bounded_words) {
    assert.ok(row.word.filter(x => x !== 'M').length <= 2);
    assert.ok(row.word.filter(x => x === 'M').length <= 1);
  }
  assert.ok(!/<script[^>]+\bsrc=/.test(html));
  assert.ok(!/\bfetch\s*\(/.test(source));
});

test('affine chart values reproduce every exact endpoint and reference value', () => {
  for (const row of model.data.bounded_words) {
    near(model.at(row, 0).left, model.fraction(row.left_at_zero));
    near(model.at(row, 1).left, model.fraction(row.left_at_one));
    near(model.at(row, 0).right, model.fraction(row.right_at_zero));
    near(model.at(row, 1).right, model.fraction(row.right_at_one));
    near(model.at(row, .8).left, model.fraction(row.left));
    near(model.at(row, .8).right, model.fraction(row.right));
    near(model.at(row, .8).gap, Math.abs(model.fraction(row.difference)));
  }
  assert.throws(() => model.at(model.rowFor('M'), -1));
  assert.throws(() => model.fraction('1/0'));
});

test('ordinary words and zero repair preserve the displayed pair exactly', () => {
  for (const row of model.data.bounded_words) {
    assert.equal(model.at(row, 0).gap, 0);
    if (!row.word.includes('M')) {
      for (const s of [0, .2, .8, 1]) assert.equal(model.at(row, s).gap, 0);
    }
  }
  assert.equal(model.at(model.rowFor('RM'), 1).gap, 0);
  assert.ok(model.at(model.rowFor('MR'), 1).gap > 0);
});

test('the global tolerance frontier is attained by M and remains separate from a selected word', () => {
  const slope = model.fraction(canonical.approximation.gap_per_unit_success);
  for (const s of [0, .1, .5, .8, 1]) {
    const largest = Math.max(...model.data.bounded_words.map(row => model.at(row, s).gap));
    near(model.globalGap(s), largest);
    near(model.at(model.rowFor('M'), s).gap, largest);
  }
  const limit = model.threshold(.005, slope);
  near(limit, model.fraction(canonical.approximation.success_threshold));
  near(limit, .6588667095, 1e-10);
  assert.equal(model.assess(model.rowFor('DR'), .8, .005).selectedFits, true);
  assert.equal(model.assess(model.rowFor('DR'), .8, .005).globalFits, false);
  assert.equal(model.assess(model.rowFor('M'), limit, .005).globalFits, true);
  assert.equal(model.assess(model.rowFor('M'), limit + .001, .005).globalFits, false);
});

test('the common midpoint predictor attains half of the pair separation', () => {
  for (const row of model.data.bounded_words) {
    for (const s of [0, .8, 1]) {
      const assessment = model.assess(row, s, .005);
      near(Math.abs(assessment.value.left - assessment.value.midpoint), assessment.selectedError);
      near(Math.abs(assessment.value.right - assessment.value.midpoint), assessment.selectedError);
    }
  }
  assert.equal(model.threshold(.005, 0), null);
  assert.equal(model.assess(model.rowFor('M'), 0, 0).globalFits, true);
  assert.equal(model.assess(model.rowFor('M'), .01, 0).globalFits, false);
});

test('prices include an additional maintenance interval and preserve distinct resource units', () => {
  for (const row of model.data.bounded_words) {
    const counts = { D: 0, R: 0, M: 0 };
    row.word.forEach(x => counts[x]++);
    assert.equal(row.cost.installed_nands, 6);
    assert.equal(row.cost.retained_cells, 3);
    assert.equal(row.cost.cell_writes, 3 * counts.R);
    assert.equal(row.cost.cell_channel_updates, 3 * (counts.D + counts.R));
    assert.equal(row.cost.prepaid_service_slots, counts.M);
    assert.equal(row.cost.voter_evaluations, counts.R + counts.M + 1);
    assert.equal(row.cost.nand_evaluations, 6 * row.cost.voter_evaluations);
    assert.equal(row.cost.clock_intervals, row.word.length + 1);
  }
  assert.equal(model.rowFor('DMR').cost.clock_intervals, 4);
  assert.match(model.intervalDescription(model.rowFor('DMR')), /2 atualizações D\/R \+ 1 intervalo adicional/);
});

test('rank labels preserve the exact zero-success regime and do not claim hardware bits', () => {
  assert.equal(model.rankModel(0).oneMaintenance, 10);
  assert.equal(model.rankModel(.0001).oneMaintenance, 12);
  assert.equal(model.rankModel(0).paid, 20);
  assert.equal(model.rankModel(1).paid, 22);
  assert.ok(html.includes('não são contagens de bits físicos'));
  assert.ok(html.includes('M ocupa um intervalo adicional'));
  assert.ok(html.includes('certificado de referência em s = 0,8'));
  assert.ok(html.includes('o voto de M aciona o reparo internamente'));
});

test('all plotted regimes produce accessible finite SVGs, including zero tolerance', () => {
  for (const row of model.data.bounded_words) {
    for (const s of [0, .8, 1]) {
      const probability = model.probabilitySVG(row, s);
      assert.match(probability, /^<svg[\s\S]*<\/svg>$/);
      assert.ok(probability.includes('role="img"') && probability.includes('<desc'));
      assert.ok(!/NaN|Infinity|undefined/.test(probability));
      for (const epsilon of [0, .005, .015]) {
        const gap = model.gapSVG(row, s, epsilon);
        assert.match(gap, /^<svg[\s\S]*<\/svg>$/);
        assert.ok(gap.includes('pontos percentuais'));
        assert.ok(!/NaN|Infinity|undefined/.test(gap));
      }
    }
  }
});

function mockDocument() {
  const element = () => ({
    textContent: '', innerHTML: '', value: '', attributes: {}, listeners: {}, dataset: {},
    setAttribute(name, value) { this.attributes[name] = value; },
    addEventListener(name, handler) { this.listeners[name] = handler; }
  });
  const elements = new Map([...html.matchAll(/\bid="([^"]+)"/g)].map(match => [match[1], element()]));
  const buttons = ['DR', 'M', 'DMR'].map(word => ({ ...element(), dataset: { word } }));
  return {
    elements, buttons,
    getElementById(id) { return elements.get(id) ?? null; },
    querySelectorAll(selector) { return selector === '[data-word]' ? buttons : []; }
  };
}

test('DOM smoke render initializes DMR and updates both charts and scope labels', () => {
  const doc = mockDocument();
  const app = model.mount(doc);
  const get = id => doc.getElementById(id);
  assert.equal(get('word').value, 'DMR');
  assert.equal((get('word').innerHTML.match(/<option /g) ?? []).length, 24);
  assert.ok(get('probability-plot').innerHTML.startsWith('<svg'));
  assert.ok(get('gap-plot').innerHTML.startsWith('<svg'));
  assert.match(get('interval-note').textContent, /4 intervalos/);
  assert.equal(get('selected-status').attributes['data-state'], 'outside');
  get('success').value = '0';
  get('success').listeners.input();
  assert.equal(get('one-maintenance-rank').textContent, '10');
  assert.equal(get('selected-status').attributes['data-state'], 'inside');
  get('success').value = '.8';
  doc.buttons[0].listeners.click();
  assert.equal(get('word').value, 'DR');
  assert.equal(get('selected-status').attributes['data-state'], 'inside');
  assert.match(get('global-status').textContent, /exige preservar/);
  assert.ok(!/NaN|undefined/.test(get('gap-explanation').textContent));
  app.update();
});
