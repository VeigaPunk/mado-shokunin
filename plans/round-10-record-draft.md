# mado round-10 record — scribe prep DRAFT (SCR-M10)

Draft v1 window: 2026-10-14 20:50–20:58Z (local 17:50–17:58 −03:00). Lane SCR-M10.
This file is scribe scratch product for the round-10 finalizer — **not the record**.
Nothing outside this file was written by this lane in the repo; scratch
`/tmp/w10-scr-m10/` (`selftest.log`, `nolive.log`, `live.log`, `regression.log`,
`snap-a.log`, `snap-b.log`, `diff.log`, `pair-a.snap`, `pair-b.snap`,
`ids-live.txt`, `hist/` with the four historical gate copies + their logs).
All probes read-only: file reads, `wc`/`sha256sum`/`stat`/`grep`/`readlink`/`ls`,
the gate's own modes at the landed revision and on frozen historical copies,
`hyprctl` read verbs, `pgrep`, `busctl --user list`, `omarchy theme current`,
`/proc/<pid>` existence checks. No substrate file under `~/.config`/`~/.local`
written; no live session disturbed; no socket connected; no network command;
**no `git status`/`fetch` on the omarchy checkout** (none was needed; none ran).

Reading key: **⟨PENDING⟩** = must be resolved at finalization; every other
number names the command that produced it at v1 time. Tags: **[OBS]** measured,
**[INF]** inference from measured code/record, **[UNK]** unknown. Counts on
`.md` notes use `wc -l`; the gate's last line is unterminated (`exit 1`) —
3,231 by `wc -l` / 3,232 editor view (the round-7/8/9 idiom). Shas are cited
as measured prefixes (16 hex) unless noted.

## 0. Round-10 frame

- Plan: `plans/round-10.plan.md` — **committed in the round-9 landing**
  (`de22dfd`), 295 L by `wc -l` (296 editor view) / 19,322 B / sha
  `eca573b271e926e3…` (design lane PREP-M10, freeze 20:04Z at base `12c8f08`
  with round-9 work in flight). Axis move: **calibration + operability** — ONE
  move, three ordered stages: (a) the ten-round synthesis
  (`corpus/knowledge/ten-round-synthesis.md`, self-label M10-1; sections
  (i)–(vi): arc ledger, gate ladder, invariants, three trends, gap ledger,
  classification); (b) the gate's standing-use note
  (`corpus/knowledge/gate-standing-use.md`, self-label M10-2) plus the SKILL
  final append; (c) the record family (README, SCORECARD, LOG, lessons,
  walker-deep errata, AGENTS pointer). Plan lines: ordering `:224-236`,
  anti-claim `:238-252`, measure `:254-269`, draft unknowns `:271-289`, write
  scope `:291-296`.
- Final-round frame (as written, plan `:7-14`): the arc's last plan; the
  synthesis and the handoff are the charter; **a clause that did not land is a
  finding the synthesis records — round 10 does not re-attempt it**. See §6(c):
  a round-11 plan appeared in-flight, so "arc's last" describes this plan's
  lane, not the fleet.
- Ordering (plan `:224-236`): (a)/(b) consume the round-9 landed revision;
  (a9)/(b9)/(c9) resolved **at dispatch from the round-9 record, checked not
  assumed**; residual closures (help text, version string, exit-2 arms, rc-6,
  J/K/L) are not this round's claim — if one lands anyway it carries the full
  discipline (covering mutant, re-cut, `MADO_REGRESSION: PASS`, selftest count
  before → after) and is named in both (a) and (b); (c) rides (a)/(b); the
  final commit lands last and carries the arc-end statement.
- Anti-claim (as written, plan `:238-252`): the synthesis is a distillation,
  not a new measurement — every number carries its command and date at the
  landed revision; a number that cannot be re-derived is tagged [OBS-record]
  with its source or dropped, never recited; records are never rewritten;
  the standing-use note cannot upgrade the gate (NOTE stays non-verdict,
  UNKNOWN stays unknown, a stub scenario proves row logic never live values,
  the verdict stays `bash tools/mado-verify.sh`); no compositor/session
  mutation; substrates read-only; the tameshi harness and sibling repos are
  read-only; snapshots/receipts stay in scratch; the final round opens no new
  frontier; promotion is never self-declared.
- Measure (plan `:254-269`): synthesis landed (lines/bytes/sha; per-row
  command or source; classification counts); gate ladder re-derived per arc
  commit; standing-use note's mode map matches the landed `--help`/mode helps;
  residual ledger per item with its grep; final runs at the landed revision;
  record family before → after; boundary invariants quoted; three trend
  verdicts with evidence; operator channel.

### 0.1 The plan's design-time pins are superseded by the round-9 landing [OBS]

The plan froze 20:04Z **while round 9 was still writing** (round-9 commit
`de22dfd` landed 20:47:30Z). Every gate number in the plan reads at the
round-8 revision `12c8f08`. Landed values (re-measured at v1, §1.1/§1.2):

| plan says (round-8 base) | landed at `de22dfd` [OBS] |
|---|---|
| gate `7da4ec50…`, 2,887 L / 131,612 B | `93e43f8f…`, **3,231 L** / 150,103 B, mtime 17:05:32 −03:00 |
| selftest `217/217` | **`268/268`** |
| `--no-live` CLEAN (20 pass, 3 notes) | CLEAN (**29 pass, 4 notes**), `counts: pass=29 fail=0 unknown=0 skip=8 note=4` |
| live CLEAN (43 pass, 7 notes) | CLEAN (**52 pass, 8 notes**), `counts: pass=52 fail=0 unknown=0 skip=0 note=8` |
| census 162 `row` + 6 `row_from_rc`; 51 ids; seven plane ids; helper regexes seven ids `:357`/`:361`/`:376-380` | **189 `row` + 6 `row_from_rc` = 195 sites; 55 literal ids (60 distinct in a live run); eight plane ids** — omarchy 56 / hypr-live 51(+6 rc) / **theme 27** / hypr 23 / waybar 17 / terms 10 / gate 3 / walker 2; helper regexes **eight ids** `:387`/`:391`/`:406-410` |
| theme rows 0 (`live.theme.current` NOTE only) | theme plane 27 sites / 10 runtime rows; the two live theme rows **exempted by name**; `live.theme.current` NOTE `:2753`/`:2757` |
| walker live = `live.walker.version` + `live.walker.services` | unchanged: walker plane 2 row sites; `walker.sock` 0 hits |
| regression PASS target `d2bcdb31…db62` | PASS, target **`dc7c4141…f8fd`**; spec `c7ee75b9…1dd8` unchanged (finding, §0.2) |
| "selftest asserts 22 of 51" | **32 of 55 literal ids** (the +10 are the theme ids) |
| "no round-9 artifact committed at freeze" | round 9 landed: `de22dfd` (10 files, +2,571/−8) — file halves of (a) + (c), not (b) |
| debt: README 9 unrowed; lessons 0 | README still 8 rows (**11 notes unrowed**); lessons still 0 (**tenth** round) |

The record must cite landed values; any number copied from the plan
(2,887; 217; 20/3; 43/7; `d2bcdb31…`; "162"; "51") is a stale-base defect —
the same class rounds 7, 8 and 9 each recorded.

