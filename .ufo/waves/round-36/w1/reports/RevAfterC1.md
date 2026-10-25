# RevAfterC1 — the C1 measurement reproduces exactly; its c1 control set does not exercise the repair it is cited for

Seat: `RevAfterC1` (reviewer, leaf, no dispatch). Round 36, wave 1, residual attack pass.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. All writes confined to
`.ufo/waves/round-36/scratch/RevAfterC1/`, `/tmp` and this report. No production file,
counter, frozen spec, control tree, `LOG.md`, `SCORECARD.md`, `quality/` or `corpus/` artifact
was modified; no git command that mutates state was run; no tool was installed.

## Axes

1. **Arithmetic** — does `--profile r36` read 25/25 and exit 0?
2. **Contrast** — does `--profile r35` read 14/25 and exit 1?
3. **Receipt agreement** — do both runs match the committed receipts control-for-control?
4. **Accept side** — are the three accepts load-bearing, and what single input separates each
   from its nearest reject?
5. **Reuse** — can the round-35 code reach `correct == controls` under the gate's selector?
6. *(opened by 4)* **Clause exercise** — does the landed control set actually exercise the
   clauses the round claims it repairs?

---

## 1. `--profile r36` → 25/25, exit 0 — CONFIRMED

```sh
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ python3 -I quality/check-counter-discrimination.py --profile r36 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --receipts /tmp/res-disc --mutants /tmp/mut-r36-revA
…
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 \
  label='round-36 repaired counters' verdict=TARGET_MET
EXIT=0
```

All 25 rows `ok=1`; the ten clause rows read `controls=N missed=N` (full ledger in
`scratch/RevAfterC1/run-r36-*.log`). Run twice, at two different revisions (§3), identical.

## 2. `--profile r35` → 14/25, exit 1 — CONFIRMED

```sh
$ python3 -I quality/check-counter-discrimination.py --profile r35 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --receipts /tmp/res-disc-r35 --mutants /tmp/mut-r35-revA
…
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=14/25 \
  label='round-35 frozen counters (unmodified)' verdict=TARGET_MISSED
EXIT=1
```

The eleven misses are exactly the round-35 defects, quoted from the run:

```
control=c1-shape-only            … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-fabricated-payload     … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-no-registry-heading    … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-row-moved-out          … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-tip-stale              … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-tip-one-copy           … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-blob-corrupt           … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-blob-row-deleted       … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-clause-deleted         … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-receipt-token          … expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-receipt-unbound        … expected=TARGET_MISSED observed=TARGET_MET ok=0
```

Note `c1-digest` is **not** among them: the round-35 counter still catches a mutated
anchor *cell* (`receipt["sha256"] in cs[5]`, `.ufo/waves/round-35/c1/count.py:192`), so the
D3 defect is only visible through payload controls — of which the r35 profile fails two.

## 3. Both runs against the committed receipts — 25/25 control lines match

```sh
$ diff <(grep '^control=' /tmp/revA-r36.log) \
       <(grep '^control=' .ufo/waves/round-36/receipts/after-discrimination.txt)
(no output)                                   # R36_CONTROL_LINES_IDENTICAL
$ diff <(grep -E '^(clause=|MADO_DISCRIMINATION)' /tmp/revA-r36.log) \
       <(grep -E '^(clause=|MADO_DISCRIMINATION)' .ufo/waves/round-36/receipts/after-discrimination.txt)
(no output)                                   # R36_CLAUSE_AND_VERDICT_IDENTICAL
$ diff <(grep '^control=' /tmp/revA-r35.log) \
       <(grep '^control=' .ufo/waves/round-36/receipts/before-discrimination.txt)
(no output)                                   # R35_CONTROL_LINES_IDENTICAL
$ diff <(grep -E '^(clause=|MADO_DISCRIMINATION)' /tmp/revA-r35.log) \
       <(grep -E '^(clause=|MADO_DISCRIMINATION)' .ufo/waves/round-36/receipts/before-discrimination.txt)
(no output)                                   # R35_CLAUSE_AND_VERDICT_IDENTICAL
```

