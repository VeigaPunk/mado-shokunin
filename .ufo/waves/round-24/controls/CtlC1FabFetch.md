# CtlC1FabFetch — fabricated committed fetch bytes

CONTROL_MEETS_TARGET: no
OFFLINE_DIAGNOSTIC_MEETS_TARGET: yes

## Control, expected detector, and scope

One control commit adds eight locally invented, on-topic window-rule attribution quotes in three text files named `.ufo/waves/round-24/fetch/S900.bin`, `S901.bin`, and `S902.bin`. Each file contains all eight quotes; its source-id header differs, so its digest differs. SOURCES rows S900–S902 record the corresponding local digest, a real-looking pinned upstream Hyprland URL that does not serve those local bytes, status `mined`, opened `2026-10-23`, and the note in `used-by`. Eight note rows distribute distinct invented quotes across those three source ids; each claim repeats its quote wording. A README coverage-map row indexes the note. No upstream study or actual rule-attribution implementation is supplied.

Expected detector: counted refetch must reject all rows because the URL bytes have a different sha256; `--offline` may accept the locally fabricated bytes and matching locally recorded sha256. Both v1 and v2 behaved exactly this way. Every counted row failed specifically with `sha256-mismatch`, not a fetch failure. The v2 claim-anchor clause makes no difference to this same, unchanged control.

Axes: provenance integrity; diagnostic-versus-counted separation; exact scratch restoration. No production code, counter, manifest, host configuration, service, or sibling checkout was edited. No tools were installed or updated.

- Base: `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`.
- Control commit: `6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94`.
- Isolated clone: `/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch`.
- Patch: `.ufo/waves/round-24/controls/CtlC1FabFetch.patch` (full `format-patch` stdout, saved with the file-write tool).

## Counter identity and change notification

The first read and lane `sha256sum` observed v1. Before the first pristine execution, the lane copy was externally changed to v2. The parent then explicitly requested both versions and identified v2 as lane commit `c9b76646`. All v2 pristine/control/restored runs used the same v2 digest below. V1 runs used the clone's untouched, committed `.ufo/waves/round-24/c1/count.py` at the instructed base; its digest exactly equals the original lane v1 digest. No counter was edited or copied over another counter. The control stayed based on the instructed base, and the same control commit was scored by both versions.

Actual lane hash outputs before/after that external movement:

```text
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py
```

V1 counter sha256: `sha256:2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291`.
V2 counter sha256: `sha256:b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`.

## Frozen predicates

V1:

> PASS_ROW: a claim row `| A<n> | <claim> | S### | "<quote>" |` in corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or /hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs verbatim (whitespace-collapsed) in those bytes.

V2:

> PASS_ROW: a claim row `| A<n> | <claim> | S### | "<quote>" |` in corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or /hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs verbatim (whitespace-collapsed) in those bytes, and whose claim cell contains a run of at least 4 consecutive words of that quote or a backticked identifier of at least 4 characters that occurs in that quote.

Target, unchanged: `PASS_ROW >= 6` from at least three distinct source ids, with the note indexed by a README coverage-map row. Offline is diagnostic only.

## Exact commands

All shell commands were individually timeout-bounded. Recursive Git operations and every detector process had a 2 GiB virtual-memory cap (`ulimit -v 2097152`). Git environment overrides were unset for every Git write and detector invocation. Content creation used the file-write and anchored-edit tools, not shell edit scripts; the exact created/added bytes are retained in the patch.

### Clone and one control commit

```sh
timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'ulimit -v 2097152; exec git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch'
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'ulimit -v 2097152; exec git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949'
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'ulimit -v 2097152; exec git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch add -f -- .ufo/waves/round-24/fetch/S900.bin .ufo/waves/round-24/fetch/S901.bin .ufo/waves/round-24/fetch/S902.bin corpus/knowledge/rule-attribution-r24.md corpus/SOURCES.md corpus/README.md' && timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'ulimit -v 2097152; exec git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch -c user.name=ctl -c user.email=ctl@local commit -m "control: fabricate local fetch bytes behind pinned Hyprland URLs"'
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch show --stat HEAD
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'ulimit -v 2097152; exec git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch format-patch -1 --stdout 6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94'
```

### Pristine detector invocations

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 --offline'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 --offline'
```

### Control detector invocations

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py 6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py 6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94 --offline'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94 --offline'
```

### Restoration and restored detector invocations

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'ulimit -v 2097152; exec git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py HEAD'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py HEAD --offline'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py HEAD'
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch bash -c 'ulimit -v 2097152; exec python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py HEAD --offline'
```

### Hash commands

```sh
timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
timeout 20 sha256sum /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/corpus/README.md
timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py
timeout 20 sha256sum /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/fetch/S900.bin /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/fetch/S901.bin /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/fetch/S902.bin
timeout 20 sha256sum /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/corpus/README.md /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/corpus/knowledge/rule-attribution-r24.md /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/fetch/S900.bin /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/fetch/S901.bin /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/fetch/S902.bin /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py
timeout 20 sha256sum /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/corpus/README.md /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py /fast/scratch/hyaku/mado-r24/ctl/CtlC1FabFetch/.ufo/waves/round-24/c1/count.py
```

## Control commit: actual `git show --stat`

```text
commit 6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:35:13 2026 -0300

    control: fabricate local fetch bytes behind pinned Hyprland URLs

 .ufo/waves/round-24/fetch/S900.bin       | 10 ++++++++++
 .ufo/waves/round-24/fetch/S901.bin       | 10 ++++++++++
 .ufo/waves/round-24/fetch/S902.bin       | 10 ++++++++++
 corpus/README.md                         |  1 +
 corpus/SOURCES.md                        |  3 +++
 corpus/knowledge/rule-attribution-r24.md | 14 ++++++++++++++
 6 files changed, 48 insertions(+)
