# R68CriticClaims — round-68 claims critique (w1, leaf seat)

Critique of the two frozen claims without building them. Read: `.ufo/waves/round-68/claims-declaration-r68.md`
(declaration), `.ufo/waves/round-68/control-baseline-r68.txt` (baseline), both counters, the control JSON,
the lesson, the errata and the lane history. No production file was written by this seat; all fixtures are
under `/fast/scratch/hyaku/mado-r68/R68CriticClaims/` and were deleted before yield.

## Revisions and instrument hashes

| item | value |
|---|---|
| base (pre-r68 tip) | `510100c81e6cf63fec6be380c2f2f9c670f32cbc` (21:57:06) |
| pre-freeze baseline commit | `2ca2bec39c42770a3176989f013e8c1cbbdb7df3` (22:04:23) |
| freeze commit | `e0727cda15621766c35dcf8b70c211b6531aab45` (22:04:51) |
| launch marker | `.ufo/waves/round-68/w1.ready` mtime 22:05:53; `.ufo/waves/round-68/w1.ready.dispatched` first line `2026-11-03T22:06:25` |
| launch commit (harness + dispatch evidence) | `40d2bef8964a098ae50f01094fa19e4725952010` (22:06:33) |
| instrument fix 1 (C2 `--scratch-root`) | `2a39e74142e3c3710db7af0f4d73a7a6eac64831` (22:09:06) |
| instrument fix 2 (C2 denominator/guard shapes) | `686d6345` (22:12:03) |
| twelve-gate repair | `425d4b2fec41fc94bf9cd59dc5ca8c3e0bbcb9ed` (22:12:09) |
| ledger rows for the three instruments | `18d692f3` (22:14:55) |
| measured content (SCORECARD/receipt) | `379e97f884a6cf7ed3ac96068b0165d63495524f` |
| lane tip while writing this report | `20f692bed520b607d0d7eaa017a1ee441bc8e144` (moving) |

`sha256` of the frozen/correction artifacts:

```
1f3a2392f9140b6828511c5bc1f433e4417d9c04159ce061dde7fc9b549e5f12  claims-declaration-r68.md
44551431b885cc60f3be52ed722b740887d908d696461681aab8e29baa1a8025  control-baseline-r68.txt
b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91  controls/c2-controls.json
43a7638993de7ada49a4a43a42ab884dbcc36ae9d3cf9bf3a2fe1bfe830ce7c7  c2-command-erratum-r68.txt
175d373ce1cc7ad5b26acb164e381fedafa9f686ce3324dd63a72174b7b4b0c3  c2-denominator-erratum-r68.txt
205f39c574194056f5f67072e9d0cae3149a2941fc94dd2e94d6bad4b9a136a5  corpus/lessons/round-68.md
```

Instruments at the tip (blobs): harness `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527`
(`e970d6ea`), C1 counter `bdea8dc6b4455f45c59896a44f0bd4ede21c26b82c67e0618a05ac069ef50a85`
(`f131c7f7`), C2 counter `5a6b386545889e3b072740d1d5fa39b3a4c523661d4a788993d48d4607410faa`
(`b53e6084`). Freeze-time C2 counter: `8eb99a63e324fce18eda824d7aefa48d72650ff6abb7c4afa45def9191ce880e`
(13429 B); post-`--scratch-root`/pre-denominator C2 counter at `2a39e741`:
`0e853b1b11b3f327bc2c0e6a4aa6ce32a5fc5561d9575b0bf1bc548c7f4dfea8` (14057 B).

## Open blockers

### B1 — the frozen `controls=11/11` is not enforced by the C2 exit rule

- Declared: `.ufo/waves/round-68/claims-declaration-r68.md:99-103` (frozen line) and `:117`
  ("`controls=11/11`: the frozen classification case set ... is scored in the same run").
- Delivered: `quality/counters/c2-r68-reader-guard.py:145-148` (`verdict_met`) requires
  `population == 20`, `readers == 13`, `unguarded == 0`, `controls_total > 0`, `correct == controls_total`.
  It does not require `controls_total == 11`, and the counter does not verify the controls file's
  `sha256` `b7a1c939…` (grep: no `b7a1c939`, no `sha256` in the file).
- Reproduction (lane tip `049c2e0c`, counter bytes `b53e6084`):

