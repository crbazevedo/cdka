"""Reproduce v12 exact closure certificates and small separating executions."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse, hashlib, json
from cdka.semantic_closure import (
    close_continuations, plant_operators, refine_lumping, quotient_matrix,
    point, vector, dot, apply, word_value, observation_masks,
    delayed_fixture, feedback_fixture, rank_vs_states, delayed_chain,
    refinement_falsifier, lift_nuisance, matrix,
)
from cdka.trace_microscope import terminal_law
from cdka.composition import Contract, quotient


def clean(value):
    if isinstance(value,F):return {'exact':str(value),'value':float(value)}
    if isinstance(value,dict):return {str(k):clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(x) for x in value]
    return value


def snapshot(c, limit=None):
    n=c.basis.n
    depth_classes=[]
    for depth in range(len(c.profile)):
        selected=[v for v,w in zip(c.basis.originals,c.witnesses) if len(w[0])<=depth]
        signatures={tuple(v[i] for v in selected) for i in range(n)}
        depth_classes.append(len(signatures))
    return {
        'physical_states':n,'dimension':c.dimension,'evaluations':c.attempts,
        'rank_by_word_length':c.profile,'classes_by_word_length':depth_classes,
        'classes':c.state_classes(),
        'basis_words':[{'word':w,'probe':p} for w,p in c.witnesses],
        'intertwining_verified':c.verify(),
        'basis':c.basis.originals if limit is None else c.basis.originals[:limit],
    }


def certificate():
    states,ops,labels=plant_operators(micro=True)
    full=close_continuations(ops,{'alive':[1]*len(states)})
    hold=close_continuations({'hold':ops['hold']},{'alive':[1]*len(states)})
    lumps=refine_lumping(ops,labels)
    for q in ops.values():quotient_matrix(q,lumps['blocks'])
    macro,mo,_=plant_operators()
    c=close_continuations(mo,{'alive':[1]*len(macro)})
    a,b=terminal_law(48),terminal_law(63)
    mu=tuple(a.get(s,F(0)) for s in macro);nu=tuple(b.get(s,F(0)) for s in macro)
    endpoint={'mass_left':sum(mu),'mass_right':sum(nu),'separator':c.separator(mu,nu),
              'refresh_left':dot(mu,apply(mo['refresh'],vector([1]*20))),
              'refresh_right':dot(nu,apply(mo['refresh'],vector([1]*20)))}
    names,q,g=delayed_fixture();delayed=close_continuations(q,g)
    ds=snapshot(delayed);ds.update(names=names,separator=delayed.separator(point(4,0),point(4,1)),
        reverse_values=(dot(point(4,0),word_value(q,('check','prepare'),g['alive'])),
                        dot(point(4,1),word_value(q,('check','prepare'),g['alive']))))
    st,q,obs,mu,nu=feedback_fixture()
    blind=close_continuations(q,{'alive':[1]*4})
    observed=close_continuations(obs,{'alive':[1]*4})
    v=tuple(word_value(obs,('observe:0','act0'),[1]*4)[i]+
            word_value(obs,('observe:1','act1'),[1]*4)[i] for i in range(4))
    feedback={'states':st,'blind_rank':blind.dimension,'observed_rank':observed.dimension,
      'blind_equivalent':blind.equivalent(mu,nu),'feedback_values':(dot(mu,v),dot(nu,v)),
      'separator':observed.separator(mu,nu)}
    chain=[]
    for n in (3,5,9,12):
        q,g=delayed_chain(n);x=close_continuations(q,g)
        chain.append({'states':n,'profile':x.profile,'rank':x.dimension,
                      'witness':x.separator(point(n,0),point(n,1))})
    q,g=rank_vs_states(17);rc=close_continuations(q,g)
    rank={'rank':rc.dimension,'distinct_states':len(rc.state_classes()),
          'signatures':[[v[i] for v in rc.basis.originals] for i in range(17)]}
    q,g=refinement_falsifier();bc=close_continuations(q,g)
    try:quotient_matrix(q['step'],bc.state_classes());reject=False
    except ValueError:reject=True
    lump={'trace_classes':bc.state_classes(),'linear_rank':bc.dimension,'markov_quotient_rejected':reject,
          'stable_classes':refine_lumping(q,[0]*5)['blocks']}
    core={'stay':matrix([{0:F(3,4),1:F(1,8)},{1:F(1,2)}]),
          'repair':matrix([{0:F(4,5)},{0:F(2,3)}])}
    scaling=[]
    for m in (1,2,5,16,64):
        q=lift_nuisance(core,m);x=close_continuations(q,{'alive':[1]*(2*m)})
        scaling.append({'nuisance_modes':m,'states':2*m,'rank':x.dimension,
                        'evaluations':x.attempts,'classes':len(x.state_classes()),'verified':x.verify()})
    return clean({'revision':'v12','date':'2026-11-02','source_commit':'644945674871f7b0d6dcf7de1f1693d5c237c155',
        'physical_contract_git_blob':'d2b9ccc2253b326af5d494b6d14c5dac6666105c',
        'plant':{'states':states,'full':snapshot(full,limit=0),'hold':snapshot(hold,limit=0),
                 'readable_initial_classes':len(set(labels)),
                 'stable_partition_counts':lumps['history']},
        'endpoint_extension':endpoint,'delayed':ds,'feedback':feedback,
        'no_collapse_chain':chain,'rank_not_memory':rank,'trace_not_lumping':lump,
        'nuisance_scaling':scaling,
        'verification':{'python_scientific_tests':17,'local_fixture_word_checks':1488,
                        'original_command_words_checked':85,'original_plans_checked':64,
                        'macro_intertwining_identities':80,'microscopic_states':80},
        'scope':'Exact finite explicit substochastic kernels, declared tasks and observable masks; algebraic rank is not controller memory or universal computational complexity.'})


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true')
    args=parser.parse_args();out=certificate()
    text=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    dest=Path('docs/lab/semantic-certificate.json')
    if args.write:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
    if args.check:
        if dest.read_text()!=text:raise SystemExit('semantic certificate drift')
        print('Certificate matches exact recomputation.')
    p=out['plant'];print(json.dumps({'rank':p['full']['dimension'],'profile':p['full']['rank_by_word_length'],
       'candidate_evaluations':p['full']['evaluations'],'hold_rank':p['hold']['dimension'],
       'feedback':out['feedback'],'nuisance_scaling':out['nuisance_scaling'],
       'endpoint_extension':out['endpoint_extension']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
