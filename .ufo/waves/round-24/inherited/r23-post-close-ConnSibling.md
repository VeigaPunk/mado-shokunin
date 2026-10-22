# ConnSibling — sibling overlap scan for round 23 (C1, C2, C3) and mutation-reporting conventions

Seat `MadoR23.ConnSibling` (connector, leaf). Scan at 2026-10-22 ~11:00Z, lane `master` at
`a28e4815aabfa85f55274884000fb2608355f8cf`. I wrote only this file. No edits anywhere else, no
installs, no subagents, no jj commands, no classifier runs.

**Verdict: no contested ownership on any of the three claims.** No sibling corpus or PROVINCE
holds foot, kitty or ghostty config knowledge, no sibling classifies seat-issued commands for host
harm, and no sibling PROVINCE names any of mado's four unnamed tools. Two adjacencies are new
relative to mado's round-22 ConnProvince: souji's `souji-seat-audit.py` (a second classifier of
seat tool calls, on a different substrate) and the fact that the routed tameshi pin `f4e8f7d8` is
not the note's current bytes. One move is proposed for the MutMeasure and MutTruth seats.

## Sibling pins used

tameshi `a08e85c5d7f8` (HEAD; working tree dirty on two cited files, see below), souji
`4edb25dfe262`, mori `8ef481ea7f9e`, kotoba `f054b8e88f4c`, kumitate `dfa159d5152f`, kagi
`899c50b42634`, tsukuroi `0cd9b28bee5f`, tabi `e3cf4e0d30bb`. Every path:line below is read at
those working trees. The cited souji and tsukuroi files have clean `git status`.

## C2 coverage — foot, kitty, ghostty config knowledge

**Overlap: none.** No sibling corpus documents any of the three config trees. The only sibling
facts that touch them are package and process state, which help the HostFoot, HostKitty and
HostGhostty seats cross-check their conclusions but cannot satisfy the C2 counter, because the
counter needs a `mined` SOURCES row opened 2026-10-22 naming the terminal.

Reusable cross-checks (all observed 2026-10-14, so eight days stale; re-probe before relying on them):

- `tsukuroi-shokunin/corpus/knowledge/update-safety-v3.md:190-193`: the `ghostty`,
  `ghostty-nautilus`, `ghostty-shell-integration` and `ghostty-terminfo` packages were **not
  installed**; extra `1.3.1-2` is shadowed by a newer omarchy `1.3.1-3`. Same fact at
  `update-safety-note.md:269` and `update-safety-v2.md:90`. HostGhostty's `pacman -Q ghostty`
  should agree or record the change.
- `tabi-shokunin/corpus/knowledge/hygiene-sweep-r4.md:113-114` and
  `tabi-shokunin/corpus/evidence/w4-t4-3-sweep/forensics.log:13`: the live terminal in a seat's
  process ancestry was **alacritty** (shell → kimi → alacritty → Hyprland). It is evidence that
  the live terminal tree is alacritty's, not foot's, kitty's or ghostty's.
- `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:70-71` and
  `mori-shokunin/corpus/knowledge/observability-census-r1.md:94,143`: terminal launches go
  through `xdg-terminal-exec` (`app-Hyprland-xdg-terminal-exec-*.scope`), which supports the
  host seats' plan to read `~/.config/xdg-terminals.list`.
- Upstream documentation: zero sibling SOURCES rows or corpus URLs for foot (codeberg dnkl),
  kitty (sw.kovidgoyal.net) or ghostty (ghostty.org). Nothing to reuse; C2 has to mine its own.

Ownership is consistent across siblings: mado's `PROVINCE.md:7-8` claims the terminal config
trees, and tsukuroi `PROVINCE.md:48` (ADJ-03) and `:124` (OUT-004) route terminal configuration
to mado. No conflict.

The bare-word scan mostly hit noise: audio's `foot` subprocess variable in `measure_audio.py`,
"foot" in kotodama's linguistics notes, and a product name in kengaku's benchmark evidence.

## C1 operability — transcript tripwire and static spawn-classifier work

