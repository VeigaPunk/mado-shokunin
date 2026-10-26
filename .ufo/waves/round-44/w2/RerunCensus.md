# RerunCensus — w2, round 44 (mado, hyaku run 9) — census, registry counts, index gates

**Verdict: the data commit holds on every point of my assignment.** Census findings are unchanged from the pre-data
receipt (the four new rows add no E/W finding), the registry grew 234 → 238 by exactly the four declared rows with S164's
`used-by` as the only edited cell, and both index gates pass at `e4678921` (61/61 notes indexed; 61 rows, 0 errors).
No OPEN predicate defect and no content error in this axis; nothing here needs re-registration or a correction.

Data commit under test: `e46789213830597348fe96a351ae004d10587385` (base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`).
Lane tree at `290cddea` — `git diff e4678921 290cddea -- . ':(exclude).ufo'` is empty, so `corpus/SOURCES.md`,
`corpus/README.md` and `corpus/knowledge/` carry the data-commit bytes in the working tree as well
(`SOURCES.md` blob `71853a71…` at both revs; `receipts/census-compare.txt`).

## 1. Axes attacked (assignment, then free strengthening moves)

| # | Axis | Result |
|---|---|---|
| A1 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` vs `receipts/census-before.txt` | identical except the receipt's own trailing `exit=0` line; 8 finding lines + `ok`, exit 0 |
| A2 | row count via the mandated `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base/data | 234 → 238 (expected 234 → 238) |
| A3 | `git diff base data -- corpus/SOURCES.md` shape | 2 hunks, numstat `5 1`: four added rows S298-S301, one changed row (S164) whose only differing cell is `used-by` |
| A4 | `quality/check-index.py` and `quality/check-index-rows.py` at the data commit | 60/60 → 61/61 index; rows 60 → 61, errors 0, warns 3 (the same three as base); both exit 0 |
| S1 | census at a *base export* (independent reproduction of the before-receipt) | byte-identical to `receipts/census-before.txt` minus its `exit=0` echo |
| S2 | id-gap parity | absent ids among `1..max` = 63 at base (max 297) and 63 at data (max 301) → pure append, no id retired/reused |
| S3 | new-row cells | all four: tier `A`, status `mined`, `opened 2026-10-26`, `recheck on-release`, `used-by` = the new note; kinds `code/spec/code/code` |
| S4 | URL uniqueness / E04-E12 | each new URL occurs once; no `E`-code at data; all row-shaped lines inside `## Registry` (9-251), S298-S301 at 247-250, `## Paths` starts 252 → no E12 |
| S5 | cited receipt bytes vs row cells | sizes and sha256 of all four `fetch/` receipts equal the row cells and `receipts/fetch-sha256.txt` |
| S6 | landed prose numbers | `SCORECARD.md:2583` (`Sources 234 -> 238 rows …`), `corpus/lessons/round-44.md:24`, `:80`, `corpus/README.md:72` all agree with the measured counts |
| S7 | fleet-wide census (context only; other lanes out of scope) | exit 0; every lane `ok`; mado line identical to the lane-filtered run; no `E`-code fleet-wide |

## 2. Commands and retained evidence (all in this seat dir)

Each line is a command I ran; the receipt is the captured stdout/stderr plus the recorded exit status.

1. `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
   → `census-live.txt` (`daf4086e5643479baa9501daa26de720e17f054640290d4342e5f5f14ca92140`, exit 0), re-run to `census-live-recheck.txt`
   (`858315d225193675535aafa5be0bfd7ee1fad308db763d22e2065021a097bcc3`), `diff -u` against the frozen
   before-receipt in `census-compare.txt`.
2. `bash scripts/sources-census.sh validate --root /fast/scratch/…/root mado`, root = `git archive e4678921` export of
   the lane plus the real `mado|mado-shokunin|…` conf row → `census-data-tree.txt`; the same root in `census` mode →
   `census-data-tree.txt` (238 / A 228 / B 3 / C 7 / mined 219 / queued 10 / rejected 9, exit 0).
3. `git archive 6a1a9052 … | tar -x` into a second scratch root, then `census` and `validate` → `census-base-tree.txt`
   (234 / A 224 / B 3 / C 7 / mined 215 / queued 10 / rejected 9; the same 8 finding lines, exit 0).
4. `bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mado` → `census-counts.txt`.
5. `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` for base, data, tip →
   `counts.txt` (234 / 238 / 238).
6. `git diff base data -- corpus/SOURCES.md` → `sources-diff.txt`; cell-by-cell comparison of the two blobs, hunk and
   numstat counts, id set and id-gap arithmetic → `counts-extra.txt`, `id-gaps.txt`, `registry-lines.txt`.
7. `python3 -I quality/check-index.py --repo . --rev <rev>` at base and data → `gate-check-index.txt`.
8. `python3 -I quality/check-index-rows.py --repo . --rev <rev>` at base and data → `gate-check-index-rows.txt`.
9. `git show <rev>:corpus/SOURCES.md` cell dump for S298-S301 and S164 → `new-row-cells.txt`.
10. size + sha256 of the four cited receipts at the data rev vs the row cells vs `receipts/fetch-sha256.txt` →
    `pin-sizes.txt`.
11. cited-locator spot checks inside the pinned receipts (symbols and computed block ends) → `boundaries.txt`,
    `range-ends.txt`, `readme-row-cells.txt`, `readme-row.txt`, `prose-numbers.txt`, `lesson-crossrefs.txt`,
    `quote-locators.txt`.
12. `bash scripts/sources-census.sh validate|census --root /home/vgpnk/Projects/shokunin` (no lane filter) →
    `census-fleet.txt` (401 lines, exit 0).
13. `python3 -I .ufo/waves/round-44/w2/RerunCensus/verify-quotes.py` → `verify-quotes.txt`
    (`QUOTES: PASS (6 of 6)`, every quoted fragment ≤ 25 words and found on its cited line at the data rev).

## 3. Measured results

**A1 — census.** At the data commit the validate output is the same eight finding lines as the frozen before-receipt
(seven `W04` duplicate-URL warnings on S030, S042, S045, S097, S119, S120, S121, one `W01` on S277) plus `mado ok`,
exit 0. The only byte difference to `receipts/census-before.txt` is that receipt's final literal `exit=0` line, which
is wrapper text, not census output (`census-compare.txt`). The four new rows therefore introduce **no** new E/W finding:
no E03 duplicate id, no E04 duplicate URL+scope, no E11 dangling `used-by`, no E12 row outside `## Registry`.

**A2 — counts.** 234 at base, 238 at data, 238 at the tip. Census counts move exactly on the tier-A/mined axes:
rows 234 → 238, tier.A 224 → 228, status.mined 215 → 219; tier.B 3, tier.C 7, queued 10, rejected 9 unchanged.

**A3 — diff shape.** Two hunks (`@@ -173,7 +173,7 @@`, `@@ -244,6 +244,10 @@`), numstat `5 1`. Added ids: S298, S299,
S300, S301 (each present exactly once at the data rev). Removed ids: none. Changed ids: S164 only, and inside that row
only the 11th cell differs — the `used-by` cell appends `corpus/knowledge/hyprland-gkeep-size-request-r44.md` after
`corpus/knowledge/rule-attribution-r24.md`; cells 1-10 are byte-equal, status stays `mined`, `opened 2026-10-23`.
This is exactly the claim in `corpus/lessons/round-44.md:80` ("one item appended; cells 1-10 …", verified).

**A4 — index gates.**

```
MADO_INDEX: rev=6a1a905… indexed=60/60 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   exit=0
MADO_INDEX: rev=e467892… indexed=61/61 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   exit=0
MADO_INDEX_ROWS: rev=6a1a905… rows=60 errors=0 warns=3                                        exit=0
MADO_INDEX_ROWS: rev=e467892… rows=61 errors=0 warns=3                                        exit=0
```

Note-count parity: `corpus/knowledge/*.md` 60 → 61 and fence rows in `corpus/README.md` 60 → 61 (`counts-extra.txt`),
so the new note is covered by exactly one new index row (`corpus/README.md:72`), whose Sources cell is
`S164, S298, S299, S300, S301` and whose cited ids all resolve. The three `WARN cited-glob-nomatch` lines are the same
three strings at base and data (round-12 evidence globs and a `S###.bin` glob in a round-24 row) — pre-existing, not
touched by this data. The `--rev` mode demonstrably reads the revision: base and data differ 60 vs 61.

**S5 — the rows' own byte claims check out.** For each new row, the cited `fetch/` receipt exists at the data rev and
its size and sha256 equal the row cell: `Hyprland-XDGShell.cpp` 35458 B `d90b534c…`, `xdg-shell.xml` 63846 B
`7ba7f9c8…`, `gdktoplevel-wayland.c` 97548 B `0ee38458…`, `gkeep-ui.py` 14639 B `07a3c4a5…`; `receipts/fetch-sha256.txt`
lists the same four digests. Working-tree copies hash identically.

## 4. Findings

### In-axis: none

No contradiction of A1-A4. Nothing to report as an OPEN predicate defect (the predicates I exercised are the census
script and the two index gates, and they behave as registered); no content error in the texts I checked.

### Out-of-axis informational (LOW; not a predicate defect, no re-registration)

I checked the registry rows' cited locators against the pinned receipts while counting them. Three of the eight cited
ranges stop before the block they name ends. Clause **j** only requires the range to *cover the anchor line*, so these
are precision notes, not predicate holes; the L1 decides whether a cell edit is worth a round.

1. `corpus/SOURCES.md:249` (S300) cites `gdktoplevel-wayland.c:606-700 handle_configure`; the function
   `gdk_wayland_toplevel_handle_configure` opens at `:606` and closes at `:707`, and its own
   `XDG_SHELL_CALL (xdg_surface, ack_configure, …)` sits at `:706` — outside the cited range. A reader who follows the
   row's range to check "does GTK ack the configure?" lands one line short of the ack. Computed end: `:707`
   (`boundaries.txt`, `range-ends.txt`). Minimal cell edit if wanted: `gdktoplevel-wayland.c:606-700` →
   `gdktoplevel-wayland.c:606-707`.
2. `corpus/SOURCES.md:249` (S300) also cites `gdktoplevel-wayland.c:444-545 compute_size`; the function closes at
   `:554` (the `gdk_surface_constrain_size` call is cut mid-statement at `:545`). Minimal edit: `:444-545` → `:444-554`.
3. `corpus/SOURCES.md:248` (S299) cites `xdg-shell.xml:560-590`; the `ack_configure` request closes at `:596`
   (`</request>`), so the range omits the `invalid_serial` sentence at 589-593. Minimal edit: `:560-590` → `:560-596`.
   The same row's `:1144-1172` is exact (the toplevel `configure` event closes at `:1172`), and S298's `:354-358` is
   exact (the function closes at `:358`) while its `:443-462` covers `scheduleStateApplication`, which closes at
   `:461`; S301's `:446-480`, `:449`, `:474-476` and `:80-91` all land on their symbols (`class GkeepApp` at 446,
   `application_id=` at 449, `set_default_size(420, 500)` at 476, `button.ink` at 80).

