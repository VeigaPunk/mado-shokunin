#!/usr/bin/env python3
"""Generates .ufo/waves/round-43/w2-spec.json (32 seats, v1 wave: falsify the round-43 data commit).

Run: python3 make-w2-spec.py  (writes next to itself, lane-relative reportDir).
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-43"
W42 = LANE + "/.ufo/waves/round-42"
FREEZE = "b2e2efd6e268920d31f3c32cf52dc097dd6e1d22"
FREEZE2 = "496340dd53fabd800be42e8fb19090f35e2c235c"
DATA = "1959770657f1f8665097c1aed4be6c1cbb07139f"
BASE = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r43"
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
mado round 43 (hyaku run 8, 2026-10-26), inline v1 wave w2 of two (32 seats: FALSIFY the landed data). Lane repo: %(L)s
Read %(W)s/registration.md (freeze %(F)s) and %(W)s/registration-v2.md (C2 v2 freeze %(F2)s, made BEFORE data) first. The data commit is %(D)s
(base %(B)s); every attack names the item it attacks. Claims as judged:
- C1 operability (capability acquisition): `tools/mado-geometry.py` (byte-identical to the round-42 reference %(W42)s/c1/ctl-ref-tool.py.txt, sha256 e3c2e471...),
  counter `quality/counters/c1-r42-geometry.py` (PRED-C1-r42, unchanged). L1 measured at %(D)s: `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0
  (%(W)s/receipts/c1-after-data.txt). Live host run: %(W)s/receipts/live-geometry-host.txt (NO_MATCHING_CLIENT, rc 3).
- C2 coverage (sourced; assimilation): `corpus/knowledge/hyprland-gkeep-geometry-r43.md`, counter `quality/counters/c2-r43-gkeep-entry-v2.py` (PRED-C2-r43-v2);
  L1 measured at %(D)s: `admitted=1/1 verdict=TARGET_MET`, exit 0 (%(W)s/receipts/c2-after-data.txt; v1 also 1/1). New rows S290-S297 in corpus/SOURCES.md
  (S290 RegexMatchEngine.cpp, S291 DefaultFloatingAlgorithm.cpp, S292 Target.cpp, S293 WindowTarget.cpp, S294 GeometricMovableAnimated.cpp - all at
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>; S295 host-gkeep.conf, S296 host-clients-r43.json,
  S297 gkeep-ui-excerpt.py - own-work receipts in %(W)s/fetch/); held rows S155 (WindowRuleApplicator.cpp) and S158 (HyprCtl.cpp) cited with one used-by item appended.
  Lesson corpus/lessons/round-43.md (Gate, ADMIT/REFUSE, Mistakes M43-1..8), README index row + Frontier bullet, PROVINCE.md tool row, SKILL.md rows
  (decision row, probe row, subsection 'Rule size versus reported size'), QUALITY.md criteria 77-81, the locator checker quality/check-locators.py.
- Wave w1 reports (38 seats) are in %(W)s/w1/ - read the ones your item names; do not re-report a w1 finding unless you show it still holds at %(D)s.
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin except as your task names), sibling lanes,
  templates/, scripts/, MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout, or the lane's jj/git index.
  Never run mutating git/jj anywhere in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git
  (log/show/diff/status/rev-parse/ls-tree/cat-file) is fine.
- Write ONLY to your own seat directory %(W)s/w2/<YourSeatName>/ (create it), plus any explicit destination your task names. Never edit an
  existing tracked file (the counters, controls, registration, reference, fetch receipts are FROZEN); the L1 is the only integrator.
  Write your Report file FIRST (a short status), then refine it; a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>.
- SCRATCH (operator directive 2026-10-25): every clone, venv, build, fixture and counter work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it explicitly as TMPDIR/--work/dir=, never
  rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB; copy receipts into your seat dir first, then delete your scratch dir before you finish (`trap 'rm -rf -- "$S"' EXIT`).
  The driver reaps idle scratch after 45 min, so a /tmp or scratch path is never citable evidence: cite only files in your seat dir. A tree you leave on disk is your own reported defect.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input injection, no
  Wayland-client connection of your own on the host session. Allowed compositor reads (read verbs of the request socket only): `hyprctl version`, `hyprctl clients -j`,
  `hyprctl monitors -j`, `hyprctl getoption <name> -j`, `hyprctl binds -j`; NEVER `dispatch`, `keyword`, `reload`, `setprop`, `--batch`, `output`, `plugin`, `kill`. Host config
  trees and binaries are READ-ONLY. A nested/oracle compositor may run ONLY inside the bubblewrap oracle of the round-27 harness, never on the host session.
- Git fixtures (run-6 incident): any fixture repo is `D=$(mktemp -d -p %(S)s) && git -C "$D" init -q`, every later git call names `-C "$D"`, and
  `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the first commit; never `git commit` with a throwaway identity anywhere else.
- Tooling authorization (operator, 2026-10-19): install tools that help the task (read /home/vgpnk/.omp/agent/RULES.md first; official
  channels only: uv tool / uv pip into a scratch venv / npx / official binaries in ~/.local/bin; never pacman, never -Sy/-Syu/-U/-R). Record tool/version/channel/reason in your report.
  pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide until the operator resolves the host-recovery L0 question; install only via `uv tool`/`uv pip`/`npx`/an official binary in
  ~/.local/bin, or report a blocker; never -Sy, -Syu, -U, -R, a downgrade, or a restart of a host service.
- Seat tool state: your tools start at the fleet root, not the lane: use absolute paths everywhere.
- You are a leaf: no subagent dispatch, no background jobs, no spawning (an executor MAY spawn one read-only labrat probe).
- Every finding names what it attacks or supports (a path:line, a command and its output, or a hash). Never fabricate: an unrun check has
  not passed. Quotes lifted from a source are <= 25 words, located (file:line or section), and verified by a script that greps your receipt.
"""


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W42)s", W42), ("%(W)s", W), ("%(F2)s", FREEZE2), ("%(F)s", FREEZE),
                 ("%(D)s", DATA), ("%(B)s", BASE), ("%(P)s", PKG), ("%(S)s", SCR)):
        t = t.replace(k, v)
    return t.replace("%%", "%")


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({
        "name": name, "role": role,
        "prompt": sub(GODSPEED + "# Target\n" + target.strip() +
                      "\n# Task\n" + task.strip() + "\n")})


