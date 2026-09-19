# Interview Knowledge Bank

> SELF-DIRECTED ENGINEERING PROJECT — NOT A COMMISSIONED CLIENT DESIGN

**Document:** DC2MW-EL-IKB-001 — **live document, extended each week**

Format: question → strong answer → ELI10 → likely follow-up → the mistake
inexperienced engineers make.

---

## The framing statement (learn this first, use it once)

Say this early in any data centre interview, once, without apology:

> *"I haven't yet delivered a live data centre project. That's why I built this
> one — a 2N critical power design for a notional 2 MW IT load, with the failure
> mode analysis, the concurrent maintainability assessment and the L1–L5
> commissioning matrix. I'd rather tell you that upfront and then show you I can
> defend the engineering."*

Then stop apologising and talk like an engineer. The framing statement buys you
credibility precisely because it is honest; repeating it turns it into an excuse.

**Never** describe this project as client work, contracted work, or work you
"delivered". The approved wording is in the README.

---

## Q1. Explain 2N.

**Strong answer:** Two complete, independent systems, each individually capable of
carrying the full design load, sharing no element upstream of the load. Not two
units — two systems, each with its own source, transformation, standby generation,
uninterruptible power, distribution and controls.

But the definition isn't the useful part. The way I'd actually test a design for 2N
is to ask: can I de-energise, earth and open one entire path, with technicians
working inside it, and have zero IT impact? If the answer needs any qualification,
it isn't 2N. Then I'd go hunting for common-mode failures — a normally-closed bus
tie, a shared DC control supply, both boards in one fire compartment, a shared fuel
polishing skid, single-corded loads. Two of something on a drawing isn't 2N. 2N is
proven by the switching sequence.

**ELI10:** Two completely separate roads to the hospital, each wide enough to carry
all the food by itself. But you have to check they don't both start at the same
roundabout.

**Likely follow-up:** *"So what's the one place your 2N design shares an element?"*
→ The IT equipment itself, which is the intended convergence point, and the
rack-level STS serving single-corded loads, which is a deliberate documented
exception.

**Common mistake:** Reciting the definition and stopping. Everyone can recite it.
The differentiator is volunteering the test and the common-mode hunt.

---

## Q2. What's the difference between N+1 and 2N?

**Strong answer:** N+1 is capacity redundancy — enough capability for the load plus
one spare unit. 2N is capacity *and* path redundancy — two complete independent
systems. The critical distinction is that in N+1, the units usually share a
busbar, a controller, or a room. That shared element is a single point of failure,
so the system is N+1 for the units and N for the system. N+1 chillers on a single
non-sectionalised chilled water ring is not N+1 cooling.

The other difference is what they protect against. N+1 protects against a unit
failing. 2N additionally protects against busbar faults, switchboard fires, control
system failures, protection maloperation, human switching error, and planned
maintenance on any asset.

**ELI10:** N+1 is bringing a spare bus. 2N is having two completely separate roads.
The spare bus doesn't help if someone parks a truck across the only gate.

**Likely follow-up:** *"Where would you use N+1 rather than 2N?"* → Capacity plant
outside the critical path: chillers, pumps, CRAHs, and modules inside a UPS frame.
Cooling has thermal inertia, so it doesn't need instantaneous redundancy the way
the power path does.

**Common mistake:** Treating it as purely a quantity difference. It's a difference
in kind — capacity versus path.

---

## Q3. Why would you use an STS?

**Strong answer:** To give a single-corded load the benefit of a dual-path supply.
An STS transfers between two independent sources in a quarter to half cycle, around
4 to 8 ms, which is inside the ride-through of an IT power supply, so the load
doesn't see the transfer.

The important part is the caveat: an STS is itself a device that both paths pass
through, so it's a common element and a single point of failure for the loads behind
it. That's a deliberate exception to the no-shared-element rule of 2N, and you make
it only because the alternative — a single-corded load on one path — is worse.
On my project I chose many small rack-level STS units over one large facility-level
unit, so one failure affects one rack rather than all single-corded load.

**ELI10:** A very fast electronic switch that flips between two water pipes in about
four thousandths of a second, so a machine with only one hose never notices which
pipe it's drinking from.

**Likely follow-up:** *"So would you allow single-corded equipment in a Tier III
facility?"* → You'd rather not, but you don't control what the client's IT team
buys. So you design the provision, you document the proportion as an assumption,
and you allow for it growing — because it always does.

