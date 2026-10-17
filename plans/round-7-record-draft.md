# mado round-7 record — scribe prep DRAFT (SCR-M7)

Draft v1 window: 2026-10-14 18:18–18:33Z (local 15:18–15:33 −03:00). Lane SCR-M7.
**v2a (18:26Z): the stage-(c) note landed — `corpus/knowledge/walker-live-surface.md`
(M7-3); read §10.** **v2+ updates append to §10** — read §10 first if the scribe
window shut before finalization. This file is scribe scratch product for the round-7 finalizer —
**not the record**. Nothing outside this file was written by this lane in the
repo; scratch `/tmp/w7-scr-m7/` (`selftest.log`, `nolive.log`, `live.log`).
All probes read-only (file reads, `sha256sum`/`wc`/`stat`/`git` read verbs,
`pgrep`/`busctl`/`systemctl`/`find`, `omarchy theme current`, the gate's own
hyprctl read verbs); no substrate file under `~/.config`/`~/.local` written; no
live session disturbed; no network command.

Headline prep (measured at v1): **all three ordered stages are still unlanded** —
`--regression` is refused by the gate's argument parser (usage error, rc 2), the
theme plane still has no verdict-bearing row (`live.theme.current` is a NOTE,
gate `:1102-1108`), and the walker live surface still reads version + services
only (`:1077-1101`) with no socket / D-Bus-owner / layer-invariant rows. What the
scribe can pre-measure is the pre-state (§1), the input pins the three lanes will
consume (§5), the case the (a) lane needs from the round-6 record (§3.1 —
**present**, so the plan's SETUP-refusal branch is not forced [INF from the
record]), and the record debt the round-7 commit should repay (§1.4, §4).

State at v1 cut (all measured 18:20–18:23Z, read-only): HEAD `c8f6667`
("probation round 6 (training r5): see LOG"); `git status --porcelain` empty at
18:20Z; gate `tools/mado-verify.sh` 1,186 L / 50,126 B / sha256
`c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171`, selftest
`53/53` rc 0, live `MADO_VERIFY: CLEAN (35 pass, 4 notes)` rc 0; round-7 plan
committed: `plans/round-7.plan.md` 135 L by `wc -l` (136 editor view) / 8,689 B /
sha `d4e23e8159ff4441…`.

Reading key: **⟨PENDING⟩** = must be resolved at finalization; every other number
names the command that produced it at v1 time. Tags: **[OBS]** measured, **[INF]**
inference from measured code/record, **[UNK]** unknown. Counts on `.md` notes use
`wc -l` (notes without a trailing newline show editor view = +1; this draft also
ends without a trailing newline — `tail -c 1` → `0xa9`, so `wc -l` counts one
fewer than the editor view; re-measure both at finalization).

## 0. Round-7 frame

- Plan (worktree, committed at `c8f6667`): `plans/round-7.plan.md` — 135 L,
  sha `d4e23e8159ff4441…`. Axis move: **operability + coverage** — ONE move,
  three ordered stages: (a) the gate's own proof becomes a gate
  (`--regression` mode); (b) the gate's declared census closes over the
  theme/wallpaper plane; (c) the walker live surface. Ordering: **(b) and (c)
  are gated on (a) green** — "they widen the very census and live plane the
  mutation spec's clauses guard"; if (a) cannot land, (b)/(c) do not ship and
  the round says why.
- Claim (a) — `tools/mado-verify.sh --regression`: re-runs the round-6 mutation
  case (case artifacts resolved from the round-6 record/commit at dispatch). If
  the record leaves no case, (a) refuses with SETUP and the round reports, no
  headline. Contract mirrors tameshi's `--regression`
  (`tameshi-shokunin/tools/mutate-and-run.sh:64-95`): target pin = the gate
  revision the sweep measured (a live mismatch is a SETUP refusal; the recorded
  table is revision-tied); suite `bash "$MUTANT" --selftest`; pre-stated band —
  defects exactly the recorded count, |killed − recorded| ≤ 1, ≤ 1 verdict flip,
  control green, `MUTATE_RESTORE: OK` required before any PASS; outside the band
  is FAIL; a case that cannot run is SETUP. Token `MADO_REGRESSION: PASS|FAIL|SETUP`
  (never `MADO_VERIFY:`); exit 0/1/2 aligned by meaning; `--target/--defects/--suite`
  refused (usage). The harness is consumed read-only (a needed change is a
  recommendation to tameshi, never a patch); scratch only under
  `/tmp/mado-verify-regression.*`. **From round 7 every gate-widening claim
  carries `MADO_REGRESSION: PASS`.**
- Claim (b) — theme/wallpaper plane rows. File plane: `theme.name` parsed and
  pinned; `current/background` symlink resolves inside
  `current/theme/backgrounds/` to a non-empty file; consumer declarations
  resolve for installed consumers only. Live plane: `omarchy theme current`
  agrees with `theme.name` under the measured normalization rule (`Matte Black`
  ↔ `matte-black`); swaybg argv names the background symlink and the level-0
  `wallpaper` layer pid == swaybg pid. The theme *choice* stays NOTE
  (operator-owned); chain *integrity* becomes verdict input; every mutating verb
  (`omarchy theme set`; `omarchy-theme-bg-*`) stays fenced. Unresolved theme
  parts (`walker.css`, `swayosd.css`, `btop.theme`, `themed/*.tpl.sample`
  rendering) get their exact probe recorded, never an inferred consumer.
