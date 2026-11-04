# R75ExecGate — no-harm and routed-defect findings

Axes: no-harm correctness; closure-count accuracy; scratch routing; frozen-versus-working-tree provenance. Investigation only: no production edits, installations, commits or delegates.

All commands below ran with cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`. Let `S=/fast/scratch/hyaku/mado-r75/R75ExecGate`. Receipts named below are siblings of this report and retain commands, observed output and exit codes.

## Exact selftest tallies

| Command | Observed line | rc | Receipt |
|---|---|---:|---|
| `env -u MADO_SELFTEST_SCRATCH TMPDIR="$S/tmp" bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed` | 0 | `gate-current.txt` |
| `python3 -I quality/counters/c1-r74-witness-rule.py --selftest --scratch-root "$S/r74"` | `MADO_R74_WITNESS_RULE_SELFTEST: 23/23 assertions passed` | 0 | `c1-r74.txt` |
| `python3 -I quality/counters/c2-r74-shapes.py --selftest --controls .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root "$S/r74c2"` | `MADO_R74_GUARD_SHAPES_SELFTEST: 86/86 assertions passed` | 0 | `c2-r74.txt` |
| `python3 -I quality/counters/c2-r75-shapes.py --selftest --controls .ufo/waves/round-75/controls/c2-cases-r75.json --scratch-root "$S/r75c2"` | `MADO_R75_GUARD_SHAPES_SELFTEST: 97/97 assertions passed` | 0 | `c2-r75.txt` |
| `env -u MADO_SELFTEST_SCRATCH TMPDIR="$S/tmp" bash -x "$S/frozen-mado-verify.sh" --selftest` | `MADO_SELFTEST: 460/460 assertions passed` | 0 | `gate-frozen-red.txt` |

The frozen script was obtained by `git show def73656c94f0e88bd671cfb4a65124338261722:tools/mado-verify.sh` (rc 0), written only to this seat's scratch. The two gate selftests and three counter selftests were executed as explicitly assigned, not as an integration gate.

## Frozen gate identity versus repaired working tree

Command (rc 0):

```sh
git rev-parse b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6:tools/mado-verify.sh def73656c94f0e88bd671cfb4a65124338261722:tools/mado-verify.sh
```

Both outputs are `9113c7c05e586328f44ed6822a3d12ff34c47a36`: the two committed gate blobs are byte-identical (`gate-blob-identity.txt`). This does NOT claim that the current working tree equals either blob. On first inspection the working tree already contained the scratch-routing repair at lines 418–422.

The repaired bytes pass 460/460, including R10's derived-target/recorded-pin assertion (`tools/mado-verify.sh:610`). The working-tree pin at line 2040 is `49567a0fd1d7d3601cd6111aafcb5aef7a89aaa9d08c6eba65b6439730128249`; the frozen trace records old pin `367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e` and R10 equality at that old pin. The re-cut note at working-tree lines 2021–2024 explicitly attributes the move to scratch routing outside the marker pairs. This seat did not edit the gate or pin and did not run a mutation sweep.

## D1 reproduced: closure undercounts witness-rule selftest

At observation, `SKILL.md:734` says:

> 0 only when every assertion passes (21/21)

`LOG.md:3657–3658` identifies `quality/counters/c1-r74-witness-rule.py` and states:

> (`credit(out, nonce)`, hermetic selftest 21/21)

The explicitly named rule actually prints **23/23**, rc 0. The closure undercounts by two assertions; it is a documentation mismatch, not a failed rule selftest. The neighboring replay-witness tool also says 21/21 but is a different instrument; that row is not the finding. These observations predate any concurrent correction by the owning seat.

## Routed /tmp defect: independent red-before reproduction

Exact frozen `tools/mado-verify.sh:418` (`frozen-gate-lines.txt`):

```sh
  T=$(mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX) || { echo "cannot mktemp" >&2; exit 2; }
```

Even with `TMPDIR="$S/tmp"`, the frozen script's trace is:

```text
++ mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX
+ T=/tmp/w5-mado-m52-selftest.mEPO3H
```

An independent observer repeatedly executed this command during the selftests (rc 0; unique observed directory paths retained in `scratch-find.txt`):

```sh
find /tmp /fast/scratch/hyaku/mado-r75/R75ExecGate/tmp -maxdepth 1 -type d -name 'w5-mado-m52-selftest.*' -print
```

It observed `/tmp/w5-mado-m52-selftest.mEPO3H`, exactly matching the frozen trace, and directories under the assigned TMPDIR including `w5-mado-m52-selftest.5XOeKe` and `w5-mado-m52-selftest.RoTuGb` during the repaired run. Other `/tmp` names in the receipt are not attributed to this seat. The gates remove their own successful fixtures, so observation was performed while they ran, not only after deletion.

**Red-before means scratch-policy failure, not a red selftest exit:** the frozen gate still passes 460/460 while ignoring TMPDIR. The repaired working-tree allocation uses `SCRATCH_BASE=${MADO_SELFTEST_SCRATCH:-${TMPDIR:-/tmp}}` and creates fixtures beneath that base. Thus the routing repair and the frozen no-harm blob claim concern different bytes.

## Committed receipts re-read, not rerun or rewritten

- `control-baseline-r75.txt`: held C1 6/11; held C2 41/47.
- `measurement-c1-r75.txt`: `cases=11 correct=11 base_correct=6 verdict=TARGET_MET`.
- `measurement-c2-r75.txt`: `population=20 readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET`.

The assignment states rc 0 for both measurement receipts; their file contents contain contract lines but no rc trailers. Those are committed-receipt claims, not newly exercised measurement commands by this seat.

## Delivery, limits and cleanup

Files changed: only this report and sibling advisory evidence receipts inside this seat's exclusive directory. No production, corpus, closure or sibling-lane files were changed. No tooling installed. No LSP-supported symbol/refactor work was needed; no LSP tool is exposed in this seat.

The scratch tree is removed after retaining the cited evidence. No blocker. Scope does not establish broad mutation coverage or validate other seats' concurrent edits. L1 owns post-integration gates and any documentation correction.

Self-evaluation: accuracy 4/5 (concurrent /tmp paths require attribution by frozen trace); completeness 5/5 (all requested tallies, identity and routing evidence retained); clarity 4/5 (frozen/current distinction necessarily adds detail); actionability 5/5 (D1 and exact allocation identified); conciseness 4/5 (separate receipts preserve detail). Overall 4.4/5. Improvement priority: preserve provenance distinction when incorporating findings. Would the user agree? Expected yes: both routed defects are independently reproduced without edits to committed instruments.
