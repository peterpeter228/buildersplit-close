# BS-SAMPLE-01 / BS-SAMPLE-02 — A–E 准备清单 / Preparation checklists

仅为模板：未收到许可或记录，不表示已签署或达成协议。空状态不代表通过。
Template only: no permission received, no records supplied, no signature or agreement implied. An empty status is not a pass.

## 来源与共用定义 / Provenance and shared definitions

P3 前置检索已覆盖 `docs/` 及工作树：未发现既有 BS-SAMPLE 或 A–E 定义。本文件按 P3 授权从许可说明定义共用 A–E，并保留 [规范清单](../docs/CUSTOMER_SAMPLE_CHECKLIST.md) 第 1–9 项及安全收集规则的含义；不是替代或降低该清单。两个样本使用完全相同的 A–E 定义。
The P3 prerequisite search covered `docs/` and the worktree and found no existing BS-SAMPLE or A–E definitions. As authorized for P3, these shared A–E definitions derive from the permission pack and preserve requirements 1–9 and safe collection in the [canonical checklist](../docs/CUSTOMER_SAMPLE_CHECKLIST.md); they do not replace or relax it. Both samples use exactly the same definitions.

### A — 许可、用途、撤回 / Permission, purpose, revocation

规范第 1 项及安全收集：使用前取得数据所有者明确书面许可，限定本地对账用途、最少文件、本地位置、访问角色和保留期限 `[ ]`。确认地址或交易记录是否允许离开其机器；本方案优先全程本地，未经明确许可不得外传。可随时经约定联系人角色及渠道 `[ ]` 撤回；立即停止处理，依 D 删除。模板不构成授权。
Canonical item 1 and safe collection: obtain explicit written owner permission before use for local reconciliation, minimum files, local location, access roles and retention `[ ]`. Confirm whether addresses or transaction records may leave the owner's machine; prefer entirely local handling and never transfer without explicit permission. Revoke at any time through agreed contact role/channel `[ ]`; stop immediately and delete under D. Templates do not authorize use.

### B — 最小范围、来源、完整性 / Minimum scope, source, completeness

规范第 2–4 项：一个 Builder、一个已结束的 UTC 七天区间（含起点、不含终点），注明网络、批准的市场及费用币种；最多 50,000 笔成交、100 位受益人。从有代表性的小型独立手算样本开始，并披露其不完整、仅供诊断的范围。保留原始导出字段结构及来源版本、稳定成交标识及其唯一性范围、毫秒时间、费用归属证据、费用币种及总额与实留金额的已验证定义。公开的 14 列 Builder CSV 不足；不得按时间、价格、数量拼接身份不明的成交。完整性证据包括查询范围、分页终点或数据截止标记、核对总数及其计算依据；声明或文件哈希本身不能证明完整。
Canonical items 2–4: one Builder, one completed UTC seven-day interval (start inclusive, end exclusive), documented network and approved markets/fee assets; at most 50,000 fills and 100 beneficiaries. Start with a representative small independently hand-checked subset and disclose its incomplete, diagnostic-only scope. Preserve original export structure and source/version, stable fill identity and uniqueness scope, millisecond timestamps, Builder attribution evidence, fee asset and verified gross-versus-kept definitions. Public 14-column Builder CSV alone is insufficient; never join unidentified fills by time/price/size. Completeness evidence includes query range, final pagination or cutoff marker, control totals and their derivation; assertion or file hash alone is not proof.

### C — 匿名标签、规则、余额、已付映射 / Pseudonyms, rules, balances, paid mapping

规范第 5–7 项：用一致标签替换身份，保持关系及按生效日期的费用归属；身份对照表只留所有者侧。冻结规则版本：费用基数、受益人标签、费率、舍入环节/精度/方式及确认。提供明确带正负号的期初余额和相同 UTC 截点的独立期末账目，包括明确零值、来源版本及所有者确认；计算输出的复制件不是独立账目。外部已付证据须确认唯一转账事件标识、金额/币种、受益人、发生时间及应付款项/分组映射，并附分配快照及其他活跃分组占用（即使为零）。不得提供钱包秘密或签名能力。
Canonical items 5–7: replace identifiers with consistent labels preserving relationships and effective-dated attribution; keep the identity key owner-side. Freeze the rule version: fee basis, beneficiary pseudonyms, rate, rounding stage/scale/mode and confirmation. Supply explicit signed opening balances and an independent period-end statement at identical UTC cutoffs, including explicit zeros, source/version and owner confirmation; copied calculated output is not independent. Confirm external already-made payment evidence with unique transfer-event identity, amount/asset, beneficiary, occurrence time and obligation/group mapping, plus an allocation snapshot including other active groups' usage, even if zero. Never provide wallet secrets or signing capability.

