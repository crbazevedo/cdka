from pathlib import Path
import hashlib,json,unittest

class PhysicalUpdateCatalogTests(unittest.TestCase):
    def test_preserved_memory_and_reusable_method(self):
        root=Path('registry');d=json.loads((root/'v13-physical-update-addendum.json').read_text())
        self.assertEqual(d['active_branches'],['R11','R14'])
        self.assertEqual(d['combined_counts'],{'branches':45,'rejected':34})
        for path,expected in d['historical_blobs'].items():
            b=(root/path).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),expected)
        self.assertEqual(d['branch_additions'][0]['id'],'R45')
        self.assertEqual(d['rejected_additions'][0]['id'],'D34')
        for entry in d['branch_additions']+d['branch_updates']+d['rejected_additions']:
            self.assertTrue(all(x.startswith('R')and 1<=int(x[1:])<=45 for x in entry['fallbacks']))
            for path in entry['provenance']:self.assertTrue(Path(path).exists())
        for k in ('prompt','manual'):
            text=Path(d['methodology'][k]).read_text()
            self.assertGreater(len(text),5000)
            self.assertIn('contrato',text.lower())
            self.assertIn('continua',text.lower())

if __name__=='__main__':unittest.main()
