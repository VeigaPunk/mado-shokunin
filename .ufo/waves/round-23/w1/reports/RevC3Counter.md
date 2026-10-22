# RevC3Counter: C3 counter attack (round 23, wave 1)

Seat: `MadoR23.RevC3Counter` (leaf; no agents spawned). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, read-only except this report. Scratch: `/fast/scratch/hyaku/mado-r23/RevC3Counter` (branch `revc3`, never pushed). Pinned rev `a28e4815aabfa85f55274884000fb2608355f8cf`; lane tip at review `4de44647f93bfd25ed5c979f61ff016b50456549` (landed C3 v2).

Scope: attack the C3 counter against SHONEN box 4, "No cross-domain bleed (PROVINCE.md still accurate)". The L1 note asked for probes re-run against v2 at 4de44647, the v1 holes v2 closes, and the holes that remain. Both are answered in sections 4 and 6.

## 1. Verdicts

| Question | Verdict | Confidence | Basis |
|---|---|---|---|
| Does the pinned run reproduce (count 4, exit 1)? | Yes | High | Direct run at a28e4815 (section 2, command 1) |
| Can the counter be gamed? | **Yes.** v1 by prose, comments, bullet denials, substrings and unticked boxes. Landed v2 still reaches 0 by table shapes that declare nothing (denial cells, dash cells, tables inside fences or HTML comments), by tool names with no extension or non-ASCII names, by stale rows, and by a config-writing tool declared "nothing". | High | 27 committed states; each counter is a pure function of committed bytes, so one run per rev is conclusive for that rev |
| Does it measure a self-assessment mismatch as the hyaku rule requires? | **No** (v1 and v2). Both count tools that have no PROVINCE row. Neither reads what any tool reads or writes, neither checks any row for truth, and SHONEN is read only for one phrase. The five at base are five missing rows, not five observed bleeds. | High | By construction; probes `T_bleed` and `T_sibling` read 0 under v2 |
| Is a stricter one-command check possible? | **Yes, proposed and tested** (`count_v3.py`, commit `af1ef0f7` in scratch). It closes every table, population, stale-row and declared-bleed probe except one. It stays blind to config writes built from variables (`T_indirect`) and to whether row prose is true. Not landed; the lane decides. | Medium | Heuristic scanner; tested on the five base tools and 27 committed states |

**Verdict line: gameable: yes. Measures observed bleed: no (partially under v3). Stricter v3: proposed and tested, not landed.**

## 2. Commands and receipts

1. Pin check, lane counter (v1 script in the working tree before v2 landed):
   `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/c3/count.py a28e4815aabfa85f55274884000fb2608355f8cf`
   Result: exit 1, `"count": 4`; mismatches `tools/mado-action-plan.py`, `tools/mado-assessment.py`, `tools/mado-evidence-audit.py`, `tools/mado-tripwire.py`. Tracked tools: five (`tools/mado-verify.sh` is credited by prose in PROVINCE.md line 18 under v1).
2. Tip check, landed v2: `python3 -I .../c3/count.py 4de4464` gives exit 1, `"count": 5`, all five tools. In scratch, after `git fetch -q <lane> master`, `python3 -I .ufo/waves/round-23/c3/count_v2.py 4de44647f93bfd25ed5c979f61ff016b50456549` gives count 5 (rc 1) and `count_v3.py` gives count 5 (rc 1). Landed v2 file sha256 `4828d7b87a76870f3c0fe4fced6d78df2ca0da44e8c0984d2818bec753ee6d6f`.
3. Drift check (read-only): `git diff --stat a28e4815 HEAD -- PROVINCE.md SHONEN.md tools/ .ufo/waves/round-23/c3/` changes only `c3/count.py` (+36/−9). PROVINCE.md has 20 lines and zero table rows at HEAD. Its history: `61eaa07` and `df84807` (both 2026-10-20, round 19), `74d3b7b` (2026-10-14, round 0).
4. Probe driver (scratch only): `python3 c3-attack-driver.py`. It commits 15 probe states on `revc3`, on top of 12 earlier matrix states, and measures v1, v2 and v3 at each rev with `python3 -I <script> <rev>`. Receipts: `/fast/scratch/hyaku/mado-r23/RevC3Counter/receipts/c3-attack-r23.json` (27 rows, sha256 `6863cf2842a69f00f9e3bbe9d95d5919c871a6e2dcb0b60b101c7990bf477980`). Proposal and driver: commit `af1ef0f7` on `revc3`, `.ufo/waves/round-23/c3/count_v3.py` sha256 `564198765c026ee638970d67f8de45d9a746cb9d84d5f8f44c3e888f956f9d26`.
5. Registration shell form, run as written against two revs:
   `git ls-tree --name-only $REV tools/ | grep -E '\.(py|sh)$' | while read f; do git show $REV:PROVINCE.md | grep -qF "$(basename "$f")" || echo "$f"; done | wc -l`
   At `a28e4815`: prints `4`, exit 0. At `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef`: prints `0`, exit 0, stderr `fatal: not a tree object`.
