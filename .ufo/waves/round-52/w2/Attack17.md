# Attack17 — C1 forged functional-phrase context bypass

Axes: **operability** (C1 only). No coverage claim touched; no axis moved. Attack wave
item: *C1 forged functional-phrase context bypass* — find a concrete falsifier of the
context clause, or verify the specified control. Verdicts below are measured, not judged
as non-author.

Scope at attack time: the frozen registration names `quality/counters/c1-r52-ledger.py`
as the draft target path and no r52 counter exists at base
(`git ls-tree -r --name-only 85d57a8 | grep -c c1-r52` → 0). Three candidate
implementations were measured, all at the frozen revision `85d57a818c3707397e21c840b6498b105ba798aa`:

- **DRAFT** — `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`, 847 lines,
  sha256 `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`. The
  W1 `C1CounterDesign` deliverable; strongest context surface (adjacent-word binding
  plus four filters: own-name, population vocabulary, path fragments, function words).
- **REF** — `.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py`, 194 lines,
  sha256 `0d31fc6c748c018752d76730c3f539fe1449c94ea6114eef4ec1821d3c298957`.
  The W1 simplifier's reference (raw adjacent-word binding, no filters).
- **STAGED** — `quality/counters/c1-r52-ledger.py` in the lane working tree, 78
  lines, sha256 `923faf02cd0c2db374f7757d38ef24fc8381c2882cb3d853882f0fadce1c17d7`.
  Untracked, uncommitted, byte-distinct from DRAFT. Its provenance is unclear — it
  is not the C1CounterDesign draft at its stated integration path — so it is
  attacked as a found object, not as a candidate deliverable.

## A1 (primary) — forged "functional-phrase" context bypass: reproduced, now closed on the strongest surface too

**Attacked clause** (claims-frozen.md C1): the counter distinguishes production from a
no-work control "using … instrument-specific context checks." The bypass premise (W1
signal: "C1 F3 counterfeit semantic-context bypass passed its draft"): a ledger whose
descriptions are generic boilerplate — carrying zero functional content — can satisfy
every implementation of the context clause by copying one adjacent word pair out of
each instrument's committed bytes.

**Construction** (`Attack17/forge.py`, deterministic; reads `git show` blobs only):
all 82 population rows, unique backticked path cells, every pointer cell copied
verbatim from the production ledger (so every pointer resolves and names its
instrument), and each description is the literal boilerplate

```
Generic accountability boilerplate line NNN cites <w1> <w2> verbatim.
```

where `<w1> <w2>` is the **last adjacent word pair in byte order** in that
instrument's own bytes that survives DRAFT's four filters. Every row's `<w1> <w2>`
exists (0 instruments lacked a candidate). The 82 plants reduce to only **8 distinct
bigrams**, all Python boilerplate, not instrument function:

| count | planted bigram | source |
|---|---|---|
| 32 | `exit main` | `sys.exit(main())` trailer |
| 32 | `exit 2` | `sys.exit(2)` error path |
| 6 | `argv 1` | `sys.argv[1]` slice |
| 4 | `systemexit main` | `SystemExit(main())` |
| 4 | `main main` | `main(main())` / `sys.exit(main())` normalisation |
| 2 | `sys argv` | `sys.argv` |
| 1 | `str exc` | `str(exc)` |
| 1 | `exit 1` | `sys.exit(1)` |

Example proof of occurrence: `quality/check-axis-scores.py` at base line 297 is
`    sys.exit(main())`; normalized, that yields the pair `exit main`, which the
forged row cites verbatim. Nothing in the description says what the instrument does.

**Exact reproduction** (run from any directory; read-only):

```
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=85d57a818c3707397e21c840b6498b105ba798aa
F=.ufo/waves/round-52/w2/Attack17/forged.md   # sha256 4dd20c7a…efec8

python3 -I $LANE/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py \
    --repo $LANE --rev $REV --work <scratch> --ledger $LANE/$F
python3 -I $LANE/.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py \
    --repo $LANE --rev $REV --ledger $LANE/$F
python3 -I $LANE/quality/counters/c1-r52-ledger.py \
    --repo $LANE --rev $REV --ledger $LANE/$F
```

