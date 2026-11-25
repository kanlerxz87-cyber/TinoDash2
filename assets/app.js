/* TinoDash2 UI — what-if controls, charts, suggestions voting */
(function(){
"use strict";
function $(id){ return document.getElementById(id); }
function fmt(n){ return "$" + Math.round(n).toLocaleString("en-US"); }
function readParams(){
  var p = JSON.parse(JSON.stringify(window.TinoModel.DEFAULTS));
  function num(id, key, scale){ var el=$(id); if(el && el.value!==""){ p[key]=parseFloat(el.value)*(scale||1); } }
  num("in-inheritYear","inheritYear"); num("in-horizon","horizonYears");
  num("in-apprec","homeApprec_base",0.01); num("in-stock","stockRet_base",0.01);
  num("in-rentA","propA_rent_mo_base"); num("in-imputed","imputedRentA_mo");
  num("in-insA","insuranceA"); num("in-sellPct","sellCostPct",0.01);
  num("in-phase","phaseMonths");
  return p;
}
function drawBars(canvas, dist){
  if(!canvas) return;
  var ctx = canvas.getContext("2d");
  var W = canvas.width = canvas.offsetWidth*2, H = canvas.height = 520;
  ctx.scale(2,2); var w = canvas.offsetWidth, h = 260;
  ctx.clearRect(0,0,w,h);
  var keys = Object.keys(dist);
  var maxW = 0;
  keys.forEach(function(k){ dist[k].bins.forEach(function(b){ if(b.weight>maxW) maxW=b.weight; }); });
  var bw = w/keys.length;
  ctx.font = "11px system-ui"; ctx.fillStyle = "#9fb0c0";
  keys.forEach(function(k,ki){
    var x0 = ki*bw;
    dist[k].bins.forEach(function(b,i){
      var bh = (b.weight/maxW)*(h-50);
      ctx.fillStyle = i===5? "#4cc2ff" : "#2e5a7a";
      ctx.fillRect(x0+4+i*((bw-8)/11), h-30-bh, (bw-8)/11-2, bh);
    });
    ctx.fillStyle="#e8eef4"; ctx.textAlign="center";
    ctx.fillText(k, x0+bw/2, h-12);
    ctx.fillText(fmt(dist[k].base), x0+bw/2, 16);
  });
}
function drawLine(canvas, rows, label){
  if(!canvas || !rows) return;
  var ctx = canvas.getContext("2d");
  var w = canvas.offsetWidth, h = 260;
  canvas.width = w*2; canvas.height = h*2; ctx.scale(2,2);
  ctx.clearRect(0,0,w,h);
  var vals = rows.map(function(r){ return r.cash; });
  var min = Math.min.apply(null, vals), max = Math.max.apply(null, vals);
  if(max===min) max=min+1;
  ctx.strokeStyle="#4cc2ff"; ctx.lineWidth=2; ctx.beginPath();
  rows.forEach(function(r,i){
    var x = 30 + i*(w-50)/Math.max(1,rows.length-1);
    var y = 20 + (1-(r.cash-min)/(max-min))*(h-50);
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();
  ctx.fillStyle="#9fb0c0"; ctx.font="11px system-ui";
  ctx.fillText(label+"  min "+fmt(min)+"  max "+fmt(max), 30, h-8);
}
function render(){
  var p = readParams();
  var all = window.TinoModel.runAll(p);
  var dist = window.TinoModel.distribution(p);
  var bs = window.TinoModel.blackSwan(p);
  // summary table
  var tb = $("pathTableBody");
  if(tb){
    tb.innerHTML = "";
    Object.keys(all).forEach(function(k){
      var tr = document.createElement("tr");
      tr.innerHTML = "<td>"+k+"</td><td class='num'>"+fmt(all[k].low.terminal)+"</td><td class='num'><strong>"+fmt(all[k].base.terminal)+"</strong></td><td class='num'>"+fmt(all[k].high.terminal)+"</td><td class='num'>"+fmt(all[k].base.npv)+"</td><td class='num'>"+fmt(all[k].base.saleTax)+"</td>";
      tb.appendChild(tr);
    });
  }
  var bsEl = $("blackSwanOut");
  if(bsEl){
    bsEl.innerHTML = "<p>Net proceeds (before income tax, simplified): <strong>"+fmt(bs.proceeds)+"</strong></p>"+
    "<table><tr><th>Scenario</th><th class='num'>Lump-sum</th><th class='num'>Phased (Treasury 30 mo)</th><th class='num'>Phased advantage</th></tr>"+
    "<tr><td>2008-style −57% crash in year 1</td><td class='num'>"+fmt(bs.lump2008)+"</td><td class='num'>"+fmt(bs.phased2008)+"</td><td class='num'>"+fmt(bs.phased2008-bs.lump2008)+"</td></tr>"+
    "<tr><td>1929-style −89% crash in year 1</td><td class='num'>"+fmt(bs.lump1929)+"</td><td class='num'>"+fmt(bs.phased1929)+"</td><td class='num'>"+fmt(bs.phased1929-bs.lump1929)+"</td></tr>"+
    "<tr><td>No crash (20-yr)</td><td class='num'>"+fmt(bs.lumpNoCrash)+"</td><td class='num'>"+fmt(bs.phasedNoCrash)+"</td><td class='num'>"+fmt(bs.phasedNoCrash-bs.lumpNoCrash)+"</td></tr></table>"+
    "<p class='mut small'>Reinvestment risk: phased path lags in bull markets (Treasury yield &lt; stock return). See black-swan.html for full drawdown history. Simplified — excludes income tax on sale and B-property cash flows.</p>";
  }
  drawBars($("distChart"), dist);
  var base = all['live'] ? all['live'].base.rows : null;
  drawLine($("cashChart"), base, "Live path cumulative cash (base)");
  var rankEl = $("rankOut");
  if(rankEl){
    var ranked = Object.keys(all).map(function(k){ return {k:k, v:all[k].base.terminal}; }).sort(function(a,b){return b.v-a.v;});
    rankEl.innerHTML = ranked.map(function(r,i){ return (i+1)+". "+r.k+" — "+fmt(r.v); }).join("<br>");
  }
  var meta = $("modelMeta");
  if(meta){ meta.textContent = "Inheritance "+p.inheritYear+" · horizon "+p.horizonYears+" yrs · appreciation "+(p.homeApprec_base*100).toFixed(0)+"% · stocks "+(p.stockRet_base*100).toFixed(0)+"% · Treasury "+(p.treasuryRet*100).toFixed(1)+"%"; }
}
document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll("[data-bind]").forEach(function(el){
    el.addEventListener("input", render);
  });
  render();
  // suggestions voting (localStorage, no tracking)
  document.querySelectorAll("[data-vote]").forEach(function(btn){
    var key = "tino-sug-"+btn.getAttribute("data-vote");
    if(localStorage.getItem(key)) btn.textContent = "✓ Chosen";
    btn.addEventListener("click", function(){
      localStorage.setItem(key, "1");
      document.querySelectorAll("[data-vote]").forEach(function(b){ if(b!==btn) b.textContent="Choose this"; });
      btn.textContent = "✓ Chosen";
    });
  });
});
})();
