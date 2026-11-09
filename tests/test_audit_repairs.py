import csv
import io
import unittest
import tempfile
from pathlib import Path
from datetime import timedelta
from unittest.mock import patch
from test_core import sample
from bsclose import core
from bsclose.artifacts import csv_render, export_run, verify_run

class AuditRepairs(unittest.TestCase):
    def blocked(self, bundle, code):
        report=core.reconcile(bundle)
        self.assertEqual(report['status'],'BLOCKED')
        self.assertEqual(report['calculations'],[])
        self.assertIn(code,[x['code'] for x in report['issues']])

    def test_unmatched_rules_validated(self):
        cases=[('rate','NaN','DECIMAL_INVALID'),('rate','1.01','RATE_INVALID'),
               ('rate','-0.1','RATE_INVALID'),('from','bad','TIMESTAMP_UNIT_UNKNOWN'),
               ('fee_basis','UNKNOWN','FEE_BASIS_UNKNOWN'),
               ('to','2026-10-01T00:00:00Z','RULE_INTERVAL_INVALID')]
        for field,value,code in cases:
            with self.subTest(field=field,value=value):
                b=sample();b['rules'].append({**b['rules'][0],'account':'unmatched',field:value})
                self.blocked(b,code)

    def test_no_fills_still_validate_rules(self):
        b=sample();b['fills']=[];b['rules'][0]['rate']='Infinity'
        self.blocked(b,'DECIMAL_INVALID')

    def test_unmatched_overlaps_blocked(self):
        b=sample()
        b['rules'] += [{**b['rules'][0],'account':'other'}]*2
        self.blocked(b,'RULE_OVERLAP')

    def test_adjacent_intervals_and_gap(self):
        b=sample();mid='2026-10-04T00:00:00Z'
        b['rules']=[{**b['rules'][0],'to':mid},{**b['rules'][0],'from':mid,'rate':'0.25'}]
        b['fills'][0]['occurred_at']=mid
        self.assertEqual(core.reconcile(b)['calculations'][0]['accrual'],'15.00000000')
        b['rules']=b['rules'][:1];self.blocked(b,'RULE_GAP')

    def test_caps_before_row_validation(self):
        for name,limit in [('rules',core.MAX_RULES),('payments',core.MAX_PAYMENTS)]:
            b=sample();b[name]=[None]*(limit+1)
            self.blocked(b,'INPUT_LIMIT_EXCEEDED')

    def test_rule_bound_and_parse_work(self):
        b=sample()
        b['rules']=[{**b['rules'][0],'account':str(i)} for i in range(core.MAX_RULES)]
        b['rules'][0]['account']='a'
        b['fills']=[{**b['fills'][0],'canonical_fill_id':str(i)} for i in range(1000)]
        with patch.object(core,'stamp',wraps=core.stamp) as stamp:
            report=core.reconcile(b)
        self.assertEqual(report['status'],'DIAGNOSTIC_ONLY')
        # No F x R timestamp parsing: once per rule plus fill/payment/cutoffs.
        self.assertLess(stamp.call_count,2*core.MAX_RULES+1100)

    def test_payment_bound(self):
        b=sample()
        b['payments']=[{**b['payments'][0],'receipt_event_key':str(i),'applied':'0'} for i in range(core.MAX_PAYMENTS)]
        self.assertEqual(core.reconcile(b)['status'],'DIAGNOSTIC_ONLY')

    def test_negative_numeric_export(self):
        b=sample();b['balances'][0]['opening']='0'
        row=next(csv.DictReader(io.StringIO(csv_render(core.reconcile(b)).decode())))
        self.assertEqual(row['closing_calculated'],'-5.00000000')
        self.assertEqual(row['statement_variance'],'-17.00000000')

    def test_csv_text_escaped_numeric_injection_rejected(self):
        report=core.reconcile(sample())
        for value in ['=SUM(A1)',' +1','-3','@test']:
            report['calculations'][0]['beneficiary_id']=value
            row=next(csv.DictReader(io.StringIO(csv_render(report).decode())))
            self.assertTrue(row['beneficiary_id'].startswith("'"))
        report['calculations'][0]['opening']='-1+CMD'
        with self.assertRaises(core.Invalid):csv_render(report)

    def test_rules_order_invariant(self):
        b=sample();b['rules'].append({**b['rules'][0],'account':'unmatched'})
        first=core.reconcile(b);b['rules'].reverse()
        self.assertEqual(first['business_hash'],core.reconcile(b)['business_hash'])

    def test_large_derived_numeric_export_replay(self):
        b=sample();b['balances'][0]['opening']='9'*100
        with tempfile.TemporaryDirectory() as folder:
            report=export_run(b,core.digest(b),Path(folder)/'run')
            self.assertEqual(report['status'],'DIAGNOSTIC_ONLY')
            self.assertGreater(len(report['calculations'][0]['closing_calculated']),100)
            self.assertEqual(verify_run(Path(folder)/'run')['integrity'],'VERIFIED')
