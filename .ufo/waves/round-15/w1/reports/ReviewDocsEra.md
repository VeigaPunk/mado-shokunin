# ReviewDocsEra — U6 integration risk: installed version vs docs era

Seat: MadoR15.ReviewDocsEra (reviewer, leaf). Axis judged: coverage (C1). Read-only; no tests, gates, builds, live probes, input reads, or compositor actions. Installs by this seat: none. Scratch fetches (curl of static docs into /tmp) were removed.

## Verdict

**Accept U6 only with the conditions in §3.** The libinput docs are version-moving, and the host's installed libinput changed during this round. A U6 note that cites `doc/latest` as the host's installed behaviour is rejected.

## 1. Findings, most severe first

**F1 — HIGH: mid-round partial upgrade of the input stack by another seat.**
- `/var/log/pacman.log`: `[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`, then `upgraded libinput (1.31.3-1 -> 1.32.0-1)` and `installed libinput-tools (1.32.0-1)` at 04:25:17.
- `pacman -Qi libinput-tools`: Install Date `Tue 20 Oct 2026 04:25:17 AM -03`.
- At my first read (before 04:25) `pacman -Q libinput` was `1.31.3-1` and `pacman -Qi libinput-tools` said "not found". The change is therefore inside this round.
- This is a targeted `-S` of two packages, not `-Syu`. The operator rule forbids partial upgrades; the log shows no update-safety gate record. Hyprland 0.56.2-2 and aquamarine both list `libinput` as a dependency.
- I did not identify the acting seat from the log. The roster's LibinputTools scout is the likeliest candidate `[INFERENCE]`. The integrator must confirm which seat ran it and whether it recorded tool/version/channel/reason per the operator directive.
- Action for the integrator: record the upgrade in the round report. Do not claim "installed 1.31.3" for any U6 entry after 04:25:17.

**F2 — HIGH: the running compositor still maps the pre-upgrade library.**
- `/proc/1706/maps` (Hyprland `--watchdog-fd 4`) contains `/usr/lib/libinput.so.10.13.0 (deleted)`.
- `pacman -Qo /usr/lib/libinput.so.10.13.0` now reports the on-disk file as owned by `libinput 1.32.0-1`.
- So: package state = 1.32.0; the process that receives input = 1.31.3 code, until Hyprland restarts. The restart is operator-owned; this seat did not touch it.
- Consequence: "installed version" and "runtime version" are now different facts. Any U6 claim about host input behaviour must name which one it measured.

**F3 — HIGH: `doc/latest` is a moving docs era, not an installed version.**
- Banner of `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`: "Helper tools — libinput 1.32.0 documentation". The index says "generated from git commit 4cf1775".
- Versioned doc paths `.../doc/1.31/tools.html` and `.../doc/1.31.3/tools.html` return HTTP 404. No versioned doc URL exists to anchor 1.31.3. Version-pinned anchors must use the gitlab raw source at tag.
- Pinned sources read this seat (curl, sha256 of bytes):
  - `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.31.3/doc/user/tools.rst`: `20bcf797b26fc262071bd46dc7f5a649d173aaac37171b393b52357fafd1e69e`
  - `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`: `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`
  - Both tags resolve (HTTP 200 on `/-/tags/<v>`).
- `diff` of the two sources, complete. Four hunks differ; all others are byte-identical:
  1. `libinput replay` prompt line: 1.31.3 `SynPS/2 Synaptics TouchPad: /dev/input/event19`; 1.32.0 `/dev/input/event19: SynPS/2 Synaptics TouchPad`.
  2. `record` autorestart: 1.31.3 says a file is created immediately with a timestamped name; 1.32.0 says the tool waits for device activity before creating a file.
  3. Multi-device record: 1.31.3 requires `--multiple --output-file=...`; 1.32.0 drops `--multiple` and requires only `--output-file`.
  4. New in 1.32.0: `libinput record --no-events` (device description only, no event wait).
- Unchanged across both: `list-devices` (including the "does **not** show your desktop's configuration, just the libinput built-in defaults" note), `list-kernel-devices`, `debug-events`, `debug-gui`, `quirks`. The round-12 lesson M04 claim (`libinput list-devices` ≠ desktop config) survives the version split.
- Consequence: any record/replay command form in a U6 note must be cited to the source tag matching the measured installed library. Copying 1.32.0 forms onto a 1.31.3 state is a rejection condition.

**F4 — MEDIUM: S007 cannot support a U6 claim as written.**
- `corpus/SOURCES.md` S007: "libinput helper tools — https://wayland.freedesktop.org/libinput/doc/latest/tools.html", teaches "(libinput 1.32.0)", status `queued`, recheck `180d`.
- Its anchor is an unpinned moving URL. Under the lane's own convention (S042 superseded S006 for exactly this reason; S049 corrected S046), a superseding row with a tag or commit anchor is needed before mining. The row cannot change in place for its teaches cell.
- Owed: a superseding row citing `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` (sha `53264328…`) plus, if 1.31.3 is claimed as the historical state, a separate row for `…/1.31.3/…` (sha `20bcf797…`). Registry edits belong to L1 only.

