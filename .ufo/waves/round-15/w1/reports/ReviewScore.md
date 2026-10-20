# ReviewScore — round 15 C1 coverage 5/7 → 6/7 (U6 integration risk)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline HEAD `ea0446f`.
Scope: coverage score mapping only. No commits, tests, gates, builds, input
observers, record/replay, device reads or lane-artifact edits were performed.
Read-only: lane files, primary docs (fetched), static `--help`/`--version`,
installed XML bytes, `pacman -Q`.

## Verdict

**Not yet accepted. Conditional.** The score mapping is arithmetically right
(`10×5/7 = 7.1429`, `10×6/7 = 8.5714`, delta `+1.4286`), but on the current
tree **U6 is not credited**: the coverage counter would still read 5/7 =
7.1429. The draft note has one factual defect (version boundary) that must be
fixed before admission. 6/7 is a bounded documented-route ceiling, not input
coverage and not saturation.

## Observed state

| Item | Observation | Pointer |
|---|---|---|
| Committed `covers:` lines | U1–U5 only; no `covers: U6` | `grep -rn '^covers:' corpus/knowledge/` (HEAD `ea0446f`) |
| Draft U6 note | untracked (`??`), 89 lines, `covers: U6` at line 4 | `corpus/knowledge/input-debugging-boundaries-r15.md` |
| S007 registry row | `status=queued`, `used-by=—` | `corpus/SOURCES.md:19` |
| S051 registry row | absent (`grep -c S051` → 0) | `corpus/SOURCES.md` |
| Navigation index | no row for the draft note; the count would become 28/29 (exit 1) | `corpus/README.md` knowledge rows (`:39`, `:100` only) |
| Round-15 counter | `.ufo/waves/round-15/measure.py` requires status `mined`, tier A/B, exact used-by path, `covers` in first 15 lines, both S007 and S051 on the source line | `measure.py:57-65,150-185` |
| SCORECARD claim | declares 5/7 → 6/7 = 8.5714 with S007 reuse and S051 new | `SCORECARD.md` (uncommitted +25 lines) |

## Findings (by severity)

### F1 — HIGH: draft note's version boundary is contradicted by the host

`corpus/knowledge/input-debugging-boundaries-r15.md:14-15` says
`pacman -Q libinput wayland` printed `libinput 1.31.3-1`. Re-measured now:

- `pacman -Q libinput wayland` → `libinput 1.32.0-1`, `wayland 1.26.0-1`
- `libinput --version` → `1.32.0`
- `grep` of `/var/log/pacman.log` for libinput/wayland: no lines returned, so
  I cannot date a 1.31.3→1.32.0 change.

The note's central caveat ("not verified behavior of the installed 1.31.3")
is therefore wrong on the current host. Either the note recorded a stale or
wrong value, or the host changed in between; the note must not be admitted
until the value is re-measured and the sentence is rewritten. The S007 page
title is 1.32.0, so the documentation version matches the installed 1.32.0
binary today, which is a stronger statement than the note now makes.

### F2 — HIGH (count-blocking): no mined joins yet

The counter credits U6 only if both `S007` and `S051` are `mined`, tier A/B,
and their `used-by` contains exactly `corpus/knowledge/input-debugging-boundaries-r15.md`.
Today S007 is `queued` with `used-by=—` (`corpus/SOURCES.md:19`) and S051 does
not exist. Until L1 applies those registry edits (logged old→new per the
registry rule), the note is not counted and the score stays 7.1429.

### F3 — MEDIUM (count-blocking): index row missing

`corpus/README.md` has no route to the new note, so the navigation counter
(28/28 → 29 existing notes) would exit 1 with one missing row. Add the index
row in the same committed revision.

### F4 — MEDIUM: S007 anchor is a mutable `latest` URL

The fetched `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`
is titled `Helper tools — libinput 1.32.0 documentation`, which matches S007's
anchor text. A versioned `/doc/1.32.0/tools.html` returned HTTP 404, so the
note correctly declines to substitute it. A web search snippet still listed
`latest` as 1.31.0; that is a stale index, and the fetched page is authoritative
today. Because the URL is mutable, the registry anchor should carry the fetch
date and the sha256 of the bytes fetched (or be superseded by an immutable
revision). Recheck debt, not a count blocker.

### F5 — LOW: S051 shares a local path with S043

