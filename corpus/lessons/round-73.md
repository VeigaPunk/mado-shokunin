# mado round 73 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-04 (America/Sao_Paulo)
base: `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce`
frozen declaration: `.ufo/waves/round-73/claims-declaration-r73.md`, `87e4c61ac90e9ac587c9f65ac7844ded268d9046`
control sets: `.ufo/waves/round-73/controls/c1-outcomes-r73.json` sha256
`263b3c5a288c45a59587890a7e4c2e6dc3389630e5dd4a5cd1731976b5d2832b` and
`.ufo/waves/round-73/controls/c2-cases-r73.json` sha256
`65e9464450d58f803ca626f7b7ce6bc4712f46710ac5707602601cee9ecf230d`
pre-freeze baseline: `.ufo/waves/round-73/control-baseline-r73.txt` (held set killed 2/4; held
classifier 25/28)
measured content: `1459cca11fb5d3956a6e9a128217852dd0c28cb9` (both instruments; measurement
`.ufo/waves/round-73/measurement-c1-r73.txt` and `measurement-c2-r73.txt`)

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data; both `TARGET_MET` at the measured
content with the do-nothing controls at their declared scores.

- **C1 calibration — the frozen outcome set separates the four named rule mutations.** The
  round-72 eight-case set passed a rule without the `n > 0` guard and the pre-repair
  prefix-matching parse; the round-73 ten-case set (the eight carried byte-identically plus
  `zero-denominator` and `valid-then-garbled`) separates N1–N4: `cases=10 mutants=4 killed=4
  base_killed=2 verdict=TARGET_MET` rc 0. N1's only separator is `zero-denominator`; N2's only
  separator is `valid-then-garbled`; N4's zero-denominator miss is not a marginal kill (the held
  set already separates N4).
- **C2 operability — the guard census counts the global-declared guard and the mutated
  `os.environ` transport.** `population=20 readers=13 guarded=13 unguarded=0 controls=28/28
  base_controls=25/28 verdict=TARGET_MET` rc 0; the held round-71 classifier misses exactly the
  three new positives.

**Not claimed.** That four named mutations of one rule family are fault coverage; that the
outcome rule authenticates a summary; that the census models execution order (it models line
order), follows an alias of `os.environ`, or interprets values; that the control sets exhaust the
summary grammar or the guard grammar; any desktop, compositor, service or session behaviour (none
was probed); any `[x]`, promotion or axis retirement.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M73-1: the frozen declaration's §C1 counting command omitted `--controls`, so the literal command exits 2 with no contract line — a pasteable-command defect in the freeze itself. | landing | the wave's `R73RevC1` seat replayed the printed line and got exit 2, stderr `--repo, --rev and --controls are required`; the receipt's own invocation in §"After" includes the flag. | `none` — no rule required the declaration's command to be replayed before the instrument's receipt was filed. | Erratum E1 pins the invocation with `--controls .ufo/waves/round-73/controls/c1-outcomes-r73.json`; QUALITY 118 makes a declaration's counting command replayed verbatim, and its red case is exactly this line. |
| M73-2: the first global-guard regression was labelled by execution order (`setup()` called after the launch must not count) while the rule models line order — the label asserted a behaviour the rule does not have. | scope | the counter selftest printed `FAIL: review regression r73-global-rebind-after-use is (True, False)` against a classifier that answers `(True, True)`. | the harness selftest (the label and the rule disagreed on the first run). | The case was replaced by `r73-global-rebind-replaced-between` (a replacement between store and launch, which the rule does refuse) and the line-order approximation is declared in the entry and the declaration. The failure it can show: any future case whose label assumes execution order now fails the selftest. |
| M73-3: the new selftest case literals were first written with doubled newline escapes, so the embedded snippets were invalid Python and classified `(False, False)`. | landing | the counter selftest printed four `FAIL: classify <name> is (True, True)` lines on the first run. | the harness selftest (the embedded table is checked against the classifier). | Escapes fixed; the selftest's embedded-table check is the capture mechanism. The failure it can show: a case whose snippet does not parse is no longer a silent `(False, False)` mismatch. |
| M73-4: the connector item asserted `tools/mado-verify.sh` had never been mutation-scored; it was (round 6, 10/10). | stale-premise | `tools/mado-verify.sh:1886-1904` and `:2074-2076`; `corpus/knowledge/gate-mutation-proof.md`; SCORECARD:21; LOG:297. | the connector seat, on reading the instrument it was told to name. | The connector report records the correction and names `c1-r67-register.py` (after verifying its history) as a genuine candidate. The failure it can show: a prompt premise that a seat's first read contradicts is now a reported correction, not a finding against the lane. |

