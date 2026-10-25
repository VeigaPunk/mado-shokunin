# RevC1Tip — C1 re-derived from bytes, and what the counter cannot see

Seat: `L1Mado35.RevC1Tip` (leaf reviewer, no dispatch). Lane: mado-shokunin. Wave 2, round 35.
Verified at **2026-10-25T03:39:33-03:00**, HEAD `02088b4` (`round-35: the idle-lock control
surface lands — three entries, eight rows S203-S210, errata, and the wave-1 evidence`).
Read-only: no lane corpus, counter, control, `SOURCES.md`, jj state or Git index was written.
Everything written lives under `.ufo/waves/round-35/scratch/RevC1Tip/` plus this file.
No tool was installed (nothing was needed).

## Axes

1. **A1 verdict** — does the assigned command print the claimed numbers on the bytes that exist now?
2. **A2 committed bytes** — does the claim survive a run over `HEAD` only, with the committed
   counter and committed frozen spec (no working-copy help)?
3. **A3 self-containment** — is any seat's output consulted at run time? (source audit + syscall trace
   + a minimal rebuild of the scored tree)
4. **A4 predicate↔code fidelity** — does each frozen clause mean what its English says?
5. **A5 failable** — can the counter report `TARGET_MISSED`, or is the verdict a tautology?
6. **A6 durability/provenance** — are the inputs the claim closes over actually committed?

## 0. Verdict up front

| Axis | Verdict | Confidence |
|---|---|---|
| A1 numbers on current bytes | **CONFIRMED** — `3 / 8 / 0`, `rc=0`, exact line in §1 | HIGH |
| A2 committed-only run | **CONFIRMED** — `git archive HEAD` → `3 / 8 / 0`, `rc=0` | HIGH |
| A3 no seat's help at run time | **CONFIRMED** — reads 12 files (192,875 B) + frozen spec; zero network syscalls; cwd-independent; deterministic ×3 | HIGH |
| A4 fidelity of `digest-match` | **FALSIFIED as coded** — receipt bytes are never hashed; a rotated receipt still closes (F1, §4.1) | HIGH |
| A4 fidelity of the row clause | **FALSIFIED as coded** — the row may sit outside `## Registry`; the lane census calls that E12 (F2, §4.2) | HIGH |
| A5 failable | **CONFIRMED** — six independent mutations each give `2 / 7 / 1` `TARGET_MISSED`, `rc=1` | HIGH |
| A6 durability | **CONFIRMED at `02088b4`** — an earlier mid-wave snapshot (`19e4ab3`) returned `0 / 0 / 8`; the commit that landed the data makes the claim reproducible from committed bytes | HIGH |

Both fidelity defects are **latent on the current bytes**: all 8 receipts do hash to their frozen
values and the 8 rows do sit inside `## Registry` (lines 205-212, between `## Registry` at 9 and
`## Paths` at 214). They are instrument defects, not data defects, and the round's numbers stand.

## 1. The assigned command, verbatim

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json; echo rc=$?
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
rc=0
```

That is the whole stdout; the stderr stream was empty. `python3 --version` → `Python 3.14.8`.

Artifact digests (sha256):

| artifact | sha256 |
|---|---|
| `.ufo/waves/round-35/c1/count.py` | `78c2589286a2d70c9b109672c85cd4e9bcb85438bc80ab888d10b73ad12abad6` |
| `.ufo/waves/round-35/c1/frozen.json` | `e18e7aef81e78fc385b3fa9d524a6c875182273517d65d97bb94c463b7743b30` |

Both working-copy files are **byte-identical to their `HEAD` blobs** (`git cat-file -p HEAD:<path> |
sha256sum` gives the same two digests), so the numbers above describe committed counter bytes and a
committed predicate. The scored data at the same moment:

| artifact | sha256 | bytes |
|---|---|---|
| `corpus/SOURCES.md` | `848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80` | 171,446 |
| `corpus/knowledge/idle-lock-never-asked-r12.md` | `7f27ced01e9edf627e2e4693ec57663fa14dd739cd8f9065cf177d0bfae4dd58` | 3,586 |
| `corpus/knowledge/idle-lock-chain-armed-r14.md` | `583c708c338ecb063f8ef38071d415c79476088f27994551fd964384be1e0bf3` | 3,768 |
| `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | `82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe` | 5,806 |

