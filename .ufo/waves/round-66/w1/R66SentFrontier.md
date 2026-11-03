# R66SentFrontier — round-66 frontier/security sentinel

Seat: `R66SentFrontier` (sentinel, leaf). Lane: `mado-shokunin`, claims freeze
`ed980316e330703030d0c17b2a7098e058295b99`, frozen base
`eafd500fa7be76dca59e729435e231a5032cc037`; integration observed at
`043b9af13c0af23e5ee7d48e8cda00e6d3207ad9` (2026-11-03T20:28:48-03:00), date 2026-11-03.
Scope: read-only attack on round-evidence security/hermeticity and frontier conformance. No
production edits, no commits, no installs, no credentials/session/env reads, no r56 material, no
host configuration/service/compositor change. Scratch `/fast/scratch/hyaku/mado-r66/R66SentFrontier/`
used only for fixtures and removed before yield; retained evidence is in
`.ufo/waves/round-66/w1/R66SentFrontier/evidence/`.

## Axes and bottom line

Axes: **calibration** (committed-object and register discrimination), **operability** (landing
instrument marker/rc map), **frontier conformance** (source row schema/rule 2/quote/used-by,
census, registries, evidence pointers). The frontier walked through four real containment defects;
each was fixed by the owning seat and re-tested here. L1 then integrated the final bytes at
`043b9af1`, and the frozen counts at that revision both pass: C1 candidate 4/4 + selftest
TARGET_MET; C2 candidate 4/4 + selftest + driver real landing
`MADO_LANDING_COUNTERS: GREEN … citecheck=4 resolved=4` rc0 TARGET_MET; census end rc0 with the
warning set unchanged. What remains is low-severity hardening and the declared truth/forgery
limits.

Final integrated bytes (same hashes as the final seat drafts):

| integrated path | sha256 at `043b9af1` |
|---|---|
| `quality/counters/c1-r66-register.py` | `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31` |
| `quality/landing-counters.sh` | `e4767ec74f1ff481a826573c7880f6107734ad31bd3b085e0eaba45415d82c4f` |
| `quality/counters/c2-r66-landing-instrument.py` | `e4d62b3c1e6f19f2cc1d6540d5f7feb33136cc6cb08e68ef31392d45b7dd6d65` |
| `.ufo/waves/round-66/check-controls.py` | `2e34eab0705b173a6c90d5635b4eb7bd8a71d57932821a0c01c855d17967db13` |
| `corpus/lessons/round-66.md` | `33426e552d9426798951ad9a59e0503b1b3840518532444c87a7d0e49a4114a8` |
| S435 integrated row | 11 cells / NF=13 in `corpus/SOURCES.md`; source-seat draft/gate hashes `cbe17a50…` / `626ade22…` are not the integrated bytes |

## Findings, ordered

| # | status | sev | finding |
|---|---|---|---|
| 1 | FIXED, re-tested | MED | In-repo `refs/replace` steered the C1 counter from TARGET_MISSED to TARGET_MET on unchanged bytes |
| 2 | FIXED, re-tested | MED | Landing dirty guard refreshed/wrote `.git/index`; a read-only instrument mutated the measured repo |
| 3 | FIXED, re-tested | MED | Harness followed a pre-planted scratch symlink and wrote outside its intended evidence tree |
| 4 | FIXED, re-tested | MED | C2 harness counted only cases a–d; candidate selftest and real landing were not verdict gates |
| 5 | RESIDUAL, low | LOW | Driver (`e4d62b3c…`) and harness (`2e34eab0…`) still do not set `GIT_NO_REPLACE_OBJECTS` |
| 6 | RESIDUAL, low | LOW | Seat source gate says the supporting quote is 19 words; it is 18; integrated lesson has one 15-word quote, no production defect |
| 7 | HISTORICAL WORDING, low | LOW | Integrated lesson calls `1671cebc…` “final” in the mutation sentence while naming `e4767ec7…` final later; mutation evidence is on `1671` |
| 8 | RESOLVED at `043b9af1` | — | Lesson + S435 + round-66 receipts are committed together; census end rc0 (0 E, 0 S435 findings) and citecheck resolves 4/4 |
| 9 | ACCEPTED LIMIT | MED | C1 still accepts a register whose rows cite only the file-plane receipt when `gate-live-r65.txt` remains committed (L1 ruled tree-level; not fixed) |
| 10 | DECLARED LIMIT | — | State-cell truth unmeasured; marker checks are structural, not anti-forgery; frozen `MADO_TOOL_LEDGER` literal is a premise erratum |
| 11 | DISCLOSED CUTOVER | LOW | `--citecheck-paths` outside `--repo` is refused rc2; frozen text only says the caller may provide paths |
| 12 | INFO | LOW | Raw child stdout/stderr is relayed/retained verbatim; no env/session reads found; seat `__pycache__` is non-production |

