# RevFrozenBlobs — round-33 unamended / round-34 frozen-before-data

Scope: blob-identity proof that the frozen counter files under `.ufo/waves/` were never
modified after their freeze commits on `master`.

Refs resolved (2026-10-24):

- Lane tip = `master` = `HEAD` = `fa7ba11346116672352b5d41494141c5c4d738d0`
- R34 freeze `F` = `3420e827bd7b21b1374b23245526554ffd20d096` — `git merge-base --is-ancestor F master` → yes
- R33 freeze `R33F` = `9a46ccf3282117f960b8d53cd71599a91f388ee3`
- R33 tip `R33T` = `69f72100bee31a60b811f8fbbe7796db883e17b3`
- Ancestry: `R33F` → `R33T` → `F` → `master`, all verified via `merge-base --is-ancestor`.

## 1. Blob hashes at r34 freeze `3420e827` vs lane tip `fa7ba113`

| Path | blob @ freeze | blob @ tip | match |
|---|---|---|---|
| `.ufo/waves/round-33/c1/count.py`    | `4ab3db435dd2e396402d1d83039e35082f1138fe` | `4ab3db435dd2e396402d1d83039e35082f1138fe` | YES |
| `.ufo/waves/round-33/c1/frozen.json` | `60d1094baa2992294533bae37e0990ae23077609` | `60d1094baa2992294533bae37e0990ae23077609` | YES |
| `.ufo/waves/round-33/c2/count.py`    | `df563528e725951b447ef31b324ec4b7d264e91b` | `df563528e725951b447ef31b324ec4b7d264e91b` | YES |
| `.ufo/waves/round-34/c1/count.py`    | `49089c186fb75f1bd2cc4c45c0161282ea6e8a46` | `49089c186fb75f1bd2cc4c45c0161282ea6e8a46` | YES |
| `.ufo/waves/round-34/c1/frozen.json` | `0bfe0d866c4e9a2d17da297a11dae389150b488b` | `0bfe0d866c4e9a2d17da297a11dae389150b488b` | YES |
| `.ufo/waves/round-34/c2/count.py`    | `3a499a7eaa6cf5e861a5849992c37f1a7bede962` | `3a499a7eaa6cf5e861a5849992c37f1a7bede962` | YES |
| `.ufo/waves/round-34/c2/frozen.json` | `ef3392b45f638513ff98dda95808f3f3938705e0` | `ef3392b45f638513ff98dda95808f3f3938705e0` | YES |

All seven blobs identical between freeze and tip — no divergence.

## 2. Round-33 `c1` blobs across three refs

| Path | @ R33F `9a46ccf3` | @ R33T `69f72100` | @ tip `fa7ba113` |
|---|---|---|---|
| `.ufo/waves/round-33/c1/count.py`    | `4ab3db435dd2e396402d1d83039e35082f1138fe` | `4ab3db435dd2e396402d1d83039e35082f1138fe` | `4ab3db435dd2e396402d1d83039e35082f1138fe` |
| `.ufo/waves/round-33/c1/frozen.json` | `60d1094baa2992294533bae37e0990ae23077609` | `60d1094baa2992294533bae37e0990ae23077609` | `60d1094baa2992294533bae37e0990ae23077609` |

Identical at all three refs.

## 3. Amendment check — per-path history on `master`

`git log master -- <path>` returns exactly **one** commit for every frozen path:

- round-33 paths: only `9a46ccf3282117f960b8d53cd71599a91f388ee3` (the r33 freeze)
- round-34 paths: only `3420e827bd7b21b1374b23245526554ffd20d096` (the r34 freeze)

No later master commit touched any of the seven paths — they were written once, at freeze
time, and never amended (no write-then-revert is possible with a single-touch history).

Non-ancestor commits (`dbc1f8a`, `520a667`, `735f7e5`, `c42a21f` — subjectless jj
working-copy snapshots) also appear in `git log --all` for these paths, but none is an
ancestor of `master`. The snapshots additionally corroborate ordering: `dbc1f8a` (pre-r33-freeze
snapshot) already held the final r33 blobs and no r34 paths; `735f7e5` (pre-r34-freeze
snapshot) already held the final r34 blobs.

## 4. Frozen-before-data ordering

- Round 33: freeze `9a46ccf3` 20:54:21 precedes data commits `d40b35f9` 21:08:35 and
  `69f72100` 21:29:04 (wave-1 evidence). Counters landed before the data they count.
- Round 34: freeze `3420e827` 21:40:03; the only later master commit `fa7ba113` 21:58:15
  touches `SCORECARD.md`, `corpus/` only — `git diff 3420e827 master -- .ufo/waves/round-34/`
  is empty. No round-34 wave data commit exists after the freeze; counters are still
  pre-data at tip.
- Both freeze commits bundle the counter files with control receipts + fetch bins +
  `registration.md` in a single commit (r33: 27 files; r34: 67 files), matching the
  "freeze C1 and C2 predicates and pre-data control receipts" subjects.

## 5. `git log --format='%H %an %ae %ad %s' --date=iso -6 master` (verbatim)

```
fa7ba11346116672352b5d41494141c5c4d738d0 mado-shokunin mado@shokunin.local 2026-10-24 21:58:15 -0300 round-34: admit the waybar event-socket entry after the frozen counter
3420e827bd7b21b1374b23245526554ffd20d096 mado-shokunin mado@shokunin.local 2026-10-24 21:40:03 -0300 round-34: freeze C1 and C2 predicates and pre-data control receipts
fefdefd4cca6adfd847826f1e406f7aa712007d3 protocol-shokunin protocol@shokunin.local 2026-10-24 21:40:03 -0300 round-33 verifier spot-check (integrator, hyaku): non-author admit/reject
69f72100bee31a60b811f8fbbe7796db883e17b3 mado-shokunin mado@shokunin.local 2026-10-24 21:29:04 -0300 round-33: wave-1 evidence, 32 dispatched, ScribeLesson dead, critic junk tree kept
d40b35f90ad8bf630ad9404d25aeee1d9737f300 mado-shokunin mado@shokunin.local 2026-10-24 21:08:35 -0300 round-33: correct the false r32 C1 row, register the axis gate, and keep the killed coverage counter frozen
9a46ccf3282117f960b8d53cd71599a91f388ee3 mado-shokunin mado@shokunin.local 2026-10-24 20:54:21 -0300 round-33: freeze C1 and C2 predicates and pre-data control receipts
```

## Verdict

PROVEN. Round-33 counters were never amended (single-touch history; blob-identical at
freeze, r33 tip, and lane tip). Round-34 counters were committed in freeze `3420e827`
before any round-34 data landed on `master`, and remain byte-identical at tip.
