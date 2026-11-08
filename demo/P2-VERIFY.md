# P2 synthetic demo — capture evidence

Executed 2026-11-08 using configured model `sub2api/gpt-6.1-sol` (required implementation family: `gpt-6.1-sol`). Worktree: `/root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p2`. Approved gate: `/workspace/loop/buildersplit-g1-pack-20261108/plan-review-p2.md` (`VERDICT: PASS`).

## Deliverables and provenance

All four PNGs were captured with real headless Chrome at `1100,1350`, isolated from external networking with `unshare --net`:

| PNG under `demo/screenshots/` | Rendered source | Chrome exit | Bytes |
|---|---|---:|---:|
| `input-file.png` | Escaped local text view of exact `demo/synthetic-close.json` lines 1–30 of 91 | 0 | 143775 |
| `run-command.png` | Escaped local viewer of the actually executed generator command and captured stdout/stderr/exit | 0 | 99619 |
| `report-page.png` | Original `demo/close-report-sample.html` loaded directly by `file://` | 0 | 191195 |
| `variance-csv.png` | Escaped local view of complete raw `demo/engine-run/reconciliation.csv`, header and all four rows | 0 | 111118 |

Every screen is labeled `SYNTHETIC SAMPLE — NOT A REAL LEDGER / 合成样例，非真实账本`. The input view explicitly identifies its excerpt and displays the full source hash; it does not pretend to show the entire JSON document. The run screen explicitly says **transcript viewer, not a native terminal screenshot**. Empty stdout/stderr are marked only when the captured stream was empty. The CSV view preserves the original leading apostrophes protecting negative numbers (`'-5.00000000` and `'-2.00000000`); it is not a reconstruction of the report table. CSV line-ending bytes are not visually distinguishable in a browser; the hash identifies the raw bytes.

`demo/close-report-sample-variance.csv` was created by `Path.write_bytes` from `demo/engine-run/reconciliation.csv` without parsing or recalculating values. Both have the same SHA-256 below. The four P1 variance amounts remain `3`, `-5`, `5`, `-2`; all amounts/identities/confirmations are synthetic.

No report redesign or engine modification occurred. The generator rewrote the report with exactly the same P1 HTML hash. The input, engine input/report/CSV, and generator hashes before and after capture are unchanged in the job manifest.

## Executed generation and capture commands

All commands ran from the worktree root above. The job-local driver was created outside the repository and invoked as:

```sh
python3 /tmp/omp-jobs/buildersplit-g1-pack-20261108-p2/capture_p2.py
```

Driver exit: **0**. It used `subprocess.run(..., text=True, capture_output=True)` for generation and each Chrome invocation, retaining actual streams and exit codes. It generated escaped local HTML text views and the byte-identical CSV copy; it did not manufacture a terminal transcript. The temporary executable driver was removed after successful capture; its invocation above is historical executed evidence, not a currently available script. The individual generation/capture commands and non-executable receipts remain available below.

Generation executed at `2026-11-08T11:40:41.706642+00:00`, completed at `2026-11-08T11:40:41.744744+00:00`, exit **0**:

```sh
python3 demo/generate_close_report.py demo/engine-run --output demo/close-report-sample.html
```

Captured stdout was exactly `demo/close-report-sample.html\n`; captured stderr was empty. This command renders the existing P1 bundle and checks JSON/CSV agreement; it does not independently authenticate data or replace engine replay verification.

Exact Chrome commands (each exit **0**, completed by `2026-11-08T11:40:43.217583+00:00`):

```sh
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --window-size=1100,1350 --screenshot=/root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p2/demo/screenshots/input-file.png file:///tmp/omp-jobs/buildersplit-g1-pack-20261108-p2/input-file.html
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --window-size=1100,1350 --screenshot=/root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p2/demo/screenshots/run-command.png file:///tmp/omp-jobs/buildersplit-g1-pack-20261108-p2/run-command.html
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --window-size=1100,1350 --screenshot=/root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p2/demo/screenshots/report-page.png file:///root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p2/demo/close-report-sample.html
unshare --user --map-root-user --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --window-size=1100,1350 --screenshot=/root/work/buildersplit-close/.worktrees/buildersplit-g1-pack-20261108-p2/demo/screenshots/variance-csv.png file:///tmp/omp-jobs/buildersplit-g1-pack-20261108-p2/variance-csv.html
```

