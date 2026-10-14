# VER-M9 — round-9 theme-arm verification (independent re-run: one arm's selftest case path + the live arm)

Lane VER-M9, 2026-10-14 (round-9 32-lane wave, training r8). Window
19:58–20:12Z (local 16:58–17:12 −03:00); dispatch contract: re-run one arm's
selftest case + the live arm independently, poll with a 25-min cap, do not
edit. Poll: `/tmp/w9-ver-m9/poll.sh` → `poll.log` (20 s cadence from
19:58:53Z; round-9 landing detected 20:02:13Z); `watch.sh` → `watch.log`
(stability 5 samples ~100 s, 20:07:34Z). Verification completed inside the
cap. **Read-only on every artifact**: the gate, the repo, the theme tree and
the live session were only read; no repo file other than **this report** was
written by this lane. No socket opened; no compositor/session mutation; no
external site; secrets shape-only (none read). Marks: **[O]** measured,
**[I]** inference, **[U]** unknown. This file's path follows the VER-M8
convention (`reports/r8-ver-m8.md`); the dispatch text named no path.

## Artifact under verification

`tools/mado-verify.sh` (mado working tree, **uncommitted** at verification) —
sha256 `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`,
3,231 L (`wc -l`) / 150,103 B / mtime 2026-10-14 17:05:32.368 −03:00. HEAD
`12c8f08a…` (round-8 commit); `git status --porcelain` = the gate modified +
3 untracked (`corpus/knowledge/walker-deep-r9.md`,
`plans/round-9-record-draft.md`, `plans/round-10.plan.md`). The file **moved
six times** during this lane's window (`7da4ec50` → `d44a8933` → `cbc0f5f7` →
`31364115` → `d9ae12f9` → `93e43f8f` [O]); every number below binds to
`93e43f8f`, stable ≥100 s before my runs and sha-identical before and after
them.

## Landed theme-arm shape at `93e43f8f` [O]

- Plane id `theme`; 27 `row theme ` sites; scenarios **T1–T9** (gate
  `:777-912`) drive the real row code against `--root` fixture roots built by
  `build_fixture`.
- The plane comment (`:3001-3008`) states the landed scope: **FILE rows
  only** — "the note's live rows, swaybg argv and the theme-name display
  agreement, are not landed here". Grep confirms: no `theme.wallpaper.live`,
  no `theme.name.display_agree`; `theme.choice` unchanged as the
  `live.theme.current` NOTE.
- Walker live-surface rows (round-9 stage (b)): absent at this revision
  (`grep -c 'walker.sock'` → 0) [O]; the `walker-deep-r9.md` note landed as a
  file.

## Verdict

**VER-M9: PASS — the landed theme file-plane arm reproduces independently at
`93e43f8f…`**: selftest 268/268 green; three hand-re-run theme cases (clean /
one broken anchor / missing tree) each match their landed T-case claim; the
live arm is CLEAN with the theme rows reading the measured anchors. Two
caveats the record must carry: **(1)** the arm verified is the file-plane
form — the note's live rows are not in the gate at this revision (the plan's
own clause requires such an exemption named with its clause anchor);
**(2)** the gate was moving through the window — these numbers bind to
`93e43f8f` only, and any later revision re-opens the selftest count and the
re-cut receipt.

## Evidence

### 1. Selftest re-run (baseline → landed) [O]

- Baseline, committed round-8 gate (`7da4ec50…`, re-materialized from
  `git show HEAD:tools/mado-verify.sh`): `MADO_SELFTEST: 217/217 assertions
  passed`, rc 0 (`selftest-baseline.log`).
- Landed revision: `MADO_SELFTEST: 268/268 assertions passed`, rc 0, ~6.5 s
  (`selftest-final.log`). Delta **+51** assertions.
- In-flight datum (append-only): a run at 20:05Z on a mid-write revision
  failed `267 passed, 1 failed` — `R10: derived target equals the recorded
  gate revision (got 'dc7c4141…' want 'd2bcdb31…')`, the pin-re-cut alarm;
  at `93e43f8f` `PIN_MADO='dc7c4141…'` and R10 is green. Not a defect — the
  same pre-re-cut state SCR-M9 recorded at 20:02:35Z.

### 2. One arm's selftest case, re-run by hand (T1/T2/T9 stand-ins) [O]

