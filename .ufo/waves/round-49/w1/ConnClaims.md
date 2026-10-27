# ConnClaims — Cross-Claim Pre-Freeze Checklist & FSD Synthesis (Round 49, Wave w1)

- **Seat:** `ConnClaims` (UFO-FSD connector, leaf member)
- **Lane:** `mado-shokunin` (desktop and compositor craft: Hyprland, waybar, walker, terminal config plane)
- **Base:** `03e4ae76aff7a4be59cb69970dd553baa319695a` (round-48 closure tip)
- **Lane HEAD:** `5f37c1b87b3ce5e438d19284e32b2e46fd548a92` (round-49 setup commit)
- **Status:** Complete.
- **Detailed Report:** See `.ufo/waves/round-49/w1/ConnClaims/report.md` for full breakdown.

---

## 1. Executive Summary & Context

Round 49 advances two complementary claims:
- **C1 — Operability (Capability Acquisition):** `tools/mado-keysym.py`, answering which physical key, layout, level, and modifier masks type a keysym under a compiled keymap, verified byte-for-byte against the pinned `xkbcli-how-to-type` (libxkbcommon 1.13.2-1).
- **C2 — Coverage (Sourced Knowledge):** `corpus/knowledge/hyprland-bind-key-match-r49.md`, documenting how Hyprland 0.56.2 (commit `efb50993`) matches key events against configured `bind = MODS, KEY, dispatcher, arg` rules, supported by newly opened SOURCES rows `S352`..`S361`.

In accordance with round policy, **nothing freezes in wave w1**. The L1 integrator freezes predicates, counters, fixtures, pins, references, controls, and base receipts in `registration.md` after wave w1 returns, and wave w2 attacks the frozen instruments.

This report delivers:
1. The **Pre-Freeze Checklist** defining the mandatory contents of the freeze commit.
2. The **Separability Proofs** establishing that C1 and C2 can be independently verified and falsified.
3. The **Closure Defect Prevention Matrix** resolving recurring defects from round 48 (post-freeze narrowing, unreceipted numbers, mislabelled receipt fields, dropped matrix rows, host writes, cut controls, attach noise, and recipe size cap limits).
4. The **UFO-FSD Connector Synthesis**: finding a non-obvious operational move linking C1's XKB level output to C2's Hyprland translation state without creating contract coupling.

---

## 2. Pre-Freeze Checklist for Round 49

The freeze commit (committed by L1 before wave w2 dispatch and before any data commit) must contain all of the following:

### 2.1 Counters
1. **C1 Counter:** `quality/counters/c1-r49-keysym.py` (derived from `w1/ExecCounterC1/c1-r49-keysym.py`).
   - Clauses:
     * `t`: Tool is a regular blob at `REV` (`tools/mado-keysym.py`).
     * `s`: Tool self-checks (`--selftest` exits 0 with `MADO_KEYSYM_SELFTEST: N/N passed`, $N \ge 25$; documented refusals without `--disable-compose` or `--keysym` exit 2).
     * `f`: Scored fixtures (633 cases) compiled with pinned `compile-keymap` in clean env, judged against pinned `how-to-type`; stdout bytes and exit code must match.
     * `g`: Nonce-generated cases (60 cases) compiled and judged at count time.
     * `r`: Read-only / execution sandbox tripwire via `strace` (no subprocess, no socket, no file writes; only selftest tmpfs writes permitted).
     * `i`: Bubblewrap isolation mount allowlist: clean root, Python runtime only (no host `xkbcli` or `libxkbcommon` binaries/libraries visible to tool).
   - Execution rule: Refuses `--work` under `/tmp`, `/var/tmp`, `/dev/shm`, inside repository, or in real operator home (`SentScratch`, QUALITY 95).
