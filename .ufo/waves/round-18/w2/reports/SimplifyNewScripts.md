# SimplifyNewScripts — dead code and duplicated helpers

Report: `.ufo/waves/round-18/w2/reports/SimplifyNewScripts.md`
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Measured revision: `4c103b55b1ea5c3c555884afe3eb69b5189701b7`
Scope: the seven round-18 scripts named in the item, read at the committed
blobs. I edited no lane file; the only lane write I made is this report.
Scratch copies live in `/tmp/r18-*`.

All line numbers below are line numbers of the **committed** blob at
`4c103b5`, extracted with `git show 4c103b5:<path>`. Two files were being
edited by their wave-2 owners while this review ran (see §5); the committed
bytes did not move.

Committed hashes (verified equal to the worktree at first read; later drift
noted in §5):

| file | sha256 |
|---|---|
| `.ufo/waves/round-18/receipt-check.py` | `5aec6154085c22cd8de34ec32d8ffdb29e783955ab52c6282d25344f559dc7b2` |
| `.ufo/waves/round-18/fetch-verify.py` | `f0e91f10649685544d534e4610302f2180a5ac42a92ffde5d154af6ec2cc10e3` |
| `.ufo/waves/round-18/frozen-provenance-check.py` | `5ee0791b6bdb46b1f753b1589908b3b875202e6eb16bcaf787eeafe36f2c8e74` |
| `.ufo/waves/round-18/pipe-rc-census.py` | `cb150cb2f9df6ddb4d80df37256b463ec5f4822790ede91543ff977b908a4564` |
| `.ufo/waves/round-18/measure-mutants.py` | `075815bd5bbcf80fbf00a80ac9400ff9ec82082562a6691c1f5cc290da601d73` |
| `.ufo/waves/round-18/harm-watch.sh` | `a256d28c7b43ad28c24c0bf97bffda57ba2ff5feadbf6c042686c180779db6c7` |
| `.ufo/waves/round-18/recut-receipts.sh` | `d4a9eafd8c4f0fd247faf09ffcb281926ac5d49f73828e710fedc01e043d46ff` |

Summary: 11 dead-code findings — A1-A11: 4 zero-reference constants and 2
unused parameters, 1 dead disjunct, 5 unreachable branches/checks, 1 dead
local state, 1 constant evidence field — plus 12 duplicated-helper or
duplicated-contract findings, 7 checked-and-not-dead traps, and no unused
imports or zero-use shell names in any of the seven files. The heaviest
duplication is the `RECEIPT` header dialect (two writers, one parser, three
implementations) and the six-times-repeated pin/run block in `harm-watch.sh`.

---

## 1. Dead code

### 1.1 Zero-reference module symbols

| # | file:lines | unit | proof | effect of deletion |
|---|---|---|---|---|
| A1 | `pipe-rc-census.py:45-47,51` | `SINKS`, `FILE_READERS`, `WRAPPERS`, `WORD_AT` | AST pass: each has **0** `Name(Load)` references. Their values are re-inlined in the regex literals at `:61-66` (`timeout|xargs|env|command|sudo|nice|stdbuf|tmo`, `sha256sum|wc|cut`, `sha256sum|wc|cat|head`). `WORD_AT` has no inlined twin; it is unused outright. | source-only; no output change. |
| A2 | `pipe-rc-census.py:363-366` | dead `or '&&' in body` disjunct; redundant `re.search(r'\|\|', body)` on `:365` | `_status_consumed("v=$(foo && bar)")` returns `None`; `_status_consumed("v=$(foo || bar)")` returns `pipeline-fallback`. With no `'||'` in the body, `tail` is `''` and line 365's first conjunct is false, so the `&&` term can never reach the return on 366. When the term is reached via `'||'`, the second `re.search` is tautologically true. | no input changes classification; `&&`-only path already returns `None`. |
| A3 | `pipe-rc-census.py:432-446` | unused parameter `path` of `scan_text` | AST unused-param scan: `scan_text` never loads `path`; sole call site `:504` passes it. | internal only; one caller updated. |

