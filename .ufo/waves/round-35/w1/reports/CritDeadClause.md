# CritDeadClause — dead-clause hunt on the r35 counters

Seat: CritDeadClause (critic, round-35 w1). Scope: `PRED-C1-r35-v1` and
`PRED-C2-r35-v1`, each clause tested against its own frozen spec. Method: for each
clause, ask whether a spec-legal configuration exists that falsifies that clause.
The r34 lesson applied forward: a clause is dead when the spec itself pins the
variable it tests, so no input can ever falsify it.

Counters run as committed:

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED   (pre-data)
$ python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
```

## PRED-C1-r35-v1 — the per-cite closure conjunction (count.py:185-196)

The implemented conjunct is `ok = blob is not None and row is not None and nf_ok
and used_by == citing and cs[7]=="mined" and valid_recheck(cs[9]) and
receipt["sha256"] in cs[5] and quote is not None and 1<=len(words)<=25 and
quote.encode() in blob`. Clause ledger: `c1/clauses.json`, nine live + one
not-load-bearing + one retired.

| clause | failable? | argument / evidence |
|---|---|---|
| `entry-regular` | YES | Entry must be a regular file, every component non-symlink, inside root. `controls/c1-entry-symlink` → `closed_rows=7 open_cites=1 verdict=TARGET_MISSED` (committed receipt). |
| `row-unique` | YES | `len(rows)==1`. Two matching rows and zero rows both fail. `controls/c1-row-duplicate` → TARGET_MISSED. |
| `row-well-formed` | YES | `len(cells(row))==11`; a literal pipe adds a field. `controls/c1-row-extra-field` → TARGET_MISSED. **Caveat:** the spec text says "no literal or escaped pipe"; `split('|')` counts fields only, and `\|` never adds a field, so the *escaped-pipe half of the spec wording is unimplemented dead text* (clauses.json:23's claim that both cases are "covered by the field count" is wrong for `\|`). The clause as implemented is live; the spec phrase over-promises. |
| `used-by-exact` | YES | Set-equality against `spec["entries"]` citing set. `controls/c1-usedby-extra` (stray token) → TARGET_MISSED; a missing token fails the same conjunct. |
| `status-mined` | YES | `cs[7]=="mined"`. `controls/c1-status-queued` → TARGET_MISSED. |
| `recheck-valid` | YES | ISO date \| `\d+d` \| symbolic token. `controls/c1-recheck-prose` → TARGET_MISSED. |
| `digest-match` | YES | `receipt["sha256"] in cs[5]` — substring test of the frozen digest in the anchor cell. `controls/c1-digest` → TARGET_MISSED. It binds the *spec's* digest to the cell, not the cell to the blob bytes; that is what the spec words say, so faithful, not dead. |
| `gate-quote-substring` | YES | Two sub-conditions: extraction yields exactly one `gate-quote: {sid} ` line (`quote is not None`), and the quote is a contiguous substring of the receipt bytes (`quote.encode() in blob`). `controls/c1-quote-absent` → TARGET_MISSED. Probe: duplicating the S205 line in a golden copy → `closed_rows=7 open_cites=1 verdict=TARGET_MISSED` (exactly-one enforced, scratch `CritDeadClause/dup`). |
| `gate-quote-word-bound` | YES — **live, this is the repair** | Quote is now a *free variable*: `frozen.json` carries no `quotes` block (diff vs r34 frozen.json, which pinned `spec["quotes"][sid]`). Upper bound: `controls/c1-quote-long` writes a 26+-word contiguous substring of receipt S203 (222 `wc -w` words — the substring domain contains it) → TARGET_MISSED attributable to the bound alone. Lower bound: whitespace-only quote probe → `closed_rows=7 open_cites=1 verdict=TARGET_MISSED` (scratch `CritDeadClause/ws`). Both directions failable. |
| (unledgered) receipt-regular | YES but **absent from clauses.json** | `blob is not None` requires the receipt path itself to pass `read_regular`. Probe: deleting `fetch/S205.receipt.txt` from a golden copy → TARGET_MISSED (scratch `CritDeadClause/norec`). The spec text does not name this check ("sha256 of the named receipt" implies reading it); the implementation enforces it and the C2 `uncovered` audit cannot see a clause that is not in the ledger. Live code, invisible to the clause audit. |

### Summary thresholds — redundant, not dead

`open_cites + closed_rows = 8` holds for every tree under the frozen spec (the
eight frozen cites partition over the three frozen entries). Hence under the spec
`closed_rows=8 ⟺ open_cites=0 ⟺ closed_entries=3`: all three are logically
equivalent propositions. Each *can* fail (the do-nothing control fails all three),
so none is dead in the r34 unfailable sense — but `closed_entries=3` and
`open_cites=0` carry zero independent discriminating power; `closed_rows=8` is
the only summary clause doing work. Dead weight, flag-forward material.

`o-nofollow-open` is declared `not-load-bearing` with a reason — correctly, since
no static tree can exercise an open-time flag. This is the honest label, not a
dead clause smuggled past the audit.

## PRED-C2-r35-v1 — four summary conjuncts (count.py:81-124)

| clause | failable? | argument / evidence |
|---|---|---|
| `uncovered=0` | YES | Clause skipped iff `not-load-bearing` has a `reason`, else requires a committed receipt containing `verdict=TARGET_MISSED`. Control `c2-donothing` (one clause stripped of both) → `uncovered=1 ... verdict=TARGET_MISSED`, receipt committed. |
| `retired=1` | YES | Counts `retired[]` ids absent from live ids; target pins exactly 1. Probe: ledger with `retired` deleted → `retired=0 ... TARGET_MISSED` (scratch `CritDeadClause/noret`). Live. **Weakness, not deadness:** the counter counts *any* retired id absent from live — it never checks the retired id is `r34-word-bound-1-25`, so a bogus retired entry satisfies it. |
| `toctou_declared=1` | YES | Exact-list equality `declared == [spec["toctou_clause"]]`. Probe: renaming the declared clause id → `toctou_declared=0 ... TARGET_MISSED`. Fails on zero declarations, on two, and on a renamed id. Live. **Weakness:** a clause carrying both `not-load-bearing` and `control` is skipped in the `uncovered` loop before its control is checked — a clause can dodge a false control this way (spec is silent on co-occurrence). |
| `ledger_tip_ok=1` | YES | Probe: `blob_ledger` pointed at a doc naming the stale tip `fa7ba1…` with "all blobs verified" → `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=0 TARGET_MISSED` — isolated failure, clause confirmed live. **Weakness:** the tip check is substring-in-text; a doc that merely contains the string and lists re-verifying blobs passes the first half without claiming the tip is the tip. |

No dead clauses in C2. The four conjuncts measure disjoint artifacts (clause
ledger, retired list, declaration list, blob ledger + git object store).

## Was the r34 repair complete?

The defect: in `PRED-C1-r34-v1` the entry's gate-quote was pinned by
`found == spec["quotes"][sid]` (count.py:144,152), so `words` was derived from a
frozen string whose length was fixed inside 1-25 — the bound could never fail.

The repair, verified at r35:

1. `frozen.json` has no `quotes` block; `gate_quote(entry, sid)` reads the quote
   from the entry text — the variable is free (count.py:127-135,175-195).
2. The bound is failable in both directions: `controls/c1-quote-long`
   (committed receipt, TARGET_MISSED attributable solely to `len(words)>25`,
   since the 26-word quote is a real substring of receipt
   `1b7fa87f…`, 222 words) and the whitespace probe for `len(words)<1`.
3. The dead clause is recorded: `r34-word-bound-1-25` sits in `clauses.json
   .retired`, absent from `live`, and C2's `retired=1` conjunct — itself
   probe-verified failable — audits that fact.
4. The r34 companion defect (TOCTOU pair presented as load-bearing) is likewise
   discharged by the `o-nofollow-open` declaration plus the split `S_ISLNK`
   control.

**Verdict: the repair is complete for the diagnosed defect.** The retired clause
is genuinely dead only in r34; in r35 no live clause of either predicate is dead.
Residual exposure, forward-flagged rather than repair-blocking: the spec's
"escaped pipe" half is unimplemented text; `blob is not None` is a live conjunct
with no clause-ledger entry, so the C2 audit is blind to it; two of three C1
summary thresholds are redundant; and C2 accepts any retired id, any receipt file
mentioning `TARGET_MISSED`, and any ledger doc containing the tip string —
satisfaction-shaped checks, not dead clauses.
