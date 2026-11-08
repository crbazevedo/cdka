from fractions import Fraction as F
from pathlib import Path
import unittest,json,random,hashlib
from cdka22.enclosures import *
from cdka22.portfolio import FrozenSelector,solve
from vendor.v21.cdka.regenerative import meeting_restart,path_oracle,exact_histogram_value,Local,Model,mat,vector
ROOT=Path(__file__).resolve().parents[1]
class CertifiedTests(unittest.TestCase):
 def test_arithmetic(self):
  rng=random.Random(22)
  for bits in (8,32,64):
   a=Dyadic(bits)
   for _ in range(100):
    x,y=F(rng.randrange(100),101),F(rng.randrange(100),103)
    for r,q in ((a.rational(x),x),(a.add(a.rational(x),a.rational(y)),x+y),(a.mul(a.rational(x),a.rational(y)),x*y),(a.complement(a.rational(x)),1-x)):
     self.assertLessEqual(F(r[0],a.scale),q);self.assertGreaterEqual(F(r[1],a.scale),q)
 def test_both_backends_exact_words(self):
  for n in (1,2,3):
   m=meeting_restart(n)
   for h in range(8):
    q=path_oracle(m,h)
    self.assertEqual(q,exact_histogram_value(m,h))
    for b in (histogram,subset):self.assertTrue(b(m,h).contains(q))
 def test_rare_and_adaptive(self):
  cs=[]
  for i in range(8):
   p=F(100+i,10**6);q=F(1,2)
   cs.append(Local(mat([[1-p,p,0],[1-q,0,q],[0,0,1]]),mat([[1,0,0],[1,0,0],[0,0,1]]),vector([1,0,0]),(2,)))
  m=Model(tuple(cs));q=exact_histogram_value(m,4)
  for b in ('histogram','subset'):
   r=certified_solve(m,4,b);e=r['enclosure'];self.assertGreater(e.bits,64);self.assertTrue(e.contains(q));self.assertTrue(e.meets())
 def test_exhaustion(self):
  with self.assertRaises(PrecisionExhausted):certified_solve(meeting_restart(2),6,'subset',initial_bits=8,max_bits=8,rtol=F(1,10**20))
 def test_zero(self):
  for b in ('histogram','subset'):
   r=certified_solve(meeting_restart(3),1,b);self.assertTrue(r['structural_zero']);self.assertEqual(r['enclosure'].upper,0)
 def test_wrong_selector_still_sound(self):
  s=FrozenSelector((10.,0.,0.,0.,0.),(1.,0.,0.,0.,0.),'x','y');m=meeting_restart(6)
  r=solve(m,8,s);self.assertEqual(r['backend'],'subset');self.assertTrue(r['enclosure'].contains(exact_histogram_value(m,8)))
 def test_bad_inputs(self):
  for h in (-1,True,1.5):
   with self.assertRaises(ContractError):certified_solve(meeting_restart(2),h,'subset')
  with self.assertRaises(ValueError):certified_solve(meeting_restart(2),4,'subset',rtol=-1)
 def test_precision(self):
  e=Enclosure(10000,10002,20,'test',0,0);self.assertTrue(e.meets(F(1,1000)))
  for q in (e.lower,e.upper,e.midpoint):self.assertLessEqual(abs(e.midpoint-q),q/F(1000))
 def test_frozen_and_all_holdout(self):
  f=json.loads((ROOT/'evidence/freeze.json').read_text());self.assertFalse(f['heldout_timing_read'])
  self.assertEqual(hashlib.sha256((ROOT/'evidence/frozen_selector.json').read_bytes()).hexdigest(),f['selector_sha256'])
  rows=json.loads((ROOT/'evidence/heldout_rows.json').read_text());self.assertEqual(len(rows),48)
  for r in rows:
   self.assertEqual(r['selector_sha256'],f['selector_sha256']);self.assertTrue(r['interval_overlap'])
   for x in r['enclosures'].values():
    e=Enclosure(int(x['lower_numerator']),int(x['upper_numerator']),x['bits'],x['backend'],x['multiplications'],x['additions'])
    self.assertTrue(e.meets())
    if r['exact_probability'] is not None:self.assertTrue(e.contains(F(r['exact_probability'])))
if __name__=='__main__':unittest.main()
