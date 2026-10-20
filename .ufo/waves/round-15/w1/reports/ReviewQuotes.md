# ReviewQuotes — round 15 w1 (C1 / U6 input-evidence ladder)

Seat: `MadoR15.ReviewQuotes` (leaf reviewer; no delegation). Date: 2026-10-20 (UTC).
Scope: quote discipline for libinput helper tools (S007 route) and Wayland core input
protocol XML. Read-only: web/static fetch, installed-file hashing, help-free reads of
`/usr/share/wayland/wayland.xml`, package metadata (`pacman -Q/-Qi/-Si/-Ql`). No input
events read, recorded, replayed or injected; no libinput binary executed; no live probe;
no test/gate/lint/build; no registry, corpus, SKILL, SCORECARD or LOG edits.
No credential/auth file and no `~/.omp/agent/agent.db*` was opened; `omp` CLI not run.

## 1. Pinned revisions (verified now)

| Source | Exact location | Revision / identity | Check result |
|---|---|---|---|
| libinput helper tools, HTML | `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (§Helper tools) | "latest" rendering, header "libinput 1.32.0 documentation"; **no commit** | Unpinned alias (moves). Opened 2026-10-20 |
| libinput helper tools, source | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` | tag `1.32.0`; sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f` (fetched to /tmp/r15q) | Strict anchor. Quoted phrases confirmed at lines 31, 45–46, 78, 135, 141–143, 220, 262 |
| libinput reporting-bugs (lead, not admitted) | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/reporting-bugs.rst` | tag `1.32.0`; sha256 `d56f53688487f61f6e0d647fb804991769904dfc742780b63fe560a04ff2df10` | Phrase confirmed at line 226 |
| Wayland core protocol XML (upstream) | `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` | tag `1.26.0`; sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` | **Byte-identical** to installed `/usr/share/wayland/wayland.xml` (same sha256); `wl_seat` version 11 at line 2004 |
| Installed Wayland | `pacman -Q wayland` | 1.26.0-1 | Matches the XML tag |
| Installed libinput | `pacman -Q libinput` | **1.31.3-1** (library package); no libinput binary in `pacman -Ql libinput` | Host ≠ doc pin 1.32.0 |
| libinput-tools | `pacman -Si libinput-tools` (sync) | 1.32.0-1 available, **not installed** | Not installed (see §6) |
| Host Wayland diagnostic | `pacman -Qi wayland-utils` | 1.3.0-1 | Matches S046 pin |

Word-count method: whitespace-delimited words in the quoted fragment, Markdown/markup removed.
Apostrophes are quoted as rendered in the HTML (curly `’`); the `.rst` bytes use ASCII `'`.
Cite the HTML text and the `.rst` line together so either can be re-derived.

## 2. Quote rows (each ≤25 words)

Status key: `primary-quote` = the quoted text is in the pinned source and supports the stated
row only; `[INF-docs]` = documented semantics, not host behaviour; `[UNK]` = not exercised.