6. Host and tools: read-only probes only (`git`, `ls -l`, `sha256sum`). Python 3.14.8 (stdlib only), git 2.56.0. No installs, updates, network calls or pacman activity. Lane `git status` shows untracked files from other seats (`.ufo/waves/round-23/w1/`, `w1-*.json`); I did not touch them.

## 3. Findings, by severity

**F1, High (confidence high). Landed v2 reaches 0 with table rows that declare nothing.**
- Evidence: `T_neg` (4b78fb8) has denial cells such as "not declared in this province": v2 0, v3 5. `T_vacuous` (9d67fa0) has dash cells: v2 0, v3 5. `T_fence` (1828cad) has the honest table inside a fenced block: v2 0, v3 5. `T_comment` (17377ce) has it inside an HTML comment: v2 0, v3 5.
- Cause: v2 accepts any column-0 line starting with `|` whose first cell is a backticked `tools/` path and whose first four cells are non-empty (`all(row[:4])`). It never checks cell content, fences, comments or denial words.
- Impact: the refinement the registration asks for is a table, so this is exactly where a refinement could reach target 0 without declaring anything true.

**F2, High (confidence high). v2 does not observe what the claim is about.**
- Evidence: `T_bleed` (44146a8) has `tools/mado-bleed.py` writing `~/.config/hypr/x.conf` under a row that says "nothing": v2 0. `T_sibling` (7de9352) runs a sibling lane's script under a silent row: v2 0. `T_stale` (11bceac) names a deleted tool: v2 0. `T_negdup` (ce59f14) adds a denial row for a declared tool: v2 0.
- Cause: v2 reads tool names and PROVINCE rows, never tool source. Its five at base are five missing rows.
- Impact: "no cross-domain bleed" can be counted as satisfied (0) while a tool writes into a config tree.

**F3, High for the C3 refinement (facts high; the word "bleed" is medium). `mado-verify.sh` cannot honestly be described as "read-only, writes nothing".** Lane file `tools/mado-verify.sh` (identical at a28e4815):
- Header, lines 22-24: "no file is written; scratch lives under /tmp/w5-mado-m52-* and only --selftest makes it."
- Line 2251: `root=$(mktemp -d /tmp/mado-verify-regression.XXXXXX)` inside `run_regression`, reached through `--regression` (dispatch at lines 2330-2332 and 2370-2372). The header's usage block (lines 15-19) does not list `--regression`. The comment at lines 2420-2421 says usage stays silent on these modes.
- Line 2245: default harness `"${MADO_VERIFY_HARNESS:-$MADO_R7_FLEET/tameshi-shokunin/tools/mutate-and-run.sh}"`. `MADO_R7_FLEET` is derived from the gate's own location (line 2035). Line 2250 runs it as `REGRESSION_RUNNER`. The file exists on this host (`-rwxr-xr-x`, 102,681 bytes, mtime 2026-10-22 07:04). I did not read or run it.
- Usage text, lines 2344-2346: "No substrate read." Comment, lines 1938-1941: the harness is "consumed read-only", scratch is "only under /tmp/mado-verify-regression.*". That comment agrees with the code and contradicts the header.
- Assessment: the header is stale. The default live run is read-only as documented, and the cross-lane execution is opt-in via `--regression`. It is still a scratch write outside the documented root and an execution of another lane's script. Whether that is "bleed" depends on PROVINCE's "Out of province → report, never absorb"; that judgment belongs to L1 or the operator. v3 flags it (`scope:/tmp`, `sibling:tameshi-shokunin`); v2 does not.
- Required for any honest refinement: name the two `/tmp` roots, the `tameshi-shokunin` execution and the opt-in flag. A row saying "read-only, writes nothing" would be a false calibration that v2 accepts.

**F4, Medium (high). v2 population escapes.**
- Evidence: `T_population` (10e4c6b) adds `tools/mado-probe` (no extension), `tools/mado-helper.js`, and `tools/mádo-x.py` (non-ASCII; git prints it quoted, so the closing quote defeats `\.(py|sh)$`). v1 and v2 read 0; v3 reads 3.
- Lane convention: `SCORECARD.md:1082` counts owned files as `tools/*`, any extension.