### 0.2 Round-9 clause resolution at dispatch [OBS — landed artifacts]

- **(a9) theme plane — FILE HALF LANDED; live half exempted by name.** Plane
  id `theme`, 27 `row theme` sites, scenarios T1–T9 (`:777-912`; T9 at `:905`),
  file-plane run emits 10 theme rows (9 PASS + `theme.parts.declared_only`
  NOTE). The plane comment (`:3002-3012`) states the scope verbatim: "the FILE
  rows only (the note's live rows, swaybg argv and the theme-name display
  agreement, are not landed here)". `theme.wallpaper.live` /
  `theme.name.display_agree`: `grep -c` → **0**. `theme.choice` stays the
  `live.theme.current` NOTE. VER-M9 PASS (file arm reproduced); AUD-M9 C1 PASS
  / C1b NOT LANDED.
- **(b9) walker live-surface rows — NOT LANDED.** `grep -c 'walker.sock'` → 0;
  walker plane still 2 row sites; `corpus/knowledge/walker-deep.md` sha
  `0982ba066c72575a…` **unchanged since round 7** — its §10 (`:521`) / §11
  (`:533`) errata append is still owed. `walker-deep-r9.md`
  (`a5acfe0162c9e5cd…`, 398 L) is M9-2's **new note**, not that append (do not
  conflate — SKILL `:1246` and AUD-M9 §2 both flag it).
- **(c9) census closure + receipts — PARTIAL, with a standing finding.** The
  helper regexes widened seven → eight ids; census re-run (189/55/60);
  selftest 217 → 268; PIN re-cut (`PIN_MADO` `:1290` = `dc7c4141…f8fd`);
  `MADO_REGRESSION: PASS` at the landed revision (my own run, §1.2). **But the
  recorded defect spec is byte-identical to round 8** (`c7ee75b9…`, 10
  defects) — "every widening carries its mutant" is **NOT met** at the landed
  revision; the theme clauses' only kill vehicles are the T1–T9 scenarios
  (AUD-M9 C4, finding, recorded not smoothed in SKILL `:1290-1300`). No
  survivor (`survived=0`).
- Record debt round 9 did **not** pay: README rows, SCORECARD stubs (one-liner
  added at `:21`), LOG one-liner (`:300`), walker-deep errata, lessons; the
  round-9 draft went to commit **with its D1–D5 slots unfilled** (19
  `⟨PENDING` mentions; last update v2c 20:10:28Z — 37 min before the commit).
- The T6-1 open unknown is resolved by the landed bytes: the round-9 re-cut
  case still PASSes (my run §1.2; AUD-M9 C4) and the authority target is
  `dc7c4141…f8fd`.

## 1. Pre-state at v1 (round 9 landed; round 10 in flight)

