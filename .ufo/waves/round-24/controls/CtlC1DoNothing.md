# CtlC1DoNothing — C1 unchanged-tree control

CONTROL_MEETS_TARGET: no

## Control and expected detector

Do no coverage work: score the unchanged round base and registered pre-data tip with the lane's committed C1 counter. Per assignment, no clone, mutation, control commit, or patch was created. Commands unset `MADO_LANE`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`; the counter used its default lane. No git/jj write commands were run.

- Base: `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`.
- Registered tip: `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`.
- Expected detector: the missing note yields `PASS_ROW=0`, zero distinct sources, no README coverage-map row, `TARGET_NOT_MET`, exit 1.
- Target: at least six PASS_ROW rows from at least three distinct S### rows plus the README coverage-map row. Offline mode is diagnostic only.

Frozen predicate v1 used for the first three runs (the committed counter at the registered tip):

> PASS_ROW: a claim row `| A<n> | <claim> | S### | "<quote>" |` in corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or /hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs verbatim (whitespace-collapsed) in those bytes.

## V1 counter provenance and before/after hashes

Before the three v1 runs:

```sh
timeout --kill-after=5s 30s sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

Exit 0; stdout:

```text
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

Counter used by all three v1 runs: `sha256:2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291`, as independently printed in each result below. It matches the registered tip's committed counter:

```sh
timeout --kill-after=5s 30s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949:.ufo/waves/round-24/c1/count.py | timeout --kill-after=5s 30s sha256sum
```

Exit 0; stdout:

```text
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  -
```

After all three runs, the same lane-file hash command returned exit 0 and:

```text
037ffd3b33200107e33445a7f74e018b1ba94e5a934a65884dcef501e0c33966  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

Post-run observation: the lane counter changed concurrently to `sha256:037ffd3b33200107e33445a7f74e018b1ba94e5a934a65884dcef501e0c33966`; reading it showed a `COUNTER_VERSION = v2` docstring and a new claim-anchor predicate. That intermediate state was not scored. Drift was reported to MadoR24. This seat made no counter/source modification and did not overwrite the intervening change. Exact lane-byte preservation across the v1 probe therefore cannot be asserted; all v1 results identify the original committed bytes. The finalized committed v2 was subsequently scored separately below. No restoration was needed for this no-mutation control, and no restoration was performed on externally changed files.

## V1 counted run: unchanged base

Exact command:

```sh
timeout --kill-after=5s 180s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
```

Full stdout:

```text
revision=8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

Stderr: empty. Exit: **1**.

## V1 counted run: registered tip

Exact command:

```sh
timeout --kill-after=5s 180s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout:

```text
revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
```

Stderr: empty. Exit: **1**.

## V1 offline JSON diagnostic: registered tip

Exact command (one run combining both requested flags):

```sh
timeout --kill-after=5s 180s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 --offline --json
```

Full stdout:

```json
{
 "summary": {
  "revision": "4f21d9956e8c7a5d9f824ff24b9a4426a3f51949",
  "mode": "offline",
  "note_present": false,
  "rows": 0,
  "PASS_ROW": 0,
  "distinct_sources": 0,
  "readme_indexed": false,
  "verdict": "TARGET_NOT_MET",
  "counter_sha256": "2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291"
 },
 "rows": []
}
```

Stderr: empty. Exit: **1**.

Both counted runs used `mode=refetch`; there were no claim rows and therefore no source URLs to fetch. The offline run is not counted evidence.

## Compared commit metadata

No control commit exists by assignment. Exact read-only metadata command:

```sh
timeout --kill-after=5s 30s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mado-shokunin show --stat --no-renames 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Exit 0; full stdout:

```text
commit 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
Author: protocol-shokunin <protocol@shokunin.local>
Date:   Thu Oct 22 09:19:49 2026 -0300

    round-23 verifier spot-check (integrator, hyaku): non-author admit/reject

 corpus/lessons/round-23-verifier-spotcheck.md | 153 ++++++++++++++++++++++++++
 1 file changed, 153 insertions(+)

commit 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
Author: mado-shokunin <mado@shokunin.local>
Date:   Fri Oct 23 00:31:24 2026 -0300

    round-24: frozen C2 counter and manifest (before controls); base smoke 1/12 mismatches

 .ufo/waves/round-24/c2/README.md               |  36 +++
 .ufo/waves/round-24/c2/count.py                | 354 +++++++++++++++++++++++++
 .ufo/waves/round-24/c2/manifest.json           | 163 ++++++++++++
 .ufo/waves/round-24/c2/smoke/base-8e5d9369.txt |  15 ++
 4 files changed, 568 insertions(+)
```

