# mado round-8 record — scribe prep DRAFT (SCR-M8)

Draft v1 window: 2026-10-14 19:10–19:16Z (local 16:10–16:16 −03:00). Lane SCR-M8.
This file is scribe scratch product for the round-8 finalizer — **not the record**.
Nothing outside this file was written by this lane in the repo; scratch
`/tmp/w8-scr-m8/` (`selftest.log`, `nolive.log`, `live.log`, `regression.log`,
`selftest-rowids.txt`). All probes read-only (file reads, `wc`/`sha256sum`/
`stat`/`git` read verbs, the gate's own modes, `hyprctl` read verbs, `pgrep`/
`systemctl --user is-active`/`ls` on the socket dirs, `omarchy version`/
`theme current`/`commands --json --all`); no substrate file under
`~/.config`/`~/.local` was written; no live session disturbed; no socket
connected; no network command.

**One boundary deviation, disclosed [OBS].** Before reading the omarchy §6
guard list this lane ran `git -C ~/.local/share/omarchy status --porcelain`
once (19:12Z) — a verb the note's own guard list forbids ("never `git status`
on the checkout", `omarchy-drift-watch.md` §6, per `province-accuracy-selfaudit.md`
§:110-128: it refreshes the index stat cache). Measured immediately after:
`.git/index` mtime `2026-10-14 11:42:09.67 −03:00` (i.e. predates this lane's
probe by ~7.5 h), size 122,964 B — no index write observed, tree read as clean.
No other guard-adjacent verb was run; the finalizer should not repeat it.

Reading key: **⟨PENDING⟩** = must be resolved at finalization; every other
number names the command that produced it at v1 time. Tags: **[OBS]** measured,
**[INF]** inference from measured code/record, **[UNK]** unknown. Counts on
`.md` notes use `wc -l` (files without a trailing newline show editor view = +1;
`plans/round-8.plan.md` ends with `0x2e` — `.` — so 206 by `wc -l` / 207 editor
view). Shas are cited as measured prefixes (16 hex) unless noted.

## 0. Round-8 frame

- Plan: `plans/round-8.plan.md` — **committed in the round-7 landing** (`0c20a76`),
  206 L by `wc -l` / 13,854 B / sha `ffcc058aa17755d9…` (freeze 18:25Z; design
  lane PREP-M8). Axis move: **operability + freshness** — ONE move, three
  ordered stages: (a) the suite's proof body closes over the live plane
  (hermetic PATH-stub scenarios J/K/L; never the substrate); (b) the declared
  census closes over the freshness plane — `omarchy` plane id 7, rows and
  constants from `omarchy-drift-watch.md` §6, D-1 resolved as NOTE for the
  theme row; (c) the assertion floor rises over the recorded residuals
  (`--root` no value, bad `MADO_VERIFY_LIVE`, the version string, the boundary
  combined-hash prefix) plus the rc-6 dead-code decision.
- Ordering (plan `:151-159`): (a) is gated on the round-7 precondition set
  (a7)/(b7)/(c7), each resolved from the round-7 record; (b)/(c) are gated on
  (a) green; **every widening carries a `MADO_REGRESSION: PASS` at the widened
  revision** — widening without a covering kill vehicle does not ship.
- Anti-claim (as written): a surviving mutant is a FINDING (append-only errata);
  a stubbed scenario proves row logic, never live values; an unfaithful stub
  shape is exempted **by name**, never faked; any unverifiable check reads
  UNKNOWN, never CLEAN; the `omarchy` baseline is never edited to match reality;
  the theme row stays NOTE; no compositor/session mutation; tameshi harness and
  the omarchy checkout read-only (a needed change is a recommendation to that
  lane); no `git status`/`fetch` on the checkout; the gate's revision sha is
  measured before and after every sweep.
- Measure (plan `:173-188`): regression verdict per landed revision; selftest
  count before → after with scenario ids; distinct asserted row ids 11 of 40 →
  measured; plane census 6 ids / 106 row sites / 40 row ids → 7+ / 106+N;
  omarchy per-pin HELD|MOVED|UNKNOWN; extended kill grid; the two verdicts;
  SKILL gate section gains the plane + regression usage; SCORECARD + LOG +
  README rows; `corpus/lessons/round-8.md` chartered (with `## Gate` section
  and a non-author spot-check, or the round records why no independent seat
  exists).

### 0.1 Design-time pins in the plan are superseded by the round-7 landing [OBS]

The plan was frozen 18:25Z **while round 7 was still writing**; the round-7
commit landed at 19:06:31Z. Every gate number in the plan reads at the
round-6 revision. Landed values (re-measured at v1, §1.2):

| plan says (round-6 base) | landed at `0c20a76` [OBS] |
|---|---|
| gate `c4c1afb7…`, 1,186 L, 50,126 B | `90d50cdd…`, **1,755 L**, 75,771 B (+569/−0) |
| `--regression` token absent (`grep -c regression` → 0) | **present** (`grep -c regression` → 42; `grep -c -- '--regression'` → 21); `MADO_REGRESSION: PASS` measured by this lane (§1.2) |
| selftest `53/53` | **`89/89`** (53 → 89, +36, per LOG `:297`) |
| census "106 `row` + 6 `row_from_rc`, 40 row ids, six plane ids — hypr 23 / hypr-live 51 / …" | **unchanged at the site level**: 106 `row` + 6 `row_from_rc`, 40 distinct row ids, six plane ids; the `row`-only prefix census reads hypr 23 / hypr-live **51** / waybar 17 / terms 10 / gate 3 / walker 2, and `row_from_rc` adds **6 hypr-live** sites → hypr-live 57 of 112 [OBS, §1.3] |
| "the gate's own readers `:676-1108`" | current readers live in `live_plane()` `:1408-1679`; the round-6 anchor range is stale (§3.1) |
| "selftest's awk helpers hard-code the six ids at `:352`, `:356`, `:371-375`" | **still current**: `:352`, `:356`, `:371-375`, regex `(hypr|hypr-live|waybar|walker|terms|gate)` [OBS] |
| "assertion count 53 → 53+M" | arithmetic base is **89 → 89+M** |
| "distinct asserted row ids (11 of 40 today)" | **still 11 of 40** [OBS, §1.3] — this plan number holds |

