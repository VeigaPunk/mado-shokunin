# CritAxisClaim — critic report, mado round 37 wave 1

Seat: `L1Mado37-2.CritAxisClaim` (critic). Assignment: `.ufo/waves/round-37/w1/prompts/CritAxisClaim.md`.
Target: `.ufo/waves/round-37/registration.md` (v2 freeze `893a8aa`; lane `master` = `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b` when measured).
Read-only on the lane. Writes: this report and `.ufo/waves/round-37/w1/scratch/CritAxisClaim/` (`controls_critaxis.py`, `controls-critaxis.txt`). Sandbox: `/dev/shm/mado37-CritAxisClaim/sb` (a `git clone --no-local` of the lane, sandbox identity `sandbox@invalid`, one branch per control). No socket connected, no hyprctl verb run, no counter edited. Tool installs: none.

## Verdict summary

| # | Item | Verdict |
|---|---|---|
| 1 | Lowest-axis rule and stagnation-nudge reading | **PASS, with a finding.** The tie reading is literally honest and the nudge reading is right, but "coverage is a lowest axis" is vacuous: every published rubric normalises itself to N/N. The rule that actually discriminates, AXES.md's "trend furthest behind", supports coverage and is not cited. |
| 2 | kaidoku-r29 naming rule | **FINDING (fixable record defect plus a counter limit).** C1 names a surface and an "unmoved" command, but the frontier row it says it moves is a different surface (the Walker launcher's sockets). The surface is partly held already, so only one edge class is new. The C1 counter measures wiring and sourcing (quality), not the coverage move. |
| 3 | kake-r34 rule: build the do-nothing control, score it with both counters | **Do-nothing: PASS** (both counters miss at freeze, at tip and on an empty commit). **Cheapest skip-the-work control: FAIL on both counters.** C1 reaches `TARGET_MET` with two 7-line stubs, with an entry that asserts the inference the round refuses, and with the refused package entry pasted verbatim. C2 reaches `TARGET_MET live=1` with a hand-written 4-line snapshot that was never read from the host. |
| 4 | Is C2 a capability acquisition by AXES.md's definition? | **Qualifies by type; its demonstration is not evidenced by the counter.** The capability is new to the lane, but the counter's `live` clause cannot tell a live run from a fabricated one. On this host only the census half can ever be demonstrated, because the markers half reads `markers_observable=no`. |

---

## 1. Lowest-axis rule and stagnation nudge

**Checked.** AXES.md (§Working the axes, §The stagnation nudge, §The learning path), SCORECARD.md round 34–36 sections, `quality/check-axis-scores.py`, `quality/check-index.py`, the base receipt `receipts/axis-base.txt`, and the MANIFEST closure records for mado rounds 34–36.

**Quotes.**
- AXES.md:32-34: "At least one claim works the lane's **lowest-scoring non-retired axis**, except when the stagnation nudge (below) waives it."
- AXES.md:68-70: the nudge applies "When every axis the lane owns sits at or above the lane's saturation line **and** no capability has entered the table within the lane's stagnation window".
- AXES.md:20-23: "Expansion ↔ `coverage` + `adjacency`; quality ↔ `depth` + `freshness` + `operability`; discernment ↔ `calibration`. Pick the round's axis from the trend furthest behind."
- `receipts/axis-base.txt`: `MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH`, `calibration published=48/48`, `operability published=12/12`, `MADO_AXIS: checked=3 mismatched=0`.
- MANIFEST.json, mado round 36: `"admitted": true, ... "capabilities_added": ["counter-discrimination audit", "evidence-pointer durability audit"]`. Round 34: `"admitted": true, ... "capabilities_added": ["crib-rejecting coverage counter ..."]`.
- MANIFEST.json, mado round 36 trends: `"trends": {"expansion": "unchanged", "quality": "improved", "discernment": "improved"}`. The spot-check `corpus/lessons/round-36-verifier-spotcheck.md:106` says: "**expansion: unchanged.** One grounding row (S211) and zero admitted knowledge entries".

**Assessment.**
- **Nudge reading is correct.** Admitted capability rows entered in round 36 (two rows) and round 34 (one row), both inside the declared window of N=3 (SCORECARD.md:2311, "Saturation 9.0 / N=3 unchanged"). The second nudge condition fails, so the waiver is off. The conclusion does not depend on the scale: round 36's text calls the scores "their rubric's 1.0 against a 9.0 saturation line" (SCORECARD.md:2244), and whether 1.0 is read as 10/10 or as 1.0, the nudge stays off.
- **The tie is honest but uninformative.** All three published rubrics are self-normalising:
  - navigation is `check-index.py` `indexed=A/B`, where B is the count of `corpus/knowledge/*.md` files (`check-index.py:8`, "`corpus/knowledge/*.md` note has exactly one index row"). It has been at N/N in every publication since 32/32. The one exception is a single `35/38` (`grep -o "navigation [0-9]*/[0-9]*" SCORECARD.md` → `32/32 ×2, 34/34 ×2, 35/35, 35/38, 43/43, 46/46 ×2, 47/47 ×3, 50/50 ×3, 8/22`).
  - operability is `check-index.py --selftest`, the selftest of a single gate (`check-axis-scores.py:14`). It has read 12/12 since round 34.
  - The corpus itself says so: README `## Frontier`, "Index completeness does not retire these unresolved surfaces".

  A three-way tie at max for the third consecutive round (r34 47/47·41/41·12/12, r35 50/50·43/43·12/12, r36 50/50·48/48·12/12) means the lowest-axis rule cannot discriminate. Any claim on any published axis "works the lowest axis". Neither C1 nor C2 can move a published number: adding two indexed entries gives 52/52, and C2's tool is not in the operability selftest. The registration states this itself (registration.md:100, "No score change on any axis is claimed by either counter").
- **The discriminating rule is uncited.** The trend furthest behind at round 36's closure is *expansion* ("unchanged"), which maps to coverage plus adjacency. That justifies C1 as coverage more strongly than the tie does, and the registration does not cite it.
- **Is "coverage (published as navigation)" honest?** It is the label the fleet closure itself uses (round-36 spot-check per-axis table: "coverage (published as navigation 50/50) | unchanged"). Navigation measures index completeness, not "Fraction of the domain's real surfaces the skill governs" (AXES.md:12), so the label is accepted usage rather than a measurement of coverage.

**Impacted axes:** calibration (self-description of the axis choice). **Smallest safe correction:** an append-only line in the registration or round record: "lowest-axis rule is vacuous under a three-way saturated tie; axis chosen by AXES.md §The learning path — expansion was `unchanged` at the round-36 closure". Separately, route the saturation clause (AXES.md:37-39, retire or split) for navigation and operability, since both are self-normalising. Neither fix changes a predicate.

## 2. kaidoku-r29 naming rule (lane-addendum §9)

**Rule** (`scripts/hyaku/lane-addendum.md` §9): "Name the axis by the surface the round changes, not by the number it produces (kaidoku r29). Re-scoring a rule the lane already holds on new inputs, or counting rows a sourceless fixture also counts, is quality work, never coverage or depth. A coverage claim names the surface it moves (frontier → core, a new tool, operation or edge class) and the command that would show it unmoved."

**What C1 names.**
- Surface: "event-socket delivery — what the compositor does to an event client that stops reading (`EventManager.cpp`: a 64-event per-client cap, removal on overflow, partial-write resume)" (registration.md:21-23).
- Unmoved command: "`git grep -l -F <token> master -- corpus/knowledge` is empty for `MAX_QUEUED_EVENTS`, `overflowed event queue`, `debug:disable_logs` and `m_logsEnabled`" (registration.md:24-25). The same four tokens form the counter's precondition (`c1-r37-event-ground.py:25-26`).
- Frontier: "`corpus/README.md` *Frontier* — 'Waybar module text, Walker socket protocol … No … socket connection is added here' (the event-socket client half)" (registration.md:28-29).

So the form of the rule is satisfied: a surface and an "unmoved" command are both named.

**Counterexample A: the cited frontier row is a different surface (false provenance).** The full row at base (`git show b4e47e9:corpus/README.md`, lines 98-100) reads: "Rendered UI, Waybar module text, Walker socket protocol, dispatcher behavior and per-window rule effects: [arc gap ledger](knowledge/arc-synthesis.md) §6. No screenshot, input injection or socket connection is added here." The gap ledger defines the item:
- `arc-synthesis.md:297`: "walker socket protocol | never connected (constraint); the r9 note measured shape only — protocol semantics UNKNOWN".
- `arc-synthesis.md:229`: walker "sockets `srwxr-xr-x` 0 B under `$XDG_RUNTIME_DIR`; `dev.benz.walker` D-Bus owner == walker pid".

That is the Walker launcher's own sockets, not Hyprland's `.socket2.sock`. The phrase "event socket" does not appear in the Frontier list, and `git show b4e47e9:PROVINCE.md | grep -i 'socket\|event\|ipc'` returns only tool-boundary lines. The gloss "(the event-socket client half)" is the registration's own and is not supported by the row it cites. **No frontier row moves.**

**Counterexample B: the surface is partly held at base.** The four tokens were chosen to be absent; the surface itself is not absent:
- `git grep -l -F -i socket2 b4e47e9 -- corpus/knowledge` → 7 files.
- `ipc-contract-r25.md` already cites **S189** (Hyprland v0.56.2 `EventManager.cpp`) for socket creation, path, listen backlog and framing (lines 11, 27, 61-69). The base S189 row is `status= mined used-by= corpus/knowledge/ipc-contract-r25.md`.
- The round-37 receipt is byte-identical to the one the lane committed in round 32: `sha256sum .ufo/waves/round-37/fetch/S189.bin` = `git show b4e47e9:.ufo/waves/round-32/fetch/S189.bin | sha256sum` = `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`.
- The queue-cap line has been quoted in lessons since round 33 (`git grep -n -F MAX_QUEUED b4e47e9 -- corpus/lessons` → `round-33.md:64`, `round-34.md:83`, both spot-checks).

What is genuinely new to `corpus/knowledge` is one **edge class**: per-client overflow, then removal, plus whether the logger can observe it (`disable_logs`/`m_logsEnabled`). The rule admits "edge class" as coverage, so the coverage naming survives only on that narrower ground. The "unmoved" command is token-scoped, not surface-scoped.

**Counterexample C: the counter counts what a stub also counts (quality, not coverage).** See item 3. The C1 counter admits a 7-line entry carrying only a header and one quoted constant. It also admits an entry asserting the exact inference the round refuses. It therefore measures wiring and sourcing (registry row, Gate digest, quote restated, index row), which is quality work under §9. A C1 `TARGET_MET` cannot by itself show that the edge class moved into the corpus.

**Verdict:** FINDING. The axis naming is defensible only as "a new edge class". The frontier sentence is wrong. The counter is a quality instrument wearing a coverage label. **Impacted axes:** coverage (claim evidence), calibration (false provenance in a frozen record). **Smallest safe correction:**
1. Add an append-only erratum to the registration: "the cited Frontier row is the Walker launcher socket item (`arc-synthesis.md:297`), not Hyprland socket2; C1 moves a new edge class (overflow→removal and its observability), no frontier row".
2. State in the round record that C1's `TARGET_MET` is wiring evidence, and that the edge-class content is judged by a non-author reading of the two entries (see item 3's correction).

