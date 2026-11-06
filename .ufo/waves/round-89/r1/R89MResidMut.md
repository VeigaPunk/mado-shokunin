# R89MResidMut — residual mutation probe of the landed C1 tool against the FROZEN case set

Seat: mutation-tester (residual attack seat `r1`). Lane: `mado-shokunin`. Round 89, hyaku run 15, attempt 1.
Scope: the frozen and measured bytes only. The claims, the predicates, the case set and the tool are not
changed here; survivors route to round 90 as coverage findings. No lane file was written except this
report; no git/jj mutation was run anywhere (no fixture repo was needed — every mutation was applied
in memory to the bytes of `A`).

## 1. Bytes under test (read with `git show <rev>:<path>`, never the working tree)

| item | rev | sha256 | check |
|---|---|---|---|
| tool `tools/mado-mako.py` | `A = 099c662dc55521e365cd4126132cdcda4efc54b6` | `6b4bc409750f493469ce789b6b6c0c072d6ab638ff7e90dc9b31d642ae673a98` | = declaration pin for `build/mado-mako.c1.py` |
| base tool `tools/mado-mako.py` | `af998dcc41d48618ffe7afe0efc9354755a9244e` | `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237` | = declaration base / C2 measured tool |
| `quality/counters/c1-r89-mako-regex.py` | `F = d87361354b4d142287aac05bb973315749ef1fce` | `5b977141ec1f21911c6247d250900bcd6ec35ae16213318e41ef8f5c4111634e` | = declaration pin |
| `quality/counters/c1-r88-mako-fields.py` (pinned machinery) | `F` | `3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f` | = declaration pin |
| `quality/counters/c1-r87-mako-criteria.py` (pinned machinery) | `F` | `4d801c30b302ed5972142415012d8f461109459d9c44e85e0badef57a2ed3645` | = `R87_COUNTER_SHA256` inside the r88 counter |
| `.ufo/waves/round-89/controls/mako-cases-r89.json` (N=141) | `F` | `5fdca7dbcce6687d81aa31548e935a49fa39cee03117db41358068a0ded15672` | = declaration pin |
| `.ufo/waves/round-89/controls/mako-mutants-r89.json` (M=37) | `F` | `5471bee29b4ba5da7fa7e55d8b11003028b0eb4c7937bd8d114062491338e35f` | = declaration pin (used only to prove non-duplication) |

All eight files were materialized into `$S` with `git show`, and the three counters sit in
`$S/quality/counters/` so the counter's own `HERE`-relative load of the pinned machinery is the one under
test (`R88_COUNTER = os.path.join(HERE, "c1-r88-mako-fields.py")`). The counter hashes were re-checked
inside the scratch (`sha256sum`) and equal the table above before any scoring ran.

## 2. Method

Driver `$S/harness.py` imports the frozen counter from its F bytes (`importlib`), loads the F case file
with the counter's own `R88.load_cases`, and scores each mutation with the exact call the seat tasking
fixes (all positional up to `carried`):

```python
m.score(mutant_text, base_text, cases, [], S, 61, declared=None, range_check=False)
```

