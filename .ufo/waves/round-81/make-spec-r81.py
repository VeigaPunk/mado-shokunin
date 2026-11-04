#!/usr/bin/env python3
"""Generate `.ufo/waves/round-81/w1-spec.json` (ONE v1 wave, 14 seats).

Seat paths are absolute; the runner renders a relative `Report:` trailer that a seat must
resolve from the lane root, and the context says so. Nothing here is a claim: the claim
contract lives in `.ufo/waves/round-81/claims-declaration-r81.md` (frozen at
`0e2ccd2a8692825cac534f57246053b276be9f13`).
"""

import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROUND = LANE + "/.ufo/waves/round-81"
FREEZE = "0e2ccd2a8692825cac534f57246053b276be9f13"
BASE = "c702094ace5dd9b2b5e152951b4b2f4dd578f8b6"
SCRATCH = "/fast/scratch/hyaku/mado-r81"

DIRECTIVE = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = DIRECTIVE + """
Round mado 81, ONE v1 wave (14 seats). Lane root: {LANE}.
Claims (frozen; declaration {ROUND}/claims-declaration-r81.md, freeze `{FREEZE}`, base `{BASE}`):
C1 coverage — the composition's overflow rounding and its auto-zone gate: 39 frozen cases (33
carried from round 80 parsed-equal + 6: `overflow-tie-negative`, `auto-dynamic-band-refused`,
`auto-corner-edge`, `auto-all-four-edge`, `auto-parallel-edge`, `auto-left-dock`), 28 named
mutations killed, the held round-80 tool `base_correct=33/39`, tool selftest 121/121; C2
operability — the runbook gains an action-column matcher (`cut -c36-`) and a `pgrep -x waybar`
PID-list/exit-status matcher: 26 cases / 26 rows / 26 distinct anchors, `control_new=0/2`, 23
matcher mutants killed.

Frozen instruments (never rewritten by a seat):
- {LANE}/tools/mado-barfoot.py (r81-v1, sha256 a129a435…)
- {LANE}/quality/counters/c1-r81-overflow-auto.py (sha256 22405133…)
- {LANE}/quality/counters/c2-r81-runbook.py (sha256 1bc9ca40…)
- {ROUND}/controls/c1-cases-r81.json (sha256 ab8154a1…, 39 cases)
- {ROUND}/controls/c2-runbook-cases-r81.json (sha256 ae7ee90e…, 26 cases)
- {ROUND}/receipts/measurement-c{{1,2}}-r81.txt (the round's measured receipt at the freeze)

Ground truth sources already pinned in the lane (open the committed bytes, do not re-fetch unless a
prompt says so): {ROUND}/fetch/S478.bin = hyprutils v0.14.0 `src/math/Box.cpp`; S479.bin = Hyprland
`CMakeLists.txt` at efb50993 (`set(HYPRUTILS_MINIMUM_VERSION 0.14.0)`); {LANE}/.ufo/waves/round-80/
fetch/S470.bin = Hyprland `src/render/Renderer.cpp`; {LANE}/.ufo/waves/round-79/fetch/S464.bin =
gtk-layer-shell v0.10.1 `src/layer-surface.c`; {LANE}/.ufo/waves/round-80/fetch/S473.txt =
`~/.local/share/omarchy/bin/omarchy-menu-keybindings`.

## Absolute rules for every seat
- Every path you read or write is absolute under {LANE}. Never write to the fleet repo
  /home/vgpnk/Projects/shokunin, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, or
  `/home/vgpnk/Projects/shokuknow`.
- Write only inside your own seat directory {ROUND}/w1/<YourSeatName>/ and your own scratch dir
  {SCRATCH}/<YourSeatName>/. Copy any receipt you want kept into your seat directory BEFORE you
  yield, then remove your scratch dir (`trap 'rm -rf -- "$S"' EXIT` in shell; `finally:
  shutil.rmtree` in Python). Never use /tmp as evidence: it is reaped and never citable.
- Never run a mutating git or jj command anywhere (`git add|commit|stash|checkout|switch|reset|
  pull|push`, `jj commit|new|describe|squash|rebase|abandon|bookmark|undo`). Read-only git
  (`log`, `show`, `diff`, `status`, `rev-parse`) is fine. If you need a fixture repo it is
  `D=$(mktemp -d)` under your scratch dir and every git call names `-C "$D"`.
- The lane's git HEAD is detached: name revisions by the branch (`master`) or the hashes above.
- Never message `agent://all`; never edit the frozen instruments, the control sets, the
  declaration, SKILL.md, or LOG.md — you report, the L1 integrates.
- Every `Report:` trailer path the runner prints is relative to {LANE}: write it at
  {LANE}/<that path>. Also write a `findings.md` in your seat directory whose last line is
  `STATUS: ok` (or `blocked` / `partial`) and which quotes every command you ran with its exact
  argv and the lines that matter.
- Evidence discipline: quote the literal output line, never paraphrase; an unrun check has not
  passed. If a source contradicts the claim, say so plainly — that is the seat's value.

## Tooling authorization (operator, 2026-10-19)
You may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first
(official channels, update-safety gate; record tool/version/channel/reason in findings). **pacman
guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide.** Install via
`uv tool` / `npx` / an official binary in `~/.local/bin`, or file no install at all. Never `pacman
-S`, `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service.
"""

