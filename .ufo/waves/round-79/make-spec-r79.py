#!/usr/bin/env python3
"""Build the round-79 w1 wave spec (14 seats, one v1 wave, band 8-16)."""

import json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROUND = LANE + "/.ufo/waves/round-79"
SCRATCH = "/fast/scratch/hyaku/mado-r79"
FREEZE = "5eb8f20fe291603c74973fa94cc55723ac8089a4"
BASE = "e4b153dfa4a67ca56f7ec65cb6639082451626a7"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + f"""
Round mado 79, ONE v1 wave (14 seats). Claims (frozen; declaration {ROUND}/claims-declaration-r79.md):
C1 coverage — the static `monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT` reserve composes
with the bar's own band: 23 frozen cases 23/23, twelve named mutations killed 12/12, held round-78
tool `base_correct=18/23`, the eighteen round-78 cases carried byte-identically; C2 operability —
the runbook executes per-row bindings: 22 cases, 22 rows / 22 distinct anchors, four documented
model refusals plus the keybindings shape row, `control_new=0/5`, nine matcher mutants killed.
Read the declaration first; it is the frozen contract. The freeze is `{FREEZE}`; the base
revision is `{BASE}`.

Frozen instruments and controls (never rewritten by a seat; every measurement is pinned here):
- {LANE}/tools/mado-barfoot.py (r79-v1, sha256 c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de)
- {LANE}/quality/counters/c1-r79-reserve.py, {LANE}/quality/counters/c2-r79-runbook.py
- {ROUND}/controls/c1-cases-r79.json (23 cases, sha256 5f7ebb3c…), c2-runbook-cases-r79.json (22 cases)
- {ROUND}/fixtures/refuse-{{mode,scale,layer-background,output-space}}/ (committed refusal fixtures)
- Measurement receipts: {ROUND}/receipts/measurement-c{{1,2}}-r79.txt (both TARGET_MET at {FREEZE});
  before-state receipts: control-c1-r79-at-base.txt (correct=18/23, killed=4), `control-c2-heled-instrument-at-base.txt`
  (rc 2), control-c2-r79-at-base.txt (rc 2).
- Pinned source bytes (read-only): {ROUND}/fetch/ (S457-S466, sha256-r79.txt). Host config is
  read-only: ~/.config/hypr/**, ~/.config/waybar/**.

Hard bounds, every seat:
- Your write directory is {ROUND}/w1/<your name>/ plus the one scoped findings file the validator
  trailered for you ({ROUND}/w1/<your name>.md). Never edit a committed lane file (tools, quality,
  corpus, SKILL.md, SCORECARD.md, LOG.md, README, SOURCES.md, PROVINCE.md, the declaration, the
  control sets, the fixtures); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash/jj mutation); read-only
  git (`show`, `ls-tree`, `rev-parse`, `status`, `log`, `cat-file`) is fine. Never write the fleet
  repo, a sibling lane, ~/.config, .ufo/state/, .ufo/watchdog.log, .scratch/, scripts/, templates/
  or MANIFEST.json. Any fixture git repo lives under your scratch and every git call names `-C` it.
- Host posture: READ-ONLY probes only. Allowed: `hyprctl version|configerrors|monitors|workspaces|
  activeworkspace|getoption|binds|layers|clients|animations|workspacerules|devices|instances|
  systeminfo|submap|locked`, `pgrep`, `makoctl mode`, `systemctl --user is-active`, `busctl --user
  status|get-property`, `omarchy theme current|version|commands --json|menu keybindings --print`,
  file reads. FORBIDDEN: any hyprctl write verb (`keyword`, `dispatch`, `reload`, `setprop`,
  `output …`, `plugin …`), any write under ~/.config or the repo, any socket connection,
  screenshots, package transactions, service restarts, compositor state changes. Never print an
  instance signature, window title or other session material.
- Scratch: {SCRATCH}/<your name>/ (create it, pass it explicitly, never use /tmp; copy any receipt
  you cite into your own dir, then delete the scratch dir before you finish).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps this
  task, first reading /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate) and
  recording tool/version/channel/reason in your report. ALL pacman transactions are PAUSED
  host-wide this run: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or report that
  you needed one; never `pacman -Sy/-S/-Syu/-U/-R`, never restart a host service.
- Never message `agent://all`; reply only to your L1 (`MadoR79`) or nothing.
- Every `Report:` trailer path the validator renders is relative to {LANE} — write it at
  {LANE}/<that path>. End your final output with one line `Report: <repo-relative path>` naming
  the file you actually wrote, then a 3-line summary.
"""


