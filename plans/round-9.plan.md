# WWKD plan — mado round 9 (ufo-round-plan-v1)

Design lane: PREP-M9 (2026-10-14; round-8 32-lane wave, width 32; mado
round-8 work in flight). Everything below was read at design time by this
lane — freeze 2026-10-14T19:14Z — not taken from a record; every pin is
re-measured at dispatch. Round-8 clauses (a8) stub discipline / (b8) omarchy
plane / (c8) assertion floor are this plan's precondition set, checked at
dispatch from the round-8 record, never assumed.

Design-time state (measured, read-only; re-measure at dispatch):
- HEAD `0c20a76fa5ff985047c8ca2d455c75179c3dd0d1` ("probation round 7
  (training r6): see LOG", commit 19:06:31Z); `git status --porcelain`
  empty at freeze. Round-7 artifacts committed and read at their landed
  sizes: `corpus/knowledge/theme-wallpaper-plane.md` (394 L by `wc -l`,
  27,594 B, sha `8c578cc70e36506d…`), `corpus/knowledge/walker-live-surface.md`
  (300 L, 19,203 B, sha `2bbb9609283f2d81…`),
  `plans/round-7-record-draft.md` (569 L, sha `045d380ab52ce317…`),
  `reports/r7-aud-m7.md` (240 L by `wc -l`, sha `4011b2c44c9abb35…`),
  `SKILL.md` (905 L, sha `e0d516e84ed27834…`), `LOG.md` (298 L, sha
  `9843f0f3df38c7f9…`), `SCORECARD.md` (19 L, sha `40d87245af6c5a02…`),
  `corpus/README.md` (19 L, sha `2dd274f5e270e65b…`, 8 `knowledge/`
  coverage rows), `plans/round-8.plan.md` (206 L by `wc -l`, sha
  `ffcc058aa17755d9…`, frozen 18:25Z, committed).
- Gate `tools/mado-verify.sh` sha256
  `90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd`,
  1,755 L (`wc -l`), 75,771 B, mtime 15:31:57 −03:00. Executed at freeze:
  `--selftest` → `MADO_SELFTEST: 89/89 assertions passed` rc 0; `--no-live`
  → `MADO_VERIFY: CLEAN (17 pass, 2 notes)`, `counts: pass=17 fail=0
  unknown=0 skip=1 note=2`, boundary `bb2639d9a980…`; live → `MADO_VERIFY:
  CLEAN (35 pass, 4 notes)`, `counts: pass=35 fail=0 unknown=0 skip=0
  note=4`; `--regression` → `MADO_REGRESSION: PASS` rc 0 in 12.4 s
  (`match=10/10`, flips 0, inconclusive 0, control GREEN,
  `MUTATE_RESTORE: OK`, target `c4c1afb75dd1c8aa…a5171`; harness sha
  `cf41efaa8be5f52d…242c75` printed as provenance, not gated). A
  `--no-live --root <empty dir>` run at freeze read `DIVERGED` (8 fail, 6
  unknown, 1 pass) rc 1 — the file plane fails closed on a missing tree,
  never CLEAN; the `theme.*` file rows inherit that discipline.
- Gate census [OBS]: 106 `row` + 6 `row_from_rc` call sites (a 7th
  `row_from_rc` line is the helper definition), 40 distinct row ids; by
  plane field hypr-live 57 / hypr 23 / waybar 17 / terms 10 / gate 3 /
  walker 2 (112 sites = 106+6). Six plane ids; the helper regexes
  `:352`, `:356`, `:371-375` hard-code them. The selftest asserts ≈11 of
  40 distinct row ids (token count over the selftest region; re-counted at
  dispatch). `theme.*` = 0 row sites — the theme appears only as the NOTE
  row `live.theme.current` (`:1673`, `:1677`, under the `hypr-live`
  plane). Walker live = `live.walker.version` + `live.walker.services`
  (`:1659-1667`).
- The two measured-but-unlanded surfaces this move consumes (round-7
  stages (b)/(c) as gate rows; audit `r7-aud-m7.md` C3/C4 verdicts
  NOT-LANDED, notes verified): (i) `theme-wallpaper-plane.md` §6 is a
  paste-ready 12-row spec for plane id `theme` — `theme.name.read`,
  `theme.chain.{hypr_include,hyprlock,waybar_css,alacritty,mako_link}`
  plus installed-consumer-gated `theme.chain.walker_css`/`.swayosd_css`,
  `theme.wallpaper.link`, live `theme.wallpaper.live` and
  `theme.name.display_agree`, NOTE-only `theme.choice` and
  `theme.parts.declared_only`; (ii) `walker-live-surface.md` §4/§5 is the
  measured surface for socket rows, the D-Bus owner row and the
  layer-invariant row, plus the §5 ledger owed to `walker-deep.md`
  §10/§11. Landing conditions, stated in SKILL's round-7 "Open items":
  widen the selftest plane-prefix regexes to any new plane id; a covering
  mutant per new clause (round-6 reading rule 2, `SKILL.md:596-599`); then
  `MADO_REGRESSION: PASS` under reading rule 1 (`SKILL.md:783-788`) — the
  rows land outside the marked blocks, so the case needs a re-cut (sweep,
  then update `PIN_MADO`/`TABLE_MADO`).
- Design-time anchors for the two surfaces (read verbs only; re-measure
  at dispatch): `theme.name` = `matte-black` (12 B); `omarchy theme
  current` → `Matte Black`; `current/background` →
  `~/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`;
  `~/.config/mako/config` → `~/.config/omarchy/current/theme/mako.ini`;
  swaybg pid 1203358 `/usr/bin/swaybg -i …/current/background -m fill`;
  `hyprctl -j layers` DP-1 level 0 `wallpaper` / level 2 `waybar`
  (levels 1/3 empty); walker 2.17.0 pid 1203471
  `/usr/bin/walker --gapplication-service`; elephant 1203474; `busctl
  --user list` → `dev.benz.walker` owner 1203471 `:1.23`; sockets
  `/run/user/1000/walker/walker.sock` and `…/elephant/elephant.sock` both
  `srwxr-xr-x`, 0 B.
- Round-8 work in flight [OBS point sample; content NOT consumed]:
  scratch `/tmp/w8-mado-m8-1` (mtime 16:12:41 −03:00) and
  `/tmp/w8-mado-m8-4` (16:10:32 −03:00); no round-8 artifact committed at
  freeze. Everything round 8 lands (gate revision, plane id, stub verbs,
  record) is resolved at dispatch from the round-8 record.
- Sibling harness (read-only): `tameshi-shokunin/tools/mutate-and-run.sh`
  61,632 B, sha `cf41efaa8be5f52d…242c75` at freeze — the revision the
  freeze-time regression run printed as provenance.
- Debt carried: `corpus/lessons/` still 0 entries at freeze (the round-8
  plan charters `round-8.md`; resolved at dispatch);
  `corpus/README.md` 8 coverage rows (missing the two round-7 notes and
  round-8's); SCORECARD round-7 row landed.

Candidate decision: the post-round-8 candidates — (1) the two measured
surfaces still not gate rows (theme plane; walker live rows), (2)
`walker-deep.md` §10/§11 errata append, (3) receipt durability (the
round-7 receipts live only in `/tmp`), (4) record debt — are one move
here, not four. (1) is the claim: it completes the round-7 plan's stages
(b)/(c) *as gate rows* (the notes are the measured input, unedited), and
it closes the declared-coverage invariant the gate has carried since
round 5 (every declared plane either has rows or a named exemption). (2)
is the same revision's record-family append (the note's §5 ledger is the
substance). (3) is the measure's receipt clause (receipt lines quoted in
the record, not left only in scratch). (4) rides the record, not the move.
(1) is the largest named remainder from the round-7 audit's open set and
the round-8 plan does not claim it.

