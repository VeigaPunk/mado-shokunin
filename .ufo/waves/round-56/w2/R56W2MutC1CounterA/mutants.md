# R56W2MutC1CounterA — mutation test of `quality/counters/c1-r56-autoreload-entry.py` at 28fc86ac

Target: the C1 counter at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (tree `d83d2ebe…`). Pristine md5 `6d13eec7…`, a byte-copy in `receipts/pristine-c1-counter.py`.
Scratch: `git archive 28fc86ac…` into a fresh git repo (toplevel asserted); every mutant is a COPY of the counter. The lane was read-only (`git show`, `git archive`).

## 1. Result in one table

| set | count | killed by the lane's own oracles | killed by proposed fixtures |
|---|---|---|---|
| one-line mutants (`mutate.py`, `MUTANTS`) | 67 | 39 (selftest 38, harness 26; both 25, selftest-only 13, harness-only 1) | — |
| survivors of the lane's oracles | 28 | — | — |
| of which fully EQUIVALENT (argued + randomized) | 5 (M02, M11, M46, M60, M61) | — | — |
| of which VERDICT-EQUIVALENT on sha-verified inputs (output witness given) | 2 (M16, M53) | — | killed at output level by F21, F22 |
| of which NON-EQUIVALENT | 21 | 0 | **21/21** by F01–F20 |

Kill rate with the lane's oracles: **39/67 = 58.2 %** overall; **39/60 = 65.0 %** over the 60 mutants that are not EQUIVALENT (5 mutants fully equivalent, 2 verdict-equivalent set aside). With the proposed fixtures the non-equivalent kill rate is **60/60** (39 already killed + 21 by F01–F20); the two verdict-equivalent mutants are killed at output level by F21/F22.

Oracles: (A) `python3 -I <mutant> --selftest --repo <base> --rev <sha> --work W`, rc 1 = killed; (B) `python3 -I quality/check-r56-controls.py --claim c1 --repo <base> --rev <sha> --work W --counter <mutant>`, killed when the line is not `verdict=OK` with rc 1. Both oracles are unchanged lane code; no mutant was run through a modified harness.

Baseline (pristine): selftest `242/242 assertions passed` (rc 0); harness `MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK` (rc 0); counter `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` (rc 0). Receipts: `receipts/baseline.txt`.

## 2. Mutant table (all 67)

Columns: id, pristine line number, mutation, verdict under the lane's oracles, which oracle killed it, class (killed / EQUIV / VERDICT-EQUIV / NON-EQUIV), and the proposed killer fixture. Full raw data (both oracles' rc and output tails): `receipts/mut-results-67.json`.

