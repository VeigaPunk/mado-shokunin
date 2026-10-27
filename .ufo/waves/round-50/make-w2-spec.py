#!/usr/bin/env python3
"""Generates .ufo/waves/round-50/w2-spec.json (round 50, wave w2 = FALSIFY, policy v1).

w2 attacks the round-50 freeze at %(TIP)s: both frozen counters, both claims, the v3 gate, the new
instruments, the lesson/registry/README integration, the host guard, the freeze controls and the
assimilation quarantine. Every item attacks a named landed thing. Read-only on the lane; seats write
their seat dir + Report file only.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-50"
BASE = "8ae47b957034ae21012bbf09173cca2c48be345e"
CLAIMS = "13631f24050f22db92bf5bd33e0f4d014192992e"
DATA = "906178b607f2071af7c2efec5aad976a8bfa5757"
TIP = "b4a79843cc2545bbe800db9322e58f6e00436629"   # tip to attack (freeze + receipts)
W49 = LANE + "/.ufo/waves/round-49"
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
mado round 50 (hyaku run 10, 2026-10-27, attempt 2), wave w2 = FALSIFY (policy v1). Lane repo: %(L)s (desktop/compositor craft:
Hyprland/waybar/walker/terminal/keyboard config plane of this host; axes coverage + operability). Read %(W)s/claims.md and
%(W)s/registration.md FIRST: the freeze names every counter, receipt and artifact to attack. The round state you attack:
- Freeze commits: claims %(C)s (attempt 1); data %(D)s (entry corpus/knowledge/hyprland-bind-key-match-r50.md, rows S352-S363 in
  corpus/SOURCES.md `## Registry`, README row + Frontier bullet, SKILL.md pointer, lesson corpus/lessons/round-50.md, QUALITY
  criteria 100-102, gate v3 installed at quality/check-session-material.py sha256 ffdc9d62..., quality/check-wave-done.py
  10f4359a..., quality/check-state-cite.py, quality/check-deliverables.py, tools/mado-hostguard.py fdaa5c2e...,
  receipts/binds-live-r50.txt, w1-results.json); freeze 470bfd77 (registration + counter receipts); results repair 8dbbf61a.
- Attack revision: %(TIP)s (landed tip). Counters score committed bytes at a --rev; run them on a `git clone -q --shared`
  of the lane inside your scratch, never in the lane tree.
- PRED-C1-r50: `TMPDIR=<your scratch> python3 -I %(L)s/quality/counters/c1-r50-bind-entry.py --repo <clone> --rev <rev>`.
  Data run: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET` at %(D)s
  (%(W)s/receipts/c1-at-data.txt). Controls c00/c13/c12 all MISSED (%(W)s/receipts/controls-c1.txt).
- PRED-C2-r50: `python3 -I %(L)s/quality/counters/c2-r50-session-gate.py --repo <clone> --rev <rev> --work <your scratch> --nonce <n>`.
  Data runs: nonces 50117 `red=42/42 green=44/44`, 778899 `red=44/44 green=41/41`, both `selftest=94/94 names=69/69 scope=seen
  verdict=TARGET_MET` (%(W)s/receipts/c2-at-data-*.txt). Controls c00/c12/c14 all MISSED (%(W)s/receipts/controls-c2.txt).
- w1 (54 seats) artifacts live under %(W)s/w1/ - seat reports, receipts, drafts. Four w1 seats were cut off by the run-9 wrap-up
  (CritC1Random, CritC1Exotic, MutC2Entry, CritQuality): their attacks are re-run here (lesson M50-4).
# Write scope and safety
- Write ONLY to your own seat directory %(W)s/w2/<YourSeatName>/ (create it) plus your Report file. NEVER edit a tracked file, never create
  files elsewhere in the lane, the fleet repo (/home/vgpnk/Projects/shokunin outside the lane), sibling lanes, templates/, scripts/,
  MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, or the shokuknow checkout (READ-ONLY; never run a campaign tool there). Never run
  mutating git/jj in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark/new). Read-only git is fine. The L1 is the
  only integrator. Do NOT score or grade claims for admission: your verdicts are attack evidence for the L1.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>. Your tools start at the fleet root: absolute paths only.
  Write your Report file FIRST (a short status), then refine it; a seat that dies without a report is a dead seat. Every deliverable your
  report names must exist when you finish (round-49 M49-3) - `test -f` each before yielding.
- SCRATCH: every clone, venv, build, fixture tree and work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it explicitly as
  TMPDIR/--work/dir=, never rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB; `ulimit -f 65536` on every
  writer shell; bound every loop; never `yes`, never an unbounded redirect, never a FIFO or device; copy receipts into your seat dir first,
  then delete your scratch dir before you finish. A /tmp or scratch path is never citable evidence.
- HOST GUARD (M48-10): NEVER write the operator's real ~/.cache, ~/.config, ~/.local or any home state. HOME, XDG_CACHE_HOME,
  XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME and TMPDIR all under your scratch for every run; a mutant that writes targets a path inside
  the sandbox. tools/mado-hostguard.py is installed if your probe is stateful.
- Host safety: pacman is PAUSED host-wide. No host-service or compositor mutation, no input injection, never launch a GUI program. xkbcli:
  ONLY `compile-keymap`, `how-to-type`, `list` (clean env). Allowed compositor reads: `hyprctl version`, `hyprctl binds -j`,
  `hyprctl getoption <opt> -j`, `hyprctl devices -j`; NEVER dispatch/keyword/reload/setprop/switchxkblayout/--batch/output/plugin/kill.
  Session material stays shape-only: never commit raw binds JSON, window titles, monitor serials, device names, process tables, home
  listings, the account name, or absolute home paths in grep-style output; write `~` for the home directory in receipts.
- Git fixtures: `D=$(mktemp -d -p %(S)s/<Seat>) && git -C "$D" init -q` or `git clone -q --shared %(L)s "$D"`; every git call names `-C "$D"`;
  `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the first commit; never commit with a throwaway identity elsewhere.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help - read /home/vgpnk/.omp/agent/RULES.md first
  (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions PAUSED
  host-wide - use uv tool / npx / an official binary in ~/.local/bin; never -Sy/-Syu/-U/-R/downgrade/service restarts.
- You are a leaf: no subagent dispatch, no background jobs (an executor MAY spawn one read-only labrat probe).
- Every finding names what it attacks or supports (path:line, command + output, or a hash). Never fabricate. Quotes from a source: <=25
  words, located (file:line), verified by a script. Locators computed (grep -n). Pins you fetch: seat dir, sha256, tag/commit URLs only.
- Keep your final answer short: verdict, deliverable paths, the key command outputs. The L1 reads your Report file and seat dir.
"""


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(W49)s", W49), ("%(B)s", BASE), ("%(C)s", CLAIMS),
                 ("%(D)s", DATA), ("%(TIP)s", TIP), ("%(S)s", SCR)):
        t = t.replace(k, v)
    return t


