# R56RevC3Contract — report (attack on PRED-C3-r56, calibration)

Base `13f0acbe3a15da2d9c08357a576d91dcadc85273`. Read-only lane access (`git ls-tree`, `git cat-file blob`, `git archive corpus`). No tracked lane file, index, or fleet/sibling repo was touched. No subagents. No host reads or hyprctl calls (C3 is lane-only). No hold-out path was seen or used.

Deliverables (all under `.ufo/waves/round-56/w1/R56RevC3Contract/`):
- `pairs.md`: the 65 missing (S, entry) pairs with base row status and read evidence, the 5 range-hidden pairs, the dangling/extra checks.
- `c3_v.py`: my counter, written from registration §C3 only, with variant switches (`--commonmark`, `--ranges`, `--allsource`, `--dump`). `c3_seat.py` is the first literal-only version. Both give the same base result.
- `classification.json`, `classify.py`: per-pair label and reason (the labels are my judgement from reading each line; they are not mechanical).
- `forge.py`: scratch-copy mutation driver for the evasion tests.
- `dump-base.tsv`, `dump-ranges.tsv`, `missing.tsv`, `missing-lines-full.txt`, `SOURCES-base.md`, `runs.txt` (all decisive outputs).

## 1. Counter at base and baseline comparison

Command: `python3 -I c3_v.py /home/vgpnk/Projects/shokunin/mado-shokunin 13f0acbe3a15da2d9c08357a576d91dcadc85273 <work>`

```
MADO_USED_BY: rev=13f0acbe3a15da2d9c08357a576d91dcadc85273 entries=70 rows=319 missing=65 extra=0 dangling=0 verdict=TARGET_MISSED
```

Same as the frozen baseline `entries=70 rows=319 missing=65 extra=0 dangling=0`. Registry sha256 at base equals `frozen-tables.json` `c3.sources_sha256_at_base`. My counter matches the frozen baseline; no discrepancy at base under the literal reading.

## 2. The 65 pairs, read line by line

Every occurrence was read in full (`missing-lines-full.txt`). Result: **REAL 41, MIS 23, BORD 1**.

**MIS pairs (23): adding the entry to `used-by` would misrepresent the row.** Each entry refutes, disclaims, rejects, supersedes, or names another object / another entry's row / a retired id, and states that the row is not used:

| S | row status | entry | the entry's own statement (base line) |
|---|---|---|---|
| S030 | rejected | hyprland-config-era-r12 | L127,132-134: "Every historical S030 occurrence ... resolves to **S017**, not to an admitted S030" |
| S045 | rejected | hyprland-config-era-r12 | L139: pointer to the rejection record; S045 is itself rejected |
| S061 | rejected | terminal-route-r17 | L152: "S061-S062 (rejected)" |
| S062 | rejected | terminal-route-r17 | L152 same |
| S084 | rejected | walker-route-r18 | L327: "Head source token S084 ... was replaced in place by S098. S084 is now rejected" |
| S094 | rejected | theme-route-r18 | L158-161 the S094 digests "do not reproduce"; L167 "S094 is now rejected", replaced by S097 |
| S007 | queued | input-debugging-boundaries-r15 | L10 "S051 supersedes queued S007's loose ... description" |
| S132 | queued | terminal-trees-r23 | L1 (the `source:` line): "S132 stays queued and supports nothing." S132 is deliberately absent from the source list |
| S005 | mined | output-colour-boundaries-r14 | L65 "Neither the S005 README's earlier commit nor ... is substituted for this file revision" |
| S040 | mined | output-colour-boundaries-r14 | L20 "do not apply S040's ... governance as its authority"; L65 not substituted; L106 "Reject" |
| S043 | mined | input-debugging-boundaries-r15 | L11 "distinct from S043's registry scope" |
| S044 | mined | config-drift-r12 | L160 "round-13 S044 cites the actual gate-maintenance rule" (names the lesson's citation) |
| S056 | mined | xdg-terminal-selection-r47 | L11 "held neighbours ... (rows S056-S060)" (neighbour pointer; this entry uses S059/S060 at L74) |
| S096 | mined | config-health-report-r3 | L1017 "S096 (host walker bytes) now exists and is not cited here" |
| S187 | mined | event-delivery-limits-r26 | L80 correction "package S187 -> S189" (retired id) |
| S188 | mined | event-delivery-limits-r26 | L80 correction "S188 -> S201" (retired id) |
| S214 | mined | event-delivery-limits-r26 | L80 correction "S214 -> S212" (retired id) |
| S357 | mined | hyprland-bind-key-match-r50 | L3 "S357/S358 serve that tool only" (tools/mado-keysym.py) |
| S358 | mined | hyprland-bind-key-match-r50 | L3 same |
| S113 | mined | tripwire-binding-boundaries-r21 | L34 "S119 explicitly supersedes the universal inference in S113's teaches field" (quoted fact "retained", inference refuted) |
| S116 | mined | tripwire-precision-r20 | L146 round-21 correction pointer "(S116–S120)" |
| S119 | mined | tripwire-precision-r20 | L146 "S119 explicitly supersedes S113's ..." (pointer) |
| S120 | mined | tripwire-precision-r20 | L146 range pointer "(S116–S120)" |

Note S113 is the one MIS pair where a quoted fact of the row is retained by the sentence; I counted it MIS because the only mention refutes the row's inference.

**BORD (1):** S046, output-colour-boundaries-r14 L87: "The diagnostic used for S041 did bind/query some interfaces (S046 in the U4 note)". A locator to another note's use of S046 for a claim this entry makes. I did not count it as MIS.

**REAL (41):** log/version citations (`/var/log/pacman.log:2929`, `:3062`, `:3123` for S090 across the walker family), held rows (S318/S319 in bind-key, xkb and dispatcher entries; S352/S353/S359 in dispatcher-r51), locators (S158 `:2107`, S186 `:19`, S277 `:61`), and procedural uses (S015 in walker-route-r18 L236). Full table with line refs in `pairs.md`.

## 3. Findings

### F1 (main): the fix target is unsatisfiable without misrepresenting used-by
`missing=0` requires adding the entry to `used-by` for all 65 pairs. For 23 of them the entry's own text says the row is not cited (rejected, queued, superseded, retired id, or another object). Two rules force the misrepresentation: (a) registration §C3 defines `CITE` as any token, so a refutation is a citation; (b) claims-frozen fixes the target to "used-by edits only (cell 11)". Entry prose edits would remove the mention but fall outside that stated scope. Under the frozen wording, TARGET_MET is reachable only by writing `used-by` entries that the entries themselves disclaim. The honest fix needs either an entry prose change (a scope decision for the operator) or a pre-data re-registration (a new versioned file).

### F2: "citing" is undefined; the counter has no row-status check
§C3 never defines what counts as citing. It counts any token. 6 rejected and 2 queued rows are in the 65. A counter that ignores `status` cannot distinguish "the entry uses this row" from "the entry says this row is rejected". Pinned to the base text: rejected S030/S045/S061/S062/S084/S094 are counted as missing.

### F3: range notation is not expanded (under-count)
Literal tokens only. Human-read ranges hide five pairs: S176 (`S175–S177`), S117/S118 (`S116–S120`), S057/S058 (`S056-S060`). Expanded count: `missing=70`. The frozen 65 is a literal-token artefact. Forger test: a new entry with the sentence "Covered by rows S100–S110" gives `missing=67` literal, `81` expanded: the literal count sees 2 of 11 cited rows.

### F4: unclosed fence silently removes all later citations
§C3 says "``` / ~~~ fences with 0-3 leading spaces" but gives no closing rule and no unclosed-fence rule. Prepending a single "```" line to `arc-synthesis.md` (never closed) takes `missing` from 65 to 62 with `extra=0`, `dangling=0`. The entry becomes unreadable as a fenced block after line 1, so a reviewer would see it, but the counter does not.

### F5: mixed fence characters
A "```" opener followed by "~~~" and then a closing "```": toggle reading (my `c3_seat.py` and the default `c3_v.py`) closes on "~~~" and counts the next line (`missing=66`). CommonMark reading (the `~~~` line is content, the fence closes on "```") gives `missing=65`. The spec does not say which. No base entry has mixed fence characters (checked: `mixed fence chars: []`), so the base count is unaffected.

### F6: `SRC` = any token on a `source:` line within lines 1–15, including prose
`terminal-trees-r23.md` L1 is a `source:` line that contains "S132 stays queued and supports nothing." The counter therefore treats the disclaimer as a provenance token (S132 is one of the 23 MIS pairs). The window is also a hole: `hyprland-dispatcher-dispatch-r51.md` has `source:` lines at L16–19 (outside the window). Appending " S999" to L19: `dangling=0` (window 15); `dangling=1` with `--allsource`. A `**source:**` prefix plus S999: `dangling=0`. Both are literal-rule consequences; the base corpus has no non-registry id there (so the base count is not affected).

### F7: entries are direct children, regular blobs only; used-by regex is substring-based
- Move an entry to a subdirectory (`corpus/knowledge/archive/arc-synthesis.md`), no used-by change: `missing 65 -> 62`, `extra 0`. Fully silent when no `used-by` names the path.
- Replace `walker-deep.md` by a symlink: `missing 62`, `extra 1`. The `extra 1` only appears because S096's used-by names `walker-deep.md` (the symlink is not in ENTRIES).
- `USEDBY` regex `corpus/knowledge/[A-Za-z0-9_.-]+\.md` is unanchored and ignores `corpus/lessons/*.md`, so lesson back-references are invisible to `extra`, which contradicts the CORPUS wording "entries or lessons citing the row".

### F8: unicode and homoglyph S-tokens evade the count
- ZWSP inside "S090" / "S096" in closeout-r11: `missing 65 -> 63`.
- Fullwidth "Ｓ090" / "Ｓ096": `missing 65 -> 63`.
The rule's ASCII-only regex is what allows this. A reader sees the same id.

### F9: `dangling` is blind to any `source:` line that does not start the line at column 0
By the literal rule (`line.startswith("source:")`), a `**source:**` header or an indented `source:` is not SRC. Verified for the bold form (B3 above).

### F10: `rows` regex `S[0-9]{3,}` vs citation `S[0-9]{3}`
The row regex accepts four or more digits; citations accept exactly three. A row S1000 could never be "missing". No such row exists at base (all 319 are S###). Inconsistent as written; no base effect.

### F11: harness control 6 depends on an unstated sort order
§C3 control 6: "the first (S, entry) pair where entry cites S exactly once on a non-fence line" and "while used-by still lists it".
- Sorted by (S, entry): the first candidate is (S002, window-rule-effects-getprop), which IS in used-by. Wrapping its line 3 gives `missing=65 extra=4` → control passes.
- Sorted by (entry, S): the first candidate is (arc-synthesis, S091), which is NOT in used-by. Wrapping line 402 gives `missing=63 extra=0` → the control prints no `extra` and FAILS.
The selection rule does not state the order and does not require the pair to be listed, although the expectation text assumes it is. Under one natural reading the control cannot pass. Note the wrap of a whole line also removes every id on that line (the S002 case removed 4 pairs' citations at once).

### F12: controls 3 and 4 are valid at base
"First entry (sorted)" = `animation-table-r26.md`; "first row (sorted by id) that lists it" = S158, which cites it on lines 7, 81, …; drop-one then gives `missing+1`. Its `source:` is at L3, so appending S999 gives `dangling=1`. Control 5 (`ghost-path` on S001) and 2 (`fill-all`) are trivially valid. Control 1 (base registry) is trivially 65.

## 4. Verification boundary

- Frozen harness `quality/check-r56-controls.py --claim c3` and counter `quality/counters/c3-r56-used-by.py` are absent at base (`receipts/before.txt`). I did not run them. My counter is the only counter run.
- My variants and forger tests are scratch copies of `corpus/` at base (`git archive REV corpus`), one mutation per commit, in `mktemp` dirs under `/fast/scratch/hyaku/mado-r56/R56RevC3Contract`.
- Per-pair labels (REAL/MIS/BORD) are my reading, not a mechanical rule. I give the line for each in `pairs.md`; a second reader could move S046 (BORD) and S113 (MIS, partly "retained") differently.
- I did not check entailment of any claim, only the citation mechanics.
- Host guard: lane accessed read-only. Scratch repos: `git init`, `add`, `commit -c user.name=ctl -c user.email=ctl@ctl`; `rev-parse --show-toplevel` asserted before the commit in `forge.py` and the batch runs. The control-6 wrap run did not repeat the explicit assertion (fresh `mktemp` dir plus `git init` in one call) — disclosed.
- Nothing installed. No pacman, no uv, no npx, no ~/.local/bin writes. No hyprctl.
- Scratch `/fast/scratch/hyaku/mado-r56/R56RevC3Contract` removed at the end after the receipts were copied (see below).

## 5. Verdict for the attack

PRED-C3-r56 as written can reach `missing=0` only by one of two routes: write `used-by` for 23 rows whose entries disclaim them (misrepresentation, F1), or change entry prose outside the frozen "used-by edits only" scope. The counter itself can also be driven to `missing=0` with text edits that do not cite anything (unclosed fence, ZWSP or fullwidth ids, moving or symlinking an entry out of the scanned set), so a green `missing=0` is not evidence that the citations are right. Control 6 is not reproducible under one of its two readings. I do not think the C3 predicate, as frozen, shows calibration; it shows the counter's arithmetic.

## 6. Residual risk / verification gaps

- No entailment check; only citation mechanics.
- Labels are judgement-based (see §4).
- The literal 65 is the frozen baseline; under the range reading the baseline is 70. If the operator decides ranges count, the target moves.
- Mixed-fence and unclosed-fence rules are unstated in §C3; the base corpus does not exercise them, so the base result is unaffected, but the predicate is not robust to them.