## 3. kake-r34 rule: do-nothing and cheapest-skip controls, both counters

**Rule** (lane-addendum §9): "A target must be one a do-nothing control cannot reach (… kake r34, where a no-parse replay and a junk-row commit met both counters). Before freezing, build the cheapest control that skips the claimed work, score it with the frozen counter … if it meets the target, the counter or target is wrong — fix it before data."

**Command run:**
`cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/w1/scratch/CritAxisClaim && python3 -I controls_critaxis.py > controls-critaxis.txt` (exit 0, 2.47 s). Each control is a branch in the sandbox clone, scored by the lane's frozen counters: `python3 -I quality/counters/c1-r37-event-ground.py --repo <sb> --rev <rev> --base b4e47e9…` and `python3 -I quality/counters/c2-r37-eventq.py --repo <sb> --rev <rev>`. The full transcript is in `controls-critaxis.txt`.

| Control (sandbox rev) | What it is | C1 summary line | C2 summary line |
|---|---|---|---|
| do-nothing-freeze (`893a8aa`) | the v2 freeze commit itself | `admitted=0/2 verdict=TARGET_MISSED` rc=1 | `fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED` rc=1 |
| do-nothing-tip (`80b83c8`) | lane master now | `admitted=0/2 verdict=TARGET_MISSED` rc=1 | `fixtures=0/10 … TARGET_MISSED` rc=1 |
| do-nothing-empty-commit (`1a07422`) | empty sandbox commit on tip | `admitted=0/2 verdict=TARGET_MISSED` rc=1 | `fixtures=0/10 … TARGET_MISSED` rc=1 |
| c1-min-two-rows (`3fa9265`) | E1 cites **only S189**, E2 **only S214**; each body is a header plus one `**OBS**` line quoting two Gate lines. S189 `used-by` extended in place, one new S214 row, 4 Gate lines, 2 index rows. `--stat`: 5 files, +26/−1 | **`admitted=2/2 verdict=TARGET_MET` rc=0** (both entries `a..g=1`, `ids=S189` / `ids=S214`) | `TARGET_MISSED` rc=1 |
| c1-refused-inference (`122cf14`) | as above, but E2 also says: "A zero count of `overflowed event queue` markers in the session log proves that the compositor's event queue has never overflowed on this host." | **`admitted=2/2 verdict=TARGET_MET` rc=0** | `TARGET_MISSED` rc=1 |
| c1-refused-pkg28-verbatim (`9bfe72e`) | E2 is the **refused** package entry `event-queue-host-measurement-r28.md` (sha256 `93f26adf…`, title "Measured: the compositor's event queue has never overflowed on this host") pasted whole, under a 4-line header and one OBS line | **`admitted=2/2 verdict=TARGET_MET` rc=0** | `TARGET_MISSED` rc=1 |
| c1-duplicate-s189-row (`dc8da2a`) | S189 cited through a *second* `| S189 |` row instead of editing the existing one | **`admitted=2/2 verdict=TARGET_MET` rc=0** | `TARGET_MISSED` rc=1 |
| c2-fabricated-live (`2cfffdc`) | a 44-line `tools/mado-eventq.py` written in this seat; `receipts/eventq-live-ss.txt` is a **hand-written 4-line snapshot** (header, LISTEN, one server row, one waybar row at the placeholder path `/run/user/1000/hypr/HIS/.socket2.sock`, never read from the host); `eventq-live.txt` is the tool's output on that file plus `tool_sha256=2c7824dc…` | `TARGET_MISSED` rc=1 | **`fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET`** rc=0 |

