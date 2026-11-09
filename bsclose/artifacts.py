"""Completion markers detect partial exports, corruption and replay mismatches.
Hashes are integrity checks, not signatures or protection from a malicious writer.
"""
import csv
import hashlib
import io
import re
from datetime import datetime, timezone
import json
from pathlib import Path
from .core import canonical, reconcile, stamp, Invalid

FILES = ('input.json','report.json','reconciliation.csv','README.txt')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe_cell(value):
    value=str(value)
    return "'"+value if value.lstrip().startswith(('=','+','-','@','\t','\r')) else value

def numeric_cell(value):
    # Derived sums may exceed the 100-character input limit. The engine's
    # precision is 256 and scale <=18; retain a separate bounded output grammar.
    if not isinstance(value, str) or len(value)>300 or not re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?', value):
        raise Invalid('DECIMAL_INVALID')
    return value

def check_path(path):
    path=Path(path)
    if any(p.is_symlink() for p in [path,*path.parents]):
        raise ValueError('SYMLINK_REJECTED')
    return path

def csv_render(report):
    stream=io.StringIO(newline='')
    columns=['beneficiary_id','currency_id','opening','accrual','external_paid','closing_calculated','customer_closing_statement','statement_variance']
    writer=csv.writer(stream);writer.writerow(columns)
    for row in report['calculations']:
        # Only fixed numeric schema columns bypass text escaping, after strict
        # decimal validation. Identifiers always remain formula-protected.
        writer.writerow([safe_cell(row[c]) if c in columns[:2] else
                         numeric_cell(row[c]) for c in columns])
    return stream.getvalue().encode('utf-8')

def export_run(bundle, source_hash, output):
    output=check_path(output)
    output.mkdir(parents=False,exist_ok=False)
    evaluated=datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
    report=reconcile(bundle,now=stamp(evaluated))
    report['evaluation_as_of']=evaluated
    report['input_sha256']=source_hash
    (output/'input.json').write_text(canonical(bundle)+'\n',encoding='utf-8')
    (output/'report.json').write_text(canonical(report)+'\n',encoding='utf-8')
    (output/'reconciliation.csv').write_bytes(csv_render(report))
    (output/'README.txt').write_text('SYNTHETIC TECHNICAL EXPERIMENT ONLY. Not a customer report or payment instruction. COMPLETED.json must verify before using this diagnostic. Hashes are not signatures.\n',encoding='utf-8')
    marker={'schema':'bsclose.artifacts.v1','files':{name:sha((output/name).read_bytes()) for name in FILES},'business_hash':report['business_hash'],'status':report['status']}
    # Written last: an interrupted export lacks a valid completed marker.
    with (output/'COMPLETED.json').open('x',encoding='utf-8') as f:
        f.write(canonical(marker)+'\n')
    return report

def verify_run(path):
    path=check_path(path)
    try:
        marker_path=check_path(path/'COMPLETED.json')
        if marker_path.stat().st_size>16384: raise ValueError('MARKER_INVALID')
        marker=json.loads(marker_path.read_text(encoding='utf-8'))
        if marker.get('schema')!='bsclose.artifacts.v1' or set(marker.get('files',{}))!=set(FILES): raise ValueError('MARKER_INVALID')
        for name in FILES:
            file=check_path(path/name)
            if file.stat().st_size>50*1024*1024: raise ValueError('INPUT_LIMIT_EXCEEDED')
            if sha(file.read_bytes())!=marker['files'][name]: raise ValueError('ARTIFACT_HASH_MISMATCH:'+name)
        report=json.loads((path/'report.json').read_text(encoding='utf-8'))
        bundle=json.loads((path/'input.json').read_text(encoding='utf-8'))
        replay=reconcile(bundle,now=stamp(report['evaluation_as_of']))
        expected={**replay,'evaluation_as_of':report['evaluation_as_of'],'input_sha256':report['input_sha256']}
        if canonical(expected)!=canonical(report): raise ValueError('REPORT_REPLAY_MISMATCH')
        if (path/'reconciliation.csv').read_bytes()!=csv_render(replay): raise ValueError('CSV_REPLAY_MISMATCH')
        if marker['business_hash']!=report['business_hash'] or replay['business_hash']!=report['business_hash'] or replay['status']!=marker['status']:
            raise ValueError('REPLAY_MISMATCH')
        return {'integrity':'VERIFIED','status':replay['status'],'business_hash':replay['business_hash'],'note':'Synthetic diagnostic replay only; not authenticated customer evidence.'}
    except (OSError,KeyError,TypeError,AttributeError,json.JSONDecodeError) as exc:
        raise ValueError('INCOMPLETE_OR_INVALID_RUN') from exc
