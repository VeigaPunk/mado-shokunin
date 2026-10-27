# MutC1Counter — frozen C1 control sensitivity

## Verdict

The frozen controls expose sensitivity to weakened `f`, `g`, and `r`; they do not expose a weakened `s` in the present control set. `t` has a direct absent-tool control. `i` remains unprobed: the supplied frozen scorer does not implement an `i` mutation, and its sandbox already mounts all of `/usr/lib`, so it cannot distinguish the counter's narrow runtime-library closure from the proposed broad `/usr/lib` bind. This is a bounded control-sensitivity probe, not a claim that six literal counter-source mutants were executed.

## Method and outputs

Used the frozen `.ufo/waves/round-49/w1/ExecControlsC1/score-controls.py`, `controls/`, and `cases.json`; scorer reports 44 cases (14 fixed + 30 generated), not the frozen production counter's 633 + 150. Ran pristine, then scorer `--weaken s`, `f`, `g`, and `r` independently, with `--header`; scratch and HOME/XDG paths were under `/fast/scratch/hyaku/mado-r50/MutC1Counter/`. Actual full output receipts are under `receipts/`.

- Pristine: `controls=20 met=0`; rc 0.
- `s` off: `controls=20 met=0`; rc 0. No control detects this weakening in this 44-case scorer. In particular c02/c20 still fail other predicates, so their presence does not establish selftest-clause sensitivity.
- `f` off: `controls=20 met=1 c15-layout1-only.py`; rc 1. Killed: the layout1-only defect passes once fixture equality is omitted.
- `g` off: `controls=20 met=2 c06-cache-table.py,c10-overfit.py`; rc 1. Killed: fixture-table/overfit controls pass once generated equality is omitted.
- `r` off: `controls=20 met=3 c05-exec-xkbcli.py,c08-writes-file.py,c09-opens-socket.py`; rc 1. Killed: process, write, and socket controls pass once tracing is omitted.
- `t`: pristine output has `c01-absent ... verdict=TARGET_MISSED stop=t (tool absent)`, so the absent-tool case exercises the t check. There is no `--weaken t` implementation in the scorer.
- `i`: scorer's `Box.argv` mounts `/usr/lib` read-only (`score-controls.py:104-117`) and has no `i` switch (`:246-247`, `:281-284`). Consequently the scorer cannot exercise narrow-vs-whole `/usr/lib` binding. c07 is a repository-read isolation control, not a discriminator for that mount widening.

The `--weaken` runs are the provided scorer's clause-off controls, not byte-mutated copies of `quality/counters/c1-r49-keysym.py`; this limits the verdict to sensitivity under that scoring replica. In particular it would be inaccurate to report full six-clause mutation coverage.

## Restoration and artifacts

No source/control/case bytes were edited. Counter SHA-256 before/after (same unchanged source): `2597c204abf1e9e7c625d98cf83f0b340a0d82897da4986c550e35c5dff5db62`. Scorer: `e1074a4978da928c25601d6b4bb875cb55172b07bb2f4c2c8ea3ccad358103e1`; cases: `0cc35aef40f3d74b3e59b7fbeb3f17963fd6b7bb7b371f249ca2d614d85c482f`; manifest: `53a019d25a0f8bd822886bc68a1e5f0f5932e4abfcfe8866ecfd66a4529910bc`. Scratch tree was removed after copying the complete stdout receipts into `.ufo/waves/round-50/w1/MutC1Counter/receipts/`.

Receipt SHA-256: `baseline.txt` ff4c38bdae5c7e4c558f63aa92dc48571486926660a25f6b406852dce6f54142; `weaken-s.txt` d73813b6001f23d33e7dac8152bf60bdcdd52ecd36d096b6721f62f4918495cd; `weaken-f.txt` 700b5ca75a504346a2e7fde9f589c99ea6c84fd836659721b7a8e11e22a302af; `weaken-g.txt` ae717d475cce7e26e72285637e6f6d5bef764031f2844d3edb2765d0b07da178; `weaken-r.txt` a041d305811d767b0dcd7b8fc885d8312dd7e8dcfcd05c912ab073813464883d.

Report: `.ufo/waves/round-50/w1/MutC1Counter.md`