Chrome stdout was empty in each case; stderr reported the corresponding byte count and screenshot filename shown above, with no other messages.

Job-local evidence remains under `/tmp/omp-jobs/buildersplit-g1-pack-20261108-p2/`:

- `input-file.html`, `run-command.html`, `variance-csv.html`: escaped local text viewers; no report replacement.
- `generation-transcript.json`, `generation-transcript.txt`: captured generator process details.
- `capture-evidence.json`: actual command, working directory, UTC times, exit, stdout, stderr for generation and four captures.
- `source-before.json`, `capture-manifest.json`: source and PNG SHA-256 values and capture provenance.

No capture scaffolding was added to the repository.

## SHA-256

PNG hashes computed from the generated files:

| Path | SHA-256 |
|---|---|
| `demo/screenshots/input-file.png` | `94991b9767a95321af5d43ff4dcef81e16134456ef8b6b2ddcb2e64c416cb56a` |
| `demo/screenshots/run-command.png` | `41384984ba221faa5f7ca06b2d9b91a1dd129f5a05bc6a62a9e41c3061ffd041` |
| `demo/screenshots/report-page.png` | `efc658c1cbc22f32fe322e5fd44456a2eb21077e11c62030204c46aab959394f` |
| `demo/screenshots/variance-csv.png` | `0e2a76d6cb88e51b89abf481d7335afc26ce902649db40c00728aebfd489f8ba` |

Source/copy hashes from the capture manifest:

| Path | SHA-256 |
|---|---|
| `demo/synthetic-close.json` | `7d0c9fdabe8a6fafd5c20eb1b80dc69ea3560b2bd57a84a09d572052ce387f5b` |
| `demo/engine-run/input.json` | `7a956cdbb59370aac6e1682a934dbcd392af648377fc3983899f3f97a6842275` |
| `demo/engine-run/report.json` | `6ea27133b0c15ce3ea912fbc0c205415b8209869955f779c72b9a8f581d5f2d7` |
| `demo/engine-run/reconciliation.csv` | `df5fb3e06aa264743b33aa3c52a4496017eb5a62c9ab33552ec27bf83cceb0bc` |
| `demo/close-report-sample-variance.csv` | `df5fb3e06aa264743b33aa3c52a4496017eb5a62c9ab33552ec27bf83cceb0bc` |
| `demo/close-report-sample.html` | `5d92861abe76f9b0db282beb208a6715077bce5192c23f2ac44232d98b06ee35` |
| `demo/generate_close_report.py` | `95f029292e6486ea4f633bb08b927b052a56d226917c0e6314e94a70f9d949c5` |

The fixture and HTML hashes match `demo/P1-VERIFY.md` exactly. `engine-run/input.json` is a distinct engine-bundle file, not the original fixture bytes; its hash must not be substituted for the fixture's P1 `input_sha256`.

## Parent-run checks and script self-check

The parent reported the following commands executed with exit **0** (not rerun by the capture worker):

```sh
python3 -m bsclose --verify-run demo/engine-run
sha256sum demo/synthetic-close.json demo/engine-run/reconciliation.csv demo/close-report-sample.html demo/close-report-sample.pdf
python3 -c 'from pathlib import Path; s=Path("demo/60s-script.md").read_text(); body=s.split("\n\n",1)[1].split("\n\nWord count:")[0]; n=len(body.split()); assert 110 <= n <= 150; assert f"Word count: {n}" in s; print(f"spoken_words={n}; at_140_wpm={n/140*60:.2f}s; at_130_wpm={n/130*60:.2f}s")'
```

Parent-reported replay result: `integrity=VERIFIED`, `status=DIAGNOSTIC_ONLY`, business hash `612ebab4581abe363c877c4b54f98c0903099bd26ad7e64b33d1b460197b3aa0`. Parent-reported input/CSV/HTML hashes match the table above; PDF SHA-256 is `a255396bb91aeb7a5431b57127f41594811322eb9d8f8a2e4a4095d5a1522473`, also matching P1.

