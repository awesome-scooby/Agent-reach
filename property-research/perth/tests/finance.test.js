const test = require("node:test");
const assert = require("node:assert");
const PF = require("../finance.js");

test("WA general duty schedule", () => {
  assert.strictEqual(PF.dutyGeneral(100000), 1900);
  assert.strictEqual(PF.dutyGeneral(500000), 17765);
  assert.strictEqual(PF.dutyGeneral(725000), 28452.5); // 11115 + 3650*4.75
  assert.strictEqual(PF.dutyGeneral(800000), 32315.5); // 28453 + 750*5.15
});

test("First home owner rate from 7 May 2026", () => {
  assert.strictEqual(PF.dutyFirstHome(600000, "2026-11-14"), 0);
  assert.strictEqual(PF.dutyFirstHome(600050, "2026-11-14"), 16.15); // part of $100
  assert.strictEqual(PF.dutyFirstHome(700000, "2026-11-14"), 16150);
  assert.strictEqual(PF.dutyFirstHome(800000, "2026-11-14"), 32300);
  assert.strictEqual(PF.dutyFirstHome(800001, "2026-11-14"), PF.dutyGeneral(800001));
  // before 7 May 2026 the old thresholds apply (agreement date decides)
  assert.strictEqual(PF.dutyFirstHome(550000, "2026-05-06"), 6815);
});

test("repayment formula", () => {
  assert.ok(Math.abs(PF.pmt(500000, 6, 30) - 2997.75) < 0.01);
  const a = PF.amortise({ principal: 500000, rate: 6, years: 30 });
  assert.ok(Math.abs(a.years - 30) < 0.1);
  const b = PF.amortise({ principal: 500000, rate: 6, years: 30, extra: 500 });
  assert.ok(b.years < 23 && b.totalInterest < a.totalInterest);
  const f = PF.amortise({ principal: 500000, rate: 6, years: 30, freq: "fortnightly" });
  assert.ok(f.years < 26 && f.years > 23, "half-monthly fortnightly ~ 13 payments/yr");
  const o = PF.amortise({ principal: 500000, rate: 6, years: 30, offset: 50000 });
  assert.ok(o.years < a.years);
});

test("LMI: none at 80%, none under guarantee, null above 95%", () => {
  assert.strictEqual(PF.lmi(480000, 600000), 0);
  assert.ok(PF.lmi(540000, 600000) > 0);
  assert.strictEqual(PF.lmi(570000, 600000, { guarantee: true }), 0);
  assert.strictEqual(PF.lmi(590000, 600000), null);
});

test("purchase at $600k with $130k deposit, first home", () => {
  const p = PF.purchase({ price: 600000, deposit: 130000, keepBuffer: 0, income1: 120000, income2: 80000,
    expenses: 4500, rate: 6.39, years: 30, date: "2026-11-14" });
  assert.strictEqual(p.duty, 0);
  assert.strictEqual(p.loan, 473000);
  assert.ok(p.lvr < 0.8 && p.lmi === 0);
});

test("buy vs wait: flat prices + rent > interest favours buying; big fall favours waiting", () => {
  const base = { price: 600000, deposit: 130000, income1: 120000, income2: 80000, expenses: 4500, rate: 6.39, years: 30,
    rentWeek: 600, monthlyBudget: 4500, horizon: 36, saveRate: 4, rentGrowth: 3, date: "2026-11-14" };
  const now = PF.buyVsWait({ ...base, wait: 0, pricePath: () => 1 });
  const wait = PF.buyVsWait({ ...base, wait: 12, pricePath: () => 1 });
  assert.ok(now.feasible && wait.feasible);
  const be = PF.breakEvenFall({ ...base, wait: 12 });
  assert.ok(be.fall !== null && be.fall > -0.2 && be.fall < 0.6);
  const fallBig = (m) => (m >= 12 ? 0.75 : 1 - 0.25 * m / 12);
  assert.ok(PF.buyVsWait({ ...base, wait: 12, pricePath: fallBig }).wealth > PF.buyVsWait({ ...base, wait: 0, pricePath: fallBig }).wealth);
});

test("net income and borrowing power are sane", () => {
  assert.ok(Math.abs(PF.netIncome(120000) - 91080) < 1);
  const bp = PF.borrowingPower({ income1: 120000, income2: 80000, expenses: 4500, rate: 6.39 });
  assert.ok(bp.maxLoan > 500000 && bp.maxLoan < 1200000);
  assert.ok(PF.conservativeLoan({ income1: 120000, income2: 80000, rate: 6.39 }) < bp.maxLoan);
});
