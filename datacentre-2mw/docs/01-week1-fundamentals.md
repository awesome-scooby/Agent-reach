# Week 1 — Data Centre Critical Power Fundamentals

> SELF-DIRECTED ENGINEERING PROJECT — NOT A COMMISSIONED CLIENT DESIGN

**Document:** DC2MW-EL-TEACH-001
**Rev:** 0.1
**Purpose:** Establish the conceptual foundation required before any equipment
selection. No equipment is selected in this document.

---

## What we are learning this week, and why

This week is about one idea: **a data centre is not a building with computers in
it. It is an electrical and mechanical machine whose product is uninterrupted
power and cooling, and the computers are the customer.**

Everything that follows in Weeks 2–10 — transformer sizing, generator
paralleling, UPS module counts, selectivity studies, commissioning scripts —
is downstream of the vocabulary and architecture logic we build now. If you
get "2N" or "concurrent maintainability" subtly wrong this week, you will
produce a design that looks correct on a single line diagram and fails in a
design review, because a reviewer will find a component that both Path A and
Path B depend on.

**Explain Like I'm 10:** This week we learn the words and the big ideas, like
learning the rules of a game before you play it. If you learn the rules wrong,
you can play very confidently for a long time and still be playing wrong.

---

## 1. What a data centre actually is

### Engineer Explanation

A data centre is a purpose-built facility whose function is to deliver
**conditioned, continuous electrical power** and **continuous heat removal** to
IT equipment, within controlled environmental limits, at a defined availability
target, for a defined operational life.

Functionally it is four coupled systems:

1. **Electrical** — utility intake, transformation, standby generation,
   uninterruptible power, distribution to rack.
2. **Mechanical** — heat rejection. Every watt of electrical power delivered to
   IT equipment becomes very nearly a watt of heat that must be removed.
3. **Control and monitoring** — BMS (mechanical), EPMS (electrical), the logic
   that sequences generators, transfers sources and alarms faults.
4. **Fire, security and structure** — detection and suppression suited to
   energised electrical rooms, physical access control, floor loading, cable
   containment.

The electrical and mechanical systems are not independent. **Cooling is an
electrical load.** If you lose power to the chillers, you lose cooling, and a
high-density data hall with no airflow reaches IT thermal shutdown temperature
in single-digit minutes. This is the single most common conceptual error made by
electrical engineers new to the sector: they protect the IT load with a UPS and
leave the cooling plant on a non-backed board. The IT equipment then survives the
power event and dies of heat twenty minutes later.

Classification frameworks you will be asked about:

- **Uptime Institute Tier I–IV** — a topology and operational classification.
  Tier III ≈ concurrently maintainable. Tier IV ≈ fault tolerant. These are
  certification marks with specific criteria; do not claim a Tier rating for a
  design that has not been certified.
- **ISO/IEC 22237 series** — availability classes 1–4 for data centre
  facilities and infrastructures. The international standard equivalent concept.
- **EN 50600 series** — the European antecedent, largely aligned with 22237.
- **TIA-942** — telecommunications infrastructure standard for data centres,
  includes a rating system and a strong cabling/spaces focus.

*Standard/clause verification required for the specific criteria of each
availability class before citing them as design compliance.*

### Explain Like I'm 10

A data centre is a big building full of computers that hold everyone's photos,
bank records, emails and websites. But the interesting part isn't the computers —
it's everything built around them to keep them alive. Think of it like a
hospital's intensive care unit. The patients are the computers. The building has
to give them a perfectly steady supply of electricity and constantly blow cool
air over them, because computers turn electricity into heat, and hot computers
break.

So a data centre is really an electricity-and-cooling factory that happens to
have computers as its customers. If the electricity wobbles for even a fraction
of a second, or the cool air stops for a few minutes, the computers stop — and
suddenly thousands of people can't use their bank or their hospital records.

### Practical Data Centre Example (our design)

Our facility has a 2,000 kW IT load. That means roughly **2,000 kW of heat**
continuously dumped into two data halls. Our air-cooled chilled water plant that
removes it will itself draw around **1,110 kW of electricity**. So our electrical
design is not a 2 MW problem — it is a **~3.5 MW problem**, and about a third of
our total electrical design work exists purely to serve the cooling system that
exists purely to serve the IT load.

### Interview Connection

You should be able to say, unprompted: *"A data centre electrical design isn't
just the critical power path. The mechanical plant is an electrical load, and
which parts of it sit on UPS versus generator-only versus utility-only is a
critical power decision, not a mechanical one. Get that wrong and you've built a
facility that rides through a power event and then thermally shuts down."*

---

## 2. Why electrical reliability matters so much

### Engineer Explanation

Three reasons, in order of how often they actually drive design:

**1. Commercial and contractual.** Colocation and cloud operators sell
availability under an SLA. "Five nines" (99.999%) permits about **5.3 minutes of
downtime per year**. Four nines (99.99%) permits about 52.6 minutes. Three nines
(99.9%) permits 8.8 hours. SLA breach means service credits, and at scale a
single outage can cost more than the redundancy that would have prevented it.
The redundancy is bought with money and justified against the cost of an outage.

**2. Technical fragility of the load.** IT power supplies are switch-mode units
with limited stored energy. The relevant reference is the **ITIC curve** (the
Information Technology Industry Council curve, successor to CBEMA) which
describes the voltage/duration envelope IT equipment is expected to tolerate.
Practically, a modern server PSU will ride through a complete loss of supply for
roughly **10–20 ms**, and will tolerate moderate sags for longer. It will not
ride through the **8–15 seconds** a diesel generator needs to start, come up to
speed, achieve stable voltage and frequency, and close its breaker. That gap is
the entire reason the UPS exists.

**3. Recovery is not instant and not free.** An unplanned data hall shutdown is
not a "switch it back on" event. You get filesystem corruption, databases
requiring consistency checks, storage arrays rebuilding, virtualisation clusters
recovering, and a restart sequence that must be ordered (storage, then network,
then compute, then applications). A 2-second power event can produce a
**6-hour service restoration**. The ratio between event duration and outage
duration is the thing non-specialists consistently underestimate.

A fourth, underrated reason: **thermal runaway couples to the electrical event**,
as covered above.

### Explain Like I'm 10

Imagine a whole city's worth of people all keeping their most important
information in one building. If the electricity in that building flickers for
even one second, the computers switch off — and when they switch back on, a lot
of the information is muddled up and has to be checked and repaired, one piece
at a time. That repair can take all day, even though the power was only gone for
a second.

It's like a library where one tiny gust of wind knocks every book off every
shelf. Picking them all up and putting them back in order takes far longer than
the gust of wind did. So the people who build these buildings work extremely hard
to make sure that gust of wind can never happen.

### Practical Data Centre Example (our design)

Our 2N architecture exists specifically to close the gap between what the utility
can deliver and what the load requires. A single 11 kV utility feeder in an
Australian metro area is a good supply — but it will still see momentary
interruptions from upstream reclosers, transient sags from network faults, and
planned outages for network maintenance. Over a 15-year design life, a single
feeder with no standby generation and no UPS would produce dozens of IT load
events. Our target is **zero IT load events from any single component failure,
and zero from any planned maintenance activity.**

### Interview Connection

