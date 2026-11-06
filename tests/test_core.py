import copy
import json
import tempfile
import unittest
from pathlib import Path
from bsclose.core import reconcile,money,Invalid
from bsclose.__main__ import load,safe_cell

def sample():
    start='2026-10-01T00:00:00Z'; end='2026-10-08T00:00:00Z'; builder='0x'+'1'*40; currency='hypercore-mainnet:USDC'
    return {'schema_version':'bsclose.synthetic.v1','sample_class':'SYNTHETIC','network':'hypercore-mainnet','builder':builder,'period_start':start,'period_end':end,'close_group_id':'demo','fee_currency_id':currency,'coverage':'SOURCE_SUPPORTED','coverage_evidence':'SYNTHETIC CONTROL','verified_market_ids':['BTC'],'rounding':{'stage':'PER_FILL','scale':8,'mode':'HALF_EVEN'},'payments_confirmed':True,'allocation_snapshot_confirmed':True,'fills':[{'canonical_fill_id':'account:100000000000000000001','identity_evidence':'fixture','occurred_at':start,'builder':builder,'attribution_evidence':'fixture','market_id':'BTC','market_class':'validator-operated-perp','fee_currency_id':currency,'fee_basis':'GROSS','native_split_presence':'NO','builder_fee':'60','account':'a'}],'rules':[{'account':'a','beneficiary_id':'b','from':start,'to':end,'fee_basis':'GROSS','rate':'0.5'}],'balances':[{'beneficiary_id':'b','opening':'20','closing_statement':'12','opening_cutoff':start,'closing_cutoff':end,'confirmation_evidence':'fixture','independent_statement_evidence':'fixture'}],'payments':[{'beneficiary_id':'b','receipt_event_key':'fixture:tx:log0','evidence':'fixture','status':'CONFIRMED','channel':'EXTERNAL','currency_id':currency,'occurred_at':start,'close_group_id':'demo','confirmed_total':'35','applied':'35','other_group_allocated':'0'}]}

class Tests(unittest.TestCase):
    def check_block(self,b,code):
        r=reconcile(b);self.assertEqual(r['status'],'BLOCKED');self.assertEqual(r['calculations'],[]);self.assertIn(code,[x['code'] for x in r['issues']])
    def test_golden(self):
        r=reconcile(sample());self.assertEqual(r['status'],'DIAGNOSTIC_ONLY');self.assertFalse(r['commercial_g0_passed']);self.assertEqual(r['calculations'][0]['closing_calculated'],'15.00000000');self.assertEqual(r['calculations'][0]['statement_variance'],'3.00000000')
    def test_unsupported_adjustments(self):
        b=sample();b['adjustments']=[{'amount':'10'}];self.check_block(b,'UNSUPPORTED_INPUT_FIELDS')
    def test_malformed_row(self):
        b=sample();b['fills']=[None];self.check_block(b,'SCHEMA_INVALID')
    def test_negative(self):
        b=sample();b['balances'][0]['opening']='0';self.assertEqual(reconcile(b)['calculations'][0]['closing_calculated'],'-5.00000000')
    def test_duplicate(self):
        b=sample();b['fills']*=2;self.assertEqual(reconcile(b)['calculations'],reconcile(sample())['calculations'])
    def test_conflict(self):
        b=sample();b['fills'].append({**b['fills'][0],'builder_fee':'61'});self.check_block(b,'CANONICAL_ID_CONFLICT')
    def test_native(self):
        b=sample();b['fills'][0]['native_split_presence']='YES';self.check_block(b,'NATIVE_SPLIT_UNCALIBRATED')
    def test_missing_balances(self):
        for field,code in [('opening','OPENING_BALANCE_UNKNOWN'),('closing_statement','CLOSING_STATEMENT_MISSING')]:
            b=sample();del b['balances'][0][field];self.check_block(b,code)
    def test_unknowns(self):
        for field,value,code in [('fee_currency_id','unknown','FEE_TOKEN_UNKNOWN'),('fee_basis','UNKNOWN','FEE_BASIS_UNKNOWN'),('builder','','BUILDER_ATTRIBUTION_MISSING'),('market_class','spot','MARKET_UNSUPPORTED')]:
            b=sample();b['fills'][0][field]=value;self.check_block(b,code)
    def test_rules(self):
        b=sample();b['rules']*=2;self.check_block(b,'RULE_OVERLAP')
        b['rules']=[];self.check_block(b,'RULE_GAP')
    def test_end_excluded(self):
        b=sample();b['fills'][0]['occurred_at']=b['period_end'];self.assertEqual(reconcile(b)['calculations'][0]['accrual'],'0')
    def test_payments(self):
        for field,value,code in [('status','PENDING','PAYMENT_UNVERIFIED'),('other_group_allocated','1','PAYMENT_OVERALLOCATED'),('close_group_id','other','PAYMENT_WRONG_GROUP'),('occurred_at','2026-10-08T00:00:00Z','PAYMENT_OUTSIDE_PERIOD')]:
            b=sample();b['payments'][0][field]=value;self.check_block(b,code)
    def test_payment_duplicate(self):
        b=sample();b['payments']*=2;self.check_block(b,'PAYMENT_DUPLICATE_RECEIPT')
    def test_declared_coverage(self):
        b=sample();b['coverage']='DECLARED_ONLY';self.check_block(b,'SOURCE_COVERAGE_UNPROVEN')
    def test_not_real_adapter(self):
        b=sample();b['sample_class']='CUSTOMER_AUTHORIZED';self.check_block(b,'ADAPTER_UNVALIDATED')
    def test_decimal(self):
        for value in ['NaN','Infinity','1e2','1,000',0.1]:
            with self.assertRaises(Invalid): money(value)
        self.assertEqual(str(money('0.000000000123')),'1.23E-10')
    def test_precision(self):
        b=sample();b['fills'][0]['builder_fee']='0.000000123';b['rounding']['scale']=12;self.assertEqual(reconcile(b)['calculations'][0]['accrual'],'0.000000061500')
    def test_rounding(self):
        b=sample();b['rounding']['scale']=0;b['fills'][0]['builder_fee']='1';b['fills'].append({**b['fills'][0],'canonical_fill_id':'second'});self.assertEqual(reconcile(b)['calculations'][0]['accrual'],'0');b['rounding']['stage']='PER_RECIPIENT_PERIOD';self.assertEqual(reconcile(b)['calculations'][0]['accrual'],'1')
    def test_order(self):
        b=sample();b['fills'].append({**b['fills'][0],'canonical_fill_id':'second'});r=reconcile(b);b['fills'].reverse();self.assertEqual(r['business_hash'],reconcile(b)['business_hash'])
    def test_input_guards(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_text('{"x":1,"x":2}')
            with self.assertRaises(ValueError):load(p)
            link=Path(d)/'link';link.symlink_to(p)
            with self.assertRaises(ValueError):load(link)
    def test_csv(self):
        for value in ['=1+1',' @SUM(A1)','-3','+1']:
            self.assertTrue(safe_cell(value).startswith("'"))
    def test_open_period(self):
        b=sample();b['period_start']='2099-01-01T00:00:00Z';b['period_end']='2099-01-08T00:00:00Z';self.check_block(b,'PERIOD_OPEN')
if __name__=='__main__':unittest.main()
