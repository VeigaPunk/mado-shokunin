# RevClaimsCounter — w2 falsify (round 50, attempt 2)

Seat: RevClaimsCounter. Attack rev: `b4a79843cc2545bbe800db9322e58f6e00436629` (master tip).
Scope: claim/counter/admission consistency for C1 and C2 (claims.md vs registration vs receipts).
Verdict: **no actionable defect found** — the claim/counter/admission chain is consistent at the attack rev on every axis checked.

## The table

### C1 — coverage (sourced): `corpus/knowledge/hyprland-bind-key-match-r50.md`

| field | value | verified |
|---|---|---|
| claim | one axis-move: coverage/expansion, "sourced" label | claims.md:29-37; counter docstring: "(C1, coverage, sourced)" |
| frozen counter | `quality/counters/c1-r50-bind-entry.py` sha256 `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0` | `git cat-file blob b4a79843:…` sha256 = freeze value ✓ |
| predicate sentence | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET` | registration.md:31; counter docstring clauses a-r |
| data rev | `906178b607f2071af7c2efec5aad976a8bfa5757` | receipt final line names it ✓ |
| receipts | `receipts/c1-at-data.txt` (final line exact, rc 0); `receipts/controls-c1.txt` | both byte-identical between freeze `470bfd77` and attack rev (sha256 compared) ✓ |
| controls | c00-absent `a:0 … TARGET_MISSED` rc1; c13-r49-paste `f:0 r:0 … MISSED` rc1; c12-stub `b:0 e:0 f:0 g:0 h:0 i:0 j:0 r:0 … MISSED` rc1 — all exactly as registration quotes | controls-c1.txt contents ✓ |

### C2 — operability: session-material gate v3

| field | value | verified |
|---|---|---|
| claim | one axis-move: operability (evidence-privacy gate v2→v3) | claims.md:39-46; registration.md:45 |
| frozen counter | `quality/counters/c2-r50-session-gate.py` sha256 `1d52a62cd969aba59c2cd1f944212b6f9619212b5fb313c470c4c14ebd62b298` | matches at attack rev ✓ |
| predicate sentence | `selftest=94/94 names=69/69 red=K/K green=K/K scope=seen verdict=TARGET_MET` | registration.md:49 |
| data rev | `906178b6…` | both receipts name it ✓ |
| receipts | `receipts/c2-at-data-nonce50117.txt` (`red=42/42 green=44/44`), `receipts/c2-at-data-nonce778899.txt` (`red=44/44 green=41/41`) — final lines exact, rc 0 | byte-identical freeze↔attack ✓ |
| controls (nonce 602211) | c00-v2-at-base `selftest=69/69 red=0/41 green=0/40 scope=blind TARGET_MISSED`; c12-stub `selftest=34/94 green=0/40 TARGET_MISSED`; c14-v3-ufo-default `selftest=93/94 red=0/41 scope=blind TARGET_MISSED` — all rc 1, exactly as quoted | controls-c2.txt contents ✓ |

## Checks

(a) **One-axis + separable** — C1 is the coverage/expansion move, C2 the operability/quality-trend move (claims.md "Lowest-axis rule"); counter docstrings confirm disjoint reads: C1 reads entry/registry/lesson/`corpus/README.md`/pins/receipt only; C2 reads `quality/check-session-material.py` at the rev + its own generated fixtures. ✓

(b) **Receipts exist at b4a79843 with quoted final lines** — all five receipts exist; final lines byte-match the kill-rule sentences; all five are sha256-identical to their freeze-commit (`470bfd77`) blobs, so no post-freeze receipt tampering. ✓

(c) **'sourced' is real** — all 12 rows S352-S363 exist in `corpus/SOURCES.md` `## Registry` (lines 301-312), every opened date = 2026-10-27, recheck cells valid, used-by → the entry/lesson; the entry's head cites 10 of them (`source: S###` lines; S357/S358 are tool-only per entry line 3) and its `verified-at: 2026-10-27` gate date matches. Data receipt clause b: `ids=10 … verified=2026-10-27 recheck=on-release readme=1 ok=1`; clause i: `new_rows=12`. The 14 upstream fetch pins are byte-equal to the round-49 pins (cmp loop: same=14, diff=0). ✓

(d) **Two-nonce requirement** — nonces 50117 and 778899 each have an exact TARGET_MET receipt at the data rev; the control nonce 602211 is distinct; my third-nonce reproduction (424242) at the attack rev also scores `selftest=94/94 names=69/69 red=42/42 green=41/41 scope=seen verdict=TARGET_MET` rc 0 — nonce-independence holds. ✓

(e) **QUALITY criteria 100-102** — exist in `corpus/QUALITY.md` under "## Criteria from the round-50 w1 quality seat (round 50; …)": 100 → `quality/check-state-cite.py` (M49-1), 101 → `quality/check-deliverables.py` (M49-3), 102 → `quality/check-wave-done.py` (round-49 D2). All three instruments exist at the rev; `check-wave-done.py` sha256 = frozen `10f4359a…`. ✓

(f) **README/SKILL pointers resolve** — `corpus/README.md:77` holds exactly one index row naming `knowledge/hyprland-bind-key-match-r50.md` (three cells, no redirect word, ids cover the head); the round-50 Frontier bullet at `corpus/README.md:114` names it; `SKILL.md:2241` points at the entry (file exists at rev). Note: the counter's README constant is `corpus/README.md` (counter line 163); the 14-line root `README.md` names no knowledge index and no claim requires it to. ✓

## Reproduction at the attack rev (evidence)

Clone: `git clone -q --shared` into `/fast/scratch/hyaku/mado-r50/RevClaimsCounter/lane` (toplevel asserted).

- `TMPDIR=<scratch> python3 -I quality/counters/c1-r50-bind-entry.py --repo <clone> --rev b4a79843…` →
  `PRED-C1-r50: clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET rev=b4a79843…` rc 0 (clause r `replay=ok sha=9a47199e2297 binds=192`).
- `python3 -I quality/counters/c2-r50-session-gate.py --repo <clone> --rev b4a79843… --work <scratch> --nonce 424242` →
  `PRED-C2-r50: selftest=94/94 names=69/69 red=42/42 green=41/41 scope=seen verdict=TARGET_MET rev=b4a79843…` rc 0.

Also consistent: claims.md and registration.md blobs at b4a79843 equal their freeze commits (`13631f24`, `470bfd77`) sha256-for-sha256; `w1-results.json` parses to 54 w1 rows, 0 unsettled; the 4 wrap-up-cut seats (CritC1Random, CritC1Exotic, MutC2Entry, CritQuality) have committed w1 reports; round-49 lesson erratum (D8) present at `corpus/lessons/round-49.md:65`; `fetch/SHA256SUMS` verifies for all 15 real pins (its self-line cannot match by fixed-point construction — artifact, not a defect).

## Residual risk / verification gaps

- C1 clause r replay reads the live compositor socket; it succeeded on this host at attack time, but the receipt's replay leg is host-state dependent (registration declares this residual).
- C2 green/red K varies by nonce (41-44) because fixtures are nonce-sized; I added one nonce, not a sweep.
- Instrument correctness (as opposed to claim/counter/admission consistency) is attacked by sibling seats; my scope did not re-derive clause internals beyond the docstrings and receipts.
- Pin truth upstream (that the pinned bytes really are Hyprland 0.56.2 at `efb50993` etc.) was not re-fetched; byte-equality with round-49 pins was verified instead.

## Deliverables

- Report: `.ufo/waves/round-50/w2/RevClaimsCounter.md` (this file).
