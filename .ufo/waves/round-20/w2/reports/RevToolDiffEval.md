# RevToolDiffEval — partly falsified: env/reset/exception mechanics of the diff hold, but the diff introduces one silent-drop (no row, no counter) regression for rebinding-shadowed dotted spawn calls, and one documented lead contract for dotted imports is not met (pre-existing)

Seat: MadoR20.RevToolDiffEval. Scope: `git diff f3da504 28c6837 -- tools/mado-tripwire.py`, restricted to `classify_eval`, binding environments (`prepare_eval_calls`/`update_bindings`/`binding_envs`), and `scan_file`, for unbound variables, state leaking across files, reset handling, and exceptions swallowed into clean verdicts.

## Method and baselines

- Clone: `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-RevToolDiffEval && git remote remove origin`; clone HEAD `a4046a8216080d4004de3f268c62cf142095ac07`.
- Blob identity: `git show 28c6837:tools/mado-tripwire.py | sha256sum` = `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`; worktree `sha256sum tools/mado-tripwire.py` = same. All probes ran the clone copy (never the lane worktree).
- Old reference: `f3da504:tools/mado-tripwire.py` → `/tmp/r20w2-RevToolDiffEval-probes/tw_old.py` (2128 lines; new 2612).
- Baselines run in the clone: `--selftest .ufo/waves/round-17/tripwire/core` → `CASE incident-replica ok`; `--selftest .ufo/waves/round-17/tripwire/compound` → `CASE compound-and-sudo-pacman ok`; `--frozen .ufo/waves/round-19/frozen` → `MADO_TRIPWIRE_FROZEN: frozen_match`, exit 0.
- All fixture `.jsonl` files are synthetic transcripts under `/tmp/r20w2-RevToolDiffEval-probes/fx/` (format: `{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","name":"eval","arguments":{...}}]}}`).

## Findings (by severity)

### F1 — MEDIUM (introduced by this diff): after a non-module rebinding of a spawn-alias head, a literal dotted spawn call produces NO row and NO counter — silent under-claim where f3da504 reported observed

- Behavior: `import subprocess as sp` → `sp.run('pacman -Syu', shell=True)` (observed) → `sp = mymod` → `sp.run('pacman -Syu', shell=True)`.
- Code path: `callable_info` resolves the head against bindings; a non-`module` binding returns plain unresolved without a name — tools/mado-tripwire.py:1487-1491 (`if bound.get("kind") != "module": return {"kind": "unresolved"}`). `spawn_scan`'s lead branch then requires `isinstance(node.func, ast.Name)` — tools/mado-tripwire.py:1874-1878 — but `sp.run` is an `ast.Attribute`, so the call is dropped with no lead and no `unparsed_spawns` increment.
- Evidence (new tool, 28c6837 bytes):
  `python3 -I /tmp/mado-r20w2-RevToolDiffEval/tools/mado-tripwire.py --scan fx/H.jsonl`
  → `"counts": {"host_mutation": 1, ...}` with findings only at `line: 2` (observed) and `line: 5`; `"unparsed_spawns": 0`, `"eval_unparsed": 0`; file sha256 `8a12d679b548a8f8081d5aab9b5b76622d7e6e15d2966b49f34378498406edfa`. The line-4 `sp.run('pacman -Syu', shell=True)` is absent from `findings` and from every counter.
- Counter-evidence that this is a regression, not the old baseline (command that shows the opposite): same fixture under f3da504 bytes:
  `python3 -I ./tw_old.py --scan fx/H.jsonl` → `"counts": {"host_mutation": 2, ...}` with findings at lines 2 **and 4** (old static alias table `aliases = {"sp": "subprocess"}`, tw_old.py:1340, flagged line 4 as observed host_mutation).
