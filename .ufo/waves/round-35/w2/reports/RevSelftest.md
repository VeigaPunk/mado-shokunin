# RevSelftest — operability-suite attack; "no axis is harmed" falsified at HEAD

Seat scope: run the operability suite at the round-35 tree, confirm the assertion count is
unchanged-or-higher versus the round-34 tip, confirm zero assertions fail, and falsify the
instrument itself. Read-only: no lane corpus, counter, control, `SOURCES.md`, jj or Git
index was written. All writes are under
`.ufo/waves/round-35/scratch/RevSelftest/` plus this report.

## Verdict

| Question | Answer |
|---|---|
| Assigned suite `tools/mado-verify.sh --selftest`: count unchanged-or-higher? | **Yes** — 460/460, byte-identical to the round-34 tip |
| Zero assertions now fail? | **Yes** — rc=0, no `FAILED` line |
| Is the suite live (can it fail)? | **Yes** — two mutants prove it |
| **Is "no axis is harmed" true?** | **NO.** At the committed round-35 HEAD `02088b4d`, the lane's own axis gate is red: `mismatched=2`, exit 1 — `navigation` STALE and `calibration` STALE, the latter backed by its instrument returning `TARGET_MISSED`, exit 1. |

Operability itself is unharmed (460/460; 12/12; 50/50). The harm is on **navigation**
(stale publication) and **calibration** (two unresolved qualifying criteria). Details below.

### Measurement timeline (why two HEADs appear)

The lane HEAD moved *during* this seat's run:

- measurements at HEAD `19e4ab31` (round-35 freeze commit) → axis gate `mismatched=0`, rc=0;
- the wave committed the data at `02088b4d` ("the idle-lock control surface lands — three
  entries, eight rows S203-S210, errata, and the wave-1 evidence", 2026-10-25 03:34:26);
- re-measurement at HEAD `02088b4d` → axis gate `mismatched=2`, rc=1.

Both states are reported rather than papered over; the current, committed state is red.

## A1/A2 — the assigned command

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && bash tools/mado-verify.sh --selftest; echo rc=$?
```

Summary line, verbatim:

```
MADO_SELFTEST: 460/460 assertions passed
rc=0
```

Re-run again after the new HEAD landed: `MADO_SELFTEST: 460/460 assertions passed`, `rc=0`.
No `FAILED` line, no `- <assertion>` lines, no `fixtures kept:` line (they appear only on
failure).

### Baseline: unchanged versus the round-34 tip — by byte identity

| Evidence | Command | Result |
|---|---|---|
| last commit touching the suite | `git log -1 --format='%h %ci %s' -- tools/mado-verify.sh` | `7b4839d 2026-10-20 round-19: … (460/460)` |
| round-34 tip | `git log -1 --format='%h %ci %s' 6d754bd` | `6d754bd 2026-10-24 23:04:26 round-34 verifier spot-check` |
| tip blob vs worktree | `git show 6d754bd:tools/mado-verify.sh \| sha256sum` ; `sha256sum tools/mado-verify.sh` | both `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` |
| post-commit HEAD blob | `git show HEAD:tools/mado-verify.sh \| sha256sum` | same `050efc72…` |
| worktree vs HEAD | `git diff --stat HEAD -- tools/mado-verify.sh quality/` | empty |

The suite bytes are identical at the round-34 tip, at both round-35 HEADs, and in the
worktree, and `--selftest` is hermetic (fixtures in `/tmp/w5-mado-m52-*`, no substrate
reads). So the round-34-tip count is **460/460** and the round-35 count is **460/460**:
unchanged, not higher, zero failures.

### Correction to the dispatch's "12/12"

That figure is not this suite. `quality/check-axis-scores.py:14` maps the operability axis to
`quality/check-index.py --selftest → A/B assertions passed`, and
`.ufo/waves/round-34/controls/axis-selftest.txt` records
`axis=operability published=12/12 derived=12/12`. Measured now:
`MADO_INDEX_SELFTEST: 12/12 assertions passed`, rc=0. `mado-verify.sh` publishes 460/460.

## A3/A4 — falsifying the instrument

`selftest()` counts at runtime (`st_ok`/`st_bad` increment `n_pass`/`n_fail`, lines 421-424);
the summary prints `$n_pass/$n_pass` or `FAILED — $n_pass passed, $n_fail failed` and returns
2. Static assertion call sites:
`grep -c "st_eq \|st_has \|st_not_has \|st_rows \|st_row_has \|st_row_detail \|st_row_exact \|st_counts_agree " tools/mado-verify.sh`
→ **460**, exactly the runtime total.

| Mutant (scratch copy) | Change | Observed | rc |
|---|---|---|---|
| `mut-false-assert.sh` | injected `st_eq "PROBE: …" 0 1` after `# <<< MADO-R8-BLOCK <<<` | `MADO_SELFTEST: FAILED — 459 passed, 2 failed`; failures = PROBE and `R10: derived target equals the recorded gate revision (got 'f3b49ade…' want '367ff5ec…')` | 2 |
| `mut-drop-assert.sh` | deleted `S10: the unchanged row stays silent` (inside the R8 block) | `MADO_SELFTEST: 459/459 assertions passed` | 0 |

Both are diagnostic, not defects:

- The dropped assertion lowers the total to 459 — the denominator tracks the source, so the
  pristine 460 cannot be a literal masking a vanished assertion.
- The false-assert mutant's **R10 collateral failure is probe-induced**: `mado_r7_target_build()`
  (lines 2114-2124) excises the `MADO-R7/R8` marker families and `PIN_MADO='367ff5ec…'` pins
  the residual target's sha256. My line sat outside every excised family, so it moved the
  derived target — exactly the pin's documented purpose. The dropped line sat inside the R8
  family, so excision left the target byte-identical and R10 stayed green.

## A5 — data-level operability (the three new entries)

`mado-verify.sh --selftest` measures the gate, not the corpus, so the corpus was measured and
then perturbed directly:

| Root / rev | Command | Result | rc |
|---|---|---|---|
| HEAD `02088b4d` (3 entries committed) | `python3 -I quality/check-index.py --rev HEAD --repo .` | `indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 |
| worktree (same data) | `python3 -I quality/check-index.py --root .` | `indexed=50/50 missing=0 dangling=0 duplicates=0` | 0 |
| pre-commit HEAD `19e4ab31` | `python3 -I quality/check-index.py --rev HEAD --repo .` | `indexed=47/47 …` | 0 |
| scratch copy, unperturbed | `--root …/root-ok` | `indexed=50/50` | 0 |
| scratch copy, r12 index row deleted | `--root …/root-missing` | `indexed=49/50 missing=1`, `missing: knowledge/idle-lock-never-asked-r12.md` | 1 |
| scratch copy, r14 row duplicated | `--root …/root-dup` | `indexed=49/50 duplicates=1`, `duplicate: knowledge/idle-lock-chain-armed-r14.md` | 1 |

Each new entry is indexed exactly once, and the gate names the entry when its row is removed
or duplicated. Sibling instrument selftest: `quality/check-index-rows.py --selftest` →
`MADO_INDEX_ROWS_SELFTEST: 10/10`, rc=0.

## A6 — the axis gate: green before the commit, red at it

```
python3 -I quality/check-axis-scores.py --rev 19e4ab31 --repo .
  MADO_AXIS_ROW: axis=navigation  published=47/47 derived=47/47 verdict=MATCH
  MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/41 verdict=MATCH
  MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
  MADO_AXIS: checked=3 mismatched=0 rev=19e4ab31…        rc=0

python3 -I quality/check-axis-scores.py --rev HEAD --repo .
  MADO_AXIS_ROW: axis=navigation  published=47/47 derived=50/50 verdict=STALE
  MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/43 verdict=STALE
  MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
  MADO_AXIS: checked=3 mismatched=2 rev=02088b4d…        rc=1
```

The publication being compared is `SCORECARD.md:2110`: *"Axis table re-derived at the
round-34 data tree (criterion 22): navigation 47/47 = 1.0; calibration resolved-active
41/41 = 1.0; operability selftest 12/12 = 1.0."* It was correct for `19e4ab31`; commit
`02088b4d` moved both denominators without re-deriving it.

### Navigation harm (publication only)

`02088b4d` added the three notes (47 → 50). The instrument is healthy — `indexed=50/50` — but
the published navigation cell still says `47/47`. Under the gate's own rule
(published == derived, `quality/check-axis-scores.py:88-113`) that is STALE. **Repair:** re-derive
the publication at the round-35 tree (navigation 50/50).

### Calibration harm (instrument, not just publication)

This one is real, not cosmetic. The calibration derivation runs
`.ufo/waves/round-31/c2/count.py` and greps `resolved_active=(\d+)` / `active=(\d+)`:

| Revision | Command | Result | rc |
|---|---|---|---|
| `19e4ab31` | `python3 -I .ufo/waves/round-31/c2/count.py 19e4ab31` | `active=41 resolved_active=41 fraction=1.0000`, `verdict=TARGET_MET` | 0 |
| `02088b4d` | `python3 -I .ufo/waves/round-31/c2/count.py HEAD` | `literal 44/56`, `active=43 resolved_active=41 fraction=0.9535`, `verdict=TARGET_MISSED` | 1 |

The two new unresolved criteria, verbatim:

```
UNRESOLVED criterion 55: id \bM35-2\b absent in section '#mistakes' of corpus/lessons/round-35.md
UNRESOLVED criterion 56: id \bM35-2\b absent in section '#mistakes' of corpus/lessons/round-35.md
```

Both were added by `02088b4d` (`git show --stat 02088b4d` → `corpus/QUALITY.md | 2 +`) and both
cite `lessons/round-35.md#mistakes M35-2`.

**Root cause — a heading-style mismatch with the frozen resolver.** `M35-2` is *not* missing;
it is `### M35-2 — instrument vacuity (class: instrument)` at
`corpus/lessons/round-35.md:203`, inside `## Mistakes` (heading at :165). The resolver does not
see it because of how it bounds a section (`count.py:107-118`):

```python
def sections(body, anchor):
    for m in re.finditer(r"^#{2,4}\s+(.+?)\s*$", body, re.M):
        s = slug(m.group(1))
        if s == anchor or s.startswith(anchor + "-"):
            rest = body[m.end():]
            nxt = re.search(r"^#{1,4}\s", rest, re.M)      # scope ends at ANY heading
            out.append(rest[: nxt.start()] if nxt else rest)
```

`## Mistakes` is immediately followed by `### M35-1` (line 167), so the `#mistakes` scope is
the near-empty gap between them; every `M35-*` id lives in a `###` subheading line, i.e.
outside the scope. The working precedent, `corpus/lessons/round-30.md:9`, keeps its ids in a
**table under** `## Mistakes`, so `M30-1` lands inside the scope and criterion 53 resolves.
Round-35 changed the lesson's shape and the frozen rubric could not follow.

**Repairs (parent's choice; I did not edit lane files):**
1. Put the ids in the `## Mistakes` body — e.g. a round-30-style table (or an index line
   naming `M35-1`…`M35-4`) directly under the heading, keeping the `###` narratives below it.
   Re-citing `#m35-2---…` does *not* work: the scope starts at `m.end()`, so an id inside the
   matched heading is still out of scope.
2. Then re-derive the axis publication at the round-35 tree: navigation 50/50, calibration
   43/43 (after the repair) or 41/41 (if criteria 55-56 are withdrawn/superseded), operability
   12/12.

### The wave's own frozen C2 predicate cannot see this

```
python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen …/c2/frozen.json
  PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   rc=0
```

Also `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, rc=0 —
both after the offending commit. So both round-35 predicates are green while the lane's
calibration axis is red: the frozen C2 predicate does not include criterion-citation
resolution, so it cannot detect the harm it inherits. That gap is worth a routed defect; the
published-axis gate is currently the only reader that catches it.

## Live-session dependency

None blocked the run. The suite asserts its live-plane rows *as* `SKIP` with a reason
(e.g. scenario A `st_row_has … live.plane SKIP`), so a non-live host is a contract case, not a
failure. `--selftest` passed 460/460 twice without a live probe — expected behavior, not a
masked skip.

## State note — repairs in flight, uncommitted (observed after the measurement)

At the time of writing, HEAD is still `02088b4d` (red), but the worktree carries an
uncommitted lesson repair: `git diff --stat -- corpus/lessons/round-35.md` → `+32` lines, and
the `## Mistakes` heading is now followed by a section-level index:

```
Four mistakes, named here at section level so a citation check that reads `#mistakes`
sees them: **M35-1** id-space citation … · **M35-2** instrument vacuity … · **M35-3** … · **M35-4** …
```

That is repair direction 1. I replayed the resolver's exact predicate (`sections()` from
`count.py:107-118` plus `\bM35-N\b`) against the worktree text:

```
M35-1: True   M35-2: True   M35-3: True   M35-4: True   (scope_len=501)
```

The round-31 instrument cannot see uncommitted lessons — `file_text()` reads
`git show <rev>:<path>` — so this is the only available confirmation, and it is a faithful
replay of the predicate rather than a gate run. Expected after commit: criteria 55 and 56
resolve, `active=43 resolved_active=43 fraction=1.0000`, `TARGET_MET`. **Still owed at that
point:** re-derive `SCORECARD.md:2110` to the round-35 tree (navigation 50/50, calibration
43/43, operability 12/12), or the axis gate remains `mismatched≥1`. Neither edit was made by
this seat.

Also uncommitted and not mine: `corpus/knowledge/idle-lock-*.md` (all three) and
`corpus/README.md`. The committed-index measurement A5 (`indexed=50/50` at HEAD) is unaffected.

## Residual risks

1. The axis gate reads only committed revisions; uncommitted fixes will not move it. The
   publication repair must be committed together with the lesson/citation repair or the gate
   stays red for a fresh clone.
2. Operability's published fraction measures the instrument's own assertions (12/12), not the
   corpus — corpus evidence rests on `indexed=50/50` plus the perturbation probes above.
3. `PIN_MADO` is a maintenance tripwire: edits outside the `MADO-R7/R8` families move the
   derived target and fail R10 until a measured re-cut. It fired on my out-of-family probe by
   design.
4. The calibration harm is inherited by any consumer that trusts the published table; the
   table currently overstates calibration by 2 criteria.

## Artifacts (scratch)

- `.ufo/waves/round-35/scratch/RevSelftest/mut-false-assert.sh`, `mut-drop-assert.sh` — suite mutants
- `.ufo/waves/round-35/scratch/RevSelftest/{root-ok,root-missing,root-dup}/` — index-gate perturbation roots
- `/tmp` fixture from the failed mutant run (`/tmp/w5-mado-m52-selftest.t1qDe7`) removed;
  `ls -d /tmp/w5-mado-m52-selftest.* | wc -l` → 0.

## Installs

None. No pacman transaction attempted (host-wide pause honored); no uv/npx/binary install needed.
