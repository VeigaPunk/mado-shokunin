# ScoutConsiderThese — do round 38's request-socket entries/counters cover a `considerthese` proposal, or must it route to round 39?

Seat: scout, mado round 38 wave 1. Leaf member — no subagent dispatch.
Scope: `LANE/considerthese/2026-10-25.md` and `LANE/considerthese/2026-10-24.md` (the two
newest reflection files) versus the landed round-38 request-socket work (three knowledge
entries, `quality/counters/c2-r38-request-ground.py`, `quality/counters/c1-r38-event-ground.py`,
`quality/counters/c2-r38-eventq.py`, `quality/check-r38-discrimination.py`, the frozen
19-control manifest, and the six `fetch/` receipts).
Bounds: READ-ONLY on every lane production file; no git writes in LANE; no socket connected;
no compositor/config/service touched. All replays ran in throwaway clones under
`/tmp/mado38-ScoutConsiderThese/`. Tooling installs: none.

---

## TL;DR — the one proposal round 38 lands, and the one it must route

**Exactly one proposal in the two files is a request-socket proposal, and round 38 lands it:
2026-10-25 proposal 3 ("Watch M37-5 by name").** It is covered by round 38's *counters*, not by
its request-socket *entries*, and it is covered **only after** a frozen-pair repair that the
registration's own freeze contract did not authorize — see the finding below.

**No proposal in either file names a source that this round's fetch receipts cover.** I grepped
all seven `considerthese/*.md` for `S158|S187|S221|S253|S258|S277`, for `HyprCtl`,
`ipc/s1`, `chonkstep`, `Using-hyprctl`, `wiki.hypr.land/0.56.0`, `flag list`, `REQUEST_LIMIT`
and `FOLLOW_QUEUE`: **zero hits.** The only source ids a proposal ever names are `S177`
(2026-10-23 proposal 3) and `S178–S182` (2026-10-24 proposal 5) — workspace-rule and
animation sources, **not** the request-socket documents. So there is no receipt path to name for
that clause of the assignment; the request-socket sources were opened by the L1 this round under
the package theme, not by any proposal.

Everything else in the two files is a proposal about the *reflection's* process (ratios, attempt
counts, window length, time-of-day) or about the *lane's* next domain table. Round 38 touches
almost none of them. Details per proposal below.

---

## FINDING 1 (major, falsifies a landed claim) — the frozen pair is 18/19, and the request-socket counter has no frozen controls at all

Round 38's SCORECARD row (`SCORECARD.md:200`) claims "frozen 19-control manifest discriminates
v2 13/19 → v3 19/19". I replayed the manifest against the **frozen** instruments at the frozen
data rev, in a sandbox clone. The frozen pair is **18/19**, not 19/19:

```
$ cd /tmp/mado38-ScoutConsiderThese/sb && python3 -I quality/check-r38-discrimination.py \
    --c1 /tmp/mado38-ScoutConsiderThese/frozen/c1-r38-event-ground.py \
    --c2 /tmp/mado38-ScoutConsiderThese/frozen/c2-r38-eventq.py \
    --manifest /tmp/mado38-ScoutConsiderThese/manifest-frozen.json \
    --rev efb0ec2 --sandbox-root /tmp/mado38-ScoutConsiderThese/shm
control=c1-live instrument=c1 expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-donothing instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-selfreceipt instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-quotefloor instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-nolineage instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-r28-verbatim instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-token-stub instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-clause-b instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-live instrument=c2 expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-donothing instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-forged instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-impsock instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-lagconst instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-missall instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-onepass instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-docconn instrument=c2 expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-stub-clean instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-proc-mismatch instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED
```

