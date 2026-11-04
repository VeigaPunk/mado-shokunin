# mado round 75 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-04 (America/Sao_Paulo)
base: `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`
frozen declaration: `.ufo/waves/round-75/claims-declaration-r75.md`, landed with the instruments at
`def73656c94f0e88bd671cfb4a65124338261722`
control sets: `.ufo/waves/round-75/controls/c1-harness-cases-r75.json` sha256
`f1e851a9d6133b44f6d538e97c8448bbeb174dcb5ba0a6906fe962ed3e8a6c31` and
`.ufo/waves/round-75/controls/c2-cases-r75.json` sha256
`d99502ba23e969a981a856a06742d8da14e1684850c7ca0e0900cd2dc7767897`
pre-freeze baseline: `.ufo/waves/round-75/control-baseline-r75.txt` (held 6/11 and 41/47)
measured content: `4527fcae6a8619e890172ca0a616ae8a3e20fd87` (final receipts
`measurement-c{1,2}-r75-final.txt`; the earlier receipts at `def73656…`, `e3e29bb4…`,
`f75afbf6…` are kept beside them, append-only)

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data; both `TARGET_MET` at the measured
content with the do-nothing controls at their declared scores.

- **C1 calibration — the harness credits a kill only on the run's own echo of its challenge.**
  The round-74 rule's declared limit ("not wired into the frozen round-72 harness") is closed by
  `quality/counters/c1-r75-landing-controls.py`: it loads the frozen generation (sha256 pinned),
  draws one `secrets.token_hex(8)` per run, hands it to the child in `MADO_LANDING_NONCE`, and
  credits the M-Z kill and greens the outcome only when the child's last parsed
  `MADO_LANDING_WITNESS: <16 hex>` equals it byte-exactly. Eleven real `bash` fixture modes
  through the actual harness pipeline: `cases=11 correct=11 base_correct=6`. The held harness
  scores 6/11 and misses exactly the five witness separators.
- **C2 operability — the census counts key-carrying copies and the literal-key delete.** The
  successor adds a name-neutral keyed-mapping rule (`child = dict(env, KEY="1")`,
  `{**env, KEY: "1"}`, handed as `env=child`) and a `del env[KEY]` cancellation. Forty-seven
  frozen cases (36 carried byte-identically + 11 appended): `controls=47/47 base_controls=41/47`;
  population unchanged at `20 readers=13 guarded=13 unguarded=0`. The held classifier misses
  exactly the four copy positives and the two deletion cancellations.

