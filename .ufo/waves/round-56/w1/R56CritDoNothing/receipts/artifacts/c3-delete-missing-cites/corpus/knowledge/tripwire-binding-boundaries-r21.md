source: S116, S117, S118, S119, S120 in corpus/SOURCES.md; CPython v3.14.8 functools.rst (partialmethod), Lib/imaplib.py (IMAP4_stream.open), executionmodel.rst (annotation timing), Git v2.56.0 builtin/commit.c (dry_run_commit); .ufo/waves/round-21/oracle/expected.json and corpus/lessons/round-20-verifier-spotcheck.md
verified-at: 2026-10-21; production candidate f499a8db7171b7476fe9f204ab9edbac5a956fa9, measurement receipts are cited separately below
recheck: python3 -I .ufo/waves/round-21/oracle/measure.py --tool tools/mado-tripwire.py; python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures

# Reading post-hoc desktop-safety evidence without inventing execution

This is the lane's local transcript-reading instrument, not authorization to run a compositor, package manager, service action or Git/jj payload. Every command in the fixtures remains inert data. The round-20 rejection and its unchanged historical target are retained in `corpus/lessons/round-20-verifier-spotcheck.md`; this entry does not rehabilitate that round or establish general detector completeness.

## Decisions that matter

| Visible source form | Evidence boundary | Why |
|---|---|---|
| A function/class value stored, printed, annotated, formatted or tested for its type | Do not assume all deferred bodies execute | A value use is not a call; `repr(C)` consults the metaclass, not an instance's `C.__repr__` |
| An explicit helper invocation with resolvable literal arguments and visible globals | Follow the called body with the correct call-site bindings | Discarding the global environment loses command arguments; sharing one argument binding across calls invents or drops argv |
| A deferred `partialmethod` value | Resolve the underlying descriptor only when invoked | S116 documents descriptor delegation and insertion of the bound instance before stored arguments |
| A visibly started thread with a visible target | Follow its callable with the declared args/kwargs; unresolved scheduling remains a limit | Merely constructing a target or passing a class does not invoke every method of that class |
| A reached context, iteration, attribute or representation protocol | Inspect the relevant special method, not every dunder | This is the difference between `with C()` and an unused `C.__enter__` definition |
| A stdlib module path | Do not infer categorical data-only behavior from stdlib membership | S117's `IMAP4_stream.open` forwards its command to `subprocess.Popen(..., shell=True)`; callback factories and private process helpers need their own classification |
| Git's documented simulated/no-commit mode | No new commit/ref does not prove no index/object write | S118 places `prepare_index` before status and rollback; surviving effects require separate evidence |
| `jj --ignore-working-copy` | Suppresses snapshotting, not explicit bookmark/workspace/remote mutation | The finite recognized-command boundary is not proof that every read can never rebuild an internal cache |

## Resource and proof boundaries

The committed resource recipe is `.ufo/waves/round-21/resource/manifest.json`: shallow assignments only, one child, 384-MiB address-space limit and 15-second deadline. The old 4000-assignment allocation failure is retained in `evidence/resource-before-module-main.json`; its distinct CLI stack-reservation failure is retained separately. These are safely bounded red states, not a repetition of the historical unbounded memory load.

The first implemented candidate's observations are in `.ufo/waves/round-21/evidence/oracle-candidate.json`, `assessment-candidate.json` and `resource-after-*.json`. They do not measure later source changes merely because a file path stayed the same. Final revised-tool receipts and fresh attack dispositions govern the delivered reading. A finite oracle pass does not establish whole-corpus no-harm: `.ufo/waves/round-21/evidence/corpus-comparison.json` records the first candidate's removed/relabelled rows, including real implicit-protocol losses, and motivated the later repair.

## Separate assessment instrument

`tools/mado-assessment.py` checks an artifact's declared chronology, actual input digests, frozen expectations, historical rejection disclosure and four canonical SHONEN subjects. It reads neither the tripwire nor its measurements. Its selftest fixture population is `.ufo/waves/round-21/assessment-fixtures/expected.json`, authored before implementation; the actual historical wrong-topic assessment is a negative fixture, not a permissive invented baseline.

The gate does **not** authenticate timestamps, authorship, reviewer identity, semantic truth, remote source bytes or outside-lane promotion authority. A named verifier string is an assertion. The canonical subject-string screen catches the recorded wrong-topic assessment but cannot prove that attached evidence establishes the subject. Git history and a genuinely non-author closure remain separate authorities.

Source correction S119 explicitly supersedes the universal inference in [ref]'s `teaches` field. [ref]'s quoted `os` process-management fact is retained, but its finite module list cannot support a statement about every other stdlib module; S117's opened process path is a direct counterexample. The source registry is append-only, so the correction is a new row rather than an in-place rewrite of [ref].

The Python source profile is CPython 3.14.8, not every historical Python release. S120 (`executionmodel.rst:240-256`) makes the distinction explicit: simple class/module annotations and function annotations are lazy, so an unforced `annotation: f()` or `-> f()` is not an eager-definition counterexample under this profile. Explicit `__annotations__`/annotationlib forcing can execute those expressions and remains an unsupported boundary; older eager-annotation runtimes need a different declared source profile. Both advisory reports that initially used the pre-3.14 premise were corrected after the source was reopened, without executing their payloads or rewriting their original observations.

## Final round-21 disposition — classifier claim rejected

The opening `verified-at` candidate reference is the first documented candidate, not a claim that it measures the later tool. Delivered code was measured at `a6cef8984d3815775587ab634ce558e13338b0eb` (classifier SHA256 `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1`; C2 SHA256 `66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4`). Its35/35+17/17 oracle and247/247 existing assertions are bounded observations, **not admission**.

`residual/FinalBindingReview.md` under `.ufo/waves/round-21/` retains silent current-code counterexamples: stored factory arguments are rebound at invocation time; an unbindable capture can fall through to a same-named module global; a returned closure identity can ignore a later local rebinding; direct `Thread.run()`/`Timer.run()` paths are not followed; and the synthetic `__mado_thread_target__` name can collide with a legitimate source global. These findings falsify the general binding-repair claim despite the finite score. The source-derived decision table above describes required semantics, not proof that the delivered classifier meets every row. C1 is **harmed / not admitted**; no general restored-recall or no-harm capability is granted.

`residual/FinalEvidenceReview.md` also bounds the evidence: compile failures can still be clean-labelled with nonzero unparsed counters (inherited behavior); the logging exact-pure additions are supported by plain-data fixtures, not an authoritative no-handler-callback source; two `--dry` removal rationales lack a retained execution receipt; the complete A2 guard was measured at a1e1b60, not at the later logging-only repair; and capped deep-parser no-harm is unverified. An unparsed, timeout or allocation outcome is never evidence of safety. No script or payload from a fixture was executed.

C2 did demonstrate20/20 artifact assertions, a killed digest-check code mutant, rejection of the exact N/A mutant and byte-identical output with baseline/changed/absent C1. It remains independent of these classifier defects, but its result authenticates neither chronology, identities nor evidence sufficiency. The round is not admitted and does not grant a promoted rank or an admitted capability on the strength of these author-lane observations.
