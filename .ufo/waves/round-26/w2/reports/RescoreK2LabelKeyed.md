# RescoreK2LabelKeyed — C2 fresh-seed re-score

RESCORE K2LabelKeyed not met (best 23/51)

The unchanged committed control scored **21/51** and **22/51** on two fresh seeds. The scratch strengthening attempt scored **23/51** on a third fresh seed. Every run reported `embed_hits=0`, `TARGET_MISSED`, and detector/process exit 1. No setup guard fired or retry occurred. The best above is across these three w2 runs; w1's separate best 24/51 is unchanged.

Axes: detector pressure, label/stat-only shape fidelity, exact source preservation, and host safety. This is a control re-score, not a killed-mutant claim: the pristine control already misses the target, so a mutation-kill interpretation would be inconclusive.

## Detector and unchanged control

- Revision: `1b0b91e9889cbf984b052f5de564db78330a72aa`.
- Frozen detector: `.ufo/waves/round-26/c2/count.py`, SHA-256 `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`.
- Expected detection: exact 18-field bind-multiset agreement with the isolated Hyprland oracle over BASE, 30 ARITH cases and 20 V3 cases; target `cases_pass=51/51 embed_hits=0` (`count.py:4-21,199-225`).
- Committed control: `.ufo/waves/round-26/controls/K2LabelKeyed.py`, SHA-256 `0408d03f6af9675c91764a952a800b27fc4350e9f317a86df64d755820631b9f`.
- Both unchanged runs used its byte-identical scratch copy, `/fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/pristine.py`.

The registered shape is cached oracle tables selected by paths, process labels and stat metadata, with the unchanged round-25 resolver used for unknown identities; no expression evaluator or new bind/source resolver (`w1/reports/K2LabelKeyed.md:10-16`; control `:27-65,68-87`).

## Actual receipts

All three runs observed the same 79-file snapshot digest, `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, and printed `ORACLE_CHECK base_twice equal binds=192`. BASE and all 20 V3 cases passed in every run.

### Unchanged run 1

```text
seed=87f7dd7b09d98f8a
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

ARITH: 0/30. Bash independently reported command exit 1, wall time 171.21 seconds.

Full detector stdout: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/rescore-1.stdout` (12,389 bytes; SHA-256 `fb09983d3e649de6c21b6de267d969ebc5026e010d30e82f776d98d5e55ebb58`). Original tool transcript: `artifact://23591`.

### Unchanged run 2

```text
seed=2697c57e3c288561
CASE A09            PASS oracle_binds=194 missing=0 extra=0 (ARITH[unclosed+unclosed]@sourced)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=22/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

ARITH: 1/30. Bash independently reported command exit 1, wall time 124.80 seconds.

Full detector stdout: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/rescore-2.stdout` (12,641 bytes; SHA-256 `7b39e45c0ced56c296f6b8da4c713807a66ed83ad933b5f8b5388ef01494c516`). Original tool transcript: `artifact://23508`.

### Strengthening attempt

```text
seed=16654ff514949817
CASE A17            PASS oracle_binds=192 missing=0 extra=0 (ARITH[desc+resize+desc+ws]@sourced)
CASE A18            PASS oracle_binds=192 missing=0 extra=0 (ARITH[move+ws]@sourced)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

ARITH: 2/30. Bash independently reported command exit 1, wall time 47.34 seconds. Retained receipt excerpt: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/strengthened.receipt.txt`. That file is explicitly an excerpt, not full stdout; the full third output was delivered in the completed `bg_4866` tool result, but the job handle had expired when subsequently opened.

The saved unchanged-run stdout files contain the detector's 59 lines through `exit=1`; tool-added display footers and wall-time/process-status annotations were excluded. Read-tool truncation and an unexpected footer despite `:raw` were reported to `xd://report_issue`.

## What was strengthened, within the control shape

