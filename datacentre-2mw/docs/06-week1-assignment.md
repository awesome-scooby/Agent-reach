# Week 1 Engineering Assignment

> SELF-DIRECTED ENGINEERING PROJECT — NOT A COMMISSIONED CLIENT DESIGN

**Document:** DC2MW-EL-ASSIGN-001
**Issued:** 2026-09-19
**Due before:** Week 2 commences
**Marked by:** Principal Engineer (design review standard, not encouragement
standard)

---

## Explain Like I'm 10 — what this assignment is for

I've just told you a lot of things. Right now, none of it is yours — it's mine, and
you've read it. This assignment is how it becomes yours. You're going to go and
attack my design, find things wrong with it, and defend your own numbers. That's
the actual job.

If you hand back work that agrees with everything I wrote, you've failed the
assignment, because I put real errors and real weak assumptions in the package and
some of them I haven't told you about.

---

## Task 1 — Answer the five understanding checks (mandatory)

In `docs/01-week1-fundamentals.md`, at the end. Two simple, three engineering.
Write your answers in a new file `docs/07-week1-answers.md`. Do not look back at
the teaching document while answering — answer from memory, then check.

**Marking standard for the engineering checks:** I want the loading percentage, the
specific failure that breaks it, and the reason. "Path B carries the load" is a
third of an answer.

---

## Task 2 — Independently verify the facility load build-up

Rebuild the load build-up in section 3 of the Basis of Design from first principles
in Excel. Do not copy my numbers — derive them.

Required structure — build it exactly like this, because this becomes your load
schedule template for Week 2:

| Column | Content |
|---|---|
| A | Load ID |
| B | Description |
| C | Quantity |
| D | Unit connected load (kW) |
| E | Total connected load (kW) — `=C*D` |
| F | Demand factor |
| G | Diversified load (kW) — `=E*F` |
| H | Criticality (UPS / Generator / Utility-only) |
| I | Supply path (A / B / Split) |
| J | A-side load (kW) |
| K | B-side load (kW) |
| L | Power factor |
| M | kVA — `=G/L` |
| N | Design current (A) — `=M*1000/(1.732*415)` for 3-phase |
| O | Upstream board |
| P | Notes |

Sections: IT load, UPS losses, chillers, pumps, CRAHs, mechanical controls,
lighting, small power, fire/life safety, security, BMS/EPMS, lifts/workshop,
generator ancillaries, transformer losses.

**Then answer these three questions in writing:**

2a. Do you get 3,465 kW? If not, where do we differ and which of us is right?

2b. My chiller electrical load is 780 kW, derived from a 2,150 kW thermal load and
an assumed COP of 2.9. **If the real COP at 38 °C turns out to be 2.4 instead of
2.9, recalculate the chiller load, the total facility load, the required per-path
generator capacity, and state whether my 4 × 2,400 kW generator selection still
works.** Show the arithmetic.

2c. I have assumed all 24 CRAHs run continuously at 8 kW each. But only 20 are
needed for duty. If all 24 run simultaneously sharing the same required airflow,
each runs at roughly 83% flow. Fan power varies approximately with the cube of
flow. **Recalculate the CRAH fan load on that basis and tell me whether my 170 kW
figure is conservative or wrong.**

---

## Task 3 — Find my errors

There are at least **four** genuine problems in the package I've issued. One of
them I have already flagged and corrected in front of you (the rack PDU current).
The others I have not pointed out.

Categories to look in:
- an arithmetic or unit error somewhere in the sizing calculations
- an assumption stated in one document that contradicts a value in another
- a redundancy claim that the supporting numbers do not actually support
- a load that appears in the load build-up but has no defined supply path
- something described as concurrently maintainable that the architecture does not
  actually permit

For each one you find, write: the document and section, what is wrong, why it is
wrong, the corrected value or statement, and what else in the package changes as a
consequence. **That last part is the real skill** — a design is a connected system
and a corrected number propagates.

**Do not invent errors to fill the quota.** Reporting three real ones is better than
three real ones plus two fabricated. If you think there are more than four, say so.

---

## Task 4 — Challenge one design decision, properly

