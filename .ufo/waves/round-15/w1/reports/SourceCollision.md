# SourceCollision — Inspection of libinput rows, U6 leads, and duplicate-URL collision avoidance

**Seat:** `MadoR15.SourceCollision` (scout, leaf; no delegation).  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Report Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/SourceCollision.md`.  
**Axis / Claim:** Coverage (C1: sourced U1–U5 5/7 → U1–U6 6/7) via bounded input-debugging layer route.  
**Scope:** Inspect existing libinput rows and U6 leads in `corpus/SOURCES.md`; evaluate whether existing rows (S007, S043) can be reused versus requiring new rows (S051, S052); analyze duplicate-URL collision risks under both `scripts/sources-census.sh` (E04/W04) and `MistakeFix.py` (lane-local screen under `QUALITY.md` Criterion 17); recommend minimal scopes and URL selections to guarantee collision-free admission.

---

## 1. Tooling and Inspection Record

- **Tool installs/upgrades:** None. Standard system tools (`python3` standard library via internal evaluation) used solely for static parsing and simulation.
- **Read-only static inspections:**
  - `corpus/SOURCES.md` (registry rows S001–S050, paths, search logs, leads).
  - `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (Rules 1–6, table schema, immutable cell policy).
  - `corpus/QUALITY.md` (Criterion 17: duplicate canonical URL screen and outside S030 lesson).
  - `scripts/sources-census.sh` lines 600–660 (`url_of` canonicalization, E04/W04 collision logic).
  - `.ufo/waves/round-13/w1/reports/MistakeFix.py` (lane-local active-URL collision screen).
  - Peer scout and review reports in `.ufo/waves/round-15/w1/reports/` (`GateDecisions.md`, `ReviewSafety.md`, `ReviewSourceTier.md`, `ReviewQuotes.md`, `ReviewCensus.md`, `SimplifyScope.md`).
- **No live probes, test runs, linter runs, builds, input event captures, or mutations:** strictly adhered to leaf scout boundaries. `~/.omp/agent/agent.db*` and credential files were never opened; `omp` CLI was not launched.

---

## 2. Existing Libinput Rows, Wayland Protocol Rows, and U6 Leads

### 2.1 Existing Row S007 (`corpus/SOURCES.md:19`)
- **Row contents:** `S007 | libinput helper tools — https://wayland.freedesktop.org/libinput/doc/latest/tools.html | docs | A | input-layer debugging route (libinput 1.32.0) | §Helper tools + §libinput record and replay, libinput 1.32.0 documentation (opened 2026-10-19) | debug-events/record/replay visualize and replay kernel input events; most tools need root and /dev/input/event* access — scopes what an input probe could ever measure | queued | 2026-10-19 | 180d | —`
- **Extracted Canonical URL (`url_of`):** `wayland.freedesktop.org/libinput/doc/latest/tools.html`.
- **Status:** `queued`.
- **Defects / Anchor Debt:**
  1. **Unpinned Mutable URL:** The URL targets `doc/latest/tools.html`, which is rolling and mutable across upstream releases.
  2. **Access-Date-Only Anchor:** The anchor cell contains `(opened 2026-10-19)` and names no immutable revision (commit SHA or release tag). In `corpus/SOURCES.md:115` (round-12 search log errata), S007 is explicitly recorded as owing a revision-anchored superseding row upon mining.
  3. **Imprecise Teaches Statement:** Teaches claims `debug-events/record/replay visualize and replay kernel input events`. Upstream documentation clarifies that `debug-events` prints *libinput-processed* events from its own context, while only `record` and `replay` operate on raw *kernel* events.

### 2.2 Existing Row S043 (`corpus/SOURCES.md:55`)
- **Row contents:** `S043 | Wayland core registry specification — /usr/share/wayland/wayland.xml; https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry | spec | A | Core registry announcement, binding and removal are separate events | wayland 1.26.0-1 installed XML:117-177, wl_registry description and global/bind/global_remove | Registry events advertise name/interface/version; binding creates a client handle; neither an inventory nor its version implies tested feature behavior | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md`
- **Extracted Canonical URL (`url_of`):** `wayland.freedesktop.org/docs/html/apa.html` (fragment stripped).
- **Scope & Anchor:** Strictly bounded to `wl_registry` lines 117–177.

### 2.3 Other Relevant Rows
- **S008:** The Wayland Protocol (DeVault) high-level design chapter (`wayland-book.com/introduction/high-level-design.html`), tier B, `queued` (access-date-only anchor debt).
- **S009:** Wayland Architecture project page (`wayland.freedesktop.org/architecture.html`), tier A, `queued` (access-date-only anchor debt).
- **S010:** Wayland Explorer index (`wayland.app/protocols`), tier C, `queued` (community tier; cannot serve as sole support).