def prompt(name, role, body):
    return GODSPEED + f"""Your name: {name} ({role}). Your only write directory:
{ROUND}/w1/{name}/. Scratch: {SCRATCH}/{name}/.

{body}

Report to {ROUND}/w1/{name}.md (also copy it into your write directory). Findings are data:
name the command, the observed output and the file:line. Do not edit the repo, do not commit,
do not run a mutating git/jj command. End with `Report: .ufo/waves/round-79/w1/{name}.md`.
"""


def item(name, role, body):
    return {"name": name, "role": role, "prompt": prompt(name, role, body)}


ITEMS = [
    item("R79ScoutModel", "scout", f"""
Source reconnaissance for the C1 static-reserve composition (read-only).

1. Open the pinned bytes in {{ROUND}}/fetch/ and locate exact lines: Hyprland `src/output/Monitor.cpp`
   `applyMonitorRuleSoft` (setStatic) and `logicalBoxMinusReserved`; `src/desktop/reserved/ReservedArea.cpp`
   `calculate`, `setStatic`, `apply`; `src/render/Renderer.cpp` `arrangeLayersForMonitor`
   (`ORIGINAL_USABLE_AREA`, `addType`) and `arrangeLayerArray`; `src/debug/HyprCtl.cpp` monitors
   `reserved` print; `src/config/legacy/ConfigManager.cpp` `handleMonitor` `addreserved` argument
   mapping and the same-selector rule replacement.
2. Build an anchor table: operation -> exact line -> what it proves about `expected = static + bar`.
   Specifically decide: does the dynamic (layer) contribution sum with the static one or replace it?
   Is the layer box arranged inside the static-reduced usable box? What happens when the static
   reserve leaves no usable box?
3. Attack the tool's model: find any reachable declaration where the recorded composition is wrong
   (a bottom bar with a static bottom reserve, a left bar with a static left reserve, a margined
   bottom bar, `transform`/`disable` interactions, a positional rule after `addreserved`).
4. Name what the model cannot cover and why (a second layer-surface consumer, scaled outputs,
   `desc:` selectors, sourced config files).
"""),
    item("R79ScoutHost", "scout", f"""
Read-only host reconnaissance for both claims.

1. Capture (read-only) the current `hyprctl layers -j` and `hyprctl monitors -j` into your dir
   (reduce the monitors reply to name, size, reserved, scale, transform — never print the
   description/serial). Check `~/.config/hypr/**` for any `addreserved` or `source =` line that the
   C1 join would meet, and run `python3 -I tools/mado-barfoot.py --config ~/.config/waybar/config.jsonc
   --layers <cap> --monitors <cap> --rules ~/.config/hypr/monitors.conf` (read-only) — report the
   exact stdout and exit code.
2. Run every one of the 22 runbook row commands from SKILL.md's new section yourself, in the lane
   root, and record `case | rc | first 80 chars`. Flag any row that needs a shell feature the
   table's command does not show, any row slower than 5 s, and any row whose current output is
   volatile within a minute (run it twice).
3. Report which rows would break on a plausible host change (another workspace, a waybar restart, a
   theme switch, a bind edit) and whether the declared shape would still pass.
"""),
    item("R79ConnSiblings", "connector", """
Sibling-overlap and cross-claim scan (read-only).

1. Scan sibling repos under /home/vgpnk/Projects/shokunin/*-shokunin for any claim on the static
   reserved area, `monitor = … addreserved`, the `reserved` band, the monitor rule parser, or an
   executable runbook of `hyprctl`/`omarchy` read rows. Report hits with file:line and the province
   they name; no overlap is a finding too.
2. Scan this lane's record for the defect classes these claims touch: a cited revision described as
   an instrument's last change (routed r78 D2), a registry row describing superseded tool behaviour,
   a ledger row whose description no longer matches the instrument, and an index/frontier count that
   disagrees with the lesson (routed r78 D3). Give each file:line and a red/green-able command.
3. Prove the provenance chain resolves: declaration -> counter -> control set -> fixture -> receipt,
   for both claims, at the freeze `5eb8f20f`. Name any link that does not resolve.
"""),
    item("R79ExecC1Cases", "executor", """
Independent re-derivation of the five new C1 expectations (compute first, run second).

1. From the source rules alone (do not read the tool first), derive for each of the five new cases
   in controls/c1-cases-r79.json: the usable box, the declared box, the expected band, the reserved
   verdict and exit code. Write your derivation down, then run the tool and compare.
2. Build five MORE adversarial fixtures of your own (bottom bar + static bottom; left bar + static
   left; margined bottom bar + static top; static reserve exactly equal to the bar band; static
   reserve larger than the monitor) and state what the correct answer is from the sources, then
   report the tool's answer.
3. Report a table `case | re-derived | tool | agree?` and every divergence with its fixture inline.
"""),
    item("R79ExecC1Tool", "executor", """
Fuzz and boundary-test the `--rules` reader and the composition (write code and run it).

1. Copy tools/mado-barfoot.py at 5eb8f20f into your dir. Probe: a rules file with comments,
   whitespace variants, `monitor=x,addreserved,1,2,3,4` (no spaces), a huge field, a negative field,
   six fields, five fields, an unknown positional key, `disable`, `transform`, a positional rule
   after `addreserved` and before it, two selectors, `$VAR`, `##`, a `source =` line, a non-UTF-8
   byte, a directory, a FIFO, a 2 MiB file.
2. For each: the expected exit class from the docstring vs observed; report divergences with the
   fixture inline and the command line. Fix nothing in the lane; propose the minimal repair.
3. Check box arithmetic for each of the four positions with a static reserve on each axis, including
   a centred explicit width inside a static-reduced usable box.
"""),
    item("R79ExecC2Cases", "executor", """
Independent re-derivation of the five new C2 cases and their mutant separation.

1. Run the four refusal fixtures yourself and confirm each is a `stage=model` exit-3 refusal with a
   distinct reason; confirm that no fixture is a setup error dressed as a model refusal.
2. For the keybindings row: count the arrow lines, check the regex against every line, and test the
   declared churn and negative samples against the rule independently of the counter.
3. Build the separation table for the four new mutants (refusal-stage-blind, refusal-rc-blind,
   lines-any-line, lines-min-lines-dropped): which case/sample kills each, and whether any sample is
   load-bearing for more than one mutant. Report an unkillable mutant or an unseparated sample.
"""),
    item("R79ExecC2Runbook", "executor", """
Execute the runbook from its documentation alone (no counter).

1. Extract the 22 command cells from SKILL.md's `### Executable runbook rows (round 79)` section
   with your own parser (handle `\\|`), run each verbatim from the lane root, and compare with the
   counter's receipt lines case by case.
2. Check the binding direction: for every row, does exactly one case claim it, and does every case's
   `skill_anchor` equal its row's unescaped command cell? Report any prefix/equality ambiguity
   (e.g. `hyprctl layers -j` vs a longer cell that starts with it).
3. Verify the tree binding: change nothing, but prove the counter would refuse a working tree whose
   SKILL.md or tool bytes differ from the measured rev (use a scratch copy, never the lane).
"""),
    item("R79ScribeEntry", "scribe", """
Draft the C1 knowledge entry `corpus/knowledge/bar-footprint-reserve-r79.md` (prose only).

1. Read corpus/knowledge/bar-footprint-margins-r78.md for shape and voice, the frozen declaration,
   the case set, the receipts and fetch/sha256-r79.txt. Draft a 60-110 line entry with the
   provenance trio (`source:`, `verified-at:`, `recheck:`), the composition rule with file:line
   anchors (S465/S466 and the mined S457/S458/S459), a decision table from reachable declaration to
   expected band (including static reserve on each axis, `exclusive: false`, and the refusal
   classes), the worked five-case set, and a limits section.
2. Every number carries its command or its case name; every source claim names its S-id and line;
   no measured value is invented — use only the receipts named in the declaration.
3. Include `## What is not claimed` (a second layer-surface consumer, scaled outputs, `desc:`
   selectors, sourced config files).
"""),
    item("R79ScribeSources", "scribe", """
Draft the round's frontier bookkeeping (prose only).

1. Draft the two new SOURCES rows S465 (`src/output/Monitor.cpp`) and S466
   (`src/desktop/reserved/ReservedArea.cpp`) in the registry's 11-column shape, each with an
   access date 2026-11-04, the sha256 from {ROUND}/fetch/sha256-r79.txt, a located <=25-word quote,
   tier, scope, teaches, status `mined`, recheck `on-release`, and `used-by` naming the new entry.
2. Draft the in-place registry changes as old -> new pairs: `used-by` for S457/S458/S459/S461 (and
   S303 if its anchor covers the `addreserved` argument mapping) adding
   `corpus/knowledge/bar-footprint-reserve-r79.md`; list them in a table.
3. Run the census commands from CORPUS.md (rows, malformed rows, tier/status histogram, duplicate
   ids) at the freeze and paste the outputs with exit codes; state which command line the L1 must
   paste into the report.
"""),
    item("R79RevC1", "reviewer", """
Adversarial review of C1 (re-derive; do not trust the receipt).

1. Re-extract tools/mado-barfoot.py at 5eb8f20f and verify sha256 c9aa1391…; re-run
   `python3 -I quality/counters/c1-r79-reserve.py --repo {LANE} --rev 5eb8f20f --base-rev
   e4b153df… --controls … --carried … --scratch-root <your scratch>` from a clean scratch and
   compare every count with the committed receipt.
2. Attack the counter: can it report TARGET_MET with a wrong tool (mutate the counter's checks in a
   scratch copy)? Are the twelve mutation anchors real mutations of the named rule? Does the
   carried-prefix assertion compare the right objects? Is `base_correct == 18` a real control, or
   could another do-nothing rule reach 23?
3. Attack the claim itself: is `coverage` the right axis? Does the composition really need the
   `--rules` input, or could the tool have derived it from the two captures? Is any case expectation
   derived from the tool rather than from the sources?
"""),
    item("R79RevC2", "reviewer", """
Adversarial review of C2 (re-derive; do not trust the receipt).

1. Re-run the C2 counting command at 5eb8f20f from a clean scratch and compare every count with the
   committed receipt. Check `shapes=17/17` against an independent enumeration of shape kinds.
2. Attack the binding grammar: can one row satisfy two anchors (prefix/equality), can a deleted row
   survive through another row, does the escaped-pipe splitter lose a backslash? Attack the refusal
   matcher (message-only refusal, stage spoofing, rc spoofing) and the tree binding (a stale working
   tree, a fixture edited in place).
3. Attack the claim's axis and size: is "operability" fair when four of the cases execute the lane's
   own tool rather than a probe row? Is the held control meaningful at `control_new=0/5`?
"""),
    item("R79CritClaims", "critic", """
Falsify the two frozen claims (adversarial, reasons required).

1. For C1: construct the cheapest route to `correct=23, killed=12, base=18` that does NOT implement
   the claimed composition (e.g. a special-case lookup table in the tool, a branch on the fixture
   name, a hard-coded expected band for the five new cases). Would the counter catch it? If not, the
   target is under-specified — say so with the route.
2. For C2: can a rule that only special-cases the five new cases reach 22/22 without executing
   anything? Is `control_new=0/5` tautological in a way that makes the control worthless? Name what
   a stronger control would be.
3. Judge the claim sizing (fleet §9): is each after-state one concrete value a closure can re-derive
   with one command over committed bytes? Is any universal clause used without an enumeration? Is
   either claim actually the same axis twice? Report a verdict per claim with reasons.
"""),
    item("R79MutC1", "mutation-tester", """
Mutation-test the C1 counter, not the tool (write code and run it).

1. Copy quality/counters/c1-r79-reserve.py and apply single-anchor mutations to the COUNTER: drop
   the carried-prefix check; accept `base_correct != 18`; treat an absent anchor as killed; drop the
   refusal stage pin; compare only `verdict` (ignore band/expected); accept a red tool selftest.
2. For each counter mutant, re-run it against the freeze and state whether it still prints
   `verdict=TARGET_MET` (a counter survivor) — those are the counter's own holes. Report a table
   `counter-mutant | still TARGET_MET? | the case that would have caught it`.
3. Check the twelve tool mutants' separation: for each, the case that kills it and whether that case
   is the sole separator. Name any mutant killed only by a refusal or by an unrelated field.
"""),
    item("R79Sentinel", "sentinel", """
Security and boundary review of the round's artifacts.

1. Read `--rules` handling in tools/mado-barfoot.py at 5eb8f20f: path refusals (symlink, FIFO,
   device, directory, >1 MiB), UTF-8 handling, and whether any content is echoed. Then read the two
   counters for scratch discipline (no `/tmp` default, removal on exit, refusal of `/` and symlinked
   scratch), child environment (no inherited secrets), and any place a child's stdout is echoed raw.
2. Audit the new artifacts for session material or secret shapes: SKILL.md rows, the case sets, the
   four fixture dirs, the fetch receipts, the declaration. Name any window title, instance
   signature, pid, token or host path that should not be committed.
3. Check the runbook rows' write scope: every command is a read verb or the lane's read-only join;
   no row writes host state. Report a row that could be made to write (quoting, redirection,
   `omarchy` subcommand) and whether the table's text invites it.
"""),
]

SPEC = {
    "wave": "w1",
    "reportDir": ".ufo/waves/round-79/w1",
    "context": CONTEXT,
    "items": ITEMS,
}


def main():
    path = ROUND + "/w1-spec.json"
    with open(path, "w") as fh:
        json.dump(SPEC, fh, indent=1)
        fh.write("\n")
    roles = {}
    for entry in ITEMS:
        roles[entry["role"]] = roles.get(entry["role"], 0) + 1
    print("WROTE %s seats=%d roles=%s" % (path, len(ITEMS), roles))


if __name__ == "__main__":
    main()
