# P4 verification — public contacts

Check date: **2026-11-08, Asia/Shanghai (+08:00)**. Scope: public contact discovery only; no messages, login, paid database, deployment, charge, broadcast, engine changes, P5/P6 work, main mutation or PR #1 mutation.

## Evidence standard

- Two different URLs alone do not establish independence. Each firm must pair its own published page with an independently operated publisher. Website + vendor docs + vendor X/TG are one publisher, not three.
- OpenChainBench (OCB) independently publishes the builder directory/fee benchmark. Its product page and GitHub registry are the same publisher and never counted as two. OCB describes a curated registry seeded from DefiLlama/HyperTracker; its external links may originate with vendors. This corroborates public identity/channel attribution, not independent auditing of vendor claims or legal control of a wallet.
- A public link is not proof that DMs are open, an inbox works, a person will respond, or a founder owns fee reconciliation. No delivery/reachability tests were made.
- `未找到` means not verified in the listed paths, not proof of nonexistence. Search snippets, login/error pages and similarly named products do not qualify as fetched supporting evidence.
- HTTP status is reported only when observed. Parent `curl` downloads below were unauthenticated GETs; times are saved-response mtimes captured immediately afterward, rounded down to whole seconds. Reader-only checks are labeled as reader results, not invented HTTP 200s.

## Dextrabot official footer recheck

**PASS.** Source: <https://dextrabot.com/>; HTTP **200**; fetched **2026-11-08 21:23:03 +08:00 (Asia/Shanghai)**. Parent inspected the downloaded response `/tmp/omp-jobs/buildersplit-g1-pack-20261108-p4/dextrabot.html`: `<footer>` opens at line 828, closes at 934; X anchor is inside it at 859–864 and TG anchor at 910–915. This is actual HTML footer evidence, not merely metadata, a search snippet, or an unexecuted JavaScript string.

Exact anchor attributes (SVG contents omitted):

```html
<a href="https://x.com/dextrabot" target="_blank"
   class="text-[#696969] hover:text-white transition-colors" aria-label="X">
<a href="https://t.me/Dextrabot_Official" target="_blank"
   class="text-[#696969] hover:text-white transition-colors" aria-label="Telegram">
```

The footer uses an X icon, not visible text spelling `@dextrabot`; the destination URL identifies the handle. Independent OCB product attribution also links `https://x.com/dextrabot`. No X login or outbound interaction was needed.

## Independent builder-list checks

All of these were HTTP **200**, fetched on **2026-11-08 (Asia/Shanghai)**. Each product page was also read for its organization/domain/social crosslinks. Figures were not used to infer a fee owner or a need for reconciliation.

| Firm | Independent URL | Fetch time +08:00 | Observed attribution |
|---|---|---|---|
| Legend | https://openchainbench.com/products/legend-trade | 21:22:33 | Legend Trade; `www.legend.trade`; X `legendtrade`. |
| Dextrabot | https://openchainbench.com/products/dextrabot | 21:22:34 | Dextrabot; `dextrabot.com`; X `dextrabot`. |
| pvp | https://openchainbench.com/products/pvp-trade | 21:22:34 | pvp.trade; `pvp.trade`; X `pvptrade` — differs from starting `pvp_dot_trade`; not silently reconciled. |
| Owly | https://openchainbench.com/products/owlyfi | 21:22:34 | Owly.fi; `owly.fi`; X `owlyfi`. |
| Invo | https://openchainbench.com/products/invo | 21:22:34 | Invo; `invoapp.com`; X `invoapp`; described as Hyperliquid social/copy-trading app. |

The selection universe was checked at <https://openchainbench.com/benchmarks/hyperliquid-frontends>, HTTP **200**, **2026-11-08 21:19:37 +08:00**: the page states **106** ranked providers and includes all five firms. This page and the product pages are not independent of each other.

## Per-row two-source audit

All timestamps below are **2026-11-08, Asia/Shanghai (+08:00)**. All ten principal URLs were fetched with parent `curl` (HTTP **200**) and their content inspected. These are the exact two principal URLs in each contacts-table row, not merely two arbitrary links.

