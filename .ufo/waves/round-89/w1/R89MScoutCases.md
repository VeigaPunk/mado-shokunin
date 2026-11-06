# R89MScoutCases — round-89 C1 blind cases for `summary~` / `body~`

Seat: `R89MScoutCases` (scout). Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base revision examined: `af998dcc41d48618ffe7afe0efc9354755a9244e` (master).

**Status: complete.** One file written (a new blind case file), one report (this file).
Nothing else in the lane, the fleet root, `tools/`, `quality/`, `corpus/`, or any other
lane file was created, edited, or deleted. No git/jj mutation was run anywhere (read-only
`git`/`jj` was not needed at all for this seat).

## Deliverable

| Path | What |
| --- | --- |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-89/controls/mako-cases-r89-blind.json` | **NEW** blind case file: 45 cases, schema `mako-cases-r89-v1`, ids `b01`–`b45` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-89/w1/R89MScoutCases.md` | this report |

No receipt was written under `.ufo/waves/round-89/receipts/` — the round-89 brief forbids it
for draft work. **Every run recorded below is DRAFT, not a measurement.**

## Independence (the point of this seat)

I did **not** open the candidate tool. Both of these were left unopened:

* `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-89/build/mado-mako.c1.py`
* `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-mako.py`

I read only `controls/mako-cases-r89.json`, and only to copy its JSON shape and to avoid
duplicate ids/patterns (its ids are `c01`–`c62` and `r01`–`r30`; my ids are `b01`–`b45`).
`quality/counters/c1-r89-mako-regex.py` was also not opened. Every expectation below comes
from **upstream source + the oracle**, never from the candidate.

## Sources actually read

| Source | How | What it gave |
| --- | --- | --- |
| `https://raw.githubusercontent.com/emersion/mako/v1.11.0/criteria.c` | `curl -sSfL` → `$S/criteria.c` (573 lines) | `parse_criteria` 162-262, `apply_criteria_field` 267-411, `match_regex_criteria` 47-58, `match_criteria` 61-159, `validate_criteria` 498-551, `regcomp` 332-351 |
| `https://raw.githubusercontent.com/emersion/mako/v1.11.0/config.c` | via the v1.11.0 tarball | `load_config_file` 780-885: section slice `strndup(stripped_line + 1, len - 2)` at 842-843, refusal path 834-838 / 844-848 |
| `https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0` | `curl` + `tar xzf` → `$S/mako-1.11.0/` | `include/enum.h` 7-11 (parse-state bitmask), `types.c` 264-328 (a *different* tokenizer — the format parser, not the criteria parser) |
| `grep -rn setlocale mako-1.11.0/` | bash | **no output** — the v1.11.0 tree never calls `setlocale`, so libc runs in the C locale |
| `/usr/include/regex.h` | read | `REG_EXTENDED` 310, `REG_NOSUB` 323, error enum 346-368 (`REG_ERPAREN` is "not returned from regcomp") |

The upstream tree also contains a *second* tokenizer in `types.c:264-328` used for **format**
strings, not criteria. It is a different function and I did not use it; `parse_criteria`
(criteria.c:162-262) is the one that applies to a section header.

## Method

1. **Oracle.** Built exactly as the item specifies:
   `cc -O0 -o "$S/ore" .../controls/posix-ere-oracle.c` → exit 0. The oracle is
   `regcomp(&re, argv[1], REG_EXTENDED | REG_NOSUB)` then `regexec(&re, argv[2], 0, NULL, 0)`,
   printing `match` / `nomatch` / `invalid`. It makes **no** `setlocale` call, so it runs in
   the C locale exactly like mako. Exit code 0 on every run, including `invalid`.
2. **Tokenizer.** I re-implemented `parse_criteria`'s character loop from criteria.c alone
   (`$S/tok.py`): `NORMAL`(0) / `ESCAPE`(1) / `QUOTE`(2) / `QUOTE_ESCAPE`(3), with
   `state &= ~MAKO_PARSE_STATE_ESCAPE` (criteria.c:181) collapsing `QUOTE_ESCAPE`→`QUOTE`
   and `ESCAPE`→`NORMAL`; a space splits tokens only in `NORMAL` (criteria.c:207-215); the
   backslash is **dropped** and the next character taken verbatim (criteria.c:177-182).
