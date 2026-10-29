# Round 56 — registration v2 (pre-data re-registration; v1 files are untouched)

Written 2026-10-28 by the L1 after wave 1 settled (43 seats, 0 dead) and BEFORE the real C1 entry, the real C3 registry edit,
the real C1/C3 counters, the harness modules and the C2 tool were integrated or scored on real data. Wave-1 seats scored only
synthetic trees and the base revision. It is a NEW versioned file (claims-frozen.md rule: "a falsified predicate is an honest
stop or a pre-data re-registration under a NEW versioned file, never an edit of this one"); the v1 files `claims-frozen.md`,
`registration.md`, `frozen-tables.json` stay byte-identical (freeze commit `3423ae28`, wave commit `2aa347b1`). v2 files:
`claims-frozen-v2.md`, `registration-v2.md` (this file), `frozen-tables-v2.json`, `c3-name-only.tsv`, `ctl/sibling-reader.py`,
`freeze-verify-v2.py`, `receipts/{freeze-verify-v2,witness-v2,c3-base-v2}.txt`. Every counter and harness reads
`frozen-tables-v2.json` (embedded sha256 in `claims-frozen-v2.md`). Where v2 and v1 disagree, v2 wins; everything v2 does not
mention stays as in `registration.md`. Wave 2 attacks v2.

**Disclosure the report repeats.** Read literally, v1 could be passed or broken in ways wave 1 proved, with the seat evidence under
`.ufo/waves/round-56/w1/`: (a) v1 harness control 8 (`edited-quote` → `quote:K05`) was unsatisfiable as written (R56RevC1Contract §3.1:
the leg `quote:<id>` tests the FROZEN quote, which the mutation never touches) — the round-55 class M55-2; (b) the C2 harness
layout put `expected.out` beside the argument paths, so a six-line tool reading `<display-root>/expected.out` scored 18/18 committed
and the revealed hold-out (R56CritHoldout F1, R56CritControls §0.2) — the round-55 class M55-4; (c) the C3 definition of `missing`
was satisfiable by deleting the citing tokens from the entries (R56CritDoNothing C3: `missing=0 extra=0 dangling=0 TARGET_MET`), and
a mechanical fill of `used-by` would record reliance that the entry text refutes for ~21 of the 65 pairs (R56CritCiteDef §0, R56RevC3Contract §2); (d) `receipts/witness.txt`
covered K-row presence, `tok`, `num` and `scope` only for the generator's own anchors, not the H rows, `source_cell`, `prov`,
`index` or `new_rows` (R56RevC1Contract §3.4; the `claims-frozen.md` sentence "every row, tok, num, scope leg" overstated it); (e) the
registration's declared divergence "GLOB_TILDE `~user` forms" is not a divergence (R56RevC2Spec DEF-2, R56ConnClaims row 14). No
predicate sentence of C1 changes; the C2 sentence changes `controls=3/3` to `controls=4/4`; the C3 sentence changes (below).

## Changes (each names the seat evidence under `.ufo/waves/round-56/w1/`)

| id | v1 text | v2 text | evidence |
|---|---|---|---|
| E1 | C1 control 8 `edited-quote` requires `quote:K05` | requires `row:K05`; collateral legs (`source_cell:K05` etc.) are allowed; `quote:<id>` stays the frozen-quote-versus-pin test | R56RevC1Contract §3.1 |
| E2 | `prov`: `source:` among the first 30 lines | the `source:` line, `verified-at` and `recheck` lines must lie within the first 15 lines (C3's `SRC` window) | R56ConnClaims #7 |
| E3 | `scope`: any range containing the line | additionally every `N`/`N-M` locator of that basename is bounded above by the pin's line count `len(blob.split(b"\n"))`; a locator past the end of the pin makes `scope:<id>` fail for every row of that pin | R56RevC1Contract §2 table (7 of 8 cheap anchors ran past EOF) |
| E4 | no echo leg | new leg `echo:<id>` (K and H rows): when the frozen quote has >=30 characters the proposition must not contain the frozen quote as a substring (a quote copied into the proposition says nothing); `content=<e>/33` counts rows whose `tok`, `num` AND `echo` hold | R56CritControls §0.3 (quote-echo reaches 33/33) |
| E5 | C1 controls 10 | 12: control 2 requires any `tok:` leg (the name `content` is not a leg); new control 11 `quote-echo` — every K and H proposition whose frozen quote has >=30 characters becomes `<quote> echoed on this line, no analysis added here` → `echo:` legs; new control 12 `anchor-past-eof` — the anchor cell of S383 becomes `ConfigWatcher.cpp:1-9999` → `scope:` legs of the S383 K rows. Harness line `controls=<k>/12` | R56CritControls §0.3/§0.6, R56RevC1Contract §3.2 |
| E6 | C2 `{FX}` = the fixture directory in the export; tool cwd = export root | the harness STAGES each fixture run: for fixture `<id>` it creates `<work>/run/<id>/` holding ONLY the fixture's `tree/` (symlinks preserved) and runs the tool from a staging cwd `<work>/cwd/` that is empty and is not an ancestor of the export, the stage or any `expected.*`; `{FX}` = the absolute stage path `<work>/run/<id>`; the tool itself is exported to `<work>/tool/` (never beside the fixtures); expected bytes live only in the harness process memory; nothing named `expected.*`, `note.txt` or `args.json` exists under `<work>/run/`, `<work>/cwd/` or `<work>/tool/`; the harness removes `<work>` subtrees it created. Expected outputs are unchanged (the stage path is the display root) | R56CritHoldout F1/F2, R56CritControls §0.2 |
| E7 | C2 controls `controls=3/3` | `controls=4/4`: new stub `ctl/sibling-reader.py` reads `<display-root>/expected.out` and `expected.rc` from the directory named by `--display-root` (printing nothing and exiting 0 when absent); under the staged layout (E6) it must pass 0 of the 26 fixtures. Harness line `controls=<k>/4`; predicate sentence `controls=4/4` | R56CritHoldout F1 (the cheat that works) |
| E8 | C2 declared divergence list (5 items incl. "GLOB_TILDE `~user` forms") | replaced by this list, required verbatim in the tool's docstring: (1) `~` expands from `--home`, Hyprland reads `getenv("HOME")`; (2) `glob` order is bytewise, glibc's is locale collation, and glibc returns `.` and `..` for a `.*` pattern while python's `glob` does not; (3) the depth cap of 16 (Hyprland has none); (4) the canonical watch prints the realpath, Hyprland records the symlink path as the watch's file name (`ConfigWatcher.cpp:70`); (5) duplicate paths print as separate watches, the kernel returns the same watch descriptor for the same inode; `watches=` counts add attempts, a missing path's `inotify_add_watch` result is never checked; (6) the Lua configuration provider and a runtime `hyprctl keyword misc:disable_autoreload` are not modelled; (7) the value grammar and line grammar are the hyprlang 0.6.8 subset of this registration (the round-46 pin `.ufo/waves/round-46/fetch/hyprlang-config.cpp` is byte-identical to tag v0.6.8, R56ScoutHyprlang) | R56RevC2Spec DEF-2/DEF-5, R56ConnClaims #14,#15,#20,#27 |
| E9 | C3 `missing` / `extra` / `dangling` over every token pair | C3-v2 below (frozen NAME-ONLY allowlist; `conflict`, `stale`, `lost`, allowlist hash; 9 controls) | R56CritCiteDef, R56RevC3Contract, R56CritDoNothing C3 |
| E10 | harness holds expectations; run paths unspecified | every harness and counter honours `--work`, creates nothing outside it, and removes what it created before exit (the lane scratch rule); the L1 passes `--work /fast/scratch/hyaku/mado-r56/<name>` | R56RevScratchDiscipline |
| E11 | the F12 fixture note says `UNKNOWN: no record; non-object lines are bad_json` | the note is informational and wrong about the output: F12 expects `SETUP bad_json` (rc 2) because `[1,2]` is not a JSON object; fixture bytes are unchanged | R56RevC2Spec DEF-1 |

## §C3-v2 — registry back-references (calibration), re-registered

**Why the label changed.** The measured quantity is registry back-reference consistency between entry text and `used-by`
cells (token level), reviewed for name-only mentions. It is not a measure of how well the lane calibrates its confidence;
the SCORECARD row carries that wording. The axis stays calibration because the lane's own registry (its statement of what it
relies on) is compared with the repository state.

**Definitions** (at `--rev` unless named; ENTRIES, ROWS, CITE, USEDBY, SRC as in registration.md §C3):
- PAIRS(rev) = {(S, entry) : S is a registry row id at rev, entry in ENTRIES(rev), S in CITE(entry)}.
- `c3-name-only.tsv` (frozen, sha256 `c3.allowlist_sha256` in `frozen-tables-v2.json`; path `.ufo/waves/round-56/c3-name-only.tsv`): 24 tab-separated rows `S###`, entry path, line-sha, reason. They are the pairs that AT LEAST ONE of two independent wave-1 readers judged name-only (R56RevC3Contract `MIS` or R56CritCiteDef `N`/`R`/`M-N`): the entry mentions the id to refute, supersede, redirect, disclaim or name another object, so adding the entry to that row's `used-by` would record reliance the text denies. LINESHA(S, entry, rev) = sha256 over the UTF-8 bytes of the lines of the entry at `rev` that are outside fenced code blocks and contain the token S (token rule of CITE), in file order, each line as in the blob split on `\n` (no stripping), joined by `\n`.
- `missing` = |{(S, entry) in PAIRS(rev) : entry not in USEDBY(S) and (S, entry) not an allowlist row}|.
- `extra` = |{(S, path) : path in USEDBY(S) and (path is not an ENTRIES member or S not in CITE(path))}| (unchanged).
- `dangling` = |{(entry, S) : S in SRC(entry), S not a registry row id}| (unchanged).
- `conflict` = |{allowlist rows (S, entry) with entry in USEDBY(S)}|.
- `stale` = |{allowlist rows whose entry is absent at rev, or whose S is not in CITE(entry), or whose LINESHA(S, entry, rev) differs from the row's line-sha}|.
- `lost` = |{(S, entry) in PAIRS(base) : (S, entry) not in PAIRS(rev)}| where PAIRS(base) is computed from the lane objects at the frozen `base` revision (`frozen-tables-v2.json` `c3.base_rev`; its sorted `S###|path` lines joined by `\n` plus a final `\n` have sha256 `c3.base_pairs_sha256` — the counter fails closed when the objects are absent or the hash differs).
- `allow_sha`: the blob `c3-name-only.tsv` at `--rev` has sha256 `c3.allowlist_sha256` (a miss prints `missed=allow_sha`).
- `exempt` = the number of allowlist rows (frozen: 24).
Output: `MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=<m> extra=<x> dangling=<d> conflict=<c> stale=<s> lost=<l> exempt=<n> verdict=<TARGET_MET|TARGET_MISSED> missed=<legs,comma|none>`; `TARGET_MET` only at `m=x=d=c=s=l=0`, `n=24` and every of `allow_sha`, `tables_sha` ok; exit 0/1/2. Baseline at the base revision (`receipts/c3-base-v2.txt`): `entries=70 rows=319 missing=41 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24`.

**Harness (`--claim c3`) — 9 controls**, one mutation each on a scratch commit of the good tree at `--rev`; the counter must exit 1 with the required leg in `missed`; line `MADO_R56_CONTROLS: claim=c3 good=<ok|bad> controls=<k>/9 verdict=<OK|FAIL>`:
1. `base-registry` — `corpus/SOURCES.md` replaced by its bytes at the frozen base → `missing`.
2. `fill-all` — every row's used-by gets every entry path → `extra`.
3. `drop-one` — remove the first entry (sorted) that is not an allowlist pair for the first row (sorted by id) that lists it, from that row's used-by → `missing`.
4. `dangling-source` — append ` S999` to the `source:` line of the first entry (sorted) that has one → `dangling`.
5. `ghost-path` — add `corpus/knowledge/no-such-entry.md` to the used-by of S001 → `extra`.
6. `fenced-cite` — wrap in a ``` fence the line holding the first non-allowlist, single-occurrence citation (first by sorted (S, entry)) while used-by still lists it → `extra` (and `lost`).
7. `allow-everything` — replace `c3-name-only.tsv` by a file listing every pair of PAIRS(rev) with correct line-shas → `allow_sha`.
8. `delete-citation` — in the first entry (sorted) that has a base pair outside the allowlist, replace one occurrence of its S-token on a citing line by `S---` while used-by is untouched → `lost` (collateral `extra`, `missing` allowed).
9. `stale-allow` — append ` x` to the first line (file order) of the first allowlist row's LINESHA lines → `stale`.

## §C1 and §C2 — restated deltas

C1: legs and grammar of registration.md §C1 plus E2, E3, E4; controls 12 (E1, E5); output line unchanged except the harness count.
Recount of the unchanged rest: 30 K rows, 3 H rows, rows S383-S390.

C2: model, grammar, fixtures and hold-out unchanged; harness per E6; controls 4 (E7); divergence docstring per E8. A tool author must
treat the stage layout (E6) as the only layout in which the tool runs.

## What v2 does not repair (declared limits, carried into the report)

C1: `TARGET_MET` proves quote identity, registry binding, anchor scope and lexical grounding; a forged proposition that shares a
quote identifier, keeps to the quote's numbers and does not echo the quote passes (R56RevC1Contract §2); entailment is the wave-2
sentence-to-pin audit (reported, not counted) and the non-author closure. C2: a tool that fingerprints the tree and replays the
committed table scores 18/18 committed and fails the hold-out only (the hold-out is the guard); a tool that reads the lane's
revealed hold-out by absolute path passes (non-adversarial harness). C3: `CITE` reads literal tokens only (ranges such as
`S175–S177` hide `S176`, five pairs; entries without a `source:` line are invisible to `dangling`, 20 entries); the
allowlist is two readers' judgment, frozen, disclosed and open to the non-author closure; the 41 pairs that remain are filled and were judged
reliance (or leaning reliance) by BOTH readers (R56RevC3Contract `REAL`/`BORD`, R56CritCiteDef `U`/`M-U`); six carry an `M-U` or `BORD` hedge.
