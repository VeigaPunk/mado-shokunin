# RevengeSuiteNegatives — partly falsified: seven clean pins were deliberate R19 guards; one was a semantic error

## Verdict

The eight `clean → finding` edits are not one class of correction. Seven preserve explicit round-19 matcher limits that round 20 deliberately replaces with E1/E3 binding and evidence semantics. The remaining edit, `r19-class-body-deferred-clean`, corrects a round-19 semantic mistake: an ordinary Python class body runs as part of executing the class definition, rather than being deferred like a function body. The round-20 expectation is therefore justified, but its parenthetical `S111` citation is not the exact anchor for that class-execution fact (details below).

This is a reconstruction of the old expectations and stated contracts, not evidence that any fixture command was executed. In particular, `lead` means uncertainty about an opaque callee, not proof of a command run.

## Reconstructed contract and evidence chain

Round 19's HelperFn rule A indexed top-level, undecorated `def`s; it dropped duplicate names, only bound a call after the definition when call arguments were literal and there were no varargs, and required literal defaults for omitted parameters. Rule B emitted a lead only for an unresolved bare-name call with a syntactically literal positional argv list/tuple; it did not inspect keyword argv lists or pure-call arguments (`.ufo/waves/round-19/w1/reports/TwHelperFn.md:32-45`). The report explicitly lists nonliteral arguments, call-before-def, redefinition, varargs, and nonliteral defaults among its 20 clean guard cases (`TwHelperFn.md:137-139`). The merged implementation intentionally kept distinct environments: a cell's module env for direct spawn arguments, but an empty module-scope helper-binding env, so helper arguments were substituted only when the call text itself stated them literally (`.ufo/waves/round-19/w1/reports/TwMerge.md:61-73`).

Round 20 states the broader contract: visible helper bodies count as `observed` when a literal argv reaches a spawn; an opaque/unresolved callee is a `lead`; and E3 uses the binding in effect at the call (latest preceding binding) (`.ufo/waves/round-20/gen_w1.py:36-38`; see also `SCORECARD.md:1244-1260`). That change explains why the seven old negative pins are not evidence that the round-19 expectations were accidental: each enforced a documented conservative boundary, and round 20 explicitly widened that boundary.

## The eight clean-to-finding cases

| Case and fixture | Why round 19 pinned it clean | Round-20 expectation and disposition |
|---|---|---|
| `py-helper-nonliteral-arg` — `r19-helperfn/py-helper-nonliteral-arg.jsonl:1` | `cmd` is module-bound to a literal argv list, but the visible helper is called as `run_record(cmd)`, not with a literal AST argument. R19's HelperFn rule required literal call arguments, and the merge deliberately did not feed the module env into helper bindings. **Deliberate conservative limit.** | `expected.json:104-112` changes to `package_query/pacman:-Q`, `observed`: the module literal reaches `subprocess.run` in the visible helper. This is the round-20 E1 expansion. |
| `py-helper-defined-after-call` — `r19-helperfn/py-helper-defined-after-call.jsonl:1` | The `run_record([...])` call precedes its `def`; R19 indexed helpers and followed only calls after the def line. This is the explicitly listed call-before-def guard. **Deliberate conservative limit.** | `expected.json:114-122` changes to `package_query/pacman:-Q`, `lead`, not `observed`: E3 does not resolve the later definition backward to the call. The round-20 contract treats the unbound-at-call literal argv as a lead. It remains only a lead; it does not prove a callee received or ran it. |
| `py-helper-redefined` — `r19-helperfn/py-helper-redefined.jsonl:1` | The same helper name has two definitions. R19 dropped duplicate names rather than choose one, an explicit ambiguity guard (`TwHelperFn.md:32-34`). **Deliberate conservative limit**, although this particular pair has identical bodies. | `expected.json:124-132` changes to `host_mutation/pacman:-S`, `observed`: E3 selects the second, latest preceding spawning definition. |
| `py-helper-vararg` — `r19-helperfn/py-helper-vararg.jsonl:1` | `run(*a)` forwards through a variadic parameter; R19's binder excluded varargs/starargs (`TwHelperFn.md:33-35`). **Deliberate conservative limit.** | `expected.json:134-142` changes to `package_query/pacman:-Q`, `observed`: the visible `*a` body passes the literal positional values to `subprocess.run`, within round 20's W-wrapper coverage. |
| `py-helper-default-nonliteral` — `r19-helperfn/py-helper-default-nonliteral.jsonl:1` | The omitted `timeout` parameter's source default is `T`, a name rather than a literal AST expression. R19 required every omitted parameter to have a literal default, even though the fixture binds `T = 5` first (`TwHelperFn.md:33-35,137-139`). **Deliberate conservative limit.** | `expected.json:158-166` changes to `package_query/pacman:-Q`, `observed`: the straight-line module binding fixes the default and the argv reaches the visible spawn. |
| `py-lead-nonliteral-var` — `r19-helperfn/py-lead-nonliteral-var.jsonl:1` | `cmd` is assigned a literal list, but `run_record(cmd)` passes a name, not the literal positional list/tuple required by R19 rule B (`TwHelperFn.md:41-45`). **Deliberate conservative limit.** | `expected.json:263-271` changes to `package_query/pacman:-Q`, `lead`: round 20 follows the statically fixed module value to the unresolved callee. This is a lead only. |
| `py-lead-defined-nonliteral` — `r19-helperfn/py-lead-defined-nonliteral.jsonl:1` | The helper is defined, so R19 rule B's unresolved-helper lead does not apply; its call argument is a module name rather than a literal expression, so rule A does not bind it. The merge's empty module-scope helper env explains this exact clean result (`TwMerge.md:61-73`). **Deliberate conservative limit.** | `expected.json:280-288` changes to `package_query/pacman:-Q`, `observed`: round 20 resolves the module literal through the visible helper body to the spawn. |
| `r19-class-body-deferred-clean` — `r19-bashcvar/class-body-deferred.jsonl:1` | The fixture assigns `p = subprocess.run([...recipe...])` in a class body. R19 recorded “class/lambda deferral” as a precision-negative shape (`.ufo/waves/round-19/w1/reports/TwBashCVar.md:53-60`), and the old suite named it `class-body-deferred-clean`. The old `scoped_call_ids` comment also grouped class bodies with deferred def/lambda bodies (`.ufo/waves/round-20/w1/patches/TwRuleB-v2.patch:124-130`). **This was an error, not merely a conservative boundary:** a class definition is an executable statement and a class definition is a block executed as a unit (pinned CPython execution-model text at `.ufo/waves/round-20/w2/ReopenExecModel/fetch/cpython-3.14.8-Doc-reference-executionmodel.rst:20-21,163-170`). | `r19-bashcvar/expected.json:412-426` changes to `package_query/pacman:-Q`, `observed`. The direct spawn is inside the executing class body, with the literal module recipe. This correction is semantically required. |

