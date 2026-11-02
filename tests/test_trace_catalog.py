import json,hashlib,unittest
from pathlib import Path

class TraceCatalogTests(unittest.TestCase):
    def test_append_only_catalog_and_fallbacks(self):
        root=Path(__file__).resolve().parents[1];reg=root/'registry'
        add=json.loads((reg/'v11-trace-addendum.json').read_text())
        base=json.loads((reg/'research-options.json').read_text())
        for name,expected in add['historical_blobs'].items():
            b=(reg/name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),expected)
        all_branches=base['branches']+add['branch_additions'];ids={b['id']for b in all_branches}
        self.assertEqual(len(ids),43);self.assertEqual(len(all_branches),43)
        self.assertEqual(add['active_branches'],['R11','R14'])
        self.assertTrue(all(b['status']!='active'for b in add['branch_additions']))
        rejected=base['rejected_simplifications'][:]
        for name in ['v8-transport-addendum.json','v9-continuation-addendum.json','v10-joint-compilation-addendum.json']:
            rejected+=json.loads((reg/name).read_text())['rejected_additions']
        rejected+=add['rejected_additions']
        self.assertEqual(len({x['id']for x in rejected}),29)
        for b in add['branch_additions']:
            for k in ['hypothesis','reactivation_trigger','minimal_test','tools','acceptance_gate','provenance','contribution']:
                self.assertTrue(b[k],(b['id'],k))
        for b in all_branches+rejected:
            self.assertTrue(set(b.get('fallbacks',[]))<=ids,b['id'])
        for b in add['branch_additions']+add['rejected_additions']:
            for p in b['provenance']:self.assertTrue((root/p).exists(),p)

if __name__=='__main__':unittest.main()
