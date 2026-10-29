# R56RevC3Contract — PRED-C3-r56 attack: the 65 missing (S, entry) pairs at base

Seat: R56RevC3Contract (leaf reviewer, no subagents). Base: `13f0acbe3a15da2d9c08357a576d91dcadc85273` (lane `/home/vgpnk/Projects/shokunin/mado-shokunin`), read only through `git ls-tree` / `git cat-file blob` / `git archive corpus` (no lane mutation).

## Counter (own, written from registration.md §C3 only)

`/fast/scratch/hyaku/mado-r56/R56RevC3Contract/c3_v.py` (copied to the seat directory as `c3_v.py`). Literal reading, no flags:

```
MADO_USED_BY: rev=13f0acbe3a15da2d9c08357a576d91dcadc85273 entries=70 rows=319 missing=65 extra=0 dangling=0 flags=[]
```

Matches the frozen baseline `entries=70 rows=319 missing=65 extra=0 dangling=0`. The registry sha256 at base equals `frozen-tables.json` `c3.sources_sha256_at_base` (`422f35f8…e122`). The 65 pairs are in `missing.tsv` (copied as `dump-base.tsv`).

## Classification rule

Each pair was checked by reading the base line(s) on which the id occurs (`missing-full.txt`, every occurrence, not truncated). Labels:

- **REAL** — the entry attributes a claim, value, locator or held-row read to the row's source (a citation in the sense of the rule).
- **MIS** — every occurrence of the id in that entry refutes, disclaims, rejects, supersedes, or names another object / another entry's row / a retired id. Adding the entry to `used-by` would state the row is used by this entry when the entry says it is not. These are the pairs where the frozen fix misrepresents the row.
- **BORD** — borderline, reason given.

Result over the 65 pairs: **REAL 41, MIS 23, BORD 1**. Of the 23 MIS pairs, 6 are on rejected rows (S030, S045, S061, S062, S084, S094), 2 on queued rows (S007, S132), 15 on mined rows.

## The 65 pairs

Sorted: MIS first, then BORD, then REAL. `label` as above; `row status` is the registry status cell at base; evidence cites base line numbers of the entry.

