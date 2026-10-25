# Seat RevC2Counter-2 — attack on counter c2-r40-forms-entry.py (round 40, w1)

Target: `quality/counters/c2-r40-forms-entry.py` (PRED-C2-r40-v1, clauses a–h) at freeze
`5e7e88525cc539563de7746361b2650802e81809`. Worktree counter AND controls harness verified
byte-equal to the freeze commit (`git show 5e7e885…:quality/counters/c2-r40-forms-entry.py | cmp`
and same for `.ufo/waves/round-40/ctl/run-c2-controls.py` → both `COUNTER-FROZEN-MATCH` /
`CTL-FROZEN-MATCH`). The 20 shipped mutants are N01–N20; none of my mutants duplicates one.

## Method

Harness: `.ufo/waves/round-40/w1/RevC2Counter/mutants-c2-x.py` (in my seat dir). It imports the
frozen controls module and reuses its `good()`/`after()`/`row()`/`sha()`/`score()` unchanged, so
every fixture repo is `mktemp -d` + `git init -q`, toplevel verified equal to the temp dir before
the first commit, throwaway identity passed with `-c`, GIT_* stripped, and the counter runs via
`python3 -I … --repo D --rev A --base B` — the same machinery the shipped controls use.
Reproduce: `python3 -I .ufo/waves/round-40/w1/RevC2Counter/mutants-c2-x.py`.

Baseline sanity: the unmutated admitted state scores `admitted=1/1 verdict=TARGET_MET rc=0`
(mirrors control P; proves my fixture builder is byte-faithful).

## Result: 15 new mutants, 6 pass wrongly (admitted=1/1)

| mutant | what it changes | verdict | clauses failing |
|---|---|---|---|
| X01-sha-not-own-line | tool sha not on a line of its own in the own-work receipt | **PASS (wrong)** | none — all 1 |
| X03-counts-in-prose-line | forms/labels embedded mid-sentence, no standalone lines in entry | **PASS (wrong)** | none — all 1 |
| X05-usedby-longer-path | a cited row's used-by is `<entry>.draft-copy.md` (a different file) | **PASS (wrong)** | none — all 1 |
| X07-index-row-in-fence | the only README index row sits inside a ``` fence | **PASS (wrong)** | none — all 1 |
| X11-gate-lines-indented | every GATE line indented two spaces | **PASS (wrong)** | none — all 1 |
| X13-dual-gate-second-valid | stale GATE S303 line (round-39 path, zero sha) precedes the valid one | **PASS (wrong)** | none — all 1 |
| X02-receipt-spacing-differs | receipt count lines with doubled internal spacing | FAIL (correct) | h:0 |
| X04-two-own-work-rows | S301 kind also own-work | FAIL (correct) | h:0 |
| X06-quote-two-words | gate quote of 2 words (floor is 3) | FAIL (correct) | d:0 g:0 |
| X08-location-collides-held | new row's location equals the HELD row's last token | FAIL (correct) | e:0 |
| X09-quote-only-in-script | quote present only inside a `<script>` block | FAIL (correct) | d:0 g:0 |
| X10-recheck-on-date | `recheck: on-2026-10-25` (digits after `on-`) | FAIL (correct) | b:0 |
| X12-second-index-row-in-fence | legit index row + fenced duplicate | FAIL (correct) | f:0 |
| X14-new-id-opened-stale | new id's opened = 2026-10-24 | FAIL (correct) | c:0 |
| X15-receipt-crlf | own-work receipt with CRLF endings | FAIL (correct) | h:0 |

Scored run summary line: `REV-X: mutants=15 expectations-met=15/15` (my expectations, not the
counter's).

## Findings by severity

**F1 (medium) — clause c used-by is a substring check, so "used-by naming the entry" accepts rows
that point at a different file.** `c2-r40-forms-entry.py:147` (`good = cells[7] == "mined" and
entry in cells[10]`). Mutant X05 sets S301's used-by cell to
`corpus/knowledge/hyprctl-getoption-native-forms-r40.md.draft-copy.md`; `entry in cells[10]` holds
and the fixture is admitted 1/1. A row never actually used by the entry passes; even the docstring
wording ("used-by naming the entry") is over-claims relative to the code.

**F2 (medium) — clause h's "the entry text carries both lines verbatim" is substring containment in
the raw entry, not line presence.** `c2-r40-forms-entry.py:223`
(`and fm.group(0) in text and lm.group(0) in text`). Mutant X03 replaces the two standalone count
lines with one prose sentence ("The census reported forms int=44 … live-default=0.") and is
admitted 1/1. The receipt side enforces standalone lines (`^…$` with re.M, lines 210–217); the
entry side does not — an asymmetric implementation of one stated contract.

**F3 (medium-low) — clause f index counting is fence-blind, in both directions.**
`c2-r40-forms-entry.py:226-227` matches `^\| \`knowledge/<name>\`` over `readme.splitlines()`.
X07: an index row that exists ONLY inside a code fence counts as the index row → admitted 1/1.
X12: a legitimate README that additionally quotes its own row inside a fenced block is rejected
(f:0 → 0/1). The check cannot distinguish a real index row from documentation that mentions one.

**F4 (low-medium) — clause h's tool-sha binding is an unanchored substring check in the receipt.**
`c2-r40-forms-entry.py:221` (`hashlib.sha256(tool).hexdigest() in rtext`). Mutant X01 deletes the
standalone `tool sha256 …` line and appends the sha mid-line inside the census sentence; admitted
1/1. The byte binding survives, but the format contract is uneven: count lines are line-anchored,
the sha is not.

**F5 (low) — clause d tolerates arbitrary leading whitespace on GATE lines.**
`c2-r40-forms-entry.py:163` (`GATE_RE.match(line.strip())`). Registry rows have an explicit 0–3
space allowance; the docstring's gate line (`GATE <id> …`) has none, yet indented gate lines are
accepted (X11 admitted 1/1). Tolerance, arguably benign, but undocumented.

**F6 (low) — clause d accepts any number of GATE lines per id, first passing one wins.**
`c2-r40-forms-entry.py:163-178`: gates accumulate per id (`setdefault … append`, line 165); the
loop `for path, digest, quote in gates.get(i, [])` (line 171) skips a receipt outside `fetch/` or
with a wrong sha and binds on the first line that passes. X13 puts a stale GATE S303 (round-39
path, all-zero sha) ahead of the valid line → admitted 1/1. Docstring says "a line", so this is
laxity rather than a clear violation — but gate multiplicity/staleness is invisible to the counter.

## Residual risk

- Findings are laxities of the counter's clause checks, demonstrated on synthetic fixtures; whether
  the real delivered entry/registry/receipt bytes hit any of these shapes is L1/integrator scope.
- The declared residual stands untouched: a fabricated self-consistent set passes (control P).
- X02/X15 show the receipt-side count regexes are brittle in the opposite direction (doubled
  spacing or CRLF endings in a genuine receipt → false TARGET_MISSED) — a robustness note for
  whoever authors the real S30x receipt, not a wrong pass.
- I did not rerun the shipped `run-c2-controls.py` itself (its 21-control receipt is registered at
  the freeze); my run is an independent fixture family on the same counter.

## Verification gaps / notes

- No `lsp` device is mounted in this session; all checks are text/byte-level on files verified
  byte-equal to the freeze commit (recorded above). Nothing here should be read as semantic proof
  beyond the cited counter lines.
- No tool installs (python3 + git only; pacman untouched per host pause).
- No lane writes outside my seat dir (`w1/RevC2Counter/mutants-c2-x.py`, this report); fixture
  repos lived in mktemp dirs and were removed by the harness's `finally`.
