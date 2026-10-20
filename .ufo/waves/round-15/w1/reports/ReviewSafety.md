# ReviewSafety — round 15 (mado-r15-w1) — U6 input-debugging integration risk

Scope: adversarial review of the U6 input-debugging layer route under PROVINCE.
Question: can the admitted U6 note stay inside "no input injection, no replay, no kernel diagnosis, no raw input capture"?
Verdict: **conditionally acceptable as a documentation-only ladder**. Acceptance requires the conditions in §3 and none of the rejection triggers in §4. Two source-registry defects block admission as currently planned (F1, F3).

Tags: `[OBS]` measured here · `[INF-docs]` upstream documentation · `[INF]` inference · `[UNK]` unknown.

## 0. Actions and tooling record

- Read-only inspection only: lane artifacts, PROVINCE, SKILL, SCORECARD, LOG, corpus notes and registry, the round-15 `spec.json` item `ReviewSafety` (spec.json:152-156), and the libinput 1.32.0 documentation pages (`tools.html`, `reporting-bugs.html`) via static fetch.
- Static host checks, nothing executed against devices: `sha256sum /usr/share/wayland/wayland.xml`; `grep -nE` on that file; `command -v libinput`; `pacman -Q libinput wayland` (package query).
- Not run: any libinput subcommand, `wayland-info`, `hyprctl`, `sudo`, `evemu`, any `/dev/input` access, any test, gate, linter or formatter. No delegation. No `~/.omp/agent/agent.db*`, credential or auth file opened. `omp` CLI not launched.
- Tool installs or updates by this seat: **none**. Pre-existing state observed, installer unknown: `/usr/bin/libinput`, `libinput 1.32.0-1` (`pacman -Q`), and `wayland 1.26.0-1`. The scout record `.ufo/evidence/round-12/l2-scout.md:3` measured libinput **absent** on 2026-10-19. This is drift and is routed as F2.

## 1. Evidence checked

| Pointer | What it establishes |
|---|---|
| `PROVINCE.md:6-9` | Mado owns `~/.config/hypr/`, waybar, walker, terminals, themes, screen/idle. Input devices and kernel input are not enumerated. |
| `PROVINCE.md:14-18` | Refuses secrets, endpoints, model quality. Never mutates running compositor state. "Out of province → report, never absorb." |
| `SKILL.md:218-240` | Safety fence: hyprctl read-verb whitelist (220-224, includes `devices`); "No firing, no injection" incl. keystroke injection (225-226); session material shape-only (234-236); unverifiable → UNKNOWN (237-240). libinput, evdev, uinput, `/dev/input`, sudo and recording files are **not** named. |
| `SCORECARD.md:598-621` | Round-15 declared claim: C1 coverage 5/7 → 6/7 by bounded route. Excludes "kernel diagnosis, device/event reading, replay, input injection". Requires `covers: U6`, provenance trio, reciprocal S051/S052 joins, headings `## Layer ladder`, `## Safe boundary`, `## Unexercised delivery` with `[UNK]` last. |
| `corpus/SOURCES.md:19` (S007) | libinput tools docs row, **status `queued`**, anchor "libinput 1.32.0 documentation (opened 2026-10-19)", no repo revision. Same URL as S051 would use. |
| `corpus/SOURCES.md:34` (QUALITY 17) and `corpus/QUALITY.md:34-40` | Repeated canonical URLs must be screened; duplicates are rejected/merged or a genuine superseding row with a resolvable prior id is required. |
| `corpus/SOURCES.md:115` | Owed-anchor rule: a queued row mined later needs a superseding row with the source-repository commit. |
| `corpus/SOURCES.md:61` (S049) and `corpus/knowledge/wayland-protocol-boundaries-r13.md:89,121` | Installed `/usr/share/wayland/wayland.xml` pinned at sha256 `cc860987…5f07`. Retained S041 data scope correction. |
| `corpus/knowledge/wayland-protocol-boundaries-r13.md:8` | U6 kernel-input ladder explicitly not closed by U4. |
| `corpus/knowledge/output-colour-boundaries-r14.md:108` | U6 explicitly outside U5. |
| `corpus/QUALITY.md:50-55` (criterion 19) | Scope retained-data statements to field/record class. |
| `corpus/lessons/round-14-verifier-spotcheck.md:169` (R14-V1) | Ancillary receipt precision debt. Unscored correction, not a U6 issue. |
| `/usr/share/wayland/wayland.xml` (static) | sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` (matches S043 pin). Contains `wl_seat` v11 at line 2004, `wl_pointer` v11 at 2138, `wl_keyboard` v11 at 2573. |
| `tools.html#libinput-list-devices` [INF-docs] | "This tool does **not** show your desktop's configuration, just the libinput built-in defaults." Output "intended for human-consumption and may change its output at any time." |
| `tools.html` root note [INF-docs] | "Most of the tools must be run as root to have access to the kernel's `/dev/input/event*` device files." |
| `tools.html#libinput-debug-events` [INF-docs] | "prints events from devices and can help to identify why a device behaves different than expected." |
| `tools.html#libinput-record-and-libinput-replay` [INF-docs] | `record` records kernel events from a device node. "For data protection, libinput record obscures key codes by default, any alphanumeric key shows up as letter 'a'." `replay`: "creates a new virtual device based on the description in the log file." `record --no-events` prints the device description and exits. |
| `tools.html#libinput-record-s-autorestart-feature` [INF-docs] | `--autorestart` writes event recordings to files on disk as the device is used. |
| `reporting-bugs.html#reporting-keyboard-bugs` [INF-docs] | "libinput does not handle keyboard layouts and merely forwards the physical key events." |
| `reporting-bugs.html#reporting-touchpad-bugs`, `#udev-information-for-the-device` [INF-docs] | Requests a virtual device description, `udevadm info`, vendor model, `/sys/class/dmi/id/modalias`, and `libinput measure touchpad-size` on the device. |