### 1.2 Unreachable branches and checks

| # | file:lines | unit | proof | effect of deletion |
|---|---|---|---|---|
| A4 | `receipt-check.py:93-96` | `try/except Exception` around `body.decode("utf-8", errors="replace")` | `receipt_bytes` returns only `bytes` (`Path.read_bytes()` at `:67`, `subprocess` stdout at `:60`). With `errors="replace"` the only exception `decode` raises for bytes (UnicodeDecodeError) cannot occur; observed `b"\xff\xfe".decode("utf-8","replace")` returns replacement chars, no exception. | returns the same `text`; the `ERROR` arm was unreachable. |
| A5 | `fetch-verify.py:102-106` | `cells[2] if len(cells) > 2 else ""` and `cells[6] if len(cells) > 6 else ""` | Guard `:102` continues unless `len(cells) >= 8`; therefore both ternaries are statically always the true arm. | identical `source`/`anchor`; the comment on `:101` already fixes the indices. |
| A6 | `fetch-verify.py:57` + `:201-203` | unused parameter `seat` of `verify_receipt` | AST unused-param scan: body never loads `seat`; the caller passes it, and the caller separately stores `"seat": seat` at `:210`. | internal only; drop argument and call-site value. |
| A7 | `fetch-verify.py:208-215` | appending non-`ok` receipts to local `receipts` | The only consumer is `verified = [e for e in receipts if e["status"] == "ok"]` at `:221`; row joins (`:226`) and quotes (`:246-...`) read only `verified`. Every non-`ok` entry is appended and never read. | memory only; append can be conditional on `status == "ok"`. |
| A8 | `measure-mutants.py:506-510` | `if head != BASELINE_REV` | `BASELINE_REV` is a full 40-hex sha; `git rev-parse --verify <full-sha>` echoes it. Observed in the lane: `git rev-parse --verify d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` → the same string, rc 0. `subprocess.run(..., check=True)` already raises on a missing revision, so the compare can never fire. | keep the `rev-parse` presence check; drop the compare. |
| A9 | `measure-mutants.py:583` | `'baselines_agree': True` in the summary | The field is a literal. The disagreement path is `baseline_assert` (`:401-417`), which raises `SystemExit` before the summary exists. No assignment can set it false. | the summary schema changes; the committed `evidence/measure-mutants.json` records `"baselines_agree": true` as if measured. Do not delete without re-issuing the evidence (see §6). |
| A10 | `recut-receipts.sh:123` | `[ -n "$full" ]` after `full=$(git ... rev-parse ...) \|\| refuse` | A successful `rev-parse --verify --quiet <rev>^{commit}` prints one non-empty 40-hex sha; the `\|\| refuse` already handles failure. | none. |
| A11 | `recut-receipts.sh:461-463` | `[ "$summary_rc" -eq 2 ]` branch | The summary heredoc ends with `sys.exit(0 if all_identical else 1)` (`:458`) and has no other `sys.exit`. An unhandled Python exception exits 1; a missing interpreter is 127. `refuse`'s exit 2 belongs to the shell function, not this process. | none; the `refuse "recut summary could not be produced"` message is unreachable. |

### 1.3 Write-only state (dead to every decision, not to the evidence)

These are not code-deletion candidates: they are payload the JSON receipt
records. They are listed because no comparison, assertion, or exit code reads
them, so a reader should not mistake them for measured controls.

