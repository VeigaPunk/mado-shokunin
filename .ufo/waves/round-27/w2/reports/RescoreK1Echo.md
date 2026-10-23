# K1Echo — fresh-seed v4 re-score

RESCORE K1Echo best: PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED — not met

## Scope and detector

Axes: selector-only ECHO shape fidelity, exact-oracle coverage, source/lexical coverage, and host safety.

Read the frozen registration first. The detector was the unchanged `c1/count-v4.py`, SHA-256 `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`, at resolved revision `2fdca5caaab6859386effbb8fa6acc5250c90633`. It requires type-strict, ordered JSON equality against the isolated pinned Hyprland oracle for all 41 cases: BASE, 25 APPEND, and 15 SYNTH.

The committed control was scored exactly twice with fresh counter-selected seeds. Both runs passed only BASE, returned exit 1, and had empty stderr. No guard failed or retry occurred.

## Fresh results and receipts

Receipt paths below are under `/fast/scratch/hyaku/mado-r27/rescore/`.

| Bytes/run | Fresh seed | BASE | APPEND | SYNTH | Exit | Receipt |
| --- | --- | --- | --- | --- | --- | --- |
| Committed, 1 | `c6ff2633d458c8b9` | 1/1 | 0/25 | 0/15 | 1 | `K1Echo-fresh-seed1.txt` |
| Committed, 2 | `7c8309aac8db9967` | 1/1 | 0/25 | 0/15 | 1 | `K1Echo-fresh-seed2.txt` |
| Strengthened, 1 | `a9b7c3713abcf045` | 1/1 | 0/25 | 0/15 | 1 | `K1Echo-strengthened-seed1.txt` |
| Strengthened, 2 | `986f5197441851a6` | 1/1 | 0/25 | 0/15 | 1 | `K1Echo-strengthened-seed2.txt` |
| Restored scratch bytes | `82d564ff8b302d93` | 1/1 | 0/25 | 0/15 | 1 | `K1Echo-restored-seed1.txt` |

Verbatim PRED lines, in the table's order:

```text
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
```

Every run had empty stderr and printed `exit=1`, equal duplicate BASE oracle tables (`rules=0`), and oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

## Comparison with committed receipts

The assignment calls the supplied receipts “v3”, but its supplied paths `controls/v4/K1Echo-seed{1,2}.txt` actually identify themselves as counter v4 and print `PRED-C1-r27-v4`. I compared those and also the actual `controls/v3/` receipts.

| Committed receipt | Seed | PRED line |
| --- | --- | --- |
| `controls/v4/K1Echo-seed1.txt` | `6d21918c524dd761` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| `controls/v4/K1Echo-seed2.txt` | `2b425b9f475a06e8` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| `controls/v3/K1Echo-seed1.txt` | `908f2689b7dc8f9d` | `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED` |
| `controls/v3/K1Echo-seed2.txt` | `32783f2e1331a85f` | `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED` |

Paths in that table are relative to `.ufo/waves/round-27/`. All four committed receipts identify the same unchanged ECHO tool hash. The two new committed-control v4 results reproduce the previous 1/41 result on different seeds.

## Is this the strongest ECHO shape?

No: the committed implementation reads only the root file and echoes its raw selectors. The registered ECHO shape is one selector-only object per workspace directive; it does not require root-only traversal or literal variables.

I constructed a stronger lexical/traversal variant while retaining the deliberate omission of workspace-rule semantics. The only output fields remain `workspaceString` and `enabled: true`; it still appends one object per reached workspace directive and never merges selectors or interprets rule items. Reusing the committed `K1NoMerge.py` traversal pattern, it follows sources in encounter order, sorted globs, nested and repeated sources, encounter-time variable definitions/redefinitions, comments, continuations, escaped braces, and hyprlang conditional comments. It reads config bytes, not labels or counter metadata, and never invokes Hyprland itself.

The retained stronger variant is:

`/fast/scratch/hyaku/mado-r27/rescore/K1Echo-strengthened.py`

SHA-256: `30e56ecd99438cb21420ef3d6c439ec187d5c89004f3cf6ad42b8f000758e9c0`.

It was scored twice while located at `K1Echo-probe.py`; the receipts identify that path and the stronger hash. It was then renamed without changing bytes so the probe path could be restored. Both stronger runs also scored 1/41. Thus the stronger lexical implementation ties the committed control under this detector; it does not meet the target. This is not a proof of an exhaustive maximum over all possible selector-only readers.

## Mutation interpretation and restoration

The challenged shortcut was root-file-only selector echoing. The isolated scratch probe began as the exact 736 committed bytes, was changed only in this seat's scratch area to the source-aware ECHO variant, and was restored to the exact original bytes after preserving the stronger variant. The same bounded v4 detector ran on pristine, changed, and restored bytes.