**F5, Medium (high). v2 gives a false mismatch for a tool name with a space.**
- Evidence: `T_space-name` (adee115) declares `tools/mado probe.py` honestly. v2 exits 1 with mismatch `probe.py`, because `ls-tree` output is split on whitespace. v3 reads 0. Latent at base (no such file).

**F6, Medium (high). The abstention path is unbound, and v2 abstains on several box edits.**
- Evidence: reworded box `G3a` (a2a9b44), duplicated box `G3c` (5480f97), deleted box `T_box-removed` (83a4b1a): v2 exit 2, `count` absent. `[X]` in `G3b` (7d4c8ea): v2 exit 2; v3 accepts it as asserted. Unticked box `T_box-unticked` (7e692bf): v2 exit 2.
- Risk: the registration binds only "target 0". A reader that defaults a missing count to 0 turns a reworded box into a pass. I could not inspect the harness that reads this number, so this risk is conditional.

**F7, Medium-high (high). The registration's shell form is a silent-pass hazard.**
- Evidence: section 2, command 5. A mistyped rev prints `0` with exit 0. The pipeline's exit code is `wc`'s, so a git failure becomes an empty list. The form also matches by substring, so it carries the v1 collision. The registration says the shell form "stays as recorded; the script is the counter of record." The record needs a non-authoritative note, appended, not an edit.

**F8, Medium (high). v1 holes, historical but relevant to the before record.**
- Prose "not" sentence `G1a` (ac80636), one-line HTML comment `G1c` (eec05a5) and bullet denials `G1b` (9ae6633): v1 reads 0.
- Substring collision `G2` (f1a07e7): adding an undeclared `tools/plan.py` drops v1 from 4 to 3, because it is a substring of `mado-action-plan.py`.
- Unticked box `T_box-unticked`: v1 exits 0 with count 0 on a box that asserts nothing.
- Git failure `C4` (20e96e0): v1 exits 1 with count null, which looks like a mismatch.
- Honest bullet inventory `C5` (b2ded23) with no `/tmp` and no sibling: v1 reads 0, a false pass.

**F9, Medium-low (medium). Counting unit.** Under v3, counting per tool gives 5 at base. Counting per (tool, reason) gives 7: five undeclared, plus `scope:/tmp` and `sibling:tameshi-shokunin` on `mado-verify.sh`. Per tool hides observed-scope findings behind an undeclared tool, so I recommend per reason. This moves the before value, so it needs an append-only clarification before any after-measurement. L1's call.

**F10, Low (medium). Box 4's evidence predates the current PROVINCE.** `SHONEN.md:12` cites `corpus/knowledge/province-accuracy-selfaudit.md` (round-5 receipt, VER-M4B). That file is dated 2026-10-14, while PROVINCE.md changed on 2026-10-20. Neither counter reads the evidence pointer, so "PROVINCE.md still accurate" is asserted, not checked. A refinement should cite a current receipt.

**What v2 does right (verified, high).** Prose-only mentions (`G1a`), a one-line HTML comment (`G1c`) and bullet denials (`G1b`) do not count. Exact path equality closes the substring collision (`G2` goes to 6). Git failure exits 2 (`C4`). Box rewording, duplication and deletion abstain. `ls-tree -r` recursion is by code reading only; I did not probe it.

## 4. v1 holes closed by v2, and holes that remain (L1 request)

**Closed by v2 (verified at 4de44647 probes):** prose negation (`G1a`), one-line HTML comment (`G1c`), bullet denials (`G1b`), substring collision (`G2`), unticked box (`T_box-unticked`, now exit 2), git failure (`C4`, now exit 2).

**Changed, not closed:** honest bullet inventory (`C5`): v1 read 0 (false pass), v2 reads 5 because it rejects bullets. Honest declarations in bullet form now fail closed.

**Remaining under v2 (each reproduced):** denial cells (`T_neg`), placeholder cells (`T_vacuous`), tables in fences (`T_fence`) or HTML comments (`T_comment`), extensionless or non-ASCII names (`T_population`), stale rows (`T_stale`), duplicate denial rows (`T_negdup`), a declared config writer (`T_bleed`), a declared sibling execution (`T_sibling`), the verify gate's `/tmp` scope (`T_scope-gap`), a false mismatch on a spaced name (`T_space-name`), and the shell form's exit 0 on bad revs (F7).

## 5. Stricter check v3: what it checks, base result, blind spots

