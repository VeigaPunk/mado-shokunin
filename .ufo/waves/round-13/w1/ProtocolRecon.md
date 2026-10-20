# ProtocolRecon — Queued U4 Source Review and Minimal Evidence Join Recommendation

**Seat:** `MadoR13.ProtocolRecon` (scout, leaf; no subagent dispatch, no background jobs).  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Milestone:** exact-set census and sourced U4 boundaries.  
**Judged on:** coverage, operability.  
**Draft path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ProtocolRecon.md`  
**Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/ProtocolRecon.md`  
**Status:** complete findings; no shared repo files edited; no tests/builds/selftests run.

---

## 1. Axes

1. **Coverage (C1):** Sourced current-art ground $U_1–U_3 = 3/7$ (4.2857/10) $\rightarrow U_1–U_4 = 4/7$ (5.7143/10). Admit exactly one $U_4$ entry separating protocol phases, compositor-advertised globals, and unexercised behavior. Count unique `covers: U[1-7]` joined to existing knowledge paths and mined source rows, not source-row volume. $U_5–U_7$ must remain unadmitted.
2. **Operability (C2):** Exact-set census detection for Hyprland source and local configuration inventory (`tools/mado-verify.sh`), with named missing/extra details and hermetic negative testing. Harm watch: selftest and regression remain intact.

---

## 2. Review of Current SOURCES Queued Rows and README Frontier

### 2.1 Current Queued Rows in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`

| ID | Source | Kind | Tier | Scope | Current Status | Round-13 Disposition for U4 Join |
|---|---|---|---|---|---|---|
| **S005** | `wayland-protocols README` | docs | A | Wayland protocol phasing and change policy | `queued` | **Promote to `mined`**: primary upstream definition of `experimental`, `staging`, and `stable` phases. |
| **S006** | `Wayland debugging extras` | docs | A | Compositor globals surface (`wayland-info`, `WAYLAND_DEBUG`) | `queued` | **Promote to `mined`** (or supersede via S042 with commit `8923a199`): anchors `wayland-info` tool role. |
| **S007** | `libinput helper tools` | docs | A | Input-layer debugging (`libinput`, `/dev/input/event*`) | `queued` | **MUST REMAIN `queued`**: belongs strictly to $U_6$ (kernel-input debugging ladder); do NOT join to $U_4$. |
| **S008** | `The Wayland Protocol (DeVault)` | book | B | Wayland architecture, compositor dispatch/composite concepts | `queued` | **REMAIN `queued`**: secondary Tier B source; unnecessary for minimal join; avoids tier mixing. |
| **S009** | `Wayland Architecture` | docs | A | X-vs-Wayland event path and direct-rendering model | `queued` | **REMAIN `queued`**: general architecture background; not required for minimal $U_4$ join. |
| **S010** | `Wayland Explorer` | community | C | Protocol-document discovery index | `queued` | **REMAIN `queued`**: community index (Tier C); cannot serve as evidence. |
| **S036** | `RemoteDesktop portal` | spec | A | RemoteDesktop v2 and ScreenCast integration | `queued` | **REMAIN `queued`**: $U_3$ side reading; unrelated to $U_4$. |
| **S038** | `xdg-desktop-portal 1.21.0` | docs | A | Portal frontend feature notes | `queued` | **REMAIN `queued`**: $U_3$ side reading; unrelated to $U_4$. |
| **S039** | `xdg-desktop-portal 1.22.0` | docs | A | Portal frontend bug fixes | `queued` | **REMAIN `queued`**: $U_3$ side reading; unrelated to $U_4$. |

### 2.2 Review of the README Frontier

