# R89MMutTester — case-set gaps beyond M01–M32 (DRAFT probe)

Status: **DRAFT**. Nothing here is a measurement and no receipt was written under
`.ufo/waves/round-89/receipts/`. I ran the round-89 counter in-process (`m.score(...)`) over the
DRAFT case file and the DRAFT candidate only, exactly as the seat item permits.

Seat: mutation tester, round mado 89 / hyaku 15 w1. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

## 1. Inputs and hashes (read, not written)

| input | path | sha256 |
|---|---|---|
| candidate | `.ufo/waves/round-89/build/mado-mako.c1.py` | `2720922b1b9206549bf20248a20c5b70d7dc445ab2d1815112a2cb524fce229e` |
| case set | `.ufo/waves/round-89/controls/mako-cases-r89.json` (91 cases) | `d04e27fccd7b4ffffa820872706c394eb59b96a46e792e0bbb2f30cfb2980431` |
| counter | `quality/counters/c1-r89-mako-regex.py` | `de6dfd4f87901d0941836f5f09aa976d46ce5790255dd9619162125b4f2810b1` |
| base tool | `git show af998dcc41d48618ffe7afe0efc9354755a9244e:tools/mado-mako.py` | (read through `git show`, not written) |

Baseline (DRAFT, exit 0): candidate `correct=91/91`; controls `naive=22 globals=23 base=67
python-re=81`. Every kill below is therefore attributable to the mutation, not to a pre-existing
candidate failure.

## 2. Method

1. `S=$HYAKU_SCRATCH/mado-r89/R89MMutTester` (`HYAKU_SCRATCH=/fast/scratch/hyaku`), `mkdir -p`.
2. Imported the counter with `importlib.util.spec_from_file_location` (its own sha256 pins run at
   import); `cases = m.R88.load_cases(<round-89 case bytes>)`; candidate text from the build path;
   base text from `git -C <lane> show af998dcc…:tools/mado-mako.py`.
3. For each new mutant `Nxx`: asserted its `old` anchor occurs **exactly once** in the candidate
   (`cand.count(old) == 1`; a violation exits before any scoring), then
   `m.score(mutant_text, base_text, cases, [], S, 61, declared=None, range_check=False)`; the same
   call on the candidate gives the per-case verdicts (`case <id> ok|FAIL <reason>` lines).
4. Kill rule identical to the frozen machinery: a case kills only when the verdict differs **and**
   the mutant's reason there does not start with `CRASH_PREFIXES` (`timeout`, `exit=`, `bad-json`,
   …). Otherwise `crashed` (never a kill).
5. Per-case comparison is exact on the `(ok|FAIL, reason)` tuple, so a reason-only difference also
   counts as a difference (this matters for N09/N10).

Disclosed deviation from the literal call in the seat item: the counter's python-re control is a
forgery applied to the *measured* tool text, and five of my mutants (N01, N02, N03, N04, N11) mutate
bytes inside those forgery anchors. For those, and only those, I derived the forgery anchors from the
same mutation (`old.replace(mu.old, mu.new, 1)`) so the control stays well-formed; every derived
anchor was asserted to occur exactly once. The per-case mutant verdicts are unaffected (the control
score is not part of the kill rule).

## 3. Mutant table (15 new mutants, DRAFT)

Round-88/89 anchors M01–M32 were **not** re-scored; these are new and target the C1 surface:
`posix_ere_search` encoding/eflags, regcomp flags, the cannot-set-both check, validation-vs-mismatch
order, tokenizer end-of-input inside/outside quotes, the `REGEX_FIELDS` input lookup, the undecided
message, and free-before-use.

