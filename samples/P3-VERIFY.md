# P3 artifact verification

## State and scope

**PASS — P3 resume attempt 2.** The three content documents are unchanged from attempt 1. SHA-256, filename-only identifier scan, executable table/placeholder parser and offline local render completed successfully. No permission or records received, no signature/agreement implied. This is document-preparation evidence, not real-data validation. No outbound contact, deployment, charge, broadcast, engine/adapter change, main or PR #1 mutation, or P4 work.

| Content file | SHA-256 |
| --- | --- |
| `samples/permission-pack.md` | `85a30940803532dffa2826fb67374fe2d1487a387872dee0dcb91504d07376c2` |
| `samples/permission-letter-template.md` | `428d79a88cd09579c5be54c970a3cf440984469971548c954d9997289f2a9f9c` |
| `samples/bs-sample-checklists.md` | `bbe533b60cda5365c22de61a1640e4ddf653ce5b084e78dd95b9717eb4f30d1d` |

`samples/P3-VERIFY.md` is excluded from its own hash table to avoid self-reference. Its final SHA-256 is recorded in `result-p3.json` alongside all three content hashes.

**Manual review:** read all three complete documents, including long checklist lines in raw mode, and compared A–E with `docs/CUSTOMER_SAMPLE_CHECKLIST.md` items 1–9 and safe collection. Only generic organisation/role labels, BS-SAMPLE-01/02, document references and unfilled `[ ]` fields occur; no actual customer names, physical addresses, emails or keys were found. Regex cannot prove arbitrary names absent or recognize every address/secret format. Both samples retain identical A–E requirements and all canonical constraints. The bilingual pack explains native splits and paid mapping, requires unrelated organisations, and covers local-only preference, pseudonyms, retention, deletion and revocation. All three documents explicitly disclaim received permission or agreement.

## Executed commands and outputs

Commands below ran from the P3 worktree. Exit codes refer to the command named, not merely the trailing `printf`.

### Earlier tool limitations (not passing evidence)

- Attempt 1 could not execute shell/parser/render checks because execution tools required unavailable approval.
- Attempt 2 Python Eval remained policy-denied; no code executed in that call. The prescribed shell commands below ran using the available Bash tool.
- `preview_export` with `format=png`, `source=file`, `path=samples/permission-pack.md`, `fontSizePx=14`, and output `/tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-preview.png` reported success, but the output was invalid: `file` returned `data`; its first bytes were `d77efcd3bf3bd75d`, not the PNG signature. Image read failed. The tool defect was reported; this output is not visual proof. Installed Pandoc/Chrome produced the valid replacement below without downloads.


### Hashes

```sh
sha256sum samples/permission-pack.md samples/permission-letter-template.md samples/bs-sample-checklists.md
```

Exit **0**. Output:

```text
85a30940803532dffa2826fb67374fe2d1487a387872dee0dcb91504d07376c2  samples/permission-pack.md
428d79a88cd09579c5be54c970a3cf440984469971548c954d9997289f2a9f9c  samples/permission-letter-template.md
bbe533b60cda5365c22de61a1640e4ddf653ce5b084e78dd95b9717eb4f30d1d  samples/bs-sample-checklists.md
```

### Filename-only grep and exit status

This conservative scanner covers common email, hexadecimal blockchain address/key, PEM key header, common key-prefix and street-address shapes. It does not prove the absence of arbitrary names, all addresses or all secrets; retain the manual review above.

```sh
grep -Eil -- '[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}|0x[[:xdigit:]]{40,64}|[[:xdigit:]]{64}|-----BEGIN[ A-Z]*PRIVATE KEY-----|(AKIA|ASIA)[A-Z0-9]{16}|sk[-_][[:alnum:]_-]{20,}|[0-9]{1,6}[[:blank:]]+([[:alpha:].-]+[[:blank:]]+){1,5}(street|st|road|rd|avenue|ave|lane|ln|drive|dr|boulevard|blvd)\b|(省|市|区|县).{0,24}(路|街|巷).{0,12}[0-9０-９]+号' samples/permission-pack.md samples/permission-letter-template.md samples/bs-sample-checklists.md
scan_status=$?
printf 'grep exit status: %s\n' "$scan_status"
```

Actual output (no filenames emitted):

```text
grep exit status: 1
```

Grep exit **1** means no matches; wrapper exit **0**. Exit 0 from grep would mean a matching filename; 2 would mean an error. Only the three content files are scanned: this evidence file intentionally contains scanner patterns and content hashes, not customer data.

### Executable table/placeholder parser