Parent-reported script count is **123 spoken words**, excluding heading/count: **52.71 s at 140 wpm**, **56.77 s at 130 wpm**. Allowing approximately 3 seconds of pauses at 140 wpm gives approximately **56 seconds**. These are pacing estimates, not a measured human read-aloud trial or recording. The parent reports explicit First/Second/Third steps and synthetic-only qualification.

The parent's text-based nonexpert restatement self-check is: deliverable = “a local weekly fee/payout report and a CSV showing differences”; ask = “permission for a read-only sample checked on my own machine; no keys or money movement.” This is not an actual listener study. The capture worker did not edit `demo/60s-script.md` or claim a human check.

Parent final byte/type check, exit **0**:

```sh
cmp demo/engine-run/reconciliation.csv demo/close-report-sample-variance.csv && sha256sum demo/screenshots/input-file.png demo/screenshots/run-command.png demo/screenshots/report-page.png demo/screenshots/variance-csv.png && file demo/screenshots/input-file.png demo/screenshots/run-command.png demo/screenshots/report-page.png demo/screenshots/variance-csv.png
```

The parent reports the CSV copy is byte-identical, all four PNG hashes match the capture manifest, and all four files are **1100 × 1350 RGB PNGs**.

The parent opened all four PNGs using `read` and reported visual **PASS**: the input's labeled exact lines 1–30 and full source hash are visible; the command view's full command, actual stdout, empty stderr, exit 0, and HTML hash are readable; the original report's four accounting/variance rows, full hashes, header, and footer are visible without clipping; the raw CSV's complete header and all four rows, including original apostrophe-protected negatives, are visible. All four synthetic labels are visible. This is actual parent image inspection, not a human listener study.

Parent source-fidelity check: the initial checker exited **1** because it incorrectly removed the expected terminal newline; the actual viewer preserves that newline. No artifact change was needed. The corrected command exited **0**:

```sh
python3 -c 'from pathlib import Path; import re,html,json; j=Path("/tmp/omp-jobs/buildersplit-g1-pack-20261108-p2"); pre=lambda n: html.unescape(re.search(r"<pre[^>]*>(.*?)</pre>",(j/n).read_text(),re.S).group(1)); assert pre("input-file.html")=="".join(Path("demo/synthetic-close.json").read_text().splitlines(keepends=True)[:30]); assert pre("variance-csv.html")==Path("demo/engine-run/reconciliation.csv").read_text(); t=json.loads((j/"generation-transcript.json").read_text()); assert t["command"] in pre("run-command.html") and t["stdout"].strip() in pre("run-command.html"); assert t["exit_code"]==0 and t["stderr"]==""; print("Input excerpt and complete raw CSV text match source; rendered command/output match captured process receipt")'
```

This confirms the input excerpt and complete CSV text match their sources, and the rendered command/output match the captured process receipt. The parent also reports that all six `source_before` SHA-256 values remain unchanged, all four current PNG hashes equal the manifest, and the CSV's exact variance amounts are `3`, `-5`, `5`, `-2`. These are parent-run results; the capture worker did not rerun the checks.

Parent final integration evidence: `git diff --cached --check` exited **2**, reporting trailing whitespace on all five CSV rows because the byte-identical P1 CSV uses CRLF. Its bytes/hash were preserved; no newline normalization was applied. The CRLF-aware command below exited **0**, accepting intentional CRLF while retaining the other whitespace checks:

```sh
git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --cached --check
```

The parent reports `git status --short` and the cached diff stat show exactly seven new demo-only files: the script, this verification document, the CSV copy, and four PNGs; no tracked source changes. These integration results were not rerun by the capture worker.

## Limits and handoff

The capture worker inspected process outcomes, captured streams, written byte counts, and hashes only; the parent performed the final visual and byte/type checks documented above. A Chrome exit 0 alone does not prove visual acceptance. PNG hashes identify these exact captures and can change on rerender across environments.

No tests, lint, formatters, builds, deployments, payments, outbound contacts, or engine changes were performed by the capture worker. All pages were local and Chrome ran in an isolated network namespace. The sample remains `DIAGNOSTIC_ONLY`, `commercial_g0_passed=false`; successful generation/replay is not real-data approval, source authentication, production readiness, or a real payment confirmation. No human trial, recording, or customer validation is claimed.
