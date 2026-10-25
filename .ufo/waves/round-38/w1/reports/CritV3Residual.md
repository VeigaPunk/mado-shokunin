# CritV3Residual — mado round 38, wave 1

**Scope:** residual crib surface of the two v3 counters after the 19-control manifest
discriminates (19/19 at lane HEAD `b6c1d31`). Built the cheapest TARGET_MET cribs against
`quality/counters/c1-r38-event-ground.py` and `quality/counters/c2-r38-eventq.py` in a
`/tmp` sandbox at base `b4e47e9`, measured their bytes, classified each residual, and
proposed the cheapest additional frozen clause per residual.

**Method:** sandbox clone `git clone -q --no-local /home/vgpnk/Projects/shokunin/mado-shokunin
/tmp/mado38-CritV3Residual/sb`, checked out at `b4e47e9` (both target entries, the
round-37 lesson and the round-38 receipts are absent there, so the c1 precondition
"ground unheld at base" holds — verified: `grep` for the four frozen tokens over
`corpus/knowledge/*` at base returns nothing). Lane files were only read/copied, never
written. No tools installed (python3/git/sha256sum/wc only).

---

## C1 — cheapest surviving TARGET_MET

### Shape A — hollow prose + real gates (PASSES, cheapest)

Sandbox branch `master` rev `6f48d22`. Added content:

| artifact | bytes |
|---|---|
| `corpus/knowledge/event-delivery-limits-r26.md` (hollow) | 316 |
| `corpus/knowledge/event-queue-observability-r37.md` (hollow) | 360 |
| `corpus/lessons/round-37.md` (4 `GATE` lines only) | 798 |
| `corpus/README.md` (2 coverage-map rows) | ~110 |
| `corpus/SOURCES.md` (S189 used-by append 48 B + 2 stub rows 318 B) | ~366 |
| copied pinned receipts `S189.bin` + `S213.receipt.txt` + `S217.bin` | 6,479 + 1,814 + 1,767 = **10,060** |
| **total** | **≈ 12,009 B** |

Why each clause is satisfied by construction:

- **a/b/k** — entries absent at base; header carries `source:`, `verified-at: 2026-10-25`,
  `recheck: 90d`.
