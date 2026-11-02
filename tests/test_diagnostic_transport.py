from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import unittest
from cdka.diagnostic_transport import (
 TransportContract as C,terminal_table,terminal_joint,summaries,skip_value,
 optimize_terminal,margin_identity,closed_value,optimize_architecture,
 sign_partition_oracle,information_before_selector,reservation)

class DiagnosticTransportTests(unittest.TestCase):
 def test_original_physical_values(self):
  self.assertEqual(terminal_table(),((F('0.894557536'),F('0.945778666584')),
                                    (F('0.872081216'),F('0.6594959384'))))
 def test_complete_joint_preserves_killed_mass(self):
  c=C(diagnostic_failure=F(1,7),ticks=3,selector_wear=F(1,5),memory_flip=F(1,10))
  for p,s in product((False,True),repeat=2):
   self.assertEqual(sum(terminal_joint(c,p,s).values(),F(0)),F(6,7))
 def test_closed_formula_486_cases(self):
  count=0
  for eta,rho,bad,nu,omega in product((F(0),F(1,5),F(1,2)),
                                    (F(0),F(1,2),F(1)),
                                    (F(0),F(1,2),F(1)),
                                    (F(0),F(1,10),F(1,2)),
                                    (F(0),F(1,10),F(1,2))):
   # 243 cases, both drivers = 486. Rotate architecture variants deterministically.
   protect=(count//2)%2==0;service=(count//2)%3==0
   for driver in ('flip','silent'):
    c=C(budget=9, ticks=2,sensor_error=eta,erasure=rho,selector_bad=bad,
        health_drift=nu,memory_flip=omega,driver=driver,selector_wear=F(1,7),
        diagnostic_failure=F(1,11))
    joint=terminal_joint(c,protect,service)
    actual=optimize_terminal(joint,c.selector_errors,driver)['value']
    self.assertEqual(actual,closed_value(c,protect,service))
    if driver=='flip': self.assertEqual(actual,margin_identity(joint,c.selector_errors)['value'])
    count+=1
  self.assertEqual(count,486)
 def test_margin_identity_with_correlated_selector(self):
  table=terminal_table();errors=(F(0),F(1,2))
  for a,b,c,d in product(range(3),repeat=4):
   z=a+b+c+d
   if not z: continue
   joint={(0,0,0):F(a,2*z),(0,1,1):F(b,2*z),(1,0,0):F(c,2*z),(1,2,1):F(d,2*z)}
   self.assertEqual(margin_identity(joint,errors)['value'],optimize_terminal(joint,errors)['value'])
 def test_v7_is_nested_with_no_transport_failure(self):
  c=C(budget=5,erasure=0,sensor_error=0,selector_errors=(F(0),F(0)))
  self.assertEqual(optimize_architecture(c)['value'],F('0.908929941292'))
 def test_budget_pathwise_reserves_faulty_refresh(self):
  self.assertEqual(optimize_architecture(C(budget=4))['choice'],'skip')
  for b in range(1,10):
   ans=optimize_architecture(C(budget=b))
   self.assertTrue(all(x['cost']<=b for x in ans['options'].values()))
 def test_maintenance_can_beat_memory_protection(self):
  r=optimize_architecture(C(budget=6))
  self.assertEqual(r['choice'],'service')
  self.assertGreater(r['options']['service']['value'],r['options']['protect+diagnose']['value'])
  self.assertEqual(optimize_architecture(C(budget=7))['choice'],'protect+service')
 def test_selector_service_is_hidden_stochastic_transition(self):
  c=C(selector_wear=F(1,10),ticks=2)
  self.assertEqual(summaries(c)['bad_selector'],F(119,200))
  self.assertEqual(summaries(c,service=True)['bad_selector'],F(119,1000))
 def test_positive_information_zero_actionable_value(self):
  c=C(budget=5)
  self.assertGreater(information_before_selector(c),0)
  self.assertLess(closed_value(c),skip_value(c))
  self.assertEqual(optimize_architecture(c)['gain'],0)
 def test_fault_semantics_change_threshold(self):
  flip=C(budget=5)
  silent=replace(flip,driver='silent')
  self.assertLessEqual(closed_value(flip),skip_value(flip))
  self.assertGreater(closed_value(silent),skip_value(silent))
 def test_full_erasure_breaks_diagnosis_but_not_signaling_bypass(self):
  c=C(budget=5,erasure=1,selector_errors=(F(0),F(0)))
  self.assertEqual(closed_value(c),skip_value(c))
  # Adversarial architectural change: a durable actuator mode stores the
  # same diagnostic bit before reset. It is represented by retention=1,
  # not silently given to the original policy.
  bypass=replace(c,erasure=0)
  self.assertGreater(closed_value(bypass),skip_value(bypass))
 def test_same_marginals_different_joint_health(self):
  a={(h,h,h):F(1,2) for h in (0,1)}
  b={(h,h,1-h):F(1,2) for h in (0,1)}
  errs=(F(0),F(2,5))
  va=optimize_terminal(a,errs)['value'];vb=optimize_terminal(b,errs)['value']
  self.assertEqual(va,F('0.866412885772'))
  self.assertEqual(vb,F('0.8986857151752'))
  self.assertEqual(margin_identity(a,errs)['value'],va)
  self.assertEqual(margin_identity(b,errs)['value'],vb)
 def test_maintenance_priority_boundary(self):
  c=C(budget=7);t=terminal_table();g=t[0][1]-t[0][0];loss=t[1][0]-t[1][1]
  m=summaries(c);u=max(F(0),g-m['error']*(g+loss));th=m['theta']
  th1=summaries(c,service=True)['theta'];keep=m['keep']
  protection_gain=(1-keep)*(1-2*th)*u/2
  service_gain=(th-th1)*(loss-g+2*keep*u)/2
  self.assertEqual(closed_value(c,True,False)-closed_value(c),protection_gain)
  self.assertEqual(closed_value(c,False,True)-closed_value(c),service_gain)
  self.assertGreater(service_gain,protection_gain)
 def test_positive_information_but_finite_useful_delay(self):
  p=[]
  for n in (7,8):
   c=C(budget=20,ticks=n,selector_bad=F(1,6),erasure=F(1,5),sensor_error=0)
   p.append(closed_value(c)-skip_value(c))
   self.assertGreater(information_before_selector(c),0)
  self.assertGreater(p[0],0);self.assertLess(p[1],0)
 def test_task_aware_binary_encoder_exhaustive(self):
  count=0
  for margins in product((-2,-1,0,1,2),repeat=3):
   z=sign_partition_oracle(margins,F(1,5),F(1,3),F(1,7))
   self.assertEqual(z['enumerated'],z['sign']);count+=1
  self.assertEqual(count,125)
 def test_delay_loss_not_universal_hard_deadline(self):
  # Stable H, no bit corruption: erasure reduces gain but does not change
  # its sign when the selector is reliable and diagnosis itself is safe.
  for t in range(1,7):
   c=C(budget=20,ticks=t,sensor_error=0,erasure=F(1,3),selector_errors=(F(0),F(0)))
   self.assertGreater(closed_value(c),skip_value(c))
 def test_future_control_not_preserved_by_task_sign(self):
  # A universal action can make the first task require zero information;
  # that same compression loses the next binary identification task.
  equal_task=((F(1),F(1)),(F(1),F(1)))
  joint={(0,0,0):F(1,2),(1,1,0):F(1,2)}
  collapsed={(0,2,0):F(1,2),(1,2,0):F(1,2)}
  errs=(F(0),F(0));next_task=((F(1),F(0)),(F(0),F(1)))
  self.assertEqual(optimize_terminal(joint,errs,table=equal_task)['value'],1)
  self.assertEqual(optimize_terminal(collapsed,errs,table=equal_task)['value'],1)
  self.assertEqual(optimize_terminal(joint,errs,table=next_task)['value'],1)
  self.assertEqual(optimize_terminal(collapsed,errs,table=next_task)['value'],F(1,2))
 def test_invalid_parameters(self):
  for kw in ({'ticks':0},{'sensor_error':F(2,3)},{'budget':-1},{'driver':'anything'}):
   with self.assertRaises(ValueError): C(**kw)
if __name__=='__main__': unittest.main()
