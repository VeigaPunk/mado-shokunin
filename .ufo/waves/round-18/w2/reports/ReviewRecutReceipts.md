# Review — re-cut tripwire receipts (r13-r16 + anchor), round 18 wave 2

Seat: MadoR18.ReviewRecutReceipts (leaf; no dispatch, no lane write outside this
report). Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Revision pins (everything below is read at these, not at a moving HEAD):

| name | hash | role |
|---|---|---|
| baseline | `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` | round-17 closure |
| integration | `4c103b55b1ea5c3c555884afe3eb69b5189701b7` | `measured_commit` pinned by the receipts |
| receipts | `abfbf35b1ed4d4a1eb294d525ef286be30f3886f` | holds the re-cut receipts and `recut-summary.json` |

Method: read-only git (`show`, `cat-file`, `merge-base`, `diff`, `log`), file
bytes, `sha256sum`, and an in-memory reimplementation of the committed
`receipt-check.py` logic. No lane tool was executed (contract: only
`--selftest`/`--regression` of `tools/mado-verify.sh`, and neither was in
scope). The worktree was being edited by another actor during this review
(§F1); all findings are pinned to the two commits above.

## 0. Answer to the assigned questions

1. **Identical verdict JSON, round 18 vs round 17? Yes — byte-identical, 5/5.**
   Not merely equal counts: the SHA-256 of each round-18 verdict-JSON line equals
   the SHA-256 of the round-17 JSON line, and each round-18 file decomposes
   exactly as `RECEIPT line + <round-17 file verbatim> + "exit=1\n"`.
2. **Each `RECEIPT` header's `tool_sha256` equals
   `git show <measured_commit>:tools/mado-tripwire.py | sha256sum`? Yes — 5/5,
   with `git show` rc 0.** All five pin `c87a31ef…`, which is the blob at
   `4c103b55` (and the worktree tool).
3. **Is `measured_commit` an ancestor of `abfbf35…`? Yes**, `merge-base
   --is-ancestor` rc 0; the pinned commit is also self-ancestor (rc 0).

The receipts themselves are cryptographically consistent with the claim. The
actionable defect is in the criterion-24 check that is supposed to certify them
(§F1), not in the five files.

## 1. Receipt identity and provenance — evidence

Per-file facts (all paths lane-relative; `E18` =
`.ufo/waves/round-18/evidence`, `E17` = `.ufo/waves/round-17/evidence`):

| file | r17 JSON sha256 | r18 JSON sha256 | header bytes | r18−r17 bytes | r18 file sha256 |
|---|---|---|---|---|---|
| `tripwire-r13.txt` | `9b372752…` | `9b372752…` | 5173 | 5180 = 5173+7 | `397d294f…` |
| `tripwire-r14.txt` | `11af7800…` | `11af7800…` | 5173 | 5180 = 5173+7 | `62a0b099…` |
| `tripwire-r15.txt` | `3f755282…` | `3f755282…` | 9952 | 9959 = 9952+7 | `192e1664…` |
| `tripwire-r16.txt` | `e357e49a…` | `e357e49a…` | 14738 | 14745 = 14738+7 | `abc106c8…` |
| `tripwire-anchor-r15.txt` | `fddd7dbd…` | `fddd7dbd…` | 442 | 449 = 442+7 | `f6a28708…` |

Full-value digests for the two smallest/edge rows: r13 JSON
`9b372752871d51f09d3409f844144a941f9d62b9090da138afdccf34c00d26ac`; anchor
JSON `fddd7dbde59878996ae995a87b49f0ca6aa05ff4adb03cde5d114ba0f44db6d9`.

Exact decomposition, computed on bytes, all five `decomp_ok True`:
`r18 == header_line + r17_file + b"exit=1\n"` (and `r17` ends with a newline).
Consequences, stated precisely:

- The round-18 bodies are the **whole** round-17 artifacts (label line and JSON),
  not just the JSON object.
- Strictly, "`tripwire-anchor-r15.txt` line 2 onward is identical" is **false as
  a file-range statement**: line 2 onward of the round-18 file is
  `label + JSON + exit=1`, i.e. one line longer than the round-17 file. The
  extra `exit=1` agrees with the JSON's `"exit": 1`; the verdict payload is
  identical.
