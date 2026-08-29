# Pricing Waterfall Analysis
## Purpose
Diagnose where value leaks between list price and pocket price by mapping each discount, rebate, and giveaway step. It distinguishes a list-price issue from leakage after the quote.
## Use
- List-to-pocket margin erosion must be quantified step by step
- You need to find which discounts, terms, and giveaways destroy realized price
- Pricing governance redesign requires evidence of leakage by customer, segment, or channel
## Avoid
- You still need to set strategic list price from customer value—use value-based-pricing first
- The question is demand response to list price changes—use price-elasticity-analysis
- You lack transaction-level invoice and cost-to-serve data—gather that before modeling
## Inputs
**Must-have:** Transaction-level list, invoice, and net price data; inventory of on- and off-invoice discounts, rebates, freights, and terms; cost-to-serve or pocket-margin components where available; customer, product, and channel dimensions for cut analysis.

**Nice-to-have:** approval logs, contract clauses, claimed-versus-paid rebate records, competitor allowances, and sales-representative identifiers.

**When data is thin:** build a gross-to-net bridge for a representative account set, mark estimated deductions separately, and reconcile every selected invoice to a source document before extrapolating.
## Procedure
1. **Set the price basis and grain.** Select list price, currency, unit, period, and transaction grain. Exclude taxes and pass-throughs consistently. Prevent a rebate or freight charge being counted twice.
2. **Construct the ordered waterfall.** For each transaction, subtract invoice discounts from list, then off-invoice rebates, prompt-payment discounts, freight, free goods, and other allowances in their contractual order. Retain both dollars and percentage-of-list at every rung.
3. **Reconcile and classify deductions.** Tie invoice revenue to finance totals; classify each deduction as standard policy, negotiated term, execution error, or unknown. Investigate unmatched credit memos rather than burying them in “other.”
4. **Cut the leakage.** Compare rungs by customer, product, channel, salesperson, and contract cohort. Rank both absolute leakage and leakage rate, then isolate the small number of combinations driving most pocket-price loss.
5. **Test controllable actions.** Separate unavoidable economics, such as contracted freight, from concessions that can be gated or redesigned. Size the effect of changing an approval threshold, removing a free-good practice, or collecting an expired rebate.
6. **Issue the governance decision.** Name the owner, policy change, account action, and control metric for each material leak. Preserve the bridge as a repeatable monthly view, not a one-off margin explanation.
## Output Contract
A list-to-pocket bridge with dollar and rate deductions at each rung; reconciliation to invoice revenue; leakage cut views; deduction classification; and an action register with owner and expected realization. The result must show where the price disappeared, not merely report an average discount.
## Evidence
Treat invoiced amounts, credit notes, and signed terms as observed. Treat allocation of pooled freight or free-good value as inferred, and show the key. Flag accruals, disputed rebates, and missing contract identifiers as unknowns. If list prices change mid-period, normalize to each transaction’s effective list.
## Checks
- Every waterfall rung has a business definition, data field, and sign convention.
- Transaction totals reconcile to the general ledger within an explicitly stated tolerance.
- A sample of high-leakage transactions traces to contract, invoice, and credit evidence.
- Rankings show both dollars and percentage so large accounts do not hide extreme erosion.
- Proposed controls target a named deduction and decision right.
## Failure Modes
- Starting at invoice price and therefore missing off-invoice rebates and promotional claims.
- Combining freight recovery with freight expense, which confuses realized price with cost-to-serve.
- Treating all discounts as sales discretion when contract terms or claims administration caused the loss.
- Comparing percentage leakage across products with incompatible list-price units.
- Canceling a concession without checking the customer commitment that authorized it.
