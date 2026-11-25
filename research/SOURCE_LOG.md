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

## Verification log — session arena/da762c26 (2026-11-25)

| # | Item | Verified value / point | Source | Status |
|---|------|------------------------|--------|--------|
| 21 | Federal basic exclusion CY2026 | $15,000,000 (P.L. 119-21 §70106 amends §2010(c)(3)) | https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax | enacted (fetch re-verified) |
| 22 | Prop 19 $1M amount adjustment | $1,044,586 for transfers 2/16/2025–2/15/2027; prior $1,022,600 / $1,000,000; adjusted every other Feb 16 by FHFA CA HPI; next Feb 2027 | https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf | enacted (fetch re-verified) |
| 23 | SB 293 (2025) | Chaptered 10/10/2025 (ch. 539); amends R&T 63.1/63.2 — claim-filing relief for specified 2025 wildfire cases (3-yr window from supplemental/escape notice, claims < 1/1/2031) + homeowners'/veterans' exemption filing relief | https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB293 | enacted (fetch re-verified) |
| 24 | S&P 500 + T-bill annual returns 1928–2025 | Full series read (1929 −8.30/3.16 … 2008 −36.55/1.40, 2022 −18.04/2.09, 2025 +17.78/4.21) | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html | verified-fetch (Jan 2026 dataset) |
| 25 | FTB 540 line 62 (1% over $1M) | Behavioral Health Services Tax (renamed TY2025+); CA gain = ordinary income | https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html | verified (booklet read in session s-95fcebfc; corroborated by search) |
| 26 | SF real property transfer tax schedule | Not extracted — sf.gov and sftreasurer transfer-tax URLs failed to load | https://sf.gov/information--real-property-transfer-tax | FLAGGED — no figures published |
| 27 | HUD FMR Santa Clara County FY2026 3BR/4BR | $4,602 / $5,010 (via data mirrors of HUD FMR) | https://www.huduser.gov/portal/datasets/fmr.html | FLAGGED — mirror-sourced; confirm in HUD lookup |
| 28 | Home insurance expectations, Santa Clara County | Commercial aggregators show county averages ≈$1,000–$1,300 (2025-26); no official premium dataset exists | https://www.insurance.ca.gov/ | FLAGGED — estimates only; quotes required |

Owner policy applied this session: household figures published rounded to nearest $10;
identifiers (names/addresses/ZIPs/APNs/account numbers) and exact unrounded values banned
from public artifacts. Decision recorded in COORDINATION.md, 2026-11-25.

## Session a69037f0 (2026-11-25) — figures layer verification (numbering continues after da762c26)

Owner policy applied: household figures published rounded to the nearest $10 with placeholders
(Property A / Property B); identifiers and unrounded values blocked by CI. Not published here.

