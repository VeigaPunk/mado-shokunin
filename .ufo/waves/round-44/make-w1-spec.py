#!/usr/bin/env python3
"""Generates .ufo/waves/round-44/w1-spec.json (38 seats, v1 wave: build + first falsifiers).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
"""
import collections
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-44"
FREEZE = "e2289516a9a857f55cda7be635933e89b931c3da"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r44"
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls "
    "concurrently in large batches. Do not serialize what can run in "
    "parallel. Do not output philosophical reasoning or verbose plans. Act "
    "directly via tool calls.\n\n")

CONTEXT = """# Goal
mado round 44 (hyaku run 9, 2026-10-26), inline v1 wave w1 of two (38 seats: build + first falsifiers). Lane repo: %(L)s
Claims are FROZEN at %(W)s/registration.md (freeze commit %(F)s, base %(B)s) - read it first. Two claims:
- C1 operability: `tools/mado-geometry.py` (the round-43 read-only join of `windowrule = size W H, match:class RX` lines and one `hyprctl clients -j`
  dump: AGREE / DIFFER / TILED / BADSIZE) gains state verdicts: fsmode = the client's `fullscreen` value when a JSON integer 1 or 2 (not bool, not
  float), else 0; verdict order BADSIZE | FULLSCREEN (2) | MAXIMIZED (1) | TILED | AGREE | DIFFER; summary carries ` maximized=<n> fullscreen=<n>`
  before ` verdict=` exactly when their sum > 0, else the round-43 line is byte-identical. Why: Hyprland 0.56.2 sets a maximized window's box to the
  work area and a fullscreen window's box to the monitor box (pins %(W)s/fetch-c1/: Hyprland-FullscreenHandler.cpp setTargetSizeAndPosition,
  Hyprland-FullscreenController.hpp eFullscreenMode, Hyprland-HyprCtl.cpp `fullscreen` = `.internal`), so the round-43 tool reports a fullscreen
  gkeep window DIFFER (false). Frozen counter %(L)s/quality/counters/c1-r44-geometry-states.py (PRED-C1-r44; its docstring is the contract
  extension; it imports quality/counters/c1-r42-geometry.py, whose docstring is the rest of the contract): target fixtures=26/26 TARGET_MET; base
  12-13/26 MISSED. Reference control (NOT yet installed): %(W)s/c1/ctl-ref-tool.py.txt (26/26 MET, selftest 91/91, round-43 counter still 37/37).
  Controls %(W)s/ctl/run-c1-controls.py -> %(W)s/receipts/ctl-c1.txt: 0 of 15 non-reference runs MET.
  Score any tool file: `cd %(L)s && python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev %(F)s --tool <file> --work %(S)s/<YourSeatName>`
- C2 coverage (sourced; assimilation of the gkeep residue of the shokuknow package): a new entry corpus/knowledge/hyprland-gkeep-size-request-r44.md -
  what happens after Hyprland sets the gkeep window's box: CWindow::sendWindowSize -> realToReportSize -> xdg toplevel setSize -> scheduleConfigure,
  the pending-size-ack list and onAck (Window.cpp), the X11 configure branch, what xdg-shell 1.49 says a client may do with a configure size, what
  GTK 4.24.1's Wayland toplevel does with it, and what gkeep 133b867 declares (set_default_size(420, 500), no set_size_request). Frozen counter
  %(L)s/quality/counters/c2-r44-gkeep-size-request.py (PRED-C2-r44 = PRED-C2-r43-v2 with round-44 constants and a rebuilt clause h: the entry
  carries `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and
  `hyprland sendWindowSize xdg_setSize=1 x11_configure=1`, recomputed from the pins). Target admitted=1/1; base 0/1. Controls
  %(W)s/ctl/run-c2-controls.py -> receipts/ctl-c2.txt: 0 of 3 do-nothing controls admitted; NO positive control exists yet.
  `cd %(L)s && python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <repo> --rev <rev> --base %(B)s`
Pins (fetched by the L1 2026-10-26; each seat re-opens what it relies on; sha256 in %(W)s/receipts/fetch-sha256.txt) in %(W)s/fetch/:
  Hyprland-Window.cpp (= held row S164's exact URL, raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp),
  Hyprland-XDGShell.cpp (same commit, src/protocols/XDGShell.cpp), xdg-shell.xml (gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml),
  gdktoplevel-wayland.c (gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c), gkeep-ui.py (raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py,
  full file; held S297 is only its lines 446-488 as own-work). Provisional ids: S164 held (Window.cpp), S298 XDGShell.cpp, S299 xdg-shell.xml, S300 gdktoplevel-wayland.c,
  S301 gkeep-ui.py. The registry tops at S297 (234 rows); new rows are append-only, 11 columns, status `mined`, opened 2026-10-26. Host: Hyprland 0.56.2-4,
  gtk4 1:4.24.1-1, wayland-protocols 1.49-1.
Package (READ-ONLY; read bytes, never run a campaign tool there): %(P)s; residue files under knowledge/corpus/knowledge/: gkeep-client-size-request-r12.md
  (the predecessor: staged S311 Window.cpp at tag v0.56.2 -> held S164 by document; staged S312 gkeep ui.py -> new row), gkeep-rendered-geometry-chain-r9.md
  (fetchClass), gkeep-rendered-geometry-record-r13.md, -r14.md, gkeep-geometry-never-recorded-r15.md (journal route), gkeep-element-rules-r30.md,
  glyph-and-geometry-r31.md, gkeep-geometry-unobservable-r8.md, gkeep-size-rule-application-r10.md, gkeep-observation-route-r11.md; gkeep-size-to-real-size-r11.md
  was admitted in round 43 (corpus/knowledge/hyprland-gkeep-geometry-r43.md) and may not be admitted again. Id guard and quarantine slice: %(W)s/assimilation/.
Round-43 closure routed defects (%(L)s/corpus/lessons/round-43-verifier-spotcheck.md section 6): D1 lesson r10-refusal reason under-cites S294/S158 and S310 maps
  to S295/S296/S297; D2 S293 title echoes the refuted premise (supersede with the other w2 row-cell defects); D3 SKILL.md TILED licence wrong for pseudo-tiled
  clients; D4 entry cites w1/ExecOracleGkeep files absent at the data commit, receipt cites gkeep-shm.c:156-164 (true 150-159); D5 registration seat count 37
  (38 ran), SCORECARD says M43-1..8 (lesson has M43-9); D6 open predicate defects; D7 no committed axis receipt at the tip.
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin outside the lane), sibling lanes, templates/, scripts/,
  MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout, ~/Projects/gkeep, or the lane's jj/git index. Never run mutating
  git/jj anywhere in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git (log/show/diff/status/rev-parse/ls-tree/cat-file) is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus any explicit destination your task names. Never edit an existing
  tracked file (counters, controls, registration, reference, pins are FROZEN); the L1 is the only integrator. Write your Report file FIRST (a short
  status), then refine it; a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>.
- SCRATCH (operator directive 2026-10-25): every clone, venv, build, fixture and counter work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it
  explicitly as TMPDIR/--work/dir=, never rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB; copy receipts into your
  seat dir first, then delete your scratch dir before you finish (`trap 'rm -rf -- "$S"' EXIT`). The reaper deletes idle scratch after 45 min, so a
  /tmp or scratch path is never citable evidence: cite only files in your seat dir. A tree you leave on disk is your own reported defect.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input injection,
  no Wayland-client connection of your own on the host session. Allowed compositor reads: `hyprctl version`, `hyprctl clients -j`, `hyprctl monitors -j`,
  `hyprctl workspaces -j`, `hyprctl getoption <name> -j`; NEVER `dispatch`, `keyword`, `reload`, `setprop`, `--batch`, `output`, `plugin`, `kill`.
  Host config trees and binaries are READ-ONLY.
- Git fixtures (run-6 incident): any fixture repo is `D=$(mktemp -d -p %(S)s/<YourSeatName>)` then `git -C "$D" init -q` (or `git clone -q --shared <lane> "$D"`),
  every later git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the first commit; never `git commit` with a
  throwaway identity anywhere else.
- Tooling authorization (operator, 2026-10-19): you may install tools that help the task (read /home/vgpnk/.omp/agent/RULES.md first; official channels only:
  uv tool / uv pip into a scratch venv / npx / official binaries in ~/.local/bin). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions
  are PAUSED host-wide until the operator resolves the host-recovery L0 question; never -Sy, -Syu, -U, -R, a downgrade, or a restart of a host service.
  Record tool/version/channel/reason in your report.
- Seat tool state: your tools start at the fleet root, not the lane: use absolute paths everywhere.
- You are a leaf: no subagent dispatch, no background jobs, no spawning (an executor MAY spawn one read-only labrat probe).
- Every finding names what it attacks or supports (a path:line, a command and its output, or a hash). Never fabricate: an unrun check has not passed.
  Quotes lifted from a source are <= 25 words, located (file:line), and verified by a script that greps your receipt; locators are computed (grep -n), never typed.
"""


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(F)s", FREEZE), ("%(B)s", BASE),
                 ("%(P)s", PKG), ("%(S)s", SCR)):
        t = t.replace(k, v)
    return t.replace("%%", "%")


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({
        "name": name, "role": role,
        "prompt": sub(GODSPEED + "# Target\n" + target.strip() +
                      "\n# Task\n" + task.strip() + "\n")})


