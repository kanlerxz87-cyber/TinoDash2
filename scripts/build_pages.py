#!/usr/bin/env python3
"""
Generate the decision-support pages from one consistent template.

Pages produced
    war-room.html    cockpit: first-screen gates, pre-commitment, requirement coverage, decision journal
    worksheets.html  blank depreciation/recapture and estate-liquidity/portability worksheets
    law-watch.html   enacted law vs proposals, recheck calendar
    questions.html   every open question, its status, and how to close it
    comparison.html  all choices on identical dates/horizons + reinvestment risk + browser calculator
    suggestions.html reviewable implementation queue with acceptance criteria
    brief.html       one-page printable attorney & CPA briefing sheet

Rules enforced here
    * No household figures. Everything is a protocol, a range, or a public-law anchor.
    * Every table row carries at least one link (scripts/check_site.py enforces it).
    * Status language never claims more than the evidence: "verified", "unverified",
      "missing", "owner action".
"""
from __future__ import annotations

import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TODAY = "2026-11-25"

# ---------------------------------------------------------------- sources ----
S = {
    "irs_excl": "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax",
    "irs_706": "https://www.irs.gov/instructions/i706",
    "irs_estate": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
    "irs_551": "https://www.irs.gov/publications/p551",
    "irs_523": "https://www.irs.gov/publications/p523",
    "irs_t701": "https://www.irs.gov/taxtopics/tc701",
    "irs_527": "https://www.irs.gov/publications/p527",
    "irs_544": "https://www.irs.gov/publications/p544",
    "irs_1031": "https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips",
    "irs_409": "https://www.irs.gov/taxtopics/tc409",
    "irs_4562": "https://www.irs.gov/forms-pubs/about-form-4562",
    "irs_4797": "https://www.irs.gov/forms-pubs/about-form-4797",
    "irs_4768": "https://www.irs.gov/forms-pubs/about-form-4768",
    "irs_nd": "https://www.irs.gov/businesses/small-businesses-self-employed/how-to-close-a-business",
    "rtc17043": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=17043",
    "rtc632": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2",
    "rtc11911": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911",
    "ftb540_2025": "https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html",
    "ftb540_2024": "https://www.ftb.ca.gov/forms/2024/2024-540-booklet.html",
    "ftb_capgain": "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html",
    "boe19": "https://www.boe.ca.gov/prop19/",
    "boe_allow": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
    "boe_pub29": "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf",
    "scc_ratebook": "https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book",
    "scc_assessor": "https://asr.santaclaracounty.gov/",
    "scc_dtac": "https://www.sccdtac.org/",
    "sf_transfer": "https://www.sf.gov/transfer-tax",
    "sf_rent": "https://www.sf.gov/departments--rent-board",
    "sf_dbi": "https://www.sf.gov/departments--department-building-inspection",
    "sfmta_proph": "https://www.sfmta.com/getting-around/muni/parcel",
    "sco_estate": "https://www.sco.ca.gov/ardtax_estate_tax.html",
    "treasury": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates",
    "tbill": "https://www.treasurydirect.gov/marketable-securities/treasury-bills/",
    "sipc": "https://www.sec.gov/about/reports-publications/investorpubsips",
    "investor": "https://www.investor.gov/introduction-investing",
    "ins": "https://www.insurance.ca.gov/",
    "cslb": "https://www.cslb.ca.gov/",
    "leginfo": "https://leginfo.legislature.ca.gov/",
    "nber": "https://www.nber.org/research/business-cycle-dating",
    "bls": "https://www.bls.gov/cpi/",
    "ftc": "https://www.ftc.gov/business-guidance/privacy-security",
    "irs": "https://www.irs.gov/",
    "ftb": "https://www.ftb.ca.gov/",
    "boe": "https://www.boe.ca.gov/",
    "sccgov": "https://www.sccgov.org/",
    "damodaran": "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html",
    "minfed": "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-",
}


def a(key: str, label: str) -> str:
    return f'<a href="{S[key]}">{label}</a>'


def ext(url: str, label: str) -> str:
    return f'<a href="{url}">{label}</a>'


# ------------------------------------------------------------------- layout ---
GROUPS = [
    ("Decide", [
        ("war-room.html", "War room &amp; decision gates"),
        ("comparison.html", "Compare every path"),
        ("crash-replay.html", "Crash-entry replay"),
        ("crash-replay.html#how-to-use", "Reinvestment risk"),
        ("worksheets.html", "Tax worksheets"),
    ]),
    ("Evidence", [
        ("questions.html", "Questions &amp; missing data"),
        ("law-watch.html", "Law watch: enacted vs proposed"),
        ("index.html#facts", "Evidence inventory"),
        ("FLAGGED_FOR_REVIEW.html", "Flagged for review"),
    ]),
    ("Act", [
        ("brief.html", "Printable attorney &amp; CPA brief"),
        ("index.html#timeline", "Deadlines timeline"),
        ("suggestions.html", "Suggested improvements"),
        ("index.html#glossary", "Glossary"),
    ]),
]


def nav(current: str) -> str:
    blocks = []
    for label, items in GROUPS:
        links = []
        for href, text in items:
            active = ' class="nav-link active"' if href == current else ' class="nav-link"'
            links.append(f'<a{active} href="{href}">{text}</a>')
        blocks.append(f'<p class="nav-label">{label.upper()}</p>' + "".join(links))
    return (
        '<aside class="sidebar" aria-label="Main navigation">'
        + "".join(blocks)
        + '<div class="sidebar-note"><strong>Privacy first</strong><p>No names, addresses, ZIP codes, parcel '
        'numbers, trust terms, or household values appear on this site. Anything entered in the '
        'calculator stays in your browser.</p></div></aside>'
    )