```sh
python3 - <<'PY'
import json
d = json.load(open('.ufo/waves/round-68/controls/c2-controls.json'))
d['cases'] = d['cases'][:-1]          # drop the 11th case (non-reader)
json.dump(d, open('<S>/controls-10cases.json', 'w'), indent=1)
PY
python3 -I quality/counters/c2-r68-reader-guard.py --repo . --rev 049c2e0c \
  --controls <S>/controls-10cases.json
# rc=0
# MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=10/10 \
#   verdict=TARGET_MET rev=049c2e0c7ec444f81f3eec32c4869e43c50c6f51
```

The frozen sentence prints `controls=11/11`; the exit rule returns 0 with `controls=10/10` and
`TARGET_MET`. The 10-case file's sha256 is
`336b578fae0c72d44a4204fe84b6968387824619f6beaa33403574bd0b277886`. This is the same defect class as
M68-4 (denominator) but for the controls denominator: the round's own QUALITY 110(b) rule ("the frozen
sentence and the counter's code are the same sentence") is not met. It is latent for the declared run
because the command's path is frozen, but the instrument's verdict is decoupled from the frozen count.
Smallest safe correction: add `controls_total == 11` (a frozen constant) to `verdict_met` plus a
selftest case `verdict_met(20, 13, 0, 10, 10) is False`; instrument-only, predicate text unchanged.
If the round refuses a third post-freeze instrument edit, append an erratum naming the residual and
record why the frozen path makes it unreachable.

### B2 — axis-posture numbers are stale and the receipt citation is false

- Declared: `claims-declaration-r68.md:17-21` — "navigation 78/78, hermetic gate suite 460/460,
  register 8/8 groups, used-by missing=0, ledger 108/108 — the round-67 landing receipt
  `.ufo/waves/round-67/landing-counters-r67.txt`", and "the gap is 0, below the window N=3 —
  `SCORECARD.md` § Saturation".
- Actual at the base `510100c8`:

```sh
python3 -I quality/check-index.py --repo . --rev 510100c81e6cf63fec6be380c2f2f9c670f32cbc
# MADO_INDEX: rev=510100c8… indexed=79/79 missing=0 dangling=0 duplicates=0 coverage=10.0000/10 rc=0
python3 -I quality/check-tool-ledger.py --repo . --rev 510100c81e6cf63fec6be380c2f2f9c670f32cbc
# LEDGER: population=110 ledger_rows=110 uncovered=0 … verdict=TARGET_MET rc=0
sed -n '5p;11p' .ufo/waves/round-67/landing-counters-r67.txt
# revision=caf131d6… indexed=79/79 …
# LEDGER: population=110 ledger_rows=110 uncovered=0 … verdict=TARGET_MET …
```

