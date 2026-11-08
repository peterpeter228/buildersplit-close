# P7 verification — PARTIAL / needs_owner

Worktree: `/root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p7`; branch `wp/buildersplit-g1-pack-20261108-p7`; baseline `255483bea2f0dc94397d5fab62df736ccf044804`. Run commands from this worktree. No engine or P1 renderer code changed.

## Public retrieval (2026-11-08 Asia/Shanghai)

Exact seven-day retrieval command, exit **0**, seven HTTP **200** responses:

```sh
curl --silent --show-error --location --max-time 45 --create-dirs --output 'demo/public-dextrabot/raw/2026110#1.csv.lz4' --write-out 'http_status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' 'https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/2026110[1-7].csv.lz4'
```

In date order, downloaded sizes: **5721, 16114, 24693, 71262, 62703, 40010, 6517 bytes**. Initial availability probe fetched the final URL to `/tmp/omp-jobs/buildersplit-g1-pack-20261108-p7/20261107.response`, also HTTP 200 / 6517 bytes, exit 0. No monetary interpretation was made.

Exact source archive command, exit **0**, three HTTP **200** responses:

```sh
curl --silent --show-error --location --max-time 45 --output demo/public-dextrabot/raw/defillama-dextrabot.ts --write-out 'http_status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://raw.githubusercontent.com/DefiLlama/dimension-adapters/master/dexs/dextrabot.ts --next --silent --show-error --location --max-time 45 --output demo/public-dextrabot/raw/ocb-builders.json --write-out 'http_status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://raw.githubusercontent.com/ChainBench/OpenChainBench/main/harnesses/hyperliquid-frontends/builders.json --next --silent --show-error --location --max-time 45 --output demo/public-dextrabot/raw/ocb-method.html --write-out 'http_status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://openchainbench.com/benchmarks/hyperliquid-frontends
```

Sizes: **1728, 31608, 939186 bytes**. Exact URLs, timestamps and raw-byte SHA-256 are in [SOURCES.md](SOURCES.md). Live refetches may change; frozen bytes are the evidence.

## Existing-engine compatibility smoke

This is a **classification rejection probe**, not a public-fill mapping or successful recomputation. Empty arrays mean unmapped/unknown, not zero observations. The only accepted schema name is retained to exercise the public sample-class guard without falsely classifying the input as synthetic.

```sh
python3 -m bsclose demo/public-dextrabot/engine-probe-input.json --output demo/public-dextrabot/engine-run
```

Exit **2**, stdout `BLOCKED`. Key fields: `sample_class=PUBLIC_DATA_ESTIMATE`, `issues=[{code: ADAPTER_UNVALIDATED, ref: manifest}]`, `calculations=[]`, `commercial_g0_passed=false`. Input SHA-256: `79ac32c733652ddd002167e06d87fd5cc7cab50ab875ca36ea5ca178fbbbd2aa`.

```sh
python3 -m bsclose --verify-run demo/public-dextrabot/engine-run
```

Exit **0**; `integrity=VERIFIED`, **`status=BLOCKED`**, business hash `5aca2de31147bce4208b47ee4e4965b8f0414d9c156341f0b9585a9d7d0db19c`. This verifies the persisted blocked export/replay, not fee calculations or public-source authenticity. Re-running export requires a fresh output directory; use `--output /tmp/p7-engine-probe-new` instead of overwriting evidence. The report's evaluation timestamp may change.

```sh
sha256sum /workspace/loop/buildersplit-g1-pack-20261108/GOAL-P7.md demo/public-dextrabot/engine-probe-input.json demo/public-dextrabot/engine-run/report.json
```

Exit **0**; hashes in order:
- frozen goal: `15fede417a4e8c27bfe3e2a51428b9d947aa2a5f0802cbeb14c93ea0ed85756e`
- input: `79ac32c733652ddd002167e06d87fd5cc7cab50ab875ca36ea5ca178fbbbd2aa`
- output report: `f208df77ab7e63fb3bda51ab89d1326628ca6ecff897b40e3f897cfbc3f4b86b`

## Unmet acceptance / owner boundary

No decoded CSV mapping, observed fee sum, successful engine accrual, HTML, PDF, variance sample or visual verification. No source-unavailable fallback is claimed. Engine lines 49–50 reject a truthful public class; lines 61, 108–122, 145–156 additionally require evidence unavailable from these fills. Owner must resolve the acceptance/engine contract mismatch before rendering an estimate. No synthetic fixture, fake payee split, fabricated balance/payment or guessed coverage was substituted.

`eval` was denied by tool policy; no policy settings were changed. Direct headless Chrome discovery of HyperTracker timed out after 60 seconds; its rendered content is not cited as captured evidence. No build/test suite was run: no production code changed. No outbound messages, deployment, charge, broadcast, main push/merge or PR mutation occurred.