Per-control receipts too: the generated file set is identical (`diff <(ls …) <(ls …)` empty,
25 names each side), and every file's body — header, `instrument=…` line, counter stdout,
`exit=`, fixture block — is byte-identical, except the `$` argv line, which differs only in
the `--mutants` path I chose:

```sh
$ diff <(grep '^\$ ' /tmp/res-disc/c1-live.txt | sed 's#/tmp/mut-r36-revA#[MUT]#g') \
       <(grep '^\$ ' .ufo/waves/round-36/controls/receipts/c1-live.txt | sed 's#/tmp/mut-r36-revA#[MUT]#g')
(no output)                                   # same_cmdline
```

Loop result: `r36_bodies_checked` / `r35_bodies_checked` with no `DIFF:` line. The gate is
reproducible to the byte.

**Revision drift observed during the review (not mine).** When this seat opened, `HEAD` was
`2d90524` and the receipts cited `cf175c7`; while I was running, a peer advanced `HEAD` to
`a5f76c9` and rewrote three record files. Current tree state:

```sh
$ git status --porcelain
 M .ufo/waves/round-36/fetch/S211.receipt.txt
 M .ufo/waves/round-36/receipts/after-discrimination.txt
 M .ufo/waves/round-36/receipts/after-pointers.txt
 M .ufo/waves/round-36/w1/reports/RevSourceS211.md
 M corpus/lessons/round-36.md
$ git diff .ufo/waves/round-36/receipts/after-discrimination.txt | head -6
-# C1 after-state — PRED-C1-r36-v1 discrimination at cf175c7…
+# C1 after-state — PRED-C1-r36-v1 discrimination at a5f76c9…
```

I re-ran both profiles at `a5f76c9` and re-diffed: the control lines are still identical, to
the working-tree receipt and to `HEAD:` — i.e. the rewrite touched the header line only.
The 25/25 is stable across both revisions. None of the discrimination inputs
(`quality/counters/*`, `.ufo/waves/round-36/{c1,c2}/*`, `controls/**`, the manifest) appear
in `git status`; the drift is confined to record text.

## 4. The accept side — all three accepts are load-bearing

### 4a. Measured distance from each accept to every reject

Scored over exactly the files the counter reads (`corpus/SOURCES.md` + 3 entries + 8 receipts
for c1; clause ledger + blob ledger + 10 receipts for c2), diffed line-wise:

| accept | nearest reject | files | opcodes | ±chars |
|---|---|---|---|---|
| `c1-golden-r36` | `c1-no-registry-heading` | 1 | 1 | 149 |
| `c1-golden-r36` | `c1-row-moved-out` (next) | 1 | 2 | 1525 |
| `c1-live` | every committed reject ≥ | 4 | 2 | 171227 |
| `c2-live` | `c2-blob-row-deleted` | 1 row | 1 | 87 |
| `c2-live` | `c2-tip-one-copy` | 1 line | 1 | 126 |
| `c2-live` | `c2-blob-corrupt` | 1 line | 1 | 168 |

### 4b. `c1-golden-r36` — separated by exactly one input: the `## Registry` heading line

Its nearest reject is the round-35 golden tree, which is byte-identical except that it lacks
the round-36 header. Adding back **only** the heading line converts the reject:

```sh
$ cp -a .ufo/waves/round-35/controls/golden /tmp/hdr-one
$ python3 - <<'EOF'
from pathlib import Path
p = Path("/tmp/hdr-one/corpus/SOURCES.md"); p.write_text("## Registry\n\n" + p.read_text())
EOF
$ diff .ufo/waves/round-35/controls/golden/corpus/SOURCES.md /tmp/hdr-one/corpus/SOURCES.md
0a1,2
> ## Registry
> 
$ python3 -I quality/counters/c1-idle-lock.py --root /tmp/hdr-one \
    --frozen .ufo/waves/round-36/c1/frozen.json
PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

Unmodified, the same tree is the committed control:

```
control=c1-no-registry-heading … expected=TARGET_MISSED observed=TARGET_MISSED ok=1
PRED-C1-r36-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
exit=1
```

**Separating input: one line, `## Registry`, in `corpus/SOURCES.md`. Not trivially satisfied.**

