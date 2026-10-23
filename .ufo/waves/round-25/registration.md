author: mado

# Round 25 — registration (written and landed before any control or data seat)

Base: lane tip `41cc04c8d593837a0d5078bffaacdaa163d12897` (includes the round-24 closure
`corpus/lessons/round-24-verifier-spotcheck.md`, rejected-honest-stop). Prompt `.ufo/prompts/mado-round-25.md`.
L1 holds the canonical planner seat. Order this round: registration + frozen counter + before receipt (this
commit) → control call → control receipts landed → wave 1 (data) → wave 2 (falsify). No data seat exists before the
control receipts land; the receipts commit is cited in the report with its time, and wave 1's registry `createdAt`
must be later.

Anti-loop: rounds 20–23 worked the tripwire classifier, round 24 a knowledge-note counter and a transcribed
capability table; all were rejected. This round works neither: one new runnable tool on a surface the lane has
never instrumented (the Hyprland bind table), and one exploratory claim. Routed repairs are repairs, not claims.

## C1 — operability, capability acquisition (sourced): static Hyprland bind-table resolver

Surface moved: a new tool, `tools/mado-binds.py`, over the P1 Hyprland config tree (`~/.config/hypr/**` and the files
it sources). Today the lane can read the bind table only from the running compositor (`hyprctl binds`); it cannot
say what a config tree will bind before the operator applies it. The tool reads config bytes only (no compositor, no
socket) and prints the bind table Hyprland v0.56.2 would build, as a JSON array with the 18 `hyprctl binds -j` fields.
The command that shows the surface unmoved: `git show REV:tools/mado-binds.py` fails, and the counter prints
`tool=MISSING_TOOL`.

Tool interface (frozen): `python3 -I tools/mado-binds.py --home DIR` reads `DIR/.config/hypr/hyprland.conf` as root,
expands `~` to `DIR`, follows `source =` (globs included), prints one JSON array to stdout, exit 0.

**PRED-C1** (the same sentence as the counter docstring and the receipt label `PRED-C1`):
At REV, the committed bytes of tools/mado-binds.py, run in a bubblewrap sandbox (no network, no /run, cleared
environment, HOME = a fresh case directory), reproduce the expected bind multiset exactly over all 18 hyprctl JSON
fields for the unperturbed snapshot of the four Hyprland config roots and for each of 32 counter-generated cases (4
each of ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT on that snapshot, and 4 SYNTH whole synthetic config
trees), and the tool bytes contain none of the live capture's arg or description strings of 12 or more characters;
target: cases_pass=33/33 and embed_hits=0.

- Counter: `python3 -I .ufo/waves/round-25/c1/count.py REV` (sha256:`70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`).
  Exit 0 `TARGET_MET`, 1 `TARGET_MISSED`, 2 setup error or `UNSTABLE` (live capture changed during the snapshot).
  Perturbations come from a fresh `os.urandom` seed per run (printed; `--seed` replays). The unperturbed case expects
  the live `hyprctl binds -j` capture; every other case expects the delta the counter itself wrote (Hyprland v0.56.2
  `efb50993`: legacy `ConfigManager::handleBind`/`handleUnbind`/`parseKey`, `KeybindManager::stringToModMask`/
  `removeKeybind`, `HyprCtl` `bindsRequest`; hyprlang v0.6.8 `3a1c1b25` comment handling; hyprutils v0.14.2
  `a21e87b8` `CVarList` trimming).
- Before @ `41cc04c8`: `tool=MISSING_TOOL`, `PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED`, exit 1
  (`evidence/c1-before-41cc04c8.txt`, seed `0123456789abcdef`).
- Target after: `cases_pass=33/33 embed_hits=0 verdict=TARGET_MET`, exit 0, measured at the lane commit that lands
  the tool, on one fresh seed, receipt committed. Kill rule: any other result is a miss; reported, never amended, never
  re-scaled, never re-run until it passes (one measurement run at the measured commit; a run that exits 2 is
  re-run and both receipts are kept).
- Why a do-nothing or shortcut control cannot meet it (to be scored by the control call before data): absent tool 0;
  `[]` or junk 0; a server echo (`hyprctl binds -j`) cannot reach a socket inside the sandbox and in any case does
  not contain the perturbations; an embedded copy of the live table trips `embed_hits` and fails every non-BASE case
  except UNSOURCED; a grep of every bind line under the roots fails UNSOURCED, UNBIND and COMMENT; a cache of the
  original files plus a delta parser has nothing to cache in SYNTH. Keys, mods, flags, descriptions and args of
  generated binds are random per run, so no fixture id or label exists to key on.
