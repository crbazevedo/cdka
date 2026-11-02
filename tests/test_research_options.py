import json
from pathlib import Path
import unittest

class ResearchLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book=json.loads((Path(__file__).resolve().parents[1]/'registry'/'research-options.json').read_text())
    def test_unique_named_branches_and_limited_active_work(self):
        rows=self.book['branches'];ids={b['id'] for b in rows}
        self.assertEqual(len(rows),32);self.assertEqual(len(ids),32)
        active=[b['id'] for b in rows if b['status']=='active']
        self.assertEqual(set(active),{'R11','R14'})
        self.assertLessEqual(len(active),self.book['active_limit'])
    def test_no_orphaned_options_or_empty_exit_rules(self):
        ids={b['id'] for b in self.book['branches']}
        for b in self.book['branches']:
            for key in ('hypothesis','reactivation_trigger','minimal_test','tools','acceptance_gate','fallbacks','provenance','novelty_status'):
                self.assertTrue(b[key],(b['id'],key))
            self.assertTrue(set(b['fallbacks'])<=ids)
            self.assertNotIn(b['id'],b['fallbacks'])
    def test_refuted_shortcuts_keep_their_reason_and_fallback(self):
        entries=self.book['rejected_simplifications'];ids={b['id'] for b in self.book['branches']}
        self.assertEqual(len(entries),14);self.assertEqual(len({e['id'] for e in entries}),14)
        for e in entries:
            self.assertTrue(e['claim'] and e['reason']);self.assertTrue(set(e['fallbacks'])<=ids)
    def test_browser_catalog_matches_authoritative_source(self):
        root=Path(__file__).resolve().parents[1]
        rendered=json.loads((root/'docs/lab/research-options.json').read_text())
        self.assertEqual(self.book,rendered)

if __name__=='__main__':unittest.main()
