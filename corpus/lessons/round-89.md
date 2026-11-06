# mado round 89 — lessons

Round 89, hyaku run 15, attempt 1. Two frozen claims from `.ufo/waves/round-89/claims-declaration-r89.md` (freeze
`d87361354b4d142287aac05bb973315749ef1fce`): C1 coverage capability (mako `summary~`/`body~` matched as POSIX extended
regex through libc in the C locale, with upstream's criteria tokenizer escapes) and C2 operability (a runnable survivor
gate that kills seven of round 88's eight routed survivors; RM6C2 declared crash-only before data).

## Mistakes

**M89-1 — a crash was routed as a distinguishing probe, although the same report states that a crash is not a kill.**
Class: evidence-inference — an abnormal termination read as a semantic difference.
Evidence: `.ufo/waves/round-88/r1/R88MResidMut.md:131` routes the missing case `probe-cycle-via-second-lexical-path`
with `mutant `FAIL exit=1` (RecursionError)`, and `:192-195` (§8) lists "cycle detection through a second lexical
path is untested" among the C2 coverage gaps — while `:38` of the same report states the frozen rule: "a mutant that only crashes is reported as
`crashed-not-killed`, per the frozen rule." The rule's implementation is
`quality/counters/c2-r88-include-containment.py:225` (`status = "killed" if hit else ("crashed-not-killed" if crashed else "survived")`),
with the predicate note at `:168` ("a crash is not a kill") and the selftest at `:471-475`; the C1 counter carries
the same rule at `:281`, `:207` and `:563-566`. On that probe the correct tool refuses with `cycle` and the mutant
only recurses, so the probe is a statement about the mutant's termination, not about a wrong answer.
Captured-by: **none in round 88** — the probe ran outside the frozen case set, so no scorer ever assigned the
mutant a status for it. Round 89's C2 declaration
(`.ufo/waves/round-89/claims-declaration-r89.md` §C2, "RM6C2 is declared crash-only before data") re-reads the
probe against the kill rule, excludes RM6C2 from the 7-of-7 target with the argument that no terminating input
separates it, and keeps `s2-cycle-second-lexical-path` in the supplementary set with its crash printed.
Fix: the declaration declares RM6C2 crash-only before data (not after a miss), and QUALITY criterion 148 makes a
probe's scorer-assigned status the evidence a survivor routing needs:
> **148. A survivor is a coverage gap only when a probe makes the mutant return a well-formed wrong answer.** A seat
> that routes a survivor names the probe, the correct tool's result, and the mutant's result *as the scorer assigned
> it* — a `killed`/semantic verdict, not a process exit status. A probe on which the mutant terminates abnormally
> (nonzero exit, traceback, abort, timeout) distinguishes nothing: it is recorded as "no separating input found",
> the crash is kept as evidence, and the mutant is declared crash-only or equivalent. Check: re-score the probe
> through the same predicate the claim uses and quote its status field; no row whose mutant status is
> `crashed-not-killed` may carry the word "distinguishes". Shown able to fail:
> `.ufo/waves/round-88/r1/R88MResidMut.md:131` routes RM6C2 on `mutant FAIL exit=1 (RecursionError)` while `:38`
> states the rule and `quality/counters/c2-r88-include-containment.py:225` assigns `crashed-not-killed`.
> (lesson: lessons/round-89.md#mistakes M89-1)

**M89-2 — the round-88 tokenizer kept a backslash inside quotes before any character other than `"` and `\`, unlike `parse_criteria`'s `QUOTE_ESCAPE` state.**
Class: model-drift — a re-implementation narrowed an upstream state to two characters.
Evidence: `tools/mado-mako.py` at `7d3074865a9f5acfa0f1c9c66b460e73d4031331:222` reads
`if char == "\\" and i + 1 < len(body) and body[i + 1] in ('"', "\\"):`, and a backslash before any other
character falls through to `:229` `word.append(char)`, keeping it. Upstream `criteria.c:186-188` sends **every**
backslash inside quotes to `MAKO_PARSE_STATE_QUOTE_ESCAPE`, and `:177-182` appends the next character and clears
the escape bit; `include/enum.h:7-11` gives `QUOTE_ESCAPE = 3 = QUOTE | ESCAPE`, so the clear returns to `QUOTE`.
The same pass also shows the separator rule: round 88 split on `char.isspace()` (`:242`), upstream splits on
`case ' '` only (`criteria.c:207-212`), so a tab inside a token ends the token in the lane's model and stays in it
upstream. Measured against a verbatim replica of the state machine: `summary="a\.b"` yields `summary=a.b` upstream
and `('summary', 'a\.b')` from the round-88 `tokenize`; `body~="\d+"` yields `body~=d+` upstream and
`('body~', '\d+')`; `app-name=a<TAB>b` yields one token upstream and two (`('app-name','a'), ('b', None)`) from
round 88. Latent since round 88 in exact `summary=`/`body=` values, and made visible by round 89's regex fields:
on the scratch fixture `[summary="a\.b"]`, the round-88 tool at `7d30748` applies the section to a notification
summary that literally contains a backslash and not to `a.b`, which is the opposite of what the tokenizer-fed
exact compare does upstream.
Captured-by: **no round-88 case** — `c16-backslash-escaped-space` is the only backslash case in
`.ufo/waves/round-88/controls/mako-cases-r88.json` and it is outside quotes (`[app-name=Google\ Chrome]`), so no
case carried a quoted backslash. Round 89's C1 build caught it when the same tokenizer had to feed `regcomp`: the
candidate's `tokenize` (`build/mado-mako.c1.py:276-288`) escapes any character inside quotes and splits on `" "`
only (`:299`), and the C1 case set now pins it with `r14-quoted-backslash-escapes-dot`,
`r15-quoted-double-backslash` and `r16-tab-inside-token`.
Fix: the candidate tokenizer matches the state-machine replica on eight probe inputs (quoted single backslash,
quoted double backslash, escaped quote, bare quote, outside-quote backslash, tab, trailing backslash, unterminated
quote); QUALITY criterion 149 requires the model to be checked against the upstream state machine's own states:
> **149. A model of an upstream parser is checked against the upstream state machine's own states, one probe per
> state, and the probe list is frozen with the model.** A re-implementation of a tokenizer or scanner names the
> upstream file and line range of each state it copies and carries one input that enters that state: for mako's
> `parse_criteria` at minimum the quoted state with a backslash before a character other than the quote or a
> backslash, and the normal state with a tab inside a token. Check: compile a replica of the upstream state machine
> from the pinned source lines and require the model's token output to equal the replica's on every probe; a probe
> whose escaped character is only `"` or `\` does not enter the rule being copied. Shown able to fail:
> `tools/mado-mako.py` at `7d3074865a9f5acfa0f1c9c66b460e73d4031331:222` keeps `\` before `.` inside quotes
> (`('summary', 'a\.b')` where `criteria.c:177-182` yields `a.b`) and splits on any whitespace at `:242` where
> `criteria.c:207` splits on a space only. (lesson: lessons/round-89.md#mistakes M89-2)

**M89-3 — the L1's first declaration draft left the after-state symbolic and rested the sourced claim on a row opened by round 88.**
Class: claim-sizing — a target that a later append could redefine, and a §2b.4 duty met by an old row.
Evidence: the pre-wave draft of `.ufo/waves/round-89/claims-declaration-r89.md` (wave input, read by every w1 seat)
declared "correct = N" while saying blind cases would be "appended after review", and named no SOURCES row for C1
beyond S494, whose `opened` is round 88's (`corpus/SOURCES.md` S494 row). R89MCritic F5 and F10
(`.ufo/waves/round-89/w1/R89MCritic.md` §2 and §5) caught both.
Captured-by: the w1 critic seat, before the freeze — the round prompt §9 ("one concrete value") and §2b.4 already state
the rule; nothing lane-owned checks a declaration for a symbolic N.
Fix: the frozen declaration states `correct=141 of cases=141`, `killed=37 of mutants=37` and the case-file sha256, and
C1's entry cites S496–S500, opened this round (below). No new criterion: QUALITY 118 and 147 already bind the exact
argv and pins; this lesson records that the draft missed them before a seat read it.

**M89-4 — the records commit again cited receipts it did not contain (a repeat of round 88's R4).**
Class: commit-ordering — a receipt path written into SCORECARD/lesson before the receipt is committed.
Evidence: records commit `51bf076fd970106da854e11873b886528c3cffaf` cites `receipts/harm-final-r89.txt` (SCORECARD harm row) and
`receipts/census-end-r89.txt` (lesson §Census), both produced after that commit (`.ufo/waves/round-89/r1/R89MResidCritic.md` F1–F3);
round 88's spot-check routed the same defect as R4.
Captured-by: the r1 critic seat only — R4 was routed as prose, never turned into a check.
Fix: both receipts land in the round's final commit; the report cites only receipts present at the final hash. A pre-report
check (`git ls-tree -r <final> --name-only` contains every `receipts/` path the records cite) is proposed for round 90; it is
not claimed here because it has not yet been shown able to fail on committed bytes.

## Wave findings routed (instruments frozen or named as limits)

| finding | seat | severity | disposition |
|---|---|---|---|
| earlier invalid `summary~` occurrence accepted (`[summary~=a(b summary~=x]`) | R89MReviewC1 F1 | medium | fixed before the freeze (every occurrence compiled in order), r32, M37, selftest check |
| outside-quote escape keeping its backslash not pinned | R89MReviewC1 M33 | low | M33 + r31 |
| escaped `=` and a standalone `""` token refused, upstream accepts/ignores | R89MReviewC1 F2/F3 | low | named limits (pre-existing at base, outside the claimed rules) |
| REG_NEWLINE, end-of-input escapes unpinned | R89MMutTester N04/N07/N14 | medium | M34–M36 + n04 ×2, n07 (b40 covers N14) |
| refusal message text not observable (N09); free-before-use crash-only (N10) | R89MMutTester | low | named limits |
| C2 axis: instrument depth, not operability | R89MCritic F2 | high | C2 reworded: the surface is a new runnable survivor gate; the axis ruling stays with the closure |
| symbolic N; "two criteria fields"; count command; label provenance; freeze sequencing; named limits; harm watch | R89MCritic F4–F11 | medium | all applied before the freeze (declaration `## Draft revisions` 5) |
| RM6C2 crash-only | R89MReviewC2 §3 | — | confirmed; four counterexample attempts failed |
| counter gaming by a candidate that detects its own role (filename / generation dir) | R89MExecForgery (`w1/forgeries/counter-*.py`) | low | named limit: the counters trust that the measured tool does not inspect its own path |
| tool selftest already kills RM7C1, RM3C2, RM4C2 | L1 (pre-freeze control) | — | stated as C2's second "before" (3/7), `receipts/c2-selftest-control-r89.txt` |
| residual r1: survivors RS01 (body~ earlier-invalid), RS05 (quoted bare token), RS12 (group-index accepted) | R89MResidMut §7 | medium | routed to round 90 as cases; RS02 crash-only, RS04/RS09 text-only, RS07/RS08/RS11/RS15 argued equivalent |
| residual r1: receipts cited before commit; blind set 45 not 44; host-refusal sentence; locators | R89MResidCritic F1–F8 | medium | corrected in the final commit (records, errata) |

## Gate

### Registry rows added (opened 2026-11-06 by R89MScoutSources; re-opened by the L1 the same day)

| id | locator | access | located quote (≤25 words) | line |
|---|---|---|---|---|
| S496 | file:///usr/share/man/man3/regex.3.gz (sha256 f79f05fd7ecd85fb292110e53d3709e956fddefbcce8f0e156c88ca0624be6ff) | 2026-11-06 | "Use POSIX Extended Regular Expression syntax when interpreting regex. If not set, POSIX Basic Regular Expression syntax is used." | decompressed 77-84 |
| S497 | file:///usr/share/man/man7/regex.7.gz (sha256 7d3f3e609b015ffa8906c3d06c4f79b8f5f93495b87471ca776b133e1de94373) | 2026-11-06 | "as defined in POSIX.2, come in two forms: modern REs (roughly those of egrep(1); POSIX.2 calls these \"extended\" REs)" | decompressed 34-37 |
| S498 | file:///usr/share/man/man3/setlocale.3.gz (sha256 253d8b37dc72ff3fbe3e34c3968e3268d88ec1a3833cd5606790450709f56111) | 2026-11-06 | "On startup of the main program, the portable \"C\" locale is selected as default." | decompressed 135-137 |
| S499 | file:///usr/include/regex.h (sha256 ae656ea6032f59d670c8c1055e1eebcb93ddbc482fd26b333ed529d6a4784b97) | 2026-11-06 | "#define REG_EXTENDED 1" … "#define REG_NOSUB (1 << 3)" | 310, 323 |
| S500 | https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0 (sha256 72d11d3fca20a3dfbca0107ff875eace479751be0cf2ddd1dd5bafa131ac7282) | 2026-11-06 | criteria.c: "if (regcomp(&criteria->summary_pattern, value, REG_EXTENDED \| REG_NOSUB)) {" — and `grep -rn setlocale` over the tree prints nothing | criteria.c 333-334 |

Re-open commands (L1, 2026-11-06): `zcat <page> | nl -ba | sed -n <lines>p`, `nl -ba /usr/include/regex.h`,
`sha256sum` of each container, `curl -fsSL <tarball> | sha256sum` → the digests above.

Considered, not appended (no admitted entry cites them): the POSIX Base Specifications chapter 9 and `regcomp()` pages
(R89MScoutSources draft ids S499/S500 — not the admitted rows that now carry those ids) — the entry rests the ERE/flag semantics on the host's own man pages and header,
which are the bytes this host's libc implements; flip: an entry that needs the normative POSIX text.

### Registry rows touched (old → new)

- S493 `used-by`: `corpus/knowledge/mako-criteria-resolution-r87.md,corpus/lessons/round-87.md` →
  `…,corpus/knowledge/mako-regex-criteria-r89.md` (the entry cites mako(5) L447-457).
- S494 `used-by`: `corpus/knowledge/mako-fields-containment-r88.md,corpus/lessons/round-88.md` →
  `…,corpus/knowledge/mako-regex-criteria-r89.md` (the entry cites criteria.c 46-59, 162-262, 332-351, 542-550).

### Candidates considered (round 89)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mako-regex-criteria-r89.md` (regex fields, C locale, tokenizer, host sections) | **admit** | every rule cites S494/S496–S500 at a line; the comparison table is measured on this host; the host replay decides 9/9 criteria sections (base 4/9) | a source line that contradicts a stated rule |
| modelling the two fields with Python `re` | **reject** | the python-re control scores 127/141 on the frozen set; the fuzz seat measured 404/3200 Python disagreements against the oracle | a `re` configuration that reproduces every oracle verdict |
| calling `regcomp`/`regexec` from Python without pinning the locale | **reject** | M24 (inherited locale) is killed by r08, r25, b42 | a measured host where the Python process starts in the C locale |
| `summary~` as an anchored literal match | **reject** | M25 (anchored) is killed by r02, r28 | a case set where literal search and ERE agree on every row |
| assimilating a `merge/mado/` theme | **reject** (`Assimilation: none`) | R89MConnector §2: no regex/notification-criteria theme in the package | a staged entry on mako criteria |

### Spot-check

Pending: the non-author closure is the operator-dispatched verifier (LEARNING.md).

### Census

- Start: `receipts/census-start-r89.txt` — `mado ok`, rc 0, 55 W04 warnings; 430 rows by `grep -c '^| S[0-9]' corpus/SOURCES.md` at the base (the receipt prints no row count).
- End: `receipts/census-end-r89.txt` — `mado ok`, rc 0, 55 W04 warnings (same as start; the census prints no row count); 435 rows by the same grep at the records revision.

## Considerthese

`considerthese/2026-11-06.md` proposal 1 — "Carry a survivor ledger across quiet days … tracking named open mutants …
and reporting the first later commit that kills one" — is what C2 builds: `quality/counters/c2-r89-survivor-kills.py`
prints, per routed round-88 survivor, killed/survived/crashed and whether the round-88 sets alone kill it; the first
commit that kills seven of them is the freeze `d8736135`. Proposal 3 (read-only live check of `mado-mako.py` against
João's real theme files) is acted on inside the credential-material rule: R89MExecHostDiff replayed the mako chain
only. Still open: r86/r85 survivors named in the reflection's table are not in this ledger.

## Domain share

New or changed artifacts: one knowledge entry (desktop-facing), one tool change (`tools/mado-mako.py`, desktop-facing),
two counters (lane-internal). Desktop-facing: 2 of 4.