Pick **one** decision from `registers/design-decision-register.csv` and argue
against it. Requirements:

- State the decision and my stated justification.
- Make the strongest case for the alternative, including at least one quantified
  argument (cost ratio, loading percentage, availability implication, capacity
  figure — something with a number in it).
- Identify what would have to be true for your alternative to be correct.
- State what additional information would settle the question.
- Give your own recommendation and commit to it.

The two I have explicitly flagged as contestable are DDR-001 (air-cooled versus
water-cooled chillers) and DDR-006 (generator redundancy, N per path versus N+1 per
path). **DDR-006 is the more interesting fight** — I have given a justification I
believe is defensible, and a good Principal Engineer would push back on it hard.
Push back on it.

"I agree with the decision" is not an acceptable answer to this task. If after
working through it you genuinely agree, argue the other side anyway and then say so
at the end — that is how design reviews work.

---

## Task 5 — Resolve TQ-001 far enough to make a recommendation

TQ-001, continuous cooling, is the largest open technical issue in the design. You
do not have the tools to do a proper thermal transient analysis, so do this instead:

5a. **Estimate** the data hall temperature rise rate with 2,000 kW of heat input and
zero airflow. You will need to assume an air volume and use the specific heat
capacity of air. State every assumption. Give an answer in °C per minute. This will
be crude — say so, and say which way it errs.

5b. Given that estimate, is a 60–120 second cooling interruption acceptable? What
IT inlet temperature limit are you working to, and where did that limit come from?

5c. If it is not acceptable, cost the electrical consequence: **which mechanical
loads move onto the UPS, how many kW, and what does that do to the UPS sizing and
to the battery sizing?** Give me the new per-path UPS rating. Note that this may
resolve TQ-011 at the same time.

5d. Make a recommendation, in one paragraph, of the kind you would put in front of a
client.

---

## Task 6 — Produce drawing DC2MW-EL-SLD-001

Using `docs/03-architecture-block-diagram.md`, produce the overall key single line
diagram in AutoCAD Electrical.

Non-negotiables for the first issue:
- Both paths on one sheet, Path A left, Path B right, **empty vertical gutter down
  the centre**.
- Every switching device annotated `N.O.` or `N.C.`
- Transformer ratings, ratio, vector group, %Z and LV FLC annotated.
- Fault level annotated at MSB-A and MSB-B, with the preliminary-status note.
- Fire compartment boundaries shown.
- The 4-pole generator changeover shown as 4-pole, with the neutral switching note.
- The full notes block from section 4.6.
- Title block marked **SELF-DIRECTED PROJECT — NOT FOR CONSTRUCTION**.

Issue it as Rev A. I will review it as a 30% design review submission, and I will
mark it against the eight comprehension tests in section 4.8 of the brief.

---

## Task 7 — Rehearse three interview answers out loud

From `docs/05-interview-knowledge-bank.md`, take **Q1 (explain 2N)**, **Q4 (utility
failure)** and **Q7 (redundancy vs resilience)**.

Say each one out loud, without notes, and time it. Target 60–90 seconds each.
Then write down what you actually said, not what you meant to say.

Then answer this: for each one, which sentence in your spoken answer was the weakest,
and why? The weak sentence is almost always the one where you're reciting rather than
reasoning — and an interviewer can hear the difference immediately.

---

## What I will do with your submission

I will review it as a **30% Design Review**, at Principal Engineer standard:

- Technical errors identified without softening.
- Weak assumptions challenged.
- Missing interfaces named.
- Common-mode failures you missed, named.
- Calculations you have not supported, called out.
- Your drawing marked against the eight comprehension tests.

I will not approve weak engineering to encourage you. If the load schedule doesn't
reconcile, I will say so. If the drawing doesn't communicate the two-path
architecture at a glance, it goes back for Rev B.

Then we move to Week 2 — load development and electrical architecture — and the
difficulty increases.

---

## Explain Like I'm 10 — what finishing this proves

If you can finish this, you'll have proved something more useful than "I read about
data centres." You'll have proved you can take someone else's design, check their
sums, find their mistakes, argue with their decisions using numbers, and draw the
whole thing yourself.

That's not learning about the job. That's doing the job.
