# RevC2Counter: C2 counter attack, v1 probes and v2 re-run

Scope: attack `.ufo/waves/round-23/c2/count.py` (C2 coverage counter). Part 1 was the assigned v1 attack at base a28e4815. Part 2 is the L1 follow-up: re-run the same probes against the landed v2 at 4de44647. The lane's master tip is 4de44647 (checked read-only). Between a28e48 and 4de44647 the diff touches only `c2/count.py`, `c3/count.py`, two evidence files and `registration.md`. `corpus/SOURCES.md` and the note path are unchanged, so probe commits based on a28e48 are valid inputs for v2.

Verdict: v2 closes the substring-name, two-terminal and substring-only 3/3 holes, and adds a host-tree cell rule. It leaves open the duplicate-id, leads-scope, fence and table scope, id-prefix, decode-exit and silent-drop holes. It also adds one hole, a fork-path prefix (V2-H6). The v3 candidate on the v2 schema clears every structural hole in the probe set. It is not landed, and it has no corpus replay. Bookkeeping-only 3/3 and annotation words in route rows are residual risks for L1 to decide.

## 1. Base run (assignment step 1)

Command, run under `prlimit --as=402653184 timeout 15`:
`python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/c2/count.py a28e4815aabfa85f55274884000fb2608355f8cf`

Output: `{"rev": "a28e4815...", "note_present": false, "terminals": {"foot": [], "kitty": [], "ghostty": []}, "count": "0/3"}`, then `EXIT=1`. This matches the expectation of 0/3 and exit 1.

Same counter at 4de44647 (v2, read through a worktree): 0/3, exit 1. v3 candidate at a28e48 and 4de44647: 0/3, exit 1. The v2 and v3 counters report `counter_version` 2 and 3. The count and exit code did not change at base.

## 2. Method

- Scratch clone: `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r23/RevC2Counter`, then `checkout -B revc2-base a28e4815...`. Each probe is one commit on `probe/<name>` (v1 set) or `probe-v2/<name>` (v2 set), branched from a28e48. Each commit adds one note and one or more SOURCES rows. Probe SHAs are in `RevC2Counter-work/probes.json` and `probes_v2.json`.
- Lane v2 was fetched into the clone with `git -C RevC2Counter fetch -q <lane> "+refs/heads/*:refs/lane/heads/*"` and checked out read-only as worktree `RevC2Counter-v2` (detached at 4de44647).
- Fix candidates live in worktrees: `RevC2Counter-fix` (branch `revc2-fix`, v1 fix) and `RevC2Counter-v3` (branch `revc2-v3`, v3 on top of v2). Nothing was pushed. The lane was not written, except for this report.
- Runner: `RevC2Counter-work/run_all.py`. It runs 59 cases through 4 counters, one child at a time, with `prlimit --as=402653184 timeout 15 python3 -I`. That is 236 child runs, about 6 s wall time. The full JSON is at `RevC2Counter-work/results_all.json`.
- Installs or updates: none. Tools used were python3 3.14.8, prlimit and timeout (both already present), and read-only git against the lane.

Counters in the matrix:
- `v1`: the lane counter at a28e48 (the assignment target).
- `v1-cand`: my v1 fix candidate, commit 1ca93479 on `revc2-fix`.
- `v2`: the lane counter at 4de44647 (landed).
- `v3-cand`: my v3 candidate, commit cc254c24 on `revc2-v3`.

## 3. Findings by severity (v2 as landed at 4de44647)

High

1. **Duplicate registry ids resolve silently to the last row.** `main` does `registry[row[0]] = {...}` (v2 lines 69-75), with no duplicate check. V2-H1b (a rejected row, then a valid row for S305) counts FP kitty S305. V2-H1c (an appended S021 row shadows the real S021) counts FP kitty S021. The same holes exist in v1 (P6b, P6c). v3 withholds duplicated ids and lists them in `duplicate_ids`.
2. **Registry scope is every `| S### |` line in the file.** The regex at v2 line 71 has no section check. V2-H2 places a valid registry row under `## Leads (unopened)` and it counts FP kitty S306. SOURCES.md says "A lead is not evidence and never a row." v3 reads only the `## Registry` section.
3. **Route rows need not be in a table, and fenced code is read.** V2-H3 (a valid route row inside a fenced block) counts FP kitty S307. V2-H4 (one pipe-led line with no header or delimiter row) counts FP kitty S308. v3 reads only rows of a table with a header and a delimiter row, and skips fenced code.

