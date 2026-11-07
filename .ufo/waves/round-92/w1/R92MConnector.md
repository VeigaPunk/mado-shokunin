# R92MConnector — sibling overlap, assimilation, considerthese, and cross-claim synthesis (mado round 92, w1)

Seat: `R92MConnector` (connector). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round 92, ONE v1 wave `w1`, base `d992ef7494b054591ee9104df1da49264678df5d` (master).
Scratch root: `S=/fast/scratch/hyaku/mado-r92/R92MConnector` (used and removed on exit).
No pacman transactions, no background processes kept, no mutating git/jj commands anywhere.
All draft executions are labelled **DRAFT**; no measurement receipts were written.

**Axes named:**
- **C1 coverage capability:** read-only emulation of `xdg-mime query default TYPE` (xdg-utils 1.2.1 `defapp_generic` resolver on Hyprland/unknown desktops).
- **C2 operability:** seat-report retention gate (`quality/check-seat-reports.py`) addressing residual defects F1–F5.

---

## 1. Sibling-overlap scan — no sibling owns the xdg-open / xdg-mime plane

A read-only scan of all sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `mado-shokunin`) was conducted for the six target tokens:

| Token | Hits in sibling lanes (`path:line`) | Interpretation | Owns the plane? |
|---|---|---|---|
| `defapp_generic` | *none* (0 matches across all sibling lanes) | Exclusive to mado round 92 | **no** |
| `desktop_file_to_binary` | *none* (0 matches across all sibling lanes) | Exclusive to mado round 92 | **no** |
| `xdg-mime` | *none* (0 matches across all sibling lanes) | Exclusive to mado round 92 | **no** |
| `xdg-open` | `souji-shokunin/census/round-6/seat-07.json:99`<br>`kotoba-shokunin/.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:35588`<br>`kotoba-shokunin/waves/round-82/build/Kb82E12Loader-omp-18.14.0-strings.txt:37869` | `souji` hit is an execution prohibition rule ("Never exec or signal obsidian, electron, xdg-open, gio..."); `kotoba` hits are raw binary string captures of external OMP binaries. | **no** |
| `mimeapps.list` | `souji-shokunin/.ufo/waves/round-22/attempt2/w1/evidence/snap-gio1.raw:407`<br>`souji-shokunin/.ufo/waves/round-22/attempt2/w1/evidence/snap-gio1.txt:156`<br>`souji-shokunin/.ufo/waves/round-22/attempt2/w1/evidence/CritC2Counter/arch-gio.1.html:407`<br>`souji-shokunin/census/round-22/attempt2/sources/arch-gio.1.raw:407`<br>`souji-shokunin/census/round-22/attempt2/sources/arch-gio.1.txt:424` | All five hits in `souji` are static captures of the upstream `gio(1)` man page text mentioning `$XDG_DATA_HOME/applications/mimeapps.list`. | **no** |
| `seat-report gates` | `kama-shokunin/tools/seat-report-immutability.py:21-22`<br>`kama-shokunin/tools/pre-report-gate.py`<br>`kama-shokunin/tools/report-landing-audit.py`<br>`souji-shokunin/tools/souji-pre-report-gate.sh`<br>`souji-shokunin/tools/souji-report-contract.py`<br>`kotoba-shokunin/verifiers/check_report_pointers.py`<br>`tsukuroi-shokunin/tools/check-report-receipts.py`<br>`tsukuroi-shokunin/tools/report-red-causes.py` | Sibling lanes maintain their own seat-report integrity checkers for their private layouts; none read, import, or gate `mado-shokunin`'s `.ufo/waves/` layout or `quality/check-seat-reports.py`. | **no** |

