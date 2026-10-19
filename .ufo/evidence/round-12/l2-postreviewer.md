# L2 seat R12PostReviewer — final output (verbatim, 2026-10-19; reviewed commit 5174e15)

**Verdicts at 5174e15 (C1 mostly verifies, with a provenance defect and an unproven separability claim; C2 verifies with one miscount; C3 verifies, with one citation off by a line)**

**Reproduced**
- **Counts in after.txt (re-run at 5174e15):** QUALITY `lessons/` cites 11 and numbered criteria 16. `--no-live` gives 0 FAIL/UNKNOWN and 29 PASS. Live verify gives 52 pass / 0 fail / 8 notes. `--selftest` gives 268/268. `--regression` gives PASS with target e5894387…. `sha256sum tools/mado-verify.sh` gives fdd3a4d8…. SOURCES census: 39 rows, 0 malformed, A=35/B=1/C=3, mined 28 / queued 9 / rejected 2, empty dup/missing/used-by/enum/inflation checks. The criterion resolver (paths exist and M-rows exist) gives 11.
- **Diffs:** `--numstat` gives SKILL.md 20/0, QUALITY 16/0, SOURCES 114/0, so all pure insertions. Gate hunks are at mado-verify.sh:261, 265, 1291 (PIN only), 2191–2200 and 2218–2219. They touch no VERSION_STR (:77), no `--help` (:87, :93, :583–587, :973–975) and no marker blocks (MADO-R7 at :415–594, R8 heredocs at :1159–1192).
- **Gate quotes checked against source:**
  - S005: raw README line 19 matches.
  - S017: `<em>All</em> props must match for a rule to be applied` matches (the tag splits the quote).
  - S024: matches.
  - S013: install.sh:34 matches at HEAD 133b867.
  - S014: mado-verify.sh:2191 matches.
  - S002: arc-synthesis.md:300 matches, and the a6528e6 sha prefix a5b48331… matches.
  - S001: round-10 sha prefix d7b4708e… matches.
  - S018: HyprCtl.cpp:1566 at v0.56.2 matches.
  - S020: terminals.conf:4 matches.
- **U1 host claims (read-only, class/address selectors only, no titles):** `class:Alacritty` gives opacity 0.97, inactive 0.9, fullscreen 1, override false. Bare `Alacritty` and `class:NoSuchClass` both give "window not found". Both `getoption` values are 1.000000 with set false. `workspacerules -j` gives `[]`. `getprop` with no args gives "not enough args". `hyprctl version` gives 0.56.2 at efb5099. Host config matches: `terminals.conf:4`, `windows.conf:15`.
- **Host config for the SKILL erratum:** 18 sources, 32 lines, sha ce7483f35ab52bc2, with gkeep at line 32. Backup sha 4f52854a… matches.

**Breaks**
1. **[medium] C1 provenance.** QUALITY.md:19 is headed "Criteria from mined mistakes", but criteria 15–16 cite `lessons/round-12.md#inference-traps` (:28–40). That section is labelled "external, not incidents". The heading misattributes those two criteria. This is the same issue the critic raised: criteria 15–16 are not mado-owned mistakes.
2. **[medium] C1 separability not shown.** All of criteria 6–16 are imperative rules, so criterion 1 ("every claim falsifiable or marked opinion") has nothing to test. No per-criterion check against 1–5 is recorded. The resolver measures citation existence, not discernment.
3. **[low] after.txt:17 miscount.** `grep -c "Erratum (round 12" SKILL.md` gives 1 (SKILL.md:49), not 2. The `## Errata (round 12)` heading at :1588 does not match that pattern.
4. **[low] Unrecorded commands.** The freshness "7/26" and "sourced entries 4" lines have no printed command. They reproduce only under reconstructed definitions: verified-at + recheck = 7; any S-id in head-15 = 4. The navigation and counter fence lines in the harm-watch block also have no printed commands, and I did not reproduce them.
5. **[low] Gate citation.** S003 "never a naked assertion" is at PROTOCOL.md:331 (fleet 31baf5c), not :330.
6. **[low, unverified]** The criterion 8 citation `round-10.md:108-118` opens on "a gap is a bill", not path-landing. I read only the first lines of that range, so this needs a check.
7. **[info]** The worktree is not clean: `?? .ufo/evidence/round-12/after.txt` is untracked.

**Harm:** none observed on the axes I re-ran. The pin re-cut is disclosed and backed by the recut-2 mutant run (10/10 killed, restore sha matches).

**Checks for main agent:** re-run `--regression` and the navigation fence at 5174e15, and record the commands behind the freshness and fence lines.