items = []


def seat(name, role, target, task):
    items.append({"name": name, "role": role,
                  "prompt": sub(GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() + "\n")})


# ------------------------------------------------- frozen-counter attacks (8)
seat("RevC1FrozenCounter", "reviewer",
     "Frozen counter quality/counters/c1-r50-bind-entry.py (PRED-C1-r50) and its data receipt.",
     "Re-run it twice on a --shared scratch clone at --rev %(D)s (data) and once at --rev %(B)s (base, entry absent must MISS), TMPDIR under your scratch. Then read the counter source and attack its clause code (a-r): locate each clause's predicate in code and verify the receipt's clause vector matches what the code computes. Attack clause d (the F1 numeric-band repair: a histogram token like `0:23` must not parse as a locator), clause f/r (RECEIPT_NAME pin `^binds-live-r50\\.txt$`), clause g's 150 generated cases (is sampling actually nonce-seeded inside one run, or fixed?), and the two-nonce gap: report whether the generated case sets differ run-to-run and what changes them.")

seat("RevC2FrozenCounter", "reviewer",
     "Frozen counter quality/counters/c2-r50-session-gate.py (PRED-C2-r50).",
     "Re-run on a --shared clone: --rev %(D)s at two fresh nonces of your own choosing, plus --rev %(B)s (v2 at base must MISS). Verify each receipt line shape `selftest=.. names=.. red=.. green=.. scope=.. verdict=..`. Then attack clauses s/r/g/d in code: names containment (69 v2 cases), red counting (expected rule appears AND findings>=1 AND exit!=0), green (exit 0 AND findings==0 AND files>=1), d (outside-.ufo seen, ufo-blind). Try the cheapest under-claim: a gate byte that passes s/g but emits no R7/R8/R9 findings (would `red` still count?) - build it only if code review says it is a real hole.")

