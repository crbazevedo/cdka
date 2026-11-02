"""Generate full exact traces, a browser dataset, and proof summaries."""
import argparse
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
from cdka.trace_microscope import (trace_program,trace_summary,endpoint_alias_witness,
    harmful_route_witness,suffix_conflict,coupling_guard,to_json,write_trace_jsonl)


def build_data():
    fixtures=[('merged',(0,0,3),(58,58,58,42)),('injective',(0,1,3),(58,58,58,42))]
    runs={};raw={}
    for name,enc,dec in fixtures:
        ts=trace_program(enc,dec,F(1,10));raw[name]=ts
        runs[name]={'encoding':enc,'decoder':dec,'summary':trace_summary(ts),'traces':list(ts)}
    summary={'endpoint_alias':endpoint_alias_witness(),'harmful_route':harmful_route_witness(),
             'suffix_conflict':suffix_conflict(),'coupling_guard':coupling_guard(),
             'trace_counts':{name:len(t)for name,t in raw.items()},
             'trace_probabilities':'exact Fraction, complete stopped prefix tree, no sampling',
             'runtime_inputs':['received_word','syndrome','balance','stage'],
             'evaluator_only':['initial_diagnostic','hidden_health','primitive_noise_flags']}
    return {'revision':'v11','base_commit':'5f4f6e05f4a83f253c4a9657e282f78acabfb509',
            'summary':summary,'runs':runs},raw


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--web');parser.add_argument('--out')
    args=parser.parse_args();data,raw=build_data();serialized=to_json(data)
    if args.web:
        p=Path(args.web);p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(serialized,ensure_ascii=False,separators=(',',':')),encoding='utf8')
    if args.out:
        out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
        for name,rows in raw.items():write_trace_jsonl(rows,out/(name+'.jsonl'))
        (out/'summary.json').write_text(json.dumps(to_json(data['summary']),indent=2,ensure_ascii=False))
        manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(out.glob('*.json*'))}
        (out/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(to_json(data['summary']),indent=2,ensure_ascii=False))

if __name__=='__main__':main()
