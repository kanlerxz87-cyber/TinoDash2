import { SCENARIOS, equityMonthlyReturn, housingReturnAt, inflationAt, treasuryYieldAt } from './economy.js';

export const CURRENT = Object.freeze({year:2026, prop19Allowance:1044586, estateExclusion:15000000, bhThreshold:1000000, bhRate:.01});
export const RANGE_DEFS = {
  marketA: [2000000,4000000,'A · current synthetic value','$'],
  marketB: [1000000,2500000,'B · current synthetic value','$'],
  rentA: [5000,10000,'A · synthetic monthly market rent','$'],
  rentB: [5000,11000,'B · existing monthly leased income','$'],
  assessedA: [350000,750000,'A · current synthetic assessment','$'],
  assessedB: [100000,300000,'B · current synthetic assessment','$'],
  maintenanceA: [10000,30000,'A · annual recurring repairs','$'],
  maintenanceB: [18000,50000,'B · annual recurring repairs','$'],
  insuranceA: [2000,8000,'A · annual primary policy budget','$'],
  insuranceB: [3000,12000,'B · annual landlord policy budget','$'],
  utilitiesA: [1200,3600,'A · annual water / power budget','$'],
  utilitiesB: [3600,8400,'B · annual water / power budget','$'],
  debtA: [0,500000,'A · debt at transfer, NOT current payoff','$'],
  debtB: [0,300000,'B · debt at A transfer, NOT current payoff','$'],
  renewalA: [8000,20000,'A · annual capital replacements after year 5','$'],
  renewalB: [12000,30000,'B · annual capital replacements after year 5','$'],
  directA: [0,3000,'A · annual direct parcel charges','$'],
  directB: [500,3000,'B · annual direct parcel charges','$'],
  homeGrowth: [.01,.05,'Nominal pre-transfer home growth; post-transfer center','%'],
  stockGrowth: [.04,.09,'Nominal stock-return center before tax','%'],
  inflation: [.02,.04,'Inflation center; actual annual scenario varies','%'],
  rentGrowth: [.01,.035,'Lawful rent-growth proxy (NOT authority to raise rent)','%'],
  treasuryYield: [.01,.05,'Treasury starting yield; varies on rollover','%'],
  vacancy: [.03,.12,'Vacancy / noncollection','%'],
  saleCost: [.04,.08,'Negotiable selling-cost budget, excluding transfer/recording','%'],
  federalOrdinary: [.24,.37,'Federal ordinary marginal sensitivity','%'],
  federalGains: [.15,.2,'Federal gain marginal sensitivity','%'],
  californiaRate: [.093,.123,'California marginal sensitivity, before 1% surtax','%'],
  prop19Growth: [0,.04,'Future biennial allowance annualized proxy, not CPI law','%']
};
export function defaultInputs() {
  const i = Object.fromEntries(Object.entries(RANGE_DEFS).map(([k,v])=>[k,(v[0]+v[1])/2]));
  return {...i, transferYear:2045,horizon:30,scenario:'baseline',stockTarget:.7,parkMonths:24,phaseMonths:12,
    prop19Eligible:false,longTermOccupancy:false,section121:true,section121Limit:500000,
    imputedA:7500,imputedB:3500,extraBRent:0,allowExtraBRent:false,
    landShare:.65,management:.08,landlordUtilityShare:.5,landlordInsuranceFactor:1.2,
    adValoremA:.012,adValoremB:.012,assessedGrowth:.02,insuranceGrowth:.045,
    mortgageRate:.05,mortgageYears:30,workingReserve:200000,fundingRate:.06,
    otherTaxableIncome:250000,niitThreshold:250000,niitExposed:true,basisFraction:1,
    recordingReserve:200,escrowReserve:4000,capexScale:1,bRentalShare:.65,
    bDepreciableBasis:250000,bPriorDepreciation:100000,sameYearMove:0,
    includePropH:false,bBuildingArea:4000,bSeniorUnits:0,propHCpi:.03};
}
export function validateInputs(i) {
  for (const [key,value] of Object.entries(defaultInputs())) {
    if (typeof value==='number'&&(typeof i[key]!=='number'||!Number.isFinite(i[key]))) throw new Error(`${key} must be a finite number.`);
    if (typeof value==='boolean'&&typeof i[key]!=='boolean') throw new Error(`${key} must be boolean.`);
  }
  if (!SCENARIOS.some(s=>s.id===i.scenario)) throw new Error('Unknown economic scenario.');
  if (!Number.isInteger(i.transferYear)||i.transferYear<2026||i.transferYear>2100) throw new Error('Transfer year must be 2026–2100.');
  if (!Number.isInteger(i.horizon)||i.horizon<1||i.horizon>50) throw new Error('Horizon must be 1–50 whole years.');
  for (const k of ['stockTarget','landShare','bRentalShare','basisFraction','vacancy','saleCost','management','landlordUtilityShare']) if (i[k]<0||i[k]>1) throw new Error(`${k} must be between zero and one.`);
  for (const k of ['marketA','marketB','rentA','rentB','assessedA','assessedB','maintenanceA','maintenanceB','insuranceA','insuranceB','utilitiesA','utilitiesB','debtA','debtB','directA','directB','renewalA','renewalB','workingReserve','recordingReserve','escrowReserve','capexScale','otherTaxableIncome','bDepreciableBasis','bPriorDepreciation','extraBRent','imputedA','imputedB','bBuildingArea','bSeniorUnits']) if(i[k]<0) throw new Error(`${k} cannot be negative.`);
  for (const k of ['homeGrowth','stockGrowth','rentGrowth','inflation','prop19Growth','insuranceGrowth','fundingRate','sameYearMove']) if (i[k]<=-1) throw new Error(`${k} must exceed -100%.`);
  for (const k of ['treasuryYield','federalOrdinary','federalGains','californiaRate','adValoremA','adValoremB','propHCpi']) if(i[k]<0||i[k]>1) throw new Error(`${k} must be 0–1.`);
  if (i.mortgageRate<0||i.mortgageYears<1||!Number.isInteger(i.mortgageYears)||i.assessedGrowth<0||i.assessedGrowth>.02) throw new Error('Invalid debt/assessment scenario.');
  if (![24,36].includes(i.parkMonths)||![12,24].includes(i.phaseMonths)) throw new Error('Use a 24/36-month park and 12/24-month phase.');
  if (![250000,500000].includes(i.section121Limit)||![125000,200000,250000].includes(i.niitThreshold)) throw new Error('Select a published filing-status sensitivity.');
  return i;
}
export const money10 = n => Math.round(n/10)*10;
export function bhTax(taxableIncome) { return Math.max(0,taxableIncome-CURRENT.bhThreshold)*CURRENT.bhRate; }
export function bhIncrement(other, extra) { return bhTax(other+Math.max(0,extra))-bhTax(other); }
export function niitTax(netInvestmentIncome,otherIncome,threshold=250000) {
  const nii=Math.max(0,netInvestmentIncome);
  return .038*Math.min(nii,Math.max(0,otherIncome+nii-threshold));
}
export function prop19Allowance(year,annualizedProxy=0) {
  // July 1 transfer convention: 2025/26 published period; later cycles are hypothetical.
  const cycles=Math.max(0,Math.floor((year-2025)/2));
  return CURRENT.prop19Allowance*Math.pow(1+annualizedProxy,cycles*2);
}
export function prop19Assessment(market,factoredBase,allowance,eligible=false) {
  if(!eligible) return market;
  return Math.min(market,factoredBase+Math.max(0,market-factoredBase-allowance));
}
export function documentaryTax(consideration,liensRemaining=0) {
  return Math.ceil(Math.max(0,consideration-liensRemaining)/500)*.55;
}
function incomeContext(otherIncome) {
  return typeof otherIncome==='number'?{ca:otherIncome,magi:otherIncome,nii:0}:{...otherIncome};
}
function incrementalNIIT(amount,c,i) {
  if(!i.niitExposed) return 0;
  const due=(nii,magi)=>.038*Math.min(Math.max(0,nii),Math.max(0,magi-i.niitThreshold));
  return due(c.nii+amount,c.magi+amount)-due(c.nii,c.magi);
}
export function gainTaxes(gain,unrecaptured=0,exclusion=0,i=defaultInputs(),otherIncome=i.otherTaxableIncome) {
  const c=incomeContext(otherIncome);
  const d=Math.min(Math.max(0,unrecaptured),Math.max(0,gain));
  const excluded=Math.min(Math.max(0,exclusion),Math.max(0,gain-d));
  const ordinaryGain=Math.max(0,gain-d-excluded);
  const taxable=ordinaryGain+d;
  const federal=ordinaryGain*i.federalGains+d*Math.min(.25,i.federalOrdinary);
  const california=taxable*i.californiaRate;
  const surtax=bhIncrement(c.ca,taxable);
  const niit=incrementalNIIT(taxable,c,i);
  return {federal,california,surtax,niit,tax:federal+california+surtax+niit,excluded,taxable,unrecaptured:d};
}
/** Annual threshold ledger: Treasury interest is NII/MAGI but excluded from CA.
 * Other income is held constant and presumed non-investment income. Flat marginal
 * rates remain a sensitivity; this is not a bracketed household/trust return.
 */