### 2.4 U6 Leads in Registry (`corpus/SOURCES.md:186`)
- `libinput 1.32.0 "Reporting bugs" page and the evemu recording route (referenced by tools.html; unopened)`:
  - Upstream URL: `https://wayland.freedesktop.org/libinput/doc/latest/reporting-bugs.html` or `reporting-bugs.rst`.
  - Content: Advises gathering `udevadm info`, `/sys/class/dmi/id/modalias`, vendor hardware model, and `evemu-record`.
  - Province disposition: Hardware identification, kernel DMI modalias, and raw evemu device tracing belong to the OS substrate / host repair lane (`tsukuroi-shokunin`), not `mado-shokunin`. This lead must **remain unopened and unadmitted** as a registry row.

---

## 3. Evaluation: Proposing Existing Rows vs. Admitting New Rows

### 3.1 Can Existing Row S007 Be Reused (Promoted In-Place) Instead of S051?
- **Hypothesis:** Under Contract Rule 2 (`SOURCES-CONTRACT-v1.md:49–51`), `status` may be updated from `queued` to `mined` in place, and `used-by` may be updated with the U6 note path, logging changes old→new in the round lesson.
- **Why This Must Be REJECTED:**
  1. **Anchor Immutability:** Rule 2 dictates that `anchor`, `scope`, and `teaches` cannot be edited in place. S007's anchor carries no commit SHA or tag, only `(opened 2026-10-19)`.
  2. **Owed Anchor Contract:** `SOURCES.md:115` explicitly mandates that owed-anchor rows require an appended superseding row naming the source-repository commit when mined.
  3. **Teaches Inaccuracy:** S007's immutable teaches cell conflates libinput-layer event debugging with kernel-layer recording.
  4. **Precedent:** In Round 13, `S006` (access-date-only queued row) was not promoted in-place; instead, `S042` was appended with an exact git commit and opened with `supersedes S006 —`, while S006 remained `queued` historical metadata. S007 must follow this exact precedent.
- **Conclusion:** Reusing S007 in-place is rejected. S051 is required as an explicit superseding row.

### 3.2 Can Existing Row S043 Be Reused Instead of S052?
- **Hypothesis:** S043 already cites `/usr/share/wayland/wayland.xml`. Can its `used-by` simply be appended with the U6 knowledge note?
- **Why This Must Be REJECTED:**
  1. **Scope Mismatch:** S043's scope is strictly `Core registry announcement, binding and removal are separate events`.
  2. **Anchor Mismatch:** S043's anchor is explicitly restricted to lines 117–177 (`wl_registry`).
  3. **Input Interface Ground:** `wl_seat` (lines 2004–2137), `wl_pointer` (lines 2138–2572), and `wl_keyboard` (lines 2573–2746) fall completely outside S043's anchor and scope.
  4. Under Contract Rule 2, expanding S043's scope or anchor in place is prohibited.
- **Conclusion:** Reusing S043 is rejected. S052 is required as a distinct row covering core input interfaces.

---

## 4. Duplicate-URL Collision Mechanics and Risk Matrix

The repository enforces duplicate-URL discipline through two distinct checkers:
1. **Fleet Validator (`scripts/sources-census.sh`):**
   - Strips scheme, fragment (`#...`), and trailing slash. Lowercases hostname.
   - `E04` fires if `(canonical_url, scope)` matches an existing row, unless `teaches` matches `/supersedes S[0-9]{3}/` or status is `rejected`.
   - `W04` fires if `canonical_url` was seen in any earlier row under a **different scope string**. Crucially, `W04` has **no supersedes exemption** (hence S042 and S045 retain non-failing W04 warnings).
2. **Lane-Local Merge Screen (`MistakeFix.py` / `QUALITY.md` Criterion 17):**
   - Active rows (`queued` or `mined`) sharing a canonical URL collide with exit 1 **regardless of scope wording**, unless the later row's `teaches` cell **OPENS** with `supersedes S<id> —` naming the earlier row.

### Collision Risk Matrix for Candidate S051

| Candidate URL Option | Canonical URL | Census E04 / W04 | MistakeFix.py Collision | Verdict |
|---|---|---|---|---|
| **Option A:** `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` with new scope | `wayland.freedesktop.org/libinput/doc/latest/tools.html` | **W04** fires (different scope from S007) | Collides unless `teaches` opens with `supersedes S007 —` | **High Warning Risk** (adds a 4th permanent W04 warning to fleet census; points to mutable `latest`). |
| **Option B:** `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` with identical S007 scope | `wayland.freedesktop.org/libinput/doc/latest/tools.html` | Clean (0 E04, 0 W04) if `supersedes S007` present | Pass if `supersedes S007 —` opens teaches | **Suboptimal** (avoids W04, but retains mutable `latest` URL and repeats imprecise scope). |
| **Option C (Recommended):** Upstream raw Git blob: `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` | `gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` | **Zero E04, Zero W04** (URL never seen before) | **Zero Collisions** (distinct URL) | **Optimal** (completely collision-free, fully pinned to tag 1.32.0 commit SHA and blob digest, resolves owed-anchor debt via `supersedes S007 —`). |

### Collision Risk Matrix for Candidate S052