| id | line | mutation (pristine -> mutant) | verdict | killed by | class | killer |
|---|---|---|---|---|---|---|
| M01 | 223 | row: cell separator widened to '|': `split(" \| ")` -> `split("\|")` | KILLED | selftest,harness | killed | - |
| M02 | 221 | row: strict_row min length 4 -> 3: `or len(line) < 4:` -> `or len(line) < 3:` | SURVIVED | - | EQUIV | - |
| M03 | 255 | registry_id: min 3 digits -> 2: `if k - j - 1 < 3:` -> `if k - j - 1 < 2:` | KILLED | selftest | killed | - |
| M04 | 245 | registry_id: leading-space tolerance 3 -> 4: `if n > 3 or n >= len(line) or line[n] != "\|":` -> `if n > 4 or ...` | KILLED | selftest | killed | - |
| M05 | 513 | row: '|' inside a cell check dropped: `if any("\|" in c for c in strict):` -> `if False:` | SURVIVED | - | NON-EQUIV | F01 |
| M06 | 524 | row: quote-cell backtick requirement dropped: `if strict[4] != "`" + quote + "`":` -> `if strict[4] != quote:` | KILLED | selftest,harness | killed | - |
| M07 | 527 | row: proposition leading/trailing-space check dropped: `if prop != prop.strip() or len(prop) < ...` -> `if len(prop) < ...` | SURVIVED | - | NON-EQUIV | F02 |
| M08 | 529 | row: proposition uniqueness count != 1 -> != 2: `if prop_count.get(prop, 0) != 1:` -> `!= 2` | KILLED | selftest,harness | killed | - |
| M09 | 518 | row: src-cell ASCII check dropped: `and strict[2][1:].isascii()):` -> `and True):` | SURVIVED | - | NON-EQUIV | F03 |
| M10 | 522 | row: pin:line cell arguments swapped: `% (pin, line)` -> `% (line, pin)` | KILLED | selftest,harness | killed | - |
| M11 | 511 | row: candidate multiplicity == 1 -> >= 1 (redundant check): `len(cand[rid]) == 1` -> `>= 1` | SURVIVED | - | EQUIV | - |
| M12 | 381 | row: duplicated row tolerated by row_data: `if len(lines) != 1:` -> `if len(lines) < 1:` | SURVIVED | - | NON-EQUIV | F04 |
| M13 | 539 | quote: empty-carried-quote check dropped: `or carried == ""` -> (deleted) | SURVIVED | - | NON-EQUIV | F05 |
| M14 | 538 | quote: backtick delimiters not required in the quote cell: `... and q[-1] == "`" else ""` -> `if len(q) >= 2 else ""` | SURVIVED | - | NON-EQUIV | F05 |
| M15 | 533 | quote: pin line off by one (line -> line+1): `pin_line(pin, line)` -> `pin_line(pin, line + 1)` | KILLED | selftest,harness | killed | - |
| M16 | 440 | quote: pin line bound widened (n > len(pl) -> n > len(pl)+1): `or n > len(pl):` -> `or n > len(pl) + 1:` | SURVIVED | - | VERDICT-EQUIV (sha domain) | F21 |
| M17 | 442 | quote: pin line index off by one (pl[n-1] -> pl[n]): `return pl[n - 1]` -> `return pl[n]` | KILLED | selftest,harness | killed | - |
| M18 | 543 | host: empty-carried-quote check dropped: `carried != ""` -> `True` | SURVIVED | - | NON-EQUIV | F06 |
| M19 | 545 | host: host leg always true: `host_ok[rid] = hok` -> `host_ok[rid] = True` | KILLED | selftest | killed | - |
| M20 | 464 | source_cell: tier check dropped: `or cells[3] not in ("A", "B")` -> (deleted) | KILLED | selftest | killed | - |
| M21 | 471 | source_cell: rev_rule token in URL dropped: `or tok not in urls[-1]` -> (deleted) | SURVIVED | - | NON-EQUIV | F07 |
| M22 | 473 | source_cell: used-by cell check dropped: `return ENTRY in cells[10]` -> `return True` | KILLED | selftest | killed | - |
| M23 | 455 | source_cell: duplicated registry row tolerated: `if len(rows) != 1:` -> `< 1` | KILLED | selftest | killed | - |
| M24 | 458 | source_cell: registry cell count 11 -> >= 11: `len(cells) == 11` -> `>= 11` | KILLED | selftest | killed | - |
| M25 | 466 | source_cell: URL read from the id cell instead of the source cell: `URL_RE.findall(cells[1])` -> `cells[0]` | KILLED | selftest,harness | killed | - |
| M26 | 290 | scope: locator lower-bound check dropped: `or lo > nlines` -> (deleted) | SURVIVED | - | NON-EQUIV | F08 |
| M27 | 292 | scope: range upper bound exclusive (line <= hi -> line < hi): `elif lo <= line <= hi:` -> `elif lo <= line < hi:` | KILLED | selftest,harness | killed | - |
| M28 | 302 | scope: 'over' veto dropped (anchor-past-EOF not fatal): `return covered and not over` -> `return covered` | SURVIVED | - | NON-EQUIV | F09 |
| M29 | 268 | scope: locator key widened (basename -> basename, no colon): `key = basename + ":"` -> `key = basename` | KILLED | selftest,harness | killed | - |
| M30 | 483 | scope: pin line-count bound not passed to the scanner: `len(pl) if pl is not None else None` -> `None` | KILLED | selftest,harness | killed | - |
| M31 | 294 | scope: locator list separator ',' -> ';' | KILLED | selftest,harness | killed | - |
| M32 | 486 | tok: shared-quote side of the intersection dropped: `& set(TOKEN_RE.findall(quote))` removed | KILLED | selftest,harness | killed | - |
| M33 | 305 | tok: identifier length bound widened (3 -> 2): `{3,}` -> `{2,}` | KILLED | selftest | killed | - |
| M34 | 305 | tok: identifier length bound narrowed (3 -> 4): `{3,}` -> `{4,}` | SURVIVED | - | NON-EQUIV | F10 |
| M35 | 556 | tok/num/echo: echo result forced true: `..., echo_ok[rid] = t, n, ec` -> `..., t, n, True` | KILLED | selftest,harness | killed | - |
| M36 | 487 | num: digit runs taken from the proposition instead of the quote: `re.findall(r"[0-9]+", quote)` -> `prop` | KILLED | selftest,harness | killed | - |
| M37 | 488 | num: the row's own line dropped from the allowed integers: `ints = {0, 1, 2, 3, line}` -> `{0, 1, 2, 3}` | SURVIVED | - | NON-EQUIV | F11 |
| M38 | 490 | num: allowed integers taken from every pin (same-pin filter dropped): `if r["pin"] == pin:` -> `... or True:` | SURVIVED | - | NON-EQUIV | F12 |
| M39 | 306 | num: digit-run regex trailing boundary dropped: `(?![A-Za-z0-9_])` removed from RUN_RE | SURVIVED | - | NON-EQUIV | F13 |
| M40 | 495 | num: allowed-integer comparison inverted: `v in ints` -> `v not in ints` | KILLED | selftest,harness | killed | - |
| M41 | 498 | echo: 'quote in proposition' test dropped: `and quote in prop` removed | KILLED | selftest,harness | killed | - |
| M42 | 25 | echo: ECHO_MIN constant 30 -> 20 | KILLED | selftest | killed | - |
| M43 | 25 | echo: ECHO_MIN constant 30 -> 31 | SURVIVED | - | NON-EQUIV | F14 |
| M44 | 402 | prov: window widened (first 15 lines -> first 30): `entry_lines[:15]` -> `[:30]` | SURVIVED | - | NON-EQUIV | F15 |
| M45 | 406 | prov: exactly one verified-at line -> at least one: `len(ver_idx) == 1` -> `>= 1` | SURVIVED | - | NON-EQUIV | F16 |
| M46 | 408 | prov: order comparison off by one (source < verified -> source <= verified) | SURVIVED | - | EQUIV | - |
| M47 | 414 | prov: cited-sid subset test inverted: `sids_cited <= src_set` -> `>=` | KILLED | selftest,harness | killed | - |
| M48 | 412 | prov: registry-membership test inverted: `any(...)` -> `all(...)` | KILLED | selftest,harness | killed | - |
| M49 | 411 | prov: source-line sid regex widened: `SID_RE.findall` -> `re.findall(r"S[0-9]+", ...)` | SURVIVED | - | NON-EQUIV | F17 |
| M50 | 423 | index: README match widened (startswith -> contains): `l.startswith(INDEX_PREFIX)` -> `INDEX_PREFIX in l` | SURVIVED | - | NON-EQUIV | F18 |
| M51 | 424 | index: index count check inverted (!= 1 -> < 1) | KILLED | selftest | killed | - |
| M52 | 36 | new_rows: required denominator 8 -> 7 | KILLED | selftest,harness | killed | - |
| M53 | 604 | new_rows: frozen id-count check dropped: `or len(c1["new_row_ids"]) != NEW_ROWS_DENOM` -> (deleted) | SURVIVED | - | VERDICT-EQUIV (sha domain) | F22 |
| M54 | 601 | new_rows: source_cell requirement dropped from the count: `and source_cell_ok(sid, pin)` removed | KILLED | selftest,harness | killed | - |
| M55 | 570 | pin_hash: only the first pin blob is checked: `pins_all.items()` -> `list(...)[:1]` | KILLED | selftest,harness | killed | - |
| M56 | 572 | pin_hash: comparison inverted (!= want -> == want) | KILLED | selftest,harness | killed | - |
| M57 | 432 | pin_hash: host pin blobs not checked: `pins_all.update(c1["host_pin_sha256"])` -> (deleted) | SURVIVED | - | NON-EQUIV | F19 |
| M58 | 321 | tables_sha: comparison inverted (== -> !=) | KILLED | selftest,harness | killed | - |
| M59 | 23 | tables_sha: frozen constant altered (last hex digit 2 -> 3) | KILLED | harness | killed | - |
| M60 | 622 | render: content threshold 33 -> >= 33: `counts["e"] == 33` -> `>= 33` | SURVIVED | - | EQUIV | - |
| M61 | 621 | render: rows threshold 30 -> >= 30: `counts["a"] == 30` -> `>= 30` | SURVIVED | - | EQUIV | - |
| M62 | 627 | render: 'none' for an empty missed list dropped | KILLED | selftest,harness | killed | - |
| M63 | 117 | repo: symlink blob mode accepted as a regular file: `mode not in REGULAR_MODES` removed | KILLED | selftest | killed | - |
| M64 | 201 | scanner: a row inside an HTML comment counts as live: `if first_pipe_live:` -> `is not None` | KILLED | selftest | killed | - |
| M65 | 148 | scanner: fence minimum length 3 -> 2: `if m - n < 3:` -> `< 2:` | SURVIVED | - | NON-EQUIV | F20 |
| M66 | 299 | scope: 'continue' after a comma locator dropped | KILLED | selftest,harness | killed | - |
| M67 | 306 | num: RUN_RE both boundaries dropped (`[0-9]+` only) | KILLED | selftest | killed | - |

