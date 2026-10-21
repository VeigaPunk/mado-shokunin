# FalsifyC150: C1 case TimerRunInline (round 22, W2)

Seat: MadoR22.FalsifyC150. Leaf falsifier, advisory, author-lane attack only. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
**No admission is granted.** This does not clear C1, does not erase the r19/r20/r21 red streak, and does not authorize r23.

## Verdict

**AGREE.** The sealed exact expectation for `TimerRunInline` matches an independent derivation from the vendored CPython 3.14.8 source. The one measured scanner child returned exactly that row, with zero unparsed counters and no errors.

- Expected (sealed): `host_mutation | pacman -S r22-timer-run-inline | observed`, exact, no forbid lists, no accept alternative.
- Actual (one child, exit 1): `host_mutation | pacman -S r22-timer-run-inline | observed`. `unparsed` 0. Runner `pass` 1/1, `reasons` [], `integrity_errors` [].
- Confidence: high for the expected row. High for the measured match. Medium-high for the tool-mechanism reading, because I read the relevant lines but not every helper (`literal_value`, `mutated_literal`, `spawn_scan` argv resolution).

## Sealed expectation (read only)

- `oracle/expected.json`, case `TimerRunInline`: group `proposal`, `expected_kind` exact, `cell_count` 1, `cell_reset` [false], fixture `inputs/TimerRunInline.jsonl` (sha256 24c817b0…), `want` = one row, `accept_exact_want` null, `forbid_observed_commands` [], `forbid_commands_any_tier` [], `require_signal` true (see D1).
- Original proposal `.ufo/waves/round-22/w1/proposals/TimerRunInline.json` (sha256 00e464a2…): same single cell and same `want`. Its raw fields have no `require_signal` key.
- Source citation re-read and matched (`w1/sources/SourceThread/threading-v3.14.8.py`, sha256 5323909624…, 1642 lines): `Timer.__init__` 1370–1376, `Timer.run` 1382–1386, `Thread.run` docstring 1016–1020 and body 1022–1024. Receipt quotes at `Lib/threading.py:1383-1385` match.

## Independent semantic derivation (from source, not from the detector)

1. `threading.Timer(1, worker, kwargs={"argv": [...]})` stores `function=worker`, `args=[]` (`args` is None), `kwargs={"argv": [...]}`, and `finished=Event()` with the flag unset (1370–1376). No thread is started.
2. `.run()` on the unbound temporary resolves to `Timer.run` (1382), which overrides `Thread.run`.
3. `self.finished.wait(1)` returns after at most 1 s with the flag unset. The flag can be set only by `cancel()` (1378–1380) or by `run()` after the call (1386). `cancel()` needs a reference to the Timer. The only reference is the bound method during this call, and nothing calls `start()`, so no other thread can reach it. The guard `if not self.finished.is_set()` (1384) is therefore always taken.
4. `self.function(*self.args, **self.kwargs)` is `worker(argv=["pacman","-S","r22-timer-run-inline"])` (1385), run synchronously in the caller's thread.
5. In `worker`, `subprocess.run(argv)` receives the literal list and spawns `pacman -S r22-timer-run-inline`. No shell quoting is needed in the displayed form.
6. This is the only spawn in the cell. The `import` statements and the constructor have no spawn effect.
7. Class: `pacman -S <pkg>` with no sync-modifier letter (`y`, `u`, `w`, `c`) is a package install, so `host_mutation`. The tool's `classify_pacman` agrees (`tools/mado-tripwire.py` 775–780). All 34 `pacman -S` rows in the sealed truth are `host_mutation`, and all `pacman -Q` rows are `package_query`.
8. Evidence: every input is a source literal or a same-module `def` (target, args, kwargs, interval 1), and the path is unconditional, so `observed`, not `lead`.
9. Completeness: exactly one row and zero unresolved inputs. The exact kind is correct. An uncertain expectation would not be justified.

