# mado round 94 — Connector Report (w1)

- Seat: `R94MConnector`
- Round: mado round 94 (hyaku run 15, attempt 1)
- Base revision: `a3de997289014e7dbf1d73ae206be1d6f8cdadd0` (master)
- Role: UFO-FSD Connector
- Report path: `.ufo/waves/round-94/w1/R94MConnector.md`
- Scratch: `/fast/scratch/hyaku/mado-r94/R94MConnector`

---

## 1. Named Axes

1. **coverage** (primary claim C1): File name → MIME type guessing as GLib 2.90.1 evaluates it (`g_content_type_guess(name, NULL, 0, &uncertain)`), covering shared-mime-info directory structures, `mime.cache` vs `globs2`/`globs` modes, literal/suffix/fnmatch lookup, case-sensitivity flags, weight sorting, duplicate merging, and trailing-slash directory resolution (`tools/mado-mimeglob.py`).
2. **operability** (primary claim C2): Extending the selftest-strength gate (`quality/check-selftest-strength.py`) to guard two existing lane tools (`tools/mado-xdgmime.py` with 12 checks, `tools/mado-mime.py` with 17 checks; 29 single-check neutralisations total).
3. **quality / discernment / expansion** (monitored axes): Invariant preservation, no false greens, no harm to prior capabilities (rounds 90–93 tools and gates green), clean separability between C1 and C2.

---

## 2. Sibling Overlap and Province Mapping (§1)

A full recursive scan was performed across every sibling repository (`/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` and `corpus/knowledge/**`) searching for `shared-mime-info`, `mime.cache`, `globs2`, `g_content_type_guess`, `xdgmime`, and `update-mime-database`.

### Findings & Ownership:

1. **`mado-shokunin` (Desktop & Association Plane — owns resolution):**
   - `mado-shokunin/PROVINCE.md:509-527`: Explicitly owns reading `mime/{mime.cache,aliases,subclasses}` under XDG data roots (`~/.local/share`, `/usr/local/share`, `/usr/share`), replaying xdgmime alias lookup and reading `.desktop` associations. Declares: *"Writing an association (`gio mime TYPE HANDLER`, `xdg-mime default`, `xdg-settings set`, `update-desktop-database`) is operator-owned and never run by the lane."*
   - `mado-shokunin/corpus/knowledge/mime-default-resolution-r91.md:1-272` (rows S504–S507): Documents GLib 2.90.1 default-application resolution and xdgmime cache/text parsing (`xdgmime.c`, `xdgmimecache.c`, `xdgmimealias.c`, `xdgmimeparent.c`).
   - `mado-shokunin/corpus/knowledge/xdg-mime-default-resolution-r92.md:1-338`: Documents xdg-utils 1.2.1 `xdg-mime query default` resolution.

2. **`tsukuroi-shokunin` (System Maintenance & ALPM Hook Plane — owns hook ordering):**
   - `tsukuroi-shokunin/corpus/knowledge/pacman-hook-order-r38.md:53,97`: Documents pacman libalpm post-transaction hooks:
     - Line 53: `| PostTransaction | 14 | 30-update-mime-database.hook | usr | no | no | /usr/bin/env |`
     - Line 97: `| PostTransaction | 49 | shared-mime-info-remove-cache.hook | usr | no | no | /usr/bin/sh |`
   - `tsukuroi-shokunin/PROVINCE.md:8-12`: Owns pacman state, ALPM hook order, and `.pkg.tar.zst` discipline. Tsukuroi tracks the trigger and invocation of `update-mime-database` during system package transactions, but does not parse MIME cache bytes or resolve associations.

