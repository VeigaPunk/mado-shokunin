# R96MConnector — UFO-FSD Connector Report (Round mado 96, Wave w1)

**Seat**: `R96MConnector`  
**Role**: UFO-FSD connector / leaf member  
**Report target**: `.ufo/waves/round-96/w1/R96MConnector.md`  
**Base revision**: `9f029f46f01f6cd3a1d29ac39bb498a1d0c3d` (`master`)  
**Declared axes**:
- C1 `coverage` (new surface): GLib 2.90.1 text MIME database's magic step (`tools/mado-mimetext.py` modeling `xdgmimemagic.c`).
- C2 `operability`: `quality/check-receipt-presence.py` guarded by `quality/selftest-kills/check-receipt-presence.json` under `quality/check-selftest-strength.py`.

---

## 1. Sibling-Overlap Scan

We swept every sibling `PROVINCE.md` across all 21 active and physical lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (read-only), querying for `file(1)`, `libmagic`, `shared-mime-info`, `MIME`, `xdg-mime`, `xdg-utils`, `desktop entry`, and `Exec`:

1. **`audio-shokunin`**: References `--magic`, SoX autodetect, `libsndfile` + `libmagic` linkage, and container sniffing for audio formats (`act`, `au`, `wav`). Scope: audio container payloads and SoX driver flags.
2. **`chousa-shokunin`**: References `openat2` `RESOLVE_NO_MAGICLINKS`, RFC 5147 `text/plain` MIME entities, and gate baseline magic lines. Scope: syscall flags and kernel man page truth.
3. **`kagi-shokunin`**: References SQLite 3 format header magic string (`SQLite format 3\0`) in database state shape census (`PROVINCE.md:54`) and shell `exec` lines. Scope: local credential/state stores and shell wrappers.
4. **`kaidoku-shokunin`**: References `file(1)` for ASAR/PE/ELF triage (`2026-10-13-asar-surface.md`, `2026-10-13-pe-surface.md`), `readelf` wrong-magic rejection, AppImage squashfs, and V8 bytecode magic `0xC0DE06C3`. Scope: reverse-engineering format heuristics.
5. **`kake-shokunin`**: References OpenGraph `og:image` HTTP headers ("no fetch, MIME, dimension..."). Scope: web publishing metadata.
6. **`kengaku-shokunin`**: References harness execution classifications (`subprocess-exec`, `shell-exec`, `candidate-import`). Scope: model evaluation harness accounting.
7. **`revenger-shokunin`**: Holds extensive coverage of `magic(5)` (S176, Arch `core/file 5.48-1`), `file(1)` magic manual (S190, darwinsys/file), `libmagic` definitions, and format-specific magic bytes (Mach-O, PE, DEX, JVM ClassFile, Hermes HBC, WebAssembly, pyc, BTF, APE). Scope: binary analysis and format disassembly.
8. **`souji-shokunin`**: References git pathspec magic `:(top)` and `GIT_LITERAL_PATHSPECS`. Scope: repository hygiene and git tree filtering.
9. **`tabi-shokunin`**: References PNG magic bytes in browser screenshot validation (`Page.captureScreenshot`), and HTTP response `mimeType`. Scope: browser automation (CDP / WebDriver BiDi).
10. **`tameshi-shokunin`**: References magic byte length probes in mutation testing. Scope: mutation harnesses.
11. **`tsukuroi-shokunin`**: References pacman hooks `30-update-mime-database.hook` and `shared-mime-info-remove-cache.hook` (`pacman-hook-order-r38.md:53,97`), and kernel module `VERMAGIC_STRING`. Scope: system update safety and package manager transaction hooks.
12. **`mado-shokunin`**: Exclusively owns desktop & compositor craft, including the XDG desktop MIME stack (`mimeapps.list`, `defaults.list`, `mimeinfo.cache`, `*.desktop` default resolver in `tools/mado-mime.py`; `xdg-mime query default` in `tools/mado-xdgmime.py`; `globs2`/`globs` filename guesser in `tools/mado-mimeglob.py`; `mime.cache` binary magic sniffer in `tools/mado-mimesniff.py`; and the TEXT MIME database parser `mime/magic` in `tools/mado-mimetext.py`).