### 4c. `c1-live` — no committed reject is one input away; a one-cell edit flips it

Every committed c1 reject sits on the golden lineage, not on live bytes, so the nearest is
≥4 files and ≥171 KB of textual distance (table 4a). The nearest *constructible* reject is one
registry cell. Two minimal, independent flips on a faithful mirror of the live read set:

```sh
$ # mirror of the 12 files the counter reads, unchanged
$ python3 -I quality/counters/c1-idle-lock.py --root /tmp/live-acc --frozen …/round-36/c1/frozen.json
PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   (control)
```

| one input changed in `corpus/SOURCES.md` | difflib opcodes | observed |
|---|---|---|
| S203 status cell `mined` → `queued` (one token) | 1 | `closed_entries=2 closed_rows=7 open_cites=1 TARGET_MISSED` rc 1 |
| one character of the declared S205 receipt sha (`f3387bfc…`) in the anchor cell | 1 | `closed_entries=2 closed_rows=7 open_cites=1 TARGET_MISSED` rc 1 |

**Separating input: a single registry cell — the status token, or one hex character of the
anchor's receipt digest. Not trivially satisfied.**

Probe that was *not* a digest flip (recorded so the table above is not over-read): the S205
row carries two 64-hex tokens — the source digest `e7d3b8dd…` and the receipt digest
`f3387bfc…`. Flipping the first one leaves the counter `TARGET_MET`, correctly: the clause is
about the receipt's digest, and the source digest is quoted evidence the predicate does not
bind. That is a property of the predicate, not a pass.

### 4d. `c2-live` — separated by a single 40-hex token, or a single row, or a single receipt

```sh
$ python3 -I quality/counters/c2-ledger.py --repo /tmp/c2-acc --frozen …/round-36/c2/frozen.json   # GIT_DIR=<lane>/.git
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived      (control)
```

| one input changed | changed files vs live | observed |
|---|---|---|
| one tip-labelled 40-hex token → `fa7ba113…` | blob ledger only | `uncovered=0 retired=1 tip_ok=0 TARGET_MISSED` rc 1 |
| one table row's blob id (`.ufo/waves/round-33/c1/count.py`) → zeros | blob ledger only | `tip_ok=0`, `tip: blob drift …: doc 0000… tip 4ab3db43…` rc 1 |
| one receipt file → `verdict=TARGET_MISSED\n` | that receipt only | `uncovered=1 retired=1 tip_ok=1`, `uncovered: entry-regular receipt does not bind clause and control` rc 1 |

The committed neighbours agree with the measured distance table: `c2-blob-row-deleted` (one
row) is the smallest edit, `c2-tip-one-copy` and `c2-blob-corrupt` are one token each.

**Separating input: one 40-hex token in the blob ledger (nearest by token count), or one table
row (nearest by changed bytes). Not trivially satisfied.**

### 4e. What 4b–4d do *not* establish

The positive controls pass, and each flips on a one-input change, so none is vacuous. But the
c1 reject set is degenerate in a way that matters — see finding **F1**: 13 of the 14 c1 rejects
return the identical observable `0/0/8`, so the c1 half of the score is effectively a one-bit
test on the heading.

## 5. Can the round-35 code reach `correct == controls`? — No

**(a) Through the only selector it scores 14/25.** `--profile r35` is the sole mapping to
`.ufo/waves/round-35/c1/count.py` and `…/c2/count.py`; it exits 1 (§2).

**(b) Mixing the old code with the new frozen spec is impossible by construction.** Every
counter pins its own predicate string against the spec it is handed:

```sh
$ python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen …/round-36/c1/frozen.json
PRED-C1-r35-v1 error=predicate-drift                                    exit=2
$ python3 -I quality/counters/c1-idle-lock.py --root . --frozen …/round-35/c1/frozen.json
PRED-C1-r36-v1 error=predicate-drift                                    exit=2
$ GIT_DIR=$PWD/.git python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen …/round-36/c2/frozen.json
PRED-C2-r35-v1 error=predicate-drift                                    exit=2
$ GIT_DIR=$PWD/.git python3 -I quality/counters/c2-ledger.py --repo . --frozen …/round-35/c2/frozen.json
PRED-C2-r36-v1 error=predicate-drift                                    exit=2
```

`observed_of` maps `rc == 2` to `ERROR`, never to `ok` (`check-counter-discrimination.py:69-72`),
so no mixed pair can contribute a correct row.

**(c) The selector table itself** is two literal entries, and the r35 entry pairs the old
script with the old frozen file — there is no r35-script + r36-frozen cell:

```
PROFILES keys: ['r35', 'r36']
  r35 -> .ufo/waves/round-35/c1/count.py | .ufo/waves/round-35/c1/frozen.json || .ufo/waves/round-35/c2/count.py
  r36 -> quality/counters/c1-idle-lock.py | .ufo/waves/round-36/c1/frozen.json || quality/counters/c2-ledger.py
```

**Answer: no.** Unmodified round-35 code is reachable only via `--profile r35`, where it scores
14/25 and exits 1; any attempt to reuse it against the round-36 specs is rejected as
`predicate-drift` (exit 2 → `ERROR`). A *modified* counter is by definition a different
instrument and would need a new profile entry — an edit to the gate that the landed measurement
does not contain.

One caveat carried into F5: the gate scores the printed verdict token, not the exit code, for
`rc ∈ {0,1}`.

## 6. Findings (severity order)

### F1 — MEDIUM: nine of the fourteen c1 rejects are killed by the missing `## Registry` heading, not by the mutation they are named for; ten of eleven c1 clauses are unexercised

Root cause: those rejects are derived from `.ufo/waves/round-35/controls/golden`, which has no
`## Registry` heading — the very defect that `c1-no-registry-heading` exists to test. The
counter therefore stops at the section rule and never reaches the cell each control mutates.

Observables on the **committed** trees (r36):

```
c1-donothing         0/0/8 MISSED     c1-digest            0/0/8 MISSED
c1-entry-symlink     0/0/8 MISSED     c1-quote-absent      0/0/8 MISSED
c1-quote-long        0/0/8 MISSED     c1-recheck-prose     0/0/8 MISSED
c1-row-duplicate     0/0/8 MISSED     c1-row-extra-field   0/0/8 MISSED
c1-status-queued     0/0/8 MISSED     c1-usedby-extra      0/0/8 MISSED
c1-shape-only        0/0/8 MISSED     c1-fabricated-payload 0/0/8 MISSED
c1-no-registry-heading 0/0/8 MISSED   c1-row-moved-out     2/7/1 MISSED
```

