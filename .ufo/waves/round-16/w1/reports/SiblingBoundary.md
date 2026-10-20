# SiblingBoundary: desktop source reading vs host recovery vs package management (Round 16, w1)

**Seat:** `MadoR16.SiblingBoundary` (connector, leaf; no subagent dispatch).
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.
**Baseline:** `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
**Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-16/w1/reports/SiblingBoundary.md`.
**Status:** Complete. Read-only source reading of lane and sibling PROVINCE files and recorded corpus/wave evidence. No package, service, compositor, input or command probe was run. No edits outside this report.

---

## 1. Axes named

- **Primary judged axis: `adjacency`.** The assignment is ownership: which lane may read desktop source, and which lane owns host recovery and package management.
- **Axes the proposed move can move:**
  - `coverage` (C1): the U7 Waybar route and the source admission plan need to say which sources are desktop-owned and which are host-owned.
  - `operability` (C2): the static action-plan gate needs a fail-closed classification of desktop, host, package and service actions.
- **Watched, not moved:** `calibration` (do not read a bar glyph or a unit state as package or host health), `quality` (boundary claims need correct citations), `freshness` (the host is paused, so no current host state is claimed).

---

## 2. Province partition with anchors

### 2.1 Desktop source reading (mado-owned)

- `PROVINCE.md:3-4`: domain is the Hyprland/waybar/walker configuration plane and display behavior on this host.
- `PROVINCE.md:6-9`: owned surfaces are `~/.config/hypr/`, `~/.config/waybar/`, `~/.config/walker/`, terminal configs, declared themes/wallpapers, and screen/idle configuration.
- `PROVINCE.md:10-12`: the omarchy skill is read-only documentation. All config trees are read-only for this lane. The operator applies changes.
- `PROVINCE.md:14-16`: refuses secrets, model endpoints and model quality. Never mutates running compositor state. Every claim is file-byte or screenshot verified.
- `PROVINCE.md:18`: "Out of province → report, never absorb."

Reading upstream desktop documentation and source (Hyprland, waybar, walker, Wayland protocol XML) as static text is desktop-domain work. Examples in the lane: `corpus/SOURCES.md` rows for `custom.cpp` and the Waybar custom-module man page (reserved S053/S054 in this round).

### 2.2 Host recovery and package management (tsukuroi-owned, operator-owned remediation)

- `tsukuroi-shokunin/PROVINCE.md:8-14`: tsukuroi owns pacman state (`pacman -Qkk`, foreign/AUR census, receipt discipline), systemd user units and timers, journal and boot triage, and the driver/firmware plane. Update-safety questions ("what an -Syu would touch, what pins/holds exist") are also tsukuroi's.
- `tsukuroi-shokunin/PROVINCE.md:16-23`: additional surfaces are the Arch News gate, `.pacnew` drift, initramfs v42 and boot recovery, and the snapper/rollback net. Each has a corpus entry (`arch-news-gate-2026.md`, `initramfs-v42-sysroot-recovery.md`, and others).
- `tsukuroi-shokunin/PROVINCE.md:25-28`: "Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates."
- `tsukuroi-shokunin/PROVINCE.md:48` (ADJ-03): desktop rendering, bindings, menu or idle behavior needing configuration-level diagnosis goes to mado. Tsukuroi retains "user-manager/unit, package and driver health; an active unit does not prove the UI works." Mado verifies file and screenshot behavior itself.
- `tsukuroi-shokunin/PROVINCE.md:59-60`: "Select the matching row by the **question being asked**, not the binary or service name."
- `mori-shokunin/PROVINCE.md:12-16`: mori refuses OS package, systemd unit, driver/firmware and boot state (→ tsukuroi). Mori is "Detection and report only — never remediation" (`:16`).

### 2.3 Package management right now (paused)

- `.ufo/waves/round-16/w1/spec.json:3` (round-16 contract): all pacman transactions are PAUSED host-wide until an operator recovery decision. Forbidden: `-Sy`, `-Syu`, `-U`, `-R`, downgrade and service restart. After the pause, only an operator-authorized future install may use a real `pacman -Sp --print-format '%n %v'` plan plus a complete installed-name comparison. Any overlap refuses. The hard-coded fixture is not package validation.
- `~/.omp/agent/RULES.md:1-14` (tooling directive): any agent may install helpful tools through the channel order. Full-system upgrades go through tsukuroi's update-safety gate first. "Never run a partial upgrade (`pacman -Sy <pkg>`)."
- `corpus/lessons/round-15.md:15` (M2) and `corpus/lessons/round-15-verifier-spotcheck.md:254-277` (R15-V1, R15-V2): a wave seat ran `sudo pacman -S --needed --noconfirm libinput libinput-tools` for static inspection. That upgraded already-installed libinput (1.31.3-1 → 1.32.0-1) and pulled new packages. The orchestrator ruled it a forbidden partial upgrade. The guard requirement is the real `-Sp` plan with installed-name overlap refusal.
- `SKILL.md:467-475` and `corpus/QUALITY.md:72-78` (item 20): the lane-level restatement of the same rule.

