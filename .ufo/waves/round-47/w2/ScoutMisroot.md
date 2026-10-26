# ScoutMisroot — misrooted round-47 seat files (mado w2, read-only sweep)

Verdict: **no misrooted mado round-47 seat file found.** No hole to re-register. Nothing moved or deleted.

## Q1 — fleet `git status --porcelain` (repo /home/vgpnk/Projects/shokunin, tip 34a47b1a)
- `git -C /home/vgpnk/Projects/shokunin status --porcelain` → 0 lines; `-uall` → 0 lines. Zero untracked paths, so none names mado r47 or a r47 seat.
- Why it is empty: fleet `.gitignore:1` is `*-shokunin/` (`git check-ignore -v mado-shokunin`), so every lane tree is invisible to fleet status. The lane's own repo is the one with untracked r47 files.
- `--ignored` outside `.jj/`, lane dirs, `.tower/` showed only `.tower/comms/*` (r18, 2026-10-15/24, not mado r47).
- Fleet-root files newer than 2026-10-26 10:00: `.ufo`, `.scratch`, `.git`, `.gitignore`, `LOG.md`, `SCORECARD.md`, `MANIFEST.json`, and the lane dirs kaidoku/kasegi/kama/tsukuroi. Fleet-root stray `m-rev-vs-rev.py` (Oct 25) is tracked and predates r47. `ok/` is an empty dir (Oct 25).

## Content sweep of fleet-owned and other-lane trees (excluding mado lane, .git, .jj, .tower, MANIFEST.json)
Pattern: `mado-r47`, `mado round 47`, `mado-shokunin/.ufo/waves/round-47`, `xdg-terminal-selection-r47`, `mado-terminal.py`. Command: `grep -rIl ... ` (timeout 120). Hits, each checked:
- `.ufo/prompts/mado-round-47.md` — the orchestrator's own mado r47 prompt (fleet-owned, expected).
- `.ufo/state/disk-guard.log`, `.ufo/state/inline-dispatcher.log` — orchestrator logs naming `/fast/scratch/hyaku/mado-r47` and `w1-results.json` (expected).
- `.scratch/goal-20261026-hyaku-run9.md:192` — operator goal file citing the ExecRefB runaway path (expected).
- `kasegi/.../LabScratchClean.md:12,18`, `kengaku/.../R43ScoutMisroot.md:66`, `tsukuroi/.../SentMisroot.md:18`, `tabi/.../ScoutMisrootSweep.md:22` — other lanes' own seats' reports that mention `mado-r47` as someone else's /fast/scratch dir. Their own lanes; not mado seat output.
- Pattern `round-47/w[12]/` hits (`.ufo/reports/round-47/{chousa,tameshi,kama}.md`, `.ufo/reports/round-48/kake.md`, kasegi round-28/29/36 files, `kake/corpus/lessons/round-48.md`): those files contain 0 occurrences of "mado" in the five checked, so they cite their own lanes' round-47.
- Basename sweep: all 83 w1/w2 seat names against every fleet path outside the mado lane. Matches (e.g. `ScoutMisroot.md`, `ConnClaims.md`, `MutC2Counter.md`, `CritMistakes.md`, `ExecRows.md`) are other lanes' older-round files (kasegi r25..r37, kake r37..r57, kumitate, kotoba, kengaku, kaidoku). Name reuse across lanes, not misroots. No file named `*r47*` / `*Misroot*` at fleet level belongs to mado r47 (the `.ufo/prompts/*-round-47.md` and `.ufo/reports/round-47/` entries are other lanes' round 47).
- No path outside the lane contains `mado-terminal.py`, `xdg-terminal-selection-r47`, or `mado-shokunin/.ufo/waves/round-47/w`, other than the files above.

## Q2 — `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47`
Allowed subdirs present: `w1/ w2/ ctl/ receipts/ fetch/ l1-draft/ assimilation/` (all 7 dirs, no others).
**Files outside the allowed subdirs (all at round-47 top level; 15 files):**

| path | size | note |
|---|---|---|
| claims.md | 1982 | L1 declared claims |
| registration.md | 8148 | L1 freeze (the file seats were told to read first) |
| make-w1-spec.py, make-w2-spec.py | 45967, 25925 | spec generators |
| w1-spec.json, w2-spec.json | 69325, 60533 | specs |
| w1-dispatch.json, w2-dispatch.json | 82470, 74774 | dispatch records |
| w1-results.json | 232905 | w1 results (41 seats) |
| w1.ready, w2.ready | 148 each | ready markers |
| w1.ready.dispatched, w2.ready.dispatched | 1287, 1545 | dispatcher acks |
| w1-run.err, w2-run.err | 0 | empty |

These are orchestrator/L1 artifacts (inline-dispatcher.log:3118 `done mado w1 .../w1-results.json`), not seat output. None is seat-misrooted. Observations only: `__pycache__/` exists in `ctl/` and `l1-draft/` (python byproduct); `fetch/` holds `xdg-terminal-exec`, spec/man/test pins and `omarchy/`; `w1/` and `w2/` each contain `swarm-registry.json` besides seat dirs/reports (non-seat file, orchestrator registry).
- Lane repo `git status -uall` outside round-47: **empty**; all untracked paths are under `.ufo/waves/round-47/`. So `tools/mado-terminal.py` and `corpus/knowledge/xdg-terminal-selection-r47.md` are still absent (as stated).

## Seat report-path check (w1-results.json, 41 seats)
- Path regex over each seat's output: every `.ufo/...` report path that is named exists under `w1/`. Two paths carry a parenthetical suffix (`ExecCounterC2.md (11776 B...)`, `ScoutShokuknow/report.md (copy at ...)`); on disk `w1/ExecCounterC2.md` (11776 B) and `w1/ScoutShokuknow.md` + `w1/ScoutShokuknow/report.md` exist. No report landed elsewhere.
- Seats whose JSON output carries no `"report"` key (ExecOracle, ExecCounterC1, ExecLive, ExecCache, ExecSupersede, ExecR2Digest, ExecAxisBase, ExecRefCompare, ScoutOmarchy, ScoutHeld, ScrEntry, ScrRows, ScrErrataR45, ScrSkill, CritClaimSizing, CritRoutedItems, ConnSiblings, RevengerUwsm): the format simply differs; their dirs/files are in w1 (83 entries in w1). Not verified one by one for content.
- Out-of-lane paths named in seat outputs are reads/runs, not writes, by evidence: fleet `scripts/` mtimes are `sources-census.sh` 2026-10-19 and `hyaku/` 2026-10-26 11:52 (before w1 began 18:xx; orchestrator's); `shokuknow` has no file newer than 2026-10-26 10:00; `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` mtime 2026-10-24. `/fast/scratch/hyaku/mado-r26/wlroots/build` is cited by ScrToolLedger as an older path.
- Host cache `~/.cache/xdg-terminal-exec` directory mtime 2026-10-26 17:42 (the known w1 rewrite incident; cited by ExecRefB, SentHost, RevengerUwsm). Not a r47 w2 write; not changed here.

## Scratch
`/fast/scratch/hyaku/mado-r47/` has 41 seat dirs (w2 seats plus `l1`), all younger than 10 min at 19:40; ExecRefB's runaway dir is no longer listed. I wrote nothing there.

Repro: `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall; git -C /home/vgpnk/Projects/shokunin check-ignore -v mado-shokunin; ls -la /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47; git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain -uall | grep -v ' \.ufo/waves/round-47/'`
