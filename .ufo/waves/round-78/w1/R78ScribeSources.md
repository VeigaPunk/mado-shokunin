# R78ScribeSources — seat report (round 78, wave w1)

Seat: R78ScribeSources (scribe — sources/registry bookkeeping, draft form). Write dir
`.ufo/waves/round-78/w1/R78ScribeSources/`; scratch `/fast/scratch/hyaku/mado-r78/R78ScribeSources/`
(created, used, deleted at finish). Repo state found: the wave was live and the L1 was committing
while this seat ran (`93a10a13` → `90fc8d84` → `e117a113` → `d27c5ff4` during the seat), so every
measurement below is pinned to a revision **and** to the blob it read. No committed lane file was
edited; no git/jj write verb was run.

## Axes

- **A1 — registry integrity.** Row shape, id uniqueness, enum vocabulary, `used-by` path
  existence, and whether the round's fetched bytes are pinned by a manifest that the entry's
  own Evidence sentence names.
- **A2 — Gate completeness.** For each source re-opened this round: URL, access date
  2026-11-04, a located ≤25-word quote, and an explicit statement of what the row licenses and
  what it does not.

Both are bookkeeping axes; this seat claims no capability axis and ran no counter.

## Behavior (what this seat executed)

1. **Read the contract locations.** The seat brief says "the census commands from CORPUS.md".
   The lane has no `corpus/CORPUS.md` (`find mado-shokunin -name CORPUS.md` → empty); the
   canonical block is the fleet root `CORPUS.md:131-158` (§ Census, `## SOURCES.md — where a
   shokunin learns`). The six commands there are the six run in § C below, verbatim.
2. **Fetch pin verification.** At 06:32 `sha256sum -c sha256-r78.txt` in
   `.ufo/waves/round-78/fetch/` prints seven `OK` and exits 0. At 06:30 the same manifest held
   six lines (see F1). `cmp` against `.ufo/waves/round-77/fetch/` prints identical for all seven
   artifacts (S457, S458, S459, S460, S461.txt, S462, S464).
3. **Quote location.** Eleven candidate fragments were searched byte-exactly in the round-78
   fetch bytes; each hit is reported with byte offset, line number(s) and whitespace-token count
   (`receipts/quote-verify-r78.txt`, `receipts/quote-tokens-r78.txt`). No fragment exceeds 25
   tokens; the two-fragment cells total 24 (S457) and 6 (S464).
4. **Registry delta.** Parsed `git show 93a10a13^:corpus/SOURCES.md` and
   `git show 93a10a13:corpus/SOURCES.md` as pipe tables keyed by id: 401 rows before, 401 after,
   no id added or removed, exactly eight rows differ and in each the only differing field is
   index 10 (`used-by`). `corpus/SOURCES.md` blob `33c02802ced9…` is unchanged from `93a10a13`
   through `d27c5ff4`, so the delta still describes the tip.
5. **Census** at that blob (`receipts/census-r78.txt`): six CORPUS.md commands plus the
   maintained CLI `census` and `validate`; every command exits 0.
6. **Drafts produced** (this dir): `lesson-gate-r78.md` (the `## Gate` section, ready to paste),
   `registry-inplace-r78.md` (old→new pairs), and the two receipts named above plus
   `receipts/census-r78.txt`.

## A. Gate draft (round-78 lesson `## Gate`)

Seven held rows were re-opened 2026-11-04 before the round's entry was written — no new row, no
reused id: the registry stays at **401 rows** (S001–S464; A 386 + B 7 + C 8). The round's bytes
are re-pinned under `.ufo/waves/round-78/fetch/`; `sha256sum -c sha256-r78.txt` prints seven
`OK`, and `cmp` against the round-77 copies prints identical for all seven fetched artifacts
including `S461.txt` (`d59c4651…`). Census at `corpus/SOURCES.md` blob `33c02802` (unchanged
from `93a10a13` to `d27c5ff4`): exit 0, 0 malformed rows, 0 duplicate ids, 0 enum violations,
0 missing `used-by` paths; the only output is the standing W04/W01 warning set (48 W04, 1 W01).

Quote cells carry one or two **verbatim** source fragments, each with its own line locator; a
fragment is never reflowed or stitched across a line break. Line numbers are in the round-78
fetch bytes.