| # | file:lines | fields | proof |
|---|---|---|---|
| A12 | `measure-mutants.py:333,336-338,350,353` | `c2.score`, `c2.u_routes`, `c1`, `c3_present`, `cmd`, `stdout_sha256` | Each key is written once and read nowhere; `c1` also occurs as a substring of the `TIGHT_SHA` hex literal, which is not a reference. `compare()` reads only `covered`, `count`, `exit`; `expectation_met()` reads `rejected`; the summary reads `bites`, `tight_only`, `expectation_met`. `stdout` (`:356`) is a diagnostic fallback when JSON parsing fails and is never read by the harness. |
| A13 | `recut-receipts.sh:143-144` | `[ -n "$blob_sha" ]` and the `EMPTY_SHA` guard | Line 143 is reachable only if `cut` fails (its rc is unchecked); `git show`/`sha256sum` failures are already refused at `:137-142`. Line 144 is the actual F10 control and must stay. |

`receipt-check.py`'s `PENDING-L1` (`:88-89`) and `WORKTREE` (`:64-70`) are
**not** dead: `receipt-claims.json` uses `PENDING-L1` 6 times and `WORKTREE` 3
times (measured with `json.load` on the committed claims file).

---

## 2. Duplicated helpers and duplicated contracts

| # | duplicated unit | sites (committed lines) | notes |
|---|---|---|---|
| D1 | `sha256_file(path)` streaming helper | `fetch-verify.py:49-54`; `frozen-provenance-check.py:74-79` | Same algorithm; only `path.open("rb")` vs `open(path,"rb")` and `fh` vs `f` differ. The only true cross-file helper duplicate in the seven scripts. |
| D2 | hash of bytes / hex digest idiom | `receipt-check.py:103` (`hashlib.sha256(blob).hexdigest()`); `measure-mutants.py:55-56` (`sha256_bytes`); `recut-receipts.sh:342` (`hashlib.sha256(text.encode())`); plus the two file helpers in D1 | Five hash primitives for one convention. D1+D2 is a shared module candidate; §6 explains why that trade is bad here. |
| D3 | "read a blob at a revision" wrapper | Python: `receipt-check.py:54-60` (`git_show`), `pipe-rc-census.py:449-452` (`_git`), `measure-mutants.py:59-62` (`git`). Shell: `recut-receipts.sh:121,134-147`; `harm-watch.sh:125-148`. | Same subprocess idiom, five shapes. Only `recut-receipts.sh:134-147` checks the producer rc via `PIPESTATUS`; `harm-watch.sh` uses `git cat-file -e` then `git show` to a temp file. The other three Python wrappers treat nonzero rc as "unreadable" (which is correct for them) but do not expose rc. |
| D4 | `RECEIPT` header dialect (writer/parser) | Writer 1: `harm-watch.sh:87-100` (`RECEIPT tool=... tool_sha256=... measured_commit=... utc=... cwd=... argv=`). Writer 2: `recut-receipts.sh:179` (`RECEIPT tool=... tool_sha256=... measured_commit=... utc=... cmd=`). Parser: `receipt-check.py:47-51` + `:73-83` (only keys at line start: `^\s*tool_sha256...$`, `^\s*measured_commit...$`). | Three implementations, and the parser matches **neither** producer: both writers put the keys inline after `RECEIPT tool=...`, so the anchored regexes fail on the shared line. This is the highest-value duplication finding; the fix belongs to the wave-2 `ReceiptCheckFix` owner (`gen_w2.py:79`), not to a simplifier. |
| D5 | receipt file-name list | `recut-receipts.sh:55` (bash array); `:205-206` (join heredoc); `:361-362` (summary heredoc) | Three sources of truth. Adding a sixth receipt means editing three lists in one file. |
| D6 | `MADO_RECUT_*` environment envelope | pass/read at `recut-receipts.sh:192-194` ↔ `:201-203`; repeated at `:347-349` ↔ `:357-359` | The same three values are marshalled twice to two separate Python processes. `JOIN_SUMMARY` shows the existing one-envelope pattern that could carry all of it once. |
| D7 | first-`{`-line JSON extraction from a receipt | `recut-receipts.sh:72-78` (`receipt_files` heredoc) vs `:366-375` (`parse` in summary heredoc) | Both scan lines, strip, take the first line starting `{`, `json.loads` it; `parse` additionally tolerates `ValueError`. Two parsers of one receipt format in one file. |
| D8 | receipt pre-validation loop | `recut-receipts.sh:149-154` vs `:157-164` | Identical `receipt_files` call plus emptiness check. The first pass runs 5 extra Python subprocesses and is redundant with the second: `OUTDIR` is not written until `:470-473`, so a bad input already leaves the output untouched. |
| D9 | pinned run block | `harm-watch.sh:169-182` (gate), `:185-198` (action-plan), `:261-274` (measure U) are the same 14-line shape; variants `:231-258` (tripwire loop), `:279-310` (nav), `:313-332` (fleet census) | `pin_assert` → `pin_log` → `begin` → `timeout` → `end_out` → `record_result`, with `pin_log` duplicated in **both** arms: `:170/179`, `:186/195`, `:232/247`, `:262/271`, `:317/329`. Each executed command is additionally re-spelled as a summary string: `ARGV` at `:171`, `:187`, `:263`, `:318`; `SUITE_ARGV` at `:220` versus the executed command at `:238-240`. The summary copy interpolates `$ROOT`/`$rel` unquoted while the executed copy quotes them, so the receipt argv can drift from what ran. A `run_pinned FILE TOOL ARGV...` helper covers the three scalar blocks; the three variants need their own shape. |
| D10 | first field of `sha256sum` | `harm-watch.sh:132`, `:138`, `:287` (`sha256sum ... \| cut -d' ' -f1`); `recut-receipts.sh:125-126`, `:168-169` (`$(sha256sum ...)` then `${var%% *}`) | Five sites, two idioms, one operation. |
| D11 | SOURCES.md row parser | `fetch-verify.py:100-108` (`len(cells) >= 8`, uses cells 1/2/6) vs `measure-mutants.py:148-153` + `:195-205` (`len(cells) == 13`, edits cell 11) | The table is 11 columns (`corpus/SOURCES.md:12-13`, `line.split("|")` yields 13 cells). Both encode the same shape with different strictness: fetch accepts a short row and reads a possibly wrong anchor; measure refuses anything not exactly 13. Same contract, two parsers, no shared code. |
| D13 | could-not-evaluate error envelope | `frozen-provenance-check.py:412-414`, `:426-428`, `:432-434`, `:442-445`, `:452-455`, `:458-461` | Six `return emit("could_not_evaluate", 2, {...})` calls repeat the same `schema`/`outcome`/`exit` envelope around one varying `error` (and sometimes `root`/`provenance`/`index`/`tool_sha256`). A single `fail(error, **extra)` helper would remove five copies. |

