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

## Round 18 — producer identity, instrument bite, producer status (outside R17-V1/V2/V5, JjAuditMado F10)

The round-14/15 rulings ("no duplicate provenance criterion") stand for
input binding and commit binding, which criteria 7, 9, 13 and 23 already
carry. Criterion 24 adds only what those leave open: the identity of the
*producer* bytes that ran, and receipt-borne evidence for a re-cut claim.

24. A sentence that relies on a scan, selftest, measure or replay receipt cites one whose own bytes name its producer (`tool_sha256=` equal to `git show <measured_commit>:<tool> | sha256sum`, read with the producer status checked) and its `measured_commit`; a claimed re-cut is a committed receipt with those fields, never a narrated rerun; a report labels every tool sha with the revision it belongs to (lesson: lessons/round-18.md#mistakes M1; outside lessons/round-17-verifier-spotcheck.md R17-V1/V2).
    Runnable check: `python3 -I .ufo/waves/round-18/receipt-check.py`
    (claims `.ufo/waves/round-18/receipt-claims.json`). Red: the six
    round-17 real-transcript receipts read at `d9a5a18` print
    `MISSING_PROVENANCE` (they carry input digests only); a fixture bound
    to the `f71ccbe` tool sha read at a later tool prints `SHA_MISMATCH`.
    Green: the round-18 re-cut receipts and the frozen-replay receipt.
25. An instrument tightening counts as biting only with a committed mutant receipt in which the pre-change instrument credits a committed mutant and the post-change instrument rejects it, both instruments named by sha256 and each mutant by its diff digest; a seat or `/tmp` lab run is provenance, not credit (lesson: lessons/round-18.md#mistakes M2; outside lessons/round-17-verifier-spotcheck.md R17-V5).
    Runnable check: `python3 -I .ufo/waves/round-18/measure-mutants.py`
    → `.ufo/waves/round-18/evidence/measure-mutants.json` (`no_bite` lists
    any tightening the loose instrument already rejects). Red at `d9a5a18`:
    no committed mutant receipt exists for any of the six round-17
    tightenings, so round-17 M3's "shown to bite" has no credit under 25.
26. A digest, count or identity taken through a pipe or command substitution carries the producer's exit status; when the producer fails the result is UNKNOWN, never a value (`e3b0c44298fc1c14…` is the sha256 of empty input, not of a file) (lesson: lessons/round-18.md#mistakes M3; outside /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md F10).
    Runnable check (behavioural, the bite): `bash tools/mado-verify.sh
    --selftest` scenarios OM9/OM10 (stub `git show`/`describe`/`rev-parse`
    exit 128 must read UNKNOWN with `rc=128`, never `local edit`); red
    before at `d9a5a18`: `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt`
    §1. Screen only (not proof — pipefail alone does not consume the rc):
    `python3 -I .ufo/waves/round-18/pipe-rc-census.py REV` lists unchecked
    producer sites; at `d9a5a18` it flags nine, of which only `:3406` was a
    verdict-bearing hazard (the others are fixture or display values).
    `${PIPESTATUS[0]}` read after `x=$(…)` is the assignment's status, not
    the producer's; capture inside the substitution.

Round-18 wave-2 correction (append-only): criterion 24's red-fixture sentence
above says a fixture bound to the `f71ccbe` tool sha read at a later tool prints
`SHA_MISMATCH`; the hardened checker (ReceiptCheckFix) prints `STALE` for that
stale-but-consistent shape; `receipt-fixtures/stale-rev-receipt.txt` remains the
`SHA_MISMATCH` control. Green arm: `EXPECT_SUMMARY: 21/21`, exit 0, with the
round-18 re-cut, frozen and measure receipts as `ok` claims.

## Round 19 — durable anchors, supersession sweep (outside R18-V1/V3/V4); R18-V2 applies criterion 24

Not restatements: criteria 7 and 13 bind a digest to committed bytes, and a
committed digest of a rotating GitHub tree page satisfies both; 27 asks whether the
upstream an anchor names can be re-obtained to the same bytes. Criterion 6 asks for
a named revision; 28 is a property of the owned file set after a supersession,
which passes 6 and 9 untouched. R18-V2 (criterion 26's own red-before receipt has
no producer header) is not a new criterion: it is criterion 24 applied to the
lane's own criterion evidence (outside critic CriticC1, round-19 w1), recorded in
the note after 28.

27. A credited source row's anchor is reproducible — tag- or commit-pinned bytes with their sha256, a content-addressed object id, or a registry checksum; a digest that committed receipts show rotating between fetches never anchors a row, and an unversioned alias (`latest`, `main`, `master`, `HEAD`) never serves as version-specific support without a pin in the anchor; the superseding row names the replaced id (lesson: lessons/round-19.md#mistakes M1/M2; outside lessons/round-18-verifier-spotcheck.md R18-V1/R18-V4).
    Runnable check: `python3 -I .ufo/waves/round-19/anchor-durability.py REV`
    (mined rows only; PER_FETCH_DIGEST needs ≥2 distinct committed 200
    digests for a URL the anchor credits; a single-digest page digest prints
    `durable — … not shown to rotate`). Red at `9c54c56`: `FLAGGED S084 S094`
    (S084 UNPINNED_ALIAS, S094 PER_FETCH_DIGEST, 5 receipts / 5 digests),
    exit 1. Green at `df84807`: `flagged=0`, exit 0 (S094 → S097, S084 → S098,
    both old rows `rejected`). Limit: it reads the anchor text; it cannot tell a
    reproducible page that has never been fetched twice.
28. When a present-tense value is superseded, every owned file that still states the old value carries, in the same round, an in-file pointer naming the new value and the SOURCES row that superseded it; a SKILL erratum or one note does not discharge the sweep for the other files (lesson: lessons/round-19.md#mistakes M3; outside lessons/round-18-verifier-spotcheck.md R18-V3).
    Runnable check: `python3 -I .ufo/waves/round-19/supersede-sweep.py REV`
    (ledger `.ufo/waves/round-19/supersessions.json`: `2.17.0` → `2.17.2`,
    rows S090/S096; scope knowledge notes, corpus/README.md, SKILL.md,
    PROVINCE.md, tools/*). Red at `9c54c56`: `files=13 pointed=2 stale=11`,
    exit 1. Green at `df84807`: `pointed=13 stale=0`, exit 0. Limit (CriticC1):
    file-level — one pointer line clears a file with other untouched mentions;
    a reviewer reads each pointer, the check only proves none is missing.

Round-19 application of criterion 24 to criterion 26's evidence (R18-V2,
append-only; no new number): criterion 26's red-before
`.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` and `regression-recut.txt`
read `MISSING_PROVENANCE` under `python3 -I .ufo/waves/round-18/receipt-check.py
.ufo/waves/round-19/receipt-claims.json`. The header-bound re-cut is
`.ufo/waves/round-19/evidence/gate-swap-receipt.txt` (`tool_sha256=6e6782c3…` =
the committed fixture `evidence/gate-swap-d9a5a18.sh`, `measured_commit=df84807`):
`383 passed, 6 failed` — five OM9 assertions plus `R10` (the fixture's own
`PIN_MADO` self-pin moves with any gate edit); round 18's "383/389, five OM9"
omitted R10. Criterion 25's runnable command now needs an explicit lane receipt:
`python3 -I .ufo/waves/round-18/measure-mutants.py --out
.ufo/waves/round-18/evidence/measure-mutants.json --force-lane-receipt` (a bare
run prints JSON to stdout and writes nothing; w1 MeasureMutantsOut).

Round-19 wave-2 limits (append-only; CriticC1W2, RerunC1): criterion 27's checker
prints `durable` when no rule fires — not proof of reproducibility. It reads any
`N.N` in the anchor as a pin (even an unrelated or superseded version), knows only
the alias words `latest`/`main`/`master`/`HEAD`, does not check that a registry
checksum is present, and does not exercise "the superseding row names the replaced
id" (true by reading for S097/S098). Access-date-only anchors (S032–S035) print
`durable`. Criterion 28's ledger now also carries the S094→S097 and S084→S098
supersessions; its walker entry is the C2 file set, so 28's green there is not
independent of C2. The line rule credits `corpus/README.md:44` (a round-18 row with
`Walker v2.17.2` and the span S072–S091) and `walker-route-r18.md:1` (its source
list) at `9c54c56`: substantively the pre-state held 0 dated pointers, not 2.
Wave-2 correction (append-only; w2 RerunGateSwap): round 18 did not omit R10 everywhere —
`.ufo/waves/round-18/w3/reports/W3CriticC1Final.md:188` lists "R10 (pin drift, expected)";
only the round-18 SCORECARD fragment "(383/389, five OM9 failures …)" left it out. The
round-19 gate-swap receipt is a new red run on a hybrid fixture (the d9a5a18 block inside
the 17661e0 gate), header-bound; criterion 26's original red-before file still reads
`MISSING_PROVENANCE`.
More criterion-27 checker limits (w2 RerunAnchor): `accessed on <date>` counts as a date
pin, licence/protocol versions (`Apache-2.0`, `HTTP/1.1`) count as version pins, a 40-hex
tree id counts as a commit, `develop`/`trunk` branch URLs are not aliases, a GitHub release
HTML page at a tag reads as raw bytes, and a row made malformed by a literal `|` drops out
of evaluation. The red at `9c54c56` and green at the tip stand; a `durable` line is a screen
result, and the closure reads the anchor.

## Round 20 — fail-closed isolation and detector precision (outside R19-V3, R19-V4)

29. An isolation harness fails closed: every setup step (namespace creation, each bind or mount, each post-mount verification that the target now holds the stub) is tested on its own, and any failure — or a missing target or stub — aborts before the payload starts; `set -e` with a non-final `&&` member is not a gate, and a harness that exits 0 without running its payload under a forced failure counts as failing open (lesson: lessons/round-20.md#mistakes M2; outside lessons/round-19-verifier-spotcheck.md R19-V4).
    Runnable check: `bash .ufo/waves/round-20/isolation-check.sh HARNESS` — forces six
    setup failures (mount non-zero, `unshare` refused, mount exits 0 without binding,
    partial arm over two targets, missing target, missing stub) through PATH stubs over
    `/tmp` targets only, with a payload that only writes a `/tmp` canary, plus a positive
    control. Red: `.ufo/waves/round-20/evidence/inns-r19-shape.sh` (the round-19
    `[ -e ] && mount && echo` shape, SentinelGatePath §Incident) reads `FAIL_OPEN` in five
    of six modes, exit 1 (`evidence/crit29-inns-r19-shape.txt`). Green:
    `.ufo/waves/round-20/isolate.sh` reads `FAIL_CLOSED` in all six and
    `POSITIVE_CONTROL_OK`, exit 0 (`evidence/crit29-isolate.txt`); four single-point
    mutants of it (`evidence/isolation-mutants/`) each read `FAIL_OPEN` in the mode they
    break. Sources: bash 5.3 `set -e` exceptions (S110), util-linux unshare/mount and the
    namespace capability rules (S109, S112). Limit: a harness that resolves `mount` or
    `unshare` by absolute path bypasses the stubs and reads `COULD_NOT_EVALUATE`, never a
    pass; fail-closed setup is not containment — `isolate.sh` passes the environment
    through and the compositor and session-bus sockets stay reachable inside it
    (w1 SentinelPause20 H3), so it is no licence to run a host probe while the pause binds.
30. A detector change credited for recall is admitted only beside its precision evidence: committed negatives of the shapes the new rule could misread (pure data, formatters, names bound or shadowed in the text), each read at the pre-change and the changed tool; a whole-corpus diff against the pre-change tool that lists every added and relabelled row; and a machine-readable marker on every row the detector cannot tie to a visible execution path (`evidence: lead`), never the shape of an observed row (lesson: lessons/round-20.md#mistakes M1; outside lessons/round-19-verifier-spotcheck.md R19-V3).
    Runnable check: `python3 -I .ufo/waves/round-20/tw-precision.py REV` (suite pinned at
    `f3da504`), read for families P (pure data → no row) and L (invisible body → `lead`).
    Red at `1f7f995` (tool `367be947…`): P 7/66, L 1/18 — the closure's data-only
    `BLOCK=frozenset([...])` artifact is case `P-CasePureBuiltins-frozenset-closure`,
    an unmarked ordinary `package_query` row. Green at `28c6837` (tool `9613f510…`): P
    66/66, L 17/18 (`.ufo/waves/round-20/evidence/precision-*.txt`). Its green is not
    independent of the round-20 C1 repair (it reads the same counter). Limit: the suite
    was written in the same round as the fix (blind authors, but one contract); a
    held-out set (`precision-heldout/`, 12 cases outside the contract) reads 0/12 before
    and after, and the corpus diff is the out-of-suite evidence.

Round-20 application of criterion 10 to round-19 tallies (R19-V2, R19-V4, R19-V5;
append-only, no new number — registered criterion 30 "re-derive stated counts" was
withdrawn as a restatement of 10, SCORECARD "Round-20 pre-measurement corrections"):
`python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json`
re-derives each registered round-19 count under its named counting rule from committed
bytes. Red: "155 round-19 transcripts" (lesson round-19 :124) → 154 receipt files;
"5/13 name S096" (SCORECARD :1167, lesson :108, LOG :1324) → 6/13 first-matching line
(8/13 any matching line; the 5 was RerunC2's cited-as-evidence reading at `01b8094`);
"the ten old OM10 assertions" (SCORECARD :1225) → nine labeled occurrences, eight
distinct. Green entries are the round-20 correction sentences. Limit: it reads only
registered statements; a stale sentence left beside its correction is not flagged.

Round-20 attempt-2 corrections (append-only; 2026-10-21; no new number):
- Criterion 10's application above: the bare invocation exits 2 (green entries read at a
  revision; w2 RevCrit10Application F1). The runnable form is `python3 -I
  .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json --set all --rev
  REV --expect` (at `a8960de`: `TALLY_SUMMARY n=9 match=4 mismatch=5`, `EXPECT_SUMMARY:
  9/9`, exit 0).
- Criterion 29's check was rebuilt by attempt 1 (`f8576f7`: controls not exported, an
  execution witness, stat identity, a scrubbed environment) after w2 RevQuality29 showed
  a harness could read the leaked controls and mask itself green. Its six modes are four
  PATH-stub injections and two real missing target/stub paths (w2 RevKnowledgeNote3). Re-run
  at `a8960de` (`a2/evidence/iso/crit29-*.txt`): red `inns-r19-shape` 5/6 `FAIL_OPEN`, exit 1;
  green `isolate.sh` 6/6 `FAIL_CLOSED`, exit 0; the four adversarial harnesses
  (masked, env-aware, fake-cmp, canary-deleter3) and the four mutants each read
  `FAIL_OPEN` in at least one mode, exit 1.
- Criterion 30's green at `28c6837` held on its three legs and still admitted a recall
  loss: w2 found 52 out-of-suite real-execution shapes the older tools reported and the
  repair dropped without a row (lessons/round-20.md#mistakes M9). The legs bound what a
  detector adds, not what it removes. At `a8960de` the legs read P 66/66, L 17/18, corpus
  diff from `9c54c56` 0 lost; the recall-loss evidence that caught M9 is the attempt-2
  guard (`a2/a2-guards.py`, `recall_lost` 52 → 0). A criterion requiring a removal-side
  population for every detector change is a candidate for round 21, not registered here:
  adding it after measurement would move this round's C2 target.

## Round 21 — residual-resource guard and assessment applications

31. A detector no-harm claim includes bounded resource evidence on independently frozen wide/shallow as well as recursive/deep inputs. A call-descent limit is not a retained-memory bound: snapshot storage must not grow quadratically with unrelated literal assignments. Register input recipes, expected semantic outcomes, process concurrency, memory/time caps and the exact API/CLI entry path before measurement. A harness cap, timeout, allocation failure or unparsed/error verdict is not a clean result; retain it with input/tool/runner digests and status. Do not reproduce an unsafe historical memory load to confirm it. Ground: `lessons/round-21.md#mistakes` M2 and outside `lessons/round-20-verifier-spotcheck.md:42,78`; resource source cause in `.ufo/waves/round-20/a2/review/ReviewRuntimeV3.md:38`. Runnable bounded evidence producer: `python3 -I .ufo/waves/round-21/resource/measure.py --tool TOOL --mode module-main` (384-MiB address-space cap, 15-second timeout, sequential children); its own zero exit means receipt production, not that children passed. The same CLI mode separately exposes the old 512-MiB thread-reservation issue and is not mislabelled quadratic-memory evidence. Red/green results count only when actually committed.

Applications, not new numbered criteria: criteria 7/9/13/24 bind frozen oracle/corpus/runner bytes and measured revisions; 3/28 require the in-entry residual correction; 12 and the canonical SHONEN contract require assessment of the actual four subjects. Criterion 30's old positive guard did not cover removal-side true-finding loss, so round21 explicitly adjudicates removed/relabelled rows on its entire frozen committed fixture population. It does not equate that population with the old private mutable session corpus. Round20's criterion30-prime count remains coupled to C1, never an independent C2 pass.

Registration integrity is scoped honestly: C2's separate artifact-only assessment gate may reject declared late/unbound/inconsistent evidence, but self-authored timestamp strings or Git ancestry cannot prove that nobody measured an unrecorded sandbox earlier. Commit independent expectations before implementation and preserve runner receipts; disclose the evidence boundary rather than convert a 20-case selftest into twenty criteria or absolute chronology proof. Ground: round21 M3/M5/M6 and w1/reports/CriticRegistration.md, ConnIndependence.md. No criterion-count improvement is claimed this round.

Round-21 applications after W2 (no new numbered criterion): criterion12's named-verifier condition requires a complete non-absence identifier, not the `N` prefix of `N/A` or an explicitly author-only assessment. The gate still validates assertions rather than authenticating identity/dispatching lane; it cannot supply promotion clearance (lesson round21 M10; `w2/reports/GateShonenXWithoutNonauthor.md`). Criterion15's version/era check rejects an eager-definition annotation argument when the declared source profile is CPython3.14.8: S120 and the corrected `AtkClassAnnotation`/`AtkReturnAnnotation` reports distinguish lazy expressions from forced annotation evaluation (M11). Criterion31's demonstrated resource claim is the frozen assignment-only population, not a proof that every eager-call workload has linear retained storage; the bounded call-heavy observation and remaining complexity limit are retained in `w2/reports/ResourceMemory.md`.

32. A claimed binding repair separates lifetime, scope and callable identity: captured factory arguments/locals are bound at closure creation, module globals remain late-bound, a returned name follows the last executed local rebinding, and unresolved factory arguments never fall through to same-named globals as observed values. Synthetic helper state must not shadow a legal source identifier. Include independently specified stored/cross-cell lifetime, unknown-argument and reserved-name-collision counterexamples before claiming general repair; a finite direct-literal fixture pass is insufficient. Ground: lesson round21 M13, `residual/FinalBindingReview.md` F1–F5 and its six inert fixtures. This criterion is added after final falsification, supplies no retroactive pass and no numeric C2/criterion-count credit; delivered C1 fails it and remains harmed.

## Round 22 — applying existing lifetime and evidence criteria

No new numbered criterion or count credit. Criterion32's “bound at closure creation” means the enclosing factory frame and argument objects, not a deep-copy of every lexical value or the module namespace. S121 and `lessons/round-22.md` M1–M3 distinguish a caller name rebound later from an enclosing cell rebound before return, later nonlocal/object mutation, and a free global read at invocation. Preserve both literal and callable halves of the lexical overlay; an unknown parameter must shadow a same-named module callable as well as a literal. Renaming a synthetic key to another legal source identifier does not satisfy the hygiene bar.

Criteria30/31 and the original no-harm requirement cover added findings, removed findings, evidence relabels, per-file unparsed counters and bounded closure-heavy as well as assignment-only resources. A borrowed argv relabelled `lead` is still invented binding evidence. A definitely invalid factory invocation is not the same as dynamically unknown arguments; the independently sealed oracle must state whether a signal is semantically required before measurement.

Criteria7/9/10/24 and `lessons/round-22.md` M4 bind finding-row versus incident-line arithmetic and actual artifact labels. The markerless r19 raw receipt cannot be silently enriched or made green by treating missing evidence as observed. Later10-observed/1-lead rows or a6-line5/1 projection must name their derivation and never replace the original receipt, its rejection or the strict registered target. An artifact-only audit checks consistency, not the truth of a detector's marker, semantic precision, authenticated chronology or outside-lane admission.

## Criteria from the round-23 outside spot-check (round 24; routed defect 3)

33. A detector or gate repair earns no-harm credit only against discovery attacks frozen before the patch, not only the existing corpus, precision suite, oracles and selftests: base-versus-tip cases for global-store silent misses, recall shapes where base reports a lead and the candidate reports nothing, and frame or scope reuse, each kept with its outcome at both revisions. Check: `python3 -I .ufo/waves/round-24/quality/check-registration-order.py --round N` exits 1 when a `tools/` change precedes the first registered discovery population of round N (red on round 23, receipt `.ufo/waves/round-24/quality/m23-4-7-red-green.txt`). (lesson: lessons/round-23.md#mistakes M23-4)
34. A scratch measurement receipt counts only when writer and reader use the same absolute result paths, prior results are removed before each run, and the receipt names the sha256 of the tool bytes measured. Check: `python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py RECEIPT` exits 1 on a receipt with a relative result path or no measured-tool sha256 (red/green receipt `.ufo/waves/round-24/quality/m23-5-red-green.txt`). (lesson: lessons/round-23.md#mistakes M23-5)
35. A fixture first discovered after a patch is never credited as a pre-patch guard: register it, withdraw the affected production change to base, and assess a new patch only after registration. The round-23 wave-2 regression fixtures are registered at `.ufo/waves/round-24/carry/` (28 fixtures, manifest sha256 per file). Check: the same `check-registration-order.py --round N`. (lesson: lessons/round-23.md#mistakes M23-7)

## Criterion from the round-24 outside spot-check (round 25; routed defects 1–2)

36. A claim's counter is admitted only after controls that skip the claimed work have been built and scored under the frozen counter, and their receipts are committed before any data seat is created: the receipts name the shortcut shapes the closures have seen meet a counter (do-nothing, all-false/empty, junk, server echo, label- or fixture-keyed, no-reader), and a counter whose expected value the lane computes with its own model is replaced by an independent oracle or declared to measure only agreement with that model. Check: `python3 -I .ufo/waves/round-25/quality/check-control-receipts.py --round N --data-registry <data-wave registry>` exits 1 when the first control-receipt commit is not earlier than the data wave's `createdAt` or a named shape has no receipt; red on round 24 (`.ufo/waves/round-25/quality/q36-red-round24.txt`: receipts 1083 s after wave 1 was created). (lesson: lessons/round-24.md#mistakes M24-2, M24-5; lessons/round-25.md#mistakes)

## Criterion from the round-25 outside spot-check (round 26; routed defect 3, M25-4)

37. A predicate's population and its counter's population are one number: for every `PRED-<id> ... cases_pass=N/T` summary a receipt prints, the receipt's denominator T, its count of `CASE ` lines and the total T stated for the same `PRED-<id>` sentence in the registration must be equal, and a receipt naming a predicate with no registered total never counts as measuring that population. Check: `python3 -I .ufo/waves/round-26/quality/check-population.py --registration .ufo/waves/round-26/registration.md RECEIPT` exits 1 on any disagreement and 2 when the registration or a receipt cannot be read; green on both committed round-26 base receipts (C1 41 `CASE` lines at `cases_pass=0/41`, C2 51 at `cases_pass=22/51`) and on a synthetic 41-case receipt, red on fixtures dropping one `CASE` line, changing the printed denominator, changing the registration total and shrinking to a self-consistent `40/40` (`.ufo/waves/round-26/quality/q37-population-red-green.txt`). (lesson: lessons/round-25-verifier-spotcheck.md#7-routed-defects-lane-fixes-next-round item 3)
