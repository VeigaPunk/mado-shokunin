#!/usr/bin/env python3
"""Generates .ufo/waves/round-45/w1-spec.json (41 seats, v1 wave: build + first falsifiers).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
"""
import collections
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-45"
FREEZE = "22a8dedd02f507689c567777e0f20b5e645c8ce0"
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r45"
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
mado round 45 (hyaku run 9, 2026-10-26), inline v1 wave w1 of two (41 seats: build + first falsifiers). Lane repo: %(L)s (desktop and
compositor craft: the Hyprland/waybar/walker config plane and display behaviour of this host; axes coverage + operability).
Claims are FROZEN at %(W)s/registration.md (freeze commit %(F)s, base %(B)s) - read it first. Two claims, both on the Hyprland MONITOR RULE plane:
- C1 operability (capability acquisition): a new read-only tool tools/mado-monitors.py joining `monitor = NAME, MODE, POSITION, SCALE[, KEY, VALUE]...`
  lines of config files with one `hyprctl monitors all -j` dump: which rule each output gets, whether mode / position / scale (after Hyprland's 1/120
  correction) / transform / mirror agree; AGREE / DIFFER / DISABLED / UNRULED per output; top verdict NO_RULES 4 | NOT_COMPARED 5 | DIFFER 1 |
  NO_MATCHING_MONITOR 3 | OK 0. The CONTRACT is the docstring of the reference %(W)s/l1-draft/mado-monitors.py (not yet installed; selftest 33/33).
  Frozen counter %(L)s/quality/counters/c1-r45-monitors.py (PRED-C1-r45: clauses a tool present, s selftest N/N >= 30, f 49 seeded fixtures, r no
  hyprctl/journalctl/wlr-randr/wayland-info on PATH run). Target fixtures=49/49 TARGET_MET; base 0/49 MISSED. Controls receipts/ctl-c1.txt: 0 of 16 MET.
  Score a tool: put it at tools/mado-monitors.py in a scratch clone (below), commit there, then
  `python3 -I %(L)s/quality/counters/c1-r45-monitors.py --repo <clone> --rev HEAD --work %(S)s/<YourSeatName>/w [--seed N]`
- C2 coverage (sourced): a new entry corpus/knowledge/hyprland-monitor-rule-r45.md - the chain from the `monitor =` line to `hyprctl monitors all -j`
  at the host's Hyprland 0.56.2 (efb50993). L1 draft: %(W)s/l1-draft/entry.md; rows S302-S310 and the lesson Gate are built by %(W)s/l1-draft/build-pos.py.
  Frozen counter %(L)s/quality/counters/c2-r45-monitor-entry.py (PRED-C2-r45, clauses a-j; census line `hyprland monitor-rule default_refresh=60
  refresh_tolerance=1 scale_step=1/120 scale_search=89 json_refresh_decimals=5 line_keys=8`; 17 surfaces; locator width <= 30). Target admitted=1/1;
  base 0/1. Controls receipts/ctl-c2.txt: P admitted, 9 do-nothing/forged rejected. Positive-control repo recipe:
  `D=$(mktemp -d -p %(S)s/<YourSeatName>); git clone -q --shared --no-checkout %(L)s "$D"; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D";
  git -C "$D" checkout -q --detach %(F)s; python3 -I %(W)s/l1-draft/build-pos.py "$D"; git -C "$D" add -A;
  git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m pos` then
  `python3 -I %(L)s/quality/counters/c2-r45-monitor-entry.py --repo "$D" --rev HEAD --base %(B)s`
Pins (fetched + opened by the L1 2026-10-26; sha256 in %(W)s/receipts/fetch-sha256.txt) in %(W)s/fetch/: Hyprland-Parser.cpp, Hyprland-legacy-ConfigManager.cpp,
  Hyprland-MonitorRuleManager.cpp, Hyprland-MonitorRule.hpp, Hyprland-Monitor.cpp, Hyprland-HyprCtl.cpp, Hyprland-MonitorPositionController.cpp (all
  raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/...), hyprutils-String.cpp (hyprwm/hyprutils v0.14.2), wiki-Monitors.md
  (hyprwm/hyprland-wiki ecc06f3b6605e453c0ad533d979fccbefff788ef content/Configuring/Monitors.md). Host: Hyprland 0.56.2-4, hyprutils 0.14.2-1, one output DP-1;
  ~/.config/hypr/monitors.conf declares `monitor = DP-1, 3440x1440@100, 0x0, 1`; live run receipts/live-monitors-host-l1.txt (AGREE, OK).
  The registry (%(L)s/corpus/SOURCES.md) tops at S301 (238 rows); held S158 (HyprCtl.cpp) and S162 (legacy ConfigManager.cpp) have the same URLs
  under other scopes.
