# R56CritDoNothing — round 56, wave w1 (critic: do-nothing / skip-the-work controls)

Scope: for C1, C2, C3 build the cheapest control that skips the claimed work, score it with the registered
contract (checkers written from `registration.md` text only), and report every control that meets the target.
Leaf seat, no subagents, no lane edits, no git mutation of lane or fleet, no host writes, no tool installs.

## 0. Result

| claim | control (skips the work) | measured | meets target? | implication |
|---|---|---|---|---|
| C1 | junk entry: frozen quotes, template propositions satisfying tok/num, fabricated registry rows S383-S390, README row | `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` | **YES** | counter/target is wrong for "sourced entry" coverage; see §3 C1.3 |
| C1 | same entry, no fabricated registry rows | `sources=0/30 scope=0/30 new_rows=0/8` | no | registry legs do bind |
| C1 | contract control 2 (placeholder propositions) | `content=1/33`; tok fails on 32 rows | no | matches the contract's expectation |
| C2 | reference tool with `source =` ignored (main file only) | 8/18 committed | no | |
| C2 | reference tool with symlink canonical watch dropped | 16/18 | no | |
| C2 | reference tool ignoring `misc:disable_autoreload` | 14/18 | no | |
| C2 | empty program / `ctl/const-host.py` | 0/18 / 1/18 | no | agrees with contract |
| C2 | shape replay: keyed on (args with fixture root → `{FX}`, tree file listing + content); committed table only | 18/18 committed | **YES on committed; hold-out unscored (sealed)** | the committed half is memorisable; only the sealed 8/8 separates it (§3 C2.3) |
| C3 | fill-all: every used-by cell lists every entry (contract control 2) | `missing=0 extra=21949` | no | |
| C3 | append a comment line after every registry row | `missing=65 extra=0 dangling=0` | no | |
| C3 | append an HTML comment (no path) to every used-by cell | `missing=65` | no | |
| C3 | delete the 65 citation tokens that `missing` counts, from the entries; used-by untouched | `missing=0 extra=0 dangling=0 TARGET_MET` | **YES** | counter/target wrong; leg needed (§3 C3.3) |
| C3 | delete all 381 citation pairs from the entries and clear every used-by cell | `missing=0 extra=0 dangling=0 TARGET_MET` | **YES** | counter/target wrong; same leg |

Every control that meets its target is a defect in the counter or the target. Legs to add are in §4; each needs a new
frozen predicate, none is an edit.

## 1. Setup and provenance

