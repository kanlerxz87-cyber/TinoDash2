async function loadModel() {
  const res = await fetch('data/model.json');
  return res.json();
}
function fmt(n) {
  if (n === null || n === undefined || Number.isNaN(n)) return '—';
  const sign = n < 0 ? '-' : '';
  const abs = Math.abs(Math.round(n/10)*10);
  return sign + '$' + abs.toLocaleString('en-US');
}
function fmtPct(x) {
  if (x === null || x === undefined) return '—';
  return (x*100).toFixed(2) + '%';
}
function el(tag, attrs={}, children=[]) {
  const e = document.createElement(tag);
  for (const [k,v] of Object.entries(attrs)) {
    if (k === 'class') e.className = v;
    else if (k === 'html') e.innerHTML = v;
    else e.setAttribute(k,v);
  }
  for (const c of children) e.append(typeof c === 'string' ? document.createTextNode(c) : c);
  return e;
}
function setActiveNav() {
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path) a.classList.add('active');
  });
}
document.addEventListener('DOMContentLoaded', setActiveNav);