---

## 3. Checked and **not** dead (deletion traps)

| file:lines | why it must stay |
|---|---|
| `measure-mutants.py:420-431` (`archive_member(member, dest)`) | `dest` is unused, but the tarfile extraction filter is called as `filter_function(unfiltered, path)` — verified by `inspect.getsource(tarfile.TarFile._get_extract_tarinfo)`. Dropping the second parameter raises `TypeError` before extraction. This is the one unused parameter that must not be "cleaned". |
| `measure-mutants.py:441` (`tar.extractall(repo, filter=archive_member)`) | The filter's `None` return is a documented skip, not an error; the symlink-skip rationale in the docstring is live. |
| `receipt-check.py:64-70,88-89` | `WORKTREE` and `PENDING-L1` are live claim modes (3 and 6 claims). |
| `recut-receipts.sh:137-142,144` | The `PIPESTATUS` capture and `EMPTY_SHA` refusal are the F10 fix under test; removing either would recreate the defect M3 records. |
| `pipe-rc-census.py:386` | `re.fullmatch(r'[0-9]+[a-z]?', t) and t.endswith('s')` is **not** dead: it matches `10s`/`5s`. It is suspicious (for `timeout 10s sha256sum "$f"` the next token returned is `sha256sum`, so the guard sees no `$`), but it is a behaviour question, not dead code. Leave for a behavioural ticket. |
| `frozen-provenance-check.py` (whole file) | No zero-use module names, no unused imports, no unused parameters. The alias-tolerant `pick`/`normalise_*` paths are the documented schema contract, not dead branches. |
| `receipt-check.py:47-51` | The anchored header regexes are load-bearing (D4); do not delete as "unused" just because the current producers do not match them. |

