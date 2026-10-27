C1CounterDesign — prototype counter + selftest for the frozen C1 ledger predicate

status: COMPLETE (draft only; nothing tracked was edited — the lane's tracked tree is
byte-identical, `git diff --name-only` empty and `git status --porcelain` shows only the
untracked round-52 wave directory that holds this seat)

## Deliverables

- `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py` — the prototype counter and
  its `--selftest` (847 lines, sha256 `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`)
- `.ufo/waves/round-52/w1/C1CounterDesign/fixtures/hole-probes.py` — six single-defect
  ledger mutations the counter must reject (178 lines, sha256
  `f5ecb96fbfa2e0379e5a5df765981d60f367f9a0d96a5c0c309028ea30aaf0f8`)
- `.ufo/waves/round-52/w1/C1CounterDesign/fixtures/receipts.sh` — the receipt generator
  (every command and its exact output)
- `.ufo/waves/round-52/w1/C1CounterDesign/receipts/receipts.txt` — the receipted runs
- `.ufo/waves/round-52/w1/C1CounterDesign/receipts/hole-probes.txt` — the five hole probes
- `.ufo/waves/round-52/w1/C1CounterDesign/receipts/harness-summary.json` — the
  `C1Fixture` harness verdict over this counter (5/5 cases `ok=True`, `lane_unchanged=true`)

Draft target path for integration: `quality/counters/c1-r52-ledger.py`
(847 lines, sha256 `0fe862f1…`). Integration is the L1's call; nothing was committed.

