from fractions import Fraction as F
import unittest
from cdka.boundary_voting import portfolio, task_value, circuit_triplet_channel, SEQUENTIAL

class MaintenanceMixtureTest(unittest.TestCase):
    def test_maintained_bank_is_not_its_mean_gate_rate(self):
        exact={r['id']:r['value'] for r in portfolio()}['triple_voter_maintained']
        average=F(4,5)*F(1,1000)+F(1,5)*F(1,50)
        naive=task_value(circuit_triplet_channel(SEQUENTIAL,F(1,50),average))
        self.assertNotEqual(exact,naive)

if __name__=='__main__':unittest.main()
