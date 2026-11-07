author: hyaku closure (non-author integrator, @m_zfl)

# mado round 91 — verifier spot-check (non-author)

Lane-round: mado round 91 (hyaku run 15, attempt 1). Base `cc0381db585cc44c3dfc13ced807409c32c45bb0`, after
`847f589a1f2b772f5dac7e32a9cbb599a7aa09fc`. Report `.ufo/reports/round-91/mado.md` (fleet repo). This reviewer did not
author the round and changed none of its files; this file is the only lane path it writes.

Driver digest (copied from the mutable `.ufo/watchdog.log`):

    2026-11-06T20:53:12-03:00 launch mado round=91 pgid=2378783 driver=hyaku-inline attempt=1
    2026-11-06T22:21:12-03:00 complete mado round=91; hyaku-inline attempt=1

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-91/mado.md` (fleet) | `mado-shokunin <mado@shokunin.local> 1759fe46846410d63db927efd4f74ee15a32410f 2026-11-06 22:20:33 -0300` | pass |
| report filed after its last cited commit | records commit `847f589a` committed 22:19:28 -0300; report 22:20:33 | order holds | pass |
| `SHONEN` heading, one line per box | read of the report | `## SHONEN`, 4 lines, all `[~]` | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for cc0381db, fa71279f, 54a0683c, 0e09349e, cbbeb862, 847f589a | all `commit`, all `anc-ok` | pass |
| lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain` | `state branch=master local=847f589a… remote=847f589a… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `847f589a…` | pass |
| round commits by the lane identity | `git log --format='%h %an <%ae>' cc0381db..847f589a` | 5 commits, all `mado-shokunin <mado@shokunin.local>` | pass |
| prompt carries the template contract | `diff <(sed -n 1,140p kimi-shokunin/templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/mado-round-91.md)` | only placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §§1–5 headings identical; hyaku addendum §6 follows | pass |
| append-only lane records | `git diff --numstat cc0381db 847f589a \| awk '$2>0'` | only `SKILL.md 5/1` (mado-receipt-presence registry row updated for D1) and `corpus/SOURCES.md 5/1` (S502 used-by); PROVINCE/LOG/README/SCORECARD pure additions | pass |

Conformance notes (status-neutral): the dispatched prompt `.ufo/prompts/mado-round-91.md` was committed in the fleet repo
under the lane identity (`88c20a2e`, 20:53:10, two seconds before launch) — driver attribution, as in prior rounds. The
report's "4 reject" count includes the r1 NoDisplay erratum recorded under `## Residual r1` (lesson line 82), not in the
`## Gate` candidates table, which lists 1 admit + 3 rejects; the two places agree once both are read.

## Per-claim re-check

### C1 — coverage (capability): GLib 2.90.1 default-application resolution

Re-measured (plain measurements, mine):

- Tool absent at base, present after: `git cat-file -e cc0381db:tools/mado-mime.py` → `fatal: … not in 'cc0381db'`;
  present at `847f589a`. Before → after 0 → 1 tool. Matches the report.
- Landed bytes = frozen candidate: `git show 847f589a:tools/mado-mime.py | sha256sum` and
  `git show fa71279f:.ufo/waves/round-91/build/mado-mime.c1.py | sha256sum` both
  `2532ccb57cf9d67f6590e4aac2e8d0a9f9eb011b25eb42e45118a6ff51871a5e` = the declared pin.
- Frozen inputs unchanged after the freeze: `git diff --stat fa71279f 847f589a -- .ufo/waves/round-91/controls quality/counters`
  → only `controls/host-run-r91.py` added (new host-replay driver; no frozen file touched). sha256 prefixes at `847f589a`:
  cases `15e4b3fc0af091d4`, mutants `ed7716546bd7df57`, oracle `c3a13e26173a0eca`, fuzz-gen `0d147b83f85d0a0d` — all equal
  the declared `--expect-*` pins. Host oracle unchanged: `sha256sum /usr/bin/gio /usr/lib/libgio-2.0.so.0` →
  `d216426080f8…`, `b38001cca69b…` = pins; `gio --version` → `2.90.1`.
- Independent host probe (my run of `tools/mado-mime.py` bytes from `847f589a` against `gio mime TYPE` on this host):
  text/html, x-scheme-handler/https, image/png, application/pdf, inode/directory, text/plain, video/mp4,
  application/x-zerosize, application/x-pdf (alias), text/x-python3 (parent, no recommended), application/x-shellscript,
  image/jpg (alias) — **12/12 identical** default, registered and recommended lists (including order and "none").
- Independent fixture probe (my XDG roots under `/dev/shm`, `env -i`): (a) `hyprland-mimeapps.list` with only
  `[Added Associations] text/x-cl91=c.desktop` → gio warns "not permitted here", `No default applications`; tool
  `default=none registered=- recommended=-`. (b) the same group moved to `mimeapps.list` → gio `c.desktop` in all three
  lists; tool `default=c.desktop registered=c.desktop recommended=c.desktop`. 2/2 agree.

