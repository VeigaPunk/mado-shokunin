#!/usr/bin/env python3
"""Generates .ufo/waves/round-46/w1-spec.json (66 seats, one v2 wave: build + attack + round-45 w2 falsification).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
"""
import collections
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-46"
FREEZE = "8c5434c60e03f147ee1f75ab195e8bc3f0db4dec"
BASE = "b22ea56bff2faec39ce9ff75d2107eaf4612ecbe"
R45DATA = "ee6659b90f7bf69aa03283dba804dd90081b7ff5"
R45TIP = "4d22eeb66c2835af8aaa3fac6ad838fa616aa663"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r46"
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
mado round 46 (hyaku run 9, 2026-10-26), ONE v2 wave w1 (66 seats: build + attack + the round-45 w2 falsification the last round never ran).
Lane repo: %(L)s (desktop and compositor craft: the Hyprland/waybar/walker config plane and the display/input behaviour of this host;
axes coverage + operability). Claims are FROZEN at %(W)s/registration.md (freeze commit %(F)s, base %(B)s) - read it first. Two claims,
both on the Hyprland INPUT-DEVICE plane (how `input { kb_* }` and `device { name = X ... }` config becomes what `hyprctl devices -j` prints):
- C1 operability (capability acquisition): a new read-only tool tools/mado-devices.py joining the input/device lines of config files with one
  `hyprctl devices -j` dump: per keyboard the expected XKB names (device block value when the block SETS it, else global input:kb_*, else the
  default us/empty) vs the printed rules -> AGREE / DIFFER / FALLBACK (printed us+empty = keymap failed to compile) / VIRTUAL (hl-virtual-keyboard*);
  per mouse the expected scrollFactor (device block scroll_factor clamped 0..100 when set, else -1) -> AGREE / DIFFER; per device block MATCHED /
  NO_SUCH_DEVICE; top verdict NOT_COMPARED 5 | DIFFER 1 | NO_KEYBOARDS 3 | STALE_BLOCK 4 | OK 0. The CONTRACT is the docstring of the reference
  %(W)s/l1-draft/mado-devices.py (not yet installed; selftest 48/48). Frozen counter %(L)s/quality/counters/c1-r46-devices.py (PRED-C1-r46: a tool
  present, s selftest N/N >= 30, f 90 fixtures from quality/counters/c1-r46-fixtures.json x 3 runs (seed 46 env A, seed 46 env B, nonce env A),
  i bubblewrap isolation, r no hyprctl/libinput/journalctl/udevadm run, g 150 nonce-generated cases judged by the pinned reference). Target
  fixtures=90/90 generated=150/150 ... TARGET_MET; base 0/90 MISSED. Controls receipts/ctl-c1.txt: PASS, 0 of 23 MET, reference MET.
  Score a tool: put it at tools/mado-devices.py in a scratch clone (recipe below), commit there, then
  `python3 -I %(L)s/quality/counters/c1-r46-devices.py --repo <clone> --rev HEAD --work %(S)s/<YourSeatName>/w [--nonce N]`
- C2 coverage (sourced): a new entry corpus/knowledge/hyprland-input-devices-r46.md - the chain from config to `hyprctl devices -j` at the host's
  Hyprland 0.56.2 (efb50993) and hyprlang 0.6.8. L1 draft: %(W)s/l1-draft/entry.md; rows S316-S325, the lesson Gate and the README row are built by
  %(W)s/l1-draft/build-pos.py. Frozen counter %(L)s/quality/counters/c2-r46-input-device-entry.py (PRED-C2-r46, clauses a-j; census line
  `hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 json_scroll_decimals=2
  virtual_prefix=hl-virtual-keyboard`; 28 surfaces; locator width <= 30). Target admitted=1/1; base 0/1. Controls receipts/ctl-c2.txt: PASS
  (P admitted, 14 do-nothing/forged rejected). Positive-control recipe:
  `D=$(mktemp -d -p %(S)s/<YourSeatName>); git clone -q --shared --no-checkout %(L)s "$D"; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D";
  git -C "$D" checkout -q --detach %(F)s; python3 -I %(W)s/l1-draft/build-pos.py "$D"; git -C "$D" add -A;
  git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m pos` then
  `python3 -I %(L)s/quality/counters/c2-r46-input-device-entry.py --repo "$D" --rev HEAD --base %(B)s`
Pins (fetched + opened by the L1 2026-10-26; sha256 in %(W)s/receipts/fetch-sha256.txt) in %(W)s/fetch/: Hyprland-InputManager.cpp,
  Hyprland-ConfigManager.cpp (legacy), Hyprland-ConfigValues.cpp, Hyprland-IKeyboard.cpp, Hyprland-HyprCtl.cpp, Hyprland-MiscFunctions.cpp,
  Hyprland-VirtualKeyboard.cpp (src/devices), Hyprland-protocols-VirtualKeyboard.cpp (src/protocols) - all
  raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/... -, hyprlang-config.cpp (hyprwm/hyprlang v0.6.8 src/config.cpp)
  and wiki-Keywords.md (hyprwm/hyprland-wiki ecc06f3b6605e453c0ad533d979fccbefff788ef content/Configuring/Keywords.md). Host: Hyprland 0.56.2,
  hyprlang 0.6.8-5 (headers /usr/include/hyprlang.hpp, /usr/lib/libhyprlang.so), libxkbcommon 1.13.2, 10 keyboards + 4 pointers; ~/.config/hypr/input.conf
  has one `input` block, no `device` block; live run of the reference: receipts/live-devices-host-l1.txt (9 AGREE, 1 VIRTUAL, OK).
  The registry (%(L)s/corpus/SOURCES.md) tops at S315 (252 rows). Held rows already on the same URLs under other scopes: S162/S303 (legacy
  ConfigManager.cpp), S158/S307 (HyprCtl.cpp), S173 (hyprlang config.cpp), S182 (MiscFunctions.cpp), S215 (ConfigValues.cpp).
Round-45 data under attack this round (closure D1: the w2 never ran): tool tools/mado-monitors.py, entry corpus/knowledge/hyprland-monitor-rule-r45.md,
  rows S302-S315, gate quality/check-session-material.py, landed at %(R45D)s (tip %(R45T)s); counters quality/counters/c1-r45-monitors-v2.py and
  c2-r45-monitor-entry-v2.py; closure %(L)s/corpus/lessons/round-45-verifier-spotcheck.md section 6 (D1-D6).
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin outside the lane), sibling lanes, templates/, scripts/,
  MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout (READ-ONLY; never run a campaign tool there), or the lane's jj/git
  index. Never run mutating git/jj in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus your Report file. Never edit an existing tracked file (counters,
  fixtures, controls, registration, reference, pins are FROZEN); the L1 is the only integrator. Write your Report file FIRST (a short status), then
  refine it; a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>.