```sh
python3 - <<'PY'
from pathlib import Path
import re

text = Path('samples/bs-sample-checklists.md').read_text(encoding='utf-8')
sections = re.findall(r'^## (BS-SAMPLE-0[12])\n(.*?)(?=^## |\Z)', text, re.M | re.S)
assert [name for name, _ in sections] == ['BS-SAMPLE-01', 'BS-SAMPLE-02']
requirements = []
total = 0
for name, body in sections:
    rows = []
    for line in body.splitlines():
        if not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if cells[0] == 'Item' or all(re.fullmatch(r':?-+:?', cell) for cell in cells):
            continue
        assert len(cells) == 3, (name, 'malformed row')
        rows.append(cells)
    assert [row[0] for row in rows] == list('ABCDE'), (name, 'labels/count')
    assert all(row[2] == '' for row in rows), (name, 'nonempty status')
    requirements.append([(row[0], row[1]) for row in rows])
    total += len(rows)
    print(f'{name}: A-E; 5/5 status cells empty')
assert requirements[0] == requirements[1], 'shared definitions differ'
assert total == 10
letter = Path('samples/permission-letter-template.md').read_text(encoding='utf-8')
placeholders = re.findall(r'\[[^\]\n]*\]', letter)
assert placeholders and all(value == '[ ]' for value in placeholders)
assert letter.count('[') == letter.count(']') == len(placeholders)
fields = []
for line in letter.splitlines():
    if not line.startswith('|'):
        continue
    cells = [cell.strip() for cell in line.split('|')[1:-1]]
    if cells[0] == '项目 / Field' or all(re.fullmatch(r':?-+:?', cell) for cell in cells):
        continue
    assert len(cells) == 2 and cells[1] == '[ ]', 'nonblank letter field'
    fields.append(cells)
assert len(fields) == 14
print('TOTAL: 10/10 status cells empty; shared A-E definitions identical')
print(f'LETTER: {len(fields)} blank fields; {len(placeholders)} placeholders, all [ ]')
PY
parser_status=$?
printf 'parser exit status: %s\n' "$parser_status"
```

Actual output:

```text
BS-SAMPLE-01: A-E; 5/5 status cells empty
BS-SAMPLE-02: A-E; 5/5 status cells empty
TOTAL: 10/10 status cells empty; shared A-E definitions identical
LETTER: 14 blank fields; 16 placeholders, all [ ]
parser exit status: 0
```

Parser exit **0**, wrapper exit **0**. All status cells are whitespace-only, not `[ ]`, dashes or pending labels. The 16 letter placeholders comprise 14 table fields and two literal-format instructions.

### Render

Used installed `/usr/bin/pandoc`, `/usr/bin/google-chrome` and `/usr/bin/unshare`; no dependency installation. Network was isolated with `unshare --net`.

Temporary stylesheet `/tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-print.css`:

```css
@page { size: A4; margin: 10mm; }
html { color: #111; background: white; }
body { font-family: 'Noto Sans CJK SC', sans-serif; font-size: 12px; line-height: 1.35; max-width: 718px; margin: 20px auto; }
h1 { font-size: 20px; line-height: 1.2; margin: 0 0 10px; }
h2 { font-size: 15px; margin: 12px 0 6px; }
p { margin: 5px 0; }
ul { margin: 5px 0; padding-left: 20px; }
li { margin: 0 0 7px; }
a { color: inherit; }
@media print { body { margin: 0; max-width: none; } }
```

Executed command:

```sh
pandoc samples/permission-pack.md --standalone --metadata title='Local reconciliation permission pack' --css=/tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-print.css --output=/tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-local.html && unshare --net google-chrome --headless --no-sandbox --disable-gpu --disable-background-networking --no-pdf-header-footer --print-to-pdf=/tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-local.pdf --screenshot=/tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-local.png --window-size=794,1123 file:///tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-local.html
```

Exit **0**. Output:

```text
253622 bytes written to file /tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-local.png
318818 bytes written to file /tmp/omp-jobs/buildersplit-g1-pack-20261108-p3/permission-pack-local.pdf
```

Executed structural check:

```sh
python3 - <<'PY'
from pathlib import Path
import re, struct
p = Path('/tmp/omp-jobs/buildersplit-g1-pack-20261108-p3')
pdf = (p/'permission-pack-local.pdf').read_bytes()
png = (p/'permission-pack-local.png').read_bytes()
assert pdf.startswith(b'%PDF-')
assert png.startswith(b'\x89PNG\r\n\x1a\n')
pages = len(re.findall(rb'/Type\s*/Page\b', pdf))
print('PDF pages:', pages)
print('PNG dimensions:', *struct.unpack('>II', png[16:24]))
assert pages == 1
print('Render checks: PASS')
PY
```

Exit **0**. Output:

```text
PDF pages: 1
PNG dimensions: 794 1123
Render checks: PASS
```

**Visual inspection:** opened the valid PNG with the image reader. Chinese and English glyphs, all three requested sections, both sample conditions, template disclaimer and final retention/deletion/revocation paragraph are visible without clipping or overlap. One A4 PDF page was counted; the screenshot shows the same rendered HTML at 794×1123. Pandoc adds an English title above the source heading. This is a local readability/layout check, not a human comprehension study. Temporary render files are removed after inspection; commands and findings are retained here.
