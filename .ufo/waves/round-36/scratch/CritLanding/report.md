# CritLanding — residual attack pass on landed round 36

Scope: the two landed claims (C1 discrimination, C2 pointer gate), causal separability,
axis harm, the `sourced-art` retirement, and the `## Mistakes` rows. Read-only on every
production file. Lane tip at audit time: `2d90524` (`master`), base `4243d03`.

**Headline.** C1 reproduces exactly. C2's after-state does **not** reproduce from the
landed bytes: at `master` the committed gate prints `TARGET_MISSED`; the receipt's
`TARGET_MET` line is produced only by a 5-line **uncommitted** work-tree edit that is
still dirty in the lane.

## Item 1 — both claims' before→after, declared command, receipts reproduce

### 1a C1 after — CONFIRMED

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ python3 -I quality/check-counter-discrimination.py --profile r36 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --receipts .ufo/waves/round-36/controls/receipts
… 25 × "control=… ok=1" …
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
rc=0
```

Re-run in a clean `git clone` of `master` (`/tmp/mado-critic`): identical 25/25, rc 0.
Matches `.ufo/waves/round-36/receipts/after-discrimination.txt` line for line.

### 1b C1 before — CONFIRMED

```
$ python3 -I quality/check-counter-discrimination.py --profile r35 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --receipts .ufo/waves/round-36/controls/receipts-r35
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=14/25 label='round-35 frozen counters (unmodified)' verdict=TARGET_MISSED
rc=1
```

The four `c1` and seven `c2` wrong lines match the SCORECARD's attribution exactly
(`c1-shape-only`, `c1-fabricated-payload`, `c1-no-registry-heading`, `c1-row-moved-out`,
plus the seven `c2` rejects other than `c2-retired-also-live`).

### 1c C2 before — CONFIRMED (with the receipt's own disclosed caveat)

```
$ git clone -q --no-hardlinks LANE /tmp/mado-critic && cd /tmp/mado-critic
$ python3 -I quality/check-evidence-pointers.py --rev 4243d03 --repo .
PRED-PTR-r36-v1 rev=4243d03 pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED
rc=1
```

Exactly the receipt's re-run line. `inherited_dirty=10` in the receipt header is a live-tree
reading the receipt already declares unreproducible; the disclosure is honest.

### 1d C2 after — **FALSIFIED (HIGH)**

The declared command against the landed bytes:

```
$ cd /tmp/mado-critic            # clean clone, master = 2d905245
$ python3 -I quality/check-evidence-pointers.py --rev master --repo .
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=34 dangling_r36=3 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MISSED
dangling_r36: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r36: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
dangling_r36: quality/receipts/axis-a3094c99ab85bec35534de2447552c47dd2b647f.txt
rc=1
```

Same result at the receipt's own revision `cf175c7` (`dangling_r36=3`, `TARGET_MISSED`, rc 1).

The receipt's `TARGET_MET` line is produced only by the lane's **uncommitted** work tree:

```
$ git -C LANE status --porcelain
 M quality/check-evidence-pointers.py