- SCRATCH (operator directive 2026-10-25): every clone, venv, build, fixture and counter work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it
  explicitly as TMPDIR/--work/dir=, never rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB; copy receipts into your
  seat dir first, then delete your scratch dir before you finish (`trap 'rm -rf -- "$S"' EXIT`). A /tmp or scratch path is never citable evidence.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input injection, no
  Wayland-client connection of your own on the host session. Allowed compositor reads: `hyprctl version`, `hyprctl devices -j`, `hyprctl monitors -j`,
  `hyprctl monitors all -j`, `hyprctl getoption <name> -j`; NEVER `dispatch`, `keyword`, `reload`, `setprop`, `switchxkblayout`, `--batch`, `output`,
  `plugin`, `kill`. Host config trees and binaries are READ-ONLY. Session material stays shape-only: never commit window titles, monitor
  serials/descriptions, process tables or home-directory listings - project live dumps to the fields you need. Never write the host monitor's serial
  number anywhere (refer to it as "the serial" and by file:line only).
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
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(F)s", FREEZE), ("%(B)s", BASE), ("%(R45D)s", R45DATA),
                 ("%(R45T)s", R45TIP), ("%(P)s", PKG), ("%(S)s", SCR)):
        t = t.replace(k, v)
    return t.replace("%%", "%")


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({
        "name": name, "role": role,
        "prompt": sub(GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() + "\n")})


REF = "%(W)s/l1-draft/mado-devices.py"
C1 = "python3 -I %(L)s/quality/counters/c1-r46-devices.py --repo <clone> --rev HEAD --work %(S)s/<YourSeatName>/w"
C2 = "python3 -I %(L)s/quality/counters/c2-r46-input-device-entry.py --repo <repo> --rev HEAD --base %(B)s"
ORACLE_NOTE = """Build a TRUE oracle with the host's own parser: a small C++ program (g++ -std=c++23, -lhyprlang; headers /usr/include/hyprlang.hpp) that
registers exactly what Hyprland registers (%(W)s/fetch/Hyprland-ConfigManager.cpp: the `device` special category with key `name` and its values at
:518-565, plus regular values input:kb_layout/kb_variant/kb_options/kb_model/kb_rules/kb_file with the defaults of %(W)s/fetch/Hyprland-ConfigValues.cpp
:271-276 and input:scroll_factor; whatever else a config line needs, e.g. `input:touchpad:scroll_factor`), parses a config, and for a list of device
names prints what Hyprland's getConfigValueSafeDevice/getDeviceString/deviceConfigExplicitlySet (%(W)s/fetch/Hyprland-ConfigManager.cpp:1115-1201) would
return: the five XKB names, kb_file, and the scroll factor (set-by-user or not)."""