CLONE = """Work on a shared clone: S=%(S)s/<YourSeatName>; mkdir -p "$S"; D=$(mktemp -d -p "$S"); git clone -q --shared %(L)s "$D"; check
`git -C "$D" rev-parse --show-toplevel` equals $D; `git -C "$D" checkout -q <rev>` only inside it; delete $S before you finish."""

# ---------------------------------------------------------------- executors (7)
seat("RerunC1Data", "executor", "Re-run C1's counting command at the data commit (attacks receipts/c1-after-data.txt).",
     CLONE + """ In the clone, run `C1R42_TMP=$S python3 -I %(L)s/quality/counters/c1-r42-geometry.py --repo "$D" --rev %(D)s` three times (three fresh nonces) and once
with `--nonce` replaying the nonce printed in %(W)s/receipts/c1-after-data.txt; also at %(B)s (expect tool=absent). Confirm `git -C "$D" show %(D)s:tools/mado-geometry.py | sha256sum`
equals the round-42 reference's sha256. Paste every final line and exit code verbatim into %(W)s/w2/RerunC1Data/receipt.txt; state AGREE/DISAGREE with the L1 receipt.""")
seat("RerunC2Data", "executor", "Re-run C2's counting commands at the data commit (attacks receipts/c2-after-data.txt and c2-v1-after-data.txt).",
     CLONE + """ Run `TMPDIR=$S python3 -I %(L)s/quality/counters/c2-r43-gkeep-entry-v2.py --repo "$D" --rev %(D)s` and the v1 counter c2-r43-gkeep-entry.py at the same rev and at %(B)s;
paste all per-clause lines and the final lines with exit codes to %(W)s/w2/RerunC2Data/receipt.txt. Then independently (your own script, not the counter) recompute for each of the 10 cited ids:
the Gate receipt sha256, that the quote occurs exactly once word-bounded in the whitespace-collapsed receipt, the 1-based start line, and that the entry line carries it. Report any disagreement.""")
seat("RerunControlsV2", "executor", "Re-run the C2 v2 controls and the forgery harness (attacks receipts/ctl-c2-v2.txt and ctl/v2-forgeries/*.log).",
     """Run `cd %(L)s && TMPDIR=%(S)s/RerunControlsV2 python3 -I .ufo/waves/round-43/ctl/run-c2-controls-v2.py` and the two harness scripts in %(W)s/ctl/v2-forgeries/ (forge.py, more.py)
- BUT copy them into your seat dir first and change their output/scratch dirs to your seat dir and %(S)s/RerunControlsV2 so nothing in ctl/ is rewritten. Compare every line with the committed logs
(`diff`), report the tallies (controls, correct, admitted forgeries by name) and any divergence. Write %(W)s/w2/RerunControlsV2/report.md.""")
seat("RerunCensus", "executor", "Re-run the source census and registry counts (attacks receipts/census-after-data.txt and the 226 -> 234 row claim).",
     """Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (paste output + exit), and at %(B)s and %(D)s (via `git -C %(L)s show <rev>:corpus/SOURCES.md` into your seat dir)
`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|'` on both. Check: exactly S290-S297 added, every new row 11 cells, status mined, opened 2026-10-26, used-by = the entry; S155/S158 cells 1-10 byte-equal to base and one used-by item appended;
no other row changed (`diff` of the two registries). Run the census on the base registry too (`--file`) and state the W-set difference. Write %(W)s/w2/RerunCensus/receipt.txt.""")
seat("ExecHarmTip", "executor", "No-harm check: base vs data commit on every lane gate and selftest (attacks the round's no-harm claim).",
     CLONE + """ At %(B)s and at %(D)s run: `bash tools/mado-verify.sh --selftest`, `python3 -I tools/mado-options.py --selftest`, `python3 -I tools/mado-globals.py --selftest`, `python3 -I tools/mado-geometry.py --selftest` (data only),
`python3 -I quality/check-index.py --rev <rev> --repo .`, `python3 -I quality/check-index-rows.py --rev <rev> --repo .`, `python3 -I quality/check-axis-scores.py --rev <rev> --repo .`, `python3 -I quality/check-locators.py --selftest`.
Tabulate every value base -> data and name each difference as expected (new entry, new tool) or a harm. Note: the published axis table is updated by a later records commit; report the axis rows as they are at %(D)s.
Write %(W)s/w2/ExecHarmTip/harm.txt and report.md.""")
seat("ExecSeparability", "executor", "Causal separability of C1 and C2 at the data commit (attacks registration 'Separability').",
     CLONE + """ In the clone, from %(D)s make two scratch commits (identity via `-c user.name=t -c user.email=t@t.invalid`, only with `-C "$D"`): (a) delete tools/mado-geometry.py -> C2 v2 counter must still print admitted=1/1;
(b) revert the entry, lesson, SOURCES.md, README.md to %(B)s -> C1 counter must still print 37/37 TARGET_MET. Paste the commands and final lines into %(W)s/w2/ExecSeparability/receipt.txt.""")
seat("ExecDoNothingV2", "executor", "Do-nothing and cheap controls against PRED-C2-r43-v2 at the data commit's shape (attacks the v2 target's discrimination).",
     """Using the v2 controls runner's helpers (importlib on %(W)s/ctl/run-c2-controls-v2.py; never run main; fixture repos under %(S)s/ExecDoNothingV2 with `-C "$D"` on every git call), build at least 12 cheap
controls that skip the claimed work but keep the shape: an entry that quotes each pinned receipt correctly but whose prose claims nothing about gkeep; one whose decision table contradicts the census; a wallpaper entry made of
the ten quotes only; the landed entry with every INF/UNK line deleted; the landed entry with its claims negated but quotes intact; etc. Score each under v2; list which are admitted (declared residual: claim-binding) vs rejected,
and for each admitted one say whether the landed entry's actual prose is distinguishable from it by any mechanical rule. Write %(W)s/w2/ExecDoNothingV2/report.md.""")

