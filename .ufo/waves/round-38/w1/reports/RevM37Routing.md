# RevM37Routing — is M37-5 fully discharged? (round 38, wave 1)

Seat: reviewer, mado round 38 wave 1. Leaf member; no subagents dispatched. Date 2026-10-25.
Scope: the M37-5 routing chain — `corpus/lessons/round-37.md` M37-5 → the two wave-1 attack
reports (`.ufo/waves/round-37/w1/reports/CritC1Cheap.md`, `RevC2Code.md`) → the landed round-38
v3 instruments (`quality/counters/c1-r38-event-ground.py`, `quality/counters/c2-r38-eventq.py`,
`quality/counters/c2-r38-request-ground.py`, `quality/check-r38-discrimination.py`,
`.ufo/waves/round-38/controls/manifest.json`). Question: does **every crib the two reports
demonstrated** have a named killer in the landed v3 clause set or the frozen manifest — and does
the killer actually kill?

Lane touched READ-ONLY. No tool installed (record: none). Scratch: `/tmp/mado38-RevM37Routing/`
(sandbox clone + drivers + gate outputs); no lane writes except this report.

**Revisions reviewed:** discrimination replays at `3f14bd2` (the errata commit). The lane moved
to `b8400aa` (gate sandbox confinement, SentManifestScope HIGH) and `ff81aaf` (flags-entry seat
fix) mid-review; neither touches a counter or the manifest, and the accept paths were re-verified
at `ff81aaf` (§5). All gate/counter outputs below are my own runs unless marked "committed".

## Verdict (TLDR)

**ROUTED-COMPLETE.** All six M37-5-named cribs (receipt-not-pinned, quote-no-floor,
non-unique-rows, forged snapshot, docconn trap, fixture gaps) plus every additional crib the two
reports demonstrated (k0/k3/k5, r28-verbatim, `x` headers, golden-v2 append-rows wiring,
whole-line `tool_sha256`) have a named killer in the landed v3 clauses or manifest controls, and
I re-ran the exact demonstrated crib trees and the full 19-control gate: every crib rejects, both
accept paths hold. No demonstrated crib is left without a named killer. The residual list (§6)
is declared tradeoffs, out-of-scope LOW/design items, pending wave-1 demonstrations for the
domain counter, and the already-declared governance errata — none of it is an un-routed
demonstrated crib. Two findings refine the record (§5A refutes one RevCommitChain claim; §5B is
a new honest-kill demonstration).

## 1. The routing chain, as landed

M37-5 (round-37 lesson, "Mistakes"): *"routed: next counter binds each Gate receipt to `fetch/`
and to a re-fetch digest, and cross-checks a live snapshot against `/proc/net/unix` server
inodes."* Round-38 registration §"Routed defect being worked" names the v3 design; freeze
`58e55ec` (09:40, committer 11:06) landed the three counters + manifest + fetch receipts + live
triplet; data `245065c`/`efb0ec2` (11:08–11:09); post-freeze patches `859d0cf` (c1 clause-c
uniqueness, 11:10) and `b6c1d31` (manifest: c1-duprow in-table insert, 11:12); errata `3f14bd2`
(11:18) declares the frozen claim failed as declared (18/19) and routes the 19/19 to
re-registration closure.

## 2. C1 cribs (CritC1Cheap) → killers

