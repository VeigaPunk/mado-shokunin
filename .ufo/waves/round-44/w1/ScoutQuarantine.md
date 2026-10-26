# ScoutQuarantine report (round 44, w1, assimilation item 10)
Status: done. Full table: `.ufo/waves/round-44/w1/ScoutQuarantine/verdicts.md`; re-run `sh .ufo/waves/round-44/w1/ScoutQuarantine/verify.sh`.
- Slice re-derived: 13 rows, byte-identical to `assimilation/quarantine-slice`; register sha256 `5afe1810…d833` (375 lines) unchanged; 7 residue files unchanged vs round 43.
- Joins: id-level 0 hits; source-level 0 hits for all 8 source-bearing rows. No row cited by r9/r12/r13/r14/r15/r30/r31 → no adopt, no refuse.
- Verdicts: 7 prose rows `unverifiable` (S199, S200 fetch 521 / proxy 200 for S199; S209, S222, S223, S225, S235 no locator); 6 payload-absent rows no action.
- New: S189 register quote is PRESENT at EventManager.cpp@efb5099 line 128 (register "absent" is false for it; not cited, register not edited).
- r31:28 stale id S216 (CSDN blog) for a weather-glyph claim; producer row is S248 (matches round 43).
- Trap: package files r25/r28 cite packaged ids S209/S222/S223/S224/S225/S228 that numerically equal slice ids but are different documents (+17 offset); never join by number.
- Tools: curl only; scratch removed. No installs.
