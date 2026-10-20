# LibinputRecord — Scoped Report (Round 15, Wave w1)

- **Seat:** `MadoR15.LibinputRecord` (scout, leaf; no subagent dispatch).
- **Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/LibinputRecord.md`
- **Milestone:** U6 input evidence ladder and R14 ancillary provenance correction.
- **Judged axis:** `coverage` (C1 coverage: sourced U1–U5 5/7 → sourced U1–U6 6/7 via bounded input-debugging documentation route).

---

## 1. Pinned Primary Upstream Sources Opened

All sources were statically inspected and verified against the official libinput project repository hosted at `gitlab.freedesktop.org/libinput/libinput` and official documentation at `wayland.freedesktop.org`:

| Source Descriptor | Exact Location | Revision / Checksum | Check Method |
|---|---|---|---|
| **libinput HTML Documentation** | `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` | Header declares: "Helper tools — libinput 1.32.0 documentation"; section `libinput record and libinput replay` | `read` (2026-10-20), [INF-docs 1.32.0] |
| **libinput tools documentation source** | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` | Git tag `1.32.0` (`c7e6fe66f509ba2eda680c28aa64795987b49e7c`); `sha256: 53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f` | `read` & `sha256sum`, [OBS] |
| **libinput-record manual page** | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/tools/libinput-record.man` | Git tag `1.32.0` (`c7e6fe66f509ba2eda680c28aa64795987b49e7c`); `sha256: 89a08189f82308253f71f97c188fb3e85151044089dd5e2c56d6d2bbbf7a6445` | `read` & `sha256sum`, [OBS] |
| **libinput-record implementation** | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/tools/libinput-record.c` | Git tag `1.32.0` (`c7e6fe66f509ba2eda680c28aa64795987b49e7c`); `sha256: 06721130765f489be1e75e20b96e6bf21b01380f43ce1fc87dc9c5d4fa403e46` | `read` & `sha256sum`, [OBS] |

---

## 2. Exact Anchored Quotes: Privacy Warnings & Data Protection Constraints

Each verbatim quotation is $\le 25$ words, anchored to exact source lines in the pinned 1.32.0 release:

1. **Default keycode obfuscation for data protection**  
   - *Source:* `doc/user/tools.rst:262–263` (also rendered HTML `tools.html#libinput-record`)  
   - *Verbatim quote (18 words):*  
     > "For data protection, libinput record obscures key codes by default, any alphanumeric key shows up as letter “a”."  
   - *Scope:* Establishes that upstream acknowledges input recording poses an inherent data protection risk, necessitating default key masking. Does not prove recordings are confidential or leak-free.

2. **Obfuscation bypass via `--show-keycodes`**  
   - *Source:* `tools/libinput-record.man:64–66` (`OPTIONS` section)  
   - *Verbatim quote (20 words):*  
     > "Show keycodes as-is in the recording. By default, common keys are obfuscated and printed as KEY_A to avoid information leaks."  
   - *Scope:* Confirms the existence of an explicit override that completely unmasks raw keycodes, exposing plaintext keystroke contents.

3. **Explicit warning against sensitive data on HID capture**  
   - *Source:* `tools/libinput-record.man:75–78` (`OPTIONS` section)  
   - *Verbatim quote (17 words):*  
     > "Record hidraw events alongside device events. DO NOT TYPE SENSITIVE DATA. See RECORDING HID REPORTS for more details."  
   - *Scope:* Upstream capitalized imperative warning confirming raw HID data collection exposes sensitive input.

4. **HID reports non-obfuscation and keystroke recovery**  
   - *Source:* `tools/libinput-record.man:134–136` (`RECORDING HID REPORTS` section)  
   - *Verbatim quote (18 words):*  
     > "HID reports are not obfuscated and a sufficiently motivated person could recover the key strokes from the logs."  
   - *Scope:* Documents that USB/HID raw report streams bypass all evdev key masking, permitting keystroke reconstruction.

5. **Explicit password warning during HID recording**  
   - *Source:* `tools/libinput-record.man:135–136` (`RECORDING HID REPORTS` section)  
   - *Verbatim quote (8 words):*  
     > "Do not type passwords while recording HID reports."  
   - *Scope:* Direct upstream admonition identifying password exposure as an active hazard during HID device recording.

6. **Privilege constraint for kernel node access**  
   - *Source:* `doc/user/tools.rst:31` (also rendered HTML `tools.html#helper-tools`)  
   - *Verbatim quote (18 words):*  
     > "Most of the tools must be run as root to have access to the kernel’s /dev/input/event* device files."  
   - *Scope:* Documents that accessing the event layer requires superuser privilege.

7. **Root privilege requirement for recording**  
   - *Source:* `tools/libinput-record.man:9–10` (`DESCRIPTION` section)  
   - *Verbatim quote (12 words):*  
     > "This tool needs to run as root to read from the device."  
   - *Scope:* Establishes that `libinput record` cannot operate without elevated administrative privilege.

