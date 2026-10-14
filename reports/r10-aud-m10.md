# AUD-M10 — round-10 audit: the arc synthesis (4 claims re-derived) and the standing-use note's 2 commands

Lane AUD-M10, 2026-10-14 (window 20:54–21:02Z, local 17:54–18:02 −03:00),
single host, bash 5.3.15. Write scope: **this file only** — no audited file was
edited; the round-10 artifacts, the gate and the sibling harness were read or
executed from frozen copies under my scratch `/tmp/w10-aud-m10/`
(`gate-93e43f8f.sh`, `note-7f61d87d.md`, `hist/*.sh`, logs). Read-only
throughout: `sha256sum`/`wc`/`grep`/`sed`/`git show`; the gate's own modes; the
tameshi harness consumed read-only; no substrate file written; no
compositor/session mutation (no launcher, no socket connect, no
`omarchy theme set`, no restart); no `git status`/`fetch` on the omarchy
checkout; secrets shape-only. Every live number below comes from the gate's own
read verbs.

Objects audited, sha-pinned at my read (uncommitted worktree files; HEAD
`de22dfd`, tree otherwise clean at 17:54):

| object | sha256 / size | read |
|---|---|---|
| `corpus/knowledge/arc-synthesis.md` (self-label M10-1) | `a5b4833141461810…` · 387 L / 30,796 B | full text; byte-stable through my close |
| `corpus/knowledge/gate-standing-use.md` (M10-2 text) | `7f61d87d…` · 327 L / 21,004 B | full text 17:56 |
| the same file after lane M10-3's appended receipt | `aaa2e625253e881e…` · 361 L / 22,931 B | diff = one append-only block (+34 L); M10-2 text unchanged |
| `tools/mado-verify.sh` (landed revision) | `93e43f8fe8b9bdd4…` · 3,231 L / 150,103 B | == commit `de22dfd` blob, worktree clean |
| `tameshi-shokunin/tools/mutate-and-run.sh` (sibling, read-only) | moved 3× in my window: `cf41efaa…242c75` → `5807fd38…` (17:57) → `75ed934d…` (18:03) | provenance, not gated (F3) |

Tags: **[O]** measured by this lane; **[OBS-record]** cited from a round record;
**[I]** inference; **[U]** unknown.

## 1. Verdict table

