# PROVINCE.md append — round-66 instrument addendum

Insertion: append immediately after the round-65 refinement paragraph at `PROVINCE.md:276`
(the line beginning `**Round-65 refinement (append-only; two record counters, one standing
instrument, no new write surface):**`). Append-only; this does not edit any existing line and does
not add a write surface.

---

**Round-66 refinement (append-only; two record counters, one hardened standing instrument, no new
write surface):** the round-66 instruments are `quality/counters/c1-r66-register.py` (reads git
objects at `--rev` only; requires exactly one returned-host heading, exactly one row per eight
groups, a resolving receipt in each row's receipt cell, and the exact live CLEAN line from
`.ufo/waves/round-65/receipts/gate-live-r65.txt`; writes nothing), `quality/counters/c2-r66-landing-
instrument.py` (a read-only driver that pins `--rev` to a commit SHA, extracts the hardened
instrument and its three frozen dependencies at that rev into private scratch, strips inherited
`GIT_*` from git and leg children, refuses tmp-family and symlink-ancestor scratch, and writes only
under its declared scratch), and the hardened `quality/landing-counters.sh` (requires `--round N`,
selects `.ufo/waves/round-N/receipts` and applies the dirty guard to explicit citecheck paths;
validates each child's actual marker against its rc — navigation `indexed=A/B`, used-by
`MADO_USED_BY:`, ledger `LEDGER:`, citecheck `MADO_CITECHECK:` — and maps genuine red rc=1 to RED/1,
while rc>=2, an absent or inconsistent marker, or a missing used-by sibling maps to ERROR/2; GREEN
requires four green markers and rc=0). They score the lane's own record and the receipts it lands;
none touches a config plane, a compositor socket or a host service. The marker checks are bounded
structural consistency, not authentication or truth binding: register state-cell truth remains NOT
measured, and a child that forges its own marker is outside this bound. The round-66 declaration's
`MADO_TOOL_LEDGER` literal is a recorded premise error
(`.ufo/waves/round-66/marker-premise-erratum.md`); the instrument anchors the child's actual
`LEDGER:` line and never renames child output. The r65 counters and instrument bytes stay frozen;
round 66 adds successors. The omarchy-host freshness register above is untouched by this addendum.
