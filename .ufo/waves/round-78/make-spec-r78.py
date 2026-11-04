#!/usr/bin/env python3
"""Build the round-78 w1 wave spec (13 seats, one v1 wave)."""

import json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROUND = LANE + "/.ufo/waves/round-78"
SCRATCH = "/fast/scratch/hyaku/mado-r78"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + f"""
Round mado 78, ONE v1 wave (13 seats). Claims (frozen; declaration {ROUND}/claims-declaration-r78.md):
C1 coverage — the margined auto exclusive-zone composition becomes a modelled join: 18 frozen cases
18/18, seven named mutations killed 7/7, held-r77 control 8/18; C2 operability — the read-only
runbook binds its volatile rows by shape: 17 cases, 17 executed, 17 matched, 12 shape-bound, held
fixed-value control 5/17. Read the declaration first; it is the frozen contract.

Frozen instruments and controls (never rewritten by a seat; every measurement is pinned here):
- {LANE}/tools/mado-barfoot.py (r78-v1, sha256 aac5d41b923711e174c6d62bb24da5a2b53abf7c938bfc5b68816929a12009c0)
- {LANE}/quality/counters/c1-r78-margins.py (sha256 1c39a53c9320b3f4c849ceb973e7fb0d42fb115e2f8f7a64bc3338fc4ab85000)
- {LANE}/quality/counters/c2-r78-runbook.py (sha256 b9c774b8883e9972a8975f87b3f0be4e17d9d0967e3f22659d001bab718d743a)
- {ROUND}/controls/c1-cases-r78.json (18 cases, sha256 99f1d82fd3476b151be2951549645ce71fd47b6d8a9e96f90a5f891bda5a56ae)
- {ROUND}/controls/c2-runbook-cases-r78.json (17 cases, sha256 f1c75a7dba92d7c1e0dae4feb60c022e0bacd4c95e03a95cfc53ccf7788932e8)
- Freeze b8508bd9; pre-wave amendment (fixture boxes + mutation anchors) 44a36b64; both counters
  TARGET_MET at 44a36b64 (receipts {ROUND}/receipts/measurement-c{{1,2}}-r78.txt). Base revision
  f597eccbffefd5fd6bbb01f3511c88bbeaed493c.
- Red-before receipts: {ROUND}/receipts/control-baseline-c1-r78.txt (correct=8/18 at base) and
  control-baseline-c2-r78.txt (rc 2 at base: two rows absent from SKILL.md).
- Pinned source bytes (read-only): {ROUND}/fetch/ (to be filled by the round's own fetches) and the
  round-77 copies under {LANE}/.ufo/waves/round-77/fetch/S457.bin, S462.bin, S464.bin. Host config is
  read-only: ~/.config/waybar/config.jsonc, ~/.config/hypr/**.

Hard bounds, every seat:
- Your write directory is {ROUND}/w1/<your name>/ plus the one scoped findings file the validator
  trailered for you ({ROUND}/w1/<your name>.md). Never edit a committed lane file (tools, quality,
  corpus, SKILL.md, SCORECARD.md, LOG.md, README, SOURCES.md, PROVINCE.md, the declaration, the
  control sets); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash/jj mutation); read-only
  git (`show`, `ls-tree`, `rev-parse`, `status`, `log`, `cat-file`) is fine. Never write the fleet
  repo, a sibling lane, ~/.config, .ufo/state/, .ufo/watchdog.log, .scratch/, scripts/, templates/
  or MANIFEST.json. Any fixture git repo lives under your scratch and every git call names `-C` it.
- Host posture: READ-ONLY probes only. Allowed: `hyprctl version|configerrors|monitors|workspaces|
  activeworkspace|getoption|binds|layers|clients|animations|workspacerules|devices|instances|
  systeminfo|submap|locked`, `pgrep`, `makoctl mode`, `systemctl --user is-active`, `busctl --user
  status|get-property`, `omarchy theme current|version|commands --json`, file reads. FORBIDDEN:
  any hyprctl write verb (`keyword`, `dispatch`, `reload`, `setprop`, `output …`, `plugin …`),
  any write under ~/.config or the repo, any socket connection, screenshots, package transactions,
  service restarts, compositor state changes. Never print an instance signature, window title or
  other session material.
- Scratch: {SCRATCH}/<your name>/ (create it, pass it explicitly, never use /tmp; copy any receipt you
  cite into your own dir, then delete the scratch dir before you finish).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps this
  task, first reading /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate) and
  recording tool/version/channel/reason in your report. ALL pacman transactions are PAUSED
  host-wide this run: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or report that
  you needed one; never `pacman -Sy/-S/-Syu/-U/-R`, never restart a host service.
- Never message `agent://all`; reply only to your L1 (`MadoR78`) or nothing.
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
do not run a mutating git/jj command. End with `Report: .ufo/waves/round-78/w1/{name}.md`.
"""


