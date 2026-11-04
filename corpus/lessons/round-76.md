# mado round 76 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-04 (America/Sao_Paulo)
base: `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`
frozen declaration: `.ufo/waves/round-76/claims-declaration-r76.md`, freeze v1 `755b339f…`
(controls + instruments), freeze v2 `cb713254ee9926e036e594312fdc61b57825526b` (label set v3,
named outcome rule, observable mutant class)
control sets: `controls/c1-outcome-cases-r76.json` v3 sha256
`320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea` (16 cases) and
`controls/c2-cases-r76.json` sha256
`df9e89841ed560613d7a05ad50f345b2d6bbf0d8e40a98f51e8b8134492b3948` (59 cases)
pre-freeze control: `.ufo/waves/round-76/control-baseline-r76.txt` (held mz-only rule 0/4;
held round-75 classifier 55/59)
measured content: `cb713254…` (receipts `measurement-c{1,2}-r76.txt`)

## Outcome and boundaries

Two bounded claims, both frozen before any seat scored; both `TARGET_MET` at the measured
content with do-nothing controls at their declared scores.

- **C1 calibration — the counter certifies the harness's contract outcome field.** Sixteen
  frozen fixture modes scored on both `mz=` and `verdict=`; four named mutations of the
  harness's `outcome_green` rule killed 4/4 (scores 15/16, 15/16, 15/16, 14/16), while the
  held mz-only rule kills 0/4 (`cases=16 correct=16 mutants=4 killed=4 base_killed=0`). Two
  mechanical fixes ride along: the witness grammar reads 16+ hex (an over-long echo is a
  parsed mismatch) and the challenge always contains an `a-f` letter (deterministic uppercase
  oracle, closing M75-4).
- **C2 operability — the census counts interprocedural and dynamic-key deletions.** Fifty-nine
  frozen cases (47 carried byte-identically + 12 appended): `controls=59/59
  base_controls=55/59`, population unchanged at 20 readers / 13 guarded / 0 unguarded.

**Negative result (lands with the round).** The round-75 plan's first item — kill the
echo-dropping outcome mutation — is impossible through `verdict=`: the field is green only
when `killed == 2`, and the M-Z kill already requires the echo, so the mutation changes no
reachable published field. The finding is recorded in
`corpus/knowledge/outcome-field-r76.md` §2 and the claim moves to the observable class.

**Not claimed.** That the challenge authenticates the assertions; that the sixteen modes are
fault coverage; that the echo term is certified through `verdict=`; that D3 covers the
attribute or `os.environ` transport flows; any desktop, compositor, service or session
behaviour (none was probed); any `[x]`, promotion or axis retirement.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M76-1: label set v1 modelled the harness's `verdict=` as summary-green only; the harness greens it only when the extracted instrument is green AND both baseline mutants were killed, so three labels were wrong and the candidate scored `correct=12/15` at the first measurement. | label | `.ufo/waves/round-76/measurement-c1-r76.txt` as first produced (`correct=12/15`, three `correct=no` rows) versus the re-derived labels in `receipts/label-derivation-r76.txt`. | none — no criterion required a frozen label to be derived from the instrument's own evidence lines before the freeze. | The labels are re-derived from `MADO_R76_SELFTEST ... green=` and `MADO_R76_MUTANT M-Z/M-R ... killed=` only, committed as a receipt, and the declaration says so; QUALITY 128 makes that a bar. Failure it can now show: a label that the instrument's own evidence lines contradict. |
| M76-2: label set v2 kept the echo-dropping outcome mutation the round-75 plan named; that mutation is unobservable through `verdict=` because `killed == 2` already requires the echo, so the frozen target could not be reached by construction (`killed=0/4`). | false ground | `.ufo/waves/round-76/measurement-c1-r76.txt` v2 run (`mutants=4 killed=0`) and the case table in `corpus/knowledge/outcome-field-r76.md` §2. | none — no criterion required a frozen separator to be reachable through the field it is scored through. | The claim moves to the four observable outcome-rule mutations (`outcome-summary-only`, `-killed-only`, `-killed-any`, `-killed-or`) with `always-red` as the shape that separates a rule ignoring the green conjunct; the negative result is recorded instead of claimed; QUALITY 129. Failure it can now show: a frozen mutation whose behaviour is identical to the correct rule on every reachable case. |
| M76-3: the pre-freeze control's mutant leg parsed `MADO_R76_*` rows with a regex anchored to end-of-line while the row carries a trailing `sha256=`, so every mutant scored `0/15` and the control printed `killed_by_held_rule=yes` for mutations that were in fact unobserved. | instrument | `.ufo/waves/round-76/control-baseline-r76.txt` first produced (four `mz_score=0/15` rows) versus the final receipt (`15/15`, `killed_by_held_rule=no`). | none — a leg that finds no row at all printed a score instead of failing. | Both regexes use `search` on the parsed line, and a missing row is visible because the score is reported per mutant; QUALITY 130. Failure it can now show: a leg that silently measures nothing and reports 0%. |
| M76-4: the C1 fixture template's first draft made `green-mutant`'s outcome expectation `pass`, but the contract's `killed=1/2` (the green summary never kills M-Z) makes it `fail`; the same draft assumed `right` could not green the outcome. | label | the case table in `receipts/label-derivation-r76.txt` at v1 (`right` and `liar-success` derived `pass`, `green-mutant` derived `fail`). | the derivation receipt itself (a label that disagrees with the instrument's own lines is reported, not silently accepted). | The derivation catches it before the wave; the frozen v3 labels equal the derived values for all sixteen cases. Failure it can now show: a label the derivation disagrees with. |

