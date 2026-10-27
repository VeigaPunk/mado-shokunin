# ScoutQuarantineAudit — round 51 w2

## Deliverables
- `.ufo/waves/round-51/w2/ScoutQuarantineAudit/quarantine-audit.md`

Report: `.ufo/waves/round-51/w2/ScoutQuarantineAudit/quarantine-audit.md`

## Finding
The 13 row IDs in `w1/ScoutQuarantine/quarantine-verdicts.md` match the mado slice of the read-only register: payload-absent S189, S195, S201, S205, S224, S228; unchecked/unreachable-prose S199, S200, S209, S222, S223, S225, S235. The register's class is provenance about prior checking, not proof that a payload is absent. W1 correctly uses `unverifiable` for all 13 rather than relabeling any as fabricated/absent. Confidence: high for row identity and class; no quote-presence conclusions.

## Row-by-row disposition and flip requirements

| ID | Register class / W1 classification | What would be needed to flip from unverifiable |
|---|---|---|
| S189 | payload-absent; payload available only by cited immutable Hyprland raw URL | Fetch/verify exact commit payload, inspect exact quoted line and companion/local artifacts. Quote found => present; reproducible comprehensive absence check => absent. |
| S195 | payload-absent; remote `.pkg.tar.zst` archive | Obtain exact archive bytes, verify integrity, list/extract relevant payload and search both Chinese quote fragments; inspect companions. |
| S201 | payload-absent; arXiv paper URL | Obtain paper/version bytes and search both quoted passages, with companion/local artifact checks. |
| S205 | payload-absent; ArchWiki API JSON URL | Fetch the relevant response (or archived exact response), check both exact JSON fragments and companions. |
| S224 | payload-absent; host-private `/home/vgpnk/.cache/ai-usage/status.json` | Authorized access to the exact captured file or its immutable capture/companion artifacts; compare exact timestamp line. W1 appropriately did not infer its state from a different missing `.qcache`. |
| S228 | payload-absent; lane-relative `lanes/mado/round5/fetch/cn-export-hyprland.html` | Locate the historical lane capture and companion artifacts; inspect exact Chinese phrase. |
| S199 | source-fetch unreachable prose | Successful independent retrieval of the cited CSDN URL or an attributable archived capture, then quote and companion checks. |
| S200 | source-fetch unreachable prose | Successful independent retrieval of cited CSDN URL or attributable archived capture, then quote and companion checks. |
| S209 | unchecked prose, no locator | A source locator plus source payload/capture and the original quote/context; without locator there is no source content to classify. |
| S222 | unchecked prose, no locator | Same: locator and inspectable payload/capture plus quote/context. |
| S223 | unchecked prose, no locator | Same. |
| S225 | unchecked prose, no locator | Same. |
| S235 | unchecked prose, no locator | Same. |

A match can establish `present` even if the register's earlier automated match failed. `absent` requires actual examination of the cited source and relevant companion/local artifacts, not merely repeating the register's label. For inaccessible sources, failed fetches alone support neither fabrication nor absence.

## Evidence and scope
- Row IDs/classes/locators/quotes: read-only `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, rows 141–146 and 349–355 (grep line references).
- W1 verdicts and stated limitations: `.ufo/waves/round-51/w1/ScoutQuarantine/quarantine-verdicts.md:3-68`.
- Assignment's 6+7 row grouping is independently consistent with the register and W1 artifact. The register describes payload-absent records as previously checked, but the W1 seat did not redo those source inspections; do not inherit that history as fresh evidence.
- No source payload was fetched or opened for this audit; therefore all 13 per-row quote outcomes remain unverifiable. This is an explicit evidence gap, not an absence finding.
