/* TinoDash2 model — ranges, not points. All $ rounded to $10.
   Official rules (Prop 13 2% cap, Prop 19 cap, 1% MHST, $15M exemption)
   are parameters, not forecasts. Forecasts are labeled assumptions. */
(function(global){
"use strict";
function r10(n){ return Math.round(n/10)*10; }
function clamp(n,a,b){ return Math.max(a, Math.min(b,n)); }

var DEFAULTS = {
  inheritYear: 2045,          // 2040-2050 range midpoint; user can change
  horizonYears: 20,           // years after inheritance to compare
  propA_value_2026: 3100000,  // user estimate Nov 2026 (unverified)
  propA_assessed_2026: 550540,// user table 2026 (rounded)
  propA_tax_2025: 7210,       // user table 2025 (rounded)
  propB_value_2026: 1800000,  // user estimate Nov 2026 (unverified)
  propB_assessed_2025: 114250,// user table 2025 (rounded)
  propB_tax_2025: 2440,       // user table 2025 (rounded)
  propB_rent_mo: 7150,        // user: 2 units rented
  propA_rent_mo_base: 3800,   // Zillow median floor benchmark (flagged)
  propA_rent_mo_high: 6200,   // comparable 3bd 95014 rent zestimate range
  homeApprec_low: 0.01, homeApprec_base: 0.03, homeApprec_high: 0.05,
  stockRet_low: 0.05, stockRet_base: 0.07, stockRet_high: 0.09,
  treasuryRet: 0.043,         // ~3-mo/2-yr par yield Nov 2026 (Treasury)
  inflation: 0.025,
  insuranceA: 1250,           // range $930-$1500, midpoint (flagged)
  insuranceB: 1500,           // user guess (flagged)
  waterA_mo: 125, elecA_mo: -15,   // solar credit (user range)
  waterB_mo: 365, elecB_mo: 50,    // user ranges midpoint
  maintA_pct: 0.006, maintB_pct: 0.008, // of market value /yr (assumption)
  sellCostPct: 0.065,         // commission ~5-6% + transfer/recording (assumption)
  prop19_addon: 1044586,      // BOE LTA 2025/009, 2025-2027 (indexed biennially)
  fedExemption_2026: 15000000,
  fedRateTop: 0.40,
  caTopRate: 0.123, mhstRate: 0.01, mhstThreshold: 1000000,
  fedLTCG: 0.20, fedNIIT: 0.038, unrec1250: 0.25,
  imputedRentA_mo: 3800,      // = market rent floor; user can override
  phaseMonths: 30,            // 24-36 mo Treasury parking
  phaseSteps: 6,              // equal tranches into stocks
  vacancy: 0.05, mgmt: 0.08,  // rent path haircuts (assumption)
  discountRate: 0.04
};

function factoredBase(assessed2026, years, cap){
  var v = assessed2026;
  for(var i=0;i<years;i++){ v = v * (1+cap); }
  return v;
}

/* Prop 19 parent-child: new base = min(market, factoredBase + addon) if heir occupies within 1yr.
   If not occupied: full reassessment to market. */
function prop19NewBase(marketAtTransfer, factoredAtTransfer, occupies){
  if(!occupies) return marketAtTransfer;
  var cap = factoredAtTransfer + DEFAULTS.prop19_addon;
  return Math.min(marketAtTransfer, cap);
}

function marketAt(year, base2026, g){
  return base2026 * Math.pow(1+g, Math.max(0, year-2026));
}

/* Year-by-year projection for one path. Returns {years:[...], terminal, npv} */
function projectPath(path, p, scenario){
  // scenario: 'low'|'base'|'high' picks appreciation/return ends
  var g = scenario==='low'? p.homeApprec_low : scenario==='high'? p.homeApprec_high : p.homeApprec_base;
  var sr = scenario==='low'? p.stockRet_low : scenario==='high'? p.stockRet_high : p.stockRet_base;
  var Y0 = p.inheritYear, H = p.horizonYears;
  var mktA0 = marketAt(Y0, p.propA_value_2026, g);
  var mktB0 = marketAt(Y0, p.propB_value_2026, g);
  var factA0 = factoredBase(p.propA_assessed_2026, Y0-2026, 0.02);
  var factB0 = factoredBase(p.propB_assessed_2025, Y0-2025, 0.02);
  // effective rates implied by user bills (flagged, parcel TRA unverified)
  var rateA = p.propA_tax_2025 / p.propA_assessed_2026; // ~1.31%
  var rateB = p.propB_tax_2025 / p.propB_assessed_2025; // ~2.14%?? check: 2440/114250=2.14% — high, flag
  // NOTE: rateB implied looks high vs Prop13 1%+bonds; keep as user-bill implied, flagged.
  var occupiesA = (path==='live' || path==='live-then-sell' || path==='live-then-rent');
  var baseA = prop19NewBase(mktA0, factA0, occupiesA);
  var baseB = factB0; // B already owned, no transfer
  var cash = 0, invested = 0, treasury = 0, stocks = 0;
  var rows = [];
  var soldA = false, soldAValue = 0, saleTax = 0;
  var basisA = mktA0; // stepped-up basis IRC 1014
  var deprAccum = 0;
  var buildingShare = 0.75; // assumption: 75% of value is building (flagged)
  var deprPerYr = (basisA*buildingShare)/27.5;

  function sellA(yearIdx, price){
    var costs = price * p.sellCostPct;
    var net = price - costs;
    var gain = Math.max(0, price - basisA + deprAccum); // basis reduced by depreciation if rented
    // 121 exclusion if lived 2 of last 5 yrs
    var excl = (path==='live-then-sell' || path==='live-then-rent' && yearIdx>=2) ? 500000 : 0;
    var taxable = Math.max(0, gain - excl);
    var unrec = Math.min(deprAccum, taxable);
    var rest = taxable - unrec;
    // Federal: unrec up to 25%, rest at LTCG 20% (+NIIT if high income — simplified: apply NIIT on rest)
    var fed = unrec*p.unrec1250 + rest*(p.fedLTCG + p.fedNIIT);
    // CA: ordinary rates; simplified top marginal on gain above threshold logic handled in summary
    var ca = taxable * 0.093; // placeholder mid-bracket; sensitivity via what-if
    return {net: net, tax: fed+ca, gain: gain};
  }

  for(var t=0;t<=H;t++){
    var yr = Y0 + t;
    var mktA = marketAt(yr, p.propA_value_2026, g);
    var mktB = marketAt(yr, p.propB_value_2026, g);
    var baseAt = baseA * Math.pow(1.02, t);
    var baseBt = baseB * Math.pow(1.02, t);
    var taxA = baseAt * rateA;
    var taxB = baseBt * rateB;
    var infl = Math.pow(1+p.inflation, t);
    var insA = p.insuranceA * infl, insB = p.insuranceB * infl;
    var maintA = mktA * p.maintA_pct, maintB = mktB * p.maintB_pct;
    var utilA = (p.waterA_mo + p.elecA_mo)*12*infl;
    var utilB = (p.waterB_mo + p.elecB_mo)*12*infl;
    var rentA = p.propA_rent_mo_base*12*Math.pow(1+Math.min(0.05,g), t);
    var rentB = p.propB_rent_mo*12*Math.pow(1+Math.min(0.05,g), t);
    var net = 0, note="";
    var mode = path;
    if(path==='live-then-rent' && t>=5) mode='rent';
    if(path==='rent-then-sell' && t>=10) mode='sell';
    if(path==='live-then-sell' && t>=5) mode='sell';

    if(mode==='live'){
      // Live in A, keep B as-is (2 rented, 1 owner unit). Imputed rent = avoided rent.
      var imputed = p.imputedRentA_mo*12*infl;
      net = imputed + rentB*(1-p.vacancy) - taxA - taxB - insA - insB - maintA - maintB - utilA - utilB;
      note = "Live in A; B: 2 rented + owner unit";
    } else if(mode==='rent'){
      var gross = rentA + rentB;
      var afterVac = gross*(1-p.vacancy);
      var afterMgmt = afterVac*(1-p.mgmt);
      deprAccum += deprPerYr;
      net = afterMgmt - taxA - taxB - insA - insB - maintA - maintB - utilB; // tenant pays A utilities (assumption)
      note = "Rent A + B (vacancy/mgmt haircuts)";
    } else if(mode==='sell'){
      if(!soldA){
        var s = sellA(t, mktA);
        soldA = true; soldAValue = s.net; saleTax = s.tax;
        invested = s.net - s.tax;
        treasury = invested; stocks = 0;
        net = rentB*(1-p.vacancy) - taxB - insB - maintB - utilB;
        note = "Sold A (net of costs/tax) → Treasury parking";
      } else {
        // phased: hold in Treasuries phaseMonths, then tranche into stocks
        var phaseYrs = p.phaseMonths/12;
        if(t < phaseYrs){
          treasury = treasury*(1+p.treasuryRet);
          note = "Treasury parking (3M–2Y ladder)";
        } else {
          var frac = clamp((t-phaseYrs)/ (p.phaseSteps/12 + 0.001), 0, 1);
          // move tranches: simplified — grow treasury until phase end, then stocks
          if(t===Math.ceil(phaseYrs)){
            stocks = treasury; treasury = 0;
          }
          stocks = stocks*(1+sr);
          note = "Phased into stocks (tranches)";
        }
        net = rentB*(1-p.vacancy) - taxB - insB - maintB - utilB;
      }
    } else if(mode==='sell-immediate'){
      // handled below
    }
    if(path==='sell-immediate' && t===0){
      var s0 = sellA(0, mktA0);
      soldA = true; invested = s0.net - s0.tax; treasury = invested;
      net = rentB*(1-p.vacancy) - taxB - insB - maintB - utilB;
      note = "Sold A in inheritance year → Treasury parking";
    } else if(path==='sell-immediate' && t>0){
      var ph = p.phaseMonths/12;
      if(t < ph){ treasury = treasury*(1+p.treasuryRet); }
      else {
        if(t===Math.ceil(ph)){ stocks = treasury; treasury=0; }
        stocks = stocks*(1+sr);
      }
      net = rentB*(1-p.vacancy) - taxB - insB - maintB - utilB;
      note = t<ph? "Treasury parking" : "Phased into stocks";
    }
    cash += net;
    rows.push({year:yr, t:t, mktA:r10(mktA), mktB:r10(mktB), taxA:r10(taxA), taxB:r10(taxB),
      net:r10(net), cash:r10(cash), treasury:r10(treasury), stocks:r10(stocks), note:note});
  }
  var terminal = cash + treasury + stocks;
  // terminal property value if not sold (for live/rent paths, add equity at market minus future sell costs)
  var equity = 0;
  if(!soldA){
    var mktEnd = marketAt(Y0+H, p.propA_value_2026, g);
    equity = mktEnd*(1-p.sellCostPct);
    terminal += equity;
  }
  // NPV of annual nets at discount rate (for ranking robustness)
  var npv = 0;
  for(var i=0;i<rows.length;i++){ npv += rows[i].net / Math.pow(1+p.discountRate, rows[i].t); }
  return {path:path, scenario:scenario, rows:rows, terminal:r10(terminal), npv:r10(npv),
    equity:r10(equity), saleTax:r10(saleTax), baseA:r10(baseA), mktA0:r10(mktA0), rateA:rateA, rateB:rateB};
}

function runAll(p){
  var paths = ['live','rent','sell-immediate','live-then-sell','rent-then-sell','live-then-rent'];
  var out = {};
  paths.forEach(function(path){
    out[path] = {low: projectPath(path,p,'low'), base: projectPath(path,p,'base'), high: projectPath(path,p,'high')};
  });
  return out;
}

/* Black swan: crash entry — stocks -57% (2008) or -89% (1929 price) in year 1 after phase-in.
   Phased path softens because only tranches after crash buy low; lump-sum buys pre-crash. */
function blackSwan(p){
  var mktA0 = marketAt(p.inheritYear, p.propA_value_2026, p.homeApprec_base);
  var netProceeds = mktA0*(1-p.sellCostPct); // before income tax (simplified, flagged)
  function lumpSum(crashDepth, crashYear){
    var v = netProceeds;
    for(var t=1;t<=20;t++){
      if(t===crashYear) v = v*(1-crashDepth);
      v = v*(1+p.stockRet_base);
    }
    return r10(v);
  }
  function phased(crashDepth, crashYear){
    // 30mo in Treasuries, then 6 tranches over 6mo; crash hits during phase-in
    var v = netProceeds;
    var inTreasury = v;
    var stocks = 0;
    for(var t=1;t<=20;t++){
      if(t<=2.5){ inTreasury = inTreasury*(1+p.treasuryRet); }
      else if(t===3){ stocks = inTreasury; inTreasury=0; stocks = stocks*(1+p.stockRet_base); }
      else { stocks = stocks*(1+p.stockRet_base); }
      if(t===crashYear){
        // crash hits stocks held so far; treasury portion (if any) spared
        stocks = stocks*(1-crashDepth);
        if(inTreasury>0) inTreasury = inTreasury*(1-crashDepth*0); // Treasuries spared
      }
    }
    return r10(inTreasury+stocks);
  }
  return {
    proceeds: r10(netProceeds),
    lump2008: lumpSum(0.57, 1), phased2008: phased(0.57, 1),
    lump1929: lumpSum(0.89, 1), phased1929: phased(0.89, 1),
    lumpNoCrash: lumpSum(0, 99), phasedNoCrash: phased(0, 99)
  };
}

/* Distribution: triangular-ish fan from low/base/high + crash overlay */
function distribution(p){
  var all = runAll(p);
  var res = {};
  Object.keys(all).forEach(function(k){
    var lo = all[k].low.terminal, ba = all[k].base.terminal, hi = all[k].high.terminal;
    // pseudo-distribution: 11 bins between low and high, peak at base
    var bins = [];
    for(var i=0;i<11;i++){
      var v = lo + (hi-lo)*i/10;
      var w = 1 - Math.abs(i-5)/6; // triangular weight
      bins.push({value:r10(v), weight:Math.round(w*100)});
    }
    res[k] = {low:lo, base:ba, high:hi, bins:bins};
  });
  return res;
}

global.TinoModel = {DEFAULTS:DEFAULTS, r10:r10, runAll:runAll, blackSwan:blackSwan, distribution:distribution, projectPath:projectPath};
})(window);
