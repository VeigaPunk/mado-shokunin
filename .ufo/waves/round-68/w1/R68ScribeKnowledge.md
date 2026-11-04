# R68ScribeKnowledge — report (round 68, wave 1)

Axes served: C2 operability (sourced-claim grounding for the reader census) and
C1 calibration (lesson-grade record of what the census does and does not
classify). Seat is a scribe: drafts only, nothing integrated, no production file
touched.

## Deliverables

All under `.ufo/waves/round-68/w1/R68ScribeKnowledge/`:

| draft | sha256 | bytes | lines |
|---|---|---|---|
| `draft/corpus/knowledge/gate-git-read-guards-r68.md` | `0f8c5728867243038893017d7ac325cec9166f0fd8e09334c9e899421ceca7f2` | 15042 | 269 |
| `draft/corpus/README-row.txt` | `25a4e52b3e7e116c7051f5c26f230fe32a5a04013dd72dbfafe3fddc8b326e68` | 1147 | 1 |
| `draft/corpus/SOURCES-row.txt` | `cbf4cf5ef05b0ca3381b2a6b5222049607c0ad055a97a463e56ff8b0e1eaac05` | 1068 | 1 |

Knowledge header order is `source:`, `verified-at:`, `recheck:` (lines 1-3).
README row is a 3-cell pipe row whose first cell is
`` `knowledge/gate-git-read-guards-r68.md` ``. SOURCES row is 11 cells
(`awk -F'|' '{print NF-2}'` → `11`), no literal or escaped pipe in any cell
(`grep -c '\\|'` → `0` in both row drafts).

## Source opened and pinned

- URL: `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc`
- Access date: 2026-11-03. Tag `v2.56.0`; host `git --version` → `git version 2.56.0`.
- sha256 `6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2`, 16099 bytes, 470 lines.
- Located quote (L198-199, 14 words): "Objects are presented as-is, without respecting the "replace" mechanism of linkgit:git-replace[1]."
- Other pinned lines used: L6 (NAME), L21-22 (DESCRIPTION), L40/L44/L50/L54-55 (option forms), L295-296 (raw contents), L303-304 (batch name "as if it were fed to ... git-rev-parse"), L379/L392 (missing/ambiguous).

## Next SOURCES id

Round-start census maximum is `S436` (`corpus/SOURCES.md:386`), 373 rows.
`S437` occurs zero times in `corpus/SOURCES.md` (grep -c → 0) and is used once in
the drafted row. Computed next id: **S437**, no collision.

## Findings recorded in the entry

1. The census guard is presence-tested, not key-position-tested:
   `carries_key` (`quality/counters/c2-r68-reader-guard.py:103-109`) accepts any
   `ast.Constant` equal to the key or any keyword of that name anywhere in an
   env-named binding or `env=` value. A value-position constant
   (`env = {"NOTE": "GIT_NO_REPLACE_OBJECTS"}`) would read as guarded.
2. The `env=` branch does not follow a callee: `env=git_env()` is a bare
   `ast.Call`, so only a helper's own env-named binding can satisfy the
   test. A helper that builds `e = dict(os.environ)` then
   `e["GIT_NO_REPLACE_OBJECTS"] = "1"` classifies as unguarded though the
   child would be guarded — under-inclusion symmetric to finding 1.
   Conversely the `env=` value is not followed through a non-env-named
   alias: `unrelated-dict-as-env` (`labels = {...}; env=labels`) is rejected
   because the walk sees a bare `ast.Name`.
3. Reader detection is lexical (`is_reader`, `:84-85`): a comment containing the
   word `git` and a quoted vocabulary verb still marks the blob a reader
   (`comment-only-mention` control expects reader=yes).
4. The name anchor is a case-insensitive substring: `env_named` accepts any
   `ast.Name` id containing `env` (`:100-101`).
5. Population is object-enumerated, `^quality/check-[^/]+\.py$` (`:39`),
   `ls-tree -r --name-only <sha> -- quality` + `show <sha>:<path>`
   (`:138-144`); `quality/counters/*` is outside it.
6. Base state: population 20, readers 13, guarded 1 (`check-tool-ledger.py`,
   subscript-store at `:109`), unguarded 12. The twelve repaired files are named
   in the entry.
7. Before line (`.ufo/waves/round-68/control-baseline-r68.txt:57`, rc 1):
   `population=20 readers=13 guarded=1 unguarded=12 controls=11/11 verdict=TARGET_MISSED`.
   After line is quoted as the frozen predicate
   (`claims-declaration-r68.md:101`, rc 0):
   `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 verdict=TARGET_MET`.
   The seat did not re-run the census; the entry labels the after line as the
   frozen target, not a landing measurement.
8. Control-set sha256 read from the frozen file:
   `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91` (11 cases).
9. No frozen control case isolates the direct `env=` literal shape: the three
   positive controls all reach the guard through an env-named binding, and
   `env=git_env()` itself contributes nothing because the walk does not follow
   calls. Recorded in the entry as a coverage gap; the declaration's control
   count is not changed.

## Commands and exit codes

| command | rc |
|---|---|
| `curl -sSfL -o git-cat-file.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc` (in scratch) | 0 |
| `sha256sum git-cat-file.adoc; wc -c; wc -l` → hashes above | 0 |
| `git cat-file -e 510100c8…:quality/counters/c2-r68-reader-guard.py` | 128 (ABSENT; counter landed pre-freeze at `2ca2bec3`, not in base) |
| `git log -1 --format='%H %ad %s' -- .ufo/waves/round-68/claims-declaration-r68.md` → `e0727cda15621766c35dcf8b70c211b6531aab45 2026-11-03 22:04:51 -0300` | 0 |
| `sha256sum .ufo/waves/round-68/controls/c2-controls.json` | 0 |
| `awk -F'|' '{print NF-2}'` on SOURCES row → 11; README row → 3 | 0 |
| `grep -c '\\|'` on both rows → 0 | 1 (no matches, expected) |
| `grep -c 'S437' corpus/SOURCES.md` → 0 | 1 (no matches, expected) |

No gate, build, test or census was run; no git/jj mutation, stage, commit,
checkout or reset was issued; fixture repos were not needed.

## Limits

- Drafts are unintegrated; the L1 owns insertion into `corpus/README.md` and
  `corpus/SOURCES.md` and the knowledge file's placement.
- The entry's `show`/`ls-tree` role sentences are marked `[INF-docs]`; S437
  documents `cat-file` and delegates naming to `rev-parse`. The replacement rule
  is anchored in the already-mined S436 row (`git-replace.adoc:34`).
- No desktop, compositor, socket, service or session surface was read or written.
- No tool was installed or upgraded this seat.
- Scratch `/fast/scratch/hyaku/mado-r68/R68ScribeKnowledge/` removed before
  yield (`rm -rf`, verified absent). No writes to `/tmp`, `/var/tmp`, the fleet
  root, other lanes, `.ufo/state`, `MANIFEST.json` or `~/.local/bin`.
