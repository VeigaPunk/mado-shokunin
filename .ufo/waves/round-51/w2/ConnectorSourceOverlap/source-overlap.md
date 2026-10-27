# Source overlap scan — dispatcher-dispatch entry (mado round 51 w2)

## Scope and axes
Axes: **coverage** (C2) and **operability** (C1). This is source overlap / adjacency advice, not a verdict on either claim. Frozen predicates are unchanged. Scan was read-only; no lane files or sibling lanes were edited.

## Evidence and commands
- Frozen boundary: `.ufo/waves/round-51/claims.md:39-69` defines C2's dispatcher-dispatch subject, overlap baseline, held citations and controls. C1's tool-ledger subject is at `:12-37`; it is distinct in purpose from this knowledge entry.
- Committed entry: `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:3-8` explicitly says it picks up after key matching and follows dispatcher + argument + submap + socket path. Lines 20-24 identify held S352-S353 and explicitly ground the extension in `hyprland-bind-key-match-r50.md:57-124`, not as replacement. Lines 88-243 deliver the new dispatch chain; lines 282-300 enumerate limits.
- Adjacent local entries exist by inventory: `corpus/knowledge/hyprland-bind-key-match-r50.md`, `dispatcher-semantics-r25.md`, `dispatcher-surface-and-request-grammar-r26.md`, `bind-table-r25.md`, and `keybind-rule-semantics.md`. The C2 entry cites these as held ground at lines 62-68 and states the division of subject at lines 3-12, 57-68. Thus there is deliberate conceptual adjacency and some shared vocabulary, not evidence of duplicating the entire old entry. Frozen C2 uses word-8-gram threshold ≤30% per file, not a semantic identity test.
- Prior evidence: `.ufo/waves/round-51/w1/CritC2Stub/stub-c2.md:44-45` records that low lexical overlap does not establish subject coverage; `.ufo/waves/round-51/w1/CritEntryTruth/truth-audit.md:37-39` says the round-50 entry does not cover the specific execution mechanisms. `.ufo/waves/round-51/registration.md:17-19` retains these as residual limits, not predicate amendments.
- Commands used: `read` on the frozen claims and registration, entry and W1 evidence; `glob` on `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge`, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/w2`, and `/home/vgpnk/Projects/shokunin/merge`. The first two inventories confirmed the listed local files. The merge path did not exist (`Skipped missing paths: /home/vgpnk/Projects/shokunin/merge`), so no staged `merge/mado` material was available to compare. A broad fleet-root glob timed out; it is not evidence of absence. `/home/vgpnk/Projects/shokunin/MANIFEST.json` provides sibling repo names/domains but does not identify a sibling dispatcher province. No sibling-lane source corpus was consequently inspected, so sibling non-overlap cannot be asserted.

## Assessment
**Cross-claim:** no observed subject collision. C1 is a tracked-instrument ledger/capability; C2 is Hyprland dispatcher knowledge. C2 may improve coverage; no C1 operability harm is evidenced by this material. This is a bounded subject comparison, not proof that C1 has no indirect dependencies.

**Cross-entry:** recommend **adjacent**, rather than refuse or accept as wholly disjoint. The new entry directly builds on the key-match entry and reuses held knowledge (including bind-table/parser and prior dispatcher semantics), while its declared subject and new sourced sections cover the press-time lookup/call, translator, submap, dispatcher-specific argument handling, and socket request route. A strict “no overlap” standard would contradict its explicit continuation/held-ground design. Conversely, C2's lexical ceiling alone is not a semantic novelty or coverage guarantee, as W1 explicitly demonstrated.

**Sibling / staged merge:** undecidable from repository evidence available to this scan. The expected `merge/mado` directory was absent and no sibling corpus paths were returned by inventory. Do not infer non-overlap or a conflict. If integration presents staged material later, compare its actual scope and cited pins against entry sections 1–9 before making an accept/refuse call; this is a future comparison, not a predicate amendment.

## Recommendation
**Adjacent.** Keep the entry's explicit boundary and held-ground links; do not treat shared Hyprland/keybind terminology as duplication. No concrete current conflict is evidenced. The unavailable merge/sibling material is a material limitation on any stronger accept/refuse recommendation. Any taxonomy or semantic-novelty strengthening belongs in a future amendment, not this frozen round.

## Risks and verification
- Risk: lexical overlap can miss semantic redundancy or admit a generic low-overlap stub; covered by W1 evidence above. Keep semantic review distinct from frozen PASS/MISS.
- Risk: staged merge or sibling material may later reveal a concrete same-surface duplicate; current scan cannot resolve that possibility.
- Verification pointers: re-read `claims.md:39-69`, entry `:3-24`, `:88-243`, and W1 evidence cited above. No executable check was run or claimed; no frozen-predicate or lane-artifact mutation was performed.

## Deliverables
- `.ufo/waves/round-51/w2/ConnectorSourceOverlap/source-overlap.md`

Report: .ufo/waves/round-51/w2/ConnectorSourceOverlap/source-overlap.md
