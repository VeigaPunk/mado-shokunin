# AttackSynthetic — critic report (mado r15 w1)

Seat: MadoR15.AttackSynthetic (critic, leaf). Target: any assertion that `libinput replay` or a uinput virtual input device is a harmless, read-only probe.

**Verdict: falsified on every reading.** `replay` and uinput device creation are **injection and mutation class**. `record` and `debug-events`, including `record --no-events`, are **device-access and input-read class**. None of them is a probe. On this host, root is not the barrier: the tools now run without `sudo`.

Tags: `[OBS]` measured here (static or metadata only) · `[DOC]` official upstream text or code · `[INF]` inference.

## Boundary of this seat
- No libinput subcommand was executed, no `/dev/input` or `/dev/uinput` node was opened, and no event was read, recorded, replayed or injected. No compositor action and no `sudo`.
- Metadata-only host reads:
  - `pacman -Q/-Qi/-Ql`
  - `stat` and `getfacl` on `/dev/uinput`
  - a `stat` permission histogram of `/dev/input/event*` (no names)
  - `id -nG`
  - static reads of `/usr/lib/udev/rules.d/{60-steam-input,70-power-switch}.rules`
  - `sha256sum` and `grep` of `/usr/lib/libinput/libinput-replay`
- Static upstream reads:
  - libinput tag `1.32.0` (shallow clone, HEAD `5cf833b572f5`), plus the `1.31.3` raw `libinput-replay.py`, `libinput-replay.man` and `src/quirks.c`
  - `tools.html`
  - kernel `docs.kernel.org/input/uinput.html`
- `/tmp/attacksyn-*` scratch was deleted.
- Tool installs/updates by this seat: **none**.

## Fence as it stands
- `SKILL.md:218-240` is the "mutation-free fence". Rule 1 is a hyprctl read-verb whitelist and includes `devices` (`:220-221`). Rule 2 says "No firing, no injection", with keystroke injection and dispatchers as the named examples (`:225-230`).
- The fence does not name libinput, evdev, uinput, `/dev/input`, recordings or replay.
- `corpus/SOURCES.md:19` (S007, queued) groups "debug-events/record/replay" as material that "scopes what an input probe could ever measure". In effect it files replay under *probe*. That is the assertion attacked below.

## Counterexamples

**CE1 — `replay` is injection by definition (HIGH).**
- [DOC] `tools.rst:276`: "`libinput replay` creates a new virtual device based on the description in the log file."
- [DOC] `libinput-replay.man:9-10`: needs root "to create a device and/or replay events."
- [DOC] kernel uinput §7.1: events sent through a virtual device "will be delivered to userspace and in-kernel consumers."
- [DOC] Code at 1.32.0: `create_uinput_device()` is at `libinput-replay.py:148`; `uinput.send_events(evs)` is at `:224`.
- [OBS] The installed `/usr/lib/libinput/libinput-replay` has sha256 `c8cd3fa9…3f93`, byte-identical to upstream 1.32.0. Upstream 1.31.3 differs only in style, with no semantic change.
- Consequence: `record` output obscures keys to `KEY_A` by default (`tools.rst:262`). Replaying a keyboard recording therefore types into whichever client has focus, for example a terminal running a shell.

**CE2 — creating the device with zero events still mutates the session (HIGH).**
- [DOC] `UI_DEV_CREATE` makes the kernel create a device node (uinput §7.4.1). [INF] udev then announces it and the compositor's libinput adds it on hotplug.
- [OBS-prior] The lane's own device measurement is hotplug-sensitive. `corpus/knowledge/config-health-report-r3.md:412-416` counted 9 devices, including the `hl-virtual-keyboard-fcitx5` virtual node.
- A replay device would therefore change the output of the whitelisted `hyprctl devices` probe. The lane would be contaminating its own measured substrate, which is an identity change.
- [DOC] systemd `70-power-switch.rules` tags *any* `event*` node with `ID_INPUT_KEY=1` or `ID_INPUT_SWITCH=1` as `power-switch`. [INF] A replayed recording of the Power Button or Lid Switch (both shown as recordable in `tools.html` §record) reaches logind's power-key and lid handling, so the outcome could be suspend or power-off.

**CE3 — replay writes into the live compositor's quirks path (HIGH).**
- [DOC] `libinput-replay.py:311-339` (`setup_quirks`) does `mkdir` on `$XDG_RUNTIME_DIR/libinput` (falling back to `/run/user/<euid>`). It writes `libinput-replay*.quirks` there *before* any device exists (`main`, `:390-391`).
- [DOC] libinput itself parses that same directory: `src/quirks.c:1275-1281`, the same lines at 1.31.3 `:1273-1278`.
- Leak:
  - The file is removed only in a Python `finally` block (`:398-407`). A SIGKILL or crash leaves it behind.
  - The file's own header says "Unless libinput replay is running right now, remove this file."
- Match scope:
  - The quirk matches on `MatchName`, `MatchVendor` and `MatchProduct` (`:299-305`).
  - [INF] It therefore also applies to the *physical* device the recording came from at the next libinput context creation.
