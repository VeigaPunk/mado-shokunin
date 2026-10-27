# Attack01 — W2 attack #01: C1 forged functional-phrase context bypass

Axes: **operability** (C1 only). Attack wave, not a vote; this seat takes no claim
verdict. Attacked claim clause (frozen, `claims-frozen.md` C1): *"…distinguishes the
production ledger from a no-work control … using unique population, non-self
resolvable evidence targets, and **instrument-specific context checks**."* The
attacked counter clause is the `generic_desc` context check.

Base `85d57a818c3707397e21c840b6498b105ba798aa` (lane HEAD unchanged at test time).
Two byte sets measured:

- **w1draft** = `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`, sha256
  `0fe862f116a7…` — matches the final byte identity W1 reported (847 lines,
  53-check selftest → `C1_R52_SELFTEST: 53/53 passed`, measured here).
- **landed** = `quality/counters/c1-r52-ledger.py`, sha256 `923faf02cd0c…` — an
  **untracked, uncommitted 78-line rewrite** present in the working tree; NOT the
  W1-reviewed bytes (all four context filters absent, no selftest body, no
  fence-skip). Working tree also carries `M quality/tool-ledger.md` (+2 counter
  rows), `M corpus/README.md`, `M corpus/SOURCES.md`, `?? corpus/knowledge/
  hyprland-synthetic-dispatch-r52.md`, `?? corpus/lessons/round-52.md`,
  `?? quality/counters/c2-r52-proposition-entry.py`. HEAD untouched.

## T1 — W1 bypass evidence independently reproduced (w1draft)

Command shape (all runs, read-only, cwd = own scratch):
`python3 -I <counter> --repo $LANE --rev 85d57a8… [--work <scratch>] --ledger <ledger>`

| ledger | result |
|---|---|
| production at base | `generic_desc=0 verdict=TARGET_MET` exit 0 |
| `w1/C1Simplify/control-F3-forged.md` | `generic_desc=10` (all `reason=bound-only-by-name-path-or-function-words`) `TARGET_MISSED` exit 1 |
| `w1/C1Simplify/control-H-minimal-forgery.md` | `generic_desc=0 verdict=TARGET_MET` exit 0 |
| committed `controls/c1-do-nothing.md` | `uncovered=81 dup=1 self_pointer=1 generic_desc=1 TARGET_MISSED` |

Byte identity confirmed by `sha256sum` (receipts/inputs.sha256): my copies of the
F3/H controls hash `15fe970d…`/`f4e5bba1…`, identical to the W1 originals.
Verdict: **reproduced** — W1's numbers are exact on the bytes W1 hashed.

## T2 — F-all: the bypass is a class, not a control artifact (both byte sets)

`forge.py` (this seat dir) builds an 82-row ledger with production paths and
production pointer cells verbatim; every description is semantically empty
`Generic accountability note <i> <phrase>.` where `<phrase>` is a consecutive
word pair lifted from that instrument's own committed bytes, chosen to survive
all four w1draft filters (not own-name words, not population vocabulary, not a
filesystem-path fragment, not function-words-only). Most rows bind `env python3`
— the shebang. A shebang is not functional context by any measure.

```
w1draft × F-all-forged.md → generic_desc=0 verdict=TARGET_MET exit 0
landed  × F-all-forged.md → generic_desc=0 verdict=TARGET_MET exit 0
```

