# SourceInventory — Audit of SOURCES.md, Prospective U5 Protocol XMLs, and Immutable-Cell Contract (Round 14, w1)

**Seat ID:** `MadoR14.SourceInventory`  
**Role:** Scout (UFO-FSD leaf subagent — no delegation, no background jobs, no tests/build/lint runs, no shared-file edits)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base Revision:** `59cfbdc3ab5e7b6aaf68f86e1b2ae8d51c938b1e` (round 13 delivered revision)  
**Milestone:** U5 boundaries and regular-source targets  
**Axes Judged On:** `coverage` (C1), `operability` (C2)  
**Date:** 2026-10-20  

---

## 1. Executive Summary & Godspeed Posture

In accordance with `/skill:godspeed`:
1. **Name the axes:**
   - **Coverage (C1):** Advance sourced protocol knowledge from U1–U4 ($4/7 = 5.7143/10$) to U1–U5 ($5/7 = 7.1429/10$) by auditing prospective upstream XML sources for output management (`zwlr_output_manager_v1`, reserved `S047`) and colour management (`wp_color_manager_v1`, reserved `S048`). Establish reciprocal mined joins without asserting unexercised feature behavior.
   - **Operability (C2):** Guarantee zero registry schema or census errors (`sources-census.sh` E01–E12, W01–W04 clean), enforce `QUALITY.md` Criterion 17 (pre-merge URL collision screen), protect the 11-column immutable-cell contract, prevent duplicate source inflation, and provide exact re-derivable pins for the canonical integrator.
2. **Iterate cheap, in parallel:** Coordinate findings with peer scouts (`OutputSpec`, `ColourSpec`, `OutputPhase`, `WlrVersion`, `OutputHost`) and reviewers (`ReviewSourceBar`, `ReviewCorrections`).
3. **Keep moves that improve any axis and harm none:** Ensure prospective rows introduce zero duplicate warnings (`W04`) or duplicate errors (`E04`), preserve existing 46 registry rows intact, and enforce strict distinction between protocol wire specifications and host runtime capabilities.
4. **Don't aim — let the frontier walk itself:** Identify exact canonical repository URLs, true commit SHAs, blob digests, and non-overlapping minimal scopes for S047 and S048.

### Key Audit Findings

1. **Collision Screen Clean (E04/W04 Clean):**
   A complete audit of existing rows `S001`–`S046` in `corpus/SOURCES.md` reveals **zero URL collisions** and **zero scope collisions** for prospective S047 and S048.
   - `wlr-output-management-unstable-v1.xml` originates from `https://gitlab.freedesktop.org/wlroots/wlr-protocols`, a repository and domain path never previously cited in `SOURCES.md`.
   - `color-management-v1.xml` originates from `staging/color-management/` under `https://gitlab.freedesktop.org/wayland/wayland-protocols`. Although `wayland-protocols` hosts existing rows `S005` (`README.md`) and `S040` (`GOVERNANCE.md`), its distinct file path prevents URL collision under `sources-census.sh` normalizer `url_of()`.
   - Bounded scopes prevent semantic overlap with S005 (protocol phases), S040 (upstream governance), S043 (core registry announcement/bind), and S046 (`wayland-info` observer code).
2. **Canonical Upstream URL & Pin Correction for S047:**
   - Common path trap: attempting `wayland/wlr-protocols` yields a GitLab authentication page (not public XML).
   - The authoritative upstream repository is `https://gitlab.freedesktop.org/wlroots/wlr-protocols` (0 git tags upstream; untagged repository).
   - Upstream commit alignment (corroborated by `WlrVersion`):
     - Master branch HEAD: `bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a` (2026-03-09).
     - Last modifying commit touching `unstable/wlr-output-management-unstable-v1.xml`: `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (2025-07-02).
     - Downstream Arch package snapshot commit: `a741f0ac5d655338a5100fc34bc8cec87d237346` (package `wlr-protocols r112.a741f0a-1`).
     - Blob SHA-256 is byte-identical across all three (`a5028af`, `a741f0a`, `bf4fc79`): `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` (611 lines, 26,355 bytes).
     - Disambiguation: Round-13 `ReviewPhases` cited commit `cdd2c7e0` in `wlroots/wlroots`. Canonical S047 must cite the `wlroots/wlr-protocols` repository commit (`a5028af` or `bf4fc79`), not `wlroots/wlroots`.
3. **Revision Binding & Discrepancy Alert for S048:**
   - Host Hyprland 0.56.2 advertises `wp_color_manager_v1` version **3** (`globals.json:295-296`).
   - Pinning historical commit `3dac056d` (the S005 README pin) yields an outdated color-management XML declaring version **2**; this is an invalid pin for the host advertisement.
   - Upstream commit `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (same commit as S040) declares version **3**, matching tag `1.49`. XML blob SHA-256: `afa46ce15b135cce09cb46e0fbe9469914f5f9819cb938662c3cea370bd825ca`.
   - Package notice: the local file `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` installed by `wayland-protocols 1.49-1` has SHA-256 `18a2678e...` due to 3 typo/wording differences from upstream `35d9638c` (e.g. line 41 `docs/html/` vs `docs/book/`). S048 must pin upstream `35d9638c` explicitly; line numbers must not be cited against the local file without noting the 3-line delta.