Medium

4. **Id tokens are not bounded.** `re.findall(r"S\d{3}", line)` (v2 line 89) makes a citation of S3090 count through S309 (V2-H5a FP). XS309 counts through S309 (V2-H5b FP). v3 uses `(?<![A-Za-z0-9])S\d{3}(?![A-Za-z0-9])`.
5. **The upstream test is a bare substring (v2 line 59).** `https://github.com/kovidgoyal/kitty-fork-unofficial` satisfies kitty's upstream prefix, so V2-H6 counts FP kitty S310. This rule is new in v2. v1 had no upstream rule. v3 requires the next character to lie outside `[A-Za-z0-9_-]`.
6. **Decode errors exit 1 with a traceback, not 2.** `show()` uses `text=True` (v2 lines 36-37), so `UnicodeDecodeError` escapes. P10a and V2-H11 both exit 1 with `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff`. Exit 1 also means "not 3/3", so the two cannot be told apart. v3 decodes bytes and exits 2.
7. **Registry rows are dropped silently.** A row with a 12th cell (an escaped pipe) is dropped with no diagnostic (V2-H10, v1 P9d). A row written `| S319  |` with two spaces fails the `^\| S\d{3} \|` match and is dropped (V2-H15, v1 P9e, a false negative). v3 counts cells, lists malformed ids, and accepts the double-space form.

Judgment items (not counted as defects, for L1 to decide)

8. **Route-row annotations are not read.** A `(unused)` annotation in the config cell (V2-H13) counts. A `REJECTED` annotation in the config cell (V2-H14) counts. v1 P1b and P3b also counted. Options: reject rows that carry status words, or accept this as residual.
9. **Bookkeeping-only 3/3 (V2-X1).** Three self-written registry rows (status mined, opened 2026-10-22, an upstream URL, used-by the note) give 3/3 with exit 0, with no retained receipt. The counter checks the text of the registry, not that anything was opened. A check that the anchor names a file that exists at REV would close this. It is not implemented in any candidate.
10. **The name check is redundant with the upstream check (code reading; not probed).** Every UPSTREAM string contains its terminal as a whole word, so any source carrying an upstream URL passes the name test whatever its prose says. This is a simplification candidate, not a probe result.

Strictness false negatives (fail closed; all three candidates keep them)

11. Status `Mined` (V2-H9, v1 P9a), status `**mined**` (P9b), opened `2026-10-22T09:00Z` (P9c), and first cell `**kitty**` (P1c) are not counted.

Silent resolution, order-dependent

12. Duplicate valid-then-rejected (P6a, V2-H1a) is not counted only because last-wins picks the rejected row. There is no diagnostic. The same pair in reverse order counts (V2-H1b).

## 4. Assignment probes, v1 at base a28e48

| Assignment probe | v1 result | Verdict |
|---|---|---|
| 1. First cell `kitty (unused)` over a valid kitty row (P1a) | Not counted | ok. The exact-name match rejects it silently. |
| 2. Source opened on a different date (P2a, 2026-10-21); suffix variant (P2b) | Not counted | ok. Exact date match. |
| 3. Rejected row: status `rejected`, opened 2026-10-22 (P3a); `REJECTED` text in a route row (P3b) | P3a not counted. P3b counted. | P3a ok. P3b is a FP (semantic). |
| 4. Source names another terminal (P4a, ghostty source cited by a kitty row) | Not counted | ok. Substring hazards are FPs: `barefoot` for foot (P4b), `Skitty` for kitty (P4c). A two-terminal source counts for both (P4d, judgment). |
| 5. Row id in prose outside a table (P5a); list item (P5d) | Not counted | ok. A fenced example row counts FP (P5b). A pipe-led line with no table counts FP (P5c). |
| 6. Duplicate ids: mined then rejected (P6a); rejected then mined (P6b); appended S021 shadows the real S021 (P6c) | P6a not counted (silent). P6b and P6c count FP. | P6b and P6c are FPs. |

