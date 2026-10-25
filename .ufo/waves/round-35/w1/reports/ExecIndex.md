# ExecIndex — index-gate read at tip + README requirement for the three C1 entries

Seat: ExecIndex (wave w1, round 35, mado). Read-only; no repo mutation.
Repo tip used for `--rev`: `19e4ab3171c1540c40d6b12097745af98053b07d`
(`round-35: freeze C1 and C2 predicates, the clause ledger, the control receipts and the re-issued blob ledger`).

## Gate output at tip

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-index.py \
  --rev 19e4ab3171c1540c40d6b12097745af98053b07d \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin
```

Output:

```
MADO_INDEX: rev=19e4ab3171c1540c40d6b12097745af98053b07d indexed=47/47 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
```

Exit code: **0**

## Selftest output

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-index.py --selftest
```

Output:

```
MADO_INDEX_SELFTEST: 12/12 assertions passed
```

Exit code: **0**

## What the three new knowledge entries require in `corpus/README.md`

The three round-35 C1 entries (currently present only in the golden control fixture at
`.ufo/waves/round-35/controls/golden/corpus/knowledge/`; not yet in `corpus/knowledge/`
at tip — `git ls-tree HEAD corpus/knowledge/` shows only the pre-existing
`idle-lock-plane.md` and `idle-lock-route-r17.md` idle notes):

- `corpus/knowledge/idle-lock-never-asked-r12.md` (sources S203, S204)
- `corpus/knowledge/idle-lock-chain-armed-r14.md` (source S205)
- `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` (sources S206–S210)

Gate contract (`quality/check-index.py`): the gate enumerates
`corpus/knowledge/*.md` in the scored tree/revision and matches them against
`corpus/README.md` rows matching `^\| \`knowledge/([^`]+\.md)\``. It passes iff
`missing=0 dangling=0 duplicates=0` — i.e. each new regular `.md` file needs
**exactly one** index row whose backticked path names it; no other README section is
checked.

To keep the index complete when the three entries land:

1. **Exactly one table row per file** in the `| Note | Holds | Sources |` table
   (rows start at `corpus/README.md:12`; last row at tip is line 58,
   `waybar-module-text-route-r25.md`). Row form, per existing convention:
   `| \`knowledge/<name>.md\` (id, round 35) | <Holds cell> | <Sources cell> |`.
   Note-cell conventions to keep: `source:` S-ids in [SOURCES](SOURCES.md),
   receipt `.ufo/waves/round-35/fetch/<S…>.receipt.txt` (round-35 uses
   `.receipt.txt`, not round-34's `.bin`), `recheck` token.
2. **No duplicates, no dangling rows**: a row for a path absent from
   `corpus/knowledge/` in the same commit is `dangling`; two rows for one path is
   `duplicates`. Rows and files must land in the same commit — a split commit fails
   the gate at every intermediate tip.
3. **Entry files must be regular files** (the selftest's symlink control exists in
   `controls/c1-entry-symlink`; the same "regular member" check `REFUSED` path
   applies to README-adjacent anomalies in the gate's loader).
4. Optional but conventional: a `## Frontier` bullet describing the new idle-lock
   control-surface coverage (sibling of the "### Round-25 bind-table route" style
   sections after line 58's table). Not gate-checked; completeness under
   corpus README conventions only.

After landing, re-run the tip command above; expected result `indexed=50/50
missing=0 dangling=0 duplicates=0`, exit 0.
