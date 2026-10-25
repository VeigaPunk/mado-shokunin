# RevengerRepair — round 35, wave 1

Mission: revenge the two routed round-34 defects — (a) the dead word bound, repaired by
retiring `r34-word-bound-1-25` and making the quote a free variable under the live clause
`gate-quote-word-bound`; (b) the `S_ISLNK`/`O_NOFOLLOW` pair mislabelled load-bearing,
repaired by splitting it in `c1/clauses.json` (walk = load-bearing, flag = declared
`not-load-bearing` TOCTOU defence).

Method: all runs against committed bytes re-executed at write time; revenge trees and mutant
counters built in `/tmp/revenge-r35` (scratch, not committed). Leaf member — no subagents.

## Verdicts

| Defect | Verdict |
|---|---|
| Dead word bound (`gate-quote-word-bound`) | **Repair holds — could not revenge.** The clause really fails; I constructed two independent trees (0-word and 31-word quotes) where it is the *sole* failing clause. |
| TOCTOU pair (`S_ISLNK`/`O_NOFOLLOW` split) | **Repair holds — split is honest**, with one cosmetic imprecision: the named walk-killer control (`c1-entry-symlink`) is a leaf link and cannot discriminate walk from flag. The split itself is proven by a parent-symlink tree and a live stat→open race, both run here. |

## Defect 1 — the dead word bound

**r34 deadness confirmed first.** In `PRED-C1-r34-v1` (`round-34/c1/count.py:152-153`) the bound
ran on `found`, which `found == quote` pinned to the frozen quote; frozen quotes are 8 and 2
words (`c1/frozen.json` `quotes`: S201=8w, S202=2w). `1 <= len(words) <= 25` could never
evaluate false — dead code under its own spec, as diagnosed.

**r35 repair tested by construction.** The r35 counter (`c1/count.py:175-194`) computes the
quote from the entry (`gate_quote`, :127-135) and checks `1 <= len(words) <= 25` (:194) with
no frozen-quote pin. Two trees, built by copying `controls/golden` and editing one line each:

| Tree (scratch) | Change | Result | Sole failing clause (attribution) |
|---|---|---|---|
| `quote-empty` | `gate-quote: S203 ` with empty quote text | `closed_rows=7 open_cites=1 TARGET_MISSED` exit 1 | `gate-quote-word-bound` (0w) — note `b"" in blob` is True, so substring passes; only the bound kills |
| `quote-long-own` | S203 quote = 31-word *contiguous* tail span of the receipt's 64-word line | `closed_rows=7 open_cites=1 TARGET_MISSED` exit 1 | `gate-quote-word-bound` (31w) — substring verified `True` in receipt bytes before running |

Attribution computed by replaying `main()`'s per-clause conjunction (:185-196) and naming each
failed conjunct: both trees fail **only** `gate-quote-word-bound`. The committed control
`controls/c1-quote-long` was re-run and re-verified (`closed_rows=7 open_cites=1 TARGET_MISSED`,
matching its committed receipt `:1-4`); its 35-word quote is likewise a contiguous substring of
the S203 receipt, so it too kills solely through the bound. All eleven c1 controls + golden
re-executed; every output matches its committed `controls/*.txt` verbatim.

Verdict: **discharged.** The clause is failable on both bounds with everything else passing.

## Defect 2 — the TOCTOU pair split

Ledger claim (`c1/clauses.json:78-83`): the `S_ISLNK` component walk is load-bearing; the
`O_NOFOLLOW` flag on `os.open` (`count.py:90`) is `not-load-bearing` because "the S_ISLNK
component walk already rejects every static symlinked tree, and no static tree can kill the
open-time flag."

**Walk is load-bearing — proven.** Mutant `count-nowalk.py` (every `stat.S_ISLNK` rejection
removed, intermediates followed via `stat()`, `O_NOFOLLOW` retained) vs `count-nonofollow.py`
(flag removed, walk intact), run on a constructed `parent-symlink` tree
(`corpus/knowledge -> ../knowledge-real`, entry files real inside it):

