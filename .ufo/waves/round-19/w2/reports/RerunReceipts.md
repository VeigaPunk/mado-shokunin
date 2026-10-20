# MadoR19.RerunReceipts — breaks

Item under attack: the round-19 receipt bundle — `receipt-claims.json`, the six committed receipt
files under `evidence/`, and the header test "`tool_sha256` equals `git show <measured_commit>:<tool>`".
Read at the integrated tip `01b80946d92b26370d3012a7da655d00dd135154`. My only lane write is this
report; the worktree now also carries sibling wave-2 edits (`SCORECARD.md`, `corpus/QUALITY.md`,
`landed-check.sh`, `supersessions.json`, `fetch/.gitignore`) that I did not make, so every citation
below was re-derived at `01b8094` with `git show`, not from a moving worktree line number.

Verdict: the **red arm holds and round-18's own 33/33 holds**, but the round-19 claims file is
**false against itself at the tip**: two claims declare `expect: "ok"` and print `ERROR` under the
checker that file names (`EXPECT_SUMMARY: 3/5`, exit 2). The named remedy is not committed, and the
one copy of it that exists (`/tmp` lab) converts a `SHA_MISMATCH` into `ok` — it buys the credit by
dropping criterion 24's defining equality. Separately, a checker-compatible fix **already sits in
the tree** (the recut receipts), so the "structural, no claim shape can credit it" premise is false
at tip.

## 1. The two assigned runs

```
$ python3 -I .ufo/waves/round-18/receipt-check.py .ufo/waves/round-19/receipt-claims.json
RECEIPT r19-c26-redbefore-headerless MISSING_PROVENANCE
RECEIPT r19-c26-regression-recut-headerless MISSING_PROVENANCE
RECEIPT r19-tw-recall-before ERROR
RECEIPT r19-fresh-pins-before ERROR
RECEIPT r19-measure-before ok
EXPECT_SUMMARY: 3/5
EXIT=2
```

```
$ python3 -I .ufo/waves/round-18/receipt-check.py .ufo/waves/round-18/receipt-claims.json
RECEIPT r18-fixture-bad-sha SHA_MISMATCH
RECEIPT r18-fixture-stale-rev SHA_MISMATCH
RECEIPT r18-fixture-stale-tool STALE
RECEIPT r18-fixture-nonancestor NOT_ANCESTOR
RECEIPT r18-fixture-producer-mismatch PRODUCER_MISMATCH
... 28 further lines all `ok` ...
EXPECT_SUMMARY: 33/33
EXIT=0
```

Every non-`ok` line accounted for:
- round-18 file: 5 non-`ok` lines, all deliberate controls whose declared `expect` matches the
  printed token (hence 33/33). No finding.
- round-19 file: 2 `MISSING_PROVENANCE` are the declared red arm (`.ufo/waves/round-18/evidence/gate-rc-redbefore.txt`,
  `regression-recut.txt`) — **twice independently confirmed red**: both are byte-identical at
  `9c54c56`, `17661e0` and the worktree (`d69f9b55a4a61789…`, `643e927173a400b0…`) and carry
  `grep -cE 'tool_sha256|measured_commit|^RECEIPT'` → `0`.
- round-19 file: the 2 `ERROR` lines are the finding (F1).

## 2. Header census — every r19 receipt vs `git show <measured_commit>:<tool>`

28 files under `evidence/` carry a `RECEIPT` header (6 top-level + 22 under `harm/`).
**24 MATCH, 4 ABSENT, 0 digest-mismatch.** Method: `git cat-file -e $rev:$tool` first, then
`git show $rev:$tool | sha256sum`; a failed `cat-file` is reported **ABSENT**, never as a digest —
the pipeline alone would have printed `e3b0c442…`, which is the sha256 of empty input, not of a file
(criterion 26's own hazard; the round-18 checker's `git_show` returns `None` for the same reason).

ABSENT (the four that fail the assigned test):

| receipt | measured_commit | why |
|---|---|---|
| `evidence/tw-recall-before.txt` | `9c54c56` | tool first committed at `17661e0`; not in git at the measured rev |
| `evidence/fresh-pins-before.txt` | `9c54c56` | same |
| `harm/harm-census-validate.txt` | `fleet:fc05a552…` | `REV` regex needs 40 hex; `fleet:` is not a lane revision, and the tool is `…/scripts/sources-census.sh`, outside the lane |
| `harm/harm-nav-fleet-round-1.txt` | `01b8094` | `tool=…/SCORECARD.md#Counting-command` is a *block* id, not a path; its `tool_sha256` is the block digest (`block_sha256=8b59b503…` in the body), so no blob can equal it |

