# Snapshot-diff receipt r9 — first real diff across the round-9 gate edit (M9-3)

Date 2026-10-14 (training round 9, lane M9-3). Marks: **O** = observation
(command output / receipt bytes re-quoted); **I** = inference from measured
bytes; **U** = unknown. Single host, one window (bash 5.3.15, 19:58–20:19Z).
Scratch: `/tmp/w9-mado-m93/` — snapshots `before.snap`, `before2-ctl.snap`,
`after.snap`, `after2.snap`, `after2-ctl.snap`, `after3-ctl.snap`; logs
`before.run.log`, `before.selftest.log`, `after.run.log`,
`after.selftest.log`, `after2.run.log`, `after2.selftest.log`,
`after3-ctl.run.log`, `diff.log`, `diff2.log`, `diff-12.log`, `poll.log`,
`settle.log`, `settle2.log`, `settle3.log`; gate copies
`after-gate-bytes.sh`, `after2-gate-bytes.sh`.

## 0. The receipt pair (O)

The round-9 gate edit (lane M9-1: the `theme` plane lands as rows + the
census regex widening + the mutation re-cut) was watched live; the pair below
straddles it. This is the round-8 `--snapshot` / `--snapshot-diff` mode's
first real (non-hermetic) use.

    bash tools/mado-verify.sh --live --snapshot /tmp/w9-mado-m93/before.snap   # 19:58:54Z
    bash tools/mado-verify.sh --live --snapshot /tmp/w9-mado-m93/after2.snap   # 20:07:06Z
    bash tools/mado-verify.sh --snapshot-diff before.snap after2.snap          # rc 1

- **Before** — gate sha256 `7da4ec50…f2f4f`, 131 612 B, 2 887 `wc -l` lines,
  mtime 16:29:03 −03:00 (the round-8 settled revision). `--live` →
  `MADO_VERIFY: CLEAN (43 pass, 7 notes)`, rc 0; snapshot rows=50 (pass=43
  fail=0 unknown=0 skip=0 note=7), scope=live, root=/home/vgpnk, created
  19:58:55Z. `--selftest` → `217/217`, rc 0.
- **After** — gate sha256 `93e43f8f…00095`, 150 103 B, 3 231 `wc -l` lines,
  mtime 17:05:32 −03:00. `--live` → `CLEAN (52 pass, 8 notes)`, rc 0;
  snapshot rows=60 (pass=52 … note=8), created 20:07:07Z. `--selftest` →
  `268/268`, rc 0; `PIN_MADO` re-cut to `dc7c4141…db62` (10 KILLED table).
- The edit was observed mid-flight and the after leg waits for a 60 s settle
  (`settle.log`/`settle2.log`): `7da4ec50` → `4a2730a2` 20:01:57Z →
  `6e8cd830` 20:02:03Z → `1e9da5e6` 20:02:20Z → `5b6ace8e` 20:02:23Z →
  `62f81516` 20:02:38Z (theme rows appear, 27 sites) → `cbc0f5f7` 20:02:56Z →
  `31364115` settled 20:04:32Z → `93e43f8f` 20:06:01Z, settled 20:07:01Z.
  Gate sha re-measured immediately before and after each snapshot run:
  unchanged in every leg; the after revision then held through 20:19Z.
- Exit-code semantics of the mode (so `rc 1` is not misread): `MADO_DIFF:
  SAME` exits 0, `CHANGED` exits 1 by contract, `SETUP` exits 2. The pair's
  rc 1 = “the receipt pair brackets a change”, not a failure.

## 1. Controls — the noise floor is zero (O)

| # | pair (same revision) | window | verdict | rows |
|---|---|---|---|---|
| C1 | `before.snap` → `before2-ctl.snap` | 19:58:55Z → 20:00:28Z (93 s) | `MADO_DIFF: SAME` | 50→50 |
| C2 | `after.snap` → `after2-ctl.snap` (at `31364115…`) | 20:04:38Z → 20:04:47Z (9 s) | `MADO_DIFF: SAME` | 60→60 |
| C3 | `after2.snap` → `after3-ctl.snap` (at `93e43f8f…`) | 20:07:07Z → 20:19:12Z (12 min) | `MADO_DIFF: SAME` | 60→60 |

All three: every class 0, `detail-changed=0`. [I] Every line of the pair diff
below is edit-attributable, not ambient drift — the live substrate (pids,
details) held still across a 12-minute window at the after revision.