| row | URL | locator | accessed | status | quote (≤25 words, located) | what it licenses / does not license |
|---|---|---|---|---|---|---|
| S457 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp | `Renderer.cpp` @ efb5099, `applyExclusive :2529-2585`, `arrangeLayerArray :2587-2670`, `arrangeLayersForMonitor :2673-2700` | 2026-11-04 | mined (unchanged) | `*edges[i].positive_axis += exclusive + edges[i].margin;` (:2577, 5 tokens) | Licenses the **compositor-side contributor**: the edge selected at :2575 by `exclusiveEdge` or by the singular/triplet anchor receives `exclusive + edges[i].margin`, and the loop `break`s (:2581) so exactly one margin is added; the guard also requires a positive sum. It does **not** license the client-side zone (S464), which margin an ambiguous multi-anchor surface should use, or that the guard's positivity test is a margin refusal — the tool's refusal of a negative margin is the tool's rule, not this function's. |
| S458 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | `HyprCtl.cpp` @ efb5099, `layersRequest :647-700`, reserved template `:253`, print `:281-282`, command `:2010` | 2026-11-04 | mined (unchanged) | `sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top())` (:281, 2 tokens) | Licenses the reply shape and the reserved print order — left, top, right, bottom (:281-282) — which the join parses. It does **not** say which surface set the zone, and it does **not** license a unit conversion: the round-78 tool refuses a monitor whose `scale` is not 1 or whose `transform` is not 0. |
| S459 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/reserved/ReservedArea.cpp | `ReservedArea.cpp` @ efb5099, parent/child constructor `:19-35`, `apply`/`applyip` `:53-60` | 2026-11-04 | mined (unchanged) | `m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());` (:34, 9 tokens) | Licenses the parent/child reserved band the reply's four integers carry. It does **not** license a per-consumer attribution (which namespace produced the band). |
| S460 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/protocols/wlr-layer-shell-unstable-v1.xml | protocol XML @ efb5099, enum `layer :86-90`, request `set_exclusive_zone :152-190` | 2026-11-04 | mined (unchanged) | `The exclusive zone includes the margin.` (:196, 6 tokens) | Licenses the layer levels and the exclusive-zone contract: the client submits a zone that already includes its margin. It is a **contract, not host behaviour** — it does not say how Hyprland composes the band (S457). |
| S461 | host file `/usr/share/man/man5/waybar.5.gz` (`man -w waybar`) | installed `waybar(5)` 0.15.0, `BAR CONFIGURATION` (:38), quote at decompressed line 91 | 2026-11-04 | mined (unchanged) | `Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&` (:91, 8 tokens) | Licenses the declared placement keys and defaults (`position`, `layer`, `height`, `width`, `margin`, `margin-<side>`, `exclusive`). It does **not** license what gtk-layer-shell or the compositor does with them. |
| S462 | https://raw.githubusercontent.com/Alexays/Waybar/90b209add8937514d0a987aa842e701bd8f1232e/src/bar.cpp | `bar.cpp` @ 90b209ad, margin precedence `:178-222`, namespace `:232-233`, size request `:240`, `setMode` `:355-361` | 2026-11-04 | mined (unchanged) | `gtk_layer_auto_exclusive_zone_enable(gtk_window);` (:358, 1 token) | Licenses that exclusive mode reaches the auto-zone API (guarded by `if (mode.exclusive)` at :357) while the non-exclusive branch sets the zone to 0 (:360), so S464's arithmetic is what the host actually submits, and that the margins it sums come from the precedence chain at `:178-222`. It does **not** license the zone arithmetic itself or any band value. |
| S464 | https://raw.githubusercontent.com/wmww/gtk-layer-shell/v0.10.1/src/layer-surface.c | `layer-surface.c` @ v0.10.1, `layer_surface_update_auto_exclusive_zone :264-292` | 2026-11-04 | mined (unchanged) | `new_exclusive_zone = self->current_allocation.height;` (:276, 3 tokens) + `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` (:280, 3 tokens; 6 total) | Licenses the **client-side contributor**: the auto zone starts at the allocation on the band axis (:276 horizontal, :282 vertical) and adds the margin of each *unanchored* edge of that axis (guards :277 and :279; transposed twins :283 and :285), then submits it via `zwlr_layer_surface_v1_set_exclusive_zone` (:289-291). It does **not** license the compositor side (S457) and does **not** license the cross-axis margins. |

