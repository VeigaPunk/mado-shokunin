# SourceChain: Reciprocal Provenance Chain Design (S051/S052 → U6 → README → Measurement)

- **Date:** 2026-10-20
- **Seat:** `MadoR15.SourceChain` (connector, leaf)
- **Lane Root:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Goal:** Mado round 15, Claim C1 coverage: sourced U1–U5 (5/7 = 7.1429/10) → sourced U1–U6 (6/7 = 8.5714/10) via bounded input-debugging layer route.
- **Milestone:** U6 input evidence ladder and R14 ancillary provenance correction.
- **Contract & Discipline:** Leaf connector; read-only repository and source inspection; no commits, tests, gates, linters, formatters, live probes, or input collection.

---

## 1. Executive Summary & The Proposed Move

### 1.1 The Tension Across Round Proposals
In round 15 proposals, two competing approaches emerged regarding source admission:
1. **The In-Place Shortcut (SimplifyScope F1):** Proposes dropping S051 and reusing S007 (`corpus/SOURCES.md:19`) by flipping its status from `queued` to `mined` in place to avoid duplicate URLs.
2. **The Source Integrity Critique (ReviewSourceTier F2, ReviewQuotes §1, ReviewSafety F1, ReviewCensus F5):** Points out that S007 points to the mutable URL `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` with an unpinned access-date anchor (`opened 2026-10-19`). Under `SOURCES.md:115` ("owed-anchor rule"), queued rows lacking an immutable revision SHA cannot be mined in place because the `anchor` cell is immutable by contract (Rule 2: only `status`, `recheck`, and `used-by` change in place).

### 1.2 The Non-Obvious Move (Compatible Synthesis)
**Execute a Clean Reciprocal Anchor-Pair via Superseding Pinned S051 and Scope-Disjoint S052:**
- **S051 (libinput helper tools):** Do not mutate S007's anchor. Admit S051 as a new `mined` Tier-A row pointing to the raw upstream git tag `1.32.0` RST source (`https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`), with commit `5cf833b572f5a33663888da321dce0ba1abd82a2` and SHA-256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`. Its `teaches` cell opens with `supersedes S007 —`. This discharges S007's owed anchor, avoids duplicate-URL collisions (`sources-census.sh` E04), and provides an immutable revision anchor.
- **S052 (Wayland core input protocols):** Avoid duplicate-scope collisions with S043 (which is pinned to `wl_registry` lines 117–177). Admit S052 as a new `mined` Tier-A row pointing to upstream tag `1.26.0` (`https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`), commit `87cc8a8728a923fc57938faa81ba0e74f34ecdc7`, SHA-256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` (byte-identical to host `/usr/share/wayland/wayland.xml`), scoped strictly to `wl_seat`, `wl_pointer`, and `wl_keyboard` protocols.
- **Bidirectional Reciprocity:** The U6 note's header cites both S051 and S052; both registry rows cite the U6 note in `used-by`. The round-15 measurement probe verifies this reciprocity identically to round 14's U5 `inverse` check, while leaving semantic evaluation to human review.

---

## 2. Evidence & Provenance Node Inventory

### Node 1: Sources Registry (`corpus/SOURCES.md`)
- **Baseline State:** 50 rows (S001–S050). S007 is `queued` with mutable `doc/latest/` URL; S043 is `mined` with installed-path anchor scoped to `wl_registry`.
- **Target Additions (Append-only to `## Registry`):**
  - `S051`: `libinput helper tools — https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst | docs | A | input-layer debugging route and tool defaults (libinput 1.32.0) | tag 1.32.0 @ 5cf833b5 (sha256 53264328…); tools.rst:31,45-46,135,220,262 | supersedes S007 — debug-events processes libinput events; list-devices shows built-in defaults not desktop config; record captures kernel events and obscures keys by default; tools need root | mined | 2026-10-20 | on-release | corpus/knowledge/input-debugging-ladder-r15.md`
  - `S052`: `Wayland core input protocol specification — https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml | spec | A | Wayland core seat, keyboard and pointer event lifecycle | tag 1.26.0 @ 87cc8a87 (sha256 cc860987…; byte-identical to installed /usr/share/wayland/wayland.xml); wl_seat:2004, wl_pointer:2138, wl_keyboard:2573 | Seat capability advertisement, surface focus entry/leave, keycode translation offset (+8), and discrete event delivery; advertisement != client delivery | mined | 2026-10-20 | on-release | corpus/knowledge/input-debugging-ladder-r15.md`
- **Validation:** Both rows have exactly 11 columns (13 `|` delimiters), Tier A, status `mined`, ISO open date `2026-10-20`, symbolic recheck `on-release`, and valid `used-by` paths.

### Node 2: Knowledge Note (`corpus/knowledge/input-debugging-ladder-r15.md`)
- **Header Block (First 15 lines):**
  ```markdown
  source: S051 (libinput 1.32.0 tools.rst @ 5cf833b5, sha256 53264328…; supersedes S007); S052 (Wayland 1.26.0 wayland.xml @ 87cc8a87, sha256 cc860987…; wl_seat/wl_pointer/wl_keyboard)
  verified-at: 2026-10-20; upstream raw digests verified; host package libinput 1.31.3-1 and wayland 1.26.0-1 observed read-only
  recheck: on-release of libinput or wayland; repeat static source digest verification
  covers: U6
  ```