## 2. Findings (by severity)

**F1 — HIGH, blocks admission. S051 collides with queued S007.**
S007 (`SOURCES.md:19`) already names the same URL, `wayland.freedesktop.org/libinput/doc/latest/tools.html`, with status `queued`. The round-15 reservation "S051 libinput 1.32 tools docs" would create a second active row on that URL. QUALITY 17 forbids a silent duplicate. The `latest` path is also not a revision pin, and `SOURCES.md:115` owes one.
Acceptance: either (a) promote S007 in place (status `queued` → `mined`, used-by → U6 note, change logged old→new) and pin the libinput 1.32.0 source tag/commit with sha, or (b) a superseding row whose `teaches` begins `supersedes S007 —` with that pin. Reject a new S051 with the same URL and no supersedes link.

**F2 — HIGH, safety drift. libinput is now installed.**
`/usr/bin/libinput` is present, `libinput 1.32.0-1` per `pacman -Q`. The scout measured it absent on 2026-10-19 (`l2-scout.md:3`). Its installer and date are `[UNK]`, and no record in this round names one. The presence raises the risk that a later seat runs `sudo libinput debug-events` or `record`.
Acceptance: the U6 note records the package state (`pacman -Q libinput` → `1.32.0-1`, observed 2026-10-20, installer `[UNK]`) and states that no subcommand was executed. Permitted invocations are documentation and help only (`libinput --help`, `man libinput-*`); `--version` is acceptable. Any other subcommand is a §4 rejection.

**F3 — HIGH, blocks admission. S052 duplicates the installed S043 file.**
The "exact revision" wl_keyboard/wl_pointer source is `/usr/share/wayland/wayland.xml`. Its sha256 `cc860987…5f07` is already S043's pin (`SOURCES.md:55`). `wl_seat`, `wl_pointer` and `wl_keyboard` all live in that file (lines 2004, 2138, 2573), so a new S052 citing the same bytes is a duplicate with a different id.
Acceptance: reuse S043 with an in-place `used-by` addition and a new anchor at lines 2004/2138/2573 (logged old→new). Or fetch the upstream Wayland core tag with its own sha and a superseding row. Either way, state that `1.26.0-1` link-time provenance remains `[UNK]`, as in the r13 note.

**F4 — MEDIUM. Route boundary: `list-devices` is not compositor config.**
Acceptance: the ladder must quote the `list-devices` "built-in defaults" note and must not present its output as Hyprland's effective input configuration. Effective values come only from `hyprctl -j getoption input:*` (already in `hyprctl-verification-layer.md` §3.2). Reject any row that equates the two.

**F5 — MEDIUM. Privacy class of the libinput routes.**
- `debug-events` prints live events from devices. Keystroke-level output is a keylogger-class surface. Reject as a route.
- `record` obscures alphanumeric keys "by default" only. The obscuring is a default, not an absence of key content, and the override option is in `libinput-record(1)`, which is unopened (`[UNK]`). Recordings persist to disk, and `--autorestart` rotates them.
- `reporting-bugs` asks for udev properties, `/sys/class/dmi/id/modalias` and vendor model. These are hardware identifiers, which are out of province and are session/hardware material under SKILL.md:234-236.
Acceptance: the note lists these as rejected routes with their anchors, and no retained output, device names, udev, modalias or DMI values appear in any artifact.

**F6 — MEDIUM. Ownership: kernel-input diagnosis is out of province.**
PROVINCE.md:6-9 does not list input devices. The kernel and driver plane belongs to tsukuroi (`tsukuroi-shokunin/PROVINCE.md:11-14`: journal/boot, `dmesg` error classes, driver/firmware). Its ADJ-03 routes only configuration-level desktop behavior to mado (`tsukuroi-shokunin/PROVINCE.md:48`).
Acceptance: the note's Safe boundary names kernel `/dev/input`, `dmesg`, evdev state and driver state as out-of-province, with report-route to tsukuroi. It must not present any kernel-level read as lane evidence.