Not re-opened, unchanged: **S463** stays `rejected` at tier C — it renders the protocol without
a revision pin, so the pinned XML (S460) remains the authoritative copy. Its `used-by` gains the
round-78 entry, which cites the rejection at `corpus/knowledge/bar-footprint-margins-r78.md:154`.

**Together.** S464 gives `allocation + margin(unanchored edges of the band axis)`, S457 adds
`exclusive + margin(anchored edge)`, and S462 establishes that the host's own bar submits the
first and that Waybar's margin chain feeds both. The composition is a **derivation from the two
source rules**, not a reading of a reserved-area value: S458/S459 report the result, and the
round's cases are fixtures. Nothing here licenses a static `monitor … addreserved` band, a
scaled or transformed output, a dynamic cross size, centring rounding, a negative margin, or
which process set a zone.

## B. Registry in-place changes (old → new)

Method: parse `93a10a13^` and `93a10a13` (`git show`), key by id. **401 rows before, 401 after,
no id churn, eight rows differ, only field index 10 (`used-by`) differs.** No `status` change is
due or made; `mined=378 queued=10 rejected=13` before and after.

| id | field | old | new | basis in the entry (current lines) |
|---|---|---|---|---|
| S457 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:3` (`source:`), `:12` |
| S458 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:3`, `:128` |
| S459 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:3`, `:154` |
| S460 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:3`, `:154` |
| S461 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:3`, `:139` |
| S462 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:3`, `:154` |
| S463 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:154` (`S463 stays rejected`) |
| S464 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `:3`, `:12` |

Notes: (a) the seat brief named three rows (S457/S462/S464); the landed change is eight, and all
eight are supported by the entry's `source:` line or its `Sources`/Evidence paragraphs, so no
addition is uncited. (b) Line numbers are pinned to the entry at worktree sha256 `15f30972…`
(155 lines, HEAD `d27c5ff4`); it was rewritten from the 118-line `93a10a13` version during the
wave, so the S-id + section name is the durable reference. (c) The `used-by` addition order is
`r77 entry, r78 entry` with no space after the comma, matching existing multi-path cells.

## C. Census at the tip (verbatim, with exit codes)

Pinned: `corpus/SOURCES.md` blob `33c02802ced927ca71a4f00a94dd5b4378ec20e0` (HEAD `d27c5ff4` at
the last check; the blob is unchanged from `93a10a13`). Full log: `receipts/census-r78.txt`.

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
401
exit=0

$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
exit=0

$ awk -F'|' '... tier histogram ...' corpus/SOURCES.md
A=386 B=7 C=8 
exit=0

$ awk -F'|' '... status histogram ...' corpus/SOURCES.md
mined=378 queued=10 rejected=13 
exit=0

$ awk -F'|' '... ids ...' corpus/SOURCES.md | sort | uniq -d
(no output)
exit=0

$ awk -F'|' '... enum violations ...' corpus/SOURCES.md
(no output)
exit=0

$ awk -F'|' '... mined used-by paths ...' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
exit=0
```

