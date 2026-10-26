# CritEntryHyprland — round 44 w2 — sections 1-2 of the gkeep size-request entry

Status: **COMPLETE**. Verifier `verify.sh` → `CHECKS=58 FAILURES=0` (`quotes-verified.txt`).

Scope: the compositor-side claims of `corpus/knowledge/hyprland-gkeep-size-request-r44.md` §1 and §2, sentence by
sentence, against the two Hyprland pins only. Sections 3-5 (protocol, GTK, gkeep) were not attacked here — they are a
sibling w2 seat's target — and the C2 predicate is out of this seat's target.

Pins (sha256 recomputed, agree with `receipts/fetch-sha256.txt:2-3`):
- `fetch/Hyprland-Window.cpp` 2966 lines `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded`
- `fetch/Hyprland-XDGShell.cpp` 980 lines `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0`

## Verdicts (one row per claim; locators computed with `grep -n`/`sed -n`, verified by `verify.sh`)

| # | entry sentence (fragment) | locator (the entry's where it gives one; pinned lines for the INF rows) | verdict |
|---|---|---|---|
| 1 | report size is the GOAL of the animated size, clamped at zero | Window.cpp:1687 | **supported** |
| 2 | for X11 clamps at 1x1 and may scale by the monitor | Window.cpp:1691, :1694-1696 | **supported** |
| 3 | returns early when the pending reported size is unchanged and the call is not forced | Window.cpp:1743-1744 | **overstated** — omits the X11 position conjunct (F3) |
| 4 | otherwise configures an X11 surface directly | Window.cpp:1751 | **supported** |
| 5 | or, for an xdg toplevel, appends the serial returned by setSize and the floored size | Window.cpp:1753 | **supported** |
| 6 | setSize stores the size as pending state and returns the next configure serial | XDGShell.cpp:354-358 | **supported**, with the coalescing caveat (N2) |
| 7 | the deferred state application sends it to the client | XDGShell.cpp:443-455 | **supported** (size read at fire time) |
| 8 | onAck takes the newest pending pair whose serial is not after the acknowledged one | Window.cpp:1515, :1517 | **supported** |
| 9 | drops it and every older pair | Window.cpp:1521 | **overstated** — also drops equal-serial siblings (F5); the ack gate upstream is unmentioned (F4) |
| 10 | writes that pair's size into the surface's pending state as the acked size | Window.cpp:1526-1527 | **supported** |
| 11 | the ack records which size the client says it is answering | (INF, Window.cpp:1515-1526) | **overstated** — the client sends a serial only (F1) |
| 12 | it does not force the client's next buffer to be that size | Window.cpp:1514-1529 | **supported** — `onAck` sends/emits nothing to the client (0 `send`/`emit` hits in its body); it only writes local state |
| 13 | what Hyprland does with a buffer of another size is outside this entry's pins (UNK) | Window.cpp:1861-1865 | **overstated** — a pinned consumer exists (F2) |

No locator in §1-§2 is wrong: every cited line/range was hit exactly where the entry puts it.

## Findings (each: what it attacks, severity, reproduction, smallest safe correction)

**F1 — MEDIUM. The ack carries no size, so "the size the client says it is answering" re-imports the predecessor
reading this entry rejects.** Attacks §2 INF sentence 11. Source: `setAckConfigure` takes one payload, the serial
(`XDGShell.cpp:601`), drops stale serials (`:602-603`) and re-emits it (`:605`); `onAck` writes the *compositor's*
stored number (`Window.cpp:1520`, `:1526`). Repro: `sed -n '601,605p' fetch/Hyprland-XDGShell.cpp`. The entry's own
"what the pins correct" section says the same thing, so §2 and that section disagree in framing.
Smallest safe correction, exact sentence: "The ack carries a serial only; it names which of the compositor's own
pending (serial, size) pairs the client is answering, and the size written back is the compositor's
(Hyprland-Window.cpp:1520-1526), not one the client chose."

**F2 — MEDIUM. "outside this entry's pins (UNK)" understates what the pin pair shows.** Attacks §2 INF sentence 13.
`ackedSize` has exactly two occurrences in the pinned Window.cpp: the write (`:1526`) and a **read** in
`getReportedSize` (`:1861-1865`) that returns it as the window's reported size; the third hit of
`grep 'ackedSize\|updated.bits.acked'` is the flag write (`:1527`). `XDGShell.cpp` has none. Neither pin compares a
committed buffer size with it. So the pins answer "nothing size-specific", and the only genuinely unpinned step is
the pending-to-current promotion in the wl_surface commit handler.
Repro: `grep -c ackedSize fetch/Hyprland-Window.cpp` → 2, `grep -c ackedSize fetch/Hyprland-XDGShell.cpp` → 0.
Smallest safe correction, exact sentence: "The ack changes only the compositor's stored size: it writes it into the
surface's pending state as the acked size (Hyprland-Window.cpp:1526-1527), getReportedSize then returns it as the
window's reported size (Hyprland-Window.cpp:1861-1865), and no line in either pin compares a committed buffer size
with it; only the pending-to-current promotion lies outside these pins."

**F3 — LOW. The early return is stated without its X11 position conjunct.** Attacks §1 sentence 3, which covers
both branches (`:1751` X11 and `:1753` xdg). Source line: `if (!force && m_pendingReportedSize == REPORTSIZE &&
(m_reportedPosition == REPORTPOS || !m_isX11))` (`Window.cpp:1743`). For X11 an unchanged size with a moved position
does **not** return early; for Wayland the position half is short-circuited, so the entry's sentence is true only for
the case it happens to care about. Repro: `sed -n '1743,1744p' fetch/Hyprland-Window.cpp`.
Smallest safe correction: "returns early when the call is not forced and the pending reported size is unchanged — and,
for an X11 client, the reported position is unchanged too (Hyprland-Window.cpp:1743-1744); a Wayland client skips the
position test."