Verdict: **reproduced and extended**. W1's F3 forged control left 72/82 rows
through the strongest reviewed clause; the same mechanism reaches **82/82**.
No lexical configuration of this clause shape distinguishes a motivated forgery
from production. This is the exact residual W1 disclosed ("copy a real
functional phrase out of the instrument's own bytes"); it is real and total.

## T3 — landed bytes regress the attacked clause

All four w1draft context filters are absent at `quality/counters/
c1-r52-ledger.py:62-63` (`phrases={tuple(iw[i:i+2]) …}; if len(dw)<5 or
PLACEHOLDER.match(desc) or not any(tuple(dw[i:i+2]) in phrases …): generic+=1`).

| ledger | landed result |
|---|---|
| `control-F3-forged.md` | `generic_desc=0 verdict=TARGET_MET` — **all 82 forged rows accepted** (w1draft rejected 10) |
| `control-H-minimal-forgery.md` | `TARGET_MET` |
| `H4n-nameonly-forged.md` (`mado-anims.py` desc = `mado anims py does things here.`) | `generic_desc=0 TARGET_MET` — pure own-name restatement accepted; w1draft flags it `bound-only-by-name-path-or-function-words` |

Verdict: **reproduced, strictly worse** — the landed bytes accept the W1 bypass
completely, plus bypass shapes the draft already rejects.

## T4 — single-row forgery variants (isolating the clause)

On `production-ledger-nofence.md` (base ledger with only the fenced grammar
example removed — needed to isolate landed's parser defect, see O1):

| forgery | w1draft | landed |
|---|---|---|
| `tools/mado-verify.sh` desc → `env bash and nothing else here okay.` | `generic_desc=0 TARGET_MET` | `TARGET_MET` |
| `quality/counters/c2-r51-dispatch-entry.py` desc → `PRED-C2-r51 does things.` | `generic_desc=0 TARGET_MET` | `TARGET_MET` |

Shebang pairs and prediction ids are genuine byte-bigrams of those instruments;
both are semantically empty filler. The second case is the second thin-margin
row W1 named (`survives on exactly one qualifying phrase … its prediction id`).

## O1 — [NEW] landed counter cannot pass the frozen green clause

`landed` has no fenced-block skipping: `parse_ledger` (lines 39-43) accepts any
3-cell pipe row whose first cell is backticked. Measured on the production
ledger at base:

```
C1_R52: population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1
        self_pointer=0 generic_desc=0 verdict=TARGET_MISSED  exit=1
```

The 83rd row is the ledger's own grammar example at `quality/tool-ledger.md`
lines 11-13 (inside a fence): path `<repo-relative path>`, pointer `<pointer
path> or <pointer path>:<line>` — parsed as a data row, charged `dangling=1`
and `bad_pointer=1`. This is W1's measured "83 vs 82, fence-skipping is not
optional" hazard realized in the landed bytes. The claim requires "production
pass … at the frozen revision": **landed fails green outright** (only a
fence-stripped ledger, which is not the committed artifact, passes). w1draft is
clean here (`TARGET_MET`, r1 receipt).

## O2 — landed: frozen red case cannot report the required signals

`landed × controls/c1-do-nothing.md`:
`population=82 ledger_rows=0 uncovered=82 … self_pointer=0 generic_desc=0
verdict=TARGET_MISSED`. The 4-cell control rows never reach parsing
(`len(c)==3` at line 43), so the required "fail specifically for
self-pointer/context defects" is unobservable — the counter reports only a
coverage miss. (Registration/claim language, w1draft: `self_pointer=1
generic_desc=1` on the same control — the signals exist only in the draft.)
This is the concrete instance of the W1 signal "the control does not isolate
required defects if schema shape causes failure."

## O3 — landed: `--selftest` is a silent no-op

Flag declared at line 68 (`action='store_true'`), never consulted: `main()` runs
the measurement path regardless. `landed --selftest --repo $LANE --rev …`
prints a normal measurement line and exits 1, with zero selftest checks.
Registration requires "Selftest includes explicit red/green receipts"; w1draft
measured `C1_R52_SELFTEST: 53/53 passed` in this seat's scratch. The landed
bytes cannot satisfy that predicate.

## Verdict

- **Against the attacked clause "instrument-specific context checks"**:
  falsifier reproduced. On the W1-reviewed bytes the bypass is a disclosed
  ceiling (claim text "bounded accountability checks, not prose entailment"
  bounds it, and the new working-tree ledger description honestly repeats that
  bound). On the landed working-tree bytes the same bypass is total **and**
  the bytes separately break the green clause (O1), the red-signal
  requirement (O2), and the selftest predicate (O3): the landed bytes do not
  satisfy the frozen C1 predicate as written. If the landed bytes are what
  integration intends to commit, they must not ship.
- Attacked clause named, reproduction exact, outcomes measured at base.

## Limitations

- The landed bytes are untracked/uncommitted; whether they are the integration
  candidate or a sibling artifact is outside my lane. If integration instead
  lands the w1draft bytes, O1-O3 do not apply and T2 is a claimed-residual
  boundary, not a defect (per W1's own ceiling note).
- `--ledger` reads control bytes from the filesystem while instruments resolve
  at `--rev` — the intended control mechanism, same as W1 used.
- My forged controls exercise the context clause only; pointers/population are
  production-verbatim by construction, isolating `generic_desc`.
- No claim about non-author judgment; verdict here states measured outcomes
  against the frozen predicates, not admission.

## Reproduction (exact)

```
S=<scratch>; LANE=<lane>; REV=85d57a818c3707397e21c840b6498b105ba798aa
git -C $LANE show $REV:quality/tool-ledger.md > $S/production-ledger-base.md
python3 $S/forge.py $S/F-all-forged.md
python3 -I <counter> --repo $LANE --rev $REV [--work $S/work] --ledger <ledger>
```

Artifacts kept under `.ufo/waves/round-52/w2/Attack01/`: `forge.py`,
`production-ledger-nofence.md`, `controls/{F-all,H2n,H3n,H4n}-*.md`,
`receipts/{inputs.sha256,r1-w1draft-matrix,r2-landed-matrix,r3-fall,
r4-singlerow,r5-nofence}.txt`. Scratch `/fast/scratch/hyaku/mado-r52/Attack01`
removed on completion. No tracked edits, no fleet/sibling writes, no git/jj
mutation (read-only `git show`/`ls-tree`/`diff`/`status`/`rev-parse` only), no
package queries, no live reads, no installs.

Report: `.ufo/waves/round-52/w2/Attack01.md`
