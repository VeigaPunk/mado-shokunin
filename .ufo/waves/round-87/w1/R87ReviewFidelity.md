# R87ReviewFidelity — attack on the C2 counter (c2-r87-control-fidelity.py) and the figure file (r86-figures-r87.json)

Reviewed bytes: `quality/counters/c2-r87-control-fidelity.py` (402 lines, sha256
`e4654d9de1dc14a49576b0a8df2e57ad43ca98589735e725179c421cafdbed60`) and
`.ufo/waves/round-87/controls/r86-figures-r87.json` (sha256
`da21797b07e6ae09f4e78f49f4dcefceee17164c8af148c8ba7676bd125fe092`), both landed on the clean lane
worktree at base `e4875ba5619053cc3f91bb2f4d819e189df4088c` (HEAD = base, `git status --porcelain`
showed only the wave's untracked files — no inherited defect from a sibling seat pollutes this
review). The r85 counter blob pulled from base e4875ba via `git archive` was staged at scratch
`$SCR/git/remote85` and has sha256
`b4bde359f66804cf9b982e40bbdf8d4bc6c9baa283378f9f1448b3aff82b111c` — that is the exact byte set
the counter runs.

## Check 1 — F1 re-derivation reads the held r85 counter's case_correct and the border-size-int witness from the r86 controls at base e4875ba

Counter code pins: `R85_COUNTER = "quality/counters/c2-r85-status-classes.py"`,
`R86_CASES = ".ufo/waves/round-86/controls/c2-cases-r86.json"`, `HELD_CASE = "border-size-int"`
(counter lines 30, 31, 38). `derive_held_rule` (lines 146–164) extracts both files from `REV` via
`git show`, imports the r85 counter module, selects the named case, and scores
`module.case_correct(named[0], 0, named[0]["frozen"])`.

Confirmed against the r85 counter at base: `case_correct` is defined at
`c2-r85-status-classes.py:509`; the frozen witness `border-size-int` is the last case in
`.ufo/waves/round-86/controls/c2-cases-r86.json` (lines 1579–1606), with `"kind": "regex"`,
`"value": "[0-9]+"`, `"anchor": "line"`, `"frozen": "0"`.

The r85 rule's regex/anchor chase: `case_correct → special_matches` (line 505) delegates non-refusal
kinds to `matches` (line 369). For `kind == "regex"` with `anchor == "line"` `matches` calls
`line_anchored(value, text)` (lines 380–382), which returns True only if the pattern matches one
complete output line (lines 359–366). The frozen `border-size-int` witness scores 1/1
(`case_correct(border-size-int, 0, "0") == True`).

The derive does not leave it to code reading: instrumented call `c2.derive_held_rule(repo, BASE, work)`
prints `1/1` for this witness.

The live producer was cross-checked separately: `hyprctl getoption general:border_size -j | jq -r .int`
returns rc=0 with bare `0\n` on this host — `re.fullmatch(r"[0-9]+", "0")` matches — and is a
producer sample never frozen (`c2-cases-r86.json` cases imply at least the committed 0/extra
negatives, never frozen).

Two scoring paths show why the held-rule figure matters at all: (a) the r86 model
`held_case_correct` (`c2-r86-clause-observations.py:574`) searches the WHOLE output — its selftest
pins this at line 736-737 with `ok(not held_case_correct(anchor_case, 0, "0"), "the held rule scores
the anchored witness 0: it searches the whole text")` — any word between the witness digits and the
line's end defeats it; (b) the held r85 rule's `case_correct` (`c2-r85-status-classes.py:509`)
enforces a whole-line match via `line_anchored` (lines 380–382) and accepts the single-line
witness. The r86 record's stated `0/1` came from path (a); the C2 counter re-derives with path (b)
and gets `1/1`. The declaration's figure reconciliation rests on exactly this asymmetry, and the
derivation code reads it faithfully.

Line numbers that decide the verdict: counter lines 30/31/38 (pins), 146–164 (derive_held_rule),
`c2-r85-status-classes.py` lines 509/515/517/521 (case_correct/samples/negatives gate),
lines 380–382 (the anchor==line branch), lines 359–366 (line_anchored).

## Check 2 — six adversarial correction blocks (scratch copies in $HYAKU_SCRATCH)