Round-44 closure routed defects (%(L)s/corpus/lessons/round-44-verifier-spotcheck.md section 6): D1 live window titles tracked in
  .ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json and .ufo/waves/round-43/w2/SentLiveRun/dump-now.json (SKILL.md rule 4: session material
  shape-only); D2 SCORECARD Round 44 rows lack after values; D3 tip receipts named 74c606a not the tip; D4 nonce before-share; D5 open predicate defects;
  D6 S290-S297 supersession; D7 w2/ConnCalibration mismatches. considerthese: %(L)s/considerthese/2026-10-26.md (proposal 1: privacy check on receipts).
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin outside the lane), sibling lanes, templates/, scripts/,
  MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout (READ-ONLY; never run a campaign tool there), or the lane's jj/git
  index. Never run mutating git/jj in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus your Report file. Never edit an existing tracked file (counters,
  controls, registration, reference, pins are FROZEN); the L1 is the only integrator. Write your Report file FIRST (a short status), then refine it;
  a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>.
- SCRATCH (operator directive 2026-10-25): every clone, venv, build, fixture and counter work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it
  explicitly as TMPDIR/--work/dir=, never rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB; copy receipts into your
  seat dir first, then delete your scratch dir before you finish (`trap 'rm -rf -- "$S"' EXIT`). A /tmp or scratch path is never citable evidence.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input injection, no
  Wayland-client connection of your own on the host session. Allowed compositor reads: `hyprctl version`, `hyprctl monitors -j`, `hyprctl monitors all -j`,
  `hyprctl workspaces -j`, `hyprctl getoption <name> -j`; NEVER `dispatch`, `keyword`, `reload`, `setprop`, `--batch`, `output`, `plugin`, `kill`. Host
  config trees and binaries are READ-ONLY. Session material stays shape-only: never commit window titles, monitor serials/descriptions, process tables
  or home-directory listings - project live dumps to the fields you need.
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


REF = "%(W)s/l1-draft/mado-monitors.py"
C1 = "python3 -I %(L)s/quality/counters/c1-r45-monitors.py --repo <clone> --rev HEAD --work %(S)s/<YourSeatName>/w"
C2 = "python3 -I %(L)s/quality/counters/c2-r45-monitor-entry.py --repo <repo> --rev HEAD --base %(B)s"