The cited receipt contains `79/79` and `110/110`, not `78/78` and `108/108`. Those two stale values are
the round-66/pre-round-67 posture (SCORECARD `:3577-3582`), which the declaration copied while citing the
round-67 *landing* receipt. The conclusion ("all at their measured maximum; no axis distinctly lowest")
still holds for `79/79` and `110/110`, so this is a provenance/number defect, not a target defect.
Separately, `SCORECARD.md` § Saturation (`:211-218`) is a placeholder ("to be declared by the lane on
its next round per `AXES.md` …") and contains no `N=3`; the value appears in the round-posture prose
(SCORECARD `:3577`) and the round-68 block. Smallest safe correction: append an erratum correcting
`78/78 → 79/79`, `108/108 → 110/110`, and re-citing the receipt (or the SCORECARD posture line as the
pre-round value); cite `SCORECARD.md:3577` for `N=3`, not `§ Saturation`.

### B3 — duplicate mistake ID `M68-3` in the lesson

- `corpus/lessons/round-68.md:51` — `M68-3` = the r67 "controls unchanged" sweep is path-vacuous.
- `corpus/lessons/round-68.md:57` — `M68-3` = the frozen C2 command passed `--scratch-root`, which the
  counter did not accept.

Two distinct defects share one ID; the landing commit message (`67b47df4`, "mistakes M68-3/M68-4") and
the SCORECARD's "two counter defects" make a citation of `M68-3` ambiguous. Reproduction:
`grep -n '^| M68-' corpus/lessons/round-68.md` returns `49,50,51,57,58` with `51` and `57` both `M68-3`.
Smallest safe correction: an appended lesson correction renumbering the second occurrence (and
`M68-4` after it), or disambiguating suffixes `M68-3a`/`M68-3b`; the lesson is append-only.

### B4 — C1 counter docstring token contradicts the frozen and emitted token

- `quality/counters/c1-r68-selfmutants.py:21`: "A recipe that does not occur exactly once is
  `recipe=none`".
- The emitted token is `applicable=no` (`:158`), and the declaration says `applicable=no`
  (`claims-declaration-r68.md:66`).
- The counter blob is unchanged since the freeze (`f131c7f7`), so the drift is still present.
Reproduction: `grep -n 'recipe=none\|applicable=no' quality/counters/c1-r68-selfmutants.py` → `21` vs
`158`. The frozen line does not print the token, so the target is unaffected; this is exactly the
"frozen text must describe the delivered observable" class. Smallest safe correction: a doc-only edit
or a lesson/erratum note (no predicate change).

### B5 — both counters' `CONTRACT_RE` never validates the emitted line

- C1: `CONTRACT_RE` defined at `quality/counters/c1-r68-selfmutants.py:47-49`; used only at `:249`,
  `:253`, `:257`, all against literal strings in `--selftest`. `measure()` (`:179`) prints the line with
  a `%` format (`:214-218`) without a `fullmatch`.
- C2: `CONTRACT_RE` at `quality/counters/c2-r68-reader-guard.py:47-51`; used only at `:301` and `:305`
  (selftest literals). `measure()` (`:151`) prints at `:189-192` without a `fullmatch`.
- `.ufo/waves/round-68/predicate-binding-r68.txt:22-23` says "The counters' CONTRACT_RE patterns are
  asserted by their own selftests" — true of the literals, but it does not bind the emitted line.
Reproduction: `grep -n CONTRACT_RE quality/counters/c1-r68-selfmutants.py quality/counters/c2-r68-reader-guard.py`
(definitions at 47; all uses in the selftest ranges). A format-string drift would still exit 0 and print a
non-conforming line. Smallest safe correction: `fullmatch` the assembled line before printing/returning
in both `measure()` bodies, or record the limit in the lesson. Instrument-only; predicate unchanged.

### B6 — the exact frozen C2 line is reachable with zero behavioral repair (declared limit)

- Fixture `fixture-deadguard` (rev `c62198603265bb843f3cbc562787783d4b279f4a`): the 20 base
  `quality/check-*.py` files plus, appended to each of the 12 unguarded readers, a never-called function:

```python
def _r68_dead_guard():
    """Added by an executor to satisfy the census; never called, never passed to git."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env
```

- Reproduction against the current counter (`b53e6084`):

```sh
python3 -I quality/counters/c2-r68-reader-guard.py \
  --repo /fast/scratch/hyaku/mado-r68/R68CriticClaims/fixture-deadguard \
  --rev HEAD --controls .ufo/waves/round-68/controls/c2-controls.json
# rc=0
# MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 \
#   verdict=TARGET_MET rev=c62198603265bb843f3cbc562787783d4b279f4a
```

No gate's runtime behavior changed: a `def` that is never called leaves every existing line and every
git invocation untouched. This is inside the declaration's Limits ("a guard set in a branch never taken
reads as guarded"; "presence-tested ... not by dataflow", lesson `:203-208`; SCORECARD round-68 row
"presence-tested (no dominance check, no dataflow)"), so it is disclosed rather than a predicate
mismatch. It does, however, falsify the stronger What-changes sentence that a planted `refs/replace`
"changes the bytes a gate scores" (declaration C2): the census cannot distinguish a wired repair from an
uncalled construction. The actual twelve production repairs are wired (see no-harm inventory), and the
auxiliary hazard probe samples one gate (declaration `:129-133`), so 11/12 gates have no runtime receipt.
Smallest safe correction: no predicate change (the count is frozen and the repairs are real); make the
Limits explicit about an uncalled/never-passed guard and either extend the hazard probe to all 12 or
state that only one is sampled.

### B7 — C1 is already TARGET_MET at the launch commit, before any seat works

