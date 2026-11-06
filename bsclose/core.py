"""Offline G0 experiment. Synthetic normalized adapter, not a production ledger."""
import hashlib
import json
import re
from datetime import datetime, timezone
from decimal import Decimal, localcontext, ROUND_HALF_EVEN, ROUND_DOWN

VERSION = '0.1.0-experiment'
class Invalid(ValueError):
    pass

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def money(value):
    if not isinstance(value, str) or len(value)>100 or not re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?', value):
        raise Invalid('DECIMAL_INVALID')
    return Decimal(value)

def stamp(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,3})?Z', value):
        raise Invalid('TIMESTAMP_UNIT_UNKNOWN')
    try:
        parsed = datetime.fromisoformat(value[:-1]+'+00:00')
    except ValueError as exc:
        raise Invalid('TIMESTAMP_UNIT_UNKNOWN') from exc
    return parsed

def textnum(value):
    return format(value, 'f')

def reconcile(bundle, now=None):
    """No externally asserted evidence can upgrade this experimental adapter."""
    issues=[]
    def fail(code, ref='manifest'):
        issues.append({'code':code,'ref':str(ref)})
    rows=[]
    counts={'input_fills':0,'confirmed_duplicates':0,'outside_period':0}
    try:
        allowed={'schema_version','sample_class','network','builder','period_start','period_end','close_group_id','fee_currency_id','coverage','coverage_evidence','verified_market_ids','rounding','payments_confirmed','allocation_snapshot_confirmed','fills','rules','balances','payments'}
        if set(bundle)-allowed: raise Invalid('UNSUPPORTED_INPUT_FIELDS')
        def nonempty(value):
            return isinstance(value,str) and bool(value.strip())
        if not nonempty(bundle.get('close_group_id')): raise Invalid('CLOSE_GROUP_INVALID')
        if not nonempty(bundle.get('coverage_evidence')): fail('SOURCE_COVERAGE_UNPROVEN')
        if bundle.get('schema_version')!='bsclose.synthetic.v1': raise Invalid('SCHEMA_UNSUPPORTED')
        if bundle.get('sample_class')!='SYNTHETIC': raise Invalid('ADAPTER_UNVALIDATED')
        start,end=stamp(bundle['period_start']),stamp(bundle['period_end'])
        if (end-start).total_seconds()!=604800: raise Invalid('PERIOD_INVALID')
        if end>(now or datetime.now(timezone.utc)): raise Invalid('PERIOD_OPEN')
        if not re.fullmatch(r'0x[0-9a-fA-F]{40}',bundle['builder']): raise Invalid('BUILDER_INVALID')
        if bundle.get('network')!='hypercore-mainnet': raise Invalid('NETWORK_UNSUPPORTED')
        if bundle.get('fee_currency_id')!='hypercore-mainnet:USDC': raise Invalid('FEE_TOKEN_UNKNOWN')
        if bundle.get('coverage')!='SOURCE_SUPPORTED' or not bundle.get('coverage_evidence'): fail('SOURCE_COVERAGE_UNPROVEN')
        fills=bundle['fills']; rules=bundle['rules']; balances=bundle['balances']; payments=bundle['payments']
        if not all(isinstance(v,list) for v in [fills,rules,balances,payments]): raise Invalid('SCHEMA_INVALID')
        if len(fills)>50000 or len(balances)>100: raise Invalid('INPUT_LIMIT_EXCEEDED')
        if bundle.get('payments_confirmed') is not True or bundle.get('allocation_snapshot_confirmed') is not True: fail('ALLOCATION_SNAPSHOT_UNKNOWN')
        markets=bundle.get('verified_market_ids')
        if not isinstance(markets,list) or not markets or any(not isinstance(v,str) or not v for v in markets): raise Invalid('MARKET_REGISTRY_INVALID')
        schemas={
            'fills': {'canonical_fill_id','identity_evidence','occurred_at','builder','attribution_evidence','market_id','market_class','fee_currency_id','fee_basis','native_split_presence','builder_fee','account'},
            'rules': {'account','beneficiary_id','from','to','fee_basis','rate'},
            'balances': {'beneficiary_id','opening','closing_statement','opening_cutoff','closing_cutoff','confirmation_evidence','independent_statement_evidence'},
            'payments': {'beneficiary_id','receipt_event_key','evidence','status','channel','currency_id','occurred_at','close_group_id','confirmed_total','applied','other_group_allocated'}
        }
        for collection,fields in schemas.items():
            for row in bundle[collection]:
                if not isinstance(row,dict): raise Invalid('SCHEMA_INVALID')
                if set(row)-fields: raise Invalid('UNSUPPORTED_INPUT_FIELDS')
        string_fields={
            'fills':['canonical_fill_id','identity_evidence','occurred_at','builder','attribution_evidence','market_id','market_class','fee_currency_id','fee_basis','native_split_presence','builder_fee','account'],
            'rules':['account','beneficiary_id','from','to','fee_basis','rate'],
            'balances':['beneficiary_id','opening_cutoff','closing_cutoff','confirmation_evidence','independent_statement_evidence'],
            'payments':['beneficiary_id','receipt_event_key','evidence','status','channel','currency_id','occurred_at','close_group_id','confirmed_total','applied','other_group_allocated']
        }
        for collection,fields in string_fields.items():
            for row in bundle[collection]:
                if any(not nonempty(row.get(field)) for field in fields):
                    fail('SCHEMA_INVALID',collection)
        policy=bundle['rounding']
        if not isinstance(policy,dict) or set(policy)!={'stage','scale','mode'}: raise Invalid('ROUNDING_INVALID')
        if policy['stage'] not in ('PER_FILL','PER_RECIPIENT_PERIOD'): raise Invalid('ROUNDING_INVALID')
        if type(policy['scale']) is not int or not 0<=policy['scale']<=18: raise Invalid('ROUNDING_INVALID')
        mode={'HALF_EVEN':ROUND_HALF_EVEN,'DOWN':ROUND_DOWN}.get(policy['mode'])
        if mode is None: raise Invalid('ROUNDING_INVALID')
        quantum=Decimal(1).scaleb(-policy['scale'])
        counts['input_fills']=len(fills)
        totals={}; seen={}
        with localcontext() as ctx:
            ctx.prec=256
            for i,f in enumerate(fills):
                ref=f'fills:{i+1}'
                identity=f.get('canonical_fill_id')
                if not isinstance(identity,str) or not identity or not f.get('identity_evidence'): fail('FILL_ID_AMBIGUOUS',ref); continue
                content=digest(f)
                if identity in seen:
                    if seen[identity]!=content: fail('CANONICAL_ID_CONFLICT',identity)
                    else: counts['confirmed_duplicates']+=1
                    continue
                seen[identity]=content
                t=stamp(f['occurred_at'])
                if not start<=t<end: counts['outside_period']+=1; continue
                if f.get('builder','').lower()!=bundle['builder'].lower() or not f.get('attribution_evidence'): fail('BUILDER_ATTRIBUTION_MISSING',ref); continue
                if f.get('market_class')!='validator-operated-perp' or f.get('market_id') not in bundle.get('verified_market_ids',[]): fail('MARKET_UNSUPPORTED',ref); continue
                if f.get('fee_currency_id')!=bundle['fee_currency_id']: fail('FEE_TOKEN_UNKNOWN',ref); continue
                if f.get('fee_basis') not in ('GROSS','BUILDER_KEPT'): fail('FEE_BASIS_UNKNOWN',ref); continue
                if f.get('native_split_presence')!='NO': fail('NATIVE_SPLIT_UNCALIBRATED',ref); continue
                fee=money(f['builder_fee'])
                if fee<0: fail('NEGATIVE_FEE_UNSUPPORTED',ref); continue
                matches=[r for r in rules if r['account']==f['account'] and stamp(r['from'])<=t<stamp(r['to'])]
                if len(matches)!=1: fail('RULE_GAP' if not matches else 'RULE_OVERLAP',ref); continue
                r=matches[0]
                if r['fee_basis']!=f['fee_basis']: fail('FEE_BASIS_UNKNOWN',ref); continue
                rate=money(r['rate'])
                if not Decimal(0)<=rate<=Decimal(1): fail('RATE_INVALID',ref); continue
                part=fee*rate
                if policy['stage']=='PER_FILL': part=part.quantize(quantum,rounding=mode)
                key=r['beneficiary_id']; totals[key]=totals.get(key,Decimal(0))+part
            indexed={}
            for b in balances:
                key=b['beneficiary_id']
                if key in indexed: fail('BALANCE_CONFLICT',key)
                indexed[key]=b
            if len(set(totals)|set(indexed))>100: raise Invalid('INPUT_LIMIT_EXCEEDED')
            paid={}; receipts=set()
            for p in payments:
                key=p['beneficiary_id']; receipt=p.get('receipt_event_key')
                if not receipt or not p.get('evidence'): fail('PAYMENT_UNVERIFIED',key); continue
                if receipt in receipts: fail('PAYMENT_DUPLICATE_RECEIPT',receipt); continue
                receipts.add(receipt)
                if p.get('status')!='CONFIRMED': fail('PAYMENT_UNVERIFIED',receipt); continue
                if p.get('channel')!='EXTERNAL': fail('NATIVE_SPLIT_UNCALIBRATED',receipt); continue
                if p.get('currency_id')!=bundle['fee_currency_id']: fail('CURRENCY_MAPPING_UNKNOWN',receipt); continue
                if not start<=stamp(p['occurred_at'])<end: fail('PAYMENT_OUTSIDE_PERIOD',receipt); continue
                if p.get('close_group_id')!=bundle['close_group_id']: fail('PAYMENT_WRONG_GROUP',receipt); continue
                amount,allocated,other=map(money,[p['confirmed_total'],p['applied'],p['other_group_allocated']])
                if min(amount,allocated,other)<0 or allocated+other>amount: fail('PAYMENT_OVERALLOCATED',receipt); continue
                paid[key]=paid.get(key,Decimal(0))+allocated
            for key in sorted(set(totals)|set(indexed)|set(paid)):
                b=indexed.get(key)
                if not b or 'opening' not in b: fail('OPENING_BALANCE_UNKNOWN',key); continue
                if 'closing_statement' not in b: fail('CLOSING_STATEMENT_MISSING',key); continue
                if not b.get('confirmation_evidence') or not b.get('independent_statement_evidence'): fail('BALANCE_UNVERIFIED',key); continue
                if stamp(b['opening_cutoff'])!=start or stamp(b['closing_cutoff'])!=end: fail('BALANCE_CUTOFF_MISMATCH',key); continue
                opening,statement=money(b['opening']),money(b['closing_statement'])
                accrued=totals.get(key,Decimal(0))
                if policy['stage']=='PER_RECIPIENT_PERIOD': accrued=accrued.quantize(quantum,rounding=mode)
                external=paid.get(key,Decimal(0)); closing=opening+accrued-external
                rows.append({'beneficiary_id':key,'currency_id':bundle['fee_currency_id'],'opening':textnum(opening),'accrual':textnum(accrued),'external_paid':textnum(external),'closing_calculated':textnum(closing),'customer_closing_statement':textnum(statement),'statement_variance':textnum(closing-statement)})
    except (KeyError,TypeError,ValueError,ArithmeticError,AttributeError) as exc:
        fail(str(exc) if isinstance(exc,Invalid) else 'SCHEMA_INVALID')
    result={'engine_version':VERSION,'sample_class':bundle.get('sample_class'),'status':'BLOCKED' if issues else 'DIAGNOSTIC_ONLY','commercial_g0_passed':False,'counts':counts,'limitations':['Synthetic adapter only; no customer/source authenticity or coverage certification.','Native splits, adjustments, production adapters, review and storage workflows not implemented.'],'issues':sorted(issues,key=lambda x:(x['code'],x['ref'])),'calculations':[] if issues else rows}
    result['scope']={k:bundle.get(k) for k in ['builder','network','period_start','period_end','close_group_id','fee_currency_id','rounding','verified_market_ids']}
    result['rule_set_hash']=digest(sorted(bundle.get('rules',[]),key=canonical)) if isinstance(bundle.get('rules'),list) else None
    result['business_hash']=digest(result)
    return result
