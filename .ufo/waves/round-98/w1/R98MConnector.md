# R98MConnector — UFO-FSD Connector Report (Round mado 98, Wave w1)

**Seat**: `R98MConnector`  
**Role**: UFO-FSD connector / leaf member  
**Report target**: `.ufo/waves/round-98/w1/R98MConnector.md`  
**Receipt target**: `.ufo/waves/round-98/receipts/connector-sweep-r98.txt`  
**Lane root**: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base revision**: `35f3ce808788b11c063309b1b5ad0192754795ea` (`master`)  
**Declared axes**:
- **C1 `coverage`** (capability): The launch argv GIO 2.90.1 builds from a desktop entry's `Exec` key and argument list (`tools/mado-execargv.py` modeling `expand_application_parameters` in `gio/gdesktopappinfo.c:2700-2750` and `g_shell_parse_argv` in `glib/gshell.c`).
- **C2 `operability`** (gate & repair): The `corpus/SOURCES.md` registry citation read-back (`quality/check-sources-readback.py`), verifying bidirectional consistency between registry `used-by` cells and `corpus/knowledge/*.md` `source:` frontmatter lines, plus the 23-cell repair.

---

## 1. Sibling-Overlap Scan (Adjacency Axis, Read-Only)

We conducted an exhaustive sweep of all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (read-only). For each lane, we inspected `PROVINCE.md` and searched all entries in `corpus/knowledge/*.md` for the C1 and C2 surfaces:
- **C1 Surface**: `Exec` field codes (`%f`, `%F`, `%u`, `%U`, `%d`, `%D`, `%n`, `%N`, `%i`, `%c`, `%k`), `g_shell_parse_argv`, desktop-entry launch, `gio launch`.
- **C2 Surface**: `SOURCES.md` read-back, registry citation consistency, `used-by` cells.

### 1.1 Sibling Sweep Findings Per Lane

1. **`audio-shokunin`** (`audio-shokunin/PROVINCE.md:1-55`):
   - **C1 Surface**: **SILENT**. PROVINCE owns game audio production (SFX, ambience, soundtrack loops/stems; `PROVINCE.md:2-5`); 0 hits in `corpus/knowledge/`.
   - **C2 Surface**: **SILENT**. PROVINCE has standard read-only SOURCES citation; 0 read-back/citation gate tools in `corpus/knowledge/`.

2. **`chousa-shokunin`** (`chousa-shokunin/PROVINCE.md:1-12`):
   - **C1 Surface**: **SILENT**. PROVINCE owns deep-research method (question framing, source hierarchy, claim-vs-source verification; `PROVINCE.md:3-6`); 0 hits in `corpus/knowledge/`.
   - **C2 Surface**: **ADJACENT (Research Method Only)**. PROVINCE line 6 claims *"citation chaining and hop resolution; claim-vs-source verification"*; `corpus/knowledge/aggregator-vs-source-r36.md:10`, `citation-chain-fidelity-r24.md:42`, `citation-searching-tarcis-r81.md:9` explore citation verification methodology. Chousa owns the intellectual research method, not the repository gate or automated `used-by` cell read-back.

3. **`game-dev-2d-shokunin`** (`game-dev-2d-shokunin/PROVINCE.md:1-40`):
   - **C1 Surface**: **ADJACENT (Engine Binary Export/Launch)**. PROVINCE lines 18 and 23 mention *"export/launch"*, strictly in the context of headless Godot/Unity 2D engine test loops; 0 hits in `corpus/knowledge/` for desktop entries, field codes, or GIO.
   - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 gate claims.

4. **`game-dev-3d-shokunin`** (`game-dev-3d-shokunin/PROVINCE.md:1-85`):
   - **C1 Surface**: **ADJACENT (Explicit Deferral to mado)**. PROVINCE line 75 explicitly declares:
     > *"Desktop/compositor display behavior belongs to `mado-shokunin` (`../mado-shokunin/PROVINCE.md:3-12`)."*
     PROVINCE lines 14, 19, 40 mention headless engine execution (Godot 4.7.2 headless, Blender bpy); 0 hits in `corpus/knowledge/` for desktop entry Exec grammar.
   - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 gate claims.

