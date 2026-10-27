# Attack22 — round-52 W2 attack #22

Target: **C1 false-positive on legitimate ledger-reader row**. Axes named: **operability** (C1 only; no coverage move). This is an attack on the landed C1 counter draft and its claimed green/red semantics, not a vote and not a predicate amendment.

Seat `Attack22` · round 52 w2 · lane `mado-shokunin` · frozen base `85d57a818c3707397e21c840b6498b105ba798aa`.
Source-only fences held: no host/compositor/process reads, no input capture, no screenshots, no package queries, no producer execution, no git/jj mutation, no tracked or fleet-root writes. The counter was executed read-only against git blobs; all writes went to `/fast/scratch/hyaku/mado-r52/Attack22/` (removed at exit) and this seat directory.

## 0. Attacked clauses (named)

- **C1-green** — `registration.md` "Frozen predicates" C1: "It must pass on the existing production ledger at the base revision…"
- **C1-context** — `claims-frozen.md` C1: "…instrument-specific context checks"; `registration.md` C1: "fail on `controls/c1-do-nothing.md` specifically for self-pointer/context defects" (attribution requires the context signal not to fire on context-rich legitimate rows).
- Instrument attacked: the landed counter draft `quality/counters/c1-r52-ledger.py` (untracked at HEAD = frozen base; not landed, per the W1 signal that draft r-green proves a synthetic fixture only).

W1 evidence read before judging: `C1Evidence.md`, `C1ControlAttack.md`, `C1CounterDesign.md`, `C1Simplify.md` (+ its `control-G/H`, receipts, `gen-controls.py`), `C1Fixture.md`, `C1Mutation.md`, `Falsify11.md`, `Falsify35.md`, `receipts/c1-base.txt`, `controls/c1-do-nothing.md`.

## 1. Falsifier 1 (primary): the landed draft fails its own green arm on the untouched production ledger

