# RevKnowledge — waybar-module-text-route-r25.md vs corpus/QUALITY.md

Seat: w1 RevKnowledge. Reviewed 2026-10-24, lane-dispatched, not an outside
verifier. Subject: `corpus/knowledge/waybar-module-text-route-r25.md` (27
lines). Bar: `corpus/QUALITY.md` plus the lane's established route-file
convention (`dispatcher-semantics-r25.md`, `bind-table-r25.md`,
`ipc-contract-r25.md` — `## Gate` block, located quotes).

## Verdict per criterion

| # | Criterion | Verdict |
|---|---|---|
| 1 | Decision table | **FAIL** — absent |
| 2 | Error signature | **PASS** |
| 3 | Located quote for each cited id | **PASS** (one claim overstates its quote — see caveat) |
| 4 | Gate block with URL and access date | **FAIL** — no `## Gate`; URL/date present in header only |
| 5 | No filler | **PASS** |

## Evidence

### 1. Decision table — FAIL

No table exists anywhere in the file. The file's entire structure is a header
(`:3-13`), `### What the bytes say` (`:15`), and `### What this does not
license` (`:24`). Sibling route notes carry explicit decision/anchor tables
(`bind-table-r25.md:29-36` flag-suffix table; `theme-route-r18.md:19-30`
anchor-key table; `keybind-rule-semantics.md:63` "Modifier grammar — decision
table"). `walker-deep.md` §9 and `hyprland-config-plane.md` §7 likewise carry
them. This note ships none.

### 2. Error signature — PASS

`gate-quote: S201 $XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr`
(`:12`) is a verbatim error signature from `spdlog::warn` at
`backend.cpp:38` in tag 0.15.0 — re-fetched and confirmed today:

```
38:    spdlog::warn("$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr");
```

The signature is real, located, and named in SOURCES.md S201 (":203").

### 3. Located quote for each cited id — PASS, with one caveat

Two cited ids, both carry verbatim quotes confirmed against upstream bytes:

- `gate-quote: S201` (`:12`) — verbatim at `backend.cpp:38`, and the note cites
  "S201 line 38" (`:18`). Match.
- `gate-quote: S202 m_ipc.registerForIPC("activewindow", this);` (`:13`) —
  verbatim at `window.cpp:27`, cited "S202 line 27" (`:21`). Match.

Caveat (over-reach, criterion 1/41 spirit — the claim says more than the quote):
the OBS at `:17-19` reads "The Hyprland backend derives a socket folder and
warns when `$XDG_RUNTIME_DIR/hypr` is absent (S201 line 38). **That warning is
the event-socket client path, not the request socket.**" The emphasised clause
is not located and is false as stated: `getSocketFolder()` is shared — the warn
at `:38` is inside it, and it is called by both the event socket
(`backend.cpp:98`: `"/.socket2.sock"`) and the request socket (`backend.cpp:198`:
`"/.socket.sock"`). The warning marks the socket-*folder* derivation common to
both, not the event-socket path specifically.

### 4. Gate block with URL and access date — FAIL

No `## Gate` heading exists. The convention in the same round family is an
explicit `## Gate` section carrying per-source URL, open date, byte count and
sha256 — e.g. `dispatcher-semantics-r25.md:14-22`:

```
## Gate
- **S188** — https://raw.githubusercontent.com/... — opened 2026-10-24;
  12,879 B, sha256 c830ce07...
```

This note has only flat header lines (`:7-9`):

```
source: S201 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp — tag 0.15.0
source: S202 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp — tag 0.15.0
verified-at: 2026-10-24
```

URL: present per source (`:7-8`). Access date: `verified-at: 2026-10-24` (`:9`)
supplies it semantically. Missing: the `## Gate` block itself, the fetched-byte
receipt path (siblings name `.ufo/waves/round-*/fetch/S*.bin`), and per-source
sha256/size (SOURCES.md :203-204 carries sha256 prefixes `799bf02f6d18ae04` /
`5df496eb3cfe5cae` — the note does not reproduce them, so the Gate block does
not stand on its own).

### 5. No filler — PASS

27 lines, all load-bearing: provenance and read-only boundary (`:3-5`), source
pins (`:7-10`), gate quotes (`:12-13`), two OBS claims (`:17-22`), one UNK
scope limit (`:26-27`). No ceremony, no marketing, no restatement. The only
weak sentence is the over-reaching clause quoted under criterion 3 — that is an
accuracy defect, not filler.

## Summary

**2 of 5 criteria met.** The note's quotes are real and located and its UNK
boundary is honest, but it fails the required Gate-block shape and ships no
decision table, and its S201 OBS overclaims what the quote supports (the warn
serves both sockets, not only the event socket). Admission as-is: **reject /
repair before keeping** — needs a `## Gate` block with receipts and shas, a
decision table, and correction of the event-socket-only clause (append-only
erratum per criterion 44/4 if the note is already committed).
