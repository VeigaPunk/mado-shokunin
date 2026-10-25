# RevReceiptsBytes — re-derivation of round-34 pre-data receipts

Seat: re-run every counter named by each committed receipt in
`.ufo/waves/round-34/controls/*.txt` (15 files; `c2-*-card.md` are inputs, not
receipts) and compare every numeric field, plus `exit=` and `verdict=`, against
the committed bytes. Receipts and control trees untouched (verified:
`git status --short .ufo/waves/round-34/controls` empty; controls committed at
`3420e82`). Rebuilt hardlink tree lived at `$HOME/.r34-hardlink-check`
(same filesystem as the lane — `/home`, per `df -P`), removed after the run.
No controls or receipts edited.

Counters: `python3 -I .ufo/waves/round-34/c1/count.py --root <root> --frozen
.ufo/waves/round-34/c1/frozen.json`; `c2/count.py --repo . --scorecard <card>
--frozen .ufo/waves/round-34/c2/frozen.json`; r33 crib via
`round-33/c1/count.py --root round-33/scratch/CriticC1Junk --frozen
round-33/c1/frozen.json` — all per `build-controls.py` and `registration.md`.

## Result

**13/15 receipts match a fresh run in every numeric field.** 2 receipts do not.

## Mismatched receipts

| receipt | field | claimed | fresh |
|---|---|---|---|
| `c1-donothing.txt` | exit | 1 | 0 |
| | closed_entries | 0 | 1 |
| | closed_rows | 0 | 2 |
| | open_cites | 2 | 0 |
| | verdict | TARGET_MISSED | TARGET_MET |
| `c2-donothing.txt` | exit | 1 | 0 |
| | published | absent | 169 |
| | mismatch | 1 | 0 |
| | verdict | TARGET_MISSED | TARGET_MET |

(`measured=169` agrees.) Both are the live-lane do-nothing controls; the drift
is post-data landing, not a bad receipt: the lane now contains
`corpus/knowledge/waybar-module-text-route-r25.md` + S201/S202 registry rows
(`corpus/SOURCES.md:203-204`), and `SCORECARD.md:2108` publishes
`r34-s189-line: line=169`. A do-nothing receipt is expected to go stale once
data lands; the receipt correctly records the pre-data state.

## Matching receipts

| receipt | fresh run |
|---|---|
| `c1-golden.txt` | exit=0, closed_entries=1 closed_rows=2 open_cites=0, TARGET_MET |
| `c1-entries-only.txt` | exit=1, 0/0/2, TARGET_MISSED |
| `c1-rows-only.txt` | exit=1, 0/0/2, TARGET_MISSED |
| `c1-symlink-crib.txt` | exit=1, 0/0/2, TARGET_MISSED |
| `c1-symlink-entry.txt` | exit=1, 0/0/2, TARGET_MISSED |
| `c1-symlink-parent.txt` | exit=1, 0/0/2, TARGET_MISSED (root `controls/extra/symlink-parent`; `fetch/` is a symlinked parent dir) |
| `c1-symlink-sources.txt` | exit=1, 0/0/2, TARGET_MISSED (root `controls/extra/symlink-sources`; `corpus/SOURCES.md` → `held-sources.md`) |
| `c1-used-by-prefix.txt` | exit=1, 0/0/2, TARGET_MISSED (root `controls/extra/used-by-prefix`; used-by token `…r25.md.evil` rejected as whole token) |
| `c1-hardlink.txt` | exit=1, 0/0/2, TARGET_MISSED, nlink=2 (rebuilt tree: dest `S201.bin` st_nlink=2 at count time; counter rejects nlink≠1) |
| `c2-junk.txt` | exit=1, published=128 measured=169 mismatch=1, TARGET_MISSED |
| `c2-reachable.txt` | exit=0, published=169 measured=169 mismatch=0, TARGET_MET |
| `r33-counter-on-its-crib.txt` | exit=0, PRED-C1-r33-v1 2/4/0 TARGET_MET, `nlink_note` constant matches |
| `indented-guard.txt` | `spaced=S197 column_zero='' collisions='S197'` identical; staged `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` (128826 B, mtime 2026-10-24 21:17) still contains a `| S197 |` row |

## Notes

- Fixture trees are byte-stable (all `controls/**` blobs are regular files,
  nlink=1, committed at 21:54); symlink controls re-checked with `find -type l`
  — all 5 symlinks intact and pointing at the held blobs.
- The three `extra/*` controls have no builder case in `build-controls.py`;
  roots were inferred from receipt naming (`c1-<shape>` → `controls/extra/<shape>`)
  and confirmed by identical fresh output.