`python3 -I .ufo/waves/round-23/c3/count_v3.py REV` (scratch commit `af1ef0f7`). Reads committed bytes only (`git show`, `git ls-tree -z`). Rules:
1. **Box.** Exactly one SHONEN.md line at REV contains "PROVINCE.md still accurate" and it is ticked (`[~]`, `[x]` or `[X]`). Otherwise exit 2, `"count": null`.
2. **Population.** Every tracked entry under `tools/`, any extension, nested, any name bytes.
3. **Declaration.** A PROVINCE.md list item or table row, outside fences and HTML comments, whose first backticked token is the exact `tools/<path>`. A table row needs four non-placeholder cells (placeholders: empty, `-`, `—`, `n/a`, `tbd`, `todo`, `?`, `x`). A list item needs at least four alphabetic words after the token. Denial phrases ("not declared", "undeclared", "absent from" and similar) mark a row negated and mismatch the tool.
4. **Stale.** A declaration whose `tools/` path is not tracked at REV is one mismatch.
5. **Observed scope** (committed source; `#` comment lines skipped; `/dev/null` redirects ignored). For each write- or exec-capable line (write-mode `open`, `write_text`, `os.mkdir`/`remove`/…, `shutil`, `mkdtemp`, `TemporaryDirectory`, `subprocess`, or `mkdir`/`cp`/`mv`/`rm`/`ln`/`chmod`/`tee`/`touch`/`bash`/`sh` at command position, or a redirect):
   a. a home- or config-rooted target (`~/`, `$HOME`, `${HOME}`, `/home/`, `.config/`, `.local/`) is **bleed**; no row excuses it; shell single-quoted payloads are not examined for this;
   b. an absolute literal root (for example `/tmp`; `/dev`, `/bin`, `/usr` exempt) must be named by a valid row, else `scope:<root>`;
   c. any non-comment line naming `<x>-shokunin/` (except `mado-shokunin`) must be named by a valid row, else `sibling:<x>`.
6. **Count** = tools with any reason + stale declarations. Exit 0 at zero, 1 above zero, 2 cannot evaluate.

Base result (`a28e4815`, and tip `4de44647` identically): count 5, exit 1. All five tools are undeclared. `mado-verify.sh` also has `scope:/tmp` and `sibling:tameshi-shokunin`. No base tool has a bleed line: the config-tree reads in `mado-tripwire.py` and the `$R` fixture writes in `mado-verify.sh` are correctly not flagged.

Positive control (`T_honest`, 8805a04): five honest table rows, written by me from grep evidence (write call sites and subprocess call sites checked; the tools were not run), with the verify row naming `/tmp` and the harness. Result: count 0, exit 0. These rows are my text, not the lane's, and a refinement needs a non-author check. `_self_invoke` in action-plan is called only inside `run_selftest` (lines 741 and 845); assessment and evidence-audit spawn only inside `selftest`; tripwire spawns only inside `run_selftest`.

Blind spots, stated: (i) variable-built config writes (`T_indirect`, e77bbd4: home built on another line, count 0); (ii) variable-indirected execution such as `"$REGRESSION_RUNNER"`; (iii) verbs outside the list (`sqlite3`, `zipfile` write modes, `tar -x`, `sed -i`, git and jj writes); (iv) sibling names that do not match `-shokunin/`; (v) whether row prose is true; (vi) SCORECARD, which v3 does not read. SHONEN is the only current self-assessment surface: SCORECARD's claim rows are dated history. (vii) Header and comment claims, such as F3's header contradiction. No counter here sees these; a verifier must.

Development note: three false-positive classes in the first scanner draft (single-quoted fixture payloads, a D-Bus object path after `2>/dev/null`, and prose "bash" in a docstring), plus one truncation bug that made honest declarations look undeclared, were all fixed against base before the final run. Base agreement is therefore partly by construction, and I rate the scanner medium confidence.

## 6. Probe matrix (27 committed states; counts with exit codes)

