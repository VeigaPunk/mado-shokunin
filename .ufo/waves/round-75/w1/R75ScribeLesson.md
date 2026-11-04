# R75ScribeLesson — seat report (round 75, mado lane)

seat: R75ScribeLesson (wave w1 leaf member; no subagent dispatch)
date: 2026-11-04 (America/Sao_Paulo)
deliverable: `.ufo/waves/round-75/w1/R75ScribeLesson/lesson-r75.md` — the round-75 lesson
skeleton the L1 finishes. Nothing outside my write dir and this report was written.

## What was read (inputs, never rewritten)

- `.ufo/waves/round-75/claims-declaration-r75.md` — frozen claims, predicates, counting
  commands, kill rules, limits, pre-freeze disclosure, routed-defect dispositions D1–D5.
- `corpus/lessons/round-74.md` — shape and tone (header field order, two-claim Outcome,
  five-column Mistakes table, Gate stanza format, spot-check duty sentence, Assimilation).
- `corpus/lessons/round-74-verifier-spotcheck.md` §6 — routed defects D1–D5 (D1 stale 21/21
  tally; D2 unlanded selftest receipts; D3 S446 quote count 23 vs 21; D4 declaration seat count;
  D5 advisory probe class + `tools/mado-verify.sh:418` `/tmp` scratch).
- Committed receipts re-read: `.ufo/waves/round-75/control-baseline-r75.txt` (held C1 6/11 —
  credited modes `right`, `liar-success`, `uppercase-echo`, `stale-witness`, `absent-witness`,
  `wrong-witness`, `last-wins-wrong`; held C2 41/47 — misses exactly the four copy positives and
  two `del` negatives), `measurement-c1-r75.txt` (`MADO_R75_HARNESS_WITNESS: cases=11
  correct=11 base_correct=6 verdict=TARGET_MET rev=def7365…`, candidate harness sha256
  `058ba699…`, base harness sha256 `b6108c86…`), `measurement-c2-r75.txt`
  (`MADO_R75_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=47/47
  base_controls=41/47 verdict=TARGET_MET rev=def7365…`, 36 held cases `carried=yes`).
- `.ufo/waves/round-75/w1-dispatch.json` — `counts: {spawn: 13, resume: 0, total: 13}`;
  registry members 13 (R75ScoutChain, R75ScoutSources, R75ExecC1, R75ExecC2, R75ExecGate,
  R75ScribeEntries, R75ScribeLesson, R75RevC1, R75RevC2, R75Critic, R75Mutant, R75Conn,
  R75Sentinel).
- Read-only record checks: `SKILL.md:734` already carries "23/23, corrected from the stale
  21/21 at round 75" with class `probe` (D1 SKILL fix + D5 reclassification observed landed in
  the tree); `LOG.md:3657-3660` still shows "21/21" for the round-74 instruments bullet (the
  append-only LOG correction is still the L1's to land); `.ufo/waves/round-75/receipts/` holds
  the `mado-verify.sh` scratch red-before/green-after/green-valid receipts (the D5 carried
  scratch fix) and no `selftest-r75.txt` yet (D2 open → `<L1>`).

## What was derived (commands and outcomes)

All fetches: `curl -fsSL https://raw.githubusercontent.com/python/cpython/v3.14.8/<path>`,
three times per file, into my scratch `/fast/scratch/hyaku/mado-r75/R75ScribeLesson/fetch/`
(deleted after this report was written; every number cited below is inlined in
`lesson-r75.md`, so no receipt copy is needed outside my dir).

- `Doc/reference/simple_stmts.rst` ×3 → byte-identical, sha256
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41,375 B (= S447/S451's
  recorded digest; W04 pairs S453/S447, S453/S451 expected). Quote located at :468-469: "Deletion
  of attribute references and subscriptions is passed to the primary object involved" — 13 words
  (`len(q.split())`, markup-stripped, no double space inside the span).
- `Doc/library/stdtypes.rst` ×3 → **HTTP 404 all three attempts (curl rc 22)**.
- `Doc/builtins/stdtypes.rst` ×3 → byte-identical, sha256
  `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`, 248,201 B — exactly
  S446's recorded digest and size (SOURCES.md:865 already documents this path as the round-71
  404 repair). Quote located at :5350-5351: "If keyword arguments are given, the keyword
  arguments and their values are added to the dictionary created from the positional
  argument." — 21 words (the sentence ends before the double space after "argument.", which
  is outside the quote).