4. **Duplicate Inflation Prevention:**
   Exactly two rows (`S047` and `S048`) are recommended. No separate rows for sub-interfaces (`zwlr_output_configuration_v1`, `wp_color_management_output_v1`, etc.) or secondary community documentation.
5. **Strict Immutable-Cell Enforcement:**
   Columns 1–8 (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`) are strictly immutable. Only `status`, `recheck`, and `used-by` may change in place, and every such change must be logged old→new in `lessons/round-14.md` § Gate.

---

## 2. Complete Existing Registry Census & Collision Audit

`corpus/SOURCES.md` currently contains 46 rows (`S001` through `S046`).

### 2.1 URL Normalization Engine & Contract Rules

Per `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`row_pass` lines 600–652):
```awk
function url_of(s,   u,n) {
  if (match(s,/https?:\/\/[^[:space:]|]+/)) {
    u=substr(s,RSTART,RLENGTH)
    sub(/#[^ ]*$/,"",u); sub(/\/$/,"",u); sub(/^[A-Za-z]+:\/\//,"",u)
    n=index(u,"/"); if(n) u=tolower(substr(u,1,n-1)) substr(u,n); else u=tolower(u)
    return u
  }
  return ""
}
```
Validation rules:
- **`E04` (Duplicate URL within same scope):** Triggered when `u != ""` and `(u SUBSEP scope)` was previously seen in an active, non-rejected row without `supersedes S[0-9]{3}` in `teaches`.
- **`W04` (Duplicate URL across different scopes):** Triggered when `u != ""` and `u` was seen with a different scope.
- **`QUALITY.md` Criterion 17:** Pre-merge review must screen repeated canonical URLs across active rows even when scope strings differ, explicitly reviewing overlapping scope and preventing duplicate admission (lesson: `M1`, `S030` vs `S017`).

### 2.2 Cross-Examination of All Relevant Existing Rows

| Row | Canonical Source / Normalized URL | Scope | Kind / Tier | Status | Relationship to Prospective S047 / S048 |
|---|---|---|---|---|---|
| **S005** | `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md`<br>→ `gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md` | wayland protocol phasing and change policy (ground for later U4/U6 rounds) | docs / A | mined | **Same repository, different file.** S005 defines phase governance (experimental/staging/stable). Prospective S048 is in the same repo but points to `staging/color-management/color-management-v1.xml`. URL normalizer treats them as distinct paths. Scope is strictly non-overlapping. |
| **S010** | `https://wayland.app/protocols/`<br>→ `wayland.app/protocols` | protocol-document discovery index (community-maintained) | community / C | queued | **Discovery index only.** S010 indexes core and compositor protocols, but is Tier C. Cannot serve as sole support for an admitted claim. Does not collide with primary XML sources S047/S048. |
| **S040** | `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/GOVERNANCE.md`<br>→ `gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/GOVERNANCE.md` | Namespace-specific protocol inclusion and promotion authority, not runtime support | spec / A | mined | **Same repository & commit, different file.** S040 governs upstream namespace inclusion (`xdg`, `wp`, `ext`, `xx`). It does not govern wlroots protocols (`S047`) and does not specify color management interface semantics (`S048`). Scope is non-overlapping. |
| **S041** | `.ufo/waves/round-13/w1/globals.json`<br>→ `""` (local path, no HTTP URL) | This client's time-bound Hyprland 0.56.2 interface/version advertisements | own-work / A | mined | **Committed host observation.** Advertises `zwlr_output_manager_v1` v4 and `wp_color_manager_v1` v3. S041 provides runtime advertisement evidence; S047/S048 provide upstream protocol specifications. Perfect reciprocal complement. |
| **S042** | `https://wayland.freedesktop.org/extras.html`<br>→ `wayland.freedesktop.org/extras.html` | Documented compositor-global discovery, revision-anchored correction to S006 | docs / A | mined | **Tool purpose only.** Documents `wayland-info` global listing. Does not collide with XML protocols. Supersedes S006. |
| **S043** | `/usr/share/wayland/wayland.xml; https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry`<br>→ `wayland.freedesktop.org/docs/html/apa.html` | Core registry announcement, binding and removal are separate events | spec / A | mined | **Core registry protocol.** Defines `wl_registry`. Output and color management are protocol extensions, not core registry interfaces. Scope is non-overlapping. |
| **S045** | `https://wiki.hypr.land/Configuring/Basics/Window-Rules/`<br>→ `wiki.hypr.land/Configuring/Basics/Window-Rules` | Duplicate current-wiki source admission, not a new window-rule fact | docs / A | rejected | **Correction row.** Supersedes S030, marking duplicate admission. Serves as precedent for preventing duplicate row inflation. |
| **S046** | `https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c`<br>→ `gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c` | Upstream 1.3.0 observer bindings, output/colour detail queries and print filtering; not binary-source equivalence | code / A | mined | **Diagnostic client code.** Cites `wp_color_manager_v1_get_output` binding call in `wayland-info.c`. S046 covers diagnostic observer execution; S048 covers the protocol contract. Distinct repositories (`wayland-utils` vs `wayland-protocols`), distinct kinds (`code` vs `spec`). |

