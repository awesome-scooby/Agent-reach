# Data Centre Electrical Glossary

> SELF-DIRECTED ENGINEERING PROJECT — NOT A COMMISSIONED CLIENT DESIGN

**Document:** DC2MW-EL-GLOS-001 — **live document, extended each week**

Format for every term: engineer definition, 10-year-old definition, why it matters
to this project.

---

### Term: MV (Medium Voltage)

**Engineer definition:** Voltages above low voltage and below high voltage. In
Australian practice, distribution at 11 kV and 22 kV is conventionally called MV,
though AS/NZS terminology formally uses "low voltage" (≤1,000 V AC) and "high
voltage" (>1,000 V AC), with AS/NZS 2067 covering installations above 1 kV. MV is
industry usage, not a standards-defined band in AS/NZS. *Clause verification
required before citing a formal definition.*

**10-year-old definition:** The really strong electricity that travels along the
big wires between suburbs. Too strong to plug anything into — it has to be turned
down first.

**Why it matters:** Our intake is 11 kV. MV lets us move 3.6 MVA with only 191 A
of current, which is why the incoming cables are manageable in size.

---

### Term: LV (Low Voltage)

**Engineer definition:** Up to and including 1,000 V AC. In Australia,
415 V 3-phase / 240 V single phase, 50 Hz. Governed by AS/NZS 3000.

**10-year-old definition:** Normal electricity — the kind in the plugs at your
house, strong enough to run things but turned down enough to be usable.

**Why it matters:** Everything from the transformer onward is LV. LV is where the
currents get enormous (3,478 A per transformer), which drives busbar, room
layout and fault level decisions.

---

### Term: N

**Engineer definition:** The capacity required to serve the design load with no
redundancy. A quantity of capability, not a count of units.

**10-year-old definition:** Exactly enough, with nothing spare.

**Why it matters:** Our generators are N per path. Understanding that N means
"capability" not "one unit" prevents the most common redundancy error.

---

### Term: N+1

**Engineer definition:** The required capacity plus one additional unit at least
as large as the largest unit it must cover. Tolerates loss of any one unit.
Provides capacity redundancy, not path redundancy.

**10-year-old definition:** Exactly enough, plus one spare.

**Why it matters:** Our chillers, CRAHs and UPS modules are N+1. The limitation —
that a shared bus or shared controller makes an N+1 set of units into an N
system — is the single most important caveat to remember.

---

### Term: 2N

**Engineer definition:** Two complete, independent systems, each individually
capable of the full design load, sharing no element upstream of the load.

**10-year-old definition:** Two completely separate roads to the same place, each
big enough to carry everything by itself.

**Why it matters:** This is the project's given requirement. Proving it means
hunting for the element that is still shared, not counting the elements that are
duplicated.

---

### Term: 2(N+1)

**Engineer definition:** Two independent systems, each of which is itself N+1.
The bracket describes the contents of one path.

**10-year-old definition:** Two separate roads, and each road has a spare lane.

**Why it matters:** Our UPS architecture. Its value is that during a UPS
maintenance window the remaining path is still single-fault tolerant, instead of
running with no redundancy at all.

---

### Term: UPS (Uninterruptible Power Supply)

**Engineer definition:** A device that converts incoming AC to DC (rectifier),
maintains a DC bus supported by energy storage, and reconverts to AC (inverter) to
supply the load. In double-conversion (on-line) mode the load is always supplied by
the inverter, so the load never sees an input disturbance and transfer time on
supply loss is zero. Includes a static bypass for instant transfer to raw supply on
internal fault, and a maintenance bypass for manual isolation.

**10-year-old definition:** A very big battery that is also an electricity
cleaner and a traffic controller. The computers never actually drink the
electricity from the street — they drink it from the UPS, and the UPS is always
topping itself up from the street. So when the street supply disappears, the
computers don't notice anything at all, because nothing about their drink changed.

