# SimplifyFinal — holds: 28c6837 reproduces 172/175 and 247/247, and its round-20 weight includes 23 measured-deletable net lines plus ~85–100 unmeasured duplicated lines; no constant is unused, but `REDIRECTS` is inert and the spawn-kind gate never fires on 1,292 fixtures

Item: list dead code, duplicated logic and unused constants in `tools/mado-tripwire.py` at
`28c6837`, estimate deletable lines, no edits. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`
at `a4046a8`; tool bytes at `28c6837` are `sha256 9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`
(2612 lines), identical to the claim's pin.

All measurements below come from a scratch clone (`git clone -q <lane> /tmp/mado-r20w2-SimplifyFinal`,
origin removed). The lane worktree was not edited: `git status --porcelain` there shows only other
seats' files (`.ufo/waves/round-20/w1/reports/SimplifyRuleB.md`, `gen_w2.py`, `w2/`), and
`sha256sum tools/mado-tripwire.py` still prints `9613f510…`.

## Baseline I reproduced (would have shown the opposite if the claim were wrong)

```
$ cd /tmp/mado-r20w2-SimplifyFinal && python3 -I .ufo/waves/round-20/tw-precision.py 28c6837
{"commit": "28c68378…", "families": {"H": {"passed": 51, "total": 52}, "L": {"passed": 17, "total": 18},
 "P": {"passed": 66, "total": 66}, "S": {"passed": 17, "total": 17}, "W": {"passed": 21, "total": 22}},
 "score": 9.8286, "rev": "28c6837", "tool_sha256": "9613f510…"}
fails: W-CaseWrapperForms-class-method-instance, L-AdoptW2-AdvHelperFn-b14,
       H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help
