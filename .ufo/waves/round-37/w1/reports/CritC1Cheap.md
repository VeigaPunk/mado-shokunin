# CritC1Cheap — cheapest crib against PRED-C1-r37-v2

Seat: critic, mado round 37 wave 1. Lane files untouched (READ-ONLY). Tools installed: none.

## Verdict (TLDR)

**FINDING — counter defect.** The frozen C1 v2 counter reaches `admitted=2/2 verdict=TARGET_MET`
on a 766-byte, 19-line tree that opens **no source at all**. It uses a fabricated id `S999`
with one registry row, each entry is its own Gate receipt, and the quote is the single
character `"e"`. The registration says both entries "rest on rows opened this round (S189,
S201 re-opened; S212, S213, S214 new)" (registration.md:42-43). The counter does not enforce
that sentence. Three holes cause this, and each can be fixed with a frozen clause:

1. **The receipt is not pinned.** Clause d accepts any file committed at REV whose sha256
   matches the declared digest, including the entry itself.
2. **The quote has no floor.** One character, or the bare surface token, satisfies both d and g.
3. **Registry rows are not unique.** Clause c accepts any one of several rows for the same id,
   so an appended row can contradict the held one.

**The residual is a tradeoff, not a defect.** After those three holes are closed, a stub that
states the real located quotes still passes. The lane's golden-v2 control is that stub. Once
the E1 lineage clause (below) is added, the residual narrows to E2: three lines plus wiring
(`k5`). No syntactic clause separates that from an honest E2 without also failing honest
paraphrase. Treat it as an accept-path existence proof. It does not prove the counter
separates knowledge from wiring, and the judge has to close that gap by reading E2.

## Method

- Sandbox: `git clone -q --no-local --no-checkout <LANE> /dev/shm/mado37-CritC1Cheap/sb`,
  plus `git sparse-checkout set --no-cone /corpus/ /.ufo/waves/round-37/fetch/`. A full
  checkout failed on the `/dev/shm` per-user quota (`Disk quota exceeded (os error 122)`;
  `findmnt` shows `usrquota`, and the shared filesystem was at 65% use from sibling seats).
  The counter reads only through `git show`, so a sparse tree scores the same.
  Sandbox identity is `sandbox@invalid`. Every crib is committed on a detached HEAD at base
  `b4e47e980bfb0cbc8a4e788f59a41db858751fd8`.
- Builder: `.ufo/waves/round-37/w1/scratch/CritC1Cheap/cribs.py`. Its helpers follow
  `controls.py` (`wire`, `row`, `entry`, `QUOTES`).
- Scorer: the lane's frozen counter, run unmodified
  (sha256 `1c21f8ba736bf8c17eeab4d485c9101ba98436d17bad4dfe73a66bededb6294f`):
  `python3 -I quality/counters/c1-r37-event-ground.py --repo <sb> --rev <crib> --base b4e47e9…`.
- Clause test: `.ufo/waves/round-37/w1/scratch/CritC1Cheap/c1-hardened.py`, a scratch copy
  of the counter with 38 changed lines. It adds clause **h** with switchable parts:
  `p` pin, `q` quote floor, `u` unique row, `l` E1 lineage. The PRED string is renamed so it
  cannot be mistaken for the lane predicate.
- Run: `cd /dev/shm/mado37-CritC1Cheap && python3 -B <scratch>/cribs.py > run2.txt`. Exit 0,
  wall time 2.6 s. The full output is in `/dev/shm/mado37-CritC1Cheap/run2.txt`.

## Cribs and costs (frozen counter)

The cost counts lines and bytes added under `corpus/` (`git diff --numstat` and `-U0` against
base). Receipt bytes copied from the lane's `fetch/` are counted separately.

| tree | corpus lines | corpus bytes | receipt bytes | frozen v2 |
|---|---|---|---|---|
| `k2_self_receipt`: fabricated S999, entries are their own receipts, quote `"e"` | 19 | 766 | 0 | **2/2 TARGET_MET** |
| `k1_real_min`: S189 / S214 only, quote = surface token, appended contradicting S189 row | 20 | 879 | 8,268 | **2/2 TARGET_MET** |
| `k3_receipt_reading`: real quotes; E2 lifts S213's own "reading" sentence | 21 | 2,325 | 10,082 | **2/2 TARGET_MET** |
| `k0_golden_v2`: the lane control, rebuilt | 35 | 2,348 | 58,024 | 2/2 TARGET_MET |
| `k5_pkg_plus_e2_stub`: honest-proxy E1 plus a 3-line stated-quote E2 | 85 | 6,113 | 58,024 | 2/2 TARGET_MET |
| `h2_honest`: honest proxy (E1 re-grounded, lane-authored E2) | 110 | 7,039 | 58,024 | 2/2 TARGET_MET |
| `h3_honest_trimmed`: h2 without the preamble and merge note | 102 | 6,571 | 58,024 | 2/2 TARGET_MET |
| `h1_pkg_renumbered`: package entry with ids renumbered only | 104 | 6,749 | 58,024 | 1/2 (E1 `g=0`) |

