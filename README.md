# BuilderSplit Close

Private G0 technical experiment, **not a validated SaaS or customer ledger**.

An offline, standard-library Python core tests whether a bounded seven-day Builder fee reconciliation can be calculated deterministically while rejecting unknown inputs. Research recommendation: PIVOT 64/100. Customer interviews, payments and renewals remain zero. No production adapter, deployment, signing or money movement exists.

## Run

Python 3.12+; no installation, network or credentials required.

```sh
python -m unittest discover -s tests -v
python -m bsclose examples/synthetic.json --output /tmp/bsclose-new-run
```

The output directory must not exist. Exit 0 means a synthetic diagnostic completed, **not** REVIEW_READY. Exit 2 means blocked/error. Always inspect report.json. The experiment never produces REVIEW_READY or CLIENT_REVIEWED. Existing run folders cannot be overwritten.

## First milestone

- Explicit normalized synthetic schema, one Builder, ended seven-day UTC period, verified market list and USDC accounting identity.
- Decimal calculation, half-open time rules, stable IDs and conflicting identity rejection.
- Signed opening + accrual - eligible external payment, independently supplied closing statement variance.
- Explicit business rounding policy and source hash; JSON plus formula-safe CSV exports.
- Unknown provenance, currency, native split, payment allocation or balances block calculation.

Unknown/unsupported top-level fields are rejected rather than silently treated as supported adjustments. The source/provenance labels in the fixture are **synthetic assertions**, not independent evidence. This engine cannot validate whether supplied references are authentic.

## Not implemented

Real source adapter; CSV/JSONL intake; independently verified source coverage; native split calibration; adjustments/reversals; multiple allocation recipients; persistent SQLite snapshots; customer review; cross-period real allocation history; immutable backup/recovery workflow; UI; production readiness. No raw public observation or customer sample has been used as a successful ledger.

See docs/PRD.md and docs/TEST_EVIDENCE.md. Do not infer commercial completion from passing synthetic tests.

## Verify or restore a diagnostic bundle

```sh
python -m bsclose --verify-run /tmp/bsclose-new-run
```

New exports save a normalized synthetic input snapshot and write `COMPLETED.json` last. Verification checks the required artifact hashes and recomputes the business result. A byte-for-byte copied backup can be verified on another path; missing markers, altered files, symlinks or inconsistent replay fail. Exit 0 for verification means integrity/replay matched only: a BLOCKED report remains BLOCKED. Hashes are not signatures and do not authenticate a source or protect against a malicious writer replacing all files. Older exports without the marker cannot pass this verifier; create a new run rather than overwrite them.

See docs/CUSTOMER_SAMPLE_CHECKLIST.md before any real-input work.