with `mutant_text = tool_A_text.replace(old, new, 1)` after asserting `tool_A_text.count(old) == 1`
(15/15 anchors occur exactly once, so no mutant is a setup error), `base_text` = the base tool bytes,
`S` = `$S`. **Kill rule** (the counters' own, `quality/counters/c1-r88-mako-fields.py:202,205-209`): a
mutant is *killed* iff on some case its verdict differs from the candidate's and it produced a
well-formed result there (exit 0, JSON object with `effective` and `refusals`); a crash is not a kill.

Two controls on the method itself:

1. **The counter's own `verdict` field is not used for the mutant verdict.** With `mutants=[]` and
   `declared=None`, `predicate()` sees `killed == m == 0` and prints `TARGET_MET` for any mutant that
   is correct on every case (e.g. RS01's score file says `TARGET_MET`). The kill determination below is
   the per-case verdict diff parsed from the run's `case <id> ok|FAIL <why>` lines, as the
   `semantic_kill` rule requires.
2. **Independent per-case differential.** `$S/harness.py diff <id>` re-runs the candidate and the mutant
   over all 141 cases through the same machinery runner (`R88.materialize` + `R88.run_tool`) and
   compares rc, full stdout bytes and `tool_verdict`. Its `semantic_kills` equal the score's
   `FAIL` case lists for all 15 mutants (e.g. RS03 7 = 7, RS10 2 = 2, RS14 8 = 8), so the two paths agree.

**Forgery-anchor handling (structural, three mutants).** The counter's python-re control is forged from
three exact anchors: the `posix_ere_compile` body, the `posix_ere_search` return line, and the
`_libc().regfree(compiled)` line. Three mutants deliberately change those lines, so `score()` gets a
rebuilt anchor tuple (its `forgery=` keyword) instead of `PYRE_FORGERY`:

* RS02 / RS03 — anchor 2 is rebuilt from the mutant's own `regexec(...)` line;
* RS08 — `posix_ere_free` is already a no-op in the mutant, so anchor 3 is a verified no-op replace.

The control values are unchanged under every rebuild (`naive 34 / globals 35 / base 78 / python-re 127`
for RS02, RS03, RS08 — identical to the unmodified run), so the rebuilt control is still the same
python-re forgery.

## 3. Baseline reproduction (the candidate on the frozen cases, through the frozen counter)

`TOOL` (the unmodified A bytes) scored through the same call:

```
correct=141/141  controls naive=34 globals=35 base=78 python_re=127  sha256=6b4bc409…673a98
```

That is exactly `receipts/c1-measured-A-r89.txt` (`cases=141 correct=141 … naive_correct=34
globals_include_correct=35 base_tool_correct=78 python_re_correct=127`) and the tool pin, so every
mutant below is scored against the same measured configuration. The same bytes run twice through the
per-case differential produce 141/141 byte-identical outputs (the runner is deterministic), which is
the control for the divergence counts in §6.

## 4. Mutants (15, none in M01–M37) and verdicts

Non-duplication checked mechanically against the frozen list: no id, no `(old,new)` pair, and no anchor
string of the 15 occurs in `mako-mutants-r89.json`. (RS06 is a deliberately *narrower* semantic sibling
of frozen M31 — same site, `char in " \t"` vs `char.isspace()` — and is killed by the same case; see
§5.)

Line numbers are `tools/mado-mako.py` at `A`.

| id | site | semantic change | verdict | differing frozen cases | mutant correct |
|---|---|---|---|---|---|
| RS01-body-earlier-invalid-ignored | `:431` | only the last `body~` occurrence is compiled (the r32/M37 earlier-invalid rule is dropped for `body~` only) | **survived** | — | 141/141 |
| RS02-search-encode-strict | `:151` | `text.encode("utf-8","surrogateescape")` → `text.encode("utf-8")` | **survived** (crash-only) | — (141/141 identical) | 141/141 |
| RS03-regexec-noteol | `:151` | `regexec(..., eflags=2)` (REG_NOTEOL) | **killed** | r05, r28, r29, b10, b11, b23, b42 | 134/141 |
| RS04-both-check-after-compile | `:423-441` | the cannot-set-both refusal moved after the compile loop | **survived** (text-only) | — (141/141 identical) | 141/141 |
| RS05-quote-start-not-started | `:289-291` | opening a quote no longer marks the token `started` | **survived** | — (141/141 identical) | 141/141 |
| RS06-tab-splits | `:299` | a tab also separates tokens (`char in " \t"`) | **killed** | r16 | 140/141 |
| RS07-setlocale-lc-ctype-only | `:124` | `LC_ALL` → `LC_CTYPE` (LC_COLLATE stays at the inherited `C.UTF-8`) | **survived** (equivalent, §6.4) | — (141/141 identical) | 141/141 |
| RS08-regfree-skipped | `:154-155` | `regfree` never runs | **survived** (equivalent, §6.4) | — (141/141 identical) | 141/141 |
| RS09-undecided-names-regex-key | `:479` | the "needs" refusal names `--summary~`/`--body~` instead of `--summary`/`--body` | **survived** (text-only) | r19, b25 (both still `ok`) | 141/141 |
| RS10-last-equals-splits | `:301` | every `=` splits key from value | **killed** | c17, b19 | 139/141 |
| RS11-nosub-constant-zero | `:116` | `REG_NOSUB = 0` (regcomp flags 1 instead of 9) | **survived** (equivalent, §6.4) | — (141/141 identical) | 141/141 |
| RS12-group-index-accepted | `:396` | `group-index`/`grouped` accepted instead of refused | **survived** | — (141/141 identical) | 141/141 |
| RS13-both-check-summary-only | `:425` | cannot-set-both enforced for `summary`/`summary~` only | **killed** | r18 | 140/141 |
| RS14-quotes-literal | `:289-291` | `"` is an ordinary character, never a grouping marker | **killed** | c15, c29, r01, r14, r26, b17, b18, b41 | 133/141 |
| RS15-regex-field-lookup-default | `:477` | `REGEX_FIELDS[key]` → `REGEX_FIELDS.get(key, key)` | **survived** (equivalent, §6.4) | — (141/141 identical) | 141/141 |

Mutant text sha256 (full): RS01 `f6634593b5c5c0967752c722c2cfe0f5db4bca81a221fea1b481d2db30230466`,
RS02 `58471f53745f026fb77d4b2e41a826f45fd9edf79f2edc56b4123a05494e6a91`,
RS03 `c9c7cddabfaf62024fbf36cfdf25d26f31bdcffcb5c90cc4c9b24ac2f6343917`,
RS04 `f16f81477bf5231adaa1ad7e9b4f87b1eed26406cf20c83622f56bf5cbdcf3b5`,
RS05 `960a1ab33f82c5e66ad159ef392a494b25f7f6e08375e1b2f7e356f0aa6db3db`,
RS06 `75ef1806a68501ca9d6fa75ea82e8530a862a2769179ebe1570a6401c075b1ab`,
RS07 `f988c41855a5d176cd4d0811dfe615ccc4402b5800aeede9ba7962901bbe0ad5`,
RS08 `f8230247cdf604fcc93b4572267e99f356b78e2d3e2806a628526de7ac77fd66`,
RS09 `630be071521d359fc8635c25d24a3e3c1eb4fd82beba5cb77b1a288a9313254c`,
RS10 `099618d2eb4a7a12395b643a3643d3ad3384d63c33fed7f0113c9f6c29104468`,
RS11 `e93fb9cc79bf0295357f05c8be69da7a75ab56dbf5d6fe1437a0d65f9f8408d8`,
RS12 `0602db39903c453cf93331564152653b690cda2f661a6d148a7fab18bbe917a7`,
RS13 `4c9864836c0774fe9c735a64847a41728336864dc5e1863c45b211882fae88ef`,
RS14 `2e58281b2bf880dee56c2fe7c7a16d9d0fe223820ba79dee9d16758e155a212d`,
RS15 `6fc11452a66970ef282b59b45e05d6cbe3d53f5af40ff3ebbdd18cd3f730e10d`.

## 5. Killed mutants — what the frozen set already pins

| mutant | detector case(s) | candidate output | mutant output |
|---|---|---|---|
| RS03 REG_NOTEOL | r28 `[summary~=Fi$]` + summary `Setup Wi-Fi` (also r05, r29, b10, b11, b23, b42) | section applies, `anchor=bottom-center` | `$` no longer matches end-of-string → nomatch, `anchor=top-right` |
| RS06 tab splits | r16 `[summary~=a<TAB>b]` + summary `a<TAB>b` | `anchor=bottom-center`, no refusal | the tab splits the token, `b` is bare → refusal, `anchor=top-right` |
| RS10 last `=` splits | c17, b19 `[summary~=a=b]` + summary `a=b` | `anchor=bottom-center` | key becomes `a` → unknown field → refusal, `anchor=top-right` |
| RS13 both-check summary-only | r18 `[body=x body~=y]` + body `x` | refusal, `anchor=top-right` | no refusal, `anchor=top-right` (`missing-refusal`) |
| RS14 quotes literal | c15, r14, r26, b17, b18, b41, c29, r01 | quote grouping, expected effective | literal `"` in the value / no grouping → mismatch or refusal |

Direct check that the eflags-2 mutation is real (not just an expectation artifact), via libc on this host:

```
regcomp("Fi$", REG_EXTENDED|REG_NOSUB) rc=0 ; regexec(eflags=0)="Setup Wi-Fi" -> 0 ;
regexec(eflags=2) -> 1   ($ blocked at end-of-string)
```

RS14's ninth divergence (`n07-dangling-quote-escape-refused`) changes only the refusal text (both
verdicts `ok`), i.e. the same text-only blindness discussed in §6.2. **RS06 is redundant with frozen
M31**: `char.isspace()` (M31) subsumes `char in " \t"` (RS06) and both die on r16, so RS06 adds no case
coverage — reported for completeness, not as a finding.

## 6. Survivors — distinguishing case or equivalence

Every survivor below was re-run in a per-case differential over all 141 frozen cases (rc + full stdout
bytes). Counts of *byte-identical* outputs are given; "well-formed separator" means a case on which the
candidate is `ok` and the mutant exits 0 with valid JSON but differs.

### 6.1 Well-formed separators exist — the frozen set lacks the case (routable)

All three probes were built outside the frozen set and run through the frozen machinery's own runner
(`R88.materialize` + `R88.run_tool`, same env/cwd/timeout). In each: **candidate `ok`, mutant `ok`-exit
and differing** — a genuine kill case, not an expectation artifact.

1. **RS01 — `body~` earlier-invalid occurrence (141/141 identical on the frozen set).**
   The r32 case `[summary~=a(b summary~=x]` pins "an earlier invalid occurrence still rejects" for
   `summary~` only; no frozen case has two `body~` occurrences (checked: 0 of 141).
   Probe `p1-body-earlier-invalid`: `anchor=top-right` + `[body~=a(b body~=x]` + `anchor=bottom-center`,
   `--body x` →
   candidate: `refusals=[…:2: body~ 'a(b' is not a valid POSIX extended regex (regcomp refused it)]`,
   `anchor=top-right`, verdict `ok`;
   mutant: `refusals=[]`, `anchor=bottom-center`, verdict `missing-refusal`, rc 0.
   Missing case: `body-pattern-earlier-invalid-occurrence` (expect `refusals: present`, section not applied).
2. **RS05 — bare quoted token (141/141 identical).**
   No frozen header has a token that starts with a quote and has no `=value` (checked: 0 of 141; b17's
   `""` is inside a value, after `summary~=` which already marks the token started). The declaration's
   named limit already says a standalone `""` token is refused by the tool; that behavior has no case.
   Probe `p2-bare-quoted-token`: `anchor=top-right` + `["x"]` + `anchor=bottom-center` →
   candidate: `refusals=[…: criteria token 'x' has no '=value' …]`, `anchor=top-right`, `ok`;
   mutant: token dropped → empty header → section matches, `refusals=[]`, `anchor=bottom-center`,
   `missing-refusal`, rc 0.
   Missing case: `bare-quoted-token-refused` (or the declared `""` form).
3. **RS12 — `group-index`/`grouped` accepted (141/141 identical).**
   The claim's named limit says the two second-pass fields "stay refused", but no frozen case contains
   either word (checked: 0 of 141). The refusal is live in the candidate and absent in the mutant.
   Probe `p3-group-index-section`: `anchor=top-right` + `[group-index=1]` + `anchor=bottom-center` →
   candidate: `refusals=[…: criteria field 'group-index' is outside the model (refused)]`,
   `anchor=top-right`, `ok`; mutant: `refusals=[]`, `anchor=bottom-center`, `missing-refusal`, rc 0.
   Missing case: `group-index-field-refused` (turns the named limit into a scored case).

### 6.2 Text-only divergences — the declared named limit (N09), extended to refusal *precedence*

`tool_verdict` compares `effective` values and only the *presence* of refusals
(`quality/counters/c1-r87-mako-criteria.py:245-248`); refusal strings are never compared. So:

4. **RS04 — both-check moved after compile (141/141 identical on the frozen set).**
   The mutant differs only when a header sets both fields *and* the pattern is invalid: the refusal
   precedence flips. Probe `p4-both-set-invalid-pattern` (`[summary=x summary~=(]`, `--summary x`):
   candidate refuses `criteria sets both summary and summary~ (criteria.c: cannot set both)`; mutant
   refuses `summary~ '(' is not a valid POSIX extended regex (regcomp refused it)`. Both `ok`
   (refusals present, `anchor=top-right`), rc 0. No frozen case has both-set + invalid pattern, and
   even if it did the verdict would not move — this is the N09 limit applied to refusal *order*, not
   only wording. Not routable as a case without changing the case schema (which asserts only
   presence/count), i.e. an instrument limit, not a tool defect against the frozen language.
5. **RS09 — the "needs" refusal names the field key (2 divergences: r19, b25; both `ok`).**
   Candidate: `criteria needs --body to decide the match; section not applied`; mutant:
   `criteria needs --body~ …`. Same verdict, same effective. This is a direct instance of the declared
   named limit (declaration §Named limits: "Mutation-tester N09 (refusal message text) is not
   observable by the case language"). **Named-limit confirmation, not a routed defect.**

### 6.3 Crash-only (RM6C2 class) — no well-formed separator exists

6. **RS02 — strict encoding of the matched text (141/141 identical on the frozen set).**
   The candidate encodes the summary/body with `surrogateescape`, so an argv byte that is not valid
   UTF-8 (Python surfaces it as a lone surrogate) is matched byte-wise. The mutant raises
   `UnicodeEncodeError` before matching. Probe `p6-non-utf8-summary-byte` (`--summary` = `\udc80a`,
   pattern `a`): candidate rc 0, `refusals=[]`, `anchor=bottom-center`, `ok`; mutant rc 1,
   `UnicodeEncodeError: 'utf-8' codec can't encode character '\udc80' …: surrogates not allowed`.
   Every input that separates the two makes the mutant **crash**, and the frozen kill rule counts a
   crash as *not* a kill (`c1-r88-mako-fields.py:202,205-209`), so this mutant is unkillable by the
   frozen language even though a case could be written. It is the same class as the declared RM6C2:
   a real behavioral difference (candidate resolves, mutant dies), but not a kill. Routing note: a
   round-90 counter that wants it needs an explicit "crash on an input the candidate resolves counts
   as killed" element (a predicate change), or it stays a named limit.

### 6.4 Equivalent on these bytes — argued and, for four, evidenced

7. **RS07 — `LC_CTYPE` only vs `LC_ALL`.** glibc's regex takes multibyte/character-class behavior from
   `LC_CTYPE` and range collation from `LC_COLLATE`; the mutant leaves `LC_COLLATE` at the inherited
   `C.UTF-8`, whose collation is byte order and whose `MB_CUR_MAX` is overridden by `LC_CTYPE=C` in
   both variants. Evidence: a libc probe over **400 synthetic pattern/text pairs** (`[[:alpha:]]`,
   `[[:upper:]]`, `[a-z]`, `[^a-z]`, `[[:print:]]`, `[[:space:]]`, `[[:word:]]`, `\w`, `\W`, `[]a]`,
   `[-a]`, `[a-]`, `[à-ÿ]`, UTF-8 literals, `.`, `^.$`, … × ASCII/Latin-1/UTF-8/control texts) and the
   **69 (pattern, text) pairs extracted from the frozen case set** produced **0 differences**; plus
   141/141 byte-identical case outputs. Environment-scoped equivalence: a locale whose collation is
   not byte order (a real non-C.UTF-8 `LC_ALL`) would separate them, which is a hazard for a later
   host, not a defect of the frozen bytes.
8. **RS08 — `regfree` skipped.** Output is identical on all 141 cases (byte-for-byte) and the process
   is one-shot (one notification per invocation), so the leak is unobservable; it is a resource
   defect for an embedding, not a behavioral one under this language.
9. **RS11 — `REG_NOSUB = 0`.** POSIX/glibc: `REG_NOSUB` only controls whether subexpression offsets are
   recorded; `regexec` is called with `nmatch=0`, so the result is unchanged. 141/141 identical outputs.
10. **RS15 — `REGEX_FIELDS.get(key, key)`.** Total-map argument: `key` is always `"summary~"` or
    `"body~"` at that site, and both are keys of `REGEX_FIELDS`, so the default is never taken; the
    expression is extensionally identical to the indexed read. 141/141 identical outputs.

Summary of survivor classes: **3 routable case gaps** (RS01, RS05, RS12), **2 text-only / declared
limit** (RS04, RS09), **1 crash-only** (RS02), **4 equivalent on these bytes** (RS07, RS08, RS11, RS15).

## 7. Routing to round 90 (case-set additions only; the predicate, the tool and C1/C2 are untouched)

1. `body-pattern-earlier-invalid-occurrence`: `[body~=a(b body~=x]`, `--body x` → `refusals present`,
   section not applied (the r32 twin for `body~`). Kills RS01.
2. `bare-quoted-token-refused` (`["x"]`, and optionally the declared `""` form) → `refusals present`.
   Kills RS05.
3. `group-index-field-refused` (`[group-index=1]`) → `refusals present`, section not applied; makes the
   declaration's named limit executable. Kills RS12.
4. `non-utf8-summary-byte` (a lone argv byte `0x80` in `--summary`, pattern `a`) → section applies,
   `refusals none`: pins the `surrogateescape` byte-wise path the claim asserts. RS02 then **crashes**
   rather than diverging, so it would still be `crashed-not-killed` under the frozen rule — route it
   only together with an explicit crash rule, or record it as a named limit.
5. Refusal *text/precedence* (RS04, RS09): not expressible by the current case schema; already a
   declared named limit for wording. If precedence is to be pinned, the schema needs a refusal-reason
   assertion — a claim-element change, to be declared before data, not a predicate tweak.

## 8. Dead steps (scratch only, with error text)

1. First timing probe passed a **relative** tool path with `cwd=home`, so `python3 -I tool-A.py` exited
   `rc=2` (argparse could not open the script). Fixed to an absolute path; real per-run cost 41 ms.
2. `locale_probe.py` first run: `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position
   31398` — after `setlocale(LC_ALL,"C")` in the same process Python's default `open()` encoding becomes
   ASCII. Fixed with `encoding="utf-8"`; the 400-pair battery had already printed `diffs=0`.
3. RS15's first validation: `FAIL RS15-regex-field-lookup-default: anchor occurs 0 times` — the anchor
   was written at the wrong indentation (20 spaces; the site is at 16). Fixed; re-validate `OK`.

No mutant was unscoreable (15/15 scored through the frozen counter), and no mutant crashed on any frozen
case (`crashed=0` for all 15 rows).

## 9. Restoration evidence

The measured bytes were never edited: mutations were produced in memory and written only into
generation directories the machinery removes in its `finally` block (`evaluate`'s `mkdtemp`, and this
seat's own differential/probe dirs, removed with `shutil.rmtree`).

| artifact | sha256 before | sha256 after |
|---|---|---|
| `$S/tool-A.py` (bytes of `099c662d:tools/mado-mako.py`) | `6b4bc409750f493469ce789b6b6c0c072d6ab638ff7e90dc9b31d642ae673a98` | `6b4bc409…673a98` (`sha256sum` re-run after all scoring) |
| `$S/base-tool.py` (bytes of `af998dcc:tools/mado-mako.py`) | `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237` | `c374d715…92237` |
| `$S/quality/counters/*.py`, `$S/mako-cases-r89.json` | pins of §1 | unchanged (same `sha256sum`) |
| lane working tree | — | no lane path written except this report; no git/jj mutation |
| scratch `$S` = `/fast/scratch/hyaku/mado-r89/R89MResidMut` | — | deleted on exit |

## 10. Commands and exit codes

| # | command | rc |
|---|---|---|
| 1 | `git -C mado-shokunin show <rev>:<path> > $S/…` for tool-A, base-tool, three counters, cases, frozen mutants | 0 |
| 2 | `sha256sum $S/…` (eight digests equal §1) | 0 |
| 3 | `python3 harness.py validate` (anchors, compile, forgery anchors, REG_NOTEOL probe) | 0 |
| 4 | `xargs -P 6 … harness.py score/diff` over TOOL + 15 mutants (32 jobs) | 0 |
| 5 | `python3 probe_case.py TOOL` (six probes; candidate `ok` on all six) | 0 |
| 6 | `python3 probe_case.py <id>` for RS01, RS02, RS04, RS05, RS09, RS12 | 0 |
| 7 | `python3 locale_probe.py` (400 + 69 pairs, `diffs=0`) | 0 |
| 8 | `git -C mado-shokunin status --porcelain` / `rev-parse HEAD` (read-only) | 0 |

No installs: python3 3.14.8 and libc on the host were sufficient; no pacman transaction was attempted.

## 11. Verdict

The frozen C1 bytes stand: the candidate reproduces `141/141` with the measured control values, and the
frozen set kills 5 of 15 new mutants outright (19 case-level kills), so the detector works on exactly
these bytes. The residuals route to round 90 as **case-set coverage**, not as a predicate change:
`body~`'s earlier-invalid occurrence, a bare quoted token, and the declared `group-index` refusal have
no frozen case at all; refusal text/precedence is blind by the declared N09 limit; and the
`surrogateescape` path is pinned only up to a crash (RM6C2 class). Four mutants are equivalent on these
bytes (locale category, leak, REG_NOSUB, `dict.get` default) and do not deserve a case.