### Province ownership check (`PROVINCE.md`)
- **Sibling lanes:** Grep across all `*-shokunin/PROVINCE.md` files for `xdg-open`, `xdg-mime`, `defapp`, and `mime` yielded zero matches outside `mado-shokunin`. No sibling lane claims or touches default applications or `xdg-open`.
- **Mado lane:** In `mado-shokunin/PROVINCE.md:504-514` (round 91 refinement), mado explicitly owns the default-application plane:
  > "The question 'which .desktop application opens this MIME type or URI scheme' (xdg-open, file managers and OpenURI reduce to GLib's g_app_info_get_default_for_type) is in province: it is desktop behavior configured by Omarchy's `~/.config/mimeapps.list` and `~/.config/<desktop>-mimeapps.list`."
- **Contract contradiction identified:** `PROVINCE.md:505` claimed that `xdg-open` reduces to GLib's `g_app_info_get_default_for_type`. On Hyprland / wlroots compositors, `xdg-open` falls back to `open_generic_xdg_mime`, querying `xdg-mime query default TYPE` (`defapp_generic`), which produces divergent answers from GLib in 69 of 128 draft cases (glib agreement only 59/128). Round 92 properly retains ownership of both resolvers within mado, but requires a PROVINCE refinement acknowledging `mado-xdgmime.py`.

---

## 2. Assimilation — shokuknow merge review & ID collision check

A read-only inspection of `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md` and `SOURCES.append.md` was conducted:
- **Content scan:** Neither file contains any staged entry regarding `xdg-utils`, `xdg-open`, `xdg-mime`, `defapp_generic`, or desktop MIME associations. Staged rows cover rounds 1–16 (Hyprland IPC, idle-lock daemon, Waybar custom producers, focus-grab protocols, and bilingual ArchWiki documentation).
- **ID collision check:** Executed in `$S` using the canonical round prompt pattern `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort -u`:
  * `reg-ids`: **442** unique IDs (`S001`–`S507`, with 65 gaps; sha256 `f9252e9efeb00570dfe6d186642cbf394e3d7d45bc42f588399d21e0bde18038`).
  * `staged-ids`: **147** unique IDs (`S203`–`S349`; sha256 `079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d`).
  * `collisions`: **94** exact ID collisions (`comm -12`; sha256 `18e1d089c96fd5f43af25a6a1c656cc296d5048192f08f1ffd6cc45ba5f82a5c`).
  * `gap-collisions`: The remaining **53** staged IDs (`S222`–`S252`, `S254`–`S257`, `S259`–`S276`) fall into historical gaps below the current registry maximum `S507`.
- **Recommendation: REJECT (do not admit).**
  * *Reason 1 (Collision severity):* 94 direct collisions with active registry entries; admitting would corrupt or overwrite verified knowledge citations.
  * *Reason 2 (Below-max insertion):* The 53 non-colliding staged rows violate append-only integrity by backfilling below the maximum ID (`S507`). Safe allocation requires starting above `S509`.
  * *Reason 3 (Relevance):* The package has zero overlap with Round 92 claims (C1 citations for xdg-utils 1.2.1 are freshly sourced in rows S508–S509).

---

## 3. considerthese — reflection alignment

Analysis of `considerthese/2026-11-06.md` (the latest reflection at tip `1ee8b669`):