**Why it matters:** The UPS closes the ~15 second gap between utility loss and
generator availability. Our servers ride through only 10–20 ms on their own. The
UPS is the only reason a generator-backed facility works.

---

### Term: Static bypass

**Engineer definition:** A thyristor-based path within the UPS that transfers the
load from the inverter to the raw bypass supply automatically, typically in under a
quarter cycle (≈5 ms at 50 Hz), on inverter fault or overload. The load is then
unprotected but still supplied.

**10-year-old definition:** An emergency escape hatch inside the UPS. If the UPS
itself breaks, the hatch opens in a few thousandths of a second and the computers
go straight back to drinking from the street. Not as clean, but much better than
nothing.

**Why it matters:** It converts "UPS failure" from "load lost" into "load
unprotected". In our 2N design the load is still protected by the other path, so
static bypass is a second layer, not the primary one.

---

### Term: Maintenance bypass

**Engineer definition:** A manually operated, mechanically and electrically
interlocked path that allows the entire UPS — including its static switch — to be
isolated and de-energised while the load continues to be supplied from raw mains.
The interlock exists to prevent paralleling the inverter output with the bypass
source out of synchronism.

**10-year-old definition:** A way to completely unplug the UPS and put it on a
workbench, while the computers keep running straight off the street supply in the
meantime.

**Why it matters:** Without it, a UPS can never be maintained without dropping its
load, and the facility is not concurrently maintainable. It is the single feature
that makes UPS maintenance possible.

---

### Term: ATS (Automatic Transfer Switch)

**Engineer definition:** A device that automatically transfers a load between two
AC sources based on source availability. Mechanically operated, so transfer time is
in the range of hundreds of milliseconds to several seconds. May be open transition
(break-before-make) or closed transition (make-before-break, requiring
synchronism).

**10-year-old definition:** A switch that notices the electricity has gone and
flips over to the backup by itself. It takes about a second — fast for a person,
far too slow for a computer.

**Why it matters:** Our utility/generator changeover is effectively an ATS
function, implemented as an interlocked 4-pole ACB pair. Its transfer time is why
mechanical plant restarts and the UPS must carry the IT load through the gap.

---

### Term: STS (Static Transfer Switch)

**Engineer definition:** A thyristor-based device that transfers a load between two
independent AC sources in a quarter to half cycle (≈4–8 ms), fast enough that IT
power supplies ride through the transfer. Requires both sources to be within
acceptable phase and voltage tolerance. Used to give a single-corded load the
benefit of a dual-path supply.

**10-year-old definition:** Like the switch above, but electronic instead of
mechanical, so it flips over in about four thousandths of a second — fast enough
that a computer with only one plug never notices.

**Why it matters:** Our only solution for single-corded IT equipment. Critically,
an STS is a device that **both** paths pass through, so it is a deliberate,
documented exception to our no-shared-element rule — which is exactly why we chose
many small rack-level units over one large facility-level unit.

---

### Term: PDU (Power Distribution Unit)

**Engineer definition:** Regionally ambiguous. In North America, typically a
floor-standing unit containing a step-down isolation transformer (480 V to
208/120 V) plus distribution. In Australia, where LV is already 415/240 V and IT
equipment accepts it directly, no step-down is needed, so "PDU" in an Australian
data centre generally means a distribution board.

**10-year-old definition:** The box on the data hall floor where one big cable
comes in and lots of smaller cables go out to the computer cabinets.

**Why it matters:** Our design has no transformer PDUs — that removes a failure
point and its losses, but also removes a local isolation transformer, so all
fault-current management is upstream. Using US terminology in an Australian
review will get noticed.

---

### Term: RPP (Remote Power Panel)

**Engineer definition:** A distribution board located on or near the data hall
floor, fed from the UPS output board, providing final subcircuits to rack PDUs.
Typically with per-circuit metering and monitoring.

**10-year-old definition:** A smaller fuse box out on the computer room floor,
close to the cabinets, so the cables to each cabinet are short.