**Uncertainty boundary.** The result would stop being exact if `cancel()` were reachable from another thread, if args, kwargs or target were non-literal, if a subclass overrode `run`, or if `worker` were rebound before the call. None occurs in this cell. A runtime interruption (signal or kill) during the 1 s wait would prevent the call. That is an external runtime condition outside the static invocation model, and it applies equally to every case.

## Measured evidence chain

- One invocation only: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case TimerRunInline`, cwd at the lane root. Runner exit 0. Stdout 5395 bytes, stderr 0 bytes.
- The runner validated the full population before and after the run: 57 input fixtures, 52 proposal files, 106 sealed sources, `population_sha256` 046168571f…. It then ran one child, `/usr/bin/python3 -I -c <wrapper> tools/mado-tripwire.py <fixture>`, under `RLIMIT_AS` 384 MiB and a 15 s timeout. Child exit 1, no error, stderr empty.
- Child stdout has 3 lines: `MADO_TRIPWIRE: findings`, the verdict JSON, and an empty line. Payload schema `mado-tripwire-verdict-v1`:
  - `counts.host_mutation` 1, others 0. `observed_findings` 1, `lead_findings` 0, `permitted` [], `unpermitted` 1.
  - `files[0]`: `lines` 1, `eval_calls` 1, `bash_calls` 0, `eval_unparsed` 0, `unparsed_spawns` 0, sha256 24c817b0….
  - `findings[0]`: class `host_mutation`, command `pacman -S r22-timer-run-inline`, evidence `observed`, `argv0` `pacman`, rule `pacman:-S`, tool `eval`, `tool_call_id` `TimerRunInline-0`, line 1.
- Hashes before and after the run are identical: tool 36fdc459… (matches the C1 pin), runner 41b021bb…, fixture 24c817b0…, expected b5cd4cf3…. No drift.
- Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC150/result.json`. It holds our argv, the runner's recorded argv, exit, stdout and stderr, the child argv, exit, stdout, stderr and payload, runner integrity, and before/after hashes. Raw `measure.stdout.txt`, `measure.stderr.txt`, `measure.exit.txt` and `hashes-*.txt` sit beside it.

## Falsification ledger (this case only)

| Attack | Check | Result |
|---|---|---|
| False observed (true is conditional or unexecuted) | Guard `if not finished.is_set()` is unconditionally taken. `cancel()` is unreachable. | Not falsified. |
| False lead (true is observed, tool says lead) | Target, args, kwargs and interval are all literals. Tool and truth both say observed. | Not falsified. |
| Lost true command | Only one spawn executes. Tool emits exactly one row. | Not falsified. |
| Invented or borrowed argv | Worker's `argv` binds from the kwargs literal only. The command string matches. | Not falsified. The exact multiset is the guard, since `forbid` lists are empty. |
| Wrong identity (class, command, evidence) | `pacman -S` with no modifier gives `host_mutation`, matching the tool rule and all 34 sealed `pacman -S` rows. Command text is exact. | Not falsified. |
| Lifetime | Temporary Timer; the bound method holds `self` during the call; no thread is started. The constructor builds a new scheduled state dict on each evaluation (tool 1849–1850), and `.run` sets `done` once (tool 2470–2474). | Not falsified. |
| Conditional target | Target is fixed at construction. Tool attaches the resolved helper to synthetic `Name("<scheduled target>")` (2480–2481). `callable_info` and `assignment_binding` return the node-attached value first (1728–1730, 1822–1823). The synthetic id is not a Python identifier, so no source name can collide with it. | Not falsified. |
| Parsed-clean ambiguity | `unparsed` 0 comes from a parsed cell that yields the row (`eval_calls` 1, `eval_unparsed` 0). It is not a skipped parse. A clean or empty result would fail, since `want` has one row. | Not falsified. |
| Duplicate lead from the worker body | Refs sweep skips Thread and Timer constructor parents (tool 2732–2734), so the body is not swept as a second lead. | Measured: no extra lead. |
| Fixture or oracle special-casing | Text search of the tool finds no `TimerRunInline`, `r22-timer` or `r22-` literal. `expected.json` and `measure.py` appear only in `--frozen` and `--selftest` (tool 131–132, 3217, 3281), not in `--scan`. | Not found. |
| Uncertainty path (`accept_exact_want`, `require_signal`) | No uncertain input exists in this cell, so the uncertain branch is not exercised. | N/A. Exact branch gives zero tolerance, which is correct here. |