Other v1 probes:
- P0 control (one valid row per terminal): 3/3, exit 0. The positive path works.
- P1b `(unused)` in a later cell: counted (FP, semantic).
- P1c bold first cell: not counted (FN, strictness).
- P7a row under Leads: counted (FP).
- P8a `S2010` citing S201: counted (FP). P8b `XS201`: counted (FP).
- P9a, P9b, P9c: not counted (FN, strictness).
- P9d 12-cell row: silent drop.
- P9e double-space id: not counted (FN).
- P10a non-UTF-8 note: exit 1 with traceback, not 2.
- P11 note present only as an uncommitted working-tree file: not read. Counter reads committed bytes only. OK.
- P12 exploit, three substring names: 3/3 with exit 0. Every count is a FP.

## 5. Fix candidates (not landed)

- **v1 candidate** (`RevC2Counter-fix`, branch `revc2-fix`, commit 1ca93479, patch `RevC2Counter-work/count-fix.patch`, +68/-23 against a28e48). It is a v1 fix; it does not implement v2 rules. It closes P4b, P4c, P5b, P5c, P6b, P6c, P7a, P8a, P8b, P9e, P10a and P12. It reports P9d. It keeps P1b, P3b, P4d (no other-terminal check), and the strictness FNs.
- **v3 candidate on v2** (`RevC2Counter-v3`, branch `revc2-v3`, commit cc254c24, patch `RevC2Counter-work/count-v3.patch`, +75/-30 against 4de44647). It keeps every v2 rule (host-tree cell, upstream, used-by, whole-word, one-terminal source). Its structural changes are: table-only rows with fences skipped; registry section only; whole-token ids; duplicate ids withheld and listed; malformed rows listed; upstream path boundary; decode errors exit 2; cell-based registry id (double space accepted). On the v2 probe set it clears V2-H1a, H1b, H1c, H2, H3, H4, H5a, H5b, H6, H10 (reported), H11 and H15. It keeps the judgment items (H13, H14, X1) and the strictness FNs (H9). Its base values are 0/3 at both a28e48 and 4de44647.

## 6. Part 2: v2 re-run at 4de44647 and closure map

Schema note. The v1-shaped probes lack the `~/.config/<T>/` cell, the upstream URL and the used-by note, so under v2 they are not counted for schema reasons alone. They are not attribution evidence for v2. The closure claims below rest on the v2-shaped set (V2-*), where each probe is valid except for the property under test. Several v1-set rows under v2 show `FN` or `ok` only because of this schema mismatch, and are marked "(schema)" in the matrix below.

Closed by v2:
- P4b substring `barefoot` (V2-H7 is ok at v2, and the v1 result was FP). Closed. A source with a foot URL still counts whatever its prose (see judgment item 10).
- P4c substring `Skitty` (V2-X2 is ok at v2). Closed for the substring-only form.
- P4d two-terminal source (V2-H8: counted by v1 and v1-cand, ok at v2). Closed.
- P12 substring-only 3/3 exploit (V2-X2: 3/3 at v1, 0/3 at v2). Closed. The bookkeeping-only form remains (V2-X1, judgment item 9).
- Missing host-tree rows (V2-H12): counted by v1, not counted at v2 by design. New v2 requirement.
- P5a prose and P5d list item: ok at v1 and v2. Already closed.
- P10b unknown revision: exit 2 at v1 and v2. Already closed.

Still open at v2:
- P5b fenced example (V2-H3): FP.
- P5c pipe-led line without a table (V2-H4): FP.
- P6b duplicate rejected-then-valid (V2-H1b): FP.
- P6c shadow of real S021 (V2-H1c): FP.
- P6a duplicate valid-then-rejected (V2-H1a): not counted, but silent and order-dependent.
- P7a row under Leads (V2-H2): FP.
- P8a `S2010` citing S201 and V2-H5a `S3090` citing S309: FP (same id-prefix hole).
- P8b `XS309` citing S309 (V2-H5b): FP.
- P10a and V2-H11 non-UTF-8 note: exit 1 with traceback, not 2.
- P9d and V2-H10 12-cell row: silent drop (no diagnostic).
- P9e and V2-H15 double-space id: false negative.
- P1b and V2-H13 `(unused)` annotation: counted.
- P3b and V2-H14 `REJECTED` annotation: counted.
- P1c, P9a, P9b, P9c, V2-H9 strictness: not counted (deliberate, fail closed).