- **Required Body Headings:**
  - `## Layer ladder`: Defines 5 distinct rungs (L0 Kernel `/dev/input/event*`, L1 Libinput processing & defaults, L2 Compositor device policy & mapping, L3 Wayland protocol surface focus & events, L4 Client application outcome).
  - `## Safe boundary`: Explicitly lists forbidden/refused routes (`debug-events`, `record`, `replay`, `measure`, `analyze`, `sudo`, raw `/dev/input`, `uinput`, `evemu`, `dmesg`). Affirmatively states that no event capture, injection, or kernel diagnosis was performed.
  - `## Unexercised delivery`: Explicitly marks client event receipt, IME / text-input composition, keymap application, and physical hardware behavior as `[UNK]`.

### Node 3: Navigation Map (`corpus/README.md`)
- **Coverage Map Join:** Add exactly one row in the `## Coverage map` table (line 40):
  ```markdown
  | `knowledge/input-debugging-ladder-r15.md` (round 15; covers U6) | Documented input-debugging ladder from kernel device nodes to Wayland surface focus; libinput defaults vs compositor policy vs client delivery; safe boundary refusing injection/capture. | `source:` S051, S052 in [SOURCES](SOURCES.md); recheck on-release. |
  ```
- **Frontier Ledger Update (`## Frontier` lines 91–95):**
  - Update: "Round 15 moves U6's documented input-debugging layer route onto [sourced ground](knowledge/input-debugging-ladder-r15.md)."
  - Retain: "Actual client event delivery, IME composition, kernel/hardware diagnostics, and Waybar module text (U7) remain open."

### Node 4: Measurement Probe (`.ufo/waves/round-15/measure.py`)
- **Revision-Bound Input:** Evaluates resolved commit SHA via `git show <sha>:<path>`.
- **Join Verification:**
  - Reads `source:`, `verified-at:`, `recheck:`, and `covers: U6` in note head-15.
  - Matches S051 and S052 in `corpus/SOURCES.md`, verifying `status == mined`, `tier in ('A', 'B')`, and `used-by` contains the note path.
  - Enforces `inverse`: every mined row in `SOURCES.md` that lists the note in `used-by` must be cited in the note's `source:` line.
  - Scans body facets: checks for headings `## Layer ladder`, `## Safe boundary`, and `## Unexercised delivery` containing `[UNK]`.
  - Verifies navigation: `corpus/knowledge/*.md` basenames match `corpus/README.md` indexed rows 1:1 (`notes == indexed == 29`, `missing == extra == duplicates == []`).
  - Emits JSON with `coverage.score = 8.5714` (6/7) and `admission = "manual-required"`.

---

## 3. Structural versus Semantic Checks

As demonstrated by `AttackMetric`, structural counters are blind to semantic truth (e.g. an inverted safety section recommending `sudo libinput record` would still pass structural regexes). The table below demarcates the exact division between automated structural checks and required semantic checks:

| Subsystem / Property | Structural Check (`measure.py` / `sources-census.sh`) | Semantic Check (Manual Review / Non-Author Spot-Check) |
|---|---|---|
| **S051 / S052 Registration** | Row splits to 13 cells (`NF==13`), ID format `S\d{3,}`, status `mined`, tier `A`, valid ISO date, valid recheck token. | URL points to canonical raw git commit/tag; SHA-256 hash matches upstream bytes; `teaches` accurately summarizes document scope. |
| **S051 Collision & Provenance** | `sources-census.sh validate` exits 0; `teaches` starts with `supersedes S007 —`. | Explains why S007 remains queued (owed-anchor debt) and how S051 provides the immutable revision anchor without in-place mutation. |
| **S052 Scope Disjointness** | URL differs from S043; `used-by` path resolves on disk. | Verifies S052 scope is restricted to `wl_seat/wl_pointer/wl_keyboard` (lines 2004–2700), distinct from S043's `wl_registry` scope. |
| **Reciprocal Join (U6 ↔ Sources)** | Regex finds `S051` and `S052` in note's `source:`; note path in rows' `used-by`; `inverse` boolean is True. | Note accurately uses concepts taught by S051/S052 without extending claims beyond their documented boundaries. |
| **U6 Header Provenance** | First 15 lines contain `source:`, `verified-at:`, `recheck:`, and exactly one `covers: U6`. | Verified-at date reflects actual inspection date; recheck cadence matches source lifecycle (`on-release`). |
| **Body Facet Headings** | Regex matches `## Layer ladder`, `## Safe boundary`, `## Unexercised delivery`. | Headings are genuine Markdown (not inside code fences or comments); content under headings matches their stated purpose. |
| **Safety Boundary Content** | Heading `## Safe boundary` exists. | Section affirmatively **refuses** execution of `debug-events`, `record`, `replay`, `sudo`, and `/dev/input`; zero injection or capture recommended. |
| **Unexercised Delivery Content** | Case-insensitive token `[UNK]` appears in `## Unexercised delivery`. | Context of `[UNK]` affirms that actual client delivery, IME, and kernel diagnostics are unexercised (not negated as "no [UNK] remains"). |
| **Layer Ladder Distinction** | Heading `## Layer ladder` exists. | Rung 1 (libinput defaults) is explicitly distinguished from Rung 2 (compositor effective policy via Hyprland getoption/devices); avoids M04 trap. |
| **Host Version Alignment** | N/A (probe does not inspect system packages). | Note acknowledges host libinput package is `1.31.3-1` and lacks the `libinput` CLI binary; upstream 1.32.0 docs are tagged `[INF-docs 1.32.0]`. |
| **Navigation Join** | `len(notes) == 29`, `missing == []`, `extra == []`, `duplicates == []`. | README coverage row's description accurately reflects U6 scope; Frontier text removes U6 from open list while keeping U7 open. |

