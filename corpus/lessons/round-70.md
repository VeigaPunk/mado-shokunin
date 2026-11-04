# mado round 70 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-04 (America/Sao_Paulo)
base: `b37a5aec4ea03f2223d8e09dd5d386d055c24179`
frozen declaration: `.ufo/waves/round-70/claims-declaration-r70.md`, `bc18399b409a6390a6c6e8831bf9ad2dacbbf189`
control set: `.ufo/waves/round-70/controls/c2-controls-r70.json`, sha256
`29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff` (17 cases)
pre-freeze baseline: `.ufo/waves/round-70/control-baseline-r70.txt`
measured content: `3d28f92a819b84e2004ef1301f9303f81ad497ab` (C2 classifier repaired after review;
C1's counter byte-identical to its `5adba5a9` form); record tip `f754347a` and the commits after it

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data.

- **C1 calibration — the landing harness credits a kill only on a parsed failed assertion, proven
  with real children.** At the measured revision the frozen counter
  `quality/counters/c1-r70-real-children.py` builds a scratch git fixture whose lane decides its
  behaviour from the frozen clause's own effect, runs three real `bash` children (a genuine failed
  assertion, a crash with no summary, a garbled summary) against the round-70 harness
  (`c1-r70-landing-controls.py`) and the frozen round-69 harness, and requires
  `correct=3 base_correct=1`. Measured `cases=3 correct=3 base_correct=1 verdict=TARGET_MET` rc 0
  (`measurement-r70.txt`). At the base rev both the counter and the successor harness are absent;
  the held harness credits all three scenarios (`base_correct=1/3`) — the do-nothing control.
- **C2 operability — the guard census counts four more carrier shapes.** At the measured revision
  `quality/counters/c2-r70-carriers.py` applies the round-69 key-position and dominance rule plus
  alias, attribute, `**`-splat and module-string-constant-key carriers to the frozen 17-case set and
  requires `population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17`.
  Measured exactly that, rc 0. The held round-69 classifier scores 13/17 on the same set, missing
  exactly the four new carriers. **After review** (`w1/R70RevC2.md` blockers 1-2) the implementation
  was repaired against the same frozen sentence - attribute carriers now require store-before-use
  with no intervening replacement, and a module constant counts only when the store's scope does not
  rebind it - with the red-before/green-after in
  `.ufo/waves/round-70/c2-classifier-repair-r70.txt`; the frozen 17 score identically before and
  after, and the five attack cases are pinned in the counter's selftest (54/54).

**Not claimed.** Universal fault coverage; that three scenarios exhaust the kill-credit hazards;
that the fixture lane is the lane's real landing instrument; that the four carriers are the only
remaining Python shapes; that the dominance rule is sound for arbitrary Python (one module, one hop,
one-level `**` of a module-level literal mapping, no attribute chain longer than one dotted name, no
path-sensitivity beyond a literal-false branch); runtime behaviour of the extracted instruments; that
a guarded environment authenticates objects or repairs a rewritten repository; state truth of any
`PROVINCE.md` cell; any desktop, compositor, session or service observation (none was probed); any
`[x]`, promotion or axis retirement.

