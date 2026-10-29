# Round 56 w2 — R56W2MutC2ToolA: mutation test of `tools/mado-watchplan.py`

Revision attacked: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (tool blob sha256 `ed6ee9f200cdc0646fb2f31898f37a2570318a7609d91c7cd730c501c1aa9379`).
Contract: registration-v2 §C2 and claims-frozen-v2 PRED-C2-r56-v2, read first; registration.md where v2 is silent. Nothing in the lane was edited; all lane reads were `git archive`, `git show`, `git ls-tree`, `git cat-file` and filesystem reads.

Full write-up, mutant table and killing-fixture table: `.ufo/waves/round-56/w2/R56W2MutC2ToolA/mutants.md`.

## 1. What I attacked

Item: the C2 tool's config model — comment/brace stack, `=` split and comment cut, the `$`/`{`/backslash/`##` unsupported rules, value parsing (`configStringToInt` model), depth cap and size bounds, `source` handling, watch-list construction, `--display-root`, the `--getoption` join, and the header and DONE counters — against the committed oracle. The oracle is the unchanged `quality/check-r56-controls.py --claim c2` (18 committed + 8 hold-out fixtures) plus the tool's own `--selftest`.

Question from the seat spec: wave-1 seats wrote each artifact once and kept their own selftests as the only kill evidence. Does the committed oracle actually detect mutations of the model?

## 2. Result

| measure | count |
|---|---|
| one-line mutants generated and run (none skipped) | 105 |
| killed by the frozen claim predicate (`TARGET_MET` not printed) | 62 (59.0%) |
| killed by the full oracle (claim predicate + `--selftest`) | 77 (73.3%) |
| provably equivalent (no observable behaviour change) | 9 |
| claim survivors that are not equivalent | **34** |
| full-oracle survivors that are not equivalent (no lane test catches them) | **19** |

Equivalent-adjusted kill rate: 64.6% (claim predicate), 80.2% (full oracle).

The attack lands. The frozen predicate `TARGET_MET` is satisfied by 34 mutants that break a normative rule of registration-v2 §C2. Of those, 19 also pass the tool's own `--selftest`. Every one of the 34 has a killing fixture, verified through the harness's staged bwrap layout (section 4).

## 3. What I did (commands and decisive output)

Scratch: `/fast/scratch/hyaku/mado-r56/R56W2MutC2ToolA/` (removed before yield; every deliverable was copied first).

1. Fresh repo from the lane archive, toplevel asserted before commit:
   `git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive --format=tar 28fc86ac… | tar -x -C …/repo`; `git -C …/repo rev-parse --show-toplevel` = `…/repo`; commit `d997f00` (`-c user.name=ctl -c user.email=ctl@ctl`).
2. Baseline, unchanged oracle:
   `python3 -I quality/check-r56-controls.py --claim c2 --repo …/repo --rev d997f00… --work …/work-base/w` →
   `MADO_R56_C2: rev=d997f00… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET` (exit 0).
   Tool `--selftest`: `MADO_WATCH_SELFTEST: 82/82 assertions passed`.
3. `mutate.py` (105 one-line mutants, one commit per mutant in the scratch repo, the lane never touched). Each mutant ran the unchanged claim harness and `--selftest`. Excerpt from `receipts/run.log`:
   - `M16 stack SURVIVED  MADO_R56_C2: … fixtures=18/18 holdout=8/8 … verdict=TARGET_MET`
   - `M27 unsupported SURVIVED … verdict=TARGET_MET`
   - `M44 source SURVIVED … verdict=TARGET_MET`
   - `M50 watch SURVIVED … verdict=TARGET_MET`
   - `M86 source KILLED … fixtures=16/18 holdout=7/8 … verdict=TARGET_MISSED`
   - `M01 args KILLED … fixtures=1/18 … TARGET_MISSED`
   - Restoration: `cmp` of the scratch tool against `git show HEAD:tools/mado-watchplan.py` after the run: identical.
