from pathlib import Path
import hashlib,json,unittest

class BoundaryCatalogTests(unittest.TestCase):
    def test_preserved_catalog_and_bounded_scope(self):
        root=Path('registry');d=json.loads((root/'v15-realized-correction-addendum.json').read_text())
        self.assertEqual(d['active_branches'],['R11','R14'])
        self.assertEqual(d['active_limit'],2)
        self.assertEqual(d['combined_counts'],{'branches':47,'rejected':40})
        for name in ('research-options.json','v12-semantic-addendum.json'):
            b=(root/name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),d['historical_blobs'][name])
        known={'R'+str(i) for i in range(1,48)}
        for item in d['branch_additions']+d['branch_updates']+d['rejected_additions']:
            self.assertTrue(set(item['fallbacks'])<=known)
            for path in item['provenance']:self.assertTrue(Path(path).exists(),path)
        self.assertEqual([x['id'] for x in d['rejected_additions']],['D38','D39','D40'])
        self.assertEqual(d['branch_additions'][0]['status'],'instrument')

if __name__=='__main__':unittest.main()