- Lane freeze commit `3423ae285676c2a10273000f4519163472b443db`; base `13f0acbe3a15da2d9c08357a576d91dcadc85273`.
- Scratch: `/fast/scratch/hyaku/mado-r56/R56CritDoNothing/`. One `git archive 3423ae28 | tar -x` into a fresh `git init` repo (`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D`; commits with `-c user.name=ctl -c user.email=ctl@ctl`). Each variant was a separate fresh repo, deleted after scoring. The whole scratch tree was removed before yield (`rm -rf`; checked).
- Lane reads only: `git -C <lane> show`, `ls-tree`, `archive` (read-only). Nothing written under the lane except this report and the deliverable dir.
- Sealed hold-out: **not opened, not looked for**. No `fixtures/c2-holdout` path was touched.
- Host: not read (no control needs it). No `hyprctl`, no `~/.config` or `~/.local` access.
- Tools installed: none (no pacman, uv, npm or cargo action).
- Deliverables: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56CritDoNothing/`
  - `c1_check.py`: C1 counter written from `registration.md` §C1 (legs: tables_sha, prov, index, row, quote, pin_hash, host, source_cell, scope, tok, num, new_rows, entry_absent).
  - `c3_check.py`: C3 counter from §C3. Reproduces the frozen baseline exactly: `entries=70 rows=319 missing=65 extra=0 dangling=0`.
  - `c2_ref.py`: C2 reference tool from §C2, with `--ablate source|symlink|disable` (critic-only switch; the registered tool has none). Passes all 18 committed fixtures byte for byte and exit status.
  - `c2_replay.py`: shape-replay control (§3 C2.3). `c2_harness.py`: scores any tool over the 18 committed fixtures under the registration's byte/rc rule.
  - `mk_variants.py`: builds the C1 and C3 variants in scratch repos and runs the checkers on them.
  - `run-all.sh`: the whole run, in order. `receipts/critic-run.txt`: its full output. `receipts/variants-run.txt`: variant lines.
  - `receipts/artifacts/c1-junk-full/`: the junk entry, README and SOURCES.md as scored. `receipts/artifacts/c3-*`: the C3 variant corpora.

## 2. Exact commands and decisive output

Full output: `receipts/critic-run.txt`. (The `rc=0` after the C1 baseline line in that file is the exit status of `cut`, not of the checker; the checker printed `TARGET_MISSED` and exits 1.)

```
$ python3 -I c3_check.py --repo $D --rev HEAD --work $S/w3
MADO_USED_BY: rev=HEAD entries=70 rows=319 missing=65 extra=0 dangling=0 verdict=TARGET_MISSED missed=missing     (rc=1)
$ python3 -I c1_check.py --repo $D --rev HEAD --work $S/w1base
MADO_AUTORELOAD_ENTRY: rev=HEAD rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8 verdict=TARGET_MISSED missed=index,entry_absent,...
$ python3 -I c2_harness.py --base $D --tool c2_ref.py                  -> CRITIC_C2: ablate=none fixtures=18/18 target=MET
$ ... --ablate source   -> fixtures=8/18  target=MISSED
$ ... --ablate symlink  -> fixtures=16/18 target=MISSED   (F05, F06 mismatch)
$ ... --ablate disable  -> fixtures=14/18 target=MISSED   (F07, F08, F09, F11 mismatch)
$ c2_harness.py --tool ctl/empty.py -> 0/18 ;  ctl/const-host.py -> 1/18 ;  ctl/lookup-committed.py -> 18/18 MET
$ c2_harness.py --tool c2_replay.py -> fixtures=18/18 target=MET
$ KEEP=1 python3 -I mk_variants.py ...
c1-junk-full:               rc=0 ... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
c1-junk-no-registry:        rc=1 ... sources=0/30 scope=0/30 content=33/33 new_rows=0/8 verdict=TARGET_MISSED
c1-placeholder-full:        rc=1 ... content=1/33 ... verdict=TARGET_MISSED
c3-fill-all:                rc=1 ... missing=0 extra=21949 ... verdict=TARGET_MISSED missed=extra
c3-comment-line-per-row:    rc=1 ... missing=65 extra=0 dangling=0 ... missed=missing
c3-comment-in-cell-per-row: rc=1 ... missing=65 extra=0 dangling=0 ... missed=missing
c3-delete-missing-cites:    rc=0 ... missing=0 extra=0 dangling=0 verdict=TARGET_MET missed=none
c3-strip-all-citations:     rc=0 ... missing=0 extra=0 dangling=0 verdict=TARGET_MET missed=none
```

The first C1 variant run (before the fix described in §3 C1.1) reported `content=31/33 … missed=num:K29,num:K30`. The cause was my own template: the pin name `man7-inotify.7.html` contains a digit run `7` after a dot, which `num` correctly rejects. I changed the template to avoid the pin name; the reported result above is from the corrected template. Both runs are the same control otherwise.

## 3. Per-claim findings

### C1 — coverage (junk entry)

**C1.1 The control.** `c1-junk-full` (artifact `receipts/artifacts/c1-junk-full/`):
- Entry `corpus/knowledge/hyprland-config-autoreload-r56.md`: line 3 `source: S383 … S390`, `verified-at: 2026-10-28`, `recheck: 90d`; a table with exactly the 33 rows, each carrying the frozen id, the frozen source id (or `host`), the frozen `pin:line`, and the frozen quote verbatim in single backticks.
- Each proposition is a template filled from frozen fields, e.g. `K01 pins line 492 of the pinned source and says that misc is part of the config reload path.` It contains the row id, the frozen line, and the first identifier of the frozen quote (so `tok` holds), and no digits except the row's own line (so `num` holds). H rows are analogous.
- `corpus/SOURCES.md`: eight fabricated registry rows S383-S390, 11 cells each, `mined`, tier A, `opened 2026-10-28`, URL = the upstream URL for the pin at `efb50993…` (man7 for S390) ending in the pin suffix, `used-by` = the entry path, anchor = the min..max line span of that pin's frozen K rows (e.g. `ConfigWatcher.cpp:33-105`).
- `corpus/README.md`: one index line starting `` | `knowledge/hyprland-config-autoreload-r56.md` ``.
- Nothing is fetched, read, or checked against the source. Only the frozen quotes, frozen line numbers and frozen sids are used.

**C1.2 Why it passes.** Every leg in §C1 of the registration is a string, digit or hash test. The propositions are a template filled with frozen fields; the registry rows are written by the same author. All 13 leg kinds hold, and the verdict is TARGET_MET. The counter does not prove entailment, and the registration says so (declared limit). That limit is exactly why this control meets the target: the claim is "sourced entry", and a junk entry passes every mechanical test in the contract.

**C1.3 Verdict.** Counter/target defect. Two legs that would have failed this control are not in the contract:
1. **Entailment leg (new frozen predicate).** A sealed table `reviews.json` (written and sha-pinned before the wave) holding, for each of the 33 rows, a non-author verdict `entails` / `does-not-entail` bound to `sha256(proposition)`; the counter requires 33/33 `entails` and that every proposition sha matches. A forged proposition changes its sha and fails. This turns the declared limit into a leg instead of a note.
2. **Template-uniqueness tripwire (cheap, gameable).** After removing the row id, digits, the pin name and the quote identifiers, the residual text of the propositions must be pairwise distinct. The junk fails it (the 30 K residuals are identical). A generator that varies wording defeats it, so it is a tripwire, not a proof.
Without leg 1, the target should be restated as structural coverage (ids, quotes, pins, registry binding), not as "sourced entry".

### C2 — operability (tool that predicts the watch list)

**C2.1 Reference.** `c2_ref.py` was written from `registration.md` §C2 alone (argument grammar, setup reasons, the model, source handling with `absolutePath`, glob semantics, the watch list rules, output lines). It reproduces all 18 committed fixtures byte for byte and exit status. So the registration and the committed fixtures agree on every fixture I could check; no disagreement was found. The lane has no `tools/mado-watchplan.py` at the freeze commit, so this is a critic model, not the lane tool.

**C2.2 Ablations (skip one of the named mechanisms).** Each fails committed fixtures, so none meets the target:
- `source` ignored (main file only): 8/18. Fails F02, F03, F04, F05, F06, F07, F08, F10, F15, F16 (every fixture where a `source` line produces a watch).
- Symlink canonical watch dropped: 16/18. Fails F05, F06.
- `misc:disable_autoreload` ignored: 14/18. Fails F07, F08, F09, F11.
The contract's own stubs score as the registration says (`empty` 0/18, `const-host` 1/18, `lookup-committed` 18/18).

**C2.3 Shape replay (memorisation).** `c2_replay.py` builds a key from the arguments (fixture root replaced by `{FX}`) and the tree (relative file listing with content sha256 and symlink targets). On a match it replays the committed `expected.out`/`expected.rc`; otherwise it prints nothing. It scores **18/18 committed**. Any control that replays committed fixtures meets the committed half of C2 by construction, so that leg cannot distinguish capability from memorisation. Only the sealed 8/8 hold-out separates them. I did not open the hold-out, so I cannot state the hold-out score for the replay or for `lookup-committed`; the contract's own claim is 0/8 for `lookup-committed`. Whether a shape replay reaches a hold-out fixture depends on whether that fixture's arguments and file listing coincide with a committed one, which only the L1 can check at reveal.
- Leg to add (frozen, checked at reveal): **hold-out shape disjointness**: no hold-out (args after `{FX}` normalisation, tree relative-path listing) equals a committed one. Also state that the committed 18/18 cannot close the capability row alone (SCORECARD requires 8/8 hold-out).

### C3 — calibration (registry back-references)

**C3.1 Baseline reproduced.** `c3_check.py` on the freeze copy prints `entries=70 rows=319 missing=65 extra=0 dangling=0`, matching `frozen-tables.json` `c3.baseline` and the registration.

**C3.2 Controls that do not meet target (correct behaviour):** fill-all (`extra=21949`), an HTML comment line after each row (`missing=65`), an HTML comment with no path inside each used-by cell (`missing=65`). The counter is not fooled by comments or by over-filling.

**C3.3 Controls that meet target (defect).**
- *Delete the 65 missing citations*: remove, from the entries' non-fence lines, exactly the S-id tokens that `missing` counts (registry id cited, entry path not in its used-by). Used-by is untouched. Result `missing=0 extra=0 dangling=0` → TARGET_MET. Nothing in the counter or harness checks that entries still cite what they cited at base.
- *Strip all citations*: replace every S-id outside fences in all 70 entries (base: 381 registry-id citation pairs, computed with the same CITE rule) and clear every used-by cell → `missing=0 extra=0 dangling=0` → TARGET_MET. The target text says "used-by edits only (cell 11)", but no leg enforces it.
- Legs to add (new frozen predicates):
  1. **Cite floor**: every (S, entry) pair in CITE at `c3.base_rev` for an entry that exists at rev must still be in CITE at rev (no citation removed). Base count: 381 pairs.
  2. **Registry scope**: `corpus/SOURCES.md` at rev equals base in every cell except cell 11, checked against `c3.base_rev`.

## 4. Legs that must be added (summary; new frozen predicates, none an edit)

| claim | control that passes | leg to add |
|---|---|---|
| C1 | junk entry; all legs hold | `review:<id>`: sealed non-author entailment verdict bound to sha256(proposition) for all 33 rows; plus a template-uniqueness tripwire; or restate the claim as structural coverage |
| C2 | shape replay 18/18 committed | hold-out shape-disjointness at reveal; committed 18/18 may not close the capability row alone |
| C3 | delete 65 citations; strip all 381 | cite floor vs `c3.base_rev`; registry-scope check (only cell 11 may differ from base) |

## 5. Defects and ambiguities found while building the checkers

1. **C1 `entry_absent` output.** The registration says entry-dependent legs are "not evaluated; rows/hosts/sources/scope/content print 0". My output also lists them in `missed=` (`row:K01 … source_cell:K01 …`). Verdict and counts are unchanged; the `missed=` field differs from a literal reading. (Input: `c1_check.py` on the freeze copy, no entry.)
2. **C1 `tables_sha` as a leg vs setup.** The registration lists `tables_sha` as a leg but also says the counter embeds the constant. I treat a mismatch as a missed leg and continue; a setup exit (2) is the other reading. Not exercised.
3. **C1 `scope` locator grammar.** "comma-separated list of N or N-M locators" does not say whether spaces may follow the comma. I allow optional spaces. Not exercised by any control here.
4. **C1 `prov` multiplicity.** "a line starting `source:`" is singular, while the leg then says "`source:` line(s)". I allow one or more `source:` lines in the first 30 and require exactly one `verified-at` and one `recheck`.
5. **C1 candidate row detection.** A row is "a line whose first cell is an id K01..K30 or H01..H03", but a malformed id such as `K31` or `|K01|` is neither a row nor an error under that wording. I treat any line whose first cell matches `[KH][0-9]{2}` as a candidate: `K31` is ignored; a malformed `K01` line is `row:K01`.
6. **C1 `new_rows` vs `source_cell`.** `new_rows` requires that the S383..S390 rows "each satisfy `source_cell`", whose last clause compares the S-id to the frozen sid of a K row. I checked that every one of S383..S390 is the frozen sid of at least one K row (K29/K30 for S390), so both readings coincide for this freeze; I implemented the registry-row checks and the K-row equality is implied.
7. **C3 target vs legs.** The target says "used-by edits only (cell 11)", but no leg enforces it (§3 C3.3). This is a target/leg mismatch, not an ambiguity.
8. **C3 `dangling` scope.** Only the first 15 lines of an entry count as `source:` lines. A `source:` line at line 16 is not dangling-checked. The registration states this, so it is not a defect, but it is a place a citation escapes the counter. Not exercised by any control here.
9. **C2 reference agreement.** No disagreement between the registration text and the 18 committed fixtures was found (the reference matches all 18). The only divergences are those the registration already lists (§C2 declared divergences).

## 6. What I could not verify

- The hold-out `fixtures/c2-holdout` (sealed; not opened). The C2 replay and `lookup-committed` hold-out scores are therefore **not measured**.
- The lane's own counters and harnesses (`quality/counters/c1-r56-autoreload-entry.py`, `quality/counters/c3-r56-used-by.py`, `quality/check-r56-controls.py`, `tools/mado-watchplan.py`) do not exist at the freeze commit and were not run. My checkers are written from the contract text and may differ from the wave's counters. The junk and variant verdicts apply to my checkers; the wave's counter should be run on `receipts/artifacts/` to confirm the same verdicts.
- Entailment of any proposition: not checked by anything in this seat (the contract declares it out of counter scope).
- Live host behaviour (Hyprland 0.56.2 inotify, `misc:disable_autoreload` value): not observed, not needed for any control.
- Symlink preservation in `git archive | tar -x`: assumed. The committed symlink fixtures F05/F06 score as the registration says, so the export behaved.
- Timing: the full `run-all.sh` took about 74 s wall (including the variant runs in that pass); an earlier pass of the same variants took about 209 s. No timing claim is made beyond that.
