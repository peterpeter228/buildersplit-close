"""Reproduce the frozen P7 public-fee estimate offline; Python 3 stdlib only.

Run: python3 demo/public-dextrabot/summarize_public_fees.py
This is not an engine adapter, ledger reconciliation, or completeness check.
"""
import csv
from datetime import datetime
from decimal import Decimal, DecimalException, Inexact, localcontext
import hashlib
from html import escape
import io
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
DEMO = HERE.parent
BUILDER = "0x49ae63056b3a0be0b166813ee687309ab653c07c"
START = "2026-11-01T00:00:00Z"
END = "2026-11-08T00:00:00Z"
BANNER = "PUBLIC-DATA ESTIMATE — NOT THE BUILDER'S BOOKS / 公开数据估算，非对方账本"
UNKNOWN = "UNKNOWN"
CSV_FIELDS = (
    "time", "user", "coin", "side", "px", "sz", "crossed", "special_trade_type",
    "tif", "is_trigger", "counterparty", "closed_pnl", "twap_id", "builder_fee",
)
UNKNOWN_FIELDS = (
    "payouts", "opening_balance", "closing_balance", "carryforward_balance",
    "splits", "independent_closing_statement", "statement_variance",
)
CAVEAT = (
    "OpenChainBench/Totalis ~12:10 UTC daily cutoff caveat: their aggregates may "
    "differ from a full UTC-day window and these saved exports. Observed first/last "
    "fills do not establish complete coverage or prove a cutoff. No node data, "
    "reconstructed afternoons, extrapolation or missing-activity zeros are used."
)


