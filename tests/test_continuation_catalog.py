import hashlib,json,unittest
from pathlib import Path

class ContinuationCatalogTests(unittest.TestCase):
    def test_historical_ledgers_remain_immutable_and_routing_is_valid(self):
        root=Path(__file__).resolve().parents[1]
        add=json.loads((root/'registry/v9-continuation-addendum.json').read_text())
        blobs=[]
        for path,sha in ((add['base_ledger'],add['base_blob_sha']),
                         (add['previous_addendum'],add['previous_blob_sha'])):
            raw=(root/'registry'/path).read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            self.assertEqual(actual,sha);blobs.append(json.loads(raw))
        base,previous=blobs;ids={x['id'] for x in base['branches']}
        self.assertEqual(len(ids),37)
        self.assertEqual(set(add['active_branches']),{'R11','R14'})
        self.assertLessEqual(len(add['active_branches']),add['active_limit'])
        all_rejected=base['rejected_simplifications']+previous['rejected_additions']+add['rejected_additions']
        self.assertEqual(len(all_rejected),23)
        self.assertEqual(len({x['id'] for x in all_rejected}),23)
        for record in add['branch_updates']+add['rejected_additions']:
            self.assertTrue(set(record['fallbacks'])<=ids)
            for path in record['provenance']:self.assertTrue((root/path).exists(),path)
        for update in add['branch_updates']:
            for key in ['remaining_gate','dead_end_trigger','minimal_test']:self.assertTrue(update[key])

if __name__=='__main__':unittest.main()
