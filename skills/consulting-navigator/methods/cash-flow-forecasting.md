# Cash Flow Forecasting
## Purpose
Project timed cash inflows and outflows so liquidity gaps, surplus, and funding needs are visible before they hit. It follows the dates cash moves, which may differ substantially from revenue recognition or expense accrual.
## Use
- You must estimate near- or medium-term cash inflows and outflows to manage liquidity
- Covenant headroom, funding draws, or dividend capacity depend on cash timing
- Working-capital swings or growth are distorting the P&L picture of cash
## Avoid
- The question is structural balance-sheet efficiency rather than a timed forecast—use working-capital-management
- You need daily treasury positioning and bank-account control—use treasury-management-framework or liquidity-management
- You are valuing a firm or project from free cash flows—use discounted-cash-flow-valuation
## Inputs
**Must-have:**

- Historical cash receipts and disbursements by major category
- AR/AP aging, inventory plans, and known one-time cash events
- Revenue and cost outlook with payment-term assumptions
- Debt service, capex, tax, and financing schedules

**Nice-to-have:** customer-level collections history, purchase-order schedule, covenant definitions, committed facility availability, and seasonality analysis.

**When data is thin:** start with a 13-week direct cash forecast, isolate the largest receipts and payments, and show a downside collection-timing case.
## Procedure
1. **Set horizon and opening position.** Select weekly, daily, or monthly buckets based on the decision; reconcile opening cash, restricted cash, and available credit to the latest bank and debt records. Output: starting liquidity position.
2. **Forecast cash collections.** Convert invoiced receivables, expected sales, and other receipts into receipt dates using aging, contractual terms, collection behavior, disputes, and concentration risk. Output: collections schedule by period.
3. **Forecast cash payments.** Time payroll, suppliers, inventory, tax, rent, capex, debt service, interest, and one-off obligations from payment terms and committed dates. Output: disbursements schedule by period.
4. **Roll the cash balance.** Add collections and financing inflows, subtract payments and financing outflows, then calculate ending cash, facility draw, and covenant headroom for every period. Output: base liquidity forecast.
5. **Challenge and operate the forecast.** Run collection-delay, sales, cost, and payment-timing cases; compare prior forecast with actual cash and update the drivers responsible for variance. Output: scenarios, actions, and weekly refresh process.
## Output Contract
Provide a time-phased receipts-and-payments model with opening and closing cash, financing movements, minimum liquidity, covenant headroom, major drivers, and downside scenarios. It identifies the first date a funding action is required, its amount, and the trigger for escalating it; it is not a free-cash-flow valuation.
## Evidence
Bank balances, AR and AP aging, payroll calendars, signed debt schedules, and committed payments are observed inputs. Treat expected collections, sales conversion, supplier flexibility, and refinancing as assumptions. Maintain a separately labeled base, downside, and management-action case. Never offset a late customer receipt with a vague “other income” line or use accrual revenue as cash without a collection curve.
## Checks
- Opening cash and credit availability reconcile to current records.
- Every major P&L driver has a payment or receipt timing rule.
- Debt service, tax, capex, and restricted cash are included on their actual dates.
- The model exposes minimum cash and covenant headroom, not only period-end cash.
- Forecast-versus-actual variance leads to an updated driver assumption.
## Failure Modes
- Spreading a customer receipt evenly across months despite a known payment date.
- Forecasting revenue growth while holding working-capital days flat without justification.
- Omitting tax, annual insurance, or debt amortization because they are not operating expenses.
- Treating unused revolver capacity as cash when a covenant blocks the draw.
- Refreshing totals each month but never learning why collections missed forecast.
