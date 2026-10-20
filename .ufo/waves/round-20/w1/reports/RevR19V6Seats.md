# RevR19V6Seats — Relative report routing is guarded; M9 cites reportless seats collectively

## Findings

### Medium — M9 relies on task results from the reportless w1 seats

The round-19 registry has 86 member keys (`.ufo/waves/round-19/w1/record.json:7-525`); comparing those keys with the w1 reports directory leaves 25 without a matching member-named report:

- Reviewers (15): `RevDraftBashCVar`, `RevDraftHelperFn`, `RevPreReg19`, `RevTwRecallPrecision`, `RevFreshPinsCounter`, `RevR18Mining`, `RevJjDisposition`, `RevQualityOverlap`, `RevSourcesContract`, `RevF1F2Repro`, `RevPipeRcTip`, `RevReceiptChecker`, `RevNavigationU`, `RevGateWalkerRow`, `RevSkillHeadGuidance`.
- Connectors (6): `ConnSiblingAnchors`, `ConnSiblingSupersede`, `ConnJjAuditsFleet`, `ConnRegistryTools`, `ConnCarriedLedger`, `ConnFrontierPlan`.
- Revengers (3): `RevengeS094Anchor`, `RevengeFrozenValidation`, `RevengeWalkerPinHistory`.
- Simplifier (1): `SimplifyTripwireTip`.

`corpus/lessons/round-19.md:147-150` explicitly labels the M9 support as evidence from “each dead w1 seat's task result” and says the supporting material is in L1 session task results, while the lane holds only registry membership. Thus the reportless group is credited collectively for the 429 claim; the lesson does not name those seats individually or point to per-seat result records. The M9 table row itself says `captured-by: none` at line 24, so distinguish this generic task-result evidence from a named captured-by attribution. Exact-name search for the 25 missing keys in the lesson returned no matches.

Evidence: record SHA-256 `f64c997e6f29d9bf4a1573fd03a6d8b6a02defbd5762edc38f33006a9309cc58`; lesson SHA-256 `da9d8a87a2fe79bc9bf3614e3d29412b39abb4a5affa33a89a77dd6a7afbcdf6`. The report-directory listing also contains `TwMerge.md`, but `record.json` has no `members.TwMerge` entry; it is not counted as a member report.

### Low — Relative report destinations can resolve to the fleet root if the root rule is ignored

The received `Report:` trailer names `.ufo/waves/round-20/w1/reports/RevR19V6Seats.md` relatively, and the persisted wave spec also gives a relative `reportDir` (`.ufo/waves/round-20/w1/spec.json:4`). Since tools start in `/home/vgpnk/Projects/shokunin`, resolving either path against the current directory literally would write under the fleet root rather than `/home/vgpnk/Projects/shokunin/mado-shokunin`. The shared context at `spec.json:3` explicitly resolves report trailers against the lane root and requires absolute paths for reads, commands, and writes, so this is a guarded hazard, not an observed misroot in this audit. The same failure mode was recorded for `QualityDraft` in `corpus/lessons/round-19.md:23`. This report was written to its absolute lane path. In the stored item prompts, the output destinations returned by the path/write scan were absolute; no additional relative write target was identified.

Evidence: spec SHA-256 `a70afe1fdd3b10266e0e8ea41df1edf35f068b5b8814a6afb22f1834c78cdfef`.

## Limits

- I checked the round-20 shared context, stored item prompts for write/path destinations, round-19 w1 registry, its reports directory, and `corpus/lessons/round-19.md`; I did not inspect L1 session task-result transcripts to independently validate the 429 outputs or enumerate which task result belongs to each reportless member.
- I did not test how the wave orchestrator resolves the relative `reportDir` metadata; the context's absolute-path rule was followed.

## Installs

none
