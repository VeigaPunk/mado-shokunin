# Control CtlC1OffTopic — C1 off-topic real pinned rows (round 24, pre-data)

## Control description

One commit (base `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`) adding:

- 8 new SOURCES rows `S900`–`S907`, all opened `2026-10-23`, status `mined`, used-by
  `corpus/knowledge/rule-attribution-r24.md`:
  - `S900` Hyprland v0.56.2 `AGENTS.md` (raw.githubusercontent.com, tag v0.56.2)
  - `S901` Hyprland v0.56.2 `CODE_OF_CONDUCT.md`
  - `S902` Hyprland v0.56.2 `hyprctl/hyprctl.usage`
  - `S903` Hyprland v0.56.2 `README.md`
  - `S904` Hyprland v0.56.2 `example/hyprland.lua`
  - `S905` Hyprland v0.56.2 `LICENSE`
  - `S906` kitty v0.49.2 `docs/conf.rst` (r23 row S123 bytes re-registered; NOT under /hyprwm/)
  - `S907` foot 1.28.0 `README.md` (r23 row S143 bytes re-registered; codeberg, NOT under /hyprwm/)
- `corpus/knowledge/rule-attribution-r24.md` with 8 claim rows `A1`–`A8`: real quotes,
  verbatim in the pinned bytes, recorded sha256 equal to re-fetched bytes; rows are **off the
  rule-attribution topic** by construction (style/conduct/CLI-grammar/README bullet/license/terminal docs).
- a `corpus/README.md` coverage-map row for the note.

Control commit: `0b354079ba7210e0cd9a91d7607b9b3203520b63` (parent `4f21d995…`).

## Exact commands

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/C1OffTopic
git -C /fast/scratch/hyaku/mado-r24/ctl/C1OffTopic checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
# (edit SOURCES.md, note, README.md)
git -C /fast/scratch/hyaku/mado-r24/ctl/C1OffTopic add corpus/SOURCES.md corpus/README.md corpus/knowledge/rule-attribution-r24.md
git -C /fast/scratch/hyaku/mado-r24/ctl/C1OffTopic -c user.name=ctl -c user.email=ctl@local commit -q -m \
  "C1 control: off-topic real pinned rows (S900-S907) + rule-attribution note + README coverage row"
# v1 counter (frozen copy from d9fec1d3, sha256 2fc366ab…2291):
cd /fast/scratch/hyaku/mado-r24/ctl
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show d9fec1d3:.ufo/waves/round-24/c1/count.py > c1-v1.py
timeout 300 env MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1OffTopic \
  python3 -I c1-v1.py 0b354079ba7210e0cd9a91d7607b9b3203520b63
# v2 counter (lane file at c9b76646):
timeout 300 env MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1OffTopic \
  python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py \
  0b354079ba7210e0cd9a91d7607b9b3203520b63
```

## Control commit

```
commit 0b354079ba7210e0cd9a91d7607b9b3203520b63
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:36:30 2026 -0300

    C1 control: off-topic real pinned rows (S900-S907) + rule-attribution note + README coverage row

 corpus/README.md                         |  1 +
 corpus/SOURCES.md                        |  8 ++++++++
 corpus/knowledge/rule-attribution-r24.md | 24 ++++++++++++++++++++++++
 3 files changed, 33 insertions(+)
```

## Counter sha256 (lane copies)

- v1 (`d9fec1d3:.ufo/waves/round-24/c1/count.py`): `2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291`
- v2 (lane file at `c9b76646`): `b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`

## Full counter output

### v1 (exit 0)

```
A1	S900	PASS_ROW	-
A2	S901	PASS_ROW	-
A3	S901	PASS_ROW	-
A4	S902	PASS_ROW	-
A5	S902	PASS_ROW	-
A6	S903	PASS_ROW	-
A7	S903	FAIL_ROW	quote-off-topic
A8	S906	FAIL_ROW	quote-off-topic,no-hyprwm-url
revision=0b354079ba7210e0cd9a91d7607b9b3203520b63 mode=refetch note_present=True rows=8 PASS_ROW=6 distinct_sources=4 readme_indexed=True verdict=TARGET_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

### v2 (exit 1)

```
A1	S900	FAIL_ROW	claim-not-anchored-to-quote
A2	S901	FAIL_ROW	claim-not-anchored-to-quote
A3	S901	FAIL_ROW	claim-not-anchored-to-quote
A4	S902	FAIL_ROW	claim-not-anchored-to-quote
A5	S902	FAIL_ROW	claim-not-anchored-to-quote
A6	S903	FAIL_ROW	claim-not-anchored-to-quote
A7	S903	FAIL_ROW	quote-off-topic
A8	S906	FAIL_ROW	quote-off-topic,claim-not-anchored-to-quote,no-hyprwm-url
counter_version=v2 revision=0b354079ba7210e0cd9a91d7607b9b3203520b63 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

## Verdict

v1 (the counter committed at the round base `4f21d995`, and the one the control was designed against):
**CONTROL_MEETS_TARGET: yes** — `TARGET_MET` (PASS_ROW=6 ≥ 6; distinct sources 4 ≥ 3; README coverage-map row present).
v2 (counter added later at lane `c9b76646`): **CONTROL_MEETS_TARGET: no** — `TARGET_NOT_MET` (PASS_ROW=0).

## Exact hole (v1)

v1's `PASS_ROW` has **no claim-anchor requirement**, and its topic regex
`TOPIC_RE = \b(?:window ?rules?|windowrules?(?:v2)?|layerrules?|rules?|getprop|props?|tags?|match(?:es|ing)?)\b`
matches the bare words `rule(s)`, `tag`, `matching` anywhere. Therefore a row whose *quoted line*
is wholly off the attribution topic **passes** as long as the line incidentally contains one of those
words, the URL is a pinned /hyprwm/Hyprland (or hyprland-wiki) URL, the recorded sha256 equals the
re-fetched bytes, and the no is present. All six passing rows are such cases (A1 style-contract "rule",
A2/A3 conduct "rule(s)", A4 CLI help "matching", A5 CLI help "tag", A6 README feature bullet "rules");
A7 (no topic word) fails `quote-off-topic` and A8 (kitty) fails `no-hyprwm-url`, which is the only
clause separating the non-hyprwm rows — the r23 terminal URLs fail v1 solely on the URL clause, even
with correct pinned sha256. v2 closes this specific control by rejecting every claim that does not
contain a ≥4-word quote run or a backticked ≥4-char identifier occurring in the quote
(`claim-not-anchored-to-quote`); a v2-meeting row that is still off-topic is possible if the claim
quotes the line's words in order, so the anchor clause is a syntactic, not a topical, gate.
