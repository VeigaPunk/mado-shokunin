# CriticC1Junk — false-positive attack on PRED-C1-r33-v1

**Verdict: the claim dies.** A junk tree containing zero mined, fetched, or
verified bytes prints `TARGET_MET` (exit 0) under the frozen counter and the
lane's own `frozen.json`.

## Run 1 — junk tree, real frozen spec

```
$ python3 .ufo/waves/round-33/c1/count.py \
    --root .ufo/waves/round-33/scratch/CriticC1Junk \
    --frozen .ufo/waves/round-33/c1/frozen.json
PRED-C1-r33-v1 closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET
exit=0
```

## Tree contents (3 files + 4 symlinks, ~700 authored bytes)

- `corpus/knowledge/waybar-module-text-route-r25.md` — `JUNK ENTRY` banner plus
  two `gate-quote:` lines whose payloads are **copied verbatim out of
  `frozen.json`'s `quotes` map** — no fetch was ever opened to mine them.
- `corpus/knowledge/event-delivery-limits-r26.md` — same, for S197/S189.
- `corpus/SOURCES.md` — four self-authored registry rows; `used_by` is whatever
  the attacker writes in the last `|` field. Nothing upstream validates them.
- `.ufo/waves/round-33/fetch/{S190,S191,S197}.bin` and
  `.ufo/waves/round-32/fetch/S189.bin` — **absolute symlinks into the lane's
  real fetch dirs**. `Path.read_bytes()` follows them, so the sha256 conjunct
  passes on bytes the tree does not own.

## Why it passes — the `ok` conjuncts are all shape, no provenance

| Conjunct | How junk satisfies it without the claimed work |
|---|---|
| `found == quote` | quote copied from `frozen.json` itself — the spec is a crib |
| `1 <= words <= 25` | same copied string (6–8 words each) |
| `quote.encode() in blob` | blob is the real file, reached by symlink |
| `digest == sha256` | digest verifies the *linked* bytes, not tree provenance |
| `row_for` + `entry_rel in used_by(row)` | attacker writes both sides of the join |

The counter proves **closure-shape** (the right strings sit at the right paths,
resolvable blobs hash right), not that quotes were mined, hashes verified, or
rows earned. Note the boundary: a purely fake blob still fails — the
hash-mismatch control scored `closed_entries=1 … TARGET_MISSED`. The
exploitation is that "the right bytes reachable at that path" ≠ "bytes this
tree fetched."

## Run 2 — second frontier: doctored spec, empty root

`--frozen` takes any path. Keeping `predicate` verbatim passes the
`predicate-drift` guard even with `entries` gutted:

```
$ python3 .ufo/waves/round-33/c1/count.py \
    --root .ufo/waves/round-33/scratch/CriticC1Junk/empty \
    --frozen .ufo/waves/round-33/scratch/CriticC1Junk/doctored-frozen.json
PRED-C1-r33-v1 closed_entries=0 closed_rows=0 open_cites=0 verdict=TARGET_MET
exit=0
```

`frozen.json` with `entries={}` and `target={0,0,0}` on an empty root meets
target. The drift check pins the predicate *sentence*; it does not pin the spec
*data*. Caller-side fix: digest-pin `frozen.json` (or embed spec in the
counter). Cheapest single hardening for the tree-side attack in Run 1: resolve
fetch paths and reject anything outside `--root` (`resolve()` + `is_relative_to`),
which forces the blobs to be real tree bytes — though provenance-vs-symlink
to a *sibling controlled* tree stays open as long as blobs are addressable
outside the measured root.

## Files

- Tree: `.ufo/waves/round-33/scratch/CriticC1Junk/` (kept as evidence)
- Doctored spec: `.ufo/waves/round-33/scratch/CriticC1Junk/doctored-frozen.json`
- Counter + spec untouched; lane corpus untouched.