# ------------------------------------------------------------ executors (13)
seat("ExecIndepA", "executor",
     "Independent implementation of C1's contract (from the docstring text only).",
     """WITHOUT reading the code below the docstring of """ + REF + """ (read only its docstring), write %(W)s/w1/ExecIndepA/mado-monitors.py from scratch
(python3 stdlib, `--selftest` with >= 30 real assertions). Install it in a scratch clone at tools/mado-monitors.py and score it: `""" + C1 + """` (also --seed 7
and --seed 1234). Report every failing fixture verbatim; for each, decide from the docstring whether your file or the contract/fixture is wrong (quote the
sentence). Then list every docstring sentence you had to read twice, both readings, and which fixture decides (or 'none' = a hole in the contract).""")
seat("ExecIndepB", "executor",
     "Second independent implementation of C1's contract, different author habits.",
     """Same as an independent rebuild: read ONLY the docstring of """ + REF + """, write %(W)s/w1/ExecIndepB/mado-monitors.py (stdlib; structure it differently:
e.g. a table-driven parser; selftest >= 30), score it with `""" + C1 + """` at seeds 45, 3, 99. Report failing fixtures with your ruling (tool vs
contract), the ambiguous sentences and a proposed contract wording per ambiguity.""")
seat("ExecScaleOracle", "executor",
     "Differential test of the scale correction against a C++ transcription of Monitor.cpp.",
     """Transcribe Hyprland's scale correction (%(W)s/fetch/Hyprland-Monitor.cpp:989-1051, incl. float m_scale, double Vector2D division, std::round) into a
small C++ program (g++ if present; if absent, say so and use a careful Python float32 emulation via struct) and compare it with expected_scale() of """ + REF + """
on >= 5000 cases: scales 0.25-3.0 in 0.01 and 1/120 steps plus random floats with <= 6 decimals, pixel sizes from common modes (640x480 .. 7680x4320, ultrawides,
odd sizes like 1366x768). Report every divergence (inputs, both outputs) and whether the 1e-4 agreement tolerance in the contract can flip a verdict. Note the
explicit-scale branch only (autoScale is not compared). Write %(W)s/w1/ExecScaleOracle/report.md with the harness source.""")
seat("ExecParseOracle", "executor",
     "Differential test of the line parser against Hyprland's handleMonitor/Parser.cpp semantics.",
     """Build a faithful model of handleMonitor (%(W)s/fetch/Hyprland-legacy-ConfigManager.cpp:1293-1387) + CMonitorRuleParser (%(W)s/fetch/Hyprland-Parser.cpp) +
MonitorRuleManager add/get (%(W)s/fetch/Hyprland-MonitorRuleManager.cpp:37-117) in C++ or Python (stoi/stof prefix semantics, CVarList2 trimming; read
hyprutils v0.14.2 src/string/VarList2.cpp yourself and pin it in your seat dir with sha256). Generate >= 3000 random monitor-line sequences (selectors, modes,
positions, scales, keys, modifiers, comments) and compare the final rule list + which rule each synthetic output gets with """ + REF + """ (which marks
unmodelled forms `unsupported`). Report every divergence on lines the tool models (not unsupported) - those are contract bugs - and the unsupported share.
Write %(W)s/w1/ExecParseOracle/report.md.""")
seat("ExecPrivacyGate", "executor",
     "considerthese 2026-10-26 proposal 1 + round-44 closure D1: a committed-receipt privacy gate shown able to fail.",
     """Write %(W)s/w1/ExecPrivacyGate/check-session-material.py (stdlib; the L1 may install it as quality/check-session-material.py): given --repo and
--rev, scan every tracked file under .ufo/ (git ls-tree -r at the rev, git show blobs) for session material: JSON arrays of objects carrying both `class`
and `title`/`initialTitle` keys with non-empty strings (live `hyprctl clients -j` dumps), `ss -xpa`/`ss -p` process tables (users:(("...",pid=)), monitor
`serial`/`description` strings from `monitors -j`, absolute /home/<user>/ paths listing more than N entries. Output one line per finding + a summary
`SESSION_MATERIAL: files=<n> findings=<n> rev=<hash>`, exit 1 if findings else 0; --selftest with positive and negative fixtures. Show it able to fail: run it at
base %(B)s (must list the two round-43 files of D1 and any others - report them all) and on a scratch clone where those files are replaced by 7-key
projections (must pass for them). Also list the round-38 `eventq-live-ss.txt` status. Write %(W)s/w1/ExecPrivacyGate/report.md with both runs verbatim.""")
seat("ExecProjectTitles", "executor",
     "Round-44 closure D1: produce the shape-only projections of the tracked live client dumps.",
     """Sweep every tracked file at %(B)s for live `hyprctl clients -j` content (`git grep -l -E '"(initialTitle|title)"' %(B)s -- .ufo`); for each, decide: live
host dump (session material) or a seat's own synthetic/test window (state why, e.g. the round-43 ExecOracleGkeep gkeep test windows). For every live dump write
a projection to %(W)s/w1/ExecProjectTitles/proj/<same repo-relative path> keeping exactly the 7 keys of .ufo/waves/round-43/fetch/host-clients-r43.json
(address, at, class, floating, mapped, monitor, size), same element order, json.dumps(indent=2) + newline; verify with a script that no `title` remains and that
every other value equals the original. Write %(W)s/w1/ExecProjectTitles/report.md: table path | kind | titles before | after | sha256 old/new. Do NOT edit the
originals; the L1 lands the replacements.""")
seat("ExecLiveHost", "executor",
     "Read-only live runs of the reference on this host, both list forms, both config scopes.",
     """Run """ + REF + """ read-only: (1) `hyprctl monitors all -j | python3 -I <ref> --monitors - --config ~/.config/hypr/monitors.conf`; (2) the same with
`hyprctl monitors -j` (no all); (3) with every .conf file that ~/.config/hypr/hyprland.conf reaches through `source =` lines (list them; check none other has a
`monitor` or `monitorv2` line: grep); (4) with omarchy's default monitors.conf if present under ~/.local/share/omarchy (read-only) to show what the tool says
about a commented/default file. Record each command, stdout, exit code in %(W)s/w1/ExecLiveHost/runs.txt; commit-safe projections only (name, width, height,
refreshRate, x, y, scale, transform, disabled, mirrorOf - never description/serial/make/model). State whether `monitors -j` and `monitors all -j` differ here.""")
seat("ExecSeedSweep", "executor",
     "Determinism and seed independence of PRED-C1-r45.",
     """In a scratch clone with the reference installed as tools/mado-monitors.py (commit it there), run the C1 counter for seeds 1..150 and 3 times at seed 45 with
PYTHONHASHSEED=0/1/random (the counter runs under python3 -I; still check). Record every non-MET seed with its failing fixture and why (name collision between
{A}/{B}/{C}/{D}? a name that is a prefix of another? a description containing a name?). Also time a run. Write %(W)s/w1/ExecSeedSweep/report.md.""")
seat("ExecHarmBase", "executor",
     "Harm watch baseline: every lane gate at the base and at the freeze.",
     """At %(B)s and at %(F)s (read-only; use scratch clones), run and record verbatim (command, last lines, exit): python3 -I %(L)s/quality/check-axis-scores.py --rev <rev>
--repo <repo>; quality/check-index.py --rev <rev> --repo <repo>; the round-44 counters (quality/counters/c1-r44-geometry-states-v2.py --work <scratch>,
c2-r44-gkeep-size-request-v2.py); tools/mado-geometry.py --selftest; tools/mado-verify.sh --selftest; the census
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (current tree). Write %(W)s/w1/ExecHarmBase/baseline.md
(the w2 harm check compares the tip against it).""")
seat("ExecC2Census", "executor",
     "Re-derive C2's census line, surfaces and Gate quotes independently from the pins.",
     """Without using the counter, compute from %(W)s/fetch/ by grep/awk: the rule's default refresh, the closeness bound, the scale step, the search length, the JSON
refresh decimals, the handleMonitor key count; compare with the frozen census line. Then for each of the 17 SURFACES in the counter, find the anchor line yourself
and check the L1 draft entry %(W)s/l1-draft/entry.md cites it with a <= 30-line locator on a keyword line. Then verify each GATE quote in %(W)s/l1-draft/build-pos.py
occurs exactly once in its receipt (whitespace-normalized, comments stripped) and the locators in the entry match the quote start lines. Build the positive control
(recipe in context) and run the counter. Write %(W)s/w1/ExecC2Census/report.md.""")
seat("ExecDoNothingC1", "executor",
     "Cheapest controls against C1 beyond the 16 registered.",
     """Try to reach PRED-C1-r45 TARGET_MET without the capability: (a) a lookup tool that embeds the counter's FIXTURES (import or copy) and maps a normalized input
(names replaced back to placeholders) to expected output; (b) a tool that reads the counter file from the lane at runtime; (c) mado-geometry.py with a 20-line patch;
(d) a tool that only handles the exact host config; (e) anything else cheap. Score each: `""" + C1 + """`. For each MET: the clause that should catch it and a
tightening that keeps the reference MET, or 'declared residual'. Write %(W)s/w1/ExecDoNothingC1/controls.md with the files.""")
seat("ExecSupersede", "executor",
     "Round-43 closure D2 / round-44 D6: a census-clean supersession of the imprecise S290-S297 cells.",
     """Read %(L)s/corpus/lessons/round-43-verifier-spotcheck.md (D2) and round-44-verifier-spotcheck.md (D6), %(L)s/.ufo/waves/round-44/w1/ScrSupersedeRows* if present,
and rows S290-S297 in %(L)s/corpus/SOURCES.md. Re-open each source the corrected cells need (fetch, sha256, locate the quote). Draft supersession rows (new ids
continuing after S310, `teaches` opening `supersedes S0NN -`, 11 cells, no `|` in cells, status per CORPUS.md) in %(W)s/w1/ExecSupersede/rows.md, then prove them in a
scratch mirror: copy %(L)s/corpus to a scratch dir, append the rows, run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/SOURCES.md`
(exit 0 required; paste output). List the Gate lines (URL, access date, <= 25-word located quote) each new row needs.""")
seat("ExecIdGuard", "executor",
     "Section 10 assimilation guards, read-only: id-collision proof, quarantine slice, package fit.",
     """Run the prompt's id guard into %(W)s/w1/ExecIdGuard/ (not into %(W)s/assimilation): reg-ids from %(L)s/corpus/SOURCES.md, staged-ids from %(P)s/SOURCES.append.md
with the 0-3-space pattern, comm -12 collisions; prove the guard on a scratch registry with an indented `  | S311 |` row. Derive the quarantine slice from
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data rows for mado only). Then read %(P)s/MERGE-REPORT.md and list every
staged theme touching monitors, outputs, modes, scale, displays (grep), with a fit verdict for this round's C2 (admit/refuse/none). Write report.md; read bytes only.""")

