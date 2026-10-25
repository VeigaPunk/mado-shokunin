# SentinelScope — mado round 34, wave 1

Scope check: did any seat of this wave write outside `/home/vgpnk/Projects/shokunin/mado-shokunin`?
Verdict: **no seat write detected at the fleet root attributable to mado round 34.** Every dirty
fleet-root path is driver runtime, another lane's fetch debris, or pre-existing operator artifacts.
Nothing was deleted or moved.

## Fleet-root `git status --porcelain` (2026-10-24, no pathspec)

### Modified — all driver runtime, leave alone

| Path | Attribution |
|---|---|
| `.ufo/state/chousa.report-baseline` | Driver round counter (43) — chousa lane |
| `.ufo/state/kagi.report-baseline` | Driver (28) |
| `.ufo/state/kaidoku.report-baseline` | Driver (34) |
| `.ufo/state/kake.report-baseline` | Driver (50) |
| `.ufo/state/kama.report-baseline` | Driver (36) |
| `.ufo/state/kengaku.report-baseline` | Driver (29) |
| `.ufo/state/kumitate.report-baseline` | Driver (58) |
| `.ufo/state/mado.report-baseline` | Driver (34) — names mado only because it is the mado counter; written by `inline.sh` driver, not a seat |
| `.ufo/state/mori.report-baseline` | Driver (43) |
| `.ufo/state/souji.report-baseline` | Driver (22) |
| `.ufo/state/tameshi.report-baseline` | Driver (40) |
| `.ufo/state/tsukuroi.report-baseline` | Driver (36) |
| `.ufo/watchdog.log` | Driver launch/complete log; latest line `launch mado round=34 pgid=3166550 driver=hyaku-inline` — driver output, not a seat write |

`.ufo/state/` and `.ufo/watchdog.log` are declared driver runtime in AGENTS.md; expected churn while
the watchdog drives multiple lanes concurrently.

### Untracked — none name mado or round 34

| Path | Content observed | Names mado/r34? | Attribution |
|---|---|---|---|
| `.omp/mcp.json` | Tooling config (285 B) | no | Operator/tooling |
| `bm.json` | Cloudflare "Just a moment…" challenge HTML | no | Other-lane web-fetch debris |
| `live.html`, `nama.html`, `live_s228.html`, `tf_bavelas.html`, `wb2.html` | Fetched web pages; `wb2.html` is a Wayback bot-block page | no | Other-lane web-fetch debris |
| `s395.txt` | Empty (0 B) | no | Unknown stray; no mado content |
| `unblob.log` | `unblob` extraction log on `/tmp/test-fw.bin`, dated 2026-10-24 02:00 | no | Firmware-reversing lane debris (predates r34 launch 21:40) |
| `write` | Contains `agent://U100N079H334f935b` | no | Stray redirect artifact; no mado content |
| `xc.xml` | "Too many requests" page (Perseus) | no | Other-lane web-fetch debris |
| `scripts/hyaku/append-closure.py.bak-20261023T040735Z` | Backup of operator script, timestamped 2026-10-23 | no | Operator backup, predates round 34 |
| `scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z` | Same | no | Operator backup, predates round 34 |
| `.ufo/state/kotoba.report-baseline`, `kotodama.report-baseline`, `revenger.report-baseline` | New driver counters (67/68/67) | no | Driver — new lanes rostered since last commit |

Grep for `mado|round[-_ ]?34` over every untracked path: zero matches. No seat wrote here.

## Lane-side writes under `mado-shokunin/.ufo/waves/round-34/scratch/`

All regular files, no symlinks, every path inside the scratch tree:

- `ConnRound30Cite/cite.md` (299 B)
- `ExecAxisRun/run.txt` (515 B)
- `ExecCensus/census.txt` (976 B)
- `ExecSizes/sizes.tsv` (1304 B)
- `MutC2Drop/count.py` (5196 B)
- `ScoutS201/backend.cpp` (6550 B)
- `ScoutS202/window.cpp` (8324 B)
- `ExecSelftest/` — directory exists, no files

**Confirmed: every scratch artifact is under `.ufo/waves/round-34/scratch/` inside the mado lane
repo.** Other round-34 files (`build-w1-spec.py`, `dispatch-w1.sh`, `w1-spec.json`,
`w1-taskcall.json`, `assimilation/`, `w1/`) are also inside the lane's `.ufo/waves/round-34/`
tree — in bounds. Round-33 untracked leftovers (`round-33/scratch/*`, `round-33/controls/*`)
are prior-round residue inside the lane, not this wave's writes.

## Conclusion

Zero out-of-bounds seat writes. Fleet-root dirt is driver counters + watchdog log + other lanes'
fetch leftovers + operator `.bak` files — all hands-off per instructions.
