# mado round 11 — closeout: the arc end, verified (M11-1, round 11)

source: this lane's own re-verification at the round-10 landed revision
(commit `f7bfc9f`; gate sha256 `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`,
3,231 L / 150,103 B, unchanged by round 10). Every number below was re-run
by this lane at that revision and names its command, or is tagged
**[OBS-record]** with the round record that measured it. Scratch:
`/tmp/w11-m11-1/`; the repo was read and the gate run read-only
throughout — no repo write, no commit, no substrate read, no session
disturbance; secrets shape-only.

verified-at: 2026-10-14 21:23–21:35Z (host offset −03:00), single host
(bash 5.3.15).

recheck: `sha256sum tools/mado-verify.sh` — a moved gate sha invalidates
every number here; then the battery

    bash tools/mado-verify.sh --selftest                       # today 268/268
    bash tools/mado-verify.sh --no-live
    bash tools/mado-verify.sh
    bash tools/mado-verify.sh --regression

Marks: **[O]** measured by this lane (command quoted); **[OBS-record]**
cited from a round record, source named; **[I]** inference; **[U]** unknown.

## 1. The arc in one page

The arc is the config plane of this host, probed, measured, and
recommended — never edited (PROVINCE.md:10-12). The lane's single verdict
instrument is `tools/mado-verify.sh`: `MADO_VERIFY: CLEAN|DIVERGED` is the
only token mado issues about the config plane. `corpus/knowledge/` stands at
**21 notes** after round 10 (`ls corpus/knowledge/ | wc -l`) — 19 arc notes +
round 10's synthesis and standing-use note (counts per note: arc-synthesis
§1.1, [OBS-record]); README rows are still 8, so **13 notes are unrowed**.

The planes as measured (authority: `corpus/knowledge/arc-synthesis.md` §3):

| plane | what exists (measured) | evidence class |
|---|---|---|
| hypr core | 12 active `*.conf`; `hyprland.conf` 29 L pure orchestrator, 17 `source` statements, 192 binds, sha `4f52854a3c143dcf…` (= r1 pin) [OBS-record] | file bytes + hyprctl read verbs |
| hypr-live | `configerrors` empty rc 0; 57/57 `getoption` 0 mismatch; 46 agreement + 6 agreement* + 4 live-default; dispatcher behaviour `[INF-docs]`/[UNK] [OBS-record] | hyprctl live read |
| waybar | JSONC parses; bar top 26; 19 modules; layer surface + live tray watcher; no IPC/query verb in 0.15.0 → module text stays **[UNK]** | file bytes + consumer probe |
| walker | 2.17.0; sockets `stat`'d 0 B, never connected; no reload path — restart is the apply path | consumer-side probe |
| terms | alacritty only installed (`command -v`); font 12.5 + padding 14 uniform | file bytes + install-state sweep |
| theme | `matte-black`; include/import chain resolves 7 routes; `current/background` → `0-ship-at-sea.jpg`; the theme *choice* is operator-owned (NOTE) | file bytes + gate rows |
| omarchy | `omarchy version` 3.8.3; tag `v3.8.4` at HEAD; skill leaf `becd149e…`; `git status`/`fetch` never run | read-only git verbs |
| idle/lock | hypridle/hyprlock/hyprsunset **absent**; the declared 150 s/152 s chain has no consumer (F1, S1, stop cause `[UNK]`) | `pgrep -x` + r3/r4 records |
| mako/swayosd | mako owns `org.freedesktop.Notifications`; `makoctl mode` → `default`; mako config is a symlink into the theme | consumer probes |

Evidence classes (routing in `SKILL.md:111-139`): **file bytes** (declares,
include order, identity), **hyprctl live read** (effective values, owners),
**docs-inference** `[INF-docs]` (grammar; never host state), **consumer-side
probe** (runtime facts another consumer owns), **gate rows** (verdicts).
Divergence vocabulary `agreement`/`agreement*`/`live-default`/`mismatch`/
`config-only`; severity S1–S3 (register F1–F10: 1×S1 + 2×S2 + 7×S3).

Boundaries held every round: read-only substrate — the gate's own
`boundary.readonly` row prints the combined hash `bb2639d9a980…` in every
verdict run (`grep -h -o 'bb2639d9a980[0-9a-f]*'` on this lane's no-live
and live logs → equal) [O]; no compositor/session mutation (no launcher, no
socket connect, no `omarchy theme set`, no restart); receipts stay in scratch;
secrets shape-only; the omarchy checkout only via `git show/describe/rev-parse`;
no new frontier in the final round — uncovered surfaces are gaps, §5, not promises.