- Corruption path:
  - [DOC] `name` is copied unescaped into the section header (`:302-303`). A name containing a newline yields a section line without its closing `]`, and `quirks.c:1089-1090` rejects that line.
  - [DOC] Any failure inside `parse_files` makes `quirks_init_subsystem` return NULL, so `libinput.c:1922-1931` drops the *entire* quirks database, system data included ("This will negatively affect device behavior").
  - [INF] One malformed or stale runtime file can therefore disable all quirks for the compositor the next time it starts.

**CE4 — Ctrl+C does not return the device to a clean state (MEDIUM).**
- [DOC] `libinput-replay.py:292`: "Note that the device may not be in a neutral state now." This means keys and buttons can be left held.
- [DOC] `create()` enables `EV_REP` with a 500/20 delay/period (`:138-141`). [INF] Kernel soft-autorepeat then fires for a held key on the virtual node, even though replay itself drops recorded repeats (`:174`).
- `tools.rst:279` says only that Ctrl+C "removes the virtual device". It does not say any state is reverted.

**CE5 — "needs root" is not a fence on this host (HIGH, a precondition the others depend on).**
- [OBS] `getfacl /dev/uinput` shows `user:<operator>:rw-`. The source is the uaccess tag in `/usr/lib/udev/rules.d/60-steam-input.rules:5`.
- [OBS] `/dev/input/event*` are 26 nodes, all `root:input 660`, and the operator account is in group `input`.
- [OBS] `libinput-tools 1.32.0-1` was explicitly installed 2026-10-20 04:25:17 -03. `python-libevdev`, `python-pyudev` and `python-yaml` are present. When this seat started, `pacman -Q` showed `libinput 1.31.3-1` and no `libinput-tools`: the state drifted mid-round, installer unknown, as also recorded in `DocsVersion.md` / `ReviewDocsEra.md`.
- Result: `replay`, `record` and `debug-events` can now run as the session user with no `sudo` [INF]. The documentation's "must be run as root" (`tools.rst:31`) holds on stock systems but describes no protection here. Only the lane rule protects.

**CE6 — `record`/`debug-events` "read-only" still means device access, exclusive grab and data leaks (MEDIUM).**
- `--grab`:
  - [DOC] `libinput-record.man:64-66` and `libinput-debug-events.man:31-33`: `--grab` will "prevent events from being delivered to the host system". This takes input away from the session.
- Key-data leaks:
  - [DOC] `--show-keycodes` removes the obfuscation.
  - [DOC] `--with-hidraw` reports are "**not obfuscated** … could recover the key strokes" (`record.man:130-136`).
  - [INF] Even obfuscated output keeps key timing and key counts.
- `--no-events`:
  - [DOC] It still opens the node. Its YAML carries the OS, kernel, DMI modalias, device names, udev properties and the HID descriptor (`record.man` FILE FORMAT).
  - Under `SKILL.md:234-236` that is identity material, not shape.

## Impacted axes
- **coverage (C1/U6):** a U6 note that lists replay, uinput or `record --no-events` as a probe rung cannot be credited. It contradicts the round contract ("no … replay/injection") and `SCORECARD.md:618-620`.
- **safety/operability:** the fence's rule 2 names keystroke injection only. Virtual-device creation, the runtime-quirks write and `--grab` fall through it.
- **provenance:** S007's teaches cell places replay among probe material. Any superseding row must say that replay is injection.
- Classification: this is a fixable defect, not a tradeoff. No reading exists under which replay or uinput is read-only.

## Smallest safe correction (InputDraft note; L1 owns the SKILL/registry edits)
1. In the U6 `## Safe boundary`, add a class table:
   - **Injection/mutation:** `libinput replay`, any uinput/virtual-device creation (`evemu-device`/`evemu-play`, `ydotool`, Wayland virtual-keyboard/pointer clients). Cite `tools.rst:276`, uinput §7.1 and `libinput-replay.py:148,224,326-332`.
   - **Device access / input read:** `record` (every flag, including `--no-events`), `debug-events`, `debug-gui`, `measure`, `list-devices`, `list-kernel-devices`, `quirks`.
   - State that **none was executed**.
2. State that the fence is the lane rule, not privilege. Record this as shape only: "this host grants the session user `/dev/uinput` and `input`-group event-node access; `libinput-tools` 1.32.0 present since 2026-10-20". Never print usernames or device names.
3. List the side effects of `replay` as [UNK]-never-exercised:
   - the runtime-quirks write and its leak/corruption path (CE3)
   - logind power-switch reach (CE2)
   - non-neutral exit and autorepeat (CE4)
   - contamination of `hyprctl devices` counts (CE2)
4. Owned by L1, later: extend `SKILL.md` rule 2 to cover "no virtual input device (uinput/evemu/replay), no `--grab`, no `$XDG_RUNTIME_DIR/libinput` writes". Supersede S007 so that its teaches cell separates the inventory, input-read and injection classes.

Flip condition: none at this pin. Replay's purpose is to create a device and send events, so no version of it can be read-only.