### 2.4 Adjacent, not owned by this lane

- `mori-shokunin/PROVINCE.md:6-9`: mori reads journal and cgroup kill/OOM classes as fleet evidence. It does not own the OS state behind them.
- `souji-shokunin/PROVINCE.md:40-43`: souji acts on artifacts and never on processes or the OS.

---

## 3. Contradictions and unreconciled boundaries

Each item is stated with anchors. None is resolved by this seat.

**C-a. Tooling directive versus the round-16 pause.** RULES.md grants install authority to every agent and does not mention a package pause. The round-16 contract pauses pacman host-wide. The round-15 M2 lesson shows the directive's install channel produced a partial upgrade. Precedence used here: the later, more specific round-16 contract governs, and RULES.md's own "never partial upgrade" clause applies. This seat installed nothing. The directive's install permission does not extend to pacman during round 16.

**C-b. Lane's package-mutation boundary is misattributed and not followed.**
- `.ufo/waves/round-13/w1/SiblingOverlap.md:71` says: "Package mutation is strictly forbidden to `mado` and operator-owned (`RULES.md`)."
- The RULES.md text read today contains no such clause. It grants install authority to any agent (`RULES.md:3-4`). The claim is unsourced.
- The lane's own logs show package mutation by lane seats in round 13 (`LOG.md:798-799`, `wayland-utils`), round 14 (`LOG.md:974-976`, `lessons/round-14.md:111-115`, `wlr-protocols`) and round 15 (`LOG.md:1092-1093`, libinput partial upgrade).
- `PROVINCE.md` does not list package state among owned surfaces or refusals. The package boundary exists only in notes and the round-16 contract.
- Route to L1: an append-only correction that cites the round-16 contract and the M2 lesson, not RULES.md, as the source of the prohibition.

**C-c. hyprland.log reading.**
- `.ufo/waves/round-13/w1/reports/SiblingOverlap.md:32` says mado inspects `hyprland.log` for config syntax and parser errors only.
- `corpus/knowledge/province-accuracy-selfaudit.md:29-30` says the self-audit did not inspect "hyprland.log content", by discipline.
- Both are lane notes. No sourced rule in the corpus admits a hyprland.log read. Until one exists, the gate should classify hyprland.log reads as undecided and refuse them.

**C-d. Sibling self-description versus tsukuroi's own.** `souji-shokunin/PROVINCE.md:42` says tsukuroi "repairs host operability." Tsukuroi's own PROVINCE says "Detection and report; the operator remediates" (`tsukuroi-shokunin/PROVINCE.md:27-28`). Tsukuroi's self-description controls for tsukuroi's scope. Mado must not cite souji's wording as a license for host repair.

**C-e. The bar update glyph is not package evidence.**
- `corpus/knowledge/waybar-walker-semantics.md:136` records `custom/update`: exec `omarchy-update-available`, which runs `git ls-remote origin` against the omarchy checkout and compares it with local `git describe --tags`. On click it launches a floating terminal running `omarchy-update`.
- The corpus does not record the body of `omarchy-update` (`[UNK]`).
- The glyph reflects an omarchy checkout tag comparison. It says nothing about pacman state, and tsukuroi retains the package question.
- The on-click route is a package-state path by name only. Treat any plan containing it as refused.

**C-f. Wrapper commands hide the boundary.**
- `corpus/knowledge/walker-deep-r9.md:223-225` records `omarchy-restart-walker` running `systemctl --user restart elephant.service` and `systemctl --user restart app-walker@autostart.service`.
- The unit restart is a tsukuroi-owned user-manager mutation (`tsukuroi-shokunin/PROVINCE.md:10-11`, "systemd user units & timers"). Tsukuroi itself never restarts services (`:27`).
- Desktop-named units do not change the owner. A basename-only deny misses these wrappers.

**C-g. Git side effect on a read verb.** `corpus/knowledge/province-accuracy-selfaudit.md:110-128` (§3.5) records that `git status --porcelain` on the non-declared omarchy checkout refreshed the index stat cache. `waybar-walker-semantics.md:433` carries the matching E-candidate. A read-class command with a write side effect must be classified as not read-only, or invoked with `git --no-optional-locks` (or not at all) on foreign checkouts.

