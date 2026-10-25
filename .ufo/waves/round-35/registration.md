# Round 35 registration — mado

Author: Kimi fresh L1. Date: 2026-10-24. Frozen **before** any round-35 data lands.
Nothing in this file is rewritten after a seat scores it.

## Claims (2, distinct axes, causally separable)

Both claims sit on the lane's **lowest non-retired axes**. The published axis table at
the round-34 tip reads `navigation 47/47`, `calibration resolved-active 41/41`,
`operability selftest 12/12` — three sub-axes tied at 1.0 — and a capability entered
the capabilities table in round 34, so the AXES.md stagnation nudge does **not** waive
the lowest-axis obligation. C1 works coverage and C2 works calibration; the other two
of the three tied axes are untouched, and no axis is lowered.

### C1 — coverage: the idle-lock control surface

**Surface.** The desktop's idle-lock control surface — the bar's idle-indicator module,
the desktop menu's Idle Lock entry, the indicator's own two-state vocabulary, the
screensaver/lock chain that is armed on this host, and the setup path that never asks
the question. The corpus holds the 2026-10-14 idle-chain point sample
(`knowledge/idle-lock-plane.md`) and the 2026-10-14 first-run reading, and it holds no
measurement of the *offer*: the bar module, the menu entry or the indicator's tooltip
were never opened by this lane.

**Predicate (`PRED-C1-r35-v1`, frozen in `c1/frozen.json`, implemented in `c1/count.py`).**

> TARGET_MET iff `closed_entries=3 AND closed_rows=8 AND open_cites=0`, where a frozen
> cite is closed only when the entry path is a regular file inside the scored root, the
> registry holds exactly one well-formed row for that id whose used-by token set is
> exactly the admitted entries citing it, whose status is `mined`, whose recheck cell is
> a valid cadence token, whose cells contain no literal or escaped pipe, and whose
> anchor cell carries the sha256 of the named receipt; and the entry carries exactly one
> gate-quote line for that id whose quote is a contiguous substring of the receipt bytes
> and is 1-25 words long.

**Target.** `closed_entries=3`, `closed_rows=8`, `open_cites=0`.

**Counting command.**

```sh
python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
```

**Kill rule (discharged before data).** Every control tree under
`.ufo/waves/round-35/controls/` must print `verdict=TARGET_MISSED` with exit 1, except
`controls/golden`, which must print `TARGET_MET` with exit 0. Receipts are committed
beside each tree (`controls/<name>.txt`).

| control | what it injects | receipt |
|---|---|---|
| `c1-donothing` | no entries, no rows | `controls/c1-donothing.txt` |
| `c1-entry-symlink` | the entry path is a symlink | `controls/c1-entry-symlink.txt` |
| `c1-row-duplicate` | the id's row is duplicated | `controls/c1-row-duplicate.txt` |
| `c1-row-extra-field` | a cell carries an extra field (the literal-pipe case) | `controls/c1-row-extra-field.txt` |
| `c1-usedby-extra` | `used-by` carries a stray token | `controls/c1-usedby-extra.txt` |
| `c1-status-queued` | `status` is `queued` | `controls/c1-status-queued.txt` |
| `c1-recheck-prose` | `recheck` is prose, not a cadence | `controls/c1-recheck-prose.txt` |
| `c1-digest` | the anchor digest is wrong | `controls/c1-digest.txt` |
| `c1-quote-absent` | the gate-quote is not in the receipt | `controls/c1-quote-absent.txt` |
| `c1-quote-long` | the gate-quote is 30 words and contiguous | `controls/c1-quote-long.txt` |
| `golden` | nothing — the anti-vacuity control | `controls/golden.txt` |

**The data.** Three knowledge entries and eight registry rows, all from
`/home/vgpnk/Projects/shokuknow/merge/mado/` (read-only), re-grounded in-round:
`corpus/knowledge/idle-lock-never-asked-r12.md` (S203, S204),
`corpus/knowledge/idle-lock-chain-armed-r14.md` (S205),
`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` (S206–S210).

### C2 — calibration: the lane's own evidence ledger

