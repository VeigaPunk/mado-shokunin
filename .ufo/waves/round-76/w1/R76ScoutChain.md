# R76ScoutChain — what the two successor instruments actually rest on

Frozen instrument rev: `cb713254ee9926e036e594312fdc61b57825526b` (freeze v2). Base:
`c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`. Declaration anchors are the frozen file's
(`git show cb713254:.ufo/waves/round-76/claims-declaration-r76.md`). Method: read-only `git show`
for every instrument; independent runs in `/fast/scratch/hyaku/mado-r76/R76ScoutChain/` (no repo
writes, no git mutations, no tool installs).

**Observed state caution.** While this seat ran, the working-tree copy of
`quality/counters/c2-r76-shapes.py` acquired an uncommitted edit by another seat (parameter-aware
`call_cancellations`). Every C2 probe below therefore runs against the **frozen** bytes extracted to
scratch (`rev/c2-r76.py`); a live-tree artefact must not be read as the claim's code.

---

## 1. C1 — `c1-r76-landing-controls.py` + `c1-r76-outcome-field.py`

### 1.1 Where the challenge is drawn

- `c1-r76-landing-controls.py:254-263` — `draw_challenge()`: `while True: nonce = secrets.token_hex(8);
  if CHALLENGE_RE.search(nonce): return nonce`.
- `:66` — `CHALLENGE_RE = re.compile(r"[a-f]")`. `token_hex` emits `[0-9a-f]`, so a digits-only draw
  is rejected and **every returned challenge contains at least one `a-f` byte by construction**
  (rejection sampling, not probability). Rejection probability per draw `(10/16)^16 ≈ 5.4e-4`.
- `:269` — one draw per measurement (`nonce = draw_challenge()`), after the generation loads.
- `:271-272` — announced as `MADO_R76_CHALLENGE source=secrets.token_hex(8) length=16 has_letter=yes
  generation_sha256=… rev=…`; the value is never printed.
- `:223-226` — the only child-env change: `child_env` adds `MADO_LANDING_NONCE`; `:236-244` wraps the
  frozen `describe_env` to redact that one key.
- `:295-297` — selftest draws 200, asserts every draw has an `a-f` and all are distinct.

### 1.2 Witness grammar

- `:65` — `WITNESS_RE = re.compile(r"MADO_LANDING_WITNESS: ([0-9a-fA-F]{16,})")` (G1: 16 **or more**).
- `:114-120` — `last_witness`: reversed line scan, `fullmatch(line.strip())`, first hit wins (i.e. the
  **last** parsed marker); a malformed trailing marker cannot suppress a real one.
- `:123-127` — `witness_state` → `ok` / `absent` / `mismatch`.
- `:137-138` — `green_with_witness` = frozen `summary_green(out)` **and** byte-equality of the last
  parsed echo with the challenge.
- `:149-150` — `credit_with_witness` = frozen `credit(out)` **and** the same byte-equality. This is
  the M-Z kill rule, so **a credited M-Z kill already proves the echo** — the declared negative result.
- G1's only effect is `absent → mismatch` on overlong echoes; no scored field reads `witness=` (see F7).

### 1.3 The named `outcome_green` rule and the contract row

- `:141-146` — `outcome_green(r72_green, selftest_out, nonce, killed)`; `:146` returns
  `bool(green_with_witness(...)) and killed == 2`. This single line is the mutants' anchor.
- `:228-234` — `contract_line`, nested in `install_rule`, assembles
  `MADO_R76_LANDING_CONTROLS: selftest=<p/n|none> mz=<pass|fail> mr=<pass|fail> killed=<d>/2
  baseline=0/2 witness=<ok|absent|mismatch> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>` from
  `summary_fraction` (`:153-158`, last parsed frozen summary), the passed-in `mz`/`mr`/`killed`
  (computed by the frozen r72 `measure` at its `:593`: `killed = int(mz_killed) + int(mr_killed)`),
  `witness_state`, `outcome_green`, `rev`.
- Emitted through the patched `emit` `:220-221` → `rewrite_prefix` `:130-134`, which rewrites only
  lines starting `MADO_R72` to `MADO_R76`.
- The harness's own `CONTRACT_RE` (`:69-72`) is used **only in the selftest** (`:336-338`); the measure
  path never validates its row. The counter's `CAND_RE` (`c1-r76-outcome-field.py:93-96`) is the gate.
