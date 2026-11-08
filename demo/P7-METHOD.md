# P7 — Dextrabot public-data estimate: PARTIAL / needs_owner

**PUBLIC-DATA ESTIMATE — NOT THE BUILDER'S BOOKS / 公开数据估算，非对方账本**

Target: the most recent ended seven-day UTC window at retrieval, **[2026-11-01T00:00:00Z, 2026-11-08T00:00:00Z)**. No monetary estimate has been generated.

## Attribution and source evidence

Candidate builder `0x49ae63056b3a0be0b166813ee687309ab653c07c` is explicitly named by [DefiLlama](https://raw.githubusercontent.com/DefiLlama/dimension-adapters/master/dexs/dextrabot.ts) and [OpenChainBench's registry](https://raw.githubusercontent.com/ChainBench/OpenChainBench/main/harnesses/hyperliquid-frontends/builders.json). The latter's Dextrabot entry cites **HyperTracker's public registry**, not DefiLlama, and a node-fill coverage audit. These are separate attribution chains, not cryptographic proof of ownership. The [HyperTracker profile](https://app.coinmarketman.com/hypertracker/builder/0x49ae63056b3a0be0b166813ee687309ab653c07c) appeared in search under Dextrabot; direct static extraction returned an application shell and a headless-browser attempt timed out, so it is not claimed as a third independently captured attribution.

Seven exact daily URLs and all source bytes, SHA-256 hashes and fetch-completion times (Asia/Shanghai, recorded from file mtimes immediately after curl) are in [public-dextrabot/SOURCES.md](public-dextrabot/SOURCES.md). All seven daily downloads returned HTTP 200; compressed inputs are preserved unchanged. They have **not been decoded, mapped, or summed**. Availability is not completeness or schema validation.

## Coverage and interpretation

[OpenChainBench methodology](https://openchainbench.com/benchmarks/hyperliquid-frontends) reports public exports stopping around **12:10 UTC** on many days since 2026-09-08, and substitution with its own node data or reconstructed afternoons. **OpenChainBench/Totalis ~12:10 UTC daily cutoff caveat:** their aggregates may differ from a full UTC-day window and from these raw exports. No Totalis aggregate or node/reconstruction data is used here, and the cutoff has not yet been measured in these seven files. Do not scale a partial day into a full-day estimate or interpret an absent fill as zero activity.

If authorized to continue, the only proposed amount is the sum of observed `builder_fee` values inside the half-open window, with units, identities and timestamps checked first. It is not trading notional, exchange fees, a beneficiary entitlement or a statement reconciliation. Payees, 已付, 期初, 期末, 结转 and statement variances remain **UNKNOWN / not public**; no invented split, payment zero, opening zero or allocation confirmation is permitted.

## Engine contract blocker

The unchanged engine accepts only `bsclose.synthetic.v1` with `sample_class=SYNTHETIC` (`bsclose/core.py:49–50`). It also requires confirmed allocation/payment snapshots, supported markets, no native splits, allocation rules and independent balances; any issue suppresses calculation rows (`:61,108–122,145–156`). A truthful public-class compatibility probe returned **BLOCKED / ADAPTER_UNVALIDATED**, exit 2, with no calculations. Replay integrity passed; that does **not** validate public accruals. See [P7-VERIFY.md](public-dextrabot/P7-VERIFY.md).

Owner decision is required before either substituting a separately labeled demo-local sum for engine-derived accruals or expanding the engine contract. Neither is silently assumed. The probe's empty arrays mean **not mapped**, never zero fills/payments. HTML, PDF and variance sample are intentionally absent pending that decision. This is **not** the source-unavailable fallback: public files were available.

This evidence cannot establish ledger accuracy, complete revenue, beneficiary obligations, settlement, balances, ownership or independent statement differences. **Not the builder's books; not a G0 real-sample substitute; no real-money or adapter gate is unlocked.** No outbound contact, login, paid API, deployment or broadcast was performed.