# ------------------------------------------------------------ critics (6)
seat("CritC1Cheat", "critic",
     "Cheats against PRED-C1-r45: TARGET_MET without the capability.",
     """Read the counter %(L)s/quality/counters/c1-r45-monitors.py and the controls %(W)s/ctl/run-c1-controls.py. Build tools that reach TARGET_MET while being wrong
on inputs the fixtures do not cover (e.g. ignore desc: on the long form, refresh tolerance only near 60/100, scale correction only for 1.3/1.6, mirror by id only,
environment sniffing: HYPRLAND_INSTANCE_SIGNATURE=mado-r45-fixture, cwd names fx-*, HOME layout). Score: `""" + C1 + """`. For each MET cheat: input where it is wrong,
the clause/fixture that should catch it, a fixture or clause that would, and whether the reference still passes it. Write %(W)s/w1/CritC1Cheat/findings.md.""")
seat("CritC2Forgery", "critic",
     "Forgeries against PRED-C2-r45: admitted entries whose claims are not grounded.",
     """Build forged entry/registry/lesson sets on the positive-control recipe (context) that the counter admits although wrong: true quotes at true locators beside false
claims (e.g. 'Hyprland uses the first matching rule', 'a rule without @ picks the fastest mode', 'disabled outputs never appear in monitors all'), a decision table that
overclaims, the census true but prose contradicting it in words rather than tokens. Score: `""" + C2 + """`. For each admitted forgery: lines, the clause that should catch it,
a tightening that keeps P admitted, or 'declared residual'. Write %(W)s/w1/CritC2Forgery/forgeries.md. Do NOT edit the counter.""")
seat("CritClaimSizing", "critic",
     "Attack the round's claim sizing before any data (prompt section 6 item 9).",
     """Read %(W)s/registration.md, /home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-45.md section 6 item 9, /home/vgpnk/Projects/shokunin/AXES.md. Attack: (1) can a
do-nothing or near-do-nothing control reach either target (build the cheapest ones beyond the registered controls and score them); (2) is C1 an operability axis-move
(name the surface; is tools/mado-verify.sh's hardcoded DP-1 row prior art that makes it not new?); (3) is C2 new ground per corpus/README.md and receipts/c2-ground-base.txt,
or a deepening of output-colour-boundaries-r14.md / config-health-report-r3.md; (4) universal clauses; (5) the lowest-axis argument against receipts/axis-base.txt;
(6) separability both ways. Each finding: severity, exact sentence/line, command and output. Write %(W)s/w1/CritClaimSizing/findings.md.""")
seat("CritEntryContent", "critic",
     "Sentence-by-sentence check of the L1 draft entry against the pins.",
     """For every sentence of %(W)s/l1-draft/entry.md open the cited locator in %(W)s/fetch/ and rule: supported / overclaimed / wrong / unsupported (no locator). Pay
attention to: 'the long or the short description' (where does m_description come from? aquamarine output->description - fetch aquamarine at the host's version
(pacman -Q aquamarine, read-only) and pin it), 'only the word all lists every output including disabled ones' (what do monitorState()->monitors() and allMonitors()
contain? fetch src/state/MonitorState.cpp at efb50993), 'explicit position is applied as written' (any later clamp/overlap fix?), 'falls back to its default scale',
'monitorv2 blocks are added after every monitor = line', 'the 0.003 Hz gap is inside the 1 Hz closeness bound' (is the closeness bound what accepted it?). Pin every
new file you fetch (sha256). Write %(W)s/w1/CritEntryContent/findings.md: sentence | verdict | evidence | corrected text.""")
seat("CritToolSemantics", "critic",
     "Where does the C1 contract diverge from Hyprland's real behaviour?",
     """Compare the docstring of """ + REF + """ with the pins: rule matching (desc: against short vs long description; empty selector; a name rule `desc:` with spaces),
transform modifier copy semantics, addreserved fall-through, unknown-key drop, mode `pref*`/keywords/modeline, `@RATE` grammar vs stof, scale < 0.25 vs isNumber failure,
auto positions, mirror name resolution (how does Hyprland find the mirror target: name or desc? find setMirror in Monitor.cpp), live `disabled` vs `monitors()` membership,
vrr/bitdepth/cm not compared, a wlr-output-management override. For each divergence: input, tool verdict, Hyprland's actual result (with locator), severity (wrong verdict /
missing verdict / documented limit). Write %(W)s/w1/CritToolSemantics/findings.md.""")
seat("CritPremise", "critic",
     "Falsify the premises: is the monitor plane genuinely uncovered and is the host claim honest?",
     """Sweep %(L)s/corpus/knowledge, SKILL.md, PROVINCE.md and tools/ at %(B)s for monitor/output/mode/scale coverage (grep -n -i 'monitor =|monitors -j|refreshRate|scale|
transform|desc:'). Rule whether C2's ground statement in %(W)s/registration.md is true, what the round-3 note says about 99.997 vs @100 ('EDID nominal quantization [INF]')
and whether the new entry supersedes, corrects or contradicts it (state which sentence). Check the live receipt %(W)s/receipts/live-monitors-host-l1.txt for session
material. Write %(W)s/w1/CritPremise/findings.md.""")