| # | Item / source | Extracted value / conclusion | URL | Status |
|---|---|---|---|---|
| 29 | IRS Pub 527 (2025), Chapter 2 + Table 2-1 | Residential rental GDS recovery period 27.5 years (table + worked example); land not depreciable; allocate land/building cost by FMV ratio (assessed values if FMV unknown); MACRS mandatory post-1986; placed-in-service = ready and available for rent; settlement fees (abstract, recording, title insurance, transfer taxes, legal, survey) in basis; loan costs/points/appraisal/credit report out; depreciation reduces basis | https://www.irs.gov/publications/p527 | verified-fetch |
| 30 | IRS "What's new — estate and gift tax" | Basic exclusion $13,610,000 (2024) / $13,990,000 (2025) / $15,000,000 (2026, P.L. 119-21); 2011–2026 exclusion table; annual gift exclusion per donee $19,000 (2025) and $19,000 (2026) — resolves earlier "gift amount not on overview page" flag; top rate 40%; portability/DSUE; Form 8971; closing-letter fee $76 | https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax | verified-fetch |
| 31 | SCC Controller FY2025-26 Tax Rate Book (PDF) | 1% maximum levy + voter debt per $100 of assessed value; 816 TRAs; agency rate rows read (County Retirement 0.03880, Library Retirement 0.00240, VMC 2008 0.00520, County Housing Bond 2016 0.00560, SCVWD State Water 0.00390 L&I; Property A market-area school measures read but name↔rate pairing inferred). Parcel's exact TRA row beyond 30-page fetch cap | https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf | verified-fetch (structure), **flagged** (exact TRA row) |
| 32 | ASR Santa Clara County site | DTAC contact (408) 808-7900 / scctax@dtac.santaclaracounty.gov; old sccassessor.org DTAC URL is dead (redirects to home) | https://asr.santaclaracounty.gov/home | verified-fetch |
| 33 | FHFA all-transactions HPI (via public mirror) | California 2025 index 324: +0.8% (2024–25), +39.8%/5y (~6.9%/yr), +80.3%/10y (~6.1%/yr), +224% since 2000 (~4.9%/yr). San Jose MSA 2025 index 279.7: +33%/5y, +180% since 2000 (~4.2%/yr). Grounds the 2.0–5.0% nominal band | mirror of https://www.fhfa.gov/data/hpi | **mirror — flagged** |
| 34 | Property A market rental comps (commercial listing snapshot) | 4BR asking: $5,150/1,800sf, $5,895/1,798sf, $6,888/2,169sf, $7,495/2,524sf, $7,750/2,539sf, $8,395/2,595sf; 3BR $5,500/1,576sf; outliers $14,130 furnished, $10,800 3BR excluded. Band used: $5,150–$8,400/mo | listing snapshot, 2026-11-25 (search URL withheld to protect market area) | **unofficial — flagged** |
| 35 | Insurance planning bands (commercial) | County typical $1,010–$1,260/yr; California typical $1,490–$1,760/yr; household estimate $1,500/yr; high-value dwelling and landlord cover expected above typical | quote aggregators, 2026-11-25; official start https://www.insurance.ca.gov/ | **unverified — flagged** |
| 36 | Treasury bill yield (for staged path) | Approx. 3–5 yr ≈ 4.3% (Treasury curve, Nov 2026) used as the park rate | https://home.treasury.gov/resource-center/data-chart-center/interest-rates | approximate — flagged |

## Not verified (flagged, not published) — additions in session a69037f0
- Exact Property A TRA row (rate book deep page): publish household-derived effective rate ≈ 1.33% of assessed value only, with "confirm from the tax bill TRA line" flag.
- Property B effective rate anomaly (≈ 2.0–2.1% of assessed value): parcel taxes/special assessments suspected; reconcile the actual bill lines.
- City documentary transfer tax add-on for Property A's city; title/escrow/recording fees (left blank in the model).
- Recording fees, sewer-lateral transfer compliance for Property B's city, free-unit rental opportunity estimate (~$3,200/mo placeholder).
- Any future Prop 19 allowance adjustment (carry-forward at +2.15%/biennium is a labelled placeholder) and any federal exclusion figure beyond 2026.

## Privacy (supplement)
Under the owner decision of 2026-11-25, rounded ($10) household figures with placeholders appear on
figures.html only; unrounded values, identifiers and market-area names are blocked by CI. Nothing
in this log identifies a property.

| 37 | RTC 63.2(d) Prop 19 new-taxable-value formula | New taxable value = transferor's factored value immediately prior to transfer (Sec. 110.1) PLUS, where market value at transfer >= factored + adjusted allowance, the excess of market value over that sum (statute text says $1,000,000; adjusted allowance $1,044,586 for 2/16/2025-2/15/2027 per BOE LTA 2025/009). Filing: homeowners' exemption within 1 year; claim within 3 years or before a third-party transfer/occupancy end, whichever earlier; late claims apply from lien date of filing year (subd. (f)(3)) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2 | verified-fetch (full text, 3 chunks) |