- Honesty comparison: the tool's own round-20 semantics treat an unknown-rebound BARE name's literal argv as a `lead` (header: "A literal positional `['prog', ...]` argv passed to an unresolved bare name or imported external callable is a `lead`"; suite case `S-CaseShadowing-print-imported` expects `evidence: lead` for exactly this rebinding shape). A dotted spawn whose callable became unknown is at least as suspicious, yet yields neither lead nor unparsed count. Old behavior over-claimed (observed); new behavior under-claims with zero trace; neither matches the tool's stated fail-visible philosophy.
- Severity framing: the argv is fully literal and shell-spawning, so nothing about the *finding rules* changed — only the call became invisible. [INFERENCE] real-transcript frequency of `sp = <unknown>`-style rebinding is low, which is why the 175-case precision suite (which covers the bare-name shadowing forms, e.g. `CaseShadowing/param-shadows-spawn-alias.jsonl`, and misses the dotted-after-unknown-assignment form) still scores 172/175.

### F2 — LOW (pre-existing at f3da504, unchanged by the diff; documented contract not met): a literal argv passed to a dotted call on an imported external module produces no lead and no counter

- Header contract (28c6837, tools/mado-tripwire.py:44-48): "A literal positional `['prog', ...]` argv passed to an unresolved bare name **or imported external callable** is a `lead`".
- Behavior: `import ext` → `ext.run(['pacman', '-Syu'])` → `from ext import run2` + `run2(['pacman', '-Syu'])`.
- Evidence (new tool): `--scan fx/F.jsonl` (sha256 `4982d214e5a4fd8891016b8f415b5bd207842021a8a4bc68ed9143847e89b1c8`) → exactly ONE finding: line 3, `evidence: lead`, `rule: pacman:-Syu` (the from-import form). The line-2 `ext.run([...])` row is absent; `"unparsed_spawns": 0`.
- Same result at f3da504: `--scan fx/F.jsonl` with old bytes → single finding at line 3 (old lead guard was equally `ast.Name`-only, tw_old.py:1431-1433). So the diff did not regress this; it is a live gap between the header text and both versions.
- Suite coverage gap: the wave-1 fixture `.ufo/waves/round-20/w1/patches/TwRuleB-dev-cases/imported-external-lead.jsonl` exercises only the from-import shape (`from audit_helpers import inspect as audit; audit([...])`), so the precision suite cannot see the dotted gap.

### F3 — LOW (behavior change of this diff, honest direction): deeper AST recursion consumption moves previously-clean inputs to `could_not_evaluate` (exit 2)

- `700`-term string concatenation cell (`S = 'a' + 'a' + …`, fx/Q700.jsonl, sha256 `7344bcdc38b78b375aa110866a0fadb886582adc5d406682024bd7b3d56fac63`):
  - f3da504: `MADO_TRIPWIRE: clean`, exit 0, `eval_unparsed: 0`, `unparsed_spawns: 0` (completed silently).
  - 28c6837: `MADO_TRIPWIRE: could_not_evaluate`, exit 2, `"error": "internal RecursionError"`.
