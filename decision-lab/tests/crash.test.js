import test from "node:test";
import assert from "node:assert/strict";
import { defaultInputs } from "../model.js";
import { simulateCrash, crashComparison } from "../crash.js";
import { SCENARIOS, equityMonthlyReturn, treasuryYieldAt } from "../economy.js";
const near = (a, b, tol = 1e-5) =>
  assert.ok(Math.abs(a - b) <= tol, `${a} ≠ ${b}`);

test("entry strategies start from identical normalized proceeds", () => {
  const runs = crashComparison(defaultInputs());
  for (const r of runs) {
    near(r.rows[0].value, 1000000);
    assert.equal(r.rows.length, 361);
    assert.ok(r.end.afterTax <= r.end.value);
  }
  near(runs[0].rows[0].stock, 700000);
  near(runs[1].rows[0].stock, 0);
  near(runs[2].rows[0].stock, 0);
});
test("park and phase dates honored for both periods and lengths", () => {
  for (const parkMonths of [24, 36])
    for (const phaseMonths of [12, 24]) {
      const r = simulateCrash({ months: 120, parkMonths, phaseMonths });
      near(r.rows[parkMonths].stock, 0);
      assert.ok(r.rows[parkMonths + 1].stock > 0);
      near(r.phaseDeployed, r.phaseBudget);
      assert.ok(r.rows.every((x) => x.treasury >= 0 && x.stock >= 0));
    }
});
test("pre-phase ladder holds no maturity beyond phase start", () => {
  const r = simulateCrash({ months: 23, parkMonths: 24 });
  assert.ok(r.finalHoldings.every((h) => h.maturity <= 24));
  assert.equal(r.phaseBudget, 0);
  const x = simulateCrash({ months: 35, parkMonths: 36 });
  assert.ok(x.finalHoldings.every((h) => h.maturity <= 36));
});
test("cash reserved for phasing is not an early bond sale or continued catch-up", () => {
  const i = defaultInputs(),
    r = simulateCrash({
      months: 25,
      parkMonths: 24,
      phaseMonths: 12,
      inputs: i,
    });
  assert.ok(r.rows[25].cash > 0);
  assert.ok(r.phaseDeployed < r.phaseBudget);
  const a = simulateCrash({ months: 60, parkMonths: 24, phaseMonths: 12 }),
    b = simulateCrash({ months: 120, parkMonths: 24, phaseMonths: 12 });
  near(a.phaseDeployed, b.phaseDeployed);
});
test("chosen 1929/2008 severity shapes are exact assumptions, not labeled replays", () => {
  for (const [scenario, n, target] of [
    ["depression", 34, 0.11],
    ["gfc", 18, 0.45],
  ]) {
    let v = 1;
    for (let m = 0; m < n; m++)
      v *= 1 + equityMonthlyReturn(m, { ...defaultInputs(), scenario });
    near(v, target);
  }
  assert.ok(
    SCENARIOS.every((s) =>
      /synthetic|hypothetical|forecast|chosen|explicit|staging/i.test(s.detail),
    ),
  );
});
test("early depression shape reduces entry drawdown under staging, with no guarantee claim", () => {
  const r = crashComparison({ ...defaultInputs(), scenario: "depression" });
  assert.ok(r[1].maxDrawdown > r[0].maxDrawdown);
  assert.ok(r[2].maxDrawdown > r[0].maxDrawdown);
});
test("rapid rebound counterexample publishes a cost of waiting", () => {
  const r = crashComparison({ ...defaultInputs(), scenario: "rebound" });
  assert.ok(r[0].end.afterTax > r[1].end.afterTax);
  assert.ok(r[0].end.afterTax > r[2].end.afterTax);
});
test("late crash still causes a material staged drawdown", () => {
  const r = crashComparison({ ...defaultInputs(), scenario: "late" });
  assert.ok(r[1].maxDrawdown < -0.2);
  assert.ok(r[2].maxDrawdown < -0.2);
});
test("reinvestment yields fall in entry credit stress; all-Treasury case shows that risk", () => {
  const i = { ...defaultInputs(), stockTarget: 0, scenario: "gfc" };
  assert.ok(treasuryYieldAt(24, i) < treasuryYieldAt(0, i));
  const a = simulateCrash({ inputs: i, months: 120, parkMonths: 0 }),
    b = simulateCrash({
      inputs: { ...i, scenario: "baseline" },
      months: 120,
      parkMonths: 0,
    });
  assert.ok(a.end.afterTax < b.end.afterTax);
});
test("all monthly stress cases remain finite, with correct after-tax/real and drawdown bounds", () => {
  for (const s of SCENARIOS)
    for (const r of crashComparison(
      { ...defaultInputs(), scenario: s.id },
      600,
    )) {
      assert.ok(r.maxDrawdown <= 0 && r.maxDrawdown >= -1);
      assert.ok(r.exitTax >= 0);
      for (const row of r.rows)
        for (const [k, v] of Object.entries(row))
          if (typeof v === "number")
            assert.ok(Number.isFinite(v), `${s.id}/${k}`);
      assert.ok(r.end.afterTax <= r.end.value);
      assert.ok(r.end.realAfterTax > 0);
    }
});
test("invalid requests cannot create hidden fallback scenarios", () => {
  for (const opts of [
    { initial: 0 },
    { initial: Infinity },
    { months: 601 },
    { months: 1.1 },
    { parkMonths: 30 },
    { phaseMonths: 18 },
    { inputs: { ...defaultInputs(), scenario: "unknown" } },
  ])
    assert.throws(() => simulateCrash(opts));
});
