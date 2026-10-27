# Attack19 — C1 population and row-grammar omissions in the integrated counter

Seat `Attack19` · round 52 w2 · lane `mado-shokunin` · base `85d57a818c3707397e21c840b6498b105ba798aa`.
Axes named: **operability** (C1 only; no coverage move). Attack posture: each item names the
frozen clause, the exact reproduction, and a reproduced/not-reproduced verdict. This is an
attack report, not a vote and not a judgment of non-author seats.

Artifact under test: `quality/counters/c1-r52-ledger.py`, 78 lines,
sha256 `923faf02cd0c2db374f7757d38ef24fc8381c2882cb3d853882f0fadce1c17d7`
(untracked, `git status`: `?? quality/counters/c1-r52-ledger.py`). These bytes match **neither**
W1 draft — not `C1CounterDesign`'s `0fe862f1…` (847 lines) nor `C1Simplify`'s `0d31fc6c…` (194
lines). No W1 receipt scored this file; every measured result below is new evidence on the
integrated artifact. Verbatim command/output for every run: `w2/Attack19/receipts.txt`; mutated
ledgers: `w2/Attack19/*.md` (base-ledger = `git show <base>:quality/tool-ledger.md` minus the
fenced doc block, lines 9–13 removed only).

## Falsifier F1 — production pass is impossible: the row parser is fence-blind

Attacked clause: `claims-frozen.md:7` "Demonstrate production pass and control fail at the
frozen revision"; `registration.md:7` "must pass on the existing production ledger at the base
revision".

Defect: `parse_ledger`/`cells` (`c1-r52-ledger.py:33-45`) have no fenced-block tracking. Any
3-cell pipe line with a backticked first cell is a "row" — including the ledger's own grammar
example inside a ``` block at `quality/tool-ledger.md:9-13`:

```
| `<repo-relative path>` | <one-line description> | `<pointer path>` or `<pointer path>:<line>` |
```

This parses to row (`<repo-relative path>`, `…`, `<pointer path> or <pointer path>:<line>`):
path is non-population (`dangling`), pointer target does not resolve (`bad_pointer`).

Reproduction (receipt §T1):

```
$ python3 -I quality/counters/c1-r52-ledger.py --repo <lane> --rev 85d57a8…
C1_R52: population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1
        self_pointer=0 generic_desc=0 verdict=TARGET_MISSED rev=85d57a8…  exit=1
```

`ledger_rows=83` vs. 82 real rows; the phantom is proven by deleting only lines 9–13, which
restores a clean pass (receipt §green baseline: `ledger_rows=82 … TARGET_MET`, exit 0). The
regression is measured against both predecessors: committed `check-tool-ledger.py:173-187`
(`unfenced()` — "a fenced row is documentation, not a ledger row") and `c1-r51-ledger.py:155-163`
(`fenced` toggle) both skip it; `C1Simplify.md` §2 measured this exact trap and called skipping
non-optional ("a naive parser counts 83 rows"). The integrated artifact re-introduced the naive
parse.

**Verdict: REPRODUCED — the green arm is falsified at the frozen revision.** The defect is
revision-independent: any ledger that documents its own grammar in a fenced example can never
pass this counter (the integration-state worktree ledger also fails at base: `ledger_rows=85
dangling=3 bad_pointer=3`, receipt §T1-note in commands).

## Falsifier F2 — the frozen control fails for schema shape, not self-pointer/context

Attacked clause: `registration.md:7` "fail on `controls/c1-do-nothing.md` specifically for
self-pointer/context defects".

Reproduction (receipt §T2):

```
$ python3 -I c1-r52-ledger.py --repo <lane> --rev 85d57a8… \
    --ledger .ufo/waves/round-52/controls/c1-do-nothing.md
C1_R52: population=82 ledger_rows=0 uncovered=82 dup=0 dangling=0 bad_pointer=0
        self_pointer=0 generic_desc=0 verdict=TARGET_MISSED  exit=1