$ git -C LANE diff quality/check-evidence-pointers.py
+                        entry, `SCORECARD.md` sections and `corpus/lessons/round-36.md`,
+                        except pointers written as the `old` side of a correction
+                        pair — a superseded pointer is named, not cited;
-    dangling36 = [p for p in ptr36 if not resolves(p, files)]
+    superseded_old = {m.group(1).strip() for m in (PAIR.match(ln) for ln in log36.splitlines()) if m}
+    dangling36 = [p for p in ptr36 if not resolves(p, files) and p not in superseded_old]
```

With those bytes copied in, the same command prints the receipt's exact line:

```
PRED-PTR-r36-v1 rev=master … dangling_r36=0 … verdict=TARGET_MET
rc=0
```

Provenance: `git log --oneline -- quality/check-evidence-pointers.py` = one commit
(`dbf8b57`, the freeze); `git show cf175c7:quality/check-evidence-pointers.py | grep -c
superseded_old` = `0`. The exemption was never committed at any round-36 revision.
`.ufo/waves/round-36/receipts/after-pointers.txt` records no sha256 of the gate it ran, so
nothing in the receipt binds it to those bytes (criterion 58's analogue).

Consequence: SCORECARD's C2 row ("→ `TARGET_MET` exit 0 | **improved**"), the LOG C2
bullet ("After: all five at target"), the lesson's C2 bullet and the round report's
"Before `TARGET_MISSED`, after `TARGET_MET`" are all false at the landed tip.

Compounding blind spot: `inherited_dirty` is a hard-coded ten-path tuple
(`INHERITED_PATHS`) of round-35 paths, so the gate reported `inherited_dirty=0` **while
its own file was modified in the tree it was measuring**.

Smallest safe correction: commit the exemption (optionally additionally requiring
`resolves(new)` so a pair cannot name a dead replacement), re-run the declared command at
the new tip, and re-commit `after-pointers.txt` with the gate's sha256 in its header.

## Item 2 — causal separability

### C1 → C2: independent — CONFIRMED

```
$ rm -f corpus/lessons/round-36.md LOG.md SCORECARD.md   # in a clone; C2's three records
$ python3 -I quality/check-counter-discrimination.py --profile r36 --manifest … --receipts …
MADO_DISCRIMINATION: … correct=25/25 … verdict=TARGET_MET
rc=0
```

C1 reads only the manifest, the two counters, the generator and the frozen specs. It is
also green at `a3094c9`, the commit where the counters landed and before any round-36
record section existed.

### C2 → C1: dependent — **FINDING (MEDIUM)**

SCORECARD (line 2250) says: "Neither reads the other's output". C2's gate resolves pointers
that the round-36 records cite, and three of those are C1's artifacts. Removing them from
the revision flips the gate:

```
$ git -C /tmp/mado-critic2 rm -rq quality/counters quality/check-counter-discrimination.py
$ git -C /tmp/mado-critic2 commit -qm "remove c1 tools"
$ python3 -I quality/check-evidence-pointers.py --rev HEAD --repo .
PRED-PTR-r36-v1 … dangling_r36=3 … verdict=TARGET_MISSED
dangling_r36: quality/counters/c1-idle-lock.py
dangling_r36: quality/counters/c2-ledger.py
dangling_r36: quality/check-counter-discrimination.py
rc=1
```

So C2 is not verifiable "without the other having landed": its record cites
`quality/counters/c1-idle-lock.py`, `quality/counters/c2-ledger.py` and
`quality/check-counter-discrimination.py`. The registration's "causally separable" and the
SCORECARD's "each was measured with the other's artifacts absent" overstate the result.

Smallest safe correction: state the dependency in one sentence (C2's record cites C1's
three artifacts, so C2 is measurable only after C1 lands; C1 is independent of C2), and
drop "Neither reads the other's output".

## Item 3 — no axis harmed

### 3a No lowered published row — CONFIRMED

```
$ git -C LANE diff 4243d03 master --stat
184 files changed, 9340 insertions(+), 0 deletions(-)
```

The SCORECARD hunk is `+98 −0`; no existing row is rewritten, so no published row moves
down. `PROVINCE.md +33`, `corpus/QUALITY.md +7`, `corpus/SOURCES.md +1` are also additive.

### 3b The three fractions do not fall — CONFIRMED

```
$ python3 -I quality/check-axis-scores.py --repo . --rev 4243d03
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=43/43 derived=43/43 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
$ python3 -I quality/check-axis-scores.py --repo . --rev master
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=48/48 derived=48/48 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
```

43/43 → 48/48 (up), 50/50 and 12/12 unchanged. Independent harm watch reproduces:
`bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed` (rc 0);
`tools/mado-verify.sh` blob identical at both revs
(`050efc72…` = `050efc72…`); census exits 0 with the same seven `W04` warnings; row count
`201` at master vs `200` at `4243d03`.

### 3c False provenance anchor — **FINDING (LOW)**

SCORECARD: "Axis table re-derived at `a3094c99…` (this round's data commit): navigation
50/50; calibration resolved-active 48/48; operability selftest 12/12." At `a3094c9` the
calibration derivation is 47/47, as the lane's own committed red receipt states:

```
$ python3 -I quality/check-axis-scores.py --repo . --rev a3094c99ab85bec35534de2447552c47dd2b647f
MADO_AXIS_ROW: axis=calibration published=43/43 derived=47/47 verdict=STALE
MADO_AXIS: checked=3 mismatched=1 …
rc=1
```

`48/48` exists only from `520c631` (criterion 61 landed there; verified `MADO_AXIS:
mismatched=0 rev=520c631…`). `check-axis-scores.py` never re-derives at the revision the
publication names, so the wrong anchor passes the gate. Correction: name `520c631` (or
state 47/47 at `a3094c9` and 48/48 at `520c631`).

## Item 4 — `sourced-art` retirement

### 4a Stated with a reason — partial; canonical field still says "none retired" — **FINDING (MEDIUM)**

`SCORECARD.md:2273` does state a reason ("its denominator was the fixed seven-item
uncovered-ground list U1–U7 … a saturated 1.0 would read as coverage progress it is not").
But the contract field itself is untouched:

```
$ awk '/^## Retired/{f=1} f' SCORECARD.md | head -3
## Retired

