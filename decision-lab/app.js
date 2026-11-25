import {
  SOURCES,
  REVIEW_DATE,
  MODEL_VERSION,
  PATHS,
  QUESTIONS,
  LEGAL_ROWS,
  TIMELINE,
  SUGGESTIONS,
  FLAGS,
  GLOSSARY,
} from "./data.js";
import {
  defaultInputs,
  rangeComparison,
  comparisonMatrix,
  scenarioDistribution,
  sensitivityRows,
  money10,
  RANGE_DEFS,
  CURRENT,
  CAPITAL_PLAN,
  saleQuote,
  propH,
  bhTax,
  bhIncrement,
} from "./model.js";
import { SCENARIOS } from "./economy.js";
import { crashComparison } from "./crash.js";
const $ = (s, r = document) => r.querySelector(s),
  $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const money = (n) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(money10(n));
const compact = (n) =>
  Math.abs(n) >= 1e6
    ? `${n < 0 ? "−" : ""}$${(Math.abs(n) / 1e6).toFixed(2)}m`
    : money(n);
const pct = (n, d = 1) => `${(n * 100).toFixed(d)}%`,
  pathName = (id) => PATHS.find((p) => p.id === id)?.name ?? id,
  pathShort = (id) => PATHS.find((p) => p.id === id)?.short ?? id;