**Why it matters:** 16 of them in our design (8 A, 8 B). Sizing each for full
takeover load rather than normal load is the 2N discipline applied at the
distribution level.

---

### Term: Rack PDU

**Engineer definition:** A vertical or horizontal power strip within the rack,
providing outlets to IT equipment, commonly with per-outlet metering, remote
switching and environmental monitoring. Two per rack in a 2N design, each sized for
100% of the rack load.

**10-year-old definition:** The powerboard inside the computer cabinet that all the
computers plug into.

**Why it matters:** The last electrical device we own before the IT equipment. Each
must carry the full rack load, not half — because the other one may be absent.

---

### Term: Dual-corded load

**Engineer definition:** IT equipment with two independent power supply units, each
capable of supporting the full equipment load, connected to two independent supply
paths. Under normal conditions the PSUs share the load; on loss of one supply the
remaining PSU assumes the full load with no interruption.

**10-year-old definition:** A machine with two power cords that can drink from two
different pipes at once. If one pipe stops, it just keeps drinking from the other
and doesn't even hiccup.

**Why it matters:** The entire justification for 2N. Without dual-corded loads, two
independent paths deliver no benefit to the IT equipment.

---

### Term: Single-corded load

**Engineer definition:** Equipment with one power input, incapable of connecting to
two paths. Common in network appliances, legacy equipment, KVM devices and some
storage controllers. Requires an STS or ATS at rack level to obtain dual-path
benefit.

**10-year-old definition:** A machine with only one power cord. It can only drink
from one pipe, so if that pipe stops, it stops — unless you put a very fast switch
in front of it.

**Why it matters:** Our assumed 5% (100 kW) is the one part of the IT load that is
**not** inherently concurrently maintainable. It is the biggest hole in an
otherwise clean 2N design, and it is almost always worse than assumed on real
projects.

---

### Term: CRAC (Computer Room Air Conditioner)

**Engineer definition:** A direct-expansion (DX) precision air conditioning unit
with an integral refrigeration circuit, serving a data hall. Self-contained,
requiring a condenser but no chilled water plant.

**10-year-old definition:** A big air conditioner that sits in the computer room
and makes its own cold air, like a household split system but much bigger and
built to run every second of every year.

**Why it matters:** Not used in our design — we selected chilled water. Know the
distinction because interviewers use the terms loosely and correcting them
politely demonstrates competence.

---

### Term: CRAH (Computer Room Air Handler)

**Engineer definition:** An air handling unit serving a data hall with a chilled
water cooling coil and (typically EC) fans, but no integral refrigeration. Relies
on a central chilled water plant. Generally more efficient at scale than CRAC and
allows plant-level N+1 redundancy.

**10-year-old definition:** A big fan-and-radiator box in the computer room. It
doesn't make the cold itself — cold water is piped to it from the chillers
outside, and it blows air across that cold water.

**Why it matters:** 24 units in our design, 8 kW fan power each, 170 kW total.
Whether their fans sit on UPS or on generator-only is the central question in the
continuous cooling issue, TQ-001.

---

### Term: EPMS (Electrical Power Monitoring System)

**Engineer definition:** A dedicated system monitoring electrical parameters
across the distribution system — power, energy, power quality, harmonics, breaker
status, protection events, alarms — usually via Modbus/IEC 61850 from meters,
relays, UPS and generator controllers. Provides operational visibility, event
forensics and capacity management.

**10-year-old definition:** A big screen in the control room that shows exactly
how much electricity is flowing everywhere in the building, and lights up when
anything is wrong.

**Why it matters:** The EPMS is how an operator knows the facility has silently
degraded from 2N to N. Alarming on **loss of redundancy**, not just loss of
supply, is a specific design requirement in our resilience philosophy.

---

### Term: BMS (Building Management System)

