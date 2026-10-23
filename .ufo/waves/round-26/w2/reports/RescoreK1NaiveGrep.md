# RescoreK1NaiveGrep — C1 counter v2

## Verdict

RESCORE K1NaiveGrep not met (best 13/41)

The unchanged committed control scored **9/41** and **13/41** on two fresh seeds. A new scratch derivative with a one-line, shape-preserving enabled-token improvement scored **6/41** on a third fresh seed. All three processes exited **1**, with `TARGET_MISSED`; none hit a setup/oracle guard. The L1's earlier v2 receipt scored 9/41. These re-scores do not invalidate the kill rule or meet the 41/41 target.

Axes: control-shape fidelity, enabled-value fidelity, detector discrimination, byte preservation, and host isolation.

## Scope and expected detector

- Committed control: `.ufo/waves/round-26/controls/K1NaiveGrep.py`, sha256 `16658352272840f66284b2daf0085709b9535c2e3269c949d029af9d9b1258b3`.
- Shape contract: `w1/reports/K1NaiveGrep.md:10-16`. Blind native `os.walk` order, every regular file, last assignment by name; no source following, sorting, variables, category tracking, inline-comment removal, directive validation, or unknown-name filtering.
- Deliberate defect challenged: replacing config/source evaluation with that blind walk.
- Detector: frozen `.ufo/waves/round-26/c1/count-v2.py`, sha256 `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428`. It compares the exact animation-node and bezier tuple sets against isolated Hyprland for BASE + 20 APPEND + 10 EDIT + 10 SYNTH cases; target 41/41.
- Revision argument for all three runs: `1b0b91e9889cbf984b052f5de564db78330a72aa`. `--tool-file` selects the actual bytes measured; this is not a measurement of a landed production animation tool.

## Exact scoring commands

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

The following identical command ran twice concurrently, once for each unchanged-control re-score. No `--seed` was supplied; each counter generated its own seed. `--jobs 1` bounded this seat to two simultaneous oracle instances during these runs; the pinned harness also enforces the host-wide twelve-slot lock (`harness/oracle.py:32-33,109-125`).

```sh
timeout 900 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NaiveGrep.py --jobs 1
```

After both completed, the strengthened derivative was scored exactly once:

```sh
timeout 900 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/K1NaiveGrep-stronger.py --jobs 1
```

## Actual outputs and receipts

All stdout receipts, including their `exit=` lines, are retained under `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/`:

| Run | Seed | Process exit | Elapsed | Receipt | Receipt sha256 |
| --- | --- | --- | --- | --- | --- |
| Unchanged 1 | `165d22902c1467e9` | 1 | 144.35 s | `rescore-1.txt` | `ed3d7a4649abbbe72e3028b3ba112c069b34e7bc42da5d23df4a0261892a529d` |
| Unchanged 2 | `02efd95414ab3efd` | 1 | 94.94 s | `rescore-2.txt` | `5aea18b78e56a611e51f61bd26d75c4d735cabef1c0508fda47250efac7ebd79` |
| Strengthened | `7b4279e3b06537d6` | 1 | 93.79 s | `stronger.txt` | `45b0b1c190823f418092ac9955080b95037810c928f8a0e18ca29f3ef404d144` |

Verbatim PRED/exit tails, in that order:

```text
PRED-C1-r26-v2 cases_pass=9/41 verdict=TARGET_MISSED
exit=1
```

```text
PRED-C1-r26-v2 cases_pass=13/41 verdict=TARGET_MISSED
exit=1
```

```text
PRED-C1-r26-v2 cases_pass=6/41 verdict=TARGET_MISSED
exit=1
```

Every run printed the following shared diagnostics:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=base (unperturbed)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

Passing cases by family, counted from those receipts:

| Run | BASE / 1 | APPEND / 20 | EDIT / 10 | SYNTH / 10 | Total / 41 |
| --- | --- | --- | --- | --- | --- |
| Unchanged 1 | 1 | 3 | 3 | 2 | 9 |
| Unchanged 2 | 1 | 6 | 4 | 2 | 13 |
| Strengthened | 1 | 2 | 3 | 0 | 6 |

Example actual failure witnesses (multi-operation cases, not individual-operation causal proofs):

