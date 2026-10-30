# R56W3MutKillC2 — C2 killer fixtures

## Attacked and result

Attacked the survivor mutants and proposed killer fixtures from wave-2 ToolA/ToolB against **0f3a54361a9824484d0801679ceb1fd8ac7c32e1**, not the working tree. Axes: discrimination, honest-tool fidelity, portability, restoration, frozen-contract preservation.

- Rebuilt 78 mutation IDs: A's 34 non-equivalent claim survivors + 9 argued equivalents; B's 25 non-equivalent survivors + 10 argued equivalents. Some IDs duplicate semantic changes across reports; these are not 78 independent defects.
- All scored **18/18 committed + 8/8 holdout** under the harness's `score()`. Fifteen additionally fail the tool's informational selftest; selftest is explicitly outside the frozen C2 predicate.
- **57/59 non-equivalent mutation IDs killed by staged fixtures.** Final same-detector runs: pristine passes, mutant fails, restored passes, for every one of those 57.
- Remaining **Bm75/Bm76 killed by a separate root-level bwrap probe**, not by the frozen fixture contract. They cannot be expressed by its staging layout; this limitation is not hidden or changed.
- The 19 w2-argued equivalent IDs had no kill in the bounded cross-matrix. No general equivalence proof is claimed.
- Delivered **52 distinct fixture directories** from 63 candidate specifications after deduplication. All **52/52 pass the honest tip tool through the harness's own staged `score()`**. Eight proposals kill no tested mutant; the table identifies them. In particular A-K80 misses M80, which A-K27 kills instead.

The frozen predicate remains unchanged and passes on pristine bytes. These are proposed fixtures outside the committed fixture set, not a new registered predicate.

## Commands and decisive output

Scratch root was `/fast/scratch/hyaku/mado-r56/R56W3MutKillC2`. Archived tip content was committed only in scratch as `1736e73d9788497202eca72771c7136eed48e46d`; hence that different `rev=` below.

```text
python3 -I <scratch>/repo/quality/check-r56-controls.py --claim c2 \
  --repo <scratch>/repo --rev 1736e73d9788497202eca72771c7136eed48e46d --work <scratch>/work
MADO_R56_C2: rev=1736e73d9788497202eca72771c7136eed48e46d fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET
exit=0
```

Thus all 26 frozen fixtures pass the unmutated tool. Committed fixture commitment remained `a9f552511cc4939e3c83190e7ca55a09d5f01dd520c59b3a6feeba2e0c4647d6`; holdout commitment remained `65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183`.

The harness-native cross-matrix ran 4,914 comparisons: 63 proposals × 78 mutation IDs. Final restoration probes, with exact stdout/rc/hashes retained, returned:

```text
staged final probes 57 killed 57
root probes [('Bm75', True), ('Bm76', True)]
52 fixtures delivered; frozen-harness score on pristine: 52/52
```

Example: `misc:disable_autoreload = on$x` in `a-k27` gives pristine `unsupported=1 autoreload=on`; AM27/AM80 instead accept it and give `unsupported=0 autoreload=off`. Both rc=0; stdout mismatch kills them. `a-k100` gives pristine `SETUP bad_json`, rc=2; AM100 skips the comment and returns normal UNKNOWN output, rc=0.

## Defects and repairs

**Weakens proposal reproducibility:** the filesystem-delivered B `m08/K03/tree/conf.d` presently contains only U+0100.conf, missing the raw 0x80.conf named in its spec. Both the old tool and tip tool produce `paths=2` from that delivered tree, while its expected.out says `paths=3`. Cause and timing are unknown; this does not disprove the earlier author's historical run. Rebuilt `b-k03` contains both names. Its expected output uses the tip's `\x80` escaping, introduced after the w2 revision.

**Weakens proposal readiness:** A-K55/A-K57 print absolute staging paths in their pristine outputs. Two staging locations produced different bytes, so their expectations were not reusable. Repaired here using symlinked display roots; both repaired fixtures produce stable `$ROOT` output and kill their intended mutants. Details in `defects.md` and fixture notes.

**Weakens staged coverage:** Bm75/Bm76 require filesystem-root paths; no frozen-layout fixture can provide them. Root-only probe output is separately labelled in the receipt. This is a routed coverage limit, not permission to widen the frozen predicate.

**Correction:** K100 was present in ToolA's `extra.py:8-11`, with historical receipts. Earlier exploratory drafts inspected only `kill2.py` and incorrectly alleged it was missing/unverified. That allegation is withdrawn. Delivered a-k100 is a simplified comment-only version of that proposal.

## Evidence and deliverables

All paths below are lane-relative:

- `.ufo/waves/round-56/w3/R56W3MutKillC2/fixtures/` — 52 directories with `args.json`, `tree/`, `expected.out`, `expected.rc`, plus notes.
- `…/kill-table.md`, `table.json`, `matrix.json` — survivor → fixture → kill mappings, aliases and explicit no-kills.
- `…/receipts/kill-c2.txt` — authoritative commands/results, limits and corrections.
- `…/receipts/final-probes.json` — exact pristine/mutated/restored stdout, rc and SHA256 for all 57 staged and both root-only probes.
- `…/receipts/kill-*.txt` — earlier per-fixture transcripts; final-probes.json is authoritative for final restoration.
- `…/mutants_a.json`, `mutants_b.json` — reconstruction anchors/replacements from the w2 drivers.
- `…/defects.md`, `manifest.json` — detailed findings and artifact hashes.

## Restoration, limits and tooling

Original and restored tool SHA256: `3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7`. Each final probe restored exact pristine bytes in `finally`; no lane tracked file was mutated. Scratch was removed after preserving receipts.

No installs or updates. Used existing Python 3.14.8 and bubblewrap 0.13.1. No compositor or host configuration changes.

An optional equivalence experiment printed zero differences but was invalid: its arguments retained literal `{FX}` and its generated dump paths were reused after deletion. Its purported 502-case equivalence evidence is **withdrawn**, not shipped or credited. Equivalence remains the w2 arguments plus bounded no-kill observations in the actual matrix. No Hyprland/glibc correctness comparison was run. No proof that this candidate set is minimal or exhaustive.