**Source substitution (pre-data).** The declaration named CPython `Doc/library/subprocess.rst` as
C1's ground. The registry already holds that URL as S108 with the same bytes (61,603 B, sha256
`05cd782c…`), so no row was appended for it; C1 instead rests on the held S435 (Bash exit-status
vocabulary), and the two opened rows S439/S440 ground C2. The predicate, counter, kill rule and
target are unchanged; only the source plan moved, and it moved before the first candidate run.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M70-1: the first committed C1 counter (`5144a6b5`) created no per-scenario scratch directory, so `subprocess.run(cwd=…)` raised `FileNotFoundError` mid-measurement. | setup bug committed before the command ran | first measurement attempt: `FileNotFoundError: …/meas-c1/r70-c1/cand-genuine`; fixed in `9508e878` with `os.makedirs(scratch, exist_ok=True)` in `run_harness` | **existing criterion 110(a)** — "a counter is frozen only after its declared command is run verbatim". The L1 committed the instrument before running the frozen command, exactly the defect that criterion names. The counter's hermetic `--selftest` cannot see it (it forbids spawning). | The frozen command was then run at `5adba5a9` and is the receipt this round cites. The rule the round re-learns: run the advertised command against a scratch fixture *before* the instrument commit, not after. |
| M70-2: the C2 entry's `source:` line was first written with a placeholder digest (`1e7f0a3c…`) instead of the fetched bytes' sha256. | fabricated value in a draft | caught by re-grepping every digest against `sha256sum` of the three fetches before commit; the committed line carries `e19de4fe…` / `d4320642…` and their byte counts | `none` — no rule said an entry's `source:` digest must be re-derived from a fetch in the same round | Every `source:` digest in this round's entries was re-derived with `sha256sum` from `$S/src/*.1` and cross-checked against the three fetched copies' identity (`sha256sum | sort -u | wc -l` → 1). The failure it can show: a digest that matches no fetched byte. |
| M70-3: the declaration named a source URL without checking the registry first, and the URL was a duplicate (S108). | plan-level, caught pre-data | `grep -n 'Doc/library/subprocess.rst' corpus/SOURCES.md` → S108 (61,603 B, `05cd782c…` — the same bytes); `.ufo/waves/round-70/w1/R70ScoutSources.md` § F1 confirms the same tag pin | `none` for the plan phase; the census's duplicate-URL rule caught the row only after it would have been appended | The round refused the row and substituted the held S435 for C1; the registry diff is 2 rows (S439/S440), not 3. A later declaration must run the duplicate check at freeze time. |
| M70-4: the C2 counter printed the candidate and base leg's `MADO_R70_CONTROL` lines under one label, so the receipt carried 34 lines with duplicate case names and only the summary separated the legs. | observability | `.ufo/waves/round-70/measurement-r70.txt` before `5adba5a9` (17 `correct=no` lines from the base leg are indistinguishable from candidate misses) | `none` | Fixed in `5adba5a9` (`leg=candidate|base`), an observability change only; the contract line and verdict are unchanged, and the selftest stays 49/49. |
| M70-5: the round-69 LOG block was inserted into the Round 67 and Round 68 entries, and one round commit was left unenumerated (outside spot-check defects 1–2). | record order, inherited | `corpus/lessons/round-69-verifier-spotcheck.md` § Conformance defects 1–2; `LOG.md:3257-3266`, `3314-3323`, `3396-3405`; `grep -rn b9b70a09` rc 1 | `none` before this round — no criterion required an append to be anchored to its own round heading, or the commit list to close against the range | QUALITY criterion 112 is registered from this defect, and this round's own LOG block is appended under the Round 70 heading only. The sweep that would have caught it: `grep -n 'Wave settlement: 12 seats dispatched' LOG.md` (three hits before r70) and `git rev-list --count <base>..<tip>` against the report's enumerated rows. |

A fix counts only on its named red/green evidence: M70-1's red is the first measurement attempt's
traceback (no data was produced) and its green is `measurement-r70.txt` at `5adba5a9`; M70-2's and
M70-3's checks are the grep/sha256 transcripts in this round's shell history and the registry diff;
M70-4's green is the same receipt's `leg=` labels.

## Gate

