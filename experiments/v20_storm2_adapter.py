"""Auditable adaptation to the official Stormpy2.0 API, after failed smoke run.
Sources: stormchecker/stormpy tag2.0.0 examples/02-getting-started.py,
03-getting-started.py and analysis/02-analysis.py. No solver changes.
"""
from pathlib import Path
import subprocess,sys,json
p=Path('experiments/v20_official_probe.py')
s=p.read_text()
patches={
 'stormpy.parse_properties_for_prism_program': '(lambda s,p: [stormpy.parse_property(s,p)])',
 'stormpy.build_sparse_model': 'stormpy.build_model',
 'float(result.at(model.initial_states[0]))': 'float(result[model.initial_states[0]])',
 'result.filter(stormpy.create_filter_initial_states_symbolic(model))': 'stormpy.filter_initial_states(result,model)',
 'float(result.min if not callable(result.min) else result.min())': 'float(result.get_min())',
}
for a,b in patches.items():
 if s.count(a)!=1:raise RuntimeError('unexpected probe source for '+a)
 s=s.replace(a,b)
path=Path('experiments/v20_official_probe_storm2.py');path.write_text(s)
r=subprocess.run([sys.executable,'-u',str(path)])
if r.returncode:raise SystemExit(r.returncode)
results=json.loads(Path('v20_probe_evidence/results.json').read_text())
Path('v20_probe_evidence/executed_probe.py').write_text(s)
solved=[r for r in results['rows'] if r['method'].startswith('storm') and r['status']=='ok']
if not solved:raise RuntimeError('No official Storm result: successful workflow is NOT evidence of a completed comparison')
if any(r['status']=='value_mismatch' for r in results['rows']):raise RuntimeError('solver disagreement')
print('V20_VALIDATED_OFFICIAL_ROWS',len(solved),flush=True)