3. **Expectations.** Each case's post-tokenizer pattern was fed to `"$S/ore" PATTERN TEXT`
   and the oracle's own verdict recorded in the case's `oracle` field; the case's `expect`
   follows from that verdict plus the criteria.c matching rules.
4. **Independent re-verification.** `$S/verify.py` re-reads the **written artifact**,
   re-derives every pattern with a **second, separately-written tokenizer** (explicit state
   table, different code shape), re-runs the oracle on every pattern, and re-checks the
   expectations. Final run: `VERIFY OK` (exit 0), 45 cases, 33 892 bytes.

### glibc facts I confirmed empirically (not assumed)

* `regcomp` return codes, measured: `[`→2 (REG_BADPAT), `[abc`→7 (REG_EBRACK),
  `*a`→13 (REG_BADRPT), `\1`→6 (REG_ESUBREG); `a)`, `(a)\1`, `x|`, `a]`, `[^[:digit:]]` all
  compile (rc 0).
* `\1` **alone** is invalid, but `(a)\1` compiles and matches `aa` — glibc's ERE backreference
  extension, not POSIX. Both are covered (b07 invalid, b06 match).
* `a)` compiles: an unmatched `)` is an ordinary byte on glibc (regex.h:367 says
  `REG_ERPAREN` is "not returned from regcomp").
* A **second** `regcomp` into the same `regex_t` replaces the compiled program
  (`$S/d1.c`: regcomp "alpha" then "beta" → `regexec("beta")` matches, `regexec("alpha")`
  does not). This is what makes the repeated-`summary~` token last-wins (b32/b33).
  Note: upstream `criteria.c:333` never `regfree`s between the two `regcomp`s, so this
  leaks the first program — an upstream detail, not a defect I introduce.
