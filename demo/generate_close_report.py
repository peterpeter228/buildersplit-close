"""Render an engine bundle as an offline synthetic A4 sample; Python 3 stdlib only.

Usage: python3 demo/generate_close_report.py demo/engine-run
This checks JSON/CSV agreement, not replay, authenticity, or customer review.
"""
import argparse
import csv
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from html import escape
import json
from pathlib import Path
import re


BANNER = "SYNTHETIC SAMPLE — NOT A REAL LEDGER / 合成样例，非真实账本"
COLUMNS = (
    "beneficiary_id", "currency_id", "opening", "accrual", "external_paid",
    "closing_calculated", "customer_closing_statement", "statement_variance",
)
MONEY_COLUMNS = COLUMNS[2:]


def load_bundle(bundle):
    report = json.loads((bundle / "report.json").read_text(encoding="utf-8"))
    if (report["sample_class"] != "SYNTHETIC"
            or report["status"] != "DIAGNOSTIC_ONLY"
            or report["commercial_g0_passed"] is not False
            or report["issues"]):
        raise ValueError("Only unblocked SYNTHETIC / DIAGNOSTIC_ONLY reports are supported")
    scope = report["scope"]
    start, end = (datetime.fromisoformat(scope[key].replace("Z", "+00:00"))
                  for key in ("period_start", "period_end"))
    if (start.utcoffset() != timedelta(0) or end.utcoffset() != timedelta(0)
            or end - start != timedelta(days=7)
            or end > datetime.now(timezone.utc)):
        raise ValueError("The sample requires an ended seven-day UTC [start,end) period")
    if (scope["builder"] != "0x1111111111111111111111111111111111111111"
            or scope["network"] != "hypercore-mainnet"
            or scope["fee_currency_id"] != "hypercore-mainnet:USDC"):
        raise ValueError("Only the explicitly fake Builder / USDC sample scope is supported")
    rows = report["calculations"]
    count = report["counts"]["input_fills"]
    if type(count) is not int or not 0 <= count <= 50000 or not 1 <= len(rows) <= 100:
        raise ValueError("Sample limit: 50,000 fills and 100 payees")
    for key in ("input_sha256", "rule_set_hash"):
        if not re.fullmatch(r"[0-9a-f]{64}", report[key]):
            raise ValueError("Missing engine SHA-256 field: " + key)
    for row in rows:
        if row["currency_id"] != scope["fee_currency_id"]:
            raise ValueError("Mixed currencies are not supported")
        for key in MONEY_COLUMNS:
            if (not isinstance(row[key], str)
                    or not re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", row[key])):
                raise ValueError("Expected an engine decimal string: " + key)
    # Match the engine's spreadsheet-injection protection, including negative money.
    expected = []
    for row in rows:
        cells = []
        for key in COLUMNS:
            value = str(row[key])
            cells.append("'" + value if value.lstrip().startswith(
                ("=", "+", "-", "@", "\t", "\r")) else value)
        expected.append(cells)
    with (bundle / "reconciliation.csv").open(encoding="utf-8", newline="") as handle:
        actual = list(csv.reader(handle))
    if actual != [list(COLUMNS), *expected]:
        raise ValueError("reconciliation.csv does not match report.json")
    samples = [row for row in rows if Decimal(row["statement_variance"]) != 0][:5]
    if len(samples) < 3:
        raise ValueError("Need at least three nonzero variance rows; use demo/synthetic-close.json")
    return report, samples


def amount(row, key, signed=False):
    """Preserve every engine decimal digit; never use float or presentation rounding."""
    value = row[key]
    if signed and Decimal(value) > 0:
        value = "+" + value
    return escape(value)


def render(report, samples):
    scope = report["scope"]
    balances = "".join(
        "<tr><th scope='row'>" + escape(row["beneficiary_id"]) + "</th>"
        + "".join("<td>" + amount(row, key) + "</td>" for key in (
            "accrual", "external_paid", "opening", "closing_calculated", "closing_calculated"))
        + "</tr>" for row in samples)
    variances = "".join(
        "<tr><th scope='row'>" + escape(row["beneficiary_id"]) + "</th><td>"
        + amount(row, "closing_calculated") + "</td><td>"
        + amount(row, "customer_closing_statement") + "</td><td class='variance'>"
        + amount(row, "statement_variance", signed=True) + "</td></tr>"
        for row in samples)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BuilderSplit Close · 合成关账样例</title>
<style>
@page {{ size: A4 portrait; margin: 12mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; color: #20262e; background: #fff; font: 9.5pt/1.45 "WenQuanYi Zen Hei", sans-serif; }}
main {{ max-width: 186mm; margin: 0 auto; }}
.banner {{ color: #b00020; border: 1.5px solid #b00020; padding: 6px; text-align: center; font-size: 9pt; font-weight: bold; }}
h1 {{ font-size: 20pt; margin: 12px 0 0; }}
h2 {{ font-size: 11pt; margin: 13px 0 5px; }}
p {{ margin: 5px 0; }}
.subtitle {{ color: #485462; margin-bottom: 10px; }}
.meta {{ padding: 8px 10px; background: #f3f5f7; border-left: 3px solid #485462; }}
.label {{ font-weight: bold; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8.5pt; table-layout: fixed; }}
th, td {{ padding: 6px 4px; border-bottom: 1px solid #ccd1d7; text-align: right; overflow-wrap: anywhere; font-variant-numeric: tabular-nums; }}
thead th {{ background: #edf0f4; }}
th:first-child {{ text-align: left; width: 29%; font-weight: normal; }}
thead th:first-child {{ font-weight: bold; }}
.variance {{ font-weight: bold; }}
.note {{ font-size: 8.3pt; color: #424d59; }}
.hash {{ font-size: 7.8pt; overflow-wrap: anywhere; }}
.identity {{ border-top: 1px solid #ccd1d7; padding-top: 6px; }}
footer {{ margin-top: 12px; }}
section, tr, footer {{ break-inside: avoid; }}
@media screen {{ body {{ padding: 18px; background: #e8ebef; }} main {{ background: white; padding: 12mm; box-sizing: content-box; }} }}
@media print {{ body {{ print-color-adjust: exact; -webkit-print-color-adjust: exact; }} }}
</style>
</head>
<body><main>
<header>
<div class="banner">{BANNER}</div>
<h1>BuilderSplit Close <span style="font-size:13pt">合成关账样例</span></h1>
<p class="subtitle">Offline close report · 七日 UTC 诊断 · 非付款指令 / Not a payment instruction</p>
</header>
<section class="meta" aria-label="Synthetic scope">
<p><span class="label">虚构 Builder：</span>{escape(scope['builder'])}</p>
<p><span class="label">周期 [start,end)：</span>[{escape(scope['period_start'])}, {escape(scope['period_end'])})</p>
<p><span class="label">规模：</span>{report['counts']['input_fills']} fills / {len(report['calculations'])} payees；上限 50,000 / 100；单一冻结规则集</p>
<p><span class="label">单位：</span>USDC（{escape(scope['fee_currency_id'])}，仅合成记账单位）</p>
<p><span class="label">状态：</span>DIAGNOSTIC_ONLY · 非 REVIEW_READY · commercial_g0_passed=false</p>
</section>
<section>
<h2>1 · 关账展示 / Close view</h2>
<p class="note">差异样本 {len(samples)} 行 / 全部 {len(report['calculations'])} payees；以下两表使用同一组非零差异样本，不代表完整账本。</p>
<table aria-label="Synthetic close balances">
<thead><tr><th>合成收款方</th><th>应计</th><th>已付</th><th>期初</th><th>期末</th><th>结转*</th></tr></thead>
<tbody>{balances}</tbody>
</table>
<p class="note">期末 = 期初 + 应计 − 已付。已付仅为引擎计入本关账组的合成外部付款分配额（external_paid），不是现实付款确认。</p>
<p class="note">*结转：仅重复展示带符号期末，表示“若沿用至下期，则为下期期初”；不是引擎独立字段、已完成结转或应付净额。负数不截零、不跨收款方抵销；负期末仅作合成贷方余额 / 超付示例，不断言现实原因。</p>
</section>
<section>
<h2>2 · 差异样本 / Variance samples</h2>
<table aria-label="Synthetic statement variances">
<thead><tr><th>合成收款方</th><th>计算期末</th><th>合成独立期末陈述</th><th>差异（计算 − 陈述）</th></tr></thead>
<tbody>{variances}</tbody>
</table>
<p class="note">陈述值来自合成输入的 closing_statement；不是客户核验。正差异表示计算期末高于陈述，负差异表示低于陈述；均不表示应收、欠付或付款建议。</p>
</section>
<section class="identity">
<h2>3 · 输入与冻结规则 / Input &amp; frozen rule identity</h2>
<p class="hash"><span class="label">输入哈希占位：</span>[INPUT_SHA256] · 合成输入实际 SHA-256：<br>{escape(report['input_sha256'])}</p>
<p class="hash"><span class="label">规则版本占位：</span>[RULE_VERSION]（未分配；引擎不提供命名版本）<br>合成冻结规则实际身份 rule_set_hash：{escape(report['rule_set_hash'])}</p>
<p class="note">引擎版本 {escape(report['engine_version'])}；舍入 {escape(scope['rounding']['stage'])} / scale {scope['rounding']['scale']} / {escape(scope['rounding']['mode'])}。金额逐字取自引擎 Decimal 字符串，无浮点或显示舍入。</p>
<p class="note">来源：report.json + reconciliation.csv；生成器仅比对两者内容，不替代引擎 replay 校验。哈希不是签名、真实来源证明或客户确认。样例不证明真实数据覆盖、原生分账支持或生产可用性。</p>
</section>
<footer><div class="banner">{BANNER}</div></footer>
</main></body></html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Engine output directory containing report.json and reconciliation.csv")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("close-report-sample.html"))
    args = parser.parse_args()
    try:
        report, samples = load_bundle(args.bundle)
        args.output.write_text(render(report, samples), encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        parser.exit(2, "ERROR: " + str(exc) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