seat("MutC1FrozenCounter", "mutation-tester",
     "Frozen PRED-C1-r50 counter bytes e162d671...",
     "Copy the frozen counter into your scratch, mutate it under a fixture clone, and prove each mutation changes the verdict or is honestly equivalent: (a) drop clause c entirely (rows never checked), (b) weaken clause d to presence-only, (c) remove the RECEIPT_NAME filter in clause f/r (any receipt counts), (d) accept clause i ground terms present at base, (e) restore the round-49 GROUND tuple (should MISS at data: the round-49 closure quotes those terms - this is the load-bearing check, expect TARGET_MISSED). Score each mutant by running it at --rev %(D)s on a --shared clone; pristine control first. Report per mutant: KILLED/SURVIVED + the verdict line.")

seat("MutC2FrozenCounter", "mutation-tester",
     "Frozen PRED-C2-r50 counter bytes 1d52a62c... and the rule-removal mutants.",
     "On a --shared clone: (a) remove R7 emission from the scored gate bytes (receipt from w1 says each rule-removal mutant drops exactly its family - verify under YOUR nonce), (b) a counter mutant: widen `names` containment to any 69-case set, (c) a counter mutant: drop the `files>=1` green condition (can a scan-nothing gate pass?), (d) a gate mutant that passes selftest but prints no findings at all under scan (green must still fail? or does g's files>=1 catch it). Pristine control first; score each mutant with the frozen counter at --rev %(D)s.")

seat("CritC1FrozenStub", "critic",
     "PRED-C1-r50 do-nothing controls + residual cheaper controls.",
     "Re-verify %(W)s/receipts/controls-c1.txt by rebuilding ONE control revision on a --shared clone (choose c13: paste %(W49)s/candidate/hyprland-bind-key-match-r49.md at corpus/knowledge/hyprland-bind-key-match-r50.md, commit, run the frozen counter at that rev) - its verdict must MISS. Then find a CHEAPER do-nothing the counter would wrongly admit: e.g. the real entry bytes with the recheck/ground paragraph stripped, an entry that cites the receipts but never quotes pins, or rows present but citing the wrong used-by. Run the strongest candidate; if it is admitted, that is a real defect - report the exact clause gap.")

seat("CritC2FrozenStub", "critic",
     "PRED-C2-r50 do-nothing controls + cheaper wrong gates.",
     "Re-verify %(W)s/receipts/controls-c2.txt: rebuild c14 (v3 rules, DEFAULT_SCOPE ufo) on a --shared clone atop %(D)s, run the frozen counter at that rev, expect MISS. Then try the cheapest wrong gate the counter might admit: (a) v3 with R9 removed but selftest edited to keep 94/94 (does clause r catch it?), (b) a gate whose scan emits the R7 finding string for one line only per red repo (parroting) - does clause r's rule-check stop it, or does it only count findings? Report the weakest admitted variant you can build; if none, say what stopped it.")

seat("CritC1EntryOverfit", "critic",
     "The landed entry corpus/knowledge/hyprland-bind-key-match-r50.md vs PRED-C1-r50.",
     "Write adversarial entry variants in a scratch clone atop %(D)s and score each with the frozen counter at its rev: (a) an entry that passes quote/topology checks but makes a WRONG claim (e.g. assert masks are compared before the group is chosen), (b) an entry that copies the real one but changes the values (binds=200), (c) the real entry with the live-receipt paragraph removed. Verdict each variant; the counter should MISS (a) and (b) - if it admits them, that is a defect; report exact clause lines. Also check whether clause e's quote attachment can be satisfied by a *correct quote in a wrong step* (misattribution).")

