# MutC1Clauses — mutation probe of PRED-C1-r37-v2 against the round-37 controls

Seat: L1Mado37-2.MutC1Clauses (mutation-tester). Lane production files were not touched. Tool installs: none.

## Verdict

9 mutants. 4 killed, 5 survived. The pristine baseline scored 13/13, so every verdict below is conclusive.

| mutant | controls that kill it | verdict |
|---|---|---|
| force-a | none | SURVIVED (equivalent at the frozen BASE, see finding F1) |
| force-b | none | SURVIVED (real coverage gap, F2) |
| force-c | `c1-not-mined` | KILLED |
| force-d | none | SURVIVED (equivalent mutant: clause g implies clause d, F3) |
| force-e | `c1-unindexed` | KILLED |
| force-f | `c1-token-ungrounded` | KILLED |
| force-g | `c1-token-stub` | KILLED |
| drop-registry-fence | none | SURVIVED (real coverage gap, F4) |
| drop-gate-fence | none | SURVIVED (real coverage gap, F4) |

Each clause is exercised by exactly one control. No control has two kills, and the five C1 controls `c1-do-nothing`, `c1-package-copy`, `c1-junk-quotes`, `c1-wrong-digest` and `c1-golden-v2` killed nothing. The golden control stayed `TARGET_MET` 2/2 under every mutant, as expected.

## Method

- Frozen counter `quality/counters/c1-r37-event-ground.py`, sha256 `1c21f8ba736bf8c17eeab4d485c9101ba98436d17bad4dfe73a66bededb6294f`. Frozen `.ufo/waves/round-37/controls.py`, sha256 `27fc5213464168e58d879d2a0d39162c6c348e5f7da57dbf70fa604bd55709ef`.
- Generator `/dev/shm/mado37-MutC1Clauses/gen.py` (a copy is in `.ufo/waves/round-37/w1/scratch/MutC1Clauses/gen.py`). It asserts that each anchor occurs exactly once, then writes one `c1.py` per variant and one `controls.py` copy. The `controls.py` copy differs from the frozen file only on line 21: `C1 = "/dev/shm/mado37-MutC1Clauses/<variant>/c1.py"`. `diff` confirmed that this was the only change, and that `pristine/c1.py` is byte-identical to the frozen counter.
- Mutations, each a one-line diff confirmed by `diff`:
  - `force-<k>`, for k = a…g: inserts `c["<k>"] = 1` at line 158, directly before `ok = int(all(c.values()))`. This forces the clause to 1 after it has been computed.
  - `drop-registry-fence`: line 80 `for line in section(text, "## Registry"):` becomes `for line in text.splitlines():`.
  - `drop-gate-fence`: line 115 `for line in section(lesson, "## Gate"):` becomes `for line in lesson.splitlines():`.
- Detector: `python3 <variant>/controls.py --out <variant>/receipt.txt`. Each variant was scored with the same detector, the frozen 13-control set (C2 controls included, unchanged).

| variant | c1.py sha256 (16 hex) |
|---|---|
| pristine | 1c21f8ba736bf8c1 |
| force-a | fd4d30adc9a55a0d |
| force-b | 00e81c21abe74623 |
| force-c | d7fe2ea6954749b4 |
| force-d | 476bf43fc411f20d |
| force-e | eae808c815562e36 |
| force-f | bb47b1443f62a5e2 |
| force-g | 185b56beca246187 |
| drop-registry-fence | 53c70da4145cfcce |
| drop-gate-fence | c6a6373eeb53af31 |

### Detector noise (discarded runs)

- First pass: ran 4 at a time with `xargs -P 4`. It produced contaminated results, including pristine `correct=12/13` with `c1-golden-v2 ... admitted=0/2` and every clause 0, and force-d `c2-do-nothing ... SETUP unresolvable revision`. Several runs crashed with `FileNotFoundError: ... /c1-token-stub/corpus/SOURCES.md`. Cause: `controls.py` `sh("git","clone",...)` does not check its return code, so a failed clone leaves an empty sandbox. Every result from this pass was discarded.
- Second pass: serial, with retries when no receipt was written or `SETUP unresolvable` appeared. force-a and force-c each needed 3 tries; the other variants passed on the first try. force-b failed all 3 with `OSError: [Errno 122] Disk quota exceeded`, which means `/dev/shm` was contended by siblings even though `df` later showed 22% used. force-b was rerun alone and succeeded on the first try. No final receipt contains a `SETUP` line (`grep -c SETUP` returned 0 for all 10).
- Side observation, not in scope to fix: because `controls.py` ignores clone failures, a transient failure turns into a false `ok=0` or a crash.

## Final receipts (serial pass)

