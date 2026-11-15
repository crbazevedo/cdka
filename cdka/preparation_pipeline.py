"""Compose physical program coverage, preparation coverage and one decision.

This public checker starts from raw physical inputs. A decision certificate
cannot supply its own unchecked subset of histories or executable programs:
the appropriate independent cover is checked first, then its actual retained
representatives are passed to the compact decision checker. Streaming uses
the same output contract and replays every preparation without a value table.

The objects are offline evaluator certificates. They grant no history label,
hidden source, health state or convexly mixed controller to the physical agent.
"""
from hashlib import sha256
import json

from .program_families import _exact
from .suffix_features import compile_feature_family, check_feature_family
from .suffix_contexts import compile_family as compile_program_contexts
from .suffix_contexts import check_family as check_program_contexts
from .preparation_families import compile_family as compile_preparations
from .preparation_families import check_family as check_preparations
from .preparation_decisions import make_problem, compile_decision, check_decision


SCHEMA = 'cdka.covered-common-decision/v1'
PROGRAM_METHODS = ('feature8', 'finite_context8')
PREPARATION_METHODS = ('stream', 'convex_cover')
OUTPUT_CONTRACT = (
    'one minimax and one maximin original complete program; '
    'exact per-program worst regret and minimum fidelity with actual-history '
    'attainers; joint feasibility from those checked bounds; informed values '
    'queryable, not an explicit value per original history'
)


def _counts(h, k):
    if type(h) is not int or h < 0 or type(k) is not int or k < 0:
        raise ValueError('nonnegative preparation and continuation horizons required')


def _methods(program_method, preparation_method):
    if type(program_method) is not str or program_method not in PROGRAM_METHODS:
        raise ValueError('program coverage method')
    if type(preparation_method) is not str or preparation_method not in PREPARATION_METHODS:
        raise ValueError('preparation coverage method')


def _binding(operators, terminal, initial_law, h, k, program_method,
             preparation_method, contract):
    payload = {'schema': SCHEMA, 'operators': operators, 'terminal': terminal,
               'initial_law': initial_law, 'preparation_updates': h,
               'ordinary_continuation_updates': k, 'program_method': program_method,
               'preparation_method': preparation_method, 'contract': contract,
               'output_contract': OUTPUT_CONTRACT}
    return sha256(json.dumps(_exact(payload), sort_keys=True,
                             separators=(',', ':')).encode()).hexdigest()


def _scope(contract, k):
    return {'user_contract': contract, 'ordinary_continuation_updates': k,
            'program_grammar': 'exactly k D/R and at most one additional M',
            'output_contract': OUTPUT_CONTRACT}


def compile_task(operators, terminal, initial_law, h, k, *,
                 program_method='feature8', preparation_method='convex_cover',
                 contract=None, program_certificate=None,
                 preparation_certificate=None, optimize=True):
    """Construct a self-contained composite certificate and work statistics.

    Optional supplied covers support explicit reuse and frozen reproduction.
    They are checked before use. A first-use benchmark must not supply a
    previously discovered cover without charging its construction separately.
    """
    _counts(h, k)
    _methods(program_method, preparation_method)
    if type(optimize) is not bool:
        raise ValueError('optimization flag')
    program_compiler = (compile_feature_family if program_method == 'feature8'
                        else compile_program_contexts)
    program_checker = (check_feature_family if program_method == 'feature8'
                       else check_program_contexts)
    if program_certificate is None:
        kwargs = {'optimize': optimize} if program_method == 'finite_context8' else {}
        frontier, program_certificate, program_stats = program_compiler(
            operators, terminal, k, **kwargs)
    else:
        frontier = program_checker(program_certificate, operators, terminal, k)
        program_stats = {'supplied_cover': True, 'retained_programs': len(frontier)}

    preparations = None
    if preparation_method == 'convex_cover':
        if preparation_certificate is None:
            preparations, preparation_certificate, preparation_stats = compile_preparations(
                operators, initial_law, h, optimize=optimize)
        else:
            preparations = check_preparations(preparation_certificate, operators, initial_law, h)
            preparation_stats = {'supplied_cover': True,
                                 'retained_preparations': len(preparations)}
    else:
        if preparation_certificate is not None:
            raise ValueError('streaming cannot substitute a supplied preparation subset')
        preparation_stats = {'streamed_histories': 2**h, 'value_table_materialized': False}

    problem = make_problem(operators, terminal, initial_law, h, frontier,
                           feature_certificate=program_certificate['features'],
                           contract=_scope(contract, k))
    kwargs = ({'preparation_binding': problem['preparation_binding']}
              if preparations is not None else {})
    decision, decision_stats = compile_decision(problem, preparations, **kwargs)
    certificate = {
        'schema': SCHEMA, 'preparation_updates': h, 'ordinary_continuation_updates': k,
        'program_method': program_method, 'preparation_method': preparation_method,
        'binding': _binding(operators, terminal, initial_law, h, k,
                            program_method, preparation_method, contract),
        'output_contract': OUTPUT_CONTRACT, 'contract': _exact(contract),
        'program_certificate': program_certificate,
        'preparation_certificate': preparation_certificate, 'decision': decision,
    }
    return certificate, {'programs': program_stats, 'preparations': preparation_stats,
                         'decision': decision_stats}


def _check_task(certificate, operators, terminal, initial_law, h, k, contract):
    _counts(h, k)
    keys = {'schema', 'preparation_updates', 'ordinary_continuation_updates',
            'program_method', 'preparation_method', 'binding', 'output_contract',
            'contract', 'program_certificate', 'preparation_certificate', 'decision'}
    if type(certificate) is not dict or set(certificate) != keys:
        raise ValueError('composite certificate object')
    c = certificate
    if (c['schema'] != SCHEMA or type(c['preparation_updates']) is not int or
            c['preparation_updates'] != h or
            type(c['ordinary_continuation_updates']) is not int or
            c['ordinary_continuation_updates'] != k or
            c['output_contract'] != OUTPUT_CONTRACT or c['contract'] != _exact(contract)):
        raise ValueError('composite decision contract')
    _methods(c['program_method'], c['preparation_method'])
    if c['binding'] != _binding(operators, terminal, initial_law, h, k,
                                c['program_method'], c['preparation_method'], contract):
        raise ValueError('composite physical binding')
    checker = (check_feature_family if c['program_method'] == 'feature8'
               else check_program_contexts)
    frontier = checker(c['program_certificate'], operators, terminal, k)
    if c['preparation_method'] == 'convex_cover':
        preparations = check_preparations(c['preparation_certificate'], operators, initial_law, h)
    else:
        if c['preparation_certificate'] is not None:
            raise ValueError('unchecked preparation subset in streaming certificate')
        preparations = None
    problem = make_problem(operators, terminal, initial_law, h, frontier,
                           feature_certificate=c['program_certificate']['features'],
                           contract=_scope(contract, k))
    kwargs = ({'preparation_binding': problem['preparation_binding']}
              if preparations is not None else {})
    check_decision(c['decision'], problem, preparations, **kwargs)
    return {'frontier': frontier, 'preparations': preparations,
            'problem': problem, 'decision': c['decision']}


def check_task(certificate, operators, terminal, initial_law, h, k, *, contract=None):
    """Verify every cover from raw physical inputs, then all decision bounds.

    No numerical library is imported on this path. Streaming replays the full
    history tree; convex_cover reconstructs only retained children and checks
    every supplied convex identity before the compact decision certificate.
    """
    try:
        return _check_task(certificate, operators, terminal, initial_law, h, k, contract)
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed composite decision certificate') from error