| Proposal | Description | Status in Round 92 |
|---|---|---|
| **P4** | "Widen desktop coverage past bar + mako ... Prefer one operator-config gap over another harness counter." | **Directly served by C1:** C1 models `xdg-open`'s shell resolver (`defapp_generic`) on Hyprland, closing an active desktop configuration gap where `xdg-open` diverges from GLib. |
| **P1** | "Carry a survivor ledger across quiet days" (tracking r87 mako mutants M03/M05/M06/M08/M10 and r86 forgeries). | **STAYS OPEN:** Round 92 C1 mutant battery addresses xdg-mime; it does not track or kill the carried mako survivors. |
| **P2** | "Always quote verdict before score" (`score_scope=finite-cases` on finite case sets). | **STAYS OPEN:** C1 and C2 counters output standard `DRAFT_TARGET_MET` / `TARGET_MET` without `score_scope`. |
| **P3** | "Read-only live check of `mado-mako.py` against João's real theme files." | **STAYS OPEN:** Untouched; mako plane is not under review in round 92. |
| **P5** | "Verify QUALITY 145 has an instrument, not only a criterion" (gating on wave-done / null-seat). | **STAYS OPEN:** C2 repairs seat-report retention defects F1–F5 in `quality/check-seat-reports.py`, but explicitly excludes F6 (`counts.total` vs tasks) as a new rule. |
| **P6** | "Keep fetching LOG/SCORECARD by round header, not whole file." | **STAYS OPEN:** Ongoing operational discipline. |
| **P7** | "Ask João (via parent) for a decision on the tracked `eventq-live-ss.txt` receipts." | **STAYS OPEN:** Historical receipt artifacts remain tracked. |

---

## 4. Cross-claim pattern: GLib resolver (`mado-mime.py`) vs xdg-mime (`mado-xdgmime.py`)

Round 91 introduced `tools/mado-mime.py` (modeling GLib 2.90.1 `g_app_info_get_default_for_type`), while Round 92 introduces `tools/mado-xdgmime.py` (modeling xdg-utils 1.2.1 `defapp_generic`). Because both tools operate on the desktop default-application plane, operators and agents must know which tool to consult:

### Divergence evidence (DRAFT run)
On the 128 frozen cases of Round 92, the GLib resolver agrees with `xdg-mime` on only **59 cases (46.1%)**, failing on 69 cases (`glib_resolver_correct=59`):
1. **Hierarchy traversal:** `defapp_generic` stops at the first `[Default Applications]` file containing `TYPE=` and tries its semicolon-separated list in order. If none resolve, it does *not* fall back to lower files in the hierarchy. GLib merges all `mimeapps.list` files down the XDG stack.
2. **Added/Removed associations:** `defapp_generic` ignores `[Removed Associations]` and `[Added Associations]` completely. GLib applies blocklists across all hierarchy levels.
3. **Binary resolution (`desktop_file_to_binary`):** `xdg-mime` resolves `Exec=` lines via shell `command -v` and `xdg_realpath` (`[ -e "$command" ]`). Shell builtins and keywords (e.g., `Exec=true`) resolve relative to `$PWD` rather than PATH. GLib resolves executables strictly on PATH and handles KeyFile escapes.
4. **Fallback mechanism:** `xdg-mime` falls back to unanchored BRE greps in `defaults.list` and `mimeinfo.cache`, followed by an `InitialPreference` scan across `.desktop` files. GLib uses `subclasses`, `aliases`, and `mimeinfo.cache` additions.

### Operator decision rules for `SKILL.md`
- **Use `tools/mado-mime.py`:** When inquiring what GUI file managers (Nautilus, Thunar), GTK/Adwaita applications, or Flatpak portals (`org.freedesktop.portal.OpenURI`) will launch.
- **Use `tools/mado-xdgmime.py`:** When inquiring what terminal commands, shell scripts, CLI applications, or Electron/browser subprocesses calling `/usr/bin/xdg-open` will launch on a Hyprland session.
- **Diagnostic divergence pattern:** When an application launched from the terminal via `xdg-open` differs from one launched by double-clicking in a file manager, run both tools in tandem to isolate whether the divergence stems from `defapp_generic`'s first-file cutoff, lack of `[Removed Associations]` filtering, or `InitialPreference` fallback.

---

## 5. Proposed move — non-obvious synthesis (UFO-FSD connector)

**Move: Equip `tools/mado-xdgmime.py` with an in-memory hermetic `--selftest` and update `PROVINCE.md:504-514` to formalize the dual-resolver plane before the L1 freeze commit.**

