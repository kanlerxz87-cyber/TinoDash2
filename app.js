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
    const raw = $(id).value.trim();
    return raw === '' ? null : Number(raw);
  };
  const validNumber = (value) => Number.isFinite(value);
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

  $('printBrief').addEventListener('click', () => window.print());

  function errorsFrom(data) {
    const errors = [];
    const required = ['years', 'homeValue', 'netProceeds', 'liquidAssets', 'homeLow', 'homeHigh', 'stockLow', 'stockHigh', 'inflation', 'imputedRent', 'grossRent', 'homeTax', 'homeInsurance', 'homeUtilities', 'homeMaintenance', 'homeCapital', 'rentalOther', 'sfNet', 'sfUseChange', 'keepShare', 'treasuryYield'];
    for (const id of required) {
      if (data[id] === null || !validNumber(data[id])) errors.push(`Enter a valid ${id === 'years' ? 'comparison horizon' : id === 'homeValue' ? 'date-of-death property value' : id === 'netProceeds' ? 'same-year net sale proceeds' : id.replace(/([A-Z])/g, ' $1').toLowerCase()}.`);
    }
    if (data.years !== null && (!Number.isInteger(data.years) || data.years < 1 || data.years > 50)) errors.push('Comparison horizon must be a whole number from 1 to 50 years.');
    for (const id of ['homeValue', 'netProceeds', 'liquidAssets']) if (data[id] !== null && data[id] < 0) errors.push('Property value, net proceeds, and liquid assets cannot be negative.');
    if (data.homeLow !== null && data.homeHigh !== null && data.homeLow > data.homeHigh) errors.push('Home growth low must be no higher than home growth high.');
    if (data.stockLow !== null && data.stockHigh !== null && data.stockLow > data.stockHigh) errors.push('Investment return low must be no higher than investment return high.');
    if (data.phaseMonths !== null && (!Number.isInteger(data.phaseMonths) || data.phaseMonths < 24 || data.phaseMonths > 36)) errors.push('Phase-in period must be between 24 and 36 whole months; immediate investment is a separate path.');
    if (data.keepShare !== null && (data.keepShare < 0 || data.keepShare > 100)) errors.push('Retained share must be between 0% and 100%.');
    if (data.drawdown !== null && (data.drawdown < 0 || data.drawdown > 100)) errors.push('Drawdown must be between 0% and 100%.');
    if (data.crashYear !== null && (!Number.isInteger(data.crashYear) || data.crashYear < 1 || data.crashYear > data.years)) errors.push('Crash year must be within the selected horizon.');
    if ((data.crashYear === null) !== (data.drawdown === null)) errors.push('Enter both a crash year and drawdown stress, or leave both blank.');
    if (data.saleYear !== null && (!Number.isInteger(data.saleYear) || data.saleYear < 0 || data.saleYear >= data.years)) errors.push('Delayed sale year must be 0 or a whole year before the comparison date.');
    if (data.delayedProceeds !== null && (data.saleYear === null || data.saleYear === 0)) errors.push('Enter a delayed sale year before adding future after-tax sale proceeds.');
    if (data.delayedProceeds !== null && data.delayedProceeds < 0) errors.push('Delayed sale proceeds cannot be negative.');
    if (data.caTaxableIncome !== null && data.caTaxableIncome < 0) errors.push('California taxable income sensitivity cannot be negative.');
    for (const id of ['homeLow','homeHigh','stockLow','stockHigh','treasuryYield']) if (data[id] !== null && data[id] <= -100) errors.push('Growth, investment and Treasury rates must be greater than -100%.');
    if (data.inflation !== null && data.inflation <= -100) errors.push('Inflation must be greater than -100%.');
    for (const id of ['imputedRent','grossRent','homeTax','homeInsurance','homeMaintenance','homeCapital','rentalOther']) if (data[id] !== null && data[id] < 0) errors.push('Rent, tax, insurance, maintenance, capital reserve and rental cost inputs cannot be negative.');
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

  function futureValueOfFlow(flow, annualPct, years, inflationPct) {
    let total = 0;
    for (let y = 1; y <= years; y += 1) {
      const nominalFlow = flow * Math.pow(1 + inflationPct / 100, y - 1);
      total = total * (1 + annualPct / 100) + nominalFlow;
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

  function readData() {
    const keys = ['years','homeValue','netProceeds','liquidAssets','homeLow','homeHigh','stockLow','stockHigh','inflation','imputedRent','grossRent','homeTax','homeInsurance','homeUtilities','homeMaintenance','homeCapital','rentalOther','sfNet','sfUseChange','keepShare','phaseMonths','treasuryYield','caTaxableIncome','crashYear','drawdown','saleYear','delayedProceeds'];
    const data = Object.fromEntries(keys.map((key) => [key, number(key)]));
    data.phaseMonths ??= 24;
    data.crashYear ??= null;
    data.drawdown ??= null;
    data.saleYear ??= null;
    data.delayedProceeds ??= null;
    data.mixedUse = $('mixedUse').value;
    data.treasuryTenor = $('treasuryTenor').value;
    const inheritedCosts = data.homeTax + data.homeInsurance + data.homeUtilities + data.homeMaintenance + data.homeCapital;
    data.liveBenefit = data.imputedRent - inheritedCosts + data.sfUseChange;
    data.rentalCash = data.grossRent - inheritedCosts - data.rentalOther;
    return data;
  }

  function calc(data) {
    const n = data.years;
    const shockYear = data.crashYear;
    const shock = data.drawdown;
    const rows = [];
    const ranges = [
      {label:'Live in inherited home', homeFlow:data.liveBenefit, retain:1, sale:null, phased:false, source:'Prop 19 eligibility and primary-home conditions must be verified; imputed rent is user-entered.'},
      {label:'Rent inherited home', homeFlow:data.rentalCash, retain:1, sale:null, phased:false, source:'IRS rental depreciation / disposition rules; net rent is user-entered.'},
      {label:'Sell same tax year · invest now', homeFlow:0, retain:0, sale:data.netProceeds, phased:false, source:'IRS inherited basis and FTB current-year tax rules; proceeds must be after tax and costs.'},
      {label:`Sell · phase over ${data.phaseMonths} months`, homeFlow:0, retain:0, sale:data.netProceeds, phased:true, source:'U.S. Treasury rates are date-specific; reinvestment risk is not eliminated.'},
    ];
    const keep = data.keepShare / 100;
    const mixFlow = data.mixedUse === 'live' ? data.liveBenefit : data.mixedUse === 'rent' ? data.rentalCash : (data.liveBenefit + data.rentalCash) / 2;
    ranges.push({label:`Mixed · keep ${data.keepShare}% / sell ${100-data.keepShare}%`, homeFlow:mixFlow, retain:keep, sale:data.netProceeds * (1-keep), phased:false, source:'Fractional split is a modeling convention; title, taxes and legal divisibility need adviser review.'});

    for (const path of ranges) {
      const cases = [];
      for (const [tag, homeRate, stockRate] of [['low', data.homeLow, data.stockLow], ['high', data.homeHigh, data.stockHigh]]) {
        const keptHome = data.homeValue * path.retain * Math.pow(1 + homeRate / 100, n);
        const benefit = futureValueOfFlow(path.homeFlow * path.retain, stockRate, n, data.inflation);
        const baseLiquid = compound(data.liquidAssets, stockRate, n, shockYear, shock);
        let invest;
        if (path.phased) invest = phasedValue(path.sale, stockRate, data.treasuryYield, n, data.phaseMonths, shockYear, shock);
        else invest = compound(path.sale ?? 0, stockRate, n, shockYear, shock);
        const nominal = keptHome + benefit + baseLiquid + invest;
        const real = nominal / Math.pow(1 + data.inflation / 100, n);
        cases.push({nominal, real});
      }
      const first = cases[0], second = cases[1];
      rows.push({label:path.label, low:first.nominal, high:second.nominal, realLow:first.real, realHigh:second.real, source:path.source});
    }
    if (data.saleYear !== null && data.saleYear > 0) {
      const remaining = n - data.saleYear;
      for (const [tag, homeRate, stockRate] of [['low', data.homeLow, data.stockLow], ['high', data.homeHigh, data.stockHigh]]) {
        const adviserNet = data.delayedProceeds;
        const proceedsAtHorizon = adviserNet === null ? null : compound(adviserNet, stockRate, remaining, shockYear !== null && shockYear > data.saleYear ? shockYear - data.saleYear : null, shock);
        const holdingFlows = futureValueOfFlow(data.rentalCash, stockRate, data.saleYear, data.inflation);
        const otherLiquid = compound(data.liquidAssets, stockRate, n, shockYear, shock);
        const terminal = adviserNet === null ? null : proceedsAtHorizon + holdingFlows + otherLiquid;
        if (tag === 'low') rows.push({label:`Hold / rent then sell in year ${data.saleYear}`,low:terminal,high:null,realLow:terminal === null ? null : terminal/Math.pow(1+data.inflation/100,n),realHigh:null,source: adviserNet === null ? 'Unpriced: future after-tax proceeds not provided. See IRS basis / home-sale rules.' : 'Delayed net proceeds entered by user; verify home-sale exclusion, basis, depreciation and sale-year tax.' , pendingFuture:adviserNet===null});
        else if (adviserNet !== null) {
          const r=rows[rows.length-1];r.high=terminal;r.realHigh=terminal/Math.pow(1+data.inflation/100,n);
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
    const operatingCostBase = data.homeTax + data.homeInsurance + data.homeUtilities + data.homeMaintenance + data.homeCapital;
    for (let year = 0; year <= data.years; year += 1) {
      const row = document.createElement('tr');
      const lowValue = data.homeValue * Math.pow(1 + data.homeLow / 100, year);
      const highValue = data.homeValue * Math.pow(1 + data.homeHigh / 100, year);
      const costValue = operatingCostBase * Math.pow(1 + data.inflation / 100, year);
      const items = [year === 0 ? 'Transfer date' : `Year ${year}`, displayMoney(lowValue), displayMoney(highValue), displayMoney(costValue), 'Not modeled — parcel / Prop 19 required'];
      for (const value of items) { const cell=document.createElement('td');cell.textContent=value;row.append(cell); }
      const sourceCell=document.createElement('td');
      const assessorLink=document.createElement('a');assessorLink.href='https://www.sccassessor.org/';assessorLink.textContent='County assessor';
      const propLink=document.createElement('a');propLink.href='#src-boe-prop19';propLink.textContent='BOE Prop 19';
      sourceCell.append(assessorLink,document.createTextNode(' · '),propLink);row.append(sourceCell);
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
      source.href = row.label.startsWith('Live') ? '#src-boe-prop19' : row.label.startsWith('Rent') ? '#src-irs-depreciation' : row.label.startsWith('Hold') ? '#src-irs-home-sale' : row.label.startsWith('Mixed') && data.mixedUse === 'rent' ? '#src-irs-depreciation' : row.label.startsWith('Mixed') ? '#src-boe-prop19' : '#src-irs-basis';
      source.textContent = row.source;
      const values = [row.label, low, high, real, 'Taxes excluded; see official source / limits'];
      for (let i=0;i<values.length;i+=1) {
        const td=document.createElement('td');
        if (i===4) td.append(source);
        else td.textContent=values[i];
        tr.append(td);
      }
      resultRows.append(tr);
      const wrap=document.createElement('div');wrap.className='bar-row';
      const label=document.createElement('span');label.textContent=row.label;
      const track=document.createElement('div');track.className='bar-track';track.setAttribute('aria-hidden','true');
      const bar=document.createElement('div');bar.className='bar-range';
      const left=clamp(Math.min(row.low,row.high ?? row.low)/maxValue*100,0,100);
      const right=clamp(Math.max(row.low,row.high ?? row.low)/maxValue*100,0,100);
      bar.style.left=`${left}%`;bar.style.width=`${Math.max(1,right-left)}%`;track.append(bar);
      const val=document.createElement('span');val.className='bar-value';val.textContent=high==='Needs input'?`${low} → ?`:`${low} → ${high}`;
      wrap.append(label,track,val);distribution.append(wrap);
    }
    const realIntro = $('resultDisclaimer');
    realIntro.textContent = `Common ${data.years}-year horizon; selected low/high assumptions; ${data.phaseMonths}-month phase-in using the ${data.treasuryTenor} Treasury yield; optional ${data.drawdown === null ? 'no' : `${data.drawdown}%`} shock in year ${data.crashYear ?? '—'}. Displayed amounts are rounded to the nearest $10 and stay in this browser only. These are arithmetic scenarios, not probabilities. SF net annual cash flow is ${displayMoney(data.sfNet)} and is shown separately; the SF property's principal value is not included.`;
    const taxNote = $('taxSensitivity');
    taxNote.replaceChildren();
    if (data.caTaxableIncome === null) {
      taxNote.textContent = '2025 California 1% tax sensitivity: not calculated (no taxable-income input). This estimate is outside the path values.';
    } else {
      const additionalTax = Math.max(0, data.caTaxableIncome - 1000000) * 0.01;
      taxNote.append(document.createTextNode(`2025 Form 540 reference only: estimated 1% Behavioral Health Services Tax = ${displayMoney(additionalTax)} based on entered California taxable income of ${displayMoney(data.caTaxableIncome)}; not added to path values. `));
      const link = document.createElement('a'); link.href = '#src-ftb-540'; link.textContent = 'Review official FTB instructions.'; taxNote.append(link);
    }
    results.hidden=false;
    status.textContent='Scenario comparison generated in this browser only. Nothing has been saved or transmitted.';
    status.style.color='#24736b';
    results.scrollIntoView({behavior:'smooth',block:'start'});
  });

  form.addEventListener('reset', () => {
    results.hidden=true;
    status.textContent='All fields cleared. No inputs have been saved or calculated.';
    status.style.color='';
  });
})();