seat("CritFrozenNovelty", "critic",
     "C1's novelty/ground clause (i) and the held-fact enumeration in the entry's ground paragraph.",
     "At base %(B)s run `git grep -F <term> %(B)s -- corpus` for every term the landed entry or counter treats as new (xkb_state_key_get_layout, m_modifiersState, keysym_to_name, xkb_keysym_get_name, the matcher-chain topic names in clause j's TOPICS). Any term already present under corpus/ at base is a novelty error - list them. Then read the entry's ground paragraph (extended this round per w1/CritC2Scope) and find one held fact it still claims as new. Also check clause j's seven topics actually correspond to the mechanism, not to filler words.")

# ------------------------------------------------- entry/rows/pins/receipt attacks (6)
seat("RevEntrySentences", "reviewer",
     "Every numbered step of corpus/knowledge/hyprland-bind-key-match-r50.md at %(TIP)s vs the round-50 pins.",
     "Re-open each pin in %(W)s/fetch/ (committed at %(TIP)s). For each of steps 1-17: verify every quoted code span is byte-present at the cited locator (grep -n the quote inside the pin), and judge whether the step's claim follows from it. Pay attention to the steps w1/RevC2Entry corrected (12, 14, 16, 17) - the landed text was rewritten; check the correction did not introduce a new over-claim. Also verify the [INF] label on the version-commit inference and the held-fact enumeration in the ground paragraph (w1/CritC2Scope). Deliver a verdict table verdicts.md: step, locator, verdict, line text.")

seat("ScrQuoteVerify2", "scribe",
     "Round-50 lesson Gate admit lines and the entry's located quotes, against committed pins.",
     "Re-run the scribe's verify-quotes logic against the COMMITTED bytes: port %(W)s/w1/ScrRowsR50/verify-quotes.sh so it reads the pins from `git show %(TIP)s:.ufo/waves/round-50/fetch/<file>` (or a --shared clone worktree at %(TIP)s) and the admit lines from `git show %(TIP)s:corpus/lessons/round-50.md`. Every admit line must carry a URL, `opened 2026-10-27`, pin:line, a <=25-word quote present at that line. Then check each `source:` line in corpus/knowledge/hyprland-bind-key-match-r50.md resolves to a registry row whose anchor covers the cited region. Report pass/fail per line.")

seat("ScrRowsPlaced", "scribe",
     "Registry placement and schema of rows S352-S363 at %(TIP)s.",
     "Check `git show %(TIP)s:corpus/SOURCES.md`: (a) the 12 rows sit inside `## Registry` (before `## Paths`), (b) 11 cells per row, no literal `|` inside a cell, (c) every anchor's pin path exists at %(TIP)s and its sha256 matches the pin bytes, (d) recheck cells are ISO-date/NNd/on-* shaped, (e) used-by targets exist (S357/S358 -> corpus/lessons/round-50.md; the rest -> the entry). Then re-run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` and compare against %(W)s/receipts/census-after.txt: same warnings set, `mado ok`, exit 0. Report any E03/E04/E11/E12.")

seat("CritPinsLive", "critic",
     "Pin/receipt freshness and the receipt name pin (PRED-C1-r50 clause f/r).",
     "(a) Verify `git show %(TIP)s:.ufo/waves/round-50/fetch/SHA256SUMS` actually matches the fetch files (recompute each sha256 from the tree). (b) Check the 14 upstream pins byte-equal to %(W49)s/fetch/ pins via `git cat-file`/`git show` at %(TIP)s vs %(W49)s pins at %(B)s - any mismatch is a defect. (c) The receipt `.ufo/waves/round-50/receipts/binds-live-r50.txt` must byte-equal the fetch pin copy (cmp). (d) Clause r replays the capture: confirm the counter's live capture path cannot be satisfied by the pinned bytes alone (read the code), and that a tampered receipt (one digit changed) fails. (e) Verify `binds-live-r50.txt` carries no device names/titles/serials/home path.")

