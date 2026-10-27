# ScoutMisroot — round 48 w2 · fleet-root misroot quarantine and scope

Verdict: **quarantine claim confirmed; no other round-48-attributable untracked file at the fleet root; attribution of the writer is NOT proven (and cannot be by bytes).** Read-only seat: no fleet-root file written or deleted, no scratch created (no shell writer ran, so `ulimit -f 2048` was never needed; the only files written are this report), no pacman, no git/jj mutation, no GUI.

Paths below are absolute under `/home/vgpnk/Projects/shokunin` (`F`).

## 1. What the notice says (observed)
Orchestrator log `F/.scratch/goal-20261026-hyaku-run9.md:221-225`: at 20:44 -03 `tree.json` (347495 B, GitHub API tree dump of hyprwm/Hyprland `efb50993`) appeared at the fleet root; "the Hyprland keymap scouting shape attributes it to a mado r48 w1 seat with cwd = fleet root". Moved bytes unchanged to ignored `F/.tower/quarantine/fleet-root-strays-20261026T2055/` (sha256 in `SHA256SUMS` there), MadoR48 told, "a conformance item for mado r48's closure". It also states `.ufo/reports/round-49/kama.md` was in-flight, not a stray.

## 2. Which file moved, and hash equality (observed)
- `ls -la --time-style=full-iso` of `F/.tower/quarantine/fleet-root-strays-20261026T2055/`: exactly two files, `tree.json` (347495 B, mtime 20:44:14.65) and `SHA256SUMS` (76 B, written 20:48:20). Only `tree.json` moved.
- `SHA256SUMS` content: `fdb0b7a49736a50b956ef899b64a4381547a0b37a4663a3eae46f731257e16d3  tree.json`. `sha256sum -c SHA256SUMS` -> `tree.json: OK`. `stat` size 347495 = the size named in the notice.
- Content parse (`python3 json.load`): `sha` = `efb50993780079460b0cbed1363e2166a2de1d9f`, `truncated` = False, 1181 tree entries. Matches the notice's description.
- **Hash equality with a lane path:** `sha256sum` of `F/mado-shokunin/.ufo/waves/round-44/w1/ExecFsSemantics/pins/tree.json` = same `fdb0b7a4…16d3`; `cmp` of the two files -> byte-identical. That lane file is a tracked, committed round-44 pin (lane commit `290cddea92a18e2202456db89cb2bb60d9aaacff`, 2026-10-26T14:36:49-03:00; `git ls-files --error-unmatch` ok; `pins/SOURCES.md:5` names the URL `https://api.github.com/repos/hyprwm/Hyprland/git/trees/efb50993…?recursive=1`; line 28 of `pins/SHA256SUMS.txt` carries the same hash).
- Consequence (inference): the stray is not new data. Any seat that fetched the same API URL, or copied the r44 pin, produces these exact bytes, so the hash proves the *content* and its provenance (round-44 pin) but cannot identify the *writer*.
- No round-48 report names this hash: `grep -r fdb0b7a4` over the lane `.ufo` and fleet `.ufo`/`.scratch` found only the round-44 `SHA256SUMS.txt` line.