| Firm | Source A / fetch time | Source B / fetch time | Distinct sources / independence / supported scope |
|---|---|---|---|
| Legend | https://www.legend.trade/help/contact-support — **200**, **21:25:59** | https://openchainbench.com/products/legend-trade — **200**, **21:22:33** | **PASS: 2 distinct URLs, 2 publishers.** Official page: `Email: support@legend.trade`. OCB identifies Legend Trade, official domain and X `legendtrade`; it does not separately verify email delivery or identify a fee owner. |
| Dextrabot | https://dextrabot.com/ — **200**, **21:23:03** | https://openchainbench.com/products/dextrabot — **200**, **21:22:34** | **PASS: 2 distinct URLs, 2 publishers.** Actual official footer links X `dextrabot` and TG `Dextrabot_Official`; OCB links the same website and X. TG is vendor-published, not independently confirmed by OCB. |
| pvp | https://pvp.trade/ — **200**, **21:25:59** | https://api.llama.fi/protocol/pvp.trade — **200**, **21:25:59** | **PASS: 2 distinct URLs, 2 publishers.** Official site links `https://twitter.com/pvp_dot_trade` and `https://t.me/pvptrade_bot`. DefiLlama JSON gives `name: pvp.trade`, `url: https://pvp.trade/`, `twitter: pvp_dot_trade`. Bot link is vendor-published. |
| Owly | https://owly.fi/docs/faq/community.md — **200**, **21:25:05** | https://openchainbench.com/products/owlyfi — **200**, **21:22:34** | **PASS: 2 distinct URLs, 2 publishers.** Official page links X `owlyfi`, TG `owlyfi_support`, and `support@owly.fi` under Bug Reports. OCB independently associates Owly.fi, its domain/X and the Hyperliquid builder listing. Email and TG support role are vendor-published. |
| Invo | https://www.invoapp.com/guides/fees — **200**, **21:25:05** | https://www.tinytechfund.com/company/involio-inc — **200**, **21:25:07** | **PASS: 2 distinct URLs, 2 publishers.** Official guide byline: `Ryan Pace / CEO, Co Founder`. TinyTech: `co-founder and CEO Ryan Pace`, product Invo and `app.invoapp.com`; its people-on-file section names Ryan as President/CEO/Form D signer. TinyTech uses SEC filings; this is separate publication, not independent auditing of the underlying issuer assertions. Neither source assigns fee reconciliation to him. |

**Five of five rows pass distinct-URL and different-publisher checks.** This does not mean every email or role has two independent eyewitness confirmations. Field-level support and limitations are stated above. No pair consists of a vendor website and its own social account, or OCB's site and its own registry.

## Additional Invo channel proof and identity chain

- <https://play.google.com/store/apps/details?id=com.involio.app&hl=en> — **HTTP 200**, **2026-11-08 21:25:17 +08:00**. Parent read the public app page and downloaded it. Title `Invo: Where Traders Are Made`; developer `Involio Inc`; “About the developer” publishes **`Ryan@involio.com`**. A developer response dated September 12, 2026 says `please reach out to us at support@involio.com`. These are published business addresses, not generated patterns. The developer metadata/reply is first-party content hosted by Google, **not an independent second attestation**. Do not assume Ryan personally reads the developer mailbox.
- <https://www.invoapp.com/privacy-policy> — **HTTP 200**, **2026-11-08 21:25:07 +08:00**. Identifies `Involio, Inc.` and references Hyperliquid. The parent's Markdown reader showed the contact email as `[email protected]`; the parent therefore relies on the explicit Google Play text above for the exact email, not on guessing or that obscured text.
- <https://openchainbench.com/products/invo> — **HTTP 200**, **2026-11-08 21:22:34 +08:00**. Links `invoapp.com` and X `invoapp`; associates the product with the Hyperliquid builder ranking. This resolves the original Invo product identity, independently of the executive byline.
- The research worker also read <https://www.sec.gov/Archives/edgar/data/1938327/000193832726000003/primary_doc.xml> on **2026-11-08, approximately 21:24 +08:00** (reader returned XML). It reports Ryan Pace as an executive officer/director and `President/CEO` signer. This is an issuer-filed record, not SEC certification of current duties; TinyTech and this filing are **not counted as independent origin chains**. No unnecessary home address, phone number or contributor email is copied into the contact deliverable.

## pvp handle disagreement

OCB's product page links `https://x.com/pvptrade`; the official site and independently operated DefiLlama API instead agree on **`pvp_dot_trade`**. Adopt the official + DefiLlama pair. Preserve OCB only for builder-list membership, not the X field. No conclusion is drawn about why the discrepancy exists, whether the other account is related, or whether either account accepts messages.

The worker additionally read <https://t.me/pvptrade_bot> on **2026-11-08, approximately 21:23 +08:00** (public Telegram preview returned content): its bio links `https://x.com/pvp_dot_trade`. No bot was started. This is useful first-party crosslinking, not a new independent publisher.

## 未找到 — names, responsibilities and attempted paths

All paths in this section were checked on **2026-11-08 (Asia/Shanghai)**. Worker time windows are stated as windows, not exact per-request seconds. Public content was returned unless a failure is expressly noted. These are bounded negative searches, not claims that a person or role does not exist.

### Legend — 未找到: directly verified named contact / fee-reconciliation owner

Worker checks **21:19–21:23 +08:00**: <https://www.legend.trade/help/contact-support>, <https://www.legend.trade/terms>, <https://www.legend.trade/privacy>, <https://www.legend.trade/affiliates>, <https://www.legend.trade/careers>, <https://docs.legend.trade/>. The affiliates page mentions operator approval without naming that operator. Open role listings do not establish who currently owns finance.

Public team searches and <https://www.gate.com/en-eu/price/market-data/institutions/fundraising/legend.trade-17463> (worker reader returned content, approximately **21:20 +08:00**) produced pseudonymous team/founder labels, not a two-source named fee-owner match. Snippet-only LinkedIn/X names were not promoted to verified contacts. Distinctly branded Legend Trading and legend.xyz were excluded.