**Overlap: none on the question C1 asks.** No sibling statically classifies seat-issued commands
(including `subprocess` spawns in eval code) for host mutation, package query, live probe, tool
install or VCS writes. Positive control: the `toolCall`/`arguments.command` regex matches
`mado-tripwire.py` (2 hits) and no file under any sibling `tools/`, `scripts/` or `corpus/`
(excluding `live/` and `evidence/` copies). No sibling `PROVINCE.md` mentions a tripwire or spawn
classifier.

Sibling readers of transcripts, each answering a different question:

| Sibling | What it reads, for what | Anchor | Relation to C1 |
|---|---|---|---|
| souji | Harness-rendered `history://` text exports (`→ tool(args…) ⇒ status`). It classifies every recorded tool call against the wave contract: forbidden surfaces, write scope, `V-SIGNAL` kill calls including the `sudo` prefix, `V-EXEC`, `V-PROBE` | `souji-shokunin/tools/souji-seat-audit.py:2-45`, prefix regex `:118`, selftest `signal-sudo-kill` `:639`; corpus row `souji-shokunin/corpus/README.md:277` | **New adjacency.** It is the closest functional sibling (it classifies issued commands), but it uses a different substrate (rendered text, not JSONL) and question (contract compliance, not host harm). Not listed in mado round-22 `ConnProvince.md:48-57`. Not claimed in souji's `PROVINCE.md`. |
| mori | Last `type=message` record of a v3 transcript tail, for terminal seat status | `mori-shokunin/PROVINCE.md:103-105`; `corpus/knowledge/seat-terminal-status-r17.md:9-12,37` | Same JSONL substrate, status not commands. Mori's own prior-art scan names `mado-tripwire.py` as its near neighbour: `mori-shokunin/.ufo/waves/round-17/build/SiblingSeatDeathTools.md:8-12,43-53` (its tripwire line numbers are from r17 bytes and are stale now). |
| kotoba | OMP session JSONL `toolCall` args for `skill://` activation counts | `kotoba-shokunin/corpus/knowledge/skill-activation-telemetry.md:23,66` | Same record type, telemetry only. |
| kumitate | Rust native transcript reader; task-dispatch `arguments` re-parsed when they arrive as a JSON **string** | `kumitate-shokunin/corpus/knowledge/native-transcript-ledger-seats.md:11,160-162` | Shape fact, see the second-order check below. |
| kagi | opencode SQLite DB, secret-shaped tripwires | `kagi-shokunin/corpus/knowledge/transcript-hygiene.md:3-7,39`; `PROVINCE.md:33,48` | "Tripwire" means a secret-leak gate here; unrelated substrate. |

Other sibling "tripwire" hits are unrelated uses of the word: kake fleet-registry probes
(`kake-shokunin/corpus/knowledge/fleet-registry.md:5,31`), kumitate's dedupe asymmetry pin
(`distill-and-l3.md:88,104`), kotoba's sentinel file (`substrate-pin-guard-round23.md:36`),
souji's `--baseline` gate (`lessons/round-20.md:307,388`) and 551 game-dev-2d fixture comments.

Second-order check on the kumitate shape fact: `mado-tripwire.py:2849` turns a non-dict
`arguments` into `{}`, so a bash call with string-encoded arguments would count as a bash call
with no finding and no unparsed counter. I counted `toolCall` argument types over the lane's 2889
tracked `.jsonl` files: 1576 bash and 2385 eval calls have dict arguments, and the 12 non-dict
cases (list, null, number, string) all sit in round 20's deliberately authored
`.ufo/waves/round-20/w2/AdvCrash/fixtures/` (e.g. `args_string.jsonl`). The shape is already
adjudicated there; nothing for C1 to do. Whether OMP ever emits string arguments for bash or eval
calls in live sessions is `[INFERENCE]` / unmeasured; I did not read live sessions.

Prior sibling characterizations of the tripwire (all consistent with C1; none claims it):
`tameshi-shokunin/.ufo/waves/round-17/w1/C01SiblingOverlap.md:53`,
`kotodama-shokunin/.ufo/waves/round-50/build/ConnectSiblingJj.md:23` (jj handling at
`mado-tripwire.py:84-108,622-654`, older bytes), and
`kama-shokunin/.ufo/waves/round-23/build/advice/ConnFleetAuditors.md:144-146` (mado-tripwire and
mado-verify mention git in prose only and are not exposed to GIT_* environment variables).

