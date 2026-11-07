# R97MConnector — UFO-FSD Connector Report (Round mado 97, Wave w1)

**Seat**: `R97MConnector`  
**Role**: UFO-FSD connector / leaf member  
**Report target**: `.ufo/waves/round-97/w1/R97MConnector.md`  
**Lane root**: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base revision**: `e6152b589c2c6a28426c28263c4bcc3c46398be4` (`master`)  
**Declared axes**:
- **C1 `coverage`** (new surface): GLib 2.90.1 GIO `standard::content-type` and `standard::fast-content-type` for local filesystem paths (`tools/mado-filetype.py` modeling `GLocalFileInfo`'s `get_content_type` in `glocalfileinfo.c:1300-1389`).
- **C2 `operability`**: Gate standard self-invocation (`--selftest`) over isolated fixtures for the two round-96 counters (`quality/counters/c1-r96-magictext.py` and `quality/counters/c2-r96-selftest-kills.py`), plus closing the Gate standard's registry gap in `SKILL.md`.

---

## 1. Sibling-Overlap Scan (Adjacency Axis, Read-Only)

We swept every sibling lane's `PROVINCE.md` across all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` (read-only), testing for claims on the seven target categories:
1. GIO's `standard::content-type`
2. `gio info`
3. content-type by path
4. file-kind detection
5. MIME databases
6. `file(1)`
7. execution/launch

### 1.1 Sibling Sweep Findings Per Lane

1. **`audio-shokunin`** (`/home/vgpnk/Projects/shokunin/audio-shokunin/PROVINCE.md`):
   - **NO-HIT** across all 7 categories. (Audio container payloads, SoX driver flags, and ALSA/PipeWire/PulseAudio audio sinks).

2. **`chousa-shokunin`** (`/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md`):
   - **NO-HIT** across all 7 categories. (Kernel syscall man pages, `openat2` flag semantics, Linux kernel docs).

3. **`game-dev-2d-shokunin`** (`/home/vgpnk/Projects/shokunin/game-dev-2d-shokunin/PROVINCE.md`):
   - Category: `execution/launch`
     - Line 18: `save/load and export/launch. \`corpus/README.md\` §Coverage map gives the measured`
     - Line 23: `Rendered output/performance, clean-checkout import→export→launch, engine-version`
   - Categories 1–6: **NO-HIT**. (Confined to Godot/Unity 2D engine export and game project launch).

4. **`game-dev-3d-shokunin`** (`/home/vgpnk/Projects/shokunin/game-dev-3d-shokunin/PROVINCE.md`):
   - Category: `execution/launch`
     - Line 14: `Engine census and execution reality live in corpus/knowledge/engines.md`
     - Line 19: `execute headless on this host, the lane builds format-level and static`
     - Line 40: `craft evidence only: no live-target execution beyond a declared target`
   - Categories 1–6: **NO-HIT**. (Confined to Godot/Blender 3D headless tool execution).

5. **`kagi-shokunin`** (`/home/vgpnk/Projects/shokunin/kagi-shokunin/PROVINCE.md`):
   - Category: `execution/launch`
     - Line 42: `- \`~/.config/the-janitor/client.py\` (755, 117 lines) — HTTP client: session-id, \`THE_JANITOR_REQUEST_TIMEOUT\` (the \`client.lock\` flock lives in the CLI, not here — measured round 15: \`grep -nic lock client.py\` ⇒ 0; \`the-janitor\` holds \`LOCK_FILE\` at L12, \`exec 9>"$LOCK_FILE"\` at L130/139/175 and \`flock 9\` at L131/140/176)`
     - Line 67: `- \`corpus/surface-census.sh\` — the declaration gate over the surface list above. \`verify\` (default): kind/exact mode per declared path, \`UNLISTED\` children of the 4 enumerable dirs, and the runtime shape pins; \`--verbs\` exercises the local write-side verbs on scratch overrides (no \`op\` exec); ...`
     - Line 68: `- \`corpus/drift-pins.sh\` + \`corpus/drift-baseline.tsv\` (15 files) + \`corpus/drift-symbols.tsv\` (20 claims — 20 since round 12 added the \`cmd_run\` L248 \`exec op run\` row, the masking premise) — byte/line/symbol drift; modes cross-checked against the census`
     - Line 70: `- \`corpus/op-ref-probe.sh\` — the \`op.env\` contract gate: \`refs\` (\`cmd_refs\` awk) vs \`op run --env-file\` (what \`cmd_run\` execs) over generated plain-value fixtures, plus the dotenv edge classes, precedence, six error signatures ...`
   - Categories 1–6: **NO-HIT**. (Shell `exec` / flock wrappers and 1Password CLI `op run` command-line execution).

6. **`kaidoku-shokunin`** (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md`):
   - Category: `execution/launch`
     - Line 108: `execution, Frida-style hooking \`(unowned)\`. gdb stays a fallback reader for`
     - Line 139: `| Runtime observation verbs | self-launched CDP/V8-inspector targets (r3 recipe); \`node --inspect\` needs a real file target (bare \`file://\` → \`unsupported_location\`) | \`observe-web-session\`, \`observe-web-execution\`, \`observe-javascript-runtime\`, \`reconcile-javascript-runtime\` | all held r4-08; \`capture-electron-scenario\` remains typed refusal (Playwright handshake, not app launch) |`
     - Line 180: `| Rizin command observation | \`rizin\` on PATH (\`/usr/bin/rizin\`), optional \`REA_RIZIN_COMMAND\`; REA runs \`rizin -N -q -c <cmd> <path>\` | \`execute-rizin-command <path> iI\` | jq, libjq, round-2 PE (\`corpus/knowledge/2026-10-20-r20-rizin-command-observation.md\`); unrestricted shell-capable surface — read-only info commands only |`
     - Line 226: `round; replacement work performed no debugger/target execution. Correct aliases in the`
     - Line 248: `decompilation or target execution claim follows.`
     - Line 271: `| decode-signal-recording | Held on the exact synthetic/public offline recordings; literal annotations and diagnostics, not lossless traffic recovery, live acquisition or device execution |`
     - Line 366: `| ARM64X hybrid PE through REA 6.5.0 \`inspect\` | Native-view \`binary_overview\` on twelve pinned, author-built exported-leaf DLLs; raw COFF 0xAA64 plus CHPE ARM64/ARM64EC ranges; ordered segments and native-view procedure counts checked against the frozen byte oracle and predictions. Not dual-view recovery, decompilation or execution | \`corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md\` |`
     - Line 523: `| The safe packer seam — identity before first execution, the validated path threaded through every packer call, a four-key child-env allowlist (HOME/LANG/PATH/TMPDIR, HOME and TMPDIR inside the run's scratch), typed \`broken_tool: node\` and packer refusals instead of tracebacks, per-run \`mkdtemp\` scratch, no \`/tmp\` HOME fallback | \`tools/round-70/seam-probe.py\` (seven arms) against \`tools/round-70/packed-elf.py\` | ...`
     - Line 596: `\`counting-command\` block, refuses every unbound placeholder and shell metacharacter before any execution,`
   - Categories 1–6: **NO-HIT**. (Confined to binary reverse-engineering target execution and CDP debug targets).

7. **`kake-shokunin`** (`/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md`):
   - Category: `content-type by path`
     - Line 235: `response “MUST have a Content-Type of "text/plain" with the default charset`
     - Line 282: `Content-Type was recorded, so their conformance to the RFC's serving`
     - Line 669: `(\`content-length\`, \`content-type\`, \`content-encoding\`, \`vary\`, …), \`policy\` (\`cache-control\`, ...)`
     *(Note: All three hits refer to HTTP response headers from web servers per RFC 5147, not filesystem path content-type detection).*
   - Category: `MIME databases`
     - Line 202: `non-empty \`og:image\` (no fetch, MIME, dimension, HTTPS or reachability test);`
     *(Note: Explicit refusal of MIME verification on OpenGraph images).*
   - Category: `execution/launch`
     - Line 67: `JS-rendered-canonical frontier above remains open; browser execution stays tabi's`
     - Line 86: `execution stays separately authorized adjacent work; publishing stays with`
     - Line 718: `contract, with an execution-time sandbox against delegation and an advisory line for`
   - Categories 1–2, 4, 6: **NO-HIT**.

8. **`kama-shokunin`** (`/home/vgpnk/Projects/shokunin/kama-shokunin/PROVINCE.md`):
   - Category: `execution/launch`
     - Line 242: `\`python3\` on PATH is the Microsoft Store app-execution alias stub, not a`
     - Line 331: `registers and self-record, execute no endpoint call and write nothing outside their scratch.`
   - Categories 1–6: **NO-HIT**. (LLM endpoint gateway observation; refuses endpoint execution).

9. **`kasegi-shokunin`** (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md`):
   - Category: `execution/launch`
     - Line 221: `[r74 Frontier amendment, appended 2026-11-05, end-of-file append per R6] F52 — the Fuzzilli project's own README ... the REPRL execution mode; ...`
   - Categories 1–6: **NO-HIT**. (JavaScript engine vulnerability research / fuzzer architecture).

10. **`kengaku-shokunin`** (`/home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md`):
    - Category: `execution/launch`
      - Lines 254, 266, 282, 288, 311, 335, 375, 394, 424, 443, 475, 494, 536, 561, 594, 674, 977: Sandboxed offline execution of Terminal-Bench 2.0 benchmark task graders.
      - Line 335: `Sandboxed execution of a graded or mutated child is fleet prior art, not kengaku ground.`
    - Categories 1–6: **NO-HIT**. (Model evaluation benchmark harness execution).

11. **`kotoba-shokunin`** (`/home/vgpnk/Projects/shokunin/kotoba-shokunin/PROVINCE.md`):
    - **NO-HIT** across all 7 categories. (Natural language grammar, glossaries, localization).

12. **`kotodama-shokunin`** (`/home/vgpnk/Projects/shokunin/kotodama-shokunin/PROVINCE.md`):
    - **NO-HIT** across all 7 categories. (Lexicon and linguistic semantics).

13. **`kumitate-shokunin`** (`/home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md`):
    - Category: `execution/launch`
      - Line 24: `- Durable-execution and multi-agent failure research (idempotency, timeouts, failure taxonomies) — first entry \`corpus/knowledge/at-least-once-dedupe.md\` (round 54; S106/S107) ...`
    - Categories 1–6: **NO-HIT**. (Durable execution engine patterns and multi-agent orchestration).

14. **`lore-shokunin`** (`/home/vgpnk/Projects/shokunin/lore-shokunin/PROVINCE.md`):
    - **NO-HIT** across all 7 categories. (Narrative fiction and campaign lore).

15. **`mori-shokunin`** (`/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md`):
    - Category: `execution/launch`
      - Line 22: `- **Watchdog liveness** — census \`SURFACE watchdog\`: watchdog pid/start and log freshness, plus \`.ufo/state/*.round\` values against each lane's latest launch-ledger entry.`
      - Line 28: `- **Lane silence** — \`SURFACE lane.<id>\` rows: launch-anchored authorship grading as silent, progressing, progressing-weak, young, not-open, or unavailable.`
      - Line 47: `- **FR4 — Driver-state versus MANIFEST versus lane-LOG round reconciliation** (state F4). ... Boundary: the census compares driver state with watchdog launch lines only; it does not establish MANIFEST admission or lane-LOG agreement.`
    - Categories 1–6: **NO-HIT**. (Fleet watchdog liveness and lane launch observability).

16. **`revenger-shokunin`** (`/home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md`):
    - Category: `execution/launch`
      - Line 44: `Refuses: live-target execution beyond the declared target and lifecycle`
    - Categories 1–6: **NO-HIT**.
    *(Note on `file(1)`: While revenger owns binary reverse engineering and holds source references for `file(1)` / `libmagic` (S176/S190), revenger's `PROVINCE.md` claims binary forensics of shipped artifacts and explicitly refuses desktop configuration).*

17. **`souji-shokunin`** (`/home/vgpnk/Projects/shokunin/souji-shokunin/PROVINCE.md`):
    - Category: `execution/launch`
      - Line 139: `and do not infer historical command execution or acquire kumitate's fleet`
    - Categories 1–6: **NO-HIT**. (Repository sanitation, git hygiene, worktree maintenance).

18. **`tabi-shokunin`** (`/home/vgpnk/Projects/shokunin/tabi-shokunin/PROVINCE.md`):
    - Category: `execution/launch`
      - Line 53: `(resolve-at-launch \`--scratch\`/\`--out\`, optional \`--nav\`); the r48 runner above stays frozen and`
      - Line 190: `| kaidoku | contested | 0b518f568da7b40a4ab026508d63c942faa7badf | PROVINCE.md:55 | self-launched targets: chromium --headless --remote-debugging-port=9222 | Both lanes self-launch Chromium over loopback CDP and inspect pages ...`
    - Categories 1–6: **NO-HIT**. (Browser automation over CDP / WebDriver BiDi).

19. **`tameshi-shokunin`** (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md`):
    - **NO-HIT** across all 7 categories. (Mutation testing harnesses and operator mutation suites).

20. **`tsukuroi-shokunin`** (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`):
    - Category: `execution/launch`
      - Line 40: `service changes, credential reads, endpoint requests, or target execution.`
      - Line 104: `fields only; VM execution unverified; second opinion and maintainer deferral`
      - Line 335: `sourced S258 S259). The \`python3\` interpreter name resolves to the Store App-execution-alias stub on this`
    - Categories 1–6: **NO-HIT**. (System updates, ALPM package transactions, systemd service units. `tsukuroi` observes package hooks like `30-update-mime-database.hook` in knowledge, but does not parse or resolve MIME databases in PROVINCE).

### 1.2 Summary of Adjacency Sweep

- **GIO `standard::content-type`**: **0 sibling hits**. Exclusively referenced in `mado-shokunin/PROVINCE.md`.
- **`gio info`**: **0 sibling hits**. Exclusively referenced in `mado-shokunin/PROVINCE.md`.
- **content-type by path**: **0 sibling hits** (`kake-shokunin` mentions HTTP response `Content-Type` headers over TCP sockets; no sibling touches filesystem path content-type).
- **file-kind detection**: **0 sibling hits**.
- **MIME databases**: **0 sibling claims** (`kake` refuses MIME validation for `og:image`; `tsukuroi` tracks package hooks for database regeneration).
- **`file(1)`**: **0 sibling claims** in `PROVINCE.md`.
- **execution/launch**: Mentions in sibling lanes are strictly partitioned within their domain boundaries (game engines, reverse-engineering targets, benchmark graders, browser instances, or command runners). **No sibling lane claims desktop default application launch or MIME-based handler execution.**

---

## 2. Cross-Check Against mado's Own PROVINCE.md

### 2.1 Current Province Quotes

Is `standard::content-type` inside mado's declared province?  
**YES.** `mado-shokunin/PROVINCE.md` explicitly cites GIO's `standard::content-type` in lines 555 and 570 as the desktop caller governing file content-type resolution:

1. **Line 555–556 (Round-95 refinement):**
   > *"Its caller on this host is GIO's `standard::content-type`; `xdg-open` on Hyprland uses `file(1)` (revenger's ground for libmagic rules) and is outside it."*

2. **Line 570–572 (Round-96 refinement):**
   > *"Its callers are the same GIO `standard::content-type` path as round 95, but only on a host whose reachable directories hold no loadable cache; `xdg-open` on Hyprland still uses `file(1)` (revenger's ground) and is outside it."*

### 2.2 Boundary Analysis and New Surface Demarcation

At the base revision (`e6152b58`), `mado`'s province accounted for three read-only instruments in the MIME classification stack:
- `tools/mado-mimeglob.py` (Round 94): Models filename-only guessing (`g_content_type_guess(name, NULL, 0)`).
- `tools/mado-mimesniff.py` (Round 95): Models binary cache sniffing (`g_content_type_guess(name, data, len)` against `mime.cache`).
- `tools/mado-mimetext.py` (Round 96): Models text database sniffing (`g_content_type_guess(name, data, len)` against `mime/magic`).

All three answer *inputs* (strings and byte buffers), not filesystem *paths*.  
The C1 candidate, `tools/mado-filetype.py`, answers `standard::content-type` and `standard::fast-content-type` for actual filesystem paths by modeling `GLocalFileInfo`'s `get_content_type` (`gio/gio/glocalfileinfo.c:1300-1389`, held as S522).

**Boundary Definition for the Integrator's PROVINCE Refinement:**
- **Inside mado's province**: Read-only evaluation of a path's content type matching `GLocalFileInfo`:
  1. `lstat(2)` mode inspection: broken symlink or `--nofollow` → `inode/symlink`; directory → `inode/directory`; character device → `inode/chardevice`; block device → `inode/blockdevice`; FIFO → `inode/fifo`; regular file with size 0 → `application/x-zerosize`; UNIX socket → `inode/socket`.
  2. Basename name-only guess (`tools/mado-mimeglob.py`).
  3. Bounded sniffing (`_g_unix_content_type_get_sniff_len()` clamped to 16384 bytes, opened `O_RDONLY|O_CLOEXEC`) only when `--fast` is absent and the name guess is uncertain.
  4. Sibling module composition: loading `mado-mimeglob.py`, `mado-mimesniff.py`, and `mado-mimetext.py` via pinned paths.
- **Outside mado's province (Refused & Separated)**:
  1. `file(1)` / `libmagic` execution: `xdg-open` on Hyprland shells out to `file(1)`, which belongs to `revenger-shokunin` (S176/S190); `mado` does not model `magic(5)` grammar.
  2. MIME database generation or mutation: `update-mime-database` and modifying `/usr/share/mime` or `~/.local/share/mime` stay operator-owned (and package hook order belongs to `tsukuroi-shokunin`).
  3. Application execution / launching: `gio launch`, `gtk-launch`, `xdg-open` stay operator-owned.
  4. Path failure refusal: A path that cannot be stat'ed (missing path, or non-directory traversal) is refused with `MADO_FILETYPE: ERROR stat` and exit 2; it is not guessed.
  5. Non-content-type attributes: GIO attributes such as `standard::display-name`, `standard::icon`, `standard::size`, and POSIX permissions are outside this model.

---

## 3. Duplicated Ground Check Inside mado's Own Corpus

We searched `corpus/knowledge/*.md` for `inode/`, `standard::content-type`, and `zerosize`:

1. **`corpus/knowledge/mime-default-resolution-r91.md`**:
   - Line 313: `| inode/directory | org.gnome.Nautilus.desktop | org.gnome.Nautilus.desktop | org.gnome.Nautilus.desktop |`
   - *Analysis*: Evaluates `mimeapps.list` default application mapping for the MIME type string `"inode/directory"`. It states no rule for classifying a filesystem path or stat buffer.

2. **`corpus/knowledge/mime-glob-guess-r94.md`**:
   - Lines 155, 185, 334: `filename ends /` → `inode/directory`, uncertain=1 (`gcontenttype-fdo.c:594-604`).
   - *Analysis*: Analyzes the string-level rule in `g_content_type_guess` when a supplied filename ends with ASCII `/`. It does not execute `stat(2)` or evaluate directories on disk.

3. **`corpus/knowledge/mime-magic-sniff-r95.md`**:
   - Lines 34–38: Cites GIO's `glocalfileinfo.c:1337-1351` as the host caller passing byte buffers to `g_content_type_guess`.
   - Lines 74, 269, 297, 408, 410: Documents that `g_content_type_guess` with `data != NULL` and `len == 0` returns `application/x-zerosize` with priority 100.
   - Line 78–79, 298: Explicitly records: *"one name type wins over empty data (row `n-one-empty` → `t/single 0`), while zero or several name types get `application/x-zerosize 0`"*.
   - Line 246: Supertyping rule: `application/octet-stream` is a supertype for everything except `inode/*`.
   - *Analysis*: Analyzes `g_content_type_guess` when provided with in-memory byte buffers. It does **not** evaluate paths on disk. In fact, for in-memory inputs, a file named `empty.png` with 0 bytes returns `image/png` (because the single extension match short-circuits before data evaluation). In contrast, on disk `glocalfileinfo.c:1320-1325` intercepts size-0 regular files before name guessing, returning `application/x-zerosize`.

4. **`corpus/knowledge/mime-textdb-magic-r96.md`**:
   - Lines 240, 249, 486, 608: Documents `len == 0` handling in text mode for `g_content_type_guess`.
   - Line 285: `application/octet-stream` supertype exclusion for `inode/*`.
   - Line 263, 485: Trailing slash filename rule.
   - *Analysis*: Pure buffer and string semantics for text-mode magic parsing; no path or stat rules.

### Conclusion:
**No duplicated ground exists.** Not a single held entry in `corpus/knowledge/*.md` states path-level content-type resolution or `statbuf` dispatch rules. All existing entries cover `g_content_type_guess` given synthetic name and byte inputs. The path-level surface of `GLocalFileInfo` (`glocalfileinfo.c`) is entirely new ground for round 97.

---

## 4. Contested Scope Line for the Integrator

```
CONTESTED_SCOPE: NONE (clean boundary between mado-shokunin's GLocalFileInfo get_content_type path-level resolution, revenger-shokunin's file(1)/libmagic reverse-engineering ground, and tsukuroi-shokunin's update-mime-database ALPM hook order).
```

---

## 5. Non-Obvious Move (UFO-FSD Compatible Synthesis Across Proposals)

### 5.1 Evidence and Contradictions Identified in Current Round w1

A rigorous cross-examination of upstream C source code (`glocalfileinfo.c`), the frozen declaration (`claims-declaration-r97.md`), and in-flight wave artifacts revealed two critical contradictions that threaten round closure:

#### Contradiction 1: Symlink Loop and Broken Symlink Refusal Bug in C1 Candidate
1. **Upstream GLib Behavior** (`glocalfileinfo.c:1932-1996`):
   GIO queries local file information by calling `g_local_file_lstat(path, ...)` first.
   - When `path` is a broken symlink (`broken -> nowhere`) or a symlink loop (`loop -> loop`):
     - `lstat` **succeeds** (`res != -1`), setting `stat_ok = TRUE` and `is_symlink = TRUE`.
     - In follow mode (`!(flags & G_FILE_QUERY_INFO_NOFOLLOW_SYMLINKS)`), GIO then calls `g_local_file_stat(path, ...)` (`:1982`).
     - This follow-stat fails (`res == -1`, with `ENOENT` for dangling targets or `ELOOP` for loops).
     - GIO handles this failure cleanly at line 1994: `else symlink_broken = TRUE;`.
   - In `get_content_type` (`:1308-1310`):
     ```c
     if (is_symlink && (symlink_broken || (flags & G_FILE_QUERY_INFO_NOFOLLOW_SYMLINKS)))
       return g_content_type_from_mime_type ("inode/symlink");
     ```
   - **Empirical Oracle Verification**: Running `/usr/bin/gio info -a standard::content-type` against a dangling symlink or a symlink loop (`loop -> loop`) exits 0 and prints:
     ```
     attributes:
       standard::content-type: inode/symlink
     ```
2. **The Contradiction in the Wave Artifacts**:
   - `claims-declaration-r97.md:58` asserted:
     > *"a path that cannot be stat'ed at all (missing, or a symlink loop) is outside the surface: the tool prints MADO_FILETYPE: ERROR stat for that path and exits 2 (the same refusal gio info makes), and no case scores it."*
   - In the in-wave draft `.ufo/waves/round-97/build/mado-filetype.py` (lines 96–105), `_stat_branch` implements:
     ```python
     st = os.lstat(path)
     mode = st.st_mode
     if stat.S_ISLNK(mode):
         if follow:
             st = os.stat(path)
             mode = st.st_mode
         else:
             return "inode/symlink"
     ```
   - When `follow=True` and `path` is a broken symlink or a symlink loop:
     `os.stat(path)` raises `FileNotFoundError` (for broken links) or `OSError: [Errno 40] ELOOP` (for loops).
     Because `_stat_branch` does not catch this `OSError`, it propagates to `main()`, which catches it as `except OSError:` and outputs:
     `MADO_FILETYPE: ERROR stat path=...` with exit code 2!
   - This directly breaks case classes `brok` and `sym`, causing the candidate to falsely refuse cases where the oracle emits `inode/symlink`!

#### Contradiction 2: C2 Registry Baseline Drift (0 → 4 vs 1 → 4)
As proven by `R97MReviewC2` (§1):
- `claims-declaration-r97.md:121,141` claims `SKILL.md` holds 0 rows for the four round-96 artifacts and that the count moves `0 → 4`.
- In reality, at base revision `e6152b58`, `SKILL.md` line 887 already carries a probe row for `tools/mado-mimetext.py`.
- The actual baseline row count is **1**, and the true landing delta is **1 → 4** (or 0 → 3 if restricted to the three missing rows).
- Furthermore, the C2 counting command lacks `--base-rev`, making a runtime before/after delta calculation impossible without hardcoding a literal that contradicts reality.

---

### 5.2 Affected Axes
- **`coverage` (C1)**: Resolves the symlink loop / broken symlink handling in `tools/mado-filetype.py` to match GLib 2.90.1 oracle truth, ensuring exact fidelity across `brok` and `sym` classes.
- **`operability` (C2)**: Pre-aligns the C2 counter to derive registry row changes dynamically or verify the 3 unregistered artifacts, avoiding false baseline verification failures.
- **Harms no axis**: Maintains 100% adherence to all frozen contracts and allows all 15 C1 classes to evaluate cleanly.

---

### 5.3 Proposed Move (Bounded Synthesis)

We propose a unified, two-sided resolution for the L1 integrator:

1. **For C1 (`tools/mado-filetype.py`)**:
   Implement GIO's exact two-stage stat model in `_stat_branch`:
   ```python
   def _stat_branch(path, follow):
       st = os.lstat(path)
       mode = st.st_mode
       if stat.S_ISLNK(mode):
           if not follow:
               return "inode/symlink"
           try:
               st = os.stat(path)
               mode = st.st_mode
           except OSError:
               # Target is dangling or a symlink loop: glocalfileinfo.c:1309 (symlink_broken=TRUE) -> inode/symlink
               return "inode/symlink"
       if stat.S_ISDIR(mode):
           return "inode/directory"
       if stat.S_ISCHR(mode):
           return "inode/chardevice"
       if stat.S_ISBLK(mode):
           return "inode/blockdevice"
       if stat.S_ISFIFO(mode):
           return "inode/fifo"
       if stat.S_ISREG(mode) and st.st_size == 0:
           return "application/x-zerosize"
       if stat.S_ISSOCK(mode):
           return "inode/socket"
       return None
   ```
   *Consequence*: `ERROR stat` exit 2 is reserved strictly for paths where `os.lstat` itself fails (true `ENOENT` for missing files, or `loop/child` path traversal failures), exactly matching `gio info` error behavior.

2. **For C2 (`quality/counters/c2-r97-counter-selftest.py`)**:
   - Reconcile the registry verification clause to derive the registry count dynamically from `--base-rev` (1 row) to `--rev` (4 rows), or assert the addition of the 3 unregistered artifacts (`quality/counters/c1-r96-magictext.py`, `quality/counters/c2-r96-selftest-kills.py`, `quality/selftest-kills/check-receipt-presence.json`).
   - Treat `quality/tool-ledger.md` coverage as an invariant ("population 188 -> 188, uncovered 0") rather than an un-derivable delta.

---

### 5.4 Risks and Mitigations

- **Risk**: Touching `mado-filetype.py` directly during the wave could conflict with `R97MExecToolC1`'s in-progress work.
  - *Mitigation*: This move is submitted as a bounded architectural synthesis in this report for the L1 integrator (`MadoR97`) and `R97MExecToolC1`. No candidate code is mutated by this seat.
- **Risk**: Test fixtures for `sym` or `brok` might assume `ERROR stat` exit 2.
  - *Mitigation*: The oracle for all cases is `/usr/bin/gio`. Since `gio info` outputs `inode/symlink` exit 0 on broken symlinks and symlink loops, fixing `_stat_branch` aligns the candidate with the oracle labels.

---

### 5.5 Verification

The synthesis was verified by executing isolated read-only probes against the system oracle `/usr/bin/gio`:
1. **Broken Symlink**: `broken -> nowhere`
   - `gio info -a standard::content-type broken` → `rc=0`, `standard::content-type: inode/symlink`
2. **Symlink Loop**: `loop -> loop`
   - `gio info -a standard::content-type loop` → `rc=0`, `standard::content-type: inode/symlink`
3. **Child of Symlink Loop**: `loop/child`
   - `gio info -a standard::content-type loop/child` → `rc=2`, `Error when getting information for file: Too many levels of symbolic links`
4. **Zero-Byte File with Name Match**: `empty.png` (0 bytes)
   - `gio info -a standard::content-type empty.png` → `rc=0`, `standard::content-type: application/x-zerosize` (proves stat branch precedes name lookup).

---

## 6. Execution and Host Guard Compliance

- **CWD**: Fleet root `/home/vgpnk/Projects/shokunin` maintained for all operations.
- **Scratch**: Cleaned scratch directory `$HYAKU_SCRATCH/mado-r97/R97MConnector` utilized and purged before yield.
- **Write Scope**: Wrote strictly to assigned file `.ufo/waves/round-97/w1/R97MConnector.md`. No fleet, sibling, tools, quality, git index, or jj state was modified.
- **Read-Only Invariant**: All probes executed were read-only; no services restarted, no host packages mutated, no compositor state changed.