---

## 4. Caller analysis (deletion safety at the code level)

`grep` for all seven file names under `tools/` (and the lane's `scripts/`,
which does not exist) returned **no matches**: no lane tool sources, imports,
execs, or dispatches any of these scripts. They are wave-local evidence
artifacts.

That is **not** the same as "no callers". The same names are cited by:

- `SKILL.md` registry rows (`mado-receipt-check`, `mado-fetch-verify`,
  `mado-pipe-rc-census`, `mado-measure-mutants`, `mado-frozen-provenance`);
- `SCORECARD.md` C1/C2/C3 commands;
- `.ufo/waves/round-18/drafts/SkillRegistryDraft.md:25-29`;
- reports that quote their sha256 (`w1/reports/FetchVerify.md:9` cites
  `f0e91f10…`; `Evidence/measure-mutants.json:33` records
  `075815bd…`; `harm-watch-summary.txt` cites gate/tripwire shas).

So a helper can be deleted with no *code* caller, but every edit changes the
file's sha256 and re-pins or invalidates at least one cited receipt/registry
row. The cheap deletions are those that keep the file's output byte-identical;
the evidence still needs a re-issue because criterion 24 binds the tool digest,
not the output alone.

---

## 5. Concurrent drift observed during the review

At first read every worktree file matched its committed blob. By the second
check (after the AST and line-range passes):

- `receipt-check.py`: worktree `62d020a9b2690d00…`, committed `5aec6154…`;
- `fetch-verify.py`: worktree `07e7ac7443bc5a3a…`, committed `f0e91f10…`.

Both are owned by wave-2 items `ReceiptCheckFix` and `FetchVerifyFix`
(`.ufo/waves/round-18/gen_w2.py:79-80`), which were editing at the same time.
Findings A4, A5, A6, A7 and D4 refer to the committed bytes only and may be
superseded by those owners. The other five files were still byte-identical to
the committed blobs at the second check.

---

## 6. Recommendation and the stop point

Tier 1 (output byte-identical; the tool digest still moves and the cited
receipt must be re-issued): A1, A2, A3, A4, A5, A6, A7, A8 (keep the
`rev-parse`), A10, A11. These remove 4 zero-use constants, 1 dead disjunct,
2 unused parameters, 1 unreachable `except`, 1 pair of dead ternaries, 1 dead
local append, 1 dead compare, 1 dead guard and 1 dead branch without changing
any printed line or exit code.

Tier 2 (output byte-identical, structural dedup within one file): D5, D6, D7,
D8, D10, D12, and the three scalar blocks in D9. D11 and D4 should not be
"consolidated" by a simplifier: D11 changes acceptance strictness, D4 is an
active wave-2 repair with a different owner.

Tier 3 (do not delete): A9 and A12. `baselines_agree` and the write-only
fields are part of the receipt payload. Removing them changes the committed
`measure-mutants.json` schema and the claim surface criterion 25 reads; that
harms the evidence axis without removing any runtime work.

Cross-file deduplication (D1-D3) is **not** recommended for the wave scripts
as they stand. One shared module would either live outside the seven paths and
acquire a sha none of the receipts name, or change all seven shas at once;
the per-file digest pin is the point of criterion 24. The duplication is the
price of independent, individually pinned evidence tools.

Stop point: the next candidate after Tier 1/2 is the receipt-payload schema
(A9/A12) or the cross-file module; both trade evidence integrity for a smaller
diff. That trade is worse on the axis the round is measuring.