Thirteen of fourteen rejects are byte-identical on the counter's only surface, and identical
to the empty-corpus control. (Round 35's counter showed `2/7/1` on nine of them because it
scanned rows anywhere; r36's is more correct and less informative here.)

Proven by clause deletion — each repair removed alone from a `/tmp` copy, then all 16 c1
controls re-run:

```
status-mined             agreement=16/16 SURVIVES
recheck-valid            agreement=16/16 SURVIVES
used-by-exact            agreement=16/16 SURVIVES
row-well-formed          agreement=16/16 SURVIVES
row-unique               agreement=16/16 SURVIVES
gate-quote-word-bound    agreement=16/16 SURVIVES
digest-match(payload)    agreement=16/16 SURVIVES
digest-match(anchor)     agreement=16/16 SURVIVES
gate-quote-substring     agreement=16/16 SURVIVES
row-in-registry          agreement=14/16 killed by: c1-no-registry-heading, c1-row-moved-out
```

And the sharpest form — **the unmodified round-35 c1 counter with only the section rule
added**, still missing `digest == receipt["sha256"]`:

```sh
$ python3 - <<'EOF'   # r35 count.py + registry_section()/rows_for() restricted to it
… assert patched.count("digest == receipt") == 0 …
EOF
r35 c1 code + section rule only: 16/16 c1 controls  diffs=[]
```

So the c1 half of 25/25 is consistent with an instrument that repairs only `row-in-registry`.
The D3 digest repair — the round-35 defect C1 exists to falsify — is not falsified by any
landed c1 control, because the only payload controls (`c1-shape-only`,
`c1-fabricated-payload`) are also missing the heading.

**Not a false pass.** Every control really is `MISSED`, and the counter really is repaired
(`and digest == receipt["sha256"]` is present at `c1-idle-lock.py:194`, and the payload probes
below show it firing). What fails is
the inference "25/25 shows each repaired clause is load-bearing". Clause attribution *is*
recoverable, and I recovered it: normalizing the shared heading on each reject tree gives
exactly one open cite, on the row the control names —

```
c1-digest                  -> [('S210', 'anchor-string-missing')]
c1-entry-symlink           -> [('S205', 'gate-quote-missing')]
c1-quote-absent            -> [('S206', 'quote-not-substring')]
c1-quote-long              -> [('S203', 'quote-words=35')]
c1-recheck-prose           -> [('S209', "recheck='90d - re-verify the fetch'")]
c1-row-duplicate           -> [('S205', 'rows=2(need 1 in ##Registry)')]
c1-row-extra-field         -> [('S206', 'cells=12')]
c1-status-queued           -> [('S208', "status='queued'")]
c1-usedby-extra            -> [('S207', "usedby!=['…idle-lock-offered-in-the-bar-r15.md']")]
c1-shape-only              -> 8× 'digest-mismatch'
c1-fabricated-payload      -> 8× 'digest-mismatch'
c1-no-registry-heading     -> []   (MET once the heading is restored)
c1-row-moved-out           -> [('S206', 'rows=0(need 1 in ##Registry)')]
```

Every clause is live in the code; the *manifest* is what fails to exercise nine of them.
Smallest repair that does not weaken the claim: add one r36-lineage control per cell (the
golden-r36 tree with one cell changed), or simply give the nine round-35-lineage trees the
`## Registry` heading — after which they keep `MISSED` and their receipts become
attributable.

Related and smaller: `c1-entry-symlink` cannot separate `entry-regular` from
`gate-quote-substring` — an unreadable entry has no quote, so both die together (the
same double-kill round-35 `CritControls` §2 recorded). `c1-quote-absent` separates
`gate-quote-substring`, but nothing isolates `entry-regular`: a counter that followed
symlinks would still reject that tree, because the link target carries no S205 quote.

### F2 — MEDIUM: the manifest's "each differ from an accept control in exactly one committed input" is false for nine c1 rejects (and three whole-tree controls)

Measured against the only accept they are near: `c1-golden-r36`.

| reject class | inputs differing from the accept |
|---|---|
| `c1-row-moved-out` | 1 (S206 row moved to `## Leads (unopened)`) |
| `c1-no-registry-heading` | 1 (the `## Registry` heading) |
| the nine single-cell controls | 2 (heading **and** the named cell) |
| `c1-donothing` | 4 files (whole corpus absent) |
| `c1-shape-only` | 4 files (registry + 3 entries replaced) |
| `c1-fabricated-payload` | 12 files (registry + entries + all 8 receipts replaced) |

This is F1's other face: because those nine trees carry a second, dominating kill, their
committed `observed=TARGET_MISSED` is over-determined and the manifest note overstates the
design. The `--profile r35` receipt is unaffected (r35 ignores the heading), which is why the
gap is invisible in the before/after pair.

### F3 — LOW: the `## Registry` section test is a prefix match, so a row outside the canonical section can still score

`quality/counters/c1-idle-lock.py:112`:

```python
keep = line.strip().lower().startswith("## registry")
```

Probe — take the `c1-row-moved-out` tree and rename its holding heading:

```sh
$ # "## Leads (unopened)" → "## Registry archive"   (row still outside the canonical section)
PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   rc 0
$ # "## Leads (unopened)" → "## Registry"            (row now genuinely inside)
PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   rc 0
```

The clause reads "the `## Registry` section of the registry holds exactly one well-formed row";
the code accepts any level-2 heading whose text begins with `registry`. The live tree is
unaffected (one exact `## Registry`, `corpus/SOURCES.md:9`), so 25/25 stands; no control covers
the looseness, and a future one could. Equality (`== "## registry"` after strip) closes it.

### F4 — LOW: the receipts do not bind the manifest bytes

`sha256(.ufo/waves/round-36/controls/manifest.json)` =
`cace34b4f041ea4d68c738b700aa83ee635c814a0a9be816bb9ecd5f84418ab7`; that digest appears in
**0** files in the lane. Both receipts name the manifest by path and id only, as does every
per-control receipt header. So "25/25 on MANIFEST-r36-v1" reproduces against a path, not
against frozen bytes, and the manifest's own "Frozen before any round-36 data" claim is not
checkable from the committed artifacts. Recording the digest in the two receipts (or in the
manifest's consumers) would close it. My run re-derived identical lines from the same bytes,
so this is provenance, not a measurement defect.

### F5 — LOW (residual): the gate scores the verdict token over the exit code for `rc ∈ {0,1}`

`check-counter-discrimination.py:68-72` returns `ERROR` only for `rc == 2`, then trusts the
last `verdict=` token. Called directly on the module:

```
observed_of(0,'verdict=TARGET_MET')    = TARGET_MET
observed_of(1,'verdict=TARGET_MET')    = TARGET_MET
observed_of(1,'verdict=TARGET_MISSED') = TARGET_MISSED
observed_of(2,'verdict=TARGET_MET')    = ERROR
observed_of(124,'<timeout>')           = ERROR
```

Inert for both landed counters (all 50 runs across both profiles had stdout and exit in
agreement — visible in the `exit=` line of every receipt). But a counter that printed a
`TARGET_MET` line and then died would be scored `TARGET_MET`. Requiring agreement between
token and exit code would cost one `if`.

### F6 — LOW (fixture hygiene): every c2 fixture carries an extra 1-byte input

`gen-mutants.py` writes the clause ledger as `json.dumps(ledger, indent=1) + "\n"`; the
committed `.ufo/waves/round-36/c2/clauses.json` has no trailing newline. Consequence:

```sh
$ tail -c 20 .ufo/waves/round-36/c2/clauses.json | xxd | tail -1
… .".}                       # ends `}` — no newline
$ tail -c 20 /tmp/mut-r36-revA/c2-tip-one-copy/.ufo/waves/round-36/c2/clauses.json | xxd | tail -1
… ".}.                       # ends `}\n`
```