4. `kill4.py` (each proposed killing fixture against its own mutant, staged bwrap run, both outputs saved in `receipts/kill-<K>.txt`) and `cross.py` (every fixture against every claim survivor, one stage per fixture shared by pristine and mutant, so raw stage paths match).
5. `equiv.py` (in-process differential over a 3,851-case corpus) for the nine survivors that no fixture kills: zero differences for M73, M77, M78, M79, M81, M83, M85, M99, M104. M80 and M96 were in that run and are not equivalent (M80 distinguished in 66 cases; M96 killed by K57, which the corpus did not reach).
6. `report.py` generated `mutants.md` from the receipts; every number in the report is computed there.

Equivalence arguments (each in `mutants.md`): M73/M77 `len(stack) > 0` ≡ `stack`; M78/M79 on the OPTION branch no `#` or `$` can sit in lhs or the stack, so `##`/`$` in `line` ⇔ in `rhs`; M81 an lhs equal to `$` alone has key ≠ OPTION and is discarded either way; M83 an empty `matches` makes the dropped `return` a no-op; M85 `glob` never yields `""` and `VALUE` is absolute, so `absolute_path` is the identity; M99 `dict.get(k)` ≡ `dict.get(k, None)`; M104 `int(int)` is the identity.

## 4. Defects the committed oracle misses (each: mutant, input, pristine vs mutant, severity)

Severity: **blocking the claim** = the frozen predicate accepts a tool that breaks a normative registration-v2 §C2 rule and no lane test catches it. **weakens the claim** = the lane's own `--selftest` catches it, but the frozen predicate does not.

| mutant | normative rule broken (registration-v2 §C2) | killing input (verified) | pristine vs mutant | severity |
|---|---|---|---|---|
| M27, M80 | a value line holding `$` is `unsupported` | `misc:disable_autoreload = on$x` (K27) | `unsupported=1`, autoreload=on vs `unsupported=0`, autoreload=off | blocking |
| M28 | value line holding `{` is `unsupported` | `misc:disable_autoreload = on{` (K28) | unsupported vs accepted | blocking |
| M29 | value line holding a backslash is `unsupported` | `misc:disable_autoreload = off\` (K29) | unsupported vs accepted | blocking |
| M76 | RHS is stripped of WS only | `misc:disable_autoreload = 1!` (K76) | unsupported vs accepted | blocking |
| M16 | `#`-first lines are skipped | `# note {` then `misc:disable_autoreload = 1` (K16) | autoreload=off vs on | blocking |
| M17 | same rule (comment rule removed) | K16 / K17 | as above | blocking |
| M71 | only `#`-first lines are comments | `; note {` then the option (K71) | pristine: `;` line opens a category, option ignored (autoreload=on); mutant: `;` line skipped (autoreload=off) | blocking |
| M44 | an inaccessible match aborts the rest of that line's matches | `source = mix/*.conf` with a dangling `a-broken.conf` before `z.conf` (K44) | `paths=1` vs `paths=2` | blocking |
| M50, M89, M90 | a dangling `--config` is listed as `type=file` (lexists); canonical only on `realpath(strict)` | `--config` = dangling symlink (K50) | `type=file` vs `type=missing` | blocking |
| M56, M94, M96 | the display prefix is the given text minus its `/` or its realpath | link root with or without trailing `/` (K56, K94); symlink root with realpath (K57) | `$ROOT/…` vs absolute path | blocking |
| M63, M97 | `--getoption` must be a regular file, else `unreadable` | `--getoption /dev/null` (K63) | `SETUP unreadable` rc 2 vs rc 0 | blocking |
| M98 | the live value is the `int` key | `{"option":…,"value":1}` (K98) | UNKNOWN vs DIFFER/AGREE | blocking |
| M100 | a `--getoption` line that is not a JSON object is `bad_json` | first line `# comment` (K100) | `SETUP bad_json` vs OK | blocking |
| M101 | an integer `int` (any sign) records the live value | `"int": -1` (K101) | record vs UNKNOWN | blocking |
| M04, M06, M07, M11, M12 | args must be absolute; `too_large` above 1048576 bytes exactly | relative `--config` (K04); 1048576 vs 1048577 byte files (K06, K07, K11, K12) | the boundary cases | weakens (selftest catches) |
| M18 | a stray `}` on an empty stack is ignored | `}` then the option (K18) | rc 0 vs crash | weakens (selftest catches) |
| M26, M33 | RHS cut at `#` and stripped; a value that starts with digits is not an int | `1 # x` (K26): pristine 1, mutant unsupported; `1abc` (K33): pristine unsupported, mutant accepts and prints `disable_autoreload=1abc` | as stated | weakens (selftest catches) |
| M54, M93 | a directory watch carries the directory mask | `--config` = directory (K54, K93) | mask | weakens (selftest catches) |
| M55 | `--display-root` is a path prefix | `…/sub` root over `…/sub2/…` (K55) | `$ROOT` vs raw path | weakens (selftest catches) |
| M57 | the realpath is the root alternative | K57 | `$ROOT` vs raw | weakens (selftest catches) |
| M60, M62 | a bool `int` is ignored; a missing record is UNKNOWN | `"int": false` (K60, corrected, see below); no record (K62) | UNKNOWN vs AGREE; `live=?` vs `live=0` | weakens (selftest catches) |

