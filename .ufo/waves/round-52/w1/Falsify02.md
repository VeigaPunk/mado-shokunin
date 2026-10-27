# Falsify02 — C1 uniqueness/population falsification (mado round 52, w1)

Seat: Falsify02 (leaf falsifier). Target item: **C1, the population/uniqueness leg** of the
frozen predicate. No tracked lane files touched; all fixtures were seat-local under
`/fast/scratch/hyaku/mado-r52/Falsify02/` (removed on exit; receipt copies in this seat dir).

## Attacked clause

From `.ufo/waves/round-52/registration.md` (frozen predicate, C1):

> a new counter for the tracked instrument ledger runs at a requested pinned revision, and
> validates **population row uniqueness**, resolvable evidence pointer, non-self pointer, and a
> description containing instrument-specific functional context.

and from `claims-frozen.md`:

> a new committed counter distinguishes the production ledger from a no-work control ... using
> **unique population**, non-self resolvable evidence targets, and instrument-specific context checks.

Attacked specifically: the **population P the uniqueness leg ranges over**. The r52 predicate
freezes four checks but never defines P; the only definitions in the lane are the two committed
reference implementations, and they (a) silently drop git-legal instrument paths and (b)
disagree with each other. A counter implementing the frozen four checks over either definition
certifies ledgers that omit real instruments — the uniqueness/population leg is unsound as
specified. This is a fixable defect in the claim's operability, not a tradeoff.

## Reference implementation bytes under test (read-only)

- `quality/counters/c1-r51-ledger.py:128-148` — `listing()` runs
  `git ls-tree -r --name-only <rev>` (newline-delimited; git C-quotes unusual paths);
  `population()` keeps any path with `path.startswith("tools/")` (:138) plus
  `quality/*.py` / `quality/counters/*.py` with `rest.startswith(".")` excluded (:145).
- `quality/check-tool-ledger.py:135-149` — `tree()` runs `git ls-tree -r -z <sha>` (raw bytes);
  `is_population()` again uses `path.startswith("tools/")` (:164); `QUALITY_PY` is
  `^quality/[^/]+\.py$` (:73), which admits dotfiles the counter excludes.

## Attack 1 (primary, fail-open, reproduced end-to-end): leading-space path prefix

Git-legal tree: top-level directory ` tools` (leading space) holding `lead.py`, i.e. blob path
` tools/lead.py`. Both implementations' literal `startswith("tools/")` test excludes it from P.

Fixture A (scratch repo, built per commands below) true tree at `aaeb408d…`:

```
 tools/lead.py            <- real instrument, first byte is 0x20
quality/check-tool-ledger.py
quality/tool-ledger.md
tools/ok.py
```

Ledger rows cover exactly the measured P (2 rows: `tools/ok.py`, `quality/check-tool-ledger.py`).

Actual results (`a-counter.txt`, `a-gate.txt`):

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <fixtureA> --rev aaeb408d… --work <scratch>
C1_R51: population=2 ledger_rows=2 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=aaeb408d…   exit=0

$ python3 -I quality/check-tool-ledger.py --repo <fixtureA> --rev aaeb408d…
LEDGER: population=2 ledger_rows=2 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=aaeb408d…               exit=0
```

Both committed implementations print TARGET_MET while the tree's third instrument
` tools/lead.py` is unaccounted — the ledger's own contract header promises "every file under
`tools/`" (`quality/tool-ledger.md:11-14`). Even a good-faith row for it cannot help: the
counter strips the path cell with `EMPHASIS = "*_ \t"` (`c1-r51-ledger.py:46,167`) and the gate
with `clean()` (`check-tool-ledger.py:191-193`), so `` ` tools/lead.py` `` normalizes to
`tools/lead.py`, scores `dangling`, and the real file remains outside P. Reproduced: **yes**.

## Attack 2 (r52-forward, fail-open under the frozen four legs): non-ASCII C-quoting

The two enumerations diverge: non-z `--name-only` C-quotes `tools/café.py` as
`"tools/caf\303\251.py"` (one line, leading `"`), which fails `startswith("tools/")` and is
dropped from the counter's P; the gate's `-z` tree keeps it. Fixture B v2 true tree
(`b-tree.txt`, cat -A) holds 2 instruments (`tools/ok.py`, `tools/café.py`) + gate + ledger;
the ledger deliberately omits `tools/café.py` and uses non-self pointers (`corpus/notes.md`).