# ------------------------------------------------------------ executors (17)
seat("ExecIndepA", "executor",
     "Independent implementation of C1's contract (from the docstring text only).",
     """WITHOUT reading the code below the docstring of """ + REF + """ (read only its docstring), write %(W)s/w1/ExecIndepA/mado-devices.py from scratch
(python3 stdlib, `--selftest` with >= 30 real assertions). Install it in a scratch clone at tools/mado-devices.py and score it: `""" + C1 + """` (also
--nonce 7 and --nonce 1234). Report every failing fixture verbatim; for each, decide from the docstring whether your file or the contract/fixture is
wrong (quote the sentence). Then list every docstring sentence you had to read twice, both readings, and which fixture decides (or 'none' = a hole).""")
seat("ExecIndepB", "executor",
     "Second independent implementation of C1's contract, different author habits.",
     """Read ONLY the docstring of """ + REF + """, write %(W)s/w1/ExecIndepB/mado-devices.py (stdlib; structure it differently: e.g. a tokenizer +
state machine for the config; selftest >= 30), score it with `""" + C1 + """` at nonces 46, 3, 99. Report failing fixtures with your ruling (tool vs
contract), the ambiguous sentences and a proposed contract wording per ambiguity.""")
seat("ExecHyprlangOracle", "executor",
     "Differential test of the contract's config model against the host's real hyprlang 0.6.8 library (random configs).",
     ORACLE_NOTE + """ Generate >= 3000 random configs (input blocks and flat input:kb_* lines, device blocks by name, `device[X] {` and
`device[X]:key =` forms, merges, duplicate names, empty RHS, [[EMPTY]], comments with `#` and `##`, backslash continuations, CRLF, nested categories,
unknown keys, scroll_factor values with prefixes/exponents/garbage) restricted to forms the reference does NOT mark unsupported, and compare per device
the reference's expected names/factor (import """ + REF + """ and call parse_config/expected_names in-process) with the oracle. Report every divergence
(minimal config, both outputs) - each is a contract bug - and the share of generated lines the reference counts unsupported. Write
%(W)s/w1/ExecHyprlangOracle/report.md with the oracle source and the generator.""")
seat("ExecHyprlangOracleB", "executor",
     "Targeted edge cases of the contract against the real hyprlang 0.6.8 library.",
     ORACLE_NOTE + """ Then run these targeted cases and compare with the reference: a `device {` block whose first key is not `name`
(what device does hyprlang create, which name, what happens to later keys); a second `name =` inside a block; `device[X]:name = Y`; `device:kb_layout`
outside a block; a block closed and a flat `device:...` after it; `device [X]` with a space; brackets in a value; `input[x]:kb_layout`; a `device`
block nested in another category; `##` at line end; `###`; a `#` inside a value after `##`; continuation into a comment; a final continuation line;
`kb_layout =` (empty); `scroll_factor = 1e-40`, `0x10`, ` 1.5` (leading space), `+.5e1`, `1e39`; a variable defined AFTER use; `$` inside a device
name. For each: oracle result, reference result, and whether the reference marks it unsupported (then not a bug). Write
%(W)s/w1/ExecHyprlangOracleB/report.md.""")
seat("ExecStofOracle", "executor",
     "Differential test of the scroll-factor arithmetic: std::stof + std::clamp + std::format(\"{:.2f}\") on float vs the reference.",
     """Write a C++ program reproducing exactly %(W)s/fetch/Hyprland-InputManager.cpp:1379-1383 (std::stof on the value, clamp 0.F..100.F, the float
stored in an optional<float>) and %(W)s/fetch/Hyprland-HyprCtl.cpp:765-772 (std::format "{:.2f}" of m_scrollFactor.value_or(-1)); also reproduce hyprlang's
float parse (%(W)s/fetch/hyprlang-config.cpp: CONFIGDATATYPE_FLOAT branch, std::stof, exceptions). Compare against the reference's read_float() and its
"%%.2f" formatting (import """ + REF + """) on >= 20000 values: decimals with 1-7 places in [-5, 300], halves at the 3rd decimal (0.125, 0.135, 2.675 ...),
prefixes (`0.7x`, `1e`, `1e+`, `.5`, `5.`), exponents, subnormals, 1e38/1e39, hex, inf/nan spellings, leading/trailing spaces. Report every divergence and
whether it can flip an AGREE/DIFFER. Write %(W)s/w1/ExecStofOracle/report.md with the harness.""")
seat("ExecSeedSweep", "executor",
     "Determinism and nonce independence of PRED-C1-r46.",
     """In a scratch clone with the reference installed as tools/mado-devices.py (commit it there), run the C1 counter for nonces 1..120 and 3 times at
nonce 46 with PYTHONHASHSEED=0/1/random. Record every non-MET nonce with its failing fixture or generated case and why (placeholder names colliding,
one name a prefix of another, a generated config the model and the installed copy treat differently?). Time a run. Also check the counter's names()
cannot produce a name containing `[`, `]`, `$`, `#`, `=` or uppercase. Write %(W)s/w1/ExecSeedSweep/report.md.""")
seat("ExecDoNothingC1", "executor",
     "Cheapest controls against C1 beyond the 23 registered.",
     """Try to reach PRED-C1-r46 TARGET_MET without the capability: (a) a lookup tool that embeds c1-r46-fixtures.json and maps a normalized input
(names replaced back to placeholders) to the expected output, falling back to something for generated cases; (b) a tool that reads the counter or the
reference from the lane at runtime (clause i should hide it - prove it); (c) tools/mado-monitors.py or tools/mado-binds.py with a <= 30-line patch;
(d) a tool that only handles the host's config; (e) anything else cheap. Score each: `""" + C1 + """`. For each MET: the clause that should catch it and
a tightening that keeps the reference MET, or 'declared residual'. Write %(W)s/w1/ExecDoNothingC1/controls.md with the files.""")
seat("ExecLiveHost", "executor",
     "Read-only live runs of the reference on this host, every config scope.",
     """Run """ + REF + """ read-only: (1) `hyprctl devices -j | python3 -I <ref> --devices - --config ~/.config/hypr/input.conf`; (2) with every .conf
file that ~/.config/hypr/hyprland.conf reaches through `source =` lines, in source order (list them; grep each for `kb_`, `device`, `scroll_factor`);
(3) with omarchy's default input.conf (~/.local/share/omarchy/default/hypr/input.conf, read-only) placed BEFORE the user's file, as Hyprland sources
them - does the verdict change; (4) the same dump against a scratch copy of input.conf with `kb_layout = zz` to show what a typo would look like (the
tool can only predict, not observe, a FALLBACK - say so). Record each command, stdout, exit code in %(W)s/w1/ExecLiveHost/runs.txt (device names are
product names: keep them; drop nothing else is needed). Report whether `hyprctl devices -j` lists any device twice, and the `main` keyboard.""")
seat("ExecC2Census", "executor",
     "Re-derive C2's census line, surfaces and Gate quotes independently from the pins.",
     """Without using the counter, compute from %(W)s/fetch/ by grep/awk: the global kb_layout default, the fallback layout, the number of device
special values, the scroll-factor clamp ceiling, the JSON scrollFactor decimals, the virtual-keyboard prefix; compare with the frozen census line. For
each of the 28 SURFACES in %(L)s/quality/counters/c2-r46-input-device-entry.py find the anchor line yourself and check the draft entry
%(W)s/l1-draft/entry.md cites it with a <= 30-line locator on a keyword line, AND that the sentence around the locator says something the cited lines
actually support (quote them). Verify each QUOTES item of %(W)s/l1-draft/build-pos.py occurs exactly once in its receipt (whitespace-normalized,
comments stripped) at the entry's locator. Build the positive control (recipe in context) and run the counter. Write %(W)s/w1/ExecC2Census/report.md.""")
seat("ExecW2Monitors", "executor",
     "Round-45 w2 (closure D1): re-measure the landed round-45 tool and entry with fresh nonces and a live run.",
     """At %(R45T)s run `python3 -I %(L)s/quality/counters/c1-r45-monitors-v2.py --repo %(L)s --rev %(R45T)s --work %(S)s/ExecW2Monitors/w --nonce N`
for 5 fresh nonces, and `python3 -I %(L)s/quality/counters/c2-r45-monitor-entry-v2.py --repo %(L)s --rev %(R45T)s`. Then live: `hyprctl monitors all -j |
python3 -I <the tool from git show %(R45T)s:tools/mado-monitors.py> --monitors - --config ~/.config/hypr/monitors.conf` and against every .conf the host
sources that has a `monitor` line. Then 10 hand-written adversarial configs in scratch (desc: selectors with the long description, a transform modifier
before the rule, a scale needing the 1/120 search) - compare the tool's verdict with your own reading of the pins %(L)s/.ufo/waves/round-45/fetch/. Write
%(W)s/w1/ExecW2Monitors/report.md (projected dumps only: name, width, height, refreshRate, x, y, scale, transform, disabled, mirrorOf).""")
seat("ExecSessionTriage", "executor",
     "Round-45 closure D3 + SCORECARD planned 2: triage the session-material gate findings and teach it a synthetic marker.",
     """Run `python3 -I %(L)s/quality/check-session-material.py --repo %(L)s --rev %(R45T)s` (read its docstring for the exact CLI) and classify every
finding: real session material (which rule, which file), a synthetic fixture (a seat's own test data), or a false positive. Count each class. Design a
synthetic marker (e.g. a sentinel key/value or a path convention) the gate can honour WITHOUT letting a real dump hide behind it (state how you prevent
that), implement it in %(W)s/w1/ExecSessionTriage/check-session-material.py (a copy; never edit the tracked one), and show both directions: the 49
synthetic findings disappear, a planted real dump with the marker still fails. Draft the SKILL.md gate-registry row (name, command, verdict map, selftest
spelling, pinned value) in the shape of the existing `mado-axis-scores` row (grep -n 'mado-axis-scores' %(L)s/SKILL.md). Write report.md.""")
seat("ExecSerialRule", "executor",
     "Round-45 closure D2: teach the session-material gate a prose serial rule, without ever printing the serial.",
     """The host monitor's serial appears in prose in 3 held corpus entries and 21 wave files (closure D2; find them by reading `hyprctl monitors all -j`
-> `serial` into a shell variable and `git -C %(L)s grep -l -F "$SERIAL" %(R45T)s` - NEVER echo the value, print only file paths, line numbers and counts).
Extend a copy of %(L)s/quality/check-session-material.py in %(W)s/w1/ExecSerialRule/ with a rule that flags serial-like tokens in prose (state the
pattern and its false-positive rate on the whole tracked tree) and, optionally, a `--serial-from-host` mode that reads the live serial and greps for it
without printing it. Show it able to fail (the 24 files) and to pass (a projected tree). Write report.md with counts and paths only.""")
seat("ExecSupersede", "executor",
     "Round-44 D6 (carried twice): a census-clean supersession of the imprecise S290-S297 cells.",
     """Read %(L)s/corpus/lessons/round-43-verifier-spotcheck.md (D2), round-44-verifier-spotcheck.md (D6), round-45-verifier-spotcheck.md (D6) and rows
S290-S297 in %(L)s/corpus/SOURCES.md; read CORPUS.md rule 2 (/home/vgpnk/Projects/shokunin/CORPUS.md). Re-open each source the corrected cells need
(fetch, sha256, locate the quote). Draft the supersession in the form CORPUS.md allows (new rows continuing after S325 with `teaches` opening
`supersedes S0NN -`, or an appended errata block - decide which the census accepts), prove it in a scratch mirror: copy %(L)s/corpus, apply, run
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/SOURCES.md` (exit 0 required; paste output). List the Gate lines each
new row needs (URL, access date 2026-10-26, <= 25-word located quote). Write %(W)s/w1/ExecSupersede/rows.md.""")
seat("ExecIdGuard", "executor",
     "Section 10 assimilation guards, read-only: id-collision proof, quarantine slice, package fit for the input-device plane.",
     """Run the prompt's id guard into %(W)s/w1/ExecIdGuard/ (not into %(W)s/assimilation): reg-ids from %(L)s/corpus/SOURCES.md, staged-ids from
%(P)s/SOURCES.append.md with the 0-3-space pattern `^ {0,3}\\|[[:space:]]*S[0-9]{3,}`, comm -12 collisions; prove the guard on a scratch registry with an
indented `  | S316 |` row. Derive the quarantine slice from /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data
rows for mado only: awk -F'|' -v l=mado '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'). Then read %(P)s/MERGE-REPORT.md and
list every staged theme touching keyboards, input devices, XKB, layouts, libinput (grep -i), with a fit verdict for this round's C2 (admit/refuse/none
+ reason). Write report.md; read bytes only.""")
seat("ExecHarmBase", "executor",
     "Harm watch baseline: every lane gate at the base and at the freeze.",
     """At %(B)s and at %(F)s (read-only; scratch clones), run and record verbatim (command, last lines, exit): python3 -I %(L)s/quality/check-axis-scores.py
--rev <rev> --repo <repo>; quality/check-index.py --rev <rev> --repo <repo> (if present); the round-45 counters (c1-r45-monitors-v2.py --work <scratch>,
c2-r45-monitor-entry-v2.py); tools/mado-monitors.py --selftest; tools/mado-geometry.py --selftest; bash tools/mado-verify.sh --selftest; the census
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`. Write %(W)s/w1/ExecHarmBase/baseline.md
(the L1 compares the data tip against it).""")
seat("ExecXkbCompile", "executor",
     "Probe: can a read-only tool predict FALLBACK by compiling the declared names with the host's libxkbcommon?",
     """Using ctypes on the host's libxkbcommon (1.13.2; xkb_context_new, xkb_keymap_new_from_names / _names2, xkb_keymap_layout_get_name), compile:
the host's names (br, compose:caps), us, `br,us`, a typo `zz`, a valid layout with an invalid variant (`br` + `nodeadkeys`?), an invalid option. Report
which compile, the layout names they yield (compare with `active_keymap` in `hyprctl devices -j`), and whether failing names exactly match Hyprland's
fallback path (%(W)s/fetch/Hyprland-IKeyboard.cpp:96-116: names first, then reset to us). Conclude whether a future `--xkb` mode could turn the entry's
'compile failure not observed' limit into a check, and its risks (environment XKB_CONFIG_ROOT, include paths). Write %(W)s/w1/ExecXkbCompile/report.md.""")
seat("ExecDataRehearsal", "executor",
     "Pre-data dress rehearsal: the full data tree in scratch, every counter and gate on it.",
     """In a scratch clone at %(F)s: install """ + REF + """ as tools/mado-devices.py, apply %(W)s/l1-draft/build-pos.py, commit. Then run on that commit:
both C1/C2 counters, quality/check-axis-scores.py (expect STALE for the README/QUALITY change window - report exactly which rows), the census validate
`--file <clone>/corpus/SOURCES.md` (paste every warning; count W04 duplicates and name the held rows), tools/*.py --selftest for every tool with a
selftest, and quality/check-session-material.py on the clone (does the new live receipt or the entry trip it?). Write %(W)s/w1/ExecDataRehearsal/report.md
listing every red item with the fix the L1 must make before data.""")
seat("ExecC1Separability", "executor",
     "Separability of C1 and C2 shown on scratch trees (both directions).",
     """Build two scratch trees from %(F)s: TOOL-ONLY (reference installed as tools/mado-devices.py, nothing else) and DATA-ONLY (build-pos.py applied,
no tool). Score both with both counters (commands in context). Expected: TOOL-ONLY C1 MET / C2 0/1; DATA-ONLY C1 MISSED / C2 1/1. Report the four
final lines verbatim and any cross-read either counter does. Write %(W)s/w1/ExecC1Separability/report.md.""")