| # | Demonstrated crib (report pointer) | v3 killer (file:line) | Manifest control | My verification |
|---|---|---|---|---|
| F1 | **receipt-not-pinned** — `k2_self_receipt`: 19-line tree, fabricated `S999`, each entry its own Gate receipt (report §cribs table, counter v2 :144-149) | **clause h** — every cited id needs a `## Gate` line whose (receipt path, sha256) equals the frozen `PINS` entry; d/f/g score only pin-matching gates (`c1-r38-event-ground.py:67-88` PINS, `:211-225` h/j, `:229-241` d/f/g) | `c1-selfreceipt` expect MISSED, clause h | Re-ran the report's own `cribs.py` `k2` tree against the landed v3: `h=0 d=0 f=0 g=0 k=0 … admitted=0/2 verdict=TARGET_MISSED`. Gate: `c1-selfreceipt … observed=TARGET_MISSED ok=1` |
| F2 | **quote-no-floor** — quote `"e"` or the bare token `MAX_QUEUED_EVENTS` satisfied v2 d+g (report F2, `k1`/`k2`) | **clause i** — `quote_floor_ok` rejects frozen surface tokens and bare `S`-ids, requires ≥3 words or ≥24 chars (`:149-153`) | `c1-quotefloor` expect MISSED, clause i | `k1` → `h=0` (token quote); `k2` → `h=0` (`"e"`); gate `c1-quotefloor … ok=1` |
| F3 | **non-unique-rows** — appended contradicting S189 row passed v2 clause c (`rows.setdefault(...).append` + `any(...)`) (report F3) | **clause j** — exactly one Registry row per cited id (`:226`); **clause c** also unique post-`859d0cf` (`:203`) | `c1-duprow` expect MISSED, clause j (in-table insert after `b6c1d31`) | `k1` → `c=0 j=0`; gate `c1-duprow … ok=1`. **Frozen counter + fixed manifest also rejects it** (§5A) |
| F4 | golden-v2 control wiring relies on F3 (`controls.py wire` appends rows instead of extending `used-by`) (report F4) | same clause j/c uniqueness; the honest extend-`used-by` wiring is the accept path | `c1-live` (accept) + `c1-duprow` (reject) | Re-ran `k0_golden_v2` (the report's rebuild of golden-v2): `c=0 j=0 … admitted=0/2 verdict=TARGET_MISSED`; landed lane at tip: `c=1 j=1` both entries, `admitted=2/2 verdict=TARGET_MET` |
| F5/k5 | **stated-quote stub** — `k5`: honest-proxy E1 + 3-line E2 stating real quotes (report §clause test, "residual") | **clause l extended to E2** — 2 of 3 frozen mechanism phrases ("null channel", "returns before", "core-logger") (`:87-97` LINEAGE, `:262-264` scoring) | `c1-nolineage` covers the k3 form; no dedicated k5 control | `k5` → E2 `l=0 lineage=0/2` (also `k=0`: `verified-at: x`) → `admitted=1/2 verdict=TARGET_MISSED`. **The demonstrated k5 tree is killed.** The residual (stub + mechanism phrases) is the declared accept-path tradeoff (counter docstring; registration §C1 Residual) |
| F7/k3 | **receipt-reading lift** — `k3`: E2 lifts S213's own "reading" sentence (report F7) | **clause l** (E2 mechanism phrases) — k3's lifted wording carries none of the three | `c1-nolineage` ("the k3 crib: stated real quotes, no package claim content") | `k3` → E1 `l=0 lineage=1/4`, E2 `l=0 lineage=0/2` → `admitted=0/2 verdict=TARGET_MISSED`; gate `c1-nolineage … ok=1` |
| (k2 note) | `verified-at: x` / `recheck: x` passed v2 clause b (report §"work the crib skips") | **clause k** — `DATE_RE`/`RECHECK_RE` must parse (`:100-101`, `:196-201`) | `c1-clause-b` (missing verified-at; the k family) | `k1`/`k2`/`k3`/`k5` all show `k=0`; gate `c1-clause-b … ok=1` |
| (M37-1) | token-only stub (held discrimination) | **clause g** — verbatim quote stated in body + `**OBS**` line naming the id (`:243-247`) | `c1-token-stub` | gate `c1-token-stub … ok=1` |
| F6 | honest-kill risk: renumbered-only package entry fails g (report F6) | not a crib — routed by the landed entries (OBS line per id + verbatim quote) and the `c1-live` accept control | `c1-live` expect MET | `h1_pkg_renumbered` → E1 `g=0` → MISSED (correct: renumbering alone is not re-grounding); landed E1 at tip `g=1 l=1 lineage=6/4` |

## 3. C2 cribs (RevC2Code) → killers

| # | Demonstrated crib (report pointer) | v3 killer (file:line) | Manifest control | My verification |
|---|---|---|---|---|
| F1 | **forged snapshot** — the counter's own `CLEAN_SS` fixture committed as `eventq-live-ss.txt` scored v2 `TARGET_MET` (report F1, scenario `ref-forged-fixture`) | **live-v3 three-artifact clause** (`c2-r38-eventq.py:190-252`): snapshot byte-unequal to both embedded fixtures (`:199-200` `snapshot-is-fixture`), replay consistency (client triples + `subscribers` count, `:214-223`), full-table requirement (`:226-229`), `/proc` binding — `ss_sha256=` of the snapshot, every socket2 server inode named as compositor-held, `OVERALL: AGREE` (`:231-245`) | `c2-forged` (CLEAN_SS as snapshot → MISSED), `c2-proc-mismatch` (fabricated inodes → MISSED) | gate: `c2-forged … ok=1`, `c2-proc-mismatch … ok=1` at both 3f14bd2 and ff81aaf |
| F2 | **whole-line `tool_sha256`** false-missed a genuine prefixed receipt (report F2, scenario `ref-live-prefixed-sha`) | **substring match** — `"tool_sha256="+digest in l` for any line (`:216-217`) | none dedicated; exercised via `c2-live` accept and `c2-docconn`'s sha-update write | **Probe**: prefixed the real receipt's line to `MADO_EVENTQ_RECEIPT: tool_sha256=…`, committed in sandbox → `live-detail replay=1 sha=1 full_table=1 proc=3/3` → `fixtures=14/14 readonly=1 live=1 verdict=TARGET_MET`. Fix verified; see §5D for the control gap |
| F3 | **fixture gaps** — all v2 fixtures server-first, no `users`-less row, no two-tuple server `users`, no comm with spaces; one-pass parser passed fixtures (report F3, `onepass-*`) | **four new fixture cases** (`:99-127`): `clients-first` (LIVEORDER_SS, clients before servers), `client-no-users` (CLI_NU), `comm-spaces` (CLI_SP), `expect-present`; two-tuple server rows (SRV_W) in both fixture tables (`:147`); `clean` now also asserts `lagging=0` | `c2-onepass` (one-pass mutant vs clients-first → MISSED) | **Mutant re-run**: applied the control's exact one-pass mutation to the real tool → `case=clients-first … ok=0`, `fixtures=8/14 … verdict=TARGET_MISSED` — intrinsic fixture discrimination, not a receipt artifact |
| F4 | **lagging undiscriminated** — constant `lagging=1` met v2 (report F4, `lagconst-live`) | `clean` asserts `lagging=0` (`:103`); `lagging` case asserts `peer_recv_q=2048` + `lagging=1` (`:121-124`) | `c2-lagconst` | **Mutant re-run**: `lagging = 1` → v3 `case=clean … ok=0`, `fixtures=13/14 … TARGET_MISSED` (intrinsic). Notably v2 rejected the *control* only via the stale `tool_sha256` (see §5C) |
| F5 | **`--expect-client` no positive case** — always-missing met v2 (report F5, `missall-live`) | **`expect-present` case** — waybar+socat present, both expected, `missing_client=- ` required (`:103-105`) | `c2-missall` | **Mutant re-run**: `missing = list(dict.fromkeys(a.expect_client))` → `case=expect-present want_rc=0 rc=1 ok=0`, `fixtures=13/14 … TARGET_MISSED` (intrinsic) |
| F6 | **docconn trap** — v2's readonly text heuristic false-missed a genuine tool whose docstring says "connect(" (report F6, `docconn-live` → `TARGET_MISSED`); `import socket` bypassed it (`impsock-live` → MET) | **comment/docstring-aware scan** — `code_lines()` strips full-line comments, inline `#`, and the module docstring (`:177-187`); clause scans code only for `import socket`/`from socket` and `connect(` (`:283-285`) | `c2-impsock` expect MISSED, `c2-docconn` expect **MET** (accept) | gate: `c2-impsock … ok=1`, `c2-docconn … observed=TARGET_MET ok=1` at both tips |

## 4. The domain counter (C2-r38-v1) carries the same killer set

`c2-r38-request-ground.py` implements the M37-5 repairs directly: pins `d` bound to
`.ufo/waves/round-38/fetch/` by (path, sha256) with at-score re-hash (`:63-74`, `:190-205`),
quote floor inside `g` (`:148-152`, `:206-215`), unique rows inside `c` (`:185-190`), header
parse inside `b` (`:179-184`), lineage `l` (`:78-92`). Verified at tip `ff81aaf`:

```
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md … l=1 ids=S221 lineage=3/3 ok=1
PRED-C2-r38-v1 entry=corpus/knowledge/request-socket-live-bound-r8.md … l=1 ids=S158,S187,S258,S277 lineage=5/3 ok=1
PRED-C2-r38-v1 entry=corpus/knowledge/request-limits-upstream-r31.md … l=1 ids=S253 lineage=5/3 ok=1
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=ff81aaf…
```

Its **crib demonstrations** (junk rows, wrong digest, self-receipt, stated-quote stub,
unindexed, refused-paste) ride wave-1 seats per registration §Controls — at review time only
`RevCommitChain.md` and `RevLiveTriplet.md` are landed in `w1/reports/`; the domain crib seats
have not reported. Killers present, demonstrations pending (§6 item 7).

## 5. Findings

**A — Refinement of RevCommitChain F3: the post-freeze counter patch was NOT load-bearing
(verified).** RevCommitChain F3 claimed "Only the post-freeze counter patch **and** crib fix
together yield 19/19" and left the frozen-pair replay as a gap. I ran both replays:

- Frozen pair × frozen manifest (`58e55ec` instruments + `58e55ec` manifest, rev `3f14bd2`):
  `MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED` — sole failure
  `control=c1-duprow … observed=TARGET_MET ok=0`. **Confirms the errata's 18/19 claim
  empirically** and closes their declared gap.
- Frozen c1 × current c2 × current manifest, rev `3f14bd2`:
  `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`.

So the frozen c1 counter (whose clause j already enforced uniqueness at freeze —
`c1-frozen.py:223`) rejects the in-table duprow crib; the load-bearing post-freeze change was
the **manifest control fix alone** (`b6c1d31`). The `859d0cf` counter patch was redundant with
clause j — it breached the freeze contract (registration:6-7) without changing any control
outcome. For the re-registration ruling: the "new predicate" 19/19 is reachable with the frozen
counter; only the manifest control needed amending. (RevCommitChain F1/F2 — the breach happened
— stand; the errata already declares them.)

**B — NEW: the v3 E2 lineage floor honest-kills the round-37 honest proxies (demonstrated).**
Re-running CritC1Cheap's own builders against the landed v3 counter:

```
== h2_honest rev=3a60616 rc=1
   … entry=event-delivery-limits-r26.md … l=1 lineage=7/4 ok=1
   … entry=event-queue-observability-r37.md … l=0 ids=S213,S214 lineage=1/2 ok=0
   … admitted=1/2 verdict=TARGET_MISSED
== h3_honest_trimmed rev=93f52d9 rc=1   (same shape: E2 lineage=1/2)
```

The honest proxies' E2 (`E2_HONEST` — a genuine lane-authored observability entry) carries only
1 of the 3 frozen mechanism phrases ("core-logger" yes; "null channel", "returns before" no).
The landed E2 carries exactly 2/3 (`grep -ic` on the tip: `null channel: 1`, `returns before: 0`,
`core-logger: 2`). So the accept path is calibrated to the landed vocabulary: an honest
re-grounding of these entries in fresh words fails clause l. CritC1Cheap F6 warned exactly this
for E1 ("the phrase list must be frozen together with that threshold"); it materialized on the
E2 side. The registration declares only the fabricated-residual, not the paraphrase-kill.
Severity LOW-MEDIUM, future-facing (the landed entries pass with margin E1 6/4, E2 2/2; the
clause pattern is reusable in later rounds).

**C — NEW (interpretation): the before receipt's v2 rejections of c2-lagconst/c2-missall/
c2-onepass are sha-staleness artifacts, not discriminations.** The before receipt
(`before-discrimination-v2.txt`, committed at freeze) shows v2 "correctly" rejecting those three
controls. I replicated the c2-lagconst control by hand (mutant tool, honest receipt) and ran the
v2 counter: `fixtures=10/10 readonly=1 live=0 … TARGET_MISSED` — the rejection comes from v2's
whole-line `tool_sha256` check failing against the mutated tool's digest, i.e. the same
incidental staleness RevC2Code F2 criticized, **not** from any lagging discrimination (v2's
`clean` case has no `lagging=0` assertion — verified at `c2-r37-eventq.py:66-73`). RevC2Code's
self-consistent demonstrations (`lagconst-live` etc. → MET) remain the truth about v2. The v3
fixture cases close the self-consistent forms intrinsically (my mutant re-runs, §3). No action
needed; this corrects how the before receipt should be read.

**D — Minor: no manifest control exercises the prefixed `tool_sha256` form.** F2's fix
(substring) is verified by code read and my probe (§3), and `c2-live`/`c2-docconn` exercise the
plain form, but no frozen control pins the prefixed-line acceptance. If the clause regresses to
a whole-line test, the manifest stays green. Cheap addition for a future manifest revision.

**E — Info: readonly bypass variants beyond the two demonstrated forms remain open.** The v3
clause kills plain `import socket`/`from socket` and code-level `connect(`; the variants
RevC2Code's probe list demonstrated (`__import__('socket')`, `importlib.import_module('socket')`,
`asyncio.open_unix_connection`, `subprocess` socat) still pass it. RevC2Code F6 itself declared
this ("Reviewers must read the tool for indirect socket use: the counter cannot"); the v3
docstring claims only the demonstrated forms. Residual, not a routing gap.