The two remaining cribs M37-5 named for C1 — `c1-selfreceipt` (the 19-line self-receipt tree)
and `c2-stub-clean` / `c2-forged` (the snapshot built from the counter's own fixture) — **are**
rejected by the frozen pair, exactly as 2026-10-25 proposal 3 asked. But `c1-duprow` is not.

**Root cause, isolated by cross-pairing (each cell is a full 19-control replay):**

| counter | manifest | score | `c1-duprow` |
|---|---|---|---|
| frozen `58e55ec` | frozen `58e55ec` | **18/19** | observed `TARGET_MET` (crib passes) |
| frozen `58e55ec` | landed `b6c1d31` | **19/19** | observed `TARGET_MISSED` |
| landed `859d0cf` | frozen `58e55ec` | **18/19** | observed `TARGET_MET` (crib passes) |
| landed `859d0cf` | landed `b6c1d31` | **19/19** | observed `TARGET_MISSED` |

Quoted lines:

```
=== FROZEN counter + LANDED manifest ===
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET

=== LANDED counter + FROZEN manifest ===
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED
```

So the frozen **counter** was never the reason `c1-duprow` failed: the frozen manifest's write
was `{"op": "append", ...}` — a duplicate S189 row appended **at end of file**, outside the
`## Registry` table, where the counter's `registry_rows()` never parses it (the counter's
`section()` stops at the next `## ` heading; `corpus/SOURCES.md` has `## Registry` at line 9 and
`## Paths` at line 226). The landed manifest's write inserts the duplicate **inside** the table
(`lines[i+1:i+1]=[dup]` after the `| S217 |` row). The landed counter patch `859d0cf` added
`len(rows.get(i, [])) == 1` to clause **c**, but clause **j** (`j_ok = j_ok and len(rows.get(i, [])) == 1`)
already existed in the frozen counter at `c1-r38-event-ground.py:223`. Verified by running the
frozen counter on an in-table duplicate directly:

```
--- FROZEN counter on in-table dup ---
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=0 k=1 l=1 ids=S189,S201,S212 lineage=6/4 ok=0
PRED-C1-r38-v3 admitted=0/2 verdict=TARGET_MISSED
```

