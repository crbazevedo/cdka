/** Exact finite witness. No DOM, random sampling or physical-simulator code. */
const freeze = value => {
  if (value && typeof value === 'object') {
    for (const child of Object.values(value)) freeze(child);
    Object.freeze(value);
  }
  return value;
};

const gcd = (a, b) => {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a;
};

function rational(n, d = 1n) {
  if (d === 0n) throw new RangeError('Denominator must be nonzero');
  if (d < 0n) { n = -n; d = -d; }
  const divisor = gcd(n, d);
  return {n: n / divisor, d: d / divisor};
}

function parse(value) {
  if (typeof value === 'number' && !Number.isFinite(value)) {
    throw new TypeError('A finite rational value is required');
  }
  if (typeof value !== 'number' && typeof value !== 'string') {
    throw new TypeError('Use a number or a rational string');
  }
  const text = String(value).trim();
  const fraction = text.match(/^([+-]?\d+)\/([+-]?\d+)$/);
  if (fraction) return rational(BigInt(fraction[1]), BigInt(fraction[2]));
  const decimal = text.match(/^([+-]?)(\d*)(?:\.(\d*))?(?:[eE]([+-]?\d+))?$/);
  if (!decimal || !(decimal[2] || decimal[3])) throw new TypeError('Invalid rational');
  const digits = decimal[3] || '';
  const exponent = Number(decimal[4] || 0) - digits.length;
  if (!Number.isSafeInteger(exponent) || Math.abs(exponent) > 10000) {
    throw new RangeError('Exponent outside supported range');
  }
  let numerator = BigInt((decimal[2] || '0') + digits);
  if (decimal[1] === '-') numerator = -numerator;
  return exponent >= 0
    ? rational(numerator * 10n ** BigInt(exponent))
    : rational(numerator, 10n ** BigInt(-exponent));
}

const add = (a, b) => rational(a.n * b.d + b.n * a.d, a.d * b.d);
const subtract = (a, b) => rational(a.n * b.d - b.n * a.d, a.d * b.d);
const multiply = (a, b) => rational(a.n * b.n, a.d * b.d);
const compare = (a, b) => {
  const difference = a.n * b.d - b.n * a.d;
  return difference < 0n ? -1 : difference > 0n ? 1 : 0;
};
const show = a => a.d === 1n ? String(a.n) : `${a.n}/${a.d}`;
const zero = rational(0n);
const one = rational(1n);
const half = rational(1n, 2n);

export const exact = value => show(parse(value));
export const compareExact = (a, b) => compare(parse(a), parse(b));
export function asNumber(value) {
  const a = parse(value);
  return Number(a.n * 1000000000000000n / a.d) / 1e15;
}

export const MODEL = freeze({
  states: ['A0', 'A1', 'B'],
  emission: [['1/2', '1/2', '0'], ['0', '0', '1']],
  terminal: ['1', '1', '0'],
  feature: ['1/2', '1/2', '-1/2'],
  operators: {
    I: [['1','0','0'], ['0','1','0'], ['0','0','1']],
    T: [['0','1','0'], ['1','0','0'], ['0','0','1']],
    R: [['1/2','1/2','0'], ['1/2','1/2','0'], ['0','0','1']],
    S: [['0','0','1'], ['0','0','1'], ['1/2','1/2','0']],
    C: [['1','0','0'], ['1','0','0'], ['0','0','1']]
  },
  observation: ['0', '1', '0']
});

// U chooses S for observation 0, R for 1. W makes the opposite choice.
export const U = freeze([MODEL.operators.S[0], MODEL.operators.R[1], MODEL.operators.S[2]]);
export const W = freeze([MODEL.operators.R[0], MODEL.operators.S[1], MODEL.operators.R[2]]);
export const LABELS = freeze(['R', 'S', 'U']);
export const FULL_LABELS = freeze(['R', 'S', 'U', 'W']);
export const GATE = freeze({maximum_regret: '1/10', minimum_value: '2/3'});
export const DEFAULT_A = '3/5';

export function lawAfter(law, kernel) {
  if (!Array.isArray(law) || !Array.isArray(kernel) || law.length !== kernel.length || !kernel.length) {
    throw new RangeError('Law and kernel dimensions differ');
  }
  const columns = kernel[0].length;
  if (!columns || kernel.some(row => row.length !== columns)) throw new RangeError('Ragged kernel');
  return Array.from({length: columns}, (_, j) => show(law.reduce(
    (sum, mass, i) => add(sum, multiply(parse(mass), parse(kernel[i][j]))), zero
  )));
}