---

## 7. Commands run and observed output

1. Extract and hash the committed blobs (worktree compared at the same time):

```
for f in receipt-check.py fetch-verify.py frozen-provenance-check.py \
         pipe-rc-census.py measure-mutants.py harm-watch.sh recut-receipts.sh; do
  git show 4c103b55b1ea5c3c555884afe3eb69b5189701b7:.ufo/waves/round-18/$f \
    2>/dev/null > /tmp/r18-$f && sha256sum /tmp/r18-$f .ufo/waves/round-18/$f
done
```

Result: all seven pairs identical at first read (hashes in the table above).

2. AST zero-use / unused-parameter / unused-import scan on the committed
   copies (`/tmp/r18-*.py`), Python 3 (summarised output of the scan):

```
ZERO union:  pipe-rc-census.py SINKS:45-45 FILE_READERS:46-46 WRAPPERS:47-47 WORD_AT:51-51
UNUSED-PARAM: fetch-verify.py verify_receipt 57-86 ['seat']
UNUSED-PARAM: pipe-rc-census.py scan_text 432-446 ['path']
UNUSED-PARAM: measure-mutants.py archive_member 420-431 ['dest']
UNUSED IMPORTS: none in all five Python files
```

3. Dead-disjunct falsification (`_status_consumed` imported from the
   committed `pipe-rc-census.py`):

```
'foo && bar' -> None
'foo || bar' -> pipeline-fallback
'foo || true' -> None
```

Only the `'||'` term can yield a verdict; `'&&'`-only bodies already fall
through to `None`, so `or '&&' in body` (`:363`) contributes no path.

4. `rev-parse` fixed-point check for A8:

```
$ git rev-parse --verify d9a5a18e17cd3a68b52148fcc01c4a30e340ba98
d9a5a18e17cd3a68b52148fcc01c4a30e340ba98
rc=0
```

5. Decode replacement check for A4:

```
$ python3 -c 'print(repr(b"\xff\xfe".decode("utf-8","replace")))'
'\ufffd\ufffd'
```

No exception; `except Exception` at `receipt-check.py:95` has no bytes input
that can reach it.

6. tarfile filter arity for the `archive_member` trap:

```
$ python3 -c 'import tarfile,inspect; print(inspect.getsource(tarfile.TarFile._get_extract_tarinfo))'
...
filtered = filter_function(unfiltered, path)
```

The filter is called with two positional arguments; `dest` is protocol, not
dead.

7. Caller search (no semantic callers):

```
workspace grep tool, pattern 'receipt-check|fetch-verify|frozen-provenance|pipe-rc-census|measure-mutants|recut-receipts|harm-watch'
paths: tools/;scripts/
-> No matches found. Skipped missing paths: .../mado-shokunin/scripts
```

8. Shell write-only scan on `harm-watch.sh` and `recut-receipts.sh`
   (assignment/function definitions vs references): no `ONLY-DEFINED` names;
   every shell variable and function has at least one reference. The shell
   dead weight is duplication (D5-D10, D12), not unreferenced names.

9. SOURCES table shape check for D11:

```
$ sed -n '1,20p' corpus/SOURCES.md
...
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|----|--------|------|------|-------|--------|---------|--------|--------|---------|---------|
```

11 columns; `split("|")` → 13 cells; `fetch-verify` accepts `>= 8` and reads
cells 1/2/6, `measure-mutants` requires exactly 13 and edits cell 11.

10. Second hash check (drift, §5):

```
receipt-check.py worktree 62d020a9… vs committed 5aec6154…
fetch-verify.py  worktree 07e7ac74… vs committed f0e91f10…
```

I made no edits to any lane file. No package-manager, service, compositor,
input, screenshot, browser, or REA command was run. The only git commands were
read-only `show`, `rev-parse`, `cat-file`, and `ls-tree` inside the lane.