2. **C2 Counter:** `quality/counters/c2-r49-bind-entry.py` (derived from `w1/ExecCounterC2/c2-r49-bind-entry.py`).
   - Clauses:
     * `a`: Entry absent at `BASE`, present at `REV`.
     * `b`: Provenance header within first 20 lines ($\ge 3$ `source: S###` rows $\ge S352$, `verified-at: 2026-10-27`, valid `recheck:`); 11-column registry rows in `corpus/SOURCES.md`; `corpus/README.md` index row covering all cited rows.
     * `c`: Pins mode 100644 under `.ufo/waves/round-49/fetch/`, matching sha256 digests in SOURCES rows; ref-pinned URLs (`efb50993`, `d1442aaa`, `d5f07c60`).
     * `d`: Quoted spans (2–25 words) match verbatim inside pin line ranges.
     * `e`: $\ge 6$ numbered chain steps, each with pin locators within line bounds.
     * `f`: Live receipt answers entry: matches `hyprctl binds -j` (192 binds, 4 form counts summing to total), version 0.56.2 commit `efb50993`, and `input:resolve_binds_by_sym` = `int 0` (`set false`).
     * `g`: Held ground row `S319` cited, byte-equal to base, not re-registered.

### 2.2 Fixtures
- **C1 Fixture Set:** `quality/counters/c1-r49-fixtures.json` (committed bytes, sha256 pinned in counter and `registration.md`).
- **Census from `w1/ExecFixtures`:**
  * Total cases: 633 cases across 27 distinct RMLVO configurations.
  * Sha256: `80fd778adb5e72430158a51c29e713b6ffb203c75a7eda2cba57b1339d9a4547` (303,537 bytes).
  * 17 distinct classes: `ABSENT` (15), `BIND` (58), `CASE` (27), `DEAD` (27), `DIGITS` (18), `FUNCTION` (59), `HOST` (55), `INVALID` (20), `KEYPAD` (25), `LETTERS` (40), `MODIFIER` (16), `MULTI` (58), `NUMERIC` (21), `OPTIONS` (51), `PUNCT` (38), `VARIANT` (81), `XF86` (24).
  * Exit code breakdown: 581 `rc=0`, 52 `rc=2`.
  * Multi-key level coverage: 496 cases have $\ge 1$ output row; 180 cases have $\ge 2$ output rows; 137 cases have 0 rows (valid keysym but untypable in that layout).

