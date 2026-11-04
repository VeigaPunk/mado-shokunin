# R76ScoutChain — findings.md (claim | declaration sentence | code anchor | agree/disagree)

Frozen instrument rev: `cb713254ee9926e036e594312fdc61b57825526b` (freeze v2). Base:
`c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`. Declaration line numbers are the frozen file's
(`git show cb713254:.ufo/waves/round-76/claims-declaration-r76.md`). All code anchors are the
frozen bytes; the working-tree copy of `c2-r76-shapes.py` was found modified by an in-flight seat
mid-audit, so the frozen copy was extracted to scratch
(`/fast/scratch/hyaku/mado-r76/R76ScoutChain/rev/c2-r76.py`) and every probe below ran against it.

Evidence class: **[O]** observed (my run/probe against the frozen bytes), **[D]** derived
arithmetic from observed values, **[I]** inference from reading code.

## C1 — `c1-r76-outcome-field.py` / `c1-r76-landing-controls.py`

| # | Claim | Declaration sentence (line) | Code anchor | Verdict |
|---|---|---|---|---|
| F1 | C1 denominator | "against a frozen **fifteen-case** expectation" (L26) | `c1-r76-outcome-field.py:68` `FROZEN_CASES = 16`, `:69` `FROZEN_CORRECT = 16`, `:99` `CONTRACT_RE` `cases=16`; controls JSON has 16 cases | **DISAGREE** — the same section then says "sixteen real bash fixture lanes" (L40). "fifteen" is the v1 constant (`755b339f:…:68` `FROZEN_CASES = 15`), left in the claim sentence at freeze v2. |
| F2 | C1 kill rule | "A mutant is killed iff its two-field score is **below fifteen**"; base-killed "mz-only score is **below fifteen**" (L67–69) | `:393` `is_killed = score < len(cases)`; `:394` `is_base_killed = base_score < len(cases)`; `len(cases) == 16` | **DISAGREE** — the measured scores are 15/16, 15/16, 15/16, 14/16 [O]. Under the literal `< 15` threshold **none** is killed → `killed=0/4`, so the frozen kill rule contradicts the frozen target (`cases=16 correct=16 killed=4`, L72). The code's threshold is 16. |
| F3 | C1 separator, `outcome-summary-only` | separator `green-absent` (green, killed 1) (L62) | `c1-r76-outcome-field.py:80-82` mutant; rule `c1-r76-landing-controls.py:141-146`; fixture echo for `green-absent` falls to `c1-r76-outcome-field.py:131` (`*) : ;;` → no echo); observed miss = `green-mutant` only [O] | **DISAGREE** — `green-absent` carries `witness=absent`, so `green_with_witness` is false and the mutated rule returns `TARGET_MISSED` exactly like the base: it separates nothing. The real separator is `green-mutant` (witness ok, killed 1/2). |
| F4 | C1 separator, `outcome-killed-or` | separator `always-red` (L65) | `c1-r76-outcome-field.py:89-91`; observed misses = `always-red` **and** `green-mutant` → 14/16 [O] | **DISAGREE (incomplete)** — the row omits that `green-mutant` also separates it; that is why its score is 14, not 15. |
| F5 | C1 "separates four named mutations" | "separates four named mutations of the outcome rule" (L26–27) | `:79-92`; miss sets [O]: summary-only `{green-mutant}`, killed-any `{green-mutant}`, killed-only `{always-red}`, killed-or `{always-red, green-mutant}` | **PARTIAL** — all four are killed (target met), but `outcome-summary-only` and `outcome-killed-any` are behaviourally identical on all 16 cases (same 15/16, same miss). The set kills each mutant; it does not separate those two rules from each other. "Separates" holds only in the weak sense. |
| F6 | C1 counter prose vs its own constants | n/a (code-internal) | docstring `:10` "Fifteen REAL", `:24` "same fifteen cases", `:26-29` the four **v1** mutant names (`outcome-term-dropped`, `prefix-match`, `first-witness-wins`, `case-insensitive`), `:31-32` "below fifteen"/"stays fifteen", `:37` receipt `cases=15 correct=15` (rejected by its own `CONTRACT_RE` `:99`), `:39` "cases == 15", `:51` "fifteen modes" | **DISAGREE** — the module's usage text advertises the v1 instrument; the constants and `MUTANTS` (`:79-92`) are v2. Only `:45` was updated to "sixteen". |
| F7 | C1 G1/G2 load-bearing | G1: `{16,}` makes prefix-vs-equality observable; G2: challenge always changes under uppercasing (L75–80) | `c1-r76-landing-controls.py:65` `WITNESS_RE … {16,}`; `:114-120` `last_witness`; `:254-263` `draw_challenge`; `c1-r76-outcome-field.py:245-251` `parse_row` scores `mz` and `verdict` only | **IMPLEMENTED, NOT EXERCISED [O][D]** — G1 flips only `witness=absent→mismatch` on overlong cases; `verdict` is unchanged, and `witness=` is not scored. The prefix mutant that needed G1 was deleted at freeze v2 (`755b339f:…:83-85`). G2 removes a ~(10/16)^16 ≈ 5.4e-4 flake from the `uppercase`/`green-uppercase` candidate legs; the case-insensitive mutant that needed it is also gone. |
| F8 | C1 do-nothing control | "the **do-nothing control is the held round-75 scoring rule**, which reads `mz=` only" (L68–69) | `:378-399` `base_score` counts `mz` matches **from the same candidate run**; `:345` `base_sha = resolve_rev(...)` is never used again | **DISAGREE (provenance)** — the held instrument is not extracted or run; the control is a projection of the candidate's own `mz` field. `base_killed=0` is analytic, not measured, because the mutants patch a line the M-Z path never calls. The committed `control-baseline-r76.txt` measured the **v1** mutant set on 15 cases; the working-tree `control-baseline-r76-matched.txt` is a post-freeze re-derivation. |
| F9 | C1 target predicate | target = `cases=16 correct=16 mutants=4 killed=4 base_killed=0` (L71–72) | `:401-402` `met = (… and challenge_ok)`; `challenge_ok` from `has_case_changing_challenge` `:254-258` matching `MADO_R76_CHALLENGE source=… has_letter=yes `, printed unconditionally at `c1-r76-landing-controls.py:271-272` | **DISAGREE** — the code adds a sixth conjunct the target omits, and it is a grep of the candidate's self-announcement, not an observation of the draw (a harness that never rejected a digits-only draw still passes it). |
| F10 | C1 "one per mode" | "sixteen real `bash` fixture lanes, **one per mode**" (L40–41) | `LANE_TEMPLATE :103-160` carries 17 modes; selftest `:428-433` asserts 17; the 16 cases use 16 distinct modes; `green-last-wrong` has no case | **DISAGREE (minor)** — 16 lanes / 17 modes. |
| F11 | C1 anchors | "anchored at the single return line of … `outcome_green(...)`, which the contract line calls" (L57–58) | `:146` return line; `:230` `contract_line` calls `outcome_green`; `apply_mutants :293-310` counts each anchor (`:298-301`), replaces once (`:302`), requires a change (`:303-304`), compiles (`:305-308`); candidate each time from pristine `text` (`:295`) | **AGREE** — mechanism as declared. Uniqueness matters because a duplicate anchor would let the one-shot replace patch a line that may not be the named rule, and a missing anchor would yield a no-op mutant scoring 16/16; both are rc-2 `SetupError`. |