### Decision: Is the TEXT MIME Database (`mime/magic`) mado's Own?
**YES.** `mado-shokunin` exclusively owns the text MIME database (`mime/magic`), with full evidence:
- **Format Header**: GLib xdgmime's `mime/magic` strictly requires the 12-byte magic header `MIME-Magic\0\n` (`xdgmimemagic.c:806-819`). Traditional `file(1)`/`libmagic` does not use this header; it reads UNIX `magic(5)` rule files (`Magdir`).
- **Standard & Specification**: `mime/magic` is the freedesktop.org Shared MIME-Info specification (§2.5 "The magic files", S523/S525), compiled by `update-mime-database` and parsed by GLib's `gio/xdgmime/xdgmimemagic.c`.
- **Runtime Substrate**: On Linux desktop sessions running GLib/GTK applications (such as `walker`, `nautilus`, `gio info`, and any consumer of `g_content_type_guess`), when no `mime.cache` is present in reachable XDG data directories, `xdgmime.c:391-436` reads `DIR/mime/magic` in text mode. This directly governs desktop launcher associations and default application dispatch, which `mado-shokunin` owns under `PROVINCE.md`.

### Sibling Conflict Sentence
Which sibling sentence would conflict?
In `mado-shokunin/PROVINCE.md:555-556` (Round-95 refinement):
> "`xdg-open` on Hyprland uses `file(1)` (revenger's ground for libmagic rules) and is outside it."

And in `revenger-shokunin/PROVINCE.md:3-7`:
> "Owns: reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence — using the REA skill and its toolset, with an evidence-ledger discipline"

If `mado` attempted to model `file(1)`'s `magic(5)` / `libmagic` rule grammar, that would directly conflict with `revenger-shokunin`'s registered ownership of `file(1)` / `libmagic` (S176/S190).
However, GLib `xdgmime`'s `mime/magic` is NOT `libmagic` — it is freedesktop.org shared-mime-info syntax implemented in `gio/xdgmime/xdgmimemagic.c`, strictly within `mado`'s desktop MIME classification domain. No sibling sentence claims it, and `revenger` explicitly refuses non-binary-RE harness and desktop configuration.

---

## 2. Consideration Mining (`considerthese/2026-11-07.md`)

We reviewed `/home/vgpnk/Projects/shokunin/mado-shokunin/considerthese/2026-11-07.md` (read-only) and newest round reflections. Exactly ONE still-unimplemented proposal fits the round's C1/C2 surfaces:

> **Proposal 3**: "Distrust selftests written by the same author as the code. M95-1 shows a selftest can certify the author's misreading. Suggest a standing rule: library-semantics ports carry at least one exhaustive small-domain sweep (e.g. all 256 bytes against the shipped library) as a check, since that is what caught the VT bug."

### Fit with C1 and C2
- **C1 Fit**: C1 is an in-tree library-semantics port of GLib 2.90.1 `xdgmimemagic.c` into Python `tools/mado-mimetext.py`. Proposal 3 warns directly against relying solely on author-written `--selftest` assertions, which in round 95 allowed the VT whitespace bug (`isspace` vs `g_ascii_isspace`, M95-1) to pass `23/23` green. C1's 260+ case suite generated from the independent compiled C oracle (`mimesniff-oracle-r95.c`) provides the external verification requested by Proposal 3.
- **C2 Fit**: C2 is the operability gate `quality/check-selftest-strength.py`. It is the concrete institutionalization of Proposal 3: ensuring that `--selftest` assertions cannot be weakened or replaced with trivial passes without failing the gate.

---

## 3. Assimilation Census (`merge/mado/`)

We executed the id-collision and quarantine check from `.ufo/prompts/mado-round-96.md` §6 (read-only on `/home/vgpnk/Projects/shokuknow/merge/mado/`):

```sh
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-96/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"

R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
  {print $4, $5}' "$R" > "$A/quarantine-slice"
```

### Census Evidence
- **`reg-ids`**: 458 existing registry IDs (`S001` through `S523`).
- **`staged-ids`**: 147 staged IDs (`S203` through `S349`).
- **`collisions`**: Exactly 94 colliding IDs (`S203` through `S296`).
- **`quarantine-slice`**: 13 quarantine rows for `mado` (`S189`, `S195`, `S201`, `S205`, `S224`, `S228` payload-absent; `S199`, `S200`, `S209`, `S222`, `S223`, `S225`, `S235` unverified locators).
- **Plane Check**: We inspected every staged file under `/home/vgpnk/Projects/shokuknow/merge/mado/` (`MERGE-REPORT.md`, `SOURCES.append.md`, and 69 knowledge entries in `knowledge/corpus/knowledge/`). All staged entries cover legacy rounds 7–31 (Hyprland window rules, IPC socket framing, gkeep geometry, idle-lock chain, Chinese/Japanese wiki translations). Exactly **ZERO** staged entries touch MIME magic, content sniffing, `mime.cache`, or `xdgmime`.
- **Verdict**: `Assimilation: none`.