The base production ledger (`git show <base>:quality/tool-ledger.md`, sha256 `df5b3705…`, matching `C1Evidence`'s measured bytes) contains a fenced row-grammar example at line 12:

```
| `<repo-relative path>` | <one-line description> | `<pointer path>` or `<pointer path>:<line>` |
```

The landed draft's `parse_ledger` (c1-r52-ledger.py, `cells()`/`parse_ledger()`) accepts any 3-cell backticked line anywhere in the file — it has **no fenced-code skip**. The round-51 counter it replaces skips fences (`c1-r51-ledger.py:157-163`, `fenced = not fenced`). The landed draft therefore parses the documentation example as an 83rd row whose path is not in the population and whose pointer does not resolve.

Exact reproduction (receipt: `Attack22/battery.txt` §A/A2):

```
$ python3 -I quality/counters/c1-r52-ledger.py --repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa --ledger ledger-base.md
C1_R52: population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED exit=1
# identical without --ledger (ledger blob read from the repo at the rev)
```

Isolating control (base ledger minus only that fenced example line; fixture `ledger-clean.md`, sha256 `1dcb5028…`): `ledger_rows=82 … verdict=TARGET_MET exit=0` (battery §B). So the entire green-arm failure is attributable to the fence row, and **verdict TARGET_MISSED on the frozen production ledger is reproduced with the committed draft counter**.

Consequence: the C1 green arm ("pass on the existing production ledger at the base revision") is **not satisfied** by the landed draft at any revision — the fenced example is tracked ledger content. Any fix requires either a counter change (fence skip, as r51 does) or a tracked edit to the scored production ledger itself (which changes the artifact the claim is about and must be registered, not silently folded into integration).

## 2. Falsifier 2 (seat target): false positive on a legitimate ledger-reader row

The draft's context clause (`assess()` in c1-r52-ledger.py) flags `generic_desc` when the normalized description shares **no two-word phrase** with the instrument's own bytes. That operationalization rejects truthful, instrument-specific descriptions written in vocabulary disjoint from the file's identifiers and docstring wording.

Fixtures (full production population, unique rows, non-self resolvable pointers untouched — only the description cell of one ledger-reader row differs from production):

- `ledger-fp-c1r51.md` (sha256 `692d9de7…`) — row `quality/counters/c1-r51-ledger.py` gets: *"Audits the tabulated roster of tracked utilities for omissions, malformed lines, duplicated entries, dangling references and hollow wording, then prints one verdict line."* Every clause of this sentence is verified against the instrument's source (`c1-r51-ledger.py:215-247`: uncovered/dangling/dup/bad_pointer/empty_desc tallies; one `C1_R51` verdict line).
- `ledger-fp-checker.md` (sha256 `4162f983…`) — row `quality/check-tool-ledger.py` gets: *"Compares the declared roster of tracked utilities against the revision's file listing and reports omissions, malformed lines, duplicated entries, unresolvable references and hollow wording."* Verified against `check-tool-ledger.py:28-39,268-296` (findings classes and population derivation from the rev's tree).

Both descriptions are legitimate and instrument-specific by any ordinary reading; a probe replicating the counter's exact predicate (`Attack22/probe_fp.py`) measured **zero shared two-word phrases** with the respective instrument bytes (23 and 25 normalized words, 0 collisions), while the G control's legitimate row passes only because it copies the ledger path tokens into its description (measured shared bigrams: `quality tool`, `tool ledger`, `ledger md`, `reads quality`, `md and`).

Exact reproduction (battery §C/§D):

```
$ python3 -I c1-r52-ledger.py --repo <lane> --rev <base> --ledger ledger-fp-c1r51.md
C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=1 verdict=TARGET_MISSED exit=1
$ python3 -I c1-r52-ledger.py --repo <lane> --rev <base> --ledger ledger-fp-checker.md
C1_R52: … generic_desc=1 verdict=TARGET_MISSED exit=1
```

The §B isolating control proves these runs carry no other defect: the sole delta from a green ledger is the description wording. **Verdict: false positive on legitimate ledger-reader rows — reproduced.** A maintainer can truthfully re-word a row and flip the lane's C1 verdict without any accountability regression; conversely a `generic_desc=1` red can no longer be attributed "specifically" to a missing-context defect, which is what the frozen red arm requires.

## 3. Specified-control verification and calibration (the attacked counter's other arms)

Run against the same landed draft (battery §E–§H):

| Case | Result | Reading |
|---|---|---|
| `C1Simplify/control-G-legit-ledger-reader.md` | `generic_desc=0 TARGET_MET` exit 0 | The peer's first-draft G false positive (`self_pointer=1` all-cell scan) is **not** reproduced on the landed draft; its self check reads only the pointer cell. Verified, not assumed. |
| `C1Simplify/control-F3-forged.md` | `generic_desc=0 TARGET_MET` exit 0 | **W1 signal confirmed on the landed draft**: the F3 counterfeit semantic-context bypass (distinct generic descriptions each copying a word pair from the instrument's header) passes completely. The landed draft has none of the peer-final's four filters. |
| `C1Simplify/control-H-minimal-forgery.md` | `generic_desc=0 TARGET_MET` exit 0 | Minimal forgery accepted (consistent with the disclosed lexical ceiling). |
| frozen `controls/c1-do-nothing.md` | `ledger_rows=0 uncovered=82 TARGET_MISSED` exit 1 | Red only through zero parsed rows / full non-coverage: **no `self_pointer`, no `generic_desc`** finding. W1's claim (control does not isolate the required defects; failure not attributable to self-pointer/context) is reproduced verbatim on the landed draft. |

## 4. Reported errors (instrument defects observed, not inferred)

1. **Green-arm failure at base** (§1): `dangling=1 bad_pointer=1` on untouched production bytes; default blob mode identical.
2. **`--selftest` and `--work` are accepted and ignored** by the landed draft (`main()` parses both, references neither; no selftest code path exists). `registration.md` requires "Selftest includes explicit red/green receipts" — the landed draft cannot produce them; a `--selftest` invocation silently scores the ledger instead (verified by reading `main()`; the flag is a no-op).
3. **Chronology trap measured** (battery §I): the in-flight modified `quality/tool-ledger.md` (2 added r52 rows, uncommitted) scored at the base rev yields `ledger_rows=85 dangling=3 bad_pointer=3` — the two new rows' pointers (`.ufo/waves/round-52/registration.md`) do not exist at the base rev. A green run must pin a revision that contains the registration and counters; running "at base" after integration edits is a guaranteed false red. (Consistent with C1Evidence ER-1/ER-13; here measured on the landed draft.)
4. **Context check measures lexical overlap, not instrument-specific context** — false-positive direction demonstrated with truthful rows (§2), false-negative direction with F3/H (§3).

## 5. Limitations

- Falsifier 2's descriptions were authored by me and verified truthful against instrument source; a non-author reviewer may judge them insufficiently specific, but their defect classes and verdict behaviour are mechanically exact and reproducible from the fixtures.
- The lexical-ceiling false negatives (F3/H pass) are disclosed limits the frozen claim already bounds ("not prose entailment"); I report them as calibration, not as new falsifications.
- The landed draft is untracked; if integration substitutes the W1-verified peer-final draft instead, §1's fence defect and §3's F3 pass may not apply to that artifact — but they are true of the bytes currently at `quality/counters/c1-r52-ledger.py`, which is what the wave was told to attack.
- All runs are read-only counter executions against committed git objects at the frozen base revision; no fixture was committed and no clone was mutated. No external source candidate used; no URL/access date applies.
- No installs: no package, tool, or binary was installed or upgraded. Scratch `/fast/scratch/hyaku/mado-r52/Attack22/` removed after evidence was copied into this seat directory.

## Deliverables

- `.ufo/waves/round-52/w2/Attack22.md` — this report.
- `.ufo/waves/round-52/w2/Attack22/battery.txt` — verbatim commands and outputs for §A–§I with exit codes.
- `.ufo/waves/round-52/w2/Attack22/probe_fp.py` — the predicate-replication probe and bigram measurements.
- `.ufo/waves/round-52/w2/Attack22/ledger-clean.md` (sha256 `1dcb5028…`), `ledger-fp-c1r51.md` (sha256 `692d9de7…`), `ledger-fp-checker.md` (sha256 `4162f983…`) — reproduction fixtures; base ledger bytes are reconstructible via `git show 85d57a818c3707397e21c840b6498b105ba798aa:quality/tool-ledger.md` (sha256 recorded in `ledger-base.sha256`).

Report: `.ufo/waves/round-52/w2/Attack22.md`