# ------------------------------------------------------------ reviewers (4)
seat("RevC1Counter", "reviewer",
     "Code review of the C1 counter.",
     """Review %(L)s/quality/counters/c1-r45-monitors.py line by line: docstring vs code (every clause), crash paths (bad rev, tool printing binary, huge output, timeout),
fixture expectations vs the reference docstring (re-derive 10 fixtures by hand: scale-1.3-corrected, readd-moves-last, fallback-first-empty-and-named, transform-modifier-bad,
addreserved-keeps-rule, mirror-missing, comments, wrong-types, monitorv2, sdr-eotf-drops-rule), the seeded name generator (collisions, prefix relations), the read-only clause,
scratch hygiene (does it delete what it creates? honours --work only?). Severity-ranked findings with repro. Write %(W)s/w1/RevC1Counter/review.md.""")
seat("RevC2Counter", "reviewer",
     "Code review of the C2 counter delta against its round-44 parent.",
     """Diff %(L)s/quality/counters/c2-r45-monitor-entry.py against %(L)s/quality/counters/c2-r44-gkeep-size-request-v2.py. Review every changed line: clause e scope comparison
(cell index right? whitespace?), clause h census (regexes exactly-once? handleMonitor end detection; census exemption only for the exact line), the h contradiction
check (false positives on legitimate prose such as `scale_search=89` inside a code span? trailing punctuation), clause i without assimilation, clause j width bound,
SURFACES anchors (exactly once each - verify), docstring vs code. Write %(W)s/w1/RevC2Counter/review.md, severity-ranked with repro.""")
seat("RevTool", "reviewer",
     "Code review of the reference tool.",
     """Review """ + REF + """: docstring vs code for every sentence; input handling (BOM, CRLF, tabs, NUL, huge lines, non-UTF-8, JSON NaN/Infinity, numbers as
floats like 3440.0, negative sizes, bool-as-int), output injection (selector strings with newlines or `verdict=` inside: json.dumps?), exit codes, stdin cap, read-only
(no subprocess/socket/env use), the selftest's teeth. Severity-ranked findings with repro commands. Write %(W)s/w1/RevTool/review.md.""")
seat("RevRows", "reviewer",
     "Review the draft registry rows S302-S310 and Gate lines.",
     """Take the ROWS and QUOTES in %(W)s/l1-draft/build-pos.py: per row check kind/tier/scope against CORPUS.md contract v1 (/home/vgpnk/Projects/shokunin/CORPUS.md section
SOURCES.md), the anchor ranges against the receipt (open them: do the named functions sit there?), the teaches cell against the bytes, the location URL (re-fetch each, sha256
must equal the pin), the cross-scope repeats of S158/S162 (is a new row justified or should the held row be cited?). Build the positive control and run the census
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md`. Write %(W)s/w1/RevRows/review.md: row | verdict | fix.""")

