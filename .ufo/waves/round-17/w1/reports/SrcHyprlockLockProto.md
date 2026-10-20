# hyprlock → ext-session-lock-v1 binding, at tag-pinned source (round 17, W1)

Seat: `MadoR17.SrcHyprlockLockProto`. Scope: at hyprlock's latest release tag, locate the
code that binds `ext-session-lock-v1`, and record the wayland-protocols
`staging/ext-session-lock/ext-session-lock-v1.xml` semantics for `lock` /
`unlock_and_destroy` and for client death while locked. Report only; source bytes only.

Method — network reads with `curl` and local `sha256sum`/`grep`/`sed` on the fetched bytes:
no `pacman`/`yay`/`paru` (not even `-Q`/`-Si`, pause), no `sudo`, no `systemctl`, no
`hyprctl`, no `hyprlock`/`hypridle`, no live/device probes, no screenshots, no OMP
transcripts, no `git`/`jj` commands. Read `corpus/lessons/round-16-verifier-spotcheck.md`
first (done). Nothing was built, installed, or executed. No tools installed or updated.

Tags: `[OBS]` byte observed in fetched artifact · `[INF]` inference from those bytes ·
`[UNK]` unknown / not established by these fetches.

This report is **documentary source evidence**, not host observation. A tag's source does
not prove what the host binary or compositor do (see §7).

## 1. Tag resolution and fetched artifacts `[OBS]`

Latest release for `hyprwm/hyprlock` resolved on 2026-10-20 via
`curl -sSIL https://github.com/hyprwm/hyprlock/releases/latest` →
`200 https://github.com/hyprwm/hyprlock/releases/tag/v0.9.6`; release page title
`Release v0.9.6 · hyprwm/hyprlock · GitHub`. Tag-pinned `VERSION` file content: `0.9.6`.

| Artifact | Tag-pinned raw URL | Bytes | Lines | sha256 |
|---|---|---|---|---|
| hyprlock source tree (tarball) | `https://codeload.github.com/hyprwm/hyprlock/tar.gz/refs/tags/v0.9.6` | 85 275 | — | `7f653b87765bcfff7c1f8e04af326a7e73bbcacd1fb7d4436f6a16624a2247bb` |
| `src/core/hyprlock.cpp` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/src/core/hyprlock.cpp` | 32 922 | — | `68b5491c4ea9105e51b31d1694c18c62efd4addaef24b261ff32556f56ce3663` |
| `src/core/LockSurface.cpp` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/src/core/LockSurface.cpp` | 6 398 | — | `7561d7127fe6db973f4e20ecbaf894d2c118c7a921e400581762dfc3e38d9a0f` |
| `src/core/Output.cpp` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/src/core/Output.cpp` | 2 312 | — | `b971f74e64dae4a7a926b31d787940390dcc7de303243b66bf6c6925a4d22849` |
| `src/renderer/Renderer.cpp` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/src/renderer/Renderer.cpp` | 26 037 | — | `bea8eb00a02f33fdd7d1952cbc7330d7aeee23fc06e1a5a2d71d35b7795417cf` |
| `CMakeLists.txt` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/CMakeLists.txt` | 5 301 | — | `96d8c54a4f1669cf1052f6d0dab8e6169762c2ad46a6d5b4c148bd5c65a0d54e` |
| ext-session-lock-v1 XML @ wayland-protocols `1.49` | `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/ext-session-lock/ext-session-lock-v1.xml` | 16 072 | 328 | `a05df7d95c5e523e457037b3a149484e8064828cda66971f3c7caeb87d597a81` |

Cross-check `[OBS]`: the five raw GitHub files hash identically to the same paths
extracted from the tag tarball (5/5 match), so the line citations below are tag-pinned.
The XML fetched at tag `1.48` produced the **identical** digest `a05df7d9…597a81`
(16 072 bytes), so the quoted text is stable across the two most recent tags. The
wayland-protocols `/tags` page observed on 2026-10-20 lists `1.49` as the highest tag
(names `1.38 … 1.49`; max `1.49`, tag link `/wayland/wayland-protocols/-/tags/1.49`).

All quotes below are ≤25 words, copied verbatim, with 1-based line anchors into these
exact bytes.

## 2. hyprlock binds the global: one place, version 1 `[OBS]`

`src/core/hyprlock.cpp`:

- L306: `} else if (IFACE == ext_session_lock_manager_v1_interface.name)`
- L307–308:
  `m_sWaylandState.sessionLock = makeShared<CCExtSessionLockManagerV1>((wl_proxy*)wl_registry_bind((wl_registry*)r->resource(), name, &ext_session_lock_manager_v1_interface, 1));`

So the client binds `ext_session_lock_manager_v1` at **interface version 1**, via the
generated `hyprwayland-scanner` wrapper, in the registry handler.

Failure is fatal, not degraded (L347–350):

```text
    if (!m_sWaylandState.sessionLock) {
        Log::logger->log(Log::CRIT, "Couldn't bind to ext-session-lock-v1, does your compositor support it?");
        exit(1);
    }