- none retired; record with justification when an axis is retired.
```

`git diff 4243d03 master -- SCORECARD.md` contains no hunk in `## Retired` (additions only,
`+98 −0`). This is the same defect round 35 routed — publication and `## Retired`
disagreeing — merely inverted: the round-36 prose retires an axis that the canonical list
still reports live. `AXES.md`'s scorecard contract puts the justification in the `retired`
field, not in a round stanza.

Smallest safe correction: replace the `- none retired` bullet with a dated
`sourced-art — retired round 36: <reason>` row (append, do not rewrite history).

### 4b No measured surface silently dropped — CONFIRMED

The retirement says the ground "stays measured by the per-round frontier rows in
`corpus/README.md`". Verified: `corpus/README.md` rows 34–41 still carry the U1–U7 notes and
the round-12 rubric still counts them:

```
$ grep -cE '^covers: U[1-7]' corpus/knowledge/*.md | awk -F: '{s+=$2} END{print s}'
7
$ for f in corpus/knowledge/*.md; do head -n 15 "$f" | grep -qE '^source:.*\bS[0-9]{3,}\b' && echo "$f"; done | wc -l
24
```

### 4c Retirement reason's count is wrong — **FINDING (LOW)**

The reason says "five of which have since been closed by admitted entries". The rubric's own
command counts **7** covered U-items (above), one `covers:` line per U1–U7. The number has no
command attached, contrary to CORPUS.md's "a count carries its command". The conclusion
(saturated, denominator stale) survives and is in fact stronger.

## Item 5 — `## Mistakes`

All six rows carry a class (in the section index: M36-1 instrument, M36-2 number-drift,
M36-3 instrument, M36-4 vacuous, M36-5 stale-premise, M36-6 reference-drift), an explicit
`**Evidence pointer.**`, a `**Captured-by.**` (three of them `none` with the reason) and a
`**Fix.**` with a "Demonstrated able to fail" sentence. Three of those demonstrations do not
hold.

### 5a M36-2 — CONFIRMED (reproduced)

Trimming the ledger to two tip-labelled lines in a clone and running the frozen counter:

```
$ python3 -I quality/counters/c2-ledger.py --repo . --frozen .ufo/waves/round-36/c2/frozen.json
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=0 verdict=TARGET_MISSED
  tip: 2 tip lines, minimum 3
```

Post-fix doc reads `tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows
re-derived`. Claim exact.

### 5b M36-4 — direction CONFIRMED, second receipt pointer dangling — **FINDING (MEDIUM)**

The GIT_DIR claim reproduces: without it the fixture fails for the environment, with it for
the mutation.

