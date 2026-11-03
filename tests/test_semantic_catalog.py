"""v12 additive research memory: preserve history and bounded active scope."""
from pathlib import Path
import hashlib,json,unittest

class SemanticCatalogTests(unittest.TestCase):
    def test_additive_catalog_and_preserved_roots(self):
        root=Path('registry');doc=json.loads((root/'v12-semantic-addendum.json').read_text())
        self.assertEqual(doc['active_branches'],['R11','R14'])
        self.assertEqual(doc['active_limit'],2)
        self.assertEqual(doc['combined_counts'],{'branches':44,'rejected':33})
        for path in ('research-options.json','v9-continuation-addendum.json','v11-trace-addendum.json'):
            b=(root/path).read_bytes()
            sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            self.assertEqual(sha,doc['historical_blobs'][path])
        base=json.loads((root/'research-options.json').read_text())
        prev=json.loads((root/'v11-trace-addendum.json').read_text())
        known={b['id'] for b in base['branches']}|{b['id'] for b in prev['branch_additions']}|{'R44'}
        self.assertEqual(len(known),44)
        for entry in doc['branch_additions']+doc['branch_updates']+doc['rejected_additions']:
            self.assertTrue(set(entry['fallbacks'])<=known)
            for path in entry['provenance']:self.assertTrue(Path(path).exists(),path)
        self.assertEqual([r['id'] for r in doc['rejected_additions']],['D30','D31','D32','D33'])
        branch=doc['branch_additions'][0]
        for k in ('hypothesis','reactivation_trigger','minimal_test','tools','acceptance_gate','fallbacks','provenance','contribution'):
            self.assertTrue(branch[k])

if __name__=='__main__':unittest.main()
