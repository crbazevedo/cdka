from pathlib import Path
import unittest,hashlib,json

class RenewalCatalogTests(unittest.TestCase):
    def test_preserve_history_and_two_active_proof_branches(self):
        root=Path('registry');d=json.loads((root/'v17-renewal-addendum.json').read_text())
        self.assertEqual(d['active_branches'],['R11','R14'])
        self.assertEqual(d['combined_counts'],{'branches':49,'rejected':44})
        for name,expected in d['historical_blobs'].items():
            b=(root/name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),expected)
        self.assertEqual([x['id'] for x in d['rejected_additions']],['D43','D44'])
        for e in d['branch_additions']+d['branch_updates']+d['rejected_additions']:
            self.assertTrue(e['fallbacks'])
            for file in e['provenance']:self.assertTrue(Path(file).exists(),file)
        self.assertTrue(Path(d['integration_note']).exists())

if __name__=='__main__':unittest.main()
