# P5 draft verification

Drafts: `outreach/short-first-touch.md`. No messages sent and no deletion or other data operation performed.

## Exact counting command

Run from the repository root. This extracts exactly the three fenced `text` message bodies. `str.split()` counts include greetings and signoffs; headings, recipient metadata, safety labels and operator notes are excluded. Times are calculated as `n * 60 / 150` seconds.

```sh
python3 - <<'PY'
from pathlib import Path
import re

source = Path("outreach/short-first-touch.md").read_text(encoding="utf-8")
bodies = re.findall(r"^```text\n(.*?)^```$", source, flags=re.MULTILINE | re.DOTALL)
assert len(bodies) == 3, f"Expected three text bodies, found {len(bodies)}"
for label, body in zip(("First touch", "Follow-up", "Decline reply"), bodies):
    n = len(body.split())
    seconds = n * 60 / 150
    print(f"{label}: {n} words; {seconds:.2f} seconds at 150 wpm")
PY
```

Acceptance: first touch at most 75 words, satisfying both the 80-word ceiling and the 30-second ceiling at 150 words per minute; follow-up at most 50 words. The decline reply has no specified word ceiling.

## Evidence status

Parent-reported verification: the exact fenced shell command above was executed through a temporary standalone Python subprocess verifier after eval was denied. Exit status: 0. Actual output:

```text
First touch: 64 words; 25.60 seconds at 150 wpm
Follow-up: 35 words; 14.00 seconds at 150 wpm
Decline reply: 40 words; 16.00 seconds at 150 wpm
```

Times are calculated at 150 words per minute, not measured from a human recording. Recount words and recalculate times if placeholders are replaced.

The parent reports that the verifier also passed the exact one-line header, three safety labels, `[name/role]` in each body, word/time ceilings and exclusion of pitch terms.

The parent manually reviewed all copy and confirmed:

- The first touch truthfully identifies the BuilderSplit Close team and local, read-only prototype, compares builder fees owed versus paid for a completed week, asks who owns reconciliation and offers five asynchronous written questions by email with no call needed.
- The follow-up is a single nudge around day +3, only if there is no reply or decline, with no further nudges.
- The decline reply thanks the recipient, commits to stopping outreach, retaining only a minimal do-not-contact record and anonymized decline note, and deleting any supplied data and working copies, including derived reports and retained copies. These are future commitments, not completed deletion claims.
- There are no P4 recipient names, pricing pitches, yield promises, private-key requests or payment asks. Safety labels are outside each message. Sending is Muse-only after owner approval; no contact or deletion was performed.

Provenance: baseline `8320da3`. P4's PARTIAL contact gaps are not inherited as a P5 failure. The P5 plan review is PASS with zero blockers at `/workspace/loop/buildersplit-g1-pack-20261108/plan-review-p5.md`.

The drafting worker ran no checks, builds, lint, tests or formatters; the execution and manual-review evidence above was supplied by the parent.