Axis move: coverage + operability — ONE move, three ordered stages: the
`theme` plane lands as gate rows from the note's §6 spec (a); the walker
live-surface rows land from the note's §4/§5 surface (b); the census
closes over the landed set, every widening carries its mutant and its
re-cut regression receipt, and the errata/receipts land in the record (c).
Every widening is covered by a mutant before it ships.

Claim:
(a) `theme` plane (plane id `theme`; rides round-8's stub discipline) —
    rows from `theme-wallpaper-plane.md` §6, re-anchored at dispatch (the
    note's table is the input, never edited; a re-anchoring is an
    appended erratum — the note's §10 where write scope allows, else the
    record). File rows: `theme.name.read`; the include/import chain rows
    for `hyprland.conf:13`, `hyprlock.conf:1`, waybar `style.css:1`,
    `alacritty.toml:1`, the mako symlink; `theme.chain.walker_css` /
    `.swayosd_css` (installed-consumer-gated — NOTE when the consumer is
    not installed, never a silent skip); `theme.wallpaper.link`; NOTE-only
    `theme.parts.declared_only`. Live rows: `theme.wallpaper.live` —
    swaybg argv names the background **symlink** with `-m fill`, level-0
    `wallpaper` layer pid == swaybg pid; NOTE if no swaybg (mirroring
    `live.consumer.hypridle`), UNKNOWN if hyprctl unavailable.
    `theme.name.display_agree` — `omarchy theme current` equals
    reader-rule(`theme.name`); a pair the rule does not join is recorded,
    never forced; UNKNOWN if `omarchy` absent. `theme.choice` stays NOTE
    always (operator-owned — today's `live.theme.current`, unchanged).
    Exercise: file rows under the existing `--root` fixture discipline
    (missing tree → FAIL/UNKNOWN, never CLEAN — measured at freeze on the
    empty root); live rows under round-8's stub discipline (stubs for
    `hyprctl -j layers`, `pgrep -ax swaybg`, `omarchy theme current`,
    fixture shapes derived from the gate's own readers, not invented).
    Scenarios, round-8 idiom: stubbed-clean → the covered rows PASS; one
    stubbed pin MOVED → the named row FAILs; stub absent with live
    requested → UNKNOWN, never CLEAN. Any read whose fixture shape cannot
    be faithfully reproduced is exempted **by name** with its clause
    anchor, never silently skipped; the exemption is counted.
(b) Walker live-surface rows — from `walker-live-surface.md` §4/§5:
    socket rows (path, type `s`, mode, size for
    `$XDG_RUNTIME_DIR/walker/walker.sock` and `…/elephant/elephant.sock`;
    stat'd, **never connected**); the D-Bus owner row (`busctl --user
    list` parse — `dev.benz.walker` owner pid == the walker pid; a
    mismatch FAILs); the layer-invariant row (`hyprctl -j layers` — a
    walker namespace must carry the walker pid; absence is a NOTE, never
    a pass/fail signal — the gate never opens the launcher). The socket
    rows read `$XDG_RUNTIME_DIR`; hermetic exercise needs either a
    fixture runtime dir carrying a real bound socket or an accepted
    override seam in the row's read shape — if the landed shape accepts
    neither, the socket rows are exempted by name and the exemption is
    counted. The `walker-deep.md` §10/§11 errata append (substance = the
    note's §5 ledger, append-only) is this claim's record-family clause.
(c) Census closure + receipts — the helper regexes (`:352`, `:356`,
    `:371-375`) widen to the landed plane set (the six + round-8's
    landed ids + `theme` + the walker-live id — the exact set is counted
    at dispatch, never assumed); the per-plane census is re-reported
    before → after by the counting command. The defect spec extends per
    newly covered clause and the sweep is re-cut at the landed revision
    (the printed `REGRESSION_RECUT` command, then `PIN_MADO`/`TABLE_MADO`);
    `MADO_REGRESSION: PASS` with `MUTATE_RESTORE: OK` and target sha
    before = after is the receipt — and the receipt lines (tool sha,
    target sha, table, sweep) are quoted in the record (LOG + SKILL), not
    left only in `/tmp`. A surviving mutant is a FINDING (append-only
    errata, not smoothed); widening without a covering kill vehicle does
    not ship, and the round says why.

Ordering: (a) and (b) are gated on the round-8 precondition set, resolved
at dispatch from the round-8 record: (a8) the stub discipline and its
token contract landed, or the round records its absence; (b8) the omarchy
plane landed and its plane id/namespace is known (the regex widening
consumes it); (c8) the assertion floor landed. If (a8) did not land, the
live rows of (a)/(b) are exempted by name and only the file-plane halves
ship — the round says why; no deprecation of round-8 values. (c) rides
(a) and (b); every widening carries a regression pass at the widened
revision, run by the round-7 `--regression` idiom with the re-cut.

Anti-claim: a stubbed scenario proves row logic, never live values — the
gate's verdicts stay `bash tools/mado-verify.sh`; an unfaithful stub
shape is exempted by name, never faked; any unverifiable check reads
UNKNOWN, never CLEAN; the theme choice stays NOTE (operator-owned) and
chain integrity is the verdict input; a MOVED anchor is reported first,
never smoothed into the baseline; no compositor/session mutation (no
launcher open, no socket connect, no `omarchy theme set`, no restart);
the theme tree, the omarchy checkout, the tameshi harness and sibling
repos are read-only — a needed change is a recommendation to that lane,
never a patch; no `git status`/`git fetch` on the checkout; secrets
shape-only.

Measure: regression verdict per landed revision (`MADO_REGRESSION: PASS`
at the widened revision; receipt lines quoted in the record); selftest
count before → after (89 → 89+M, scenario ids listed) and distinct
asserted row ids before → after (≈11 of 40 at freeze, re-counted — every
landed row covered by a scenario or exempted by name); plane census
before → after (6 ids / 106 `row` + 6 `row_from_rc` call sites / 40
distinct ids / per-plane hypr-live 57 · hypr 23 · waybar 17 · terms 10 ·
gate 3 · walker 2 → the landed set, per the counting command);
helper-regex id count before → after; the two verdicts at the landed
revision (`--no-live` and live, counts quoted); `walker-deep.md` sha
before → after (errata append); SKILL gate section gains the two planes
and the landing receipts; SCORECARD move row + LOG entry carrying the
commands; README coverage rows for the two round-7 notes plus round-8's;
`corpus/lessons/round-9.md` chartered with its `## Gate` section and a
non-author spot-check (at least one admit and one reject) — or the round
records why no independent seat exists (a lane's own subagent does not
count; `LEARNING.md:38-43`).

Open unknowns at draft: whether round 8 lands (a8)/(b8)/(c8) and under
which gate sha, and which plane id/row namespace the omarchy plane takes
(the regex widening consumes the counted answer); whether the round-8
stub discipline extends to the reads this move needs (`stat` of sockets,
`busctl --user list`, `pgrep -ax swaybg`) or stops at its six named
verbs — the exemptions follow; whether the walker socket rows can be
hermetically exercised (fixture socket vs override seam vs exemption by
name); whether the theme note §6's `walker_css`/`swayosd_css` split lands
as one row or two; whether the mako symlink row can be fixture-rooted
under `--root` (a fixture home carries its own mako path) — counted at
dispatch; whether round-8's (c) resolved the rc-6 arm and by which
vector (white-box pin or removal) — if removal, the round-9 sweep's
defect spec loses that class, recorded; whether the round-8 record's
numbers match its plan (the record is authority); whether
`corpus/lessons/round-8.md` charters — if not, the lessons debt runs an
eighth round; whether the live anchors (pids, sockets, layer pids)
survive to dispatch — point-sampled, re-measured, MOVED reported;
whether tameshi's harness ever gains a stdout-reading criterion (the
exit-flatten family — that lane's call, recommendation only); whether
the `walker-deep.md` §10/§11 errata owner materializes (the round-7
record assigns it to the lane owning the note).

Write scope (execution): one output file per lane as assigned; the gate
is single-writer; scratch `/tmp/w9-<lane>-*`; substrates (`~/.config`,
`~/.local`, the omarchy checkout, the tameshi harness) read-only; secrets
shape-only. This design lane wrote only this file.