# TallyCheck — criterion-30 checker built: all 5 red statements MISMATCH (155→154; 5/13→6/13 in SCORECARD, lesson and LOG; ten→9) with 0 ERROR, the derivations reproduce every closure figure, and the critic's numerator/denominator false-green is now refused

## Files written

| file (lane-relative) | sha256 | shape |
|---|---|---|
| `.ufo/waves/round-20/tally-check.py` | `21ce9dd57a47d975623aa9ca2bf53c3dadb8fa68b6f066a92461edba2fd2aea4` | 1020 lines, stdlib only, untracked |
| `.ufo/waves/round-20/tally-claims.json` | `eaa5a151983173dcad402f1152c7b0bc5841ac07158e4560b5c93c549c342ab1` | 108 lines, `red` 5 entries, `green` `[]` |
| `.ufo/waves/round-20/w1/reports/TallyCheck.md` | — | this report |

- I built and ran everything in the /tmp clone `/tmp/mado-r20-TallyCheck` (observed HEAD `e629f731172b8238caffe50f152217ce56535fb4`).
- `git status --short` there shows only the two untracked files.
- The lane copies hash to the same sha256 values.
- In the lane I ran only read-only `git show`, `git log`, `git diff`, `git grep` and `git rev-parse`. No jj command and no git write was run. Fixture code and transcripts were never executed.

The build went through two passes:
- **Pass 1** (`1ce05aa0…`) was re-attacked by `CriticTally` (`w1/reports/CriticTally.md`). It found one live false-green and several looser pins.
- **Pass 2** (this file) closes them; see "What the checker pins".

## The red run, ready for L1 to recut

Run from the clone root:

`python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json` → **exit 1**

```
TALLY_REGISTRY: .ufo/waves/round-20/tally-claims.json sha256=eaa5a151…42ab1 checker_sha256=21ce9dd5…2aea4 set=all rev=-
MISMATCH r19-lesson-155-transcripts stated=155 derived=154
  set=red expect=MISMATCH statement corpus/lessons/round-19.md:124@1f7f995c… claim="155 round-19 transcripts" | key=files | derive: python3 -I .ufo/waves/round-20/tally-check.py receipt-files --rev 1f7f995c… --path .ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt
MISMATCH r19-scorecard-c2-5of13-s096 stated=5/13 derived=6/13
  set=red expect=MISMATCH statement SCORECARD.md:1167@1f7f995c… claim="13/13 pointed; 5/13 name S096 on the" | key=first_line | derive: … pointer-token --counter .ufo/waves/round-19/fresh-pins.py --counter-rev 1f7f995c… --rev 1f7f995c… --token S096
MISMATCH r19-lesson-c2-5of13-s096 stated=5/13 derived=6/13   (corpus/lessons/round-19.md:108)
MISMATCH r19-log-c2-5of13-s096 stated=5/13 derived=6/13      (LOG.md:1324)
MISMATCH r19-scorecard-ten-om10 stated=10 derived=9          (SCORECARD.md:1225, key=removed_occurrences, --label-id OM10)
TALLY_SUMMARY: set=all n=5 match=0 mismatch=5 error=0
EXPECT_SUMMARY: 5/5
```

The other two modes:
- `--set red --expect` exits 0 (every red is on its side).
- `--set green` exits 2 (`no entries in set green`). An empty set is never a vacuous pass.

## Derived numbers and how each was computed

### 1. lesson "155 round-19 transcripts" → **154**

- **Statement:** `corpus/lessons/round-19.md:124@1f7f995`. It was introduced by `c7693eb`, together with the receipt.
- **Derivation:** `receipt-files --rev 1f7f995… --path .ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt`.
  - It reads the committed receipt (sha256 `9572d2a655d1e06aef73b4e87edb713e9486be1f0e9a8f92ed98bb42830e3139`).
  - The receipt must hold exactly one JSON line with `"schema":"mado-tripwire-verdict-v1"` and a `files` list; it does, at line 7 of 8.
  - The derived value is `len(files)`.
- **Output:**
  - `files=154`, `distinct_paths=154`, `jsonl_paths=154`, `pathless_entries=0`.
  - Header: `tool_sha256=367be947…`, `measured_commit=0fa41252…`, `utc=2026-10-20T18:29:35Z`.
  - `counts={"host_mutation":0,"live_probe":3,"package_query":0,"tool_install":0,"vcs_write":164}`.
- `git log` on the receipt shows only `c7693eb`, so the bytes are identical through e629f73.
- **Not part of the derivation (names and mtimes only, no content read):**
  - The live `…/MadoR19/` directory lists 154 `.jsonl` plus 154 `.md` files.
  - Its `.jsonl` names are the same set as the receipt's 154 basenames.
  - 12 have an mtime after the scan time, and all 12 were scanned.
  - So 155 is supported by neither the receipt nor the directory. Where it came from is `[UNK]`.