- `:274` — dead `line = None` in the wrapper's `measure`; the wrapper returns the r72 rc unchanged.

### 1.4 How the four mutants are patched, and why the anchor must occur exactly once

- `c1-r76-outcome-field.py:79-92` — `MUTANTS`: four `(name, old, new)` triples; all four share the
  **same** `old` (the whole return line of `outcome_green`), and differ only in `new`.
- `:293-310` — `apply_mutants`: `text.count(old)` must be exactly 1 (`:298-301`), then
  `text.replace(old, new, 1)` (`:302`), then require a change (`:303-304`) and `compile()`
  (`:305-308`). Each mutant is applied to the pristine `text` (`:295`), never to a previous mutant,
  so the four are mutually exclusive alternatives of one line.
- Why once: a duplicated anchor would let the one-shot replace patch an occurrence that need not be
  the named rule (the mutant's name/provenance would be unverifiable), and a missing anchor would
  yield a no-op mutant that scores 16/16 and silently lowers `killed`. Both are rc-2 `SetupError`.
- `:437-438` re-checks the anchors against the embedded `RULE_SNIPPET` copy; `:439-440` checks the
  replacements differ. The real bytes are checked by `apply_mutants` at run time.

### 1.5 Where the frozen round-72 harness passes through unchanged

`load_generation` (`:177-210`) reads `quality/counters/c1-r72-landing-controls.py` from git at
`--rev`, pins sha256 `b6108c86…` (`:63`, verified equal to the file at cb713254), writes it to a
private `mkdtemp` under the validated scratch (`:188-190`, `O_NOFOLLOW` at `:207`) and
`runpy.run_path`s it (`:210`). `measure` then calls `mod["measure"](args)` (`:273`).
`install_rule` overrides **only six globals** (`:246-251`): `emit`, `child_env`, `describe_env`,
`credit`, `summary_green`, `contract_line`.

Unchanged and executed as frozen (`c1-r72-landing-controls.py` anchors): extraction of the four
instrument files (`:223-234`), the extracted instrument's own `--selftest` run and evidence
(`:489-496`), the M-Z recipe `mutate_clause` (`:238-246`) + `bash -n` + rerun (`:507-525`), the M-R
fixture `build_r_fixture` (`:411-458`, `git replace` plant, guarded/forged `ls-tree`), `neutralize_guard`
(`:257-273`), `citecheck_marker` / `control_ok` / `forged_credit` (`:277-295`), `last_summary`,
`count_fails`, `last_parsed_summary`, `summary_fraction` (`:298-330`), `describe_env` base
(`:375-386`), the kill tally (`:593`), the rc `outcome_exit` (`:596`), and every emitted evidence
line except the prefix rewrite.

Consequence not stated in the declaration: the printed `verdict=` comes from the overridden
`contract_line`/`outcome_green`, while the harness's **exit code still comes from r72
`outcome_exit`** (`summary_green` + `killed == 2`). Under mutation the two deliberately diverge, and
the counter reads only stdout (F9/F-not-modelled).

---

## 2. C2 — delta sites of `c2-r76-shapes.py` against `c2-r75-shapes.py`

`git diff c3e0bc5f… cb713254 -- quality/counters/` shows the three successor files as new; the
meaningful delta is `diff -u c2-r75 c2-r76` (frozen copies in scratch). Delta sites, r76 line numbers:

| # | Site | Lines | Kind |
|---|---|---|---|
| 1 | module docstring: D3/D4, base rev, 59/55, limits | 1-43 | prose |
| 2 | `TOOL`, `BASE_COUNTER`, `BASE_COUNTER_SHA256` | 55-57 | constants |
| 3 | `FROZEN_CONTROLS 59`, `FROZEN_BASE_CONTROLS 55`, controls sha, `HELD_CONTROLS` r75 / sha / 47 | 64-72 | constants |
| 4 | `CONTRACT_RE` denominators `/59` | 74-77 | receipt |
| 5 | **`keyed_names`** (D4 helper) | 382-399 | new |
| 6 | **`cancelling_functions`** (D3 callee scan) | 402-435 | new |
| 7 | **`call_cancellations`** (D3 call-site map) | 438-450 | new |
| 8 | `unguarded_rebindings(..., consts)` + del branch rewritten | 453, 478-490 | predicate |
| 9 | `guard_producers` passes `const_key_names(tree)` | 533 | wiring (D4 only) |
| 10 | `has_guard`: compute `cancelling`; pass `consts`; merge call cancellations | 575, 609-611 | wiring (D3+D4) |
| 11 | `carrier_guard`: compute `cancelling`/`calls`; pass `consts`; merge | 987-988, 1020-1022 | wiring (D3+D4) |
| 12 | receipt prefix `MADO_R75_*` → `MADO_R76_*` | 1431, 1464, 1477, 1487, 1496, 1516, 1536, 1546 | labels |
| 13 | selftest prose/labels only; 47 embedded `CASES` and 28 `REGRESSIONS` untouched | 1772, 1790-1811, 1826-1829 | tests |

**D3 paths.** `cancelling_functions` (`:402-435`) names a local function whose body contains a live
`del <param>[<literal-or-module-const>]` with no earlier rebinding of that parameter
(`:427-434`, `out.add(fn.name)`), skipping `false_guarded_lines` bodies (`:411`).
`call_cancellations` (`:438-450`) maps **the first positional `Name` argument** of any call to such a
name (`:448-449`). The map is merged into the scope's rebind lines at `:610-611` and `:1021-1022`, so
the existing dominance test (`guard_line < r < first_use`) decides.

**D4 paths.** `keyed_names` (`:382-399`) counts simple assignments whose value is the guard key
(literal string, or a name in `const_key_names`) and keeps names with exactly one such assignment;
the del branch (`:478-490`) accepts `key_is_guard(target.slice, consts)` **or** a `Name` present in
`keyed_names` and bound before the delete (`keyed[slice.id] < node.lineno`). Note site 8 also widens
the *literal-only* del test of r75 to `key_is_guard`, which newly accepts a module constant written
directly as the slice — a delta the declaration does not name (F13).

**Where D3 is absent.** `guard_producers` (`:523-546`; D4 is wired at `:533`, D3 is not),
`attribute_flow` (`:797-900`, `:893` calls `unguarded_rebindings(nodes)` with no `consts`),
`alias_store_guard` (`:903-980`, own `rebound` map, no del handling), `global_guard`
(`:1038-1127`, own `replaced` map, a `Delete` is never recorded), `environ_transport_guard`
(`:1140-1177`, own `replaced` set; `del os.environ[KEY]` literal/const only), `twohop_guard`
(`:1235-1292`, own `replaced`), `environ_alias_guard` (`:1318-1372`, own `cancels`
`:1332-1339`, literal/const only, no name-bound key).

**Where D4's name binding is absent.** The same list, because only `unguarded_rebindings` carries it;
plus `attribute_flow` loses D4's module-constant half (no `consts` at `:893`).

---

## 3. Declaration vs code — disagreements (the findings)

Full table with quoted declaration sentences: `w1/R76ScoutChain/findings.md`. Condensed:

| # | Where | Disagreement |
|---|---|---|
| F1 | C1 denominator | Declaration L26 "fifteen-case expectation" vs code `FROZEN_CASES = 16` (`outcome-field:68`), controls 16, target `cases=16` (L72). v1 residue. |
| F2 | C1 kill rule | Declaration L67/L69 "below fifteen" vs code `score < len(cases)` = below **16** (`:393-394`). Literal threshold makes 15/16 and 14/16 survive → `killed=0/4` → the frozen target is unsatisfiable. |
| F3 | C1 separator | Declaration L62 assigns `outcome-summary-only` to `green-absent`; observed miss is `green-mutant` only. `green-absent` has `witness=absent`, so both rules reject — it separates nothing. |
| F4 | C1 separator | Declaration L65 assigns `outcome-killed-or` to `always-red`; it also misses `green-mutant` (14/16). |
| F5 | C1 "separates four" | `outcome-summary-only` and `outcome-killed-any` have identical scores and identical miss sets; the set kills each mutant but does not distinguish those two rules. |
| F6 | C1 counter prose | Docstring still describes v1: 15 cases, "below fifteen", receipt `cases=15` (rejected by its own regex), and the four v1 mutant names (`:10,24,26-29,31-32,37,39,51`); constants/mutants are v2. |
| F7 | C1 G1/G2 | Implemented (`:65`, `:254-263`) but not load-bearing: no frozen case or mutant depends on G1 (only `witness=` changes, unscored), and the mutants that needed G2 were removed at v2. |
| F8 | C1 control | "the held round-75 scoring rule" is not run: `base_score` is a projection of the same candidate's `mz` field (`:378-399`); `--base-rev` is resolved (`:345`) and unused. `base_killed=0` is analytic. The committed baseline receipt measured the v1 mutant set on 15 cases. |
| F9 | C1 target | `met` adds `challenge_ok` (`:401-402`), a grep of the candidate's own unconditional `MADO_R76_CHALLENGE … has_letter=yes` line (harness `:271-272`), not an observation of the draw. |
| F10 | C1 modes | "one per mode" (L40-41): 16 cases, 17 template modes, `green-last-wrong` unused. |
| F11 | C1 anchors | Agrees: one anchor line, exactly-once enforced (`:298-301`). |
| F12 | C2 denominators | Agrees (59/59, 55/59, 47 carried, hash-checked). |
| F13 | C2 D4 attribution | `dynamic-key-module-const` is separated by `key_is_guard(slice, consts)` (`:486`), not by a same-scope binding; `keyed_names` in `run` is `{}`. D4's sentence predicts guarded for it. |
| F14 | C2 D4 "once" | `keyed_names` counts only `Assign`/`AnnAssign`; `for k in …` / `with … as k` rebinds are invisible → false unguarded (probes: `{'k': 2}`, `(True, False)`), although `assigned_names` already counts them (`:261-277`). |
| F15 | C2 D3 argument | The callee's deleting parameter is not tracked; only the first positional `Name` is mapped. Observed over-cancel (`drop(env, m)` deleting `m`) and under-detect (`drop(m, env)` deleting `env`), plus keyword miss (disclosed by the limits). |
| F16 | C2 D3 scope | `call_cancellations` walks the whole tree and the map is applied to every scope: a nested helper's `drop(env)` flips an unrelated outer guard to unguarded (probe `nested-same-name` → `(True, False)`). |
| F17 | C2 D3 flows | D3 exists only in `has_guard` and `carrier_guard`; absent from six other flows, not just "the attribute flow" (L141-142). |
| F18 | C2 population | 20/13/13/0 is correct but independent of D3/D4: **0 `del` statements** in the 20 population files; the controls are the only discriminators. |

---

## 4. Observed runs (my scratch, frozen bytes)

| Run | Result |
|---|---|
| `c1-r76-outcome-field.py` full measure, rev cb713254 | `cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET`, rc 0, 9.5 s |
| per-case `killed` (driver using the counter's own `make_fixture`/`harness_run`/`apply_mutants`) | 2/2 on `right`, `liar-success`, `always-red`; 1/2 on the other 13 |
| mutant miss sets | summary-only `{green-mutant}`, killed-only `{always-red}`, killed-any `{green-mutant}`, killed-or `{always-red, green-mutant}` |
| `c1-r76-landing-controls.py --selftest` | 23/23, rc 0 |
| `c1-r76-outcome-field.py --selftest` | 19/19, rc 0 |
| `c2-r76-shapes.py --selftest` (with controls) | 97/97, rc 0 |
| `c2-r76-shapes.py` measure, rev cb713254 | `population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET`, rc 0 |
| held 59-case misses | `callee-del-literal`, `callee-del-store`, `dynamic-key-del`, `dynamic-key-module-const` (exactly base 55/59) |
| population AST scan | 0 `del` statements across the 20 `quality/check-*.py` files |
| pins | r72 `b6108c86…`, r75 census `0544c0ef…` both match their constants |

Receipts for every row (commands, stdout, rc) are in `w1/R76ScoutChain/probes/`:
`ran-c1-outcome-field.txt`, `ran-c1-per-case.txt`, `ran-c2-shapes.txt`, `ran-selftests.txt`,
`ran-probe-c2.txt` (+ the re-runnable `probe-c2-d3-d4.py`, which extracts the frozen instrument
with `git show` so the in-flight working-tree edit cannot be mistaken for the claim's code).

## 5. Remaining unknowns

- The held round-75 counter (`c1-r75-harness-witness.py`) has no mutant machinery, so "the held rule
  kills 0/4" is a projection over the candidate's `mz` field, never an executed held run. I did not
  build one (out of seat scope).
- F16's cross-scope leak is demonstrated on a synthetic case; its effect on the production population
  is nil only because no population file contains `del` (observed).
- The label set was not re-derived with the committed `proto/label-derivation-r76.py`; I re-derived the
  16 candidate `(mz, verdict)` pairs directly and all 16 match the frozen labels.
- The in-flight, uncommitted rewrite of `call_cancellations` in the working tree was not audited; it
  is not the frozen claim's code.