**F — Infrastructure note: one gate run scored 17/19 on two transient `clone-failed` controls.**
My first current-pair run at `3f14bd2` had `c1-live`/`c1-donothing` `observed=ERROR note=clone-failed`
(three gate runs cloning the lane concurrently); the clean re-run scored 19/19. The gate's
clone-failure path is honest (ERROR, ok=0), but a transient clone failure is indistinguishable
from a real one in the receipt. No action required for this round.

## 6. Residual list (none is an un-routed demonstrated crib)

1. **Declared accept-path tradeoffs** (registration §C1 Residual + both v3 docstrings): a fully
   fabricated self-consistent artifact set (invented lineage phrases; invented inode triples
   repeated identically across ss + proc + receipt) still passes; a stated-quote stub that adds
   the mechanism phrases passes clause l. Declared, not hidden.
2. **F7 (design, unchanged):** `logs-disabled` still requires `verdict=CLEAN` exit 0 with
   `markers_observable=no` — the machine form of the refused r28/r29 inference, mitigated only
   by the tool's documented semantics (`markers_observable=no` means "not logged", not "never
   overflowed"; RevLiveTriplet re-verified the semantics live). Not named in M37-5; out of the
   routing's scope.
3. **F8/F9/F10 (LOW, unchanged):** `unparseable` redundancy; journal fixture still in `-o cat`
   shape while the registered live default prefixes lines (fixture byte-identical v2→v3 — my
   grep); `--socket2` never passed, tool subprocess inherits ambient env
   (`HYPRLAND_INSTANCE_SIGNATURE`/`XDG_RUNTIME_DIR` set on this host), fixture identities are
   this host's live subscribers. All unregistered interface constraints on the tool; none named
   in M37-5.