## C2 — `c2-r76-shapes.py` vs `c2-r75-shapes.py`

| # | Claim | Declaration sentence (line) | Code anchor | Verdict |
|---|---|---|---|---|
| F12 | C2 denominators | 59 cases, 47 carried + 12; `controls=59/59 base_controls=55/59` (L108–112, L129–130) | `:67` `FROZEN_CONTROLS = 59`, `:68` `FROZEN_BASE_CONTROLS = 55`, `:69` controls sha, `:70-72` held path/sha/count, `:74-77` `/59` denominators, `verdict_met :1385-1388`, `held_check :1411-1436` | **AGREE [O]** — my run: 20/13/13/0, controls 59/59, base 55/59, rc 0; held 47 compare byte-identically by `src`/expectations. |
| F13 | C2 D4 attribution | "`del env[k]` where `k` is bound exactly once **in the same scope** … to the guard key (a literal or a module constant)" (L135–137) | `keyed_names :382-399`; del branch `:478-490`; `key_is_guard(target.slice, consts)` `:486` | **DISAGREE** — for the `dynamic-key-module-const` control, `keyed_names` in `run`'s scope is `{}` (the binding is module-level) yet `classify` is `(True, False)` [O]: the case passes through the literal→module-constant widening of the **slice**, a rule the declaration does not name. Read literally, D4 predicts *guarded* for that case; the frozen control requires *unguarded*. |
| F14 | C2 D4 "exactly once" | "bound exactly once in the same scope" (L136) | `keyed_names :386-398` counts only `Assign`/`AnnAssign` with one `Name` target; `assigned_names :261-277` already counts `For`/`withitem` and is not used | **DISAGREE [O]** — `k = KEY` followed by `for k in ["PATH"]:` or `with open(...) as k:` leaves `keyed_names = {'k': 2}` and `classify = (True, False)`: the delete targets `PATH`, the guard stands, the census says unguarded. The frozen `dynamic-key-rebound` control only covers a second `Assign`. |
| F15 | C2 D3 argument binding | "cancels a guard on the mapping the caller hands to `f(env)`" (L133–135) | `cancelling_functions :402-435` returns only `fn.name` (`:434`); `call_cancellations :438-450` maps the **first positional `Name`** only (`:448-449`) | **DISAGREE (both directions) [O]** — (a) `def drop(env, m): del m[KEY]` + `drop(env, {…})` → `(True, False)`: over-cancel, `env`'s key is untouched; (b) `def drop(m, env): del env[KEY]` + `drop({…}, env)` → `(True, True)`: under-detect, the key **is** deleted from the caller's mapping; (c) `drop(m=env)` → `(True, True)`. (c) is disclosed by L139–141 ("positional first argument"); (a) and (b) are not. |
| F16 | C2 D3 scope | dominance = "the call line strictly between the guard line and the first launch use" (L134–135), read as scope-local | `call_cancellations` walks the whole tree (`:443`); the same map is merged into **every** scope's rebinds (`:610-611`, `:1021-1022`) | **DISAGREE [O]** — a nested helper that calls `drop(env)` on its own `env` between the outer guard and launch flips the outer guarded binding to unguarded (`nested-same-name` probe → `(True, False)`). No frozen control covers a second `env` binding. |
| F17 | C2 D3 flow coverage | "D3 is modelled in the env-named/subscript carrier flows, **not in the attribute flow**" (L141–142) | D3 wired only in `has_guard :575,:610-611` and `carrier_guard :987-988,:1021-1022`; absent from `guard_producers :523-546` (D4 present at `:533`), `attribute_flow :893` (consts not passed), `alias_store_guard :903-980`, `global_guard :1038-1127`, `environ_transport_guard :1140-1177`, `twohop_guard :1235-1292`, `environ_alias_guard :1318-1372` (own `cancels :1332-1339`, literal/const only) | **UNDER-DISCLOSED** — six flows besides the attribute flow lack D3; two lack D4's name binding. The limits name one. |
| F18 | C2 population half of the claim | "counts both shapes and keeps its population verdict" (L96–97) | `measure :1527-1541` re-derives 20/13/13/0 [O]; AST count: **0 `del` statements** across the 20 population files [O] | **EVIDENTIALLY EMPTY** — the number is correct and unchanged, but no population file can exercise D3/D4, so that half of the claim carries no information about the new rules; the 59 controls are the only discriminators. |

