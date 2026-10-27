#!/usr/bin/env python3
"""Generates .ufo/waves/round-51/w1-spec.json (round 51, wave w1 = BUILD + first attack, policy v1, 48 seats).

Claims frozen at d2740281 (claims.md): C1 operability = tracked lane-level tool ledger
(quality/tool-ledger.md + quality/check-tool-ledger.py + counter c1-r51-ledger.py);
C2 coverage = dispatcher-dispatch entry with candidate-inclusive novelty (entry + rows S364+
+ pins + counter c2-r51-dispatch-entry.py). The L1 freezes counters/fixtures/controls after w1
returns; wave w2 (separate dispatch) attacks that freeze.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-51"
BASE = "6ca8c559a4a3d6d361101592116eea2bc7452437"
CLAIMS = "d274028163033244bd78938ad152dc250cc50480"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r51"

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
mado round 51 (hyaku run 10, 2026-10-27), wave w1 = BUILD + first-attack (policy v1). Lane repo: %(L)s (desktop and
compositor craft: the Hyprland/waybar/walker/terminal/keyboard config plane of this host; lane axes coverage + operability).
Round base (lane tip at round start) %(B)s; claims committed at %(C)s. READ %(W)s/claims.md FIRST - it carries the two frozen
predicate sentences this wave builds against - then %(L)s/corpus/lessons/round-50-verifier-spotcheck.md (section 6 routes
defects to this round). Nothing is frozen beyond claims.md: the L1 freezes counters, fixtures and controls AFTER w1 returns;
wave w2 attacks that freeze. Your output feeds the freeze.
- C1 (operability, capability acquisition): the tracked lane-level tool ledger. Round 50 w2/RevLedgerR50 found the wave-seat
  tool ledger missed tools/mado-hostguard.py and tools/mado-keysym.py and no lane-level ledger/checker exists. Build:
  quality/tool-ledger.md (draft: seat dir), quality/check-tool-ledger.py (checker, hermetic --selftest),
  quality/counters/c1-r51-ledger.py (counter PRED-C1-r51, wording frozen in claims.md).
- C2 (coverage, sourced): corpus/knowledge/hyprland-dispatcher-dispatch-r51.md - how Hyprland 0.56.2 parses and executes a
  keybind's dispatcher string (handleKeybind -> m_mDispatchers, argument splitting, submap special cases, hyprctl dispatch path).
  Round 50 falsified the bind-key-match novelty: 81.7% shingles from the round-49 candidate - the C2 novelty baseline MUST
  include .ufo/waves/round-*/candidate/** and bind >=3 held facts to held corpus lines.
- Routed items: D1 (final WAVE-DONE receipt committed at integration tip - process design), D4/M50-9 (fetch checksum manifest
  self-row cleanup at .ufo/waves/round-50/fetch/SHA256SUMS - a receipt-only fix, never edit round-50 bytes), the 13-row mado
  absent-defect register slice verdicts (quarantine hand-check).
# Write scope and safety
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it; mkdir -p) plus your Report file
  %(W)s/w1/<YourSeatName>.md. NEVER edit a tracked file anywhere; drafts of files meant for tracked paths go in your seat dir
  under the same basename. Never touch the fleet repo outside the lane, sibling lanes, templates/, scripts/, MANIFEST.json,
  .ufo/state/, .ufo/watchdog.log, .scratch/, or the shokuknow checkout (READ-ONLY; never run a campaign tool there). Never run
  mutating git/jj anywhere (no add/commit/push/checkout/reset/stash/describe/bookmark/new). Read-only git is fine.
- The L1 is the only integrator and the only committer. Every `Report:` trailer path is relative to %(L)s - write it at
  %(L)s/<that path>. Your tools start at the fleet root: absolute paths only, everywhere.
- Write your Report file FIRST (short status), then refine it. Declare every deliverable under a `## Deliverables` heading as
  one `- `<path>`` bullet AND in a `Report:` trailer line; `test -f` each declared path before yielding (a declared-but-absent
  path is an ABSENT defect under QUALITY 101). A seat that dies without a report is a dead seat.
- You are a LEAF: no task/tool spawns of your own (one executor may spawn one read-only labrat probe; everyone else stays a
  leaf). Never message agent://all; message only your L1 if truly blocked. Never call the ask tool.
# Scratch and host discipline (operator directive 2026-10-25)
- Every clone, venv, fixture tree and work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it explicitly as TMPDIR/--work/
  mkdtemp(dir=...)). /tmp is for files under 50 MB only. DELETE your scratch dir before you finish (trap/finally); copy
  receipts you need into your seat dir first. A counter, probe or gate you write must honour TMPDIR and accept a scratch
  argument - a hardcoded /tmp is a routed defect (scratch rule 4).
- Check `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass; on ENOSPC report the free
  space you saw and stop.
- The lane's config planes (~/.config/hypr, waybar, walker, terminals, omarchy theme) are READ-ONLY: you may read bytes but never
  write them; never connect a compositor socket; never mutate a running service. Never write, commit, fetch or push into
  /home/vgpnk/Projects/shokuknow.
# Tooling authorization (operator, 2026-10-19) and pacman guard
- You may install or upgrade tools that help your task (read /home/vgpnk/.omp/agent/RULES.md first; official channels only:
  uv tool install, npx, official release binary into ~/.local/bin, cargo/npm -g; record tool/version/channel/reason in your
  report). ALL PACMAN TRANSACTIONS ARE PAUSED HOST-WIDE: never run pacman -S/-Sy/-Syu/-U/-R; if you need a system package,
  use uv/npx/a binary or say so in your report. Never restart a host service.
- If you need REA, use the CLI (npx -y rea-agents@6.5.0 <command>), never an xd://mcp__rea_* device.
"""
for _k, _v in {"L": LANE, "W": W, "B": BASE, "C": CLAIMS, "S": SCR}.items():
    CONTEXT = CONTEXT.replace("%(" + _k + ")s", _v)