MATCH includes `gate-swap-receipt.txt` (`6e6782c3…` = the committed fixture at `df84807`) and both
recuts (`22090298…`/`a094be01…` at `df84807`). Two more `evidence/` files carry no `RECEIPT` header:
`census-before.txt` (tracked, cited as a baseline receipt — F6) and the harm roll-ups
`harm-watch-pins.txt` (`PINS schema=…`) / `harm-watch-summary.txt` (tabular).

## 3. Falsifications

### F1. The committed claims file does not meet its own declared expectations at the tip
`receipt-claims.json:47` and `:56` say `"expect": "ok"`; the run prints `ERROR` for both, so
`EXPECT_SUMMARY: 3/5`, **exit 2**. The file's own `tool_rev_semantics` (`:15`) states the
unmodified checker "returns ERROR for the two such claims", so the failure is disclosed — but the
declared expectation is what the checker's `EXPECT_SUMMARY` counts, and 2/5 declarations are unmet.
The file names its checker at `:5` (`".ufo/waves/round-18/receipt-check.py"`); no round-19 checker
exists (`ls .ufo/waves/round-19/` → no `receipt-check.py`).

### F2. The remedy is not committed — 5/5 exists only in a /tmp lab
```
$ git show 01b8094:.ufo/waves/round-18/receipt-check.py | grep -c tool_rev
0
```
So no runnable artifact in the lane produces 5/5. Reproduced the w1 demonstration independently in
my own clone (`git clone --shared` → `/tmp/r19verify`, checkout `01b8094`, the report's exact diff
applied with `patch -p1`, fuzz 1/2/1 as reported):

```
== r19 claims, patched ==   EXPECT_SUMMARY: 5/5   EXIT=0
== r18 claims, patched ==   EXPECT_SUMMARY: 33/33 EXIT=0
```
`ReceiptClaims19.md:105-107` is therefore honest about *what the patch does*. F3 is about what it
costs.

### F3. The patch buys the credit by dropping criterion 24's equality; the stated invariant is false
Criterion 24 (`corpus/QUALITY.md:131`, same line number at `01b8094` and in the worktree) defines the bar as "`tool_sha256=` equal to
`git show <measured_commit>:<tool> | sha256sum`". The patch replaces the `measured` read with
`tool_rev` (`receipt-check.py:148` becomes `blob = git_show(tool_rev, …)`), while
`if bind == measured: return "ok"` (`:153-154`) still skips the second read. So when a claim declares
`bind_rev == measured` and `tool_rev == rev`, the **only** tool read is at `tool_rev`, and the
`measured_commit` equality is never evaluated. Demonstrated in the clone with a synthetic receipt
whose header digest is the tip gate (`1036d1…`) while `measured_commit=17661e0` (whose gate is
`c9fb0cef…`):

```
== ORIGINAL checker ==   RECEIPT lie-bind-measured SHA_MISMATCH     EXPECT_SUMMARY: 0/1 EXIT=1
== PATCHED checker  ==   RECEIPT lie-bind-measured ok               EXPECT_SUMMARY: 1/1 EXIT=0
$ git show 17661e0:tools/mado-verify.sh | sha256sum  → c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5
$ git show 01b8094:tools/mado-verify.sh | sha256sum  → 1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af
```
`ReceiptClaims19.md:46` claims the opposite: "the identity chain is unchanged in strength: the header
digest must equal the tool bytes at `tool_rev` **and** at the binding revision (`bind`, default
`rev`)". Two independent refutations:
1. the configuration above returns `ok` with **zero** reads at `measured_commit`;
2. for the lane's actual two claims, `tool_rev == bind == rev == 17661e0`, so the two reads are the
   same revision. Logged with a `git` shim on `PATH` for `r19-tw-recall-before`:
   ```
   show 17661e0fa83f978fb659f5bb8fef47f0969f6945:.ufo/waves/round-19/tw-recall.py
   show 17661e0fa83f978fb659f5bb8fef47f0969f6945:.ufo/waves/round-19/tw-recall.py
   distinct revs for tool reads: 1
   ```
   Two calls, one distinct revision, one bit of information. "AND at the binding revision" is
   vacuous for the very claims the patch exists to credit.

