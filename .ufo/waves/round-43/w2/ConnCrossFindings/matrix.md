# ConnCrossFindings — w1 finding status matrix at the data commit 1959770657f1f8665097c1aed4be6c1cbb07139f

Status keys: **FIXED** = the defect is gone in the landed tree, with the pointer where; **DECLARED** = named as a
residual in registration.md / registration-v2.md / corpus/lessons/round-43.md (pointer given); **OPEN** = still
present at 1959770 and not declared; **SUPPORT** = finding supports the claim/landing (no defect); **INFO** = no
action (observation). Verdict anchors: `tools/mado-geometry.py` at 1959770 = sha256
`e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` (byte-identical to the round-42 reference and to
the artifact SentReDoS/RevRefTool/MutRefSelftest/ExecC1ExtraMutants reviewed); C1 counter at 1959770 = `ed78d693…`
(freeze bytes, unchanged); C2-v2 counter at 1959770 = freeze blob `9a834070…` (unchanged since 496340d).

## C1 side (operability)

| finding | seat | severity | status | pointer |
|---|---|---|---|---|
| SR-1 ReDoS `(a+)+$` etc. contract-admissible; 31-byte class ≈ 35.7 s; 1 MiB never returns | SentReDoS | High | OPEN | SR-1 in `w1/SentReDoS/findings.md:23-78`; tool byte-identical at data (`sha256sum tools/mado-geometry.py` = e3c2e471); no `regex_ok`/matcher change in landed tool |
| SR-2 unbounded clients×rules×length product; 99.3 s at 12000 rules | SentReDoS | High | OPEN | `w1/SentReDoS/findings.md:82-115`; no budget in landed tool |
| SR-3 deep JSON `RecursionError` → rc 1, empty stdout, traceback (violates bad_json/exit 2/stderr-empty) | SentReDoS | High | OPEN | `w1/SentReDoS/findings.md:119-151`; `parse_clients` unchanged in landed tool |
| SR-4 early-closing consumer → `BrokenPipeError` traceback / silent truncation, exit 1 | SentReDoS | Medium | OPEN | `w1/SentReDoS/findings.md:155-175`; no handler in landed tool |
| SR-5 field-level forgery inside `MADO_GEOM_CLIENT` (`class="x\" verdict=DIFFER …`) | SentReDoS | Low | OPEN | `w1/SentReDoS/findings.md:179-211`; line layout unchanged |
| SR-6 `S_ISREG` type-only check accepts `/proc`, `/sys`, symlinks | SentReDoS | Low | OPEN | `w1/SentReDoS/findings.md:215-236`; `read_regular` unchanged; clause-g block on `/proc` literal also unchanged |
| SR-7 4300-digit sizes accepted/echoed | SentReDoS | Low | OPEN | `w1/SentReDoS/findings.md:240-253` |
| V1 ReDoS hang through SAFE gate | RevRefTool | High | OPEN | `w1/RevRefTool/findings.md:31-51`; same artifact; same root as SR-1 |
| V2 legal-input scan blowup (24000 rules × 5000 clients) | RevRefTool | Medium | OPEN | `w1/RevRefTool/findings.md:53-68`; same root as SR-2 |
| V3 deep-nested JSON crash instead of SETUP | RevRefTool | Medium | OPEN | `w1/RevRefTool/findings.md:70-86`; same root as SR-3 |
| V4 broken pipe: silent truncation w/ exit 0 on this host (EPIPE traceback on mainline) | RevRefTool | Medium | OPEN | `w1/RevRefTool/findings.md:88-118`; same root as SR-4 |
| V5 stdin closed `0<&-` → AttributeError, exit 1, no SETUP | RevRefTool | Low-Med | OPEN | `w1/RevRefTool/findings.md:120-128` |
| V6 stdout closed normal path → AttributeError | RevRefTool | Low | OPEN | `w1/RevRefTool/findings.md:130-135` |
| V7 stdout closed SETUP path → exit 2 with no SETUP line | RevRefTool | Low | OPEN | `w1/RevRefTool/findings.md:137-142` |
| V8 5000-digit int size rejected as bad_json (int limit) | RevRefTool | Low | OPEN | `w1/RevRefTool/findings.md:144-153` |
| U4 non-UTF-8 rules decode (`errors="ignore"`) unexercised; mutant survives | MutRefSelftest | — | OPEN | `w1/MutRefSelftest.md:30-32`; fixture population unchanged |
| N1 deep-nesting crash: pristine reference fails its own contract (RecursionError) | MutRefSelftest | — | OPEN | `w1/MutRefSelftest.md:34-36`; same root as SR-3/V3 |
| R5 `os.close` fd leak indistinguishable at host ulimit | MutRefSelftest | — | OPEN | `w1/MutRefSelftest.md:39-40`; latent |
| N48 rules-file UTF-8 error-handler mutation survives all 37 fixtures | ExecC1ExtraMutants | — | OPEN | `w1/ExecC1ExtraMutants.md:95-106`; no fixture change |
| N51 descriptor-leak mutation survives (no RLIMIT_NOFILE fixture) | ExecC1ExtraMutants | — | OPEN | `w1/ExecC1ExtraMutants.md:107-116` |
| F1 contract grammar requires effect-first + exactly two fields; legacy parser is order-free/any-arity (`handleWindowrule`, ConfigManager.cpp:2016-2050); false AGREE mis | CritContract | High | OPEN | `w1/CritContract/findings.md:31-62`; the C1 contract is frozen and unamended (no C1 v2); the landed tool still implements the narrowing grammar |
| F2 "a tiled window never reads it" false (applicator stores static size for every matching window; first-map floating branch is the only consumer) | CritContract | High | OPEN (C1 contract) / honored in entry | `w1/CritContract/findings.md:64-85`; reference docstring sentence unchanged; the landed C2 entry states the corrected form ("A tiled window never takes this branch… only acts through the floating algorithm", `corpus/knowledge/hyprland-gkeep-geometry-r43.md:48`) |
| F3 "rules apply in file order" ambiguous; compositor registers named blocks first | CritContract | Medium | OPEN | `w1/CritContract/findings.md:87-112` |
| F4 class guard (<U+0020) diverges from RE2 `.` semantics; `ctlclass0` locks it in | CritContract | Medium | OPEN | `w1/CritContract/findings.md:114-132` |
| F5 whitespace model: tab-runs accepted by tool, rejected by Hyprland; double-space swallowed (false AGREE) | CritContract | Medium | OPEN | `w1/CritContract/findings.md:134-157` |
| F6 no inline `#` comment handling (hyprlang truncates) | CritContract | Low/Med | OPEN | `w1/CritContract/findings.md:159-175` |
| F7 `unsupported` conflates malformed lines with well-formed non-class-joinable size rules (host: tag/title rules) | CritContract | Low | OPEN | `w1/CritContract/findings.md:177-194`; same ground as ExecLiveHost F5/ScoutSizeGrammar |
| F8 two boundary sentences (stdin 1048577; repeated `--rules`) with no deciding fixture | CritContract | Low | OPEN | `w1/CritContract/findings.md:196-208` |
| F9 editorial duplicated `first` | CritContract | Editorial | OPEN | `w1/CritContract/findings.md:210-214` (harmless) |
| F1 docstring "not UTF-8 JSON → bad_json" vs `json.loads` NaN/Infinity leniency; `nan0` pins lenient reading | RevC1Counter | Medium | OPEN | `w1/RevC1Counter/findings.md:12-17`; counter unchanged (`ed78d693…` at 1959770) |
| F2 global 3-timeout breaker is order/load-sensitive; slow-but-correct tool scores 0/37 | RevC1Counter | Medium | OPEN | `w1/RevC1Counter/findings.md:19-25` |
| F2b clause b2 nonce coin-flip at boundary (P(pass)=0.47-0.87 in 26-30-kill band) | RevC1Counter | Med-Low | OPEN | `w1/RevC1Counter/findings.md:27-31` |
| F3 BOM/ast-parse crash → traceback, no final P line | RevC1Counter | Medium | OPEN | `w1/RevC1Counter/findings.md:33-37` |
| F4 fixture vacuity: no fixture passes ≥4 `--rules`; 3-file truncating tool scores 37/37 | RevC1Counter | Low-Med | OPEN | `w1/RevC1Counter/findings.md:39-44` |
| F5 unpinned orderings/domains (bad_json×unreadable, usage×unreadable, stdin >1048577) | RevC1Counter | Low | OPEN | `w1/RevC1Counter/findings.md:46-50` |
| F6 clause g code ≠ docstring in both directions (strict: names/zero-import; loose: `sys.argv[:1][0]`) | RevC1Counter | Low | DECLARED | `w1/RevC1Counter/findings.md:52-57`; residual "clause g is a heuristic over names" (`registration.md:68`) |
| F7 dead guard `STDLIB_DENY` ∩ `ALLOW` empty | RevC1Counter | Low | INFO | `w1/RevC1Counter/findings.md:59-61` |
| F8 `many0` seed ignores REV (docstring formula mismatch) | RevC1Counter | Low | INFO | `w1/RevC1Counter/findings.md:63-65` |
| F9 selftest phase runs without RLIMIT_NPROC; clause g does not ban `os.fork` | RevC1Counter | Low | INFO | `w1/RevC1Counter/findings.md:67-69` |
| F10 stale comment about nonexistent stub; file-mode stdin blocks to timeout | RevC1Counter | Low | INFO | `w1/RevC1Counter/findings.md:71-73` |
| F11 alphabet admits catastrophic regexes the counter can never score (would hang on its own model) | RevC1Counter | INFO | OPEN | `w1/RevC1Counter/findings.md:75-77`; sharpens the declared re≠RE2 residual but the liveness dimension is not declared |
| F12 gate integrity + model≡reference (392 fresh cases) | RevC1Counter | — | SUPPORT | `w1/RevC1Counter/findings.md:79-84` |
| GATE-BROKEN mutants (call-exec/name-getattr/total-ge/allow-open/verdict-string) show gates can fail | MutC1CounterGates | — | OPEN | `w1/MutC1CounterGates.md:28-36`; counter unchanged; verdict-string variant is caught by the runner |
| SPLIT `exit-always-0`: runner ignores counter exit code | MutC1CounterGates | — | OPEN | `w1/MutC1CounterGates.md:37-39`; runner-side coverage gap, not addressed |
| 65 survivor mutants with no isolating control (deny-list entries, os.*, teeth counts, sandbox flags, timeout breaker) | MutC1CounterGates | — | OPEN | `w1/MutC1CounterGates.md:48-55`; coverage findings |
| cheat 4 source-integrity pin selftest reaches MET (b/b2/b3/g all 1) | CritC1Cheat | High | DECLARED | `w1/CritC1Cheat.md:24,85-135`; named an open defect of PRED-C1-r42 in `registration-v2.md:39-45`; not fixed (tool unchanged) |
| cheat 6 sandbox-detection tool reaches MET but is useless on host | CritC1Cheat | High | DECLARED | `w1/CritC1Cheat.md:27,149-165`; named in `registration-v2.md:39-45` and residual "the sandbox is detectable" (`registration.md:68`) |
| cheat 1 rename-only model reaches MET | CritC1Cheat | — | DECLARED | `w1/CritC1Cheat.md:21,33-52`; residual "a tool that contains a model of the contract is an implementation" (`registration.md:67`) |
| F3 b2 site inventory name-derived (`NOT_SITES`); KILL_NEED=4/6 met by cheat-1 | CritC1Cheat | — | OPEN | `w1/CritC1Cheat.md:45-52,188` |
| F4 byte-table passes 26/27 nonce-free fixed fixtures; gen lattice is the only defense | CritC1Cheat | — | SUPPORT (defense) | `w1/CritC1Cheat.md:54-73`; no change needed; lattice intact |
| cheat 3 mirror-selftest caught by b2; cheat 5 cross-run cache structurally impossible | CritC1Cheat | — | SUPPORT | `w1/CritC1Cheat.md:75-83,136-147` |
| D1 control-char guard divergence (tool declines rules RE2 applies; 767/466189 pairs) | LabRe2Fuzz | — | DECLARED | `w1/LabRe2Fuzz.md:71-87`; documented in contract `c1-r42-geometry.py:39`; falls under the re≠RE2 residual |
| D2 Python `re` exponential where RE2 linear (`(a*)*`, `(a+)+`, `(a|aa)*`) — liveness not covered by alphabet restriction | LabRe2Fuzz | High | OPEN | `w1/LabRe2Fuzz.md:89-163`; 49 organic slow pairs at 0.05 s budget; same root as SR-1/V1 |
| H not falsified: 466,189 value pairs 0 divergences; all 77,690 gated patterns compile under RE2 | LabRe2Fuzz | — | SUPPORT | `w1/LabRe2Fuzz.md:18-27` |
| DEL-1..6 deletable contract dead weight (1-200 chars, 1048577 cap, verdict order, floats, two sentences, duplicate `first`) | SimpContract | Low | OPEN | `w1/SimpContract.md:24-42`; no C1 v2; contract text unchanged |
| 9 live-but-unexercised free passes (flag order, non-UTF-8 rules, setup-order links, dup address, permission-denied, `unreadable≺too_large`, `too_large≺bad_json`, zero-arg size) | SimpContract | — | OPEN | `w1/SimpContract.md:44-47`; counter gaps; same family as RevC1Counter F5/ExecIndepC holes |
| F1 float field-0 grammar "exactly one token" vs one *argument* token (literal reading wrong) | ExecIndepA | — | OPEN | `w1/ExecIndepA.md:78-88` |
| F2 TILED decided by client JSON `floating`, not by a matched float rule; never stated in one sentence | ExecIndepA | — | OPEN | `w1/ExecIndepA.md:90-96` |
| F3 regex bound "1-200 characters" ≈ 200 grammar items, not source chars | ExecIndepA | — | OPEN | `w1/ExecIndepA.md:98-106`; same root as ExecIndepC 5.1/SimpContract DEL-1 |
| 5.1 chars-vs-tokens under-determined (both readings score 37/37) | ExecIndepC | — | OPEN | `w1/ExecIndepC.md:91-104` |
| 5.2 clients bad_json vs rules readability order under-determined | ExecIndepC | — | OPEN | `w1/ExecIndepC.md:105-116` |
| 5.3 per-file vs per-reason rules check order under-determined | ExecIndepC | — | OPEN | `w1/ExecIndepC.md:117-127` |
| 5.4 non-UTF-8 rules decode under-determined (no fixture writes invalid bytes into rules) | ExecIndepC | — | OPEN | `w1/ExecIndepC.md:128-138`; same root as MutRefSelftest U4/N48 |
| 5.5-5.10 readings decided by fixtures (NO_SIZE_RULES order, BADSIZE≻TILED, other-vs-unsupported, rules= size-only, stdin boundary, CRLF) | ExecIndepC | — | SUPPORT | `w1/ExecIndepC.md:140-219` |
| Host has 7 size lines; the tool supports 3, refuses 4 (match:tag ×2, class+title ×2), mislabels 1 reversed-order rule; block-form `windowrule {}` invisible | ScoutSizeGrammar | — | OPEN | `w1/ScoutSizeGrammar.md:6`; same root as CritContract F1/F7; E1/E2 proposals deferred to round 44 |
| F4/F5 host census: 4 tiled clients, no gkeep; 77/77 rule lines classified, 3/7 size rules usable | ExecLiveHost | — | SUPPORT | `w1/ExecLiveHost.md:50-89` |
| F8 blind spots: tag/title rule joins read as NO_MATCHING_CLIENT (fx-tag-btop, fx-steam) | ExecLiveHost | — | OPEN/by-scope | `w1/ExecLiveHost.md:103-109`; inherent to the claim's `match:class` scope; not declared in v2/lesson |
| F9 landing bytes = reference bytes (E3c2e471) | ExecLiveHost | — | SUPPORT | `w1/ExecLiveHost.md:111-114`; feeds CritClaimSizing C1 F1 (declared) |
| Oracle observation: nested 0.56.2 gives gkeep `size=[420,500] floating=true`; controls track rule text; rule, not client, is origin | ExecOracleGkeep | — | SUPPORT | `w1/ExecOracleGkeep.md:8-46`; reported-not-scored per residual; cited in entry §4 (`hyprland-gkeep-geometry-r43.md:62`) |
| Goal-vs-current: `clients -j` size = GEOMETRIC_GOAL; no read verb exposes CURRENT; premature-AGREE blind spot | ExecGoalVsValue | — | SUPPORT | `w1/ExecGoalVsValue.md:11-44`; absorbed in entry §3 INF and SKILL.md subsection |
| Chain facts S290-S296 (65 quotes verified) | ExecSrcChain | — | SUPPORT | `w1/ExecSrcChain.md:18-46`; used by the entry |
| No sibling-lane overlap; gkeep bounds; separability holds | ConnCrossClaim / ConnSiblingOverlap | — | SUPPORT | `w1/ConnCrossClaim.md:9-11`, `w1/ConnSiblingOverlap.md:7-25` |
| No harm at base; all gates identical to round-41 tip; round-41 receipt capture defects (WARN pair, 2-line census, bare check-index-rows) | ExecHarmBase | — | SUPPORT | `w1/ExecHarmBase.md:50-81`; historical receipt defects remain in round-41 files (not round-43 data) |