Be ready with the numbers: five nines = 5.3 min/yr; server PSU ride-through
≈ 10–20 ms; generator start-to-on-load ≈ 8–15 s. Then the punchline: *"The
mismatch between 20 milliseconds of ride-through and 15 seconds of generator
start time is why the UPS exists. Everything else in the critical power chain is
arranged around that one fact."*

---

## 3. What a 2 MW IT load means

### Engineer Explanation

"2 MW IT load" is dangerously ambiguous until you pin down four things:

**Where is it measured?** Options are: sum of IT nameplate; sum of rack PDU
design capacity; actual measured draw at the rack PDU; UPS output. These can
differ by a factor of two or more. Nameplate on a dual-PSU server is typically
the rating of one PSU, and a server at typical utilisation draws perhaps 40–60%
of its nameplate.

**Is it per-path or total?** In a 2N facility carrying 2 MW of IT, under normal
operation each path carries **1 MW**. But each path must be **capable of 2 MW**,
because it has to absorb the whole load when the other path is out. Someone who
sizes each side at 1 MW has built a single-fault-intolerant facility and called
it 2N. This is the classic sizing error.

**Is it design load or ultimate load?** Data centres are built in phases. A
2 MW day-one design may be on a site master-planned for 8 MW, which changes
intake, containment, plant room and spatial allowances even though the day-one
electrical equipment is sized for 2 MW.

**Does it include network and MMR?** The Meet-Me Room, core network and
storage are IT loads on UPS but are sometimes accounted separately from
"data hall IT".

**Our definition (locked):** 2,000 kW is the **total diversified IT design load
measured at the output of the rack PDUs**, inclusive of data hall IT equipment,
core network and MMR. Each of Path A and Path B shall be capable of carrying the
full 2,000 kW.

### Explain Like I'm 10

Saying "the data centre is 2 megawatts" is a bit like saying "the bridge carries
10 tonnes". You immediately have to ask: 10 tonnes of trucks sitting still, or
10 tonnes moving? 10 tonnes on each lane, or 10 tonnes shared across both lanes?
10 tonnes today, or 10 tonnes once the new suburb is built?

In our data centre, the answer is: 2 megawatts is what all the computers use
altogether. Normally the two separate electricity systems share it, so each one
carries 1 megawatt. But each one has to be built big enough to carry the whole
2 megawatts on its own, because one day the other one will be switched off for
repairs and the remaining one has to do the whole job by itself.

### Practical Data Centre Example (our design)

This definition drives the single most expensive decision in the project:

| Item | Normal operation | Design capability |
|---|---|---|
| Path A IT load | 1,000 kW | **2,000 kW** |
| Path B IT load | 1,000 kW | **2,000 kW** |
| Installed UPS capability | — | 2 × 2,500 kW |
| Normal UPS loading | 40% | — |
| Single-path loading (worst case) | — | 80% |

We are installing 5,000 kW of UPS capability to serve 2,000 kW of load. That is
what genuine 2N costs, and being able to justify that 2.5× ratio to a
cost-focused client is a real project-engineering skill.

### Interview Connection

If an interviewer says "we have a 2 MW data hall", your first question should be
*"measured where, and is that per path or total?"* Asking that question tells
them more about your competence than any answer you could give.

---

## 4. Facility load versus IT load

### Engineer Explanation

**IT load** is the electrical power consumed by the computing, storage and
network equipment. It is the facility's revenue-earning load.

**Facility load** (also "total facility power", TFP) is everything the site
draws at the utility meter: IT load, plus cooling plant, plus electrical
distribution losses, plus lighting, fire, security, controls, offices,
lifts and every other ancillary.

The ratio is **PUE**:

```
PUE = Total Facility Power / IT Equipment Power
```

PUE is defined in the ISO/IEC 30134 series. Critical points that separate
engineers from marketers:

- **PUE is an energy ratio, measured annualised (kWh/kWh)** — not a power ratio
  at an instant. Quoting "our PUE is 1.2" at a design point is a category error.
- **Design-day (peak) PUE is always worse than annualised PUE**, because peak
  PUE happens at maximum ambient temperature when chillers are least efficient,
  while annualised PUE benefits from all the mild hours of the year.
- **You cannot size electrical equipment from PUE.** PUE is a sanity check.
  You size from an actual mechanical load calculation based on selected plant at
  design ambient conditions. Using PUE × IT load to size a transformer is a
  shortcut that will be picked apart in a design review.
- A low PUE is an operating-cost metric. It says nothing about reliability. A
  Tier IV facility will have a worse PUE than a Tier I facility with identical
  cooling, because 2N distribution means equipment runs at lower load factors
  where it is less efficient. **Resilience and efficiency trade against each
  other.**

### Explain Like I'm 10

Imagine you buy a pizza for $10, but delivery costs $4. You paid $14 to get $10
of pizza. So for every dollar of actual pizza, you spent $1.40. That's the
"pizza usage effectiveness" — 1.4.

In a data centre, the pizza is the electricity that actually goes into the
computers, and the delivery cost is all the extra electricity needed for fans,
chillers, pumps and lights to keep the computers cool and the building running.
If our computers use 2 megawatts and the whole building uses 2.8 megawatts, our
number is 1.4. Everybody wants that number to be as close to 1.0 as possible,
because the extra is pure cost with no benefit — but you can never reach 1.0,
because the cooling can never be free.

### Practical Data Centre Example (our design)

Preliminary facility load build-up, derived from selected plant rather than from
a PUE assumption:

| Category | Design (kW) | Basis |
|---|---|---|
| IT load | 2,000 | Given requirement |
| UPS losses | 85 | 2,000 kW at 96% efficiency |
| Chillers (3 duty of 4) | 780 | 2,150 kW(th) at COP 2.9, 38 °C ambient |
| CHW pumps (primary + secondary) | 135 | Assumed |
| CRAH EC fans (24 units) | 170 | Assumed |
| Mechanical controls / valves / humidity | 25 | Assumed |
| House and ancillary loads | 235 | Lighting, fire, security, offices, lifts, generator ancillaries |
| Transformer losses | 35 | ~1.0% at operating load |
| **Total facility design load** | **3,465** | Calculated |

**Design-day PUE = 3,465 / 2,000 = 1.73**

**Assumed annualised PUE = 1.40** — much better than design-day because our
Australian temperate-climate site sits well below 38 °C ambient for the large
majority of the year, and free-cooling/high-CHW-setpoint hours are available.

Note the teaching point directly: the two numbers differ by 24%, and they are
both correct. The 1.73 sizes our electrical equipment. The 1.40 goes on the
client's sustainability report.

### Interview Connection

Three things to have ready: (1) PUE is annualised energy, not instantaneous
power; (2) design-day PUE is worse than annualised, and design-day is what sizes
your switchgear; (3) you never size electrical equipment from PUE — you size it
from a mechanical load calculation. Saying the third one out loud will mark you
as someone who has actually done the work.

---

## 5. What N means

### Engineer Explanation

**N is the capacity required to carry the design load, with no redundancy and no
spare.** N is not a number of units — it is a *quantity of capability*, which
may be delivered by one unit or by many.

If your load is 2,100 kW of cooling and you select 700 kW chillers, then N = 3
chillers. If you select 1,050 kW chillers, N = 2. Same N, different unit count.

