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