# ---------------------------------------------------------------- critics (7)
seat("CritEntryOverreach", "critic", "Sentence-by-sentence overreach hunt in the landed entry (attacks corpus/knowledge/hyprland-gkeep-geometry-r43.md).",
     """For EVERY sentence of `git -C %(L)s show %(D)s:corpus/knowledge/hyprland-gkeep-geometry-r43.md`, open the receipt it rests on (%(W)s/fetch/, the w1 seat files it points at) and classify: SUPPORTED (quote the line),
OVERSTATED (say what the source supports instead), UNSUPPORTED, or WRONG. Pay special attention to: 'evaluates that expression only inside its first-map branch', 'A tiled window never takes this branch', 'the dots match any character',
'no read verb of the request socket exposes the current value', the oracle paragraph, the census line claims, the decision-table states. Write %(W)s/w2/CritEntryOverreach/findings.md (table + the exact replacement text for every non-SUPPORTED sentence).""")
seat("CritEntryInf", "critic", "Attack the entry's INF and UNK reasoning against the full upstream sources (not just the pinned excerpts).",
     """The entry's INF lines claim: a tiled window never reads the size rule; the size rule acts only on first map; FullMatch makes `^`/`$` redundant; GOAL vs CURRENT differ during the open animation. Open the full Hyprland v0.56.2 sources at
efb50993780079460b0cbed1363e2166a2de1d9f (raw.githubusercontent.com; pin what you open with sha256 in your seat dir): any other consumer of `static_.size` (grep the tree via the GitHub search API or a shallow clone under %(S)s/CritEntryInf),
e.g. toggling floating later, `setFloating`, tiled->float transitions, `Window.cpp`, the tiled algorithms, xwayland paths. Is 'never'/'only' true? Write %(W)s/w2/CritEntryInf/findings.md with located <= 25-word quotes and a verdict per INF line.""")
seat("CritC1Capability", "critic", "Does the installed tool deliver the capability the SKILL/PROVINCE/SCORECARD text claims (attacks the C1 capability row and SKILL.md 'Rule size versus reported size').",
     """Read `git -C %(L)s show %(D)s:SKILL.md` (the new decision row, probe row and subsection), PROVINCE.md's new tool row, and tools/mado-geometry.py. For every sentence about the tool (inputs, outputs, exit map, verdict licences,
'opens no file and writes nothing', 'starts no process'), build an input that would falsify it and run the tool (copy it to your scratch; host reads only via `hyprctl clients -j`). Also test it on the host's REAL rule set: every file the host's hyprland.conf sources
(read-only) - how many size rules exist, how many the tool supports vs counts unsupported, and is that limit stated honestly in SKILL.md? Write %(W)s/w2/CritC1Capability/findings.md.""")
seat("CritOracleClaim", "critic", "Attack the oracle observation the entry cites (attacks entry section 4 and %(W)s/w1/ExecOracleGkeep/).",
     """Read %(W)s/w1/ExecOracleGkeep.md and its directory (20-observation.txt, 10-cases.txt, receipts/). Check: is the nested compositor really Hyprland 0.56.2 at efb5099 (which binary, sha)? was the host's rule file used byte-identically
(sha256)? does the clients -j object really carry size [420,500] and floating true (quote the receipt line)? do the controls (nofloat, size300, floatonly, nomatch, minsize) show what the entry says they show? Is anything in the entry's oracle
sentence stronger than the receipts? Do NOT run a compositor yourself. Write %(W)s/w2/CritOracleClaim/findings.md (per entry clause: SUPPORTED / OVERSTATED with receipt path:line).""")
seat("CritAssimilation", "critic", "Attack the assimilation decisions (attacks the lesson's ADMIT/REFUSE lines and the ledger).",
     """Re-open the five decided staged files in %(P)s/knowledge/corpus/knowledge/ (ADMIT gkeep-size-to-real-size-r11.md; REFUSE gkeep-size-rule-application-r10.md, gkeep-geometry-unobservable-r8.md, gkeep-observation-route-r11.md,
gkeep-element-rules-r30.md) and the lesson's `## Assimilation ledger` (`git -C %(L)s show %(D)s:corpus/lessons/round-43.md`). For each: is the stated reason TRUE of the file (quote it), is the flip condition meaningful, and does the landed entry
actually carry what it says it took from the admitted file? Is any not-adopted file actually better grounded than the admit? PROVINCE fit (`PROVINCE.md`). Read-only in shokuknow. Write %(W)s/w2/CritAssimilation/findings.md.""")
seat("CritLocatorGate", "critic", "Attack the new locator checker (attacks quality/check-locators.py and QUALITY criterion 77).",
     """Run `python3 -I %(L)s/quality/check-locators.py --selftest` and build inputs that it judges wrongly: false OK (a locator whose range does not hold the fact but shares identifier tokens with it, a fragment of only short tokens,
a locator wrapped onto the next prose line, a locator with no backticked fragment), false MISS (multi-line quotes, fragments abbreviating a qualified name like `w->size(GEOMETRIC_GOAL)` vs the source's qualified form). Run it over the lane's
SKILL.md, LOG.md and corpus/knowledge/*.md at %(D)s with `--fetch %(W)s/fetch` and `--fetch %(W42)s/fetch`; triage every MISS (real error vs checker limit). Write %(W)s/w2/CritLocatorGate/findings.md.""")
seat("CritClaimSizingData", "critic", "Re-attack the round's claim sizing now that data landed (prompt section 6 item 9; attacks both claims' verdicts).",
     """Read %(W)s/registration.md, registration-v2.md, %(W)s/w1/CritClaimSizing.md and the receipts. Attack: (1) was v2 frozen strictly before any data (compare commit order: `git -C %(L)s log --format='%%H %%cI %%s' %(B)s..%(D)s`);
(2) does any committed byte of %(D)s show the target reached by something other than the claimed work; (3) is C1's 'capability acquisition' honest given the tool is byte-identical to a round-42 reference (is the claim worded as installation +
falsification, as registration-v2 says?); (4) does any LOG/lesson sentence use a universal clause the counter does not enumerate; (5) is the axis naming right (C2 coverage: which PROVINCE/README surface moved; command that would show it unmoved).
Write %(W)s/w2/CritClaimSizingData/findings.md.""")