| # | label | S | row status (base) | entry (corpus/knowledge/) | evidence (base line; read) |
|---|---|---|---|---|---|
| 1 | MIS | S005 | mined | output-colour-boundaries-r14.md | L65: 'Neither the S005 README's earlier commit nor the later S040 governance commit is substituted for this file revision' = disclaims |
| 2 | MIS | S007 | queued | input-debugging-boundaries-r15.md | L10: 'S051 supersedes queued S007's loose composite tools description' = superseded, queued row |
| 3 | MIS | S030 | rejected | hyprland-config-era-r12.md | rejected row. L127,L132-134: 'Every historical S030 occurrence ... resolves to S017, not to an admitted S030'; L139 'the original S030 stays rejected'. Source header and L59/67/103/116/120 are re-attributed to S017 by the entry |
| 4 | MIS | S040 | mined | output-colour-boundaries-r14.md | L20: 'do not apply S040's wayland-protocols governance as its authority'; L65 'not substituted'; L106 'S040 governance makes wlr-output-management stable. Reject' |
| 5 | MIS | S043 | mined | input-debugging-boundaries-r15.md | L11: 'S052 adds the core input contract, distinct from S043's registry scope' = disclaims S043 |
| 6 | MIS | S044 | mined | config-drift-r12.md | L160: 'round-13 S044 cites the actual gate-maintenance rule' = names another entry/lesson's citation; this entry does not rely on S044 (S044 used-by corpus/lessons/round-13.md) |
| 7 | MIS | S045 | rejected | hyprland-config-era-r12.md | L139: 'by superseding registry row S045' = pointer to the duplicate-rejection record; S045 itself is rejected |
| 8 | MIS | S056 | mined | xdg-terminal-selection-r47.md | L11 'held neighbours: the documentary route in terminal-route-r17.md (rows S056-S060)' = neighbour pointer; no S056 use in this entry's text |
| 9 | MIS | S061 | rejected | terminal-route-r17.md | L152 'Source rows: S056-S060 (mined) and S061-S062 (rejected)' = status list; S061 rejected |
| 10 | MIS | S062 | rejected | terminal-route-r17.md | L152 same list; S062 rejected |
| 11 | MIS | S084 | rejected | walker-route-r18.md | L327: 'Head source: token S084 ... was replaced in place by S098. S084 is now rejected' |
| 12 | MIS | S094 | rejected | theme-route-r18.md | L158-161: S094 tree digests 'do not reproduce'; L162 names S094 scope; L167 'S094 is now rejected' and replaced by S097 |
| 13 | MIS | S096 | mined | config-health-report-r3.md | L1017: 'S096 (host walker bytes) now exists and is not cited here' = explicit disclaimer |
| 14 | MIS | S113 | mined | tripwire-binding-boundaries-r21.md | L34: 'S119 explicitly supersedes the universal inference in S113's teaches field'; quoted fact 'retained' but inference refuted (borderline on the retained quote) |
| 15 | MIS | S116 | mined | tripwire-precision-r20.md | L146 round-21 correction pointer '(S116-S120)' to tripwire-binding-boundaries-r21.md; S116 is a round-21 row |
| 16 | MIS | S119 | mined | tripwire-precision-r20.md | L146 'S119 explicitly supersedes S113's finite-module-list inference' = pointer to round-21 correction row |
| 17 | MIS | S120 | mined | tripwire-precision-r20.md | L146 range pointer '(S116-S120)' to round-21 entry |
| 18 | MIS | S132 | queued | terminal-trees-r23.md | L1 `source:` line: 'S132 stays queued and supports nothing.' (S132 deliberately omitted from the source list); S132 status queued |
| 19 | MIS | S187 | mined | event-delivery-limits-r26.md | L80 correction: 'package S187 -> S189' = retired/renumbered id, not this entry's source |
| 20 | MIS | S188 | mined | event-delivery-limits-r26.md | L80 correction: 'S188 -> S201' = retired id remap; S188 row is dispatcher semantics, not this entry's content |
| 21 | MIS | S214 | mined | event-delivery-limits-r26.md | L80 correction: 'S214 -> S212' = retired id remap |
| 22 | MIS | S357 | mined | hyprland-bind-key-match-r50.md | L3 header: 'S357/S358 serve that tool only' (tools/mado-keysym.py); no content use in this entry |
| 23 | MIS | S358 | mined | hyprland-bind-key-match-r50.md | L3 header: 'S357/S358 serve that tool only'; no content use in this entry |
| 24 | BORD | S046 | mined | output-colour-boundaries-r14.md | L87: 'The diagnostic used for S041 did bind/query some interfaces (S046 in the U4 note)' = locator to another note's use of S046; leans REAL for the bind claim, not a source of this entry's own row |
| 25 | REAL | S015 | mined | walker-route-r18.md | L236: 'Per the S015 protocol, these moved pins are reported with old and new values' = applies the protocol (procedural use) |
| 26 | REAL | S041 | mined | input-debugging-boundaries-r15.md | L34 table cell: 'S041 retained only wl_seat interface/version 9' |
| 27 | REAL | S057 | mined | terminal-trees-r23.md | L87: 'the round-17 resolver honours (S057)' |
| 28 | REAL | S059 | mined | xdg-terminal-selection-r47.md | L74: 'held as row S059' for the hotkey declaration |
| 29 | REAL | S060 | mined | xdg-terminal-selection-r47.md | L74: 'the distro list ... (held as S060)' |
| 30 | REAL | S073 | mined | walker-deep.md | L623: 'upstream v2.17.2 default S073' |
| 31 | REAL | S090 | mined | arc-synthesis.md | L392,394: `/var/log/pacman.log:2929` (S090); restart hooks `:3062`,`:3123` (S090) |
| 32 | REAL | S090 | mined | closeout-r11.md | L299: pacman log `:2929` (S090) |
| 33 | REAL | S090 | mined | config-health-report-r3.md | L1009-1010: pacman log `:2929`, `:3062`, `:3123` (S090) |
| 34 | REAL | S090 | mined | remaining-planes-census.md | L338, L340: pacman `:2929`, `:3062`, `:3123` (S090) and host binary `S096` cited |
| 35 | REAL | S090 | mined | walker-deep-r9.md | L403,404,414: pacman `:2929`, hooks `:3062`,`:3123` (S090); L412 disclaims S090 for printed bytes only |
| 36 | REAL | S090 | mined | walker-deep.md | L622, L624: pacman `:2929`, elephant `:3095` (S090) |
| 37 | REAL | S090 | mined | walker-live-surface.md | L305: pacman `:2929` (S090) |
| 38 | REAL | S090 | mined | waybar-walker-plane.md | L479, L481: pacman `:2929`, hooks `:3062`,`:3123` (S090); L483 disclaims only the Waybar versions |
| 39 | REAL | S090 | mined | waybar-walker-semantics.md | L467, L469, L477: pacman `:2929`, `:3095`, hooks (S090) |
| 40 | REAL | S091 | mined | arc-synthesis.md | L402: binary sha is 'the S096/S091 file-byte value' |
| 41 | REAL | S091 | mined | walker-deep-r9.md | L415: 'config.toml ... (S091)' delta sites |
| 42 | REAL | S091 | mined | walker-deep.md | L623, L630: host file 13,743 B (S091), embedded default at offset 806,960 (S091) |
| 43 | REAL | S091 | mined | walker-live-surface.md | L314: packaged config 13,220 B -> 13,743 B (S091) |
| 44 | REAL | S091 | mined | waybar-walker-semantics.md | L476: packaged default 13,743 B (S091), user config 1,336 B |
| 45 | REAL | S096 | mined | arc-synthesis.md | L402: 'S096 recorded at df84807' |
| 46 | REAL | S096 | mined | closeout-r11.md | L307: 'Host walker bytes: S096'; corrects an earlier not-re-measured claim using S096 |
| 47 | REAL | S096 | mined | waybar-walker-semantics.md | L476: 'the binary bytes are S096' |
| 48 | REAL | S158 | mined | hyprctl-flags-r28.md | L23,25,44: `S158 :2107/:2126`, `:2085-2092`, 'OBS S158: the server strips...' |
| 49 | REAL | S158 | mined | hyprctl-verification-layer.md | L306: table 'from the directives (S175-S177, S158, S162)' |
| 50 | REAL | S158 | mined | request-limits-upstream-r31.md | L35 'S158 :2270-2280', L37 'S253, S158: a client can therefore send...' |
| 51 | REAL | S162 | mined | hyprctl-verification-layer.md | L306: same sentence, source list |
| 52 | REAL | S175 | mined | hyprctl-verification-layer.md | L306: range member 'S175-S177' (literal tokens S175, S177 counted; S176 not, see range test) |
| 53 | REAL | S177 | mined | hyprctl-verification-layer.md | L306: range member 'S175-S177' |
| 54 | REAL | S186 | mined | hyprctl-flags-r28.md | L29: locator 'S186 :19' for the documented contract line |
| 55 | REAL | S187 | mined | hyprctl-flags-r28.md | L37: '**INF** S221, S187: this is the documented counterpart of the request socket' |
| 56 | REAL | S201 | mined | event-queue-observability-r37.md | L76: '**INF** S201: Waybar never reconnects (backend.cpp:105,119-122)' |
| 57 | REAL | S277 | mined | request-limits-upstream-r31.md | L31: 'S277 :61' locator for the re-implementation cap |
| 58 | REAL | S318 | mined | hyprland-bind-key-match-r50.md | held row: L15 'held (cited, not re-registered): S318 - ConfigValues.cpp'; L19, L31 table, L93 census held_rows_cited |
| 59 | REAL | S318 | mined | xkb-keymap-compile-r48.md | L17 'held neighbours: rows S318/S319 give the compositor's us default'; L30, L43 step 8 'S318' |
| 60 | REAL | S319 | mined | hyprland-bind-key-match-r50.md | held row: L16 'held: S319 - IKeyboard.cpp'; L19, L29, L88 'OBS S319', L93 census |
| 61 | REAL | S319 | mined | xkb-keymap-compile-r48.md | L17, L30, L32, L36, L43 steps 1 and 8 cite S319 |
| 62 | REAL | S350 | mined | hyprland-bind-key-match-r50.md | L130: host layout receipt 'the round-48 S350 receipt' |
| 63 | REAL | S352 | mined | hyprland-dispatcher-dispatch-r51.md | held row: L20 'held (cited, not re-registered): S352 through S353 ... the same two Hyprland files this entry reads'; L278 census held_rows_cited. (L53 is an ownership note) |
| 64 | REAL | S353 | mined | hyprland-dispatcher-dispatch-r51.md | held row: L20, L278 census held_rows_cited=2 (S352, S353) |
| 65 | REAL | S359 | mined | hyprland-dispatcher-dispatch-r51.md | held row: L20 'S359, the wiki Binds page at the 0.56.2-era revision' |

