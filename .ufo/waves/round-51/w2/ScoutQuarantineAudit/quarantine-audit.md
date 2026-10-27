# Quarantine audit

## Finding
The 13 IDs in `w1/ScoutQuarantine/quarantine-verdicts.md` match the mado register slice: payload-absent S189, S195, S201, S205, S224, S228; unchecked/unreachable-prose S199, S200, S209, S222, S223, S225, S235. Register class describes previous-check status, not proof of absence. W1 correctly marks all unverifiable, not fabricated/absent. Confidence: high on identity/class; no quote outcome established.

| ID | Class | Source access needed to flip from unverifiable |
|---|---|---|
| S189 | payload-absent | Fetch exact immutable Hyprland commit payload; inspect quote and companion/local artifacts. |
| S195 | payload-absent | Obtain exact `.pkg.tar.zst`, verify/extract relevant archive contents; search both fragments and companions. |
| S201 | payload-absent | Obtain cited arXiv version bytes; search both passages and companions. |
| S205 | payload-absent | Fetch relevant ArchWiki API response or attributable archived response; check exact JSON fragments. |
| S224 | payload-absent | Authorized access to exact private cache capture or immutable copy/companions; check exact timestamp line. A different missing `.qcache` is not evidence. |
| S228 | payload-absent | Locate historical `lanes/mado/round5/fetch/cn-export-hyprland.html` and companions; inspect phrase. |
| S199 | unchecked/unreachable prose | Successfully retrieve cited CSDN URL or attributable archived capture, then inspect quote/context. |
| S200 | unchecked/unreachable prose | Successfully retrieve cited CSDN URL or attributable archived capture, then inspect quote/context. |
| S209 | unchecked prose, no locator | Obtain a locator and inspectable payload/capture plus original quote/context. |
| S222 | unchecked prose, no locator | Same. |
| S223 | unchecked prose, no locator | Same. |
| S225 | unchecked prose, no locator | Same. |
| S235 | unchecked prose, no locator | Same. |

A matching quote supports `present`; `absent` requires examination of cited source plus relevant companions/local artifacts. Failed fetches alone establish neither. W1 explicitly had not completed source checks for these rows, so this audit does not independently verify the original register's past-check claims.

Evidence: read-only shokuknow register rows 141–146 and 349–355; W1 verdict artifact lines 3–68. No source payload was fetched/opened for this audit; all 13 quote outcomes remain unverifiable.
