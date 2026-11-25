# Estate / Decision Lab

A dependency-free, public-safe decision dashboard. **It contains synthetic scenarios, not a household recommendation or private financial records.** Property A is a future inheritance; B is already owned by the heir and retains its existing leased income in every modeled path.

## Run, check and build

Requires Node 20+; no package install is needed for core checks or the static build.

```sh
npm --prefix decision-lab test
npm --prefix decision-lab run verify
npm --prefix decision-lab run build
python3 -m http.server 4173 --bind 0.0.0.0
# Open /decision-lab/ for source preview or /decision-lab/dist/ for the allowlisted build.
```

Serve over HTTP, not file:// (ES modules). All browser asset URLs are relative for GitHub Pages subpaths. `dist/` is generated/ignored. The build copies only named, public runtime assets and public documentation; it does not copy the repository, tests, source records, COORDINATION.md, environment files, uploads or Git metadata.

**Root integration is a separate coordination claim.** The root deployment workflow's explicit allowlist must copy the built `decision-lab/dist/` to `_site/decision-lab/` and add a root menu link. A directory merged into Git is not proof of a Pages deployment. See issue [#2](https://github.com/kanlerxz87-cyber/TinoDash2/issues/2). Do not restore artifact upload of `.`.

## Navigation / deliverables

- Overview: what would change the answer, ownership distinction and next evidence steps.
- Executive summary and decision questions: known context, blank actual evidence, acquisition plan and responsible professional.
- Compare paths: seven common-date after-tax illustrative paths, three-case ranges, sensitivities, 2040/2045/2050 × 10/20/30/50-year matrix.
- Projections: annual cash, asset/assessment/basis/tax/debt/capital/portfolio/funding audit schedule and 81-point design distribution.
- Black swan lab: immediate investment vs 24/36-month parking, 12/24-month fixed phasing, maturity-matched 3/6/12/24-month Treasury ladder, early-crash and missed-rebound counterexamples.
- Laws/taxes, deadlines, buildings/liquidity, suggestions and a dated official-source ledger/glossary.
- Flagged for Review and privacy limits; unknowns are visible, not silently filled.
- **Attorney & CPA Briefing Sheet**: dedicated one-page Letter print layout. Actual amounts, eligibility, chosen path, decision date and rationale remain blank.

## Model boundaries

This is a decision-preparation illustration, not a tax return, appraisal, investment recommendation, backtest, transaction instruction or filing. No actual household criteria/path/filing/investment policy has been approved. Every numeric input other than a dated public-law constant is a hypothetical sensitivity. Independent evidence belongs in a separate encrypted private matter file, never in this public site/Git or URL/browser storage.

Official links support the stated **rule or methodology**, not a bespoke rent, valuation, property tax rate or insurance quote. Actual fields remain `— Unverified`. See [dated research](docs/RESEARCH.md), [privacy](PRIVACY.md) and the runtime source register for specific sections read.

### Seven consistent paths

1. Live in A, retain B's existing leased income.
2. Rent A, live in B's separate owner space (legality/availability unverified).
3. **Sell in the transfer tax year**, then immediately allocate stock/Treasury contributions.
4. Sell, park 24/36 months, phase the planned stock sleeve over 12/24 months.
5. Rent A five full operating years, sell at the end of year 5.
6. Live in A ten full operating years, sell at the end of year 10; separately test §121.
7. Live in A ten years, then rent it; any Prop 19 benefit ends on departure.

All start at the same transfer date, A value/basis premise, B ownership/cash-flow premise, reserve, economic path and horizon. Mixed sales execute even when the sale year equals the selected horizon. No B rent vanishes merely because the owner lives in B. Optional extra-unit B income starts OFF, needs lease/legal review, and is not a household assumption.

### Calendar, prices and inflation

- 2026 is the real-dollar base. Pre-transfer property prices use a nominal growth sensitivity, assessments a separate capped factor, rents a separate lawful-growth proxy, expenses inflation or insurance escalation.
- After transfer, deterministic uneven housing/stock/inflation/yield sequences replace a single 50-year line. Different scenarios test a 1929-severity shape, 2008-style credit stress, persistent inflation, fast rebound and a later crash.
- Transfer is an annual period boundary. Row 0 is the transfer/same-year sale event; row n ends n full operating years later. Tax-year-0 sale tax uses the entered other-income proxy; it is **not** reconciled with a partial death-year B rental/investment tax return. Later events stack within their full modeled operating year.
- Annual property taxes use that period's starting assessment/market cap; the schedule shows the assessment **used for that period's bill**, which can be nonzero in an end-of-year sale row even when ending A market/basis are zero. Actual lien dates, supplemental proration and Prop 8 restoration need county/CPA reconciliation.
- Real values divide by cumulative scenario inflation since 2026. The investment-only crash chart instead uses **transfer-date purchasing power**, clearly labeled. These are not interchangeable real-dollar bases.

