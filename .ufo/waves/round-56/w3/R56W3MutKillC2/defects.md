# R56W3MutKillC2 — fixture findings

Severity uses the requested scale; findings concern proposed fixtures, not a falsification of the frozen predicate.

- **Weakens the claim / proposal readiness:** A's K55 and K57 print absolute stage paths in their pristine outputs. Two staging locations produced different bytes. Repaired here using symlinked display roots whose realpaths cover every pristine printed path. Both repaired fixtures pass the honest tool and kill their intended mutants. See fixtures/a-k55 and fixtures/a-k57.
- **Weakens proposal reproducibility:** the filesystem-delivered B m08/K03 tree currently contains only U+0100.conf, not the raw-byte 0x80.conf named in cands.py. On that delivered tree both the old and tip tools produce paths=2 while its expected.out says paths=3. Cause/time of disappearance is unknown; no claim about the earlier author's verification follows. Rebuilt b-k03 contains both names. Its expectation uses the tip's escaped `\x80` output, not the old raw-byte output.
- **Weakens staged coverage:** Bm75/Bm76 need root-level paths and cannot be represented by the frozen staging layout. Both die in a separate tmpfs-root bwrap probe. That probe is not a frozen-contract fixture; no contract change was made.

Correction: K100 WAS present in A's extra.py (lines 8–11), with historical kill receipts. Earlier local drafts wrongly called it absent/unverified after inspecting only kill2.py. That allegation is withdrawn. The delivered a-k100 simplifies its dump to the initial comment line alone and verifies the same bad_json-vs-skipped-comment distinction.

A's K80 proposal does not kill M80; a-k27 does. A's K96 proposal does not kill M96; repaired a-k55/a-k57 and b-k09 do. Equivalent-target proposals that kill nothing are explicitly identified in the table.

No frozen predicate, target, fixture commitment, tool or lane tracked file was changed. Adding proposals to the frozen set would require a future registration, not a change in this round.