**Common mistake:** Presenting the STS as a redundancy improvement without
acknowledging that it's a new single point of failure.

---

## Q4. What happens when the utility fails?

**Strong answer:** Walk the sequence:

At t=0, both feeders are lost. The UPS inverters were already supplying the IT load
in double conversion, so nothing changes at the load — the rectifiers stop drawing
from the dead supply and the DC bus is supported by the battery instead. **Zero
transfer, zero interruption**, because there was never a transfer to make.

Simultaneously, non-essential boards shed, and the generators get a start signal.
They reach rated speed, the AVR establishes stable voltage, the sync check relay
permits paralleling onto the generator switchboard, and the utility/generator
changeover transfers — call it 15 seconds. The changeover is 4-pole, so we never
have two earthed neutrals in service at once.

Then the load comes back in a controlled way: UPS rectifiers walk in over 10 to 30
seconds rather than slamming on as a step load, and chillers restart on a sequenced
ramp over 60 to 120 seconds so we don't present the generator with a simultaneous
start of three large compressors. Batteries recharge. IT load never saw an event.

And the honest part: for those 60 to 120 seconds, the data hall has 2 MW of heat
going in and much reduced heat rejection. Whether that's acceptable needs a thermal
transient analysis, and if it isn't, you put the CRAH fans and secondary CHW pumps
on the UPS. On my project that's my largest open technical issue.

**ELI10:** The street power vanished. The batteries were already doing the work, so
the computers didn't notice anything at all. The big emergency engines started up,
took about fifteen seconds to get ready, then took over the job. About a minute
later the cooling came back on properly. Nobody using the website saw a thing.

**Likely follow-up:** *"What if a generator doesn't start?"* → See Q10.

**Common mistake:** Saying "the UPS takes over" or "the UPS transfers to battery".
In double conversion there is no transfer — the inverter was already supplying the
load. Getting this right signals that you understand the topology rather than the
marketing.

---

## Q5. How does UPS bypass operate, and what's the difference between static and maintenance bypass?

**Strong answer:** Two different devices for two different purposes.

**Static bypass** is thyristor-based, automatic, and operates in under a quarter
cycle — about 5 ms at 50 Hz. It triggers on inverter fault or overload. It moves the
load from the inverter to the raw bypass supply. The load stays *supplied* but
becomes *unprotected* — no ride-through, no conditioning. It converts "UPS failure"
from "load lost" into "load exposed".

**Maintenance bypass** is manual, mechanically and electrically interlocked, and
exists so the entire UPS — including its static switch — can be isolated,
de-energised and worked on while the load runs on raw mains. The interlock is
essential: without it you could parallel the inverter output with the bypass source
out of synchronism.

The design point: without a maintenance bypass, a UPS can never be maintained
without dropping its load, so the facility is not concurrently maintainable. And
the operational point: while a UPS is on maintenance bypass in a plain 2N facility,
the other path is carrying 100% of the load with zero redundancy. That's the
argument for 2(N+1).

**ELI10:** The static bypass is an emergency escape hatch that opens by itself in a
few thousandths of a second if the UPS breaks. The maintenance bypass is a way to
completely unplug the UPS and carry it to a workbench, while the computers keep
running straight off the street in the meantime.

**Likely follow-up:** *"What's the risk when you're on bypass?"* → No ride-through.
A utility event during a bypass operation drops that path. In 2N the other path
covers it, which is why the bypass window is the moment your redundancy actually
matters.

**Common mistake:** Using the two terms interchangeably, or not knowing the static
bypass is automatic and the maintenance bypass is manual.

---

## Q6. What is concurrent maintainability?

**Strong answer:** The ability to remove any single capacity component or
distribution element from service for planned work without impacting the critical
load. It needs three things, and most candidates only give the first:

1. Remaining capacity to carry the full load.
2. An alternative distribution path that doesn't traverse the isolated element.
3. The ability to safely isolate, prove dead and earth the element so people can
   actually work on it.

The third one is what designs actually fail, and it's a switchboard construction
issue rather than a topology issue: you need withdrawable devices, Form 3b or Form 4
internal separation, earthing provisions, and CT test isolation links so a relay can
be injection-tested without a bus outage. A 2N single line diagram with Form 2
boards is not concurrently maintainable, whatever the topology says.