def F(s):
    for _k,_v in {"W":W,"L":LANE,"B":BASE,"C":CLAIMS,"S":SCR}.items():
        s=s.replace("%("+_k+")s",_v)
    return s

def sub(s):
    assert "\t" not in s
    return s

ITEMS = [
# ---------------- C1 build: the tool ledger ----------------
dict(name="ExecLedgerPopulation", role="executor",
target="""The C1 population and the ledger draft for the round-51 tool ledger.""",
task="""Read %(W)s/claims.md (C1) first. Derive the C1 population exactly as the frozen predicate defines it: every file under
tools/, every quality/*.py, every quality/counters/*.py at round base %(B)s (use read-only git: git ls-tree -r <base> -- tools quality).
Exclude __pycache__, .pyc, .txt, .json, .sh non-.py files are included only under tools/. Draft quality/tool-ledger.md INTO YOUR
SEAT DIR (same basename): one row per population file with (a) repo-relative path, (b) one-line description of what it does
(read the file header/docstring - do not invent), (c) an accountability pointer: an existing repo file (PROVINCE.md,
SCORECARD.md, corpus/README.md, corpus/lessons/<specific>.md, corpus/knowledge/<specific>.md) that contains the file's basename -
grep to verify each pointer actually contains the basename and record the line number; if no existing file names the tool,
pointer = your report with a noted gap. Also write population.json listing every population path. Deliverables: tool-ledger.md,
population.json in your seat dir."""),

dict(name="ExecLedgerGate", role="executor",
target="""The C1 checker quality/check-tool-ledger.py.""",
task="""Read %(W)s/claims.md (C1) - the frozen PRED-C1-r51 sentence is the contract. Write quality/check-tool-ledger.py INTO YOUR
SEAT DIR (python3, stdlib only): given --repo and --rev (read-only git at that rev, like sibling counters
quality/counters/c1-r50-bind-entry.py), it (1) derives the population = files under tools/ + quality/*.py + quality/counters/*.py
at --rev (same exclusion rules as the predicate); (2) parses quality/tool-ledger.md rows (one per file: path, description,
pointer); (3) prints one LEDGER line: population=<P> ledger_rows=<R> uncovered=<n> dangling=<n> bad_pointer=<n> empty_desc=<n>
and exits 0 iff P>0, R==P, uncovered=0, dangling=0, bad_pointer=0, empty_desc=0 - else exit 1; a missing ledger at --rev prints
verdict=TARGET_MISSED ledger=absent, exit 1; unreadable rev/setup errors exit 2. bad_pointer = pointer path missing at rev or its
bytes lacking the basename. --selftest (hermetic, TMPDIR-honouring fixtures only): green ledger passes; each of the 5 control
classes (omitted file, pointer lacking basename, empty description, dangling row, absent ledger) fails. Run the selftest in your
scratch dir and paste the transcript. Deliverable: check-tool-ledger.py + selftest transcript in your seat dir."""),

dict(name="ExecLedgerCounter", role="executor",
target="""The C1 counter quality/counters/c1-r51-ledger.py (PRED-C1-r51).""",
task="""Read %(W)s/claims.md (C1). Write quality/counters/c1-r51-ledger.py INTO YOUR SEAT DIR, mirroring the frozen predicate
sentence byte-for-byte in its docstring: --repo --rev --work (scratch clone under --work via git clone --shared, TMPDIR-honouring,
no /tmp hardcoding; the clone is removed on exit). It runs the seat's check-tool-ledger.py (path supplied via --checker, default
quality/check-tool-ledger.py) at --rev, requires its LEDGER line clean, requires --selftest ok, and prints the exact final line
`C1_R51: population=<P> ledger_rows=<P> uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=<rev>`
exit 0 only when all hold; any ledger defect or absent ledger -> `verdict=TARGET_MISSED` with the failing fields, exit 1; setup
errors exit 2. At --rev=%(B)s (round base) it must print TARGET_MISSED ledger=absent exit 1. Run it against base using the CURRENT
tree's ledger as a stand-in is NOT valid for the base case - the base tree has no ledger file, which is the point; test that path.
Deliverable: c1-r51-ledger.py + run receipts for base and for a fixture tree with a complete ledger."""),

dict(name="ScrLedgerRows", role="scribe",
target="""Descriptions and pointer provenance for the tool-ledger rows.""",
task="""Read %(W)s/claims.md (C1) and the tool inventory in %(L)s/PROVINCE.md (the round-23/36/45/46 tables). For EVERY file under
tools/ and the quality/*.py + quality/counters/*.py instruments, write one ledger row's prose: a one-line description (<=20 words,
factual, from the file's own docstring/header) plus the accountability pointer with its verified line number. Mark each row's
accountability class: province-table (named in PROVINCE.md), scorecard-capability (named in SCORECARD.md capabilities),
lesson-named (named in a corpus/lessons file), knowledge-named, or GAP (no existing file names it - list these separately; gaps
are expected for older counters and are themselves a finding). Output: ledger-rows.md in your seat dir with the full row set and
the gap list. Do not write outside your seat dir."""),

dict(name="RevLedgerPred", role="reviewer",
target="""The frozen C1 predicate sentence in claims.md - attack it.""",
task="""Read %(W)s/claims.md (C1) closely. Your job is to break PRED-C1-r51 as worded: construct in your seat dir (as mock
descriptions + arithmetic, no full implementation needed) every do-nothing or cheating artifact that would still print
TARGET_MET: e.g. a ledger whose pointer files merely contain the basename in a comment; a ledger that lists each file but whose
descriptions are copied from one another; a population derivation gap (a file under tools/ that is a .sh - the predicate covers
tools/ wholesale; does the population rule exclude anything ambiguously, like quality/receipts/ or __pycache__?); a ledger row
whose description is whitespace-only (is empty_desc defined against whitespace?); the counter reading the WORKTREE instead of the
--rev objects. For each attack: verdict would it pass the frozen predicate (yes/no) + the one-sentence fix that closes it WITHOUT
changing the predicate's intent. Output: attacks.md in your seat dir, one attack per numbered section, each ending PASS/MISS and
the closing fix."""),

dict(name="CritLedgerControls", role="critic",
target="""The C1 do-nothing control set.""",
task="""Read %(W)s/claims.md (C1) and §9 claim sizing of the round prompt. Design the cheapest control set that skips the claimed
work yet must MISS: (a) ledger omitting tools/mado-keysym.py (the round-50 miss, replayed); (b) ledger whose rows for the 5 newest
tools point at PROVINCE.md lines that do NOT contain those basenames; (c) ledger with empty descriptions for all counters;
(d) ledger listing 3 files that are not in the population; (e) the pre-round tree itself (no ledger). For each control write the
expected counter output line (exact field values) and expected exit code, as a fixture spec the L1 can implement blind. Also state
the cheapest do-nothing control that WOULD pass (if none, say why the population-vs-ledger diff has no shortcut). Output:
controls-c1.md in your seat dir."""),

dict(name="MutLedgerGate", role="mutation-tester",
target="""The C1 checker design - mutation-test it on paper.""",
task="""Read %(W)s/claims.md (C1) + the sibling checker quality/check-evidence-pointers.py for the house style. List 12 mutations of
the check-tool-ledger.py design (population glob, row parse, basename containment, exit-code mapping, selftest arms), each with:
mutant description, which fixture/control it must FAIL against, and whether the hermetic --selftest as specified would catch it.
Flag any mutation that would pass ALL specified controls (a live mutant) - those become freeze-time additions. Output:
mutations-c1.md in your seat dir."""),

# ---------------- C2 build: the dispatcher entry ----------------
dict(name="ScoutDispatchMap", role="scout",
target="""Source recon for the Hyprland 0.56.2 dispatcher surface.""",
task="""Read %(W)s/claims.md (C2). The committed pins under %(L)s/.ufo/waves/round-50/fetch/ include Hyprland sources at
efb50993780079460b0cbed1363e2166a2de1d9f (v0.56.2). Map the dispatcher-execution surface: where m_mDispatchers is declared and
registered, handleKeybind's dispatch call, argument parsing/splitting for dispatchers, the submap special cases, the pass
dispatcher, and how `hyprctl dispatch` reaches the same code (HyprCtl.cpp). Use ONLY the pinned local copies and read-only git -
no network needed if the pins cover it; note any file you need fetched (exact URL + revision) as a fetch request for
ExecFetchDispatch. Verify against %(L)s/corpus/knowledge/*.md that no admitted entry already covers dispatcher semantics (grep
dispatcher|dispatch across corpus/knowledge and report the closest rows). Output: dispatch-map.md in your seat dir: per-source
file, the relevant line ranges, the mechanism each teaches, and the fetch-request list."""),

dict(name="ExecFetchDispatch", role="executor",
target="""The round-51 fetch pins.""",
task="""Read %(W)s/claims.md (C2) and ScoutDispatchMap's fetch requests (if its report exists when you run; otherwise use your own
read of the pinned Hyprland tree under %(L)s/.ufo/waves/round-50/fetch/ plus the hyprland-wiki pins). Fetch the needed sources at
commit-pinned URLs (raw.githubusercontent.com only, the efb50993... revision for Hyprland code, the d5f07c60... revision for wiki
content) INTO YOUR SEAT DIR under fetch/ (these are drafts; the L1 moves them to %(W)s/fetch/ at integration): one file per URL,
basename prefixed by source (e.g. Hyprland-KeybindManager.cpp), plus a SHA256SUMS manifest. Every file must be byte-fetched with
curl -fsSL and sha256-verified. Record each URL, revision, byte size and sha256 in fetch-manifest.json. Also fetch (do not
extract from pins) any source ScoutDispatchMap flagged. No writes outside your seat dir. Deliverables: fetch/, SHA256SUMS,
fetch-manifest.json."""),

dict(name="ScrDispatchEntry", role="scribe",
target="""The draft entry corpus/knowledge/hyprland-dispatcher-dispatch-r51.md.""",
task="""Read %(W)s/claims.md (C2) and the house bar in %(L)s/corpus/QUALITY.md (esp. criterion 100: a host-consequence model cites
the line that SETS the state). Draft corpus/knowledge/hyprland-dispatcher-dispatch-r51.md INTO YOUR SEAT DIR from the pinned
sources (use %(L)s/.ufo/waves/round-50/fetch/ pins and, if present, %(W)s/w1/ExecFetchDispatch/fetch/): how a keybind's
dispatcher+arg string is stored at parse time, looked up in m_mDispatchers at key-press time, how the argument is split/parsed,
the submap and pass special cases, and how hyprctl dispatch reaches the same path - each mechanism claim carrying a pin cite
(file:line, revision). Include: (1) a `source:` block listing the new S-rows the entry will cite (S364+ placeholders);
(2) a `## Held ground` section with >=3 `held:` citations, each naming corpus/knowledge/<file>:<line> at base %(B)s whose line
contains the fact's pinned key tokens (verify by reading the held file at that line - e.g. facts the bind-key-match r50 entry
holds that this entry reuses); (3) a pin-manifest table (pin path, sha256, cited lines). Keep overlap with the r49/r50
bind-key-match entries minimal: do not re-explain key matching; the entry starts where the match ends. Output: the entry draft +
held-citations.md listing each held citation, its key tokens, and the verification line text."""),

dict(name="ScrRowsDispatch", role="scribe",
target="""The new registry rows S364+ (draft).""",
task="""Read %(W)s/claims.md (C2), the SOURCES contract in /home/vgpnk/Projects/shokunin/CORPUS.md (section SOURCES.md - where a
shokunin learns), and the row shape in %(L)s/corpus/SOURCES.md. From the pins (round-50 fetch dir + %(W)s/w1/ExecFetchDispatch/fetch/
if present) draft 3-6 new registry rows numbered S364..S369, each: id, source title - canonical commit-pinned URL, kind (code/docs),
tier A, scope (the exact claim the row supports), anchor (file:line + revision), teaches (one grounded benefit), status mined,
opened 2026-10-27, recheck on-release, used-by corpus/knowledge/hyprland-dispatcher-dispatch-r51.md. Every row carries a <=25-word
located quote whose words appear verbatim at the pin's cited line - verify each by grepping the pin and paste the verifying grep
output. Only rows the entry actually cites; a row no mechanism claim needs is a violation of CORPUS.md rule 4. Output: rows.md
(table rows + per-row quote-verification transcript) in your seat dir."""),

dict(name="ExecCounterC2", role="executor",
target="""The C2 counter quality/counters/c2-r51-dispatch-entry.py (PRED-C2-r51).""",
task="""Read %(W)s/claims.md (C2) - the frozen PRED-C2-r51 sentence is the contract. Write quality/counters/c2-r51-dispatch-entry.py
INTO YOUR SEAT DIR (python3 stdlib, TMPDIR-honouring, --work scratch): at --repo --rev it checks clauses (a)-(d) exactly as frozen:
(a) entry exists and is indexed in corpus/README.md (the index row naming the entry path); (b) the entry's source block cites >=2
rows S364-S379 in corpus/SOURCES.md at rev with status mined + opened 2026-10-27, each bound to a pin named in the entry's pin
manifest existing at rev, whose cited line contains the row's quote verbatim and whose word count <=25; (c) word-8-gram shingle
overlap of the entry body vs every corpus/knowledge/*.md at BASE 6ca8c559a4a3d6d361101592116eea2bc7452437 (frozen constant in the
counter) and vs every file under .ufo/waves/round-*/candidate/ (recursive) is <=30% per file - print the top-3 overlap values;
(d) >=3 distinct held: citations each naming corpus/knowledge/<file>:<line> at BASE whose line contains every pinned key token.
Final line exactly `C2_R51: clauses=abcd clauses_met=<n> admitted=<0|1>/1 verdict=TARGET_MET|TARGET_MISSED rev=<rev>`; exit 0 only on
4/4. At base rev it must print admitted=0/1 verdict=TARGET_MISSED exit 1. Setup errors exit 2. Test: run at base (must MISS) and
against a fixture tree built in scratch holding the round-50 entry bytes at the C2 path (must MISS via clause c; paste the receipt).
Deliverable: c2-r51-dispatch-entry.py + both run receipts."""),

dict(name="RevNovelty", role="reviewer",
target="""The C2 clause (c) novelty baseline - audit it for holes.""",
task="""Read %(W)s/claims.md (C2). Attack the shingle novelty clause: (1) compute the ACTUAL word-8-gram overlap of
%(L)s/corpus/knowledge/hyprland-bind-key-match-r50.md against the round-49 candidate
%(L)s/.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md (real computation, paste outputs) - is 81.7% reproducible;
(2) try synonym/paraphrase shingle evasion on paper: does an entry that rewords the r50 entry at ~50% shingle overlap pass a 30%
threshold while conveying no new ground? is the threshold defensible - recommend a number with the computation behind it;
(3) find any corpus/knowledge file or candidate file the baseline misses (e.g. files under .ufo/waves/round-*/w1|w2/** seat
reports that carry candidate text - the frozen baseline only names candidate/; does that matter?); (4) check the baseline pins the
comparison corpus at BASE - an entry that quotes an OLDER entry verbatim from its own rev... can that happen given the corpus only
grows? Output: novelty-audit.md with the computations and a keep/change recommendation; if you recommend changing the predicate,
state the exact new sentence."""),

dict(name="CritHeldFacts", role="critic",
target="""The C2 clause (d) held-fact bindings - falsify them.""",
task="""Read %(W)s/claims.md (C2) and the r50/r49 bind-key-match entries. Attack clause (d): design an entry whose 3 held:
citations each point at real held lines but whose key tokens are chosen so the citation is vacuous (tokens like `the` or
`keybind` that appear anywhere). What stops that - must the counter pin token sets, and who chooses them? Write the exact
vicious fixture (3 citations, token sets, the counter's verdict under the frozen wording). Also: is >=3 the right floor, and does
clause (d) as frozen distinguish reuse-of-held-ground from novelty? Output: held-attacks.md in your seat dir with the fixture and
a keep/change recommendation."""),

dict(name="MutC2Counter", role="mutation-tester",
target="""The C2 counter design - mutation list.""",
task="""Read %(W)s/claims.md (C2) + a sibling counter (quality/counters/c1-r50-bind-entry.py). List 12 mutations of the
c2-r51 counter design (index check, row-status check, pin manifest, quote verbatim, 25-word count, shingle set, 30% compare,
held-token containment, exit codes), each: mutant, control/fixture it must miss, whether the round's own do-nothing controls catch
it. Flag live mutants (pass everything specified) for freeze-time addition. Output: mutations-c2.md."""),

# ---------------- frontier / routed / assimilation ----------------
dict(name="ScoutQuarantine", role="scout",
target="""The 13-row mado absent-defect register slice - verdicts.""",
task="""The round-50 lesson left adoption closed until the lane's absent-defect register slice is hand-checked. Read
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (READ-ONLY; never write there) and extract
the mado rows per the §10 quarantine slice command (lane cell mado, round cell, S-id cell). For EACH row: fetch the cited source,
locate the quoted text; verdict absent (quote not present - reason in Gate block), present (quote found - record the located
anchor), or unverifiable (source unreachable / prose class). Note: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/
was reported GONE on 2026-10-27 (chousa r56 L0) - if a cited capture is cache-bound and gone, that row is unverifiable, say so.
Output: quarantine-verdicts.md, one section per row: id, URL, verdict, evidence. These verdicts stay in the lane; nothing is
appended to the register or any campaign file.""" % {}),

dict(name="ScoutAssim", role="scout",
target="""The merge/mado staged package and id-collision guard for round 51.""",
task="""Read /home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md and SOURCES.append.md (READ-ONLY). (1) Theme scan: does any
staged entry match this round's claims (dispatcher/dispatch semantics; tool-ledger/operability) or PROVINCE.md's desktop scope?
Keyword scan + one-line reason per candidate. (2) Run the id-collision guard per §10 into your seat dir: lane registry ids (grep
-oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' %(L)s/corpus/SOURCES.md) vs staged ids; intersection count; paste both id lists and the
collision count. (3) If any staged row is a candidate, note the quarantine status (ScoutQuarantine's verdicts) it would inherit.
Output: assimilation-scan.md."""),

dict(name="ConnSibling", role="connector",
target="""Sibling-overlap scan: dispatcher/ledger themes across lanes.""",
task="""Scan the sibling lane repos under /home/vgpnk/Projects/shokunin (read-only; the *-shokunin dirs) for overlap with this
round's two claims: (1) does any sibling hold dispatcher/dispatch knowledge or counters that would duplicate C2 (grep
dispatcher|m_mDispatchers|handleKeybind across tsukuroi, chousa, kake, kumitate, kotoba SKILL.md/corpus); (2) does any sibling
already operate a tool-ledger/instrument-ledger checker that C1 would duplicate (grep ledger|inventory.*tools)? Report per sibling:
overlap found (with path:line) or clean. Also flag adjacency-duty items: evidence that belongs to another lane's province that this
round's seats surfaced. Output: sibling-scan.md.""" % {}),

dict(name="RevRouted50", role="reviewer",
target="""Round-50 routed defects D1 and D4/M50-9 - implementation receipts.""",
task="""Two routed items: (1) D1 - the round-50 report and LOG assert a final two-wave WAVE-DONE receipt at tip 74782d39 that was
never committed; this round must not repeat that: design (as a short procedure + the exact command lines, into your seat dir) the
round-51 integration-time receipt procedure: run quality/check-wave-done.py at the FINAL integration tip for w1 and w2 after both
results files land, commit the receipt BEFORE the report, and cite only the committed receipt. Check the checker supports being run
twice (once per wave) and its --round flag semantics by reading quality/check-wave-done.py. (2) D4/M50-9 - the round-50 fetch
checksum manifest has an unverifiable self-entry: read %(L)s/.ufo/waves/round-50/fetch/SHA256SUMS, identify the self-entry, and
write the corrected manifest for ROUND-51's fetch dir design (the manifest must never list its own checksum): the convention the
L1 should enforce at %(W)s/fetch/SHA256SUMS. Do NOT edit round-50 bytes. Output: routed-d1-d4.md with both procedures.""" % {"L": LANE, "W": W}),

dict(name="RevQuality103", role="reviewer",
target="""QUALITY criterion 103 draft: wave-done receipt at integration tip.""",
task="""Read %(L)s/corpus/QUALITY.md criteria 100-102 (shape and bar) and quality/check-wave-done.py. Draft criterion 103 into your
seat dir (criterion text + check tool description, following the house style): a round report may cite a WAVE-DONE/settled verdict
only if a receipt for that verdict at the report's integration revision is committed in the round's wave dir (D1's generalization).
Include the red-arm receipt (it must fail on round-50's tip state) and green-arm description, and a Declared limit. Do not edit
QUALITY.md (L1 integrates). Output: criterion-103.md."""),

dict(name="ScrLesson51", role="scribe",
target="""The corpus/lessons/round-51.md skeleton.""",
task="""Read %(L)s/corpus/lessons/round-50.md for house shape. Draft corpus/lessons/round-51.md INTO YOUR SEAT DIR with: header
(base, claims commit, wave summary - leave TBD), a `## Gate` section skeleton with the sub-blocks the round must fill (admit lines
for S364+ with URL/access date/<=25-word quote; reject lines; status/recheck/used-by changes old->new; assimilation verdicts
>=1 admit >=1 reject or none-reason; the quarantine verdict summary), and a `## Mistakes` section holding M51-1 (drafted from the
round-50 spot-check: the final WAVE-DONE receipt was claimed but not committed at the tip - evidence
corpus/lessons/round-50-verifier-spotcheck.md §2 D1 - captured-by: none pre-round-51 - fix: criterion 103 + integration-time
receipt procedure) with the `fix shown able to fail` arm left TBD for the L1. Output: round-51.md (draft)."""),

dict(name="SentScope51", role="sentinel",
target="""Scope and safety sweep of the round's in-flight seat writes.""",
task="""Mid/late-wave sweep: list every file created under %(W)s/w1/ so far (find), and check: (1) nothing outside %(W)s/w1/ and
seat dirs was written by seats (git status --porcelain in the lane must show no untracked files outside .ufo/waves/round-51);
(2) no pin or receipt contains secret-shaped material (session tokens, op:// refs, private URLs - run a shape scan like
quality/check-session-material.py would; you may RUN quality/check-session-material.py read-only against the wave dir and paste
its verdict); (3) no hardcoded /tmp paths in drafted tools; (4) fetch pins are byte-fetched upstream sources only (no local
private paths). Output: scope-sweep.md with findings per check."""),

# ---------------- attack density: predicates, controls, prior instruments ----------------
dict(name="CritLedgerForgery", role="critic",
target="""Forge a passing tool ledger.""",
task="""Read %(W)s/claims.md (C1). Try to design a ledger that passes PRED-C1-r51 while doing no real accountability work:
e.g. every pointer = a single new file that contains every basename in a comment (does that pass? is it a real accountability?
argue both); descriptions auto-generated from filenames (empty_desc clean but content-free - does the predicate care?);
pointer to the ledger itself (circular). For each forgery: exact verdict under the frozen predicate + whether it constitutes
harmed operability + the minimal closing fix. Output: forgery-c1.md."""),

dict(name="MutLedgerCounter", role="mutation-tester",
target="""The C1 counter design - second mutation pass (population derivation).""",
task="""Read %(W)s/claims.md (C1). Focus on the population derivation only: mutations of the glob set (tools/ including .sh?,
quality/*.py vs quality/**/*.py, counters json fixtures excluded?), the basename-containment test (case sensitivity, subdirectory
basenames), and the --rev vs worktree confusion (counter must read --rev objects, never the live tree). 8 mutations, each with its
control. Live mutants flagged. Output: mutations-c1b.md."""),

dict(name="RevC2Predicate", role="reviewer",
target="""The frozen C2 predicate - attack clauses a-d as worded.""",
task="""Read %(W)s/claims.md (C2). Construct per clause the cheapest artifact that passes it while defeating the intent:
(a) an index row that names the entry in a comment - does the index check grep data rows or any mention?; (b) a quote that is
<=25 words and verbatim but lifted from an IRRELEVANT line of the same pin (teaches nothing - does binding care?); (c) threshold
evasion via sentence-shuffling (measure on the r49->r50 pair: what does shuffling do to 8-gram overlap?); (d) held citations to
held lines with generic tokens. For each: PASS/MISS under the frozen sentence + the one-sentence closure fix. Where the fix
changes the predicate, write the exact replacement sentence. Output: attacks-c2.md."""),

dict(name="CritC2Stub", role="critic",
target="""The best stub entry under the frozen C2 predicate.""",
task="""Read %(W)s/claims.md (C2) and the r50 entry. Design the maximal-overlap stub that still passes: take the r50 entry,
strip/reword minimally, add 2 new-row citations with real pins, add 3 held citations. Compute the stub's actual shingle overlap
against the r50 entry (real computation in scratch). Two questions: (1) at what overlap does the stub still teach the dispatcher
surface - i.e. is high overlap with a DIFFERENT-surface entry even a violation? Argue whether clause (c)'s baseline should be
same-surface only (the predicate says every knowledge file - is that overbroad, catching legitimate cross-references?);
(2) give the L1 a keep/change recommendation with numbers. Output: stub-c2.md with the computation."""),

dict(name="RevSessionGate", role="reviewer",
target="""Post-landing attack on round-50 instruments (session gate v3, hostguard, wave-done).""",
task="""Round-50 w2 bounded the session-material gate: a 7,046-byte canned-transcript/all-rule-spray replacement still scores
TARGET_MET. Read quality/check-session-material.py, quality/counters/c2-r50-session-gate.py, quality/check-wave-done.py and
quality/check-round-outcome-first.py. Post-landing findings only (never rewrite round-50 bytes): for each instrument, one
section: the strongest remaining cheat, a concrete round-51+ fix candidate (new criterion or gate arm), and whether the fix
belongs in this round's scope or a later one. Output: postlanding-attacks.md.""" % {}),

dict(name="RevWaveDone", role="reviewer",
target="""The wave-done checker vs the D1 defect - can it re-happen in round 51?""",
task="""Read quality/check-wave-done.py fully. Question: if the L1 (a) writes w1.ready, (b) gets WAVE-DONE w1, (c) writes
w2.ready, (d) gets WAVE-DONE w2, (e) integrates and commits everything EXCEPT a final check run, then files the report - does ANY
committed gate catch the missing final receipt? Test the checker against the round-50 tree state (git worktree/show at 74782d39
in scratch): does --round 50 at that rev read waves=1 or waves=2, and would a committed receipt at 8dbbf61a plus a later c12b588e
change what the tip says? Output: wavedone-analysis.md with the exact commands and outputs, plus the one-line procedure addition
that makes D1 impossible (for the L1 to adopt).""" % {}),

dict(name="MutToolLedger", role="mutation-tester",
target="""The ledger row-parse - mutation list.""",
task="""Read %(W)s/claims.md (C1) and the tool-ledger.md draft in %(W)s/w1/ExecLedgerPopulation/ if present (else design the row
grammar yourself and say so). Mutation-test the row grammar: 8 mutations (extra column, pipe in description - forbidden by
SOURCES-house rules for md tables but is the ledger a census table? decide and defend, whitespace-only description, pointer to
directory, duplicate row, wrong order, missing description, unicode basename). Each with expected checker verdict. Output:
mutations-ledger.md."""),

dict(name="CritEntryTruth", role="critic",
target="""Truth audit of the drafted dispatcher entry (false-claim hunt).""",
task="""When %(W)s/w1/ScrDispatchEntry/ holds a draft: read it line by line against the pins it cites (every file:line - open the
pin, compare). List every sentence whose claim is not supported by the cited line (overreach, wrong direction, stale line), each
with the pin evidence and a corrected sentence. If the draft does not exist yet, instead audit the r50 bind-key-match entry's
dispatcher-adjacent sentences for the same class and report those. Output: truth-audit.md."""),

dict(name="RevRowsTruth", role="reviewer",
target="""Row-quote verification for S364+ drafts.""",
task="""When %(W)s/w1/ScrRowsDispatch/rows.md exists: for EVERY drafted row, independently grep the named pin at the cited line
and verify the <=25-word quote verbatim + count the words; report per row VERIFIED/REFUTED with your own grep output (do not
trust the scribe's transcript). Also verify the URLs are commit-pinned raw URLs (no moving targets). If the draft does not exist
yet, verify the same way the rows in %(L)s/corpus/SOURCES.md S352-S363 against the round-50 pins and report any drift. Output:
rows-verify.md."""),

dict(name="ScrSearchLog", role="scribe",
target="""The SOURCES.md search-log entry for round 51.""",
task="""Read the Search log section of %(L)s/corpus/SOURCES.md. Draft the round-51 entry into your seat dir (search-log.md):
question (how does a matched keybind's dispatcher string execute at 0.56.2), where searched (pinned Hyprland tree at efb50993,
hyprland-wiki at d5f07c60, held corpus), date 2026-10-27, identified/screened/included/excluded counts (fill from the rows draft if
present: identified = sources opened, screened = relevant to dispatch phase, included = rows S364+, excluded = with reasons, e.g.
already held as S352-S353, no commit anchor, off-surface), stop rationale. One bounded note, PRISMA-inspired. Output: search-log.md.
"""),

dict(name="RevFreezeReg", role="reviewer",
target="""The freeze registration requirements for round 51.""",
task="""Read %(W)s/claims.md, %(L)s/.ufo/waves/round-50/registration.md and criterion 64 (freeze-time checks) in
%(L)s/corpus/QUALITY.md. Draft registration-req.md: the exact checklist the L1 must satisfy at freeze time for round 51 -
counter files exist at the freeze commit, named in registration; controls fixtures + expected outputs committed; base receipts
(C1 base TARGET_MISSED, C2 base TARGET_MISSED) committed; counter docstrings quote the frozen predicate sentence byte-for-byte;
no predicate rewording after any seat scored. Output: registration-req.md."""),

dict(name="ExecControlsC1", role="executor",
target="""The C1 control fixtures and expected receipts.""",
task="""Read %(W)s/claims.md (C1) + %(W)s/w1/CritLedgerControls/controls-c1.md if present. Build the control fixture trees in your
scratch dir (git init sandbox clones - verify rev-parse toplevel == your dir BEFORE any commit; never touch the lane or fleet):
ctl-a ledger omitting tools/mado-keysym.py; ctl-b pointers lacking basenames for the 5 newest tools; ctl-c empty descriptions;
ctl-d 3 dangling files; ctl-e base tree itself. For each: run the check-tool-ledger.py draft from %(W)s/w1/ExecLedgerGate/ (or your
own faithful build of the frozen predicate if absent) and record expected-vs-actual. The freeze commits these fixtures only as
SPEC + receipts (fixture trees stay in scratch and are deleted). Output: controls-c1/ dir with spec.md + expected.txt +
actual-run receipts where a runnable draft existed."""),

dict(name="ExecControlsC2", role="executor",
target="""The C2 control fixtures and expected receipts.""",
task="""Read %(W)s/claims.md (C2) + the r49 candidate bytes at %(L)s/.ufo/waves/round-49/candidate/. Build in scratch: ctl-a = base
tree + r50 entry bytes at the C2 path (expect MISS via clause c); ctl-b = base tree + r49 candidate at the C2 path (expect MISS);
ctl-c = a new entry with held citations whose pinned tokens are absent from the cited lines (expect MISS via d); ctl-d = entry
citing rows with no pins (expect MISS via b). Run the c2 counter draft from %(W)s/w1/ExecCounterC2/ if present (else record the
spec only). Output: controls-c2/ with spec.md + receipts."""),

dict(name="RevC1Base", role="reviewer",
target="""The C1 base receipt - independent red-before.""",
task="""Independently reproduce the C1 base measurement: run the c1-r51 counter draft (from %(W)s/w1/ExecLedgerCounter/ if
present, else verify the predicate's base clause by inspection) at --rev 6ca8c559a4a3d6d361101592116eea2bc7452437 in a scratch
clone and confirm TARGET_MISSED ledger=absent exit 1. Also verify by read-only git that no quality/tool-ledger.md or
check-tool-ledger.py exists at that rev. Paste the full receipt. Output: base-c1-receipt.txt + notes."""),

dict(name="CritBaseC2", role="critic",
target="""The C2 base receipt - independent red-before.""",
task="""Independently reproduce the C2 base measurement: at --rev 6ca8c559a4a3d6d361101592116eea2bc7452437, verify by read-only
git that corpus/knowledge/hyprland-dispatcher-dispatch-r51.md is absent and run the c2 counter draft from
%(W)s/w1/ExecCounterC2/ if present to confirm admitted=0/1 verdict=TARGET_MISSED exit 1. Also verify no rows S364+ exist in
corpus/SOURCES.md at base (the registry ends at S363). Paste the full receipt. Output: base-c2-receipt.txt + notes."""),

dict(name="SentPrivacy", role="sentinel",
target="""Privacy scan of the round-51 wave dir receipts.""",
task="""Run %(L)s/quality/check-session-material.py (read-only) against %(W)s (the whole round dir) and paste the verdict; then
hand-check the fetch pins and receipts for host-private material (home paths other than the lane's declared surfaces, process
tables, socket tables, account names). Round 38's 190 KB ss-table incident is the class to prevent BEFORE commit. Output:
privacy-scan.md with the gate verdict and per-file findings."""),

dict(name="RevengerLedger", role="revenger",
target="""Root-cause the round-50 ledger miss (how hostguard/keysym fell out).""",
task="""Reverse-engineer from committed bytes why the round-50 wave-seat tool ledger missed tools/mado-hostguard.py and
tools/mado-keysym.py: find the ledger artifact the round-50 seat produced (under %(L)s/.ufo/waves/round-50/), determine its
population derivation, and name the exact step where the two tools escaped it (ordering? seat-knowledge boundary? the tools
landed in w2 while the ledger was a w1 artifact?). Then derive the invariant a lane-level ledger must satisfy so the class cannot
recur (population derived from the tree at scoring time, not from any prior seat's knowledge). Output: ledger-rootcause.md."""),

dict(name="SimplifierLedger", role="simplifier",
target="""YAGNI pass on the C1/C2 instrument designs.""",
task="""Read the drafts in %(W)s/w1/ExecLedgerGate/, ExecLedgerCounter/, ExecCounterC2/ as they exist (review what's there; if a
draft is missing, note it and review the predicate instead). For each instrument: list any feature beyond the frozen predicate
( Extra CLI flags, duplicate checks, speculative generality) that can be deleted without weakening the frozen clauses - the
freeze-then-attack pattern punishes overbuilt counters (more surface for live mutants). Output: yagni.md with per-instrument
keep/delete recommendations."""),

dict(name="ScoutConsiderthese", role="scout",
target="""The considerthese grounding path for C1.""",
task="""Read %(L)s/considerthese/2026-10-26.md proposal 2 (running ledger of live-state tools). Verify the claim that C1's tool
ledger implements its core direction - and name precisely where it falls short of the proposal (the proposal asks for last-live-run
and verdict per tool; C1 covers accountability, not live-run freshness). Write the lesson-ready row: proposal pointer + date,
what landed, what stays open. Also check proposals 1-6 for any other still-unimplemented item this round already covers (say so)
or must refuse (say why). Output: considerthese-row.md."""),

dict(name="RevSHONEN", role="reviewer",
target="""The round-51 report/SHONEN shape - one line per box.""",
task="""Read %(L)s/SHONEN.md (the four boxes and their current [~] states) and the round-50 spot-check defect D2 (one summary line
covered four boxes; the contract is one line per box). Draft the exact SHONEN section the round-51 report must carry: one line per
box, [x] only with a named non-author verifier, [~] with a resolvable evidence pointer, [ ] if untouched - with the pointer each
[~] will cite at round end. Output: shonen-section.md."""),

dict(name="ExecDiskHygiene", role="executor",
target="""Scratch-rule-4 verification of the round's drafted tools.""",
task="""When the C1/C2 counter and checker drafts exist under %(W)s/w1/: grep every drafted .py for hardcoded /tmp or /var/tmp
writes (mkdtemp(dir=, open('/tmp, NamedTemporaryFile without dir=), and verify each honours TMPDIR or --work. Run each draft's
--selftest with TMPDIR pointed at your scratch dir and confirm green. Also verify the drafts run under python3 -I. Output:
disk-hygiene.md with per-file verdicts and the selftest receipts."""),
]

spec = {
    "wave": "w1",
    "context": CONTEXT,
    "reportDir": ".ufo/waves/round-51/w1",
    "items": [{"name": it["name"], "role": it["role"],
               "prompt": sub(F(GODSPEED + "# Target\n" + it["target"].strip()) + "\n# Task\n" + it["task"].strip() + "\n")}
              for it in ITEMS],
}
out = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/w1-spec.json"
with open(out, "w") as f:
    json.dump(spec, f, indent=1)
import collections
print("items:", len(ITEMS))
print(collections.Counter(it["role"] for it in ITEMS))