Only an isolated scratch copy was changed. The tested candidate is preserved at:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/strengthened-at-score.py`

SHA-256: `7de84b075057b5fcaf8c10aeddb9427161d35c5fa719549807f46cd61fd7630c`.

The added branch broadens metadata-based selection of the already cached BASE table. It stores the baseline filename/size inventory from the existing w1 training artifacts and, after the original cache/label lookups fail, selects BASE when:

1. The filename set exactly matches that inventory.
2. Exactly one file's size differs.
3. That file is under `.local/share/omarchy/default/hypr/apps/` and has grown by at least 141 bytes.

The hypothesis was motivated by two existing oracle-trained examples with unchanged BASE truth: training-1 A07 (200-byte growth in `apps/1password.conf`) and training-2 A13 (141-byte growth in `apps/browser.conf`). Sources are the retained `/fast/scratch/hyaku/mado-r26/K2LabelKeyed/training-1.json` and `training-2.json` records. These are two motivating examples, **not** evidence that this generalized metadata family has unanimous truth; the new branch is deliberately a speculative cache-selection heuristic, less conservative than the original cache-eligibility policy.

The candidate still selects only a precomputed table using relative paths and stat sizes, otherwise executes the unchanged fallback. It does not read configuration contents for the added branch, evaluate expressions, add a bind/source resolver, change the counter, or change its acceptance contract. The original encoded table data and fallback source were not edited.

The third score is one case above the best unchanged w2 run, but the seeds differ. No paired-population improvement or cache-hit telemetry was measured, and no general improvement is claimed. It still missed 28/30 ARITH cases and remained far below the target. Encoded cached tables again produced zero literal-source embed hits; that is not evidence that the tool contains no cached table.

## Exact commands

Scoring cwd: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Capacity check:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 df -h /fast
```

Observed: `/fast` 804G total, 658G used, 146G available, 82% used. No large writes were made.

Scratch setup:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 20 prlimit --as=4000000000 mkdir -p /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 20 prlimit --as=4000000000 cp .ufo/waves/round-26/controls/K2LabelKeyed.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/pristine.py
```

The following identical command was run twice, independently and concurrently. No `--seed` argument was supplied; the frozen counter generated the distinct seeds printed above.

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/pristine.py --jobs 2
```

Candidate creation used the same bounded/display-cleared `cp` from `pristine.py` to `strengthened.py`, followed by a surgical scratch-only edit adding the metadata inventory, selector and call. Its single score command was:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/strengthened.py --jobs 2
```

After the candidate run completed, its exact tested bytes were retained and the edited scratch path restored:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 20 prlimit --as=4000000000 cp /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/strengthened.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/strengthened-at-score.py
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 20 prlimit --as=4000000000 cp /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/pristine.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK2LabelKeyed/strengthened.py
```

Before/after hashes used `env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 20 prlimit --as=4000000000 sha256sum` on the paths in the next table. Receipts were retained through Eval's read/write helpers; no detector was rerun merely to obtain its output.

## Preservation, restoration and safety

| Path | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `.ufo/waves/round-26/controls/K2LabelKeyed.py` | `0408d03f6af9675c91764a952a800b27fc4350e9f317a86df64d755820631b9f` | `0408d03f6af9675c91764a952a800b27fc4350e9f317a86df64d755820631b9f` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |
| `.ufo/waves/round-25/c1/count-v3.py` | `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` | `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` |
| `tools/mado-binds.py` | `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950` | `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950` |
| Scratch `strengthened.py` | `0408d03f6af9675c91764a952a800b27fc4350e9f317a86df64d755820631b9f` | `0408d03f6af9675c91764a952a800b27fc4350e9f317a86df64d755820631b9f` |

At-score scratch hash was `7de84b075057b5fcaf8c10aeddb9427161d35c5fa719549807f46cd61fd7630c`; the retained `strengthened-at-score.py` has that hash. `pristine.py` also still hashes to `0408d03f6af9675c91764a952a800b27fc4350e9f317a86df64d755820631b9f`. Restoration evidence is byte-hash equality; no separate restored behavioral run was requested or claimed.

All nested compositors were launched only by the pinned oracle through the frozen counter. Its shared flock slot pool enforces the host-wide 12-instance ceiling (`oracle.py:109-125`); these commands used `--jobs 2`. Outer soft/hard address-space limits were 4/8 GB, allowing the oracle's own 8 GB limit. The commands removed inherited display/signature variables. No direct Hyprland launch, DRM card-node access, live-compositor mutation, git/jj write, service restart, network access, subagent dispatch, or sibling-source edit occurred.

All three counter processes completed normally; their oracle cleanup runs stop and kill each sandbox process group in `finally` (`oracle.py:203-226`). No long-lived job was started. Every score's coredump delta was zero. No tools were installed or upgraded. No build, lint, formatter, unrelated test or extra frozen-counter score was run. The only lane write was this report; scratch evidence was retained, with no integration or shipping action.
