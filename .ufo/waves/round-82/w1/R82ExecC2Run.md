# R82ExecC2Run — independent replay of the C2 counting command and the three tray rows

Scope: read-only replay at freeze `780c30fcae12d74ce8ab3b871a0888696c2415d9`. No lane writes
outside this seat file, no commits, no network fetch, no tool installs. Scratch root
`/fast/scratch/hyaku/mado-r82/R82ExecC2Run` (removed at exit). Lane HEAD while replaying:
`b6146ee69689bb4e19826bc18429b6ff77473341` (child of the freeze; `git diff --stat 780c..HEAD`
touches only round-82 wave evidence — make-spec, receipts, dispatch/ready — never `SKILL.md` or
`tools/mado-barfoot.py`, so the instrument's working-tree/rev byte checks pass and the contract
line prints `tree=bound`).

## 1. Frozen C2 counting command — rc 0, byte-identical to the receipt

Run verbatim from lane root (only `REV`/`DIR` substituted):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c2-r82-runbook.py --repo . \
  --rev 780c30fcae12d74ce8ab3b871a0888696c2415d9 \
  --controls .ufo/waves/round-82/controls/c2-runbook-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c2-runbook-cases-r81.json \
  --scratch-root /fast/scratch/hyaku/mado-r82/R82ExecC2Run
```

- exit status: `0`; wall time 13.44 s; stdout 57 lines; stderr 0 bytes.
- `diff -u .ufo/waves/round-82/receipts/measurement-c2-r82.txt <replay>`: empty, rc 0 (0 bytes).
- sha256 replay output = `e95b19cc3893cfa5be99a74d5b3b217c135dcad6a6b3d291ebda3ad500e57679` =
  sha256 of the committed receipt.
- Because the whole file is identical, all 29 probe lines and all 25 mutant lines are
  byte-identical: `mutants=25 killed=25`.

Contract lines printed (verbatim):

```text
MADO_R82_CONTROLS: sha256=f64d7d5db40fc1da3d75c15315274264dfb53c38396135b978dff7b0b04b36d5 cases=29
MADO_R82_CONTROL: control_new=0/3 held=fixed-value(no-frozen-value-for-the-new-rows) control_all=15/29 rule=held-r78-fixed-value
MADO_R82_RUNBOOK: cases=29 executed=29 matched=29 shapes=24/24 anchors=29/29 rows=29/29 control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET rev=780c30fcae12d74ce8ab3b871a0888696c2415d9 tree=bound
```

## 2. Held round-81 instrument at the freeze — rc 2, setup refusal byte-identical

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c2-r81-runbook.py --repo . \
  --rev 780c30fcae12d74ce8ab3b871a0888696c2415d9 \
  --controls .ufo/waves/round-81/controls/c2-runbook-cases-r81.json \
  --carried .ufo/waves/round-80/controls/c2-runbook-cases-r80.json \
  --scratch-root /fast/scratch/hyaku/mado-r82/R82ExecC2Run
```

- exit status: `2`; stdout 1 line; stderr 0 bytes.
- `diff -u .ufo/waves/round-82/receipts/control-c2-held-instrument-r82.txt <output>`: empty, rc 0.
- sha256 output = `bed3045474cad8b0af7433f4d6d2919d271e0992adee3134dc003012b64b9976` =
  sha256 of the committed control receipt.

Output (verbatim):

```text
MADO_R81_RUNBOOK: ERROR (stage=setup the runbook section carries 0 command rows, frozen target expects 26)
```

The refusal is the expected one: the r81 instrument looks for `### Executable runbook rows
(round 81)`, and the frozen tree's `SKILL.md:231` carries `### Executable runbook rows (round
82)`, so it binds zero rows and refuses before scoring.

## 3. The three tray commands, run twice 2 s apart

Each command executed exactly as its runbook row documents, twice, with a 2 s gap. Shape is the
descriptor the row binds; raw captures stayed in scratch and are not quoted.

| row | run 1 | run 2 | shape stable |
|---|---|---|---|
| `tray-owner` (`busctl --user list`) | rc 0; 1 watcher row; 8 fields; PID column decimal non-zero (1720); regex `(?m)^org\.kde\.StatusNotifierWatcher\s+[1-9][0-9]*\s` matches; header present | identical descriptor | **yes** |
| `tray-interface` (`busctl --user introspect … --no-pager`) | rc 0; exactly 1 `org.kde.StatusNotifierWatcher interface` row; 5 fields; regex matches; header present | identical descriptor | **yes** |
| `tray-methods` (`… \| awk '$2=="method"'`) | rc 0; 8 lines; every line matches `^\.[A-Za-z]+\s+method\s+`; ≥2 lines; names `.Introspect .GetMachineId .Ping .Get .GetAll .Set .RegisterStatusNotifierHost .RegisterStatusNotifierItem` | identical descriptor and identical bytes | **yes** |

Byte-level notes:

- `tray-interface` and `tray-methods`: both runs byte-identical (sha256 prefixes
  `54170b15b3546983…`, `50fdfbb796aba0a1…`).
- `tray-owner`: shape stable and the declared watcher row is identical in both runs; the full
  `busctl --user list` bytes differ only in the **invoking busctl's own transient row** (unique
  name/PID changes per invocation, e.g. `:1.12175/3490515` vs `:1.12176/3502574`). The bound rule
  is the watcher row, so this is not a row-shape flip.
- No row flipped shape; stderr empty (0 bytes) in every run.

## 4. Exit statuses (summary)

| check | rc | evidence |
|---|---|---|
| frozen C2 counter at `780c30fc` | `0` | `verdict=TARGET_MET … tree=bound`; byte-identical to `measurement-c2-r82.txt` |
| held r81 instrument at `780c30fc` | `2` | one-line setup refusal; byte-identical to `control-c2-held-instrument-r82.txt` |
| `tray-owner` ×2 | `0`, `0` | watcher row stable |
| `tray-interface` ×2 | `0`, `0` | byte-identical |
| `tray-methods` ×2 | `0`, `0` | byte-identical |

## Risks / observations (no defect)

- The probe lines embed live host state (e.g. waybar PID 1720) and matched only because that
  state is unchanged since the measurement; a bar restart would change observed text (not the
  bound shape) and a whole-file replay diff would then differ. Expected for live probes.
- `busctl --user list` is never byte-stable because the calling busctl adds its own transient
  row; the declared row binds only the watcher line, which was stable across both samples.

STATUS: ok