Introduced or kept by v2 (new in this set):
- V2-H6 fork path under the kitty upstream prefix: FP. v1 counted it too, and v2's upstream rule does not close it.

### Matrix: each probe under each counter

Key: `ok` = matches intent; `FP` = counted but should not be; `FN` = not counted but should be; `judg` = counted, intent undecided; `e<N>` = exit code; `(schema)` = v1-shaped row that fails v2 schema.

| Probe (v1 set) | v1 | v1-cand | v2 | v3-cand |
|---|---|---|---|---|
| P0-control | e0 ok (3/3) | e0 ok | e1 FN x3 (schema) | e1 FN x3 (schema) |
| P1a kitty (unused) first cell | ok | ok | ok | ok |
| P1b (unused) in later cell | FP kitty S201 | FP kitty S201 | ok (schema) | ok (schema) |
| P1c bold first cell | FN kitty S201 | FN | FN (schema) | FN (schema) |
| P2a other date | ok | ok | ok | ok |
| P2b date with suffix | ok | ok | ok | ok |
| P3a rejected status | ok | ok | ok | ok |
| P3b REJECTED route text | FP kitty S201 | FP | ok (schema) | ok (schema) |
| P4a source names other terminal | ok | ok | ok | ok |
| P4b barefoot source | FP foot S208 | ok | ok (schema) | ok (schema) |
| P4c Skitty source | FP kitty S209 | ok | ok (schema) | ok (schema) |
| P4d two-terminal source | judg kitty,ghostty | judg | judg none (schema) | judg none (schema) |
| P5a prose outside table | ok | ok | ok | ok |
| P5b fenced example | FP kitty S201 | ok | ok (schema) | ok (schema) |
| P5c pipe line without table | FP kitty S201 | ok | ok (schema) | ok (schema) |
| P5d list item | ok | ok | ok | ok |
| P6a dup mined then rejected | ok (silent) | ok (lists S211) | ok (silent) | ok (lists S211) |
| P6b dup rejected then mined | FP kitty S212 | ok | ok (schema) | ok (schema) |
| P6c dup shadows S021 | FP kitty S021 | ok | ok (schema) | ok (schema) |
| P7a row under Leads | FP kitty S213 | ok | ok (schema) | ok (schema) |
| P8a id prefix S2010 | FP kitty S201 | ok | ok (schema) | ok (schema) |
| P8b id prefix XS201 | FP kitty S201 | ok | ok (schema) | ok (schema) |
| P9a status `Mined` | FN kitty S214 | FN | FN (schema) | FN (schema) |
| P9b status `**mined**` | FN kitty S215 | FN | FN (schema) | FN (schema) |
| P9c timestamp opened | FN kitty S216 | FN | FN (schema) | FN (schema) |
| P9d 12-cell row | ok (silent) | ok (lists S217) | ok (silent) | ok (lists S217) |
| P9e double-space id | FN kitty S218 | ok | FN (schema) | FN (schema) |
| P10a non-UTF-8 note | e1 (want 2) | e2 ok | e1 (want 2) | e2 ok |
| P11 uncommitted note | ok | ok | ok | ok |
| P12 three substring names | FP x3, e0 | ok | ok (schema) | ok (schema) |