seat("RevCensusAfter", "reviewer",
     "Census conformance: SOURCES.md rows before -> after, and the validator's own verdict at the lane tip.",
     "Count registry rows at %(B)s and at %(TIP)s (`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\\| *S[0-9]{3,}'`): expect exactly +12 (288 -> 300). Re-run the validator (`sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`) and diff the warning set against %(W)s/receipts/census-before.txt: the 18 baseline W01/W04 warnings may shift (new rows may legitimately add W04 cross-scope duplicates of held URLs S303/S317-family) - name the delta precisely; any E-level line or exit != 0 is a defect.")

seat("RevLedgerR50", "reviewer",
     "The live-state tool ledger classification gap (w1/ConnLedger finding).",
     "Find the ledger artifact the w1 connector attacked (start %(W49)s/w1/ScrToolLedger/, and check whether a tracked ledger/checker exists: `git show %(TIP)s -- | grep` or `grep -rn 'live-state' quality/ corpus/ tools/ | head`). tools/mado-keysym.py (landed round 49) reads no live state; tools/mado-hostguard.py (landed this round) reads declared paths only. If the checker enforces all-tools-must-be-row-or-exclusion, draft the two rows/exclusions with a cited class reason to your seat dir (do not edit the lane). If no tracked ledger exists, say so plainly with the search evidence - the claim that it does is then a defect.")

# ------------------------------------------------- gate/tool attacks (6)
seat("MutGateInstalled", "mutation-tester",
     "Installed quality/check-session-material.py (sha256 ffdc9d62..., v3) both-ways.",
     "From a --shared clone at %(TIP)s: copy the gate to scratch; run selftest (expect 94/94). Mutate IN COPIES ONLY: (a) remove the R8 rule emission, (b) turn the waiver-delta retain into a remove, (c) bypass the waiver-target sha check, (d) make the waivable band include R5/R6 (the SURVIVED w1 mutant - it must now be caught or honestly reported as surviving with evidence), (e) weaken `emit`'s masking (would a raw value leak - prove it on a synthetic fixture, never real data). Score each mutant against the frozen PRED-C2-r50 counter at a fixture rev where the gate is mutant: every claimed kill must be an executed run. Control: pristine gate at %(TIP)s run with the frozen counter -> TARGET_MET.")

seat("CritSidecarsV3", "critic",
     "w1/CritSidecars residual: v3 scan with sidecars enabled and --no-waivers at the round-50 revision.",
     "Run the installed v3 gate on a --shared clone of the lane at %(TIP)s: once with the 47 round-49/50 sidecar waivers honoured, once with --no-waivers. Record per-target shape-only classifications for all waived matches and the exact delta (sidecars should only ever reduce findings, never change which rules fire on the target file). Confirm every waived match's identity is still reserved (the file's waiver row names it) and that no newly covered real-shaped value is suppressed. Shape-only output in your receipts - mask every value.")

seat("RevGateDelta50", "reviewer",
     "Gate v3 findings on the landed round-50 tree vs the w1 base-scan receipts.",
     "Run the installed gate at %(TIP)s (--repo a --shared clone) at scope all and ufo; compare rule-count tables to %(W)s/w1/ExecGateV3/receipts/base-scan-v3-*.txt (which ran at %(B)s before integration). The delta should name exactly the round-50 files (the new entry, lesson, quality/counters, wave dir, sidecars): R7/R8/R9 findings in round-50 artifacts are self-inflicted receipt material - classify each file count by path prefix (which dir), shape-only, and name any corpus/, quality/ or tools/ file that newly trips a rule (a defect). Receipts under your seat dir, masked.")

