# PtrRemainingPlanesCensus — R18-V3 freshness pointer appended to remaining-planes-census.md; old prefix byte-identical

## Scope

- Target: `corpus/knowledge/remaining-planes-census.md` (sole writer this wave), append-only.
- Routed defect: R18-V3 (walker 2.17.0 pins without an in-file pointer; host moved to 2.17.2).

## Lines containing `2.17.0` (grep -n, before edit)

- One hit in the old note: line 246 — `0.15.0-3 · walker 2.17.0-1 · alacritty 0.17.0-1 · uwsm 0.26.7-1 · sddm` (§4 "Packages (shape)").

## Hashes and prefix check

- before: sha256 `710e3e289643f2ff1ebb21522f662c31302bf06c6d467b3e110f49f0bb859f06`, 20,512 B; the old final line had no trailing newline.
- after: sha256 `b1016a4b6b36172021b3d3b2f9357dd8ea1926d19c9d1f07606be6e16b1e6d78`, 22,211 B.
- Prefix: `head -c 20512` of the new file has sha256 `710e3e28…9f06` = the before hash (checked before and after the final write).
- `cmp -n 20512` of a pre-edit copy (`/tmp/rpc-old.md`) against the new file: identical.
- Two append steps: first the block (with a leading newline), then one extra `\n` inserted at byte 20,512 so the heading gets a blank line before it. Both steps only add bytes after the old prefix.

## Appended block (file lines 335-343)

- Line 335 blank; line 336 `## Freshness pointer (round 19, 2026-10-20)`.
- Bullets at lines 338-343 (one line each; under the 20-line limit).
- Line 338 (first bullet) contains `2.17.2` and `S090` on the same line, plus `/var/log/pacman.log:2929`, line 246 and `corpus/knowledge/walker-route-r18.md`. It also names S096 as reserved and not yet recorded.
- Line 339: version-bound, dated — line 246 only (walker 2.17.0-1 in the package-shape list). The other package versions on that line are 2026-10-14 pins, not re-measured.
- Line 340: walker process and CSS-import rows (§2 walker row, §4 clients) — dated point samples; S090 lines 3062 and 3123 (walker-restart.hook) noted; no live walker fact re-asserted.
- Line 341: version-independent (theme-tree census and sha pins §1, symlink targets, hyprsunset/hyprlock pins, session/portal/monitor shape §4, §6 spot-checks) — still 2026-10-14 point samples dated by the probe window; none depends on walker version.
- Line 342: not in the note — walker help text, walker binary sha, config line counts, `walker --version` output; nothing asserted, nothing to re-pin.
- Line 343 verbatim: `Not re-measured live this round (host pause): behaviour of the 2.17.2 binary stays [UNK].`

## Behaviour verified

- Read verbs on repo files only (`sha256sum`, `wc`, `stat`, `grep -n`, `head -c`, `tail -c`, `cmp`, `sed -n`, `od -c`), one `cp` into `/tmp` as the pre-edit copy, and two appends/rewrites of the note via shell.
- No host command (pacman, systemctl, hyprctl, walker, etc.) was run. No host file was read. No git or jj command was run.
- The live gate was not run; `fresh-pins.py` and `tw-recall.py` were not run (outside this item).

## Findings

- R18-V3 pointer for this note: done. The note carries a dated pointer to walker 2.17.2 with S090 and the round-18 route note.
- Fresh-pin effect (not measured by me): the note's `2.17.0` lines are now 246 (old, unchanged) and 339 (inside the dated block, which sits next to the `2.17.2` line 338 carrying `S090`). L1 should confirm the `fresh-pins.py` result after the run.
- No other file was touched. S096 is still unrecorded; no SOURCES row was created (not my file).

## Limits

- Did not open `/var/log/pacman.log` or the S090 host bytes this round (host pause); the pointer relies on the SOURCES.md S090 row as recorded.
- Did not read the body of `walker-route-r18.md` beyond its header and a grep for `2.17`; the pointer names it as current routing.
- The S096 binary-bytes row does not exist yet; the block states it as reserved.

## Installs

none
