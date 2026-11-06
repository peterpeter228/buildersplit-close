import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
from .core import reconcile,canonical

from .artifacts import safe_cell, export_run, verify_run

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
    parser.add_argument('input',nargs='?'); parser.add_argument('--output'); parser.add_argument('--verify-run')
    args=parser.parse_args()
    try:
        if args.verify_run:
            if args.input or args.output: raise ValueError('VERIFY_ARGUMENT_CONFLICT')
            print(canonical(verify_run(args.verify_run)))
            return 0
        if not args.input or not args.output: raise ValueError('INPUT_AND_OUTPUT_REQUIRED')
        bundle,source_hash=load(args.input)
        report=export_run(bundle,source_hash,args.output)
        print(report['status'])
        return 2 if report['status']=='BLOCKED' else 0
    except (ValueError,OSError) as exc:
        print('ERROR: '+str(exc));return 2
if __name__=='__main__': raise SystemExit(main())
