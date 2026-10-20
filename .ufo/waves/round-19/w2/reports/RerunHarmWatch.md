# MadoR19.RerunHarmWatch — holds

Attack: run the assigned harness at the integrated tip, then try to make its PASS
lie — receipts vs REV bytes, every command class re-run independently, what PASS
cannot see, and the invocation in the ticket itself. No false PASS was produced at
this REV; the one BASELINE line is the declared frozen-r18 observation.

Lane HEAD is `01b80946d92b26370d3012a7da655d00dd135154`. The tracked tree was
clean when this attack began (15:03 local / 18:03Z `git status --porcelain` showed only
untracked `w1/reports/RevDraftInstallers.md`, `w2/`, `evidence/harm/`,
`fetch/…`); concurrent w2 siblings began editing tracked files at 15:07:07 local,
after every receipt below was written (see Limits). The harness itself is tracked at that rev
(`git ls-tree HEAD -- .ufo/waves/round-19/harm-watch.sh` → blob
`3ad8da275693c6e814f260ac0740b92b7940b84a`, mode 100755).

## Run and TALLY

    OUTDIR=/tmp/hw-r19-w2 bash .ufo/waves/round-19/harm-watch.sh 01b80946d92b26370d3012a7da655d00dd135154
    HARM_WATCH: PASS            (exit 0, wall 167.59 s, 22 commands)

Verbatim from `/tmp/hw-r19-w2/harm-watch-summary.txt`:

```
TALLY	total	runs=22	ok=21	fail=0	skip=0	baseline=1	blocking=0
TALLY	action-plan	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	census	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	fresh-pins	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	gate	runs=2	ok=2	fail=0	skip=0	baseline=0
TALLY	measure-r16	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	measure-r17	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	navigation	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	tripwire-frozen	runs=2	ok=1	fail=0	skip=0	baseline=1
TALLY	tripwire-selftest	runs=11	ok=11	fail=0	skip=0	baseline=0
TALLY	tw-recall	runs=1	ok=1	fail=0	skip=0	baseline=0
HARM_WATCH: PASS
rev=01b80946d92b26370d3012a7da655d00dd135154 outdir=/tmp/hw-r19-w2 commands=22 failures=0 pins=/tmp/hw-r19-w2/harm-watch-pins.txt
```

No FAIL and no SKIP. The single BASELINE is the round-18 frozen replay:
`BASELINE exit=1 group=tripwire-frozen label=MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`
(`/tmp/hw-r19-w2/harm-tripwire-frozen-round-18.txt:2`). That is the expected
baseline, not harm: the body has `missing_findings: []` and `extra_findings` equal
to exactly the three recorded known misses — `inputs/r13-root.jsonl:4`,
`inputs/r14-source-safety.jsonl:2`, `:3`, all `pacman:-Q` — i.e. the merged tool
now detects the three lines the round-18 pin accepted as misses. `expected_sha256`
`4f3534ae…` is the source pin named in `.ufo/waves/round-19/frozen/README.md`.

Receipt integrity: 22 command files (24 `harm-*.txt` minus `harm-watch-pins.txt`
and `harm-watch-summary.txt`); every one starts with a `RECEIPT` line naming
`measured_commit=01b80946…` (census: `fleet:fc05a552…`) and the only non-zero
`exit=` is the baseline above. `harm-watch-pins.txt` records `state=ok` for all 11
pinned paths. I recomputed the digests independently: `tools/mado-verify.sh`
`1036d100…`, `tools/mado-action-plan.py` `226220ae…`, `tools/mado-tripwire.py`
`367be947…`, round-16 `measure.py` `ea3db43f…`, round-17 `measure.py`
`de4c422b…`, `tw-recall.py` `22090298…`, `fresh-pins.py` `a094be01…`, SCORECARD
`ba581ff4…` with block `8b59b503…`, fleet census `3fb72615…` — each equal to
`git show HEAD:<path>` / fleet HEAD.

Counter values in the receipts (read, not inferred): gate `MADO_SELFTEST: 443/443
assertions passed` and `MADO_REGRESSION: PASS (target=05aea198…)`; action-plan
`52/52`; 11/11 tripwire suites (including `r19-frozen-f1f2`); round-19 frozen
`frozen_match`; measure-r16 U1–U7 `score 10.0`; measure-r17 c1 `20/28`,
c2 `6/6`; tw-recall `incident_lines 6, detected 6, score 10.0`; fresh-pins
`denominator 13, current 13`; navigation `indexed=34/34 missing=0 dangling=0
duplicates=0 coverage=10.0000/10`; census `mado ok`.

Independent re-runs (outside the harness): `tw-recall.py` and `fresh-pins.py`
produced JSON identical to the receipts; `--frozen` on both frozen dirs produced
`frozen_verdict_mismatch` rc 1 / `frozen_match` rc 0; all five round-19 suites
exited 0 in 3.76 s; action-plan, the extracted SCORECARD block (`REV=` exported)
and the census re-ran green. A second, concurrent run of the same harness at the
same REV already existed at the lane default OUTDIR (PINS utc `18:02:28Z`, mine
`18:03:33Z`): its TALLY is line-for-line identical, and 21 of 22 command bodies
are byte-identical; the only body diff is `harm-gate-regression.txt`, whose
random `/tmp/mado-verify-regression.XXXX` paths, `REGRESSION_DATE`, and
`removed=3` vs `removed=4` (a leftover from the other run) differ while both end
`MADO_REGRESSION: PASS` with the same target digest `05aea198…`.