### 2.3 Verdict on Collisions

- **Prospective S047 (`wlr-output-management-unstable-v1.xml`):**
  - Normalized URL domain/path: `gitlab.freedesktop.org/wlroots/wlr-protocols/...`
  - Existing match: **None** (zero occurrences of `wlroots` in existing rows).
  - Collision check: `E04` = 0, `W04` = 0.
- **Prospective S048 (`color-management-v1.xml`):**
  - Normalized URL domain/path: `gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/35d9638c.../staging/color-management/color-management-v1.xml`
  - Existing match: Shares repository with S005 (`README.md`) and S040 (`GOVERNANCE.md`), but unique file subpath ensures distinct normalized URL.
  - Collision check: `E04` = 0, `W04` = 0.

---

## 3. Recommended S047 and S048 Minimal Source Scopes

To avoid duplicate inflation, vague claims, or inference traps, S047 and S048 must be scoped strictly to their protocol specification boundaries.

### 3.1 S047 Recommendation: wlr-output-management-unstable-v1

- **ID:** `S047`
- **Source:** `wlr-output-management-unstable-v1 — https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/blob/a5028afbe4a1cf0daf020c4104c1565a09d6e58a/unstable/wlr-output-management-unstable-v1.xml` (or master HEAD `bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a` / pkg `a741f0ac5d655338a5100fc34bc8cec87d237346`)
- **Kind:** `spec`
- **Tier:** `A`
- **Minimal Recommended Scope:**
  `wlr-output-management unstable v1 configuration transaction, serial, and head lifecycle semantics; not host display state`
- **Anchor:**
  `unstable/wlr-output-management-unstable-v1.xml @ a5028afbe4a1cf0daf020c4104c1565a09d6e58a (last modifying commit in wlr-protocols; blob sha256 65b0f82a…; identical at master bf4fc79 and pkg a741f0a); lines 29–34, 42, 424, 466, 481, 495, 507, 517`
- **Teaches:**
  `zwlr_output_manager_v1 allows reading configuration and creating transactional configuration objects to test or apply changes; test validates without applying; apply and test share succeeded/failed/cancelled events; outdated serial cancels transaction; does not prove monitor hardware support or active compositor output modes`
- **Status:** `mined` (upon landing with the U5 note)
- **Opened:** `2026-10-20`
- **Recheck:** `on-release`
- **Used-by:** `corpus/knowledge/output-colour-boundaries-r14.md` (or exact U5 knowledge note path)

### 3.2 S048 Recommendation: color-management-v1

- **ID:** `S048`
- **Source:** `color-management-v1 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/staging/color-management/color-management-v1.xml`
- **Kind:** `spec`
- **Tier:** `A`
- **Minimal Recommended Scope:**
  `wayland-protocols staging color-management-v1 image description, output rendering intent, and surface attachment protocol; not display hardware HDR capability`
