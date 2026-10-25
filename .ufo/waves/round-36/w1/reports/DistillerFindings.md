# DistillerFindings — wave-1 findings, deduplicated

Seat: `L1Mado36.DistillerFindings` (simplifier). Date: 2026-10-25. Lane: mado-shokunin.

## Snapshot

- Reports read: **50** (all files present in `LANE/.ufo/waves/round-36/w1/reports/` at run time besides the registry; the registry lists 64 members).
- Seats whose reports had **not** landed at snapshot time: CritClaimSizing, CritFailClosed, CritSeparability, ExecReceiptForge, RevAcceptControls, RevFenceSemantics, RevPtrBefore, RevTipRule, ScoutConsiderRatio, ScoutInheritedTen, ScoutPriorArt2, ScribeFrontier, ScribeLessonGate, ScribeQualityCrit, ScribeQualityRatio, ScribeReportErrata, SimplifierGates.
- Normalization: each finding is keyed by the file/clause it concerns, the claim it touches (C1/C2/frontier/harm-watch) and its status; restatements of the same key across reports are merged.

## Counts

| metric | count |
|---|---|
| raw finding rows extracted | 88 |
| distinct rows after dedup/merge | 70 |
| merged rows (restatements collapsed) | 18 |

## Findings table

| # | Where it points | Claim | Status | Source seats | Finding (normalized) |
|---|---|---|---|---|---|
| F01 | `gate: manifest verification (identity/count/N)` | C1 | open (HIGH) | ConnGateReuse, CritManifestBalance, LabratGateOracle, RevAfterC1 | TARGET_MET reachable without repairs: trimmed manifest (14/14) with unmodified r35 counters, and echo-stub instruments passing the full manifest 25/25; no manifest id/N/control check; expect-flip on a manifest copy gives 25/25 exit 0 with unmodified r35 counters; one-control shrink gives 1/1; manifest sha256 appears nowhere; receipts name manifest by path/id only; 'frozen before data' not checkable from artifacts; manifest without id passes controls check then dies KeyError mid-loop; partial receipts, no verdict line |
| F02 | `manifest c1 reject-set coverage (digest/anchor + clause exercise)` | C1 | open (HIGH) | MutC1CheckAnchor, MutC1NoDigest, RevAfterC1 | removing anchor-cell digest test survives 25/25; digest-match controls never reach digest clauses (r35 cribs lack ## Registry; fence dominates); removing digest==receipt[sha256] conjunct survives 25/25; the D3 repair is not falsified by any landed c1 control; 13/14 c1 rejects return identical 0/0/8 observable; 10/11 repaired c1 clauses unexercised; r35 c1 + section rule alone scores 16/16 |
| F03 | `check-counter-discrimination.py / check-evidence-pointers.py: env` | C1 | open (HIGH) | SentGateExec | ambient GIT_* unscrubbed; GIT_DIR forced but overridable -> caller can spoof every git-backed observable |
| F04 | `check-counter-discrimination.py: receipt filename traversal` | C1 | open (HIGH) | SentGateExec | control['id'] unvalidated in receipt path (can write outside receipts_dir, e.g. forge axis receipts) |
| F05 | `manifest c1 reject-set one-input claim` | C1 | open (MEDIUM) | RevAfterC1 | manifest note 'differ from an accept in exactly one committed input' false for 9 c1 rejects (heading + cell both differ) |
| F06 | `check-counter-discrimination.py: /tmp fixture path` | C1 | open (MEDIUM) | SentGateExec | fixed predictable /tmp dir + unguarded rmtree: same-user race, foreign-owner DoS, --out recursive delete |
| F07 | `gate: verdict-token semantics (first-match; no exit agreement)` | C1 | open (LOW) | ConnGateReuse, CritManifestBalance, RevAfterC1 | first verdict-token wins (regex first match); prefix/met-context not enforced; instrument echoing spec text containing 'verdict' misclassifies; stdout+stderr merged so rc!=0/2 with MET token still scores MET; observed_of trusts verdict token over exit code for rc in {0,1}; a counter printing MET then dying would score MET |
| F08 | `c1-idle-lock.py: ## Registry fence` | C1 | open (LOW) | RevAfterC1 | section test is prefix match: '## Registry archive' heading is accepted; no control covers the looseness |
| F09 | `gen-mutants.py: c2 fixtures` | C1 | open (LOW) | RevAfterC1 | every c2 fixture clause ledger is +1 byte vs live (trailing newline); 'exactly one committed input' overstated |
| F10 | `check-counter-discrimination.py: receipt capture` | C1 | open (LOW) | SentGateExec | instrument stdout+stderr captured verbatim into committed receipts; with unscrubbed env could include credential-shaped output |
| F11 | `check-counter-discrimination.py: path traversal` | C1 | open (LOW) | SentGateExec | manifest/receipts/control roots resolved without containment from --repo; control['root'] can name any directory |
| F12 | `check-counter-discrimination.py: generator output parse` | C1 | open (LOW) | SentGateExec | line.split(' ') parse of generator output fails on dirs with spaces; wrong fixture could be scored |
| F13 | `check-counter-discrimination.py / gen-mutants.py: symlink writes` | C1 | open (LOW) | SentGateExec | writes follow symlinked intermediate components (defense-in-depth) |
| F14 | `c1 manifest: kill rule` | C1 | refuted | MutC1AcceptAll, MutC1RejectAll | always-accept mutant killed 11/25 by all 14 c1 reject controls; always-reject mutant killed 23/25 by the two c1 accept controls; correct sets disjoint across degenerates |
| F15 | `c1-idle-lock.py: ## Registry fence` | C1 | refuted | MutC1NoFence | fence removal killed 23/25 by c1-no-registry-heading and c1-row-moved-out |
| F16 | `c2 tip rule vs r35 substring rule` | C1 | refuted | MutC2HardcodedTip | r36 tip rule kills all four tip/blob mutants that the r35 substring rule survived |
| F17 | `measurement reproduction` | C1 | refuted | RevAfterC1 | 25/25 and 14/25 reproduce byte-identical to committed receipts; mixed old-counter/new-spec always predicate-drift ERROR; accepts load-bearing (one-input separation verified) |
| F18 | `before measurement` | C1 | refuted | RevDiscrimBefore | before 14/25 reproduces byte-identical; all 11 ok=0 lines attribute to D3/F2-E12/D4; no legitimate-reject-of-legitimate-control |
| F19 | `c1 digest byte-binding` | C1 | refuted | ExecDigestCribs | r36 counter rejects first-byte flip and anchored-real-sha alterations; accepts byte-identical rewrite; r35 accepts flip (D3); b3 accept-side intact |
| F20 | `c1 ## Registry fence vs census E12` | C1 | refuted | ScoutE12Source | census E12 selftest green; tab-indented table invisible; first-cell S[0-9]{3,} exact; E12 only in validate mode |
| F21 | `SCORECARD.md: C2 after-pin` | C2 | open (HIGH) | RevAfterC2 | scorecard line 2318 cites cf175c7 while receipt re-pinned to a5f76c9; at cf175c7 the claim is false (dangling_r36=3) |
| F22 | `C2 correction-pair/supersede semantics (as-frozen unsatisfiable; exemption unconstrained)` | C2 | open (HIGH) | RevAfterC2, RevPtrExtract, RevSupersedeBind | exemption is a global string set with unconstrained target; any dangling pointer can be laundered by a pair whose new is any existing file (e.g. LOG.md); as-frozen pair rule unsatisfiable (pair old-sides re-poison dangling_r36); supersession exemption closed it but exempts ANY pair old side, even never-dangling ones; pair-closure observable unreachable in pre-exemption gate; what actually passes is committing the absent paths so citations resolve; pair validator works when it runs |
| F23 | `check-evidence-pointers.py: dangling_r35_closed` | C2 | open (HIGH) | RevAfterC2 | closure satisfied by zero dangling plus 0-byte placeholders (resolves is existence-only); record_intact orthogonal to this branch |
| F24 | `check-evidence-pointers.py: D5 pair targets` | C2 | open (HIGH) | RevAfterC2 | pair 'new' unconstrained; retargeting both D5 pairs to LOG.md still closes (dangling_r35_closed=1) |
| F25 | `check-evidence-pointers.py: scratch_disposition_ok` | C2 | open (MEDIUM) | RevAfterC2 | substring match, not a disposition: a negated/self-contradicting sentence with the right 'tracked paths=N' passes |
| F26 | `check-evidence-pointers.py: inherited_dirty` | C2 | open (MEDIUM) | RevAfterC2 | inherited_dirty is a live-worktree reading, independent of --rev; docstring/scorecard claim committed bytes; receipts don't record checkout state or script blob |
| F27 | `check-evidence-pointers.py: pointer extraction` | C2 | open (MEDIUM) | RevAfterC2 | pointer class is a string-shape test: over-counts 3 pair-old sides, misses 8 lane-relative pointers (PATHY prefix allowlist; lesson scratch token dropped); pointers_r36 != count of cited pointers |
| F28 | `check-evidence-pointers.py: instrument identity in verdict` | C2 | open (MEDIUM) | RevAfterC2 | verdict line/receipt header carry no instrument blob; a different gate version can be replayed without detection |
| F29 | `round-35 report/count errata (D7/D1/D6)` | C2 | open (MEDIUM) | ScoutD1Facts, ScoutD6Rows, ScoutD7Counts | D7 upheld: 38 never committed; 37@4f35c80/7b745a1, 40@tip; erratum owed; RevScorecard unaccounted in parenthetical; D1 upheld: report did not land last (tip 7a068cb postdates last report commit); under author-date the tail is 4 commits, not 3; erratum sentence provided; D6 confirmed: three rows (S203-S205) corrected, cells scope/teaches/recheck; scorecard text fixed at 7d708cf; report erratum still owed |
| F30 | `S211 lesson anchor/trio + receipt identity rows` | C2 | open (MEDIUM) | RevSourceS211 | S211 quote still attributed to Introduction; it is section S2 paragraph P15; the lesson's own Gate block retracts it (self-contradiction); SOURCES.md fixed in worktree only; raw-HTML sha256 unreproducible by construction (rotating ncbi_phid/csrf tokens); receipt identity unfalsifiable; record extraction digest instead; lesson says 1,033 B; actual committed size 1,037 B |
| F31 | `gen-mutants.py: receipt path traversal` | C2 | open (MEDIUM) | SentGateExec | receipt_rels from ledger unvalidated; read/write outside dest/repo possible (secret-shaped bytes copied into /tmp fixtures) |
| F32 | `C2 tip_axis_transcript schema (rev binding, substrings)` | C2 | open (LOW) | ExecPtrFixtures, RevAxisTranscriptAsk | receipt binds rev, not instrument; hand-authored one-line file passes; substring looseness (mismatched=0x, rev=<hex>anything); MADO_AXIS line schema not enforced (bare substrings); filename HEX40 strict, line not strict |
| F33 | `axis publication: named derivation commit unverified` | C2 | open (LOW) | MutPublication, RevAxisNow | the named derivation commit in the publication is never checked; green with a nonexistent sha; publication could cite an older derivation commit and stay green while counts don't move; named commit is informational only |
| F34 | `axis publication: dirty worktree invisible` | C2 | open (LOW) | MutPublication | gate reads committed bytes only; an uncommitted publication edit is invisible; receipts must not be taken from a dirty tree |
| F35 | `LOG.md:417` | C2 | open (LOW) | RevShonen | stale 'Probation 4/4 [x] since round 5' while zero [x] exist since 7cd7f33 |
| F36 | `SHONEN.md box 2 pointer` | C2 | open (LOW) | RevShonen | box 2 cites 'LOG.md round 3 (VER-M3)'; VER-M3 is in the round-4 entry (LOG.md:294) |
| F37 | `SHONEN.md box 4 pointer` | C2 | open (LOW) | RevShonen | box 4 cites (VER-M4B); receipt does not name VER-M4B (grep 0) |
| F38 | `.ufo/waves/round-35/scratch size/kind claim` | C2 | open (LOW) | ScoutDisposition124 | count 124 verified; size 1.87 MiB not 2.2 MB (~10% overstated); 'm1-m9' off by one (m6 never existed); stale CritAxisClaims README uncited |
| F39 | `c2 clause-pin duplicate blind spot` | C2 | open (LOW) | ExecClausePins, MutC2NoClausePin | pin compares id sets; a duplicated live id scores zero uncovered (no c2-*-duplicate control exists); live list with one controlled clause duplicated passes TARGET_MET (set equality blind to multiplicity; 'exactly one declaration' only fires for declared duplicates) |
| F40 | `check-evidence-pointers.py: git() fail-open` | C2 | open (LOW) | SentGateExec | git() returns '' on failure; broken git -> inherited_dirty=0 passes; --rev/--branch unvalidated (option confusion) |
| F41 | `D9 provenance-trio policy and ownership` | C2 | needs L1 | ScoutD9Provenance, ScoutRound35Defects | 21/50 notes lack anchored trio in head-15 (20 pre-trio-era, 1 partial); append-only trailer policy proposed; no gate observable and no owner for the edit; D9 is the weakest-covered routed defect: no gate observable scores corpus form, no seat owns normalization; L1/round-end decision owed |
| F42 | `c2 receipt binding` | C2 | refuted | MutC2NoReceiptBind | token-grep regression caught by c2-receipt-token/unbound; binding is exactly what kills them |
| F43 | `c2 blob-table parse` | C2 | refuted | MutC2NoTable | dropping the document-table parse lets both blob mutants survive; the parse is the only observable killing them |
| F44 | `c2 clause pin` | C2 | refuted | ExecClausePins | pin holds for delete/not-load-bearing/retired/duplicate-declared fixtures; fresh implementation byte-identical to lane counter |
| F45 | `check-evidence-pointers.py: tracked paths=N equality` | C2 | refuted | MutPtrDisposition | equality load-bearing; wrong count and no-count disposition lines rejected honestly |
| F46 | `check-evidence-pointers.py: dangling counter` | C2 | refuted | MutPtrExistingOnly | dangling-count-only-existing is vacuous (flips verdict at master while D5 uncorrected); honest gate rejects; hardening note |
| F47 | `check-evidence-pointers.py: setup_ok` | C2 | refuted | MutPtrNoSetup | absence-is-a-pass guard load-bearing; no-sections tree exits 1 only via setup_ok conjunct |
| F48 | `check-evidence-pointers.py: tip_axis_transcript checks` | C2 | refuted | MutPtrTipAncestor | ancestor and rev= checks both load-bearing; fabricated non-ancestor and rev-mismatch receipts rejected |
| F49 | `check-evidence-pointers.py: tip fixtures` | C2 | refuted | ExecPtrFixtures | all four fixture classes discriminated as designed; positive passes; poisoning by non-ancestor receipt does not invalidate correct sibling |
| F50 | `check-evidence-pointers.py: record_intact` | C2 | refuted | RevRecordIntact | record_intact is the operative anti-rewrite guard; deleting mentions gives dangling_r35=0 but closed=0 |
| F51 | `LOG.md D5 pairs` | C2 | refuted | RevSupersedeBind | both D5 pairs honest and closable (scratch-evidence carries count-min.py 104 lines, analysis.md, gen_and_run.py, results.json); no dangling pointer a pair cannot honestly close |
| F52 | `check-evidence-pointers.py: after measurement` | C2 | refuted | RevAfterC2 | TARGET_MET at f77b554 reproduces byte-identical to after-pointers.txt; planted dangling pointer in r36 section caught and named; before-state reproduces too |
| F53 | `check-evidence-pointers.py: plants` | C2 | refuted | RevPtrExtract | all four planted defects (nonexistent file, bad new, deleted r35 lines, empty glob) caught on the first line they touch |
| F54 | `LOG.md/SCORECARD.md round-36 form` | C2 | refuted | RevLogScaffold | heading/citation/pair form identified and verified; adjacent observables (lesson, disposition, axis receipt) also required by setup |
| F55 | `quality/check-index-rows.py exists_glob` | frontier | open (LOW) | RevIndexGate | rev-mode exists_glob broken under git 2.56 (--format+--name-only fatal; swallowed -> warns=3 false positives); --root mode clean |
| F56 | `prompt/CORPUS.md reference` | frontier | open (LOW) | ScoutD9Provenance | no CORPUS.md exists anywhere; trio convention is real and documented elsewhere; prompt references a non-existent file |
| F57 | `corpus/SOURCES.md S211 anchor` | frontier | open (LOW) | ScoutPriorArt | S211 already cites the same paper with loose anchor; tighter anchor (#S2/P15) and verbatim quote supplied; update in place rather than duplicate |
| F58 | `PROVINCE refusal boundary statement (D9)` | frontier | needs L1 | CritD9Boundary | localization refusal boundary practised only; no PROVINCE sentence states it; one-sentence fix proposed (channel rule keeping omarchy ownership) |
| F59 | `round report phrasing: sibling boundary` | frontier | needs L1 | ConnOverlap | tameshi owns mutation-testing method; evidence-pointer audit instrument class held by kaidoku/kagi/chousa; report must keep claims lane-scoped (PROVINCE.md:20,28,62-65) |
| F60 | `ScoutPriorArt/ScoutPriorArt2 availability` | frontier | refuted | RevSourceQuotes | scout reports were absent at RevSourceQuotes run time (agentId null); both quotes self-verified (Lipsitch 25w contiguous; Papadakis 17w); LWW Cloudflare-blocked, PMC used |
| F61 | `primary-source row` | frontier | refuted | ScoutPriorArt | Lipsitch et al. 2010 opened and verified (PMC3053408, #S1/P8, 22-word quote); licenses kill rule, does not license instrument-correctness claims |
| F62 | `registration.md:156 harm-watch command` | harm-watch | open (LOW) | RevIndexGate | assigned `python3 quality/check-index.py --repo .` exits 2 (--rev/--root required); correct forms verified green |
| F63 | `PROVINCE.md post-freeze modification` | harm-watch | needs L1 | SentBoundary | PROVINCE.md modified after freeze; consistent with L1 round-open housekeeping but no w1 seat prompt grants it; confirm authorship (or a breach) |
| F64 | `tools/mado-verify.sh` | harm-watch | refuted | RevSelftest | selftest green 460/460 exit 0 at freeze; bytes identical to r35 tip 7a068cb |
| F65 | `scripts/sources-census.sh validate` | harm-watch | refuted | RevCensusNow | exit 0; 200 rows; W04 set identical to lesson before/after; byte-identical to r35 after-block |
| F66 | `corpus/SOURCES.md` | harm-watch | refuted | RevRowsUnchanged | no commits touch the path in 7a068cb..master; byte-identical sha256; 200 data rows at both |
| F67 | `host config planes` | harm-watch | refuted | ScoutHostProbe | all 14 sha-pinned declared files match latest pins; walker 2.17.2 drift already ledgered; gkeep.conf intentionally pinless by shape |
| F68 | `fleet root strays` | harm-watch | refuted | RevFleetMisroot | zero stray mado r36 lane files; no fleet-side round-36 wave dir; all hits canonical |
| F69 | `write-boundary audit` | harm-watch | refuted | SentBoundary | no seat write outside reports/scratch at snapshot; frozen bytes intact; only tracked modification is PROVINCE.md (attributed to L1) |
| F70 | `SCORECARD.md axis fractions` | harm-watch | refuted | RevAxisNow | all three published fractions re-derive MATCH at master (dbf8b57); gate selftest 18/18; negative/STALE controls reproduce |

## Status legend

- **open** — an actionable defect/gap on the current bytes (counter, gate, manifest, record, or security posture); severity in parentheses.
- **refuted** — the probed defect/harm did not materialize: the tested attack failed, the baseline held, or the finding confirms load-bearing behavior of the shipped instrument.
- **needs L1** — a decision or application owned by the L1 (production edits, policy phrasing, authorship confirmation); the seat cannot apply it under read-only bounds.

## Coverage note

The 50 read reports cover all 64 registry members except the 17 listed above (Scribe seats may deliver to scratch instead of the reports dir; ScoutPriorArt2 was observed unassigned by RevSourceQuotes). Findings are normalized per file/clause, so late reports for the same targets would merge into the rows above.