```

- L345 and L353: `wl_display_roundtrip(...)` around global discovery, before the missing-
  global check.
- L375–380: if `acquireSessionLock()` returns false, the client notifies its loop,
  terminates auth, and `exit(1)`.

Build-time provenance `[OBS]`: `CMakeLists.txt` L80 requires `wayland-protocols>=1.35` and
L154 declares `protocolnew("staging/ext-session-lock" "ext-session-lock-v1" false)`, i.e.
the protocol XML is consumed from the build host's wayland-protocols **staging**
directory. hyprlock ships no local copy of this XML (`protocols/` contains only
`wlr-screencopy-unstable-v1.xml`). `README.md` L5 states: `- Uses the ext-session-lock
protocol`.

## 3. Lock acquisition in hyprlock `[OBS]`

`src/core/hyprlock.cpp`, `CHyprlock::acquireSessionLock()` L760–790:

- L762: `m_sLockState.lock = makeShared<CCExtSessionLockV1>(m_sWaylandState.sessionLock->sendLock());`
- L768: `m_sLockState.lock->setLocked([this](CCExtSessionLockV1* r) { onLockLocked(); });`
- L770: `m_sLockState.lock->setFinished([this](CCExtSessionLockV1* r) { onLockFinished(); });`
- L772–773 comment/roundtrip: `// roundtrip in case the compositor sends \`finished\` right away`
- L775–777: if `m_bTerminate` was set by a `finished`-triggered handler, return false
  (`// recieved finished right away (probably already locked)` [sic]).
- L779: `m_lockAquired = true;` [sic]
- L782–788: creates a session-lock surface per ready output.

`src/core/LockSurface.cpp`:

- L50: `lockSurface = makeShared<CCExtSessionLockSurfaceV1>(g_pHyprlock->getSessionLock()->sendGetLockSurface(surface->resource(), pOutput->m_wlOutput->resource()));`
- L51: `RASSERT(lockSurface, "Couldn't create ext_session_lock_surface_v1");`
- L53: `setConfigure(...)` → `configure({(double)width, (double)height}, serial)`
- L70: `lockSurface->sendAckConfigure(serial);`

`src/core/Output.cpp` L26–28 / L48–59 gates surface creation on
`g_pHyprlock->isLockAquired() && !m_sessionLockSurface` and constructs
`CSessionLockSurface`.

## 4. Unlock path in hyprlock `[OBS]`

`src/core/hyprlock.cpp`, `CHyprlock::releaseSessionLock()` L792–820:

- L800–803: refuses if no lock object (`"Unlock without a lock object!"`).
- L805–810: refuses unless the `locked` event arrived, with the code comment at L806:
  `// Would be a protocol error to allow this`; log text L808:
  `"Trying to unlock the session, but never recieved the locked event!"` [sic].
- L811: `m_sLockState.lock->sendUnlockAndDestroy();`
- L812: `m_sLockState.lock = nullptr;`
- L814: `Log::logger->log(Log::INFO, "Unlocked, exiting!");`
- L819: `wl_display_roundtrip(m_sWaylandState.display);`

`src/renderer/Renderer.cpp` L613 triggers `releaseSessionLock()` when a fade-out
callback ends (`opacity->setCallbackOnEnd([](auto) { g_pHyprlock->releaseSessionLock(); }, true);`).