3. **All other 19 sibling repositories (`audio`, `chousa`, `game-dev-2d`, `game-dev-3d`, `kagi`, `kaidoku`, `kake`, `kama`, `kasegi`, `kengaku`, `kotoba`, `kotodama`, `kumitate`, `lore`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`):**
   - Exactly **0** occurrences across their `PROVINCE.md` files and knowledge directories. No sibling claims or touches MIME globbing, MIME caches, or default application resolution.

---

## 3. Assimilation Check (§2)

Read of `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md` (read-only):
- Staged by `corpus-expansion-1`: 147 proposed source rows, 69 proposed knowledge entries.
- **Staged entries on MIME globbing / content-type guessing:** Exactly **0** (none). Every staged entry belongs to earlier rounds (rounds 1–16) covering Hyprland IPC contracts, dispatchers, waybar module text routes, idle-lock runtime states, and gkeep window geometry.
- **L1 Collision Check (`.ufo/waves/round-94/assimilation/`):**
  - `staged-ids`: Range S203 through S349 (147 rows).
  - `reg-ids`: Current mado registry holds 449 rows (up to S518).
  - `collisions`: 94 rows in `staged-ids` collide with existing mado rows (S203..S221, S253, S258, S277..S349) because mado continued minting rows after `corpus-expansion-1` packaged MERGE-REPORT.md.
  - Conclusion: No substantive overlap with Round 94's MIME globbing claims; the collision is purely numeric S-id crowding on historical Hyprland entries.

---

## 4. Pipeline Link: C1 to Rounds 91–92 Tools (§3)

Tracing where `file name → MIME type` feeds `MIME type → application (.desktop)`:

### A. The Two Separate Desktop Pipelines

1. **GLib / GIO Pipeline (`gio open`, GTK apps, Nautilus, portals):**
   - Step 1 (Name → Type): Calls `g_content_type_guess(filename, NULL, 0, &uncertain)`. Modeled by C1 candidate `tools/mado-mimeglob.py`.
   - Step 2 (Type → Application): Guessed type feeds `g_app_info_get_default_for_type(type, FALSE)`. Modeled by Round 91 tool `tools/mado-mime.py`.
   - Chaining: Direct feed. If `mado-mimeglob.py` answers `text/plain` (uncertain 0), `mado-mime.py text/plain` answers the default application (e.g., `org.gnome.TextEditor.desktop`).

2. **Generic Desktop Pipeline (`xdg-open` on Hyprland / sway):**
   - Step 1 (Name → Type): `xdg-open` detects `generic` DE on Hyprland (`detectDE` empty → `generic`). In `open_generic`, it invokes `xdg-mime query filetype FILE`.
   - Substrate mechanism: In `/usr/bin/xdg-mime:844-859` (`info_generic`), it calls `mimetype --brief --dereference "$1"` or `/usr/bin/file --brief --dereference --mime-type "$1"`.
   - Step 2 (Type → Application): Output feeds `xdg-mime query default "$filetype"`. Modeled by Round 92 tool `tools/mado-xdgmime.py`.

### B. Precise Caller Coverage of C1 (`mado-mimeglob.py`)

- **Covered Callers:**
  - Callers asking GLib for content type by filename alone without file contents (`g_content_type_guess(name, NULL, 0, &uncertain)`).
  - File managers, file choosers, and indexers determining icon/type metadata for remote, unread, or planned/non-existent files.
  - GLib/GIO application launchers where data sniffing is bypassed or deferred.
- **NOT Covered Callers:**
  - **`g_content_type_guess` with data (`data != NULL, data_size > 0`):** When content sniffing runs, GLib evaluates magic bytes via `_xdg_mime_magic_lookup`. Magic matches override uncertain filename matches and resolve filename glob conflicts (e.g., multiple equal-weight globs). `mado-mimeglob.py` does not model magic sniffing.
  - **`xdg-open` on generic desktops:** `xdg-open` uses `file(1)` (libmagic) or `mimetype(1)` to inspect existing files on disk, NOT `g_content_type_guess` and NOT shared-mime-info `mime.cache`/`globs2`.
  - **Non-existent files under `xdg-mime`:** `xdg-mime query filetype` exits rc 2 with error if the file does not exist, whereas `mado-mimeglob.py` evaluates filename strings purely offline.

### C. Explicit Contradiction Identified

`claims-declaration-r94.md:11` states:
> *"Surface moved: the name-to-type step that precedes every default-application answer (rounds 91–92 resolve type → application; nothing in the lane answers name → type)."*

**Contradiction:** This premise is over-broad. C1's name-to-type step precedes **GLib/GIO** default-application answers (`mado-mime.py`), but does **not** precede `xdg-open`'s default-application answers on generic desktops (`mado-xdgmime.py`), which route through libmagic (`file(1)`). This is a second recurrence of mistake class **M92-2** (caller premise overstatement).

---

## 5. Cross-Domain Evidence Encountered (§4)

1. **System Packaging & Pacman Hooks (`tsukuroi-shokunin`):**
   `update-mime-database` builds `mime.cache` from `/usr/share/mime/packages/*.xml`. This binary compilation is driven by ALPM post-transaction hooks owned by tsukuroi. Mado inspects the resulting database formats read-only, never triggering package hooks.
2. **Binary Parsing / Structural Deserialization (`kaidoku-shokunin` / `revenger-shokunin`):**
   `mime.cache` uses a binary structure (32-bit offsets, 16-bit counts, reverse suffix trie nodes, magic headers). While resembling reverse-engineering binary analysis, mado implements the reader per GLib upstream C source (`xdgmimecache.c`), maintaining strict domain boundaries.
3. **Application Execution Plane (`kumitate-shokunin`):**
   Resolving a `.desktop` file name (e.g., `gedit.desktop`) stops at identification. Executing `Exec=` arguments, field code expansion (`%f`, `%u`), and process spawning belong to execution/orchestration runtimes. Mado remains strictly a read-only resolution oracle.

---

## 6. Considerthese Reflection Mapping (§5)

Read of `considerthese/2026-11-06.md`:
- **Proposal 4 ("Widen desktop coverage past bar + mako ... prefer one operator-config gap over another harness counter"):**
  Directly answered by **C1** (`tools/mado-mimeglob.py`). Extends mado's desktop coverage into user-level MIME configuration (`~/.local/share/mime/packages/*.xml`, `globs2`, `mime.cache`) and filename-to-type evaluation.
- **Proposal 5 ("Verify QUALITY 145 has an instrument, not only a criterion") & Round-93 Spot-Check Routed Defect 2:**
  Directly answered by **C2** (`quality/counters/c2-r94-selftest-kills.py` + kill-sets for `mado-xdgmime.py` and `mado-mime.py`). Transitions selftest-strength gating from a single-tool check into multi-tool coverage.

---

## 7. Mined Mistake Candidate from Rounds 90–93 Records (§6)

- **Candidate:** Uncreated Scratch Directory in Harm Watch Harness (Harness-Invocation Precondition Failure).
- **Class:** `harness-precondition defect` / `uncreated-scratch invocation`.
- **Evidence:** `.ufo/waves/round-93/receipts/harm-final-r93.txt:59-61`:
  ```
  $ python3 -I tools/mado-mako.py --selftest --scratch-root /fast/scratch/hyaku/mado-r93/L1/harm/mako
  mado-mako: setup error: --scratch-root is not a directory: /fast/scratch/hyaku/mado-r93/L1/harm/mako
  rc=2
  ```
  Reported by the non-author verifier in `corpus/lessons/round-93-verifier-spotcheck.md:30-33` as a harness defect, and corrected append-only at `harm-final-r93.txt:225-230` (`mkdir -p "$S/mako"`).
- **Why Unmined:** `corpus/lessons/round-93.md` mined six mistakes (M93-1 through M93-6) focusing on mutant sweep moving targets, unique-killer constraints, and counter exit-code fidelity, but omitted this harness execution failure.
- **Remedy:** All harness scripts running tools with `--scratch-root` must guarantee `mkdir -p` before invocation, or tools must adopt `os.makedirs(scratch_root, exist_ok=True)` (as implemented in `quality/check-selftest-strength.py:136`).

---

## 8. Non-Obvious Move / Synthesis Proposal (§7)

### A. Evidence & Context
1. In C1, `tools/mado-mimeglob.py` is authored with 15 selftest checks (`checks.append((label, condition))`) ending with `failed = [n for n, ok in checks if not ok]`.
2. In C2, `quality/check-selftest-strength.py` guards against weakened selftest assertions by applying single-check neutralisations (`... if not ok and n != X`). C2 commits kill-sets for `mado-xdgmime.py` (12 checks) and `mado-mime.py` (17 checks) totaling 29 checks.
3. `mado-mimeglob.py` uses the exact structural pattern required by `check-selftest-strength.py`. However, because C1 is measured at its own commit prior to C2, and C2's predicate is strictly bounded to the 29 checks of the two older tools, `mado-mimeglob.py` enters the repository with 15 unguarded selftest assertions.
4. When chaining `mado-mimeglob.py` into `mado-mime.py`, `mado-mimeglob.py` emits an `uncertain` flag (0 or 1). When `uncertain=1` (trailing slash, no match, or multiple equal-weight conflicting globs), GLib picks the first type tentatively, but full desktop environments trigger content sniffing before default application launch.

### B. Affected Axes
- **operability (improved):** Prevents the recurring defect where newly minted tools carry unguarded selftests that can erode without detection.
- **coverage (improved):** Clarifies the exact composability contract between `mado-mimeglob.py` and `mado-mime.py` when handling uncertain classifications.
- **quality (unharmed):** Preserves strict claim separability (C1 measured before C2 without cyclic dependencies).

### C. Proposed Move: Co-Landed Selftest Kill-Set Specification at Mint Time
1. **Contract Standard:** Formulate the requirement that any future capability tool authored to the `checks` tuple convention must author its candidate kill-set JSON (`quality/selftest-kills/<tool>.json`) at mint time.
2. **Immediate Fast-Follow (Round 95 Route):** Route the creation of `quality/selftest-kills/mado-mimeglob.json` (covering `mado-mimeglob.py`'s 15 checks) as an immediate operability claim in the next round, preventing test-erosion debt.
3. **Pipeline Contract Enforcement:** In the knowledge entry for `mado-mimeglob.py`, document the pipeline rule:
   - When `mado-mimeglob.py` returns `uncertain=0`, output type is authoritative for `tools/mado-mime.py`.
   - When `mado-mimeglob.py` returns `uncertain=1`, output is tentative; callers must check `types` for conflicts or recognize fallback to `application/octet-stream` / `inode/directory`.
   - Explicitly document that `xdg-open` generic callers must **not** invoke this pipeline, as `xdg-mime query filetype` evaluates file content on disk via libmagic.

### D. Risks & Second-Order Effects
- *Risk:* Attempting to fold `mado-mimeglob.py` into C2 during Round 94 would violate separability (C1 must land and measure independently before C2, and C2's panel/counter inputs are already frozen).
- *Mitigation:* Keep C2 strictly bounded to the 29 checks of `mado-xdgmime.py` and `mado-mime.py`. Route `mado-mimeglob.py`'s kill-set as a declared next-round task.

### E. Verification
- DRAFT candidate selftest:
  `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-94/build/mado-mimeglob.c1.py --selftest`
  → `MADO_MIMEGLOB_SELFTEST: checks=15 failed=0` (rc 0).
- DRAFT gate selftest:
  `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-selftest-strength.py --selftest`
  → `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0` (rc 0).
- Scratch oracle verification against glib2 2.90.1-1:
  Compiled `mimeglob-oracle-r94.c` in `/fast/scratch/hyaku/mado-r94/R94MConnector/oracle`; confirmed identical answers on trailing slashes (`inode/directory`, 1), standard files (`text/plain`, 0), and unknown extensions (`application/octet-stream`, 1).

---

## 9. Cleanup

- Scratch directory `/fast/scratch/hyaku/mado-r94/R94MConnector` and compiled oracle artifact will be cleaned up prior to final exit.
