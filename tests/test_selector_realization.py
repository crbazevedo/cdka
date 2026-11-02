from fractions import Fraction as F
from itertools import product
import unittest
from cdka.selector_realization import erasure_selector

class SelectorRealizationTests(unittest.TestCase):
    def test_exact_physical_realization_of_every_grid_prescription(self):
        grid=tuple(F(i,4) for i in range(5))
        for f0,f1,sigma in product(grid,repeat=3):
            if abs(f1-f0)>sigma:
                with self.assertRaises(ValueError): erasure_selector(f0,f1,sigma)
            else:
                r,b0,b1=erasure_selector(f0,f1,sigma)
                self.assertTrue(all(0<=x<=1 for x in (r,b0,b1)))
                self.assertEqual((1-sigma)*r+sigma*b0,f0)
                self.assertEqual((1-sigma)*r+sigma*b1,f1)