A fix counts only on its named red/green evidence: M73-1's red is the rc-2 replay of the printed
line and its green is erratum E1's invocation printing the contract line; M73-2's red is the
selftest FAIL line and its green is 75/75 with the replacement case; M73-3's red is the four
`classify … is (True, True)` failures and its green is the same table passing; M73-4's red is the
false premise and its green is the corrected connector report.

## Gate

Admitted, **S447** — CPython v3.14.8 language reference, `Doc/reference/simple_stmts.rst`,
§ The global statement.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (sha256
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41,375 bytes; receipts
  `.ufo/waves/round-73/fetch/Doc_reference_simple_stmts.rst.{1,2,3}`).
- Located quote, 12 words, simple_stmts.rst:972-973 (markup stripped): "The global statement
  causes the listed identifiers to be interpreted as globals."
- Why it grounds C2: the declaration is what makes a store inside a function bind the module
  mapping — the fact the `global_guard` detector rests on.

Admitted, **S448** — CPython v3.14.8 `Doc/library/os.rst`, `.. data:: environ`.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e`, 208,655 bytes).
- Located quote, 21 words, os.rst:193-194: "Changes to the environment made after this time are
  not reflected in os.environ, except for changes made by modifying os.environ directly."
- Why it grounds C2: the store *into* `os.environ` is what updates the mapping, so the store —
  not an inherited environment — is the guard.

Admitted, **S449** — CPython v3.14.8 `Doc/library/subprocess.rst`, the `subprocess.run` `env`
paragraph (S442's document; this row scopes the paragraph).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`, 61,603 bytes — S442's
  recorded digest).
- Located quote, 11 words, subprocess.rst:88-90: "a mapping that defines the environment
  variables for the new process".
- Why it grounds C2: the non-None `env` mapping is the child's whole environment, so a copy of
  the mutated mapping carries the key.

Registry cell changes (old → new, per CORPUS rule 2; only `used-by` changed on a held row):

- **S442** `used-by` `corpus/knowledge/kill-credit-exit-disagreement-r71.md,corpus/lessons/round-71.md,corpus/knowledge/summary-credit-own-detail-r72.md`
  → unchanged this round (S449 is a separate row for the same document at a different scope);
- S447, S448, S449 enter `mined` with `used-by corpus/knowledge/guard-carrier-global-environ-r73.md`.

No `status` or `recheck` cell changed on any held row. Registry 383 → 386 rows; the census
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` printed W04 for
S449's shared URL (the documented duplicate-URL warning across scopes) and E11 until the entry
landed; both the round-start (383, no E-findings) and round-end runs are in the report.

**Reject:** none this round — the three-source set contained no candidate worth refusing. The
registry's most recent rejection is S446 (round 72, `Doc/builtins/stdtypes.rst`).

**Spot-check duty.** The in-round wave seats are the lane's own; the non-author spot-check of
this round's gate decisions (at least one admit and one reject) is the closure's, per LEARNING.md.
The three admits are handed over with URLs, dates and quotes above.

## Assimilation

`Assimilation: none` — `considerthese/` was mined by the wave's `R73ScoutFrontier` seat for the
next round's candidate, but nothing from `/home/vgpnk/Projects/shokuknow/merge/mado/` was adopted
this round: the round's claims are instrument work on the lane's own harness chain, and the
package's staged entries are domain material for a later assimilation round.