`onLockFinished()` L828–846 handles the compositor's `finished` event:

- L829 log: `"onLockFinished called. Seems we got yeeten. Is another lockscreen running?"`
- L836–838 comment: `// The \`finished\` event specifies that whenever the \`locked\` event has been recieved and the compositor sends \`finished\`,` / `// \`unlock_and_destroy\` should be called by the client.` / `// This does not mean the session gets unlocked! That is ultimately the responsiblity of the compositor.` [sic]
- L839–840: if `m_sLockState.locked` → `sendUnlockAndDestroy()`; else L842
  `m_sLockState.lock.reset();`
- L844–846: clears state, sets `m_bTerminate = true`.

`[INF]` hyprlock's `wl_display_roundtrip` after `unlock_and_destroy` is a client-side
synchronisation. The protocol text asks an exiting client to use `wl_display.sync` (§5);
libwayland's `wl_display_roundtrip` is defined to issue a `sync` and dispatch until the
callback fires, so the intent is plausibly met — but libwayland's source was **not fetched
in this pass**, so the equivalence is inference, not byte evidence.

## 5. Protocol semantics, quoted from the 1.49 XML `[OBS]`

All three interfaces declare `version="1"` (L48 manager, L72 lock, L240 surface). The
document still carries the testing-phase warning (L42–45): `Warning! The protocol
described in this file is currently in the testing phase.`

### 5.1 `lock` — who authenticates, and client death

- L33–34: "The client is responsible for performing authentication and informing the
  compositor when the session should be unlocked."
- L34–36: "If the client dies while the session is locked the session remains locked,
  possibly permanently depending on compositor policy."
- L63–64 (`ext_session_lock_manager_v1.lock` description): "This request creates a
  session lock and asks the compositor to lock the session."
- L64–66: "The compositor will send either the ext_session_lock_v1.locked or
  ext_session_lock_v1.finished event on the created object in response to this request."

### 5.2 `ext_session_lock_v1`: what `locked` obliges, and death while locked

- L77–79: "The locked event indicates that the session is locked. This means that the
  compositor must stop rendering and providing input to normal clients."
- L79–80: "Instead the compositor must blank all outputs with an opaque color such that
  their normal content is fully hidden."
- L87–88: "The locked event must not be sent until a new "locked" frame (either from a
  session lock surface or the compositor blanking the output)"
- L88–90: "has been presented on all outputs and no security sensitive normal/unlocked
  content is possibly visible."
- L111–112: "If the client dies while the session is locked, the compositor must not
  unlock the session in response."
- L112–113: "It is acceptable for the session to be permanently locked if this happens."
- L113–114: "The compositor may choose to continue to display the lock surfaces the client
  had mapped before it died"
- L115: "or alternatively fall back to a solid color, this is compositor policy."
- L117–118 recovery policy: "Compositors may also allow a secure way to recover the
  session, the details of this are compositor policy."
- L118–120: "Compositors may allow a new client to create a ext_session_lock_v1 object and
  take responsibility for unlocking the session"
- L120–121: "they may even start a new lock client instance automatically."

So the protocol's answer to "what happens if the client dies": the session **stays
locked**; the compositor must not unlock, may keep showing the dead client's last mapped
lock surfaces or a solid colour, and may (policy) let a new client take over. Permanent
lock is explicitly acceptable.

### 5.3 `finished` — lock object must go away, not a session unlock

- L167–168: "The compositor has decided that the session lock should be destroyed as it
  will no longer be used by the compositor."
- L168–170: "Exactly when this event is sent is compositor policy, but it must never be
  sent more than once for a given session lock object."
- L172–173: "This might be sent because there is already another ext_session_lock_v1
  object held by a client"
- L173–174: "or the compositor has decided to deny the request to lock the session for
  some other reason."
- L174–176: "This might also be sent because the compositor implements some alternative,
  secure way to authenticate and unlock the session."
- L186–187 client obligation: "Upon receiving this event, the client should make either the
  destroy request or the unlock_and_destroy request" / L187–188 "depending on whether or
  not the locked event was received on this object."
- L178–180: "The finished event should be sent immediately on creation of this object if
  the compositor decides that the locked event will not be sent."

