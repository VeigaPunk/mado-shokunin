# R74RevC2 — C2 adversarial review

Axes: operability (C2), calibration (C1, held here), navigation and ledger/no-harm (unchanged). This review probes operability without changing any scored artifact or denominator.

## Findings, ordered by severity

### P1 — New environment-alias flow mistakes a shadowing parameter for the module alias

`quality/counters/c2-r74-shapes.py:1118–1131,1159–1194` builds one module-wide name table and walks every function without resolving lexical bindings. `08_parameter_shadow.py:4–9` binds/stores the module `env`, then launches with `dict(env)` inside `def launch(env)` called with `{}`. Observed `classify=(True, True)`; held classifier `(True, False)`; `environ_alias_guard=True`. The child receives the empty argument, not the guarded module environment. This is a new false accept, not the disclosed cross-method execution-order approximation: the parameter denotes a different object regardless of call order. Resolve the parameter's lexical identity before accepting it as the one-hop alias.

### P2 — Annotated rebindings evade the new exactly-once/rebinding checks

`object_alias_map:1046–1056` and `environ_alias_names:1122–1131` count only `ast.Assign`; `ast.AnnAssign` is invisible. `16_environ_annotated.py:4–7` stores the guard, executes `env: dict = {}`, then launches with `dict(env)`: observed `(True, True)`, held `(True, False)`, `environ_alias_guard=True`. This directly violates the frozen exclusion of alias rebinding (declaration:73–75) and creates a new unsafe false accept.

`14_annotated_rebind.py:4–7` similarly accepts `r: object = other` between store and `env=r.env`; held also accepts via its same-spelling attribute path. `15_annotated_cross.py:4–7` proves the new two-hop path itself ignores the annotation: `twohop_guard=True`, candidate accepts, held rejects. The latter remains semantically guarded through `cfg.runner.env`, but violates the conservative exactly-once alias rule; distinguish this contract overaccept from the unsafe `16` case. Count all binding forms relevant to the declared once-bound invariant.

### P2 — Alias canonicalisation has no binding-time check

`object_alias_map:1042–1056` drops alias binding lines; `canonical_dotted:1059–1066` rewrites every occurrence; `twohop_guard:1089–1114` checks only store-to-launch order. `13_late_alias.py:4–6` stores into pre-existing `r.env`, then sets `r = cfg.runner`, then launches with `cfg.runner.env`. Observed `(True, True)`, held `(True, False)`, `twohop_guard=True`. The earlier store need not have touched `cfg.runner.env`. This is a new semantic false accept on straight-line source, not a cross-method scheduling ambiguity. The frozen sentence does not separately spell out bind-before-store, so this is an alias-identity/dominance defect rather than a claim that its literal store-before-launch clause failed. Retain binding lines and require the edge to exist at the occurrence being resolved.

### P2 — Held same-spelling attribute path bypasses object rebinding rejection

`01_rebound_same.py:4–7`: `r = cfg.runner; r.env[KEY] = "1"; r = other; ... env=r.env` yields `(True, True)` in both candidate and held classifier. The new `object_alias_map` correctly discards `r` and `twohop_guard=False`, but `has_guard:456–457` falls through to `carrier_guard:852–853` and `attribute_flow:678–691,726–739`, which checks dotted-attribute replacements, not a replacement of their root name. The launch can use an unguarded `other.env`. This is a carried false accept in the stated dominance surface, not a new round-74 regression. Contrast `02_rebound_dotted.py`, correctly rejected under the frozen once-bound rule even though the original `cfg.runner.env` remains guarded at runtime.

## Complete fixture results

All fixtures are beside this report. Every reader result is `True`; the table shows only the guard result. `classification.json` records full tuples, held results and individual carrier answers. Fixtures are parsed as data; their subprocess calls are never executed.