5. **`kagi-shokunin`** (`kagi-shokunin/PROVINCE.md:1-120`):
   - **C1 Surface**: **SILENT**. Token hits for `%F` in `corpus/knowledge/handler-on-disk-state.md:264`, `handler-trust-boundary.md:304`, `surface-census.md:46` are coreutils `stat -c '%F %a %s'` (file type string), not desktop entry field codes; 0 GIO/desktop launch mentions.
   - **C2 Surface**: **ADJACENT (Lane-Local Instrument)**. PROVINCE line 78 claims `- corpus/sources-census.sh — source-registry gate (round 21): the SOURCES-CONTRACT-v1 census over corpus/SOURCES.md`. This is a lane-local shell script verifying kagi's own registry against SOURCES-CONTRACT-v1 awk one-liners; it does not claim fleet-wide read-back or mado's surface.

6. **`kaidoku-shokunin`** (`kaidoku-shokunin/PROVINCE.md:1-600`):
   - **C1 Surface**: **ADJACENT (Reverse-Engineering Forensic Observation)**. In `corpus/knowledge/2026-10-13-r4-15-appimage-inner.md:16`, kaidoku records an observation of an unpacked AppImage's desktop entry:
     `| 3 | cat grok-bot.desktop / head AppRun | Name=Grok Bot, Exec=AppRun --no-sandbox %U, X-AppImage-Version=0.68.`
     Other hits are `sysctl kernel.core_pattern` `%F` (`2026-10-13-crash-evidence.md:9`) and `stat -c '%y %U'` (`2026-10-13-r2-jq-shadow-verdict.md:177`). Kaidoku reverses shipped artifacts; it does not model the desktop launch argv parser or GIO macro expansion.
   - **C2 Surface**: **ADJACENT (Lane-Local Record Audit)**. PROVINCE line 577 notes `tools/round-75/record-audit.py` parsing used-by path grammars for kaidoku's own records; 0 fleet or mado read-back claims.

7. **`kake-shokunin`** (`kake-shokunin/PROVINCE.md:1-730`):
   - **C1 Surface**: **SILENT**. Web properties and publishing; 0 desktop entry or GIO hits.
   - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 gate claims.

8. **`kama-shokunin`** (`kama-shokunin/PROVINCE.md:1-350`):
   - **C1 Surface**: **SILENT**. Local model serving endpoints; 0 desktop entry or GIO hits.
   - **C2 Surface**: **SILENT**. Standard SOURCES usage (`error-is-not-a-verdict.md:168`, `receipt-tip-binding.md:1`); 0 gate claims.

9. **`kasegi-shokunin`** (`kasegi-shokunin/PROVINCE.md:1-300`):
   - **C1 Surface**: **SILENT**. Bounty research and JavaScript engine fuzzer architecture; 0 desktop entry or GIO hits.
   - **C2 Surface**: **SILENT**. Standard SOURCES usage (`cloud-signed-cookies-and-user-bound-sas.md:9,285`, `github-prefixed-tokens-in-captured-evidence.md:3,9,297`); 0 gate claims.

10. **`kengaku-shokunin`** (`kengaku-shokunin/PROVINCE.md:1-990`):
    - **C1 Surface**: **SILENT**. LLM evaluation and benchmark harness execution; 0 desktop entry or GIO hits.
    - **C2 Surface**: **ADJACENT (Adoption Checker)**. PROVINCE line 248 mentions `plans/adoption_check.py` with `used-by` projection for benchmark tasks; 0 fleet or mado read-back gate claims.

11. **`kotoba-shokunin`** (`kotoba-shokunin/PROVINCE.md:1-40`):
    - **C1 Surface**: **SILENT**. Prompt and skill craft; 0 desktop entry or GIO hits.
    - **C2 Surface**: **SILENT**. Standard SOURCES citations; `mutation-battery-arms-round91.md:48` mentions test copy read-back, unrelated to registry.

12. **`kotodama-shokunin`** (`kotodama-shokunin/PROVINCE.md:1-30`):
    - **C1 Surface**: **SILENT**. Linguistic-cultural worldbuilding; 0 hits.
    - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 hits.