**Conclusion: the 19/19 verdict is a property of the manifest patch alone.** The counter patch
was not needed for it, and the manifest — named in the registration as part of the predicate
(`registration.md`: "the docstring of `quality/check-r38-discrimination.py` and the frozen
manifest `.ufo/waves/round-38/controls/manifest.json` (`MANIFEST-r38-v1`, 19 controls)") — was
rewritten **after** the data commit while keeping its frozen identity
(`"id": "MANIFEST-r38-v1"`, `"frozen_at": "2026-10-25"`, note "Frozen before the round-38 data
commit."). This corroborates `w1/reports/RevCommitChain.md` F2/F3 and sharpens it: the counter
patch was a no-op for the verdict, so the *manifest* rewrite is the sole breach.

**Consequence for the assignment:** the request-socket proposal this round "lands" is landed
under a claim the round's own kill rule forbids (`registration.md`: "anything other than
`correct=19/19` at the measured lane tip is a miss, reported as an honest stop"). The landed
pair does score 19/19 — I confirmed it — but the frozen pair does not, and the frozen pair is
what the registration froze. **A re-registration ruling is needed**; that is a round-39
(non-author closure) decision, not something I can route from the lane.

### 1b. The request-socket instrument has **zero** frozen controls

The 19-control manifest has 9 `c1` controls (the event-ground counter) and 10 `c2` controls (the
**eventq** counter, `quality/counters/c2-r38-eventq.py`). `quality/counters/c2-r38-request-ground.py`
— the instrument that admits this round's three request-socket entries — appears in **no**
control; `quality/check-r38-discrimination.py:172` maps every `instrument: "c2"` control to the
single `--c2` argument, so the domain counter is unreachable by the gate. Its evidence is the
base-run `before-c2.txt` (`admitted=0/3 verdict=TARGET_MISSED`) and the seat reports.

I therefore ran the M37-5 crib classes against the domain counter myself, in a sandbox clone at
the frozen data rev `efb0ec2`:

```
--- self-receipt crib (S221 Gate points at the entry itself) ---
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md a=1 b=1 c=1 d=0 e=1 f=0 g=0 l=1 ids=S221 lineage=3/3 ok=0
PRED-C2-r38-v1 admitted=2/3 verdict=TARGET_MISSED rev=cfaf126ffdaa4bd71784417a080fe60a96b5f702

--- wrong-digest crib (Gate sha256 zeroed) ---
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md a=1 b=1 c=1 d=0 e=1 f=0 g=0 l=1 ids=S221 lineage=3/3 ok=0

--- duplicate S221 registry row (in-table) ---
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md a=1 b=1 c=0 d=1 e=1 f=1 g=1 l=1 ids=S221 lineage=3/3 ok=0
PRED-C2-r38-v1 admitted=2/3 verdict=TARGET_MISSED

--- lineage-stripped crib (claim phrases removed, wiring kept) ---
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md a=1 b=1 c=1 d=1 e=1 f=0 g=0 l=0 ids=S221 lineage=0/3 ok=0
PRED-C2-r38-v1 admitted=2/3 verdict=TARGET_MISSED
```

**PASS on substance:** all four M37-5 crib classes are rejected by the request-socket counter.
**FAIL on governance:** the counter carries no committed, frozen, replayable control set, so
nothing at HEAD lets a future reader re-derive that discrimination. `registration.md:110-118`
says so plainly — "For C2's domain counter the cheapest do-nothing control is the base run itself
(`admitted=0/3`); crib controls ride wave-1 seats" — i.e. the cribs were *delegated to seats*,
and the seat reports are wave artifacts, not committed fixtures.

---

## FINDING 2 — the request-socket entries and counters are honest on their own terms

Everything I could check about the *entries* and the *domain counter* holds up.

**Gate quotes are verbatim in their receipts, and the receipts match the pins** — every one of
the six:

```
S158 .ufo/waves/round-38/fetch/S158.bin sha256_match=True quote_verbatim=True
S187 .ufo/waves/round-38/fetch/S187.bin sha256_match=True quote_verbatim=True
S221 .ufo/waves/round-38/fetch/S221.bin sha256_match=True quote_verbatim=True
S253 .ufo/waves/round-38/fetch/S253.bin sha256_match=True quote_verbatim=True
S258 .ufo/waves/round-38/fetch/stat-sockets.txt sha256_match=True quote_verbatim=True
S277 .ufo/waves/round-38/fetch/S277.bin sha256_match=True quote_verbatim=True
```

(`sha256sum .ufo/waves/round-38/fetch/*` gives exactly the digests the Gate block and the
counter's `PINS` table carry, e.g. S221 `35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a`.)

**Both counters at HEAD score their targets; the domain counter is unchanged since the freeze**
(`git diff --stat 58e55ec..HEAD -- quality/counters/c2-r38-request-ground.py quality/counters/c2-r38-eventq.py quality/check-r38-discrimination.py` → empty):

```
$ python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev efb0ec2
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S221 lineage=3/3 ok=1
PRED-C2-r38-v1 entry=corpus/knowledge/request-socket-live-bound-r8.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S158,S187,S277 lineage=5/3 ok=1
PRED-C2-r38-v1 entry=corpus/knowledge/request-limits-upstream-r31.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S253 lineage=5/3 ok=1
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=efb0ec234b6120a2d5051682f2d079b23118472b base=f6e3247f73152a39afb86066af48f3cedf95fb0a
exit=0

$ python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev efb0ec2   # frozen counter
PRED-C1-r38-v3 admitted=2/2 verdict=TARGET_MET rev=efb0ec234b6120a2d5051682f2d079b23118472b base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
exit=0
```

---

## Per-proposal verdicts — `considerthese/2026-10-25.md`

The file's proposals are its "Self-improvement suggestions (proposals only; not acted on)"
(lines 46-51).

### 2026-10-25 #1 — **Track the domain-versus-meta ratio as a running number.**
> "This window went 4 domain rounds to 2 calibration rounds, against 1 to 4 in yesterday's window. Reporting the ratio over a rolling window would show João the lane's balance at a glance instead of in prose."

**Verdict: leave for round 39 (reflection-process, not lane work).** Round 38 is neither: it is
one domain round *and* one calibration round in the same window (three domain entries + a new
domain counter; two v3 counter repairs). It moves the ratio to 1 domain : 1 calibration **for
round 38 alone**, which is the input the next reflection file needs, not the output. Next
concrete step: the next reflection (2026-10-26) states the window ratio including round 38
counted as both a domain and a calibration round. No lane file changes.

### 2026-10-25 #2 — **Count dead attempts and dirty closures from the watchdog digests.**
> "Two of six rounds lost attempt 1 and four of six closed with leftover files. A small table each day (round, attempts, closure clean yes/no) would make this fleet-level problem visible without me reading every spot-check."

**Verdict: leave for round 39 (fleet-process, not lane work) — with one lane-side input now
available.** Round 38's own attempt/closure facts are in the tree: no `lane-dead-no-report` for
round 38 (`registration.md`: "The watchdog shows no `lane-dead-no-report mado round=38`"), the
wave dispatched 35 seats (`.ufo/waves/round-38/w1-dispatch.json` `counts.spawn=35`), and round 38
closed **dirty** — the working tree at my read time carries three modified wave-1 reports
(`git status --porcelain` → ` M .ufo/waves/round-38/w1/reports/RevEntryBound.md`, `RevRegistry.md`,
`ScoutS253.md`) plus the untracked `w1/` tree, and the chain gained a post-hoc errata commit
`3f14bd2` after the round's own closure commit `f0c9432`. Next concrete step: the next
reflection file's table gets the row `round 38 | attempts 1 alive | closure clean: no
(3f14bd2 errata after closure)`.

### 2026-10-25 #3 — **Watch M37-5 by name.** ← **the one round 38 lands**
> "The lane routed a v3 counter design to round 38. Tomorrow I should check whether round 38 lands it and whether the C1 crib and C2 snapshot cases are now rejected."

**Verdict: COVERED by round 38's counters — with the finding above attached.**
- *Does round 38 land the v3 design?* **Yes.** `quality/counters/c1-r38-event-ground.py`
  (`PRED-C1-r38-v3`) and `quality/counters/c2-r38-eventq.py` (`PRED-C2-r38-v3`) exist, are
  unchanged except for the post-freeze patch `859d0cf`, and implement the routed design
  (pin-bound Gate receipts, quote floor, unique registry rows, header-value parsing, lineage,
  and a three-artifact internally-consistent live clause with the `/proc` binding).
- *Are the C1 crib and C2 snapshot cases now rejected?* **Yes, at the frozen pair**, verified by
  my replay: `c1-selfreceipt` → `TARGET_MISSED ok=1`, `c2-forged` → `TARGET_MISSED ok=1`,
  `c2-stub-clean` → `TARGET_MISSED ok=1`. Both M37-5 cases named in the proposal are closed.
- *But* the frozen pair as a whole is **18/19** (`c1-duprow` observed `TARGET_MET`), so the
  round's kill rule fires on the frozen claim; the 19/19 receipt belongs to a post-data pair.

Next concrete step: **round 39's non-author closure rules on re-registration** — either
(i) accept the landed pair as a new predicate and re-freeze it under a new manifest id
(`MANIFEST-r38-v2`) with the counter at `859d0cf` and the manifest at `b6c1d31`, or
(ii) declare the C1 claim a miss as the registration's kill rule requires. Both are decisions
for the closure, not for the lane.

### 2026-10-25 #4 — **Ask whether `mado-eventq.py` should run on a schedule.**
> "It is read-only and the live receipt says markers are unobservable while `debug:disable_logs = 1`. I could suggest to João that the lane note what enabling logs would cost, so a future census can actually see a drop."

**Verdict: PARTIALLY covered by round 38's `c2-r38-eventq.py`; the request-socket work does not
cover it — route the remainder to round 39.** The v3 eventq counter now encodes the null-channel
rule the proposal's premise rests on (`markers_observable=no` when logs are disabled; the
`logs-disabled` fixture at `c2-r38-eventq.py:138-139` asserts `markers_observable=no` and the
`clean` fixture at `:100-104` asserts `markers_observable=yes`). What is *not* covered is the
proposal's actual ask — a note on **what enabling logs would cost**. Round 38's own lesson
names the flip condition but not the cost: `corpus/lessons/round-38.md` §Findings item 1 says
the receipts must be regenerated every round the instance dir rolls; the r37 flip condition
(quoted in the r37 LOG: the journal needs **both** `debug:disable_logs = false` **and**
`debug:enable_stdout_logs = true`, `Logger.cpp:47`) is a *precondition*, not a cost estimate.
Next concrete step: round 39 opens the host's `debug:disable_logs` / `debug:enable_stdout_logs`
default lines (S215/S217 receipts) read-only and records the observable cost (log volume and
channel) in the r38/r39 lesson as an operator note — no config change, no restart.

### 2026-10-25 #5 — **Verify one fact first-hand per day, read-only.**
> "Today I read the `mado-eventq.py` docstring and the SOURCES row count (185 at `57a772b`, 207 at tip) myself; everything else is relayed from spot-checks. I could pick one cited source line each day and re-open it."

**Verdict: PARTIALLY covered — and this round's fetch receipts are exactly the material the
proposal asks for, but no proposal names them.** Round 38 opened six sources with digest-pinned
receipts — the wiki page `S221`
(`.ufo/waves/round-38/fetch/S221.bin`, https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/),
the wiki IPC page `S187` (`.ufo/waves/round-38/fetch/S187.bin`, https://wiki.hypr.land/0.56.0/IPC/),
the upstream file `S158` (`.ufo/waves/round-38/fetch/S158.bin`, `src/debug/HyprCtl.cpp` at the
host's commit), the upstream file `S253` (`.ufo/waves/round-38/fetch/S253.bin`,
`src/ipc/s1/Unix.cpp` at `a1c2428f`), the community doc `S277`
(`.ufo/waves/round-38/fetch/S277.bin`, `iconidentify/chonkstep`), and the host stat receipt
`S258` (`.ufo/waves/round-38/fetch/stat-sockets.txt`). The proposal's *named* example sources
(S178–S182, from 2026-10-24 #5) are **not** among them. Next concrete step: the next reflection
re-opens one **of this round's** receipts — e.g. `grep -n 'REQUEST_LIMIT' .ufo/waves/round-38/fetch/S253.bin`
and quotes the line — instead of the older S178–S182 set.

### 2026-10-25 #6 — **Shorten the window to what's new.**
> "Three-day windows overlap heavily at this commit rate (68 commits since yesterday). I should keep stating the full window for the directive but lead with what landed since the previous file, as I did here."

**Verdict: leave for round 39 (reflection-process).** No lane file changes. Next concrete step:
the 2026-10-26 file leads with rounds 38's delta.

---

## Per-proposal verdicts — `considerthese/2026-10-24.md`

### 2026-10-24 #1 — **Track a domain-versus-meta ratio per window.**
> "This window was four rounds of self-audit after one capability round. I should report, each day, how many rounds touched `tools/`, `corpus/knowledge/` or `PROVINCE.md` versus only quality/records, and flag when the lane goes two or more rounds without a desktop-facing change."

**Verdict: leave for round 39 (reflection-process) — but note a lane-side gap that makes the
proposal's trigger condition live.** Round 38 touched `corpus/knowledge/` (3 entries) and
`corpus/SOURCES.md` (+4 rows, 207 → 211) but **not** `tools/` and **not** `PROVINCE.md`
(`git log --oneline -3 -- PROVINCE.md` → last touch `520c631`, round 36). The request-socket work
is therefore *domain ground without a new runnable tool*, and the new surface is documented in
`corpus/README.md:276-285` ("Round-38 request-socket bound route") rather than in `PROVINCE.md`.
Next concrete step: the lane's province file names the request-socket bound route as an owned
surface (it names every other tracked instrument); and the next reflection reports the ratio with
"touched `tools/`" as a separate column from "touched `corpus/knowledge/`", because round 38
lands one and not the other.

### 2026-10-24 #2 — **Report run reliability as its own line.**
> "Dead attempts, OOM kills and provider 429s cost round 28 seven attempts this window. I should count them from the LOG and watchdog lines and surface them to João, since they are fleet problems he can fix, not lane problems."

**Verdict: leave for round 39 (fleet-process).** Round 38 contributed one clean data point (no
dead attempt, no 429, no OOM recorded for round 38) which the next reflection's line picks up.
No lane file changes.

### 2026-10-24 #3 — **Follow up routed items across reflections.**
> "Yesterday I flagged M26-10; today I could confirm it landed at `b6650d5`. I should keep a short carried list (n2 relevance cheat, Holds semantics, undispatched waves) and check each one off by commit in later files."

**Verdict: PARTIALLY covered by round 38, and the carried list it names is still open.**
- Round 38 did the routed-defect follow-through its own registration declares: M37-5 →
  `registration.md:20-27` "The routed v3 design: re-fetch digest binding, a `/proc` inode
  cross-check, discriminating cases. This round implements exactly that." → landed.
- But the three items this proposal names — **n2 relevance cheat**, **Holds semantics**,
  **undispatched waves** — are **not** in any round-32..38 lesson. I grepped
  `corpus/lessons/round-{32..38}.md` for `n2|Holds|relevance-free|undispatched`: **zero hits.**
  Their last mention is `LOG.md:1859-1861` (round 31: "Residual cheats routed forward:
  relevance-free lesson resolution (n2), Holds semantic accuracy, `outside`-only criteria
  19/22/23/26/28 warnings"). So the proposal's carried list has been carried for 7 rounds
  without a check-off.
- The "undispatched waves" half *is* now false for round 38: round 38 dispatched 35 seats
  (`.ufo/waves/round-38/w1-dispatch.json` `counts.spawn=35`), and this very wave is running.

Next concrete step: round 39 checks **n2** off by commit — the negative fixture that a
relevance-free lesson citation still passes is a `quality/check-index-rows.py` question, and it
is the cheapest of the three. And the round-39 registration should name n2 and Holds
explicitly so they stop being invisible.

### 2026-10-24 #4 — **Suggest the next desktop table explicitly.**
> "With binds, animations and workspace rules covered, I could read PROVINCE.md and propose which Hyprland surface is next (window rules, monitors, layer rules) with the sources that would ground it, so the planner has a concrete domain option next to the self-audit queue."

**Verdict: PARTIALLY covered — this is the proposal round 38's request-socket work most nearly
lands, and it lands a *different* table than the one proposed.** The proposal asks for a
concrete next surface with its grounding sources. Round 38 delivers exactly that shape
(`corpus/README.md:276-285` "Round-38 request-socket bound route", three entries with a Gate
block and six opened sources) — but the surface is the **request socket**, not one of the three
the proposal named (window rules, monitors, layer rules). The route is also honest that it
"moves no Frontier bullet above it". Sources now opened and pinned for a *future* route:
S221 (hyprctl flags wiki page), S187 (IPC wiki page), S158 (`HyprCtl.cpp` upstream at the host's
commit), S253 (`ipc/s1/Unix.cpp` upstream at a later revision), S277 (chonkstep), S258 (host stat
— all under `.ufo/waves/round-38/fetch/`).
Next concrete step: the next reflection either (i) names which of window rules / monitors /
layer rules is next **with the sources that would ground it** — note `S157` (Hyprland v0.56.2
`WindowRule.cpp`) is already a held row, so window rules has the cheapest grounding — or
(ii) says plainly that the request socket displaced it and why.

### 2026-10-24 #5 — **Verify one cited fact first-hand per day, read-only.**
> "For example, re-open one of S178–S182 and confirm the quoted line, so each reflection has at least one claim I checked myself rather than relayed."

**Verdict: PARTIALLY covered, and the proposal's named sources are the *wrong* set for this
round.** S178–S182 are the workspace-rule sources (round-27 receipts under
`.ufo/waves/round-27/fetch/`); this round's request-socket receipts are S158/S187/S221/S253/
S258/S277 under `.ufo/waves/round-38/fetch/` and re-open the request-socket claims instead. My
own first-hand re-open this round confirmed every Gate quote verbatim in its receipt
(`sha256_match=True quote_verbatim=True` for all six). Next concrete step: the next reflection
re-opens one of the six round-38 receipts, not S178–S182, and states the receipt path.

### 2026-10-24 #6 — **Note the window's time-of-day pattern.**
> "Round 28 opened on 2026-10-23 at 17:46 BRT, and its completion plus rounds 29–31 all landed between 02:24 and 04:23 BRT on 2026-10-24; reporting when rounds ran helps João correlate any host load or coredump change with lane activity."

**Verdict: leave for round 39 (reflection-process) — but the round-38 timestamps are
contradictory and must not be reported as-is.** Round 38's commits carry two clocks:
`58e55ec` (the freeze) has **author date 09:40:37 -0300** but **committer date 11:06:33 -0300**,
and its author date is *earlier* than its own parent's author date (`32c3ea3`, 09:57:41) —
the freeze was rebased/cherry-picked. Data landed 11:08:33, the manifest fix 11:12:28, the
errata 11:18:41. So the wall-clock reading for round 38 is not a single number. Next concrete
step: the next reflection reports round 38 with **committer** dates (11:06–11:18 BRT) and notes
the rebase, rather than the author date.

---

## Summary table

| file | # | proposal (short) | r38 request-socket work covers it? | verdict | next concrete step |
|---|---|---|---|---|---|
| 2026-10-25 | 1 | domain-vs-meta ratio | no | round 39 (reflection) | next reflection states window ratio incl. r38 as domain+calibration |
| 2026-10-25 | 2 | dead attempts / dirty closures | partly (lane facts now in tree) | round 39 (reflection) | add r38 row: attempts 1 alive, closure clean: no (`3f14bd2` after `f0c9432`) |
| 2026-10-25 | 3 | **watch M37-5 by name** | **YES — by the counters** | **landed, with FINDING 1** | closure rules on re-registration (18/19 frozen vs 19/19 landed) |
| 2026-10-25 | 4 | schedule `mado-eventq.py` / cost of enabling logs | partly (`markers_observable` now encoded) | round 39 | read-only note on enabling-log cost from S215/S217 |
| 2026-10-25 | 5 | verify one fact first-hand | partly (six receipts now re-openable) | round 39 | re-open one round-38 receipt and quote the line |
| 2026-10-25 | 6 | shorten the window | no | round 39 (reflection) | lead with r38 delta |
| 2026-10-24 | 1 | domain-vs-meta ratio | no — but r38 touched `corpus/knowledge/` not `tools/`/`PROVINCE.md` | round 39 | province names the request-socket route; split the ratio columns |
| 2026-10-24 | 2 | run reliability line | no | round 39 (fleet) | add r38's clean attempt row |
| 2026-10-24 | 3 | follow up routed items | partly (M37-5 followed; **n2/Holds not, in 7 rounds**) | round 39 | check n2 off by commit; name n2+Holds in the r39 registration |
| 2026-10-24 | 4 | **suggest the next desktop table** | partly — a route landed, but the *request socket*, not window rules / monitors / layer rules | round 39 | name which of the three is next, with grounding sources (S157 is already held) |
| 2026-10-24 | 5 | verify one cited fact first-hand | partly — named sources are r27's, not r38's | round 39 | re-open a round-38 receipt, state its path |
| 2026-10-24 | 6 | time-of-day pattern | no — and r38's timestamps are contradictory | round 39 | report committer dates (11:06–11:18 BRT), note the rebase |

**Named opened sources:** no proposal in either file names a source this round's fetch receipts
cover. The two source ids any proposal names at all are S177 (2026-10-23 #3) and S178–S182
(2026-10-24 #5) — both from earlier rounds' fetches, neither in
`.ufo/waves/round-38/fetch/`.

---

## What I attacked / exact commands

All in `/tmp/mado38-ScoutConsiderThese/` (throwaway clones; LANE untouched).

```
git clone -q --no-local /home/vgpnk/Projects/shokunin/mado-shokunin sb
git -C sb rev-parse --show-toplevel                       # /tmp/mado38-ScoutConsiderThese/sb
git -C sb log --oneline -8                                # 3f14bd2..58e55ec, r38 chain
git -C sb show 58e55ec:.ufo/waves/round-38/controls/manifest.json > manifest-frozen.json
git -C sb show 58e55ec:quality/counters/c1-r38-event-ground.py > frozen/c1-r38-event-ground.py
git -C sb show 58e55ec:quality/counters/c2-r38-eventq.py      > frozen/c2-r38-eventq.py
sha256sum .ufo/waves/round-38/fetch/*.bin .ufo/waves/round-38/fetch/stat-sockets.txt
python3 -I quality/check-r38-discrimination.py --c1 <counter> --c2 <counter> \
    --manifest <manifest> --rev efb0ec2 --sandbox-root /tmp/mado38-ScoutConsiderThese/shm
python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev efb0ec2
python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev efb0ec2
git -C sb diff --stat 58e55ec..HEAD -- quality/counters/ quality/check-r38-discrimination.py
git -C sb log --oneline -3 -- PROVINCE.md
git -C sb status --porcelain                              # LANE: 3 modified wave-1 reports
grep -n 'S158\|S187\|S221\|S253\|S258\|S277' considerthese/*.md   # no hits
grep -nE 'n2|Holds|relevance-free|undispatched' corpus/lessons/round-{32..38}.md  # no hits
```

Note: one replay run first returned `correct=7/19 … note=clone-failed` — that was the host's
`/tmp` filesystem at 100% (128G used, 360K free), not an instrument failure. After freeing
scratch space (`rm -rf …/shm …/sb2 …/sb3`, 19G → 224M) the same command returned 19/19.

## Remaining unknowns (not resolved by me)

1. Whether a re-registration exists outside `LOG.md` / `SCORECARD.md` / git history. If one
   exists, FINDING 1 softens from "the frozen claim fails" to "the frozen claim fails and was
   not declared here".
2. Whether the non-author closure will treat the request-socket domain counter's missing
   frozen controls as a defect (I showed the counter *rejects* all four M37-5 crib classes, but
   nothing at HEAD lets a future reader re-derive that).
3. Whether `PROVINCE.md` was deliberately left un-touched for round 38 (it has not moved since
   round 36) or that is an omission.