Consequence for the round: adopting `tool_rev` makes the criterion-24 check unable to assert what
criterion 24 says. A claim labelled `ok` would no longer mean "`tool_sha256` equals the tool at
`measured_commit`"; for `r19-tw-recall-before` it would mean "equals the tool at `17661e0`", where
the measurement at `9c54c56` used an uncommitted worktree file.

### F4. "No claim shape the current checker understands can credit a split tool/measurement provenance" is false at tip
`ReceiptClaims19.md:45` asserts the gap is structural. But wave 1 also committed recut receipts, and
they credit under the **unmodified** checker — I only had to point a claim at them and at a readable
revision:

```
$ python3 -I .ufo/waves/round-18/receipt-check.py /tmp/r19probe/recut-at-tip.json
RECEIPT recut-tw-at-01b8094 ok
RECEIPT recut-fresh-at-01b8094 ok
EXPECT_SUMMARY: 2/4   (the 2 misses are probes I deliberately mis-shaped: ERROR / PRODUCER_MISMATCH)
```
The claims file was never re-pointed at them, so the round ships the fix and not the claim.

### F5. The recuts are unreadable at the claims' declared revision and cited by nothing
```
$ .../receipt-check.py /tmp/r19probe/recut-at-df.json
RECEIPT recut-tw-at-df84807 ERROR      RECEIPT recut-fresh-at-df84807 ERROR
RECEIPT recut-tw-at-17661e0 ERROR      RECEIPT recut-fresh-at-17661e0 ERROR
EXPECT_SUMMARY: 1/6
```
(the two probe lines not shown are `gate-swap-receipt ok` — the 1 credited — and
`census-before-headerless MISSING_PROVENANCE`).
`receipt_bytes` is absent at both `df84807` and `17661e0` (the recuts commit at `01b8094`), so no
claim reading at `17661e0` can use them. And `grep -rn "recut"` over `corpus/`, `SCORECARD.md` and
the round-19 trees finds **no** sentence citing `tw-recall-before-recut.txt` or
`fresh-pins-before-recut.txt` (LogDraft cites the originals at `w1/reports/LogDraft.md:13-14`).
They are dead evidence: bodies byte-identical to the originals (`diff` apart from line 1), header
only.

### F6. A headerless receipt sits inside round-19's own evidence and is cited as a baseline
`evidence/census-before.txt` is tracked at the tip, has `grep -cE 'tool_sha256|measured_commit|^RECEIPT'`
→ `0`, and records a verdict (`exit=0`, with W04 duplicate warnings). Probe:
```
RECEIPT census-before-headerless MISSING_PROVENANCE
```
It is cited as one of the four baseline receipts (`w1/reports/LogDraft.md:13`,
`drafts/LogDraft.md:5`). This is precisely the R18-V2 defect class the round claims to have applied
criterion 24 to — now in round-19's own `evidence/`, and outside the 5-claim set.

