import copy
from datetime import datetime,timezone
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from bsclose.artifacts import export_run,verify_run,sha
from bsclose.core import reconcile
from test_core import sample

class Artifacts(unittest.TestCase):
    def test_repacked_contradictory_report(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'run';export_run(sample(),'fixture',run)
            report=json.loads((run/'report.json').read_text());report['calculations'][0]['closing_calculated']='999999';report['status']='REVIEW_READY'
            (run/'report.json').write_text(json.dumps(report))
            marker=json.loads((run/'COMPLETED.json').read_text());marker['files']['report.json']=sha((run/'report.json').read_bytes());(run/'COMPLETED.json').write_text(json.dumps(marker))
            with self.assertRaisesRegex(ValueError,'REPORT_REPLAY_MISMATCH'):verify_run(run)
    def test_repacked_wrong_csv(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'run';export_run(sample(),'fixture',run);(run/'reconciliation.csv').write_text('wrong')
            marker=json.loads((run/'COMPLETED.json').read_text());marker['files']['reconciliation.csv']=sha((run/'reconciliation.csv').read_bytes());(run/'COMPLETED.json').write_text(json.dumps(marker))
            with self.assertRaisesRegex(ValueError,'CSV_REPLAY_MISMATCH'):verify_run(run)
    def test_fixed_evaluation_time(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'run'
            with patch('bsclose.artifacts.datetime') as clock:
                clock.now.return_value=datetime(2000,1,1,tzinfo=timezone.utc)
                export_run(sample(),'fixture',run)
            self.assertEqual(verify_run(run)['status'],'BLOCKED')
    def test_backup_replay(self):
        with tempfile.TemporaryDirectory() as d:
            original=Path(d)/'one';backup=Path(d)/'copy'
            export_run(sample(),'fixture',original)
            shutil.copytree(original,backup)
            self.assertEqual(verify_run(original),verify_run(backup))
            self.assertEqual(verify_run(backup)['status'],'DIAGNOSTIC_ONLY')
    def test_tampering_each_file(self):
        for name in ['input.json','report.json','reconciliation.csv','README.txt']:
            with tempfile.TemporaryDirectory() as d:
                run=Path(d)/'run';export_run(sample(),'fixture',run)
                with (run/name).open('a') as f:f.write('tamper')
                with self.assertRaisesRegex(ValueError,'ARTIFACT_HASH_MISMATCH'):verify_run(run)
    def test_missing_marker(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'INCOMPLETE'):verify_run(d)
    def test_disk_write_failure(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'run'
            with patch.object(Path,'write_text',side_effect=OSError('simulated disk full')):
                with self.assertRaises(OSError):export_run(sample(),'fixture',run)
            self.assertFalse((run/'COMPLETED.json').exists())
            with self.assertRaises(ValueError):verify_run(run)
    def test_existing_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'run';export_run(sample(),'fixture',run);before=verify_run(run)
            with self.assertRaises(FileExistsError):export_run(sample(),'fixture',run)
            self.assertEqual(before,verify_run(run))
    def test_symlink_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'run';export_run(sample(),'fixture',run);file=run/'README.txt';backup=Path(d)/'readme';file.rename(backup);file.symlink_to(backup)
            with self.assertRaisesRegex(ValueError,'SYMLINK'):verify_run(run)
    def test_blocked_replay_not_upgrade(self):
        with tempfile.TemporaryDirectory() as d:
            b=sample();del b['balances'][0]['opening'];run=Path(d)/'run';export_run(b,'fixture',run)
            self.assertEqual(verify_run(run)['status'],'BLOCKED')
    def test_capacity_50000(self):
        b=sample();base=b['fills'][0];b['fills']=[{**base,'canonical_fill_id':str(i)} for i in range(50000)]
        r=reconcile(b);self.assertEqual(r['status'],'DIAGNOSTIC_ONLY');self.assertEqual(r['calculations'][0]['accrual'],'1500000.00000000')
        b['fills'].append({**base,'canonical_fill_id':'extra'});r=reconcile(b);self.assertEqual(r['status'],'BLOCKED');self.assertIn('INPUT_LIMIT_EXCEEDED',[x['code'] for x in r['issues']])