### 1. C1 replace-ref steering — FIXED in `8ca15c66…`

Scratch repo: commit A had the walker row's receipt cell set to `none`; commit B was the same
tree with the genuine row. `git -C repo replace A B` makes `git show A:PROVINCE.md` return B's
bytes. The old C1 draft `4e1b94ff…` read the replaced bytes and printed
`MADO_R66_REGISTER: … verdict=TARGET_MET rev=A` rc=0 while
`git --no-replace-objects cat-file -p A:PROVINCE.md` still showed `none`. That is a real
false-positive path: a local `.git/refs/replace` entry changes the object `--rev` resolves to
without changing committed bytes. The fixed draft sets
`GIT_NO_REPLACE_OBJECTS=1` after the inherited-env scrub; re-test on the same fixture gives
`verdict=TARGET_MISSED` rc=1, `detail=row-receipt-missing='walker'`; selftest 15/15; genuine
base `eafd500` still TARGET_MET rc=0. Receipt: `w1/R66ExecRegister/replace-refs.txt`.
Caller environment cannot mitigate this, because the counter strips every inherited `GIT_*`.

### 2. Landing index refresh — FIXED in `e4767ec7…`

A `git status` dirty guard without `GIT_OPTIONAL_LOCKS=0` can refresh the index. In a scratch
clone I ran `git update-index --refresh`, touched
`.ufo/waves/round-65/receipts/gate-live-r65.txt`, and ran the old landing draft `1671cebc…`:
landing rc=0 GREEN, but `.git/index` sha256 changed
`310eaeac…` → `196a4845…` (`INDEX_CHANGED`). The final draft exports
`GIT_OPTIONAL_LOCKS=0 GIT_NO_REPLACE_OBJECTS=1`; the same test now leaves the index
`9c73f1f3…` unchanged (`INDEX_UNCHANGED`), selftest 58/58 rc0, and a real lane run with
committed r65 receipts remains GREEN. This closes both the read-only-index and replacement-ref
paths for the landing instrument and its children.

### 3. Harness scratch symlink escape — FIXED in `2e34eab0…`

With the old harness `84ec73dd…` I planted
`<scratch>/r66harness/c1/extracted -> <scratch>/victim`; `check-controls.py --rev eafd500
--claim c1` wrote `c1-r65-register.py`, `gate-live-r65.txt` and `gate-fileplane-r65.txt`
through the symlink into the victim directory (`victim_count=3`). The frozen command's scratch
root is shared, so a sibling could redirect writes. The final harness creates a fresh private
`tempfile.mkdtemp` run directory, rejects scratch-root symlink components, and the planted
legacy symlink is ignored (`victim_count=0`).

### 4. C2 count omitted two required gates — FIXED in `2e34eab0…`

The frozen target is “correct=4/4 across a–d **plus** selftest green and real four-leg landing
GREEN”; the earlier harness computed TARGET_MET from a–d only. The final harness runs the
candidate selftest as a verdict gate and, at a rev carrying the r66 driver marker, runs the
driver at `--rev` and requires `MADO_R66_INSTRUMENT: … verdict=TARGET_MET` rc0. Independent
scratch-clone run with final drafts (`rev d6ca466…`): C1 candidate 4/4, selftest rc0,
TARGET_MET (baseline 1/4); C2 candidate 4/4, selftest rc0, driver rc0
`verdict=TARGET_MET` (baseline 1/4). Files:
`w1/R66SentFrontier/evidence/harness-final-c1.txt`, `…-c2.txt`.

### 5. Residual replace-ref gap in driver/harness

`c2-r66-landing-instrument.py` `e4d62b3c…` and `check-controls.py` `2e34eab0…` have no
`GIT_NO_REPLACE_OBJECTS`. Their `git ls-tree/show` reads at `--rev` could therefore be steered
by a local replace ref during extraction/baseline reads, the same class fixed in C1/landing.
Not live on the lane (no replace refs), and not observed in the integrated-clone run; smallest
remediation is one env assignment each (`GIT_ENV`/`clean_env`).

### 6. Quote arithmetic (seat draft only)

The integrated lesson carries one located quote, 15 words, exact at
`Exit-Status.html:68-69` / texi `:3905-3906`. The seat source gate
`w1/R66ScribeSources/gate-r66-s435.md` still says “Supporting located quote (19 words)” where
the sentence is 18 whitespace tokens by `len(split())`. Both are under the 25-word contract;
this is a seat-snippet arithmetic defect, not a production defect.

### 7. Minor stale prose about intermediate bytes

