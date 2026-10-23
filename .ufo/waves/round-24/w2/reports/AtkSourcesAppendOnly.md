# AtkSourcesAppendOnly — round 24, wave 2

VERDICT: partial

The delivered SOURCES discipline holds at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`: only S153–S168 were appended, all requested row fields conform, and the requested census exits 0. Mutation protection is partial: the census rejects a missing cell, C1 diagnoses a corrupted referenced hash without rejecting the overall target, and an unused row promoted to mined only produces a census warning. These are coverage findings, not evidence that the pristine tip violates the contract or that C1's frozen target should change.

## Scope and axes

Attacked append-only fidelity, row shape/provenance, status/used-by consistency, detector sensitivity, and exact restoration. Read the round registration and both detector implementations. No round adjudication or integration was performed.

Only this report was written in the lane. All mutations and git writes occurred in the isolated clone:

`/fast/scratch/hyaku/mado-r24/w2/AtkSourcesAppendOnly/mado-shokunin`

The clone was checked out at the assigned tip. `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset for every sandbox git invocation. Each mutation and restoration was snapshotted with a path-limited, hooks-disabled scratch commit because C1 reads committed revisions, not working-tree bytes.

## 1. Append-only and row census at the assigned tip

Executed, exit 0:

```sh
timeout 30 git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 8e5d9369 39c596307333b8ca0a1e42b3f3b9a748bb8b208b -- corpus/SOURCES.md
```

Observed one hunk, `@@ -162,6 +162,22 @@`: 16 added lines, zero removed lines. Parsing the actual diff additions gave exactly S153, S154, S155, S156, S157, S158, S159, S160, S161, S162, S163, S164, S165, S166, S167, S168, in that order; no other added content and no edited old row.

All 16 additions have 11 cells, opened `2026-10-23`, and one labelled 64-lowercase-hex SHA-256. Statuses are 15 mined and one queued (S161). The mined rows all name `corpus/knowledge/rule-attribution-r24.md` in used-by; S161 has `—`. This is a presence/format check, not a claim that this task independently re-fetched all 16 payloads.

| Row | Cells | Status | Opened | Recorded digest |
|---|---:|---|---|---|
| S153 | 11 | mined | 2026-10-23 | sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6 |
| S154 | 11 | mined | 2026-10-23 | sha256:ee1b0e64c970c62ada2110935de4afb4b8023838244732520c2695dd50e7de19 |
| S155 | 11 | mined | 2026-10-23 | sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| S156 | 11 | mined | 2026-10-23 | sha256:334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44 |
| S157 | 11 | mined | 2026-10-23 | sha256:7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78 |
| S158 | 11 | mined | 2026-10-23 | sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa |
| S159 | 11 | mined | 2026-10-23 | sha256:157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9 |
| S160 | 11 | mined | 2026-10-23 | sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a |
| S161 | 11 | queued | 2026-10-23 | sha256:af0d274b5616ae69b8f62bdf2534a29586eab2a3d20b28c1b0e620d313ca66db |
| S162 | 11 | mined | 2026-10-23 | sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b |
| S163 | 11 | mined | 2026-10-23 | sha256:9321999ac030e8da73abab53f6a0d6f0cf82ddc3c8c63befa845ade8716568ba |
| S164 | 11 | mined | 2026-10-23 | sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded |
| S165 | 11 | mined | 2026-10-23 | sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95 |
| S166 | 11 | mined | 2026-10-23 | sha256:a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836 |
| S167 | 11 | mined | 2026-10-23 | sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0 |
| S168 | 11 | mined | 2026-10-23 | sha256:46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789 |

## 2. Requested live-lane census

Executed:

```sh
timeout --kill-after=5s 60s /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

Exit **0**, **8 stdout lines**, no stderr. Complete stdout:

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

All warnings concern old rows. The pristine scratch census independently exited 0 with the same seven W04 findings and its scratch-path `ok` line.

## 3. Same bounded detector pair on pristine, mutant, restored bytes

For all seven phases below, ran the same commands, with the same scratch directory and environment. The C1 runs used counted **refetch** mode, not `--offline`.

```sh
S=/fast/scratch/hyaku/mado-r24/w2/AtkSourcesAppendOnly/mado-shokunin
timeout --kill-after=5s 60s /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin "$S"
MADO_LANE="$S" timeout --kill-after=5s 360s python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py HEAD
```

Commands ran with a 2 GiB address-space limit. The runner used a separate process group and killed remaining group members in a finally block. No command timed out; all detector stderr streams were empty.

Detector identities:

- Census: sha256:3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30.
- Frozen C1 v2: sha256:b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66.

Baseline C1: exit 0, `rows=26 PASS_ROW=23 distinct_sources=14 readme_indexed=True verdict=TARGET_MET`; A1/S153 was `PASS_ROW`. A5, A7, and A8 were already excluded for `quote-off-topic`; those exclusions are not mutant kills. Every restoration reproduced this baseline.

### M1 — drop one S153 cell

Smallest change: remove the `on-release` recheck cell from SOURCES.md:165, leaving 10 cells. Expected detectors: census E01 and C1's `no-11-cell-sources-row` for A1.

Observed distinguishing output:

```text
# census: exit 1, 8 stdout lines (seven unchanged W04 lines plus E01; no ok line)
mado-shokunin	E01	S153 fields=10