## 3. Equivalence arguments (the five EQUIV mutants)

Each is backed by the argument below AND by a randomized differential: `equiv_fuzz.py --trials 300 --seed 56` applied one random byte-level perturbation (delete, insert `|`/space/char, substitute a digit, duplicate a line, tab or double-space a pipe) to the entry, registry or README of 300 fresh repos and compared stdout and rc of each mutant with the pristine. Result: `M02 trials=300 divergences=0`, `M11 trials=300 divergences=0`, `M46 trials=300 divergences=0`, `M60 trials=300 divergences=0`, `M61 trials=300 divergences=0` (`receipts/equiv-fuzz-300.json`). Empirical support only; the arguments are the proof.

- **M02** (`len(line) < 4` -> `< 3`). `strict_row` runs only on candidate lines (first cell an id `K01..K30`/`H01..H03`), both in `row_data` and in the `prop_count` loop over the same candidates. A candidate line contains at least `| K01 |` (7 bytes), so a 3-byte bound never decides.
- **M11** (`len(cand[rid]) == 1` -> `>= 1`). The conjunct is reached only with `strict is not None`. `row_data` (L378-387) returns a non-None strict only when `len(lines) == 1`, so the conjunct is already true when evaluated.
- **M46** (`min(src_idx) < ver_idx[0]` -> `<=`). `src_idx` indexes lines starting `source:`; `ver_idx[0]` indexes a line equal to `verified-at: 2026-10-28`. No line satisfies both, so the two indices are never equal.
- **M60** (`counts["e"] == 33` -> `>= 33`). `counts["e"]` is a sum over the 33 K+H rows, so it is at most 33.
- **M61** (`counts["a"] == 30` -> `>= 30`). `counts["a"]` is a sum over the 30 K rows, so it is at most 30.

