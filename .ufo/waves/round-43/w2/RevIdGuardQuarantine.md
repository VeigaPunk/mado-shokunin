# Seat RevIdGuardQuarantine — round-43 w2 (id guard re-run, renumber map vs landed, quarantine spot-checks)

Status: DONE. Full findings: `.ufo/waves/round-43/w2/RevIdGuardQuarantine/findings.md`. Scratch
`/fast/scratch/hyaku/mado-r43/RevIdGuardQuarantine/` deleted; all receipts are in the seat dir.

## Findings (each names what it attacks or supports)

1. **Guard holds at the data commit** [supports]. Round-prompt guard (0-3 leading spaces) re-run at
   `1959770` directly on the git object: reg 234 / staged 147 / collisions 42; at freeze `b2e2efd` it
   reproduces w1 byte-identically (226/147/34; sha256 `76e986db…`, `079d7538…`, `da4b74d2…` equal w1's
   published artifact hashes). Delta = exactly S290-S297 added, none removed; 0 registry rows at ≥4
   spaces; no duplicate ids in the landed registry. The 8 new collisions are the reserved-band
   staged rows by construction; the landed registry itself is collision-free.
2. **Guard proof** [supports]. On a scratch registry with `  | S203 |` (two leading spaces) colliding
   with the staged set: 0-3 extractor → collisions = {S203} (nonempty, guard fires); a column-zero-only
   extractor → 0 collisions (the false-green the pattern prevents); a four-space row is invisible to
   both (measured blind spot, matches w1).
3. **Landed ids verified** [supports]. At `1959770`: rows S290-S297 carry exactly the claimed
   documents (five Hyprland files at `efb5099…`, host-gkeep.conf, host-clients-r43.json,
   gkeep-ui-excerpt.py); no row S298+; S155/S158 each gained exactly one used-by item
   (`, corpus/knowledge/hyprland-gkeep-geometry-r43.md`), no other cell touched (+10 −2 registry diff);
   the entry cites exactly {S155, S158, S290-S297}.
4. **Renumber map vs landed: 6 pin mismatches, 2 matches, 13 dropped documents** [attacks
   `assimilation/renumber-map.tsv` + `id-guard.md` §5]. Map said DefaultFloatingAlgorithm→S292,
   Target→S293, WindowTarget→S294, GeometricMovableAnimated→S295, host-gkeep.conf→S297,
   excerpt→S299; landed S291/S292/S293/S294/S295/S297. Matches: WindowRuleApplicator→S155 held,
   HyprCtl→S158 held. Map gaps: RegexMatchEngine (S290), host-clients (S296). Map rows unused by the
   landing: Window.cpp→S164 (entry cites no Window.cpp row), ui.py→S300, gtk4→S303, wiki 0.56.0→S304,
   nerd-fonts→S301, 8 lanes/mado artifacts→S302/S305-S311 — none landed, none refused (lesson refuses
   4 staged FILES only).
5. **Executing the frozen map today would mis-attach five documents** [attacks `renumber-map.tsv`
   rows S251/S302/S303/S304/S305]. Their targets now hold different documents in the landed registry
   (e.g. map "S302→S292 pin DefaultFloatingAlgorithm" but landed S292=Target.cpp). The map's own
   near-miss hazard, realized between map and landed data; re-derive before any future use.
6. **Landed mapping IS by document** [supports, with one caveat]. One id per document; held docs
   reused (S155/S158); no duplicate-document row created. Caveat: pre-existing S018/S158 are two URL
   forms of HyprCtl.cpp and the used-by went to S158 only (asymmetric pair, consistent with
   `id-guard.md` §6 finding 1); and the by-document mapping covers only the admitted subset — 13 of
   the map's 19 documents have neither a landed row nor a refusal.
7. **Frozen w1 prose defect** [attacks `assimilation/id-guard.md` §6 finding 2]: says "the other six"
   but lists five ids, omitting S293.
8. **Quarantine spot-check 3 of 13: S199 HOLDS, S200 HOLDS, S189 FALSIFIED** [attacks register:141 via
   `assimilation/quarantine-verdicts.md` §6]. S199: direct re-fetch HTTP 521 (stub sha `a5a6ce51…`),
   proxy 200 carrying the quoted `opacity 0.80` rule at proxy line 152 — both legs reproduce. S200:
   direct re-fetch HTTP 521 (stub sha `62721e72…`). S189: the row pins EventManager.cpp @ `efb5099`
   and claims the quote "is in none of them" (the register's fabrication class); re-fetch HTTP 200
   (sha `eea605df…`) and the quoted line is present at line 128, byte-identical including the 13-space
   `auto             eventString` run. The `payload-absent` class is unreliable without per-row
   re-verification; the other five payload-absent rows (S195, S201, S205, S224, S228) were not
   re-fetched and should be before any reader acts on them. New evidence — w1 issued no verdict on
   the unnamed rows.

## Verification gaps

C2 counter, entry quote/locator binding, lesson sections beyond ADMIT/REFUSE, README/PROVINCE/SKILL/
QUALITY rows: other seats' items. Remaining 10 slice rows not re-fetched. w1's +17 offset claim not
re-derived (inputs pinned by sha256 instead).

## Tools

None installed (base-system grep/sort/comm/wc/curl/sha256sum/python3; no pacman, no uv, no npx).
Network: 4 read-only GETs. No compositor read, no input injection, no git mutation.

Report: .ufo/waves/round-43/w2/RevIdGuardQuarantine.md