Every fixture's clause ledger is `+1` byte versus live (measured: `clause_delta=1` on the six
kinds that do not touch it), so no fixture differs from live in exactly one committed input —
contradicting the generator's own docstring — and `mutation.txt` consequently lists
`changed=['…/clauses.json', '…/RevFrozenBlobs-r36.md']` for `tip-*`/`blob-*`, though only the
blob carries the mutation. Semantically inert (the counter parses JSON), and the verdicts are
unaffected; it is a label that overstates the fixtures' surgical quality.

## 7. Also measured, no finding

- **c2 clause exercise is much better than c1's.** Removing one c2 rule at a time:

```
live-set-pinned         8/9  killed by: c2-clause-deleted
row-blob-rederived      8/9  killed by: c2-blob-corrupt
row-set-equals-frozen   8/9  killed by: c2-blob-row-deleted
receipt-names-clause    9/9  SURVIVES
receipt-names-control   9/9  SURVIVES
min-tip-lines           9/9  SURVIVES
retired-ids-frozen      9/9  SURVIVES
declared-exactly-one    9/9  SURVIVES
```

The tip-token rule is exercised too (both tip controls flip `tip_ok` 1→0, quoted in §4d). The
four survivors are individually unexercised: the clause/control naming pair is only jointly
testable (`c2-receipt-unbound` is killed by the control-id check, and `c2-receipt-token` by
the absence of both), and `min_tip_lines` / retired-id freeze / `declared == 1` have no
control at all. These are coverage gaps of the same kind as F1 but with no consequence for the
score, since nothing in the round claims those three are falsified.
- **Exit/verdict agreement:** every `count=25` row's `ok` matches its counter's `exit=` line in
  the per-control receipts, both profiles — no row passes on a crash.