SCORE1 = ("cd %(L)s && python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev %(F)s "
          "--tool <your file> --work %(S)s/<YourSeatName>")
SCORE2 = "cd %(L)s && python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <your fixture repo> --rev HEAD --base %(B)s"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"

# ------------------------------------------------------------ executors (12)
seat("ExecIndepA", "executor",
     "Differential implementation of C1's contract extension (from the counter text only).",
     """WITHOUT reading %(W)s/c1/ctl-ref-tool.py.txt, copy %(L)s/tools/mado-geometry.py (the round-43 tool) to %(W)s/w1/ExecIndepA/mado-geometry.py and extend
it from the docstring of %(L)s/quality/counters/c1-r44-geometry-states.py alone (stdlib only; add selftest cases so k==n>=80; the state logic must have
teeth). Score it: `""" + SCORE1 + """`. Report every failing fixture/clause verbatim (a failure is a finding about the contract text or counter unless you
show your file is wrong). Then list the contract sentences you needed to read twice, both readings, and the fixture that decides (or none = a hole).""")
seat("ExecIndepB", "executor",
     "Second differential implementation of C1's extension (table-driven style).",
     """WITHOUT reading %(W)s/c1/ctl-ref-tool.py.txt, start from %(L)s/tools/mado-geometry.py and implement the extension of
%(L)s/quality/counters/c1-r44-geometry-states.py's docstring with a verdict TABLE (an ordered list of (predicate, verdict) pairs) instead of if/elif, and
the summary suffix built from a dict. Selftest k==n>=80. Score it: `""" + SCORE1 + """`. Then differential-fuzz it against the counter's model
(import the counter with importlib.util; use model_out_states, gen_state_clients and the round-42 gen_texts; never call main) on >= 2000 cases plus 200
adversarial ones of your own (fullscreen as huge ints, nested objects, duplicate keys) and list every disagreement with a minimised input. Seat dir %(W)s/w1/ExecIndepB/.""")
seat("ExecC1ExtraMutants", "executor",
     "Mutation population for C1: single-defect mutants of the reference's state logic beyond the 13 registered variants.",
     """Read %(W)s/ctl/run-c1-controls.py and %(W)s/c1/ctl-ref-tool.py.txt. Build >= 30 NEW single-defect mutants concentrated on client_fsmode, evaluate and
report (and the docstring-free code only): boundary values (f in (1,2,3)), `not isinstance(f, bool)` dropped, `>= 0` vs `> 0` on the suffix, suffix position,
counts swapped, matched-count changes, unmapped fullscreen counted, MAXIMIZED counted as tiled, etc. - each a text replacement asserted to match exactly once.
Score each with `""" + SCORE1 + """` and write %(W)s/w1/ExecC1ExtraMutants/survivors.md (`mutant | edit | verdict | failing fixtures/clauses`). For every
survivor: EQUIVALENT (with proof) or MISSING CHECK (the fixture input and expected output that kills it). Save the mutant files in your seat dir.""")
seat("ExecC2Positive", "executor",
     "Build the missing C2 positive control: a complete, honest admitted fixture from the pins (proves the target is reachable and gives w1 a base for forgeries).",
     """In a fixture clone (`D=$(mktemp -d -p %(S)s/ExecC2Positive); git clone -q --shared %(L)s "$D"`; `git -C "$D" checkout -q --detach %(F)s`; verify toplevel), write a
minimal but TRUE entry at """ + ENTRY + """ citing S164, S298, S299, S300, S301 (header in the first 20 lines: `source:` lines, `verified-at: 2026-10-26`,
`recheck: 30d`), one claim line per id with its quote and computed `<receipt name>:<line>` locator, the two census lines; registry rows S298-S301 (11 cells,
mined, opened 2026-10-26, used-by the entry; S164's used-by extended, cells 1-9 byte-equal); corpus/lessons/round-44.md `## Gate` with one GATE line per id
(sha256 of the pin, quote) plus `ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as """ + ENTRY + """` and one REFUSE line with a flip
word; a README index row. Commit inside "$D" only and score: `""" + SCORE2 + """`. Iterate until admitted=1/1, recording every clause failure you hit and
whether it was your error or a counter defect. Save the fixture's changed files (git -C "$D" diff --stat, and the files themselves) to %(W)s/w1/ExecC2Positive/positive/
and write a script %(W)s/w1/ExecC2Positive/make-positive.sh that rebuilds the commit from those files at %(F)s (the L1 commits it as control P).""")
seat("ExecC2ExtraMutants", "executor",
     "Mutation population for C2: clause mutants of a positive fixture.",
     """Build your own positive fixture exactly as described for an admitted PRED-C2-r44 entry (read the counter docstring %(L)s/quality/counters/c2-r44-gkeep-size-request.py;
fixture clone `D=$(mktemp -d -p %(S)s/ExecC2ExtraMutants)` from %(L)s at %(F)s with `-C "$D"` on every git call), reach admitted=1/1 with `""" + SCORE2 + """`, then build >= 30
single-defect mutants of it (header window, `source:` outside the window, a ghost S### token, row cell edits, used-by missing, S164 cells 1-9 changed, Gate sha wrong,
quote in a comment, quote occurring twice, locator off by one, census numbers changed, census line inside a fence, census line duplicated, README row missing or doubled,
ADMIT of gkeep-size-to-real-size-r11.md, REFUSE without flip word, a pin not cited). Each must score 0/1; write %(W)s/w1/ExecC2ExtraMutants/survivors.md with every
mutant the counter still admits and the clause that should have killed it.""")
seat("ExecLiveHost", "executor",
     "Host receipt for C1: the reference tool on the running desktop and on state fixtures.",
     """Copy %(W)s/c1/ctl-ref-tool.py.txt to %(W)s/w1/ExecLiveHost/mado-geometry.py. Run `hyprctl clients -j | python3 -I mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf`
(expect NO_MATCHING_CLIENT rc 3 while no gkeep window is open) and record which `fullscreen`/`fullscreenClient` values the live dump carries for every client
(`hyprctl clients -j | python3 -c ...`), plus `hyprctl monitors -j` (size, reserved) and `hyprctl workspaces -j` for the active workspace. Then a hand-made dump with a
floating `org.omarchy.gkeep` client at the active monitor's full size and `fullscreen: 2`, one at the work-area size (monitor minus reserved) with `fullscreen: 1`, and
the same two with the round-43 tool (`git -C %(L)s show %(B)s:tools/mado-geometry.py`) to show the before/after verdicts. Save verbatim outputs, exit codes, tool
sha256s and `hyprctl version` to %(W)s/w1/ExecLiveHost/live-states.txt (reported, not scored). Read-only verbs only.""")
seat("ExecSrcHyprland", "executor",
     "Located-quote fact table for the compositor side of C2 (Window.cpp, XDGShell.cpp).",
     """From %(W)s/fetch/Hyprland-Window.cpp and Hyprland-XDGShell.cpp extract, each as `claim | <= 25-word quote | file:line (grep -n) | sha256`: realToReportSize for
a Wayland client (goal clamped); sendWindowSize's early return when the pending reported size is unchanged; the xdg branch emplacing (serial, size) into
m_pendingSizeAcks; the X11 configure branch; onAck picking the newest serial <= the acked one and writing ackedSize into the surface's pending state; where
sendWindowSize is called (grep every call site, name its function); CXDGToplevelResource::setSize -> scheduleStateApplication -> scheduleConfigure; where the
configure with the size is actually sent (sendConfigure with m_pendingApply.size); what Hyprland does when the client commits a different size (search for
ackedSize use, `reportedSize`, `m_realSize` updates on commit). State plainly what the sources do NOT say. Verify every quote by a grep printed in your report.
Write %(W)s/w1/ExecSrcHyprland/facts.md.""")
seat("ExecSrcClient", "executor",
     "Located-quote fact table for the client side of C2 (xdg-shell 1.49, GTK 4.24.1, gkeep).",
     """From %(W)s/fetch/xdg-shell.xml: the xdg_toplevel.configure description (width/height are a hint? 0 means the client decides? which states make the size a
maximum or exact), xdg_surface.ack_configure; from %(W)s/fetch/gdktoplevel-wayland.c: the configure handler storing the pending width/height, how a non-zero
configure size is applied to a floating (non-maximized, non-fullscreen, non-tiled) toplevel, how the default size is used when the compositor sends 0x0, and
min-size constraints (search for `min`, `geometry`, `default`); from %(W)s/fetch/gkeep-ui.py: application_id, set_default_size, the absence of set_size_request
(grep -c), any CSS min-width/min-height and which selector it sits under. Each: claim | <= 25-word quote | file:line | sha256; every quote verified by grep.
Add what the sources do NOT establish (e.g. that GTK honours a hint larger than its natural size). Write %(W)s/w1/ExecSrcClient/facts.md.""")
seat("ExecHarmBase", "executor",
     "Harm-check baseline at base, on a clone, for the round's no-harm comparison.",
     """On a fresh clone of the base (`D=$(mktemp -d -p %(S)s/ExecHarmBase); git clone -q --shared %(L)s "$D"`; verify toplevel; `git -C "$D" checkout -q --detach %(B)s`
only inside it) capture to %(W)s/w1/ExecHarmBase/harm-base.txt: every `tools/*.py` and `tools/*.sh` selftest the tools offer (read each usage line; python3 -I),
`python3 -I quality/check-index.py --rev %(B)s --repo .`, `python3 -I quality/check-index-rows.py` (read its usage), `python3 -I quality/check-axis-scores.py --rev %(B)s --repo .`,
`python3 -I quality/check-locators.py --selftest`, and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.
Record tools count, knowledge count, registry rows (`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md`), QUALITY's last criterion
number. Compare with %(L)s/.ufo/waves/round-43/w2/ExecHarmTip/harm.txt if present and state every difference. Delete the clone.""")
seat("ExecFsSemantics", "executor",
     "Ground C1's premise in source: what `clients -j` size is for a maximized or fullscreen window, and which `fullscreen` values occur.",
     """From the pins in %(W)s/fetch-c1/ and any further Hyprland efb50993 file you open and pin (raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>;
save under %(W)s/w1/ExecFsSemantics/pins/ with sha256): (1) can `.internal` be anything but 0, 1, 2 (enum, casts, combined modes FSMODE_MAX?); (2) after
setTargetSizeAndPosition, does the window's GEOMETRIC_GOAL size become the monitor box / work area (follow setPositionGlobal into the target and the window's
m_realSize); (3) is the floating flag kept while fullscreen (so the round-43 tool says DIFFER, not TILED); (4) what happens to the rule's box on exit
(rememberFloatingSize / restore); (5) any state where internal is 1 or 2 but the box is NOT replaced (e.g. a fullscreen window on a hidden workspace, a group).
Each claim: <= 25-word quote with a computed file:line. Verdict: does the evidence support FULLSCREEN/MAXIMIZED as "the reported size says nothing about the rule"?
Write %(W)s/w1/ExecFsSemantics/finding.md.""")
seat("ExecLocatorTeeth", "executor",
     "Frontier-step fix for closure D6: quality/check-locators.py compares identifiers, not numbers, and 12 of 37 of its mutants survive its selftest.",
     """Read %(L)s/quality/check-locators.py, %(L)s/.ufo/waves/round-43/w2/CritLocatorGate.md and MutCheckLocators.md (and their seat dirs). Write a candidate
successor %(W)s/w1/ExecLocatorTeeth/check-locators.py (same CLI and output lines) whose selftest kills the surviving mutants (re-run the MutCheckLocators mutation
set against it: before/after kill counts) and which also fails when a numeric literal in a backticked fragment is absent from the cited range. Show it CAN FAIL:
a red-before run on a prose line the old checker passes (commit the input and the observed failure text to your seat dir), then green on the corrected line.
Run both checkers over %(L)s/LOG.md and %(L)s/corpus/knowledge/hyprland-gkeep-geometry-r43.md with `--fetch %(L)s/.ufo/waves/round-43/fetch` and report the diff.""")
seat("ExecDomainMetaRatio", "executor",
     "considerthese 2026-10-25 proposal 1: a running domain-versus-meta ratio, as a re-runnable count.",
     """Read %(L)s/considerthese/2026-10-25.md proposal 1 (never edit it) and open what it points at. Define, from committed lane bytes only, which claims are
domain (a tool, a knowledge entry, a SKILL table about the desktop) and which are meta (calibration, counters, process): classify every claim row of the
SCORECARD Round sections 34-43 (`grep -n '^| C[0-9]' %(L)s/SCORECARD.md` and the round headings) with a rule you state BEFORE classifying, write
%(W)s/w1/ExecDomainMetaRatio/ratio.py (stdlib, read-only, `--repo --rev --from --to`, prints `round | claim | axis | class` and `DOMAIN_META: domain=<d> meta=<m> window=<a>-<b>`),
run it for rounds 34-43 and 39-43, and paste outputs. Show the classifier CAN FAIL: one hand-labelled row where your rule disagrees with your own reading, and
what you changed or why not. Draft a QUALITY.md criterion (next free number) citing considerthese/2026-10-25.md proposal 1 and corpus/lessons/round-44.md, with the
command a closure can re-run. Write %(W)s/w1/ExecDomainMetaRatio/proposal.md.""")

