# R69RevC1 — adversarial review of claim C1 (calibration: paired-recipe hardening)

Verdict: **C1 predicate sound as bounded** — with conditions named in S1–S3/S5 that hold
only because the frozen counting command pins `--base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454`
(where the r68 harness exists and is byte-identical to the worktree, sha256 `25470bc4…`).
The currently integrated production counter (`2060da8d…`) is **not** sound outside that
invocation shape; the executor counter draft (`f7cd7bb2…`) closes S1/S2/S3/S5 and is the
bytes the L1 should ship. Attack only; nothing built, nothing edited outside this report.

## Bytes attacked (sha256 at attack time; L1 integration landed mid-review, all versions re-attacked)

| role | sha256 |
|---|---|
| r68 harness at base `04093b83` (`git show`, = worktree) | `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527` |
| r69 harness, production `quality/counters/c1-r69-landing-controls.py` (current) | `b374cfb8e024971e69a19d44af21efe5ed1b46c03a3b57387f7dd7fd4eed69aa` |
| r69 harness, proto `.ufo/waves/round-69/proto/c1-r69-landing-controls.proto.py` | `f4d138bfe806f787a98d5ca4d48ebf44896a4276cb0964df5d99e16f6b25390f` |
| r69 harness, seat draft `w1/R69ExecHarness/draft/...` (current) | `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73` |
| r69 harness, earlier integrated + earlier draft (superseded mid-review) | `f4d138bf…` (prod), `89b0cb1c…` (draft) — attacked first, results identical |
| counter, production `quality/counters/c1-r69-paired-recipes.py` (current) | `2060da8dcdb43bcbd08756d0e55630fe585833af3a638b5bc891aa4d77492f82` |
| counter, production (earlier, superseded) | `cf383c91551e4b3de9c17760a19b291a0d9da2c543921df80d6f79588a1c008d` |
| counter, seat draft `w1/R69ExecRecipeCounter/draft/...` | `f7cd7bb2e53864118b5527e93c6e789cc10d94c3c304cafce71f669acc87112d` |

Production harness `b374cfb8` differs from proto `f4d138bf` by exactly one hunk (`"""`→`r"""`,
docstring) — measurement-identical; kill-table results below are byte-stable across all versions.

## Findings by severity

**S1 — production counter: vacuous do-nothing leg can print `TARGET_MET` rc 0.**
`mutation_score`/`measure` treat an absent base harness as `base=0/3`
(`quality/counters/c1-r69-paired-recipes.py:200` `base_rev = args.base_rev or sha`; base-absent
branch sets `base_killed=0` and continues). Live proof (fixture repo containing only the r69
harness at HEAD, `--base-rev HEAD`):
`rc=0`, `MADO_R69_EXTRACT path=quality/counters/c1-r68-landing-controls.py present=no sha256=absent`,
`MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=3d95f9f9…`.
The declared sentence "the r68 harness … must survive all three" is not testable when it is
absent, yet the observable says TARGET_MET. Counter draft `f7cd7bb2` refuses: `raise SetupError("…
is absent at --base-rev …")` → rc 2 (live-proven). Bounded out of the frozen command only because
`04093b83` contains the file.

**S2 — production counter: no compile/parses gate before crediting a kill.**
`killed += int(rc != 0)` (line 168) with no `compile()` of the mutant. Live proof (fixture B:
candidate = r69 harness + trailing `&&&&& syntax error &&&&&`): all three mutants die with
`SyntaxError: invalid syntax` and are printed `killed=yes`, receipt
`selftest=1 killed=3/3 applied=3/3 verdict=TARGET_MISSED rc=1`. The verdict stays MISSED (the
`selftest_rc == 0` gate), so the score cannot be inflated — but the receipt's per-mutant
`killed=yes` rows are credited for failures unrelated to the recipes. Draft closes it:
`apply_recipe` runs `compile(out, "<mutant %s>", "exec")` and refuses non-compiling mutants
(`applicable=no note=… does not compile: SyntaxError`, live-proven), plus selftest pins
"recipe refuses a text that does not compile after substitution".