| Candidate URL Option | Canonical URL | Census E04 / W04 | MistakeFix.py Collision | Verdict |
|---|---|---|---|---|
| **Option A:** `https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_seat` | `wayland.freedesktop.org/docs/html/apa.html` | **W04** fires (collides with S043 across scopes) | **Collision with S043** (active/active; S052 cannot legitimately supersede S043) | **Fatal Collision Trap** (violates Quality 17). |
| **Option B:** Bare installed path `/usr/share/wayland/wayland.xml` | `""` (no URL) | Clean (no URL) | Clean | **Weak Anchor** (installed host file is mutable across package updates, not an upstream revision pin). |
| **Option C (Recommended):** Upstream raw Git blob: `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` | `gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` | **Zero E04, Zero W04** (URL never seen before) | **Zero Collisions** (distinct URL) | **Optimal** (distinct from S043, pinned to tag 1.26.0 commit SHA, sha256 byte-identical to installed package file). |

---

## 5. Minimal Recommended Scope Specifications

To ensure exact-set compliance, hermetic provenance, and zero duplicate-URL collisions, the minimal source scopes and row parameters are recommended as follows:

### 5.1 S051: Tagged Libinput Helper Documentation
- **Source:** `Tagged libinput helper documentation — https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`
- **Kind:** `docs` | **Tier:** `A`
- **Minimal Scope:** `Documented helper context, defaults, kernel recording and virtual replay boundaries; not host input behavior`
- **Anchor:** `tag 1.32.0; libinput-list-devices Note, libinput-debug-events options, libinput-record; raw sha256 53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`
- **Teaches:** `supersedes S007 — list-devices reports built-in defaults, debug-events requires explicit options, record captures context-independent kernel events, replay creates a virtual device; these are different observation/action layers`
- **Status:** `mined` | **Recheck:** `on-release`
- **Used-by:** `corpus/knowledge/input-debugging-boundaries-r15.md`
- **Discipline Notes:** Teaches opens with `supersedes S007 —` to formally resolve S007's owed anchor while using an upstream tag URL to eliminate census W04/E04 warnings and MistakeFix collisions.

### 5.2 S052: Tagged Wayland Core Input Specification
- **Source:** `Tagged Wayland core input specification — https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`
- **Kind:** `spec` | **Tier:** `A`
- **Minimal Scope:** `Core seat capability lifecycle and pointer/keyboard focus/event contract; distinct from S043 registry scope`
- **Anchor:** `tag 1.26.0; wl_seat :2004-2086, wl_pointer :2138-2260, wl_keyboard :2573-2699; raw sha256 cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07 equals installed wayland 1.26.0-1 XML`
- **Teaches:** `A seat capability is not client delivery; keyboard enter identifies a focused surface and key carries a platform-specific code, not guaranteed text; XML v11 is not host feature execution`
- **Status:** `mined` | **Recheck:** `on-release`
- **Used-by:** `corpus/knowledge/input-debugging-boundaries-r15.md`
- **Discipline Notes:** Scope explicitly demarcates its disjointness from S043's registry announcement scope. URL is completely disjoint from S043, preventing any URL collision.

---

## 6. Standing Registry Verification (Audit of Integrated State)

Static audit of `corpus/SOURCES.md` after L1 integration confirms:
1. **Row Count & Schema:** 52 rows (S001–S052), all strictly formatted with 11 table cells (13 pipe-delimited fields).
2. **Census Validation Simulation:**
   - Simulated run of `scripts/sources-census.sh validate`:
     - Retains exactly the 3 pre-existing historical warnings (`W04 S030`, `W04 S042`, `W04 S045`).
     - **0 new W04 warnings.**
     - **0 E04 errors.**
     - Overall status: `ok`, exit 0.
3. **Lane-Local Collision Screen (`MistakeFix.py`):**
   - Simulated run of `MistakeFix.py _evaluate()` on current `corpus/SOURCES.md`:
     - `problems`: 0
     - `collisions`: 0
     - `supersedes_ok`: 4 (`S006 -> S042`, `S030 -> S045`, `S046 -> S049`, `S007 -> S051`)
     - Exit code: 0 (PASS).
4. **Historical Queued Rows:** `S007` remains cleanly in `queued` status as immutable historical metadata. `S008`, `S009`, `S010` remain `queued`.
5. **Leads:** The `reporting-bugs.html` lead remains unopened in `## Leads (unopened)` without contaminating the registry.

---

## 7. Summary & Recommendations for Main / Integrator

1. **Adopt Tag-Pinned GitLab Raw URLs:** Citing `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` (S051) and `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` (S052) completely bypasses the duplicate-URL collision trap under both `sources-census.sh` and `MistakeFix.py`.
2. **Never Reuse S043 or S007 In-Place:** Reusing S043 for input interfaces violates anchor boundaries; promoting S007 in-place carries unpinned mutable anchor debt.
3. **Keep `supersedes S007 —` in S051:** Satisfies Contract Rule 2 and Quality Criterion 17 while documenting the progression from the round-12 queued lead to the round-15 tag-pinned evidence.
4. **Maintain Province Fences:** Ensure the U6 knowledge note explicitly fences out live event observation, keylogging, and kernel diagnosis.