| # | claim (source) | my re-derivation (method) | result | verdict |
|---|---|---|---|---|
| C1 | **Gate ladder + landed row** — synth §2.1 `:124-131`, §2.2 `:140-152` | `git show <c>:tools/mado-verify.sh` → sha/lines/bytes for all five revisions; each blob's own `--selftest` re-run; the landed revision's whole row re-run on my frozen copy | 5/5 rows byte-exact: `d7edaab4…` 1,098 L / 45,334 B / **28/28** · `c4c1afb7…` 1,186 / 50,126 / **53/53** · `90d50cdd…` 1,755 / 75,771 / **89/89** · `7da4ec50…` 2,887 / 131,612 / **217/217** · `93e43f8f…` 3,231 / 150,103 / **268/268**; landed: selftest 268/268 rc 0; `--no-live` CLEAN (29 pass, 4 notes) rc 0; `--regression` PASS, `match=10/10`, flips 0, control GREEN, `MUTATE_RESTORE: OK`, target `dc7c4141…`, rc 0 (54.5 s); live **DIVERGED (3 fail, 49 pass, 8 notes, 60 rows)** in my window — session state, named in F2 | **PASS** (ladder + file-plane + regression rows exact; the live row is a point sample — mine diverged, not smoothed) |
| C2 | **Pin lineage + spec + kill ladder** — synth §2.3 `:154-186` | my own sed excision of the three marker families at r7/r8/r9; the spec re-extracted from the gate's own heredoc (`:1324-1369`) and hashed; the round-5 blob replayed through the harness | r7 → `c4c1afb75dd1c8aa…` (1,186 L), r8 → `d2bcdb31daea5d68…` (1,617 L), r9 → `dc7c4141449891cd…` (1,945 L), all byte-exact; `PIN_MADO` present only from r7 (absent r5/r6, as tabled); spec = **2,141 B, 10 `@defect`, sha `c7ee75b97c38ac8f…1dd8`** = the recorded pin; r5 replay: `killed=4 survived=6 inconclusive=0` (40 %), control GREEN, `MUTATE_RESTORE: OK` | **PASS** |
| C3 | **Census at the landed revision** — synth §2.5 `:205-215` | the counting commands on the frozen gate + row counts in my own runs | `row` sites **189** + `row_from_rc` **6**; per-plane gate 3 / hypr 23 / hypr-live 57 (51 + 6 rc) / omarchy 56 / terms 10 / theme 27 / walker 2 / waybar 17; distinct ids **55**; helper regexes **8 ids at 7 sites** `:387`, `:391`, `:406-410`; asserted ids **32**; emitted rows **41** (`--no-live`) / **60** (live) | **PASS** |
| C4 | **Corpus ledger + record debt** — synth §1.1 `:78-107`, §1.2 `:109-118` | `wc -l` + `sha256sum` per note; `grep`/`sed` per ledger row | all 19 note rows byte-match the table (L + sha16); `README.md` 19 L / `2dd274f5…` / **8 rows, 11 notes unrowed**; `SCORECARD.md` 21 L / `17fe5a42…`, rows 4–9 one-line stubs; `LOG.md` 300 L / `b6b5a4b2…`, rounds 4–9 one-liners; drafts' ⟨PENDING⟩ **13/19/19**; `corpus/lessons/` **0**; `walker-deep.md` sha `0982ba06…` unchanged | **PASS** |
| N1 | **note §8 command 2** (`gate-standing-use.md:324`) — `--selftest && --no-live` | frozen copy | `MADO_SELFTEST: 268/268` rc 0; `MADO_VERIFY: CLEAN (29 pass, 4 notes)` rc 0, `counts: pass=29 fail=0 unknown=0 skip=8 note=4`, boundary `bb2639d9a980…` | **PASS** |
| N2 | **note §8 command 3** (`:325`) — `--regression \| grep -E 'MADO_REGRESSION\|REGRESSION_TABLE'` | from the repo, worktree gate (sha checked before/after) | `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=dc7c4141…)` rc 0; `REGRESSION_TABLE … match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`; `REGRESSION_SPEC` `c7ee75b9…` (recorded pin matches); harness line printed `5807fd38…` (moved; F3) | **PASS** |

Note spot-checks beyond the two commands (all [O], on the frozen copy):
§1's help text quotes match byte-for-byte (base help + the three mode
paragraphs, each rc 0); `--root` with no value → `usage error: --root needs a
directory` rc 2; `MADO_VERIFY_LIVE=bogus` (default mode) → `usage error:
MADO_VERIFY_LIVE must be auto|yes|no` rc 2 (F4); §5.6 marker ranges
(`:414-593`, `:596-775`, `:1041-1204`, `:1216-1634`, `:1635-2157`) measured,
the derived target keeps the OMARCHY pair (2 marker hits) and loses the other
three families (0 hits each); §6 greps: `wallpaper.live|display_agree` 0,
`walker.sock` 0, `bb2639d9` 0, `VERSION_STR` unchanged at `:77`.

## 2. Re-run detail (commands and receipts)

- **Freeze.** `cp tools/mado-verify.sh /tmp/w10-aud-m10/gate-93e43f8f.sh` (sha
  re-checked on the copy); `git show <c>:tools/mado-verify.sh >
  hist/<c>.sh` for the five revisions; the note frozen as `note-7f61d87d.md`.
- **Ladder.** `sha256sum`/`wc -lc` per blob; `bash hist/<c>.sh --selftest`
  for each (28 / 53 / 89 / 217 / 268, all rc 0, ~14 s total).