Quoted output for the cheapest crib:

```
== k2_self_receipt rev=7753a82059e8d87a1ca01a53e725cbb70afd73b2 files=5 corpus_added_lines=19 corpus_added_bytes=766 copied_receipt_bytes=0
   [frozen rc=0] v2 entry=event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S999 ok=1
   [frozen rc=0] v2 entry=event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S999 ok=1
   [frozen rc=0] v2 admitted=2/2 verdict=TARGET_MET rev=7753a82059e8d87a1ca01a53e725cbb70afd73b2 base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
```

The whole crib, as committed in the sandbox (`git show 7753a82:<path>`):

```
corpus/knowledge/event-delivery-limits-r26.md:
source: S999
verified-at: x
recheck: x
MAX_QUEUED_EVENTS overflowed event queue
**OBS** S999

corpus/lessons/round-37.md:
## Gate
GATE S999 receipt=corpus/knowledge/event-delivery-limits-r26.md sha256=33f886e1…0727 quote="e"
GATE S999 receipt=corpus/knowledge/event-queue-observability-r37.md sha256=38dd9f7a…ba47 quote="e"
```

E2 has the same shape. The other files are one `| S999 | … | mined | … | E1, E2 |` row and
two `## Coverage map` rows.

**Work the crib skips:** opening any source, re-grounding the package entry, locating any
quote, stating any mechanism, inference or unknown, and any value for `verified-at` or
`recheck` (`x` passes clause b).

## Per-item findings

| # | item | verdict | pointer |
|---|---|---|---|
| F1 | The receipt can be any committed file, including the entry itself, and the id can be fabricated | **FAIL (defect)** | counter :144-149; `k2` above |
| F2 | The quote floor is one character, or the bare token (`"MAX_QUEUED_EVENTS"`); this satisfies d and g together | **FAIL (defect)** | counter :147 checks only `<= 25` words; `k1`, `k2` |
| F3 | Duplicate registry rows are accepted (`rows.setdefault(...).append`, then `any(...)`), so a second S189 row with a contradicting URL passes c | **FAIL (defect, duplicate authority)** | counter :85, :135-138; `k1` has `S189_rows=2` |
| F4 | The lane's golden-v2 control relies on F3: `controls.py` `wire` appends new rows for held S189 and S201 rather than extending `used-by` | **finding** | controls.py:69-76; `c75ea05 S189_rows=2 S201_rows=2`. The renumber map says "`used-by` extended" (renumber-map.md:19-20), so golden-v2 does not model the honest path |
| F5 | A stated-quote stub (golden-v2, `k3`, `k5`) meets. Apart from the inference prose, honest and crib differ only in content no mechanical clause checks | **tradeoff** | `k5` passes every hardened clause (below) |
| F6 | Honest-entry trap: the package entry renumbered as-is fails g. Its OBS paragraphs wrap ids onto continuation lines, and no OBS line names S201 or S212 | **finding (honest-kill risk, not a defect)** | `h1` E1 `g=0`; package lines 50-52 put the ids two lines below `**OBS**`. The seat writing E1 must add an OBS line that names each of S189, S201 and S212 on the same line, and states that id's Gate quote verbatim |
| F7 | The S213 receipt is lane-authored (renumber-map: "own-work"). Its `## reading` paragraph states the whole E2 inference in 15 quotable words, so E2 can be lifted from the receipt | **finding** | S213.receipt.txt:31 (last sentence); `k3` |

## Clause test (scratch hardened counter, same trees)

Clauses:

- **h-p (pin)**: every cited id has a frozen `(receipt path, sha256)` pin from the
  renumber-map digests. Only Gates that match the pin count for d, f and g. Each entry must
  cite its required ids: E1 ⊇ {S189}, E2 ⊇ {S213, S214}.
- **h-q (quote floor)**: the quote is not a bare surface token, and is at least 3 words or
  at least 24 characters.
- **h-u (unique row)**: each cited id has exactly one `## Registry` row.
- **h-l (E1 lineage)**: E1 contains at least 4 of 7 frozen, id-free package claim phrases,
  compared case-, `*`- and backtick-insensitively.