```text
# Unchanged 1
CASE C02   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 changed=yes (APPEND:SPACING+COMMENT)
# Unchanged 2
CASE C25   FAIL nodes missing=6 extra=6 beziers missing=0 extra=0 changed=yes (EDIT:delete-bezier+VARIABLE)
# Strengthened
CASE C38   FAIL nodes missing=0 extra=1 beziers missing=0 extra=0 changed=yes (SYNTH:DISABLE+BEZIER+REBEZ+SOURCED+INVALID+ROOT)
```

## Strengthening within the same shape

New scratch artifact: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/K1NaiveGrep-stronger.py` (6,059 bytes), sha256 `e7aed046d308f384f732ff1231b666eb58a13702ab5e872707917cb11323c533`.

Only the enabled-value assignment differs from the committed control. Original line 51:

```python
enabled = fields[1].lower() in ("1", "true", "yes", "on")
```

Scratch line 51:

```python
enabled = fields[1].startswith(("true", "on", "yes")) or re.fullmatch(r"(?:0*1|0[xX]0*1)", fields[1]) is not None
```

This recognizes the case-sensitive true/on/yes prefixes and decimal/hex encodings of integer one, while not treating uppercase `TRUE` as enabled. It still assigns every matched directive: this is value conversion, not directive validation. All traversal, matching, defaults, number handling, unknown-name retention, and malformed-field behavior remain the same. No source graph, variables, inline-comment removal, category logic, path/case keys, filters, or validation were added.

Opened evidence:

- `.ufo/waves/round-26/fetch/SrcAnimConfig.bin:1437-1446`: the handler stores `parseInt(ARGS[1]).value_or(0) == 1` and takes the off path otherwise.
- `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp:134-149`: case-sensitive prefixes and integer conversion.
- `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/Numeric.hpp:25-51`: integral conversion recognizes `0x` and `0X` prefixes and requires the whole token.
- `.ufo/waves/round-26/recon/anim-grammar.md:70-78` records the same enabled behavior.

The candidate scored lower on its fresh seed; no empirical score improvement is claimed. Different seeds prevent attributing the score difference to the code change. The generator's emitted enabled values are 0/1/2 (`count-v2.py:124,175,178-183,225-226`), so this probe does not establish behavioral coverage of the newly handled prefix/hex forms. The blind-walk limitations remain intentional.

## Preservation, restoration, and safety

Before scoring and after all three runs, the following existing files had identical SHA-256 values:

| File | Before and after sha256 |
| --- | --- |
| `.ufo/waves/round-26/controls/K1NaiveGrep.py` | `16658352272840f66284b2daf0085709b9535c2e3269c949d029af9d9b1258b3` |
| `.ufo/waves/round-26/c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `.ufo/waves/round-26/harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

No existing control, product, counter, or harness bytes were mutated; restoration was therefore unnecessary. The scratch derivative is a new evidence artifact, retained with its receipts. This assignment was a control re-score, not a passing-pristine → mutated → restored production-tool experiment. It provides **no separately killed-mutant verdict**; an interpretation requiring the full unchanged control to pass as a pristine baseline would be inconclusive, not a kill.

Auxiliary commands actually used, from the lane directory except the disk check (which ran from `/home/vgpnk/Projects/shokunin`):

```sh
timeout 10 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000 -- df -h /fast
timeout 10 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000 -- sha256sum .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py .ufo/waves/round-26/controls/K1NaiveGrep.py
timeout 10 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/K1NaiveGrep-stronger.py
timeout 10 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000 -- sha256sum .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py .ufo/waves/round-26/controls/K1NaiveGrep.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/K1NaiveGrep-stronger.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/rescore-1.txt /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/rescore-2.txt /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NaiveGrep/stronger.txt
```

The disk check reported `/fast`: 804G total, 658G used, 146G available, 82% used. All three scoring jobs completed normally, without timeout. Hyprland was started only by the pinned oracle, whose `finally` block terminates and waits for its sandbox process groups (`harness/oracle.py:212-226`); the counter removes its temporary trees (`count-v2.py:375-376`). No direct compositor startup, live compositor mutation, card-node access, or long-lived service was initiated by this seat.

Lane writes: this report only. Scratch writes: the new candidate and three bounded receipts. No subagents, git/jj writes, tool installs/updates, builds, linters, formatters, or unrelated tests were run.
