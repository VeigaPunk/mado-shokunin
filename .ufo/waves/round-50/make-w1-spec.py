#!/usr/bin/env python3
"""Generates .ufo/waves/round-50/w1-spec.json (round 50, wave w1 = BUILD + attack of the round-49 instruments, policy v1).

w1 carries the 38 never-dispatched round-49 w2 items (.ufo/waves/round-49/w2-items.json; round-49 closure D1), each retargeted
to the round-50 facts by a per-item note, plus the round-50 build items. Nothing of round 50 is frozen yet: the L1 freezes after
w1 returns; wave w2 attacks the round-50 freeze.
"""
import collections
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-50"
W49 = LANE + "/.ufo/waves/round-49"
BASE = "8ae47b957034ae21012bbf09173cca2c48be345e"
CLAIMS = "13631f24050f22db92bf5bd33e0f4d014192992e"
B49 = "03e4ae76aff7a4be59cb69970dd553baa319695a"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r50"
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
mado round 50 (hyaku run 9, 2026-10-27), wave w1 = BUILD + ATTACK of the round-49 instruments (policy v1). Lane repo: %(L)s (desktop and
compositor craft: the Hyprland/waybar/walker/terminal/keyboard config plane of this host; axes coverage + operability). Base (lane tip at round
start) %(B)s; claims committed at %(C)s: read %(W)s/claims.md FIRST, then %(L)s/corpus/lessons/round-49-verifier-spotcheck.md (the outside
check of round 49; its section 6 routes defects D1-D8 to this round). Nothing of round 50 is frozen yet: the L1 freezes predicates, counters,
fixtures and controls AFTER this wave returns, and wave w2 attacks that freeze. Your output feeds the freeze and the round's corrections.
- Round 49 (base %(B49)s, freeze dd2e827e, C1 data 430d2569) LANDED tools/mado-keysym.py (sha256 dcc13cce3b71...0265, byte-equal to
  %(W49)s/candidate/mado-keysym.py): it prints exactly what `/usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG`
  prints (libxkbcommon 1.13.2) for keymaps serialized by `/usr/lib/xkbcommon/xkbcli-compile-keymap`; frozen counter
  quality/counters/c1-r49-keysym.py (PRED-C1-r49) with fixtures quality/counters/c1-r49-fixtures.json (633). Its freeze was NEVER attacked
  (round-49 w2 never ran). Attacking it now is post-landing: a finding becomes a round-50 erratum or fix, never a rewrite of round-49 bytes.
- Round 49's C2 stopped honestly: the bind-key-match entry (candidate %(W49)s/candidate/hyprland-bind-key-match-r49.md, rows
  %(W49)s/candidate/rows.md S352-S363, pins %(W49)s/fetch/, live receipt %(W49)s/receipts/binds-live-r49.txt) failed its frozen counter
  quality/counters/c2-r49-bind-entry.py (clauses b/c/d/e/j: row-pin binding and quote attachment; %(W49)s/registration.md:24-31). Round 50
  C1 lands it as corpus/knowledge/hyprland-bind-key-match-r50.md under a round-50 port of that counter (PRED-C1-r50: base %(B)s, lesson
  corpus/lessons/round-50.md, pins %(W)s/fetch/, receipts %(W)s/receipts/), rows re-opened THIS round (access date 2026-10-27).
- Round 50 C2: the session-material gate v3 (draft %(W49)s/w1/ExecSessionShapes/check-session-material.py, 94/94 selftest) replaces the
  installed v2 %(L)s/quality/check-session-material.py (sha256 82c9053a...); counter PRED-C2-r50 = detection of the covered shapes in
  nonce-generated fixture repos + no false positive on green counter-shapes + selftest, at the revision.
- Routed non-claim items: D2 final state of 7 round-49 w1 seats that never reported before that report; D3 the unreceipted "57,865 pairs";
  D4 do-nothing control on the FROZEN round-49 C1 counter (the round-49 control ran on a draft); D6 QUALITY criteria owed for M49-1 and M49-3;
  D7 host guard (draft %(W49)s/w1/ExecMutantSandbox/hostguard.py) installed with a both-ways receipt; D8 lesson gate-count drift.
# Write scope and safety
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it) plus your Report file. NEVER edit a tracked file, never create
  files elsewhere in the lane, the fleet repo (/home/vgpnk/Projects/shokunin outside the lane), sibling lanes, templates/, scripts/,
  MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, or the shokuknow checkout (READ-ONLY; never run a campaign tool there). Never run
  mutating git/jj in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark/new). Read-only git is fine. The L1 is the
  only integrator; drafts of files meant for tracked paths go in your seat dir under the same basename.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>. Your tools start at the fleet root: absolute paths only.
  Write your Report file FIRST (a short status), then refine it; a seat that dies without a report is a dead seat. Every deliverable your
  report names must exist when you finish (round-49 M49-3: two seats reported files that did not exist) - `test -f` each before yielding.
