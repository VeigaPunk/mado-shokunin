# Seat ConnSiblingClosure — Round 41 (Wave w2) Report

- **Seat:** `ConnSiblingClosure`
- **Role:** UFO-FSD Connector
- **Round:** 41 (hyaku run 7, 2026-10-25), Wave `w2`
- **Target:** Attack: adjacency — does the lane absorb another lane's domain, and does the report need a sibling pointer?
- **Lane Repo:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Deliverables:**
  - Artifact: `.ufo/waves/round-41/w2/ConnSiblingClosure/adjacency.md`
  - Quote Verification Script: `.ufo/waves/round-41/w2/ConnSiblingClosure/verify-quotes.py`
  - Quote Verification Receipt: `.ufo/waves/round-41/w2/ConnSiblingClosure/quote-verification.txt`
  - Report: `.ufo/waves/round-41/w2/ConnSiblingClosure.md`
- **Status:** COMPLETE.

---

## 1. Executive Summary

In round 41, `mado-shokunin` introduced two major artifacts:
- **C1 (operability):** `tools/mado-globals.py` (parses `journalctl -o short-iso` logs from `xdg-desktop-portal-hyprland` to census advertised Wayland globals without a socket connection).
- **C2 (coverage):** `corpus/knowledge/hyprland-focus-grab-r41.md` (analyzes `focus-grab-v1`, `CFocusGrab`, quickshell client usage, and window rule interactions).

In wave 1, seat `ConnSiblingOverlap` died without producing an artifact or report file (`report.md:14-16,51-52`), leaving the round with an unverified sibling boundary record. Furthermore, `w1/ScrSkillProvince/province-row.md:34` drafted a tool inventory row for `mado-globals.py` that omitted adjacent lane citations.

