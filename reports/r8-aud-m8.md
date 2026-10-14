# AUD-M8 — round-8 audit: the post-hardening sweep (M8-1), the snapshot-diff mode, zero config mutation

Lane AUD-M8, 2026-10-14. Write scope: **this file only** — no other file in
mado-shokunin was written by this lane (the round-8 lanes' modified/untracked
files are untouched by me; `git status --porcelain` separate). Scratch
`/tmp/w8-audm8-gate/` (logs retained; the 20 `/tmp/w5-mado-m52-selftest.*` dirs
named by my own runs were removed by exact path, 187 foreign dirs left alone).
**Zero config mutation**: the combined config-plane hash (the gate's own
`boundary_hash` rule, `LC_ALL=C`) is `bb2639d9a98045d4…9862` before my first
run (19:14:25Z) and after my last (19:29Z), identical to the value every gate
run's own `boundary.readonly` row prints. No compositor/session state, no
launch, no socket.

**Audited revisions (in flight throughout).** The gate was being written by
round-8 lanes during the whole window; every number below is tied to a
measured sha, and anything after my close (≈19:30Z) is not covered (U1).

| artifact | sha256 (prefix) | measured at |
|---|---|---|
| `tools/mado-verify.sh` — revision M8-1's headline is tied to (HEAD blob, `0c20a76`) | `90d50cdd4d18410b…` · 1,755 L / 75,771 B · mtime 15:31:57 −03:00 | frozen copy 19:14Z |
| derived post-hardening revision — my own excision of the two `MADO-R7` blocks | `c4c1afb75dd1c8aa…a5171` · 1,186 L / 50,126 B | 19:15Z |
| recorded T6-1 defect spec (extracted by me from the harness's r7-1 leg heredoc) | `7b951171e9e5ab39…` · 2,142 B | 19:14Z |
| M8-1's re-cut spec (copied from the lane's scratch, sha re-verified) | `85d946d7905d8c92…6b01` · 3,166 B | 19:21Z |
| M8-1's landed note `corpus/knowledge/gate-mutation-sweep-r8.md` | 10,946 B · mtime 16:17 −03:00 | 19:22Z |
| in-flight gate revisions observed (mine + M8-4's poll; the list is incomplete — the file kept moving) | `05c52e14…` `60582907…` `e7834b54…` `6ea07110…` `cbadcbe4…` `1183c58e…` `da3a4c39…` `dc864c6a…` `f58632b9…` `07df6f81…` `7b9ad733…` `d1f947dc…` (1,760 → 2,835 L; suite red at each) | 19:15–19:27Z |
| settled green revision — frozen copy used for the C6 measurements | `38ed880fedfe457c…` · 2,837 L · `MADO_SELFTEST: 207/207` | 19:27:51Z |

## 1. Verdict table

| # | claim | scope / method (my own runs) | result | verdict |
|---|---|---|---|---|
| C1 | **M8-1 headline** — post-hardening sweep of `mado-verify.sh` @ `90d50cdd…` kills **10/10** (`gate-mutation-sweep-r8.md` §1) | independent re-run: tameshi harness `cf41efaa…` against **my frozen copy** of `90d50cdd…` with M8-1's re-cut spec `85d946d7…` (`/tmp/w8-audm8-gate/sweep-recut-audit`) | `MUTATE: DONE … killed=10 survived=0 inconclusive=0 kill-rate=100%`, rc 0, 15.8 s; `CONTROL: GREEN` (89/89); `MUTATE_RESTORE: OK` (before = after = `90d50cdd…`); all ten `DEFECT …: KILLED` | **PASS (reproduced independently)** |
| C2 | **The recorded spec is refused verbatim on the live bytes** — 9 non-unique anchors (M8-1 §3) | my own sweep of `90d50cdd…` with the recorded spec `7b951171…` | `APPLY FAIL`: D1 2 · D2 2 · D3 2 · D5 **15** · D6 2 · D7 2 · D8 2 · D9 2 · R1 2 (D4 count 1); `MUTATE: SETUP`, rc 2, no suite run | **PASS (reproduced)** |
| C3 | **The recorded post-hardening revision still kills 10/10 with the recorded spec** (the round-6 hardening target, source of the 10/10 expectation) | my own excision (`sed` on the two marked blocks) → `c4c1afb7…` = `git show c8f6667:tools/mado-verify.sh` byte-identical; sweep with `7b951171…` | `killed=10 survived=0 inconclusive=0 kill-rate=100%`, rc 0, 12.7 s; `CONTROL: GREEN` (53/53); `MUTATE_RESTORE: OK` | **PASS** |
| C4 | **The gate's own recorded-table replay** (`--regression`) reproduces the table at the live revision | `bash tools/mado-verify.sh --regression` (repo path, 19:16:01Z and 19:21Z) | `REGRESSION_TARGET … sha256=95d4b5a6…` (later `d2bcdb31…`) vs recorded `c4c1afb7…`; `MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks…)` rc 2 | **FAIL — open, in-flight** (round-8 edits sit outside the marked blocks; the mode's own `REGRESSION_RECUT` hint is the remedy) |
| C5 | **The gate's suite is green at the live revision** | `--selftest` on my frozen copies | `e7834b54…` (1,760 L): `FAILED — 88 passed, 1 failed` (R10 derived target `e2df0e2f…` ≠ pin); `dc864c6a…` (2,186 L): `FAILED — 147 passed, 1 failed` (R10, derived `d2bcdb31…`) — both rc 2 | **FAIL — in-flight** (a lane's mid-edit state; the R10 case is the pin-re-cut alarm doing its job) |
| C6 | **M8-3's snapshot-diff mode + its selftest** (dispatch: "two invocations' verdicts diffed, what-classes-changed") | absent at every revision through 19:22Z (0 `snapshot` hits, five-flag usage); landed 19:25:01Z; measured on my frozen copy of the settled revision `38ed880f…` (2,837 L): its `--selftest`, `--snapshot FILE --no-live` twice, `--snapshot-diff`, and a diff against a doctored root | `MADO_SELFTEST: 207/207 assertions passed` rc 0; `MADO_SNAPSHOT: WRITTEN … (rows=31 pass=20 fail=0 unknown=0 skip=8 note=3; scope=file-plane)` rc 0; same-root pair → `MADO_DIFF: SAME (rows 31→31; every class 0)` rc 0; doctored root (one `source` line removed) → `MADO_VERIFY: DIVERGED (2 fail…)` rc 1 and `MADO_DIFF: CHANGED (regressed=2 relabeled=4 detail-changed=9 scope=1)` rc 1 | **PASS (landed mid-window; measured green)** — recorded alongside: a mid-edit revision (`07df6f81…`, 2,724 L) refused a snapshot write (`MADO_SNAPSHOT: REFUSED (write verification failed: 0 row lines on disk vs 31 expected)`) while its suite read 111/37 red; both are the in-flight state, superseded by `38ed880f…` |
| C7 | **Zero config mutation** | my own `boundary_hash`-rule hash (`LC_ALL=C`) before/after every run; every gate run's own boundary row | `bb2639d9a98045d4…` at 19:14:25Z = 19:29Z; `boundary.readonly PASS` with the same prefix in every `--no-live` run (round-7 revision and `dc864c6a…`) | **PASS** |

