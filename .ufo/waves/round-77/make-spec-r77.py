#!/usr/bin/env python3
"""Build the round-77 w1 wave spec (12 seats, one v1 wave)."""

import json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROUND = LANE + "/.ufo/waves/round-77"
SCRATCH = "/fast/scratch/hyaku/mado-r77"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + f"""
Round mado 77, ONE v1 wave (12 seats). Claims (frozen): C1 coverage — the bar-footprint chain
(declared waybar config -> live layer box -> monitor `reserved` band) becomes a measured join:
15 frozen cases 15/15, five named mutations killed 5/5, live-echo control 8/15; C2 operability —
the SKILL.md read-only probe table executes end-to-end: 12 cases, 12 executed, 12 matched.
The declaration is {ROUND}/claims-declaration-r77.md; read it first.

Frozen instruments and controls (never rewritten by a seat):
- {LANE}/tools/mado-barfoot.py (sha256 409e78a4…, blob 41f3341f…)
- {LANE}/quality/counters/c1-r77-barfoot.py (sha256 56620959…, blob ae5d27e7…)
- {LANE}/quality/counters/c2-r77-runbook.py (sha256 056a9152…, blob 57383fc7…)
- {ROUND}/controls/c1-cases-r77.json (sha256 7d6e2b1a…, 15 cases)
- {ROUND}/controls/c2-runbook-cases-r77.json (sha256 597b2302…, 12 cases)
- Freeze revisions: e4717a1c (instruments+declaration), a83e9bee (C1 counter absolute-repo fix),
  94b5afb1 (pre-wave receipts). Base: aeeef067bd63672dfc681d6dacc3797f53ffd1f9.
- Pre-wave receipts: {ROUND}/receipts/control-baseline-r77.txt (C1 base 8/15; C2 executed=0) and
  {ROUND}/receipts/pre-wave-evidence-r77.txt (live run, gate 460/460, census).
- Pinned source trees (read-only): {SCRATCH}/l1-src/Hyprland (v0.56.2 @ efb5099) and
  {SCRATCH}/l1-src/Waybar (tag 0.15.0). Host config is read-only: ~/.config/waybar/config.jsonc,
  ~/.config/hypr/**.

Hard bounds, every seat:
- Your write directory is {ROUND}/w1/<your name>/ plus the one scoped findings file the validator
  trailered for you ({ROUND}/w1/<your name>.md). Never edit a committed lane file (tools,
  quality, corpus, SKILL.md, SCORECARD.md, LOG.md, README, SOURCES.md, PROVINCE.md, the declaration,
  the control sets); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash/jj mutation); read-only
  git (`show`, `ls-tree`, `rev-parse`, `status`, `log`, `cat-file`) is fine. Never write the fleet
  repo, a sibling lane, ~/.config, .ufo/state/, .ufo/watchdog.log, .scratch/, scripts/, templates/
  or MANIFEST.json. Any fixture git repo lives under your scratch: `D=$(mktemp -d <scratch>/gitXXXX)`;
  `git -C "$D" init -q`; prove `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first
  commit; never use a throwaway identity anywhere else.
- Host posture: READ-ONLY probes only. Allowed: `hyprctl version|configerrors|monitors|workspaces|
  activeworkspace|getoption|binds|layers|clients|animations|workspacerules|devices|instances|
  systeminfo|submap|locked`, `pgrep`, `makoctl mode`, `systemctl --user is-active`, `busctl --user
  status|get-property`, `omarchy theme current|version|commands --json`, file reads. FORBIDDEN:
  any hyprctl write verb (`keyword`, `dispatch`, `reload`, `setprop`, `output …`, `plugin …`),
  any write under ~/.config or the repo, any socket connection, screenshots, package transactions,
  service restarts, compositor state changes. Never print an instance signature, window title or
  other session material.
- Scratch: {SCRATCH}/<your name>/ (create it; pass it explicitly; never use /tmp; copy any receipt
  you cite into your own dir, then delete the scratch dir before you finish).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps this
  task, first reading /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate) and
  recording tool/version/channel/reason in your report. ALL pacman transactions are PAUSED
  host-wide this run: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or report that
  you needed one; never `pacman -Sy/-S/-Syu/-U/-R`, never restart a host service.
- Never message `agent://all`; reply only to your L1 (`MadoR77`) or nothing.
- Every `Report:` trailer path the validator renders is relative to {LANE} — write it at
  {LANE}/<that path>. End your final output with one line `Report: <repo-relative path>` naming
  the file you actually wrote, then a 3-line summary.
"""