**Readings.**
- **Do-nothing: PASS.** Neither counter can be met by leaving the tree alone: 0/2 and 0/10, rc 1, at every do-nothing revision. This agrees with the L1's `controls-v2.txt` (`control=c1-do-nothing … admitted=0/2`, `control=c2-do-nothing … fixtures=0/10`).
- **Separability: holds.** Every C1 crib leaves C2 at `tool=absent` 0/10, and the C2 crib leaves C1 at 0/2. Neither counter reads the other's files.
- **Cheapest skip-the-work, C1: FAIL.** The claimed work is "two event-delivery entries", one being the package entry "re-grounded" and the other a lane entry "replacing the two refused package host measurements" because "a zero there cannot tell 'never overflowed' from 'not logged'" (registration.md:31-35, 88-93). The v2 counter admits:
  - two stubs that carry neither the re-grounding nor the refusal argument;
  - an entry stating the **negation** of the round's key finding;
  - the **refused** r28 entry, verbatim.

  So it cannot tell the assimilation decision (admit r26, refuse r28/r29) from its opposite. The registration says both entries "rest on rows opened this round (S189, S201 re-opened; S212, S213, S214 new)" (registration.md:42-43), but the counter needs only S189 and S214. S213, the host-channel receipt that grounds the refusal, is optional. The L1's own `c1-golden-v2` (a "# synthetic control entry … body naming …" stub plus OBS quotes, `controls.py:50-53`) already met the target. That control *is* the cheapest skip-the-work control, and amendment 1 relabelled it "the accept path" instead of treating it as the kake-r34 failure signal. Clause **g** raised the bar from "tokens" to "tokens plus a restated quote", and a stub still clears it. Smaller gap: clause **c** accepts a duplicate registry id, and the L1's golden also relies on this, because `wire()` appends a second S189 and S201 row.