| Fixture | Guard / held | Follows declared bound? |
|---|---|---|
| `01_rebound_same.py` | yes / yes | No: false accept after root rebinding; held defect above. |
| `02_rebound_dotted.py` | no / no | Yes: alias is bound twice; conservative rejection required. Not a bounded false reject. |
| `03_sibling_aliases.py` | yes / no | Yes: each spelling independently resolves one edge to the same dotted path; no alias chain. |
| `04_dict_extra.py` | no / no | Yes, narrowly: `dict(env, PATH="/usr/bin")` is not the declared exact `dict(alias)` shape. Semantic false negative outside the promised spellings, not a bounded false reject. |
| `05_splat_extra.py` | no / no | Yes, narrowly: `{**env, "X": "y"}` is not the declared exact `{**alias}` shape. Same outside-bound semantic false negative. |
| `06_nested_attribute.py` | yes / no | Yes: `r.cfg.env[KEY]` and `cfg.runner.cfg.env` cross one alias edge, not a chain of aliases. |
| `07_cross_function.py` | yes / no | Yes: module binding, store in one function and launch in another match the explicitly disclosed line-order approximation; functions need not be called. |
| `08_parameter_shadow.py` | yes / no | No: new false accept; parameter is not the module alias. |
| `09_generic_delete.py` | yes / yes | Yes to the declared gap, unsafe semantically: `del env[KEY]` at line 6 is ignored by generic flow. |
| `10_copy_alias.py` | yes / yes | Yes: store into an env-named mapping copied by `os.environ.copy()` reaches a direct launch through held generic flow; neither new alias carrier fires. |
| `11_alias_delete_copy.py` | no / no | Yes: alias-specific deletion cancellation prevents the exact `dict(env)` copy from counting. |
| `12_alias_delete_direct.py` | yes / yes | Covered by generic deletion gap: alias-specific carrier rejects but generic direct-env fallback accepts after deletion at line 6. Do not advertise universal deletion cancellation. |
| `13_late_alias.py` | yes / no | Semantic false accept: edge used before binding; see dominance qualification above. |
| `14_annotated_rebind.py` | yes / yes | No: unsafe false accept; annotation ignored by new alias table and old attribute flow. |
| `15_annotated_cross.py` | yes / no | No to exactly-once rule: annotated rebind ignored; runtime dotted launch remains guarded. |
| `16_environ_annotated.py` | yes / no | No: unsafe new false accept after annotated environment alias rebinding. |
| `17_environ_rebind_direct.py` | no / no | Yes: ordinary `env = {}` replacement is rejected, unlike annotation. |

`copies_alias:1134–1143` explicitly requires no dict-call keywords and a one-entry splat literal. There are no demonstrated false rejects *inside* those exact declared copy shapes. Extending copies is not needed to uphold this frozen bound.

## Evidence, runtime and residual risk

- Re-read frozen declaration and all three committed receipts without rewriting them. C1 receipt ends at 12/12 versus held 8/12; C2 ends at population 20, readers 13, guarded 13, unguarded 0, controls 36/36 versus held 32/36. These are recorded finite results, not universal classifier soundness.
- Actual candidate addition inspected with read-only `git show b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 -- quality/counters/c2-r74-shapes.py`. Requested six functions and relevant inherited fallthroughs read directly.
- Scoped executable probe: `python3 -I -B .../R74RevC2/attack.py --scratch-root /fast/scratch/hyaku/mado-r74/R74RevC2`, exit 0. Initial 14-fixture pass followed by one expanded 17-fixture pass; final retained receipt is `classification.json`.
- Candidate SHA256: `8a0fc3b24d66fb66f710b0c5c4ac0d8e83826960bc25fdf732652a9108497ab6`. Held round-73 source extracted at declared base; SHA256 `95fd2b7b44ba773eab25349659ac92235f7ca133adaee78883aa9496ed3ec9a4`.
- Canonical counting path is `measure:1348–1365`: population, controls and extracted held controls invoke `classify`; `classify:1202–1204` invokes `has_guard`, whose early returns and inherited fallback determine these results. No alternate production runtime, rerouting, resume path or saturation machinery was introduced or exercised. `resume_continuity_v1` is outside this assigned classifier surface.
- LSP device unavailable: `read xd://lsp` returned “No such tool”; therefore semantic references, definitions and diagnostics could not be requested. Findings instead combine explicit AST implementation reads with executed `classify` outputs; textual reads are not claimed as LSP proof.
- No full gate/selftest/measurement rerun; committed receipts only re-read. No scored file edited, no git/jj mutation, no installation, no host/config/service probes. Receipt copied from the explicitly owned scratch into this directory before scratch removal.
- Recommendation: retain the honest finite 36-case receipt, but do not describe these new carriers as sound against rebinding/shadowing until the findings are resolved under a future, explicitly frozen scope. This review is not admission or integration.

Self-evaluation (1–5): accuracy 4 (executed fixtures, but no LSP); completeness 5 (all eight requested classes plus nine contrast/attack cases); clarity 4 (literal-bound versus semantic distinctions require qualifications); actionability 4 (source causes identified, no edits permitted); conciseness 4 (full fixture matrix retained for reproducibility). Overall 4.2. Highest-impact improvement: scope-aware identity and complete rebinding accounting, with the supplied negative cases used in a newly declared control set. The user should agree this remains a scoped evidence report, not a general proof.