8. **Independence from desktop/compositor context**  
   - *Source:* `doc/user/tools.rst:220` (also rendered HTML `tools.html#libinput-record`)  
   - *Verbatim quote (12 words):*  
     > "The recorded events are kernel events and independent of the libinput context."  
   - *Scope:* Demonstrates that kernel recording captures raw kernel device streams, not compositor-applied policy or focused client delivery.

---

## 3. Why Recording Is NOT Authorized Here

Executing `libinput record` (or any equivalent live input capture) is strictly rejected across multiple independent architectural, safety, and contractual axes:

### A. Inviolable Contractual & Wave Boundary
- **Wave Mandate:** Round 15 contract strictly decrees: *"No new capability or input event collection; retain unexercised delivery/IME/kernel limits... All seats leaf, no tests/gates/build/lint/formatters/smoke runs or live probes... no input event reading/recording/replay/injection, compositor action or hardware/kernel diagnosis."*
- **Rubric Scope (C1 Coverage):** The milestone requires admitting a *bounded input-debugging layer route* grounded in primary documentation (`[INF-docs]`), explicitly prohibiting live input capture, injection, or kernel diagnostic tools (`SCORECARD.md:592–593`).

### B. Elevated Administrative Privilege (`sudo`)
- Per upstream documentation (`tools.rst:31`, `libinput-record.man:9–10`), capturing events requires root access to `/dev/input/event*` nodes.
- Running `sudo libinput record` violates the principle of least privilege, leaf execution safety, and mado's unprivileged user-session fence.

### C. Keystroke Leakage and Incomplete Redaction Hazards
- **Partial Masking Only:** Examination of `tools/libinput-record.c:159–185` (`obfuscate_keycode`) proves that evdev masking only replaces keycodes 2–57 and 71–83 with `KEY_A`.
- **Unmasked Control Keys:** Crucial keys—such as `KEY_ESC` (1), `KEY_TAB` (15), `KEY_ENTER` (28), `KEY_LEFTCTRL` (29), `KEY_CAPSLOCK` (58), function keys `KEY_F1`–`KEY_F10` (59–68), `KEY_F11`–`KEY_F12` (87–88), and `KEY_LEFTMETA` (125)—are transmitted completely unmasked.
- **Timing Leakage:** Inter-event timestamps and deltas (`%+dms` on `SYN_REPORT`) are retained verbatim. Timing analysis over preserved modifier and control key sequences exposes user interaction patterns, typing cadence, and structural content.
- **Total Obfuscation Failure:** Any execution using `--show-keycodes` or `--with-hidraw` completely disables obfuscation, directly capturing credentials, tokens, or private text in plain text.

### D. Persistent Device Identity & Machine Metadata Exposure
- When initialized, `libinput record` invokes `print_device_description` (`record.c:1889–1898`, `1498–1530`), which dumps hardware bus IDs, vendor IDs, product IDs, model names, serial numbers, DMI strings, and filtered udev properties into the output YAML file.
- Persisting or transmitting raw device descriptors violates anonymization standards and the lane's data-retention rules (`QUALITY.md:50–55`).

### E. Out of Province
- `PROVINCE.md:6–9` circumscribes mado's ownership to Hyprland compositor configuration (`~/.config/hypr/`), Waybar, Walker, and desktop styling.
- Kernel device nodes (`/dev/input/event*`), kernel evdev subsystems, and USB/HID controller hardware are strictly out of province, routing to `tsukuroi-shokunin` (kernel/hardware/boot layer) or remaining uncollected.

### F. Desktop Interference and Mutating Hazards
- Using `libinput record --grab` exclusively seizes input nodes (`record.c:2433`), cutting off event propagation to Hyprland and rendering the interactive desktop unresponsive.
- Furthermore, recorded YAML files are designed to feed `libinput replay`, which utilizes the Linux `uinput` kernel module to construct virtual devices and inject synthetic input into the live session—an unauthorized active mutation.

### G. Sufficiency of the Documentation Ladder
- Sourced static evaluation of upstream official release documentation fulfills the U6 input-debugging ladder safely and completely as an `[INF-docs]` reference model without exposing sensitive user inputs or executing invasive kernel-level commands.

---

## 4. Evidence Class Tags

- `[OBS]`: Static file inspections and checksum verifications of the pinned upstream `libinput 1.32.0` release artifacts.
- `[INF-docs 1.32.0]`: Specifications, command arguments, and privacy warnings documented in official libinput 1.32.0 manual pages and documentation.
- `[UNK]`: Live event delivery to sandboxed Wayland clients, IME composition pathways, and kernel hardware dynamics remain unexercised.

---

## 5. Tooling & Install Record

- **Tool installs or updates:** None (0 installed, 0 updated).
- **Inspection commands executed:**
  - `pacman -Q libinput` (package inspection: observed `libinput 1.31.3-1` installed without CLI binaries).
  - `git ls-remote --tags` (verified commit `c7e6fe66f509ba2eda680c28aa64795987b49e7c` for tag `1.32.0`).
  - Read-only static fetches and SHA-256 verifications of upstream documentation and man pages.
- No live probes, input capturing, event recording, replay, injection, or test gates were executed.