- **`c1-live` vs `c1-golden-r36`** are both `MET` but are not the same bytes (live carries the
  round-35 errata and ~440 more registry rows); both accepts are needed, and both are
  sensitive to a one-cell change (§4b–4c).

## Verdict

- **§1 (25/25, exit 0):** CONFIRMED, twice, at two revisions, byte-identical to the committed
  receipt.
- **§2 (14/25, exit 1):** CONFIRMED, byte-identical to the committed receipt, and the eleven
  misses are exactly the round-35 defects.
- **§3:** CONFIRMED for all 25 control lines and all 25 per-control receipt bodies; only the
  `$` argv's `--mutants` path differs. The receipts' header revision moved from `cf175c7` to
  `a5f76c9` mid-review (peer commit, header line only); the score is invariant to it.
- **§4:** the three accepts are load-bearing — each separates from a nearest reject by one
  input (heading line; one registry cell; one 40-hex token / one table row / one receipt) and
  flips `MET`→`MISSED` on it.
- **§5:** the round-35 code cannot reach `correct == controls`: 14/25 via its only selector, and
  `predicate-drift` (exit 2 → `ERROR`) against every round-36 spec.
- **F1 is the finding that matters:** the c1 half of the score is carried entirely by
  `row-in-registry`. Nine of ten other repaired c1 clauses can be deleted with 16/16 intact,
  and the unmodified round-35 c1 code plus that one rule also scores 16/16. The gate is
  honest; the control *base* is wrong for the clause it is cited to exercise.

## Residual risk / verification gaps

- F1 and F2 bound what the 25/25 *proves*, not what it *says*: the number and the receipts are
  correct. A reader who takes "25/25 after the repair" to mean "every repaired clause is
  falsified by the manifest" is over-reading; the report supplies the missing attribution
  (§F1 table) so the claim can be restated correctly.
- No control covers: the heading-prefix looseness (F3), the manifest digest (F4), the c2 rules
  in §7's survivor list, `entry-regular` in isolation, `min_tip_lines`.
- I did not re-derive C2's pointer gate (`--rev master`) — that is `RevAfterC2`'s seat. I did
  not judge, admit, integrate, edit or ship anything; no installs, so no tool record.

## Reproduction

Scratch, all under `.ufo/waves/round-36/scratch/RevAfterC1/`:

| path | what |
|---|---|
| `run-r36-2d90524.log`, `run-r36-a5f76c9.log` | full gate stdout for both r36 runs |
| `run-r35-2d90524.log`, `run-r35-a5f76c9.log` | full gate stdout for both r35 runs |

`/tmp` constructs (regenerable, referenced by the tables above): `res-disc`, `res-disc-r35`,
`res-disc2`, `res-disc3-r35`, `mut-r36-revA/B`, `mut-r35-revA/B`, `live-acc*`, `hdr/`,
`hdr-one/`, `c2-acc*`, `c1-follow.py`, `c1-mut-*.py`, `c2-mut-*.py`,
`c1-r35-plus-section.py`.

No lane artifact was written outside this report and that scratch directory.