### What wealth means

`realizable nominal = A hypothetical net sale proceeds (if held) + portfolio after exit tax − financed funding deficit`

The headline **excludes common retained B equity**: B is not sold, its actual basis/tax is unknown, and calling its market equity after-tax liquidation wealth would be misleading. B's modeled market, assessment, debt, continuing leased income, cash costs and separately labeled pre-exit-tax retained equity remain visible. Other inherited cash, full estate tax and tax apportionment stay uncomputed without an estate-wide inventory, gifts/DSUE and documents.

Imputed A-vs-B housing service is a **separate non-cash preference metric**, discounted at an explicit 3% nominal proxy. It is never rent received, an investable contribution, a tax deduction or part of the wealth ranking. The public module does not impute a new B rent payment to its existing owner.

### Property costs, debt and liquidity

- Deduct property percentage levies, direct charges, maintenance, occupancy-specific insurance/utilities, management/vacancy, inspected-plan placeholders, debt service and tax before investing annual cash surplus.
- Years 1–5 spend the midpoint of each explicitly synthetic capital work slot × a multiplier. After year 5, recurring annual capital replacement budgets prevent an unsupported 50-year no-replacement assumption. Maintenance is separate current repairs. The model capitalizes work slots conservatively; a CPA must reclassify true deductible repairs. No reserve deposit plus actual-capital-spend double count.
- Mortgage payments amortize monthly with separate interest/principal. Principal reduces debt and cash, **not** rental taxable income. Property sale pays debt from cash proceeds, **not** from taxable gain.
- Surpluses first repay financed deficits, then use the selected stock contribution weight. Deficits consume Treasuries, then sell stock (with incremental modeled gain tax), then accrue an explicitly flagged funding balance at a sensitivity rate. Credit is **not** assured; a funding gap can make a path infeasible despite positive property wealth.
- Contributions occur at annual period-end, an approximation; portfolio returns accrue monthly. No annual portfolio rebalancing, transaction fees or tax-lot/short-term-lot optimization is asserted.

### Income, gain and assessment rules

- A basis defaults to 100% of transfer FMV **only as a sensitivity**, not a trust/legal conclusion; test a lower basis fraction. Add capital improvements, subtract allowed/allowable modeled depreciation. No B reset from A's inheritance.
- Residential rental depreciation: land excluded; 27.5-year GDS approximation, assumed January service (11.5 months first year), then annual capped deductions by vintage. At live-to-rental conversion, initial depreciable building basis uses the lower of adjusted building basis or allocated conversion FMV; income-tax gain basis is kept separately. B has an existing-basis/previous-deduction sensitivity plus rental-share capital vintages. Actual service dates, allocation, remaining life and disposal-year mid-month adjustments require CPA schedules; annual disposal-year depreciation is not exact.
- Flat federal ordinary/gain and California marginal rates are **sensitivities**, not full progressive/bracket stacking. State gains use ordinary-income sensitivity. Unrecaptured §1250 portion is capped at the lower of 25% or the entered federal ordinary rate; remaining eligible gain uses the gain rate.
- Annual threshold ledger aggregates positive rental taxable income, qualified-dividend proxy, realized stock/property gains and Treasury interest. California excludes direct Treasury interest. The 1% Form 540 tax is incremental income above $1m; NIIT is the incremental 3.8% lesser-of-NII/excess-MAGI calculation. Other income is held constant and assumed noninvestment. Deductions, IRD, QBI, AMT, passive-loss release, participation exceptions, trust brackets, capital-loss offsets and cross-property loss benefits are omitted. Losses receive no current/terminal tax benefit. Actual short-term tax lots are not tracked.
- §121 is separate from Prop 19: only lived-in paths with sufficient modeled 2/5-year use, conditional on **all** actual tests. Depreciation-related gain is not excluded. Pure rentals, rent-then-sale and immediate sale never get a residence exclusion. Future nonqualified-use exceptions and special cases require counsel.
- Prop 19 starts OFF, requires both an eligibility and genuine long-term-occupancy switch. Formula: `base + max(0, FMV − base − allowance)`, capped to market for the scenario. Official 2025–27 allowance is exact internally; future biennial amounts use an explicitly hypothetical annualized proxy (not CPI law). Departure restores transfer-date FMV factored forward, with simplified annual lien timing, not current FMV or a permanent reduced base.
- Closing costs separate negotiable selling budget, official county $0.55/$500-or-fraction transfer rule, recording and escrow sensitivities. Actual deed/city/exemption/negotiated incidence is not verified. No tax refund for a loss is invented.
- Nov 2026 Prop H ballot text is an optional sensitivity, OFF by default: per-parcel multifamily base, area increment, cap, conditional resident-senior deduction, CPI increases/downward rounding and explicit June 30, 2042 sunset. No unsupported tenant recovery booked. Certification, classification and real area remain unverified; official summary/legal-text rate discrepancy is flagged.