Seat `ConnSiblingClosure` audited all sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` and `corpus/knowledge` files) across four explicit overlap surfaces:
1. **Wayland protocol security literature:** adjacent to `kasegi-shokunin` and `chousa-shokunin`.
2. **XDG portals:** adjacent to `tsukuroi-shokunin`.
3. **Desktop process census:** adjacent to `mori-shokunin` and `tsukuroi-shokunin`.
4. **Journal parsing tools:** adjacent to `mori-shokunin` and `tsukuroi-shokunin`.

For all four, mado maintains strict boundaries: **adjacency to report, never absorb**. The round report's "No cross-domain bleed" SHONEN box 4 must truthfully remain `[~]` (HOLD) with machine-verifiable evidence.

---

## 2. Four Overlap Surfaces & Arbiter Lane Assignments

### Surface 1: Wayland Protocol Security Literature & Upstream Trackers
- **What Round 41 Touched:**
  - `corpus/knowledge/hyprland-focus-grab-r41.md` cites S287 (`hyprwm/Hyprland/issues/565`, "Focus grab protocol / surface focus confinement", 2022).
  - Quoted from `fetch/focus-grab-v1.xml:34-36` (24 words):
    > "This protocol allows clients to limit input focus to a specific set of surfaces and receive a notification when the limiter is removed as"
  - Quoted from `fetch/focus-grab-v1.xml:62-64` (25 words):
    > "This interface restricts input focus to a specified whitelist of surfaces as long as the focus grab object exists and has at least one comitted"
  - Staged entry `privileged-client-surface-r29.md` was refused for lacking host state/measurements.
- **Sibling Domain Evidence:**
  - `kasegi-shokunin/PROVINCE.md:3`: `**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages`.
  - `chousa-shokunin/PROVINCE.md:3`: `**Domain:** deep-research method (調査) — the reusable craft of source research. Owns: question framing; source hierarchy...`.
- **Finding & Boundary:** Mado owns desktop/compositor seat focus geometry (`CFocusGrab`) and window rules (`no_focus`). General vulnerability analysis, threat modeling, and security policy classifications belong to `kasegi-shokunin`.
- **Verdict:** **Adjacency to report, never absorb.**
- **Arbiter Lanes:** **`kasegi-shokunin`** (security literature/vulnerabilities) and **`chousa-shokunin`** (source hierarchy).

### Surface 2: XDG Portals (`xdg-desktop-portal-hyprland`, `xdg-desktop-portal`, `portals.conf`)
- **What Round 41 Touched:**
  - `tools/mado-globals.py` runs `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` to extract `Got interface: <name> (ver <ver>)`.
  - Quoted from `fetch/xdph-PortalManager.cpp:88` (10 words):
    > `Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);`
  - Quoted from `fetch/xdph-journal.txt:117` (10 words):
    > `2026-10-25T13:36:24-03:00 plazir27 xdg-desktop-portal-hyprland[1952]: [LOG]  | Got interface: hyprland_focus_grab_manager_v1 (ver 1)`
  - Held row S037 checks `xdg-desktop-portal-hyprland 1.4.1-2` via pacman (`fetch/xdph-installed-version.txt`).
- **Sibling Domain Evidence:**
  - `tsukuroi-shokunin/PROVINCE.md:3-4`: `**Domain:** host operability & system repair (繕, mending) — the OS substrate itself: package state, systemd, drivers/firmware, boot health.`.
  - `tsukuroi-shokunin/PROVINCE.md:8-11`: owns pacman state and systemd user units & timers (`systemctl --user`).
  - `tsukuroi-shokunin/PROVINCE.md:48` (ADJ-03): routes desktop configuration to mado; mado owns no unit health.
- **Finding & Boundary:** `tsukuroi-shokunin` owns OS packages, systemd unit health, and portal service lifecycle. Mado reads the portal log purely as a zero-socket, read-only witness of compositor protocol advertisements.
- **Verdict:** **Adjacency to report, never absorb.**
- **Arbiter Lane:** **`tsukuroi-shokunin`**.

### Surface 3: Desktop Process Census
- **What Round 41 Touched:**
  - `corpus/knowledge/host-bar-producer-census-r40.md` uses `pgrep -a -x hypridle`, `pgrep -f "^gpu-screen-recorder"`, `makoctl mode` to evaluate Waybar chip outputs.
  - `tools/mado-verify.sh` executes `pgrep` for walker/waybar.
  - `tools/mado-globals.py` extracts PIDs (`xdg-desktop-portal-hyprland[PID]`) from journal lines for session partitioning.
- **Sibling Domain Evidence:**
  - `mori-shokunin/PROVINCE.md:3-4`: `**Domain:** fleet & host observability (森) — whether the fleet, its waves and its host are alive and progressing.`.
  - `mori-shokunin/PROVINCE.md:6-10,48`: owns watchdog liveness, process runway, and daemon identity verification (`FR5`).
  - `souji-shokunin/PROVINCE.md:43-46`: monitors process residue, refusing to signal unrelated processes.
- **Finding & Boundary:** `mori-shokunin` owns host/fleet process census and liveness observability. Mado's process reads are strictly point-in-time chain evidence for UI display rules, not a host process census.
- **Verdict:** **Adjacency to report, never absorb.**
- **Arbiter Lanes:** **`mori-shokunin`** (host/fleet process observability) and **`tsukuroi-shokunin`** (systemd service processes).

### Surface 4: Journal Parsing Tools
- **What Round 41 Touched:**
  - `tools/mado-globals.py` parses `journalctl -o short-iso` logs from `xdg-desktop-portal-hyprland`.
  - Implements boot boundary tracking (`-- Boot <id> --`), timestamp/PID parsing, session diffs (`--diff`), and expected interface asserts (`--expect`).
- **Sibling Domain Evidence:**
  - `mori-shokunin/PROVINCE.md:8-10,24-25`: owns structured journal records with catalog IDs, `tools/mori-journal-window.py`, and `tools/mori-oom-killers.py`.
  - `tsukuroi-shokunin/PROVINCE.md:11`: owns journal/boot triage (`journalctl -b`, dmesg classes). Knowledge: `journalctl-v262-field-filter-r36.md`.
- **Finding & Boundary:** Mori and tsukuroi own journal parsing tooling, cursor window probes, and boot log triage. `mado-globals.py` is narrowly bounded to extracting `Got interface:` lines from one service unit; it explicitly rejects other formats (`UNRECOGNIZED_FORMAT`, exit 4) and is not a general journal tool.
- **Verdict:** **Adjacency to report, never absorb.**
- **Arbiter Lanes:** **`mori-shokunin`** (journal probe tooling) and **`tsukuroi-shokunin`** (journald daemon health & boot triage).

---

## 3. Truthful SHONEN Box 4 Specification

In `report.md:150-153`, the "No cross-domain bleed" SHONEN box 4 currently lacks specific evidence pointers. It **must remain `[~]` (HOLD)** because PROVINCE.md drafts are unmerged at HEAD and non-author outside-lane verification is pending.

Truthful text to integrate into `report.md`:
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

## 4. Required Sibling Pointers in Report Trailer

The round report must include these explicit sibling pointers:
- `kasegi-shokunin/PROVINCE.md:3` (Wayland protocol security literature)
- `chousa-shokunin/PROVINCE.md:3` (Source research hierarchy)
- `tsukuroi-shokunin/PROVINCE.md:3,48` (XDG portal service units & package state)
- `mori-shokunin/PROVINCE.md:3,24-25` (Process census & journal parsing tooling)

---

## 5. UFO-FSD Connector Move: Tripartite Sibling Pointer Closure with Bounded Tool Adjacency Annotation

1. **Evidence:**
   `w1/ScrSkillProvince/province-row.md:34` drafted an inventory row for `tools/mado-globals.py` whose Column 4 omitted all sibling lane adjacency names. `report.md:14-16,51-52` noted that w1's `ConnSiblingOverlap` seat died without publishing, leaving an unverified adjacency record.
2. **Affected Axes:**
   - **`adjacency` (IMPROVED):** Preemptively resolves latent domain tension with `mori`, `tsukuroi`, and `kasegi`.
   - **`coverage` (IMPROVED):** Closes all 4 overlap surfaces systematically.
   - **`calibration` (IMPROVED):** Grounded SHONEN Box 4 text preserving `[~]` (HOLD).
   - **Zero Harm:** `operability` (tool unchanged), `depth` (entry unchanged), `freshness` (receipts unchanged).
3. **Proposed Move:**
   - In `PROVINCE.md` Column 4 of `tools/mado-globals.py`:
     `mado, round 41 (portal registry global census only; not general journal querying → mori; not portal unit/package management → tsukuroi)`
   - In Anchor D (addendum), explicitly name arbiters `kasegi`, `chousa`, `tsukuroi`, and `mori`.
   - Append the 4 sibling pointers to `report.md`.
4. **Second-Order Effects:**
   - Runtime: zero impact (tool and sandbox unchanged).
   - Contract: clears PROVINCE.md ambiguity across sibling lanes.
   - Substrate: enforces zero-socket, read-only host discipline.
   - Verification: receipt-backed quote verification.
5. **Risks & Mitigation:**
   - Risk: tool scope creep. Mitigation: `tools/mado-globals.py` hardcodes the unit name and rejects unrecognized log formats with exit 4 (`UNRECOGNIZED_FORMAT`).
6. **Verification:**
   Script `.ufo/waves/round-41/w2/ConnSiblingClosure/verify-quotes.py` verified all 9 citations ($\le 25$ words) against raw source files; receipt `.ufo/waves/round-41/w2/ConnSiblingClosure/quote-verification.txt` records 0 failures.

---

## 6. Verification & Quote Check

```
VERIFYING QUOTES FOR ConnSiblingClosure:
[1] PASS (24 words): focus-grab-v1.xml:34-36 -> 'This protocol allows clients to limit input f...'
[2] PASS (25 words): focus-grab-v1.xml:62-64 -> 'This interface restricts input focus to a spe...'
[3] PASS (10 words): xdph-PortalManager.cpp:88 -> 'Debug::log(LOG, " | Got interface: {} (ver {})", I...'
[4] PASS (10 words): xdph-journal.txt:117 -> '2026-10-25T13:36:24-03:00 plazir27 xdg-deskto...'
[5] PASS (12 words): PROVINCE.md:3 -> '**Domain:** bounty & security research — scop...'
[6] PASS (19 words): PROVINCE.md:3-4 -> '**Domain:** host operability & system repair ...'
[7] PASS (19 words): PROVINCE.md:3-4 -> '**Domain:** fleet & host observability (森) — ...'
[8] PASS (16 words): PROVINCE.md:3-4 -> '**Domain:** desktop & compositor craft — the ...'
[9] PASS (7 words): PROVINCE.md:34 -> '**Out of province → report, never absorb.**...'

TOTAL: 9 checked, 0 failures.
```

- **Tool Installs:** None (python3 and standard coreutils used).
- **Mutating Git/JJ Executions:** None (strictly read-only inspection).
- **Host Changes:** None.