- Claim (c) — walker live surface: sockets exist with mode + size
  (`srwxr-xr-x`, 0 B); `dev.benz.walker` owner pid == the walker pid; layer
  invariant — if a walker namespace appears in `hyprctl -j layers` its pid ==
  walker pid; absence is a NOTE (the launcher is closed; the gate never opens
  it). Version/services rows stand. Rendered UI and the socket protocol stay
  UNKNOWN by constraint; resolutions append to `walker-deep.md` §10/§11 as
  errata.
- Anti-claim (as written): a kill-rate outside the band is a FINDING
  (append-only errata, not smoothed); any unverifiable surface reads UNKNOWN,
  never CLEAN; the gate observes the theme plane and never sets it; absent
  consumers stay declared-only rows; the normalization rule is measured on this
  host's one theme, not assumed general; no compositor/session mutation (no
  launcher open, no socket connect, no `omarchy theme set`); dependencies
  read-only — tameshi harness and omarchy payload untouched.
- Measure: `MADO_REGRESSION: PASS` + `REGRESSION_TABLE`-shaped lines (case,
  expected vs observed, band, flips, restore sha before = after, target sha) +
  selftest count before → after + gate row census before → after by plane
  prefix (the selftest's prefix awk `:352/:356` extended for any new plane id —
  counted) + theme chain rows vs the design-time pins + walker live rows + SKILL
  gate section gains the mode + SCORECARD move row + LOG entry carrying the
  commands.
- **Design-time pins in the plan are superseded by the round-6 landing** [OBS]:
  the plan was frozen 17:40Z against the round-5 gate (`d7edaab4…`, 1,098 L)
  and HEAD `c03c249` with round-6 artifacts untracked; at dispatch the landed
  state is HEAD `c8f6667`, gate `c4c1afb7…` (1,186 L), and the three round-6
  artifacts committed. The record cites landed pins; §1 carries them
  re-measured. Two plan numbers are stale for the same reason: "selftest count
  before → after (28 → 28+N)" reads **53 → 53+N** at the landed base, and the
  plan's walker/theme gap line anchors (`:1014-1021` theme NOTE,
  `:989-998`/`:1000-1011` walker) sit at the round-5 revision — current
  anchors are `:1102-1108` / `:1077-1101` [OBS].

## 1. Pre-state at v1 (round 6 landed; round 7 in flight)

1. **Repo identity** [OBS, 18:20–18:23Z]: HEAD `c8f6667` (round-6 landing,
   committed 15:17:26 −03:00; `git show --stat`: LOG +1, SCORECARD +1, SKILL
   +193, gate-mutation-proof +168, omarchy-drift-watch +287,
   remaining-planes-census +334, round-6 draft +459, round-7 plan +136, gate
   +88 — 9 files, +1,666/−1). `git status --porcelain` empty at 18:20Z. Pins:
   SKILL 709 L / 58,143 B / `72196e7e967f4516…`; SHONEN 12 L / 1,688 B /
   `edace65e13c8ad20…` (4/4 `[x]`, PROBATION COMPLETE per `c03c249`); SCORECARD
   18 L / 8,813 B / `e23b75fed1ebea28…`; LOG 296 L / 20,444 B /
   `62e9014c7e0bb76e…`; corpus/README.md 19 L / 12,709 B / `2dd274f5e270e65b…`
   (8 coverage rows); PROVINCE 18 L / 891 B / `7aad7b863dc3c10b…`.
2. **Gate identity and runs** [OBS]: `tools/mado-verify.sh` 1,186 L / 50,126 B /
   `c4c1afb7…a5171` = the round-6 landed revision, unchanged from
   `gate-mutation-proof.md` §5. Runs (read-only): `--selftest` →
   `MADO_SELFTEST: 53/53 assertions passed` rc 0; `--no-live` →
   `MADO_VERIFY: CLEAN (17 pass, 2 notes; file plane only)` rc 0, `counts:
   pass=17 fail=0 unknown=0 skip=1 note=2`; live →
   `MADO_VERIFY: CLEAN (35 pass, 4 notes; file + live planes verified
   read-only)` rc 0, `counts: pass=35 fail=0 unknown=0 skip=0 note=4`;
   `boundary.readonly` PASS both, combined sha `bb2639d9a980…`. Logs
   `/tmp/w7-scr-m7/{selftest,nolive,live}.log`.
3. **Gate census (before)** [OBS]: output rows 39 = hypr 9 / hypr-live 20 /
   waybar 4 / walker 1 / terms 4 / gate 1. Row *sites*: 106 `row` + 6
   `row_from_rc` = 112; by first-arg prefix — hypr 23, hypr-live 57, waybar 17,
   walker 2, terms 10, gate 3. Note: the walker *live* rows print under the
   `hypr-live` prefix (`live.walker.version`, `live.walker.services` — live log
   rows 30–31), so a plane-prefix census does not separate them; count
   `live.walker.*` by row id.