The integrated lesson’s mutation sentence calls `1671cebc…` “the final landing-script draft”
(line 45) while the same file later names `e4767ec7…` as the final standing script (line 93);
the mutation battery evidence is on `1671`. The functional delta is the two hardening exports
(`GIT_OPTIONAL_LOCKS=0`, `GIT_NO_REPLACE_OBJECTS=1`); predicate behaviour is unchanged, and all
integrated counts pass on `e476`. Treat line 45 as historical wording, or re-run the mutation
battery on `e476` for byte-bound credit. No predicate impact.

### 8. Integration dependency — RESOLVED at `043b9af1`

Before integration, S435’s `used-by` path was absent and the round-66 receipts were untracked;
`mado-receipt-citecheck.py` reported `citations=4 resolved=1 missing=3`. L1 then committed the
lesson, the S435 row, both counters, the driver, the landing script and the round-66 receipts in
one revision. At `043b9af1`:

- census end `validate --root <fleet> mado` → rc0, 0 E-lines, 0 findings naming S435, and the
  W01/W04 warning set is byte-identical to `census-start-r66.txt`;
- citecheck over the round-66 receipts → `citations=4 resolved=4 missing=0 verdict=TARGET_MET`;
- the C2 driver → `selftest=0 landing=0 green=yes verdict=TARGET_MET`, landing
  `MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0)`;
- the rule-2 diff `eafd500..043b9af1 -- corpus/SOURCES.md` is 11 insertions, 0 deletions, only
  the S435 row; no existing `opened`/`recheck`/`status`/`used-by` cell changed.

The integrated S435 row was rewritten by L1 (HTML URL in the source cell, shorter scope/teaches)
rather than taking the source-seat tarball row verbatim; it is schema-clean
(11 cells/NF=13, docs/A/mined, opened 2026-11-03, recheck on-release, used-by exists) and the
census adds no warning. The seat-draft tarball row is therefore supporting evidence, not the
integrated bytes. Evidence: `evidence/census-end-integrated.txt`,
`evidence/integrated-count-c1.txt`, `evidence/integrated-count-c2.txt`,
`evidence/integrated-driver.txt`, `evidence/integrated-verification.txt`.

### 9. Accepted C1 citation gap (do not call fixed)

With `gate-live-r65.txt` still committed, a register whose rows cite only the file-plane receipt
is accepted by the structural counter (`diag-unreferenced-live-accepted` → TARGET_MET/0; the
candidate’s own selftest asserts it). The frozen sentence is tree-level (“the exact live CLEAN
line in …gate-live-r65.txt”); L1 ruled not to tighten after scoring. It remains a citation gap,
not a truth binding. The file-plane-only control that removes the live object is rejected.

### 10. Declared limits (unchanged)

State-cell truth is not measured: forged state prose with valid receipts and the exact live line
still passes (`state-truth-not-measured`). Marker validation binds one marker line to rc; a
child that prints a correct marker over wrong data or forges its own marker is outside the
bounded structural guarantee. The frozen C2 ledger literal `MADO_TOOL_LEDGER` is not emitted by
the child; the erratum `marker-premise-erratum.md` records it and the implementation correctly
anchors the child’s actual `LEDGER:` line.

### 11. Disclosed cutover restriction

`landing-counters.sh --citecheck-paths <outside --repo>` exits 2 with `citecheck paths must be
inside repository for dirty guard`. The frozen text only says the caller may provide paths; the
landing report records this as an explicit cutover restriction. Closure should either accept
that restriction in the predicate reading or require the instrument to accept external paths
with an explicit “dirty guard unchecked” disclosure.

### 12. Informational

Landing captures each child’s combined stdout/stderr and prints/retains it verbatim; the driver
and harness retain raw logs. No draft invokes `env`, reads `$HOME`/session files, or prints an
environment dump; lane-owned children only, so raw-output exposure is limited to their own
strings (host paths, receipts), not credentials. No tmp hardcoding exists in production paths;
`/tmp`, `/var/tmp`, `/dev/shm` appear only as refusal tests. A harness seat
`__pycache__/check-controls.cpython-314.pyc` exists on disk but is not in the integrated tree at
`043b9af1`; the integration copied only the `.py`.

## Frontier conformance checks