And I wouldn't claim a facility is concurrently maintainable without a written
switching sequence for each asset. The claim is only as good as the sequence that
proves it.

**ELI10:** Repairing one lane of the highway while cars keep using the other lane.
But the workers need a proper concrete barrier to stand behind, not just a painted
line — otherwise there are two lanes and still no safe way to do the work.

**Likely follow-up:** *"What's the one thing in your design that isn't concurrently
maintainable?"* → Single-corded IT equipment. No amount of electrical redundancy
fixes it; it needs an STS.

**Common mistake:** Answering with capacity only, and never mentioning safe
isolation or switchboard form of separation. That omission is exactly what marks
out someone who hasn't worked around a live switchroom.

---

## Q7. What's the difference between redundancy and resilience?

**Strong answer:** Redundancy is a topology property — capacity or paths beyond what
the load needs. It's countable, it's on the drawing, and you buy it with capital.
Resilience is a behavioural property of the whole system — whether it actually keeps
delivering under disturbance and recovers afterwards. Resilience depends on
redundancy plus controls, protection coordination, procedures, training, maintenance
regime, change management and monitoring.

You can have full 2N redundancy and poor resilience. Both paths' protection on a
single DC control supply is 2N on paper and single-fault-vulnerable in reality.
N+1 generators that have never had their fuel polished all fail together on
contaminated fuel during the one outage that mattered. 2N distribution with 30% of
the servers single-corded onto Path A drops load on every Path A event.

And since human error and control system issues cause more data centre outages than
raw equipment failure, extra hardware is often not where the next increment of
availability comes from. Procedures, interlocks, training and proper commissioning
are. There's even a point past which more redundancy reduces resilience, because
complexity itself causes outages — a clean 2N that the operations team fully
understands beats a baroque distributed scheme that nobody does.

**ELI10:** Redundancy is having a spare tyre. Resilience is actually getting home
after the flat. You also need the jack, air in the spare, wheel nuts that aren't
rusted on, and to know how to change a tyre in the rain.

**Likely follow-up:** *"So how would you improve resilience without adding
hardware?"* → Interlocks that make switching errors impossible; written switching
sequences for every scenario; EPMS alarms on *loss of redundancy* rather than just
loss of supply; selectivity verified for both utility and generator source
impedance; and Level 5 integrated testing including simultaneous failures.

**Common mistake:** Treating the two words as synonyms. Most candidates do.

---

## Q8. How would you commission the power chain?

**Strong answer:** Five levels, and the value is concentrated in the last two.

**L1 Factory** — FAT on switchboards, UPS and generators; type test certificates;
documentation review; equipment inspection on delivery.

**L2 Installation** — installation inspection, cable verification, torque checks,
continuity, insulation resistance, labelling, earthing verification. Static
verification, nothing energised.

**L3 Start-up / pre-functional** — energisation, breaker primary and secondary
injection, relay testing, transformer ratio and polarity, UPS start-up, generator
start-up and load bank, battery discharge verification, controls point-to-point.
Each system proven **by itself**.

**L4 Functional performance** — deliberately create the faults. Simulated utility
failure, changeover operation, UPS transfer to battery, static bypass operation,
generator start and paralleling, STS transfer, interlock verification, alarm
verification to EPMS and BMS. Each system proven **to respond correctly**.

**L5 Integrated systems testing** — everything together, at load, with the failures
stacked. Full utility outage with load banks at design load, generator failure
during the outage, UPS module failure, whole-path outage, and recovery to normal.
The whole facility proven **as one machine**.

The point I'd emphasise: L5 is where resilience is actually proven, and it's the
level clients most often compress when the programme slips. Compressing L5 means
the first real test of your transfer schemes happens with live customer load on the
floor. Also — the entire commissioning programme should be **witnessed and
documented against a matrix** with preconditions, method, expected result and pass
criteria written *before* the test, not after.

**ELI10:** First you check each part at the factory. Then you check it was installed
properly. Then you turn each thing on by itself and check it works. Then you
deliberately break things and check each system reacts correctly. Then you do one
giant rehearsal where you break several things at once and see if the whole building
copes. That last rehearsal is the one that actually tells you the truth.

**Likely follow-up:** *"What would you test in L5 that people usually skip?"* →
Simultaneous failures, black start from fully de-energised, and a generator failure
*during* a utility outage. Also load bank testing at the real design load, because
testing at 30% proves very little about thermal performance or step-load response.

