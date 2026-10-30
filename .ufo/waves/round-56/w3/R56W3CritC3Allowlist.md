# R56W3CritC3Allowlist — third-reading evidence

## Scope, axes and result

Attacked item: **C3 allowlist adjudication**, specifically false exemptions, false provenance and consistency with the hedged fills. Axes: **C3 calibration** (truthful registry back-references), **reviewability/provenance**, and **frozen-contract fidelity**. No ruling on admission or the canonical judge is made here.

Scored tree: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. All 24 exempt pairs and every outside-fence token-bearing line were opened from git objects at that revision. Full lines, including S030's ten lines and S040/S094's multiple lines, are preserved in `citing-lines.json`; table quotations are exact substrings, not paraphrases. Definitions: reliance means the entry uses the row's registered material to support its own assertion; name-only includes explicit refusal, status, correction, redirect and neighbour labels. A reader's hedge is compared by its leaning direction, not treated as certainty.

**My reading: 23 NAME-ONLY, 1 RELIANCE-leaning (S044).** S113 remains a close name-only call. This is evidence for closure, not a change to the frozen list. The counter and controls remain green under the frozen contract.

## 24-pair table

| pair (all paths repository-relative) | my reading | exact quoted substring at score revision | RevC3Contract | CritCiteDef |
|---|---|---|---|---|
| S005 / corpus/knowledge/output-colour-boundaries-r14.md | NAME-ONLY | L65: “Neither the S005 README's earlier commit nor the later S040 governance commit is substituted for this file revision.” | agree (MIS) | agree (N) |
| S007 / corpus/knowledge/input-debugging-boundaries-r15.md | NAME-ONLY | L10: “S051 supersedes queued S007's loose composite tools description and mutable” | agree (MIS) | agree (N) |
| S030 / corpus/knowledge/hyprland-config-era-r12.md | NAME-ONLY | L132: “**Every** historical S030 occurrence in this entry, including the source header,” | agree (MIS) | agree (R) |
| S040 / corpus/knowledge/output-colour-boundaries-r14.md | NAME-ONLY | L20: “do not apply S040's wayland-protocols governance as its authority.” | agree (MIS) | agree (N) |
| S043 / corpus/knowledge/input-debugging-boundaries-r15.md | NAME-ONLY | L11: “S052 adds the core input contract, distinct from S043's registry scope.” | agree (MIS) | agree (N) |
| S044 / corpus/knowledge/config-drift-r12.md | RELIANCE (leaning) | L160: “S015 stays a historical omarchy-method source; round-13 S044 cites the” | disagree (MIS) | agree (lean) (M-U) |
| S045 / corpus/knowledge/hyprland-config-era-r12.md | NAME-ONLY | L139: “by superseding registry row S045; the original S030 stays rejected.” | agree (MIS) | agree (N) |
| S056 / corpus/knowledge/xdg-terminal-selection-r47.md | NAME-ONLY | L11: “held neighbours: the documentary route in terminal-route-r17.md (rows S056-S060)” | agree (MIS) | agree (N) |
| S061 / corpus/knowledge/terminal-route-r17.md | NAME-ONLY | L152: “Source rows: `corpus/SOURCES.md` S056-S060 (mined) and S061-S062 (rejected)” | agree (MIS) | agree (M-N) |
| S062 / corpus/knowledge/terminal-route-r17.md | NAME-ONLY | L152: “Source rows: `corpus/SOURCES.md` S056-S060 (mined) and S061-S062 (rejected)” | agree (MIS) | agree (M-N) |
| S084 / corpus/knowledge/walker-route-r18.md | NAME-ONLY | L327: “S084 is now `rejected` in SOURCES.md.” | agree (MIS) | agree (N) |
| S094 / corpus/knowledge/theme-route-r18.md | NAME-ONLY | L167: “S094 is now `rejected` in SOURCES.md.” | agree (MIS) | agree (N) |
| S096 / corpus/knowledge/config-health-report-r3.md | NAME-ONLY | L1017: “S096 (host walker bytes) now exists and is not cited here.” | agree (MIS) | disagree (U) |
| S113 / corpus/knowledge/tripwire-binding-boundaries-r21.md | NAME-ONLY (borderline) | L34: “S113's quoted `os` process-management fact is retained, but its finite module list cannot support a statement about every other stdlib module” | agree (MIS) | disagree (M-U) |
| S116 / corpus/knowledge/tripwire-precision-r20.md | NAME-ONLY | L146: “Current bounded reasoning and unresolved forcing/dynamic boundaries are in `tripwire-binding-boundaries-r21.md` (S116–S120)” | agree (MIS) | agree (N) |
| S119 / corpus/knowledge/tripwire-precision-r20.md | NAME-ONLY | L146: “S119 explicitly supersedes S113's finite-module-list inference.” | agree (MIS) | agree (N) |
| S120 / corpus/knowledge/tripwire-precision-r20.md | NAME-ONLY | L146: “Current bounded reasoning and unresolved forcing/dynamic boundaries are in `tripwire-binding-boundaries-r21.md` (S116–S120)” | agree (MIS) | agree (N) |
| S132 / corpus/knowledge/terminal-trees-r23.md | NAME-ONLY | L1: “S132 stays queued and supports nothing.” | agree (MIS) | agree (N) |
| S187 / corpus/knowledge/event-delivery-limits-r26.md | NAME-ONLY | L80: “the source ids (package S187 → S189, S188 → S201, S214 → S212, by document)” | agree (MIS) | agree (N) |
| S188 / corpus/knowledge/event-delivery-limits-r26.md | NAME-ONLY | L80: “the source ids (package S187 → S189, S188 → S201, S214 → S212, by document)” | agree (MIS) | agree (N) |
| S214 / corpus/knowledge/event-delivery-limits-r26.md | NAME-ONLY | L80: “the source ids (package S187 → S189, S188 → S201, S214 → S212, by document)” | agree (MIS) | agree (N) |
| S357 / corpus/knowledge/hyprland-bind-key-match-r50.md | NAME-ONLY | L3: “S357/S358 serve that tool only.” | agree (MIS) | agree (N) |
| S358 / corpus/knowledge/hyprland-bind-key-match-r50.md | NAME-ONLY | L3: “S357/S358 serve that tool only.” | agree (MIS) | agree (N) |
| S359 / corpus/knowledge/hyprland-dispatcher-dispatch-r51.md | NAME-ONLY | L20: “S359, the wiki Binds page at the 0.56.2-era revision” | disagree (REAL) | agree (lean) (M-N) |