## C3 calibration — PROVINCE boundaries over the same tools

**Conflict: none.** In every sibling repo, outside `.ufo/`, nothing names `mado-action-plan`,
`mado-assessment`, `mado-evidence-audit` or `mado-tripwire`. Inside sibling `.ufo/` wave reports
they appear only as overlap census or prior art (the table above, plus
`mori-shokunin/.ufo/waves/round-20/build/GtLaneMado.md:30-31` on the tripwire's frozen and verdict
schemas). The sibling PROVINCE references to mado name only its config plane
(`game-dev-3d-shokunin/PROVINCE.md:75`, `kotoba-shokunin/PROVINCE.md:50`, tsukuroi `:48,124`)
or its already-named `tools/mado-verify.sh` (`tameshi-shokunin/PROVINCE.md:32-35`, tameshi's
mutation service target; mado `PROVINCE.md` already contains `mado-verify`).

Reusable scope statements for the append-only PROVINCE refinement:

- `kotoba-shokunin/.ufo/waves/round-49/build/CensusMado.md:40-46`: `tools/` was five files over
  mado's own config plane, and `tools/mado-assessment.py:21` encodes the SHONEN promotion item as
  a probation gate over mado's own files only ("applied to no other lane"). That is a sibling's
  independent wording of mado-assessment's scope.
- mado round-22 `ConnProvince.md:13-18`: the tripwire is an integrator-admitted mado capability
  (MANIFEST `rounds[359]`, `rounds[362]`). No fleet surface references `mado-tripwire`,
  `mado-assessment` or `mado-evidence-audit`.
- Open item that the C3 wording should not paper over: round-22 `ConnProvince.md:19-22` (CP-U1).
  Round 20 ran the tripwire over the whole fleet's session root, and the receipts name sibling
  seats. A PROVINCE line saying "read-only over mado's own surfaces" would be false for the
  tripwire's historical use. Say "read-only; inputs are transcript files it is given" or similar
  instead.

## Mutation-test reporting conventions for MutMeasure and MutTruth

**Pin status.** The routed pin `f4e8f7d8` ("round-25: retain late SiblingOverlap seat report") is
an ancestor of tameshi HEAD `a08e85c`, and `mte-report-interop.md` is byte-identical at the two
commits (`git diff f4e8f7d8 HEAD` is empty). The **current bytes differ**: the working tree has
an uncommitted round-26 refresh (sha256 `6e10d010…` vs `b173e3e5…` at the pin). It rewrites
`verified-at` (line 2) and appends "Round 26 append — nine legs" (`:172-180`). Lines 1 and 3-170
are unchanged, so the line numbers below are valid at both. Tameshi's own rule
(`tameshi-shokunin/SKILL.md:150-157`) calls a pin on uncommitted bytes a false anchor, so cite
`f4e8f7d8` for content and treat the nine-leg text as unlanded. Tameshi `SKILL.md` is also dirty,
but only at `:2085+`, and the cited lines 140-234 are identical at the pin, HEAD and the working
tree.

Conventions that apply (cite as `tameshi-shokunin/SKILL.md` @ f4e8f7d8):

1. **Green control first** (`:140-149`). Run the pristine `measure.py` and `truth.py` copies
   against the base classifier and record the exact verdict line, count and exit (the before value
   is 6/12 for measure, 12/12 for truth). "A red control has no kill denominator": stop and record
   a setup failure.
2. **Pin committed bytes** (`:150-157`): path, sha256, size, lines, revision, and an empty
   `git status --porcelain` for `repair/measure.py` and `repair/truth.py`.
3. **Pre-register** `expect: killed|survived` plus the reason for every mutant before running
   (`:162-170`, template `:261`). That makes an expectation miss a calibration datum.
4. **Uniqueness gate** (`:171-178`): `count(old) == 1` in the pristine copy, `new != old`, and
   mutant sha256 ≠ pristine (`:182`). A no-op is a driver defect, not a survivor.