| Row | Location and revision | Verbatim quote (words) | Supports | Does not support | Status |
|---|---|---|---|---|---|
| Q1 | libinput 1.32.0 `tools.rst:31` (§Helper tools) | "Most of the tools must be run as root to have access to the kernel’s `/dev/input/event*` device files." (18) | Kernel-node access needs privilege for *most* helper tools | "All tools" need root; any host permission state; that this lane may run them | primary-quote, [INF-docs 1.32.0] |
| Q2 | libinput 1.32.0 `tools.rst:45–46` (§list-devices note) | "This tool does not show your desktop’s configuration, just the libinput built-in defaults." (14; `not` is bold in source) | `list-devices` shows libinput defaults, not desktop-applied settings (M04 boundary) | What Hyprland `input.conf` actually applies; any compositor rung | primary-quote, [INF-docs 1.32.0] |
| Q3 | libinput 1.32.0 `tools.rst:78–79` (§list-devices note; continuation line not separately grepped, HTML text confirmed) | "This tool is intended for human-consumption and may change its output at any time." (15) | Output is not a stable parse contract | Correctness of any displayed value | primary-quote, [INF-docs 1.32.0] |
| Q4 | libinput 1.32.0 `tools.rst:135–136` (§debug-events) | "The libinput debug-events command prints events from devices and can help to identify why a device behaves different than expected." (20) | `debug-events` prints libinput-level events for diagnosis | What the compositor forwarded to any client | primary-quote, [INF-docs 1.32.0] |
| Q5 | libinput 1.32.0 `tools.rst:141–143` (§debug-events) | "To reproduce the event sequence as your desktop session sees it, ensure that all options are turned on or off as required." (22) | Options must be passed explicitly to mirror the session; tool does not infer them | That defaults in this session equal the operator's settings | primary-quote, [INF-docs 1.32.0] |
| Q6 | libinput 1.32.0 `tools.rst:220` (§record) | "The recorded events are kernel events and independent of the libinput context." (12) | `record` captures kernel-layer events independent of libinput/compositor state | Any compositor delivery, or anything about the desktop | primary-quote, [INF-docs 1.32.0]; record = input capture, **not run** |
| Q7 | libinput 1.32.0 `tools.rst:262–263` (§record) | "For data protection, libinput record obscures key codes by default, any alphanumeric key shows up as letter “a”." (18) | Default redaction: recordings are not faithful keystroke traces | That redaction is complete or that a recording is safe to store | primary-quote, [INF-docs 1.32.0] |
| Q8 | libinput 1.32.0 `reporting-bugs.rst:226` (lead, §evemu warning) | "Where available, the libinput record and libinput replay tools should be used instead of evemu" (15) | Preference order between recorders | Any capture result or host capability | candidate (not admitted), [INF-docs 1.32.0] |
| Q9 | Wayland 1.26.0 `wayland.xml:2030–2033` (`wl_seat.capabilities` event) | "This is sent on binding to the seat global or whenever a seat gains or loses the pointer, keyboard or touch capabilities." (22) | Capabilities are a per-seat advertisement, sent on bind and on change | Which physical device produced an event; libinput device list | primary-quote, [INF-docs]; byte-identical to installed XML |
| Q10 | Wayland 1.26.0 `wayland.xml` `wl_seat.capabilities` description (after line 2033; ~2034–2057) | "a client should destroy the wl_pointer objects associated with the seat where the capability was removed" (16) | Object lifecycle on capability removal is client-side release, not implicit | That the compositor stops events synchronously | primary-quote, [INF-docs] |
| Q11 | Wayland 1.26.0 `wayland.xml:2614–2620` (`wl_keyboard.enter`) | "Notification that this seat’s keyboard focus is on a certain surface." (11) | Keyboard focus is per-surface and announced by enter/leave | Which app or window Hyprland focuses; focus policy | primary-quote, [INF-docs] |
| Q12 | Wayland 1.26.0 `wayland.xml:~2620–2627` (`wl_keyboard.enter`) | "Clients should not use the list of pressed keys to emulate key-press events." (13) | Pressed-key list is not an event stream to replay | Ordering of keys (spec says unspecified) | primary-quote, [INF-docs] |
| Q13 | Wayland 1.26.0 `wayland.xml:2597` (`keymap_format` entry `xkb_v1`) | "libxkbcommon compatible, null-terminated string; to determine the xkb keycode, clients must add 8 to the key event keycode" (18) | Keycode offset (+8) is a protocol-level contract for xkb mapping | Layout or symbol result of any key | primary-quote, [INF-docs] |
| Q14 | Wayland 1.26.0 `wayland.xml:~2669–2674` (`wl_keyboard.key`) | "The key is a platform-specific key code that can be interpreted by feeding it to the keyboard mapping" (18) | `key` carries a platform code; meaning comes from the keymap event | Meaning of the code on this host without the keymap | primary-quote, [INF-docs] |
| Q15 | Wayland 1.26.0 `wayland.xml` `wl_keyboard.key_state` enum, entry `repeated` (`since="10"`), immediately before `wl_keyboard.key` at ~2669 | (attribute, not prose) `since="10"` | Version gate: a client bound below v10 must not expect `repeated` | Anything about the host's advertised version (see §3) | primary-quote (attribute), [INF-docs] |

## 3. Advertised version versus XML version (discipline finding)

- Upstream XML: `wl_seat` version 11 (`wayland.xml:2004`); `wl_pointer` 11; `wl_keyboard` 11.
- Host capture `.ufo/waves/round-13/w1/globals.json` (captured 2026-10-20T04:10:03Z, read-only
  here): `wl_seat` advertised at **version 9**.
- Therefore Q15 (`since="10"`) is **not** available on this compositor's `wl_seat` advertisement.
  Any row that cites XML-level events must name the advertised version and gate by `since`.
- The S041 "selected pairs" table in the round-13 knowledge file omits `wl_seat`; the full
  record exists in `globals.json`. Do not cite the omission as absence.

## 4. Whole-ladder mapping: what each primary quote can and cannot carry