**F7 — MEDIUM. The SKILL fence does not name the input routes.**
`SKILL.md:218-240` covers hyprctl verbs and keystroke injection (`:225`). It does not name libinput, evdev, uinput, `/dev/input`, `sudo`, recordings or replay. The U6 note is therefore the only place these are fenced.
Recommendation only, owned by L1: add a SKILL rule listing the forbidden input routes. Until that lands, the U6 `## Safe boundary` section must enumerate them (see §3, item 4).

**F8 — LOW. `hyprctl devices` is whitelisted but not shape-limited.**
`SKILL.md:220-221` includes `devices`. The admitted notes use it for counts and shape (`hyprctl-verification-layer.md:13`). There is no explicit rule that device names, ids or keymap strings are not retained.
Acceptance: any U6 host row cites counts or shape only, and reproduces no device name or id, following the S041/S049 retention precedent (`QUALITY.md:50-55`).

**F9 — INFO. Keyboard layout is not a libinput-layer fact.**
`reporting-bugs.html#reporting-keyboard-bugs` states that libinput "does not handle keyboard layouts". The host's `kb_layout` `br` (`input.conf:10`, `hyprctl-verification-layer.md` §3.2) is a compositor/XKB fact. The U6 ladder must not place it in the libinput row.

## 3. Acceptance conditions (all required)

1. Registry: S051 is either S007 promoted in place with a pinned libinput 1.32.0 source, or a superseding row with `supersedes S007`. S052 is S043 reused, or a pinned upstream core row with its own sha. No duplicate-URL row without a supersedes link (F1, F3).
2. Headings present: `## Layer ladder`, `## Safe boundary`, `## Unexercised delivery`, with `[UNK]` in the last (SCORECARD.md:605-608). The provenance trio is present and the note carries exactly `covers: U6`.
3. Ladder rows each state what they prove and what they do not. Layers, kernel node → libinput → compositor (Hyprland `getoption`/`devices` counts) → `wl_seat`/`wl_keyboard` interface → client receipt. A `[INF-docs]` row is never promoted to host behavior (QUALITY 15-16). `libinput` output is not delivery evidence (F4).
4. Safe boundary enumerates the forbidden routes, each with its tools.html or reporting-bugs anchor: `debug-events`, `record` (including `--autorestart` and `--no-events`), `replay`, `measure`, `analyze`, `list-devices`, `list-kernel-devices`, `quirks`, `debug-gui`, any `sudo`, any `/dev/input` access, `evemu-*`, `uinput`/virtual-device tools, `dmesg`, and udev/modalias/DMI capture. It states that no such route was executed and that the lane's fence is unchanged.
5. Unexercised delivery lists at least: event delivery to clients, IME, keyboard-layout application, kernel and driver behavior, libinput defaults as applied by Hyprland, and any device-specific behavior. Each is `[UNK]`.
6. Quotes are ≤25 words and anchored to the doc sections named in §1. Host state is cited only from the read verbs already in the fence.
7. The package state (F2) is recorded with its command and date.

## 4. Rejection triggers (any one fails the U6 milestone)

- R1: any libinput subcommand other than help/version executed, or any device-touching invocation, including `list-devices` and `record --no-events`.
- R2: any `sudo` used for input tooling in this lane.
- R3: any input event read, recording, replay, injection or virtual-device creation, including `evemu`, `uinput`, `wtype` and `ydotool`.
- R4: a claim that libinput defaults equal the effective Hyprland configuration (F4).
- R5: a claim that the keyboard layout is libinput-owned (F9), or that a debug or record run proves application delivery (criterion 3).
- R6: any persisted recording, udev property, modalias, DMI value, vendor model, device name or device path (F5, F8).
- R7: any kernel or driver diagnosis under this lane (F6).
- R8: a new S051 or S052 row that duplicates an existing URL or file without a supersedes link or in-place reuse (F1, F3).
- R9: an unsupported "U6 complete", "full input coverage" or "delivery verified" claim. Coverage counts `covers: U6` only.

## 5. Residual risk and verification gaps

- The libinput man pages (`libinput-record(1)`, `libinput-debug-events(1)`, `libinput-replay(1)`) were not opened. Per-subcommand privilege, the obscuring override and the exact `--no-events` behavior are `[UNK]` until static man-page reads are done.
- The Hyprland-side use of libinput is not sourced here. Hyprland's internal libinput integration is `[UNK]`.
- The installed libinput package (F2) has no installer record. Its provenance is unverified.
- No independent non-author verdict on the U6 note exists yet. Per LOG/SHONEN, this review is authoring-lane advice, not clearance.
- Verification the main agent should run after the note lands: the registry collision check (`sources-census.sh validate`), `python3 .ufo/waves/round-15/measure.py REV`, and `pacman -Q libinput`. No libinput execution.