# ------------------------------------------------------------ scribes (8)
ENTRY_SHAPE = """Entry shape (follow %(L)s/corpus/knowledge/hyprland-gkeep-geometry-r43.md and the counter docstring %(L)s/quality/counters/c2-r44-gkeep-size-request.py):
title; `Lane: mado-shokunin. Round: 44.`; within the FIRST 20 raw lines `source: S### - <title> - <anchor>` for S164, S298, S299, S300, S301, exactly one
`verified-at: 2026-10-26`, exactly one `recheck: 30d` (or ISO date/on-release); no other source:/verified-at:/recheck: line. Body: each cited id has ONE claim
line naming only that id, carrying its Gate quote verbatim (3-25 words, word-bounded, outside comments, unique across the five receipts) and the computed locator
`<receipt file name>:<line>`; tag claims OBS/INF/UNK; a decision table `question | where the answer lives | state`; the two census lines verbatim on lines
of their own outside fences: `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and
`hyprland sendWindowSize xdg_setSize=1 x11_configure=1`. No S### token other than the cited ids (refer to held S291/S293/S294 knowledge by entry path, not id).
Never claim a gkeep window was observed; the live state is UNK. Mark what supersedes or amends the staged r12 (its "settled"/"complete" wording is not adopted)."""
seat("ScrEntryA", "scribe",
     "Draft the C2 entry - chain-first structure.",
     ENTRY_SHAPE + """
Structure: (1) where round 43 stopped (the goal box), (2) report size, (3) the configure and its serial, (4) the ack, (5) what the protocol lets the client do,
(6) what GTK does, (7) what gkeep asks for, (8) what is and is not observed. Re-open every receipt you quote and verify each quote and locator with a script
(print it). Write %(W)s/w1/ScrEntryA/hyprland-gkeep-size-request-r44.md and quotes.tsv (id, quote, file, line, sha256).""")
seat("ScrEntryB", "scribe",
     "Draft the C2 entry - decision-table-first structure.",
     ENTRY_SHAPE + """
Structure: open with the decision table (what a reader can conclude about the size gkeep renders from the configure alone, from the ack, from the client's
own declarations - and what each does NOT license), then short evidence paragraphs, then the census lines. Under 90 lines. Verify every quote/locator with a
script. Write %(W)s/w1/ScrEntryB/hyprland-gkeep-size-request-r44.md and quotes.tsv.""")
seat("ScrRowsDraft", "scribe",
     "Draft registry rows S298-S301 and the held S164 used-by change.",
     """Read %(L)s/corpus/SOURCES.md (Registry shape; rows S290-S297 as exemplars) and /home/vgpnk/Projects/shokunin/CORPUS.md (SOURCES contract). Draft 11-column rows for
XDGShell.cpp (S298), xdg-shell.xml (S299), gdktoplevel-wayland.c (S300), gkeep ui.py full file (S301; kind code, tier A, location the raw GitHub URL): anchor =
file + line ranges (computed) + tag/commit; teaches = one grounded benefit that does NOT overstate (round-43 w2 found S290-S294 cells echoing refuted premises
- avoid that); status mined; opened 2026-10-26; recheck on-release or an ISO date; used-by """ + ENTRY + """; no `|` in any cell; the location's last path
component and the receipt file name contain one another. curl each URL and compare sha256 with %(W)s/receipts/fetch-sha256.txt. grep the registry for each
URL (duplicate within scope = census E04). Draft the S164 row with used-by extended (cells 1-9 byte-equal). Mirror-validate: copy %(L)s/corpus to
%(S)s/ScrRowsDraft/validate/corpus, append, run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` (exit 0
required; paste output). Write %(W)s/w1/ScrRowsDraft/rows-block.txt and rows.md.""")
seat("ScrLessonSkeleton", "scribe",
     "Draft corpus/lessons/round-44.md: Gate, assimilation ledger, Mistakes, round-43 errata.",
     """Read %(L)s/corpus/lessons/round-43.md and round-43-verifier-spotcheck.md for the shape, and the Gate grammar in the counter docstring
(`GATE <id> receipt=<path> sha256=<64 hex> quote="<q>"` in column 0 under `## Gate`; `ADMIT <staged path> as <entry>`; `REFUSE <staged path> reason=<>= 4
distinct words, with a flip word>`). Draft: `## Gate` (GATE lines for S164, S298-S301 - quotes 3-25 words, word-bounded, outside comments, unique across the five
pins; URL and access date 2026-10-26 per new row), the assimilation ledger (one row per residue file: decision, reason, flip), the old->new log for S164 used-by;
`## Mistakes` rows (class . evidence . captured-by . fix) for the round-43 closure's D1-D7 and for this round's C1 finding (the round-43 tool reports a fullscreen
window as DIFFER: captured-by none?); `## Round-43 errata` appending D1's corrections (S294/S158 links; S310 -> S295/S296/S297) and D5 (37 vs 38 seats; M43-1..9).
Mark every value the L1 must fill with `<<L1>>`. Write %(W)s/w1/ScrLessonSkeleton/round-44-lesson.md.""")
seat("ScrSkillProvince", "scribe",
     "Draft the SKILL.md / PROVINCE.md / README rows for C1 and C2, and the D3 correction.",
     """Read %(L)s/SKILL.md (the 'Rule size versus reported size' subsection and its licence table, the TILED row at ~line 276), PROVINCE.md (the
mado-geometry tool row) and corpus/README.md (index rows, all columns; `## Frontier`). Draft exact insertion text with neighbouring line numbers: two licence rows
(FULLSCREEN, MAXIMIZED: what each licenses and does NOT license), an appended correction note for the TILED row (pseudo-tiled clients: size from the stored
pseudo size; `clients -j` carries no pseudo field) - append, never rewrite; a PROVINCE row update (append); a README index row for
knowledge/hyprland-gkeep-size-request-r44.md with every cell the index requires (run `python3 -I %(L)s/quality/check-index-rows.py` on a scratch copy: errors=0),
and a Frontier bullet advance. Write %(W)s/w1/ScrSkillProvince/{skill-rows.md,province-row.md,readme-row.md}.""")
seat("ScrQualityCriteria", "scribe",
     "Draft QUALITY.md criteria 82+ from this round's mistakes.",
     """Read the tail of %(L)s/corpus/QUALITY.md (criteria 70-81 for the form) and the round-43 closure section 6. Draft criteria only where a mistake stands
behind them: (a) a tool's verdict vocabulary is checked against every state field the input carries (the round-43 tool ignored `fullscreen`; evidence:
%(W)s/fetch-c1/Hyprland-HyprCtl.cpp `fullscreen` field and %(W)s/receipts/ctl-c1.txt BASE-tool line); (b) a cited receipt exists at the commit that cites it
(D4); (c) a report's axis line points at a committed receipt at the tip (D7); (d) any other you can ground. Each: rule, mistake class, evidence pointer
(path:line or command), the control that shows it can fail. Say which you refuse for lack of a mistake. Write %(W)s/w1/ScrQualityCriteria/criteria.md.""")
seat("ScrSupersedeRows", "scribe",
     "Closure D2: superseding rows for the S290-S297 registry cells round-43 w2 found imprecise.",
     """Read %(L)s/.ufo/waves/round-43/w2/ScoutRowsA.md, ScoutRowsB.md, ScoutRowsC.md (and ScoutRowsD if present), the round-43 closure D2, CORPUS.md rule 2 (a
correction is a new row whose `teaches` opens `supersedes S0NN -`) and the census rules (a duplicate URL within one scope is fatal E04; across scopes W04).
Draft superseding rows (S302+ provisional) for the cells that are wrong (at least S293's title), with the corrected cell text grounded in the round-43 pins
(%(L)s/.ufo/waves/round-43/fetch/; computed locators). Decide per row whether supersession is possible without an E04 (scope wording) and mirror-validate in
%(S)s/ScrSupersedeRows/ with `sources-census.sh validate --file` (paste output). If supersession cannot pass the census, say so and draft the honest
alternative (lesson erratum). Write %(W)s/w1/ScrSupersedeRows/rows.md and rows-block.txt.""")
seat("ScrRecords", "scribe",
     "Draft the SCORECARD Round 44 section and the LOG.md Round 44 entry skeleton.",
     """Read the SCORECARD.md Round 43 section (~line 2529 to end) and LOG.md's Round 43 entry for shape. Draft for round 44: the claim table (C1 operability,
C2 coverage; before from %(W)s/receipts/c1-before-base.txt and c2-before-base.txt, after `<<L1>>`), the capabilities table update for 'rule size versus reported
size join' (state verdicts; first-working stays 43, the row is extended, or a new row - argue which is honest per /home/vgpnk/Projects/shokunin/AXES.md
Capabilities), Sources/saturation/planned (round 45 intent), and the LOG bullets (one per landed change, `<<L1>>` hashes). Also fix-forward D5 (SCORECARD says
M43-1..8) as an appended erratum line. Write %(W)s/w1/ScrRecords/{scorecard.md,log.md}.""")