# ---------------------------------------------------------------- scribes (2), simplifier (1), sentinel (1)
seat("ScribeClosureTable", "scribe", "Run and record the considerthese proposal-2 closure table (attacks QUALITY criterion 81's numbers).",
     """Run `bash %(W)s/w1/ScrConsiderthese/check78.sh --selftest` and the command criterion 81 names (read `git -C %(L)s show %(D)s:corpus/QUALITY.md`, criterion 81) for rounds 36-42 with the tip map %(W)s/w1/ScrConsiderthese/tips.txt
(read-only; run from %(L)s). Paste outputs; compare every number in criterion 81 and in %(W)s/w1/ScrConsiderthese/proposal.md section 3.1 with the output; draft the corrected sentence if any number differs.
Write %(W)s/w2/ScribeClosureTable/table.md.""")
seat("ScribeReportDraft", "scribe", "Draft the Sources & frontier and Trend-verdict sections of the round report from committed evidence only.",
     """From `git -C %(L)s show %(D)s:<path>` of corpus/SOURCES.md, corpus/lessons/round-43.md, corpus/README.md and the receipts in %(W)s/receipts/, draft: rows before -> after with the counting command, rows added by tier, rows touched old->new (S155/S158 used-by),
frontier rows advanced (README Frontier), assimilation (theme, admitted, refused, id guard: %(W)s/assimilation/), and one trend verdict each for expansion, quality, discernment (improved/harmed/unchanged/unprovable-but-better) with evidence pointers.
Mark anything you could not verify as UNVERIFIED. Write %(W)s/w2/ScribeReportDraft/draft.md.""")
seat("SimpEntryLesson", "simplifier", "Dead weight in the landed entry, lesson and SKILL subsection (attacks prose that no reader or gate needs).",
     """Read the entry, the lesson and the SKILL.md subsection at %(D)s. List sentences that are redundant (say the same thing twice), unverifiable as written, or dead (point at a file that does not exist at %(D)s: check each path with
`git -C %(L)s cat-file -e %(D)s:<path>`). Give exact deletion/replacement text, and say which deletions are SAFE against the C2 v2 counter (a line carrying an id's quote+locator must stay). Write %(W)s/w2/SimpEntryLesson/dead-weight.md.""")
seat("SentLiveRun", "sentinel", "Security/safety check of the installed tool's real host use (attacks 'starts no process, opens no socket, writes nothing').",
     """Copy `git -C %(L)s show %(D)s:tools/mado-geometry.py` into %(S)s/SentLiveRun. Run it under `strace -f -e trace=process,network,file` (install strace via an official non-pacman channel only if missing; otherwise use python audit hooks:
`python3 -I -X importtime` is not enough - use `sys.addaudithook` in a wrapper) on: the host dump (`hyprctl clients -j` piped), the selftest, a FIFO path, /dev/stdin closed. Confirm no execve beyond python, no socket/connect, no write/open-for-write.
Also check %(W)s/receipts/live-geometry-host.txt is reproducible now (same verdict). Write %(W)s/w2/SentLiveRun/findings.md with the trace excerpts.""")