# ------------------------------------------------------------ critics (11)
seat("CritC1Cheat", "critic",
     "Break PRED-C1-r46: cheat tools that reach TARGET_MET without implementing the contract.",
     """Write cheat tools (each a different idea: sandbox/environment detection beyond the A/B variation, a fixture-shape detector, a tool that handles
only the generator's distribution, reading /proc for the parent's argv, timing) and score each with `""" + C1 + """`. Report each MET cheat, the clause
that should have caught it and a tightening that keeps the reference MET. Write %(W)s/w1/CritC1Cheat/report.md with the files.""")
seat("CritC1Narrow", "critic",
     "Break PRED-C1-r46 by narrowing: a tool wrong on real configs yet MET.",
     """Find semantics the 90 fixtures + 150 generated cases do NOT pin: for each docstring rule of """ + REF + """, make a variant that breaks only
that rule and score it (`""" + C1 + """`, 3 nonces). Every MET variant is a hole: name the rule, give a fixture that would catch it. Write
%(W)s/w1/CritC1Narrow/report.md.""")
seat("CritToolSemantics", "critic",
     "Attack the C1 contract against Hyprland/hyprlang source: where does the reference's model disagree with the pins?",
     """Read """ + REF + """'s docstring and %(W)s/fetch/ (InputManager.cpp applyConfigToKeyboard and setPointerConfigs, ConfigManager.cpp
getConfigValueSafeDevice/getDeviceString/deviceConfigExists, IKeyboard.cpp setKeymap, HyprCtl.cpp devicesRequest, hyprlang-config.cpp configSetValueSafe
and parseLine). For each docstring sentence: supported / wrong / unpinned, with the pin line. Specifically probe: when does applyConfigToKeyboard run for
a virtual keyboard relative to its keymap event; can a keyboard print rules after a reload that differ from config even when not virtual; does
`enabled = false` hide a keyboard from the dump; does `kb_file` change what is printed; is FALLBACK exactly us + 4 empties. Write
%(W)s/w1/CritToolSemantics/report.md.""")
seat("CritC2Forgery", "critic",
     "Break PRED-C2-r46: forged or hollow revisions the counter admits.",
     """Starting from the positive control (recipe in context), craft revisions that the counter admits but that a reader would reject: false sentences
next to true locators, a census contradicted in words, a decision table naming no id, a row with a misleading scope, a Gate quote that is true but
irrelevant, a README row pointing elsewhere, a duplicate-URL row abuse. Score each (`""" + C2 + """`). Report each admitted forgery, whether the
registration declares it a residual, and a tightening. Write %(W)s/w1/CritC2Forgery/report.md.""")
seat("CritEntryContent", "critic",
     "Read every sentence of the C2 draft entry against the pins.",
     """For each sentence of %(W)s/l1-draft/entry.md: supported (pin:line, quote) / wrong / unpinned. Pay attention to: "47 values", the three bracket
spellings, "the current device is forgotten when the last category closes", "a flat device:kb_layout outside a block has no device to land on", the
"did not change" skip, the kb_file order, the fallback, virtual-keyboard naming when misc:name_vk_after_proc is off, the duplicate suffix, the wiki
quote. List missing facts a reader needs (e.g. what `main` means in the dump). Write %(W)s/w1/CritEntryContent/report.md.""")
seat("CritClaimSizing", "critic",
     "Attack the claim sizing of the registration against prompt section 9 rules.",
     """Read %(W)s/registration.md and the prompt rules in /home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-46.md (section 6 item 9). For each claim:
can a do-nothing control reach the target; are there universal clauses the counter does not enumerate; is the axis named by the surface; is the
predicate the same sentence in registration, counter code and receipt label; are C1 and C2 really separable and on distinct axes. Number your findings
F1..Fn with severity. Write %(W)s/w1/CritClaimSizing/report.md.""")
seat("CritPremise", "critic",
     "Attack the premise: is the input-device ground really new to the lane, and is the tool useful?",
     """Search the lane corpus at %(B)s (git grep, read) for anything that already covers per-device input config, keyboard layout resolution or
`hyprctl devices`: config-health-report-r3.md, hyprctl-verification-layer.md, hyprland-config-plane.md, SKILL.md tables. Decide whether C2's ground is
new (cite) and whether C1 answers a question `hyprctl getoption input:kb_layout` or `hyprctl devices -j` alone cannot. Also: does omarchy offer
anything equivalent (grep ~/.local/share/omarchy/bin for 'devices -j' / kb_layout, read-only)? Write %(W)s/w1/CritPremise/report.md.""")
seat("CritRegistration", "critic",
     "Attack the registration's factual statements.",
     """Check every factual statement in %(W)s/registration.md against the repo and the host: base hash and ahead/behind, host versions, keyboard and pointer
counts, 'one input block and no device block', the ground grep, 'registry tops at S315', 'two cross-scope URL repeats' (count every held row whose URL
equals a pin URL: grep the registry), control counts in receipts/ctl-c1.txt and ctl-c2.txt, fixture count. List each wrong or imprecise statement with the
command that shows the truth. Write %(W)s/w1/CritRegistration/report.md.""")
seat("CritW2ToolSemantics", "critic",
     "Round-45 w2: attack the landed tools/mado-monitors.py contract against the round-45 pins with fresh eyes.",
     """Read the docstring of `git -C %(L)s show %(R45T)s:tools/mado-monitors.py` and %(L)s/.ufo/waves/round-45/fetch/. Find semantics the round-45 w1 did
not check (see %(L)s/.ufo/waves/round-45/w1/CritToolSemantics.md and ExecParseOracle.md for what was checked): monitorv2 interplay, `desc:` with trailing
spaces, transform values on the mirror line, a rule for a disabled output re-enabled at runtime, reserved areas, `auto-left` positions. Build a scratch
case per finding and run the landed tool. Write %(W)s/w1/CritW2ToolSemantics/report.md.""")
seat("CritW2Entry", "critic",
     "Round-45 w2: read the landed monitor-rule entry against its pins.",
     """For each sentence of `git -C %(L)s show %(R45T)s:corpus/knowledge/hyprland-monitor-rule-r45.md`: supported (pin:line in
%(L)s/.ufo/waves/round-45/fetch/) / wrong / unpinned. Count each class. Flag any sentence the round-45 closure did not sample. Write
%(W)s/w1/CritW2Entry/report.md.""")
seat("CritW2Gate", "critic",
     "Round-45 w2: attack quality/check-session-material.py (false negatives and false positives).",
     """Read %(L)s/quality/check-session-material.py. Craft committed-file shapes it misses (a clients dump with a renamed key, YAML, a CSV ps table,
`hyprctl clients` plain text, a monitors dump with serial in prose, base64) and shapes it wrongly flags (synthetic fixtures, documentation examples).
Run it on a scratch clone with each planted file. Report misses and false flags with the file content shape (no real session material). Write
%(W)s/w1/CritW2Gate/report.md.""")

