# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command,
   evidence id) — never oral knowledge.
3. Observation, inference, and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

## Criteria from mined mistakes (round 12)

6. Publish each pinned value with a re-derivation command and named revision; any shortened hash must be a true suffix, with corrections preserving old and new values. (lesson: lessons/round-12.md#mistakes M1; lessons/round-10.md:82-97)
7. Hash committed artifacts from `git show <commit>:<path>`; label work-window hashes provisional and bind them again at the commit. (lesson: lessons/round-12.md#mistakes M2; lessons/round-10.md:98-107)
8. Treat a path as landed or as a recheck target only after confirming it exists at the named commit; label predicted names as planned. (lesson: lessons/round-12.md#mistakes M3; lessons/round-10.md:108-118)
9. Bind each audit verdict to a commit or frozen-copy sha; label mid-edit failures in-flight, never as settled defects. (lesson: lessons/round-12.md#mistakes M6; lessons/round-10.md:98-107)
10. Report each count as `<n> — <command> <date>` and rederive it from the named revision instead of transcribing a prior summary. (lesson: lessons/round-12.md#mistakes M7; LOG.md:138-141,253-256)
11. An absence claim about a tool includes its own `--help`/man/source sweep, pinned version, and matching locations; do not infer behavior from a verb name. (lesson: lessons/round-12.md#mistakes M8)
12. An `[x]` requires a named non-author verifier and its dispatching lane; a lane-dispatched seat remains `[~]`, not independent clearance. (lesson: lessons/round-12.md#mistakes M9; lessons/round-1.md:19-22)
13. Evidence meant to outlive a round is a committed path or quoted lines plus sha; `/tmp` records provenance only. (lesson: lessons/round-12.md#mistakes M11; lessons/round-10.md:74-78)
14. A census compares expected and observed sets and names both missing and extra members; pin module membership where it is a claim. (lesson: lessons/round-12.md#mistakes M13)
15. Label every protocol or config inference by layer, phase, and version/era; do not substitute protocol status, documentation syntax, or tool layer for host behavior. (lesson: lessons/round-12.md#inference-traps M01-M07)
16. Upstream documentation and releases support only dated `[INF-docs]`; never promote them to installed-host or end-to-end facts without independent host measurement. (lesson: lessons/round-12.md#inference-traps M03/M05/M06/M07)

Source tiers and the registry live in SOURCES.md (contract v1); this bar governs claim admission only.
