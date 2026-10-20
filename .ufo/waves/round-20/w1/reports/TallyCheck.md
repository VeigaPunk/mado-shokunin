# TallyCheck — criterion-30 checker built: all 5 red statements MISMATCH (155→154; 5/13→6/13 in SCORECARD, lesson and LOG; ten→9) with 0 ERROR, and its committed derivations reproduce every closure figure (154; 6/13 and 8/13; 9 occurrences, 8 distinct; 390/370→461/440)

## Files written

| file (lane-relative) | sha256 | shape |
|---|---|---|
| `.ufo/waves/round-20/tally-check.py` | `1ce05aa0aab392e67148dbaa9a08d46ba7c2aa2cc093b853ef6c2b6f0905f572` | 912 lines, stdlib only, untracked |
| `.ufo/waves/round-20/tally-claims.json` | `79ac2191760b948eee3ebc47cdc49758cc8a9095307a53a346e1e5ebd2a87334` | 109 lines, `red` 5 entries, `green` `[]` |
| `.ufo/waves/round-20/w1/reports/TallyCheck.md` | — | this report |

- I built and ran everything in the /tmp clone `/tmp/mado-r20-TallyCheck` (observed HEAD `e629f731172b8238caffe50f152217ce56535fb4`). I copied the two files in, and `git status --short` there shows only those two untracked files.
- The lane copies hash to the same sha256 values as the clone copies.
- In the lane I ran only read-only `git show`, `git log`, `git diff`, `git grep` and `git rev-parse`. No jj command and no git write was run.
- Fixture code and transcripts were never executed.

## The red run, ready for L1 to recut

Run from the clone root:

`python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json` → **exit 1**

```
TALLY_REGISTRY: .ufo/waves/round-20/tally-claims.json sha256=79ac2191…87334 set=all rev=-
MISMATCH r19-lesson-155-transcripts stated=155 derived=154
  set=red expect=MISMATCH statement corpus/lessons/round-19.md:124@1f7f995c… | key=files | derive: python3 -I .ufo/waves/round-20/tally-check.py receipt-files --rev 1f7f995c… --path .ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt
MISMATCH r19-scorecard-c2-5of13-s096 stated=5 derived=6
  set=red expect=MISMATCH statement SCORECARD.md:1167@1f7f995c… | key=first_line | derive: … pointer-token --counter .ufo/waves/round-19/fresh-pins.py --counter-rev 1f7f995c… --rev 1f7f995c… --token S096
MISMATCH r19-lesson-c2-5of13-s096 stated=5 derived=6     (corpus/lessons/round-19.md:108)
MISMATCH r19-log-c2-5of13-s096 stated=5 derived=6        (LOG.md:1324)
MISMATCH r19-scorecard-ten-om10 stated=10 derived=9      (SCORECARD.md:1225, key=removed_occurrences)
TALLY_SUMMARY: set=all n=5 match=0 mismatch=5 error=0
EXPECT_SUMMARY: 5/5
```

The other two modes behave as follows:
- `--set red --expect` exits 0 (every red is on its side, 5/5).
- `--set green` exits 2 (`TALLY_REGISTRY_ERROR: … no entries in set green`). An empty set is never a vacuous pass.

## Derived numbers and how each was computed

### 1. lesson "155 round-19 transcripts" → **154**

- **Statement:** `corpus/lessons/round-19.md:124@1f7f995` reads "155 round-19 transcripts, `--permit tool_install`): …". It was introduced by `c7693eb`, the same commit as the receipt (`git log -S`).
- **Derivation:** `receipt-files --rev 1f7f995… --path .ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt`.
  - The command reads the committed receipt bytes (sha256 `9572d2a655d1e06aef73b4e87edb713e9486be1f0e9a8f92ed98bb42830e3139`).
  - The receipt must hold exactly one JSON line with `"schema":"mado-tripwire-verdict-v1"` and a `files` list. It does: line 7 of 8, 116,610 bytes.
  - The derived value is `len(files)`.
- **Output:**
  - `files=154`, `distinct_paths=154`, `jsonl_paths=154`, `pathless_entries=0`.
  - Header: `tool=tools/mado-tripwire.py`, `tool_sha256=367be947…`, `measured_commit=0fa41252…`, `utc=2026-10-20T18:29:35Z`.
  - `counts={"host_mutation":0,"live_probe":3,"package_query":0,"tool_install":0,"vcs_write":164}`.