Reviewed and cleared (no defect): the README index row's Holds cell says `setSize` "calls `scheduleConfigure`" — true
at `Hyprland-XDGShell.cpp:357` (`return m_owner->scheduleConfigure();`), whose body is the cited `:629-643`; it
abbreviates away the intermediate `scheduleStateApplication()` at `:356` (`:443-462`), which is where `sendConfigure`
is actually invoked (`:455`). Literal reading is correct; no edit proposed.

## 5. Pre-existing warnings carried, not introduced

`W01 S277` (tier-C mined with a non-`—` `used-by`) and the seven `W04` duplicate-URL warnings are present in the base
export too and are outside round 44's rows. The fleet-wide run adds no `E`-code for any lane.

## 6. Risks and limits of this report

- `sources-census.sh validate` resolves `E11` against a *filesystem* directory and derives lane rows from
  `shokunin.conf`, so there is no `--rev` mode. My at-data run used a `git archive` export of `e4678921` plus the real
  `mado|mado-shokunin|coverage + operability (desktop and compositor craft)` conf row (extracted, not retyped); the
  exported tree is scratch and is deleted, so the receipt is the citable artifact. The live-tree run against the fleet
  root is independent corroboration and gives the same eight lines.
- I did not verify the *truth* of the four rows' upstream claims (the fetches predate the wave and are C2's pins); I
  verified only that the cited receipt bytes match the cells and that the URLs are registry-unique.