| tree | frozen v2 | h = p+q+u | h = p+q+u+l |
|---|---|---|---|
| k2 self-receipt | MET | MISSED 0/2 | MISSED 0/2 |
| k1 real-min + duplicate row | MET | MISSED 0/2 | MISSED 0/2 |
| k3 receipt-reading | MET | MET | MISSED 1/2 (E1 `lineage=0/7`) |
| k0 golden-v2 (duplicate rows) | MET | MISSED 1/2 (E1 `h=0`, u) | MISSED 1/2 |
| k5 package E1 + 3-line E2 stub | MET | MET | **MET** (residual) |
| h2 honest | MET | **MET** | **MET** (E1 `lineage=7/7`) |
| h3 honest trimmed | MET | **MET** | **MET** (E1 `lineage=7/7`) |
| h1 renumbered only | 1/2 | 1/2 | 1/2 (E1 `g=0`, which is correct: not re-grounded) |

Quoted honest-proxy lines:
`[hard-pqul rc=0] hardened-scratch entry=event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 ids=S189,S201,S212 lineage=7/7 clauses=lpqu ok=1`
and `[hard-pqul rc=0] hardened-scratch admitted=2/2 verdict=TARGET_MET rev=7ce9e0dd…`.

## Judgement

- **Is the crib meaningfully cheaper than honest work?** Yes, for F1 to F3. `k2` costs
  766 B and no source. The honest proxy costs about 7 KB, and it rests on five opened
  receipts and located quotes. That is a counter defect: the registration's "Sourced"
  sentence is false under `k2`.
- **Is golden-v2 passing acceptable?** As a control proving the accept path exists, yes.
  As evidence that C1 measures admitted coverage, no. Golden-v2 also depends on duplicate
  rows (F4), so it is not even the honest wiring. With h-l, a stated-quote stub cannot pass
  as E1 unless it carries the package's claims, and carrying them is the assimilation act.
  E2 has no lineage source. A 3-line E2 that states the S213 and S214 quotes (`k5`) passes
  every clause that does not also fail honest paraphrase, and S213's own "reading" line
  (F7) makes even the inference liftable. That residual is a tradeoff for the judge, not a
  fixable counter defect.

## Smallest safe correction

**1. Freeze clause h (p, q, u), then add l.** This kills `k0`, `k1`, `k2` and `k3` and keeps
both honest proxies.

- **p**: pin only the required ids (S189 `eea605df…540d`, S213 `1c1b0ce1…ce58`, S214
  `d04e3a2f…b868`; add S201 `799bf02f…4f9e` and S212 `1e19d926…d7e9` if E1 must keep them),
  and require each extra cited id's receipt to live under `.ufo/waves/round-37/fetch/`. Do
  not pin the whole cited set to exactly five ids. New receipts are already appearing
  untracked in the lane (`?? .ufo/waves/round-37/fetch/S215.bin`, `S216.bin` in
  `git status --porcelain`), and a closed set would fail an honest entry that cites them.
- **u** also requires `controls.py` golden-v2 to extend `used-by` on the held S189 and S201
  rows instead of appending new rows. Without that change the accept control flips to
  MISSED (shown above).
- **l** is E1 only. Its risk is that an honest rewrite in fresh words drops below 4 of 7
  phrases, so the phrase list must be frozen together with that threshold.

**2. Governance.** Registration.md:5-6 makes any counter change a new predicate, and wave-1
seats are already dispatched. Amending to v3 is legitimate only if no target entry, row or
Gate line has landed at the lane tip yet. That timing is the judge's decision, not mine. If
v3 is refused, the judge must manually check, at the measured tip:

- every Gate receipt path is under `fetch/` and its digest matches renumber-map;
- each cited id has exactly one Registry row;
- E2 says more than its quotes.

**3. For the E1 seat (F6).** The re-grounded package entry needs one OBS line per id
(S189, S201, S212), and each must state that id's Gate quote verbatim. Renumbering alone
yields `g=0`.

Impacted axes: coverage (C1 claim validity). Operability: not touched.

## Scratch left

- `.ufo/waves/round-37/w1/scratch/CritC1Cheap/cribs.py`
- `.ufo/waves/round-37/w1/scratch/CritC1Cheap/c1-hardened.py`
- `/dev/shm/mado37-CritC1Cheap/` (sandbox, 26M, plus `run1.txt` and `run2.txt`)

No lane production file, jj state, git index, socket or compositor was touched.