1. **Repo identity** [OBS, 20:51:34Z–20:57:56Z]: HEAD
   `de22dfdedc941563cc102781d3936cef9580e74b` ("probation round 9 (training
   r8): see LOG", 2026-10-14 17:47:30 −03:00 = 20:47:30Z); `git status
   --porcelain` **empty** at 20:51:34Z / 20:54:12Z / 20:55:26Z, then the
   in-flight set of §1.8. `git show --numstat HEAD` (10 files, +2,571/−8):
   LOG +1, SCORECARD +1, SKILL +240, `snapshot-diff-receipt-r9.md` +197,
   `walker-deep-r9.md` +399, `plans/round-10.plan.md` +296,
   `plans/round-9-record-draft.md` +778, `reports/r9-aud-m9.md` +167,
   `reports/r9-ver-m9.md` +140, `tools/mado-verify.sh` **+352/−8**.
   Pins (`wc -l` / bytes / sha256 prefix, all read at v1):
   `tools/mado-verify.sh` 3,231 L / 150,103 B / `93e43f8fe8b9bdd4…`;
   SKILL.md 1,336 L / 99,084 B / `946bf9d5e7f7fb1b…`;
   LOG.md 300 L / 22,712 B / `b6b5a4b226722421…`;
   SCORECARD.md 21 L / 9,198 B / `17fe5a4270698b08…`;
   `corpus/README.md` 19 L / 12,709 B / `2dd274f5e270e65b…` (**8 note rows**,
   byte-identical through rounds 5–9 — the r5–r8 drafts' freezes and the r9
   landing);
   `plans/round-10.plan.md` 295 L / 19,322 B / `eca573b271e926e3…`;
   `plans/round-9-record-draft.md` 777 L / 50,905 B / `f0e811c296194a9f…`
   (committed with its D1–D5 slots unfilled — `grep -c PENDING` → 19);
   `reports/r9-aud-m9.md` 166 L / 15,580 B / `866272eeda09bc08…`;
   `reports/r9-ver-m9.md` 139 L / 7,725 B / `98ec0c3b57a0d348…`;
   `corpus/knowledge/snapshot-diff-receipt-r9.md` 196 L / 12,701 B /
   `73b1466b6f876924…`; `corpus/knowledge/walker-deep-r9.md` 398 L / 24,391 B
   / `a5acfe0162c9e5cd…`;
   `corpus/knowledge/walker-deep.md` 617 L / 38,403 B / `0982ba066c72575a…`
   (**unchanged → §10/§11 errata still owed**);
   `corpus/knowledge/theme-wallpaper-plane.md` 394 L / 27,594 B /
   `8c578cc70e36506d…` (unchanged);
   `corpus/knowledge/walker-live-surface.md` 300 L / 19,203 B /
   `2bbb9609283f2d81…` (unchanged);
   `SHONEN.md` 12 L / 1,688 B / `edace65e13c8ad20…` (byte-identical since
   `c03c249` — 4/4 `[x]`, PROBATION COMPLETE; round-9 landing did not touch
   it); `PROVINCE.md` 18 L / `7aad7b863dc3c10b…`;
   `MINT.md` 20 L / `4408f66765729a44…`;
   `AGENTS.md` 6 L / 251 B / `66adcad6fd6cdd4b…` (no standing-note pointer
   yet — that is (c)); `corpus/QUALITY.md` 8 L / `1923c94f49788ade…`.
   `corpus/knowledge/` holds **19 committed notes** (+2 in flight, §1.8).
2. **Gate identity and runs** [OBS, my own runs 20:52:1x–20:53:15Z; logs
   `/tmp/w10-scr-m10/`]: `tools/mado-verify.sh` **3,231 L by `wc -l` (3,232
   editor) / 150,103 B / sha256
   `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`**,
   mtime 2026-10-14 17:05:32 −03:00; re-hashed identical after every run.
   - `--selftest` → `MADO_SELFTEST: 268/268 assertions passed`, rc 0;
   - `--no-live` → `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only —
     live layer skipped: --no-live)`, `counts: pass=29 fail=0 unknown=0
     skip=8 note=4`, rc 0; `gate boundary.readonly PASS config plane
     byte-identical before/after (combined sha bb2639d9a980…)`;
   - live → `MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes
     verified read-only)`, `counts: pass=52 fail=0 unknown=0 skip=0 note=8`,
     rc 0; same boundary row; waybar rows read `waybar pid 3501967` (§1.7 —
     the process is gone by 20:54:32Z);
   - `--regression` → **`MADO_REGRESSION: PASS (case=mado-verify-hardened;
     target=dc7c4141449891cdd83bb603aff7215358328a9ce1b32dba0bb9c0514cb6f8fd)`**,
     rc 0, `REGRESSION_DATE: 2026-10-14T20:52:59Z`;
     `REGRESSION_SPEC … c7ee75b97c38ac8f…1dd8 (recorded pin matches)`;
     `REGRESSION_TARGET … match=yes`; `REGRESSION_TABLE … match=10/10
     recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`;
     `REGRESSION_BAND: all recorded kills required … MUTATE_RESTORE OK`;
     `REGRESSION_CLEANUP: removed=10`; workdir
     `/tmp/mado-verify-regression.VeqhQp` removed on PASS;
     `REGRESSION_HARNESS … cf41efaa…242c75 (recorded revision b56c6e57… —
     provenance, not gated)`.
3. **Census and suite coverage (before round-10 edits)** [OBS, my commands]:
   `row ` call sites `grep -cE '^[[:space:]]*row [a-z-]+ '` → **189**;
   `row_from_rc` sites **6** (all hypr-live) → 195 total. By first-arg plane
   prefix (row only): **omarchy 56 / hypr-live 51 / theme 27 / hypr 23 /
   waybar 17 / terms 10 / gate 3 / walker 2** = 189; +6 rc → hypr-live 57
   combined [OBS]. **Distinct literal ids: 55**
   (`grep -oE '^ *(row|row_from_rc) [a-z-]+ [a-z0-9._-]+' … | awk '{print
   $NF}' | sort -u | wc -l`); **distinct ids in my live run: 60** (`awk
   'NF>=3 && $3 ~ /^(PASS|FAIL|UNKNOWN|SKIP|NOTE)$/ {print $2}' | sort -u` on
   `live.log` — the difference is the helper-emitted theme rows whose ids are
   not literal `row theme <id>` sites). **Asserted ids: 32 of 55/60** (union
   of `st_row_has`/`st_row_detail` targets). Among them exactly **one `live.*`
   id: `live.plane`** (asserted twice, `:930` SKIP arm / `:965` UNKNOWN arm) —
   the round-8 record's "0 of 21 hypr-live ids asserted" is at odds with this
   site; carry the measured form (1 of 21, via `live.plane`) and let the
   finalizer re-count at dispatch. Helper regex sites: **seven**
   (`:387`, `:391`, `:406-410`), alternation
   `(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate)` — eight ids.
   `theme` plane: 27 sites, 10 runtime ids; `walker.sock` 0;
   `wallpaper.live|display_agree` 0; `live.theme.current` `:2753`/`:2757`;
   `theme_plane()` `:3113`; `row_from_rc() {` `:116`; `VERSION_STR` `:77`;
   `mado_r8_usage_note()` `:1708`; block markers
   `:414-593` (R7 selftest), `:1041-1204` + `:1635-2157` (R8), `:1216-1634`
   (R7 regression); excisor `:1380-1382`; `PIN_MADO` `:1290`.
4. **The arc ladder, re-derived** [OBS — this lane, at v1]: `git show
   <commit>:tools/mado-verify.sh`:

   | round | commit | gate sha256 (prefix) | `wc -l` | selftest (my re-run) |
   |---|---|---|---|---|
   | 5 | `eead56b` | `d7edaab4bf108625…` | 1,098 | **28/28 rc 0** |
   | 6 | `c8f6667` | `c4c1afb75dd1c8aa…` | 1,186 | **53/53 rc 0** |
   | 7 | `0c20a76` | `90d50cdd4d18410b…` | 1,755 | **89/89 rc 0** |
   | 8 | `12c8f08` | `7da4ec5013583c91…` | 2,887 | **217/217 rc 0** |
   | 9 | `de22dfd` | `93e43f8fe8b9bdd4…` | 3,231 | **268/268 rc 0** |

   Rounds 1–4: **no gate file** (`git show <c>:tools/mado-verify.sh` → empty
   blob `e3b0c442…`, 0 L). Every historical revision still runs its selftest
   faithfully at dispatch (frozen copies in `/tmp/w10-scr-m10/hist/`, rc 0
   each) — no toolchain/fixture drift; the ladder's selftest column is
   first-hand, not recited.
   Kill ladder + pin lineage (for (a)(ii); receipts):
   round-5 revision `d7edaab4` **4/10 (40 %)** → `c4c1afb7` 10/10 →
   `90d50cdd` 10/10 → `7da4ec50` 10/10 → landed `93e43f8f` 10/10 (my run
   §1.2). The 4/10 and the ×3 receipts are **[OBS-record]**, quoted from
   `corpus/knowledge/gate-mutation-sweep-r8.md:49-50` ("Rate path for the same
   spec: round-5 revision `d7edaab4` **4/10 (40 %)** → hardened `c4c1afb7`
   **10/10 (100 %)** → live `90d50cdd` **10/10 (100 %)**") and
   `gate-mutation-proof.md:46`; the 10-defect table (D1–D9, R1) sits at
   `gate-mutation-sweep-r8.md:54-68`. Pin lineage: `c4c1afb7…a5171` (recorded
   target, round 7) → `d2bcdb31…db62` (round 8) → **`dc7c4141…f8fd`** (round
   9; `PIN_MADO` `:1290`, derived by the excisor `:1380-1382`).
5. **(c)-inputs and ready receipts** [OBS]: SKILL `:1099-1337` is the landed
   round-9 narrative (theme table, T1–T9 register, receipts, corrections,
   unknowns); the two round-9 notes and two reports are pins in §1.1; the
   snapshot receipt example is §3.4; the invocation map quotes are §3.1. The
   synthesis's classification (a)(vi) inputs: LOG `:294-300`, SCORECARD
   `:16-21`, the six drafts' `⟨PENDING` markers, reports r7–r9, and the
   round-10 plan's own debt list (`:87-93`).
6. **Record debt carried into round 10** [OBS, all still unpaid]:
   1. `corpus/README.md` — **8 note rows; 11 notes unrowed**:
      `idle-lock-plane.md` (r4), `province-accuracy-selfaudit.md` (r4/r5),
      `walker-deep.md` (r5), `gate-mutation-proof.md`,
      `omarchy-drift-watch.md`, `remaining-planes-census.md` (r6),
      `theme-wallpaper-plane.md`, `walker-live-surface.md` (r7),
      `gate-mutation-sweep-r8.md` (r8), `snapshot-diff-receipt-r9.md`,
      `walker-deep-r9.md` (r9). Ready row text: round-4 draft §4b `:300`,
      round-5 §4b `:276`, round-6 §4b `:258`, round-7 §4b `:321`, round-8 §4b
      `:435`; the two r9 notes have no ready row text (r9 draft §4b deferred).
   2. `SCORECARD.md:16-21` — rounds 4–9 are one-line stubs; full row text
      sits in the drafts (r4 §4c `:311`, r5 §4c `:287`, r6 §4c `:270`, r7 §4c
      `:335`, r8 §4c `:446`; r9 §4c `:490` is a template with ⟨fill⟩s).
   3. `LOG.md` — rounds 4–9 as one-liners (`:294`–`:300`); the only full
      entry is round 7 lane M7-1 at `:297`.
   4. Draft `⟨PENDING` markers, all unfilled as committed: r4 **5**, r5
      **3** (superseded by its own §10 `:477`), r6 **8**, r7 **13**, r8
      **19**, r9 **19** (`grep -c PENDING` each). Ready closure text exists:
      round-7 closure at r8 draft `:471-486` (D1 landed: gate
      `c4c1afb7…`→`90d50cdd…`, selftest 53→89, target `c4c1afb7…a5171`;
      D2/D3 not landed — notes only); round-8 closure at r9 draft §4f
      (`:515-539`; J/K/L not landed; omarchy landed; floor not landed; debt
      not repaid; lessons not landed). **Neither closure was ever applied** —
      append-only errata belong to (c). Round-9's own closure is §4f here.
   5. Errata: `walker-deep.md` §10 `:521` / §11 `:533` still owe
      `walker-live-surface.md` §5's ledger (file sha unchanged since round 7);
      `theme-wallpaper-plane.md` §10 (`:362`, append-only) is the theme-note
      errata route; no repo-level errata block exists.
   6. `corpus/lessons/` **0 entries** — tenth round of the round-1 promise;
      the plan's (c) charters `corpus/lessons/round-10.md` with a `## Gate`
      section and a **non-author** spot-check (≥1 admit, ≥1 reject; a lane's
      own subagent does not count — `LEARNING.md:38-43`) or the refusal
      recorded by name.
7. **Live pins** [OBS, point samples — session state can move under the
   round; see §6(e)]: same session since rounds 7/8/9 — sockets' mtime
   13:11:09 −03:00; walker **1203471** (`/usr/bin/walker
   --gapplication-service`), elephant **1203474**, swaybg **1203358**
   (`-i …/current/background -m fill`); `dev.benz.walker` owner 1203471
   (`busctl --user list`); sockets `/run/user/1000/walker/walker.sock` /
   `…/elephant/elephant.sock` type socket mode 755 size 0 (stat, never
   connected); `theme.name` = `matte-black`; `omarchy theme current` → `Matte
   Black`; `current/background` → `…/theme/backgrounds/0-ship-at-sea.jpg`;
   `mako/config` → `…/current/theme/mako.ini`; `~/.config/hypr/hyprland.conf`
   sha `4f52854a3c143dcf…`. **Waybar: pid 3501967 read by the gate's live
   rows at 20:52:36Z (Layer `DP-1 level 2 pid 3501967 3440x26`); `pgrep -ax
   waybar` → rc 1 at 20:54:32Z; `/proc/3501967` and `/proc/1203352` (r9's
   reading) both absent + no waybar layer surface at 20:57:56Z** — waybar
   exited mid-window (§6(e); cause [UNK]; no command from this lane touched it).
8. **Round-10 lane activity at v1** [OBS, shape-only]: `git status
   --porcelain` empty through 20:55:26Z; first artifacts appeared untracked:
   `corpus/knowledge/arc-synthesis.md` (386 L / 30,756 B /
   `b118c6722b90abb6…`, mtime 17:56:41 −03:00 — self-label "Arc synthesis —
   mado's ten rounds, re-derivable (M10-1, round 10)"; **note the filename is
   NOT the plan's `ten-round-synthesis.md`**), `corpus/knowledge/
   gate-standing-use.md` (327 L / 21,004 B / `7f61d87da50b48a5…`, mtime
   17:56:26 −03:00; self-label "The gate's standing-use note" and its `source:`
   cites `93e43f8f…`), and `plans/round-11.plan.md` (349 L / 23,290 B, mtime
   17:57:43 −03:00; "WWKD plan — mado round 11 … — the closeout round",
   design lane PREP-M11, freeze 20:56Z). All three are **in flight**, not
   landed; the gate sha is unchanged. Details in §10 (v2a).

## 2. Deliverables and ⟨PENDING⟩ slots

### D1 (a) — the ten-round synthesis ⟨PENDING⟩

Sections (i)–(vi) per the plan `:120-157`. Ready scaffolding: §3.2 (ladder,
kill/pin lineage), §1.1 (pins), §1.6 (debt movement), §0.2 (round-9 clause
resolution), §3.3 (residual ledger → (a)(iv)/(vi) and (b)(vi)). Hard rules
repeated for the writer: every number carries the command that produced it at
the landed revision; a number that cannot be re-derived is tagged
**[OBS-record]** with its source line, or dropped; the synthesis cites records
and landed artifacts, never design-time plan numbers except where a record
cites them. The one already-measured divergence to reconcile: the landed file
name (`arc-synthesis.md` at v1) vs the plan's (`ten-round-synthesis.md`).
⟨PENDING: landed filename; lines/bytes/sha; each of (i)–(vi) present with its
measurements; classification counts per class (closed / operator-owned /
unknown) with every item named; the [OBS-record]-tagged values list; the three
trend verdicts with evidence lines.⟩

### D2 (b) — the gate's standing-use note + SKILL final append ⟨PENDING⟩

Substance per the plan `:158-198`. Ready quotes and tables: §3.1 (invocation
map, verdict vocabulary, cadence material), §3.3 (residual/limit ledger),
§3.4 (receipt example), §1.2 (receipt lines at the landed revision). The note
must **not** upgrade the gate: NOTE stays non-verdict, UNKNOWN stays unknown,
stub scenarios prove row logic never live values.
⟨PENDING: landed file sha (in-flight `7f61d87d…` at v1); the SKILL append's
location/sha; the residual ledger per item with the grep that shows open/closed
at dispatch; the quick invocation table; the harness read-only boundary line
(tameshi stays a recommendation, never a patch).⟩

### D3 (c) — the record family ⟨PENDING⟩

Items and before-values: README 8 rows → 8+N (11 + round-10's notes; a
`## Known gaps` section from (a)(v)); SCORECARD `:16-21` stubs replaced from
the drafts (ready-text refs in §1.6.2) + rounds 8–10 rows + a final row naming
the standing gate revision and the synthesis; LOG final entry (§4a) with the
arc-end statement (probation 4/4 `[x]` since round 5; promotion is the
operator/gate decision, never self-declared); `corpus/lessons/round-10.md` or
the recorded refusal; `walker-deep.md` §10/§11 errata if round 9's equivalent
did not land (§4g); the round-7/8/9 draft closures as appended errata (§4f,
§4g); AGENTS.md one pointer line (§4e). Every pin re-measured at apply time.
⟨PENDING: which items land; README 8 → ?; SCORECARD 21 L → ?; lessons 0 → 1
or refusal; walker-deep sha `0982ba06…` → ?; AGENTS `66adcad6…` → ?; LOG 300 L
→ ?; drafts' markers 13/19/19 → appended closures or named as never-closed.⟩

### D4 — classification + operator handoff ⟨PENDING⟩

Every open item from round records 1–9 (and round 9's resolution) classified
**closed (evidence) / operator-owned (named) / unknown (named)**; "carried"
does not exist in the final round (plan `:149-153`). Source universe: §1.6 +
§3.3 + the drafts' markers + reports r7–r9 + the operator channel.
⟨PENDING: the class counts; the operator-owned list; the unknown list; the
operator channel reading at dispatch (0 `mado` lines at v1 — a mid-round
filing is named, never answered here).⟩

### D5 — residual closures, named never claimed ⟨PENDING⟩

The plan's own list: the help text, the version string, the exit-2 arms,
rc-6, J/K/L (+ the theme-clause mutant gap found at landing, §0.2). If any
lands, it carries the full discipline (covering mutant, re-cut,
`MADO_REGRESSION: PASS`, selftest before → after) and is named in both (a)
and (b); whatever stays open ships named in (b)(vi) and the operator handoff.
⟨PENDING: open|closed per item with the evidence; if any closure lands, its
receipts and the before → after counts.⟩

### D6 — round-9 draft closure (appended erratum, never an edit)

The committed `plans/round-9-record-draft.md` keeps its D1–D5 slots unfilled
(§1.6.4). §4f carries the measured fill for an appended closure block in the
round-10 commit — the same route rounds 8 and 9 owed for their predecessors
and never applied.

## 3. Ready tables

### 3.1 Invocation map — quoted at the landed revision (for (b)(ii))

Base `--help` (`bash tools/mado-verify.sh --help`, rc 0; source `:86-97`):

```
usage: mado-verify.sh [--no-live] [--live] [--root DIR] [--selftest] [--help]

  (default)     live read-only run against $HOME (or MADO_VERIFY_ROOT)
  --no-live     file plane only; the verdict names the skipped live layer
  --root DIR    verify DIR as the config root (default $HOME)
  --selftest    hermetic fixture tests under /tmp/w5-mado-m52-* (no substrate)
  --help        this text

verdict: MADO_VERIFY: CLEAN|DIVERGED (...)   exit 0 / 1  (usage error: 2)
env: MADO_VERIFY_ROOT (config root), MADO_VERIFY_LIVE=auto|yes|no
```

The base help **omits `--regression`, `--snapshot`, `--snapshot-diff`** (and
`MADO_VERIFY_HARNESS`); the mode helps print them (`mado_r8_usage_note()`
`:1708`; regression help `:1604-1607`) — this is the discoverability residual
(§3.3), five rounds old, stated plainly in the standing-use note.

`--snapshot --help` / `--snapshot-diff --help` (rc 0; quoted):

```
  --snapshot FILE   run the gate (honouring --no-live/--live/--root) and write
                a v1 verdict snapshot to FILE (FILE must not exist; receipts
                are never overwritten). Exit = the run's verdict; the write
                adds MADO_SNAPSHOT: WRITTEN|REFUSED (a refusal exits 2).
  --snapshot-diff OLD NEW  diff two snapshots class by class; MADO_DIFF:
                SAME|DETAIL-CHANGED|CHANGED|SETUP (exit 0/0/1/2). Reads only
                the two files; never prints MADO_VERIFY:.
```

`--regression --help` (rc 0; quoted):

```
  --regression  replay the recorded mutation case (tameshi T6-1 spec at
                pinned bytes over the recorded gate revision); --keep
                retains the scratch root also on PASS. No substrate read.
```

Env: `MADO_VERIFY_ROOT` (config root; `:78`), `MADO_VERIFY_LIVE=auto|yes|no`
(`:79`; a bad value is a usage error `:3185`), `MADO_VERIFY_HARNESS` (regression
harness path, `:1505`). Exit map (`:13`): 0 verified · 1 unverifiable/diverged
· 2 tool/usage error. Verdict vocabulary, all re-quoted from my runs at the
landed revision: `MADO_VERIFY: CLEAN|DIVERGED`; `MADO_SELFTEST: N/N assertions
passed` (or `FAILED`); `MADO_REGRESSION: PASS|FAIL|SETUP`; `MADO_SNAPSHOT:
WRITTEN|REFUSED`; `MADO_DIFF: SAME|DETAIL-CHANGED|CHANGED|SETUP`; row classes
PASS/FAIL/UNKNOWN/SKIP/NOTE — UNKNOWN never CLEAN (selftest arms B/C/E/I), NOTE
never flips the verdict (both verdict runs carry notes with CLEAN).

### 3.2 Arc ladder + kill/pin lineage (for (a)(i)/(ii))

Table as §1.4; add per round the axis move and record-debt movement from LOG
`:294-300` and SCORECARD `:16-21` (the finalizer fills the columns from the
records; the gate/selftest columns above are first-hand). Verifying seats as
the records name them: r4 VER-M3 | VER-M4; r5 VER-M4B (box-4 closure); r6
VER-M6 | AUD-M6; r7 VER-M7 | AUD-M7; r8 VER-M8 | AUD-M8; r9 VER-M9 | AUD-M9
(LOG lines; reports in `reports/`). Rounds 1–3: scribe re-verification runs
(MADO-SCRIBE, MADO-B4 — LOG). Judge/verdict rule text (`LEARNING.md:27-35`;
axes `AXES.md`). The three trends' evidence lives in §1.6 (expansion: notes
3 → 19 admitted; quality: re-verifications + the gate ladder; discernment:
AUD/VER verdicts vs the gate — the r9 spec gap is the harm-side fact to name).

### 3.3 Residual ledger (open/closed at `93e43f8f`) — for (b)(vi)

| residual | state at v1 [OBS] | command |
|---|---|---|
| `VERSION_STR` still "v1 … round 5 / M5-2" | OPEN (`:77`; now also in every snapshot's `tool=` line) | `grep -n 'VERSION_STR=' tools/mado-verify.sh` |
| base `--help` omits the three modes | OPEN (quoted §3.1) | `bash tools/mado-verify.sh --help` |
| rc-6 arm of `row_from_rc` (6 → UNKNOWN) | OPEN — mapped, no white-box pin, no test | `sed -n '116,122p' tools/mado-verify.sh` |
| bad `MADO_VERIFY_LIVE` usage arm | behaviour exists, **unasserted** | `grep -n 'must be auto' tools/mado-verify.sh` (`:3185` only) |
| `--root` with no value usage arm | behaviour exists (`:1748`), unasserted (the suite asserts snapshot/diff arms only) | `grep -n 'usage error: --root' tools/mado-verify.sh` |
| boundary combined-hash prefix in the `sha_pin`/boundary detail | unasserted (detail prints `${before:0:12}` `:2476`; assertions `:927`/`:1038` do not pin the value) | `sed -n '2470,2482p' tools/mado-verify.sh` |
| hypr-live stub scenarios J/K/L | OPEN — no `hyprctl` PATH stub (`grep -cE 'STUB_HYPR|stub_hypr|scenario J…'` → 0) | that grep |
| walker live-surface rows (sockets / D-Bus owner / layer invariant) | OPEN — 0 sites; walker plane 2 sites; measured-only in `walker-live-surface.md` | `grep -c 'walker.sock' tools/mado-verify.sh` |
| theme live rows | **exempted by name** (plane comment `:3002-3012`) | `grep -c 'wallpaper.live\|display_agree' tools/mado-verify.sh` |
| theme-clause covering mutant | **FINDING** — spec byte-identical `c7ee75b9…` (10 defects); T1–T9 are the only kill vehicles | `REGRESSION_SPEC` line vs `git show 0c20a76:tools/mado-verify.sh` heredoc |

### 3.4 Snapshot pair worked example (scratch, never committed)

My run, `--no-live` pairs on the real root (`/tmp/w10-scr-m10/`):

```
MADO_SNAPSHOT: WRITTEN /tmp/w10-scr-m10/pair-a.snap (rows=41 pass=29 fail=0 unknown=0 skip=8 note=4; scope=file-plane)
MADO_SNAPSHOT: WRITTEN /tmp/w10-scr-m10/pair-b.snap (same counts)
MADO_DIFF: SAME (rows 41→41; regressed=0 recovered=0 flipped=0 relaxed=0 relabeled=0 appeared=0 vanished=0; detail-changed=0; scope=0)
```

receipt header: `# mado-verify snapshot v1`, `created: 2026-10-14T20:55:09Z`,
`tool: mado-verify.sh v1 (mado-shokunin round 5 / M5-2)`, `gate-sha256:
93e43f8f…`, `root: /home/vgpnk`, `scope: file-plane`. (The round-9 landing
receipt — `CHANGED, appeared=10` — is quoted in `snapshot-diff-receipt-r9.md`
and AUD-M9; cite the note, do not re-run history.)

## 4. Record text to apply

### 4a. LOG.md round-10 entry (append after `LOG.md:300`)

```
- 2026-10-14 — round 10 (training r9): the ten-round synthesis ⟨fill: file,
  L/B/sha; the ladder re-derived; classification counts⟩; the gate's
  standing-use note ⟨fill: file, L/B/sha; invocation map quoted; the residual
  ledger: open/closed per item⟩; the record family ⟨fill: README 8 → ? rows;
  SCORECARD stubs r4–r9 replaced from the drafts (r9 filled) + round 10 +
  final row; LOG arc-end
  statement; corpus/lessons/round-10.md ⟨landed|refused, reason + seat⟩;
  walker-deep §10/§11 errata ⟨sha before → after⟩; round-7/8/9 draft closures
  as appended errata; AGENTS.md pointer⟩. Gate revision `93e43f8f…` unchanged
  ⟨| moved + receipts⟩; selftest 268/268; `--no-live` CLEAN (29 pass, 4
  notes); live CLEAN ⟨fill: 52 pass, 8 notes at v1 — re-run at the commit⟩;
  regression PASS target `dc7c4141…`; spec `c7ee75b9…` ⟨unchanged — finding⟩.
  Boundary: gate + notes + substrate read-only; no substrate file written; no
  live session disturbed; no socket connected; no `git status` on the
  checkout. Probation 4/4 `[x]` since round 5; promotion is the operator/gate
  decision, never self-declared.
```

### 4b. `corpus/README.md` — coverage map rows

Apply the 11 carried rows in order (§1.6.1 refs), **re-measure every pin at
apply time**, then one row per round-10 note as landed ⟨PENDING⟩, then a
`## Known gaps` section from (a)(v). Row count before → after: **8 → 8+N**.
⟨PENDING: N; the round-10 note rows (write from the measured artifacts, never
from this draft); the Known-gaps text.⟩

### 4c. `SCORECARD.md` — move-log rows

Replace the stubs `:16-21` with the committed full rows (sources §1.6.2),
add the round-9 full row from the r9 draft §4c template (filled from the
landed bytes, §0.2), then round 10:

```
| 10 | calibration + operability | round-9 state: no arc synthesis existed; the gate's limits lived across nine records; README/SCORECARD/lessons debt six rounds deep | the ten-round synthesis ⟨fill: file, classification counts⟩; the standing-use note ⟨fill: mode map + residual ledger⟩ | ⟨fill: receipts; gate 93e43f8f… ⟨unchanged|moved⟩; selftest 268/268; verdicts; scratch /tmp/w10-scr-m10/⟩ |
```

plus the final row naming the standing gate revision and the synthesis
⟨fill⟩. Before → after: 21 L → ?.

### 4d. SHONEN.md

No box move expected: 4/4 `[x]` since round 5; promotion is the
operator/integrator decision, never self-declared. Byte-identical at
`edace65e13c8ad20…` unless the finalizer edits an evidence line — if edited,
re-apply the seed check (`PROTOCOL.md:419-431`).

### 4e. AGENTS.md — one appended pointer line (plan (c))

```
Standing rules: the gate's custody, invocation map and residual ledger live
in `corpus/knowledge/gate-standing-use.md`.
```

⟨PENDING: landed line + sha of AGENTS.md before (`66adcad6fd6cdd4b…`) → after.⟩

### 4f. Round-9 draft closure (appended erratum, never an edit)

The measured fill for `plans/round-9-record-draft.md`'s unfilled slots (D1
`:326`, D2 `:349`, D3 `:368`, D4 `:377`, D5 `:386`), from the landed bytes:

- D1 (a) — **landed as the file-plane arm**: plane id `theme`, 10 file rows
  (9 PASS + `theme.parts.declared_only` NOTE), 27 row sites, scenarios T1–T9
  (`:777-912`); the two live rows **exempted by name** (`theme.wallpaper.live`,
  `theme.name.display_agree`; plane comment `:3002-3012`); gate `7da4ec50…` →
  `93e43f8f…` (numstat +352/−8; 2,887 → 3,231 L by `wc -l`); selftest **217 → 268**; asserted ids
  **22 → 32**; regexes seven → eight ids; `MADO_REGRESSION: PASS` target
  `dc7c4141…` (receipt §1.2); VER-M9 PASS; AUD-M9 C1 PASS / C1b NOT LANDED.
- D2 (b) — **not landed**: `walker.sock` 0 hits; walker plane still 2 row
  sites; `walker-deep.md` sha `0982ba06…` unchanged (its §10/§11 append still
  owed); `walker-deep-r9.md` is M9-2's new note, not the append.
- D3 (c) — **partial**: regex widening + census + re-cut receipt landed
  (189 sites / 55 literal ids / 60 runtime; `PIN_MADO` `:1290` = `dc7c4141…`;
  table `match=10/10 flips=0`; `MUTATE_RESTORE: OK`; no survivors). **The
  defect spec was not extended** (`c7ee75b9…` byte-identical; no covering
  mutant for the theme clauses — AUD-M9 C4 finding); the "every widening
  carries its mutant" clause is NOT met at the landed revision.
- D4 — record debt **not repaid** (README 8 rows; SCORECARD `:21` one-line;
  LOG `:300` one-line; walker-deep errata owed; round-8 draft 19 markers
  unfilled).
- D5 — `corpus/lessons/round-9.md` **not landed** (`corpus/lessons/` 0
  entries; no independent seat recorded).

### 4g. Further append-only closures owed by (c)

- `walker-deep.md` §10 (`:521`) / §11 (`:533`) errata append — substance =
  `walker-live-surface.md` §5's ledger; append under its `Errata (append-only)`
  (`:615`) section; sha before `0982ba066c72575a…` → after ⟨PENDING⟩.
- Round-7 closure text (r8 draft `:471-486`) and round-8 closure text (r9
  draft §4f `:515-539`) — append as closure blocks (their own drafts, appended
  erratum) if the finalizer closes them this round; otherwise classify them
  under D4 as never-closed.
- `reports/r9-aud-m9.md` sha note: SKILL `:1313-1314` quotes
  `7ad8eccdd8d213a5…`; the committed report measures
  `866272eeda09bc08…` ([OBS] both; the quote is a pre-final revision). The
  standing text should carry the committed sha, or an erratum should name the
  drift. (VER-M9's quoted sha matches its committed file.)

## 5. Scribe measurements and spot-checks (executed)

1. **Gate runs at the landed revision** (read-only, 20:52:1x–20:53:15Z; logs
   `/tmp/w10-scr-m10/`): `--selftest` → 268/268 rc 0; `--no-live` → CLEAN
   (29 pass, 4 notes) rc 0; live → CLEAN (52 pass, 8 notes) rc 0;
   `--regression` → PASS rc 0, target `dc7c4141…`, spec `c7ee75b9…`, table
   `match=10/10 flips=0`, cleanup `removed=10`, workdir removed on PASS. Gate
   sha identical before and after every run (§1.2).
2. **Ladder re-derivation + historical selftests** (§1.4): five blobs
   re-hashed from git; each selftest re-run on a frozen copy — `28/28`,
   `53/53`, `89/89`, `217/217`, `268/268`, rc 0 each. Rounds 1–4 have no gate
   file. **First-hand, not recited.**
3. **Census + coverage** (§1.3): 189 `row` + 6 `row_from_rc`; per-plane
   omarchy 56 / hypr-live 51 / theme 27 / hypr 23 / waybar 17 / terms 10 /
   gate 3 / walker 2; 55 literal ids / 60 runtime in the live log; asserted
   32, incl. exactly one `live.*` (`live.plane`, `:930`/`:965`); helper regex
   seven sites / eight ids; `walker.sock` 0; two theme live ids 0.
4. **Receipts + examples**: snapshot pair → `MADO_DIFF: SAME` rc 0 (§3.4);
   mode helps quoted with rc 0 (§3.1); boundary combined sha `bb2639d9a980…`
   in both verdict runs; config-plane file `hyprland.conf`
   `4f52854a3c143dcf…` read directly.
5. **Live pins + the waybar timeline** (§1.7, §6(e)): walker 1203471 /
   elephant 1203474 / swaybg 1203358 unchanged; waybar 3501967 at 20:52:36Z →
   gone by 20:54:32Z (`pgrep -ax waybar` rc 1; no `/proc` entry; no layer
   surface at 20:57:56Z). Sockets stat'd, never connected. No substrate file
   written; cause of the waybar exit [UNK].
6. **Boundary**: writes = this draft + `/tmp/w10-scr-m10/` only; no substrate
   file written; no live session disturbed (reads only); no socket connected;
   no network command; no `git status`/`fetch` on the omarchy checkout.

## 6. Observations (v1)

(a) The plan's design-time base is the **round-8** revision (frozen 20:04Z
    while round 9 was writing; round 9 landed 20:47:30Z) — every gate number
    it carries is superseded (§0.1). The finalizer must not copy "2,887",
    "217", "20 pass", "43 pass", "162", "51", or `d2bcdb31…` into the record
    without the landed re-measure — the same stale-base class rounds 7/8/9
    recorded. The plan's own ordering clause anticipated this for (a)/(b);
    the debt table also moved (9 → 11 unrowed notes).
(b) **Filename divergence, already visible**: the plan's (a) names
    `corpus/knowledge/ten-round-synthesis.md`; the in-flight artifact is
    `corpus/knowledge/arc-synthesis.md` (self-label M10-1 correct). The
    record must reconcile by name at the commit — either the landed name is
    the record's, or the divergence is a finding. Same watch for (b):
    `gate-standing-use.md` matches so far.
(c) **The "final-round" frame is contradicted in-flight**: `plans/
    round-11.plan.md` ("the closeout round", PREP-M11, freeze 20:56Z) appeared
    at 20:57:43Z, 1 minute after the round-10 synthesis started landing. The
    ten-round synthesis remains the round-10 charter (rounds 1–10), but the
    record **must not describe the fleet or the arc as ended at round 10**
    ("no round-11 plan follows from this lane" is true of PREP-M10 only).
(d) The round-9 landing left a structural gap that bears on (a)(iv)/(vi) and
    (b)(vi): the theme clauses' only kill vehicles are T1–T9; the mutation
    spec was not extended (AUD-M9 C4). A future widening rule statement must
    carry this as an open finding, not a promise.
(e) **Live-state movement in-window**: waybar (pid 3501967 at 20:52:36Z, and
    already restarted once since round 9's 1203352 reading) **exited between
    20:52:36Z and 20:54:32Z**. Cause [UNK]; no command from this lane touched
    the session (this lane's probes are reads; the gate's live mode is read-only).
    The live verdict *now* would read FAIL on the waybar rows if it is still
    down (`live.waybar.process` / `.layer` / `.tray`), i.e. session state, not
    gate state. The config-plane boundary hash is unaffected (`bb2639d9a980…`
    covers files). The finalizer re-measures at dispatch and records the
    reading with its clock; a MOVED pin is reported first, never smoothed.
(f) Record debt is now six drafts deep (5/3/8/13/19/19 markers) plus the
    lessons ledger at 0 for ten rounds; (c) is the only stage that can close
    any of it, and only what it actually applies. §4 carries ready text; every
    closure must be append-only.
(g) A stale sha sits in standing text: SKILL `:1314` quotes AUD-M9 as
    `7ad8eccdd8d213a5…`; the committed report is `866272eeda09bc08…` (both
    measured). The final round either cites the committed sha or appends an
    erratum naming the drift.
(h) The round-9 draft's window closed at v2c (20:10:28Z), 37 minutes before
    its commit; the draft is not the record — the landed record text for round
    9 lives in SKILL `:1099-1337` and the two reports. Same caution for this
    file: **this draft is not the round-10 record**; the finalizer re-runs the
    §9 checklist from the landed revision, never from these numbers.

## 7. Unknowns (v1)

1. Whether (a)/(b)/(c) land in-window and at which gate revision; the landed
   filenames (one already diverges, §6(b)); whether the round's own edits
   touch the gate at all (the plan claims none).
2. Whether any residual closure lands (help text, version string, rc-6,
   exit-2 arms, J/K/L, the theme-clause mutant) and under which discipline
   receipts.
3. Whether the record family repays any of the six-round debt: README rows,
   SCORECARD full rows, lessons entry (and who sits as its non-author seat),
   walker-deep errata, draft closures; or defers again, named.
4. Whether the gate stays at `93e43f8f…` through the round — every v1 number
   here binds to that sha; the finalizer re-pins from the commit.
5. Whether the waybar exit is permanent or transient at dispatch; the live
   verdict at the commit depends on it (§6(e)).
6. Which lanes attest round 10 (AUD/VER labels, report files) and their
   self-labels — record by artifact self-label.
7. Whether the synthesis's per-round verdict counts for rounds 5–7 can be
   re-derived first-hand or must be tagged [OBS-record] (the selftest ladder
   is first-hand; the verdict counts are in the records only).
8. Whether the operator files a mado entry mid-round (0 at v1; `.ufo/
   l0-questions.md` grep -ci mado → 0, shape-only) — a filing is named, never
   answered in the record.
9. Whether round-11's plan changes round 10's record contract (it postdates
   the round-10 plan's freeze; §6(c)) — the round-10 record covers rounds
   1–10 as chartered.

## 8. Falsifiable next-iterations (carry + new)

- Land (a) with every ledger cell carrying its command or [OBS-record] source
  line; reconcile the filename (§6(b)); three trend verdicts with evidence.
- Land (b) with the invocation map quoted from the landed helps and the
  residual ledger re-grepped per item; never upgrade a residual into a
  promise; keep the harness read-only boundary a recommendation.
- Land (c) append-only: README rows re-measured; SCORECARD full rows from the
  drafts; LOG entry with commands; lessons entry or recorded refusal; errata
  appends measured by sha before → after.
- Carry the round-9 spec-mutant gap as a named finding in (a)/(b) — no
  smoothing; state the T1–T9-kill-vehicles situation.
- Record the live-state reading at the commit with its clock (waybar) and the
  boundary hash before/after; report a MOVED pin first.
- Durability: fold receipt lines + tool/target/spec/harness shas + gate sha
  into the record (scratch does not survive; the audit's kept workdirs are
  ephemeral).
- If the round is cut short: leave this draft as the record's ancestry with
  its v2 trailer stating what was verified and what was not.

## 9. Finalization checklist (mechanical, ordered)

1. Re-measure §1.1/§1.2 anchors at the commit; note drift as freshness rows;
   re-run the three verify modes and `--regression` at the revision being
   committed; re-check the gate sha is `93e43f8f…` (or record the move + its
   full discipline).
2. Read the landed (a)/(b) files; verify every quoted mode help against the
   landed gate; verify the residual ledger per §3.3's greps, quoted
   open/closed.
3. Verify the record-family applies: README 8 → N rows with re-measured pins;
   SCORECARD rows; lessons file or refusal; walker-deep sha before → after;
   AGENTS line; appends only.
4. Confirm the classification covers every open item (no "carried"); count
   per class; name the operator-owned items.
5. Quote the boundary invariants before/after every run (gate sha; config
   combined hash `bb2639d9a980…`).
6. Apply §4a (LOG), §4b (README), §4c (SCORECARD), §4d (SHONEN — likely
   no-op), §4e (AGENTS), §4f (round-9 closure), §4g (errata + further
   closures as applicable).
7. Commit under the lane identity; freeze every cited sha in the entry; check
   the gate/harness/note shas appear; confirm no `git status` ran on the
   omarchy checkout during the round.
8. If any clause does not land: record it as never landed, by name, with its
   owner — the final round names gaps; it does not re-attempt them.

## 10. v2 updates (append as artifacts land)

**v1 cut (20:58Z): round 9 landed and green; round-10 work appearing but
nothing from round 10 is in this draft's numbers.** `git status --porcelain`
empty at 20:51:34Z / 20:54:12Z / 20:55:26Z; gate sha `93e43f8f…` unchanged
through every poll and run; first round-10 artifacts untracked from 20:56:24Z
(§1.8). This file is this lane's only write. Poll targets for the finalizer:
`sha256sum tools/mado-verify.sh` (≠ `93e43f8f…` means a gate move),
`git status --porcelain`, `ls corpus/knowledge/` (arc-synthesis vs
ten-round-synthesis naming), `ls corpus/lessons/`, `grep -c PENDING plans/
round-9-record-draft.md`, `bash tools/mado-verify.sh --selftest` (>268),
`pgrep -ax waybar` (live state).

**v2a (20:56:24Z–20:57:56Z): the round-10 artifacts are landing — read
shape-only, in flight, not landed.** All readings below are [OBS] at their
clocks; another lane's single-writer work; this scribe lane read it, never
touched it.
- `corpus/knowledge/arc-synthesis.md` — 386 L / 30,756 B /
  `b118c6722b90abb6…`, mtime 17:56:41 −03:00; self-label "Arc synthesis —
  mado's ten rounds, re-derivable (M10-1, round 10)"; its `source:` line cites
  the arc commits `74d3b7b`…`de22dfd`, the gate and the 19 notes. **Filename
  ≠ the plan's `ten-round-synthesis.md`** (§6(b)).
- `corpus/knowledge/gate-standing-use.md` — 327 L / 21,004 B /
  `7f61d87da50b48a5…`, mtime 17:56:26 −03:00; `source:` cites the gate at
  `93e43f8f…` (the landed sha).
- `plans/round-11.plan.md` — 349 L / 23,290 B, mtime 17:57:43 −03:00; "WWKD
  plan — mado round 11 … — the closeout round", design lane PREP-M11, freeze
  20:56Z — the round-10 plan's "final-round" frame is a lane-scoped statement
  (§6(c)).
- No commit; the gate sha is unchanged; `corpus/lessons/` still 0; README
  still 8 rows; the live-state reading (§6(e)) is the only substrate movement
  observed.

**v2b (20:59:52Z–21:01:13Z): the in-flight artifacts kept moving; the gate did
not.** Polls (all [OBS] at their clocks; untracked, in flight, **not landed**):
- `corpus/knowledge/arc-synthesis.md` — 386 → **387 L** / 30,796 B / sha
  `b118c6722b90abb6…` → **`a5b4833141461810…`**, mtime 17:57:22 −03:00
  (still evolving);
- `corpus/knowledge/gate-standing-use.md` — 327 → **361 L** / 22,931 B /
  `7f61d87d…` → **`aaa2e625253e881e…`**, mtime 17:58:01 −03:00;
- `plans/round-11.plan.md` — 349 → **352 L** / 23,438 B /
  **`4bde28aa5eef9600…`**, mtime 17:58:18 −03:00.
- `tools/mado-verify.sh` sha **unchanged** `93e43f8f…` at every poll
  (20:56:24Z–21:01:13Z); `corpus/knowledge/` 21 entries (19 committed + the
  two in flight); `corpus/lessons/` still 0; README still 8 rows; no commit.
- Consequence: every v2 shape is a moving target — the finalizer re-measures
  from the commit; the v1 numbers above stay the pre-state.

**v2c (21:01:45Z–21:02Z): the round's audit report is appearing.**
- `reports/r10-aud-m10.md` — 160 L / 13,177 B / `d98926185a3a299e…`, mtime
  18:01:45 −03:00 (= 21:01:45Z), untracked, in flight; self-label "AUD-M10 —
  round-10 audit: the arc synthesis (4 claims re-derived) and the standing-use
  note's 2 commands"; its window 20:54–21:02Z; sections incl. "Findings
  (named, not smoothed)". Its scratch freezes `gate-93e43f8f.sh` and
  `note-7f61d87d.md` — i.e., the audit's note subject is the **earlier**
  revision `7f61d87d…`; the note has since grown to `aaa2e625…` (361 L at
  21:01Z). The finalizer must check the landed note revision against the
  audit's frozen subject and record the coverage (the same stale-subject
  class as SKILL's AUD-M9 sha quote, §6(g)).
- The three earlier in-flight artifacts have been steady since 17:57–17:58:
  arc-synthesis 387 L / `a5b48331…`; gate-standing-use 361 L / `aaa2e625…`;
  round-11 plan 352 L / `4bde28aa…`. Gate sha unchanged `93e43f8f…`;
  `corpus/lessons/` still 0; no commit.
- Scribe window closes here (~21:02Z): this draft is this lane's only repo
  write; anything landing after this line is unmeasured by this lane and must
  be re-measured at the commit.

⟨Append v2+ here as artifacts land: each update tagged with its own
measurement time; v1 numbers above stay for provenance. Re-run the §9
checklist from the landed revision, not from this draft's before-state.⟩