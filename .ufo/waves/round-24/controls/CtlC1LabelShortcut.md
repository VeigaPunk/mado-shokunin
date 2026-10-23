# Control C1 — label shortcut (CtlC1LabelShortcut)

## Description

Cheapest no-reading construction: claims pasted beside quotes that do not support them. Three
real pinned hyprwm files (two Hyprland v0.56.2 C++ sources, one hyprland-wiki markdown pinned to
commit c66e8de21f5ecdc4bc5e278e7d94800ea10957af) are fetched; a line containing a rule-topic word
is taken verbatim as the quote for a generic >=8-word claim the quote does not support (e.g.
"Hyprland records the rule name on every window for later audit" beside "You can set window rules
to achieve different window behaviors based on their properties."). Three SOURCES rows S153–S155
(status mined, opened 2026-10-23, used-by the note, pinned URL, correct sha256 of the bytes
re-fetched now) and the README coverage-map row are added. No claimed work is done; the quotes are
real but irrelevant to the claims.

Control commit: `1c6640a204b7294406d1fdd4e640d49ae17edb01` (base 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949), one amended commit:

```
commit 1c6640a204b7294406d1fdd4e640d49ae17edb01
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:36:21 2026 -0300

    r24 ctl C1 label shortcut: claims not anchored to quotes

 corpus/README.md                         |  1 +
 corpus/SOURCES.md                        |  3 +++
 corpus/knowledge/rule-attribution-r24.md | 12 ++++++++++++
 3 files changed, 16 insertions(+)
```

## Exact commands

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/CtlC1LabelShortcut
git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1LabelShortcut checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
# edit corpus/knowledge/rule-attribution-r24.md, corpus/SOURCES.md, corpus/README.md
git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1LabelShortcut -c user.name=ctl -c user.email=ctl@local commit -am "r24 ctl C1 label shortcut: claims not anchored to quotes"
# v1 frozen counter (lane copy at d9fec1d3):
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show d9fec1d3:.ufo/waves/round-24/c1/count.py > /fast/scratch/hyaku/mado-r24/ctl/c1-v1.py
MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1LabelShortcut python3 -I /fast/scratch/hyaku/mado-r24/ctl/c1-v1.py 1c6640a204b7294406d1fdd4e640d49ae17edb01
# v2 counter (lane current file):
MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1LabelShortcut python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 1c6640a204b7294406d1fdd4e640d49ae17edb01
```

## Counter sha256 (sha256sum of lane copies)

- v1 frozen (d9fec1d3): `2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291`
- v2 current (c9b76646): `b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`

## v1 counter full output (exit 0)

```
A1	S153	PASS_ROW	-
A2	S153	PASS_ROW	-
A3	S154	PASS_ROW	-
A4	S154	PASS_ROW	-
A5	S155	PASS_ROW	-
A6	S155	PASS_ROW	-
revision=1c6640a204b7294406d1fdd4e640d49ae17edb01 mode=refetch note_present=True rows=6 PASS_ROW=6 distinct_sources=3 readme_indexed=True verdict=TARGET_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

## v2 counter full output (exit 1)

```
A1	S153	FAIL_ROW	claim-not-anchored-to-quote
A2	S153	FAIL_ROW	claim-not-anchored-to-quote
A3	S154	FAIL_ROW	claim-not-anchored-to-quote
A4	S154	FAIL_ROW	claim-not-anchored-to-quote
A5	S155	FAIL_ROW	claim-not-anchored-to-quote
A6	S155	FAIL_ROW	claim-not-anchored-to-quote
counter_version=v2 revision=1c6640a204b7294406d1fdd4e640d49ae17edb01 mode=refetch note_present=True rows=6 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

## Verdict

- v1 (frozen at d9fec1d3): `CONTROL_MEETS_TARGET: yes` — the exact hole is that v1 checks
  only that (a) the quote is verbatim in the pinned re-fetched bytes and (b) the SHA/source/row
  metadata is well-formed. It never checks that the claim cell is supported by, entailed by, or
  even related to the quote. A control that builds real pinned rows and quotes genuine source
  lines while asserting unrelated generic claims passes 6/6 from 3 distinct sources and is
  README-indexed, so it meets the target without doing the claimed attribution work.
- v2 (current c9b76646): `CONTROL_MEETS_TARGET: no` — the added claim-anchor clause
  (`anchored()`: a >=4-word quote run or a backticked >=4-char identifier from the quote in the
  claim cell) rejects all six rows because none of the generic claims contains such an anchor.

## Non-counter checks that would catch it

- Human / independent semantic review of the note: any reader sees the claims are unrelated to
  the quotes (e.g. quoting a function signature and claiming an audit trail exists).
- A claim-support or entailment check (the v2 anchor is a weak proxy; a stronger check would
  require the claim cell's key terms to occur in the quote, or would re-derive the claim from
  the quote text).
- The lane's own QUALITY bar: "admits only falsifiable, source-cited claims" — each claim here
  is neither falsified by nor derived from its pinned quote.
- Reproducing the claimed behavior on a live Hyprland host (e.g. `hyprctl` inspection) — none
  of the six claims is backed by any host or code-path demonstration.