4. **`--regression` pre-state** [OBS]: `bash tools/mado-verify.sh --regression`
   → `usage error: unknown argument '--regression'`, rc 2. Stage (a) is absent
   at the v1 cut; the mode must take the exit-2 usage channel when it lands
   (its own `--target/--defects/--suite` refusal is a second usage path).
5. **Round-6 artifact pins** [OBS]: `corpus/knowledge/gate-mutation-proof.md`
   167 L / 10,693 B / `716836ca1bf3484a…`; `omarchy-drift-watch.md` 287 L /
   18,714 B / `49f5a9a14776d83d…`; `remaining-planes-census.md` 333 L /
   20,512 B / `710e3e289643f2ff…`; `plans/round-6-record-draft.md` 459 L (editor
   view) / 28,813 B, committed. These are the (a)/(b)/(c) input artifacts.
6. **Record debt carried into round 7** [OBS, still unpaid after round 6]:
   1. `corpus/README.md` — 8 rows; missing one row per note for
      `idle-lock-plane.md` (r4; 381 L / 23,118 B / `a0597be96c107799…`),
      `province-accuracy-selfaudit.md` (r4/r5; 345 L / 24,670 B /
      `7c0a58208dea60e8…`), `walker-deep.md` (r5; 617 L / 38,403 B /
      `0982ba066c72575a…`), `gate-mutation-proof.md`, `omarchy-drift-watch.md`,
      `remaining-planes-census.md` (r6). Ready text: round-4 draft §4b
      (committed, two r4 rows incl. the byte-verified `a0597be9…` addendum),
      round-5 draft §4b (points at round-4 draft §4b verbatim), round-6 draft
      §4b (r5/r6 rows). The self-audit row needs the round-5 update (now 345 L
      `7c0a58208dea60e8…`, addendum = M5-1/VER-M4B receipt).
   2. `SCORECARD.md:16` (round-4 row) and `:17` (round-5 row) are **stubs**,
      and `:18` (round-6 row) is a one-liner; full rows sit in the committed
      drafts (round-4 draft §4c lines ~311-316 — 3 rows: calibration / depth /
      freshness; round-5 draft §4c lines ~287-296 — 2 rows; round-6 draft §4c —
      1 row + the SETUP-refusal branch).
   3. `LOG.md:294/:295/:296` — rounds 4/5/6 entries are one-line summaries; the
      fuller entries from the round-4/5/6 drafts were not applied.
   4. Errata: no `Errata (round 5)` / `Errata (round 6)` block exists
      (`grep -rn 'Errata (round 5|6'` → empty). Still owed (round-5 draft §4e):
      `keybind-rule-semantics.md` §2.3 dispatcher-tail prose (the `swapwindow`
      row is still at `:151` [OBS]), runner V2/V3 receipts, K2 "29/29" scope
      wording (`config-health-report-r3.md:935,:953` [OBS]). Also still present
      for a third round: SKILL `:103`/`:138` spell the tray bus name
      `fr.arrouillard.waybar` (double r; live name `fr.arouillard.waybar`
      [OBS]) — erratum candidate for the SKILL lane, outside a scribe write
      scope.
   5. `corpus/lessons/` still 0 entries (seventh round of the round-1 promise);
      `find corpus -name '*.sh'` → 0 (the round-1 ceiling stays retired via
      `tools/`).
7. **Round-7 lane activity at v1** (shape-only, by scratch dirs; no artifact
   self-labels read, no repo file landed): `/tmp/w7-mado-m7-2/` (theme/wallpaper
   probes — `bg-plane.log`, `chain-decl.log`, `tree-before.sha.txt`; the log
   shows background readlink/stat, 4 background shas, theme `file` types,
   `theme.name` byte count); `/tmp/w7-m7-3/` (walker probes —
   `snapshot-before.txt`, `sockets-before.txt`, `walker-help-*`,
   `newfiles-after.txt`; snapshot carries walker 2.17.0, binary sha
   `64826a8531eac525…`, config shas, `t0.epoch` = `1792002044` = 18:20:44Z);
   tameshi-side `/tmp/w7-t7-4-work/`, `/tmp/w7-t7-4-regr/`,
   `/tmp/w7-tameshi-scr-t7/` — tameshi's own `--regression` receipt
   (`REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1 flips<=1)`,
   `REGRESSION_DATE: 2026-10-14T18:21:15Z`, tool sha `b56c6e57f1b7ae91…`) —
   read as the *idiom* reference, not mado's mode [OBS]. No `/tmp/w7-m7-1`
   directory seen → the (a) lane's scratch not visible at v1 [UNK]; lane
   labels are recorded by artifact self-label at finalization (round-5 lesson).

## 2. Deliverables and ⟨PENDING⟩ slots

### D1 (a) — gate `--regression` mode ⟨PENDING⟩