---

## 4. Sibling Defect Sweep

We swept the latest round-96 lessons across sibling lanes for defects that round 96's surfaces would inherit:

1. **`kake-shokunin` (`corpus/lessons/round-96.md` M1)**:
   - *Defect*: "Instrument governance: the frozen C2 counter's main scoring path crashes on every candidate-present run while its selftest passes" (`c96_reval.py:624`, `NameError: name 'mutants' is not defined` because only `selftest()` bound the population list, and pre-freeze controls ran only where candidate was absent).
   - *Inheritance risk*: `quality/counters/c1-r96-magictext.py` and `c2-r96-selftest-kills.py` must execute the candidate-present code path in pre-freeze checks, verifying variable bindings in `main()` independently of `selftest()`.
2. **`revenger-shokunin` (`corpus/lessons/round-96.md` M5)**:
   - *Defect*: "real-tree path-form mismatch (this round's miss): the v5 exclusivity leg compares used-by to `knowledge/round-96-…md` (fixture form) while the census and every existing row use `corpus/knowledge/round-96-…md`".
   - *Inheritance risk*: `tools/mado-mimetext.py` and the case fixtures must not assume short relative paths (`tools/mado-mimeglob.py` lazy import must resolve from `__file__` directory, and case root fixtures must handle `{root}/h` normalization without hardcoded path segments).
3. **`kaidoku-shokunin` (`corpus/lessons/round-96.md` M96-b)**:
   - *Defect*: "the honest run failed closed on its own revision ... v6's resolve_rev accepted only hex, so `--rev HEAD` returned None".
   - *Inheritance risk*: Both counters (`c1-r96-magictext.py` and `c2-r96-selftest-kills.py`) take `--rev`. They must handle symbolic Git references (`HEAD`, branch names) as well as 40-character hex commits.
4. **`kengaku-shokunin` (`corpus/lessons/round-96.md` M7)**:
   - *Defect*: "seat scratch inside the lane / fleet root ... fleet-root `.pytest_cache` naming the round-96 grader tests".
   - *Inheritance risk*: Seats must ensure all scratch files, caches, and test artifacts reside exclusively in `$HYAKU_SCRATCH`, never writing `__pycache__` or temporary files into the repository root or lane tree.
5. **`kotoba-shokunin` (`corpus/lessons/round-96.md` M96)**:
   - *Defect*: "`decoy-builder-cuts-elif-chain`: a decoy builder that inserts its guard immediately before a target statement splices a new statement between `if`/`elif` arms and cuts the chain, so the decoy world no longer compiles".
   - *Inheritance risk*: In C2, kill-set replacements in `quality/selftest-kills/check-receipt-presence.json` must be checked to ensure mutations do not splice invalid statements into Python `try`/`except` or `if`/`elif` blocks, causing syntax errors rather than clean check failures.
6. **`kumitate-shokunin` (`corpus/lessons/round-96.md` M96-2)**:
   - *Defect*: "the frozen counter again certified a fixture, not every clause of the rule ... The clause battery grew from 4 to 20 controls and still left 8 HELD constructions".
   - *Inheritance risk*: In C1, the case generator must test all 16 classes and boundary conditions of `xdgmimemagic.c`, especially the edge cases where upstream C departs from the specification text.

---

## 5. Non-Obvious Move (UFO-FSD Synthesis)

### 5.1 Evidence and Contradiction
A detailed code analysis of `gio/xdgmime/xdgmimemagic.c` against the freedesktop.org Shared MIME-Info specification (§2.5 "The magic files") and GLib's runtime behavior reveals five subtle semantic behaviors where upstream C diverges from the specification text or where Python ports easily introduce bugs:
1. **Section Discard on Parse Error** (`xdgmimemagic.c:283-300`, `:749-782`): If any matchlet line inside a section has a syntax or numerical error, the parser drops the **entire section** (`_xdg_mime_magic_match_free(match)`). The SMI specification text states: *"If an unknown character is found where a newline is expected then the whole line should be ignored"*. Upstream C discards the whole section.
2. **Parse-Time Word Swapping on Little-Endian** (`xdgmimemagic.c:476-505`): For word sizes 2 and 4 (`~2` or `~4`), upstream C swaps bytes at parse time on little-endian machines (`SWAP_BE16_TO_LE16` / `SWAP_BE32_TO_LE32`) for **both `value` and `mask`**. A port that only swaps `value` or swaps during matching will produce incorrect masked comparisons.
3. **Priority Tie Preservation** (`xdgmimemagic.c:596-629`): In `_xdg_mime_magic_insert_match`, insertion checks `if (list->next->priority < match->priority)`. Sections with strictly lower priority are placed after; sections with **equal priority preserve file order**.
4. **Matchlet Subtree Backtracking** (`xdgmimemagic.c:561-595`): In `_xdg_mime_magic_matchlet_compare_level`, if an indent-0 matchlet matches but its child matchlets (`indent > 0`) fail, upstream C skips the child subtree and **continues checking subsequent sibling matchlets at indent 0**. It does not terminate section evaluation on a child failure.
5. **Short-Buffer Abort** (`xdgmimemagic.c:515-536`): In `_xdg_mime_magic_matchlet_compare_to_data`, `if (i + matchlet->value_length > len) return FALSE;`. If the buffer ends before `offset + value_length`, it immediately aborts the range loop with `FALSE`.

