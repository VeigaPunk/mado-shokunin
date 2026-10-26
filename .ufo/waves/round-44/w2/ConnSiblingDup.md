Report: .ufo/waves/round-44/w2/ConnSiblingDup.md
Status: complete. Post-landing sibling-duplication scan for round-44 landed facts across all 20 sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin`, read-only). **No duplication and no contradiction found in any sibling lane.** Extends w1/ConnSiblingOverlap.md (pre-land scan, same null result) to the landed data commit `e46789213830597348fe96a351ae004d10587385`.

## Scope and method
- Terms grepped per task: `sendWindowSize`, `ack_configure`, `gdktoplevel` (case-insensitive), fullscreen modes (`FULLSCREEN`/`MAXIMIZED`/integer semantics), `gkeep`; plus follow-ups `sendConfigure|size.request|xdg_toplevel|mado-geometry|gkeep-size|hyprland-gkeep`, `verdict=NOT_COMPARED`, `maximized=<`, `e467892`, `round-44`.
- Coverage: all 20 sibling lanes; gitignore-respecting pass plus a `gitignore:false` pass on the four lanes w1 flagged (kumitate, souji, kotoba, game-dev-2d).
- Recency sweep: all 257,242 sibling files with mtime ≥ 2026-10-25 (post-landing window) grepped for the landed-fact terms.

## Findings (each: term → sibling hits → disposition)

1. **`sendWindowSize`** — 0 hits in all 20 siblings. C2's report-size route fact is held only by mado. CLEAN.
2. **`gdktoplevel` / `GDK_TOPLEVEL`** — 0 hits (both cases). CLEAN.
3. **`ack_configure`** — sole hits are kagi-shokunin CPython changelog HTML (`test_pack_configure_in`, `.ufo/waves/round-26/build/ClockS027-artifacts/chlog.body:19490-19494` and a round-27 sandbox copy). Tk test names; unrelated. CLEAN.
4. **Fullscreen modes** — no sibling asserts Hyprland's `fullscreen` integer semantics (FULLSCREEN(2)/MAXIMIZED(1)) or mado's verdict vocabulary. All `FULLSCREEN`/`MAXIMIZED`/`fullscreen=2`-family hits are unrelated web artifacts: tabi WebDriver-BiDi spec snapshot (`webdriver-bidi-20261008.html:22092-22544`, WHATWG Fullscreen API bibliography), kake oEmbed crawl sources (`round-34/sources/S070.txt`, `S076.txt`, `round-36/sources/S094.txt`), kama/tsukuroi/revenger GitHub-page HTML, kagi vault-releases.json. No contradiction available for C1's landed contract. CLEAN.
5. **`NOT_COMPARED`** — tameshi-shokunin uses the same English token as lane-local tool vocabulary: `NOT_COMPARED` disclaimer tuple (`tools/pin-disposition.py:125-134`, `:687`; `tools/context-capture.py:185`, `:525`, `:1608`, `:2144`) and `NOT_COMPARED_LIMITS` (`:170-174`). This is a string-list of measurement disclaimers in a mutation/test-disposition tool, not a geometry verdict; different contract, different namespace, no cross-lane binding, no contradiction with C1's exit-5 verdict. Namespace coincidence only. CLEAN (note for arbitration: if either lane later cites the other's `NOT_COMPARED`, the tokens must be qualified by lane).
6. **`gkeep`** — byte-hits only, all non-substantive (directory-name mentions, not the landed size-request route facts):
   - kake-shokunin: `~/Projects` children census listings (`round-20/resume/paths-after.txt:67`, `round-21/waves/paths-before.json`, `round-24` receipts, `round-52/control/drift-before.txt:78`, `round-52/control/sweep-after.txt:78` — the round-52 pair is the only post-landing hit and is an informational name list); and ds4cc-marketplace provenance text (`round-24/c1-receipts/T16.json:44` etc., `round-33/sources/ds4cc-7fc6aa2f/sitemap.xml:10`) about the ds4cc.com gkeep *web page* — a different domain's fact.
   - souji-shokunin: tmp-snapshot hygiene census paths listing `/tmp/xsnapshot*/applied/hypr/gkeep.conf` (`census/operator-sweep-20261019/fresh-120min.txt:686` and 9 more); path hygiene only.
   - kotoba-shokunin: 2 coincidental substring hits inside a Bun binary `strings` dump (`.ufo/round-44/evidence/omp-live-18.12.2-strings.txt`); binary noise, verified by per-term `grep -c` on that file (only `gkeep` matches, 2×).
   - w1 reported a kumitate archived-session substring; this re-scan (gitignore off) finds no current kumitate hit — the archive appears rotated; no residual exposure.
7. **Cross-lane references to mado's artifacts** — only tsukuroi-shokunin round-40 tmp sweep noting a stale `/tmp/mado-geometry-selftest` file (`.ufo/waves/round-40/w1/SentScope.md:156`, `SentScope/sweep-evidence.txt:83`; round-40, pre-landing, hygiene observation). audio-shokunin's `round-44` hits are that lane's own same-numbered audio round, unrelated.

## Conclusion
The round-44 landed facts (C1 fullscreen/maximized verdict semantics + NOT_COMPARED exit 5; C2 sendWindowSize/report-size route, ack_configure zero-size sentence, GTK configured-size store, gkeep application_id line, S298-S301/S164 registration) exist in **no sibling lane**, before or after landing. No duplicate to arbitrate, no contradiction to correct.

## Arbitration owner (if a sibling later lands a conflicting claim)
- Primary: mado lane L1 (integrator) — owns the landed contract and any correction to it.
- Cross-lane registrar: kotoba-shokunin (overlap registrar per w1/ConnSiblingOverlap.md; its census r74 records mado adjacency `none` — consistent with this scan).
- Secondary surface arbitrators per w1: tsukuroi (host/compositor adjacency), game-dev-2d (sole `hyprctl clients -j` consumer, presence-fields only, disjoint), tameshi (tool-mutation method; owner of the `NOT_COMPARED` token collision noted in finding 5).

## Hygiene
- Read-only only on siblings; no installs (no tools needed beyond grep/find); no git/jj mutations anywhere. Seat created no scratch dir (pure greps); the one /tmp list file (<1 MB, under the 50 MB allowance) was removed. No host reads beyond plain filesystem grep.
- Verification: every claim above names its grep term and hit path; null results are from executed greps over all 20 lanes, not inferred.
