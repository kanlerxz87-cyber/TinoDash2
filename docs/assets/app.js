/* TinoDash2 — shared app: nav injection, formatting, simulation, charts, what-if engine.
   All monetary display rounded to nearest $10 (privacy-by-rounding). No external requests. */
'use strict';

const PAGE = (document.body.dataset.page || '').trim();

const NAV = [
  { group: 'Overview', items: [
    ['index.html','Executive Dashboard'],
    ['brief.html','Attorney & CPA Brief (print)'],
  ]},
  { group: 'Properties', items: [
    ['property-a.html','Property A — Cupertino'],
    ['property-b.html','Property B — San Francisco'],
  ]},
  { group: 'Analysis', items: [
    ['compare.html','Path Comparison Matrix'],
    ['mixed.html','Mixed Paths & Staging'],
    ['black-swan.html','Black Swan Stress Lab'],
    ['projections.html','50-Year Projections & What-If'],
  ]},
  { group: 'Taxes', items: [
    ['taxes.html','Three Taxes, Separated'],
  ]},
  { group: 'Process & Decisions', items: [
    ['process.html','Step-by-Step & Deadlines'],
    ['questions.html','Open Questions & Missing Info'],
    ['suggestions.html','Suggestions Board (review)'],
    ['policy.html','Investment Policy & Pre-commitment'],
    ['journal.html','Decision Journal (dated)'],
  ]},
  { group: 'Reference', items: [
    ['glossary.html','Glossary'],
    ['sources.html','Sources & Verification Log'],
    ['flagged.html','Flagged for Review'],
  ]},
];

function injectNav(){
  const mount = document.getElementById('nav-mount');
  if(!mount) return;
  const nav = NAV.map(g=>`
    <div class="nav-group">
      <div class="nav-group-label">${g.group}</div>
      ${g.items.map(([href,label])=>`<a href="${href}"${PAGE===href?' aria-current="page"':''}>${label}</a>`).join('')}
    </div>`).join('');
  mount.innerHTML = `<nav class="sidebar no-print" aria-label="Site sections">
    <div class="brand">
      <div class="mark">A</div>
      <div><h1>Cupertino Inheritance<br>Decision Desk</h1><small>Private · Anonymized · 2040–2050</small></div>
    </div>
    ${nav}
    <div class="nav-foot">
      All figures rounded to the nearest $10. No names, addresses or parcel numbers appear anywhere.
      Educational decision-support model — not legal, tax, or investment advice. Last verified pass: 2026-11-25.
    </div>
  </nav>`;
}

function injectFooter(){
  document.querySelectorAll('.footer-inject').forEach(el=>{
    el.innerHTML = `<div class="footer">
      <strong>TinoDash2 · Cupertino Inheritance Decision Desk</strong> — private, anonymized decision-support model prepared 2026-11-25.
      Figures are rounded to the nearest $10 and are planning estimates, not quotes. Enacted law as of 2026-11-25; proposals are labeled and are not law.
      Not legal, tax, or investment advice — confirm everything with the attorney and CPA listed on the <a href="brief.html">Briefing Sheet</a>.
      &nbsp;|&nbsp; <a href="flagged.html">Flagged for Review</a> &nbsp;|&nbsp; <a href="sources.html">Sources</a> &nbsp;|&nbsp; <a href="journal.html">Decision journal</a>
    </div>`;
  });
}

/* ---------- formatting ---------- */
const r10 = x => Math.round(x/10)*10;
const fmt10 = x => { if(!isFinite(x)) return '—'; return '$' + r10(x).toLocaleString('en-US'); };
const pct = (x,d=2) => (x*100).toFixed(d) + '%';
const el = id => document.getElementById(id);

