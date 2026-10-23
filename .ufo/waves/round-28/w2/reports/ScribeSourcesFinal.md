# ScribeSourcesFinal — round 28 wave 2

## Axis and scope
- Axis audited: C1 operability / S183 source provenance, via end-of-round frontier conformance. C2 calibration and coverage/U-items were not measured here.
- Measured census validity, final registry row count, S183 row/note conformance, changes against lane-tip blob `4f610066efd90804b055c42ae20c41a7f44404f9`, and the census-script digest.

## Findings and gates
- Census validation passed, exit 0. Seven W04 duplicate-URL warnings are present; the script reports the registry `ok` and these warnings do not fail validation.
- `census-start.txt` has the same seven W04 warnings, `mado ok`, and `exit=0`, but no numeric row count. Counting the committed lane-tip blob gives 182 rows; the final census reports 183, +1. The diff shows the increase is the newly appended S183 row.
- S183 has 11 contract fields. It is `mined`; `opened=2026-10-23`; `recheck=on-release`; `used-by=corpus/knowledge/mutation-testing-r28.md`. The note frontmatter says `verified-at: 2026-10-23`.
- The note's `## Gate` contains the URL, access date, and located 11-word quote: “Are mutants a valid substitute for real faults in software testing?”
- SHA256 matches required digest `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.

## Command record

1. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` — exit 0 (captured by the wrapper below).
   ```text
   mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
   mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
   mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
   mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
   mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
   mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
   mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
   mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
   exit=0
   ```
   Actual capture wrapper: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado; rc=$?; printf 'exit=%s\n' "$rc"; exit 0` — wrapper exit 0; validator exit 0.

2. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mado` — exit 0 (normal completion).
   ```text
   mado	rows	183
   mado	tier.A	176
   mado	tier.B	1
   mado	tier.C	6
   mado	status.mined	164
   mado	status.queued	10
   mado	status.rejected	9
   FLEET	rows	183
   FLEET	tier.A	176
   FLEET	tier.B	1
   FLEET	tier.C	6
   FLEET	tier.invalid	0
   FLEET	status.queued	10
   FLEET	status.mined	164
   FLEET	status.rejected	9
   FLEET	status.invalid	0
   FLEET	missing	0
   ```

3. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 4f610066efd90804b055c42ae20c41a7f44404f9:corpus/SOURCES.md | awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9][0-9]*[[:space:]]*\|/ {n++} END {printf "lane-tip rows=%d\n", n+0}'` — exit 0; output: `lane-tip rows=182`.

4. `awk -F'|' '/^\|[[:space:]]*S183[[:space:]]*\|/ {for (i=1;i<=NF;i++) gsub(/^[[:space:]]+|[[:space:]]+$/, "", $i); printf "fields=%d\nstatus=%s\nopened=%s\nrecheck=%s\nused-by=%s\n", NF-2, $9, $10, $11, $12}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` — exit 0; output:
   ```text
   fields=11
   status=mined
   opened=2026-10-23
   recheck=on-release
   used-by=corpus/knowledge/mutation-testing-r28.md
   ```

5. `awk 'NR>=1 && NR<=6 {print}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/mutation-testing-r28.md` — exit 0; output:
   ```text
   ---
   source:
     - S183
   verified-at: 2026-10-23 (S183 DOI metadata opened; prior-gate references checked)
   recheck: on-source-or-gate-change
   ---
   ```

6. `awk 'NR>=29 && NR<=35 {print}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/mutation-testing-r28.md` — exit 0; output:
   ```text
   ## Gate
   - **S183 URL:** https://doi.org/10.1145/2635868.2635929
   - **Access date:** 2026-10-23 (opened with the reader; CrossRef metadata, no abstract).
   - **Located quote (11 words):** “Are mutants a valid substitute for real faults in software testing?” — DOI reader, CrossRef `title` field. This is title metadata, not a quotation from the paper body.
   - **Source decision:** use S183 to identify and frame the paper's research question only. No article result or method detail is attributed to it.
   - **Prior-gate evidence:** M26-8, [`corpus/lessons/round-26.md:32`]; M27-3, [`corpus/lessons/round-27.md:15`]. These lane records show concrete finite-suite survivors and shortcuts, and bound the lesson to observed gate behavior.
   ```

7. `awk '/^## Gate$/ {gate=1} gate && /Located quote/ {print; found=1} END {if (!found) exit 1}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/mutation-testing-r28.md` — exit 0; output is the same located-quote line above.

8. `sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — exit 0 (normal completion); output:
   ```text
   3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
   ```

9. Corrected comparison: `diff -u --label committed-blob --label worktree <(git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 4f610066efd90804b055c42ae20c41a7f44404f9:corpus/SOURCES.md) /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md; rc=$?; printf 'exit=%s\n' "$rc"; exit 0` — diff exit 1 because it found additions (expected); wrapper exit 0. Relevant added row and search-log text:
   ```text
   +| S183 | Are mutants a valid substitute for real faults in software testing? — https://doi.org/10.1145/2635868.2635929 | paper | A | The paper's question of whether mutants are a valid substitute for real faults in software testing | DOI metadata `title` field; Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering; published 2014-11-11 (reader accessed 2026-10-23) | Frames mutant-to-real-fault substitution as an empirical question; the title does not establish that a mutation score predicts fault detection | mined | 2026-10-23 | on-release | corpus/knowledge/mutation-testing-r28.md |
   +Round 28 (2026-10-23), bounded question: what does the assigned primary mutation-testing
   +paper establish about finite mutant suites and real-fault detection? Identified/screened/
   +included/excluded: 1/1/1/0 at metadata/title scope. Opened the selected Just et al. DOI
   +with the reader, which returned CrossRef metadata (title, authors, venue and publication
   +date; no abstract); the same DOI's ACM target returned HTTP 403. No alternate URL or
   +source was opened. S183 is included only for the paper identity and its title's research
   +question; no finding from inaccessible article text is attributed to it. Stop: title
   +metadata plus the lane's M26-8/M27-3 gate records are enough to frame the bounded
   +question, not to report the paper's result or method details.
   ```
   Row audit: one new S183 row (fields `id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `status`, `opened`, `recheck`, `used-by`); no existing row changed. The other diff additions are the Round 28 search-log entry, not registry fields. Therefore no old→new status/recheck/used-by transition (or missing log entry) was found.

10. Initial comparison dead end: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 4f610066efd90804b055c42ae20c41a7f44404f9:corpus/SOURCES.md | diff -u --label committed-blob --label worktree - corpus/SOURCES.md; rc=$?; printf 'exit=%s\n' "$rc"; exit 0` — diff exit 2, output `diff: corpus/SOURCES.md: No such file or directory`. The worktree operand was wrongly relative to the fleet-root cwd; corrected comparison above used its absolute path and exposed the additions.

## Touched surfaces, out of scope, and failures
- Observed `corpus/SOURCES.md` changes: append S183 and a Round 28 search-log paragraph. I did not edit this file: validation passed, so no defect repair or row change was needed.
- Files written by this seat: `.ufo/waves/round-28/evidence/census-end.txt` (full validator output plus exit code) and this report.
- `corpus/knowledge/mutation-testing-r28.md`, lessons, counters, frozen registration, and product code were read-only/out of scope. No tests/builds, installs, or tool updates were run.
- No source-census check failed. The only failed command was the initial misrooted diff (exit 2); the corrected diff returned 1 as expected for detected additions.

## Artifact paths
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/census-end.txt`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w2/reports/ScribeSourcesFinal.md`