- Base `510100c8` (frozen command): `selftest=absent killed=0/3 applied=0/3 base=0/3 verdict=TARGET_MISSED`
  rc 1 — correctly not met pre-r68.
- Launch commit `40d2bef8` (22:06:33, eight seconds after the `22:06:25` dispatch marker; it carries the
  harness and the dispatch evidence):

```sh
python3 -I quality/counters/c1-r68-selfmutants.py --repo . --rev 40d2bef8964a098ae50f01094fa19e4725952010 \
  --base-rev 510100c81e6cf63fec6be380c2f2f9c670f32cbc --scratch-root <S>/launch-c1
# rc=0
# MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET \
#   rev=40d2bef8964a098ae50f01094fa19e4725952010
```

The same line holds at `67b47df4` (tip when measured); the later tip `20f692be` adds only the
predicate-binding receipt and changes no instrument byte (counter blobs unchanged). Consequence: the C1 target requires no wave-seat
authorship; the wave's C1 seat is measurement/hazard only, so a no-op wave still scores C1 (unless the
harness is subsequently changed). This is not a base-level do-nothing violation (the pre-r68 state is
correctly MISSED) but it is a wave-level do-nothing hazard; the claim's Before/After (base vs REV)
remains honest.

## Closed / acknowledged (verified, not re-opened)

| id | finding | evidence and closure |
|---|---|---|
| C-a | Frozen C2 command included `--scratch-root`, unsupported at freeze → rc 2 | Freeze-byte counter `8eb99a63` on the frozen argv: `error: unrecognized arguments: --scratch-root` rc 2; erratum `.ufo/waves/round-68/c2-command-erratum-r68.txt`; fix `2a39e741`; current counter parses the flag (selftest 25/25); lesson `:211-216` conflict 1. |
| C-b | Freeze-byte C2 verdict ignored the frozen denominator | Freeze-byte counter `8eb99a63` on the readers=12 fixture (`696b216f`): `population=20 readers=12 guarded=12 unguarded=0 controls=11/11 verdict=TARGET_MET` rc 0; erratum `c2-denominator-erratum-r68.txt`; fix `686d6345`; current counter on the same fixture: `TARGET_MISSED` rc 1; lesson `M68-4` (`:58`). |
| C-c | Declaration `:114` cites "control cases 6, 8, 10, 11" as not-guards, but JSON case 6 is `module-const-guard` with `expect_guard=true` | Case map by name: `comment-only-mention` 7, `docstring-only-mention` 8, `unrelated-dict-as-env` 10, `non-reader` 11; lesson `:221-227` records the index-6 drift verbatim; the counter scores by name/expectation, so the predicate is unaffected. |
| C-d | "sha256 recorded in the lesson at freeze" (`:118`, `:142`) | The freeze tree `e0727cda` has no lesson (`git ls-tree -r --name-only e0727cda .ufo/waves/round-68/` → 4 files); the sha `b7a1c939…` is now at `corpus/lessons/round-68.md:9` and in the docs table. The value is recorded; the timing sentence is unfulfillable as written. |
| C-e | The three new instruments broke the standing tool ledger | At `2a39e741`/`425d4b2f`: `LEDGER: population=113 ledger_rows=110 uncovered=3 … verdict=TARGET_MISSED` rc 1 (`quality/check-tool-ledger.py --repo . --rev <rev>`); rows added at `18d692f3` (`quality/tool-ledger.md:149-151`); at `67b47df4`: `113/113 uncovered=0 verdict=TARGET_MET` rc 0. |
| C-f | Duplicate freeze commit | `e6fbe05d…` has the identical tree to `e0727cda`, the same author/committer time, an empty subject, and is kept at `refs/jj/keep/e6fbe05d…`; `git diff e6fbe05d e0727cda` is empty. The main-line/lesson citation `e0727cda` is the correct freeze; no content difference. |

## Assignment items

### 1. Do-nothing control (at `510100c8`)

Both frozen commands were rerun with the current instruments from the lane root:

```sh
python3 -I quality/counters/c1-r68-selfmutants.py --repo . --rev 510100c8… \
  --base-rev 510100c8… --scratch-root <S>/dn-c1
# MADO_R68_SELFMUTANTS: selftest=absent killed=0/3 applied=0/3 base=0/3 \
#   verdict=TARGET_MISSED rev=510100c8… ; rc=1
python3 -I quality/counters/c2-r68-reader-guard.py --repo . --rev 510100c8… \
  --controls .ufo/waves/round-68/controls/c2-controls.json --scratch-root <S>/dn-c2
# MADO_R68_READER_GUARD: population=20 readers=13 guarded=1 unguarded=12 \
#   controls=11/11 verdict=TARGET_MISSED rev=510100c8… ; rc=1
```

Neither target is met by the pre-r68 state: C1's scored harness is absent at the base (0/3 killed; the
three recipes survive the r67 harness, base=0/3), and C2 has one guarded reader of thirteen. A target is
reachable without the claimed work only in the wave-level C1 sense (B7: MET at `40d2bef8`) and, for C2,
without a *behavioral* repair via the uncalled-guard construction (B6); the C2 base itself is not
reachable.

### 2. Predicate-literal binding (character-level)

- **C1 recipes**: the declaration table (`:60-62`) and the counter `RECIPES` (`:42-46`) are byte-identical
  for S1/S2/S3 (script compare: `exact match: True`; find/replace strings identical).
- **C1 frozen line**: `selftest=0` ← `result["rc"] == 0`; `killed=3/3` ← `killed == len(RECIPES)`;
  `applied=3/3` is implied (`killed ≤ applied ≤ 3`); `base=<n>/3` is declared as a wildcard; `rev` is the
  resolved REV. The emitted line at `67b47df4` matches the frozen sentence exactly.
- **C2 frozen line**: `population=20`/`readers=13` are enforced only after `686d6345` (B/C-b);
  `unguarded=0` and every control correct are enforced; `controls=11/11` is **not** enforced (B1); `rev`
  is the resolved REV. The emitted line at `67b47df4`/`379e97f8` matches.
- **Exit rules**: C1 `return 0 if met else 1` (`met = rc==0 and killed==3`), C2 `return 0 if met else 1`
  (`verdict_met` above), `2` on usage/setup. The frozen C2 argv is parseable only after `2a39e741`
  (closed C-a). The C1 kill rule is `selftest rc != 0`; for the actual three recipes the failure is the
  asserted contract line, not a crash — S1/S2 `51/52`, S3 `50/52`, failing
  `MADO_R68_SELFTEST FAIL: scripted none-killed prints the miss line` (reproduced from the scratch
  mutants; `measurement-final-r68.txt`). The rule still counts any nonzero (including a crash) as
  killed; the declaration's Limits ("does not authenticate the harness") bound this, so it is a limit,
  not the round-67 M-R defect in the actual artifact.
- **Guard vocabulary**: the freeze-byte counter lacked the annotated-binding and `update()` shapes named
  at declaration `:110-114`; `686d6345` added them (and the denominator pin), recorded in the denominator
  erratum; the current selftest exercises both (`:324-330`). The frozen 11-case JSON has no update/
  AnnAssign case, so those shapes are selftest-only, not control-set-scored.
- **Doc/label drifts**: B1 (controls count), B4 (`recipe=none`), B5 (`CONTRACT_RE` never applied).

### 3. Causal separability

- Files are disjoint: C1 = `quality/counters/c1-r68-landing-controls.py` (new) + `c1-r68-selfmutants.py`
  (new) + scratch `r68-c1`; C2 = twelve `quality/check-*.py` + `quality/counters/c2-r68-reader-guard.py`
  (new) + `quality/tool-ledger.md` rows. Neither counter reads the other's artifact or scratch.
- C1 without C2: at `40d2bef8` the C1 command is `TARGET_MET` rc 0 (B7) while the C2 command at the same
  rev is `guarded=1 unguarded=12 TARGET_MISSED` rc 1 (reproduced: `.ufo/.../c2-at-40.out`; rev
  `40d2bef8`).
- C2 without C1: a fixture built from the `425d4b2f` `quality/` tree minus
  `c1-r68-landing-controls.py` and `c1-r68-selfmutants.py` (rev `a3863d9c5c091e7bde3ade153ace335122f57bb3`)
  gives `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 TARGET_MET` rc 0; the two C1 files
  are absent from the fixture.
- Both at base: both `TARGET_MISSED` (item 1). Both at `379e97f8`/`67b47df4`: both `TARGET_MET`
  (`measurement-final-r68.txt`; my reruns).

