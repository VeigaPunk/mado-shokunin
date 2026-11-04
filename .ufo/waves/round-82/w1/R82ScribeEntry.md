# R82ScribeEntry — round-82 knowledge entry (C1 ground)

Seat: `R82ScribeEntry` (scribe; leaf member, no subagent dispatch).
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round: 82, wave 1. Freeze `780c30fcae12d74ce8ab3b871a0888696c2415d9`; base
`6ea2386d49318a5f223097c78b5fe79c31b064f8`. Lane HEAD observed at close: `89acb06c`
(“round-82 erratum E1”, 2026-11-04 10:34:28 −0300); HEAD advanced during the seat
(`6ea2386d` → … → `b6146ee6` → `3ec7fb75` → `89acb06c`).

Deliverable: `corpus/knowledge/bar-footprint-allocation-r82.md` — 245 lines, 17,370 B,
sha256 `117f1730b32c7fa71c0cf9e41686cb344be84f0d2bd398b90db63f3c1dd01229`, worktree modification
(`git diff --stat`: 203 insertions, 114 deletions against HEAD's committed draft).
Report: this file.

## 1. Behavior — what the entry carries

The entry is prose over committed bytes, in the lane's note shape (front-matter `source:` /
`verified-at:` / `recheck:`, numbered sections, evidence classes, a `## sources` block). Its six
required grounds map as follows.

1. **Zero means the client's number** (§1). `set_size`'s zero clause at `S481:128-131`
   (“If you pass 0 for either value, the compositor will assign it …”, 22 words) is separated from
   the `configure` event's hint/zero clauses at `S481:341-345` and `:347-348` (“… the client
   should decide its own window dimension.”, 18 words). The chain is then followed through
   gtk-layer-shell: `layer_surface_on_size_allocate` copies GTK's allocation (`S464:304-310`),
   sends it back (`S464:312`), and recomputes the zone (`S464:313`); `layer_surface_send_set_size`
   zeroes only the stretched axes (`S464:33-45`). Hyprland's arranged box starts from
   `PSTATE->desiredSize` (`S470:2607`), and a zero request takes the assign/span branches
   (`:2610-2611`, `:2623-2624`, `:2635-2637`, `:2645-2647`) before `box.round()` (`:2660`), so the
   box fed by a zero declaration is the available span, not the client's chosen band. The entry
   also records that `S481` is byte-identical to held `S460` (same sha256, both 407 lines).
2. **gtk's auto zone** (§2). The gate is anchor equality (`S464:269-272`), the two arms read
   `self->current_allocation.height` / `.width` (`:276` / `:282`), the unanchored margins are added
   at `:277-280` / `:283-286`, and the send is guarded at `:289-292`. The entry states explicitly
   that the `-1` sentinel means *no call* (not “sends -1”), and that Hyprland adds the anchored
   margin later (`S470:2575-2581` after the `S470:2531-2533` guard).
3. **The round-82 model** (§3). `--allocation` parses a `{namespace: band}` object
   (`tools/mado-barfoot.py:436-453`); `band_of`'s order is declaration (`:461-462`), allocation
   (`:463`), absent refusal (`:464-467`), zero/negative refusal (`:468-470`). The single-surface
   path resolves through `declared_box` (`:481-482`) and measures the extent from the resolved box
   (`:515-524`, `:1041`); the composition path writes the resolved band into `bar_spec` before the
   order is built (`:802-803`), so `surface_zone` reads the allocation stand-in (`:614-622`,
   called at `:837`), and `apply_exclusive` shrinks the running box (`:718-738`, `:855-866`).
   Unknown namespaces are setup refusals in both paths (`:962-965`, `:769-773`).
4. **Decision table** (§4) — nine rows: the carried no-allocation refusal plus the eight
   `alloc-*` cases, with the class, input, modelled box/band and refusal stage per row.
5. **Limits** (§5) — a declared-not-observed allocation (a real `--layers` capture catches it as
   `box=DIFFER` at `:1025`); per-axis dynamic extra surfaces stay refused and an allocation entry
   for a known extra is accepted but inert (`:769-773`, `:802-803`, `:614-616`/`:624-626`);
   fractional scale refused (`:978-981`, `:763-766`); unknown namespace and negative band setup
   refusals; zero band model refusal; three caller mis-declarations the model does not refuse
   (oversized band, non-band-axis entry, entry shadowed by a positive declaration); S481 is not a
   host observation; the carried case name is historical.
6. **`## sources`** (§sources) names `source: S481` (new; sha256, 407 lines, byte-identical to
   S460), `source: S464` (held; all anchors), `source: S470` (held; all anchors).

