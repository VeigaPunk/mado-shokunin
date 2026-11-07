# R93MConnector — Sibling Overlap, Assimilation, considerthese, Cross-Domain Evidence, and Survivor Ledger (mado round 93, w1)

Seat: `R93MConnector` (connector). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round 93, ONE v1 wave `w1`, base `4c6f723f3dca3a26f9d14475d695fe797e2e972c` (master).
Scratch root: `S=/fast/scratch/hyaku/mado-r93/R93MConnector` (used and removed on exit).
No pacman transactions, no background processes kept, no mutating git/jj commands anywhere.
All draft executions are labelled **DRAFT**; no measurement receipts were written.

**Axes named:**
- **C1 coverage (edge class):** GKeyFile byte-class compliance in `tools/mado-portals.py` for `xdg-desktop-portal 1.22.1` configuration (`portals.conf`) and backend selection (`.portal` files).
- **C2 operability:** `quality/check-selftest-strength.py` gate failing (WEAK rc 1) when a passing selftest assertion of `quality/check-seat-reports.py` (23 checks) is weakened.

---

## 1. Sibling-overlap scan — no sibling owns the GKeyFile or portal plane

A read-only scan of all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `mado-shokunin`) was conducted:
1. `git -C <lane> log --oneline -30` filtered for `keyfile|gkeyfile|key-file|xdg-desktop-portal|portal|selftest|strength|mutation|kill-set`.
2. `grep -rn -iE 'GKeyFile|gkeyfile|xdg-desktop-portal|selftest-strength' <lane>/corpus/knowledge`.
3. `grep -rn -iE 'GKeyFile|gkeyfile|xdg-desktop-portal' <lane>/tools/`.
4. `grep -rn -iE 'glib|gkeyfile|portal|xdg-desktop-portal|selftest|surrogateescape' <lane>/PROVINCE.md`.

### Sibling findings

| Lane | Path | Commit / Context | Interpretation | Cite vs Route? |
|---|---|---|---|---|
| `souji-shokunin` | `corpus/knowledge/origin-record-format-gvfs-r40.md:10` | `128e412b` (round 40) | Mentions GVFS trash reader parsing `.trashinfo` origin records as a GKeyFile with one group (`[Trash Info]`) and two keys (`Path`, `DeletionDate`). | **Neither.** Archival note only; souji has no GKeyFile parser, tool, or GLib byte model. |
| `tsukuroi-shokunin` | `corpus/knowledge/journal-boot-plane.md:130,161`<br>`corpus/knowledge/systemd-user-plane.md:20,22`<br>`corpus/knowledge/kill-event-deep-r8.md:47,78` | `780bad66` / `aa110cc5` (round 76)<br>`c0f6303f` (round 18) | Log captures of running systemd user units where `xdg-desktop-portal` and `xdg-desktop-portal-gtk` emit journal records (`Failed to load RealtimeKit property`). | **Neither.** Tsukuroi monitors service lifecycle and ALPM update safety; it does not parse portal configs or route backends. |
| `kotoba-shokunin` | `verifiers/fixtures/round-100/selftest-kills.py`<br>`verifiers/fixtures/round-99/selftest-kills.py` | `d1e1170` (round 100)<br>`c0489d1` (round 99) | Meta-testing instrument (`selftest-kills.py` v6.2) verifying that verifier `--self-test` detects mutations in the instrument itself (comment/code decoys, source-blind runs, mirror runs, git-less trees). | **Cite for methodology in C2.** Sibling maintains active selftest-kill methodology, but applies it strictly to its own verifiers. Mado should cite its isolation rules (fresh scratch, minimal env) as supporting evidence. No routing. |
| `kumitate-shokunin` | `scripts/round-gate.mjs` | `b0084b20`–`2cba824a` (rounds 94–96) | Gating selftest arms against surviving mutants in `round-gate`. | **Neither.** Private to kumitate harness. |
| `tameshi-shokunin` | Historical cold-read traces | Rounds 6, 9, 21, 25 | Historical cross-lane verification. No active checks on mado's seat-reports gate. | **Neither.** |

**Summary:** No sibling lane owns, develops, or gates GKeyFile parsing, xdg-desktop-portal configuration, or seat-report selftest-strength verification.

---

## 2. Assimilation — shokuknow merge review & ID collision check