## Four disputed pairs

- **S044/config-drift-r12 — reliance-leaning (D1).** L160–161 completes “round-13 S044 cites the actual gate-maintenance rule.” More decisively, L156–158 says: “The governing gate rule is `gate-standing-use.md` §5 rule 4 (:222-226):” / “the response is re-verification and an appended erratum.” / “also requires re-cutting after changes outside the excised blocks.” S044 registers precisely §5 rules 2/4, :212–226 and teaches the same requirements. It is the only registry row naming gate-standing-use.md. Round-13 lesson L12 says “Append the actual gate-rule citation in `config-drift-r12.md`, record S044”; L38 records S044 with the same quote and anchor. This supports both W2 readers' reliance lean. Strongest counterargument: L160's token itself names round-13's citation, while the direct rule citation is by file path. “Record S044” may mean create the registry row, not prescribe its used-by cell. I nevertheless read the entry's explicit adoption of that governing rule as reliance, not denial of reliance.
- **S096/config-health — name-only.** L1017 explicitly says “is not cited here.” Its preceding re-read is the 1,336-B user config, digest fecf71fa (registered by S085/S091), not S096's binary/version binding. S096's binary digest prefix 25240650 has zero occurrences in this entry. CritCiteDef's U basis conflates these objects; the exemption stands.
- **S113/r21 — name-only, borderline.** L34 really does say the quoted os fact “is retained”; that is the strongest counterargument. The sentence's operative act is to delimit a superseded inference, and the entry's current table uses S117's counterexample (L18), not a fresh os.rst derivation. S119's scope expressly preserves the os quote in its own scope and already credits r21. I do not read this as a clean denial of all S113 content; the exemption needs the disclosed hedge.
- **S359/r51 — name-only.** L20 is its sole token line. The manifest L30–46 has wiki-Using-hyprctl.md and wiki-Dispatchers.md, not wiki-Binds.md; the entry's census L278 says exactly `held_rows_cited=2 (S352, S353)`. S352/S353, in the same L20 enumeration, have independent byte-identity support at L48/L52–53; S359 does not. This is a justified split within one sentence, not a reason to fill every enumeration member. Absence of a pin alone cannot prove no historical consultation; it bounds this verdict.

