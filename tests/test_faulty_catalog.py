from pathlib import Path
import json,unittest

class FaultyCatalogTests(unittest.TestCase):
    def test_additive_ledger(self):
        p=Path('registry');d=json.loads((p/'v14-stochastic-boundary-addendum.json').read_text());old=json.loads((p/'v13-physical-update-addendum.json').read_text())
        self.assertEqual(d['active_branches'],['R11','R14']);self.assertEqual(d['active_limit'],2)
        self.assertEqual(d['combined_counts'],{'branches':46,'rejected':37})
        self.assertEqual(old['combined_counts'],{'branches':45,'rejected':34})
        self.assertEqual([x['id'] for x in d['rejected_additions']],['D35','D36','D37'])
        self.assertEqual(d['branch_additions'][0]['id'],'R46')
        for a in d['branch_additions']+d['branch_updates']+d['rejected_additions']:
            for f in a['fallbacks']:self.assertTrue(f.startswith('R') and 1<=int(f[1:])<=46)
            for file in a['provenance']:self.assertTrue(Path(file).exists())
        for f in ['docs/synthesis/finite-core-v9-v14.md','docs/strategy/proof-engine-v14.md','docs/articles/T4O.md']:self.assertTrue(Path(f).exists())

if __name__=='__main__':unittest.main()