## 4. Verdict-equivalent mutants (sha-domain) — witnesses only

- **M16** (`n > len(pl)` -> `n > len(pl)+1`) differs only when a row line equals `len(pl)+1`, where `pl[n-1]` raises IndexError. Every frozen row line is below its pin's split length (measured: ConfigWatcher max row 105 vs split 112; ConfigValues 492 vs 735; HyprCtl 1276 vs 2347; legacy ConfigManager 1844 vs 2185; man7 262 vs 920; host-sources 10 vs 19; host-getoption 1 vs 2; host-version 3 vs 23). The frozen tables are fixed by `TABLES_SHA256`, so no sha-verified input reaches the branch. Witness F21 (below): a row line one past the split length gives IndexError, rc 1, no stdout.
- **M53** (`or len(c1["new_row_ids"]) != NEW_ROWS_DENOM` removed). The frozen `new_row_ids` has 8 entries; `TABLES_SHA256` fixes it. Witness F22 (nine ids): the pristine prints `new_rows`, the mutant does not; both print `tables_sha`.

## 5. Non-equivalent survivors: the smallest killer fixture, verified

Each fixture is ONE edit of the good tree (a minimal scratch repo holding only the paths the counter reads at `--rev`: entry, registry, README, frozen tables, fetch pins), committed with the ctl identity. The pristine counter must print the registered leg (sanity check); the mutant is killed when its stdout or rc differs. Driver: `killers.py`; receipt: `receipts/killers-results.json`. All 22 fixtures ran: 22/22 pristine expectations held, and each named mutant was killed.

