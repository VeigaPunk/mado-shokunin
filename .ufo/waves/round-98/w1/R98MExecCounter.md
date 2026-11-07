# R98MExecCounter -- w1 report: C1 execargv counter (round 98)

Seat `R98MExecCounter`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
predicate **PRED-C1-r98-v1** (amended twice in flight: 16 -> 20 classes, >=60 ->
>=70 cases, predicate (v) three DISTINCT controls, schema gains
`X-GIO-NoFuse`/`desktop_raw`, predicate (iv) two-measurement freeze).

## Files written (owned paths only)

- `.ufo/waves/round-98/build/c1-r98-execargv.py` -- the C1 counter draft.
  sha256 `7ed2f8f62ca9bb0fe2706f1e6c09ad20d6276404f7f5112507842b0eee0a64c5`.
  ASCII only, stdlib only, ~1720 lines. Never writes the lane.
- `.ufo/waves/round-98/w1/R98MExecCounter.md` -- this report.

## Verdicts (measured this session)

- counter `--selftest`: `MADO_COUNTER_SELFTEST: checks=16 failed=0`, exit 0
  (stable ids; mini universe synthesised at runtime, see Deviations).
- Full measurement on the 16-class freeze (64 cases, candidate
  `31aca8d8...`, real 75-mutant file `c5b66f58...`, generator `f9a0df27...`,
  fixture repo `e2e2/repo` rev `5274cf30...`):

  ```
  MADO_EXECARGV_COUNT: TARGET_MET pred=PRED-C1-r98-v1 rev=5274cf30... base_rev=ccc9751e...
    tool_sha256=31aca8d8... tool_pin=ok gio_sha256=d2164260... cases=64 correct=64
    classes=16/16 per_class plain=4 f=4 F=3 u-file=3 u-uri=3 u-anchor=4 U-mixed=4 d=3 n=3
    i=4 c=3 k=3 pct=4 bad=7 quote=8 path=4
    mutants=75 killed=75/75 crashed_not_killed=0 survived=0 class_kills=16/16
    fresh=60/60 fresh_seed=74ab7402b9abb078
    census cases=ok fresh=ok static_structural=ok audit_denials=0
    control_naive=4/64 control_noexp=5/64 memoriser_frozen=64/64 memoriser_fresh=0/60
    selftest=ok checks=31 failed=0
  ```

  rc 0. Every predicate leg green: frozen exact, mutants all killed with every
  class killing >=1, fresh exact, controls behind, memoriser clean on fresh,
  candidate selftest green, zero audit denials.
- rc discipline verified: a bogus `--expect-tool-sha256` run exits 2 with
  `SETUP_ERROR` (the earlier `RC=0` readings were a pipe artifact of
  `| tail`, not the counter).
- 20-class artifact set validated structurally (the amended universe):
  cases `bb78dc3f...` (20 classes, 86 cases, 0 absolute expect strings, 7
  refusal expects with causes no-exec/desktop-file/exec-parse, 10
  `desktop_raw` cases), mutants `5f074f70...` (79 counted + 16
  not_observable + 8 equivalents, `candidate_sha256=acfcc4f7...`, all 20
  classes covered; MutC1 sweep: killed 79/79, class_kills 20/20),
  generator `b7bc137a...` (CLI unchanged; absolute `--dir` produces
  ok/refusal mixes correctly), renderer `182cf06c...` (`PROBE_SH` bytes
  identical to the counter's materialised probe; `render_desktop` key order
  Type/Name/Icon/Exec/Path/Terminal/Hidden/X-GIO-NoFuse == counter
  `DESKTOP_KEYS`), candidate `acfcc4f7...` (selftest `checks=38 failed=0`;
  imports json/os/re/shutil/sys/tempfile, only `os.path` used; Tool
  head-to-head 52/52 multiset vs `/usr/bin/gio`).

## Counter design (what the instrument does)

- Pins, fail-closed: `--expect-cases-sha256`, `--expect-mutants-sha256`,
  `--expect-genseed-sha256`, `--expect-tool-sha256`, `--expect-gio-sha256`
  (all 64-hex, SETUP_ERROR on mismatch); the cases envelope's
  `renderer_sha256` is required (64-hex) and verified against
  `execargv-probe-r98.py` beside the `--cases` file (`renderer_pin=ok`,
  `=skip` when absent, SETUP_ERROR on mismatch -- it caught two real
  post-freeze renderer edits this session).
- Revisions: `--rev` accepts a commit or `worktree` (reads the lane working
  tree for an uncommitted candidate); `--base-rev` must be a commit where
  `tools/mado-execargv.py` is absent (the declared before-state).