- All five round-18 files are committed at `abfbf35` with exactly the worktree
  bytes (independent `git show … | sha256sum` equals the on-disk sha for each).
- The round-17 files were not touched by round 18: their blobs at `d9a5a18` and
  at `abfbf35` are identical, and `git diff d9a5a18 abfbf35 --` over the five
  round-17 paths is empty. So "identical to round 17" is against unmodified
  committed round-17 bytes, not a re-cut round-17 file.

Header verification (the exact assigned pipeline, once; all five headers pin the
same producer because they were written by one script run):

```
$ git show 4c103b55…:tools/mado-tripwire.py | sha256sum
c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb  -
$ echo "pipestatus git=${PIPESTATUS[0]} sha=${PIPESTATUS[1]}"
pipestatus git=0 sha=0
$ git merge-base --is-ancestor 4c103b55… abfbf35…
ancestor_rc=0
```

All five header lines begin
`RECEIPT tool=tools/mado-tripwire.py tool_sha256=c87a31ef… measured_commit=4c103b55…`
and carry one `utc=` and one `cmd=` token.

Internal consistency of the recorded command (checked because the round-17
receipts never recorded argv, so this is the re-cut's only replay key):

- `permitted: []` and `unpermitted == len(findings)` in all five verdicts, so no
  `--permit` argument was needed and its absence from `cmd=` is correct.
- The `cmd=` path list equals `files[].path` **in order** for all five
  (33, 33, 65, 97, 1 paths); `counts` sum equals `len(findings)` equals
  `unpermitted` in all five (33, 50, 209, 2, 8).
- The receipt verdicts are `schema mado-tripwire-verdict-v1`, `exit 1`, label
  `MADO_TRIPWIRE: findings`; no `stderr:` block is present, and the tool's
  `--scan` path emits exactly label + JSON (`tools/mado-tripwire.py:822-824` at
  `4c103b55`), so the bodies are shaped as the wrapper documents
  (`recut-receipts.sh:179-188`).

## 2. Findings

### F1 — HIGH: at `abfbf35`, criterion 24's runnable check cannot certify these receipts (two independent causes)

QUALITY 24 (`corpus/QUALITY.md:131-137`) names as its *green* arm "the round-18
re-cut receipts and the frozen-replay receipt". At the receipts commit neither
is demonstrated; both causes are in committed bytes.

**F1a — the committed checker cannot parse the `RECEIPT` header shape.**
`.ufo/waves/round-18/receipt-check.py` at `abfbf35` (sha
`5aec6154085c22cd8de34ec32d8ffdb29e783955ab52c6282d25344f559dc7b2`) uses
line-anchored header regexes (lines 47-48):

```
HDR_SHA = re.compile(rf"^\s*tool_sha256\s*[=:]\s*({HEX64})\s*$", re.M)
HDR_REV = re.compile(rf"^\s*measured_commit\s*[=:]\s*({HEX40})\s*$", re.M)
```

The receipt line begins `RECEIPT tool=…`, so neither regex can match it, and the
JSON fallback (lines 50-51, `"tool_sha256": …` / `"measured_commit": …`) finds
nothing in a `--scan` verdict. Measured on the five committed receipts:

| file | HDR_SHA | HDR_REV | JSN_SHA | JSN_REV |
|---|---|---|---|---|
| `tripwire-r13`..`r16`, `anchor-r15` | False | False | False | False |
| `tripwire-frozen-match` | False | False | True | False |

So `provenance()` returns `(None, None)` for all five re-cut receipts and
`(sha, None)` for the frozen receipt → `MISSING_PROVENANCE` for every one of
them, i.e. the checker reports the exact defect (R17-V1) that the receipts were
cut to remove. This is latent only because the claims do not name them (F1b).
The worktree already contains a rewritten checker (`a2c05fe1…`, mtime
2026-10-20 13:04:20 -0300) whose docstring says it accepts "the shape
recut-receipts.sh writes"; the rewrite is evidence that the committed parser is
wrong, not evidence that the committed one works.

**F1b — the committed claims still hold placeholders that point at files that
do not exist.** `.ufo/waves/round-18/receipt-claims.json` at `abfbf35` (sha
`14aaee0f051788662948510c4faf116f86f44f34a3248405f206bc5a697b0628`, byte-equal
at `4c103b55`) has 15 claims: six round-17 red claims, three authored fixtures,
and six `"rev": "PENDING-L1"` claims whose `receipt` paths are
`.ufo/waves/round-18/evidence/tripwire-{r13,r14,r15,r16,anchor-r15,pacmanlog-join}-recut.txt`
(lines 78-116). All six paths do not exist (`test -e` rc 1 for each); the real
files are `tripwire-r13.txt` etc. There is no claim at all for
`tripwire-frozen-match/tampered/before`.

Executing the committed checker's own logic (faithful reimplementation, since
the lane tool may not be run under this contract) over the committed claims
gives:

```
RECEIPT r17-tripwire-{r13,r14,r15,r16,anchor-r15,pacmanlog-join} MISSING_PROVENANCE   (6 meet)
RECEIPT r18-fixture-{ok,bad-sha,stale-rev} ok / SHA_MISMATCH / SHA_MISMATCH           (3 meet)
RECEIPT r18-recut-tripwire-* PENDING x6                                              (unevaluated)
EXPECT_SUMMARY: 9/15   exit=2
```

This reproduces the w1 seat's recorded Scenario A (`w1/reports/ReceiptCheck.md`,
`EXPECT_SUMMARY: 9/15`, exit 2) — the run is honest, but it is **red**, and it
evaluates none of the five receipts this item reviewed. Filling the placeholder
revs without fixing F1a would print `MISSING_PROVENANCE` for the receipts, not
`ok`.

**Status of the in-flight fix (informational, not mine).** During this review an
uncommitted worktree change replaced both files: `receipt-claims.json` sha
`175e74cd2aad43f35e7c1b7c34c39ad65e5322bf9f07bf4f6464f7539c6334be` (mtime
13:03:37 -0300, 21 claims, `rev=abfbf35` for the eight round-18 receipts,
`bind_rev=d9a5a18` for the frozen-before receipt) and `receipt-check.py` sha
`a2c05fe1…` (mtime 13:04:20). Reimplementing the *new* semantics over the *new*
claims yields `EXPECT_SUMMARY: 21/21 exit=0`, including `ok` for all five
receipts reviewed here. That fix must be committed at/after `abfbf35` and a run
output recorded; until then the committed criterion-24 evidence remains red and
silent about these receipts. I did not write either file.

### F2 — LOW: `recut-summary.json`'s `all_receipts_identical: true` is a verdict predicate, not file identity

`recut-receipts.sh:431-436` defines `identical` as equality of exit, label,
counts, `files_identical`, findings multiset, `permitted`, and `header_ok`; and
`files_identical` (`:422`) compares `file_paths(...)` — **paths only, not the
per-file `sha256`**; `schema` and `unpermitted` are not compared, and the JSON
bytes are never compared. The same summary prints
`round17_receipt_sha256 != recut_receipt_sha256` for all five receipts, so
`all_receipts_identical: true` reads as file identity while meaning
verdict-equivalence. The byte identity I measured is stronger than the summary
asserts; the primary field should be the verdict-body (or whole-body) digest,
and the field should be renamed or documented. No live contradiction: the five
r18 files differ from r17 only by the documented header and `exit=` lines.

### F3 — LOW (latent): `cmd=` is a space-joined argv, not a quoting-preserving argv

`recut-receipts.sh:161` writes `printf '%s\n' "${cmd[*]}"`, while the script's
own docstring (lines 19 and 24) calls it "the exact argv". For today's space-free
session paths the join round-trips exactly (checked: cmd path list equals
`files[]` order), but any path with whitespace or glob characters would make the
recorded command ambiguous and not literally replayable. Cosmetic now; worth
fixing before the receipt is treated as a replay recipe.

### F4 — LOW: the header `utc` dates the wrapper start, not each scan

`recut-receipts.sh:156` captures `utc=$(date -u)` once, before the scan loop, and
reuses it for all five headers and the summary. Observed: all five headers and
`recut-summary.json` carry `Tue Oct 20 15:55:51 UTC 2026`, while the five files
were written at `12:55:53.375-.378 -0300` (= 15:55:53 UTC), i.e. ~2 s later by
the staging `cp`. The stamp is not wrong, but it should not be read as the time
of each measurement.

### F5 — INFO / residual limit: the header is wrapper-authored, not tool-emitted