Must carry, per plan: the token line `MADO_REGRESSION: PASS|FAIL|SETUP` (never
`MADO_VERIFY:`), `REGRESSION_TABLE`-shaped lines (case, expected vs observed,
band, flips, restore sha before = after, target sha), the exit map 0/1/2 aligned
by meaning, the usage refusal of `--target/--defects/--suite`, scratch under
`/tmp/mado-verify-regression.*`, and the selftest count before → after at the
landed revision. Case source at v1: **`corpus/knowledge/gate-mutation-proof.md`
§1** — spec sha `c7ee75b97c38ac8f…`, tameshi case note
`tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md` (323 L /
24,534 B / `f2d53d495e6c1d8b…`, uncommitted — re-pin before quoting), recorded
table: control GREEN, 10 defects, 10 killed / 0 survived / 0 inconclusive,
kill-rate 100%, `MUTATE_RESTORE: OK`, target sha `c4c1afb7…a5171` before =
after. Because the record leaves a case, the plan's SETUP-refusal branch is not
forced [INF]; it fires only if the dispatch re-resolution finds the artifacts
missing. ⟨PENDING: mode landed? gate sha `c4c1afb7…` → ??; line/byte delta;
selftest 53 → 53+N; receipt lines verbatim; which revision the receipt cites;
whether the widened revision re-ran the case (§6 (d)).⟩

### D2 (b) — theme/wallpaper plane rows ⟨PENDING⟩

Before state [OBS]: the theme plane's only live row is
`live.theme.current NOTE` "operator-owned; not a verdict input"
(`:1102-1108`; two `row hypr-live` sites at `:1104`/`:1108`); the file plane has
no `theme.name` / background-symlink / background-file rows; consumer
declarations are only partially covered (`waybar.style` `:723-726`,
`term.alacritty.theme_import` `:765-768` exist; hypr theme include is covered by
the include-graph census; hyprlock `:1` and the mako symlink are not rows).
⟨PENDING: landed row ids + plane prefix (new `theme`-prefixed plane id? then the
census awk at `:352/:356/:371-375` must be extended — see §3.2); gate sha after;
selftest additions; `MADO_REGRESSION: PASS` receipt on the widening; the
normalization-rule row behaviour (`Matte Black` ↔ `matte-black`); list of
unresolved theme-part probes recorded as rows vs notes.⟩ Note (v2b): the
measured surface landed during the scribe window as a note —
`corpus/knowledge/theme-wallpaper-plane.md` (M7-2), see §10; the gate wiring
stays this deliverable's ⟨PENDING⟩.

### D3 (c) — walker live surface rows ⟨PENDING⟩

Before state [OBS]: walker live = `live.walker.version` (pin 2.17.0) +
`live.walker.services` (app-walker@autostart + elephant active), `:1077-1101`;
file plane = `walker.config` (TOML parse + 4 keys, `:733-747`). Missing rows:
sockets exists + mode + size; `dev.benz.walker` owner pid; layer invariant
(walker namespace pid == walker pid; absence = NOTE). Errata target:
`walker-deep.md` §10 (`:521`) / §11 (`:533`), errata section opens at `:615`
("None yet") — append-only, flag which §11 unknowns resolve (§11.3 is the
socket-protocol unknown: **stays UNKNOWN**; socket existence/owner is what
lands). Note (v2a): the measured surface landed during the scribe window as a
note — `corpus/knowledge/walker-live-surface.md` (M7-3), see §10; the gate
wiring stays this deliverable's ⟨PENDING⟩. ⟨PENDING: row ids, gate sha, selftest
additions, `MADO_REGRESSION: PASS` receipt; whether any walker surface is opened
(it must not be).⟩

### D4 — record debt repayment (record work, not a new claim)

README rows ×6 + round-7 rows ⟨PENDING⟩; SCORECARD rows 4/5/6 replacement +
round-7 row; LOG round-7 entry (§4a) and optionally the fuller 4/5/6 entries;
errata status (§4e). See §4.

## 3. Clause maps — anchor → selftest coverage (before state)

### 3.1 The (a) case and the regression contract

| Clause | Anchor today | Evidence/coverage at v1 |
|---|---|---|
| Recorded case exists (else SETUP) | `gate-mutation-proof.md` §1 table; spec `c7ee75b9…`; tameshi note `f2d53d49…` | **present** [OBS]; SETUP-refusal branch not forced [INF] |
| Target pin = revision the sweep measured | target sha `c4c1afb7…a5171` (before = after) | revision-tied; a live mismatch ⇒ SETUP |
| Band: defects exact, \|killed−recorded\| ≤ 1, ≤ 1 flip, control green, restore OK | tameshi `--regression` contract `mutate-and-run.sh:64-95`; recorded table 10/10/0 | tameshi's own receipt measured: `REGRESSION: PASS (cases=2)` 18:21:15Z [OBS] |
| Token `MADO_REGRESSION:` never `MADO_VERIFY:` | new — no site yet | must be asserted in the new selftest scenarios |
| Exit map 0/1/2 aligned by meaning | new; current gate exit map at header `:12-13`, usage `:71-84` | usage refusal path exists to extend |
| Usage refusal `--target/--defects/--suite` | new | the existing per-arg parse (`:71-84`) is the pattern |
| Scratch `/tmp/mado-verify-regression.*` only | new | grep-able in the landed mode |
| Every gate-widening claim carries `MADO_REGRESSION: PASS` | new orchestration rule | (b)/(c) receipts depend on it |

Structural tension to record at dispatch [UNK at v1]: the recorded table is
revision-tied to `c4c1afb7…`; if (b)/(c) edit the gate *before* (a)'s receipt is
taken, the pin must move — either the receipt is taken at the (a) revision
before widening, or the case re-pins to the widened revision after a fresh
sweep. The record must state which path the round took and which revision the
receipt cites.