Run command: instrumented counter module (`spec.loader.exec_module` over the lane file), then
`c2.evaluate(repo, rev, c2.FIGURES_PATH, root, None, c2.stub_flood)` with `repo` produced by the
counter's own `c2.fixture(root, label, corpus_extra, score_extra, f2_text, extra)` — fixture
construction goes through the counter's `make_repo`, which asserts
`git rev-parse --show-toplevel == fixture dir` before any commit and commits with the throwaway
identity `mado-selftest <selftest@invalid>`. F2 is stubbed (`stub_flood`) so check 2 isolates the
reconciliation logic; F2's real reproduction is check 3. All runs under explicit
`$HYAKU_SCRATCH=/fast/scratch/hyaku/mado-r87/R87ReviewFidelity` with TMPDIR redirected.

Declarative boundary derived from the module's own `correction_blocks` (counter lines 115–136): a
block starts at any heading matching `"Correction (round 87"` and runs to the next heading of the
same or higher level; a deeper heading stays inside the block. This puts the heading-level question
(was the correction placed at the right level?) OUTSIDE the counter's scope by design — the counter
never checks a heading level; it accepts a level-4 heading appended under a level-1 section. The
declaration itself does not name a heading level: "a `Correction (round 87)` heading in the same
file, naming the figure id and its re-derived value" — so E below is a correct append, not a
forgery the counter failed to reject.

| # | adversarial block | counter exit | reconciled | verdict |
|---|---|---|---|---|
| A | bare heading `## Correction (round 87)` with no id/value | 1 (TARGET_MISSED) | 1 (F2-stub only) | rejects, as the declaration demands |
| B | heading with a correction naming only the id (`## Correction (round 87): F1_held_rule_witness_r86` with `value left unstated.`) | 1 | 1 | rejects, value token absent |
| C | correction with the wrong value (`still 0/1 per the old model.`) | 1 | 1 | rejects (the declarative `0/1` is not my `re-derived 1/1`) |
| D | correction in another file (`notes/other.md`) with the fully valid block | 1 | 1 | rejects — no reconciliation from a third file, only the two in `CORRECTION_FILES` |
| E | correction whose heading is level 4 `#### Correction (round 87): F1…` with the correct value | 0 (TARGET_MET) | **2** | ACCEPTED — heading-level question is outside the counter's contract by design; the plain reading of the declaration ("a Correction (round 87) heading in the same file, naming the figure id and its re-derived value") does not require a heading level |
| F | correction placed after a higher-level heading (`## Later`) | 1 | 1 | rejects — content outside the block is unbound |

Additional probes in the same run keep the boundary honest:
- same-level heading AFTER the value (`## Correction (round 87): F1…\n## Later\n\nF1… re-derived
  1/1`) → **rejects** (exit 1): the id/value pair must be in the SAME block; text after the
  terminating heading is out of scope (counter line 127–135);
- a deeper `### Later` subheading inside the block with the value under it → accepted, and a
  `### sub` subsection's value with an id-bearing top-level `Correction (round 87)` heading →
  accepted: the boundary is a same/higher-level event only;
- token boundary: `token_in("1/1", "1/1x")` False, `token_in("1/1", "x1/1")` False,
  `token_in("1/1", "1/1.")` True — the period boundary case (trailing punctuation) is accepted
  because `(?![0-9A-Za-z_])` excludes non-word chars only; the substring search is thus
  punctuation-bound, not whitespace-bound.

`reconciles` (counter lines 138–144) accepts a block only when BOTH `token_in(fig_id, block)` and
`token_in(value, block)` are True. The figure id token (`F1_held_rule_witness_r86`) matches anywhere
in the block; the value token (`1/1`) is punctuation-bound by the same token regex. In every check-2
run F2's derivation is the counter's own `stub_flood` — a fixed string
`flooding 48/75; held 75/75` that equals the figure's `stated` (hence `reconciled=1` in the
table's rejects: F2 reproduces, F1 does not) — so the exit values isolate F1's reconciliation
from F2's. F2's own real reproduction is check 3.

## Check 3 — F2 reproduces (the r86 receipt `final-c1-r86.txt`)

The counter's `derive_flood` (counter lines 165–203) parses the receipt's own bytes with three
regexes and re-runs the r86 derivation from them:
- `^MADO_R86_REFUSALS: cases=\d+ .*?\brev=([0-9a-f]{40})\b` → line 129 of
  `.ufo/waves/round-86/receipts/final-c1-r86.txt` carries `rev=3afdb7136904b70b0a01ac31963b6e9b14320f1f`
  and `flooding=48/75 held_flooding=75/75 verdict=TARGET_MET` — the derivation's input values
  are exactly the receipt's own words, not a re-answer key;
- `^MADO_R86_BASE: .*?\bbase_rev=([0-9a-f]{40})\b` → line 127 `base_rev=2b6dd76b65de4dfe701db87db13b7e448b3538ee`;
- `^MADO_R86_CONTROL: sha256=([0-9a-f]{64})\b` → line 128 `sha256=f6dd9cdef7daa2e6b51c95f27cf8ebe8509188
  c551ff18ed42a176a08d8620bf`;