## 2. The gate — 28 → 268

The ladder re-derived complete, cell for cell **[O]** — per-arc-commit
`git show <commit>:tools/mado-verify.sh | sha256sum | cut -c1-16`,
`| wc -lc`, then each blob's own `--selftest` re-run from a frozen copy:

| arc commit | round | gate sha16 | L / B | `--selftest` (this lane) | `PIN_MADO` |
|---|---|---|---|---|---|
| r1–r4 | — | (empty blob, 0 L — round-1 operability ceiling) | — | — | — |
| `eead56b` | r5 | `d7edaab4bf108625` | 1,098 / 45,334 | **28/28** rc 0 | (absent) |
| `c03c249` | SHONEN | same r5 blob | — | — | (absent) |
| `c8f6667` | r6 | `c4c1afb75dd1c8aa` | 1,186 / 50,126 | **53/53** rc 0 | (absent) |
| `0c20a76` | r7 | `90d50cdd4d18410b` | 1,755 / 75,771 | **89/89** rc 0 | `c4c1afb7…a5171` |
| `12c8f08` | r8 | `7da4ec5013583c91` | 2,887 / 131,612 | **217/217** rc 0 | `d2bcdb31…db62` |
| `de22dfd` | r9 | `93e43f8fe8b9bdd4` | 3,231 / 150,103 | **268/268** rc 0 | `dc7c4141…f8fd` |
| `f7bfc9f` | r10 | `93e43f8fe8b9bdd4` | 3,231 / 150,103 | **268/268** rc 0 | (unchanged) |

Round 10 opened **no gate edit** — the landed and frozen revisions are
identical. Pin lineage `c4c1afb7…a5171` (r7) → `d2bcdb31…db62` (r8) →
`dc7c4141…f8fd` (r9); the three excised marker families are
`MADO-R7-SELFTEST-BLOCK`, `MADO-R7-REGRESSION-BLOCK`, `MADO-R8-BLOCK`;
a widening outside every pair re-cuts via the printed `REGRESSION_RECUT`.
Kill ladder: r5 `d7edaab4…` **4/10 (40 %)** **[OBS-record:** gate-mutation-proof
§1; re-derived by AUD-M10 §2: `killed=4 survived=6 inconclusive=0`, control
GREEN, `MUTATE_RESTORE: OK`**]** → r6–r9 **10/10**.

The frozen revision's whole row re-run by this lane **[O]**, receipts
`/tmp/w11-m11-1/`:

- `MADO_SELFTEST: 268/268 assertions passed` rc 0.
- `--no-live` → `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only —
  live layer skipped: --no-live)`; counts `pass=29 fail=0 unknown=0 skip=8
  note=4`; boundary `bb2639d9a980…` PASS.
- `--regression` → `MADO_REGRESSION: PASS (case=mado-verify-hardened;
  target=dc7c4141…f8fd)` rc 0; `REGRESSION_TABLE … match=10/10
  recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`;
  `REGRESSION_SPEC c7ee75b9…1dd8` (recorded pin matches);
  `REGRESSION_HARNESS 75ed934d…` vs recorded `b56c6e57…` — provenance,
  not gated; `REGRESSION_CASE … PASS (control=green restore=ok)`.
- live → `MADO_VERIFY: DIVERGED (3 fail, 0 unknown, 49 pass)` rc 1 —
  first fail `live.waybar.process (no waybar process)`; **three consecutive
  live runs in this lane's window diverged identically** (`pgrep -ax waybar`
  → rc 1). By the standing-use note's own reading rule (re-run once before
  filing a live FAIL), this survived the re-run: it is a finding about the
  session, not a gate defect, and is not smoothed. The file plane never
  moved (`boundary.readonly PASS` in every run). The live layer is
  correctly catching a session whose waybar has not returned; the round-9/10
  records' live CLEAN rows were taken while it ran.

Modes and vocabulary: (default) live read-only; `--no-live`; `--root DIR`;
`--selftest`; `--regression [--keep]`; `--snapshot FILE`;
`--snapshot-diff OLD NEW`; `--help`. Row classes PASS/FAIL/UNKNOWN/SKIP/
NOTE; UNKNOWN blocks CLEAN; NOTE never flips the verdict; exit map 0/1/2.
`VERSION_STR` still reads `mado-verify.sh v1 (mado-shokunin round 5 / M5-2)`
(`:77`) — a named residual, §5.

## 3. The standing-use runbook — pointer

**`corpus/knowledge/gate-standing-use.md`** (361 L / `aaa2e625253e881e…`
/ 22,931 B, self-label M10-2 + lane M10-3's appended cadence
receipt; landed `f7bfc9f`). The operator reads it in this order:

- **§4, the standing cadence** — what to run when: a config file
  changed → live run; pre-commit → `--selftest`; a gate edit inside the
  marked pairs → `--selftest`; a widening → `--regression`; drift watch →
  snapshot pair + `--snapshot-diff`.
- **§8, the three commands** — `sha256sum tools/mado-verify.sh`;
  `--selftest && --no-live`; `--regression | grep -E 'MADO_REGRESSION|REGRESSION_TABLE'`.
- **§5, the maintenance rules** — a surviving mutant says "no test
  notices this clause"; a widening carries `MADO_REGRESSION: PASS`; pins are
  never edited to match reality; exemptions by name and counted; the tameshi
  harness is read-only; marker families measured.

Finding **F4 [O]**: the note's own recheck line (`:13`) still cites
`corpus/knowledge/ten-round-synthesis.md` — the path the round-10 design
predicted and which never landed; the landed path is
`corpus/knowledge/arc-synthesis.md`. Both values are carried here; the
append-only correction belongs to this round's settlement (see §5).

## 4. The round-10 handoff, verified (a)

Precondition read **[O]**: `git show f7bfc9f --stat` → 9 files, +2,312/−1.

| clause | landed? (measured) | receipts | verdict |
|---|---|---|---|
| (a10) the arc synthesis | **yes** — `corpus/knowledge/arc-synthesis.md`, 387 L by `wc -l` / `a5b4833141461810…` (editor view 388) | `sha256sum` + `wc -l` | matches the design's predicted sha `a5b48331…` |
| (b10) the standing-use note | **yes** — `corpus/knowledge/gate-standing-use.md`, 361 L / `aaa2e625253e881e…` / 22,931 B | `sha256sum` | matches the design's freeze-time metric |
| (c10) the record family | **partly** — SCORECARD row 10 (stub), LOG `:301` (round-10 one-liner), SKILL round-10 append (+90/−1 at commit); **not landed**: README rows (unchanged, `2dd274f5e270e65b`, still 8), lessons (0), the drafts' ⟨PENDING⟩ sets (13/19/19/22 open), walker-deep §10/§11 errata, AGENTS.md | `wc -l` + `sha256sum` + `grep -c PENDING` | owed — §5 |
| (a)(v) citations | SKILL.md `:1314` cites AUD-M9 as `7ad8eccdd8d213a5…`; landed `reports/r9-aud-m9.md` = `866272eeda09bc08` (166 L / 15,580 B) | `git show HEAD:<path> \| sha256sum` | **mismatch — finding F5** |
| (a)(vii) residual greps | README 8 rows / 21 notes → **13 unrowed**; SCORECARD rows 1–3 full, 4–10 stubs; LOG rounds 4–9 one-liners (round 7's full M7-1 paragraph `:297` excepted); `corpus/lessons/` **0**; walker-deep `0982ba066c72575a…` unchanged, round-7/9 errata still unappended; theme covering mutant owed (`gate-standing-use.md:199/:208/:264/:313`); five live rows exempted by name (4 matches in SKILL.md) | named commands per §6 | owed — §5 |

Ladder, battery, pin lineage, kill ladder: §2 **[O]**. Named sample of the
synthesis re-derived: all five arc-ledger gate rows (§2), the pin lineage,
and the invariants above; everything not re-run here is [OBS-record] with its
source (the synthesis's own tagging).

## 5. Terminal dispositions (round-11 attributed)

Final-round rule: "carried" does not exist — every item is named with its
state and where it lands.

**Closed [O]:** the round-10 handoff (a10/b10 verified at `f7bfc9f`; the
battery reproduced); the round-1 operability ceiling (the committed verdict
gate — landed at round 5 in `tools/mado-verify.sh`; the round-1 wording
`corpus/scripts/` is superseded by that path); the gate's own hardening,
regression mode, snapshot modes, and the 89→217→268 ladder (every row
re-verified this round, §2).

**Operator-owned:** the five live rows exempted by name (theme ×2,
walker ×3 — a seam decision, not the lane's; exemptions are counted); the
theme choice and every config edit; the omarchy checkout's cleanliness
(`git status`/`fetch` never run from this lane); the promotion decision
(SHONEN is 4/4 since round 5 — promotion is never self-declared); the live
waybar absence in this window (session weather; a live FAIL that survives
re-run is a finding about the session — §2).

**Unknown — named, with owner and why it stays so:** the record-family
items this round's settlement (b)/(c) is chartered to pay — README rows
(13 unrowed), SCORECARD 4–10 stubs and the missing final row, LOG
rounds 4–9 one-liners and the arc-end entry, `corpus/lessons/round-11.md`
(chartered with a `## Gate` section and a non-author spot-check, or the
refusal recorded as the arc's named failure), the ⟨PENDING⟩ closure blocks
(13 + 19 + 19 + 22), walker-deep §10/§11 errata, the theme clauses'
covering mutant (owner named by the gate's own re-cut record, `:1266-1268`),
the assertion-floor residue (the dead `row_from_rc` rc-6 arm, the usage
arms, `VERSION_STR` at `:77`, base-help discoverability) — each lands with
this round's settlement edits or the round records the failure; this note is
the ledger and cannot close them (write scope). The round-11 commit itself
lands after this write.

**Open findings (5), both values carried — append-only correction owed:**
**F1** the `…a5171` prose corruption — correct tail `c4c1afb75dd1c8aa…1a625171`
(`…5171`); still published in 34 places across 13 files, incl. the landed
`arc-synthesis.md:129/:167` and the round-10 record draft ×2 **[O]**. **F2**
`snapshot-diff-receipt-r9.md:33` reads `…db62` (the previous pin's tail);
the re-cut pin ends `…c0514cb6f8fd`; one occurrence, not propagated
**[OBS-record:** AUD-M10 §4**]**. **F3** `walker-deep-r9.md:296` says
"round 8 ended at 2,837 L"; round 8 is 2,887 L / 131,612 B; 2,837
reproduces nowhere, not propagated **[OBS-record:** AUD-M10 §4**]**. **F4**
the standing-use note's stale synthesis path (§3) **[O]**. **F5** the
`SKILL.md:1314` stale citation (§4) **[O]**.

## 6. Unknowns

- **The round-11 commit.** This note is written pre-commit; every row state
  above binds to `f7bfc9f`. The sibling SKILL-lane append (M11-4) was in
  flight at this read (`git status --porcelain` → ` M SKILL.md`, +122/−1;
  its own recheck line names the three shas) — the SKILL sha moves with it.
- **The record family's settlement.** Whether (b)/(c) pays §5's unknowns is
  outside this note; the final commit lands last and re-opens nothing quoted
  here.
- **Point samples.** Every live anchor is one host, one window, one session;
  a session restart invalidates the PIDs and the sockets' mtime marks it
  (`bb2639d9a980…` is the invariant, the live rows are not).
- **Historical suites.** The 28/53/89/217 counts are this lane's re-runs of
  the landed blobs on one toolchain (bash 5.3.15); another toolchain was
  not tested.
- **`.ufo/`** was not inspected this round; audit-lane verdicts remain in
  their records.

## 7. Falsifiable next-iterations (the handoff)

- If the gate moves: re-derive §2 whole — never quote this note's counts
  for a revision it does not name; re-cut pins from the measured table, not
  to match reality.
- If the theme clauses' covering mutant lands: the spec sha changes; re-derive
  the pin, the rate path and `PIN_MADO`.
- If the exempted live rows land: §5's exemption item closes by name; count
  it.
- Append-only: every correction above is an appended erratum — none of the
  records or notes is edited by this note.---

## 8. M11-3 — the gate's final-state receipt: selftest + live verdict + regression mode (2026-10-14)

Appended by the M11-3 lane; **§1–§7 above are the M11-1 note and are not
edited by this append**. Window 2026-10-14T21:33:40Z – 21:36:01Z (−03
18:33:40–18:36:01). Read-only: the gate was run, not edited; nothing outside
scratch `/tmp/w11-mado-m11-3/` was written by this lane; every run's stderr was
empty (0 B). The frozen revision re-bound here: `tools/mado-verify.sh` sha256
`93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`
(3,231 L / 150,103 B), byte-identical before and after the battery, at HEAD
`f7bfc9f`. Marks: **[O]** measured this window · **[I]** inference · **[U]** unknown.

The whole row re-run by this lane — every number below re-derives §2's battery
and agrees with it; where §2 and the landed bytes differ, they govern:

1. **Selftest [O]** — `MADO_SELFTEST: 268/268 assertions passed` rc 0
   (`/tmp/w11-mado-m11-3/selftest.out`): the recorded r9 count, cell-for-cell.
2. **`--no-live` [O]** — `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane
   only — live layer skipped: --no-live)`; counts `pass=29 fail=0 unknown=0 skip=8
   note=4`; the 8 SKIP rows named (`live.plane` + the seven `omarchy.*` live
   rows); 4 NOTEs; boundary `bb2639d9a980…` PASS; snapshot
   `MADO_SNAPSHOT: WRITTEN /tmp/w11-mado-m11-3/live-now.snap (rows=41 pass=29
   fail=0 unknown=0 skip=8 note=4; scope=file-plane)`.
3. **Live, today [O]** — `MADO_VERIFY: DIVERGED (3 fail, 0 unknown, 49 pass)`
   rc 1; counts `pass=49 fail=3 unknown=0 skip=0 note=8`; first fail
   `live.waybar.process (no waybar process)`; snapshot `MADO_SNAPSHOT: WRITTEN
   /tmp/w11-mado-m11-3/live-run.snap (rows=60 pass=49 fail=3 unknown=0 skip=0
   note=8; scope=live)`; boundary `bb2639d9a980…` PASS. §2's finding re-derived
   in this lane: `pgrep -fl waybar` → no match at 21:36Z; walker 1203471,
   elephant 1203474, swaybg 1203358 alive; `wayland-1` socket 0 B mtime 13:11:08
   (−03). Class unchanged from §2: a live-session move, not a gate defect and not
   a config drift; its terminal disposition rides the settlement (M11-2). This block
   appends the finding with both values and edits nothing.
4. **Regression [O]** — `MADO_REGRESSION: PASS (case=mado-verify-hardened;
   target=dc7c4141449891cdd83bb603aff7215358328a9ce1b32dba0bb9c0514cb6f8fd)`
   rc 0; `REGRESSION_DATE 2026-10-14T21:34:39Z`; `REGRESSION_TARGET` sha
   `dc7c4141…f8fd` match=yes (recorded pin); `REGRESSION_SPEC` sha
   `c7ee75b9…1dd8` (recorded pin matches); `REGRESSION_HARNESS` `75ed934d…`
   vs recorded `b56c6e57…` — provenance, not gated; `REGRESSION_BAND` all
   recorded kills required (10/10 KILLED, flips=0, inconclusive=0, control GREEN,
   `MUTATE_RESTORE: OK`, target sha unchanged); `REGRESSION_SWEEP` killed=10
   survived=0 inconclusive=0 kill-rate=100%; `REGRESSION_TABLE` match=10/10
   recorded-killed=10 measured-killed=10 flips=0; `REGRESSION_CASE` PASS
   (recorded table reproduced: control=green restore=ok); `REGRESSION_CLEANUP`
   removed=10; workdir removed on PASS.

**What this append adds beyond §2 [O]:** the snapshot pair worked example,
scratch only — `--snapshot-diff` on the two snapshots above →
`MADO_DIFF: CHANGED (rows 41→60; regressed=0 recovered=0 flipped=0 relaxed=0
relabeled=7 appeared=20 vanished=1; detail-changed=7; scope=1)`, the scope move
named (`file-plane → live`) and the class move (`fail 0→3`, the three waybar
rows); the control (a snapshot diffed with itself) → `MADO_DIFF: SAME (rows
41→41; all class counters 0; scope=0)` rc 0; and the gate sha byte-identical
before and after the whole battery (read-only proof). The gate revision did not
move this round: no re-cut or recalibration is owed from this lane.

**Carried note:** like §6, this append is pre-commit; the sibling SKILL-lane
append (M11-4) was still in flight at this read (`git status --porcelain` →
` M SKILL.md`; `plans/completion-evidence.md` untracked, another seat's). This
lane wrote only this append.

## Freshness pointer (round 19, 2026-10-20)

- The walker version pins in this note (lines 43) are dated 2026-10-14 (`verified-at`, line 12; §1 measurement) and describe walker 2.17.0. On 2026-10-20 the host package moved to 2.17.2: `/var/log/pacman.log:2929` (S090). Current routing: corpus/knowledge/walker-route-r18.md.
- Version-bound (dated, superseded for the host package): the `2.17.0` version print on line 43. No walker version pin is re-asserted here.
- Point sample, dated, not version-bound: "sockets `stat`'d 0 B, never connected" is a 2026-10-14 host-state observation, session-dependent, not re-measured this round.
- Version-bound behaviour: "no reload path — restart is the apply path" is a consumer-side reading against 2.17.0. walker-route-r18.md greps the v2.17.2 tag tree for `reload_config`/`set_config` in `src/` (source reading only); the 2.17.2 binary's live reload behaviour is [UNK].
- Other walker mentions (lines 152, 154, 187, 201: walker-deep notes; line 174: the exempted `walker ×3` live rows; line 264: the 2026-10-14 PID sample) are not walker version pins; none is re-asserted here, and none is affected by the host move to 2.17.2.
- Not re-measured live this round (host pause): behaviour of the 2.17.2 binary stays [UNK].