**Not claimed.** That the challenge authenticates the assertions; that the eleven modes are fault
coverage; that the C1 counter certifies the outcome clause (it scores the M-Z decision only — the
critic's finding, declared); any desktop, compositor, service or session behaviour (none was
probed); any `[x]`, promotion or axis retirement.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M75-1: the frozen declaration's no-harm line listed `tools/mado-verify.sh` as staying byte-identical while the same declaration's D5 disposition amended it (the `/tmp` scratch repair), and the amendment moved the gate's self-pin. | scope | `claims-declaration-r75.md` § No-harm vs § Routed-defect dispositions; the gate diff at `b545bea9`; receipts `red-scratch-before.txt` (TMPDIR ignored, 460/460) and `green-scratch-after.txt` (refusal) / `green-scratch-valid.txt` (460/460). | none — the freeze statement and the disposition contradicted each other in one file and no criterion compared them. | The report and the round-75 SCORECARD row declare the amendment and the `PIN_MADO` re-cut (`367ff5ec…` → `49567a0f…`) instead of claiming byte-identity; the gate is re-measured 460/460 at the amended bytes. The failure it can now show: a no-harm list that names an instrument the same round edits. |
| M75-2: the sentinel's hardening (a private `mkdtemp` generation dir under the validated scratch) made the C1 counter score `correct=0/11` — `mkdtemp(dir=scratch)` ran before the validated root existed, so every case printed `candidate=absent`; the instrument's `--selftest` passed throughout. | landing | `.ufo/waves/round-75/measurement-c1-r75-final.txt` at `f75afbf6…` (`cases=11 correct=0 base_correct=6`) versus the same file at `4527fcae…` (`correct=11`); the loader trace `FileNotFoundError: …/r75-c1-gen-…`. | none — the selftest validated the scratch path but not the allocation, and no rule required a counter run after a hardening change. | `os.makedirs(scratch, exist_ok=True)` before `mkdtemp`; the counter was re-run and the `/tmp`-free receipts kept. The failure it can now show: a repair that only the selftest path touches and the counter has not exercised. |
| M75-3: C2's frozen `del-before-store` fixture deletes a key that its own mapping never had, so the source would raise `KeyError` before any launch — the label pins the syntactic ordering rule, not a reachable runtime state. | survivor | `controls/c2-cases-r75.json` case `del-before-store`; the round's C2 executor hand-check (`w1/R75ExecC2.md`). | the round's executor hand-check (no criterion required a fixture's runtime reachability before the freeze). | The frozen case is not re-cut; the knowledge entry and this row state the limit, and the successor shape initialises the key before the delete. The failure it can now show: a frozen fixture whose source cannot execute as written. |
| M75-4: C1's `uppercase-echo` separator is probabilistic — `token_hex(8)` can draw sixteen decimal digits (`(10/16)^16 ≈ 5.4e-4`), uppercasing which leaves the challenge byte-identical, so a correct implementation can miss the label through no defect. | survivor | the critic's re-derivation (`w1/R75Critic/rederived-controls.txt`) with the deterministic challenge `1234567890123456`. | the round's critic (no criterion required a frozen separator to be deterministic). | The frozen label stands and the probability is disclosed in the entry and the report; a successor denominator forces a case-changing challenge. The failure it can now show: an oracle whose expected value is only probabilistically reachable. |
| M75-5: the round-74 closure's D1 (the witness-rule selftest tally 21/21 where the rule prints 23/23) survived a round in `SKILL.md:734` and the round-74 LOG bullet. | number-drift | `SKILL.md` row `mado-r74-witness-rule` (now 23/23) and the LOG correction appended this round; the rule prints `23/23` (`w1/R75ExecGate/c1-r74.txt`). | the round-74 closure spot-check D1 (routed; not repaired until now). | The row is corrected in place and the LOG correction appended; the row is also reclassified `probe` as D5 advised. The failure it can now show: a stale tally copied from a planning note instead of the run. |
| M75-6: the round-74 closure's D2 (post-repair instrument selftest receipts unlanded) repeated in this round's first landing: the freeze commit carried no selftest stdout, and the sentinel could not verify the scratch receipts because `green-scratch-valid.txt` was still empty when read. | landing | `.ufo/waves/round-75/receipts/` (now `gate-selftest-r75.txt`, `host-*` absent, `green-scratch-valid.txt` 460/460) and the sentinel's § Scratch disposition. | the round-74 closure spot-check D2 (routed); the sentinel re-found the shape. | The receipts are committed with their commands and rc, and the receipts directory is named in the report. The failure it can now show: a claim whose selftest is described but whose stdout is not committed. |
| M75-7: the declaration's planning line says "ONE v1 wave of 12 seats"; thirteen seats were dispatched and settled (round-74's D4 repeated). | number-drift | `claims-declaration-r75.md` line 6 versus `w1-dispatch.json` `counts.spawn=13` and the registry's thirteen members. | the round-74 closure D4 (routed); the same planning line was copied again. | Disclosed in the report; the frozen file is not rewritten (the seat count is a planning line, not a claim predicate) and the next declaration will carry the actual count. The failure it can now show: a planning number never re-derived from the dispatch. |