Evidence-verified (lane-owned counter, not executed — §Gate standard, Closure consequence):
`receipts/c1-measured-r91.txt` → `MADO_MIME_RESOLUTION: TARGET_MET … rev=54a0683c… cases=268 correct=268 … fresh=120/120
mutants=65 killed=65 crashed_not_killed=0 oracle_agree=268/268 do_nothing_correct=63 naive_mimeapps_correct=62
cache_only_correct=102 base_tool_correct=0 base_tool=absent tool_sha256=2532ccb5…`, `rc=0`; separability
`receipts/c1-at-c2-r91.txt` TARGET_MET at `0e09349e`, rc 0; host replay `receipts/host-run-r91.txt` →
`types=1211 agree=1211 semantic_diff=0`, rc 0. Revision measured is the cited C1 commit. Registry rows
`mado-r91-mime-resolution` (gate) and `mado-mime` (probe) present in `SKILL.md` at `847f589a` (lines 871–872).

Verdict: **verified** — coverage `improved`.

### C2 — operability: seat-report retention gate

Re-measured:

- Gate absent at base, present after: `git cat-file -e cc0381db:quality/check-seat-reports.py` → not in `cc0381db`;
  present at `847f589a`. Landed sha256 `13c4b0a7dc4bbc39c70731dd35ec1f312c09f1a48f3b620e02945184d9cce39a` = frozen
  candidate `build/check-seat-reports.c2.py` at `fa71279f` = declared pin. Set/mutants sha256 prefixes `9a05fa8ad4ef771e`,
  `7cf06df7dc0903e1` = pins.
