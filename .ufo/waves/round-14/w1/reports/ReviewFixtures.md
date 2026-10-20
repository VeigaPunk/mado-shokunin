# ReviewFixtures — rendered report (mado-r14-w1)

Full findings: `.ufo/waves/round-14/w1/ReviewFixtures.md`. Read-only review; nothing executed; no edits to `tools/mado-verify.sh`.

## Findings (by severity)

1. **High — C2 operability: resolver accepts directory-shaped targets.** `hypr.root.sources_resolve` uses `[ -e ]` for direct targets (~L2420) and `compgen -G` for globs (~L2421–2423). A directory satisfies both, so a directory where a sourced file belongs reads PASS. The census in the same plane already uses `[ -f ]`. Fix: `[ -f ]` for direct targets, a glob must have ≥1 regular-file match, and non-regular matches get a separate `nonregular:` token on the same owning row.

2. **Medium — coverage: no isolated source-order negative.** The positional walk (`include_graph`, ~L2391–2396) is never exercised for order alone. Recommended case N10: swap `monitors.conf` (file line 14) and `input.conf` (line 15) with `sed '/^source = ~\/.config\/hypr\/monitors.conf$/{N;s/\(.*\)\n\(.*\)/\2\n\1/}'` on a copy of the clean fixture. Expected: `include_graph` FAIL with `line 11: got '~/.config/hypr/input.conf' want '~/.config/hypr/monitors.conf'`; `sources_resolve`, `hypr.local.inventory` and `theme.chain.hypr_include` (line-13 anchor) stay PASS. Pin only; the order path already works and is not an improvement.

3. **Medium — coverage: no directory-target negatives.** N9: replace `gkeep.conf` with a directory (expect `sources_resolve` FAIL `nonregular:`, `include_graph` PASS, local census FAIL `missing: gkeep.conf`). N11: replace the only `toggles/hypr/*.conf` match with a directory (expect `sources_resolve` FAIL `nonregular:` on the glob; `include_graph` PASS). N11 also changes the no-gaps toggle row (~L2511); its expected status must be asserted, not left implicit. N9 is red until finding 1 lands.

4. **Process — derived target moves.** Findings 1–3 sit outside the MADO-R7/R8 marker pairs, so L1 must re-cut `PIN_MADO`/`TABLE_MADO` per the header rule. Do not place the new cases inside the R8 pair to avoid it. Until re-cut, `--regression` reads SETUP.

5. **Informational — no new cases exist yet.** No U5 output-management, colour, directory or order-shaped scenarios are present in the file. Terminal theme includes are fixtured and read (~L2638–2672), but those rows judge size and padding only.

## Judgement
- Coverage: directory path and order path both unexercised; proposed N9–N11 close that. U5 output/colour boundaries are not advanced by this lane.
- Operability: fix keeps `unresolved:` and existing N2/N4 assertions intact; owning-row diagnostics stay stable.

## Gaps
- Nothing run (by instruction). The N10 sed, the glob loop in finding 1, and the N11 toggle-row side effect need confirmation at L1.
- Line numbers will shift after the GateImplement edit.

## Tooling
None installed or upgraded.
