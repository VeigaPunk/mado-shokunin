# WWKD plan — mado round 8 (ufo-round-plan-v1)

Design lane: PREP-M8 (2026-10-14; round-7 32-lane wave, width 32; mado
round-7 work in flight). Everything below was read at design time by this
lane — freeze 2026-10-14T18:25Z — not taken from a record; every pin is
re-measured at dispatch. Round-7 clauses (a) gate regression mode / (b)
theme-wallpaper plane / (c) walker live surface are this plan's precondition
set, checked at dispatch, never assumed.

Design-time state (measured, read-only; re-measure at dispatch):
- HEAD `c8f6667` (round-6 landing, commit 18:17:26Z); `git status
  --porcelain` empty at freeze. Round-6 artifacts committed and read at
  their landed sizes: `corpus/knowledge/gate-mutation-proof.md` (167 L by
  `wc -l`, 10,693 B), `corpus/knowledge/omarchy-drift-watch.md` (287 L,
  18,714 B, sha `49f5a9a1…`), `corpus/knowledge/remaining-planes-census.md`
  (333 L by `wc -l`, 20,512 B, sha `710e3e28…`), `plans/round-7.plan.md`
  (135 L by `wc -l`, sha `d4e23e81…`).
- Gate `tools/mado-verify.sh` sha256
  `c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171`,
  1,186 L (`wc -l`), 50,126 B, mtime 14:55:16 −03:00. Executed at freeze:
  `--selftest` → `MADO_SELFTEST: 53/53 assertions passed` rc 0; `--no-live`
  → `MADO_VERIFY: CLEAN (17 pass, 2 notes)`,
  `counts: pass=17 fail=0 unknown=0 skip=1 note=2`, `boundary.readonly` PASS
  combined sha `bb2639d9a980…`; live → `MADO_VERIFY: CLEAN (35 pass, 4
  notes)`, `counts: pass=35 fail=0 unknown=0 skip=0 note=4`.
- Gate census [OBS]: 106 `row` + 6 `row_from_rc` call sites, 40 distinct row
  ids, six plane ids — hypr 23 / hypr-live 51 / waybar 17 / terms 10 / gate 3
  / walker 2 (counted by plane prefix). The selftest exercises 11 distinct row
  ids of 40; of the 51 `hypr-live` sites only the guard row `live.plane` is
  reached (2 row sites `:676`/`:851`, 2 assertions `:397`/`:432`). The
  selftest's awk helpers hard-code the six ids at
  `:352`, `:356`, `:371-375`. No `--regression` token exists yet
  (`grep -c regression` → 0). Modes verify / `--no-live` / `--live` /
  `--root` / `--selftest` / `--help`; verdicts `MADO_VERIFY: CLEAN|DIVERGED`;
  exit map 0/1/2.
- Round-6 record's open set (this move's input; [OBS] from the landed notes):
  (i) live-plane body unexercised — tameshi's spec §8 rec #1 (a PATH-stub
  `hyprctl` scenario) is the named highest-yield remainder; the v2 probe grid
  stayed at 33% for exactly this reason (SKILL round-6 append);
  (ii) `row_from_rc` rc-6 arm is dead code — an equivalent edit under any
  black-box suite; "kill requires a white-box pin or removing the branch —
  owner decision, recorded unabsorbed" (`gate-mutation-proof.md` §3);
  (iii) usage paths unasserted: `--root` with no value and a bad
  `MADO_VERIFY_LIVE` (exit 2 arms) — recorded survivors (§3 minor residuals);
  (iv) exit-flatten family — harness boundary; the harness judges by exit
  only, so a mutant whose suite run is red but whose own exit is 0 reads
  SURVIVED; "a future harness that also reads suite stdout would close this
  class" (§3);
  (v) version string / boundary cosmetics unpinned (§3);
  (vi) the `omarchy` freshness plane is spec-only — paste-ready rows,
  constants and four scenarios in `omarchy-drift-watch.md` §6; census 6 → 7
  plane ids; open decision D-1 (theme row NOTE vs FAIL).
- Round-7 work in flight [OBS point sample; content NOT consumed]: scratch
  `/tmp/w7-mado-m7-2` (theme/wallpaper probes), `/tmp/w7-m7-3` (walker live
  probes), `/tmp/w7-scr-m7` (scribe preflight logs); two round-7 artifacts
  landed during the freeze minute, untracked —
  `corpus/knowledge/walker-live-surface.md` (300 L by `wc -l`, 19,111 B,
  15:24:42 −03:00) and `plans/round-7-record-draft.md` (499 L, 32,443 B,
  15:24:48). Gate mtime/sha unchanged by the landing at freeze. Round-7
  artifact shas and the round-7 record are resolved at dispatch.