A read-only inspection of `/home/vgpnk/Projects/shokuknow/merge/mado/` was conducted:
- **Plane scan:**
  - `gkeyfile`: **0 matches** across `MERGE-REPORT.md`, `MERGE-REPORT.json`, `SOURCES.append.md`, and `knowledge/`.
  - `portal`: Staged rows `S328`, `S329`, `S332`, `S338` and knowledge notes (`focus-grab-protocol-live-on-host-r14.md`, `focus-grab-has-no-client-here-r15.md`, `idle-lock-runtime-state-r28.md`) document Wayland compositor focus-grab / EIS interface advertisement (`CPortalManager::onGlobal`) from rounds 14–28.
  - Zero staged entries or knowledge notes touch xdg-desktop-portal's backend selection, `portals.conf`, `.portal` files, or GLib GKeyFile byte-class parsing.
- **ID collision check:** Executed in `$S` using the canonical round prompt pattern `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort -u`:
  * `reg-ids`: **445** unique IDs (`S001`–`S510`; sha256 `080c8a4effbf2dce6dc68363b965c1ef05cf0e02e52f75ab5d06e6c543a18949`).
  * `staged-ids`: **147** unique IDs (`S203`–`S349`; sha256 `079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d`).
  * `collisions`: **94** exact ID collisions (`comm -12`; sha256 `18e1d089c96fd5f43af25a6a1c656cc296d5048192f08f1ffd6cc45ba5f82a5c`).
  * `gap-ids`: The remaining **53** staged IDs (`S222`–`S252`, `S254`–`S257`, `S259`–`S276`) fall into historical gaps strictly below the current registry maximum `S510`.
- **Recommendation: REJECT (do not admit).**
  * *Reason 1 (Collision severity):* 94 exact collisions with active, verified registry entries.
  * *Reason 2 (Below-max insertion):* The 53 non-colliding staged rows violate append-only integrity by backfilling below `S510`. Safe allocation requires starting above `S511`.
  * *Reason 3 (Relevance):* The package has zero overlap with Round 93 claims (C1 sources for GLib 2.90.1 are freshly sourced in S511 and re-opened S502).

---

## 3. considerthese — reflection alignment

Analysis of `considerthese/2026-11-06.md` (the latest reflection file; tip was `1ee8b669`):

| Proposal | Description | Status in Round 93 |
|---|---|---|
| **P4** | "Widen desktop coverage past bar + mako ... Still thin or absent in this window's knowledge names: window-rule live semantics beyond inventory, xdg-desktop-portal / screen-share (`xdph.conf`), clipboard, non-bar exclusive surfaces João actually runs, and hypridle volatility (long-standing UNK). Prefer one operator-config gap over another harness counter." | **Directly served by C1:** C1 deepens coverage on the `xdg-desktop-portal` configuration plane that Proposal 4 explicitly called out as thin/absent. In round 90, `tools/mado-portals.py` answered portal routing for the 21 interfaces but failed on GLib byte classes (invalid UTF-8 in comments, `\v` 0x0B whitespace rejection). Round 93 C1 ports GLib 2.90.1 GKeyFile byte-class rules into `tools/mado-portals.py`, transforming a fragile parser into a byte-accurate emulator of xdg-desktop-portal's actual config loader. |
| **P1** | "Carry a survivor ledger across quiet days" (tracking r87 mako mutants M03/M05/M06/M08/M10 and r86 forgeries). | **RESOLVED IN ROUND 88:** (See Section 5 below; all 5 mutants were killed in r88 C1 at `650e18bdf0ae`). |
| **P2** | "Always quote verdict before score" (`score_scope=finite-cases` on finite case sets). | **STAYS OPEN:** Round 93 counters output standard `TARGET_MET` / `DRAFT_TARGET_MET`. |
| **P3** | "Read-only live check of `mado-mako.py` against João's real theme files." | **STAYS OPEN:** Untouched; mako plane is not under review in round 93. |
| **P5** | "Verify QUALITY 145 has an instrument, not only a criterion" (gating on wave-done / null-seat). | **STAYS OPEN:** C2 builds `check-selftest-strength.py` for seat-report assertions, but wave-done gating remains a separate instrument. |
| **P6** | "Keep fetching LOG/SCORECARD by round header, not whole file." | **STAYS OPEN:** Ongoing operational reading discipline. |
| **P7** | "Ask João (via parent) for a decision on the tracked `eventq-live-ss.txt` receipts." | **STAYS OPEN:** Tracked historical receipts remain. |

---