```
== pristine            controls=13 correct=13/13
== force-a             controls=13 correct=13/13
== force-b             controls=13 correct=13/13
== force-c             controls=13 correct=12/13
control=c1-not-mined expect=TARGET_MISSED rc=0 ok=0 :: PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET
== force-d             controls=13 correct=13/13
== force-e             controls=13 correct=12/13
control=c1-unindexed expect=TARGET_MISSED rc=0 ok=0 :: PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET
== force-f             controls=13 correct=12/13
control=c1-token-ungrounded expect=TARGET_MISSED rc=0 ok=0 :: PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET
== force-g             controls=13 correct=12/13
control=c1-token-stub expect=TARGET_MISSED rc=0 ok=0 :: PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET
== drop-registry-fence controls=13 correct=13/13
== drop-gate-fence     controls=13 correct=13/13
```

Full receipts, mutants and controls copies: `.ufo/waves/round-37/w1/scratch/MutC1Clauses/<variant>/{c1.py,controls.py,receipt.txt}`.

## Findings

### F1: force-a survives because no control can isolate a=0

Under force-a, the only controls with a=0 also had every other clause at 0:

```
control=c1-do-nothing ... entry=event-delivery-limits-r26.md a=1 b=0 c=0 d=0 e=0 f=0 g=0 ids=- ok=0
```

At the frozen BASE, `git ls-tree b4e47e98… -- <both targets> corpus/lessons/round-37.md` returned 0 lines, so neither target exists there. Every control is built on BASE and `controls.py` passes the fixed `--base BASE`. So for this harness, a=0 means "the entry is absent at REV". An absent entry has an empty body, which already forces f=0 (and b, c, d, g to 0 for lack of ids).

Clause a's "did not exist at BASE" half only matters when an entry exists at BASE but holds no frozen token, which the precondition's token check would not catch. Killing force-a needs a control with a different base: commit a token-free entry at the target path, wire everything on top, and pass `--base` at the first commit. The current harness cannot express this because the base is fixed.

### F2: force-b survives; no control exercises a missing verified-at or recheck

Every wired control's entry template, `entry()` at `controls.py:50-53`, always writes `source:`, `verified-at:` and `recheck:`. The only b=0 case is `c1-do-nothing`, which has no ids, so c, d, f and g are also 0:

```
control=c1-do-nothing ... a=0 b=1 c=0 d=0 e=0 f=0 g=0 ids=- ok=0
```

Missing kill: a golden-shaped control with `verified-at:` or `recheck:` dropped from the header, or pushed below line 15.

### F3: force-d is an equivalent mutant, so clause d is subsumed by clause g

At `c1-r37-event-ground.py:143-152`, `stated` can only become true inside the `if blob … and quote.encode() in blob:` branch, which is the same branch that sets `good`. That gives `g_ok ⇒ every cited id good ⇒ d_ok`. So d=0 always implies g=0, and forcing d=1 can never change `ok`. The receipts confirm it: under force-d, `c1-junk-quotes` and `c1-wrong-digest` still miss on f and g.

```
control=c1-junk-quotes  ... a=1 b=1 c=1 d=1 e=1 f=0 g=0 ids=S189,S201,S212 ok=0
control=c1-wrong-digest ... a=1 b=1 c=1 d=1 e=1 f=0 g=0 ids=S189,S201,S212 ok=0
```

No control can kill force-d while clause g keeps its current form. The receipt's `d` column is informative only; it never decides the verdict. This is a coverage finding about the claim's structure, not a defect in any control, and not permission to change the frozen counter.

### F4: both fence mutants survive; no control places rows or GATE lines outside their fences

- At BASE, `corpus/SOURCES.md` has every S-id table row under `## Registry` (`{'## Registry': 201}`). `corpus/lessons/round-37.md` does not exist at BASE.
- `wire()` writes rows before `\n## Paths`, inside Registry (`controls.py:75-76`). It writes GATE lines directly under `## Gate`, the only heading in the lesson (`controls.py:83`).
- So dropping either fence admits nothing new in any control. Missing kills:
  - Registry fence: a control that puts the cited ids' 11-cell `mined` rows under a non-Registry heading (for example after `## Paths`) and leaves Registry without them.
  - Gate fence: a control that puts the valid GATE lines under a different heading (for example `## Notes`) instead of `## Gate`.

## Restoration evidence

All mutation happened on copies under `/dev/shm/mado37-MutC1Clauses/`. The frozen files were never written. After all runs, `sha256sum -c hashes-before.txt` reported:

```
/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r37-event-ground.py: OK
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/controls.py: OK
```

Lane git state was only read (`git log -1`, `git status --porcelain`). The one clone I made directly, a `--no-local` read-only clone used to inspect BASE, was deleted afterwards.