The record must cite landed values, and any finalizer arithmetic copied from
the plan ("53", `c4c1afb7…`, "hypr-live 51") is a stale-base defect (same class
as round-7 §0).

### 0.2 Round-7 precondition resolution [OBS]

- **(a7) regression mode exists with token and exit map — SATISFIED.**
  `--regression` present with token `MADO_REGRESSION: PASS|FAIL|SETUP`
  (`:745`, `:955-1036`), usage refusals for `--target/--defects/--suite` and
  the gate's own flags (`:1063-1075`), scratch `/tmp/mado-verify-regression.*`;
  selftest R12/R13 assert the contract; this lane's own receipt: PASS 10/10 at
  19:12:40Z, 12.6 s (§1.2). One plan deviation is documented by round 7 and
  must be carried, not smoothed: the implementation requires **all ten kills
  exactly** (`flips=0`), the plan's `|killed − recorded| ≤ 1` tolerance is
  deliberately not applied (`r7-aud-m7.md` §5.1).
- **(b7) theme/wallpaper rows landed — RESOLVED AS: note landed, gate rows
  absent.** `corpus/knowledge/theme-wallpaper-plane.md` (394 L / `8c578cc7…`)
  landed and committed; the gate still carries **no** theme plane/rows beyond
  `live.theme.current` NOTE (`:1673`, `:1677`); audit `r7-aud-m7.md` C3 =
  **NOT-LANDED (note verified)**.
- **(c7) walker live rows landed — RESOLVED AS: note landed, gate rows
  absent.** `corpus/knowledge/walker-live-surface.md` (300 L / `2bbb9609…`)
  landed; walker live rows are still version + services only
  (`:1648-1667`); audit C4 = **NOT-LANDED (note verified)**.
  The plan's measure line "plane census … → 7+" assumes the omarchy plane is
  the first new id; at v1 the round-7 theme/walker rows still add none — the
  landed-set count is what the round measures, never the plan's assumption.

## 1. Pre-state at v1 (round 7 landed; round 8 in flight)

