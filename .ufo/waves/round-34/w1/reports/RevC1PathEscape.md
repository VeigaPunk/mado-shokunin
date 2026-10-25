# RevC1PathEscape — path-walk attack on c1/count.py

Target: `.ufo/waves/round-34/c1/count.py` (`read_regular`, lines 40–85). Frozen spec:
`.ufo/waves/round-34/c1/frozen.json`. Trees under
`.ufo/waves/round-34/scratch/RevC1PathEscape/`. Committed counter unmodified.

Command for every tree:

    python3 .ufo/waves/round-34/c1/count.py --root <tree> --frozen .ufo/waves/round-34/c1/frozen.json

## Baseline (controls/golden)

```
PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
exit=0
```

## (a) tree-a-symlink-sources — corpus/SOURCES.md → real registry outside tree

`corpus/SOURCES.md` is a symlink to the lane's real `mado-shokunin/corpus/SOURCES.md`
(164 674 bytes, dozens of rows). If followed, the registry would satisfy the used-by
check trivially.

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
exit=1
```

**Refused.** `lstat` on the final component sees `S_ISLNK` → `read_regular` returns
`None` → `sources=""` → `rows_for` finds zero rows → both cites open.

## (b) tree-b-symlink-knowledge — corpus/knowledge/ → dir outside tree

`corpus/knowledge` is a symlink to `scratch/RevC1PathEscape/outside/knowledge/`,
which contains a *byte-identical* copy of the real entry file — so refusal is about
the link, not missing content.

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
exit=1
```

**Refused.** Intermediate-component `lstat` at `corpus/knowledge` sees `S_ISLNK`
→ entry unread → `entry_bytes is None` → both cites open.

## (c) used-by cell escape — no filesystem reach possible

Two sub-trees, each with S201's used-by token mutated (S202 left clean as control):

- `tree-c1-usedby-dotdot`: `corpus/../corpus/knowledge/waybar-module-text-route-r25.md`
- `tree-c2-usedby-abs`: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/waybar-module-text-route-r25.md`

Both:

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
exit=1
```

**Refused** — but not by path resolution. `used_by_tokens()` returns raw strings and
`main` compares `tokens == {entry_rel}` (line 157) where `entry_rel` is the frozen
key `corpus/knowledge/waybar-module-text-route-r25.md`. `..` and absolute tokens are
string-unequal → S201 open, S202 closed (1/1). The used-by cell is **never used as a
path**: only `spec["entries"]` keys and `spec["fetches"][sid]["path"]` reach
`read_regular`, and those come from the frozen spec, not the tree.

## Additional walk observations

- `read_regular` rejects `rel` starting with `/` or `\` and any component in
  `{"", ".", ".."}`. `Path("a//b").parts` normalizes `//` → `("a","b")`, but the
  frozen spec controls `rel`, so normalization only helps the attacker, never hurts.
- The walk is a re-`lstat` per component followed by `os.open(O_NOFOLLOW)` on the
  final path — a TOCTOU window exists between the last intermediate `lstat` and
  `open` (a racing writer could swap `corpus/knowledge` for a symlink), but it is
  not exercisable from static tree construction.
- `st.st_nlink != 1` on the leaf also rejects hardlinked registry/fetch files
  (consistent with `controls/c1-hardlink.txt`).

## Verdict

All three escape shapes refused, `exit=1`, `verdict=TARGET_MISSED`. The path walk
holds: symlinked leaves, symlinked intermediate components, and lexical escapes in
registry cells cannot reach outside `--root`.
