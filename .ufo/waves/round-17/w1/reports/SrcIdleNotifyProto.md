# SrcIdleNotifyProto — ext-idle-notify-v1 primary text + hypridle use

Seat: `MadoR17.SrcIdleNotifyProto` (scout, leaf, no dispatch).
Item: fetch tag-pinned raw `ext-idle-notify-v1.xml` (wayland-protocols, staging);
record SHA-256 and ≤25-word quotes on timeout / `idled` / `resumed` / inhibitor
semantics; and establish whether hypridle uses ext-idle-notify (grep its tagged
source). Report only — no round claim is made here.
Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Read first (binding): `corpus/lessons/round-16-verifier-spotcheck.md` (R16-V1
labeling defect, M5 `pacman -Q` breach, tag-source≠host-binary rule).
Host constraints observed: no pacman/yay/paru/sudo/systemctl/hyprctl and no live
probe of any kind; only `curl`, `sha256sum`, `cmp`, `tar`, `sed`, `nl`, `grep`,
`wc`, `file`, `stat`, `python3` (JSON parsing of GitLab tags API). No tool was
installed or upgraded; no host file outside `/tmp` was read or written.

## 1. Protocol text — pinned bytes

| Field | Value |
|---|---|
| Upstream | wayland-protocols (freedesktop GitLab) |
| Path | `staging/ext-idle-notify/ext-idle-notify-v1.xml` (still staging at 1.49) |
| Tag-pinned URL | `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/ext-idle-notify/ext-idle-notify-v1.xml` |
| Access | 2026-10-20, HTTP 200 |
| Size / lines | 5,881 bytes / 131 lines |
| SHA-256 | `e56a9c22684e6b46655f7221b798328e304c1efc8f63f01241a1cf8c070f4c30` |
| Cross-check (independent host) | `https://raw.githubusercontent.com/wayland-mirror/wayland-protocols/1.45/staging/ext-idle-notify/ext-idle-notify-v1.xml` → same SHA-256; `cmp` identical |
| Stability window | identical bytes at tags 1.40, 1.45, 1.49 (`cmp` + one hash); `get_input_idle_notification` absent and `version="1"` at every sampled tag 1.27–1.39 |
| Tag dates (GitLab API) | 1.39 = 2024-12-20, 1.40 = 2025-01-30, 1.49 = 2026-06-07 |

Observed version history (direct fetch per tag, not inference): interface
`ext_idle_notifier_v1` is `version="1"` through 1.39 and `version="2"` from 1.40
onward; `get_input_idle_notification since="2"` first appears at 1.40 and the file
is byte-identical in 1.40/1.45/1.49.

### 1.1 Timeout semantics

Quotes are verbatim from the pinned 1.49 bytes; line anchors are from `nl -ba` on
that file; every quote ≤25 words.

- L46–48: "The client will be notified if the seat is inactive for at least the provided timeout." (16 words)
- L50–51: "A zero timeout is valid and means the client wants to be notified as soon as possible when the seat is inactive." (22 words)
- L54: `timeout` argument summary is "minimum idle timeout in msec" (5 words) — a `uint` in milliseconds, not seconds.
- L86–87: the object "becomes idle when no user activity has happened for at least the timeout duration" (14 words), and per L87 this counts "starting from the creation of the notification object" (8 words).
- L87–89: "User activity may include input events or a presence sensor, but is compositor-specific." (13 words)

Consequences that are text-explicit: the timeout is a floor, not an exact schedule;
the object starts un-idle at creation; a zero timeout is legal; and the only
mechanism offered is notification objects — `ext_idle_notifier_v1` has no
synchronous "get idle time" request (requests are `destroy`,
`get_idle_notification`, `get_input_idle_notification`, L35–76).

### 1.2 `idled` / `resumed` events

- L101–103: "When the notification object becomes idle, an idled event is sent." (11 words); "a resumed event is sent and the timeout is restarted." (10 words)
- L112–114: `idled` — "This event is sent when the notification object becomes idle." (10 words)
- L116–117: "It's a compositor protocol error to send this event twice without a resumed event in-between." (15 words)
- L121–123: `resumed` — "This event is sent when the notification object stops being idle." (11 words)
- L125–127: "It's a compositor protocol error to send this event prior to any idled event." (14 words)

So `idled` and `resumed` must strictly alternate starting with `idled`; any user
activity after `idled` restarts the full timeout.

### 1.3 Inhibitor interaction (the part that matters for idle/lock notes)

Two constructor requests with deliberately different inhibitor behaviour:

- `get_idle_notification` (L42, no `since`, i.e. v1): L93–96 — with an active
  inhibitor (e.g. another client's `zwp_idle_inhibitor_v1` on a visible surface),
  "the compositor must not make the notification object idle" (9 words).
- `get_input_idle_notification` (L60, `since="2"`): L63–64 — "Because this object is meant to track user input alone, it ignores idle inhibitors." (14 words); L96–99 adds that then "only input from the user, e.g. from a keyboard or mouse, counts as activity" (14 words).

Both requests take the same `(new_id, uint timeout msec, wl_seat)` triple
(L53–55, L73–75), so the inhibitor policy is the only semantic difference at
creation time.

## 2. Does hypridle use ext-idle-notify? — Yes (tagged source)

Tag selection: `v0.1.8` is the newest tag that exists. Probed by fetching archive
bodies and reading `VERSION`: `v0.1.8` → gzip, `VERSION=0.1.8`; `v0.1.9`,
`v0.2.0`, `v0.2.1` → 14-byte `404: Not Found` body (tags absent). Note: `HEAD` on
GitHub archive URLs returns 302 even for absent tags, so body size/content was
used, not status.

| Artifact | SHA-256 | Size |
|---|---|---|
| `hypridle` v0.1.8 tarball (`https://github.com/hyprwm/hypridle/archive/refs/tags/v0.1.8.tar.gz`) | `08703613cc33cc796c2179bcaa6076e8618113f67b938daaf7535f90c7d39595` | 19,972 B |
| raw `v0.1.8/src/core/Hypridle.cpp` | `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` | = tarball member (`cmp` identical) |
| raw `v0.1.8/CMakeLists.txt` | `84c0fd3ce2b2a19c8f22471d2931fd394b7c9dc889b4b34d37a7f11e92919aeb` | = tarball member |
| raw `v0.1.8/README.md` | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6` | = tarball member |

Anchors (v0.1.8 line numbers):

- `CMakeLists.txt:94` — `protocolnew("staging/ext-idle-notify" "ext-idle-notify-v1" false)`: the
  generated protocol bindings are built into the binary.
- `README.md:5` — "based on the `ext-idle-notify-v1` wayland protocol" (6 words).
- `src/core/Hypridle.cpp:30–32` — on registry globals it matches
  `ext_idle_notifier_v1_interface.name` and binds
  `wl_registry_bind(..., &ext_idle_notifier_v1_interface, version)` using the
  compositor-advertised `version` verbatim (no `min()` clamp).
- `src/core/Hypridle.cpp:53–55` — if no notifier was bound: "Couldn't bind to
  ext-idle-notifier-v1, does your compositor support it?" (9 words) then `exit(1)`;
  the protocol is a hard requirement, not an optional path.
- `src/core/Hypridle.cpp:58, 74–79` — per rule it calls
  `sendGetInputIdleNotification(r.timeout * 1000, seat)` when
  `general:ignore_wayland_inhibit` or the listener's `ignore_inhibit` is set, else
  `sendGetIdleNotification(r.timeout * 1000, seat)`. Config timeout is in seconds
  and converted to msec, matching the protocol's `uint` msec argument
  (`README.md:25` comment "in seconds").
- `src/core/Hypridle.cpp:83–84` — registers `setIdled`/`setResumed` handler pairs
  per listener (protocol events drive `onTimeout`/`onResume`).
- `src/core/Hypridle.cpp:363–393` — when the inhibitor count drops to 0 while
  already idled, every notification is destroyed and recreated with the same
  request-selection logic; the comment at L334–342 explains the reason (orphaned
  condition retries after notification recreation). This is the one place the
  inhibitor semantics interact with a compositor-side inhibit latch.
- `src/core/Hypridle.cpp:89–92` — separately binds `hyprland-lock-notify-v1`
  (`CMakeLists.txt:95`) for lock/unlock events; lock state is **not** obtained from
  ext-idle-notify.
- `src/config/ConfigManager.cpp:74` — `general:ignore_wayland_inhibit` defaults to `0`.

Same use is already present in v0.1.7 (`src/core/Hypridle.cpp:74,77` and
`312,315`; tarball SHA-256 `c4ef2e2894fc2082cfdabe7db086b1f246e3f0de571f7f2c6b26d7c0d9a5f8f3`),
so the ext-idle-notify dependency is not new to 0.1.8.

## 3. Supplementary: compositor side (tag-pinned, NOT host)

Hyprland `v0.51.1` source tarball
(`https://codeload.github.com/hyprwm/Hyprland/tar.gz/refs/tags/v0.51.1`) SHA-256
`ebcdde9b3cec53dc1841cb221f0d3e26c3086f7c59416bf85243ec700a4a7f68`.

- `src/managers/ProtocolManager.cpp:166` — `makeUnique<CIdleNotifyProtocol>(&ext_idle_notifier_v1_interface, 2, "IdleNotify")`:
  the global is registered at protocol **version 2**.
- `src/protocols/IdleNotify.cpp:71–74` — both `setGetIdleNotification`
  (`obeyInhibitors = true`) and `setGetInputIdleNotification`
  (`obeyInhibitors = false`) are wired, so the v2 request is implemented.
- `src/protocols/IdleNotify.cpp:39–42, 103–108` — an obeyed notification's timer is
  stopped while `isInhibited`, and on inhibit release `onActivity()` restarts it;
  `:50–56` sends `resumed` only when the object had actually idled, preserving the
  protocol's no-resumed-before-idled rule.
- Raw per-file hashes match tarball members: `ProtocolManager.cpp`
  `e295d20253ff158e83557a7cdab2cd5b5e6ae29243b066a238c4c3fdbb97ab33`,
  `IdleNotify.cpp` (v0.51.1) `62d042f07f72cebd466a40f9554990fd649cae6ebec8f7154f4489293986a1b2`.

[INFERENCE] Because hypridle binds the notifier at whatever version the
compositor advertises and never checks `wl_proxy_get_version()` before
`get_input_idle_notification`, a v1-only compositor combined with
`ignore_wayland_inhibit=1` (or a listener's `ignore_inhibit`) would issue a
`since="2"` request against a v1 object — a server-side protocol error. Under
Hyprland ≥ the pinned 0.51.1 this branch is version-legal. Not tested; not
executed.

## 4. Confidence and limits

| Statement | Confidence | Basis |
|---|---|---|
| Pinned protocol bytes and SHA-256 | high | two independent hosts, `cmp` identical |
| Timeout / event / inhibitor quotes | high | verbatim lines of the hashed bytes |
| interface is v2 from wayland-protocols 1.40 | high | per-tag direct fetch (1.39 absent, 1.40 present) |
| hypridle uses ext-idle-notify and the v2 request | high | build rule + bind + call sites in hashed tag sources |
| hypridle sends v2 request under a v1-only compositor | medium | code read; [INFERENCE], no execution |
| Hyprland advertises v2 | high for tag v0.51.1 source; **not** a host claim | hashed tag source only |

Not proven / remaining unknowns:

- Host hypridle and Hyprland versions and the host-advertised protocol version are
  `[UNK]` — package queries and live probes are paused for this round; a tag's
  source never proves the installed binary (round-16 lesson rule).
- Whether the host hypridle config actually declares listeners, and their timeouts,
  was not read (out of this item; other seats own host config).
- hyprlock's own protocol surface is out of this item (separate seats).
- Behaviour of the DBus `logind` Inhibit path beyond config defaults was not traced
  (`README.md:6–7`, `Hypridle.cpp:97–98` show a system-bus connection exists).

## 5. Facts usable by the P6 (idle/lock) documentary route note

Usable as documentary statements, all traceable to the pinned hashes above:

1. Idle detection is a per-`wl_seat` inactivity timer; clients get `idled` after at
   least the requested msec timeout (counted from object creation) and `resumed`
   when activity resumes, which also restarts the timeout.
2. `idled`/`resumed` strictly alternate; no synchronous idle-time query exists.
3. Two constructor requests differ only in inhibitor policy: the v1 request must
   not idle while an idle inhibitor is active; the v2 input request ignores
   inhibitors and reacts to input only.
4. hypridle (v0.1.8) builds `staging/ext-idle-notify`, binds
   `ext_idle_notifier_v1`, converts rule timeout seconds to msec, maps
   `idled`/`resumed` to `on-timeout`/`on-resume`, and selects the input variant
   only when `ignore_wayland_inhibit`/`ignore_inhibit` is set.
5. hypridle's lock awareness comes from `hyprland-lock-notify-v1` plus logind DBus,
   not from ext-idle-notify — the two surfaces should not be conflated in a route
   note.

## 6. Suggested SOURCES rows (L1 assigns ids; drafts say S0xx-pending)

| id | tier | url | sha256 | access | anchor/quote |
|---|---|---|---|---|---|
| S0xx-pending | A (upstream tag) | `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/ext-idle-notify/ext-idle-notify-v1.xml` | `e56a9c22684e6b46655f7221b798328e304c1efc8f63f01241a1cf8c070f4c30` | 2026-10-20 | L95–96 "the compositor must not make the notification object idle" (9 words) |
| S0xx-pending | A (upstream tag) | `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp` | `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` | 2026-10-20 | L74–79 request selection; L30–32 bind |
| S0xx-pending | A (upstream tag) | `https://raw.githubusercontent.com/hyprwm/Hyprland/v0.51.1/src/managers/ProtocolManager.cpp` | `e295d20253ff158e83557a7cdab2cd5b5e6ae29243b066a238c4c3fdbb97ab33` | 2026-10-20 | L166 global registered at version 2 |

All three are primary upstream artifacts at pinned tags, hashed from raw bytes;
none is a host observation.
