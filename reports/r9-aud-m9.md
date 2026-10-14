# AUD-M9 — round-9 audit: the theme-plane arms, the snapshot-diff receipt, zero config mutation

Lane AUD-M9, 2026-10-14. Write scope: **this file only** — no other repo file
was written by this lane; the gate, the notes, the record draft and the
sibling reports were read or executed from frozen copies under my scratch.
Scratch `/tmp/w9-aud-m9-gate/` (frozen copies + logs) and `/tmp/w9-aud-m9-snap/`
(receipts, empty root). **Zero config mutation**: the gate's own `boundary_hash`
rule (`LC_ALL=C`) reads `bb2639d9a98045d4…9862` at 19:59:48Z (before my first
run) and at 20:16:32Z (my close), identical to the value every gate run's own
`boundary.readonly` row prints; `~/.config/hypr/hyprland.conf` sha256
`4f52854a3c143dcf…` unchanged across my window. Session reads only: `hyprctl`
read verbs through the gate's live mode, `pgrep -ax swaybg`,
`omarchy theme current` (inside the gate), `readlink`/`ls`/`sed -n` on the
theme tree; no launch, no socket, no `omarchy theme set`, no restart, no `git`
on the omarchy checkout, no network. One fixture dir my mid-flight failing
selftest kept (`/tmp/w5-mado-m52-selftest.UWQIBO`, named in my own run's
output) was removed by exact path; foreign fixture dirs were left alone.

**In-flight window.** The gate was uncommitted worktree work throughout, so
every number below is tied to a measured sha; the gate was byte-stable at
`93e43f8f…` for the last ~12 min of my window (mtime 17:05:32 −03:00), and the
round-9 record draft / verifier report were still appearing at my close.
Anything after my close is uncovered (U1). Tags: **[O]** measured by this lane,
**[I]** inference, **[U]** unknown.

| artifact (read-only to me) | sha256 prefix · size | measured at |
|---|---|---|
| gate, round-8 landed revision (HEAD `12c8f08` blob) | `7da4ec50…` · 2,887 L / 131,612 B · mtime 16:29:03 −03:00 | frozen copy `gate-7da4ec50.sh`; baseline runs 19:59–20:00Z + 20:22Z |
| gate, mid-edit revision | `31364115…` · 3,215 L / 148,946 B | 20:04:48Z — selftest RED (R10 derived target `dc7c4141…` ≠ then-pin `d2bcdb31…`); superseded, kept as the re-cut alarm receipt |
| gate, round-9 revision — all round-9 numbers below | `93e43f8f…` · 3,231 L / 150,103 B · mtime 17:05:32 −03:00 | frozen copy `gate-93e43f8f.sh`; runs 20:06–20:16Z |
| derived target (my own 3-family excision of `93e43f8f…`) | `dc7c4141…` · 1,945 L = the gate's `PIN_MADO` (`:1290`) | 20:12Z |
| recorded defect spec (replayed unmodified) | `c7ee75b9…` · 10 `@defect` entries (D1–D9, R1) at **both** revisions | 20:08Z, my `--regression` |
| sibling artifacts encountered (read-only) | `plans/round-9-record-draft.md` 729 L · `corpus/knowledge/walker-deep-r9.md` 398 L · `reports/r9-ver-m9.md` | 20:06–20:19Z |

## 1. Verdict table