| Rung | Admitted quote(s) | Status |
|---|---|---|
| L0 kernel `/dev/input/event*` | Q1, Q6 | primary-quote, [INF-docs]; no host read |
| L1 libinput processing and defaults | Q2, Q3, Q4, Q5, Q7 | primary-quote, [INF-docs 1.32.0]; host lib 1.31.3 |
| L2 compositor applies desktop config to devices (Hyprland) | none admitted; Q2 explicitly disclaims it | **gap / [UNK]** — needs a tagged Hyprland input-dispatch source row |
| L3 compositor → client seat/pointer/keyboard protocol | Q9–Q15 | primary-quote, [INF-docs], version-gated by advertisement |
| L4 client handling / application behaviour | none | [UNK] |
| End-to-end "kernel event → Hyprland → app" | no single quote supports it | **[INF] composed from rungs**; never an admitted row |

Rule: each rung is cited by its own quote; the composed ladder is labelled `[INF]`.
No row may say "input path verified" from L0/L1/L3 documentation alone.

## 5. Integration checklist (for L1; L1 owns the registry)

1. **S007 anchor is unpinned.** Its `anchor` cell says "§Helper tools … libinput 1.32.0 documentation"
   with no revision (the round-12 owed-anchor case). Do **not** edit the immutable anchor cell.
   Add a superseding row (`teaches` opening `supersedes S007 —`) with the tag-1.32.0 raw URL and
   sha256 `53264328…4ff5f` (Q1–Q7 lines above). Keep S007 `queued`/status rules as the registry specifies.
2. **Wayland core XML needs its own row.** S043 cites "installed XML:117–177" (no URL, no hash). A
   new row (ids reserved S051/S052 per spec — L1 assigns) should cite
   `…/wayland/-/raw/1.26.0/protocol/wayland.xml`, sha256 `cc860987…57f5e07`, identical to the installed file.
   Q9–Q15 come from that row.
3. **Collision screen before merge.** The new raw URLs are distinct from S007's `tools.html` and from
   S043's wayland.xml anchor; run the lane's collision screen (QUALITY 17) before admitting. Not run here.
4. **Version pin.** Label every libinput-tool statement `[INF-docs 1.32.0]`. Host has libinput
   1.31.3-1 (library only); host-side tool behaviour is `[UNK]` until a tool revision matches the pin.
5. **Advertised version.** Record `wl_seat` advertised v9 vs XML v11 wherever Q9–Q15 are used. Gate by `since`.
6. **Keep rungs separate.** Do not merge L0/L1/L3 quotes into one row; do not add an L2 row from Q2 (it disclaims L2).
7. **Quote form.** Quote the HTML rendering (curly apostrophes), cite the `.rst` line with the sha256 above.
   Keep "not" bold-only emphasis out of quotes unless shown.
8. **Privacy/boundary.** Q6–Q7 describe input capture. The lane quotes them and does not run `libinput record`
   or `debug-events`. Any future run requires the authorised lane and root.
9. **Lead, not admitted.** Q8 (reporting-bugs) stays a candidate until L1 decides whether the registry needs it.
10. **Owned files.** Nothing outside this report was written; registry, corpus and SCORECARD were not touched.

## 6. Tooling record (directive)

- Installed: **none**. Read-only fetch used `curl` (system package, pre-existing) to `/tmp/r15q/` for three static files.
- Found but not installed: `libinput-tools 1.32.0-1` (extra, sync). It would give a `libinput` binary matching the
  doc pin, but `libinput` (installed 1.31.3-1; sync 1.32.0-1) would also need to move. That is a library-level upgrade
  on the host, outside this seat's bounded read-only scope. Recommended for the main agent to decide under the
  update-safety gate. Not executed; no partial upgrade attempted.
- `/tmp/r15q/` holds copies only; they are not evidence artifacts and may be removed.

## 7. Verification gaps

- The HTML `latest` page was fetched on 2026-10-20 and is not pinned; the `.rst` at tag 1.32.0 is the pinned authority used for line citations.
- Q3 continuation line and Q10/Q14 line ranges were confirmed by the rendered text and the installed XML, not by a separate grep of each line.
- No libinput binary exists on the host; no `libinput --help` or man page check was performed.
- Upstream reporting-bugs (Q8) is not admitted; it is a candidate only.
- Hyprland's input dispatch (L2) and any client behaviour (L4) have no source row here; they remain `[UNK]`.
- No input-event collection, no replay, no live compositor probe were performed; the advertised-version point rests on the round-13 retained capture, not a fresh read.
- Word counts are whitespace counts; a stricter tokenizer could differ by one or two for hyphenated words.
