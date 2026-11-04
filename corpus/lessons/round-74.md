# mado round 74 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-04 (America/Sao_Paulo)
base: `bd5a971532f37df85a78f6f566dd1e649b79de11`
frozen declaration: `.ufo/waves/round-74/claims-declaration-r74.md`, landed with the instruments at
`b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`
control sets: `.ufo/waves/round-74/controls/c1-replay-cases-r74.json` sha256
`17c95774044fb2d8125b9f4bf85bdcb947babb60e438424f246b77785574727c` and
`.ufo/waves/round-74/controls/c2-cases-r74.json` sha256
`4db4cc70d1a8e86876f20a9527cfc7f0c7a344eb6d2655b398443b907b3a73d0`
pre-freeze baseline: `.ufo/waves/round-74/control-baseline-r74.txt` (held credit 8/12; held
classifier 32/36)
measured content: `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` (both instruments; measurements
`.ufo/waves/round-74/measurement-c1-r74.txt` and `measurement-c2-r74.txt`)

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data; both `TARGET_MET` at the measured
content with the do-nothing controls at their declared scores.

- **C1 calibration — the credit rule requires the run's own echo of a per-run challenge.** The
  round-72 rule's own declared limit (a captured summary replayed with matching detail lines is
  byte-indistinguishable) is measured at `8/12` on the twelve-case set; the successor
  `credit(out, nonce)` scores `12/12` — `MADO_R74_REPLAY_WITNESS: cases=12 correct=12
  base_correct=8 verdict=TARGET_MET` rc 0. The four replay modes are each refused by one named
  part of the rule (stale witness, absent witness, wrong witness, last-wrong witness).
- **C2 operability — the guard census counts the two-hop object alias and the one-hop
  `os.environ` alias.** `population=20 readers=13 guarded=13 unguarded=0 controls=36/36
  base_controls=32/36 verdict=TARGET_MET` rc 0; the held round-73 classifier misses exactly the
  four new positives.

