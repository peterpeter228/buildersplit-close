# P1 synthetic close report — verification

Verified 2026-11-08. Baseline: `c1a4593cc59e3fa38fc9987e44bcbbc440e6e0e3`.
Worktree: `/root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p1`.
Commit branch: `wp/buildersplit-g1-pack-20261108-p1-p1`; publication target: `feat/g1-pack-20261108`, never main.

## Artifacts and scope

- `close-report-sample.html`: single-file offline report; inline CSS, no external resources or JavaScript.
- `close-report-sample.pdf`: matching one-page A4 PDF.
- `synthetic-close.json`: four-payee synthetic fixture derived from the stock example's schema; stock example and engine unchanged.
- `engine-run/`: actual `input.json`, `report.json`, `reconciliation.csv`, `README.txt`, and `COMPLETED.json` from the unchanged engine.
- `generate_close_report.py`: Python stdlib renderer consuming engine JSON and checking CSV agreement, including spreadsheet-protected negative values.

One explicitly fake Builder (`0x1111111111111111111111111111111111111111`); ended UTC period `[2026-10-01T00:00:00Z, 2026-10-08T00:00:00Z)`; 4 fills, 4 payees; one frozen rule set. All four allocation rules have the same full-period interval and synthetic rate `0.5`. No real source, identity, ledger, payment, pricing, or yield claim. Status remains `DIAGNOSTIC_ONLY`, `commercial_g0_passed=false`; exit 0 is not real-data approval.

## Exact engine and generation commands

All commands below ran from the worktree root. This host has Python 3.12.3 as `python3` and no `python` alias. Engine output directories must not already exist; use a fresh path for a rerun.

```sh
python3 -m bsclose examples/synthetic.json --output /tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/baseline-recompute
python3 -m bsclose --verify-run /tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/baseline-recompute
python3 -m bsclose demo/synthetic-close.json --output demo/engine-run
python3 -m bsclose --verify-run demo/engine-run
python3 demo/generate_close_report.py demo/engine-run --output demo/close-report-sample.html
```

Each command exited **0**. Both engine runs printed `DIAGNOSTIC_ONLY`; both verification commands returned `integrity=VERIFIED`, `status=DIAGNOSTIC_ONLY`.

Stock example: one fill/payee, opening `20`, accrual `30.00000000`, external paid `35`, calculated closing `15.00000000`, statement `12`, variance `3.00000000`. Its single variance row cannot satisfy the requested 3–5 rows, hence the separate demo fixture.

Stock hashes:
- Input SHA-256: `649ba15d116bf4ce16ca97ed79edb9f3ca4de422694edcc4e3652ce3b4423bfb`
- Business hash: `a8304e0a633f27442cfd96850c27839f173ddc43b868431ac27fd97f54e175ba`

Demo report key fields:
- `evaluation_as_of`: `2026-11-08T08:53:27.497Z`
- `engine_version`: `0.1.0-experiment`
- `counts`: `input_fills=4`, `confirmed_duplicates=0`, `outside_period=0`
- `issues`: `[]`
- Input SHA-256: `7d0c9fdabe8a6fafd5c20eb1b80dc69ea3560b2bd57a84a09d572052ce387f5b`
- Frozen `rule_set_hash`: `680cc7e3e489e1fe9c095f34d8e843f4c220320d5c9d80f6ee3b3da39e26e039`
- `business_hash`: `612ebab4581abe363c877c4b54f98c0903099bd26ad7e64b33d1b460197b3aa0`
- Rounding: `PER_FILL`, scale `8`, `HALF_EVEN`.

Amounts below are synthetic USDC accounting units; zeros after the decimal are omitted in this evidence table only. The HTML/PDF preserves engine decimal strings.