The 19 full-oracle survivors (undetected by the lane) are M16, M17, M27, M28, M29, M44, M50, M56, M63, M71, M76, M80, M89, M90, M94, M97, M98, M100, M101.

Proposed additions: a greedy cover of the 34 real claim survivors needs **28** fixtures (not proven minimum); the list is in `mutants.md`. Examples: K50 (kills M50, M89, M90), K27 (kills M27, M80), K57 (kills M57, M96), K63 (kills M63, M97), K16 (kills M16, M17). Each proposal was verified to separate its mutant from the pristine tool through the staged run; the pristine output is the expected output for each. Adding any of them changes the harness's fixed counts (18 to 19, etc.), so they are a pre-data re-registration under a new versioned file, not an edit of the committed set.

Errors in my own first pass, disclosed: K60 was first written with a typo (`misc:disable_autoridl`) and was corrected and re-verified. K80 and K96 were mis-targeted (their true killers are K27 and K57, both confirmed by the cross matrix). Their NO-KILL rows are kept in the receipts.

## 5. Claim-level verdict

PRED-C2-r56-v2 is not falsified as written: the pristine tool at `28fc86ac` passes it. It is weakened as evidence of operability. The committed oracle does not pin the tool's model. The proposed fixtures are the smallest set I found that does; adding them is a re-registration decision, not a silent change.

## 6. Tooling

No tools were installed or updated. `python3` 3.14, `git`, `tar` and `bwrap` were already present (bwrap was used only for the harness staging, read from `/usr/bin/bwrap`). No pacman, no `uv`, no `npm`, no `cargo`.

## 7. What I could not verify

- Whether registration-v2 §C2 itself matches Hyprland 0.56.2. I attacked the tool against the registration's text, not against the running compositor. The host reads were not part of this seat.
- The kill transcripts use a re-implementation of the harness's `staged_run` command line (same bwrap arguments); the verdicts for the 105 mutants come from the unchanged harness itself. The proposed fixtures were not run through the harness's `score()` because the harness's counts are fixed at 18/8.
- The equivalence corpus is finite; the nine equivalence claims rest on the arguments in `mutants.md` plus zero differences over 3,851 cases.
- The hold-out fixtures are revealed (not sealed), so a fixture I propose cannot be checked for hold-out status; overfitting to the revealed set is possible.
- I did not run the lane's own harness at any other revision, nor the wave-1 selftests.

## 8. Deliverables (lane-relative)

- `.ufo/waves/round-56/w2/R56W2MutC2ToolA/mutants.md` — the full report: mutant table (all 105), the 9 equivalents with arguments, the 34 real survivors with killing fixtures, the greedy cover, and the disclosures.
- Driver: `.ufo/waves/round-56/w2/R56W2MutC2ToolA/{mutate.py, kill2.py, kill4.py, extra.py, cross.py, equiv.py, report.py}`.
- Receipts: `.ufo/waves/round-56/w2/R56W2MutC2ToolA/receipts/` — `M01.txt`…`M105.txt` (one per mutant: sha256, blob, oracle line, selftest rc) and `kill-K##.txt` (44 transcripts, both outputs, verdict).
- Machine-readable: `…/R56W2MutC2ToolA/results.json`, `results.tsv`, `kill-results.json`, `cross/cross-matrix.json`, `equiv-results.json`, `baseline.txt`, `run.log`.
- Hygiene: the scratch directory is removed after the copy; nothing under the lane was written except `.ufo/waves/round-56/w2/R56W2MutC2ToolA/` and this report.