**Not claimed.** That the challenge authenticates the assertions (it authenticates the echo); that
the twelve or thirty-six cases are fault coverage; that the successor rule is wired into the
frozen round-72 harness (it is a standalone instrument this round); that the census models
execution order, chains aliases, or interprets values; any desktop, compositor, service or
session behaviour (none was probed); any `[x]`, promotion or axis retirement.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M74-1: the first prototype ran the fixture lane **without** the harness's M-Z mutation (the zero-citation clause still in place), so three carried modes took the `if` branch and the held rule scored `9/12` with three false rejections — a baseline that measured the wrong lane. | landing | `.ufo/waves/round-74/receipts/m74-1-red.txt` (the reproduced first run: `c1_correct=9/12`, `liar-success`, `stderr-genuine`, `last-wins-fail` all `correct=no`) versus the committed `control-baseline-r74.txt` (`c1_correct=8/12`, every carried mode correct). | the pre-freeze prototype itself (the held leg scored below the declared base, which the freeze would have rejected). | The counter's `build_lane` asserts the mutation marker occurs exactly once and deletes it; the fixture is the mutant lane by construction. The failure it can now show: a lane built without the mutation scores 9/12 and cannot reach the frozen `base_correct=8`. |
| M74-2: the first C2 case draft labelled `environ-alias-not-environ` and `environ-alias-deleted` as negatives; the held classifier answers `(True, True)` for both — the first because the key really is in the mapping handed as `env=` (the generic env-named flow counts it, correctly), the second because the generic flow does not model `del`. A frozen set with those labels would have made the successor miss its own target for a reason that is not its carrier. | scope | `.ufo/waves/round-74/receipts/m74-2-red.txt` (`draft_expect=(True, False) held=(True, True) disagrees=True` for both). | the pre-freeze prototype (the do-nothing control disagreed with the draft labels before the freeze). | The case set was re-cut before freeze: `environ-alias-no-store` and `environ-alias-rebound` replace them, and the declared limit names the unmodelled `del` gap. The failure it can now show: any future case whose label assumes a stronger rule than the declared bound disagrees in the prototype run. |
| M74-3: round 73 recorded S448's sha256 as `2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e`; the fetched bytes hash to `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5`. The lane's own `R73ScoutSources` found it in round 73 and no correction landed (round-73 closure D1). | number-drift | `corpus/SOURCES.md` S448 (the false digest), `.ufo/waves/round-73/w1/R73ScoutSources.md:119`, `.ufo/waves/round-73-verifier-spotcheck.md` D1, and this round's three fetches `.ufo/waves/round-74/fetch/os.rst.{1,2,3}` (all `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5`, 208,655 B). | QUALITY 6 (a pinned value carries its re-derivation command) — the digest was transcribed from a run instead of re-derived from the fetched bytes in the same breath. | S452 supersedes S448 with the re-derived digest (append-only, CORPUS rule 2), the sweep of every mention is in the report, and the round's own fetches re-derive it three times. The failure it can now show: a digest that shares only a prefix with the bytes is caught by `sha256sum` against the committed fetch. |
| M74-4: round 73's criteria 118–119 landed in the root `QUALITY.md`, not the canonical `corpus/QUALITY.md` (round-73 closure D4), so the contract-path bar stopped at 117. | landing | root `QUALITY.md` tail (criteria 118–119) versus `corpus/QUALITY.md` (last criterion 117); the round-73 spot-check's D4. | the round-73 closure spot-check (an outside reader at the contract path could not see the criteria). | Criteria 118–119 are appended to `corpus/QUALITY.md` this round and the root fragment carries a redirect line; `grep -c '^118\.' corpus/QUALITY.md` was 0 before the append and 1 after. The failure it can now show: a criterion written at a non-contract path is invisible to a reader who follows `corpus/README.md`'s pointer. |
| M74-5: the three new rows' `teaches` cells recorded the located quotes as 21/24/16 words; the bytes tokenise to 20/23/15 (a double space in each source line was counted as a token). | number-drift | the wave's `R74ScoutSources` F1 (`fetch-digests.txt`, `quote-locations.txt`): every quoted string was re-tokenised whitespace-split. | the sources scout's quote re-measurement (no lane rule required a word count to be re-derived before the row landed; QUALITY 6's re-derivation duty was applied to digests, not to the count in the same cell). | The three counts are corrected in the rows and the Gate before landing; the ≤25-word rule was never violated. The failure it can now show: a count that the bytes do not produce is caught by re-tokenising the quoted string. |

A fix counts only on its named red/green evidence: M74-1's red is `receipts/m74-1-red.txt`
(9/12) and its green the committed baseline (8/12); M74-2's red is `receipts/m74-2-red.txt` (both
draft labels disagree) and its green the frozen set's 36/36 with base 32/36; M74-3's red is the
S448 cell and its green S452's re-derived digest in three fetches; M74-4's red is
`grep -c '^118\.' corpus/QUALITY.md` → 0 and its green → 1 after the append.

## Gate

Admitted, **S450** — CPython v3.14.8 library reference, `Doc/library/secrets.rst`, § `secrets`,
`token_hex`.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/secrets.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (sha256
  `289ff11e32dc6023446b1e8e0853635a9c19be200cb7df76f50a029993890659`, 6,305 bytes; receipts
  `.ufo/waves/round-74/fetch/secrets.rst.{1,2,3}`).
- Located quote, 20 words, secrets.rst:80-81 (markup stripped): "Return a random text string, in
  hexadecimal. The string has nbytes random bytes, each byte converted to two hex digits."
- Why it grounds C1: 8 bytes give the 16 hex characters the witness grammar matches, and a block
  captured from an earlier run cannot contain the challenge generated now.

Admitted, **S451** — CPython v3.14.8 language reference, `Doc/reference/simple_stmts.rst`,
§ Assignment statements, the attribute-reference bullet.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41,375 bytes — S447's
  recorded digest).