```

172/175 scored. The 11 `tripwire/*/expected.json` suites run in `harm-watch.sh`'s sweep total
**247/247** at 28c6837 (16+9+33+30+31+1+45+13+34+18+17, all `failed=[]`). `--heldout` is 0/12, and
`precision-heldout/expected.json` says why: every case is `EDGE (outside the TwRuleB/TwVcsHelp patch
scope)` and `red at 9c54c56 too` — the held-out set is declared out of scope, so 0/12 breaks no claim.

Round-20 cost: the tool grew `2128 → 2612` lines for the repair (`git diff --stat 1f7f995 28c6837
-- tools/mado-tripwire.py` → `710 insertions(+), 226 deletions(-)`). Weight was added much faster
than removed; the audit below is what a simplifier would take back out.

## A. Dead code — six candidates, each measured behavior-neutral

I built one mutant per candidate as a commit in the clone, then re-ran the 11 suites and the
175-case precision counter, plus a per-file equivalence over **all 1,292 `.jsonl` fixtures** under
`.ufo/waves` (findings rows for every mutant — all seven runs produced result digest `c70b171ceb6fa2fc…`, 0
differing files; findings **and** both unparsed counters for the whole-gate variant and for the
combined branch, also 0 differing files). Combined branch `a5424c1` is 2589 lines,
`28 insertions(+), 51 deletions(-)`, pyflakes-clean, suites 247/247 and precision 172/175 unchanged.

| # | anchor (28c6837) | what is dead | net lines | mutant | why it is dead |
|---|---|---|---|---|---|
| S1 | `tools/mado-tripwire.py:146`, `:382` | `REDIRECTS` set, and the `tok in REDIRECTS or` disjunct | −1 (2−,1+) | `dd1b54a` | every member is `< > & \|` only, so the generic clause `set(tok) <= set("<>&|")` on the same `elif` already catches it; both branches run the identical `skip_next = …` (`:383`) |
| S2 | `:1879-1887` | `tail`, `is_sub`, and the `or is_sub or is_shell_fn or is_exec or is_tool` gate | −4 | `cc45396` | the disjunction cannot change the branch: `kind == "spawn"` already makes it true (`spawn_path`, `:1426-1431`), and for the only other kind that reaches here (`instance`, a called object whose class has no `__call__` — `name` is then absent) all four predicates are false, so the effective test is `kind != "spawn"`; the two `continue` blocks above it cover the remaining kinds (`:1871`, `:1872-1878`). `is_shell_fn` (`:1934`), `is_exec`, `is_tool` stay (used later) |
| S3 | `:1810-1811`, `:1818-1819` | `env`/`bindings` params of `spawn_scan` and the `call_env is None` / `binding_env is None` fallbacks | −1 (9−,8+) | `a0ded54` | all three `spawn_scan` calls pass the snapshot maps (`:1793`, `:1842`, `:1866`), so the fallbacks never run; `env`/`bindings` exist only for them |
| S4 | `:159` (vs `:157-158`) | second hand-written jj option table | −1 (2−,1+) | `17e4466` | `JJ_SUB_ARG_OPTS` = `JJ_ARG_OPTS ∪ {-r/--revision}` minus `--config-toml`; a derived set removes the copy (semantics of the `--config-toml` delta: [UNK], see Limits) |
| S5 | `:2106-2111`, `:2567-2572`, `:2580-2585`, `:2587-2592`, `:2606-2611` | five literal copies of the `could_not_evaluate` verdict object | −11 (25−,14+) | `68bfae3` | one 7-line builder reproduces every copy; byte-identical stdout on all five error paths (`cmp` on usage / `--scan` / bad `--permit` / unreadable path / permit-without-path), and `json.dumps` of the builder equals the old literal byte-for-byte for the `__main__` handler too |
| S6 | `:1475-1483` | the `instance` and `class` arms of `callable_info`'s attribute branch | −5 (9−,4+) | `d58c559` | the two arms are textually identical (`class_method_info(class_info.get("node"), node.attr)`); merging with the `class_info is not None` guard preserved gives the same result |

Evidence excerpts (baseline vs mutant):

```
$ for b in ...; do git diff --shortstat 28c6837 $b; done
m-redir       1 file changed, 1 insertion(+), 2 deletions(-)
m-gate        1 file changed, 2 insertions(+), 4 deletions(-)
m-nogate      1 file changed, 4 deletions(-)
m-jj          1 file changed, 1 insertion(+), 2 deletions(-)
m-payload     1 file changed, 14 insertions(+), 25 deletions(-)
m-callarms    1 file changed, 4 insertions(+), 9 deletions(-)
m-scanparams  1 file changed, 8 insertions(+), 9 deletions(-)
m-all (a5424c1) 1 file changed, 28 insertions(+), 51 deletions(-)   -> 2589 lines
```

Caveat recorded honestly: deleting the whole S2 gate (`m-nogate`, 4 deletions) also produced zero
corpus differences, but it removes a guard that is *theoretically* live for `instance(...)` calls whose
class has no `__call__` (that call would raise `TypeError` at runtime); deleting the guard would
[INFERENCE] let such a construct increment `unparsed_spawns`. Deleting only the impossible
disjunction (`m-gate`) is the safe form of S2.

## B. Duplicated logic (estimates are [INFERENCE] unless a mutant is named)

1. **Five copies of "walk argv, skip option values, yield positionals"** — `verb_index`
   (`:527-540`, 14 lines, *new in round 20*), `first_verb` (`:543-545`, 3, pure wrapper),
   `sub_verb` (`:548-565`, 18), `leading_tokens` (`:895-913`, 19), `has_operand` (`:916-931`, 16).
   70 lines for one loop; one generator plus thin wrappers ≈ 25 lines, **≈ −40 net** [INFERENCE].
   Drift already present: `--` is skipped as a flag by `verb_index`/`sub_verb`, stops iteration in
   `leading_tokens`, and returns `i + 1 < len(args)` in `has_operand`; no comment owns that choice.
2. **Two enumerations of the same rebinding AST forms** — `module_unsafe_names` (`:1307-1359`) and the
   `visit()` cascade inside `update_bindings` (`:1603-1640`). One `(node → bound names)` extractor
   would serve both: **≈ −25 net** [INFERENCE]. This duplication has already drifted: the new
   `update_bindings` has no `ast.TypeAlias` branch, while `module_unsafe_names` does
   (`TYPE_ALIAS` occurs only at `:1222` and `:1354`) — see D2.
3. **Four hand-rolled quote state machines** — `strip_comment` (`:335-355`), `substitutions`
   (`:390-422`), `last_unquoted` (`:739-758`), and the scan loop of `shell_expand` (`:850-892`).
   `strip_comment` and `last_unquoted` are the same algorithm with a different exit; a shared
   scanner is **≈ −15…−25 net**, medium risk because `substitutions` adds `$( )` nesting and a
   `line.count('"') % 2` heuristic that a naive merge would change.
4. **The spawn-path set encoded twice** — `spawn_path` (`:1426-1431`) vs the inline
   `is_shell_fn`/`is_exec`/`is_tool` predicates (`:1882-1885`). After S2 the gate use is gone; a
   `(kind, shape)` return from one predicate would remove the rest: **≈ −2…−4** [INFERENCE].
5. **Small duplicated authorities** — help flags `("-h", "--help")` inline at `:648` while
   `JJ_HELP_FLAGS` exists at `:160`; the `python[0-9.]*` regex twice (`:1036`, `:1098`); and
   `GIT_DRY_NEGATIONS["commit"]` (`:204-207`) re-listing the exact tokens already enumerated at
   `:664-670`. Deriving each saves **≈ −5** total, all three *introduced or co-introduced in round 20*.

## C. Constants: none unused; four redundant-by-construction, one conflicting pair

- `pyflakes 4.0.3` on 28c6837, on all seven mutants, and on the combined branch: **no output** (no
  unused import, no redefinition, no undefined name). `vulture 2.16 --min-confidence 100`: **no
  output**; at `--min-confidence 60` only the three `shlex` attribute setters in `tokenize`
  (`:361-363`), a known false positive. A manual reference count over all 59 module-level constants
  found **no constant with only its definition** (minimum count 2).
- Redundant: `REDIRECTS` (`:146`, measured inert, S1); `JJ_SUB_ARG_OPTS` (`:159`, duplicate of
  `JJ_ARG_OPTS`, S4); `GIT_DRY_NEGATIONS` commit tuple (`:204-207`, duplicated literals);
  `JJ_HELP_FLAGS` (`:160`, duplicated literal).
- Conflicting authorities: `PURE_ARG_CALLS` (`:1396`) and `OPAQUE_PY_CALLS` (`:1217`) both contain
  `compile`, `eval`, `exec`, `setattr`, `vars` — the first says "does not execute a command", the
  second forces `env.clear()`/`bindings.clear()` at `:1745-1746`. Deliberate, but announced nowhere;
  a reader cannot tell which meaning wins. No lines deletable.

## D. Two live consequences the duplication audit surfaced (not part of the author's claims)

**D1 — `git stash -m …` is a missed `vcs_write` (left by round 20, identical at 1f7f995:527).**
`sub_verb` (`:548`) always skips values from the jj table, but `classify_git` uses it for `git stash`
(`:682`), so the message argument is read as the stash sub-verb. Probe (canary transcript in `/tmp/probe`,
`python3 -I /tmp/tw-base.py --scan …`):

```
git stash                 -> MADO_TRIPWIRE: findings  [('vcs_write', 'git:stash')]
git stash push -m list    -> MADO_TRIPWIRE: findings  [('vcs_write', 'git:stash')]
git stash -m list         -> MADO_TRIPWIRE: clean     []
git stash -m show         -> MADO_TRIPWIRE: clean     []
```

`GIT_VALUE_OPTS["stash"]` (`:183-184`), added by round 20, already lists `-m`/`--message`; passing
that table into `sub_verb` fixes it without new code. This is a detector false negative, not dead
code — flagged because it is the direct cost of the duplicated option tables.

**D2 — a stale binding after `type X = …` (round-20-introduced duplication drift).**
`update_bindings` (`:1552`) lacks the `ast.TypeAlias` branch that `module_unsafe_names` has, so a
prior binding survives. Probe (Python 3.14.8):

```
code: import subprocess as X\ntype X = int\nX.run(["pacman","-Syu"])
-> MADO_TRIPWIRE: findings [('host_mutation', 'pacman:-Syu', 'observed')]
```

`X` is a type alias by then, so `X.run` cannot reach pacman; the row is a false positive that the
fix (add `TypeAlias` to the shared extractor of B2) removes. Rare construct, low severity.

## Totals

| bucket | net lines | status |
|---|---|---|
| S1–S6 combined (`a5424c1`) | **−23** (51 deleted, 28 inserted; 2612 → 2589) | measured: 172/175 same pass-set, 247/247 same, 1292/1292 same findings+counters |
| B1 walkers | ≈ −40 | [INFERENCE], not mutant-tested |
| B2 binding cascades | ≈ −25 | [INFERENCE]; also fixes D2 |
| B3 quote scanners | ≈ −15…−25 | [INFERENCE], medium risk |
| B4 path predicates | ≈ −2…−4 | [INFERENCE] |
| B5 small authorities | ≈ −5 | [INFERENCE] |
| **plausible total** | **≈ −110…−122** | of which only −23 is proven neutral |

Round 20 added 484 net lines; the tool at 28c6837 carries at least the measured 23 lines that can be
deleted with zero observable change, and roughly 85–100 more that a careful unification would take.

## Limits

- Behavioral equivalence, not proof: S1/S2/S3/S4/S5/S6 and the combined branch were compared on the
  175 scored cases, the 247 selftest cases, and the 1,292 fixture files under `.ufo/waves`
  (findings rows and both unparsed counters). A construct absent from all fixtures could still
  distinguish them; S2's guard is the one I found (see A).
- I did not run the isolation check, the recall counters (`tw-recall.py`, `tw-recall-split.py`), the
  frozen replay, the tally check, or the 20 control lines — other wave-2 items own those. My corpus
  set includes the frozen snapshot inputs but does not validate `--frozen`.
- S4's semantic delta (`--config-toml` accepted after a jj subcommand?) is [UNK]: no jj invocation is
  permitted here (host pause / no jj command), so the derived set is measured neutral but not proven
  correct. The union is the direction the existing set already implies; a conservative alternative is
  to keep `--config-toml` out explicitly.
- B1–B5 line estimates are [INFERENCE] from spans (`ast` start/end lines) and are not
  mutant-tested. S2 and S3 were revised downward after measurement (S2's gate guard is live in
  theory; S3's parameter removal saves only the fallback lines), and S6's merge needed its `None`
  guard restored, so it saved less than the two arms span (measured −5).
- No web source was opened, so no fetch receipts.
- The lane's `w2/` tree is shared with other seats; I wrote only this report.

## Installs

- `pyflakes 4.0.3` via `uv tool install pyflakes` — reason: unused-import / undefined-name / redefinition
  check on the target and on every mutant (`uv tool` is permitted under the host pause).
- `vulture 2.16` was already present (`uv tool install vulture` → "`vulture` is already installed");
  not installed by me.
- No pacman/sudo/systemctl or any paused channel was used.