## C2 side (coverage)

| finding | seat | severity | status | pointer |
|---|---|---|---|---|
| F1 held-id receipt entirely unpinned (S050 fabricated receipt admits) | RevC2Counter | Medium | DECLARED | `w1/RevC2Counter/findings.md:13-29`; residual named in `registration-v2.md:31-34`; the landing avoids it (held S155/S158 gate receipts are the pinned bytes, `corpus/lessons/round-43.md:61-65`) |
| F2 bypass 1: byte-identical GATE line outside `## Gate` invisible (set-membership) | RevC2Counter / ExecC2ExtraMutants | Medium/Low | DECLARED | `w1/RevC2Counter/findings.md:31-39`, `w1/ExecC2ExtraMutants.md:116-136`; declared in `registration-v2.md:31-34` |
| F2 bypass 2: fenced decoy GATE line invisible to every check | RevC2Counter | Medium | OPEN | `w1/RevC2Counter/findings.md:40-49`; probe at 1959770: appended fenced decoy GATE → still `admitted=1/1` (`probes-c2-leftovers.txt`) |
| F3 locator `file:42x` (garbage after line number) passes | RevC2Counter | Low-Med | OPEN | `w1/RevC2Counter/findings.md:51-62`; probe at 1959770: `(:10x)` locator → `admitted=1/1` |
| F4 junction-space quote line-mapping off-by-one | RevC2Counter | Low-Med | OPEN | `w1/RevC2Counter/findings.md:64-77`; `collapse_with_lines` unchanged; unit probe: `quote_at` returns 3 for words on line 4 (`probes-c2-leftovers.txt`) |
| F5 `recheck:` prefix-match admits trailing junk (entry + registry cells) | RevC2Counter | Low | OPEN | `w1/RevC2Counter/findings.md:79-88`; probe: entry `recheck: 90d whatever junk` → `admitted=1/1`; `recheck_ok("90d and-never-recheck")=True` |
| F6 entry claim line may carry the Gate quote mid-word (substring check) | RevC2Counter | Low | OPEN | `w1/RevC2Counter/findings.md:90-99`; probe: S292 quote embedded mid-word → `admitted=1/1` |
| F7 locator inside a longer path admits | RevC2Counter | Low | OPEN | `w1/RevC2Counter/findings.md:101-109`; probe: `archive/deep/Hyprland-Target.cpp:10` → `admitted=1/1` |
| F8 own-work row location can point elsewhere (`host-gkeep.conf.bak`) | RevC2Counter | Low | OPEN | `w1/RevC2Counter/findings.md:110-121`; probe: S295 row location → `elsewhere/host-gkeep.conf.bak` → `admitted=1/1` |
| Verified negatives (dup recheck, pinned-receipt edit, `..` traversal, on-2027, census trivial-total, rxc≡RE2) | RevC2Counter | — | SUPPORT | `w1/RevC2Counter/findings.md:123-137` |
| F1 GATE-outside-section hole (low) | ExecC2ExtraMutants | Low | DECLARED | `w1/ExecC2ExtraMutants.md:98,116-136`; declared in `registration-v2.md:31-34` |
| F2 ADMIT/REFUSE staged basename from any directory accepted | ExecC2ExtraMutants | Low | FIXED | `w1/ExecC2ExtraMutants.md:99-100,137-156`; v2 i+ requires exact `merge/mado/knowledge/corpus/knowledge/<basename>` (`c2-r43-gkeep-entry-v2.py:16-18`); lesson's ADMIT/REFUSE lines use exact staged paths |
| F3 ids with fewer than three digits escape every clause (S99 silent) | ExecC2ExtraMutants | Low | DECLARED | `w1/ExecC2ExtraMutants.md:101,158-176`; declared in `registration-v2.md:31-34` |
| F4 declared residual confirmed: real quote + unsupported claim at true locator (R01/R05/R06) | ExecC2ExtraMutants | — | DECLARED | `w1/ExecC2ExtraMutants.md:103-105,178-188`; claim-to-quote binding residual (`registration-v2.md:31`) |
| F5 declared residual confirmed: held id's receipt not pinned (R08) | ExecC2ExtraMutants | — | DECLARED | `w1/ExecC2ExtraMutants.md:106,190-194` |
| F6 legitimate admission (`m_box = box` ending before `;`) | ExecC2ExtraMutants | — | SUPPORT | `w1/ExecC2ExtraMutants.md:196-203` |
| O1 registered `patched` scorer does not override frozen pins (frozen value wins) | ExecC2ExtraMutants | — | INFO | `w1/ExecC2ExtraMutants.md:205-229`; control-harness note, not a predicate defect |
| H1 wallpaper entry (control P itself makes no chain claim); A2 census contradiction ignored; D1/E2 claim-binding survivors | CritC2Cheat | — | DECLARED | `w1/CritC2Cheat.md:24-33,55-79`; claim-to-quote binding + census-contradiction residual (`registration-v2.md:31-34`) |
| X3 no Hyprland receipt cited admits under v1 | CritC2Cheat | — | FIXED | `w1/CritC2Cheat.md:48-50`; v2 i+ requires all ten PINS cited; negative probe at 1959770: own-work-only entry → `admitted=0/1` (`probes-c2-leftovers.txt`) |
| X1 index-row lie | CritC2Cheat | — | DECLARED | `w1/CritC2Cheat.md:55-57`; included in the named residual set (`registration-v2.md:31`) |
| B1 occurrence ambiguity; C1/C2 comment cited as code; E1 id contradicted on another line; F1 basename-only; F2 REFUSE words; X2 BAD_LOC in entry | CritC2Cheat | — | FIXED | `w1/CritC2Cheat.md:34-47,70-79`; v2 d+ (exactly-once, word-bounded, outside comments), g+ (every naming line bound), i+ (exact path, flip word, BAD_LOC) |
| G1/G2 location cell carries example.org URLs in control P (tradeoff) | CritC2Cheat | — | FIXED | `w1/CritC2Cheat.md:51-54`; v2 e+ requires true raw URL prefix; controls re-run under v2 74/74 (`receipts/ctl-c2-v2.txt`) |
| C1 F1: C1 target met by `cp` of frozen reference (provenance fact) | CritClaimSizing | High | DECLARED | `w1/CritClaimSizing/findings.md:34-73`; declared in `registration-v2.md:38-45`; landing is byte-identical to the reference (e3c2e471) |
| C2 F2: v1 target met by 17-line entry citing no compositor source | CritClaimSizing | High | FIXED | `w1/CritClaimSizing/findings.md:75-112`; v2 requires all ten PINS cited (i+), frozen at 496340d |
| F3 "end to end" universal clause not enumerated | CritClaimSizing | Medium | FIXED | `w1/CritClaimSizing/findings.md:114-128`; enumerated by i+ (PINS ⊆ cited) |
| F4 lowest-axis sentence not enumerated (coverage absent from axis-base.txt) | CritClaimSizing | Low | OPEN | `w1/CritClaimSizing/findings.md:130-147`; registration/lesson repeat the sentence without SCORECARD rubric V/U-route citations |
| F5 separability universal negative without named command (holds) | CritClaimSizing | Low | OPEN | `w1/CritClaimSizing/findings.md:149-157`; true but unnamed in registration |
| F6 frozen seat count 37 vs spec 38 | CritClaimSizing | Low | FIXED | `w1/CritClaimSizing/findings.md:159-169`; lesson records 38 seats and the LOG.md correction (`corpus/lessons/round-43.md:20-22`) |
| M43-1 wrong prose locators (`LOG.md:2483`, round-42 `registration.md:61`) | ExecLocatorGate/ScrLessonSkeleton/ScrQualityCriteria | High | FIXED | lesson `corpus/lessons/round-43.md:113-125`; checker `quality/check-locators.py` landed (sha256 `c1ea52ad…` = ExecLocatorGate deliverable), shown able to fail; entry locators computed |
| M43-2 C1 tally stated three ways | ScrQualityCriteria/ScrLessonSkeleton | — | FIXED | lesson `corpus/lessons/round-43.md:127-133`; definition single-sourced at `registration.md:59`; criterion 78 landed |
| M43-3 SHONEN box pointed at un-written LOG line | ScrLessonSkeleton/ScrQualityCriteria | — | FIXED | `receipts/live-geometry-host.txt` committed in the data commit (`corpus/lessons/round-43.md:135-143`); criterion 79 landed |
| M43-4 no round-42 lesson | ScrLessonSkeleton | — | FIXED | lesson round-43 landed (`corpus/lessons/round-43.md:145-150`) |
| M43-5 excerpt header 446-495 of 488-line file + extra blank | ScrLessonSkeleton/ScrQualityCriteria/ScrRowsDraft | — | FIXED | round-43 excerpt regenerated (`fetch/gkeep-ui-excerpt.py` sha `3695b788…`); criterion 80 landed; S297 row anchor corrected to 5 lines |
| M43-6 driver `complete` misread as round success | ScrConsiderthese/ScrLessonSkeleton | — | FIXED (as mistake) | lesson `corpus/lessons/round-43.md:161-171`; criterion 81 landed; driver-side routing remains operator-owned |
| M43-7 this round's own first entry locators missed 2-line spans | ExecLocatorGate | — | FIXED | lesson `corpus/lessons/round-43.md:173-180`; entry locators are ranges (`:70-71`, `:428-429`, `:33-34`, `:50-51`); `CHECK_LOCATORS: locators=10 miss=0` |
| M43-8 v1 counted citations, not the chain | ScrLessonSkeleton | — | FIXED | lesson `corpus/lessons/round-43.md:182-188`; v2 freeze 496340d, all pins cited |
| F1 clause-e collision S291/S296 vs held S155/S158 | ScrLessonSkeleton/ScrRowsDraft/ScrEntryA/ScrEntryB | — | FIXED | held-row resolution landed: entry cites S155/S158; new rows are S290-S297 (`corpus/lessons/round-43.md:61-68`; `corpus/SOURCES.md:167,170` used-by appended) |
| F2 37-vs-38 seats | ScrLessonSkeleton | — | FIXED | `corpus/lessons/round-43.md:20-22` |
| F3 round-42 report commit unresolvable in this repo | ScrLessonSkeleton | — | HANDLED | lesson M43-1 records the unresolved report commit (`corpus/lessons/round-43.md:118-120`) |
| F5 live-geometry-host.txt is wave-time, not freeze | ScrLessonSkeleton | — | FIXED | receipt committed at 1959770 (M43-3) |
| Staged-id collisions (S284-S287, S203-S349) and reserved-band hazard | ExecAssimIdGuard/ConnStagedVsRegistry/ScoutStagedGkeep | — | FIXED | rows S290-S297 minted, held rows cited; lesson ledger records no staged row carried over (`corpus/lessons/round-43.md:83`) |
| Quarantine contact S199/S216 unverifiable; three stale inline staged ids | ExecQuarantineSlice | — | HANDLED | verdicts published in `assimilation/quarantine-verdicts.md`; lesson ledger refuses/not-adopts the affected staged files |
| README row Sources cell depends on registry append; `warns=0` condition | ScrSkillProvince/ScrEntryA | — | FIXED | README row at `corpus/README.md:71` lists S290-S297 + held; index gate passes at data (clause f 1 row) |
| "no gkeep window observed" honest limit | all entry seats | — | SUPPORT | entry §5 UNK (`hyprland-gkeep-geometry-r43.md:68`); census lines match clause h (`receipts/c2-after-data.txt`) |

## Cross-cutting

- C1 L1 receipt at 1959770: `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0, clauses a/b/b2/b3/g = 1
  (`receipts/c1-after-data.txt`). C2-v2 L1 receipt: `admitted=1/1 verdict=TARGET_MET`, exit 0
  (`receipts/c2-after-data.txt`). Both consistent with the declared/declared+open matrix above.
- No w1 finding was found to be falsified by the landed data; every C1-tool/counter finding still holds at 1959770
  because the tool is byte-identical to the reviewed artifact and the counter bytes are unchanged.