# ------------------------------------------------------------ mutation-testers (2)
seat("MutC1Counter", "mutation-tester",
     "Mutation-test the C1 counter: each clause and each fixture family must be able to fail.",
     """Copy %(L)s/quality/counters/c1-r45-monitors.py to %(S)s/MutC1Counter/ and mutate it (>= 25 single edits): SELFTEST_MIN, the selftest parse, the stderr check,
the rc check, the readonly marker, fixture expectations (flip one verdict, drop a line), the name table, the env. Run each mutant on the reference (scratch clone) and on the
registered controls (regenerate with %(W)s/ctl/run-c1-controls.py VARIANTS logic into your scratch). Record: mutant scores a bad control MET (gate broken) or the reference
below MET (over-strict). Write %(W)s/w1/MutC1Counter/matrix.md; each survivor: equivalent (proof) or missing control.""")
seat("MutTool", "mutation-tester",
     "Mutation-test the reference tool: which semantic mutants survive selftest + fixtures?",
     """Mutate """ + REF + """ (>= 40 single edits across parse_line, parse_mode/pos/scale, add, effective, compare, expected_scale, verdict order, output formats). For each
mutant run --selftest, then score survivors with `""" + C1 + """`. List mutants killed by neither (missing fixture: give the input, expected output and the contract
sentence) and by fixtures only (missing selftest assertion). Write %(W)s/w1/MutTool/matrix.md.""")

# ------------------------------------------------------------ scouts (3)
seat("ScoutFrontier", "scout",
     "Where does the monitor plane sit in the lane's coverage map and Frontier?",
     """Read %(L)s/corpus/README.md (index + `## Frontier`), PROVINCE.md, SKILL.md rows on monitors (grep -n -i monitor), corpus/knowledge/output-colour-boundaries-r14.md.
Report: the exact Frontier text the new entry moves (quote + line), the README index row shape to use, the SKILL.md tables where the tool and its exit map belong (line
numbers of the round-43/44 mado-geometry rows to mirror), and the PROVINCE.md tool-table row shape. Write %(W)s/w1/ScoutFrontier/map.md.""")
seat("ScoutSiblings", "scout",
     "Sibling-lane overlap on the monitor/output plane.",
     """Read-only sweep of sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (not mado): PROVINCE.md and corpus/knowledge for monitor rules, outputs, displays,
hyprctl monitors, EDID, scale (grep -l -i). For each hit: lane, file:line, whether it owns the ground, overlaps, or is adjacent. Rule whether C1/C2 absorb sibling ground
(adjacency axis). Write %(W)s/w1/ScoutSiblings/overlap.md.""")
seat("ScoutRecheck", "scout",
     "Upstream drift since the pins: is efb50993 still what the host runs, and has the monitor code moved upstream?",
     """Confirm the host's Hyprland commit (`hyprctl version`, pacman -Q hyprland hyprutils - read-only) equals the pins. Then compare the pinned Parser.cpp,
MonitorRuleManager.cpp and the monitor part of legacy ConfigManager.cpp with hyprwm/Hyprland main today (fetch raw, diff): what changed (e.g. sdr_eotf added to the
line handler? rule matching?), which entry sentences would go stale on upgrade, and what `recheck:` should say. Also check whether the hyprland-wiki Monitors page at
main still documents `sdr_eotf` on the line form. Pin what you fetch (sha256). Write %(W)s/w1/ScoutRecheck/drift.md.""")

