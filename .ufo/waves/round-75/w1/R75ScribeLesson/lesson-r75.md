# mado round 75 — lesson (DRAFT SKELETON)

author: mado L1 (the scored instruments are the L1's own; this skeleton was drafted by the
wave's R75ScribeLesson seat, and every `<L1>` cell plus the landed states are the L1's to finish
before this file enters `corpus/lessons/`).
date: 2026-11-04 (America/Sao_Paulo)
base: `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6` (round-74 closure tip; lane clean at freeze:
`tracked=0 untracked=0`)
frozen declaration: `.ufo/waves/round-75/claims-declaration-r75.md`, landed with the instruments
at `def73656c94f0e88bd671cfb4a65124338261722`
control sets: `.ufo/waves/round-75/controls/c1-harness-cases-r75.json` sha256
`f1e851a9d6133b44f6d538e97c8448bbeb174dcb5ba0a6906fe962ed3e8a6c31` and
`.ufo/waves/round-75/controls/c2-cases-r75.json` sha256
`d99502ba23e969a981a856a06742d8da14e1684850c7ca0e0900cd2dc7767897`
pre-freeze baseline: `.ufo/waves/round-75/control-baseline-r75.txt` (held round-72 harness 6/11;
held round-74 classifier 41/47; the receipt carries its base revision on every leg, per
round-74's carried note "stamp pre-freeze receipts")
measured content: `def73656c94f0e88bd671cfb4a65124338261722` (both instruments; measurements
`.ufo/waves/round-75/measurement-c1-r75.txt` and `measurement-c2-r75.txt`)

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data; both `TARGET_MET` at the measured
content with the do-nothing controls at their declared scores (C1 6/11 and C2 41/47 in
`control-baseline-r75.txt`).

- **C1 calibration — the successor landing harness credits the M-Z kill and greens the outcome
  only on the run's own echo of a per-run challenge.** The held round-72 harness, extracted at
  the base revision and run through the real harness pipeline (fixture git repo → harness
  extraction → M-Z clause deletion → contract line), scores `6/11` on the eleven frozen fixture
  modes: it credits `right` and `liar-success` genuinely and still credits `uppercase-echo`,
  `stale-witness`, `absent-witness`, `wrong-witness` and `last-wins-wrong` on arithmetic alone.
  The successor `quality/counters/c1-r75-landing-controls.py` loads the frozen round-72
  generation from the measured repository (bytes pinned by sha256), draws one
  `secrets.token_hex(8)` challenge per run in `MADO_LANDING_NONCE`, and credits the kill and
  greens the contract outcome only when the round-72 arithmetic holds **and** the child's last
  parsed `MADO_LANDING_WITNESS: <16 hex>` line equals the challenge byte-exactly:
  `MADO_R75_HARNESS_WITNESS: cases=11 correct=11 base_correct=6 verdict=TARGET_MET` rc 0
  (`measurement-c1-r75.txt`).
- **C2 operability — the guard census counts key-carrying copies bound to any name and treats
  `del env[KEY]` as a cancellation.** The held round-74 classifier scores `41/47` on the frozen
  forty-seven-case set, missing exactly the four copy positives (`copy-dict-kw-bound`,
  `copy-splat-bound`, `copy-dict-builtin-bound`, `copy-dict-literal-base`) and the two `del`
  negatives (`del-env-store-cancel`, `del-env-literal-cancel`). The successor counts any simple
  name bound to a mapping that carries the guard key in key position and handed as `env=`, under
  the same dominance test, and treats `del env[KEY]` (literal key, same scope) strictly between
  the guard construction and the launch as a cancellation: `MADO_R75_GUARD_SHAPES: population=20
  readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET` rc 0
  (`measurement-c2-r75.txt`). The thirty-six round-74 cases are carried byte-identically
  (`MADO_R75_HELD_CONTROLS … carried=yes`).

**Not claimed.** That the challenge authenticates the truth of the assertions (it authenticates
the run's echo); that the eleven modes or the forty-seven cases are fault coverage; that the
fixture lanes are the production instrument (they are test doubles); that the successor
re-implements the extraction or the M-R leg (it composes the frozen generation by import);
that the census models execution order, chains aliases, or interprets values; that `del` is
modelled beyond a literal key in the same scope; any desktop, compositor, service or session
behaviour (none was probed); any `[x]`, promotion or axis retirement.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M75-1: the round-74 witness-rule selftest tally was recorded as 21/21 in `SKILL.md` (`mado-r74-witness-rule`) and in `LOG.md`'s round-74 instruments bullet, while the rule's own `--selftest` prints 23/23 — a stale count that survived a full round (round-74 closure D1). | number-drift | `<L1>` (the stale cells quoted and the re-derived selftest line: `SKILL.md:734` now carries "23/23, corrected from the stale 21/21 at round 75" with class `probe`; the append-only LOG correction line quoted; `LOG.md:3657-3658` still shows 21/21 until the correction lands). | the round-74 closure spot-check §6 D1. | The SKILL row is corrected in place and the LOG correction appended append-only. The failure it can now show: a tally a record carries is re-derived from the instrument's own `--selftest` output before it is cited anywhere. |
| M75-2: the round-74 declaration's D2 disposition promised committing the post-repair selftest receipts at the measured commit, and round 74 landed none — the only committed selftest stdout was the pre-repair `w1/R74ExecC2/selftest.stdout.txt` (86/86) and `receipts/gate-selftest-r74.txt` (460/460) (round-74 closure D2). | landing | `<L1>` (the round-75 receipt `.ufo/waves/round-75/receipts/selftest-r75.txt` resolved at the measured commit with `--controls` named — C2 prints 84/84 without `--controls` and 86/86 with it; the receipt's instrument selftest lines quoted). | the round-74 closure spot-check §6 D2. | The receipts are committed with `--controls` named. The failure it can now show: a disposition that names a receipt path resolves to a file at that path, or the round cannot close. |
| M75-3: the round-74 lesson's Gate says the S446 `setdefault` quote is 23 words; the quoted sentence tokenises to 21 (whitespace-split of the markup-stripped sentence) — the ≤25-word rule holds either way, the count does not (round-74 closure D3). | number-drift | `<L1>` (the re-tokenisation command and its output, 21; the round-74 Gate line cited, never rewritten). | the round-74 closure spot-check §4 count defect → §6 D3. | The corrected count stands recorded in this lesson (21 words); no held cell is edited. The failure it can now show: a count the bytes do not produce is caught by re-tokenising the quoted string. |
| M75-4: round-74's frozen declaration says "ONE v1 wave of 12 seats" while 13 seats were dispatched and settled (`spawn=13 resume=0`) — a planning line, not a claim predicate (round-74 closure D4). | planning | `<L1>` (the round-74 declaration shape line and `w1-dispatch.json` `counts` quoted side by side). | the round-74 closure spot-check §1 conformance defect → §6 D4. | The actual dispatched size is disclosed in this round's report and in M75-7 below; the next declaration takes the count from the dispatch record. The failure it can now show: a shape line that the dispatch record contradicts is caught by diffing the declaration against `counts.total` before freeze. |
| M75-5: the round-75 L1 ran a three-case plumbing run of the C1 candidate harness (`right`, `stale-witness`, `crash`) **before** the declaration froze — the candidate instrument executed pre-freeze. The declaration self-discloses the run, states it produced the labels the frozen set carries, and that no case, label, predicate, target or counter was re-cut after it; the baseline receipt stamps its base revision on every leg (round-74's carried erratum (c) answered). | freeze-order | `<L1>` (the disclosure paragraph quoted; the frozen `c1-harness-cases-r75.json` blob id equal at base and tip; the baseline receipt's rev stamps quoted). | self-disclosed pre-freeze (the declaration's own "Pre-freeze disclosure" paragraph). | The run stays bounded by its disclosure and the frozen set carries its labels unchanged; future plumbing runs are scratch-only with stamped receipts. The failure it can now show: a pre-freeze run that re-cuts a frozen input is caught by the freeze-order blob comparison and the do-nothing control. |
| M75-6: the declaration's sources plan anchors the second new row at `Doc/library/stdtypes.rst`, which serves no bytes at tag v3.14.8 (HTTP 404, curl rc 22, three attempts) — the same 404 round 73 already repaired when it re-anchored S446 at `Doc/builtins/stdtypes.rst` (`corpus/SOURCES.md` records the round-71 citation 404ing on all three attempts). The real tag path's bytes hash `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1` (248,201 B, three byte-identical scratch fetches) — exactly S446's recorded digest. | landing | `<L1>` (the three 404 attempts and the three byte-identical `Doc/builtins/stdtypes.rst` receipts under `.ufo/waves/round-75/fetch/`, with digests; the declaration line and SOURCES S446 quoted). | this seat's own read (R75ScribeLesson), pre-landing. | S454 anchors at `Doc/builtins/stdtypes.rst`; the declaration's URL stands as the record defect named here, never rewritten. The failure it can now show: a pinned URL that returns 404 is caught by the three-fetch duty itself, before a row lands. |
| M75-7: the stale seat count repeated: this round's declaration also says "ONE v1 wave of 12 seats" while `.ufo/waves/round-75/w1-dispatch.json` counts `spawn=13 resume=0 total=13` and the wave registry lists 13 members — D4's disposition ("disclose the actual wave size … next round") did not reach the declaration it governs. | planning | `<L1>` (the round-75 declaration shape line, the dispatch `counts`, and the 13 member ids quoted). | this seat's own read (R75ScribeLesson), pre-landing. | The report states 13; the next declaration's shape line is generated from `counts.total`, not from the plan. The failure it can now show: the declared/dispatched size mismatch is caught before freeze instead of by the closure. |

A fix counts only on its named red/green evidence: M75-1's red is the stale 21/21 cells and its
green the rule's own selftest line `<L1>`; M75-2's red is the absent receipt path and its green
`receipts/selftest-r75.txt` with `--controls` named `<L1>`; M75-3's red is the round-74 Gate's
23 and its green the re-tokenised 21 `<L1>`; M75-4/M75-7's red is the declaration shape line and
its green the dispatch `counts.total=13` `<L1>`; M75-5's red is the disclosed pre-freeze run and
its green the unchanged frozen control blob plus the stamped baseline receipt `<L1>`; M75-6's
red is the three 404s and its green the three byte-identical `Doc/builtins/stdtypes.rst` fetches
`<L1>`.

## Gate

The round opens two rows (S453, S454) and keeps one reject. The wave's sources scout's
`sources.md` carries the round's numbers; these were independently derived by this seat's own
three-fold fetches of the same URLs, and where the two derivations differ the landed fetch
receipts decide and this skeleton is corrected before landing. The fetch receipts land at
`.ufo/waves/round-75/fetch/` (the declaration's receipts directory).

Admitted, **S453** — CPython v3.14.8 language reference, `Doc/reference/simple_stmts.rst`,
§ The `del` statement.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41,375 bytes — the same
  bytes S447 and S451 record; the documented W04 duplicate-URL pairs S453/S447 and S453/S451
  are expected at the census).
- Located quote, 13 words, simple_stmts.rst:468-469 (markup stripped): "Deletion of attribute
  references and subscriptions is passed to the primary object involved".
- Why it grounds C2: the subscription delete is passed to the primary object, so
  `del env["GIT_NO_REPLACE_OBJECTS"]` mutates the very mapping handed to the child — a delete of
  the guard key strictly between the guard construction and the launch is a cancellation, while
  a delete of another key and a delete before the store cancel nothing.
- Duty `<L1>`: re-derive digest, byte count, quote span and word count from the landed
  receipts (`fetch/simple_stmts.rst.{1,2,3}`) before the row lands; count words by tokenising,
  never by eye (M74-5's rule).

Admitted, **S454** — CPython v3.14.8 language reference, `Doc/builtins/stdtypes.rst`,
§ Mapping Types — `dict` (the declaration's sources plan names `Doc/library/stdtypes.rst`, the
round-71 404 path; the row lands at the real tag path — M75-6).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`, 248,201 bytes — the same
  bytes S446 records; the documented W04 duplicate-URL pair S454/S446 is expected at the
  census).
- Located quote, 21 words, builtins/stdtypes.rst:5350-5351 (markup stripped): "If keyword
  arguments are given, the keyword arguments and their values are added to the dictionary
  created from the positional argument."
- Why it grounds C2: `dict(env, GIT_NO_REPLACE_OBJECTS="1")` is the constructor's
  positional-plus-keyword creation, so a copy bound to any name and handed as `env=child`
  carries the guard key; a copy without the key, a key in value position and a rebound copy stay
  unguarded — the four frozen copy positives separate exactly there.
- Scope note: the admit scope is the constructor's keyword-pair copy; it does not flip S446's
  reject, whose scope is mapping-method behaviour (`update`, `setdefault`) — different scopes of
  one document, no supersession.
- Duty `<L1>`: same derivation from the landed receipts (naming per the scout's receipts).

Rejected — `Doc/library/random.rst` (the C1 challenge alternative; this seat's proposed stanza,
kept only if the L1 adopts it).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/random.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `18235d86c91f69256453f300dfbc3c0dbfe8068099c9ba5ed877d3dd75547ab4`, 30,766 bytes).
- Located quote, 22 words, random.rst:46-48 (markup stripped): "The pseudo-random generators of
  this module should not be used for security purposes. For security or cryptographic uses, see
  the `secrets` module."
- Why it stays rejected: the module declares its own generators unfit for security purposes and
  redirects them to `secrets` — the dependency S450 already grounds — so it can ground no
  challenge claim; a captured replay is an adversarial case, not a statistical one. Flip: a rule
  that needed reproducible, seed-fixed per-run values (not unpredictability) would turn to
  `random`.
- Duty `<L1>`: if kept, land the three receipts under `.ufo/waves/round-75/fetch/` with the same
  trio discipline; if dropped, record the drop here and nothing lands.

Registry cell changes (old → new, per CORPUS rule 2; no held cell changed in place):

- S453, S454 enter `mined` with `used-by` `<L1>` (the knowledge-entry paths the round's entries
  seat lands: the del-cancellation and dict-copy carriers).
- S446 keeps its `status`, `recheck` and `used-by`; S454 adds the constructor-copy scope beside
  the mapping-method reject scope on the same document — no supersession, no digest edit.
- Registry 389 → 391 rows; the census `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mado` runs at round end with the expected W04 duplicate-URL
  warnings (S453 with S447 and S451; S454 with S446) and exit 0 `<L1>` (round-start and
  round-end runs cited in the report).

**Spot-check duty.** The in-round wave seats are the lane's own; the non-author spot-check of
this round's gate decisions (at least one admit and one reject) is the closure's, per
LEARNING.md. The two admits and the reject are handed over with URLs, dates and quotes above.

## Assimilation

`<L1>` — state whether any `/home/vgpnk/Projects/shokuknow/merge/mado/` material was adopted
this round; round 74's entry (`Assimilation: none`, with the frontier-mining note) is the shape
to mirror.