| id | change (short) | verdict | differing cases (candidate ok → mutant verdict) |
|---|---|---|---|
| N01-search-text-encoding | `posix_ere_search` encodes the value as latin-1 instead of UTF-8 | **killed** | `r08-c-locale-dot` (ok→FAIL mismatch anchor), `r24-utf8-literal` (ok→FAIL mismatch anchor) |
| N02-notbol-eflag | `regexec` eflags `0`→`REG_NOTBOL` (1) | **killed** | `r05-posix-digit-class` (ok→FAIL), `r29-ere-interval` (ok→FAIL) — both patterns start with `^` |
| N03-icase-added | `regcomp` flags gain `REG_ICASE` (2) | **killed** | `r06-backslash-d-is-literal-d` (ok→FAIL), `r27-case-sensitive` (ok→FAIL) |
| N04-newline-added | `regcomp` flags gain `REG_NEWLINE` (4) | **survived** | none (0/91 differ) |
| N05-both-check-body-only | cannot-set-both applies to `summary`/`summary~` only, so body+body~ is accepted | **killed** | `r18-body-and-pattern` (ok→FAIL) |
| N06-invalid-regex-multifield-nomatch | invalid regex refused only in a one-field section; beside another field it becomes a silent non-match | **killed** | `r22-invalid-with-other-mismatch` (ok→FAIL) |
| N07-dangling-quote-escape-yields-token | trailing `\` at end-of-input inside a quote ends the quoted run and yields the token | **survived** | none (0/91 differ) |
| N08-regex-input-lookup-by-field-key | `decide` looks up the input under `summary~` instead of `summary` | **killed** | 24 cases: `r01 r02 r03 r04 r05 r06 r07 r08 r09 r10 r13 r14 r15 r16 r20 r21 r23 r24 r25 r26 r27 r28 r29 r30` (all ok→FAIL; every regex case whose input is supplied) |
| N09-undecided-message-shortened | refusal message drops `; section not applied` | **survived** | none (0/91 differ) — detector-equivalent, see §5.3 |
| N10-free-immediately-after-compile | `regfree` right after `regcomp` (then the `finally` frees again) | **crashed** | 24 cases, all `FAIL exit=-11` (SIGSEGV) — crash, not a kill |
| N11-compile-pattern-encoding | `posix_ere_compile` encodes the pattern as latin-1 instead of UTF-8 | **killed** | `r24-utf8-literal` (ok→FAIL mismatch anchor) |
| N12-equals-always-splits | every `=` splits key/value, not only the first | **killed** | `c17-equal-sign-inside-value` (ok→FAIL) |
| N13-quoted-value-dropped | opening a quote no longer marks the token started, so a fully quoted value is dropped | **killed** | `r15-quoted-double-backslash` (ok→FAIL) |
| N14-dangling-backslash-outside-dropped | trailing `\` outside quotes is dropped instead of refusing the header | **survived** | none (0/91 differ) |
| N15-mismatch-loses-to-undecided | a decided mismatch no longer short-circuits when another field is undecided | **killed** | `c59-mismatch-beside-undecided-no-refusal` (ok→FAIL) |

Totals: **killed 11, survived 4, crashed 1**; no setup error in the scored runs.

## 4. Case-set gaps and proposed cases

Four survivors: N04, N07, N14 need new cases; N09 cannot be distinguished by the case language and
is argued equivalent. Each proposal below was verified with the *same* detector (candidate ok,
mutant differs, mutant reason not a crash) over `91 + 4 = 95` cases:

```
candidate correct: 95 / 95   (all four proposals ok on the candidate)
N04 → n04-reg-newline-dot-crosses-newline      cand ('ok','ok') mut ('FAIL','mismatch anchor')
N04 → n04-reg-newline-caret-after-newline      cand ('ok','ok') mut ('FAIL','mismatch anchor')
N07 → n07-dangling-quote-escape-refused        cand ('ok','ok') mut ('FAIL','missing-refusal')
N14 → n14-dangling-backslash-refused           cand ('ok','ok') mut ('FAIL','missing-refusal')
```

Why the current set misses each:

- **N04 (REG_NEWLINE).** No carried or r-case puts a newline in a `summary`/`body` operand, so
  neither REG_NEWLINE effect is exercised: `.`/`[^…]` not crossing newline, and `^`/`$` matching at
  line boundaries. Two cases pin the two effects separately.
- **N07 (end-of-input inside a quote).** `r14`/`r15` cover a backslash before a character inside
  quotes; nothing covers a backslash as the **last** character of the header. `c29` covers an
  unterminated quote *without* a dangling escape (`[app-name="alpha]`), and no case anywhere ends a
  header on a backslash (neither branch).
- **N14 (end-of-input outside a quote).** Same gap on the outside-quote branch: no case has a
  trailing `\` as the last header byte.
- **N10** is not a case gap: the defect is memory safety and manifests as SIGSEGV on the first regex
  case (`r01`), which the kill rule correctly refuses to count (same shape as round-88's RM6C2).
  It is moot after the `free-before-use` refactor is excluded by review; no case can separate it with
  a well-formed result.

### Proposed case-set additions (case-file JSON shape, `mako-cases-r89-v1`)

```json
[
 {"id": "n04-reg-newline-dot-crosses-newline", "config": ".config/mako/config",
  "home_files": {".config/mako/config": "anchor=top-right\n[body~=a.b]\nanchor=bottom-center\n"},
  "args": {"body": "a\nb"},
  "expect": {"effective": {"anchor": "bottom-center"}, "refusals": "none"},
  "pin": "no REG_NEWLINE: . matches a newline byte in the C locale", "oracle": "body~:match"},
 {"id": "n04-reg-newline-caret-after-newline", "config": ".config/mako/config",
  "home_files": {".config/mako/config": "anchor=top-right\n[body~=^b]\nanchor=bottom-center\n"},
  "args": {"body": "a\nb"},
  "expect": {"effective": {"anchor": "top-right"}, "refusals": "none"},
  "pin": "no REG_NEWLINE: ^ anchors at the start of the value only", "oracle": "body~:nomatch"},
 {"id": "n07-dangling-quote-escape-refused", "config": ".config/mako/config",
  "home_files": {".config/mako/config": "anchor=top-right\n[summary~=\"abc\\]\nanchor=bottom-center\n"},
  "args": {"summary": "abc"},
  "expect": {"effective": {"anchor": "top-right"}, "refusals": "present"},
  "pin": "parse_criteria: a backslash at end-of-input inside a quote is an unmatched quote", "oracle": "refused"},
 {"id": "n14-dangling-backslash-refused", "config": ".config/mako/config",
  "home_files": {".config/mako/config": "anchor=top-right\n[summary~=abc\\]\nanchor=bottom-center\n"},
  "args": {"summary": "abc"},
  "expect": {"effective": {"anchor": "top-right"}, "refusals": "present"},
  "pin": "parse_criteria: a trailing backslash outside quotes is refused, not dropped", "oracle": "refused"}
]
```

Case-file notes for integration (L1): the config strings above are the literal file bytes (in
`[summary~=abc\]` the backslash is the last byte of the header content, before the closing `]`; in
`[summary~="abc\]` it is the last byte inside the quote). The expected `effective` is a subset like
every other case; `refusals` is only the presence flag.

Caveat on the two refusal-oracle cases: the dangling-backslash refusals are the **tool's declared
stance** (source header `L497-508`, `tokenize` docstring), not a behaviour I re-derived from
`criteria.c`. Upstream `parse_criteria` with a trailing escape at end-of-buffer is not modelled by
these cases; the cases pin the candidate's stated rule and must be re-derived if the L1 narrows that
stance.

## 5. Survivor arguments

### 5.1 N04 — killed by new cases (above)
Equivalent on the current 91-case set (no newline in any regex operand), not equivalent in general.

### 5.2 N07 / N14 — killed by new cases (above)
Same shape: the 91-case set never ends a header on a backslash.

### 5.3 N09 — equivalent under the declared detector, NOT under raw output

Verified with one case (`[summary~=x]`, no `--summary`, so the section is undecided):

```
cand refusals = ["…/config:2: criteria needs --summary to decide the match; section not applied"]
mut  refusals = ["…/config:2: criteria needs --summary to decide the match"]
cand other stdout keys equal except refusals: True
mut  other stdout keys equal except refusals: True
```

`tool_verdict` checks only `refusals` **presence**, so both score `ok` — the case language has no way
to assert message text. Verdict: **detector-equivalent**, and the mutation is a real user-visible
wording change. If the L1 wants this covered, the case schema would need an expectation field for the
refusal text (out of scope here; I did not change the schema). Not a case gap of the current
predicate.

### 5.4 N10 — crashed, not a kill

`FAIL exit=-11` on all 24 regex cases (SIGSEGV from `regexec` on a freed `regex_t`/double
`regfree`). Reported per the frozen rule: a crash is not a kill, so the detector's coverage of
use-after-free is zero by construction. No terminating well-formed case can separate it.

## 6. Exact commands run and exit codes

All inside `S=/fast/scratch/hyaku/mado-r89/R89MMutTester`, `TMPDIR` pointed at `S`, absolute lane paths.

| command | exit |
|---|---|
| `python3 probe.py` (import counter, baseline candidate score) | 0 |
| `python3 run_mutants.py` (15 mutants, 6-thread pool) | 0 |
| `python3 verify.py` (95-case candidate + 3 survivors + N09 raw diff) | 0 |
| inline N09 message-diff driver | 0 |

Dead step: the **first** `run_mutants.py` run exited **1** with
`AttributeError: module 'c1_r89' has no attribute 'CRASH_PREFIXES'` (the constant lives on
`m.R88`); fixed to `m.R88.CRASH_PREFIXES` and re-run to exit 0. That first run wasted its 48 s of
scoring but produced no table.

Scratch: `S` held only the drivers, mutant JSON, proposed cases, and result JSON; the proposed cases
and the mutant table are embedded verbatim in this report, and `S` was removed on exit
(`rm -rf -- /fast/scratch/hyaku/mado-r89/R89MMutTester`). No installs, no pacman,
no git mutation (base tool read with read-only `git show`), no host config or credential reads.

## 7. Suggested L1 action

1. Add the four proposed cases to `.ufo/waves/round-89/controls/mako-cases-r89.json` (it stays inside
   `N_MIN..N_MAX`: 91 → 95) **or** record them as named follow-ups; the C1 mutant count stays 32, so
   the predicate is unchanged either way.
2. Optionally record N09 as a named detector limit (message text not observable) and N10 as
   crash-only (like RM6C2), so a later round does not re-discover them as surprises.
3. If the four cases are added, `m.score` over them must be re-run at the freeze revision — I have
   only run the DRAFT bytes.