## 4. Cross-domain evidence (round-92 spot-check routed defect 1)

Spot-check routed defect 1 (`corpus/lessons/round-92-verifier-spotcheck.md:168-169`) mandates naming cross-domain evidence encountered in its own item.

Round 93 materials touch three cross-domain areas:
1. **GLib 2.90.1 C library internals and ASCII classification table**:
   - Files: `glib/gkeyfile.c`, `glib/gstrfuncs.c` (`ascii_table_data`), `glib/gstrfuncs.h`.
   - Evidence: `g_ascii_isspace` does not treat vertical tab `0x0B` (`\v`) as whitespace; UTF-8 validation occurs in `g_key_file_get_string` / `get_string_list` when a key's value is queried, not during `g_key_file_load_from_data`.
   - Owning lane: **None.**
2. **Python `surrogateescape` error handler semantics (PEP 383)**:
   - Evidence: Raw bytes `0x80`..`0xFF` mapped to lone surrogates `U+DC80`..`U+DCFF` in string fixtures. Used to represent raw/invalid byte-class sequences in JSON fixtures.
   - Owning lane: **None.** Sweep across sibling `corpus/` and `tools/` shows `surrogateescape` is widely used as an I/O implementation detail across 8 sibling lanes (`chousa`, `game-dev-2d`, `kaidoku`, `kake`, `kama`, `kasegi`, `souji`, `tameshi`, `tsukuroi`), with `souji` documenting `codecs.html#error-handlers` (row S253), but no lane claims Python runtime semantics in PROVINCE.md.
3. **Test-mutation methodology (mutating test assertions to verify gate strength)**:
   - Evidence: `quality/check-selftest-strength.py` mutating `check-seat-reports.py`'s `--selftest` assertions to detect weakened checks.
   - Owning lane: **None.** `kotoba-shokunin` operates `selftest-kills.py` (v6.2 in round 100), but its domain is strictly internal verifier fixtures for kotoba.

### Sweep command and output
```bash
for p in /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md; do
    echo "=== Lane: $(basename $(dirname "$p")) ==="
    grep -in -E 'glib|surrogateescape|mutation-of-test|selftest-strength|meta-test' "$p" || echo "none"
done
```
Output:
All 20 sibling lanes returned `none`. Only `mado-shokunin` (lines 506, 519, 521, 523) references GLib in its own PROVINCE.md.
**Verdict: none** (no sibling lane owns any of the three cross-domain surfaces).

---

## 5. Survivor ledger (considerthese proposal 1)

Considerthese `2026-11-06.md` Proposal 1 noted 5 surviving mutants from Round 87 mako resolver (`tools/mado-mako.py`):
- `M03-relative-include-accepted`
- `M05-no-initial-mode`
- `M06-no-defaults`
- `M08-missing-input-matches`
- `M10-unterminated-quote-accepted`

Receipt and LOG search:
- **Round 87:** `c1-measured-r87.txt` at freeze `00c96721` reported TARGET_MISSED with 5 survivors: M03, M05, M06, M08, M10.
- **Round 88:** Freeze `9e36e3a3103349b939982e532feca443f02e660d`, measured commit `650e18bdf0ae404ec9a80874c4503ecf3237e8e6` (`LOG.md:4300-4320`).
- **Receipt evidence:** `.ufo/waves/round-88/receipts/c1-measured-A-r88.txt` lines 194–201:
  * `mutant M03-relative-include-accepted killed`
  * `mutant M05-no-initial-mode killed`
  * `mutant M06-no-defaults killed`
  * `mutant M08-missing-input-matches killed`
  * `mutant M10-unterminated-quote-accepted killed`
  *(Also verified in `.ufo/waves/round-88/receipts/c1-harm-at-B-r88.txt` lines 194–201).*
- **Conclusion:** All five mutants were **KILLED** in Round 88 C1 at commit `650e18bdf0ae404ec9a80874c4503ecf3237e8e6` (TARGET_MET 62/62, mutants 22/22 killed). They are **NOT open**. The note in `2026-11-06.md` reflected a window written before Round 88 landed.

---

## 6. Proposed move — non-obvious synthesis (UFO-FSD connector)

**Move: Equip `tools/mado-portals.py`'s built-in `--selftest` with hermetic byte-class assertions (advancing `checks=22` to `checks=26`), enabling `errors="surrogateescape"` in its test fixture writer, to explicitly assert the 4 ported GKeyFile byte behaviors before the L1 freeze.**

