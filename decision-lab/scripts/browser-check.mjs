// Optional: npm install --no-save --package-lock=false playwright-core@1.65.1 @sparticuz/chromium@158.0.0 axe-core@4.14.1
// Run the allowlisted preview first, then: node scripts/browser-check.mjs
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { chromium as playwright } from "playwright-core";
import chromium from "@sparticuz/chromium";
const require = createRequire(import.meta.url),
  root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const artifacts = path.join(root, "artifacts");
fs.mkdirSync(artifacts, { recursive: true });
const base =
  process.env.TEST_BASE_URL ?? "http://127.0.0.1:4173/TinoDash2/decision-lab/";
const routes = [
  "overview",
  "summary",
  "questions",
  "compare",
  "projections",
  "black-swan",
  "taxes",
  "timeline",
  "planning",
  "suggestions",
  "sources",
  "glossary",
  "flagged",
  "privacy",
  "briefing",
];
// The minimal sandbox lacks NSS/NSPR. Reuse the npm package's bundled Lambda
// libraries; no system package repositories or external browser downloads needed.
const { inflate } =
  await import("../node_modules/@sparticuz/chromium/build/lambdafs.js");
const libs = await inflate(
  path.join(root, "node_modules/@sparticuz/chromium/bin/al2023.tar.br"),
);
process.env.LD_LIBRARY_PATH =
  path.join(libs, "lib") + ":" + (process.env.LD_LIBRARY_PATH ?? "");
const args = chromium.args.filter(
  (a) =>
    ![
      "--disable-web-security",
      "--allow-running-insecure-content",
      "--disable-site-isolation-trials",
    ].includes(a),
);
const browser = await playwright.launch({
  executablePath: await chromium.executablePath(),
  args,
  headless: true,
});
const context = await browser.newContext({
  viewport: { width: 1440, height: 1050 },
  deviceScaleFactor: 1,
  acceptDownloads: true,
});
const page = await context.newPage(),
  errors = [],
  badResponses = [],
  externalRequests = [],
  a11y = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