- Materialisation: `probe.sh` = the oracle's lock-seq `PROBE_SH` bytes
  (byte-verified against the renderer), 0755; `case.desktop` from the
  desktop dict in canonical key order with literal values (`None` omitted,
  bools `true`/`false`, LF, trailing newline) or the case's `desktop_raw`
  whole-file bytes; `{probe}`/`{root}` substituted in every desktop value,
  every arg (with `{probe}` -> empty in args, per `gio_argv`), and
  `desktop_raw`; empty `h/` HOME; `X-GIO-NoFuse` accepted as
  str/bool/null (8th key, after `Hidden`).
- Scoring: every run goes through the r97 audit launcher with an empty PATH
  (`env PATH=<mkdtemp> LC_ALL=C HOME=<case>/h TMPDIR=<cwd>`) and carries
  `--json`; the counter parses the single JSON object (lossless --
  newline-valued argv cannot break it). Comparison is launch count +
  MULTISET of argv vectors (declaration rule 7; both sides sorted).
  Refusal expects `{"error": cause}` match rc 2 + cause exactly.
  rc not in {0,2} = crash; unparseable/missing output = malformed = a
  scored wrong answer, never a crash.
- Mutants: `find` must occur exactly once in the candidate's non-selftest
  prefix (cut at `def selftest(`) and be unique across mutants /
  not_observable / equivalents; `candidate_sha256` must equal the pinned
  tool sha; `classes` must equal the frozen 20 in order. A kill requires a
  NEW wrong answer (mutant wrong where the candidate was ok) -- a mutant
  that only re-fails a case the candidate already fails is `survived`,
  and a new crash with no new wrong is `crashed_not_killed`.
- Fresh leg: counter runs the pinned generator
  (`python3 -I <genseed> --seed HEX --dir D --out F --count 60`, all four
  flags) with absolute paths, requires the `FRESH_GEN` summary count to
  equal the JSONL line count and a `FRESH_GEN_PIN` line carrying the
  pinned gio sha; validates every case (class absent -> "fresh"), checks
  label/expect consistency (`ok` <-> argv shape, `refusal:<cause>` <->
  error cause), repairs the generator's canon gap defensively (mid-string
  case roots rewritten back to `{probe}`/`{root}` tokens -- belt and
  suspenders since the oracle's canon fix landed), then rebuilds every
  root itself under scratch and scores with the same launcher/parser.
  A persistent `setup-error` label fails closed (SETUP_ERROR).
- Controls (amended predicate (v), three DISTINCT models, all embedded
  <=30-line scripts written by this counter): `NAIVE_SRC` (28 lines,
  `Exec.split()`, no field codes) and `FIELD_SRC` (30 lines, expands the
  consuming codes %f/%u/%d/%n/%F/%U/%D/%N + `%%`, ignores quoting and
  iteration, one launch, non-local URI rules) -- each must score strictly
  fewer than the total; the memoriser (frozen expects keyed by case id)
  must score 0 on the fresh leg. The earlier no-expansion model was
  replaced by the field-code model per the L1's distinctness ruling.
- Candidate `--selftest`: `checks=N failed=0`, N >= 12, rc 0 required.
- Static check on the frozen candidate bytes: stdlib-only imports,
  denied top-levels (process/socket/network/dynamic), denied dynamic-load
  attributes, denied bare names, dunder access, `os.*` spawn attrs
  (`re.compile` as an attribute is exempt -- legitimate; bare `compile(`
  needs eval/exec and stays flagged).
- `--mini-scale` hidden flag rebinds the census (2 classes, tiny minimums)
  for the counter's own selftest.

## Routed findings (for the L1 / sibling seats)

1. **Fresh canon gap (fixed by the oracle)**: the generator's `canon()`
   only rewrote the case root as a value prefix; an attached field code
   (`end%f`) left `<transient-root>/f2.txt` absolute mid-string (measured
   `fresh-07f72045b91a494c-56`). The oracle fixed canon (substitute
   anywhere, probe first) and re-pinned; the counter keeps a defensive
   transient-root repair.
2. **Renderer post-freeze edits (twice)**: `execargv-probe-r98.py` changed
   after the cases freeze both times (17:04 canon fix, 17:17
   X-GIO-NoFuse render order). The counter's renderer pin correctly
   SETUP_ERRORed on each transient state; the oracle re-pinned the cases
   header both times.
3. **Generator relative `--dir` doubling bug (renderer/generator side,
   NOT the counter)**: with a relative `--dir`, `case_expect` builds a
   doubled desktop path (`<abs>/gs-probe/repro/<rel>/gs-probe/repro/...`)
   and every case measures a refusal. The counter always passes absolute
   `--dir`/`--out` (verified: absolute dir produces ok/refusal mixes), so
   the fresh leg is unaffected; the oracle should still fix or document
   the relative-path case.
