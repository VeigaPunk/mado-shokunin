# C1QuoteSplice — round-24 pre-data adversarial control

CONTROL_MEETS_TARGET: no

- Control commit: `ca20844a8b5ac21c7b0f8da19ffa4d3f59c49159`; exactly one new commit on `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`.
- Isolated clone: `/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice`. The clone is now restored to the assigned base; the control commit remains addressable by its hash and the accompanying patch.
- Receipt: `.ufo/waves/round-24/controls/C1QuoteSplice.md`.
- Patch: `.ufo/waves/round-24/controls/C1QuoteSplice.patch` (sha256:a721bd9afcd8f27973c738791ebe298a97477192d466600a626956d37a70925c).
- Axes challenged: quote contiguity/order, duplicate admission, maximum word count, whitespace normalization. No rule-attribution study was performed or claimed by this fixture.
- v1 result: `rows=8 PASS_ROW=1 distinct_sources=1 readme_indexed=True TARGET_NOT_MET`, exit 1.
- v2 result: `rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True TARGET_NOT_MET`, exit 1.

## Control and expected detector

Eight parseable claim rows, three valid 11-cell source rows, and one README coverage-map row were committed. All source rows are mined, opened 2026-10-23, name the note in used-by, have real pinned upstream URLs, and carry matching full sha256 digests. S901 and S903 deliberately reference the same wiki bytes under different source IDs; S902 references the tagged HyprCtl implementation. This also challenges duplicate detection across source IDs, rather than just duplicate claim IDs.

| Rows | Variant | Expected v1 outcome | Actual v1 | Actual v2 |
|---|---|---|---|---|
| A1 | 22-word quote crossing a real source newline, flattened onto one table line | Accept: frozen predicate collapses whitespace | PASS_ROW, `-` | `claim-not-anchored-to-quote` |
| A2–A6 | Same quote in six total claim rows A1–A6, alternating S901/S903; A2 also doubles spaces | Reject five repetitions despite different IDs and whitespace | `duplicate-quote` for all five | `claim-not-anchored-to-quote` for all five |
| A7 | Two non-adjacent source fragments stitched in reverse source order | Reject nonverbatim reordered splice | `quote-not-in-bytes` | `claim-not-anchored-to-quote,quote-not-in-bytes` |
| A8 | Exact whitespace-collapsed 30-word source span | Reject overlong quote, even though text occurs | `quote>25w` | `quote>25w,claim-not-anchored-to-quote` |

To keep exactly eight rows while including six duplicate instances, the splice and order-change variants share A7, and the whitespace-wrap variant shares the duplicate group. These are not separate independent probes of pure word reordering and pure splicing; the combined defect is rejected by their shared verbatim-membership check.

A1–A6 quote is 22 words; its source contains a literal newline after `changes.` on lines 315–316, but the note contains spaces. A2 has double spaces throughout. A7 places the fragment from HyprCtl line 1470 before the fragment from line 1467, omitting the intervening material. A8 has exactly 30 whitespace-separated words from the wiki's lines 315–316.

The unchanged generic claims do not satisfy the new v2 claim-anchor clause. v2 adds a reason to every row; its `seen_quotes` set receives only passing rows, so v2 does not emit `duplicate-quote` after A1 fails the anchor check. The paired v1 output independently demonstrates rejection of repetition. Neither output contains a provenance, pin, sha256, or fetch failure.

Whitespace flattening survives v1 only as the predicate explicitly permits; this is not a target-level hole. No tested variant meets the target. The control was not changed or recommitted to accommodate v2.

Mutation classification: **inconclusive as a killed-mutant assertion**, because the pristine assigned tip lacks the note and already returns TARGET_NOT_MET. The observed control non-success and individual why-codes above are direct counter results, not a claim that a passing baseline was killed.

## Frozen predicates and counter identities

Per the parent's pre-data instruction, both named committed counter versions were used on the same unchanged control.

### v1 — committed lane copy at d9fec1d3

sha256:2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291

Extracted unchanged to `/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/c1-v1.py`. Extraction stdout was saved byte-for-byte with the file-write tool; the counter itself was not edited.