A fix counts only on its named red/green evidence: M76-1's red is `correct=12/15` and its
green `correct=16/16` with the derivation receipt agreeing on all sixteen labels; M76-2's red
is `killed=0/4` and its green `killed=4/4` on the observable class with the negative result
written down; M76-3's red is four `0/15` mutant rows and its green four `15/16`-or-better
rows; M76-4's red is the v1 label/derivation disagreement and its green the v3 equality.

## Gate

Admitted, **S455** — CPython v3.14.8 language reference, `Doc/reference/expressions.rst`,
§ Calls, parameter call semantics.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (sha256
  `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92,034 bytes; receipts
  `.ufo/waves/round-76/fetch/expressions.rst.{1,2,3}`).
- Located quote, 18 words, expressions.rst:1350-1351 (markup stripped): "argument is placed in
  the slot, filling it (even if the expression is None, it fills the slot)."
- Why it grounds C2/D3: the callee's parameter holds the caller's argument object, so a
  `del m[KEY]` in the callee mutates the mapping the caller later hands to the child.

Admitted, **S456** — CPython v3.14.8 language reference, `Doc/reference/simple_stmts.rst`,
§ The del statement.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41,375 bytes; receipts
  `.ufo/waves/round-76/fetch/simple_stmts.rst.{1,2,3}`).
- Located quote, 10 words, simple_stmts.rst:463-464: "Trying to delete an unbound name raises
  a NameError exception."
- Why it grounds C2/D4: a dynamic delete key must be *bound before* the delete, so the rule
  resolves a name bound once and earlier, never a name bound after it.

**Re-opened reject, S446** — CPython 3.14.8 `Doc/builtins/stdtypes.rst`, mapping methods.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`
- Access date: 2026-11-04 (re-opened; the three-fetch digest is unchanged from round 75,
  `5a6951b7…`, 248,201 bytes).
- Rejected at its method-behaviour scope (argument forms and defaults); no admitted round-76
  entry cites it. Flip condition unchanged: a mapping-method claim. S454's constructor row
  remains the separate, admitted scope.

Registry cell changes (old → new, per CORPUS rule 2; no held cell changed in place):

- S455 and S456 enter `mined`, tier A, `used-by` `corpus/knowledge/interprocedural-del-r76.md`.
- Both rows share a document with held rows (expressions.rst ← S443; simple_stmts.rst ←
  S440/S447/S451/S453), so each raises the documented non-failing W04 warning; neither
  carries `supersedes`, because no held row is replaced.
- **S450 `used-by`** changes old → new: `corpus/knowledge/replay-witness-credit-r74.md` →
  `corpus/knowledge/replay-witness-credit-r74.md, corpus/knowledge/outcome-field-r76.md` (the
  round-76 C1 entry cites it).
- S453's `used-by` is unchanged: the round-76 C2 entry re-cites it, and the entry names it in
  its sources line without a registry edit (the row already names a round-75 entry).

Registry 391 → 393 rows. Census, round start (`census-start-r76.txt`, run at round start):
`validate --root /home/vgpnk/Projects/shokunin mado` → exit 0, 47 lines. Round end
(`census-end-r76.txt`): same command → exit 0, 49 lines (47 + the two new W04 warnings).

**Spot-check duty.** The in-round wave seats are the lane's own; the non-author spot-check of
this round's gate decisions (at least one admit and one reject) is the closure's, per
LEARNING.md. The two admits and the re-opened reject are handed over with URLs, dates and
quotes above.

## Assimilation

Assimilation: none this round (no `merge/mado/` package adopted; the round states it in the
report's Sources & frontier section). considerthese mined: proposal 5 of
`considerthese/2026-10-28.md` ("separate relayed from re-measured in every number") lands as
QUALITY 131.