# ------------------------------------------------------------ connectors (3)
seat("ConnCrossClaim", "connector",
     "Cross-claim and cross-source pattern check: separability and shared assumptions.",
     """Show C1 and C2 are causally separable: build (scratch clones) a tree with only the tool installed (C1 MET? C2 still 0/1?) and one with only the C2 data from
build-pos.py (C2 admitted? C1 still MISSED?); run both counters on both. Then find assumptions both claims share (e.g. the 60 Hz default, the 1 Hz bound) and
whether one wrong pin would sink both. Write %(W)s/w1/ConnCrossClaim/report.md.""")
seat("ConnCalibration", "connector",
     "Count self-assessment mismatches at the base (round-44 D7 follow-through).",
     """At %(B)s compare the lane's self-assessment with repo state: SCORECARD Round 44 section claims (rows, counts, receipts named), SHONEN.md boxes and their pointers,
LOG.md Round 44 bullets, corpus/README.md counts, PROVINCE tool table vs `git ls-tree tools/`. Count mismatches (each: claim, location, observed, command). Include the
round-44 closure D2/D3/D7 items and say which are still open. Write %(W)s/w1/ConnCalibration/mismatches.md with a final `mismatches=<n>` line.""")
seat("ConnLessonsPattern", "connector",
     "Pattern across the lane's last six closures: which routed defect classes recur?",
     """Read %(L)s/corpus/lessons/round-{39,40,41,43,44}-verifier-spotcheck.md section 6 (routed defects) and the lessons' ## Mistakes. Cluster the defects by class (tip
receipts, nonce, session material, open predicate defects, SCORECARD values, cited-before-landed paths...), count recurrences, and say which class this round's freeze
already addresses (seeded counter, width bound) and which needs a QUALITY criterion or a gate. Propose <= 3 criteria with the lesson rows that would back them. Write
%(W)s/w1/ConnLessonsPattern/patterns.md.""")

