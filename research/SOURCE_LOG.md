# Official-source verification log (session s-95fcebfc)

All entries were fetched and read in this session. No values were inferred.
Sandbox bash has no outbound network; every check used the page fetch tool.

| # | Item | Verified value / point | Source | Status |
|---|------|------------------------|--------|--------|
| 1 | Federal estate/gift basic exclusion, CY2026 | $15,000,000 (P.L. 119-21) | https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax | enacted |
| 2 | Federal estate filing threshold, year of death 2026 | $15,000,000 | https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax | enacted |
| 3 | Prop 19 parent-child allowance 2/16/2025–2/15/2027 | $1,044,586 | https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf ; https://www.boe.ca.gov/news/2025/nr-25-02.htm | enacted |
| 4 | Prop 19 / RTC 63.2 as amended by SB 293 (Stats. 2025 ch. 539, eff. 1/1/2026) | exclusion only on filed claim; new taxable value formula; claim deadlines | https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB293 ; https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB293 | **enacted** (chaptered 10/10/2025) |
| 5 | SB 284 (family homes & farms, CIC) | Active — in committee process | https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284 | **proposal, not law** |
| 6 | CA estate/inheritance/GST return | None required for deaths ≥ 1/1/2005 | https://www.sco.ca.gov/ardtax_estate_tax.html | enacted |
| 7 | CA property tax overview: 1% general levy, 2% base-year cap, $7,000 homeowners' exemption | — | https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf | enacted |
| 8 | IRS Pub 523 — §121 exclusion, basis, improvements | $250k / $500k MFJ; 2-of-5 tests | https://www.irs.gov/publications/p523 | enacted |
| 9 | FTB 2025 Form 540 instructions: line 62 BHS 1% over $1M | 1% | https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html | enacted |
| 10 | 2025 CA rate schedules X / Y / Z | see model.json | https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf | enacted |
| 11 | 2025 federal LTCG brackets, collectibles 28%, §1250 25% | see model.json | https://www.irs.gov/taxtopics/tc409 | enacted |
| 12 | NIIT 3.8%, single threshold $200,000 | — | https://www.irs.gov/taxtopics/tc559 | enacted |
| 13 | Filing threshold table (IRS estate tax page) | 2026 = $15,000,000 | https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax | enacted |
| 14 | FRED NASDAQCOM daily, 2007–2009 | peak 2,859.12 (2007-10-31); trough 1,268.64 (2009-03-09) = −55.6% | https://fred.stlouisfed.org/series/NASDAQCOM | verified-fetch |
| 15 | FRED M1109BUSM293NNBR (NBER monthly index) 1929–1932 | peak 362.35 (Sep 1929); trough 46.85 (Jun 1932) = −87.1% | https://fred.stlouisfed.org/series/M1109BUSM293NNBR | verified-fetch |
| 16 | FRED CPIAUCNS 1929–1932 | 17.3 (Sep 1929) → 13.6 (Jun 1932) = −21.4% | https://fred.stlouisfed.org/series/CPIAUCNS | verified-fetch |
| 17 | FRED TB3MS (3-month bill) 2007–2008 and 1934–1940 | 2007-09 3.89%; 2008-12 0.03%; 1934-01 0.72%; 1940-01 0.01% | https://fred.stlouisfed.org/series/TB3MS | verified-fetch |
| 18 | Fed Dec-2025 SEP medians | PCE 2026 2.4 / 2027 2.1 / LR 2.0; real GDP 2026 2.3 / LR 1.8; fed funds LR 3.0 | https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20251210.htm | verified-fetch |
| 19 | CBO Jan 2025 outlook addendum | real GDP ~1.8%/yr 2027–2035; inflation 2% by 2027 | https://www.cbo.gov/publication/61189 | verified-fetch |
| 20 | SSA 2025 Trustees Report | TOC only; values NOT extracted | https://www.ssa.gov/oact/TR/2025/trTOC.html | **flagged** |

## Not verified (flagged, not published)
- SF real property transfer tax schedule — sf.gov and sftreasurer transfer-tax URLs failed to load.
- Santa Clara assessor Prop 13 / Prop 19 guidance — assessor Prop 13 URL returned homepage only.
- Full monthly 1929–1932 and 2008 equity paths — only endpoints fetched; phased-entry path results NOT published.
- Treasury daily par yield curve, SF Rent Board allowable increase, HUD FMR (SF), insurance and rent comparables — not verified.
- FRED S&P 500 graph endpoint returns only 2016+ data in this session.

## Privacy
Personal and household figures gathered for the analysis are not in this log or the published site.