Mutation-kill verdict: **inconclusive**, not killed. The pristine negative control already fails the 41/41 target, so a changed-byte target failure cannot establish a killed mutant. The re-score verdict itself is **not met**.

Before/changed/restored SHA-256:

| Subject | Before | Changed | Restored |
| --- | --- | --- | --- |
| Scratch probe | `093aa876dca8081acd1c3a88a0d17475f8510cfaa105d9be57ab12f6a8b9fedd` | `30e56ecd99438cb21420ef3d6c439ec187d5c89004f3cf6ad42b8f000758e9c0` | `093aa876dca8081acd1c3a88a0d17475f8510cfaa105d9be57ab12f6a8b9fedd` |

The restored probe is retained at `/fast/scratch/hyaku/mado-r27/rescore/K1Echo-probe.py`. Its restored-byte detector also returned 1/41. The committed control was never edited and has the same before/after SHA-256 as the restored probe. The counter and oracle remained unchanged; oracle SHA-256 is `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

## Exact scoring commands

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Executed this exact command twice, concurrently, with fresh seeds selected by the counter:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1Echo.py --jobs 6
```

Executed this command twice concurrently on the stronger bytes, then once on restored bytes:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1Echo-probe.py --jobs 6
```

The Python subprocess wrapper also supplied only PATH and HOME in the initial environment, started each command in its own process group, captured stdout/stderr, imposed a 925-second parent deadline, and attempted process-group SIGKILL in `finally` after completion, ignoring an already-absent group. No parent deadline fired. Receipts contain actual counter stdout; stderr was empty in every case.

## Host safety and hash commands

Before writes:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- df -h /fast
```

Output: 804G total, 730G used, 74G available, 91% used.

Before the first score and after the restored-byte score, ran the following argument vector with the initial environment restricted to PATH=/usr/bin and HOME=/home/vgpnk, counting stdout lines containing `/usr/bin/Hyprland` in Python:

```sh
timeout 30 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend
```

Both listings exited 0 with empty stderr. Counts: **1338 before, 1338 after, delta 0**. Every new receipt independently prints:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

Initial hashes:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1Echo.py .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/controls/v4/K1Echo-seed1.txt .ufo/waves/round-27/controls/v4/K1Echo-seed2.txt
```

Changed-byte and oracle hashes:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/mado-r27/rescore/K1Echo-probe.py .ufo/waves/round-27/harness/oracle.py
```

Final unchanged/restored hashes:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1Echo.py .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/harness/oracle.py /fast/scratch/hyaku/mado-r27/rescore/K1Echo-probe.py /fast/scratch/hyaku/mado-r27/rescore/K1Echo-strengthened.py .ufo/waves/round-27/controls/v4/K1Echo-seed1.txt .ufo/waves/round-27/controls/v4/K1Echo-seed2.txt
```

The two supplied committed v4 receipts remained unchanged, with SHA-256 values `2ccbd3fb46e73d3ffacc3b120dbd8a2d1c2d2e26a4dd3965088f9c61b1e98029` and `b55f183620786f07470f73cc987b4fe777bcb0ea5ce272eab0b4393096e64d1a`.

New receipt SHA-256 values, computed over the saved stdout:

| Receipt | SHA-256 |
| --- | --- |
| `K1Echo-fresh-seed1.txt` | `f5531be29c48ab56b2d7303950efce1a5f82cba10a424c1b8f9b48d25baa58b8` |
| `K1Echo-fresh-seed2.txt` | `1834b5d8d8b53ca8f41d01f47fdc971407e6a2a832bd09e5574cf700aacead31` |
| `K1Echo-strengthened-seed1.txt` | `e8933878272b6bf52831c471c29f92a2ab3e69b672fa01e22f820338004297bb` |
| `K1Echo-strengthened-seed2.txt` | `a721c7c9b0a1480becca6b222dec1931ba88684142136bf6d39fa1708ba00664` |
| `K1Echo-restored-seed1.txt` | `93d6af57581b1d37fffa29794021658127640bed9f495d684bfed0e597653542` |

Hyprland was started only through the frozen counter/oracle, whose host-wide slot locks cap nested instances at 12 and whose cleanup terminates its nested process groups. No live-compositor command, display-variable inheritance in launched subprocesses, card-node access, package transaction, service restart, git/jj write, subagent dispatch, unrelated test, or tool installation/upgrade occurred. All started scoring processes completed and their process groups were cleaned up. Lane writes were limited to this report; all candidate/probe/receipt files are in the assigned rescore scratch area.
