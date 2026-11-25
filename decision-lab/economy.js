/** Deterministic, synthetic economic shapes. NOT historical return data. */
export const SCENARIOS = [
  {
    id: "baseline",
    name: "Uneven baseline",
    detail:
      "Repeating expansion, cooling, drawdown and recovery years. Not a forecast.",
  },
  {
    id: "depression",
    name: "1929-severity entry shock",
    detail:
      "Chosen 34-month decline of 89%, then a synthetic recovery to the starting index by month 300. Price-index severity anchor, not a total-return replay.",
  },
  {
    id: "gfc",
    name: "2008-style credit shock",
    detail:
      "Chosen 55% equity decline over 18 months, followed by a 54-month recovery; housing/rent stress and falling reinvestment yields. Numerical shape is hypothetical.",
  },
  {
    id: "stagflation",
    name: "Persistent inflation",
    detail:
      "Five years of 8% inflation, weak stocks, higher maintenance/insurance and yield changes. Hypothetical, not a 1970s replay.",
  },
  {
    id: "rebound",
    name: "Rapid rebound / no entry crash",
    detail:
      "Two years of 25% stock growth, then the uneven baseline. Explicitly tests the cost of waiting.",
  },
  {
    id: "late",
    name: "Crash after deployment",
    detail:
      "The synthetic credit shock begins in month 60, after 24/36-month parking plus phasing. Staging does not remove later market risk.",
  },
];
const STOCK_OFFSETS = [0.07, -0.02, -0.16, 0.1, 0.04, -0.03, 0.08, -0.05];
const HOME_OFFSETS = [0.015, 0.005, -0.05, 0.025, 0.01, -0.005, 0.005, -0.015];
const CPI_OFFSETS = [0, 0.01, 0.02, -0.005, -0.015, 0, 0.005, -0.005];
export function equityMonthlyReturn(month, i) {
  const year = Math.floor(month / 12);
  const normal = () =>
    Math.pow(
      1 + Math.max(-0.9, i.stockGrowth + STOCK_OFFSETS[year % 8]),
      1 / 12,
    ) - 1;
  if (i.scenario === "depression") {
    if (month < 34) return Math.pow(0.11, 1 / 34) - 1;
    if (month < 300) return Math.pow(1 / 0.11, 1 / 266) - 1;
  }
  const start = i.scenario === "late" ? 60 : 0;
  if (["gfc", "late"].includes(i.scenario) && month >= start) {
    const m = month - start;
    if (m < 18) return Math.pow(0.45, 1 / 18) - 1;
    if (m < 72) return Math.pow(1 / 0.45, 1 / 54) - 1;
  }
  if (i.scenario === "rebound" && month < 24) return Math.pow(1.25, 1 / 12) - 1;
  if (i.scenario === "stagflation" && month < 60)
    return Math.pow(month < 24 ? 0.9 : 1.03, 1 / 12) - 1;
  return normal();
}
export function inflationAt(year, i) {
  if (i.scenario === "stagflation" && year < 5) return 0.08;
  if (i.scenario === "depression" && year < 3) return -0.02;
  if (i.scenario === "gfc" && year < 2) return year ? 0.015 : 0;
  return Math.max(-0.04, i.inflation + CPI_OFFSETS[year % 8]);
}
export function housingReturnAt(year, i) {
  if (["depression", "gfc"].includes(i.scenario) && year < 3)
    return [-0.15, -0.1, 0][year];
  if (i.scenario === "late" && year >= 5 && year < 8)
    return [-0.15, -0.1, 0][year - 5];
  return Math.max(-0.4, i.homeGrowth + HOME_OFFSETS[year % 8]);
}
export function treasuryYieldAt(month, i) {
  if (["depression", "gfc"].includes(i.scenario))
    return Math.max(
      0.0025,
      i.treasuryYield - Math.min(0.03, Math.floor(month / 3) * 0.003),
    );
  if (i.scenario === "late" && month >= 60)
    return Math.max(
      0.0025,
      i.treasuryYield - Math.min(0.03, Math.floor((month - 60) / 3) * 0.003),
    );
  if (i.scenario === "stagflation" && month >= 12 && month < 60)
    return Math.min(0.12, i.treasuryYield + 0.025);
  const shifts = [0, -0.005, 0.005, -0.01];
  return Math.max(0, i.treasuryYield + shifts[Math.floor(month / 12) % 4]);
}