- **Landed modes (frozen copy).** `bash gate-93e43f8f.sh --selftest` → 268/268;
  `--no-live` → CLEAN (29 pass, 4 notes); `bash gate-93e43f8f.sh` ×2 (live) →
  DIVERGED `(3 fail, 0 unknown, 49 pass)` both times — first fail:
  `live.waybar.process (no waybar process)`; `pgrep -ax waybar` → no process;
  `boundary.readonly PASS` with `bb2639d9a980…` in both runs.
- **Regression (N2).** `bash tools/mado-verify.sh --regression` in the repo;
  gate sha `93e43f8f…` identical before and after; log
  `note-cmd3-regression.live.log`.
- **Pin excisions (C2).** `sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK
  >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d'` + the R7-SELFTEST
  and R8-BLOCK pairs applied to `hist/0c20a76.sh`, `hist/12c8f08.sh`,
  `gate-93e43f8f.sh` → byte-exact pins above; `grep -c 'PIN_MADO='` per blob.
- **Spec (C2).** `sed -n '1325,1368p' gate-93e43f8f.sh` (the heredoc body,
  trailing LF stripped as `mado_r7_spec_write` does) → 2,141 B,
  `c7ee75b9…1dd8`, 10 `@defect`.
- **R5 replay (C2).** `bash <tameshi>/tools/mutate-and-run.sh --target
  hist/eead56b.sh --defects spec-derived.txt --suite 'bash "$MUTANT"
  --selftest' --label mado-verify-r5-audit --timeout 30` → `MUTATE: DONE
  (defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%)`, control
  GREEN, `MUTATE_RESTORE: OK`; log `mut-r5-audit.log` (run under the moved
  harness `75ed934d…`, so the 40 % rate survives that move).
- **Census (C3).** `grep -cE '^[[:space:]]*row '` → 189;
  `…'row_from_rc '` → 6; `grep -oE '^[[:space:]]*(row|row_from_rc)
  [a-z-]+ [a-z0-9._-]+' | awk '{print $NF}' | sort -u | wc -l` → 55;
  per-plane `awk '{print $2}' | sort | uniq -c`; asserted
  `grep -oE 'st_row_(has|detail) "[^"]*" [a-z0-9._-]+' | awk '{print $NF}' |
  sort -u | wc -l` → 32; row counts from my logs → 41 / 60.
- **Corpus (C4).** `wc -l` + `sha256sum` over the 19 committed notes;
  `grep -cE '^\| .knowledge' corpus/README.md` → 8;
  `grep -c PENDING plans/round-{7,8,9}-record-draft.md` → 13/19/19;
  `ls corpus/lessons/ | wc -l` → 0; `sha256sum corpus/knowledge/walker-deep.md`
  → `0982ba066c72575a…`.
- **Note checks.** Helps for base + `--regression/--snapshot/--snapshot-diff`
  (rc 0 each, base help deliberately silent on the mode flags); the two
  refusal arms above; §6 greps above.

## 3. Spot-checks (three, all re-run 2026-10-14)

1. **Pin/excision + spec + kill rate.** Three excisions byte-exact
   (`c4c1afb7`/`d2bcdb31`/`dc7c4141`), the spec heredoc re-hashed to the
   recorded pin (2,141 B / 10 defects / `c7ee75b9…1dd8`), and the round-5
   blob re-replayed to 4/10 (40 %) with control GREEN and restore OK — the
   kill ladder's bottom rung is measured, not recited.
2. **Census + corpus.** 189 + 6 sites, 55 ids, 32 asserted, 8-id helper
   regexes at seven sites, 41/60 emitted rows; all 19 note rows byte-match
   the synthesis table; README 8 rows / 11 unrowed; SCORECARD stubs 4–9;
   LOG 300 L; PENDING 13/19/19; lessons 0; `walker-deep.md` unchanged.
