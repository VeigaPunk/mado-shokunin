# D1 — shape-only projections of the tracked live client dumps

Seat `ExecProjectTitles`, mado round 45 w1. Pin `0c89478af821a6424c9ac922eafe02e39630cf4f`.
Deliverable is `proj/<same repo-relative path>`; **no original was edited** — the L1 lands the
replacements. No `hyprctl` call, no compositor state, no host config byte was read for this
seat: every input came from `git show <pin>:<path>`.

## 1. Sweep

Command (as specified), run at the pin over the whole tracked tree:

```
git grep -l -E '"(initialTitle|title)"' 0c89478af821a6424c9ac922eafe02e39630cf4f -- .ufo
```

154 hits. `sweep.py` classified every one (`sweep.json` in this directory):

| kind | count | what it is |
|---|---|---|
| `upstream_source_pin` | 86 | fetch pins: 74 `.bin`, 9 `.cpp` (HyprCtl/Rule/hyprctl source), 3 `.html` |
| `prose` | 17 | seat reports, notes and the round-44 leak receipt — the keys as words, not client objects |
| `other` | 15 | guard/evidence JSON (rounds 17, 22, 23), guard and probe scripts (`.py`, one `.c` pin), one `.html.live` capture |
| `fixture_jsonl` | 8 | round-18/19 frozen prompt inputs (`r13-root`, `r14-source-safety`) and their four round-21 snapshot copies |
| `upstream_xml` | 6 | walker/browser layout XML and protocol XML |
| `client_dump` | 22 | client-shaped JSON, i.e. real or synthetic `hyprctl clients -j` |

Of the 22 client-shaped files, 2 are live host dumps and 20 are a seat's own synthetic windows
(§3). `sweep.py` exits non-zero if any client-shaped file is left unclassified; it exited 0.

## 2. Live dumps → projections

Both files are live `hyprctl clients -j` output: 4 real session windows each, host addresses,
host pids, `mapped: true`, `monitor: 0`, real `class` values. `host-clients-live.json` is the
round-43 ExecLiveHost capture whose provenance the seat itself recorded at
`.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt:109` (`$ hyprctl clients -j > host-clients-live.json`).

| path | kind | titles before | after | sha256 old → new |
|---|---|---|---|---|
| `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` | live host dump, 4 windows | 8 (`title`×4, `initialTitle`×4; 20 title-family fields incl. `initialClass`, `xdgDescription`, `xdgTag`) | 0 | `6cdada1a687201ebc42f73c58da27137189d5cc2b5f419c512c3956bab95e06b` → `4f2a877634f33b0e3492b76c19d958eeafa17d3d2ab4a5a2d1ee1df5e8301c46` |
| `.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` | live host dump, 4 windows | 8 (`title`×4, `initialTitle`×4; 20 title-family fields) | 0 | `e4b1fb7232e6709befddb92f1a23e8d9f08497d70f355b23523690671568ba0c` → `4f2a877634f33b0e3492b76c19d958eeafa17d3d2ab4a5a2d1ee1df5e8301c46` |

Each element goes from 32 keys to the 7 of `.ufo/waves/round-43/fetch/host-clients-r43.json`
(25 keys dropped per element, 5 of them title-family). Element count (4) and element order
(the `address` sequence) are unchanged; `json.dumps(indent=2)` + one trailing newline; 3537 B →
839 B each.

Key order is the reference file's literal order, `address, mapped, class, floating, size, at,
monitor` (read from the reference bytes, `od -c`), not the alphabetical listing in the seat
spec — those are the same seven keys; the reference is the artefact that a diff will be taken
against. The reference file is itself serialised at `indent=1` (711 B); the emitted projections
follow the spec's `indent=2`.

## 3. Synthetic / no-projection decisions

| paths (count) | decision | why |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/{dump,receipt}-*.json` (18) | synthetic test window — no projection | nested `bwrap --unshare-all` Hyprland instance (`receipt-host-r1.json` `cmd`/`steps`), monitor `HEADLESS-2`, client is the seat's own `gkeep-shm` probe with title `gkeep-oracle-probe`, sandbox pids 54/57, `libwlroots` from `/fast/scratch/hyaku/mado-r43/oracle/`. No host session was read; nothing there is session material |
| `.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/client1.json`, `client2.json` (2) | hand-written lesson fixture — no projection | `address` `0x1`/`0x2`, 7-key reduced shape with no `at`/`monitor`, class `org.omarchy.gkeep`, title `gkeep`: a teaching example, and it does not even carry the reference's 7 keys |
| `.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt:7` | synthetic, left alone | one verbatim client line for the same probe title; probe label, not session material |