| # | claim | my own runs (method) | result | verdict |
|---|---|---|---|---|
| C1 | **The theme arms landed as gate rows** — plane id `theme`, file rows from `theme-wallpaper-plane.md` §6 | census on `93e43f8f…` + a `--no-live` run of my frozen copy; every anchor value re-read directly | 27 `row theme` sites; a file-plane run emits **10 theme rows** — `theme.name.read`, `chain.hypr_include`, `chain.hyprlock`, `chain.waybar_css`, `chain.alacritty`, `chain.mako_link`, `chain.walker_css`, `chain.swayosd_css`, `wallpaper.link` (all PASS), `parts.declared_only` (NOTE, lists foot/kitty/ghostty/helix/code/asusctl). Independent anchor re-reads: `hyprland.conf:13` = `source = ~/.config/omarchy/current/theme/hyprland.conf`; `theme.name` = `matte-black`; `mako/config` → `…/current/theme/mako.ini`; `current/background` → `…/theme/backgrounds/0-ship-at-sea.jpg`; swaybg pid 1203358 `-i …/current/background -m fill`; theme files hyprlock.conf 176 B / waybar.css 68 B / alacritty.toml 772 B | **PASS (file half)** |
| C1b | the **live** half of claim (a) — `theme.wallpaper.live`, `theme.name.display_agree` | `grep -c 'wallpaper.live\|display_agree'` → 0; a live run at `93e43f8f…` | absent; the `live.theme.current` NOTE the plan maps `theme.choice` onto is still emitted | **NOT LANDED at the measured revision** (in-flight, owed) |
| C2 | **Selftest + assertion floor at the landed revision** | `--selftest` on my frozen copy, run twice | `MADO_SELFTEST: 268/268 assertions passed` rc 0 both runs; 217 → 268 (+51); theme scenarios T1–T9 (35 labelled assertions; 25 `st_row_has`/`st_row_detail` calls over the 10 theme ids); distinct asserted row ids 22 → 32 — the +10 are exactly the theme ids | **PASS** |
| C3 | **Census closure / regex widening** | my counting commands on both revisions | `row` sites 162 → 189 (`row_from_rc` 6 → 6; total 168 → 195); distinct ids 51 → 55; per-plane hypr-live 57 · omarchy 56 · hypr 23 · waybar 17 · terms 10 · gate 3 · walker 2 → same + **theme 27**; the three helper-regex sites I checked (`:387`, `:391`, `:406`) carry `hypr\|hypr-live\|waybar\|walker\|terms\|omarchy\|theme\|gate` (7 → 8 ids) | **PASS** |
| C4 | **Regression receipt at the landed revision** — recorded case replays, target sha before = after, pin internally consistent | my own `--regression` on the frozen copy (harness pinned to tameshi `cf41efaa…`) + my own 3-family excision | `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=dc7c4141…)` rc 0 (53.9 s); `REGRESSION_TABLE … match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`; `REGRESSION_CASE … PASS (… control=green restore=ok)`; my independent excision gives `dc7c4141…` byte-exact = `PIN_MADO`. **But the received defect spec is byte-identical to round 8** (`c7ee75b9…`, 10 defects, `@defect` count 10 at both revisions) — no new recorded mutant covers the theme clauses at this revision | **PASS for the recorded case; the plan's "every widening carries its mutant" is NOT met at this revision — finding, recorded not smoothed** |
| C5 | **Snapshot-diff receipt at the landed revision** (M8-3 re-measured) | `--snapshot` runs + `--snapshot-diff` on my frozen copy | `WRITTEN … (rows=41 pass=29 fail=0 unknown=0 skip=8 note=4; scope=file-plane)` rc 0; same-root pair → `MADO_DIFF: SAME (rows 41→41; every class 0)` rc 0; empty root → `MADO_VERIFY: DIVERGED (14 fail, 7 unknown, 2 pass)` rc 1 + `WRITTEN … rows=40`, and diff → `MADO_DIFF: CHANGED (rows 41→40; regressed=21 relabeled=6 vanished=1; detail-changed=32; scope=1)` rc 1; overwrite → `REFUSED (destination exists …)` rc 2; missing file → `SETUP (missing snapshot file …)` rc 2; header carries `# mado-verify snapshot v1`, `created=`, `tool=`, `gate-sha256=93e43f8f…`, `root=`, `scope=` | **PASS** |
| C5b | **the landing receipt itself** — the round's own tool applied across the landing | `--snapshot-diff` of my pre-landing receipt (`7da4ec50…`, 31 rows) vs post-landing receipt (`93e43f8f…`, 41 rows), same root | `MADO_DIFF: CHANGED (rows 31→41; regressed=0 recovered=0 flipped=0 relaxed=0 relabeled=0 appeared=10 vanished=0; detail-changed=0; scope=1)` rc 1, with each of the ten theme rows named as `DIFF_ROW appeared <id>: -→PASS/NOTE` | **PASS (the receipt exists and is exactly the ten theme rows)** |
| C6 | **Zero config mutation** | the boundary rule before/after every run, plus the gate's own row in every run | `bb2639d9a98045d4…` at 19:59:48Z = 20:16:32Z; `boundary.readonly PASS` with the same prefix in every baseline and landed run, `--no-live` and `--live`; `hyprland.conf` sha `4f52854a3c143dcf…` unchanged | **PASS** |

