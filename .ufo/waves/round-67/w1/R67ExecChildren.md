# R67ExecChildren — C2 replacement-ref guards (drafts + control probes)

Seat: R67ExecChildren (executor, w1). Axes: calibration (C1) untouched; operability (C2) replacement-ref
residual. Frozen claims/controls unchanged; no production file, lane git state or fleet file was written.
L1 steering honoured: the **bound R control is the citecheck child** (planted refs/replace on the root TREE);
used-by and ledger guards are delivered as **defense-in-depth** with their own probes, since both were
cheaply fixtureable on this host.

## Files (drafts only, L1 integrates)

| draft | intended production path | base sha256 | draft sha256 | intended diff |
|---|---|---|---|---|
| `draft/quality/counters/c3-r56-used-by.py` | `quality/counters/c3-r56-used-by.py` | `68b34e3c7c1d61e7f5f3da36a0f8ab36ebe3c54b1b756cb18c740e0aa7c1635b` | `f54423eb8ab24eeb5a8cd51f2d38408fe02054797ba841c3940cde28d3903b3f` | +1 line in `git_env()`: `"GIT_NO_REPLACE_OBJECTS": "1",` |
| `draft/quality/check-tool-ledger.py` | `quality/check-tool-ledger.py` | `b65042e82b30f162909695f2f2560b13a8cb690a5dbfe0c116857bc4fb339991` | `1c96c4cfd69ad97fbfc9174c9fe4d27b1d157df69cbcbc2451067f1374febdfb` | +1 line in `git_env()`: `env["GIT_NO_REPLACE_OBJECTS"] = "1"` |
| `draft/tools/mado-receipt-citecheck.py` | `tools/mado-receipt-citecheck.py` | `414ca759232a3d31451f86060f4b0ba3382dd151f4bffe797793cb2ced5cee11` | `3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0` | +1 line on the `ls-tree` child: `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),` |

Diff audit: each draft differs from base at exactly one added line (unified diff captured during the run);
`GIT_NO_REPLACE_OBJECTS` occurs exactly **1** time in each file, so M-R can delete exactly one occurrence.
Base revisions extracted from `0b28ffb4baac9586566d246c3f0986b2bb650a33` with `git show`; production
files were not modified (`git -C lane status` shows only this seat dir untracked).

## Bound control (L1 steering): citecheck + root-TREE replacement

Fixture recipe (all in scratch; `git init`, toplevel asserted before first commit):

```
D=$(mktemp -d "$S/fixture.cite.XXXX"); git -C "$D" init -q
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
# real tree LACKS the cited file
artifacts/cite.txt = "cites corpus/present-r67.md and corpus/real-r67.md"
corpus/real-r67.md present; git add -A; commit "real-tree-lacks-cited-file"
C=$(git rev-parse HEAD); T=$(git rev-parse C^{tree})
# forged tree ADDS the cited file, without touching C
write corpus/present-r67.md; git add; TF=$(git write-tree); git rm --cached corpus/present-r67.md
git update-ref refs/replace/$T $TF
```

- Real listing (guard forced only for the probe): `corpus/present-r67.md` absent.
- Forged listing (no guard): `corpus/present-r67.md` present.
- Base child (`git show 0b28ffb4:tools/mado-receipt-citecheck.py` → scratch), scrubbed env
  `env -i PATH=/usr/bin:/bin HOME=$S/home`: **rc 0**,
  `MADO_CITECHECK: rev=7b537eec... files=1 citations=2 resolved=2 missing=0 skipped_large=0 verdict=TARGET_MET`.
- Draft child, same scrubbed env: **rc 1**,
  `... citations=2 resolved=1 missing=1 ... verdict=TARGET_MISSED`, `CITECHECK MISSING: corpus/present-r67.md`.
- Fixture commits: real `7b537eec4618668810e90dedf1c86b89a997b3c1`, T_real
  `1c47f203e9e14c67ce6851e45859a3969ce9cdf7`, T_forged `2e01a7eee1353cf2eb47ea5505484af48e55b9b9`.

## Defense-in-depth 1: used-by counter (blob replacement)

The counter reads the frozen tables at `.ufo/waves/round-56/frozen-tables-v2.json` (sha256 fixed) whose
`c3.base_rev` is `13f0acbe3a15da2d9c08357a576d91dcadc85273`, so the fixture carries that commit's objects
(commit + root/corpus/knowledge trees + SOURCES + 78 entry blobs, 496 objects, 664 224-byte pack via
`git pack-objects --stdout` + `git index-pack --stdin`; fixture-only, lane objects read-only). Clean tree
extracted at `0b28ffb4` for `corpus/SOURCES.md`, `corpus/knowledge/`, the frozen tables and
`.ufo/waves/round-56/c3-name-only.tsv`.