```

The control's 4-cell, unbackticked rows are all dropped by `parse_ledger` (`len(c)==3` +
backtick guard), so `ledger_rows=0` and the only firing field is `uncovered`. `self_pointer`
and `generic_desc` are **0** — the counter cannot attribute the failure to either required
defect class. This reproduces the W1-predicted signature (`C1Evidence.md` §3: "a failure …
through malformed row shape and coverage"; `C1ControlAttack.md`: "schema/pointer parsing and
duplication, not a targeted demonstration"). `C1CounterDesign`'s draft closed this by scoring
wide rows and scanning all cells; the integrated artifact scores neither, so the draft's
`self_pointer=1 generic_desc=1` red receipt does not transfer to these bytes. For completeness
(receipt §T2b): `controls/c1-row-context-control.md` fires `generic_desc=2` but structurally
cannot fire `self_pointer` (its pointers name `PROVINCE.md`), and it is not the frozen control.

**Verdict: REPRODUCED — the red arm as scored is a coverage failure only; the "specifically for
self-pointer/context defects" requirement is not met.**

## Falsifier F3 — "population row uniqueness" is enforced only on well-formed rows

Attacked clause: `registration.md:7` "validates population row uniqueness"; ledger contract
`quality/tool-ledger.md:15` "listed exactly once".

Defect: `parse_ledger` silently discards any row failing the 3-cell/backtick grammar **before**
the `dup`/`by[]` bookkeeping (`c1-r52-ledger.py:43-44,51-55`). A second listing of an
instrument in malformed shape is invisible to the uniqueness check — it produces no `dup`, no
`dangling`, not even a `ledger_rows` increment.

Reproduction (receipts §F3, §F4 — production ledger minus fence plus one appended row each):

```
| tools/mado-verify.sh | Second unbackticked row naming a real document. | `PROVINCE.md:18` |
   → ledger_rows=82 dup=0 … verdict=TARGET_MET exit=0
| `tools/mado-verify.sh` | Second row with four cells. | `PROVINCE.md:18` | extra |
   → ledger_rows=82 dup=0 … verdict=TARGET_MET exit=0
```

Head-to-head on the same committed bytes (fixture repo `fix3`, 2 instruments, ledger = 2 clean
rows + 1 unbackticked duplicate of `tools/one.py`):

```
candidate:  C1_R52: population=2 ledger_rows=2 uncovered=0 dup=0 … verdict=TARGET_MET   exit=0
checker:    LEDGER-ROW reason=dangling path=tools/one.py detail=row-duplicate-line-5
            LEDGER: population=2 ledger_rows=3 … dangling=1 verdict=TARGET_MISSED