Aggregate: **the theme arms are real and green at `93e43f8f…` for the half
that landed** — ten file rows with every anchor independently re-read, hermetic
T1–T9 coverage, a re-cut pin that my own excision reproduces byte-exactly, and
a regression PASS whose receipt lines name the revision, the target and the
table. **What is still open is visible, not smoothed:** the two live theme rows
and the walker live-surface rows are unlanded at the measured revision, the
recorded defect spec was not extended for the new clauses, and the `theme`
plane's new clauses rest on the selftest scenarios (T1–T9) as their kill
vehicles so far. The snapshot-diff receipt re-measures green end-to-end at the
landed revision and produces the cleanest artifact of the round: a
`MADO_DIFF: CHANGED` whose only delta is `appeared=10` — the theme arms
appearing between the two receipts.

## 2. Re-run detail (commands and receipts)

- **Freeze.** `cp tools/mado-verify.sh /tmp/w9-aud-m9-gate/gate-93e43f8f.sh`
  (sha re-checked on the copy; every run below is against a frozen copy, never
  the moving worktree file).
- **Selftest, both revisions:**
  `bash gate-7da4ec50.sh --selftest` → `MADO_SELFTEST: 217/217 assertions
  passed` rc 0 (mtime of the run 19:59:19Z);
  `bash gate-93e43f8f.sh --selftest` → `268/268` rc 0 (20:06:39Z, re-run
  20:21Z — identical).
- **Verdicts, both revisions (frozen copies, `--no-live`/`--live`):**
  baseline `CLEAN (20 pass, 3 notes)` / `CLEAN (43 pass, 7 notes)`;
  landed `CLEAN (29 pass, 4 notes)` / `CLEAN (52 pass, 8 notes)` — counts lines
  quoted in the table above. The live runs read via `hyprctl` read verbs only.
- **Theme anchors (direct, read-only):** `sed -n '13p' ~/.config/hypr/hyprland.conf`;
  `cat ~/.config/omarchy/current/theme.name`; `readlink ~/.config/mako/config`;
  `readlink ~/.config/omarchy/current/background`; `pgrep -ax swaybg`;
  `ls -l` on the three theme part files. All equal the rows' details.
- **Regression, both revisions (my own runs, harness pinned):**
  `env MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh bash gate-<rev>.sh --regression`.
  Baseline: `MADO_REGRESSION: PASS (… target=d2bcdb31…)` rc 0, 30.2 s. Landed:
  `MADO_REGRESSION: PASS (… target=dc7c4141…)` rc 0, 53.9 s. The gate's own
  `REGRESSION_SPEC` line reads the recorded sha `c7ee75b9…` in both runs —
  the spec did not move with the gate (finding, C4).
- **The pin.** `PIN_MADO='dc7c4141449891cdd83bb603…'` at `:1290` of
  `93e43f8f…`. My excision —
  `sed -e '/…MADO-R7-REGRESSION-BLOCK >>>/,/…<<<…/d' -e '/…MADO-R7-SELFTEST-BLOCK …/d' -e '/…MADO-R8-BLOCK …/d'`
  — yields `dc7c4141449891cdd83bb603…` byte-exact, 1,945 L. The mid-edit
  revision `31364115…` was red on exactly this check (`R10: derived target …
  got 'dc7c4141…' want 'd2bcdb31…'`), i.e. the re-cut alarm did its job before
  the pin moved.
- **Receipts (frozen `93e43f8f…` copy):** `--no-live --snapshot …/r9-a.snap` →
  `MADO_SNAPSHOT: WRITTEN …` rc 0; second receipt `r9-b.snap` rc 0; diff pair →
  `MADO_DIFF: SAME` rc 0; empty-root run (`--root /tmp/w9-aud-m9-snap/root-empty`)
  → `DIVERGED (14 fail, 7 unknown, 2 pass)` + `WRITTEN … rows=40` rc 1; diff →
  `CHANGED` rc 1; re-write to `r9-a.snap` → `REFUSED` rc 2; missing file →
  `SETUP` rc 2. `head -6` of a receipt shows the magic, `created`, `tool`,
  `gate-sha256=93e43f8f…`, `root`, `scope`.
- **The landing receipt (C5b):** `bash gate-93e43f8f.sh --snapshot-diff
  /tmp/w9-aud-m9-snap/base-a.snap /tmp/w9-aud-m9-snap/r9-a.snap` — left =
  `7da4ec50…` receipt (created 19:59:55Z, 31 rows), right = `93e43f8f…`
  receipt (created 20:08:05Z, 41 rows), same root `/home/vgpnk`; verdict
  `MADO_DIFF: CHANGED (rows 31→41; … appeared=10 …; detail-changed=0; scope=1)`
  rc 1, with `DIFF_SCOPE gate-sha256: 7da4ec50… → 93e43f8f…` and ten
  `DIFF_ROW appeared theme.*` lines.
