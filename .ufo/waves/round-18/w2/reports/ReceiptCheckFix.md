# ReceiptCheckFix — criterion-24 receipt checker: inline header, rev binding, STALE

Seat: `MadoR18.ReceiptCheckFix` (executor). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`; integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`; receipts `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`.
No lane VCS write of any kind; read-only `git show` / `git rev-parse` /
`git merge-base --is-ancestor` only. No host command, no package query, no gate,
no network. Wrote only the five owned files and this report.

## Axes

- **Calibration:** criterion 24's check now fails the exact R17-V1/V2 shape on
  committed bytes, and passes the honest re-cut — the old checker could not tell
  them apart.
- **Operability:** none — the script is a read-only probe; no gate, tripwire or
  suite is invoked or changed.
- **Provenance:** a receipt can no longer be cited at a later revision than it
  measured; the claim declares either the read revision or the measured one.
- **Discernment:** each new refusal token has a committed-or-authored red control
  and is killed by mutation, so a non-author can see the rule bite.

## 1. Files changed

| path (lane-relative) | sha256 |
|---|---|
| `.ufo/waves/round-18/receipt-check.py` | `a2c05fe194789e49988be957c03394737841f403e5fa9b2d757c4fe2e458e94c` |
| `.ufo/waves/round-18/receipt-claims.json` | `175e74cd2aad43f35e7c1b7c34c39ad65e5322bf9f07bf4f6464f7539c6334be` |
| `.ufo/waves/round-18/receipt-fixtures/stale-receipt.txt` | `c75c2c1209208e9cf1b3750d728cc518ee04557bcc4ee8cb9a39c0278bbb0873` |
| `.ufo/waves/round-18/receipt-fixtures/nonancestor-receipt.txt` | `2d54325356012f5bad8b676cd3c941da34e4653b6f27d4052ed9a84a60ea1f49` |
| `.ufo/waves/round-18/receipt-fixtures/producer-mismatch-receipt.txt` | `60415145cd72d90e77a00ad1c047c619933f283ef3e077207e154e1d01598691` |

Untouched (w1 controls, their bytes still match `w1/reports/ReceiptCheck.md`):
`ok-receipt.txt` `04b431ff…`, `bad-sha-receipt.txt` `2018ca40…`,
`stale-rev-receipt.txt` `6ad4af10…`.

## 2. Behaviour

`python3 -I .ufo/waves/round-18/receipt-check.py [CLAIMS]`

Claim: `{id, receipt, rev, bind_rev?, tool, expect}`, with
`expect ∈ {ok, MISSING_PROVENANCE, SHA_MISMATCH, STALE, NOT_ANCESTOR, PRODUCER_MISMATCH}`.

1. Receipt bytes: `git show <rev>:<receipt>`; `rev: "WORKTREE"` reads the lane
   file (authored fixtures) and then **requires** `bind_rev`; `rev: "PENDING-L1"`
   stays the could-not-evaluate placeholder (exit 2, never credit).
2. Provenance: `tool` (only on a line-1 `RECEIPT` header), `tool_sha256`,
   `measured_commit` — unanchored key/value tokens (`=` or `:`), so the shared
   header line `RECEIPT tool=… tool_sha256=<hex> measured_commit=<hex> …`
   parses, and so do the per-line and JSON `"key": "hex"` forms. Absent sha or
   rev → `MISSING_PROVENANCE`; a line-1 `tool=` naming another producer →
   `PRODUCER_MISMATCH`.
3. `measured_commit` must be an ancestor of (or equal to) the revision the
   claim reads at (`bind_rev` for a WORKTREE read). Otherwise `NOT_ANCESTOR`.
4. `tool_sha256 == sha256(git show <measured_commit>:<tool>)`, else
   `SHA_MISMATCH`.
5. The same tool bytes are required at the binding revision (`bind_rev`,
   default `rev`). Difference → `STALE`. A declared `bind_rev` must be `rev` or
   `measured_commit`; the latter is a before-state receipt that explicitly ran
   the older tool, and any other binding is a malformed claim (`ERROR`).

Output `RECEIPT <id> <status>` per claim then `EXPECT_SUMMARY: k/n`.
Exit 0 all expectations met; 1 all evaluated but some unmet; 2 any
`PENDING`/`ERROR` (unreadable receipt/tool, unresolved commit, malformed claim
or expectation). This matches the committed `SKILL.md:568` exit map; no edit there.