export function annualTaxLedger(i=defaultInputs()) {
  let context=incomeContext(i.otherTaxableIncome);
  function quote(kind,amount) {
    const n=Math.max(0,amount),caAmount=kind==='treasury'?0:n;
    const federal=n*(['rental','treasury'].includes(kind)?i.federalOrdinary:i.federalGains);
    return federal+caAmount*i.californiaRate+bhIncrement(context.ca,caAmount)+incrementalNIIT(n,context,i);
  }
  function record(amount,stateTaxable=true) {
    const n=Math.max(0,amount);context.ca+=stateTaxable?n:0;context.nii+=n;context.magi+=n;
  }
  return {context:()=>({...context}),quote,record,charge(kind,amount){const tax=quote(kind,amount);record(amount,kind!=='treasury');return tax;}};
}
export function saleQuote({market,basis,debt=0,depreciation=0,eligible121=false},i=defaultInputs(),otherIncome=i.otherTaxableIncome) {
  const transferTax=documentaryTax(market); // no liens remain after modeled payoff
  const commission=market*i.saleCost;
  const recording=i.recordingReserve;
  const escrow=i.escrowReserve;
  const sellingCosts=transferTax+commission+recording+escrow;
  const amountRealized=market-sellingCosts;
  const gain=Math.max(0,amountRealized-basis);
  const taxes=gainTaxes(gain,depreciation,eligible121&&i.section121?i.section121Limit:0,i,otherIncome);
  // No tax refund/loss benefit is invented. Debt payoff reduces cash, NOT gain.
  return {...taxes,market,basis,debt,transferTax,commission,recording,escrow,sellingCosts,amountRealized,gain,net:amountRealized-debt-taxes.tax};
}
export function annualDebt(balance,rate,remainingYears=30) {
  if(balance<=0) return {balance:0,payment:0,interest:0,principal:0};
  const n=Math.max(1,Math.round(remainingYears*12)),r=rate/12;
  const p=r===0?balance/n:balance*r/(1-Math.pow(1+r,-n));
  let b=balance,interest=0,payment=0;
  for(let m=0;m<Math.min(12,n)&&b>1e-8;m++) {const int=b*r;const pay=Math.min(p,b+int);b=Math.max(0,b+int-pay);interest+=int;payment+=pay;}
  return {balance:b,payment,interest,principal:balance-b};
}
const floorDollars=n=>Math.floor((n+1e-9));
const floorMills=n=>Math.floor((n+1e-9)*1000)/1000;
/** Legal-text calculator, NOT a certification or parcel eligibility finding.
 * fiscalYear is the July 1 start year. cpiRates are prospective scenario inputs.
 */
