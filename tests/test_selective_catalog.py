import json,hashlib
from pathlib import Path
import unittest
class SelectiveCatalogTests(unittest.TestCase):
    def test_additive_reconciliation_and_two_active_branches(self):
        root=Path('registry');r=json.loads((root/'v18-selective-acquisition-addendum.json').read_text())
        self.assertEqual(r['active_branches'],['R11','R14']);self.assertEqual(r['active_limit'],2)
        self.assertEqual(r['combined_counts'],{'branches':50,'rejected':48})
        self.assertEqual([x['id'] for x in r['imported_local_lessons']],['D45'])
        self.assertEqual([x['id'] for x in r['rejected_additions']],['D46','D47','D48'])
        for x in r['branch_additions']+r['branch_updates']+r['imported_local_lessons']+r['rejected_additions']:
            for path in x['provenance']:self.assertTrue(Path(path).exists(),path)
        path=root/'v17-renewal-addendum.json'
        if path.exists():
            b=path.read_bytes();sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            self.assertEqual(sha,r['historical_blobs'][path.name])
if __name__=='__main__':unittest.main()