## 3. The three wave-1 defects, each with a differential

### F1 — the checker could not parse the receipt format the fix writes

`recut-receipts.sh` writes provenance on one `RECEIPT …` line; the old checker
anchored `tool_sha256`/`measured_commit` to whole lines, so every re-cut would
have read `MISSING_PROVENANCE`. Fixed by the unanchored token regexes (step 2).

Differential, on the **committed** receipt (old checker = `git show
abfbf35:.ufo/waves/round-18/receipt-check.py` with its `LANE` constant pointed
at the lane, claims `rev=abfbf35`, receipt `evidence/tripwire-r13.txt`,
`expect=ok`):

```
=== OLD checker (committed at abfbf35)
RECEIPT f1-committed-inline-header MISSING_PROVENANCE
EXPECT_SUMMARY: 0/2
EXIT=1
=== NEW checker on same claims
RECEIPT f1-committed-inline-header ok
EXPECT_SUMMARY: 1/2
EXIT=2
```

(the second old-suite claim was a WORKTREE stale fixture without `bind_rev`;
the new checker refuses to bind a worktree read to a revision it was not given,
hence `ERROR` — not a credit).

### F2 — a stale-but-consistent receipt read `ok` at a later revision

The old `evaluate()` resolved `tool_sha256` at `measured_commit` only and never
compared with the read revision. Fixed by steps 3–5.

Differential in a disposable `/tmp` repo where the old parser works (two
commits; the receipt records the c1 tool and is unchanged at c2):

```
c1=201073f73aa583d1081ca7817f3160660f1afd12
c2=60b036f853e0b4330757622e80300ad982516383
tool_sha=8419ff13897cbe37259aafcdf99caa54532b826445935be0fcb71456525ebc26
=== OLD checker (committed at abfbf35), stale receipt read at c2
RECEIPT f2-stale-mini-repo ok
EXPECT_SUMMARY: 1/1
EXIT=0
=== NEW checker, same claim
RECEIPT f2-stale-mini-repo STALE
EXPECT_SUMMARY: 0/1
EXIT=1
```

The same rule bites on lane bytes without any lab: the committed
`tripwire-frozen-before.txt` (it ran the `d9a5a18` tool, `962919ce`) read at
`abfbf35` with no `bind_rev` is `STALE`; with `bind_rev=d9a5a18` it is `ok`
(§4.2, `attack-committed-before-*`). That is the file's whole purpose — a
before-state probe — and the claim now has to say so.

### F3 — claim paths did not match the re-cut outputs

All six old claims named `…-recut.txt` files that **do not exist** at
`abfbf35` (verified with `git cat-file -e`, six `MISSING`). The new claims name
the files `recut-receipts.sh` actually writes (`evidence/tripwire-r13.txt` …
`r16`, `tripwire-anchor-r15.txt`), plus the frozen and measure receipts. The
round-18 join claim is **dropped**: `tripwire-pacmanlog-join.txt` is a
hand-authored `awk` join over `/var/log/pacman.log`, not tool output, so it
cannot carry a producer header; the round-17 join stays as one of the six reds
with a `note` (CriticC1 defect 3).

## 4. Retained evidence

### 4.1 Canonical run (lane, 2026-10-20)

```
$ python3 -I .ufo/waves/round-18/receipt-check.py
RECEIPT r17-tripwire-r13 MISSING_PROVENANCE
RECEIPT r17-tripwire-r14 MISSING_PROVENANCE
RECEIPT r17-tripwire-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-r16 MISSING_PROVENANCE
RECEIPT r17-tripwire-anchor-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-pacmanlog-join MISSING_PROVENANCE
RECEIPT r18-fixture-ok ok
RECEIPT r18-fixture-bad-sha SHA_MISMATCH
RECEIPT r18-fixture-stale-rev SHA_MISMATCH
RECEIPT r18-fixture-stale-tool STALE
RECEIPT r18-fixture-nonancestor NOT_ANCESTOR
RECEIPT r18-fixture-producer-mismatch PRODUCER_MISMATCH
RECEIPT r18-tripwire-r13 ok
RECEIPT r18-tripwire-r14 ok
RECEIPT r18-tripwire-r15 ok
RECEIPT r18-tripwire-r16 ok
RECEIPT r18-tripwire-anchor-r15 ok
RECEIPT r18-tripwire-frozen-match ok
RECEIPT r18-tripwire-frozen-tampered ok
RECEIPT r18-tripwire-frozen-before ok
RECEIPT r18-measure-after ok
EXPECT_SUMMARY: 21/21
EXIT=0
```

