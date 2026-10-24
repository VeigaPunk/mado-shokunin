# RevC2Counter — attack on the C2 counter (PRED-C2-r30)

Seat: reviewer, leaf (no subagents). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target: `.ufo/waves/round-30/c2/count.py` against the frozen registration's rubric text
(`.ufo/waves/round-30/registration.md` § C2). Report only — nothing was edited, no git state
mutated. All experiments ran in throwaway `/tmp` git repos built from `git show` bytes.

Method: line-by-line read; executed the frozen counter at `8f51071b` (base) and `446dc396`
(data) in the lane; replicated its resolution branch exactly (`count.py:127-162`) against
committed lesson bytes; re-ran it inside a synthetic `/tmp` repo to test reachability of the
predicate. No `lsp` device is exposed on this seat's tool surface (only `ast_edit`/`debug`), so
caller/definition checks were done by execution + targeted grep, not IDE-semantic lookup.

Headline: **the claim's arithmetic is honest, the predicate is not sound.** Every number in the
registration and in both receipts reproduces exactly, but `TARGET_MET` is reachable at the base
revision with one added sentence and one zero-byte file, and four active criteria validate only
the first id of a multi-id citation.

---

## S1 — HIGH (predicate): base + one supersession sentence + one empty lesson file = TARGET_MET

Reproduction (base `8f51071b`, no grounding added anywhere):

```
git show 8f51071b:corpus/QUALITY.md > /tmp/c2attack/corpus/QUALITY.md
git archive 8f51071b corpus/lessons | tar -x -C /tmp/c2attack
printf '\n41. Every claim falsifiable or marked opinion. Supersedes criteria 1-5, 38, 39 and 40. (lesson: lessons/round-99.md)\n' \
  >> corpus/QUALITY.md
: > corpus/lessons/round-99.md          # zero bytes
run frozen count.py HEAD
-> literal 29/41 = 0.7073 ; active=32 resolved_active=32 = 1.0000 ; TARGET_MET exit 0
```

The new row resolves because `count.py:133-136` treats a bare `lessons/<file>` citation as
"exists at REV" and nothing else — `PATH_RE` (`:41`) has no anchor/id group, so the empty blob
satisfies it. The eight base UNRESOLVED criteria leave the denominator by label alone: `:103-107`
adds every number named by any `Supersedes` phrase, `:170` drops them, `:189` then requires only
"no unresolved *active*" plus `literal >= 0.70`. `res_f` (`:177`) is printed but never gates.
`exists()` uses `git cat-file -e`, which also accepts a tree, so a directory named
`corpus/lessons/round-99.md` would satisfy a bare citation with an empty body.

Consequence for the claim: `resolved-active 31/39 -> 40/40` does not distinguish a grounded
criterion from one that was superseded out of the denominator or pointed at an empty blob. The
registered control K2 (do-nothing) cannot catch this shape, and the lane's own **active
criterion 36** (`corpus/QUALITY.md`, not superseded) requires exactly the shapes that do —
"do-nothing, all-false/empty, junk, server echo, label- or fixture-keyed, no-reader". C2 shipped
only the do-nothing shape. Under criterion 36, C2's control set is incomplete for its own counter.

## S2 — HIGH (implementation): only the FIRST id of any multi-id citation is validated

`ANCH_RE` (`:42`) is `… #([\w-]+)\s*(M[0-9/\-]*)`. The `M` of the second id is outside the char
class, so the capture stops there:

| criterion | committed citation | ids the counter checks | ids unvalidated |
|---|---|---|---|
| 15 | `#inference-traps M01-M07` | `\bM0*1\b` | 6 |
| 16 | `#inference-traps M03/M05/M06/M07` | `\bM0*3\b` | 3 |
| 21 | `#mistakes M1/M2` | `\bM0*1\b` | 1 |
| 27 | `#mistakes M1/M2` | `\bM0*1\b` | 1 |

Proof that this is a false-green mechanism, not a cosmetic detail — a nonexistent id in the tail
resolves:

```
resolve("lessons/round-30.md#mistakes M30-1/M30-99") -> resolved=True, ids_actually_checked=['\bM30-1\b']
   (M30-99 does not exist anywhere in corpus/lessons/round-30.md at 446dc396)
resolve("lessons/round-30.md#mistakes M30-1, M30-99") -> resolved=True, same single id
```

