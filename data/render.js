/* Estate Pathways — model renderers + browser-only what-if calculator.
   Loads data/model.js (rounded to $10, owner policy 2026-11-25).
   No analytics, no network calls. Figures are planning estimates, not advice. */
(() => {
  'use strict';
  const M = window.MODEL || null;
  const $ = (id) => document.getElementById(id);
  const fmt = (v) => (v === null || v === undefined) ? '—' : '$' + Number(v).toLocaleString('en-US');
  const pctS = (v) => v + '%';
  const SRC = {
    prop13: 'https://www.boe.ca.gov/proptaxes/pub29.htm',
    prop19: 'https://www.boe.ca.gov/prop19/',
    lta: 'https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf',
    irsEstate: 'https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax',
    irs523: 'https://www.irs.gov/publications/p523',
    irs551: 'https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances',
    ftb540: 'https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html',
    damodaran: 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html',
    treasury: 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates',
    hud: 'https://www.huduser.gov/portal/datasets/fmr.html',
    scc: 'https://www.sccassessor.org/',
    sfmta: 'https://www.sfmta.com/getting-around/muni/parcel',
    sfrb: 'https://www.sf.gov/departments/rent-board',
    sco: 'https://www.sco.ca.gov/ardtax_estate_tax.html',
    method: 'pages/comparison.html#method',
  };

  // ---------------- history tables ----------------
  function renderHistory() {
    const mk = (rows, elId, note) => {
      const el = $(elId); if (!el || !M) return;
      el.innerHTML = rows.map(r =>
        `<tr><td>${r.year}</td><td>${r.taxes === null ? '<span class="warn-chip">not provided</span>' : fmt(r.taxes)}</td><td>${fmt(r.assessed)}</td><td>${(r.note || '')}</td><td><a href="${SRC.scc}">Santa Clara Assessor / SF Assessor portals</a> · <span class="warn-chip">household record, rounded; verify against the parcel bill</span></td></tr>`
      ).join('');
    };
    if (!M) return;
    mk(M.history_a, 'histA');
    mk(M.history_b, 'histB');
  }

  // ---------------- assumption ranges ----------------
  function renderAssumptions() {
    const el = $('assumptionRanges'); if (!el || !M) return;
    const a = M.assumptions;
    const rows = [
      ['Property A value (2026)', `${fmt(a.property_a.value_2026_low)} – ${fmt(a.property_a.value_2026_high)} (base ${fmt(a.property_a.value_2026_base)})`, a.property_a.value_note, SRC.scc],
      ['Property A appreciation', `${pctS(a.property_a.appreciation_low)} – ${pctS(a.property_a.appreciation_high)} / yr (base ${pctS(a.property_a.appreciation_base)})`, 'ASSUMPTION range; long-run CA appreciation varies by decade.', SRC.damodaran],
      ['Property A effective property-tax rate', `${pctS(a.property_a.effective_tax_rate_low_pct)} – ${pctS(a.property_a.effective_tax_rate_high_pct)} (base ${pctS(a.property_a.effective_tax_rate_base_pct)})`, a.property_a.tax_rate_note, SRC.scc],
      ['Property A water / electricity (solar)', `${fmt(a.property_a.water_mo_low)} – ${fmt(a.property_a.water_mo_high)} /mo water; net electricity ${fmt(a.property_a.elec_net_mo_low)} – ${fmt(a.property_a.elec_net_mo_high)} /mo`, a.property_a.elec_note, SRC.scc],
      ['Property A insurance', `${fmt(a.property_a.insurance_yr_low)} – ${fmt(a.property_a.insurance_yr_high)} /yr (base ${fmt(a.property_a.insurance_yr_base)})`, a.property_a.insurance_note, 'https://www.insurance.ca.gov/'],
      ['Property A market rent', `${fmt(a.property_a.market_rent_mo_low)} – ${fmt(a.property_a.market_rent_mo_high)} /mo (base ${fmt(a.property_a.market_rent_mo_base)})`, a.property_a.market_rent_note, SRC.hud],
      ['Property B value (2026)', `${fmt(a.property_b.value_2026_low)} – ${fmt(a.property_b.value_2026_high)} (base ${fmt(a.property_b.value_2026_base)})`, 'Household estimate, rounded.', 'https://www.sftreasurer.org/property'],
      ['Property B rent (2 units)', `${fmt(a.property_b.rent_mo_low)} – ${fmt(a.property_b.rent_mo_high)} /mo (base ${fmt(a.property_b.rent_mo_base)})`, a.property_b.rent_note, SRC.sfrb],
      ['Property B effective property-tax rate', `${pctS(a.property_b.effective_tax_rate_low_pct)} – ${pctS(a.property_b.effective_tax_rate_high_pct)} (base ${pctS(a.property_b.effective_tax_rate_base_pct)})`, a.property_b.tax_rate_note, 'https://www.sftreasurer.org/property'],
      ['Property B insurance / Prop H parcel tax', `${fmt(a.property_b.insurance_yr_low)} – ${fmt(a.property_b.insurance_yr_high)} /yr insurance; Prop H ${fmt(a.property_b.prop_h_annual)} /yr from FY2027-28`, a.property_b.prop_h_note, SRC.sfmta],
      ['Inflation', `${pctS(a.macro.inflation_low)} – ${pctS(a.macro.inflation_high)} (base ${pctS(a.macro.inflation_base)})`, a.macro.inflation_note, 'https://www.federalreserve.gov/monetarypolicy/fomc.htm'],
      ['Stocks (nominal)', `${pctS(a.macro.stock_nom_low)} – ${pctS(a.macro.stock_nom_high)} /yr (base ${pctS(a.macro.stock_nom_base)})`, a.macro.stock_note, SRC.damodaran],
      ['Treasury phase-in yield', `${pctS(a.macro.tbill_low)} – ${pctS(a.macro.tbill_high)} /yr (base ${pctS(a.macro.tbill_base)})`, a.macro.tbill_note, SRC.treasury],
    ];
    el.innerHTML = rows.map(r => `<tr><td><strong>${r[0]}</strong></td><td>${r[1]}</td><td>${r[2]} <span class="warn-chip">assumption / unverified where noted</span></td><td><a href="${r[3]}">official source / register</a></td></tr>`).join('');
  }

  // ---------------- sale stack ----------------
  function renderSaleStack() {
    const el = $('saleStack'); if (!el || !M) return;
    el.innerHTML = M.sale_stack_a.map(r =>
      `<tr><td>${r.line}</td><td>${fmt(r.amount)}</td><td>${r.basis}</td><td><a href="${SRC.irs551}">IRS basis rules</a> · <a href="pages/tax-legal.html#transfer">local transfer-tax detail</a></td></tr>`
    ).join('');
  }

  // ---------------- capital plans ----------------
  function renderCapital() {
    const mk = (rows, elId) => {
      const el = $(elId); if (!el) return;
      el.innerHTML = rows.map(r =>
        `<tr><td>${r.item}</td><td>${r.window}</td><td>${fmt(r.low)}</td><td>${fmt(r.base)}</td><td>${fmt(r.high)}</td><td><span class="warn-chip">${r.status}</span> · <a href="https://www.cslb.ca.gov/">CSLB</a></td></tr>`
      ).join('');
    };
    if (!M) return;
    mk(M.capital_plan_a, 'capA');
    mk(M.capital_plan_b, 'capB');
  }

  // ---------------- year-by-year projections ----------------
  function renderProjections() {
    const el = $('projectionRows'); if (!el || !M) return;
    el.innerHTML = M.projections.map(p => {
      const ph = p.b_prop_h ? ` + Prop H ${fmt(p.b_prop_h)}` : '';
      return `<tr><td>${p.year}</td><td>${fmt(p.a_value.low)}</td><td>${fmt(p.a_value.base)}</td><td>${fmt(p.a_value.high)}</td><td>${fmt(p.a_assessed)}</td><td>${fmt(p.a_tax.base)}</td><td>${fmt(p.a_opex.base)}</td><td>${fmt(p.b_value.base)}</td><td>${fmt(p.b_assessed)}</td><td>${fmt(p.b_tax.base)}${ph}</td><td><a href="${SRC.prop13}">Prop 13 basis</a> · <a href="#method">method</a></td></tr>`;
    }).join('');
  }

  // ---------------- comparison engine (page control) ----------------
  function renderComparison() {
    const selTy = $('cmpYear'), selH = $('cmpHorizon'), selC = $('cmpCase'), body = $('comparisonRows'), dist = $('cmpDistribution');
    if (!selTy || !M) return;
    const pick = () => {
      const ty = Number(selTy.value), h = Number(selH.value), c = selC.value;
      const rec = M.comparisons.find(x => x.transfer_year === ty && x.horizon === h && x.case === c);
      if (!rec) return;
      $('cmpMeta').innerHTML = `Transfer year <strong>${ty}</strong> · horizon <strong>${h} years</strong> · case <strong>${c}</strong> · Property A value at transfer ${fmt(rec.value_at_transfer)} · same-year net proceeds ${fmt(rec.net_proceeds_same_year)} · property tax at transfer ${fmt(rec.prop_tax_at_transfer)}/yr. <a href="#method">Method</a>`;
      const order = ['sell_same_year', 'sell_phase24', 'sell_phase36', 'mixed_70_30', 'live_in', 'live_then_sell', 'rent_out', 'rent_then_sell', 'live2_then_rent'];
      const rows = order.map(k => rec.paths[k]).filter(Boolean);
      const max = Math.max(...rows.map(r => r.terminal));
      body.innerHTML = rows.map(r => {
        const risky = r.name.includes('phase');
        return `<tr><td><strong>${r.name}</strong><br><span class="mini">${r.note}</span>${risky ? '<br><span class="warn-chip">Reinvestment risk beside the headline: each maturity resets at then-current yields — cash drag in a bull run is the price of crash protection.</span>' : ''}</td><td>${fmt(r.terminal)}</td><td>${fmt(r.terminal_real)}</td><td><a href="#method">method</a> · <a href="${SRC.irs551}">basis</a> · <a href="${SRC.prop19}">Prop 19</a></td></tr>`;
      }).join('');
      if (dist) {
        dist.innerHTML = rows.map((r, i) =>
          `<div class="bar-row"><span>${r.name.split('(')[0].trim()}</span><div class="bar-wrap"><div class="bar ${i % 3 === 1 ? 'b2' : i % 3 === 2 ? 'b3' : ''}" style="width:${Math.max(2, (r.terminal / max) * 100).toFixed(1)}%"></div></div><span>${fmt(r.terminal)}</span></div>`
        ).join('');
      }
    };
    [selTy, selH, selC].forEach(s => s.addEventListener('change', pick));
    pick();
  }

  // ---------------- estate + BHS sensitivities ----------------
  function renderEstate() {
    const el = $('estateRows'); if (!el || !M) return;
    el.innerHTML = M.estate_sensitivity.map(r =>
      `<tr><td>${fmt(r.gross_estate)}</td><td>${r.filing}</td><td>${fmt(r.exclusion)}</td><td>${fmt(r.tax_estimated)}</td><td>${pctS(r.effective_rate_pct)}</td><td><a href="${SRC.irsEstate}">IRS 2026 exclusion</a> · <a href="https://www.irs.gov/instructions/i706">Form 706</a></td></tr>`
    ).join('');
  }
  function renderBhs() {
    const el = $('bhsRows'); if (!el || !M) return;
    el.innerHTML = M.bhs_sensitivity.map(r =>
      `<tr><td>${fmt(r.ca_taxable_income)}</td><td>${fmt(r.bhs_tax)}</td><td>1% of CA taxable income over ${fmt(1000000)} (line 62, whole dollars, not indexed)</td><td><a href="${SRC.ftb540}">FTB 2025 Form 540 booklet</a></td></tr>`
    ).join('');
  }

  // ---------------- black-swan replays + decades ----------------
  function renderReplays() {
    const el = $('replayRows'); if (!el || !M) return;
    el.innerHTML = M.replays.map(rep =>
      rep.endpoints.map(e =>
        `<tr><td><strong>${rep.name}</strong><br><span class="mini">${rep.series}</span></td><td>${e.years} years</td><td>${fmt(e.immediate)}</td><td>${fmt(e.phase_24)}</td><td>${fmt(e.phase_36)}</td><td><a href="${SRC.damodaran}">Damodaran annual returns (Jan 2026)</a> · <a href="black-swan.html#method-replay">replay rules</a></td></tr>`
      ).join('')
    ).join('');
  }
  function renderDecades() {
    const el = $('decadeRows'); if (!el || !M) return;
    el.innerHTML = M.decades.map(d =>
      `<tr><td>${d.decade}</td><td>${d.sp_nom_cagr === null ? '—' : pctS(d.sp_nom_cagr)}</td><td>${d.cpi_note}</td><td>${d.regime}</td><td><a href="${SRC.damodaran}">Damodaran series</a></td></tr>`
    ).join('');
  }

  // ---------------- what-if calculator (pre-filled, auto-run) ----------------
  function calcRun() {
    const g = (id) => { const v = Number(($(id) || {}).value); return Number.isFinite(v) ? v : 0; };
    const years = Math.max(1, Math.min(50, g('wifYears')));
    const home = g('wifHome'), gl = g('wifGrowthLow'), gh = g('wifGrowthHigh');
    const sl = g('wifStockLow'), sh = g('wifStockHigh'), infl = g('wifInflation');
    const tb = g('wifTreasury'), phase = g('wifPhaseMonths');
    const crashY = g('wifCrashYear'), dd = g('wifDrawdown');
    const rentMo = g('wifRentMo'), friction = g('wifFriction') / 100;
    const carryYr = g('wifCarryYr'), netRentYr = g('wifNetRentYr');
    const out = $('wifResults'), dist = $('wifDistribution');
    if (!out) return;

    const fv = (p, r, n, crashOn) => {
      let v = p;
      for (let y = 1; y <= n; y += 1) {
        v *= (1 + r / 100);
        if (crashOn && crashY === y && dd > 0) v *= (1 - dd / 100);
      }
      return v;
    };
    const flows = (flow, growth, ret, n) => {
      let t = 0;
      for (let k = 1; k <= n; k += 1) {
        let v = flow * Math.pow(1 + growth / 100, k - 1);
        for (let y = k; y <= n; y += 1) {
          v *= (1 + ret / 100);
          if (crashY === y && dd > 0) v *= (1 - dd / 100);
        }
        t += v;
      }
      return t;
    };
    const phased = (p, n, months, ret, tbill) => {
      const nTr = Math.floor(months / 12) + 1, chunk = p / nTr;
      let t = 0;
      for (let i = 0; i < nTr; i += 1) {
        let v = chunk;
        for (let y = 1; y <= n; y += 1) {
          if (y <= i) v *= (1 + tbill / 100);
          else {
            v *= (1 + ret / 100);
            if (crashY === y && dd > 0) v *= (1 - dd / 100);
          }
        }
        t += v;
      }
      return t;
    };
    const money = (v) => fmt(Math.round(v / 10) * 10);
    const real = (v) => v / Math.pow(1 + infl / 100, years);
    const net = home * (1 - friction);
    const carry = carryYr, netRent = netRentYr, imputed = rentMo * 12 - carry;

    const rows = [
      ['Sell now + invest immediately', fv(net, sl, years, true), fv(net, sh, years, true)],
      [`Sell now + ${phase}-month phase-in`, phased(net, years, phase, sl, tb), phased(net, years, phase, sh, tb)],
      ['Live in (imputed rent net of costs)', fv(home, gl, years, false) + flows(imputed, infl, sl, years), fv(home, gh, years, false) + flows(imputed, infl, sh, years)],
      ['Rent out (net rent + value)', fv(home, gl, years, false) + flows(netRent, infl, sl, years), fv(home, gh, years, false) + flows(netRent, infl, sh, years)],
      ['Mixed 70% equities / 30% Treasuries', 0.7 * fv(net, sl, years, true) + 0.3 * fv(net, tb, years, true), 0.7 * fv(net, sh, years, true) + 0.3 * fv(net, tb, years, true)],
    ];
    out.innerHTML = rows.map(r =>
      `<tr><td>${r[0]}</td><td>${money(r[1])}</td><td>${money(r[2])}</td><td>${money(real(r[1]))} / ${money(real(r[2]))}</td><td><a href="#method">what is excluded</a></td></tr>`
    ).join('');
    const max = Math.max(...rows.map(r => r[2]));
    dist.innerHTML = rows.map((r, i) =>
      `<div class="bar-row"><span>${r[0].split('(')[0].trim()}</span><div class="bar-wrap"><div class="bar ${i % 2 ? 'b2' : ''}" style="width:${Math.max(2, (r[2] / max) * 100).toFixed(1)}%"></div></div><span>${money(r[2])}</span></div>`
    ).join('');
    $('wifStatus').textContent = `Computed from the pre-filled ranges at ${new Date().toLocaleDateString('en-US')} — illustrative, pre-tax, rounded to $10.`;
  }

  // ---------------- boot ----------------
  document.addEventListener('DOMContentLoaded', () => {
    renderHistory(); renderAssumptions(); renderSaleStack(); renderCapital();
    renderProjections(); renderComparison(); renderEstate(); renderBhs();
    renderReplays(); renderDecades();
    const form = $('wifForm');
    if (form) {
      form.addEventListener('submit', (e) => { e.preventDefault(); calcRun(); });
      form.addEventListener('reset', () => setTimeout(calcRun, 0));
      calcRun();
    }
    const pb = $('printBrief');
    if (pb) pb.addEventListener('click', () => window.print());
  });
})();