# ---------------------------------------------------------------- scouts (4): re-open every new row
for nm, rows_, what in (
        ("ScoutRowsA", "S290 and S291", "RegexMatchEngine.cpp and DefaultFloatingAlgorithm.cpp"),
        ("ScoutRowsB", "S292 and S293", "Target.cpp and WindowTarget.cpp"),
        ("ScoutRowsC", "S294 and the held S155, S158", "GeometricMovableAnimated.cpp, WindowRuleApplicator.cpp and HyprCtl.cpp"),
        ("ScoutRowsD", "the own-work rows S295, S296, S297", "host-gkeep.conf, host-clients-r43.json, gkeep-ui-excerpt.py")):
    seat(nm, "scout", "Re-open registry rows " + rows_ + " (" + what + ") - attacks each row's every cell.",
         """For each row (`grep -nE '^\\| (S29[0-7]|S155|S158) ' %(L)s/corpus/SOURCES.md`), re-open the source yourself TODAY: upstream rows - curl the row's URL and compare sha256 with %(W)s/receipts/fetch-sha256.txt; own-work rows - compare the pinned receipt with the live host file
(`~/.config/hypr/gkeep.conf`, a fresh `hyprctl clients -j` reduced the same way, `sed -n '446,$p' ~/Projects/gkeep/gkeep/ui.py` at `git -C ~/Projects/gkeep rev-parse HEAD`). Then check every cell: the anchor's line ranges hold what it says (grep -n),
the 'teaches' cell is true of the source, the tier/kind are right, recheck is a valid date/cadence, used-by names the entry, and the lesson's GATE line for the id (quote, sha256) is exact. Verdict per cell; exact fix text for any wrong cell.
Write %(W)s/w2/""" + nm + """/rows.md.""")