### 3.2 The selftest plumbing new rows must clear

The suite's plane-prefix regexes hard-code six ids in **seven** awk sites:
`st_rows` `:352`, `st_row_has` `:356`, `st_counts_agree` `:371-375`. Any new
plane id (e.g. a `theme` prefix for (b)) must extend all seven, or the new rows
are invisible to the suite's counts (a fake-PASS risk the round-6 hardening's
`st_counts_agree` exists to catch). New clause families need their own selftest
scenarios before they may ship (round-6 reading rule 2: "nothing ships wider
without a covering mutant"). Gate helpers to reuse: `st_row_detail` `:361-368`,
`st_rows` `:350-354`.

### 3.3 Current gate rows the two widenings touch

| Plane | Rows today | Widening target |
|---|---|---|
| theme (live) | `live.theme.current` NOTE ×2 sites `:1104/:1108` | chain-integrity rows (file + live) |
| walker (live) | `live.walker.version` `:1080-1090`, `live.walker.services` `:1091-1101` | sockets / D-Bus owner / layer invariant |
| waybar (file) | `waybar.style` theme import `:723-726` | (consumer-side check stays) |
| terms (file) | `term.alacritty.theme_import` `:765-768` | (consumer-side check stays) |

Line numbers are the round-6 revision (`c4c1afb7…`); re-measure at finalization
against the landed gate.

## 4. Record text to apply

### 4a. LOG.md round-7 entry (append after LOG.md:296)

```
- 2026-10-14 — round 7 (training r6): operability + coverage — three ordered
  stages. (a) the gate's own proof becomes a gate: `tools/mado-verify.sh
  --regression` re-runs the round-6 mutation case ⟨fill: case source + spec
  sha; token lines; band verdict; target sha `c4c1afb7…` before = after;
  MUTATE_RESTORE: OK; tool sha `b56c6e57…`; receipt run time⟩. (b) theme/
  wallpaper plane ⟨fill: landed rows + plane prefix; normalization rule
  measured on this host's one theme; theme choice stays NOTE; MADO_REGRESSION:
  PASS receipt⟩. (c) walker live surface ⟨fill: sockets mode/size, D-Bus owner
  pid == walker pid, layer invariant/absence NOTE; errata appended to
  walker-deep §10/§11⟩. Gate census 39 rows → ⟨fill⟩; gate sha `c4c1afb7…` →
  ⟨fill⟩; selftest 53/53 → ⟨fill⟩; live verdict ⟨fill⟩ at the committed
  revision. Record debt repaid: README +⟨fill⟩ rows (6 carried + round-7);
  SCORECARD rows 4/5/6 stubs replaced + round-7 row; ⟨errata applied? list
  block headers⟩. Boundary: gate + harness + omarchy payload read-only; no
  substrate file written; no live session disturbed; no socket opened.
- ⟨If (a) refuses (SETUP): replace the first paragraph with the refusal text —
  (b)/(c) do not ship (plan ordering) — no kill-rate claim.⟩
```

### 4b. corpus/README.md — coverage map rows

Apply the six carried rows in order: round-4 draft §4b's two rows
(`idle-lock-plane.md` — re-measure current 381 L / `a0597be9…`;
`province-accuracy-selfaudit.md` — with the round-5 update 345 L /
`7c0a58208dea60e8…`), round-5's `walker-deep.md` row (617 L /
`0982ba066c72575a…`), then one row per round-6 note as measured
(`gate-mutation-proof.md` 167 L / `716836ca1bf3484a…`; `omarchy-drift-watch.md`
287 L / `49f5a9a14776d83d…`; `remaining-planes-census.md` 333 L /
`710e3e289643f2ff…`). Append round-4 draft §4b's round-4 addenda sentences only
if the errata-status lines are also repaid (§4e). Then one row per round-7 note
as landed ⟨PENDING⟩ (composition follows the existing row shape: note → holds →
sources with probe window; write from the measured artifacts).

### 4c. SCORECARD.md — move-log rows

Replace the three stub/one-line rows (`SCORECARD.md:16-18`) with the committed
full rows: round-4 draft §4c (3 rows — calibration / depth / freshness, lines
~311-316), round-5 draft §4c (2 rows — calibration / operability, lines
~287-296; the operability row must cite the gate at the committed revision,
`c4c1afb7…` with selftest 53/53 after the round-6 hardening — re-measure at
commit), round-6 draft §4c (1 row; fill its ⟨fill⟩s from the landed record:
10 defects / 10 killed / 0 survived; census 39 → 39; drift pins HELD). Then
append round 7:

```
| 7 | operability + coverage | round-6 gate: provably falsifiable but its proof was a one-shot run (no re-runnable regression), and two declared planes (theme/wallpaper, walker live surface) were observed only as notes | gate gains `--regression` ⟨fill: case, band verdict, restore proof⟩; theme/wallpaper chain becomes verdict input ⟨fill: rows; normalization rule; theme choice stays NOTE⟩; walker live surface rows ⟨fill: sockets / owner / layer invariant⟩; every widening carries `MADO_REGRESSION: PASS` | ⟨fill: receipt lines; gate sha `c4c1afb7…` → ??; census 39 → ??; selftest 53 → ??; live verdict at committed revision; scratch `/tmp/…`⟩ |
```

