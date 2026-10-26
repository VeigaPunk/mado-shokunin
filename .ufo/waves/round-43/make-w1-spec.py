#!/usr/bin/env python3
"""Generates .ufo/waves/round-43/w1-spec.json (38 seats, v1 wave: build + first falsifiers).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-43"
W42 = LANE + "/.ufo/waves/round-42"
FREEZE = "b2e2efd6e268920d31f3c32cf52dc097dd6e1d22"
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
mado round 43 (hyaku run 8, 2026-10-26), inline v1 wave w1 of two (38 seats: build + first falsifiers). Lane repo: %(L)s
Claims are FROZEN at %(W)s/registration.md (freeze commit %(F)s, base %(B)s) - read it first. Two claims:
- C1 operability (capability acquisition): a new tool `tools/mado-geometry.py` - a read-only join of the window-rule sizes in Hyprland config files
  (`windowrule = size W H, match:class RX`) and the sizes the compositor reports in one `hyprctl clients -j` dump:
  `hyprctl clients -j | mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf`; per matched client AGREE / DIFFER / TILED / BADSIZE,
  `--selftest`. Frozen counter quality/counters/c1-r42-geometry.py (PRED-C1-r42; its docstring IS the tool's contract): target fixtures=37/37
  TARGET_MET; base 0/37 (tool absent). Reference control (NOT the deliverable): %(W42)s/c1/ctl-ref-tool.py.txt (37/37 MET, selftest 73/73).
  Controls: %(W42)s/ctl/run-c1-controls.py (re-run at the round-43 base; receipt %(W)s/receipts/ctl-c1.txt: controls=46 (3 do-nothing, 5 cheats, 38 mutants; REF and BASE-absent are anchors), CTL_C1 VERDICT PASS, 0 of 47 non-reference runs reach MET, the reference does).
- C2 coverage (sourced; assimilation of the gkeep-geometry theme of the shokuknow package): corpus/knowledge/hyprland-gkeep-geometry-r43.md - what determines
  the size of the host's gkeep window, end to end (host rule text, RE2 FullMatch, size/float effects, floating algorithm, target/window storage, the animated variable
  behind `hyprctl clients -j` size, the client's own request, the host census). Frozen counter quality/counters/c2-r43-gkeep-entry.py (PRED-C2-r43, clauses a-i);
  target admitted=1/1; base 0/1. Controls: %(W)s/ctl/run-c2-controls.py (the round-42 runner with the round constants; receipt %(W)s/receipts/ctl-c2.txt: CTL_C2 controls=74 correct=74/74 (control P admitted under the real and the pin-patched counter, 72 mutants and forgeries rejected)).
Pre-fetched receipts (the L1 fetched them 2026-10-26, byte-identical to the round-42 pins except the two re-captured own-work receipts; each seat re-opens what it relies on) in %(W)s/fetch/ with ids reserved for the entry's rows:
  S290 Hyprland-RegexMatchEngine.cpp, S291 Hyprland-WindowRuleApplicator.cpp, S292 Hyprland-DefaultFloatingAlgorithm.cpp, S293 Hyprland-Target.cpp,
  S294 Hyprland-WindowTarget.cpp, S295 Hyprland-GeometricMovableAnimated.cpp, S296 Hyprland-HyprCtl.cpp (all hyprwm/Hyprland tag v0.56.2 commit
  efb50993780079460b0cbed1363e2166a2de1d9f, raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/<path>), S297 host-gkeep.conf (own-work: byte copy of
  ~/.config/hypr/gkeep.conf), S298 host-clients-r43.json (own-work: `hyprctl clients -j` reduced to class/size/floating/mapped/address/at/monitor),
  S299 gkeep-ui-excerpt.py (own-work: lines 446-495 of ~/Projects/gkeep/gkeep/ui.py at gkeep 133b867). sha256 list: %(W)s/receipts/fetch-sha256.txt.
  Ids S300+ are free for rows a seat proposes. The lane registry tops at S289 (226 rows); new rows are append-only, 11 columns, status `mined`, opened 2026-10-26.
Provisional facts (from the L1; every seat re-derives what it relies on, none is evidence until re-opened):
- host Hyprland 0.56.2; the host's gkeep rule file declares float, center and `size 420 500` for class `^(org.omarchy.gkeep)$`; no gkeep window is open now
  (`hyprctl clients -j` has 4 clients: chromium, grok-bot, zcode, Alacritty; all tiled).
- the rule match engine is `re2::RE2::FullMatch` (anchored) with a `negative:` prefix; `static_.size` is an expression (SExpressionVec2) consumed in the
  floating branch of the default floating algorithm; `hyprctl clients -j` `size` is `w->size(GEOMETRIC_GOAL)` - the animation GOAL, not the current value.
- the staged package is %(P)s (READ-ONLY; never run a campaign tool there; read bytes only); its gkeep files: gkeep-geometry-unobservable-r8, gkeep-rendered-geometry-chain-r9,
  gkeep-size-rule-application-r10, gkeep-size-to-real-size-r11, gkeep-observation-route-r11, gkeep-client-size-request-r12, gkeep-rendered-geometry-record-r13/-r14,
  gkeep-geometry-never-recorded-r15, glyph-and-geometry-r31, gkeep-element-rules-r30 (under knowledge/corpus/knowledge/). Staged ids S203-S349 collide with the lane's.
- PROVINCE.md excludes localized (Chinese/Japanese) documentation-channel material.
- history: round 42 froze these instruments (freeze 809dc2c) and stopped before its wave was spawned (no seat ran, no data). Round 43 re-registers C1 UNCHANGED
  (PRED-C1-r42, its counter, reference and controls stay under round-42 paths) and C2 with ROUND CONSTANTS ONLY (PRED-C2-r43: base, paths, dates, two re-captured
  own-work pins). The round-42 non-author closure (%(L)s/corpus/lessons/round-42-verifier-spotcheck.md section 6) routed: wrong locators in the round-42 prose
  (`Hyprland-HyprCtl.cpp:394-395,412-413` is really :427-428 and :448; `Hyprland-RegexMatchEngine.cpp:10-16` is really :7-8 and :16), a control tally stated three ways,
  a SHONEN pointer to an uncommitted run, no round-42 lesson. The round-42 gkeep excerpt header said `lines 446-495` of a 488-line file and carried one extra blank line;
  the round-43 excerpt is regenerated with `sed -n '446,$p'` and its header says `446-488 (end of file)`.
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin except as your task names), sibling lanes,
  templates/, scripts/, MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout, or the lane's jj/git index.
  Never run mutating git/jj anywhere in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git
  (log/show/diff/status/rev-parse/ls-tree/cat-file) is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus any explicit destination your task names. Never edit an
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
    for k, v in (("%(L)s", LANE), ("%(W42)s", W42), ("%(W)s", W), ("%(F)s", FREEZE), ("%(B)s", BASE),
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


CNT = "%(L)s/quality/counters/c1-r42-geometry.py"
SCORE = "cd %(L)s && C1R42_TMP=%(S)s/<YourSeatName> python3 -I quality/counters/c1-r42-geometry.py --repo . --rev %(F)s --tool <your file>"

# ------------------------------------------------------------ executors (12)
seat("ExecIndepA", "executor",
     "Differential implementation for C1 (regex style): an independent tool written from the contract only.",
     """WITHOUT reading %(W42)s/c1/ctl-ref-tool.py.txt, read only the docstring of %(L)s/quality/counters/c1-r42-geometry.py (the contract) and write your own