Byte history of this draft, for the record: `c0291662` → `39e3d1f4` (create a
caller-named `--work` rather than rejecting it) → `eb508569` (the non-self scan stops
firing on a row that designates an accountable document, which fixes a false positive on
an honest description that names the ledger) → `382a0606` (the context clause closes the
two escapes the peer seat demonstrated) → `701b497d` (the non-self charge now keys on the
pointer region itself, closing the laundering hole the peer seat then found) →
`0fe862f1` (the pointer's spelling of the ledger is pinned by three new selftest
cases: the relative path form, the line-anchor form, and the row's own path). The
receipts in this directory are regenerated from `0fe862f1`; earlier receipts in my
messages refer to the earlier bytes.

## What the counter measures

`python3 -I c1-r52-ledger.py --repo <lane> --rev <rev> --work <scratch> [--ledger <file>]`

Every byte comes from `--rev`; the working tree is never read. The population is derived
independently of the ledger — one `git ls-tree -r --name-only <rev>` listing, filtered to
every file under `tools/` plus the direct children `quality/*.py` and
`quality/counters/*.py` (`__pycache__`/`*.pyc`/`*.pyo` excluded). At the frozen base
`85d57a818c3707397e21c840b6498b105ba798aa` that is **P=82**, independently reproduced.

Summary line (always last, always the same fields):

```
C1_R52: population=<P> ledger_rows=<R> uncovered=<n> dup=<n> dangling=<n> bad_pointer=<n> \
self_pointer=<n> generic_desc=<n> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>
```

Exit 0 = TARGET_MET, 1 = TARGET_MISSED, 2 = setup error.

## The four frozen C1 clauses, and how each is measured

| frozen clause | field | rule |
|---|---|---|
| population row uniqueness | `dup` / `uncovered` | each population path has exactly one row; a repeated path is `dup`, a missing one is `uncovered` |
| resolvable evidence pointer | `bad_pointer` | a target in the pointer region (the ledger's own cell 3) must exist at `--rev` and name the row file's basename **as a name** (name-bounded, not a substring), and must not be a peer instrument |
| non-self pointer | `self_pointer` | the accountability pointer (cells 3 and after) names the ledger under test (`quality/tool-ledger.md`) or the row's own path; or the row designates no accountable target at all and any cell names one of those |
| instrument-specific functional context | `generic_desc` | the description must share a two-word phrase with the instrument's own bytes at `--rev` that is not made of the instrument's own path words, not of the population's naming vocabulary, not a filesystem-path fragment, and not made only of English function words |

Three design decisions that matter, and why:

1. **A row wider than three cells is scored, not discarded.** The frozen do-nothing control
   is a four-cell table (`| Tool | Reads | Writes | Owner |`). A counter that rejected
   four-cell rows as malformed could never name the control's defect — it would only ever
   report a coverage miss. This counter scores the row and prints an informational
   `note path=… cells=4` alongside the defect lines.
2. **The non-self charge keys on the pointer region itself, with a wider fallback.**
   *If the ledger or the row's own path is named in the pointer region (cells 3 and
   after), the accountability claim is circular* — whatever else the row names. This is
   unconditional, so a second accountable document cannot launder a circular pointer
   (the laundering hole the `C1Fixture` peer seat found against my earlier narrowing:
   their N4/N5/N7 probes all now read `self_pointer=1`). *If the ledger is named only
   elsewhere in the row*, the charge fires only when the row designates no accountable
   target at all — that is what the frozen control needs, since it names the ledger in
   its Reads cell. A row that designates an accountable document and merely mentions the
   ledger in prose is recorded as `note path=… names-the-ledger-in-prose` and not scored,
   which is what lets `C1Simplify`'s `control-G-legit-ledger-reader.md` — the very tool
   whose job is to read the ledger — score `TARGET_MET`.
3. **The context clause is phrase binding with four filters.** A bound phrase only counts
   as functional context if it is not (a) the instrument's own name words, (b) the
   population's naming vocabulary, (c) a filesystem path in the instrument's bytes, or
   (d) made only of English function words. Filters (a), (c) and (d) close the two
   escapes the `C1Fixture` peer seat demonstrated against my earlier draft (a semantically
   empty description quoting `usr bin`, and one quoting the lane's naming vocabulary);
   both are now `generic_desc=1`.

## Green and red at the frozen revision

Green — the production ledger at the base:

```
$ python3 -I c1-r52-ledger.py --repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa --work <scratch>
C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET rev=85d57a818c3707397e21c840b6498b105ba798aa
exit=0
```

Red — the frozen control, scored in place of the ledger:

```
$ python3 -I c1-r52-ledger.py --repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa --work <scratch> \
    --ledger <lane>/.ufo/waves/round-52/controls/c1-do-nothing.md
detail: self_pointer path=tools/mado-verify.sh target=quality/tool-ledger.md
detail: note path=tools/mado-verify.sh cells=4
detail: generic_desc path=tools/mado-verify.sh reason=no-instrument-specific-phrase
detail: dup path=tools/mado-verify.sh already-seen
detail: uncovered path=quality/check-axis-scores.py
… (8 uncovered paths listed, 73 more not listed)
C1_R52: population=82 ledger_rows=2 uncovered=81 dup=1 dangling=0 bad_pointer=0 self_pointer=1 generic_desc=1 verdict=TARGET_MISSED rev=85d57a818c3707397e21c840b6498b105ba798aa
exit=1
```

The control fails **with both named defect signals** (`self_pointer=1`,
`generic_desc=1`), not only on coverage — which is what the frozen registration asks for
("fail … specifically for self-pointer/context defects").

## Self-test

`python3 -I c1-r52-ledger.py --selftest --work <scratch>` builds a throwaway three-instrument
git repository under `--work` (asserting `git rev-parse --show-toplevel` prints the fixture
dir before any commit) and asserts **53 named checks**, including a fixed-count guard so a
silently dropped case fails the run:

```
C1_R52_SELFTEST: 53/53 passed
exit=0
```

Covered: green fixture clean on all eight fields; self-pointer at the ledger; self-pointer
at the row's own path; generic ("does things.") description; path-name-only description;
path-fragment description (the `usr bin` escape); name-laundered description (the
`c1 r49 tools mado` escape); peer-instrument pointer; unresolvable pointer; duplicate row;
dangling row; uncovered row; an honest row whose description names the ledger (must pass);
a laundered self-pointer (the pointer names the ledger **and** an accountable document)
and the same laundering split across two cells; the ledger spelled as a relative path
(`./quality/tool-ledger.md`), as a line anchor (`quality/tool-ledger.md:1`) and as the
row's own path alongside an accountable document; and the frozen control's four-cell
shape (self-pointer **and** context defect).

## Cross-checks against sibling work

- **The laundering probes the `C1Fixture` peer seat built against my earlier narrowing**
  (their N4/N5/N7/N8) are now closed, each measured on the real production ledger with
  one row replaced: a pointer cell naming the ledger **and** an accountable document →
  `self_pointer=1` exit 1; the same split across two cells → `self_pointer=1` exit 1; the
  minimal form → `self_pointer=1` exit 1; and the variant whose second document does not
  name the instrument → `self_pointer=1` exit 1.
- **`C1Fixture` harness** (`--counter` this file): `HARNESS: verdict=PASS cases=5`,
  `lane_unchanged=True`. All five cases `ok=True` — green TARGET_MET/exit 0; red
  TARGET_MISSED/exit 1 with both `self_pointer` and `generic_desc` non-zero;
  `mut-selfptr` → `self_pointer=1`; `mut-generic` → `generic_desc=1`; `mut-duprow` →
  `dup=1`. The harness reads only stdout/stderr/exit and never the counter's source.
  `C1Fixture` re-ran the harness against my bytes independently (not taking my report)
  and additionally ran four probes of their own against **row 83**
  (`quality/counters/c1-r49-keysym.py`, not the first row their `mut-*` fixtures touch),
  each with different wording: P1 self-pointer **and** generic description →
  `self_pointer=1 generic_desc=1`; P2 generic description with a legitimate cell-3
  pointer → `self_pointer=0 generic_desc=1`; P3 rich specific description with a
  self-pointer → `self_pointer=1 generic_desc=0`; P4 self-pointer in the *description*
  cell with a legitimate cell-3 pointer → `self_pointer=1 generic_desc=0`. P2/P3 show the
  two signals are separated rather than conflated; P4 confirms the wider self-pointer
  scan. They also grepped my bytes and confirmed the control-shaped literal appears only
  in my own `--selftest` constant and that the counter never reads the control file.
  Their harness reads my `generic_desc` **count**, so it structurally cannot see a
  semantically empty description that my counter accepts with `generic_desc=0` — which
  is how they found the two escapes above by hand. Their final confirmation pass re-ran
  the whole control set against the shipped bytes (B `self_pointer=82 generic_desc=82`,
  C `82/0`, D `0/82`, E `1/0`, F3 `0/10`, G `TARGET_MET`, H `TARGET_MET`) and worked out
  the F3 mechanism described in the ceilings below.
- **`C1Simplify` controls** (read-only, their seat dir): B (row self-pointers + repeated
  generic descriptions) → `self_pointer=82 generic_desc=82`; C (every pointer = the ledger)
  → `self_pointer=82`; D (production pointers + repeated generic descriptions) →
  `generic_desc=82`; E (exactly one self-pointer) → `self_pointer=1`;
  `control-F3-forged.md` → `generic_desc=10` (**the reference implementation passes F3;
  this counter rejects it** — see the ceiling note below);
  `control-G-legit-ledger-reader.md` (an honest row whose description names the ledger)
  → `TARGET_MET`, which it was not before the non-self scan was narrowed — with the
  `note path=quality/check-tool-ledger.py names-the-ledger-in-prose` line, which is
  kept in the receipts so the two senses of the self-reference stay visible;
  `control-H-minimal-forgery.md` (a single row forged as `PRED-C1-r47 does things.`)
  → `TARGET_MET`, which is the disclosed ceiling below, receipted rather than hidden.
- **The two escapes the `C1Fixture` peer seat demonstrated against my earlier draft** are
  now closed, each measured on the real production ledger with one row replaced:
  `| quality/counters/c1-r49-keysym.py | usr bin and nothing else at all here okay. |`
  → `generic_desc=1` (reason `bound-only-by-name-path-or-function-words`), and
  `| quality/counters/c1-r49-keysym.py | c1 r49 tools mado keysym and nothing more here okay. |`
  → `generic_desc=1`.

## Six hole probes (all rejected)

`fixtures/hole-probes.py` starts from the production ledger and injects exactly one defect
class per probe; each must exit 1 with the expected signal non-zero.

```
HOLE_PROBES: 6/6 rejected
```

| probe | expected signal | result |
|---|---|---|
| every pointer = `quality/tool-ledger.md` | `self_pointer` | `self_pointer=82`, exit 1 |
| every pointer = the row's own path | `self_pointer` | `self_pointer=82`, exit 1 |
| one pointer = a sibling instrument's file | `bad_pointer` | `bad_pointer=1`, exit 1 |
| every description = the next row's description | `generic_desc` | `generic_desc=15`, exit 1 |
| every pointer = one shared omnibus file | `bad_pointer` | `bad_pointer=22`, exit 1 |
| one pointer names the ledger **and** an accountable document | `self_pointer` | `self_pointer=1`, exit 1 |

The driver's scoring line is `ok = proc.returncode == 1 and value is not None and value not in
("0", "absent")` — a probe passes only on **exit 1 *and* the expected field present and
non-zero**, so a driver that only checked the exit code would be worthless. The peer seat
proved that property by **substitution**: the same driver and the same six probes against
a scratch counter that accepts every ledger (always `verdict=TARGET_MET`, exit 0) report
**all six FALSE-GREEN, `HOLE_PROBES: 0/6 rejected`, exit 1**. The driver therefore
discriminates in both directions, not merely against the subject under test.

The third and fifth probes were **false greens before I added the peer-instrument pointer
clause**: a peer tool's source may name a sibling basename in passing, and one shared file
may name many basenames. Both are green-safe to reject — the production ledger has **zero**
pointer cells that target a population instrument (measured: 82/82 pointer cells are one
backticked document path; 12 distinct targets, all documents).

## Ceilings and limits, honestly

1. **The context clause is lexical binding, not context detection, and the mechanism of
   its residual is measured.** It closes the two escapes
   the `C1Fixture` peer seat demonstrated against my earlier draft — a semantically empty
   description quoting a filesystem path fragment (`usr bin and nothing else at all here
   okay.`) and one quoting the lane's naming vocabulary (`c1 r49 tools mado keysym …`) are
   now `generic_desc=1` each — but it cannot close the class. A description that quotes
   **any** real phrase from the instrument's bytes still passes: measured, the row
   `| quality/counters/c1-r47-terminal.py | PRED-C1-r47 does things. | SCORECARD.md:2660 |`
   is accepted, because `pred c1` is a genuine two-word phrase in that file. No lexical
   rule can exclude it without also excluding the production descriptions, which begin
   with the same prediction id. The claim is bounded this way ("bounded accountability
   checks, not prose entailment"), and this is the residual a wave-2 critic should push.
   `C1Simplify`'s `control-F3-forged.md` is now rejected on **10 of 82** rows (it was 7
   before the four filters); the other 72 still pass.

   **The mechanism, worked out with the counter's own helpers.** The ten rows that *are*
   rejected are exactly the rows whose filler is built only from that instrument's own path
   words — e.g. for `tools/mado-action-plan.py`, the description `Generic accountability
   note 0 mado action plan py.` binds only `mado action`, `action plan`, `plan py`, and
   all three are made of the instrument's own name, so none survives. The other 72 bind a
   *functional* phrase lifted from the instrument's own header — for
   `tools/mado-anims.py`, `static resolver` and `resolver for` survive because that is
   genuinely what the tool's own bytes say. Those phrases are exactly the vocabulary an
   honest description would use, so no purely lexical rule can separate them. The same
   mechanism produced the peer's independent sweep (replacing each production row's
   description with `pred c1 does things for the widget registry`: caught 59, accepted 23
   — the 23 being the instruments whose own bytes contain `pred c1`). One mechanism, two
   measurements. The wave-2 critic's attack to aim at is therefore precise: copy a real
   functional phrase out of the instrument's own bytes into a description that says nothing
   about the function. `control-H-minimal-forgery.md` is the minimal instance and is the
   right artifact to leave behind.
2. **Production margin on the context clause is thin.** Two of the 82 production rows
   (`quality/counters/c1-r47-terminal.py`, `quality/counters/c2-r51-dispatch-entry.py`)
   survive on exactly one qualifying phrase, and that phrase is their prediction id.
   Measured: every production row has at least one surviving phrase and none has zero, so
   the base is green; but a reworded description for those two rows could tip them. The
   failure would be visible and actionable — the detail line names the reason.
3. **The context clause is anchored on the instrument's whole file, not its header.** I
   measured a header-only variant: it fails 80 of 82 production rows, so it is not usable.
   The path-word exclusion is what makes the whole-file anchor usable.
4. **No document-frequency cutoff.** Measured: any DF cutoff below 25 fails at least three
   production rows, so no distinctiveness-by-frequency rule is used. The one hand-written
   vocabulary in the counter is the closed-class list of English function words (filter
   (d)); the other three filters are derived from the tree and from the instrument's own
   bytes.
5. **The pointer check requires the basename to appear in the target's bytes, name-bounded.**
   A target that names the instrument in a comment still counts. That is the same licence
   the r51 gate gave; it is not a strengthening.
6. **The peer-instrument clause assumes a tool is not accountable for a sibling tool.** If
   the lane ever wants a tool's own file to be its accountability record, this clause must
   be revisited. It is green-safe today (0 production rows).
7. **The counter does not cross-check against `quality/check-tool-ledger.py`, and the two
   gates are independent.** The r51 counter required the lane's own gate to agree
   numerically; this draft does not, because the gate's `LEDGER:` line has no
   `self_pointer` or `generic_desc` field to agree on. **Field ownership:** the round-51
   gate owns `population`, `ledger_rows`, `uncovered`, `dangling`, `bad_pointer`,
   `empty_desc`; this counter owns the same population/coverage fields plus `dup`,
   `self_pointer` and `generic_desc`; neither constrains the other's verdict. This is
   stated in the receipts (`## GATE OWNERSHIP`) so a reader of a receipt cannot mistake
   one gate's fields for the other's. Integration must either extend the gate with the two
   new fields (to allow a cross-check clause) or let this counter stand alone — a
   decision for the L1, not a defect of this draft.
8. **`self_pointer` has two senses after the narrowing**, and both are visible in the
   receipts: a scored `self_pointer` defect (the row has no accountable pointer and its
   only accountability claim is circular), and an unscored
   `note … names-the-ledger-in-prose` line (the row designates an accountable document
   and merely mentions the ledger in its description). The note line is kept in
   `receipts/receipts.txt` so a reader of the receipt can tell the two apart.
9. **`--work` is validated and created if absent, but nothing is written into it** in
   measurement mode (the counter needs no scratch: `git show` reads committed bytes
   directly). The `--selftest` mode does build a throwaway repository under `--work` and
   removes it on exit. The `/tmp`, `/var/tmp` and `/dev/shm` roots are refused. A
   caller-named path that does not exist yet is created rather than rejected, so a driver
   that passes a fresh scratch path is not punished for it (pointed out by `C1Fixture`,
   who noted their harness's own scratch-confinement check would otherwise see exit 2).

## Scratch and hygiene

- Scratch: `/fast/scratch/hyaku/mado-r52/C1CounterDesign/` (fixture work dir, probe
  scratch, harness work/out trees, measurement scripts) — **deleted at the end of this
  seat**; the receipts above are the retained evidence.
- Disk guard checked before the heavy passes: `/fast/scratch` 26% used, 600 G free.
- No tool installed or upgraded; no pacman transaction; no package query; no live read;
  no compositor socket, host service or config plane touched. The round is source-only and
  this seat stayed inside it.
- Lane tracked tree unchanged: `git diff --name-only` empty, `git status --porcelain` shows
  only `?? .ufo/waves/round-52/`. The `C1Fixture` harness independently recorded
  `lane_unchanged=true` over the same window.
- Every write is inside this seat directory. A `__pycache__/` byproduct (a peer seat
  importing this module to reuse its filter helpers) was removed; the seat directory holds
  only the six declared files.

Report: .ufo/waves/round-52/w1/C1CounterDesign.md
