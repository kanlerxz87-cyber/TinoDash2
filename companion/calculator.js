/* Browser-only comparison calculator for Estate Pathways.
   No network calls, no storage, no analytics, no remote assets.
   Every field starts empty; nothing is prefilled with household data.
   Rounding: displayed currency is rounded to the nearest $10. */
(function () {
  "use strict";

  var FIELDS = [
    "horizon", "value", "basis", "saleCostPct", "appLow", "appHigh",
    "rentLow", "rentHigh", "imputedRent", "propTax", "insurance", "utilities",
    "maint", "capitalReserve", "vacancyPct", "inflPct",
    "retLow", "retHigh", "taxDragPct", "treasuryPct", "parkMonths", "phaseMonths",
    "otherCaIncome", "gainTaxPct", "reserve"
  ];

  function num(id) {
    var el = document.getElementById(id);
    if (!el || el.value === "") return null;
    var v = parseFloat(el.value);
    return isFinite(v) ? v : null;
  }

  function r10(x) {
    return Math.round(x / 10) * 10;
  }

  function money(x) {
    var neg = x < 0;
    var s = Math.abs(r10(x)).toLocaleString("en-US");
    return (neg ? "−$" : "$") + s;
  }

  /* After-tax capital gain on a sale in year t.
     Basis is the date-of-death fair market value (step-up), so only post-death
     appreciation plus disallowed selling costs create gain. */
  function gainTax(value, basis, saleCostPct, otherIncome, ratePct, s121) {
    var costs = value * saleCostPct / 100;
    var gain = Math.max(0, value - costs - basis - (s121 || 0));
    var tax = gain * ratePct / 100;
    // California additional 1% on taxable income above $1,000,000 (RTC 17043)
    var income = (otherIncome || 0) + gain;
    if (income > 1000000) {
      tax += Math.min(gain, income - 1000000) * 0.01;
    }
    return tax;
  }

  function sellOutcome(value, basis, saleCostPct, otherIncome, ratePct, reserve, s121) {
    var costs = value * saleCostPct / 100;
    var tax = gainTax(value, basis, saleCostPct, otherIncome, ratePct, s121);
    return Math.max(0, value - costs - tax - (reserve || 0));
  }

  function grow(principal, annualPct, years) {
    return principal * Math.pow(1 + annualPct / 100, years);
  }

  /* Park in Treasury bills then buy equities in equal monthly tranches. */
  function phased(principal, treasuryPct, retPct, parkMonths, phaseMonths, years) {
    var months = Math.round(years * 12);
    if (months <= 0) return principal;
    var cash = principal;
    var invested = 0;
    var tranche = 1 / Math.max(1, phaseMonths);
    var tb = Math.pow(1 + treasuryPct / 100, 1 / 12);
    var eq = Math.pow(1 + retPct / 100, 1 / 12);
    for (var m = 0; m < months; m++) {
      invested *= eq;
      if (m < parkMonths) {
        cash *= tb;
      } else if (m < parkMonths + phaseMonths) {
        var buy = cash * tranche;
        cash -= buy;
        invested += buy;
      } else {
        cash *= tb;
      }
    }
    return invested + cash;
  }

  function operatingCosts(v, y, d) {
    var f = Math.pow(1 + d.infl / 100, y);
    var pv = v * Math.pow(1 + d.app / 100, y);
    return (d.propTax * f) + (d.insurance * f) + (d.utilities * f) +
      (pv * (d.maintPct + d.capitalPct) / 100);
  }

  function collect() {
    var d = {
      horizon: num("horizon"),
      value: num("value"),
      basis: num("basis"),
      saleCostPct: num("saleCostPct") || 0,
      appLow: num("appLow") || 0,
      appHigh: num("appHigh") || d_appFallback(),
      rentLow: num("rentLow") || 0,
      rentHigh: num("rentHigh") || 0,
      imputed: num("imputedRent") || 0,
      propTax: num("propTax") || 0,
      insurance: num("insurance") || 0,
      utilities: num("utilities") || 0,
      maintPct: num("maint") || 0,
      capitalPct: num("capitalReserve") || 0,
      vacancyPct: num("vacancyPct") || 0,
      infl: num("inflPct") || 0,
      retLow: num("retLow") || 0,
      retHigh: num("retHigh") || d_retFallback(),
      taxDrag: num("taxDragPct") || 0,
      treasury: num("treasuryPct") || 0,
      park: num("parkMonths") || 0,
      phase: num("phaseMonths") || 0,
      otherIncome: num("otherCaIncome") || 0,
      gainTaxPct: num("gainTaxPct") || 0,
      s121: num("s121cap") || 0,
      reserve: num("reserve") || 0
    };
    if (d.basis === null) d.basis = d.value;
    if (d.appHigh < d.appLow) d.appHigh = d.appLow;
    if (d.retHigh < d.retLow) d.retHigh = d.retLow;
    return d;
  }

  function d_appFallback() { return num("appLow") || 0; }
  function d_retFallback() { return num("retLow") || 0; }

  function build(d, app, rent, ret) {
    var N = d.horizon;
    var defl = Math.pow(1 + d.infl / 100, N);
    var rows = [];

    /* 1. Live in the home. Keeps the asset; pays carrying costs; avoids paying rent. */
    var costs = 0, rentValue = 0;
    for (var y = 1; y <= N; y++) costs += operatingCosts(d.value, y, { infl: d.infl, app: app, propTax: d.propTax, insurance: d.insurance, utilities: d.utilities, maintPct: d.maintPct, capitalPct: d.capitalPct });
    for (var y2 = 1; y2 <= N; y2++) rentValue += d.imputed * 12 * Math.pow(1 + d.infl / 100, y2);
    var liveAsset = grow(d.value, app, N);
    rows.push({
      name: "Live in the inherited home",
      capital: liveAsset - costs + rentValue,
      cash: rentValue - costs,
      asset: liveAsset,
      liquid: "Low — one illiquid asset",
      risk: "Concentration, capital calls, insurability",
      note: "Imputed rent credited as a benefit; not cash. No sale costs or gains."
    });

    /* 2. Rent it out and stay put. */
    var rentNet = 0, rentCosts = 0;
    for (var y3 = 1; y3 <= N; y3++) {
      var gross = rent * 12 * Math.pow(1 + d.infl / 100, y3) * (1 - d.vacancyPct / 100);
      var oc = operatingCosts(d.value, y3, { infl: d.infl, app: app, propTax: d.propTax, insurance: d.insurance, utilities: d.utilities, maintPct: d.maintPct, capitalPct: d.capitalPct });
      rentNet += gross - oc;
      rentCosts += oc;
    }
    rows.push({
      name: "Rent it out, keep owning",
      capital: grow(d.value, app, N) + rentNet,
      cash: rentNet,
      asset: grow(d.value, app, N),
      liquid: "Medium — sale possible but slow",
      risk: "Tenant, vacancy, regulation, recapture",
      note: "Pre-tax net rent; depreciation shield and recapture excluded."
    });

    /* 3. Sell immediately and invest. */
    var proceeds = sellOutcome(d.value, d.basis, d.saleCostPct, d.otherIncome, d.gainTaxPct, d.reserve);
    var lump = grow(proceeds, (ret - d.taxDrag), N);
    rows.push({
      name: "Sell now, invest the proceeds",
      capital: lump,
      cash: 0,
      asset: 0,
      liquid: "High — fully diversified and divisible",
      risk: "Sequence of returns at entry; no rent, no property",
      note: "Net of sale costs, capital-gain tax and the California 1% above $1M."
    });

    /* 4. Sell, park in Treasury bills, then phase into equities. */
    var phasedEnd = phased(proceeds, d.treasury, ret - d.taxDrag, d.park, d.phase, N);
    rows.push({
      name: "Sell, park in Treasuries, phase in",
      capital: phasedEnd,
      cash: 0,
      asset: 0,
      liquid: "High — but partly idle by rule",
      risk: "Cash drag and reinvestment risk; lower crash-entry risk",
      note: (d.park + d.phase) + " months to full equity exposure; bill yield resets at each maturity."
    });

    /* 5. Live in it, then sell and invest. */
    var liveYears = Math.min(2, N);
    var c5 = 0, rv5 = 0;
    for (var y4 = 1; y4 <= liveYears; y4++) {
      c5 += operatingCosts(d.value, y4, { infl: d.infl, app: app, propTax: d.propTax, insurance: d.insurance, utilities: d.utilities, maintPct: d.maintPct, capitalPct: d.capitalPct });
      rv5 += d.imputed * 12 * Math.pow(1 + d.infl / 100, y4);
    }
    var v5 = grow(d.value, app, liveYears);
    var p5 = sellOutcome(v5, d.basis, d.saleCostPct, d.otherIncome, d.gainTaxPct, d.reserve, d.s121);
    var rest5 = grow(p5, ret - d.taxDrag, N - liveYears);
    rows.push({
      name: "Live " + liveYears + " years, then sell",
      capital: rest5 + rv5 - c5,
      cash: rv5 - c5,
      asset: 0,
      liquid: "Low → High after the sale",
      risk: "Exit price risk postponed; eligibility and occupancy must be real",
      note: (d.s121 ? "Section 121 exclusion of " + d.s121 + " applied — only valid if the ownership and use tests are genuinely met." : "Section 121 exclusion switched off; switch it on only if the ownership and use tests are genuinely met.")
    });

    /* 6. Rent for 3 years, then sell and invest. */
    var rentYears = Math.min(3, N);
    var rn6 = 0, c6 = 0;
    for (var y5 = 1; y5 <= rentYears; y5++) {
      var g6 = rent * 12 * Math.pow(1 + d.infl / 100, y5) * (1 - d.vacancyPct / 100);
      var o6 = operatingCosts(d.value, y5, { infl: d.infl, app: app, propTax: d.propTax, insurance: d.insurance, utilities: d.utilities, maintPct: d.maintPct, capitalPct: d.capitalPct });
      rn6 += g6 - o6;
      c6 += o6;
    }
    var v6 = grow(d.value, app, rentYears);
    var p6 = sellOutcome(v6, d.basis, d.saleCostPct, d.otherIncome, d.gainTaxPct, d.reserve);
    var rest6 = grow(p6, ret - d.taxDrag, N - rentYears);
    rows.push({
      name: "Rent " + rentYears + " years, then sell",
      capital: rest6 + rn6,
      cash: rn6,
      asset: 0,
      liquid: "Low until the sale",
      risk: "Tenant and exit risk; recapture on rented years",
      note: "Depreciation taken while rented reduces basis and is recaptured."
    });

    /* 7. Mixed: keep half, sell half. */
    var halfValue = d.value / 2;
    var proceedsHalf = sellOutcome(halfValue, d.basis / 2, d.saleCostPct, d.otherIncome, d.gainTaxPct, d.reserve / 2);
    var keptHalf = grow(halfValue, app, N);
    var c7 = 0, rv7 = 0;
    for (var y6 = 1; y6 <= N; y6++) {
      c7 += operatingCosts(halfValue, y6, { infl: d.infl, app: app, propTax: d.propTax / 2, insurance: d.insurance / 2, utilities: d.utilities / 2, maintPct: d.maintPct, capitalPct: d.capitalPct });
      rv7 += d.imputed * 6 * Math.pow(1 + d.infl / 100, y6);
    }
    var investedHalf = grow(proceedsHalf, ret - d.taxDrag, N);
    rows.push({
      name: "Keep half, sell half",
      capital: keptHalf + investedHalf + rv7 - c7,
      cash: rv7 - c7,
      asset: keptHalf,
      liquid: "Mixed",
      risk: "Diversifies without giving up the home entirely; more complexity",
      note: "A partial sale needs its own valuation, title and tax treatment."
    });

    rows.forEach(function (r) {
      r.real = r.capital / defl;
    });
    return rows;
  }

  function run() {
    var status = document.getElementById("calcStatus");
    var out = document.getElementById("calcOut");
    var d = collect();
    var missing = [];
    if (!d.horizon || d.horizon < 1) missing.push("horizon");
    if (!d.value) missing.push("value at transfer");
    if (!d.retLow && !d.retHigh) missing.push("investment return");
    if (missing.length) {
      out.hidden = true;
      status.textContent = "Still needed: " + missing.join(", ") + ".";
      return;
    }
    var low = build(d, d.appLow, d.rentLow, d.retLow);
    var base = build(d, (d.appLow + d.appHigh) / 2, (d.rentLow + d.rentHigh) / 2, (d.retLow + d.retHigh) / 2);
    var high = build(d, d.appHigh, d.rentHigh, d.retHigh);

    var tbody = document.getElementById("calcRows");
    tbody.innerHTML = "";
    low.forEach(function (row, i) {
      var tr = document.createElement("tr");
      var cells = [
        "<strong>" + row.name + "</strong><span class=\"small muted\"> " + row.note + "</span>",
        money(row.capital),
        money(base[i].capital),
        money(high[i].capital),
        money(row.real) + " – " + money(high[i].real),
        row.liquid,
        row.risk
      ];
      cells.forEach(function (c, j) {
        var td = document.createElement("td");
        td.innerHTML = c;
        if (j > 0 && j < 5) td.style.textAlign = "right";
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    var ranked = low.map(function (r, i) { return [r.name, base[i].capital]; })
      .sort(function (a, b) { return b[1] - a[1]; });
    document.getElementById("calcRank").innerHTML =
      "<strong>Base-case ranking (narrowest reading of the inputs):</strong> " +
      ranked.map(function (r, i) { return (i + 1) + ". " + r[0] + " (" + money(r[1]) + ")"; }).join(" · ") +
      "<br><span class=\"small muted\">A ranking is not a recommendation. It changes with every assumption, and it is blind to everything listed as " +
      "unverified on the questions page.</span>";
    out.hidden = false;
    status.textContent = "Computed in this browser only. Nothing was saved or sent.";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("calcForm");
    if (!form) return;
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    form.addEventListener("reset", function () {
      setTimeout(function () {
        document.getElementById("calcOut").hidden = true;
        document.getElementById("calcStatus").textContent = "No inputs yet.";
      }, 0);
    });
    document.getElementById("calcStatus").textContent = "No inputs yet — every field is blank on purpose.";
  });
})();