Also inspected and clean of client data: `.ufo/waves/round-44/w1/SentLiveReads/evidence/leak.txt`
(prose only — it withholds the very values it reports), `.ufo/evidence/round-12/getprop-measure.txt`
(round-12 already used a title-free `jq` projection: `getprop-measure.txt:6` `## Window selection: title-free projection`, and `:4` states no window titles were requested, emitted or recorded).

## 4. Findings

- **F1 — D1's residual set at the pin is exactly these 2 files.** `sweep.py` found no third
  live dump. Supporting: round-44 w1 had already applied the same discipline to its own live
  artefacts — `.ufo/waves/round-44/w1/ExecLiveHost/live-clients.json`, `fs2.json`, `max1.json`
  carry a 10-key projection with no title key, and `live-states.txt:9-18` records the kept
  fields plus the raw dump's sha256 while stating title/initialTitle/pid were dropped unread.
- **F2 — the projections are exactly the reference shape and lose nothing else.** `project.py`
  runs 9 checks per file (count, element order, key set, key order, per-key value equality with
  the original, no title-family key, no `"title"`/`initialTitle` token, no surviving
  title-family value, trailing-newline/indent shape) plus one seat-wide check: a title-family
  value that is not also a kept `class` value appears nowhere in this seat directory — 6 values
  checked, 0 hits. `crosscheck.py` independently rebuilds the projection with
  `[.[] | {address, mapped, class, floating, size, at, monitor}]` and gets the same bytes, and
  confirms each emitted file re-serialises to itself. All PASS (`proj-verify.txt`).
- **F3 — the two originals differ only in `title`.** Same addresses, classes, geometry, monitor;
  hence both projections are byte-identical (`4f2a8776…`). That is a direct proof that the bytes
  removed are precisely the per-session material and nothing else.
- **F4 — the round-44 wave chose a wider kept set (10 keys incl. the `fullscreen` trio); the
  round-43 reference is 7.** Both are title-free. I did not touch the round-44 files; if the L1
  wants one lane-wide shape it is a separate change.

## 5. Landing (L1)

```
install -m 644 .ufo/waves/round-45/w1/ExecProjectTitles/proj/.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json .ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json
install -m 644 .ufo/waves/round-45/w1/ExecProjectTitles/proj/.ufo/waves/round-43/w2/SentLiveRun/dump-now.json .ufo/waves/round-43/w2/SentLiveRun/dump-now.json
```

Five receipts quote the *old* sha256 and will no longer match the files after landing; they are
hearings of the pre-fix bytes and should stay as they are, not be edited:

- `.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt:112` (`6cdada1a… host-clients-live.json`)
- `.ufo/waves/round-43/w1/ExecLiveHost.md:17`, `:55` (`6cdada1a…` twice)
- `.ufo/waves/round-43/w1-results.json:40` (`6cdada1a…`, quoting raw-key census)
- `.ufo/waves/round-43/w2/SentLiveRun/hashes.txt:1` (`e4b1fb72…  dump-now.json`)

## 6. Risks (not mine to fix)

- **History is untouched.** Replacing the working tree does not unpublish the old blobs: the
  four titles stay readable in git history of a public repo. That is the operator/L1 call
  (`considerthese/2026-10-26.md` carried item on the 190 KB socket table is the same class).
- **Pin-scoped.** The sweep is bound to `0c89478`. Any round-45 seat that writes a new live
  `clients -j` dump is invisible here; re-run `sweep.py` with the new pin at integration.
- **No history rewrite attempted, no `git` mutation of the lane** (lane status shows only
  `.ufo/waves/round-45/w1/` untracked).

## 7. Tooling

Nothing installed. Used: `python3` 3.14.8, `git` 2.56.0, and the `jq` on PATH, which is
**jaq 3.1.1** (jq-compatible) — that matters for the cross-check claim: the second
implementation is a different codebase from the Python emitter and it agrees byte-for-byte.

## 8. Files in this seat

| file | role |
|---|---|
| `proj/.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` | projection (839 B, `4f2a8776…`) |
| `proj/.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` | projection (839 B, `4f2a8776…`) |
| `project.py` | emit + 9 checks per file + the seat-dir hygiene check (reads originals via `git show`) |
| `crosscheck.py` | jaq rebuild, style round-trip, diff-scope check |
| `sweep.py` | pin-wide grep classification, writes `sweep.json` |
| `citecheck.py` | verifies all 12 cited path:line locators and 14 numbers in this report |
| `sweep.json` | every one of the 154 hits with kind and, for dumps, verdict + reason |
| `proj-verify.txt` | full command transcript used for the table above |
