"""Frozen feature-only selector. Predictions affect cost, never certificate validity."""
from dataclasses import dataclass
from fractions import Fraction as F
import json,time
import numpy as np
from vendor.v21.cdka.regenerative import validate,horizon_ok,partition_number,ContractError
from .enclosures import certified_solve

def features(model,h,backend):
    horizon_ok(h);n=len(model.components);local=h*sum((len(c.initial)-len(c.target))**2 for c in model.components)
    if backend=='histogram':
        p=partition_number(h+1);return np.asarray([1.,local,h*h,n*p,p],dtype=float)
    if backend=='subset':
        s=2**n;return np.asarray([1.,local,s*h*h,s*n*h,s*h],dtype=float)
    raise ValueError('unknown backend')

@dataclass(frozen=True)
class FrozenSelector:
    histogram_coefficients:tuple
    subset_coefficients:tuple
    training_manifest_sha256:str
    calibration_sha256:str
    max_histograms:int=100000
    max_subset_components:int=16
    version:str='v22-structural-nnls-1'
    def choose(self,model,h):
        n=len(model.components);p=partition_number(h+1);choices={}
        if p<=self.max_histograms:choices['histogram']=max(1e-9,float(features(model,h,'histogram')@np.asarray(self.histogram_coefficients)))
        if n<=self.max_subset_components:choices['subset']=max(1e-9,float(features(model,h,'subset')@np.asarray(self.subset_coefficients)))
        if not choices:raise ContractError('no covered bounded backend; use general solver')
        winner=min(choices,key=lambda k:(choices[k],k));return winner,choices
    def as_dict(self):return dict(self.__dict__)
    @classmethod
    def read(cls,path):return cls(**json.loads(open(path).read()))

def solve(model,h,selector,*,rtol=F(1,10**8),atol=F(0),initial_bits=64,max_bits=512):
    start=time.perf_counter();contract=validate(model);horizon_ok(h)
    t=time.perf_counter();backend,predictions=selector.choose(model,h);selection_s=time.perf_counter()-t
    out=certified_solve(model,h,backend,rtol=rtol,atol=atol,initial_bits=initial_bits,max_bits=max_bits,checked=True)
    out.update(backend=backend,predictions_s=predictions,selection_s=selection_s,end_to_end_s=time.perf_counter()-start,contract_sha256=contract['sha256'])
    return out