- **Cheapest skip-the-work, C2: FAIL on `live`.** Amendment 1's replay was added because "a hand-written receipt carrying the right digest passed" (`c2-r37-eventq.py:20-21`). The replay moves the forgery from the receipt to the snapshot. Both files are author-written, so `live=1` proves consistency between two author-controlled files, not that the tool ran against this host. This is kake r34's "no-parse replay" in a new place. The ten fixtures do discriminate: a minimal parser had to be written to pass them, and the L1's stubs top out at 2/10.

**Impacted axes:** coverage (C1 evidence), operability and capability (C2 evidence), calibration (the controls receipt reads 13/13 "correct" while the strongest cribs were never built). **This is a fixable defect, not a tradeoff.** The tradeoff is timing. Per §9 and kumitate r42, "A rule changed after any seat has scored is not the claim's rule", and the registration says "any later change to a counter is a new predicate and the claim it belongs to then fails as declared" (registration.md:6-7). Wave-1 seats have already scored the v2 counters.

**Smallest safe correction (no counter edit):**
1. Commit this seat's five cribs as named controls with their observed verdict `TARGET_MET` and the label "counter limit — does not discriminate". The round record then says, in committed bytes, that v2 `TARGET_MET` is wiring evidence only.
2. For C1, route a non-author content check to wave 2 or the closure. It should confirm: (a) E2 states the refusal ("zero markers ≠ never overflowed" under `disable_logs=1`) and cites S213; (b) E1 carries the overflow→removal edge class; (c) no entry asserts the refused inference.
3. For C2, require a non-author **live** re-run at closure (read-only `ss -xpa` through the committed tool, comparing the subscriber comm set) before the capability row enters.
4. If the L1 prefers a v3 counter (negative clause on the refused sentence, S213 required for E2, unique registry id, live snapshot bound to an independently committed host receipt), the registration's own rule makes v2's claim fail as declared. That choice belongs to the judge, not to this seat.