13. **`kumitate-shokunin`** (`kumitate-shokunin/PROVINCE.md:1-40`):
    - **C1 Surface**: **SILENT**. Orchestration and tooling; hits in `corpus/knowledge/` are `stat -c '%F ...'` (`kimi-mcp-plane.md:26`, `kimi-skills-plugins.md:211,225`) and `find ... -printf '%f\n'` (`sighting-wall.md:78`), not desktop entry field codes.
    - **C2 Surface**: **ADJACENT (Lane-Local Gate Ownership)**. PROVINCE line 15 claims `scripts/*.mjs` and `corpus/SOURCES.md`. Kumitate owns `scripts/sources-check.mjs` (contract `kumitate-sources-v1`), which validates kumitate's own source registry and `corpus/knowledge/*.md` citations (E01–E12, W02/W03). It does not validate mado's registry or provide the Python read-back gate.

14. **`lore-shokunin`** (`lore-shokunin/PROVINCE.md:1-30`):
    - **C1 Surface**: **SILENT**. Fictional-world records; 0 hits.
    - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 hits.

15. **`mori-shokunin`** (`mori-shokunin/PROVINCE.md:1-700`):
    - **C1 Surface**: **SILENT**. Observability and watchdog monitoring; hits in `oom-memcg-stat-r50.md:40` and `kernel-v7.3-recheck-r54.md:49` are kernel `pr_err` printk format specifiers (`%s`, `%d`), not desktop entries.
    - **C2 Surface**: **SILENT**. Standard SOURCES usage (`entry-claims-hardening-r60.md:23`, `journal-alarm-routing-r14.md:347`); 0 read-back gate claims.

16. **`revenger-shokunin`** (`revenger-shokunin/PROVINCE.md:1-60`):
    - **C1 Surface**: **SILENT**. Binary reverse engineering; token hits in `utf16-unpaired-surrogates-in-resource-names.md:20,151` are Python string format `%04X` for surrogate pairs.
    - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 gate claims.

17. **`souji-shokunin`** (`souji-shokunin/PROVINCE.md:1-330`):
    - **C1 Surface**: **SILENT**. Repository hygiene and artifact cleanup; 0 hits.
    - **C2 Surface**: **ADJACENT (Consumer of Fleet Validator)**. PROVINCE line 50 notes running `sources-census.sh validate --root <fleet-root> souji`; souji consumes the fleet validator, does not own citation read-back.

18. **`tabi-shokunin`** (`tabi-shokunin/PROVINCE.md:1-205`):
    - **C1 Surface**: **SILENT (Explicit Recognition of mado)**. PROVINCE line 199 explicitly records:
      `| mado | none | ... | PROVINCE.md:3 | desktop & compositor craft`
      Hits in `arc-synthesis.md:21,135` and `closeout-r11.md:37,128` are `date -u +%F`. Tabi automates browsers, not desktop application launches.
    - **C2 Surface**: **SILENT**. Mentions DOM read-back (`PROVINCE.md:144`) and operator response read-back (`arc-synthesis.md:1,19,60`); unrelated to source registry.

19. **`tameshi-shokunin`** (`tameshi-shokunin/PROVINCE.md:1-200`):
    - **C1 Surface**: **SILENT**. Verification-fixture craft; 0 hits.
    - **C2 Surface**: **ADJACENT (Mutation Testing of Sibling Gates)**. PROVINCE lines 61, 76, 79 claim mutation testing of kumitate's `scripts/sources-check.mjs`, and line 195 notes testing fleet-root `scripts/sources-census.sh`. Tameshi benchmarks and falsifies gates; it does not own the mado citation read-back gate.

20. **`tsukuroi-shokunin`** (`tsukuroi-shokunin/PROVINCE.md:1-580`):
    - **C1 Surface**: **ADJACENT (Explicit Deferral to mado & Systemd Units)**. PROVINCE line 48 (ADJ-03) explicitly delegates desktop behavior to mado:
      `| ADJ-03 | Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis | User-manager/unit, pam, display manager, socket or session boundary (→ mado)`
      In `btrfs-scrub-grounding-r45.md:269` and `btrfs-scrub-record-r44.md:97,117`, tsukuroi cites systemd unit specifier `ExecStart=/usr/bin/btrfs scrub start -B %f` (`systemd.unit(5)` `%f` = unescaped filename). In `degraded-triage-r4.md:175`, it mentions `walker` package triage. Tsukuroi governs systemd services and OS packages, leaving desktop application Exec expansion to mado.
    - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 gate claims.

### 1.2 Summary of Adjacency Sweep