Also green from `/tmp` (lane root derived from the script path; claims path may
be relative to cwd): `21/21`, exit 0, and with an explicit relative claims
argument `21/21`, exit 0.

### 4.2 Attack battery (`/tmp/receipt-attack-claims.json`)

```
RECEIPT attack-committed-before-no-bind STALE
RECEIPT attack-committed-before-with-bind ok
RECEIPT attack-bad-bind ERROR
RECEIPT attack-pending PENDING
RECEIPT attack-unreadable ERROR
EXPECT_SUMMARY: 2/5
EXIT=2
```

- `attack-committed-before-no-bind`: committed lane bytes, no `bind_rev` → `STALE`.
- `with-bind`: the same bytes with `bind_rev=d9a5a18` → `ok`.
- `attack-bad-bind`: `bind_rev=f71ccbe` on a receipt measured at `4c103b5` is a
  binding that is neither the read revision nor the measured one → `ERROR`.
- `attack-pending` / `attack-unreadable` → `PENDING` / `ERROR`, exit 2.

Exit-1 and malformed-claim controls:

```
$ … /tmp/receipt-wrong-expect.json      # ok claimed on a SHA_MISMATCH fixture
RECEIPT attack-wrong-expect SHA_MISMATCH
EXPECT_SUMMARY: 0/1
EXIT=1
$ … /tmp/claims-empty.json              # no "claims" key
RECEIPT_CLAIMS_ERROR: /tmp/claims-empty.json: 'claims'
EXIT=2
$ … /tmp/claims-malformed.json          # claim missing fields
RECEIPT claim#1 ERROR (bad claim or expect)
EXPECT_SUMMARY: 0/1
EXIT=2
$ … /tmp/claims-badexpect.json          # expect: "WAT"
RECEIPT claim#1 ERROR (bad claim or expect)
EXPECT_SUMMARY: 0/1
EXIT=2
```

### 4.3 Mutation battery

Each row copies the final lane script to `/tmp/mut-MN.py` (only the `LANE`
constant patched to the lane), applies one mutation, and runs the lane claims
(`M6`/`M7` run the controls noted). All mutants are killed:

| mutant | exit | EXPECT_SUMMARY | divergence |
|---|---|---|---|
| M1 digest compare disabled | 1 | 19/21 | `r18-fixture-bad-sha:ok`, `r18-fixture-stale-rev:ok` |
| M2 STALE collapsed to ok | 1 | 20/21 | `r18-fixture-stale-tool:ok` |
| M3 ancestry disabled | 1 | 20/21 | `r18-fixture-nonancestor:STALE` |
| M4 producer check disabled | 1 | 20/21 | `r18-fixture-producer-mismatch:ok` |
| M5 missing-provenance branch disabled | 2 | 15/21 | four round-17 reds become `ERROR` |
| M6 expectation compare disabled | 0 | 1/1 | wrong-expect control (baseline exit 1) |
| M7 unevaluated not tracked | 1 | 2/5 | attack claims baseline exit 2 → exit 1 |
| M8 anchored sha regex (F1 regression) | 1 | 9/21 | round-18 receipts + new fixtures `MISSING_PROVENANCE` |

M8 reproduces exactly the wave-1 F1 defect, so the unanchored parse is
load-bearing, not cosmetic.

### 4.4 Digests the claims bind to (`git show <rev>:<path> | sha256sum`)

```
abfbf35 tripwire=c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb
4c103b5 tripwire=c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb
d9a5a18 tripwire=962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
f71ccbe tripwire=7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7
d9a5a18 measure=de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc
abfbf35 measure=de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc
```

Ancestry used by the claims (all `git merge-base --is-ancestor … ; echo $?` = 0):
`4c103b5 ≤ abfbf35`, `d9a5a18 ≤ abfbf35`, `f71ccbe ≤ d9a5a18`; `abfbf35 ≤ d9a5a18` = 1
(the `NOT_ANCESTOR` fixture).