This contradicts the docstring's frozen rubric ("every M-id appears in that file", and the
explicit "`M<a>/M<b>` lists" support, `count.py:26-28`). No current false credit: M02–M06 do exist
in round-12's inference-traps table (checked section-wise), so today the missing checks happen to
be satisfied. The guarantee is nonetheless absent for every future citation written this way.

## S3 — MEDIUM (implementation): `M01-M07` is not expanded even when the full string arrives; compound-vs-range is decided by numeric order

`expand_ids` (`:53-66`) + `MID_RE` (`:47`), probes on the frozen module:

```
expand_ids("M01-M07") -> ['\bM0*1\b', '\bM0*7\b']      # endpoints only, M2..M6 dropped
expand_ids("M1-5")    -> ['\bM0*1\b' … '\bM0*5\b']     # a round-1/mistake-5 compound widened to a 5-id range
expand_ids("M23-4")   -> ['\bM23-4\b']                 # literal, as documented
expand_ids("M23-4-7") -> ['\bM23-4\b']                 # tail silently dropped
```

Two independent defects on the same construct: (a) ranges written in the observed in-repo spelling
`M01-M07` are narrowed to their endpoints (and, through S2, to `M01` alone); (b) the literal/range
decision is `b < a`, not syntax, so any legitimate `M<round>-<n>` with round ≤ n (`M1-5`, `M2-2`)
is silently widened to range semantics. The frozen registration says compound ids "match
literally" — the discriminator chosen cannot honour that for the ambiguous quadrant.

## S4 — MEDIUM (latent, implementation): compound supersession lists are silently truncated

`SUPER_RE` (`:44-46`) allows an optional range on the *first* number only, so later multi-range
members fall out of the match:

```
"Supersedes criteria 1-5 and 38-40"        -> {1,2,3,4,5,38}        (39, 40 lost)
"Supersedes criteria 1–5, 18–20, 32, 38–40"-> {1,2,3,4,5,18}        (19, 20, 32, 38, 39, 40 lost)
```

The docstring (`:8-10`) and the registration both claim `<N1>-<N2>` and `N and M` support. The
committed rows 41–51 each supersede one criterion, so no score moved this round; the failure
direction is fail-closed (lines stay active), but the counter mis-scores any compound row written
in the grammar it advertises.

## S5 — MEDIUM (implementation vs frozen rubric): no "later line" ordering

Registration: "a line is superseded when a **later** line says `Supersedes criterion N`".
`count.py:103-107` scans every criterion and adds every named number; only self-reference is
guarded (`if n != c["num"]`). Any row can retro-kill a later row — e.g. `Supersedes criterion 52`
inside criterion 41 removes the newly added routing criterion from the denominator. Not exercised
by the data commit (all supersessions point backwards), but the gate does not implement the
frozen rule.

## S6 — MEDIUM (degenerate population): `active = 0` passes

A mutual supersession pair makes every criterion inactive, and the predicate still goes green:

```
41. Supersedes criteria 1-20 and 42. (lesson: lessons/none.md)
42. Supersedes criteria 21-41. (lesson: lessons/none.md)
-> METRIC active=0 resolved_active=0 fraction=0.0000 ; literal 30/42 = 0.7143 ; TARGET_MET exit 0
```

`:189` gates on `unresolved_active` (empty when nothing is active) and `lit_f` only; `res_f` and
`act_n` are not consulted. Neither the code nor the registration sets a minimum active
population, so "resolved-active 40/40" is one label-keyed move away from "0/0".

## S7 — MEDIUM (committed semantic vacuity): criteria 41–45 share one self-referential id

`corpus/lessons/round-30.md:13`: M30-1 = "`corpus/QUALITY.md` criteria 1–5 carry no lesson
citation; …". Rows 41–45 all cite that single row for four *different* rules (source carriage,
observation/inference separation, append-only errata, rejections kept). The ground offered for
"this criterion had no citation" is the audit finding that this criterion had no citation. Five of
the 40 active criteria therefore resolve on one id, and the counter cannot see the difference:
`:145` accepts any anchor word anywhere in the file, `:148-151` accepts any id anywhere in the
file — anchor and id are two independent whole-file substring tests, never a conjunction scoped to
a section.