- **C1 Surface (`Exec` field codes, `g_shell_parse_argv`, `gio launch`)**: **0 sibling claims**. Completely **UNCONTESTED**. Three sibling lanes (`game-dev-3d` PROVINCE:75, `tabi` PROVINCE:199, `tsukuroi` PROVINCE:48) explicitly defer desktop/compositor craft to `mado-shokunin`.
- **C2 Surface (SOURCES read-back, registry citation consistency)**: **0 sibling claims**. Completely **UNCONTESTED**. While `kagi` and `kumitate` maintain lane-local scripts (`corpus/sources-census.sh`, `scripts/sources-check.mjs`) and `tameshi` mutation-tests gates, no sibling owns citation read-back for mado or fleet-wide.

---

## 2. Fleet Census Contrast (`scripts/sources-census.sh`)

Does mado's C2 candidate (`quality/check-sources-readback.py`) duplicate the fleet instrument `scripts/sources-census.sh`?  
**NO.** The fleet census and mado's read-back gate operate on fundamentally different planes:

### 2.1 Exact Quotes from `scripts/sources-census.sh`

1. **Header definition of E09 and E11 (`scripts/sources-census.sh:28-29`)**:
   ```bash
   #             E09 invalid recheck (ISO date, NNd, or symbolic cadence)
   #             E10 community at tier A            E11 used-by path missing on disk
   ```

2. **Implementation of E11 (`scripts/sources-census.sh:563-570`)**:
   ```bash
       for path in "${paths[@]}"; do
         path=$(trim_cell "$path")
         [ -n "$path" ] && [ "$path" != "—" ] || continue
         if [ ! -e "$dir/$path" ]; then
           printf '%s\tE11\t%s missing used-by %s\n' "$lane" "$id" "$path"
         fi
       done
     done < "$f"
   ```

3. **Implementation of E09 (`scripts/sources-census.sh:663-667`)**:
   ```awk
           if (recheck ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) {
             if (epoch(recheck)==INVALID_EPOCH) printf "%s\tE09\t%s recheck=%s\n",lane,id,recheck
           } else if (recheck !~ /^[0-9]+d$/ && !symbolic(recheck)) {
             printf "%s\tE09\t%s recheck=%s\n",lane,id,recheck
           }
   ```

### 2.2 What `scripts/sources-census.sh` Does NOT Check

1. **Bidirectional Reverse Read-Back (`R4 entry-cites-unacknowledged`)**:
   `scripts/sources-census.sh` is strictly single-file: it inspects `corpus/SOURCES.md` and only tests whether paths already listed in `used-by` exist on disk (`[ ! -e "$dir/$path" ]`). It **never reads `corpus/knowledge/*.md` files**. If a knowledge entry's frontmatter contains `source: S504`, but row S504's `used-by` cell is `—` (or lists other files), `sources-census.sh` reports `CLEAN` (exit 0).
2. **Missing Row for Cited Source (`R5 entry-cites-missing-row`)**:
   If a knowledge file cites `source: S999`, but S999 does not exist in `SOURCES.md`, `sources-census.sh` cannot detect it because it never inspects knowledge file contents.
3. **Misplaced Path in Cadence (`R1 recheck-path`)**:
   When a knowledge entry path (e.g. `corpus/knowledge/foo.md`) accidentally lands in the `recheck` cell, `sources-census.sh` checks if it matches an ISO date or cadence (`NNd`), triggering a generic `E09` format violation; it has no semantic awareness of file paths in cadence cells and cannot correlate them to `used-by`.

**Conclusion**: `check-sources-readback.py` fills a critical gap in the fleet verification surface: it establishes bidirectional citation truth between the registry and knowledge entries that `sources-census.sh` cannot see by construction.

---

## 3. Cross-Source Pattern: Connecting the Desktop-Entry Exec Grammar

### 3.1 The Complete MIME & Launch Resolution Chain

Round 98's C1 capability (`tools/mado-execargv.py`) is the capstone of mado's MIME and application resolution stack across rounds 91, 92, 94, and 97:

1. **`tools/mado-filetype.py` (Round 97)**:
   Models `GLocalFileInfo`'s `get_content_type` (`glocalfileinfo.c:1300-1389`). Given a filesystem path on disk, evaluates `lstat(2)` mode inspection, basename glob matching (`tools/mado-mimeglob.py`), and bounded sniffing (`tools/mado-mimesniff.py` / `tools/mado-mimetext.py`) to determine the MIME type (e.g., `text/plain` or `application/pdf`).
