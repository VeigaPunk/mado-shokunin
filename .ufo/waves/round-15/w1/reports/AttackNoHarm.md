# AttackNoHarm — round 15 W1 critic

Proposal under attack: add one bounded U6 note (libinput/Wayland input-debugging route), keep the gate unchanged, use only read-only static sources, and score coverage 5/7 → 6/7.
Axes: coverage (scored); harm watch covers navigation, registry census, gate identity, host state and privacy.
Baseline HEAD `ea0446f` (measured content `32118fc`). Every check below was a static read. I installed nothing, ran no gate or tests, and read no input events.

## Verdict

The note itself can be harmless. **The claim that the round is harm-free is already false in one place, and is fragile in four more.** Items 1–2 must be recorded or fixed before admission. The judge should reject the round if items 3–5 are left as they stand.

## 1. A peer changed host state in the middle of the round — DEFECT, must be recorded

- **Counterexample.** `/var/log/pacman.log`: `[2026-10-20T04:25:16-0300] Running 'pacman -S --needed --noconfirm libinput libinput-tools'` → `upgraded libinput (1.31.3-1 -> 1.32.0-1)`, plus installs of `libinput-tools 1.32.0-1`, `python-libevdev`, `python-pyudev` and `python-yaml`. The same run then fired `35-systemd-udev-reload.hook`.
- **The udev hook is not a no-op.** `/usr/share/libalpm/scripts/systemd-hook` udev-reload runs `udevadm control --reload` and then `udevadm trigger -c change; udevadm settle`. The opt-out file `/etc/systemd/do-not-udevadm-trigger-on-update` does not exist. So every device, input devices included, received a change uevent. The install also changed the libinput udev rules and quirks shipped under `/usr/lib/udev/rules.d/*libinput*` and `/usr/share/libinput/*.quirks`.
- **Consumers.** `readelf -d`: `/usr/bin/Hyprland` and `libaquamarine.so*` both have `NEEDED libinput.so.10`. The soname is unchanged, so ABI risk is low. The new library and quirks will load at the next compositor start.
- **This is a partial upgrade.** The sync DB was last refreshed by `pacman -Sy --noconfirm` (2026-10-18 14:11), and `pacman -Qu` lists **413** pending updates, including `hyprland 0.56.2-2→-4`, `aquamarine 0.15.0-2→0.15.1-1`, `systemd 261.2→262`, `mesa` and `linux`. Pulling one library from that newer DB is a partial upgrade in Arch terms. RULES.md forbids partial upgrades.
- **Evidence went stale inside the wave.** `reports/DocsVersion.md:4,6` still says the host has "`1.31.3-1`" and "libinput-tools … not found". Both stopped being true at 04:25:17. Round-12 also recorded libinput as not installed (`SCORECARD.md:321`).
- **Impacted.** The "no host/config mutation" harm watch, the "no hardware/kernel action" bound, provenance, and the tooling-record duty.
- **Smallest safe correction.**
  - Do **not** revert; a downgrade is a second mutation.
  - Record the install in the lesson, the SCORECARD harm watch and the SKILL tool note, following the precedent at `SKILL.md:407-408` (round 13's wayland-utils). The record must include:
    - exact old→new versions, the four added packages and the time;
    - channel `pacman -S`, plus the partial-upgrade caveat and the 413 pending updates;
    - the udev reload/trigger side effect.
  - Change the harm-watch sentence from "no host mutation" to "an authorised tool install changed the input library/udev rules; no config or event read".
  - Any version cited in the note is **1.32.0 as of 04:25:17**, not 1.31.3.
  - Flag that a full `-Syu` still has to go through the tsukuroi update-safety gate.

## 2. The safe boundary cannot rest on "needs root" — DEFECT in the S007 / draft framing

- **Counterexample.** `id -nG` → `vgpnk docker input wheel`, and `getent group input` → `input:x:992:vgpnk`. On this host the login account is in `input`. The "Most of the tools must be run as root" quote (`lessons/round-12.md:61`, S007) is therefore not a barrier. InputDraft's ban only covers "sudo input tools". With `/usr/bin/libinput` now installed (item 1), an unprivileged `libinput debug-events` or `libinput record` may work with no sudo at all. Whether it actually opens the device nodes is `[INF]`; I did not probe it.
- **Static man-page evidence (libinput-tools 1.32.0).**
  - `libinput-record(1)`: "By default, common keys are obfuscated"; `--show-keycodes` turns obfuscation off. The HID-report option says "DO NOT TYPE SENSITIVE DATA", and "HID reports are not obfuscated … Do not type passwords while recording HID reports."
  - `libinput-debug-events(1)`: key events are only "partially obfuscated".
  - `libinput-replay(1)` must "create a device and/or replay events". That is injection.
  - `libinput-list-devices(1)` opens `/dev/input/eventX`. That is a device read, not a docs read.
- **Impacted.** Privacy and no-harm. The note's `## Safe boundary` facet would be wrong.
- **Smallest safe correction.**
  - The `## Safe boundary` section must state the boundary as **policy (never run)**, not as privilege. Bar `list-devices`, `debug-events`, `record`, `replay`, `measure`, `analyze` and `--show-keycodes` / hidraw recording, whether run as root or as a non-root `input` member.
  - Put no copy-paste invocation lines in any "recheck" section. The safe recheck is limited to `pacman -Q libinput libinput-tools wayland`, `sha256sum` of the cited XML/man/doc bytes, and `man`/`--help` text.
  - Optionally record the `input` membership as `[OBS] id -nG`, without enumerating devices.

## 3. Duplicate-source collision if S051 re-registers tools.html — gate-able DEFECT

- **Counterexample.** S007 (`SOURCES.md:19`) is **queued**, active, and already uses `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (§Helper tools + record/replay). A new S051 with the same canonical URL fails the round-14 merge screen. `MistakeFix.py:11-13,290-313` treats any two queued/mined rows sharing a URL as a collision unless the later row's `teaches` opens with `supersedes S007 —`. That collision exits 1. Round 14's harm watch recorded `collisions=0` (`round-14/evidence/source-merge.txt`).
- The fleet census `scripts/sources-census.sh:645-649` adds W04 for a different scope and E04 for the same scope without `supersedes`.
- **Same risk for S052.** S043 is mined and points at `/usr/share/wayland/wayland.xml` plus `apa.html`. Reusing either URL for S052 needs `supersedes S043 —`, or a different pinned URL.
- **Registry rule.** Only `status`, `recheck` and `used-by` may change in place, and each change must be logged (`SOURCES.md:5-7`). The owed-anchor rule at `SOURCES.md:115` asks the round that mines a queued page to append a superseding row with a pinned revision.
- **Smallest safe correction.**
  - S051's `teaches` opens `supersedes S007 — …` and pins an immutable revision: the libinput tag `1.32.0` doc source, or the installed `libinput-tools 1.32.0-1` man pages with sha256. The mutable `latest` page is not acceptable.
  - Leave S007's cells unchanged. If its status flips, log it, and do not add the U6 note to S007's `used-by` unless S007 is also cited on the note's source line. The round-14 inverse rule (`measure.py:184-186`) fails otherwise.
  - Re-run the merge screen and census at the measured revision: `collisions=0`, no new E04, and any new W04 named.

## 4. Version and semantics mismatch in the Wayland core XML — DEFECT if left unpinned

- **Counterexample A: upstream main ≠ host.** The upstream `main` HEAD `93c04ad` (2026-10-08) is "protocol: define that wl_pointer.leave means buttons are no longer pressed". Its sha256 is `4831fd1c…`, recorded at `round-13/w1/reports/GlobalDocs.md:73-76`. The installed `wayland 1.26.0-1` XML has sha256 `cc860987…`, re-checked today. Its `wl_pointer.leave` text (`wayland.xml:2212-2221`) has no such clause. Citing main for leave/button semantics would put post-1.26.0 semantics onto the host.
- **Counterexample B: XML version > advertised version.** In the installed XML, `wl_seat`, `wl_pointer` and `wl_keyboard` are all `version="11"` (`:2004,:2138,:2573`). It includes `wl_pointer.warp since="11"` and `wl_keyboard` key state `repeated since="10"`. The host advertised `wl_seat` **v9** (`round-13/w1/globals.json:35-36`). Child objects inherit the seat version, so features from v10 and v11 are not reachable through that advertisement.
- **Smallest safe correction.**
  - Pin S052 to `/-/raw/1.26.0/protocol/wayland.xml` and require its sha256 to equal the installed `cc860987…`.
  - Tag every cited event or request with its `since`. Anything with `since` greater than 9 is marked `[UNK]`, "not available at historical advertised wl_seat v9".
  - Keep the r13 advertisement dated: it is a historical capture, not a fresh read.

## 5. Duplicate authority, stale present tense, and claims about live readings — fixable

- **Stale index text.** `corpus/README.md:94-95` still lists "the input debugging ladder" as open. Once U6 is admitted, that present-tense claim is stale. Add a round-15 bullet in the style of `:99-102`. The navigation counter (`measure.py:202-212`) also needs exactly one README row for the new note; 28/28 should become 29/29 with no missing, extra or duplicate entries.
- **Existing input claims.** Several notes already carry input claims: `input:kb_layout` br (`SKILL.md:54,69`), "8 keyboard nodes" from `hyprctl -j devices` (`hyprctl-verification-layer.md:159`), and lesson M04 (`lessons/round-12.md:37`: `list-devices` shows libinput defaults, not desktop configuration). The U6 note must cite these, not re-measure or restate them as new observations. Its ladder must keep the compositor-policy layer (Hyprland `input:*`) separate from libinput defaults.
- **No live reads this round.** Fresh `hyprctl getoption/devices` output is outside this round's permitted classes (docs/package/help/static only). Anything from hyprctl must be a dated historical citation. Device names from `devices` are host-identifying, so do not paste the list.
- **SKILL.md line anchors.** Inserting the U6 routing text above existing sections shifts present-tense `SKILL.md:NNN` anchors. Round 14 already turned the round-13 spot-check's `SKILL.md:411-433` gate-registry pointer into the output/colour text. Append the U6 routing block after `SKILL.md:446`, the end of the round-14 section, and cite anchors revision-bound (`git show <rev>:SKILL.md`).

## 6. Measurement, gate and receipt drift — constraints, not current defects

- **Gate unchanged is structurally sound.** `tools/mado-verify.sh` never parses corpus notes, SOURCES or README (`:3244-3247`, "the gate never *parses* the note"; grep shows no corpus reads). Constraint: the whole-gate sha256 must still equal `fba82a66…c5207` at the measured revision. If the gate bytes move, the PIN/recut duties of `gate-standing-use.md` §5 apply and "gate unchanged" may not be claimed.
- **Probe drift.** The new `round-15/measure.py` replaces round 14's probe. Constraint: run it on **both** the baseline and the delivered revision. The baseline must reproduce 5/7, navigation 28/28 and registry 50 (46/1/3 by tier; 38 mined / 8 queued / 4 rejected), or the delta mixes in a change of instrument.
- **Heading-only facets can be gamed.** Three headings plus an `[UNK]` would satisfy the structural check. The admission still needs a semantic hand check that the ladder actually distinguishes the hardware/libinput, compositor-policy, Wayland-delivery and toolkit/app layers. Score only U6 at 8.5714 (6/7). That is below the 9.0 saturation line, so do not hint at saturation.
- **R14-V1 receipts.** `receipt-correction.json` must leave `round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt` byte-identical; `git diff 32118fc -- .ufo/waves/round-14/evidence/` must be empty. It must also say it is a mapping, not a final full-gate receipt (`round-14-verifier-spotcheck.md:169`). It does not count toward the score.

## Acceptance conditions (smallest set)

1. The tool install from item 1 is recorded: versions, packages, time, channel, partial-upgrade caveat, and the udev trigger side effect. The no-harm wording is corrected and stale DocsVersion facts are superseded.
2. `## Safe boundary` is policy-based and covers non-root `input` group access. There are no runnable event, record, replay or device-listing commands.
3. S051 opens with `supersedes S007 —` and has a pinned revision. S052 is pinned at `1.26.0` with a sha matching the installed copy, and does not collide with S043. The merge screen shows `collisions=0` and no new E04.
4. Every cited protocol element has `since` ≤ 9, or is marked `[UNK]`.
5. Navigation is 29/29 and README:94-95 is updated. The gate sha is unchanged. The new probe reproduces the baseline at 5/7. The R14 evidence bytes are unchanged.

## Tooling record

None installed or updated by this seat. Item 1's install was made by another seat; that seat must record it under the operator directive.