### F7. The whole harm-watch receipt family is uncreditable by criterion 24's runnable check
All 22 `harm/` receipts name the producer by **absolute** path
(`tool=/home/vgpnk/Projects/shokunin/mado-shokunin/tools/…`). The checker uses `claim["tool"]` as the
`git show` path, so:
```
RECEIPT harm-gate-selftest-wt ERROR            (claim tool = absolute path → not a git path)
RECEIPT harm-gate-relative-spelling PRODUCER_MISMATCH  (claim tool lane-relative → ≠ header token)
RECEIPT harm-census-external MISSING_PROVENANCE        (measured_commit = "fleet:fc05a552…", not 40 hex)
RECEIPT harm-nav-fragment-tool PRODUCER_MISMATCH
```
Both spellings fail, so the receipts are true-but-uncreditable: 20 of 22 verify by manual
lane-relative strip, and none can pass criterion 24 as written. This matters because the family
carries the round's harm-watch numbers (`harm-gate-selftest.txt:2` → `MADO_SELFTEST: 443/443
assertions passed`, `harm-action-plan-selftest.txt:55` → `52/52`, tripwire 16+9+33+30+31+1+45+13+34+18+17).
The receipts are untracked at the tip (wave 2 in flight — expected, not a defect), but the *format*
defect survives committing. `harm-watch-summary.txt` itself is consistent (`commands=22 failures=0`,
21 `OK` + 1 `BASELINE exit=1` for the deliberately-mismatched round-18 frozen baseline, with the
`frozen_verdict_mismatch` token recorded at `harm-tripwire-frozen-round-18.txt:2`).

### F8. `gate-swap-receipt.txt` is mechanically ok but does not bind the d9a5a18 gate
Header resolves exactly (`6e6782c3…` = committed `evidence/gate-swap-d9a5a18.sh`, `measured_commit=df84807`),
and the receipt's splice provenance is independently true:
`git show d9a5a18:tools/mado-verify.sh | sed -n '3402,3415p' | sha256sum` → `414bf6ed…` and
`git show 17661e0:… | sed -n '3467,3489p' | sha256sum` → `c86f51b8…`, both exactly as line 2 states.
But the producer is a fixture under `evidence/`, not the gate:
`git show d9a5a18:tools/mado-verify.sh | sha256sum` → `fba82a66…` ≠ `6e6782c3…`; retargeting the
claim's `tool` to `tools/mado-verify.sh` prints `PRODUCER_MISMATCH`. The fixture is the d9a5a18 gate
plus the OM9 stub-rc knobs and the OM9 selftest block (`diff` shows only those additions), and the
receipt records `MADO_SELFTEST: FAILED — 383 passed, 6 failed`, `exit=2`.
So `QUALITY.md:196` / `lessons/round-19.md:19` are accurate about the tool and the outcome, but "the
header-bound re-cut" overstates: it is a **new red run on a hybrid fixture**, and criterion 26's
actual cited red-before (`gate-rc-redbefore.txt`) still prints `MISSING_PROVENANCE` and still has no
header. Note also the hole this exposes in the criterion-24 check: a receipt naming its own sibling
fixture satisfies `git show <measured_commit>:<tool>` trivially, with no binding to any tool under
`tools/`.

## 4. What holds (attack failed here)

- Round-18's own claims: 33/33, exit 0, reproduced from committed bytes.
- The red arm: both receipts headerless, byte-identical at `9c54c56`/`17661e0`/worktree, both print
  `MISSING_PROVENANCE` as declared.
- The `tool_rev` lab claim itself (`ReceiptClaims19.md:96-101`): 5/5 and 33/33 reproduce exactly,
  same fuzz, and round-18's 33/33 is genuinely unchanged by the patch.
- `measure-before.json.txt` credits under the unmodified checker (`measure.py` = `de4c422b…` at both
  `9c54c56` and `17661e0`).
- The receipts' own "(tool not yet committed)" annotation is **true**, contrary to
  `LogDraft.md:22`'s Finding 1: receipt `utc=2026-10-20T16:59:29Z` = `13:59:29-03:00`, and the tools
  first appear in `17661e0` at `13:59:52-03:00` — 23 s later. (Adjacent seat's item; recorded because
  it bears on receipt consistency. The receipts are internally consistent.)
- All splice/block digests in `gate-swap-receipt.txt` verify; the harm-watch tallies are internally
  consistent.

## Limits

- I did not run the gate in any mode (host pause). No statement here depends on a gate execution;
  F8 rests on bytes, digests and the receipt's own recorded output.
- The `tool_rev`/`sha-mismatch→ok` demonstration used a synthetic receipt committed **in my own /tmp
  clone** (`/tmp/r19verify`, rev `caa9eb0…`); no lane file was created, edited or committed. The
  lane was read with `git show`/`cat`/`sha256sum` only.
- I did not enumerate every `evidence/`-adjacent artefact (e.g. `gate-swap-d9a5a18.sh` is a tool, not
  a receipt); the census covers files whose first line begins `RECEIPT`.
- F7's "uncreditable in both spellings" is measured against this checker's code
  (`receipt-check.py:128-158`); a future checker could resolve absolute paths — [INFERENCE] that is
  what it would take.
- Whether L1 adopts `tool_rev`, re-points the claims at the recuts, or leaves 3/5 declared is a
  decision, not a measurement. [UNK]
- The 22 `harm/` receipts are untracked at `01b8094` (wave 2 in flight); I assume they are meant to
  be committed in the wave-2 integration — [INFERENCE].

## Installs

none. (No package, service, or tool was installed or upgraded; nothing was fetched with curl.)
