# P7 frozen public source provenance

All files below are under `raw/`, fetched by unauthenticated HTTP GET, status **200**. Times are Asia/Shanghai fetch-completion file mtimes captured immediately after curl; date is **2026-11-08**, offset **+08:00**. Raw files total under 5 MB and are retained, not replaced by this manifest.

| Raw file | Exact URL | Completed time | SHA-256 |
|---|---|---|---|
|20261101.csv.lz4|https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/20261101.csv.lz4|17:22:00.288493|0d54b63e4a10930269fe479fe326f4d3cdc5ff8489ae15a4b1707490c4f2f7fa|
|20261102.csv.lz4|https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/20261102.csv.lz4|17:22:00.797486|0f75cbb6ad2f045f1a99535ca1ea622c1875503cce39b90f1eccaf8e0d9937ef|
|20261103.csv.lz4|https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/20261103.csv.lz4|17:22:01.361477|ec7f9232e124b74efe1199217d91a73c35be9d3047b655873c28c4d900bf6529|
|20261104.csv.lz4|https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/20261104.csv.lz4|17:22:02.032466|750ad48a77e24782d5c0bb1daf2611f78b642ca7804bfffcc1219c6a08dcdaea|
|20261105.csv.lz4|https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/20261105.csv.lz4|17:22:02.454460|cac6d866323b57b4e80899bf18daca47fccc24fd970bb47a30b0c1eaa91f2f2b|
|20261106.csv.lz4|https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/20261106.csv.lz4|17:22:03.084450|a30b750dcb08aa14cf41b98b9d4bc9a9e180ec36b1835a9b6f2d491ea051835d|
|20261107.csv.lz4|https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x49ae63056b3a0be0b166813ee687309ab653c07c/20261107.csv.lz4|17:22:03.247447|15f64f0e70f206e8618215243e64dc6849b8407cfc0bbd46d963cabe5db8da21|
|defillama-dextrabot.ts|https://raw.githubusercontent.com/DefiLlama/dimension-adapters/master/dexs/dextrabot.ts|17:22:22.577148|fc5cac5cb2cbb20fbdfdf956bcec03def736a06ccf352cf1ee162a4ac95a77a0|
|ocb-builders.json|https://raw.githubusercontent.com/ChainBench/OpenChainBench/main/harnesses/hyperliquid-frontends/builders.json|17:22:22.581148|610765d8f3fa60f806fedd3fb1f4c7410b31768acb9667ed03cdc2700ae28c7a|
|ocb-method.html|https://openchainbench.com/benchmarks/hyperliquid-frontends|17:22:22.657147|fb03f308c4eb4c3acaa0dbeb382018e570c1dc59b03cee1d381f656784eb30ac|

Additional discovery paths tried, not used as frozen attribution evidence:
- https://github.com/DefiLlama/dimension-adapters/blob/master/dexs/dextrabot.ts — reader resolved to raw URL above.
- https://raw.githubusercontent.com/DefiLlama/dimension-adapters/master/helpers/hyperliquid.ts — documented builder_fills URL pattern and `builder_fee` column; no local copy used in calculation.
- https://docs.dextrabot.com/dextrabot/fees — reader selected https://docs.dextrabot.com/dextrabot/fees.md; no builder address shown. No pricing content used.
- https://app.coinmarketman.com/hypertracker/builder/0x49ae63056b3a0be0b166813ee687309ab653c07c — search title named Dextrabot; static extraction returned shell; Chrome timed out after 60 seconds.

Search discovery terms: `Dextrabot builder address Hyperliquid OpenChainBench`; exact-address search (irrelevant results); `Dextrabot Hyperliquid builder address hypertracker`. Search snippets are not raw fills or a calculation source.