2. **`tools/mado-mime.py` (Round 91) & `tools/mado-xdgmime.py` (Round 92)**:
   Given the MIME type, resolves the default `.desktop` file:
   - `mado-mime.py` models GLib's `g_app_info_get_default_for_type` reading `mimeapps.list` over `XDG_DATA_DIRS/applications/`.
   - `mado-xdgmime.py` models `xdg-mime query default <type>` (used by `xdg-open` on Hyprland).
3. **`tools/mado-execargv.py` (Round 98)**:
   Given the resolved `.desktop` file and argument list (files or URIs), models GLib 2.90.1's `expand_application_parameters` (`gdesktopappinfo.c:2700-2750`) and `g_shell_parse_argv` (`gshell.c`) to compute the exact `argc` and `argv` array passed to `execve`.

### 3.2 What the Join Makes Answerable: "Which file xdg-open opens" vs "Which argv gio launch builds"

Prior to round 98, mado could answer only:
- *"Which `.desktop` file opens a given file?"* (`mado-filetype.py` + `mado-mime.py` / `mado-xdgmime.py`).

With `mado-execargv.py`, mado can answer:
- *"What exact process command line is executed when the file is launched?"*

Crucially, examining upstream `xdg-open.in:334-380` (held as S508) reveals a stark cross-source divergence between generic shell handlers and GLib:
- In `xdg-open.in:334-380` (`search_desktop_file`):
  `xdg-open` on Hyprland uses naive shell IFS word-splitting:
  ```bash
  set -- $(get_key "${file}" "Exec" | last_word)
  while [ $args -gt 0 ]; do
      case $1 in
          %[c]) arg="${localised_name}"; shift; set -- "$@" "$arg" ;;
          %[fF]) [ -n "$target" ] || return; arg="$target"; shift; set -- "$@" "$arg" ;;
          %[uU]) arg="${target_uri:-$target}"; shift; set -- "$@" "$arg" ;;
          %[i]) shift; set -- "$@" "--icon" "$icon" ;;
          *) arg="$1"; shift; set -- "$@" "$arg" ;;
      esac
      args=$(( args - 1 ))
  done
  [ $replaced -eq 1 ] || set -- "$@" "${target:-$target_uri}"
  ```
  This naive shell expansion:
  1. Breaks quoted arguments containing spaces (e.g. `Exec=myprog --name="a b"` splits into `--name="a` and `b"`).
  2. Matches field codes **only as standalone arguments** (`%[fF]`). An embedded field code like `--file=%f` is **ignored** and passed verbatim as `--file=%f`!
  3. Ignores `%d`, `%n`, `%k`, `%%`.
- In contrast, GLib 2.90.1's `expand_application_parameters` (`gdesktopappinfo.c`):
  1. Walks the Exec string byte-by-byte, expanding `%f` even when embedded inside `--file=%f`.
  2. Quotes every inserted parameter via `g_shell_quote`.
  3. Parses the result with `g_shell_parse_argv`, cleanly preserving quoted tokens with spaces and escape sequences.
  4. Appends ` %f` if no parameter macro was present.

The join across mado's tools allows static prediction and falsification of whether a desktop entry will execute cleanly under `gio launch` versus silently breaking under generic `xdg-open`!

---

## 4. Frontier / Adjacency Verdict

```
CONTESTED_SCOPE: NONE
C1_SURFACE: UNCONTESTED across all 20 sibling lanes. (game-dev-3d, tabi, and tsukuroi explicitly assign desktop & compositor craft to mado).
C2_SURFACE: UNCONTESTED (quality/check-sources-readback.py provides bidirectional citation read-back not performed by fleet scripts/sources-census.sh).
```

---

## 5. Non-Obvious Move (UFO-FSD Compatible Synthesis Across Proposals)

### 5.1 Evidence Across Wave Proposals