## 3. Seat reports — admissions and denials (observed)
No round-48 seat report admits writing a fleet-root `tree.json`.
- Deny, with scratch-only evidence: `w1/ExecXkbLive.md:251-256` (three absolute paths, "find on the fleet root shows no tree.json"); `w1/ExecXkbSource.md:112-113`; `w1/CritPremiseC2.md:23-24`; `w1/ScoutXkbSpecs.md:93` (says it wrote "its one tree.json, a GitHub trees API dump, … inside the scratch dir after `cd` there" — i.e. this seat did fetch the same kind of dump, but its fetch dir `w1/ScoutXkbSpecs/fetch/SHA256SUMS` has no tree.json entry and scratch was removed, so that file is no longer checkable).
- Silent: `w1/ScoutHyprKeymap.md` (the seat the notice's "shape" points at) contains no `tree.json`, `fleet`, `cwd` or `api.github` string; it only says the rules.c files "were fetched earlier in scratch" (line 39). Its report mtime is 20:46:48, two minutes after the stray's 20:44:14 mtime; ScoutXkbSpecs.md mtime is 20:48:57.
- Timeline fits both ScoutHyprKeymap and ScoutXkbSpecs (and any other seat running at 20:44). Writer: **unattributed**. The notice's attribution is the orchestrator's inference; it is not corroborated or refuted by any seat byte.
- Lane receipt `receipts/m48-revived-r47-seat-edit.diff:15-17` (the round-48 r47-seat-edit) already adds the rule "never `tree.json` and never in the fleet root" to the revived seat text, so the incident is handled as a conformance item, not left silent. (The `cd` into the fleet root named there is for the read-only `scripts/sources-census.sh`.)
- Related, not this incident: `w1/ConnClaims.md:24` records ExecD2Receipt ran a fleet-root-relative path (rc=2) — a failed read, no file produced.

## 4. Other fleet-root untracked files attributable to round 48 (observed: none)
- `git -C F status --porcelain -uall` -> empty. `git status --ignored=traditional` ignored set outside `.jj/` and `.ufo/state/`: `.tower/`, `.ufo/watchdog.log`, `.ufo/waves/*/x{connector,sentinel}-scratch/`, and the `*-shokunin/` lane dirs. Nothing else.
- `find` at the fleet root (excluding `.git .jj .tower` and lane dirs) for files newer than 2026-10-26 20:00: only prompts, reports, `MANIFEST.json`, `l0-questions.md`, `watchdog.log`, `.scratch/goal-…run9.md`, `scripts/hyaku/lane-addendum.md`; every one is tracked or ignored-by-rule (status clean). No `tree.json`, `p.out`, `p.err`, `fx/`, `=NNNN`, `T`, or `*.synthetic` at depth <= 2 outside lanes and `.tower`.
- Fleet-root top-level files (`ls`) are all tracked entries with mtimes before round 48 or the known 15:29/22:13 LOG/SCORECARD/MANIFEST updates; the empty `ok/` dir dates 2026-10-25 16:43 (pre-round).
- The other quarantine dirs are not round 48: `…T1956` (`=1239`, `=3900`, `T`; orchestrator log: unattributed, tsukuroi r43-pin-audit-shaped), `…T2010` (`p.out`, `p.err` — chousa r52), `…T2114` (`fx/A2-uppercase-fsid-sysfs/…/scrub_speed_max` — tsukuroi r44). Each also carries its own record in the run9 log; none names mado r48.
- Lane side (`F/mado-shokunin`, a separate git root): HEAD `3e6c848a…`, status shows tracked `M` files (SKILL.md, corpus/*, quality/check-session-material.py, tools/mado-terminal.py, lessons/round-47.md) and one `??` outside round-48 dirs: `.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json.synthetic` (a round-48 marker-gate install sidecar presumably, per `w1/ExecSessionMarker.md`; not a fleet-root file). I did not inspect further; out of this seat's task.
- The wave directory `F/mado-shokunin/.ufo/waves/round-48/w1/` holds no `tree.json` file anywhere (`find -iname '*tree*'` hits only `ExecLsEmu/receipts/real-tree.txt` and `SentPrivacy/receipts/scan_tree.py`).

## 5. Findings for the L1 (concerns, no action taken)
1. Misroot confirmed, quarantined bytes intact, hash verified (`tree.json: OK`), and identical to a committed round-44 pin. The closure item should say "writer unattributed; content equal to r44 pin `pins/tree.json`" rather than "ScoutHyprKeymap wrote it".
2. `w1/ScoutHyprKeymap.md` is the only suspect seat that neither admits nor denies; a one-line statement from that seat (or the L1) would close the attribution. I could not obtain it (no transcript access asked; leaf scope).
3. `w1/ScoutXkbSpecs.md:93` itself admits a trees-API dump existed in its scratch; the seat's own claim is unverifiable now (scratch deleted, no hash recorded).
4. No frozen predicate (C1/C2 counters, fixtures, claims) depends on the fleet-root file; the stray does not affect any frozen data.
5. Residual: `git status` can only prove absence at 22:2x -03 now; a stray created and removed in between would not show. Any later one is outside this check.

## Evidence index (commands run, all read-only)
`ls`, `find`, `stat`, `sha256sum -c`, `sha256sum`, `cmp`, `git -C F status --porcelain -uall`, `git status --ignored=traditional`, `git ls-files --error-unmatch`, `git log -1 -- <pin>`, `grep`, `python3 -c json.load` (stdout only). Largest output file written by this seat: this report. Scratch: none created, none to clean.
