# ScrRowsDraft — registry rows S298-S301 + held S164 used-by (round 44, w1)

Seat: `ScrRowsDraft` (scribe, leaf; no subagents, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Freeze read first:
`.ufo/waves/round-44/registration.md` (C2 = the gkeep size-request entry; provisional ids S298-S301
for the four non-held pins).

## Behavior (what this seat produced)

Four new 11-column registry rows for the round-44 C2 pins and the held S164 row with its `used-by`
cell extended, all as a draft block for the L1 integrator — no tracked lane file was edited.

| id | source (kind/tier) | anchored to | used-by |
|---|---|---|---|
| S298 | Hyprland `efb5099` `src/protocols/XDGShell.cpp` (code/A) | `src/protocols/XDGShell.cpp:354-358`, `:443-461`, `:455`, `:601-606`, `:629-638`, `:640-643` @ commit `efb50993780079460b0cbed1363e2166a2de1d9f` | `corpus/knowledge/hyprland-gkeep-size-request-r44.md` |
| S299 | wayland-protocols 1.49 `stable/xdg-shell/xdg-shell.xml` (spec/A) | `:560-596`, `:598-618`, `:1144-1172`, `:1166-1167`, versions at `:409`/`:622` @ 1.49 | same |
| S300 | GTK 4.24.1 `gdk/wayland/gdktoplevel-wayland.c` (code/A) | `:606-616`, `:633-642`, `:644-647`, `:656-660`, `:662-683`, `:382-441` @ gtk 4.24.1 | same |
| S301 | gkeep `133b867` `gkeep/ui.py`, full file, location = the raw GitHub URL (code/A) | `:446`, `:449`, `:472-479`, `:475`, `:476`; `set_size_request(` count 0 in 488 lines @ commit `133b86717a02548aeaff3f1411bf301d936c5308` | same |
| S164 (held) | unchanged cells 1-10 | unchanged anchor | `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/hyprland-gkeep-size-request-r44.md` |

`teaches` discipline: each cell states only what its pinned bytes say — the compositor side stores
and defers (S298), the protocol words the size as a hint (S299), GTK stores the configure and marks
it fixed for maximized/fullscreen/tiled (S300), the client declares one default size and no
`set_size_request` (S301). No cell asserts a rule fired, a box Hyprland wrote, or a reported size;
that assembly is the C2 entry's job (round-43 w2 finding: cells echoing a refuted premise).

## Gates (all run; outputs are in the seat dir)

1. **Pins re-fetched, sha256 compared** — `fetch-recheck.txt`: four `HTTP 200 MATCH pin` lines
   (XDGShell.cpp `d90b534c…` 35458 B; xdg-shell.xml `7ba7f9c8…` 63846 B; gdktoplevel-wayland.c
   `0ee38458…` 97548 B; gkeep-ui.py `07a3c4a5…` 14639 B) against
   `.ufo/waves/round-44/receipts/fetch-sha256.txt`.
2. **Duplicate-URL census (E04)** — `grep -n` for `src/protocols/XDGShell.cpp`,
   `xdg-shell/xdg-shell.xml`, `gdktoplevel-wayland.c` and
   `VeigaPunk/gkeep/133b867…/gkeep/ui.py` in `corpus/SOURCES.md`: no match, four times. The mirror
   validate reports no E04 either.
3. **Held-row byte equality** — `s164-cells.txt`: awk field split of registry line 176 and of the
   drafted S164 line, cells 1-9 concatenated with `\036`, both sha256
   `250884ba859b13956954e48801ff831568f69649dfcde4535c038182a0269afa`, 658 B each,
   `VERDICT BYTE-EQUAL`; cell 11 goes from `corpus/knowledge/rule-attribution-r24.md` to
   `…, corpus/knowledge/hyprland-gkeep-size-request-r44.md`.
4. **Mirror validate** (`scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`),
   with the four new rows inserted **from `rows-block.txt` itself** so the validated bytes are the
   delivered bytes; `roundtrip.txt` reads them back out of the mirror and compares: rows S298-S301
   vs lines 1-4 `MATCH`, S164 vs line 5 `MATCH`.
   - `validate-base.txt` — pristine corpus copy: exit 0, `file ok`, 8 W codes (W04×7, W01×1).
   - `validate-no-entry.txt` — appended rows, entry absent: **exit 1**, exactly five E11 lines
     (S164, S298, S299, S300, S301 → `missing used-by corpus/knowledge/hyprland-gkeep-size-request-r44.md`),
     the same 8 W codes, no other E.
   - `validate-with-entry.txt` — appended rows + a three-line placeholder entry in the *mirror only*:
     **exit 0**, `file ok`, same 8 W codes. So the rows add no census finding; the only E-class
     finding they can produce is the entry the C2 seat has not written yet.
5. **Frozen CORPUS.md census on the mirror** (`census-mirror.txt`): rows 238 (234 + 4),
   malformed (NF!=13) 0, duplicate ids none, enum/tier violations none, status histogram
   `mined=219 queued=10 rejected=9`.
6. **Locator verifier** (`check-anchors.sh` → `check-anchors.out`, exit 0): 40 `file:line` needle
   checks plus one count check (`set_size_request(` = 0), 21 `ECHO` lines printing each cited line
   verbatim, 4 sha256/bytes checks, 4 clause-e containment PASS + 1 SKIP (held row),
   `SUMMARY failures=0` (49 PASS lines).
7. **Red-before** (`check-anchors-red.out`): two mutants of my own rows block — locator `:476`→`:477`
   (in range, so only the needle cross-check can see it) and location `gkeep/ui.py`→`gkeep/main.py`
   — each exits 1 with `SUMMARY failures=1`. The verifier is shown able to fail, and it exits 2 with
   `SETUP FAIL …` when its inputs are unreadable instead of reporting zero failures.
8. **Quote check** (`check-quotes.sh` → `check-quotes.out`): the five quotes used in `rows.md` and
   here are ≤25 words, occur verbatim in `check-anchors.out` next to the file:line they claim
   (`SUMMARY quote-failures=0`) — e.g. `window.set_default_size(420, 500)` at `gkeep-ui.py:476`
   (2 words), `Clients must send an ack_configure in response to this event. See` at
   `xdg-shell.xml:1166` (11 words).
9. **Id space** — read-only `git show`: base `6a1a905` and freeze `e228951` each hold 234 rows, max
   id `S297`, zero rows matching `S298|S299|S300|S301`. Provisional ids are the next unused.

## Touched surfaces

- Written: `.ufo/waves/round-44/w1/ScrRowsDraft/` (`rows-block.txt`, `rows.md`, `check-anchors.sh`,
  `check-anchors.out`, `check-anchors-red.out`, `check-quotes.sh`, `check-quotes.out`,
  `fetch-recheck.txt`, `validate-base.txt`, `validate-no-entry.txt`, `validate-with-entry.txt`,
  `census-mirror.txt`, `roundtrip.txt`, `s164-cells.txt`, `mutants/mut-locator.txt`,
  `mutants/mut-location.txt`) and this report `.ufo/waves/round-44/w1/ScrRowsDraft.md`.
- Read-only: the pins under `.ufo/waves/round-44/fetch/`, `receipts/fetch-sha256.txt`,
  `corpus/SOURCES.md`, `corpus/..` copy target, `/home/vgpnk/Projects/shokunin/CORPUS.md`,
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, `quality/counters/c2-r44-gkeep-size-request.py`,
  `.ufo/waves/round-44/assimilation/id-guard.md`.
- Scratch `/fast/scratch/hyaku/mado-r44/ScrRowsDraft/` (mirror + mutants) — deleted before yielding.
- No installs (nothing needed; no pacman, no host mutation, no compositor call, no `git` write).

## Out of scope (not done here, by assignment)

- Scoring `PRED-C2-r44` (needs the committed entry at a rev) and writing
  `corpus/knowledge/hyprland-gkeep-size-request-r44.md` — the C2 seat.
- The `corpus/lessons/round-44.md` § Gate `GATE <id>` lines, the `corpus/README.md` index row, and
  applying the rows to the lane registry — the L1 integrator.
- Final id assignment at the data commit (S298-S301 are provisional; renumbering by document must
  keep each row's receipt name and pinned sha256, or clause e/d of the counter breaks).
- Round-43 closure defects D1-D7 — other seats.

## Findings

1. **The rows are census-clean; the only E-class finding they can raise is the missing entry**
   (`validate-no-entry.txt`: five E11 lines, the same 8 pre-existing W codes as the pristine copy).
   Reported as the expected state, not as a defect of the rows.
2. **A bare `cp -a corpus` mirror cannot be validated**: base rows cite `tools/`, `SKILL.md`,
   `.ufo/`, `quality/`, so a corpus-only copy yields 12 spurious E11 lines
   (S096×2, S173, S174, S178-S182, S184, S185×2) on top of my five. Fixed in the mirror by
   symlinking those four lane-root paths; recorded because a w2 seat repeating this needs the links,
   not a code change.
3. **Cross-check for the C2 seat (not scored by me)**: the two clause-h census lines the entry must
   carry recompute from the pins as stated in the registration —
   `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep`
   (`gkeep-ui.py:476`, `:449`, `set_size_request(` count 0) and
   `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` (Window.cpp `sendWindowSize` body
   `:1732-1754`, first line exactly `}` at 1754; `->setSize(` once at `:1753`, `->configure(` once
   at `:1751`).
4. **Receipt-name containment holds for all four rows** (clause e): `xdgshell.cpp` ⊂
   `hyprland-xdgshell.cpp`; `xdg-shell.xml` = `xdg-shell.xml`; `gdktoplevel-wayland.c` =
   `gdktoplevel-wayland.c`; `ui.py` ⊂ `gkeep-ui.py`. S301 deliberately uses the full-file receipt
   `fetch/gkeep-ui.py`, not S297's `gkeep-ui-excerpt.py`, so no two ids share a receipt path
   (clause d).
5. **S164's base anchor carries no receipt path** (it predates the receipt convention), so the
   clause-e containment check is skipped for it explicitly (`SKIP S164` in `check-anchors.out`);
   clause e applies to new ids only.
6. **Process note, disclosed**: one patch of my own scratch verifier (`check-anchors.sh`, seat dir,
   never a product file) was applied through a python heredoc instead of the edit tool; every later
   change to it used the edit tool. No product or frozen file was touched that way.
7. **Self-inflicted vacuity, caught and closed**: `check-anchors.sh` first put its `mktemp` files
   under `/fast/scratch/hyaku/mado-r44/ScrRowsDraft/` and counted failures through them. After that
   dir was deleted the script still printed 16 `FAIL … no semantic needle check` lines while
   reporting `SUMMARY failures=0` (the appends went nowhere, so the counter never saw them). Fixed by
   rewriting the loops with process substitution so failures count in the main shell, keeping the one
   temp file in the seat dir, and exiting 2 on any setup failure; the red-before runs and the
   `SETUP FAIL rows block unreadable: /nonexistent` probe (exit 2) are the controls.

## Provenance and limits

- Access date for all four rows: 2026-10-26 (the re-fetch timestamp is in `fetch-recheck.txt`).
- Workspace: `/fast/scratch/hyaku/mado-r44/ScrRowsDraft/` — mirror and mutant rows deleted after
  the receipts were copied; only seat-dir files are cited.
- Declared residuals: the six `teaches` cells are a non-author reading of true locators (the
  counter cannot check that a sentence is supported); range-end locators are existence-checked
  only; the mirror's exit 0 depends on a placeholder entry that exists only in scratch.
- No tool installed, no version pinned beyond the host's `bash`/`gawk`/`coreutils` and Python 3 used
  by the census script.

## Artifact paths

- `.ufo/waves/round-44/w1/ScrRowsDraft/rows-block.txt` — the five table lines for the integrator.
- `.ufo/waves/round-44/w1/ScrRowsDraft/rows.md` — cell-by-cell rationale and handoff constraints.
- `.ufo/waves/round-44/w1/ScrRowsDraft/check-anchors.sh`, `check-anchors.out`,
  `check-anchors-red.out`, `check-quotes.sh`, `check-quotes.out`, `fetch-recheck.txt`,
  `validate-base.txt`, `validate-no-entry.txt`, `validate-with-entry.txt`, `census-mirror.txt`,
  `roundtrip.txt`, `s164-cells.txt`, `mutants/mut-locator.txt`, `mutants/mut-location.txt`.