### 2. "5/13 name S096 on the crediting line" (SCORECARD:1167, LOG:1324) and "5 of 13 credited files name S096 on the crediting line" (lesson:108) → **6/13** first-matching-line (any-line **8/13**)

**Derivation:** `pointer-token --counter .ufo/waves/round-19/fresh-pins.py --counter-rev 1f7f995… --rev 1f7f995… --token S096`.
- The counter `fresh-pins.py@1f7f995` (sha256 `a094be01…`; single commit `17661e0`) is parsed with `ast` and never executed.
- From it the command takes `PIN_REV=9c54c56…`, `OLD=2.17.0` and `POINTER=2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2`.
- The counter's `in_scope` must be AST-identical to the copy in tally-check.py, otherwise exit 2.
- **Denominator:** in-scope paths at PIN_REV containing `2.17.0` → 13.
- Pointer lines are numbered with `str.splitlines()`, as the counter numbers them.
- `first_line` counts files whose first pointer line contains `\bS096\b`; `any_line` counts files with it on any pointer line. Both are printed as N/13.
- **The claim's denominator is also checked.** The statement's `(?P<den>13)` must equal the derived 13, so a changed file set reads MISMATCH.

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

These match the closure's sets exactly (`round-19-verifier-spotcheck.md:59,61`).

**Contradicts the closure's "snapshot-stale" framing.** I ran the same command at more revisions:

| revision | first_line | any_line |
|---|---|---|
| `01b8094` (RerunC2's snapshot) | 6/13 | 7/13 |
| `61eaa07` | 6/13 | 8/13 |
| `daf6543`, `b435568`, `1f7f995`, `e629f73` | 6/13 | 8/13 |

So 5/13 was never the token count. It is RerunC2's semantic "S096 cited as evidence **5/13**" (`RerunC2.md:71`):
- That tally excludes the two "denied/reserved" pointers.
- It counts walker-route-r18 through :328, which is not that file's first pointer line.

The stale claim is a definition mismatch, not only a snapshot.

### 3. SCORECARD "the ten old OM10 assertions" → **9** occurrences (**8** distinct)

**Derivation:** `selftest-labels --path tools/mado-verify.sh --old 9c54c56… --new 7b4839d… --label-id OM10`.

- The `selftest()` body is tokenized as shell text: quotes, `$( )`, `${ }`, backticks, comments and continuations are handled, and here-document bodies are skipped.
- Each helper's label position is derived by following its body down to `st_bad`, whose label is `$1`. The result is the same at both revisions: `st_bad:1, st_counts_agree:2, st_eq:1, st_has:1, st_not_has:1, st_row_detail:5, st_row_exact:5, st_row_has:4, st_rows:1`. `st_ok` has no label.
- A labeled assertion is a call to one of those helpers outside helper definitions.
- The result is the multiset old − new, restricted to labels whose leading id is exactly `OM10`. OM10A and OM10B are different ids.

| revision | block | blob sha256 | occurrences | distinct |
|---|---|---|---|---|
| 9c54c56 | 393–1590 | `c9fb0cef…` | 390 | 370 |
| 7b4839d | 416–1883 | `050efc72…` (= SCORECARD's gate) | 461 | 440 |

The totals are the closure's figures (`spotcheck.md:88`).

- **Removed:** `removed_occurrences=9`, `removed_distinct=8`, `removed_other_id_occurrences=0`, `removed_by_id=OM10:9`. Every removed label is OM10, so "no other prior assertion lost" holds at the label level.
- **The nine removed occurrences, with old line numbers:**
  - 839 `OM10 (describe rc=128 is unverified)`
  - 840 `OM10 (rev-parse rc=128 is unverified)`
  - 841 and 842 `OM10: the UNKNOWN names the rc` (the duplicate, hence 8 distinct)
  - 843 `OM10 (show succeeds; the comparison still runs)`
  - 844 `OM10: no false tag MOVED`
  - 845 `OM10: no false head MOVED`
  - 846 `OM10: exactly two omarchy UNKNOWNs (tag + head)`
  - 848 `OM10: counts agree with rows`
- **Added:** `OM10A:6, OM10B:8`.
- **Parser validation across revisions:** source occurrences equal recorded runtime + 1 at every gate revision, where the +1 is the closure's mutually exclusive R10 branch:

  | revision | source | runtime (SCORECARD) |
  |---|---|---|
  | 9c54c56 | 390 | 389 |
  | 01b8094 | 444 | 443 |
  | 61eaa07 | 453 | 452 |
  | 7b4839d | 461 | 460 |

- **Why lines are not counted:** `git diff 9c54c56 7b4839d -- tools/mado-verify.sh | grep -c '^-.*OM10'` gives **10**, because one removed line is the `# --- OM10:` banner comment. That is the cheat that would MATCH "ten". This derivation counts labeled calls, so it cannot reach 10.

## What the checker pins

The brief's schema and default exit codes are kept. Every pin below was cheap and harms nothing, so I took it. Pass 2 additions are marked **(P2)**.

**The claimed number is read from the statement text:**
- A `(?P<stated>…)` group is required and must equal `stated`. Number words zero to twenty are accepted ("ten" parses as 10).
- **(P2)** The stated number must be a standalone token, not digits inside `S096`, `OM10`, `round-19` or `2.17.2`.
- **(P2) Fraction claims** (keys `current`/`first_line`/`any_line`, printed as N/D):
  - `line_regex` also needs `(?P<den>…)`, standalone, with only "/" or "of" between the two groups.
  - MATCH requires both N and D to equal the derived N/D.
  - For any other key, a `den` group, or a stated number that sits next to "/D" or "N of", is ERROR.
- These rules kill the critic's demonstrated false-green: `of (?P<stated>13) credited files` + `denominator=` → MATCH over the stale "5 of 13".

**Exactly one matching line.** Zero matching lines gives "statement absent"; more than one gives "ambiguous".

**Revisions are pinned:**
- Every registry revision, including derive `--rev/--counter-rev/--old/--new`, is 40-hex.
- `REV` (the checker's `--rev`, resolved and printed) is allowed **only in green entries (P2)**. A red entry always measures its pinned historical staleness.

**Derive commands are restricted:**
- argv is `python3 -I .ufo/waves/round-20/tally-check.py <receipt-files|pointer-token|selftest-labels>` followed by `--flag value` pairs.
- **(P2)** Each flag may appear at most once and must be in `REGISTRY_FLAGS`:
  - receipt-files: `--rev --path`
  - pointer-token: `--counter --counter-rev --rev --token`
  - selftest-labels: `--path --old --new --label-id`
- **(P2)** Abbreviations, `--flag=value`, CLI-only `--function/--fail-helper` and values starting with `-` are refused. argparse also uses `allow_abbrev=False`.
- The derive runs as `sys.executable -I <this file>` with cwd = lane and a 300 s timeout.

**No self-certification:**
- A `--path/--counter` equal to the statement file gives ERROR.
- **(P2)** Paths must be in canonical spelling, so `./x` cannot bypass that check.
- A `--token` value **and (P2) a `--label-id` value** must occur as a word in the statement line, so the counted family is the one the prose names. **(P2)** `--label-regex` and `--schema` no longer exist.

**Only headline counts are claimable:**
- `extract_regex` must begin `(?m)^<key>=` with a headline key.
- **(P2)** Diagnostics are not claimable: the counter's `denominator`, `pathless_entries`, other-id and all-id label totals.
- **(P2)** The derive's stdout must carry exactly one `<key>=N` (or `N/D`) line, and `extract_regex` must read that same N. Capturing the denominator gives ERROR "reads 13, but the derive printed first_line=6".

**Polarity and provenance:**
- `EXPECT_SUMMARY: k/n` is always printed (red→MISMATCH, green→MATCH).
- `--expect` exits 0 only if every entry is on its side.
- Default exit codes are the brief's.
- **(P2)** The `TALLY_REGISTRY` line carries `checker_sha256` next to the registry sha256.
- **(P2, critic's auditability nit)** Each detail line prints the matched claim text, e.g. `claim="13/13 pointed; 5/13 name S096 on the"`, truncated at 200 characters. A reviewer can see which claim on a multi-claim line was certified.

**Read-only:** every git read is `rev-parse/show/ls-tree` with `GIT_OPTIONAL_LOCKS=0`.

## Adversarial checks run

All ran in the clone, against registries under `/tmp/mado-r20-TallyCheck-tests/`; each is one registry run.

| attack | result |
|---|---|
| **(P2) critic's live false-green:** stated=13 from "of 13", key `denominator` | ERROR, key not claimable |
| … same with key `current` and no den group | ERROR, fraction needs `(?P<den>)` |
| … `(?P<stated>(?P<den>13))` on one span | ERROR, must read N/D or N of D |
| … stated=13 from "of 13" with a non-fraction key | ERROR, stated number sits in a fraction |
| extract_regex capturing the denominator (stated 5) | ERROR, extract reads 13 but key printed 6 |
| stated bound inside `S096` / `round-19` | ERROR, part of a larger token |
| `--label-id OM10` on a line without OM10; `OM10A` on the OM10 line | ERROR, not a word of the statement line |
| keys `all_ids_removed_occurrences`, `removed_other_id_occurrences=0`, `pathless_entries=0` | ERROR, not claimable |
| extract_regex with no group | ERROR |
| duplicate `--token`, `--tok`, `--token=S096`, `--function` in registry, value `-x`, `./corpus/…` self-path | ERROR each |
| red entry with `REV` in the statement or the derive (even with `--rev`) | ERROR, REV is green-only |
| claim "5 of 13" vs derived 6/13 | MISMATCH `stated=5/13 derived=6/13` |
| `stated` 154 over "155"; `stated` 9 over "ten" | ERROR, statement says '155' / 'ten' |
| `bash -c …`, `python3 -c …` argv | ERROR, argv shape |
| key-shopping `header_utc`, unanchored extract | ERROR |
| `refs/heads/master` / short rev | ERROR |
| no stated group; regex matching 109 lines; absent statement; derive reading the statement file; `--token S090` | ERROR each |
| duplicate id; boolean `stated`; non-JSON registry; unknown `--rev` | ERROR / exit 2 |
| a red entry that MATCHes, hidden among 5 reds | default exit 1 (brief), `EXPECT_SUMMARY: 5/6`, `--expect` exit 1 |

**Green path:** six test entries at `statement.rev: "REV"`, run with `--rev 1f7f995…`. All six MATCH, giving exit 0 and `EXPECT_SUMMARY: 6/6`:
- Five over the closure's own true statements: "154 files"; "8/13" with `any_line`; "6/13" with `first_line`; "nine … occurrences" and "(eight distinct)" with `--label-id OM10`.
- One over the honest "13/13 pointed" claim at SCORECARD:1167, with `current`.

These are test registries only; I did not add them to `green`.

## Notes for L1

- **Five red entries, one more than the brief named.** `r19-log-c2-5of13-s096` (LOG.md:1324) is outside the brief's SCORECARD/lesson list. I added it because `git grep` and CriticTally both found it as a third copy of the same stale claim, following one entry per stating file. CriticTally's closing advice (`CriticTally.md`) is to keep it, since completeness wants one entry per stating file rather than a fixed count. The decision is L1's: drop it if the criterion must name exactly four.
- **Template for a green entry:**
  - Statement: `{"rev": "REV", "path": <corrected file>, "line_regex": <phrase naming the counting rule, with (?P<stated>…) and, for N/D, (?P<den>…)>}`.
  - Reuse the red derive with the intended key: `first_line` or `any_line`, `removed_occurrences` or `removed_distinct`, `files`.
  - Check with `--set green --rev <commit>`.
- **Report-scope statements, recommend not registering:** `RerunC2.md:71` ("S096 cited as evidence 5/13") and `CriticC2W2.md:11,153`. As derived above, "5/13" was never the S096 token count, so these reports state a different claim (a semantic "cited as evidence" tally) on their own snapshot. CriticTally and I both recommend narrowing the criterion-30 wording to SCORECARD/lesson/LOG instead of registering them. The decision is L1's.
- CriticTally's original citation of `round-19.md:110` for "5 of 13" was off by two; at 1f7f995 the line is **108**, and the critic has corrected it.
- **Outside the registry:** SCORECARD's "the 9 added since [443]" is net. From 01b8094 to 61eaa07, 10 labels were added and 1 removed: the in-round `WL: no row still names the old 2.17.0 pin` at 01b8094:1291. Why it was dropped is `[UNK]`.

## Limits

- The checker does not bind `--path/--counter` values to the prose; a reviewer has to read the printed derive.
- A green entry can certify a different true claim on a line that still carries a stale one. For example, "13/13 pointed" MATCHes on SCORECARD:1167 next to the stale "5/13"; CriticTally reproduced this. The detail line's `claim=` text shows which claim was certified, but rejecting it is a reviewer's call; `line_regex` and `note` must name the intended claim.
- There is no contra-sweep, consistent with the lane's append-only records.
- The checker cannot tell whether prose names its counting rule, beyond the token, label-id and fraction bindings.
- The shell tokenizer covers a subset of bash. It does not handle `case … )` inside `$( )`, quote characters in comments within `$( )`, parentheses in `[[ =~ ]]`, or a here-document opened inside a multi-line quoted span. I validated it only on `tools/mado-verify.sh` at four revisions.
- If a future fresh-pins `in_scope` changes, `pointer-token` exits 2 by design.
- `--expect`, `EXPECT_SUMMARY`, the `TALLY_REGISTRY` line and the detail lines go beyond the brief's output contract, and fractions print as N/D. The MATCH/MISMATCH/ERROR line shape and the default exit codes are as specified.
- Not run: tw-precision, tw-recall, the gate (any mode), the tripwire suites, measure.py. No QUALITY or SCORECARD text was written.
- No transcript content and no host file was read.

## Installs

none