⟨If (a) fails: the round-7 row reads the refusal (SETUP reason, exit 2) and
states (b)/(c) did not ship — no kill-rate headline.⟩

### 4d. SHONEN.md

No box move expected: 4/4 `[x]` since round 5 (`c03c249`); promotion remains the
operator/integrator decision. If the finalizer edits any evidence line, re-apply
the seed-diff check (`PROTOCOL.md:419-431`); otherwise the file stays
byte-identical at `edace65e13c8ad20…`.

### 4e. Errata status

Owed, append-only when applied: the round-5 §4e list (`keybind-rule-semantics.md`
§2.3 dispatcher-tail prose — `swapwindow` row at `:151`; runner V2/V3 receipts;
K2 "29/29" scope wording at `config-health-report-r3.md:935/:953`), the SKILL
`arrouillard` typo (`:103/:138`), and the (c) lane's `walker-deep.md` §10/§11
appends. No round-5/6/7 errata block exists as of v1. Any mutation-sweep
recommendation to tameshi (harness changes, e.g. a stdout-reading kill
criterion for the exit-flatten family) is a recommendation to that lane — record
it in this repo's LOG unknowns, never as a patch.

## 5. Scribe measurements and spot-checks (v1, executed)

1. **Repo pins** (18:20–18:23Z): §1.1 table; round-7 plan 135 L / 8,689 B /
   `d4e23e8159ff4441…`; round-6 draft 459 L / 28,813 B; round-6 artifacts per
   §1.5; walker-deep 617 L `0982ba06…`; idle-lock 381 L `a0597be9…`; self-audit
   345 L `7c0a58208…`.
2. **Gate runs** (read-only): `--selftest` → `MADO_SELFTEST: 53/53 assertions
   passed` rc 0; `--no-live` → `counts: pass=17 fail=0 unknown=0 skip=1 note=2`
   + `MADO_VERIFY: CLEAN (17 pass, 2 notes; file plane only)` rc 0; live →
   `counts: pass=35 fail=0 unknown=0 skip=0 note=4` + `MADO_VERIFY: CLEAN
   (35 pass, 4 notes)` rc 0; row census 39 (§1.3); logs `/tmp/w7-scr-m7/`.
3. **`--regression` refusal**: `usage error: unknown argument '--regression'`,
   rc 2 (§1.4) — re-run at finalization; a landed mode changes this cell.
4. **Live input pins for (b)/(c)** (read-only, 18:20–18:23Z): `theme.name` 12 B
   `matte-black`; `current/background` symlink (71 B link) →
   `…/current/theme/backgrounds/0-ship-at-sea.jpg`, sha `55fa691adfd3fb8a…`
   [OBS; the other three backgrounds also sha'd in the M7-2 scratch]; swaybg
   1203358 `-i …/current/background -m fill`; `hyprctl -j layers` level 0
   `wallpaper` pid 1203358 (== swaybg), level 2 `waybar` pid 1203352 (note:
   stale PIDs in SKILL `:103` text — avoid re-quoting); `omarchy theme current`
   → `Matte Black`; walker 1203471 `--gapplication-service`, elephant 1203474,
   both units `active`; sockets `/run/user/1000/walker/walker.sock` +
   `/run/user/1000/elephant/elephant.sock` `srwxr-xr-x` 0 B (under
   `$XDG_RUNTIME_DIR` **subdirs**, not the root — the round-6 plan's shorthand
   "under `$XDG_RUNTIME_DIR`" is true of the tree); `busctl --user status
   dev.benz.walker` PID=1203471 (== walker pid); consumer declarations:
   `hyprland.conf:13` → theme `hyprland.conf`, `hyprlock.conf:1` → theme
   `hyprlock.conf`, `waybar/style.css:1` `@import "../omarchy/current/theme/
   waybar.css"`, `alacritty.toml:1` `general.import`, mako `config` symlink →
   theme `mako.ini` [OBS].
5. **Tameshi idiom receipt** (read, not run, from `/tmp/w7-t7-4-work/regr.out`):
   `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1 flips<=1)`,
   `REGRESSION_DATE: 2026-10-14T18:21:15Z`, tool sha `b56c6e57f1b7ae91…`,
   workdir kept `/tmp/w7-t7-4-regr`. The fleet idiom is live and current; mado's
   own mode is absent (§1.4) — the record must not cite tameshi's receipt as
   mado's [OBS].
6. **Boundary**: read-only throughout; writes = this draft + `/tmp/w7-scr-m7/`;
   no substrate file written; no live session disturbed; no socket connected;
   no network command.

## 6. Observations (v1)

(a) The plan's design-time state is one round stale by construction (frozen
    17:40Z during the round-6 wave) — superseded pins are listed in §0; the
    record must cite the landed `c8f6667`/`c4c1afb7…` values.
(b) The plan's measure line "selftest count before → after (28 → 28+N)" carries
    the round-5 base; the landed base is 53 (round-6 hardening 28 → 53, merged),
    so the arithmetic stands as 53 → 53+N — finalizer, do not copy "28".
