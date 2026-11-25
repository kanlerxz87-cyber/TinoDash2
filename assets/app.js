/**
 * TinoDash2 — Privacy-First Inheritance & Tax Decision Engine (Client-Side Interactive Controller)
 * All calculated dollar figures are strictly rounded to the nearest $10 increment.
 */

function r10(val) {
  if (val === null || val === undefined || isNaN(val)) return 0;
  return Math.round(Number(val) / 10) * 10;
}

function fmtUSD(val) {
  if (val === null || val === undefined || isNaN(val)) return "--";
  const rounded = r10(val);
  const sign = rounded < 0 ? "-" : "";
  return sign + "$" + Math.abs(rounded).toLocaleString("en-US");
}

/**
 * Core deterministic simulation matching scripts/build_model.py
 */
function runInheritanceModel(params) {
  const {
    transferYear = 2045,
    horizonYears = 30,
    propAVal2026 = 3100000,
    propBVal2026 = 1800000,
    propAApprec = 0.040,
    propBApprec = 0.035,
    inflation = 0.026,
    cupertinoRentMo = 6400,
    imputedRentMo = 6200,
    sfUnit3RentMo = 3500,
    equityReturn = 0.078,
    treasuryYield = 0.042,
    marginalCaRate = 0.133, // 12.3% + 1% Mental Health Services Tax > $1M
    treasuryStageMonths = 30, // 0, 24, or 36 months
    enableIrc121 = true,
    enableProp19 = true,
    enable1031 = true,
    cashInheritance2026 = 4500000
  } = params;

  const tTransfer = Math.max(0, transferYear - 2026);
  const sccAdValorem = 0.01185;
  const sccFixed2026 = 810;
  const assdABase2026 = 550540;
  const prop19Base2026 = 1044586;

  const fmvAAtTransfer = propAVal2026 * Math.pow(1 + propAApprec, tTransfer);
  const fbyvAAtTransfer = assdABase2026 * Math.pow(1.02, tTransfer);
  const prop19AllowAtTransfer = prop19Base2026 * Math.pow(1.0215, tTransfer);
  const fixedSccTransfer = sccFixed2026 * Math.pow(1.015, tTransfer);

  // Prop 19 occupied assessment vs Full reassessment
  const excludedCeiling = fbyvAAtTransfer + prop19AllowAtTransfer;
  const excessOverCap = Math.max(0, fmvAAtTransfer - excludedCeiling);
  const assdAProp19 = enableProp19 ? (fbyvAAtTransfer + excessOverCap) : fmvAAtTransfer;
  const taxAProp19Yr1 = assdAProp19 * sccAdValorem + fixedSccTransfer;
  const taxAFullReassessYr1 = fmvAAtTransfer * sccAdValorem + fixedSccTransfer;

  // Same-year sale proceeds (IRC §1014 full stepped-up basis)
  const sccTransferTax = (fmvAAtTransfer / 1000.0) * 1.10;
  const recordingFees = 400;
  const brokerageCosts = fmvAAtTransfer * 0.050;
  const totalSellCosts = brokerageCosts + sccTransferTax + recordingFees;
  const netSaleProceeds = fmvAAtTransfer - totalSellCosts;

  const annualPortGrowth = (0.75 * equityReturn + 0.25 * treasuryYield) - 0.0055;
  const annualTreasuryAfterTax = treasuryYield * (1 - 0.35); // CA tax-exempt under 31 U.S.C. §3124

  let port1A = netSaleProceeds;
  let port1B = netSaleProceeds;

  const depreciableBasisA = fmvAAtTransfer * 0.28;
  const annualDepA = depreciableBasisA / 27.5;
  let cumCf2 = 0;
  let cumDep2 = 0;
  let cumCf3 = 0;
  let cumCf4 = 0;
  let port4 = 0;
  let cumCf5 = 0;

  const stageYears = treasuryStageMonths / 12.0;

  for (let h = 0; h < horizonYears; h++) {
    const yrCurr = transferYear + h;
    const t2026 = yrCurr - 2026;
    const infMult = Math.pow(1 + inflation, t2026);
    const fixedScc = sccFixed2026 * Math.pow(1.015, t2026);

    // Path 1A
    port1A *= (1 + annualPortGrowth);

    // Path 1B (Phased 3M-2Y Treasury staging over 24-36 months)
    let eqWeight = 1.0;
    if (stageYears > 0 && h < Math.ceil(stageYears)) {
      eqWeight = Math.min(1.0, (h + 0.5) / stageYears);
    }
    const r1B = eqWeight * annualPortGrowth + (1 - eqWeight) * annualTreasuryAfterTax;
    port1B *= (1 + r1B);

    // Property A yearly metrics
    const valACurr = propAVal2026 * Math.pow(1 + propAApprec, t2026);
    const waterA = 1500 * infMult;
    const elecA = yrCurr <= 2038 ? (-180 * infMult) : (480 * infMult);
    const insAPrim = 1950 * Math.pow(1 + inflation + 0.008, t2026);
    const insALand = 2450 * Math.pow(1 + inflation + 0.008, t2026);
    const maintA = 9600 * infMult;
    const grossRentA = (cupertinoRentMo * 12) * Math.pow(1 + inflation + 0.004, t2026);
    const netRentA = grossRentA * 0.92;

    // Path 2: Rent Property A
    const assdAP2 = fmvAAtTransfer * Math.pow(1.02, h);
    const taxAP2 = assdAP2 * sccAdValorem + fixedScc;
    const noiP2 = netRentA - (taxAP2 + waterA + elecA + insALand + maintA);
    const depYr = h < 27 ? annualDepA : (h === 27 ? annualDepA * 0.5 : 0);
    cumDep2 += depYr;
    const taxableIncP2 = Math.max(0, noiP2 - depYr);
    const afterTaxCfP2 = noiP2 - taxableIncP2 * (0.35 + marginalCaRate);
    cumCf2 = cumCf2 * (1 + annualPortGrowth) + afterTaxCfP2;

    // Path 3: Occupy Property A
    const assdAP3 = assdAProp19 * Math.pow(1.02, h);
    const taxAP3 = assdAP3 * sccAdValorem + fixedScc;
    const opP3 = taxAP3 + waterA + elecA + insAPrim + maintA;
    const imputedBenefit = (imputedRentMo * 12) * infMult;
    const sfRentGrowth = Math.min(0.07, 0.60 * inflation + 0.003);
    const sfUnit3Gross = (sfUnit3RentMo * 12) * Math.pow(1 + sfRentGrowth, h) * Math.pow(1 + inflation, tTransfer);
    const sfUnit3Net = (sfUnit3Gross * 0.90) * (1 - (0.35 + marginalCaRate));
    const netFlowP3 = imputedBenefit + sfUnit3Net - opP3;
    cumCf3 = cumCf3 * (1 + annualPortGrowth) + netFlowP3;

    // Path 4: Occupy 3 yrs then sell with IRC §121
    if (h < 3) {
      cumCf4 = cumCf4 * (1 + annualPortGrowth) + netFlowP3;
      if (h === 2) {
        const sellCosts4 = valACurr * 0.0511 + 400;
        const gain4 = Math.max(0, (valACurr - sellCosts4) - fmvAAtTransfer);
        const ex121 = enableIrc121 ? 500000 : 0;
        const tax4 = Math.max(0, gain4 - ex121) * (0.238 + marginalCaRate);
        port4 = (valACurr - sellCosts4 - tax4) + cumCf4;
      }
    } else {
      port4 *= (1 + annualPortGrowth);
    }

    // Path 5: Rent 7 yrs then 1031 or Taxable Sale
    if (h < 7) {
      cumCf5 = cumCf5 * (1 + annualPortGrowth) + afterTaxCfP2;
      if (h === 6) {
        if (enable1031) {
          cumCf5 += valACurr * 0.985;
        } else {
          const sellCosts5 = valACurr * 0.0511 + 400;
          const dep7 = annualDepA * 7;
          const recapTax = dep7 * (0.25 + 0.038 + marginalCaRate);
          const capGainTax = Math.max(0, (valACurr - sellCosts5) - fmvAAtTransfer) * (0.238 + marginalCaRate);
          cumCf5 += (valACurr - sellCosts5 - recapTax - capGainTax);
        }
      }
    } else {
      cumCf5 *= (1 + (enable1031 ? (annualPortGrowth - 0.002) : annualPortGrowth));
    }
  }

  const valATerminal = propAVal2026 * Math.pow(1 + propAApprec, tTransfer + horizonYears);
  const ltcgCombined = 0.238 + marginalCaRate;

  const nw1A = port1A - Math.max(0, port1A - netSaleProceeds) * 0.35 * ltcgCombined;
  const nw1B = port1B - Math.max(0, port1B - netSaleProceeds) * 0.35 * ltcgCombined;
  const nw2 = valATerminal + cumCf2;
  const nw3 = valATerminal + cumCf3;
  const nw4 = port4 * 0.91;
  const nw5 = enable1031 ? cumCf5 : cumCf5 * 0.91;

  // Federal estate tax check at transferYear
  const infTransfer = Math.pow(1 + inflation, tTransfer);
  const fedExclSingle = 15000000 * infTransfer;
  const cashAtTransfer = cashInheritance2026 * Math.pow(1.045, tTransfer);
  const grossEstate = fmvAAtTransfer + cashAtTransfer;
  const estateTaxSingle = Math.max(0, grossEstate - fedExclSingle) * 0.40;
  const estateTaxPortability = Math.max(0, grossEstate - fedExclSingle * 2) * 0.40;

  const paths = [
    {
      id: "path_1a",
      name: "Path 1A (Pure): Same-Year Sale & Lump-Sum Portfolio",
      type: "Pure Choice",
      yr1Tax: 0,
      day1Proceeds: r10(netSaleProceeds),
      terminalWealth: r10(nw1A),
      reinvestmentRisk: "High Crash-Entry Exposure (100% Equity Day 1)",
      notes: "Full IRC §1014 step-up ($0 cap gains tax); stay in SF Unit 3."
    },
    {
      id: "path_1b",
      name: `Path 1B (Mixed): Same-Year Sale + ${treasuryStageMonths}m 3M–2Y Treasury Ladder -> Stocks`,
      type: "Mixed / Staged",
      yr1Tax: 0,
      day1Proceeds: r10(netSaleProceeds),
      terminalWealth: r10(nw1B),
      reinvestmentRisk: "Low — Softens 1929/2008 crash entry drawdown by +24% to +38%",
      notes: "Parks proceeds in CA-tax-exempt Treasuries; phases into equities."
    },
    {
      id: "path_4",
      name: "Path 4 (Mixed): Live in Property A 3 Yrs (Prop 19 + IRC §121), Then Sell",
      type: "Mixed Path",
      yr1Tax: r10(taxAProp19Yr1),
      day1Proceeds: 0,
      terminalWealth: r10(nw4),
      reinvestmentRisk: "Moderate — 3-yr delayed entry + 3 yrs of Prop 19 partial property tax",
      notes: enableIrc121 ? "Uses $500k IRC §121 exclusion on post-inheritance gain." : "IRC §121 switched OFF."
    },
    {
      id: "path_3",
      name: "Path 3 (Pure): Occupy Property A Long-Term (Claim Prop 19 Exclusion)",
      type: "Pure Choice",
      yr1Tax: r10(taxAProp19Yr1),
      day1Proceeds: 0,
      terminalWealth: r10(nw3),
      reinvestmentRisk: "Low timing risk; High Bay Area single-parcel concentration risk",
      notes: enableProp19 ? "BOE-19-P shelters FBYV + $1M inflation-adjusted cap; rent SF Unit 3." : "Prop 19 switched OFF (full reassessment)."
    },
    {
      id: "path_5",
      name: `Path 5 (Mixed): Rent Property A 7 Yrs, Then ${enable1031 ? "IRC §1031 Exchange" : "Taxable Sale"}`,
      type: "Mixed Path",
      yr1Tax: r10(taxAFullReassessYr1),
      day1Proceeds: 0,
      terminalWealth: r10(nw5),
      reinvestmentRisk: "Moderate — Suffers 7 yrs of full Prop 19 tax reset before exit",
      notes: enable1031 ? "Defers cap gains & §1250 depreciation recapture via 1031 DST." : "Pays 25% Fed + 13.3% CA §1250 recapture at Year 7."
    },
    {
      id: "path_2",
      name: "Path 2 (Pure): Rent Out Property A Long-Term (Full Prop 19 Reassessment)",
      type: "Pure Choice",
      yr1Tax: r10(taxAFullReassessYr1),
      day1Proceeds: 0,
      terminalWealth: r10(nw2),
      reinvestmentRisk: "Severe Property Tax Drag — Prop 19 reset consumes ~50% of gross rent",
      notes: "No Prop 19 exclusion on non-primary residence; 27.5-yr depreciation."
    }
  ];

  const sorted = [...paths].sort((a, b) => b.terminalWealth - a.terminalWealth);

  return {
    fmvAAtTransfer: r10(fmvAAtTransfer),
    fbyvAAtTransfer: r10(fbyvAAtTransfer),
    prop19AllowAtTransfer: r10(prop19AllowAtTransfer),
    taxAProp19Yr1: r10(taxAProp19Yr1),
    taxAFullReassessYr1: r10(taxAFullReassessYr1),
    netSaleProceeds: r10(netSaleProceeds),
    totalSellCosts: r10(totalSellCosts),
    fedExclSingle: r10(fedExclSingle),
    grossEstate: r10(grossEstate),
    estateTaxSingle: r10(estateTaxSingle),
    estateTaxPortability: r10(estateTaxPortability),
    paths,
    sorted,
    topWinner: sorted[0],
    runnerUp: sorted[1]
  };
}

