import test from 'node:test';
import assert from 'node:assert/strict';
import {defaultInputs,bhTax,bhIncrement,niitTax,gainTaxes,annualTaxLedger,saleQuote,documentaryTax,annualDebt,prop19Assessment,prop19Allowance,propH,propHCalendar,depreciationStep,money10} from '../model.js';
const near=(a,b,tol=1e-6)=>assert.ok(Math.abs(a-b)<=tol,`${a} ≠ ${b}`);

test('Form 540 1% is only income above $1m, not proceeds',()=>{
 for(const [income,due] of [[-1,0],[900000,0],[1000000,0],[1100000,1000],[1500000,5000]])near(bhTax(income),due);
 near(bhIncrement(900000,200000),1000);near(bhIncrement(1200000,200000),2000);near(bhIncrement(1200000,-1000),0);
});
test('NIIT lesser-of calculation and filing threshold',()=>{
 near(niitTax(100000,225000,250000),2850);near(niitTax(20000,100000,250000),0);
 near(niitTax(100000,300000,250000),3800);near(niitTax(-100,300000,200000),0);
});
test('gain separates excluded gain, §1250 and federal/state/NIIT',()=>{
 const i={...defaultInputs(),federalOrdinary:.24,federalGains:.15,californiaRate:.1,otherTaxableIncome:900000};
 const q=gainTaxes(1000000,200000,500000,i);
 near(q.unrecaptured,200000);near(q.excluded,500000);near(q.taxable,500000);
 near(q.federal,300000*.15+200000*.24);near(q.california,50000);near(q.surtax,4000);near(q.niit,19000);
 near(gainTaxes(-1000,0,0,i).tax,0);
});
test('§1250 federal maximum 25%; exclusion cannot erase depreciation-related gain',()=>{
 const i={...defaultInputs(),federalOrdinary:.37};const q=gainTaxes(100000,100000,500000,i);
 near(q.federal,25000);near(q.excluded,0);
});
test('annual ledger aggregates thresholds rather than taxing components in isolation',()=>{
 const i={...defaultInputs(),otherTaxableIncome:150000,niitThreshold:200000,californiaRate:0,federalOrdinary:0,federalGains:0};
 const l=annualTaxLedger(i);near(l.charge('rental',30000),0);near(l.charge('dividend',30000),380);
 const h={...i,otherTaxableIncome:900000,niitExposed:false};const x=annualTaxLedger(h);
 near(x.charge('rental',90000),0);near(x.charge('dividend',20000),100);
});
test('annual tax is order-independent for same income classes',()=>{
 const i={...defaultInputs(),otherTaxableIncome:950000};const l=annualTaxLedger(i),r=annualTaxLedger(i);
 near(l.charge('rental',90000)+l.charge('dividend',30000)+l.charge('treasury',10000),r.charge('treasury',10000)+r.charge('dividend',30000)+r.charge('rental',90000));
});
test('Treasury interest excluded from CA and 1% threshold, included in conditional NIIT',()=>{
 const i={...defaultInputs(),otherTaxableIncome:995000,federalOrdinary:.3,californiaRate:.12};
 const l=annualTaxLedger(i);near(l.charge('treasury',10000),3380);near(l.context().ca,995000);near(l.context().magi,1005000);
 near(l.charge('dividend',10000),10000*(i.federalGains+i.californiaRate+.038)+50);
});
test('transfer tax uses fractions; sale costs affect gain, debt does not',()=>{
 near(documentaryTax(500),.55);near(documentaryTax(501),1.10);near(documentaryTax(1000,500),.55);near(documentaryTax(-10),0);
 const i={...defaultInputs(),saleCost:0,recordingReserve:0,escrowReserve:0};
 const a=saleQuote({market:2000000,basis:1000000},i),b=saleQuote({market:2000000,basis:1000000,debt:300000},i);
 near(a.tax,b.tax);near(a.net-b.net,300000);near(a.amountRealized,2000000-2200);
 assert.equal(saleQuote({market:1000000,basis:2000000},i).tax,0);
});
test('monthly amortization reconciles balance, interest, principal and zero-rate loan',()=>{
 const a=annualDebt(100000,.05,30);near(a.principal,100000-a.balance);near(a.payment,a.interest+a.principal);assert.ok(a.interest<5000);
 const b=annualDebt(120000,0,10);near(b.payment,12000);near(b.interest,0);near(b.balance,108000);
 const c=annualDebt(1000,.05,1);near(c.balance,0,1e-5);assert.ok(c.payment>1000);
 assert.deepEqual(annualDebt(0,.05),{balance:0,payment:0,interest:0,principal:0});
});
test('Prop 19 formula and future allowance cycles are explicit',()=>{
 near(prop19Assessment(3000000,500000,1000000,true),2000000);near(prop19Assessment(1200000,500000,1000000,true),500000);
 near(prop19Assessment(300000,500000,1000000,true),300000);near(prop19Assessment(3000000,500000,1000000,false),3000000);
 near(prop19Allowance(2025,.02),1044586);near(prop19Allowance(2026,.02),1044586);
 near(prop19Allowance(2027,.02),1044586*1.02**2);near(prop19Allowance(2028,.02),prop19Allowance(2027,.02));
});
test('Prop H multifamily is per parcel, increments above 5000, with cap and deduction',()=>{
 near(propH({area:4000}),249);near(propH({area:6000}),444);near(propH({area:1000000}),50000);
 near(propH({area:4000,seniorUnits:1}),0);near(propH({area:6000,seniorUnits:1}),195);near(propH({area:4000,seniorUnits:2}),0);
 near(propH({area:6000,sroArea:2000}),249);near(propH({area:6000,exempt:true}),0);
});
test('Prop H legal single-family upper rate is $1.99, not summary $1.19',()=>{
 near(propH({type:'single',area:3000}),129);near(propH({type:'single',area:5000}),969);near(propH({type:'single',area:6000}),2959);
 near(propH({type:'single',area:6000,seniorOwner:true}),0);
});
test('Prop H CPI rounds down amounts / rates and sunsets at FY2042',()=>{
 near(propH({area:6000,fiscalYear:2028,cpiRates:[.03]}),256+1000*.2);
 near(propH({area:6000,fiscalYear:2028,cpiRates:[-.02]}),444);
 near(propH({area:6000,fiscalYear:2026}),0);near(propH({area:6000,fiscalYear:2042}),0);
 const i={...defaultInputs(),includePropH:true,propHCpi:0,bBuildingArea:4000};near(propHCalendar(2027,i),124.5);near(propHCalendar(2042,i),124.5);near(propHCalendar(2043,i),0);
 near(propHCalendar(2027,{...i,includePropH:false}),0);
});
test('Prop H nonres/unimproved sensitivity; mixed use explicitly rejected',()=>{
 near(propH({type:'nonres',area:5000}),799);near(propH({type:'nonres',area:50000}),34999);near(propH({type:'nonres',area:250000}),202999);
 near(propH({type:'nonres',area:1000000}),400000);near(propH({type:'unimproved',landArea:2000}),0);near(propH({type:'unimproved',landArea:2001}),392);
 assert.throws(()=>propH({type:'mixed'}),/review/);
});
test('depreciation capped by vintage; January first year uses 11.5 months',()=>{
 const v={basis:275000,recovered:0,start:3};near(depreciationStep(v,2),0);near(depreciationStep(v,3),10000*11.5/12);
 let total=v.recovered;for(let y=4;y<60;y++)total+=depreciationStep(v,y);near(total,275000);near(depreciationStep(v,60),0);
});
test('$10 display rounding leaves calculation inputs alone',()=>{near(money10(1044586),1044590);near(money10(144),140);near(money10(-144),-140);});