Aggregate: **the M8-1 claim holds and reproduces independently — the gate kills
10/10 at the revision the claim names, with a re-cut spec whose ten mutants I
re-ran myself; and it kills 10/10 at the recorded post-hardening revision with
the recorded spec, via an excision I re-derived myself.** What was *red*
throughout my window is the gate's own internal state, not its kill power: the
moving revisions kept the pin self-checks red (`--regression` SETUP, `R10`,
and twice a partly-built suite), the pin-re-cut alarm doing its job, and the
owner's own remedy (`REGRESSION_RECUT`) is printed. The snapshot-diff mode
(M8-3) landed mid-window and measures green end-to-end at its settled revision
(C6).

## 2. Re-run detail (commands and receipts)

- **My own excision (independent of the gate's helper):**
  `sed -e '/…MADO-R7-REGRESSION-BLOCK >>>/,/…<<<…/d' -e '/…MADO-R7-SELFTEST-BLOCK >>>…/,/…<<<…/d'`
  on the `90d50cdd…` bytes → `c4c1afb75dd1c8aa…a5171`, 1,186 L; `diff` vs
  `git show c8f6667:tools/mado-verify.sh` → empty.
- **Recorded-spec sweep (C3):** `mutate-and-run.sh --target derived-c4c1afb7.sh
  --defects mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest'`
  → ten `KILLED`, `CONTROL: GREEN (exit=0 … pristine-sha256=c4c1afb7…)`,
  evidence `/tmp/w8-audm8-gate/sweep-c4c1afb7/` (per-defect `results.tsv`).
- **Re-cut-spec sweep (C1):** spec bytes copied from `/tmp/w8-mado-m8-1/spec/`
  and re-hashed (`85d946d7…` matches the note's §0); run against my frozen
  `90d50cdd…` copy; ten `KILLED`; evidence
  `/tmp/w8-audm8-gate/sweep-recut-audit/results.tsv` (mutant shas per defect,
  e.g. D2 `109e5a32…`, D9 `01e8e466…`).
- **Mutant semantics (spot, my diffs):** D2 at `:1743` drops `&& [ "$UNKNOWN" = 0 ]`;
  D6 at `:1179` drops `xdph` from `LOCAL=`; D9 at `:1395` turns
  `[ "$after" = "$before" ]` into `[ -n "$after" ]` — single-site semantic
  edits at the intended live lines, as the note claims.
- **The live revision is not sweepable with the recorded spec** (C2): the
  round-7 block embeds the spec text in the gate's own heredoc, so nine anchors
  occur twice; `  return 2` occurs 15 times. This is per-revision, not a lane
  error — the re-cut (or the excision route) is the only sweep path.
- **In-flight corroboration:** M8-1's I1 (`MUTATE_RESTORE: DRIFT` at 19:15:38Z)
  matches my own observations — the gate moved 9 times inside my window
  (`90d50cdd` → … → `f58632b9`, 1,755 → 2,194 L) and M8-4's poll logged
  `GATE-MOVED sha=05c52e14…` at 19:15:47Z.
- **Snapshot-diff mode (C6), measured on my frozen copy of `38ed880f…`:**
  `--snapshot FILE --no-live` → `MADO_SNAPSHOT: WRITTEN /tmp/w8-audm8-gate/snap-a.json
  (rows=31 pass=20 fail=0 unknown=0 skip=8 note=3; scope=file-plane)` rc 0;
  the same-root pair → `MADO_DIFF: SAME (rows 31→31; every class 0)` rc 0; a
  doctored root (`/tmp/w8-audm8-gate/root-mut/`, one `source` line removed from
  `hyprland.conf`, 17 → 16) → `MADO_VERIFY: DIVERGED (2 fail, 0 unknown, 14 pass)`
  rc 1 and `MADO_DIFF: CHANGED (regressed=2 recovered=0 flipped=0 relaxed=0
  relabeled=4 appeared=0 vanished=0; detail-changed=9; scope=1)` rc 1. The mode
  wrote only the three snapshot files I named; the substrate was untouched.

## 3. Spot-checks (three, all re-run 2026-10-14)

1. **Pin/excision.** My `sed` excision of the two marked blocks from the
   HEAD-blob gate yields exactly `c4c1afb75dd1c8aa…a5171`, 1,186 L, and
   byte-identical to the committed round-6 blob (empty `diff`). Run 19:15Z;
   file `/tmp/w8-audm8-gate/derived-c4c1afb7.sh`.
2. **Re-run of the claim.** M8-1's re-cut spec (`85d946d7…`) against my frozen
   copy of `90d50cdd…` → `killed=10 survived=0 inconclusive=0 kill-rate=100%`,
   rc 0, `CONTROL: GREEN`, `MUTATE_RESTORE: OK`; results.tsv kept at
   `/tmp/w8-audm8-gate/sweep-recut-audit/results.tsv`. Log
   `sweep-recut-audit.log`.
3. **Zero mutation + counts.** Config-plane hash `bb2639d9a98045d4…` unchanged
   across all runs and equal to the gate's own `boundary.readonly` row value;
   `--no-live` on my copies → `CLEAN (17 pass, 2 notes)` rc 0 at both
   `90d50cdd…` and `dc864c6a…`. (Ambient-locale variant of the same hash is
   `579d2eda…` — the ordering is locale-sensitive and the gate exports
   `LC_ALL=C`; recorded so nobody re-derives a different constant.)

## 4. Unknowns

- **U1 — in-flight revisions.** Everything after my close (≈19:30Z) is
  uncovered: the gate may have landed further edits, a pin re-cut, or the
  snapshot-diff mode.
- **U2 — the snapshot-diff mode's long-run semantics.** Landed and measured
  green (C6) on two same-root snapshots and one doctored-root pair — all taken
  seconds apart. The mode's stated purpose (verdicts across a day) is
  unmeasured: no time-spanning pair exists, and the class vocabulary beyond my
  two pairs is sampled, not exhaustively probed. `--selftest` counts to compare
  against: 89 (round-7 revision) → 207 (settled round-8 revision).
- **U3 — whether the owner re-cuts the pin this round.** The R10 selftest case
  is red and `--regression` refuses at my close; whether that is fixed before
  round close is unknown (the mode prints the re-cut command).
- **U4 — re-cut anchor equivalence.** Nine of the re-cut's anchors are widened
  by adjacent lines, so its mutant bytes differ from the recorded spec's;
  equivalence is argued per defect from the live-site diffs (I spot-checked
  three) — not proven by byte identity (M8-1's U2 carried).
- **U5 — single host / toolchain** (the ledger's U1 shape): bash 5.3.15,
  one measurement window, 2026-10-14.
- **U6 — sweep coverage at the widened revision.** Whatever round 8 lands
  (drift arm, snapshot-diff, live-body exercise) needs its own re-cut and
  sweep; nothing here measures that revision.