source: S116, S117, S118, S119 in corpus/SOURCES.md; CPython v3.14.8 functools.rst (partialmethod), Lib/imaplib.py (IMAP4_stream.open), Git v2.56.0 builtin/commit.c (dry_run_commit); .ufo/waves/round-21/oracle/expected.json and corpus/lessons/round-20-verifier-spotcheck.md
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

Source correction S119 explicitly supersedes the universal inference in S113's `teaches` field. S113's quoted `os` process-management fact is retained, but its finite module list cannot support a statement about every other stdlib module; S117's opened process path is a direct counterexample. The source registry is append-only, so the correction is a new row rather than an in-place rewrite of S113.
