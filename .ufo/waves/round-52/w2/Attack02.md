# Attack02 — W2 attack on C1 pointer self-reference laundering

Seat: `Attack02` (critic, leaf — no subagent dispatch). Wave: w2, round 52, lane `mado-shokunin`.
Axes named: **operability** (C1 only; no coverage move). This is an attack on the frozen C1
predicate and the W1 draft counter's self-pointer mechanism, not a vote and not a predicate
amendment. No non-author judgment is claimed; integration decisions belong to L1.

## Frozen clauses attacked

- `claims-frozen.md` C1: target distinguishes the production ledger from a no-work control
  of repeated generic self-pointers "using unique population, **non-self resolvable
  evidence targets**, and instrument-specific context checks … Claim is limited to bounded
  accountability checks, not prose entailment."
- `registration.md` C1 (frozen predicate): the new counter "validates population row
  uniqueness, **resolvable evidence pointer, non-self pointer**, and a description
  containing instrument-specific functional context," passes the production ledger at
  base, and fails `controls/c1-do-nothing.md` "**specifically** for self-pointer/context
  defects."
- Sub-clause under direct attack: the `self_pointer` mechanism of the W1 draft counter
  `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`
  (sha256 `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`, 847 lines).

## Method

Concrete tests only, all reproducible from `Attack02/run-probes.sh` (fixture driver) with
the verbatim transcript in `Attack02/transcript.txt`. Predictions were pre-registered in
`Attack02/PREDICTIONS.md` before any probe ran; every prediction matched the observed
result.

Two harnesses:

1. **Fixture repo** (scratch, 3-instrument population `tools/alpha.py`, `tools/beta.sh`,
   `quality/gamma.py` + documents), one commit per probe, counter invoked as
   `python3 -I c1-r52-ledger.py --repo <fixture> --rev <probe-sha> --work <scratch>`.
   Before every fixture mutation the driver asserts `git rev-parse --show-toplevel`
   prints the fixture dir (host guard).
2. **Real lane at the frozen base** `85d57a818c3707397e21c840b6498b105ba798aa`,
   read-only (`git show`/`git ls-tree` only), for the green arm and the frozen-control arm.

Mechanism under test (counter source, `measure()` lines 346–383 and `path_tokens()` lines
231–245): a row is charged `self_pointer` only when a token emitted by `path_tokens` from
the pointer region (cells 3+) — or, when the row names no accountable target, from any
non-path cell — is **exactly equal** to `quality/tool-ledger.md` or the row's normalized
own path, and the token contains `/`. `path_tokens` strips backticks, `#fragment`, a
leading `./`, and a numeric `:N`/`:N-M` suffix. It does not fold case, collapse repeated
slashes, strip other punctuation, recognize basenames, or inspect git file mode.

## Reproduced verifications (W1 claims confirmed on these bytes)

| probe | reproduction | observed | verdict |
|---|---|---|---|
| P01 green arm | counter at `--repo <lane> --rev 85d57a8…` | `population=82 ledger_rows=82` all fields 0 `TARGET_MET` exit 0 | **reproduced** (matches `receipts/c1-base.txt` field-for-field and W1 reports) |
| P02 frozen control | `--ledger .ufo/waves/round-52/controls/c1-do-nothing.md` | `self_pointer=1 generic_desc=1 … TARGET_MISSED` exit 1; both named defect signals present | **reproduced** — the control fails *specifically* for the two defect classes |
| P15 closed-hole regression | pointer `` `quality/tool-ledger.md` and `docs/alpha.md:1` `` | `self_pointer=1 … TARGET_MISSED` exit 1 | **reproduced** — the W1-closed laundering hole (full-path + accountable doc) stays closed |
| P16 selftest | `--selftest` | `C1_R52_SELFTEST: 53/53 passed` exit 0 | **reproduced** |
| P17 population arithmetic | `git ls-tree -r --name-only 85d57a8…` filtered by the lane's population rule | 82 population paths, 0 `c1-r52` paths at base | **reproduced** — committing the counter at `quality/counters/c1-r52-ledger.py` raises the population to 83 and its own ledger row must name it (C1Evidence ER-11 burden; observed again here as working-tree sibling edits add exactly those rows) |