**F4 — LOW. The XDG-side ack gate is missing, so "when the client acknowledges, onAck ..." is not universal.**
Attacks §2 sentence 8 (and, adjacent, §3's "that ack is what Hyprland's onAck receives" — outside this seat's
sections, flagged for the L1). Source: `if (serial < m_lastConfigureSerial) return;` (`XDGShell.cpp:602-603`) runs
before `m_events.ack.emit(serial)` (`:605`), so an ack older than the last accepted one never reaches `onAck`.
Repro: `sed -n '601,605p' fetch/Hyprland-XDGShell.cpp`.
Smallest safe correction / addendum clause: "Before onAck runs, the xdg_surface ack handler drops any ack whose serial
is older than the last one it accepted (Hyprland-XDGShell.cpp:601-605), so onAck only ever sees non-decreasing
serials."

**F5 — LOW. "it and every older pair" also takes equal-serial siblings.** Attacks §2 sentence 9. The erase predicate
is `el.first <= SERIAL->first` (`Window.cpp:1521`), and two `setSize` calls before the loop drains return the *same*
serial (`XDGShell.cpp:630-631`) and push two pairs with it (`Window.cpp:1753`), so one ack retires both.
Repro: `sed -n '1515,1521p' fetch/Hyprland-Window.cpp` together with `sed -n '629,637p' fetch/Hyprland-XDGShell.cpp`.
Smallest safe correction: "drops every pair whose serial is not after the matched pair's — including any pair sharing
that serial".

## Supporting notes (not entry errors; sharpen the same sentences)

**N1 — the serial and the size travel in two different events.** The serial returned by `setSize` is the serial of the
**xdg_surface.configure** event (`XDGShell.cpp:635`, `:637`, sent at `:642`); the size travels in the separate
**xdg_toplevel.configure** event (`:455`), which carries no serial. The pending-ack pair joins the two. This is
supported, and it is the precise answer to "is scheduleConfigure's serial the configure's serial": yes for the
surface configure, by construction — the serial is minted once per scheduled configure (`:629-637`) and read at fire
time (`:640-642`), and it is reused, not re-minted, whenever a configure is already scheduled (`:630-631`).

**N2 — the pair list is not one pair per configure.** `scheduleStateApplication` latches on its own `m_stateUpdate`
(`:443-445`) and the surface scheduler latches independently (`:629-631`), so two `setSize` calls in one loop turn
produce one `xdg_toplevel.configure` carrying the *last* size and two pending pairs (same serial, two sizes). The
reverse "newest `<=`" search then resolves to the last one, which is the size actually sent, so the mapping stays
correct; a reader of §2 should not assume pair *k* is configure *k*.

**N3 — a popup can mint the surface serial.** `CXDGPopupResource::configure` sends the popup configure and then calls
`m_surface->scheduleConfigure()` (`:130-132`), so a toplevel pair can be recorded against a serial minted by a popup's
schedule. Irrelevant to gkeep (no popups) and harmless to the claim, but the serial is the *surface's*, not the
toplevel's.

**N4 — source-level note, not an entry error.** The erase at `Window.cpp:1521` reads `SERIAL->first` through a reverse
iterator into the vector that `std::erase_if` is simultaneously shifting. It is benign only because the list stays
non-decreasing in serial (the serial only grows and erasure is prefix-only), so no element with a serial above the
match is retired in practice.

**Predicate note.** PRED-C2-r44-v2's witness (`hyprland sendWindowSize xdg_setSize=1 x11_configure=1`) is a structural
count: `sed -n '1732,1754p' fetch/Hyprland-Window.cpp` contains exactly one `configure(` and one `setSize(` — the
inline numbers are reproducible. Nothing in C2 tests the truth of a §1-§2 sentence, and the counter declares exactly
that residual: "a true quote at a true locator can stand beside a claim it does not support"
(`quality/counters/c2-r44-gkeep-size-request-v2.py:65-66`), and "clause j binds a locator and a keyword per surface,
not the truth of the sentence around them" (`:67-68`). So F1-F5 are **content corrections for the L1**, inside a
residual C2 already declares; they are not an OPEN predicate defect and no re-registration is implied. The only
predicate-adjacent observation is the scope limit that an admitted entry may carry a false behavioural sentence
unchallenged.

## Evidence

`verify.sh` (this directory) greps each quoted/located line out of the pins and fails on any mismatch; its output is
`quotes-verified.txt` (`CHECKS=58 FAILURES=0`, exit 0; run with
`TMPDIR=/fast/scratch/hyaku/mado-r44/CritEntryHyprland`).

## Housekeeping

- No tracked file edited; no counter, control, registration, reference, pin, README or corpus file touched. Writes
  confined to `.ufo/waves/round-44/w2/CritEntryHyprland.md` and `.ufo/waves/round-44/w2/CritEntryHyprland/`.
- No tool installed or upgraded (none needed; `sed`/`grep`/`sha256sum` only).
- Scratch `/fast/scratch/hyaku/mado-r44/CritEntryHyprland` removed after the receipt was copied into this seat.
- Only read-only compositor calls were not needed: no `hyprctl` call was made, no host binary or config read, no
  Wayland connection, no git/jj command in the lane or the fleet.