- Located quote, 23 words, simple_stmts.rst:160-162: "If the target is an attribute reference:
  The primary expression in the reference is evaluated. It should yield an object with assignable
  attributes".
- Why it grounds C2: `r.env[KEY] = "1"` evaluates `r` first, so an alias of the object carries
  the store at the alias's dotted path.

Admitted, **S452** — CPython v3.14.8 library reference, `Doc/library/os.rst`,
§ Process Parameters, `.. data:: environ` (supersedes S448's recorded digest).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5`, 208,655 bytes).
- Located quote, 15 words, os.rst:196-197: "This mapping may be used to modify the environment as
  well as query the environment."
- Why it grounds C2: the environ mapping itself is the mutation surface, so a one-hop alias of it
  carries a key store into a later copy of the alias. It also supersedes S448: the same document's
  `.. data:: environ` block, at the alias-modification paragraph, with the digest re-derived
  (`2d0f2892…b2ae5`), closing round-73 D1 append-only.

**Re-opened reject, S446** — CPython 3.14.8 `Doc/builtins/stdtypes.rst` (round-72 reject; round-73
routed D5 asked for its located quote).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`
- Access date: 2026-11-04, three times byte-identical (sha256
  `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`, 248,201 bytes).
- Located quote, 23 words, stdtypes.rst:5525-5527 (span 5525-5527) (`setdefault`): "If key is in the dictionary,
  return its value. If not, insert key with a value of default and return default."
- Why it stays rejected: the document is mapping-method behaviour, not call-site or result-object
  semantics; no admitted entry needs it. Flip: a rule that turns on a dict method's own behaviour.

Registry cell changes (old → new, per CORPUS rule 2; no held cell changed in place):

- S450, S451, S452 enter `mined` with `used-by` `corpus/knowledge/replay-witness-credit-r74.md`
  (S450) and `corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md` (S451, S452).
- S448 keeps its `status`, `recheck` and `used-by`; its digest is corrected by S452's superseding
  row, never by an edit.

Registry 386 → 389 rows; the census
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` printed W04 for
S451/S447 and S452/S448 (the documented duplicate-URL warning across scopes) and exit 0 at round
end. The round-start run (386 rows, exit 0) and the round-end run are in the report.

**Carried errata recorded this round.** (a) S448's located quote starts at os.rst:192, not 193
(`corpus/knowledge/guard-carrier-global-environ-r73.md:21` and the round-73 spot-check's table cite
`193-194`); the sentence begins on line 192 ("...site.py`.  Changes"), so the true span is 192-194
and the registry's block anchor `184-196` contains it — a record defect in the round-73 notes, not
a registry claim, recorded here rather than rewritten. (b) The wave's critic found that the C1
modes `liar-success` and `stderr-genuine` emit byte-identical combined output (they differ only in
stream split and exit status, neither of which `credit` reads), so the twelve cases carry eleven
distinct rule-visible inputs; the arithmetic is unaffected and the pair is recorded as a declared
limit, not re-cut after the freeze. (c) The pre-freeze baseline receipt carries no `rev=` stamp;
its held legs and the measurement's exact-base arithmetic are the order evidence (round-75 note:
stamp pre-freeze receipts).

**Spot-check duty.** The in-round wave seats are the lane's own; the non-author spot-check of this
round's gate decisions (at least one admit and one reject) is the closure's, per LEARNING.md. The
three admits and the re-opened reject are handed over with URLs, dates and quotes above.

## Assimilation

`Assimilation: none` — `considerthese/` was mined by the wave's `R74ScoutFrontier` seat for the
next round's candidate, but nothing from `/home/vgpnk/Projects/shokuknow/merge/mado/` was adopted
this round: the round's claims are instrument work on the lane's own harness chain, and the
package's staged entries are domain material for a later assimilation round.