---

## 4. Proposed move (single bounded synthesis)

Adopt one province-tagged action classification for the C2 static gate, and reuse the same classes for C1 source admission. The classification is by the **question and effect** of the action, not by binary name, per `tsukuroi-shokunin/PROVINCE.md:59-60`.

| Class | Scope | Gate decision | Route |
|---|---|---|---|
| **D — desktop static read** | Lane-owned config bytes; tagged upstream desktop docs and source (Hyprland, waybar, walker, Wayland XML); module producer scripts read as source text | Admit as static read | Desktop evidence in mado |
| **H — host recovery** | Boot/initramfs/mkinitcpio/UKI; kernel, driver, modprobe, DKMS; `journalctl`/`dmesg` triage; snapper/rollback; `.pacnew`; udev; `/dev/input/*` | Refuse | ADJ-style packet to tsukuroi (`tsukuroi-shokunin/PROVINCE.md:44-52`) |
| **P — package management** | Any pacman or AUR helper invocation in any mode (`-S`, `-Sy`, `-Syu`, `-Sw`, `-U`, `-R`, `-Sp`); `omarchy-update`; any `pacman -Q*` used as a gate input is a read and is routed to tsukuroi, not counted as desktop evidence | Refuse. `-Sp` is refused during the pause. | Operator, via tsukuroi update-safety; round-16 pause governs |
| **S — unit, service, process mutation** | Any `systemctl` verb, including `--user restart` of desktop-named units; `omarchy-restart-*` wrappers; `pkill`/`kill` of bar, idle, notification or launcher processes; `hyprctl dispatch`, `keyword`, `reload` | Refuse | Operator; tsukuroi retains the unit |
| **Unknown or opaque wrapper** | `omarchy-*` scripts whose body is not read in the corpus; `sh -c`, `env`, `setsid`, `uwsm-app --`; any argv whose effect is not sourced | **Fail closed: refuse** | Report to integrator |

Rules that make the gate fail-closed:

1. Deny by default. Only class D admits. Everything else is refused with its route.
2. Classify by effect. A wrapper inherits the class of its body. If the body is not read and tagged, the wrapper is opaque and refused (C-f).
3. Source-quoted commands are data, never permission (round-16 contract).
4. Refuse `git status` on foreign checkouts unless invoked with `--no-optional-locks` (C-g).

**Why this move and not another.** It improves `adjacency` by naming three owners explicitly. It improves `operability` by making every host, package and service path refused by default. It improves `coverage` by letting U7 cite only class-D Waybar sources (module definitions, producer scripts as text, and tagged upstream man and custom.cpp) without any package or unit evidence. It harms no axis: no new probe, no new install, no new host claim. It does not require an operator decision to adopt.

**Risks.**
- Argv parsing for class decisions is hard. The gate must treat opaque wrappers as refused, not as unknown-but-allowed.
- Desktop and host overlap at the systemd user manager (C-f) will generate refusals on legitimate desktop questions. Each refusal should carry the ADJ-03 route so the question is answered by the owner, not dropped.
- Classification by question means the gate cannot be a basename list. Any basename list is a secondary aid, not the rule.

**Verification (for L1 to run once after integration, not by this seat).**
- Confirm the gate plan has no class-P or class-S token admitted: a grep-style check for `pacman`, `yay`, `paru`, `omarchy-update`, `systemctl`, `pkill`, `mkinitcpio`, `modprobe`, `udevadm`, `journalctl`, `hyprctl dispatch`, `hyprctl keyword`, `hyprctl reload`.
- Confirm every `omarchy-*` wrapper in the plan is either read-only-tagged or refused.
- Confirm C-b is corrected append-only and that no lane document still cites RULES.md as the package prohibition.

---

## 5. Limits

- Source reading only. No live compositor, service, input, screenshot or package probe was run. I did not open `/var/log/pacman.log`; the package evidence above is the repo's recorded evidence, not a fresh host read.
- The body of `omarchy-update` and of the `omarchy-restart-*` wrappers is not in the corpus. Their classes above are by effect as recorded, not by a verified script body.
- `hyprland.log` handling (C-c) and the git side effect (C-g) are unresolved in the corpus. This report does not decide them.
- Sibling PROVINCE files were read at their current state. Their declarations can drift; re-read before any later handoff.

---

## 6. Tooling record

- **Installed or updated:** none.
- **Package operations:** none. No pacman invocation of any mode, including `-Sp` and `-Sw`.
- **Service or process operations:** none. No `systemctl`, `pkill` or `hyprctl` call.
- **Subagents:** none dispatched.
- **Commands run:** read-only file reads only.