| Counter | parent-symlink | entry-symlink-ident | entry-symlink (committed) |
|---|---|---|---|
| orig | MISSED | MISSED | MISSED |
| nowalk (walk off, flag on) | **MET** | MISSED | MISSED |
| nonofollow (walk on, flag off) | MISSED | MISSED | MISSED |
| neither | **MET** | **MET** | MISSED |

Removing the walk alone flips `parent-symlink` to MET — the flag cannot substitute for it
(`O_NOFOLLOW` guards only the final component). So the walk is load-bearing, and its load is
**intermediate/root symlinks**: `open("corpus/knowledge/x.md")` resolves the linked parent
regardless of the flag; only the walk's `lstat` sees `S_IFLNK` there.

**Flag is not statically load-bearing — proven.** `entry-symlink-ident` (leaf symlink →
byte-identical shadow outside `corpus/`): MISSED under orig and under each single mutant;
only `neither` reaches MET. No static tree fails *because of* the flag — the walk always
rejects first. Deleting the flag alone changes nothing on any static tree (`nonofollow` row).

**Flag carries exactly the TOCTOU load — proven by live race.** Patched `os.lstat` so that the
walk's final-component stat of `idle-lock-chain-armed-r14.md` returns a real-file mode, then
the file is renamed aside and a symlink (→ identical bytes) planted before `os.open`:

- orig counter (`O_RDONLY|O_NOFOLLOW`): `race_fired=True` → `TARGET_MISSED` exit 1 (open raises ELOOP → entry unreadable → `entry-regular` fails).
- flagless mutant (`O_RDONLY`): `race_fired=True` → **`TARGET_MET` exit 0** — the open follows the planted symlink and every clause passes on identical bytes.

The flag's entire killing power is confined to the check→use window; with identical target
bytes it is also only detectable, not protective — consistent with "TOCTOU-only defence."

**Honesty caveat (non-blocking):** the walk's named killer `controls/c1-entry-symlink` is a
*leaf* symlink (`corpus/knowledge/idle-lock-chain-armed-r14.md -> idle-lock-never-asked-r12.md`).
Either half alone rejects it (flag: ELOOP; walk: S_ISLNK), so the receipt does not isolate the
walk — under the honest `nowalk` mutant it still MISSED. The split's load-bearing claim is
true, but the committed control is non-discriminating; a parent-component link would have been
the discriminating witness. Registration wording ("`controls/c1-entry-symlink.txt` kills it")
is directionally right but the receipt alone cannot prove which half fired.

**Secondary check — the c2 ledger counter.** `python3 -I .ufo/waves/round-35/c2/count.py
--repo . --frozen .ufo/waves/round-35/c2/frozen.json` → `uncovered=0 retired=1
toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` exit 0. Note its `uncovered` check
(`c2/count.py:90-92`) only regex-matches `verdict=TARGET_MISSED` in committed receipt text —
it never re-runs the trees; receipt authenticity rests on commit-time honesty, which this
report verified by re-execution (all 11 receipts reproduce verbatim).

## Reproduction

```sh
# defect 1 — bound fails, sole clause
python3 -I .ufo/waves/round-35/c1/count.py --root <quote-empty|quote-long-own> \
  --frozen .ufo/waves/round-35/c1/frozen.json        # → TARGET_MISSED, exit 1

# defect 2 — mutant matrix (mutants remove S_ISLNK walk / O_NOFOLLOW / both)
python3 -I <mutant>.py --root parent-symlink  --frozen …/c1/frozen.json
python3 -I <mutant>.py --root entry-symlink-ident --frozen …/c1/frozen.json

# defect 2 — race: os.lstat patched; leaf renamed + symlink planted between
# walk stat and os.open → orig MISSED, flagless MET
```

## Bottom line

Both routed repairs survive revenge: the word bound is live and independently failable
(two constructed trees, sole-clause failure each), and the ledger's split correctly names the
`S_ISLNK` walk load-bearing (only it rejects intermediate-component links) and `O_NOFOLLOW`
TOCTOU-only (no static tree can kill it; only a stat→open swap can, and does). The single
imprecision is cosmetic: `c1-entry-symlink` is a leaf link and cannot discriminate the two
halves — a parent-symlink control would be the honest witness for the walk.
