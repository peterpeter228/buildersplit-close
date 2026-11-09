# Audit repair evidence — 2026-11-09

Base: d583aa8de590adc9cbb19db2a13671bf8e0092be.
Scope: R1 rule validation, R2 bounded/indexed processing, R3 numeric CSV.
No customer data, production adapter, credentials, messages or payment actions.

## Before repair (actually reproduced)
- Existing 40 unittest tests passed.
- Appending an unmatched account rule with rate NaN, malformed from timestamp,
  or fee_basis UNKNOWN each incorrectly returned DIAGNOSTIC_ONLY.
- A synthetic negative closing/variance exported as '-5.00000000 / '-17.00000000,
  with an apostrophe prefix.

## Repair
- Validate every rule before fill processing; reject invalid/empty/inverted
  intervals, unknown basis, non-decimal/out-of-range rates and account overlaps.
- Parse intervals once; sort by account/time; binary search for each fill.
  Complexity O(R log R + F log R), not F times R.
- Reject >10,000 rules or >50,000 payments before processing their contents.
  Existing 50K-fill/100-balance bounds remain.
- Escape identifier CSV columns; strictly validate and serialize monetary columns.
- Increment experimental engine version to 0.1.1; old bundle replay is version
  specific and should use the old checkout, rather than silently reinterpret it.

## Actual checks
Python 3.12.14, standard library, synthetic input only.
- python -m unittest discover -s tests -v: 51 tests passed.
- python -m compileall -q bsclose tests: passed.
- git diff --check: passed.
- CLI export: DIAGNOSTIC_ONLY; verify: VERIFIED / DIAGNOSTIC_ONLY.
- Re-export to existing directory: rejected, expected exit 2.
- Full combined capacity: 50,000 distinct fills, 10,000 rules and 50,000 distinct
  zero-applied payment records: DIAGNOSTIC_ONLY, 1.434 seconds in this environment.
  This is one synthetic timing observation, not a production latency guarantee.
- Timestamp-call-count regression confirms bounded rule parsing rather than
  repeating parsing per fill; adjacent intervals, unused overlaps, absent fills,
  CSV formula-like IDs and injected numeric expressions are tested.

Commercial G0 remains false. Real adapter/source authenticity, independent
customer golden controls, demand, paid pilots, UI and production are NOT VALIDATED.

## Independent review
An independent reviewer identified that derived monetary values can exceed the
100-character input limit. Fixed by separating the strict bounded derived-output
grammar (300 characters) from input validation. Added large-opening export and
replay regression; the final suite is 51 tests, all passing. The reviewer also
exercised 50K fills with 10K same-account intervals and observed only 70,005
timestamp parses, confirming interval parsing is not repeated F times R.