### 4. Axis attribution

- C1 = **calibration**: the scored surface is the control harness's own kill credit / selftest
  discrimination; this is the lane's calibration vocabulary (admission/control instruments), and the
  round-68 SCORECARD row labels C1 calibration.
- C2 = **operability**: gate hardening has that label by precedent (SCORECARD rows 6-9: gate mutation and
  hardening under operability); the round-68 row labels C2 operability.
- The surface actually changed: C1 adds an 834-line harness plus a counter (new denominator 3); C2
  changes 12 gate env constructions plus a census (new denominator 13/20). The published operability
  value `MADO_SELFTEST: 460/460` is unchanged (`measurement-selftests-r68.txt`), and the published
  calibration sub-axis (lesson-grounded criteria) is unchanged. Both claims declare new finite
  denominators, so the labels do not assert movement on those published values. No misattribution
  against precedent; the only axis-posture defect is the stale numbers/citation (B2). One nuance: C2's
  surface (measurement integrity of gates) is calibration-adjacent; the operability label is defensible
  by the gate-hardening precedent but should not be read as a 460/460 movement.

### 5. No-harm inventory

What changes:

1. **Twelve gate env constructions** (all wired to the actual git env, verified by diff of
   `40d2bef8..425d4b2f`):
   - `check-anchor-cover.py:102-104` (env dict passed to `git_blob`),
   - `check-axis-scores.py:97-100` and `:121-124` (env to `subprocess.run`, includes the child
     `check-index.py` run at `:134`/`:155`),
   - `check-control-receipts.py:61-62` (env to `git`),
   - `check-deliverables.py:95-96`, `:115-116` (env to `git show`/`cat-file`),
   - `check-evidence-pointers.py:71-72` (`GIT_ENV`, used at `:82`, `:180`, `:212`),
   - `check-freeze-order.py:45-46` (`git_env`, used at `:57`, `:189`),
   - `check-index-rows.py:56-57` and selftest env `:406`,
   - `check-index.py:49-50` and selftest env `:283`,
   - `check-landed-contract.py:56-57` (env to `git show`),
   - `check-round-outcome-first.py:73-74`, `:127-128`,
   - `check-session-material.py:926-927`, `:983-984`,
   - `check-wave-done.py:186-187` (`git_env`, used at `:195`, `:584`, `:643`, `:953-965`).
2. **One new harness** (`quality/counters/c1-r68-landing-controls.py`, 834 lines) and **two new counters**
   (`c1-r68-selfmutants.py`, `c2-r68-reader-guard.py`). They add three entries to the
   `quality/check-tool-ledger.py` population (`quality/counters/*.py`, direct children): 110 → 113.
   Rows were added at `18d692f3` (`quality/tool-ledger.md:149-151`); the gate is green at the tip
   (`113/113 uncovered=0` rc 0). Before those rows (`2a39e741`, `425d4b2f`) the gate was red
   (`uncovered=3` rc 1, closed C-e).
3. **Docs**: SKILL.md / PROVINCE.md / corpus/QUALITY.md 110 additions at `425d4b2f`; two errata; the
   lesson/knowledge/SCORECARD/LOG landing at later commits. No desktop/compositor/socket/service/package
   write.

Callers / processes that can notice:

- `quality/landing-counters.sh` invokes `quality/check-tool-ledger.py` (the ledger leg) and the r56
  used-by/citecheck children; the ledger leg is the one that saw the 110→113 population change (green
  after `18d692f3`; `measurement-final-r68.txt` shows `LEDGER: 113/113 … TARGET_MET`).
- `quality/check-axis-scores.py` runs `quality/check-index.py` from the blob at `--rev` (two sites); the
  repaired parent passes the guarded env to that child. This is the only cross-gate invocation in
  production (`grep -rn '"quality/check-[a-z-]*\.py"' quality/*.py` → `check-axis-scores.py:134,155`).
- `tools/mado-verify.sh` does not reference `quality/check-*` (`grep -n 'check-' tools/mado-verify.sh` →
  none); its `MADO_SELFTEST: 460/460` is unchanged (`measurement-selftests-r68.txt`).
