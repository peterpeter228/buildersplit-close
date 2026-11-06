# Actual validation, 2026-11-06

Environment: current cloud execution workspace, Python 3.12.14; standard library only. Connected desktop was available on initial discovery but task admission returned executor_offline with taskCreated=false; refreshed environment list was empty. No desktop task was created. Local cloud validation was used instead.

Commands actually executed:

- `python -m unittest discover -s tests -v`: exit 0, 22 tests passed (0.004 seconds on final recorded run).
- `python -m compileall -q bsclose tests`: exit 0.
- `python -m bsclose examples/synthetic.json --output /tmp/bsclose-20261106-first`: exit 0; DIAGNOSTIC_ONLY. Golden opening20 + accrual30 - external35 = closing15; independent statement12 => variance3.
- Same command with existing output directory: exit 2, File exists. Existing report not overwritten.
- CLI with missing opening balance: exit 2; BLOCKED with empty calculations; diagnostic JSON persisted.

Final smoke timestamp: 2026-11-06T13:12:11Z. Implementation elapsed approximately minutes, within 8-hour cap; exact person-hours were not separately instrumented. Code source SHA is the commit containing this file; fixed remote SHA must be recorded in synchronization receipts, not invented here.

Covered: schema guard, input class separation, unknown scope/fee/builder, identity conflict and duplicate, source coverage guard, native rejection, rule gap/overlap, time boundary, Decimal/precision/rounding, payment dedup/allocation/group/status, balances, signed overpayment, deterministic ordering, symlink/duplicate JSON key and CSV injection guards.

Not performed: real customer golden comparison, actual Hyperliquid adapter validation, all 39 original production acceptance cases, native credit calibration, SQLite/backup/disaster recovery, independent source completeness, production UI/browser E2E, security audit, deployment, external API integration or market/paid-customer validation. Browser is not applicable to this CLI-only milestone. Static compile is not type checking; no typechecker run. No complete production build is claimed.

Known limitations: this normalized JSON experiment is not the complete CSV/JSONL intake design. Statements about evidence and coverage inside synthetic fixtures are not independently verified. There is no real-source trust root; therefore even entirely valid synthetic inputs never become REVIEW_READY. Native/adjustment/refund workflows remain unsupported. Partial output I/O failures may leave an incomplete new run directory; callers must treat an error exit as failure, never as a completed export.

## Independent review fixes

Independent review reproduced fail-open synthetic input cases in the first draft: truthy non-boolean confirmations; string market registry enabling substring matches; ignored nested currency fields; absent close group with zero payments; empty/integer identifiers; permissive timestamp parsing; and a report hash not bound to scope. These were fixed before completing the milestone, with regression tests.

The adapter now requires actual True confirmation flags, a nonempty string-array market registry, rejects unsupported nested fields, validates nonempty string IDs/evidence, requires close_group even for no-payment bundles, and accepts only RFC3339 UTC Z timestamps with at most millisecond precision. Reports include scope and a canonical sorted rule-set hash within business_hash. Changed Builder/group identity now changes report hash even if arithmetic is unchanged.

`python -m unittest discover -s tests -q`: exit 0, 29 tests passed (0.007 seconds). `python -m compileall -q bsclose tests`: exit 0. This supersedes the first-draft test count, not its historical evidence. Production/source validation remains NOT_RUN.

## Continuation: recoverable synthetic evidence bundles

Added completion-last export marker, SHA-256 manifest for normalized synthetic input/report/CSV/readme, offline replay verifier, backup-copy validation and actual 50,000-fill capacity regression. This is a bounded file-bundle mechanism, not SQLite or a production disaster-recovery system. Raw source hash and normalized snapshot hash are distinct. Hashes are integrity evidence, not authenticated source evidence.

Actual commands: `python -m unittest discover -s tests -v` exit 0, 37 tests in 0.672 seconds; `python -m compileall -q bsclose tests` exit 0. The 50K unique fill fixture produces synthetic accrual 1,500,000; 50,001 fills are rejected. Disk-write failure is fault-injected, not a real full-disk experiment; no valid completion marker survives. Each required artifact tamper is rejected. A copied bundle reproduces the same result; blocked inputs stay blocked under verification. Neither customer G0 nor the whole original 39-case production matrix is claimed complete.

Continuation review found that merely checking a report's declared business_hash would miss a contradictory report repackaged with refreshed file hashes. Verification now compares the entire deterministic report and CSV against replay, not just the self-reported hash. A fixed evaluation_as_of is persisted and replayed, preventing PERIOD_OPEN results changing with wall-clock time. Regression covers inconsistent repackaged report, inconsistent CSV and a past evaluation time. Raw input_sha256 is an external provenance field: original raw bytes are not retained, so it cannot be independently authenticated here.

Completion-last prevents ordinary interrupted runs being accepted; no fsync/atomic power-loss durability is promised. The 50K test exercises the calculation core, not a 50K file-export/backup end-to-end scenario. File-copy restoration is tested on the small synthetic example only.

Final continuation regression: 40 unittest cases passed (0.629 seconds), exit 0; compileall exit 0; fresh CLI export and verify-run smoke both exit 0, DIAGNOSTIC_ONLY/VERIFIED. These 40 software tests are not the original research's 39 production acceptance cases.
