# R54Seat20 — C1 frozen-literal counter reachability

**Axis:** C1 operability — whether the frozen controls distinguish a source-truth verifier from a counter that merely recognizes frozen record literals.

## Finding — control-shaped table-diff reaches TARGET_MET without checking source bytes

**Concrete attack:** a counter reads the scored revision's P19–P22 entry rows and `SHA256SUMS`, compares those records to embedded frozen literals, and runs the six controls by applying their specified mutations to those parsed records. It never reads any of the four pin blobs, hashes a pin, or searches a pin for a quote. Nevertheless, it prints the exact frozen `TARGET_MET` line on the honest tree and rejects all six required mutated-tree inputs. The frozen controls specify verdicts, not that the counter establish the quote/hash/anchor claims from their source bytes. This is distinct from Seat18's pin-plus-updated-manifest attack: my counter never hashes pins and rejects Seat18's changed-manifest input; the independent counterexample here changes a pin while leaving the frozen manifest untouched.

The literal comparison implements registration.md's instruction to compare P19–P22 table rows byte-for-byte (lines 20–23); the table and side-claim expectations are at lines 25–34. The six required controls and expected verdicts are registration.md:40–47. The frozen predicate separately requires the quotes in pins and pin bytes hashing to round-52 recorded digests (claims-frozen.md:21–30), but those source-byte facts are not distinguished by the frozen controls. The do-nothing explanation at claims-frozen.md:41–43 only rules out an always-print counter; it does not rule out this record-literal counter.

## Executed scratch reproduction

Used an isolated `mktemp -d -p /fast/scratch/hyaku/mado-r54/R54Seat20 fixture-XXXX` local clone, checked `git rev-parse --show-toplevel` against that fixture path before commits, detached it at base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`, then staged the two scratch-only counters and committed them in the fixture. No lane/source repo changes were made.

The counter's source is reproducible from the following rule: use `git show <rev>:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` to parse the four P19–P22 rows; compare each pin:anchor and quote cell to the frozen table in registration.md; use `git show <rev>:.ufo/waves/round-52/fetch/SHA256SUMS` and compare its four recorded digests to the four frozen literals; count the six controls as rejected if each specified record mutation makes one literal check fail. Do **not** invoke git show on any pin file. This produced a counter at `quality/counters/c1-r54-errata-truth.py` in the scratch fixture; the separate naive always-print counter was `quality/counters/donothing-c1.py`.

Commands executed in the scratch fixture:

```sh
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev c2e86cc358ecc527ef06c7427962aa9665a3e027
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev 3d4a4b698256e7eda2f5f8a8566a272fb51634fe
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev c16e33e2fb1c583ae7e9d7cae4d463c0eb08333d
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev 3ad38f655692952fd0a786109752c70384524dec
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev 567c44a025e5399c4aa4a0ff52b135d3bdfca92b
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev 99bd7f8c56ec6ecbc194f2a812a4c347b7776150
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev 764e45aa7063729325dbeb66adead8ffbd986d11
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev 6b94cf9b8b50bef6e42fbd750100903c1790c38a
```

Actual result summary (all outputs were the frozen `MADO_ERRATA_TRUTH:` line; listed exit codes):

```text
honest M       exit=0  propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
CTL1 splice    exit=1  propositions=4/4 quotes=3/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
CTL2 anchor    exit=1  propositions=4/4 quotes=4/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
CTL3 SUMS nibble exit=1 propositions=4/4 quotes=4/4 anchors=4/4 pins=3/4 controls=6/6 verdict=TARGET_MISSED
CTL4 range     exit=1  propositions=4/4 quotes=4/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
CTL5 drop P22  exit=1  propositions=3/4 quotes=3/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
CTL6 swap pin  exit=1  propositions=4/4 quotes=4/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
CTLX pin byte changed, SUMS untouched
               exit=0  propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
```

CTLX is the distinguishing input: flip the first byte of `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`, leave `SHA256SUMS` unchanged, commit that fixture tree, and run the counter at that revision. The frozen P19 quote remains present under registration.md:51's verbatim normalization, but the pin digest is now `0987f7bb7a6270eba8fad64fc7578da1b26f1730f9d1a94edb0dc1887b2855fb`, not the frozen `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`; the manifest bytes equal the honest tree. Thus clause (c) is false while the counter exits 0 and prints TARGET_MET.

The literal always-print control was also executed: it prints `TARGET_MET` on both honest M and CTL1 (exit 0), so it fails the required CTL1 rejection. This confirms the written do-nothing control catches the naive case, but not the table-diff counter above.

## Distinctness and residual risk

Seat18's report attacks a counter that hashes pin bytes against a mutable in-tree manifest using a pin edit plus a matching manifest edit. This report attacks a different counter class (no pin reads or hash computation) with a pin-only edit; my counter rejects the matching-manifest mutation because the manifest differs from its frozen literal. Seat24 reports the candidate counter absent at its inspection point and has no executed mutant; Seat25's selected duplicate-proposition-ID input is distinct. This reproduction uses a constructed counter, not the not-yet-present lane implementation, so it establishes a registration/control-battery gameability, not that a landed counter actually has this defect.

Additional freeze drift: registration.md:18 says hashes are in `SHA256SUMS.txt`, but the committed round-52 fetch path is `SHA256SUMS` (no `.txt`). This is independently visible via `git ls-tree` at the pinned base. Seat14 also noted this filename mismatch.

**Verification limits:** LSP device/server was not available in this assignment environment; no LSP status, references, definition, or diagnostics could be queried. No tool installed/updated. Scratch fixture and scripts were removed before report completion.

**Report trailer:** `.ufo/waves/round-54/w1/R54Seat20.md` relative to lane root. No tracked lane changes, git/jj mutations, host reads, producer execution, or tool updates.