To regenerate the artifact instead of reusing it:
`python3 -I .ufo/waves/round-52/w2/Attack17/forge.py` writes `forged.md` next to the
script (run it inside a scratch copy or edit `OUT`; it imports DRAFT for the filter
logic and shells out to `git show`).

**Observed results** (this seat's runs, verbatim):

| input | DRAFT | REF | STAGED |
|---|---|---|---|
| production ledger at `85d57a8` | `population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET` exit 0 | identical fields, `LEDGER52:` prefix, exit 0 | `population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED` exit 1 |
| `Attack17/forged.md` | `population=82 ledger_rows=82 uncovered=0 … generic_desc=0 verdict=TARGET_MET` exit 0, **0 detail lines** | identical, exit 0 | `population=82 ledger_rows=82 uncovered=0 … generic_desc=0 verdict=TARGET_MET` exit 0 |
| frozen `controls/c1-do-nothing.md` | `uncovered=81 dup=1 self_pointer=1 generic_desc=1 verdict=TARGET_MISSED` exit 1 | `uncovered=82 dangling=2 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED` exit 1 | `population=82 ledger_rows=0 uncovered=82 … self_pointer=0 generic_desc=0 verdict=TARGET_MISSED` exit 1 |
| W1 `C1Simplify/control-F3-forged.md` | `generic_desc=10 verdict=TARGET_MISSED` exit 1 | `generic_desc=0 verdict=TARGET_MET` exit 0 | `generic_desc=0 verdict=TARGET_MET` exit 0 |
| W1 `C1Simplify/control-H-minimal-forgery.md` | `verdict=TARGET_MET` exit 0 | `verdict=TARGET_MET` exit 0 | `verdict=TARGET_MET` exit 0 |

**Outcome — verdict: REPRODUCED (bypass stands).** A ledger that is self-declared
generic boilerplate is scored `TARGET_MET` with `generic_desc=0` on every counter
written this round, including the strongest. The W1 signal that "F3 passed its draft"
needs one correction: on the final DRAFT the original F3 fixture now *fails*
(`generic_desc=10`, `bound-only-by-name-path-or-function-words`), because F3 planted
name/path-vocabulary phrases (`mado action plan py`, `usr bin`, `pred c1`). My F3x
closes that hole by planting content bigrams (`exit main`, `sys argv`) that are
inside the instrument's bytes but are shared lane boilerplate — the draft's four
filters are precisely blind to them: not own-name, not population-vocabulary
(`exit`, `main`, `argv`, `sys` appear in no instrument path), not path fragments
(no `/`), not all-function-words. The bypass is therefore not narrowed by the draft's
extra filters; it is completed by them.

Clause-level reading (not a vote): the frozen predicate's *mechanism list* — unique
population, resolvable non-self pointer, plus a context description — is satisfiable:
DRAFT fires `self_pointer=1` and `generic_desc=1` on the frozen control and
`TARGET_MET` on production. But the "instrument-specific context" clause in the
wording cannot claim instrument specificity: F3x shows the check measures
*description-to-source adjacency of one word pair*, and a pair identical across ~40%
of the population passes. Any C1 receipt should state the signal in those bounded
terms (this agrees with, and strengthens, C1Simplify §6/§7 and C1Evidence ER-12:
"lexical context signal … not semantic entailment", "context check's false-accept
exposure is stated").

**Limitations:** the forgery assumes the attacker may copy instrument bytes (all
ledger authors can; the check is lexical by design). It does not touch the
population/pointer/dup clauses — F3x keeps real pointers precisely to isolate the
context clause. No claim made on whether a *different* context check (e.g., n-gram
uniqueness against the whole population) could be forged; this item attacks the
clause as built in all three candidate implementations.

## A2 (secondary) — the frozen control is isolating on exactly one of the three surfaces

The W1 signal "C1 control does not isolate required defects if schema shape causes
failure" is **reproduced and extended**:

- On REF, the frozen control yields `dangling=2` (4-cell rows rejected) +
  `uncovered=82`; `self_pointer=0`, `generic_desc=0` — neither required defect is
  exercised at all.
- On STAGED, `ledger_rows=0`: its parser requires a backticked first cell on a
  3-cell row, and the frozen control's first cell `tools/mado-verify.sh` is
  un-backticked and the row has 4 cells — every row is skipped → `uncovered=82`
  only; again neither required defect is exercised.
- Only DRAFT scores the 4-cell row and fires both `self_pointer=1` and
  `generic_desc=1` (plus `dup=1`, `uncovered=81`). The frozen registration's red
  case — "fail … specifically for self-pointer/context defects" — therefore depends
  entirely on adopting DRAFT's wider row reading; on the other two surfaces the same
  red verdict is produced by population/shape failure alone and cannot corroborate
  either defect clause.

## A3 (incidental, reported per "report all errors") — the found STAGED file fails the green case itself

Independent of the bypass, the untracked `quality/counters/c1-r52-ledger.py` (78-line
implementation) has three defects, all measured at `85d57a8`:

1. **Fails production.** `ledger_rows=83, dangling=1, bad_pointer=1` on the real
   ledger: `parse_ledger` has no fence tracking, so it ingests the ledger's own
   fenced grammar example `| \`<repo-relative path>\` | … |` as a row; the fake path
   is dangling and its pointer unresolvable. The "pass on the existing production
   ledger at the base revision" premise cannot be demonstrated by these bytes.
2. **Red case tests nothing new.** `ledger_rows=0` on the frozen control (un-backticked
   first cell ⇒ every row skipped); the fail arrives only via `uncovered=82`.
3. **`--selftest` is a no-op.** `--selftest --repo <lane> --rev 85d57a8` ran the
   normal assessment and printed `verdict=TARGET_MISSED` exit 1 — the flag is parsed
   (line 68) and never consulted. The registration requirement "Selftest includes
   explicit red/green receipts" is unmeetable by these bytes.

Also noted for the integrator: an uncommitted `quality/tool-ledger.md` worktree edit
adds rows for `c1-r52-ledger.py`/`c2-r52-proposition-entry.py`; scoring that
*worktree* ledger at `--rev 85d57a8` would produce `dangling=2` (both counters are
absent from the base tree). Any green receipt must score the ledger blob at the
revision, not the working tree — all runs in this report already do.

## Environment, safety, limitations

- Host/lane: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` →
  `85d57a818c3707397e21c840b6498b105ba798aa` (= frozen base); `rev-parse --show-toplevel`
  → the lane root itself. No git/jj mutation anywhere; all counter runs read via
  `--rev` + `git show`/`ls-tree` only. No package queries, installs, live reads,
  probes, screenshots, or host mutations. Scratch `/fast/scratch/hyaku/mado-r52/Attack17`
  held `forge.py`, `forged.md`, `work/`; cleaned after copying artifacts into the
  seat dir.
- What I did **not** do: judge claim pass/fail (that is the planner's call, not a
  wave-2 attack seat's), mutate the lane, run the 455 MB fixture harness, or touch
  C2 surfaces.
- Artifact digest: `forged.md` sha256
  `4dd20c7a863b0a98e84482a4bf882d297fea02ae71f2e7e087b9c392194fefc8`
  (`Attack17/forged.sha256`, `Attack17/forge.py` regenerates it deterministically).

## Artifacts

- `.ufo/waves/round-52/w2/Attack17/forged.md` — the bypass ledger (82 rows).
- `.ufo/waves/round-52/w2/Attack17/forge.py` — deterministic generator.
- `.ufo/waves/round-52/w2/Attack17/forged.sha256` — digest.

Report: `.ufo/waves/round-52/w2/Attack17.md`