/**
 * Bind interactive What-If controls if present on the current page
 */
function initWhatIfControls() {
  const form = document.getElementById("whatif-form");
  if (!form) return;

  const updateView = () => {
    const transferYear = Number(document.getElementById("ctrl-transfer-year").value);
    const horizonYears = Number(document.getElementById("ctrl-horizon").value);
    const propAApprec = Number(document.getElementById("ctrl-apprec-a").value) / 100;
    const cupertinoRentMo = Number(document.getElementById("ctrl-rent-a").value);
    const imputedRentMo = Number(document.getElementById("ctrl-imputed-rent").value);
    const equityReturn = Number(document.getElementById("ctrl-equity-ret").value) / 100;
    const treasuryYield = Number(document.getElementById("ctrl-treasury-yield").value) / 100;
    const marginalCaRate = Number(document.getElementById("ctrl-ca-tax").value) / 100;
    const treasuryStageMonths = Number(document.getElementById("ctrl-stage-months").value);
    const cashInheritance2026 = Number(document.getElementById("ctrl-cash-estate").value);
    const enableProp19 = document.getElementById("ctrl-prop19").checked;
    const enableIrc121 = document.getElementById("ctrl-irc121").checked;
    const enable1031 = document.getElementById("ctrl-1031").checked;

    // Update value labels
    document.getElementById("val-transfer-year").textContent = transferYear;
    document.getElementById("val-horizon").textContent = horizonYears + " yrs";
    document.getElementById("val-apprec-a").textContent = (propAApprec * 100).toFixed(1) + "%/yr";
    document.getElementById("val-rent-a").textContent = fmtUSD(cupertinoRentMo) + "/mo";
    document.getElementById("val-imputed-rent").textContent = fmtUSD(imputedRentMo) + "/mo";
    document.getElementById("val-equity-ret").textContent = (equityReturn * 100).toFixed(1) + "%/yr";
    document.getElementById("val-treasury-yield").textContent = (treasuryYield * 100).toFixed(1) + "%/yr";
    document.getElementById("val-ca-tax").textContent = (marginalCaRate * 100).toFixed(1) + "%";
    document.getElementById("val-stage-months").textContent = treasuryStageMonths + " mos";
    document.getElementById("val-cash-estate").textContent = fmtUSD(cashInheritance2026);

    const res = runInheritanceModel({
      transferYear,
      horizonYears,
      propAApprec,
      cupertinoRentMo,
      imputedRentMo,
      equityReturn,
      treasuryYield,
      marginalCaRate,
      treasuryStageMonths,
      enableProp19,
      enableIrc121,
      enable1031,
      cashInheritance2026
    });

    // Update Recommendation Moved Banner
    const banner = document.getElementById("rec-move-banner");
    const baselineId = "path_1a";
    const moved = res.topWinner.id !== baselineId;
    if (banner) {
      banner.className = "rec-status-banner " + (moved ? "rec-status-moved" : "rec-status-unchanged");
      banner.innerHTML = moved
        ? `<div><strong>RECOMMENDATION MOVED:</strong> Top path shifted from <em>Path 1A (Same-Year Sale)</em> to <strong>${res.topWinner.name}</strong> (${fmtUSD(res.topWinner.terminalWealth)} terminal wealth, +${fmtUSD(res.topWinner.terminalWealth - res.runnerUp.terminalWealth)} ahead of #2).</div><span class="badge badge-flagged">Decision Flipped</span>`
        : `<div><strong>MODEL REBUILT — RECOMMENDATION UNCHANGED:</strong> <strong>${res.topWinner.name}</strong> remains #1 (${fmtUSD(res.topWinner.terminalWealth)}), with <strong>Path 1B (${treasuryStageMonths}m Treasury Staging)</strong> at ${fmtUSD(res.paths[1].terminalWealth)} providing Black Swan crash protection.</div><span class="badge badge-verified">Baseline Holds</span>`;
    }

    // Update KPI cards if present
    const kpiFmv = document.getElementById("kpi-fmv-transfer");
    if (kpiFmv) kpiFmv.textContent = fmtUSD(res.fmvAAtTransfer);
    const kpiNetSale = document.getElementById("kpi-net-sale");
    if (kpiNetSale) kpiNetSale.textContent = fmtUSD(res.netSaleProceeds);
    const kpiTaxOcc = document.getElementById("kpi-tax-occupy");
    if (kpiTaxOcc) kpiTaxOcc.textContent = fmtUSD(res.taxAProp19Yr1) + "/yr";
    const kpiTaxRent = document.getElementById("kpi-tax-rent");
    if (kpiTaxRent) kpiTaxRent.textContent = fmtUSD(res.taxAFullReassessYr1) + "/yr";
    const kpiEstateTax = document.getElementById("kpi-estate-tax");
    if (kpiEstateTax) {
      kpiEstateTax.textContent = fmtUSD(res.estateTaxSingle);
      document.getElementById("kpi-estate-sub").textContent =
        `Gross Estate: ${fmtUSD(res.grossEstate)} vs ${fmtUSD(res.fedExclSingle)} 1-Spouse Excl. (${fmtUSD(res.estateTaxPortability)} w/ DSUE Portability)`;
    }

    // Update dynamic comparison table rows
    const tbody = document.getElementById("whatif-paths-tbody");
    if (tbody) {
      tbody.innerHTML = res.sorted
        .map((p, idx) => {
          const isTop = idx === 0;
          const diffFromTop = p.terminalWealth - res.topWinner.terminalWealth;
          return `<tr class="${isTop ? "row-highlight" : ""}">
            <td><span class="badge ${isTop ? "badge-verified" : "badge-info"}">#${idx + 1}</span></td>
            <td><strong>${p.name}</strong><div style="font-size:11.5px;color:#64748b;">${p.notes}</div></td>
            <td><span class="badge badge-purple">${p.type}</span></td>
            <td class="num">${fmtUSD(p.day1Proceeds)}</td>
            <td class="num">${fmtUSD(p.yr1Tax)}</td>
            <td class="num"><strong>${fmtUSD(p.terminalWealth)}</strong></td>
            <td class="num">${idx === 0 ? '<span class="badge badge-verified">Leader</span>' : fmtUSD(diffFromTop)}</td>
            <td>${p.reinvestmentRisk}</td>
          </tr>`;
        })
        .join("");
    }
  };

  form.querySelectorAll("input, select").forEach((el) => {
    el.addEventListener("input", updateView);
    el.addEventListener("change", updateView);
  });

  const resetBtn = document.getElementById("btn-reset-whatif");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      document.getElementById("ctrl-transfer-year").value = 2045;
      document.getElementById("ctrl-horizon").value = 30;
      document.getElementById("ctrl-apprec-a").value = 4.0;
      document.getElementById("ctrl-rent-a").value = 6400;
      document.getElementById("ctrl-imputed-rent").value = 6200;
      document.getElementById("ctrl-equity-ret").value = 7.8;
      document.getElementById("ctrl-treasury-yield").value = 4.2;
      document.getElementById("ctrl-ca-tax").value = 13.3;
      document.getElementById("ctrl-stage-months").value = 30;
      document.getElementById("ctrl-cash-estate").value = 4500000;
      document.getElementById("ctrl-prop19").checked = true;
      document.getElementById("ctrl-irc121").checked = true;
      document.getElementById("ctrl-1031").checked = true;
      updateView();
    });
  }

  updateView();
}

document.addEventListener("DOMContentLoaded", () => {
  initWhatIfControls();
});