### D — 本地处理、保留、删除 / Local handling, retention, deletion

规范第 1 项及安全收集：优先全部留在所有者机器；只在获准的私有本地位置处理，真实记录不得进入本仓库、公开位置或外部模型提示。移除个人联系方式及无关交易；在获准私有位置保留文件哈希及来源证据，原始文件及身份对照表与演示文件分开。保留期限 `[ ]`；到期或撤回时，按本地删除步骤及路径 `[ ]` 移除保留的输入、衍生报告及所有副本。真实记录不得改称合成数据。
Canonical item 1 and safe collection: prefer everything staying on the owner's machine; use only an approved private local location, never this repository, public locations or external model prompts for real records. Remove personal contact data and irrelevant transactions; retain hashes and source evidence in the authorized private workspace, with originals and identity key separate from demo files. Retention `[ ]`; at expiry or revocation, remove retained inputs, derived reports and all copies through local deletion procedure/path `[ ]`. Never relabel real records as synthetic.

### E — 独立性、样本资格、独立答案 / Independence, sample eligibility, independent answers

规范第 8–9 项及 P3 样本约束：两个样本来自互不相关的不同组织，无共享数据。**BS-SAMPLE-01** 优先确实无原生分账（协议自动分费）的范围，来源须证明，不得删去实际原生行来制造资格。原生分账仍不受支持，直至具备匹配真实入账、费用含义、舍入及余数校准。**BS-SAMPLE-02** 必须有 C 所述“已付映射”：连接已经发生的付款、受益人及应付款项/分组的证据，不是映射费、付款请求或新付款。两者均须有所有者或独立审阅者手算的子集答案、预期差异和已知缺项。商业访谈、付款及复用仍是单独证据；合成通过不证明真实账目或需求。未获许可或完整性不足，真实验证保持未完成，不扩大生产接入或功能；本清单不授权凭证、系统接入、外联、上传、实际付款或签名。
Canonical items 8–9 and P3 sample constraints: two unrelated, different organisations with no shared data. **BS-SAMPLE-01** prefers a genuinely no-native-split scope (no protocol-automated fee distribution), substantiated by the source; never remove actual native rows to manufacture eligibility. Native splits remain unsupported until matched real credits, fee semantics, rounding and residual calibration exist. **BS-SAMPLE-02** requires C's “paid mapping”: evidence connecting payments already made to beneficiaries and obligations/groups, not a mapping fee, payment request or new payment. Both need owner/independent reviewer hand-calculated subset results, expected differences and known omissions. Commercial interviews, payments and repeat use remain separate evidence; a synthetic pass proves neither real books nor demand. Without permission or completeness, real validation remains incomplete and production-adapter/feature expansion stops; this checklist authorizes no credentials, system connections, outreach, uploads, actual payments or signatures.

## BS-SAMPLE-01

| Item | Shared requirement / 共用要求 | Status / 状态 |
| --- | --- | --- |
| A | 许可、用途、撤回 / Permission, purpose, revocation | |
| B | 最小范围、来源、完整性 / Minimum scope, source, completeness | |
| C | 匿名标签、规则、余额、已付映射 / Pseudonyms, rules, balances, paid mapping | |
| D | 本地处理、保留、删除 / Local handling, retention, deletion | |
| E | 独立性、样本资格、独立答案 / Independence, sample eligibility, independent answers | |

## BS-SAMPLE-02

| Item | Shared requirement / 共用要求 | Status / 状态 |
| --- | --- | --- |
| A | 许可、用途、撤回 / Permission, purpose, revocation | |
| B | 最小范围、来源、完整性 / Minimum scope, source, completeness | |
| C | 匿名标签、规则、余额、已付映射 / Pseudonyms, rules, balances, paid mapping | |
| D | 本地处理、保留、删除 / Local handling, retention, deletion | |
| E | 独立性、样本资格、独立答案 / Independence, sample eligibility, independent answers | |