3. **Note commands + invariants.** N1 and N2 green at the landed revision
   (268/268; regression `match=10/10`, target `dc7c4141…`); the gate sha
   `93e43f8f…` identical before and after every run of mine; the config-plane
   combined hash `bb2639d9a980…` identical in my `--no-live` run and both
   live runs; zero substrate writes.

## 4. Findings (named, not smoothed)

- **F1 — landed name vs referenced name.** The synthesis landed as
  `corpus/knowledge/arc-synthesis.md` (self-label M10-1). The round-10 plan
  §(a) names `corpus/knowledge/ten-round-synthesis.md`, the standing-use
  note's `recheck:` line still points at
  `corpus/knowledge/ten-round-synthesis.md` (`gate-standing-use.md:13`), and
  the M10-4 poll waits on the plan name — that path does not exist at my
  read. The record family should cite the landed name; the note's pointer is
  stale by one rename (cross-reference defect, naming class; not edited here).
- **F2 — live window diverged; session state, not a gate defect.** My two
  live runs (20:59:26Z, 20:59:35Z) read `DIVERGED (3 fail, 0 unknown, 49
  pass)`: `live.waybar.process` / `.layer` / `.tray`, and `pgrep -ax waybar`
  → no process. The synthesis's §2.2 live row (CLEAN 52 pass, 8 notes) is
  m10-1's window sample; the note §2's worked example documents exactly this
  class and the re-run rule — I re-ran once (same result), so by the note's
  own reading rule this is a finding about the session, not about the gate.
  The file plane and the boundary row stayed green in both runs.
- **F3 — the harness moved during the round.** `mutate-and-run.sh`:
  `cf41efaa…242c75` (m10-1 §2.2's line; m10-3's tick) → `5807fd38…` (my N2
  run) → `75ed934d…` (my R5 replay). Provenance, not gated — and both my
  re-runs reproduce under the moved bytes (regression PASS; r5 4/10), so the
  movement does not disturb the audited numbers. Recorded so no single
  harness sha is quoted as "the round's".
- **F4 — the bad-env usage arm is flag-dependent.** `MADO_VERIFY_LIVE=bogus`
  → rc 2 `usage error: MADO_VERIFY_LIVE must be auto|yes|no` in the default
  (live) mode; with `--no-live` the flag overrides the env and the same bad
  value reads a CLEAN file-plane run, rc 0. The note's claim holds in the arm
  it names; the precedence nuance belongs in §6's usage-arm row so a reader
  does not file the rc-0 case as a defect (precision note, not a defect).

## 5. Unknowns

- **U1 — the round-10 commit.** Both audited artifacts were uncommitted at my
  read; my numbers bind to `a5b48331…` (arc-synthesis) and `aaa2e625…`
  (note, incl. M10-3's append). A later edit re-opens the audited bytes;
  re-derive from the commit, never from this report.
- **U2 — live point samples.** My live window is one sample; waybar's absence
  may be transient (m10-2's own example saw the process return with a new
  pid). Whether it returns before the round closes is outside my window.
- **U3 — harness drift continues.** `75ed934d…` was the last revision I
  measured (18:03); later sibling edits are unmeasured by me.
- **U4 — single host / toolchain / window.** bash 5.3.15, one window
  20:54–21:02Z 2026-10-14. The synthesis's live row (52 pass) is m10-1's run;
  my live row is mine; both are point samples.
- **U5 — coverage of the audit.** I re-derived the four claims above and the
  note's two commands, plus the extra reads named in §1/§2. The synthesis's
  §3 (config plane), §4 (historical boundary proofs — r2–r4 records), §5
  (trend verdicts), §6 (gap ledger) and the membership of §7's 9/8/12
  classification were read ([OBS-record] by the synthesis's own tagging) but
  not re-measured member by member here; §7's arithmetic and naming were
  checked against §1.2/§6 only.