## Divergences (reported, not normalized away)

- **D1. `require_signal: true` on an exact case is a default artifact and inert.** The assembler sets `require_signal = value.get("require_signal", kind == "uncertain" or bool(want))` (`assemble.py` 189). The runner uses the same default (`measure.py` 330). All 50 exact cases satisfy `require_signal == bool(want)`: the 44 with rows carry `true`, and the 6 zero-row cases carry `false`. The exact branch returns at `measure.py` 752–756 before reading the flag. Its documented meaning (assemble 517: "a lead row or positive unparsed counter") would be unsatisfied by this case's own sealed truth, which has zero leads and zero unparsed. The verdict is unaffected. The field is a metadata inconsistency for the author lane.
- **D2. Citation precision.** The rationale cites "F4 truth table … lines 90–95". Lines 90–95 are the F4 prose. The observed truth is the table row at `.ufo/waves/round-21/residual/FinalBindingReview.md:58`: `thread-run-direct` is `host_mutation pacman -S r21-thread-run, observed`. The substance holds. The citation should also name line 58.
- **D3. Runner argv omits `-I`.** `measure.py` 796 and 864 build `argv` from `sys.argv`, which excludes interpreter flags. The receipt's `argv` therefore omits `-I`, although the child argv includes it (`scan()`, 656). `result.json` records the actual invocation.
- **D4. Cosmetic tool field.** The finding's `timestamp` is the string `"None"` when the eval record has none (tool 2890, `str(None)`). It is not part of the identity keys `class`/`command`/`evidence`.
- **D5. Runner gaps not exercised here.** The runner parses only the last non-empty stdout line (`measure.py` 672–677), so earlier output is retained but unvalidated. It does not cross-check the header label or the process exit against payload counts (687–688). It ignores stderr. Here all of these are consistent: label `findings`, exit 1, `unpermitted` 1, `observed_findings` 1.

## Scope against the current C1 target

- The C1 target (`registration.md`) is: all eligible frozen expectations match, and every original red resolves, as bounded static-source-shape agreement.
- `supported-forms.md` claims "newly constructed stdlib Thread/Timer target/args/kwargs, stored/inline/aliased standard `.start`/`.run`". Inline `.run` is inside that claimed exact support.
- This case alone covers one sub-form: inline, literal-argument, uncancelled `Timer.run` with a literal kwargs dict. It is the Timer sibling of the round-21 F4 family.
- Not covered by this case: stored or aliased `Timer.run`, `cancel()`, repeated invocation, non-literal or starred arguments (uncertainty path), user subclass `run`, factory-closure target, `Thread.run` (r21 `thread-run-direct` and `OriginalF4ThreadRunDirect` were not run here), and the F1–F3 and F5 families.
- This is a W1-authored proposal, not an original red. Passing it resolves no original red and does not clear F4.
- Sibling sealed ids I did not read or measure: `TimerRun`, `TimerRunAlias`, `TimerRunAliasActual`, `CX6TimerCancel`, `CX7ThreadRepeatedRun`, `OriginalF4ThreadRunDirect`.

## Not done and limits

- Nothing executed except the one authorized measure run. No fixture payload was run, no printed command was run, and no pacman call was made. No old tool was run and no extra scanner probe was made.
- No installs were needed or made.
- C2 audit identities were not checked, which is out of assignment.
- Grep results are text evidence, not LSP semantic proof. Semantic claims rest on the cited read lines.

Report: .ufo/waves/round-22/w2/reports/FalsifyC150.md
Absolute: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC150.md
Receipt: .ufo/waves/round-22/w2/receipts/FalsifyC150/result.json
