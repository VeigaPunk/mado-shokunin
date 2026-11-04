#!/usr/bin/env python3
"""Generate `.ufo/waves/round-80/w1-spec.json` (one v1 wave, 14 seats).

Seat paths are absolute; the runner renders a relative `Report:` trailer that a seat must
resolve from the lane root, and the context says so. Nothing here is a claim: the claim
contract lives in `.ufo/waves/round-80/claims-declaration-r80.md` (frozen at
`6c302a53eb8f577e83fbcadc01e05a286778df8e`).
"""

import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROUND = LANE + "/.ufo/waves/round-80"
FREEZE = "6c302a53eb8f577e83fbcadc01e05a286778df8e"
BASE = "e10f7e9f528b13195a1cdde28a68a702af3045c4"
SCRATCH = "/fast/scratch/hyaku/mado-r80"

DIRECTIVE = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = DIRECTIVE + """
Round mado 80, ONE v1 wave (14 seats). Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin.
Claims (frozen; declaration {ROUND}/claims-declaration-r80.md, freeze `{FREEZE}`, base `{BASE}`):
C1 coverage — a second exclusive layer surface composes under the running usable box: 33 frozen
cases (23 carried from round 79 unchanged + 10 composition cases), 22 named mutations killed, the
held round-79 tool `base_correct=23/33`, tool selftest 111/111; C2 operability — the runbook gains a
chord grammar over the keybindings chord column and a state/exit-status matcher: 24 cases / 24 rows
/ 24 distinct anchors, `control_new=0/2`, 16 matcher mutants killed.

Frozen instruments (never rewritten by a seat):
- {ROUND}/../tools/mado-barfoot.py  -> {LANE}/tools/mado-barfoot.py, r80-v1, sha256 c3eb5fbe…
- {LANE}/quality/counters/c1-r80-multisurface.py  sha256 6268667c…  (selftest 60/60)
- {LANE}/quality/counters/c2-r80-runbook.py       sha256 462287fb…  (selftest 80/80)
- {ROUND}/controls/c1-cases-r80.json  sha256 17c27157…   (33 cases)
- {ROUND}/controls/c2-runbook-cases-r80.json  sha256 f1dfb5f4…  (24 cases)
- {ROUND}/receipts/measurement-c1-r80.txt and measurement-c2-r80.txt (both TARGET_MET at {FREEZE})

Counting commands (run from the lane root; copy them exactly):
C1: python3 -I quality/counters/c1-r80-multisurface.py --repo . --rev {FREEZE} --base-rev {BASE} --controls .ufo/waves/round-80/controls/c1-cases-r80.json --carried .ufo/waves/round-79/controls/c1-cases-r79.json --scratch-root {SCRATCH}/<your-name>
C2: python3 -I quality/counters/c2-r80-runbook.py --repo . --rev {FREEZE} --controls .ufo/waves/round-80/controls/c2-runbook-cases-r80.json --carried .ufo/waves/round-79/controls/c2-runbook-cases-r79.json --scratch-root {SCRATCH}/<your-name>

Bounds for every seat (violating one voids the seat):
- Write ONLY inside {ROUND}/w1/<your-name>/ . Never commit, never push, never run a mutating git
  or jj command anywhere, never edit the frozen instruments, the control sets, SKILL.md,
  SCORECARD.md, LOG.md, corpus/, the fleet repo or any sibling lane.
- Every `Report:` trailer path the runner prints is relative to the LANE ROOT — write it at
  {LANE}/<that path>. Your findings file is {ROUND}/w1/<your-name>/findings.md.
- Scratch root: {SCRATCH}/<your-name>/ (create with mkdir -p, pass it explicitly; never use /tmp for
  anything a report must point at). Remove your scratch dir before you finish:
  `trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python; if you cannot, say so.
- Read-only host discipline: no config write, no compositor mutation, no service restart, no
  package transaction. The lane's own rule (QUALITY 21) holds: no host probe that is not a read verb.
- Tooling authorization (operator 2026-10-19): you may install/upgrade tools that help your item —
  official channels only (uv tool / npx / official binary in ~/.local/bin); pacman transactions are
  PAUSED host-wide: never run pacman -S/-Sy/-Syu/-U/-R or restart a host service.
- Never message agent://all. No seat runs its own swarm; an executor may spawn at most one read-only
  labrat probe. A dead end is reported as a dead end; never fabricate a number you did not observe.
- End your findings.md with `STATUS: ok | partial | blocked` plus one line of what is missing.
"""

