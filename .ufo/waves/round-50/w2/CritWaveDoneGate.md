# CritWaveDoneGate — round-50 w2 (FALSIFY) — attack on `quality/check-wave-done.py`

Target: the landed WAVE-DONE gate `quality/check-wave-done.py`, frozen sha256
`10f4359ac0af755a4e7bcb1959233862fcde4d1bc895806409b7ea1b054f818c`, scored at attack revision
`b4a79843cc2545bbe800db9322e58f6e00436629` (clone HEAD; `git show <rev>:quality/check-wave-done.py
| sha256sum` reproduces the freeze hash). Method per policy v1: all runs on a
`git clone -q --shared` of the lane under scratch, never in the lane tree; fixtures are their own
git repos under `/fast/scratch/hyaku/mado-r50/CritWaveDoneGate/`, every writer shell ran with
`ulimit -f 65536`, HOME/XDG/TMPDIR pointed inside scratch, no tracked file touched, no host state
read or written. Impacted axis: **operability** (the gate is round-50 criterion 102 / round-49 D2).

## 0. Selftest at the attack rev — 58/58, rc 0

```
$ HOME=<scratch> python3 -I <clone>/quality/check-wave-done.py --selftest --work <scratch>/work-selftest
MADO_WAVE_DONE_SELFTEST: 58/58 passed        rc=0
```
(receipts/selftest.txt, 1.4 s). The pinned `SELFTEST_CHECKS = 58` (`:160`) holds on the landed
bytes.

## (a) results all `output:null` + note, no seat report files — FALSE POSITIVE, and provably blind

Fixture `fp-a-noreports` (rev `de1c0121…`): round-49 tree with `w1.ready`, `w1-dispatch.json`
naming ExecA/ExecB, and `w1-results.json` where both rows are `output: null` + the dispatcher's
own lossy note (`"…not retained — read the seat report file in the wave dir"`,
`scripts/hyaku/inline-dispatcher.py:293-295`). No report file is committed anywhere.

```
WAVE wave=w1 ready=1 results=present seats=2 dispatched=2 settled=2 verdict=OK reason=none
MADO_WAVE_DONE: round=49 waves=1 settled=1 verdict=OK    rc=0
```

Control `fp-a2-reports` (rev `9e82b875…`) is byte-identical except that
`w1/ExecA.md`/`w1/ExecB.md` exist — and produces the **byte-identical verdict lines**. The gate
cannot distinguish "evidence exists" from "no evidence exists"; the information is absent from the
verdict, not merely unenforced.

**Live amplification.** On the real lane at the attack rev, round 50's committed
`.ufo/waves/round-50/w1-results.json` has all 54 rows `output: null` + wrap-up note (verified by
parsing the committed blob: `null-output rows: 54 of 54; with note: 54`), and the gate reads:

```
WAVE wave=w1 ready=1 results=present seats=54 dispatched=54 settled=54 verdict=OK reason=none
MADO_WAVE_DONE: round=50 waves=1 settled=1 verdict=OK    rc=0
```
(receipts/live-round50.txt). Registration itself says w1 was "integrated from the committed seat
reports" because the results file arrived null — i.e. the reports are load-bearing evidence, and
nothing mechanical checks them. Delete every w1 seat report from the tree and this verdict does
not change.

**Contract analysis.** The dispatcher contract makes the note *evidence-pointing*: output was not
retained "— read the seat report file in the wave dir". A gate that certifies `verdict=OK` when
that pointer dangles answers a different question than the dispatcher's note asks. Per the gate's
own declared contract, though, the OK is **per-contract, not a bug**: the docstring scores
"observable terminal states" (`:39-41`) and w1/ExecWaveDone.md declares as Limit 4 "it does not
read seat reports at all". So this is a declared tradeoff, not a hidden hole — but it is a
**false positive against the dispatcher's evidence semantics**, and it is live on round 50 today.
**Smallest safe correction:** in the lossy path of `seat_state` (`:258-260`), when a record is
`output:null` + note, require a report (`<wave>/<name>.md` or `<wave>/<name>/`) to exist in the
round dir at the revision (a `blobs_at` check the tool already performs); otherwise keep the seat
non-terminal with a new state, e.g. `report-missing`. Cost: rounds whose lossy notes point at
never-committed reports would flip to MISSING — which is the honest answer.