```text
"PASS_ROW: a claim row `| A<n> | <claim> | S### | \"<quote>\" |` in
corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with
status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a
tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or
/hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched
from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs
verbatim (whitespace-collapsed) in those bytes."
```

### v2 — lane count.py, matching committed c9b76646

sha256:b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66

The lane file was byte-equal to `git show c9b76646:.ufo/waves/round-24/c1/count.py` when captured. Its digest is also printed in both scored outputs and in the actual sha256sum output below.

```text
"PASS_ROW: a claim row `| A<n> | <claim> | S### | \"<quote>\" |` in
corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with
status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a
tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or
/hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched
from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs
verbatim (whitespace-collapsed) in those bytes, and whose claim cell contains a run of
at least 4 consecutive words of that quote or a backticked identifier of at least 4
characters that occurs in that quote."
```

Both targets: PASS_ROW >= 6, at least three distinct S### rows, and a README index row. Both counted runs used network refetch mode, not --offline. Neither counter nor the C2 manifest was edited.

## Exact setup and construction commands

The clone was created and checked out with these actual commands:

```sh
timeout 120 bash -c 'ulimit -v 1048576; exec env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice'
```

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

The raw file URLs were discovered from the upstream repository tree API or an existing committed SOURCES row, then fetched with:

```sh
timeout 90 curl --fail --silent --show-error --max-time 60 --output /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/window-rules.bin https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md
```

```sh
timeout 90 curl --fail --silent --show-error --max-time 60 --output /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/hyprctl.bin https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/debug/HyprCtl.cpp
```

Fetched source bindings, calculated over actual saved response bytes:

- wiki: 16,200 bytes; sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95.
- HyprCtl: 97,582 bytes; sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa.

The note was created with the write tool, and the two existing Markdown files were changed with the edit tool. Their exact changes are the saved format-patch; no shell editing script was used. The first edit attempt was refused for a truncated anchor and made no changes; the anchor was reread before the successful edit.

All commands below were run with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE removed from the child environment. The capture helper sets RLIMIT_AS to 1 GiB, starts a private process session, invokes `timeout --kill-after=5s`, waits for completion, and kills the remaining process group in a finally clause. Network calls have curl's 60-second maximum or the unchanged counter's 60-second fetch timeout. No process tree remains from this probe. No tools were installed or updated; no host configuration or services were changed.

### Counter extraction commands

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 30 git -C /home/vgpnk/Projects/shokunin/mado-shokunin show d9fec1d3:.ufo/waves/round-24/c1/count.py
```

Exit: `0`; stdout saved as the historical counter path above.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 30 git -C /home/vgpnk/Projects/shokunin/mado-shokunin show c9b76646:.ufo/waves/round-24/c1/count.py
```

Exit: `0`; stdout matched the lane file exactly.

### Stage exact fixture files

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 60 git -C /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice add -- corpus/SOURCES.md corpus/README.md corpus/knowledge/rule-attribution-r24.md
```

stdout:

```text

```

stderr: empty.

Exit: `0`.

### Make the sole control commit

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 60 git -C /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice -c user.name=ctl -c user.email=ctl@local commit -m 'control: C1 quote splicing, duplicate ids, wraps, and overlong span'
```

stdout:

```text
[detached HEAD ca20844] control: C1 quote splicing, duplicate ids, wraps, and overlong span
 3 files changed, 20 insertions(+)
 create mode 100644 corpus/knowledge/rule-attribution-r24.md
```

stderr: empty.

Exit: `0`.

### Control commit stat

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 30 git -C /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice show --stat ca20844a8b5ac21c7b0f8da19ffa4d3f59c49159
```

stdout:

```text
commit ca20844a8b5ac21c7b0f8da19ffa4d3f59c49159
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:36:45 2026 -0300

    control: C1 quote splicing, duplicate ids, wraps, and overlong span

 corpus/README.md                         |  1 +
 corpus/SOURCES.md                        |  3 +++
 corpus/knowledge/rule-attribution-r24.md | 16 ++++++++++++++++
 3 files changed, 20 insertions(+)
```

stderr: empty.

Exit: `0`.

## Full detector outputs and exits

### Pristine v1

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice timeout --kill-after=5s 600 python3 -I /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/c1-v1.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

stdout:

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

stderr: empty.

Exit: `1`.

### Pristine v2

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice timeout --kill-after=5s 600 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

stdout:

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

stderr: empty.

Exit: `1`.

### Committed control v1

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice timeout --kill-after=5s 600 python3 -I /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/c1-v1.py ca20844a8b5ac21c7b0f8da19ffa4d3f59c49159
```

stdout:

```text
A1	S901	PASS_ROW	-
A2	S903	FAIL_ROW	duplicate-quote
A3	S901	FAIL_ROW	duplicate-quote
A4	S903	FAIL_ROW	duplicate-quote
A5	S901	FAIL_ROW	duplicate-quote
A6	S903	FAIL_ROW	duplicate-quote
A7	S902	FAIL_ROW	quote-not-in-bytes
A8	S903	FAIL_ROW	quote>25w
revision=ca20844a8b5ac21c7b0f8da19ffa4d3f59c49159 mode=refetch note_present=True rows=8 PASS_ROW=1 distinct_sources=1 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

stderr: empty.