- then: `git show <rev>:quality/counters/c1-r86-refusal-records.py` (blob
  893d903dd23489b993cec407302ec50e01256430 — the C1 counter is byte-present at the receipt rev),
  `git show <rev>:.ufo/waves/round-86/controls/c1-cases-r86.json` keyed against its sha256
  (`m_ctl.group(1)` == `sha256(c1_cases_bytes)` — an R2-style re-bind inside the C2 counter),
  `git show <rev>:.ufo/waves/round-85/controls/c1-cases-r85.json` (blob
  339aa9656b2b2415f558c2f46ee65a2422e1c83a), then runs the C1 derivation as the counter itself
  declares the r86 receipt in its own bytes. All three files exist at base e4875ba (`git ls-tree
  e4875ba5619053cc3f91bb2f4d819e189df4088c -- <each>` shows blobs).

The re-run itself ran 127.7 s in one session and printed the exact `MADO_FIGURE:` line
`id=F2_flood_r86 stated='flooding 48/75; held 75/75' rederived='flooding 48/75; held 75/75'
reproduced=yes reconciled=yes` — the C2 counter's F2 re-derivation is not a stub; it re-executes the
r86 C1 counter end-to-end against the receipt-referenced blobs and returns
`"flooding %s/%s; held %s/%s"` from the re-run's own output (counter lines 196–200).

## Check 4 — the R2 pins (sha256 printing and the --expect-figures-sha256 path)

`evaluate` prints `figures_sha256=...` and `counter_sha256=...` at the end of the summary line
(counter lines 232–238, the `MADO_FIGURES: %s rev=%s n=%d ...` f-string). Both sha values are
bound to the real bytes: `counter_sha256 = sha256(open(os.path.abspath(__file__), "rb").read())`
(counter line 223) and `fsha = sha256(raw)` where `raw = git_bytes(repo, full, figures_path)`
(counter lines 206–207). Both were observed printed in the check-2 probe runs:
`counter_sha256=e4654d9de1dc14a49576b0a8df2e57ad43ca98589735e725179c421cafdbed60`,
`figures_sha256=da21797b07e6ae09f4e78f49f4dcefceee17164c8af148c8ba7676bd125fe092`.

The `--expect-figures-sha256` wrong-pin path: at counter line 208 the pin is compared
case-insensitively (`expect_sha.lower() != fsha`) and a mismatch raises `Setup`, which `main` maps
to exit 2 (counter lines 395–397). Verified twice in a scratch fixture: with the real figures bytes
committed at a scratch rev, `evaluate(..., expect_sha="0"*64, flood=stub_flood)` raised exactly
`Setup("figure file sha256 da21797b... differs from expected 000000...") → exit 2`, and
`evaluate(..., expect_sha=actual_sha, flood=stub_flood)` passed the pin gate and gave a verdict
(exit 1 for the F1 reason). The pin gate is a real gate, not a stub.

## Findings and defects found

### Defect R87RF-D1 (HIGH): the F2 `stated_at` text `flooding 48/75 vs held 75/75` does NOT hold in base `SCORECARD.md` bytes — it is too narrow a substring predicate

`grep -c "48/75 vs held 75/75"` over the base bytes of `SCORECARD.md` prints 0, and the figure file
demands exactly this substring from `SCORECARD.md` (`stated_at` for `F2_flood_r86`). The base bytes
carry the numbers only in two places, neither of which is that substring:
- ACCORDING-TO-DATE prose under `### Round86 final committed-revision measurements`: line 5062 ends
  `…, tool selftest 152/152, flooding` and line 5063 starts `48/75 vs held 75/75, TARGET_MET, …` —
  a line wrap splits the value from its label across the physical line boundary;
- the round-86 claim table row (line 5033): `the flood **48/75** (gap 27/75)` and
  `the honest tool and the all-cause flood **both 75/75**` — table-cell phrasing whose phrase
  `48/75` and `75/75` sit in bold markers in different sentences, no contiguous match.

The counter's `evaluate` therefore dies at its setup stage with `stated text absent from SCORECARD.md
at e4875ba (figure F2_flood_r86): 'flooding 48/75 vs held 75/75'` on every run against the frozen
base, including the declaration's own "Before (base)" run — the C2 executor's counter scores 0
(exit 2) never reaching the declared 5.0 TARGET_MISSED verdict.

Reproduction (all in scratch, base read with `git show`):
```
$ git show e4875ba…:SCORECARD.md | grep -c "48/75 vs held 75/75"
0
$ git show e4875ba…:SCORECARD.md | sed -n '5062p' | tail -c 30
…, tool selftest 152/152, flooding
$ git show e4875ba…:SCORECARD.md | sed -n '5063p' | head -c 30
48/75 vs held 75/75, TARGET_MET,…
$ python3 -I … .ufo/waves/round-87/controls/r86-figures-r87.json --stated_at F2_flood_r86
  … expects `"text": "flooding 48/75 vs held 75/75"` at `"path": "SCORECARD.md"`.