In `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md` (`## Frontier`, lines 89–94):
- **Rule attribution:** open gap from $U_1$ (`getprop` reads applied values, not matching rule attribution). Remains open.
- **Protocol phase and advertised globals ($U_4$):** **The exact targeted frontier for Round 13.** Replaces the arc gap ledger negative claim with sourced upstream phase rules and host sanitized globals inventory.
- **Output management ($U_5$):** Uncovered; remains open in Frontier.
- **Input debugging ladder ($U_6$):** Uncovered; remains open in Frontier (`libinput` S007 remains queued).
- **Waybar module text ($U_7$):** Uncovered; remains open in Frontier (no IPC/query verb).

---

## 3. Source Opens (Primary Evidence Verification)

### Source Open 1: S005 (wayland-protocols README)
- **URL:** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md`
- **Access Date:** 2026-10-20
- **Location:** `§Protocol phases`
- **Revision:** `3dac056d83ad8947eed6eb621f346e91da736efd` (committed 2026-01-16)
- **Tier:** A (Official upstream documentation/specification)
- **Exact Quote (15 words):**
  > "Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase."
- **Admission/Rejection:** Admit to `mined`.
- **Flip:** Was `queued` in round 12; now promoted to `mined` with verified commit anchor.

### Source Open 2: S006 (Wayland debugging extras)
- **URL:** `https://wayland.freedesktop.org/extras.html`
- **Access Date:** 2026-10-20
- **Location:** `§Compositor features`
- **Revision:** `8923a19916635c21a3577b616f650a7e45d70fa9` (committed 2026-01-15 in upstream repo `https://gitlab.freedesktop.org/wayland/wayland.freedesktop.org`)
- **Tier:** A (Official project documentation)
- **Exact Quote (11 words):**
  > "Running `wayland-info` will list all global interfaces advertized by the compositor."
- **Admission/Rejection:** Admit to `mined` (satisfies owed anchor from round-12 search log erratum with exact commit `8923a199`).
- **Flip:** Was `queued` with missing revision anchor; now grounded to upstream commit.

### Source Open 3: Candidate S040 (wayland-protocols GOVERNANCE.md)
- **URL:** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/GOVERNANCE.md`
- **Access Date:** 2026-10-20
- **Location:** `§2.1.1 Experimental protocol namespacing`
- **Revision:** `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (committed 2026-10-12)
- **Tier:** A (Official upstream governance specification)
- **Exact Quote (19 words):**
  > "Experimental protocols begin with the \"xx\" namespace and do not include any relation to namespaces specified in section 2.1."
- **Admission/Rejection:** Admit to `mined`.
- **Flip:** Was an unopened lead in round 12 (`corpus/SOURCES.md:100`); now verified and admitted as formal specification ground for protocol namespaces and promotion rules.