## 5. Claim population

| block | count | expectation |
|---|---|---|
| round-17 reds at `d9a5a18` (r13, r14, r15, r16, anchor-r15, pacmanlog-join) | 6 | `MISSING_PROVENANCE` |
| authored fixtures | 6 | `ok`, `SHA_MISMATCH`, `SHA_MISMATCH`, `STALE`, `NOT_ANCESTOR`, `PRODUCER_MISMATCH` |
| round-18 receipts at `abfbf35` (r13–r16, anchor, frozen match/tampered/before, measure-after) | 9 | `ok` |
| **total** | **21** | 21/21, exit 0 |

The join reading: "drop the join file" is applied to the round-18 re-cut set
(no `ok` claim can honestly exist for it); the round-17 join remains as the
sixth red so the red set stays six. If L1 reads the instruction as removing the
join entirely, delete that claim — the rest is unaffected (20/20, exit 0).

The two extra fixtures beyond the required `STALE` one (`nonancestor`,
`producer-mismatch`) are controls for the ancestry clause and the header
`tool=` token; both are killed by mutation (M3/M4). Dropping them is safe if a
minimal population is preferred, at the cost of leaving those branches untested.

## 6. Findings for L1 (not fixed here — not my files)

1. **`corpus/QUALITY.md:136` at `abfbf35` now has a status drift.** It says a
   fixture "bound to the `f71ccbe` tool sha read at a later tool prints
   `SHA_MISMATCH`". A receipt whose `tool_sha256` is the `f71ccbe` digest and
   which names `measured_commit=f71ccbe` now prints **`STALE`**; the
   `SHA_MISMATCH` case is the cross-binding fixture (`measured_commit=f71ccbe`
   but the later digest, `stale-rev-receipt.txt`). Both fixtures exist, so
   either wording is demonstrable — but line 136 should say `STALE` (or name
   `stale-rev-receipt.txt` explicitly) before round 19 cites it. The rest of the
   paragraph (six reds; green re-cuts and frozen replay) is satisfied.
2. **CriticC1 defect 2 is still open:** `label-check-final.txt` carries its tool
   digest in a `sha256sum` line, not `tool_sha256=`; this checker has no such
   form, so it cannot serve as the green control the critic proposed. Adding it
   is a new parsing rule, not a defect of this item.
3. **ConnLessonChain F7 is still open:** there is no `report` claim kind, so
   criterion 24's R17-V2 clause (a report sentence labelling a tool sha with the
   wrong revision) has no failing control in this instrument. The STALE rule
   covers the receipt-side shape only.
4. `SKILL.md:568` needs no edit: 0/1/2 and "malformed claim, pending rev" still
   describe the script exactly.
5. A `.ufo/waves/round-18/__pycache__/` exists (13:01–13:02, i.e. **before** my
   first write at 13:03; it holds `measure-mutants` and an old `receipt-check`
   pyc from another import). Left untouched; the round's `.gitignore` already
   covers `__pycache__/`.

## 7. Limits and risks

- `bind_rev` is a claim declaration. Setting it to `measured_commit` marks a
  before-state receipt; bytes alone cannot distinguish an honestly labelled
  before receipt from a mislabelled after receipt. What the checker can and does
  refuse is the silent case: no `bind_rev`, tool drift → `STALE`. The audit
  trail is the claim's `note` plus the read revision.
- A `WORKTREE` claim without `bind_rev` is `ERROR` (never credit): an authored
  fixture has no read revision to bind to.
- The `tool=` producer token is honoured only on line 1, because tripwire verdict
  bodies carry per-finding `"tool": "bash"` keys; a receipt with comments before
  its header still binds sha/rev, but its producer is not cross-checked.
- JSON-form receipts are accepted for `tool_sha256`/`measured_commit` only; a
  JSON `"tool"` key is not read as a producer (same ambiguity as above).
- Everything was read through `git show` at the named revisions or the worktree
  fixture files; no receipt body was executed and no target text was treated as
  instruction.
- Verification here is behavioural only: this script is a probe, not a gate. It
  was not run through `tools/mado-verify.sh` (out of this item's scope).

`Report: .ufo/waves/round-18/w2/reports/ReceiptCheckFix.md`
