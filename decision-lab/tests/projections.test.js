import test from 'node:test';
import assert from 'node:assert/strict';
import {defaultInputs,validateInputs,simulatePath,runComparison,rangeComparison,comparisonMatrix,scenarioDistribution,sensitivityRows,annualDebt,CAPITAL_PLAN} from '../model.js';
import {SCENARIOS} from '../economy.js';
const near=(a,b,tol=1e-5)=>assert.ok(Math.abs(a-b)<=tol,`${a} ≠ ${b}`);
const ids=['live','rent','sell','staged','rent-sell','live-sell','live-rent'];

test('defaults are complete, finite, synthetic and do not enable conditional Prop 19/H/extra rent',()=>{
 const i=defaultInputs();assert.equal(validateInputs(i),i);assert.equal(i.prop19Eligible,false);assert.equal(i.longTermOccupancy,false);assert.equal(i.includePropH,false);assert.equal(i.allowExtraBRent,false);
});
test('invalid/nonfinite/missing/unsupported controls fail before simulation',()=>{
 const i=defaultInputs();for(const bad of [{horizon:0},{horizon:51},{horizon:1.5},{transferYear:2025},{marketA:NaN},{marketB:Infinity},{vacancy:1.1},{debtB:-1},{scenario:'fiction'},{parkMonths:30},{assessedGrowth:.03},{federalGains:-.1},{mortgageYears:0},{longTermOccupancy:'yes'},{section121Limit:750000},{marketA:undefined}]) assert.throws(()=>simulatePath('rent',{...i,...bad}));
 assert.throws(()=>simulatePath('other',i),/Unknown/);
});
test('all seven paths have identical dates, horizons and original A/B values',()=>{
 const i=defaultInputs(),runs=runComparison(i);assert.equal(runs.length,7);assert.deepEqual(new Set(runs.map(r=>r.path)),new Set(ids));
 for(const r of runs){assert.equal(r.rows.length,i.horizon+1);assert.equal(r.rows[0].calendarYear,i.transferYear);assert.equal(r.end.calendarYear,i.transferYear+i.horizon);near(r.inheritA,runs[0].inheritA);near(r.inheritB,runs[0].inheritB);}
});
test('B assessment and continuing leased rent never reset or disappear due to living in B',()=>{
 const i=defaultInputs(),runs=runComparison(i),b=simulatePath('rent',{...i,marketA:i.marketA*2});
 for(const r of runs){near(r.bStartAssessment,runs[0].bStartAssessment);for(let y=1;y<=i.horizon;y++)near(r.rows[y].rentB,runs[0].rows[y].rentB);}
 near(b.bStartAssessment,runs[0].bStartAssessment);near(b.end.marketB,runs[0].end.marketB);
 assert.ok(b.bStartAssessment<b.inheritB);
});
test('extra B income is opt-in only and does not change existing B rent in other paths',()=>{
 const i={...defaultInputs(),horizon:2,extraBRent:3000};near(simulatePath('live',i).rows[1].rentB,simulatePath('rent',i).rows[1].rentB);
 assert.ok(simulatePath('live',{...i,allowExtraBRent:true}).rows[1].rentB>simulatePath('live',i).rows[1].rentB);
 near(simulatePath('rent',{...i,allowExtraBRent:true}).rows[1].rentB,simulatePath('rent',i).rows[1].rentB);
});
test('Prop 19 requires both eligibility and genuine intent; never applies to rental or sale',()=>{
 const i={...defaultInputs(),horizon:12};assert.equal(simulatePath('live',{...i,prop19Eligible:true}).prop19Applied,false);assert.equal(simulatePath('live',{...i,longTermOccupancy:true}).prop19Applied,false);
 const yes={...i,prop19Eligible:true,longTermOccupancy:true};assert.equal(simulatePath('live',yes).prop19Applied,true);
 for(const path of ['rent','sell','staged','rent-sell'])assert.equal(simulatePath(path,yes).prop19Applied,false);
 assert.ok(simulatePath('live',yes).rows[1].propertyTaxA<simulatePath('live',i).rows[1].propertyTaxA);
});
test('leaving A after ten years restores transfer-FMV factored base, not permanent reduced base',()=>{
 const i={...defaultInputs(),horizon:12,prop19Eligible:true,longTermOccupancy:true},r=simulatePath('live-rent',i);
 near(r.rows[11].assessedA,Math.min(r.rows[10].marketA,r.inheritA*(1+i.assessedGrowth)**10));
 assert.equal(r.rows[10].use,'live');assert.equal(r.rows[11].use,'rent');assert.ok(r.rows[11].propertyTaxA>r.rows[10].propertyTaxA);
});
test('same-tax-year sale is event zero; post-death price movement changes taxable gain',()=>{
 const i={...defaultInputs(),horizon:1,saleCost:0,recordingReserve:0,escrowReserve:0};const r=simulatePath('sell',i),up=simulatePath('sell',{...i,sameYearMove:.2});
 assert.equal(r.sale.year,0);assert.equal(r.rows[0].marketA,0);assert.equal(r.sale.eligible121,false);near(r.sale.tax,0);assert.ok(up.sale.tax>0);near(up.sale.basis,r.sale.basis);
});
test('mixed sales execute at exact horizon end and keep full-year preceding rents',()=>{
 for(const [path,y] of [['rent-sell',5],['live-sell',10]]){
  const i={...defaultInputs(),horizon:y},r=simulatePath(path,i),stay=simulatePath(path==='rent-sell'?'rent':'live',i);
  assert.equal(r.sale.year,y);near(r.end.marketA,0);near(r.end.debtA,0);near(r.end.basisA,0);near(r.end.rentA,stay.end.rentA);near(r.end.saleNet,r.sale.net);assert.ok(r.end.use.endsWith('sold'));
 }
 assert.equal(simulatePath('rent-sell',{...defaultInputs(),horizon:4}).sale,null);
});
test('conditional §121 does not leak to pure rental or same-year exits',()=>{
 const i={...defaultInputs(),horizon:10,homeGrowth:.05};const yes=simulatePath('live-sell',i),no=simulatePath('live-sell',{...i,section121:false});assert.ok(yes.sale.excluded>0);near(no.sale.excluded,0);
 for(const p of ['sell','staged','rent-sell'])near(simulatePath(p,i).sale.excluded,0);
});
test('capital schedules include both buildings and post-year-five renewal, not reserve plus spend',()=>{
 const i={...defaultInputs(),transferYear:2026,horizon:6},r=simulatePath('live',i);
 near(r.rows[1].capexA,(CAPITAL_PLAN.A[0].low+CAPITAL_PLAN.A[0].high)/2*i.capexScale);
 near(r.rows[1].capexB,(CAPITAL_PLAN.B[0].low+CAPITAL_PLAN.B[0].high)/2*i.capexScale);
 near(r.rows[6].capexA,i.renewalA*i.capexScale*r.rows[5].priceIndex);near(r.rows[6].capexB,i.renewalB*i.capexScale*r.rows[5].priceIndex);
 const sold=simulatePath('sell',i);assert.equal(sold.rows[1].capexA,0);assert.ok(sold.rows[1].capexB>0);
});
test('A basis increases for capital and decreases for actual modeled depreciation',()=>{
 const i={...defaultInputs(),horizon:15},r=simulatePath('rent',i);let basis=r.inheritA*i.basisFraction;
 for(const row of r.rows.slice(1)){basis+=row.capexA-row.depreciationA;near(row.basisA,basis);assert.ok(row.basisA>=r.inheritA*i.basisFraction*i.landShare-1e-5);}
});
test('rental conversion depreciation uses lower conversion FMV, separate gain basis',()=>{
 const i={...defaultInputs(),transferYear:2026,horizon:11,homeGrowth:-.05,capexScale:0},r=simulatePath('live-rent',i);
 const depBasis=Math.min(r.inheritA*i.basisFraction*(1-i.landShare),r.rows[10].marketA*(1-i.landShare));
 near(r.rows[11].depreciationA,depBasis/27.5*11.5/12);assert.ok(depBasis<r.inheritA*(1-i.landShare));
 near(r.end.basisA,r.inheritA*i.basisFraction-r.rows[11].depreciationA);
});
test('B rental capital improvements produce separately capped depreciation, no inheritance reset',()=>{
 const i={...defaultInputs(),horizon:2},cap=simulatePath('sell',i),no=simulatePath('sell',{...i,capexScale:0});
 near(cap.rows[1].depreciationB-no.rows[1].depreciationB,cap.rows[1].capexB*i.bRentalShare/27.5*11.5/12);
 const changedA=simulatePath('sell',{...i,marketA:i.marketA*3});near(cap.rows[1].depreciationB,changedA.rows[1].depreciationB);
});
test('mortgage principal is cash-only; interest alone reduces rental taxable income',()=>{
 const i={...defaultInputs(),horizon:1,debtA:0},a=simulatePath('rent',i),b=simulatePath('rent',{...i,debtA:100000}),d=annualDebt(100000,i.mortgageRate,i.mortgageYears);
 near(a.end.taxableRentalA-b.end.taxableRentalA,d.interest);near(b.end.principal-a.end.principal,d.principal);near(b.end.debtA,100000-d.principal);
});
test('real/nominal, common retained B and liquidity are distinguished',()=>{
 for(const r of runComparison(defaultInputs()))for(const row of r.rows){near(row.real*row.priceIndex,row.nominal,1e-4);near(row.bRetainedEquity,row.marketB-row.debtB);assert.ok(row.liquid<=row.stocks+row.treasuries+1e-5);}
 const stressed=simulatePath('live',{...defaultInputs(),workingReserve:0,rentB:0});assert.equal(stressed.liquidityFlag,true);assert.ok(stressed.peakFunding>0);assert.ok(stressed.end.nominal<stressed.end.marketA);
});
test('imputed housing service never becomes cash or wealth',()=>{
 const i={...defaultInputs(),horizon:10},a=simulatePath('live',i),b=simulatePath('live',{...i,imputedA:50000});near(a.end.nominal,b.end.nominal);near(a.end.stocks,b.end.stocks);assert.ok(b.housingPV>a.housingPV);
});
test('fixed staging window does not catch up after liquidity exhausts the parked budget',()=>{
 const i={...defaultInputs(),horizon:6,parkMonths:24,phaseMonths:12,capexScale:30,rentB:0,workingReserve:0},r=simulatePath('staged',i);
 assert.ok(r.stagedMissed>0);near(r.rows[3].stockPhaseDeployed,r.rows[4].stockPhaseDeployed);near(r.rows[4].stockPhaseDeployed,r.rows[6].stockPhaseDeployed);
});
test('common-horizon matrix, case bands and sensitivities re-run and remain finite',()=>{
 const i=defaultInputs(),m=comparisonMatrix(i);assert.equal(m.length,12);assert.deepEqual([...new Set(m.map(x=>x.transferYear))],[2040,2045,2050]);
 assert.deepEqual([...new Set(m.map(x=>x.horizon))],[10,20,30,50]);for(const r of m){assert.ok(ids.includes(r.leader));assert.ok(Number.isFinite(r.gap));}
 for(const r of rangeComparison(i)){assert.ok(r.low<=r.end.nominal&&r.end.nominal<=r.high);assert.equal(r.ranks.length,3);assert.ok(r.ranks.every(x=>x>=1&&x<=7));}
 for(const s of sensitivityRows(i)){assert.ok(ids.includes(s.lowLeader));assert.ok(ids.includes(s.highLeader));}
});
test('81-point distribution is deterministic, sorted and explicitly design points',()=>{
 const i={...defaultInputs(),horizon:10},a=scenarioDistribution('rent',i);assert.equal(a.length,81);assert.deepEqual(a,scenarioDistribution('rent',i));assert.ok(a.every(Number.isFinite));assert.deepEqual(a,[...a].sort((x,y)=>x-y));
});
test('every stress shape/path remains finite over 50 years without mutating inputs',()=>{
 for(const s of SCENARIOS){const i={...defaultInputs(),scenario:s.id,horizon:50},before=JSON.stringify(i);for(const r of runComparison(i))for(const row of r.rows)for(const [k,v] of Object.entries(row))if(typeof v==='number')assert.ok(Number.isFinite(v),`${s.id}/${r.path}/${k}`);assert.equal(JSON.stringify(i),before);}
});
