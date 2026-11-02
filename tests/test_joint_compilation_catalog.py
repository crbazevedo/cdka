import hashlib,json,unittest
from pathlib import Path
class JointCatalogTests(unittest.TestCase):
 def test_history_and_reactivation_contract(self):
  root=Path(__file__).resolve().parents[1]/'registry'
  base=json.loads((root/'research-options.json').read_text())
  new=json.loads((root/'v10-joint-compilation-addendum.json').read_text())
  expected={'research-options.json':new['base_blob_sha'],**{a['path']:a['sha'] for a in new['previous_addenda']}}
  for path,sha in expected.items():
   data=(root/path).read_bytes();self.assertEqual(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),sha)
  ids={x['id'] for x in base['branches']};self.assertEqual(len(ids),37)
  self.assertEqual(new['active_branches'],['R11','R14']);self.assertEqual(new['active_limit'],2)
  old_ids={x['id'] for x in base['rejected_simplifications']}
  for a in new['previous_addenda']:
   old_ids|={x['id'] for x in json.loads((root/a['path']).read_text())['rejected_additions']}
  added={x['id'] for x in new['rejected_additions']}
  self.assertFalse(old_ids&added);self.assertEqual(len(old_ids|added),26)
  for x in new['branch_updates']+new['rejected_additions']:
   self.assertTrue(x['provenance']);self.assertTrue(set(x['fallbacks'])<=ids)
  for x in new['branch_updates']:
   for field in ('remaining_gate','dead_end_trigger','minimal_test'):self.assertTrue(x[field])
