# AUD-M7 — round-7 audit: `--regression` mode + the two new planes (5 claims re-measured; zero config mutation)

Lane AUD-M7, 2026-10-14. Write scope: **this file only** — no other file in
mado-shokunin was written by this lane (the round-7 lanes' own modified/untracked
files are untouched by me; my only tree entry is this report). Scratch
`/tmp/w7-aud-m7-{gate,poll,probe,regression,final}/`; retained evidence:
`/tmp/w7-aud-m7-final/` (all logs quoted below) and two kept regression
workdirs: `/tmp/mado-verify-regression.VhZA3u` (`--keep` PASS run) and
`/tmp/mado-verify-regression.eMWeuE` (SETUP-guard run). **Zero config mutation**:
my own combined config-plane hash `cacd4cc6138b9329f3070d29a6a41982a0cf21e4157d9e3dadf21f0ce1e88676`
identical before probing (18:22:42Z), after `--selftest` (18:37Z), and after all
runs (18:39Z). No compositor/session state touched; no socket connected; no
launcher opened.

**Audited revisions (in flight — uncommitted at audit close).** The mado
round-7 lanes were writing during the audit window; every number below is tied
to a measured sha, and anything after my close (18:41Z) is not covered (U1).

| artifact | sha256 (prefix) | measured at |
|---|---|---|
| `tools/mado-verify.sh` (audited gate) | `90d50cdd4d18410b…` · 1,755 L / 75,771 B | stable 18:32:11Z → close; `git diff --numstat HEAD` = +569/−0 |
| recorded base revision (round-6 HEAD gate) | `c4c1afb75dd1c8aa…a5171` · 1,186 L | reproduced by excision (§2.5) |
| `corpus/knowledge/theme-wallpaper-plane.md` | `8c578cc70e36506d…` · 394 L / 27,594 B | 18:27:19Z |
| `corpus/knowledge/walker-live-surface.md` | `2bbb9609283f2d81…` · 300 L / 19,203 B | 18:25:55Z |
| `plans/round-7-record-draft.md` | `045d380ab52ce317…` | 18:27:15Z |
| `LOG.md` (round-7 M7-1 entry at `:297`) | `1ee327882c3f810b…` · 297 L | 18:33:41Z |

## 1. Verdict table

| # | claim (source) | scope / method | result | verdict |
|---|---|---|---|---|
| C1 | **Stage (a)** — `--regression` replays the recorded round-6 mutation case and PASSes (`plans/round-7.plan.md` §(a); `LOG.md:297`) | `bash tools/mado-verify.sh --regression` (3 runs: plain, timed, `--keep`); inspect sweep evidence | `MADO_REGRESSION: PASS` rc 0; `REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`; sweep `MUTATE: DONE … killed=10 survived=0 inconclusive=0 kill-rate=100%`; `CONTROL: GREEN`; `MUTATE_RESTORE: OK` (before = after = pristine `c4c1afb7…a5171`); derived target sha == recorded pin; embedded spec sha == recorded `c7ee75b9…`; reproducible across runs (11.85 s each); `REGRESSION_CLEANUP: removed=10` | **PASS** |
| C2 | **Stage (a) contract** — token `MADO_REGRESSION:` never `MADO_VERIFY:`; exit 0/1/2; `--target/--defects/--suite` refused (usage); scratch `/tmp/mado-verify-regression.*`; SETUP when unverifiable | refusal probes (§2.2); missing-harness SETUP (§2.3); widened-copy pin guard (§2.4); selftest R12/R13; token greps | refusals rc 2 with named flag; missing harness → `MADO_REGRESSION: SETUP` rc 2, 0 `MADO_VERIFY:` tokens; widened copy → SETUP + `REGRESSION_RECUT` hint (derived sha `116ed7ff…` ≠ pin), no sweep run; scratch path exactly as specified; `--regression --help` rc 0 and documents the mode | **PASS** (one documented deviation, §5a) |
| C3 | **Stage (b)** — theme/wallpaper plane **gate rows** (`plans/round-7.plan.md` §(b)) | row-site census + `--live` row table + note §6 row spec | **NOT LANDED as gate rows**: row census unchanged (106 `row` + 7 `row_from_rc` sites; six plane ids `hypr\|hypr-live\|waybar\|walker\|terms\|gate`; no `theme.*` rows; `live.theme.current` still the only theme site, NOTE-level). The plane shipped as the measured note, whose anchors I re-measured independently — 8/8 file pins, wallpaper chain, normalization rule, consumers all reproduce (§3.1) | **NOT-LANDED (note verified)** |
| C4 | **Stage (c)** — walker live surface **gate rows** (`plans/round-7.plan.md` §(c)) | same method | **NOT LANDED as gate rows**: walker live = version + services only (no socket/owner/layer rows; no `walker-live` id). The note landed and its anchors reproduce — sockets `srwxr-xr-x` 0 B at `$XDG_RUNTIME_DIR/{walker,elephant}/`, `dev.benz.walker` owner pid == walker pid, no walker namespace (absence = NOTE) (§3.2) | **NOT-LANDED (note verified)** |
| C5 | **No-regression + census + zero mutation** (plan Measure lines; round-6 contracts) | `--selftest`, `--no-live`, `--live`, row census, independent plane hash | selftest **53 → 89** (+36: R1–R13 in the marked block); `--no-live` → `MADO_VERIFY: CLEAN (17 pass, 2 notes)` rc 0, `counts: pass=17 fail=0 unknown=0 skip=1 note=2`; `--live` → `MADO_VERIFY: CLEAN (35 pass, 4 notes)` rc 0, `counts: pass=35 fail=0 unknown=0 skip=0 note=4` — **identical to the recorded round-6 counts**; live row table identical (39 rows: hypr 9 / hypr-live 20 / waybar 4 / walker 1 / terms 4 / gate 1); plane hash unchanged across all runs | **PASS** |