- SCRATCH (operator directive 2026-10-25): every clone, venv, build, fixture tree and work dir lives under %(S)s/<YourSeatName>/ (mkdir -p;
  pass it explicitly as TMPDIR/--work/dir=, never rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB; start
  every writer shell with `ulimit -f 65536` (64 MiB per file; `git clone -q --shared %(L)s "$D"` fits); bound every loop; never `yes`, never an
  unbounded redirect, never write into a FIFO or device; copy receipts into your seat dir first, then delete your scratch dir before you finish
  (`trap 'rm -rf -- "$S"' EXIT`). A /tmp or scratch path is never citable evidence. Committed code must honour TMPDIR / --work and REFUSE a
  work dir under /tmp, /var/tmp or /dev/shm, never hardcode /tmp.
- HOST GUARD (round-48 M48-10): NEVER write the operator's real ~/.cache, ~/.config, ~/.local or any other home state. Every probe, mutant,
  counter or judge run that could write home state runs with HOME, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME and XDG_STATE_HOME set to
  dirs under your scratch (preferably inside bwrap with the real home not bound). A mutant that writes must target a path inside the sandbox.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input
  injection, never launch a terminal or any GUI program. xkbcli: ONLY `compile-keymap`, `how-to-type`, `list` (clean env). Allowed compositor
  reads: `hyprctl version`, `hyprctl binds -j`, `hyprctl getoption <opt> -j`, `hyprctl devices -j`; NEVER `dispatch`, `keyword`, `reload`,
  `setprop`, `switchxkblayout`, `--batch`, `output`, `plugin`, `kill`. Host config trees and binaries are READ-ONLY. Session material stays
  shape-only: never commit raw binds JSON, window titles, monitor serials, input-device names, process tables, home listings, the account
  name or absolute home paths in grep-style `path:LINE:` output; write `~` for the home directory and lane-relative paths in receipts.
- Git fixtures (run-6 incident): any fixture repo is `D=$(mktemp -d -p %(S)s/<YourSeatName>)` then `git -C "$D" init -q` (or
  `git clone -q --shared %(L)s "$D"`), every later git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D`
  before the first commit; never `git commit` with a throwaway identity anywhere else.
- Tooling authorization (operator, 2026-10-19): you and every seat may install/upgrade tools that help the task - read
  /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman
  guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide until the operator resolves the host-recovery L0
  question - use uv tool / uv pip into a scratch venv / npx / an official binary in ~/.local/bin; never -Sy, -Syu, -U, -R, a downgrade, or a
  restart of a host service.
- You are a leaf: no subagent dispatch, no background jobs (an executor MAY spawn one read-only labrat probe).
- Every finding names what it attacks or supports (a path:line, a command and its output, or a hash). Never fabricate: an unrun check has not
  passed. Quotes lifted from a source are <= 25 words, located (file:line), verified by a script that greps your receipt; locators are
  computed (grep -n), never typed. Pins you fetch go to your seat dir with their sha256 and the URL (tag or commit URLs, never a branch).
- Keep your final answer short: verdict, deliverable paths, the key command outputs. The L1 reads your Report file and seat dir.
"""


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(W49)s", W49), ("%(B)s", BASE), ("%(C)s", CLAIMS), ("%(B49)s", B49),
                 ("%(P)s", PKG), ("%(S)s", SCR)):
        t = t.replace(k, v)
    return t


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({"name": name, "role": role,
                  "prompt": sub(GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() + "\n")})


# ------------------------------------------------- carried: the 38 round-49 w2 items, retargeted
CARRY = ("Carried item: round-49 w2 item `%s` (%%(W49)s/w2-items.json; never dispatched in round 49, routed by the round-49 closure D1). "
         "Round-50 retarget: %s\n\nOriginal item text (round-49 wording; where it says 'candidate tool' or 'at the freeze', apply the "
         "retarget above):\n")
RETARGET = {
    "RevC1Counter": "the tool is LANDED: run the frozen counter at the lane tip %(C)s (tools/mado-keysym.py present there; no fixture commit "
                    "needed) on a --shared scratch clone, twice with different nonces.",
    "RevC1Tool": "attack the LANDED tools/mado-keysym.py at %(C)s (byte-equal to the round-49 candidate).",
    "CritC1Random": "attack the LANDED tool at %(C)s. Also routed D3: commit to your seat dir a receipt with the exact command, the seeds, the "
                    "pair count, the mismatch count and the judge/tool sha256 - it is the round's committed random-pair figure.",
    "CritC1Exotic": "attack the LANDED tool at %(C)s.",
    "CritC1Args": "attack the LANDED tool at %(C)s (ExecKeysymNames: %(W49)s/w1/ExecKeysymNames.md).",
    "CritC1Fixtures": "the fixtures are frozen and landed (quality/counters/c1-r49-fixtures.json at %(C)s).",
    "MutC1Tool": "mutate the LANDED tool; score each mutant with the frozen counter on a --shared scratch clone where a fixture commit "
                 "replaces tools/mado-keysym.py by the mutant.",
    "MutC1Counter": "the round-49 controls are under %(W49)s/w1/ExecControlsC1/ (controls/, cases.json, score-controls.py).",
    "ExecC1Cheats": "score the cheats with the frozen counter at %(C)s on a scratch clone (fixture commit replacing the tool).",
    "ExecC1Overfit": "score with the frozen counter at %(C)s on a scratch clone (fixture commit replacing the tool).",
    "CritC1Judge": "the frozen counter at %(C)s.",
    "RevC1Usage": "read the LANDED tool's docstring (tools/mado-keysym.py) and the round-49 SKILL draft %(W49)s/w1/ScrSkill/skill-section.md.",
    "RevC2Entry": "the candidate is still %(W49)s/candidate/hyprland-bind-key-match-r49.md with pins %(W49)s/fetch/; it becomes the round-50 "
                  "entry hyprland-bind-key-match-r50.md, so every unsupported or partly-supported sentence you list is removed or fixed "
                  "before the freeze. Write your verdict table to your seat dir as verdicts.md (sentence, locator, verdict, line text).",
    "CritC2FalseClaim": "same candidate (it becomes the round-50 entry).",
    "CritC2Scope": "compare against BOTH the round-49 base %(B49)s and the round-50 base %(B)s (round 49 added corpus/lessons/round-49.md, which "
                   "quotes some C2 terms: name every C2 term that already occurs under corpus/ at %(B)s - the round-50 counter's novelty "
                   "clause must not use those).",
    "RevC2Counter": "the round-49 counter is the template of the round-50 counter PRED-C1-r50 (re-pointed base/lesson/fetch/receipts): every "
                    "clause flaw you show is fixed in the port before the freeze.",
    "MutC2Counter": "the round-49 C2 controls are under %(W49)s/w1/ExecControlsC2/ (controls/, build-controls.py, drive.py).",
    "MutC2Entry": "same candidate; your admitted semantic mutations become the round-50 lesson's declared residual and w2 reading targets.",
    "CritC2Pins": "re-fetch every URL THIS round (2026-10-27) and compare byte-for-byte with the round-49 pins; the rows will be appended this "
                  "round, so also check each candidate row against the census schema (11 cells, no `|` in a cell, recheck ISO/NNd/on-*).",
    "CritC2Live": "re-capture now; the round-50 receipt will be taken this round, so report which round-49 receipt numbers moved.",
    "ScoutC2Wiki": "same pins.",
    "RevGateV3": "nothing landed in round 49: attack the round-49 DRAFT %(W49)s/w1/ExecSessionShapes/check-session-material.py (the base of the "
                 "round-50 C2 install) at the round-50 base %(B)s; a round-50 install candidate is being built in parallel by seat "
                 "ExecGateV3 (%(W)s/w1/ExecGateV3/) - attack whichever exists when you run, name which.",
    "MutGateV3": "mutate the round-49 DRAFT %(W49)s/w1/ExecSessionShapes/check-session-material.py (the base of the round-50 C2 install).",
    "CritSidecars": "the L1 COMMITTED all 47 sidecars in round 49 (freeze dd2e827e; rationale %(W49)s/w1/CritSidecars.md): attack that "
                    "disposition at %(C)s - does any sidecar waive real material (open each target, classify by shape only)? does the gate "
                    "(v2 installed, and the v3 draft) agree?",
    "RevHostGuard": "nothing landed in round 49: attack the DRAFT %(W49)s/w1/ExecMutantSandbox/hostguard.py (+ demo.sh); grep the round-49 "
                    "frozen counters (quality/counters/c1-r49-keysym.py, c2-r49-bind-entry.py) for HOME/XDG handling.",
    "SentHostState": "compare %(W49)s/receipts/operator-state-before.txt, %(W49)s/receipts/operator-state-after.txt and "
                     "%(W)s/receipts/operator-state-before.txt (round 50 start) with a fresh read-only stat+sha256.",
    "SentScratch": "the round-49 frozen counters (quality/counters/c1-r49-keysym.py, c2-r49-bind-entry.py) and tools/mado-keysym.py at %(C)s.",
    "SentPrivacy": "scan what round 49 COMMITTED under .ufo/waves/round-49/ at %(C)s (it is public now: report classes and paths, never values, "
                   "so the round-50 lesson can name them) and anything already under %(W)s/; run the installed v2 gate and the v3 draft "
                   "with --scope all on a scratch clone at %(C)s.",
    "CritCorrections": "the N1-N5 corrections were committed in round 49 at corpus/lessons/round-49.md:49-64 (section 'Round-48 closure "
                       "items'), not in a candidate/corrections.md: attack those lines at %(C)s.",
    "RevN4Matrix": "compare the round-48 paths between %(B49)s and the round-49 tip %(B)s.",
    "CritQuality": "no criterion landed in round 49: attack the round-49 drafts %(W49)s/w1/ScrQuality/criteria.md and its check*.py "
                   "instruments, and the round-50 owed criteria for M49-1/M49-3 (corpus/lessons/round-49.md:31-43; drafted in parallel "
                   "by seat ScrQualityR50 at %(W)s/w1/ScrQualityR50/ - attack whichever exists when you run).",
    "ConnCrossClaim": "the round-50 claims are C1 = the bind-key-match entry and C2 = the session-material gate v3 (%(W)s/claims.md). Build a "
                      "gate-only tree (the v3 draft at quality/check-session-material.py) and an entry-only tree (the round-49 candidate "
                      "entry, rows, receipts); run the round-49 C2 counter on both and the v3 draft's selftest on both; list every file "
                      "either round-50 counter would read and any coupling.",
    "ConnLedger": "the ledger draft is %(W49)s/w1/ScrToolLedger/ (ledger.md, check-ledger.py).",
    "ScoutCensus": "the round-50 start receipt is %(W)s/receipts/census-before.txt; candidate rows %(W49)s/candidate/rows.md.",
    "ExecDoNothing": "routed D4: score the do-nothing and cheap controls with the FROZEN round-49 counters as committed at %(C)s "
                     "(quality/counters/c1-r49-keysym.py, c2-r49-bind-entry.py), never a draft; write each control's final line, exit "
                     "code and the exact command to %(W)s/w1/ExecDoNothing/receipts/.",
    "CritGateLesson": "the round-49 lesson as COMMITTED: corpus/lessons/round-49.md:6-27 and %(W49)s/w1/ScrRows/gate.md. Routed D8: compute "
                      "the admit and reject counts of each with a command and state the correction line.",
    "ExecSkillRows": "the candidate SKILL section is %(W49)s/w1/ScrSkill/skill-section.md (not landed).",
    "RevRegistration": "%(W49)s/registration.md vs the frozen counters at %(C)s; include D3 (registration.md:22 '57,865 random pairs' has no "
                       "committed receipt: find any receipt in the round-49 tree that carries that number, `git grep -n 57865` / `57,865`).",
}
with open(os.path.join(W49, "w2-items.json")) as fh:
    carried = json.load(fh)
assert len(carried) == 38
for it in carried:
    note = RETARGET[it["name"]]
    seat(it["name"], it["role"], it["target"], (CARRY % (it["name"], note)) + it["task"])

# ------------------------------------------------- round-50 build items
seat("ExecFetchR50", "executor",
     "C1 rows: re-fetch every source the round-49 candidate rows pin, this round, and prove byte stability.",
     """For every row in %(W49)s/candidate/rows.md (S352-S363) and every pin in %(W49)s/fetch/: fetch the row's URL now (commit/tag URLs only;
GitHub raw), save under %(W)s/w1/ExecFetchR50/fetch/ with the SAME basename as the round-49 pin, and write fetch-manifest.tsv
(basename, url, http status, bytes, lines, sha256, round-49 pin sha256, equal yes/no, access time ISO). The host receipt pins (binds-live-*.txt)
are not fetched: list them as own-work. Also fetch at the same commits any extra file the entry may need (e.g. the libxkbcommon tag's
tools/how-to-type.c) only if a round-49 pin exists for it. Report the equal/differ count; a differing pin is a finding with its diff stat.""")
seat("ExecLiveR50", "executor",
     "C1 live receipt: this round's read-only capture of the host bind surface, in the round-49 receipt's shape.",
     """Read %(W49)s/receipts/binds-live-r49.txt and %(W49)s/receipts/binds-shape-r49.txt (shape, fields, digest line) and the round-49 counter's
clause f/r (quality/counters/c2-r49-bind-entry.py: what the receipt must state and how replay re-derives it). With HOME/XDG_* in scratch and
/usr/bin/hyprctl: capture `hyprctl version`, `hyprctl binds -j` (sha256 of the raw JSON, bind total, the four key-form counts by the counter's
rule, the modmask histogram - never commit the JSON or any bind arg/description), `hyprctl getoption input:resolve_binds_by_sym -j`. Write
%(W)s/w1/ExecLiveR50/binds-live-r50.txt in the same shape (names `hyprctl binds -j`, `Hyprland 0.56.2` with commit
efb50993780079460b0cbed1363e2166a2de1d9f, `sha256` line, total, form counts summing to it, resolve value) and a generator script
make-receipt.py that produces it byte-identically from a fresh capture (run it twice; digests equal unless the binds changed). Report what moved
vs round 49.""")
seat("ExecCounterC1R50", "executor",
     "C1 counter draft: port quality/counters/c2-r49-bind-entry.py to round 50 as c1-r50-bind-entry.py (PRED-C1-r50), at your seat dir.",
     """Copy the round-49 counter to %(W)s/w1/ExecCounterC1R50/c1-r50-bind-entry.py and re-point it: PRED name PRED-C1-r50; BASE %(B)s;
ENTRY corpus/knowledge/hyprland-bind-key-match-r50.md; LESSON corpus/lessons/round-50.md; FETCH .ufo/waves/round-50/fetch/; RECEIPTS
.ufo/waves/round-50/receipts/; OPENED 2026-10-27; head ids >= S352 (registry still tops at S351 at %(B)s - verify with the census row
pattern); the held row S319 and its round-46 pin unchanged. Clause i's GROUND terms must be absent under corpus/ at the NEW base: round 49's
corpus/lessons/round-49.md now quotes `m_xkbSymState` and `m_xkbTranslationState` - `git grep` each GROUND term at %(B)s and replace any that
match by source-derived terms that do not (state which and why). Clause f/r receipt name pattern: binds-live-r50.txt. Keep every other clause
byte-identical in meaning; write port-diff.txt (unified diff vs the round-49 counter) and a table of each changed line with its reason. Run it at
%(B)s (entry absent: must print TARGET_MISSED, clause a) and on a scratch clone where the round-49 candidate artifacts are committed at the
round-50 paths (fixture identity, toplevel verified) - report every failing clause and the exact failure text, so the scribe seats know what
the entry/rows must satisfy. TMPDIR under your scratch.""")
seat("ExecControlsC1R50", "executor",
     "C1 control bundles for the section-9 do-nothing check of the round-50 counter (PRED-C1-r50).",
     """Write %(W)s/w1/ExecControlsC1R50/build-controls.py: given --counter PATH --repo LANE --rev REV --work DIR, it builds scratch clones
(fixture identity, toplevel verified) holding each control at the round-50 paths and runs the counter on each, printing one line per control
(name, final line, exit). Controls: BASE (nothing added); STUB (entry with a valid provenance head and one sentence); HELD (the held
corpus/knowledge/keybind-rule-semantics.md section 2.3 pasted under a round-50 head with real row ids); OLDPATHS (the round-49 candidate
entry/rows/receipt unchanged, round-49 paths); NOLIVE (a complete candidate minus the live receipt); NOROWS (entry without registry rows);
FORGEDQUOTE (one step quote altered by one word); BRANCHURL (one row URL on `main`). Run it now against the round-49 counter
(quality/counters/c2-r49-bind-entry.py) and, if it exists when you run, ExecCounterC1R50's draft; every control must read TARGET_MISSED -
report the clause that stopped each. The L1 re-runs it on the frozen counter.""")
seat("ScrEntryR50", "scribe",
     "C1 data: the round-50 candidate entry hyprland-bind-key-match-r50.md (at your seat dir), built from the round-49 candidate.",
     """Start from %(W49)s/candidate/hyprland-bind-key-match-r49.md. Write %(W)s/w1/ScrEntryR50/hyprland-bind-key-match-r50.md: round-50 paths
(.ufo/waves/round-50/fetch/<same basenames> for pins, .ufo/waves/round-50/receipts/binds-live-r50.txt for the live receipt; 'Round: 50'),
`verified-at: 2026-10-27`, provenance head within the first 20 lines (source: S### lines for every new row >= S352 it cites, one recheck:).
Fix what failed the round-49 counter (%(W49)s/registration.md:30-31: clauses b/c/d/e/j - row-pin binding and quote attachment): EVERY numbered
step carries at least one backticked 2-25-word quote immediately followed by a locator `, <pin>:<a>[-<b>]` that resolves to a pin a row cites,
and the quote occurs verbatim inside that range (verify with a script you write: verify-quotes.py over %(W49)s/fetch/ - the round-50 pins are
expected byte-equal; ExecFetchR50 checks). Cover the seven clause-j topics at their implementing lines (resolve_binds_by_sym ternary;
case-insensitive second lookup; exact modmask comparison with the `i` escape; `code:` form; zero-modifier sym-state update; depressed-only bind
mask; per-device option read). Remove the M49-1 claim (corpus/lessons/round-49.md:31-35: Shift binds are NOT dead). Keep a `## Limits` section
(>= 3 bullets). Write the host-section numbers as placeholders `<<total>>`, `<<named>>`, `<<code>>`, `<<mouse>>`, `<<switch>>`, `<<sha256>>`
that the L1 fills from binds-live-r50.txt. Output: the entry, verify-quotes.py, quotes-verified.txt.""")
seat("ScrRowsR50", "scribe",
     "C1 registry rows S352-S363 in fleet/census schema, plus the round-50 lesson Gate lines (at your seat dir).",
     """From %(W49)s/candidate/rows.md and %(W49)s/w1/ScrRows/gate.md write %(W)s/w1/ScrRowsR50/rows.md: one row per cited source, 11 cells, no
literal or escaped `|` in any cell, kind/tier/status enums per /home/vgpnk/Projects/shokunin/CORPUS.md section SOURCES.md, opened 2026-10-27,
recheck an ISO date, NNd or on-release, status `mined`, anchor naming the pin `.ufo/waves/round-50/fetch/<basename>` and `sha256:<64hex>`,
used-by exactly `corpus/knowledge/hyprland-bind-key-match-r50.md` (rows that serve only tools/mado-keysym.py - S357/S358 - get used-by
`corpus/lessons/round-50.md` and are marked so; say which rows those are). Validate: build a scratch mirror of %(L)s/corpus/ with the rows
appended to the Registry table and run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`
(exit 0 required; paste output; E03/E04 means refuse/supersede). Write gate.md: one `**S### admit**` line per row with URL, access date
2026-10-27 and a <= 25-word quote with its pin:line, verified by a script against the pins (round-49 pins are expected byte-equal to round-50
re-fetches), and the REJECT lines carried from round 49 (wiki rendered pages, ArchWiki, re-registering S318/S319) with reason and flip; end with
the computed counts (`grep -c` commands shown).""")
seat("ExecGateV3", "executor",
     "C2 data: the install-ready session-material gate v3 (at your seat dir), from the round-49 draft.",
     """Start from %(W49)s/w1/ExecSessionShapes/check-session-material.py (v3 draft; report %(W49)s/w1/ExecSessionShapes.md) and the installed v2
%(L)s/quality/check-session-material.py. Write %(W)s/w1/ExecGateV3/check-session-material.py: v3 rules R7-R9, default scope all, every v2 selftest
case name kept, `--selftest` last line in the v2 format with N/N; fix any defect the draft's report or receipts name. Never print a found value:
counts and masked shapes only; the account is resolved at run time and never printed. Run: --selftest; the gate at %(B)s with --scope all and
--scope ufo on a --shared scratch clone (findings counts by rule; write masked summaries only); the both-ways mutation (remove each of R7/R8/R9:
its red cases fail, green stay green; mutate.py from the draft); and the e2e fixture (v2 blind, v3 red). Write receipts/ with commands and exits,
and SHA256SUMS. Also state the exact CLI the C2 counter should call (flags, exit codes, output lines).""")
seat("ExecCounterC2R50", "executor",
     "C2 counter draft quality/counters/c2-r50-session-gate.py (PRED-C2-r50) with nonce-generated shape fixtures (at your seat dir).",
     """Write %(W)s/w1/ExecCounterC2R50/c2-r50-session-gate.py: --repo --rev --work --nonce; refuses --work/TMPDIR under /tmp, /var/tmp, /dev/shm
(exit 2); reads quality/check-session-material.py from REV with `git show` (never the working tree); runs it under python3 -I with HOME and
XDG_* in --work. Clauses: s - `--selftest` passes (N/N, N >= 94) and every v2 selftest case name (from the v2 bytes at %(B)s, listed in your
seat dir with sha256) is present; r - RED: generate from the nonce K >= 40 fixture git repos (fixture identity, toplevel verified, under --work)
each holding one instance of one covered shape (R7 forms: grep-style `path:LINE:` home prefix, a listing header `path:`, a quoted path on a tool
diagnostic line, a home path in an `ls -l` row; R8 owner/group column equal to the account; R9 >= 2 column-0 exec-cache fields; material outside
`.ufo/`), with random synthetic account names and paths, run the gate with its default scope and an explicit `--account <synthetic>` if the CLI
needs it; every red repo must yield findings >= 1 and exit non-zero; g - GREEN: K >= 40 counter-shape repos (`~/` and `$HOME/` forms, a home path
inside a prose sentence, numeric ids in `ls -ln`, one cache field only, indented usage text) must yield 0 findings, exit 0; d - default scope sees
a file outside `.ufo/`. Final line `PRED-C2-r50: selftest=.. red=A/K green=B/K scope=.. verdict=TARGET_MET|TARGET_MISSED rev=<hash>` exit 0/1,
setup error 2. Shapes come from %(W49)s/w1/ExecSessionShapes.md section 2 and the draft's selftest; never use the real account name. Run it at
%(B)s (v2 installed: must MISS) and on a scratch clone with the v3 draft installed (should MEET); plus controls: a flag-every-line stub gate
and a v2-with-scope-all gate (both must MISS). Receipts in your seat dir.""")
seat("ExecHostGuardR50", "executor",
     "D7 (M48-10): the install-ready host-state guard (at your seat dir) with its both-ways demonstration.",
     """Start from %(W49)s/w1/ExecMutantSandbox/hostguard.py and demo.sh (report %(W49)s/w1/ExecMutantSandbox.md). Write
%(W)s/w1/ExecHostGuardR50/mado-hostguard.py (target path tools/mado-hostguard.py) with a hermetic --selftest (last line
`MADO_HOSTGUARD_SELFTEST: N/N passed`), refusing work dirs under /tmp, /var/tmp, /dev/shm, and demo.sh that shows on a FAKE operator home under
your scratch: an unsandboxed mutant writing <fake>/.cache/xdg-terminal-exec is caught (exit 3, fields named), the same mutant under `run
--sandbox bwrap` is contained (exit 0, digest unchanged), a no-op command exits 0. Never point `run` at the real home; `digest` (read-only) may
read the four operator paths named in %(W)s/receipts/operator-state-before.txt and must reproduce those sha256 values. Receipts + SHA256SUMS.""")
seat("ExecWaveDone", "executor",
     "Mistake fix for round-49 D2 (report filed before WAVE-DONE): quality/check-wave-done.py (at your seat dir), shown able to fail.",
     """Write %(W)s/w1/ExecWaveDone/check-wave-done.py: --repo --rev --round N. Reads only committed bytes at REV: for every
`.ufo/waves/round-N/<wave>.ready` it requires `.ufo/waves/round-N/<wave>-results.json` at REV, parses it, and requires every seat to carry a
terminal status (list the statuses the orchestrator writes - read an existing *-results.json under %(L)s/.ufo/waves/ if any exists at any revision,
`git log --all --name-only -- '*-results.json'`, else read the dispatcher contract in the round prompt
/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-50.md section 6 run-7 block); prints one line per wave and a final
`MADO_WAVE_DONE: round=N waves=W settled=S verdict=OK|MISSING`, exit 0/1, usage 2. Hermetic --selftest. Show it able to fail: at %(B)s with
--round 49 it must print MISSING (w1.ready committed, no w1-results.json); on a fixture repo with a results file it prints OK. Receipts.""")
seat("ScrQualityR50", "scribe",
     "D6: QUALITY.md criteria owed for M49-1 and M49-3, plus one for the D2 mistake (at your seat dir), each citing its lesson line.",
     """Read %(L)s/corpus/QUALITY.md (criteria 1-99; the format of 96-99 with their check lines) and corpus/lessons/round-49.md:31-47. Draft
%(W)s/w1/ScrQualityR50/criteria.md with criteria 100-102 in the same format: 100 (M49-1) a host-consequence model or claim about which state a
compositor reads cites the source line that sets that state; 101 (M49-3) every deliverable a seat or report names exists at the cited revision
(`test -f` / `git cat-file -e REV:path`); 102 (round-49 D2) a round report is committed only after every dispatched wave's results file exists
with every seat settled (instrument: quality/check-wave-done.py, drafted by ExecWaveDone). Each criterion cites its lesson line (round-49 lines
for 100-101; `corpus/lessons/round-50.md` mistake M50-1 for 102) and has an instrument or check command shown failing on a red input and passing
on a green one (write tiny instruments for 100/101 in your seat dir if none exists; reuse %(W49)s/w1/ScrQuality/ drafts where they fit, name
which). Paste each instrument's red and green output.""")
seat("ScrCorrectionsR50", "scribe",
     "Routed D2, D3, D8: correction lines with their commands (at your seat dir).",
     """Write %(W)s/w1/ScrCorrectionsR50/corrections.md. D2: for each of the 7 round-49 w1 seats the report was filed without (ExecControlsC1,
ExecSessionTriage, ScoutHyprBinds, CritPremiseC1, CritPremiseC2, CritRoutedItems, SentPrivacy) state the final state - report landed (commit
via `git log --format='%h %ci' -- <path>` on %(W49)s/w1/<Seat>.md and its dir), partial (dir without report), or absent - and whether any of
their bytes landed after the round-49 report commit (fleet `git -C /home/vgpnk/Projects/shokunin log --format='%h %ci' -- .ufo/reports/round-49/mado.md`).
D3: the '57,865 random pairs over 400 keymaps' sentence (%(W49)s/registration.md:22 and the round-49 report) - search for a receipt
(`git -C %(L)s grep -n -e 57865 -e 57,865`), and write the correction naming the committed figure (%(W49)s/w1/ExecRefKeysymB.md:51, 24898
comparisons). D8: corpus/lessons/round-49.md:26 says '2 drafted admits and 4 rejects' - count the admits/rejects in that lesson's Gate section
and in %(W49)s/w1/ScrRows/gate.md with grep commands and write the correction line with the commands and outputs. Every line append-only
(it lands in the round-50 lesson, never edits round-49 files).""")
seat("ScoutAssimR50", "scout",
     "Assimilation and considerthese for round 50: the merge/mado/ package, the id guard, the quarantine slice, the latest reflection.",
     """Read %(P)s/MERGE-REPORT.md (read-only; run no campaign tool) and say whether any staged theme matches C1 (Hyprland binds / keysyms /
keymaps) or C2 (session-material privacy) and PROVINCE.md. Run the round prompt's section-6 item-10 id-collision commands with the output
directory set to %(W)s/w1/ScoutAssimR50/assimilation/ (reg-ids, staged-ids, collisions; also prove the guard on a scratch registry with an
indented `  | S002 |` row) and the quarantine-slice awk (register
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md) into the same dir; paste counts. Then read
%(L)s/considerthese/2026-10-26.md (latest; `ls`) section 'Self-improvement suggestions' and corpus/lessons/round-4[5-9].md for which proposals
were already landed or refused (proposal 6 landed as QUALITY 99 in round 48; proposal 2 refused in round 47); recommend ONE still-unimplemented
proposal this round can ground (proposal 1, a privacy check on new receipts, overlaps C2: say whether C2 implements it and what is left).""")
seat("ConnSiblingsR50", "connector",
     "Sibling overlap for round 50's ground: bind/keysym/keymap knowledge and evidence-privacy gates across sibling lanes (read-only).",
     """Read-only: for each sibling lane dir /home/vgpnk/Projects/shokunin/*-shokunin (not mado) grep PROVINCE.md, corpus/README.md and
corpus/knowledge/ for xkb, keysym, keymap, resolve_binds_by_sym, `bind =`, hyprctl binds, and for session-material / privacy gates over receipts
(home paths, account names). Report contested scope (a sibling that owns bind or keymap ground), reusable patterns (a sibling's privacy gate with
rules mado's v3 lacks, with file:line), and anything round 50 must cite instead of absorb.""")
seat("ScoutHeldR50", "scout",
     "Held ground the C1 entry must cite, not restate; README coverage-map and SKILL.md placement.",
     """In %(L)s at %(B)s: corpus/knowledge/keybind-rule-semantics.md (section 2.3), xkb-keymap-compile-r48.md, hyprland-input-devices-r46.md
(:71), tools/mado-binds.py and tools/mado-keysym.py docstrings, SKILL.md bind/keymap sections, corpus/README.md coverage map and `## Frontier`.
List every held sentence the round-49 candidate entry (%(W49)s/candidate/hyprland-bind-key-match-r49.md) restates (line pairs), the exact
README index row and frontier row the round-50 entry should get (match the column format of existing rows, cite the rows' S-ids), and the
SKILL.md line or table row that should point at the entry (one, with its proposed text). Output %(W)s/w1/ScoutHeldR50/placement.md.""")
seat("RevAxisR50", "reviewer",
     "Calibration sweep at the round-50 base: SCORECARD/SHONEN/LOG self-statements vs observed repo state.",
     """At %(B)s: re-derive every number SCORECARD.md's round-49 section (from `## Round 49`) and the round-49 LOG entry state (counts, hashes,
receipt verdicts, capability row, 'Axis table not re-derived' claim, planned items), each with its command, and SHONEN.md's four boxes vs their
evidence pointers. Run `TMPDIR=<scratch> python3 -I quality/check-axis-scores.py --rev %(B)s --repo .` from the lane root. Report each
self-statement as match/mismatch with the command and output; a mismatch is a round-50 erratum candidate.""")

n = len(items)
assert 32 <= n <= 64, n
assert len({i["name"] for i in items}) == n
print(n, dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-50/w1", "items": items}
with open(os.path.join(W, "w1-spec.json"), "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