# ------------------------------------------------------------ scouts (3)
seat("ScoutStagedResidue", "scout",
     "Planning data-walk (the L1's planner seat): the gkeep residue files against the pins and the lane.",
     """Read %(P)s/knowledge/corpus/knowledge/{gkeep-client-size-request-r12,gkeep-rendered-geometry-chain-r9,gkeep-rendered-geometry-record-r13,gkeep-rendered-geometry-record-r14,gkeep-geometry-never-recorded-r15,gkeep-element-rules-r30,glyph-and-geometry-r31}.md,
%(P)s/MERGE-REPORT.md, the rows they cite in %(P)s/SOURCES.append.md, %(L)s/corpus/lessons/round-43.md (assimilation ledger) and PROVINCE.md. For each file: claims, which
the five pins can re-ground (grep the staged quotes in %(W)s/fetch/), which rest on private `lanes/mado/roundN` receipts or unpinned sources, PROVINCE fit, overlap with
corpus/knowledge/hyprland-gkeep-geometry-r43.md. Recommend the admit (r12 predecessor?) and refusals with reason + flip; flag claims in r12 the pins refute or do not
support (e.g. 'a GTK4 window with no minimum-size request will adopt the size the compositor configures'). Write %(W)s/w1/ScoutStagedResidue/survey.md.""")
seat("ScoutCoverage", "scout",
     "Coverage-map ground for C1 and C2 in corpus/README.md, PROVINCE.md and SKILL.md.",
     """With grep commands and outputs, determine whether the lane held at base %(B)s: the configure/ack path, xdg-shell configure semantics, GTK default-size
behaviour, gkeep's client declarations, Hyprland fullscreen/maximized geometry (`git grep -ciE '...' %(B)s -- corpus/knowledge PROVINCE.md SKILL.md tools`). Name
the coverage-map row(s) and Frontier bullet(s) each claim moves and the honest expansion-credit sentence (new ground vs deepening of hyprland-gkeep-geometry-r43.md /
wayland-* entries). Flag adjacency with siblings' provinces. Write %(W)s/w1/ScoutCoverage/coverage.md.""")
seat("ScoutQuarantine", "scout",
     "Quarantine slice for mado (item 10): re-derive and verdict the 13 rows.",
     """Re-derive the slice (read-only): `awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
and compare with %(W)s/assimilation/quarantine-slice. For every row: does any residue file (r9, r12, r13, r14, r15, r30, r31) cite it? For those, fetch the cited
source and locate the quote (absent -> refuse, fabrication class; present -> adopt anchor; prose class cell -> unverifiable). Compare with round 43's verdicts
(%(L)s/.ufo/waves/round-43/assimilation/quarantine-verdicts.md). Write %(W)s/w1/ScoutQuarantine/verdicts.md (id, class, URL, evidence, verdict). Never edit the register.""")

