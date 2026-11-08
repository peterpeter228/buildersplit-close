# P6 verification

Run from the P6 worktree root. Executed with Python 3.12.3; exit status **0**. The command checks the exact headers, one fully populated mock row, local evidence anchors, and PII/real-organization identifiers. Privacy scan scope is the mock row and its fictional notes below it, not the required comparison-tool header. The source-backed denylist includes the five contact organizations, aliases, other named organizations/products/publishers, the named person, and extracted channels/domains from `research/contacts-20261108.md`.

## Exact command

```bash
python3 -c 'from pathlib import Path
import re
text = Path("interviews/template.md").read_text()
lines = text.splitlines()
table = [line for line in lines if line.startswith("|")]
rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in table]
expected = ["date", "lead", "role", "concrete tasks (UTC period, owner role, tools, effort)", "tool gaps vs sheets/Hyperdash/Coinversa/Fuul/in-house", "299 interest (verbatim band, no leading)", "sample-permission intent", "counter-evidence (already-good solution?)", "links"]
assert len(rows) == 3, "Expected header, separator and one mock row"
assert rows[0] == expected, "Wrong column names or order"
assert len(rows[1]) == 9 and all(re.fullmatch(r":?-{3,}:?", c) for c in rows[1])
mock = rows[2]
assert len(mock) == 9 and all(mock), "Empty or missing mock cells"
assert all(not re.search(r"\b(TBD|TODO|placeholder)\b", c, re.I) for c in mock)
assert "SYNTHETIC" in table[2]
for anchor in re.findall(r"\]\(#([^)]+)\)", mock[8]):
    assert any(line.startswith("## ") and line[3:].lower().replace(" ", "-") == anchor for line in lines), anchor
print("Columns: 9/9; exact names and order: PASS")
print("Mock rows: 1; filled cells: 9/9; empty cells: 0; TBD/TODO/placeholder cells: 0")
print("SYNTHETIC label and local evidence anchors: PASS")
scan = text[text.index(table[2]):]
patterns = {"emails": r"[\w.+-]+@[\w.-]+", "@handles": r"(?<!\w)@[\w]+", "0x addresses": r"\b0x[a-fA-F0-9]+\b"}
for label, pattern in patterns.items():
    hits = re.findall(pattern, scan)
    assert not hits, label
    print(f"{label}: {len(hits)} matches")
contacts = Path("research/contacts-20261108.md").read_text()
identifiers = {"Legend", "Legend Trading", "legend.trade", "legend.xyz", "Dextrabot", "NFTinit", "pvp", "pvp.trade", "Owly", "Owly.fi", "owlyfi", "Invo", "Involio", "invoapp", "OCB", "OpenChainBench", "DefiLlama", "Hyperdash", "Hyperliquid", "TinyTech", "TinyTechFund", "Google Play", "Ryan", "Ryan Pace"}
assert all(name.casefold() in contacts.casefold() for name in identifiers)
identifiers.update(re.findall(r"[\w.+-]+@[\w.-]+|@[\w]+|\b(?:[\w-]+\.)+[A-Za-z]{2,}\b", contacts))
hits = [name for name in sorted(identifiers) if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", scan, re.I)]
assert not hits, hits
print(f"Contacts-derived firm/person/channel/domain identifiers: {len(identifiers)} checked; 0 matches")
print("PASS: complete synthetic mock; no scanned PII or real firm identifiers")'
```

## Observed output

```text
Columns: 9/9; exact names and order: PASS
Mock rows: 1; filled cells: 9/9; empty cells: 0; TBD/TODO/placeholder cells: 0
SYNTHETIC label and local evidence anchors: PASS
emails: 0 matches
@handles: 0 matches
0x addresses: 0 matches
Contacts-derived firm/person/channel/domain identifiers: 47 checked; 0 matches
PASS: complete synthetic mock; no scanned PII or real firm identifiers
```

## Acceptance review

- Exact nine-column table; one explicitly SYNTHETIC, fully filled row with fictional lead and role.
- Valid-interview checkbox requires UTC period/owner/tool/effort OR clear refusal plus why; all three stop-asking conditions are present.
- Mock includes a bounded UTC period, responsible role, tools, effort, a verbatim negative response and post-response band, fictional sample intent without authorization, and explicit already-good counter-evidence.
- Local links lead only to fictional notes. No real interview, outreach, customer data, or sample permission is claimed.
- Automated patterns and contacts-derived identifiers are a bounded scan, not a universal identity detector. Manual review found no real person or firm in the mock. Required comparison-tool names remain in the header only.

VERDICT: PASS

| id | severity | requirement | evidence | minimal_fix |
|---|---|---|---|---|
| — | — | P6 requirements and global bans | `template.md:3–24`; command/output above | None |

BLOCKER_COUNT: 0
SUGGESTION_COUNT: 0