5. **One mutant per fresh copy**, never compounded (`:179-188`), with a timeout. Retain stdout,
   stderr, exit, mutant sha, duration and the verdict line.
6. **Adjudicate on exit AND verdict token, never exit alone** (`:189-204`). Kills can be
   token-only. Quote the failing case labels; "a kill quoted without its failing labels is
   unverified".
7. **Three verdicts** (`:205-213`). KILLED, SURVIVED (a finding that names a gap), and
   INCONCLUSIVE (timeout, crash before the summary, count not enumerated). Kill rate is
   `killed/(killed+survived)`, with inconclusive runs excluded and named beside it.
8. **Survivor non-equivalence probe** (`:214-223`). Show an input on which the mutant's output
   differs from pristine; otherwise record it as possibly equivalent code (a calibration item).
9. **Restore proof as the headline** (`:224-229`): after-sha equals before-sha and the lane path
   is clean.
10. **Record shape** (`:230-234`): a kill-rate table (control + one row per mutant: exact edit and
    site, exit, verdict line, verdict, failing labels), survivor probes and reproduce commands.

If a seat also emits a machine report in mutation-testing-elements form
(`mte-report-interop.md` @ f4e8f7d8): map KILLED → `Killed`, SURVIVED → `Survived`,
INCONCLUSIVE → `RuntimeError`, and **never** `Timeout`, since Timeout counts as detected and would
inflate the score (`:24-31,90-107`, decision table `:159-164`). Use `language: "python"`
(`:41-43`) and 1-based end-exclusive locations derived from a unique `@old` string (`:48-52`).
Report the score as the unrounded `k/(k+s)` (`:110-124`). The vendored schema/metrics are pinned
to 3.9.0 (`:136-140`), and the score equality is a sanity check by construction, not an
independent measurement (`:141-142`).

Mado's own precedent is close to this already: round-18 `MutTripwireScan.md:22-25` ("killed only
when pristine passes, mutated rejects, restoration passes"; "8 killed, 12 survived, 0
inconclusive"). The gap is pre-registration and survivor non-equivalence probes, which tameshi
requires and mado's round-18 `MutMeasureR17.md:7-11,46-50` (nine survivors) did not record per
mutant.

## Proposed move (one)

**Make MutMeasure's verdict discriminate KILLED from INCONCLUSIVE on the counter's own error
paths.** Two of MutMeasure's six required mutants ("drop the exit/error check", "skip the tamper
check") act on the code that makes `measure.py` exit non-zero for setup reasons. Under convention
6, a mutant run that exits 2 or times out because the scratch layout or HELPER path is wrong is
INCONCLUSIVE, not KILLED. MutMeasure is told to "find a tool output under which the mutant gives
a different verdict". A difference caused by a setup error looks the same in that test, so it
would inflate the kill count. The fix is to pre-register, for each mutant, the expected verdict
line of both pristine and mutant on the chosen output, and to count KILLED only when the pristine
copy gives its expected verdict line on that output (a green control for the pair) and the mutant
gives a different, well-formed verdict line. MutTruth uses the same rule for its tamper-check and
`safe()` import-gate mutants, plus a scratch-only wrong-expectation copy as the red input.

- **Axes:** C1 operability, through verification strength: the 12/12 claim rests on a counter
  whose mutation record is trustworthy. Nothing in `tools/`, the frozen set or any guard changes,
  so no other axis is touched.