## 2. The diff — raw (O; `diff2.log`, quoted verbatim)

    DIFF_LEFT: /tmp/w9-mado-m93/before.snap created=2026-10-14T19:58:55Z scope=live root=/home/vgpnk gate-sha256=7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f tool=mado-verify.sh v1 (mado-shokunin round 5 / M5-2)
    DIFF_RIGHT: /tmp/w9-mado-m93/after2.snap created=2026-10-14T20:07:07Z scope=live root=/home/vgpnk gate-sha256=93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095 tool=mado-verify.sh v1 (mado-shokunin round 5 / M5-2)
    DIFF_SCOPE gate-sha256: 7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f → 93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095
    DIFF_ROW appeared theme.name.read: -→PASS
    DIFF_DETAIL theme.name.read new: theme.name = 'matte-black' (one line, machine-name shape)
    DIFF_ROW appeared theme.chain.hypr_include: -→PASS
    DIFF_DETAIL theme.chain.hypr_include new: line 13 imports current/theme/hyprland.conf (target exists)
    DIFF_ROW appeared theme.chain.hyprlock: -→PASS
    DIFF_DETAIL theme.chain.hyprlock new: line 1 imports current/theme/hyprlock.conf (target exists)
    DIFF_ROW appeared theme.chain.waybar_css: -→PASS
    DIFF_DETAIL theme.chain.waybar_css new: line 1 imports current/theme/waybar.css (target exists)
    DIFF_ROW appeared theme.chain.alacritty: -→PASS
    DIFF_DETAIL theme.chain.alacritty new: line 1 imports current/theme/alacritty.toml (target exists)
    DIFF_ROW appeared theme.chain.mako_link: -→PASS
    DIFF_DETAIL theme.chain.mako_link new: symlink → .config/omarchy/current/theme/mako.ini (inside .config/omarchy/current/theme)
    DIFF_ROW appeared theme.chain.walker_css: -→PASS
    DIFF_DETAIL theme.chain.walker_css new: package 'omarchy-default' style.css imports current/theme/walker.css (target exists)
    DIFF_ROW appeared theme.chain.swayosd_css: -→PASS
    DIFF_DETAIL theme.chain.swayosd_css new: style.css imports current/theme/swayosd.css (target exists)
    DIFF_ROW appeared theme.wallpaper.link: -→PASS
    DIFF_DETAIL theme.wallpaper.link new: symlink → .config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg (inside .config/omarchy/current/theme/backgrounds)
    DIFF_ROW appeared theme.parts.declared_only: -→NOTE
    DIFF_DETAIL theme.parts.declared_only new: declared-only, consumer absent: foot.ini(foot) kitty.conf(kitty) ghostty.conf(ghostty) helix.toml(helix) vscode.json(code) keyboard.rgb(asusctl)
    DIFF_COUNTS: pass 43→52 fail 0→0 unknown 0→0 skip 0→0 note 7→8
    MADO_DIFF: CHANGED (rows 50→60; regressed=0 recovered=0 flipped=0 relaxed=0 relabeled=0 appeared=10 vanished=0; detail-changed=0; scope=1)

## 3. Classes — what changed (O + I)

| class | count | what |
|---|---|---|
| scope | 1 | `gate-sha256` moved; `tool`, `root`, `scope` unchanged (the gate version string still self-labels round-5 text — unchanged by this edit) |
| appeared | 10 | the `theme` plane's file rows: 9 PASS + 1 NOTE; none existed before |
| regressed · recovered · flipped · relaxed · relabeled · vanished · detail-changed | 0 each | the 43 pre-existing verdict rows and 7 pre-existing NOTEs are unmoved, detail byte-for-byte |

[I] The receipt reads the round's story in one object: the `theme` plane
arrived (10 rows), nothing else moved, no row regressed, and the only non-row
change is the gate's identity.

**First settle as a leg (O).** The first settled revision `31364115…`
(20:04:32Z) yields the *same* class table against `before.snap` (`diff2.log`
vs `diff.log` agree line-for-line apart from the scope sha). Between the two
settles only the gate moved:

    DIFF_SCOPE gate-sha256: 31364115… → 93e43f8f…
    MADO_DIFF: CHANGED (rows 60→60; … appeared=0 vanished=0; detail-changed=0; scope=1)   # rc 1

i.e. `--snapshot-diff` separates “the gate changed” (scope) from “the
observation changed” (rows): a revision that alters only the gate reports
scope 1 with zero row classes — measured, not asserted.

## 4. What the edit contains, per the gate's own bytes (O)

- `theme` plane id; rows landed from `theme-wallpaper-plane.md` §6 —
  **file rows only**; the gate says so itself at `:3004-3006` (“…the FILE
  rows only (the note's live rows, swaybg argv and the theme-name display
  agreement, are not landed here)”). The two live rows
  (`theme.wallpaper.live`, `theme.name.display_agree`) are absent at the
  after revision (grep: 0 sites); `theme.choice` stays today's
  `live.theme.current` NOTE.
- Hermetic suite for the new rows: scenarios T1–T9 at `:777-…`, 51 assertion
  labels; `--selftest` 217/217 → 268/268 (+51 = exactly the T labels). At
  the first settle `31364115…` the suite read `267 passed, 1 failed` — R10,
  derived target vs the recorded pin (`dc7c4141…` got, `d2bcdb31…` want);
  the `93e43f8f…` settle carries the re-cut (`PIN_MADO` now `dc7c4141…`).