1. **Repo identity** [OBS, 19:10–19:14Z]: HEAD
   `0c20a76fa5ff985047c8ca2d455c75179c3dd0d1` ("probation round 7 (training r6):
   see LOG", 2026-10-14 16:06:31 −03:00 = 19:06:31Z); `git status --porcelain`
   empty at 19:10Z. `git show --stat HEAD`: 9 files, **+2,480/−1** — LOG +2,
   SCORECARD +1, SKILL +198, `corpus/knowledge/theme-wallpaper-plane.md` +394,
   `…/walker-live-surface.md` +301, `plans/round-7-record-draft.md` +569,
   `plans/round-8.plan.md` +207, `reports/r7-aud-m7.md` +240,
   `tools/mado-verify.sh` +569/−0.
   Pins (`wc -l` / bytes / sha256 prefix, all read at v1):
   SKILL.md 905 L / 70,490 B / `e0d516e84ed27834…`;
   LOG.md 298 L / 22,283 B / `9843f0f3df38c7f9…`;
   SCORECARD.md 19 L / 8,938 B / `40d87245af6c5a02…`;
   SHONEN.md 12 L / 1,688 B / `edace65e13c8ad20…` (byte-identical since
   `c03c249` — 4/4 `[x]`, PROBATION COMPLETE);
   PROVINCE.md 18 L / 891 B / `7aad7b863dc3c10b…`;
   MINT.md 20 L / 919 B / `4408f66765729a44…`;
   `corpus/README.md` 19 L / 12,709 B / `2dd274f5e270e65b…` (**8 note rows**);
   `corpus/QUALITY.md` 8 L / 329 B / `1923c94f49788ade…`;
   `plans/round-8.plan.md` 206 L / 13,854 B / `ffcc058aa17755d9…`;
   `plans/round-7.plan.md` 135 L / 8,689 B / `d4e23e8159ff4441…`;
   `plans/round-7-record-draft.md` 568 L / 37,482 B / `045d380ab52ce317…`
   (committed **with 13 ⟨PENDING⟩ markers unfilled** — `grep -c PENDING` → 13;
   see §1.8.5);
   `plans/round-6-record-draft.md` 458 L / 28,813 B / `f9210046e9fb8e99…`;
   `reports/r7-aud-m7.md` 239 L / 18,927 B / `4011b2c44c9abb35…`.
2. **Gate identity and runs** [OBS]: `tools/mado-verify.sh` **1,755 L / 75,771 B
   / sha256 `90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd`**,
   mtime 2026-10-14 15:31:57.66 −03:00. Runs (all read-only, this lane, logs
   `/tmp/w8-scr-m8/`):
   - `--selftest` → `MADO_SELFTEST: 89/89 assertions passed`, rc 0 (~2 s);
   - `--no-live` → `MADO_VERIFY: CLEAN (17 pass, 2 notes; file plane only —
     live layer skipped: --no-live)`, `counts: pass=17 fail=0 unknown=0 skip=1
     note=2`, rc 0;
   - live → `MADO_VERIFY: CLEAN (35 pass, 4 notes; file + live planes verified
     read-only)`, `counts: pass=35 fail=0 unknown=0 skip=0 note=4`, rc 0;
     `boundary.readonly` PASS "config plane byte-identical before/after
     (combined sha **bb2639d9a980**…)" — the same combined-hash prefix the
     round-6/7 records carry;
   - `--regression` → **`MADO_REGRESSION: PASS (case=mado-verify-hardened;
     target=c4c1afb75dd1c8aa…a5171)`**, rc 0, 12.6 s, `REGRESSION_DATE:
     2026-10-14T19:12:40Z`; `REGRESSION_SPEC` sha `c7ee75b97c38ac8f…1dd8`
     (recorded pin matches); `REGRESSION_HARNESS` `cf41efaa…242c75` (recorded
     revision `b56c6e57…22bcb` — provenance, not gated);
     `REGRESSION_TABLE … match=10/10 recorded-killed=10 measured-killed=10
     survived=0 inconclusive=0 flips=0`; `REGRESSION_CLEANUP: removed=10`;
     workdir `/tmp/mado-verify-regression.AoG1em` removed on PASS.
3. **Gate census (before)** [OBS]: `grep -cE '^[[:space:]]*row [a-z-]+ '` → **106**;
   `row_from_rc` call sites **6** (`:1474`, `:1483`, `:1508`, `:1544`, `:1553`,
   `:1632`; definition `:102`) → 112 row sites. By first-arg plane prefix
   (row only) — hypr 23 / hypr-live 51 / waybar 17 / terms 10 / gate 3 /
   walker 2 = 106; adding the 6 `row_from_rc` sites (all `hypr-live`) →
   **hypr-live 57 / 112 total** [OBS]. **Distinct row ids: 40** (same count as
   round 6). Live row ids: 21 distinct (`live.*`), incl. `live.theme.current`
   and `live.walker.{version,services}`. **Distinct row ids asserted by the
   suite: 11 of 40** — `st_row_has` touches 10 ids + `st_row_detail` pins
   `hypr.file.sha_pin` (`:580-581`) [OBS; matches the plan's 11]. The six
   helper regexes are still `(hypr|hypr-live|waybar|walker|terms|gate)` at
   `:352`, `:356`, `:371-375`.
4. **Stage (c) pre-state — the recorded residuals are still open** [OBS]:
   - `--root` with no value: `:1689`, `usage error: --root needs a directory`,
     exit 2 — **no selftest assertion** (no `st_*` case exercises it);
   - bad `MADO_VERIFY_LIVE`: `:1709`, `usage error: MADO_VERIFY_LIVE must be
     auto|yes|no`, exit 2 — **no selftest assertion** (the only env use is
     `MADO_VERIFY_LIVE=yes` at `:609`, a valid value);
   - version string: `VERSION_STR="mado-verify.sh v1 (mado-shokunin round 5 /
     M5-2)"` at `:63`, printed at `:1720` — **unasserted and stale** (the gate
     has shipped two rounds of change under a round-5 self-label);
   - boundary combined hash: detail at `:1396` prints `${before:0:12}…`; the
     suite asserts the row status only (`:574`, `:685`) — **prefix pattern
     unasserted**;
   - rc-6 arm: `row_from_rc` maps `6) → UNKNOWN` (`:102-108`); nothing in the
     gate exits/returns 6 (`grep -nE 'exit 6\b|return 6\b|sys\.exit\(6\)'` →
     empty) → **still dead code**, reconfirming `gate-mutation-proof.md` §3;
   - exit-flatten family: harness boundary (round-6 §3); whether tameshi's
     harness now reads suite stdout is **not measured here** (sibling,
     read-only); the harness moved `b56c6e57…` (46,850 B class) →
     `cf41efaa…` 1,341 L / 61,632 B, mtime 15:29:01 −03:00 [OBS].
5. **Round-7 artifacts the round-8 stages consume** [OBS]: `theme-wallpaper-plane.md`
   394 L / 27,594 B / `8c578cc70e36506d…`; `walker-live-surface.md` 300 L /
   19,203 B / `2bbb9609283f2d81…`; `omarchy-drift-watch.md` 287 L / 18,714 B /
   `49f5a9a14776d83d…` (the §6 arm spec is stage (b)'s input, **never edited** —
   re-anchoring appends to its `Errata (append-only)` section at `:280`);
   `remaining-planes-census.md` 333 L / 20,512 B / `710e3e289643f2ff…`;
   `gate-mutation-proof.md` 167 L / 10,693 B / `716836ca1bf3484a…`;
   `walker-deep.md` 617 L / 38,403 B / `0982ba066c72575a…` (its §10/§11 errata
   append — the r7 note's ledger — **still owed** [OBS: file unchanged]).
   Audit `reports/r7-aud-m7.md` verdicts: C1 PASS (regression), C2 PASS (one
   documented band deviation), C3/C4 NOT-LANDED (notes verified), C5 PASS
   (selftest 53 → 89; `--no-live`/live counts identical to round 6).
6. **Stage (b) design anchors re-measured** [OBS, 19:11–19:13Z] — all held:
   `omarchy version` → `3.8.3`; `~/.local/share/omarchy/version` → `3.8.3`
   (6 B); `git -C ~/.local/share/omarchy describe --tags --exact-match` →
   `v3.8.4`; `rev-parse HEAD` → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`
   (`git log -1`: 2026-07-20 14:05:35 −07:00, "Merge branch 'master' into rc");
   skill link `~/.agents/skills/omarchy` → `/home/vgpnk/.local/share/omarchy/
   default/omarchy-skill` (54 B symlink); leaf SKILL.md 392 L / 14,908 B /
   `becd149e4d1c0767…`; `omarchy theme current` → `Matte Black`;
   `~/.config/omarchy/current/theme.name` 12 B `matte-black`;
   `omarchy commands --json --all` → **282 commands / 56 groups**, the §6
   eleven skill groups (refresh restart toggle theme install launch capture
   reminder pkg setup update) all present; `.git/index` 122,964 B, mtime
   11:42:09.67 −03:00 (see the boundary deviation note).
7. **Live pins for the stubbed rows** [OBS, 19:11–19:12Z; point samples —
   a session restart invalidates them]: Hyprland instance
   `efb50993780079460b0cbed1363e2166a2de1d9f_1791994267_1144437716`, wl_socket
   `wayland-1`; walker 1203471 `/usr/bin/walker --gapplication-service`,
   elephant 1203474; `systemctl --user is-active app-walker@autostart.service
   elephant.service` → `active`/`active`; sockets
   `/run/user/1000/{walker,elephant}/*.sock` `srwxr-xr-x` 0 B (mtime 13:11
   local); `hyprctl -j layers` → DP-1 level 0 `wallpaper` 1203358, level 2
   `waybar` 1203352, **no walker namespace** (launcher closed). These are the
   *values* a stub must imitate faithfully; the substrate itself is never read
   by the new scenarios.
8. **Record debt carried into round 8** [OBS, all still unpaid]:
   1. `corpus/README.md` — **8 note rows; 8 rows missing**, one per note:
      `idle-lock-plane.md` (r4), `province-accuracy-selfaudit.md` (r4/r5),
      `walker-deep.md` (r5), `gate-mutation-proof.md`, `omarchy-drift-watch.md`,
      `remaining-planes-census.md` (r6), `theme-wallpaper-plane.md`,
      `walker-live-surface.md` (r7). Ready text: round-4 draft §4b (`:300`),
      round-5 draft §4b (`:276`), round-6 draft §4b (`:258`), round-7 draft
      §4b (`:321`).
   2. `SCORECARD.md:16-19` — rounds 4, 5, 6, 7 are one-line stubs; full rows
      sit in the committed drafts (round-4 §4c `:311`, round-5 §4c `:287`,
      round-6 §4c `:270`, round-7 §4c `:335`).
   3. `LOG.md:294-296` — rounds 4/5/6 entries are one-line summaries (round 7
      has the full M7-1 entry at `:297` plus the round summary at `:298`).
   4. Errata: the theme note's `§10 Errata` (`:362`) exists — append-only target
      for stage (b) re-anchoring; the walker note routed its ledger to
      `walker-deep.md` §10/§11 (parent dir still unchanged → still owed); no
      repo-level `Errata (round N)` block exists.
   5. The committed `plans/round-7-record-draft.md` keeps **13 ⟨PENDING⟩
      markers** — D1/D2/D3 and the record-text slots were never filled after
      the landing. §4f supplies the measured fill so the round-8 commit can
      close them as an appended erratum (never an edit of the committed text).
   6. `corpus/lessons/` still 0 entries (eighth round of the round-1 promise);
      the plan's measure line charters `corpus/lessons/round-8.md` with a
      `## Gate` section and a non-author spot-check — **first lesson file** if
      it lands (a lane's own subagent does not count as the non-author seat;
      `LEARNING.md:38-43`).
9. **Round-8 lane activity at v1** (shape-only; no repo file landed):
   `git status --porcelain` clean at 19:10Z; scratch seen `/tmp/w8-mado-m8-1/`
   (not read), `/tmp/w8-mado-m8-4/` (`poll.sh`, `poll.log` — 280 B, last write
   16:12 local), tameshi-side `/tmp/w8-tameshi-t81/`, `/tmp/w8-tameshi-scr-t8/`;
   audit/verifier seats `/tmp/w8-ver`, `/tmp/w8-ver-m8-scr`,
   `/tmp/w8-ver-m8-pol.sh`, `/tmp/w8-ver-t8-*`; others
   (`/tmp/w8-arch-tranche`, `/tmp/w8-scrb8`, `/tmp/w8-preps9-tsukuroi`, …) are
   sibling-lane scratch, not mado artifacts. Lane labels are recorded by
   artifact self-label at finalization (round-5 lesson).

## 2. Deliverables and ⟨PENDING⟩ slots

### D1 (a) — live-body exercise through PATH stubs ⟨PENDING⟩

Must carry, per plan `:56-71`: scenarios **J** (stubbed-clean live run →
covered live rows PASS, verdict CLEAN, counts agree), **K** (one stubbed pin
MOVED → the named live row FAILs, DIVERGED, exit 1), **L** (stub absent with
live requested → affected rows UNKNOWN, never CLEAN); stubs for the readers in
§3.1, first on PATH; `$HOME` never the root; assertion count **89 → 89+M** with
scenario ids listed; distinct asserted row ids **11 of 40 → measured**; any
reader whose fixture shape is unfaithful is exempted **by name** with its
clause anchor. The defect spec extends per newly covered clause (live-branch
verdict token / M16 class; skip-reason strings; `--root=DIR` form; env-var
renames; version string) and the sweep is re-cut at the landed revision;
survivors are findings. ⟨PENDING: scenario ids + M; landed gate sha
`90d50cdd…` → ??; line/byte delta; the covered live row ids list; the
exemption list (or "none"); the extended spec sha + `MADO_REGRESSION: PASS`
receipt at the widened revision; whether the M16-class mutant (live-branch
CLEAN token) is now killed.⟩

### D2 (b) — `omarchy` freshness plane, id 7 ⟨PENDING⟩

Rows/constants from `omarchy-drift-watch.md` §6 (input, never edited). Verdict
rows: `.version.cmd`, `.version.file`, `.git.tag`, `.git.head`, `.skill.link`,
`.skill.sha`, `.skill.vs_head`, `.cmd.groups`; NOTE rows: `.cmd.surface`,
`.theme` (D-1 resolved as NOTE with HELD|MOVED in the detail), `.doc.drifts`.
Four §6 scenarios land as selftest cases (clean; version file MOVED → FAIL +
DIVERGED; live verb unavailable → UNKNOWN; link replaced by a real dir with
equal sha → `.skill.link` FAIL while `.skill.sha` PASS). Reads only the §6
guard list; never `git status`/`fetch`; no mutating omarchy verb. The selftest
helper plane regexes (`:352`, `:356`, `:371-375`) widen from six ids to the
landed set; the per-plane census is re-reported. §6's own anchor numbers are
round-6 revisions (`:1069` plane column → now `:1726` `printf '%-9s %-31s …'`;
`:99` `tmo` — unchanged; `:587-591` live-skip semantics → now `:1243-1247`;
`:400-412` scenario C sandbox → now `:602-617`; `:368` `$0`-vs-`$MUTANT` — the
suite still invokes `"$0"`, see §3.2). ⟨PENDING: landed row ids + plane token
spelling; gate sha after; which 4+ scenarios landed and their assertion count;
helper-regex widening proof (id count before → after); `MADO_REGRESSION: PASS`
receipt; D-1's landed form; whether `omarchy.skill.vs_head` shipped (it needs
`git show`, a read verb, inside the checkout).⟩

### D3 (c) — assertion floor + rc-6 decision ⟨PENDING⟩

Per plan `:140-149`: `--root` with no value → exit 2 + usage text; a bad
`MADO_VERIFY_LIVE` → exit 2; the version string becomes a checked claim (the
self-label names the landed revision, asserted); the boundary combined-hash
prefix asserted in the `sha_pin` detail pattern. The rc-6 dead-code arm is
resolved by its named decision — a white-box pin in the suite (the arm maps
6 → UNKNOWN) **or** branch removal — choice and consequence recorded. The
exit-flatten family stays a harness boundary: a recommendation to tameshi (a
kill criterion that also reads suite stdout), never a patch. ⟨PENDING: the
landed assertions + their labels; the version string's new text; the rc-6
decision taken and its evidence; whether the boundary prefix check landed;
the recommendation's landing place (LOG unknowns vs a note).⟩

### D4 — record debt repayment (record work, not a new claim)

README 8 carried rows + round-8 rows; SCORECARD rows 4–7 replacement + round-8
row; LOG round-8 entry (§4a) and optionally the fuller 4–6 entries; errata
status (§4e) incl. the round-7 draft fill (§4f). ⟨PENDING: which of the carried
items the round actually pays; every landed row quoted from the measured
artifact.⟩

### D5 — `corpus/lessons/round-8.md` charter ⟨PENDING⟩

Plan measure `:185-188`: chartered with its `## Gate` section and a non-author
spot-check (at least one admit and one reject) — or the round records why no
independent seat exists. The file would be the **first** entry in
`corpus/lessons/` (0 entries since round 1). ⟨PENDING: landed or refused; if
landed: line count/sha, the seat's identity (not the lane's own subagent),
one admit + one reject quoted; if refused: the recorded reason.⟩

## 3. Clause maps — anchor → coverage (before state)

### 3.1 The live readers the stubs must imitate (`live_plane()` `:1408-1679`)

| Reader call | Call sites [OBS] | Guard / degradation today | Stub shape needed |
|---|---|---|---|
| `hyprctl version` | `:1416` (pre-check), `:1426` | `have hyprctl` `:1409`; rc≠0 → live.plane UNKNOWN | `Hyprland 0.56.2 … efb5099…` |
| `hyprctl -j instances` | `:1435` | python3 parse; empty/bad → UNKNOWN | JSON array, 1 instance, `wl_socket` |
| `hyprctl configerrors` | `:1457` | text read | empty output (clean) |
| `hyprctl -j getoption {general:gaps_out, input:kb_layout, general:border_size, decoration:rounding, animations:enabled, input:touchpad:scroll_factor}` | `:1469`, `:1478`, `:1491`, `:1493`, `:1503`, `:1548` | python3 parse; rc 5 → FAIL, rc 4 → also non-6 → FAIL | per-key JSON `{"custom","set"}` / `{"str","set"}` / `{"int"}` / `{"float"}` |
| `hyprctl -j binds` | `:1513` | parse | 192-element array |
| `hyprctl -j monitors` | `:1529` | parse | DP-1 3440x1440@~100 |
| `hyprctl -j layers` | `:1609` | parse | DP-1 + waybar surface |
| `printenv GDK_SCALE` / `NVD_BACKEND` | `:1571`, `:1577` | `have printenv` | `1` / unset (rc 1) |
| `waybar --version` | `:1590` | `have waybar` | `Waybar v0.15.0` |
| `pgrep -x hypridle` / `-x waybar` | `:1559`, `:1601` | `have pgrep` `:1557`, `:1598` | absent (NOTE class) / pid |
| `busctl --user get-property fr.arouillard.waybar … RegisteredStatusNotifierItems` | `:1638` | `have busctl` | property string (tray list) |
| `walker --version` | `:1651` | `have walker` | `2.17.0` |
| `systemctl --user is-active app-walker@autostart.service` / `elephant.service` | `:1662`, `:1663` | `have systemctl` | `active` ×2 |
| `omarchy theme current` | `:1676` | `have omarchy` | `Matte Black` |

Environment preconditions a stubbed run must satisfy: `hyprctl` first on PATH
(`:1409`), **`HYPRLAND_INSTANCE_SIGNATURE` set** (`:1411` — unset alone forces
`live.plane UNKNOWN`), `python3` present (parse arms degrade to UNKNOWN
otherwise), and `timeout` optional (`tmo` `:99` falls back to direct
invocation). Note the plan's stub list names `hyprctl -j clients`; the gate has
**no** clients call (`grep -n clients tools/mado-verify.sh` → empty) — a
plan-vs-gate mismatch to record, not to implement [OBS].

Fidelity trap for scenario K and the rc-6 decision: the parse blocks exit
**3** (read error), **4** (parse error), **5** (mismatch) — never 6 — so a
"corrupt fixture" stub maps to FAIL via `row_from_rc`'s `*)` arm, not UNKNOWN.
The UNKNOWN-by-absence path is the `have`/`python3`-missing arm, which is what
scenario L exercises.

### 3.2 The suite plumbing new rows must clear

The helper plane regexes still hard-code six ids in seven awk sites — `st_rows`
`:352`, `st_row_has` `:356`, `st_counts_agree` `:371-375`. Any new plane token
(in practice `omarchy`) must extend all seven or its rows are invisible to the
suite's counts (the fake-PASS risk `st_counts_agree` exists to catch). The
suite invokes **`"$0"`** (e.g. `:564`, `:609`) — the round-6 noted `$MUTANT`
gap was not closed by round 7's engine (the *regression* path does target the
mutant's copy, which is why the sweep still kills); a stub scenario must keep
`$0` resolution and PATH-based stubbing compatible (scenario C's sandbox idiom
`:602-617` is the pattern; no `--selftest` nesting needed for J/K/L). Assertion
counts measured at v1: helper invocations `st_eq` 29 · `st_has` 29 ·
`st_not_has` 7 · `st_rg` 14 · `st_ok` 5 · `st_bad` 5 · `st_rows` 3 ·
`st_row_has` 19 · `st_row_detail` 3 · `st_counts_agree` 7 — the gate's own
counter reads 89 (helpers wrap each other; cite 89, not the site sums).

### 3.3 The §6 arm spec → current gate anchors

| §6 element | §6's anchor (r6 revision) | Current anchor [OBS] |
|---|---|---|
| `tmo` helper | `:99` | `:99` (unchanged) |
| plane column `%-9s` | `:1069` | `:1726`, `:1730` |
| live-skip semantics (`live.plane SKIP`, scope named) | `:587-591` | `:1243-1247` |
| scenario C sandbox idiom | `:400-412` | `:602-617` |
| helper plane regexes | `:352,356` (+counts `:371-375`) | `:352`, `:356`, `:371-375` (unchanged) |
| row helper | — | `row()` `:86`, `row_from_rc()` `:102` |
| verdict print | — | `:1745-1755` |

### 3.4 Round-7 residue not covered by round 8 [OBS]

The theme chain rows (file + live) and the walker sockets / D-Bus-owner /
layer-invariant rows remain **unlanded in the gate**; they are not part of
round 8's claim (plan stages are (a)/(b)/(c) as above). Current sites:
`live.theme.current` NOTE `:1673`/`:1677`; `live.walker.version` `:1648-1655`;
`live.walker.services` `:1659-1667`. The paste-ready specs are
`theme-wallpaper-plane.md` §6 and `walker-live-surface.md`'s ledger — the
record should state the residue plainly rather than let the round read as if
the plan's 7-plane census arrived.

## 4. Record text to apply

### 4a. LOG.md round-8 entry (append after `LOG.md:298`)

```
- 2026-10-14 — round 8 (training r7): (a) live-body exercise — hermetic
  PATH-stub scenarios J/K/L reach the live rows the suite never executed:
  ⟨fill: covered live row ids; stubs shipped; assertion count 89 → ?? (+M,
  scenario ids); distinct asserted row ids 11 of 40 → ??; exemptions by name
  or none; the extended defect spec sha + MADO_REGRESSION: PASS receipt at the
  widened revision⟩. (b) `omarchy` freshness plane, id 7: ⟨fill: landed rows
  (verdict vs NOTE); the §6 constants vs the held anchors — version 3.8.3 /
  file 3.8.3 / tag v3.8.4 / head 8fcc9d60… / skill link + sha becd149e… /
  theme Matte Black (NOTE, D-1); helper regex widening 6 → 7 ids; selftest
  additions; MADO_REGRESSION: PASS⟩. (c) assertion floor: ⟨fill: the two
  usage arms + version string + boundary prefix; rc-6 decision (pin or
  removal) + consequence; exit-flatten recommendation to tameshi recorded,
  not patched⟩. Gate sha `90d50cdd…` → ⟨fill⟩; selftest 89/89 → ⟨fill⟩;
  census 106 row + 6 row_from_rc sites / 40 ids / 6 plane ids → ⟨fill⟩;
  `--no-live`/live verdicts ⟨fill⟩; regression PASS at the landed revision.
  Record debt repaid: README +⟨fill⟩ rows (8 carried + round-8); SCORECARD
  rows 4–7 stubs replaced + round 8; round-7 draft ⟨PENDING⟩s filled by
  appended erratum; `corpus/lessons/round-8.md` ⟨landed|refused, reason⟩.
  Boundary: gate + harness + omarchy checkout read-only; no substrate file
  written; no live session disturbed; no socket opened; no `git status` on the
  checkout.
- ⟨If (a) does not land: the round reports the stub scenario set as unshipped,
  (b)/(c) follow plan ordering only under (a) green — no widening headline.⟩
```

### 4b. `corpus/README.md` — coverage map rows

Apply the eight carried rows in order (ready text named in §1.8.1: round-4
draft §4b for `idle-lock-plane.md` + `province-accuracy-selfaudit.md`,
round-5 draft §4b for `walker-deep.md`, round-6 draft §4b for the three r6
notes, round-7 draft §4b for the two r7 notes) — **re-measure every pin at
apply time**; the lands are unchanged at v1 (§1.5) except as the round's own
work moves them. Then one row per round-8 note as landed ⟨PENDING⟩
(composition follows the existing row shape: note → holds → sources with the
probe window; write from the measured artifacts, never from this draft).

### 4c. `SCORECARD.md` — move-log rows

Replace the stubs `:16-19` with the committed full rows (sources in §1.8.2),
then append round 8:

```
| 8 | operability + freshness | round-7 gate: the live plane was 57 of 112 row sites with only its guard rows exercised, the `omarchy` freshness arm was a paste-ready spec, and the recorded usage/cosmetic residuals had no assertions | live rows reached hermetically via PATH stubs ⟨fill: J/K/L evidence; row ids; assertion count 89 → ??⟩; `omarchy` plane 7 lands ⟨fill: verdict vs NOTE rows; constants held⟩; assertion floor ⟨fill: usage arms, version string, boundary prefix; rc-6 decision⟩ | ⟨fill: receipt lines; gate sha `90d50cdd…` → ??; census 6 → ?? plane ids; selftest 89 → ??; `--no-live`/live verdicts; scratch `/tmp/…`⟩ |
```

### 4d. SHONEN.md

No box move expected: 4/4 `[x]` since round 5; promotion is the
operator/integrator decision. Byte-identical at `edace65e13c8ad20…` unless the
finalizer edits an evidence line — if edited, re-apply the seed check
(`PROTOCOL.md:419-431`).

### 4e. Errata status

Append-only when applied: `theme-wallpaper-plane.md` §10 (its own errata route,
opened at `:362`) is the re-anchoring target for stage (b); `walker-deep.md`
§10/§11 owe the walker note's ledger (r7 note routed it explicitly); the §3
residuals of `gate-mutation-proof.md` are closed/retained per D3's rc-6
decision and the harness recommendation (record the latter in the LOG unknown,
never as a patch to tameshi). No repo-level errata block exists.

### 4f. Round-7 record closure (appended erratum, never an edit)

The committed `plans/round-7-record-draft.md` keeps 13 unfilled ⟨PENDING⟩
markers (§1.8.5). The measured fill, for an appended closure block in the
round-8 commit:

- D1 (a): landed; gate `c4c1afb7…` → `90d50cdd…` (+569/−0, 1,186 → 1,755 L);
  selftest 53 → 89; receipt `MADO_REGRESSION: PASS (case=mado-verify-hardened;
  target=c4c1afb7…a5171)` — reproduced by this lane 19:12:40Z, 12.6 s; band =
  exact 10/10 (the plan's ±1 tolerance deliberately not applied; audit §5.1);
  spec `c7ee75b9…1dd8`; harness `cf41efaa…` (recorded `b56c6e57…`, provenance).
- D2 (b) / D3 (c): **gate rows NOT landed** — notes only
  (`theme-wallpaper-plane.md` 394 L `8c578cc7…`; `walker-live-surface.md`
  300 L `2bbb9609…`); audit C3/C4 NOT-LANDED (notes verified); the round-7
  draft's ⟨PENDING⟩ slots for these are answered "not landed" — the wiring
  remains open work carried into later rounds.

## 5. Scribe measurements and spot-checks (executed)

1. **Gate runs** (read-only, 19:10–19:12Z; logs `/tmp/w8-scr-m8/`):
   `--selftest` → `89/89` rc 0; `--no-live` → `counts: pass=17 fail=0
   unknown=0 skip=1 note=2` + CLEAN rc 0; live → `counts: pass=35 fail=0
   unknown=0 skip=0 note=4` + CLEAN rc 0; `--regression` → `MADO_REGRESSION:
   PASS` rc 0, 12.6 s, exact-table match, cleanup `removed=10`, workdir removed
   on PASS (§1.2). Verdict lines and receipt lines are quoted verbatim above.
2. **Census + suite coverage** (§1.3): 106 `row` + 6 `row_from_rc`; prefix
   census hypr 23 / hypr-live 51(+6 rc) / waybar 17 / terms 10 / gate 3 /
   walker 2; 40 distinct row ids; 11 of 40 asserted (10 `st_row_has` + 1
   `st_row_detail`); helper regex sites `:352/:356/:371-375` six ids.
3. **Omarchy anchors** (§1.6): all §6 constants HELD at 19:11–19:13Z; 282
   commands / 56 groups; 11 skill groups present; leaf 392 L / `becd149e…`.
4. **Live pins** (§1.7): instance `efb50993…`, walker 1203471, elephant
   1203474, sockets 0 B `srwxr-xr-x`, layers wallpaper 1203358 / waybar
   1203352, no walker namespace — the same values as round 7's record (no
   session restart since).
5. **Boundary**: writes = this draft + `/tmp/w8-scr-m8/`; no substrate file
   written; no live session disturbed; no socket connected; no network
   command; one guard-adjacent verb disclosed in the header (`git status` on
   the checkout — index mtime unchanged before/after).

## 6. Observations (v1)

(a) The plan's design-time state predates the round-7 landing by ~41 minutes
    and every gate number it carries is a round-6 value (§0.1). The finalizer
    must not copy "53", `c4c1afb7…`, or "hypr-live 51" into the record without
    the landed re-measure.
(b) The precondition set resolved unevenly [OBS]: (a7) satisfied; (b7)/(c7)
    are "note landed, gate rows absent". The plan's ordering clause reads as if
    round-7 rows would exist; the record should state the measured shape, mark
    the round-7 wiring as carried open work (§3.4), and not treat its absence
    as a round-8 defect.
(c) The stub contract is mostly a PATH-availability contract: every live
    reader is guarded by `have`, one is guarded by an env var
    (`HYPRLAND_INSTANCE_SIGNATURE`, `:1411`), and all parse arms need
    `python3`. The plan's stipulation "the suite reads no substrate ($HOME is
    never the root)" is achievable with the scenario-C idiom already in the
    file — the highest-risk fidelity gap is not the stubs but the parse-rc
    mapping (3/4/5 → FAIL; 6 unreachable), which shapes what K and L can
    demonstrate (§3.1).
(d) The rc-6 arm is still dead code at the landed revision [OBS, re-confirmed]
    — D3's named decision (white-box pin or removal) is the only way it stops
    surviving equivalent-edit mutants; the round-6 note anticipated exactly
    this.
(e) The version string has now survived two rounds of gate change
    (`v1 (round 5 / M5-2)` at `:63`); the round-7 audit listed the same class
    as cosmetic (§5.5: base `--help` omits `--regression`). D3 makes the string
    a checked claim; whether the base `--help` discoverability gap is folded in
    is the round's choice, not the plan's.
(f) Record debt is now three rounds deep: README owes 8 rows, SCORECARD 4–7
    are stubs, the committed round-7 draft's 13 ⟨PENDING⟩s stand unfilled, and
    `corpus/lessons/` is empty for an eighth round. §4 carries ready-to-apply
    text for all four; every round that lands notes without repaying deepens
    the hole.
(g) The §6 arm spec's anchor numbers are round-6 revisions; only `:99` and the
    helper regexes still coincide. The omarchy lane must re-anchor from the
    current file (§3.3), and any re-anchoring of the note itself is an
    append-only erratum (`omarchy-drift-watch.md` §Errata `:280`).
(h) Round-8's freshness claim rides a plane whose constants all held at v1 —
    the first time a freshness arm's design pins reproduce byte-for-byte a
    round later [OBS; §1.6 vs §0.2 of the round-7 draft]. If they move
    mid-round, the MOVED reading is the landing's first finding, not an edit of
    the baseline.

## 7. Unknowns (v1)

1. Whether (a) lands in-window; which readers prove faithfully stubbable and
   which get exempted **by name**; the extended spec sha and the re-cut sweep's
   survivors.
2. Whether (b) lands; whether `omarchy.skill.vs_head` ships (needs `git show`,
   a read verb, on the checkout) and how the 11-skill-group check is
   implemented against 282/56 live.
3. Whether (c) lands whole or partially; the rc-6 decision path (white-box pin
   vs removal) and who owns it; whether the boundary prefix lands as an
   assertion on `boundary.readonly` or inside the `sha_pin` detail.
4. Whether tameshi's harness ever gains a stdout-reading kill criterion (the
   exit-flatten family — that lane's call); the harness revision that the
   round's regression receipts cite.
5. Whether the round pays any of the carried record debt (§1.8) or defers
   again; whether `corpus/lessons/round-8.md` lands and who sits as its
   non-author seat.
6. Which lanes attest the round (audit/verifier seats seen at v1 but no
   verdict artifact exists) and their self-labels; the round-8 lane map is not
   visible from inside this lane [UNK] — record by artifact self-label.
7. Whether round-7's theme/walker gate wiring gets picked up by any round-8
   lane (it is not in the plan's claim) or stays carried into round 9.

## 8. Falsifiable next-iterations (carry + new)

- Land (a) with the covered-row list + assertion arithmetic + the re-cut sweep;
  state the exemptions by name; re-run `--selftest` and the regression at the
  landed revision.
- (b) only with the helper-regex widening proven by a before/after id count and
  a `MADO_REGRESSION: PASS`; theme row stays NOTE; the constants' HELD readings
  are the receipt.
- (c): the two usage arms asserted; version string names the landed revision;
  boundary prefix asserted; rc-6 resolved by the named decision; exit-flatten
  recorded as a recommendation.
- Repay record debt (README 8 + round-8; SCORECARD 4–7 full rows + 8; round-7
  draft ⟨PENDING⟩ fill as an appended erratum; LOG 4–6 fuller entries
  optionally).
- Charter `corpus/lessons/round-8.md` or record why no independent seat exists.
- Durability: fold receipt lines + tool/harness/target shas + gate sha into the
  record (scratch does not survive; the audit's kept workdirs are ephemeral).

## 9. Finalization checklist (mechanical, ordered)

1. Re-measure §1.1/§1.2 anchors; note drift as freshness rows; re-run the three
   verify modes and `--regression` at the revision being committed.
2. Read the landed (a) scenarios; list covered live row ids; count assertions
   (89 → ?) and distinct asserted row ids (11 → ?); verify each covered reader
   is stub-backed and each unfaithful one is exempted by name; verify the
   extended spec sha and the sweep's survivors/restore proof.
3. For (b): verify the plane token, the seven helper regex sites carry it, the
   §6 constants vs the held anchors (any MOVED pin reported first, never
   smoothed), D-1's landed form, and a regression receipt at the widened
   revision.
4. For (c): verify each new assertion actually fails when its subject is
   broken (spot-check one arm by hand); record the rc-6 decision and the
   exit-flatten recommendation's location.
5. Census before → after by the counting commands; quote `--no-live` and live
   verdicts at the committed revision.
6. Apply §4a (LOG), §4b (README), §4c (SCORECARD), §4d (SHONEN — likely
   no-op), §4e (errata), §4f (round-7 draft closure erratum).
7. Commit under the lane identity; freeze every cited sha in the entry; check
   the gate/harness/note shas appear; confirm no `git status` ran on the
   omarchy checkout during the round.
8. If (a) does not land: record the unshipped scenario set, keep (b)/(c) per
   plan ordering, and keep this draft as the record's ancestry.

## 10. v2 updates (append as artifacts land)

**v1 cut (19:16Z): nothing landed.** `git status --porcelain` empty at 19:10Z;
gate sha `90d50cdd…` and mtime 15:31:57 −03:00 unchanged through the window;
no new file under `corpus/knowledge/`, `corpus/lessons/`, `reports/`, `tools/`.
Lane activity is scratch-only (§1.9). Poll targets for the finalizer:
`sha256sum tools/mado-verify.sh` (≠ `90d50cdd…`), `grep -c 'row omarchy'
tools/mado-verify.sh` (today 0 — the string `omarchy` appears 53× in fixture
text/consumers, so count the row sites, not the word), `grep -n 'PATH='
tools/mado-verify.sh` (new sandboxes), `bash tools/mado-verify.sh --selftest`
count (>89), and `ls corpus/lessons/`.

**v2a (19:14:31Z): another lane's prep landed — not a mado round-8 artifact.**
`plans/round-9.plan.md` appeared untracked (231 L / 15,136 B / sha
`8630c91a75a2eb43…`, mtime 16:14:31 −03:00; self-label "Design lane: PREP-M9 …
freeze 2026-10-14T19:14Z"). It is the same pattern as rounds 5/6/7 (the next
round's plan appearing in the current round's window): **do not fold it into
the round-8 commit** unless the finalizer intends the round-7 precedent (where
`plans/round-8.plan.md` *was* committed with the round-7 landing). Nothing
else landed: gate sha `90d50cdd…` unchanged at 19:15Z; `git status
--porcelain` shows only this draft + `plans/round-9.plan.md`.

**v2b (19:16:05Z): the round-8 gate lane has begun — the baseline moved.**
`tools/mado-verify.sh` is now modified in the worktree: 1,760 L / 76,187 B /
sha `6058290731bfc0b2d54fcd765d3f167b58c860feb33bba1d67ea3e0d0712e25a`,
mtime 16:15:56.11 −03:00, `git diff --numstat` **+7/−2** vs the committed
revision. Readings at this instant: `grep -c 'row omarchy'` → 0 (no omarchy
rows yet), `grep -c stub` → 9 (same as the committed revision — that count
does not discriminate; the sha and the selftest count do). This is another
lane's single-writer work; this scribe
lane read it, never touched it. Consequence for the record: every gate pin in
this draft names the **round-7-landed** revision `90d50cdd…` as the v1 baseline;
the finalizer must re-pin from the commit, never from this note. The poll
targets above are live: re-run `sha256sum tools/mado-verify.sh` and
`bash tools/mado-verify.sh --selftest` before quoting anything.

⟨Append v2+ here as artifacts land: each update tagged with its own
measurement time; v1 numbers above stay for provenance. Re-run the §9
checklist from the landed revision, not from this draft's before-state.⟩
