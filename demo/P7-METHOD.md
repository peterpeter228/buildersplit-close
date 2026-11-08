# P7 — Dextrabot public-fee estimate · Q1=A

**PUBLIC-DATA ESTIMATE — NOT THE BUILDER'S BOOKS / 公开数据估算，非对方账本**

**Not an engine reconciliation result / 非引擎核账结果.** Window: **[2026-11-01T00:00:00Z, 2026-11-08T00:00:00Z)**, the most recent ended seven-day UTC window at retrieval. Owner **t256u**, **2026-11-08T17:37+08:00**, accepted **P7-Q1=A**: a demo-local public-fee sum replaces the engine-derived-accrual acceptance, not the engine/real-adapter contract.

## Attribution and source evidence

Builder `0x49ae63056b3a0be0b166813ee687309ab653c07c` is publicly attributed to Dextrabot by [DefiLlama](https://raw.githubusercontent.com/DefiLlama/dimension-adapters/master/dexs/dextrabot.ts) and [OpenChainBench's registry](https://raw.githubusercontent.com/ChainBench/OpenChainBench/main/harnesses/hyperliquid-frontends/builders.json). OCB's entry cites **HyperTracker's public registry** and a node-fill coverage audit: separate attribution chains, not proof of ownership. Failed discovery paths remain recorded in the source manifest.

All ten unchanged raw sources, seven exact Hyperliquid daily URLs, per-file **SHA-256** and fetch-completion times are preserved in [public-dextrabot/SOURCES.md](public-dextrabot/SOURCES.md). Fetch date **2026-11-08, Asia/Shanghai (+08:00)**: fills **17:22:00.288493–17:22:03.247447**; attribution/method sources **17:22:22.577148–17:22:22.657147**. Times were captured from file mtimes immediately after the original unauthenticated HTTP 200 downloads; no refetch is used. The script verifies every raw hash against this manifest before decoding.

## Coverage and interpretation

**OpenChainBench/Totalis ~12:10 UTC daily cutoff caveat:** [OCB's preserved methodology](https://openchainbench.com/benchmarks/hyperliquid-frontends) reports exports stopping around that time on many days since 2026-09-08, with its own node substitution or reconstructed afternoons. Their aggregates may therefore differ from a full UTC-day window and these exports. No Totalis aggregate, node data, reconstruction or scaling is used. Daily observed first/last timestamps and row counts are in the [summary](public-dextrabot/summary.json) and HTML; **extrema do not prove coverage or a cutoff**, and absent fills are not zero activity.

The actual CSV has 14 fields, including `time` (ISO 8601 UTC seconds ending `Z`) and `builder_fee` (plain decimal), but **no builder or currency column**. Identity comes from the exact per-builder URL plus the two attribution sources. The frozen OCB methodology explicitly describes **builder fee in USDC**; that source-described unit is retained, not inferred from `coin`, converted to USD, or recomputed from a fee rate. Each saved row in `[start,end)` is summed once with **Decimal precision 80, Inexact trapped**, no rounding, deduplication or extrapolation: **6,104 rows, 595.460472 USDC observed builder fees**. Seven daily counts/sums and decoded hashes are recorded in JSON. This is not trading notional, complete revenue or an entitlement.

## Engine boundary and reproduction

The preserved [engine-run/report.json](public-dextrabot/engine-run/report.json) remains **BLOCKED / ADAPTER_UNVALIDATED**, `calculations=[]`, `commercial_g0_passed=false`; the original compatibility probe exited **2**. Empty arrays mean **not mapped**, not zero fills/payments. Q1=A authorizes only this separately labeled demo summary: no engine, raw input, engine-run or real-adapter change. Prior probe evidence and parent-run verification belong in [P7-VERIFY.md](public-dextrabot/P7-VERIFY.md), not in this estimate's amount.

Reproduce offline: `python3 demo/public-dextrabot/summarize_public_fees.py`. Stdlib only; the narrow independent-block LZ4 reader accepts the observed frozen frame descriptors **only after SHA-256 verification**. SHA-256 binds the LZ4 content-checksum bytes; the script does not implement xxHash or claim a general-purpose decoder. It writes `public-dextrabot/summary.json`, `close-dextrabot-public-week.html` and `close-dextrabot-public-week-variance.csv`, printing each output SHA-256. No runtime timestamp or filesystem mtime enters the generated outputs.

One **builder fee pool** only; ledger fee pool, payouts/已付, opening/期初, closing/期末, carryforward/结转, splits, independent statement and every variance remain **UNKNOWN**—never payment/balance zeros or invented allocations. This cannot establish ledger accuracy, complete coverage, settlement, ownership or beneficiary obligations. **Not the builder's books; not a G0 real-sample substitute; no real-money or adapter gate is unlocked.** No outbound contact, login, paid API, deployment or broadcast is part of this method.