Exit: `1`.

### Committed control v2

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice timeout --kill-after=5s 600 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py ca20844a8b5ac21c7b0f8da19ffa4d3f59c49159
```

stdout:

```text
A1	S901	FAIL_ROW	claim-not-anchored-to-quote
A2	S903	FAIL_ROW	claim-not-anchored-to-quote
A3	S901	FAIL_ROW	claim-not-anchored-to-quote
A4	S903	FAIL_ROW	claim-not-anchored-to-quote
A5	S901	FAIL_ROW	claim-not-anchored-to-quote
A6	S903	FAIL_ROW	claim-not-anchored-to-quote
A7	S902	FAIL_ROW	claim-not-anchored-to-quote,quote-not-in-bytes
A8	S903	FAIL_ROW	quote>25w,claim-not-anchored-to-quote
counter_version=v2 revision=ca20844a8b5ac21c7b0f8da19ffa4d3f59c49159 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

stderr: empty.

Exit: `1`.

### Restore assigned base bytes

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 60 git -C /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

stdout:

```text

```

stderr: empty.

Exit: `0`.

### Restored v1

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice timeout --kill-after=5s 600 python3 -I /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/c1-v1.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

stdout:

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

stderr: empty.

Exit: `1`.

### Restored v2

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice timeout --kill-after=5s 600 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

stdout:

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

stderr: empty.

Exit: `1`.

### Initial read-only baseline before the parent named v1/v2

The first baseline used the then-present lane working copy (sha256:037ffd3b33200107e33445a7f74e018b1ba94e5a934a65884dcef501e0c33966), not either later named committed digest. It is not substituted for either paired pristine run above.

```sh
timeout 600 bash -c 'ulimit -v 1048576; exec env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949'
```

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=037ffd3b33200107e33445a7f74e018b1ba94e5a934a65884dcef501e0c33966
```

Exit: `1`; stderr empty.

## Patch export

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 30 git -C /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice format-patch -1 --stdout
```

Exit: `0`; stderr empty. Full stdout was saved unchanged with the write tool to `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/controls/C1QuoteSplice.patch` (the tool equivalent of redirecting format-patch stdout to that required file). Export happened while the control commit was checked out, before restoration.

## Before / control / after hashes and restoration evidence

| Path | Pristine sha256 | Control sha256 | Restored sha256 |
|---|---|---|---|
| corpus/SOURCES.md | ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc | 45cfcc87cbe12faf2c3743b48c471116d30da367dbcd1d18385f9a8abeb867cf | ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc |
| corpus/README.md | 3bcf586809dd506c32546ceefd84163ae73fa857a3047ee5d49076d75ea933e4 | 32b265dbca463b517b453c89972e2c7e7356c739e0a25a998795763415f50178 | 3bcf586809dd506c32546ceefd84163ae73fa857a3047ee5d49076d75ea933e4 |
| corpus/knowledge/rule-attribution-r24.md | absent | 5ae8a616b0d44984e11639b056b465b00ddf0be65f994a36f461bd4cc5ebfca3 | absent |

Pristine tree: `fdb682d76833d97942bee7e6748a7d34c5718fc9`. Control tree: `e514f3b101f23cb85bc1cdcd93ed21124b926242`. Restored tree: `fdb682d76833d97942bee7e6748a7d34c5718fc9`. The original two file digests match exactly after checkout; the added note is absent. Both restored counter outputs equal their corresponding pristine output, including exit status.

### Control file hashes

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/README.md /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/knowledge/rule-attribution-r24.md
```

stdout:

```text
45cfcc87cbe12faf2c3743b48c471116d30da367dbcd1d18385f9a8abeb867cf  /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/SOURCES.md
32b265dbca463b517b453c89972e2c7e7356c739e0a25a998795763415f50178  /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/README.md
5ae8a616b0d44984e11639b056b465b00ddf0be65f994a36f461bd4cc5ebfca3  /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/knowledge/rule-attribution-r24.md
```

stderr: empty.

Exit: `0`.

### Restored file hashes

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/README.md
```

stdout:

```text
ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc  /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/SOURCES.md
3bcf586809dd506c32546ceefd84163ae73fa857a3047ee5d49076d75ea933e4  /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/corpus/README.md
```

stderr: empty.

Exit: `0`.

### Counter sha256sum

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/c1-v1.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

stdout:

```text
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  /fast/scratch/hyaku/mado-r24/ctl/C1QuoteSplice/.git/c1-v1.py
b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

stderr: empty.

Exit: `0`.

No lane/fleet Git or jj write command was run. Only the isolated clone and this control's two receipt artifacts were written. The fixture is not integrated or shipped.

CONTROL_MEETS_TARGET: no