export function propH({type='multi',area=0,landArea=0,seniorUnits=0,seniorOwner=false,exempt=false,sroArea=0,fiscalYear=2027,cpiRates=[]}={}) {
  if(exempt||fiscalYear<2027||fiscalYear>2041) return 0;
  let base={single:129,multi:249,nonres:799,unimproved:392};
  let rates={single1:.42,single2:1.99,multi:.195,non1:.76,non2:.84,non3:.99};
  let multiCap=50000,nonCap=400000;
  for(let y=2028;y<=fiscalYear;y++) {
    const f=1+Math.max(0,cpiRates[y-2028]??0);
    base=Object.fromEntries(Object.entries(base).map(([k,v])=>[k,floorDollars(v*f)]));
    rates=Object.fromEntries(Object.entries(rates).map(([k,v])=>[k,floorMills(v*f)]));
    multiCap=floorDollars(multiCap*f);nonCap=floorDollars(nonCap*f);
  }
  const a=Math.max(0,area-sroArea);
  if(type==='single') return seniorOwner?0:base.single+Math.max(0,Math.min(a,5000)-3000)*rates.single1+Math.max(0,a-5000)*rates.single2;
  if(type==='multi') return Math.max(0,Math.min(multiCap,base.multi+Math.max(0,a-5000)*rates.multi)-seniorUnits*base.multi);
  if(type==='nonres') return Math.min(nonCap,base.nonres+Math.max(0,Math.min(a,50000)-5000)*rates.non1+Math.max(0,Math.min(a,250000)-50000)*rates.non2+Math.max(0,a-250000)*rates.non3);
  if(type==='unimproved') return landArea<=2000?0:base.unimproved;
  throw new Error('Mixed-use classification requires professional review; not implemented.');
}
export function propHCalendar(year,i,liveInB=true) {
  if(!i.includePropH) return 0;
  const fy=y=>propH({type:'multi',area:i.bBuildingArea,seniorUnits:liveInB?i.bSeniorUnits:0,fiscalYear:y,cpiRates:Array(30).fill(i.propHCpi)});
  return (fy(year-1)+fy(year))/2;
}
// Explicit scenario schedules; not diagnoses or quotes. No reserve+spend double count.
export const CAPITAL_PLAN = {
 A:[{year:1,item:'Inspection-led safety / immediate repairs',low:10000,high:24000},{year:2,item:'Roof / weatherproofing allowance',low:25000,high:65000},{year:3,item:'Solar / electrical replacement allowance',low:10000,high:24000},{year:4,item:'Water / plumbing systems allowance',low:5000,high:16000},{year:5,item:'Envelope / interior lifecycle allowance',low:10000,high:36000}],
 B:[{year:1,item:'Safety / condition and permit review',low:15000,high:35000},{year:2,item:'Roof / envelope / drainage allowance',low:20000,high:70000},{year:3,item:'Plumbing / electrical lifecycle allowance',low:15000,high:60000},{year:4,item:'Seismic / structural contingency',low:40000,high:150000},{year:5,item:'Common-area / interior lifecycle allowance',low:15000,high:50000}]
};
function capitalAt(property,year,i,priceIndex) {
  const v=CAPITAL_PLAN[property].find(v=>v.year===year);
  return (v?(v.low+v.high)/2:year>5?i['renewal'+property]:0)*i.capexScale*priceIndex;
}
export function depreciationStep(vintage,year) {
  if(year<vintage.start) return 0;
  // January placed-in-service sensitivity: first year 11.5 months, then cap
  // lifetime deductions at depreciable basis. Actual month/vintage requires CPA.
  const fraction=year===vintage.start?11.5/12:1;
  const amount=Math.max(0,Math.min(vintage.basis-vintage.recovered,vintage.basis/27.5*fraction));
  vintage.recovered+=amount;return amount;
}
function portfolio() { return {stock:0,stockBasis:0,treasury:0,funding:0,taxes:0,planned:0,deployed:0,missedPhase:0}; }
function contribute(p,n,weight,i,ledger) {
  if(n>=0) {
    const repayment=Math.min(n,p.funding);p.funding-=repayment;n-=repayment;
    p.stock+=n*weight;p.stockBasis+=n*weight;p.treasury+=n*(1-weight);
  } else {
    let need=-n;const cash=Math.min(need,p.treasury);p.treasury-=cash;need-=cash;
    if(need>0&&p.stock>0) {
      const gainShare=Math.max(0,1-p.stockBasis/p.stock),stockBefore=p.stock;
      const net=sell=>sell-ledger.quote('gain',sell*gainShare);
      let low=0,high=stockBefore;
      for(let k=0;k<48;k++){const mid=(low+high)/2;if(net(mid)<need)low=mid;else high=mid;}
      const sell=high,tax=ledger.charge('gain',sell*gainShare),frac=sell/stockBefore;
      p.stock=Math.max(0,p.stock-sell);p.stockBasis=Math.max(0,p.stockBasis*(1-frac));p.taxes+=tax;
      need=Math.max(0,need-(sell-tax));
    }
    p.funding+=need;
  }
}
function advancePortfolio(p,startMonth,i,isStaged,ledger) {
  const taxStart=p.taxes;let dividends=0,treasuryInterest=0;
  for(let k=0;k<12;k++) {
    const m=startMonth+k;
    if(isStaged&&m>=i.parkMonths&&m<i.parkMonths+i.phaseMonths&&p.deployed<p.planned) {
      const scheduled=Math.min(p.planned-p.deployed,p.planned/i.phaseMonths);
      const tranche=Math.min(scheduled,Math.max(0,p.treasury));
      p.treasury-=tranche;p.stock+=tranche;p.stockBasis+=tranche;p.deployed+=tranche;p.missedPhase+=scheduled-tranche;
    }
    const dividend=p.stock*.018/12,divTax=ledger.charge('dividend',dividend);
    p.stock=Math.max(0,p.stock*(1+equityMonthlyReturn(m,i))-divTax);
    p.stockBasis+=Math.max(0,dividend-divTax);dividends+=dividend;
    const interest=p.treasury*treasuryYieldAt(m,i)/12,interestTax=ledger.charge('treasury',interest);
    p.treasury+=interest-interestTax;p.taxes+=divTax+interestTax;treasuryInterest+=interest;
  }
  p.funding*=1+i.fundingRate;
  return {tax:p.taxes-taxStart,dividends,treasuryInterest};
}
function aUse(path,year) {
  if(path==='live') return 'live';
  if(path==='rent') return 'rent';
  if(path==='rent-sell') return year<=5?'rent':'sold';
  if(path==='live-sell') return year<=10?'live':'sold';
  if(path==='live-rent') return year<=10?'live':'rent';
  return 'sold';
}
function eligible121(path,year,i) {
  if(!i.section121) return false;
  if(path==='live'||(path==='live-sell'&&year>=2)) return year>=2;
  if(path==='live-rent') return year>=2&&year<=13; // 10 years lived; last 2/5 years remain through year 13
  return false;
}
export function simulatePath(path,i=defaultInputs()) {
  validateInputs(i);
  if(!['live','rent','sell','staged','rent-sell','live-sell','live-rent'].includes(path)) throw new Error('Unknown decision path.');
  const pre=i.transferYear-CURRENT.year;
  const inheritA=i.marketA*Math.pow(1+i.homeGrowth,pre),inheritB=i.marketB*Math.pow(1+i.homeGrowth,pre);
  const transferBase=i.assessedA*Math.pow(1+i.assessedGrowth,pre),allowance=prop19Allowance(i.transferYear,i.prop19Growth);
  const eligible=i.prop19Eligible&&i.longTermOccupancy&&['live','live-sell','live-rent'].includes(path);
  const aStartAssessment=prop19Assessment(inheritA,transferBase,allowance,eligible);
  const bStartAssessment=i.assessedB*Math.pow(1+i.assessedGrowth,pre);
  const p=portfolio();p.treasury=i.workingReserve;
  let marketA=inheritA,marketB=inheritB,debtA=i.debtA,debtB=i.debtB;
  let basisA=inheritA*i.basisFraction,depA=0,rentalStarted=false;
  const landBasis=inheritA*i.basisFraction*i.landShare,aVintages=[];
  // B's preexisting basis is NOT stepped up by A's inheritance. Start dates
  // and earlier deductions are private facts; this is a remaining-life proxy.
  const bVintages=[{basis:i.bDepreciableBasis,recovered:Math.min(i.bDepreciableBasis,i.bPriorDepreciation),start:0}];
  let priceIndex=Math.pow(1+i.inflation,pre),rentIndex=Math.pow(1+i.rentGrowth,pre);
  let totalCapex=0,totalOperating=0,totalTax=0,totalRent=0,housingPV=0,peakFunding=0;
  let sale=null,held=!['sell','staged'].includes(path),ledger=annualTaxLedger(i);
  function executeSale(year) {
    const use121=eligible121(path,year,i);
    const q=saleQuote({market:marketA,basis:basisA,debt:debtA,depreciation:depA,eligible121:use121},i,ledger.context());
    ledger.record(q.taxable);
    if(path==='staged') {contribute(p,q.net,0,i,ledger);p.planned=Math.max(0,q.net)*i.stockTarget;}
    else contribute(p,q.net,i.stockTarget,i,ledger);
    totalTax+=q.tax;totalOperating+=q.sellingCosts;debtA=0;held=false;sale={...q,year,eligible121:use121};return q;
  }
  if(!held) {marketA*=1+i.sameYearMove;executeSale(0);}
  peakFunding=p.funding;
  const rows=[];
  function snapshot(year,extra={}) {
    const context=ledger.context();
    const exitA=held?saleQuote({market:marketA,basis:basisA,debt:debtA,depreciation:depA,eligible121:eligible121(path,year,i)},i,context):null;
    if(exitA){context.ca+=exitA.taxable;context.magi+=exitA.taxable;context.nii+=exitA.taxable;}
    const stockExit=gainTaxes(Math.max(0,p.stock-p.stockBasis),0,0,i,context);
    const liquid=p.treasury+p.stock-stockExit.tax-p.funding,nominal=liquid+(exitA?exitA.net:0);
    return {year,calendarYear:i.transferYear+year,marketA:held?marketA:0,marketB,
      assessedA:held?Math.min(marketA,(eligible&&aUse(path,Math.max(1,year))==='live'?aStartAssessment:inheritA)*Math.pow(1+i.assessedGrowth,year)):0,
      assessedB:Math.min(marketB,bStartAssessment*Math.pow(1+i.assessedGrowth,year)),
      basisA:held?basisA:0,depA,debtA:held?debtA:0,debtB,stocks:p.stock,treasuries:p.treasury,
      funding:p.funding,liquid,nominal,real:nominal/priceIndex,bRetainedEquity:marketB-debtB,
      terminalTax:(exitA?.tax??0)+stockExit.tax,terminalSaleCosts:exitA?.sellingCosts??0,
      priceIndex,capex:0,operating:0,rent:0,netCash:0,propertyTaxA:0,propertyTaxB:0,taxes:0,...extra};
  }
  rows.push(snapshot(0,{saleTax:sale?.tax??0,saleNet:sale?.net??0,saleCosts:sale?.sellingCosts??0}));
  for(let y=1;y<=i.horizon;y++) {
    ledger=annualTaxLedger(i);
    const use=aUse(path,y),liveA=held&&use==='live',rentA=held&&use==='rent',liveB=!liveA;
    const prevIndex=priceIndex,marketAtStart=marketA;
    // At residential-to-rental conversion, depreciation uses the lower of
    // adjusted building basis or allocated FMV, separate from gain/loss basis.
    if(rentA&&!rentalStarted) {
      aVintages.push({basis:Math.max(0,Math.min(basisA-landBasis,marketAtStart*(1-i.landShare))),recovered:0,start:y});
      rentalStarted=true;
    }
    const aFactored=(eligible&&liveA?aStartAssessment:inheritA)*Math.pow(1+i.assessedGrowth,y-1);
    const assessedA=held?Math.min(marketAtStart,aFactored):0;
    const assessedB=Math.min(marketB,bStartAssessment*Math.pow(1+i.assessedGrowth,y-1));
    priceIndex*=1+inflationAt(y-1,i);
    marketA*=1+housingReturnAt(y-1,i);marketB*=1+housingReturnAt(y-1,i);
    rentIndex*=1+Math.max(-.02,Math.min(i.rentGrowth,inflationAt(y-1,i)+.01));
    const insuranceIndex=Math.pow(1+i.insuranceGrowth,pre+y);
    const aDebt=annualDebt(held?debtA:0,i.mortgageRate,Math.max(1,i.mortgageYears-y+1));debtA=aDebt.balance;
    const bDebt=annualDebt(debtB,i.mortgageRate,Math.max(1,i.mortgageYears-y+1));debtB=bDebt.balance;
    const aTax=held?assessedA*i.adValoremA+i.directA*prevIndex:0;
    const propHCharge=propHCalendar(i.transferYear+y-1,i,liveB);
    const bTax=assessedB*i.adValoremB+i.directB*prevIndex+propHCharge;
    const aInsurance=held?i.insuranceA*insuranceIndex*(rentA?i.landlordInsuranceFactor:1):0;
    const aUtility=held?i.utilitiesA*prevIndex*(rentA?i.landlordUtilityShare:1):0;
    const aMaintenance=held?i.maintenanceA*prevIndex:0;
    const bInsurance=i.insuranceB*insuranceIndex,bUtility=i.utilitiesB*prevIndex,bMaintenance=i.maintenanceB*prevIndex;
    const capitalA=held?capitalAt('A',y,i,prevIndex):0,capitalB=capitalAt('B',y,i,prevIndex);
    if(held) basisA+=capitalA;
    if(rentA&&capitalA>0)aVintages.push({basis:capitalA,recovered:0,start:y});
    if(capitalB>0)bVintages.push({basis:capitalB*i.bRentalShare,recovered:0,start:y});
    const yearDepA=rentA?aVintages.reduce((s,v)=>s+depreciationStep(v,y),0):0;
    depA+=yearDepA;basisA-=yearDepA;
    const bDep=bVintages.reduce((s,v)=>s+depreciationStep(v,y),0);
    const stressVacancy=['depression','gfc'].includes(i.scenario)&&y<=3?.15:0;
    const collectedA=rentA?i.rentA*12*rentIndex*(1-Math.min(.9,i.vacancy+stressVacancy)):0;
    const extraB=liveA&&i.allowExtraBRent?i.extraBRent*12*rentIndex:0;
    const collectedB=(i.rentB*12*rentIndex+extraB)*(1-Math.min(.9,i.vacancy+stressVacancy));
    const managementA=collectedA*i.management,managementB=collectedB*i.management;
    const aOperating=aTax+aInsurance+aUtility+aMaintenance+managementA;
    const bOperating=bTax+bInsurance+bUtility+bMaintenance+managementB;
    const taxableA=rentA?collectedA-aOperating-aDebt.interest-yearDepA:0;
    const taxableB=collectedB-(bTax+bInsurance+bUtility+bMaintenance+bDebt.interest)*i.bRentalShare-managementB-bDep;
    // Losses receive no current or terminal tax benefit in this conservative proxy.
    const annualIncomeTax=ledger.charge('rental',Math.max(0,taxableA)+Math.max(0,taxableB));
    const portfolioResult=advancePortfolio(p,(y-1)*12,i,path==='staged',ledger);
    const netCash=collectedA+collectedB-aOperating-bOperating-capitalA-capitalB-aDebt.payment-bDebt.payment-annualIncomeTax;
    const contributionWeight=path==='staged'&&y*12<i.parkMonths+i.phaseMonths?0:i.stockTarget;
    const taxesBeforeWithdrawal=p.taxes;contribute(p,netCash,contributionWeight,i,ledger);
    const forcedSaleTax=p.taxes-taxesBeforeWithdrawal;
    // Fixed sale occurs at the END of the fifth/tenth operating year, including
    // when that year is the selected horizon. Never defer it to year 6/11.
    let saleEvent=null;
    if(held&&((path==='rent-sell'&&y===5)||(path==='live-sell'&&y===10)))saleEvent=executeSale(y);
    peakFunding=Math.max(peakFunding,p.funding);
    const housingDifference=liveA?(i.imputedA-i.imputedB)*12*prevIndex:0;
    housingPV+=housingDifference/Math.pow(1.03,y);
    totalCapex+=capitalA+capitalB;totalOperating+=aOperating+bOperating;
    totalTax+=annualIncomeTax+portfolioResult.tax+forcedSaleTax;totalRent+=collectedA+collectedB;
    rows.push(snapshot(y,{assessedA,assessedB,propertyTaxA:aTax,propertyTaxB:bTax,propHCharge,
      capex:capitalA+capitalB,capexA:capitalA,capexB:capitalB,operating:aOperating+bOperating,
      rent:collectedA+collectedB,rentA:collectedA,rentB:collectedB,netCash,
      taxes:annualIncomeTax+portfolioResult.tax+forcedSaleTax+(saleEvent?.tax??0),
      saleNet:saleEvent?.net??0,saleTax:saleEvent?.tax??0,saleCosts:saleEvent?.sellingCosts??0,
      depreciation:yearDepA+bDep,depreciationA:yearDepA,depreciationB:bDep,taxableRentalA:taxableA,taxableRentalB:taxableB,
      interest:aDebt.interest+bDebt.interest,principal:aDebt.principal+bDebt.principal,
      dividends:portfolioResult.dividends,treasuryInterest:portfolioResult.treasuryInterest,
      stockPhaseDeployed:p.deployed,stockPhasePlanned:p.planned,
      housingDifference,use:saleEvent?use+' → sold':held?use:'sold'}));
  }
  const end=rows.at(-1);
  return {path,inputs:i,rows,end,sale,inheritA,inheritB,transferBase,allowance,aStartAssessment,bStartAssessment,
    prop19Applied:eligible,totalCapex,totalOperating,totalTax,totalRent,housingPV,peakFunding,
    stagedPlanned:p.planned,stagedDeployed:p.deployed,stagedMissed:Math.max(0,p.planned-p.deployed),
    firstYearCash:rows[1].netCash,liquidityFlag:peakFunding>.01,method:'Synthetic scenario; not a household estimate or tax return.'};
}
export function runComparison(i=defaultInputs()) {
  return ['live','rent','sell','staged','rent-sell','live-sell','live-rent'].map(p=>simulatePath(p,i)).sort((a,b)=>b.end.nominal-a.end.nominal);
}
export function rangeVariants(i) {
  const shift=(down)=>({...i,marketA:i.marketA*(down?.8:1.2),rentA:i.rentA*(down?.75:1.25),rentB:i.rentB*(down?.85:1.15),
    homeGrowth:i.homeGrowth+(down?-.015:.015),stockGrowth:i.stockGrowth+(down?-.02:.02),inflation:i.inflation+(down?.01:-.01),
    maintenanceA:i.maintenanceA*(down?1.25:.75),maintenanceB:i.maintenanceB*(down?1.25:.75),
    insuranceA:i.insuranceA*(down?1.25:.75),insuranceB:i.insuranceB*(down?1.25:.75),vacancy:Math.max(0,Math.min(.9,i.vacancy+(down?.03:-.03)))});
  return [shift(true),{...i},shift(false)];
}
export function rangeComparison(i) {
  const runs=rangeVariants(i).map(v=>runComparison(v));
  return runs[1].map(base=>{
    const all=runs.map(r=>r.find(v=>v.path===base.path));
    const vals=all.map(r=>r.end.nominal);
    return {...base,low:Math.min(...vals),high:Math.max(...vals),ranks:runs.map(r=>r.findIndex(v=>v.path===base.path)+1)};
  });
}
export function comparisonMatrix(i) {
  return [2040,2045,2050].flatMap(transferYear=>[10,20,30,50].map(horizon=>{
    const runs=runComparison({...i,transferYear,horizon});
    return {transferYear,horizon,leader:runs[0].path,gap:runs[0].end.nominal-runs[1].end.nominal,nominal:runs[0].end.nominal};
  }));
}
export function scenarioDistribution(path,i) {
  const values=[];
  // Fixed factorial grid: 3^4 = 81 design points; no probabilistic claims.
  for(const homeShift of [-.015,0,.015]) for(const stockShift of [-.02,0,.02]) for(const cost of [.75,1,1.25]) for(const rentScale of [.75,1,1.25]) {
    const v={...i,homeGrowth:i.homeGrowth+homeShift,stockGrowth:i.stockGrowth+stockShift,
      maintenanceA:i.maintenanceA*cost,maintenanceB:i.maintenanceB*cost,insuranceA:i.insuranceA*cost,insuranceB:i.insuranceB*cost,
      rentA:i.rentA*rentScale};
    values.push(simulatePath(path,v).end.real);
  }
  return values.sort((a,b)=>a-b);
}
export function sensitivityRows(i) {
  const base=runComparison(i)[0].path;
  return [
    ['A rent / month','rentA',i.rentA*.75,i.rentA*1.25],
    ['Home growth center','homeGrowth',Math.max(-.05,i.homeGrowth-.02),i.homeGrowth+.02],
    ['Stock growth center','stockGrowth',i.stockGrowth-.03,i.stockGrowth+.03],
    ['Treasury starting yield','treasuryYield',.01,.05],
    ['California marginal rate','californiaRate',.093,.123],
    ['Capital-work multiplier','capexScale',.5,2]
  ].map(([label,key,low,high])=>({label,key,low,high,base,
    lowLeader:runComparison({...i,[key]:low})[0].path,highLeader:runComparison({...i,[key]:high})[0].path}));
}