(c) The (a) lane's hardest dependency is already satisfied: the round-6 record
    contains a complete, revision-tied 10-defect case with a spec sha and a
    matching table (0 survivors, restore proof). The SETUP-refusal branch is a
    contingency, not the expected path [INF].
(d) The round's structural tension is the pin-vs-widening order (§3.1): (a)'s
    receipt is revision-tied to `c4c1afb7…`, while (b)/(c) by design edit the
    gate. The record must state the resolution — receipt-before-widening, or a
    re-pin to the widened revision — and the finalizer should check the receipt
    it cites against the gate sha in the same commit.
(e) The selftest's seven hard-coded plane-prefix awk sites (§3.2) are the
    round's likeliest quiet failure: rows can land while the suite never counts
    them. Both widening lanes should add their prefix before their rows.
(f) Record debt is now two rounds deep (README 6 missing rows, SCORECARD 4/5
    stubs, terse LOG 4–6, no errata blocks since round 4). Every round that
    lands more notes without repaying compounds it; §4 is ready-to-apply text.
(g) The walker socket path detail (subdir, not runtime root — §5.4) differs
    from the plan's shorthand; the landed rows should encode the measured path,
    not the plan's paraphrase.

## 7. Unknowns (v1)

1. Whether (a) lands in-window; its band verdict and the receipt's target
   revision (§3.1 tension).
2. Whether (b)/(c) ship at all (gated on (a)); if (a) refuses, the round stops
   and the record says why — no deprecation of round-6 values.
3. Which plane prefix the (b) rows use (new `theme` id vs existing prefixes) —
   decides the census-awk extension and the before/after layout.
4. Whether the walker socket/owner rows stay `hypr-live`-prefixed like the
   existing `live.walker.*` rows or move under a walker-live group.
5. Round-7 lane labels/attributions: `/tmp/w7-mado-m7-2` (theme-plane probes),
   `/tmp/w7-m7-3` (walker; its self-label M7-3 is now landed in the note),
   tameshi-side `t7-4`; `/tmp/w7-mado-m7-4` and `/tmp/w7-aud-m7-*` seats appeared
   during the window (18:25Z) — no assignment map visible from inside this lane
   [UNK]; record by artifact self-label.
6. Which named seats deliberate this round: audit threads `/tmp/w7-aud-m7-{gate,
   poll,probe,regression}` and `/tmp/w7-ver-t7-leg` exist [OBS 18:25Z]; no verdict
   artifact seen yet — the record cites whatever lands, by sha, or says none.
7. Whether the finalizer repays D4 (record debt) in the round-7 commit (this
   draft assumes yes — cheapest correct state).
8. `corpus/lessons/` — seventh round at 0 entries; no lane chartered yet.

## 8. Falsifiable next-iterations (carry + new)

- Land (a) with its receipt; state which revision the receipt cites; re-run at
  the committed revision (§3.1).
- (b)/(c) rows only under `MADO_REGRESSION: PASS`; extend the seven awk sites;
  count new rows by prefix before/after.
- Walker socket rows use the measured path (`$XDG_RUNTIME_DIR/walker/walker.sock`);
  the socket protocol and rendered UI stay UNKNOWN (§11.3 of walker-deep not
  closed by existence evidence).
- Theme choice stays NOTE; chain integrity becomes verdict input; the
  normalization rule stays host-local.
- Repay record debt (README ×6+; SCORECARD 4/5/6; LOG 4–6 fuller entries; owed
  errata incl. the SKILL typo).
- `corpus/lessons/round-7.md` — dir still empty; the round-1 promise fails a
  seventh round unless a lane is chartered.
- Durability: fold receipt lines + tool sha + target sha + gate sha into the
  record (scratch does not survive).

## 9. Finalization checklist (mechanical, ordered)

1. Re-measure §1.1/§1.2 anchors + §5.4 pins; note any drift as freshness rows.
2. Read the landed (a) mode; verify its token/exit map/usage refusal; capture
   the receipt lines verbatim; verify the target sha it names equals the gate
   revision it claims and that the restore proof is before = after.
3. Run the landed gate at the revision being committed: `--selftest`,
   `--no-live`, live; compute the census before (39) → after by plane prefix;
   fill D1/D2/D3/§4a/§4c.
4. For (b)/(c): verify every new row id is covered by the suite's prefix awk
   sites; verify each widening carries a `MADO_REGRESSION: PASS` receipt; list
   unresolved-probe rows vs notes.
5. Fill (b) chain rows against the §5.4 pins; record the normalization-rule
   row's behaviour on this host's one theme.
6. Apply 4a (LOG), 4b (README rows incl. the six carried), 4c (SCORECARD:
   replace 16-18 + append round 7), 4d (SHONEN — likely no-op), 4e status.
7. Commit under the lane identity; freeze every cited sha in the entry; check
   the gate/harness/note shas appear.
8. If (a) refused or is red at commit: record the SETUP/refusal text, mark
   (b)/(c) unsent, and keep this draft as the record's ancestry.

## 10. v2 update — artifacts landing during the scribe window