**S3 — production counter: hung selftest crashes with no contract line.**
`candidate_selftest` uses `run(..., timeout=900)`; `TimeoutExpired` is a `SubprocessError`,
and production `main` catches only `UsageError`/`SetupError` → traceback, rc 1, **no**
`MADO_R69_PAIRED_RECIPES` line — indistinguishable from TARGET_MISSED for rc-only consumers.
Draft `main` catches `(OSError, subprocess.SubprocessError)` → rc 2 with a stderr reason.

**S4 — production harness bytes: stale self-description (round-67 defect class, prose only).**
`b374cfb8` line 2: `r"""Round-68 C1 control harness … (claim C1, attempt 1)`; work dirs
`r68-c1`, `r68-c1-selftest`; fixture git identity `r68-c1@example.invalid` (lines 347–348, 393,
829) — on the r69 surface printing `MADO_R69_*` lines. The **printed contract line and
CONTRACT_RE are correct and byte-exact** (attack 5 below), so this is a docstring/dirname
defect, not an observable-contract defect. Seat draft `9461a059` fixes it ("Round-69", exit
map, `r69-c1`, declared-limits paragraph) and is not yet integrated.

**S5 — production counter: `--base-rev` optional, defaults to `--rev`** (line 200), deviating
from the frozen command shape; omitting it silently runs the do-nothing leg at the measured
content. Draft makes it required (`UsageError`).

**S6 — frozen receipt vs declared contract line (disclosure; receipt cannot be edited).**
`control-baseline-r69.txt` § C1 verdict lines use labels `MADO_R69_C1_BASE`/`MADO_R69_C1_PROTO`
and omit the `base=` and `rev=` fields that the declared contract line requires; the § L probe
evidence cites `grep -n` line numbers without the frozen byte strings. The receipt therefore
cannot alone re-derive the predicate; the operative byte embedding is the counter's `RECIPES`
(verified to match the declaration's texts, including the 12+29-space R1 shape).

**S7 — kill credit is rc-based by predicate (both counters; bounded, disclose).**
Any environment-induced nonzero rc (OOM, interpreter failure) of a mutant selftest is credited
as a kill. The frozen sentence defines kill exactly this way ("counts a mutant killed iff its
own --selftest exits nonzero"), so this is within predicate; it must be disclosed as a limit.

## Attack list results

1. **Kill table** (independent applier, `python3 -I <mutant> --selftest --scratch-root <st>`,
   each mutant also `py_compile`-checked = yes): r68@base R1/R2/R3 → rc 0, `52/52`,
   killed=no (sha256 `bc2d71bc…`, `d85500d4…`, `1764a008…`); r69 (prod, proto, draft ×2
   versions) R1/R2/R3 → rc 1, `57/59`, `58/59`, `57/59`, killed=yes (e.g. current prod:
   `a1f751a4…`, `13c0540e…`, `d61748fe…`). Matches the frozen receipt outcome-for-outcome.
   Kill mechanisms verified: R1 dies via the scripted mr-crash pair case, R2 via the
   no-summary mute case, R3 via the two live guard assertions.
2. **Occurrence counts**: R1/R2/R3 old-texts occur exactly **1** time each in r68@base,
   production, proto and both harness drafts; recipe L occurs **0** times everywhere; it is
   absent from the counter's `RECIPES`. In the counter source the R1 literal is split across
   concatenated string fragments (raw-text count 0; runtime value contiguous) and R2/R3 appear
   5× (definitions + stub + selftest replace) — irrelevant: the occurrence assertion binds the
   scored target only. A second occurrence would make the recipe `applicable=no` → `TARGET_MISSED`
   (production candidate leg; draft base leg raises SetupError) — a second occurrence can only
   block the claim, never inflate it.
3. **Kill-rule**: answered — see S2/S3. The harness's own M-Z leg *does* gate (`bash -n` →
   RecipeError, harness line ~428); the production counter has no analogue for its Python
   mutants; the draft adds `compile()`.
4. **Denominator**: `killed=3/3 ∧ applied<3` is impossible (kill increments only inside the
   `count==1` branch); `TARGET_MET` with `base>0` impossible (`verdict_met` requires
   `selftest_rc==0 ∧ killed==3 ∧ applied==3 ∧ base==0`; pinned by selftests of both counters:
   prod 23/23, draft 61/61, both rc 0 live). The one real hole is the vacuous base leg — S1.
5. **Predicate-literal binding**: `contract_line` prints
   `MADO_R69_PAIRED_RECIPES: selftest=%s killed=%d/3 applied=%d/3 base=%d/3 verdict=%s rev=%s`
   with `absent` substituted for a missing candidate — char-for-char equal to the declared
   line; both counters' `CONTRACT_RE` accept exactly that shape (prod selftest pins the
   byte-exact met/absent lines; draft additionally refuses wrong denominators/missing rev).
   Mismatches found are S4 (stale prose/dirnames), S5 (optional `--base-rev`), S6 (receipt
   labels/fields). The declaration's "Surface changed" sentence is delivered: measurement body
   unchanged (item 6), selftest drives decision+oracle, guard asserted live.
