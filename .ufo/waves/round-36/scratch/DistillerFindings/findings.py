# -*- coding: utf-8 -*-
# Raw findings as extracted from the 50 reports present at snapshot time.
# Fields: seat (report author), target (file/clause the finding concerns),
#         claim (C1/C2/frontier/harm-watch), status (open/refuted/needs L1),
#         sev (severity for open/needs-L1 rows), text.
RAW = [
# --- C1: calibration ---
dict(seat="LabratGateOracle", target="quality/check-counter-discrimination.py: manifest authenticity", claim="C1", status="open", sev="HIGH", text="TARGET_MET reachable without repairs: trimmed manifest (14/14) with unmodified r35 counters, and echo-stub instruments passing the full manifest 25/25; no manifest id/N/control check"),
dict(seat="CritManifestBalance", target="quality/check-counter-discrimination.py: manifest authenticity", claim="C1", status="open", sev="HIGH", text="expect-flip on a manifest copy gives 25/25 exit 0 with unmodified r35 counters; one-control shrink gives 1/1"),
dict(seat="RevAfterC1", target="quality/check-counter-discrimination.py: manifest/bytes binding", claim="C1", status="open", sev="LOW", text="manifest sha256 appears nowhere; receipts name manifest by path/id only; 'frozen before data' not checkable from artifacts"),
dict(seat="ConnGateReuse", target="quality/check-counter-discrimination.py: manifest['id']", claim="C1", status="open", sev="LOW", text="manifest without id passes controls check then dies KeyError mid-loop; partial receipts, no verdict line"),
dict(seat="CritManifestBalance", target="quality/check-counter-discrimination.py: verdict token parse", claim="C1", status="open", sev="LOW", text="first verdict-token wins (regex first match); prefix/met-context not enforced"),
dict(seat="ConnGateReuse", target="quality/check-counter-discrimination.py: verdict token parse", claim="C1", status="open", sev="LOW", text="instrument echoing spec text containing 'verdict' misclassifies; stdout+stderr merged so rc!=0/2 with MET token still scores MET"),
dict(seat="RevAfterC1", target="quality/check-counter-discrimination.py: verdict/exit agreement", claim="C1", status="open", sev="LOW", text="observed_of trusts verdict token over exit code for rc in {0,1}; a counter printing MET then dying would score MET"),
dict(seat="MutC1CheckAnchor", target="c1 manifest reject set: digest-match/anchor clause", claim="C1", status="open", sev="HIGH", text="removing anchor-cell digest test survives 25/25; digest-match controls never reach digest clauses (r35 cribs lack ## Registry; fence dominates)"),
dict(seat="MutC1NoDigest", target="c1 manifest reject set: digest-match/bytes clause", claim="C1", status="open", sev="HIGH", text="removing digest==receipt[sha256] conjunct survives 25/25; the D3 repair is not falsified by any landed c1 control"),
dict(seat="RevAfterC1", target="c1 manifest reject set: clause exercise", claim="C1", status="open", sev="MEDIUM", text="13/14 c1 rejects return identical 0/0/8 observable; 10/11 repaired c1 clauses unexercised; r35 c1 + section rule alone scores 16/16"),
dict(seat="RevAfterC1", target="c1 manifest reject set: one-input claim", claim="C1", status="open", sev="MEDIUM", text="manifest note 'differ from an accept in exactly one committed input' false for 9 c1 rejects (heading + cell both differ)"),
dict(seat="RevAfterC1", target="c1-idle-lock.py: ## Registry fence", claim="C1", status="open", sev="LOW", text="section test is prefix match: '## Registry archive' heading is accepted; no control covers the looseness"),
dict(seat="RevAfterC1", target="gen-mutants.py: c2 fixtures", claim="C1", status="open", sev="LOW", text="every c2 fixture clause ledger is +1 byte vs live (trailing newline); 'exactly one committed input' overstated"),
dict(seat="MutC1AcceptAll", target="c1 manifest: kill rule", claim="C1", status="refuted", sev="", text="always-accept mutant killed 11/25 by all 14 c1 reject controls"),
dict(seat="MutC1RejectAll", target="c1 manifest: kill rule", claim="C1", status="refuted", sev="", text="always-reject mutant killed 23/25 by the two c1 accept controls; correct sets disjoint across degenerates"),
dict(seat="MutC1NoFence", target="c1-idle-lock.py: ## Registry fence", claim="C1", status="refuted", sev="", text="fence removal killed 23/25 by c1-no-registry-heading and c1-row-moved-out"),
dict(seat="MutC2HardcodedTip", target="c2 tip rule vs r35 substring rule", claim="C1", status="refuted", sev="", text="r36 tip rule kills all four tip/blob mutants that the r35 substring rule survived"),
dict(seat="RevAfterC1", target="measurement reproduction", claim="C1", status="refuted", sev="", text="25/25 and 14/25 reproduce byte-identical to committed receipts; mixed old-counter/new-spec always predicate-drift ERROR; accepts load-bearing (one-input separation verified)"),
dict(seat="RevDiscrimBefore", target="before measurement", claim="C1", status="refuted", sev="", text="before 14/25 reproduces byte-identical; all 11 ok=0 lines attribute to D3/F2-E12/D4; no legitimate-reject-of-legitimate-control"),
dict(seat="ExecDigestCribs", target="c1 digest byte-binding", claim="C1", status="refuted", sev="", text="r36 counter rejects first-byte flip and anchored-real-sha alterations; accepts byte-identical rewrite; r35 accepts flip (D3); b3 accept-side intact"),
dict(seat="RevFenceSemantics", target="c1 ## Registry fence vs census E12", claim="C1", status="refuted", sev="", text="E12 rules recorded: exact 'Registry' head, 0-3 spaces, 4-space/tab invisible, ### doesn't toggle; fence reproduces them"),
dict(seat="ScoutE12Source", target="c1 ## Registry fence vs census E12", claim="C1", status="refuted", sev="", text="census E12 selftest green; tab-indented table invisible; first-cell S[0-9]{3,} exact; E12 only in validate mode"),
# --- C2: operability ---
dict(seat="RevAfterC2", target="SCORECARD.md: C2 after-pin", claim="C2", status="open", sev="HIGH", text="scorecard line 2318 cites cf175c7 while receipt re-pinned to a5f76c9; at cf175c7 the claim is false (dangling_r36=3)"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: supersede exemption", claim="C2", status="open", sev="HIGH", text="exemption is a global string set with unconstrained target; any dangling pointer can be laundered by a pair whose new is any existing file (e.g. LOG.md)"),
dict(seat="RevSupersedeBind", target="check-evidence-pointers.py: correction-pair rule", claim="C2", status="open", sev="HIGH", text="as-frozen pair rule unsatisfiable (pair old-sides re-poison dangling_r36); supersession exemption closed it but exempts ANY pair old side, even never-dangling ones"),
dict(seat="RevPtrExtract", target="check-evidence-pointers.py: pair closure", claim="C2", status="open", sev="MEDIUM", text="pair-closure observable unreachable in pre-exemption gate; what actually passes is committing the absent paths so citations resolve; pair validator works when it runs"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: dangling_r35_closed", claim="C2", status="open", sev="HIGH", text="closure satisfied by zero dangling plus 0-byte placeholders (resolves is existence-only); record_intact orthogonal to this branch"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: D5 pair targets", claim="C2", status="open", sev="HIGH", text="pair 'new' unconstrained; retargeting both D5 pairs to LOG.md still closes (dangling_r35_closed=1)"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: scratch_disposition_ok", claim="C2", status="open", sev="MEDIUM", text="substring match, not a disposition: a negated/self-contradicting sentence with the right 'tracked paths=N' passes"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: inherited_dirty", claim="C2", status="open", sev="MEDIUM", text="inherited_dirty is a live-worktree reading, independent of --rev; docstring/scorecard claim committed bytes; receipts don't record checkout state or script blob"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: pointer extraction", claim="C2", status="open", sev="MEDIUM", text="pointer class is a string-shape test: over-counts 3 pair-old sides, misses 8 lane-relative pointers (PATHY prefix allowlist; lesson scratch token dropped); pointers_r36 != count of cited pointers"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: instrument identity in verdict", claim="C2", status="open", sev="MEDIUM", text="verdict line/receipt header carry no instrument blob; a different gate version can be replayed without detection"),
dict(seat="RevAxisTranscriptAsk", target="check-evidence-pointers.py: tip_axis_transcript", claim="C2", status="open", sev="LOW", text="receipt binds rev, not instrument; hand-authored one-line file passes; substring looseness (mismatched=0x, rev=<hex>anything)"),
dict(seat="ExecPtrFixtures", target="check-evidence-pointers.py: tip_axis_transcript", claim="C2", status="open", sev="LOW", text="MADO_AXIS line schema not enforced (bare substrings); filename HEX40 strict, line not strict"),
dict(seat="MutPublication", target="check-axis-scores.py: publication anchor", claim="C2", status="open", sev="LOW", text="the named derivation commit in the publication is never checked; green with a nonexistent sha"),
dict(seat="RevAxisNow", target="check-axis-scores.py: publication anchor", claim="C2", status="open", sev="LOW", text="publication could cite an older derivation commit and stay green while counts don't move; named commit is informational only"),
dict(seat="MutPublication", target="check-axis-scores.py: dirty worktree", claim="C2", status="open", sev="LOW", text="gate reads committed bytes only; an uncommitted publication edit is invisible; receipts must not be taken from a dirty tree"),
dict(seat="ScoutD7Counts", target="fleet report round-35: '38 reports'", claim="C2", status="open", sev="MEDIUM", text="D7 upheld: 38 never committed; 37@4f35c80/7b745a1, 40@tip; erratum owed; RevScorecard unaccounted in parenthetical"),
dict(seat="ScoutD1Facts", target="fleet report round-35: ordering/tip", claim="C2", status="open", sev="MEDIUM", text="D1 upheld: report did not land last (tip 7a068cb postdates last report commit); under author-date the tail is 4 commits, not 3; erratum sentence provided"),
dict(seat="ScoutD6Rows", target="round-35 scorecard/report: row-correction count", claim="C2", status="open", sev="LOW", text="D6 confirmed: three rows (S203-S205) corrected, cells scope/teaches/recheck; scorecard text fixed at 7d708cf; report erratum still owed"),
dict(seat="RevSourceS211", target="corpus/lessons/round-36.md:74", claim="C2", status="open", sev="MEDIUM", text="S211 quote still attributed to Introduction; it is section S2 paragraph P15; the lesson's own Gate block retracts it (self-contradiction); SOURCES.md fixed in worktree only"),
dict(seat="RevSourceS211", target=".ufo/waves/round-36/fetch/S211.receipt.txt", claim="C2", status="open", sev="LOW", text="raw-HTML sha256 unreproducible by construction (rotating ncbi_phid/csrf tokens); receipt identity unfalsifiable; record extraction digest instead"),
dict(seat="RevSourceS211", target="corpus/lessons/round-36.md: receipt size", claim="C2", status="open", sev="LOW", text="lesson says 1,033 B; actual committed size 1,037 B"),
dict(seat="RevShonen", target="LOG.md:417", claim="C2", status="open", sev="LOW", text="stale 'Probation 4/4 [x] since round 5' while zero [x] exist since 7cd7f33"),
dict(seat="RevShonen", target="SHONEN.md box 2 pointer", claim="C2", status="open", sev="LOW", text="box 2 cites 'LOG.md round 3 (VER-M3)'; VER-M3 is in the round-4 entry (LOG.md:294)"),
dict(seat="RevShonen", target="SHONEN.md box 4 pointer", claim="C2", status="open", sev="LOW", text="box 4 cites (VER-M4B); receipt does not name VER-M4B (grep 0)"),
dict(seat="ScoutDisposition124", target=".ufo/waves/round-35/scratch size/kind claim", claim="C2", status="open", sev="LOW", text="count 124 verified; size 1.87 MiB not 2.2 MB (~10% overstated); 'm1-m9' off by one (m6 never existed); stale CritAxisClaims README uncited"),
dict(seat="ScoutD9Provenance", target="corpus/knowledge provenance trio", claim="C2", status="needs L1", sev="", text="21/50 notes lack anchored trio in head-15 (20 pre-trio-era, 1 partial); append-only trailer policy proposed; no gate observable and no owner for the edit"),
dict(seat="ScoutRound35Defects", target="D9 disposition", claim="C2", status="needs L1", sev="", text="D9 is the weakest-covered routed defect: no gate observable scores corpus form, no seat owns normalization; L1/round-end decision owed"),
dict(seat="CritD9Boundary", target="PROVINCE.md refuses boundary", claim="frontier", status="needs L1", sev="", text="localization refusal boundary practised only; no PROVINCE sentence states it; one-sentence fix proposed (channel rule keeping omarchy ownership)"),
dict(seat="MutC2NoClausePin", target="c2 clause pin: set arithmetic", claim="C2", status="open", sev="LOW", text="pin compares id sets; a duplicated live id scores zero uncovered (no c2-*-duplicate control exists)"),
dict(seat="ExecClausePins", target="c2 clause pin: duplicated controlled clause", claim="C2", status="open", sev="LOW", text="live list with one controlled clause duplicated passes TARGET_MET (set equality blind to multiplicity; 'exactly one declaration' only fires for declared duplicates)"),
dict(seat="MutC2NoReceiptBind", target="c2 receipt binding", claim="C2", status="refuted", sev="", text="token-grep regression caught by c2-receipt-token/unbound; binding is exactly what kills them"),
dict(seat="MutC2NoTable", target="c2 blob-table parse", claim="C2", status="refuted", sev="", text="dropping the document-table parse lets both blob mutants survive; the parse is the only observable killing them"),
dict(seat="ExecClausePins", target="c2 clause pin", claim="C2", status="refuted", sev="", text="pin holds for delete/not-load-bearing/retired/duplicate-declared fixtures; fresh implementation byte-identical to lane counter"),
dict(seat="MutPtrDisposition", target="check-evidence-pointers.py: tracked paths=N equality", claim="C2", status="refuted", sev="", text="equality load-bearing; wrong count and no-count disposition lines rejected honestly"),
dict(seat="MutPtrExistingOnly", target="check-evidence-pointers.py: dangling counter", claim="C2", status="refuted", sev="", text="dangling-count-only-existing is vacuous (flips verdict at master while D5 uncorrected); honest gate rejects; hardening note"),
dict(seat="MutPtrNoSetup", target="check-evidence-pointers.py: setup_ok", claim="C2", status="refuted", sev="", text="absence-is-a-pass guard load-bearing; no-sections tree exits 1 only via setup_ok conjunct"),
dict(seat="MutPtrTipAncestor", target="check-evidence-pointers.py: tip_axis_transcript checks", claim="C2", status="refuted", sev="", text="ancestor and rev= checks both load-bearing; fabricated non-ancestor and rev-mismatch receipts rejected"),
dict(seat="ExecPtrFixtures", target="check-evidence-pointers.py: tip fixtures", claim="C2", status="refuted", sev="", text="all four fixture classes discriminated as designed; positive passes; poisoning by non-ancestor receipt does not invalidate correct sibling"),
dict(seat="RevRecordIntact", target="check-evidence-pointers.py: record_intact", claim="C2", status="refuted", sev="", text="record_intact is the operative anti-rewrite guard; deleting mentions gives dangling_r35=0 but closed=0"),
dict(seat="RevSupersedeBind", target="LOG.md D5 pairs", claim="C2", status="refuted", sev="", text="both D5 pairs honest and closable (scratch-evidence carries count-min.py 104 lines, analysis.md, gen_and_run.py, results.json); no dangling pointer a pair cannot honestly close"),
dict(seat="RevAfterC2", target="check-evidence-pointers.py: after measurement", claim="C2", status="refuted", sev="", text="TARGET_MET at f77b554 reproduces byte-identical to after-pointers.txt; planted dangling pointer in r36 section caught and named; before-state reproduces too"),
dict(seat="RevPtrExtract", target="check-evidence-pointers.py: plants", claim="C2", status="refuted", sev="", text="all four planted defects (nonexistent file, bad new, deleted r35 lines, empty glob) caught on the first line they touch"),
dict(seat="RevLogScaffold", target="LOG.md/SCORECARD.md round-36 form", claim="C2", status="refuted", sev="", text="heading/citation/pair form identified and verified; adjacent observables (lesson, disposition, axis receipt) also required by setup"),
# --- frontier ---
dict(seat="RevIndexGate", target="registration.md:156 harm-watch command", claim="harm-watch", status="open", sev="LOW", text="assigned `python3 quality/check-index.py --repo .` exits 2 (--rev/--root required); correct forms verified green"),
dict(seat="RevIndexGate", target="quality/check-index-rows.py exists_glob", claim="frontier", status="open", sev="LOW", text="rev-mode exists_glob broken under git 2.56 (--format+--name-only fatal; swallowed -> warns=3 false positives); --root mode clean"),
dict(seat="ScoutD9Provenance", target="prompt/CORPUS.md reference", claim="frontier", status="open", sev="LOW", text="no CORPUS.md exists anywhere; trio convention is real and documented elsewhere; prompt references a non-existent file"),
dict(seat="ScoutPriorArt", target="corpus/SOURCES.md S211 anchor", claim="frontier", status="open", sev="LOW", text="S211 already cites the same paper with loose anchor; tighter anchor (#S2/P15) and verbatim quote supplied; update in place rather than duplicate"),
dict(seat="ConnOverlap", target="round report phrasing: sibling boundary", claim="frontier", status="needs L1", sev="", text="tameshi owns mutation-testing method; evidence-pointer audit instrument class held by kaidoku/kagi/chousa; report must keep claims lane-scoped (PROVINCE.md:20,28,62-65)"),
dict(seat="RevSourceQuotes", target="ScoutPriorArt/ScoutPriorArt2 availability", claim="frontier", status="refuted", sev="", text="scout reports were absent at RevSourceQuotes run time (agentId null); both quotes self-verified (Lipsitch 25w contiguous; Papadakis 17w); LWW Cloudflare-blocked, PMC used"),
dict(seat="ScoutPriorArt", target="primary-source row", claim="frontier", status="refuted", sev="", text="Lipsitch et al. 2010 opened and verified (PMC3053408, #S1/P8, 22-word quote); licenses kill rule, does not license instrument-correctness claims"),
# --- harm-watch ---
dict(seat="RevSelftest", target="tools/mado-verify.sh", claim="harm-watch", status="refuted", sev="", text="selftest green 460/460 exit 0 at freeze; bytes identical to r35 tip 7a068cb"),
dict(seat="RevCensusNow", target="scripts/sources-census.sh validate", claim="harm-watch", status="refuted", sev="", text="exit 0; 200 rows; W04 set identical to lesson before/after; byte-identical to r35 after-block"),
dict(seat="RevRowsUnchanged", target="corpus/SOURCES.md", claim="harm-watch", status="refuted", sev="", text="no commits touch the path in 7a068cb..master; byte-identical sha256; 200 data rows at both"),
dict(seat="ScoutHostProbe", target="host config planes", claim="harm-watch", status="refuted", sev="", text="all 14 sha-pinned declared files match latest pins; walker 2.17.2 drift already ledgered; gkeep.conf intentionally pinless by shape"),
dict(seat="RevFleetMisroot", target="fleet root strays", claim="harm-watch", status="refuted", sev="", text="zero stray mado r36 lane files; no fleet-side round-36 wave dir; all hits canonical"),
dict(seat="SentBoundary", target="write-boundary audit", claim="harm-watch", status="refuted", sev="", text="no seat write outside reports/scratch at snapshot; frozen bytes intact; only tracked modification is PROVINCE.md (attributed to L1)"),
dict(seat="SentBoundary", target="PROVINCE.md post-freeze modification", claim="harm-watch", status="needs L1", sev="", text="PROVINCE.md modified after freeze; consistent with L1 round-open housekeeping but no w1 seat prompt grants it; confirm authorship (or a breach)"),
dict(seat="RevAxisNow", target="SCORECARD.md axis fractions", claim="harm-watch", status="refuted", sev="", text="all three published fractions re-derive MATCH at master (dbf8b57); gate selftest 18/18; negative/STALE controls reproduce"),
# --- security (C1/C2 instrumentation) ---
dict(seat="SentGateExec", target="check-counter-discrimination.py / check-evidence-pointers.py: env", claim="C1", status="open", sev="HIGH", text="ambient GIT_* unscrubbed; GIT_DIR forced but overridable -> caller can spoof every git-backed observable"),
dict(seat="SentGateExec", target="check-counter-discrimination.py: receipt filename traversal", claim="C1", status="open", sev="HIGH", text="control['id'] unvalidated in receipt path (can write outside receipts_dir, e.g. forge axis receipts)"),
dict(seat="SentGateExec", target="gen-mutants.py: receipt path traversal", claim="C2", status="open", sev="MEDIUM", text="receipt_rels from ledger unvalidated; read/write outside dest/repo possible (secret-shaped bytes copied into /tmp fixtures)"),
dict(seat="SentGateExec", target="check-counter-discrimination.py: /tmp fixture path", claim="C1", status="open", sev="MEDIUM", text="fixed predictable /tmp dir + unguarded rmtree: same-user race, foreign-owner DoS, --out recursive delete"),
dict(seat="SentGateExec", target="check-counter-discrimination.py: receipt capture", claim="C1", status="open", sev="LOW", text="instrument stdout+stderr captured verbatim into committed receipts; with unscrubbed env could include credential-shaped output"),
dict(seat="SentGateExec", target="check-evidence-pointers.py: git() fail-open", claim="C2", status="open", sev="LOW", text="git() returns '' on failure; broken git -> inherited_dirty=0 passes; --rev/--branch unvalidated (option confusion)"),
dict(seat="SentGateExec", target="check-counter-discrimination.py: path traversal", claim="C1", status="open", sev="LOW", text="manifest/receipts/control roots resolved without containment from --repo; control['root'] can name any directory"),
dict(seat="SentGateExec", target="check-counter-discrimination.py: generator output parse", claim="C1", status="open", sev="LOW", text="line.split(' ') parse of generator output fails on dirs with spaces; wrong fixture could be scored"),
dict(seat="SentGateExec", target="check-counter-discrimination.py / gen-mutants.py: symlink writes", claim="C1", status="open", sev="LOW", text="writes follow symlinked intermediate components (defense-in-depth)"),
]

MISSING_SEATS = ["CritClaimSizing","CritFailClosed","CritSeparability","ExecReceiptForge","RevAcceptControls","RevFenceSemantics","RevPtrBefore","RevTipRule","ScoutConsiderRatio","ScoutInheritedTen","ScoutPriorArt2","ScribeFrontier","ScribeLessonGate","ScribeQualityCrit","ScribeQualityRatio","ScribeReportErrata","SimplifierGates"]

# remove mistaken attribution (RevFenceSemantics has not landed; E12 facts came from ScoutE12Source)
RAW = [r for r in RAW if not (r["seat"]=="RevFenceSemantics")]

CANON = {
 "quality/check-counter-discrimination.py: manifest authenticity": "gate: manifest verification (identity/count/N)",
 "quality/check-counter-discrimination.py: manifest/bytes binding": "gate: manifest verification (identity/count/N)",
 "quality/check-counter-discrimination.py: manifest['id']": "gate: manifest verification (identity/count/N)",
 "quality/check-counter-discrimination.py: verdict token parse": "gate: verdict-token semantics (first-match; no exit agreement)",
 "quality/check-counter-discrimination.py: verdict/exit agreement": "gate: verdict-token semantics (first-match; no exit agreement)",
 "c1 manifest reject set: digest-match/anchor clause": "manifest c1 reject-set coverage (digest/anchor + clause exercise)",
 "c1 manifest reject set: digest-match/bytes clause": "manifest c1 reject-set coverage (digest/anchor + clause exercise)",
 "c1 manifest reject set: clause exercise": "manifest c1 reject-set coverage (digest/anchor + clause exercise)",
 "c1 manifest reject set: one-input claim": "manifest c1 reject-set one-input claim",
 "check-evidence-pointers.py: tip_axis_transcript": "C2 tip_axis_transcript schema (rev binding, substrings)",
 "check-evidence-pointers.py: supersede exemption": "C2 correction-pair/supersede semantics (as-frozen unsatisfiable; exemption unconstrained)",
 "check-evidence-pointers.py: correction-pair rule": "C2 correction-pair/supersede semantics (as-frozen unsatisfiable; exemption unconstrained)",
 "check-evidence-pointers.py: pair closure": "C2 correction-pair/supersede semantics (as-frozen unsatisfiable; exemption unconstrained)",
 "c2 clause pin: set arithmetic": "c2 clause-pin duplicate blind spot",
 "c2 clause pin: duplicated controlled clause": "c2 clause-pin duplicate blind spot",
 "check-axis-scores.py: publication anchor": "axis publication: named derivation commit unverified",
 "check-axis-scores.py: dirty worktree": "axis publication: dirty worktree invisible",
 "reg.md:156 harm-watch command": "registration harm-watch command shape (--repo . exits 2)",
 "fleet report round-35: '38 reports'": "round-35 report/count errata (D7/D1/D6)",
 "fleet report round-35: ordering/tip": "round-35 report/count errata (D7/D1/D6)",
 "round-35 scorecard/report: row-correction count": "round-35 report/count errata (D7/D1/D6)",
 "corpus/lessons/round-36.md:74": "S211 lesson anchor/trio + receipt identity rows",
 ".ufo/waves/round-36/fetch/S211.receipt.txt": "S211 lesson anchor/trio + receipt identity rows",
 "corpus/lessons/round-36.md: receipt size": "S211 lesson anchor/trio + receipt identity rows",
 "corpus/knowledge provenance trio": "D9 provenance-trio policy and ownership",
 "D9 disposition": "D9 provenance-trio policy and ownership",
 "PROVINCE.md refuses boundary": "PROVINCE refusal boundary statement (D9)",
}

def canon(r):
    return (CANON.get(r["target"], r["target"]), r["claim"], r["status"])

from collections import OrderedDict
groups = OrderedDict()
for r in RAW:
    key = canon(r)
    groups.setdefault(key, []).append(r)

raw_n = len(RAW)
distinct_n = len(groups)
merged_n = raw_n - distinct_n

rows = []
for key, items in groups.items():
    target, claim, status = key
    sev = max((i["sev"] for i in items if i["sev"]), key=lambda x: {"HIGH":3,"MEDIUM":2,"LOW":1}.get(x,0), default="")
    seats = sorted({i["seat"] for i in items})
    texts = []
    for i in items:
        t = i["text"]
        if t not in texts:
            texts.append(t)
    rows.append(dict(target=target, claim=claim, status=status, sev=sev,
                     seats=", ".join(seats), text="; ".join(texts), n=len(items)))

# order: C1, C2, frontier, harm-watch; then open first, needs L1, refuted
claim_order = {"C1":0, "C2":1, "frontier":2, "harm-watch":3}
status_order = {"open":0, "needs L1":1, "refuted":2}
rows.sort(key=lambda r: (claim_order[r["claim"]], status_order[r["status"]], -len(r["sev"])))

print(f"RAW={raw_n} DISTINCT={distinct_n} MERGED={merged_n}")
for r in rows:
    print(f"[{r['claim']}|{r['status']}|{r['sev']}] {r['target']} (n={r['n']}) seats={r['seats']}")