```
counter P = 2  ['quality/check-tool-ledger.py', 'tools/ok.py']
gate    P = 3  ['quality/check-tool-ledger.py', 'tools/café.py', 'tools/ok.py']
```

Full r51 counter on fixture B v2 (`b-counter-v2.txt`): its own measurement is clean
(population=2, all counters 0) and it only misses because the r51-only checker-agreement clause
(`checker_ledger`, `c1-r51-ledger.py:296-319`) cross-compares with the gate. The r52 frozen
predicate contains **no such cross-check** — it freezes only the four legs. Evaluating exactly
those four legs over the counter's own P (`b-r52-legs.txt`, driver imports the committed
counter module unmodified):

```
uniqueness  dup=0 | population uncovered=0 dangling=0 | pointer bad=0 self=0 | description empty=0
-> all four r52-frozen legs pass over the counter's P: YES
-> instruments unaccounted in the true tree: ['tools/café.py']
```

Reproduced: **yes**.

## Attack 3 (corroboration): newline filename and dotfile divergence

- Fixture C: `tools/evil\nname.py` — counter P=1 (C-quoted single line, dropped), gate P=2
  (includes it, where no one-line markdown row can ever cover it — the gate is fail-closed but
  the tree is unscoreable). Reproduced: **yes** (`c-tree.txt` + enumeration output, fixture
  removed with scratch; commands below regenerate it).
- `quality/.hidden.py`: counter excludes (`rest.startswith(".")`, :145), gate includes
  (`^quality/[^/]+\.py$`, :73) — the two reference definitions of P already disagree on
  dotfiles. Reproduced: **yes** (module-level evaluation, output quoted below).

## Base-state check (latent, not actual, at the frozen base)

`git ls-tree -r --name-only 85d57a818c3707397e21c840b6498b105ba798aa` → 24,582 paths, **0**
paths with non-printable-ASCII bytes or leading/trailing whitespace. Today's production tree
and the frozen control are therefore unaffected; the defect is in the methodology the claim
certifies. The new counter does not exist yet at base (per `receipts/c1-base.txt` the r51
counter reports 82/82 TARGET_MET), so this attack targets the frozen predicate's operability,
not a shipped artifact.

## Smallest safe correction

1. Freeze P in the predicate: enumeration by `git ls-tree -r -z --name-only <rev>` over raw
   byte paths; population = every blob under the exact `tools/`, `quality/*.py`,
   `quality/counters/*.py` prefixes with no other byte filtering.