const utcDate = () => new Date().toISOString().slice(0, 10);
const icon = (id, size = 20) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${
    {
      overview:
        '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
      summary: '<path d="M8 3h9l4 4v14H3V3h5M14 3v6h7M7 13h10M7 17h7"/>',
      questions:
        '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 4 2c-1 .6-1.5 1-1.5 2.5M12 17h.01"/>',
      compare: '<path d="M4 7h16m-4-4 4 4-4 4M20 17H4m4-4-4 4 4 4"/>',
      projections: '<path d="M3 3v18h18M6 15l5-5 4 3 6-8"/>',
      swan: '<path d="M3 18h18M5 18l4-9 4 5 4-11 3 15M17 3h3M17 3v3"/>',
      taxes: '<path d="M4 21h16M6 21V9m6 12V9m6 12V9M3 8l9-5 9 5H3Z"/>',
      timeline:
        '<path d="M7 3v18M12 5h9M12 12h7M12 19h9"/><circle cx="7" cy="5" r="2"/><circle cx="7" cy="12" r="2"/><circle cx="7" cy="19" r="2"/>',
      planning:
        '<path d="M3 10l9-7 9 7v11H3V10ZM9 21v-8h6v8M7 10h.01M17 10h.01"/>',
      suggestions: '<path d="M8 15a7 7 0 1 1 8 0l-1 3H9l-1-3ZM9 21h6"/>',
      sources: '<path d="M8 4H3v16h18V4h-5M8 3h8v4H8zM7 12h10M7 16h7"/>',
      glossary:
        '<path d="M12 5c-3-2-6-2-9-1v16c3-1 6-1 9 1 3-2 6-2 9-1V4c-3-1-6-1-9 1Zm0 0v16"/>',
      briefing:
        '<path d="M7 8V3h10v5M7 16H3V8h18v8h-4M7 13h10v8H7zM17 11h.01"/>',
      privacy:
        '<path d="M12 3 3 7v5c0 5 9 9 9 9s9-4 9-9V7l-9-4Z"/><path d="m8 12 3 3 5-6"/>',
      flagged: '<path d="m12 3 10 18H2L12 3ZM12 9v5M12 17h.01"/>',
      arrow: '<path d="M5 12h14m-6-6 6 6-6 6"/>',
      external: '<path d="M14 3h7v7m0-7L10 14M10 3H3v18h18v-7"/>',
      controls:
        '<path d="M4 7h16M4 17h16"/><circle cx="8" cy="7" r="3"/><circle cx="16" cy="17" r="3"/>',
      chevron: '<path d="m9 5 7 7-7 7"/>',
      download: '<path d="M12 3v12m-5-5 5 5 5-5M3 16v5h18v-5"/>',
      menu: '<path d="M3 6h18M3 12h18M3 18h18"/>',
      close: '<path d="m5 5 14 14M19 5 5 19"/>',
    }[id] ?? '<circle cx="12" cy="12" r="8"/>'
  }</svg>`;
const sourceLinks = (keys, model = false) =>
  `<span class="source-cell">${model ? '<span class="model-tag">Synthetic · derived</span>' : ""}${keys.map((k) => `<a href="${SOURCES[k].url}" target="_blank" rel="noopener noreferrer" title="${esc(SOURCES[k].scope)}">${esc(SOURCES[k].name)} ${icon("external", 11)}</a>`).join("")}</span>`;
const table = (headers, rows, caption = "") =>
  `<div class="table-scroll" tabindex="0" role="region" aria-label="${esc(caption || headers.join(", "))}"><table>${caption ? `<caption>${caption}</caption>` : ""}<thead><tr>${headers.map((x) => `<th scope="col">${x}</th>`).join("")}</tr></thead><tbody>${rows.map((cells) => `<tr>${cells.map((x, j) => (j === 0 ? `<th scope="row">${x}</th>` : `<td>${x}</td>`)).join("")}</tr>`).join("")}</tbody></table></div>`;
const badge = (text, tone = "neutral") =>
  `<span class="badge ${tone}">${esc(text)}</span>`;
const pageHead = (eyebrow, title, desc, actions = "") =>
  `<div class="page-heading"><div><p class="eyebrow">${eyebrow}</p><h1 id="page-title" tabindex="-1">${title}</h1><p class="page-description">${desc}</p></div>${actions ? `<div class="heading-actions">${actions}</div>` : ""}</div>`;
const notice = (title, body, tone = "sage") =>
  `<div class="notice ${tone}">${icon(["amber", "danger"].includes(tone) ? "flagged" : "privacy", 20)}<div><strong>${title}</strong><p>${body}</p></div></div>`;
const btn = (label, href, extra = "") =>
  `<a class="button ${extra}" href="#${href}">${label} ${icon("arrow", 16)}</a>`;
const panel = (title, sub, body, extra = "") =>
  `<section class="panel ${extra}"><div class="panel-heading"><div><h2>${title}</h2>${sub ? `<p>${sub}</p>` : ""}</div></div>${body}</section>`;
let inputs = defaultInputs(),
  runNumber = 1,
  runMessage = "Defaults loaded · no private data required",
  comparison = rangeComparison(inputs),
  selectedPath = "sell",
  questionFilter = "All",
  sourceQuery = "",
  suggestionFilter = "All";
const decisions = new Map();
let distributionCache = "",
  distributionValues = [];
const groups = [
  {
    name: "Start here",
    items: [
      ["overview", "Overview", "overview"],
      ["summary", "Executive summary", "summary"],
      ["questions", "Decision questions", "questions"],
    ],
  },
  {
    name: "Explore the choices",
    items: [
      ["compare", "Compare paths", "compare"],
      ["projections", "Projections", "projections"],
      ["black-swan", "Black swan lab", "swan"],
    ],
  },
  {
    name: "Make a plan",
    items: [
      ["taxes", "Laws & taxes", "taxes"],
      ["timeline", "Deadlines & timeline", "timeline"],
      ["planning", "Buildings & liquidity", "planning"],
      ["suggestions", "Suggestions", "suggestions"],
    ],
  },
  {
    name: "Reference",
    items: [
      ["sources", "Official sources", "sources"],
      ["glossary", "Glossary", "glossary"],
      ["flagged", "Flagged for review", "flagged"],
      ["privacy", "Privacy & limits", "privacy"],
    ],
  },
];
const validRoutes = [
  "overview",
  "summary",
  "questions",
  "compare",
  "projections",
  "black-swan",
  "taxes",
  "timeline",
  "planning",
  "suggestions",
  "sources",
  "glossary",
  "flagged",
  "privacy",
  "briefing",
];
function route() {
  const r = location.hash.slice(1).split("?")[0] || "overview";
  return validRoutes.includes(r) ? r : "overview";
}
const leader = () => comparison[0].path;
const controlsButton = () =>
  `<button class="button secondary" data-action="controls">${icon("controls", 16)} What-if controls</button>`;
const modelDisclaimer = () =>
  `<div class="model-disclaimer">${icon("questions", 17)}<p><strong>Scenario, not advice.</strong> Property values, rents, costs, debt and returns here are synthetic. Official links support rules or methodology—not these inputs. Actual household fields remain blank; the illustrative ranking cannot select a household path.</p></div>`;
const metric = (label, value, note, tone = "") =>
  `<div class="metric ${tone}"><span>${label}</span><strong>${value}</strong><small>${note}</small></div>`;
function lineChart(
  series,
  { height = 250, label = "Modeled projection", format = compact } = {},
) {
  const width = 850,
    p = { l: 75, r: 20, t: 22, b: 34 },
    all = series.flatMap((s) => s.values);
  let min = Math.min(0, ...all),
    max = Math.max(...all);
  if (max === min) max = min + 1;
  const x = (j, n) => p.l + ((width - p.l - p.r) * j) / Math.max(1, n - 1),
    y = (v) => p.t + (height - p.t - p.b) * (1 - (v - min) / (max - min));
  const grid = Array.from({ length: 5 }, (_, j) => {
    const v = min + ((max - min) * j) / 4,
      yy = y(v);
    return `<line x1="${p.l}" x2="${width - p.r}" y1="${yy}" y2="${yy}" stroke="#e4e8e1" stroke-dasharray="3 4"/><text x="${p.l - 12}" y="${yy + 4}" text-anchor="end">${format(v)}</text>`;
  }).join("");
  const lines = series
    .map(
      (s) =>
        `<polyline points="${s.values.map((v, j) => `${x(j, s.values.length).toFixed(2)},${y(v).toFixed(2)}`).join(" ")}" fill="none" stroke="${s.color}" stroke-width="2.6" stroke-linejoin="round"/>`,
    )
    .join("");
  const labels = [0, 0.25, 0.5, 0.75, 1]
    .map(
      (f) =>
        `<text x="${p.l + (width - p.l - p.r) * f}" y="${height - 6}" text-anchor="middle">Year ${Math.round((series[0].values.length - 1) * (series[0].monthScale ? 1 / 12 : 1) * f)}</text>`,
    )
    .join("");
  return `<div class="chart-wrap"><svg class="line-chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(label)}"><title>${esc(label)}</title>${grid}${lines}${labels}</svg></div><div class="legend">${series.map((s) => `<span><i style="--swatch:${s.color}"></i>${esc(s.name)}</span>`).join("")}</div>`;
}
function histogram(values) {
  const min = values[0],
    max = values.at(-1),
    n = 12,
    bins = Array(n).fill(0);
  for (const v of values)
    bins[Math.min(n - 1, Math.floor(((v - min) / (max - min || 1)) * n))]++;
  const peak = Math.max(...bins),
    w = 850,
    h = 210,
    pad = 40,
    bw = (w - 2 * pad) / n;
  return `<svg class="histogram" viewBox="0 0 ${w} ${h}" role="img" aria-label="81 hypothetical grid outcomes, not probabilities"><title>81 equal-weight design points in 2026 dollars; not a probability model.</title>${bins.map((c, j) => `<rect x="${pad + j * bw + 3}" y="${h - 35 - (c / peak) * (h - 65)}" width="${bw - 6}" height="${(c / peak) * (h - 65)}" rx="4" fill="${j === 5 || j === 6 ? "#b3c578" : "#5e8875"}"/><text x="${pad + (j + 0.5) * bw}" y="${h - 42 - (c / peak) * (h - 65)}" text-anchor="middle">${c || ""}</text>`).join("")}<text x="${pad}" y="${h - 8}">${compact(min)}</text><text x="${w / 2}" y="${h - 8}" text-anchor="middle">2026 purchasing power · counts, not likelihood</text><text x="${w - pad}" y="${h - 8}" text-anchor="end">${compact(max)}</text></svg>`;
}
function overview() {
  const gates = QUESTIONS.filter((q) => q.status === "Gate").length,
    preview = comparison.filter((r) =>
      ["live", "rent", "sell", "staged"].includes(r.path),
    );
  return `${pageHead("A CLEARER WAY FORWARD", "An inheritance.<br><em>A considered decision.</em>", "Understand the choices, surface the unknowns, and build a plan you can explain.", `<a class="button secondary" href="#briefing">${icon("briefing", 16)} Professional brief</a>`)}
 <div class="overview-layout"><div class="hero-card"><div class="hero-top">${badge("PLANNING, NOT A FINAL RECOMMENDATION", "sage")}<span class="subtle">2040–2050 transfer window</span></div><h2>The right answer starts<br>with the right evidence.</h2><p>Live in A, rent it, sell it—or combine the paths. Compare the whole picture without letting one smooth forecast make the decision.</p><div class="property-pair"><div><span class="property-icon">${icon("planning", 25)}</span><div><small>PROPERTY A</small><strong>Future inheritance</strong><span>New transfer · trust review needed</span></div></div><span class="pair-plus">+</span><div><span class="property-icon pale">${icon("planning", 25)}</span><div><small>PROPERTY B</small><strong>Already owned</strong><span>Retained home & existing leases</span></div></div></div><div class="hero-footer"><span><i class="status-dot amber-dot"></i> No defensible household winner yet</span>${btn("See the decision questions", "questions", "text-button")}</div></div>
 <aside class="next-step"><div class="next-step-icon">${icon("questions", 24)}</div><p class="eyebrow">YOUR NEXT BEST STEP</p><h2>Close the evidence gaps.</h2><p>Before choosing a path, secure the facts that could reverse the answer.</p><ol><li><span>01</span> Written value & market-rent opinions</li><li><span>02</span> True tax rate, debt & capital plan</li><li><span>03</span> Genuine occupancy & estate review</li></ol><a href="#questions">Review ${gates} decision gates ${icon("arrow", 16)}</a></aside></div>
 <section class="change-section"><div class="section-heading"><div><p class="eyebrow">PUT UNCERTAINTY TO WORK</p><h2>What would change the answer?</h2></div><a href="#compare" class="text-link">Test the sensitivities ${icon("arrow", 16)}</a></div><div class="change-grid">${[
   [
     "01",
     "A’s net market rent",
     "Independent lease evidence could strengthen—or eliminate—the rental case.",
     "rental",
   ],
   [
     "02",
     "Where you want to live",
     "Long-term primary-residence intent determines whether Prop 19 is even relevant.",
     "prop19",
   ],
   [
     "03",
     "The cost of keeping both",
     "Reassessment, insurance, debt and major building work can outweigh gross rent.",
     "prop13",
   ],
   [
     "04",
     "Liquidity & entry risk",
     "Estate cash needs, a market crash or a missed rebound can favor different paths.",
     "bondRisk",
   ],
 ]
   .map(
     ([n, t, d, s]) =>
       `<article class="change-card"><span class="card-number">${n}</span><h3>${t}</h3><p>${d}</p>${sourceLinks([s])}</article>`,
   )
   .join("")}</div></section>
 <div class="stat-strip">${metric("Comparable paths", "07", "Includes four sequential strategies")}${metric("Common transfer dates", "03", "2040 · 2045 · 2050")}${metric("Projection range", "10–50 yrs", "Uneven nominal & real scenarios")}${metric("Private financial data", "None loaded", "Illustrations only—not a private vault")}</div>
 <div class="two-col unequal">${panel(
   "A first look at the trade-offs",
   "Illustrative wealth from A + cash flows. B retained, not liquidated.",
   lineChart(
     preview.map((r) => ({
       name: pathShort(r.path),
       color: PATHS.find((p) => p.id === r.path).color,
       values: r.rows.map((x) => x.real),
     })),
     {
       height: 240,
       label:
         "Synthetic realizable wealth in 2026 dollars, four selected paths",
     },
   ) +
     `<div class="panel-bottom">${btn("Compare all seven paths", "compare", "text-button")}<span class="subtle">No guaranteed returns</span></div>`,
 )}${panel(
   "Keep three tax questions separate",
   "A trust is not an automatic answer to all three.",
   `<div class="tax-lanes">${[
     ["Estate tax", "What does the decedent’s estate owe?"],
     ["Income-tax basis", "What gain arises on a later sale?"],
     ["Property assessment", "What annual tax base is enrolled?"],
   ]
     .map(
       ([t, d], j) =>
         `<a href="#taxes"><span>0${j + 1}</span><div><strong>${t}</strong><p>${d}</p></div>${icon("chevron", 16)}</a>`,
     )
     .join("")}</div>${sourceLinks(["estate", "basis", "prop19"])}`,
 )}</div>
 ${notice("Privacy is a prerequisite, not a rounding rule.", 'This module contains synthetic examples only. Broader repository exposure remains flagged; rounding or noindex does not erase public Git history. <a href="#privacy">See the containment status</a>.', "amber")}${modelDisclaimer()}`;
}
function summary() {
  return `${pageHead("EXECUTIVE SUMMARY", "The decision, in one view.", "What we can say now—and what must be established before a household recommendation.")}
 ${notice("Current conclusion: do the evidence work, not an irreversible transaction.", "There is no verified property valuation, rental evidence, parcel rate, trust analysis, debt payoff, capital plan or full estate inventory in this public-safe module. An automated illustrative ranking is not a household recommendation.", "amber")}
 <div class="three-col">${panel("A is inherited", "A new transfer is modeled.", `<p>Death-date valuation and tax inclusion control basis. A may be reassessed. A same-tax-year sale is the first exit comparison, not an assumption of zero tax.</p>${sourceLinks(["basis", "death", "prop19"])}`)}${panel("B is already owned", "B stays in every path.", `<p>Existing leases and separate owner space need private verification. Inheriting A creates no automatic B basis or assessment reset. Common retained B equity is not called after-tax liquidation wealth.</p>${sourceLinks(["basis", "leases"])}`)}${panel("Mix the choices", "No forced three-way choice.", `<p>Compare live/rent/sell with rent-then-sell, live-then-sell, live-then-rent and sell–park–phase. Include tax, depreciation, debt, capital work and liquidity at common dates.</p>${sourceLinks(["rental", "homeSale", "bondRisk"])}`)}</div>
 ${panel(
   "A disciplined order of operations",
   "Recommended sequence—not instructions to file or transact.",
   table(
     [
       "Order",
       "Action",
       "What establishes the answer",
       "Authority / methodology",
     ],
     [
       [
         "1",
         "Contain public exposure",
         "Administrator confirms visibility/artifacts; coordinate history, PR-ref and cache remediation.",
         sourceLinks(["github"]),
       ],
       [
         "2",
         "Agree the household rules in writing",
         "Document housing preference, net-rent hurdle, liquidity need and drawdown tolerance before new figures arrive.",
         sourceLinks(["prop19", "bondRisk"]),
       ],
       [
         "3",
         "Price same-tax-year sale",
         "Written death-date appraisal, trust basis review and seller net sheet, before judging long holds.",
         sourceLinks(["basis", "gains", "transfer"]),
       ],
       [
         "4",
         "Commission independent inputs",
         "Rent comps, inspections, insurance quotes, leases, tax bill/TRA and lender statements.",
         sourceLinks(["rental", "insurance", "tra", "leases"]),
       ],
       [
         "5",
         "Have attorney & CPA compare",
         "Estate-wide inventory, gifts/portability, tax-return-level flows and conditional claims.",
         sourceLinks(["estate", "form706", "form540"]),
       ],
       [
         "6",
         "Sign the path and investment policy",
         "Record decision, date, why, disconfirming evidence and annual review. No actual choice recorded here.",
         sourceLinks(["bills", "notes", "bondRisk"]),
       ],
     ],
   ),
 )}
 ${panel(
   "Conditional choice rules",
   "Proposals for the household to agree—not choices made on its behalf.",
   table(
     [
       "Path",
       "What would need to be true",
       "Status / reviewed",
       "Official context",
     ],
     PATHS.map((p) => [
       p.name,
       p.condition,
       `Not chosen<br><small>Reviewed ${REVIEW_DATE}</small>`,
       sourceLinks(p.sources),
     ]),
   ),
 )}
 ${notice("Illustrative result, clearly separated", `With the current synthetic controls, <strong>${pathName(leader())}</strong> ranks first by modeled realizable wealth. ${comparison.filter((r) => r.liquidityFlag).length} of seven example paths need external funding. Neither statement establishes a household winner. <a href="#compare">Inspect assumptions and reversals</a>.`)}${btn("Open the one-page professional brief", "briefing")}`;
}
function questions() {
  const list = QUESTIONS.filter(
    (q) => questionFilter === "All" || q.status === questionFilter,
  );
  return `${pageHead("DECISION READINESS", "Ask better questions first.", "Known context, missing facts, the person to ask, and a practical way to obtain each answer.")}
 <div class="filter-toolbar"><div class="segmented" role="group" aria-label="Question filter">${["All", "Gate", "Open", "Critical"].map((f) => `<button data-question-filter="${f}" aria-pressed="${questionFilter === f}">${f === "All" ? "All questions" : f === "Gate" ? "Decision gates" : f}</button>`).join("")}</div><span class="subtle">${list.length} items · actual evidence fields intentionally blank</span></div>
 ${list.map((q) => `<article class="question-card" id="${q.id}"><div class="question-top"><span class="eyebrow">${q.id} / ${q.group}</span>${badge(q.status, q.status === "Critical" ? "danger" : q.status === "Gate" ? "amber" : "neutral")}</div><h2>${q.question}</h2><div class="question-grid"><div><h3>What we know</h3><p>${q.known}</p><h3>Verified household answer</h3><p class="unknown-field"><span aria-label="Blank, unverified">—</span> Not verified · no value filled</p></div><div><h3>Still missing</h3><p>${q.missing}</p><h3>How to find out</h3><p>${q.discover}</p></div></div><div class="question-bottom"><div><strong>${q.owner}</strong><small>Handling: ${q.decision}<br>Reviewed ${REVIEW_DATE}; household decision not made.</small></div>${sourceLinks(q.sources)}</div></article>`).join("")}
 ${notice("No need to enter private information here.", "These are instructions for an attorney, CPA, trustee or licensed professional to verify privately. No document upload or account fields. No appraisal, quote, filing or signed household instruction has been obtained or submitted.")}`;
}
function comparisonTable() {
  return table(
    [
      "Path",
      "Nominal realizable value",
      "2026 dollars",
      "3-case nominal span",
      "First-year cash flow",
      "Liquidity check",
      "Rule / method",
    ],
    comparison.map((r) => [
      `<a href="#projections" data-select-path="${r.path}" class="path-label"><i style="--swatch:${PATHS.find((p) => p.id === r.path).color}"></i>${pathName(r.path)}</a>${badge(PATHS.find((p) => p.id === r.path).category)}`,
      `<strong>${compact(r.end.nominal)}</strong>`,
      compact(r.end.real),
      `${compact(r.low)} – ${compact(r.high)}<small>Rank ${r.ranks.join(" / ")} (down / center / up)</small>`,
      `<span class="${r.firstYearCash < 0 ? "negative" : "positive"}">${money(r.firstYearCash)}</span>`,
      r.liquidityFlag
        ? `${badge("Funding needed", "amber")}<small>Peak shortfall ${compact(r.peakFunding)}</small>`
        : `${badge("No modeled shortfall", "sage")}<small>Terminal liquid ${compact(r.end.liquid)}</small>`,
      sourceLinks(PATHS.find((p) => p.id === r.path).sources, true),
    ]),
    "All seven paths · same transfer date and horizon",
  );
}
function compare() {
  const sensitivities = sensitivityRows(inputs),
    matrix = comparisonMatrix(inputs);
  return `${pageHead("COMPARE THE WHOLE PICTURE", "Seven paths. One common clock.", "Every choice starts with the same A transfer, B ownership, tax framework, debt and cost assumptions.", controlsButton())}
 ${modelDisclaimer()}<div class="run-strip"><span>${icon("controls", 16)} ${inputs.transferYear} transfer · ${inputs.horizon} years · ${SCENARIOS.find((s) => s.id === inputs.scenario).name}</span><span>Run ${String(runNumber).padStart(3, "0")} · ${runMessage}</span></div>
 <div class="metric-grid">${metric("Illustrative leader", pathShort(leader()), "Model ranking, not a household recommendation")}${metric("Leader nominal value", compact(comparison[0].end.nominal), "After modeled A / portfolio exit costs and tax")}${metric("Same-year sale · net", compact(comparison.find((r) => r.path === "sell").sale.net), "Hypothetical basis, costs and debt payoff")}${metric("Housing use", "Separate metric", "Imputed rent is not investable cash")}</div>
 ${panel("Common-horizon comparison", `Transfer ${inputs.transferYear} → ${inputs.transferYear + inputs.horizon}. Dollar values round to $10; calculations retain precision.`, comparisonTable())}
 ${notice("What “realizable value” includes—and does not", "A’s hypothetical after-tax sale value + liquidated portfolio − financed cash deficits. B’s annual net cash flows and debt service are included; B is retained and its common equity excluded because its real basis/exit tax is unknown. No other inherited cash or estate tax is invented. Imputed housing service is separate.")}
 <div class="two-col">${panel(
   "What would change the ranking?",
   "One variable at a time; no probability assigned.",
   table(
     ["Sensitivity", "Lower test → leader", "Upper test → leader", "Context"],
     sensitivities.map((s) => [
       s.label,
       `${s.key === "rentA" ? money(s.low) : s.key === "capexScale" ? s.low + "×" : pct(s.low)}<br><strong>${pathShort(s.lowLeader)}</strong>`,
       `${s.key === "rentA" ? money(s.high) : s.key === "capexScale" ? s.high + "×" : pct(s.high)}<br><strong>${pathShort(s.highLeader)}</strong>`,
       sourceLinks(["rental", "gains", "bondRisk"], true),
     ]),
   ),
 )}${panel(
   "Imputed housing service",
   "Non-cash preference / opportunity value, NOT rent received.",
   table(
     ["Living path", "A vs B discounted housing service", "Context"],
     comparison
       .filter((r) => ["live", "live-sell", "live-rent"].includes(r.path))
       .map((r) => [
         pathName(r.path),
         `${compact(r.housingPV)}<small>3% nominal discount proxy; no cash/wealth credit</small>`,
         sourceLinks(["rental"], true),
       ]),
   ) +
     `<p class="fine-print">Synthetic A service ${money(inputs.imputedA)}/month vs B ${money(inputs.imputedB)}/month, grown with inflation. B does not require a new rent payment.</p>`,
 )}</div>
 ${panel(
   "Same transfer dates. Same horizons.",
   "Recomputed for every control change; never compare mismatched end dates.",
   table(
     [
       "A transfer",
       "Years after transfer",
       "Illustrative leader",
       "Gap to next path",
       "Context",
     ],
     matrix.map((r) => [
       String(r.transferYear),
       String(r.horizon),
       pathShort(r.leader),
       compact(r.gap),
       sourceLinks(["basis", "gains", "rental"], true),
     ]),
   ),
 )}
 ${panel("Why the answers can differ", "A conditional map, not a reverse-engineered recommendation.", `<div class="path-cards">${PATHS.map((p) => `<article><div class="path-card-title"><i style="--swatch:${p.color}"></i><h3>${p.name}</h3></div><p>${p.summary}</p><strong>Choose only if…</strong><p>${p.condition}</p>${sourceLinks(p.sources)}</article>`).join("")}</div>`)}
 ${notice("Reinvestment risk belongs beside the staging headline.", 'Parking reduces stock exposure only while capital remains uninvested. Treasury yields can fall; inflation erodes cash; a rebound can make waiting costly; and a crash after deployment still hurts. Long-run Treasury results use a rolling-yield proxy. <a href="#black-swan">Test the maturity-matched ladder and counterexamples</a>.', "amber")}`;
}
function pathSelect() {
  return `<label class="inline-control">Inspect path <select id="path-select">${PATHS.map((p) => `<option value="${p.id}" ${selectedPath === p.id ? "selected" : ""}>${p.name}</option>`).join("")}</select></label>`;
}
function projections() {
  const r = comparison.find((r) => r.path === selectedPath),
    key = JSON.stringify([selectedPath, inputs]);
  if (key !== distributionCache) {
    distributionValues = scenarioDistribution(selectedPath, inputs);
    distributionCache = key;
  }
  const vals = distributionValues;
  return `${pageHead("YEAR-BY-YEAR PROJECTIONS", "See the moving parts.", "Inspect cash flow, values, assessments, tax, debt, capital work and liquidity—not just an endpoint.", `<button class="button secondary" data-action="csv">${icon("download", 16)} Export scenario CSV</button>${controlsButton()}`)}
 ${modelDisclaimer()}<div class="filter-toolbar">${pathSelect()}<span class="subtle">${inputs.transferYear} → ${inputs.transferYear + inputs.horizon} · 2026 real-dollar base</span></div>
 ${panel(
   "Wealth through uneven conditions",
   "Seven choices share one economic sequence and transfer year.",
   lineChart(
     comparison.map((r) => ({
       name: pathShort(r.path),
       color: PATHS.find((p) => p.id === r.path).color,
       values: r.rows.map((x) => x.real),
     })),
     {
       height: 310,
       label: "Seven synthetic path values in 2026 purchasing power",
     },
   ),
 )}
 <div class="two-col">${panel(
   "A’s market value is not its assessment",
   pathName(selectedPath),
   lineChart(
     [
       {
         name: "A market (while held)",
         color: "#426d5b",
         values: r.rows.map((x) => x.marketA),
       },
       {
         name: "A assessment",
         color: "#b88b52",
         values: r.rows.map((x) => x.assessedA),
       },
       {
         name: "A income-tax basis",
         color: "#8a78a7",
         values: r.rows.map((x) => x.basisA),
       },
     ],
     {
       height: 250,
       label: "A market value, property assessment and income-tax basis",
     },
   ),
 )}${panel("Distribution across 81 design points", "Not a forecast, confidence interval or probability of success.", histogram(vals) + `<div class="distribution-stats">${metric("Minimum", compact(vals[0]), "Hypothetical grid")}${metric("Grid median", compact(vals[40]), "Equal weighting only")}${metric("Maximum", compact(vals.at(-1)), "Hypothetical grid")}</div><p class="fine-print">Grid: home growth ±1.5 percentage points; stocks ±2 points; maintenance/insurance ×0.75/1/1.25; A rent ×0.75/1/1.25. Not calibrated probabilities.</p>${sourceLinks(["crash1929", "crash2008", "inflation"], true)}`)}</div>
 ${panel(
   "Annual audit schedule",
   `${pathName(selectedPath)} · dollar values rounded to $10`,
   table(
     [
       "Year / use",
       "A end market / bill assessment / basis",
       "B end market / bill assessment",
       "A / B property tax",
       "Rents",
       "Operating / capital",
       "Income & portfolio tax",
       "Debt interest / principal",
       "End debt A / B",
       "Net cash flow",
       "Portfolio / funding gap",
       "Realizable nominal / real",
       "Context",
     ],
     r.rows.map((x) => [
       `${x.calendarYear}<small>Year ${x.year} · ${x.year === 0 ? "Transfer" : x.use}</small>`,
       `${money(x.marketA)}<br>${money(x.assessedA)}<br>${money(x.basisA)}`,
       `${money(x.marketB)}<br>${money(x.assessedB)}`,
       `${money(x.propertyTaxA)}<br>${money(x.propertyTaxB)}`,
       money(x.rent),
       `${money(x.operating)}<br>${money(x.capex)}`,
       money(x.taxes),
       `${money(x.interest ?? 0)}<br>${money(x.principal ?? 0)}`,
       `${money(x.debtA)}<br>${money(x.debtB)}`,
       `<span class="${x.netCash < 0 ? "negative" : "positive"}">${money(x.netCash)}</span>`,
       `${money(x.stocks + x.treasuries)}<br>${money(x.funding)}`,
       `${money(x.nominal)}<br>${money(x.real)}`,
       sourceLinks(["basis", "prop13", "rental", "gains"], true),
     ]),
   ),
 )}
 ${notice("Tax and exit conventions", "Annual tax includes income/investment tax and actual sale-event tax, not a repeated liquidation charge. Realizable value subtracts remaining A/portfolio exit tax and A sale costs. Actual sale events are separate below. Debt principal is a cash cost, not a rental deduction; no loss tax benefits are invented.", "amber")}
 ${panel(
   "A’s sale event and terminal exit check",
   "Same-tax-year sale is modeled at transfer; optional post-death price sensitivity.",
   table(
     ["Item", "Synthetic amount / treatment", "Authority"],
     [
       [
         "Sale event",
         r.sale
           ? `${inputs.transferYear + r.sale.year} · year ${r.sale.year}; net ${money(r.sale.net)}`
           : "No sale during holding; hypothetical sale at common terminal date",
         sourceLinks(["basis", "gains", "transfer"], true),
       ],
       [
         "Sale friction / tax at actual event",
         r.sale
           ? `${money(r.sale.sellingCosts)} costs / ${money(r.sale.tax)} tax`
           : "Included in hypothetical terminal realizable value",
         sourceLinks(["gains", "transfer"], true),
       ],
       [
         "A depreciation approximation",
         money(r.end.depA),
         sourceLinks(["rental"], true),
       ],
       [
         "Exit tax remaining at terminal date",
         money(r.end.terminalTax),
         sourceLinks(["gains", "homeSale", "niit", "form540"], true),
       ],
       [
         "B retained equity · before B exit tax",
         money(r.end.bRetainedEquity) + " · excluded from headline",
         sourceLinks(["basis"], true),
       ],
       [
         "Other inherited cash / estate-tax allocation",
         "— Unverified; not included",
         sourceLinks(["estate", "form706"]),
       ],
     ],
   ),
 )}`;
}
function blackSwan() {
  const runs = crashComparison(
      inputs,
      Math.min(600, Math.max(120, inputs.horizon * 12)),
    ),
    colors = ["#47779c", "#8c76ae", "#3f7563"],
    immediate = runs[0];
  return `${pageHead("BLACK SWAN LAB", "What if the timing is terrible?", "Test 24–36 months in Treasuries before a fixed phase into stocks. Also test when waiting hurts.", controlsButton())}
 ${notice("Reduced entry exposure ≠ a free option.", "Reinvestment yields can fall, inflation can erode cash, early bond sales can lose value, and a rapid rebound can make staging underperform. Once deployed, stocks still face a later crash. Constructed stress paths—not predictions or historical backtests.", "amber")}
 <div class="scenario-pills" role="group" aria-label="Economic stress scenarios">${SCENARIOS.map((s) => `<button data-scenario="${s.id}" aria-pressed="${inputs.scenario === s.id}">${s.name}</button>`).join("")}</div>
 <div class="stress-intro"><div><p class="eyebrow">CURRENT STRESS SHAPE</p><h2>${SCENARIOS.find((s) => s.id === inputs.scenario).name}</h2><p>${SCENARIOS.find((s) => s.id === inputs.scenario).detail}</p></div><div class="stress-terms"><strong>One identical starting portfolio</strong><span>${money(1000000)} hypothetical · ${pct(inputs.stockTarget, 0)}% stock contribution target</span><span>3 / 6 / 12 / 24-month ladder · ${inputs.phaseMonths}-month phase</span><span>Treasury interest: federal tax proxy only; CA exempt</span></div></div>
 ${panel(
   "Same proceeds. Different entry schedules.",
   "Investment-only held-to-maturity values; sale friction is identical and not charged again in this normalized example.",
   lineChart(
     runs.map((r, j) => ({
       name:
         j === 0
           ? "Immediate allocation"
           : `${r.parkMonths}m park → ${inputs.phaseMonths}m phase`,
       color: colors[j],
       values: r.rows.map((x) => x.real),
       monthScale: true,
     })),
     {
       height: 310,
       label:
         "Immediate, 24-month and 36-month parking in transfer-date purchasing power",
     },
   ),
 )}
 ${panel(
   "Protection and opportunity cost, side by side",
   "Drawdown uses monthly modeled value before final liquidation tax; terminal values are after stock exit tax.",
   table(
     [
       "Entry path",
       "Worst monthly drawdown",
       "Terminal nominal / real",
       "Difference vs immediate",
       "Stock phase completed",
       "Context",
     ],
     runs.map((r) => [
       r.parkMonths === 0
         ? "Immediate stock / Treasury allocation"
         : `${r.parkMonths} months parked → ${inputs.phaseMonths} months phasing`,
       pct(r.maxDrawdown),
       `${money(r.end.afterTax)}<br>${money(r.end.realAfterTax)}`,
       r.parkMonths === 0
         ? "Reference"
         : `${money(r.end.afterTax - immediate.end.afterTax)}<small>${r.end.afterTax >= immediate.end.afterTax ? "Modeled staging advantage" : "Modeled opportunity cost of waiting"}</small>`,
       r.parkMonths === 0
         ? "At transfer"
         : `${r.phaseDeployed + 1 >= r.phaseBudget ? "Yes" : "Not yet in horizon"}<small>Planned ${money(r.phaseBudget)}; deployed ${money(r.phaseDeployed)}</small>`,
       sourceLinks(
         ["bills", "notes", "bondRisk", "crash1929", "crash2008"],
         true,
       ),
     ]),
   ),
 )}
 <div class="two-col">${panel("How the ladder is represented", "More explicit than a constant “cash return.”", `<ol class="readable-list"><li>Split parking across 3/6/12/24-month tenors available before the phase date; these approximate actual bill weeks and 2-year notes.</li><li>Lock each purchase’s rate to maturity; reset only on reinvestment. New maturities cannot extend past the phase date.</li><li>At parking end, reserve scheduled stock purchases in <strong>non-interest-bearing cash</strong>; reinvest the permanent Treasury sleeve. Deploy equal monthly tranches—not a bottom-timing rule.</li><li>Use separate federal Treasury-interest, dividend and terminal-gain tax proxies. No CA income tax on direct Treasury interest.</li></ol><p class="fine-print">Simplified coupons, auction discounts and day counts. Bonds are held to maturity; accrued values are not early-sale quotes. No bond mark-to-market losses or forced sales simulated. Confirm actual maturities with the adviser.</p>${sourceLinks(["bills", "notes", "bondRisk"], true)}`)}
 ${panel(
   "What the history does—and doesn’t—say",
   "Severity anchors—not an official probability distribution.",
   table(
     ["Context", "Supported fact / scenario use", "Official source"],
     [
       [
         "1929–1932",
         "Federal Reserve: about 89% Dow price decline; price peak regained in 1954. Our monthly shape is synthetic, not dividend-reinvested modern-index returns.",
         sourceLinks(["crash1929"]),
       ],
       [
         "2007–2009",
         "Federal Reserve: housing/credit stress, 18-month recession, rate cuts toward zero and slow recovery. The 55%/18-month equity shock and recovery are chosen assumptions.",
         sourceLinks(["crash2008"]),
       ],
       [
         "Inflation",
         "Federal Reserve: Great Inflation 1965–82; inflation over 14% in 1980. The five-year/8% scenario is a hypothesis, not a replay.",
         sourceLinks(["inflation"]),
       ],
       [
         "Rebound / late crash",
         "Counterexamples to the staging strategy. No claim that these exact sequences occurred historically.",
         sourceLinks(["bondRisk"], true),
       ],
     ],
   ),
 )}</div>${btn("Compare property paths under this scenario", "compare")}`;
}
function taxes() {
  const examples = [900000, 1000000, 1100000, 1500000],
    h = propH({
      type: "multi",
      area: inputs.bBuildingArea,
      fiscalYear: 2027,
      seniorUnits: inputs.bSeniorUnits,
    });
  return `${pageHead("LAW, NOT GUESSWORK", "Three tax systems.<br><em>Keep them separate.</em>", "Official rules reviewed " + REVIEW_DATE + ". Eligibility is unverified; future law is not guaranteed.", controlsButton())}
 <div class="tax-concept-grid">${[
   [
     "01 / THE ESTATE",
     "Estate tax",
     "Estate-wide assets, gifts, deductions and portability. Not a per-heir tax-free allowance.",
     ["estate", "form706"],
   ],
   [
     "02 / A LATER SALE",
     "Income-tax basis",
     "Death-date basis if applicable, improvements, depreciation and sale gain.",
     ["basis", "gains"],
   ],
   [
     "03 / ANNUAL OWNERSHIP",
     "Property assessment",
     "Prop 13/19 eligibility, TRA percentage levies, direct charges and supplemental bills.",
     ["prop19", "prop13", "tra"],
   ],
 ]
   .map(
     ([n, t, d, s]) =>
       `<article><span>${n}</span><h2>${t}</h2><p>${d}</p>${sourceLinks(s)}</article>`,
   )
   .join("")}</div>
 ${panel(
   "Rule-by-rule review",
   "Enacted rules, conditional claims and unverified future amounts are separate.",
   table(
     ["Topic", "Finding / precise limit", "Status", "Official sources"],
     LEGAL_ROWS.map(([topic, finding, status, ...keys]) => [
       topic,
       finding,
       badge(
         status,
         /unverified|Preliminary/.test(status) ? "amber" : "neutral",
       ),
       sourceLinks(keys),
     ]),
   ),
 )}
 <div class="two-col">${panel(
   "Read Form 540’s 1% tax correctly",
   "2025 line 62: all five worksheet steps read directly.",
   `<div class="formula">1% × max(0, CA taxable income − $1,000,000)</div><p>For sale sensitivity, compute surtax <strong>with the taxable gain minus without it</strong>. Do not add 1% of gross proceeds or of the entire gain below the threshold. California gains are taxed as ordinary income.</p>` +
     table(
       ["CA taxable income", "1% surtax", "Source"],
       examples.map((n) => [
         money(n),
         money(bhTax(n)),
         sourceLinks(["form540"]),
       ]),
     ) +
     `<p class="fine-print">Hypothetical ${money(900000)} other taxable income + ${money(200000)} taxable gain → ${money(bhIncrement(900000, 200000))} incremental surtax. Not a household tax return; federal NIIT is separate.</p>${sourceLinks(["caGains", "form540"])}`,
 )}
 ${panel("Prop 19: eligibility before savings", "OFF by default. A future allowance is a sensitivity.", `<div class="formula">Eligible assessment = base + max(0, FMV − base − allowance)</div><p>Document qualifying family relationship and transferor primary residence. The heir must genuinely use A as a long-term primary home, meet the 1-year exemption rule and file the separate claim.</p><p>Allowance grows in hypothetical biennial cycles; the model does not freeze the current amount in 2045 or mislabel CPI as the legal index. Moving out restores the transfer-date market base factored forward, from the following lien date (annual timing simplified).</p><p class="fine-print">Current annualized future proxy: ${pct(inputs.prop19Growth)}. Actual future FHFA California HPI adjustments are unknown.</p>${sourceLinks(["prop19", "allowance"])}`)}</div>
 ${panel(
   "Prop H · official terms, conditional calculator",
   "Nov 2026 Muni parcel measure. Certification/codification unverified; OFF in baseline.",
   notice(
     "Not an older measure also called “H”.",
     "The ballot legal text controls this scenario. The official results page still labels returns preliminary.",
     "amber",
   ) +
     table(
       ["Term", "Official text / model treatment", "Source"],
       [
         [
           "Period",
           "July 1, 2027–June 30, 2042. No automatic extension through a 50-year horizon.",
           sourceLinks(["propH"]),
         ],
         [
           "Multifamily parcel",
           `$249 per parcel through 5,000 sq ft; +$0.195/sq ft above, capped at $50,000 before inflation. Synthetic ${inputs.bBuildingArea.toLocaleString()} sq ft → about ${money(h)} before any actual parcel finding.`,
           sourceLinks(["propH"], true),
         ],
         [
           "Resident senior deduction",
           "Qualifying 65+ beneficial owner occupying a unit: $249/unit reduction before indexing; application/evidence required; no tax below zero.",
           sourceLinks(["propH"]),
         ],
         [
           "Index",
           "SF/Oakland/Hayward CPI-U increases from FY2028–29; per-sq-ft amounts round down to 0.1 cent, other dollars down to whole dollars. Future CPI is a scenario, not official data.",
           sourceLinks(["propH"]),
         ],
         [
           "Upper single-family tier",
           "Legal §1805(a)(3): $1.99/sq ft above 5,000 after lower tier; Controller summary says $1.19. Conflict flagged; calculator follows legal text.",
           sourceLinks(["propH", "propHSummary"]),
         ],
         [
           "Tenant recovery",
           "Up to 50%, capped at $65/unit/year before indexing. Exempt footage and initial base rents set on/after June 1, 2027 excluded. No recovery booked without evidence.",
           sourceLinks(["propH"]),
         ],
         [
           "Actual parcel amount",
           "— Unverified: classification, taxable area, exemptions, age, lease dates, current certification and actual CPI factors.",
           sourceLinks(["propH", "propHResults"]),
         ],
       ],
     ),
 )}
 ${notice("Legislation watch is a process—not a claim of omniscience.", "Recheck IRS annual guidance, BOE allowance/implementing changes, FTB instructions and local measures quarterly and before transactions. Log bill/ordinance ID, status, enactment/effective dates, model effect, reviewer and next review. A comprehensive pending-bill search and background monitoring are not certified complete. Proposals are never silently applied as enacted law.", "amber")}`;
}
function timeline() {
  return `${pageHead("DEADLINES & PROCESS", "Know which clock is ticking.", "Relative deadlines do not wait for a deed distribution. Planning dates and legal deadlines are distinguished.")}${notice("No actual transfer date is asserted.", "2040–2050 is a planning window. Counsel must calculate actual dates, check exceptions/extensions and use the forms in force at transfer. No forms are filed here.")}<div class="timeline">${TIMELINE.map((t, j) => `<article class="timeline-item"><div class="timeline-marker">${String(j + 1).padStart(2, "0")}</div><div class="timeline-date">${t.when}<small>${t.type}</small></div><div class="timeline-content"><h2>${t.title}</h2><p>${t.body}</p>${sourceLinks(t.sources)}</div></article>`).join("")}</div>`;
}
function planning() {
  return `${pageHead("BUILDINGS, CASH & GOVERNANCE", "Plan for the bills,<br><em>not just the balance sheet.</em>", "A private inventory and inspected capital plan are prerequisites—not automatic research deliverables.")}
 ${panel(
   "Actual property evidence stays blank",
   "No household amounts inferred from private hints.",
   table(
     [
       "Required record",
       "A · inherited",
       "B · already owned",
       "Acquisition plan / official context",
     ],
     [
       [
         "Title / beneficial ownership",
         "Attorney reviews deeds, trust and amendments.",
         ["basis", "death"],
       ],
       [
         "Written value / death-date appraisal",
         "Independent appraisal with valuation date and land/building split.",
         ["basis"],
       ],
       [
         "Market rent / leases",
         "Two managers, executed-lease comps; counsel verifies leases and lawful owner space.",
         ["rental", "leases"],
       ],
       [
         "Tax TRA / levies / direct charges",
         "Read bill; match same-fiscal-year official TRA; reconcile direct assessments separately.",
         ["tra", "prop13"],
       ],
       [
         "Debt / rate / term / payoff",
         "Lender statements and transaction-date payoff; do not assume zero debt.",
         ["estate", "rental"],
       ],
       [
         "Insurance / limits / exclusions",
         "Written occupancy-specific, replacement-cost, liability, catastrophe and rental-risk quotes.",
         ["insurance"],
       ],
       [
         "Water / power / solar settlement",
         "12–24 months of bills, tariff/true-up and condition records. No permanent solar profit assumed.",
         ["rental"],
       ],
       [
         "Condition / bids / capital timing",
         "Inspection, safety priority, specialty review and competing bids.",
         ["rental", "insurance"],
       ],
       [
         "Depreciation history / tax basis",
         "CPA reconciles improvements and allowed/allowable depreciation. No B reset with A.",
         ["basis", "rental"],
       ],
     ].map(([item, plan, s]) => [
       item,
       "— Unverified",
       "— Unverified",
       plan + sourceLinks(s),
     ]),
   ),
 )}
 <div class="two-col">${["A", "B"]
   .map((p) =>
     panel(
       `Property ${p} · five-year capital template`,
       "Allowances only. Actual condition, scope, quote and choice unverified.",
       table(
         [
           "Year",
           "Inspection-dependent work slot",
           "Synthetic low – high",
           "Actual bid / decision / date",
           "Context",
         ],
         CAPITAL_PLAN[p].map((c) => [
           String(c.year),
           c.item,
           `${money(c.low)} – ${money(c.high)}`,
           "— Unverified / not selected",
           sourceLinks(["rental", "insurance"], true),
         ]),
       ) +
         `<p class="fine-print">Model spends midpoint × ${inputs.capexScale}, inflation-adjusted, in years 1–5 while held; no duplicate reserve deduction. These amounts are conservatively capitalized. The CPA must reclassify genuine deductible repairs into operating expense.</p>`,
     ),
   )
   .join("")}</div>
 ${panel(
   "Estate liquidity plan · before committing proceeds",
   "Without the estate-wide inventory and gifts, household headroom stays blank.",
   table(
     [
       "Step",
       "Private record / calculation needed",
       "Status / reviewed",
       "Official context",
     ],
     [
       [
         "Inventory decedent’s estate",
         "Cash, brokerage, retirement/IRD, included insurance, businesses, other real estate, liabilities, ownership and beneficiaries. B is not included just because the heir owns it.",
         "Not obtained · " + REVIEW_DATE,
         sourceLinks(["estate", "form706"]),
       ],
       [
         "Ask about gifts / portability now",
         "Collect Forms 709, prior exemption use, prior spouse’s Form 706 and documented DSUE. No assumed double exclusion.",
         "Not obtained · " + REVIEW_DATE,
         sourceLinks(["estate", "form706"]),
       ],
       [
         "Compute filing and tax reserve",
         "CPA calculates estate-wide test, deductions, gifts and credit using death-year law. Actual remaining headroom: —.",
         "Unverified",
         sourceLinks(["estate", "form706"]),
       ],
       [
         "Match liquidity to due dates",
         "Map cash/Treasury maturities to tax/payment dates, administration, property bills, debt and reserves; stress a delayed sale.",
         "Plan not approved",
         sourceLinks(["form706", "bills", "notes"]),
       ],
       [
         "Confirm apportionment / distribution",
         "Attorney identifies who bears tax and costs. Hold reserves before distributing or investing all proceeds.",
         "Plan not approved",
         sourceLinks(["estate", "form706"]),
       ],
       [
         "Review annually / after major events",
         "Update ownership, gifts, coverage, debts and enacted law; archive signed decision/date/reason privately.",
         "Governance proposal",
         sourceLinks(["form706", "prop19", "insurance"]),
       ],
     ],
   ),
 )}
 ${notice("Parking is not a substitute for the estate reserve.", "The model’s working reserve is a synthetic shared starting amount, not verified distributable cash. Carve out taxes, administration, repairs and spending before selecting a risky allocation. A financed shortfall in a projection does not establish access to credit.", "amber")}`;
}
function suggestions() {
  const list = SUGGESTIONS.filter(
    (s) =>
      suggestionFilter === "All" ||
      (decisions.get(s.id)?.status ?? "Not reviewed") === suggestionFilter,
  );
  return `${pageHead("REVIEW BEFORE IMPLEMENTING", "A place for better ideas.", "Review and compare next steps. Suggestions are not household authorizations, transactions or professional filings.", `<button class="button secondary" data-action="decisions">${icon("download", 16)} Export review log</button>`)}
 ${notice("Nothing is approved on your behalf.", "Every suggestion starts “Not reviewed.” Your choice/date live in tab memory only: not sent, saved to browser storage, committed or implemented. Export a sanitized review log if wanted; refresh clears it.")}
 <div class="filter-toolbar"><div class="segmented" role="group" aria-label="Suggestion filter">${["All", "Not reviewed", "Prioritize", "Defer"].map((f) => `<button data-suggestion-filter="${f}" aria-pressed="${suggestionFilter === f}">${f}</button>`).join("")}</div><span class="subtle">Choose before doing</span></div>
 <div class="suggestion-grid">${list
   .map((s) => {
     const d = decisions.get(s.id);
     return `<article class="suggestion-card"><div class="question-top"><span class="eyebrow">${s.id} / ${s.priority}</span>${badge(d?.status ?? "Not reviewed", d?.status === "Prioritize" ? "sage" : "neutral")}</div><h2>${s.title}</h2><p class="suggestion-why">${s.reason}</p><h3>Suggested action</h3><p>${s.action}</p><h3>How to judge success</h3><p>${s.test}</p>${sourceLinks(s.sources)}<div class="suggestion-decision"><label>Review choice <select data-decision-id="${s.id}">${["Not reviewed", "Prioritize", "Defer"].map((o) => `<option ${(d?.status ?? "Not reviewed") === o ? "selected" : ""}>${o}</option>`).join("")}</select></label><small>${d ? `Decision: ${d.status} · ${d.date}<br>Reason: ${d.reason}` : "No decision / implementation date.<br>Proposal reviewed " + REVIEW_DATE}</small></div></article>`;
   })
   .join("")}</div>
 ${panel(
   "Actual household decision · separate signed record",
   "A scenario switch, suggestion review or software release is not a decision to sell, rent or move.",
   table(
     ["Required field", "Current actual decision", "Context"],
     [
       ["Path selected", "— Not made", ["prop19", "bondRisk"]],
       ["Decision date / signatories", "— Not provided", ["estate", "prop19"]],
       [
         "Why this path beats alternatives",
         "— Await independent evidence and agreed criteria",
         ["basis", "rental", "bondRisk"],
       ],
       [
         "What would reopen the decision",
         "— Define rent, cost, law, housing, liquidity and drawdown thresholds privately",
         ["prop19", "form706", "bondRisk"],
       ],
       [
         "Next review",
         "Annual / material change recommended; no meeting scheduled",
         ["form706", "prop19"],
       ],
     ].map(([t, d, s]) => [t, d, sourceLinks(s)]),
   ),
 )} `;
}
function sources() {
  const list = Object.entries(SOURCES).filter(([k, s]) =>
    (k + " " + s.name + " " + s.scope + " " + s.kind)
      .toLowerCase()
      .includes(sourceQuery.toLowerCase()),
  );
  return `${pageHead("SOURCE REGISTER", "Trust the provenance.<br><em>Keep the limits visible.</em>", "Direct official links, specific sections read, and the boundary between a legal rule and private evidence.")}
 ${notice("A related official link is not property-specific verification.", "Blank household fields stay unverified. Synthetic calculation rows are explicitly derived, not official figures. Only named sections were reviewed; no blanket full-document or future-law verification is asserted.")}
 <div class="filter-toolbar"><label class="search-control">${icon("sources", 18)}<input id="source-search" type="search" placeholder="Find an authority or topic…" value="${esc(sourceQuery)}" aria-label="Search sources" autocomplete="off"></label><span class="subtle">${list.length} sources · read ${REVIEW_DATE}</span></div>
 ${table(
   [
     "Authority",
     "What it supports—and does not",
     "Sections reviewed",
     "Status / date",
     "Official link",
   ],
   list.map(([, s]) => [
     s.name,
     s.scope,
     s.read,
     `${badge(s.unverified ? "Parcel row NOT verified" : s.kind, s.unverified ? "amber" : "neutral")}<small>${REVIEW_DATE} · one-time review</small>`,
     `<a href="${s.url}" target="_blank" rel="noopener noreferrer">Open authority ${icon("external", 13)}</a>`,
   ]),
 )}
 ${panel("Recheck protocol", "Proposed cadence; no autonomous monitoring service running.", `<ol class="readable-list"><li>Quarterly and before transactions: reopen IRS estate/portability, BOE allowance/Prop 19, FTB current instructions, county rates and local rental/parcel measures.</li><li>Record revision/retrieval date, section, claim and enacted/proposed/preliminary status. Read substantive changes, not only HTTP status.</li><li>Use only supported constants; keep unpublished future facts blank. Counsel confirms effective dates.</li><li>After each input/rule change, rebuild model/site, run tests, inspect ranking changes and record why. Signed household decisions are separate.</li><li>Annually refresh independent evidence, gifts/portability and liquidity; repeat crash, inflation, rebound and late-crash tests.</li></ol>${sourceLinks(["estateUpdate", "form706", "prop19", "form540", "propHResults"])}`)}`;
}
function glossary() {
  return `${pageHead("GLOSSARY", "Plain words for complex choices.", "A quick reference to the concepts used in the lab.")}${panel(
    "The useful distinctions",
    "Simplified definitions; the official source and professional advice control.",
    table(
      ["Term", "Meaning in this lab", "Official context"],
      GLOSSARY.map(([t, d, s]) => [t, d, sourceLinks([s])]),
    ),
  )}`;
}
function flagged() {
  return `${pageHead("FLAGGED FOR REVIEW", "Uncertainty, out in the open.", "Unverified items do not block a sanitized release. They do block pretending the household is ready to decide.")}<div class="review-counts">${metric("Critical exposure", "01", "Broader repository containment incomplete", "warn")}${metric("Published review items", String(FLAGS.length).padStart(2, "0"), "No invented confirmations")}${metric("Research snapshot", REVIEW_DATE, "No future-law guarantee")}</div>${FLAGS.map((f) => `<article class="flag-card"><div class="flag-icon">${icon("flagged", 20)}</div><div><div class="question-top"><span class="eyebrow">${f.id}</span>${badge(f.severity, f.severity === "Critical" ? "danger" : f.severity === "Gate" ? "amber" : "neutral")}</div><h2>${f.title}</h2><p>${f.body}</p><p class="fine-print">Needs review · ${REVIEW_DATE}. No private evidence or household decision supplied.</p>${sourceLinks(f.sources)}</div></article>`).join("")}`;
}
function privacy() {
  return `${pageHead("PRIVACY FIRST", "Public-safe is not the same<br>as private.", "No names, addresses, parcel numbers, exact household figures or assessment histories belong here.")}
 ${notice("Containment remains open.", "The repository is public. A concurrent root build introduced household-derived values into public history. GitHub rejected Pages unpublish and repository-private requests with HTTP 403. Neither setting changed. Administrator permission attention is required; a code update does not erase history.", "danger")}
 <div class="two-col">${panel("What this module does", "Avoid collecting private data.", `<ul class="readable-list"><li>Property A / B placeholders and genuinely synthetic ranges—not rounded household histories.</li><li>Actual valuations, rent, rates, costs, debt, estate headroom and eligibility remain blank.</li><li>No uploads, account fields, analytics, external fonts, cookies, localStorage, IndexedDB, service workers or API calls.</li><li>Controls and review choices exist in tab memory only. Exports contain synthetic values or generic suggestion reviews.</li><li>Content security policy blocks script network connections; clicked sources open without referrer.</li><li>noindex/nofollow/noarchive are crawler requests, <strong>not access control</strong>. Hosts can still log requests.</li></ul>`)}${panel("What requires an administrator", "A deletion commit is not a history scrub.", `<ol class="readable-list"><li>Stop sensitive public artifacts and restrict repository visibility. This app lacks required administrative/Pages permission.</li><li>Coordinate active sessions, collaborators and fork owners; prevent stale-clone recontamination.</li><li>Inventory all refs, PRs, Actions logs/artifacts and cached pages without copying private values into logs/issues.</li><li>Agree and execute full-ref history cleanup in a controlled clone. This session cannot rewrite/push other branches.</li><li>Request eligible GitHub Support cache/PR-ref cleanup. Third-party public copies cannot be reliably recalled.</li><li>Audit a static-artifact allowlist. Do not upload the entire repository “.” to Pages.</li></ol>${sourceLinks(["github"])}`)}</div>
 ${panel(
   "Public vs private boundary",
   "Rounding to $10 is presentation—not anonymization.",
   table(
     ["Data class", "Appropriate location", "Public treatment", "Context"],
     [
       [
         "Public-law constants",
         "Dated source register",
         "Exact legal constants retained internally; rounded scenario dollars identified.",
         ["allowance", "form540", "estate"],
       ],
       [
         "Household financial history",
         "Encrypted private matter file outside Git / Pages / browser storage",
         "Not loaded. No rounded assessment histories.",
         ["github"],
       ],
       [
         "Appraisal, trust, leases, insurance, loans",
         "Professional secure channel",
         "Not uploaded; actual values blank.",
         ["basis", "form706", "insurance"],
       ],
       [
         "Synthetic inputs / results",
         "Public scenario sandbox",
         "Hypothetical, not household estimates or official forecasts.",
         ["bondRisk", "rental"],
       ],
       [
         "Signed decisions / inventory",
         "Private legal and financial records",
         "Only generic templates / unapproved proposals here.",
         ["estate", "github"],
       ],
     ].map(([c, l, t, s]) => [c, l, t, sourceLinks(s)]),
   ),
 )}<p class="fine-print">Observed limits, not a full security audit or assurance about other root pages, remote refs, caches, forks or external copies.</p>`;
}
function briefing() {
  return `${pageHead("READY FOR THE PROFESSIONALS", "A better first meeting.", "A one-page, public-safe agenda. No household facts or tax eligibility have been confirmed.", `<button class="button" data-action="print">${icon("briefing", 17)} Print briefing sheet</button>`)}
 <div class="screen-only">${notice("Print only this sheet.", "The dedicated print layout hides navigation, charts and controls. All actual financial fields stay blank. Take records through your professional’s secure channel—not this website.")} </div>
 <article class="brief-sheet" id="brief-sheet"><header class="brief-heading"><div class="brief-wordmark"><span class="brand-mark">e.</span> Estate / Decision Lab</div><span>REVIEWED ${REVIEW_DATE} · v${MODEL_VERSION}</span><h2>Attorney &amp; CPA Briefing Sheet</h2><p>Planning agenda, not legal/tax advice · no household path selected · no filing authorized</p></header>
 <div class="brief-context"><strong>A</strong><p>Anticipated trust inheritance, 2040–2050 planning window. Transfer, basis and eligibility unverified.</p><strong>B</strong><p>Already owned by heir; retain existing leased income and verify separate owner space. No A-triggered basis/assessment reset.</p></div>
 <div class="brief-two"><section><h3>1 / Bring privately · do not upload</h3><ul><li>Trust, deeds, amendments, beneficial shares and estate-wide inventory.</li><li>Forms 709 / prior spouse’s 706, gifts, DSUE and tax apportionment.</li><li>A death-date written appraisal & land/building split; two independent rent opinions.</li><li>Both tax bills / TRA, loans/payoffs, leases/permits, depreciation, insurance and inspected five-year bids.</li></ul></section><section><h3>2 / Confirm before comparing</h3><ul><li>Genuine long-term housing preference; Prop 19 eligibility and continuing occupancy.</li><li>Liquidity reserve, tax funding, minimum net rent, concentration and drawdown limits.</li><li>§1031 desire <strong>before sale</strong>; qualified intermediary if appropriate.</li><li>Signed investment policy before proceeds; test immediate allocation vs 24/36-month park + 12/24-month phase.</li></ul></section></div>
 <section><h3>3 / Ask for a common-date, after-tax comparison</h3><p>Price the <strong>same-transfer-tax-year sale first</strong>. Compare live A, rent A, sell/reinvest, sell–park–phase, rent 5→sell, live 10→sell, live 10→rent. Retain B rents; include taxes, debt, capital work, liquidity, depreciation/§1250, conditional §121, imputed housing service separately, and estate funding. Recheck rebound and later-crash risks.</p></section>
 <div class="brief-two"><section><h3>4 / Calendar with counsel</h3>${table(
   ["Clock", "Check", "Official"],
   [
     [
       "150 days",
       "Death report; probate exception",
       `<a href="${SOURCES.death.url}" target="_blank" rel="noopener noreferrer">BOE death guide</a>`,
     ],
     [
       "9 months",
       "706 / tax; extension ≠ payment relief",
       `<a href="${SOURCES.form706.url}" target="_blank" rel="noopener noreferrer">IRS 706</a>`,
     ],
     [
       "1 year / 3 years",
       "Prop 19 exemption / separate claim; earlier if third-party transfer",
       `<a href="${SOURCES.prop19.url}" target="_blank" rel="noopener noreferrer">BOE Prop 19</a>`,
     ],
     [
       "45 / ≤180 days",
       "Only qualifying §1031; return-due-date limit",
       `<a href="${SOURCES.form8824.url}" target="_blank" rel="noopener noreferrer">IRS 8824</a>`,
     ],
   ],
 )}</section><section><h3>5 / Actual answers · remain unverified</h3>${table(
   ["Item", "Private verified answer", "Official context"],
   [
     [
       "A value / net rent / TRA",
       "— / — / —",
       `<a href="${SOURCES.basis.url}" target="_blank" rel="noopener noreferrer">IRS basis</a>`,
     ],
     [
       "Debt / capital / estate headroom",
       "— / — / —",
       `<a href="${SOURCES.form706.url}" target="_blank" rel="noopener noreferrer">IRS 706</a>`,
     ],
     [
       "Prop 19 / §121 eligible?",
       "— / —",
       `<a href="${SOURCES.homeSale.url}" target="_blank" rel="noopener noreferrer">IRS §121</a>`,
     ],
     [
       "Path / date / why / review date",
       "— / — / — / —",
       `<a href="${SOURCES.bondRisk.url}" target="_blank" rel="noopener noreferrer">SEC risk</a>`,
     ],
   ],
 )}</section></div><footer class="brief-foot"><p><strong>Keep regimes separate:</strong> estate-wide federal exclusion ≠ income-tax basis ≠ annual assessment. 2026 federal exclusion: $15m; future law unknown. CA 1% surtax is only above $1m taxable income, not gross proceeds. Prop H: preliminary, optional sensitivity with 2042 sunset.</p><p><a href="${SOURCES.estate.url}" target="_blank" rel="noopener noreferrer">IRS estate tax</a> · <a href="${SOURCES.basis.url}" target="_blank" rel="noopener noreferrer">IRS Pub 551</a> · <a href="${SOURCES.form540.url}" target="_blank" rel="noopener noreferrer">FTB Form 540 line 62</a> · <a href="${SOURCES.propH.url}" target="_blank" rel="noopener noreferrer">SF H legal text</a> · Full dated source register in Decision Lab → Official sources</p><p><strong>Privacy:</strong> prior public Git history remains exposed; current-tree sanitization is not erasure. Handle all documents outside Git/Pages.</p></footer></article>`;
}

const numberSpecs = [
  [
    "The starting point",
    [
      ["marketA", "$", 0, 10000000, 10000],
      ["marketB", "$", 0, 10000000, 10000],
      ["assessedA", "$", 0, 10000000, 10000],
      ["assessedB", "$", 0, 10000000, 10000],
      [
        "workingReserve",
        "$",
        0,
        5000000,
        10000,
        "Common cash reserve at transfer (not verified distributable estate cash)",
      ],
    ],
  ],
  [
    "Rent & housing service",
    [
      ["rentA", "$", 0, 50000, 100],
      ["rentB", "$", 0, 50000, 100],
      ["rentGrowth", "%", 0, 10, 0.05],
      ["vacancy", "%", 0, 50, 0.5],
      ["management", "%", 0, 30, 0.5, "Management share of collected rent"],
      ["bRentalShare", "%", 0, 100, 1, "B rental-cost allocation share"],
      [
        "extraBRent",
        "$",
        0,
        20000,
        100,
        "Optional extra B unit monthly rent (OFF without lease review)",
      ],
      [
        "imputedA",
        "$",
        0,
        50000,
        100,
        "A monthly housing-service value · non-cash",
      ],
      [
        "imputedB",
        "$",
        0,
        50000,
        100,
        "B monthly housing-service value · non-cash",
      ],
    ],
  ],
  [
    "Operating costs · annual in 2026 dollars",
    [
      ["maintenanceA", "$", 0, 200000, 1000],
      ["maintenanceB", "$", 0, 200000, 1000],
      ["insuranceA", "$", 0, 100000, 100],
      ["insuranceB", "$", 0, 100000, 100],
      ["utilitiesA", "$", 0, 50000, 100],
      ["utilitiesB", "$", 0, 50000, 100],
      [
        "insuranceGrowth",
        "%",
        0,
        15,
        0.1,
        "Insurance escalation (independent of inflation)",
      ],
      [
        "landlordInsuranceFactor",
        "x",
        1,
        3,
        0.1,
        "A landlord / primary insurance factor",
      ],
      [
        "landlordUtilityShare",
        "%",
        0,
        100,
        1,
        "A utilities paid by owner while rented",
      ],
    ],
  ],
  [
    "Capital spending & property tax",
    [
      [
        "capexScale",
        "x",
        0,
        5,
        0.1,
        "5-year capital plan & later renewal multiplier",
      ],
      ["renewalA", "$", 0, 200000, 1000],
      ["renewalB", "$", 0, 200000, 1000],
      [
        "adValoremA",
        "%",
        0,
        5,
        0.01,
        "A hypothetical percentage levy · actual TRA unverified",
      ],
      [
        "adValoremB",
        "%",
        0,
        5,
        0.01,
        "B hypothetical percentage levy · actual TRA unverified",
      ],
      ["directA", "$", 0, 50000, 100],
      ["directB", "$", 0, 50000, 10],
      [
        "assessedGrowth",
        "%",
        0,
        2,
        0.1,
        "Annual assessment-factor sensitivity (max 2%)",
      ],
      ["prop19Growth", "%", 0, 6, 0.1],
      [
        "bBuildingArea",
        "sf",
        0,
        100000,
        100,
        "B taxable area sensitivity; actual area unknown",
      ],
      [
        "bSeniorUnits",
        "n",
        0,
        10,
        1,
        "B eligible resident-senior units (only while living in B)",
      ],
      ["propHCpi", "%", 0, 10, 0.1, "Hypothetical SF CPI for optional Prop H"],
    ],
  ],
  [
    "Debt · balances at transfer",
    [
      ["debtA", "$", 0, 10000000, 10000],
      ["debtB", "$", 0, 10000000, 10000],
      [
        "mortgageRate",
        "%",
        0,
        20,
        0.1,
        "Common fixed mortgage interest sensitivity",
      ],
      [
        "mortgageYears",
        "n",
        1,
        50,
        1,
        "Remaining amortization years at transfer",
      ],
      [
        "fundingRate",
        "%",
        0,
        25,
        0.1,
        "Unfunded deficit interest sensitivity (not a credit offer)",
      ],
    ],
  ],
  [
    "Exit tax & basis sensitivities",
    [
      ["federalOrdinary", "%", 0, 50, 0.1],
      ["federalGains", "%", 0, 30, 0.1],
      ["californiaRate", "%", 0, 15, 0.1],
      [
        "otherTaxableIncome",
        "$",
        0,
        5000000,
        10000,
        "Other annual taxable income / MAGI proxy, noninvestment",
      ],
      [
        "basisFraction",
        "%",
        0,
        100,
        1,
        "A adjusted basis as % of death-date market (100% only if applicable)",
      ],
      [
        "landShare",
        "%",
        0,
        100,
        1,
        "A share of basis / conversion FMV allocated to land",
      ],
      [
        "bDepreciableBasis",
        "$",
        0,
        5000000,
        10000,
        "B existing rental-building depreciable basis · NO reset",
      ],
      [
        "bPriorDepreciation",
        "$",
        0,
        5000000,
        10000,
        "B depreciation previously allowed/allowable",
      ],
      ["saleCost", "%", 0, 20, 0.1],
      [
        "recordingReserve",
        "$",
        0,
        10000,
        10,
        "Unverified recording / document fee budget",
      ],
      [
        "escrowReserve",
        "$",
        0,
        50000,
        100,
        "Unverified escrow / other sale-fee budget",
      ],
      [
        "sameYearMove",
        "%",
        -30,
        30,
        0.5,
        "Same-tax-year sale price move after death (basis unchanged)",
      ],
    ],
  ],
  [
    "Economic centers · actual scenarios are uneven",
    [
      ["homeGrowth", "%", -5, 10, 0.1],
      ["stockGrowth", "%", 0, 15, 0.1],
      ["inflation", "%", 0, 10, 0.1],
      ["treasuryYield", "%", 0, 10, 0.1],
    ],
  ],
];
function field([k, kind, min, max, step, label]) {
  let value = inputs[k];
  if (kind === "%") value = +(value * 100).toFixed(5);
  if (kind === "$") value = money10(value);
  const range = RANGE_DEFS[k];
  return `<label class="number-field"><span>${label ?? range?.[2] ?? k}</span><div><input name="${k}" type="number" value="${value}" min="${min}" max="${max}" step="${step}" data-kind="${kind}" required><b>${kind === "$" ? "USD" : kind === "%" ? "%" : kind === "n" ? "years / count" : kind === "sf" ? "sq ft" : "×"}</b></div>${range ? `<small>Synthetic band ${range[3] === "%" ? pct(range[0]) + " – " + pct(range[1]) : money(range[0]) + " – " + money(range[1])}</small>` : ""}</label>`;
}
const selectField = (name, label, options) =>
  `<label class="number-field"><span>${label}</span><select name="${name}">${options.map(([v, l]) => `<option value="${v}" ${String(inputs[name]) === String(v) ? "selected" : ""}>${l}</option>`).join("")}</select></label>`;
function controlsMarkup() {
  return `<div class="drawer-head"><div><p class="eyebrow">SYNTHETIC SCENARIO SANDBOX</p><h2 id="controls-title">What would change your mind?</h2></div><button class="icon-button" data-action="close-controls" aria-label="Close what-if controls">${icon("close")}</button></div><form id="scenario-form"><div class="drawer-scroll"><p class="drawer-intro">Hypothetical values only. Defaults do not reproduce household figures. Changes stay in tab memory; applying them recalculates all seven paths and reports whether the <em>illustrative</em> leader moved. No household recommendation is made.</p>
 <fieldset><legend>One common clock & allocation</legend><div class="field-grid">${selectField(
   "transferYear",
   "A planning transfer year",
   [
     [2040, "2040"],
     [2045, "2045"],
     [2050, "2050"],
   ],
 )}${selectField("horizon", "Years after transfer", [
   [10, "10 years"],
   [20, "20 years"],
   [30, "30 years"],
   [50, "50 years"],
 ])}${selectField(
   "scenario",
   "Economic sequence",
   SCENARIOS.map((s) => [s.id, s.name]),
 )}${selectField("stockTarget", "Stock contribution weight", [
   [0.4, "40% stocks / 60% Treasury"],
   [0.6, "60% stocks / 40% Treasury"],
   [0.7, "70% stocks / 30% Treasury"],
   [0.8, "80% stocks / 20% Treasury"],
   [1, "100% stocks after phase"],
 ])}${selectField("parkMonths", "Park sale proceeds for", [
   [24, "24 months"],
   [36, "36 months"],
 ])}${selectField("phaseMonths", "Then phase stock sleeve over", [
   [12, "12 months"],
   [24, "24 months"],
 ])}</div><p class="fine-print">No periodic rebalancing. Contribution weights can drift as prices move. Annual property model uses rolling Treasury yields; the monthly black-swan lab uses fixed-term ladder purchases.</p></fieldset>
 <fieldset><legend>Eligibility · hypothetical, not a finding</legend>${[
   [
     "prop19Eligible",
     "All Prop 19 transferor, heir and filing conditions satisfied",
     "OFF by default; actual attorney / assessor review missing.",
   ],
   [
     "longTermOccupancy",
     "Genuine continuing long-term primary-home intent",
     "Both this AND eligibility must be on. Benefits stop on modeled departure.",
   ],
   [
     "section121",
     "Separately assume every §121 test is satisfied",
     "Applies only to lived-in paths with at least 2 years use; never pure rental/same-year exits.",
   ],
   [
     "niitExposed",
     "Treat net investment income as NIIT-exposed",
     "Threshold calculation still applies; rental participation exceptions not established.",
   ],
   [
     "includePropH",
     "Test Nov 2026 Prop H ballot terms (uncertified)",
     "OFF baseline; no tax after June 30, 2042, no unsupported tenant passthrough.",
   ],
   [
     "allowExtraBRent",
     "Test extra-unit B income while living in A",
     "OFF baseline. Existing B leased income remains in EVERY path. Legal availability and later return unverified.",
   ],
 ]
   .map(
     ([k, l, d]) =>
       `<label class="check-field"><input type="checkbox" name="${k}" ${inputs[k] ? "checked" : ""}><span><strong>${l}</strong><small>${d}</small></span></label>`,
   )
   .join("")}<div class="field-grid">${selectField(
   "section121Limit",
   "Conditional home-gain exclusion cap",
   [
     [250000, "$250,000 sensitivity"],
     [500000, "$500,000 · spouse conditions also required"],
   ],
 )}${selectField("niitThreshold", "NIIT threshold sensitivity", [
   [125000, "$125,000 · married filing separately"],
   [200000, "$200,000 · single / head of household"],
   [250000, "$250,000 · joint / qualifying surviving spouse"],
 ])}</div></fieldset>
 ${numberSpecs.map(([title, specs]) => `<fieldset><legend>${title}</legend><div class="field-grid">${specs.map(field).join("")}</div></fieldset>`).join("")}<p id="scenario-error" class="error-message" role="alert"></p></div><div class="drawer-actions"><button type="button" class="button secondary" data-action="reset">Reset synthetic defaults</button><button class="button" type="submit">Recalculate all paths ${icon("arrow", 16)}</button></div></form>`;
}
const renders = {
  overview,
  summary,
  questions,
  compare,
  projections,
  "black-swan": blackSwan,
  taxes,
  timeline,
  planning,
  suggestions,
  sources,
  glossary,
  flagged,
  privacy,
  briefing,
};
const routeLabel = (r) =>
  r === "briefing"
    ? "Professional brief"
    : (groups.flatMap((g) => g.items).find((x) => x[0] === r)?.[1] ??
      "Overview");
function shell() {
  return `<div class="app-shell"><aside class="sidebar" id="sidebar" aria-label="Main navigation"><a class="brand" href="#overview" aria-label="Estate Decision Lab overview"><span class="brand-mark">e.</span><span><strong>Estate</strong><small>DECISION LAB</small></span></a><button class="icon-button nav-close" data-action="close-menu" aria-label="Close navigation">${icon("close")}</button><div class="workspace-label"><i class="status-dot"></i> PUBLIC-SAFE WORKSPACE</div><nav>${groups.map((g) => `<div class="nav-group"><p>${g.name}</p>${g.items.map(([r, l, i]) => `<a href="#${r}" ${route() === r ? 'aria-current="page"' : ""}>${icon(i, 18)}<span>${l}</span>${r === "flagged" ? '<b class="nav-count">' + FLAGS.length + "</b>" : ""}</a>`).join("")}</div>`).join("")}</nav><div class="sidebar-bottom"><a href="#briefing">${icon("briefing", 18)}<span>Attorney & CPA brief</span>${icon("external", 12)}</a><p><i class="status-dot"></i> No private data loaded</p><small>Official rules. Visible unknowns.<br>A decision you can explain.</small></div></aside><button class="nav-scrim" data-action="close-menu" aria-label="Close navigation" hidden></button><div class="workspace"><header class="topbar"><div><button class="icon-button mobile-menu" data-action="menu" aria-label="Open navigation" aria-controls="sidebar" aria-expanded="false">${icon("menu")}</button><span class="breadcrumb">PLANNING WORKSPACE <b>/</b> <strong id="breadcrumb-label">${routeLabel(route())}</strong></span></div><div class="topbar-right"><span class="reviewed"><i class="status-dot"></i> Reviewed ${REVIEW_DATE}</span><a class="avatar" href="#privacy" aria-label="Privacy and limits">${icon("privacy", 17)}</a></div></header><p id="live-status" class="sr-only" aria-live="polite" role="status"></p><main id="main" tabindex="-1"></main><footer class="site-footer"><span><strong>Estate / Decision Lab</strong> · v${MODEL_VERSION}</span><span>Hypothetical scenarios. Not legal, tax or investment advice.</span><a href="#sources">Official sources ${icon("external", 11)}</a></footer></div></div><dialog id="controls-dialog" aria-labelledby="controls-title"></dialog>`;
}
function renderMain(focus = false) {
  const r = route();
  $("#main").innerHTML = renders[r]();
  $("#breadcrumb-label").textContent = routeLabel(r);
  document.title = `${routeLabel(r)} / Estate Decision Lab`;
  $$(".sidebar nav a").forEach((a) => {
    if (a.getAttribute("href") === "#" + r)
      a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
  if (focus) {
    window.scrollTo(0, 0);
    $("#page-title")?.focus({ preventScroll: true });
  }
}
function syncNavigation() {
  const mobile = matchMedia("(max-width:800px)").matches,
    open = document.body.classList.contains("menu-open");
  $("#sidebar").inert = mobile && !open;
  $(".workspace").inert = mobile && open;
  if (mobile && !open) $("#sidebar").setAttribute("aria-hidden", "true");
  else $("#sidebar").removeAttribute("aria-hidden");
}
function closeMenu() {
  document.body.classList.remove("menu-open");
  $(".nav-scrim").hidden = true;
  $('[data-action="menu"]').setAttribute("aria-expanded", "false");
  syncNavigation();
}
function openControls() {
  $("#controls-dialog").innerHTML = controlsMarkup();
  $("#controls-dialog").showModal();
  document.body.classList.add("dialog-open");
}
function closeControls() {
  $("#controls-dialog").close();
  document.body.classList.remove("dialog-open");
}
function applyInputs(next, reset = false) {
  const previous = leader(),
    newComparison = rangeComparison(next);
  inputs = next;
  comparison = newComparison;
  runNumber++;
  distributionCache = "";
  const moved = previous !== leader();
  runMessage = `${moved ? "Illustrative leader changed: " + pathShort(previous) + " → " + pathShort(leader()) : "Illustrative leader unchanged: " + pathShort(leader())}. Household recommendation not made.`;
  if (reset) runMessage = "Synthetic defaults restored. " + runMessage;
  renderMain(false);
  $("#live-status").textContent = runMessage;
}
function download(text, name, type) {
  const a = document.createElement("a"),
    url = URL.createObjectURL(new Blob([text], { type }));
  a.href = url;
  a.download = name;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
const csvCell = (v) => `"${String(v ?? "").replaceAll('"', '""')}"`;
function exportCSV() {
  const r = comparison.find((v) => v.path === selectedPath),
    headers = [
      "synthetic_only",
      "path",
      "model_version",
      "rule_review_date",
      "year",
      "calendar_year_end",
      "A_market",
      "A_assessment_for_billed_period",
      "A_adjusted_basis",
      "B_market",
      "B_assessment_for_billed_period",
      "property_tax_A",
      "property_tax_B",
      "rent_A",
      "rent_B",
      "operating",
      "capital_A",
      "capital_B",
      "depreciation_A",
      "depreciation_B",
      "income_and_investment_tax",
      "debt_interest",
      "debt_principal",
      "ending_debt_A",
      "ending_debt_B",
      "net_property_cash_flow",
      "sale_net",
      "sale_tax",
      "stocks",
      "treasuries",
      "funding_gap",
      "realizable_nominal",
      "realizable_2026_dollars",
      "B_retained_equity_before_exit_tax_excluded",
      "official_rule_context",
    ];
  const rows = r.rows.map((x) => [
    "YES",
    r.path,
    MODEL_VERSION,
    REVIEW_DATE,
    x.year,
    x.calendarYear,
    ...[
      "marketA",
      "assessedA",
      "basisA",
      "marketB",
      "assessedB",
      "propertyTaxA",
      "propertyTaxB",
      "rentA",
      "rentB",
      "operating",
      "capexA",
      "capexB",
      "depreciationA",
      "depreciationB",
      "taxes",
      "interest",
      "principal",
      "debtA",
      "debtB",
      "netCash",
      "saleNet",
      "saleTax",
      "stocks",
      "treasuries",
      "funding",
      "nominal",
      "real",
      "bRetainedEquity",
    ].map((k) => money10(x[k] ?? 0)),
    [
      SOURCES.basis.url,
      SOURCES.rental.url,
      SOURCES.prop13.url,
      SOURCES.gains.url,
    ].join(" | "),
  ]);
  download(
    [headers, ...rows].map((row) => row.map(csvCell).join(",")).join("\r\n"),
    `synthetic-${r.path}-${utcDate()}.csv`,
    "text/csv;charset=utf-8",
  );
}
function exportDecisions() {
  download(
    JSON.stringify(
      {
        scope:
          "Tab-only suggestion review; not household authorization or implementation",
        exported: utcDate(),
        modelVersion: MODEL_VERSION,
        householdDecision: null,
        items: SUGGESTIONS.map((s) => ({
          id: s.id,
          suggestion: s.title,
          status: decisions.get(s.id)?.status ?? "Not reviewed",
          reviewDate: decisions.get(s.id)?.date ?? null,
          templateReason: decisions.get(s.id)?.reason ?? null,
          implemented: false,
          officialSources: s.sources.map((k) => SOURCES[k].url),
        })),
      },
      null,
      2,
    ),
    `suggestion-review-${utcDate()}.json`,
    "application/json",
  );
}
$("#app").innerHTML = shell();
renderMain();
syncNavigation();
matchMedia("(max-width:800px)").addEventListener("change", () => closeMenu());
window.addEventListener("hashchange", () => {
  closeMenu();
  renderMain(true);
});
document.addEventListener("click", (event) => {
  const skip = event.target.closest(".skip-link");
  if (skip) {
    event.preventDefault();
    $("#main").focus();
    return;
  }
  if (event.target.closest(".sidebar a")) closeMenu();
  const selected = event.target.closest("[data-select-path]");
  if (selected) {
    selectedPath = selected.dataset.selectPath;
  }
  const q = event.target.closest("[data-question-filter]");
  if (q) {
    questionFilter = q.dataset.questionFilter;
    renderMain();
    $(`[data-question-filter="${questionFilter}"]`).focus();
    return;
  }
  const sf = event.target.closest("[data-suggestion-filter]");
  if (sf) {
    suggestionFilter = sf.dataset.suggestionFilter;
    renderMain();
    $(`[data-suggestion-filter="${suggestionFilter}"]`).focus();
    return;
  }
  const sc = event.target.closest("[data-scenario]");
  if (sc) {
    applyInputs({ ...inputs, scenario: sc.dataset.scenario });
    $(`[data-scenario="${inputs.scenario}"]`).focus();
    return;
  }
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (action === "controls") openControls();
  if (action === "close-controls") closeControls();
  if (action === "menu") {
    const open = !document.body.classList.contains("menu-open");
    document.body.classList.toggle("menu-open", open);
    $(".nav-scrim").hidden = !open;
    $('[data-action="menu"]').setAttribute("aria-expanded", String(open));
    syncNavigation();
    if (open) $(".sidebar a[aria-current]")?.focus();
  }
  if (action === "close-menu") {
    closeMenu();
    $('[data-action="menu"]').focus();
  }
  if (action === "reset") {
    applyInputs(defaultInputs(), true);
    $("#controls-dialog").innerHTML = controlsMarkup();
  }
  if (action === "print") window.print();
  if (action === "csv") exportCSV();
  if (action === "decisions") exportDecisions();
});
document.addEventListener("change", (event) => {
  if (event.target.id === "path-select") {
    selectedPath = event.target.value;
    renderMain();
    $("#path-select").focus();
  }
  if (event.target.matches("[data-decision-id]")) {
    const id = event.target.dataset.decisionId,
      status = event.target.value;
    if (status === "Not reviewed") decisions.delete(id);
    else
      decisions.set(id, {
        status,
        date: utcDate(),
        reason:
          status === "Prioritize"
            ? "Prioritize for professional discussion; no implementation authorized."
            : "Defer professional discussion; no household transaction chosen.",
      });
    renderMain();
    $(`[data-decision-id="${id}"]`)?.focus();
  }
});
document.addEventListener("input", (event) => {
  if (event.target.id === "source-search") {
    const pos = event.target.selectionStart;
    sourceQuery = event.target.value;
    renderMain();
    const search = $("#source-search");
    search.focus();
    if (typeof pos === "number") search.setSelectionRange(pos, pos);
  }
});
document.addEventListener("submit", (event) => {
  if (event.target.id !== "scenario-form") return;
  event.preventDefault();
  const form = event.target,
    data = new FormData(form),
    next = { ...inputs };
  for (const [key, old] of Object.entries(inputs)) {
    if (typeof old === "boolean") {
      next[key] = data.has(key);
      continue;
    }
    if (!data.has(key)) continue;
    const input = form.elements.namedItem(key);
    next[key] =
      typeof old === "number"
        ? Number(data.get(key)) / (input?.dataset.kind === "%" ? 100 : 1)
        : data.get(key);
  }
  try {
    applyInputs(next);
    closeControls();
  } catch (err) {
    $("#scenario-error").textContent = "Could not run: " + err.message;
    $("#scenario-error").scrollIntoView({ block: "center" });
  }
});
$("#controls-dialog").addEventListener("cancel", () =>
  document.body.classList.remove("dialog-open"),
);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && document.body.classList.contains("menu-open")) {
    closeMenu();
    $('[data-action="menu"]').focus();
  }
  if (event.key === "Tab" && document.body.classList.contains("menu-open")) {
    const links = $$("a, button", $("#sidebar")),
      first = links[0],
      last = links.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }
});