## Hedged-fill consistency check

The five **M-U fills** are S015/walker-route-r18 and S158/S162/S175/S177/hyprctl-verification-layer. Including S046's **BORD** gives six wave-1-hedged fills, exactly registration-v2's disclosure; the requested “five” corresponds to the M-U subset. W2 also adds a weak S091/arc-synthesis reading; it is not a wave-1 hedge.

- S015 L236: “Per the S015 protocol, these moved pins are reported with old and new values.” Reliance: it applies S015's protocol. This is the strongest comparison for S044: an entry applying a registered procedural rule can rely on it without putting its id in the source header.
- S046 L87: “The diagnostic used for S041 did bind/query some interfaces (S046 in the U4 note)”. Reliance, pointer-mediated: it asserts the diagnostic fact S046 registers.
- The L306 quartet: “`hyprctl animations -j` table from the directives (S175–S177, S158, S162)”. Thin provenance reliance is defensible: it forwards the derivation from animation-table-r26. But compare the exempted L146 r20 pointer “Current bounded reasoning and unresolved forcing/dynamic boundaries are in `tripwire-binding-boundaries-r21.md` (S116–S120)”. Both name another entry and its source rows. The positive coverage assertion at L304–308 versus L146's deferral and refusal to convert old counts into passes is a possible distinction; it is not an automatic lexical rule. I flag consistency risk, not four newly established false fills. S176 remains hidden inside the same L306 range and has no verification-layer back-reference; this is the already-declared literal-token limit, not a new frozen-predicate failure.

S057's separate W2 warning was also opened: terminal-trees L87 says the resolver honours Hidden=true (S057), whereas S057's teaches names lookup order and --dir. That demonstrates reliance intent, not source entailment. I did not reopen the upstream script, so the Hidden claim remains unverified rather than disproved.

## Findings, axes, smallest safe correction

| id | counterexample/input | severity | impacted axes | smallest safe correction |
|---|---|---|---|---|
| D1 | S044: adopted governing-rule content at config-drift L156–161, but S044.used-by lists only lesson13; exemption suppresses the live pair | **weakens the claim**, not a failure of the frozen arithmetic | C3 calibration; provenance | Closure explicitly resolve this dissent. If reliance is upheld, route a new registration to round57: drop this exemption and add the entry to S044.used-by. Do not edit v2 this round. |
| D2 | S096's U classification versus explicit “not cited here”; S359's REAL classification versus the manifest/census | **cosmetic** for current registry disposition | review provenance | Correct the interpretation in closure evidence; frozen artifacts stay untouched. |
| D3 | L306 filled attribution versus L146 exempted pointer; S113 retained-fact hedge | **weakens reviewability**; judgment boundary, not a proved counter bypass | calibration; reviewability | State the adopted reliance criterion explicitly in closure and route any broader semantic redesign to round57. Do not silently enlarge or narrow the frozen list. |

### Mechanical counterexamples (scratch copies only)

The S044 tests demonstrate dependency on the exemption, **not** proof of semantic reliance; that remains the textual judgment above.

1. Current frozen tree: `missing=0 conflict=0 stale=0 lost=0 exempt=24 TARGET_MET`, exit 0.
2. Remove only the S044 allowlist row: commit `917c676d9a849be0f470337f5dc40028ea384428`: `missing=1 conflict=0 exempt=23 TARGET_MISSED missed=missing,allow_sha,exempt`, exit 1.
3. Add only config-drift-r12.md to S044's used-by: commit `c689ca5cf1534930a928b3846e0a201db0a08362`: `missing=0 conflict=1 exempt=24 TARGET_MISSED missed=conflict`, exit 1.
4. **Noncanonical simulation only**: drop the exemption and fill the pair, passing an overridden c3 table to `check()` (exempt=23/new allowlist digest; bypasses frozen table authentication): `missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=23 TARGET_MET`, return 0. This is not a v2 pass or an admission; it only shows the paired bookkeeping correction is arithmetically coherent.

## Commands and decisive outputs

All scored reads used `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:<path>` (entry blobs, SOURCES, allowlist and reader artifacts). `extract.py` records the exact git invocations and the independent line-sha calculation; output `citing-lines.json`: **24/24 sha_ok=true**, no mismatches. This null result supports stale=0, not the semantic judgments.

