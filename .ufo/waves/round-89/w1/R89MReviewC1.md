# R89MReviewC1 — C1 review (candidate, counter, cases, mutants) vs upstream mako v1.11.0

Reviewer: R89MReviewC1 (leaf, no dispatch). Base `af998dcc41d48618ffe7afe0efc9354755a9244e`.
Every run in this report is **DRAFT** (pre-freeze, in-scratch); none is a measurement, no receipt written.

## Verdict: READY to freeze

All predicate conjuncts hold on DRAFT runs; the counter, case set and mutant set are internally
consistent and upstream-faithful. One new-code fidelity corner (F1) is disclosed below and recommended
as a draft revision (tiny candidate fix + case), or as a recorded residual — L1's call. No
counter/case/mutant defect found.

## Evidence: upstream checks (mandate item 1)

- `git diff --no-index tools/mado-mako.py .ufo/waves/round-89/build/mado-mako.c1.py` (read-only, rc 1 = differs, 193 lines): MODELLED_FIELDS 10 → 12 (`summary~`, `body~`), ctypes libc matcher, tokenizer changes, evaluate/decide split, selftest extensions. No other behavior touched.
- regcomp flags: candidate `mado-mako.c1.py:144` `REG_EXTENDED | REG_NOSUB` with `REG_EXTENDED=1`, `REG_NOSUB=1<<3` — matches `/usr/include/regex.h:310,323` (compiled probe printed `REG_EXTENDED=1 REG_NOSUB=8`) and criteria.c:333-336/345-347.
- regexec: candidate `:149-151` `regexec(compiled, text, 0, None, 0) == 0` — exactly criteria.c:46-59 `match_regex_criteria` (0 = match; REG_NOMATCH and any error both non-match, error text upstream goes to stderr only; observable verdict identical).
- ctypes signatures match regex.h: `regcomp(c_void_p, c_char_p, c_int)`, `regexec(c_void_p, c_char_p, c_size_t, c_void_p, c_int)`, `regfree(c_void_p)`. Buffer: host probe `sizeof(regex_t)=64`; candidate `REGEX_T_BYTES=256` (line 117) is oversized-safe, comment accurate.
- Locale: `grep -rn setlocale mako-1.11.0/` over the v1.11.0 tarball → no match (rc 1). Candidate forces `locale.setlocale(locale.LC_ALL, "C")` at `:124` before the first regcomp and the counter's run env (`LANG`/`LC_ALL=C.UTF-8`) cannot leak in. Selftest `regex-locale` proves byte semantics (`^.$` vs "é" → nomatch, DRAFT).
- Tokenizer vs parse_criteria (criteria.c:162-250, enum.h bitmask states): backslash escapes the next char inside and outside quotes (candidate `:277-282`, `:290-296`); only `' '` splits (candidate `:299`, was `isspace()` at base — correct fix); in-quote dangling backslash → error `:277-279`, mirrors upstream's "Unmatched quote" (QUOTE_ESCAPE=3 has the QUOTE bit, enum.h:6-12); unterminated quote → error `:311-312`.
- Both-fields: candidate `:422-425` per-section refusal — matches criteria.c:542-550 (`validate_criteria` runs per criteria object, i.e. per section; cross-section use stays legal both sides).
- DRAFT run: candidate `--selftest` → 58/58, rc 0.

## Findings

### F1 — Low (candidate, new code): a duplicated regex field with an earlier invalid occurrence is accepted; upstream rejects the whole config
`mado-mako.c1.py:400-401` dedups fields keeping the last occurrence; `:425-435` compiles only surviving values. Upstream `parse_criteria` applies tokens **in order** (criteria.c:209 space-split apply, :243 final apply); the FIRST `summary~=` occurrence is regcomp'd immediately (criteria.c:332-338) and a failure returns false → `load_config_file` does `ret = -1; break` (config.c:844-849): mako rejects the entire config.
Reproducer (DRAFT): config `[summary~=a(b summary~=x]\nwidth=1\n`, `--summary x` → candidate: `refusals=[] width=1` (section applied). Upstream: config refused.
Direction: permissive corner, outside the case-encoded surface; the reverse order (valid then invalid) agrees with upstream. Suggested draft revision: regcomp-validate every raw occurrence (e.g. in `open_section` before dedup) — with optional case `r31` (`[summary~=a(b summary~=x]`, summary `x`, expect top-right + refusals present). Adding the case without the fix would fail the candidate (correct < N), so fix and case must land together.

### F2 — Residual (pre-existing, out of the claimed tokenizer rules): escaped `=` is not a no-op escape
Upstream escapes only affect tokenizer states; the key/value split happens afterwards on the assembled token (criteria.c:269 `strstr`), so upstream `summary\=x` **sets** summary=x. Candidate `:290-296` makes `\=` a literal `=` with no split → bare-token refusal.
Reproducer (DRAFT): config `[summary\=x]\nwidth=1\n`, `--summary x` → candidate: `refusals=1` ("token 'summary=x' has no '=value'"), width=300. Unchanged from base; C1's claim names backslash-in-quotes and space-only rules only. Candidate refuses what upstream accepts — candidate is the stricter side here (inverse of F1).

### F3 — Residual (pre-existing): standalone `""` token refused, upstream ignores it
criteria.c:272 (`*key == '\0'` → return true) silently ignores empty tokens; candidate `end_word` emits `("", None)` → refusal. Cosmetic corner, unchanged from base.