### Evidence
1. **Tool-contract deficiency:** In `build/mado-xdgmime.c1.py`, calling `--selftest` fails with `exit code 2` (`error: the following arguments are required: types`). Unlike every other analysis tool in `tools/` (`mado-mime.py`, `mado-mako.py`, `mado-portals.py`, `mado-action-plan.py`, `check-seat-reports.py`), `mado-xdgmime.py` lacks a self-contained `--selftest` option.
2. **Prompt and PROVINCE mandate:** The round prompt explicitly states: *"run the candidates' --selftest"*. Furthermore, `PROVINCE.md:20` mandates that tracked analysis tools provide a `--selftest` that writes ephemeral fixtures inside a temporary directory and runs a child copy of itself, exiting 0.
3. **Contract contradiction:** `PROVINCE.md:505` currently asserts that `xdg-open` reduces to GLib's resolver. This is false on Hyprland.
4. **DRAFT counter safety:** The C1 counter (`quality/counters/c1-r92-xdgmime-default.py`) executes `mado-xdgmime.py` with explicit positional `types` and optional `--env`/`--cwd`/`--json`; it does not pass `--selftest`.

### Affected axes
- **C1 coverage capability:** **IMPROVES.** Providing `--selftest` brings `mado-xdgmime.py` into full compliance with the lane's tool contract, enables fast local verification (under 0.1s wall time vs 74s full counter run), and allows automated verifiers (`check-tool-ledger.py`) to gate the tool safely.
- **C2 operability:** **NO HARM / UNCHANGED.** `quality/check-seat-reports.py` and its battery are untouched.

### Implementation details (for L1 MadoR92 at freeze)
1. In `mado-xdgmime.c1.py`:
   - Change `ap.add_argument("types", nargs="+")` to `ap.add_argument("types", nargs="*")`.
   - Add `ap.add_argument("--selftest", action="store_true", help="run in-memory hermetic self-tests")`.
   - Implement `selftest()` checking 10 core assertions in a temporary directory:
     * User `mimeapps.list` resolution;
     * First-file cutoff overriding lower data dir;
     * Unanchored BRE fallback in `mimeinfo.cache`;
     * `InitialPreference` sorting;
     * Unsupported environment variable refusals.
   - Print `MADO_XDGMIME_SELFTEST: checks=10 failed=0` and exit 0.
2. In `PROVINCE.md`:
   - Add round-92 refinement block declaring `tools/mado-xdgmime.py` and noting that on Hyprland `xdg-open` resolves through `defapp_generic` rather than GLib.

### Risks and mitigations
- *Argument parsing risk:* If positional `types` is made optional, a call without types and without `--selftest` must print usage and exit 2.
- *Hash invalidation:* Adding `--selftest` changes the candidate's sha256; must be incorporated before L1 freezes `EXPECT_CASES_SHA256` and candidate pins.

### Verification (DRAFT results)
- C1 draft counter run on candidate (`bg_4700`):
  `MADO_XDGMIME_DEFAULT: DRAFT_TARGET_MET pred=PRED-C1-r92-v1 cases=128 correct=128 b=16/16 d=39/39 f=21/21 g=6/6 m=36/36 s=10/10 fresh=10/10 mutants=39 killed=39 oracle_agree=128/128 do_nothing_correct=33 naive_mimeapps_correct=44 glib_resolver_correct=59 rc=3 (73.87s wall)`
- C2 draft counter run on candidate (`bg_4787`):
  `MADO_GATE_DEFECTS: DRAFT_TARGET_MET pred=PRED-C2-r92-v1 fixtures=28 met=28 F1=5/5 F2=5/5 F3=3/3 F4=3/3 F5=4/4 P=8/8 selftest=ok:SEAT_REPORTS_SELFTEST: checks=23 failed=0 mutants=14 killed=14 r91_counter=TARGET_MET rc=3 (228.96s wall)`
- Candidate C2 `--selftest`: `SEAT_REPORTS_SELFTEST: checks=23 failed=0` (rc 0).
