#!/usr/bin/env python3
"""Generate `.ufo/waves/round-82/w1-spec.json` (ONE v1 wave, 14 seats).

Seat paths are absolute; the runner renders a relative `Report:` trailer that a seat must
resolve from the lane root, and the context says so. Nothing here is a claim: the claim
contract lives in `.ufo/waves/round-82/claims-declaration-r82.md` (frozen at
`780c30fcae12d74ce8ab3b871a0888696c2415d9`).
"""

import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROUND = LANE + "/.ufo/waves/round-82"
FREEZE = "780c30fcae12d74ce8ab3b871a0888696c2415d9"
BASE = "6ea2386d49318a5f223097c78b5fe79c31b064f8"
SCRATCH = "/fast/scratch/hyaku/mado-r82"

DIRECTIVE = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = DIRECTIVE + """
Round mado 82, ONE v1 wave (14 seats). Lane root: @@LANE@@.
Claims (frozen; declaration @@ROUND@@/claims-declaration-r82.md, freeze `@@FREEZE@@`, base `@@BASE@@`):
C1 coverage — the client's own band: a declared dynamic band (`height = 0` horizontal,
`width = 0` vertical) is modelled through a declared `--allocation` map instead of refused: 47
frozen cases (39 carried from round 81 parsed-equal + 8), 34 named mutations killed, the held
round-81 tool `base_correct=39/47`, tool selftest 133/133. C2 operability — the tray plane in
the read-only runbook: `busctl --user list` (watcher owner by live PID), `busctl --user introspect`
(watcher interface census) and the census's method table, 29 cases / 29 rows / 29 distinct
anchors, `control_new=0/3`, 25 matcher mutants killed.

Frozen instruments (never rewritten by a seat):
- @@LANE@@/tools/mado-barfoot.py (r82-v1, sha256 38007528…)
- @@LANE@@/quality/counters/c1-r82-allocation-band.py (sha256 1e9f394d…)
- @@LANE@@/quality/counters/c2-r82-runbook.py (sha256 1e8eb499…)
- @@ROUND@@/controls/c1-cases-r82.json (sha256 e404bb3f…, 47 cases)
- @@ROUND@@/controls/c2-runbook-cases-r82.json (sha256 f64d7d5d…, 29 cases)
- @@ROUND@@/receipts/measurement-c1-r82.txt and measurement-c2-r82.txt (the measured receipts at a.rev)

Ground truth sources already pinned in the lane (open the committed bytes, do not re-fetch unless a
prompt says so): @@LANE@@/.ufo/waves/round-79/fetch/S464.bin = gtk-layer-shell v0.10.1
`src/layer-surface.c` (the auto zone at `:264-292`); @@LANE@@/.ufo/waves/round-80/fetch/S470.bin
= Hyprland `src/render/Renderer.cpp` (arrangeLayerArray, applyExclusive); @@LANE@@/.ufo/waves/
round-79/fetch/S466.bin = `src/desktop/reserved/ReservedArea.cpp`.

## Absolute rules for every seat
- Every path you read or write is absolute under @@LANE@@. Never write to the fleet repo
  /home/vgpnk/Projects/shokunin, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, or
  `/home/vgpnk/Projects/shokuknow`.
- Write only inside your own seat directory @@ROUND@@/w1/<YourSeatName>/ and your own scratch dir
  @@SCRATCH@@/<YourSeatName>/ (create it; `trap 'rm -rf -- "$S"' EXIT` or
  `shutil.rmtree` in a `finally`). Never write to `/tmp`. A copy of the lane for experiments is
  `git clone --shared /home/vgpnk/Projects/shokunin/mado-shokunin <your scratch>/repo` — never a
  full clone.
- You never commit, push, or run a mutating git/jj command, in the lane or anywhere. Read-only git
  (`show`, `log`, `diff`, `rev-parse`, `ls-tree`) is fine. Never edit the frozen instruments or the
  claim declaration; a seat that believes one is wrong reports it, and the L1 decides.
- Never call `task` or spawn another agent. You are a leaf seat.
- Never message another seat or `agent://all`; report only through your files.
- Redact before saving any capture: monitor `description`/`serial`/`make`/`model`, any token,
  session id or home path outside the lane tree. Shape-only harness captures are the rule.
- Tooling authorization (operator 2026-10-19): you may install or upgrade a tool that helps the
  task — first read /home/vgpnk/.omp/agent/RULES.md (official channels only). **pacman transactions
  are PAUSED host-wide** (orchestrator ruling 2026-10-20): install via `uv tool`/`npx`/an official
  binary in `~/.local/bin`, or file nothing; never `pacman -S/-Sy/-Syu/-U/-R` and never a partial
  upgrade. Record tool/version/channel/reason in your report.
- Every `Report:` trailer path the runner prints is relative to @@LANE@@ — write it at
  @@LANE@@/<that path>.
- Your final line in the findings log is `STATUS: ok` (work complete, evidence written),
  `STATUS: defect` (you found a real defect; name it with file:line) or `STATUS: blocked`
  (with the exact missing input).
"""