Aggregate: **stage (a) and the no-regression contract are verified end-to-end;
stages (b)/(c) are not landed as gate rows** at audit close — the round shipped
them as measured notes, each self-labelling "no verdict token / landing gate
rows is stage (b)/(c), gated on (a)". Nothing audited overclaims: the M7-1 LOG
entry states only the gate change; the notes state their own non-landing. The
plan's ordering is honoured ((a) landed 18:28–18:32Z; the notes cite (a)'s
gate).

## 2. Stage (a) re-measure detail

### 2.1 The replay (my runs)

Command: `bash tools/mado-verify.sh --regression` (plain; then `--keep`; then a
timed run). Logs `/tmp/w7-aud-m7-final/{regression-run,regression-keep,regression-run2}.log`.
Receipt lines (run 2, verbatim):

    REGRESSION_TOOL: …/tools/mado-verify.sh sha256=90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd
    REGRESSION_DATE: 2026-10-14T18:37:13Z
    REGRESSION_HARNESS: …/tameshi-shokunin/tools/mutate-and-run.sh sha256=cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75 (recorded revision b56c6e57…22bcb — provenance, not gated)
    REGRESSION_SPEC: /tmp/mado-verify-regression.mvQe90/mado-verify.defects.spec sha256=c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8 (recorded pin matches)
    REGRESSION_TARGET: …/target.mado-verify.sh sha256=c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171 (recorded pin …a5171; match=yes)
    REGRESSION_BAND: all recorded kills required (recorded 10/10 KILLED; flips=0; inconclusive=0; control GREEN; MUTATE_RESTORE OK; target sha unchanged) — plan §(a) killed-delta<=1 tolerance not applied
    REGRESSION_SWEEP mado-verify-hardened: MUTATE: DONE (target=mado-verify-hardened defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
    REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
    REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
    REGRESSION_CLEANUP: removed=10 kept-fixture dir(s) named by this run (paths read from this run; /tmp/w5-mado-m52-selftest.* prefix-guarded)
    MADO_REGRESSION: PASS (case=mado-verify-hardened; target=c4c1afb75dd1c8aa…a5171)
    REGRESSION_WORKDIR: /tmp/mado-verify-regression.mvQe90 (removed on PASS; --keep retains)

- The kept workdir (run 3, `--keep`) contains `target.mado-verify.sh` byte-equal
  to **my own independent excision** (§2.5), and `case/sweep.log` with
  `CONTROL: GREEN (exit=0 … pristine-sha256=c4c1afb7…)`,
  `MUTATE_RESTORE: OK (before = after = pristine = c4c1afb7…)`,
  `MUTATE: DONE … 10/10 100%`; `case/sweep/results.tsv` carries all ten
  per-defect rows (D1–D9, R1) all `KILLED`.
- Timing: `real 0m11.848s`, rc 0 (the M7-1 LOG claims 11.99 s — corroborated,
  not repeated).
- Tokens: `grep -c 'MADO_VERIFY:'` → **0** in every regression log.

### 2.2 Refusal contract (my probes, 18:37:05Z)

| invocation | rc | first line |
|---|---|---|
| `--regression --target x` | 2 | `usage error: --regression takes no --target` |
| `--regression --defects=x` | 2 | `usage error: --regression takes no --defects` |
| `--regression --suite y` | 2 | `usage error: --regression takes no --suite` |
| `--regression --no-live` | 2 | `usage error: --no-live is not valid with --regression (the case reads no substrate)` |
| `--regression --root /tmp` | 2 | `usage error: --root is not valid with --regression (the case reads no substrate)` |
| `--regression --bogus` | 2 | `usage error: unknown argument --bogus` |
| `--regression --help` | 0 | prints usage + `--regression  replay the recorded mutation case` |

### 2.3 SETUP path (measured end-to-end)

`MADO_VERIFY_HARNESS=/nonexistent/harness bash tools/mado-verify.sh --regression`
→ `MADO_REGRESSION: SETUP (mutation harness not found: /nonexistent/harness; set MADO_VERIFY_HARNESS)`
rc **2**, no `MADO_VERIFY:` token. (Suite also asserts this shape at `:553-557`.)

### 2.4 Widened-outside-blocks guard (my copy, repo untouched)

`cp tools/mado-verify.sh /tmp/w7-aud-m7-final/widened.sh` + one appended comment
line **outside** the marked blocks, then `--regression` with the real harness:

    REGRESSION_TARGET: …/target.mado-verify.sh sha256=116ed7ffb93b4a28… (recorded pin c4c1afb7…; match=no)
    REGRESSION_RECUT: bash …/mutate-and-run.sh --target … --defects … --suite 'bash "$MUTANT" --selftest' …
    MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
    rc=2, no sweep run

### 2.5 The pin mechanism (excision) — independent reproduction

    sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^…<<<$/d' \
        -e '/…MADO-R7-SELFTEST-BLOCK >>>…/,/…<<<…/d' tools/mado-verify.sh | sha256sum
    → c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171  (1,186 L)
    diff <(git show HEAD:tools/mado-verify.sh) — → empty (byte-identical)

Designed answer to the scribe draft's §3.1 tension: the recorded table stays
revision-tied to `c4c1afb7…`; the mode reconstructs that revision from its own
file by excising the two marked blocks (`:379-558`, `:699-1087`) and refuses
with SETUP if the result no longer equals the pin. A later widening (outside
the blocks) must re-cut and move the pin — the RECUT command is printed.

## 3. Plane claims (b)/(c) — what landed, and independent anchor re-measure

**What landed:** two measured notes (no gate rows, no verdict token — as their
§0 states). Gate row-site census by plane prefix, before (HEAD `c4c1afb7…`) vs
audited revision: **identical** — 106 `row` + 7 `row_from_rc`; hypr 23,
hypr-live 51, waybar 17, walker 2, terms 10, gate 3; the selftest plane-prefix
regexes (`:352`, `:356`, `:371-375`) still match the six ids only (no new plane
id exists, so nothing is uncounted; the note §6 spec requires widening those
sites when `theme` lands).

### 3.1 theme-wallpaper-plane.md — anchors re-measured (my probes, 18:22:42Z)

| anchor (note) | my independent measurement | match |
|---|---|---|
| 8 theme-file pins (§2.1) | all 8 sha256 re-hashed from `~/.config/omarchy/current/theme/` — alacritty.toml `8c3d1457…`, colors.toml `dbdd13a6…`, hyprland.conf `79126bec…`, hyprlock.conf `3ef010e7…`, mako.ini `95bf0c86…`, swayosd.css `f88118e9…`, walker.css `f44cb450…`, waybar.css `a1807a17…` | **8/8** |
| `theme.name` | `matte-black`, 12 B | ✓ |
| background symlink → target | `current/background` → `current/theme/backgrounds/0-ship-at-sea.jpg`; target 1,681,677 B, sha `55fa691a…` | ✓ |
| normalization rule (reader) | `printf 'matte-black' \| sed -E 's/(^\|-)([a-z])/\1\u\2/g; s/-/ /g'` → `Matte Black` == `omarchy theme current` | ✓ |
| rule sources | `omarchy-theme-current:9` (reader sed), `omarchy-theme-set:17` (writer sed) | ✓ (note's final citations) |
| consumers | `hyprland.conf:13` theme source; `hyprlock.conf:1`; `waybar/style.css:1` `@import "../omarchy/current/theme/waybar.css";`; `alacritty.toml:1` `general.import`; `mako/config` symlink → `…/current/theme/mako.ini` | ✓ |
| live chain | swaybg PID 1203358 argv `-i …/current/background -m fill`; `hyprctl -j layers` DP-1 level 0 `wallpaper` pid **1203358** 3440x1440; level 2 `waybar` 1203352 3440x26 | ✓ |

### 3.2 walker-live-surface.md — anchors re-measured

| anchor | my measurement | match |
|---|---|---|
| sockets | `$XDG_RUNTIME_DIR/walker/walker.sock`, `$XDG_RUNTIME_DIR/elephant/elephant.sock` — `srwxr-xr-x`, 0 B (never connected; stat only) | ✓ |
| D-Bus owner | `busctl --user status dev.benz.walker` → `PID=1203471` == walker pid | ✓ |
| process identity | walker 1203471 `/usr/bin/walker --gapplication-service`; elephant 1203474; both units `active` | ✓ |
| layer invariant | no walker namespace in `hyprctl -j layers` → absence (NOTE direction, never pass/fail) | ✓ |

## 4. No-regression / census / zero mutation

1. `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 89/89 assertions passed` rc 0
   (baseline at HEAD: 53/53). Count check: 37 assertion call sites in the R7
   block of which 36 execute on a pristine run (R10's defected-gate branch is
   not taken) → 53 + 36 = 89, closing arithmetically.
2. `--no-live` → `CLEAN (17 pass, 2 notes)`, `counts: pass=17 fail=0 unknown=0 skip=1 note=2`, rc 0.
3. `--live` → `CLEAN (35 pass, 4 notes)`, `counts: pass=35 fail=0 unknown=0 skip=0 note=4`, rc 0.
   Both verdicts equal the recorded round-6 numbers (`gate-mutation-proof.md` §4
   spot-check 3); the verify path is untouched (§2.5 excision = byte-identical).
4. Independent boundary proof: combined config-plane hash (hypr/waybar/walker/
   alacritty/omarchy/mako, gate file classes + `*.name`) =
   `cacd4cc6138b…e88676` before probing, after `--selftest`, and after all
   regression runs — unchanged. The gate's own `boundary.readonly` row PASSes
   in both verdict runs.
5. My round-6 re-cut, before the round-7 gate landed (18:24Z, harness
   `b56c6e57…`): tameshi's spec `c7ee75b9…` against gate `c4c1afb7…` →
   `10 killed / 0 survived / 0 inconclusive`, `MUTATE_RESTORE: OK`. The mode's
   own replay (harness `cf41efaa…`) reproduces it. Two harness revisions, same
   target, same table.

## 5. Observations (recorded, not smoothed)

1. **Band deviation (documented).** The plan §(a) pre-stated
   `|killed − recorded| ≤ 1` and ≤1 verdict flip; the implementation requires
   an **exact** match (10/10 KILLED, flips=0), stating the tolerance "is
   deliberately NOT applied" (`tools/mado-verify.sh:717-722`, `:1003`; LOG
   entry repeats it). Fail-closed direction (only reduces PASSes), and it is
   disclosed in the artifact and the LOG — but a record that claims "the plan's
   band" must carry this deviation, not the plan's tolerance.
2. **Harness moved mid-round.** `tameshi-shokunin/tools/mutate-and-run.sh`
   `b56c6e57…` (46,850 B, used by my 18:24Z baseline) → `cf41efaa…` (61,632 B,
   mtime 18:29:01Z; used by the mode's 18:37–18:39Z runs; tameshi's own lane,
   concurrent). The mode prints the harness sha as **provenance, not gated**;
   both revisions re-measured the same 10/10 table against the same target.
   Nothing gates the harness revision — exact-table discipline means a
   behavior-changing harness surfaces as FAIL, not silently.
3. **Note revision churn (provenance).** Both notes were in active revision
   during my first reads (walker 19,111 → 19,203 B; theme moved several shas).
   One in-flight theme-note revision cited the writer rule at
   `bin/omarchy-theme-set:19`; the frozen revision reads `:17` and matches my
   measurement (`:17`; also `HEAD:bin/omarchy-theme-set:17`). No defect in the
   frozen text — recorded because the scribe draft's pins are provisional by
   its own rule.
4. **Record debt open at audit close** (outside this audit's claims; for the
   finalizer): `SKILL.md` unchanged (`72196e7e…`, last write 18:02:53Z) — the
   round-7 SKILL section does not exist yet; `SCORECARD.md` unchanged
   (`e23b75fe…` — still the 18-line round-6 state); `corpus/README.md` unchanged
   (`2dd274f5…`, 8 coverage rows); `walker-deep.md` unchanged (`0982ba06…`) —
   the §10/§11 errata append the walker note's ledger feeds is not done; LOG.md
   carries the M7-1 entry (`:297`). The theme/walker notes' own §10 errata
   sections are the append-only routes.
5. **Cosmetic.** The base `--help` (without `--regression`) still lists only the
   five original flags; `--regression --help` appends the mode paragraph.
   Discoverability of the mode via plain `--help` is absent (same class as the
   round-6 "still self-labels v1" note). Observation only — not a verdict input.

## 6. Spot-checks (reproducible)

1. **Excision/pin**: `sed`-excise the two `MADO-R7` blocks from
   `tools/mado-verify.sh` → `sha256sum` = `c4c1afb7…a5171`, 1,186 L; diff vs
   `git show HEAD:tools/mado-verify.sh` empty. (Run 18:37:05Z; also asserted
   in-suite at `:516-529`.)
2. **Replay**: `bash tools/mado-verify.sh --regression` → `MADO_REGRESSION: PASS`,
   `match=10/10 … flips=0`, rc 0, 11.848 s; `CONTROL: GREEN` +
   `MUTATE_RESTORE: OK` + `killed=10 survived=0 inconclusive=0 kill-rate=100%`
   in the retained workdir log.
3. **Counts/verdicts**: `--selftest` → 89/89 rc 0; `--no-live` → CLEAN
   (17 pass, 2 notes) rc 0; `--live` → CLEAN (35 pass, 4 notes) rc 0 — with the
   plane hash identical before/after (`cacd4cc6…e88676`).

## 7. Unknowns

- **U1 — in-flight revisions.** The audited artifacts are uncommitted; the
  finalizer's commit may re-pin every sha here. Anything after my close
  (18:41Z) is uncovered.
- **U2 — (b)/(c) gate rows.** Whether they land later in the round (another
  (a)-gated lane) is unknown at close; the notes' row specs (§6 / ledger) are
  the paste-ready text, and the selftest prefix-regex widening is a stated
  landing condition.
- **U3 — harness revision delta.** Two harness revisions produced the same
  table; I did not diff them (sibling repo, out of scope). Whether their
  behavior is identical for other cases is unmeasured here.
- **U4 — probe-window statements.** Live anchors (pids, layer presence, socket
  mtimes) are point samples; a session restart invalidates them. The sockets
  path parent-dir shape (`$XDG_RUNTIME_DIR/<app>/<app>.sock`) is measured for
  walker/elephant only.
- **U5 — foreign scratch.** `/tmp/w5-mado-m52-selftest.*` (109 dirs at close)
  belong to other writers' runs; I removed only the 10 named by my own baseline
  run (exact paths from its evidence), leaving foreign dirs untouched. Eight
  `/tmp/mado-verify-regression.*` dirs remain (mine: `VhZA3u` keep-evidence,
  `eMWeuE` SETUP guard; others belong to concurrent lanes).