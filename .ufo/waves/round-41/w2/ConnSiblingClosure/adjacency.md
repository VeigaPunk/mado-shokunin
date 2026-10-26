# Adjacency Audit & Sibling Closure — Round 41 (Wave w2)

- **Seat:** `ConnSiblingClosure`
- **Role:** UFO-FSD Connector
- **Target:** Attack: adjacency — does the lane absorb another lane's domain, and does the report need a sibling pointer?
- **Lane Repo:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Data Commit:** `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- **Freeze Commit (v2):** `294c667901a8c7b7165ba849d03cba9a24c14fa4`
- **Deliverable:** `.ufo/waves/round-41/w2/ConnSiblingClosure/adjacency.md`
- **Report:** `.ufo/waves/round-41/w2/ConnSiblingClosure.md`

---

## 1. Executive Summary & Audit Context

In mado round 41, two core deliverables landed:
1. **Claim C1 (operability):** `tools/mado-globals.py`, a tool that parses `xdg-desktop-portal-hyprland` log streams (`journalctl -o short-iso` or saved `--journal-file`) to inventory Wayland protocol globals advertised by the compositor.
2. **Claim C2 (coverage):** `corpus/knowledge/hyprland-focus-grab-r41.md`, analyzing the focus-grab-v1 protocol (`hyprland_focus_grab_v1` and `hyprland_focus_grab_manager_v1`), its C++ implementation in Hyprland (`CFocusGrab`), quickshell client lifecycle, and the relation to window focus rules.

In wave 1, seat `ConnSiblingOverlap` failed to produce an artifact or report file (`report.md:14-16,51-52`), leaving the round without an empirical cross-lane adjacency audit. Furthermore, `PROVINCE.md:32` contains an uncorrected tool table listing only 7 tools while 10 exist at HEAD (11 with `mado-globals.py`), and the draft additions in `w1/ScrSkillProvince` omit adjacent lane citations in the tool inventory table.

This audit executes a read-only scan across sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` and `corpus/knowledge` files) across four explicit potential domain bleed surfaces:
1. Wayland protocol security literature
2. XDG portals
3. Desktop process census
4. Journal parsing tools

For each surface, we provide grounded evidence, evaluate domain boundaries, determine whether it is an adjacency to report (not absorb), assign the authoritative arbiter lane, specify what the round report's "No cross-domain bleed" SHONEN box can truthfully state, and synthesize a bounded UFO-FSD Connector move that improves the declared axes.

---

## 2. Read-Only Scan of Sibling Lanes Across Four Overlap Surfaces

### Overlap 1: Wayland Protocol Security Literature & Upstream Trackers

- **What Round 41 Touched:**
  - `corpus/knowledge/hyprland-focus-grab-r41.md` analyzes client focus restriction:
    - Quote (`fetch/focus-grab-v1.xml:34-36`, 24 words):
      > "This protocol allows clients to limit input focus to a specific set of surfaces and receive a notification when the limiter is removed as"
    - Quote (`fetch/focus-grab-v1.xml:62-64`, 25 words):
      > "This interface restricts input focus to a specified whitelist of surfaces as long as the focus grab object exists and has at least one comitted"
  - It cites S287: `github.com/hyprwm/Hyprland/issues/565` ("Focus grab protocol / surface focus confinement", 2022).
  - In `round-41-lesson.md:46-47` and `registration.md:57`, mado explicitly **refused** staged entry `privileged-client-surface-r29.md` because it contained "generic Wayland analysis, one truncated quote, no measurement, no host state".
- **Sibling Lane Scan:**
  - `kasegi-shokunin/PROVINCE.md:3`:
    > "**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages"
  - `kasegi-shokunin/PROVINCE.md:25`:
    > "**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it."
  - `chousa-shokunin/PROVINCE.md:3`:
    > "**Domain:** deep-research method (調査) — the reusable craft of source research. Owns: question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification;"
- **Domain Analysis:**
  - `mado-shokunin` owns desktop & compositor craft on this host (`mado-shokunin/PROVINCE.md:3-4`):
    > "**Domain:** desktop & compositor craft — the Hyprland/waybar/walker configuration plane and display behavior on this host."
  - Mado owns the compositor-side focus grab mechanics (`CFocusGrab` seat grab allocation, keyboard/pointer focus routing) and how compositor window rules (`no_focus`, `no_initial_focus`, `stay_focused`) interact with client surfaces.
  - Mado does **not** own security evaluations, threat modeling, security context boundaries, privilege escalation analysis, or general vulnerability literature. Treating tracker issues (e.g. `issue-565`) as vulnerability/exploit research would bleed into `kasegi-shokunin`.
