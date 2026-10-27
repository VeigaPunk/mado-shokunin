# MutC1Counter — seat evidence index (round 48, wave w2 FALSIFY)

Report: `../MutC1Counter.md` (relative to this directory's parent: `.ufo/waves/round-48/w2/MutC1Counter.md`).

Every cell below is one **full** invocation of the frozen counter over **all 190 cold + all 204 warm fixtures**
(same `--nonce 4848` for every cell), plus the 394 explain cases and the 230 generated cases that counter runs
in the same process. Nothing in the lane was written; the replay tree lives in the clone described in the report.

| path | what it is |
|---|---|
| `matrix.tsv` | one row per measured cell: log name, verbatim final line |
| `finals.txt` | the same final lines, one block per cell |
| `own.tsv` | per cell, failing fixture ids **beyond** the frozen `reference` control's baseline (7 warm + 14 explain fixtures), i.e. what the cell's own rule costs |
| `selftests.txt` | every `clause=s` line of the frozen-control matrix (20× `43/43`, 2× `69/69`, 1× rc=1 `69/69`) |
| `probe-write.txt` | direct sandbox measurement: the frozen `writes-cache` control writes a 205-byte cache when `.rw` is writable, cannot when it is read-only, and `trips=[]` in both cases |
| `patches.txt` | full diffs of the 9 counter mutants (one per clause `a s f w x g i i r`) |
| `patches2.txt`, `patches3.txt`, `patches3b.txt` | full diffs of the candidate-derived probes (`probe-f-percent`, `probe-writes`, `probe-hash-off`, `probe-enable-off`, `probe-linelimit-off`, `probe-r-spawn`, `probe-r-spawn2`) |
| `counters/` | the 9 mutant counter files, byte-exact |
| `probes/` | the 10 candidate-derived probe tools, byte-exact |
| `logs/` | the raw counter log of every cell (each < 130 KiB) + `index.txt` (runner index) |
| `build/` | the builders (`build.py`, `build2.py`, `build3.py`), the receipt builder (`mkreceipts.py`), the aggregator (`agg.py`), the runner (`run1.sh`, `mkrev2.sh`, `batch.sh`), the direct probe (`probe-write.py`) and the four plan files |
| `sha256s.txt` | sha256 of every file in this directory (excluding itself) |

Run shape (one cell):

```
python3 -I <counter.py> --repo <scratch clone at freeze 3e6c848a> --rev tool-<name> \
        --work <scratch>/work/tmp.XXXXXXXX --nonce 4848
```

where `tool-<name>` is a commit whose `tools/mado-terminal.py` is the named tool (data candidate, frozen control,
counter mutant or probe).