## Agreements worth recording (not disagreements)

- **A1.** C2 docstring/receipt shape matches the code and the declaration (47 held + 12 new = 59;
  `/59` denominators; `Exit 0 iff … 59 … 55`); `held_check` enforces the 47 carried byte-identically
  and the held file's pinned sha `d99502ba…` against the file **at the measured rev**.
- **A2.** C1 `outcome_green` is exactly the declared sentence (`green_with_witness(…) and killed == 2`,
  `c1-r76-landing-controls.py:146`), the contract row consumes it (`:230`), and the negative result
  ("killed == 2 already requires the echo") is sound: `killed == 2` requires the M-Z kill, and M-Z
  credit requires the echo (`:149-150`), so on reachable cases `green_with_witness` reduces to
  `summary_green` — an echo-dropping outcome rule cannot move `verdict=`. [O]
- **A3.** The R72 pin is real: `R72_SHA256 = b6108c86…` (`:63`) equals the sha256 of
  `quality/counters/c1-r72-landing-controls.py` at cb713254; the generation is written to a private
  `mkdtemp` under the validated scratch with `O_NOFOLLOW` (`:188-190`, `:207`) and loaded by
  `runpy.run_path` (`:210`).
- **A4.** Measurement revs differ and should be stated separately (R5): C1 at `cb713254` (freeze v2),
  C2 at `755b339f` (freeze v1); `c2-r76-shapes.py` is byte-identical across both commits
  (`git diff` = 0 lines), so the C2 receipt is valid for the frozen bytes but its header rev is not
  the declared freeze.

