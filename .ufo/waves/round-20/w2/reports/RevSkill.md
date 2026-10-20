# RevSkill — partly falsified: two subsection claims overstate the scanner contract; the scored suite has three contrary expectations

## Findings

### P2 — Lead rows do not unconditionally imply exit 1

`SKILL.md:549` says “Leads stay in `findings` (exit 1)” without the unpermitted-class condition. The 28c6837 implementation retains rows, but `verdict_of()` returns 0 when every finding's class is permitted (`tools/mado-tripwire.py:2090-2095`); `run_scan()` emits the findings and evidence totals in that case too (`:2113-2120`). The registry already exposes `--permit CLASS` at `SKILL.md:594`. Narrow this to the default/unpermitted case, e.g. “leads remain in `findings`; exit is 1 if any is unpermitted, otherwise 0 (`permitted_only`).” Tool SHA-256: `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.

I did not run a direct `--permit` scan: the current host-pause instruction forbids it. This finding is established by the canonical verdict path above.

### P2 — “pure stdlib callables” exceeds the implementation's explicit allowlist

`SKILL.md:552-554` promises no row for “builtins and pure stdlib callables” except when rebound. The tool's contract is narrower: builtin names in `PURE_ARG_CALLS`, stdlib modules in `PURE_STDLIB_MODULES`, and exact paths in `PURE_STDLIB_EXACT` (`tools/mado-tripwire.py:1396-1423`); its docstring correctly says “listed pure stdlib callables” (`:45-46`). A scan-only counterexample using an unlisted but pure stdlib alias demonstrates the difference:

```
python3 -I /tmp/mado-r20w2-RevSkill/tools/mado-tripwire.py --scan /tmp/mado-r20w2-RevSkill/pure-stdlib-unlisted.jsonl
MADO_TRIPWIRE: findings
... "class": "package_query", "evidence": "lead", "rule": "pacman:-Q" ...
"exit": 1, "lead_findings": 1
```

The fixture imports `copy.copy` and passes it a literal list. [INFERENCE] For this built-in list input, `copy.copy` only produces a shallow copy; it does not spawn the stated command. Fixture SHA-256: `383ab685c7cca5644486eb1e6bc8a8220fa477bdba31567af53e24579c2c8e97`. State that only the known/allowlisted pure callables are exempt; the R20 P-family suite (66/66) exercises its listed cases, not this wider promise. Tool SHA-256: `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.

### P2 — The lead definition needs an explicit reachable-call-path boundary

`SKILL.md:548-550` defines a lead as literal host argv handed to an opaque callee, but does not repeat the requirement that the call be on a statically identified path. The scored case `L-AdoptW2-AdvHelperFn-b14` expects a lead from a function body that is never called: its only fixture line defines `run_all(run_case)` and places the argv inside that body (`precision/CaseAdoptW2--AdoptW2-AdvHelperFn-b14.jsonl:1`; SHA-256 `118b0136e43d282ddffabafee2d13880ac63e60b9facd3453a000cd089052c7a`). At 28c6837 the counter returns exit 0/no findings for this case, consistent with the tool docstring's explicit “Uncalled helpers do not establish an execution path” (`tools/mado-tripwire.py:35-41`) and the `eager_calls`/`spawn_scan` path (`:1643-1671`, `:1810-1847`). Clarify that a lead, like an observed row, requires a reachable call path; otherwise this case's expected lead contradicts the intended contract.

## Sentence-by-sentence check

- `SKILL.md:544-545` — **holds for `--scan` findings**: every emitted finding row gets `evidence` (`tools/mado-tripwire.py:2060-2075`); the 28c6837 scored counter validates/compares the marker (`tw-precision.py:77-105, 188-200`). Tool SHA-256 is `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.
- `:545-548` — **holds with the resolver's stated bounds**: shell/eval and statically resolved visible helpers are classified; earlier Python eval cells carry bindings until reset. The tool caps helper traversal at four nested calls, requires an awaited async helper, and excludes uncalled helpers (`tools/mado-tripwire.py:35-41, 1732-1796, 1810-1847`). The R20 results do not mean arbitrary helper dispatch is covered.
- `:548-551` — **partly holds**: the 28c result retains a literal-argv opaque-call lead, and the recall split confirms the example's 5 observed + 1 lead; however, the lead needs a reachable call path (P2 above), and exit 1 needs the unpermitted qualifier (P2 above). `tw-recall.py` at 28c returned `incident_lines: 6, detected: 6`; `tw-recall-split.py` returned `detected_observed: 5, detected_lead: 1, detected_unmarked: 0, undetected: 0`, and `control_lines: 20, control_findings: 0`. Both commands used the `/tmp` clone and revision `28c68378eccbd5f227cdc28a62406ff390e3540a`; tool SHA-256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.
- `:552-554` — **partly falsified** by the finite purity allowlist and `copy.copy` scan above. `del` restoring a shadowed builtin is consistent with the R20 `S-CaseShadowing-del-print-restores-builtin` case; it is not a general statement about Python local-scope `del` semantics.
- `:554-560` — **classifier behavior holds for the listed VCS forms**, with explicit exceptions. The code's Git/JJ help and dry-run parsing is at `tools/mado-tripwire.py:578-611, 640-686`; the H family passes 51/52. One scored case contradicts this behavior: `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` expects clean for `jj $c --help`, but the fixture contains no `$c` binding (`precision/CaseAdoptW2--AdoptW2-RerunPrecision-corpus-jj-var-verb-help.jsonl:1`; SHA-256 `047d96a1e5d8578f9a66f784f89c7faf24dbadcb986fb7aae34c842cebb548f2`). The 28c scanner returns `vcs_write` / `jj:$c` for this unknown variable verb, as the subsection says. The external note “c=describe” is not in the scanned fixture, so the clean expectation is not established by this case.
- `:560-563` — **holds as a measurement/limit, not a pass claim**. `python3 -I /tmp/mado-r20w2-RevSkill/.ufo/waves/round-20/tw-precision.py 28c68378eccbd5f227cdc28a62406ff390e3540a` reported 172/175 (score 9.8286): P 66/66, S 17/17, W 21/22, H 51/52, L 17/18. The three non-passing expectations are `W-CaseWrapperForms-class-method-instance`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`, and `L-AdoptW2-AdvHelperFn-b14`. The first expects clean for `Runner().run([...])`, but 28c follows a directly resolved visible class method and emits `observed`; the docstring says such methods are followed (`tools/mado-tripwire.py:38-41`, implementation `:1451-1483`). Its fixture and expected row are `precision/CaseWrapperForms--class-method-instance.jsonl:1` and `precision/expected.json:1312`; fixture SHA-256 `e9162d138c3560b430b7cfe58061cc206fc6c8c95c7f771a9b67579810ee4135`. Thus the 172/175 is measured honestly, but the three suite expectations are not a 175/175 confirmation of the prose.
- `:565-571` — **holds for the tested harness**. Ran `bash /tmp/mado-r20w2-RevSkill/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-RevSkill/.ufo/waves/round-20/isolate.sh`. It printed `FAIL_CLOSED` for mount-nonzero, unshare-refused, mount-noop, partial-arm, missing-target and missing-stub; each canary was absent. The positive control printed `harness exit: 0; canary=present` and `POSITIVE_CONTROL_OK isolate.sh`; the command returned successfully. Script SHA-256s: `isolate.sh` `332b3fed6ad680f0bd2eec35ff686b768e2619a828925f13d429807a817fcccc`; `isolation-check.sh` `2bf115db1658df32d5e89e600ad6ef47c0e2855beda5f25dfc936270604f6aa9`. The non-sandbox warning is consistent with the harness: it requests private mount/user namespaces but does not isolate the environment or compositor/session sockets.

All 11 existing `--selftest` suites were run from `/tmp/mado-r20w2-RevSkill` using `tools/mado-tripwire.py` at SHA-256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`: round-17 core 9/9, compound 16/16, hardening 33/33, w2-regressions 30/30; round-18 frozen 31/31 and r18-failsafe 1/1; round-19 r19-bashcvar 45/45, r19-helperfn 34/34, r19-vcs 17/17, r19-frozen-f1f2 13/13, and r19-installers 18/18; total 247/247.