## Pairs the counter does NOT see (range notation)

The rule's literal tokens (`S[0-9]{3}`) do not expand ranges. Expanding `S\d{3}\s*[-–—]\s*S\d{3}` (variant `--ranges`, `c3_v.py`) gives `missing=70`, i.e. five more pairs, none in the frozen 65:

| S | entry | where | kind |
|---|---|---|---|
| S176 | hyprctl-verification-layer.md | L306 `(S175–S177, S158, S162)` | REAL (range member) |
| S117 | tripwire-precision-r20.md | L146 `(S116–S120)` | MIS (pointer to round-21 entry) |
| S118 | tripwire-precision-r20.md | L146 `(S116–S120)` | MIS (pointer) |
| S057 | xdg-terminal-selection-r47.md | L11 `(rows S056-S060)` | MIS (neighbour pointer) |
| S058 | xdg-terminal-selection-r47.md | L11 `(rows S056-S060)` | MIS (neighbour pointer) |

So the frozen baseline 65 is the literal-token count; it under-counts the citations a human reads (true range-reading count: 70).

## Dangling / extra

- `extra = 0` at base under every variant tested (literal, `--ranges`, `--commonmark`, `--allsource`).
- `dangling = 0` at base. One `source:` header sits outside the first 15 lines (`hyprland-dispatcher-dispatch-r51.md` L16–19); it currently holds only registry ids, so the blind spot does not fire at base (see the forger tests in the report).

## Ambiguous or unsatisfiable items in §C3 (as written)

Recorded in the report `R56RevC3Contract.md` §3. Short list here: (1) `CITE` counts any token, so a refuting or disowning mention is a citation; no status check exists, so the 23 MIS pairs cannot reach `missing=0` with `used-by` edits alone without misrepresenting a row (claims-frozen fixes the target to "used-by edits only"); (2) fence closing rule unstated (mixed `` ``` `` / `~~~` changes the count 66 vs 65, verified); (3) unclosed fence silently excludes all later citations (verified −3); (4) `SRC` = any token on a line starting `source:` in lines 1–15, so prose after `source:` counts (`terminal-trees-r23` L1 "S132 stays queued and supports nothing" is a source pair); (5) range notation is not expanded (5 pairs, above).

## Verification boundary

- Counter run: literal reading, base revision only. Variants and forger tests on scratch copies of the base `corpus/` tree (`forge.py`, `c3_v.py`).
- Not run: the frozen harness `quality/check-r56-controls.py --claim c3` and the counter `quality/counters/c3-r56-used-by.py` (absent at base, `receipts/before.txt`). Control validity was checked by reasoning on the base tree and by running control 6 two ways (see report).
- No hold-out path was touched. No host read was needed for C3.