# ------------------------------------------------------------ reviewers (6)
seat("RevC1Counter", "reviewer",
     "Review the C1 counter code for bugs and unfair passes/fails.",
     """Review %(L)s/quality/counters/c1-r46-devices.py line by line: fixture loading and pinning, placeholder substitution (could {A}..{D} substitute
inside expected lines wrongly; json.dumps escaping vs substituted names), BIG_CONFIG/BIG_DUMP handling, the stdin path, env A/B, sandbox hides, the
generated-case alignment with the model (does using the model to align reported names leak anything to the tool?), timeouts, the selftest parse, the
final verdict expression. Run it to confirm each suspected bug. Write %(W)s/w1/RevC1Counter/report.md.""")
seat("RevC2Counter", "reviewer",
     "Review the C2 counter re-cut against the round-45 v2 counter it came from.",
     """Diff %(L)s/quality/counters/c2-r46-input-device-entry.py against %(L)s/quality/counters/c2-r45-monitor-entry-v2.py. Check: every changed constant,
the new host_census (each regex matches exactly once in its pin; what if a pin changes format), the 28 SURFACES (anchor unique, keyword sensible), the
verdict-token list, any r45 leftover. Run the counter on the positive control and on 3 single-clause breakages of your own. Write
%(W)s/w1/RevC2Counter/report.md.""")
seat("RevRows", "reviewer",
     "Review the ten draft rows S316-S325 against CORPUS.md and the census.",
     """Read ROWS in %(W)s/l1-draft/build-pos.py and /home/vgpnk/Projects/shokunin/CORPUS.md (SOURCES.md contract). For each row: 11 cells, tier, kind,
scope distinct from held rows on the same URL (S173, S182, S215, S162, S303, S158, S307 - read them), anchor ranges inside the receipt and pointing at
what `teaches` says (open the lines), teaches supported. Decide for each repeat URL whether a new row or extending the held row's used-by is the
CORPUS-correct form, with the rule text. Write %(W)s/w1/RevRows/report.md.""")
seat("RevW2Rows", "reviewer",
     "Round-45 w2: re-open rows S302-S315 at their sources.",
     """For each of S302-S315 in %(L)s/corpus/SOURCES.md: re-fetch the URL today, sha256 it, compare with the row and with
%(L)s/.ufo/waves/round-45/receipts/fetch-sha256.txt; locate the round-45 Gate quote (%(L)s/corpus/lessons/round-45.md `## Gate`) at its locator; check
the row's anchor ranges and teaches. Report per row: bytes equal y/n, quote found y/n at line, teaches supported y/n. Write %(W)s/w1/RevW2Rows/report.md.""")
seat("RevW2Counters", "reviewer",
     "Round-45 w2: review the round-45 v2 counters for residual cheats against the landed bytes.",
     """Review %(L)s/quality/counters/c1-r45-monitors-v2.py and c2-r45-monitor-entry-v2.py against their declared residuals
(%(L)s/.ufo/waves/round-45/registration-v2.md). Find any undeclared hole and demonstrate it on a scratch clone of %(R45T)s (one cheat per hole). Write
%(W)s/w1/RevW2Counters/report.md.""")
seat("RevPrivacyRound", "reviewer",
     "Privacy review of this round's committed and to-be-committed evidence.",
     """Review %(W)s/ (receipts/, l1-draft/, fetch/) and, as they appear, the seat dirs under %(W)s/w1/: any window title, monitor serial or description,
process table, home listing, token, or anything else SKILL.md rule 4 (grep -n 'shape-only' %(L)s/SKILL.md) forbids. Rule explicitly on whether input
device product names (e.g. a security-key model) and an input-method process name in `hyprctl devices -j` are session material under the lane's own
rule, with your reasons. Write %(W)s/w1/RevPrivacyRound/report.md.""")

