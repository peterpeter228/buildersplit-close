# P7 verification — attempt 2 / public-data estimate

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

## Owner-adjusted acceptance

Owner **t256u**, 2026-11-08T17:37+08:00, **P7-Q1=A** (`/workspace/loop/buildersplit-g1-pack-20261108-p7/DECISIONS.md`): a separately labeled demo-local Decimal summary replaces engine-derived public accrual acceptance. **Not an engine reconciliation result / 非引擎核账结果**. The historical BLOCKED run above remains evidence, not an estimate calculation. Payouts, opening/closing/carryforward balances, splits and statement variances remain UNKNOWN.

No raw files were refetched. No engine, real adapter or P1 renderer change is authorized. The prior attempt stopped before generating HTML/PDF/CSV; attempt 2 retains those deliverables under the adjusted contract.

## Independent frozen-input inspection

Exact final inspection command, exit **0**:

```sh
python3 /tmp/omp-jobs/buildersplit-g1-pack-20261108-p7/check_public_inputs.py /root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p7
```

The throwaway checker used Python stdlib `ctypes` with the already-installed `liblz4.so.1` (independent of the shipped Python decoder). It verified all ten raw-file SHA-256 values against SOURCES.md, decoded all seven LZ4 frames with library checksum validation, checked every timestamp is timezone-aware, inside the requested half-open window and on its filename's UTC day, and checked every Decimal fee is finite. CSV columns are `time,user,coin,side,px,sz,crossed,special_trade_type,tif,is_trigger,counterparty,closed_pnl,twap_id,builder_fee`; there is no builder address or fee-token column. Attribution comes from the archived address sources and per-builder URL; USDC interpretation comes from the archived OpenChainBench methodology, not a token field.

| UTC date | Observed rows | Decimal builder_fee (USDC) | First observed UTC | Last observed UTC |
|---|---:|---:|---|---|
| 2026-11-01 | 99 | 19.400503 | 00:07:06 | 12:09:21 |
| 2026-11-02 | 390 | 24.319140 | 00:01:34 | 10:47:30 |
| 2026-11-03 | 641 | 28.890891 | 00:03:05 | 12:11:53 |
| 2026-11-04 | 2005 | 148.972720 | 00:00:06 | 23:56:39 |
| 2026-11-05 | 1646 | 281.019730 | 00:02:04 | 17:30:39 |
| 2026-11-06 | 1209 | 72.221046 | 00:00:38 | 12:15:10 |
| 2026-11-07 | 114 | 20.636442 | 00:04:24 | 12:02:38 |
| Total | 6104 | 595.460472 | — | — |

These are observations, not completeness or exact-cutoff certification. No missing activity was assigned zero or extrapolated. The OpenChainBench/Totalis ~12:10 UTC daily cutoff caveat remains applicable.

The unchanged engine replay was rechecked with `python3 -m bsclose --verify-run demo/public-dextrabot/engine-run`, exit **0**: `integrity=VERIFIED`, `status=BLOCKED`, business hash `5aca2de31147bce4208b47ee4e4965b8f0414d9c156341f0b9585a9d7d0db19c`.

## Deterministic demo-local reproduction

Exact command, both invocations exit **0**:

```sh
python3 demo/public-dextrabot/summarize_public_fees.py && python3 demo/public-dextrabot/summarize_public_fees.py
```

Both runs printed the same hashes (no runtime timestamp is included):

| Output | Run 1 SHA-256 | Run 2 SHA-256 |
|---|---|---|
| `demo/public-dextrabot/summary.json` | `12fa7d9741dc0ad100f50bcdb7786dde8f0faf70bbd3f5e00713eb8f8d886a9a` | `12fa7d9741dc0ad100f50bcdb7786dde8f0faf70bbd3f5e00713eb8f8d886a9a` |
| `demo/close-dextrabot-public-week.html` | `cb068d80b46d47a0d65503ac3e1de22c43309cde203a4c374d9980292f26033d` | `cb068d80b46d47a0d65503ac3e1de22c43309cde203a4c374d9980292f26033d` |
| `demo/close-dextrabot-public-week-variance.csv` | `c034e39a71b864f118761580b28667d8ecda9085a8cf80d353e42edd027286b2` | `c034e39a71b864f118761580b28667d8ecda9085a8cf80d353e42edd027286b2` |