- **Risks:** fewer reported kills (honest, not harmful). Seats may need a second, deliberately
  wrong classifier output per mutant, which the MutMeasure prompt already allows ("trivially
  edited copy of the classifier in scratch").
- **Verification:** each Mut receipt row carries `pristine_verdict_line`, `mutant_verdict_line`,
  `exit` and `verdict ∈ {KILLED, SURVIVED, INCONCLUSIVE}`. The L1 checks that no KILLED row has a
  pristine exit ≠ 0 or a missing verdict line on the same input.

## Commands run (all read-only)

- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/corpus` (21 corpora; mado excluded from scans).
- Bare-word scan: `rg -n -i -w 'foot|kitty|ghostty' <20 sibling corpora>` (noise, see above).
- Narrow scan: `rg -n -i '\.config/(foot|kitty|ghostty)|foot\.ini|kitty\.conf|ghostty/config|xdg-terminal|terminal[- ]emulator|footclient|\bkitty\b|\bghostty\b|alacritty' <corpora>`. Per-repo hits: tsukuroi 15, kengaku 2 (noise), mori 2, tabi 2, tameshi 1 (walker, unrelated).
- Upstream URL scan `rg -i 'dnkl/foot|codeberg\.org/dnkl|sw\.kovidgoyal\.net|kovidgoyal/kitty|ghostty\.org|ghostty-org' <corpora>`: 0 hits.
- `rg -n -i 'tripwire' <corpora>`: game-dev-2d 551, kagi 26, kake 16, tameshi 10, kumitate 7, souji 3, game-dev-3d 2, kengaku 2, kotoba 1. Each was read in context.
- Classifier-vocabulary scan (`toolCall|host_mutation|vcs_write|package_query|live_probe|tool_install|unparsed_spawn`) over corpora: only kotoba `skill-activation-telemetry.md:66` and kumitate `native-transcript-ledger-seats.md:33` are relevant.
- Tool scan of `toolCall`/`arguments.command` over sibling `tools/ scripts/ corpus/` (py/sh/mjs): 0. The same regex gives 2 hits on `mado-tripwire.py`.
- Mado tool names: `rg 'mado-(action-plan|assessment|evidence-audit|tripwire)'` in each sibling repo. Outside `.ufo`: 0. Inside `.ufo`: 10 files, all listed above.
- Sibling PROVINCE scan: `rg -n -i 'terminal|foot|kitty|ghostty|tripwire|transcript|spawn|mado' */PROVINCE.md`.
- Tameshi pin: `git log -1 f4e8f7d8`; `git merge-base --is-ancestor f4e8f7d8 HEAD` (true); `git diff f4e8f7d8 HEAD -- corpus/knowledge/mte-report-interop.md` (empty); `git diff HEAD -- …` (round-26 hunks); sha256 of current file `6e10d010…` and of the pinned blob `b173e3e5…`; `git diff -U0 HEAD -- SKILL.md` and `f4e8f7d8 HEAD` (hunks only at `:2085+`).
- Argument-shape count: a `python3 -I` JSON reader over `git ls-files '*.jsonl'` in the lane (2889 files). It printed counts and file names only.

Installs: none. Sources: no external source opened.

**Verdict: adjacency clear — no contested ownership for C1, C2 or C3. One new adjacency (souji-seat-audit) and one pin caveat (tameshi note dirty past f4e8f7d8). One proposed move for MutMeasure/MutTruth: count a kill only when the pristine verdict on the same input is green.**

## Addendum (2026-10-22 ~11:40Z, after IRC from MadoR23.ScribeProvinceScope)

The C3 counter of record is now v2 (lane commit `4de4464`, registration "Second pre-measurement
clarification" item 4). I re-ran it: `python3 -I .ufo/waves/round-23/c3/count.py <rev>` gives
count **5**, exit 1, at both `e33ea304` and `a28e4815`. v2 credits a tool only through a
PROVINCE.md table row whose first cell is exactly the backticked tool path, with the first four
cells non-empty. One correction to the C3 section above follows from that. "mado `PROVINCE.md`
already contains `mado-verify`" was true for v1 only. Under v2, `tools/mado-verify.sh` is
unaccounted until it gets its own row. The no-conflict finding stands: no sibling claims any of
the five tools.

Adjacency check of the scribe's draft table (`ScribeProvinceScope.md:45-51`): all five rows parse
as 4 cells. The tripwire row's owner cell names mori, tsukuroi and kagi, and refuses the
fleet-wide reading (CP-U1). **It does not name souji** (0 mentions in the file), even though
`souji-shokunin/tools/souji-seat-audit.py:2-45` is the one sibling tool that also classifies
seat-issued tool calls. Suggested clause for that cell: "souji (seat-contract audit of rendered
tool calls, `souji-seat-audit.py`)". This is an adjacency gap, not a counter issue; v2 passes
either way.

## Addendum 2 (2026-10-22 ~11:50Z, landing status)

The scribe reported "L1 landed" the draft at 08:38:28 -0300. What I measured is that it is **in
the working tree, not committed**:

- `git status --porcelain -- PROVINCE.md` shows ` M`; HEAD is still `4de4464`. The file's mtime is
  08:38:28 -0300, 7626 B, sha256 `78bca86d…`.
- The change only appends: `git diff --numstat` gives 10 lines added, 0 removed.
- The counter of record reads committed bytes (`git show REV:PROVINCE.md`). At HEAD it still
  reports **count 5, exit 1**.
- In a scratch clone (`/fast/scratch/hyaku/mado-r23/ConnSibling/clone`), I committed exactly the
  working-tree bytes and ran the counter: **count 0, exit 0**, mismatches `[]`, all 5 tools
  accounted for.
- The working-tree text has 0 mentions of souji, so it is the variant before the souji fix.

So C3 = 0 holds only once those bytes, or the souji variant, are committed. The after-value
must be measured at that commit, consistent with registration clarification 10 (committed
bytes). The souji anchor checks out: `souji-shokunin/SKILL.md:200` is its gate row.

## Addendum 3 (2026-10-22 ~11:55Z, C3 landed)

- L1 committed the refinement at `2f1134f38930fc8b067d2d7f5bba126338faabdd`: +10/−0, single hunk
  `@@ -19,0 +20,10 @@`, 30 lines, sha256 `78bca86d…`. `python3 -I .ufo/waves/round-23/c3/count.py
  2f1134f3…` gives **count 0, exit 0**, mismatches `[]`, all 5 tools accounted for. Before
  (`4de4464`, v2) it was 5. C3 is met on committed bytes.
- The after-receipts are **untracked**. `git status` shows `??` for
  `.ufo/waves/round-23/evidence/c3-after-2f1134f3.json` (byte-identical to my run),
  `c2-after-2f1134f3.json` and `repair-after-2f1134f3.json`. They exist on disk only until
  committed.
- The landed text still has no souji mention. Changing the committed tripwire owner cell would
  rewrite a landed line, so it would not be append-only. The append-only way to add souji is a
  new line after the table, e.g. a dated adjacency note naming
  `souji-shokunin/tools/souji-seat-audit.py`.
- No LOG.md entry for round 23 (`git log 4de4464..HEAD -- LOG.md` is empty). This is outside
  my adjacency scope; I'm recording it because the scribe raised it and I confirmed it.

## Addendum 4 (2026-10-22 12:10Z, tip moved)

Lane HEAD is now `3732c7a` (after `03227dd`, a C1 wave-2 repair). `3732c7a` appends 2 lines to
PROVINCE.md (`@@ -29,0 +30,2 @@`, 0 removed): a "Round-23 wave-2 correction" paragraph at line 30,
before the closing line, which is now line 32. At `3732c7a` the C3 counter gives **count 0, exit
0**, with all 5 tools accounted for. PROVINCE.md still has 0 souji mentions. So C3 still holds,
but the landed tip for after-values is now `3732c7a`, not `2f1134f`. The `*-after-3732c7a7.json`
receipts are untracked, like the `2f1134f3` ones. LOG.md is modified in the working tree but not
committed. The proposed souji line now goes after line 30, before line 32. Its earlier
"3 inserted / 0 deleted" check was made against `2f1134f3` and needs redoing at `3732c7a`.

## Addendum 5 (2026-10-22 12:25Z, open items closed)

Lane HEAD is now `8e5d936`. PROVINCE.md hasn't changed since `3732c7a` (32 lines, 0 souji
mentions), and the C3 counter at HEAD gives **count 0, exit 0**. The two open items in
addendum 4 are closed:
- LOG.md: committed in `3df1062`, which has a "C3 (calibration)" entry at `LOG.md:1561`.
- Receipts: all six after-receipts are tracked, and `evidence/` is clean.

`c3-after-3732c7a7.json` matches my run of the counter at the full `3732c7a…` SHA byte for byte.
The only open C3 adjacency item is the optional souji line. `3df1062` also withdrew the C1
classifier to its base bytes ("honest stop"); that is outside this connector's scope.