# ---------------------------------------------------------------- reviewers (5)
seat("RevLesson", "reviewer", "Review corpus/lessons/round-43.md (attacks the Gate, the ledger and Mistakes M43-1..8).",
     """At %(D)s: every GATE line's sha256 and quote (recompute); every evidence pointer in `## Mistakes` resolves (`git cat-file -e`, line numbers via `git show <rev>:<file> | sed -n Np`); every 'Shown able to fail' is actually shown
(re-run the command if cheap); every number (counts, line numbers like `LOG.md:2483`, `receipt.txt:60`) is right. List each defect with the fix text. Write %(W)s/w2/RevLesson/findings.md.""")
seat("RevQuality", "reviewer", "Review QUALITY.md criteria 77-81 (attacks each criterion's check command and its 'shown able to fail').",
     """For each of criteria 77-81 at %(D)s (`git -C %(L)s show %(D)s:corpus/QUALITY.md | tail -12`): run its Check command exactly as written (from %(L)s; scripts under .ufo/waves/round-43/w1/...); record output and exit;
does it fail on the named bad input and pass on the good one? Does every cited path/line resolve at %(D)s? Is each criterion backed by a real mistake (lesson pointer resolves)? Write %(W)s/w2/RevQuality/findings.md.""")
seat("RevSkillProvince", "reviewer", "Review the SKILL.md, PROVINCE.md and README.md additions (attacks their accuracy against the tool and the sources).",
     """`git -C %(L)s diff %(B)s %(D)s -- SKILL.md PROVINCE.md corpus/README.md`. For every added sentence: verify against tools/mado-geometry.py (run it), the pinned receipts (every locator: grep -n), and the entry. Run
`python3 -I %(L)s/quality/check-index-rows.py --rev %(D)s --repo %(L)s` and `python3 -I %(L)s/quality/check-locators.py --fetch %(W)s/fetch SKILL.md` (from %(L)s). Write %(W)s/w2/RevSkillProvince/findings.md with fix text.""")
seat("RevRegistrationV2", "reviewer", "Review the C2 v1 -> v2 re-registration (attacks 'frozen before any data' and 'the docstring is the code').",
     """Check: (1) commit order and content `git -C %(L)s log --stat %(B)s..%(D)s`; the v2 freeze %(F2)s precedes %(D)s and no entry/row/lesson byte exists at %(F2)s; (2) `diff quality/counters/c2-r43-gkeep-entry.py quality/counters/c2-r43-gkeep-entry-v2.py`
- every code change is stated in the v2 docstring and nothing in the docstring lacks code; (3) the v2 tightenings each have a control that kills a violation (ctl/v2-forgeries logs); (4) control P with true raw URLs still matches the counter's e+ prefix.
Write %(W)s/w2/RevRegistrationV2/findings.md (severity, line, reproduction).""")
seat("RevIdGuardQuarantine", "reviewer", "Review the assimilation id guard and quarantine verdicts (attacks %(W)s/assimilation/ against the landed ids).",
     """Re-run the id-collision guard from the round prompt (0-3 leading spaces) over the lane registry at %(D)s and %(P)s/SOURCES.append.md; prove it once on a scratch registry with an indented colliding row. Compare the w1 renumber map
(%(W)s/assimilation/) with the LANDED ids (S290-S297 by document; S155/S158 held) - list every mismatch and whether the landed mapping is by document. Spot-check 3 quarantine verdicts from %(W)s/assimilation/quarantine-verdicts.md by
re-fetching the source. Write %(W)s/w2/RevIdGuardQuarantine/findings.md.""")

