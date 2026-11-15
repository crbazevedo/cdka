// Deterministic resource traces and lookup of the finite exact Python scan.
// This module does not approximate uncomputed prices or infer branch probability.
export function selectCase(data, gate, write, setup, objective = 'tasks') {
  if (!['tasks', 'cycles'].includes(objective)) throw new RangeError('Unknown objective');
  const point = data.cases.find(c => c.prices.gate === gate && c.prices.write === write && c.prices.setup === setup);
  if (!point) throw new RangeError('Price point was not certified');
  return {point, result: point[objective]};
}

export function startupComparison(data, gate, write, setup, objective = 'tasks') {
  if (data.schema !== 'cdka.optional-startup/v1') throw new TypeError('Optional-startup certificate required');
  const {point, result} = selectCase(data, gate, write, setup, objective);
  const rows = [
    {key: 'paid_only', label: 'Ótimo anterior: início pago', kind: 'physical'},
    {key: 'physical', label: 'Ótimo físico ampliado', kind: 'physical'},
    {key: 'blind_optional', label: 'Melhor regra cega: início opcional', kind: 'physical'},
    {key: 'all_null_world', label: 'Canal sem conteúdo: reotimizado', kind: 'counterfactual'},
  ].map(item => ({...item, row: result.best[item.key]}));
  // The last row is an analytical world comparison even when its best
  // program itself omits acquisition.  It is not an extra physical candidate.
  const gaps = {
    paid: result.physical_gain_over_paid_only,
    blind: result.physical_gap_over_optional_blind,
    channel: result.reoptimized_all_channel_effect,
  };
  for (const {row} of rows) {
    displayNumber(row.survival); displayNumber(row.spent);
  }
  for (const gap of Object.values(gaps)) displayNumber(gap);
  return {point, result, rows, gaps, omittedBlind: result.best.blind_omitted};
}

export function conditionedTrace({balance, gate, write, gateCount, requested = 1,
  mode = 'vote', enabled = 1, terminal = false}) {
  for (const [name, value] of Object.entries({balance, gate, write, gateCount, requested, enabled})) {
    if (!Number.isInteger(value) || value < 0) throw new RangeError(`Invalid ${name}`);
  }
  if (balance > 96 || gateCount > 2 || requested > 1 || enabled > 1 || !['skip','service','vote','inverse'].includes(mode)) {
    throw new RangeError('Outside the declared contract');
  }
  const start = balance, middle = Number(balance >= 72 && balance < 96);
  const actualMode = balance < 72 ? 'skip' : mode;
  const selectionCost = ['vote','inverse'].includes(actualMode) ? 6 * gate : 0;
  const stages = [{name: 'Entrada', balance, charge: 0}];
  let spent = 0, earned = 0, spilled = 0, repair = 0, failure = null;
  const pay = (name, amount, cause) => {
    if (balance < amount) {
      failure = cause;
      stages.push({name, balance, charge: 0, required: amount, failure: cause});
      return false;
    }
    balance -= amount; spent += amount;
    stages.push({name, balance, charge: amount});
    return true;
  };
  const finish = () => ({start, balance, middle, actualMode, requested, repair,
    spent, earned, spilled, failure, stages,
    conserved: start + earned === spent + balance + spilled});
  if (!pay('Seleção', selectionCost, 'resource:selection')) return finish();
  const q = actualMode === 'skip' ? 0 : actualMode === 'service' ? 1 : requested;
  repair = Number(Boolean(q) && balance >= 48 + 24 + 6 * gate);
  if (!pay('Serviço', 48 * repair, 'resource:service')) return finish();
  if (!pay('Trabalho', 24 + 6 * gate, 'resource:task')) return finish();
  if (terminal) return finish();
  if (!pay('Enable', gateCount * gate, 'resource:enable')) return finish();
  if (!pay('Aquisição', enabled * write, 'resource:write')) return finish();
  earned = 48;
  spilled = Math.max(0, balance + earned - 96);
  balance = Math.min(96, balance + earned);
  stages.push({name: 'Colheita', balance, charge: -earned, spilled});
  return finish();
}

export function resourceComparison(balance, gate, write, terminal = false) {
  // Conditional branch: voter requests service, procedure and task succeed,
  // and the single NAND has no output flip. These are not free observations.
  const common = {balance, gate, write, mode: 'vote', requested: 1, terminal};
  const fresh = conditionedTrace({...common, gateCount: 0, enabled: 1});
  const elision = conditionedTrace({...common, gateCount: 1,
    enabled: 1 - fresh.repair * fresh.middle});
  return {fresh, elision};
}

export function displayNumber(response) {
  if (!response || typeof response.exact !== 'string' || typeof response.value !== 'number') {
    throw new TypeError('Exact response and display projection required');
  }
  return response.value;
}