S051 cites `/usr/share/wayland/wayland.xml`, the same file as S043 (registry
scope). QUALITY 17 screens canonical URLs, not local paths, so this is not a
collision. The note's claim that S051 is the distinct input-contract scope is
consistent with the XML: `wl_seat` `version="11"` at `:2004`, `wl_pointer`
`version="11"` at `:2138`, `wl_keyboard` `version="11"` at `:2573`.

### F6 — Verified, no defect

- XML digest: `sha256sum /usr/share/wayland/wayland.xml` →
  `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, equal to
  the note's stated value.
- Anchors: `wl_seat` capabilities event `:2030`; `wl_pointer` enter/leave/motion/
  button `:2197/:2212/:2224/:2244`; `wl_keyboard` enter/key `:2614/:2669`. The
  note's ranges `2004–2086`, `2138–2260`, `2614–2699` contain these events.
- Quotes checked against XML: capability "sent on binding ... or whenever a seat
  gains or loses" (`:2030`); keyboard `enter` "seat's keyboard focus is on a certain
  surface" (`:2614`); `key` "platform-specific key code ... interpreted by ... keymap"
  (`:2669`).
- Doc claims checked against the fetched S007 page: list-devices shows "built-in
  defaults, not your desktop's configuration"; `record` captures kernel events
  independent of libinput context; `record` obscures alphanumeric key codes by
  default; `replay` creates a new virtual device; "most" tools need root. These
  are `[INF-docs]` and are labeled so in the note.

## Acceptance conditions (all required)

1. Committed revision `R`: `python3 .ufo/waves/round-15/measure.py R` reports
   U1–U6 covered, 6/7, 8.5714 (delta +1.4286), with S007 and S051 both
   `mined`, tier A/B, and used-by exactly the note path.
2. The note has exactly one `covers: U6` line within its first 15 lines.
3. Version boundary equals the `pacman -Q` value read at commit time (1.32.0 at
   this review); the 1.31.3 sentence is removed or corrected.
4. Required sections present: `## Layer ladder`, `## Safe boundary`,
   `## Unexercised delivery` (last section carries `[UNK]`).
5. Navigation counter 29/29 with the new `corpus/README.md` row; maintained
   source census exit 0 with the existing W04 warnings retained.
6. No executed observer and no raw device data: no `debug-events`/`record`/
   `replay`/`debug-gui`/`evtest`/`WAYLAND_DEBUG` output, no `/dev/input/event*`
   identifiers in the note.
7. SCORECARD reads 8.5714 as sourced-ground coverage of a documented route,
   keeps U7 open, and does not claim input coverage or 10.
8. R14-V1 correction is append-only and is not counted as a coverage move;
   historical receipt bytes are unchanged (`git show <prev>:<path> | sha256sum`
   equals the pre-change value for the prefix).

## Rejection conditions (any one rejects)

- R1: U6 credited while S007 or S051 is `queued`, or their used-by omits the note.
- R2: text that establishes focus, client delivery, text insertion, IME,
  Hyprland processing of libinput events, or hardware health.
- R3: any observer run, raw device read, or sample output from this host used as
  evidence; any `sudo` input tool invocation.
- R4: two `covers:` lines, or `covers: U6` below line 15.
- R5: score claimed as 10, "complete input coverage", or saturation.
- R6: R14-V1 correction rewrites historical bytes, or is counted in C1.
- R7: version sentence left as 1.31.3 against measured 1.32.0.
- R8: a new S051 row using the S007 libinput URL (URL collision with S007).

## Verification gaps and residual risk

- I did not run `measure.py`, the gate, or any counter (forbidden for this seat);
  the F2/F3 conclusions are from reading the registry and index bytes.
- The 1.31.3→1.32.0 discrepancy is unexplained; `/var/log/pacman.log` returned
  no matching lines, so the change date is unknown.
- S007's mutable URL means a later recheck may see different doc text; the
  fetched date and digest are not yet pinned (F4).
- Doc-only coverage cannot show that libinput or Hyprland process any event on
  this host; that remains `[UNK]` by design.

## Tooling

No tools installed or upgraded. Read-only uses: `pacman -Q`, `libinput --version`,
`libinput --help`, `libinput debug-events --help` (static help), `wayland-info`
version probe, `sha256sum` on the installed XML, and one fetch each of the
official libinput `latest` and `1.32.0` tools pages.