# ------------------------------------------------------------ connectors (3)
seat("ConnSiblingOverlap", "connector",
     "Sibling-overlap scan for both claims.",
     """Scan read-only the other lanes' PROVINCE.md, corpus/README.md and knowledge under /home/vgpnk/Projects/shokunin/*-shokunin/
(`grep -rli 'fullscreen\\|maximiz\\|xdg_toplevel\\|configure\\|set_default_size\\|gtk4\\|gkeep' */corpus/knowledge */tools */SKILL.md`) for holdings that overlap C1
(fullscreen/maximized geometry verdicts) or C2 (the configure/ack path, GTK sizing, gkeep). Report overlaps, contradictions, which lane would arbitrate,
and what mado may claim about gkeep (operator's project). Write %(W)s/w1/ConnSiblingOverlap/overlap.md.""")
seat("ConnCrossClaim", "connector",
     "Cross-claim and cross-source patterns between C1 and C2; separability.",
     """Build a claims-vs-sources matrix: C1's contract sentences against fetch-c1 pins, C2's planned claims against fetch pins. Find (1) a fact both rest on
(e.g. the goal size is what `clients -j` prints AND what sendWindowSize reports) - consistent both ways? (2) a contradiction; (3) does C1's FULLSCREEN verdict
need a C2 fact or vice versa; (4) separability by reading both counters: C1's counter reads no knowledge file, C2's counter runs no tool - show it with
grep/strace-free reading and one run each (C1 with the reference via --tool; C2 on the base). Write %(W)s/w1/ConnCrossClaim/cross.md.""")
seat("ConnStagedVsRegistry", "connector",
     "Staged rows versus lane registry for the residue.",
     """For the rows the residue files cite (%(P)s/SOURCES.append.md and their `source:` lines), compare with %(L)s/corpus/SOURCES.md: URLs the lane holds (S164 for
Window.cpp; S297 excerpt vs full ui.py), different anchor/tag forms (tag v0.56.2 vs commit efb5099), tier C/community rows, private receipts, and the
duplicate-URL warnings new rows would add. Check %(W)s/assimilation/renumber-map.tsv and say whether every mapping is by document. Write
%(W)s/w1/ConnStagedVsRegistry/matrix.md with per-row verdicts and grep outputs.""")

