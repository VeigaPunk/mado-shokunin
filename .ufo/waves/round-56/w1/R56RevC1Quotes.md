# R56RevC1Quotes — seat report (round 56, wave w1)

Scope: independent verification of `c1.k` (K01–K30) and `c1.h` (H01–H03) of `frozen-tables.json`, and of each row's frozen `sid` against `c1.rows`. Deliverable: `.ufo/waves/round-56/w1/R56RevC1Quotes/rows.md`. Receipts in `.ufo/waves/round-56/w1/R56RevC1Quotes/`: `verify_rows.py`, `rows-check.txt`, `validate_props.py`, `upstream-check.txt`.

## What I did

1. Read `claims-frozen.md`, `registration.md`, `frozen-tables.json` (c1 section, both arrays, pin maps). No edits to tracked files; no git mutation (read-only `git show` and `ls-tree` only).
2. Verified `frozen-tables.json` sha256 = `d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af` (matches the contract).
3. Wrote `verify_rows.py` (own code, not `freeze-verify.py`). For each of the 33 rows: pin line byte substring, whole-file occurrence count, lines containing quote, `|`/whitespace/tab/backslash check, sid→pin check against `c1.rows`. Pin sha256 for all 12 pins checked against the frozen values, working tree and the freeze commit blob.
4. Upstream provenance: fetched the seven Hyprland sources at `efb50993780079460b0cbed1363e2166a2de1d9f` and the live man7 inotify page; all byte-identical to the pins (see `upstream-check.txt`).
5. Wrote the maximum bounded proposition for every row (single pin line, not the quote cell alone) with the NOT and FLAG fields in `rows.md`; `validate_props.py` checks length (K ≥40, H ≥20), no `|`, token overlap with the quote, and numeric legs.

## Commands and decisive output

```
$ python3 -I verify_rows.py
tables sha256: d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af
Hyprland-ConfigValues.cpp: wt=ok committed=ok      (all 12 pins: wt=ok committed=ok)
K01 Hyprland-ConfigValues.cpp:492 line_has=True occ=1 lines=1 pipe=False ws=False sid=S384->ok
... (all 30 K rows: line_has=True occ=1 lines=1 sid=<S>->ok)
H01 host-getoption.json:1 line_has=True occ=1 lines=1 pipe=False ws=False sid=host
H02 host-sources.txt:10 line_has=True occ=1 lines=1 pipe=False ws=False sid=host
H03 host-version.json:3 line_has=True occ=1 lines=1 pipe=False ws=False sid=host
K rows: 30 H rows: 3
sid set used by K: ['S383', ..., 'S390'] new_row_ids [same]
rows registry map covers new ids: True
FAILS: none

$ curl -sfL https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099.../<path>  → sha256 equal to pin for all 7 Hyprland files
$ python3 -I validate_props.py
parsed 33 of 33; failing: none
```

Note on the commit check: `git -C <lane> show 3423ae…:<fetch path>` returned the same 12 blobs; `git ls-tree 3423ae… -- corpus/knowledge/hyprland-config-autoreload-r56.md` is empty (entry not yet written, expected).

## Results

- Row verification: 33/33 pass (30/30 K, 3/3 H). Every quote is byte-identical to its pin line, occurs exactly once in its file, carries no `|`, and every K row's sid maps to the pin it cites in `c1.rows` (S383→ConfigWatcher, S384→ConfigValues, S385→PropRefresher, S386→EventLoopManager, S387→legacy ConfigManager, S388→MiscFunctions, S389→HyprCtl, S390→man7).
- Provenance: 8/8 sourced pins match upstream; 4 host captures are checked only against frozen hashes (they are not upstream files).

## Defects and ambiguities found

These are not failures of the frozen bytes; they are cases where a row's quote alone, read as a scribe would read it, gives a wrong or unsupported claim.

1. **K07 — quote truncates a mask.** Quote `fileMask      = IN_CLOSE_WRITE`; pin line 55 is `fileMask = IN_CLOSE_WRITE | IN_DONT_FOLLOW;`. A scribe working from the quote states the file mask as IN_CLOSE_WRITE only.
2. **K08 — quote asserts a false equality.** Quote `directoryMask = fileMask`; pin line 56 is `directoryMask = fileMask | IN_CREATE | IN_DELETE | IN_MOVED_TO | IN_MOVED_FROM;`. The quote alone reads as "directory mask equals file mask", which the full line contradicts. This is the most consequential quote-level hazard in the set.
3. **K24 — quote drops the error test.** Quote is the `glob(...)` call; pin line 1816 is `if (auto r = glob(...); r != 0) {`. The non-zero test is outside the quote.
4. **Counter blind spot (registration `tok` / `num` legs).** `tok` needs only one shared identifier with the quote. A proposition that adds a clause using a quote identifier passes (for K07 an added IN_DONT_FOLLOW shares IN_CLOSE_WRITE; for K08 an "equal to" reading shares fileMask). `num` likewise does not detect added qualitative claims. This is the declared limit of the counter; it is not a counter bug, but it means K07/K08/K24 are the rows where a scribe can pass the counter with a wrong proposition. The wave-2 sentence-to-pin audit must cover them.
5. **Quotes that cannot carry the flag name or the link (weak single-line support).** K29 (IN_CLOSE_WRITE is named on the line before), K30 (IN_DONT_FOLLOW named on the line before), K12 (opener only), K18 and K23 (log strings only, not the reload or skip action), K27 (test whose reload link is not on either line), H03 (a commit hash only; "v0.56.2" and "running build" need lines 2 and 4 of the same file). These rows are admissible as sourced quotes but a scribe must not state the behaviour the surrounding code implies.
6. **H01 quote omits "set": false** that sits on the same host line; H02 quote supports presence in a capture only (file existence and loading are not on the line; the `~` needs `--home`).
7. **K26 boundary.** `currentPath.substr(0, currentPath.find_last_of('/'))` — the line says nothing about slash-less paths (npos behaviour); a proposition must stop at "up to the last '/'".
8. **Row grammar ambiguity (not a failure):** `registration.md` §C1 says the proposition is ">=40 characters (K)"; this is a length check only and does not relate to whether the proposition is supported by the quote.

## Verification gaps and what did not run

- I did not check the proposition against the eventual entry text (the entry is absent at 3423ae; there is nothing to compare).
- Entailment of propositions by quotes is not established by any counter; this seat's MAX lines are my own maximum readings, not evidence that a scribe will write them. They are the cap, not the claim.
- The host captures (H01–H03) were not compared to any live host state; no `hyprctl` command was run for this seat (its scope is the pin rows).
- Upstream provenance was checked on the live man7 page (no commit-pinned copy exists); its match with the pin shows only that the pin equals the page as fetched now.
- No tool was installed. No pacman transaction. No write outside `.ufo/waves/round-56/w1/R56RevC1Quotes/` and this report; scratch `/fast/scratch/hyaku/mado-r56/R56RevC1Quotes/` removed.
- No hold-out path was touched or looked for.
- Subagent dispatch: none (leaf seat).