4. **I1 (privacy, resolved by decision):** the committed `eventq-live-ss.txt` is a full 1011-line
   `ss -xpa` dump (host-wide comm/pid/paths); the v3 full-table clause *requires* ≥1 non-socket2
   row, so the lane chose robustness over redaction deliberately (docstring: "it must name a
   request-socket or unrelated row too"). Accepted risk; worth a line in the round's privacy
   notes if the lane keeps full-table snapshots as a pattern.
5. **Domain-counter crib demonstrations pending:** registration §Controls routes six domain
   cribs to wave-1 seats; not yet landed at review time. The killers exist in the counter's
   clause set (§4); the demonstrations are open work for the round's closure.
6. **Governance (already declared by errata `3f14bd2`):** post-freeze counter patch `859d0cf` +
   post-data manifest rewrite `b6c1d31` → the frozen claim fails as declared (18/19, my replay
   confirms); the landed 19/19 is a new predicate routed to re-registration closure. My §5A
   refinement narrows what the closure must rule on: the manifest control fix alone was
   load-bearing; the counter patch was dead weight.
7. **Lineage-floor paraphrase sensitivity (§5B):** future honest re-grounds of the round-37
   entries must reuse the frozen vocabulary or fail clause l. Declared-adjacent (the docstring
   calls l "a floor, not a proof of comprehension") but the honest-kill side is not declared.

## 7. Verification record (my runs)

| run | instruments | manifest | rev | result |
|---|---|---|---|---|
| gate | current pair | current | `3f14bd2` | **19/19 TARGET_MET** (clean re-run; first attempt 17/19, two transient clone-failures) |
| gate | frozen c1 + current c2 | current | `3f14bd2` | **19/19 TARGET_MET** |
| gate | frozen pair | frozen (`58e55ec`) | `3f14bd2` | **18/19 TARGET_MISSED** (c1-duprow observed MET) |
| gate | current pair (confined gate `b8400aa`) | current | `ff81aaf` | **19/19 TARGET_MET** |
| c1 direct | landed v3 | — | `3f14bd2`, `ff81aaf` | `admitted=2/2 verdict=TARGET_MET` (E1 lineage 6/4, E2 2/2) |
| domain direct | landed v1 | — | `3f14bd2`, `ff81aaf` | `admitted=3/3 verdict=TARGET_MET` |
| crib re-run | CritC1Cheap's `cribs.py` cases × landed v3 c1 | — | base `b4e47e9` | k0/k1/k2/k3 → `0/2 MISSED`; k5/h2/h3 → `1/2 MISSED`; h1 → MISSED (E1 g=0) |
| mutants | lagconst / missall / onepass × v3; lagconst × v2 | — | tip | v3: `clean`/`expect-present`/`clients-first` fail (intrinsic); v2 lagconst: `live=0` via stale sha (incidental) |
| F2 probe | prefixed `tool_sha256` receipt × v3 | — | tip | `live=1 sha=1` → MET |

Commands (representative): `python3 -I quality/check-r38-discrimination.py --c1 <counter>
--c2 <counter> --manifest .ufo/waves/round-38/controls/manifest.json --rev <rev>`; crib re-run
driver `/tmp/mado38-RevM37Routing/rerun_c1.py` (imports the report's own
`.ufo/waves/round-37/w1/scratch/CritC1Cheap/cribs.py` builders unmodified, scores with the
landed v3 counter). All git writes in my own sandbox clone
(`/tmp/mado38-RevM37Routing/sb`, identity `s <s@i>`); no lane mutation, no socket connection, no
compositor/config/service touch, no tool installs.

## 8. Addendum — independent verification and one unreproduced claim (post-report)

RevCommitChain independently replayed my §5A configurations at three revs (`efb0ec2`,
`58e55ec9`, HEAD-manifest variants; their scratch
`.ufo/waves/round-38/w1/scratch/RevCommitChain/revm37routing-verification.md`): frozen trio →
**18/19, c1-duprow sole failure** (matches my `gate-frozen-pair.txt`); frozen c1/c2 × fixed
manifest → **19/19** (matches my `gate-frozenc1-currentman.txt`). §5A stands, now doubly
reproduced.

Two items for the closure ruling:

1. **Unreproduced conflicting claim.** RevCommitChain reports a third-party claim (RevCensusBefore)
   of "frozen pair 19/19 at freeze rev" that neither of us can reproduce — frozen pair × frozen
   manifest scores 18/19 at the freeze rev too (SOURCES.md ends `## Registry` → `## Paths` →
   `## Leads (unopened)` at every rev, so the frozen crib's EOF append lands outside `## Registry`
   at every rev; the distinguishing variable is manifest version, not rev). Their 19/19 matches
   frozen counters × FIXED manifest. The ruling should ask RevCensusBefore for the exact command
   before relying on that number.
2. **Clause-location clarification.** RevCommitChain's note "no h2/h3 or E2 clause exists in the
   round-38 instruments/manifest" is half-right: no *manifest control* exercises h2/h3 (my §5B
   says the same), but the E2 lineage clause DOES exist in the round-38 instrument — the v3 C1
   counter's clause l carries an E2 floor (`LINEAGE["corpus/knowledge/event-queue-observability-r37.md"]
   = (2, ["null channel", "returns before", "core-logger"])`, `c1-r38-event-ground.py:87-97`),
   which is exactly what rejects the h2/h3 honest proxies (`lineage=1/2`). The honest-kill
   finding is about the counter's calibration, not a missing control.