# ------------------------------------------------------------ reviewers (3)
seat("RevC1Counter", "reviewer",
     "Attack C1's frozen counter c1-r44-geometry-states.py.",
     """Review %(L)s/quality/counters/c1-r44-geometry-states.py line by line against its docstring and the round-42 counter it imports. Hunt: lattice cases that never
reach a matched fullscreen client (count over 50 nonces), fixed fixtures that are vacuous, the b4 site selection (can a correct tool fail it? can a wrong tool
pass it?), the regress clause (does it really run on the same bytes; nonce handling; timeouts), model-vs-docstring disagreements (re-derive the model from the
docstring and diff on 2000 sampled cases), importlib monkeypatching side effects (old.model_out replaced: does the regress subprocess use the ORIGINAL model?),
scratch handling (`--work`, TMPDIR, cleanup). Each finding: severity, line, reproduction. Write %(W)s/w1/RevC1Counter/findings.md. Do NOT edit the counter.""")
seat("RevC2Counter", "reviewer",
     "Attack C2's frozen counter c2-r44-gkeep-size-request.py.",
     """Diff %(L)s/quality/counters/c2-r44-gkeep-size-request.py against c2-r43-gkeep-entry-v2.py and classify every changed line (constant / clause h / docstring).
Attack clause h: comment stripping of the gkeep pin (a `set_size_request(` inside a string or docstring?), the sendWindowSize body bound (first line exactly `}`),
gates lookup by basename, whether census lines can be satisfied without citing the receipts, the entry_lines filter (lines starting with `gkeep client `/`hyprland
sendWindowSize ` are excluded from clause g - can a claim line hide there?). Re-check clauses c-e for held S164 (a held id with a pinned receipt: can a forged
receipt be substituted?). Each finding: severity, line, a fixture that scores 1/1 wrongly (scratch repo under %(S)s/RevC2Counter with -C "$D"). Write
%(W)s/w1/RevC2Counter/findings.md. Do NOT edit the counter.""")
seat("RevRefTool", "reviewer",
     "Review the C1 reference: diff, docstring truth, robustness.",
     """`diff <(git -C %(L)s show %(B)s:tools/mado-geometry.py) %(W)s/c1/ctl-ref-tool.py.txt`. Review every changed line: is each docstring sentence supported by the
pins in %(W)s/fetch-c1/ (quote them with computed locators) - especially 'remembers the floating size', 'work area', 'monitor box', and the TILED/pseudo-tiled
sentence (find the pseudo path in %(W)s/fetch/Hyprland-Window.cpp or another pinned file and quote it)? Robustness: huge `fullscreen` ints, `fullscreen` as
nested JSON, 1 MiB dumps of fullscreen clients (time), output injection via class. Does the change break any round-43 caller (SKILL.md probe rows quoting the
summary line; grep the lane for `MADO_GEOMETRY:` parsers)? Write %(W)s/w1/RevRefTool/findings.md.""")