## Older SKILL text now false or needing qualification

- `SKILL.md:530-531` — “A finding is an issued command” is false for `evidence: lead`: the row says an opaque callee received literal host argv, not that the host command ran. `:532-534`'s instruction to confirm package transactions also needs to apply only to observed evidence; a lead is not evidence of a transaction. The newer `:548-551` wording correctly forbids describing a lead as a command that ran.
- `SKILL.md:594` — the `mado-tripwire` row's `...python eval !/%%bash/literal spawns only` is stale: visible-helper paths and spawn aliases are now resolved. Its exit-1 map is also stale because it lists only `host_mutation/package_query/live_probe`; the 28c docstring lists five classes, including `tool_install` and `vcs_write` (`tools/mado-tripwire.py:7-8`).
- `SKILL.md:621-627` — `:622-623`'s unqualified “records commands issued” inherits the lead problem above. `:627`'s blanket “shell functions/aliases ... are outside it” is false for shell functions defined and called in the same scanned text (tool docstring `:35-41, 56-57`; `r19-helperfn` passed 34/34); unbound aliases and cross-text shell-function definitions remain outside the stated coverage.
- `SKILL.md:607` (`mado-tw-recall`) is **not literally false**: the pre-registered counter still computes 10 × detected / 6 and counts a line if it has any finding (`.ufo/waves/round-19/tw-recall.py:12-15, 73-85`). It is incomplete as evidence of execution, however: at 28c, 6/6 was 5 observed + 1 lead. The new sentence at `SKILL.md:550-551` supplies the necessary qualifier; cite the split counter whenever reporting the 6/6.

## Limits

- The LSP device is not mounted: `read xd://lsp` returned “No such tool”; used static `read` and literal `grep` only after recording that unavailability. Grep results were used as locators, not semantic proof.
- All executable checks ran in the isolated `/tmp/mado-r20w2-RevSkill` clone at HEAD `a4046a8216080d4004de3f268c62cf142095ac07`; the reviewed classifier bytes match 28c6837 by SHA-256. No direct `--permit` invocation was made due to the host-pause rule. The extra copy fixture was scanned as data only.
- The lane working tree was already dirty at start (`M .ufo/waves/round-20/w1/reports/SimplifyRuleB.md`, untracked `gen_w2.py` and `w2/`); I changed no tracked lane file and wrote only this report in the lane.

## Installs

None.