# ------------------------------------------------------------ mutation-testers (4)
seat("MutTool", "mutation-tester",
     "Mutation-test the C1 reference against the frozen fixtures + selftest: survivors = unpinned semantics.",
     """Generate >= 60 mutants of """ + REF + """ (operators, constants, branch deletions, comparison swaps, off-by-one in comment/bracket parsing) in
scratch; for each run its selftest and the fixtures (load quality/counters/c1-r46-fixtures.json and replay them in-process via report(), substituting
placeholders with the counter's names(46)). List survivors with the semantic they change and a fixture that would kill each. Write
%(W)s/w1/MutTool/report.md.""")
seat("MutC1Counter", "mutation-tester",
     "Mutation-test the C1 counter: which counter mutants still separate reference from controls?",
     """Mutate %(L)s/quality/counters/c1-r46-devices.py in scratch copies (drop a clause, weaken a comparison, skip env B, skip the nonce run, drop
stderr check, accept any rc) and run each mutant against the reference and 4 controls of %(W)s/ctl/run-c1-controls.py (V03, V07, V13, STUB: build them
the way that script does). Report which mutants go undetected by the control set. Write %(W)s/w1/MutC1Counter/report.md (summary only; no file > 1 MB).""")
seat("MutC2Counter", "mutation-tester",
     "Mutation-test the C2 counter against the 15 registered controls.",
     """Mutate %(L)s/quality/counters/c2-r46-input-device-entry.py in scratch (one clause weakened per mutant: census regex, surface width, quote
uniqueness, T1-T5) and run %(W)s/ctl/run-c2-controls.py logic against each mutant (copy the runner, point it at the mutant). Report surviving mutants and
the control that would kill each. Write %(W)s/w1/MutC2Counter/report.md (summary only).""")
seat("MutW2Tool", "mutation-tester",
     "Round-45 w2: mutation-test the landed tools/mado-monitors.py against its counter's fixtures.",
     """Generate >= 50 mutants of `git -C %(L)s show %(R45T)s:tools/mado-monitors.py` and score each against the round-45 v2 counter's fixtures (run the
counter with --nonce 45 on a scratch clone per mutant, or replay its FIXTURES in-process). List survivors and a fixture per survivor. Write
%(W)s/w1/MutW2Tool/report.md (summary only).""")

# ------------------------------------------------------------ falsification probes (4; critic role: labrat is not a swarm role)
seat("LabFloatFormat", "critic",
     "Hypothesis: Python '%%.2f' of an f32-rounded scroll factor equals std::format(\"{:.2f}\", float) for every value the tool can see.",
     """Falsify with a C++ program over every 3-decimal value in [0, 100] and 10^5 random floats: compare std::format("{:.2f}", f) with Python
'%%.2f' %% struct-roundtrip(f). Report the first counterexample or 'not falsified' with counts. Write %(W)s/w1/LabFloatFormat/report.md.""")
seat("LabVirtualRules", "critic",
     "Hypothesis: a virtual keyboard's printed rules are the config names at its creation and never change after its client's keymap arrives.",
     """Trace in the pins (%(W)s/fetch/Hyprland-InputManager.cpp newVirtualKeyboard/setupKeyboard/applyConfigToKeyboard,
Hyprland-VirtualKeyboard.cpp, Hyprland-IKeyboard.cpp setKeymap, Hyprland-protocols-VirtualKeyboard.cpp) the order of events; fetch any other file you
need at efb50993 (record URL + sha256). Falsify or support the hypothesis with line citations; say what a reload does. Write
%(W)s/w1/LabVirtualRules/report.md.""")
seat("LabDupNames", "critic",
     "Hypothesis: a device block named `foo` never applies to a device named `foo-1`, and names are matched byte-exactly.",
     """Using the host hyprlang library (C++, as in the context's oracle idea) or the pins alone, test exact matching of special-category keys
(getSpecialConfigValuePtr with a key, specialCategoryExistsForKey) for `foo` vs `foo-1`, case, trailing space. Also read getNameForNewDevice
(%(W)s/fetch/Hyprland-InputManager.cpp:2119-2131): which device of two identical ones gets the suffix (order of plug). Report. Write
%(W)s/w1/LabDupNames/report.md.""")
seat("LabKbFile", "critic",
     "Hypothesis: with a readable kb_file the dump still prints the declared names, and an unreadable kb_file falls back to the names.",
     """Support or falsify from %(W)s/fetch/Hyprland-IKeyboard.cpp:60-145 and Hyprland-InputManager.cpp:1226-1286 with line citations; consider
absolutePath() relative to the config path and the 'did not change' short-circuit. Say whether the C1 contract's kb_file handling (prints kb_file=set,
compares names) is right. Write %(W)s/w1/LabKbFile/report.md.""")