| State | Rev | v1 | v2 | v3 | Note |
|---|---|---|---|---|---|
| base (pin) | a28e4815 | rc1 4 | rc1 5 | rc1 5 | v1 reproduces 4 |
| M0 base content | fce9989 | rc1 4 | rc1 5 | rc1 5 | same content, scratch commit |
| G1a prose "not" | ac80636 | rc0 0 | rc1 5 | rc1 5 | v1 gamed |
| G1c one-line HTML comment | eec05a5 | rc0 0 | rc1 5 | rc1 5 | v1 gamed |
| G1b bullet denials | 9ae6633 | rc0 0 | rc1 5 | rc1 5 | v1 gamed |
| G2 substring collision | f1a07e7 | rc1 3 | rc1 6 | rc1 5 | v1 drops on an undeclared tool |
| G3a box reworded | a2a9b44 | rc2 | rc2 | rc2 | abstains |
| G3b box `[X]` | 7d4c8ea | rc2 | rc2 | rc1 5 | v3 accepts uppercase |
| G3c box duplicated | 5480f97 | rc2 | rc2 | rc2 | abstains |
| C4 PROVINCE absent | 20e96e0 | rc1 null | rc2 | rc2 | v1 exits 1 on git failure |
| C5 honest bullets, no /tmp | b2ded23 | rc0 0 | rc1 5 | rc1 1 | v1 false pass; v3 names both gaps |
| C6 bullets + negated dup | ce62727 | rc0 0 | rc1 5 | rc1 2 | v3 catches the denial |
| T_honest (positive control) | 8805a04 | rc0 0 | rc0 0 | rc0 0 | honest table passes everywhere |
| T_neg denial cells | 4b78fb8 | rc0 0 | rc0 0 | rc1 5 | v2 gamed |
| T_fence table in fence | 1828cad | rc0 0 | rc0 0 | rc1 5 | v2 gamed |
| T_comment table in HTML comment | 17377ce | rc0 0 | rc0 0 | rc1 5 | v2 gamed |
| T_vacuous dash cells | 9d67fa0 | rc0 0 | rc0 0 | rc1 5 | v2 gamed |
| T_scope-gap verify row omits /tmp | c95e72f | rc0 0 | rc0 0 | rc1 1 | v2 blind to scope |
| T_population no-ext, .js, non-ASCII | 10e4c6b | rc0 0 | rc0 0 | rc1 3 | v1 and v2 escape |
| T_space-name declared | adee115 | rc0 0 | rc1 1 (false) | rc0 0 | v2 false mismatch |
| T_stale row for deleted tool | 11bceac | rc0 0 | rc0 0 | rc1 1 | v2 blind |
| T_bleed declared "nothing", writes ~/.config | 44146a8 | rc0 0 | rc0 0 | rc1 1 | v2 blind; v3 flags bleed |
| T_indirect home built on another line | e77bbd4 | rc0 0 | rc0 0 | rc0 0 | v3 blind spot |
| T_sibling declared, runs sibling lane | 7de9352 | rc0 0 | rc0 0 | rc1 1 | v2 blind |
| T_negdup denial duplicate | ce59f14 | rc0 0 | rc0 0 | rc1 1 | v2 blind |
| T_box-unticked `- [ ]` | 7e692bf | rc0 0 | rc2 | rc2 | v1 passes an unasserted box |
| T_box-removed | 83a4b1a | rc2 | rc2 | rc2 | abstains |

Shell form (section 2, command 5): base `4` exit 0; bad rev `0` exit 0.

## 7. Residual risk and verification gaps

1. The v3 scanner was tested on five base tools and 27 states, not on the whole lane. Verb and root lists are hand-picked; there may be false positives or negatives elsewhere.
2. No counter checks whether a row's prose is true. The refinement needs a non-author check against the code, as box 4's own note already requires.
3. I did not run any `tools/` script (outside bounds), the repair or oracle guards, or the corpus comparator. Those are L1's gates.
4. The harness that consumes C3's number was not available; F6's risk is conditional on it.
5. Not tested: symlinks, submodules, CRLF, indented table rows (v2 requires column-0 pipes), escaped pipes, and `ls-tree -r` recursion. The sibling harness was not opened, only checked for existence and mode.
6. The shell form was tested at two revs only.
7. F3's bleed label depends on how PROVINCE's "report, never absorb" is read. The facts are high confidence; the classification is medium.
8. Counts were run once per rev. Output is deterministic (no time or randomness in either counter), so this is sufficient for those revs.

## 8. Changes and receipts

- Lane: only this report was written. No lane file, no git index, no jj state, no push.
- Scratch clone (not the lane): probe states on `revc3`; kit commit `af1ef0f7`; receipts `receipts/c3-attack-r23.json`; driver `c3-attack-driver.py`; proposal `.ufo/waves/round-23/c3/count_v3.py`.
- Installs or updates: none.

**Verdict line: the C3 counter is gameable (v1 and landed v2), and it does not measure observed bleed. The stricter v3 is proposed and tested, not landed, with one stated blind spot. Before any after-measurement: bind pass to exit 0 and count 0, stop using the shell form, put the `mado-verify.sh` scope facts from F3 into any refinement, and choose the counting unit.**