# ------------------------------------------------------------ scribes (7)
seat("ScrSkillRows", "scribe",
     "Draft the SKILL.md additions for tools/mado-monitors.py.",
     """Read %(L)s/SKILL.md around the mado-geometry rows (grep -n mado-geometry) and """ + REF + """'s docstring. Draft, in the SKILL's existing shapes: the tool-table
row, the exit-map line, a decision table 'monitor rule vs running output' (question | verdict/field | what it proves | what it does not), and the licence notes (DIFFER is
a join not a blame; runtime keyword/output-management overrides; desc: long form; monitorv2 -> NOT_COMPARED). Every factual line cites a pin locator. Write
%(W)s/w1/ScrSkillRows/skill-rows.md (append-ready text + the line it goes after).""")
seat("ScrProvinceRow", "scribe",
     "Draft the PROVINCE.md tool row and refinement note.",
     """Read %(L)s/PROVINCE.md (the tool table and the round-23/36 refinements). Draft an append-only round-45 refinement: the tools/mado-monitors.py row (Reads | Writes |
Owner and adjacent lanes) and the counters quality/counters/c1-r45-monitors.py, c2-r45-monitor-entry.py, and the privacy gate (if the L1 lands it) as record
instruments. Write %(W)s/w1/ScrProvinceRow/province.md.""")
seat("ScrLessonGate", "scribe",
     "Draft corpus/lessons/round-45.md: Gate, registry changes, search log.",
     """Draft %(W)s/w1/ScrLessonGate/round-45.md with: `## Gate` (candidates considered: the nine pins + any rejected candidate such as the wiki at main, held S158/S162
reuse vs new rows; admitted/rejected with reasons; one GATE line per cited id in the exact counter format from build-pos.py; each new row's URL, access date 2026-10-26,
<= 25-word located quote - verify each quote by grep against %(W)s/fetch/), `## Registry changes` (old->new for any status/recheck/used-by change), `## Search log`
(question, where searched, identified/screened/included/excluded counts, stop rationale). Leave `## Mistakes` to ScrMistakes.""")
seat("ScrMistakes", "scribe",
     "Mine the mistakes for corpus/lessons/round-45.md ## Mistakes.",
     """From %(L)s/corpus/lessons/round-44-verifier-spotcheck.md section 6 (D1-D7) and the round-44 lesson, draft M45-n rows: class (vacuous, survivor, stale-premise,
reference-drift, number-drift, scope, attribution, landing, provider - CORPUS.md vocabulary) | evidence pointer | captured-by (criterion or rule that should have caught it,
or none) | fix (and how the fix is shown able to fail). Include D1 (session material: captured-by SKILL.md rule 4, no gate), D4 (nonce before-share), D3 (tip receipts).
Propose QUALITY.md criteria (next number after the last in %(L)s/corpus/QUALITY.md) each citing its lesson row. Write %(W)s/w1/ScrMistakes/mistakes.md.""")
seat("ScrErrata", "scribe",
     "Draft the append-only errata for round-44 closure D2, D3, D7.",
     """Draft append-ready text (never rewrites): SCORECARD Round 45 errata giving Round 44's after values and verdicts (C1 `fixtures=26/26 ... TARGET_MET` at e467892 and
74c606a; C2 `admitted=1/1 TARGET_MET`; verify each against %(L)s/.ufo/waves/round-44/receipts/*after*), D3's tip-receipt equivalence statement (verify:
`git -C %(L)s diff --name-only 74c606a 8ac15c41`), and D7's ConnCalibration mismatches (read .ufo/waves/round-44/w2/ConnCalibration.md; one erratum each, with the
command that shows the truth). Write %(W)s/w1/ScrErrata/errata.md.""")
seat("ScrReadme", "scribe",
     "Draft the corpus/README.md index row and Frontier text for the new entry.",
     """Read %(L)s/corpus/README.md (index rows shape; the round-44 row; `## Frontier`). Draft the index row for knowledge/hyprland-monitor-rule-r45.md and a Frontier
bullet: what the round moves (U5 runtime state agreement for the monitor rule), what stays open (colour/HDR, output-management apply, monitorv2 field parsing,
the long description). Write %(W)s/w1/ScrReadme/readme.md.""")
seat("ScrEntryDraft", "scribe",
     "An alternative draft of the C2 entry's prose sections for the L1 to merge.",
     """Read %(W)s/l1-draft/entry.md and the pins. Draft improved prose for its weakest parts (a 'How to read a DIFFER' section: runtime keyword, output-management
client, a mode the output does not offer; the 60 Hz consequence for omarchy's default commented lines in ~/.config/hypr/monitors.conf; what `monitors -j` omits), each
sentence with a <= 30-line locator in the receipt-name:line form. Do not add S### ids outside the existing OBS lines. Verify every locator by grep -n. Write
%(W)s/w1/ScrEntryDraft/sections.md.""")

# ------------------------------------------------------------ sentinel, simplifier, revenger (3)
seat("SentTool", "sentinel",
     "Safety review of the tool, counters and the round's host reads.",
     """Review """ + REF + """ and both counters: any subprocess/socket/env/network path in the tool; output injection; path handling (symlinks, FIFOs, /proc files as
--config); resource exhaustion (1 MiB cap, regex backtracking); counters' scratch handling (rmtree targets, --work outside scratch, /tmp use - section 7 item 4); the
fake PATH binaries; the live receipt content. Rank by severity with repro. Write %(W)s/w1/SentTool/findings.md.""")
seat("SimpContract", "simplifier",
     "Dead weight in the C1 contract and the C2 counter delta.",
     """For each sentence of """ + REF + """'s docstring decide whether some input makes the output depend on it (build the pair, run the reference) or it is dead/redundant
(e.g. `len(ids) >= 1` mirror lookups, `cand != 0`, the V2 regex tail, `toks[0] == modeline` vs startswith). Same for the C2 counter's new clause h/i/j code. List dead or
redundant parts with the proof and the exact deletion text. Write %(W)s/w1/SimpContract/dead-weight.md.""")
seat("RevengerOmarchy", "revenger",
     "Reverse-engineer how omarchy writes and expects monitors.conf.",
     """Read-only: find omarchy's default monitors.conf and any omarchy script that writes or reads monitor lines (grep -rn 'monitor' under ~/.local/share/omarchy/bin
and default/hypr; never run them). Report: the default file's lines, which are active, what the tool would report for each preset if uncommented (run """ + REF + """ on
copies in your scratch with a synthetic dump), and whether any omarchy script assumes semantics the entry contradicts (e.g. GDK_SCALE pairing, fractional 1.6/1.75).
Write %(W)s/w1/RevengerOmarchy/report.md.""")

n = len(items)
assert n == 41, n
assert len({i["name"] for i in items}) == n
print(n, dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-45/w1", "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