The independent checker command above was then run against the generated artifacts, exit **0**. All seven decoded byte hashes, daily counts/sums/extrema, window membership and the total matched. Summary: `saved_rows=in_period_rows=6104`, `outside_period_rows=0`, `public_observed_builder_fee="595.460472"`, `unit="USDC"`, `coverage="UNKNOWN"`, `not_engine_reconciliation=true`. CSV has one observed fee-pool row and seven UNKNOWN ledger-field rows; every ledger value and variance is UNKNOWN. The 0 outside-window count describes these saved rows only, not absent market activity.

## Offline HTML and matching PDF

Google Chrome **144.0.7559.132**, local **WenQuanYi Zen Hei**. Exact rendering commands, each exit **0**:

```sh
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --no-pdf-header-footer --print-to-pdf=demo/close-dextrabot-public-week.pdf file:///root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p7/demo/close-dextrabot-public-week.html
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --window-size=1100,1450 --screenshot=/tmp/omp-jobs/buildersplit-g1-pack-20261108-p7/html-offline.png file:///root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p7/demo/close-dextrabot-public-week.html
```

`unshare --net` prevented external networking. `eval`/browser automation was policy-denied; no policy was changed. The actual Chrome screenshot and PDF raster were visually inspected: readable Chinese, one builder-fee-pool line, UNKNOWN ledger fields, explicit not-engine line, cutoff caveat and red bilingual header/footer without clipping. No external resources are required; source hyperlinks are citations, not fetched assets.

Exact PDF inspection command, exit **0**, reusing the existing P1 job-local PyMuPDF runtime (not a shipped dependency):

```sh
/tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/pdf-tools/bin/python /tmp/omp-jobs/buildersplit-g1-pack-20261108-p7/inspect_public_pdf.py demo/close-dextrabot-public-week.html demo/close-dextrabot-public-week.pdf /tmp/omp-jobs/buildersplit-g1-pack-20261108-p7/pdf-page.png
```

Observed **1 A4 page**, **594.96 × 841.92 pt**, **103/103 visible HTML text fragments** in PDF text, all text bounding boxes inside the page. Both exact bilingual notices are red **#b00020**; the explicit `Not an engine reconciliation result / 非引擎核账结果` line is present. PDF bytes include Chrome metadata: repeatability claims above cover summary/HTML/CSV, not PDF metadata.

Exact final hash command, exit **0**:

```sh
sha256sum demo/close-dextrabot-public-week.pdf demo/public-dextrabot/engine-run/*
```

PDF SHA-256: `ee0d717af5fe5bffbcd9a45f61dc4a16a669f43d141ea3d1d52777696ab87939`. All five engine-run hashes matched the pre-implementation snapshot byte-for-byte:

| Engine evidence | SHA-256 |
|---|---|
| `COMPLETED.json` | `638b576cdd17c0b78320c202197d4fce699bfde33604954b3abd700e574e5eac` |
| `README.txt` | `b40fa564947ffcc48bbcd4efc89dcdc2bf0317a342568d2022dc066a7e023d1f` |
| `input.json` | `ab81b9f0969aa4b0c3a7c904539507457b417c996f9f04db359667b240ef0951` |
| `reconciliation.csv` | `93f097b27338d59cbbcb9aefdd77c35b672deb2473afb28ee7e21ed4caa934da` |
| `report.json` | `f208df77ab7e63fb3bda51ab89d1326628ca6ecff897b40e3f897cfbc3f4b86b` |

Throwaway inspection scripts are removed after verification; commands document executed evidence, not shipped tooling. Inspection images remain job evidence only. No production suite was run or permanent tests added: changed behavior is demo-local and was exercised directly. No engine/real-adapter expansion, outbound contact, deploy, charge, broadcast, real-money action, main push/merge or PR mutation.
