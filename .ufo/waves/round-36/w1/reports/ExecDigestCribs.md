# ExecDigestCribs — byte-binding proof, four crib trees × two counters

Seat: `L1Mado36.ExecDigestCribs` (executor). Scratch: `/tmp/mado-r36-digest-cribs/`
(all trees persist there for re-runs). No lane files written except this report.

## Setup

Source crib copied: `LANE/.ufo/waves/round-35/controls-content/c1-fabricated-payload`
(4 corpus files + 8 fabricated 78-byte receipts; its `corpus/SOURCES.md` has **no**
`## Registry` heading — bare table). Counters:

- r35 (in place, committed bytes): `LANE/.ufo/waves/round-35/c1/count.py`
  sha256 `78c2589286a2d70c9b109672c85cd4e9bcb85438bc80ab888d10b73ad12abad6`,
  frozen `LANE/.ufo/waves/round-35/c1/frozen.json`
  sha256 `e18e7aef81e78fc385b3fa9d524a6c875182273517d65d97bb94c463b7743b30`.
- r36 (/tmp copy, as assigned): `/tmp/mado-r36-digest-cribs/c1-idle-lock-r36.py`,
  copied from `LANE/quality/counters/c1-idle-lock.py`;
  copy sha256 `2ee6d0de76dfe756a9bbb03a4f96ae9bd3e48d4dfe37564b46e6e696047f4ce7`,
  lane source re-hashed identical at report time (untracked in `git status`; the
  r36 repair is wave-1 in-flight work). Frozen `LANE/.ufo/waves/round-36/c1/frozen.json`
  sha256 `895a017dac0305eec488d967adec1d93ae0f7e4cedf1ef6f8fa47b0c02cb57a6`.
  Lane HEAD `dbf8b57`; `count.py` absent from `git status --porcelain` (unmodified).

Command shape (verbatim driver `/tmp/run-matrix.sh`):
`python3 -I <counter> --root /tmp/mado-r36-digest-cribs/<tree> --frozen <spec>`

## Mutations applied (per tree)

| tree | change |
|---|---|
| `base-pristine` | none (copy) |
| `a-anchor-real-sha` | S203 receipt bytes appended `ALTERED BYTE APPENDED\n`; S203 anchor cell's declared sha `1b7fa87f…` replaced by the altered bytes' real sha256 |
| `b-real-bytes-wrong-anchor` | all 8 receipts replaced by the lane's real bytes (`LANE/.ufo/waves/round-35/fetch/`); S203 anchor sha changed `1b7f…`→`0b7f…` |
| `c-first-byte-flip` | S203 receipt byte 0 flipped `0x54`→`0x55` (`T`→`U`); length unchanged at 78 B |
| `d-rewritten-identical` | all 8 receipts unlinked and rewritten byte-identical (fresh inodes, e.g. S203 65294449→65294457, content sha `2bb7218e…` unchanged) |
| `b2-anchor-only` | extra: every other clause repaired (real receipts, quotes = line-1 substrings of real bytes, `## Registry` heading prepended), S203 anchor wrong → anchor is the only failing clause under both counters |
| `b3-repair-check` | extra: b2 with correct anchors → accept-side control |
| `c2-digest-only` | extra: c-repairs + real bytes for S204–S210 + real quotes + heading; only S203 byte flipped → digest is the only failing clause under r36 |
| `e-registry-only` | extra: pristine + `## Registry` heading only → r35/r36 counters differ solely by the digest compare |

## Verdicts (verbatim output)

```
tree=base-pristine          r35 exit=0 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
tree=base-pristine          r36 exit=1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
tree=a-anchor-real-sha      r35 exit=1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED
tree=a-anchor-real-sha      r36 exit=1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
tree=b-real-bytes-wrong-anchor r35 exit=1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
tree=b-real-bytes-wrong-anchor r36 exit=1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
tree=c-first-byte-flip      r35 exit=0 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
tree=c-first-byte-flip      r36 exit=1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
tree=d-rewritten-identical  r35 exit=0 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
tree=d-rewritten-identical  r36 exit=1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
tree=b2-anchor-only         r35 exit=1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED
tree=b2-anchor-only         r36 exit=1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED
tree=b3-repair-check        r35 exit=0 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
tree=b3-repair-check        r36 exit=0 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
tree=c2-digest-only         r35 exit=0 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
tree=c2-digest-only         r36 exit=1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED
tree=e-registry-only        r35 exit=0 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
tree=e-registry-only        r36 exit=1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
```

## Item verdicts

- **(a) anchor=real sha, bytes altered — PASS.** r35 MISSED (open_cites=1): the anchor
  clause binds the *declared* sha256, not the file's true hash — an honest anchor is a
  reject under the old counter too. r36 MISSED. Under r35 the S203 leg's sole new failure
  is `anchor-match` (declared sha absent from cs[5]); the quote clause still passes
  (`fabricated attestation for S203` remains in the blob).
- **(b) real bytes, wrong anchor — PASS.** MISSED under both. Literal variant is
  over-determined (S203 fails anchor *and* gate-quote under r35: the entry's fabricated
  quote is not a substring of real bytes). `b2-anchor-only` isolates it: identical
  `open_cites=1` signature under **both** counters with the anchor as the only failing
  clause — the anchor cell is load-bearing in the repaired design.
- **(c) length-preserved first-byte flip — PASS.** r35 MET (still accepts: it computes
  the digest and never compares — D3). r36 MISSED. `c2-digest-only` gives the clean
  single-clause proof: same one-byte flip, all other clauses repaired to passing →
  r35 `TARGET_MET`, r36 `TARGET_MISSED open_cites=1`. The repaired `digest-match`
  clause discriminates one flipped byte.
- **(d) same bytes, fresh file — PASS.** r35 MET, r36 MISSED — identical to
  `base-pristine` under both counters. The counter binds *bytes at the named path*,
  not file identity: rebuilt files (new inodes, nlink=1) classify identically.

## Findings

1. **Over-determination in the frozen crib under r36.** The crib's `SOURCES.md` has no
   `## Registry` section, so r36's `row-in-registry` clause also fails (open_cites=8
   even where only S203 was mutated). The manifest credits `c1-fabricated-payload` to
   `digest-match`; `e-registry-only` shows the heading alone rescues nothing (r36 still
   open=8 — every row parses but all 8 fabricated payloads fail `digest-match`), so the
   attribution is correct though not sole. Wave-2 may want a crib with the heading to
   keep `row-in-registry` out of the digest controls' signal.
2. **Anchor is spec-bound in both counters.** (a) shows an *accurate* anchor cannot
   rescue altered bytes; only the declared sha satisfies `anchor-match`.
3. Accept-side intact: `b3-repair-check` (all repairs, correct anchors) scores
   `TARGET_MET` under **both** counters — the r36 gate can still accept a fully
   consistent tree, so it is not a reject-everything instrument.

## Bounds check

Writes: this report + `/tmp` trees only. Read-only planes untouched; no pacman, no
installs, no model args, no peer messages needed. Lane `git status` unchanged by me.

Report: .ufo/waves/round-36/w1/reports/ExecDigestCribs.md