### Source Open 4: Candidate S041 (Host Sanitized Advertised Globals Capture)
- **Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json`
- **Access Date:** 2026-10-20
- **Location:** `globals.json:26-315`
- **Revision:** Probe capture timestamp `2026-10-20T04:08:06Z` on Hyprland 0.56.2 (commit `efb50993780079460b0cbed1363e2166a2de1d9f`), `wayland-info` 1.3.0-1
- **Tier:** A (Direct host measurement, sanitized own-work)
- **Exact Quote (5 words):**
  > `"interface": "wl_compositor", "version": 6`
- **Admission/Rejection:** Admit to `mined`.
- **Flip:** Was a negative tool capability lead (`wayland-info absent` in round 12); now captured under authorized tool directive and verified clean.

---

## 4. Minimal Evidence Joins to Move U4 ONLY (Not U5–U7)

To satisfy the SCORECARD counting command:
`for f in corpus/knowledge/*.md; do head -n 15 "$f" | grep -qE '^source:.*\bS[0-9]{3,}\b' && echo "$f"; done | wc -l` (sourced entries)  
`grep -cE '^covers: U[1-7]' corpus/knowledge/*.md` (target: 4)

The minimal join requires:

### 4.1 Knowledge Entry Construction
1. **Target File:** `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-phases-r13.md` (or sibling designated knowledge note).
2. **Mandatory Header Format (Lines 1–10):**
   ```markdown
   # Wayland Protocol Phases and Compositor-Advertised Globals (MADO-R13-1)

   source: S005 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md — §Protocol phases; S040 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/GOVERNANCE.md — §2.1-2.3; S006 — https://wayland.freedesktop.org/extras.html — §Compositor features; S041 — .ufo/waves/round-13/w1/globals.json
   verified-at: 2026-10-20
   recheck: on-release
   covers: U4
   ```
3. **Exact Coverage Constraint:**
   - MUST contain `covers: U4`.
   - MUST NOT contain `covers: U5`, `covers: U6`, or `covers: U7`.
   - The cited sources must have status `mined` in `corpus/SOURCES.md`.

### 4.2 Decoupling $U_4$ from $U_6$ in `corpus/SOURCES.md`
In round 12, `corpus/SOURCES.md` `## Paths` grouped $U_4$ and $U_6$ together:
```text
- **Protocol and input debugging frontier (U4/U6, queued)** — S009 → S008 → S005 → S006 → S007, with S010 as a discovery index only...
```
To move $U_4$ only, the integrator must split this into two separate paths:
1. **$U_4$ Mined Path:**
   ```text
   - **Wayland protocol phases and advertised globals (U4)** — S005 → S040 → S006 → S041: official protocol phases (experimental/staging/stable), governance lifecycle and namespace rules, debugging tools surface, then host advertised globals capture; falsifies advertisement as protocol capability execution.
   ```
2. **$U_6$ Queued Path (Untouched):**
   ```text
   - **Input debugging frontier (U6, queued)** — S009 → S008 → S007, with S010 as a discovery index only: architecture before input tools; unmined.
   ```

### 4.3 Clean Fencing Against $U_5$, $U_6$, and $U_7$
- **Fencing $U_5$ (Output management / colour boundary):** The host's `globals.json` capture includes output-related interfaces such as `zwlr_output_manager_v1` (version 4) and `zwlr_output_power_manager_v1` (version 1). The knowledge note must explicitly fence these:
  > *[INF-docs / UNK]* Interface advertisement of `zwlr_output_manager_v1` establishes only that the compositor advertises the global. It does not prove client configuration requests, test/apply cycles, or a functional color/HDR pipeline. $U_5$ remains uncovered and unadmitted.
- **Fencing $U_6$ (Kernel input → Wayland debugging):** `libinput` tools (S007) and `/dev/input/event*` inspection must be explicitly omitted from the $U_4$ note. $U_6$ remains queued.
- **Fencing $U_7$ (Waybar module text):** No text inspection or IPC query verbs are inferred or admitted. $U_7$ remains unknown.

---

## 5. Confidence, Evidence Grounding, and Remaining Unknowns

### Confidence
- **High (1.00):** S005, S006, and S040 upstream commits and exact text anchors verified directly against official Gitlab repositories (`gitlab.freedesktop.org/wayland`).
- **High (1.00):** S041 sanitized capture (`globals.json`) verified against local host probe on Hyprland 0.56.2.
- **High (1.00):** Causal and rubric separability of $U_4$ from $U_5–U_7$ is absolute.

### Remaining Unknowns
1. **Client runtime binding:** Globals advertised by Hyprland are static compositor capabilities offered at registration; whether any client connects or binds to a given version is unmeasured (requires client-side interception or `WAYLAND_DEBUG=1`).
2. **Behavioral execution:** Advertising an interface does not prove protocol functionality (e.g. screencopy, gamma control, or output management).
3. **$U_5–U_7$:** Output management, input event injection/tracing, and Waybar text querying remain genuine unknown frontiers.

---

## 6. Tooling Disclosure
- **Tools installed/updated:** None. Existing host tools (`curl`, `jq`, `git`) were sufficient.
- **Host impact:** Zero mutation; zero writes to compositor, configuration, or shared files.
