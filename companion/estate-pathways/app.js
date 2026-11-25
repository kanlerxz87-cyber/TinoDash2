(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const form = $('scenarioForm');
  const results = $('modelResults');
  const status = $('modelStatus');
  const resultRows = $('resultRows');
  const distribution = $('distribution');
  const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  const displayMoney = (value) => currency.format(Math.round(value / 10) * 10);
  const number = (id) => {
    const el = $(id);
    if (!el) return null;
    const raw = el.value.trim();
    return raw === '' ? null : Number(raw);
  };
  const validNumber = (value) => Number.isFinite(value);
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

  // Public S&P 500 calendar-year nominal total-return sequences (officialdata.org / Damodaran public series cited on black-swan.html)
  const PUBLIC_HIST_SEQUENCES = {
    '1929': {
      label: '1929–1938 Great Depression cohort',
      eq: [-0.0842, -0.2490, -0.4334, -0.0819, 0.5399, -0.0144, 0.4767, 0.3392, -0.3503, 0.3112],
      ts: [0.0475, 0.0241, 0.0107, 0.0096, 0.0030, 0.0016, 0.0017, 0.0018, 0.0031, 0.0004]
    },
    '1973': {
      label: '1973–1982 Stagflation cohort',
      eq: [-0.1466, -0.2647, 0.3720, 0.2384, -0.0718, 0.0656, 0.1844, 0.3242, -0.0491, 0.2141],
      ts: [0.0693, 0.0800, 0.0580, 0.0508, 0.0512, 0.0718, 0.1038, 0.1124, 0.1471, 0.1054]
    },
    '2000': {
      label: '2000–2009 Two-crash lost decade',
      eq: [-0.0910, -0.1189, -0.2210, 0.2868, 0.1088, 0.0491, 0.1579, 0.0549, -0.3700, 0.2646],
      ts: [0.0582, 0.0340, 0.0161, 0.0101, 0.0137, 0.0315, 0.0473, 0.0436, 0.0137, 0.0015]
    },
    '2008': {
      label: '2008–2017 Great Financial Crisis cohort',
      eq: [-0.3700, 0.2646, 0.1506, 0.0211, 0.1600, 0.3239, 0.1369, 0.0138, 0.1196, 0.2183],
      ts: [0.0137, 0.0015, 0.0014, 0.0005, 0.0009, 0.0006, 0.0003, 0.0005, 0.0032, 0.0093]
    }
  };

  $('printBrief').addEventListener('click', () => window.print());

  // Progressive 2025 California income tax + Form 540 Line 62 1% Behavioral Health Services Tax > $1,000,000
  function computeCaIncrementalTax(gain, baseIncome, filingStatus) {
    if (gain <= 0) return 0;
    const singleBrackets = [
      [10756, 0.01], [25499, 0.02], [40245, 0.04], [55866, 0.06],
      [70606, 0.08], [360659, 0.093], [432787, 0.103], [721314, 0.113], [Infinity, 0.123]
    ];
    const mfjBrackets = [
      [21512, 0.01], [50998, 0.02], [80490, 0.04], [111732, 0.06],
      [141212, 0.08], [721318, 0.093], [865574, 0.103], [1442628, 0.113], [Infinity, 0.123]
    ];
    const brackets = filingStatus === 'mfj' ? mfjBrackets : singleBrackets;
    function taxOn(inc) {
      if (inc <= 0) return 0;
      let t = 0;
      let prev = 0;
      for (const [up, rate] of brackets) {
        if (inc <= prev) break;
        t += (Math.min(inc, up) - prev) * rate;
        prev = up;
      }
      if (inc > 1000000) t += (inc - 1000000) * 0.01;
      return t;
    }
    const base = Math.max(0, baseIncome ?? 0);
    return taxOn(base + gain) - taxOn(base);
  }

  function errorsFrom(data) {
    const errors = [];
    const required = ['years', 'homeValue', 'netProceeds', 'liquidAssets', 'homeLow', 'homeHigh', 'stockLow', 'stockHigh', 'inflation', 'imputedRent', 'grossRent', 'homeTax', 'homeInsurance', 'homeUtilities', 'homeMaintenance', 'homeCapital', 'rentalOther', 'sfValue', 'sfLow', 'sfHigh', 'sfGrossRent', 'sfTax', 'sfInsurance', 'sfUtilities', 'sfMaintenance', 'sfCapital', 'sfOther', 'sfUseChange', 'keepShare', 'treasuryYield'];
    for (const id of required) {
      if (data[id] === null || !validNumber(data[id])) errors.push(`Enter a valid ${id === 'years' ? 'comparison horizon' : id === 'homeValue' ? 'date-of-death property value' : id === 'netProceeds' ? 'same-year net sale proceeds' : id.replace(/([A-Z])/g, ' $1').toLowerCase()}.`);
    }
    if (data.years !== null && (!Number.isInteger(data.years) || data.years < 1 || data.years > 50)) errors.push('Comparison horizon must be a whole number from 1 to 50 years.');
    for (const id of ['homeValue', 'netProceeds', 'liquidAssets', 'sfValue']) if (data[id] !== null && data[id] < 0) errors.push('Property value, net proceeds, and liquid assets cannot be negative.');
    if (data.homeLow !== null && data.homeHigh !== null && data.homeLow > data.homeHigh) errors.push('Home growth low must be no higher than home growth high.');
    if (data.stockLow !== null && data.stockHigh !== null && data.stockLow > data.stockHigh) errors.push('Investment return low must be no higher than investment return high.');
    if (data.sfLow !== null && data.sfHigh !== null && data.sfLow > data.sfHigh) errors.push('Existing SF property growth low must be no higher than high.');
    if (data.phaseMonths !== null && (!Number.isInteger(data.phaseMonths) || data.phaseMonths < 24 || data.phaseMonths > 36)) errors.push('Phase-in period must be between 24 and 36 whole months; immediate investment is a separate path.');
    if (data.keepShare !== null && (data.keepShare < 0 || data.keepShare > 100)) errors.push('Retained share must be between 0% and 100%.');
    if (data.drawdown !== null && (data.drawdown < 0 || data.drawdown > 100)) errors.push('Drawdown must be between 0% and 100%.');
    if (data.crashYear !== null && (!Number.isInteger(data.crashYear) || data.crashYear < 1 || data.crashYear > data.years)) errors.push('Crash year must be within the selected horizon.');
    if ((data.crashYear === null) !== (data.drawdown === null)) errors.push('Enter both a crash year and drawdown stress, or leave both blank.');
    if (data.saleYear !== null && (!Number.isInteger(data.saleYear) || data.saleYear < 0 || data.saleYear >= data.years)) errors.push('Delayed sale year must be 0 or a whole year before the comparison date.');
    if (data.delayedProceeds !== null && (data.saleYear === null || data.saleYear === 0)) errors.push('Enter a delayed sale year before adding future after-tax sale proceeds.');
    if (data.delayedProceeds !== null && data.delayedProceeds < 0) errors.push('Delayed sale proceeds cannot be negative.');
    if (data.caTaxableIncome !== null && data.caTaxableIncome < 0) errors.push('California taxable income sensitivity cannot be negative.');
    if (data.prop19Mode !== 'none' && (data.traRate === null || data.traRate <= 0)) errors.push('Enter a published ad valorem TRA rate (e.g. 1.1636%) when enabling Prop 19 / parcel assessment modeling.');
    if ((data.prop19Mode === 'prop19' || data.prop19Mode === 'moveout') && data.fbyv === null) errors.push('Enter the prior factored base-year value (FBYV) to calculate the Prop 19 exclusion cap.');
    for (const id of ['homeLow','homeHigh','stockLow','stockHigh','sfLow','sfHigh','treasuryYield']) if (data[id] !== null && data[id] <= -100) errors.push('Growth, investment and Treasury rates must be greater than -100%.');
    if (data.inflation !== null && data.inflation <= -100) errors.push('Inflation must be greater than -100%.');
    for (const id of ['imputedRent','grossRent','homeTax','homeInsurance','homeMaintenance','homeCapital','rentalOther','sfGrossRent','sfTax','sfInsurance','sfMaintenance','sfCapital','sfOther']) if (data[id] !== null && data[id] < 0) errors.push('Rent, tax, insurance, maintenance, capital reserve and rental cost inputs cannot be negative.');
    return errors;
  }

  function compound(principal, annualPct, years, crashYear, drawdownPct) {
    let value = principal;
    const rate = 1 + annualPct / 100;
    for (let y = 1; y <= years; y += 1) {
      value *= rate;
      if (crashYear === y && drawdownPct !== null) value *= (1 - drawdownPct / 100);
    }
    return value;
  }

  function futureValueOfFlow(flowFnOrConst, annualPct, years, inflationPct) {
    let total = 0;
    for (let y = 1; y <= years; y += 1) {
      const flow = typeof flowFnOrConst === 'function' ? flowFnOrConst(y) : flowFnOrConst * Math.pow(1 + inflationPct / 100, y - 1);
      total = total * (1 + annualPct / 100) + flow;
    }
    return total;
  }

  function phasedValue(principal, stockPct, treasuryPct, years, months, crashYear, drawdownPct) {
    if (months <= 0) return compound(principal, stockPct, years, crashYear, drawdownPct);
    const totalMonths = years * 12;
    const phaseMonths = months;
    const stockMonthly = Math.pow(1 + stockPct / 100, 1 / 12);
    const treasuryMonthly = Math.pow(1 + treasuryPct / 100, 1 / 12);
    const tranche = principal / phaseMonths;
    let equity = 0;
    let treasury = principal;
    for (let m = 1; m <= totalMonths; m += 1) {
      treasury *= treasuryMonthly;
      equity *= stockMonthly;
      if (m <= phaseMonths) treasury -= Math.min(tranche, treasury);
      if (m === phaseMonths) {
        equity += treasury;
        treasury = 0;
      }
      if (crashYear !== null && drawdownPct !== null && m === crashYear * 12) equity *= (1 - drawdownPct / 100);
    }
    return equity + treasury;
  }

  // Statutory Prop 13 / Prop 19 annual property tax calculation (BOE LTA 2025/009 & Pub 801)
  function parcelAssessmentAtYear(data, year, forOccupancy, movedOutAfterYear) {
    if (data.prop19Mode === 'none' || data.traRate === null) return null;
    const prop13Factor = Math.pow(1 + Math.min(0.02, Math.max(0, data.inflation / 100)), year);
    const prop19CapRef = 1044586; // BOE Feb 16, 2025 – Feb 15, 2027 published cap
    let baseAssessed;
    if (!forOccupancy || data.prop19Mode === 'full') {
      baseAssessed = data.homeValue;
    } else if (movedOutAfterYear !== null && year > movedOutAfterYear) {
      // BOE Pub 801: vacating later terminates Prop 19 exclusion on next lien date -> factored transfer FMV
      baseAssessed = data.homeValue;
    } else {
      const fbyv = data.fbyv ?? data.homeValue;
      const excess = Math.max(0, data.homeValue - (fbyv + prop19CapRef));
      baseAssessed = fbyv + excess;
    }
    const assessed = baseAssessed * prop13Factor;
    const parcelCharges = (data.parcelFixed ?? 0) * Math.pow(1 + data.inflation / 100, year);
    const annualTax = assessed * (data.traRate / 100) + parcelCharges;
    return { assessed, annualTax };
  }

  // Statutory delayed-sale tax calculation (§ 121, 27.5-yr MACRS & § 1250 recapture, § 1031, Form 540 1% >$1M)
  function computeDelayedExitNet(data, saleYear, homeGrowthPct) {
    if (data.exitStrategy === 'manual') return data.delayedProceeds;
    const fmvSale = data.homeValue * Math.pow(1 + homeGrowthPct / 100, saleYear);
    const sccTransferTax = (fmvSale / 1000) * 1.10; // SCC published $1.10/$1,000
    const sellingCosts = fmvSale * 0.05 + sccTransferTax + 1500;
    const debt = data.debtBalance ?? 0;

    if (data.exitStrategy === 'sec1031') {
      // IRC § 1031 defers Fed/CA capital gains & § 1250 recapture (~1.5% QI/closing friction)
      return Math.max(0, fmvSale * 0.985 - debt);
    }

    const structShare = clamp((data.structurePct ?? 28) / 100, 0, 0.9);
    const isRental = data.exitStrategy === 'taxableRent';
    const cumDepr = isRental ? (data.homeValue * structShare / 27.5) * Math.min(27.5, saleYear) : 0;
    const adjBasis = data.homeValue - cumDepr;
    const realizedGain = (fmvSale - sellingCosts) - adjBasis;

    if (realizedGain <= 0) return Math.max(0, fmvSale - sellingCosts - debt);

    const sec121Cap = (data.exitStrategy === 'sec121' && saleYear >= 2) ? (data.filingStatus === 'mfj' ? 500000 : 250000) : 0;
    const recapture1250 = isRental ? Math.min(realizedGain, cumDepr) : 0; // § 1250 not eligible for § 121
    const appreciationGain = Math.max(0, realizedGain - recapture1250);
    const taxableAppreciation = Math.max(0, appreciationGain - sec121Cap);

    const fedTax = recapture1250 * (0.25 + 0.038) + taxableAppreciation * (0.20 + 0.038);
    const caTax = computeCaIncrementalTax(recapture1250 + taxableAppreciation, data.caTaxableIncome ?? 180000, data.filingStatus);
    return Math.max(0, fmvSale - sellingCosts - debt - fedTax - caTax);
  }

  function replayHistoricalRegime(principal, regimeKey, userTsYieldPct) {
    const reg = PUBLIC_HIST_SEQUENCES[regimeKey];
    if (!reg || principal <= 0) return null;
    function runMode(phaseMonths) {
      let eq = phaseMonths === 0 ? principal : 0;
      let ts = phaseMonths === 0 ? 0 : principal;
      const tranche = phaseMonths > 0 ? principal / phaseMonths : 0;
      let peak = principal;
      let maxDd = 0;
      for (let y = 0; y < reg.eq.length; y += 1) {
        const eqMonthly = Math.pow(1 + reg.eq[y], 1 / 12);
        const tsRate = y < 2 && userTsYieldPct !== null ? userTsYieldPct / 100 : reg.ts[y];
        const tsMonthly = Math.pow(1 + tsRate, 1 / 12);
        for (let m = 1; m <= 12; m += 1) {
          const gm = y * 12 + m;
          ts *= tsMonthly;
          eq *= eqMonthly;
          if (phaseMonths > 0 && gm <= phaseMonths) {
            const move = Math.min(tranche, ts);
            ts -= move;
            eq += move;
          }
          if (phaseMonths > 0 && gm === phaseMonths && ts > 0) {
            eq += ts;
            ts = 0;
          }
          const tot = eq + ts;
          if (tot > peak) peak = tot;
          const dd = peak > 0 ? (tot - peak) / peak : 0;
          if (dd < maxDd) maxDd = dd;
        }
      }
      return { end: eq + ts, maxDdPct: (maxDd * 100).toFixed(1) + '%' };
    }
    return {
      label: reg.label,
      lump: runMode(0),
      m24: runMode(24),
      m36: runMode(36)
    };
  }

  function readData() {
    const keys = ['years','homeValue','netProceeds','liquidAssets','homeLow','homeHigh','stockLow','stockHigh','inflation','imputedRent','grossRent','homeTax','homeInsurance','homeUtilities','homeMaintenance','homeCapital','rentalOther','sfValue','sfLow','sfHigh','sfGrossRent','sfTax','sfInsurance','sfUtilities','sfMaintenance','sfCapital','sfOther','sfUseChange','keepShare','phaseMonths','treasuryYield','caTaxableIncome','crashYear','drawdown','saleYear','delayedProceeds','fbyv','traRate','parcelFixed','debtBalance','structurePct','priorGifts'];
    const data = Object.fromEntries(keys.map((key) => [key, number(key)]));
    data.phaseMonths ??= 24;
    data.crashYear ??= null;
    data.drawdown ??= null;
    data.saleYear ??= null;
    data.delayedProceeds ??= null;
    data.mixedUse = $('mixedUse').value;
    data.treasuryTenor = $('treasuryTenor').value;
    data.prop19Mode = $('prop19Mode') ? $('prop19Mode').value : 'none';
    data.exitStrategy = $('exitStrategy') ? $('exitStrategy').value : 'manual';
    data.filingStatus = $('filingStatus') ? $('filingStatus').value : 'single';
    data.portability = $('portability') ? $('portability').value : 'no';
    data.historicalRegime = $('historicalRegime') ? $('historicalRegime').value : 'none';
    data.decisionNote = $('decisionNote') ? $('decisionNote').value.trim() : '';
    data.decisionDate = $('decisionDate') ? $('decisionDate').value : '';
    const nonTaxInherited = data.homeInsurance + data.homeUtilities + data.homeMaintenance + data.homeCapital;
    data.nonTaxInherited = nonTaxInherited;
    const inheritedCosts = data.homeTax + nonTaxInherited;
    data.liveBenefit = data.imputedRent - inheritedCosts + data.sfUseChange;
    data.rentalCash = data.grossRent - inheritedCosts - data.rentalOther;
    const sfCosts = data.sfTax + data.sfInsurance + data.sfUtilities + data.sfMaintenance + data.sfCapital + data.sfOther;
    data.sfNet = data.sfGrossRent - sfCosts;
    return data;
  }

  function calc(data) {
    const n = data.years;
    const shockYear = data.crashYear;
    const shock = data.drawdown;
    const debt = data.debtBalance ?? 0;
    const rows = [];

    const liveFlowFn = (y) => {
      const infl = Math.pow(1 + data.inflation / 100, y - 1);
      const moveOutYr = data.prop19Mode === 'moveout' && data.saleYear ? data.saleYear : null;
      const pTax = parcelAssessmentAtYear(data, y - 1, true, moveOutYr);
      const taxYr = pTax ? pTax.annualTax : data.homeTax * infl;
      return (data.imputedRent + data.sfUseChange - data.nonTaxInherited) * infl - taxYr;
    };

    const rentFlowFn = (y) => {
      const infl = Math.pow(1 + data.inflation / 100, y - 1);
      const pTax = parcelAssessmentAtYear(data, y - 1, false, null);
      const taxYr = pTax ? pTax.annualTax : data.homeTax * infl;
      return (data.grossRent - data.nonTaxInherited - data.rentalOther) * infl - taxYr;
    };

    const ranges = [
      {label:'Live in inherited home', flowFn:liveFlowFn, retain:1, sale:null, phased:false, href:'#src-boe-prop19', source: data.prop19Mode !== 'none' ? 'Prop 19 / TRA parcel formula applied; verify BOE-266 & BOE-19-P.' : 'Prop 19 eligibility must be verified; manual tax input used.'},
      {label:'Rent inherited home', flowFn:rentFlowFn, retain:1, sale:null, phased:false, href:'#src-irs-depreciation', source: data.prop19Mode !== 'none' ? 'Full FMV TRA reassessment applied; see IRS rental depreciation rules.' : 'IRS rental depreciation / disposition rules; manual tax input used.'},
      {label:'Sell same tax year · invest now', flowFn:() => 0, retain:0, sale:data.netProceeds, phased:false, href:'#src-irs-basis', source:'IRC § 1014 date-of-death basis & SCC transfer tax rules.'},
      {label:`Sell · phase over ${data.phaseMonths} months (reinvestment risk explicit)`, flowFn:() => 0, retain:0, sale:data.netProceeds, phased:true, href:'#src-scc-tra', source:'3M–2Y U.S. Treasury ladder; reinvestment & bull-market cash drag explicit.'},
    ];
    const keep = data.keepShare / 100;
    const mixFlowFn = (y) => data.mixedUse === 'live' ? liveFlowFn(y) : data.mixedUse === 'rent' ? rentFlowFn(y) : (liveFlowFn(y) + rentFlowFn(y)) / 2;
    ranges.push({label:`Mixed · keep ${data.keepShare}% / sell ${100-data.keepShare}%`, flowFn:(y) => mixFlowFn(y) * keep, retain:keep, sale:data.netProceeds * (1-keep), phased:false, href:'#src-boe-prop19', source:'Fractional split convention; verify trust divisibility & Prop 19 rules.'});

    for (const path of ranges) {
      const cases = [];
      for (const [tag, homeRate, stockRate] of [['low', data.homeLow, data.stockLow], ['high', data.homeHigh, data.stockHigh]]) {
        const keptHome = Math.max(0, data.homeValue * Math.pow(1 + homeRate / 100, n) - debt) * path.retain;
        const benefit = futureValueOfFlow(path.flowFn, stockRate, n, data.inflation);
        const baseLiquid = compound(data.liquidAssets, stockRate, n, shockYear, shock);
        const sfRate = tag === 'low' ? data.sfLow : data.sfHigh;
        const sfHomeTerminal = data.sfValue * Math.pow(1 + sfRate / 100, n);
        const sfCash = futureValueOfFlow(data.sfNet, stockRate, n, data.inflation);
        const invest = path.phased
          ? phasedValue(path.sale, stockRate, data.treasuryYield, n, data.phaseMonths, shockYear, shock)
          : compound(path.sale ?? 0, stockRate, n, shockYear, shock);
        const nominal = keptHome + benefit + baseLiquid + invest + sfHomeTerminal + sfCash;
        const real = nominal / Math.pow(1 + data.inflation / 100, n);
        cases.push({nominal, real});
      }
      rows.push({label:path.label, low:cases[0].nominal, high:cases[1].nominal, realLow:cases[0].real, realHigh:cases[1].real, href:path.href, source:path.source});
    }

    if (data.saleYear !== null && data.saleYear > 0) {
      const remaining = n - data.saleYear;
      const exitLabels = {
        manual: ['Hold / rent then sell', '#src-irs-home-sale', 'Adviser-entered delayed net proceeds.'],
        sec121: [`Occupy ${data.saleYear} yrs → sell with IRC § 121`, '#src-irs-home-sale', 'IRC § 121 exclusion applied if ≥2 yrs occupancy; verify Pub. 523.'],
        taxableRent: [`Rent ${data.saleYear} yrs → taxable sale (§ 1250 + CA 540)`, '#src-irs-depreciation', '27.5-yr MACRS + 28.8% § 1250 recapture + Fed/CA Form 540 tax modeled.'],
        sec1031: [`Rent ${data.saleYear} yrs → IRC § 1031 exchange`, '#src-irs-1031', 'Defers capital gain & § 1250 recapture; file CA FTB Form 3840 if out-of-state.']
      };
      const [baseLbl, exitHref, exitSrc] = exitLabels[data.exitStrategy] || exitLabels.manual;
      const holdFn = data.exitStrategy === 'sec121' ? liveFlowFn : rentFlowFn;

      for (const [tag, homeRate, stockRate] of [['low', data.homeLow, data.stockLow], ['high', data.homeHigh, data.stockHigh]]) {
        const exitNet = computeDelayedExitNet(data, data.saleYear, homeRate);
        const proceedsAtHorizon = exitNet === null ? null : compound(exitNet, stockRate, remaining, shockYear !== null && shockYear > data.saleYear ? shockYear - data.saleYear : null, shock);
        const holdingFlows = futureValueOfFlow(holdFn, stockRate, data.saleYear, data.inflation);
        const postHoldCompounded = compound(holdingFlows, stockRate, remaining, null, null);
        const otherLiquid = compound(data.liquidAssets, stockRate, n, shockYear, shock);
        const sfRate = tag === 'low' ? data.sfLow : data.sfHigh;
        const sfHomeTerminal = data.sfValue * Math.pow(1 + sfRate / 100, n);
        const sfCash = futureValueOfFlow(data.sfNet, stockRate, n, data.inflation);
        const terminal = exitNet === null ? null : proceedsAtHorizon + postHoldCompounded + otherLiquid + sfHomeTerminal + sfCash;
        if (tag === 'low') {
          rows.push({
            label: `${baseLbl} (yr ${data.saleYear})`,
            low: terminal,
            high: null,
            realLow: terminal === null ? null : terminal / Math.pow(1 + data.inflation / 100, n),
            realHigh: null,
            href: exitHref,
            source: exitNet === null ? 'Unpriced: enter delayed proceeds or pick a statutory exit branch.' : exitSrc
          });
        } else if (exitNet !== null) {
          const r = rows[rows.length - 1];
          r.high = terminal;
          r.realHigh = terminal / Math.pow(1 + data.inflation / 100, n);
        }
      }
    }
    return rows;
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = readData();
    const errors = errorsFrom(data);
    if (errors.length) {
      status.textContent = errors.join(' ');
      status.style.color = '#9a3e36';
      results.hidden = true;
      return;
    }
    const rows = calc(data);
    resultRows.replaceChildren();
    const annualRows = $('annualProjectionRows');
    annualRows.replaceChildren();
    const sfOperatingCostBase = data.sfTax + data.sfInsurance + data.sfUtilities + data.sfMaintenance + data.sfCapital + data.sfOther;
    const moveOutYr = data.prop19Mode === 'moveout' && data.saleYear ? data.saleYear : null;

    for (let year = 0; year <= data.years; year += 1) {
      const row = document.createElement('tr');
      const lowValue = data.homeValue * Math.pow(1 + data.homeLow / 100, year);
      const highValue = data.homeValue * Math.pow(1 + data.homeHigh / 100, year);
      const sfLowValue = data.sfValue * Math.pow(1 + data.sfLow / 100, year);
      const sfHighValue = data.sfValue * Math.pow(1 + data.sfHigh / 100, year);
      const pAssess = parcelAssessmentAtYear(data, year, data.prop19Mode !== 'full', moveOutYr);
      const costValue = (data.nonTaxInherited * Math.pow(1 + data.inflation / 100, year)) + (pAssess ? pAssess.annualTax : data.homeTax * Math.pow(1 + data.inflation / 100, year));
      const sfCostValue = sfOperatingCostBase * Math.pow(1 + data.inflation / 100, year);
      const assessText = pAssess
        ? `Assessed ${displayMoney(pAssess.assessed)} · Tax ${displayMoney(pAssess.annualTax)}`
        : 'Manual tax input — enter FBYV & TRA % for Prop 19 roll';
      const items = [year === 0 ? 'Transfer date' : `Year ${year}`, `${displayMoney(lowValue)} / ${displayMoney(highValue)}`, `${displayMoney(sfLowValue)} / ${displayMoney(sfHighValue)}`, displayMoney(costValue), displayMoney(sfCostValue), assessText];
      for (const value of items) { const cell = document.createElement('td'); cell.textContent = value; row.append(cell); }
      const sourceCell = document.createElement('td');
      const assessorLink = document.createElement('a'); assessorLink.href = '#src-scc-tra'; assessorLink.textContent = 'SCC TRA Book';
      const sfLink = document.createElement('a'); sfLink.href = '#src-sf-prop-h-m'; sfLink.textContent = 'SF Treasurer';
      const propLink = document.createElement('a'); propLink.href = '#src-boe-prop19'; propLink.textContent = 'BOE Prop 19';
      sourceCell.append(assessorLink, document.createTextNode(' · '), sfLink, document.createTextNode(' · '), propLink);
      row.append(sourceCell);
      annualRows.append(row);
    }

    const maxValue = Math.max(1, ...rows.flatMap(r => [r.low, r.high].filter(v => Number.isFinite(v))));
    distribution.replaceChildren();
    for (const row of rows) {
      const tr = document.createElement('tr');
      const low = row.low === null ? 'Not priced' : displayMoney(row.low);
      const high = row.high === null ? (row.low === null ? 'Not priced' : 'Needs input') : displayMoney(row.high);
      const real = row.realLow === null ? 'Not priced' : row.realHigh === null ? displayMoney(row.realLow) + ' / needs input' : displayMoney(row.realLow) + ' / ' + displayMoney(row.realHigh);
      const source = document.createElement('a');
      source.href = row.href || '#src-irs-basis';
      source.textContent = row.source;
      const values = [row.label, low, high, real, ''];
      for (let i = 0; i < values.length; i += 1) {
        const td = document.createElement('td');
        if (i === 4) td.append(source);
        else td.textContent = values[i];
        tr.append(td);
      }
      resultRows.append(tr);
      const wrap = document.createElement('div'); wrap.className = 'bar-row';
      const label = document.createElement('span'); label.textContent = row.label;
      const track = document.createElement('div'); track.className = 'bar-track'; track.setAttribute('aria-hidden', 'true');
      const bar = document.createElement('div'); bar.className = 'bar-range';
      const left = clamp(Math.min(row.low ?? 0, row.high ?? row.low ?? 0) / maxValue * 100, 0, 100);
      const right = clamp(Math.max(row.low ?? 0, row.high ?? row.low ?? 0) / maxValue * 100, 0, 100);
      bar.style.left = `${left}%`; bar.style.width = `${Math.max(1, right - left)}%`; track.append(bar);
      const val = document.createElement('span'); val.className = 'bar-value'; val.textContent = high === 'Needs input' ? `${low} → ?` : `${low} → ${high}`;
      wrap.append(label, track, val); distribution.append(wrap);
    }

    // Historical Crash-Entry Replay Table
    const replayBox = $('regimeReplayBox');
    const replayRows = $('regimeReplayRows');
    if (replayBox && replayRows) {
      replayRows.replaceChildren();
      if (data.historicalRegime !== 'none' && data.netProceeds > 0) {
        const rep = replayHistoricalRegime(data.netProceeds, data.historicalRegime, data.treasuryYield);
        if (rep) {
          const entries = [
            ['Immediate 100% equity lump-sum', displayMoney(rep.lump.end), rep.lump.maxDdPct, 'Zero cash drag; full peak-entry crash exposure'],
            ['24-month 3M–2Y Treasury ladder → equities', displayMoney(rep.m24.end), rep.m24.maxDdPct, `Delta vs lump-sum: ${displayMoney(rep.m24.end - rep.lump.end)} (reinvestment rate-cut risk applies)`],
            ['36-month 3M–2Y Treasury ladder → equities', displayMoney(rep.m36.end), rep.m36.maxDdPct, `Delta vs lump-sum: ${displayMoney(rep.m36.end - rep.lump.end)} (longer staging cushions deep crash, trails bull recovery)`]
          ];
          for (const [strat, endVal, ddTxt, noteTxt] of entries) {
            const rtr = document.createElement('tr');
            for (const txt of [strat, endVal, ddTxt, noteTxt]) {
              const td = document.createElement('td'); td.textContent = txt; rtr.append(td);
            }
            const linkTd = document.createElement('td');
            const a = document.createElement('a'); a.href = 'black-swan.html'; a.textContent = rep.label;
            linkTd.append(a); rtr.append(linkTd);
            replayRows.append(rtr);
          }
          replayBox.hidden = false;
        } else {
          replayBox.hidden = true;
        }
      } else {
        replayBox.hidden = true;
      }
    }

    const realIntro = $('resultDisclaimer');
    realIntro.textContent = `Common ${data.years}-year horizon; selected low/high assumptions; ${data.phaseMonths}-month phase-in using the ${data.treasuryTenor} Treasury yield; optional ${data.drawdown === null ? 'no' : `${data.drawdown}%`} shock in year ${data.crashYear ?? '—'}. Displayed amounts are rounded to the nearest $10 and stay in this browser only. SF net annual cash flow is ${displayMoney(data.sfNet)} after entered costs; SF market-value range is included as a separate already-owned asset (not part of the transferor's estate).`;

    const taxNote = $('taxSensitivity');
    taxNote.replaceChildren();
    if (data.caTaxableIncome === null) {
      taxNote.textContent = '2025 California Form 540 sensitivity: optional taxable-income field left blank.';
    } else {
      const additionalTax = Math.max(0, data.caTaxableIncome - 1000000) * 0.01;
      const totalCa = computeCaIncrementalTax(data.caTaxableIncome, 0, data.filingStatus);
      taxNote.append(document.createTextNode(`2025 Form 540 reference: estimated progressive CA tax = ${displayMoney(totalCa)} (including ${displayMoney(additionalTax)} 1% Behavioral Health Services Tax above $1,000,000). `));
      const link = document.createElement('a'); link.href = '#src-ftb-540'; link.textContent = 'Review official FTB Form 540 instructions.'; taxNote.append(link);
    }

    const estateNote = $('estateSensitivity');
    if (estateNote) {
      estateNote.replaceChildren();
      const exclRef = data.portability === 'yes' ? 30000000 : 15000000;
      const grossEst = data.homeValue - (data.debtBalance ?? 0) + data.liquidAssets + (data.priorGifts ?? 0);
      const excess = Math.max(0, grossEst - exclRef);
      const estFedTax = excess * 0.40;
      estateNote.append(document.createTextNode(`2026 Federal Form 706 reference (${displayMoney(exclRef)} exclusion${data.portability === 'yes' ? ' w/ DSUE' : ''}; CA estate tax = $0 per R&TC § 13302): modeled transferor estate + prior gifts = ${displayMoney(grossEst)} (excludes already-owned SF property) → illustrative 40% federal estate tax = ${displayMoney(estFedTax)}. Ensure 9-month cash liquidity if near threshold. `));
      const eLink = document.createElement('a'); eLink.href = '#src-irs-form706'; eLink.textContent = 'IRS Form 706 instructions.'; estateNote.append(eLink);
    }

    results.hidden = false;
    status.textContent = 'Scenario comparison generated in this browser only. Nothing has been saved or transmitted.';
    status.style.color = '#24736b';
    results.scrollIntoView({behavior:'smooth', block:'start'});
  });

  // Browser-only local JSON export & FileReader import (never transmitted over network)
  const exportBtn = $('exportJsonBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      const payload = {};
      for (const el of form.querySelectorAll('input, select')) {
        if (el.id && el.type !== 'file') payload[el.id] = el.value;
      }
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `estate-pathways-local-${payload.decisionDate || 'scenario'}.json`;
      a.click();
      URL.revokeObjectURL(url);
      status.textContent = 'Exported local scenario JSON to your device only.';
    });
  }

  const importInput = $('importJsonFile');
  if (importInput) {
    importInput.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const parsed = JSON.parse(String(reader.result));
          for (const [k, v] of Object.entries(parsed)) {
            const el = $(k);
            if (el && el.type !== 'file' && v !== undefined && v !== null) el.value = String(v);
          }
          status.textContent = 'Loaded local JSON into browser memory only. Click "Compare these assumptions" to run.';
          status.style.color = '#24736b';
        } catch (_) {
          status.textContent = 'Could not parse JSON file.';
          status.style.color = '#9a3e36';
        }
      };
      reader.readAsText(file);
    });
  }

  form.addEventListener('reset', () => {
    results.hidden = true;
    status.textContent = 'All fields cleared. No inputs have been saved or calculated.';
    status.style.color = '';
  });
})();