## 2. Gates

No gate, counter, tool or selftest was executed by this seat. The entry is prose; the only runs
were read-only `read`/`grep`/`awk`/`sha256sum`/`git show`/`git log`/`git diff` and one Python
anchor checker. Every number in the entry is quoted from the frozen receipt
(`.ufo/waves/round-82/receipts/measurement-c1-r82.txt:82-84`) or from the frozen case file; none
is a re-execution claim.

Mechanical anchor validation (script over the written file): 20/20 checks passed after two
corrections made during drafting — the vector-order line was `:897-898` (not `:846-847`, which is
the `live_box` conversion), and the `set_size` request range was `:122-137` (not `:122-136`, which
omits `</request>`). Checked anchors include `S481:128-129`, `:341`, `:347-348`; `S464:276`,
`:282`, `:312-313`; `S470:2607`, `:2610-2611`, `:2623-2624`, `:2635-2637`, `:2645-2647`, `:2660`,
`:2575`; `tools/mado-barfoot.py:456-471`, `:481-482`, `:802-803`, `:962-965`. Quote lengths are
22, 16 and 18 words.

Hashes re-read this seat: tool `380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59`;
counter `1e9f394df80284e78f1fdf3f24cb5e14d1e4091f4880ccc60a2a45060b54612d`; controls
`e404bb3fa93d5f12338129adc8733574084e6fab2ee12fbb471dd45df94a315f`; `S481.xml`
`87e0b9c837aecd6977f76f3c47d73088b7159871f5d979dc1840f6cadb5e2ed8`; `S460.bin` the same.

## 3. Touched surfaces

- Wrote `corpus/knowledge/bar-footprint-allocation-r82.md` (worktree only; uncommitted).
- Wrote this report.
- Scratch `/fast/scratch/hyaku/mado-r82/R82ScribeEntry` created and removed (`rmdir`); no files
  left. No clone, no `/tmp` write.
- Did not touch: `tools/mado-barfoot.py`, `quality/counters/*`, `.ufo/waves/round-82/controls/*`,
  `.ufo/waves/round-82/receipts/*`, `corpus/SOURCES.md`, `SCORECARD.md`, `corpus/README.md`,
  `corpus/lessons/*`, the claim declaration. No git/jj mutation, commit or push.

## 4. Findings

### F1 — the deliverable path already held a committed draft at seat start

The path is tracked at HEAD: commit `3ec7fb75` (“round-82: the allocation entry, the tray source
rows and the lesson”, 2026-11-04 10:30:07 −0300) landed it at 156 lines / 9,591 B / sha256
`1caf7e4a5e0019ca78f1b43270468ba9d31116aec184e19bcd8356f8ca5a8a6c`; the worktree file at seat
start was that byte-identical draft (`stat` mtime 10:28:43, sha `1caf7e4a…`). I treated it as a
draft and replaced it to meet the seat's anchor requirements; the replacement is the 245-line
version named above. The L1 decides whether to land it over `3ec7fb75` or reject the diff.

The committed draft has these citation/description defects (line numbers are the committed file's;
quoted verbatim):

1. `corpus/knowledge/bar-footprint-allocation-r82.md:26` presents the `configure` event's zero
   clause as the `set_size` ground:
   `> \`If the width or height arguments are zero, it means the client should decide its own window dimension.\` (S481:347-348)`
   after the sentence “A layer surface asks for its size with `set_size(serial, width, height)`.”
   The clause at `S481:347-348` is in `configure`, not `set_size`; the `set_size` zero clause is
   `S481:128-131`, and the request runs `:122-137`.
2. `:34` cites `S470:2622-2630` for the zero-height span: `:2622` is the `both_vert` mask, the zero
   branch is `:2623-2624`, and the fill is `:2645-2647`; `:2630` is the bottom-anchor branch.
3. `:73` says the no-zone classes “send `-1`, and Hyprland then keeps its previous zone”: gtk sets
   a local `-1` sentinel (`S464:273`) and the `>= 0` guard (`S464:289`) skips the request — no
   `set_exclusive_zone` is sent.
4. `:109` and `:131` say “the declaration grammar has no allocation field” / “The `--surfaces`
   grammar has no allocation field”, but the map is global: an entry naming a declared extra
   namespace passes the unknown-name check (`tools/mado-barfoot.py:769-773`) and is then never
   consumed (`band_of` is called only for `bar_spec`, `:802-803`), while the extra's dynamic band
   still refuses (`:614-616`, `:624-626`). “Inert, not an error” is the accurate statement.