- Capability row enters the SCORECARD capabilities table only if the after-run is `TARGET_MET`.
- Sourced: the tool docstring and a knowledge entry `corpus/knowledge/bind-table-r25.md` cite SOURCES rows opened this
  round (Hyprland, hyprlang, hyprutils pinned sources).

## C2 — calibration (lowest scored axis), exploratory

Calibration is the lowest scored axis (literal lesson-cited rubric 26/35 = 7.4286 at base, SCORECARD round-24
results). Declared **exploratory**: no counting command, verdict only `unprovable-but-better` from a named non-author
reviewer, otherwise `unprovable`.

What it improves: the lane's present-tense self-assessment is spread over 24 rounds of append-only SCORECARD sections;
stale present-tense rows (`SCORECARD.md:437` collision screen "current exits 0", `:1342` "L 17/18") stayed unmarked
until an outside closure found them (round-24 closure §2.2, §7.6). The claim adds one appended section,
`## Current state (round 25)`: every capability row in the file (each table row under any capability table, wherever
it sits) with its location, its stated claim, the status a fresh re-run at the base revision observed, the command,
and a pointer to any row that supersedes it; plus a pointer at each stale row. Why the prior state lacked it: the
round-24 status table covered 12 of 15 rows and was itself a transcription of a counter (round-24 closure §2.2).
Not claimed: any calibration score change. This claim is not a counter and is not judged as one.

## Routed repairs (round-24 closure §7; repairs, not claims)

| # | Defect | Disposition this round |
|---|---|---|
| R1 | C1 counter weak (M24-2) | The round-24 C1 claim is closed and its counter is not reused. QUALITY criterion 36 (cites M24-2, M24-5): a claim's control receipts cover the named shortcut shapes and land before any data seat; check `quality/check-control-receipts.py`, shown red on round-24 bytes. |
| R2 | C2 population/transcription (M24-5) | Same criterion 36; round-24 C2 closed, not reused. |
| R3 | `rule-attribution-r24.md:25` A18 body contradicts errata | In-row correction pointing to the errata. |
| R4 | lesson 24 S161 rationale false | Appended correction in `lessons/round-24.md`. |
| R5 | "receipts before any data seat" false | Appended corrections in round-24 `registration.md` and `lessons/round-24.md`. |
| R6 | `SCORECARD.md:437`, `:1342` stale rows | Pointer lines at the end of each row's section (C2 ledger names them too). |
| R7 | report SHONEN boxes without pointers | This round's report cites a resolvable pointer per box or marks `[ ]`. |
| R8 | carried: H2 (L0 `.ufo/l0-questions.md:103`); QUALITY 33–35 check survivors | H2 stays open (tripwire not touched). Hardened checks for the named survivors (MutCheckRegOrder, MutCheckReceipt) under `round-25/quality/`, old checks kept. |

## Separability and harm watch

C1 needs no SCORECARD or lesson text; C2 needs no tool. Harm watch at the measured commit: `tools/` other than the new
file byte-identical to base; census exit 0; no line removed from LOG, SCORECARD, QUALITY, README, SOURCES except the
R3 in-row correction (one line, reported); PROVINCE gains one tool row only if C1 lands; round-23 C3 counter = 0 and
round-23 C2 counter = 3/3 re-run by wave 2.

## C1 counter v2 — pre-data amendment (after the v1 control call, before any data seat)

The v1 control call (10 seats, receipts `controls/Ctl*.md`) scored every shape under counter v1
(sha256:`70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`, kept byte-identical as `c1/count-v1.py`):
none met v1 (best: CtlCacheDelta 25/33, CtlLabelKeyed 25/33). CtlLabelKeyed's critique named a shape no seat built:
an embedded (encoded) live table plus a parser for only the counter's own generator grammar plus source reachability
could pass every v1 case without parsing one real config line, because every v1 edit of the real tree is a local
delta and SYNTH uses the generator's vocabulary. v2 answers that design gap (not an observed score): it adds 4
**REWRITE** cases, which re-spell every sourced real file without changing its meaning (mod names lower-cased,
whitespace around `=` and the first two commas of every bind line, inserted comment lines) and make three edits whose
vocabulary is copied from the live table (the arg of one real bind replaced by another real arg, one bind added with a
real dispatcher/arg/description, one real bind unbound). No line keeps its cached bytes, and the new line cannot be
told apart by vocabulary, so a cache or an embedded table needs a full parse of real lines to find the edits. SYNTH
also lost its fixed `# synthetic tree` first line. Nothing else changed.