`tools/mado-tripwire.py` (at `4c103b55`) emits only the label and verdict JSON in
`--scan` mode; its only self-digest is in the frozen payload
(`tool_sha256()`, line 850). Producer identity therefore rests on the wrapper's
statement, which is independently checkable against git (it is, 5/5), not on a
tool-signed emission. Corollary: byte-identical output is exactly what a
successful re-run should produce, and it is also what a byte-faithful copy of
the round-17 file plus a header produces. The artifacts alone cannot distinguish
the two. This does not violate QUALITY 24's text (a committed receipt with the
fields), but it bounds what the receipt can prove: tool bytes and replayability,
not that a process actually executed at the stamped second.

## 3. Residual risk and verification gaps

- I did not execute `tools/mado-tripwire.py` or `receipt-check.py` (contract);
  the checker results in F1 are a reimplementation of the committed source
  (`receipt-check.py` lines 47-105 at `abfbf35`), and the expiry of that
  assumption is the checker source itself, which is quoted.
- I did not read or hash the scanned transcripts (`/home/vgpnk/.omp/agent/...`
  is readable only where an item names a line; this item does not). The verdicts'
  `files[].sha256` are unchanged round to round, which is consistent with
  unchanged inputs, but I did not independently re-hash them.
- `git cat-file -e 4c103b55:.ufo/waves/round-18/evidence/tripwire-r13.txt` returns
  128: the receipt is committed at `abfbf35`, not at the `measured_commit` it
  pins. That is expected under the criterion's `measured_commit`-is-ancestor
  rule and is not a defect, but a naive reader looking for the receipt at
  `measured_commit` will not find it.
- The worktree changed under this review (F1). All statements above are pinned
  to `4c103b55`/`abfbf35`; the uncommitted 21-claim checker pair is reported as
  observed, with its shas and mtimes, not as the reviewed state.
- `tripwire-pacmanlog-join.txt` (the sixth round-17 receipt) is outside this
  item's named file set; I did not evaluate it.

## 4. Commands actually run (representative, with output)

```
# 1. body comparison, per file
diff <(tail -n +2 E18/tripwire-r13.txt) E17/tripwire-r13.txt
3d2
< exit=1                      # only line 3 of the tail (the exit line) is extra
# r14, r15, r16 identical result; anchor identical result

# 2. JSON line digests (r18 line 3 vs r17 line 2), all five pairs equal
sha256sum via sed -n '3p' / '2p'
9b372752… / 11af7800… / 3f755282… / e357e49a… / fddd7dbd…   (pairs identical)

# 3. exact decomposition, all five True
r18 == header_line + r17_file + b"exit=1\n"

# 4. producer digest and status
git show 4c103b55…:tools/mado-tripwire.py | sha256sum
c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb  -
pipestatus git=0 sha=0

# 5. ancestry
git merge-base --is-ancestor 4c103b55… abfbf35…   -> rc 0

# 6. committed evidence equals worktree bytes
git show abfbf35…:E18/tripwire-r13.txt | sha256sum -> 397d294f… (matches disk)
# r14 62a0b099…, r15 192e1664…, r16 abc106c8…, anchor f6a28708… (all match disk)

# 7. round-17 evidence untouched by round 18
git diff d9a5a18 abfbf35 -- E17/tripwire-{r13,r14,r15,r16,anchor-r15}.txt  -> empty

# 8. committed checker cannot parse the header shape
HDR_SHA/HDR_REV/JSN_SHA/JSN_REV over the five receipts -> False/False/False/False
(frozen-match -> False/False/True/False)

# 9. faithful reimplementation over committed (checker, claims) at abfbf35
EXPECT_SUMMARY: 9/15  exit=2
# same over the uncommitted worktree pair:
EXPECT_SUMMARY: 21/21 exit=0

# 10. placeholder targets and mtimes
test -e E18/tripwire-{r13,r14,r15,r16,anchor-r15,pacmanlog-join}-recut.txt -> rc 1 (all six)
receipt-claims.json  mtime 2026-10-20 13:03:37.112 -0300  sha 175e74cd…
receipt-check.py    mtime 2026-10-20 13:04:20.674 -0300  sha a2c05fe1… (committed 5aec6154…)
E18 receipts        mtimes 12:55:53.375-.378 -0300
```

No tool was installed or updated for this review.