**v1 cut (18:33Z): nothing landed.** No round-7 repo artifact existed at the v1
cut: `git status --porcelain` empty at 18:20Z; `--regression` refused;
`live.theme.current` still NOTE-only; walker live rows still version+services.
Lane activity was scratch-only (§1.7). The plan ordering says the likely landing
order is (a) then (b)/(c) — poll for: `grep -n 'MADO_REGRESSION' tools/mado-verify.sh`
(a present), a gate mtime/sha change, new `row` sites for theme/walker, and new
files under `corpus/knowledge/`.

**v2a (18:26Z): stage (c)'s measured surface landed — as a NOTE, not as gate
rows.** `corpus/knowledge/walker-live-surface.md` appeared untracked (299 L /
19,111 B / sha `99d061c2efc7a06c…` at this read; may still grow — re-measure).
Self-label: "Lane: mado-shokunin. Assignment M7-3 (round 7)"; probe window
18:20:44–18:23:13Z; scratch `/tmp/w7-m7-3/`. It is the walker surface the
stage-(c) gate wiring would cite, and says so itself: "The round-7 plan's
stage-(c) *gate wiring* (live rows for sockets / D-Bus owner / layer invariant)
is likewise not in this file — this note is the measured surface it would
cite". It did **not** append the `walker-deep.md` §10/§11 errata either
("the lane owning walker-deep.md should carry it there, append-only").
Record consequences: (i) D3's gate rows stay ⟨PENDING⟩ — the wiring is a
separate, (a)-gated write; (ii) the `walker-deep.md` §10/§11 errata append is
now substance-ready and still owed — the note's §5 ledger is the text to carry
(§11.3 socket protocol and §11.9 rendered UI stay UNKNOWN by constraint; §11.1 /
§11.5 / §11.6 sharpened, not closed); (iii) `corpus/README.md` gains this
note's row; (iv) the note's boundary proof re-confirms the §5.4 pins (socket
mode/size/mtime identical 18:20:44 → 18:23:13Z; layers wallpaper 1203358 /
waybar 1203352; walker config sha `fecf71fa4253803e…`); (v) the note pins
`walker --version` = `2.17.0\n` 7 B and binary sha `64826a8531eac525…` —
matching §1.7's M7-3 scratch snapshot [OBS].
Also at 18:25Z: new lane dirs `/tmp/w7-mado-m7-4` (round-7 finalizer-side) and
the audit seats `/tmp/w7-aud-m7-{gate,poll,probe,regression}`; no further repo
artifact (gate sha `c4c1afb7…` unchanged; `--regression` still refused).

**v2b (18:27Z): stage (b)'s note also landed — same note-first shape.**
`corpus/knowledge/theme-wallpaper-plane.md` (393 L / 27,593 B / sha
`e766dd10df5bb217…` at this read; may still grow — re-measure), self-label
"round 7, lane M7-2", probe window 18:19:59–18:23Z, scratch `/tmp/w7-mado-m7-2/`.
It says so itself: "**No verdict token** is issued here … landing gate rows is
stage (b), gated on stage (a) green per `plans/round-7.plan.md:110-113`". It
carries §2's 24-file + 4-background census with §2.1 wall-plane pins; §3 the
declaration → link → live path; §4 consumer chains (incl. §4.1 declared-only
and §4.2 inert artifacts); §5 the theme-name normalization joint measured from
both scripts; §6 **the stage-(b) row spec**; §7 unresolved parts as exact
probes; §10 an append-only errata section; §11 hand-forward. Record
consequences: (i) D2's gate rows stay ⟨PENDING⟩ for the same reason as D3;
(ii) `corpus/README.md` gains this note's row; (iii) the note's §6 row spec is
the landing text for a future (a)-green round; (iv) this note's own §10 is its
errata append target.
**Round-level reading at the v2b cut: (a) is still absent (`--regression`
refused; gate sha `c4c1afb7…` unchanged at 18:26:24Z), while both widenings
shipped as measured notes.** If (a) does not land before the commit, the
round's (b)/(c) claims are met as *measured surfaces* (notes) and the record
must state that plainly — no shipped gate rows, no `MADO_REGRESSION` receipt,
plan ordering honored (§0). Also at 18:26Z: `plans/round-8.plan.md` appeared
untracked (206 L / sha `ffcc058aa17755d9…`; freeze 18:25Z) — another lane's
prep; **do not fold into the round-7 commit** (same pattern as rounds 5/6).

**v2c (18:27Z): the two notes are still moving — re-pin at commit.** Re-measured
both immediately after v2b: `walker-live-surface.md` 299 L / 19,111 B /
`99d061c2efc7a06c…` → **300 L / 19,203 B / `2bbb9609283f2d81…`** (grew);
`theme-wallpaper-plane.md` 393 L / 27,593 B / `e766dd10df5bb217…` →
**393 L / 27,593 B / `58b12f71cf0c9ef6…`** (equal size/lines, sha moved — read
as a live-write window; the v2b §-content summary stands as of its own read).
Gate unchanged (`c4c1afb7…`; `--regression` rc 2 at 18:27:02Z). Rule for the
finalizer: **every pin in this draft that names a round-7 artifact is a
provisional read — freeze it from the committed revision, never from here.**

⟨Append v2+ here as artifacts land: each update tagged with its own
measurement time; v1 numbers above stay for provenance. Re-run the §9 checklist
from the landed revision, not from this draft's before-state.⟩
