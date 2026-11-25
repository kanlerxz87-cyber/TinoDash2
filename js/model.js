// TinoDash2 Financial & Tax Decision Model (Privacy-First, Rounded to $10)
window.TinoModel = (function () {
  function round10(val) {
    return Math.round(val / 10) * 10;
  }

  function fmt(val) {
    const r = round10(val);
    const sign = r < 0 ? "-" : "";
    return sign + "$" + Math.abs(r).toLocaleString("en-US");
  }

  // Verified 2026 baseline constants (rounded/anonymized)
  const CONSTANTS = {
    propAValue2026: 3100000,       // Property A (95014) est. Nov 2026
    propAAssessed2026: 550540,    // Rounded to $10
    propBValue2026: 1800000,      // Property B (94122) est. Nov 2026
    propBAssessed2025: 114250,    // Rounded to $10
    propBRentMonthly: 7150,       // 2 rented units
    prop19Cap2025_2027: 1044590,  // BOE $1,044,586 rounded to $10
    fedEstateExcl2026: 15000000,  // IRS P.L. 119-21 (WFTC)
    caTaxRateTop: 0.133,          // 12.3% + 1% MHST > $1M (FTB Form 540)
    fedCapGainsTop: 0.238,        // 20% LTCG + 3.8% NIIT
    sccTransferTaxRate: 0.0011,   // $1.10 per $1,000 (Santa Clara County)
    sellingCostPct: 0.055         // ~5.5% broker + escrow + title + transfer tax
  };

  function projectPropertyValue(startVal, years, growthRate) {
    return startVal * Math.pow(1 + growthRate, years);
  }

  function simulatePaths(params) {
    const {
      transferYear = 2045,
      horizonYears = 20,
      propGrowth = 0.04,
      stockReturn = 0.07,
      inflation = 0.028,
      propARentMo = 5200,
      imputedRentMo = 5200,
      prop19Eligible = true,
      traRate = 0.0118,
      treasuryYield = 0.042,
      phasingMonths = 30
    } = params;

    const yrsToTransfer = Math.max(1, transferYear - 2026);
    const valAtTransfer = projectPropertyValue(CONSTANTS.propAValue2026, yrsToTransfer, propGrowth);
    const fbyvAtTransfer = CONSTANTS.propAAssessed2026 * Math.pow(1.02, yrsToTransfer);
    const prop19CapAtTransfer = CONSTANTS.prop19Cap2025_2027 * Math.pow(1 + inflation, yrsToTransfer);

    // 1. Pure Path: Sell Immediately at Transfer (Stepped-up basis = valAtTransfer -> $0 cap gain)
    const sellCosts = valAtTransfer * (CONSTANTS.sellingCostPct + CONSTANTS.sccTransferTaxRate);
    const netProceeds = valAtTransfer - sellCosts;
    const sellStockFinal = netProceeds * Math.pow(1 + stockReturn, horizonYears);

    // 2. Mixed Path: Sell & Phased-Invest (3M-2Y Treasuries for phasingMonths, then equities)
    const phaseYrs = phasingMonths / 12;
    const remYrs = Math.max(0, horizonYears - phaseYrs);
    const phasedMid = netProceeds * Math.pow(1 + treasuryYield, phaseYrs);
    const phasedFinal = phasedMid * Math.pow(1 + stockReturn, remYrs);

    // 3. Pure Path: Rent Property A (No Prop 19 -> Full reassessment to valAtTransfer)
    let rentCashCum = 0;
    let rentTaxBasis = valAtTransfer * 0.75; // ~75% depreciable structure
    let annualDep = rentTaxBasis / 27.5;
    let totalDepTaken = 0;
    let propValRent = valAtTransfer;
    let assessedRent = valAtTransfer;

    for (let y = 1; y <= horizonYears; y++) {
      const grossRent = propARentMo * 12 * Math.pow(1 + inflation, y - 1);
      const propTax = assessedRent * traRate;
      const opEx = (1600 + 1500 + 3500) * Math.pow(1 + inflation, y - 1); // Ins + Water + Maint
      const netOp = grossRent - propTax - opEx;
      const taxableIncome = Math.max(0, netOp - annualDep);
      const incomeTax = taxableIncome * 0.35; // Combined Fed+CA marginal est.
      rentCashCum = rentCashCum * (1 + stockReturn) + (netOp - incomeTax);
      totalDepTaken += annualDep;
      propValRent *= (1 + propGrowth);
      assessedRent *= 1.02;
    }
    const rentFinalNet = propValRent + rentCashCum;

    // 4. Pure Path: Live in Property A (Prop 19 Eligible if occupied within 1 yr)
    let assessedLive = valAtTransfer;
    if (prop19Eligible) {
      const cap = fbyvAtTransfer + prop19CapAtTransfer;
      assessedLive = valAtTransfer <= cap ? fbyvAtTransfer : fbyvAtTransfer + (valAtTransfer - cap);
    }
    let liveCashCum = 0;
    let propValLive = valAtTransfer;
    for (let y = 1; y <= horizonYears; y++) {
      const imputed = imputedRentMo * 12 * Math.pow(1 + inflation, y - 1);
      const propTax = assessedLive * traRate;
      const opEx = (1600 + 1500 + 3000) * Math.pow(1 + inflation, y - 1);
      liveCashCum = liveCashCum * (1 + stockReturn) + (imputed - propTax - opEx);
      propValLive *= (1 + propGrowth);
      assessedLive *= 1.02;
    }
    const liveFinalNet = propValLive + liveCashCum;

    // 5. Mixed Path: Live 2+ Years, Then Sell (IRC § 121 Exclusion $250k/$500k)
    const live2Val = valAtTransfer * Math.pow(1 + propGrowth, 3);
    const live2Gain = Math.max(0, live2Val - valAtTransfer - 250000); // Single §121 exclusion
    const live2Tax = live2Gain * (CONSTANTS.fedCapGainsTop + CONSTANTS.caTaxRateTop);
    const live2Net = live2Val * (1 - CONSTANTS.sellingCostPct - CONSTANTS.sccTransferTaxRate) - live2Tax;
    const liveThenSellFinal = live2Net * Math.pow(1 + stockReturn, Math.max(0, horizonYears - 3));

    return {
      valAtTransfer: round10(valAtTransfer),
      netProceeds: round10(netProceeds),
      sellStockFinal: round10(sellStockFinal),
      phasedFinal: round10(phasedFinal),
      rentFinalNet: round10(rentFinalNet),
      liveFinalNet: round10(liveFinalNet),
      liveThenSellFinal: round10(liveThenSellFinal),
      assessedLiveStart: round10(assessedLive / Math.pow(1.02, horizonYears)),
      assessedRentStart: round10(valAtTransfer)
    };
  }

  return { CONSTANTS, round10, fmt, simulatePaths };
})();
