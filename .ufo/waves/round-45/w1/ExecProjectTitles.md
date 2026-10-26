# ExecProjectTitles — round-45 w1 (D1: shape-only projections of the tracked live client dumps)

**Result: done, 2 of 2 live dumps projected; 20 synthetic dumps identified and left alone; no
original edited.** Pin `0c89478af821a6424c9ac922eafe02e39630cf4f`.

## Sweep

`git grep -l -E '"(initialTitle|title)"' <pin> -- .ufo` → 154 files. Classified mechanically
(`w1/ExecProjectTitles/sweep.py`, output `sweep.json`): 86 upstream source pins, 17 prose,
15 other, 8 fixture JSONL, 6 upstream XML, **22 client-shaped JSON = 2 live + 20 synthetic**.
Nothing left unclassified (the script exits non-zero if anything is).

## Live dumps → projections (`w1/ExecProjectTitles/proj/<same path>`)

| path | titles before → after | sha256 old → new |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` | 8 (`title`×4, `initialTitle`×4; 20 title-family fields) → 0 | `6cdada1a…e06b` → `4f2a8776…1c46` |
| `.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` | 8 (20) → 0 | `e4b1fb72…ba0c` → `4f2a8776…1c46` |

Each: 4 elements kept, element order preserved, 32 → the reference 7 keys
(`address, mapped, class, floating, size, at, monitor`, in the reference file's literal order),
`json.dumps(indent=2)` + newline, 3537 B → 839 B. The two projections are byte-identical
because the two originals differ only in `title` — the removed bytes are exactly the
per-session material.

## Synthetic, no projection

18 × `.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/{dump,receipt}-*.json` — nested
`bwrap` oracle instance, monitor `HEADLESS-2`, the seat's own `gkeep-shm` probe client, sandbox
pids, `libwlroots` from `/fast/scratch`; no host session read. 2 ×
`.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/client{1,2}.json` — hand-written lesson
fixture (`address` `0x1`/`0x2`, no `at`/`monitor`). Full reasons in `report.md` §3.

## Evidence (all re-runnable)

`w1/ExecProjectTitles/proj-verify.txt` is the transcript: `project.py` (9 checks per file + a
seat-wide check that no title-only value survives anywhere in the seat dir), `crosscheck.py`
(independent jaq rebuild equals the emitted bytes; style round-trip; the originals differ only in
title), `sweep.py`, `citecheck.py` (12 cited locators + 14 numbers recomputed), `grep` showing 0
title tokens, sha256 of old and new, and lane `git status` showing only this wave directory
untracked. Every input was read with `git show`; no `hyprctl`, no host file, no compositor state.

## Landing (L1, not done here)

```
install -m 644 .ufo/waves/round-45/w1/ExecProjectTitles/proj/.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json .ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json
install -m 644 .ufo/waves/round-45/w1/ExecProjectTitles/proj/.ufo/waves/round-43/w2/SentLiveRun/dump-now.json .ufo/waves/round-43/w2/SentLiveRun/dump-now.json
```

Five existing receipts quote the old sha256 and become historical after landing (do not edit):
`.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt:112`, `.ufo/waves/round-43/w1/ExecLiveHost.md:17`
and `:55`, `.ufo/waves/round-43/w1-results.json:40`, `.ufo/waves/round-43/w2/SentLiveRun/hashes.txt:1`.

## Risks

- **Git history still holds the titles.** Replacing the working tree does not unpublish the old
  blobs in a public repo; that is an operator/L1 decision, not a seat's.
- Sweep is pin-scoped; re-run `sweep.py` at the integration tip for any round-45 live dump.
- Round-44 w1 already projects its live artefacts at 10 keys (7 + the `fullscreen` trio);
  standardising on the round-43 seven is a separate change and I did not touch those files.

Tooling: nothing installed. `python3` 3.14.8, `git` 2.56.0, `jq` on PATH is **jaq 3.1.1**
(jq-compatible) — i.e. the cross-check is a genuinely separate implementation.