def frozen_sources():
    """Read existing provenance, then hash every frozen raw source before use."""
    entries = []
    inputs = {}
    for line in (HERE / "SOURCES.md").read_text(encoding="utf-8").splitlines():
        if not re.fullmatch(r"\|[^|]+\|https://[^|]+\|[0-9:.]+\|[0-9a-f]{64}\|", line):
            continue
        name, url, fetched, expected = line.strip("|").split("|")
        if Path(name).name != name:
            raise ValueError("Unexpected source filename")
        data = (HERE / "raw" / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError("Frozen source SHA-256 mismatch: " + name)
        inputs["raw/" + name] = data
        entries.append({"file": "raw/" + name, "url": url,
                        "fetched_at": "2026-11-08T" + fetched + "+08:00",
                        "sha256": expected})
    expected_names = {f"raw/202611{day:02}.csv.lz4" for day in range(1, 8)} | {
        "raw/defillama-dextrabot.ts", "raw/ocb-builders.json", "raw/ocb-method.html"}
    if len(entries) != 10 or {entry["file"] for entry in entries} != expected_names:
        raise ValueError("Expected exactly the ten P7 frozen source manifest entries")
    return entries, inputs


def decode_frozen_lz4(data):
    """Decode only these SHA-256-bound, independent 64 KiB–1 MiB LZ4 frames.

    Caller must hash-check bytes against SOURCES.md first. The descriptor is
    version 1, independent blocks, content checksum, no size/dictionary fields.
    SHA-256 binds the descriptor, blocks and trailing content checksum; this is
    deliberately not a general LZ4 decoder or an xxHash checksum implementation.
    """
    block_limits = {bytes.fromhex("04224d186440a7"): 65536,
                    bytes.fromhex("04224d18645008"): 262144,
                    bytes.fromhex("04224d18646085"): 1048576}
    if data[:7] not in block_limits:
        raise ValueError("Unsupported frozen LZ4 frame descriptor")
    limit = block_limits[data[:7]]
    position = 7
    output = bytearray()
    while True:
        if position + 4 > len(data):
            raise ValueError("Truncated frozen LZ4 block header")
        size = int.from_bytes(data[position:position + 4], "little")
        position += 4
        if size == 0:
            if position + 4 != len(data):
                raise ValueError("Expected one LZ4 content checksum and no trailing frame")
            return bytes(output)
        uncompressed = bool(size & 0x80000000)
        size &= 0x7fffffff
        if not 0 < size <= limit or position + size > len(data):
            raise ValueError("Invalid frozen LZ4 block size")
        block = data[position:position + size]
        position += size
        if uncompressed:
            output.extend(block)
            continue
        decoded = bytearray()
        cursor = 0

        def length(initial):
            nonlocal cursor
            count = initial
            if initial == 15:
                while True:
                    if cursor >= len(block):
                        raise ValueError("Truncated LZ4 length")
                    extra = block[cursor]
                    cursor += 1
                    count += extra
                    if extra != 255:
                        break
            return count

        while cursor < len(block):
            token = block[cursor]
            cursor += 1
            literal_length = length(token >> 4)
            if cursor + literal_length > len(block):
                raise ValueError("Truncated LZ4 literals")
            decoded.extend(block[cursor:cursor + literal_length])
            cursor += literal_length
            if cursor == len(block):
                break
            if cursor + 2 > len(block):
                raise ValueError("Truncated LZ4 offset")
            offset = int.from_bytes(block[cursor:cursor + 2], "little")
            cursor += 2
            match_length = length(token & 15) + 4
            if not 0 < offset <= len(decoded) or len(decoded) + match_length > limit:
                raise ValueError("Invalid independent LZ4 match")
            for _ in range(match_length):
                decoded.append(decoded[-offset])
        if len(decoded) > limit:
            raise ValueError("Decoded LZ4 block exceeds its declared limit")
        output.extend(decoded)


def summarize(sources, inputs):
    adapter = inputs["raw/defillama-dextrabot.ts"].decode("utf-8")
    registry = json.loads(inputs["raw/ocb-builders.json"])
    if (f'HL_BUILDER_ADDRESS = "{BUILDER}"' not in adapter
            or not any(item.get("slug") == "dextrabot" and item.get("address") == BUILDER
                       for item in registry)):
        raise ValueError("Saved attribution sources do not identify the expected builder")
    if "builder fee in USDC" not in inputs["raw/ocb-method.html"].decode("utf-8"):
        raise ValueError("Saved methodology no longer supplies the fee unit")
    start, end = (datetime.fromisoformat(value.replace("Z", "+00:00"))
                  for value in (START, END))
    daily = []
    total = Decimal("0")
    with localcontext() as context:
        context.prec = 80
        context.traps[Inexact] = True
        for source in sorted(sources, key=lambda item: item["file"]):
            name = Path(source["file"]).name
            if not name.endswith(".csv.lz4"):
                continue
            expected_url = ("https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/"
                            + BUILDER + "/" + name)
            if source["url"] != expected_url:
                raise ValueError("Saved export URL has an unexpected builder: " + name)
            decoded = decode_frozen_lz4(inputs[source["file"]])
            reader = csv.DictReader(io.StringIO(decoded.decode("utf-8"), newline=""))
            if reader.fieldnames != list(CSV_FIELDS):
                raise ValueError("Unexpected frozen CSV schema: " + name)
            count = included = 0
            subtotal = Decimal("0")
            first = last = None
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Malformed CSV record: " + name)
                stamp, value = row["time"], row["builder_fee"]
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", stamp):
                    raise ValueError("Expected an explicit UTC second timestamp: " + name)
                instant = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                if not re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value):
                    raise ValueError("Expected a finite plain builder_fee decimal: " + name)
                fee = Decimal(value)
                count += 1
                first = stamp if first is None else min(first, stamp)
                last = stamp if last is None else max(last, stamp)
                if start <= instant < end:
                    included += 1
                    subtotal += fee
            total += subtotal
            daily.append({
                "date": name[:4] + "-" + name[4:6] + "-" + name[6:8],
                "file": source["file"], "source_sha256": source["sha256"],
                "decoded_sha256": hashlib.sha256(decoded).hexdigest(),
                "saved_rows": count, "in_period_rows": included,
                "outside_period_rows": count - included,
                "first_observed_time": first or UNKNOWN,
                "last_observed_time": last or UNKNOWN,
                "builder_fee_sum": format(subtotal, "f"),
            })
    engine_bytes = (HERE / "engine-run" / "report.json").read_bytes()
    engine = json.loads(engine_bytes)
    if (engine["status"] != "BLOCKED" or engine["calculations"] != []
            or engine["commercial_g0_passed"] is not False
            or not any(issue["code"] == "ADAPTER_UNVALIDATED" for issue in engine["issues"])):
        raise ValueError("Expected the preserved BLOCKED / ADAPTER_UNVALIDATED engine evidence")
    return {
        "sample_class": "PUBLIC_DATA_ESTIMATE", "status": "PUBLIC_FEE_SUMMARY_ONLY",
        "not_engine_reconciliation": True, "commercial_g0_passed": False,
        "owner_decision": "t256u P7-Q1=A, 2026-11-08T17:37+08:00; acceptance adjusted",
        "builder": BUILDER, "builder_label": "Dextrabot (public attribution, not ownership proof)",
        "builder_identity_basis": "Per-builder source URL plus saved DefiLlama and OpenChainBench registry; no builder column in CSV",
        "period_start": START, "period_end": END, "period_interval": "[start,end)",
        "csv_fields": list(CSV_FIELDS), "timestamp_encoding": "ISO 8601 UTC seconds with explicit Z",
        "unit": "USDC",
        "unit_basis": "Saved OpenChainBench methodology explicitly describes builder fee in USDC; CSV has no currency column. No USD/FX conversion or fee-rate inference.",
        "sum_method": "Decimal precision 80 with Inexact trapped; sum each saved in-window builder_fee once, no rounding, scaling or deduplication",
        "counts": {key: sum(day[key] for day in daily)
                   for key in ("saved_rows", "in_period_rows", "outside_period_rows")},
        "builder_fee_pool": {"public_observed_builder_fee": format(total, "f"),
                             "ledger_fee_pool": UNKNOWN,
                             **{key: UNKNOWN for key in UNKNOWN_FIELDS}},
        "daily": daily, "coverage": UNKNOWN, "coverage_caveat": CAVEAT,
        "limitations": "Observed public fees only; not complete revenue, beneficiary entitlements, settlement, ledger accuracy, ownership or a G0 real-sample substitute. No real-money or adapter gate is unlocked.",
        "source_manifest": {"file": "public-dextrabot/SOURCES.md",
                            "sha256": hashlib.sha256((HERE / "SOURCES.md").read_bytes()).hexdigest()},
        "sources": sources,
        "generator": {"file": "public-dextrabot/summarize_public_fees.py",
                      "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "engine_evidence": {"file": "public-dextrabot/engine-run/report.json",
                            "sha256": hashlib.sha256(engine_bytes).hexdigest(),
                            "status": engine["status"], "issue": "ADAPTER_UNVALIDATED",
                            "calculations": [], "note": "Preserved compatibility probe, not the source of this sum; empty arrays mean not mapped, not zero activity"},
    }