| Synthetic payee | 应计 | 已付 | 期初 | 期末 | 结转* | Statement | Variance |
|---|---:|---:|---:|---:|---:|---:|---:|
| synthetic-payee-01 | 30 | 35 | 20 | 15 | 15 | 12 | +3 |
| synthetic-payee-02 | 30 | 35 | 0 | -5 | -5 | 0 | -5 |
| synthetic-payee-03 | 30 | 10 | 10 | 30 | 30 | 25 | +5 |
| synthetic-payee-04 | 30 | 0 | 0 | 30 | 30 | 32 | -2 |

Closing = opening + accrual − external paid. Variance = calculated closing − synthetic statement. `已付` is the engine's eligible synthetic external allocation, not a real payment confirmation. *Carryover repeats signed closing as a hypothetical next-period opening; it is not a separate engine field, completed operation, net payable, or cross-payee offset. The negative row is retained, not clamped. No cause of a variance is asserted.

The page retains literal `[INPUT_SHA256]` and `[RULE_VERSION]` placeholders alongside actual synthetic input/rule hashes. The engine has no named rule version; the placeholder is explicitly unassigned. Hashes are not signatures or source authentication.

## Offline rendering and PDF check

Google Chrome `144.0.7559.132`; local `WenQuanYi Zen Hei` font. Exact commands, each exit **0**:

```sh
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --no-pdf-header-footer --print-to-pdf=demo/close-report-sample.pdf file:///root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p1/demo/close-report-sample.html
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --window-size=1100,1350 --screenshot=/tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/html-offline.png file:///root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p1/demo/close-report-sample.html
```

`unshare --net` isolated Chrome from external networking. The actual `file://` page and rendered PDF were visually inspected. Both show the four rows, all required columns, full hashes, readable Chinese text, and bilingual red header/footer without clipping. No P2 screenshot deliverables were created; inspection images remain job evidence only.

Throwaway acceptance checks (not permanent tests) ran with exit **0**:

```sh
python3 /tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/check_report.py /root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p1
/tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/pdf-tools/bin/python /tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/inspect_pdf.py demo/close-report-sample.html demo/close-report-sample.pdf /tmp/omp-jobs/buildersplit-g1-pack-20261108-p1/pdf-page.png
```

Checks observed:
- Fixture bytes match `input_sha256`; ended seven-day scope, one Builder, four fills/payees, fixed full-period rules.
- Every HTML table amount matches the engine report; Decimal accounting identities and all four variances pass.
- PDF: **1 page**, approximately **595 × 842 pt (A4)**; **80/80** visible HTML text fragments occur in PDF text; all text bounding boxes are inside the page.
- Header/footer each contain exactly `SYNTHETIC SAMPLE — NOT A REAL LEDGER / 合成样例，非真实账本`, both colored **`#b00020`**. Notice positions are near page top/bottom.
- No external HTML resources. No claims of real/customer verification, pricing, or yield.

The first PDF-check invocation exited 1 because the checker assumed separate language spans; Chrome actually emitted one combined bilingual span per notice. The checker was corrected to require both full notices in each of the two spans; document content was unchanged. Browser automation through `eval` was policy-blocked, so verification used real Chrome CLI rendering, offline screenshots, and PyMuPDF text/color/geometry inspection instead.

The job-local check scripts were removed after verification. Their commands above record executed evidence, not shipped tooling; the attached engine bundle remains replay-verifiable with the engine's `--verify-run` command.

Artifact SHA-256:
- HTML: `5d92861abe76f9b0db282beb208a6715077bce5192c23f2ac44232d98b06ee35`
- PDF: `a255396bb91aeb7a5431b57127f41594811322eb9d8f8a2e4a4095d5a1522473`

## Publication boundary

Only P1 and `demo/` changes are in scope. No engine/API changes, P2–P7 work, deployment, charge, broadcast, or outbound messages. Draft PR #1 was observed open/draft on `feat/g0-synthetic-core-20261106`, not the requested G1 ref. Publication follows owner Q1=A to `feat/g1-pack-20261108`; it does not retarget PR #1 or claim that pushing G1 updates it. The loop receipt records the actual pushed commit.