**Common mistake:** Listing the five levels and stopping. The insight is that L5 is
where resilience gets proven and it's the first thing to be cut.

---

## Q9. What happens if one UPS fails?

**Strong answer:** Depends what you mean by "fails", and I'd ask that back.

**A module fails** — N+1 within the frame absorbs it, the module isolates itself,
the frame continues at reduced capacity but still above rated. No load impact, no
redundancy loss at system level. Hot-swap the module.

**A frame's inverter fails** — the static bypass operates in under a quarter cycle
and that frame's load goes to raw mains, unprotected but supplied. The other frame
in the path and the other path are unaffected.

**A whole UPS system fails** — the dual-corded IT load transfers entirely to the
other path's PSU with no interruption. Path B now carries 2,000 kW at 80% of its
2,500 kW rating. The facility is now in an N state: no redundancy, single fault
vulnerable. That's the moment the EPMS should be screaming, because the operator
needs to know the facility has degraded from 2N to N, not just that a UPS has
faulted.

And the honest limitation of my design: if a Path A *frame* fails while Path B is in
maintenance bypass, Path A has 1,250 kW available for a 2,000 kW load and the IT
load is lost. It's a double contingency where one of the two events is planned and
under my control, so the mitigation is an operational rule — no planned Path B
outage while a Path A frame is out — and that rule is written into the operating
philosophy, not left in an engineer's head.

**ELI10:** One of the two big battery systems breaks. Every computer has two plugs,
so they all just carry on using the other one and nothing goes off. But now there's
no spare left, so someone has to fix it quickly — and the control room screen should
go red to tell them the building has stopped being safe, even though nothing has
actually gone off yet.

**Likely follow-up:** *"How does the operator know redundancy has been lost?"* →
Precisely the point. The EPMS must alarm on loss of redundancy, not just loss of
supply. A facility silently running at N because a standby unit has been in fault
for six weeks is how most catastrophic failures actually begin.

**Common mistake:** Answering only for the whole-system case, and not asking what
level of failure is meant.

---

## Q10. What happens if a generator fails to start?

**Strong answer:** Walk it through by scenario.

**One set in a path fails** — the other set in that path carries that path's normal
share. In my design each path has two 2,400 kW sets and the path's normal share is
about 1,715 kW, so one set covers it at 71%. No load impact. What's lost is the
path's ability to take over the *other* path's load — so the facility is still
supplied, but no longer able to absorb a second path failure.

**Both sets in a path fail** — that path is dead once its battery depletes. The IT
load transfers entirely to the other path through the dual-corded servers, and the
other path is on its own generators. Still no IT interruption, but the facility is
now on a single path with no utility and no redundancy. That is a "get everyone out
of bed" state.

**All generators fail** — the batteries give me 10 minutes at full load. That's the
real reason the autonomy is 10 minutes rather than 5: 15 seconds would cover the
generator start, but 10 minutes gives the operators time to diagnose the failure,
attempt a manual start, and if they can't, execute a *controlled* IT shutdown
instead of a hard drop. A controlled shutdown recovers in a fraction of the time a
hard drop does.

The causes worth knowing, because they're what actually happens: contaminated or
aged fuel (the most common, and why fuel polishing matters), flat start batteries,
a failed jacket water heater leaving a cold engine, a controller in the wrong mode
after maintenance, and a failed start signal. Note how many of those are
**maintenance and human factors** rather than mechanical failure — which is the
resilience point again.

**ELI10:** The emergency engine doesn't start. The second engine on that side picks
up the work instead. If none of them start, the batteries keep everything alive for
ten minutes — long enough for the engineers to try to fix it, and if they can't,
long enough to switch all the computers off *properly* rather than having them
crash. Switching off properly means they come back in minutes instead of hours.

**Likely follow-up:** *"Why 10 minutes of battery if the generator starts in 15
seconds?"* → Exactly this. It isn't sized for the generator start. It's sized for
the diagnostic window and the controlled shutdown.

**Common mistake:** Sizing battery autonomy on generator start time. It reveals that
you've only thought about the success case.

---

## Q11. How do you identify a common-mode failure?

**Strong answer:** Systematically, not by intuition. I'd work through four passes:

1. **Trace both paths on the SLD and list every element on each.** Anything
   appearing on both lists is a candidate. This catches bus ties, shared boards,
   shared STS.
2. **Ask what's *not* on the SLD.** This is where they hide: DC control supplies,
   PLCs and controllers, communications networks, cable containment and risers, fire
   compartments, rooms, fuel systems, chilled water loops, earthing. An SLD shows
   power topology and nothing else, so an SLD review alone will never find them.
3. **Walk the failure modes, not the components.** For each failure ask "what else
   is in the blast radius?" A busbar fault isn't a loss of supply — it's an arc with
   pressure and hot gas that destroys a compartment. If both boards are in one room,
   a single fault takes both paths, and the SLD looked perfectly 2N.
4. **Check the load end.** Single-corded equipment makes the whole upstream 2N
   investment worthless for that load.

The ones I'd go looking for first, because they're the classics: a normally-closed
bus tie; a single DC control supply feeding both paths' protection; both
switchboards in one fire compartment; both paths' cables in one tray or through one
penetration; a shared generator paralleling controller; a shared fuel polishing
skid; a single earthing/MEN point; and a single BMS or EPMS controller that both
paths' automation depends on.

**ELI10:** You look at the map and see two separate roads, so you feel safe. Then
you go and actually walk both roads, and you find out they both cross the same
bridge, or they both start at the same roundabout, or they run side by side through
the same tunnel. Finding the shared bit is the whole job — drawing two lines is
easy.

**Likely follow-up:** *"Give me one from your own design."* → The rack-level STS,
which is a documented deliberate exception; and the chilled water ring main, which
is a mechanical common element requiring sectionalising valves — TQ-003 on my open
issues register. Naming your own honestly is far stronger than claiming there are
none.

**Common mistake:** Looking only at the single line diagram. The dangerous
common-mode failures are in the things an SLD doesn't show — controls, rooms, cable
routes and DC supplies.

---

## Five mistakes new data centre electrical engineers make

**1. Forgetting that cooling is an electrical load.**
They protect the IT load with a beautifully designed 2N UPS system and leave the
chillers, pumps and CRAH fans on a non-backed board. The IT equipment then rides
through the power event perfectly and thermally shuts down twenty minutes later.
The corollary error is subtler and just as common: putting the chillers on the
generator but not resolving what happens to the data hall during the 60–120 seconds
between utility loss and chilled water temperature recovering. **Continuous cooling
is the hardest part of fault tolerance, and it is a mechanical–electrical interface
problem, so it falls between two disciplines and gets missed by both.**

**2. Calling something redundant because there are two of them.**
Two transformers on one MV bus. Two UPS systems with one DC control supply. Two
switchboards in one fire compartment. Two paths of cable in one tray. N+1 chillers
on a non-sectionalised chilled water ring. Every one of these looks redundant on a
drawing and fails as a single unit in reality. **The design discipline is not
drawing two of everything. It is hunting for the thing that is still one of.**

**3. Sizing each path for half the load.**
In a 2N facility carrying 2 MW, each path carries 1 MW in normal operation — so the
lazy reading is that each path is a 1 MW path. It isn't. Each path must be capable
of the full 2 MW, because at some point it will be carrying all of it. This single
error produces a facility that is described as 2N, cost 1.5× an N facility, and
fails on the first single-path event. **Always size for the takeover case, never the
normal case.**

**4. Sizing battery autonomy on generator start time.**
"The generator starts in 15 seconds, so 30 seconds of battery is plenty." This
assumes the generator starts. Autonomy exists for the case where it doesn't — to
give operators time to diagnose, attempt a manual start, and if that fails, execute
a controlled IT shutdown rather than a hard drop. A controlled shutdown recovers in
minutes; a hard drop recovers in hours, with corrupted filesystems and rebuilding
storage arrays. **Autonomy is sized for the failure case, not the success case.**

**5. Claiming things the design hasn't proven.**
"Concurrently maintainable" with no switching sequences written. "Selective" with no
coordination study run. "Tier III" with no certification. "65 kA rated" with no
fault level study. Every one of these gets found in a design review, and the cost is
not the technical correction — it's that the reviewer now distrusts everything else
in your package. **Say what you have proven, say what you have assumed, and say what
remains open. An engineer who volunteers their open issues register is trusted. An
engineer whose gaps get discovered is not.**