### Evidence
1. **Candidate selftest deficiency:** In candidate `build/mado-portals.c1.py`, `selftest()` (lines 480–550) was copied directly from round 90 and runs only 22 checks. All 22 checks pass identically on the base unported tool (`tools/mado-portals.py`).
2. **Proof of weakness by mutation:**
   - Mutant A (reverting `ASCII_SPACE = " \t\n\f\r"` to include `\v`): candidate `--selftest` still outputs `checks=22 failed=0 exit 0`.
   - Mutant B (reverting `open(path, "rb") ... decode("utf-8", "surrogateescape")` back to strict `open(path, "r", encoding="utf-8")`): candidate `--selftest` still outputs `checks=22 failed=0 exit 0`.
   The candidate's own unit test is blind to the candidate's core capabilities.
3. **Fixture writer bug in selftest:** In `mado-portals.c1.py`'s `selftest():run()`, fixtures are written with `open(os.path.join(d, k), "w", encoding="utf-8")`. Any test fixture containing lone surrogates (`\udc80`..`\udcff`) throws `UnicodeEncodeError` unless `errors="surrogateescape"` is passed.
4. **Cross-claim synthesis (C1 meets C2):** Round 93 C2 establishes `quality/check-selftest-strength.py` specifically to address round-92 routed defect 3: *"a weakened passing selftest assertion is invisible to the counter's selftest leg"*. Applying this exact doctrine to C1 ensures that `tools/mado-portals.py`'s `--selftest` actively guards its ported GKeyFile byte capabilities against regression.

### Affected axes
- **C1 coverage (edge class):** **IMPROVES.** Edge-class byte handling becomes part of the tool's hermetic unit contract, testable in 0.04s without external D-Bus or bwrap sandboxes.
- **C2 operability:** **IMPROVES / NO HARM.** Demonstrates selftest-strength discipline in the tool layer, aligning tool testing with the lane's new selftest-strength gate. Harm watch in `SCORECARD.md` advances from `tools/mado-portals.py 22/22` to `26/26`.

### Implementation details (for L1 MadoR93 at freeze)
1. In `tools/mado-portals.py`:
   - In `selftest():run()`: update file writer:
     ```python
     with open(os.path.join(d, k), "w", encoding="utf-8", errors="surrogateescape") as fh:
         fh.write(v)
     ```
   - In `selftest()`: append four checks:
     ```python
     # 4 byte-class assertions for round 93
     r = run(base | {"portals.conf": "# non-utf8 comment \udcff\n[preferred]\ndefault=kde\n"}, "XFCE")
     chk("non-utf8 comment does not void file", r.resolve(FC) == (["kde"], "default config"))
     r = run(base | {"portals.conf": "[preferred]\n\x0bdefault=kde\n"}, "XFCE")
     chk("vertical tab line is not a valid key-value pair", r.resolve(FC) == (["gtk"], "gtk-last-resort"))
     r = run(base | {"portals.conf": "[preferred]\ndefault=gtk\ndefault=kde\n"}, "XFCE")
     chk("repeated key adopts last value", r.resolve(FC) == (["kde"], "default config"))
     r = run(base | {"portals.conf": "[preferred]\ndefault[en_US]=gtk\ndefault=kde\n"}, "XFCE")
     chk("non-C locale key dropped under C locale", r.resolve(FC) == (["kde"], "default config"))
     ```
2. In `SCORECARD.md`: update harm watch baseline expectation to `tools/mado-portals.py 26/26`.

### Risks and mitigations
- *Execution time:* Adding 4 in-memory resolver runs adds < 10 ms to `--selftest`.
- *Hash invalidation:* Incorporating these 4 checks into `mado-portals.c1.py` before freeze ensures `EXPECT_TOOL_SHA256` and counter pins match the hardened candidate.

### Verification (DRAFT results in scratch)
- Unmodified candidate with 26 checks:
  `MADO_PORTALS_SELFTEST: checks=26 failed=0` (exit 0; 0.04s wall time).
- Unmodified base tool with 26 checks:
  `MADO_PORTALS_SELFTEST_FAIL: vertical tab line is not a valid key-value pair`
  `MADO_PORTALS_SELFTEST: checks=26 failed=1` (exit 1).
- Candidate on full 300-case battery (`portal-cases-r93.json`):
  `candidate score: 300 / 300` (base score: `272 / 300`).