# C1: exit 0
A1	S153	FAIL_ROW	no-11-cell-sources-row
counter_version=v2 revision=b0af464666a5e1f2014fa193f3ab503ce02027f7 mode=refetch note_present=True rows=26 PASS_ROW=22 distinct_sources=13 readme_indexed=True verdict=TARGET_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

**KILLED by census.** C1 also detects the row defect, but its target/exit-code detector survives because 22 rows from 13 sources still exceed the frozen threshold.

### M2 — corrupt one hex digit of S153's recorded SHA-256

Smallest change: at SOURCES.md:165, change sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6 to sha256:0ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6. All other cells and fetched bytes remain unchanged. Expected detector: C1's `sha256-mismatch` for A1; census has no payload-hash check.

Observed distinguishing output:

```text
# census: exit 0, 8 stdout lines (seven unchanged W04 lines plus ok)
mado-shokunin	ok	/fast/scratch/hyaku/mado-r24/w2/AtkSourcesAppendOnly/mado-shokunin/corpus/SOURCES.md

# C1: exit 0
A1	S153	FAIL_ROW	sha256-mismatch
counter_version=v2 revision=e34f6c0a8d94fdd537bdf827c3c6b6d2a83fbca3 mode=refetch note_present=True rows=26 PASS_ROW=22 distinct_sources=13 readme_indexed=True verdict=TARGET_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

**SURVIVED both exit-code guards; detected/rejected by C1's individual-row predicate.** This is not evidence that the corrupted hash is accepted as a PASS_ROW. It shows that census exit 0 plus C1 TARGET_MET does not certify every row's hash.

### M3 — promote S161 to mined, leaving used-by `—`

Smallest change: at SOURCES.md:173, change only `queued` to `mined`. Expected detector: census W03. C1 has no A-row citing S161 and therefore does not evaluate this source row.

Observed distinguishing output:

```text
# census: exit 0, 9 stdout lines (seven unchanged W04 lines, W03, then ok)
mado-shokunin	W03	S161 mined but unused
mado-shokunin	ok	/fast/scratch/hyaku/mado-r24/w2/AtkSourcesAppendOnly/mado-shokunin/corpus/SOURCES.md

# C1: exit 0; no S161 result line
counter_version=v2 revision=76ba7164d0836e70361a336bbf2bfb8997f2653a mode=refetch note_present=True rows=26 PASS_ROW=23 distinct_sources=14 readme_indexed=True verdict=TARGET_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

**SURVIVED both exit-code guards.** Census emits a warning, so this is not silent to a reader of all lines; it is silent to C1 and non-fatal to validation. The canonical CORPUS.md source contract defines mined as cited by at least one used-by path (:103–108). Census documents W03 as warning-only (:31–33) and implements that at :673–674; C1 loops over claim rows (:102–129), not the entire source registry. No contract or detector was changed.

## 4. Restoration evidence

Each probe started with pristine bytes (the previous restoration for M2/M3), restored the original captured row, compared the entire SOURCES.md byte sequence with the saved pristine bytes, committed that restoration in scratch, and reran both detectors. Byte equality was true after each restoration, including the final one.

The complete pristine SOURCES.md digest, **H0**, is sha256:58f6e47ba6b5539291aa4fc48388ae880d4c498e67568ca5e3b908d485ab1e5f.

| Phase | Scratch revision | SOURCES.md digest | Census exit / stdout lines | C1 exit / PASS_ROW / sources |
|---|---|---|---|---|
| Pristine | `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` | H0 | 0 / 8 | 0 / 23 / 14 |
| M1: dropped cell | `b0af464666a5e1f2014fa193f3ab503ce02027f7` | sha256:8be6b41b6c31bbc1f13a2a8eb7818e2f246c3edd077c16a9277ad6a88706cf7c | 1 / 8 | 0 / 22 / 13 |
| M1 restored | `0d786130620d22d0948f1a547b6190378e68ecc0` | H0 | 0 / 8 | 0 / 23 / 14 |
| M2: changed hash | `e34f6c0a8d94fdd537bdf827c3c6b6d2a83fbca3` | sha256:429ecca2ce650e8cdb88288bdf523a7692ab8c95634460ce00864d9bbe1c7166 | 0 / 8 | 0 / 22 / 13 |
| M2 restored | `d9c1c2840dd8aea015fb28f32913f2810e0d6454` | H0 | 0 / 8 | 0 / 23 / 14 |
| M3: mined without used-by | `76ba7164d0836e70361a336bbf2bfb8997f2653a` | sha256:25053403e07b662aedc145040ce6a5ffbb21bde27deb0a82743b5ce4fef81b22 | 0 / 9 | 0 / 23 / 14 |
| M3 restored, final | `e3b0aadc887ff068eb4b98d0e1035c4217c59bdf` | H0 | 0 / 8 | 0 / 23 / 14 |

All C1 phases printed `mode=refetch`, `rows=26`, `readme_indexed=True`, and `verdict=TARGET_MET`. The restored phases returned A1/S153 to `PASS_ROW`; the seven original census warnings remained unchanged. There were no baseline-failure or timeout-based inconclusive mutant classifications.

No packages or tools were installed or updated. No host configuration, service, production instrument, sibling source, or lane git state was changed.