### Dextrabot — 未找到: directly verified named contact / fee-reconciliation owner

Worker checks **21:19–21:22 +08:00**: <https://dextrabot.com/>, <https://dextrabot.com/about-us> (SPA shell, not a verified team page), <https://docs.dextrabot.com/llms.txt>, <https://docs.dextrabot.com/dextrabot/fees.md>, <https://docs.dextrabot.com/faq-and-official-links/official-links.md>, <https://docs.dextrabot.com/faq-and-official-links/terms-of-use.md>. Fees and legal notice routes do not name a reconciliation owner. The terms' legal-only inbox is not repurposed for business outreach.

Additional attempts: <https://blog.dextrabot.com/> — worker reader **403**, approximately **21:19:35 +08:00**; <https://x.com/dextrabot> — worker `x-unavailable`, approximately **21:21:10 +08:00**, not fetched profile proof. NFTinit founder/team associations do not demonstrate a direct Dextrabot fee-owner role, so no parent-team person's name or guessed personal mailbox is inserted.

### pvp — 未找到: direct named team member / dedicated email / fee-reconciliation owner

Worker checks **21:19–21:23 +08:00**: <https://pvp.trade/>, <https://docs.pvp.trade/llms.txt>, <https://docs.pvp.trade/en-quickstart.md>, <https://docs.pvp.trade/en-commands.md>, <https://docs.pvp.trade/en-fee-tiers.md>, <https://docs.pvp.trade/en-referrals.md>. The commands page describes contact support through `/settings`; this was only read, not executed. Fee/referral documentation gives no named operator. No `@pvp.trade` email is inferred.

Worker also checked <https://docs.hyperdash.com/about-hyperdash.md> and <https://docs.hyperdash.com/get-help.md> (**21:20–21:21 +08:00**, reader returned content). Parent fetched both HTTP **200** at **21:20:21 +08:00**. Hyperdash channels/people are not automatically pvp's direct fee-owner contacts; none is substituted into the row.

### Owly — 未找到: directly verified named contact / fee-reconciliation owner; public entry FOUND

Worker checks **21:20–21:22 +08:00**: <https://owly.fi/>, <https://owly.fi/docs/legal/terms-of-service.md>, <https://owly.fi/docs/faq/fees.md>, <https://owly.fi/docs/faq/community.md>, <https://owly.fi/docs/guide/b2b-api.md>, <https://owly.fi/docs/guide/referral.md>, <https://github.com/owlyfi>. These establish the product/support paths, not a named finance operator. Repository authors are not promoted to executives or fee owners; personal contributor emails are deliberately excluded.

Public search paths included `"owly.fi" "founder"`, `"owlyfi" "team"`, and the legal-entity name from the terms. Unrelated AI/video, CRM and customer-support products named Owly were rejected rather than used as alternate identities.

### Invo — 未找到: specific fee-reconciliation owner; public entry and general CEO role FOUND

Worker checks **21:19–21:24 +08:00**: <https://www.invoapp.com/>, <https://www.invoapp.com/privacy-policy>, <https://www.invoapp.com/terms-condition>, <https://www.invoapp.com/support>, <https://www.invoapp.com/guides/fees>, <https://www.invoapp.com/guides/referral-earnings>, <https://www.invoapp.com/guides/monetize-your-edge>, the public Google Play listing, TinyTech and SEC record above. Search terms included `"Involio" CEO CFO finance operations` and `"invoapp.com" founder Hyperliquid`. None designates a specific reconciliation owner. A CEO byline on a fee article is not such a designation.

## Conditional replacement decision

**No replacement required: 0 selected.** Both Owly and Invo now have verified public organization entries, paired with independent product/company sources. Missing named fee owners do not meet the stated “no verifiable public entry” replacement trigger. Original five firms remain in the table. The 106-provider OCB list was checked directly; no extra firm is presented as a replacement without a triggered need.

## Acceptance boundary

- Five requested firms, one row each; exact five requested column names; two principal URLs per row.
- All ten principal fetches succeeded; exact status/date/time and publisher distinction recorded above. Supplemental Invo channel evidence is explicit and not counted as independent merely because it is hosted by Google.
- Dextrabot footer and pvp conflicting directory handle resolved from observed official content.
- No invented name, email pattern or fee-owner assignment. All five fee-owner gaps and four direct-name gaps remain **未找到**, with paths tried.
- **PARTIAL** is the handoff status for those named-contact/role gaps, not a claim that two-source organization research or the conditional replacement check remains unperformed. No owner decision is needed to record the authorized missing-information fallback. No outbound contact is authorized by this result.

## Artifact check actually exercised

The temporary Python acceptance checker exited **0** after reading both final Markdown artifacts: **5 firms**, exact five-column header, exactly two distinct principal URLs per row, all principal URLs present in this verification file, check dates, valid H/M/L values, and required missing/footer/replacement markers. Parent manually checked the source excerpts, publisher relationships, field-level limitations and missing-role statements; a hostname comparison alone was not treated as proof of independence. No code tests were applicable to this research-only package. The live unauthenticated source fetches and actual downloaded footer inspection above are the exercised research path.