Counter command (in the scratch clone, at the identical score object):

```text
python3 -I /fast/scratch/hyaku/mado-r56/R56W3CritC3Allowlist/laneclone/quality/counters/c3-r56-used-by.py --repo /fast/scratch/hyaku/mado-r56/R56W3CritC3Allowlist/laneclone --rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --work /fast/scratch/hyaku/mado-r56/R56W3CritC3Allowlist/work1
MADO_USED_BY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
exit 0
```

The same invocation with mutated revisions above and work2/work3 produced tests 2/3. Mutants were built using `hash-object -w --stdin`, recursive `ls-tree`/`mktree`, and `commit-tree -p 0f3a54361a9824484d0801679ceb1fd8ac7c32e1` in the scratch clone only, with its toplevel asserted. No branch or working copy of the lane was changed.

```text
python3 -I /fast/scratch/hyaku/mado-r56/R56W3CritC3Allowlist/laneclone/quality/check-r56-controls.py --claim c3 --repo /fast/scratch/hyaku/mado-r56/R56W3CritC3Allowlist/laneclone --rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --work /fast/scratch/hyaku/mado-r56/R56W3CritC3Allowlist/work4
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
exit 0
```

Harness also disclosed its raw missing count 24 versus counter 0 (not scored); exactly the exemptions, not a newly discovered mismatch.

Independent reader-label set derivation (csv/json labels):

```text
union-rule allowlist == frozen allowlist ? True | sizes 24 24
rule - frozen: []; frozen - rule: []
intersection-rule fill set size: 41
disagreements: S044/config-drift, S096/config-health, S113/r21, S359/r51
hedged fills: 6 = five M-U + one BORD
```

Source-header diagnostic: 0/41 filled pairs are in the first-15-line SRC set; 2/24 exempt pairs are (S030 and S132, whose source lines include the later rejection/disclaimer material). Thus header absence cannot independently justify S044's exemption. SRC inclusion here counts every token on the source line, **not just its affirmative source-id list**; S132 is omitted from that affirmative list but appears in the same line's disclaimer.

Reproducible null searches executed against score blobs: config-health binary digest prefix `25240650`: **0**; r51 `resolve_binds_by_sym`: **0**; r51 wiki-Binds pin: **0**; SOURCES rows naming gate-standing-use.md: **1 (S044)**. A compound shell search stopped after the first zero-match grep (exit 1); later manifest/context reads supplied the remaining evidence. One initial context-extraction command failed (awk/sed syntax), then successful git-object reads retrieved the same sections. One exploratory label computation and two simulation attempts failed with Python type errors and were retried successfully. No failed check is represented as a pass.

## Recommendation (closure evidence, not a ruling)

Uphold the 23 name-only readings with the S113 retention hedge explicitly disclosed, but do not describe S044 as an undisputed name-only exemption: its entry adopts the precise registered gate rule, and both W2 readers independently leaned reliance. Ask the closure to resolve that one substantive dissent against the strongest counterargument (the token itself points to the round-13 citation). Preserve the frozen v2 list and green mechanical receipts unchanged; if reliance is upheld, route the coupled S044 back-reference/exemption correction and newly registered hashes/counts to round57. Keep the L306/L146 attribution boundary visible rather than treating green token arithmetic as semantic consensus.

## Deliverables, limits and discipline

- Report: `.ufo/waves/round-56/w3/R56W3CritC3Allowlist.md`.
- Supporting files: `.ufo/waves/round-56/w3/R56W3CritC3Allowlist/table.md`, `citing-lines.json`, `extract.py` (receipt reproducer only).
- No host/compositor reads or writes; no tools installed/upgraded. No lane tracked files, fleet files, sibling lanes or frozen artifacts edited. One shared clone under the assigned scratch directory; removed before yield.
- Did not verify upstream entailment, run C1/C2, or claim non-author/independent-reviewer status. Reader judgments are third-reading evidence, not canonical admission.
- Deviation disclosed: scratch `commit-tree` probes used inherited git identity rather than the required explicit ctl identity; probes are not admissible authorship/timestamp evidence. Some exploratory Python invocations omitted `-I`; the counter and harness invocations used `python3 -I`. The noncanonical override simulation is not a frozen claim score.