/* ---------- seeded PRNG + lognormal Monte Carlo ---------- */
function mulberry32(seed){
  let a = seed >>> 0;
  return function(){
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function normalDraw(rand){
  // Box–Muller
  let u = 0, v = 0;
  while(u === 0) u = rand();
  while(v === 0) v = rand();
  return Math.sqrt(-2*Math.log(u)) * Math.cos(2*Math.PI*v);
}
/* annual lognormal params from target CAGR and volatility */
function simulateFan({start=5079000, years=25, cagr=0.07, sigma=0.16, n=4000, seed=20261125}){
  const rand = mulberry32(seed);
  const drift = Math.log(1+cagr) - 0.5*sigma*sigma;
  const paths = [];
  for(let i=0;i<n;i++){
    const p = [start];
    let v = start;
    for(let y=0;y<years;y++){ v = v * Math.exp(drift + sigma*normalDraw(rand)); p.push(v); }
    paths.push(p);
  }
  const q = (arr,f) => { const s=[...arr].sort((a,b)=>a-b); return s[Math.min(arr.length-1, Math.max(0, Math.floor(f*s.length)))]; };
  const bands = [];
  for(let y=0;y<=years;y++){
    const col = paths.map(p=>p[y]);
    bands.push({year:y, p10:q(col,0.10), p25:q(col,0.25), p50:q(col,0.50), p75:q(col,0.75), p90:q(col,0.90)});
  }
  const terminal = paths.map(p=>p[years]).sort((a,b)=>a-b);
  return { bands, terminal };
}
function fanChart(id, bands, opts={}){
  const svg = el(id); if(!svg) return;
  const W=860,H=300, P={l:64,r:14,t:14,b:30};
  const iw=W-P.l-P.r, ih=H-P.t-P.b;
  const n=bands.length;
  const x = i => P.l + (i/(n-1))*iw;
  const maxV = Math.max(...bands.map(b=>b.p90))*1.05;
  const y = v => P.t + ih - (v/maxV)*ih;
  const area = (top,bot) => `M ${x(0)} ${y(bands[0][top])} ` + bands.map((b,i)=>`L ${x(i)} ${y(b[top])}`).join(' ') + ' ' + [...bands].reverse().map((b,j)=>`L ${x(n-1-j)} ${y(b[bot])}`).join(' ') + ' Z';
  const line = key => `M ` + bands.map((b,i)=>`${i?'L':''} ${x(i)} ${y(b[key])}`).join(' ');
  const yTicks = [0,0.25,0.5,0.75,1].map(f=>{
    const v=maxV*f, yy=y(v);
    return `<line x1="${P.l}" y1="${yy}" x2="${W-P.r}" y2="${yy}" stroke="#e3ded2"/><text x="${P.l-8}" y="${yy+4}" text-anchor="end" font-size="10" fill="#5b6a7a">$${(v/1e6).toFixed(0)}M</text>`;
  }).join('');
  const xTicks = [0,5,10,15,20,25].map(yr=>{
    if(yr>=n) return '';
    return `<text x="${x(yr)}" y="${H-10}" text-anchor="middle" font-size="10" fill="#5b6a7a">+${yr}y</text>`;
  }).join('');
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
  svg.innerHTML = `
    <path d="${area('p90','p10')}" fill="#b8860b" opacity="0.16"/>
    <path d="${area('p75','p25')}" fill="#b8860b" opacity="0.22"/>
    <path d="${line('p50')}" fill="none" stroke="#0f2a43" stroke-width="2.5"/>
    <path d="${line('p10')}" fill="none" stroke="#b02a2a" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="${line('p90')}" fill="none" stroke="#1e7d46" stroke-width="1.4" stroke-dasharray="5 4"/>
    ${yTicks}${xTicks}`;
}
function histogram(id, values){
  const svg = el(id); if(!svg) return;
  const W=860,H=260, P={l:56,r:10,t:14,b:34};
  const iw=W-P.l-P.r, ih=H-P.t-P.b, bins=34;
  const min=values[0], max=values[values.length-1];
  const width=(max-min)/bins || 1;
  const counts=new Array(bins).fill(0);
  values.forEach(v=>{ const i=Math.min(bins-1, Math.floor((v-min)/width)); counts[i]++; });
  const maxC=Math.max(...counts);
  const bw=iw/bins;
  const bars=counts.map((c,i)=>{
    const h=(c/maxC)*ih, x=P.l+i*bw, y=P.t+ih-h;
    return `<rect x="${x+0.5}" y="${y}" width="${Math.max(1,bw-1)}" height="${h}" fill="${i<bins*0.25?'#d98f8f':(i<bins*0.75?'#173a5e':'#7fc79b')}"/>`;
  }).join('');
  const ticks=[min,(min+max)/2,max].map((v,i)=>`<text x="${P.l+(i===0?0:(i===1?iw/2:iw))}" y="${H-12}" text-anchor="${i===0?'start':(i===1?'middle':'end')}" font-size="10" fill="#5b6a7a">$${(v/1e6).toFixed(1)}M</text>`).join('');
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
  svg.innerHTML = `${bars}<line x1="${P.l}" y1="${P.t+ih}" x2="${W-P.r}" y2="${P.t+ih}" stroke="#5b6a7a"/>${ticks}`;
}

/* ---------- shared inheritance model (2026-11-25 baseline, $10-rounded display) ---------- */
const MODEL = {
  fmvToday: 3100000,             // Property A estimated value Nov 2026 (user-provided, rounded)
  fmvSf: 1800000,                // Property B estimated value Nov 2026
  assessed2026: 550540,
  taxRateA: 0.0134,              // implied from ledger (1.32–1.36%); TRA lookup pending (Flagged #3)
  commission: 0.05,              // 5.0% sell-side cost assumption (range 4.5–6%)
  sczTransfer: 0.0011,           // Santa Clara County $1.10 per $1,000
  miscSell: 15000,               // escrow/title/repairs allowance, rounded
  tbill: 0.043,                  // ~Nov 2026 3-month T-bill
  infl: 0.024,
  yearsToInherit: 14,            // 2040
};
function fmvAt(growth, years){ return MODEL.fmvToday*Math.pow(1+growth, years); }
function assessedAt(years){ return MODEL.assessed2026*Math.pow(1.02, years); }
function netSaleProceeds(fmv){ return fmv - fmv*MODEL.commission - fmv*MODEL.sczTransfer - MODEL.miscSell; }
function prop19Allowance(years){
  // $1,044,586 in force Feb 2025–Feb 2027 (BOE 2-year FHFA CA HPI cycle, ~2%/yr proxy between cycles)
  return 1044586*Math.pow(1.02, Math.max(0, years - 1));
}

/* ---------- projections page wiring ---------- */
function renderProjections(){
  const gEl=el('wi-growth'); if(!gEl) return;
  const eqEl=el('wi-equity'), infEl=el('wi-infl'), crashEl=el('wi-crash'), stageEl=el('wi-stage');
  const horizonEl=el('wi-horizon');
  function read(){
    return {
      growth:+gEl.value/100, equity:+eqEl.value/100, infl:+infEl.value/100,
      crash:+crashEl.value/100, stage:+stageEl.value, horizon:+horizonEl.value
    };
  }
  function update(){
    const v=read();
    el('wi-growth-out').textContent = pct(v.growth,1);
    el('wi-equity-out').textContent = pct(v.equity,1);
    el('wi-infl-out').textContent = pct(v.infl,1);
    el('wi-crash-out').textContent = pct(v.crash,0);
    el('wi-stage-out').textContent = v.stage + ' months';
    el('wi-horizon-out').textContent = '+' + v.horizon + ' years';
    const yrs = v.horizon;
    const fmv = fmvAt(v.growth, MODEL.yearsToInherit);
    const net = netSaleProceeds(fmv);
    const lumpNow = net*(1+v.crash);               // lump sum suffers full crash entry
    const phaseFracInvested = Math.min(1, v.stage/36); // linear ladder over staging window
    const stagedTbills = net*(Math.pow(1+MODEL.tbill, v.stage/12)*(1-0.35*(1-phaseFracInvested)) + 0.0); // approx: weight grows toward equities
    const stagedFinal = net*(Math.pow(1+MODEL.tbill, v.stage/12)*(1-phaseFracInvested) + phaseFracInvested*Math.pow(1+v.equity, v.stage/12));
    const lumpFinal = lumpNow*Math.pow(1+v.equity, yrs);
    const stagedEnd = stagedFinal*Math.pow(1+v.equity, Math.max(0, yrs - v.stage/12));
    const rentNOI = 10000*Math.pow(1.03, MODEL.yearsToInherit)*12 - (fmv*MODEL.taxRateA) - (fmv*0.005) - (10000*Math.pow(1.03,MODEL.yearsToInherit)*12*0.14) - (2600*Math.pow(1.03,MODEL.yearsToInherit));
    const liveTax = (assessedAt(MODEL.yearsToInherit) + prop19Allowance(MODEL.yearsToInherit))*MODEL.taxRateA;
    const reassessTax = fmv*MODEL.taxRateA;
    el('out-fmv').textContent = fmt10(fmv);
    el('out-net').textContent = fmt10(net);
    el('out-lump').textContent = fmt10(lumpFinal);
    el('out-staged').textContent = fmt10(stagedEnd);
    el('out-staged-pre').textContent = fmt10(stagedFinal);
    el('out-noi').textContent = fmt10(rentNOI);
    el('out-livetax').textContent = fmt10(liveTax);
    el('out-reasstax').textContent = fmt10(reassessTax);
    el('out-verdict').textContent = lumpFinal >= stagedEnd
      ? 'Lump sum wins in calm markets; staged wins when the crash slider is moved negative.'
      : 'Staged entry wins under the selected crash / horizon assumptions.';
    // projection table rows every 5 years
    const tbody = el('proj-rows');
    if(tbody){
      let rows='';
      for(let y=5;y<=50;y+=5){
        const tv = fmvAt(v.growth, y);
        rows += `<tr><td>+${y}y (${2026+y})</td><td class="num">${fmt10(tv)}</td><td class="num">${fmt10(assessedAt(y))}</td><td class="num">${fmt10((assessedAt(y))*MODEL.taxRateA)}</td><td class="num">${fmt10(netSaleProceeds(tv)*Math.pow(1+v.equity, Math.max(0,y-MODEL.yearsToInherit)))}</td></tr>`;
      }
      tbody.innerHTML = rows;
    }
  }
  [gEl,eqEl,infEl,crashEl,stageEl,horizonEl].forEach(c=>c.addEventListener('input', update));
  update();

  const {bands, terminal} = simulateFan({start: netSaleProceeds(fmvAt(0.04, MODEL.yearsToInherit)), years: 25, cagr: 0.07, sigma: 0.16});
  fanChart('fanChart', bands);
  histogram('distChart', terminal);
  const p50 = bands[bands.length-1].p50, p10 = bands[bands.length-1].p10, p90 = bands[bands.length-1].p90;
  const set=(id,val)=>{ const e=el(id); if(e) e.textContent = fmt10(val); };
  set('mc-p10', p10); set('mc-p50', p50); set('mc-p90', p90);
}

/* ---------- compare page horizon switcher ---------- */
function renderCompare(){
  const btns = document.querySelectorAll('[data-horizon]');
  if(!btns.length) return;
  const FMV_2040 = 5368200, NET_2040 = 5078880;
  const data = {
    0:  { live: 0, sell: NET_2040, rent: 0, label:'at inheritance (2040)' },
    10: { live: (120000-27000-1500*1.34-1500-15000)*10*1.35 + FMV_2040*0.0, sell: NET_2040*Math.pow(1.07,10), rent: 53390*10*1.35, label:'10 years later (2050)' },
    25: { live: (120000-27000-1500*1.34-1500-15000)*25*2.0,  sell: NET_2040*Math.pow(1.07,25), rent: 53390*25*2.2, label:'25 years later (2065)' },
    50: { live: (120000-27000-1500*1.34-1500-15000)*50*3.1,  sell: NET_2040*Math.pow(1.07,50), rent: 53390*50*3.6, label:'50 years later (2090)' },
  };
  function apply(h){
    btns.forEach(b=>b.classList.toggle('ghost', b.dataset.horizon!==String(h)));
    const d = data[h];
    el('cmp-note').textContent = 'Showing estimated cumulative wealth effect ' + d.label + ' (baseline 4% property growth, 7% equity, 2.4% inflation, figures rounded to $10).';
    el('cmp-live').textContent = fmt10(d.live);
    el('cmp-sell').textContent = fmt10(d.sell);
    el('cmp-rent').textContent = fmt10(d.rent);
  }
  btns.forEach(b=>b.addEventListener('click', ()=>apply(+b.dataset.horizon)));
  apply(25);
}

/* ---------- suggestions page: localStorage review state ---------- */
function renderSuggestions(){
  const boxes = document.querySelectorAll('.sug-check');
  if(!boxes.length) return;
  const KEY='tinodash2-sug-v1';
  let state={};
  try{ state=JSON.parse(localStorage.getItem(KEY)||'{}'); }catch(e){ state={}; }
  const counter = el('sug-count');
  function refresh(){
    const done=[...boxes].filter(b=>b.checked).length;
    if(counter) counter.textContent = `${done} of ${boxes.length} marked “implement”`;
  }
  boxes.forEach(b=>{
    b.checked = !!state[b.id];
    b.addEventListener('change', ()=>{ state[b.id]=b.checked; try{localStorage.setItem(KEY, JSON.stringify(state));}catch(e){} refresh(); });
  });
  refresh();
}

/* ---------- print buttons ---------- */
function wirePrint(){ document.querySelectorAll('[data-print]').forEach(b=>b.addEventListener('click',()=>window.print())); }

/* ---------- boot ---------- */
document.addEventListener('DOMContentLoaded', ()=>{
  injectNav(); injectFooter(); wirePrint(); renderProjections(); renderCompare(); renderSuggestions();
});
