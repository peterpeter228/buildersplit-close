# PROGRESS — BuilderSplit Close

Updated: 2026-11-09 (Asia/Shanghai) by Rio executor, per owner rule t299u/t300u (verified branches merge to `main`).

## 已完成 / Done
- G0 synthetic reconciliation core (`bsclose/`, 40 unittest pass). Baseline SHA `c1a4593`. Synthetic only: `commercial_g0_passed=false` (no permitted real sample yet).
- G1 gap pack (branch `feat/g1-pack-20261108`, head `b94d106`), merged fast-forward to `main`:
  - P1 synthetic close report HTML/PDF (`demo/close-report-sample.*`, `demo/P1-VERIFY.md`)
  - P7 public-data Dextrabot fee estimate, labelled PUBLIC-DATA ESTIMATE, not engine result (`demo/close-dextrabot-public-week.*`, `demo/public-dextrabot/`)
  - P2 60s script + screenshots (`demo/60s-script.md`, `demo/screenshots/`)
  - P3 bilingual permission pack (`samples/`)
  - P4 public contacts research — PARTIAL: some named owners/contacts 未找到 (`research/`)
  - P5 outreach drafts — DRAFT ONLY, nothing sent (`outreach/`)
  - P6 interview template + synthetic example (`interviews/`)
- Gates: plan-review PASS P1–P7; diff-review PASS P2 and P7-r2 (BLOCKER 0); per-phase `*-VERIFY.md` executed evidence. Tests re-run on fresh clone 2026-11-09: `python3 -m unittest discover -s tests` → 40 OK.

## 下一步 / Next
1. Get written permission + real samples BS-SAMPLE-01/02, then run readonly G0 on permitted inputs with independent owner golden.
2. Fill P4 evidence gaps (named fee/reconciliation owners, direct contacts).
3. Outreach send is owner → Muse only; nothing is sent from this repo.

## 如何继续 / How to resume
```
git clone https://github.com/peterpeter228/buildersplit-close && cd buildersplit-close
python3 -m unittest discover -s tests
python3 -m bsclose examples/synthetic.json --output /tmp/bs-run && python3 -m bsclose --verify-run /tmp/bs-run
```
Work on a new branch from `main`; after independent verification PASS + green tests, merge back to `main` (no force-push) and update this file.

## 边界 / Still needs owner
Production deploy, repo visibility, license/IP, contest submission, any outbound message, any charge/real money.

## Key SHAs
- G0 core: `c1a4593`
- G1 pack head: `b94d106`

## DOT engineering takeover and audit repair — 2026-11-09

User explicitly returned engineering to dot and requested merge/push after
completion. Local work based on d583aa8; publication is subject to current
remote-head and single-writer coordination verification.

R1/R2/R3 repaired; 51 unittest tests, compileall, CLI export/replay/no-overwrite and
combined 50K fills / 10K rules / 50K payments capacity check passed. See
docs/AUDIT_REPAIR_20261109.md and its test log. No real adapter or commercial gate
upgrade: ADAPTER_UNVALIDATED remains enforced for non-synthetic input.