Meanwhile, `claims-declaration-r96.md` notes that `tools/mado-mimesniff.py` was structurally unguarded by `quality/check-selftest-strength.py` because its `--selftest` could not be executed on a lone copy in scratch. While `tools/mado-mimetext.py` was designed with isolated `--selftest` execution, there is a risk that its selftest will use generic check labels (e.g. `FAIL parser`, `FAIL compare`), making it unguardable without future refactoring.

### 5.2 Affected Axes
- **`coverage` (C1)**: Strengthens the fidelity of the `xdgmimemagic.c` model by explicitly testing the 5 critical points where C diverges from the spec.
- **`operability` (C2)**: Pre-aligns `tools/mado-mimetext.py` for immediate admission into `quality/check-selftest-strength.py` without requiring future selftest refactoring or breaking output contracts.
- **Harms no axis**: Maintains full compatibility with `PRED-C1-r96-v1` and `PRED-C2-r96-v1`.

### 5.3 Proposed Move
Structure `tools/mado-mimetext.py`'s `--selftest` to implement **orthogonal 1:1 check labels** corresponding directly to the 16 declared case classes and the 5 critical divergence points identified between the SMI spec and `xdgmimemagic.c`:
1. `FAIL SECTION-DROP-ON-ERROR`: Verifies that a syntax error in a subsequent matchlet line drops the preceding valid matchlet of the same section.
2. `FAIL MASK-WORD-SWAP-LE`: Verifies that 16-bit and 32-bit word sizes (`~2`, `~4`) apply endian swapping to both value and mask on little-endian hosts.
3. `FAIL PRIORITY-TIE-ORDER`: Verifies that two sections with identical priority retain file order rather than reversing.
4. `FAIL CHILD-FAIL-CONTINUE`: Verifies that an indent-0 match whose indent-1 child fails falls through to evaluate the next indent-0 matchlet.
5. `FAIL BOUNDS-ABORT`: Verifies that data shorter than `offset + value_length` returns `FALSE` without crashing or matching.

Diagnostic details must be emitted on separate `MADO_MIMETEXT_SELFTEST_DETAIL:` lines, ensuring the failure lines strictly match `MADO_MIMETEXT_SELFTEST_FAIL: <label>` for gate compatibility.

### 5.4 Risks
- Modifying candidate code directly during wave w1 would break hash pins.  
- *Mitigation*: This move is submitted as a bounded design recommendation to L1 `MadoR96` and `R96MExecToolC1`; no candidate files are mutated by this seat.

### 5.5 Verification
1. Inspect `gio/xdgmime/xdgmimemagic.c` lines 283–300, 476–505, 515–536, 561–595, and 596–629 to confirm upstream C behavior.
2. Run `cc -O0 -o "$S/oracle" .ufo/waves/round-95/controls/mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)` against synthetic text magic fixtures isolating these five conditions to verify that GLib 2.90.1 matches these exact rules.

---

## 6. Execution and Host Guard Verification

- **Scratch**: Cleaned scratch directory `/fast/scratch/hyaku/mado-r96/R96MConnector` initialized and removed before exit.
- **Write Scope**: Wrote only `.ufo/waves/round-96/w1/R96MConnector.md` and `.ufo/waves/round-96/assimilation/` artifacts (`reg-ids`, `staged-ids`, `collisions`, `quarantine-slice`).
- **Host Guard**: Read-only verification throughout; no pacman, git, jj, or system modifications executed. CWD maintained at `/home/vgpnk/Projects/shokunin`.
