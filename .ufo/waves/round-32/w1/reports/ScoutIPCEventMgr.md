# ScoutIPCEventMgr — S189 re-open (read-only fetch + staged-entry check)

- **Source**: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp (Hyprland v0.56.2)
- **Fetch result**: HTTP 200, `curl -fsSL`. No error.
- **Byte length**: 6479 bytes (`wc -c`)
- **sha256**: `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` (prefix `eea605dfe5ce09e1`)
- **Access date**: 2026-10-24 (UTC)
- **Fetched copy**: `.ufo/waves/round-32/scratch/ScoutIPCEventMgr/EventManager.cpp` (192 lines)

## §1 The five items in the fetched bytes

### (1) Socket path construction — line 21

Derived from the compositor instance path; bounds-checked against `sun_path` at line 22, copied at line 27.

> `const auto  PATH          = g_pCompositor->m_instancePath + "/.socket2.sock";`

### (2) Socket type and listen backlog — lines 14, 34–35

> `CEventManager::CEventManager() : m_socketFD(socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0)) {`

> `// 10 max queued.`

> `if (listen(m_socketFD.get(), 10) < 0) {`

AF_UNIX, SOCK_STREAM, non-blocking (`SOCK_NONBLOCK`), close-on-exec; backlog literal `10`.

### (3) `formatEvent` framing — line 128 (function at 126–131)

> `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`

`EVENT>>DATA\n` framing produced by `std::format`.

### (4) Data truncation length — line 128

`data.substr(0, 1024)` inside the format call — payload capped at 1024 `std::string_view` chars.

### (5) Newline sanitisation — line 129

> `std::replace(eventString.begin() + event.event.length() + 2, eventString.end() - 1, '\n', ' ');`

Range covers only the payload: starts after `event.event` + the `>>` separator, ends before the trailing `\n`. Newlines inside payload → spaces; framing newline survives.

## §2 Staged-entry check — `ipc-contract-r25.md` vs the fetched bytes

Staged file: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/ipc-contract-r25.md`. Verdicts per S189-attributed claim; S186/S187 claims are out of scope for this byte check.

### Claim A — staged lines 46–50 — **AGREE**

> "the v0.56.2 source tree contains **no** `src/ipc/` path, so any source citation that places the socket in `src/ipc/s1/` or `src/ipc/s2/` describes a *later* restructure"

Attribution `(S189, tree check on commit efb50993…)` is a tree claim, not a file-line claim — file alone cannot prove directory absence, so I verified against the git tree: `GET api.github.com/repos/hyprwm/Hyprland/contents/src/ipc?ref=efb50993…` → HTTP 404. `src/ipc/` absent at the pinned commit. Agree.

### Claim B — staged lines 52–55 — **AGREE**

> "The socket path is derived from the compositor's instance path (S189:21): `const auto  PATH          = g_pCompositor->m_instancePath + "/.socket2.sock";`"

Fetched line 21 is byte-identical to the staged quote. Right file, right line. Agree.

### Claim C — staged lines 57–59 — **AGREE**

> "It is a non-blocking AF_UNIX stream with a backlog of ten (S189:14, :35): `// 10 max queued.`"

- Non-blocking AF_UNIX stream: line 14 `socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0)` — correct line.
- Backlog ten: `listen(m_socketFD.get(), 10)` is at line 35 — correct line.
- Nit (not an attribution error): the quoted comment `// 10 max queued.` sits on line 34, one above the cited `:35`. The claim's own line refs are right; only the quote's physical line is 34. Agree.

### Claim D — staged lines 61–66 — **AGREE**

> "The framing rule, including the truncation and the newline sanitisation, is in one function (S189:126-129)"

Staged quotes match fetched bytes verbatim:
- Line 128: `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`
- Line 129: `std::replace(eventString.begin() + event.event.length() + 2, eventString.end() - 1, '\n', ' ');`

The cited range 126–129 covers signature (126), `data` (127), format (128), replace (129). Right file, right range. Agree.

### Claim E — staged lines 68–71 — **AGREE**

> "The data payload is truncated to 1024 characters and any newline inside the payload is flattened to a space"

Derived from the verified lines 128–129. Precision note: `substr(0, 1024)` truncates to *at most* 1024 chars; the replace range excludes the framing newline, so only payload newlines flatten. Both read correctly out of the staged sentence. Agree.

### Claim F — staged line 12 (source header) — **AGREE**

> "source: S189 — …/src/managers/EventManager.cpp — `CEventManager::formatEvent` — commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2)"

Same URL and commit as fetched; `formatEvent` exists at line 126. Agree.

### §6 recheck spot-check — staged lines 98–102 — **AGREE**

> "curl -fsSL '…EventManager.cpp' | grep -c 'substr(0, 1024)'" — expected `1`.

Re-ran against the fetched file: `grep -c 'substr(0, 1024)'` → `1`. Matches the staged expectation.

### Not checked from these bytes (out of scope)

Staged claims citing S186 (wiki `_index.md`: request socket path, synchronous evaluation, `EVENT>>DATA\n` doc, 44-event catalogue) and S187 (0.56.0 wiki) cannot be verified from `EventManager.cpp`; different sources, not fetched under this scout id.

## Verdict

**6/6 S189-attributed claims AGREE.** One non-blocking nit: the `// 10 max queued.` quote lives at line 34 while the claim cites :35 (the `listen()` line — the correct attribution for the backlog fact). No attribution errors; no disagreements.

## Evidence appendix

```
$ wc -c EventManager.cpp → 6479
$ sha256sum EventManager.cpp → eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d
$ curl -w '%{http_code}' …/EventManager.cpp → 200
$ grep -c 'substr(0, 1024)' EventManager.cpp → 1
$ curl …/contents/src/ipc?ref=efb50993… → 404
```