2. Close the representability hole explicitly, one of:
   a. the counter refuses to score (fail-closed, setup-class exit) when any population path is
      not representable as a one-line ledger row (embedded newline/NUL, or normalizing under
      the row parser's stripping rules to a different path), or
   b. the claim is scoped to a frozen safe path grammar (e.g. components matching
      `[A-Za-z0-9._+-]+`) and the counter verifies the tree against that grammar before
      scoring.
3. Add a red/green selftest fixture containing an unusual-name instrument (leading-space
   directory component, non-ASCII name) so the population leg's soundness is itself exercised.

Until 1-2 land, "population" in C1 is implementation-defined (gate-P: fail-closed but
unscoreable on newline names; counter-P: fail-open), and the uniqueness/population leg cannot
be judged sound.

## Commands (reproduction)

Fixture A (host-guard toplevel assert before each commit; TMPDIR set to seat scratch):

```
FA=<scratch>/fixture-a; mkdir -p "$FA/tools" "$FA/quality" "$FA/ tools"
printf '#!/usr/bin/env python3\nprint("ok")\n'  > "$FA/tools/ok.py"
printf '#!/usr/bin/env python3\nprint("lead")\n' > "$FA/ tools/lead.py"
# ledger: rows for tools/ok.py and quality/check-tool-ledger.py only (see seat receipts)
cp <lane>/quality/check-tool-ledger.py "$FA/quality/"
git -C "$FA" init -q -b main && git -C "$FA" config user.email falsify02@seat.local \
  && git -C "$FA" config user.name Falsify02
test "$(git -C "$FA" rev-parse --show-toplevel)" = "$FA"
git -C "$FA" add -A && git -C "$FA" commit -qm "fixture A"
python3 -I <lane>/quality/counters/c1-r51-ledger.py --repo "$FA" --rev HEAD --work <scratch>/work-a
python3 -I <lane>/quality/check-tool-ledger.py --repo "$FA" --rev HEAD
```

Fixture B/C: same pattern; B adds `printf ... > "$FB/tools/caf$(printf '\xc3\xa9').py"` and a
two-row ledger omitting it (v1 self-pointers, v2 `corpus/notes.md` pointers); C adds
`printf ... > "$FC/tools/evil\nname.py"`. The r52-legs driver imported the committed counter
module and ran `listing()/population()/parse_rows()/pointer_resolves()` unchanged; its output
is preserved in `b-r52-legs.txt`.

Environment: git 2.56.0, Python 3.14.8, no installs (none needed). Disk guard checked:
/fast had 597 GiB free before fixture work; no ENOSPC.

## Limitations / dissent

- Latent at base: no actual divergence on the frozen base tree (24,582 paths clean), so this
  does not subvert today's production-vs-control distinction; it falsifies the claim's
  methodology as specified. If the canonical judge reads C1 as scoped to trees whose
  instrument names are printable ASCII without leading/trailing whitespace (true at base and
  plausibly for all future lane instruments, since lane tools are ASCII-named), this is a
  boundary-condition defect to fix by pinning P, not grounds to reject the claim outright;
  the four-leg architecture itself is untouched by this attack.
- The newline-name case makes a tree unscoreable by any line-based ledger under the gate's P;
  correction 2a turns that into an explicit setup-class refusal rather than an unreachable
  TARGET_MET.
- Fixtures were scratch repos under `/fast/scratch/hyaku/mado-r52/Falsify02/` and were removed
  on exit; receipts preserve every command output needed to re-run.

## Deliverables

- .ufo/waves/round-52/w1/Falsify02.md (this report)
- .ufo/waves/round-52/w1/Falsify02/a-counter.txt — r51 counter TARGET_MET on fixture A (attack 1)
- .ufo/waves/round-52/w1/Falsify02/a-gate.txt — gate TARGET_MET on fixture A (attack 1)
- .ufo/waves/round-52/w1/Falsify02/a-tree.txt — fixture A true tree bytes (cat -A, leading space visible)
- .ufo/waves/round-52/w1/Falsify02/b-tree.txt — fixture B tree bytes, -z vs non-z C-quoting divergence
- .ufo/waves/round-52/w1/Falsify02/b-counter-min.txt, b-counter-v2.txt — r51 counter runs on fixture B (own P clean; misses only via r51-only gate clause)
- .ufo/waves/round-52/w1/Falsify02/b-gate-min.txt, b-gate-v2.txt — gate runs on fixture B (P=3, uncovered café)
- .ufo/waves/round-52/w1/Falsify02/b-r52-legs.txt — all four r52-frozen legs pass over counter P while café unaccounted (attack 2)
- .ufo/waves/round-52/w1/Falsify02/c-tree.txt — fixture C newline-name tree bytes + enumeration divergence (attack 3)

Report: .ufo/waves/round-52/w1/Falsify02.md