ITEMS = [
    {
        "name": "R80ScoutModel",
        "role": "scout",
        "prompt": """Source recon for the C1 composition model (read-only, no code).

1. Read {ROUND}/fetch/S470.bin (Hyprland 0.56.2 `Renderer.cpp`) and locate with line numbers:
   `applyExclusive` (the four-rule loop, the `exclusiveEdge == singular || anchor == singular ||
   anchor == triplet` condition, the `zone + margin > 0` guard, which axis each edge moves),
   `arrangeLayerArray` (bounds selection `full_area` vs `*usableArea` for exclusive -1, the
   empty-box `continue`, margin application, `applyExclusive` call order) and
   `arrangeLayersForMonitor` (the `RESERVED_DYNAMIC_TYPE_LS` reset, the exclusive pass before the
   non-exclusive pass, the single `addType(..., CReservedArea{ORIGINAL, usable})`).
2. Read {ROUND}/fetch/S471.bin (`LayerShell.cpp`) for `set_exclusive_edge`'s alignment error and
   `set_exclusive_zone`'s stored value; read {ROUND}/fetch/S472.bin (`tests/desktop/Reserved.cpp`)
   for the upstream assertions on `CReservedArea{parent, child}` and `addType`.
3. Enumerate EVERY model class the frozen 33-case set does NOT cover (be specific: a cross-axis
   overflow with a valid area, a layer surface whose `preview_scale` differs, two surfaces of the
   same namespace on one level, a non-exclusive surface whose box is empty, `addType` saturating
   under two dynamic types, a monitor with a non-zero `x`/`y`, a static reserve on the SAME edge as
   the bar). For each: the source line that decides it and whether the tool gets it right
   (`python3 -I tools/mado-barfoot.py --selftest`, then reason).
4. Do NOT edit anything. Write findings.md: a table of class | source anchor | tool behaviour |
   covered by a frozen case? (yes: case name / no).

You may contradict the round; a real defect found here is worth more than agreement.""",
    },
    {
        "name": "R80ScoutLive",
        "role": "scout",
        "prompt": """Live surface recon for the C1 join (read-only probes; no config write).

1. Capture once into YOUR directory: `hyprctl monitors -j > monitors.json` and
   `hyprctl layers -j > layers.json`; copy `~/.config/waybar/config.jsonc` (read) beside them.
2. Run the frozen join against the host:
   `python3 -I tools/mado-barfoot.py --config <copy> --layers layers.json --monitors monitors.json --monitor DP-1`
   and record the module's README/registration expectation of the verdict (CLEAN, DIFFER, …).
   Then run it a second time with a `--surfaces` declaration that describes the real OVERLAY
   levels: read `layers.json`, and for every namespace that is not `waybar`/`wallpaper` write a
   surface entry with the box you observed (use `anchor` and `exclusive` you can justify; if you
   cannot justify one, say so instead of inventing it).
3. Report what the host actually has on each level today (namespaces, boxes, pids), whether any
   second exclusive consumer exists, and what the join prints for the unattributed part of the
   `reserved` array. If the host has no second exclusive surface, say exactly that — that is the
   honest result and it is the point of the C1 limit statement.
4. Also verify the C2 `is-active` row's real answer here: `systemctl --user is-active hypridle` with
   its exit code, and one second unit that is `active` if one exists (else say none).

Write findings.md with the captured bytes' paths, the exact commands and their output lines.""",
    },
    {
        "name": "R80ExecC1Run",
        "role": "executor",
        "prompt": """Re-run the C1 counting command and re-derive three expectations by hand.

1. Run the C1 counting command from the context verbatim at `--rev {FREEZE}` and save the full
   output in your directory as c1-after.txt; record the exit code.
2. Independently re-derive, with arithmetic you show, the expected `band`/`expected`/`attributed`/
   `attr` of `overlay-compose-top`, `same-level-order` and `ls-area-invalid` straight from
   {ROUND}/fetch/S470.bin (line numbers required) — do NOT read the tool's code to do this; read
   the compositor's.
3. Then run the tool yourself on those three cases (build the config/layers/monitors/surfaces JSON
   files in your directory from the control set) and compare its output with your derivation.
4. Run `python3 -I tools/mado-barfoot.py --selftest` and the C1 counter's `--selftest`.
5. Write findings.md: the command lines, exit codes, your three derivations, the tool's three
   outputs, and a verdict per case (AGREE / DISAGREE with the exact differing field).""",
    },
    {
        "name": "R80ExecC2Run",
        "role": "executor",
        "prompt": """Re-run the C2 counting command and test the two new rows against the real replies.

1. Run the C2 counting command from the context verbatim at `--rev {FREEZE}`; save c2-after.txt and
   the exit code.
2. Capture the two new rows' real output into your directory:
   `omarchy menu keybindings --print | cut -c1-35 > chords.txt` and
   `systemctl --user is-active hypridle > state.txt; echo $? > state.rc`.
3. Write a SMALL independent checker (python, in your directory) that parses chords.txt with the
   grammar the declaration states (1–4 distinct words from SUPER/SHIFT/CTRL/ALT, ` + `, one key; or
   a bare key) and reports: total lines, chord lines, bare lines, the set of modifier tuples, and
   every line that fails. Compare its count with the counter's `min_chords` assumption (≥100).
4. Tabulate the distinct bare-key forms you see and say whether any could be mistaken for a chord.
5. Write findings.md with the counts, the failing lines (if any), and the state row's word+rc pair.""",
    },
    {
        "name": "R80ExecMutants",
        "role": "executor",
        "prompt": """Mutation-test the two counters' own load-bearing checks (the round-79 R79MutC1 pattern).

For each of these checks, copy the counter into your directory, remove the check with a single
minimal edit, and re-run the mutant against the frozen artifacts; then say whether the mutant still
prints TARGET_MET (a hole) or TARGET_MISSED (the check bites):
C1 counter: (a) the `cases[:CARRIED] == carried` assertion, (b) the `base_correct == BASE_EXPECT`
clause of the target, (c) the `selftest_ok` clause, (d) the `ls` field comparison in `expected_ok`.
C2 counter: (e) the `documented != case["skill_anchor"]` argv check, (f) the `tree=bound` sha check
of SKILL.md, (g) the `control_new == CONTROL_NEW` clause.
Then, for each hole you find, build ONE tamper probe (a tampered artifact set, a base pointed at the
freeze, a wrong argv, a stale tree) that the unmodified counter accepts or rejects, and say plainly
which holes are *unexercised* versus *absent*. Do not edit the lane's counter; work on copies.
Write findings.md: table of check | mutant verdict | hole? | tamper probe result.""",
    },
    {
        "name": "R80ScribeEntry",
        "role": "scribe",
        "prompt": """Draft the round's knowledge entry (prose only; the L1 lands it).

Write {ROUND}/w1/R80ScribeEntry/bar-footprint-composition-r80.md, the exact bytes the L1 can adopt
as `corpus/knowledge/bar-footprint-composition-r80.md` after review. Requirements:
- The provenance trio first: `source:` (rows S470, S471, S472 plus the held S457/S459/S466/S465),
  `verified-at:` the freeze commit, `recheck:` a command.
- Propositions with source anchors, one per model rule: level order and the running usable box;
  the exclusive/non-exclusive pass split and `bounds` selection for `exclusive == -1`; the
  four-rule match order and the `exclusiveEdge`/anchor/triplet condition; the `zone + margin > 0`
  guard; the empty-box skip; the single `CReservedArea{ORIGINAL, usable}` total and its early
  return (empty child or not contained) zeroing the whole layer reserve; and that the compositor
  never attributes a band to a surface (so ATTRIBUTED is the join's model and GT is the reply).
- A limits section that names what the entry does NOT claim (no per-surface attribution on the
  host, rule order `order()` only modelled as a declared integer, `preview_scale` unmodelled,
  cross-axis overflow with a valid area unmodelled, no runtime probe).
- Every number carries its command and the revision. No credential material, no `op://`, no
  times that are not UTC-marked.
Do not write anywhere else; do not edit corpus/. Cite `S470`-style ids exactly.""",
    },
    {
        "name": "R80ScribeSources",
        "role": "scribe",
        "prompt": """Draft the SOURCES.md rows for this round (prose only; the L1 appends them).

Read {LANE}/corpus/SOURCES.md's Registry table shape and {LANE}/corpus/lessons/round-79.md's
`## Gate` for the house style. Then draft, in
{ROUND}/w1/R80ScribeSources/sources-rows-r80.md, six registry rows in the exact 11-column schema
(no literal `|` inside a cell; `used-by` names the entry this round lands):
- S470 `src/render/Renderer.cpp` @ efb5099 — arrangement/attribution scope (tier A, kind code,
  anchor `applyExclusive :2529-2586`, `arrangeLayerArray :2587-2671`, `arrangeLayersForMonitor
  :2673-2700`; sha256 `9af8a74e…`, 143211 B). Note it duplicates S457's URL at a different scope.
- S471 `src/protocols/LayerShell.cpp` @ efb5099 — `set_exclusive_zone :100-102`,
  `set_exclusive_edge :156-168` (sha256 `ad9314da…`).
- S472 `tests/desktop/Reserved.cpp` @ efb5099 — the upstream unit test for `CReservedArea`
  (sha256 `37988cca…`).
- S473 the installed `omarchy-menu-keybindings` (own-work, tier A, scope the chord column):
  `dynamic_bindings`' twelve-mask render and `printf "%-35s → %s"`.
- S474 the installed `systemctl` man page, systemd 262 (docs, tier A, scope `is-active`'s exit
  contract): quote its `Returns an exit code 0 if at least one is active`.
- S475 a row that **supersedes S467** (`teaches` must open `supersedes S467 —`), narrowing the
  reason to "dead live URL, no revision pin, tier-B prose only" — the committed round-45 fetch
  states the stacking at `:183`.
For each row give: id, source, kind, tier, scope, anchor, teaches, status, opened (2026-11-04),
recheck, used-by. Also list, for each, the ≤25-word located quote that will go in the lesson's
Gate table, with its file and line from {ROUND}/fetch/.""",
    },
    {
        "name": "R80ScribeLesson",
        "role": "scribe",
        "prompt": """Draft the round lesson's `## Mistakes` section (prose only; the L1 lands it).

Read {LANE}/corpus/lessons/round-79.md and
{LANE}/corpus/lessons/round-79-verifier-spotcheck.md §6 (the five routed defects D1–D5). Draft
{ROUND}/w1/R80ScribeLesson/mistakes-r80.md with ONE row per mistake in the house table shape
(id | class | evidence pointer | captured-by | fix (shown able to fail)):
- M80-1 the r79 report's stale after-cell (44/44 at d6be05ef vs 50/50 at 999a4a3f) — class
  `reference-drift`.
- M80-2 the S467 rejection reason overstating ("syntax only") while the committed fetch states the
  stacking — class `attribution`.
- M80-3 LOG.md's "Seven mined" vs eight `## Mistakes` rows — class `number-drift`.
- M80-4 two fetch files named `S###` with no registry row — class `scope`, with the fix that new
  ids start at S470 (state why that is a fix and not a renumber).
- M80-5 the r79 partial seat (`R79ExecC1Tool` without a `.md`) — class `landing`, and what the r80
  wave does differently (every seat's findings.md + STATUS line).
Also add your own sweep for a sixth: run `grep -n 'TODO\\|FIXME\\|XXX'` over
{LANE}/tools/mado-barfoot.py and the two r80 counters and report the empty (or non-empty) result.
Each fix must name the command that would fail without it; if a fix cannot be shown able to fail,
say so and mark it as a criterion candidate instead.""",
    },
    {
        "name": "R80ReviewerC1",
        "role": "reviewer",
        "prompt": """Attack the C1 claim (adversarial; you are graded on what you falsify).

1. Re-derive independently, from {ROUND}/fetch/S470.bin and S472, the expectations of FIVE frozen
   cases of your choice, at least three of them new in r80. Show the arithmetic.
2. For each, decide: is the frozen `expect` supported by the source? If a case is wrong, say which
   field and why — the case set is frozen, so a wrong case is a claim defect, not a fixable nit.
3. Look specifically for a case whose expectation the sources do NOT decide: (a) `same-level-order`
   leans on rule `order()`; does the source really sort by order desc, and is the bar's order 0
   justified? (b) `ls-area-invalid` leans on `CReservedArea{parent, child}`'s early return: quote
   the guard and say whether an *empty* child really zeroes the whole reserve or only the delta.
   (c) `empty-box-skip`: quote the `continue` and say what happens to the zone.
4. Check the predicate's honesty: `base_correct=23/33` — could the held r79 model have reached 33
   with a different surface input? Is `killed=22` reached by single-anchor mutants only?
Write findings.md with a per-item verdict (SUPPORTED / UNSUPPORTED / UNDECIDED + evidence).""",
    },
    {
        "name": "R80ReviewerC2",
        "role": "reviewer",
        "prompt": """Attack the C2 claim (adversarial; you are graded on what you falsify).

1. Read the installed formatter {ROUND}/fetch/S473.txt in full. Enumerate every way it can produce a
   chord line and check the grammar the declaration states (1–4 distinct SUPER/SHIFT/CTRL/ALT,
   ` + `, one key; or a bare key) against each: `dynamic_bindings`' mask table (including mask 77 =
   SUPER SHIFT CTRL ALT), the `code:201` → `COPILOT KEY` rewrite, the mouse-button rewrites, the
   `switch:` keycode symbol path, and `static_bindings`' `SHIFT ALT,L,...` line.
2. Decide whether the grammar REJECTS any line the formatter can produce (a false negative that
   would break the row on a valid host), or ACCEPTS a form the formatter cannot produce (a false
   positive that hides a regression). Name each with the source line.
3. Do the same for the state row: read {ROUND}/fetch/S474.txt and say whether `active` ⇔ rc 0 is the
   complete contract, and whether any state word in the enum can come with rc 0 that the row would
   wrongly accept or reject. Check `systemctl --user is-active` on this host for two units and record
   the word+rc pairs.
4. Check the frozen case set's two new cases for a sample that cannot occur (e.g. a bare-key form
   with a `+`, a chord with 5 modifiers) and for a missing negative that the grammar would miss.
Write findings.md: per finding, the source line, the grammar clause, and the verdict.""",
    },
    {
        "name": "R80CriticClaims",
        "role": "critic",
        "prompt": """Falsify the two claims as DECLARED (not as implemented).

1. Read {ROUND}/claims-declaration-r80.md. For C1 and C2, restate the predicate, the kill rule and
   the do-nothing control, then test each:
   - Is the do-nothing control really the cheapest skip? The r79 tool cannot take `--surfaces`, so
     it scores 23/33 — but could a *one-line* edit of the r79 tool (ignoring `--surfaces`) reach a
     higher score? Try it on a COPY and report the score.
   - Is `carried=23/23` load-bearing or tautological? The counter asserts parsed equality of the
     prefix; what would break if the carried comparison were removed? Demonstrate.
   - For C2: the declared before-state is rc 2 (the tree is not the measured revision's bytes).
     Is that a verdict or a setup refusal? Say plainly which, and whether the claim's before→after
     is therefore measurable at all. Propose (do not implement) the cheapest honest fix if it is not.
2. Check the two claims for causal separability (C1 without C2, C2 without C1) and for a shared
   dependency that would make one fail with the other.
3. Check the axis naming (coverage / operability) against AXES.md: is C1 really coverage and C2
   really operability, or are they both instrument work?
Write findings.md with a verdict per question and, for every hole, the command that shows it.""",
    },
    {
        "name": "R80MutC1Counter",
        "role": "mutation-tester",
        "prompt": """Mutation-test the C1 counter's own checks (copies only; never edit the lane's counter).

For each check, copy quality/counters/c1-r80-multisurface.py into your directory, remove exactly one
check, and re-run it against the frozen controls (C1 command from the context, with your copy):
1. the carried-prefix assertion (`cases[:CARRIED] == carried`);
2. the exact `base_correct == 23` clause;
3. the `killed == 22` clause;
4. the `selftest_ok` clause;
5. the `attr_ns` comparison in `expected_ok`;
6. the `boxes` comparison;
7. the `ls` comparison;
8. the control-set sha print (does anything read it?).
For every check that still yields TARGET_MET when removed, say whether it is *unexercised* (no
frozen case separates it) or *absent* (no such check exists), and build one tamper probe that the
unmodified counter accepts or rejects — e.g. a carried case edited, a base pointed at the freeze, a
single `attr` cell changed in the control set. Report the exact probe and its result.
Write findings.md: table of check | mutant verdict | unexercised/absent | tamper probe.""",
    },
    {
        "name": "R80Sentinel",
        "role": "sentinel",
        "prompt": """Boundary and security review of the round's two instruments (read-only).

1. Read tools/mado-barfoot.py's read path (`read_bytes`, O_NOFOLLOW, MAX_BYTES), `parse_surfaces`
   (what it refuses, what it silently accepts), `apply_exclusive` (can a negative amount shrink the
   usable box the wrong way?) and the scratch handling in both counters (`--scratch-root` refusals,
   `tempfile.mkdtemp(dir=...)`, cleanup in `finally`).
2. Look for: a path traversal in `--surfaces` (none: it is a caller path, but check the *content*'s
   namespace is not used as a path), an unbounded loop or allocation from a hostile declaration
   (e.g. 1e6 surfaces, a huge `order`, `margins` of ±10^9), a way a case file could make the counter
   read outside the scratch root, and any place a counter writes under `/tmp` regardless of
   `TMPDIR`/`--scratch-root` (QUALITY/§7 rule).
3. Check the C2 counter's `run()` environment: which variables it passes (PATH, LC_ALL, LANG,
   PYTHONDONTWRITEBYTECODE, TMPDIR), and whether a case's argv could reach a write verb (all 24
   commands are read verbs or the lane's own read-only join — verify by reading the control set).
4. Verify no credential material, session token, cookie or `op://` reference appears in the round's
   new files: `grep -rn 'op://' {ROUND}/ tools/mado-barfoot.py quality/counters/c1-r80-multisurface.py
   quality/counters/c2-r80-runbook.py` and report the (expected empty) result.
Write findings.md with severity per finding and the exact line numbers.""",
    },
    {
        "name": "R80ConnSiblings",
        "role": "connector",
        "prompt": """Sibling-overlap scan (read-only; report, never absorb).

1. Search the other lanes' corpora for the ground this round claims: layer-surface composition,
   per-surface reserved attribution, `applyExclusive`, `arrangeLayersForMonitor`, `CReservedArea`
   (`grep -rl` over /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge* for those terms), and
   for the C2 ground (`omarchy-menu-keybindings`, `is-active` runbook rows).
2. For each hit, say whether the sibling CLAIMS the same ground (contested), merely cites it, or
   owns an adjacent surface that mado should not touch. Quote the path and line.
3. Check whether any sibling lane's tools already model layer surfaces (a tool name like `*layers*`,
   `*barfoot*`, `*reserve*` in siblings' tools/) — a sibling instrument that already does this is a
   provenance question the L1 must answer in the report.
4. Also check the fleet's `merge/mado/` package under /home/vgpnk/Projects/shokuknow for a staged
   entry touching this ground (read-only; run no campaign tool there).
Write findings.md: table of sibling | path:line | contested? | what mado should say in the report.""",
    },
]


def main(out):
    context = CONTEXT.replace("{ROUND}", ROUND).replace("{LANE}", LANE) \
                     .replace("{FREEZE}", FREEZE).replace("{BASE}", BASE) \
                     .replace("{SCRATCH}", SCRATCH)
    items = []
    for item in ITEMS:
        prompt = item["prompt"].replace("{ROUND}", ROUND).replace("{LANE}", LANE) \
                               .replace("{FREEZE}", FREEZE).replace("{BASE}", BASE) \
                               .replace("{SCRATCH}", SCRATCH)
        items.append({"name": item["name"], "role": item["role"], "prompt": prompt})
    spec = {
        "wave": "w1",
        "reportDir": ".ufo/waves/round-80/w1",
        "context": context,
        "items": items,
    }
    with open(out, "w") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    roles = {}
    for item in items:
        roles[item["role"]] = roles.get(item["role"], 0) + 1
    print("items=%d roles=%s" % (len(items), roles))


if __name__ == "__main__":
    main(os.path.join(ROUND, "w1-spec.json"))