Note on a moving target: between 03:31 and 03:38 this lane was being written by other seats. My
first measurements ran against the pre-commit working copy (entries 2,078 / 1,789 / 3,428 B,
`HEAD=19e4ab3`). The report below is the **final re-run on the current bytes**; every attack that
matters was re-executed after the lane settled (§4.1, §4.2, §5, §3). The earlier transcript is kept
as `scratch/RevC1Tip/evidence.txt`; the authoritative one is `scratch/RevC1Tip/evidence2.txt`.

## 2. Independent re-derivation (A1) — own parser, no import of `count.py`

`scratch/RevC1Tip/independent_c1.py` re-implements the frozen predicate from scratch (its own file
checks, row split, cell split, cadence regexes, quote scan) and scores **both** plausible readings of
the anchor clause:

* `strictA` — anchor cell carries the digest string recorded in `frozen.json` (the counter's reading);
* `strictB` — anchor cell carries the **sha256 of the receipt bytes**, and those bytes hash to the
  frozen value (the predicate's literal reading).

```
$ python3 -I scratch/RevC1Tip/independent_c1.py . .ufo/waves/round-35/c1/frozen.json; echo rc=$?
INDEPENDENT-C1 strictA closed_entries=3 closed_rows=8 open_cites=0
INDEPENDENT-C1 strictB closed_entries=3 closed_rows=8 open_cites=0
rc=0
```

Per cite (all 8 identical in shape): exactly one row, 11 cells (NF=13 under the census's
`-F'|'`), status `mined`, opened `2026-10-24`, recheck in {`on-request`, `on-change`, `90d`}, anchor
contains both the frozen digest **and** the actual receipt digest, receipt digest == frozen digest,
exactly one `gate-quote:` line, 13-17 words, contiguous substring of the receipt bytes,
`closed_counter_reading=true`.

The frozen entry→id map is also complete against the entries' own citations: the only `S2xx`
tokens mentioned in the three entries are `S203`-`S210`, exactly the frozen set — no unlisted cite
hides behind `open_cites=0`.

Recheck legality was cross-checked against the census rather than assumed: `valid_recheck`
(`count.py:138-144`) accepts `^\d{4}-\d{2}-\d{2}$`, `^\d+d$`, and
`^[A-Za-z][A-Za-z0-9 _-]*$`; `scripts/sources-census.sh:582` defines
`symbolic(s) = s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/` and `:663-667` applies exactly ISO / `[0-9]+d` /
symbolic. No drift.

## 3. A3 — does it hold without any seat's help?

**Yes at run time.** Three independent proofs:

1. **Source audit.** `count.py` imports only `argparse, hashlib, json, os, re, stat, sys, pathlib`;
   it contains no `socket`/`urllib`/`requests`/`subprocess`; it never mentions `clauses.json`,
   `controls/`, `scratch/`, `w1/` or `w2/`. Its only data reads are `frozen.json` plus paths under
   `--root` (`count.py:156,162,168,173`).
2. **Minimal tree.** A 12-file, 192,875-byte tree containing only `corpus/SOURCES.md`, the three
   entries and the eight receipts already yields
   `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, `rc=0`. All twelve are the
   scored data — the registry, the three entries and the eight receipts; the frozen spec is the
   thirteenth input and is passed separately as `--frozen`.
3. **Syscall trace.** `strace -f -e trace=openat,stat,newfstatat` over a run of that tree: after
   excluding the interpreter's own PATH resolution, the complete read set is the counter, the frozen
   spec, and those twelve files. `strace -f -e trace=network` records **0** socket/connect/bind/send
   lines.

Determinism and environment independence: three consecutive runs on the lane tree produce the same
line (`rc=0` each), and a run launched from `/tmp` with absolute `--root`/`--frozen` produces the
same line. `python3 -I` also removes the script directory and user site-packages from `sys.path`.

The honest limit of "no seat's help": the **frozen map itself** (which entry owns which id, and the
eight receipt digests) is taken as input and never re-derived. The counter proves the tree conforms
to that map; it does not prove the map is right. F1 below shows part of the map is trusted blindly.

## 4. A4 — predicate↔code fidelity: two clauses do not mean what they say

### 4.1 F1 (medium, already reported by CritControls §5; independently reproduced): the receipt bytes are never bound

`count.py:174` computes the digest and throws it away:

```python
digest = hashlib.sha256(blob).hexdigest() if blob is not None else ""
```

AST check over `main()`: `line 174: store 'digest' loaded_later=False` — the only dead store in the
function. The only anchor test is `count.py:192`, `receipt["sha256"] in cs[5]`: a membership test of
the **manifest's recorded string** inside the row cell. Hash the receipt against nothing, and the
clause "whose anchor cell carries the sha256 **of the named receipt**" is unimplemented.

Probe (fresh tree rebuilt from the current bytes, `scratch/RevC1Tip/m1b`): append one line to
`S206.receipt.txt` after the freeze, leave every row and anchor untouched.

```
actual sha256: 889be5a1940f9d63aa40a6c8bf9e0ea637e40a1f2bda3f91bbf1dd93fae29b8c
frozen sha256: 1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5
$ python3 -I .ufo/waves/round-35/c1/count.py --root scratch/RevC1Tip/m1b --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
rc=0
```

The receipt no longer hashes to the anchor's digest, yet the cite closes. Smallest correct fix is
one conjunct after the existing anchor test: `and digest == receipt["sha256"]` (CritControls tested
the patched counter: real tree stays `3/8/0`, the corrupted-receipt tree drops to `2/7/1`).
The committed `c1-digest` control does not cover this: its deliberate defect is `S210` cell 5 →
64 zeros, i.e. it exercises the row cell, never the receipt file. The control tree's `SOURCES.md` is
a pre-data snapshot that differs from the live registry in other cells as well, so it cannot be read
as "live minus one cell" — but the receipt dimension is clean across the whole control set: in **all
ten** `c1-*` control trees, every one of the eight receipt files is byte-identical to the live file
(`cmp`, `differing=0` in each), so no committed c1 control can exercise receipt bytes at all.

### 4.2 F2 (low, not covered by any sibling report): "the registry holds … a row" is a whole-file scan

The predicate says "**the registry** holds exactly one well-formed row for that id". `rows_for`
(`count.py:118-124`) scans every line of `SOURCES.md` and matches `^ {0,3}\|\s*(S[0-9]+)\s*\|`
regardless of section. Probe (`scratch/RevC1Tip/m9b`): delete S206's only row from `## Registry`
and re-insert the identical line under `## Leads (unopened)`. Row shape, cells, used-by, status,
recheck, digest are unchanged.

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root scratch/RevC1Tip/m9b --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
rc=0
```

The lane's own registry validator disagrees on the byte-identical `SOURCES.md`
(`sha256 69783280b76522ef7a279a9ab7332930210a2685da16d9481563d639e23fe137` in both fixtures):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file …/censusB-clean/mado/corpus/SOURCES.md
file	ok	…                                   rc=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file …/censusB-m9/mado/corpus/SOURCES.md
file	E12	S206 row outside Registry section     (no ok line; rc=1)
```

Both fixtures are full lane copies (corpus, tools, quality, `.ufo`) so E11 does not contaminate the
comparison; the only difference between them is the moved row. On the live lane the census reports
`mado	ok	…/corpus/SOURCES.md`, `rc=0` (seven pre-existing W04 duplicate-URL warnings).

This is latent today: all eight rows are at lines 205-212, inside `## Registry` (9) and before
`## Paths` (214). Smallest fix: resolve the section ranges once (heading to next heading) and only
accept row lines inside `## Registry`, mirroring census E12.

Neighbour check: `MutCensusRow.md:168` explicitly says it did **not** test the outside-registry
path ("that path is E12, not E03"); `RevCensus.md:77-78` only verified that no such row exists on the
live tree. No sibling ran the C1 counter against a moved row — this finding is distinct.

## 5. A5 — the counter is failable (negative-control matrix)

Fresh trees rebuilt from the current bytes. `SOURCES.md` is the same `848a7680…` bytes as live, and
the entries' `gate-quote` lines are byte-identical to the live ones (the wave-2 edits to the entries
are 61 inserted lines with 0 deletions and do not touch a quote — verified by hashing the
`gate-quote:` line sets of `HEAD` vs worktree).

| probe | mutation | stdout | rc |
|---|---|---|---|
| M2 | S206 status `mined` → `queued` | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | 1 |
| M3 | S207 quote padded to 26 words | `2 / 7 / 1 TARGET_MISSED` | 1 |
| M5 | S205 quote replaced by text absent from the receipt | `2 / 7 / 1 TARGET_MISSED` | 1 |
| M4 | S208 used-by gains a foreign entry path | `2 / 7 / 1 TARGET_MISSED` | 1 |
| M7 | S209 receipt deleted | `2 / 7 / 1 TARGET_MISSED` | 1 |
| M8 | S210 anchor cell digest zeroed (mirrors `c1-digest`) | `2 / 7 / 1 TARGET_MISSED` | 1 |
| empty | empty tree / missing data (committed `c1-donothing` control) | `0 / 0 / 8 TARGET_MISSED` | 1 |

So the verdict is not a tautology: six load-bearing clauses were individually killed. What is *not*
killable is the receipt-bytes clause (F1) and the registry-section scoping (F2).

## 6. A6 — committed vs working bytes

`HEAD` advanced during this seat's work; both states were measured.

* **At 03:31 (HEAD `19e4ab3`):** the three entries were untracked and the eight rows existed only
  as a working-copy modification of `SOURCES.md` (`+8` lines). A tree built from `HEAD:corpus/SOURCES.md`
  plus the committed receipts and no entries returned
  `closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED`, `rc=1`. The claim then was
  reproducible from the working tree, but **not** from committed bytes.
* **At 03:38 (`HEAD 02088b4`):** the commit message is exactly "three entries, eight rows S203-S210".
  `git cat-file -e HEAD:` confirms the entries, `SOURCES.md` rows (8), counter, frozen spec and
  receipts are all tracked. A tree extracted with
  `git archive HEAD corpus/SOURCES.md corpus/knowledge/idle-lock-*.md .ufo/waves/round-35/fetch .ufo/waves/round-35/c1`
  run with the **committed** counter and **committed** frozen spec returns:

```
$ python3 -I headtree2/.ufo/waves/round-35/c1/count.py --root headtree2 --frozen headtree2/.ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
rc=0
```

The claim is therefore committed-durable at `02088b4`. The worktree still carries +61 uncommitted
lines across the three entries (wave-2 scribe work), but the claim does not depend on them: quotes
are identical, and both HEAD bytes and worktree bytes close. RevSelftest's caveat ("the C1/C2
verdicts are only durable once the wave is committed") is discharged by `02088b4`.

## 7. Residual risk and verification gaps

- **The predicate certifies wiring, not truth.** A row whose anchor and quote are honest but whose
  entry prose is fabricated still closes. `CritControls §4` already showed registry-level
  indifference (a divergent golden registry, `on-change` vs `on-request` and a changed teaches cell,
  still passes). This is a predicate-design limit, not a counter bug; fixing it needs a clause
  relating row content to entry content, which is out of scope here.
- **Quote floor is 1 word.** A single-word quote (`the`) that appears in the receipt is legal. The
  current quotes are 13-17 words, so no degenerate quote exists, but nothing prevents one.
- **F1 is the one defect that can launder fabricated evidence**: a receipt that rots or is replaced
  after the freeze keeps its cite closed as long as the appended bytes do not break quote
  substrings. Today all 8/8 receipts hash to their frozen values, so nothing is laundered yet.
- Verified only what this seat ran: I did not re-verify the host-level truth of the receipts
  (S203-S210 content against the live host) — that is the per-quote seats' lane — nor C2. I did not
  test hardlink/symlink adversarial roots beyond the committed controls (`c1-entry-symlink`,
  CritControls `hardlink-receipt`), nor counter crash paths such as a `sid` missing from
  `receipts` (the frozen spec makes that unreachable).

## 8. Reproduction

All under `.ufo/waves/round-35/scratch/RevC1Tip/`:

| path | what |
|---|---|
| `reproduce.sh` | rebuilds the minimal tree and every probe from the lane tree, including the committed-`HEAD` archive run |
| `evidence.txt` | first transcript (pre-commit working copy, `HEAD=19e4ab3`) |
| `evidence2.txt` | authoritative transcript on current bytes/`HEAD=02088b4` |
| `independent_c1.py` | own-parser re-derivation; prints `strictA`/`strictB` and per-cite facts |
| `tree/`, `tree2/` | 12-file minimal scored trees (192,875 B) |
| `m1b/`, `m9b/` | the two successful falsifications on current bytes |
| `m2/ … m8/` | negative controls from §5 |
| `headtree2/` | `git archive HEAD` extraction, run with committed counter + spec |
| `headtree/` | the earlier `19e4ab3` HEAD-only run (`0/0/8`) |
| `censusB-clean/`, `censusB-m9/` | full-lane census A/B fixtures (`ok` vs `E12`) |
| `census-ab.txt` | census A/B transcript with hashes |
| `strace.txt`, `strace-net.txt` | read-set and zero-network traces |

No package installs were required or performed (pacman stayed untouched, as directed).