def prompt(name, role, body):
    return GODSPEED + f"""Your name: {name} ({role}). Your only write directory:
{ROUND}/w1/{name}/. Scratch: {SCRATCH}/{name}/.

{body}

End your final output with the validator's `Report:` trailer line, naming the file you actually
wrote; write that file under {LANE}/<that path> (the trailered path is
.ufo/waves/round-77/w1/{name}.md). Keep working notes in your own dir. Then a 3-line summary.
Never commit; the L1 integrates and commits every production byte.
"""


def item(name, role, body):
    return {"name": name, "role": role, "prompt": prompt(name, role, body)}


ITEMS = [
    item("R77ExecTool", "executor", """
Attack the join model in tools/mado-barfoot.py (read at a83e9bee; sha256 409e78a4…).

1. Read the pinned sources and name, with file:line anchors, the rule each modelled branch
   implements: Hyprland src/render/Renderer.cpp arrangeLayerArray + arrangeLayersForMonitor,
   src/debug/HyprCtl.cpp layersRequest + the monitors `reserved` print, src/desktop/reserved/
   ReservedArea.cpp; Waybar src/bar.cpp margins/anchors/setMode and the installed waybar(5)
   `position`/`layer`/`height`/`width`/`margin`/`exclusive`.
2. Write `rule-table.md`: modelled rule | source anchor | tool code anchor | agree/disagree |
   the sentence the tool relies on (<=25 words).
3. Run `python3 -I tools/mado-barfoot.py --selftest` and the C1 counter at a83e9bee; save both
   outputs and the per-case verdicts.
4. If a branch is behaviourally wrong, write `candidate.patch` (minimal unified diff against the
   committed tool) plus `gap.md`: a config/layers/monitors triple the frozen set does not cover
   where today's tool is wrong and the patched tool is right. Do not edit the committed tool.
"""),
    item("R77ExecCases", "executor", """
Extend the model adversarially with cases outside the frozen 15.

Write six candidate case triples under your dir (`cases/<name>/{config.json,layers.json,
monitors.json}`) covering: a bottom bar with margin-bottom; a `name`-renamed bar beside a
second `waybar` namespace; a JSONC config with `//` inside a string value; a top bar with
`height: 0` (the auto branch); an overlay-layer bar (`"layer": "overlay"`); a snapshot where
another exclusive consumer adds to the reserved band. For each case write the verdict you derive
*from the sources first* (table in `derivations.md`, with the rule and source line), then run
the committed tool on it and mark agree/disagree. A disagreement is either a model gap (name
the missing rule) or a tool bug (name the line). Never modify the frozen case set.
"""),
    item("R77ExecLive", "executor", """
Independent live execution of both claims' host side.

1. Capture at t0 and t1 (>=60 s apart) `hyprctl layers -j`, `hyprctl monitors -j`,
   `hyprctl clients -j`, `hyprctl workspaces -j` into your dir; sha256 each file and keep both
   pairs. Run the committed tool on both captures with ~/.config/waybar/config.jsonc; the joined
   `MADO_BARFOOT_*` lines must be identical across t0/t1 (the layer/geometry fields); name any
   census field that moved (clients/workspaces may churn) and keep it out of the verdict claim.
2. Run the twelve frozen C2 probe commands yourself (read the control JSON) and record exact
   stdout, stderr and rc per probe in `probe-run.txt`; state match/mismatch against the frozen
   expectations and whether any expectation is too weak to catch a wrong state.
3. Save `live-pair.txt` with the two tool runs side by side and the sha256s.
"""),
    item("R77ExecRepairs", "executor", """
Build the carried-defect repair pack (round-76 spot-check D1–D8) in your dir as append-only text
the L1 can land, plus the one executable check the round needs.

- D1: `correction-d1.md` — a `## Correction (round 77)` block for
  corpus/knowledge/outcome-field-r76.md and interprocedural-del-r76.md naming the missing
  `source:`/`verified-at:`/`recheck:` fields and the cited rows (S450/S455; S453/S454/S455/S456).
- D2: `correction-d2.md` — SCORECARD.md:4339's stale C2 revision (5dade9b3 -> 3588a527) with
  `git log -1 --format=%H -- quality/counters/c2-r76-shapes.py` as the re-derivation.
- D3: `correction-d3.md` — errata for claims-declaration-r76.md:26 and the exact docstring lines
  in quality/counters/c1-r76-outcome-field.py; run the counter before/after a text-only edit on
  your own copy and show the counts identical (`parity.txt`).
- D4: the correct mistake count derived from corpus/lessons/round-76.md rows, with the command.
- D7/D8: `correction-d7-d8.md` — the r76 report pointer arithmetic and declaration pointer, each
  with its `git diff-tree`/path command.
- Executable check: `check-cited-revisions-probe.py` (or .sh) that flags a SCORECARD row whose
  "measured at <hash>" is not the file's last-change commit. Run it red on the r76:4339 text and
  green on the corrected text; save `red.txt` and `green.txt`.
"""),
    item("R77ScribeEntryC1", "scribe", """
Draft the C1 knowledge entry `corpus/knowledge/bar-footprint-r77.md` in your dir.

Open with the provenance trio (`source:` S457–S462, `verified-at: 2026-11-04`, `recheck:` with
the trigger), then: ground statement; the chain (waybar declaration -> Hyprland
arrangeLayerArray anchors/margins/exclusive -> live layer box -> monitor `reserved` band ->
usable area) with one row per link tagged OBS/INF/UNK and citing its source row id + file:line;
the host join measured today (DP-1 3440x1440@99.997, waybar level 2, box 0,0,3440,26, reserved
[0,26,0,0], bar height 26, no margins) with receipts; the tool contract (inputs, exit map,
model limits incl. NOT_MODELLED margins, output exclusion, auto branches); and a Sources section.
No number without a pointer; no sentence the sources do not license.
"""),
    item("R77ScribeSources", "scribe", """
Curate the sources and the lesson in draft form.

1. Fetch each candidate source and save it byte-identically with sha256 under `fetch/`:
   S457 Hyprland efb5099 src/render/Renderer.cpp; S458 src/debug/HyprCtl.cpp; S459
   src/desktop/reserved/ReservedArea.cpp (+ .hpp); S460 protocols/wlr-layer-shell-unstable-v1.xml;
   S461 the installed waybar(5) man page; S462 Waybar 0.15.0 src/bar.cpp; S463 candidate reject
   (the wayland.app wlr-layer-shell page). Record `<anchor> | <=25-word located quote | access`.
2. Draft `sources-rows.md`: the 11-column rows (S457…S463) with status mined/rejected, used-by the
   round-77 entry, recheck cadence, and the census command + expected W04 notes.
3. Draft `index-row.md` for corpus/README.md and `lesson-round-77.md` with `## Gate` (>=1 admit,
   >=1 reject, URL/date/quote per row) and `## Mistakes` (mine at least two: one from the r76
   D-series, one from this round; class, evidence pointer, captured-by, a fix shown able to fail).
4. Draft `log-and-scorecard.md`: the LOG entry, the SCORECARD round-77 block (two claims, the axes,
   the before/after, the capability rows) — numbers only where measured.
"""),
    item("R77ScoutSources", "scout", """
Per-surface source reconnaissance (read-only).

In the pinned trees, locate and quote (<=25 words, file:line) the sentences that license each
modelled rule: the four level slots of `m_layerSurfaceLayers` and the JSON level index; the
anchor/margin/desired-size branches in arrangeLayerArray; applyExclusive's singular/triplet edge
test and `exclusive + margin`; arrangeLayersForMonitor's reset/addType reserved composition;
the `layers` reply fields and the monitors `reserved` order; waybar's margin precedence
(per-side, CSS string, integer), `set_size_request`, `setPosition` anchors, `setMode`'s
auto-exclusive-zone vs zone-0. Also check whether a `name` in the waybar config changes the
namespace, and whether `layer: bottom` with `exclusive: true` still reserves.

Report `claim | file:line | quote | licenses | does not license`; flag any tool rule with no
source anchor and any source sentence the tool contradicts. Write `report.md` only.
"""),
    item("R77ConnSiblings", "connector", """
Cross-lane and cross-round pattern scan (read-only).

1. Search sibling repos under /home/vgpnk/Projects/shokunin/*-shokunin for the layer plane /
   bar footprint / runbook-execution ground: `hyprctl layers`, `reserved`, `bar footprint`,
   `probe table`, `runbook`. Does any lane already own or claim the surface? Report paths+lines.
2. Count the recurrence of the routed "stale revision citation" class across the lane's last ten
   lessons and state whether this round's fix (an executable check) is the first that can fail on
   the defect; cite the lesson lines.
3. Read mado-shokunin/considerthese/2026-10-28.md proposal 4 (live-tool table). Is it still
   unimplemented, and does the round's new pair of live instruments change the answer? State
   whether absorbing it is justified now, with the lane's rules.
Write `report.md` with a table; no edits.
"""),
    item("R77RevClaims", "reviewer", """
Attack the two frozen claims from committed bytes (do not trust the receipts).

1. Re-derive C1: run the counter at a83e9bee exactly as the declaration says; confirm the
   printed contract line equals the declaration sentence word for word; confirm the base line and
   that 8/15 < 15; open the 15-case JSON and check each expected tuple is the tuple the counter
   compares (box/reserved/verdict/rc); check the 5 mutant anchors are semantic rules, not comments.
2. Re-derive C2: run the counter; confirm 12 executed/12 matched/12 anchors, that each
   skill_anchor occurs in the committed SKILL.md at the measured rev, and that the expectations
   are not trivially true (name any expectation a wrong state could still pass).
3. Check the live evidence pointers (`fetch/live-*.json` sha256, `receipts/pre-wave-evidence-r77.txt`)
   and that no cited number is unlabelled (QUALITY 131).
Report `claim | predicate | re-derived | agree/disagree | defect class`; do not repair.
"""),
    item("R77Critic", "critic", """
Falsify the round design, not the wording.

(a) Is C1 a coverage move (new surface) or a re-score of a surface the lane already holds? Name
the command that would show the surface unmoved. (b) Is the live-echo control the cheapest rule
that skips the claimed work? Try one cheaper (e.g. read the live box and echo the reserved band
unconditionally) and score it; if it meets 15/15 the target is wrong. (c) Does C2's
executed/matched split separate a checklist that runs from one that is only read? Attack it with
a probe that is "matched" by mention. (d) Are C1 and C2 causally separable (each verifiable
without the other)? (e) Does either claim harm coverage/operability/freshness/calibration/
adjacency? (f) Any universal clause, unfalsifiable target, or after-state depending on
uncommitted bytes? Write `report.md` with verdicts and commands, not opinions.
"""),
    item("R77Mutant", "mutation-tester", """
Independent mutation testing of the join and the expectations.

1. Write >=8 new mutants of tools/mado-barfoot.py outside the five frozen ones (bottom/left/right
   extents; output exclusion; namespace default; height/width swap on vertical bars; reserved
   index order; per-side margin precedence; zero-size branch). Run each against the 15 frozen
   cases from your own copies; report killed/survived and the case that kills it.
2. For each survivor: real model gap (name the discriminating case) or equivalent mutant (prove
   it produces identical published fields on every frozen case).
3. Attack C2's twelve expectations: which would still pass if the underlying state were wrong
   (too weak)? What stronger read-only expectation is available? Report
   `mutant | killed/survived | case | class` and `probe | weakness | stronger expectation`.
"""),
    item("R77RevBytes", "revenger", """
Byte-fidelity audit (read-only).

1. Re-fetch each cited source (Hyprland efb5099 Renderer.cpp, HyprCtl.cpp, ReservedArea.*; the
   wlr-layer-shell XML; the waybar(5) page; Waybar 0.15.0 bar.cpp) and byte-compare sha256
   against the fetch receipts the scribes draft (or your own refetch); report any drift.
2. Verify the live captures' sha256 and that the tool's live output in
   receipts/pre-wave-evidence-r77.txt is re-derivable from those bytes.
3. Verify every quoted sentence in the drafted entry/SOURCES rows occurs verbatim (<=25 words) at
   the named anchor; verify the tool docstring's claims (`reserved` order, exit map, 1 MiB cap,
   the auto-exclusive-zone limit) against the code and sources.
Report any fabricated, shifted, overlong or stale byte; do not edit.
"""),
]


def main():
    spec = {
        "wave": "w1",
        "reportDir": ".ufo/waves/round-77/w1",
        "context": CONTEXT,
        "items": ITEMS,
    }
    with open(ROUND + "/w1-spec.json", "w") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    print("wrote %d items to %s/w1-spec.json" % (len(ITEMS), ROUND))


if __name__ == "__main__":
    main()
