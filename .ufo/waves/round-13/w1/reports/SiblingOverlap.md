# SiblingOverlap Report — Protocol Diagnostics vs Input/Kernel Lane and System Maintenance

**Seat:** `MadoR13.SiblingOverlap` (connector, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** exact-set census and sourced U4 boundaries (Round 13, Wave 1)  
**Judged on:** `coverage`, `operability`  
**Output Draft:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/SiblingOverlap.md`

---

## 1. Scope & Task Verification

- **Assignment:** Scan `PROVINCE.md` and adjacent fleet province descriptions read-only to establish protocol diagnostics ownership vs input/kernel lane and system maintenance; report, do not absorb.
- **Constraints Met:**
  - Written strictly to `.ufo/waves/round-13/w1/SiblingOverlap.md` and `.ufo/waves/round-13/w1/reports/SiblingOverlap.md`.
  - Absolute source paths used for all citations.
  - No build, test, lint, or formatting runs invoked.
  - Read-only scanning of fleet provinces (`mado`, `tsukuroi`, `mori`, `tabi`, `souji`, `kama`, `kagi`, `kumitate`).
  - No subagent dispatch (leaf seat).
  - Tooling directive: 0 tools installed or updated.

---

## 2. Key Findings

1. **Protocol Advertisement vs Kernel Hardware:**
   - Wayland interface advertisement (`wl_registry.global`, `wayland-info`) and compositor protocol negotiations are strictly owned by `mado-shokunin` as part of desktop display behavior (`mado-shokunin/PROVINCE.md:3-4`).
   - Kernel input events (`/dev/input/event*`), hardware probing (`evtest`, `evemu`, `libinput debug-events`), and DRM/KMS/video drivers belong strictly to the host substrate / system repair lane (`tsukuroi-shokunin/PROVINCE.md:3-14`). They must never be absorbed by `mado`.

2. **Journal & Process Death:**
   - Host triage, boot health, and journal analysis (`journalctl -b`) belong to `tsukuroi-shokunin`. Fleet liveness and cgroup memory/kill events belong to `mori-shokunin`.
   - `mado-shokunin` inspects compositor logs (`hyprland.log`) for config syntax/parser errors only. It does not absorb journal triage or OOM debugging.

3. **Adjacency Handoff (ADJ-03):**
   - When compositor failures stem from driver/firmware degradation or missing system packages, `mado` routes findings via ADJ-03 to `tsukuroi-shokunin`, preserving "report, never absorb".

---

## 3. Second-Order Impact

- **Coverage (C1):** Enables clean progression from $3/7 \rightarrow 4/7$ coverage by grounding U4 in advertised protocol globals and protocol phasing without leaking into ungrounded kernel claims.
- **Operability (C2):** Keeps verification checks hermetic and unprivileged, avoiding spurious failures in environments without evdev or root access.
