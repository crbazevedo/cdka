"""Reproduce v5 certificates; JSON on stdout, no simulation randomness."""
import json
from fractions import Fraction as F
from cdka.reconfiguration import *


def main():
    m=Retrofit()
    out={
        'model_scope':'Symmetric context-blind effort; finite reservoir; no free history or seed.',
        'correlation_p_01':{
            'xor_independent':xor_failure(F(1,10),F(1,10),F(1,100)),
            'xor_common':xor_failure(F(1,10),F(1,10),F(1,10)),
            'majority_independent_failure':1-repetition_success(independent_masks(3,F(1,10))),
            'majority_common_failure':1-repetition_success(common_masks(3,F(1,10)))},
        'recoverable_damage_001_perfect_repair':{
            'expected_life':redundant_lifetime(F(1,100),1),
            'spectral_radius':redundant_radius(F(1,100),1),
            'safe_support':list(safe_support(redundant_kernel(F(1,100),1)))},
        'reconfiguration':{
            'capacity':m.capacity,'cost':m.cost,'harvest':m.harvest,'install':m.install,
            'infinite_probability':m.infinite()[0][0],
            'earliest_probability':old_success(0)*old_success(2)*m.install,
            'optimal_path':m.infinite_path(0),
            'finite_horizons':{n:m.finite(n)[0][n][0] for n in (1,2,3,4,6,10,20)}},
        'support_perturbation':{
            'bounded_noise_cycle_success':repetition_success(bounded_single_upset(F(1,2))),
            'full_support_p_01_cycle_success':repetition_success(independent_masks(3,F(1,10))),
            'positive_new_error_infinite':Retrofit(upgraded=F(999,1000)).infinite()[0][0]},
        'switching':{k:[[str(x) for x in row] for row in v] for k,v in switching_witness().items()}}
    print(json.dumps(out,default=lambda x:{'exact':str(x),'float':float(x)} if isinstance(x,F) else str(x),indent=2))

if __name__=='__main__':main()
