import { defaultInputs, validateInputs, gainTaxes, annualTaxLedger } from './model.js';
import { equityMonthlyReturn, inflationAt, treasuryYieldAt } from './economy.js';

/** Synthetic monthly investment-only comparison. The 3/6/12/24-month tenors
 * approximate 13/26/52-week bills and 2-year notes. Terms are fixed at purchase.
 * Bills accrue simple interest to maturity; 24-month notes pay every six months.
 * Taxes are withheld from interest when paid (accrued net at the horizon).
 * No early bond sales, mark-to-market model, auction discount pricing, or exact
 * day-count conventions. Phase cash is held without interest to match spending.
 */
export function simulateCrash({initial=1000000,months=360,parkMonths=24,phaseMonths=12,inputs=defaultInputs()}={}) {
  if(initial<=0||!Number.isFinite(initial)||!Number.isInteger(months)||months<1||months>600) throw new Error('Invalid investment example.');
  if(![0,24,36].includes(parkMonths)||![12,24].includes(phaseMonths)) throw new Error('Invalid staging schedule.');
  const i=validateInputs(inputs);
  let ledger=annualTaxLedger(i);
  let stock=parkMonths===0?initial*i.stockTarget:0,stockBasis=stock;
  let freeCash=initial-stock,phaseCash=0,phaseBudget=0,phaseDeployed=0,interestTax=0,dividendTax=0;
  let holdings=[],priceIndex=1,peak=initial,maxDrawdown=0;
  const rows=[{month:0,value:initial,real:initial,stock,treasury:initial-stock,cash:0,drawdown:0}];
  function buyLadder(month) {
    const beforePark=parkMonths>0&&month<parkMonths;
    const deadline=beforePark?parkMonths-month:Infinity;
    const terms=[3,6,12,24].filter(t=>t<=deadline);
    if(!terms.length||freeCash<.01) return;
    const each=freeCash/terms.length;freeCash=0;
    for(const term of terms) holdings.push({principal:each,rate:treasuryYieldAt(month,i),start:month,term,maturity:month+term,accrued:0});
  }
  function settle(month) {
    const remain=[];
    for(const h of holdings) {
      const coupon=h.term===24&&(month-h.start)%6===0&&month>h.start;
      if(h.maturity===month||coupon) {
        const tax=ledger.charge('treasury',h.accrued);
        freeCash+=h.accrued-tax;interestTax+=tax;h.accrued=0;
      }
      if(h.maturity===month) freeCash+=h.principal;else remain.push(h);
    }
    holdings=remain;
  }
  for(let m=0;m<months;m++) {
    if(m>0&&m%12===0)ledger=annualTaxLedger(i);
    settle(m);
    if(parkMonths>0&&m===parkMonths) {
      // All parked ladder principal is maturity-matched to the phase date.
      phaseBudget=freeCash*i.stockTarget;phaseCash=phaseBudget;freeCash-=phaseBudget;
    }
    if(parkMonths>0&&m>=parkMonths&&m<parkMonths+phaseMonths) {
      const tranche=m===parkMonths+phaseMonths-1?phaseCash:Math.min(phaseCash,phaseBudget/phaseMonths);
      stock+=tranche;stockBasis+=tranche;phaseCash-=tranche;phaseDeployed+=tranche;
    }
    buyLadder(m);
    const dividend=stock*.018/12;
    const divTax=ledger.charge('dividend',dividend);
    stock=Math.max(0,stock*(1+equityMonthlyReturn(m,i))-divTax);
    stockBasis+=Math.max(0,dividend-divTax);dividendTax+=divTax;
    for(const h of holdings) h.accrued+=h.principal*h.rate/12;
    priceIndex*=Math.pow(1+inflationAt(Math.floor(m/12),i),1/12);
    const accrued=holdings.reduce((s,h)=>s+h.accrued,0);
    const treasury=freeCash+phaseCash+holdings.reduce((s,h)=>s+h.principal,0)+accrued-ledger.quote('treasury',accrued);
    const value=stock+treasury;peak=Math.max(peak,value);const drawdown=value/peak-1;maxDrawdown=Math.min(maxDrawdown,drawdown);
    rows.push({month:m+1,value,real:value/priceIndex,stock,treasury,cash:freeCash+phaseCash,drawdown});
  }
  const accrued=holdings.reduce((s,h)=>s+h.accrued,0),context=ledger.context();
  const accruedInterestTax=ledger.quote('treasury',accrued);
  context.nii+=accrued;context.magi+=accrued;
  const end=rows.at(-1),exitTax=gainTaxes(Math.max(0,stock-stockBasis),0,0,i,context).tax;
  return {initial,parkMonths,phaseMonths,rows,maxDrawdown,interestTax,dividendTax,exitTax,accruedInterestTax,
    end:{...end,afterTax:end.value-exitTax,realAfterTax:(end.value-exitTax)/priceIndex},phaseBudget,phaseDeployed,
    finalHoldings:holdings.map(h=>({...h})),method:'Hypothetical monthly shape; not a historical backtest or guaranteed ladder return.'};
}
export function crashComparison(inputs,months=360) {
  return [0,24,36].map(parkMonths=>simulateCrash({inputs,months,parkMonths,phaseMonths:inputs.phaseMonths}));
}