seat("MutC1ToolRandom", "mutation-tester",
     "tools/mado-keysym.py at %(TIP)s under exotic and random keymaps (w1 cut-off seats re-run).",
     "This closes w1 seats CritC1Random + CritC1Exotic + CritC1Judge's residue AND routed D3 (the unreceipted 57,865-pair figure). On a --shared clone: compile N random RMLVO keymaps (xkbcli compile-keymap, your own seeds, commit the seed list to your seat dir), draw M random (keymap, keysym) pairs, run the landed tool and the pinned judge `/usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym` on each, compare stdout+rc. Write a receipt with the exact command, seed list, pair count, mismatch count and both tool/judge sha256 (the round's committed random-pair figure; if it matches 57,865 say so, else name the true count - D3 wants a receipt or a correction). Then attack exotic keymaps: xkeyboard-config layouts with multiple groups, compose sequences, dead keys, LevelThree - any divergence the frozen 633-fixture set does not cover is a finding.")

seat("RevHostGuardInstalled", "reviewer",
     "Installed tools/mado-hostguard.py (sha256 fdaa5c2e...) and its both-ways receipts.",
     "At %(TIP)s: re-run `python3 -I tools/mado-hostguard.py --selftest --work <your scratch>` (expect 45/45). Re-run the seat's demo.sh on a fake home under your scratch (read %(W)s/w1/ExecHostGuardR50/demo.sh first; verify both ways: declared path changed -> exit 3; undeclared writes inside the fake home are or are not violations per the documented contract - check what the receipt claims). Try to defeat the guard in one way: a child that writes a declared path via a hardlink, an atomic rename (write tmp + rename), or a dirfd-relative openat outside the wrapped CWD. Report whether the digest comparison catches it.")

seat("SentScratch50", "sentinel",
     "Committed round-50 instruments honour TMPDIR/--work and refuse /tmp,/var/tmp,/dev/shm,home,inside-repo roots.",
     "Probe each landed instrument's refusals (expected rc 2 / refusal): `quality/counters/c1-r50-bind-entry.py` (TMPDIR), `quality/counters/c2-r50-session-gate.py` (--work + TMPDIR), `quality/check-wave-done.py` (--selftest --work), `quality/check-session-material.py` (--selftest --work if it takes one), `tools/mado-hostguard.py` (--selftest --work). Try TMPDIR=/tmp, TMPDIR=/var/tmp/x, TMPDIR=$HOME/scratch, TMPDIR=<lane>/x. Also check no committed tool hardcodes /tmp for >50MB writes (grep -n '/tmp' the five files; classify each hit). Receipts per probe.")

# ------------------------------------------------- process/consistency attacks (7)
seat("CritRegistration50", "critic",
     "`.ufo/waves/round-50/registration.md` vs the frozen bytes it names.",
     "Attack the registration document at %(TIP)s like w1/RevRegistration attacked round-49's: every named sha256 re-derived (counter scripts, entry, lesson, SOURCES.md, gate, instruments, receipt), every receipt path exists and its final line matches the verdict the registration quotes, control names resolve to real receipts, kill rules restate the predicate sentence EXACTLY as the counter emits it (diff the predicate text against the counter's final line format). Any mismatch (labels, counts, missing receipt, a control the registration claims but did not run) is a defect - list it.")

seat("ExecFreezeReplay", "executor",
     "Re-run every receipted freeze command byte-for-byte at %(TIP)s and re-produce the verification bytes.",
     "On a --shared clone at %(TIP)s (TMPDIR/--work under your scratch): (1) both counter data runs (`receipts/c1-at-data.txt`, `c2-at-data-nonce50117.txt` - fresh nonce allowed for c2, but name it), (2) both selftests on the installed bytes (gate 94/94, hostguard 45/45, check-wave-done 58/58 with --work), (3) `quality/check-wave-done.py --repo <clone> --rev %(TIP)s --round 50` and `--round 49`, (4) the census command at the lane tip. Produce one receipt file per run under your seat dir; a mismatch against the committed receipt line is a finding, and so is any receipt whose command does not reproduce. Report PASS/FAIL per command.")