| check | result |
|---|---|
| S435 row grammar (integrated) | 11 inner cells, split-on-`|` NF=13; `kind=docs`, `tier=A`, `status=mined`, `opened=2026-11-03`, `recheck=on-release`, `used-by=corpus/lessons/round-66.md` |
| Rule 2 / `opened` cells | `git diff eafd500..043b9af1 -- corpus/SOURCES.md` = 11 insertions, 0 deletions, only S435; no existing `opened`/`recheck`/`status`/`used-by` cell changed |
| ID / URL collision | S435 integrated once after S434; census adds no W04/E04 line; integrated URL is the HTML node, unique in the registry |
| Source quote | integrated lesson: one located quote, 15 words (`Exit-Status.html:68-69`); seat gate supporting quote is 18, not 19 (finding 6, seat-only) |
| Anchor reproducibility | Integrated row anchors `Bash Reference Manual 5.3 §3.7.5`, texi `3902-3906,3911-3916,3925-3928`, release tarball sha `0d5cd869…`; committed S110 records the same `doc/bashref.texi` 415,804 B sha `f3d37d57…`; HTML node 5,187 B sha `b5489d3d…` verified at `:68-69`. The tarball was not re-hashed here (scribe scratch removed); S110 plus the HTML digest are the independent pins. |
| Used-by path | `corpus/lessons/round-66.md` exists at `043b9af1`; census E11 clear |
| Census | end `validate --root <fleet> mado` rc0, 0 E-lines, 0 findings naming S435; W01/W04 set byte-identical to `census-start-r66.txt` |
| C1 counter | at `043b9af1`: selftest rc0; candidate 4/4 TARGET_MET; baseline 1/4; replace-ref fixture TARGET_MISSED rc1 |
| C2 instrument | at `043b9af1`: candidate 4/4, selftest rc0, driver rc0 `verdict=TARGET_MET`; landing GREEN with `citecheck=4 resolved=4`; baseline 1/4; driver on base eafd500 TARGET_MISSED |
| Tool ledger | integrated `check-tool-ledger.py --rev 043b9af1` → population=108 ledger_rows=108 bad_pointer=0 TARGET_MET; old pointer set had bad_pointer=2 |
| SKILL / QUALITY / PROVINCE | integrated SKILL Round-66 rows use `--repo --rev --scratch-root` (no `--round`); QUALITY 108 present after 107; PROVINCE round-66 refinement present |

## Commands and rc (representative; scratch paths omitted)

| command | rc |
|---|---|
| `python3 c1-r66-register.py --selftest` | 0, 15/15 |
| `python3 c1-r66-register.py --repo . --rev eafd500…` | 0 TARGET_MET |
| replace-ref fixture against final C1 | 1 TARGET_MISSED (`row-receipt-missing='walker'`) |
| `bash landing-counters.sh --selftest --scratch-root …` | 0, 58/58 |
| `bash landing-counters.sh --repo <lane> --rev HEAD --round 65 --citecheck-paths …` | 0 GREEN |
| index-refresh probe, old 1671 / final e476 | old INDEX_CHANGED / final INDEX_UNCHANGED |
| **frozen** `check-controls.py --rev 043b9af1 --claim c1` | 0, baseline 1/4, candidate 4/4 + selftest, TARGET_MET |
| **frozen** `check-controls.py --rev 043b9af1 --claim c2` | 0, baseline 1/4, candidate 4/4 + selftest + driver TARGET_MET |
| `c2-r66-landing-instrument.py --repo . --rev 043b9af1` | 0 `selftest=0 landing=0 green=yes verdict=TARGET_MET` |
| landing log at `043b9af1` | `MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0)`; citecheck 4/4 |
| driver `--repo <lane> --rev eafd500… --scratch-root …` | 1 TARGET_MISSED (baseline refuses `--round`) |
| `check-tool-ledger.py --repo . --rev 043b9af1` | 0, population=108 ledger_rows=108 bad_pointer=0 TARGET_MET |
| `sources-census.sh validate --root <fleet> mado` (end) | 0, 0 E, 0 S435 findings, warning set unchanged |
| `sources-census.sh validate --root <mirror> <mirror>/lane` (pre-integration S435+lesson) | 0, 0 E, 0 S435 findings |
| `git diff eafd500..043b9af1 -- corpus/SOURCES.md` | 11 insertions, 0 deletions (S435 only) |

## Limitations

- This seat made no production edits and no commits. L1 integrated at `043b9af1`; all count,
  driver, census and ledger results above are at that revision. This report was written after
  the integration commit and is untracked in the worktree; L1 owns committing it.
- The tarball bytes were not re-hashed (scribe scratch removed); reproducibility rests on the
  official tarball digest in the integrated row, the HTML node digest I re-fetched, and S110’s
  identical `bashref.texi` digest.
- Drafts moved during the audit; the hash table is the integrated set, and finding 7 records the
  remaining historical-wording mismatch.
- Marker authenticity is bounded structural consistency; a malicious child forging its own
  marker is outside the claim (declared).
- No whole-repo build/lint/test storm, no credentials/session reads, no r56 material, no host
  or lane git/jj mutation; fixtures were scratch-only with explicit `git -C` and toplevel
  verification, and scratch was removed before yield.

## Changed drafts

None. Only this report and `w1/R66SentFrontier/evidence/` were written.