- `Doc/library/random.rst` ×3 → byte-identical, sha256
  `18235d86c91f69256453f300dfbc3c0dbfe8068099c9ba5ed877d3dd75547ab4`, 30,766 B. Quote located
  at :46-48 (`:mod:` markup stripped): "The pseudo-random generators of this module should not
  be used for security purposes. For security or cryptographic uses, see the `secrets`
  module." — 22 words. Proposed as the round's candidate reject stanza (the C1 challenge
  alternative; the L1 adopts or drops it).

## Findings

1. **M75-6 (own read, landing): the frozen declaration's second source URL 404s.** The
   declaration's sources plan anchors S454 at `Doc/library/stdtypes.rst`; the tag serves no
   bytes there (three 404s), the real path is `Doc/builtins/stdtypes.rst` (= S446's digest), and
   round 73 already repaired this exact mistake for S446. The skeleton's S454 stanza anchors at
   the real path and names the declaration URL as the record defect (never rewritten). One
   documented W04 pair S454/S446 is expected at the census.
2. **M75-7 (own read, planning): the stale seat count repeated.** Round-75's declaration says
   "ONE v1 wave of 12 seats" while the dispatch counts `spawn=13 resume=0 total=13` and the
   registry lists 13 members. D4's disposition ("disclose the actual size … next round") did not
   reach the declaration it governs. The report/lesson disclose 13; the next declaration's shape
   line should be generated from `counts.total`.
3. Rows (a)–(e) from the ticket are drafted as M75-1..M75-5 with class / captured-by / fix per
   the round-74 shape; every evidence cell is marked `<L1>` with a hint naming the exact
   receipt/quote the L1 fills (several green states are already observable in the tree: the
   SKILL.md:734 correction, the scratch red-before receipts).
4. Gate duties handed to the L1: the wave's sources scout's `sources.md` did not exist at read
   time (`w1/R75ScoutSources/` empty, `fetch/` empty — scout still running), so the S453/S454
   numbers above are this seat's independent derivation; where they differ from `sources.md`,
   the landed fetch receipts decide and the skeleton is corrected before landing. The
   random.rst reject is a proposal, kept only if the L1 adopts it (the round is free to reject a
   different candidate; the stanza discipline — URL, trio, quote, reason, flip — is the
   deliverable).

## Bounds and tooling

- Writes confined to `.ufo/waves/round-75/w1/R75ScribeLesson/` (lesson-r75.md) and this report
  file. No lane/corpus/SKILL/LOG/SCORECARD/SOURCES writes; no `.ufo/state/`, `scripts/`,
  `templates/`, MANIFEST.json; no git/jj write commands (only read-only file reads; no git
  invocation at all); no `agent://all` messages; no pacman transactions; no tool installed or
  upgraded (none needed); no compositor/service/config probing; no credential material.
- Scratch `/fast/scratch/hyaku/mado-r75/R75ScribeLesson/` created, used for the nine fetch
  triples, then deleted after this report was written.

## Limits

- This seat does not re-measure claims, run the counting commands, or verify the wave's other
  seats; the measurements cited are the committed receipts re-read verbatim.
- The lesson is a draft: evidence cells and landed states (`<L1>`) are the L1's; the
  `## Assimilation` section is a placeholder; registry `used-by` paths await the entries seat.
- The spot-check of gate decisions is the closure's, per the handover sentence in the skeleton.