- Census widening: the suite's plane-prefix alternation is now
  `/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) /` (`:387`,
  `:391`, `:406-410`) — 8 plane ids; `row theme` call sites 0 → 27.
- `git status` at capture: ` M tools/mado-verify.sh` plus other lanes'
  untracked artifacts (`corpus/knowledge/walker-deep-r9.md`,
  `plans/round-9-record-draft.md`, `plans/round-10.plan.md`).

## 5. Spot-checks (three)

1. **Determinism + reconciliation.** `--snapshot-diff before.snap after2.snap`
   re-run twice → byte-identical output (sha256 over the piped output
   `9b4236ee516a3405…`, rc 1 both). `MADO_DIFF: CHANGED` totals reconcile
   with the snapshot headers: rows 50→60; 43+7=50, 52+8=60; appeared=10 =
   (+9 pass) + (+1 note); vanished=0.
2. **Pins vs receipt fields.** `sha256sum tools/mado-verify.sh` at each
   capture == the snapshot's `gate-sha256:` field (`7da4ec50…` /
   `93e43f8f…`); `created:` (19:58:55Z / 20:07:07Z) matches the run logs;
   `# rows:` equals the `row|` line count on disk (50 / 60); the run
   verdicts (`CLEAN 43/7` / `CLEAN 52/8`) equal the snapshot counts.
3. **Substrate cross-check of appeared rows (read-only).**
   `cat ~/.config/omarchy/current/theme.name` → `matte-black`, 1 line, 12 B
   == `theme.name.read` detail; `~/.config/mako/config` → symlink to
   `…/omarchy/current/theme/mako.ini` == `.mako_link` detail; `sed -n 13p
   ~/.config/hypr/hyprland.conf` → `source = ~/.config/omarchy/current/theme/hyprland.conf`
   (target 143 B) == `.hypr_include` detail; `~/.config/omarchy/current/background`
   → `…/backgrounds/0-ship-at-sea.jpg` == `theme.wallpaper.link` detail.

## 6. Unknowns

- **U1 — the edit's end.** The gate stood at `93e43f8f…` from 20:05:32Z
  through 20:19Z (one 12-minute same-revision control) but later revisions
  are unresolved here. The pair is per-revision; `before.snap` is the frozen
  pre-edit side for any later re-diff.
- **U2 — the live theme rows.** Not landed at the after revision; whether
  the round lands them under the omarchy stub idiom or exempts them by name
  is beyond this receipt (the gate's `:3004-3006` states the file-only
  landing).
- **U3 — walker live-surface rows (stage b)** and the `walker-deep.md`
  §10/§11 errata are outside this pair's window (no socket/D-Bus row at
  `93e43f8f…`).
- **U4 — the regression receipt at the widened revision** is the gate
  owner's (M9-1). This lane ran no `--regression`, no mutation sweep; the
  re-cut is evidenced here only by the suite going 267+1 red → 268/268 green
  and `PIN_MADO`'s new value.
- **U5** — single host/toolchain, one window; the controls cover minutes,
  not the mode's day-scale purpose.
- **U6 — the write lock.** The after leg is a snapshot of a moving file's
  settled state; byte copies of both after revisions are kept in scratch
  (`after-gate-bytes.sh`, `after2-gate-bytes.sh`) for the record.

## 7. Recommendation

Quote §2's receipt lines in the round record (D3's receipt slot); to extend
after further gate edits, re-snapshot and diff against the frozen
`before.snap` — the pair needs no re-baselining.

## 8. Corroboration — independently landed receipts (O; appended 20:22Z)

Neither report below was consulted for this note's own measurements (they
landed after them); the agreement is independent.

- **AUD-M9** (`reports/r9-aud-m9.md`, C5b): the audit lane built its *own*
  pre/post pair (file-plane scope: `7da4ec50…` 31 rows → `93e43f8f…` 41
  rows, same root) and diffed it to the same classes quoted in §2 —
  `MADO_DIFF: CHANGED (rows 31→41; regressed=0 … appeared=10 vanished=0;
  detail-changed=0; scope=1)` rc 1, "each of the ten theme rows named as
  `DIFF_ROW appeared <id>: -→PASS/NOTE`". Different scope from this
  receipt's live-scope pair (60 rows); the appeared set is the same ten ids.
- **VER-M9** (`reports/r9-ver-m9.md`): at `93e43f8f…` stable ≥100 s before
  its runs and sha-identical before/after them (this receipt's C3 control
  covers 12 min at the same revision); `--selftest` 268/268 [O]. Its window
  observed the gate move six times — `7da4ec50` → `d44a8933` → `cbc0f5f7` →
  `31364115` → `d9ae12f9` → `93e43f8f` [O] — a coarser sample that brackets
  §0's observed sequence (`d44a8933`/`d9ae12f9` fell between this lane's
  polls; every endpoint agrees).