$ python3 -I quality/counters/c2-r87-control-fidelity.py --repo . --rev e4875ba…
MADO_FIGURES: ERROR (stage=setup stated text absent from SCORECARD.md at e4875ba … 'flooding 48/75 vs held 75/75')
```
The last line is observed (exit 2), exactly as predicted by the counter's code path
(counter lines 212–218: `if loc["text"] not in text: raise Setup(...)`).

Attack seat does not edit or repair the lane bytes. Formally: this is the `stated_at` DESIGN defect
HIGH (the predicate's substring window is too narrow to be held by the same physical line wrapping
the corpus file uses). Routed as the C2 executor's own defect to fix before wave close: re-derive the
stated text as a substring that the base bytes actually hold. Cleanest options within its own item:
bind the figure id to the wrapped lines as ONE substring that spans the wrap —
`"text": "flooding\n48/75 vs held 75/75"` (a two-line substring that IS present verbatim at
base) — or switch the `F2_flood_r86` `stated_at` path to the r86 receipt bytes
(`.ufo/waves/round-86/receipts/final-c1-r86.txt:129`, which carries the contiguous
`flooding=48/75 held_flooding=75/75` on one line) and re-derive the figure file sha so the
`--expect-figures-sha256` pin follows. Either adjustment keeps the figure id, the derivations and the
pin mechanism unchanged; only the `stated_at` byte target shifts to bytes that exist.

Severity: **HIGH** — the C2 counter at the frozen base cannot run at all; F2's stated text is
unreachable in scoring-stage bytes, and the "before" receipt `c2-base-r87.txt` that the declaration
demands ("Before (base): F1 unreconciled → 5.0 TARGET_MISSED") cannot be a `5.0` verdict because the
counter never reaches a scoring stage (0/2 figures with no target measurement, not 1/2).

### Defect R87RF-D2 (INFO, contrast with D1): F1's `stated_at` DOES hold in the corpus note bytes — same design, different luck

The figure file demands `"text": "held_rule_new_case=0/1"` at
`corpus/knowledge/refusal-records-clause-observations-r86.md`; `grep -n` finds the exact substring
on line 112 (inline code, same line, unwrapped). PASS. The stated_at design is fragile in the same
way D1 shows; here the wrap fell elsewhere and the substring holds. D1 is the only instance where
it bites today.

### Defect R87RF-D3 (INFO): the selftest lacks probes for deeper-heading values and token punctuation boundaries

The selftest covers a bare heading, wrong value, id-only heading, wrong figure id in the title, block
terminating at the next same-level heading, token-bounded value, and a Setup error stage
(15/15 pass, exit 0). The six adversarial classes the declaration demands are all present across
selftest + this review's check 2. Two of my probes (the `### Later` deeper-heading acceptance and the
`token_in('1/1', '1/1.')` comma-boundary pass) do not appear anywhere in the selftest, but both match
the counter's design intent. No action; recorded for the mutation-tester seat if it draws from this
defense surface.

## R2 pin reproduction: which bytes hash what

- figure file, working-tree sha256 `da21797b07e6ae09f4e78f49f4dcefceee17164c8af148c8ba7676bd125fe092`
  — the counter's correct-pin trail (`sha256sum <figures>` in this session gave the same hex). This
  hash is what a receipt typically wants to pin via `--expect-figures-sha256`; the C2 executor can
  update the pin after landing any figure-file mutation, and re-derive it from this line.
- counter file, working-tree sha256 `e4654d9de1dc14a49576b0a8df2e57ad43ca98589735e725179c421cafdbed60`
  — the counter printed this same value as `counter_sha256=` in every check-2 and check-4 output
  line. Self-consistent against its own `open(os.path.abspath(__file__), 'rb')` read at line 223.
- This report is an attack; the counter is NOT mutated here and the lane bytes stand as landed.

## Verification state