- Clean fixture commit `9fc8bac5cc446f3bffee1fbcfce3dc328c9e9e53`:
  draft child **rc 0** `entries=78 rows=372 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0
  exempt=24 verdict=TARGET_MET missed=none` (base child identical).
- Real defect `bb767f16bf114983b526beb0c8f8d82e529454a2`: row `S001` used-by gains
  `corpus/knowledge/ghost-r67.md`. Draft child **rc 1**
  `... extra=1 ... verdict=TARGET_MISSED missed=extra`.
- Planted `refs/replace/<defect SOURCES blob 94fefec06875f2d863a1b9ebcfd85d4fc9bd4c0e>` →
  `<clean blob faa3a1b36b5208e54d0d999ed7d7383ba88ded7e>`.
  Base child (scrubbed env) **rc 0** `... verdict=TARGET_MET missed=none` (forged read confirmed);
  draft child **rc 1** `... extra=1 ... verdict=TARGET_MISSED missed=extra` (real read).
- Lane regression sanity, `--rev 0b28ffb4`: draft **rc 0** `MADO_USED_BY: ... entries=78 rows=372
  missing=0 ... verdict=TARGET_MET` — identical to the pre-edit child.

## Defense-in-depth 2: tool-ledger gate (tree replacement)

Fixture: `tools/alpha.py` population=1; real `quality/tool-ledger.md` has zero rows; replacement root TREE
swaps in a ledger with one valid row (pointer `quality/README.md` names `alpha.py`).

- Real state `23ad0e8755827f2979977cb729ff3fd714a2e79a`: draft **rc 1**
  `LEDGER-ROW reason=uncovered path=tools/alpha.py detail=no-row`;
  `LEDGER: population=1 ledger_rows=0 uncovered=1 ... verdict=TARGET_MISSED`.
- Forged tree `5ee3273d7326921c2fd202e5fa498df7a6f5b0d1` under
  `refs/replace/549d029e7c611b43ed5084741ac2f58bc3e476e6`: base child (scrubbed env) **rc 0**
  `LEDGER: population=1 ledger_rows=1 uncovered=0 ... verdict=TARGET_MET`; draft child **rc 1**
  `population=1 verdict=TARGET_MISSED ledger=absent` (real object tree: the real ledger is the zero-row
  blob and the real state still has it; the guarded read refuses the forged tree).
- Lane regression sanity, `--rev 0b28ffb4`: draft **rc 0**
  `LEDGER: population=108 ledger_rows=108 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET`.

## Selftests (scrubbed env, scratch under the seat scratch root)

| instrument | command | rc | marker |
|---|---|---|---|
| ledger draft | `python3 -I <draft>/quality/check-tool-ledger.py --selftest --scratch-root $S/st-ledger` | 0 | `LEDGER_SELFTEST: 54/54 passed` |
| citecheck draft | `python3 -I <draft>/tools/mado-receipt-citecheck.py --selftest --scratch-root $S/st-cite` | 0 | `MADO_CITECHECK_SELFTEST: 12/12 assertions passed` |
| used-by draft (extra) | `python3 -I <draft>/quality/counters/c3-r56-used-by.py --selftest --repo <lane> --rev 0b28ffb4 --work $S/st-usedby` | 0 | `MADO_USED_BY_SELFTEST: 16/16 assertions passed` |

## Notes / risks

- The frozen C2 control set is untouched; this seat supplies the exact one-line guards the M-R mutation
  deletes (`GIT_NO_REPLACE_OBJECTS`, one occurrence per file). It does not re-scope C1 or C2.
- The citecheck guard adds the key onto the inherited environment (as assigned); no other environment
  handling changed. The proof runs used `env -i PATH=/usr/bin:/bin HOME=$S/home` with no `GIT_*` ambient,
  so the child's own guard is the only defense (per L1).
- The used-by fixture needs the r56 base commit objects because the frozen tables embed `base_rev`; that is
  fixture-only, read-only w.r.t. the lane. Its guard is defense-in-depth, not the bound C2 control.
- No tool installs, no package-manager transactions (pacman pause respected), no commits/stages/checkouts in
  the lane, no writes to fleet root, sibling lanes, `.ufo/state` or scratch outside
  `/fast/scratch/hyaku/mado-r67/R67ExecChildren/`.
- Scratch was deleted before yield (`rm -rf -- "$S"`, then existence check rc nonzero); no fixture path or
  temporary object remains.

Report path: `.ufo/waves/round-67/w1/R67ExecChildren.md`.