- **Census commands** (both revisions): `grep -cE '^ *row '` (162 → 189);
  `grep -cE '^ *row_from_rc '` (6 → 6); `grep -oE '^ *(row|row_from_rc)
  [a-z-]+ [a-z0-9._-]+' | awk '{print $NF}' | sort -u | wc -l` (51 → 55);
  per-plane `awk '{print $2}' | sort | uniq -c`; asserted ids
  `grep -oE 'st_row_(has|detail) "\$[a-z_0-9]+" [a-z0-9._-]+' | awk '{print
  $NF}' | sort -u | wc -l` (22 → 32).
- **Not landed at `93e43f8f…` (measured, not inferred):**
  `grep -c 'wallpaper.live\|display_agree'` → 0 and absent from a live run;
  `grep -c 'walker.sock'` → 0, walker plane still 2 row sites;
  `corpus/knowledge/walker-deep.md` sha `0982ba066c72575a…` (mtime 14:07:43
  −03:00) unchanged — `walker-deep-r9.md` is a **new** note (M9-2's), not the
  owed §10/§11 errata append; `corpus/lessons/` still 0 entries; defect spec
  unchanged (above). These are the round's own open items, carried to U2/U3.

## 3. Spot-checks (three, all re-run 2026-10-14)

1. **Pin/excision.** My own sed excision of the three marked families from
   `93e43f8f…` → `dc7c4141449891cdd83bb603…`, 1,945 L, byte-equal to the
   gate's `PIN_MADO` and to the target its own `--regression` derived; the
   pre-re-cut revision `31364115…` fails exactly here (R10) — the pin's
   consistency is measured, not assumed. File `derived-93e43f8f.sh`.
2. **Theme anchors, direct.** The five independent re-reads (hyprland.conf:13,
   theme.name, mako symlink, background symlink, swaybg argv) all equal the
   landed rows' details; `theme.parts.declared_only`'s NOTE lists the six
   declared parts with absent consumers. No substrate file was written.
3. **Zero mutation + counts.** Config-plane combined hash
   `bb2639d9a98045d4…` at 19:59:48Z and 20:16:32Z, equal to the gate's own
   `boundary.readonly` value in every run of mine; selftest counts 217 → 268;
   row-site census 168 → 195; asserted ids 22 → 32. (Ambient-locale variant of
   the hash is `579d2eda…` — the ordering is locale-sensitive and the gate
   exports `LC_ALL=C`; recorded so nobody re-derives a different constant.)

## 4. Unknowns

- **U1 — in-flight to the close.** The gate is uncommitted and has been
  byte-stable at `93e43f8f…` since 20:05:32Z, but the round was still landing
  artifacts (record draft 729 L, `walker-deep-r9.md`, `reports/r9-ver-m9.md`
  all appeared in my window). Revisions after my close, and the eventual
  commit, are unmeasured by me; the round's receipts should be re-derived from
  the commit, never from this report.
- **U2 — the live theme rows and the walker live-surface rows.** `theme.wallpaper.live`
  / `theme.name.display_agree` and the walker socket / D-Bus-owner /
  layer-invariant rows are unlanded at the measured revision. If they land
  later, this audit covers none of them; the note-shaped surface
  (`walker-live-surface.md` §4/§5) is the input.
- **U3 — kill vehicles for the new clauses.** The plan requires "every
  widening carries its mutant". At `93e43f8f…` the recorded defect spec is
  unchanged (`c7ee75b9…`, 10 defects), so the theme clauses' only kill
  vehicles I can see are the selftest scenarios T1–T9; whether the round
  lands spec mutants (or records why the scenarios are the kill vehicle) is
  undetermined. A surviving/absent mutant is a finding by the plan's own rule.
- **U4 — snapshot receipt long-run semantics.** Round-8's U2 carries: my pairs
  are minutes apart; the mode's stated purpose (verdicts across a day) is
  still unmeasured. The landing receipt (C5b) is the first cross-revision pair
  I know of, and it is same-day, same-host.
- **U5 — single host / toolchain / window.** bash 5.3.15, one measurement
  window 19:59–20:16Z 2026-10-14, harness `cf41efaa…` (recorded `b56c6e57…`
  stays provenance, not gated).
- **U6 — the record's numbers are not mine.** `plans/round-9-record-draft.md`
  and `reports/r9-ver-m9.md` were read only after my own measurements; where
  they quote gate numbers, those are their runs, not this lane's — my numbers
  above are independent and sha-pinned.