```

`check-tool-ledger.py`'s `norm_path` strips backticks before membership, so the contract gate
sees the duplicate; the candidate's grammar gate hides it. **Verdict: REPRODUCED — uniqueness
over ledger rows is unsound whenever the second listing is malformed.**

## Falsifier F4 — the counter's population diverges from the committed contract

Attacked clause: `claims-frozen.md:7`/`registration.md:7` "unique population" (the instrument
population the claim means is the committed checker's: `tools/` + `quality/*.py` direct +
`quality/counters/*.py` direct, blobs only — `check-tool-ledger.py:163-170`, `tree()` drops
non-blob entries at :136-149).

Two divergences in `population()` (`c1-r52-ledger.py:24-28`), each reproduced:

(a) `p.startswith("quality/counters/")` has no depth limit → nested
`quality/counters/deep/x.py` is counted; `COUNTERS_PY` in the checker requires a direct child.
Fixture `fix1` (2 tools + `quality/counters/deep/x.py`, ledger covers both tools):

```
candidate:  population=3 ledger_rows=2 uncovered=1 … TARGET_MISSED  exit=1
checker:    population=2 ledger_rows=2 uncovered=0 … TARGET_MET     exit=0
```

(b) `git ls-tree -r --name-only` is filtered by path only → gitlinks (`160000 commit`) are
counted as instruments; the checker's `tree()` keeps blobs only. Fixture `fix2` (1 tool +
gitlink `tools/submod`, ledger covers the tool):

```
candidate:  population=2 ledger_rows=1 uncovered=1 … TARGET_MISSED  exit=1
checker:    population=1 ledger_rows=1 … TARGET_MET                 exit=0
```

Both fixtures' toplevels were asserted (`git rev-parse --show-toplevel` prints in receipts).
**Verdict: REPRODUCED — on any revision containing a nested counters `.py` or a submodule, the
counter enforces a different population than the contract it claims to check.** (Dormant at
base — population happens to be 82=82 — but it is a latent falsifier of parity, and the
ER-11 requirement from W1 `C1Evidence.md` is unmet.)

## Falsifier F5 — non-self pointer defeated by the `./` spelling

Attacked clause: `registration.md:7` "non-self … evidence pointer".

Defect: the self test is the literal `target in (path, LEDGER)` (`c1-r52-ledger.py:56-57`)
after only `strip().strip("\`").split(":",1)[0]` — no path normalization (the checker's
`norm_path` strips `./`, :196-197). `git show rev:./quality/tool-ledger.md` resolves, so the
row's own bytes satisfy the basename clause and nothing flags self.

Reproduction (receipts; one production row's pointer swapped, everything else identical):

```
| `tools/mado-verify.sh` | <production description> | `./quality/tool-ledger.md` |
   → self_pointer=0 bad_pointer=0 … verdict=TARGET_MET exit=0
| `tools/mado-verify.sh` | <production description> | `./tools/mado-verify.sh` |
   → self_pointer=0 bad_pointer=0 … verdict=TARGET_MET exit=0
```

**Verdict: REPRODUCED — a literal self-pointer passes if spelled `./<path>`.**

## Reproduced — secondary arithmetic and grammar observations

- **Duplicate paths are double-charged** (`assess` :64, `uncovered` counts `by.get(p,0)!=1`):
  fixture `fix4` (2 tools + well-formed duplicate) → `dup=1 uncovered=1` while the checker
  reports the same bytes as `dangling=1 uncovered=0`. A duplicated path is reported as also
  missing; receipt arithmetic is wrong, though still a fail.
- **`ledger_rows` lies about table contents**: it counts only parsed rows, so receipts can
  print `ledger_rows=0` on a ledger with visible data rows (the frozen control). The
  committed checker counts all row-shaped lines and reports `row-malformed-cells-N-line-M`;
  the candidate has no malformed-row defect class at all — malformed rows are silent drops.
- **Pointer grammar is more lenient than the contract**: `target` needs no backticks
  (`strip("\`")` is unconditional), so `| \`tools/x.py\` | desc | PROVINCE.md |` parses and
  resolves as a pointer though `tool-ledger.md:12` requires a backticked path. The committed
  checker shares this leniency (`pointer_tokens` fallback), so it is parity-with-checker but
  weaker than the ledger's own grammar and the W1 reference's single-backticked-token rule.
- **`--selftest` is inert; no selftest exists**: the flag is parsed (`:68`) and never read.
  `--selftest` alone errors on required `--repo/--rev`; with them it runs the normal measure
  (receipt §selftest). `registration.md:7` "Selftest includes explicit red/green receipts" —
  no such receipts can be produced by this artifact. Adjacent to my lane; flagged, not
  developed.
- **Artifact not committed** (`??` in `git status`): "a new committed counter" is unmet at
  inspection time; noted for the integrator, not scored as a defect of the code.

## Limitations

1. The artifact is untracked and may still be rewritten; every verdict is bound to sha256
   `923faf02…`, not to "the eventual landed counter". If a later byte lands, these results do
   not transfer automatically (the two W1 drafts' receipts already do not).
2. Fixture repositories are minimal (1–3 instruments) by construction: they isolate one rule
   each. The divergences are unconditional code paths, so scale is not required for the
   mechanism, but no production-scale ledger with these defects was scored.
3. F1's falsifier depends on the ledger keeping a fenced grammar example; a preamble rewrite
   removing it would mask the parser defect (while leaving the generalization: any future
   3-cell, backtick-first prose table in the ledger doc becomes phantom rows — no fence check
   exists).
4. The `./` self-pointer bypass was demonstrated on this host's git (`git show rev:./path`
   resolves to the in-tree path). `rev:a/../b` spellings were not exercised; the
   normalization surface may be wider than demonstrated.
5. `generic_desc`/`context`-clause internals (the W1-signalled F3 counterfeit bypass) were not
   attacked here — assigned lane is population/row grammar; those items belong to sibling
   attacks.
6. All candidate/checker runs were read-only against git objects (`git ls-tree`, `git show`);
   fixture commits happened only inside scratch repos under
   `/fast/scratch/hyaku/mado-r52/Attack19/` with printed toplevel assertions. No tracked lane
   file was modified, no host/package/live surfaces were touched, no tools installed. Scratch
   removed after receipts were copied to this seat directory.

## Deliverables

- `.ufo/waves/round-52/w2/Attack19/receipts.txt` — verbatim commands, outputs, exit codes, fixture tree listings, artifact sha256.
- `.ufo/waves/round-52/w2/Attack19/base-ledger.md` — `git show <base>:quality/tool-ledger.md` minus lines 9–13 (green baseline).
- `.ufo/waves/round-52/w2/Attack19/mut-unbackticked-dup.md`, `mut-4cell-dup.md`, `mut-selfptr-dot.md`, `mut-selfptr-own.md` — single-defect ledger mutations of F3/F5.

Report: .ufo/waves/round-52/w2/Attack19.md