- **c/j** — one `## Registry` row per cited id, 11 cells, `r[7]="mined"`, used-by naming
  the entry (S189's base row edited; S213/S217 rows appended).
- **h/d/f/g** — `GATE` lines copied verbatim from the real lesson carry the frozen
  (path, sha256) pins; S189 is the *only* pinned receipt containing both r26 tokens
  (`MAX_QUEUED_EVENTS`, `overflowed event queue` — verified by grep), so r26 cites just
  S189; r37-obs needs two receipts because S213 lacks `m_logsEnabled` (grep count 0) and
  S217 lacks `debug:disable_logs` (grep count 0) — the S213+S217 pair (3,581 B) is the
  minimal cover. Quotes are stated in the body and an `**OBS** S<id>` line names each id.
- **l** (the v3 repair under attack) — the entire body is one hollow sentence per entry:
  r26 lists `queue cap removed writeoffset eagain partial writes are resumed 1024`
  (7/7 phrases, need 4); r37-obs lists `null channel … returns before … core-logger`
  (3/3, need 2). `norm()` lowercases and strips ids/``*` ``; nothing checks that the
  prose means anything. Floor at `c1-r38-event-ground.py:87` (LINEAGE) and `:249-251`.

Counter run (exact output):

```
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S189 lineage=7/4 ok=1
PRED-C1-r38-v3 entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S213,S217 lineage=3/2 ok=1
PRED-C1-r38-v3 admitted=2/2 verdict=TARGET_MET rev=6f48d22… base=b4e47e9…   RC=0
```

### Shape B — lineage phrases harvested verbatim (PASSES, larger)

Sandbox branch `crib-harvest` rev `b64f1b9`: real-entry sentences carrying the phrases,
same wiring. Entries 523 + 445 = 968 B; total ≈ 12,300 B. Same `TARGET_MET` result
(`lineage=5/4` and `2/2`). Strictly dominated by shape A.

### C1 measurement

- **Cheapest surviving C1 shape: hollow, ≈ 12.0 KB committed**, of which **10,060 B is
  digest-pinned receipt bytes copied from the lane** (irreducible — the pins freeze
  path+sha at `c1-r38-event-ground.py:55-84` and receipts are public lane bytes) and
  **~1.9 KB is authored wiring+hollow prose** (vs the real round's 10,595 B of prose and
  157,563 B across all eight receipts). The v3 repairs raised the crib from a 19-line
  self-receipt to "copy three files and write four Gate lines"; they did not make
  authorship provable.

## C2 — cheapest surviving TARGET_MET

### Shape A — copied real tool + honestly-forged triplet (PASSES)

Sandbox branch `c2-copytool` rev `2f64ed0`. `tools/mado-eventq.py` copied from lane HEAD
(12,129 B). Triplet forged "honestly": a hand-written 6-row `ss` table with *invented*
instance dir, inodes (555001/555002/555003) and pids; the real tool was then actually run
on it (`--disable-logs 1`, empty log/journal) and its stdout became the receipt; the proc
file names the invented inodes + `ss_sha256=<sha256 of the snapshot>` + `OVERALL: AGREE`.

Counter run (exact tail):

```
PRED-C2-r38-v3 live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
PRED-C2-r38-v3 fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET rev=2f64ed0…   RC=0
```

Cost: tool 12,129 + receipt 579 + snapshot 1,165 + proc 317 = **14,190 B** (real: 204,741 B).

### Shape B — stub tool + minimal 1-subscriber triplet (PASSES, cheapest)

Sandbox branch `c2-stub-1min` rev `a69f1e9`. A behavior-exact compact rewrite of the tool
(file-driven paths identical; 7,287 B vs 12,129 B — the case fixtures fully determine the
behavior, so "stub" and "real" are interchangeable to the counter). Triplet reduced to one
LISTEN + one server + one client + one unrelated row: receipt 482 + snapshot 803 +
proc 220 = 1,505 B.

```
PRED-C2-r38-v3 live-detail replay=1 sha=1 full_table=1 proc=2/2 sha_in=1 agree=1
PRED-C2-r38-v3 fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET rev=a69f1e9…   RC=0
```

**Cheapest surviving C2 shape: 7,287 B stub + 1,505 B triplet = 8,792 B committed.**

**Answer to "what does it cost to forge the /proc binding honestly?": 220 B** (two
`server … inode=` lines + the `ss_sha256=` line + `OVERALL: AGREE`). Read strictly, the
live clause (`c2-r38-eventq.py:179-248`) checks only: snapshot ≠ the two embedded fixture
tables (`:200`), one summary line with `subscribers>=1` equal to the client-line count and
matching `(comm,pid,fd)` triples on replay (`:219`), `tool_sha256=` naming the committed
tool (`:221`), ≥1 non-socket2 row (`:229`), and the proc text containing the snapshot's
sha + every socket2 server inode as a `\b` word + `OVERALL: AGREE` (`:241-243`). Nothing
binds any of it to the live host: the forger invents the inodes in the snapshot they
themselves wrote, so consistency is free. A degenerate hash-lookup tool (recorded outputs
per fixture input hash) would cut the tool to ~3-4 KB; not built — the behavior-exact stub
already undercuts the real tool.

### Negative controls — the clause has teeth against the demonstrated cribs

- Proc naming a wrong sha: `live-detail … sha_in=0 … live=0 verdict=TARGET_MISSED` (rc=1).
- Snapshot byte-equal to the CLEAN fixture table: `live-detail snapshot-is-fixture …
  live=0 verdict=TARGET_MISSED` (rc=1).

So the v3 repairs do reject the round-37 replay cribs; what remains is specificity, not
vacuity.

---

## Classification and cheapest closing clause

### C1 hollow-prose residual — accepted tradeoff (declared, not a defect)

The frozen registration declares it ("Residual (declared, not hidden): fully fabricated
self-consistent artifacts … still pass … they do not make live truth provable from
committed bytes") and clause l's docstring repeats it ("it is reported, not hidden").
My cribs confirm the declaration is accurate. It is **not fixable by any predicate
checkable from committed bytes**: the pinned receipts are public lane history, so copying
them is always available; any new byte-checkable clause is satisfiable by construction.
The cheapest narrowing clause (raises cost, cannot close the class): **located-quote
depth + phrase co-location** — "each admitted entry must state ≥3 distinct located quotes
per cited id (≥24 quoted bytes each), and every counted lineage phrase must appear on a
line that also states a located quote." This kills the demonstrated 1-line/2-quote hollow
shape (mine) and forces quote-bearing prose structure, but a fabricator satisfies it the
same way — it shifts the frontier, it does not close it. A true close needs an
out-of-band witness (non-author re-derivation of the quotes from the receipts at admit
time); no frozen-bytes clause provides one.

### C2 forgeable-triplet residual — accepted tradeoff (declared, not a defect)

Same declaration in the registration. The triplet verifies *internal* consistency only;
committed bytes cannot distinguish "the tool ran on the live host" from "the tool ran on
bytes the claimant authored," because the replay inputs are themselves the committed
artifacts. Even upgrading the replay to full-output equality closes nothing — my forge is
a genuine tool run on committed inputs. The cheapest narrowing clause: **proc-holder
consistency + full-output replay + comm diversity** — "every holder named in the proc
artifact for a server inode must appear in that inode's `users:(…)` list in the snapshot;
the receipt's non-`tool_sha256` bytes must equal the counter's own replay of the committed
snapshot with empty log/journal; the snapshot must name ≥2 distinct client comms." This
adds three cross-artifact invariants a forger must keep aligned, but my demonstrated crib
already satisfies all three, so it narrows only lazier forgeries. A true close needs an
external anchor (e.g. a w1 witness signature over the snapshot captured independently on
the host, verified by the counter) — or the round should formally rename the clause
"internally consistent triplet" and stop claiming live truth, which is the honest cheap
move.

## Evidence index

- Sandbox: `/tmp/mado38-CritV3Residual/sb` — branches `master` (c1 hollow, `6f48d22`),
  `crib-harvest` (`b64f1b9`), `c2-copytool` (`2f64ed0`), `c2-stub` (`9cf269e`),
  `c2-stub-1min` (`a69f1e9`), `probe`/`probe2` (negative controls, deleted).
- Counter invocations (all against the sandbox, lane counters run read-only):
  `python3 -I quality/counters/c1-r38-event-ground.py --repo <sb> --rev HEAD --base b4e47e9`
  `python3 -I quality/counters/c2-r38-eventq.py --repo <sb> --rev HEAD`
- Lane citations: pins `quality/counters/c1-r38-event-ground.py:55-84`; pin-gate match
  `:222`; lineage floor `:87`, scoring `:249-251`. Live clause
  `quality/counters/c2-r38-eventq.py:179-248`; fixture check `:200`; replay `:219`;
  tool-sha `:221`; full-table `:229`; proc check `:241-243`; conjunction `:248`.
- Installs: none.