- **Decision:** **Adjacency to report, never absorb.**
- **Arbiter Lanes:**
  - **`kasegi-shokunin`** is the fleet arbiter for vulnerability analysis, security literature, and bounty scope.
  - **`chousa-shokunin`** is the fleet arbiter for source research methodology and citation hierarchy.

---

### Overlap 2: XDG Portals (`xdg-desktop-portal`, `xdg-desktop-portal-hyprland`, `portals.conf`)

- **What Round 41 Touched:**
  - `tools/mado-globals.py` runs:
    `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`
    to parse `Got interface: <name> (ver <ver>)`.
  - Quote (`fetch/xdph-PortalManager.cpp:88`, 10 words):
    > `Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);`
  - Quote (`fetch/xdph-journal.txt:117`, 10 words):
    > `2026-10-25T13:36:24-03:00 plazir27 xdg-desktop-portal-hyprland[1952]: [LOG]  | Got interface: hyprland_focus_grab_manager_v1 (ver 1)`
  - Held row S037 records `xdg-desktop-portal-hyprland v1.4.1` package identity, verified in `.ufo/waves/round-41/fetch/xdph-installed-version.txt`.
  - Historical note `corpus/knowledge/xdg-portal-routing-r12.md` analyzed `/usr/share/xdg-desktop-portal/hyprland-portals.conf`.
- **Sibling Lane Scan:**
  - `tsukuroi-shokunin/PROVINCE.md:3-4`:
    > "**Domain:** host operability & system repair (繕, mending) — the OS substrate itself: package state, systemd, drivers/firmware, boot health."
  - `tsukuroi-shokunin/PROVINCE.md:8-11`: owns pacman state (`pacman -Qkk`, foreign/AUR packages), systemd user units & timers (`systemctl --user`, unit files, failed states).
  - `tsukuroi-shokunin/PROVINCE.md:48` (ADJ-03):
    > "Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis -> mado. Mado verifies file/screenshot behavior itself."
  - `tsukuroi-shokunin/PROVINCE.md:124` (OUT-004): routes only lines 3–16 of `mado-shokunin/PROVINCE.md` (the config-plane half).
- **Domain Analysis:**
  - `tsukuroi-shokunin` owns package integrity (`xdg-desktop-portal-hyprland` package state) and systemd service unit health (`xdg-desktop-portal.service`, `xdg-desktop-portal-hyprland.service` active/failed states, socket activation).
  - `mado-shokunin` owns the configuration plane (`~/.config/hypr/xdph.conf` if configured, and `hyprland-portals.conf` candidate routes as they affect Hyprland display/screencast behavior).
  - In round 41, `mado-globals.py` uses `xdg-desktop-portal-hyprland` purely as a **passive, zero-socket witness** of compositor protocol advertisements: because safety rules strictly forbid running a live Wayland client or opening a Wayland socket, XDPH's logged startup discovery is the only on-disk evidence available. Mado does not claim ownership of portal health, unit lifecycle, or backend dispatch.
- **Decision:** **Adjacency to report, never absorb.**
- **Arbiter Lane:** **`tsukuroi-shokunin`** is the sole arbiter for portal package state, unit status, and OS substrate health.

---

### Overlap 3: Desktop Process Census

- **What Round 41 Touched:**
  - `corpus/knowledge/host-bar-producer-census-r40.md` inspected running processes (`pgrep -a -x hypridle`, `pgrep -f "^gpu-screen-recorder"`, `makoctl mode`) to evaluate Waybar chip outputs.
  - `tools/mado-verify.sh` executes `pgrep` queries for walker and waybar.
  - `tools/mado-globals.py` parses PID identifiers (`xdg-desktop-portal-hyprland[([0-9]+)]`) to partition journal logs into distinct sessions.
- **Sibling Lane Scan:**
  - `mori-shokunin/PROVINCE.md:3-4`:
    > "**Domain:** fleet & host observability (森) — whether the fleet, its waves and its host are alive and progressing."
  - `mori-shokunin/PROVINCE.md:6-10`: owns shokunin watchdog liveness (pid, start time, log freshness), kill/OOM-related records, cgroup memory events, and process silence grading.
  - `mori-shokunin/PROVINCE.md:48` (FR5): "Watchdog daemon identity and degraded-pgrep visibility... An unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity."
  - `souji-shokunin/PROVINCE.md:43-46`: refuses signaling inherited or unrelated processes; monitors process residue.
- **Domain Analysis:**
  - `mori-shokunin` owns system and fleet process census, daemon identity tracking, and process liveness observability.
  - `mado-shokunin` does not maintain a process table or daemon monitor. The process probes in `host-bar-producer-census-r40.md` and `tools/mado-verify.sh` are strictly **point-in-time chain evidence** for evaluating UI configuration rules (e.g. verifying whether a Waybar module script returns empty text or a glyph based on whether `hypridle` is running).