1. **C1 Proposal Findings (`R98MMutC1`, `R98MExecTool`, `R98MReviewC1`)**:
   - `R98MMutC1` & L1 demonstrated that `GKeyFile` (`glib/gkeyfile.c:4567-4578`) executes *before* `expand_application_parameters` or `g_shell_parse_argv`. GKeyFile strictly rejects any backslash escape in a string key outside `{\s, \n, \t, \r, \\}` as `G_KEY_FILE_ERROR_INVALID_ESCAPES`, causing `gio launch` to refuse immediately (`desktop-file` error, exit 2).
   - In GIO URI handling, `gio launch` passes commandline arguments through `g_file_new_for_commandline_arg`, which strips URI fragments (`#anchor`) at the CLI boundary.
   - `R98MReviewC1` measured straggler child writes in multi-launch cases (`n=3` and `n=6`) when using a quiet-time settle loop in the oracle probe runner.
2. **C2 Proposal Findings (`R98MCriticC2`, `R98MExecGate`, `MadoR98`)**:
   - `R98MCriticC2` and `R98MExecGate` proved that Rule R2 (`usedby-outside-corpus`) as originally drafted in `claims-declaration-r98.md` fired 21 times on 19 legitimate historical rows in `corpus/SOURCES.md` that reference repo-valid paths outside `corpus/` (`tools/mado-verify.sh`, `SKILL.md`, `.ufo/waves/round-47/...`). This rendered the declaration's predicate `findings=0` at `--rev` completely unreachable without rewriting 19 historical rows.
   - L1 directed `R98MExecGate` to remove R2 from the finding set (or keep it as a non-fatal note), leaving R1, R3, R4, R5, R6.
   - `R98MCriticC2` further proved that S030 (`rejected`) and S132 (`queued`) are disowned citations where naive used-by additions create false provenance.

### 5.2 Affected Axes

- **`coverage` (C1)**: Ensures `tools/mado-execargv.py` models GKeyFile's exact 5-escape validation before argv parsing and prevents settle races on multi-launch cases.
- **`operability` (C2)**: Reconciles the C2 gate's findings with the historical registry so that the gate reports `findings=0` and exits 0 cleanly at `--rev` without mutating valid outside-corpus references.
- **Harms no axis**: Maintains 100% adherence to declared quality criteria (QUALITY 160–169), preserves historical row immutability, and keeps the fleet census clean.

### 5.3 Proposed Move: The Unified Parser Discipline Contract

Synthesize the GKeyFile pre-filter from C1 and the registry read-back parser from C2 into one coherent architectural principle:

1. **C1 GKeyFile Pre-Validation**:
   In `tools/mado-execargv.py`, validate key-file escape syntax before Exec macro expansion:
   ```python
   def has_bad_keyfile_escape(val):
       """GKeyFile refuses escapes outside {\s, \n, \t, \r, \\}."""
       i = 0
       while i < len(val):
           if val[i] == "\\":
               if i + 1 >= len(val) or val[i + 1] not in "sntr\\":
                   return True
               i += 2
           else:
               i += 1
       return False
   ```
   If `has_bad_keyfile_escape(exec_str)` is true, emit `MADO_EXECARGV: ERROR desktop-file detail=invalid-escape` and exit 2.
2. **C2 Gate Classification Alignment**:
   In `quality/check-sources-readback.py`, classify paths outside `corpus/` as non-fatal `NOTE outside-corpus` rather than `FINDING R2`, while enforcing `R3 usedby-missing` (`os.path.lexists(os.path.join(repo, m))`) across all members. This guarantees:
   - Valid repo paths (`SKILL.md`, `tools/...`, `.ufo/...`) are preserved without error.
   - Missing paths anywhere in the repo trigger `R3`.
   - The committed repaired registry evaluates to `findings=0` and exits 0 cleanly.

### 5.4 Risks and Verification

- **Risks**:
  - GKeyFile escape validation must not reject valid double-escapes (`\\\\`).
  - Skipping outside-corpus paths must not mask dangling files outside `corpus/` (mitigated by verifying `lexists` for all members under `R3`).
- **Verification**:
  - C1: `python3 tools/mado-execargv.py` passes all 16 frozen classes in `controls/execargv-cases-r98.json`; test case `quote-02` (`{probe} a\ b c`) cleanly exits 2 with `ERROR desktop-file`.
  - C2: `python3 quality/check-sources-readback.py --repo .` outputs `SOURCES_READBACK: rows=462 entries=118 findings=0` (exit 0) and `--selftest` outputs `SOURCES_READBACK_SELFTEST: checks=15 failed=0` (exit 0).