**Surface.** The lane's self-description of its own evidence — the clause ledger of the
admission counter, the retirement of a clause that was dead code under its own frozen
spec, the treatment of the TOCTOU-only half of the symlink defence, and the tip label
of the round-34 frozen-blob artifact.

**Predicate (`PRED-C2-r35-v1`, frozen in `c2/frozen.json`, implemented in `c2/count.py`).**

> TARGET_MET iff `uncovered=0 AND retired=1 AND toctou_declared=1 AND ledger_tip_ok=1`,
> where `uncovered` counts live clauses of the round-35 admission counter that carry
> neither a named control whose committed receipt records a TARGET_MISSED verdict, nor a
> `not-load-bearing` declaration with a reason; `retired` counts live clause ids listed
> as retired in the ledger whose id is absent from the live clause list (the r34
> `quote-equals-frozen` clause, dead code under its own frozen spec); `toctou_declared`
> counts live clauses carrying a `not-load-bearing` declaration with a reason — exactly
> the S_ISLNK/O_NOFOLLOW pair, which no static tree can kill, so it is never counted as a
> load-bearing clause; `ledger_tip_ok` is 1 when the round-35 frozen-blob ledger names
> the round-34 tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2` and every frozen blob it
> lists re-verifies by git blob id at that revision.

**Target.** `uncovered=0`, `retired=1`, `toctou_declared=1`, `ledger_tip_ok=1`.

**Counting command.**

```sh
python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
```

**Kill rule.** The do-nothing control for C2 is the counter run against a clause ledger
whose one clause has neither a control nor a declaration: it must print
`verdict=TARGET_MISSED` with exit 1. Receipt committed at `controls/c2-donothing.txt`.

## The two routed r34 defects this round repairs, and how

1. **The dead word bound.** In `PRED-C1-r34-v1` the 1-25 word clause was checked
   against `found`, which `found == quote` pinned to a frozen short quote, so the clause
   could never fail — dead code under its own frozen spec. **Repaired by retirement:**
   the clause id `r34-word-bound-1-25` is recorded in `c1/clauses.json` under
   `retired`, is absent from the live clause list, and the r35 counter makes the
   entry's quote a *free* variable so the replacement clause `gate-quote-word-bound` is
   live and has a failing case (`controls/c1-quote-long.txt`).
2. **The TOCTOU-only pair.** The r34 `S_ISLNK`/`O_NOFOLLOW` pair was presented as
   load-bearing. **Repaired by splitting it:** the `S_ISLNK` component walk is
   load-bearing (`controls/c1-entry-symlink.txt` kills it), while the open-time
   `O_NOFOLLOW` flag is declared `not-load-bearing` with the reason recorded in the
   clause ledger. The counter's `uncovered` count therefore cannot be satisfied by a
   clause that merely claims to be load-bearing.
3. **The stale tip label.** The round-34 `RevFrozenBlobs.md` named `fa7ba113` the lane
   tip; the real round-34 tip is `dff3941`. **Repaired by re-issue**, not by rewriting
   the round-34 artifact: `.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md` measures the
   same seven paths at `dff3941` and the C2 counter verifies every blob id there.
4. **The stale merge-package id remap** is campaign-side and already filed as L0
   `ae2c52b8`. **Not duplicated here.** The lane's own id handling is recorded in the
   round lesson: the adopted rows continue the lane's registry at S203–S210, re-pointed
   **by document**, and the package's own ids for the same documents (S309, S310, S321,
   S329, S330, S331, S334, S336) are recorded in the lesson's Gate block for the
   campaign to reconcile.

## Non-negotiables held while the wave runs

- The predicates, targets, counters, clause ledger and controls above are **frozen**
  before the data lands and are not edited after any seat scores them.
- Seats never mutate the fleet repo, a sibling lane, the lane's jj state or the lane's
  Git index. `/home/vgpnk/Projects/shokuknow` is read-only.
- Nothing is committed from the merge package as-is: every staged row is normalised in
  scratch first (no literal or escaped pipe, a valid recheck cadence, `status=mined`,
  `used-by` exactly the admitted entries citing it) and the append is validated on a
  scratch mirror of the lane before the first real append.