seat("ScrCorrections50", "scribe",
     "w1/ScrCorrectionsR50's mid-write snapshot caveat and the landed erratum (D8).",
     "Re-run the w1 ScrCorrections commands against %(TIP)s: (a) the D8 erratum block appended to corpus/lessons/round-49.md - the proposed corrected sentence and its counting command must appear and the counts must re-derive (`grep -cE` the two patterns), (b) the lesson Gate admit/reject bullet counts in corpus/lessons/round-50.md (admit lines `^- \\*\\*S[0-9]{3} admit\\*\\*`, reject lines `^- \\*\\*REJECT`) - paste both outputs, (c) confirm the w1 reports ExecControlsC1/ExecCounterC1 (round-49 w1 tracked files the w1 reports saw dirty mid-write) are now clean at %(TIP)s (`git show %(TIP)s:<path>` vs the recorded w1 snapshots). Record landed/diverged per item.")

seat("SentPrivacy50", "sentinel",
     "Privacy shape of everything committed this round at %(TIP)s.",
     "Run the installed v3 gate on a --shared clone at %(TIP)s, scope all, --account <your invoking account>: findings inside `.ufo/waves/round-50/`, `corpus/`, `quality/`, `tools/`, `SCORECARD.md`, `LOG.md` are expected lanes - classify each by rule and path prefix, shape-only. Name any finding outside those dirs, any RAW value (device name, title, serial, home path, account) that landed in a committed round-50 file - grep the wave dir for the account name and for `/home/` literals (which files, how many occurrences, masked output). The two host receipts must carry counts and digests only.")

seat("RevClaimsCounter", "reviewer",
     "Claim/counter/admission consistency for C1 and C2 at %(TIP)s (claims.md vs registration vs receipts).",
     "Build the table: claim -> frozen counter (path+sha256) -> predicate sentence -> data rev -> receipt(s) -> controls. Check: (a) each claim is one axis-move (C1 coverage, C2 operability) and separable, (b) every receipt cited exists at %(TIP)s and its bytes contain the quoted final line, (c) C1's 'sourced' label is real (entry cites rows opened this round; the Gate dates 2026-10-27), (d) the two-nonce requirement for C2, (e) QUALITY criteria 100-102 exist and name runnable instruments that exist (check-state-cite, check-deliverables, check-wave-done), (f) README/SKILL pointers resolve. Any inconsistency is a defect.")

seat("ConnCrossClaim2", "connector",
     "Cross-claim coupling at the landed state, and the round-49-counter-attacks-validity question.",
     "w1/ConnCrossClaim found the coupling direction: C1 writes corpus files C2's default scope scans; C2 also reads C1's counter as an ordinary tracked file. Re-derive that at %(TIP)s: (a) list every file each frozen counter reads (grep their source for paths/opens), (b) check the installed v3 gate's base-scan receipts vs the landed round-50 files - does any round-50 committed file introduce a NEW finding beyond the lane's expected R7/R8/R9 receipts (run `git show %(TIP)s:<file>` pairs vs %(W)s/w1/ExecGateV3/receipts/base-scan-v3-all.txt rule counts and name the new offenders), (c) does C1's counter depend on C2's gate bytes or vice versa (should be no). A real coupling a counter misses is a defect.")

seat("SentHostState50", "sentinel",
     "No committed round-50 instrument can write host state; the outer-tracer false-miss trap (R-SHS-3).",
     "Static-read the five landed instruments (counters x2, gate, wave-done, hostguard, state-cite, deliverables): for each, list every write/exec/socket surface (open(.., 'w'), subprocess, os.replace, sockets) and prove each is confined to --work/TMPDIR/seat-out (locators). Then verify the one documented ambient read PRED-C1-r50 clause r does (hyprctl, read-only, scratch HOME). Do NOT strace/wrap a counter (outer-tracer false-miss is documented). Receipts: a containment table per instrument + one live `hyprctl version` read as control.")