- Crash frame (module imported via importlib, `scan_file` called directly): RecursionError frames end in `/usr/lib/python3.14/ast.py:506/510/516` (`NodeVisitor.visit`/`generic_visit`) — i.e. `eager_calls`' recursive `Visitor` (tools/mado-tripwire.py:1643-1683), one of the diff's new full-tree recursive passes (with `module_unsafe_names`' recursive `scan`).
- Assessment: NOT a fail-open — the entrypoint guard `except BaseException` → `could_not_evaluate` exit 2 (tools/mado-tripwire.py:2602-2611) is pre-existing (tw_old.py:2119-2127) and catches this. Old only "passed" Q700 because its shallower walkers stayed under the recursion limit. Net: the diff trades a false-clean for the contract's designed exit-2 on inputs beyond ~400–700 nesting terms (fx/Q400 clean, fx/Q700 exit-2 on this host). One previously-scannable transcript shape now fails the whole scan (availability), which is the contract's intended fail-closed outcome, but it is a real boundary movement worth naming in no-harm terms.
- Compile-level failures remain fail-visible, not swallowed: 1400-deep paren cell (fx/P1400.jsonl) → `clean` with `eval_unparsed: 1` on BOTH old and new (classify_eval's `except Exception: return hits, 1, 0`, tools/mado-tripwire.py:1788-1789).

### F4 — INFO (cosmetic, pre-existing): stale docstring on `classify_shell`

- tools/mado-tripwire.py:1008 documents "Return a list of (class, rule, argv0, segment_text, unparsed)" but `classify_segment.hit()` appends 4-tuples `(cls, rule + suffix, argv0, text)` (tools/mado-tripwire.py:1059-1060). `scan_file`'s `evidence = result[4] if len(result) > 4 else "observed"` (tools/mado-tripwire.py:2063) is therefore correct as written: shell-derived rows default to `observed`, only `helper_argv_leads` appends a 5th `"lead"` element. Identical docstring at f3da504 (tw_old.py:851). Unchanged by the diff; flag only so a future reader does not "fix" `scan_file` to match the docstring.

## Checks that held (no defect found)

- **Cross-file state leak: none.** fx/A.jsonl (defines helper `go` and literal `C = ['pacman', '-Syu']`) + fx/B.jsonl (`go('pacman -Syu')`, `subprocess.run(C)`) scanned in ONE invocation vs B alone: B's entry is byte-identical in both runs (sha256 `e1509de3f874020644d1158c9643587e25dfc80de0fabb389dc352283167f7a`, `unparsed_spawns: 1`, zero findings). `envs`/`binding_envs` are per-`scan_file`-call locals (tools/mado-tripwire.py:2011-2012); `NESTED` is the only module-level mutable and is zeroed per toolCall item (tools/mado-tripwire.py:2034).
- **Reset handling: correct.** fx/C.jsonl (sha256 `72f61ba74109cfc5b7d8429c194ffb0624d6b91d434c26494842669c227bcff4`): cell2 `subprocess.run(C)` → observed; cell3 (`reset: true`) same call → no finding, exactly 1 `unparsed_spawns`; cell4 helper-followed call → observed; cell5 post-reset `h(['pacman', '-Syu'])` → downgraded to `evidence: lead` (argv still stated, helper binding gone). Totals `observed_findings: 2, lead_findings: 1`. Reset clears BOTH environments (tools/mado-tripwire.py:2048-2050) and only for py-kernel cells, matching the fixture semantics.
- **Unbound variables: fail-visible, never crash.** fx/D.jsonl (`subprocess.run(MISSING_NAME)`, `subprocess.run(['pacman', X])`) → clean verdict with `unparsed_spawns: 2`. All env lookups are `.get(..., LITERAL_MISS)`; no NameError surface.
- **Exceptions never read as clean/findings.** Bad JSON line → `CouldNotEvaluate` exit 2; compile failure → `eval_unparsed` counter (P1400); internal RecursionError → `internal RecursionError` exit 2 (Q700). No path found where an exception yields a clean or findings verdict.
- **Dedup change is row-preserving.** New per-toolCall key `(cls, rule, evidence)` (tools/mado-tripwire.py:2064) vs old `(cls, rule)` (tw_old.py:1592): strictly finer, so an observed+lead pair for the same rule in one call now yields two rows where old kept one — no row loss vs f3da504.
- **Post-opaque pure-call lead (fx/G.jsonl) is intended, not a bug.** `print(['pacman', '-Syu'])` clean in cell 1; after `exec(s)` in cell 2 the same print yields `evidence: lead` (bindings cleared then PURE_ARG_CALLS re-seeded as unknown, tools/mado-tripwire.py:1752-1756). Matches header "exempt only while not rebound"; old was silent here (old cleared only the literal env, tw_old.py:1360) — a documented conservative tightening.

## Limits

- Host Python 3.14.8; the recursion boundary in F3 was measured only at {400 clean, 700 exit-2} granularity and is host/version-dependent [UNK].
- F1's practical weight depends on transcript frequency of alias-head rebinding to unknown callables [INFERENCE]; I did not mine live session transcripts (host pause: transcripts are data; the tripwire itself only parses them).
- The 175-case precision suite and the recall/frozen suites were not re-run here — those are sibling seats' named items; my probes are differential old-vs-new and supplementary to them.
- No `lsp` device is mounted in this session; per role rules I record that unavailability — findings rest on cited source lines and executed probes (text/grep fallback), not on a language-server answer.
- `fx/F.jsonl`'s `ext`/`ext.run` need not exist on disk; nothing in the scanned text is executed.

## Installs

none.