Properties of an N system:
- Every installed unit is required. There is no spare.
- Any single component failure results in loss of capacity, and therefore
  (partial or total) loss of load.
- **No component can be taken out of service for maintenance without losing
  capacity.** This is the operationally crippling consequence, and it is worse
  than the reliability consequence, because maintenance is certain and failure
  is only probable.
- Availability is limited by the least reliable component in series.

N is appropriate for non-critical loads: office lighting, general power,
workshop, landscape irrigation. It is never appropriate for critical power.

A trap: **N does not mean "one of something".** A 2,000 kW load served by a
single 2,000 kW UPS is N. A 2,000 kW load served by eight 250 kW UPS modules
with no spare module is also N. Both fail the same way.

### Explain Like I'm 10

N means "exactly enough, and not one bit more."

Imagine you need to move 30 kids to a school camp and each bus holds 10 kids.
You need 3 buses. That's N = 3 buses. Now if one bus breaks down on the morning
of the trip, 10 kids don't go to camp. And if a bus needs its brakes serviced,
you can't service it — because you need all three buses, every single day.

That second problem is actually the bigger one. Breakdowns might never happen.
Servicing definitely has to happen.

### Practical Data Centre Example (our design)

We use N deliberately, in exactly one place: **the generator count within each
path.** Each path has 2 × 2,400 kW generators sized to carry the full facility
load. That is N per path, with no spare generator inside the path. The redundancy
is provided at the *facility* level by the other path, not inside the path.

Whether that is the right call is a real design decision that we will argue at
the 30% review — the alternative is N+1 per path, which is 2(N+1) on generators
and adds two 2,400 kW diesel sets and their fuel, acoustics, emissions approvals
and capital cost for a second layer of protection on top of a layer we already
have. See `registers/design-decision-register.csv`, DDR-006.

### Interview Connection

Define N as *capability*, not *unit count*. Then immediately raise the
maintenance consequence: *"The reason N is unacceptable for critical loads isn't
mainly the failure risk. It's that you can never take anything out of service to
maintain it, so you're forced to choose between deferring maintenance and
dropping load."*

---

## 6. What N+1 means

### Engineer Explanation

**N+1 provides the capability required by the load, plus one additional unit of
the largest single module.** The system tolerates the loss of any one unit —
whether that loss is a failure or a planned isolation — without loss of capacity
to the load.

Critical precision points:

- **The "+1" must be at least as large as the largest unit it has to cover.**
  If you have 3 × 700 kW chillers and a "+1" of 400 kW, you do not have N+1.
- **N+1 provides capacity redundancy, not path redundancy.** This is the single
  most important limitation, and the one that inexperienced engineers miss. If
  all N+1 units connect to a common busbar, feed through a common breaker, or
  are controlled by a common controller, that shared element is a **single point
  of failure** and the system is N+1 for the *units* but N for the *system*.
- **N+1 does not survive two coincident events.** Losing a unit to failure while
  another unit is out for maintenance takes you below N. On a facility with a
  long maintenance programme this is not a remote scenario; it is a Tuesday.
- N+1 is typically expressed with a redundancy level: N+1 at module level, N+1 at
  unit level, N+1 at system level — these are different things and must be
  stated explicitly.

N+1 is the right answer for **capacity plant that isn't in the critical path** —
chillers, pumps, CRAHs, generators at a facility level — and for **modules
inside a UPS system**. It is not sufficient on its own for the critical power
*path*.

### Explain Like I'm 10

N+1 means "exactly enough, plus one spare."

Back to the school camp: you need 3 buses for 30 kids, so you bring 4. Now if
one bus breaks down, all the kids still get to camp. And on a normal week, you
can send one bus in for a service and still do every trip. That's a much better
system than 3 buses.

But here's the catch. What if all four buses have to drive out through the same
narrow gate, and someone parks a truck across the gate? Then having a spare bus
doesn't help you at all. The spare fixes "a bus broke", but it doesn't fix
"the gate is blocked". A lot of people think they have a really safe system
because they bought a spare bus, and they've never noticed the gate.

### Practical Data Centre Example (our design)

We apply N+1 in three places in our design, and in every case the shared element
is identified and dealt with:

| System | N+1 arrangement | Shared element (the "gate") | How we address it |
|---|---|---|---|
| Chillers | 4 × 750 kW(th), 3 duty + 1 standby | Common CHW ring main | Sectionalising valves; chillers split across MSB-A and MSB-B |
| CRAHs | 12 per hall, 10 duty + 2 standby | Common hall airflow; CRAH power | CRAHs alternately fed from A and B mechanical boards |
| UPS modules | 6 × 250 kW per frame, 1,250 kW rated | Common parallel bus + static switch inside the frame | Accepted within a path; Path B is fully independent |

That third row is the honest one. The parallel bus inside a UPS frame *is* a
common-mode element for the modules in that frame. We do not pretend otherwise.
We accept it because its failure costs us one path, not the load.

### Interview Connection

Two sentences that will do a lot of work for you: *"N+1 is capacity redundancy,
not path redundancy. If all the N+1 units land on a common bus or a common
controller, the system is N+1 for the units and N for the system."* Then offer
the example: N+1 chillers on a single non-sectionalised chilled water ring is not
N+1 cooling.

---

## 7. What 2N means

### Engineer Explanation

**2N provides two complete, independent systems, each individually capable of
carrying the entire design load.** Not two units. Two *systems* — each with its
own source, its own transformation, its own standby generation, its own
uninterruptible power, its own distribution, and its own controls, from the point
of divergence all the way to the load.

The defining test of 2N is not "are there two of everything". It is:

> **Can I take one entire path out of service — de-energised, earthed, doors
> open, boards stripped, technicians working inside — with zero impact on the IT
> load?**

If the answer is yes, it is 2N. If the answer requires any qualification, it is
not.

What makes 2N different from N+1 in kind, not just degree:

| | N+1 | 2N |
|---|---|---|
| Redundancy type | Capacity | Capacity **and** path |
| Surviving unit loading on failure | Increases to 100% | Increases to 100% of one path |
| Common bus | Usually present | **Must not exist** |
| Common controller | Usually present | **Must not exist** |
| Concurrent maintainability | Partial | Complete |
| Cost multiplier vs N | ~1.3× | ~2.0–2.5× |

**The failure modes 2N is specifically designed to defeat are the ones N+1
cannot touch:** busbar faults, switchboard fires, control system failures,
protection maloperation, human switching error, and — critically — planned
maintenance on any asset in the chain.

**The hidden common-mode failure problem.** A 2N architecture is only as
independent as its least independent element. Real examples of things that quietly
destroy 2N:

- Both paths' transformers fed from the same MV busbar.
- Both paths' MV switchboards in the same room, so a fire or flood takes both.
- A normally-closed bus tie between the A and B LV boards — now a fault on A
  propagates to B, and the fault level on each board doubles.
- Both UPS systems' control/monitoring on one PLC or one network switch.
- Both paths' DC control supplies from a single battery charger.
- Cable containment for both paths in one tray, or through one fire compartment.
- A single-corded server plugged into one path only.
- Both paths' generators sharing one day tank, one fuel polishing skid, or one
  fuel transfer pump.