---

## 4. Affected Axes & No-Harm Verification

| Axis | Expected Movement | Rationale & Guardrail |
|---|---|---|
| **Coverage** | **Improved: 5/7 (7.1429) → 6/7 (8.5714)** | Sourced current-art ground increases by exactly one covered item (U6). Denominator remains 7; U7 (Waybar module text) remains explicitly unexercised. |
| **Operability** | **Unchanged (10.0000 / Harm Watch)** | Existing gate `tools/mado-verify.sh` remains bit-identical (`fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`); hermetic selftest remains 372/372. |
| **Freshness** | **Unchanged (10.0000 / Harm Watch)** | Gate `--no-live` remains 29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE. |
| **Calibration** | **Unchanged / Unscored Precision Fix** | R14-V1 ancillary receipt precision is appended as an explanatory erratum mapping provisional headers to derived target `cd1d73d7…`. No generic wrapper or gate edit. |
| **Depth** | **Unchanged** | Static protocol and doc semantics remain strictly bounded; no synthetic depth claimed. |
| **Adjacency** | **Unchanged** | PROVINCE boundary strictly preserved; hardware, driver, evdev, and kernel diagnostics are refused and routed to `tsukuroi`. |

---

## 5. Risks, Contradictions & Second-Order Effects

1. **Second-Order Risk: Accidental Re-opening of M04 Trap**
   - *Risk:* Confusing libinput defaults (`libinput list-devices`) with Hyprland active configuration (`hyprctl getoption input:*`).
   - *Mitigation:* The U6 note must explicitly cite the `tools.rst:45-46` warning ("This tool does not show your desktop's configuration, just the libinput built-in defaults") and label libinput values as `[INF-docs 1.32.0]`.
2. **Second-Order Risk: Privacy Surface in Input Debugging Documentation**
   - *Risk:* Recommending or documenting `libinput record` or `debug-events` without highlighting keylogging hazards.
   - *Mitigation:* The `## Safe boundary` section must document that `record` only obscures alphanumeric keys by default, persists raw events to disk, and is classified as keylogger-class; execution is barred.
3. **Contradiction Handled: Single Revision Atomicity**
   - *Contradiction:* If `corpus/SOURCES.md`, `corpus/knowledge/input-debugging-ladder-r15.md`, and `corpus/README.md` are committed in separate commits, intermediate revisions fail navigation or coverage joins.
   - *Resolution:* All three files must land in the exact same content commit measured by `measure.py`.
4. **Tooling / Substrate Invariant:**
   - No packages installed or upgraded. Host has `libinput 1.31.3-1` and `wayland-utils 1.3.0-1`. Zero tool calls were executed against hardware or `/dev/input`.

---

## 6. Verification Checklist for Main Integration

Before declaring the round-15 deliverable complete, the main integrator should verify:
- [ ] `git show <commit>:corpus/SOURCES.md` contains S051 and S052 with exactly 11 columns, Tier A, status `mined`.
- [ ] `git show <commit>:corpus/knowledge/input-debugging-ladder-r15.md` contains header trio, `covers: U6`, and reciprocal `source: S051, S052`.
- [ ] `git show <commit>:corpus/README.md` contains the 29th note row and updated Frontier text.
- [ ] `./scripts/sources-census.sh validate --root . mado` exits 0 (warnings W04 for historical rows permissible).
- [ ] `python3 .ufo/waves/round-15/measure.py <commit>` outputs:
  - `coverage.covered = ["U1", "U2", "U3", "U4", "U5", "U6"]`
  - `coverage.count = 6`
  - `coverage.score = 8.5714`
  - `navigation.missing = []`, `navigation.extra = []`, `navigation.duplicates = []`
  - `gate.sha256 = "fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207"`
- [ ] `sha256sum tools/mado-verify.sh` matches `fba82a66…` exactly.
- [ ] Semantic check confirms `## Safe boundary` explicitly refuses capture/injection/replay and `## Unexercised delivery` contains `[UNK]`.

---

## 7. Tooling Record

- **Tool installs/updates:** None.
- **Channels used:** None.
- **System mutations:** None. Inspection conducted via read-only repository and filesystem tools.
- **Report Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/SourceChain.md`