- `git log` on the receipt path shows only `c7693eb`, so the bytes are identical at every revision from c7693eb to e629f73.
- **Not part of the derivation (names and mtimes only, no transcript content read):**
  - The live `…/MadoR19/` directory now lists 308 entries: 154 `.jsonl` plus 154 `.md`.
  - The 154 `.jsonl` names are the same set as the receipt's 154 basenames.
  - 12 of them have an mtime later than the scan's 18:29:35Z; all 12 were already scanned.
  - So 155 is supported neither by the receipt nor by the current directory. Where 155 came from is `[UNK]`.

### 2. "5/13 name S096 on the crediting line" (SCORECARD:1167, LOG:1324) and "5 of 13 credited files name S096 on the crediting line" (lesson:108) → **6/13** first-matching-line (any-line **8/13**)

**Derivation:** `pointer-token --counter .ufo/waves/round-19/fresh-pins.py --counter-rev 1f7f995… --rev 1f7f995… --token S096`. The file set is re-derived from the counter's own committed text:
- The counter `fresh-pins.py@1f7f995` (sha256 `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789`; single commit `17661e0`) is parsed with `ast` and never executed.
- From it the command takes `PIN_REV=9c54c56…`, `OLD=2.17.0` and `POINTER=2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2`.
- The counter's `in_scope` must be AST-identical to the copy in tally-check.py, otherwise exit 2.
- **Denominator:** in-scope paths at PIN_REV whose bytes contain `2.17.0` → `denominator=13`.
- At `--rev`, a file's pointer lines are its lines that match POINTER, numbered with `str.splitlines()` exactly as the counter numbers them.
- `first_line` counts files whose first pointer line contains `\bS096\b`. `any_line` counts files with S096 on any pointer line.

Output at `1f7f995`: `current=13/13 first_line=6/13 any_line=8/13`.

| file | first pointer line | S096 on it | S096 pointer lines |
|---|---|---|---|
| SKILL.md | 573 | yes | 573,1853,1855,1856,1858,1860,1861,1862,1864,1865 |
| corpus/README.md | 44 | no | 137,138 |
| arc-synthesis.md | 392 | no | — |
| closeout-r11.md | 299 | no | — |
| config-health-report-r3.md | 1009 | no | — |
| remaining-planes-census.md | 338 | yes | 338 |
| walker-deep-r9.md | 403 | yes | 403,412 |
| walker-deep.md | 622 | yes | 622 |
| walker-live-surface.md | 305 | yes | 305,312 |
| walker-route-r18.md | 1 | no | 328 |
| waybar-walker-plane.md | 479 | no | — |
| waybar-walker-semantics.md | 467 | no | — |
| tools/mado-verify.sh | 56 | yes | 56,67,104,1329,1997,3364 |

These are the closure's sets exactly (`round-19-verifier-spotcheck.md:59,61`): the same eight any-line files, six first-line files, and five files with S096 on no pointer line.

**This contradicts the closure's "snapshot-stale" framing.** I ran the same command at more revisions:

| revision | first_line | any_line |
|---|---|---|
| `01b8094` (the snapshot RerunC2 measured) | 6/13 | 7/13 |
| `61eaa07` (where the statements land) | 6/13 | 8/13 |
| `daf6543`, `b435568`, `1f7f995`, `e629f73` | 6/13 | 8/13 |

So "5/13 name S096" was never the token count at any of these revisions. It equals RerunC2's semantic tally at 01b8094 (`RerunC2.md:71`, "S096 cited as evidence 5/13"):
- That tally excludes the two "denied/reserved" pointers (remaining-planes-census:338, walker-live-surface:305).
- It counts walker-route-r18 through :328, which is not that file's first pointer line.

The red is therefore a definition mismatch: a semantic count was restated as a token claim.

### 3. SCORECARD "the ten old OM10 assertions" → **9** occurrences (**8** distinct)

**Derivation:** `selftest-labels --path tools/mado-verify.sh --function selftest --fail-helper st_bad --old 9c54c56… --new 7b4839d… --label-regex '^OM10(?![0-9A-Za-z])'`.

- The `selftest() { … }` body is tokenized as shell text. Quotes, `$( )`, `${ }`, backticks, comments and continuations are handled, and here-document bodies are skipped.
- Each helper's label position is derived by following its body down to `st_bad`, whose label is `$1`. The result is the same at both revisions: `st_bad:1, st_counts_agree:2, st_eq:1, st_has:1, st_not_has:1, st_row_detail:5, st_row_exact:5, st_row_has:4, st_rows:1`. `st_ok` has no label.
- A labeled assertion is a call to one of those helpers in the body, outside helper definitions.
- The derived value is the multiset difference old − new, restricted to the OM10 label id.

