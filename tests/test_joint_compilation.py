"""Independent finite and algebraic checks; this is not a novelty test."""
import hashlib
import unittest
from fractions import Fraction as F
from itertools import product
from math import log2
from pathlib import Path
from cdka.joint_compilation import (Surd,quadratic_roots,quadratic_nonnegative,
 channel_row,continuation_table,evaluate_witness,best_decoder,synthesize,
 funded_synthesis,polynomial_candidates,witness_polynomial,phase_certificate,phase_value)
from cdka.continuation_interfaces import plans,upper_envelope,equal_signal_joint,micro_alpha
from cdka.composition import Contract

class JointCompilationTests(unittest.TestCase):
 def test_base_kernel_and_continuations_are_unchanged(self):
  expected={'composition.py':'d2b9ccc2253b326af5d494b6d14c5dac6666105c',
            'continuation_interfaces.py':'d18aba3fca411d5db07d71952d2e64d0b3842f29'}
  for name,sha in expected.items():
   p=Path(__file__).resolve().parents[1]/'cdka'/name;data=p.read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),sha)

 def test_exact_radical_sign_and_roots(self):
  for a,b,d,sgn in [(1,-1,2,-1),(2,-1,2,1),(-1,1,2,1),(-2,1,2,-1),(2,-1,4,0)]:
   self.assertEqual(Surd(a,b,d).sign(),sgn)
  roots=quadratic_roots((F(-2),F(0),F(1)))
  self.assertEqual(roots[0].evaluate((-2,0,1)).sign(),0)
  self.assertEqual(roots[1].evaluate((-2,0,1)).sign(),0)
  self.assertFalse(quadratic_nonnegative((-1,0,1),Surd(-2),Surd(2)))
  self.assertTrue(quadratic_nonnegative((1,0,1),Surd(-2),Surd(2)))

 def test_channel_is_complete_and_has_correct_endpoints(self):
  for word,p in product(range(4),(F(0),F(1,10),F(1,2))):
   row=channel_row(word,p);self.assertEqual(sum(row),1)
   if p==0:self.assertEqual(row[word],1)
   if p==F(1,2):self.assertEqual(row,(F(1,4),)*4)

 def test_global_continuum_certificate(self):
  r=phase_certificate()
  self.assertEqual(r['joint_programs'],5184)
  self.assertEqual(r['distinct_polynomials'],486)
  self.assertEqual(r['dominance_checks'],1458)
  self.assertAlmostEqual(r['thresholds'][0].approximate(),.004921292856323312,places=13)
  self.assertAlmostEqual(r['thresholds'][1].approximate(),.2081876270782522,places=13)

 def test_hull_replacement_cardinality_with_full_plan_library(self):
  for encoding,p in [((0,1,3),F(1,100)),((0,0,3),F(1,10)),((0,1,2),F(1,5))]:
   for L in (1,2):
    reduced=best_decoder(encoding,p,L)
    full=best_decoder(encoding,p,L,reduced=False)
    self.assertEqual(full['value'],reduced['value'])

 def test_joint_optimizer_against_exhaustive_tables(self):
  # Independent full decoder enumeration (not the subset/row-max solver).
  ids,table=continuation_table()
  for error in (F(0),F(1,100),F(1,10),F(1,2)):
   best=F(-1)
   for encoding in product(range(4),repeat=3):
    terms=[[sum((table[y][j]*channel_row(encoding[y],error)[r] for y in range(3)),F(0))
            for j in range(3)] for r in range(4)]
    for decoder in product(range(3),repeat=4):
     value=sum((terms[r][decoder[r]] for r in range(4)),F(0))
     best=max(best,value)
   self.assertEqual(best,synthesize(error)['value'])
   self.assertEqual(best,phase_value(error))

 def test_polynomials_match_direct_rational_channel(self):
  c=phase_certificate()
  for witness,curve in zip(c['witnesses'],c['phase_curves']):
   for p in (F(0),F(1,1000),F(1,100),F(1,5),F(1,2)):
    self.assertEqual(curve[0]+curve[1]*p+curve[2]*p*p,evaluate_witness(*witness,p))

 def test_same_cardinality_relabeling_not_general_physical_symmetry(self):
  p=F(1,100)
  bad=best_decoder((0,1,2),p)['value'];good=best_decoder((0,1,3),p)['value']
  self.assertGreater(good,bad)
  self.assertEqual(best_decoder((0,1,2),F(0))['value'],best_decoder((0,1,3),F(0))['value'])
  # Cube XOR translations ARE symmetries; arbitrary permutations are not.
  for mask in range(4):
   self.assertEqual(best_decoder(tuple(x^mask for x in (0,1,3)),p)['value'],good)

 def test_lossy_abstraction_strictly_beats_any_injective_encoding(self):
  for p in (F(1,100),F(1,20),F(1,10)):
   best=synthesize(p);lossless=synthesize(p,injective=True)
   self.assertGreater(best['value'],lossless['value'])
   self.assertEqual(best['code_states'],2)
   self.assertEqual(best['templates'],2)

 def test_more_mutual_information_can_give_less_task_value(self):
  def mi(enc,p):
   rows=[channel_row(x,p) for x in enc]
   marginal=[sum((row[r] for row in rows),F(0))/3 for r in range(4)]
   return sum(float(q/3)*log2(float(q/marginal[r])) for row in rows for r,q in enumerate(row) if q)
  p=F(1,10);best=synthesize(p);inj=synthesize(p,injective=True)
  self.assertGreater(mi(inj['encoding'],p),mi(best['encoding'],p))
  self.assertGreater(best['value'],inj['value'])

 def test_paid_library_changes_optimum_even_without_noise(self):
  winner,options=funded_synthesis(F(0),4,1)
  self.assertEqual(winner['installed'],2);self.assertEqual(winner['fee'],1)
  self.assertEqual(winner['balance'],3)
  self.assertGreater(winner['value'],options[2]['value'])
  free,_=funded_synthesis(F(0),4,0)
  self.assertGreater(free['value'],winner['value'])

 def test_pruning_is_not_licensed_under_unequal_program_costs(self):
  # Full envelope A/B excludes C everywhere, but only C fits budget=0.
  # alpha=(healthy,degraded), installation costs are 1,1,0.
  profiles=((F(1),F(0)),(F(0),F(1)),(F(49,100),F(49,100)))
  at_prior=lambda a:(a[0]+a[1])/2
  self.assertGreater(max(map(at_prior,profiles[:2])),at_prior(profiles[2]))
  affordable=[a for a,cost in zip(profiles,(1,1,0)) if cost<=0]
  self.assertEqual(max(map(at_prior,affordable)),F(49,100))
  self.assertFalse([a for a,cost in zip(profiles[:2],(1,1)) if cost<=0])

 def test_raw_physical_transition_oracle(self):
  p=Contract();lib=plans();joint=equal_signal_joint();error=F(1,10)
  raw={i:micro_alpha(p,lib[i]) for i in (50,58,42)}
  enc=(0,0,3);dec=(58,58,58,42);value=F(0)
  for y,mu in enumerate(joint):
   for r,q in enumerate(channel_row(enc[y],error)):
    value+=q*sum((mu[h]*raw[dec[r]][h] for h in (0,1)),F(0))
  self.assertEqual(value,evaluate_witness(enc,dec,error))

 def test_input_contract(self):
  for x in (-1,F(3,4)):
   with self.assertRaises(ValueError):channel_row(0,x)
  with self.assertRaises(ValueError):funded_synthesis(0,4,-1)
  with self.assertRaises(ValueError):best_decoder((0,1),0)

if __name__=='__main__':unittest.main()