A fix counts only on its named red/green evidence: M75-1's red is the declaration's contradictory
lines and its green the amended gate at 460/460 with the pin moved; M75-2's red is `correct=0/11`
at `f75afbf6…` and its green `correct=11/11` at `4527fcae…`; M75-3's red is the fixture's
`KeyError` path and its green the declared limit in the entry; M75-4's red is the deterministic
digits-only challenge scoring a false miss and its green the disclosed probability with the frozen
label intact; M75-5's red is `21/21` in `SKILL.md` and its green `23/23` after the correction;
M75-6's red is the empty receipt file the sentinel read and its green the committed
`green-scratch-valid.txt`; M75-7's red is `12` in the declaration and its green the dispatch's 13.

## Gate

Admitted, **S453** — CPython v3.14.8 language reference, `Doc/reference/simple_stmts.rst`,
§ The ``del`` statement.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (sha256
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41,375 bytes; receipts
  `.ufo/waves/round-75/fetch/simple_stmts.rst.{1,2,3}`).
- Located quote, 13 words, simple_stmts.rst:468-469 (markup stripped): "Deletion of attribute
  references and subscriptions is passed to the primary object involved".
- Why it grounds C2: `del env[KEY]` is a subscription deletion, so the key is removed from the
  very mapping a later copy or `env=` launch hands to the child.

Admitted, **S454** — CPython v3.14.8 library reference, `Doc/builtins/stdtypes.rst`,
§ Mapping Types — dict, the `dict(mapping, /, **kwargs)` constructor (`:5325-5327`) and its
argument paragraph (`:5350-5352`).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`
  (the 3.14 tree's real path; `Doc/library/stdtypes.rst` returns HTTP 404 three times, the S446
  record re-confirmed this round).
- Access date: 2026-11-04, three times byte-identical (sha256
  `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`, 248,201 bytes; receipts
  `.ufo/waves/round-75/fetch/builtins_stdtypes.rst.{1,2,3}`).
- Located quote, 21 words, builtins_stdtypes.rst:5350-5352: "If keyword arguments are given, the
  keyword arguments and their values are added to the dictionary created from the positional
  argument".
- Why it grounds C2: `child = dict(env, KEY="1")` is a new mapping that holds the guard key in key
  position, independently of the name it is bound to.

**Re-opened reject, S446** — CPython 3.14.8 `Doc/builtins/stdtypes.rst`, mapping methods.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`
- Access date: 2026-11-04 (the round-74 re-open; this round only re-confirmed the 404 at
  `Doc/library/stdtypes.rst` and the digest of the real path).
- **Record correction (routed D3):** the round-74 Gate line says the `setdefault` quote is 23
  words; the quoted sentence tokenises to **21** (`len(q.split())`), the closure spot-check's
  reading. The ≤25-word rule is not violated; S446 stays rejected at its method-behaviour scope,
  and the round-75 rows are separate scopes, not supersessions.

Registry cell changes (old → new, per CORPUS rule 2; no held cell changed in place):

- S453 and S454 enter `mined` with `used-by` `corpus/knowledge/guard-carrier-copy-del-r75.md`.
- Both rows are different-scope repetitions of documents already held (simple_stmts.rst ←
  S440/S447/S451; builtins/stdtypes.rst ← S446), so each raises the documented non-failing W04
  warning; neither carries `supersedes`, because no held row is replaced.

Registry 389 → 391 rows. Census, round start (base revision mirror,
`git archive b149d2e` + the fleet conf, at `.ufo/waves/round-75/census-start-r75.txt`):
`validate --root <scratch>/fleet-base mado` → exit 0, 45 warning lines. Round end
(`census-end-r75.txt`): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` → exit 0, 47 lines (45 + the two new W04).

**Spot-check duty.** The in-round wave seats are the lane's own; the non-author spot-check of this
round's gate decisions (at least one admit and one reject) is the closure's, per LEARNING.md. The
two admits and the re-opened reject are handed over with URLs, dates and quotes above.

## Assimilation

`Assimilation: none` — the round's claims are instrument work on the lane's own harness chain;
nothing from `/home/vgpnk/Projects/shokuknow/merge/mado/` was adopted this round. The connector's
`considerthese/` read is recorded in its findings and carried to the next round's candidate list.