5. `:156` is a bare `` `source:` S481, S464, S470, S466. `` line with no anchors; `S466` is never
   cited in the body. The seat asks for a `## sources` block naming S481 (new) and S464/S470
   (held), which the replacement provides.

### F2 — frozen declaration anchor drift (not edited; L1 decides)

`.ufo/waves/round-82/claims-declaration-r82.md:36-37` says:

```
1. **A zero size is the client's own** (`wlr-layer-shell-unstable-v1.xml` `set_size`
   `:116-123`, S481 opened this round): the compositor's desired size is not the band, the
   client's allocation is.
```

In the pinned S481 (`sha256 87e0b9c8…`, 407 lines) `:116-123` is the unmapping description; the
`set_size` request starts at `:122`, the zero clause is `:128-131`, and the request ends at
`:137`. The claim's content is sound; the anchor is wrong.

The committed registry row repeats the conflation: `corpus/SOURCES.md:433` says
“`set_size` `:122-142`, clause at `:347-348`”. `:142` is inside the following `set_anchor`
request (the `set_size` request ends at `:137`), and `:347-348` is the `configure` event's zero
clause, not `set_size`. `corpus/README.md:133` and `:186` repeat the “`set_size` zero … (S481:347-348)”
framing. These are registry/index files I am forbidden to edit; they need the L1's errata route.

### F3 — S481 adds no new bytes

`S481` is a new id/row but byte-identical to the held `S460` pin: both 407 lines,
sha256 `87e0b9c8…` for each (`sha256sum` on
`.ufo/waves/round-79/fetch/S460.bin` and `.ufo/waves/round-82/fetch/S481.xml`; `diff` empty). The
entry states this so a later reader does not treat the new row as a revision change.

### F4 — concurrent lane changes observed

Lane HEAD moved during the seat (`6ea2386d` → … → `b6146ee6` → `3ec7fb75` → `89acb06c`), and `SCORECARD.md` is
modified in the worktree. Neither change was made by this seat; `SCORECARD.md` was not read for
content beyond `git status` line output and was not written.

## 5. Provenance of the numbers in the entry

| Number | Value | Evidence | Class |
|---|---|---|---|
| frozen cases / correct | 47 / 47 | `measurement-c1-r82.txt:84` | evidence-verified (not re-executed) |
| named mutants / killed | 34 / 34 | `measurement-c1-r82.txt:84` | evidence-verified |
| base control | `correct=39/47`, `base_sha256=a129a435…` | `measurement-c1-r82.txt:82` | evidence-verified |
| carried cases | `39/39` | `measurement-c1-r82.txt:83` | evidence-verified |
| tool selftest | `133/133` | `measurement-c1-r82.txt:84` | evidence-verified |
| base mutant kill split | 28 killed, 6 `reason=anchor-absent` | `control-c1-r82-at-base.txt` | evidence-verified |
| tool / counter / controls sha256 | see §2 | `sha256sum` this seat | re-read |
| S481 = S460 | `87e0b9c8…` both | `sha256sum` this seat | re-read |

## 6. Limits

- The counting command was not run; the prose deliverable cites the frozen receipt at
  `780c30fc`. No `TARGET_MET` here is a re-execution claim.
- Decision-table boxes/bands are the frozen cases' `expect` values and the receipt rows, not a
  fresh tool run; the fixtures are constructed (`pid: 4242`), so no row is a host capture.
- The replacement entry is worktree-only. If the runner compares committed bytes, HEAD still
  carries the 156-line `1caf7e4a…` draft.
- The anchor checker validates that a cited line contains the expected token; it does not judge
  whether the sentence is the best evidence for the claim.
- No tool was installed or upgraded; no pacman transaction was attempted.

## 7. Out of scope

C2/tray runbook, the round-82 lesson, the SOURCES/README/SCORECARD errata, the counter or tool
bytes, the judge, and any commit/push. No claim is made about the live host's tray, bar or
compositor state.

STATUS: defect — `corpus/knowledge/bar-footprint-allocation-r82.md:26` (committed `3ec7fb75`)
attributes `S481:347-348` to `set_size` although it is the `configure` event's clause
(`set_size` zero clause `:128-131`); `:34` cites `S470:2622-2630` for a span whose zero branch is
`:2623-2624`/`:2645-2647`; `:73` says the gate “sends -1” though `S464:289` sends nothing; and
`.ufo/waves/round-82/claims-declaration-r82.md:37` plus `corpus/SOURCES.md:433` carry the same
anchor drift (`:116-123` and `:122-142`/`:347-348` respectively). The replacement entry is written
and worktree-complete.