page.on("response", (r) => {
  if (r.status() >= 400) badResponses.push([r.status(), r.url()]);
});
page.on("request", (r) => {
  if (!r.url().startsWith(new URL(base).origin) && !r.url().startsWith("data:"))
    externalRequests.push(r.url());
});
async function open(route) {
  await page.goto(base + "#" + route);
  await page.waitForFunction(() => document.querySelector("#page-title"));
  await page.waitForFunction(
    (r) =>
      document.querySelector("#main")?.innerText.length > 100 &&
      document.title.endsWith("/ Estate Decision Lab") &&
      location.hash === "#" + r,
    route,
  );
}
const axe = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
async function auditAccessibility(label) {
  await page.evaluate(axe);
  const violations = await page.evaluate(async () => {
    const x = await window.axe.run(document, {
      runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa"] },
    });
    return x.violations.map((v) => ({
      id: v.id,
      impact: v.impact,
      nodes: v.nodes.map((n) => ({
        target: n.target,
        summary: n.failureSummary,
      })),
    }));
  });
  if (violations.length) a11y.push({ route: label, violations });
}
try {
  for (const r of routes) {
    await open(r);
    const result = await page.evaluate(() => ({
      title: document.querySelector("h1")?.textContent,
      rows: [...document.querySelectorAll("tbody tr")].length,
      unsourced: [...document.querySelectorAll("tbody tr")].filter(
        (tr) => !tr.querySelector('a[href^="https://"]'),
      ).length,
      bad: /\b(NaN|Infinity|undefined)\b/.test(
        document.querySelector("main").innerText,
      ),
      overflow: document.documentElement.scrollWidth > innerWidth + 1,
    }));
    assert.ok(result.title, r);
    assert.equal(result.unsourced, 0, `${r}: unsourced table row`);
    assert.equal(result.bad, false, `${r}: non-finite/undefined output`);
    assert.equal(result.overflow, false, `${r}: desktop page overflow`);
    await auditAccessibility(r + "-desktop");
    if (["overview", "compare", "black-swan", "briefing"].includes(r))
      await page.screenshot({
        path: path.join(artifacts, `desktop-${r}.png`),
        fullPage: true,
      });
    console.log(
      `Desktop ${r}: ${result.rows} source-linked rows; no overflow or invalid values.`,
    );
  }
  await open("compare");
  await page
    .getByRole("button", { name: "What-if controls", exact: true })
    .click();
  assert.equal(
    await page.locator("#scenario-form").evaluate((f) => f.checkValidity()),
    true,
    "Synthetic defaults violate their HTML form constraints",
  );
  await auditAccessibility("controls-desktop");
  await page.locator('[name="transferYear"]').selectOption("2050");
  await page.locator('[name="horizon"]').selectOption("20");
  await page.locator('[name="rentA"]').fill("10000");
  await page.getByRole("button", { name: "Recalculate all paths" }).click();
  await page.waitForFunction(() => !document.querySelector("dialog").open);
  assert.match(
    await page.locator(".run-strip").innerText(),
    /2050 transfer · 20 years/,
  );
  assert.match(
    await page.locator(".run-strip").innerText(),
    /Household recommendation not made/,
  );
  await page
    .getByRole("button", { name: "What-if controls", exact: true })
    .click();
  await page.getByRole("button", { name: "Reset synthetic defaults" }).click();
  assert.equal(
    await page.locator('[name="transferYear"]').inputValue(),
    "2045",
  );
  await page.getByRole("button", { name: "Close what-if controls" }).click();
  await open("projections");
  await page.locator("#path-select").selectOption("rent-sell");
  const csvEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export scenario CSV" }).click();
  const csv = await csvEvent;
  const csvPath = path.join(artifacts, "synthetic-check.csv");
  await csv.saveAs(csvPath);
  assert.match(fs.readFileSync(csvPath, "utf8"), /synthetic_only/);
  await open("questions");
  await page
    .getByRole("button", { name: "Decision gates", exact: true })
    .click();
  assert.ok((await page.locator(".question-card").count()) > 0);
  assert.equal(
    await page.locator(".question-card .badge:not(.amber)").count(),
    0,
  );
  await open("sources");
  await page.locator("#source-search").fill("Form 540");
  assert.equal(await page.locator("tbody tr").count(), 1);
  assert.match(await page.locator("tbody").innerText(), /Line 62/);
  await open("suggestions");
  await page.locator('[data-decision-id="S02"]').selectOption("Prioritize");
  assert.match(
    await page.locator(".suggestion-card").nth(1).innerText(),
    /no implementation authorized/i,
  );
  const logEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export review log" }).click();
  const log = await logEvent;
  const logPath = path.join(artifacts, "review-check.json");
  await log.saveAs(logPath);
  const review = JSON.parse(fs.readFileSync(logPath, "utf8"));
  assert.equal(review.householdDecision, null);
  assert.equal(review.items.find((x) => x.id === "S02").status, "Prioritize");
  assert.ok(review.items.every((x) => !x.implemented));
  assert.deepEqual((await context.storageState()).cookies, []);
  assert.deepEqual((await context.storageState()).origins, []);
  await page.reload();
  await page.waitForSelector('[data-decision-id="S02"]');
  assert.equal(
    await page.locator('[data-decision-id="S02"]').inputValue(),
    "Not reviewed",
  );
  await open("briefing");
  await page.pdf({
    path: path.join(artifacts, "Attorney-CPA-Briefing-Sheet.pdf"),
    preferCSSPageSize: true,
    printBackground: true,
  });
  const pdf = fs.readFileSync(
    path.join(artifacts, "Attorney-CPA-Briefing-Sheet.pdf"),
  );
  const pages = (pdf.toString("latin1").match(/\/Type\s*\/Page\b/g) ?? [])
    .length;
  assert.equal(
    pages,
    1,
    "Professional briefing must be one printed Letter page",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForFunction(() => document.querySelector("#sidebar").inert);
  for (const r of routes) {
    await open(r);
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth > innerWidth + 1,
      ),
      false,
      `${r}: mobile page overflow`,
    );
    await auditAccessibility(r + "-mobile");
  }
  await open("overview");
  await page.screenshot({
    path: path.join(artifacts, "mobile-overview.png"),
    fullPage: true,
  });
  await page.getByRole("button", { name: "Open navigation" }).click();
  assert.equal(
    await page.locator("#sidebar").evaluate((el) => el.inert),
    false,
  );
  assert.equal(
    await page.locator(".workspace").evaluate((el) => el.inert),
    true,
  );
  await auditAccessibility("mobile-menu");
  await page.getByRole("link", { name: "Compare paths", exact: true }).click();
  await page.waitForFunction(
    () => !document.body.classList.contains("menu-open"),
  );
  await page
    .getByRole("button", { name: "What-if controls", exact: true })
    .click();
  assert.equal(
    await page
      .locator("dialog")
      .evaluate((d) => d.scrollWidth > d.clientWidth + 1),
    false,
    "Mobile control overflow",
  );
  await auditAccessibility("controls-mobile");
  await page.screenshot({ path: path.join(artifacts, "mobile-controls.png") });
  await page.keyboard.press("Escape");
  assert.equal(await page.locator("dialog").evaluate((d) => d.open), false);
  assert.deepEqual(errors, [], "Browser console/runtime errors");
  assert.deepEqual(badResponses, [], "Missing runtime resources");
  assert.deepEqual(externalRequests, [], "Unexpected browser network requests");
  fs.writeFileSync(
    path.join(artifacts, "accessibility-report.json"),
    JSON.stringify(a11y, null, 2),
  );
  console.log(
    `Browser smoke checks passed: ${routes.length} desktop + mobile routes; controls, filters, downloads, tab-only reset, source rows; ${pages}-page briefing PDF; no external requests/runtime errors. Accessibility findings: ${a11y.reduce((s, r) => s + r.violations.length, 0)} route/rule pairs (see ignored artifact report).`,
  );
  if (process.env.STRICT_A11Y === "1")
    assert.deepEqual(a11y, [], "Accessibility findings require repair");
} finally {
  await browser.close();
}