Row 52, the criterion that governs this very repair ("a declared claim with its own counter"), is
itself resolved partly by a bare `lessons/round-29.md` (`corpus/QUALITY.md:358` at `446dc396`,
existence only).

## S8 — MEDIUM (committed anchor weakness): the anchor check is a whole-file substring test

`count.py:144-145`: `want = anchor.replace("-", " ")`; fails only if neither the spaced nor the
hyphenated form occurs anywhere in the body. No heading parse, no case sensitivity, no section
scoping. Against committed bytes at `446dc396`, both of these resolve although neither heading
exists:

```
lessons/round-30.md#attribution M30-1  -> resolved (the word appears only in M30-1's kind column)
lessons/round-30.md#evidence    M30-2  -> resolved (prose only)
```

**Committed instance, not hypothetical:** active criterion 35 cites
`lessons/round-23.md#mistakes M23-7` (`corpus/QUALITY.md` at `446dc396`), but M23-7 appears only
in `round-23.md:229`, inside `### Final C1 disposition: withdrawn to base bytes (honest stop)`
(line 212) — it is absent from the `## Mistakes` table (lines 13–26, `grep -c M23-7` = 0). The
counter resolves the citation because "mistakes" occurs as a heading somewhere in the file and
`M23-7` occurs somewhere else. This is the "file that merely mentions the word" case, committed
and counted toward C2's 40/40.

`round-30.md` headings are `# Round 30 …`, `## Mistakes`, `## Gate`, `## Notes`. So a "proper
anchor" citation is only marginally stronger than a bare path: it requires the anchor *word* and
*some* matching id to exist somewhere in the file, in any two unrelated places. This is the direct
answer to attack (3): a file that merely mentions "mistakes" passes.

## S9 — LOW (claim text): "12 lines superseded by rows 41–51" is off by one

Rows 41–51 supersede 11 criteria (1–5, 18, 19, 32, 38, 39, 40). The 12th in the counter's set,
criterion 20, was already superseded at base by criterion 21 (the registration says so itself, and
the base receipt prints `superseded=[20]`). `52 − 12 = 40` active holds, so both fractions are
right; the composition sentence in § C2 Target attributes 12 supersessions to rows 41–51.

## S10 — LOW (latent): `CRIT_RE` accepts indentation, `LIT_RE` requires column 0

`:39` `^\s*(\d+)\.\s` vs `:40` `^[0-9]+\.\s`. An indented sub-numbered list inside a criterion's
continuation becomes a separate criterion (`:92`), truncating the parent's text and creating an
uncited active criterion that can never count as literal. `grep -nE '^[[:space:]]+[0-9]+\. '`
over `446dc396:corpus/QUALITY.md` is empty — latent, not triggered.

## S11 — LOW (diagnostics)

- `c["fail"]` is overwritten at `:136`, `:146`, `:150`, `:156`, `:161`; only the last failure of a
  criterion is reported, so a criterion with two bad citations shows one.
- Missing lesson files print raw `fatal: path '…' does not exist in 'HEAD'` to stderr (observed in
  the S1 run) instead of a structured diagnostic; only a missing `corpus/QUALITY.md` yields
  `SETUP_ERROR` (`:86-90`).

---

## What passed (checked, not assumed)

- **Freeze identity.** `sha256(.ufo/waves/round-30/c2/count.py)` = `cbc2941b8126…` = the same blob
  at `451e8b3`; `git diff 451e8b3 446dc396 -- …/count.py` is empty. Freeze commit precedes data.
- **Receipts reproduce exactly.** `c2-before-8f51071b.txt` is committed at the freeze commit
  `451e8b3` and matches a live run: `literal 28/40 = 0.7000`, `superseded=[20]`, `active=39
  resolved_active=31 = 0.7949`, UNRESOLVED {1,2,3,4,5,38,39,40}, `TARGET_MISSED` exit 1.
  `c2-after-446dc396.txt` (committed `92d3c86`) matches a live run at `446dc396`: `literal 40/52 =
  0.7692`, `superseded=[1,2,3,4,5,18,19,20,32,38,39,40]`, `active=40 resolved_active=40 =
  1.0000`, `TARGET_MET` exit 0.
