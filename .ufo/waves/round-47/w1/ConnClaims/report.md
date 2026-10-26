# ConnClaims — seat status (round 47 w1)

Seat: `ConnClaims` (leaf; cross-claim / cross-item pattern scan). Date 2026-10-26.
Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`; base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (round start).

Deliverable: the pre-freeze checklist (full report) is
`.ufo/waves/round-47/w1/ConnClaims.md` — three parts: (1) C1/C2 separability both
ways, recipe for the frozen counters; (2) registration-v2/v3 failure patterns from
rounds 45/46 that will recur, with pre-emption moves for the v1 freeze; (3) routed
items sharing a cause with the claims (R1 receipts provenance vs the C2 live clause,
R2 untracked artifacts vs the C1 fixture/expect hygiene, R3 session-material gate vs
both claims' receipts, R4 supersession vs the C2 SOURCES census top).

Evidence read (all lane paths): `SCORECARD.md` rounds 45/46
(`:2594-2652`); `.ufo/waves/round-45/registration.md` + `registration-v2.md`;
`.ufo/waves/round-46/registration-v2.md` + `registration-v3.md`;
`.ufo/waves/round-46/w1/CritC2Forgery.md` (+ `patches/`, `tighten.out`);
`.ufo/waves/round-46/w1/ExecC1Separability/report.md`; `.ufo/waves/round-45/w1/ConnCrossClaim.md`;
`corpus/knowledge/terminal-route-r17.md:140-152`; `corpus/lessons/round-46-verifier-spotcheck.md:105-122`;
`corpus/knowledge/hyprland-input-devices-r46.md:55-57`; `quality/check-session-material.py:1-57`;
`quality/counters/c2-r46-input-device-entry-v2.py:1-87`; `.ufo/waves/round-47/claims.md`, `w1-spec.json`.

No writes outside the seat dir and `ConnClaims.md`; no tools installed; scratch
`/fast/scratch/hyaku/mado-r47/ConnClaims` removed at finish.