**Engineer definition:** The control and monitoring system for mechanical and
building services — chillers, pumps, CRAHs, valves, dampers, temperature and
humidity, lighting, and generator ancillaries. Sequences plant and manages
setpoints.

**10-year-old definition:** The brain that controls all the cooling and the
building's machinery, and decides when to turn each thing on.

**Why it matters:** The BMS sequences chiller restart after a generator transfer.
That sequence is an electrical concern, because an unsequenced simultaneous chiller
restart is a large step load on a generator.

---

### Term: Concurrent maintainability

**Engineer definition:** The ability to remove any single capacity component or
distribution element from service for planned work without impacting the critical
load. Requires remaining capacity, an alternative distribution path, **and** the
ability to safely isolate, prove dead and earth the element.

**10-year-old definition:** Being able to repair one lane of a highway while cars
keep driving in the other lane — and the workers have a proper barrier to stand
behind, not just a painted line.

**Why it matters:** It is the property our maintainability philosophy exists to
deliver, and the third requirement (safe isolation) is a switchboard specification
issue that topology alone does not solve.

---

### Term: Fault tolerance

**Engineer definition:** The ability to sustain an unplanned single component
failure with no critical load impact, automatically, including during a concurrent
maintenance activity. Requires that fault consequences — physical as well as
electrical — cannot propagate into the redundant path.

**10-year-old definition:** A bridge collapses with no warning at 3 a.m. and every
car still gets home, and nobody had to wake up and fix anything.

**Why it matters:** Our design is fault tolerant in its normal state but not during
all maintenance activities. We state that precisely rather than claiming Tier IV.

---

### Term: Redundancy

**Engineer definition:** A topology property — the provision of capacity or paths
in excess of load requirements. Countable, visible on a single line diagram,
purchased with capital.

**10-year-old definition:** Having a spare.

**Why it matters:** Necessary but not sufficient. Confusing it with resilience is
the most common conceptual error in the sector.

---

### Term: Resilience

**Engineer definition:** An emergent system property — the ability to continue
delivering function under disturbance and recover afterwards. Depends on
redundancy plus controls, protection coordination, procedures, training,
maintenance regime, change management and monitoring.

**10-year-old definition:** Actually getting home after the flat tyre — not just
owning a spare.

**Why it matters:** Human error and control system failures cause more outages than
equipment failure. Resilience, not redundancy, is where the last increment of
availability comes from. This is why commissioning matters.

---

### Term: Selectivity (discrimination)

**Engineer definition:** The property of a protection scheme whereby, for a fault
anywhere in the system, only the protective device immediately upstream of the
fault operates, leaving all other devices closed and all other load in service.
Achieved through current grading, time grading, zone interlocking, energy-based
(current-limiting) discrimination, or a combination.

**10-year-old definition:** Imagine every room in your house has its own little
safety switch, and there's one big one at the front door. If your toaster catches
fire in the kitchen, you want *only* the kitchen switch to trip — not the big one
at the front door that turns off the whole house. Getting the switches to
cooperate like that is selectivity.

**Why it matters:** A fault on one RPP circuit must not trip the UPS output
breaker. In a 2N facility a selectivity failure can escalate one rack's fault into
a whole-path outage.

---

### Term: Synchronisation

**Engineer definition:** Matching voltage magnitude, frequency, phase sequence and
phase angle between two AC sources before connecting them, within defined limits,
verified by a synchronising check relay (ANSI 25). Closing out of synchronism
produces very large transient torques and currents and can destroy an alternator.

**10-year-old definition:** Two people turning a skipping rope have to swing their
arms at exactly the same speed and at exactly the same moment, or the rope gets
yanked out of someone's hands. Two generators joining together have to match up the
same way, and a special device checks before letting them connect.

**Why it matters:** Our two generators per path parallel onto a common generator
switchboard, so synchronising is required. If we choose closed-transition
retransfer to utility (DDR-015), synchronising to the utility is also required,
with DNSP implications.

---

### Term: Paralleling