4. **Mutant kill semantics**: the counter requires a NEW wrong answer per
   kill (candidate-ok cases only); the old-bytes run showed pre-existing
   candidate misses would otherwise mask survivors.
5. **u-anchor-03 query leak (fixed by the tool seat)**: the old candidate
   bytes kept `?q=1` in a local file URI path; the final candidate
   (`acfcc4f7`) cuts fragment then query (Tool re-measured live; my
   64/64 on the 16-class freeze confirms).

## Deviations and risks

- The counter's `--selftest` synthesises its mini universe (fixture git
  repo, mini candidate/cases/mutants/generator/renderer stub) at runtime
  under a temp dir: this seat's write scope names no committed fixture
  path, so no `selftest-fixtures/` tree is committed (unlike the C2
  sibling). All selftest artifacts are ASCII and cleaned up.
- The counter materialises the desktop itself (canonical key order,
  literal values) rather than importing the renderer: the declaration
  makes the renderer's `render_desktop` normative and pins its sha256 in
  the cases header; my materialisation was verified byte-compatible by
  the 64/64 frozen score (any desktop-byte divergence would change gio's
  parse). `desktop_raw` bypasses the key order entirely.
- `X-GIO-NoFuse` is accepted in the desktop dict (str/bool/null) although
  the current frozen cases carry it only via `desktop_raw` / the
  generator's structured `desktop` block with null default; the 17:17
  renderer emits it as the 8th key, matching `DESKTOP_KEYS` order.
- The fresh leg's `FRESH_COUNT` is "60" (>=40 required); the generator's
  two-measurement freeze protocol makes fresh generation slow
  (~1.3 s/case measured) -- well inside `FRESH_RUN_TIMEOUT=900`.
- Tool installs: none (stdlib sufficed; `gio` at `/usr/bin/gio` is the
  pinned oracle).

## Blocker at wrap-up (2026-11-07 ~17:25)

The oracle's **88-case double-measurement re-freeze** (predicate (iv):
labels frozen only when two consecutive measurements agree; cases file
will carry the FINAL `renderer_sha256` automatically; nofuse cases move
to the structured key; +u-anchor-05-U-frag, +i-06-abs-icon;
`setup-error` labels fail closed) had NOT landed when this report was
written. The cases file on disk (`bb78dc3f...`, 17:12, 20 classes/86
cases) still pins renderer `48c9a169...` while the renderer file is
`182cf06c...`, so the counter correctly reports SETUP_ERROR
(`setup-renderer-sha256`) on the current tree -- fail-closed by design,
not a counter bug.

**Pins for the final run once the re-frozen cases file lands** (all
others already final):

```
--repo <fixture or lane> --rev <commit|worktree> --base-rev 35f3ce80...
--cases .ufo/waves/round-98/controls/execargv-cases-r98.json
--expect-cases-sha256 <sha256 of the re-frozen file; header renderer_sha256 must equal 182cf06c... or later>
--mutants .ufo/waves/round-98/controls/execargv-mutants-r98.json
--expect-mutants-sha256 5f074f70e6c30339ea61daf2e3f7d849c5ffd181f1e94d1adcca3222eee8438e
--genseed .ufo/waves/round-98/controls/execargv-fresh-r98.py
--expect-genseed-sha256 b7bc137a643c771f1cd88a3909d1650205b37a155869ade84adc419e3515357c
--expect-tool-sha256 acfcc4f7d75162d8035ac26e7ecf48ace8b78dcc8255775e8bab347cfa70ab61
--expect-gio-sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462
```

If the generator or renderer changes again before the re-freeze
completes, re-take those two shas from disk. The counter needs NO further
edits for the amended universe (20 classes, >=70 cases, three controls,
`X-GIO-NoFuse`, `desktop_raw`, `setup-error` fail-closed are all
implemented and selftest-green).

## Checks the L1 should run

1. `python3 -I .ufo/waves/round-98/build/c1-r98-execargv.py --selftest`
   -> `MADO_COUNTER_SELFTEST: checks=16 failed=0`, rc 0.
2. The full counter invocation above against the re-frozen cases file
   (fixture repo `/fast/scratch/hyaku/mado-r98/R98MExecCounter/e2e3/repo`
   rev `ebb564a9...` holds candidate `acfcc4f7` at `tools/mado-execargv.py`
   with base `6086ecbc...`, or the landed lane commit with
   `--rev <commit>` / `--rev worktree`).
3. `python3 -I tools/mado-execargv.py --selftest` on the landed candidate
   (38 checks green at `acfcc4f7`).
