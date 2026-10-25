# SimplifyCounters — simplifier seat, mado round 37 wave 1

Scope: deletion proposals for `quality/counters/c1-r37-event-ground.py` (C1),
`quality/counters/c2-r37-eventq.py` (C2) and `.ufo/waves/round-37/controls.py` that keep
every clause and every control verdict. Lane files were not edited. All work lives in
`.ufo/waves/round-37/w1/scratch/SimplifyCounters/` (variants, patches, harness, outputs) and
in `/dev/shm/mado37-SimplifyCounters/`, which has since been removed.

## Verdict summary

| id | file | proposal | 13 controls | differential on paths the controls never reach | verdict |
|----|------|----------|-------------|-----------------------------------------------|---------|
| P1 | C1 | compute `body.splitlines()` once (it ran twice per entry) | 13/13, identical to receipt | 6/6 legs byte-identical | **ACCEPT** |
| P2 | C1 | clause `a`: reuse the BASE `ls-tree` listing instead of a second `git show` | 13/13, identical to receipt | **changes a verdict** (directory at BASE) | **REJECT** |
| P3 | C2 | one `run_tool` helper shared by the fixture cases and the live replay (two copies of write-inputs/run/except become one) | 13/13, identical to receipt | 4/4 verdict legs plus 32/32 tool-input probes byte-identical | **ACCEPT** |
| P4 | controls | delete parameters no caller sets: `sh(cwd=)`, `write(mode=)`, and the `stated=False` default on `entry` | 13/13, identical to receipt | n/a (no new paths) | **ACCEPT** |
| P5 | controls | one `splice()` helper replaces three copy-pasted "insert before `## <heading>`" blocks | 13/13, identical to receipt | n/a | **ACCEPT** |
| P6 | controls | drop `--base BASE` for C1 (C1's frozen `BASE_DEFAULT` is the same sha) | 13/13, identical to receipt | n/a | OPTIONAL (tradeoff below) |
| ALL | all three | P1 + P3 + P4 + P5 | 13/13, identical to receipt | C1 6/6 and C2 4/4 + 32/32 identical | **ACCEPT as one cutover** |

"Identical to receipt" means byte-identical to `.ufo/waves/round-37/receipts/controls-v2.txt`
after normalising only the sandbox `rev=<sha>` fields, which change on every run because the
commit timestamp changes.

Net effect of ALL: C2 goes from 192 to 183 lines, controls.py from 167 to 166, and C1 stays at 173.
The gain is in duplication rather than line count: two copies of the C2 tool-runner (including
its timeout/OSError branch) become one, three copies of the controls section splice become one,
and three dead parameters go. Patches: `scratch/SimplifyCounters/out/{P1..P6,ALL}.patch`.

## What static analysis says (unused imports and names)

- `pyflakes 4.0.3` on all three files: no output, `rc=0`.
- `vulture 2.16 --min-confidence 0` on all three files: no output, `rc=0`.

There are no unused imports, unused names or unreachable statements. The candidates below are
dead parameters, duplicate parsing and duplicated logic, which these tools do not report.

Semantic-reference proof: no `lsp` device is available in this harness, so I used text search as
the fallback and do not offer it as semantic proof. These are the call-site listings I relied on:
- `controls.py` call sites (Grep `\b(sh|write|entry|wire|row|package_copy)\(`): `sh(` appears only
  at lines 142, 143, 145 and 146, none passing `cwd=`. `write(` at 66, 67, 76, 83, 89, 98, 127, 128
  and 129 never passes `mode`. `entry(` at 66 and 67 always passes `stated`.
- Importers of `controls.py` across `.ufo/waves/round-37` are peer probes only:
  `scratch/CritSeparability/probe.py` (`ctl.row`, `ctl.wire`) and `scratch/RevC1Code/probe.py`
  (`ctl.write(SB, path, text)` with 3 args, `ctl.row`, `ctl.wire(SB, quote=…, stated=False)`,
  `ctl.wire(SB, readme=False)`). P4 and P5 keep `write(sb, rel, text)`, `row` and `wire`
  signature-compatible, so neither probe breaks. No lane `.py` file imports `controls.py`.

## Proposals

### P1 — C1 splits the body once (ACCEPT)
`c1-r37-event-ground.py:129` builds `head = body.splitlines()[:15]` and `:141` runs
`lines = body.splitlines()` again on the same `body`. The proposal is `lines = body.splitlines()`
followed by `head = lines[:15]`, deleting the second split. `body` is not reassigned between the
two lines, so the change is semantically identical.

### P2 — C1 clause `a` from the BASE listing (REJECT, harms clause a)
The idea was to replace `show(repo, base, path) is None` (`:127`) with `path not in base_files`,
reusing the `ls-tree -r` listing from `:102`. But `ls-tree -r` lists only blobs, so a target path
that is a directory at BASE counts as "absent" under P2 while `git show` succeeds on it in the
original. Differential leg r2 (E1 path is a directory at BASE, golden wiring at REV):
```
< PRED-C1-r37-v2 entry=corpus/knowledge/event-delivery-limits-r26.md a=0 … ok=0
> PRED-C1-r37-v2 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 … ok=1
< PRED-C1-r37-v2 admitted=1/2 verdict=TARGET_MISSED … base=99e2297f…
> PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET … base=99e2297f…
```
It passes all 13 controls, because no control reaches that input, but it flips a verdict on a
constructible input. The second `git show` stays.

### P3 — C2 single tool runner (ACCEPT)
`run_case` (`c2-r37-eventq.py:106-125`) and the live replay (`:160-172`) each write three input
files, run `python -I tool --ss-file … --log … --journal-file … --disable-logs X`, and catch
`(TimeoutExpired, OSError)`. P3 introduces `run_tool(tool, d, ss_text, log, journal, dl, extra=())`
returning `(rc, lines)`. `run_case` calls it with the encoded fixtures, and the replay becomes
`replay = run_tool(tool, os.path.join(work, "live-replay"), snap, b"", b"", "1")[1]`. The
parameter is named `ss_text` so it does not shadow the module-level `ss()`.

The original wrote fixtures in text mode with the locale encoding; P3 writes `.encode()` (UTF-8)
bytes. These match because every fixture is ASCII:
`fixture_strings 40 all_ascii True`, `locale_encoding_under_-I UTF-8`.

### P4 — controls dead parameters (ACCEPT)
`sh(*cmd, cwd=None)` becomes `sh(*cmd)`, `write(sb, rel, text, mode="w")` becomes
`write(sb, rel, text)` with `open(p, "w")`, and `entry(ids, tokens, stated=False)` becomes
`entry(ids, tokens, stated)`. No call site uses any of them (listing above).

### P5 — controls `splice()` (ACCEPT)
```python
def splice(sb, rel, heading, add):
    head, tail = open(os.path.join(sb, rel)).read().split("\n" + heading, 1)
    write(sb, rel, head.rstrip("\n") + "\n" + add + "\n" + heading + tail)
```
This replaces `controls.py:68,75-76` (SOURCES `## Paths`), `:85-89` (README `## Quality bar` in
`wire`) and `:95-98` (the same splice in `package_copy`). Each produces the same string as the
original expression.

### P6 — redundant `--base` (OPTIONAL)
`controls.py:147-148` passes `--base BASE` only to C1, and `BASE` equals C1's frozen
`BASE_DEFAULT` (`c1-r37-event-ground.py:41`, `b4e47e98…`). Dropping it changes nothing (13/13,
identical to receipt, and every C1 line still prints `base=b4e47e98…`). The tradeoff is that
controls.py then stops pinning the base itself and depends on the counter's default. Both are
frozen today, so this is reviewer's choice, and it is left out of ALL.

### Considered and kept
- C2's `/dev/shm` fallback (`root = "/dev/shm" if os.path.isdir("/dev/shm") else None`, `:140`):
  no input on this host reaches the `None` arm, but other hosts do. Deleting it would crash
  `mkdtemp` there.
- C1's `dict.fromkeys("abcdefg", 0)` (`:126`): every key is reassigned, but the dict fixes the
  printed a…g order while the assignments run a,b,c,d,g,e,f. Deleting it changes the output.
- `wire(e1_ids=…)`: no control overrides it, but it mirrors the overridden `e2_ids`. Deleting it
  saves nothing and makes new controls more expensive to write.
- The per-file `git()` and `ENV` copies across C1, C2 and controls: each script is frozen and
  standalone. A shared module would add a second convention and couple frozen rules.
- The `p.stderr…[-200:]` summary fallback in controls (`:150`): no current control reaches it,
  but it is the only diagnostic when a counter crashes.
- The receipt copy in `wire` (`:63-65`): it is needed, because BASE has no
  `.ufo/waves/round-37/fetch` (`git ls-tree -r --name-only b4e47e98… -- .ufo/waves/round-37/fetch`
  printed nothing).

## Finding F1 — controls.py can report ok=1 on a wrongly built tree (not a deletion; for the L1)
`controls.py` ignores every `sh()` return code (`:142-146`) and keeps all 13 sandboxes until its
`finally` (`:157`). Each sandbox is a full clone: `.git` is 54M and the HEAD tree is 171507443
bytes (`git ls-tree -r -l HEAD | awk` sum). So one run holds about 2.9G, against `/dev/shm` at
2.7–3.5G free while 37 seats share it.

The unmodified files, run through my harness, produced:
- Run 0: `controls=13 correct=12/13` with
  `control=c2-stub-socket … rc=2 ok=0 :: PRED-C2-r37-v2 SETUP unresolvable revision`.
  RevFreezeOrder (F6) independently saw the same 12/13.
- Run 1: `controls=13 correct=13/13`, byte-identical to the receipt, yet the harness logged four
  failed clones and four aborted BASE checkouts, for example
  `SH_FAIL rc=128 cmd=git clone -q --no-local err="…unable to write file …\nfatal: unable to checkout working tree…"`
  followed by
  `SH_FAIL rc=1 cmd=git -C …/c1-package-copy checkout err='…Please move or remove them before you switch branches.\nAborting'`.
  Those controls were built on lane HEAD's partial tree instead of BASE and still printed the
  expected verdicts.

So "13/13" can pass vacuously. In every variant run below I accepted a run only when `SH_FAIL`
counted 0 (every run did so on its first attempt). The fix is outside my edit scope and is not a
deletion, so I only state it: fail the control when any `sh()` step returns non-zero, and
`rmtree` each sandbox right after it is scored, which brings the peak down to one sandbox
(about 225M).

## Evidence

Harness: `scratch/SimplifyCounters/run_controls.py` loads a controls file unmodified, rebinds
only `C1`, `C2` and the counter paths inside `CONTROLS`, and wraps `sh` to print `SH_FAIL` on
non-zero exits. `run_all.sh` runs it per variant with up to 3 attempts gated on `SH_FAIL == 0`,
then diffs against the receipt with `rev=` normalised.

```
$ bash run_all.sh orig P1 P2 P3 P4 P5 P6 ALL
variant=orig try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
variant=P1 try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
variant=P2 try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
variant=P3 try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
variant=P4 try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
variant=P5 try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
variant=P6 try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
variant=ALL try=1 rc=0 sh_fail=0 controls=13 correct=13/13 receipt=IDENTICAL
```
Every one of the 13 per-control verdicts, rc values and detail lines (clauses a–g, case rc/ok)
is unchanged. Per-variant outputs are in `out/<v>.txt`, empty receipt diffs in `out/<v>.diff`,
and `SH_FAIL` logs in `out/<v>.err`.

`diff_c1.sh` runs C1 differentially on a sparse sandbox clone with sandbox identity and
`GIT_*` scrubbed, covering paths no control reaches: r1 the entry existed at BASE as a
token-free file, r2 the entry path was a directory at BASE, r3 ground held at BASE (SETUP exit 2),
r4 unresolvable rev (SETUP exit 2), r5 golden wiring with the default base, and r6 lane HEAD
(read-only `git show`/`ls-tree`).
```
c1diff P1 == orig
c1diff P2 DIFFERS: (r2, quoted under P2)
c1diff ALL == orig
```
The original's legs (`out/c1diff-orig.txt`) were r1 `a=0 … admitted=1/2 TARGET_MISSED rc=1`,
r3 `SETUP ground_held_at_base corpus/knowledge/held.md:MAX_QUEUED_EVENTS rc=2`,
r4 `SETUP unresolvable revision rc=2`, r5 `admitted=2/2 verdict=TARGET_MET rc=0`, and
r6 `admitted=0/2 verdict=TARGET_MISSED rc=1`.

`diff_c2.sh` runs C2 differentially with a probe tool. The probe records, per invocation, its
argv with every file argument replaced by `basename:sha256`, keyed by its cwd (case name or
`live-replay`). Legs: L1 a receipt that matches the replay, L0 a receipt with a wrong pid,
NS no committed snapshot, and T a tool that sleeps 25 s, exercising the 20 s timeout branch.
```
c2diff verdicts P3 == orig
probe P3-L1 argv+input digests == orig (11 runs)
probe P3-L0 argv+input digests == orig (11 runs)
probe P3-NS argv+input digests == orig (10 runs)
c2diff verdicts ALL == orig
probe ALL-L1 argv+input digests == orig (11 runs)
probe ALL-L0 argv+input digests == orig (11 runs)
probe ALL-NS argv+input digests == orig (10 runs)
```
The original's legs were
L1 `fixtures=2/10 readonly=1 live=1 … TARGET_MISSED rc=1`, L0 `… live=0 …`, NS `… live=0 …`, and
T `case=… rc=None ok=0` ×10 then `fixtures=0/10 readonly=1 live=0 … rc=1`.

One limit: T was committed on top of NS, so it had no snapshot and the replay timeout was not
run. The fixture timeout, which P3 makes the same `run_tool` except-branch the replay uses, was
run in all 10 cases.

Shared tree is byte-identical to the freeze (checked at the end):
```
1c21f8ba…6294f  quality/counters/c1-r37-event-ground.py   == …@893a8aa
6fae177f…60f7a  quality/counters/c2-r37-eventq.py         == …@893a8aa
27fc5213…709ef  .ufo/waves/round-37/controls.py           == …@893a8aa
```
No git or jj command mutated LANE. Every commit happened in sandbox clones under `/dev/shm`,
and those have been removed.

## Tools
No installs or upgrades. I used the existing `pyflakes 4.0.3` (Python 3.14.8) and `vulture 2.16`
in `~/.local/bin`, plus `git 2.56.0` and `python3 3.14.8`. pacman was not touched.

## Checks for the main agent
- `cd .ufo/waves/round-37/w1/scratch/SimplifyCounters && bash run_all.sh orig ALL`: expect two
  `13/13 … receipt=IDENTICAL sh_fail=0` lines.
- `bash diff_c1.sh` and `bash diff_c2.sh` (about 4 minutes, because of the timeout leg).
