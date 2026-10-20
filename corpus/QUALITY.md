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

Provenance notes (round 12, post-integration review — `.ufo/evidence/round-12/l2-postcritic.md`, `l2-postreviewer.md`):
criteria 6–14 are grounded in lane incidents; 15–16 are grounded in external inference traps
(`lessons/round-12.md` § Inference traps), not lane incidents, despite the block heading. Criterion 8's
secondary citation `lessons/round-10.md:108-118` grounds record debt (M4), not planned paths; its
grounding is `lessons/round-12.md#mistakes M3` alone.

## Criterion from the outside S030 disagreement (round 13)

17. Before source-fragment renumbering/merge, screen repeated canonical URLs across active rows even when scope wording differs. Review overlapping scope explicitly; reject/merge duplicates or append a genuine superseding row with a resolvable prior id. Preserve rejected history, and send distinct-scope reuse to human review rather than claiming URL equality proves semantic duplication. A warning-only shared census is not this review. (lesson: lessons/round-13.md#mistakes M1; outside finding: lessons/round-12-verifier-spotcheck.md)

The lane-local collision screen is a conservative merge-review trigger,
not a new source-tier scheme or an automatic knowledge-admission authority.
Its red-before case uses the actual admitted S017/S030 pair, not merely a
synthetic same-scope duplicate; its green state preserves rejected S030.

## Criteria from regular-target and retained-data mistakes (round 14)

18. A declared source target is not validated by existence alone: direct
    targets and every matched glob member must be regular files, following
    file symlinks. Name non-regular versus unresolved targets separately.
    Exercise mixed-glob rejection without misclassifying its regular member;
    preserve source-set/order as separate invariants. This is the lane's
    strict supported-source policy, not an assertion that Hyprland itself
    rejects every skipped target. (lesson: lessons/round-14.md#mistakes M4)
19. Scope retained-data statements to the actual field or record class.
    If global records are projected to interface/version pairs but the
    enclosing artifact retains sanitized package/probe/session metadata,
    name both; “only headers” must not describe the entire artifact.
    Keep diagnostic requests, retained evidence and behavioral conclusions
    separate. (lesson: lessons/round-14.md#mistakes M1; outside R13-V1)

R13-V2/V3 use existing criteria 7, 9 and 13: a within-run boundary
receipt does not establish cross-revision output equality, and future
standalone selftest receipts carry their resolved commit and raw gate
digest locally. No duplicate provenance criterion or generic wrapper is
introduced; the lesson records the rejected implementation candidate.

## Round 15 — receipt application and host-install safety

R14-V1 applies existing criteria 7, 9 and 13: preserve provisional historical
headers; append their exact derived-target relation to committed bytes.
Never stamp a later full-gate measured commit onto a pre-commit mutation run.
The lesson's M1 and standing-use erratum name the boundary and red/green
static correction audit; no generic execution wrapper or duplicate
provenance criterion is introduced.

20. Before a future tool install, obtain `pacman -Sp --print-format '%n %v' <pkgs>`
    and compare every planned package name (including dependencies) with the
    installed-name set. The plan must contain only not-already-installed
    packages; any overlap goes to L0 instead. Helpful-tool authorization does
    not permit a partial upgrade. Round 15 performs no further pacman operation,
    rollback/downgrade or restart. (lesson: lessons/round-15.md#mistakes M2;
    orchestrator ruling on the actual libinput transaction)

## Round 16 — outside rejected-harmed follow-through

21. Host-install pause and declared-plan evidence boundary (lesson: lessons/round-16.md#mistakes M1/M2). Supersedes criterion 20's prospective install route **while the
    operator's host-wide pause holds**: no package transaction or host
    service/compositor mutation is permitted, including installing a tool
    merely to read its help. Use already available source/documentation;
    source examples are data, not execution permission. Carry the pause and
    this round's no-live-probe scope into every seat context. A static
    action-plan classifier must return nonzero on the literal libinput
    incident argv, listed argv[0] basenames even when path-prefixed or
    mislabeled, unknown kind and malformed action, with a source-read
    control. Unlisted wrappers/operands are not screened. Its verdict is
    not tool interception, credential/privacy/probe safety, host immutability,
    a real package dry run or remediation. After explicit operator lift,
    criterion 20's complete real-plan/installed-name comparison still applies; a
    hard-coded new-only fixture never proves it ran.
    Even a real new-only name comparison is necessary, not clearance:
    stale sync state, dependencies, replacements, hooks and running-process
    compatibility remain operator decisions. No filtered fixture authorizes
    a transaction, and editing the lane policy cannot lift the host pause.
    (lesson: lessons/round-16.md#mistakes M1/M2; outside
    lessons/round-15-verifier-spotcheck.md R15-V1/V2)

The runnable check and its failure evidence are registered in SKILL.md.
The unresolved host-recovery decision stays with the operator. No safety
trade is erased by this criterion or a green configuration gate.

22. Re-derive every active, non-retired axis under its recorded counting rule before selecting the lowest axis; do not compare coverage only with the hermetic-suite pass fraction while a lower calibration row remains active. Report literal versus semantic citation counters separately rather than silently changing the rubric. (lesson: lessons/round-16.md#mistakes M3; PlanningWalk is a lane-dispatched adviser, not an outside reviewer)

## Round 17 — receipt-label precision (outside R16-V1)

23. A sentence that attributes a verdict token to a receipt must cite a receipt whose recorded outcome is that token at the revision the sentence describes (lesson: lessons/round-17.md#mistakes M1; outside lessons/round-16-verifier-spotcheck.md R16-V1).
    Outcome means the verdict word on a `MADO_<NAME>:` line, a `finding`
    value, or the got-side of a selftest row — never want-side text, a fixture
    name, or `matched_exit` alone (exit 2 is shared by `frozen_error` and
    `snapshot_tampered`). When the receipt records a `measured_commit`, the
    sentence's revision must match it. A superseded receipt is named as
    superseded and keeps its true token; corrections append and never relabel.
    This specifies criterion 9's commit binding at token level; it did not
    bite on round-16 line 131-132 because 9 binds the commit, not the token.
    Runnable check: `python3 -I .ufo/waves/round-17/label-check.py`
    (seven declared claims including the R16-V1 red line, a want-side-only
    mutant and a wrong-revision mutant; `EXPECT_SUMMARY` must be 7/7).