def variance_csv(summary):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(("metric", "public_observed_value", "ledger_value", "unit", "variance"))
    writer.writerow(("builder_fee_pool", summary["builder_fee_pool"]["public_observed_builder_fee"],
                     UNKNOWN, summary["unit"], UNKNOWN))
    for key in UNKNOWN_FIELDS:
        writer.writerow((key, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN))
    return stream.getvalue()


def render(summary, summary_sha256):
    pool = escape(summary["builder_fee_pool"]["public_observed_builder_fee"])
    days = "".join(
        "<tr><th scope='row'>" + day["date"] + "</th><td>" + str(day["in_period_rows"])
        + "</td><td>" + day["first_observed_time"][11:] + "</td><td>"
        + day["last_observed_time"][11:] + "</td><td>" + day["builder_fee_sum"] + "</td></tr>"
        for day in summary["daily"])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BuilderSplit Close · Dextrabot public-data estimate</title>
<style>
@page {{ size: A4 portrait; margin: 12mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; color: #20262e; background: #fff; font: 9pt/1.4 "WenQuanYi Zen Hei", sans-serif; }}
main {{ max-width: 186mm; margin: 0 auto; }}
.banner {{ color: #b00020; border: 1.5px solid #b00020; padding: 6px; text-align: center; font-size: 9pt; font-weight: bold; }}
h1 {{ font-size: 18pt; margin: 10px 0 0; }}
h2 {{ font-size: 10.5pt; margin: 10px 0 4px; }}
p {{ margin: 4px 0; }}
.subtitle {{ color: #485462; margin-bottom: 8px; }}
.meta {{ padding: 7px 9px; background: #f3f5f7; border-left: 3px solid #485462; }}
.label {{ font-weight: bold; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8pt; table-layout: fixed; }}
th, td {{ padding: 4px; border-bottom: 1px solid #ccd1d7; text-align: right; overflow-wrap: anywhere; font-variant-numeric: tabular-nums; }}
thead th {{ background: #edf0f4; }}
th:first-child {{ text-align: left; width: 24%; font-weight: normal; }}
thead th:first-child {{ font-weight: bold; }}
.daily th:first-child {{ width: 18%; }}
.note {{ font-size: 8pt; color: #424d59; }}
.hash {{ font-size: 7.5pt; overflow-wrap: anywhere; }}
.identity {{ border-top: 1px solid #ccd1d7; padding-top: 4px; }}
footer {{ margin-top: 10px; }}
section, tr, footer {{ break-inside: avoid; }}
a {{ color: #344d69; }}
@media screen {{ body {{ padding: 18px; background: #e8ebef; }} main {{ background: white; padding: 12mm; box-sizing: content-box; }} }}
@media print {{ body {{ print-color-adjust: exact; -webkit-print-color-adjust: exact; }} }}
</style>
</head>
<body><main>
<header>
<div class="banner">{BANNER}</div>
<h1>BuilderSplit Close <span style="font-size:12pt">Dextrabot 公开费用估算</span></h1>
<p class="subtitle">Not an engine reconciliation result / 非引擎核账结果 · Not a payment instruction / 非付款指令</p>
</header>
<section class="meta" aria-label="Public estimate scope">
<p><span class="label">Builder：</span>{BUILDER}（公开归属，不证明所有权）</p>
<p><span class="label">周期 [start,end)：</span>[{START}, {END}) · UTC</p>
<p><span class="label">范围：</span>{summary['counts']['in_period_rows']:,} observed export rows / 7 saved daily files；窗口外 {summary['counts']['outside_period_rows']} 行</p>
<p><span class="label">单位：</span>USDC（冻结 OCB 方法说明；CSV 无币种列；无 USD/汇率换算、无费率推算）</p>
<p><span class="label">授权：</span>t256u · P7-Q1=A · acceptance adjusted；PUBLIC_FEE_SUMMARY_ONLY · commercial_g0_passed=false</p>
</section>
<section>
<h2>1 · 单一费用池 / Observed public fee pool</h2>
<table aria-label="Observed builder fee pool and unknown ledger fields">
<thead><tr><th>公开费用池</th><th>Observed fees<br>USDC</th><th>已付<br>Payouts</th><th>期初<br>Opening</th><th>期末<br>Closing</th><th>结转<br>Carryforward</th></tr></thead>
<tbody><tr><th scope="row">builder fee pool</th><td>{pool}</td><td>UNKNOWN</td><td>UNKNOWN</td><td>UNKNOWN</td><td>UNKNOWN</td></tr></tbody>
</table>
<p class="note">Splits / 分账、independent statement / 独立账单、statement variance / 账单差异：<strong>UNKNOWN</strong>。无收款人分配、无付款或余额零值；CSV 所有 variance 均为 UNKNOWN。</p>
</section>
<section>
<h2>2 · 冻结导出覆盖 / Saved export observations</h2>
<table class="daily" aria-label="Daily observed export row counts times and builder fees">
<thead><tr><th>UTC date</th><th>Rows in window</th><th>First observed UTC</th><th>Last observed UTC</th><th>builder_fee sum · USDC</th></tr></thead>
<tbody>{days}</tbody>
</table>
<p class="note">按 CSV 明示 UTC 时间筛选，Decimal 原值相加；不舍入、不补齐、不去重。首末时间仅为观察到的成交边界，不证明日覆盖完整或具体截断时间。</p>
<p class="note"><strong>OpenChainBench/Totalis ~12:10 UTC daily cutoff caveat:</strong> their aggregates may differ from a full UTC-day window and these exports. OCB reports node substitution/reconstruction; none is used here. 不外推午后、不将缺失成交视为零。</p>
</section>
<section class="identity">
<h2>3 · 来源与保留的引擎阻断 / Provenance &amp; engine boundary</h2>
<p class="note">归属依据：<a href="https://raw.githubusercontent.com/DefiLlama/dimension-adapters/master/dexs/dextrabot.ts">DefiLlama</a> + <a href="https://raw.githubusercontent.com/ChainBench/OpenChainBench/main/harnesses/hyperliquid-frontends/builders.json">OpenChainBench / HyperTracker registry</a>。获取：2026-11-08 17:22:00.288493–17:22:22.657147 +08:00（Asia/Shanghai）；精确 URL、逐文件时间及原始 SHA-256 见 <a href="public-dextrabot/SOURCES.md">SOURCES.md</a>。</p>
<p class="hash">Summary JSON SHA-256: {summary_sha256}<br>Source manifest SHA-256: {summary['source_manifest']['sha256']}</p>
<p class="note">保留 <a href="public-dextrabot/engine-run/report.json">engine-run/report.json</a>：<strong>BLOCKED / ADAPTER_UNVALIDATED</strong>，calculations=[]（未映射，不是零成交）。本页非该引擎输出；未修改引擎或真实 adapter。</p>
<p class="note"><a href="public-dextrabot/summary.json">Summary JSON</a> · <a href="close-dextrabot-public-week-variance.csv">Variance CSV</a> · <a href="P7-METHOD.md">Method &amp; reproduction</a>。哈希不是来源认证；不证明完整收入、账本准确性、结算或受益权；<strong>not a G0 real-sample substitute</strong>，不解锁真实资金或 adapter 门槛。</p>
</section>
<footer><div class="banner">{BANNER}</div></footer>
</main></body></html>
"""


def main():
    sources, inputs = frozen_sources()
    summary = summarize(sources, inputs)
    encoded = (json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    summary_sha256 = hashlib.sha256(encoded).hexdigest()
    outputs = (
        (HERE / "summary.json", encoded),
        (DEMO / "close-dextrabot-public-week.html", render(summary, summary_sha256).encode("utf-8")),
        (DEMO / "close-dextrabot-public-week-variance.csv", variance_csv(summary).encode("utf-8")),
    )
    for path, data in outputs:
        path.write_bytes(data)
        print(hashlib.sha256(data).hexdigest() + "  " + str(path.relative_to(DEMO.parent)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, csv.Error, DecimalException) as exc:
        raise SystemExit("ERROR: " + str(exc))