## What is NOT modelled (so the declared limits stay honest)

**C1**
- `witness=` and `killed=` are printed but **never scored** (`parse_row` captures `mz`, `verdict`).
  An echo-dropping rule is visible in `witness=` and invisible to the certificate — declared, and
  confirmed by F7.
- The candidate's **exit code is not read** (`harness_run` returns stdout; rc ignored at
  `c1-r76-outcome-field.py:365-367`, `:386-388`). The printed `verdict=` and the harness's own rc
  come from different paths (`outcome_green` vs r72 `outcome_exit`), so a rule that prints
  `TARGET_MET` and exits 1 scores as correct. Not in the limits.
- The challenge check is the candidate's **self-announcement** (F9), not an independent draw
  observation; the only real draw evidence is the harness's own selftest (200 draws, `:295-297`).
- G1/G2 are implemented but carry no weight in the frozen certificate (F7); the mutation set no
  longer includes the mutants that would need them.
- The fixture lanes are bash **test doubles**; the sixteen cases are rule separators, not fault
  coverage (declared). The r72 generation's internal correctness is assumed via the sha pin, not
  re-audited.
- The wrapper's selftest-only `_r72_credit` (`:378-393`) / `_r72_green` (`:396-406`) duplicate the
  loaded generation's `credit`/`summary_green`; the measurement uses the loaded copies, the selftest
  the duplicates. They agree today; drift would make the selftest assert about a different rule.

**C2**
- Line order is not execution order; values are not interpreted (declared).
- Callee matching is by bare `Name`, first positional argument only, no alias/chain (declared) —
  but the argument is not tied to the deleting parameter (F15) and the call map is tree-wide (F16);
  neither is declared.
- The callee's delete key is literal/module-constant (declared); the *same-scope* delete branch also
  newly accepts a module constant as the slice (F13), and "bound once" counts simple assignments
  only (F14).
- `attribute_flow` still receives no `consts` (`:893`), so module-constant delete keys and
  module-constant key names do not cancel there; the declaration mentions only the absence of D3.
- The population contains zero `del` statements (F18); D3/D4 are exercised solely by the controls.
- [I] The frozen `cancelling_functions`/`call_cancellations` conflate same-named functions (name-keyed
  map); no control exercises shadowed callee names.
