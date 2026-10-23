# C1Junk — fabricated attribution negative control

## Control and expected detector

Control: add eight invented attribution claims and distinct invented quotes containing `rule` to `corpus/knowledge/rule-attribution-r24.md`; cite three new 11-cell SOURCES rows S900–S902, marked `mined`, opened `2026-10-23`, with the required used-by path, syntactically pinned but invented Hyprland URLs and invented 64-hex SHA-256 values; add the requested `junk | junk` README coverage-map row. No source was opened or genuine attribution research performed. The note explicitly labels the fixture fabricated.

Expected: the refetch counter rejects unavailable invented URLs, so the control does not meet the target. No counter or manifest was edited. Per parent instruction, the same unchanged control was scored under both v1 and v2. Its base remains `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`.

Frozen predicate v1:

> PASS_ROW: a claim row `| A<n> | <claim> | S### | "<quote>" |` in corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or /hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs verbatim (whitespace-collapsed) in those bytes.

Frozen predicate v2:

> PASS_ROW: a claim row `| A<n> | <claim> | S### | "<quote>" |` in corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or /hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs verbatim (whitespace-collapsed) in those bytes, and whose claim cell contains a run of at least 4 consecutive words of that quote or a backticked identifier of at least 4 characters that occurs in that quote.

Target in both versions: PASS_ROW >= 6 from >= 3 distinct source rows, plus the README coverage-map row.

## Commands and commit

Working directory for commands: `/home/vgpnk/Projects/shokunin`. Every external command was timeout-bounded; clone, export and detector invocations had a 2 GiB address-space cap. Git environment overrides were unset. Fixture construction used the write/edit tools; the exact committed edits are preserved in `C1Junk.patch`.

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=2147483648 -- git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/C1Junk
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C1Junk checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C1Junk add corpus/SOURCES.md corpus/README.md corpus/knowledge/rule-attribution-r24.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C1Junk -c user.name=ctl -c user.email=ctl@local commit -m 'control: fabricate C1 attribution quotes and pinned sources'
timeout 15 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C1Junk show --stat HEAD
```

Clone, checkout, add, commit and show exited 0. Control commit: `a7f65fad400703cf8d8a45e24bfdba59073d72dc`. `HEAD` in both mutated scoring commands below resolved to that commit.

Full `git show --stat` output:

```text
commit a7f65fad400703cf8d8a45e24bfdba59073d72dc
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:34:31 2026 -0300

    control: fabricate C1 attribution quotes and pinned sources

 corpus/README.md                         |  1 +
 corpus/SOURCES.md                        |  3 +++
 corpus/knowledge/rule-attribution-r24.md | 15 +++++++++++++++
 3 files changed, 19 insertions(+)
```

The following exact export argv were executed through `subprocess.run(..., env=clean_env, capture_output=True)`, where `clean_env` removed `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`. Both exited 0. The write tool saved stdout unchanged, respectively to the clone's `.git/c1-v1.py` and the lane receipt `controls/C1Junk.patch`.

```sh
timeout 20 prlimit --as=2147483648 -- git -C /home/vgpnk/Projects/shokunin/mado-shokunin show d9fec1d3:.ufo/waves/round-24/c1/count.py
timeout 30 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mado-r24/ctl/C1Junk format-patch -1 --stdout a7f65fad400703cf8d8a45e24bfdba59073d72dc
```

## Counter identity

The lane copy was hashed with:

```sh
timeout 10 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

Initial lane v1 output, before the parent's v2 update:

```text
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

Lane v2 output, before scoring and again in the restoration hash run:

```text
b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

The exported committed v1 bytes also hashed to `sha256:2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291`. v1 was taken from the lane's committed `d9fec1d3` counter; v2 used the lane file supplied by the parent, whose reported committed revision was `c9b76646`. No offline mode was used.

## Pristine detector outputs

### v1 — pristine (before editing, before lane v2 update)

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1Junk prlimit --as=2147483648 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout:

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

Exit: 1. No stderr.

### v2 — pristine revision

The v2 pristine run scored the immutable base revision; by then the worktree held the committed control, which the detector does not read for this REV.

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1Junk prlimit --as=2147483648 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout:

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

Exit: 1. No stderr.

