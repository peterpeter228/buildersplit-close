# First implementation milestone

Source: [research PR #3](https://github.com/peterpeter228/blockchain-opportunity-radar/pull/3), fixed research commit `2e8d6d9eec44fca8f4abed94534dc85e6ebec3f5`, directory `research/web3-top3-20261106/`, especially 07–13 and 18–19. Notion project: https://app.notion.com/p/41001c9117228164a1d9df4a131ec98e . Linear validation task: HAP-30.

Latest user request authorizes creating a private repository and starting development. It does not establish customer demand or replace the research's commercial stages. This implementation is a bounded <$0 new-services, ≤8-hour local technical experiment. Existing Stonk work and other automation claims are not changed.

## User job and hypothesis

A Builder operator may need to reconcile confirmed source fills, fee rules, signed opening balances, external payments and an independent period-end statement for one closed week. A real buyer's willingness to pay remains unvalidated. This experiment tests rejection and arithmetic, not that market hypothesis.

## Scope

One synthetic normalized bundle, one mainnet HyperCore Builder, one seven-day UTC half-open interval, explicit validator-operated perp whitelist, one USDC accounting identity, ≤50K fills and ≤100 beneficiaries. The example's mainnet label describes its schema only; it contains no observed mainnet activity.

Rules allocate one beneficiary per account/time interval in this milestone. Native credits and all unsupported adjustments are blocked. Balances and statement evidence are mandatory; zero is explicit. Payment receipt identity, scope, confirmation and available allocation are mandatory. Out-of-period fills are counted and not billed. Out-of-period payments block, requiring explicit correction of scope rather than silent deduction.

## Acceptance

Synthetic independent arithmetic, signed overpayment, Decimal precision, per-fill vs per-period rounding, identity conflict, rule gap/overlap, interval boundaries, unsafe CSV text and invalid inputs are tested. All unknowns prevent calculation export. Maximum successful state is DIAGNOSTIC_ONLY. A technical pass does not satisfy the full 39-case production matrix.

## Next and stop

Obtain an authorized real input contract/sample and independent source control totals before validating a real adapter. Prepare buyer interviews and a fixed-scope offer, but do not send externally without authorization. Stop feature expansion when only buyer/source evidence remains; no multi-tenant UI or subscription platform in this milestone. G0 remains partial; G1–G4 not passed.