# ------------------------------------------------------------ critics (5)
seat("CritC1Cheat", "critic",
     "Cheats against C1: tools that reach TARGET_MET without the capability.",
     """Design and BUILD cheats (files under %(W)s/w1/CritC1Cheat/), score each with `""" + SCORE1 + """`: a tool that special-cases the 14 fixed fixtures' bytes and
handles the lattice by the round-43 logic (does the lattice defeat it?); a tool whose state logic lives in a helper without the word fullscreen (b4 vacuous?);
a selftest padded to 80 with trivial checks; a tool that reads `fullscreenClient` when `fullscreen` is absent; a tool that detects the counter's sandbox.
Report each: size, the clause that should catch it, whether it reached MET, and a tightening that does not reject the reference. Do NOT edit the counter.""")
seat("CritC2Cheat", "critic",
     "Forgeries against C2: admitted entries whose claims are not grounded.",
     """Build forged entry+registry+lesson sets in scratch fixture repos (`D=$(mktemp -d -p %(S)s/CritC2Cheat)`, clone %(L)s at %(F)s, -C "$D" everywhere) that
PRED-C2-r44 admits although ungrounded: real quotes at true locators under claims they do not support (e.g. claim 'GTK always adopts the configured size'
beside a quote that says no such thing), the census lines true but the entry's prose contradicting them, an entry citing the five pins with a decision table
that overclaims. Score: `""" + SCORE2 + """`. For each admitted forgery: the lines, the clause that should have caught it, a tightening that keeps a genuine
entry admitted, or 'declared residual (non-author reading)'. Write %(W)s/w1/CritC2Cheat/forgeries.md. Do NOT edit the counter.""")
seat("CritClaimSizing", "critic",
     "Attack the round's claim sizing before any data (prompt section 6 item 9).",
     """Read %(W)s/registration.md, /home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-44.md section 6 item 9, /home/vgpnk/Projects/shokunin/AXES.md. Attack: (1) can a
do-nothing or near-do-nothing control reach either target (build the cheapest ones beyond the registered controls: a 10-line patch to the round-43 tool, a
README-only commit, the staged r12 re-pointed to lane ids) and score them; (2) is C1 an operability axis-move or a bug fix that should not count (name the surface
it moves); (3) is C2 new ground per corpus/README.md or a deepening of hyprland-gkeep-geometry-r43.md; (4) universal clauses; (5) the lowest-axis argument against
%(W)s/receipts/axis-base.txt; (6) separability. Each finding: severity, exact sentence/line, command and output. Write %(W)s/w1/CritClaimSizing/findings.md.""")
seat("CritFsPremise", "critic",
     "Falsify C1's premise: is a DIFFER for a fullscreen/maximized client really false, and is FULLSCREEN/MAXIMIZED the right report?",
     """Argue the opposite case with sources: maybe the rule's size IS still meaningful while maximized (e.g. Hyprland restores it on exit; a user wants to know
the rule would apply); maybe `fullscreen` 1/2 can be set while the box is the rule's (fullscreen request pending, a fakefullscreen/fullscreenstate rule where
internal and client modes differ, `fullscreenClient` vs `fullscreen`). Read %(W)s/fetch-c1/ and fetch further Hyprland efb50993 files (pin them in your seat dir with sha256)
for `fullscreenstate`, `syncFullscreen`, client-only fullscreen. Verdict per scenario: tool output, true state, right/wrong. Write %(W)s/w1/CritFsPremise/findings.md.""")
seat("CritAssimilation", "critic",
     "Attack the planned assimilation decisions and the r12 predecessor's claims.",
     """Read %(P)s/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md and the residue files, then the pins %(W)s/fetch/. Attack r12 claim by claim: which are
refuted (e.g. its quotes at tag v0.56.2 vs the pinned commit; 'the acknowledgement is tracked - which is precisely the mechanism by which a client could report a
different size'; 'a GTK4 window with no minimum-size request will adopt the size the compositor configures'), which are unsupported by the pins, which survive. Also
attack the planned refusals of r13/r14/r15 (journal route) - would refusing them lose true knowledge? Check %(W)s/assimilation/id-guard.md and renumber-map.tsv
(by document? S311 tag URL vs S164 commit URL - same bytes? fetch both and compare sha256). Write %(W)s/w1/CritAssimilation/findings.md.""")