def item(name, role, body):
    return {"name": name, "role": role, "prompt": prompt(name, role, body)}


ITEMS = [
    item("R78ScoutMargins", "scout", """
Source reconnaissance (read-only) for the margined auto exclusive-zone model C1.

1. Open the pinned sources for yourself and locate the exact lines: Hyprland v0.56.2
   `src/render/Renderer.cpp` @ efb5099 (`applyExclusive` and `arrangeLayerArray`),
   gtk-layer-shell v0.10.1 `src/layer-surface.c` (`layer_surface_update_auto_exclusive_zone`),
   Waybar 0.15.0 `src/bar.cpp` (anchor clearing and the auto-zone call), and the wlr-layer-shell
   XML's `set_exclusive_zone` contract. Fetch fresh copies into {ROUND}/fetch/ (sha256 each).
2. Build an anchor table: for each reachable declaration (position top/bottom/left/right; margins
   by integer, CSS string, per-side; layer top/bottom; explicit width/height; output include and
   `!exclude`; exclusive false), state the client auto zone, the compositor addition and the
   resulting band, with file:line.
3. Attack the model in tools/mado-barfoot.py: find any reachable configuration where the recorded
   formula (`height + top + bottom`, transposed `width + left + right`) is wrong or where the tool's
   box arithmetic diverges from `arrangeLayerArray`. Name the discriminating fixture.
4. Name what the model cannot cover and why (negative margins, scaled outputs, static
   `addreserved`, dynamic cross size, centring rounding, a second exclusive consumer).
"""),
    item("R78ConnSiblings", "connector", """
Sibling-overlap and record scan (read-only).

1. Scan sibling repos under /home/vgpnk/Projects/shokunin/*-shokunin for any claim on the
   layer-shell plane, waybar margins, the monitor `reserved` band, or a runbook of `hyprctl`
   read rows. Report hits with file:line and the province they name; no overlap is a finding too.
2. Scan the lane's own record for the carried defect classes this round touches: stale revision
   citations (`measured at <hash>`, `its instrument's last change`), registry rows that describe
   superseded tool behaviour (the r77 `mado-barfoot` row), and ledger rows whose description no
   longer matches the instrument. Give each a file:line and a red/green-able command.
3. Check the two new instruments' provenance chain: declaration -> counter -> control set ->
   receipt, and name any link that is not committed or does not resolve at 44a36b64.
"""),
    item("R78ExecC1Tool", "executor", """
Adversarial fixtures against the new tool (write code and run it; red/green receipts).

1. Copy tools/mado-barfoot.py to your dir at rev 44a36b64 (`git -C {LANE} show
   44a36b64:tools/mado-barfoot.py`). Build fixtures that probe: malformed JSON/JSONC, non-regular
   inputs, >1 MiB inputs, a list-valued config, `mode` present, scale/transform refusals, dynamic
   cross sizes, negative margins, a namespace that does not exist, a level with two entries, an
   output spec with `*`, a monitor absent from either reply, and a huge/zero-size monitor.
2. For each: expected exit class from the docstring vs observed. Report every divergence with the
   fixture inline and the command line; fix nothing in the lane, propose the minimal repair.
3. Check the box arithmetic against `arrangeLayerArray` for a leading/trailing margin on each of the
   four positions, including a centred explicit width with margins.
"""),
    item("R78ExecC1Cases", "executor", """
Independent re-derivation of the eighteen frozen C1 expectations (read-only on the repo).

1. For every case in controls/c1-cases-r78.json, recompute by hand from the two source rules the
   declared box, band, expected and verdict; do not run the tool first, then run it and compare.
2. Flag any case whose fixture is inconsistent with its own declaration (a live box that does not
   match the declared box, a band that does not correspond to the declared margins, a duplicated
   case, a case whose verdict cannot separate the model from the held rule).
3. Report a table `case | declared | re-derived | tool | agree?` and a list of proposed case
   upgrades for a later round (not edits to the frozen set).
"""),
    item("R78ExecC2Shapes", "executor", """
Attack the shape matcher in quality/counters/c2-r78-runbook.py (write code and run it).

1. Copy the counter; add your own churn and negative samples to your copy of the case set for each
   shape kind: a valid-but-unexpected JSON type, a numeric string, a float where an int is asserted,
   an empty array where one item is required, a duplicated list entry, a negative pid, a
   whitespace-padded integer, a command that exits 0 with an error message on stdout.
2. Run the copy against the committed SKILL.md at 44a36b64 and report every sample that a correct
   r78 rule and a naive rule both accept (a weak shape) or both reject (an over-tight shape).
3. attack the churn clause: can a case pass while its live output is wrong? Prove any such path with
   a receipt.
"""),
    item("R78ExecC2Cases", "executor", """
Re-derive the seventeen runbook cases and their anchors (read-only on the repo, live read verbs).

1. For each case, run the command yourself, compare with the declared live expectation, and check
   the `skill_anchor` row in SKILL.md at 44a36b64 says what the case claims it says.
2. Flag every row whose anchor is shared with another row (the r77 `omarchy-version` defect class),
   every expectation that is really volatile but bound by value, and every command that needs an
   environment the counter silently supplies.
3. Report `case | live | declared | anchor row verdict | class`, and name which rows would break on
   a plausible host change (another workspace, a waybar restart, a theme switch).
"""),
    item("R78ScribeEntry", "scribe", """
Draft the C1 knowledge entry `bar-footprint-margins-r78.md` (write prose only; the L1 integrates).

1. Read corpus/knowledge/bar-footprint-r77.md for shape and voice, the frozen declaration, the case
   set and the measurement receipt. Draft a 60-110 line entry with provenance trio
   (`source:`, `verified-at:`, `recheck:`), the two-contributor composition with file:line anchors,
   a decision table of reachable declarations -> band, the worked case set, and a limits section.
2. Every number carries its command or its case name; every source claim names its S-id and line.
3. Include a short `## What is not claimed` section. Do not invent a measurement: use only the
   receipts named in the declaration and note anything you could not verify.
"""),
    item("R78ScribeSources", "scribe", """
Draft the round's frontier bookkeeping (prose only; the L1 integrates).

1. Read corpus/SOURCES.md rows S457, S462, S464 and the r77 lesson's Gate table. Draft the round-78
   lesson `## Gate` rows for the sources re-opened this round: URL, access date 2026-11-04, a
   located <=25-word quote from the stored bytes ({ROUND}/fetch/ or the round-77 copies), status,
   and what the row licenses / does not license.
2. Draft the in-place registry changes as old -> new pairs: `used-by` for S457/S462/S464 (adding
   `corpus/knowledge/bar-footprint-margins-r78.md`) and any `status` change; list them in a table.
3. Run the census commands from CORPUS.md (count rows, malformed rows, tier/status histograms,
   duplicate ids) at the current tip and paste the outputs with exit codes.
"""),
    item("R78RevC1", "reviewer", """
Byte-fidelity review of C1 (independent re-derivation; do not trust the receipt).

1. Re-extract tools/mado-barfoot.py at 44a36b64 and verify sha256 aac5d41b…; re-extract the base
   tool at f597eccb and verify e54787b7… . Re-run
   `python3 -I quality/counters/c1-r78-margins.py --repo {LANE} --rev 44a36b64 --base-rev f597eccb… --controls …`
   from a clean scratch and compare every count with the committed receipt.
2. Read the seven mutation anchors in the counter against the tool bytes: does each mutant change the
   named rule and does each kill come from a declared case (not a crash)? Name any survive or any
   kill by crash.
3. Check the model against the two source functions line by line: state whether each of the
   eighteen expectations is forced by the source, and name any assumption the declaration does not
   state.
"""),
    item("R78RevC2", "reviewer", """
Byte-fidelity review of C2 (independent re-derivation).

1. Verify the control-set sha256s and the counter bytes; re-run the counter at 44a36b64 and compare
   every line with the committed receipt.
2. Audit the churn/negative samples per case: is each churn sample genuinely plausible, and would a
   wrong implementation actually fail the negative? Name any sample that is vacuous or that no
   reachable state produces.
3. Audit the held-rule control: recompute `control=5/17` by hand and state whether the held r77 rule
   could reach the target under any live state (the counter's own separation claim).
4. Check the anchor binding: 17/17 anchors resolve, and no anchor is shared between two rows in a
   way that hides a wrong row.
"""),
    item("R78CritClaims", "critic", """
Falsify the claim design (read the declaration, the counters and the receipts; argue, do not edit).

1. Is C1 a coverage move and C2 an operability move under AXES.md? Name the surface each changes and
   the command that would show it unmoved.
2. Is the control sufficient in each claim? Try to construct a do-nothing change that still scores
   TARGET_MET (e.g. a tool that hardcodes the eighteen verdicts, a counter whose churn clause never
   runs, a shape rule that accepts everything). If one exists, the target is wrong: point at the
   exact line and the case that fails to separate.
3. Are the claims causally separable? Try to land one without the other and name any coupling.
4. Name any target that is not one value a closure can re-derive with one command over committed
   bytes, and any universal clause the predicates do not enumerate.
"""),
    item("R78MutC1", "mutation-tester", """
Own mutants of the r78 reserved-band rule (write code; run against the frozen set).

1. Write >=10 mutants of tools/mado-barfoot.py outside the seven frozen ones: band edge selection,
   margin sign, per-side precedence order, centring arithmetic with margins, level order, output
   include/exclude precedence, extent for bottom/left/right, the exclusivity branch, rounding, and
   the refusal conditions. Run each against your copy of the eighteen frozen cases.
2. Report `mutant | killed/survived | killing case`; for each survivor classify it as a real model
   gap (name the discriminating case) or an algebraic equivalent (prove it on every case).
3. State the coverage bound the eighteen cases impose and the three strongest cases a successor set
   should add.
"""),
    item("R78Sentinel", "sentinel", """
Safety, privacy and scratch audit (read-only).

1. Audit the two counters and the tool for: writes outside caller scratch, `/tmp` hardcodes,
   network, socket use, process spawning beyond the declared read verbs, environment leakage, and
   path refusals (symlinks, `/`, traversal). Report file:line and a command that shows the defect.
2. Audit every receipt in {ROUND}/receipts/ and every fetch the round commits for session material:
   instance signatures, window titles, pids paired with names, home listings, full process tables.
   Name the rule (R1-R6 of quality/check-session-material.py) and the line.
3. Check the wave's own hygiene: any seat-visible path that would write into the fleet repo, any
   scratch tree left behind, any secret-shaped string in the new prose.
"""),
]


def main():
    spec = {
        "wave": "w1",
        "reportDir": ".ufo/waves/round-78/w1",
        "context": CONTEXT,
        "items": ITEMS,
    }
    with open(ROUND + "/w1-spec.json", "w") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    print("wrote %d items to %s/w1-spec.json" % (len(ITEMS), ROUND))


if __name__ == "__main__":
    main()