* `.` matches a space and a newline-free byte but **not** a newline; in the C locale `é`
  is two bytes, so `^..$` matches `é` while `^.$` does not (b42 vs the draft's r08).

## The 45 blind cases

Config shape is the item's: `anchor=top-right\n[<header>]\nanchor=bottom-center\n`.
`effective.anchor` is `bottom-center` when the section applies and `top-right` otherwise;
`refusals` is `present` when the criteria definition itself is refused.

| id | header as written | oracle | args | effective.anchor | refusals |
| --- | --- | --- | --- | --- | --- |
| b01-bracket-range-match | `[summary~=[b-d]]` | summary~:match | summary=c | bottom-center | none |
| b02-bracket-range-nomatch | `[summary~=[b-d]]` | summary~:nomatch | summary=e | top-right | none |
| b03-bracket-negation-match | `[summary~=[^abc]]` | summary~:match | summary=z | bottom-center | none |
| b04-bracket-negation-nomatch | `[summary~=[^abc]]` | summary~:nomatch | summary=a | top-right | none |
| b05-capture-group-under-nosub | `[summary~=(ab)+]` | summary~:match | summary=abab | bottom-center | none |
| b06-backreference-within-group | `[summary~=(a)\\1]` | summary~:match | summary=aa | bottom-center | none |
| b07-backreference-alone-invalid | `[summary~=\\1]` | summary~:invalid | summary=a | top-right | present |
| b08-alt-anchored-branches-match | `[summary~=^a|b$]` | summary~:match | summary=a | bottom-center | none |
| b09-alt-anchored-branches-nomatch | `[summary~=^a|b$]` | summary~:nomatch | summary=xa | top-right | none |
| b10-alt-anchored-branches-second-match | `[summary~=^a|b$]` | summary~:match | summary=xb | bottom-center | none |
| b11-dot-single-ascii-byte | `[summary~=.$]` | summary~:match | summary=x | bottom-center | none |
| b12-dot-matches-space | `[summary~=a.b]` | summary~:match | summary="a b" | bottom-center | none |
| b13-escaped-paren-becomes-group | `[summary~=\(x\)]` | summary~:match | summary=x | bottom-center | none |
| b14-escaped-bracket-becomes-open-bracket | `[summary~=\[]` | summary~:invalid | summary=[ | top-right | present |
| b15-unquoted-space-splits-token | `[summary~=Setup Wi-Fi]` | undecided | summary="Setup Wi-Fi" | top-right | present |
| b16-unquoted-space-splits-two-fields | `[summary~=Setup app-name=alpha]` | summary~:match | app-name=alpha, summary=Setup | bottom-center | none |
| b17-quote-inside-value | `[summary~="say \"hi\""]` | summary~:match | summary=`say "hi"` | bottom-center | none |
| b18-unquoted-quote-ends-value | `[summary~=say"hi"]` | summary~:match | summary=sayhi | bottom-center | none |
| b19-first-equals-only-splits | `[summary~=a=b]` | summary~:match | summary=a=b | bottom-center | none |
| b20-escaped-dot-becomes-wildcard | `[summary~=a\.b]` | summary~:match | summary=axb | bottom-center | none |
| b21-escaped-dot-literal-wins | `[summary~=a\\.b]` | summary~:match | summary=a.b | bottom-center | none |
| b22-escaped-dot-literal-misses | `[summary~=a\\.b]` | summary~:nomatch | summary=axb | top-right | none |
| b23-body-pattern-anchored-match | `[body~=^beta$]` | body~:match | body=beta | bottom-center | none |
| b24-body-pattern-anchored-nomatch | `[body~=^beta$]` | body~:nomatch | body="beta " | top-right | none |
| b25-body-pattern-no-body-input | `[body~=beta]` | undecided | summary=beta | top-right | present |
| b26-two-regex-fields-both-match | `[summary~=alpha body~=beta]` | summary~:match,body~:match | summary=alpha, body=beta | bottom-center | none |
| b27-two-regex-fields-body-misses | `[summary~=alpha body~=beta]` | summary~:match,body~:nomatch | summary=alpha, body=gamma | top-right | none |
| b28-app-name-plus-regex-match | `[app-name=alpha summary~=x]` | summary~:match | app-name=alpha, summary=x | bottom-center | none |
| b29-app-name-plus-regex-nomatch | `[app-name=alpha summary~=x]` | summary~:nomatch | app-name=alpha, summary=y | top-right | none |
| b30-urgency-plus-regex-match | `[urgency=critical summary~=x]` | summary~:match | urgency=critical, summary=x | bottom-center | none |
| b31-urgency-plus-regex-mismatch | `[urgency=critical summary~=x]` | summary~:match | urgency=normal, summary=x | top-right | none |
| b32-repeated-summary-token-last-wins-match | `[summary~=alpha summary~=beta]` | summary~:match | summary=beta | bottom-center | none |
| b33-repeated-summary-token-last-wins-nomatch | `[summary~=alpha summary~=beta]` | summary~:nomatch | summary=alpha | top-right | none |
| b34-invalid-open-bracket | `[summary~=[abc]` | summary~:invalid | summary=a | top-right | present |
| b35-invalid-leading-star | `[summary~=*a]` | summary~:invalid | summary=a | top-right | present |
| b36-unmatched-close-paren-is-literal | `[summary~=a)]` | summary~:match | summary=a) | bottom-center | none |
| b37-empty-alternative-branch | `[summary~=x|]` | summary~:match | summary=zzz | bottom-center | none |
| b38-negated-posix-class | `[summary~=[^[:digit:]]]` | summary~:match | summary=a | bottom-center | none |
| b39-negated-posix-class-nomatch | `[summary~=[^[:digit:]]]` | summary~:nomatch | summary=5 | top-right | none |
| b40-trailing-backslash | `[summary~=abc\]` | undecided | summary=abc | top-right | present |
| b41-unmatched-quote | `[summary~="abc]` | undecided | summary=abc | top-right | present |
| b42-two-byte-locale-count | `[summary~=^..$]` | summary~:match | summary=é | bottom-center | none |
| b43-bang-inside-value-is-literal | `[summary~=!x]` | summary~:match | summary=!x | bottom-center | none |
| b44-body-pattern-reads-body-not-summary | `[body~=gamma]` | body~:nomatch | summary=gamma, body=delta | top-right | none |
| b45-bang-prefixed-regex-key-is-invalid | `[!summary~=x]` | undecided | summary=x | top-right | present |

### Per-case trace (pattern after the tokenizer → criteria.c line → oracle)

Every case's `pin` field in the JSON carries the full citation; the essential trace is:

* **b01–b04** — bracket range / negation. Pattern `[b-d]`, `[^abc]`. criteria.c:333
  `regcomp(value, REG_EXTENDED|REG_NOSUB)`; criteria.c:115-119 `match_regex_criteria` →
  `regexec`. Oracle: `match`/`match`/`nomatch`/`nomatch`.
* **b05** — capture group under `REG_NOSUB`. Pattern `(ab)+`. criteria.c:333 compiles it
  (`REG_NOSUB`, regex.h:323, suppresses submatch *reporting* only); criteria.c:115-119.
  Oracle `match`.
* **b06/b07** — backreference. Tokenizer (criteria.c:199-215 → 177-182) turns `\\1` into
  `\1` and `(a)\\1` into `(a)\1`. b06: criteria.c:333 regcomp succeeds (glibc extension),
  criteria.c:115-119 → `match` on `aa`. b07: criteria.c:333-336 `regcomp("\1")` fails
  (REG_ESUBREG) → "Invalid summary~ regex" → `apply_criteria_field` false →
  `parse_criteria` false → config.c:844-848 refuses the section. Oracle `invalid`.
* **b08–b10** — `^`/`$` inside alternation. Pattern `^a|b$`. criteria.c:333 + 115-119.
  Oracle `match`/`nomatch`/`match` — each branch anchors independently.
* **b11/b12** — `.` against newline-free text. Patterns `. $` and `a.b`. criteria.c:333 (C
  locale, no `setlocale` in the tree) + 115-119. Oracle `match`, `match`.
* **b13/b14** — escaped metacharacters **through the tokenizer**. `\(x\)` → `(x)`: a
  *capture group*, so it matches the bare text `x` (oracle `match`); `\[` → `[`, and
  `regcomp("[")` fails (oracle `invalid`) → refusal. criteria.c:177-182, 199-215, 333-336.
* **b15** — the space-only rule. `summary~=Setup Wi-Fi` splits into two tokens
  (criteria.c:207-215); the second has no `=` (criteria.c:269) so it is a bare boolean
  field (criteria.c:272-286) and `Wi-Fi` is not a boolean field → criteria.c:399-407
  "Invalid boolean criteria field" → refusal. The `=`-form of the same rule is b16.
* **b16** — the same split, but the second token *is* a valid field: `summary~=Setup` and
  `app-name=alpha`, both applied (criteria.c:207-215 → 267-411). criteria.c:74-77 (app-name
  strcmp) and 115-119 (regex) both hold → the section applies. Oracle `match`.
* **b17/b18** — quotes inside a value. `\"` inside a quoted value is kept verbatim
  (criteria.c:184-196 + 177-182) → pattern `say "hi"`; an *unquoted* `"` opens and closes a
  quoted run (criteria.c:204-206, 189-190) so both quotes vanish → pattern `sayhi`.
  criteria.c:333 + 115-119. Oracle `match`, `match`.
* **b19** — a value containing `=`. criteria.c:269 `strstr(key,"=")` splits at the **first**
  `=` only, so the value is `a=b`; criteria.c:333 compiles it (`=` is an ordinary byte);
  criteria.c:115-119. Oracle `match`.
* **b20/b21/b22** — the backslash-dropping rule, three ways. `a\.b` → `a.b` (the `.` is now
  the ERE any-character operator, so `axb` matches); `a\\.b` → `a\.b` (a literal dot, so
  `a.b` matches and `axb` does not). criteria.c:177-182, 199-215, 333, 115-119.
  Oracle `match`, `match`, `nomatch`.
* **b23/b24** — `body~` with anchors. Pattern `^beta$`. criteria.c:127-131 matches
  `body_pattern` against `notif->body` via criteria.c:47-58. Oracle `match`, `nomatch`.
* **b25** — `body~` with the body absent (only `--summary` given). criteria.c:127-131 can
  only be satisfied against a body; with no body input the criterion is refused. Same tool
  stance as the draft case r19, whose oracle verdict is likewise `undecided`.
* **b26/b27** — two regex fields in one section; **both must match**. criteria.c:115-119 and
  127-131 are independent tests; criteria.c:498-551 `validate_criteria` refuses only
  `summary`+`summary~` and `body`+`body~`, so `summary~`+`body~` is legal. Oracle
  `match`+`match` (both hold) and `match`+`nomatch` (the body branch fails).
* **b28/b29** — regex + `app-name`. criteria.c:74-77 (strcmp) and 115-119. Oracle `match`,
  `nomatch`.
* **b30/b31** — regex + `urgency`. criteria.c:91-93 (enum compare) and 115-119. b31 is the
  interesting one: the regex *does* match (`match`) but the urgency test fails first, so the
  section does not apply — a **non-match**, not a refusal.
* **b32/b33** — a repeated `summary~` token; the **last** wins. criteria.c:207-215 and
  241-247 call `apply_criteria_field` once per token; criteria.c:332-339 `regcomp`s into the
  same `criteria->summary_pattern` each time, and glibc's second `regcomp` replaces the
  compiled program (measured, `$S/d1.c`). Oracle `match` on `beta`, `nomatch` on `alpha`.
* **b34/b35** — invalid patterns: `[abc` (REG_EBRACK) and `*a` (REG_BADRPT). Both fail at
  criteria.c:333-336 → refusal. Oracle `invalid`, `invalid`.
* **b36** — `a)` is *valid* on glibc (an ordinary `)`), matching the literal `a)`.
  criteria.c:333 + 115-119. Oracle `match`.
* **b37** — `x|` compiles; the empty second branch matches the empty string at offset 0, so
  the pattern matches any text. criteria.c:333 + 115-119. Oracle `match`.
* **b38/b39** — a POSIX class inside a negated set: `[^[:digit:]]`. Oracle `match` on `a`,
  `nomatch` on `5`.
* **b40/b41** — tokenizer errors. A trailing backslash → criteria.c:228-236 "Trailing
  backslash in criteria definition"; an unterminated quote → criteria.c:228-231 "Unmatched
  quote in criteria definition". Both → `parse_criteria` false → config.c:844-848 refuses
  the section. No pattern ever reaches `regcomp`, so the oracle verdict is `undecided`.
* **b42** — the C locale, counted in bytes: `é` is two bytes, so `^..$` matches it
  (`match`) while the draft's r08 `^.$` does not. criteria.c:333 + 115-119.
* **b43** — `!` inside a value is literal. criteria.c:269-286 splits at the first `=` and
  the `!` negation prefix (criteria.c:281-285) applies only to a **bare** key, so the
  pattern is `!x`. criteria.c:333 + 115-119. Oracle `match`.
* **b44** — `body~` reads the **body**, not the summary: the summary is `gamma` (which would
  match the pattern) but the body is `delta` (which does not). criteria.c:127-131.
  Oracle `nomatch`.
* **b45** — `!summary~=x` is not a known field: criteria.c:267-272 takes the key
  `!summary~`, which matches none of criteria.c:297-373, so criteria.c:399-407 "Invalid
  criteria field" → refusal.

## Coverage against the item's checklist

| Item asked for | Cases |
| --- | --- |
| bracket ranges / negation (`[^…]`, `[a-c]`) | b01, b02, b03, b04, b38, b39 |
| backreference `\1` in ERE (glibc extension — checked what the oracle says) | b06 (`(a)\1` → match), b07 (`\1` alone → invalid) |
| `REG_NOSUB` with capture groups | b05 |
| `^`/`$` inside alternation | b08, b09, b10 |
| `.` against newline-free text | b11, b12 |
| escaped metacharacters through the tokenizer (`\[`, `\(` → `[`, `(`) | b13, b14, b20, b21, b22 |
| quotes inside a value | b17, b18, b41 |
| a value containing `=` (only the first `=` splits) | b19 |
| `body~` with summary given but body absent | b25 |
| two regex fields in one section (both must match) | b26, b27 |
| regex + urgency / app-name combined | b28–b31 |
| repeated `summary~` token (last wins) | b32, b33 |
| invalid patterns `[`, `*a`, `a)` (each checked) | b14/b34 (`[`), b35 (`*a`), b36 (`a)` — **valid**, contrary to a POSIX reading) |

Beyond the checklist, the file adds the tokenizer's backslash-dropping rule in three
readings (b20–b22), the space-only token-split rule in both of its outcomes (b15, b16),
the `!` handling in a value vs. as a key prefix (b43, b45), byte-counting in the C locale
(b42), the `body~`-reads-body-not-summary direction (b44), and two tokenizer errors
(b40, b41).

## Validation performed

| Check | Command | Result |
| --- | --- | --- |
| JSON parses | `python3 -c "json.load(...)"` | OK |
| schema / keys | `json.load` → `schema == "mako-cases-r89-v1"`, case keys `{id, config, home_files, args, expect, pin, oracle}`, `expect` keys `{effective, refusals}` | OK |
| id regex `^[a-z0-9][a-z0-9-]{0,63}$` | re-checked in the verifier | 45/45 OK |
| ids unique, no collision with `c01`–`c62`/`r01`–`r30` | verifier | OK (0 collisions) |
| no duplicated (header, args, expectation) triple | verifier | OK (0 duplicates) |
| no regex header shared with the draft file | verifier | OK after I changed b11's header |
| every expectation re-derived from the written artifact with a **second** tokenizer + the oracle | `python3 $S/verify.py` | `VERIFY OK`, exit 0 |
| every pin cites a `criteria.c`/`config.c` line and a `regcomp`/`regexec` step | verifier | 45/45 OK |

### Two errors my own verifier caught (and I fixed)

1. **b13 was wrong.** I first expected `summary~=\(x\)` to *not* match the text `(x)`.
   The oracle said `match`, correctly: the tokenizer **drops** the backslash
   (criteria.c:177-182), so the pattern is `(x)` — a capture group that matches the bare
   text `x` anywhere. I corrected the case (and added b14 so the drop is also visible as a
   *failure*).
2. **b11 duplicated the draft.** `[summary~=^.$]` is already the draft's r08 header. I
   changed b11 to `[summary~=.$]` so no regex header in the blind file collides with the
   draft. A related draft collision I also removed: my original b43 used `[summary~=a]]`,
   whose doubled `]` depends on how the config section header is sliced — replaced by the
   `!`-inside-a-value case (b43) which has no such dependency.

## Open questions for the L1 (not resolved by this seat)

* **b25** ("`body~` with the body absent") is the one expectation that rests on the *tool's*
  stance rather than on upstream: upstream `match_criteria` (criteria.c:127-131) would
  simply not match an empty body, it does not "refuse". The draft case r19 already
  establishes the tool stance ("a field without its input is refused", oracle `undecided`),
  so b25 follows r19 — but the L1 should confirm the stance generalises to "the body is
  absent while a summary is present", which is exactly b25's shape.
* **b40/b41** are tokenizer *errors*, not `regcomp` errors. Upstream rejects them at
  criteria.c:228-236 before any pattern is compiled, so their oracle verdict is
  `undecided`. Whether the candidate models "unmatched quote" / "trailing backslash" at all
  is unknown to me (I did not open it); the draft's c29 already covers the unmatched-quote
  path, so b41 has precedent and b40 does not.
* Whether the L1 wants the blind file **appended** to `mako-cases-r89.json` or kept as a
  separate file is the L1's call; I wrote a separate file (`...-blind.json`) so that the
  draft file stays byte-equal for the carried-case check. The blind file's `schema` is
  `mako-cases-r89-v1`, the same as the draft's, so a merge is mechanical.

## Scratch

`S=$HYAKU_SCRATCH/mado-r89/R89MScoutCases` (= `/fast/scratch/hyaku/mado-r89/R89MScoutCases`),
created with `mkdir -p` and used for the upstream tarball, `criteria.c`, the built oracle
`ore`, the tokenizer replica `tok.py`, the generator `gen.py`, the verifier `verify.py` and
the small C probes `d1.c`/`rc.c`/`rc2.c`/`rc3.c`. It is deleted on exit
(`trap 'rm -rf -- "$S"' EXIT`). No install was needed — `cc`, `curl` and `python3` were
already on the host, so there is nothing to record under the tooling directive.