### 5.4 `destroy` vs `unlock_and_destroy`

- `destroy` (L137–149) is for a lock object that never received `locked`. L139–140:
  "This informs the compositor that the lock object will no longer be used."
- L146–147: "It is a protocol error to make this request if the locked event was sent,
  the unlock_and_destroy request must be used instead."
- `unlock_and_destroy` (L211–237) is the unlock request. L213: "This request indicates
  that the session should be unlocked"
- L214–215: "for example because the user has entered their password and it has been
  verified by the client"
- L217–218: "This request also informs the compositor that the lock object will no longer
  be used and should be destroyed."
- L218–219: "Existing objects created through this interface remain valid."
- L221–222: "After this request is made, lock surfaces created through this object should
  be destroyed by the client"
- L225–226: "It is a protocol error to make this request if the locked event has not been
  sent."
- L226–227: "In that case, the lock object must be destroyed using the destroy request."
- L229–230: "Note that a correct client that wishes to exit directly after unlocking the
  session must use the wl_display.sync request"
- L230–231: "to ensure the server receives and processes the unlock_and_destroy request."
- L231–232: "Otherwise there is no guarantee that the server has unlocked the session"
- L232–233: "due to the asynchronous nature of the Wayland protocol."
- L233–235: "For example, the server might terminate the client with a protocol error
  before it processes the unlock_and_destroy request."
- On the `locked` event itself, L160–161: "If this event is sent, making the destroy
  request is a protocol error"
- L161: "the lock object must be destroyed using the unlock_and_destroy request."

Error enum for the same rules (L124–135): `invalid_destroy` = 0 "attempted to destroy
session lock while locked"; `invalid_unlock` = 1 "unlock requested but locked event was
never sent"; `role` = 2; `duplicate_output` = 3; `already_constructed` = 4.

## 6. Client/protocol correspondence (observed alignments)

| Protocol rule (XML anchor) | hyprlock code anchor | Note |
|---|---|---|
| manager `lock` → `locked` or `finished` (L61–66) | `sendLock()` L762; `setLocked` L768; `setFinished` L770; immediate roundtrip L773 | hyprlock handles the `finished`-on-creation case and exits (L775–777 → L375–380) |
| `locked` must not precede a locked frame (L87–90) | client callback `onLockLocked` L822–826 sets `m_sLockState.locked = true` | no local frame-presentation assertion in the fetched lines; alignment is [INF] |
| `unlock_and_destroy` only after `locked` (L225–227) | guard L805–810 then `sendUnlockAndDestroy()` L811 | explicit code comment at L806 calls the alternative a protocol error |
| exit-after-unlock needs server receipt (L229–235) | `wl_display_roundtrip` L819 | [INF] roundtrip embeds a sync; libwayland source not fetched |
| `finished` while locked still requires `unlock_and_destroy` (L160–161) | L839–840 | hyprlock comment L838: "This does not mean the session gets unlocked!" |
| client death leaves session locked (L111–113) | none — this is compositor-side | hyprlock cannot and does not unlock on its own death |

## 7. Remaining unknowns

- `[UNK]` Host hyprlock binary version/identity: tag v0.9.6 source is **not** evidence of
  the installed package; no package queries were run (pause).
- `[UNK]` Host compositor's support for `ext_session_lock_manager_v1` and its policy on
  client death (blank vs retained surfaces, auto-restart, recovery). Requires a live
  `hyprctl`/compositor query, which this round forbids; not inferred from hyprlock source.
- `[UNK]` Whether the host's build used wayland-protocols ≥1.35 or a 1.49 XML. The
  fetched 1.48 and 1.49 bytes are identical, so any 1.48/1.49 staging copy has the same
  text; earlier tags were not fetched.
- `[UNK]` Runtime behaviour of the host's lock path (never executed or observed).
- `[INF]` The protocol-level "session remains locked if the client dies" is exactly the
  documentary failure mode that makes hyprlock's own exit paths (L349, L379, L844–846)
  compositor-policy dependent; that consequence is read from the XML, not measured.

Report: .ufo/waves/round-17/w1/reports/SrcHyprlockLockProto.md
