# 本地对账许可说明 / Local reconciliation permission pack

**仅为提案和模板：未收到许可或记录，不表示已签署或达成协议。**
**Proposal and template only: no permission received, no records supplied, no signature or agreement implied.**

## 我们想要什么 / What we want

- 仅在许可后，用最少的只读记录做本地对账：比较记录的费用、应付金额和已经支付的金额。范围为一个费用归属方（Builder）、一个已结束的世界标准时间（UTC）七天周期；最多 50,000 笔成交、100 位收款方。先用有独立手算答案的小样本，并说明它不代表完整账目。
  Only after permission, use the minimum read-only records for local reconciliation: compare recorded fees, amounts owed and amounts already paid. Scope: one fee-earning business (Builder), one completed seven-day period in Coordinated Universal Time (UTC), at most 50,000 trades and 100 payees. Start with a small subset checked independently by hand; it does not represent complete books.
- **BS-SAMPLE-01**：优先选择确实没有原生分账（协议自动分配费用）的范围，须有来源证据；不得删除实际原生记录来满足条件。原生分账在获得真实入账匹配及费用、舍入和余数校验前仍不受支持。
  **BS-SAMPLE-01:** prefer a scope genuinely without native splits (fees automatically distributed by the protocol), supported by source evidence. Never remove actual native rows to make it eligible. Native splits remain unsupported until matched real credits and checks of fee meaning, rounding and remainders exist.
- **BS-SAMPLE-02**：需要“已付映射”，即证明**已经发生的付款**分别属于哪些收款方和应付款项或分组，且说明同笔付款被其他分组使用的份额。这不是映射服务收费、付款请求或新付款。
  **BS-SAMPLE-02:** needs a “paid mapping”: evidence linking **payments already made** to payees and obligations or groups, including any share used by other groups. This is not a mapping fee, payment request or new payment.
- 两个样本必须来自互不相关的不同组织，不共享数据。来源、完整性、规则、期初余额和独立期末核对要求见 [A–E 清单](bs-sample-checklists.md)。
  The two samples must come from unrelated, different organisations, with no shared data. See the [A–E checklists](bs-sample-checklists.md) for source, completeness, rules, opening balances and independent closing checks.

## 我们不要什么 / What we don't want

- 不要密钥、签名权限、资金操作、个人联系方式、无关交易或全量广泛账本；不要上传真实记录至本仓库、公开位置或外部模型。此提案不授权收集数据、接入系统或付款。
  No keys, signing access, money movement, personal contact data, unrelated transactions or broad ledgers. No real records in this repository, public locations or external models. This proposal authorizes no data collection, system connection or payment.

## 数据如何处理 / How data is handled

- 优先让全部数据留在对方机器上，由其控制。把账户和收款方标识换成前后一致的标签，保持记录间关系；标签与真实身份的对照表只由数据所有者保管。先确定最少文件、用途及本地位置；原始文件与身份对照表和演示文件分开。
  Prefer all data staying on their machine, under their control. Replace account and payee identifiers with consistent labels while preserving relationships; the identity key stays owner-side. First agree the minimum files, purpose and local location; keep originals and the identity key separate from demo files.
- 保留期限 **[ ]**；本地删除步骤及路径 **[ ]**，覆盖输入、衍生报告和所有保留副本。所有者可随时经双方约定的联系渠道 **[ ]** 撤回许可；随即停止处理，并按该步骤删除上述材料。使用前另行明确许可；本页不是生效授权。
  Retention **[ ]**; local deletion procedure and path **[ ]**, covering inputs, derived reports and all retained copies. The owner may revoke at any time through the agreed contact/channel **[ ]**; stop processing and remove those materials using that procedure. Obtain explicit permission separately before use; this page is not an authorization in force.
