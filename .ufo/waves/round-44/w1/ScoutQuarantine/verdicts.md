# Quarantine verdicts — mado, round 44 (2026-10-26), gkeep-size-request theme (seat ScoutQuarantine)

Read-only. Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(375 lines, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, byte-identical to round 43)
never edited. Re-run everything: `sh .ufo/waves/round-44/w1/ScoutQuarantine/verify.sh` (output 2026-10-26: all pass).

## Slice
The awk of the assignment yields 13 rows; `cmp` against `assimilation/quarantine-slice` is identical (sha256 `d9ea803d…bb45d`).
Families: `payload-absent` 6; never-checked prose 7 (second table's id cell lacks its closing backtick: ids print as `S199\``; ids unchanged).
Residue set (7 files, sha256 prefixes unchanged since round 43): r9 `3e0cf872`, r12 `2a3bb9f4`, r13 `4930768a`, r14 `a23782e3`,
r15 `aea823bc`, r30 `ff9c5ad1`, r31 `9edc926d`.

## Join result
- id-level: 13 slice ids vs `\bS<n>\b` in the 7 residue files: **0 hits**. The files name S216 S219 S251 S255 S256 S275 S281 S284 S285 S286 S287 S292 S293 S297 S298 S299 S302 S303 S304 S305 S310 S311 S312 (+S318/S319/S320/S326/S339 in the others) — none in the slice.
- source-level: URL/path tokens of all 8 source-bearing slice rows (EventManager, arch-wiki-docs-zh, 2604.18860, interwikimap, ai-usage, cn-export, 149787804, lxyoucan) in the 7 files: **0 hits each**. (Round 43 found 1 overlap, CSDN 149787804, but only through the *package* row S216 in `SOURCES.append.md:20` that r31:28 names by id; the residue file itself carries no CSDN URL.)
- Therefore no row is cited by the residue: **no adopt, no refuse (fabrication class) is owed this round.** Same as round 43, which verdicted only S199 (`unverifiable`).

## Verdict table (id, class, URL, evidence, verdict)

| id | class | URL / locator | evidence | verdict |
|---|---|---|---|---|
| S189 | payload-absent | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp | not cited by residue. Re-fetched 2026-10-26 HTTP 200, 6479 B (`EventManager.cpp.efb5099`, sha256 `eea605dfe5ce09e1…`): the register's quote **is present at line 128** (`auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`) — the register's "quote is in none of them" is false for this row | no action (not cited); register defect noted (false-absent), not edited |
| S195 | payload-absent | mirror.sjtu.edu.cn/…/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst | not cited; not re-fetched (outside province, localized channel) | no action |
| S199 | prose: could not be fetched (register:349) | https://blog.csdn.net/2301_76324845/article/details/149787804 | register has no quote → nothing to locate. Direct fetch 2026-10-26 HTTP 521, 2199 B stub (`csdn-2301_76324845.521.body`, sha256 `827e7c3e…`); reader proxy `r.jina.ai` HTTP 200, 69510 B (`csdn-149787804.proxy.txt`, sha256 `f9efb437…`) holds `windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$` at proxy line 152. r31:28 cites its staged id S216 for a *weather-glyph producer* claim — the row cannot support it | `unverifiable` (prose class); r31:28 stale-id defect stands (producer row is S248, as in round 43) |
| S200 | prose: could not be fetched | https://blog.csdn.net/lxyoucan/article/details/164457293 | not cited. Direct HTTP 521, 2126 B stub (`csdn-lxyoucan.521.body`, sha256 `fc6d0230…`) | `unverifiable` |
| S201 | payload-absent | https://arxiv.org/abs/2604.18860 | not cited by gkeep theme; not re-fetched | no action |
| S205 | payload-absent | wiki.archlinux.org api.php interwikimap | not cited by residue; not re-fetched | no action |
| S209, S222, S223, S225, S235 | prose: gate block named no locator (register:351-355) | cell is `## Gate — S<n>`, not a source | no locator ever existed; nothing to quote or fetch | `unverifiable` (not fabrication class) |
| S224 | payload-absent | /home/vgpnk/.cache/ai-usage/status.json | not cited | no action |
| S228 | payload-absent | lanes/mado/round5/fetch/cn-export-hyprland.html | not cited | no action |

Totals: adopt 0, refuse 0; `unverifiable` 7 (S199, S200, S209, S222, S223, S225, S235); `no action` 6 (S189, S195, S201, S205, S224, S228 — S189 additionally shown quote-present at the pin).

Comparison with round 43 (`round-43/assimilation/quarantine-verdicts.md`): slice bytes identical; register hash identical; residue hashes identical;
id-level join 0 = 0; S199 `unverifiable` repeated with a re-fetch (521 stub / proxy 200, quote at line 152 vs 160 — proxy text drifted 71957→69510 B);
S200 `unverifiable` repeated (521). New finding: S189's quote is present at the pin (round 43 did not probe it).

## Trap for the integrator: numeric collision outside the residue set
The package's *other* mado files cite packaged ids that equal slice ids numerically but name different documents: `chinese-wiki-canonical-url-r28.md:8` S222 (interwiki map = register S205 +17), `idle-lock-runtime-state-r28.md:9-11` S223/S225/S228, `host-bar-producers-r28.md:8-9` S224/S228, `two-literature-coverage-r25.md:8` S209. A numeric join over the whole package would report false hits on S209/S222/S223/S224/S225/S228 — packaged ids are not register ids (register S205→package S222, S224→S241, etc.; the register sits +17 for source-bearing rows). None of those files is in the round-44 residue set.

## Quotes used (≤25 words, located by verify.sh)
- "the cited source could not be fetched, so no quote was checked" — register:349 (and :267-268 other lanes)
- "the gate block named no locator, so no quote was checked" — register:351
- "the codemap entry and the producer's branch structure (round 5's row S216)" — glyph-and-geometry-r31.md:28
- `windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$` — csdn-149787804.proxy.txt:152
- `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` — EventManager.cpp.efb5099:128
