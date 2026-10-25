# RevCommitChain — verification of RevM37Routing's F3 correction (scratch record)

Date: 2026-10-25. Auditor: L1Mado38.RevCommitChain (leaf).
Reason: my committed report (.ufo/waves/round-38/w1/reports/RevCommitChain.md, folded into the
lane by errata 3f14bd2) is read-only per lane bounds; this correction is recorded in scratch
and delivered via the final message + peer reply.

## Replays (byte-identical inputs; checker = HEAD quality/check-r38-discrimination.py;
instruments/manifests extracted from git blobs; sandbox under /tmp/mado38-RevCommitChain/sbparent)

| run | c1 | c2 | manifest | --rev | result |
|---|---|---|---|---|---|
| A | frozen 58e55ec9 | frozen | frozen | efb0ec2 (data rev) | **18/19** — duprow sole fail `c1-duprow observed=TARGET_MET ok=0` |
| B | frozen | frozen | HEAD (b6c1d31) | efb0ec2 | **19/19 TARGET_MET** |
| C | frozen | frozen | frozen | 58e55ec9 (freeze rev) | **18/19** — duprow sole fail |
| D | frozen | frozen | HEAD | 58e55ec9 | **19/19 TARGET_MET** |

Receipt files: /tmp/mado38-RevCommitChain/replay-{A,B,C,D}-*.txt (quoted tails in this record).

A tail: `MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED` (rc=1),
only `control=c1-duprow ... expected=TARGET_MISSED observed=TARGET_MET ok=0`.
B tail: `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET` (rc=0).
C tail: identical to A. D tail: identical to B.

## Conclusions

1. **RevM37Routing's correction is verified:** the 859d0cf counter patch was NOT load-bearing —
   frozen C1 × fixed manifest = 19/19 at both the data rev (B) and the freeze rev (D). The
   load-bearing post-freeze change for the 19/19 outcome is the manifest control `c1-duprow`
   fix alone (out-of-table append → in-table insert).
2. **RevCensusBefore's "frozen pair 19/19 at freeze rev" is NOT reproduced.** Byte-identical
   frozen instruments × frozen manifest at --rev 58e55ec9 = 18/19 (C). The distinguishing
   variable is the MANIFEST version, not the rev. SOURCES.md structure at every tested rev
   (58e55ec9, efb0ec2, 3f14bd2) has `## Registry` (line 9) … `## Paths` (221/225) with only
   trailing `## Leads (unopened)` content after — so the frozen crib's EOF append lands outside
   the `## Registry` region at every rev, which is exactly why the frozen pair fails
   `c1-duprow` at both revs. RevCensusBefore's 19/19 is consistent with frozen counters ×
   FIXED manifest (B/D), suggesting a manifest-version mislabel in their run; I cannot
   reconstruct their exact command.
3. F1/F2 of my committed report stand factually (post-freeze counter change, post-data manifest
   rewrite keeping id/frozen_at/note) — the ecosystem's errata (3f14bd2, c44873e, 3674cf2)
   now declare the frozen claim failed and route the new predicate to closure; that declaration
   was absent at score-commit time (f0c9432a).
4. RevM37Routing's E2-flag for the closure ruling: the v3 E2 lineage floor rejects the
   round-37 honest proxies h2/h3 (`lineage=1/2`) — paraphrase sensitivity. Not a commit-chain
   item; relayed to the ruling.
