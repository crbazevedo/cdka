from pathlib import Path
import json,unittest

class RecurrentCatalogTests(unittest.TestCase):
    def test_research_memory_and_scope_preserved(self):
        x=json.loads(Path('registry/v16-recurrent-learning-addendum.json').read_text())
        self.assertEqual(x['active_branches'],['R11','R14'])
        self.assertEqual(x['active_limit'],2)
        self.assertEqual(x['combined_counts'],{'branches':48,'rejected':42})
        self.assertEqual([r['id'] for r in x['rejected_additions']],['D41','D42'])
        self.assertEqual(x['branch_additions'][0]['id'],'R48')
        valid={'R'+str(i) for i in range(1,49)}
        for row in x['branch_additions']+x['branch_updates']+x['rejected_additions']:
            self.assertTrue(set(row['fallbacks'])<=valid)
            for p in row['provenance']:self.assertTrue(Path(p).exists(),p)
        self.assertTrue(Path(x['learning_compass']).exists())
        for field in ('hypothesis','reactivation_trigger','minimal_test','tools','acceptance_gate','contribution'):
            self.assertTrue(x['branch_additions'][0][field])
        self.assertIn('capacidade',Path(x['learning_compass']).read_text())

if __name__=='__main__':unittest.main()
