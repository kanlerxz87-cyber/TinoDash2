'use strict';
const current = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.sidebar nav a').forEach(a => { if (a.getAttribute('href') === current) { a.classList.add('active'); a.setAttribute('aria-current','page'); } });
const button = document.getElementById('run');
if (button) {
  const returns = {depression:[-.25,-.35,-.20,.15,.10], recession:[-.35,.25,.15], steady:[]};
  function calculate() {
    const scenario = document.getElementById('scenario').value;
    const delay = Number(document.getElementById('delay').value);
    const yieldInput = document.getElementById('yield');
    const inflationInput = document.getElementById('inflation');
    if (!yieldInput.reportValidity() || !inflationInput.reportValidity()) return;
    const yieldRate = Number(yieldInput.value)/100, inflation = Number(inflationInput.value)/100;
    const years = Number(document.getElementById('horizon').value);
    if (!Number.isFinite(yieldRate) || !Number.isFinite(inflation) || yieldInput.value === '' || inflationInput.value === '') return;
    let immediate=100, stagedEquity=0, cash=100; const points=[[0,100,100]];
    for(let month=0;month<years*12;month++) {
      const y=Math.floor(month/12), annual=returns[scenario][y] ?? .06;
      const stockMonthly=(1+annual)**(1/12)-1, billMonthly=(1+yieldRate)**(1/12)-1;
      if(month>=delay && month<delay+36) {const transfer=cash/(delay+36-month); cash-=transfer; stagedEquity+=transfer;}
      immediate*=1+stockMonthly; stagedEquity*=1+stockMonthly; cash*=1+billMonthly;
      if((month+1)%12===0) {const year=(month+1)/12, deflator=(1+inflation)**year; points.push([year,immediate/deflator,(stagedEquity+cash)/deflator]);}
    }
    const fmt=n=>n.toLocaleString('en-US',{maximumFractionDigits:1}); const last=points.at(-1);
    document.getElementById('summary').innerHTML=`<div>IMMEDIATE STOCKS<strong>${fmt(last[1])}</strong>real index points</div><div>STAGED ENTRY<strong>${fmt(last[2])}</strong>real index points</div>`;
    const W=700,H=260,L=50,R=15,T=15,B=32,max=Math.max(...points.flatMap(p=>p.slice(1)))*1.08;
    const x=n=>L+n/years*(W-L-R), y=n=>H-B-n/max*(H-T-B);
    const lines=[1,2].map((j)=>`<polyline fill="none" stroke="${j===1?'#2f6452':'#c08a56'}" stroke-width="3" points="${points.map(p=>`${x(p[0])},${y(p[j])}`).join(' ')}"/>`).join('');
    document.getElementById('chart').innerHTML=`<svg viewBox="0 0 ${W} ${H}" aria-hidden="true"><line x1="${L}" y1="${H-B}" x2="${W-R}" y2="${H-B}" stroke="#cddacf"/><line x1="${L}" y1="${T}" x2="${L}" y2="${H-B}" stroke="#cddacf"/><text x="5" y="${T+8}" fill="#82988a" font-size="10">${fmt(max)}</text><text x="25" y="${H-B}" fill="#82988a" font-size="10">0</text><text x="${L}" y="${H-8}" fill="#82988a" font-size="10">TRANSFER</text><text x="${W-R-52}" y="${H-8}" fill="#82988a" font-size="10">YEAR ${years}</text>${lines}</svg>`;
    const selected=[...new Set([1,2,3,5,10,20,50,years])].filter(n=>n<=years).sort((a,b)=>a-b);
    document.getElementById('projection').innerHTML=`<div class="table-wrap"><table><thead><tr><th>Year</th><th>Immediate</th><th>Staged</th><th>Context</th></tr></thead><tbody>${selected.map(n=>`<tr><td>${n}</td><td>${fmt(points[n][1])}</td><td>${fmt(points[n][2])}</td><td><a href="https://www.treasurydirect.gov/marketable-securities/reinvesting-a-marketable-security/">TreasuryDirect ↗</a></td></tr>`).join('')}</tbody></table></div>`;
  }
  button.addEventListener('click',calculate); calculate();
}