| Probe (v2 set) | v1 | v1-cand | v2 | v3-cand |
|---|---|---|---|---|
| V2-P0-control | e0 ok (3/3) | e0 ok | e0 ok | e0 ok |
| V2-H1a dup valid then rejected | ok (silent) | ok | ok (silent) | ok (lists S304) |
| V2-H1b dup rejected then valid | FP kitty S305 | ok | FP kitty S305 | ok (lists S305) |
| V2-H1c shadow real S021 | FP kitty S021 | ok | FP kitty S021 | ok (lists S021) |
| V2-H2 row under Leads | FP kitty S306 | ok | FP kitty S306 | ok |
| V2-H3 fenced example | FP kitty S307 | ok | FP kitty S307 | ok |
| V2-H4 pipe line, no table | FP kitty S308 | ok | FP kitty S308 | ok |
| V2-H5a id prefix S3090 | FP kitty S309 | ok | FP kitty S309 | ok |
| V2-H5b id prefix XS309 | FP kitty S309 | ok | FP kitty S309 | ok |
| V2-H6 fork path under upstream prefix | FP kitty S310 | FP kitty S310 | FP kitty S310 | ok |
| V2-H7 barefoot, no URL | FP foot S311 | ok | ok | ok |
| V2-H8 two-terminal source with kitty URL | FP kitty S312 | FP kitty S312 | ok | ok |
| V2-H9 status `Mined` | FN kitty S313 | FN | FN | FN |
| V2-H10 12-cell row | ok (silent) | ok (lists S314) | ok (silent) | ok (lists S314) |
| V2-H11 non-UTF-8 note | e1 (want 2) | e2 ok | e1 (want 2) | e2 ok |
| V2-H12 no host-tree cell | FP kitty S316 | FP kitty S316 | ok | ok |
| V2-H13 `(unused)` in config cell | judg kitty S317 | judg | judg kitty S317 | judg kitty S317 |
| V2-H14 `REJECTED` in config cell | judg kitty S318 | judg | judg kitty S318 | judg kitty S318 |
| V2-H15 double-space id | FN kitty S319 | ok | FN kitty S319 | ok |
| V2-X1 bookkeeping-only 3/3 | judg 3/3 e0 | judg 3/3 e0 | judg 3/3 e0 | judg 3/3 e0 |
| V2-X2 substring names only | FP x3, e0 | ok e1 | ok e1 | ok e1 |
| V2-P1a kitty (unused) first cell | ok | ok | ok | ok |
| V2-P2a other date | ok | ok | ok | ok |
| V2-P3a rejected status | ok | ok | ok | ok |
| V2-P4a source names other terminal | ok | ok | ok | ok |
| V2-P5a prose outside table | ok | ok | ok | ok |
| V2-P5d list item | ok | ok | ok | ok |
| P10b unknown revision | e2 ok | e2 ok | e2 ok | e2 ok |
| P13 no REV argument | e2 ok | e2 ok | e2 ok | e2 ok |

Note on V2-P0: the v2-shaped control reaches 3/3 at every counter (exit 0). It confirms the positive path, and its schema is the one v2 requires.

## 7. Residual risk and verification gaps

- The probes are synthetic fixtures in the scratch clone only. No corpus-wide replay was run for the v1 or v3 candidates. The candidates were checked on the base revisions a28e48 and 4de44647, where the real 122-row registry parses without error and the count is 0/3, exit 1.
- The lane's own C2 after-value is not observed: no note exists at 4de44647, so no after-measurement is claimed here.
- Not probed: underscore and Unicode boundary cases such as `foot_notes`. Not probed: a real upstream row for each terminal, which needs real registry rows. Not probed: decode under a non-UTF-8 locale for the v2 `text=True` path.
- The judgment items (8, 9, 10) need an L1 decision. The annotation words and the bookkeeping-only 3/3 are not closed by any candidate.
- Out of scope and not run: the eleven selftest suites, the corpus comparator and the C1 and C3 counters.
- Lane writes: only this report. Lane git was used read-only (`rev-parse`, `log`, `merge-base --is-ancestor`, `diff --stat`, `show` via the counters). No jj command was run.
- Receipts: `RevC2Counter-work/` holds `build_probes.py`, `build_v2.py`, `run_all.py`, `count_fixed.py`, `count_v3.py`, `probes.json`, `probes_v2.json`, `results_all.json`, `count-fix.patch` and `count-v3.patch`. Clone at `/fast/scratch/hyaku/mado-r23/RevC2Counter`; worktrees at `RevC2Counter-fix`, `RevC2Counter-v2` and `RevC2Counter-v3`.

Verdict: v2 (4de44647) closes P4b, P4c (substring names), P4d (two-terminal source) and the substring-only 3/3 exploit, and adds a host-tree cell rule. It leaves open P5b, P5c, P6b, P6c, P7a, P8a, P8b, P10a, P9d, P9e, P1b, P3b and P6a (silent), and adds V2-H6 (fork-path prefix). The v3 candidate clears every structural hole in the probe set, and is not landed. Bookkeeping-only 3/3 (V2-X1) and annotation words (V2-H13, V2-H14) remain for L1 to decide.