**F5 — MEDIUM: S052 (Wayland core input XML) needs the installed revision.**
- Installed `wayland 1.26.0-1`; `sha256sum /usr/share/wayland/wayland.xml` = `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`. This matches the S043 record in `corpus/SOURCES.md` and the round-13 verifier note.
- `wl_keyboard` and `wl_pointer` are defined in this core XML. The wayland-protocols 1.49 package (`/usr/share/wayland-protocols/`) is a different revision and owns the text-input/IME protocols; it must not be cited as the core wl_keyboard source.
- Acceptance: S052 cites the installed XML sha `cc860987…` with package `wayland 1.26.0-1`, or the upstream 1.26.0 tag with its own sha after a fetch. Citing "latest" or the wayland-protocols package for core input semantics is rejected.

**F6 — LOW / OUT OF SCOPE HERE: Hyprland docs era.**
- `hyprland 0.56.2-2` is installed; the lane pins `efb50993…` (tag v0.56.2) in S018/S041. Hyprland wiki "latest" pages (for `hyprctl devices`, `getoption` input keys) are the same moving-docs risk. This seat did not verify them. Defer to the HyprInputDocs report.

## 2. Acceptance and rejection conditions for the U6 entry

Accept only if all hold:
- A1. Every libinput command form is cited to a version-pinned source (gitlab raw at tag, with sha256). Versioned doc URLs that 404 are not evidence. `doc/latest` may be cited only as a dated docs-era note labelled `[INF-docs]`.
- A2. The note states which libinput was measured: package `1.32.0-1` (pacman, since 04:25:17 -03) and/or the runtime library loaded by the compositor (`/proc/<pid>/maps`). If a runtime claim is made, it names the `(deleted)` entry or its absence.
- A3. The 1.31.3 vs 1.32.0 difference is stated where a command form is shown. The four differing hunks (F3) are recorded or the note limits itself to the shared sections.
- A4. The F1 upgrade is recorded: tool, versions, channel (`pacman -S --needed --noconfirm libinput libinput-tools`), time, and that it was not a full upgrade.
- A5. No statement that libinput tools show the desktop's configuration; the built-in-defaults note is quoted or paraphrased.
- A6. S007 has a superseding pinned row before any U6 claim cites it. S052 cites the installed XML sha.
- A7. Input delivery, IME, pointer rendering, kernel/device diagnosis, and any live probe stay `[UNK]`. U7 Waybar stays out of scope.

Reject if any hold:
- R1. A U6 claim treats `doc/latest` (1.32.0) as this host's behaviour without a version and hash anchor.
- R2. A claim says the host's input library is 1.31.3 after 04:25:17 without a runtime qualifier, or says 1.32.0 is the running library while `/proc/1706/maps` shows the deleted 1.31.3 file.
- R3. Record/replay/`--multiple`/`--no-events` forms are asserted for the installed state without a version-matched source.
- R4. Any step runs `libinput debug-events`, `record`, `replay`, or `list-devices` as evidence. Those are live probes or input reads, forbidden this round.
- R5. Any claim that the libinput tool is "not installed" (true at 04:23 but false now; `/usr/bin/libinput` owned by `libinput-tools 1.32.0-1`).
- R6. The F1 upgrade is absent from the round record.

## 3. Exact evidence pointers

- Pacman log: `/var/log/pacman.log` lines for 2026-10-20T04:25:16–17 -0300.
- Package state: `pacman -Q libinput libinput-tools` → `libinput 1.32.0-1`, `libinput-tools 1.32.0-1`. `pacman -Qo /usr/bin/libinput` → owned by `libinput-tools 1.32.0-1`.
- Running compositor: `/proc/1706/maps` → `/usr/lib/libinput.so.10.13.0 (deleted)`. `pgrep -x Hyprland` → `1706 Hyprland --watchdog-fd 4`.
- Hyprland: `pacman -Qi hyprland` → `0.56.2-2`; Depends On includes `libinput`.
- Docs: `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (banner 1.32.0); `…/doc/1.31/tools.html` and `…/doc/1.31.3/tools.html` → HTTP 404.
- Pinned sources: `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.31.3/doc/user/tools.rst` (sha `20bcf797b26fc262071bd46dc7f5a649d173aaac37171b393b52357fafd1e69e`); `…/raw/1.32.0/doc/user/tools.rst` (sha `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`). Diff: four hunks in §1 F3.
- Wayland core: `/usr/share/wayland/wayland.xml` sha `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, package `wayland 1.26.0-1`; matches `corpus/SOURCES.md` S043.
- Lane rows: `corpus/SOURCES.md` S007 (queued, `doc/latest`), S042/S049 (revision-anchored supersession precedent), S052 owed; `corpus/lessons/round-12.md` M04 (list-devices built-in defaults).

## 4. Residual risk and verification gaps

- Not verified: whether the acting seat for F1 ran the update-safety gate. The log shows no gate record.
- Not verified: the exact runtime library behaviour for `libinput record` / `replay` after the 1.32.0 change. No live probe permitted.
- Not verified: `hyprctl devices` / `getoption` docs era (F6, HyprInputDocs seat).
- Not verified: whether 1.32.0 and 1.31.3 `libinput-tools` `record --multiple` maps to the library ABI change. The soname `libinput.so.10` is unchanged (`/usr/lib/libinput.so.10.13.0`), but the docs diff is the only evidence I have of behaviour change.
- Gap for the integrator: the S007 and S052 owed rows are registry edits (L1 only). This seat proposes, does not edit.