export function payoff(law, terminal = MODEL.terminal) {
  if (law.length !== terminal.length) throw new RangeError('Law and payoff dimensions differ');
  return show(law.reduce((sum, mass, i) => add(sum, multiply(parse(mass), parse(terminal[i]))), zero));
}

export function assessValues(values, labels = LABELS, gate = GATE) {
  if (!values.length || !labels.length || values.some(row => row.length !== labels.length)) {
    throw new RangeError('Invalid value table');
  }
  const table = values.map(row => row.map(value => {
    const x = parse(value);
    if (compare(x, zero) < 0 || compare(x, one) > 0) throw new RangeError('Values must be in [0,1]');
    return x;
  }));
  const max = row => row.reduce((a, b) => compare(a, b) >= 0 ? a : b);
  const min = row => row.reduce((a, b) => compare(a, b) <= 0 ? a : b);
  const oracle = table.map(max);
  const regrets = labels.map((_, j) => max(table.map((row, i) => subtract(oracle[i], row[j]))));
  const floors = labels.map((_, j) => min(table.map(row => row[j])));
  const minimax = min(regrets), maximin = max(floors);
  const minimaxPrograms = labels.filter((_, j) => compare(regrets[j], minimax) === 0);
  const maximinPrograms = labels.filter((_, j) => compare(floors[j], maximin) === 0);
  const delta = parse(gate.maximum_regret), tau = parse(gate.minimum_value);
  if (compare(delta, zero) < 0 || compare(tau, zero) < 0 || compare(tau, one) > 0) {
    throw new RangeError('Invalid joint gate');
  }
  return {
    labels: [...labels],
    informed_values: oracle.map(show),
    informed_programs: table.map((row, i) => labels.filter((_, j) => compare(row[j], oracle[i]) === 0)),
    worst_regrets: regrets.map(show),
    minimum_values: floors.map(show),
    minimax_program: minimaxPrograms[0],
    minimax_programs: minimaxPrograms,
    minimax_regret: show(minimax),
    maximin_program: maximinPrograms[0],
    maximin_programs: maximinPrograms,
    maximin_value: show(maximin),
    gate: {
      maximum_regret: show(delta), minimum_value: show(tau),
      feasible_programs: labels.filter((_, j) => compare(regrets[j], delta) <= 0 && compare(floors[j], tau) >= 0)
    }
  };
}

export function evaluateWitness(a = DEFAULT_A) {
  const parameter = parse(a);
  if (compare(parameter, zero) < 0 || compare(parameter, one) > 0) throw new RangeError('a must lie in [0,1]');
  const acquisition = [show(multiply(parameter, half)), show(multiply(parameter, half)), show(subtract(one, parameter))];
  const preparations = [lawAfter(acquisition, MODEL.operators.I), lawAfter(acquisition, MODEL.operators.C)];
  const falseLaws = [acquisition.slice(), acquisition.slice()];
  const operators = [MODEL.operators.R, MODEL.operators.S, U];
  const values = laws => laws.map(law => operators.map(kernel => payoff(lawAfter(law, kernel))));
  const actualValues = values(preparations), falseValues = values(falseLaws);
  const fullValues = preparations.map((law, i) => [...actualValues[i], payoff(lawAfter(law, W))]);
  const falseFullValues = falseLaws.map((law, i) => [...falseValues[i], payoff(lawAfter(law, W))]);
  return {
    a: show(parameter), acquisition, histories: ['I', 'C'], preparations,
    old_signatures: preparations.map(law => payoff(law, MODEL.feature)),
    actual_values: actualValues,
    actual: assessValues(actualValues),
    false_fresh_reconstructions: falseLaws,
    false_values: falseValues,
    false_decision: assessValues(falseValues),
    full_class: {
      labels: [...FULL_LABELS], actual_values: fullValues,
      false_values: falseFullValues,
      actual: assessValues(fullValues, FULL_LABELS),
      false_decision: assessValues(falseFullValues, FULL_LABELS),
      dominance: fullValues.every(row => compareExact(row[0], row[3]) >= 0)
    },
    false_prediction_gap: show(subtract(parse(falseValues[1][2]), parse(actualValues[1][2]))),
    old_family_contains: [true, compare(parameter, zero) === 0],
    two_step_SU: preparations.map(law => payoff(lawAfter(lawAfter(law, MODEL.operators.S), U))),
    post_U: preparations.map(law => lawAfter(law, U))
  };
}
