# K1StaticBase — fresh-seed C1 v4 re-score

RESCORE K1StaticBase best: PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED — not met

## Scope and detector

Axes: shape fidelity, fresh-seed discrimination, reproducibility, host safety.

Read the registration first after the requested godspeed skill. Re-scored only the assigned committed control; no solver, counter, harness, control, or sibling source was edited. The control's deliberately incomplete behavior is the constant `print("[]")` at `controls/K1StaticBase.py:12`: accept `--home`, ignore the tree, and replay the previously captured unperturbed table.

The detector was the frozen `c1/count-v4.py`, at revision `2fdca5caaab6859386effbb8fa6acc5250c90633`, using the requested `--jobs 6`. It compares ordered, type-strict JSON against isolated Hyprland v0.56.2 for BASE, 25 APPEND cases, and 15 SYNTH cases; target 41/41. Expected behavior: BASE passes and generated nonempty tables reject this static control.

## Exact scoring command and fresh receipts

Executed the following command twice concurrently, without `--seed`, from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1StaticBase.py --jobs 6
```

The Eval launcher used an explicitly cleared subprocess environment containing only PATH and HOME, captured stdout/stderr, awaited both process exits, and saved the output unchanged with the write tool. Oracle launches retained the frozen harness's 12 host-wide slot locks and teardown paths.

| Run | Fresh seed | Process exit | Receipt |
| --- | --- | --- | --- |
| 1 | `fff361486240cec4` | 1 | `/fast/scratch/hyaku/mado-r27/rescore/K1StaticBase-seed1.txt` |
| 2 | `eb3ca4e36b1b53a3` | 1 | `/fast/scratch/hyaku/mado-r27/rescore/K1StaticBase-seed2.txt` |

Verbatim PRED lines, one per run:

```text
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
```

Both receipts contain:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal rules=0
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
CASE BASE  PASS rules=0 oracle_rules=0 (unperturbed)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

In each run all 25 APPEND cases and all 15 SYNTH cases failed. There were 41 CASE lines and no SETUP_ERROR lines. These are completed detector rejections, not exit-2 guards.

Receipt integrity:

| Receipt | Bytes | SHA-256 |
| --- | --- | --- |
| Fresh seed 1 | 6236 | `f5082758c752e2fde7f5c890cfef0feaba17a185dd81313b53a7b65a36d8c08b` |
| Fresh seed 2 | 6191 | `51593003d01b827f27e2e2dfb6c7ca340b8c7b86a46c833d2454433ed38eadc5` |

## Comparison with committed receipts

The assignment calls the supplied `controls/v4/K1StaticBase-seed*.txt` files “v3 receipts”; their headers and PRED labels identify them as v4. Compared both supplied files and the actual `controls/v3/` files, rather than silently treating v4 receipts as v3.

All paths in the next table are relative to `.ufo/waves/round-27/`.

| Committed receipt | Seed | Verbatim PRED line |
| --- | --- | --- |
| `controls/v4/K1StaticBase-seed1.txt` | `6b95779bb66f3bab` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| `controls/v4/K1StaticBase-seed2.txt` | `dbeaa0c35a3822a7` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| `controls/v3/K1StaticBase-seed1.txt` | `33bcddc387d41635` | `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED` |
| `controls/v3/K1StaticBase-seed2.txt` | `2ee7633fc9a66f80` | `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED` |

All four historical runs likewise passed only BASE and failed all generated cases, with exit 1 and coredump delta 0. The control hash and 79-file snapshot digest match the fresh runs. The historical v4 runs used four workers, as documented in the w1 report; the fresh runs used the requested six. No outcome changed.

## Strongest version within the registered shape

Yes: the registered STATIC-BASE shape is “prints the unperturbed snapshot's table” (`registration.md:59`). Both fresh runs independently queried BASE twice and confirmed that table has zero rules, so the sole JSON-array value faithful to this shape is `[]`. The committed control already emits it correctly.

[INFERENCE] There is no behaviorally stronger variant within this exact shape: changing whitespace leaves the canonical JSON result unchanged; replacing the constant with a nonempty table no longer replays the unperturbed snapshot and loses BASE; inspecting each input to produce a different table changes the control's shape. Accordingly, no purported stronger variant was created or scored. This conclusion is about the registered static-base shape, not a claim that no other control could improve the score.

## Preservation and restoration evidence

Before and after the two runs, executed:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/controls/K1StaticBase.py .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/v4/K1StaticBase-seed1.txt .ufo/waves/round-27/controls/v4/K1StaticBase-seed2.txt .ufo/waves/round-27/controls/v3/K1StaticBase-seed1.txt .ufo/waves/round-27/controls/v3/K1StaticBase-seed2.txt
```

The after command additionally included the two fresh receipt paths. All seven existing files retained identical before/after hashes:

| File, relative to `.ufo/waves/round-27/` | Before = after SHA-256 |
| --- | --- |
| `controls/K1StaticBase.py` | `857cd2de4de199a99fc48527ae64b17938c72cf9dc6f0b9768271297d0a76873` |
| `c1/count-v4.py` | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |
| `controls/v4/K1StaticBase-seed1.txt` | `8c0964021d2183116144a95a6f73a03f6e1f34b00b6d28799094dcf897811c55` |
| `controls/v4/K1StaticBase-seed2.txt` | `527ab4c7024ef51b2b3362f5c05e656033f48b107a25ea5e66c411b42a096a48` |
| `controls/v3/K1StaticBase-seed1.txt` | `0ca1d847a21d731d821525037228ec09429b9a23919d548314cdd8a7ebdaba2d` |
| `controls/v3/K1StaticBase-seed2.txt` | `57a1215ecbf0dcbc27e3a1acefaaf5dde1c11cc8295e9c12948c542e54c5c07d` |

No mutation was applied, so no byte restoration or separate restored run was necessary. This assignment is a negative-control re-score, not a pristine/mutated/restored probe of a passing implementation. The observed rejection is not mislabeled as a killed mutant when no passing implementation baseline was measured.

## Host safety and cleanup

Before scoring, executed:

```sh
timeout 15 df -h /fast && timeout 20 env -i PATH=/usr/bin HOME=/home/vgpnk sh -c 'coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland'
```

Output: `/fast` had 73G available (804G total, 731G used, 91%); Hyprland coredump count was `1338`.

After scoring, executed:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- sh -c 'coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland'
```

Output: `1338`. Observed coredump delta: 0; both detector receipts independently report delta 0.

No live compositor query or mutation was performed. Nested compositors ran only through the frozen counter/oracle, with no inherited desktop compositor variables in the scoring subprocesses. No DRM card node was used by this work; the unchanged oracle binds its registered render node. Both bounded counter processes exited normally, after the oracle's existing process-group termination/wait cleanup and counter scratch cleanup. No long-lived service was started.

Only the two assigned fresh receipts and this report were written. No git/jj write command, subagent dispatch, tool installation/update, unrelated verification, or access to held-out/critic artifacts occurred.