- Both paths' earthing relying on a single MEN connection point.

Every one of those has caused a real data centre outage somewhere. The discipline
of 2N design is not drawing two of everything. It is **hunting for the thing that
is still one of.**

### Explain Like I'm 10

Imagine a hospital that needs food delivered every day. Someone builds two
completely separate roads to it. Each road is wide enough to carry all the food
the hospital needs — not half of it, all of it. If one road closes for repairs, or
a truck crashes on it, or it floods, the other road keeps every single meal
arriving on time. Nobody in the hospital even notices.

That's 2N. Two complete, separate roads, each able to do the whole job by itself.

But here's the part that catches people out. What if both roads start at the same
roundabout? Then when that one roundabout is dug up, both your roads are useless
at the same time, and you never noticed because the map showed two roads. Good
engineers spend most of their time hunting for the roundabout.

### Practical Data Centre Example (our design)

Our point of divergence is the **utility supply itself** — two separate 11 kV
feeders from two different zone substations. From that point forward, nothing is
shared in the critical power path:

```
              PATH A                                   PATH B
   11 kV feeder from Zone Sub 1            11 kV feeder from Zone Sub 2
              |                                          |
      MV Switchroom A                            MV Switchroom B
   (separate fire compartment)              (separate fire compartment)
              |                                          |
    TX-A1 2500kVA  TX-A2 2500kVA            TX-B1 2500kVA  TX-B2 2500kVA
              |                                          |
      MSB-A (bus-sectioned)                    MSB-B (bus-sectioned)
       GEN-A1, GEN-A2 (2400kW)                  GEN-B1, GEN-B2 (2400kW)
              |                                          |
      UPS-A (2 x 1250 kW)                      UPS-B (2 x 1250 kW)
       + independent battery                    + independent battery
              |                                          |
        UOB-A -> RPP-A                           UOB-B -> RPP-B
              |                                          |
     Rack PDU A ------> DUAL-CORDED SERVER <------ Rack PDU B
```

**The one shared element in our whole design is the IT equipment itself.** That is
unavoidable and correct — the server is the point where the two paths are
*supposed* to meet, because the server's dual power supplies are what make the
two paths useful.

Deliberate decisions we have made to protect independence, each recorded in the
Design Decision Register:

- **Normally-open, interlocked MV bus tie** between MV-A and MV-B. Provided for
  maintenance flexibility only. Under normal operation it is open, so the two
  paths are electrically independent. If we made it normally closed we would have
  a single MV bus and no 2N at the intake.
- **Normally-open LV bus couplers** within MSB-A and MSB-B. Keeps the two
  transformers on each side from paralleling — which also keeps the prospective
  LV fault level at ~58 kA instead of ~116 kA.
- **Separate fire compartments** for MV-A/MV-B, MSB-A/MSB-B, UPS-A/UPS-B, and
  battery rooms A/B.
- **Independent DC control supplies** — separate battery and charger per path for
  protection and control power. A single DC system feeding both paths' protection
  is one of the most commonly missed common-mode failures in the industry.
- **Segregated cable routes** — Path A and Path B containment in separate risers
  and separate fire compartments. No shared tray, no shared penetration.
- **Separate fuel systems** — one bulk tank, transfer pump set and polishing skid
  per path, with a normally-closed manual cross-connect valve for operational
  flexibility only.

### Interview Connection

This is the question you will be asked, in some form, in every data centre
interview you attend. The answer that gets you the job is not the definition —
everyone can recite the definition. It is this:

*"2N means two independent systems each capable of the full load. But the way I'd
actually test a design for 2N is to ask whether I can de-energise, earth and open
one entire path with technicians working inside it, and have zero IT impact. And
then I'd go looking for the common-mode failures — a normally-closed bus tie, a
shared DC control supply, both boards in one fire compartment, a shared fuel
skid, single-corded loads. Two of something on a drawing isn't 2N. 2N is proven
by the switching sequence."*

---

## 8. What 2(N+1) means

### Engineer Explanation

**2(N+1) is two independent systems, each of which is itself N+1.** It is the
combination of path redundancy (the "2") and capacity redundancy within each path
(the "N+1").

Read the notation literally: the bracket is what one path contains, and the 2 is
how many of those paths exist. So 2(N+1) on a 2,000 kW load with 250 kW modules
means: each path needs N = 8 modules for 2,000 kW, plus 1 spare = 9 modules per
path, × 2 paths = 18 modules installed for a 2,000 kW load.

Why you would do this rather than plain 2N:

- **It preserves full capability during maintenance.** In plain 2N, when Path A's
  UPS is in maintenance bypass, Path B is carrying 100% of the load with no
  redundancy of any kind — the facility is in an N state, and any Path B fault
  drops the load. In 2(N+1), Path B is still N+1 while Path A is out, so the
  facility never drops below single-fault tolerance.
- **It shortens the exposure window.** The "2N in maintenance" state can last
  days for a UPS overhaul or battery replacement. 2(N+1) makes that window safe.

Why you would not:

- Cost. 2(N+1) typically runs 2.6–3.0× the cost of N.
- Space, weight, cooling load and electrical losses all increase.
- **Diminishing returns.** The marginal availability gain over 2N is small
  compared to the gain from N+1 to 2N. Beyond a point, human error and control
  system failures dominate the availability calculation, and adding hardware
  doesn't help — it can hurt, because complexity itself causes outages.

**Distributed redundant (sometimes "catcher" or 3M2N / N+1 distributed)** is the
third option you should know: three or more systems shared across the load such
that the loss of any one is absorbed by the others. It gets you 2N-like
resilience at closer to N+1 cost, at the price of a much more complex switching
and control scheme, and a much harder story to tell in a design review. Common in
large hyperscale builds where the capital saving across many megawatts justifies
the complexity.

### Explain Like I'm 10

Remember the two separate roads to the hospital? 2(N+1) is when each of those two
roads has an extra spare lane.

Normally you don't need the spare lane. But imagine one whole road has to close
for a week of resurfacing. Now everything is going down the other road. With plain
2N, that remaining road has no spare anything — if a truck breaks down on it
during that week, the hospital gets no food. With 2(N+1), the remaining road still
has its spare lane, so the broken-down truck gets driven around and the food still
arrives.

The cost is that you've built and paid for lanes you almost never use. Some
hospitals decide that's worth it. Others decide it isn't.

### Practical Data Centre Example (our design)

Our UPS architecture is genuinely 2(N+1), and here is the arithmetic:

| Level | Arrangement | Redundancy |
|---|---|---|
| Module | 6 × 250 kW modules per frame = 1,500 kW installed, 1,250 kW rated | **N+1** at module level |
| Frame | 2 × 1,250 kW frames per path on a parallel bus = 2,500 kW per path | N within the path for full-load takeover |
| System | 2 paths × 2,500 kW = 5,000 kW installed for a 2,000 kW load | **2N** at system level |
| Overall | | **2(N+1)** |

Loading check, which is the part a reviewer will go straight to:

| Scenario | Path A load | Path A loading | Path B load | Path B loading |
|---|---|---|---|---|
| Normal 2N operation | 1,000 kW | 40% | 1,000 kW | 40% |
| Path B in maintenance bypass | 2,000 kW | **80%** | 0 kW | — |
| Path B out, one A module failed | 2,000 kW | 80% of 2,500 kW rated, covered by +1 module | 0 kW | — |
| Path B out, one A **frame** failed | 2,000 kW into 1,250 kW | **160% — LOAD LOST** | 0 kW | — |

That last row is the honest limitation of our design and it must be written down,
not hidden. Our architecture survives *one path plus one module*. It does not
survive *one path plus one frame*. Losing a whole UPS frame while the other path
is in maintenance bypass drops the IT load.

Is that acceptable? Our position: yes, because it is a double contingency where
one of the two events is a planned, scheduled, short-duration activity that we
control and can defer, and because the mitigating operational rule is simple —
**no planned Path B outage while Path A has a frame out of service.** That rule
goes into the operating philosophy, not just into an engineer's head. Recorded as
DDR-004.

### Interview Connection

Read the notation aloud correctly — "two, of N plus one" — and explain that the
bracket describes one path. Then deliver the reason it exists: *"The real argument
for 2(N+1) over 2N is the maintenance window. In plain 2N, the moment you put one
UPS into maintenance bypass you're running the whole facility on a single path
with no redundancy, and a UPS overhaul or a battery swap can take days. 2(N+1)
means you're never below single-fault tolerance, even during that window."*

---

## 9. Redundancy versus resilience

### Engineer Explanation

These are routinely used interchangeably, including by people who should know
better. They are different concepts and confusing them produces bad designs.

**Redundancy** is a property of the *hardware topology*. It is the provision of
additional capacity or additional paths beyond what the load requires. It is
countable, it appears on a single line diagram, and it is bought with capital.

**Resilience** is a property of the *whole system's behaviour* — its ability to
continue delivering its function when subjected to disturbance, and to return to
normal afterwards. Resilience is an emergent outcome, and it depends on:

- redundancy (topology), **plus**
- **control and automation** that correctly detects and responds to events,
- **protection coordination** that isolates faults to the smallest zone,
- **operating procedures** that are written, current and actually followed,
- **competence and training** of the operations staff,
- **maintenance regime** that keeps the redundancy real rather than theoretical,
- **change management** that prevents a modification silently defeating the
  topology,
- **monitoring** that reveals when redundancy has been lost.

The relationship in one line: **redundancy is necessary but not sufficient for
resilience.**

Worked failure of this distinction — all of these are real industry outage
patterns:

| Redundancy present | Resilience absent because | Outcome |
|---|---|---|
| Full 2N topology | Both paths' protection on one DC supply; charger failed | Total loss |
| N+1 generators | Fuel never polished; all sets failed on contaminated fuel during a real outage | Total loss |
| 2N UPS | Operator opened the wrong breaker during a routine transfer, no interlock | Load lost |
| 2N distribution | 30% of installed servers were single-corded onto Path A | Partial loss on every Path A event |
| N+1 chillers | Standby chiller had been in fault for 6 weeks; no alarm to EPMS | Thermal shutdown |
| 2N everything | No one had tested the transfer under load in 3 years | Transfer failed when needed |

The uncomfortable industry statistic you should know: **human error and control
system issues cause a large share of data centre outages — a larger share than
raw equipment failure.** Adding hardware does not address those. Procedures,
interlocks, training and commissioning do. That is precisely why the commissioning
work in Weeks 7–8 of this project is not an afterthought — it is where resilience
actually comes from.

**Fragility through complexity** is the counterintuitive corollary. Each added
redundancy layer adds components, control interactions, switching states and
opportunities for human error. There is a point past which additional redundancy
*reduces* resilience. A clean, well-understood, well-documented 2N beats a baroque
distributed-redundant scheme that nobody on the operations team fully understands.

### Explain Like I'm 10

Redundancy is *having* a spare tyre in your car. Resilience is *actually getting
home* after you get a flat.

Having the spare is just the first part. You also need the jack to be in the car,
the spare to have air in it, the wheel nuts to not be rusted on, and you need to
know how to change a tyre in the rain on the side of a road. Plenty of people have
a spare tyre and still end up stranded.

Data centres are exactly the same. Lots of them have bought two of everything and
still go dark, because nobody checked the spare had air in it, or because somebody
panicked and unbolted the wrong wheel.

### Practical Data Centre Example (our design)

Redundancy items in our design (topology — countable, on the SLD):
2 utility feeders, 4 transformers, 4 generators, 2 UPS systems, 18 UPS modules,
4 chillers, 24 CRAHs, dual A/B distribution to every rack.

Resilience items in our design (behaviour — not on the SLD, and just as
important):
- Independent DC control supply per path, so no single control failure crosses paths.
- Mechanical/electrical interlocking on the MV bus tie and the utility/generator
  changeover, so a switching error cannot parallel the paths.
- Written switching sequences for all 15 operating scenarios (Week 4 deliverable).
- Selectivity study validated for **both** utility and generator source impedance
  — because generator fault current is far lower and settings that discriminate on
  utility may not discriminate on generator.
- EPMS alarm on **loss of redundancy**, not just on loss of supply. An operator
  must be told the moment the facility has silently degraded from 2N to N.
- Level 5 Integrated Systems Testing including simultaneous failures, so the
  transfer schemes are proven before the facility carries live load.
- An explicit operating rule prohibiting planned Path B outages while a Path A
  frame is out (see Topic 8).

### Interview Connection

This is a genuine differentiator question, because most candidates treat the two
words as synonyms. Say: *"Redundancy is a topology property — it's countable and
it's on the drawing. Resilience is a behavioural property of the whole system,
and it depends on the controls, the protection coordination, the procedures, the
training and the maintenance regime as much as the hardware. You can have full
2N redundancy and poor resilience — two paths' protection on a single DC supply
is 2N on paper and single-fault-vulnerable in reality. And since human error and
control issues cause more outages than equipment failure, extra hardware is often
not where the next increment of availability comes from."*

---

## 10. Concurrent maintainability

### Engineer Explanation

**Concurrent maintainability is the ability to remove any single capacity
component or distribution element from service — for planned maintenance, repair,
replacement or testing — without impacting the critical load.**

Three things must all be true, and candidates routinely address only the first:

1. **Capacity** — sufficient remaining capacity to carry the full load.
2. **Distribution path** — a path from source to load that does not traverse the
   isolated element.
3. **Safe isolation** — the element can be physically isolated, de-energised,
   proven dead, earthed and made safe for personnel to work on, *with adequate
   physical separation from adjacent live parts*.

Point 3 is where designs actually fail, and it is an equipment and layout problem
as much as a topology problem:

- A switchboard without a **removable/withdrawable device** or a dedicated
  isolation point means you cannot work on a feeder circuit breaker without
  de-energising the bus.
- A switchboard without **internal segregation** (the Form of Separation, per the
  AS/NZS 61439 series) means opening a compartment to work on one circuit exposes
  live busbar. Form 1 or 2 construction is not concurrently maintainable in
  practice; you need Form 3b or Form 4 for critical boards. *Standard/clause
  verification required for the specific Form definitions and their application.*
- No provision for **earthing and short-circuiting** means no safe work permit.
- A UPS without a **maintenance bypass** means the UPS cannot be worked on at all
  without dropping its load.