# ------------------------------------------------- frontier/assimilation/axis attacks (5)
seat("ScoutAssimQuarantine", "scout",
     "The 13-row absent-defect register slice for lane mado; hand-check per row.",
     "Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (READ-ONLY). Slice: `awk -F'|' -v l='mado' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' <register>` = 13 rows (w1/ScoutAssimR50 derived: payload-absent S189 S195 S201 S205 S224 S228; prose-class S199 S200 S209 S222 S223 S225 S235). For EACH row: open its cited source yourself (fetch the URL, or read the local file), locate the quote/anchor the staged row claims, and land a verdict line in your seat dir `quarantine-verdicts.md`: S### -> adopted-verifiable | absent-refuse (fabrication class) | unverifiable-unreachable | prose-class-unlocatable, each with the fetch status, located quote (<=25 words) or the failure. No staged row gets appended; verdicts only. A row you cannot fetch is `unreachable`, never fabrication.")

seat("RevAssimGround", "reviewer",
     "The lesson's assimilation records (admit considerthese proposal 1; reject staged package; guard proof; quarantine carried).",
     "Check corpus/lessons/round-50.md's assimilation section against the ground truth: (a) considerthese/2026-10-26.md proposal 1 is indeed the privacy-receipt check and proposal 6 was landed in round 48 (QUALITY 99) - the lesson must not re-credit it; (b) `merge/mado/MERGE-REPORT.md` (read-only) truly lacks a Hyprland bind/keysym or session-material theme (grep for hyprland|bind|keysym|keymap|privacy|session-material in the staged entry names - report counts); (c) the id-collision guard numbers (reg 288 -> now 300, staged 147, collisions 94 in the w1 artifacts under w1/ScoutAssimR50/assimilation/); (d) every still-pending quarantine verdict the wave-w2 scout lands is reflected - flag any lesson sentence claiming a verdict that the seat's file does not carry.")

seat("ScrGateLesson50", "scribe",
     "corpus/lessons/round-50.md content completeness vs the round-49 format and the routed items.",
     "Compare the landed lesson against corpus/lessons/round-49.md's structure: Gate admits+rejects+status changes, assimilation block, Mistakes rows. Verify each M50-* row names class/evidence-pointer/captured-by/fix and each evidence pointer resolves at %(TIP)s. Verify the lesson does NOT pre-claim w2 outcomes (admission judgments stay the L1's + non-author closure's). Verify the Gate's reject lines carry a flip condition and the 5 reject classes match ScrRowsR50/gate.md. Report missing/weak rows.")

seat("RevN4Tip", "reviewer",
     "Axis-table and evidence-pointer sanity at the round tip (last check before the report).",
     "At %(TIP)s: (a) re-run the axis command from %(W)s/receipts/axis-base.txt (`checked=3 mismatched=0` at base) - the tip form must print MATCH for all 3 axes or name the mismatch; (b) every path cited by corpus/lessons/round-50.md and registration.md resolves (git cat-file -e at %(TIP)s); (c) the tools/README/ledger consistency: tools/mado-hostguard.py and tools/mado-keysym.py presence vs any inventory (report what exists); (d) git log %(B)s..%(TIP)s lists exactly the round's commits - name each with its subject. Output one verdict line per item.")

seat("CritWaveDoneGate", "critic",
     "quality/check-wave-done.py landed draft (58-case selftest) - attack the contract it encodes.",
     "From %(TIP)s: re-run its --selftest with --work under your scratch (expect 58/58). Then build a scratch fixture repo proving a FALSE POSITIVE or FALSE NEGATIVE: (a) a results file where every row has output null + note but NO seat report file exists - does the gate still say OK (the dropped strictness clause)? Is that per the dispatcher contract (%(FLEET)s/scripts/hyaku/inline-dispatcher.py:293-295) or a hole? (b) a wave whose dispatch JSON names seat `X` but results renames it `x ` (whitespace) - settled or duplicate? (c) a results file with an extra seat the dispatch lacks. Report the verdict each gives and whether it is defensible under the contract the tool docstring declares (see %(W)s/w1/ExecWaveDone.md's contract table).".replace("%(FLEET)s", "/home/vgpnk/Projects/shokunin"))

spec = {"wave": "w2", "context": sub(CONTEXT), "reportDir": ".ufo/waves/round-50/w2", "items": items}
out = W + "/w2-spec.json"
json.dump(spec, open(out, "w"), indent=1)
print("wrote", out, "items=", len(items))