# ---------------------------------------------------------------- mutation-testers (2)
seat("MutCheckLocators", "mutation-tester", "Mutation-test quality/check-locators.py (attacks its selftest teeth).",
     """Copy %(L)s/quality/check-locators.py to %(S)s/MutCheckLocators/ and make >= 25 single-edit mutants (range inclusion, token length, attribution nearest-before/after, name resolution, exit codes, verdict strings).
For each run `--selftest` and the round-42 LOG control (`--fetch %(W42)s/fetch` over `git -C %(L)s show %(B)s:LOG.md` saved to your dir; expect MISS for Hyprland-HyprCtl.cpp:394-395,412-413). Table: mutant | edit | selftest | control | survivor?;
classify each survivor (equivalent with proof, or missing assertion with the input). Write %(W)s/w2/MutCheckLocators/matrix.md.""")
seat("MutC2V2", "mutation-tester", "Mutation-test the v2 tightenings of the C2 counter (attacks each d+/e+/g+/i+ condition).",
     """Copy %(L)s/quality/counters/c2-r43-gkeep-entry-v2.py to %(S)s/MutC2V2/ and, for each v2 condition (unique occurrence, comment stripping per extension, raw-URL prefix, every-naming-line bound, exact package path, flip word, BAD_LOC in entry,
all-PINS cited), make >= 2 mutants that weaken it. Score each with the v2 controls runner and forge/more harness copies pointed at the mutant (copies in your dir; never edit ctl/). A mutant no control kills is a missing control: name the input that would.
Also score each mutant on the landed data commit %(D)s (it must stay admitted). Write %(W)s/w2/MutC2V2/matrix.md.""")