## 4. Is C2 a capability acquisition by AXES.md's definition?

**Definition** (AXES.md:59-64): "The six axes measure the quality of what the skill knows; they do not measure what the shokunin can now *do*. … Rows enter only through a round that demonstrates the capability running; a capability without a passing demonstration in the round report is pre-claiming and does not enter the table."

**For "capability" (new repertoire).**
- No lane tool reads the unix-socket table or socket2 today: `ls tools/` → `mado-action-plan.py mado-anims.py mado-assessment.py mado-binds.py mado-evidence-audit.py mado-tripwire.py mado-verify.sh mado-wsrules.py`, and `rg -l -F -e 'ss -x' -e socket2 tools quality` → only `quality/counters/c2-r37-eventq.py`.
- A fleet search for `ss -xp` under sibling `tools/` directories returned no match.
- "Report the compositor's event-socket subscribers and their unread backlog without connecting" is something the lane cannot do at base. By type, this is a capability acquisition and an operability move ("scripts that run", AXES.md:13), and the registration correctly says "The capability row enters `SCORECARD.md` only with the passing run" (registration.md:67).

**Against reading the counter as the demonstration.**
- **The demonstration clause is not evidenced by the counter.** `c2-fabricated-live` reaches `live=1 TARGET_MET` with no host contact (item 3). AXES requires "demonstrates the capability running"; under the v2 predicate that can only come from a run the author cannot write, such as a non-author re-run.
- **Half the deliverable cannot be demonstrated live on this host.** The registration describes the tool as reporting "the two failure markers … plus whether those markers are observable at all (`debug:disable_logs`)" (registration.md:48-51). The host has `debug:disable_logs` = 1 (the `S213` quote in `controls.py:32`: `debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}`), and the logger returns before writing (S214 lines 15 and 48: `if (!m_logsEnabled)`, `m_logsEnabled = !*PDISABLELOGS;`). Any live run therefore prints `markers_observable=no` (case `logs-disabled`). Overflow and write-fail detection are demonstrated only on fixtures. A capability row saying "detects event-queue overflow" would pre-claim; the demonstrable row is "subscriber census plus per-subscriber backlog, with marker observability reported".
- **The published operability axis cannot register it.** Operability is published as `check-index.py --selftest` 12/12 (`check-axis-scores.py:14`). The per-axis verdict must come from the C2 counter, not the axis table.

**Verdict:** C2 qualifies as a capability acquisition by type. Its demonstration is not established by `PRED-C2-r37-v2`, and only the census half is demonstrable on this host. **Impacted axes:** operability and capabilities (pre-claiming risk). **Smallest safe correction:** scope the row to "read-only event-socket subscriber census (comm/pid/fd, peer Recv-Q, server Send-Q); markers reported as unobservable while `debug:disable_logs`=1". Enter it only after a non-author read-only live re-run of the committed tool. The fixture-only marker detection belongs in the row's limits, not its capability text.

---

## Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/w1/scratch/CritAxisClaim
python3 -I controls_critaxis.py        # rebuilds the sandbox branches if /dev/shm/mado37-CritAxisClaim/sb is absent; prints the table above
```

The sandbox `/dev/shm/mado37-CritAxisClaim/sb` holds branches `ctl-<control>` at the revisions quoted above, for any peer to re-score. Nothing in the lane, the fleet repo, a compositor or a config tree was written or touched.