- **Decision:** **Adjacency to report, never absorb.**
- **Arbiter Lanes:**
  - **`mori-shokunin`** is the fleet arbiter for host process census and liveness observability.
  - **`tsukuroi-shokunin`** arbitrates systemd service process tracking.

---

### Overlap 4: Journal Parsing Tools

- **What Round 41 Touched:**
  - `tools/mado-globals.py` is a new Python tool that parses `journalctl -o short-iso` logs from `xdg-desktop-portal-hyprland`.
  - It handles boot headers (`-- Boot <boot_id> --`), timestamps, PIDs, session aggregation, session diffs (`--diff`), and expected interface validation (`--expect`).
- **Sibling Lane Scan:**
  - `mori-shokunin/PROVINCE.md:8-10,24-25`:
    Owns structured, MESSAGE-free journal records carrying catalog IDs from user/system journals; owns `tools/mori-journal-window.py --anchor PATH --scope user|system` (reading journal scopes from an operator-retained `mori-journal-anchor-v1` cursor); owns `tools/mori-oom-killers.py`.
    Extensive knowledge entries: `structured-journal-scopes-r13.md`, `journal-alarm-routing-r14.md`, `journal-positive-evidence-r15.md`, `journal-cursor-window-r16.md`, `journal-disk-usage-total-r51.md`.
  - `tsukuroi-shokunin/PROVINCE.md:11`:
    Owns journal/boot triage (`journalctl -b`, dmesg error classes). Knowledge: `journalctl-v262-field-filter-r36.md` (evaluating `journalctl` option rejection matrices across systemd versions).
- **Domain Analysis:**
  - Journal parsing tooling and cursor stream semantics are a core surface of `mori-shokunin`, with boot-level journal triage owned by `tsukuroi-shokunin`.
  - If `mado-globals.py` were a generic system journal reader or attempted cursor tracking across arbitrary units, it would severely encroach upon `mori-shokunin`.
  - However, `tools/mado-globals.py` is narrowly constrained:
    - Its invocation of `journalctl` is hardcoded to `--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`.
    - It extracts only lines matching `Got interface: <name> (ver <ver>)`.
    - Any other `-o` format or mismatch is rejected with `UNRECOGNIZED_FORMAT` (exit 4), avoiding silent fallbacks or general log parsing.
- **Decision:** **Adjacency to report, never absorb.**
- **Arbiter Lanes:**
  - **`mori-shokunin`** is the fleet arbiter for journal parsing tools, cursor window probes, and log stream abstraction.
  - **`tsukuroi-shokunin`** is the arbiter for journald system health and journalctl CLI option constraints.

---

## 3. What the Report's "No Cross-Domain Bleed" SHONEN Box Can Truthfully Say

Under the SHONEN promotion contract (`SHONEN.md:11-12`):
```markdown
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  Historical assertion: corpus/knowledge/province-accuracy-selfaudit.md round-5 receipt (VER-M4B); PROVINCE.md remains the read-only boundary, not a fresh outside-lane approval.
```

The round report (`report.md:150-153`) currently states:
```markdown
- [~] No cross-domain bleed — localized-channel material excluded (PROVINCE.md:75), adjacency declared (client lifecycle, security literature); w1/ScrSkillProvince/province-row.md drafted, not applied to PROVINCE.md.
```

### Truthful Specification for Box 4

Based on this audit, Box 4 **must remain `[~]` (HOLD)**. An author-side seat cannot check `[x]`, which requires a named non-author outside-lane verifier. However, the explanation can be made rigorous and complete:

```markdown
- [~] No cross-domain bleed (PROVINCE.md accurate; 4 adjacencies declared, not absorbed) —
  1. Localized-channel material strictly refused pursuant to PROVINCE.md:73-76 and PRED-C2-r41-v2 clause i.
  2. Running compositor state unmutated; no Wayland client socket opened.
  3. Four domain adjacencies audited and bounded without absorption:
     - Protocol security literature (hyprwm/Hyprland#565) → adjacent to kasegi-shokunin and chousa-shokunin.
     - XDG portal unit health and package state (xdph v1.4.1) → adjacent to tsukuroi-shokunin; mado reads the journal solely as a passive witness of advertised compositor protocols.
     - Desktop process checks (hypridle, gpu-screen-recorder, mako) → adjacent to mori-shokunin; treated strictly as point-in-time chain evidence for Waybar UI rules.
     - Journal parsing tool (tools/mado-globals.py) → adjacent to mori-shokunin (journal probe arbiter) and tsukuroi-shokunin (journald boot triage); tool is strictly bounded to xdph advert extraction.
  4. Tool inventory row and Round-41 addendum drafted (w1/ScrSkillProvince) but unapplied at HEAD; outside-lane verifier unassigned → stays [~].
```