Method (non-author, no repo edit): a byte-copy of the landed gate
(`gate-93e43f8f.sh`, sha verified equal) plus the gate's own `build_fixture`
extracted verbatim (`awk` from `^build_fixture() {` to `^selftest() {`;
`build_fixture.sh`, 142 lines) built a fresh clean fixture
(`/tmp/w9-ver-m9/clean`, 40 files). The three runs reproduce the T-case
claims against that fixture — not against the suite's internal one:

- **T1 stand-in** (`--root clean --no-live`): rc 0,
  `MADO_VERIFY: CLEAN (26 pass, 4 notes…)`, exactly **10 theme rows** — 9 PASS
  + `theme.parts.declared_only` NOTE; `theme.name.read` = 'matte-black';
  `theme.chain.hypr_include` holds "line 13". (`t1-clean.log`)
- **T2 stand-in** (copy of clean with `…/current/theme/hyprlock.conf`
  removed): rc 1, `MADO_VERIFY: DIVERGED (1 fail, 0 unknown, 25 pass) — first
  fail: theme.chain.hyprlock (import at line 1 but target missing:
  current/theme/hyprlock.conf)`; exactly **1 theme FAIL**, named; isolation
  holds (`theme.chain.hypr_include` PASS). (`t2-broken.log`)
- **T9 stand-in** (empty root): rc 1, `theme.name.read UNKNOWN` ("theme tree
  absent under this root"); the string `MADO_VERIFY: CLEAN` appears **0**
  times. (`t9-empty.log`)

### 3. Live arm (real HOME, read-only) [O]

`bash tools/mado-verify.sh` at `93e43f8f` (sha before = after): rc 0,
`counts: pass=52 fail=0 unknown=0 skip=0 note=8`,
`MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)`
(`live-final.log`). Baseline live at the committed round-8 gate was CLEAN
(43 pass, 7 notes, `baseline-live.log`) — the delta is exactly the theme plane
(+9 pass, +1 NOTE). Theme rows live: 9 PASS + 1 NOTE; `theme.name.read`
'matte-black'; `theme.wallpaper.link` resolves to
`…/backgrounds/0-ship-at-sea.jpg`; `theme.parts.declared_only` NOTE names 6
"(consumer absent)" parts (foot.ini(foot) kitty.conf(kitty)
ghostty.conf(ghostty) helix.toml(helix) vscode.json(code)
keyboard.rgb(asusctl)). The fixture form of that row reads "none" because
`build_fixture` does not materialize those six parts [I, from code + fixture
inspection]; T1 asserts only the NOTE status, so the list content is
exercised live only.

## Spot-checks (3, named)

1. T1 stand-in — clean fixture → 10 theme rows, zero theme FAIL/UNKNOWN, rc 0.
2. T2 stand-in — the broken row FAILs alone, target named; rc 1.
3. T9 stand-in — missing tree reads UNKNOWN, never CLEAN; rc 1.

(Plus the aggregate 268/268 selftest re-run and the live CLEAN 52 pass /
8 notes.)

## Unknowns

- [U] Whether the walker live-surface rows (stage (b)) land in this round —
  absent from the gate at `93e43f8f`; the round's record is the authority.
- [U] Whether the note's live theme rows are deferred or dropped — the landed
  comment says "not landed here"; the record should name the exemption.
- [U] The final committed revision: if the gate moves again (six shas in my
  window), all counts above are pinned to `93e43f8f`; the regression/re-cut
  receipt at the commit must be re-run and re-quoted.
- [U] Stage (c) receipts (`MADO_REGRESSION: PASS` at the landed revision,
  census before → after) were outside this lane's assignment — not verified
  here.
- [U] The mid-write R10 failure's resolution chain belongs to the SCR/AUD
  lanes; I record the in-flight datum only (append-only).

Boundary: repo read-only; no substrate write; no live-session disturbance;
no socket connect; no external site. Scratch `/tmp/w9-ver-m9/`: `poll.sh`,
`poll.log`, `watch.sh`, `watch.log`, `selftest-baseline.log`, `selftest.log`
(mid-write run), `selftest-final.log`, `gate-round8-committed.sh`,
`gate-93e43f8f.sh`, `build_fixture.sh`, `t1-clean.log`, `t2-broken.log`,
`t9-empty.log`, `baseline-live.log`, `live-final.log`; fixtures `clean/`,
`clean-t2/`, `empty/`.