# R77ScribeSources — seat report (round 77, wave w1)

Seat: R77ScribeSources (scribe — sources and lesson, draft form). Write dir:
`.ufo/waves/round-77/w1/R77ScribeSources/`; scratch `/fast/scratch/hyaku/mado-r77/R77ScribeSources/`
(deleted at finish). Repo state found: the L1 had already landed the round-77 integration
(`3e35d0a9`, plus `69238991` and the wave-found hardening `0fa69f41`, HEAD at this writing)
while the wave ran; this seat therefore produced its drafts as an independent audit: fetch
and verify every cited byte, re-run both counters, re-run the census, and diff the drafts
against the landed files. No committed lane file was edited.

## Axes

C1 = coverage (the bar-footprint join), C2 = operability (the executable probe runbook). Both
claims verified at their freeze rev and C1 additionally at the hardened tip (below).

## Behavior (what this seat executed)

1. **Fetches** (`fetch/`, record in `fetch/RECORD.md`): S457 `Renderer.cpp`, S458
   `HyprCtl.cpp`, S459 `ReservedArea.cpp` (+ `S459.hpp.bin`), S460 `wlr-layer-shell-
   unstable-v1.xml` — copied byte-identical from the pinned read-only trees (HEADs re-verified:
   Hyprland `efb5099…`, Waybar `90b209ad…`, equal to the registry pins); S461 installed
   `/usr/share/man/man5/waybar.5.gz` (via `man -w waybar`); S462 `bar.cpp` from the pinned
   Waybar tree; S463 `https://wayland.app/protocols/wlr-layer-shell-unstable-v1` fetched
   three times, byte-identical (147036 B, sha256 `6a3f6683…`), equal to the committed wave
   copy. Every local digest re-derived the wave manifest `.ufo/waves/round-77/fetch/sha256-r77.txt`
   (`sha256sum -c` → all OK).
2. **Anchor/quote verification**: every anchor and ≤25-word quote of the seven registry rows
   re-located in the saved bytes (line numbers in `fetch/RECORD.md`; all confirmed — e.g.
   S457 quote at Renderer.cpp:2637, S458 print at HyprCtl.cpp:281-282 and command at :2010,
   S459 quote at ReservedArea.cpp:34, S460 quote at xml :165-166, S461 quote at decompressed
   line 91, S462 quote at bar.cpp:358).
3. **Independent measurements** (`receipts/`): C1 counter at the freeze rev `a83e9bee` —
   contract line identical to the committed pre-wave receipt (`cases=15 correct=15 mutants=5
   killed=5 base_correct=8/15 tool_selftest=18/18 verdict=TARGET_MET`); C2 counter at the
   same rev — `cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12 verdict=TARGET_MET`;
   C1 re-run at the hardened tip `0fa69f41` — target still met with the new tool bytes
   (tool_sha256 `61f34022…`); per-mutant scores 3/15, 14/15, 14/15, 10/15, 14/15 (the
   refusal hardening moved `reserved-wrong-edge` from 4/15 to 10/15 — still killed).
4. **Census** at HEAD `0fa69f41` (`receipts/census-scribe-r77.txt`): exit 0, `ok` for
   `corpus/SOURCES.md`; the only new warning is the documented `W04 S458` (HyprCtl.cpp URL
   shared with S158/S307/S320/S366/S389/S394 at separate scopes).
5. **Drafts produced** (all in this dir): `sources-rows.md` (the 7 eleven-column rows; cell
   for cell equal to the landed registry rows), `index-row.md` (README coverage-map row +
   Frontier bullet), `lesson-round-77.md` (Gate with 6 admits + 1 reject, URL/date/quote per
   row; Mistakes MS-1…MS-3), `log-and-scorecard.md` (LOG entry + SCORECARD round-77 block).

## Findings

- **A. Stale instrument pointer in the landed SCORECARD (D2/M77-3 class, recurring
  in-round).** The landed C1 row says "at `a83e9bee` (its instrument's last change)"; the
  wave-found hardening `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7` modified
  `tools/mado-barfoot.py` (and the entry), so `git log -1 --format=%H --
  tools/mado-barfoot.py` now prints `0fa69f41` and the tool sha256 changed (`409e78a4…` →
  `61f34022…`). This seat's re-measurement at `0fa69f41` (`receipts/measure-c1-scribe-at-0fa69f41.txt`)
  shows the target still met, so the correction is a pointer/re-measure append, not a claim
  change. The repair pack's `quality/check-cited-revisions.py` is the standing check for
  this class.
- **B. Landed lesson's S463 quote is not byte-located.** `corpus/lessons/round-77.md` Gate
  quotes `wlr-layer-shell-unstable-v1 protocol` as the page title; the string does not occur
  in the 147036-byte page (`grep -o` empty; `grep -c 'wlr-layer-shell-unstable-v1'` = 1 in
  an unrelated context). Verbatim candidates: the title element "wlr layer shell protocol |
  Wayland Explorer" (used in this seat's lesson draft) or the h1 "wlr layer shell".
- Minor (no action required): the S459 row cites only `ReservedArea.cpp`; the fetched header
  (`S459.hpp.bin`, sha256 `6222d114…`) is pinned in this dir and uncited, as the registry
  rules allow.

## Mistakes mined for the lesson draft

MS-1 — r76 D-series D7, verified by this seat with read-only git (`2308e12a` adds only the
harm-watch receipt; the census receipts landed at `e160d18e`). MS-2 — this seat's own
parallel-batch race: the S463 fetch ran before `fetch/` existed, the `cd` failed and three
files were written to the fleet root; removed immediately, re-fetched cleanly (evidence: the
job log). MS-3 — this seat's own locator assumption (`/mado-shokunin/SOURCES.md` does not
exist; the registry is `corpus/SOURCES.md`).

## Compliance

Host probes: read-only only — the C2 counter's frozen list (`hyprctl version|configerrors|
monitors|getoption|binds|layers`, `pgrep`, `makoctl mode`, `omarchy theme current`) plus
file reads; no socket, no write verb, no screenshot, no restart. No installs or upgrades (no
tool needed). No git/jj mutation anywhere; read-only `git log/show/rev-parse/status` only.
No writes outside the seat dir and scratch except the three accidental `S463.fetch*` strays
in the fleet root, which this seat deleted (restoring the prior state) and recorded as MS-2.
Cited committed receipts copied into `receipts/`; scratch dir deleted at finish. No message
sent to `agent://all`.

## Out of scope (by design)

No committed lane file was edited; integration, corrections appends and the final
`measurement-final-r77.txt` are the L1's. The drafts are reconciliation-ready: where the
landed bytes are correct they match them; findings A and B are the only deltas.

## Artifact paths

- Report: `.ufo/waves/round-77/w1/R77ScribeSources.md` (this file)
- Drafts: `.ufo/waves/round-77/w1/R77ScribeSources/{sources-rows.md,index-row.md,lesson-round-77.md,log-and-scorecard.md}`
- Fetch record + bytes: `.ufo/waves/round-77/w1/R77ScribeSources/fetch/` (`RECORD.md`, `S457.bin`…`S463.bin`, `S459.hpp.bin`, `S461.txt`)
- Seat receipts: `.ufo/waves/round-77/w1/R77ScribeSources/receipts/` (`measure-c1-scribe-r77.txt`, `measure-c2-scribe-r77.txt`, `measure-c1-scribe-at-0fa69f41.txt`, `census-scribe-r77.txt`, plus copies of the two committed pre-wave receipts and `repair-r77-tool-refusals.txt`)