- **Committed citation content.** Every anchor id that *is* checked exists in its cited file;
  round-28 M28-1..3 and round-30 M30-1/M30-2 exist under `## Mistakes`. One active criterion (35)
  names an id that exists, but in a different section than the cited anchor (S8) — the only
  section-scoped mismatch I found. No active criterion resolves to a *missing* file or a *missing
  checked* id. The defects above are mechanisms and reachability, not (yet) fabricated rows.
- **Axis selection.** Calibration is the lowest re-derived axis (0.7000 literal / 0.7949 resolved
  < 0.9535 coverage, 1.0 operability); criterion 22's "literal versus semantic counted separately"
  is honoured — both fractions are printed.
- **Kill rule / control honesty.** K2's do-nothing state is red and committed before data; the
  kill rule ("any unresolved active, or literal < 0.70") is enforced by `:189`.

## Residual risk and verification gaps

1. S1/S6 were proven in `/tmp` reconstructions of the base revision, not by mutating lane bytes
   (out of scope and forbidden). The logic is the frozen module itself, unmodified.
2. No `lsp` device on this seat; no IDE-semantic caller check. No script, harness or gate in the
   lane wraps or imports the counter (grep over `*.sh`/`*.py`/`*.json`/`*.md`: only prose
   references) — it is invoked as a standalone script.
2b. The non-author integrator spot-check (`d72243e:corpus/lessons/round-30-verifier-spotcheck.md`,
   C2 row) re-ran the same counter and reproduced the same printed numbers, then read them as
   "calibration improved". It did not exercise the shortcut shapes (S1/S6) or the multi-id capture
   (S2), so its C2 verdict is agreement with the counter's output, not an independent check of the
   resolution semantics.
3. I did not review C1/C3 artifacts (other owners). Lane-hygiene observation only: the worktree
   currently shows ` M quality/check-index.py` (L1/C3-owned, unverified by me); all C2 numbers here
   read committed bytes via `git show`, so a dirty worktree does not affect them.
4. Not tested: behaviour at revisions where `corpus/lessons/` is absent (the counter emits git
   `fatal:` noise per missing path and continues — S11), and `SPELL_RE`'s adjacency requirement
   (`lesson round21`, not `lesson round 21`), which is fail-closed but brittle.

## Answers to the three posed attacks

1. **Vacuous resolution — yes, two ways.** (a) A bare `lessons/<file>` resolves on existence
   alone, including a zero-byte blob or a directory with that name (S1). (b) A named-but-different
   mistake resolves too: criteria 41–45 all lean on M30-1, a row about those same criteria lacking
   citations (S7); anchor and id are independent whole-file substring tests, so any id in the file
   satisfies any anchor in the file (S8).
2. **M-id regex — `M23-4` is right, `M01-M07` is wrong twice.** `M23-4` stays literal because
   `4 < 23`. `M01-M07` loses `M2..M6` in `expand_ids` (endpoints only) and loses `M07` as well at
   the `ANCH_RE` capture, so criteria 15/16 validate one id each. Conversely `M1-5`/`M2-2` — legal
   compound spellings — are silently widened to ranges (S2, S3).
3. **Anchor check — yes, a file that merely contains the word passes.** `#attribution M30-1` and
   `#evidence M30-2` both resolve against `corpus/lessons/round-30.md`, which has neither heading,
   and active criterion 35 already ships the committed version of this defect: it cites
   `round-23.md#mistakes M23-7` while M23-7 lives under "Final C1 disposition", not under
   `## Mistakes` (S8). The cheapest citation that passes with no grounding at all: a bare path to
   a zero-byte `lessons/` file, paired with one `Supersedes criteria …` sentence — which turns the
   base revision green without touching any criterion's substance (S1).

**Recommendation (not an admission, not an edit):** C2's measured numbers stand as recorded, but
the axis movement should not be read as calibration repair. The predicate needs a minimum active
population, an existence-plus-content test for bare citations, section-scoped id checks, a full
multi-id parse, and the empty/label-keyed controls that active criterion 36 already demands.