- Premise (no base check reads a dispatch's seats for a report file): `quality/check-wave-done.py` at `cc0381db` reads
  dispatch/results and grades seat *status* (`results-missing`, `dispatch-mismatch`), not the `Report:` file; matches the
  M91-4 erratum wording ("lane checks that detect a missing seat report for a dispatched seat 0 → 1").
- My count over round 91: `Report:` trailers in `w1-dispatch.json` + `r1-dispatch.json` at `847f589a` → 16 seat paths
  (plus 3 template-text matches `<path>`/`write`, not paths); `git cat-file -e 847f589a:<path>` → **16 present, 0
  missing**, equal to the lane gate's `receipts/c2-gate-round91-r91.txt` (`seats=16 … present=16 missing=0 verdict=OK`).

Evidence-verified: `receipts/c2-measured-r91.txt` → `MADO_SEAT_REPORTS: TARGET_MET … rev=0e09349e… expectations=59 met=59
fresh=60/60 selftest=ok:SEAT_REPORTS_SELFTEST: checks=16 failed=0 mutants=55 killed=55 base_met=0 always_ok_met=5
always_missing_met=0 receipt_presence_met=11`, `rc=0`; separability `receipts/c2-at-c1-r91.txt` → `SETUP_ERROR … absent at
54a0683c`, `rc=2`. Self-test tally 16/16; registry rows `mado-r91-seat-reports`, `mado-seat-reports` present
(`SKILL.md` 873–874). Six residual defects F1–F6 (R91MResidC2 §5) lie outside the frozen predicate and are named in the
SCORECARD errata; F1 (symlinked dispatch under `--rev` can print OK) and F4 (FIFO blocks `--worktree`) are real gate gaps.

Verdict: **verified** — operability `improved`.

### Routed work (not claims)

- D1: `git diff --numstat 0e09349e cbbeb862` → `87 0 quality/check-receipt-presence.py`, `1 1 SKILL.md`, receipt
  `d1-selftest-r91.txt` (selftest rc 0, three mutant runs rc 1). Matches the report.
- D3: appended note in `corpus/lessons/round-91.md` `## Gate`; `corpus/lessons/round-90.md` not rewritten.

### Harm

- `git diff cc0381db 847f589a -- SCORECARD.md`: one appended `## Round 91` section, no removed line.
- `receipts/harm-final-r91.txt` (at `cbbeb862`): `MADO_SELFTEST: 460/460`, `MADO_VERIFY: CLEAN (29 pass …)`, `LEDGER …
  173/173 uncovered=0`, mako 62/0, portals 22/0, mime 17/0, seat-reports 16/0, receipt-presence 6/0, round-90 C2 `83/83`,
  round-90 C1 `229/229`. The only `rc=1` lines are `expect … ok rc=1` fixture expectations. The records commit
  `847f589a` changes no code (`git diff --name-only cbbeb862 847f589a` outside round-91 waves: LOG, SCORECARD,
  QUALITY, SOURCES, lesson only), so the harm watch revision covers the tip's code.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 re-measured (absent → tool; pins hold; 12/12 host + 2/2 fixture agree with gio) and evidence-verified (268/268, 65/65, 1211/1211) |
| operability | improved | C2 re-measured (absent → gate; pins hold; my 16/16 count = gate's) and evidence-verified (59/59, 60/60, 55/55, selftest 16/16) |

No owned axis harmed.

## Discernment spot-check (`corpus/lessons/round-91.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/mime-default-resolution-r91.md` | admit | `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c` (sha256 `8e9ce1a8…5b0d`, = S504) lines 1005–1042 and 978–984; host `gio mime`; my fixture roots | agree | the entry's file/group table (lines 59–62) cites :1011-1014, :1017-1019, :1032-1034, :1039-1041 — the source passes `FALSE` (defaults only) for `<desktop>-mimeapps.list` and `defaults.list`, `TRUE` for `mimeapps.list` and `mimeinfo.cache`; "Defaults have no blocklist (:982)" = `expand_strv (&tweaks->defaults, desktop_file_ids, NULL)`; my fixture shows gio ignoring desktop-specific `[Added Associations]` and the tool agreeing; host answers 12/12 |
| S507's "default … must be … associated with the type" as GLib's rule | reject | `https://specifications.freedesktop.org/mime-apps-spec/latest/default.html` (sha256 `00b5c8f3…7ec6`); gdesktopappinfo.c 4740–4775; gio on my fixture | agree | the spec sentence is present verbatim; the GLib loop takes the first collected id that loads (`goto out`) with no association test (line 4751 "(If any), see if one of those apps is installed..."); my fixture with `[Default Applications] text/x-cl91=c.desktop` and no `MimeType=` gives `Default application …: c.desktop`, `No registered applications` |

`corpus/SOURCES.md` rows re-opened:

- S507 (new): quote "Note as well that the default application for a given type must be an application that is
  associated with the type." — 20 words (≤ 25), found verbatim in `default.html`; index.html sha256 I fetched
  `12ddf2cc546992d5…` = the row's pin.
- S504/S505/S506 (new): my fetches of `gdesktopappinfo.c`, `xdgmime.c`, `gutils.c` hash `8e9ce1a8…5b0d`,
  `afb1c1c1…2410`, `65086c29…3771` = the rows; lesson quotes located at gdesktopappinfo.c 4751, xdgmime.c 739–740
  (`if (_caches) return _xdg_mime_cache_unalias_mime_type (mime_type);`), gutils.c 363–364
  (`if (g_path_is_absolute (original_program)) return NULL;`) — all present at the cited lines.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, rc 0; findings
`W04` 55, `W01` 1 (S277) — the report's "55 W04 as at start". Rows `grep -cE '^ {0,3}\| S[0-9]{3,} ' corpus/SOURCES.md`:
438 at `cc0381db` → 442 at `847f589a`.

## Trend verdicts

- **expansion — improved.** One admitted entry on ground the coverage map did not hold (`corpus/README.md` adds the
  `mime-default-resolution-r91.md` row and the round-91 frontier line; `ls corpus/knowledge` 111 → 112), each `source:`
  citing mined rows S502/S504–S507; four new tier-A rows; one capability row in SCORECARD. The admit survived my re-check.
- **quality — unprovable-but-better.** No admitted entry failed its re-check; QUALITY 152 is grounded in M91-1 with
  killed restoring mutants; prior capabilities re-run green at the tip (round-90 C1 229/229, C2 83/83). But no
  `knowledge/` entry was superseded or re-verified this round, and M91-1 found the round-90 GKeyFile model divergent:
  `corpus/knowledge/xdg-portal-routing-resolver-r90.md` §9 still says invalid UTF-8 makes a file unreadable "matching
  `g_key_file_load_from_file` failing", while GLib 2.90.1 `gkeyfile.c` (sha256 `e1d1270f…`, = S502) validates UTF-8 only
  in the value getters (lines 2310, 2427). The lane marked and routed it (lesson M91-1, report "Routed to round 92"),
  so it is not `harmed`, and the stronger model now held by the new entry is the better-but-unproven part.
- **discernment — improved.** The outside spot-check agrees with the gate on the sampled admit and the sampled reject;
  both rejects re-opened here were decided against an executed oracle, not by reading.

## Routed defects (lane fixes next round)

1. `corpus/knowledge/xdg-portal-routing-resolver-r90.md` §9 (and §4.4 where it models GKeyFile load) — append a named
   correction: GLib 2.90.1 loads invalid UTF-8 and fails only the value read (`gkeyfile.c:2310`, `:2427`); re-prove
   `tools/mado-portals.py` on the four M91-1 byte classes against the xdp oracle, as the report already routes.
2. `quality/check-seat-reports.py` F1 (symlinked dispatch skipped under `--rev`, can print `verdict=OK`) and F4 (FIFO at a
   dispatch path blocks `--worktree`) — fix with a failing fixture each; F2, F3, F5, F6 per R91MResidC2 §5.
3. Lesson `## Gate` candidates table omits the r1 NoDisplay reject that the report counts; list every gate decision of
   the round in the one table.

## For the operator (promotion is operator-owned)

SHONEN boxes 2 (end-to-end task) and 3 (instructions executable without oral context) now look checkable by a
non-author: this closure ran `tools/mado-mime.py` from its `SKILL.md` registry argv and `--help` alone and reproduced
gio's answers on 12 host types and 2 fixtures. Nothing was written to `SHONEN.md`.