- **Anchor:**
  `staging/color-management/color-management-v1.xml @ 35d9638cf0c3f0bbf0c42996580a284f3d8ce564 (sha256 afa46ce1…); lines 32–37, 74–75, 80, 88, 113–114, 634, 664, 704, 730`
- **Teaches:**
  `wp_color_manager_v1 allows creating immutable image descriptions to describe content color properties and query output color characteristics; self-described testing phase requires major version bump for breaking changes; unsupported feature error on unadvertised requests; does not establish HDR display hardware capabilities or active tone mapping`
- **Status:** `mined` (upon landing with the U5 note)
- **Opened:** `2026-10-20`
- **Recheck:** `on-release`
- **Used-by:** `corpus/knowledge/output-colour-boundaries-r14.md` (or exact U5 knowledge note path)

---

## 4. Duplicate Inflation Prevention Analysis

To satisfy the contract mandate ("no duplicate inflation"):
1. **No Interface Sub-Splitting:**
   `wlr-output-management-unstable-v1.xml` defines 5 interfaces (`zwlr_output_manager_v1`, `zwlr_output_head_v1`, `zwlr_output_mode_v1`, `zwlr_output_configuration_v1`, `zwlr_output_configuration_head_v1`). All are part of a single transaction lifecycle in one XML document. Opening separate rows for each interface would artificially inflate the registry by 4 rows without adding new authority.
   Similarly, `color-management-v1.xml` defines `wp_color_manager_v1`, `wp_color_management_output_v1`, `wp_color_management_surface_v1`, and image description creators. One row (`S048`) covers the entire extension specification.
2. **No Secondary Documentation Duplication:**
   Neither blog posts, wiki guides, nor third-party restatements may be admitted alongside primary Tier A specifications. Community indexes like `wayland.app` (already present as Tier C `S010`) remain queued discovery aids and must not be cloned or mined for U5.
3. **Exact Two-Row Addition:**
   The U5 advance requires exactly **two new source rows** (`S047` and `S048`). Raising C1 coverage from 4/7 to 5/7 requires exactly one new knowledge file covering U5, citing S047, S048, and the existing historical host capture S041.

---

## 5. Review of the Immutable-Cell Contract

`corpus/SOURCES.md` operates under **Contract v1** (canonical `CORPUS.md` § SOURCES.md; kaika provenance retained).

### 5.1 11-Column Schema & Mutability Classification