- Per-round wave scripts/receipts that ran these gates under a planted `refs/replace` now see the real
  objects; no production gate depends on reading replacements (`grep -rn 'refs/replace' quality/ tools/
  scripts/` → only the C1 harness's own fixture strings). Historical receipts pin old blob hashes; a
  re-run of an old receipt that compares a gate's bytes would notice the repair (the 12 files changed at
  `425d4b2f`), but the round's own pinned counters are not touched.
- Gate selftest/live pairs in the seat evidence: `check-index.py --selftest` 12/12, `check-index-rows.py`
  10/10, `check-freeze-order.py` OK, `check-round-outcome-first.py` cases=5, `check-session-material.py`
  94/94, `check-wave-done.py` 62/62, `check-evidence-pointers.py` live run byte-identical
  (`R68ExecGate2.md:76-84`, `R68ExecGate3.md:146-156`). Five gates expose no `--selftest`
  (`R68ExecGate1.md:103`, `R68ExecGate3.md:150`); their paired compile/live runs are in the seat reports. The auxiliary hazard
  probe samples one gate (`R68ExecHazard.md:125-126`, M-R: base forged credit, repaired missing=0,
  killed=yes); 11/12 gates have no runtime hazard receipt (B6).
- New counters' scratch behavior: C1 requires `--scratch-root`; the harness and C1 counter write only
  under it; C2 accepts the flag and writes nothing; no inherited `TMPDIR` is relied on in the primary
  invocations. `quality/counters/__pycache__/` is gitignored (`.gitignore:3`), so the git-object gates do
  not see it.
- Post-freeze instrument changes are recorded: `2a39e741` (argument), `686d6345` (denominator + guard
  shapes) with the two errata; the C1 counter and harness are unchanged since their commits
  (`f131c7f7`, `e970d6ea`).

### 6. Claim sizing

Both targets are finite: C1 = 3 frozen recipes (score `10 × killed / 3`); C2 = 13 readers in a pinned
population of 20 (score `10 × guarded / readers`), 11 controls. The kill rules and the before-values are
in the pre-freeze baseline (`2ca2bec3`, 22:04:23) before the freeze (22:04:51) and the launch
(22:06:25). No universal clause is used to assert more than the finite set: the Limits disclaim universal
self-test soundness, runtime behavior of the gates, object authenticity and lane-wide coverage (lesson
`:33-40`, `:203-208`). The one sentence that reads stronger than the delivered observable is C2's
"a planted `refs/replace` changes the bytes a gate scores" / "must not move a gate's verdict": the census
is construction-only and accepts an uncalled guard (B6). That is disclosed in the Limits but not in the
What-changes sentence. No all/every/complete language otherwise; "every unguarded reader" is finite (12)
and "every tracked file matching `quality/check-[^/]+\.py`" is the pinned 20.

### 7. Chronology

- Baseline commit `2ca2bec3` 22:04:23 (parent `510100c8`) < freeze `e0727cda` 22:04:51 (child of
  `2ca2bec3`) < `w1.ready` mtime 22:05:53 < `w1.ready.dispatched` 22:06:25. The freeze file's worktree
  mtime is 22:04:44, also before launch. This satisfies the declaration's order
  (baseline before freeze; freeze before wave launch).
- The launch commit `40d2bef8` is 22:06:33 (8 s after dispatch) and carries the harness; the C1 target is
  already MET there (B7). The C2 instrument fixes (`2a39e741` 22:09:06, `686d6345` 22:12:03), the gate
  repair (`425d4b2f` 22:12:09), the ledger rows (`18d692f3` 22:14:55) and the landing block
  (`67b47df4` 22:16:45) are all post-launch; the two errata are new files naming what they supersede,
  which the declaration's correction clause permits.
- The duplicate freeze object `e6fbe05d` has the same tree/time as `e0727cda` and is kept under
  `refs/jj/keep/`; the main-line and lesson citation is `e0727cda`. No content difference
  (`git diff e6fbe05d e0727cda` empty).

## Scratch

`/fast/scratch/hyaku/mado-r68/R68CriticClaims/` (fixtures `fixture-deadguard`, `fixture-shrink`,
`fixture-c2only`, the 10-case controls JSON, mutant copies and outputs) removed before yield with
`rm -rf -- /fast/scratch/hyaku/mado-r68/R68CriticClaims`. No production file was written by this seat.