### 2.3 Pins
Upstream source pins committed under `.ufo/waves/round-49/fetch/` (mode 100644) with exact sha256 hashes matching `corpus/SOURCES.md`:
1. `xkbcli-how-to-type`: sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`.
2. `xkbcli-compile-keymap`: sha256 `43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250`.
3. `/usr/include/xkbcommon/xkbcommon-keysyms.h`: sha256 `13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3`.
4. libxkbcommon 1.13.2 sources (commit `d1442aaa6b635551182e83c3b55037f4c118c962`):
   - `src/keysym.c` (sha256 `123e3390...`, S355)
   - `src/ks_tables.h` (sha256 `6960e7e4...`, S356)
   - `tools/how-to-type.c` (sha256 `f774882e...`, S357)
   - `include/xkbcommon/xkbcommon-keysyms.h` (sha256 `13023369...`, S358)
5. Hyprland 0.56.2 sources (commit `efb50993780079460b0cbed1363e2166a2de1d9f`):
   - `src/managers/KeybindManager.cpp` (sha256 `558fb695...`, S352)
   - `src/config/legacy/ConfigManager.cpp` (sha256 `9db68cf4...`, S353)
   - `src/managers/input/InputManager.cpp` (sha256 `feedf32e...`, S354)
6. Hyprland wiki pins (commit `d5f07c60e16fe03744aabb76e492117b7f7c4679`):
   - `content/Configuring/Basics/Binds.md` (sha256 `3d8a2a68...`, S359)
   - `content/Configuring/Basics/Variables.md` (sha256 `3b3bb219...`, S360)
7. Held ground:
   - `IKeyboard.cpp` (commit `efb50993`, held row S319 from round 46, cited never re-registered).
8. Live receipt:
   - `receipt-hyprctl-binds-r49.txt` (sha256 `3dc5de54479a04365cc2263a8a7db612108c7824538a105090c55c0c078db1d8`, S361).

### 2.4 References
- Candidate tool reference docstring in freeze: `mado-keysym.py` docstring establishing exact command arguments, exit codes, and out-of-contract classes (compose sequences, character codepoint interpretation, raw XKB sources with includes).
- Candidate entry draft: `l1-draft/hyprland-bind-key-match-r49.md` carrying 6-step chain, quotes, and receipt bindings.

### 2.5 Controls
**Mandatory rule from M48-9:** Every control MUST be scored on the frozen fixture set BEFORE the freeze commit, and every control must evaluate to `TARGET_MISSED`. Zero controls may be marked `cut`.
1. **C1 Controls (16 tools in `ExecControlsC1/controls/`):**
   - `c01-absent`: tool file missing (exit 2).
   - `c02-header-only`: prints `keysym:` header, no rows.
   - `c03-first-match-only`: prints only the first matching keycode row.
   - `c04-no-modifiers`: omits modifier mask column.
   - `c05-exec-xkbcli`: cheats by executing the host `xkbcli` binary (trips clause `r`/`i`).
   - `c06-cache-table`: hardcodes precomputed table of first 100 keysyms.
   - `c07-read-fixture-repo`: reads host `/usr/share/X11/xkb`.
   - `c08-writes-file`: writes diagnostic file (trips clause `r`).
   - `c09-opens-socket`: opens AF_UNIX socket (trips clause `r`).
   - `c10-overfit`: handles only `br` layout.
   - `c11-selftest-only`: passes `--selftest`, fails on fixture keymaps.
   - `c12-rc-blind`: always exits 0, even on invalid keysyms (rc 2).
   - `c13-hardcoded-br`: outputs hardcoded `br` rows for any layout.
   - `c14-stderr`: writes errors to stderr instead of stdout.
   - `c15-layout1-only`: checks layout 0 only in multi-layout keymaps.
   - `c16-always-unreachable`: reports all keysyms as 0 rows.
2. **C2 Controls (13 bundles in `ExecControlsC2/controls/`):**
   - `01-do-nothing`: absent entry.
   - `02-stub-head-one-sentence`: header only, one body sentence.
   - `03-paste-r46-verbatim`: pastes round-46 keybind text.
   - `04-paste-r46-paraphrased`: paraphrased round-46 text without locators.
   - `05-quote-forged-one-word`: one word altered in a cited pin quote.
   - `06-locator-off-by-one`: quote locator line shifted by 1.
   - `07-steps-without-locators`: 6 steps without pin locators.
   - `08-branch-url-pin`: row uses `main` branch URL instead of commit.
   - `09-digest-edited-row-file`: row digest does not match pin bytes.
   - `10-receipt-typed-by-hand`: receipt values do not match live `hyprctl`.
   - `11-receipt-accurate-handtyped`: receipt typed without command proof.
   - `12-held-s319-reregistered`: re-registers `IKeyboard.cpp` under new S-number.
   - `13-registry-row-unused`: registers S362 but never cites it in entry.

### 2.6 Base Receipts
Committed under `.ufo/waves/round-49/receipts/`:
- `c1-before-base.txt`: `PRED-C1-r49` run at base `03e4ae76` -> `verdict=TARGET_MISSED` (tool absent, exit 2).
- `c2-before-base.txt`: `PRED-C2-r49` run at base `03e4ae76` -> `verdict=TARGET_MISSED` (entry absent, rows absent).
- `axis-before-base.txt`: `python3 quality/check-axes.py` -> `checked=3 mismatched=0` (operability, coverage, calibration).
- `operator-state-before.txt`: sha256 digests of operator-owned paths (`~/.cache/xdg-terminal-exec`, `~/.config/hypr/hyprland.conf`, etc.) taken before wave writers run.
- Harm-watch historical counter runs at base:
  * `PRED-C1-r48-v2`: `warm=228/228 TARGET_MET`.
  * `PRED-C2-r48-v2`: `admitted=1/1 TARGET_MET`.
  * `PRED-C1-r47`: `TARGET_MET`.
  * `PRED-C2-r45-v2`: `TARGET_MET`.

---

## 3. Separability Proofs

To satisfy UFO-FSD protocol, C1 and C2 must be independently verifiable and falsifiable:

$$\text{Separable}(C_1, C_2) \iff \Big(\forall \Delta C_1, \, \text{Score}(C_2) \text{ unchanged}\Big) \land \Big(\forall \Delta C_2, \, \text{Score}(C_1) \text{ unchanged}\Big)$$

### 3.1 Input & Dependency Independence
| Attribute | Claim C1 (Operability) | Claim C2 (Coverage) | Overlap |
|---|---|---|---|
| **Scored Artifact** | `tools/mado-keysym.py` | `corpus/knowledge/hyprland-bind-key-match-r49.md` | **None** (Disjoint paths) |
| **Ground Truth / Judge** | Pinned `xkbcli-how-to-type` binary | Pinned Hyprland/libxkbcommon git commits (`efb50993`, `d1442aaa`) | **None** (Binary vs Source tree) |
| **Fixtures / Data** | `quality/counters/c1-r49-fixtures.json` | `corpus/SOURCES.md`, `receipt-hyprctl-binds-r49.txt` | **None** (Disjoint files) |
| **Runtime Environment** | Bubblewrap sandbox with Python stdlib only | Host Python AST / regex locator verifier | **None** |
| **Corpus Citations** | None (`tools/` contains no knowledge notes) | Cites S352..S361 and held S319 | **None** |

### 3.2 Falsification Isolation
- **Hypothetical C1 Failure:** If `tools/mado-keysym.py` is deleted, fails selftest, or misparses keymaps, `PRED-C1-r49` outputs `TARGET_MISSED`. `PRED-C2-r49` does not read `tools/` or execute `mado-keysym.py`; `PRED-C2-r49` continues to evaluate `admitted=1/1 TARGET_MET`.
- **Hypothetical C2 Failure:** If `corpus/knowledge/hyprland-bind-key-match-r49.md` is corrupted, has invalid pin locators, or fails quote checks, `PRED-C2-r49` outputs `admitted=0/1 TARGET_MISSED`. `PRED-C1-r49` reads only the tool and compiled keymap fixtures in a clean sandbox; `PRED-C1-r49` continues to evaluate `TARGET_MET`.

---

## 4. Recurring Closure Defect Prevention Matrix

Mined from `corpus/lessons/round-48-verifier-spotcheck.md`, `registration-v2.md`, and `QUALITY.md` (criteria 91–99 + candidate 100–104):

| Defect ID | Historical Incident & Root Cause | Prevention Mechanism for Round 49 | Verifying Instrument |
|---|---|---|---|
| **Post-Freeze Narrowing** | **M48-1:** C1 reference docstring froze 6 out-of-contract classes; delivered tool added 3 new refusals (HOME unset, FIFO, symlink loops) post-freeze. | Freeze the complete refusal list in the candidate docstring. Enforce zero undeclared refusals before data commit. | `quality/check-landed-contract.py` (QUALITY 96) |
| **Unreceipted Numbers** | **M48-2, M48-11:** Report/lesson transcribed `findings=128`, `222 warm fixtures`, and false "L0 question" by hand instead of deriving from tool. | Prohibit hand-typed numbers in report/lesson. Every count/digest must be emitted by an automated command reading committed receipts. | `quality/check-round-report.py` (QUALITY 10, 94) |
| **Mislabelled Receipt Field** | **N2:** `host_cache_untouched_sha256` in round-48 receipt was named "untouched" but held the 7-byte mutant payload `printf 'r48-w2\n'`. | Forbid state-asserting names (`untouched`, `clean`) unless paired with an explicit `_before` and `_after` comparator showing equality. | Candidate Criterion 101 (`w1/ScrQuality/check101-fieldname.py`) |
| **Dropped Text Matrix Rows** | **N4:** Summary JSON contained 98 mutation variants; text matrix printed only 96 rows (missing 2 base-scoring rows). | Generator script must assert `len(text_rows) == len(json_rows)` and verify total projection. | Candidate Criterion 102 (`w1/ScrQuality/check102-textprojection.py`) |
| **Host State Mutation** | **M48-10:** Unsandboxed w2 mutant executed with ambient `$HOME` and wrote to operator's `~/.cache/xdg-terminal-exec`. | All mutant and probe runs must be wrapped by `hostguard.py` (redirecting HOME/XDG_* to scratch and asserting before/after operator digest match). | Candidate Criterion 100 (`w1/ScrQuality/check100-hostwrite.py`) |
| **Freeze Before Controls** | **M48-9:** Round 48 froze v1 instruments with 11 of 20 controls marked `cut`, allowing `writes-cache` cheat to meet target. | Gate rule: 100% of controls (16 for C1, 13 for C2) must be scored and confirmed `TARGET_MISSED` before freeze commit. | Pre-freeze control test runner (`drive.py`) |
| **Flaky strace / Attach Noise** | **M48-7, M48-12:** `PRED-C1-r48` strace parser counted bwrap attach lines (`??? (<detached ...>)`) and split execve as unauthorized writes/forks. | Parser pre-filters bwrap runtime noise before checking syscall boundaries. Tested over 5 repeated runs. | Clause `r` parser verification in `c1-r49-keysym.py` |
| **Cap vs Clone Incompatibility** | **M48-13:** Dispatch enforced `ulimit -f 2048` (1 MiB), breaking `git clone --shared` because repo has tracked files > 1 MiB. | Dispatches use `ulimit -f 65536` (64 MiB); clone recipes use `--no-checkout` / archive extraction. | Candidate Criterion 104 (`w1/ScrQuality/check104-caprecipe.py`) |
| **Session Material Gate Blindness** | **M48-8:** Session material gate scanned `.ufo/` only, missing 16 of 19 synthetic `/home/<user>` shapes in other directories. | Expand gate scope to repository-wide (`--scope all`), update waiver registry, and eliminate unstated defaults. | Candidate Criterion 103 (`w1/ScrQuality/check103-envelope.py`) |

---

## 5. UFO-FSD Connector Synthesis: The Level-1 Unshifted Reachability Filter

### 5.1 Evidence & First-Order Observations
1. **From C1 Tooling (`xkbcli how-to-type` & `mado-keysym.py`):**
   - Given a compiled keymap, `how-to-type` outputs every keycode, layout, level, and modifier mask that can produce a keysym.
   - Example on host `br` keymap (`symbols/br`):
     * Physical key `AB11` (slash key) produces `slash` at **Level 1** (unshifted, mask `[ ]`).
     * Physical key `AD01` (`Q` key) produces `slash` at **Level 3** (AltGr, mask `[ Mod5 LevelThree ]`) and **Level 4** (Shift+AltGr, mask `[ Shift Lock Mod5 LevelThree ]`).
2. **From C2 Sourced Code (Hyprland 0.56.2 `KeybindManager.cpp`):**
   - In `KeybindManager.cpp:369`:
     ```cpp
     const xkb_keysym_t keysym = xkb_state_key_get_one_sym(
         pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState,
         KEYCODE);
     ```
   - In `KeybindManager.cpp:332`: `m_xkbTranslationState = xkb_state_new(PKEYMAP);`
     `m_xkbTranslationState` is initialized with zero modifiers and layout index 0, and is **never updated with modifier state**.
   - In `IKeyboard.cpp:382`: `xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, group);`
     `m_xkbSymState` updates layout index (`group`), but all modifier masks are **explicitly set to 0**.
   - In `KeybindManager.cpp:652`:
     ```cpp
     if (!IGNORECONDITIONS && ((modmask != k->modmask && !k->ignoreMods) || ...))
         continue;
     ```
     Modifier matching requires **exact equality** with the depressed modifier mask `modmask` (from `InputManager.cpp:1711` `MODS.depressed`).
   - In `KeybindManager.cpp:710-724`:
     Hyprland compares `key.keysym` against `xkb_keysym_from_name(k->key, NO_FLAGS)` and `xkb_keysym_from_name(k->key, CASE_INSENSITIVE)`.

### 5.2 The Contradiction Across Runtime Surfaces
A practitioner configuring Hyprland who relies naively on `how-to-type` (C1) will expect that because `slash` can be typed via AltGr+Q (`AD01 level 3`), a bind defined as:
```ini
bind = SUPER, slash, exec, foot
```
could be triggered by pressing `SUPER + AltGr + Q`.

**In Hyprland runtime, this bind will NEVER fire on `AD01`:**
1. When `SUPER + AltGr + Q` is pressed, physical keycode is `AD01`.
2. Hyprland queries `m_xkbTranslationState` (or `m_xkbSymState`) at keycode `AD01`. Because translation state has zero modifiers active, it retrieves **Level 1 (unshifted)**, which is `q`, NOT `slash`!
3. Hyprland compares `key.keysym` (`q`) against bind target `slash` $\to$ **Mismatch**.
4. Furthermore, depressed modifiers include `Mod5` (AltGr) $\to$ `modmask` is `SUPER | Mod5`, whereas `k->modmask` is `SUPER` $\to$ **Mismatch**.

### 5.3 The Proposed Move
**Synthesize C1 and C2 by incorporating the "Level-1 Unshifted Reachability Filter" into the verification and documentation plane:**

1. **In C2 Knowledge Entry (`hyprland-bind-key-match-r49.md`):**
   Formally define the **Bind Reachability Law**:
   > *A keysym is directly bindable as a bare keysym (`bind = MODS, KEY`) if and only if it exists at **Level 1 (unshifted)** on a physical key in layout 0 (or in the active layout when `resolve_binds_by_sym=true`). Keysyms present only at Level $\ge 2$ (shifted, AltGr) are unreachable as bare keysyms; they must be bound either by explicitly including the shifting modifier in `MODS` (e.g. `SUPER SHIFT, 7` for `/` on German keyboards) or by using raw keycodes (`bind = MODS, code:NN`).*

2. **In C1 / C2 Join Demonstration (`ExecBindsLive`):**
   The live join demo categorizes all 192 binds on the host into:
   - **Level-1 Direct Reachable:** (e.g. `SUPER, Return` $\to$ `RTRN level 1`; `SUPER, slash` $\to$ `AB11 level 1`).
   - **Keycode Direct:** (42 binds with empty key field, matching raw hardware keycodes).
   - **Level $\ge 2$ Unreachable via Bare Sym:** (keysyms that require explicit modifier folding).

3. **In Pre-Freeze Contract Integrity:**
   Ensure C1 does *not* filter its own output: `mado-keysym.py` MUST remain 100% faithful to `how-to-type` (emitting all levels). The Reachability Filter belongs to the join documentation (C2) and operator tooling layer, preserving strict separability between the C1 tool contract and the C2 compositor knowledge.

### 5.4 Risks & Second-Order Effects
- **Risk:** Conflating `mado-keysym.py`'s contract with Hyprland's bind model could lead to breaking C1's parity judge.
- **Mitigation:** C1's judge is exclusively pinned `xkbcli-how-to-type`. The reachability synthesis is documented in C2 and verified in the live receipt join, keeping C1 counter clauses untouched.
- **Second-Order Benefit:** Prevents user configuration bugs on multi-layout and non-US keyboard configurations (such as Brazilian ABNT2 and European layouts) where common symbols reside on levels 2, 3, or 4.

### 5.5 Verification
- Live receipt `receipt-hyprctl-binds-r49.txt` demonstrates that on the host's 192 binds, 0 binds attempt to use unreachable Level $\ge 2$ bare keysyms without keycodes or explicit shift modifiers.
- C1 fixture set `fixtures.json` (633 cases) verifies both single-row (level 1) and multi-row (levels 2, 3, 4) keysyms, confirming that the tool correctly distinguishes shift levels across 27 RMLVO configurations.

---

## 6. Conclusion & Handoff to Integrator

All deliverables for seat `ConnClaims` are complete:
- Pre-freeze checklist is fully specified and grounded in local repository bytes.
- Separability between C1 and C2 is formally established.
- All recurring defects from round 48 are addressed with concrete, automated prevention mechanisms.
- The FSD synthesis provides a non-obvious operational bridge connecting C1's capability to C2's domain model without violating contract boundaries.