# ---------------------------------------------------------------- connectors (3)
seat("ConnCrossFindings", "connector", "Cross-read all 38 w1 reports against the landed data (attacks 'every w1 finding was integrated or declared').",
     """Read every %(W)s/w1/*.md (and the findings files they point to). For each finding: status at %(D)s - FIXED (where), DECLARED (residual named in registration-v2.md or the lesson), or OPEN (not addressed). Pay attention to:
RevC1Counter, MutC1CounterGates, SentReDoS, RevRefTool, CritContract, MutRefSelftest, ExecC1ExtraMutants (C1 side) and RevC2Counter, ExecC2ExtraMutants (C2 side). Write %(W)s/w2/ConnCrossFindings/matrix.md (finding | seat | severity | status | pointer).""")
seat("ConnSiblingDup", "connector", "Sibling-lane overlap of the landed entry, tool and SKILL rows (adjacency axis).",
     """Scan read-only /home/vgpnk/Projects/shokunin/*-shokunin/ (PROVINCE.md, corpus/README.md, corpus/knowledge, tools, SKILL.md) for holdings about window-rule size/float, `hyprctl clients -j` size semantics, GEOMETRIC_GOAL, gkeep.
Compare with %(W)s/w1/ConnSiblingOverlap/overlap.md: anything new since? Does mado's new SKILL decision row overlap a sibling's routing row? Name the arbitrating lane for any contested surface. Write %(W)s/w2/ConnSiblingDup/overlap.md.""")
seat("ConnCalibration", "connector", "Calibration: the lane's self-assessment vs repo state after the data commit (attacks SCORECARD/SHONEN/LOG claims).",
     """At the lane tip at your run time (`/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state %(L)s` prints `local=`): list every round-43 statement in SCORECARD.md, LOG.md and SHONEN.md and check it against repo bytes
(counts, hashes, verdicts, paths). Run `python3 -I quality/check-axis-scores.py --rev <tip> --repo .` from %(L)s. Count mismatches between self-assessment and observed state (the calibration axis's own definition, AXES.md).
Write %(W)s/w2/ConnCalibration/mismatches.md (statement | location | observed | match?).""")

import collections as _c
assert len(items) == 32, len(items)
assert len({i["name"] for i in items}) == 32
print(len(items), dict(_c.Counter(i["role"] for i in items)))
spec = {"wave": "w2", "context": CONTEXT, "reportDir": ".ufo/waves/round-43/w2",
        "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w2-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