## (b) dispatch names `X`, results rename `x `/case — settled if it strips to the dispatch name, duplicate if doubled, mismatch on case-fold

- `fp-b1-ws` (dispatch `ExecA`, results name `"ExecA "` — trailing space): `settled=1 verdict=OK
  rc=0` (rev `5898abb1…`). The pad is silently normalized: `NAME_RE` is matched on
  `name.strip()` (`:241`), the dispatch comparison uses `seat_names` built from
  `name.strip()` (`:372`, compared at `:388-389`), and no `SEAT` line is emitted because the seat
  reads settled — the normalization is invisible in the output.
- `fp-b3-dupe` (results rows `ExecA` + `"ExecA "`): `state=name-duplicate:ExecA`,
  `reason=seats-not-terminal rc=1` (rev `b18785e2…`) — the seen-key is the stripped name
  (`:365-369`), so a padded copy of a present name is caught as a duplicate.
- `fp-b2-case` (dispatch `ExecA`, results `execa`): `reason=dispatch-mismatch missing=1 extra=1
  rc=1` (rev `8dd12d8d…`). Case-fold is not tolerated.

**Answer to the assigned question:** a whitespace-renamed seat is read as **settled** when it is
the only record (the pad vanishes under `strip()`), and as **duplicate** when it doubles a name
already present. Case-fold is **never** settled.
**Defensibility:** not defensible as identity-checking. The dispatcher writes names verbatim —
`res.append({'name': n, …})` where `n` comes straight from `w['names']`
(`inline-dispatcher.py:293`, populated from `tasks` at `:276`) — so a padded results name is pure
record drift, and the gate validates it on stripped bytes (`:241`) yet compares on stripped bytes
too, tolerating exactly the drift it claims to police. The historical safety claimed in
ExecWaveDone.md ("identical in all 13 historical waves, so exact equality is safe") was measured
on *real* dispatcher output, which never pads; the fixture shows the tolerance is exercised only
by mutation. Impact is bounded — the padded name must still strip to a dispatched name, and
duplicates/case-fold still fail — but a results file that renames seat `ExecA` to `ExecA ` passes
the WAVE-DONE gate with no trace. **Smallest safe correction:** emit at least a `NOTE` (or fail)
when `name != name.strip()` in a results record, or compare raw names against the dispatch set;
both are one-line changes near `:241`/`:372`.

## (c) extra seat in results the dispatch lacks — correctly MISSING

`fp-c-extra` (dispatch `ExecA`, results `ExecA`+`ExecB`, both with outputs): `settled=2` but
`reason=dispatch-mismatch`, `SEAT wave=w1 state=dispatch-mismatch missing=0 extra=1`,
`verdict=MISSING rc=1` (rev `1494df16…`). Strict and correct; an undeclared seat cannot inflate a
wave to OK. Defensible per the docstring's "results seat set equals the dispatch taskCall.tasks
name set".

## Verdict

- Selftest: 58/58 at the attack rev — the landed bytes are internally consistent (support).
- (a) **FALSE POSITIVE, live on round 50**: `verdict=OK` certifies a wave whose every seat's
  evidence pointer dangles; defensible only under the gate's own narrower, declared contract
  (docstring + Limit 4), not under the dispatcher contract the note embodies. Fixable defect, not
  a tradeoff the judge must accept, because the declared contract itself flags the limit as a
  limit rather than a pass.
- (b) **Hole (minor)**: whitespace rename of a sole seat is silently normalized to settled; the
  drift is real under the verbatim-name dispatcher contract and leaves no trace in the verdict.
  Duplicate and case-fold variants fail correctly.
- (c) **Correct** (negative control of the attack harness itself).

## Evidence

- `receipts/selftest.txt` — `MADO_WAVE_DONE_SELFTEST: 58/58 passed`, rc 0.
- `receipts/live-round50.txt` — round 50 at `b4a79843…`: `waves=1 settled=1 verdict=OK` rc 0.
- `receipts/fixtures.txt` — the six fixture verdicts quoted above, each with its rev and rc.
- `receipts/fixture-shas.txt` — the six fixture commit ids (fixture trees were scratch-only and
  are deleted; the receipt preserves the pinned inputs' identities, and every fixture is
  reproducible from the JSON shapes named above).

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r50/CritWaveDoneGate/` (shared clone, six fixtures, homes,
logs) deleted after the receipts were copied here. No lane/fleet/home write; no tool installed or
upgraded. Axis: operability.