```
$ env -u GIT_DIR python3 -I quality/counters/c2-ledger.py --repo /tmp/mado-r36-mutants-r36/c2-tip-stale … 
  tip: rule produced no commit                     → TARGET_MISSED (fixture, not mutation)
$ GIT_DIR=LANE/.git python3 -I quality/counters/c2-ledger.py --repo …/c2-tip-stale …
  tip: stale token fa7ba113… on: round-34 lane tip …   → TARGET_MISSED (mutation)
```

But the row's evidence names "the wave's `MutC2HardcodedTip` and `MutC2NoTable` receipts".
`MutC2HardcodedTip.md` exists; `MutC2NoTable.md` does not — only its prompt
(`w1/prompts/MutC2NoTable.md`) and spec entry do:

```
$ find .ufo/waves/round-36 -name '*MutC2*'
…/w1/prompts/MutC2HardcodedTip.md
…/w1/prompts/MutC2NoTable.md
…/w1/reports/MutC2HardcodedTip.md      # no reports/MutC2NoTable.md
```

### 5c M36-3 — second half unlanded — **FINDING (MEDIUM)**

"the wave's per-clause drop mutants (`MutC1NoDigest`, `MutC1NoFence`, `MutC1CheckAnchor`) are
the second". None of the three has a report; `MutC1CheckAnchor` has only a scratch directory:

```
$ ls .ufo/waves/round-36/w1/reports/
… MutC1AcceptAll.md MutC1RejectAll.md MutC2HardcodedTip.md …   # no MutC1{NoDigest,NoFence,CheckAnchor}.md
```

The clause-attribution receipt itself exists and matches its text (`c1-donothing
open_cites=8`, every other crib `open_cites=1`), but it is not re-runnable: its command line
contains the literal placeholder `(insert ## Registry heading)`.

### 5d M36-1 — the "shown able to fail" observation is false for the gate — **FINDING (LOW-MEDIUM)**

The fix text: "the post-fix run exits 0 and prints one `mutant=<id>` line per fixture."

```
$ python3 -I quality/check-counter-discrimination.py --profile r36 … | grep -c '^mutant='
0
```

The gate captures the generator's stdout (it only *parses* `mutant=` at
`check-counter-discrimination.py:126`) and prints it only on failure. The generator itself
prints 8 `mutant=` lines when invoked directly. A reader running the receipt's command cannot
observe the claimed output. The row also says "the failure text is quoted in the round
report's work-performed section": `grep -in 'FileNotFound'` over
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/mado.md` returns nothing, and no
committed receipt under `.ufo/waves/round-36/` carries `FileNotFoundError`.

### 5e M36-5, M36-6 — CONFIRMED

```
$ grep -c 'domain-versus-meta' /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/mado.md
0
$ python3 quality/check-index.py --repo .
SETUP_ERROR: --rev or --root is required
rc=2
```

M36-6's seat report is committed (`w1/reports/RevIndexGate.md`). M36-5's ratio line is
present in the round-36 record.

## Round-contract findings outside the five items

- **FINDING (MEDIUM): the round report is uncommitted and carries placeholders.**
  `git -C /home/vgpnk/Projects/shokunin status --porcelain .ufo/reports/round-36/mado.md` →
  `?? .ufo/reports/round-36/mado.md`; `grep -nE '<[A-Z_]{3,}>'` finds four:
  `Lane tip when this report was written: <LANE_TIP>`, `<FINAL_SUMMARY>`, `<FINAL_LANE>`,
  `Dead seats: <DEAD>`. MISSION.md's round end requires the report committed and pushed.
- **FINDING (LOW): the lane is dirty at the "landed" tip** — `M
  quality/check-evidence-pointers.py` plus four untracked `w1/reports/*.md` — and neither C2
  observable can see it (`inherited_dirty` is the hard-coded ten-path tuple;
  `dangling_r36` is computed from the revision).

## Assets and tooling

No installs, no package transactions (pacman untouched), no mutating git command in the
lane. All experiments ran on `git clone --no-hardlinks` copies under `/tmp`
(`/tmp/mado-critic`, `/tmp/mado-critic2`, `/tmp/mado-critic3`) and `/tmp/x36`.