# ------------------------------------------------------------ scouts (4)
seat("ScoutRecheck", "scout",
     "Re-fetch every round-46 pin from upstream today and compare; check upstream main for changes.",
     """For each file in %(W)s/receipts/fetch-sha256.txt: re-fetch its URL (see context), sha256-compare. Then fetch the same paths at Hyprland main and
hyprlang main (GitHub API or raw) and report whether applyConfigToKeyboard, the device category, devicesRequest and the virtual naming changed, and what
the Lua config offers for per-device input (search the main tree for `device` in src/config/lua). This feeds the entry's recheck line. Write
%(W)s/w1/ScoutRecheck/report.md.""")
seat("ScoutFrontier", "scout",
     "Other sources for the input-device plane worth a row (opened, not assumed).",
     """Find upstream issues/discussions/docs about per-device keyboard layouts not applying, device names in device blocks, scroll_factor per device,
virtual keyboard layouts (fcitx5) on Hyprland 0.5x (GitHub hyprwm/Hyprland issues and discussions, hyprland-wiki history). Open each candidate, give URL,
date, a <= 25-word located quote, and an admit/refuse verdict for this entry with reason (PROVINCE.md scope). Write %(W)s/w1/ScoutFrontier/report.md.""")
seat("ScoutShokuknow", "scout",
     "Assimilation fit (section 10): read merge/mado for input-device material, read-only.",
     """Read %(P)s/MERGE-REPORT.md and the staged knowledge files it lists that touch input, keyboards, focus or devices (paths under %(P)s/knowledge/).
For each: does it hold anything the C2 entry needs or contradicts (cite lines), is it in PROVINCE (/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md),
admit/refuse with reason and flip condition. Never run a campaign tool; never write under /home/vgpnk/Projects/shokuknow. Write
%(W)s/w1/ScoutShokuknow/report.md.""")
seat("ScoutOmarchyInput", "scout",
     "How omarchy ships and changes input config (read-only).",
     """Read ~/.local/share/omarchy/default/hypr/input.conf and grep ~/.local/share/omarchy/bin and migrations for kb_layout, kb_options, device {,
scroll_factor, `devices -j` (read-only; never run them). Report what omarchy writes, where the user's input.conf overrides it, and which omarchy commands
would make the C1 tool report DIFFER or STALE_BLOCK. Write %(W)s/w1/ScoutOmarchyInput/report.md.""")

# ------------------------------------------------------------ connectors (5)
seat("ConnCrossClaim", "connector",
     "Cross-claim pattern scan: do C1 and C2 lean on the same unverified assumption?",
     """Read the registration, the reference contract and the draft entry. List every factual assumption both rely on (e.g. FALLBACK = us + empties,
the set-by-user rule, the virtual prefix) and which pin line supports it; flag any assumption that only the reference (not a pin) carries. Also compare
with the round-45 pair (mado-monitors + monitor-rule entry): which round-45 w1 failure classes would recur here. Write %(W)s/w1/ConnCrossClaim/report.md.""")
seat("ConnSiblings", "connector",
     "Adjacency: sibling lanes touching the input-device plane.",
     """Read the PROVINCE.md of sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin/ (read-only) and grep their corpora for keyboard layout,
xkb, input devices, hyprctl devices. Report any overlap with mado's C2 entry, who owns what, and contested scope to name in the report. Write
%(W)s/w1/ConnSiblings/report.md.""")
seat("ConnLessons", "connector",
     "Recurring mistakes across rounds 43-45 and whether round 46's freeze repeats them.",
     """Read %(L)s/corpus/lessons/round-43.md .. round-45.md `## Mistakes` and the three spot-checks. Group the mistakes by class; for each class say whether
round 46's freeze (registration, counters, controls, receipts) repeats it, with the file:line. Write %(W)s/w1/ConnLessons/report.md.""")
seat("ConnCalibration", "connector",
     "Calibration count: SCORECARD/SHONEN statements vs repo state at the base.",
     """Take the last three SCORECARD sections (Round 43-45) and SHONEN.md; for each verifiable statement (counts, hashes, receipts named, capabilities
rows) check it against the repo at %(B)s with a command. Count mismatches; list each with the command that shows the truth. Write
%(W)s/w1/ConnCalibration/report.md.""")
seat("ConnToolFamily", "connector",
     "Consistency of the live-state tool family and considerthese 2026-10-26 proposal 2 (a ledger of live-state tools).",
     """Compare the reference """ + REF + """ with tools/mado-monitors.py, mado-geometry.py, mado-globals.py, mado-eventq.py, mado-options.py: argument
forms, setup-error lines, exit maps, output line prefixes, read-only boundaries. List inconsistencies the new tool introduces (fix proposals) and draft
the ledger table (tool | question it answers | last live run receipt | verdict) from committed receipts only. Write %(W)s/w1/ConnToolFamily/report.md.""")