| check | command | exit | observed |
|---|---|---|---|
| C2 selftest (R2 gates) | `python3 -I quality/counters/c2-r87-control-fidelity.py --selftest --scratch-root $SCR/st` | 0 | `MADO_FIGURES_SELFTEST: 15/15` |
| C2 counting (check 1, probe run against the real lane) | `python3 -I quality/counters/c2-r87-control-fidelity.py --repo . --rev e4875ba… --figures .ufo/waves/round-87/controls/r86-figures-r87.json --scratch-root $SCR/inline-f1` | 2 | `MADO_FIGURES: ERROR (stage=setup stated text absent from SCORECARD.md …)` — this IS defect R87RF-D1's own error, reproduced from the counter's code path |
| F2 stated_at presence probe | `python3 -I` session with `c2.git_bytes(BASE, scorecard)` and `'48/75 vs held 75/75' in text` | — | False → R87RF-D1 proof (see reproduction block) |
| C2 counting (check 2, scratch fixtures) | instrumented `c2.evaluate(repo, rev, figs, root, None, stub_flood)` over 8 adversarial fixture repos under `$SCR` | 1 on the 6 rejects, 0 on the 2 accepts | verdict table above; exits and reconciled counts per row |
| F2 real derive (check 3) | `c2.derive_flood(repo, BASE, work)` full re-run in one session | 0 | `flooding 48/75; held 75/75` in 127.7 s |
| F1 derive (check 1) | `c2.derive_held_rule(repo, BASE, work)` | 0 | `1/1` |
| F1 live crosscheck | `hyprctl getoption general:border_size -j \| jq -r .int`, then `re.fullmatch("[0-9]+", out)` | 0 | rc 0, bare `0`, fullmatch True |
| R2 wrong pin | `… --expect-figures-sha256 0000…` on the scratch fixture rev | 2 | `MADO_FIGURES: ERROR (stage=setup figure file sha256 da21797b… differs from expected 0000…)` |
| R2 correct pin | `… --expect-figures-sha256 da21797b…` on the same scratch rev | 1 | passes the pin gate, continues to a verdict (F1 reason) |
| sha pins recorded | `sha256sum <counter> <figures>` | 0 | `e4654d9d…` / `da21797b…` per header |

No file was modified in the lane (write scope held; report file only). Scratch
`/fast/scratch/hyaku/mado-r87/R87ReviewFidelity` was removed on exit (`rm -rf` verified with `ls`
showing the path gone). No tool was installed or upgraded (RULES.md read; none needed). No mutating
git command was run anywhere (fixture creation went through the counter's own `run_git`/`make_repo`
with the top-level assertion; scratch copies only).

## Bottom line

- Check 1 (F1): PASS — the counter's `derive_held_rule` binds the held r85 `case_correct`
  (`c2-r85-status-classes.py:509` at base), the `border-size-int` witness (last row of
  `c2-cases-r86.json`, rc/frozen=`0`/`"0"`), and re-derives `1/1` (witness verified by direct
  instrumented call and by the live producer crosscheck). The line-level branch that decides it is
  `matches` line 380–382 → `line_anchored` 359–366.
- Check 2 (adversarial): PASS — all six reject probes rejected (bare heading, id-only,
  wrong value, other file, out-of-block placement, post-boundary value) and the two accepts
  behaved as designed (level-4 append under a level-1 section, and the good-correction sanity);
  the counter's block boundary is the next heading of the same or higher level with no heading
  level constraint of its own, so a level-4 append is a valid correction (E). The selftest has no
  score probe on trailing punctuation or deeper-heading values — recorded as D3 for the mutation
  seat.
- Check 3 (F2): PASS — the counter re-runs the r86 C1 derivation at `3afdb713` from the receipt's
  own bytes and reproduces `flooding 48/75; held 75/75` in 127.7 s.
- Check 4 (R2 pins): PASS — both sha256 values are printed on the `MADO_FIGURES` line and a
  mismatching `--expect-figures-sha256` pin raises `Setup` → exit 2.
- NEW DEFECT R87RF-D1 (HIGH, in reviewable bytes): the F2 figure's `stated_at` text
  `flooding 48/75 vs held 75/75` is not a substring of `SCORECARD.md` at base e4875ba (the
  `### Round86 final committed-revision measurements` sentence wraps after the word `flooding`
  at line 5062; `48/75 vs held 75/75` opens line 5063). Every run of the C2 counter at the frozen
  base exits 2 before any scoring — the wave's own C2 `Before (base)` run cannot produce the
  declared `5.0 TARGET_MISSED`. The fix belongs to the C2 executor: adjust the `stated_at` token to
  bytes the base actually holds, or point F2's `stated_at` at the r86 receipt line
  (`final-c1-r86.txt:129`, which has the same numbers contiguously as
  `flooding=48/75 held_flooding=75/75`), then re-derive the figure file sha and re-bind
  `--expect-figures-sha256`.