Every row adheres to an 11-column pipe-delimited schema (`NF=13` in awk):
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`

| Column | Name | Mutability Discipline | Permitted Operations & Restrictions |
|---|---|---|---|
| 1 | `id` | **IMMUTABLE** | Stable identifier (`S[0-9]{3,}`). Never reassigned, never reused. |
| 2 | `source` | **IMMUTABLE** | Canonical document title and URL or path. Never changed in place. |
| 3 | `kind` | **IMMUTABLE** | Enum: `spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work`. |
| 4 | `tier` | **IMMUTABLE** | Enum: `A\|B\|C`. Community is never Tier A (`E10`). |
| 5 | `scope` | **IMMUTABLE** | Bounded topic scope. Never broadened or smoothed. |
| 6 | `anchor` | **IMMUTABLE** | Specific section, lines, commit/tag SHA, date. If defective, cannot be edited; requires superseding row. |
| 7 | `teaches` | **IMMUTABLE** | Concrete statement of what source teaches, including boundary caveats. If rejected, teaches cell is never edited; explanation is logged in lessons and search log. |
| 8 | `status` | **MUTABLE** | Enum: `queued\|mined\|rejected`. Allowed in-place transition: `queued -> mined` when cited by new knowledge note; `mined -> rejected` if rejected by spot-check. Must be logged old→new in that round's lesson. |
| 9 | `opened` | **IMMUTABLE** | ISO date (`YYYY-MM-DD`) when row was created. Never updated on reopen. |
| 10 | `recheck` | **MUTABLE** | Cadence (`on-release`, `on-change`, `90d`, `180d`) or ISO date. May be updated during re-verification. |
| 11 | `used-by` | **MUTABLE** | Comma-separated list of knowledge notes citing the row, or `—`. Must maintain reciprocal joins (`J3`/`J4`). |

### 5.2 Precedents and Enforcement Mechanisms

1. **The In-Place Edit Ban (Rule 2):**
   When `S006` (`extras.html`) was found in round 12 to lack a source repository commit in its anchor, contract rules forbade editing line 20 in place. Instead, round 13 opened `S042` with `teaches` beginning with `supersedes S006 —` and pinning commit `8923a199...`. S006 remains `queued` historical metadata.
2. **The Rejection Invariance Rule:**
   When `S030` was rejected by outside review for duplicating `S017`, its `teaches` cell was **not** edited. Its status was flipped to `rejected` in place, its `used-by` transferred to `S017`, and round 13 opened `S045` to document the rejection and flip condition.
3. **Requirement for S047 and S048:**
   Because all 8 immutable columns become permanently fixed upon commit, their authoring must be 100% verified prior to landing. Neither URL typos, incomplete git commits, nor inaccurate scopes can be fixed by amending the row later.

---

## 6. Rejection and Flip Ledger (Advisory for Gate & Lesson)

To satisfy `QUALITY.md` criteria 1, 3, 5, 15, and 16, the following candidate rejections and flips are established for the U5 output/colour milestone:

| Candidate Claim | Disposition | Grounding Evidence & Defect Class | Flip Condition |
|---|---|---|---|
| *Advertised zwlr_output_manager_v1 proves monitor configuration or layout changes succeed on this host.* | **REJECT** | S047 XML (`wlr-output-management-unstable-v1.xml:486-487`): *"Even if the compositor succeeds to test a configuration, applying it may fail."* Advertisement indicates manager presence, not hardware display capability. | Authorized dynamic execution showing client applying configuration and receiving `zwlr_output_configuration_v1.succeeded` event without error. |
| *Test configuration success guarantees apply configuration success.* | **REJECT** | S047 XML (`:486-487`): Upstream explicitly separates validation (`test`) from application (`apply`). Hotplug races emit `cancelled` (`:518-522`). | Separate authorized measurement showing `apply` succeeded after `test`. |
| *wlr-output-management-unstable-v1 is governed by wayland-protocols GOVERNANCE (S040).* | **REJECT** | S040 (`GOVERNANCE.md`) explicitly covers `wayland-protocols` repository namespaces (`xdg`, `wp`, `ext`). `wlroots` is an independent project governed under its own repository. | Official wlroots governance document establishing protocol lifecycle authority. |
| *Advertised wp_color_manager_v1 proves HDR display presentation or wide-color-gamut rendering is active.* | **REJECT** | S048 XML (`color-management-v1.xml:34-37`): *"All surface contents must be readily intended for some display, but not necessarily for the display at hand."* S041 capture excludes colorimetry blocks. | End-to-end hardware measurement (colorimeter/EDID/KMS plane) or compositor telemetry verifying active HDR/wide-gamut output pipeline. |
| *Color-management-v1 staging protocol is an immutable, frozen stable API.* | **REJECT** | S048 XML (`:74-75`): Self-described as *"currently in the testing phase."* S005 README staging rules permit interface version bumps and deprecation. | Upstream promotion to stable phase (removal of `-v1` and staging path). |
| *Installed XML file (/usr/share/wayland-protocols/...) line 41 is authoritative upstream anchor for 35d9638c.* | **REJECT** | Local file hash `18a2678e...` differs from upstream `35d9638c` hash `afa46ce1...` across 3 lines. | Citing upstream `35d9638c` raw URL and blob hash directly. |

---

## 7. Re-Derivation Commands & Integrity Checksums

All observations and pins can be re-derived with the following read-only commands:

```bash
# 1. Re-derive S047 upstream XML blob SHA-256 (expect 65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7; identical at a5028af, bf4fc79, and a741f0a)
curl -fsSL https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a5028afbe4a1cf0daf020c4104c1565a09d6e58a/unstable/wlr-output-management-unstable-v1.xml | sha256sum

# 2. Re-derive S048 upstream XML blob SHA-256 (expect afa46ce15b135cce09cb46e0fbe9469914f5f9819cb938662c3cea370bd825ca)
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/staging/color-management/color-management-v1.xml | sha256sum

# 3. Verify installed wayland-protocols XML SHA-256 (expect 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9)
sha256sum /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml

# 4. Verify host advertisement versions in committed globals.json
grep -n -E 'zwlr_output_manager_v1|wp_color_manager_v1' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json

# 5. Run sources census validation on current baseline (expect exit 0, ok with 3 known historical W04 warnings)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

### Tooling Directive Audit
No packages were installed or upgraded during this investigation. `pacman -Q` and read-only curl/git commands were used exclusively. Full host state remains untouched.