# ------------------------------------------------------------ mutation-testers (2)
seat("MutC1CounterGates", "mutation-tester",
     "Mutation-test C1's counter: each gate must be able to fail.",
     """Copy %(L)s/quality/counters/c1-r44-geometry-states.py AND c1-r42-geometry.py to %(S)s/MutC1CounterGates/ (keep them side by side) and mutate the r44 counter (one
edit each, >= 25): fsmode_of domain, verdict order in the model, suffix condition, TOTAL, N_GEN, MIN_SELFTEST, MIN_STATE_SITES, KILL_FRACTION, the regress check
(rc/needle), FS_POOL, fixture lists, the `old.model_out` patch removed. Run each mutated counter on (a) the reference %(W)s/c1/ctl-ref-tool.py.txt and (b) the
registered controls (regenerate them with %(W)s/ctl/run-c1-controls.py's VARIANTS into your scratch) and record: does a mutant score a bad control MET (gate
broken) or the reference below MET (over-strict)? Write %(W)s/w1/MutC1CounterGates/matrix.md; for each survivor: equivalent (proof) or missing control.""")
seat("MutRefSelftest", "mutation-tester",
     "Mutation-test the reference's selftest on the state logic.",
     """Mutate client_fsmode, evaluate and report of %(W)s/c1/ctl-ref-tool.py.txt (>= 30 edits) and run only `--selftest` (python3 -I) on each. Record which mutants
the selftest kills and which only the counter's fixtures kill (score survivors with `""" + SCORE1 + """`). For each selftest survivor: equivalent (proof) or
missing assertion (give it: input, expected output). Write %(W)s/w1/MutRefSelftest/matrix.md.""")

# ------------------------------------------------------------ sentinel, simplifier (2)
seat("SentLiveReads", "sentinel",
     "Safety review of the round's host reads and the C1 reference.",
     """Review: (1) every host command the wave context allows and every command the live-host and oracle-free seats run - read-only? any socket write beyond
request-socket reads? (2) the reference %(W)s/c1/ctl-ref-tool.py.txt against attacker-chosen class/title strings (output injection into MADO_GEOM_* lines,
ReDoS with the SAFE alphabet - round 43 found `(a|aa)+$` hangs; is the `timeout 5` guard in SKILL.md still the documented mitigation?), (3) whether the C2 entry's
planned claims could lead a reader to mutate the desktop (e.g. advising `dispatch`). Rank by severity with repro. Write %(W)s/w1/SentLiveReads/findings.md.""")
seat("SimpContract", "simplifier",
     "Dead weight in C1's contract extension and the C2 counter delta.",
     """For each sentence of the C1 extension (counter docstring + reference docstring) decide whether some input makes the output depend on it (build the pair,
run the reference) or whether it is dead/redundant (e.g. 'not a float' given JSON 2.0 parses to float; FULLSCREEN before MAXIMIZED order when only one value is
possible per client). Same for the C2 clause-h text. List dead/redundant sentences with the proof and the exact deletion text. Write %(W)s/w1/SimpContract/dead-weight.md.""")

assert len(items) == 38, len(items)
assert len({i["name"] for i in items}) == 38
print(len(items), dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-44/w1",
        "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