**PRED-C1 (v2, the claim's rule)** — the same sentence as the v2 counter docstring and the receipt label `PRED-C1`:
At REV, the committed bytes of tools/mado-binds.py, run in a bubblewrap sandbox (no network, no /run, cleared
environment, HOME = a fresh case directory), reproduce the expected bind multiset exactly over all 18 hyprctl JSON
fields for the unperturbed snapshot of the four Hyprland config roots and for each of 36 counter-generated cases (4
each of ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT and REWRITE on that snapshot, and 4 SYNTH whole
synthetic config trees), and the tool bytes contain none of the live capture's arg or description strings of 12 or
more characters; target: cases_pass=37/37 and embed_hits=0.

- Counter v2: `python3 -I .ufo/waves/round-25/c1/count.py REV`, sha256:`b251ddecb3a99993bbb8a7e9cb2363896da7f69ac58bf63e6b8deb2e0ccf81a8`.
- Before @ `41cc04c8` under v2: `PRED-C1 cases_pass=0/37 embed_hits=0 verdict=TARGET_MISSED`, exit 1
  (`evidence/c1-before-v2-41cc04c8.txt`).
- Both rules are reported at the after-measurement: v2 (the claim's rule) and v1 (`python3 -I
  .ufo/waves/round-25/c1/count-v1.py REV`, target 33/33), one fresh seed each, so the strict reading ("a rule changed
  after any seat has scored is not the claim's rule") can be judged too. The claim is met only if v2 is met; a v1
  result is reported, not substituted.
- Before data, the strongest v1 controls are re-scored under v2 and a fresh seat builds the named shape
  (embedded table + generator-grammar parser + source reachability); receipts land before wave 1 is created.

## Attempt 2 (L1 `MadoR25A2`, dispatched 05:26Z) — C1 counter v3, before any seat scored v2 and before any data seat

Attempt 1 (`MadoR25`) died with the orchestrator at 05:25:25Z after landing `04051723` and `7228299d`; its untracked
`w1-spec.json` was never dispatched and is deleted unread-as-evidence. No wave-1 seat exists. Re-checked by attempt 2:
`count-v2.py` keeps v2's bytes (sha256 `b251ddec…81a8`), and v3 replays v2's 37 case lines byte-identically for seed
`0123456789abcdef` (`diff` of the CASE lines, `evidence/c1-before-v2-41cc04c8.txt` vs `evidence/c1-before-v3-41cc04c8.txt`).

Why v3 (a design gap, not an observed score — no seat has scored v2): a tool holding an encoded cache of the snapshot's
lines, normalized (case, whitespace, comments), plus a parser for only the easy grammar (`bind[d] = MODS, KEY, [DESC,]
DISPATCHER, ARG`) could pass every v2 case: REWRITE's edits are easy-grammar lines, SYNTH uses only the generator's easy
grammar, and the cache supplies every real line that uses keycodes, mouse binds, `$(…)` args or flag combinations. v3
adds 4 **HARD** cases: whole synthetic trees whose fresh random lines use the hard grammar of legacy
`ConfigManager::handleBind` (v0.56.2 `efb50993` `src/config/legacy/ConfigManager.cpp:1481-1674`) — modifier aliases and
separators (`stringToModMask`, `KeybindManager.cpp:221-242`), empty mods, `code:NN` / bare-number keycodes, mouse binds
(dispatcher `mouse`, arg = the named action), every valid flag letter, dispatcher case (lowered), comma-bearing args
(`CVarList` last field), variables in mods/description/dispatcher/arg, trailing comments, and lines Hyprland rejects
(invalid flag, e/r/o conflicts, m with l/e/r, c with g, mod string with no modifier, unknown dispatcher, too few or too
many args, empty key, catchall outside a submap), plus unbinds with alias/keycode re-spellings and a case-mismatched key
(`removeKeybind` compares the key string exactly). v3 also checks its own line model against the live table before
scoring: `MODEL_CHECK modeled=190 drift=0` at base; drift exits 2.

**PRED-C1 (v3, the claim's rule)** — the same sentence as the v3 counter docstring and the receipt label `PRED-C1`:
At REV, the committed bytes of tools/mado-binds.py, run in a bubblewrap sandbox (no network, no /run, cleared
environment, HOME = a fresh case directory), reproduce the expected bind multiset exactly over all 18 hyprctl JSON
fields for the unperturbed snapshot of the four Hyprland config roots and for each of 40 counter-generated cases (4
each of ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT and REWRITE on that snapshot, 4 SYNTH whole synthetic
config trees, and 4 HARD whole synthetic trees whose lines exercise modifier aliases, keycodes, mouse binds, flag
combinations, dispatcher case, comma-bearing args, variables and rejected lines), and the tool bytes contain none of the
live capture's arg or description strings of 12 or more characters; target: cases_pass=41/41 and embed_hits=0.

- Counter v3: `python3 -I .ufo/waves/round-25/c1/count.py REV`, sha256:`8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.
- Before @ `41cc04c8` under v3: `MODEL_CHECK modeled=190 drift=0`, `PRED-C1 cases_pass=0/41 embed_hits=0
  verdict=TARGET_MISSED`, exit 1 (`evidence/c1-before-v3-41cc04c8.txt`, seed `0123456789abcdef`).
- Kill rule unchanged: one measurement run at the measured commit on a fresh seed, receipt committed; any result other
  than `TARGET_MET` is a miss, reported, never amended or re-scaled; an exit-2 run is re-run and both receipts kept.
  v1 and v2 are also run once each at the measured commit and reported, never substituted.
- Order from here: this commit → pre-data control call (fresh critic / mutation-tester seats: every committed v1
  control re-scored under v3, plus new shortcut shapes: normalized encoded cache + easy-grammar parser, counter-copy
  glue, permissive parser, partial-grammar mutants, no-source / no-variable / no-unbind readers) together with
  non-data repair and source-opening items → control receipts landed → wave 1 (data). If any control meets v3 before
  data, C1 is re-designed before data or the round reports it.

## Attempt 3 (L1 `MadoR25A3`, dispatched 06:40Z) — C1 counter v4 (Hyprland oracle), before any v4-scoring seat or data seat

Attempt 2 (`MadoR25A2`) died with the orchestrator at 06:19:06Z after landing `a258c6ae`. It left untracked scratch in
the lane (`w1-spec.json`, `w1-run.json`, `w1/`, `controls/v3/`): a pre-data control/audit wave whose seats are dead. That
scratch is not evidence: attempt 3 read only its spec item list and grep'd its verdict lines for orientation, cites none
of it, and deletes it in this commit's working copy (it was never tracked). No data seat exists in any attempt. No seat
has scored v4. Re-checked by attempt 3: `count-v3.py` (this commit) is byte-identical to the v3 `count.py` landed at
`a258c6ae` (sha256 `8532d3e9…8375`); `count-v1.py` and `count-v2.py` keep their pinned hashes.

Why v4 (a design gap, not an observed v4 score): v1–v3 take every generated case's expected table from the counter's own
line model. A tool that transcribes that model meets them by construction, whether or not the model is what Hyprland
does; the model was itself written this round, so the counter cannot tell a correct resolver from a faithful copy of a
wrong one. v4 keeps v3's case generator unchanged (imports `count-v3.py`, sha256-pinned, same rng stream, so a seed
replays v3's case trees) and takes every expected table from Hyprland v0.56.2 itself: a nested Hyprland instance started
by the counter on a copy of each case tree (exec keyword lines removed; non-bind `ecosystem` options appended so no
update/donation screen opens), read back with `hyprctl -i <instance> binds -j`, then killed with its process group. The
tool runs where that oracle cannot be reached (bubblewrap: no /run, no display socket, no network, cleared environment).
The unperturbed snapshot's oracle table must equal the live capture (`ORACLE_CHECK`), else exit 2.

**PRED-C1 (v4, the claim's rule)** — the same sentence as the v4 counter docstring and the receipt label `PRED-C1 (v4)`:
At REV, the committed bytes of tools/mado-binds.py, run in a bubblewrap sandbox (no network, no /run, cleared
environment, HOME = a fresh case directory), reproduce exactly over all 18 hyprctl JSON fields the bind multiset that
Hyprland v0.56.2 itself builds from the same case tree (a nested Hyprland instance run by the counter on a copy of the
tree with its exec lines removed, read with hyprctl binds -j), for the unperturbed snapshot of the four Hyprland config
roots and for each of the 40 cases v3 generates (4 each of ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT,
REWRITE, SYNTH and HARD), and the tool bytes contain none of the live capture's arg or description strings of 12 or more
characters; target: cases_pass=41/41 and embed_hits=0.

- Counter v4: `python3 -I .ufo/waves/round-25/c1/count.py REV`, sha256:`323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`;
  generator `c1/count-v3.py` sha256:`8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`. Exit 0 `TARGET_MET`,
  1 `TARGET_MISSED`, 2 setup / `UNSTABLE` / `ORACLE_DRIFT` / `ORACLE_FAIL`.
- Before @ `41cc04c8` under v4 (seed `0123456789abcdef`, `evidence/c1-before-v4-41cc04c8.txt`): `ORACLE_CHECK
  base_vs_live missing=0 extra=0` (192 live binds), `tool=MISSING_TOOL`, `PRED-C1 (v4) cases_pass=0/41 embed_hits=0
  verdict=TARGET_MISSED`, exit 1. Diagnostic: `V3_MODEL_AGREE 41/41` — v3's expectations equal Hyprland's tables on that
  seed; v4 changes where the truth comes from, not the cases.
- Claimed work (what a control must skip to be a control): resolve a config tree statically — follow `source =` with `~`
  and globs, expand variables, drop comments, apply the bind grammar of every line (including rejected lines) and
  `unbind` in order — in one stdlib python3 file that runs without the compositor. A tool that reuses v3's per-line
  functions (`line_entry`, `unbind_apply`, `varlist`, `parse_key`) still does that work and is judged against Hyprland's
  table, so it is an implementation path, not a control; the pre-data control wave builds only shapes that skip the
  work (do-nothing, `[]`, junk, server echo, nested-Hyprland shell-out, encoded embedded table + delta parser, grep of
  every bind line, easy-grammar-only parser, fixture/label-keyed detector, no-reader synthetic table). Feature-ablation
  mutants of the landed tool (no variables, no unbind, no comments, no aliases, permissive, all files instead of the
  source graph) are wave-2/residual mutation tests of the tool, after it exists.
- Kill rule (unchanged in substance): one measurement run of v4 at the measured commit on a fresh seed, receipt
  committed; any result other than `TARGET_MET` is a miss, reported, never amended, re-scaled or re-run until it
  passes; an exit-2 run is re-run and both receipts kept. v1, v2 and v3 are also run once each at the measured commit
  and reported, never substituted. If any pre-data control meets v4, C1 is re-designed before data or reported so.
- Oracle side effect (disclosed): each nested instance opens a window on the operator's live session for about one
  second; it runs with exec lines removed and a cleared environment, at most 6 at once host-wide (lock files under
  `/fast/scratch/hyaku/mado-r25-oracle-slots/`). No live-compositor write verb is used.
- Order from here: this commit → pre-data control wave `a3w1` (controls + counter/oracle attacks + non-data items) →
  control receipts landed → wave `a3w2` (data: the tool) → residual attack call on the landed tool → measurement.
  C2 stays exploratory as declared above. Routed repairs R3–R6 are done by the L1 (attempt 2's repair seats are dead and
  their tasks are not re-sent).

### Attempt 3 — after the control receipts (`459dd17f`), before any data seat

- Control receipts: 10 shapes under v4, none met (`controls/v4/*.md`; best K4LabelKeyed 37/41, K4EncodedTable 31/41,
  K4EasyOnly 4/41, the rest 0/41). Known weaknesses reported, not amended: the case directory name (`cases/<LABEL>/home`)
  is visible to a tool through `/proc/self/mountinfo`, so a tool can learn the case type (K4LabelKeyed); an encoded copy
  of the live table evades the plain-string embed check (K4EncodedTable, K4LabelKeyed). Neither meets the target: HARD
  trees fail every shortcut that does not parse the hard grammar. The oracle does not see binds an exec'd command would
  create at runtime (SentOracleBoundary); no generated case adds exec lines and ORACLE_CHECK equals the live table.
- Reading of a crash (RevCounterV4, minor defect, counter unchanged): a run whose output has no `PRED-C1 (v4)` line
  (an uncaught exception exits 1 with a traceback) measured nothing; it is classified with exit-2 runs (re-run once,
  both receipts kept), never as `TARGET_MISSED` or `TARGET_MET`.
