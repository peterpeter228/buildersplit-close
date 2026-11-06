import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
from .core import reconcile,canonical

def safe_cell(value):
    value=str(value)
    return "'"+value if value.lstrip().startswith(('=','+','-','@','\t','\r')) else value

def load(path):
    path=Path(path)
    if path.is_symlink() or any(p.is_symlink() for p in path.parents): raise ValueError('SYMLINK_REJECTED')
    with path.open('rb') as handle:
        raw=handle.read(50*1024*1024+1)
    if len(raw)>50*1024*1024: raise ValueError('INPUT_LIMIT_EXCEEDED')
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result: raise ValueError('DUPLICATE_JSON_KEY')
            result[key]=value
        return result
    bundle=json.loads(raw.decode('utf-8'),object_pairs_hook=unique,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
    if not isinstance(bundle,dict): raise ValueError('SCHEMA_INVALID')
    return bundle,hashlib.sha256(raw).hexdigest()

def main():
    parser=argparse.ArgumentParser(description='BuilderSplit Close G0 synthetic experiment')
    parser.add_argument('input'); parser.add_argument('--output',required=True)
    args=parser.parse_args()
    try:
        bundle,source_hash=load(args.input)
        report=reconcile(bundle)
        output=Path(args.output)
        if any(p.is_symlink() for p in [output,*output.parents]): raise ValueError('SYMLINK_REJECTED')
        output.mkdir(parents=False,exist_ok=False)
        report['input_sha256']=source_hash
        (output/'report.json').write_text(canonical(report)+'\n',encoding='utf-8')
        columns=['beneficiary_id','currency_id','opening','accrual','external_paid','closing_calculated','customer_closing_statement','statement_variance']
        with (output/'reconciliation.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f);writer.writerow(columns)
            for row in report['calculations']: writer.writerow([safe_cell(row[c]) for c in columns])
        (output/'README.txt').write_text('SYNTHETIC TECHNICAL EXPERIMENT ONLY. Not a customer report, payment instruction, or validated product. Inspect report.json status and limitations.\n',encoding='utf-8')
        print(report['status'])
        return 2 if report['status']=='BLOCKED' else 0
    except (ValueError,OSError) as exc:
        print('ERROR: '+str(exc));return 2
if __name__=='__main__': raise SystemExit(main())