| revision | block | blob sha256 | occurrences | distinct |
|---|---|---|---|---|
| 9c54c56 | 393–1590 | `c9fb0cef…` | 390 | 370 |
| 7b4839d | 416–1883 | `050efc72…` (= SCORECARD's gate `050efc72…`) | 461 | 440 |

The totals are the closure's own figures (`spotcheck.md:88`).

- **Removed:** `removed_occurrences=9`, `removed_distinct=8`, `removed_unmatched_occurrences=0`, `removed_all_occurrences=9`. Every removed label is OM10, so "no other prior assertion lost" holds at the label level.
- **The nine removed occurrences, with old line numbers:**
  - 839 `OM10 (describe rc=128 is unverified)`
  - 840 `OM10 (rev-parse rc=128 is unverified)`
  - 841 and 842 `OM10: the UNKNOWN names the rc` (the duplicate, hence 8 distinct)
  - 843 `OM10 (show succeeds; the comparison still runs)`
  - 844 `OM10: no false tag MOVED`
  - 845 `OM10: no false head MOVED`
  - 846 `OM10: exactly two omarchy UNKNOWNs (tag + head)`
  - 848 `OM10: counts agree with rows`
- **Added:** `OM10A:6, OM10B:8`, matching the closure's "OM10A six + OM10B eight".
- **Parser validation across revisions:** source occurrences equal recorded runtime + 1 at every gate revision, where the +1 is the closure's mutually exclusive R10 branch:

  | revision | source | runtime (SCORECARD) |
  |---|---|---|
  | 9c54c56 | 390 | 389 |
  | 01b8094 | 444 | 443 |
  | 61eaa07 | 453 | 452 |
  | 7b4839d | 461 | 460 |

- **Why lines are not counted:** `git diff 9c54c56 7b4839d -- tools/mado-verify.sh | grep -c '^-.*OM10'` gives **10**, because one removed line is the `# --- OM10:` banner comment (`grep -vc st_` on those lines gives 1). That is the CriticTally cheat that would MATCH "ten". The derivation counts labeled helper calls, so it cannot reach 10. A wider `--label-regex` still gives 9, because it can only pick from the removed multiset.

## What the checker pins

The brief's schema and exit codes are kept as written. CriticTally (`w1/reports/CriticTally.md`, received mid-build) raised attacks; each one below was cheap and harms nothing, so I took it.

- **Stated number comes from the text:** a `(?P<stated>…)` group in `line_regex` is **required** and must equal `stated`. Digits are accepted, as are number words zero to twenty ("ten" parses as 10). Anything else is ERROR.
- **Exactly one matching line:** zero matching lines gives ERROR "statement absent"; more than one gives ERROR "ambiguous".
- **Pinned revisions:** every registry revision, including every value after `--rev/--counter-rev/--old/--new` in argv, is 40-hex or `REV`. `REV` takes the checker's `--rev`, which is resolved and printed in the `TALLY_REGISTRY` line. This lets a corrected statement be registered before its commit exists. Branches and short hashes give ERROR.
- **No ad hoc commands:** derive argv must be `python3 -I .ufo/waves/round-20/tally-check.py <receipt-files|pointer-token|selftest-labels> …`. The checker runs it as `sys.executable -I <this file> …`, with cwd = lane and a 300 s timeout.
- **Named counts only:** `extract_regex` must begin `(?m)^<key>=` with a key the subcommand declares (`COUNT_KEYS`), and must match stdout exactly once. A digit taken from a label, hash or timestamp is rejected. A literal `/13` in both regexes binds the denominator; changing it to `/14` gave ERROR.
- **No self-certification:**
  - A `--path/--counter` equal to the statement file gives ERROR.
  - A `--token` that does not occur as a word in the statement line gives ERROR; swapping in S090 on the S096 line was refused.
- **Polarity:**
  - `EXPECT_SUMMARY: k/n` is always printed (red→MISMATCH, green→MATCH).
  - `--expect` makes the exit code follow it: 0 only if every entry is on its side.
  - Default exit codes are exactly the brief's: 0 all MATCH, 1 any MISMATCH, 2 any ERROR, a malformed registry or an empty set.
- **Read-only:** every subcommand reads committed bytes only, through `git rev-parse/show/ls-tree` with `GIT_OPTIONAL_LOCKS=0` and lane-relative paths (`..`, absolute paths and a leading `-` are refused).

## Adversarial checks run

All ran in the clone, against registries under `/tmp/mado-r20-TallyCheck-tests/`.

| case | result |
|---|---|
| `stated` 154 over the "155" line | ERROR `stated=154 but the statement says '155'` |
| `stated` 9 over "ten" | ERROR, the statement says 'ten' |
| argv `bash -c echo files=155` / `python3 -c print(...)` | ERROR, argv shape |
| extract from `header_utc` / unanchored `files=(\d+)` | ERROR, extract_regex must begin `(?m)^<key>=` |
| statement rev `refs/heads/master` / `1f7f995` | ERROR, neither 40-hex nor REV |
| short rev inside derive argv | ERROR |
| `line_regex` without a stated group / matching 100+ lines | ERROR, no group / ambiguous |
| statement rev where the file or line is absent | ERROR, `git show … exited 128` / statement absent |
| receipt-files `--path` = statement file | ERROR, derive reads the statement file itself |
| `--token S090` on the S096 line | ERROR |
| `/14` denominator in extract | ERROR, extract matched 0 times |
| `--label-regex 'OM10\|^A:\|^R1'` | MISMATCH, still 9 (cannot inflate) |
| `REV` statement without `--rev` | ERROR, pass --rev |
| duplicate id, boolean `stated` | ERROR |
| a red entry that MATCHes, hidden among 5 reds | default exit 1 (per the brief), `EXPECT_SUMMARY: 5/6`, `--expect` exits 1 |
| non-JSON registry; `--rev deadbeefdeadbeef` | exit 2 |
| subcommand: non-counter `--counter`; `--function nosuch`; non-receipt path; `--rev --output=/tmp/x`; `--path ../etc/passwd` | exit 2 each; `/tmp/x` not created |

**Green path:** five test entries were written over the closure's own true statements in `corpus/lessons/round-19-verifier-spotcheck.md`, with `statement.rev: "REV"` and `--rev 1f7f995…`:
- "154 files" (`files`)
- "8/13" (`any_line`)
- "6/13" (`first_line`)
- "nine … occurrences" (`removed_occurrences`)
- "(eight distinct)" (`removed_distinct`)

All five MATCH, giving exit 0 and `EXPECT_SUMMARY: 5/5`. Without `--rev` all five ERROR. These were test registries only; I did not add them to `green`.

## Notes for L1

- **Five red entries, one more than the brief named.** `r19-log-c2-5of13-s096` (LOG.md:1324) is outside the brief's SCORECARD/lesson list. I added it because `git grep` at 1f7f995 found it as a third copy of the same stale claim, and CriticTally argues for one entry per stating file. Drop it if the criterion should name exactly four.
- **Template for a green entry:**
  - `statement: {"rev": "REV", "path": <corrected file>, "line_regex": <text naming its counting rule, with (?P<stated>…)>}`.
  - Reuse the red entry's derive, swapping the key where needed: `any_line` or `first_line`, `removed_occurrences` or `removed_distinct`.
  - Run `--set green --rev <commit>`.
  - Corrected prose should spell its rule, e.g. "first matching line" or "labeled occurrences". The checker cannot enforce that (see Limits).
- CriticTally cites `round-19.md:110` for "5 of 13". At 1f7f995 the line is **108**, per both `git grep -n` and the checker's statement location.
- **Outside the registry:** SCORECARD's "the 9 added since [443]" is a net figure. The label diff 01b8094→61eaa07 shows 10 added and 1 removed. The removed label is the in-round `WL: no row still names the old 2.17.0 pin` at 01b8094:1291, so the 9→452 baseline claim still holds. I did not check why it was dropped `[UNK]`.

## Limits

- The shell tokenizer covers a subset of bash. It does not handle `case … )` inside `$( )`, quote characters inside comments within `$( )`, parentheses inside `[[ =~ ]]` patterns, or a here-document opened inside a multi-line quoted span. I validated it only on `tools/mado-verify.sh` at 9c54c56, 01b8094, 61eaa07 and 7b4839d (source = runtime + 1 each time, and equal to the closure's 390/370 and 461/440).
- The checker cannot tell whether prose names its counting rule; that stays with the reviewer, `note` and `line_regex`. The red statements give no counting rule, by nature.
- There is no contra-sweep: a stale line kept beside its correction at REV is not flagged. This is consistent with the lane's append-only records.
- If a future fresh-pins `in_scope` changes, `pointer-token` exits 2 by design.
- `--expect`, `EXPECT_SUMMARY`, the `TALLY_REGISTRY` header line and the indented detail lines are additions beyond the brief's output contract. The MATCH/MISMATCH/ERROR line format and the default exit codes are exactly as specified.
- Not run: tw-precision, tw-recall, the gate (any mode), the tripwire suites, measure.py. No QUALITY or SCORECARD text was written (that is L1's job).
- No transcript content was read; for the MadoR19 directory I looked at names and mtimes only. Host files were not read.

## Installs

none