6. **Weakening**: full diff r68@base → current harness = 16 hunks, all classified: TOOL/label
   renames `MADO_R68→MADO_R69` + docstring (11), `_scripted_run` stand-in extensions
   (`mz_stdout` override, `child_marker is None` handling — selftest-only fixtures), two new
   scripted cases (mr-crash, mz-unparseable) + CONTRACT_RE pair assertion, selftest guard
   assertions (guard installed; attempted spawn raises). **No hunk touches `measure()`, `run()`,
   extraction, the R fixture, evidence parsing, or the kill-credit decisions.** For well-formed
   children the real measurement is behaviourally identical to r68.
7. **Equivalence finding: CONFIRMED.** Harness lines 414/435/439: `mz_rc = None` init; inside
   `try:`, after `mz_rc = r.returncode` (a completed `subprocess.run` result — int; `run()`
   raises on timeout rather than returning None), line 439 `mz_killed = mz_rc != 0` — at that
   point `mz_rc is None` is always False, so `mz_killed = mz_rc != 0 or mz_rc is None` is a
   semantic no-op (receipt § L: 59/59 green — reproduced). Correctly excluded from the frozen
   set (0 occurrences in `RECIPES`); had it been included, killed would cap at 2/3 and the
   claim would auto-fail on a null mutation.

## Residual limits the round report must disclose

- The MET verdict is sound only under the frozen command's explicit `--base-rev 04093b83…`;
  the production counter's vacuous-base path (S1) is reachable off-command. Shipping draft
  `f7cd7bb2` (or an equivalent gate) removes the caveat.
- Kill credit is rc-nonzero-based (S2/S7): a broken or environment-failing mutant can be
  credited; verdict-level gating (green candidate selftest) prevented any score inflation in
  every fixture tried.
- Production counter on a hung mutant exits rc 1 with no contract line (S3); consumers must
  key on the `MADO_R69_PAIRED_RECIPES` line, not rc alone.
- Text-anchor recipes: an occurrence inside a string/comment would be semantically inapplicable
  while `count==1` (survivor → MISSED; misses only, no false MET).
- The predicate never requires the unmutated base harness's selftest to be green; a red base
  blocks MET (safe direction).
- The harness's real-children leg remains exercised only at measurement time (selftest is
  scripted) — already the declaration's declared harm-watch leg.
- Bytes moved twice during this review (L1 integration in flight); every finding above was
  re-verified against the final listed sha256s.

Tooling: nothing installed or upgraded (no need; python3/git only). No mutating git/jj command
run in the lane or fleet; fixture repos built under scratch with asserted
`rev-parse --show-toplevel` and explicit `-c user.name/-c user.email` identities. Scratch
`/fast/scratch/hyaku/mado-r69/R69RevC1/` removed at exit.