**Engineer definition:** Operating two or more generators in parallel onto a common
bus, sharing real power (via governor/isochronous load sharing) and reactive power
(via AVR cross-current compensation or droop). Requires synchronisation to connect
and continuous load sharing control to remain stable.

**10-year-old definition:** Getting two engines to pull the same cart together
without fighting each other, so they each do a fair share of the work.

**Why it matters:** 2 × 2,400 kW per path paralleled onto GSB-A / GSB-B. The
paralleling controller is a potential common-mode element within a path and must be
identified as such.

---

### Term: Black start

**Engineer definition:** Restoring a completely de-energised facility from zero
energised infrastructure — no utility, no generator running, no UPS output, and
only stored energy (generator start batteries, DC control batteries) available. It
tests the dependency chain: does starting the generator require control power, and
does that control power require the generator?

**10-year-old definition:** Everything in the building is completely off — no
power anywhere at all — and you have to get it all going again from nothing, one
piece at a time, in the right order.

**Why it matters:** Black start exposes circular dependencies. If the generator's
control power comes from a charger fed by a board the generator has to energise,
the facility cannot black start. Our Week 4 operating scenario 15 tests this
explicitly.

---

### Term: PUE (Power Usage Effectiveness)

**Engineer definition:** Total facility energy divided by IT equipment energy,
defined in the ISO/IEC 30134 series. An **annualised energy** ratio (kWh/kWh), not
an instantaneous power ratio. Design-day PUE is always worse than annualised PUE.

**10-year-old definition:** If the pizza costs $10 and delivery costs $4, you spent
$1.40 for every $1 of pizza. That's 1.4.

**Why it matters:** Our design-day PUE is 1.73 and our assumed annualised PUE is
1.40. **Neither is used to size electrical equipment** — that comes from the
mechanical load calculation.

---

### Term: Wet stacking

**Engineer definition:** Incomplete combustion in a diesel engine operated at
sustained low load, causing unburnt fuel and carbon to accumulate in the exhaust
system, degrading performance, fouling turbochargers and injectors, and eventually
requiring intervention. Generally avoided by keeping load above roughly 30% and
periodically load-banking.

**10-year-old definition:** A big diesel engine that never works hard gets clogged
up and dirty inside, like a fireplace that never burns hot enough and fills up with
soot.

**Why it matters:** Our generators run at only 36% when both sets are online in
normal split operation. This drives a generator loading strategy — run one set per
path and start the second on demand — which is a controls requirement, TQ-009.

---

### Term: Form of separation

**Engineer definition:** The degree of internal subdivision within a switchboard
assembly, classified in the AS/NZS 61439 series, describing separation between
busbars, functional units and terminals. Higher forms (3b, 4) allow work on one
functional unit without exposure to live parts of others. *Clause verification
required for the specific form definitions.*

**10-year-old definition:** Whether the inside of the big electrical cupboard has
proper walls between each section, or is just one open space. With walls, you can
safely work in one section while the others are still switched on.

**Why it matters:** Form 4 on critical boards is what makes concurrent
maintainability physically possible. A 2N topology in Form 2 boards is not
concurrently maintainable, whatever the SLD shows.

---

### Term: Open transition / closed transition

**Engineer definition:** Open transition (break-before-make) disconnects the load
from the first source before connecting the second, producing a brief interruption
of typically 100 ms to several seconds. Closed transition (make-before-break)
briefly parallels the two sources, requiring synchronism, and produces no
interruption.

**10-year-old definition:** Open transition is letting go of one rope before
grabbing the next one — there's a moment where you're holding nothing. Closed
transition is grabbing the second rope before letting go of the first, so you're
never holding nothing. The second way is better, but you have to be careful that
both ropes are moving the same way.

**Why it matters:** DDR-015, unresolved. Closed transition on retransfer avoids a
UPS battery discharge every time we come off generator, but requires synchronising
to the utility, which has DNSP network protection implications.