```

## Full detector stdout and exits

Each fenced block below is the complete counter stdout for that invocation. No counter stderr was emitted.

### Pristine v1 counted — exit 1

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

### Pristine v1 offline — exit 1

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=offline note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

### Pristine v2 counted — exit 1

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

### Pristine v2 offline — exit 1

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=offline note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

### Control v1 counted — exit 1

```text
A1	S900	FAIL_ROW	sha256-mismatch
A2	S900	FAIL_ROW	sha256-mismatch
A3	S900	FAIL_ROW	sha256-mismatch
A4	S901	FAIL_ROW	sha256-mismatch
A5	S901	FAIL_ROW	sha256-mismatch
A6	S901	FAIL_ROW	sha256-mismatch
A7	S902	FAIL_ROW	sha256-mismatch
A8	S902	FAIL_ROW	sha256-mismatch
revision=6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

### Control v1 offline — exit 0 (diagnostic only)

```text
A1	S900	PASS_ROW	-
A2	S900	PASS_ROW	-
A3	S900	PASS_ROW	-
A4	S901	PASS_ROW	-
A5	S901	PASS_ROW	-
A6	S901	PASS_ROW	-
A7	S902	PASS_ROW	-
A8	S902	PASS_ROW	-
revision=6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94 mode=offline note_present=True rows=8 PASS_ROW=8 distinct_sources=3 readme_indexed=True verdict=TARGET_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

### Control v2 counted — exit 1

```text
A1	S900	FAIL_ROW	sha256-mismatch
A2	S900	FAIL_ROW	sha256-mismatch
A3	S900	FAIL_ROW	sha256-mismatch
A4	S901	FAIL_ROW	sha256-mismatch
A5	S901	FAIL_ROW	sha256-mismatch
A6	S901	FAIL_ROW	sha256-mismatch
A7	S902	FAIL_ROW	sha256-mismatch
A8	S902	FAIL_ROW	sha256-mismatch
counter_version=v2 revision=6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

### Control v2 offline — exit 0 (diagnostic only)

```text
A1	S900	PASS_ROW	-
A2	S900	PASS_ROW	-
A3	S900	PASS_ROW	-
A4	S901	PASS_ROW	-
A5	S901	PASS_ROW	-
A6	S901	PASS_ROW	-
A7	S902	PASS_ROW	-
A8	S902	PASS_ROW	-
counter_version=v2 revision=6c84c4f5ac5ba39b79f460be2d3d58bf27e70c94 mode=offline note_present=True rows=8 PASS_ROW=8 distinct_sources=3 readme_indexed=True verdict=TARGET_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

### Restored v1 counted — exit 1

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

### Restored v1 offline — exit 1

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=offline note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

### Restored v2 counted — exit 1

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

### Restored v2 offline — exit 1

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=offline note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

## Before, mutated, and restored bytes

All digests in this table are sha256, not commit ids. `absent` means no file existed; both initial and restored file-name probes found no fetch files or attribution note. The restored hashes were measured after the successful checkout back to base. Restored detectors used `HEAD` and resolved it to the base commit, as printed above.

| Relative clone path | Pristine | Control | Restored |
|---|---|---|---|
| `corpus/SOURCES.md` | sha256:ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc | sha256:536480e1c22f2bd579107f53c4d14d33668cb1c56fe757c3e49142c6d6a18f8a | sha256:ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc |
| `corpus/README.md` | sha256:3bcf586809dd506c32546ceefd84163ae73fa857a3047ee5d49076d75ea933e4 | sha256:a94b79d52f2dbde2129a441f4600725a94ff6bf56b6f8326bd834efe3a988aef | sha256:3bcf586809dd506c32546ceefd84163ae73fa857a3047ee5d49076d75ea933e4 |
| `corpus/knowledge/rule-attribution-r24.md` | absent | sha256:a705b87bf4281fc6024be0b19a2b1787e88cfd7e2388b5dd6042b628ae01fb35 | absent |
| `.ufo/waves/round-24/fetch/S900.bin` | absent | sha256:67c58ff2f97906d1112edcb628853a9bdca817b8c50d2993176000a5e14a74bc | absent |
| `.ufo/waves/round-24/fetch/S901.bin` | absent | sha256:795b6209bcd33b3ec94fa47a69b2348c125ceafe38eea82d4779710a4f351626 | absent |
| `.ufo/waves/round-24/fetch/S902.bin` | absent | sha256:681f91c800d65aac176794d55f335f72fd9f1bdc9ced3ef20f1e7141cd482d7e | absent |

V1 counter remained byte-identical in the clone; v2 lane counter remained byte-identical throughout every actual detector run. All timeout-bounded processes completed; no service or long-lived process was started.

## Verdict

Counted control result under both v1 and v2: **TARGET_NOT_MET**, `PASS_ROW=0/8`, exit 1; every row rejected for a sha256 mismatch. Offline diagnostic result under both versions: **TARGET_MET**, `PASS_ROW=8/8` from three source ids, exit 0. The diagnostic trusts committed fetch bytes and their locally recorded hashes; this is not a counted-mode hole because counted mode re-fetches the URLs. Do not promote the offline result to the registered target.

Strict mutation kill classification: **inconclusive**, not a killed mutant: the pristine coverage target already exits 1 because the note is absent. This assignment is a pre-data negative control; its observed counted rejection and offline acceptance are reported independently of a passing-baseline mutation claim. No baseline failure is represented as a killed mutant.

CONTROL_MEETS_TARGET: no
