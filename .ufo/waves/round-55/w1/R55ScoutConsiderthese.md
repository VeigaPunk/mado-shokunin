# R55ScoutConsiderthese — report (round 55, wave w1, scout)

Deliverable: `.ufo/waves/round-55/w1/R55ScoutConsiderthese/considerthese.md`. Scope: the twelve "proposals only; not acted on" items in `considerthese/2026-10-26.md` (lines 47-52) and `considerthese/2026-10-25.md` (lines 46-51), mapped against frozen C1/C2/C3 and the freeze-order checker. Pick: proposal 26-4 (re-run one tool myself, read-only). Leaf seat; no dispatch; no lane edits; no git mutation; no installs; no scratch created; no hold-out path read.

## What I did (commands and decisive output)

1. Read both considerthese files and `round-55/claims-frozen.md` and `registration.md` (contract text; not edited).
2. Listing of round-55 contract and receipts, plus `git -C <lane> rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/mado-shokunin` and `git log -1` → `dbc2eef…` (read-only).
3. Grep for mining records of each proposal across `corpus/`, `quality/`, `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-4[4-9]`. Decisive hits:
   - `corpus/lessons/round-45.md:81`: 26-1 → `quality/check-session-material.py` + QUALITY 85.
   - `corpus/lessons/round-41.md:277`: 25-5 → QUALITY 76.
   - `corpus/lessons/round-44.md:248`: 25-1 → `quality/ratio-domain-meta.py` (provenance line 4 of that file: "`considerthese/2026-10-25.md:46` proposal 1").
   - `corpus/lessons/round-46.md:365`: 26-3 → QUALITY 90.
   - `corpus/lessons/round-47.md:336`: 26-2 draft refused.
   - `corpus/lessons/round-48.md:186-187`: 26-6 → QUALITY 99.
   - `corpus/lessons/round-39.md:80-82`: 25-3 served by the r39 C1 re-registration.
   - `corpus/QUALITY.md:409`: criterion 81 (attempts/dirty closures; from 25-2).
   - Zero hits for "2026-10-26 … proposal 4" or "re-run … tool … myself" (26-4). Zero hits for 25-4 and 25-6 beyond unrelated `debug:disable_logs` facts.
4. Host reads (allowlist only): `cmp /home/vgpnk/.config/hypr/input.conf …/round-55/fetch/host-input.conf` → `SAME_BYTES`; `ls -la` on the same file (1584 B). No `hyprctl` run at all.
5. Pin checks (read-only): `cd …/round-55/fetch && sha256sum -c SHA256SUMS.txt` → all 10 entries `OK`. `sed -n '1282,1283p' Hyprland-InputManager.cpp` → `pKeyboard->m_repeatRate  = std::max(0, REPEATRATE);` and the `REPEATDELAY` twin (matches the frozen anchor). `sed -n '277,280p' Hyprland-ConfigValues.cpp` → the `input:repeat_rate` default 25, range 0–200; `input:repeat_delay` default 600, range 0–2000 (matches `registration.md` §C2 ranges and defaults).
6. Contract line: `sed -n '60,63p' registration.md` → "`tools/mado-kbdopts.py` — read-only; reads only the files named by `--config` and `--getoption`; starts no process, opens no socket, writes nothing." (`registration.md:62-63`).
7. Tool docstring: `grep -nE 'sourced|\.conf' tools/mado-options.py` → line 10 "graph of DIR/.config/hypr/hyprland.conf depth-first in line order" (reads beyond the seat allowlist).
8. Ledger: `quality/tool-ledger.md` present with `| instrument | description | accountability pointer |` header; freshness not a column.

## Findings (decisive)

- The "not acted on" headers in both files are stale: mining records exist for 9 of 12 items (26-1 partial, 26-2 partial, 26-3, 26-5 via 25-1, 26-6, 25-1, 25-2, 25-3, 25-5). Unmined by grep: 25-4, 25-6, 26-4.
- 25-3's premise ("check whether round 38 lands it") is past; it was closed in r38/r39.
- 26-5 restates 25-1; 25-5 restates the 24-5 practice (r33). Both are duplicates across files.
- The frozen C2 harness reads committed copies (`fetch/host-input.conf`, `fetch/host-getoption.json`) and so cannot itself evidence a live run; a live re-run is a separate act.
- `tools/mado-options.py` reads the sourced config tree, so this seat cannot re-run it inside its allowlist. C2 is the first tool whose inputs fall inside the allowlist.
- Observation for L1 (not a claim): the committed `fetch/host-input.conf` is byte-identical to the live `~/.config/hypr/input.conf`, contains no `/home` or `vgpnk` string, and is a host-config copy in a repo the file calls public. The privacy gate's shapes do not target this class.

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScoutConsiderthese/considerthese.md`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScoutConsiderthese.md` (this report)

Only the deliverable directory was created (`mkdir -p`). No other file was written.

## Defects and ambiguities

1. Stale headers in `considerthese/2026-10-25.md:44` and `considerthese/2026-10-26.md:45` (see Findings). Not edited.
2. "Unmined" for 25-4, 25-6 and 26-4 is from grep only; not exhaustive across `.ufo/waves/`.
3. The QUALITY numbers were read at the cited lines; criteria 76, 81, 82, 85, 90 and 99 were not re-derived by a checker.
4. The round-55 root holds `w1.ready.partial` (1048 B, mtime 19:50) and `w1-run.err` (0 B); not within this seat's scope, and I did not check whether they are tracked or what they mean for the freeze-order item. Flagged for L1.

## Not verified / not run

- `mado-kbdopts.py` (not built yet), the frozen counters, `check-session-material.py`, and the round-55 freeze-order checker: not run; not this seat's assignment.
- No hyprctl command beyond the allowlist; `hyprctl getoption` and `devices` were not run by this seat.
- Hold-out fixtures: not looked for, not read.
- Scratch: none created; nothing to remove.
- Tooling: nothing installed or upgraded.
- Git: read-only `rev-parse` and `log` on the lane; no commit, checkout, stash, reset or push.