The first seven dispositions have high confidence as descriptions of R19's *intent*: each boundary is stated in the contemporaneous report or merge report, not inferred from the test name. The class-body verdict also has high semantic confidence from the pinned CPython document. The `defined-after-call` result is correctly a `lead` under the round-20 rule, not an observed finding; [INFERENCE] in a fresh empty kernel that exact snippet would raise on the unbound name, so the lead should not be read as proof that the argv was handed to a callable.

## Diff, pins, and related marker-only changes

Read-only comparison:

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --unified=0 01b8094..28c6837 -- \
  .ufo/waves/round-19/tripwire/r19-helperfn/expected.json \
  .ufo/waves/round-19/tripwire/r19-bashcvar/expected.json
```

Observed diff: one bashcvar clean expectation at `@@ -416,2 +416,11 @@`; seven helperfn clean expectations at old starts `106, 113, 120, 127, 148, 250, 264`; plus two existing helperfn rows changed only by adding `evidence: lead` (old starts 219 and 228). This matches the round-20 lesson's summary of eight clean-to-finding edits and two lead markers (`corpus/lessons/round-20.md:96-99`). The marker-only rows are `py-lead-cross-cell-literal` and `py-lead-two-calls`; they are not additional clean-to-finding cases.

Digest evidence:

- `git show 01b8094:.ufo/waves/round-19/tripwire/r19-helperfn/expected.json | sha256sum` → `717782d80f373bea30615d29d634b19061b5f38d4a0903648736cbcf9fcccda7`.
- `git show a4046a8:.ufo/waves/round-19/tripwire/r19-helperfn/expected.json | sha256sum` → `91e247912827aa5848a7ce87ef7c59273c6681d737f6456d87180f251ded3644`.
- `git show 01b8094:.ufo/waves/round-19/tripwire/r19-bashcvar/expected.json | sha256sum` → `6303675695ffa90059e6e014d03a87795f5a08ae96bd911f39d01b1d1672e602`.
- `git show a4046a8:.ufo/waves/round-19/tripwire/r19-bashcvar/expected.json | sha256sum` → `e72a97def0c67617984962c4b3276b6127862daa4d48f9dabd5ae845437abbe5`.
- The eight fixture SHA-256 values, in table order: `5c324eb69bb67c31a84a61bb4e53d6c23fe7baa79626c4cc6fd0cf6f4ccc7423`, `77cca64a6057d99eaf011e57c957e89a4342cc8d73e92085cfec8d1ba0dc1872`, `e3b6455eb039c1b343c4eacad5da66f263f6d0bfb0d9a3179a0872964bd0f0ee`, `6a80107179dc7a627a72e5051c63e5b24f17f8026ff9a99587c23ba18752d082`, `0eb2cecf1c5f6ba5031c98eb2bc3b32aeed22847970e7e1df794efff8a3b43fb`, `d6a829994866b9e32a97daabb49702a48b2f41f7b3030c302c433aa59b62d576`, `d0881d59db67c2a76c962b0039abf5ca74c4e8374d22d887485dd24a7f92bb11`, `95e415597bc63c7e66effd4b27697426b1e2ace82127dd11bde45a5a38ea2399`.
- The fetched CPython execution-model file hashes to `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`, matching the digest recorded for S111 in `corpus/SOURCES.md:123`.

## Divergence

The class-body explanation in `r19-bashcvar/expected.json:426` attributes the fact to “CPython execution model, S111.” S111's registry entry currently locates its supporting quotes at `executionmodel.rst:59-61` and `:140-142` and scopes the row to name binding/resolution (`corpus/SOURCES.md:123`); those locations are not the class-execution anchor. The exact same digest-pinned file does state at `:163-170` that a class definition is an executable statement and describes its class-definition block. Thus the semantic correction is supported by primary text, but the specific S111 citation should be anchored to those lines / accurately scoped. This is a citation precision issue, not support for restoring the round-19 clean pin.

## Limits

- Read-only review only: no `--selftest`, `--scan`, fixture execution, source runtime, gate, host probe, or VCS write was run. The round-19 suite result `247/247` is reported evidence in `TwMerge.md:105-133`, not a run performed for this assignment.
- I attempted `read xd://lsp`; the device returned `No such tool: xd://lsp` and listed no LSP route. Therefore no LSP references/definitions were available. Text searches were used only to locate files; semantic conclusions above come from the hand-read fixtures, reports, contract, and pinned source text.
- No web source was reopened; the class-semantics source was already present locally in the assigned wave's fetch directory.

## Installs

none