Maintained CLI (outside frozen v1, same file):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file corpus/SOURCES.md
file	rows	401
file	tier.A	386
file	tier.B	7
file	tier.C	8
file	status.mined	378
file	status.queued	10
file	status.rejected	13
FLEET	rows	401
FLEET	tier.invalid	0
FLEET	status.invalid	0
FLEET	missing	0
exit=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
50 lines: 48 × W04 duplicate-url, 1 × W01 (S277 tierC mined), 1 × ok
(file	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md)
exit=0
```

The W04/W01 set is byte-for-byte the pre-existing set in
`.ufo/waves/round-78/receipts/census-start-r78.txt` and `census-end-r78.txt`; the round adds no
warning (the eight edited rows change only `used-by`, which no W-code reads).

## Findings

- **F1 (resolved in-flight; provenance lag).** At **06:30** the round manifest
  `.ufo/waves/round-78/fetch/sha256-r78.txt` had **6** lines — S457, S458, S459, S460, S462,
  S464 — while `corpus/knowledge/bar-footprint-margins-r78.md:108-109` (then HEAD `e117a113`)
  claimed "`S457.bin`–`S464.bin` and `S461.txt`, sha256 in `sha256-r78.txt`". `S461.txt` was not
  pinned by the round manifest at that moment (`wc -l` → 6; the r77 manifest pins only the gz,
  `S461.bin` sha256 `3972caaf…`). At **06:32** the manifest held **7** lines including
  `d59c46512ee42590a6213173cf528eabd47371c5d2409198386fee31d283ddee  S461.txt`, is committed at
  `d27c5ff4`, and `sha256sum -c` prints seven `OK` (rc 0); the entry's sentence is true as of
  that tip. Class: an artifact sentence that names a manifest, written before the manifest was
  repaired. Standing check: run `sha256sum -c` on the manifest after any edit to an entry's
  Evidence list; a six-line manifest verifies silently (`sha256sum -c` never complains about a
  file it was not given).
- **F2 (open, outside this seat's brief).** `.ufo/waves/round-78/fetch/` now also holds **13
  untracked artifacts** named `S465-DesktopTypes.hpp`, `S466-math.hpp`, `S467-CMakeLists.txt`,
  `S468-Box.hpp`, `S469-Box.cpp`, `S470-Vector2D.cpp`, `S471-factory.cpp`, `S472-main.cpp`,
  `S473-client.cpp`, `S474-config.cpp`, `S475-bar.hpp`, `S476-layersurface.cpp`,
  `S477-proto.cpp`. None is in `sha256-r78.txt` and **no registry row exists above S464** (census:
  401 rows, max id S464), so `S465`+ are file names, not source ids. If any of them is promoted
  to a row, it needs its own Gate entry (URL, 2026-11-04, located ≤25-word quote); this seat did
  not open or adjudicate them. Observed at 06:34 by
  `git status --porcelain .ufo/waves/round-78/fetch/` (13 `??` lines).
- **F3 (observation; wording).** The entry says "fresh pinned fetches"
  (`corpus/knowledge/bar-footprint-margins-r78.md:3`). The evidence this seat can produce is
  **byte identity**, not a re-download: `cmp` prints identical for all seven artifacts against
  `.ufo/waves/round-77/fetch/`. No action claimed; the sentence is defensible if "fresh" means
  re-pinned this round.
- **F4 (observation; no committed byte wrong).** The round-77 seat draft's arithmetic
  ("Registry arithmetic: 393 → 400 rows",
  `.ufo/waves/round-77/w1/R77ScribeSources/lesson-round-77.md:84`) disagrees with the registry by
  one: `grep -cE` counts **401** rows at `f597eccb`, at `93a10a13^`, at `93a10a13` and at
  `d27c5ff4`. The landed `corpus/lessons/round-77.md` does not carry that sentence, so nothing
  committed is wrong; the round-78 Gate therefore states 401.

## Not claimed / out of scope

- This seat did not run the C1 or C2 counters, and reports no measurement of either claim.
- No live host probe of any kind was made: reads only (files, `sha256sum`, `awk`/`grep`, and
  read-only git `show`/`rev-parse`/`log`/`status`).
- The Gate draft is prose for the L1 to integrate into `corpus/lessons/round-78.md`; it is not a
  landed lesson and carries no verdict.
- No install, upgrade, or package transaction; no service action.

## Compliance

- Writes: only `.ufo/waves/round-78/w1/R78ScribeSources/**` and
  `.ufo/waves/round-78/w1/R78ScribeSources.md`. No edit to any committed lane file (tools,
  quality, corpus, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `README`, `SOURCES.md`, `PROVINCE.md`,
  the declaration, the control sets).
- No git/jj write verb anywhere; no fixture repo created.
- Scratch `/fast/scratch/hyaku/mado-r78/R78ScribeSources/` used for all intermediates; every
  receipt cited here was copied into `receipts/` and the scratch dir was removed at finish.
- No tool was installed or upgraded; nothing to record under the operator's tooling rule.

Report: .ufo/waves/round-78/w1/R78ScribeSources.md