def page(slug: str, title: str, kicker: str, heading: str, intro: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow">
<title>{title} | Estate Pathways</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="index.html"><span class="brand-mark">EP</span><span>Estate Pathways<small>Private decision workspace</small></span></a>
  <div class="top-actions">
    <span class="privacy-chip"><span aria-hidden="true">●</span> Browser-only model · no analytics</span>
    <a class="button button-quiet" href="brief.html">Print the brief</a>
  </div>
</header>
<div class="app-shell">
{nav(slug)}
<main id="main">
  <div class="eyebrow">{kicker}</div>
  <h1 style="font:800 clamp(30px,3.6vw,44px)/1.12 Manrope,sans-serif;letter-spacing:-1.4px;margin:0 0 12px;color:#123040">{heading}</h1>
  <p class="hero-sub">{intro}</p>
{body}
  <footer><p>Estate Pathways · evidence-led planning workspace · not legal, tax, insurance, appraisal, or investment advice.</p>
  <p>Public anchors re-checked {TODAY}. Never put parcel numbers, addresses, account numbers, or private documents in this repository.</p>
  <p><a href="index.html">Dashboard</a> · {ext("https://github.com/kanlerxz87-cyber/TinoDash2", "Repository")} · <a href="FLAGGED_FOR_REVIEW.html">Flagged for review</a></p></footer>
</main>
</div>
</body>
</html>
"""


def table(headers, rows) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def section(num: str, kicker: str, heading: str, lead: str, inner: str) -> str:
    return (
        f'<section class="content-section"><div class="section-heading"><div>'
        f'<div class="eyebrow">{num} · {kicker}</div><h2>{heading}</h2></div>'
        f'<p>{lead}</p></div>{inner}</section>'
    )


BADGE = {
    "verified": '<span class="status verified">Verified</span>',
    "unverified": '<span class="status unverified">Unverified</span>',
    "missing": '<span class="status unknown">Missing</span>',
    "owner": '<span class="priority urgent">Owner action</span>',
    "done": '<span class="status verified">Built</span>',
    "protocol": '<span class="status unknown">Protocol only</span>',
}


# =============================================================== war room =====
def build_war_room() -> str:
    gates = [
        ("Is the intended heir an eligible transferee under RTC 63.2, and was the home the transferor's principal residence?",
         "If yes, the property-tax base can stay partly protected; if no, a full reassessment at market value governs every hold path.",
         BADGE["unverified"], "Estate attorney + county assessor",
         a("rtc632", "RTC 63.2") + " · " + a("boe19", "BOE Prop 19")),
        ("Will the heir actually occupy the home as a primary residence within one year and file the exemption?",
         "Occupancy is a legal condition, not an intention. Filing the homeowners' or disabled veterans' exemption within one year is required; the exclusion is removed when eligibility ends.",
         BADGE["missing"], "Heir, in writing, before any projection is commissioned",
         a("rtc632", "RTC 63.2(a)(1)(B)") + " · " + a("boe19", "BOE filing period")),
        ("What is the date-of-death fair market value, and how is it split between land and improvements?",
         "Sets income-tax basis, the consistent-basis statement, the estate return, and the Prop 19 value calculation. A wrong value can invert sell-versus-hold.",
         BADGE["missing"], "Independent retrospective appraisal + CPA",
         a("irs_551", "IRS Pub 551") + " · " + a("irs_estate", "IRS estate tax")),
        ("Is a federal estate return required, and should portability be elected?",
         "The 2026 basic exclusion is $15,000,000 per person; a return is required above the threshold, and a timely return is also how a surviving spouse's unused exclusion is preserved.",
         BADGE["unverified"], "Executor + estate CPA (9-month clock)",
         a("irs_706", "Form 706 instructions") + " · " + a("irs_excl", "IRS 2026 amount")),
        ("What is the parcel's actual tax rate area and published rate?",
         "The 1% base levy is uniform; voter-approved debt and special assessments differ by tax rate area. Citywide averages cannot price a specific bill.",
         BADGE["unverified"], "County assessor / controller rate book (private lookup)",
         a("scc_ratebook", "SCC tax rate book") + " · " + a("scc_dtac", "SCC DTAC")),
        ("What would the property actually rent for, on evidence?",
         "The rent path is currently a planning floor, not an evidenced option. Independent comparables decide whether it competes at all.",
         BADGE["missing"], "Licensed rental opinion + 3–5 comparable leases",
         a("sf_rent", "Rent-regulation rules") + " · " + a("scc_assessor", "Assessor records")),
        ("What are the real operating costs: insurance, utilities, maintenance and capital?",
         "A single uninsured loss or a roof/system replacement can turn a paper-positive hold into a negative one. Quotes and inspections, not percentages, decide.",
         BADGE["missing"], "Broker quotes + inspection + contractor bids",
         a("ins", "CA Dept. of Insurance") + " · " + a("cslb", "CSLB")),
        ("What is the total estate, including prior taxable gifts, and what liquidity will it need?",
         "Estate tax is an estate-level question; liquidity is a separate one. Both change whether a forced sale is likely.",
         BADGE["missing"], "Private estate inventory + estate attorney",
         a("irs_706", "Form 706") + " · " + a("irs_estate", "IRS estate tax")),
        ("Is any exchange, sale timing, or trust distribution decision required before closing?",
         "A like-kind exchange must be decided before the sale closes and requires a qualified intermediary; the trust instrument may also constrain timing or beneficiaries.",
         BADGE["unverified"], "Attorney + CPA, in writing, pre-listing",
         a("irs_1031", "IRS 1031 guidance") + " · " + a("rtc11911", "RTC 11911")),
    ]
    gate_rows = [(q, why, status, owner, src) for q, why, status, owner, src in gates]
    gate_table = table(
        ["Decision gate", "What changes if the answer is different", "Status", "Who closes it", "Official anchor"],
        gate_rows,
    )

    precommit = [
        ("We will live in the inherited home",
         "Documented, durable occupancy intent; a written statement that the home will be the primary residence within one year and remain so; acceptance of the concentration and capital obligations.",
         "Occupancy is convenient rather than intended, or the household would move within a few years.",
         '<a href="war-room.html#journal">Journal</a> · ' + a("rtc632", "RTC 63.2")),
        ("We will rent it out",
         "Independent market rent that clears all costs after tax with a vacancy and management allowance; a lawful, insurable rental structure; a tax plan for depreciation and recapture.",
         "Evidenced rent does not cover carrying costs plus a reserve, or the legal/insurance structure is unavailable.",
         '<a href="comparison.html">Comparison</a> · ' + a("irs_527", "IRS Pub 527")),
        ("We will sell and reinvest",
         "Written investment policy before proceeds arrive; a tax estimate for a same-tax-year sale; a reserve sized to near-term needs; a decision on phased versus immediate deployment.",
         "Net proceeds cannot fund the stated reserve, or the household cannot tolerate the equity risk the plan requires.",
         '<a href="crash-replay.html">Crash replay</a> · ' + a("tbill", "Treasury bills")),
        ("We will keep a mixed position",
         "An explicit split, a reason for each part, a separate cost and tax treatment for each, and a review date.",
         "The split is a way of postponing the decision rather than expressing a preference.",
         '<a href="comparison.html#mixed">Mixed paths</a> · ' + a("irs_523", "IRS Pub 523")),
    ]
    precommit_table = table(
        ["If we choose…", "We commit to this evidence and condition first", "We change our mind if…", "Where it is recorded"],
        precommit,
    )

    coverage = [
        ("Phased-investing path tested (24–36 months of Treasuries, then phased equity entry)",
         "Replayed every historical start date 1928–2025: phasing beat immediate investing in 15.7% of ten-year windows, median −74.9 points of starting value; in a 1929 entry it won by +107.9 points.",
         BADGE["done"], '<a href="crash-replay.html">Crash-entry replay</a>'),
        ("What would change the answer, on the first screen",
         "Nine decision gates with the consequence of each answer, its status and the person who closes it.",
         BADGE["done"], '<a href="war-room.html">This page</a>'),
        ("Mixed paths alongside the three pure choices",
         "Live-then-sell, rent-then-sell, partial retention, and staged reinvestment are compared on the same dates and horizons.",
         BADGE["done"], '<a href="comparison.html#mixed">Mixed paths</a>'),
        ("Reinvestment risk shown beside the headline",
         "Every staged figure is reported with the cash-drag cost, the delay to full exposure, and the yield-reset assumption.",
         BADGE["done"], '<a href="crash-replay.html#how-to-use">Reinvestment risk</a>'),
        ("Ranges instead of round-number points",
         "Property values, rents, and returns are carried as low/base/high ranges in the calculator and as full historical distributions in the replay.",
         BADGE["protocol"], '<a href="comparison.html#calculator">Calculator</a>'),
        ("Same transfer dates and horizons for every path",
         "One shared start date and one shared end date per comparison row; no path is measured on a different calendar.",
         BADGE["protocol"], '<a href="comparison.html">Comparison</a>'),
        ("Imputed rent on living paths",
         "The calculator includes an imputed-rent field so living in the home is credited with the housing it provides, not just charged its costs.",
         BADGE["protocol"], '<a href="index.html#scenarios">What-if model</a>'),
        ("Primary-residence exclusion switch for living-then-sell",
         "Section 121 requires ownership and use tests measured on the actual history; the calculator keeps it as an explicit, off-by-default input.",
         BADGE["unverified"], a("irs_t701", "IRS Topic 701")),
        ("Proposition 19 allowance carried forward",
         "The published allowance is a biennial inflation adjustment; the current figure applies only to transfers between 16 Feb 2025 and 15 Feb 2027.",
         BADGE["verified"], a("boe_allow", "BOE LTA 2025/009")),
        ("Transfer tax and recording fees priced into the sell path",
         "County documentary transfer tax is a statutory rate; the city tier applies separately and must be confirmed at closing.",
         BADGE["verified"], a("rtc11911", "RTC 11911") + " · " + a("sf_transfer", "SF transfer tax")),
        ("Depreciation and recapture worksheet",
         "Every input is named with its official rule, so a CPA can rebuild basis, allowed or allowable depreciation and the recapture exposure. No figure is published or assumed: the numbers are property-specific facts.",
         BADGE["done"], '<a href="worksheets.html">Tax worksheets</a> · ' + a("irs_527", "IRS Pub 527")),
        ("Estate tax, income-tax basis and property-tax assessment separated",
         "Three separate systems with three separate numbers and clocks, each carried in its own column and its own source.",
         BADGE["done"], a("irs_706", "Form 706") + " · " + a("irs_551", "Pub 551") + " · " + a("boe_pub29", "BOE Pub 29")),
        ("Distribution chart, not a single projection",
         "Ten-year real outcomes are shown as percentiles and per-start-year bars, not as one CAGR.",
         BADGE["done"], '<a href="crash-replay.html#distribution">Distribution</a>'),
        ("Deadlines as a timeline",
         "Process checkpoints from before transfer to annual review, each with its statutory anchor.",
         BADGE["done"], '<a href="index.html#timeline">Timeline</a>'),
        ("Grouped menu and glossary",
         "Navigation is grouped Decide / Evidence / Act; terms that are easily confused are defined separately.",
         BADGE["done"], '<a href="index.html#glossary">Glossary</a>'),
        ("Periodic recheck of official authorities, proposals separated from law",
         "A dated recheck calendar with the exact page to open and the decision each affects.",
         BADGE["done"], '<a href="law-watch.html">Law watch</a>'),
        ("Written choice rule agreed before the figures arrive",
         "The pre-commitment register above is filled in and dated before any appraisal or rent opinion is ordered.",
         BADGE["protocol"], '<a href="war-room.html#precommit">Pre-commitment</a>'),
        ("Estate liquidity and portability worksheet",
         "Five-step order of operations with the eleven questions a CPA must answer, including the nine-month clock, the extension that does not extend payment, and the portability election that is lost by inaction. The inventory itself stays private.",
         BADGE["done"], '<a href="worksheets.html">Tax worksheets</a> · ' + a("irs_706", "Form 706")),
        ("Independent property and rental estimates",
         "Not obtained. The site deliberately shows no value or rent figure for either property.",
         BADGE["missing"], a("scc_assessor", "Assessor records") + " · " + a("cslb", "Licensed appraisers")),
        ("Re-run the model and site after any input change",
         "Two scripts rebuild the replay and the page; a third verifies the dataset against the publisher's own index columns.",
         BADGE["done"], ext("https://github.com/kanlerxz87-cyber/TinoDash2/blob/main/scripts/build_blackswan.py", "build_blackswan.py")),
        ("Prior public-data exposure contained",
         "Containment of the working tree is done; the repository history and closed pull-request refs still contain earlier household figures and require repository-owner action. This site does not claim the history is scrubbed.",
         BADGE["owner"], '<a href="FLAGGED_FOR_REVIEW.html">Flagged for review</a>'),
    ]
    coverage_table = table(["Requirement", "Where it stands", "Status", "Open it"], coverage)

    journal = [
        ("Chosen path for the inherited home", "—", "—", "—"),
        ("Written occupancy intent (yes/no, date)", "—", "—", "—"),
        ("Date-of-death appraisal ordered / received", "—", "—", "—"),
        ("Estate inventory completed", "—", "—", "—"),
        ("Portability decision recorded", "—", "—", "—"),
        ("Investment policy signed before proceeds arrive", "—", "—", "—"),
        ("Phased vs immediate deployment decided, with trigger", "—", "—", "—"),
        ("Last full model rebuild and site re-verification", "—", "—", "—"),
        ("Next scheduled law recheck", "—", "—", "—"),
    ]
    journal_table = table(
        ["Decision item", "What was chosen", "Date", "Reason recorded", "Anchor"],
        [
            (f"<strong>{d}</strong>", w, dt, r,
             a("irs_706", "Form 706") if "estate" in d.lower() or "portab" in d.lower()
             else ('<a href="crash-replay.html">Crash replay</a>' if "phased" in d.lower() or "model" in d.lower()
                   else ('<a href="law-watch.html">Law watch</a>' if "law" in d.lower()
                         else a("irs_551", "IRS Pub 551"))))
            for d, w, dt, r in journal
        ],
    )

    body = ""
    body += (
        '<div class="decision-state"><span class="state-icon">!</span><div>'
        "<strong>No defensible winner yet — by design.</strong>"
        "<p>Four of the nine gates below are missing outright and the rest are unverified. Any number produced before those gates close would be a "
        "precision the evidence cannot support. What this site can do today is fix the decision rules, price the public-law anchors, and show "
        "how the staged-investing idea performs against real history.</p></div></div>"
    )
    body += section("01", "FIRST SCREEN", "Do not decide until these are answered",
                  "Each gate changes the ranking of the options, not merely the size of the numbers.",
                  gate_table)
    body += section("02", "PRE-COMMITMENT", "Write the choice rule before the figures arrive",
                  "Agreeing the conditions in advance is the only real defence against reverse-engineering a decision from one projection. "
                  "Fill this in, date it, and only then order appraisals and rent opinions.",
                  precommit_table)
    body += '<div id="precommit"></div>'
    body += section("03", "REQUIREMENT COVERAGE", "Every requirement in the brief, and where it stands",
                  "Built items link to the page that implements them. Missing items are protocol only and are not dressed up as analysis.",
                  coverage_table)
    body += '<div id="journal"></div>'
    body += section("04", "DECISION JOURNAL", "Write the decision and the date next to the item",
                  "Print this page and keep it with the estate documents so a future reader knows what was chosen and why.",
                  journal_table)
    return page(
        "war-room.html",
        "War room: decision gates and pre-commitment",
        "DECISION COCKPIT · NO HOUSEHOLD FIGURES · NOT ADVICE",
        "The decision is not ready. Here is exactly what is missing.",
        "Nine gates stand between the current evidence and a defensible choice between living in, renting, selling, or splitting the inherited home. "
        "Below them is the pre-commitment register that should be signed before any appraisal, rent opinion or projection is ordered.",
        body,
    )


# ============================================================== law watch =====
def build_law_watch() -> str:
    enacted = [
        ("Federal basic estate-tax exclusion, 2026",
         "$15,000,000 per person; top rate 40% above that; portability available on a timely return. Enacted by Public Law 119-21, signed 4 July 2025.",
         "Sets the estate-level question and the Form 706 filing threshold for a 2026 death only. It is not indexed here and not projected to a 2040–2050 death.",
         BADGE["verified"], a("irs_excl", "IRS: what&rsquo;s new, estate &amp; gift")),
        ("Form 706 due date, extension, portability",
         "Return due 9 months after death; automatic 6-month extension on Form 4768; portability election only on a timely return, with a limited later relief route.",
         "The portability clock starts at death, so the estate discussion cannot wait for the property decision.",
         BADGE["verified"], a("irs_706", "Form 706 instructions")),
        ("Inherited basis and consistent-basis reporting",
         "Basis is generally fair market value at date of death; the recipient&rsquo;s basis must be consistent with the value finally determined for estate tax, and a statement is required where a return is filed.",
         "Makes a defensible date-of-death appraisal mandatory, not optional.",
         BADGE["verified"], a("irs_551", "IRS Pub 551") + " · " + a("irs_706", "Consistent basis reporting")),
        ("Section 121 home-sale exclusion",
         "$250,000 single / $500,000 joint, subject to two-of-five-year ownership and use tests and a two-year look-back.",
         "Only reachable on a living-then-selling path, and only on evidence of actual occupancy.",
         BADGE["verified"], a("irs_t701", "IRS Topic 701") + " · " + a("irs_523", "IRS Pub 523")),
        ("Section 1031 like-kind exchanges",
         "Since 2018 limited to real property held for business or investment; personal residences do not qualify.",
         "A decision to be taken before a sale closes, with a qualified intermediary. Not a rescue for a mistaken sale.",
         BADGE["verified"], a("irs_1031", "IRS 1031 guidance")),
        ("California Proposition 19 intergenerational exclusion",
         "Family home or family farm; transferee must occupy within one year and file the homeowners&rsquo; or disabled veterans&rsquo; exemption within one year; claim for exclusion within three years or before transfer to a third party; value cap of factored base year value plus the adjusted $1 million amount.",
         "The single largest swing factor in the property-tax projection, and it depends on facts that are not yet documented.",
         BADGE["verified"], a("rtc632", "RTC 63.2") + " · " + a("boe19", "BOE Prop 19")),
        ("Proposition 19 allowance, current adjustment",
         "$1,044,586 for transfers between 16 February 2025 and 15 February 2027 (from $1,022,600 in the prior window). Adjusted every second February 16 against the FHFA California house price index.",
         "The figure that applies to a 2040–2050 transfer does not exist yet. Any long-range model must state that it is using a placeholder.",
         BADGE["verified"], a("boe_allow", "BOE LTA 2025/009")),
        ("Proposition 13 assessment mechanics",
         "Base-year value set at change of ownership; annual inflation factor capped at 2%; voter-approved debt sits outside the 1% cap.",
         "Distinguishes assessed value from market value, which is the most common error in this kind of projection.",
         BADGE["verified"], a("boe_pub29", "BOE Pub 29")),
        ("California income tax on capital gains",
         "No preferential capital-gains rate; gains are taxed as ordinary income on the California return.",
         "A sale in a high-income year, or in the same year as other income, is materially more expensive in California than the federal rate alone suggests.",
         BADGE["verified"], a("ftb_capgain", "FTB capital gains")),
        ("California additional 1% tax above $1,000,000 of taxable income",
         "Statutory 1% additional tax under RTC 17043; shown on the 2025 Form 540 as line 62, &ldquo;Behavioral Health Services Tax&rdquo;, computed in whole dollars with a $1,000,000 threshold.",
         "A large sale gain can cross this threshold in the sale year. The 2024 booklet labelled the same line differently, so the filing-year booklet governs.",
         BADGE["verified"], a("rtc17043", "RTC 17043") + " · " + a("ftb540_2025", "2025 Form 540 booklet")),
        ("California estate or inheritance tax",
         "No California estate tax return is required for decedents dying on or after 1 January 2005 under the current framework; federal estate tax still applies.",
         "Frequently mis-stated. The federal question is the one that matters, and it is not a per-heir allowance.",
         BADGE["verified"], a("sco_estate", "CA State Controller")),
        ("County documentary transfer tax",
         "Counties may impose $0.55 per $500 of consideration under RTC 11911; a city may add up to half that rate, with a credit against the county tax.",
         "Priceable only at the actual sale price and location; it is a line in the sell path, not a rounding item.",
         BADGE["verified"], a("rtc11911", "RTC 11911")),
        ("San Francisco real property transfer tax",
         "Tiered city rate, for example $3.75 per $500 at $1M–$5M and $11.25 per $500 at $5M–$10M, applied to the whole consideration.",
         "Relevant only if the San Francisco property is ever sold; it is not a cost of inheriting the other home.",
         BADGE["verified"], a("sf_transfer", "SF transfer tax")),
        ("San Francisco parcel tax, November 2026 Proposition H",
         "Approved 3 November 2026; levied 1 July 2027 to 30 June 2042 and indexed from FY2028-29. FY2027-28 rates: single-family $129 up to 3,000 sq ft, then +$0.42/sq ft to 5,000 sq ft, then $969 + $1.99/sq ft above 5,000 sq ft; multifamily $249 up to 5,000 sq ft, then +$0.195/sq ft (cap $50,000); non-residential $799; mixed-use and unimproved parcels have their own schedules. Full exemption for an owner aged 65+ occupying a single-family parcel as principal residence; $249 reduction per senior-occupied unit in a multifamily parcel; SRO building area exempt. Senior and SRO relief requires an application by 1 June for the following fiscal year.",
         "A recurring carrying cost on the San Francisco parcel that did not exist in earlier budgets. The tier depends on building area and parcel type, so the actual figure requires the parcel record — it cannot be assumed from the property-tax bill alone.",
         BADGE["verified"], a("sfmta_proph", "SFMTA: Prop H parcel tax")),
        ("San Francisco residential rent regulation",
         "Covered units are subject to the Rent Ordinance's limits on increases and grounds for eviction; the allowable annual increase for covered units effective 1 March 2026 to 28 February 2027 is 1.6%, and a Rent Board fee and Housing Inventory filing apply to most residential units. Whether a unit is covered depends on its legal status, registration and use history.",
         "Owner move-in, unit conversion and vacancy can change lawful rent and occupancy; none of it should be assumed from gross rent, and the permitted increase is a public number rather than a household estimate.",
         BADGE["verified"], a("sf_rent", "SF Rent Board")),
    ]

    proposed = [
        ("Proposition 19 expansion proposals in the Legislature",
         "Bills have been introduced to widen qualifying intergenerational transfers and adjust timing for certain court-ordered transfers. Status must be read from the official bill page each session.",
         "None of it is modelled. A proposal that has not been enacted and taken effect cannot change a projection.",
         BADGE["unverified"], a("leginfo", "California Legislative Information") + " · " + a("boe", "BOE Prop 19 letters")),
        ("Federal exclusion after 2026",
         "The $15,000,000 amount is the 2026 figure. Later years depend on published inflation adjustments and on any future legislation.",
         "A 2040–2050 death is outside any published exclusion. The model must not imply otherwise.",
         BADGE["unverified"], a("irs_excl", "IRS what&rsquo;s new") + " · " + a("irs", "IRS")),
        ("State proposals that would tax unrealized gain or large holdings",
         "Recurring legislative interest in wealth or unrealized-gain taxation exists at state and federal level. Enactment status changes session by session.",
         "If enacted before the transfer, it would change the cost of holding rather than selling. Tracked, not modelled.",
         BADGE["unverified"], a("leginfo", "California Legislative Information")),
        ("Local parcel taxes and bond measures",
         "Voter-approved debt and parcel taxes raise the effective rate above the 1% base levy and differ by tax rate area and election cycle.",
         "Explains why a citywide average rate cannot price a specific bill.",
         BADGE["unverified"], a("scc_ratebook", "SCC tax rate book") + " · " + a("sf_transfer", "SF revenue measures")),
        ("Insurance market and FAIR-plan availability",
         "Wildfire and earthquake underwriting in California has been changing quickly, including insurer withdrawals and residual-market rules.",
         "A hold path is only as good as its insurability. This is a cost and availability risk, not a premium estimate.",
         BADGE["unverified"], a("ins", "CA Dept. of Insurance")),
        ("Interest rates and Treasury yields",
         "Short-term yields reset continuously; a phased plan&rsquo;s cash leg is reinvested at unknown future rates.",
         "The replay uses historical bill returns as one case, plus zero and equity-return bounds, precisely because the future yield is unknowable.",
         BADGE["verified"], a("treasury", "Daily Treasury rates")),
    ]

    calendar = [
        ("Every October", "Federal inflation adjustments for the following tax year, including the basic exclusion amount and gift annual exclusion.",
         "Estate-tax projection and Form 706 threshold", a("irs_excl", "IRS what&rsquo;s new")),
        ("Every February 16 (biennial)", "Proposition 19 $1 million allowance adjustment against the FHFA California house price index.",
         "Property-tax projection on any hold path", a("boe_allow", "BOE LTA letters")),
        ("Each January", "New California statutes take effect; read the enacted chapter and the BOE letters to assessors.",
         "Prop 19 mechanics, transfer rules, income tax", a("leginfo", "LegInfo") + " · " + a("boe", "BOE")),
        ("Each fiscal year (July 1)", "County tax rate book published with rates by tax rate area; parcel bill follows in the autumn.",
         "Actual property-tax bill", a("scc_ratebook", "SCC tax rate book")),
        ("Each November election", "Local parcel taxes, bonds and transfer-tax measures.",
         "Carrying cost and sell-path transaction cost", a("leginfo", "LegInfo") + " · " + a("sf_rent", "SF measures")),
        ("On any household change", "Marriage, death, gift, trust amendment, refinance or change of occupancy.",
         "Eligibility, basis, portability, rent rules", a("irs_706", "Form 706") + " · " + a("rtc632", "RTC 63.2")),
        ("Before any sale closes", "Transfer-tax schedule, recording fees, exemptions, and any exchange decision.",
         "Net proceeds", a("rtc11911", "RTC 11911") + " · " + a("sf_transfer", "SF transfer tax")),
        ("Annually, and after any input change", "Rebuild the replay and the site; re-verify every cited anchor.",
         "Whether the recommendation moved", '<a href="crash-replay.html">Crash replay</a>'),
    ]

    body = (
        '<div class="callout"><strong>Rule for this page:</strong> a proposal is never modelled as law. Enacted rules carry an effective date and an official '
        'citation; open proposals are listed separately with the official status page so the distinction cannot be lost.</div>'
        + section("01", "ENACTED", "Rules that are actually in force",
                  "Each row is a public-law anchor with the official page that states it. Re-check the page before relying on the figure.",
                  table(["Rule", "What it says now", "Why it matters to this decision", "Status", "Official source"], enacted))
        + section("02", "PROPOSED / OPEN", "Things being discussed that are not law",
                  "Tracked so they can be recognised when they change, never used to justify a projection.",
                  table(["Item", "Where it stands", "How it is treated here", "Status", "Official source"], proposed))
        + section("03", "RECHECK CALENDAR", "When each authority has to be read again",
                  "A dated cadence beats a resolution to &ldquo;keep an eye on it&rdquo;.",
                  table(["When", "What to open", "Which decision it moves", "Link"], calendar))
        + section("04", "METHOD", "How a law change enters the model",
                  "A repeatable five-step change procedure, so a new statute cannot quietly invalidate a page.",
                  f"<ol><li>Read the enrolled text or official guidance, not a summary article.</li>"
                  f"<li>Record the effective date and the exact transfer or tax year it first applies to.</li>"
                  f"<li>Change the anchor in <code>law-watch</code> and in any page that repeats it; do not leave a stale figure in place.</li>"
                  f"<li>Re-run <code>python3 scripts/verify_sources.py --online</code>, then rebuild the replay and the site.</li>"
                  f"<li>Note in the decision journal whether the ranking of the options moved.</li></ol>"
                  f'<p class="source-note">Primary entry points: {a("irs", "IRS")} · {a("leginfo", "California Legislative Information")} · '
                  f'{a("boe", "California State Board of Equalization")} · {a("ftb", "California Franchise Tax Board")} · {a("sccgov", "Santa Clara County")}.</p>')
    )
    return page(
        "law-watch.html",
        "Law watch: enacted rules versus proposals",
        "ENACTED vs PROPOSED · OFFICIAL SOURCES ONLY",
        "What the law says today, and what is only being talked about.",
        "A 2040–2050 transfer will be governed by law that does not exist yet. The useful discipline is to keep a clean, sourced list of what is "
        "in force now, a separate list of open proposals, and a dated calendar for reading the authorities again.",
        body,
    )


# ============================================================== questions =====
def build_questions() -> str:
    groups = {
        "Eligibility and transfer mechanics": [
            ("Is the intended heir an eligible transferee for a parent–child transfer, and is the relationship documented in the trust?",
             "Determines whether Prop 19 can preserve any of the base-year value.", BADGE["unverified"], "Estate attorney; trust instrument",
             a("rtc632", "RTC 63.2(a)(1)")),
            ("Was the home the transferor&rsquo;s principal residence, and is the transferred parcel the family home and homesite?",
             "Only a principal residence qualifies for the intergenerational exclusion.", BADGE["unverified"], "Assessor records + attorney",
             a("boe19", "BOE Prop 19")),
            ("Will the heir occupy within one year, file the exemption within one year, and remain eligible?",
             "The exclusion is removed when the transferee stops qualifying; occupancy cannot be a formality.", BADGE["missing"], "Written household decision",
             a("rtc632", "RTC 63.2(a)(1)(B)")),
            ("What exactly does the trust say about timing, occupancy rights, sale authority and distributions?",
             "The trust may prohibit or delay the very choice being modelled.", BADGE["missing"], "Trustee + estate attorney",
             a("irs_706", "Form 706 (trust interests)")),
            ("Did the transferor make prior taxable gifts that affect the estate calculation?",
             "Adjusted taxable gifts are added to the gross estate for the filing test and the tax computation.", BADGE["missing"], "Estate CPA",
             a("irs_706", "Form 706 instructions")),
        ],
        "Valuation and tax basis": [
            ("What is the date-of-death fair market value, with a land/improvement split?",
             "Sets income-tax basis, the estate return and the Prop 19 calculation.", BADGE["missing"], "Independent retrospective appraisal",
             a("irs_551", "IRS Pub 551")),
            ("Is there any alternate-valuation election, and did any post-death event affect value?",
             "Alternate valuation, if elected and eligible, changes the basis date and the numbers.", BADGE["missing"], "Estate CPA",
             a("irs_551", "Pub 551 (alternate valuation)")),
            ("What was the historical cost basis in the San Francisco property, and what depreciation has already been taken or allowed?",
             "Depreciation allowed or allowable reduces basis and drives recapture on a later sale.", BADGE["missing"], "CPA, from filed returns",
             a("irs_527", "IRS Pub 527") + " · " + a("irs_544", "Pub 544")),
            ("Which expenses must be capitalised rather than deducted on each property?",
             "Affects basis, current deductions and the eventual gain.", BADGE["missing"], "CPA",
             a("irs_551", "Pub 551 (increases to basis)")),
            ("Would a sale in the same tax year as the inheritance be materially different from a later sale?",
             "Same-year sale is the base case that must be computed before any hold decision.", BADGE["missing"], "CPA",
             a("ftb_capgain", "FTB capital gains") + " · " + a("rtc17043", "RTC 17043")),
        ],
        "Property tax and assessment": [
            ("What is the parcel&rsquo;s tax rate area, and what rate did the county publish for the current fiscal year?",
             "The 1% base is uniform, but voter debt and assessments are not.", BADGE["unverified"], "County rate book + parcel bill",
             a("scc_ratebook", "SCC tax rate book")),
            ("What would the reassessed value be if the exclusion does not apply?",
             "A full reassessment changes the annual carrying cost on every hold path.", BADGE["missing"], "Assessor estimate",
             a("boe_pub29", "BOE Pub 29")),
            ("How is the $1 million allowance applied to this parcel&rsquo;s factored base year value?",
             "The cap is a formula, not a flat exclusion; the arithmetic must be done for the actual parcel.", BADGE["unverified"], "Assessor + attorney",
             a("boe_allow", "BOE LTA 2025/009")),
            ("Are there special assessments, Mello-Roos or bond levies on either parcel?",
             "These sit outside the 1% cap and persist regardless of ownership.", BADGE["missing"], "Parcel tax bill",
             a("scc_dtac", "SCC DTAC")),
        ],
        "Operating costs and insurance": [
            ("What will insurance actually cost and cover, for each occupancy scenario?",
             "Primary-residence, landlord and vacant-property policies price differently and exclude differently.", BADGE["missing"], "Licensed broker, written quotes",
             a("ins", "CA Dept. of Insurance")),
            ("Is the property insurable at all in the current market, and what is the residual-market fallback?",
             "An uninsurable property changes the entire risk profile of holding it.", BADGE["unverified"], "Broker + CA Dept. of Insurance",
             a("ins", "CA Dept. of Insurance")),
            ("What are the actual utility bills and who pays them under each scenario?",
             "Tenant-paid versus owner-paid utilities change the net rent comparison.", BADGE["missing"], "Utility history",
             a("scc_assessor", "Property records")),
            ("What does a five-year capital plan cost: roof, systems, seismic, solar, paint?",
             "A single capital event can exceed several years of net rent.", BADGE["missing"], "Inspection + contractor bids",
             a("cslb", "CSLB licence lookup")),
            ("What is the deferred-maintenance condition of each building today?",
             "Condition, not a percentage of value, determines the reserve.", BADGE["missing"], "Independent inspection",
             a("cslb", "CSLB")),
        ],
        "Rent, tenants and local rules": [
            ("What is evidenced market rent for the inherited home?",
             "Without comparables the rent path is a floor, not an option.", BADGE["missing"], "Licensed rental opinion",
             a("scc_assessor", "Comparable records")),
            ("What do the San Francisco leases actually say, and which units are registered and lawful?",
             "Lawful unit status and lease terms control rent increases, occupancy and conversion.", BADGE["missing"], "Attorney review",
             a("sf_rent", "SF Rent Board") + " · " + a("sf_dbi", "SF DBI")),
            ("Can the owner occupy a unit without losing rental income, as assumed?",
             "Owner move-in can trigger relocation obligations, rent reset and vacancy rules.", BADGE["unverified"], "Rent Board + attorney",
             a("sf_rent", "SF Rent Board")),
            ("Does the November 2026 San Francisco parcel tax apply, at what tier, and can any of it be passed through?",
             "A new recurring carrying cost with a senior exemption and a capped pass-through.", BADGE["unverified"], "Administering agency",
             a("sfmta_proph", "SFMTA Prop H")),
            ("What vacancy, management and turnover allowances are realistic?",
             "Gross rent is not net rent.", BADGE["missing"], "Property manager + history",
             a("sf_rent", "SF Rent Board")),
        ],
        "Estate, liquidity and investing": [
            ("What is the total gross estate, including property outside California?",
             "The filing test and the tax computation are estate-level, not asset-level.", BADGE["missing"], "Private estate inventory",
             a("irs_706", "Form 706")),
            ("Should portability be elected, and is a return being filed anyway?",
             "A timely return preserves the unused exclusion of a deceased spouse.", BADGE["missing"], "Estate attorney + CPA",
             a("irs_706", "Portability")),
            ("Will the estate need liquidity to pay tax, administration and debts?",
             "Liquidity pressure can force a sale at the worst time and override a hold preference.", BADGE["missing"], "Estate attorney",
             a("irs_estate", "IRS estate tax")),
            ("What reserve does the household need outside the property?",
             "Sets how much of any proceeds is genuinely investable risk capital.", BADGE["missing"], "Household decision",
             a("investor", "Investor.gov")),
            ("What is the written investment policy for the proceeds?",
             "Without it, deployment becomes a market-timing decision made under stress.", BADGE["missing"], "Household + adviser",
             a("investor", "Investor.gov") + " · " + a("sipc", "SEC investor publications")),
            ("Is a phased entry wanted, and with what pre-committed trigger and end date?",
             "The replay shows phasing usually costs money and only wins in genuine crashes, so it must be a deliberate rule.", BADGE["protocol"], "Household decision",
             '<a href="crash-replay.html">Crash-entry replay</a>'),
            ("Is a like-kind exchange wanted, and is the property eligible?",
             "Must be decided before closing, with a qualified intermediary.", BADGE["unverified"], "CPA + attorney",
             a("irs_1031", "IRS 1031")),
            ("What is the plan if a sale is needed in a down market?",
             "Distinguishes a plan that survives a crash from one that depends on a good exit price.", BADGE["missing"], "Household decision",
             a("nber", "NBER cycle dates")),
        ],
    }

    sections = []
    for i, (name, rows) in enumerate(groups.items(), start=1):
        sections.append(
            section(f"{i:02d}", "OPEN ITEMS", name,
                    "Status, the person who can close it, and the official starting point.",
                    table(["Question that must be answered", "Why it changes the decision", "Status", "Who closes it", "Official starting point"], rows))
        )

    discover = [
        ("Buy the evidence instead of estimating it", "Order the appraisal, the rent opinion, the inspection, the insurance quotes and the title/escrow estimate as a single paid package, and make each one answer the gate it belongs to.",
         "Appraisal, rent opinion, inspection, quotes", BADGE["protocol"], a("cslb", "CSLB")),
        ("Read the documents already in hand", "The trust instrument, the current leases, the last three tax returns, the property tax bills and the insurance declarations page answer many of these questions at zero cost.",
         "Documents the household already holds", BADGE["protocol"], a("irs_551", "Pub 551")),
        ("Ask the assessor in writing", "A written response oneligible-transferee status, tax rate area and reassessment basis is more useful than any model.",
         "Written assessor response", BADGE["protocol"], a("scc_assessor", "SCC Assessor")),
        ("Ask the county for the rate book entry", "The controller publishes rates by tax rate area every fiscal year; the entry plus the parcel bill is the whole property-tax picture.",
         "Published rate for the parcel's area", BADGE["protocol"], a("scc_ratebook", "SCC rate book")),
        ("Commission a downside case, not a forecast", "Ask an adviser to price the scenario where the exclusion fails, insurance costs double, and a capital project lands in year two.",
         "Written downside case", BADGE["protocol"], a("ins", "CA Dept. of Insurance")),
        ("Set a date for each answer", "An unanswered question without a deadline is a decision made by default.",
         "Calendar with owners", BADGE["protocol"], '<a href="war-room.html#journal">Journal</a>'),
        ("Keep the private material private", "Inventories, parcel numbers, appraisals and leases belong outside this repository and outside any public site.",
         "Private, encrypted storage", BADGE["protocol"], a("ftc", "FTC privacy guidance")),
    ]

    body = (
        '<div class="decision-state"><span class="state-icon">!</span><div><strong>Thirty-eight questions, nine of them blocking.</strong>'
        "<p>The blocking items are grouped first. Nothing on this site fills any of them in: where a value is unknown the cell says so rather than "
        "showing an estimate that would later be mistaken for evidence.</p></div></div>"
        + "".join(sections)
        + section("09", "DISCOVERY", "How to find the missing information",
                  "A question is only open until someone is given the job of closing it.",
                  table(["Method", "What it produces", "Artifact", "Status", "Starting point"], discover))
    )
    return page(
        "questions.html",
        "Questions and missing information",
        "EVIDENCE GAPS · NOTHING INFERRED",
        "Every question that has to be answered before a decision is real.",
        "Grouped by the part of the decision it controls. Each row carries its status, the person who can close it, and the official page to start from.",
        body,
    )


# ============================================================= comparison =====
def build_comparison() -> str:
    paths = [
        ("1", "Live in the inherited home",
         "Occupy it as the primary residence for the whole horizon; carry all costs; no rent paid.",
         "Same start, same end. Asset retained; costs paid; imputed rent credited as a non-cash benefit.",
         "Prop 19 occupancy conditions must be met and sustained; if they are not, reassessment lands on this path hardest.",
         "Low — one illiquid asset and no diversification.",
         "Carrying costs, capital events, insurability, concentration.",
         '<a href="comparison.html#calculator">Calculator</a> · ' + a("rtc632", "RTC 63.2")),
        ("2", "Rent it out, keep owning",
         "Let the home at market rent; the household lives elsewhere.",
         "Same start, same end. Rent net of vacancy, management, costs and tax.",
         "Without occupancy the exclusion does not apply, and rented years create depreciation and recapture.",
         "Medium — sellable but slow and illiquid during a downturn.",
         "Tenant, vacancy, regulation, capital calls, recapture at exit.",
         '<a href="comparison.html#calculator">Calculator</a> · ' + a("irs_527", "IRS Pub 527")),
        ("3", "Sell now, invest the proceeds",
         "Sale in the same tax year as the inheritance, then immediate deployment according to a written policy.",
         "Same start, same end. Net proceeds after sale costs, gain tax and the California 1% above $1M.",
         "A same-year sale is the base case; it is also the path most sensitive to the sale-year income stack.",
         "High — divisible, diversified, immediately available.",
         "Sequence of returns at entry; loss of the property; tax concentration in one year.",
         '<a href="comparison.html#calculator">Calculator</a> · ' + a("rtc17043", "RTC 17043")),
        ("4", "Sell, park in Treasuries, phase into equities",
         "Sale first, then a Treasury bill ladder for 24–36 months, then equal monthly equity purchases over 24–36 months.",
         "Same start, same end. Full exposure is delayed by the parking plus phase-in window.",
         "Tax is incurred at sale exactly as in path 3; only the deployment schedule differs.",
         "High after the phase-in; deliberately idle during it.",
         "Cash drag and reinvestment risk, traded against lower crash-entry risk.",
         '<a href="crash-replay.html">Crash replay</a> · ' + a("tbill", "Treasury bills")),
        ("5", "Live in it, then sell",
         "Occupy for a defined period, then sell and invest.",
         "Same start, same end. Carrying costs and imputed rent for the occupancy years, then net proceeds invested.",
         "Section 121 requires two years of ownership and use out of five, so a short stay may not qualify. Prop 19 occupancy rules interact.",
         "Low during occupancy, high afterwards.",
         "Exit price risk is postponed, not removed; eligibility must be genuine.",
         '<a href="comparison.html#calculator">Calculator</a> · ' + a("irs_t701", "IRS Topic 701")),
        ("6", "Rent it out, then sell",
         "Hold for income for a defined period, then sell and reinvest.",
         "Same start, same end. Net rent during the hold, then after-tax proceeds invested.",
         "Rented years build depreciation that is recaptured on sale, and the Prop 19 exclusion is not available without occupancy.",
         "Low until the sale.",
         "Tenant and exit risk together; the classic forced-sale scenario.",
         '<a href="comparison.html#calculator">Calculator</a> · ' + a("irs_544", "IRS Pub 544")),
        ("7", "Keep part, sell part",
         "Retain a chosen share for living or letting and sell the rest.",
         "Same start, same end. Each component carries its own costs, valuation and tax treatment.",
         "A partial sale needs its own appraisal, title work and cost allocation.",
         "Mixed.",
         "Complexity and cost allocation disputes; it can also be the honest answer when the household is split.",
         '<a href="comparison.html#calculator">Calculator</a> · ' + a("irs_551", "Pub 551")),
        ("8", "Defer with a like-kind exchange",
         "Sell investment real property and acquire replacement investment real property through a qualified intermediary.",
         "Not comparable on the same cash horizon; it defers rather than realises gain.",
         "A personal residence does not qualify. Only business or investment real property is eligible, and the decision must precede closing.",
         "Low — replacement property is equally illiquid.",
         "Execution risk, timing rules and leverage; inappropriate as a rescue after a sale has been agreed.",
         a("irs_1031", "IRS 1031")),
    ]
    path_table = table(
        ["#", "Path", "What it means", "Measured how (identical dates and horizon)", "Tax and eligibility conditions",
         "Liquidity", "Main risk", "Anchor"],
        paths,
    )

    reinvest = [
        ("Cash drag during the parking window",
         "Treasury bills returned roughly 0–14% nominal in the historical record, while equities compounded far more over the same decades. Every month parked is a month of forgone equity exposure.",
         "Median ten-year outcome of the 24-month park + 36-month phase-in was −74.9 points of starting value versus immediate investing.",
         '<a href="crash-replay.html">Crash replay</a> · ' + a("treasury", "Treasury rates")),
        ("Reinvestment risk at each maturity",
         "A bill ladder resets at unknown future yields. If short rates fall, later tranches lock in lower returns; if they rise, the ladder is a benefit.",
         "Modelled as three cases: 0% while parked, historical bill returns, and (as an upper bound) the equity return on idle cash. The ranking did not flip.",
         '<a href="crash-replay.html#sensitivity">Sensitivity</a> · ' + a("treasury", "Daily Treasury rates")),
        ("Delay to full exposure",
         "The plan is not fully invested until the parking and phase-in months have elapsed, so it misses any early recovery by construction.",
         "A 2008 entry at ten years finished behind: phasing −24.2 points. A 2020 entry finished well behind because the recovery was immediate.",
         '<a href="crash-replay.html#episodes">Episodes</a> · ' + a("nber", "NBER dates")),
        ("The protection is real but narrow",
         "Phasing only wins when the crash arrives early in the window. That is exactly the scenario it is bought for — and the reason it must be pre-committed rather than improvised.",
         "Best historical window: 1929 entry, +107.9 points at ten years. Wins overall: 15.7% of ten-year windows.",
         '<a href="crash-replay.html">Crash replay</a>'),
        ("Behavioural risk in both directions",
         "A rule that is abandoned during a drawdown is worse than either pure policy, because it converts a plan into a reaction.",
         "Write the tranche dates, the acceleration trigger and the end date before the sale closes.",
         '<a href="war-room.html#precommit">Pre-commitment</a> · ' + a("investor", "Investor.gov")),
    ]
    reinvest_table = table(
        ["Reinvestment risk", "What it is", "What the evidence shows", "Where it is modelled"],
        reinvest,
    )
    for r in reinvest_table:
        pass

    inputs = [
        ("horizon", "Years to compare (same for every path)", "number", "1", "50", "1"),
        ("value", "Inherited home value at transfer ($)", "number", "0", "", "10000"),
        ("basis", "Date-of-death basis ($) — leave blank to assume equal to value", "number", "0", "", "10000"),
        ("saleCostPct", "Sale costs excluding tax (% of price)", "number", "0", "10", "0.25"),
        ("appLow", "Home appreciation, low (%/yr)", "number", "-2", "10", "0.25"),
        ("appHigh", "Home appreciation, high (%/yr)", "number", "-2", "10", "0.25"),
        ("rentLow", "Market rent, low ($/month)", "number", "0", "", "100"),
        ("rentHigh", "Market rent, high ($/month)", "number", "0", "", "100"),
        ("imputedRent", "Imputed rent credited to living paths ($/month)", "number", "0", "", "100"),
        ("propTax", "Annual property tax ($)", "number", "0", "", "100"),
        ("insurance", "Annual insurance ($)", "number", "0", "", "100"),
        ("utilities", "Annual net utilities paid by owner ($)", "number", "-2000", "", "50"),
        ("maint", "Routine maintenance (% of value/yr)", "number", "0", "3", "0.1"),
        ("capitalReserve", "Capital reserve (% of value/yr)", "number", "0", "3", "0.1"),
        ("vacancyPct", "Vacancy and management allowance (% of rent)", "number", "0", "30", "1"),
        ("inflPct", "Inflation (%/yr)", "number", "0", "12", "0.1"),
        ("retLow", "Investment return, low (%/yr nominal)", "number", "-5", "15", "0.25"),
        ("retHigh", "Investment return, high (%/yr nominal)", "number", "-5", "15", "0.25"),
        ("taxDragPct", "Annual portfolio tax drag (%/yr)", "number", "0", "3", "0.1"),
        ("treasuryPct", "Treasury bill yield while parked (%/yr)", "number", "0", "15", "0.1"),
        ("parkMonths", "Months fully parked in bills", "number", "0", "60", "6"),
        ("phaseMonths", "Months over which equities are bought", "number", "0", "60", "6"),
        ("otherCaIncome", "Other California taxable income in the sale year ($)", "number", "0", "", "10000"),
        ("gainTaxPct", "Combined tax rate on the gain, excluding the CA 1% above $1M (%)", "number", "0", "45", "1"),
        ("reserve", "Reserve withheld from proceeds, not invested ($)", "number", "0", "", "10000"),
    ]
    labels = []
    for fid, label, typ, mn, mx, step in inputs:
        attrs = f'type="{typ}" id="{fid}" step="{step}"'
        if mn != "":
            attrs += f' min="{mn}"'
        if mx != "":
            attrs += f' max="{mx}"'
        labels.append(f'<label>{label}<input {attrs} placeholder="Private input"></label>')
    form = (
        '<form id="calcForm" autocomplete="off"><div class="input-grid">'
        + "".join(labels)
        + '</div><div class="form-actions"><button class="button" type="submit">Compare these assumptions</button>'
        '<button class="button button-secondary" type="reset">Clear</button>'
        '<span id="calcStatus" role="status" aria-live="polite">No inputs yet.</span></div></form>'
        '<div id="calcOut" class="results-panel" hidden>'
        '<p id="calcRank" class="callout"></p>'
        '<div class="table-wrap"><table><thead><tr><th>Path</th><th>Low case</th><th>Base case</th><th>High case</th>'
        '<th>Real (inflation-adjusted) range</th><th>Liquidity</th><th>Main risk</th></tr></thead>'
        '<tbody id="calcRows"></tbody></table></div>'
        '<p class="source-note">Low / base / high each apply the low, midpoint and high assumptions together; this is a range display, not a probability. '
        'Currency is rounded to the nearest $10. The model excludes depreciation and recapture, Proposition 19 assessment changes, insurance repricing, '
        'debt, trust terms, and any asset other than the inherited home. Every one of those can reorder the table.</p></div>'
        '<script src="calculator.js"></script>'
    )

    body = (
        '<div class="callout"><strong>Everything on this page is a protocol, not a projection.</strong> No value, rent or tax figure for either property '
        'is published anywhere on this site. The comparison defines what has to be measured, on what dates, and what is deliberately left out; the '
        'calculator performs the arithmetic only after you supply private inputs in your own browser.</div>'
        + section("01", "PATHS", "All eight choices, on identical dates and horizons",
                  "Including the mixed paths and the exchange option, so no option is compared on a different calendar.",
                  path_table) + '<div id="mixed"></div>'
        + section("02", "REINVESTMENT RISK", "What the staged path costs, next to what it buys",
                  "Every headline about lower crash-entry risk sits beside the price of holding cash.",
                  reinvest_table) + '<div id="sensitivity"></div>'
        + section("03", "CALCULATOR", '<span id="calculator"></span>Run your own numbers — nothing leaves this browser',
                  "Blank by design. Fill only what you can evidence; leave the rest blank and treat the output as incomplete.",
                  '<div class="privacy-callout"><span aria-hidden="true">◆</span><div><strong>Browser-only</strong>'
                  "<p>No network requests, no storage, no cookies, no analytics, no remote scripts. Refreshing the page clears every field. "
                  "Do not type names, addresses or account numbers.</p></div></div>" + form)
        + section("04", "WHAT WOULD BREAK THIS", "Four assumptions that can move the answer most",
                  "Ranked by how much damage a wrong value does.",
                  table(["Assumption", "Why it dominates", "What to do instead", "Anchor"], [
                      ("Prop 19 applicability", "It changes the annual carrying cost of every hold path for as long as the home is held.",
                       "Get a written assessor and attorney answer before modelling a hold.",
                       a("rtc632", "RTC 63.2")),
                      ("Date-of-death value and basis", "It sets the sale tax, the estate return and the assessment calculation at once.",
                       "Commission a retrospective appraisal tied to the date of death.",
                       a("irs_551", "Pub 551")),
                      ("Evidenced market rent", "It decides whether the rent path competes at all.",
                       "Obtain a licensed rent opinion and comparable leases.",
                       a("sf_rent", "Rent rules")),
                      ("Insurance and capital condition", "One event can exceed several years of net rent, and cover may be unavailable.",
                       "Written quotes plus an inspection-based five-year capital plan.",
                       a("ins", "CA Dept. of Insurance")),
                  ]))
    )
    return page(
        "comparison.html",
        "Compare every path",
        "EIGHT PATHS · ONE CALENDAR · RISK SHOWN BESIDE RETURN",
        "Compare all choices at the same dates, with the risks attached.",
        "Living, renting, selling, splitting, staging, deferring — measured at one shared start and one shared end, with taxes, costs, occupancy, "
        "capital costs and liquidity stated for each. Mixed paths sit beside the pure ones because the honest answer is often a mixture.",
        body,
    )


# ============================================================= suggestions =====
def build_suggestions() -> str:
    items = [
        ("S1", "Make the first screen answer &ldquo;what would change the answer?&rdquo;",
         "Nine gates with the consequence of each answer, the status, and the person who can close it.",
         "A reader can name the three facts that block a decision within thirty seconds of landing.",
         "Done", "High", '<a href="war-room.html">War room</a>'),
        ("S2", "Replace round-number assumptions with ranges",
         "Every estimate is entered as a low/high pair; the calculator reports a range and never a single point.",
         "No page shows one number where the evidence supports only a band.", "Partly done", "High",
         '<a href="comparison.html#calculator">Calculator</a>'),
        ("S3", "Test the phased-investing idea against real history rather than intuition",
         "Replay every historical start date for lump sum versus 24–36 months of bills then a 24–36 month phase-in.",
         "A stated win rate, a median cost, and the episodes where it wins and loses.", "Done", "High",
         '<a href="crash-replay.html">Crash replay</a>'),
        ("S4", "Show reinvestment risk next to every staged headline",
         "Cash drag, reinvestment yield, delay to full exposure and behaviour risk are reported with the result, not after it.",
         "No staged figure appears without its cost.", "Done", "High",
         '<a href="crash-replay.html#how-to-use">Reinvestment risk</a>'),
        ("S5", "Model mixed paths beside the pure choices",
         "Live-then-sell, rent-then-sell, keep-half and staged deployment all appear in the same comparison at the same dates.",
         "A reader can see that the best option may be a combination.", "Done", "High",
         '<a href="comparison.html#mixed">Mixed paths</a>'),
        ("S6", "Separate estate tax, income-tax basis and property-tax assessment",
         "Three columns, three clocks, three citations — never one blended &ldquo;tax&rdquo; line.",
         "No reader confuses assessed value with basis or basis with market value.", "Done", "High",
         a("irs_706", "Form 706") + " · " + a("irs_551", "Pub 551") + " · " + a("boe_pub29", "Pub 29")),
        ("S7", "Put a market rent on the inherited home",
         "Rent stays blank until a licensed opinion and comparable leases exist; the calculator accepts a low/high band only.",
         "The rent path is either evidenced or visibly marked unverified.", "Blocked on evidence", "High",
         '<a href="questions.html">Questions</a>'),
        ("S8", "Build a five-year maintenance and capital plan for both buildings",
         "The calculator separates routine maintenance from capital reserve; the plan itself must come from inspections and bids.",
         "A single capital event can be priced into every path.", "Blocked on evidence", "Medium",
         a("cslb", "CSLB")),
        ("S9", "Print a one-page brief for the attorney and the tax adviser",
         "A single page with facts, gates, the eight paths, and the exact questions to ask each professional.",
         "A meeting can start from one sheet instead of a dashboard tour.", "Done", "High",
         '<a href="brief.html">Briefing sheet</a>'),
        ("S10", "Show the deadlines as a timeline",
         "Process checkpoints from pre-transfer to annual review, each with its statutory anchor.",
         "No deadline is discovered after it has passed.", "Done", "High",
         '<a href="index.html#timeline">Timeline</a>'),
        ("S11", "Group the menu and add a glossary",
         "Navigation grouped Decide / Evidence / Act; a glossary of the eight terms that are most often confused.",
         "A first-time reader is not lost, and does not conflate basis with assessment.", "Done", "Medium",
         '<a href="index.html#glossary">Glossary</a>'),
        ("S12", "Distinguish enacted law from proposals",
         "Two separate registers with effective dates and official status pages, plus a dated recheck calendar.",
         "No proposal is silently baked into a projection.", "Done", "High",
         '<a href="law-watch.html">Law watch</a>'),
        ("S13", "Add a distribution chart rather than a single projection",
         "Ten-year real outcomes shown as percentiles and per-start-year bars.",
         "The reader sees the shape of the risk, not one CAGR.", "Done", "Medium",
         '<a href="crash-replay.html#distribution">Distribution</a>'),
        ("S14", "Add what-if controls",
         "A browser-only calculator with low/high inputs for every material assumption and no prefilled values.",
         "Sensitivity is explored without transmitting anything.", "Done", "High",
         '<a href="comparison.html#calculator">Calculator</a>'),
        ("S15", "Dedicate a page to suggestions so they can be reviewed before implementation",
         "This page, with acceptance criteria and status for each idea.",
         "A proposal can be judged on its own terms before it changes the site.", "Done", "Medium",
         '<a href="suggestions.html">Suggestions</a>'),
        ("S16", "Rebuild the model and the site after any input change",
         "Deterministic scripts plus a verifier that refuses to pass when it compares nothing.",
         "The published figures can never drift from the data.", "Done", "High",
         ext("https://github.com/kanlerxz87-cyber/TinoDash2/blob/main/scripts/verify_sources.py", "verify_sources.py")),
        ("S17", "Contain the prior public-data exposure",
         "Working tree is clean of household figures; history and closed pull-request refs still contain them.",
         "Repository-owner action: history purge, cache and index removal, fork review.", "Owner action", "Critical",
         '<a href="FLAGGED_FOR_REVIEW.html">Flagged for review</a>'),
        ("S18", "Add a private, offline estate inventory",
         "A structured template that never enters this repository: assets, values, basis, titling, beneficiaries, debts, insurance, documents.",
         "Estate questions can be answered from one private file.", "Not built (must stay private)", "High",
         a("ftc", "FTC privacy guidance")),
        ("S19", "Wire the replay into the calculator",
         "Let a user compare their own horizon against the historical distribution of windows of that length.",
         "Ranges and history land in the same view. Requires a generated distribution file and careful framing to avoid implying prediction.",
         "Proposed", "Medium", '<a href="crash-replay.html">Crash replay</a>'),
        ("S20", "Add a depreciation and recapture module",
         "CPA-grade schedule for rented years, with basis reduction and recapture on exit.",
         "The rent-then-sell path stops being optimistic. Requires professional sign-off before publication.",
         "Proposed (needs CPA)", "High", a("irs_527", "IRS Pub 527")),
        ("S21", "Add a per-start-year heat map",
         "Colour the full cohort grid so the reader can see clusters rather than reading a table.",
         "Faster recognition of which regimes phasing protects against.", "Proposed", "Low",
         '<a href="crash-replay.html#distribution">Distribution</a>'),
        ("S22", "Add an inflation-adjusted property-tax projection",
         "Model the assessed value under both Prop 19 outcomes and both inflation factors.",
         "The largest recurring cost becomes visible on every hold path. Blocked on the parcel&rsquo;s tax rate area.",
         "Blocked on evidence", "High", a("scc_ratebook", "SCC rate book")),
    ]
    tbl = table(
        ["#", "Suggestion", "What it changes", "How you would know it worked", "Status", "Impact", "Open it"],
        items,
    )

    criteria = table(["Criterion", "Question to ask before adopting", "Anchor"], [
        ("Does it change a decision?", "Would a reasonable reader choose differently because of it?", '<a href="war-room.html">Decision gates</a>'),
        ("Is it sourced?", "Does every figure trace to an official or clearly-labelled public source?", '<a href="law-watch.html">Law watch</a>'),
        ("Is it honest about uncertainty?", "Does it show a range and name what it excludes?", '<a href="crash-replay.html">Crash replay</a>'),
        ("Does it protect privacy?", "Does it avoid household figures, identifiers and third-party requests?", a("ftc", "FTC guidance")),
        ("Is it reproducible?", "Can someone else rebuild the number from the repository?", ext("https://github.com/kanlerxz87-cyber/TinoDash2", "Repository")),
        ("Does it stay readable?", "Can a non-specialist follow it in one pass?", '<a href="index.html#glossary">Glossary</a>'),
    ])

    body = (
        '<div class="callout"><strong>How to review this page.</strong> Each item states what it changes, how you would know it worked, and where it lives. '
        'Adopt, reject or defer each one; nothing here is presented as already decided.</div>'
        + section("01", "QUEUE", "Twenty-two reviewed improvements",
                  "Twenty-two proposals, their acceptance criteria, and whether they are built, blocked on evidence, or only proposed.",
                  tbl)
        + section("02", "ADMISSION TEST", "What a change has to pass before it goes on the site",
                  "Six criteria, applied to every item above.",
                  criteria)
    )
    return page(
        "suggestions.html",
        "Suggested improvements",
        "REVIEW QUEUE · ADOPT, REJECT OR DEFER",
        "Improvements, each with a test you can apply before adopting it.",
        "A standing queue so that ideas can be reviewed and selected deliberately rather than merged on impulse. Status reflects this build only.",
        body,
    )


# =================================================================== brief ====
def build_brief() -> str:
    facts = [
        ("Property A", "Inherited single-family home in Santa Clara County, California. Expected to transfer by trust in a future period; the exact date is unknown. No value, address or parcel number is printed here."),
        ("Property B", "San Francisco multi-unit building already owned by the prospective heir; partly rented, partly owner-occupied. No value, address, rent or unit-level terms are printed here."),
        ("The distinction that matters", "Property B is already owned and its property-tax base is established. Property A arrives with a date-of-death basis and a change-of-ownership assessment question. They must never be netted into one number."),
        ("Objective", "Choose between living in, renting, selling, splitting, staging or deferring, on after-tax, risk-adjusted grounds, with the reasoning written down before the figures arrive."),
    ]
    gates = [
        ("G1", "Eligible transferee and principal-residence status", a("rtc632", "RTC 63.2")),
        ("G2", "Occupancy within one year and exemption filed", a("rtc632", "RTC 63.2(a)(1)(B)")),
        ("G3", "Date-of-death fair market value and land/improvement split", a("irs_551", "IRS Pub 551")),
        ("G4", "Estate size, prior taxable gifts, portability", a("irs_706", "Form 706")),
        ("G5", "Parcel tax rate area and published rate", a("scc_ratebook", "SCC rate book")),
        ("G6", "Evidenced market rent", a("sf_rent", "Rent rules")),
        ("G7", "Insurance quotes and insurability", a("ins", "CA Dept. of Insurance")),
        ("G8", "Five-year capital plan", a("cslb", "CSLB")),
        ("G9", "Same-tax-year sale computation and exchange decision", a("rtc17043", "RTC 17043") + " · " + a("irs_1031", "1031")),
    ]
    paths = [
        ("Live in it", "asset retained, costs paid, imputed rent credited", "Prop 19 conditions must hold", "Low", a("rtc632", "RTC 63.2")),
        ("Rent it out", "net rent after vacancy, costs and tax", "no exclusion without occupancy; recapture", "Medium", a("irs_527", "Pub 527")),
        ("Sell now, invest", "net proceeds after costs, gain tax and CA 1% above $1M", "sale-year income stack", "High", a("rtc17043", "RTC 17043")),
        ("Sell, park, phase in", "same proceeds, delayed exposure", "cash drag and reinvestment risk", "High after phase-in", '<a href="crash-replay.html">Replay</a>'),
        ("Live then sell", "costs and imputed rent, then proceeds invested", "Section 121 two-of-five tests", "Low → High", a("irs_t701", "Topic 701")),
        ("Rent then sell", "net rent, then proceeds invested", "depreciation and recapture", "Low until sale", a("irs_544", "Pub 544")),
        ("Keep half, sell half", "each part priced separately", "partial valuation and allocation", "Mixed", a("irs_551", "Pub 551")),
        ("Like-kind exchange", "deferral, not a cash outcome", "investment property only; decide before closing", "Low", a("irs_1031", "IRS 1031")),
    ]
    questions_atty = [
        "Confirm the eligible-transferee relationship, the principal-residence history, and the trust&rsquo;s authority over occupancy, sale and distribution.",
        "State the one-year occupancy and exemption-filing obligations in writing, with the date they start.",
        "Confirm what the trust says about who may live there, for how long, and who pays for what.",
        "Advise on any exchange, sale restriction or beneficiary conflict before a listing is signed.",
        "Advise on estate liquidity if the estate may exceed the federal exclusion, and on the portability election.",
        "Review the San Francisco leases, lawful unit status and owner move-in consequences.",
    ]
    questions_cpa = [
        "Establish date-of-death basis and the consistent-basis statement; reconcile it to the estate return.",
        "Compute a same-tax-year sale first: federal gain, California gain, and the 1% additional tax above $1,000,000 of taxable income.",
        "Estimate the reassessed property tax under both Prop 19 outcomes, using the parcel&rsquo;s actual tax rate area.",
        "Rebuild depreciation allowed or allowable on the San Francisco property and model recapture on any sale.",
        "Model the rent path net of depreciation, and the living-then-selling path with Section 121 only if the tests are met.",
        "Price the transfer tax, recording fees and closing costs for the actual sale scenario.",
    ]
    body = (
        '<div class="brief-sheet" id="briefSheet">'
        '<div class="brief-top"><span>PRIVATE WORKING BRIEF · NO IDENTIFIERS</span><span>Prepared 25 November 2026 · re-date before use</span></div>'
        "<h1>Attorney &amp; CPA Briefing Sheet</h1>"
        '<p class="brief-lead">One page. Facts as they stand, the nine gates that decide the answer, the eight paths being compared, and the exact questions for each professional.</p>'
        '<div class="brief-columns">'
        "<div><h2>Facts as they stand</h2><ul>"
        + "".join(f"<li><strong>{k}:</strong> {v}</li>" for k, v in facts)
        + "</ul><h2>The nine gates</h2><ul>"
        + "".join(f"<li><strong>{g}</strong> {t} — {s}</li>" for g, t, s in gates)
        + "</ul></div><div><h2>Questions for the attorney</h2><ul>"
        + "".join(f"<li>{q}</li>" for q in questions_atty)
        + "</ul><h2>Questions for the CPA</h2><ul>"
        + "".join(f"<li>{q}</li>" for q in questions_cpa)
        + "</ul></div></div>"
        '<h2>Paths under comparison</h2>'
        + table(["Path", "Measured as", "Tax and eligibility condition", "Liquidity", "Anchor"],
                [(f"<strong>{p}</strong>", m, t, l, anchor) for p, m, t, l, anchor in paths])
        + '<h2>What the evidence already says about staged investing</h2>'
        '<p>Replaying 1928–2025, parking sale proceeds in Treasury bills for 24 months and then phasing into equities over 36 months beat immediate '
        'investing in 15.7% of ten-year windows, with a median shortfall of 74.9 points of starting value. It won decisively in a 1929 entry '
        '(+107.9 points) and lost in a 2020 entry (−60.1 points). Staging is a deliberate purchase of crash protection, not a free improvement, '
        'and should be pre-committed in writing or not used at all.</p>'
        '<div class="brief-bottom"><strong>Decision guardrail:</strong> agree in writing what evidence would favour each path before the figures arrive. '
        'Current law cannot be projected as certain for a transfer in 2040–2050, and no figure on this sheet is a valuation, a quote, or advice.</div>'
        "</div>"
        '<p class="source-note">Print with your browser; the page is laid out for one sheet at A4 or Letter. '
        'Official anchors: ' + a("irs_706", "IRS Form 706") + " · " + a("irs_551", "IRS Pub 551") + " · " + a("boe19", "BOE Prop 19") + " · "
        + a("ftb540_2025", "FTB Form 540") + " · " + a("sf_rent", "SF Rent Board") + ".</p>"
    )
    return page(
        "brief.html",
        "Attorney and CPA briefing sheet",
        "ONE PAGE · PRINTABLE · NO IDENTIFIERS",
        "Attorney &amp; CPA Briefing Sheet",
        "Hand this to counsel and to the tax adviser. It contains no household identifiers, no values and no estimates — only the facts as they stand, "
        "the questions that decide the outcome, and the paths being compared.",
        body,
    )


# ==================================================================== main ====

# ============================================================ worksheets =====
def build_worksheets() -> str:
    """Two blank worksheets: depreciation/recapture, and estate liquidity/portability.

    Both are deliberately empty. They publish the rule and the arithmetic so a CPA can
    fill them in with the household's own numbers, on paper or in the browser.
    """

    depr_rows = [
        ("Value of the improvements alone at the applicable starting point",
         "Depreciation applies to the building, never the land. Split the basis between land and improvements from the appraisal; the land share is not depreciable.",
         a("irs_527", "IRS Pub 527") + " · " + a("irs_551", "IRS Pub 551")),
        ("The correct starting value: inherited basis or carryover basis",
         "Inherited property generally starts at date-of-death fair market value; a gift, a trust with carryover basis, or a non-qualifying transfer does not. The wrong starting value misstates every later year.",
         a("irs_551", "IRS Pub 551") + " · " + a("irs_706", "Form 706")),
        ("Residential rental recovery period and convention",
         "Residential rental real property is recovered over 27.5 years, straight line, mid-month convention. Non-residential or mixed-use portions differ, which is why the allocation matters.",
         a("irs_4562", "Form 4562") + " · " + a("irs_527", "Pub 527")),
        ("Placed-in-service date when the home converts to a rental",
         "Depreciation starts when the property is ready and available for rent, not when the first tenant signs. Vacancy before that date is handled differently from vacancy after it.",
         a("irs_527", "Pub 527: placed in service")),
        ("Improvements capitalised, and repairs deducted",
         "A new roof, a system replacement or a structural repair is capitalised and recovered over time; routine maintenance is deducted. Misclassifying either side distorts current income and later recapture.",
         a("irs_527", "Pub 527: repairs vs improvements")),
        ("Depreciation actually allowed or allowable in every rental year",
         "Recapture is computed on the greater of allowed or allowable, so a year that was missed on the return is still recaptured. Reconstruct it from returns, not memory.",
         a("irs_523", "Pub 523: recapturing depreciation") + " · " + a("irs_4797", "Form 4797")),
        ("Section 121 exclusion available, and the depreciation carve-out inside it",
         "If the home later qualifies as a main home, the exclusion can still apply — but the depreciation taken after 1997 is not sheltered by it and is recaptured separately.",
         a("irs_t701", "Topic 701") + " · " + a("irs_523", "Pub 523")),
        ("Rate on unrecaptured section 1250 gain",
         "Unrecaptured section 1250 gain is taxed at a maximum 25% federal rate, separate from the 0/15/20% long-term capital-gain brackets, and California does not give it preferential treatment.",
         a("irs_409", "Topic 409") + " · " + a("ftb_capgain", "FTB: no CA preference")),
        ("State treatment of the recapture and of the remaining gain",
         "California conforms to the federal depreciation mechanics but has no capital-gain rate preference, so the state cost of a sale can be materially higher than a federal-only estimate suggests.",
         a("ftb_capgain", "FTB capital gains") + " · " + a("ftb540_2025", "2025 Form 540")),
        ("Suspended or passive losses released on sale",
         "Passive losses suspended in earlier years are generally released when the property is fully disposed of. That can offset part of the gain — or none of it, if the activity was never passive.",
         a("irs_527", "Pub 527") + " · " + a("irs_4797", "Form 4797")),
        ("The 1% California surtax on taxable income above $1,000,000",
         "A sale can push a single year over the threshold. The surtax applies to taxable income above the threshold, not to the gain as such, so the rest of the year's income matters.",
         a("rtc17043", "RTC 17043") + " · " + a("ftb540_2025", "Form 540 line 62")),
        ("Net investment income tax, where it applies",
         "A 3.8% surtax can apply to net investment income above the statutory threshold. Whether a particular sale is inside it depends on the year's income, not on the property.",
         a("irs_409", "Topic 409: NIIT")),
    ]

    liq_rows = [
        ("Aggregate gross estate, not just these two properties",
         "The estate tax question is asked at the level of the whole estate, including life insurance, retirement accounts, joint property, prior taxable gifts and business interests. Two houses alone do not answer it.",
         a("irs_706", "Form 706 instructions") + " · " + a("irs_estate", "IRS estate tax")),
        ("Whether a return is required at all",
         "For 2026 the basic exclusion is $15,000,000 per person. A return is required when the gross estate plus adjusted taxable gifts plus specific exemption exceeds that amount — but a return may still be worth filing to elect portability.",
         a("irs_706", "Form 706: who must file") + " · " + a("irs_excl", "IRS 2026 amount")),
        ("The nine-month clock, and the automatic six-month extension",
         "A Form 706 is due nine months after the date of death. Form 4768 carries an automatic six-month extension <em>to file</em>; an extension of time to <em>pay</em> under section 6161 is a separate, discretionary request on the same form.",
         a("irs_706", "Form 706: when to file") + " · " + a("irs_4768", "Form 4768")),
        ("Portability: what it is, and why a timely return matters",
         "Portability transfers a deceased spouse's unused exclusion to the survivor, but only if the estate elects it on a timely filed return. The election is not automatic.",
         a("irs_706", "Form 706: portability election")),
        ("Late portability, and its limits",
         "A surviving spouse may be able to obtain portability after the deadline under the revenue procedure that allows a late election up to the fifth anniversary of death, subject to its conditions.",
         a("irs_706", "Form 706: late portability")),
        ("Liquidity: which assets can actually pay a tax bill",
         "A house cannot pay an estate tax bill without being sold, borrowed against, or distributed in kind. Cash, marketable securities and life insurance are liquid; real property is not.",
         a("irs_estate", "IRS estate tax") + " · " + a("investor", "Investor.gov")),
        ("Deferral and installment options, and their eligibility conditions",
         "Closely held business interests can qualify for installment payment of estate tax over an extended period. Whether a rental property qualifies depends on the estate's composition, not on the owner's preference.",
         a("irs_706", "Form 706: section 6166")),
        ("Deductions and credits that reduce the bill",
         "Administration expenses, debts, charitable bequests, the marital deduction and state death-tax credits all change the number. California has no estate tax, but other states may.",
         a("irs_706", "Form 706: deductions") + " · " + a("sco_estate", "CA State Controller")),
        ("Basis consistency between the return and the heirs",
         "Heirs must use a basis consistent with the value reported on the estate return, and the executor must furnish the statement. An appraisal that is never filed is not automatically the basis.",
         a("irs_551", "Pub 551: consistent basis") + " · " + a("irs_706", "Form 706")),
        ("A reserve policy, written before the tax is due",
         "The plan should state how much cash or marketable securities stays liquid, who can authorise a sale, and what happens if a sale is needed in a bad market. That is a decision, not a projection.",
         a("investor", "Investor.gov") + " · " + a("tbill", "Treasury bills")),
    ]

    worksheet = (
        '<div class="callout" style="max-width:980px"><strong>How to use these two worksheets.</strong> '
        "They are empty on purpose. Each line names the rule, the official anchor, and the question a CPA or "
        "estate attorney has to answer. Fill them in privately, on paper or in a local copy; nothing here asks "
        "for, stores, or transmits a figure.</div>"
        + section(
            "01", "DEPRECIATION AND RECAPTURE",
            "The rent path creates a tax bill you cannot see until you sell",
            "Every year of rental produces a deduction now and a recapture liability later. Both sides have to be in the same comparison or the rent path looks better than it is.",
            table(["Line", "What the rule says", "Official anchor"], [
                (f"<strong>{i+1}. {q}</strong>", why, src) for i, (q, why, src) in enumerate(depr_rows)
            ]),
        )
        + section(
            "02", "ESTATE LIQUIDITY AND PORTABILITY",
            "A tax bill is a cash problem before it is a tax problem",
            "The estate question is asked once, at death, across everything. The liquidity question is asked on the same day, and it is the one that forces sales.",
            table(["Line", "What the rule says", "Official anchor"], [
                (f"<strong>{i+1}. {q}</strong>", why, src) for i, (q, why, src) in enumerate(liq_rows)
            ]),
        )
        + section(
            "03", "WHAT THESE WORKSHEETS DO NOT DO",
            "No number, no projection, no ranking",
            "A worksheet is a checklist of rules, not a tax computation. The arithmetic depends on facts that are not public and must not be.",
            table(["Limitation", "Why it is deliberate", "What would close it"], [
                ("No dollar figures are published",
                 "Any household value, even rounded, is traceable through county records. Publishing it would breach the repository's privacy policy.",
                 "A CPA completes the worksheet privately and returns a reviewed estimate. See also "
                 + a("irs_551", "Pub 551") + " and " + '<a href="FLAGGED_FOR_REVIEW.html">flagged items</a>.'),
                ("No depreciation schedule is assumed",
                 "The recovery period, the placed-in-service date and the improvement/land split all change the answer, and all three are facts about one property.",
                 a("irs_527", "Pub 527") + " · an appraisal that splits land from improvements"),
                ("No estate-tax liability is estimated",
                 "The 2026 exclusion is $15,000,000 per person, which is an anchor, not a forecast of the law at the relevant date, and not a statement about this estate.",
                 a("irs_706", "Year-of-death Form 706 instructions")),
                ("No state estate tax is assumed",
                 "California requires no estate return for deaths after 2004 under current law; residence, situs of property, and future law can change that.",
                 a("sco_estate", "CA State Controller")),
                ("No portability outcome is predicted",
                 "Portability depends on a timely election, a surviving spouse, and the deceased spouse's remaining exclusion — all facts outside a public page.",
                 a("irs_706", "Form 706: portability")),
            ]),
        )
        + section(
            "04", "ORDER OF OPERATIONS",
            "Do these in this order, not in the order they become urgent",
            "Most expensive mistakes in an inherited-property decision come from doing the arithmetic before the facts, or the sale before the tax.",
            table(["Step", "Action", "Why it comes here", "Anchor"], [
                ("1", "Fix the date-of-death value and the land/improvement split",
                 "It sets basis, the estate return, the Prop 19 calculation and every later gain figure. Everything downstream moves if this is wrong.",
                 a("irs_551", "Pub 551")),
                ("2", "Determine whether a Form 706 is required or merely advisable",
                 "The nine-month clock starts at death, not at the decision. Portability can be lost by inaction.",
                 a("irs_706", "Form 706")),
                ("3", "Build the household's liquidity need before deciding on the house",
                 "The reserve requirement can rule out a hold path regardless of its projected return.",
                 a("investor", "Investor.gov")),
                ("4", "Compute the rent path with depreciation and recapture in the same column",
                 "A pre-tax rent comparison systematically overstates the rent path.",
                 a("irs_527", "Pub 527")),
                ("5", "Only then compare the paths on identical dates",
                 "With the first four settled, the comparison page becomes usable rather than decorative.",
                 '<a href="comparison.html">Comparison</a> · ' + a("irs_706", "Form 706")),
            ]),
        )
    )

    return page(
        "worksheets.html",
        "Depreciation, recapture, estate liquidity and portability worksheets",
        "TWO BLANK WORKSHEETS · RULES AND ANCHORS ONLY · NO HOUSEHOLD FIGURES",
        "The two tax questions that decide the answer, as blank worksheets.",
        "Rent builds a recapture liability you only meet at sale; the estate builds a cash requirement you "
        "only meet at death. Both are checklists of law here, not numbers. A CPA fills them in privately.",
        worksheet,
    )



BUILDERS = {
    "worksheets.html": build_worksheets,
    "war-room.html": build_war_room,
    "law-watch.html": build_law_watch,
    "questions.html": build_questions,
    "comparison.html": build_comparison,
    "suggestions.html": build_suggestions,
    "brief.html": build_brief,
}


def main():
    for name, fn in BUILDERS.items():
        html = fn()
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"wrote {name} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