- Warnings never affect exit status by design; a clean exit 0 here is therefore "no E", not "no warnings".
- Host: read-only. No pacman, no compositor write, no `hyprctl` dispatch/reload, no git write. Only `git show`,
  `git diff`, `git archive`, `git ls-tree`, `git cat-file`, `git rev-parse` and the census/gate scripts ran.
- No tools installed (nothing needed: bash + gawk + coreutils + python3 stdlib).

## 7. Scratch

`/fast/scratch/hyaku/mado-r44/RerunCensus/` (two `git archive` exports ≈ the lane tree twice) is removed at the end of
this seat; nothing citable lives there.

## 8. Files this seat wrote

- `.ufo/waves/round-44/w2/RerunCensus.md` (this report)
- `.ufo/waves/round-44/w2/RerunCensus/` — `census-live.txt`, `census-live-recheck.txt`, `census-compare.txt`,
  `census-data-tree.txt`, `census-base-tree.txt`, `census-counts.txt`, `census-fleet.txt`, `counts.txt`,
  `counts-extra.txt`, `sources-diff.txt`, `id-gaps.txt`, `registry-lines.txt`, `new-row-cells.txt`, `pin-sizes.txt`,
  `gate-check-index.txt`, `gate-check-index-rows.txt`, `readme-row.txt`, `readme-row-cells.txt`, `prose-numbers.txt`,
  `lesson-crossrefs.txt`, `quote-locators.txt`, `range-ends.txt`, `boundaries.txt`, `verify-quotes.py`,
  `verify-quotes.txt`
