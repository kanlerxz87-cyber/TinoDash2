(function () {
  const isSubpage = window.location.pathname.includes("/pages/");
  const root = isSubpage ? "../" : "./";
  const current = window.location.pathname.split("/").pop() || "index.html";

  function link(href, label) {
    const file = href.split("/").pop();
    const active = current === file ? " active" : "";
    return `<a class="nav-link${active}" href="${root}${href}">${label}</a>`;
  }

  const sidebarHTML = `
    <div class="brand">TinoDash2</div>
    <div class="brand-sub">Privacy-First Estate &amp; Property Model</div>

    <div class="nav-group">
      <div class="nav-group-title">Overview &amp; Decision</div>
      ${link("index.html", "Executive Summary &amp; What-If")}
      ${link("pages/comparison.html", "Pure &amp; Mixed Paths")}
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Property &amp; Risk</div>
      ${link("pages/properties.html", "Property A &amp; B Profiles")}
      ${link("pages/black-swan.html", "Black Swan &amp; Phased Investing")}
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Execution &amp; Advisors</div>
      ${link("pages/timeline.html", "Process &amp; Deadlines Timeline")}
      ${link("pages/briefing.html", "Attorney &amp; CPA Briefing Sheet")}
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Governance &amp; Sources</div>
      ${link("pages/flagged.html", "Flagged for Review &amp; Sources")}
      ${link("pages/suggestions.html", "Suggestions &amp; Law Tracker")}
    </div>

    <div class="nav-group">
      <button class="btn" style="width:100%" onclick="document.getElementById('glossaryModal').style.display='block'">Open Glossary</button>
    </div>
  `;

  const modalHTML = `
    <div id="glossaryModal" style="display:none; position:fixed; inset:0; background:rgba(15,23,42,0.55); z-index:999; padding:24px; overflow:auto;">
      <div class="card" style="max-width:720px; margin:40px auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <h2 style="margin:0;">Key Terms &amp; Glossary</h2>
          <button class="btn" onclick="document.getElementById('glossaryModal').style.display='none'">Close</button>
        </div>
        <dl style="margin:0; font-size:0.9rem;">
          <dt><strong>Prop 19 (CA)</strong></dt>
          <dd style="margin:0 0 10px 0;">Limits parent-child property tax reassessment exclusion to a principal residence that becomes the child's principal residence within 1 year, capped at Factored Base Year Value + $1,044,586 (2025–2027).</dd>
          <dt><strong>Stepped-Up Basis (IRC § 1014)</strong></dt>
          <dd style="margin:0 0 10px 0;">Resets the income-tax cost basis of inherited property to Fair Market Value at the date of death, eliminating prior unrealized capital gains.</dd>
          <dt><strong>IRC § 121 Exclusion</strong></dt>
          <dd style="margin:0 0 10px 0;">Excludes up to $250,000 ($500,000 MFJ) of capital gain on the sale of a primary residence owned and used for 2 of the last 5 years.</dd>
          <dt><strong>Reinvestment Risk</strong></dt>
          <dd style="margin:0 0 10px 0;">The risk that short-term Treasury yields (3M–2Y) fall before proceeds are phased into equities, or that equities rally while cash is parked in Treasuries.</dd>
          <dt><strong>Mental Health Services Tax (CA Form 540)</strong></dt>
          <dd style="margin:0 0 0 0;">Additional 1% California income tax on taxable income above $1,000,000, bringing the top CA marginal rate (including capital gains) to 13.3%.</dd>
        </dl>
      </div>
    </div>
  `;

  document.addEventListener("DOMContentLoaded", function () {
    const navEl = document.getElementById("sidebar");
    if (navEl) navEl.innerHTML = sidebarHTML;
    document.body.insertAdjacentHTML("beforeend", modalHTML);
  });
})();