## Attack findings — the non-self clause is defeated by reference spelling (concrete falsifiers)

Each probe below puts a circular accountability claim in the pointer region of a row that
also names a legitimate accountable document (`docs/alpha.md`, whose bytes name
`alpha.py`). Each row therefore passes end-to-end (`TARGET_MET`, exit 0) while the row's
pointer region names the ledger itself or the instrument's own file. Attacked clause in
every case: "non-self resolvable evidence targets" / "non-self pointer".

| probe | pointer cell of `tools/alpha.py` row | observed | verdict |
|---|---|---|---|
| P03 | `` `tool-ledger.md` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (bare ledger basename; token has no `/`) |
| P04 | `` `alpha.py` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (row's own basename) |
| P05 | `` `./tool-ledger.md` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (`./` stripped, basename remains) |
| P06 | `` `quality/tool-ledger.md)` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (trailing `)` inside backticks breaks exact equality) |
| P07 | `` `quality/tool-ledger.md:x` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (non-numeric suffix not stripped by `LINE_SUFFIX`) |
| P19 | `` `quality//tool-ledger.md` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (double slash not collapsed) |
| P20 | `` `/quality/tool-ledger.md` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (leading slash not normalized) |
| P21 | `` `Quality/tool-ledger.md` and `docs/alpha.md:1` `` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering** (case not folded; also not a resolvable path, yet the row stays green because the second token is the accountable doc) |
| P09 | `` `docs/alpha-evidence.md` `` where that path is a **git symlink** (mode 120000) to `../tools/alpha.py` | `self_pointer=0 … TARGET_MET` | **not reproduced — laundering via git-mode blindness** (symlink blob content `../tools/alpha.py` names the basename → counted an accountable document; the counter never checks file mode, so a pointer to the instrument's own file through a symlink alias is "non-self, resolvable") |

Nine distinct shapes, all `TARGET_MET`. The frozen control's defect (P02) is caught only
because its bytes happen to use the exact full path `quality/tool-ledger.md`; the
self-pointer mechanism is an exact-string-equality test, not a self-reference test.

Additional misclassification evidence (defect caught but reported under the wrong field,
which bears on the "specifically for self-pointer/context defects" requirement):

| probe | shape | observed |
|---|---|---|
| P08 | `` `tool-ledger.md` `` alone (no second doc) | `bad_pointer … reason=no-target-names-the-instrument`, `self_pointer=0` — a self-pointer reported as an unresolvable pointer |
| P10 | `` `docs/ledger-copy.md` `` (symlink → `../quality/tool-ledger.md`) | `bad_pointer=1` — caught only because the symlink text lacks the basename; the ledger alias itself is not recognized as self-reference |
| P11 | frozen-control 4-cell shape with **bare basename** `tool-ledger.md` in Reads | `bad_pointer=1 generic_desc=1`, `self_pointer=0` — the same control semantics fail **without** naming the frozen self-pointer defect class |
| P12 | identical 4-cell shape with **full path** `quality/tool-ledger.md` in Reads | `self_pointer=1 generic_desc=1` — attribution flips purely on path spelling |

P11/P12 is the same confound family W1's `C1ControlAttack` raised for schema shape,
applied to the signal itself: the "specific self-pointer defect" attribution is contingent
on the control's exact bytes, one spelling variant away from being lost.

## Predicate gaps measured (claim-level limitations, not counter defects)

The frozen predicate asks for non-self, resolvable, basename-naming evidence. Two
no-work ledgers satisfy it exactly and pass green:

- P13 **evidence cycle**: row `alpha` → `docs/beta-cycle.md` (names `alpha.py`), row
  `beta` → `docs/alpha-cycle.md` (names `beta.sh`). Each target is a document, resolvable,
  names the row's basename, non-self. `TARGET_MET`. The evidence is circular across rows.
- P14 **shared registry**: one `docs/registry.md` naming all three basenames; every row
  points at it. `TARGET_MET`. This is the round-51 "any file containing the basename"
  residual transplanted to a non-population file: the counter excludes only the ledger,
  the row's own path, and peer instruments from "accountable".

Both are bounded by the frozen claim's own wording ("bounded accountability checks, not
prose entailment"), so they do not falsify the claim as frozen; they mark where the claim
stops. The C1 receipt must state them in those words, and a wave-3 mutation seat should
treat registry/cycle shapes as the pointer-side analogue of the F3 counterfeit
semantic-context bypass that passed the context clause's draft (W1 signal, context side).

## Smallest safe correction

Keep the check structural (no prose entailment); close the identity hole:

1. Compare pointer tokens against the ledger and the row's own path by **normalized
   identity**, not exact string equality: strip leading `/`, collapse repeated slashes,
   fold case for the comparison, cut non-numeric suffixes, and treat an unambiguous bare
   basename (`tool-ledger.md`, and the row's own basename) as a self-reference when it
   appears in the pointer region. (Base-tree note: `tool-ledger.md` as a basename occurs
   twice at base — `quality/tool-ledger.md` and a round-51 fixture copy — so the basename
   rule should apply to the pointer region, where the referent is contextually the
   ledger, not to tree-wide disambiguation.)
2. Exclude **symlink blobs** (git mode 120000) from `accountable` targets; resolve or
   reject them. Nine of the ten green shapes above die on these two rules alone; P09
   requires rule 2.

This tightens the mechanism to match the frozen clause's meaning without amending the
predicate. Re-run P03–P09/P19–P21 against the corrected counter: expected `self_pointer=1
… TARGET_MISSED` for each, with P01/P02/P15/P16 unchanged.

## Limitations of this attack

- Fixture population is 3 instruments, not 82; the mechanism under test is per-row and
  spelling-based, so scale does not change the code path, and P01/P02 anchor the fixture
  semantics to the real frozen arms.
- P09's symlink qualifies only because its target text contains the basename; the finding
  is the missing mode check, not symlink-following semantics.
- The fixture revision hashes are run-local (commit-time dependent); the reproducer is
  `Attack02/run-probes.sh`, whose per-probe ledger bytes are the fixed inputs.
- W1 evidence read: `claims-frozen.md`, `registration.md`, `C1CounterDesign.md`,
  `C1Fixture.md`, `C1Evidence.md`, `C1ControlAttack.md`, `C1Simplify.md`, `C1Mutation.md`.
  Sibling seats own the context-clause attacks (F3/functional-phrase), population/grammar,
  control isolation, and TMPDIR boundaries; this seat's findings are scoped to the
  pointer self-reference mechanism.
- The lane working tree carried sibling integration edits at run time (uncommitted rows
  for `c1-r52`/`c2-r52` instruments in `quality/tool-ledger.md`); all receipts here read
  committed bytes at the frozen base and are unaffected. This seat wrote nothing to the
  lane, the fleet, or any sibling path.

## Hygiene

- Wrote only `.ufo/waves/round-52/w2/Attack02.md` and `.ufo/waves/round-52/w2/Attack02/`
  (predictions, driver, transcript). No tracked lane/fleet file, no git/jj mutation, no
  package query or install, no live read, probe, screenshot, or host mutation.
- Scratch was `/fast/scratch/hyaku/mado-r52/Attack02/` (disk guard: 582 G available);
  fixture repo and per-probe work dirs removed after the evidence was copied into the seat
  directory. No tools installed.

Report: `.ufo/waves/round-52/w2/Attack02.md`