### Counter observations (no defect)
- Predicate: docstring (:4-7) = code (:90-93) = declaration C1 sentence, verbatim; relabelled control line (`python-re`) applied at :117.
- `carried_count` (:96-107): skips superseded c53 by id, setup-errors if a superseded id is present in the new set; DRAFT check: 61/61 byte-equal, c53 absent, no duplicate ids, N=91 within 70..110, schema `mako-cases-r89-v1`. Note: `prior_n` (kept count = 61) is printed but not asserted; it is pinned transitively by `--expect-r88-cases-sha256` (fixed bytes → 62 r88 entries → 61 kept). Optional hardening: assert `prior_n == CARRIED_CASES`.
- Setup-error discipline: missing args, unreadable cases, all four sha mismatches, N out of range, superseded id present, and any mutant/forgery anchor not occurring exactly once (R88.evaluate) all exit 2 — never a verdict, never retried green.
- Do-nothing tool: correct < N (selftest-fixture base-tool control reaches TARGET_MISSED in the counter selftest) and killed = 0 (a crash or equal verdict is not a kill, c1-r88-mako-fields.py `semantic_kill`), so no conjunct is met by doing nothing.
- Forgery: 3 python-re anchors occur exactly once each in the candidate (DRAFT count check); the forged tool compiles (counter selftest) and scores 81 < 91.

## Case set r01–r30 (mandate item 3): 30/30 expectations re-derived, all correct

Independent re-derivation (DRAFT): my own tokenizer re-implemented from criteria.c:162-250 + enum.h bitmask states, regex verdicts from the compiled `posix-ere-oracle.c` binary (regcomp(REG_EXTENDED|REG_NOSUB)/regexec, no setlocale). All 30 derived (anchor, refusals) pairs match the case expectations; the per-case `oracle` notes match the oracle output. Spot-verified glibc quirks with the oracle: `a{1` invalid (r12), `a**` valid (r13), `(?i)x` invalid (r11), `\<foo\>` GNU boundaries valid (r10 — the case correctly encodes `\\<foo\\>` in the file so the pattern reaches regcomp with backslashes), C-locale byte semantics r08/r25, `\d` = literal d after the tokenizer (r06/r07 encode `\\d`). **No wrong expectation found; no corrected JSON needed.**

## Mutants M23–M32 (mandate item 4): all real, none equivalent, all anchored once

DRAFT anchor check: each of the 32 `old` anchors occurs exactly once in the candidate. DRAFT full in-process `score()` (candidate + 32 mutants + forgery + controls, r88 machinery at its pinned sha): **n=91, correct=91, killed=32/32, carried=61/61, verdict TARGET_MET, 0 case fails**, controls naive=22 / globals=23 / base=67 / python-re=81, all < 91. Kill mapping: M23←r03,r29,r30; M24←r08,r25; M25←r02,r28; M26←r01ff; M27←r20; M28←r11,r12,r22; M29←r17,r18; M30←r14,r15; M31←r16; M32←r19.

Omissions I checked and agree with: REG_NOSUB-drop would be equivalent on glibc (nmatch=0/pmatch=NULL behaves identically without NOSUB) — correctly not mutated; strict-encode mutant unreachable (config is decoded strict-UTF-8 before the pattern exists).

Proposed addition (optional, adjacent to the claimed tokenizer rules; candidate must gain it a killing case too — as-is it is out-of-claim coverage):

```json
{
  "id": "M33-unquoted-escape-dropped",
  "description": "outside quotes a backslash no longer escapes the next character, so \\. reaches regcomp with its backslash (criteria.c parse_criteria ESCAPE state)",
  "old": "                return [], \"dangling backslash\"\n            word.append(body[i + 1])",
  "new": "                return [], \"dangling backslash\"\n            word.append(\"\\\\\" + body[i + 1])"
}
```
Anchor unique (in-quote branch carries the longer message). Killing case (would also pin F1-class behavior): `r31-unquoted-escape`: config `[summary~=1\.0]` (file bytes `1\.0`), args `summary=1x0`, expect bottom-center/none. Under M33 the pattern is `1\.0` → nomatch → killed.

## Residual risk and verification gaps

- Nothing measured: all runs above are DRAFT; the measured runs are the frozen counters at the frozen revisions after the `## Freeze` section.
- F1/F2/F3 upstream behavior established by source reading (criteria.c, config.c, enum.h from the v1.11.0 tarball), not by executing a mako binary (not built here).
- C2 artifacts, the r88 frozen counters' content, and the base-tool sha pin `c374d715…` are out of my scope (other seats).
- Counter hardening opportunity (optional): assert `prior_n == 61` alongside `carried == 61`.

## DRAFT run ledger (all under /fast/scratch/hyaku/mado-r89/R89MReviewC1/, removed after this review)

1. `mado-mako.c1.py --selftest` → 58/58, rc 0.
2. `c1-r89-mako-regex.py --selftest --candidate-file <candidate>` → 27/27, rc 0.
3. `c1-r89-mako-regex.py --controls-only --repo <lane> --base-rev af998dc…` → `BELOW_N`, rc 0: naive=22, globals=23, base=67, python-re=81 (matches the declaration's draft disclosure exactly).
4. In-process `score()` over candidate + M01–M32 + r88 carried check → n=91 correct=91 killed=32/32 carried=61/61 TARGET_MET, 0 case fails.
5. Oracle + independent tokenizer over r01–r30 → 30/30 OK.
6. Deviation reproducers F1/F2 (candidate runs) → outputs as quoted above.

No installs (host cc/python3/git only); no pacman use; no mutating git/jj anywhere; scratch deleted on exit.