Admitted, **S439** — CPython v3.14.8 `Doc/reference/expressions.rst`, § Dictionary displays.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (`sha256`
  `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92,034 bytes, 2,407 lines);
  the scout's independent fetch agrees on the bytes and on the tag pin (tag object `992560c2…`,
  peeled commit `8e6e75d9…`).
- Located quote, 22 words, expressions.rst:514-517: "A double asterisk `**` denotes dictionary
  unpacking. Its operand must be a mapping. Each mapping item is added to the new dictionary."
- Why it grounds the claim: the carrier rule counts `env = {**os.environ, **GUARD}` as a carrier of
  the key only because the documented semantics *add the mapping's items to the new dictionary* —
  not because the token appears.

Admitted, **S440** — CPython v3.14.8 `Doc/reference/simple_stmts.rst`, § Assignment statements.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (`sha256`
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41,375 bytes); the required
  sentence is **not** in `expressions.rst` (the declaration's and this lesson's brief assumed it
  was), so the row was opened against the page that actually carries it.
- Located quote, 21 words, simple_stmts.rst:190-192: "If the target is a subscription: The primary
  expression in the reference is evaluated. Next, the subscript expression is evaluated."
- Why it grounds the claim: a subscript store evaluates the *subscript expression*, so
  `env[KEY] = "1"` with `KEY = "GIT_NO_REPLACE_OBJECTS"` stores under the key's value; the name is
  not a mention.

Admitted, **S441** - CPython 3.14 documentation (rendered), `subprocess`, `CompletedProcess.returncode`.

- URL: `https://docs.python.org/3.14/library/subprocess.html`
- Access date: 2026-11-04, fetched three times, byte-identical (`sha256`
  `c8a66b3abf91790cea34128c5636c2e27a4b26ade459f7d4f797400da706079f`, 207,155 bytes); the page is
  the site's own rendering of the 3.14 line (`<title> Python 3.14.10 documentation`), a different
  artifact from S108's raw `subprocess.rst`.
- Located quote, 17 words, subprocess.html:361-363: "Exit status of the child process. Typically, an
  exit status of 0 indicates that it ran successfully."
- Second located quote, 14 words, subprocess.html:364-365: "A negative value -N indicates that the
  child was terminated by signal N (POSIX only)."
- Why it grounds the claim: the status is the child process's exit status and a negative value is a
  signal death, so the harness cannot read a nonzero status as an assertion result; this is C1's
  opened row, and S435 stays the held multi-cause vocabulary.

Rejected: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst` as
a **new** row. Reason: duplicate scope — the URL is S108 (same 61,603 B, `05cd782c…`), and S108's
recorded claim is the `args` binding, not the `returncode` paragraph; appending a second row for the
same URL would double-index one page. Flip condition: a later round that must quote the `returncode`
paragraph re-opens S108 as a superseding row for that page with the new anchor, rather than adding a
second row for the same bytes.

Rejected: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/ast.rst` as a new
row. Reason: it documents the node vocabulary the classifier *reads*, not the runtime carrier
semantics the claim rests on; a syntactic reference would ground the implementation's shape, and the
claim is about what an environment is. Flip condition: a future claim whose subject is the
classifier's own grammar (for example "this detector keys on `ast.Subscript` with a store context")
re-opens it then.

Registry cell changes (old → new, logged per `CORPUS.md` rule 2): **S435 `used-by`**
`corpus/lessons/round-66.md` → `corpus/lessons/round-66.md,corpus/knowledge/landing-kill-credit-real-children-r70.md`
(the round-70 entry cites the held row; the reverse link was the used-by leg's one `missing` before
the append and `verdict=TARGET_MET` after it). The three adopted rows S439/S440/S441 are appends
(`status: mined`, `opened: 2026-11-04`, `recheck: 90d`, `used-by` naming the round's entry and
lesson). No `status` or `recheck` cell changed.

Assimilation: none this round — no `merge/mado/` theme was taken. `considerthese/2026-10-28.md`
proposal 4 (a live-tool table) is named in the round report as an unmined proposal (it governs
live-state instruments on a probed host; this round probes no host), not adopted.

## Wave findings

The orchestrator sent WAVE-DONE for the one v1 wave: all 14 seats settled. Results are committed at
`.ufo/waves/round-70/w1-results.json`. The material findings and dispositions follow.

- **C2's attribute and constant-key carriers bypassed the dominance test** (`w1/R70RevC2.md` blockers
  1-2). Repaired against the frozen sentence; red-before to green-after in
  `c2-classifier-repair-r70.txt`; the five attack cases are pinned in the selftest (54/54).
- **C2's splat/alias prose is broader than the implementation** (`dict(os.environ, **GUARD)` and a
  two-hop alias are missed). Disclosed as declared limits; both are pinned at `(True, False)` in the
  selftest so a future widening is a visible case change, not a silent one.
- **C1's counter cannot tell a correct decision from an agreement-only stand-in** (`w1/R70RevC1.md`
  finding 1). Disclosed; the claim is bounded to the delivered harness's decisions on three inputs.
- **The landing instrument's default `--citecheck-paths` is a setup failure** (no
  `.ufo/waves/round-N/receipts` directory exists in any round; `w1/R70ExecCadence.md` finding 2).
  Pre-existing; the round passes explicit committed paths and records both runs.
- **`check-deliverables.py` is red on the round-69 seat reports** (a doubled seat prefix in one
  trailer; eight without trailers). Pre-existing, not round-70 harm.
- All 14 seats settled per the orchestrator's WAVE-DONE message. The results file contains 14
  outputs but no per-seat status field; zero dead seats is based on that handoff, not a parsed
  status field.