`mado-geometry.py` in %(W)s/w1/ExecIndepA/ (stdlib only; selftest k==n>=50 printing `MADO_GEOMETRY_SELFTEST: k/n passed`, with teeth: a flipped comparison in your
parser must fail it). Use `re` for line and field grammar. Then score it: `""" + SCORE + """` and report every failing fixture line verbatim (a failing fixture is a finding about
the contract text or the counter unless you show your file is wrong). Then diff your behaviour against the reference on 300 random cases (import the counter with
importlib, never execute main; use its gen_texts/gen_clients/model_out) and list every disagreement with the contract sentence that decides it.""")
seat("ExecIndepB", "executor",
     "Differential implementation for C1 (hand-parser style): an independent tool written from the contract only.",
     """WITHOUT reading %(W42)s/c1/ctl-ref-tool.py.txt, read only the docstring of %(L)s/quality/counters/c1-r42-geometry.py (the contract) and write your own
`mado-geometry.py` in %(W)s/w1/ExecIndepB/ (stdlib only; selftest k==n>=50, summary line `MADO_GEOMETRY_SELFTEST: k/n passed`, with teeth). Parse lines with explicit string
operations (split/strip/startswith) and character-class loops; use `re` only to compile and fullmatch the rule's REGEX against a class. Score it:
`""" + SCORE + """`; report every failing fixture verbatim and which contract sentence you misread or which sentence is ambiguous. Then differential-fuzz it against the counter's
model_out (importlib; >= 500 generated cases plus 200 of your own adversarial cases) and list every disagreement class with a minimised input.""")
seat("ExecIndepC", "executor",
     "Differential implementation for C1 (streaming style): an independent tool written from the contract only.",
     """WITHOUT reading %(W42)s/c1/ctl-ref-tool.py.txt, read only the docstring of %(L)s/quality/counters/c1-r42-geometry.py (the contract) and write your own
`mado-geometry.py` in %(W)s/w1/ExecIndepC/ (stdlib only; selftest k==n>=50 with teeth). Structure it as two passes: first collect every supported rule into an ordered list, then
stream the clients JSON once. Score it: `""" + SCORE + """`. Report failing fixtures verbatim. Then answer, with evidence from your implementation effort, the ten places where the
contract text most needed a second reading (quote the sentence, give both readings, say which fixture or model line decides it, or that none does - an undecided reading is a hole in the predicate).""")
seat("ExecC1ExtraMutants", "executor",
     "Mutation population for C1: single-defect mutants of the reference beyond the 40 already registered.",
     """Read %(W42)s/ctl/run-c1-controls.py (the registered mutants) and %(W42)s/c1/ctl-ref-tool.py.txt. Build >= 40 NEW single-defect mutants (value-domain edits, boundary shifts,
operator swaps, dropped branches, reordered checks, wrong constants, swapped output fields, off-by-one in file/rule numbering, dropped sort/stability, changed exit codes) -
each a one-line text replacement asserted to match exactly once. Score each with `""" + SCORE + """` (use a private --nonce) and write a table `mutant | edit | verdict | failing
fixtures/clauses` to %(W)s/w1/ExecC1ExtraMutants/survivors.md. For every survivor say whether it is EQUIVALENT (give the proof: the unmutated and mutated behaviours coincide on every input
of the contract) or a MISSING CHECK (name the fixture that would kill it, with the exact input and expected output). Save the mutant files under your seat dir.""")
seat("ExecC2ExtraMutants", "executor",
     "Mutation and forgery population for C2: clause mutants and real-seeded forgeries beyond the 74 registered controls.",
     """Read %(W)s/ctl/run-c2-controls.py and import it with importlib (never run main; use its helpers admitted(), base_files(), commit_all(), score()). Build >= 40 NEW controls:
clause mutants (header window, id regexes, row cell edits, Gate-line variants, fences, README rows, ADMIT/REFUSE variants, census-line variants, locator variants, quote-boundary
variants such as a quote ending at punctuation, a quote preceded by an underscore or digit, a quote equal to a longer quote's prefix) and REAL-SEEDED FORGERIES: entries that cite a REAL
pinned receipt with a REAL quote but make a claim the receipt does not support, or cite the right quote at the wrong locator, or reuse one real quote for two ids. Every fixture repo is
`D=$(mktemp -d -p %(S)s/ExecC2ExtraMutants)` with `-C "$D"` on every git call (run-6 incident). Score under the real and the pin-patched counter; write
%(W)s/w1/ExecC2ExtraMutants/survivors.md listing every control the counter admits (survivor), the clause that should kill it, and whether the claim-to-quote binding is in principle a
non-author's job (then it is a declared residual, not a defect).""")
seat("ExecLiveHost", "executor",
     "Host receipt for C1: the reference tool on the running desktop, and how much of the host's rule set it can read.",
     """Copy the reference to %(W)s/w1/ExecLiveHost/mado-geometry.py. Run `hyprctl clients -j | python3 -I mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf` (expect
NO_MATCHING_CLIENT rc 3 while no gkeep window is open) three times, then with every rule file the host's `hyprland.conf` sources (follow `source =` lines, read only; omarchy defaults under
~/.local/share/omarchy/default/hypr/, theme and toggle files): count how many `windowrule = size ...` lines exist in total, how many the tool SUPPORTS (class match) and how many it counts
`unsupported` (tag/title/initial_class matches, percentage or expression sizes) or `other`, and for each unsupported size rule name the reason. Run it with a hand-made clients file that has
one floating `org.omarchy.gkeep` window of 420x500 (AGREE), 421x500 (DIFFER) and a tiled one (TILED), and with the real host dump piped through `--clients -`. Save verbatim outputs, exit codes,
the tool sha256 and the hyprctl version line to %(W)s/w1/ExecLiveHost/live-census.txt; this is the host receipt (reported, not scored).""")
seat("ExecOracleGkeep", "executor",
     "Oracle observation: the size Hyprland 0.56.2 itself reports for a floating window matched by the gkeep rules, in the isolated round-27 harness.",
     """Goal: observe, from a Hyprland 0.56.2 nested in the round-27 bubblewrap oracle (NEVER on the host session), a client with application id `org.omarchy.gkeep` under the host's three gkeep rules
(%(W)s/fetch/host-gkeep.conf) and read its `size` from `hyprctl clients -j` of the nested instance (expected 420x500 if the chain in the registration holds; a different value is the finding).
Method: the oracle needs tinywl from wlroots 0.20.2, which no longer exists on disk. Rebuild it with %(L)s/.ufo/waves/round-26/harness/build-tinywl.sh but with D=/fast/scratch/hyaku/mado-r43-oracle
(read the script and %(L)s/.ufo/waves/round-27/harness/oracle.py first; adapt copies into your seat dir, never edit them; the patch file is beside the script; `uv tool install meson` and ninja are
authorised; record versions). The harness pins sha256 of tinywl/libwlroots in oracle.py: record the NEW shas, they will differ. Then, inside the same bubblewrap layout as oracle.py (copy its
command), start the nested Hyprland with a minimal config that `source`s a copy of host-gkeep.conf, and map a client: try (1) `hyprctl -i <sig> dispatch exec` of `alacritty --class org.omarchy.gkeep`
(needs working EGL in the sandbox), (2) if that fails a minimal Wayland shm client you write (python + pywayland in a scratch venv, an xdg_toplevel with app_id set and a committed shm buffer; request
no size). Read `hyprctl -i <sig> clients -j` until stable. Run the same nested instance with the float rule removed (expect a tiled window: TILED) and with the size rule changed to `size 300 300`
(expect 300x300) as controls. HARD STOP: if the build or the client is not working after 45 minutes of effort, stop and write what failed (logs, commands) - an honest negative is the deliverable.
Save everything to %(W)s/w1/ExecOracleGkeep/ (receipt files <= 200 KB each: the commands, versions, shas, the `clients -j` lines, the rc of every step). Also compare the observation with the
reference tool's output on the observed JSON (`--clients` file, `--rules` the copy of host-gkeep.conf). Host coredump count (coredumpctl list) before and after must be equal.""")
seat("ExecAssimIdGuard", "executor",
     "Assimilation id guard and renumber map for the gkeep theme (item 10), in scratch.",
     """Run the id-collision guard of the round prompt in scratch: A=%(W)s/assimilation (mkdir -p); `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' %(L)s/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > $A/reg-ids`;
the same over %(P)s/SOURCES.append.md into $A/staged-ids; `comm -12` into $A/collisions. Prove the guard once on a scratch registry holding an indented row `  | S203 |` that the staged set
collides with (a non-empty collisions file), and print the proof. Then restrict to the staged rows that the 11 staged gkeep-theme files cite in their `source:` lines (list them), and write the renumber
map BY DOCUMENT (URL -> new id, S290+ for documents not already pinned, the pinned ids S290-S299 map to the URLs in the context; a staged row whose URL equals a lane-held row's URL maps to that held id,
no new row). Paste both id lists, the collision count, the renumber map (tsv: staged id, URL, new id or held id, reason) into %(W)s/assimilation/id-guard.md and renumber-map.tsv. Never write the
registry; never run a campaign tool in the shokuknow checkout.""")
seat("ExecQuarantineSlice", "executor",
     "Quarantine slice for mado, hand-checked where it touches the gkeep theme (item 10).",
     """Derive the lane's slice of the payload-absent register (read-only): A=%(W)s/assimilation; R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md;
`awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > $A/quarantine-slice` (every line carries an S-id). Report the data-row count. For every slice row whose id
is cited by one of the 11 staged gkeep-theme files (and for the row(s) of `gkeep-size-to-real-size-r11` and `gkeep-rendered-geometry-chain-r9` in particular), fetch the cited source and locate the quote:
absent -> refuse (fabrication class, reason), present -> adopt with the anchor you located (<= 25 words, access date 2026-10-26); a prose class cell ("could not be fetched") -> mark unverifiable
(`unreachable` is not fabrication). Write %(W)s/assimilation/quarantine-verdicts.md (id, class, URL, quote or absence evidence, verdict). Never edit the register.""")
seat("ExecSrcChain", "executor",
     "Located-quote fact table for the entry's source chain (the L1 writes the entry from it).",
     """For each pinned receipt S290-S296 in %(W)s/fetch/ extract the sentences/lines the entry will rest on, each a <= 25-word quote with its 1-based line number and the receipt's sha256, as a table
`id | claim the quote supports | quote | file:line | sha256`: (S290) the match is anchored RE2 FullMatch and a `negative:` prefix flips it; (S291) how the `float` and `size` effects are parsed into
`static_.floating` and `static_.size` (what value forms the size parser accepts: read the surrounding lines), min/max-size clamps; (S292) the floating-branch consumption of `static_.size` and what
else adjusts the size afterwards (clamping to monitor/work area? read the whole function); (S293) setPositionGlobal; (S294) the setBox/configure path for floating windows; (S295) the realSize write and
the GOAL/CURRENT accessors; (S296) the `clients -j` size fields. Verify every quote with a script that greps the receipt (print the grep result). Add `what the source does NOT say` (e.g. whether the client
may decline the configure, what happens on a later user resize or a monitor change). Write %(W)s/w1/ExecSrcChain/facts.md. Quote only from the pinned receipts unless you open and pin a new one (then give URL, tag/commit, sha256).""")
seat("ExecGoalVsValue", "executor",
     "Goal versus current size: what `hyprctl clients -j` size is while a window animates.",
     """From %(W)s/fetch/Hyprland-HyprCtl.cpp, Hyprland-GeometricMovableAnimated.cpp and any further v0.56.2 file you open (raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/..., e.g. src/desktop/view/Window.cpp,
src/desktop/view/types/GeometricMovableAnimated.hpp, the animation config for `windowsMove`/`windowsIn`), establish: (1) exactly which accessor the `clients -j` `size` field calls and what GEOMETRIC_GOAL
returns; (2) when goal and current differ (during the open/move animation) and whether the goal is already the rule's size at the first frame; (3) what `hyprctl getprop` or other read verbs expose the current
value, if any; (4) the consequence for a reader comparing a rule's size with `clients -j`: AGREE at goal is not a statement about pixels on screen. Every claim gets a <= 25-word located quote from a file you
pin in %(W)s/w1/ExecGoalVsValue/pins/ with sha256; any file you open that is not already S290-S296 is a candidate registry row (URL, anchor, tier, what it teaches). Write %(W)s/w1/ExecGoalVsValue/finding.md.""")
seat("ExecHarmBase", "executor",
     "Harm-check baseline at base, on a clone, for the round's no-harm comparison.",
     """On a fresh clone of the base (D=$(mktemp -d -p %(S)s/ExecHarmBase); `git clone -q --no-hardlinks %(L)s "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals $D; `git -C "$D" checkout -q %(B)s` is allowed ONLY
inside this clone), run and capture to %(W)s/w1/ExecHarmBase/harm-base.txt: `bash tools/mado-verify.sh --selftest`, `python3 -I tools/mado-options.py --selftest`, `python3 -I tools/mado-globals.py --selftest`,
`python3 -I quality/check-index.py --rev %(B)s --repo .`, `python3 -I quality/check-index-rows.py` (read its usage), `python3 -I quality/check-axis-scores.py --rev %(B)s --repo .`, and
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (the real lane). Compare with %(L)s/.ufo/waves/round-41/receipts/harm-tip.txt and
state every difference. Also record `ls tools | wc -l`, `ls corpus/knowledge | wc -l`, `grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md`, QUALITY.md's last criterion number. Delete the clone.""")

seat("ExecLocatorGate", "executor",
     "Mistake fix (frontier step): a checker that recomputes source locators written in prose, shown able to fail on round 42's wrong locators.",
     """Build %(W)s/w1/ExecLocatorGate/check-locators.py (stdlib only, read-only, `python3 -I`): given `--fetch DIR` (a directory of pinned receipts) and one or more prose files (markdown), find every
locator token `<name>:<N>[-<M>][,<N2>[-<M2>]...]` whose `<name>` (optionally prefixed by `fetch/` or a path) is a file in DIR, and for each one take the backticked code fragments of the SAME line; a fragment
is SUPPORTED when every identifier token of it (regex `[A-Za-z_][A-Za-z0-9_]*`, length >= 3) occurs inside the union of the cited line ranges of the receipt. Print one line per locator
`LOC <file>:<line of prose> <locator> fragments=<k> supported=<j> verdict=OK|MISS|NOFRAG` and a final `CHECK_LOCATORS: locators=<n> miss=<m>`; exit 1 when miss > 0, 0 otherwise, 2 on usage errors.
Include `--selftest` (k==n >= 12, with teeth: flipping the range-inclusion comparison must fail it). Show it CAN FAIL on the real mistake: run it with `--fetch %(W42)s/fetch` over
`git -C %(L)s show a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f:LOG.md` (save that to your seat dir; the Round 42 entry names `Hyprland-HyprCtl.cpp:394-395,412-413` beside `w->size(GEOMETRIC_GOAL)`) and over
`%(W42)s/registration.md` - it must report MISS for the HyprCtl locator; then write a corrected copy of those lines (the true lines: compute them with `grep -n` on the receipt) and show OK. Also run it over
every `corpus/knowledge/*.md` at the base and report the counts (an entry with no fetch-dir locator is NOFRAG/none, not a miss). Write the outputs verbatim to %(W)s/w1/ExecLocatorGate/receipt.txt and a
short report.md naming its limits (identifier tokens are a proxy for the fact; prose without backticks is not checked).""")

# ------------------------------------------------------------ scribes (7)
ENTRY_SHAPE = """Entry shape (follow the lane's existing entries, e.g. %(L)s/corpus/knowledge/hyprland-focus-grab-r41.md and hyprctl-getoption-native-forms-r40.md): title; `Lane: mado-shokunin. Round: 43.`;
within the FIRST 20 raw lines: `source: S### - <title> - <anchor>` lines for every cited id (>= 4; S050-style held ids allowed), exactly one `verified-at: 2026-10-26`, exactly one `recheck: <ISO date|NNd|on-release>`;
no other `source:`/`verified-at:`/`recheck:` line anywhere. Then the body: every cited id has ONE claim line that names only that id, carries its Gate quote verbatim (<= 25 words, >= 3 words, word-bounded in the receipt)
and the locator `<receipt file name>:<line>` (the line where the quote starts, e.g. `Hyprland-DefaultFloatingAlgorithm.cpp:60`); tag claims OBS (read from a receipt), INF (derived) or UNK (not established), and give a
decision table `question | where the answer lives | state (OBS/INF/UNK)`. Three census lines, each verbatim on a line of its own, outside any code fence, exactly once:
`host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$`, `host clients total=4 floating=0 gkeep=0`, `gkeep request default_size=420x500 application_id=org.omarchy.gkeep`
(the counter recomputes them from the pinned receipts). No S### token other than a cited id. Ids: S290-S299 as in the context; add `S300+` only for sources you pin and the L1 will open as rows.
Never state that a gkeep window was observed at 420x500 unless a receipt in the wave shows it; the honest state today is UNK (no client open)."""
seat("ScrEntryA", "scribe",
     "Draft the C2 entry - chain-first structure.",
     ENTRY_SHAPE + """
Structure: (1) the host rule text, (2) match, (3) effects, (4) consumption, (5) storage and configure, (6) the reported variable (goal), (7) the client's request, (8) what is and is not observed.
Re-open every receipt you quote (the L1 verifies each quote and locator with a script). Write the draft to %(W)s/w1/ScrEntryA/hyprland-gkeep-geometry-r43.md, and a `quotes.tsv` (id, quote, file, line, sha256).""")
seat("ScrEntryB", "scribe",
     "Draft the C2 entry - decision-table-first structure.",
     ENTRY_SHAPE + """
Structure: open with the decision table (what a reader can conclude about a gkeep window's size from the rule alone, from `clients -j`, and from the client's request - and what each does NOT license), then the chain
as short evidence paragraphs, then the census lines. Keep it under 90 lines. Re-open every receipt you quote. Write the draft to %(W)s/w1/ScrEntryB/hyprland-gkeep-geometry-r43.md and `quotes.tsv`.""")
seat("ScrRowsDraft", "scribe",
     "Draft the ten registry rows S290-S299 (and any proposed S300+) for corpus/SOURCES.md.",
     """Read %(L)s/corpus/SOURCES.md (the Registry shape, a few recent rows S283-S289 as exemplars, CORPUS.md in the fleet root for the contract). Draft rows for the ten pinned receipts in the 11-column schema
(`| id | source - URL | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`): kind code/own-work, tier A (primary source code at a tag; the lane's own receipts are `own-work` tier A), anchor = file + line range +
tag/commit (or sha256 for own-work), teaches = one grounded learner benefit, status `mined`, opened 2026-10-26, recheck an ISO date or `on-release`, used-by `corpus/knowledge/hyprland-gkeep-geometry-r43.md`; no `|` inside any cell; the
location (last whitespace token of the source cell) is the URL for upstream rows and the repo path `.ufo/waves/round-43/fetch/<file>` for own-work rows, and its last path component equals or contains/is contained by the receipt's file name
(counter clause e). Check each URL actually serves the receipt (curl the raw URL and compare sha256 with receipts/fetch-sha256.txt). Verify against the lane registry that none of the ten locations is already a row (a duplicate URL within scope is census E04):
`grep -c` per URL; report any held row (e.g. the HyprCtl.cpp rows S018/S158) and decide: new row (different tag/anchor) or cite the held one. Mirror-validate: copy %(L)s/corpus into %(S)s/ScrRowsDraft/validate/corpus, append your rows to the Registry table and run
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`; paste the output (exit 0 required). Write %(W)s/w1/ScrRowsDraft/rows-block.txt (only the table rows) and rows.md.""")
seat("ScrLessonSkeleton", "scribe",
     "Draft corpus/lessons/round-43.md: Gate, assimilation decisions, Mistakes.",
     """Read %(L)s/corpus/lessons/round-41.md and round-41-verifier-spotcheck.md for the shape, and the counter docstring %(L)s/quality/counters/c2-r43-gkeep-entry.py (clause d and i define the Gate-line grammar:
`GATE <id> receipt=<path> sha256=<64 hex> quote="<q>"` in column 0 under `## Gate`, one per cited id; `ADMIT <staged path> as <entry path>`; `REFUSE <staged path> reason=<>= 4 distinct words>`). Draft the lesson skeleton:
`## Gate` (GATE lines for S290-S299 from %(W)s/receipts/fetch-sha256.txt - compute the sha256 yourself and choose quotes that are 3-25 words, word-bounded in the receipt, unique across receipts - plus the ADMIT/REFUSE lines: read the
11 staged gkeep-theme files in %(P)s/knowledge/corpus/knowledge/ and decide: ADMIT one as the entry's predecessor; REFUSE at least one with reason and flip condition (e.g. a localized-channel source, a private-receipt dependence, a claim the
host has since falsified)); the access date 2026-10-26 for every new row; the old->new log of any status/recheck/used-by change; `## Mistakes` with class/evidence/captured-by/fix rows for the mistakes of round 42 (each with its evidence pointer: the round-42 closure's routed items 2-4 - wrong locators, the C1 control tally stated three
ways, the SHONEN pointer to an uncommitted run; the missing round-42 lesson; the round-42 gkeep excerpt header claiming lines 446-495 of a 488-line file with one extra blank line, compare
`diff <(tail -n +3 %(W42)s/fetch/gkeep-ui-excerpt.py) <(sed -n '446,$p' ~/Projects/gkeep/gkeep/ui.py)`), each with captured-by (the criterion that should have caught it, or `none`) and the fix with the control that shows it can fail; `## Spot-check` placeholders for
the non-author closure. Write %(W)s/w1/ScrLessonSkeleton/round-43-lesson.md. Mark every line the L1 must fill (hashes, results) with `<<L1>>`.""")
seat("ScrSkillProvince", "scribe",
     "Draft the SKILL.md / PROVINCE.md / README rows for the new tool and entry.",
     """Read %(L)s/SKILL.md (its probe table, decision rows and the subsection 'Advertised Wayland globals' of round 41 as the exemplar), PROVINCE.md (tool rows) and corpus/README.md (the coverage-map index rows, columns, and the `## Frontier` list).
Draft, as exact insertion text with the neighbouring line numbers: a SKILL.md probe row (command + a sample line from a real run of the reference at %(W42)s/c1/ctl-ref-tool.py.txt copied to your scratch; run it on the host:
`hyprctl clients -j | python3 -I <copy> --clients - --rules ~/.config/hypr/gkeep.conf`), a decision row (what each verdict licenses and does NOT license: AGREE reads the animation goal, TILED means the rule is inert, DIFFER is a report), a short
subsection 'Rule size versus reported size'; a PROVINCE.md tool row; a corpus/README.md index row for `knowledge/hyprland-gkeep-geometry-r43.md` with ALL of the index's cells (the round-41 data commit failed check-index-rows for a
missing Sources cell), and a Frontier bullet advance. Run `python3 -I %(L)s/quality/check-index-rows.py` on a scratch copy with your row to show errors=0. Write %(W)s/w1/ScrSkillProvince/{skill-rows.md,province-row.md,readme-row.md}.""")
seat("ScrQualityCriteria", "scribe",
     "Draft QUALITY.md criteria 77+ from this round's mistakes.",
     """Read the tail of %(L)s/corpus/QUALITY.md (criteria 60-76 for the form: one criterion per numbered line, each citing its lesson) and the round-41 spot-check (§6 routed items). Draft criteria for the round-42 mistakes: (a) a source locator written in prose (LOG.md, the registration, the report) is computed by a script from the pinned
receipt, never typed (the closure found `Hyprland-HyprCtl.cpp:394-395,412-413` for a fact at :427-428; the checker built by seat ExecLocatorGate is the control); (b) a control tally is stated once with its
definition (the round-42 report said 46 controls, the receipt header 46 and its verdict line 0 of 47); (c) a SHONEN or report pointer to a run points at a committed receipt (round-42 SHONEN box 2 pointed at a LOG line that does not exist);
(d) an excerpt header's line range is produced by the command that cut it (the round-42 gkeep excerpt). Each: the rule, the
mistake class, the evidence pointer (path:line or command), and the control that shows it can fail (name it). No criterion without a mistake behind it; say which of the four you would refuse for lack of one. Write %(W)s/w1/ScrQualityCriteria/criteria.md.""")
seat("ScrConsiderthese", "scribe",
     "Land considerthese 2026-10-25 proposal 2 (dead attempts and dirty closures) as a measured criterion.",
     """Read %(L)s/considerthese/2026-10-25.md (never edit it), proposal 2: 'Count dead attempts and dirty closures from the watchdog digests'. Ground it through the lane's own bar: open what it points at. Write the counting command(s) that produce, for mado
rounds 36-42, the table `round | attempts launched | closed clean (untracked files at closure)` from /home/vgpnk/Projects/shokunin/.ufo/watchdog.log (read-only: `grep 'mado round=' ... `) and each round's `corpus/lessons/round-N-verifier-spotcheck.md` 'uncommitted round work' line,
RUN them and paste the output; note the motivating instances: round 41's two untracked leftovers (deleted at round-42 start) and round 42's attempt that ended with its wave never spawned. Draft a QUALITY.md criterion (number 78 or the next free; cite `considerthese/2026-10-25.md`
proposal 2 and this lane's round-43 lesson) with the command a closure can re-run, and the sentence for the round report. Say honestly where the proposal's reflection is a pointer and not evidence (the table is from the watchdog, not from the reflection). Write %(W)s/w1/ScrConsiderthese/proposal.md.""")

# ------------------------------------------------------------ scouts (3)
seat("ScoutStagedGkeep", "scout",
     "Planning data-walk: the 11 staged gkeep-theme files against the lane and the pinned receipts.",
     """Read every staged file %(P)s/knowledge/corpus/knowledge/{gkeep-*,glyph-and-geometry-r31}.md, %(P)s/MERGE-REPORT.md and %(P)s/SOURCES.append.md (rows cited), PROVINCE.md, corpus/QUALITY.md (the bar) and corpus/README.md (coverage map). For each file: what it claims,
which of its sources are public (URL at a tag) versus private `lanes/mado/roundN/fetch/...` receipts, which claims the pinned receipts S290-S299 can re-ground, what is superseded by a later staged file, and PROVINCE fit. Rank them; name the SINGLE best admit set
for ONE successor entry and the refusals with reason + flip condition. Verify at least five staged quotes against the pinned receipts (grep). Write %(W)s/w1/ScoutStagedGkeep/survey.md (a table plus the recommendation).""")
seat("ScoutSizeGrammar", "scout",
     "What the `size` window-rule value can be: the grammar the C1 tool deliberately does not read.",
     """From the pinned %(W)s/fetch/Hyprland-WindowRuleApplicator.cpp (lines ~400-430) and the v0.56.2 sources it points at (`Math::SExpressionVec2`, `calculateExpression`, the rule parser for `size`: open and pin them under %(W)s/w1/ScoutSizeGrammar/pins/ with sha256),
and the host's own rule files (read-only; `grep -rn 'size' ~/.config/hypr ~/.local/share/omarchy/default/hypr`), establish what values `size` accepts (integers, percentages, `monitor_w*0.5` style expressions, `window_w`), what `float`
accepts (`on`/`off`/`true`?), and what `match:class` regex forms the host actually uses. List which real host rules the tool's contract (digits only, `float on|off`, `match:class` with a restricted regex alphabet) reads and which it refuses,
and propose (do not implement) the smallest contract extension that would read the most host rules safely. Quotes <= 25 words, located. Write %(W)s/w1/ScoutSizeGrammar/finding.md.""")
seat("ScoutReadmeCoverage", "scout",
     "Coverage-map ground: where the gkeep-geometry entry and the geometry tool land in corpus/README.md and PROVINCE.md.",
     """Read %(L)s/corpus/README.md (coverage map rows, `## Frontier`, the expansion-credit rule) and %(L)s/PROVINCE.md. Determine, with grep commands and their outputs, whether the lane held ANY of: window-rule matching semantics, the `size`/`float` effects, floating-window
geometry, `hyprctl clients -j` field semantics, the gkeep window's size, at base %(B)s (`git grep -i ... %(B)s -- corpus/knowledge PROVINCE.md SKILL.md tools`). Name the coverage-map row(s) and Frontier bullet(s) this round's entry moves, and the expansion-credit
statement the report may honestly make (new ground vs deepening of window-rule-effects-getprop.md / rule-attribution-r24.md). Flag overlap with the siblings' provinces you can see from PROVINCE.md (adjacent). Write %(W)s/w1/ScoutReadmeCoverage/coverage.md.""")

# ------------------------------------------------------------ connectors (3)
seat("ConnSiblingOverlap", "connector",
     "Sibling-overlap scan for the round's two claims (planner seat's connector).",
     """Scan read-only the other lanes' PROVINCE.md and corpus indexes under /home/vgpnk/Projects/shokunin/*-shokunin/ (PROVINCE.md, corpus/README.md, `grep -rli 'windowrule\\|window rule\\|clients -j\\|set_default_size\\|gkeep' */corpus/knowledge */tools */SKILL.md`)
for holdings that overlap C1 (a rule-size versus reported-size join) or C2 (gkeep window geometry). Report overlaps, adjacent claims, and any contradiction with the registration; say which lane would arbitrate (adjacency axis), and whether
the geometry tool or the entry duplicates a sibling's held fact. `gkeep` is the operator's own project (~/Projects/gkeep): state what mado may and may not claim about it (installer provenance vs the app's behaviour). Write %(W)s/w1/ConnSiblingOverlap/overlap.md.""")
seat("ConnCrossClaim", "connector",
     "Cross-claim and cross-source pattern finding between C1 and C2.",
     """Build a claims-vs-sources matrix for the whole round: C1's contract sentences and C2's entry claims against the pinned receipts S290-S299 and the host files. Find: (1) a contract sentence of C1 that rests on a source fact C2 will state (e.g. FullMatch anchoring, the float-only
consumption of size, the goal variable) - is the dependence consistent in both directions; (2) any fact one claim needs that the other contradicts; (3) a source that would strengthen both and is not yet pinned; (4) the separability check: delete tools/mado-geometry.py -> does C2's counter still score
1/1 on a good entry; delete the entry -> does C1 still score 37/37 (read both counters to answer, then run C1 with the reference via `--tool` and C2's control P). Write %(W)s/w1/ConnCrossClaim/cross.md.""")
seat("ConnStagedVsRegistry", "connector",
     "Staged rows versus lane registry: duplicates, held rows, tiers.",
     """For the staged rows cited by the 11 staged gkeep-theme files (%(P)s/SOURCES.append.md and the files' `source:` lines), compare with %(L)s/corpus/SOURCES.md: which staged URLs the lane already holds (S018, S158, S037 ...), which hold a different anchor/tag, which are tier C or
`community`, which are private receipts (`lanes/mado/roundN/fetch`) that cannot be re-opened, and which duplicate-URL warnings (census W04) a new row for S290-S299 would add (`sources-census.sh` prints W04 on duplicate URLs across scopes; E04 within scope is fatal). Write %(W)s/w1/ConnStagedVsRegistry/matrix.md with a per-row
verdict (reuse held / new row / refuse) and the exact grep outputs.""")

# ------------------------------------------------------------ reviewers (3), critics (3), mutation-testers (2)
seat("RevC1Counter", "reviewer",
     "Attack C1's frozen counter: gates, sandbox, determinacy.",
     """Review %(L)s/quality/counters/c1-r42-geometry.py line by line. Hunt: fixtures that are vacuous (pass for a tool that handles only the first file or only stdin), generator lattices that never reach a value domain the contract names, clauses whose guard is dead, a sandbox that
exposes the counter or the lane to the tool, ways the timeout breaker can be abused (3 timeouts make the remaining fixtures fail - can a legitimate tool trip it?), model-vs-contract disagreements (re-derive the model from the docstring alone and diff by sampling 300 cases), and any place where the docstring and the code are not the same sentence.
Each finding: severity, the exact line, a reproduction. Write %(W)s/w1/RevC1Counter/findings.md. Do NOT edit the counter.""")
seat("RevC2Counter", "reviewer",
     "Attack C2's frozen counter: forgeries that are admitted.",
     """Review %(L)s/quality/counters/c2-r43-gkeep-entry.py against its docstring. Re-derive each clause independently and try to admit a forged entry: a real quote at a true locator that supports a different claim, locator regexes (`(?<![\\\\w.-])name:N(?!\\\\d)`) edge cases (name inside a longer path, N at a line end),
word-boundary edge cases for quotes that start or end with punctuation, collapsed-whitespace line mapping when a quote spans lines, a census line that matches only because the computed values are trivial (total=0), regexes with `^`/`$` in the rule class (`rxc.fullmatch` versus the host's RE2), a held id with a receipt of the wrong file, an own-work row whose location points elsewhere.
Each finding: severity, line, a fixture that scores admitted=1/1 (build it with the controls' helpers in a scratch repo `D=$(mktemp -d -p %(S)s/RevC2Counter)` with `-C "$D"`). Write %(W)s/w1/RevC2Counter/findings.md. Do NOT edit the counter.""")
seat("RevRefTool", "reviewer",
     "Attack the reference tool: robustness and the contract's own invariants.",
     """Read %(W42)s/c1/ctl-ref-tool.py.txt and attack it outside the counter's fixtures: pathological inputs (1 MiB single-line rule files, 1 MiB of nested JSON, deeply nested lists -> RecursionError, huge integers in size, a client class of 1 MiB against a backtracking-prone regex such as `(a|aa)+$` from the SAFE alphabet - measure the time),
stdin closed, `--clients -` when stdin is a TTY-less /dev/null, stdout closed, output on a broken pipe, files that change during the read, symlinks. For each: input, expected per contract, observed, time, severity. The contract promises a verdict or `SETUP` and an exit code; list every input that violates that (traceback, hang > 5 s). Write %(W)s/w1/RevRefTool/findings.md with repro commands.""")
seat("CritC1Cheat", "critic",
     "Cheat design against C1: tools that reach TARGET_MET without implementing the capability.",
     """Design and BUILD cheats (each a single file you put under %(W)s/w1/CritC1Cheat/) and score each with `""" + SCORE + """`: a tool that embeds the model but renames everything; a tool that reads fixtures through paths it should not see (the tool dir is read-only mounted - what else is
visible in the sandbox? /usr, /proc, the clients file's neighbours); a tool whose selftest is a generated table that mirrors its code (so every flipped comparison is covered by construction); one that detects the sandbox (fresh /proc, HOME=/nonexistent, the opaque directory names) and behaves differently outside; a tool that caches by nonce or by the fixture file hash;
a tool that passes 37/37 by special-casing the fixed fixtures' exact bytes and implementing only the generated ones (does the lattice defeat it?). Report each: size, the clause that should have caught it, whether it reached TARGET_MET, and a concrete tightening that does not reject the reference. Do NOT edit the counter.""")
seat("CritC2Cheat", "critic",
     "Forgeries against C2: entries that are admitted while the claim is not grounded.",
     """Build forged entry+registry+lesson sets (in scratch fixture repos made with the controls' helpers; see %(W)s/ctl/run-c2-controls.py; `-C "$D"` on every git call) that PRED-C2-r43 admits although they are not grounded: real receipts with real quotes cited for claims they do not support (write the unsupported claim into the entry line), the right
quote with a locator that is true for a second occurrence, a quote from a comment instead of code, a census line that is true but irrelevant, ids that the entry cites in one line and contradicts in another. For each forgery: the lines that matter, the clause that should have caught it, and the tightening that would not reject the genuine fixture (control P of the controls). Distinguish
a mechanical hole (fixable in the counter) from the declared residual (needs a non-author reading). Write %(W)s/w1/CritC2Cheat/forgeries.md. Do NOT edit the counter.""")
seat("CritClaimSizing", "critic",
     "Attack the round's claim sizing and re-registration (prompt section 6 item 9) before any data.",
     """Read %(W)s/registration.md, %(L)s/corpus/lessons/round-42-verifier-spotcheck.md, /home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-43.md section 6 item 9 (claim sizing) and item 10 (frozen and resumed
rounds), and /home/vgpnk/Projects/shokunin/AXES.md. Attack: (1) is re-registering round 42's never-scored predicates in round 43 a rule changed after data? (check that no seat ever scored them:
`git -C %(L)s log --format='%%h %%s' -- quality/counters/c1-r42-geometry.py quality/counters/c2-r42-gkeep-entry.py` and the round-42 w1 dir has no seat reports); (2) is the C2 r43 counter really
constants-only (`diff %(L)s/quality/counters/c2-r42-gkeep-entry.py %(L)s/quality/counters/c2-r43-gkeep-entry.py` - classify every changed line); (3) can a do-nothing control reach either target -
build the cheapest one you can think of beyond the registered controls (a 3-line tool, a README-only commit, a copy of the reference with its selftest stripped) and score it with the counting
commands; (4) does any universal clause slip in ("all", "every", "complete") that the counter does not enumerate; (5) is the lowest-axis argument sound given %(W)s/receipts/axis-base.txt; (6) are
the claims causally separable as stated. Each finding: severity, the exact sentence or line, the command and its output. Write %(W)s/w1/CritClaimSizing/findings.md. Do NOT edit any tracked file.""")
seat("CritContract", "critic",
     "Ambiguity hunt in C1's contract against the real compositor's semantics.",
     """Read the docstring of %(L)s/quality/counters/c1-r42-geometry.py and the pinned Hyprland sources (%(W)s/fetch/Hyprland-RegexMatchEngine.cpp, WindowRuleApplicator.cpp, DefaultFloatingAlgorithm.cpp, HyprCtl.cpp). Find (1) contract sentences with two readings (list both, name the fixture that decides, or none), (2) sentences where the contract claims
more about Hyprland than the pinned source supports (e.g. 'a tiled window never reads the rule' - is that what the code shows? read the tiled path; 'the last matching size rule wins' - does the applicator apply rules in file order with later overriding? read the rule engine/priorities), (3) rule-line forms the host really writes that the contract classifies wrongly as `other`
or `unsupported` (e.g. `windowrule = float on, size ..., match:class ...` multi-effect lines? the 0.56.2 syntax: open the Window-Rules docs page https://wiki.hypr.land/Configuring/Basics/Window-Rules/ and quote its syntax section). Each finding: severity, quote of the sentence, the source line that contradicts or the missing case, and the contract amendment (text) that fixes it. Write %(W)s/w1/CritContract/findings.md.""")
seat("MutC1CounterGates", "mutation-tester",
     "Mutation-test C1's counter: each gate of the counter must be able to fail.",
     """Copy %(L)s/quality/counters/c1-r42-geometry.py to %(S)s/MutC1CounterGates/ and mutate ITS code (one edit each, >= 30): the model (verdict order, exit codes, field order), the sandbox flags, the nonce handling, `imports_ok` (each deny list entry removed), `function_sites`/`teeth` (KILL_NEED, N_MUT, MIN_SITES, the forced-site rule), `neutrality`, `judge` (stderr check, rc check), the timeout breaker, TOTAL. For each mutant run the mutated counter on (a) the reference
%(W42)s/c1/ctl-ref-tool.py.txt and (b) a control that the unmutated counter scores below MET (use %(W42)s/ctl/run-c1-controls.py's files by regenerating them into your scratch dir) and record: does the mutant counter now score a bad control MET (gate broken: a missed defect) or the reference below MET (over-strict)? Write %(W)s/w1/MutC1CounterGates/matrix.md: mutant | edit | reference verdict | worst control verdict | survivor?. For each
survivor say whether it is equivalent (proof) or a missing control (name it).""")
seat("MutRefSelftest", "mutation-tester",
     "Mutation-test the reference tool's own selftest and fixtures.",
     """Mutate every function of %(W42)s/c1/ctl-ref-tool.py.txt EXCEPT `selftest` (>= 40 edits: comparisons, constants, branch removals, regex edits, return values) and run only the tool's own `--selftest` (python3 -I) on each mutant. Record which mutants the selftest alone kills and which only the counter's fixtures kill (run the counter with --tool on survivors:
`""" + SCORE + """`). For each mutant undetected by the selftest, say whether it is equivalent (proof) or a missing assertion, and give the assertion (input, expected output). Write %(W)s/w1/MutRefSelftest/matrix.md and the assertions to add to `selftest` as a unified-diff-free list.""")

# ------------------------------------------------------------ labrat, simplifier, sentinel (3)
seat("LabRe2Fuzz", "executor",
     "One falsifiable hypothesis: Python `re.fullmatch` equals RE2 `FullMatch` over the contract's regex alphabet.",
     """Hypothesis H: for every REGEX the contract accepts (1-200 chars of `[A-Za-z0-9_.^$()|*+?-]` plus the escapes `\\\\. \\\\- \\\\( \\\\) \\\\| \\\\* \\\\+ \\\\? \\\\^ \\\\$ \\\\\\\\`, containing none of `(?`, `*+`, `++`, `?+`, and compiling under Python `re`) and every class string, `re.fullmatch(REGEX, class)` is true exactly when RE2's FullMatch is.
Falsify it: in a scratch venv under %(S)s/LabRe2Fuzz (`uv venv` then `uv pip install google-re2`; record version and channel) generate >= 300000 (regex, class) pairs - random from the alphabet, biased to nested groups, alternation, repetition of groups, `^`/`$` in the middle, empty alternatives, `.` against non-ASCII and astral characters, classes with `\\n`/NUL/surrogate-free unicode, long classes -
and compare; also compare compile acceptance (a regex RE2 rejects but Python accepts is an unsupported-in-Hyprland rule the tool would wrongly evaluate). Report the divergence classes with minimised examples and counts, or the honest negative with the pair count and seed. If a class diverges, propose the contract restriction (a substring or construct to refuse) and show it removes the divergence on the same seed. Write %(W)s/w1/LabRe2Fuzz/report.md and the script.""")
seat("SimpContract", "simplifier",
     "Delete dead weight from C1's contract before data: clauses no input can exercise.",
     """Read the docstring of %(L)s/quality/counters/c1-r42-geometry.py clause by clause. For each contract sentence, decide whether some input can make the observable output differ depending on it (build a pair of inputs that does, run the reference on both) - or whether the sentence is dead (the round's M20 `#` clause was: no input exercised it) or redundant with another (the empty-regex bound is implied by the `(.+)` capture). List dead/redundant sentences with the
proof pair or the proof of redundancy, and the exact deletion text for the contract (docstring), the reference and the model. Also list sentences that are live but unexercised by the 37 fixtures (a contract line no fixture reads is a free pass for a cheat). Write %(W)s/w1/SimpContract/dead-weight.md.""")
seat("SentReDoS", "sentinel",
     "Security review of the geometry tool: untrusted JSON and regexes from config.",
     """Review %(W42)s/c1/ctl-ref-tool.py.txt as security-sensitive code: it parses `hyprctl clients -j` (class strings are chosen by arbitrary applications) and config files (operator-owned but possibly generated), evaluates regexes with Python `re`, reads stdin/files up to 1 MiB, and prints values into line-oriented output. Probe, with commands and timings: catastrophic backtracking
(`(a|aa)+$`, `(a*)*b`, `(a+)+$` from the SAFE alphabet against a 30-100 KiB class string - a window title/class is attacker-influenced), output injection (can a class or address forge a `MADO_GEOM_CLIENT` or `MADO_GEOMETRY` line? the contract json-escapes them), integer-size abuse, JSON depth bombs, a FIFO/symlink/`/proc` path as `--rules`,
stdout/stderr leaks of file contents. Rank each with a severity and give the contract-level mitigation (e.g. a regex complexity bound, a class length bound) that keeps the reference's 37/37 behaviour. Write %(W)s/w1/SentReDoS/findings.md with timings; never run anything outside your scratch dir.""")

import collections as _c
assert len(items) == 38, len(items)
assert len({i["name"] for i in items}) == 38
print(len(items), dict(_c.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-43/w1",
        "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
