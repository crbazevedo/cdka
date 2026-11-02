import hashlib,json,unittest
from pathlib import Path
class TransportCatalogTests(unittest.TestCase):
 def test_immutable_catalog_and_scoped_addendum(self):
  root=Path(__file__).resolve().parents[1]
  raw=(root/'registry/research-options.json').read_bytes();base=json.loads(raw)
  add=json.loads((root/'registry/v8-transport-addendum.json').read_text())
  blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  self.assertEqual(blob,add['base_blob_sha'])
  self.assertEqual(len(base['branches']),37)
  ids={x['id'] for x in base['branches']}
  self.assertEqual(set(add['active_branches']),{'R11','R14'})
  self.assertLessEqual(len(add['active_branches']),add['active_limit'])
  for x in add['branch_updates']:
   self.assertIn(x['id'],ids);self.assertTrue(set(x['fallbacks'])<=ids)
   for k in ('remaining_gate','dead_end_trigger','minimal_test','evidence'):self.assertTrue(x[k])
  combined=base['rejected_simplifications']+add['rejected_additions']
  self.assertEqual(len(combined),20);self.assertEqual(len({x['id'] for x in combined}),20)
  for x in add['rejected_additions']:self.assertTrue(set(x['fallbacks'])<=ids)
  for path in ['docs/articles/T4I.md','docs/results/T4I-diagnosis-through-repair.md','docs/lab/diagnostic_transport.html']:
   self.assertTrue((root/path).exists(),path)
if __name__=='__main__':unittest.main()
