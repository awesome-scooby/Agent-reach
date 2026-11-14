/* Perth buyer finance engine. Pure functions, no DOM. Inlined into the
 * dashboard by build_perth.py and unit-tested with `node --test perth/tests`.
 *
 * Every rule here is either an official published schedule (cited) or an
 * explicit, editable assumption. Nothing in this file is a lender quote.
 */
(function (root) {
  "use strict";

  // ---------------------------------------------------------------- duty
  // WA general (= residential since 1 Jul 2022) transfer duty schedule.
  // Source: RevenueWA transfer duty assessment / fact sheets (checked 14 Nov 2026).
  const GENERAL = [
    [0, 120000, 0, 1.90],
    [120000, 150000, 2280, 2.85],
    [150000, 360000, 3135, 3.80],
    [360000, 725000, 11115, 4.75],
    [725000, Infinity, 28453, 5.15],
  ];
  function per100(x) { return Math.ceil(Math.round(x * 100) / 100 / 100); } // "or part of $100"

  function dutyGeneral(v) {
    for (const [lo, hi, base, rate] of GENERAL) {
      if (v <= hi) return round2(base + per100(v - lo) * rate);
    }
    return 0;
  }

  // First home owner rate (homes, not vacant land). Source: WA Duties Fact
  // Sheet - First Home Owner Rate (wa.gov.au, checked 14 Nov 2026).
  // Agreement date decides, not settlement.
  const FHOR = [
    { from: "2026-05-07", zero: 600000, cap: 800000, rate: 16.15 },
    { from: "2025-03-21", zero: 500000, cap: 700000, rate: 13.63 }, // Metro/Peel
    { from: "2024-05-09", zero: 450000, cap: 600000, rate: 15.01 },
    { from: "0000-01-01", zero: 430000, cap: 530000, rate: 19.19 },
  ];
  function dutyFirstHome(v, agreementDate) {
    const d = agreementDate || "2026-11-14";
    const r = FHOR.find((x) => d >= x.from);
    if (v <= r.zero) return 0;
    if (v <= r.cap) return round2(per100(v - r.zero) * r.rate);
    return dutyGeneral(v);
  }
  function duty(v, opts) {
    opts = opts || {};
    return opts.firstHome === false ? dutyGeneral(v) : dutyFirstHome(v, opts.date);
  }

  // ---------------------------------------------------------------- LMI
  // INDICATIVE ONLY. LMI is priced by the insurer per lender, loan size and
  // LVR; this table is a rough mid-market approximation, not a quote.
  // Eligible buyers under the Australian Government 5% Deposit Scheme
  // (Perth price cap $850k) pay no LMI - modelled by opts.guarantee.
  const LMI_TABLE = [[0.80, 0], [0.85, 0.009], [0.90, 0.018], [0.95, 0.032]];
  function lmi(loan, value, opts) {
    opts = opts || {};
    const lvr = loan / value;
    if (opts.guarantee && value <= (opts.guaranteeCap || 850000) && lvr <= 0.95) return 0;
    if (lvr <= 0.80) return 0;
    for (const [hi, pct] of LMI_TABLE) if (lvr <= hi) return Math.round(loan * pct);
    return null; // above 95% LVR: not lendable in this model
  }

  // ----------------------------------------------------------- repayments
  function pmt(principal, annualRate, years, perYear) {
    perYear = perYear || 12;
    const n = years * perYear, i = annualRate / 100 / perYear;
    if (principal <= 0) return 0;
    if (i === 0) return principal / n;
    return principal * i / (1 - Math.pow(1 + i, -n));
  }

  /* Simulate a P&I loan month by month (or fortnight by fortnight).
   * extra: additional repayment per period; offset: constant offset balance.
   * 'fortnightlyHalf' = pay half the monthly amount every fortnight
   * (26 half-payments = 13 monthly payments a year), the common trick. */
  function amortise(o) {
    const perYear = o.freq === "fortnightly" ? 26 : 12;
    const base = o.freq === "fortnightly" ? pmt(o.principal, o.rate, o.years, 12) / 2 : pmt(o.principal, o.rate, o.years, 12);
    const pay = base + (o.extra || 0);
    const i = o.rate / 100 / perYear;
    let bal = o.principal, interest = 0, k = 0;
    const path = [];
    while (bal > 0.005 && k < o.years * perYear * 2) {
      const charged = Math.max(0, bal - (o.offset || 0)) * i;
      interest += charged;
      bal = bal + charged - pay;
      k++;
      if (k % perYear === 0) path.push(Math.max(0, Math.round(bal)));
    }
    return { periods: k, years: k / perYear, totalInterest: Math.round(interest), payment: round2(pay), perYear: perYear, path: path };
  }

  function balanceAfter(principal, rate, years, months, extra) {
    const i = rate / 100 / 12, p = pmt(principal, rate, years, 12) + (extra || 0);
    let b = principal;
    for (let m = 0; m < months && b > 0; m++) b = b * (1 + i) - p;
    return Math.max(0, b);
  }

  // ------------------------------------------------------------ income tax
  // Resident rates 2026-27 (15% bracket from 1 Jul 2026, legislated 2025),
  // plus 2% Medicare levy. Ignores offsets, HELP, Medicare surcharge.
  function netIncome(gross) {
    const b = [[18200, 0], [45000, 0.15], [135000, 0.30], [190000, 0.37], [Infinity, 0.45]];
    let tax = 0, lo = 0;
    for (const [hi, r] of b) { if (gross > lo) tax += (Math.min(gross, hi) - lo) * r; lo = hi; }
    return gross - tax - 0.02 * gross;
  }

  /* Approximate lender serviceability (NOT a lender's calculator):
   * monthly net income - living expenses - other commitments - 3.8% of
   * card limits = surplus available; max loan = PV of that surplus at the
   * assessment rate (actual + APRA buffer, default 3.0 pts). */
  function borrowingPower(o) {
    const net = (netIncome(o.income1) + netIncome(o.income2)) / 12;
    const cards = 0.038 * (o.cardLimits || 0);
    const surplus = net - o.expenses - (o.otherDebts || 0) - cards;
    const ar = o.rate + (o.buffer == null ? 3.0 : o.buffer);
    const i = ar / 100 / 12, n = (o.years || 30) * 12;
    const max = surplus <= 0 ? 0 : surplus * (1 - Math.pow(1 + i, -n)) / i;
    return { netMonthly: Math.round(net), surplus: Math.round(surplus), assessmentRate: ar, maxLoan: Math.round(max / 1000) * 1000 };
  }

  /* Conservative recommendation, separate from what a lender might approve:
   * repayment at (rate + stress) over the chosen term must stay within
   * `share` of GROSS household income, and the buyer keeps `buffer` cash. */
  function conservativeLoan(o) {
    const cap = (o.income1 + o.income2) * (o.share || 0.30) / 12;
    const r = (o.rate + (o.stress == null ? 2 : o.stress)) / 100 / 12, n = (o.years || 25) * 12;
    return Math.round(cap * (1 - Math.pow(1 + r, -n)) / r / 1000) * 1000;
  }

  // ---------------------------------------------------------- purchase
  function purchase(o) {
    const d = duty(o.price, { firstHome: o.firstHome !== false, date: o.date });
    const other = o.otherCosts == null ? 3000 : o.otherCosts; // conveyancing, searches, inspections, Landgate fees
    const cashIn = Math.max(0, o.deposit - (o.keepBuffer || 0));
    const upfront = d + other;
    let loan = Math.max(0, o.price + upfront - cashIn);
    let lm = lmi(loan, o.price, { guarantee: o.guarantee });
    if (lm == null) return { feasible: false, reason: "LVR above 95%", duty: d, otherCosts: other, loan: loan, lvr: loan / o.price };
    if (o.capitaliseLmi !== false) loan += lm;
    const lvr = loan / o.price;
    const rep = pmt(loan, o.rate, o.years, 12);
    const stressRep = pmt(loan, o.rate + (o.stress == null ? 2 : o.stress), o.years, 12);
    const am = amortise({ principal: loan, rate: o.rate, years: o.years, extra: o.extra || 0, offset: o.offset || 0, freq: o.freq });
    const grossM = (o.income1 + o.income2) / 12;
    const netM = (netIncome(o.income1) + netIncome(o.income2)) / 12;
    const owning = (o.ownCostsYear == null ? 6500 : o.ownCostsYear) / 12;
    return {
      feasible: true, price: o.price, duty: d, otherCosts: other, lmi: lm, depositUsed: Math.min(cashIn, o.price + upfront),
      cashLeft: o.deposit - Math.min(cashIn, o.price + upfront), loan: Math.round(loan), lvr: lvr,
      repayment: Math.round(rep), stressRepayment: Math.round(stressRep),
      repaymentShareGross: rep / grossM, stressShareGross: stressRep / grossM,
      surplus: Math.round(netM - rep - (o.extra || 0) * (o.freq === "fortnightly" ? 26 / 12 : 1) - owning - o.expenses),
      yearsToRepay: am.years, totalInterest: am.totalInterest, balancePath: am.path,
    };
  }

  /* Buy now vs wait W months, compared on NET WEALTH at a common horizon H
   * (months from today). Both households spend the same on housing + saving:
   *   monthlyBudget = what they can put toward housing each month.
   * Buyer: pays mortgage + ownership costs; anything left of the budget
   *        goes into savings. Renter: pays rent; saves the rest, plus the
   *        deposit earns `saveRate`. At W the renter buys at the scenario
   *        price with the larger deposit and the then-mortgage rate.
   * Wealth = home value - loan balance + cash. Principal repaid is NOT a
   * cost (it is wealth); rent is a cost but buys housing, so is not "wasted":
   * the comparison is total wealth, not cash flow.
   * pricePath(m) -> multiplier of today's price at month m (scenario). */
  function buyVsWait(o) {
    const H = o.horizon, budget = o.monthlyBudget;
    const sr = (o.saveRate || 4.0) / 100 / 12;
    function buyAt(m, deposit, rateAt) {
      // buyDiscount: what you pay below the scenario's market value (negotiation)
      const price = o.price * o.pricePath(m) * (1 - (o.buyDiscount || 0));
      const p = purchase(Object.assign({}, o, { price: price, deposit: deposit, rate: rateAt, extra: 0, offset: 0 }));
      return p;
    }
    function run(W) {
      let cash = o.deposit, loan = 0, owned = false, rate = o.rate, bought = null, rentPaid = 0, interestPaid = 0;
      for (let m = 0; m < H; m++) {
        if (!owned && m === W) {
          rate = o.rate + (o.rateChangeAtWait || 0) * (W > 0 ? 1 : 0);
          const p = buyAt(m, cash, rate);
          if (!p.feasible) return { feasible: false, W: W };
          bought = p; owned = true;
          cash = p.cashLeft; loan = p.loan;
        }
        if (owned) {
          const i = rate / 100 / 12, rep = pmt(bought.loan, rate, o.years, 12);
          const intM = loan * i; interestPaid += intM;
          loan = Math.max(0, loan + intM - rep);
          const own = (o.ownCostsYear == null ? 6500 : o.ownCostsYear) / 12;
          cash = cash * (1 + sr) + (budget - rep - own);
        } else {
          const rent = o.rentWeek * 52 / 12 * Math.pow(1 + (o.rentGrowth || 3) / 100, m / 12);
          rentPaid += rent;
          cash = cash * (1 + sr) + (budget - rent);
        }
      }
      const value = owned ? o.price * o.pricePath(H) : 0;
      return { feasible: true, W: W, wealth: Math.round(value - loan + cash), value: Math.round(value), loan: Math.round(loan),
               cash: Math.round(cash), rentPaid: Math.round(rentPaid), interestPaid: Math.round(interestPaid),
               buyPrice: bought ? Math.round(bought.price) : null, duty: bought ? bought.duty : null };
    }
    return run(o.wait || 0);
  }

  /* Price fall (fraction of today's price, reached by month W and held
   * flat to H) at which waiting W months matches buying now. */
  function breakEvenFall(o) {
    const now = buyVsWait(Object.assign({}, o, { wait: 0, pricePath: () => 1 }));
    const f = (fall) => buyVsWait(Object.assign({}, o, { wait: o.wait, pricePath: (m) => (m >= o.wait ? 1 - fall : 1 - fall * m / o.wait) }));
    // With prices flat after W, buyer-now's home is also worth (1-fall):
    const gap = (fall) => {
      const nowF = buyVsWait(Object.assign({}, o, { wait: 0, pricePath: (m) => (m >= o.wait ? 1 - fall : 1 - fall * m / o.wait) }));
      const w = f(fall);
      return w.feasible ? w.wealth - nowF.wealth : -Infinity;
    };
    let lo = -0.2, hi = 0.6;
    if (gap(hi) < 0) return { fall: null, now: now };
    for (let k = 0; k < 60; k++) { const mid = (lo + hi) / 2; if (gap(mid) >= 0) hi = mid; else lo = mid; }
    return { fall: Math.round(hi * 1000) / 1000, now: now };
  }

  function round2(x) { return Math.round(x * 100) / 100; }

  const api = { dutyGeneral, dutyFirstHome, duty, lmi, pmt, amortise, balanceAfter, netIncome, borrowingPower,
                conservativeLoan, purchase, buyVsWait, breakEvenFall, FHOR, GENERAL };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.PF = api;
})(typeof window !== "undefined" ? window : globalThis);