### Investment / crash lab

Long-run property projections use a **rolling Treasury-yield proxy**, not maturity pricing. The dedicated monthly crash lab is more explicit:

- Normalized $1m hypothetical starting capital is identical across entry strategies. Direct Treasury interest is federally taxable (including conditional NIIT), CA-exempt. Stock shape is treated as a chosen gross total-return path; a 1.8% annual dividend proxy is a component **inside** that path, not added a second time, with reinvested net dividends increasing basis.
- During parking, purchase equal available 3/6/12/24-month tenors that mature no later than phase start; fixed purchase yield until maturity; principal/after-tax interest reinvest at the then-current synthetic rollover yield. Terms approximate 13/26/52-week bills and 2-year notes. Two-year notes pay simplified semiannual coupons; bills accrue simple interest. No precise auction discounts/day count, accrued-interest trading, forced sale or early-sale mark-to-market loss is modeled.
- At phase start, segregate the stock budget in non-interest-bearing cash and deploy equal monthly tranches on a fixed calendar. The permanent Treasury sleeve continues rolling. Both simulators prohibit catch-up purchases after the fixed phase window. The annual property model sets a stock budget from initial net sale proceeds; the standalone investment lab sets its budget from available after-tax capital at phase start, so it must not be called an exact property-model reconciliation.
- Treasury accruals at the chart horizon are valued net of prospective interest tax. Terminal portfolio value subtracts modeled gain tax; interim drawdown uses after-drag value before terminal liquidation tax. No full-year future tax return or bond early-sale value is implied.
- Early-crash shapes can favor staging; a rapid rebound demonstrates missed opportunity; a crash after deployment demonstrates retained drawdown risk. Securities may not match these chosen return paths.
- Fed historical accounts support context/severity only. **No reproducible official monthly total-return series was obtained**, so the lab never calls its numerical 1929/2008 shapes historical backtests. No current Treasury auction yield was verified; no displayed yield is a market quote.

### Ranges, distribution and changed inputs

Three coherent **design cases** jointly perturb market/rent, growth, vacancy and costs and show each path's range and ranks. “Down” and “up” describe changed inputs, not guaranteed monotonic outcomes for every path. The 81-point histogram is a fixed 3^4 sensitivity grid; its equal weights are **not probabilities**, confidence intervals, a stochastic forecast or historical frequencies. The transfer/horizon matrix re-runs complete comparisons on identical dates.

Controls recalculate all seven paths and report whether the illustrative leader changed. They never turn that ranking into a household recommendation. Changes and suggestion-review choices live only in tab memory. CSV exports are labeled synthetic and round financial fields to $10; original precision stays in calculations. Suggestion exports distinguish review from implementation. Actual decision/path/date/why stay blank pending private, signed criteria/evidence/professional advice.

## Release and refresh

Automated tests cover rule arithmetic, eligibility gates, ownership/rent invariants, sale timing, debt, capital/depreciation caps, threshold aggregation, nominal/real reconciliation, adverse inputs and staged/rebound counterexamples. Static verification checks source references, self-contained assets, dependency graph, policy and the public build allowlist. Browser checks cover every route, tables, controls, downloads, console/runtime failures, mobile overflow and the one-page PDF; external substantive source review is separate from local link checks.

Proposed review cadence: official authorities quarterly and before transactions; inspections/rent/insurance/estate inventory and scenario refresh annually or after material change. Record revision date, reviewer, sections, status (enacted/proposed/preliminary), effective date and old/new model result. No background legal monitoring, filings, appraisal, quote, secure private vault or actual household selection is running or claimed.