| fixture | one edit on the good tree | mutant(s) | pristine (registered behaviour) | mutant | killed |
|---|---|---|---|---|---|
| F01 | K01 proposition += ` Pipe a\|b here.` (a `\|` inside a cell, no spaces) | M05 | rc 1, `missed=row:K01` | rc 0, `TARGET_MET` | yes |
| F02 | K01 proposition with a leading space (`\|  prop`) | M07 | rc 1, `missed=row:K01` | rc 0, `TARGET_MET` | yes |
| F03 | K01 source cell `S384` -> `S38` + U+0664 (ARABIC-INDIC DIGIT FOUR) | M09 | `missed=prov,row:K01,source_cell:K01,scope:K01` | `missed=prov,source_cell:K01,scope:K01` (row leg lost) | yes |
| F04 | a second K08 row (proposition + ` again`) | M12 | `missed=row:K08,source_cell:K08,scope:K08,tok:K08,num:K08,echo:K08`, content 32/33 | `missed=row:K08` only, content 33/33 | yes |
| F05 | K01 quote cell without backticks | M13, M14 | `missed=row:K01,quote:K01` | `missed=row:K01` (quote leg passes) | yes (both) |
| F06 | H01 quote cell without backticks | M18 | `missed=row:H01,quote:H01,host:H01` | `missed=row:H01,quote:H01` (host leg passes) | yes |
| F07 | S383 URL (cell 1) commit `efb5…` -> 40 zeros | M21 | `source_cell:K03..K12`, `new_rows=7/8` | `TARGET_MET` | yes |
| F08 | S383 anchor += `,200-40` (reversed range past EOF) | M26 | `scope:K03..K12`, `scope=20/30` | `TARGET_MET` | yes |
| F09 | S383 anchor += `,200` (over-locator beside in-range locators) | M28 | `scope:K03..K12`, `scope=20/30` | `TARGET_MET` | yes |
| F10 | K24 proposition `The glob step expands the watched path on this line of the pinned source.` (shares only `glob`, 4 chars) | M34 | `TARGET_MET` | `missed=tok:K24`, content 32/33 | yes |
| F11 | H02 proposition += ` Line 10 of the capture is one source line.` (own line number) | M37 | `TARGET_MET` | `missed=num:H02`, content 32/33 | yes |
| F12 | K07 proposition += ` Compare the value 492 here.` (another pin's line) | M38 | `missed=num:K07`, content 32/33 | `TARGET_MET` | yes |
| F13 | K04 proposition += ` The cap is 200ms.` | M39 | `TARGET_MET` (**bypass, see DEF-1**) | `missed=num:K04` | yes |
| F14 | K07 proposition = its 30-character quote + ` echoed on this line, no analysis added here` | M43 | `missed=echo:K07` | `TARGET_MET` | yes |
| F15 | 15 filler lines before the entry header (source line now line 16) | M44 | `missed=prov` | `TARGET_MET` | yes |
| F16 | a second `verified-at: 2026-10-28` line in the head | M45 | `missed=prov` | `TARGET_MET` | yes |
| F17 | source line += ` S38` (2-digit token) | M49 | `TARGET_MET` (**weakness, see DEF-2**) | `missed=prov` | yes |
| F18 | README gains `see \| \`knowledge/hyprland-config-autoreload-r56.md\` for the chain` | M50 | `TARGET_MET` | `missed=index` | yes |
| F19 | host-getoption.json byte `f` of `false` -> `g` | M57 | `missed=pin_hash` | `TARGET_MET` | yes |
| F20 | a `` `` `` line (two backticks) before K01 | M65 | `TARGET_MET` | rc 1, `rows=0/30`, all 30 K rows missed | yes |
| F21 | frozen table: K03 line 33 -> 113 (one past ConfigWatcher's split length 112) — witness for M16 | M16 | rc 1, `missed=tables_sha,row:K03,quote:K03,scope:K03` | rc 1, IndexError traceback, no stdout | yes (output level) |
| F22 | frozen table: `new_row_ids` += `S391` — witness for M53 | M53 | rc 1, `missed=tables_sha,new_rows` | rc 1, `missed=tables_sha` | yes (output level) |

The fixtures are verified only as differentials against the pristine counter. They are proposed controls for a successor harness; the lane's frozen harness was not edited, and no new control was run through it.

## 6. Defects and weaknesses (found while attacking the counter)

- **DEF-1 — weakens claim (num leg, latent).** The registered digit-run regex `(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])` treats a numeral followed by a letter as not a digit run. A proposition such as `The cap is 200ms.` (F13) passes `num`, and the counter prints `TARGET_MET` with that K04. Input: `K04` proposition `The cap is 200ms.`. Latent at 28fc86ac: no proposition of the 33 rows contains any digit (checked). Severity: weakens claim.
- **DEF-2 — weakens claim (provenance ids, latent).** The `S###` id token (`prov` leg; the C3 `CITE`/`SRC` rules use the same shape per registration.md §C3) requires exactly three digits. A source line with `S38` (F17) passes `prov` and the counter prints `TARGET_MET`. Latent: the source line holds exactly `S383`..`S391`. Because C3's `dangling`/`CITE` use the same regex, a two- or four-digit typo in a source line is invisible to both C1 and C3. Severity: weakens claim.
- **DEF-3 — test gap (21 non-equivalent survivors).** The lane's selftest (242 assertions) and frozen controls (12) never exercise: a `|` inside a cell (M05); a leading-space proposition (M07); a non-ASCII digit in a source id (M09); a duplicated row's collateral legs (M12); a bare quote cell (M13, M14, M18); a URL with a wrong revision token (M21); a reversed locator past EOF (M26); an over-locator beside an in-range one (M28); a 4-character identifier (M34); an H row's own line number (M37); another pin's line number (M38); a numeral with letters (M39); the 30-character echo boundary (M43); the 15-line provenance window (M44); a second `verified-at` (M45); a non-`S###` source token (M49); a mid-line README match (M50); a host pin byte (M57); a two-backtick fence (M65). Severity: test gap (each survivor is a counter branch no oracle pins).
- **DEF-4 — test gap in frozen control 12 (anchor-past-eof).** The control's single over-locator (`ConfigWatcher.cpp:1-9999`) cannot separate the `over` veto from `covered`: the `elif` skips coverage for an over-locator, so `covered` is already false. The veto matters only with an over-locator beside an in-range one (F09, M28). The selftest's `reg-scope-past-eof` (`34-200`) has the same single-locator shape. Severity: weakens the test, not the claim.
- Not a defect: M16's crash path (F21) is a mutant effect; the pristine guards `n > len(pl)` and reports the leg.

## 7. What was not verified

- The five EQUIV classifications are argued and empirically supported (300 random perturbations per mutant, zero divergences); they are not exhaustively proven.
- M16 and M53 are verdict-equivalent only on sha-verified inputs; the output difference is shown on a sha-broken table, which the frozen `tables_sha` leg already fails.
- The 22 killer fixtures are differentials, not a new harness; their pristine expectations are my reading of registration.md §C1 and registration-v2 E2–E5.
- The randomized differential does not perturb the frozen tables or pins (sha-bound).
- No real-data claim: the counter's verdict on the lane's content was not reinterpreted; DEF-1 and DEF-2 are latent (the current content has no digits in propositions and no non-`S###` source tokens).

## 8. Reproduction

Driver files in this directory: `mutate.py` (67 mutants, both oracles), `killers.py` (22 fixtures), `equiv_fuzz.py` (randomized differential).

```
S=/fast/scratch/hyaku/mado-r56/<seat>; R=28fc86ac2359ec27406d8a2c63bef82ea6e947ed
python3 -I mutate.py --lane /home/vgpnk/Projects/shokunin/mado-shokunin --rev $R --out $S/mut --jobs 10
python3 -I killers.py --base $S/base --rev <base commit> --scratch $S/killers --out $S/killers/killers.json
python3 -I equiv_fuzz.py --base $S/base --rev <base commit> --scratch $S/eq --trials 300 --seed 56
```

Tool installs: none. Lane writes: none (read-only `git show` / `git archive`).