- Design-time anchors for stage (b) (read verbs only; re-measure at
  dispatch): `omarchy version` → `3.8.3`; `git -C ~/.local/share/omarchy
  describe --tags --exact-match` → `v3.8.4`; `rev-parse HEAD` →
  `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; skill leaf via
  `~/.agents/skills/omarchy` → `…/default/omarchy-skill`, 392 L / 14,908 B,
  sha256 `becd149e4d1c0767…`; `omarchy theme current` → `Matte Black`;
  `current/theme.name` → `matte-black` (12 B).
- Design-time anchors for the stage (a)/(c) surfaces [OBS]: walker PID
  1203471 `--gapplication-service`, elephant 1203474, units
  `app-walker@autostart.service` + `elephant.service` both `active`; D-Bus
  names `dev.benz.walker` and `:1.23` owned by 1203471; sockets
  `$XDG_RUNTIME_DIR/walker/walker.sock` and `…/elephant/elephant.sock`, mode
  `srwxr-xr-x`, 0 B; `hyprctl -j layers` DP-1 level 0 `wallpaper` 1203358,
  level 2 `waybar` 1203352, no walker surface (closed); `instances`
  `wl_socket` `wayland-1`.
- Sibling harness (read-only): `tameshi-shokunin/tools/mutate-and-run.sh`
  1,080 L, sha256 `b56c6e57f1b7ae91…` — moved from the round-6 sweep pin
  `597e1419…`; its own `--regression` (r4-2) re-runs its two embedded cases
  with `REGRESSION: PASS|FAIL|SETUP`, band |killed − recorded| ≤ 1, flips ≤ 1,
  inconclusive 0, exit 0/1/2. Its kill criterion is still exit-code judged —
  the exit-flatten boundary stands unless the tool grows a stdout criterion.
- Debt carried: `corpus/lessons/` still 0 entries (seventh round);
  `corpus/README.md` 8 coverage rows (missing the r4/r5 notes and the three
  round-6 notes); SCORECARD round-6 row landed.

Candidate decision: the four post-round-6 candidates — (1) live-body
exercise, (2) the `omarchy` plane landing, (3) the recorded hygiene
residuals, (4) record debt (README/lessons) — are one move here, not four.
(1) and (2) are the two halves of one artifact, the gate, closing the two
"open items" the round-6 append itself names (unexercised proof body;
declared census without the seventh plane); (3) is the same revision's
assertion floor (cheap, same file); (4) rides the record, not the move. The
round-7 regression mode is the vehicle the round-6 plan promised for "the
next hardening pass" — this move is the first that consumes it.

Axis move: operability + freshness — ONE move, three ordered stages: the
suite's proof body closes over the live plane (a); the declared census closes
over the freshness plane, shipping only under (a)'s stub discipline and a
regression pass (b); the assertion floor rises over the recorded residuals
(c). Every widening is covered by a mutant before it ships.

Claim:
(a) Live-body exercise — hermetic selftest scenarios reach the live rows
    through PATH stubs, never the substrate: a stub `hyprctl` answering the
    declared read verbs with fixture JSON (version, instances, configerrors,
    getoption, binds, monitors, layers, clients — shapes derived from the
    gate's own readers `:676-1108`, not invented), plus stubs for
    `systemctl --user is-active`, `busctl --user get-property`, `pgrep`,
    `walker --version`, `omarchy theme current`, first on PATH. Scenarios:
    J — stubbed-clean live run → the covered live rows PASS, verdict CLEAN,
    counts agree; K — one stubbed pin MOVED → the named live row FAILs,
    DIVERGED, exit 1; L — stub absent with live requested → the affected rows
    read UNKNOWN, never CLEAN. Contract: the suite reads no substrate ($HOME
    is never the root; scenario A's boundary discipline holds); assertion
    count 53 → 53+M and distinct asserted row ids (11 of 40 today) counted
    before → after; any reader whose fixture shape cannot be faithfully
    reproduced is exempted **by name** with its clause anchor, never silently
    skipped. The defect spec extends per newly covered clause (the
    live-branch verdict token / the M16 class; skip-reason strings; the
    `--root=DIR` form; env-var renames; the version string) and the sweep is
    re-cut at the landed revision; survivors are findings.
(b) `omarchy` freshness plane (rides (a)) — plane id 7; rows and constants
    from `omarchy-drift-watch.md` §6, re-anchored at dispatch (the note's
    table is the input, never edited; re-anchoring is an appended erratum).
    Verdict-bearing: `omarchy.version.cmd`, `.version.file`, `.git.tag`,
    `.git.head`, `.skill.link`, `.skill.sha`, `.skill.vs_head`,
    `.cmd.groups`; NOTE-level: `.cmd.surface`, `.theme`, `.doc.drifts`. D-1
    resolves as NOTE for the theme row (HELD|MOVED printed in the detail) —
    consistent with the gate's existing NOTE treatment (`:1104`, `:1108`)
    and with round-7 (b)'s "the theme choice stays NOTE; chain integrity is
    verdict input": a routine theme change must not turn the freshness gate
    permanently red. The four §6 scenarios land as selftest cases: clean;
    version file MOVED → FAIL naming the pin + DIVERGED; live verb
    unavailable → UNKNOWN, never CLEAN; link replaced by a real dir with
    equal sha → `.skill.link` FAIL while `.skill.sha` PASS (a copy may not
    masquerade as the live skill). Reads only the §6 guard list; never
    `git status`/`git fetch`; no mutating omarchy verb. The selftest helper
    plane regexes (`:352`, `:356`, `:371-375`) widen from six ids to the
    landed set — counted before → after; the per-plane census is re-reported.
(c) Assertion floor (rides (a)) — the recorded residuals get assertions, not
    excuses: `--root` with no value → exit 2 + usage text; a bad
    `MADO_VERIFY_LIVE` → exit 2; the version string becomes a checked claim
    (the self-label names the landed revision, asserted); the boundary
    combined-hash prefix is asserted in the `sha_pin` detail pattern. The
    rc-6 dead-code arm is resolved by its named decision — a white-box pin in
    the suite (the arm maps 6 → UNKNOWN) or branch removal — choice and
    consequence recorded. The exit-flatten family stays a harness boundary:
    recorded as a recommendation to tameshi (a kill criterion that also reads
    suite stdout), never a patch.

Ordering: (a) is gated on the round-7 precondition set, checked at dispatch:
(a7) the regression mode exists with its token and exit map; (b7) the
theme/wallpaper rows landed; (c7) the walker live rows landed — each resolved
from the round-7 record, never assumed. (b) and (c) are gated on (a) green.
Every widening carries a regression pass at the widened revision: round-7
`MADO_REGRESSION: PASS` when landed; if it is not landed, the round runs the
round-6 sweep idiom itself (tameshi harness, same spec contract, restore
proof) and records the substitution. Widening without a covering kill
vehicle does not ship, and the round says why.

Anti-claim: a surviving mutant is a FINDING (append-only errata, not
smoothed); a stubbed scenario proves row logic, never live values — the
gate's verdicts stay `bash tools/mado-verify.sh`; an unfaithful stub shape is
exempted by name, never faked; any unverifiable check reads UNKNOWN, never
CLEAN; the `omarchy` baseline is never edited to match reality (a MOVED pin
is reported first); the theme row stays NOTE (operator-owned); no
compositor/session mutation (no launcher open, no socket connect, no
`omarchy theme set`); the tameshi harness and the omarchy checkout are
read-only — a needed change is a recommendation to that lane, never a patch;
no `git status`/`fetch` on the checkout; the gate's revision sha is measured
before and after every sweep.

Measure: regression verdict per landed revision (`MADO_REGRESSION: PASS`, or
the fallback sweep's `MUTATE: DONE … kill-rate` + `MUTATE_RESTORE: OK`,
target sha before = after); selftest count before → after (53 → 53+M, scenario
ids listed) and distinct asserted row ids before → after (11 of 40 →
measured); plane census before → after (6 ids / 106 row sites / 40 row ids →
7+ / 106+N / …, per-plane counts by the counting command; helper regex
id-count 6 → 7+); omarchy per-pin verdicts vs the design-time anchors above
(HELD|MOVED|UNKNOWN each named); the extended kill grid at the widened
revision (control GREEN, per-defect verdicts, restore proof); the two
verdicts at the landed revision (`--no-live` and live, counts quoted); SKILL
gate section gains the plane + the regression usage; SCORECARD move row +
LOG entry carrying the commands; README coverage rows for the three round-6
notes plus the round-7/8 rows; `corpus/lessons/round-8.md` chartered with its
`## Gate` section and a non-author spot-check (at least one admit and one
reject) — or the round records why no independent seat exists (a lane's own
subagent does not count; LEARNING.md:38-43).

Open unknowns at draft: whether round 7 lands (a)/(b)/(c), and under which
gate sha; whether the landed theme plane adds a plane id the helper regex
must match (counted at dispatch); the round-7 regression band/table (the
recorded band is authority, not this plan's shape); whether every live row's
input is hermetically fakeable (the readers' expectations vs stub shapes —
unfaithful ones are exempted by name); whether `omarchy.git.*` stays safe
without `git status` (round 6 sampled 3 files; tree-wide cleanliness is
unmeasured by constraint); whether the rc-6 white-box pin is accepted over
removal (owner decision); whether tameshi's harness ever gains a stdout
reading criterion (the exit-flatten family — that lane's call); whether a
non-author spot-check seat materializes for `corpus/lessons/round-8.md`;
`corpus/lessons/` debt (seventh round at draft — this plan's record clause
charters the file at last).

Write scope (execution): one output file per lane as assigned; the gate is
single-writer; scratch `/tmp/w8-<lane>-*`; substrates (`~/.config`,
`~/.local`, the omarchy checkout, the tameshi harness) read-only; secrets
shape-only. This design lane wrote only this file.