## Control detector outputs

### v1 — mutated

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1Junk prlimit --as=2147483648 -- python3 -I /fast/scratch/hyaku/mado-r24/ctl/C1Junk/.git/c1-v1.py HEAD
```

Full stdout:

```text
A1	S900	FAIL_ROW	fetch-failed
A2	S901	FAIL_ROW	fetch-failed
A3	S902	FAIL_ROW	fetch-failed
A4	S900	FAIL_ROW	fetch-failed
A5	S901	FAIL_ROW	fetch-failed
A6	S902	FAIL_ROW	fetch-failed
A7	S900	FAIL_ROW	fetch-failed
A8	S901	FAIL_ROW	fetch-failed
revision=a7f65fad400703cf8d8a45e24bfdba59073d72dc mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

Exit: 1. No stderr.

### v2 — mutated (same control, no retuning)

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1Junk prlimit --as=2147483648 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py HEAD
```

Full stdout:

```text
A1	S900	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
A2	S901	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
A3	S902	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
A4	S900	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
A5	S901	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
A6	S902	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
A7	S900	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
A8	S901	FAIL_ROW	claim-not-anchored-to-quote,fetch-failed
counter_version=v2 revision=a7f65fad400703cf8d8a45e24bfdba59073d72dc mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

Exit: 1. No stderr.

## Restoration and restored detector outputs

Exact restoration command (exit 0):

```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C1Junk checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

### v1 — restored

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1Junk prlimit --as=2147483648 -- python3 -I /fast/scratch/hyaku/mado-r24/ctl/C1Junk/.git/c1-v1.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout:

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

Exit: 1. No stderr.

### v2 — restored

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C1Junk prlimit --as=2147483648 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout:

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

Exit: 1. No stderr.

### Exact byte evidence

Hash commands (each exited 0):

```sh
timeout 10 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/README.md
timeout 10 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/README.md /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/knowledge/rule-attribution-r24.md /fast/scratch/hyaku/mado-r24/ctl/C1Junk/.git/c1-v1.py
timeout 10 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/SOURCES.md /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/README.md /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
timeout 10 test ! -e /fast/scratch/hyaku/mado-r24/ctl/C1Junk/corpus/knowledge/rule-attribution-r24.md
```

The first hash command ran before fixture creation, the second on the committed mutant, and the third after restoration. The final absence test exited 0 with empty output. The detector also reported the note absent at both pristine and restored revisions.

| File | Pristine | Mutated | Restored |
|---|---|---|---|
| `corpus/SOURCES.md` | sha256:ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc | sha256:3f8784f2a2ac2fad6779402a9f49d715f09ceb36989fbaab5d0bbffc10b449ea | sha256:ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc |
| `corpus/README.md` | sha256:3bcf586809dd506c32546ceefd84163ae73fa857a3047ee5d49076d75ea933e4 | sha256:3eda2acfd1defbf48c73e6165c2c16d815b503c3ab57e70deb622c89bb67022a | sha256:3bcf586809dd506c32546ceefd84163ae73fa857a3047ee5d49076d75ea933e4 |
| `corpus/knowledge/rule-attribution-r24.md` | absent | sha256:a8891b93d89d125b1f88beaa69b170d3c2047d93a7cbcc40c58f2424c90a88f3 | absent |

The temporary exported `.git/c1-v1.py` was deleted with the edit tool after the restored run. No tools were installed or updated. All started commands completed; no background job or service was started. No lane/fleet Git or Jujutsu write command was used. The only lane writes were this receipt and its patch.

## Verdict

Both v1 and v2 reject the unchanged junk control: 0/8 PASS_ROW, 0 distinct passing sources, README indexed, TARGET_NOT_MET, exit 1. All eight rows report `fetch-failed`; v2 additionally reports `claim-not-anchored-to-quote` for all eight. This probe does not establish quote/hash checking after a successful fetch, because these invented URLs did not produce bytes.

Mutation-test kill classification: **inconclusive**, not a killed-mutant claim, because pristine already exits 1 with TARGET_NOT_MET. As the assigned negative control, the observed result is unambiguously that junk does not meet the target under either counter. Exact affected bytes were restored.

CONTROL_MEETS_TARGET: no