# ------------------------------------------------------------ scribes (9)
seat("ScrEntryDraft", "scribe",
     "Improve the C2 draft entry's weakest prose for the L1 to merge.",
     """Read %(W)s/l1-draft/entry.md and the pins. Draft improved text for: the 'Reading a DIFFER or a FALLBACK' section (runtime keyword, a file not
passed, source lines, typo, enabled=0), a short 'how to run the join on your host' paragraph (the exact read-only commands), and the Limits. Every
sentence that states a compositor behaviour carries a <= 30-line locator `<receipt>:<a>-<b>` you verified by grep -n. Do not add S### ids. Write
%(W)s/w1/ScrEntryDraft/sections.md.""")
seat("ScrReadme", "scribe",
     "Draft the corpus/README.md index row and Frontier bullet for the new entry.",
     """Read %(L)s/corpus/README.md (index row shape: the round-45 row; `## Frontier`). Draft the index row for knowledge/hyprland-input-devices-r46.md
(three cells, third = `S316-S325`) and a Frontier bullet: what the round moves (input-device plane: per-device XKB names and pointer scroll factor), what
stays open (XKB compile, repeat/numlock/libinput settings not in the dump, Lua config). Write %(W)s/w1/ScrReadme/readme.md.""")
seat("ScrSkill", "scribe",
     "Draft the SKILL.md section and the PROVINCE.md refinement for the new tool.",
     """Read the round-45 SKILL.md section (grep -n 'Monitor rule versus running output' %(L)s/SKILL.md) and the round-45 PROVINCE refinement. Draft the
round-46 equivalents for tools/mado-devices.py: a decision table (verdict -> meaning -> next read-only step), the exit map, the exact host command, the
read-only boundary (reads, writes, no process/socket). Write %(W)s/w1/ScrSkill/skill.md.""")
seat("ScrLessonGate", "scribe",
     "Draft corpus/lessons/round-46.md: Gate, registry changes, search log.",
     """Draft %(W)s/w1/ScrLessonGate/round-46.md with: `## Gate` (candidates considered: the ten pins; rejected candidates such as the hyprland-wiki at
main (Lua era), Keyboard.cpp, IKeyboard.hpp; held rows on the same URLs and why new rows; admitted/rejected with reasons; one GATE line per cited id in
the exact counter format produced by build-pos.py; each new row's URL, access date 2026-10-26, <= 25-word located quote - verify each quote by grep
against %(W)s/fetch/), `## Registry changes` (old->new), `## Search log` (question, where searched, identified/screened/included/excluded, stop rationale).
Leave `## Mistakes` to ScrMistakes.""")
seat("ScrMistakes", "scribe",
     "Mine the mistakes for corpus/lessons/round-46.md ## Mistakes.",
     """From %(L)s/corpus/lessons/round-45-verifier-spotcheck.md section 6 (D1-D6) and this round's freeze (the registration said 'two cross-scope URL
repeats' - check how many there are; the C2 control harness asserted a single URL occurrence and stopped before scoring; the pre-freeze C1 control V03
met the predicate), draft M46-n rows: class (CORPUS.md vocabulary: vacuous, survivor, stale-premise, reference-drift, number-drift, scope, attribution,
landing, provider) | evidence pointer | captured-by (criterion or rule, or none) | fix (and how the fix is shown able to fail). Propose QUALITY.md criteria
(next number after the last in %(L)s/corpus/QUALITY.md) each citing its lesson row. Write %(W)s/w1/ScrMistakes/mistakes.md.""")
seat("ScrSerialCorrection", "scribe",
     "Round-45 closure D2: the M45-2 correction text (no serial value anywhere).",
     """Draft an appended correction for %(L)s/corpus/lessons/round-45.md M45-2 (append-only, in a round-46 lesson block): the serial sits in three held
entries (config-health-report-r3.md:149, hyprctl-verification-layer.md:153, hyprland-config-plane.md:184) and 21 wave files under .ufo/waves/round-32/
and round-37/ (closure D2) - verify the counts with `git grep -c -F` using a shell variable read from `hyprctl monitors all -j`, printing counts and paths
only. State that removal from pushed history is the operator's decision. Write %(W)s/w1/ScrSerialCorrection/correction.md.""")
seat("ScrErrata", "scribe",
     "Round-44 D7 / round-45 D6: errata for the round-44 w2/ConnCalibration mismatches; round-45 D4/D5 notes.",
     """Read %(L)s/.ufo/waves/round-44/w2/ConnCalibration.md; draft one erratum per mismatch (append-only text for SCORECARD, with the command that shows the
truth, verified by you). Draft the D4 note (a digest line for .ufo/waves/round-45/w1/MutC1Counter/results.json: sha256, size, what summary.txt holds;
the file itself stays out of git) and the D5 note (w1-results.json of round 45 holds output:null for 41 seats; the seat .md files are the record).
Write %(W)s/w1/ScrErrata/errata.md.""")
seat("ScrRoutedAges", "scribe",
     "considerthese 2026-10-26 proposal 3: an age count per routed defect.",
     """Read %(L)s/considerthese/2026-10-26.md (proposal 3) and the routed-defect sections of the spot-checks round-38 .. round-45
(%(L)s/corpus/lessons/round-*-verifier-spotcheck.md). Build a table: defect (short) | first routed (round, file:line) | rounds open | closed in (round,
commit) or OPEN. Count OPEN items and their ages. Propose one QUALITY.md criterion that would make the age visible each round. Write
%(W)s/w1/ScrRoutedAges/ages.md.""")
seat("ScrScorecard", "scribe",
     "Draft the SCORECARD Round 46 section, the capabilities row and the LOG.md entry skeleton.",
     """Read the Round 45 sections of %(L)s/SCORECARD.md and %(L)s/LOG.md. Draft the Round 46 equivalents for C1/C2 with placeholders ONLY for values
that depend on the data commit (mark them <AFTER>); fill everything already known from %(W)s/registration.md and receipts/ (before values, counting
commands, controls verdicts). Include the capabilities row text and a Planned (round 47) list from the round's open items. Write
%(W)s/w1/ScrScorecard/draft.md.""")

# ------------------------------------------------------------ sentinels, simplifier, revenger (5)
seat("SentTool", "sentinel",
     "Safety review of the C1 reference, the counters and the round's host reads.",
     """Review """ + REF + """ and both round-46 counters: any subprocess/socket/env/network path in the tool; output injection (names with newlines or
quotes in the dump); path handling (symlinks, FIFOs, /proc files as --config); resource exhaustion (1 MiB cap, continuation loops, regex backtracking);
counters' scratch handling (rmtree targets, --work outside scratch, /tmp use - prompt section 7 item 4); the fake PATH binaries; the live receipt content.
Rank by severity with repro. Write %(W)s/w1/SentTool/findings.md.""")
seat("SentW2Privacy", "sentinel",
     "Round-45 w2: privacy sweep of the round-45 committed evidence.",
     """Sweep every file committed under %(L)s/.ufo/waves/round-45/ at %(R45T)s for session material (titles, serials, descriptions, process tables, home
listings, tokens). Print paths, line numbers and the class only - never the value. Compare with what quality/check-session-material.py reports at that
revision. Write %(W)s/w1/SentW2Privacy/report.md.""")
seat("SentHost", "sentinel",
     "Audit this wave's instructions and the round's commands for any host mutation risk.",
     """Read %(W)s/w1-spec.json (this wave) and %(W)s/registration.md: list every host command a seat is told to run; flag any that could mutate the
compositor, input devices or host packages (e.g. hyprctl verbs, libinput debug tools, udevadm trigger) and any instruction that contradicts the context's
safety rules. Write %(W)s/w1/SentHost/report.md.""")
seat("SimpContract", "simplifier",
     "Dead weight in the C1 contract and code.",
     """For each sentence/branch of """ + REF + """ decide whether some input makes the output depend on it (build the pair, run the reference) or it is
dead/redundant (e.g. the `bracket` branch for unknown fields, `cur is False` paths, FLT_MIN check vs isinf, dump_names on non-list values). List dead or
redundant parts with the proof and the exact deletion text. Write %(W)s/w1/SimpContract/dead-weight.md.""")
seat("RevengerHyprlang", "revenger",
     "Reverse-engineer hyprlang 0.6.8's special-category behaviour where the source is murky.",
     """From %(W)s/fetch/hyprlang-config.cpp (configSetValueSafe :270-520, parseLine :669-912, specialCategoryExistsForKey :1112) reconstruct the exact state
machine for `device` categories: currentSpecialCategory / currentSpecialKey transitions on `{`, `}`, `name =`, bracket keys, dynamic creation with key
"0". Confirm with the host library (a C++ probe) the three murky cases: block whose first key is not name (which device name results; do later keys land
there), a rename via second `name =`, and `device[X]:name = Y`. Write %(W)s/w1/RevengerHyprlang/report.md.""")

n = len(items)
assert n == 66, n
assert len({i["name"] for i in items}) == n
print(n, dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-46/w1", "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