## Falsification probes

**P1 — "PASS substantiates C2/C3".** False as a claim about scores. The counters
exit 0 at any measured value (`tw-recall.py:87`, `fresh-pins.py:84`) and the
harness records OK purely on the process rc (`harm-watch.sh:121-131`,
`:204-210`). Demonstrated at the baseline rev: `tw-recall.py 9c54c56` prints
`detected 3, score 5.0`, `fresh-pins.py 9c54c56` prints `current 2,
denominator 13`, both rc 0. At the tip the values do hold (6/6, 13/13). So PASS
is a consistency receipt, not a claim checker; a counter regression would leave
PASS green and only the receipt body would show it.

**P2 — "the frozen-r18 replay cannot regress to a match without failing".** False
by design: `harm-watch.sh:312` accepts both `0:frozen_match` and
`1:frozen_verdict_mismatch` as BASELINE, and the script says so at `:25` and
`:313`. I reproduced the exact regression this tolerance would swallow: the
`9c54c56` tool (`git show 9c54c56:tools/mado-tripwire.py` → `/tmp/r19-w2-attack/`,
run `-I --frozen .ufo/waves/round-18/frozen`) returns
`MADO_TRIPWIRE_FROZEN: frozen_match`, rc 0. The label is retained in the receipt,
so the regression is visible, not hidden.

**P3 — "every measured byte is the REV byte".** True for the tools (all pinned
via `pin_assert`, `:155-178`), not for the inputs. The suite trees
(`:254`, `:276`), both frozen trees (`:302`, `:329-334`), the SCORECARD counting
block (`:368-392`, worktree/REV digests recorded but a mismatch only NOTEs at
`:387`) and the census corpus (`validate --root FLEET mado`, `:417-428`) are read
from the worktree. At run time (15:03–15:07 local / 18:03–18:07Z, before the sibling edits) the
inputs were byte-identical to HEAD: the five fixture roots had no modified or
untracked files, `SCORECARD.md` `ba581ff4…` == HEAD, block `8b59b503…`,
`corpus/SOURCES.md` `3a85abc5…` == HEAD. No harm in this run. [INFERENCE] A later in-flight fixture or SCORECARD edit would be measured
under `measured_commit=<REV>` because those bytes are never pinned.

**P4 — the ticket's invocation.** The ticket's
`harm-watch.sh <rev> /tmp/hw-r19-w2` does not select OUTDIR: the script takes REV
from `$1` and OUTDIR only from the environment (`:41-43`, `:54-55`; no top-level
`$2`), so a literal two-arg run writes to the lane default
`.ufo/waves/round-19/evidence/harm` (`:55`). I used `OUTDIR=/tmp/hw-r19-w2` as
the usage documents. This is a ticket/script mismatch, not a harness failure.

**P5 — census warnings.** W04 duplicate-URL lines (S030/S042/S045/S097) are
warnings that cannot fail a clean lane (`scripts/sources-census.sh:33`) and exit 0.
S097's is the same URL text retained on the superseded, rejected S094 row
(`corpus/SOURCES.md:106` and `:109`); explained, not a harm.

## Limits

- No live gate, `--no-live`, host probe or substrate command was run; only the
  harness's pinned `--selftest`, `--regression`, `--frozen` and scan-class
  commands, as the host pause allows.
- Gate selftest/regression were not re-run a third time; the evidence is two
  independent pinned executions (mine and the concurrent default-OUTDIR run),
  both PASS with the same target digest. Which seat produced the concurrent run
  is [UNK]; I read its files as data only.
- The harness was run once by me (167.59 s); all 22 receipts are retained under
  `/tmp/hw-r19-w2/`. Attacker scratch is `/tmp/r19-w2-attack/`.
- Concurrency: every receipt in this attack was written 18:03:33–18:06:20Z
  (15:03:33–15:06:20 local) while the tracked tree was clean. From 15:07:07
  local, other w2 seats modified tracked lane files — `SCORECARD.md` 15:07:07,
  `corpus/knowledge/{walker-route-r18,theme-route-r18}.md` 15:07:33,
  `corpus/QUALITY.md` 15:07:46, `.ufo/waves/round-19/landed-check.sh` 15:09:19,
  `corpus/knowledge/{arc-synthesis,remaining-planes-census,walker-live-surface,
  walker-deep-r9,walker-deep}.md` 15:10:01, `tools/mado-verify.sh` 15:10:48,
  `.ufo/waves/round-19/{fetch/.gitignore,supersessions.json}` 15:07:13. None of
  these are mine; a harm-watch re-run now would pin-skip the gate
  (`tools/mado-verify.sh` no longer equals REV) and read the edited SCORECARD
  and corpus rather than REV bytes.
- Nothing was written to the lane except this report.

## Installs

none