- No **test/isolation facilities** on protection CT and VT circuits means relay
  testing requires a bus outage.

The Uptime Institute associates concurrent maintainability with **Tier III**.
The critical distinction from fault tolerance is that concurrent maintainability
addresses **planned** events, where the facility is in a known, prepared state and
the outage is scheduled. It does **not** guarantee the facility survives an
*unplanned* failure occurring during that planned activity.

**The operational reality that justifies all of this:** maintenance is not
optional. Transformers need oil/thermographic testing, switchboards need
thermographic scanning and torque checks, circuit breakers need mechanism
servicing and injection testing, protection relays need secondary injection,
generators need oil, filters, coolant and load-bank runs, UPS units need capacitor
and fan replacement, batteries need impedance testing and eventual replacement.
Over a 15-year life a facility accumulates thousands of maintenance hours. If the
design cannot absorb them, the operator faces a choice between deferring
maintenance (which degrades reliability, and is how most catastrophic failures
actually begin) and taking planned outages (which breaches the SLA).

### Explain Like I'm 10

Imagine a busy highway with two lanes going the same direction. When one lane
needs new tarmac, the workers close that lane, put out cones, and all the cars
move into the other lane. Traffic keeps flowing. Nobody has to stop. That's
concurrent maintainability — you can fix part of it while it keeps doing its job.

But notice what the workers actually need. They need somewhere safe to stand.
They need a proper barrier between them and the cars, not just a painted line.
If the only thing between a worker and 100 km/h traffic is a stripe of paint,
then technically there are two lanes, but nobody can safely do the work. Plenty of
buildings are like that — they have spare equipment, but there's no safe way to
get inside it and fix anything while the rest is running.

### Practical Data Centre Example (our design)

This table is the deliverable for Week 7, but here is the preliminary assessment
so you can see what "proving it" looks like. **Every "Yes" must eventually be
backed by a written switching sequence, not an assertion.**

| Asset | Concurrently maintainable? | The mechanism that makes it true |
|---|---|---|
| Utility feeder A | Yes | Feeder B carries full site; or generators |
| MV switchboard A (whole board) | Yes | Path B carries full load; MV-B independent |
| MV circuit breaker within MV-A | Yes | Withdrawable/isolatable device required — specification item |
| Transformer TX-A1 | Yes | TX-A2 carries Path A share at 72%; bus coupler open |
| MSB-A bus section 1 | Yes | Section 2 + Path B; section coupler normally open |
| MSB-A (entire board) | Yes | Path B carries full 2,000 kW at 80% UPS loading |
| Generator GEN-A1 | Yes | Facility not on generator during planned works; GEN-A2 covers Path A share |
| UPS-A frame 1 | Yes | Frame 2 + Path B |
| UPS-A (whole system) | Yes | Via maintenance bypass, then Path B carries full load |
| UPS-A module | Yes | Hot-swappable module, N+1 within frame |
| Battery string A1 | Yes | 4 strings; 3 remaining give ~7.5 min autonomy |
| Battery system A (whole) | **Conditional** | Path A loses ride-through; Path B must be healthy. Requires a specific operational rule. |
| RPP-A | Yes | Rack PDU B carries rack; dual-corded loads only |
| Rack PDU A | Yes | Rack PDU B carries rack; dual-corded loads only |
| Single-corded IT load | **NO** | Needs rack-level STS/ATS — this is a real gap, see Topic 12 and DDR-008 |
| Protection relay on MSB-A incomer | Yes | CT/VT test-isolation links required — specification item |
| Path A DC control supply | Yes | Independent per path; Path B unaffected |
| CHW ring main section | **Conditional** | Requires sectionalising valves — mechanical interface, TQ-003 |

Note the two "NO"/"Conditional" entries that matter. **Single-corded IT equipment
is not concurrently maintainable in a pure 2N architecture.** No amount of
electrical redundancy fixes it. That is the reason STS exists, and it is why
Topic 12 and Week 5 spend real time on it.

### Interview Connection

Give the three-part test, because most candidates give only the first part:
*"Concurrent maintainability needs three things — remaining capacity, an
alternative distribution path, and the ability to safely isolate and earth the
element so people can work on it. The third one is what most designs actually
fail, and it's a switchboard construction issue: you need withdrawable devices,
Form 3b or 4 separation, earthing provisions and CT test links. A 2N single line
diagram with Form 2 boards is not concurrently maintainable, whatever the
topology says."* Then the closer: *"And I wouldn't claim a facility is
concurrently maintainable without a written switching sequence for each asset. The
claim is only as good as the sequence that proves it."*

---

## 11. Fault tolerance

### Engineer Explanation

**Fault tolerance is the ability to sustain an unplanned failure of any single
component — including during a concurrent maintenance activity — with no impact
on the critical load, and with no operator intervention required.**

Three properties distinguish it from concurrent maintainability:

1. **Unplanned.** The facility is not in a prepared state. Nobody knew it was
   coming. There is no permit, no pre-transfer checklist, no operator standing at
   the board.
2. **Automatic.** The response must be automatic. If restoring the load requires
   an operator to make a decision and throw a switch, the facility is not fault
   tolerant — because the operator may be asleep, off-site, or wrong.
3. **Fault propagation is contained.** A fault is not merely a loss of supply. It
   is an arcing short circuit with pressure, heat, ionised gas, and a protection
   operation. Fault tolerance requires that the *consequences* of a fault —
   including the compartment it destroys and the protection zone it trips — cannot
   cross into the redundant path. This drives physical separation, separate fire
   compartments, separate rooms, and separate cable routes, not just separate
   circuits.

The Uptime Institute associates fault tolerance with **Tier IV**, and Tier IV
additionally requires **compartmentalisation** and **continuous cooling** —
recognising precisely that a fault has physical consequences and that cooling must
also be fault tolerant.

**The relationship between the three concepts, which is the thing to get straight:**

```
Redundancy        -> topology only. Countable. On the drawing.
Concurrent maint. -> survives PLANNED single-asset outages.
Fault tolerance   -> survives UNPLANNED single failures, automatically,
                     INCLUDING during a planned outage.
```

Fault tolerance implies concurrent maintainability. Concurrent maintainability
does **not** imply fault tolerance. A concurrently maintainable facility running
with Path A in planned maintenance is, at that moment, single-fault-vulnerable on
Path B. A fault tolerant facility is not.

**Where fault tolerance is hardest, and it is not the power path:**

- **Continuous cooling.** When utility fails, the UPS holds the IT load
  instantly. But the chillers stop, restart on generator 15 seconds later, and
  then need time to re-establish chilled water temperature. Meanwhile the data
  hall is absorbing 2,000 kW of heat with no heat rejection. High-density halls
  can exceed IT inlet temperature limits in a few minutes. True fault tolerance
  requires CHW thermal storage, UPS-backed CRAH fans and CHW pumps, or both.
  **This is the mechanical/electrical interface that defines whether a facility is
  really Tier IV.**
- **Control systems.** A generator paralleling controller, a UPS parallel bus
  controller, or a transfer scheme PLC that serves both paths is a common-mode
  failure that no amount of power redundancy addresses.
- **The load itself.** Single-corded equipment cannot be made fault tolerant by
  the facility. It can only be mitigated.