def item(name, role, prompt):
    return {"name": name, "role": role, "prompt": prompt}


ITEMS = [
    item("R82ScoutModel", "scout",
         """Reconnaissance of the round-82 model (read-only).

1. Read the tool diff `git -C @@LANE@@ diff @@BASE@@ @@FREEZE@@ -- tools/mado-barfoot.py` and list
   exactly what changed: the `parse_allocation` grammar, `band_of`, `declared_box`, the
   composition's band resolution, and the `--allocation` CLI.
2. Read the eight new cases in @@ROUND@@/controls/c1-cases-r82.json (names starting `alloc-`).
   For EACH, recompute the expected box and band by hand from the cited arithmetic
   (@@LANE@@/.ufo/waves/round-79/fetch/S464.bin at `:264-292`, the arrange/margin arithmetic in
   @@LANE@@/.ufo/waves/round-80/fetch/S470.bin) and say DERIVED or NOT-DERIVABLE with the line that
   does not follow. Do not run the counter for this item; this is a hand check.
3. State the classes that remain REFUSED after this round (the per-axis dynamic extra surface, the
   fractional-scale monitor, the allocation bypass) with the code line that refuses each.
4. Report the tool's declared `VERSION` and its `--selftest` tally (`python3 -I tools/mado-barfoot.py
   --selftest` with TMPDIR inside your scratch).

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ScoutModel.md."""),

    item("R82ScoutLive", "scout",
         """Live surface recon (read-only; no compositor verb that changes state).

1. Capture `hyprctl monitors -j` and `hyprctl layers -j` into your seat dir, **redacted**: every
   monitor `description`, `serial`, `make`, `model` field becomes `<redacted: ...>` before saving.
   Record sha256 of the redacted bytes and the monitor name/reserved/scale only.
2. Run the bar-footprint join against those captures for DP-1 and report the RESULT line and its
   verdict (`python3 -I @@LANE@@/tools/mado-barfoot.py --config <a waybar config you write with
   height 26 top> --layers <capture> --monitors <capture> --monitor DP-1`). If the live box differs
   from the model, say DIFFER and why in one sentence — do not "fix" it.
3. Run the three round-82 runbook commands and report the matching line and its shape verdict:
   `busctl --user list`, `busctl --user introspect org.kde.StatusNotifierWatcher
   /StatusNotifierWatcher --no-pager`, and the same introspect piped through `awk '$2=="method"'`.
   Report counts only; never quote a PID with its process name together unless it is waybar and the
   prompt asks.
4. Report the current waybar process state (`pgrep -x waybar` exit status and PID) as a state pair.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ScoutLive.md."""),

    item("R82ConnSiblings", "connector",
         """Sibling-overlap scan (read-only; sibling repos are read-only surfaces).

1. Search the sibling lane repos under /home/vgpnk/Projects/shokunin for any claim on this round's
   two grounds: (a) layer-shell/protocol surface sizing and the client allocation (terms:
   `layer_surface`, `set_size`, `exclusive_zone`, `waybar`, `bar footprint`, `allocation`);
   (b) the StatusNotifierWatcher/tray plane (terms: `StatusNotifier`, `busctl --user`,
   `tray`). Use `grep -ril` over each `*-shokunin/` tree's `corpus/`, `SKILL.md` and `PROVINCE.md`,
   excluding @@LANE@@ itself.
2. For each hit, say which lane, which file:line, whether it is the same ground (contested) or a
   different surface the other lane owns, and what this lane's report should name.
3. State plainly if no sibling claims either ground.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ConnSiblings.md."""),

    item("R82ExecC1Run", "executor",
         """Independent replay of the C1 counting command (read-only over the lane).

1. Run the frozen C1 command verbatim at the freeze and at the base, into your scratch root:
   `python3 -I quality/counters/c1-r82-allocation-band.py --repo . --rev @@FREEZE@@ --base-rev
   @@BASE@@ --controls .ufo/waves/round-82/controls/c1-cases-r82.json --carried
   .ufo/waves/round-81/controls/c1-cases-r81.json --scratch-root <your scratch>`
   (run it with cwd @@LANE@@). Save the full output.
2. `diff` your output against @@ROUND@@/receipts/measurement-c1-r82.txt and report whether every
   line except the scratch-dependent none is byte-identical; report any difference with both lines.
3. Re-run the base-only control (`--rev @@BASE@@ --base-rev @@BASE@@`) and compare to
   @@ROUND@@/receipts/control-c1-r82-at-base.txt.
4. Report the six numbers from the contract line and the exit statuses. Do not edit anything in the
   lane.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ExecC1Run.md."""),

    item("R82ExecC2Run", "executor",
         """Independent replay of the C2 counting command and the three tray rows (read-only).

1. Run the frozen C2 command verbatim (cwd @@LANE@@, freeze `@@FREEZE@@`, controls
   `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json`, carried
   `.ufo/waves/round-81/controls/c2-runbook-cases-r81.json`, your scratch root) and `diff` the
   output against @@ROUND@@/receipts/measurement-c2-r82.txt.
2. Re-run the held round-81 instrument at the freeze
   (`quality/counters/c2-r81-runbook.py --repo . --rev @@FREEZE@@ --controls
   .ufo/waves/round-81/controls/c2-runbook-cases-r81.json --carried
   .ufo/waves/round-80/controls/c2-runbook-cases-r80.json --scratch-root …`) and confirm it exits 2
   with the setup refusal; compare its text to
   @@ROUND@@/receipts/control-c2-held-instrument-r82.txt.
3. Run each of the three new commands twice, 2 s apart, and report whether the output shape is
   stable (a row that flips shape is a defect this round must know).
4. Report the contract lines and exit statuses verbatim.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ExecC2Run.md."""),

    item("R82ExecMutants", "executor",
         """Independent mutation of the C1 instrument (read-only over the lane; all edits in your scratch).

1. `git -C @@LANE@@ show @@FREEZE@@:tools/mado-barfoot.py` into your scratch as `tool.py`, and run
   the C1 counter's own case set against it to confirm 47/47.
2. Write SIX of your own mutations of the new allocation code (not the counter's list): e.g. drop the
   zero guard, apply the allocation on the wrong axis, let the declaration override the allocation,
   accept a bool allocation, ignore the composition path, add the margin twice. Save each mutant and
   report how many of the 47 cases each one fails (a mutant failing 0 cases is a gap).
3. For each mutant, name the case that separates it, or say GAP with the code line that no case
   exercises.
4. Confirm the counter's own 34 mutants die by running the frozen command once and reading the
   `MADO_R82_MUTANT` lines.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ExecMutants.md."""),

    item("R82ScribeEntry", "scribe",
         """Draft the round-82 knowledge entry (prose; no code).

Create @@LANE@@/corpus/knowledge/bar-footprint-allocation-r82.md (the C1 ground) in the lane's note
style. It must carry, each with a file:line anchor from the pinned bytes:

1. Why a zero width/height is the client's size (S481: wlr-layer-shell `set_size`) and why the
   compositor's arranged box is therefore not the band.
2. gtk-layer-shell's auto zone read of `self->current_allocation.height` / `.width` (`:276`, `:282`)
   and the unanchored-margin addition — the client's own band.
3. The round-82 model: `--allocation` as a declared `{namespace: band}` input; `band_of`'s order
   (declaration first, allocation second, refusal for absent/zero); the arranged box and the zone
   both use it; the composition path resolves the bar's band the same way.
4. A decision table (≥6 rows) of class → input → modelled result or named refusal.
5. A limits section: what stays refused (per-axis dynamic extra surfaces, fractional scale, an
   allocation for an unknown namespace, a negative band) and what a caller could mis-declare.
6. A `## sources` block naming S481 (new) and S464/S470 (held) as `source:` ids.

Read @@LANE@@/.ufo/waves/round-79/fetch/S464.bin and @@LANE@@/.ufo/waves/round-80/fetch/S470.bin
yourself before writing; quote at most 25 words per quote and give the line. Do not edit SOURCES.md,
SCORECARD.md or any counter.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ScribeEntry.md."""),

    item("R82ScribeSources", "scribe",
         """Open the two new sources and pin them (read-only fetches; no registry append).

1. Fetch and pin, into @@ROUND@@/fetch/, with sha256 in @@ROUND@@/fetch/sha256-r82.txt:
   (a) `S481` — the wlr-layer-shell protocol XML at a pinned ref (try
   `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/<commit>/unstable/wlr-layer-shell-unstable-v1.xml`
   or the vendor copy in the pinned Hyprland tree at `@@BASE@@`); the quote is `set_size`'s
   width/height 0 clause, ≤25 words, with its line number.
   (b) `S482` — the `org.kde.StatusNotifierWatcher` interface: its bus name, object path,
   `RegisterStatusNotifierItem`/`RegisterStatusNotifierHost` methods and the
   `RegisteredStatusNotifierItems` property. Use a primary source (the KDE/freedesktop specification
   page or the `StatusNotifierWatcher.xml` interface file at a pinned ref).
2. Write the two registry rows in the lane's 11-column schema into
   @@ROUND@@/sources-rows-r82.md (id, title, url, kind, tier, why, locator, status `mined`,
   recheck date, used-by `corpus/knowledge/bar-footprint-allocation-r82.md` /
   `SKILL.md`, `source:` id). No cell may contain a literal or escaped pipe.
3. Record for each row: URL, access date 2026-11-04, sha256 of the fetched bytes, byte count, and the
   located quote with its line.
4. State what each source licenses and what it does NOT (e.g. a protocol clause is not a host
   observation). Do not append to corpus/SOURCES.md — the L1 does that after checking.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ScribeSources.md."""),

    item("R82ScribeLesson", "scribe",
         """Draft the round-82 lesson (prose; no code).

Create @@LANE@@/corpus/lessons/round-82.md with:

1. A header naming the round, the two claims and the freeze/base revisions.
2. `## Mistakes` — at least one mined mistake. Candidates this round, each with its evidence
   pointer: (a) the first `alloc-explicit-overridden` mutant survived because `band_of`'s
   declaration branch was dead code (the caller only called it when the axis was 0), so the
   resolver was made the single entry point — captured-by: nothing until the counter's kill count;
   (b) two mutant anchors drifted when that refactor landed (`alloc-axis-lost`,
   `alloc-composition-ignored` reported `reason=anchor-absent`) — captured-by: the counter's
   anchor-absent branch, but only after a full run. Pick the true one, name class · evidence ·
   captured-by · fix (shown able to fail).
3. A sweep for further mistakes: `grep -n 'TODO\\|FIXME\\|XXX' @@LANE@@/tools/mado-barfoot.py
   @@LANE@@/quality/counters/c*-r82-*.py` and a dead-key sweep over the two new control sets
   (every key read by the counter; print the keys no reader uses).
4. `## Gate` — the census at round start (2026-11-04, exit 0, 415 rows) and the two rows opened this
   round (S481, S482), each with URL, access date and ≤25-word located quote; plus one reject or a
   named refusal if there is one. The registry append is the L1's.
5. A short `## Next round` naming the next finite ground.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ScribeLesson.md."""),

    item("R82ReviewerC1", "reviewer",
         """Attack C1 (coverage — the client's own band). Read-only.

1. Re-derive, from the pinned bytes and your own arithmetic, the expected box/band of all eight
   `alloc-*` cases; report AGREE or DISAGREE per case with the line that decides it. Pay special
   attention to `alloc-dyn-height-margin` (does the band really add the unanchored margin and then
   the anchored one?) and `alloc-composition-dyn-bar` (does the level-3 panel really arrange at
   y=34?).
2. Look for a class the claim says is modelled but is not: try to construct an allocation input that
   the tool accepts but that a source contradicts (a zero band reviewed as a band, an allocation on
   a non-band axis, an allocation larger than the monitor, a namespace with two surfaces).
3. Check the counter's assertions: `CASES=47`, `CARRIED=39`, `MUTANTS=34`, `BASE_EXPECT=39`; and
   whether any of the eight new cases could pass on the held round-81 tool (they must not).
4. Name the strongest single objection to the claim, and whether it is fatal or a named limit.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ReviewerC1.md."""),

    item("R82ReviewerC2", "reviewer",
         """Attack C2 (operability — the tray plane in the runbook). Read-only.

1. For each of the three new rows, construct at least two outputs that SHOULD NOT match but a
   plausible wrong matcher would accept, and one that SHOULD match. Report whether the frozen
   negatives already cover them; name any false-green you find.
2. Check the row binding rule: each of the 29 rows is bound exactly once, the three new rows'
   command cells equal the cases' argv (`documented`), and the section rename did not silently
   orphan an old row.
3. Check the counters' constants (`CASES=29`, `CARRIED=26`, `SHAPES=24`, `MUTANTS=25`) and that
   `control_new=0/3` is a construction result, not an accident.
4. Name the strongest single objection, and whether it is fatal or a named limit.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82ReviewerC2.md."""),

    item("R82CriticClaims", "critic",
         """Falsify the round's claims as declared (read-only).

1. Read @@ROUND@@/claims-declaration-r82.md and the two counters. For each claim, answer: is the
   predicate in the code the same sentence as the declaration? Is the kill rule the declared one?
   Is the target reachable only with the claimed work (does the base control prove it)?
2. Attack the do-nothing control: describe the cheapest change that is not the claimed work and try
   it in your scratch copy (e.g. editing case expectations, or a tool change that special-cases the
   eight cases). If it reaches 47/47 without the resolver, the counter is wrong — say so.
3. Check causation separability: could C2 land with C1 absent, and vice versa?
4. Check the axis names: C1 names the surface it moves (a modelled class, not a number) and C2 names
   the surface (three runbook row classes), and no axis is harmed by the other's landing.
5. Verdict per claim: ADMIT or REJECT with the exact reason and the smallest fix.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82CriticClaims.md."""),

    item("R82MutRunbook", "mutation-tester",
         """Mutation-test the C2 instrument independently (read-only over the lane; edits in scratch).

1. Copy @@LANE@@/quality/counters/c2-r82-runbook.py into your scratch and write FIVE mutations of
   your own (not the 25 in the file): e.g. `regex` matched with `re.match` on the whole text, the
   `lines_shape` floor off by one, `array_fields` accepting a non-list, the refusal stage check
   accepting any stage, the row-binding check allowing a doubly bound row.
2. Run each mutant's `--selftest` and its full run at the freeze; report which cases it breaks and
   whether the frozen set separates it (a mutant that still prints `matched=29/29` is a gap).
3. For each mutant, name the case (or state GAP with the code line).
4. Report the 25 frozen mutants' kill count by running the frozen command once.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82MutRunbook.md."""),

    item("R82Sentinel", "sentinel",
         """Security review of the round's bytes (read-only).

1. Scan every file the round adds or changes for credential material, session identifiers, serial
   numbers, EDID strings, home-path leaks and tokens:
   `grep -rnE '(serial|description|EDID|token|secret|password|Bearer|api[_-]?key|/home/[a-z])'` over
   @@ROUND@@/ and the two new counters; report every hit with file:line and whether it is a field
   name, a redaction or a leak.
2. Check the three new commands are read-only (`busctl --user list`/`introspect` only read the bus;
   prove it from `busctl --help` or the man page and from the absence of any `call`/`set` verb).
3. Check the allocation parser's input handling: size limits (`MAX_BYTES`), type checks, refusal of a
   non-object, no path traversal (the file is a caller-supplied path, like `--config`), no shell.
4. Check the wave seats cannot reach the lane's git/jj state: list the paths and prompts that could
   lead a seat to commit, and confirm the context forbids it.
5. Verdict: `clean` with the checks named, or `defect` with file:line.

Write your report at @@LANE@@/.ufo/waves/round-82/w1/R82Sentinel.md."""),
]


def main():
    subs = {"@@LANE@@": LANE, "@@ROUND@@": ROUND, "@@FREEZE@@": FREEZE, "@@BASE@@": BASE,
            "@@SCRATCH@@": SCRATCH}
    items = []
    for entry in ITEMS:
        prompt = entry["prompt"]
        for key, value in subs.items():
            prompt = prompt.replace(key, value)
        items.append({"name": entry["name"], "role": entry["role"], "prompt": prompt})
    context = CONTEXT
    for key, value in subs.items():
        context = context.replace(key, value)
    spec = {"wave": "w1", "reportDir": ".ufo/waves/round-82/w1", "context": context,
            "items": items}
    out = os.path.join(ROUND, "w1-spec.json")
    with open(out, "w") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    roles = [i["role"] for i in items]
    print("wrote %s: %d items (%s)" % (out, len(items), ", ".join(roles)))


if __name__ == "__main__":
    main()