## V1 identity at the original freeze

After MadoR24 requested scoring both versions, the already captured v1 runs were identified against the original freeze without rerunning or changing the control:

```sh
timeout --kill-after=5s 30s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mado-shokunin show d9fec1d3:.ufo/waves/round-24/c1/count.py | timeout --kill-after=5s 30s sha256sum
```

Exit 0; stdout:

```text
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  -
```

The three v1 results above therefore scored exactly the original committed frozen counter. No extracted script was necessary because those runs had already executed those bytes in the lane.

## V2 predicate and provenance

MadoR24 subsequently requested the same control under committed v2. The control revisions remained unchanged: base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` and registered tip `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`. Only the detector version changed.

Frozen predicate v2:

> PASS_ROW: a claim row `| A<n> | <claim> | S### | "<quote>" |` in corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or /hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs verbatim (whitespace-collapsed) in those bytes, and whose claim cell contains a run of at least 4 consecutive words of that quote or a backticked identifier of at least 4 characters that occurs in that quote.

Counter: `sha256:b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`.

Before and after the three v2 runs, this exact command returned exit 0 and the identical stdout shown:

```sh
timeout --kill-after=5s 30s sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

```text
b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

Committed-counter identity command:

```sh
timeout --kill-after=5s 30s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mado-shokunin show c9b76646bd2ecf44d83f5bfaafcda23971a4d107:.ufo/waves/round-24/c1/count.py | timeout --kill-after=5s 30s sha256sum
```

Exit 0; stdout:

```text
b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66  -
```

Exact read-only v2 commit metadata command:

```sh
timeout --kill-after=5s 30s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mado-shokunin show --stat --no-renames c9b76646
```

Exit 0; full stdout:

```text
commit c9b76646bd2ecf44d83f5bfaafcda23971a4d107
Author: mado-shokunin <mado@shokunin.local>
Date:   Fri Oct 23 00:33:39 2026 -0300

    round-24: C1 counter v2 (claim-anchor clause) before any data seat; registration updated

 .ufo/waves/round-24/c1/count.py                     | 21 ++++++++++++++++++---
 .../round-24/evidence/c1-before-v2-8e5d9369.txt     |  3 +++
 .ufo/waves/round-24/registration.md                 |  8 ++++++--
 3 files changed, 27 insertions(+), 5 deletions(-)
```

## V2 counted run: unchanged base

Exact command:

```sh
timeout --kill-after=5s 180s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
```

Full stdout:

```text
counter_version=v2 revision=8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

Stderr: empty. Exit: **1**.

## V2 counted run: registered tip

Exact command:

```sh
timeout --kill-after=5s 180s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout:

```text
counter_version=v2 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
```

Stderr: empty. Exit: **1**.

## V2 offline JSON diagnostic: registered tip

Exact command (one run combining both requested flags):

```sh
timeout --kill-after=5s 180s env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 --offline --json
```

Full stdout:

```json
{
 "summary": {
  "counter_version": "v2",
  "revision": "4f21d9956e8c7a5d9f824ff24b9a4426a3f51949",
  "mode": "offline",
  "note_present": false,
  "rows": 0,
  "PASS_ROW": 0,
  "distinct_sources": 0,
  "readme_indexed": false,
  "verdict": "TARGET_NOT_MET",
  "counter_sha256": "b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66"
 },
 "rows": []
}
```

Stderr: empty. Exit: **1**.

V2 before/after hashes match exactly. No source mutation or restoration occurred. As with v1, both counted runs were in refetch mode but had no claim rows or source URLs to fetch; offline is diagnostic only.

## Verdict

CONTROL_MEETS_TARGET: no

Under both v1 and v2, the unchanged base and registered tip miss the frozen C1 target: `PASS_ROW=0`, zero distinct sources, no note, and no README index. Each of the four counted runs and both offline diagnostics exited 1. This is a rejected do-nothing control, not a killed mutant; no mutation was performed and a baseline detector miss is not counted as a mutation kill. No target-meeting hole was demonstrated by this control. No source bytes were changed by this seat; the only artifact written is this receipt. No patch or clone was made. All started commands completed. Tools installed or updated: none.