### Explain Like I'm 10

Concurrent maintainability is being able to fix one lane of the highway while
cars use the other lane — but you knew about it in advance, you planned it, and
you put the cones out yourself.

Fault tolerance is when a bridge suddenly collapses with no warning at 3 o'clock
in the morning, and every car still gets where it's going, and nobody had to wake
up and redirect them. The system just handles it, by itself, instantly.

And the hardest version is when the bridge collapses *while* you already had the
other lane closed for resurfacing. That's the real test. A lot of systems can
handle one problem. Far fewer can handle a surprise problem happening during
planned work.

### Practical Data Centre Example (our design)

Honest preliminary assessment of our architecture. This is the kind of assessment
a Principal Engineer expects, and pretending otherwise is the fastest way to lose
credibility:

| Failure | Fault tolerant? | Why |
|---|---|---|
| Loss of one utility feeder | Yes | Other feeder + generators; automatic |
| Transformer fault on TX-A1 | Yes | Protection isolates; TX-A2 and Path B unaffected |
| Busbar fault in MSB-A | Yes | Path B carries load; separate fire compartment |
| UPS-A module failure | Yes | N+1 within frame; automatic |
| Complete UPS-A failure | Yes | Path B carries full load via dual-corded IT |
| Generator GEN-A1 fails to start during utility outage | Yes | GEN-A2 carries Path A share |
| Busbar fault in MSB-A **while Path B transformer is in maintenance** | **Conditional** | Needs analysis in Week 7. Likely survivable on remaining TX-B and generators, with mechanical load shedding. |
| UPS-A frame failure **while Path B is in maintenance bypass** | **NO** | Double contingency. Load lost. See Topic 8, DDR-004. |
| **Continuous cooling on utility loss** | **NOT YET ADDRESSED** | Open item. Our current mechanical design has chillers on generator-backed boards only. See TQ-001. |
| Single-corded IT load, Path A fault | **NO** | Inherent. Needs rack-level STS. DDR-008. |

**Our position, stated plainly: this design is concurrently maintainable
throughout, and fault tolerant for all single failures with the facility in its
normal state. It is not fully fault tolerant during concurrent maintenance
activities, and continuous cooling is an unresolved open item.** That is
approximately a Tier III topology with some Tier IV characteristics. We will not
describe it as Tier IV, and we will not describe it as certified anything.

Being able to state that precisely, including the gaps, is worth more in an
interview than claiming Tier IV and being unable to defend the continuous cooling
question.

### Interview Connection

The question is almost always *"what's the difference between concurrent
maintainability and fault tolerance?"* The strong answer: *"Concurrent
maintainability is about planned outages — you know it's coming, it's prepared,
and an operator can be part of the sequence. Fault tolerance is about unplanned
failures, the response has to be automatic, and critically it has to hold up
during a concurrent maintenance activity. Fault tolerance also means the physical
consequences of a fault can't cross into the other path, so it drives separate
fire compartments and separate rooms, not just separate circuits."*

Then the follow-up you should volunteer, because it shows sector experience:
*"And in my experience the hardest part of fault tolerance isn't the power path at
all — it's continuous cooling. The UPS carries the IT load through a utility
failure instantly, but the chillers stop and take time to recover chilled water
temperature, and a dense hall heats up fast. So fault tolerance usually comes down
to whether you've got thermal storage or UPS-backed pumps and CRAH fans."*

---

## 12. The complete utility-to-server power chain

### Engineer Explanation

Every element, what it does, and why it is there. This is the spine of the whole
project.

```
 STAGE  ELEMENT                        FUNCTION                                        TYPICAL AUS RATING
 -----  -----------------------------  ----------------------------------------------  ------------------
   1    Utility network / zone sub     Bulk energy source                              11 kV or 22 kV
   2    HV metering & protection       Revenue metering; network interface protection   11 kV
   3    MV switchgear                  Switching, isolation, protection of TX feeders   11 kV, 630-1250 A
   4    Distribution transformer       Step down MV to usable LV; galvanic separation   11 kV / 415 V
   5    LV main switchboard (MSB)      Consolidate sources; distribute; protect         415 V, up to ~6000 A
   6    Generator + gen switchboard    Standby energy source when utility is absent     415 V
   7    Utility/generator changeover   Select live source; prevent back-feed            ACB pair, interlocked
   8    UPS input board                Feed UPS rectifier + bypass line                 415 V
   9    UPS (rectifier/inverter)       Remove all supply disturbance; provide           415 V in / 415 V out
                                       ride-through from stored energy
  10    Battery / energy storage       Stores the ride-through energy                  DC
  11    UPS static bypass              Instant transfer to raw supply on UPS fault     < 1/4 cycle
  12    UPS maintenance bypass         Manual isolation of UPS for work                Manual, interlocked
  13    UPS output board (UOB)         Distribute UPS output                           415 V
  14    STS (where required)           Selects A or B for SINGLE-corded loads          4-8 ms
  15    PDU / RPP                      Final subdistribution to racks                  415/240 V, 250-400 A
  16    Rack PDU                       Outlets at the rack; metering; switching        32 A 1-ph or 3-ph
  17    IT equipment PSU               Converts AC to the DC the electronics use       Dual PSU
```

**Australian-specific point that matters and that most online material gets
wrong:** In North America, a "PDU" is typically a **transformer-based** unit,
because the building distributes at 480 V and IT equipment needs 208/120 V, so a
step-down transformer is required at the floor. **In Australia we distribute at
415/240 V, which IT equipment accepts directly.** So our "PDU" is a
**distribution board**, not a transformer. This has real consequences: no floor
PDU transformer losses, no floor PDU as a separate failure point, no additional
earthing reference to manage — but also no local isolation transformer to limit
fault current or block common-mode noise. If you use American terminology
uncritically in an Australian design review, someone will notice.

**Where the load is "critical" versus not** — the tiering that drives the whole
design:

| Tier | Loads | Supplied from |
|---|---|---|
| **UPS-backed critical** | IT equipment, network, MMR, DC control supplies, EPMS/BMS head end, and (design decision) CHW pumps + CRAH fans | Downstream of UPS |
| **Generator-backed essential** | Chillers, condenser fans, fuel transfer, fire pumps, essential lighting, lifts (fire mode) | MSB, generator-backed, not on UPS |
| **Utility-only non-essential** | Offices, general power, workshop, landscape, car park, amenities | Non-essential board, shed on generator |

The third row is a genuine engineering decision, not an afterthought: loads you
deliberately **do not** back up, so that generator capacity is not consumed by
things that do not matter during an outage. Automatic load shedding of
non-essential boards on generator transfer is a standard feature and should be
designed in explicitly.

**Cumulative efficiency** — a point people forget when sizing:

```
Transformer    ~99.0%
UPS            ~96.0%   (double conversion, ~40% load)
Cable/dist.    ~99.0%
------------------------------------------
Chain          ~94.1%  -> to deliver 2,000 kW at the rack,
                          ~2,125 kW enters the transformer
```

**Voltage and current scaling** — the reason the physical design looks the way it
does:

| Point | Power | Voltage | Current |
|---|---|---|---|
| Utility intake (per feeder) | 3,647 kVA | 11,000 V | **191 A** |
| Transformer LV terminals | 2,500 kVA | 415 V | **3,478 A** |
| UPS output, full path load | 2,000 kW | 415 V | **2,783 A** |
| RPP feeder | 288 kVA | 415 V | 400 A |
| Rack PDU | 8 kW | 240 V | 33 A |

Read those numbers again. **191 A at the intake, 3,478 A at the transformer
terminals.** Eighteen times the current for the same power, because the voltage
dropped by a factor of 26. This single fact dictates:

- LV connections at that current are **busbar or busduct**, not cable.
- Transformers must be located **immediately adjacent** to the switchboards,
  because LV runs at 3,478 A are physically enormous and volt-drop-limited.
- Switchroom location relative to data halls is an **electrical** decision driven
  by LV feeder length, not an architectural convenience.
- Prospective fault current at the LV board is very high (~58 kA per
  transformer), setting switchboard short-circuit withstand ratings and driving
  arc-flash risk.

This is why you will see experienced data centre engineers arguing hard about
building layout early. They are not being territorial. They are trying to avoid
500 metres of 3,500 A busduct.

### Explain Like I'm 10

Think of electricity as water, and the data centre as a city's water system.

The utility is a huge river. The transformer is like a big pressure-reducing
station that takes that enormous, dangerous pressure and turns it into normal
household pressure you can actually use. The main switchboard is the big junction
where all the pipes meet and where all the taps and safety valves live. The
generator is a giant emergency pump that switches on if the river dries up — but
it takes about fifteen seconds to get going. The UPS is a water tank sitting on
the roof, always full, that keeps water flowing during those fifteen seconds so
nobody in the city ever sees their tap splutter. Then the pipes get smaller and
smaller — big mains, then street pipes, then the pipe into your house, then your
actual tap. The tap is the rack PDU, and the computer is the person drinking.

The surprising part is this: near the river, the pipes are actually quite small,
because the pressure is so high. Close to the houses, where the pressure is low,
the pipes have to be enormous to move the same amount of water. That's exactly
what happens with electricity — 191 amps at the high-voltage end becomes 3,478
amps at the low-voltage end for the same amount of power. It's why the big
transformers have to sit right next to the switchboards, and why where you put the
electrical rooms in the building is one of the first and most important decisions
anyone makes.

### Practical Data Centre Example (our design)

Our complete chain, both paths, with preliminary ratings — this is the skeleton of
the single line diagram we develop in Week 2:

```
PATH A                                                      PATH B
======                                                      ======
11 kV Zone Substation 1                        11 kV Zone Substation 2
      |                                                           |
[HV metering + network protection]              [HV metering + network protection]
      |                                                           |
+-------------------+                                +-------------------+
|  MV-A  11 kV      |====== NO interlocked tie ======|  MV-B  11 kV      |
|  Fire comp. 1     |         (normally OPEN)        |  Fire comp. 2     |
+-------------------+                                +-------------------+
   |            |                                       |            |
 TX-A1        TX-A2                                   TX-B1        TX-B2
 2500kVA      2500kVA                                 2500kVA      2500kVA
 11kV/415V    11kV/415V                               11kV/415V    11kV/415V
 Dyn11 6%Z    Dyn11 6%Z                               Dyn11 6%Z    Dyn11 6%Z
   |            |                                       |            |
+-----------------------+                       +-----------------------+
| MSB-A   415V  65kA    |                       | MSB-B   415V  65kA    |
| Sect.1 | NO | Sect.2  |                       | Sect.1 | NO | Sect.2  |
+-----------------------+                       +-----------------------+
   |  ^                                                  |  ^
   |  | interlocked ACB pair                             |  | interlocked ACB pair
   |  |                                                  |  |
   |  +---- GSB-A ----+                                  |  +---- GSB-B ----+
   |       GEN-A1 2400kW                                 |       GEN-B1 2400kW
   |       GEN-A2 2400kW                                 |       GEN-B2 2400kW
   |       (paralleled, 4-pole switching)                 |       (paralleled)
   |                                                      |
   +--> Mech Board A (chillers 1,3 / pumps / CRAHs odd)   +--> Mech Board B (chillers 2,4 / pumps / CRAHs even)
   +--> House Board A (essential)                         +--> House Board B (essential)
   +--> Non-essential Board (shed on gen)                 |
   |                                                      |
+----------------------+                        +----------------------+
| UPS-A  2 x 1250 kW   |                        | UPS-B  2 x 1250 kW   |
| 6 x 250kW modules ea |                        | 6 x 250kW modules ea |
| Static + maint bypass|                        | Static + maint bypass|
| Battery A: 480 kWh   |                        | Battery B: 480 kWh   |
| 4 strings, 10 min    |                        | 4 strings, 10 min    |
| Fire comp. 3         |                        | Fire comp. 4         |
+----------------------+                        +----------------------+
   |                                                      |
 UOB-A  415V                                            UOB-B  415V
   |                                                      |
 RPP-A1..A4 (Hall 1)   RPP-A5..A8 (Hall 2)              RPP-B1..B4 (Hall 1)   RPP-B5..B8 (Hall 2)
 400A TP&N each                                          400A TP&N each
   |                                                      |
 Rack PDU A (32A)                                       Rack PDU B (32A)
   |                                                      |
   +---------------> DUAL-CORDED IT EQUIPMENT <-----------+
                     250 racks, 8 kW avg

   SINGLE-CORDED LOADS (assumed 5% = 100 kW):
   Rack PDU A ----+
                  +--> rack-level STS/ATS --> single-corded device
   Rack PDU B ----+
```

### Interview Connection

You should be able to draw this chain on a whiteboard from memory, name every
stage, and state what each stage protects against. Then add the two points that
demonstrate you have thought about it rather than memorised it:

1. *"The current scaling is what drives the building layout — 191 A at 11 kV
   becomes 3,478 A at 415 V, so the transformers have to be right next to the
   switchboards and the switchrooms have to be close to the halls."*
2. *"In Australia we distribute at 415/240 V so we don't need transformer-based
   PDUs the way a US design does — our PDU is a distribution board. That removes a
   failure point and some losses, but it also means no local isolation
   transformer, so fault current management is all upstream."*

---

## Understanding checks

Answer these before reading `docs/02-basis-of-design.md`. Write your answers
down; we will mark them.

**Simple check 1.** If Power Path A disappears completely, what keeps the servers
running, and what physical feature of the servers makes that possible?

**Simple check 2.** Our computers use 2 MW. Why does the whole building use about
3.5 MW? Where does the extra 1.5 MW go, and does any of it reach a computer?

**Engineering check 1.** Explain the downstream consequences of placing UPS-A into
maintenance bypass for a battery replacement. Identify every load that loses true
2N redundancy during that activity, state the loading on Path B, and name the one
additional failure that would drop IT load.

**Engineering check 2.** Our two 2,500 kVA transformers per side have a bus
coupler between their LV sections that is normally **open**. Give two independent
engineering reasons for that, one of which must be quantified.

**Engineering check 3.** A colleague proposes deleting one generator per side
(going from 4 to 2 generators total, one per side) on the grounds that "each
generator is sized for the full facility load anyway, and we have 2N". Identify
what capability is lost. Is the proposal acceptable? Defend your position.