CTX = CONTEXT.format(LANE=LANE, ROUND=ROUND, FREEZE=FREEZE, BASE=BASE, SCRATCH=SCRATCH)


def item(name, role, prompt):
    return {"name": name, "role": role, "prompt": prompt}


ITEMS = [
    item("R81ScoutLive", "scout",
         """Live recon on today's host (read-only; no compositor verb that changes state).

1. Capture `hyprctl monitors -j` and `hyprctl layers -j` into your seat dir. **Redact** every
   monitor `description`, `serial`, `make`, `model` field to `<redacted: ...>` before saving (the
   r78 L0 question's R5 rule). Then run the lane join on that capture:
   `python3 -I {LANE}/tools/mado-barfoot.py --monitors <capture> --layers <capture2>
   --config ~/.config/waybar/config.jsonc` (add `--surfaces` only if you can derive the declared
   extra surfaces from the capture; say which flag set you used). Quote the `MADO_BARFOOT_RESULT:`
   line and the `DECL` lines.
2. State the live layer census (namespace, level, box, pid count) and whether the bar's own box
   matches the declared `height`/`position` on today's host.
3. Read {ROUND}/fetch/S478.bin `CBox::round` (`:51-63`) and {LANE}/.ufo/waves/round-80/fetch/
   S470.bin `arrangeLayerArray` (`:2587-2671`). Say whether today's live boxes can ever reach the
   negative-tie class the round freezes, and why (the host's bar width vs monitor width).
4. Name two limits of the live join you observed, with the command that shows each.""")
    ,
    item("R81ScoutModel", "scout",
         """Source recon against the frozen new cases (read-only; no code edit).

1. Open {ROUND}/controls/c1-cases-r81.json and list the six new case names with their frozen
   `expect` values.
2. For each, re-derive the expected RESULT fields from the sources by hand and paste the arithmetic:
   `overflow-tie-negative` from {ROUND}/fetch/S478.bin `:51-63` plus {LANE}/.ufo/waves/round-80/
   fetch/S470.bin `:2610-2621,2660`; `auto-*` cases from {LANE}/.ufo/waves/round-79/fetch/
   S464.bin `:264-292`; the left dock's attribution from S470 `:2544-2573` and
   `:2673-2700`.
3. Identify any case whose expectation you cannot derive from the bytes alone, and say exactly what
   is missing (do not guess).
4. Probe the successor tool for reachable classes the frozen 39 do **not** pin (write fixtures only
   under your scratch dir, delete them before you yield). Record at most four classes with the exact
   `DECL`/`RESULT` lines; mark each `right`, `wrong` or `refused`. This is round 82's ground, not a
   claim: do not propose a target.""")
    ,
    item("R81ConnSiblings", "connector",
         """Sibling-overlap scan for the round's ground (read-only across the fleet).

1. Does any sibling lane claim either of this round's grounds? Check at least
   /home/vgpnk/Projects/shokunin/game-dev-3d-shokunin/PROVINCE.md, kotoba-shokunin/PROVINCE.md,
   kumitate-shokunin/PROVINCE.md and each sibling's `tools/` for: (a) layer-surface reserved-band or
   layer-arrangement modelling, (b) an auto-exclusive-zone implementation, (c) a runbook row
   grammar over omarchy output, (d) a `pgrep`-shaped liveness matcher. Quote file:line for every
   hit and name homonyms that a census must not merge.
2. Check the staged assimilation package /home/vgpnk/Projects/shokuknow/merge/mado/ (read-only; run
   nothing there) for an entry touching either ground; if one exists, say which entry and whether
   it would duplicate a row this round adds.
3. State whether a later r81 census could mistake any sibling artifact for mado's, and how your
   finding prevents it.""")
    ,
    item("R81ExecC1Run", "executor",
         """Run the C1 counting command verbatim at the freeze, then re-derive two cases by hand.

1. From {LANE} run exactly:
   `python3 -I quality/counters/c1-r81-overflow-auto.py --repo . --rev {FREEZE} --base-rev {BASE}
   --controls .ufo/waves/round-81/controls/c1-cases-r81.json --carried
   .ufo/waves/round-80/controls/c1-cases-r80.json --scratch-root {SCRATCH}/R81ExecC1Run`
   Paste the final `MADO_R81_BARFOOT:` line and its exit code. Save the full output in your seat
   dir as `c1-run.txt`.
2. Without reading `tools/mado-barfoot.py`, re-derive by hand and paste the arithmetic for
   `overflow-tie-negative` (hyprutils {ROUND}/fetch/S478.bin `:51-63` + Hyprland `Renderer.cpp`
   `:2610-2621,2660`) and `auto-left-dock` (gtk-layer-shell {LANE}/.ufo/waves/round-79/fetch/
   S464.bin `:264-292` + `applyExclusive` `:2544-2573`). State both expected RESULT lines.
3. Write the two case fixtures from the frozen set into your scratch dir (config/layers/monitors/
   surfaces) and run the tool on them; compare every field (`box`, `boxes`, `band`, `expected`,
   `attributed`, `attr`, `gt`, `ls`, `verdict`) against your hand derivation and report AGREE or the
   exact field that differs.
4. Run `python3 -I {LANE}/tools/mado-barfoot.py --selftest` and paste the tally.""")
    ,
    item("R81ExecC2Run", "executor",
         """Run the C2 counting command verbatim, then execute both new rows by hand.

1. From {LANE} run exactly:
   `python3 -I quality/counters/c2-r81-runbook.py --repo . --rev {FREEZE} --controls
   .ufo/waves/round-81/controls/c2-runbook-cases-r81.json --carried
   .ufo/waves/round-80/controls/c2-runbook-cases-r80.json --scratch-root {SCRATCH}/R81ExecC2Run`
   Paste the final `MADO_R81_RUNBOOK:` line and its exit code; save the full output as `c2-run.txt`.
2. Execute both new rows by hand from {LANE}: `omarchy menu keybindings --print | cut -c36-` and
   `pgrep -x waybar`. Paste the first five lines of the first (with `cat -A` on one), the line count,
   and the second's stdout + `echo $?`. Then read the payload
   {LANE}/.ufo/waves/round-80/fetch/S473.txt around the `printf "%-35s → %s\\n"` line and state in
   bytes/characters where the separator sits (which byte offset the arrow begins at).
3. Look for any live line in the action column that would break a stricter grammar (a bare `&`, a
   `<`, a trailing space, a second `→`): grep for each and paste counts. Say whether the frozen
   grammar's bound outcome (` → ` prefix, non-empty trimmed action, no second arrow) is right for
   today's payload.
4. Run `python3 -I quality/counters/c2-r81-runbook.py --selftest` and paste the tally.""")
    ,
    item("R81ExecMutants", "executor",
         """Independent mutation census of the six new C1 mutants (do not use the counter's mutant loop).

1. For each of `tie-round-trunc`, `round-width-spec`, `auto-gate-open`, `auto-gate-and`,
   `auto-axis-swapped`, `auto-dynamic-kept`: copy {LANE}/tools/mado-barfoot.py into your scratch
   dir, apply the same single-anchor mutation by hand (read the anchor from
   `{LANE}/quality/counters/c1-r81-overflow-auto.py` `MUTATIONS`), and score it with
   `python3 -I quality/counters/c1-r81-overflow-auto.py --repo {LANE} --rev <mutant-source-path?>
   ...` — note the counter reads the tool from `--rev`, so instead run the tool itself on the six
   new case fixtures and count how many of the six the mutant gets wrong; paste per-mutant which
   case separates it.
2. State for each mutant the *one* case that kills it and the field that differs; a mutant with no
   separating case is a real defect — say so.
3. Also confirm each anchor occurs exactly once in the tool bytes
   (`grep -c -F`), and that removing the anchor makes the counter print
   `reason=anchor-absent` rather than crashing.""")
    ,
    item("R81ScribeEntry", "scribe",
         """Draft the C1 knowledge entry (prose only; the L1 integrates it).

Write `{ROUND}/w1/R81ScribeEntry/entry-draft.md` in the shape of
{LANE}/corpus/knowledge/bar-footprint-composition-r80.md: a `source:` line, `verified-at:`, a
`recheck:` line naming the frozen counting command, then sections:

1. **What this entry is and is not** — a model over captured bytes; no surface is created.
2. **`CBox::round` is coupled** — quote {ROUND}/fetch/S478.bin `:51-63` with line anchors; derive
   the 1001-wide overflow (`x=-1, w=1002`) and show why floor-dividing the offset gives `0/1001`.
3. **Which hyprutils revision this is** — {ROUND}/fetch/S479.bin `:150` pins
   `HYPRUTILS_MINIMUM_VERSION 0.14.0`; state the inference class (the host runs 0.56.2; the
   minimum version is the tag licence, not a runtime read).
4. **The auto zone is the client's** — gtk-layer-shell {LANE}/.ufo/waves/round-79/fetch/S464.bin
   `:264-292`: the gate on `horiz`/`vert`, the allocation source, the unanchored margins. State
   which classes the join now refuses and why (`height = 0` auto has no allocation input).
5. **The gate's composition consequence** — corner / parallel / all-four anchor sets send no zone,
   so an explicit `exclusiveEdge` alone cannot make one reserve; the left dock's band reaching the
   attribution vector.
6. **What the join prints** — the `DECL`/`ATTR`/`RESULT` fields the six new cases pin.
7. **Limits** — the allocation is not modelled (refusal), the dynamic-band refusal is per-axis, the
   declaration grammar's `exclusive` default is still `auto` (a plain client must say `0`), and the
   r80 §11 item-4 defect is therefore still open.
8. **Gate block** — list the two new SOURCES rows you expect (S478, S479) with URL, access date
   2026-11-04 and a ≤25-word located quote each, taken verbatim from the pinned bytes.

Every claim needs a file:line. Do not invent an observation; if you cannot derive a sentence from
the bytes, write `[UNK]` and say what would settle it.""")
    ,
    item("R81ScribeSources", "scribe",
         """Draft and verify the two new SOURCES.md rows (prose only; the L1 appends).

1. Read {LANE}/corpus/SOURCES.md's header and the last ten rows to copy the exact 11-column schema
   (id · source · tier · status · teaches · anchor/quote · status · recheck · used-by · …). Print the
   header row and the column count you derived.
2. Draft **S478** (hyprutils v0.14.0 `src/math/Box.cpp`) and **S479** (Hyprland
   `CMakeLists.txt` @ efb50993, `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)`) as rows in that schema.
   Verify each ≤25-word quote against the pinned bytes with `grep -n -F` and paste the hits; verify
   the pins with `cd {ROUND}/fetch && sha256sum -c sha256-r81.txt`.
3. Check the id space: `grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' {LANE}/corpus/SOURCES.md |
   grep -oE 'S[0-9]+' | sort | tail -5` and prove S478/S479 are unused.
4. Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin mado` and paste the exit code plus the summary line. Then state
   which row the C1 claim rests on (it must be one of the two) and what each row does *not* license.""")
    ,
    item("R81ScribeLesson", "scribe",
         """Draft `corpus/lessons/round-81.md` (prose only; the L1 integrates).

1. Read the last two lessons ({LANE}/corpus/lessons/round-80.md and
   round-80-verifier-spotcheck.md) for the shape: a `## Mistakes` table (class · evidence pointer ·
   captured-by · fix) and a `## Gate` block.
2. Mine at least two mistakes with byte-exact pointers. Candidates you must check, and confirm or
   reject each with the command:
   (a) the first r81 C2 case imported the payload's XML-entity escaping as a rule, and one live
       action carries a **bare** `&` — `omarchy menu keybindings --print | cut -c36- | grep -c '&'`
       → 2, one of them bare at the `Pop window out (float & pin)` line; the grammar was narrowed
       and a positive sample now pins the correction.
   (b) `pgrep -x waybar` output was `.strip()`ed, so a padded `" 1720"` matched; the matcher now
       rstrips only newlines and a negative pins it.
   (c) the r80 §11 attribution "the tool's `(bounds.w - w + 1)//2` … never recomputes `w`" versus
       the successor's coupled `CBox::round` — is the r80 sentence right for the tool it described?
3. `## Gate` block: the census command with both outputs and exit codes (start 412 rows/exit 0 is
   the round's start; run it again yourself and paste today's), the two new rows with URL, access
   date 2026-11-04 and located quote, and ≥1 admit + ≥1 reject from the assimilation set
   (/home/vgpnk/Projects/shokuknow/merge/mado/, read-only) if any entry is in scope.
4. Write it as `{ROUND}/w1/R81ScribeLesson/lesson-draft.md`; quote every command and output.""")
    ,
    item("R81ReviewerC1", "reviewer",
         """Adversarial review of C1 (read-only; no edits).

1. Re-derive all six new case expectations from the pinned sources **without reading the tool's
   code first**; only afterwards read {LANE}/tools/mado-barfoot.py's `arranged_box`, `std_box`,
   `surface_zone` and say whether the code is the source's arithmetic or an approximation that
   happens to pass.
2. Check the carried assertion: print `python3 -c` equality of
   `{ROUND}/controls/c1-cases-r81.json` `.cases[:33]` against the round-80 set (parsed), and the
   sha256 of the 39-case file.
3. Attack the mutants: is any of the 28 killed by a case that does not actually test the rule
   (`killed` for the wrong reason)? Name any mutant that only dies on a carried case.
4. Attack the base control: does `base_correct=33/39` hold because the r80 tool genuinely fails all
   six new cases, or does one new case accidentally pass at the base? Run the base tool yourself on
   the six fixtures and paste the six verdicts.
5. Name the strongest sentence in the entry draft ({ROUND}/w1/R81ScribeEntry/entry-draft.md, if it
   exists) that the bytes do not support, or state that every sentence is anchored.""")
    ,
    item("R81ReviewerC2", "reviewer",
         """Adversarial review of C2 (read-only; no edits).

1. Execute the two new rows by hand and test the frozen grammar against **today's real output**:
   paste the counts of every character class the grammar forbids/rejects (second `→`, trailing
   space, leading space, non-decimal PID). Then construct three *plausible* payload changes
   (a 36-character chord, a bind whose action is a single word, a bar restarted with two processes)
   and say whether the grammar still binds — the row must survive host churn without freezing it.
2. Check the carried assertion: for all 24 carried cases, compare every field but `skill_anchor`
   against the round-80 set and print the diff (empty expected); print the 26 distinct anchors.
3. Attack the `held_rule` control: `control_new=0/2` is required; print the held rule's decision on
   each of the two new cases and on two carried cases, and say whether the control is a real
   do-nothing control (would a frozen value pass?).
4. Read the counter's `action_column` and `pid_state` implementations and name any input on which
   they disagree with the row's prose in {LANE}/SKILL.md (quote the row's cell).
5. State whether the r80 table's `pgrep -x waybar | head -n 1` row (still present) can read DIFFER
   while this round's `pgrep -x waybar` row reads CLEAN — i.e. whether the two rows are consistent.""")
    ,
    item("R81CriticClaims", "critic",
         """Falsify the round's claims and its own contract (read-only; no edits).

Read {ROUND}/claims-declaration-r81.md in full. Then:

1. For each claim, state the cheapest do-nothing or wrong-model artifact you can build that still
   prints `TARGET_MET` under the frozen counter (write it under your scratch dir only). If you find
   one, the counter or the target is wrong — say exactly which clause fails to bind.
2. Check the predicate sentence is the same sentence in the declaration, the counter's code and the
   receipt label. Quote all three.
3. Check the claim names the surface it moves, not the number: "the composition's overflow rounding
   and its auto-zone gate" and "the action column and the bar's pgrep state" — is each a coverage
   / operability move, or a re-score of ground the lane already held? Justify with the r80 §11 limit
   list and the r80 SKILL rows.
4. Check the exploratory-claim rules are not being evaded (no claim here is exploratory).
5. Attack the *harm* watch: name any axis this round could harm, and the command that would show it.
6. Give a verdict per claim: `admit`, `admit-with-caveat` (name the caveat), or `reject` (name the
   clause).""")
    ,
    item("R81MutC1Counter", "mutation-tester",
         """Mutate the C1 counter itself and prove it fails closed (writes only in your scratch dir).

1. Copy {LANE}/quality/counters/c1-r81-overflow-auto.py into your scratch dir and apply, one at a
   time, at least six counter-side mutations, e.g.: (a) accept a wrong `expect.band`; (b) skip the
   carried equality check; (c) count `killed` without running the mutant; (d) ignore a red tool
   selftest; (e) accept `base_correct != 33`; (f) let a `Setup` error exit 0. For each, run the
   counter against the lane and paste the final line + exit code; the mutant must print
   `TARGET_MISSED` or exit 2/1 — a mutant that prints `TARGET_MET` is a finding.
2. Then tamper with the *tool* one field at a time (e.g. force `reserved=EQ`; zero the attribution
   vector) and confirm the counter catches it.
3. Report which internal check is load-bearing for each tamper, and any check that is present but
   **unexercised** (no mutant separates it).""")
    ,
    item("R81Sentinel", "sentinel",
         """Security review of the round's bytes (read-only).

1. Scan every file the round adds or changes for credential material, session identifiers, serial
   numbers, EDID strings, home-path leaks and tokens:
   `grep -rnE '(serial|description|EDID|token|secret|password|Bearer|api[_-]?key)'` over
   {ROUND}/ and the two new counters; report every hit with file:line and whether it is a field
   name, a redaction, or a leak. Confirm no monitor `serial`/`description` value appears in any
   receipt or seat output.
2. Check the two new counters' scratch handling: no hardcoded `/tmp`, `TMPDIR` honoured, the scratch
   root refused when `/` or a symlink, no write outside the caller's scratch dir. Quote the code
   lines.
3. Check the new runbook rows are read-only: neither command writes (`omarchy-menu-keybindings
   --print` only prints; `pgrep` only reads) — prove it from the payload bytes for the first and from
   the process table for the second.
4. Check the wave seats cannot reach the lane's git/jj state: list the paths the round's seat
   prompts allow, and any prompt text that could lead a seat to commit.
5. Verdict: `clean` with the checks named, or `defect` with file:line.""")
]


def main():
    kw = dict(LANE=LANE, ROUND=ROUND, FREEZE=FREEZE, BASE=BASE, SCRATCH=SCRATCH)
    items = [dict(item, prompt=item["prompt"].format(**kw)) for item in ITEMS]
    spec = {"wave": "w1", "reportDir": ".ufo/waves/round-81/w1", "context": CTX,
            "items": items}
    out = os.path.join(ROUND, "w1-spec.json")
    with open(out, "w") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    print("wrote %s: %d items (%s)" % (out, len(items),
                                       ", ".join(i["role"] for i in items)))


if __name__ == "__main__":
    main()