---

## 4. Required Sibling Pointers for the Round Report Trailer

The round report (`report.md`) requires explicit sibling pointers to record these boundaries in the fleet ledger:

| Domain Surface | Adjacent Lane | Anchor | Declared Boundary |
|---|---|---|---|
| Wayland Protocol Security Literature | `kasegi-shokunin` | `kasegi-shokunin/PROVINCE.md:3` | Bounty & security research; mado owns only seat focus geometry and window rules |
| Source Hierarchy & Citation Chaining | `chousa-shokunin` | `chousa-shokunin/PROVINCE.md:3` | Source research method; mado adheres to source provenance rules |
| XDG Portal Units & Package Health | `tsukuroi-shokunin` | `tsukuroi-shokunin/PROVINCE.md:3,48` | OS substrate & systemd units; mado consumes XDPH logs strictly as a protocol witness |
| Process Census & Journal Tooling | `mori-shokunin` | `mori-shokunin/PROVINCE.md:3,24-25` | Observability & journal parsing tools; mado bounds `mado-globals.py` to XDPH adverts |

---

## 5. UFO-FSD Connector Move: Tripartite Sibling Pointer Closure with Bounded Tool Adjacency Annotation

### 1. Evidence
- `w1/ScrSkillProvince/province-row.md:34` drafted a tool inventory row for `tools/mado-globals.py` whose 4th column (`Owner and adjacent lanes`) names only mado and omits all adjacent sibling lanes (`mori`, `tsukuroi`).
- `w1/ScrSkillProvince/province-row.md:72-82` drafted Anchor D (Round-41 addendum) acknowledging security literature adjacency, but without naming the arbiter lane `kasegi-shokunin`.
- `report.md:14-16,51-52` records that w1 seat `ConnSiblingOverlap` died without publishing an artifact, leaving the round without a sibling boundary record.
- `report.md:126` notes that `PROVINCE.md:24-30` is stale, listing 7 tools while 10 exist at HEAD (11 with `mado-globals.py`).

### 2. Affected Axes
- **`adjacency` (IMPROVED):** Preemptively closes cross-domain friction with `mori-shokunin` (journal parsing), `tsukuroi-shokunin` (portal packaging/units), and `kasegi-shokunin` (security literature) by recording explicit, mutual boundaries.
- **`coverage` (IMPROVED):** Completes the four-surface overlap audit left empty by the missing w1 `ConnSiblingOverlap` seat.
- **`calibration` (IMPROVED):** Formulates an honest, evidence-grounded SHONEN Box 4 text keeping `[~]` (HOLD) with machine-verifiable citations.
- **Zero harm** to `operability` (`tools/mado-globals.py` and its 39 fixtures are completely unaffected), `depth` (`hyprland-focus-grab-r41.md` text is intact), or `freshness` (live receipts unchanged).

### 3. Proposed Move
**Synthesize the unlanded `w1/ScrSkillProvince` drafts with explicit sibling lane citations:**
1. **Update the `tools/mado-globals.py` inventory row in `PROVINCE.md`:**
   In Column 4 of the new row, append the adjacent lane designations:
   > `mado, round 41 (portal registry global census only; not general journal querying → mori; not portal unit/package management → tsukuroi)`
2. **Anchor the four arbiter lanes in the Round-41 PROVINCE addendum:**
   In the addendum text under `Adjacency — report, never absorb`, explicitly name `kasegi-shokunin` (security research), `chousa-shokunin` (source hierarchy), `tsukuroi-shokunin` (portal units), and `mori-shokunin` (process census and journal tooling).
3. **Integrate the four sibling pointers into the round report trailer (`report.md`).**

### 4. Second-Order Effects
- **Runtime Surface:** No change. `tools/mado-globals.py` runs with identical arguments, bubblewrap isolation, and execution bounds.
- **Contract Surface:** Eliminates latent ambiguity where sibling lanes scanning `PROVINCE.md` might assume mado is absorbing journal parsing or portal administration.
- **Substrate Surface:** Reaffirms read-only host discipline (`journalctl -o short-iso` read-only stream).
- **Verification Surface:** Sibling pointer table is fully traceable to committed PROVINCE.md files across the fleet.

### 5. Risks & Mitigation
- *Risk:* Future tool authors might attempt to add more `journalctl` queries to `mado-globals.py`.
- *Mitigation:* The tool's strict `UNRECOGNIZED_FORMAT` (exit 4) and hardcoded unit argument prevent scope expansion without deliberate code modification.

### 6. Verification
All 9 lifted quotes $\le 25$ words verified by `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/ConnSiblingClosure/verify-quotes.py`, recording 0 failures in `quote-verification.txt`.
