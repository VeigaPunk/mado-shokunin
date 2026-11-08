# R100MCriticClaims -- falsification of the round-100 claims as sentences

Seat: R100MCriticClaims (critic). Round mado 100 (hyaku run 15, attempt 1), wave w1.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4` (branch master).
Contract read first: `.ufo/waves/round-100/claims-declaration-r100.md`
(predicate sentences frozen before any case is scored).
Also read: `corpus/QUALITY.md` (criteria 1-172a, including M99-3's rule that a
frozen sentence wider than its instrument must be amended down pre-file),
`corpus/lessons/round-99.md`, `corpus/lessons/round-99-verifier-spotcheck.md`,
`plans/round-100.md` (pre-file amendments section is empty -- this report is its
input), `quality/harm-watch.py`, `quality/counters/c1-r99-launchenv.py`,
`quality/counters/c2-r99-harm-watch.py`, `tools/mado-launchenv.py`,
`tools/mado-mime.py`, `.ufo/waves/round-99/controls/launchenv-cases-r99.json`,
`.ufo/waves/round-99/controls/harm-panel-r99.json`,
`.ufo/waves/round-99/controls/launchenv-probe-r99.py`,
`.ufo/waves/round-99/receipts/c2-measured-r99.txt`, `.ufo/waves/round-100/claims.json`.

Axes (per the seat spec and Godspeed step 1):

- **C1 -- coverage.** Claim: the PATH-unset default search path of the launch load
  gate becomes exercised by frozen cases (round-99 spot-check routed defect 4).
- **C2 -- operability.** Claim: the harm watch's per-leg cap becomes measured and
  the 28-leg panel goes green (routed defect 3 / round-99 lesson M99-4).

Axes that improve: none by attack (this seat only attacks). Axes harmed: none
(attack artifact only; report writes nothing else). Standing verdicts reached:
- C1 sentence wider than its instrument: **CONFIRMED** (3 exact narrowings).
- C2 sentence wider than its instrument: **CONFIRMED** (4 exact narrowings).
- Self-certification path in C2: **OPEN** (the round-100 C2 predicate dropped
  every anti-self-cert conjunct its round-99 predecessor carried).
- No-work controls: C1's do-nothing control measures a label, not a branch
  (**measures nothing that discriminates**); C2's cap is a declared number, not
  a measured one, under the frozen predicate (a hand-written timing receipt
  satisfies every conjunct).

---

## 1. Sentence vs instrument -- C1 (coverage)

### 1.1 The frozen sentence (claims-declaration-r100.md:11-21, verbatim substance)

> At the base revision 43309e6a, the PATH-unset default search path of
> `g_find_program_for_path` (gutils.c:370-382: the literal `/bin:/usr/bin:.`,
> used when the `PATH` variable is absent from the environment) is modelled by
> `tools/mado-launchenv.py` (`DEFAULT_SEARCH_PATH`) and exercised by **zero**
> frozen cases: both `path-unset` cases in the round-99 case file carry an
> **absolute** `Exec`, which returns at gutils.c:331-357 before the PATH source
> is read at gutils.c:370. After this round the frozen case file
> `launchenv-cases-r100.json` carries a `path-default` class of **>=6** cases,
> every label measured against the installed `/usr/bin/gio`
> (sha256 d2164260...cfc462, glib2 2.90.1-1) and re-measured twice with agreeing
> results, and `tools/mado-launchenv.py` answers **every** case of that set
> (the whole set, not only the new class) in agreement with the oracle,
> including a seeded fresh leg and a counted mutant population.

The last paragraph (declaration:23-34) adds three separations (unset != empty;
unset != ambient search; the default's trailing `.` is real) and closes: "The
class must separate the unset default from all three neighbouring behaviours,
or the branch is not cored."

### 1.2 The weakest property PRED-C1-r100-v1 actually enforces (declaration:39-47)

```
default_cases >= 6 AND default_classes >= 3 AND cases_correct == cases_total
AND fresh_correct == fresh_total (>= 8) AND mutants_killed == mutants_counted (>= 4)
AND base_set_default_cases == 0
AND control_unset_as_empty_correct < cases_total
```

Clause by clause, what each conjunct can and cannot see:

- `default_cases` / `default_classes` count **labels** in the pinned case file.
  The counter reads the JSON bytes; it does not read fixture geometry.
- `cases_correct == cases_total` compares the candidate's output against the
  **frozen `expect` labels in the pinned file**, not against the oracle at
  measurement time. (The round-99 counter's contract, which the round-100
  counter follows, is contract 2: cases are `expect`-carrying dicts; the
  oracle that produced them is not re-run by the counter. The counter never
  opens `/usr/bin/gio`; the gio sha is a pin on the label file's envelope.)
- `fresh_correct == fresh_total` scores the **fresh generator's** cases, whose
  class composition the predicate does not constrain (only `fresh_total >= 8`).
- `mutants_killed == mutants_counted` counts mutants anchored **anywhere** in
  the candidate's non-selftest prefix. Nothing in the predicate requires a
  mutant to touch the `DEFAULT_SEARCH_PATH` line or the `path is None` branch.
- `base_set_default_cases == 0` counts labels in the round-99 file, whose
  class vocabulary (`prog-abs`, `path-unset`, ...) contains no `path-default`
  label at all. See 1.4/F3.
- `control_unset_as_empty_correct < cases_total` is the only conjunct that can
  see the branch at all: it requires that a model that treats unset as empty
  disagrees **somewhere** with the frozen labels. It is a one-case threshold.

### 1.3 Same sentence? No. The divergences (sentence minus instrument)

1. **"every label measured against the installed /usr/bin/gio ... and
   re-measured twice with agreeing results"** -- the predicate never observes a
   measurement. There is no conjunct, receipt field, or pin that distinguishes
   an oracle-measured file from a hand-typed one that happens to agree with
   the candidate. The gio sha is a pin on the case file's envelope, i.e. a pin
   on bytes the round itself freezes. Provenance sentences of this shape are
   the M99-1 class (a claim about bytes that no checker re-derives); criterion
   147 binds a file to its digest, never a file to a measurement event, and
   criterion 24 requires a producer field *in the receipt* -- the predicate
   carries no producer conjunct. The sentence must be narrowed to what the
   instrument enforces: "every case carries a frozen `expect` label in the
   pinned file."
2. **"tools/mado-launchenv.py answers every case of that set in agreement with
   the oracle."** What is enforced is agreement with the frozen labels. When
   labels and oracle disagree, the honest tool scores `cases_correct <
   cases_total` -- the predicate rewards agreement-with-file, and can only
   punish agreement-with-oracle in that case. The sentence's "in agreement
   with the oracle" must be narrowed to "in agreement with the frozen labels
   measured (by the wave's own measurement, carried by receipt, not by this
   predicate) against the oracle."
3. **"The class must separate the unset default from all three neighbouring
   behaviours, or the branch is not cored."** The three separations are
   fixture-geometry sentences: e.g. separation 1 requires a program reachable
   under unset but not under `PATH=""`. `default_classes >= 3` counts distinct
   label strings and is satisfiable by splitting one identical geometry under
   three names (`path-default-a`, `path-default-b`, `path-default-c`). This is
   exactly criterion 160's "population read from the data it judges" shape:
   the labels are both the fixture and the verdict. The three separations
   appear in **no conjunct**. Worse: `control_unset_as_empty_correct <
   cases_total` is satisfied by **exactly one** discriminating case, so the
   predicate enforces "at least one case separates unset from empty", while
   the sentence promises "a class of >=6 cases" of which the whole class
   separates. Five of the six may be `pu-abs` clones (absolute `Exec`,
   `path: null`) -- the before-state geometry itself -- and every conjunct
   still holds provided one discriminating case exists. That is the M99-3
   defect in fresh bytes.
4. **"including a seeded fresh leg"** -- the fresh leg is unconstrained by class.
   A generator emitting eight `prog-abs` cases satisfies `fresh_total >= 8`
   and `fresh_correct == fresh_total` while covering the default branch zero
   times. The predicate's fresh conjunct therefore does not extend coverage
   to the named surface; the sentence's "including a seeded fresh leg" (in the
   clause whose subject is the set of that set's answers) implies it does.
5. **"and a counted mutant population"** -- `mutants_counted >= 4` with no
   anchoring requirement to the default branch. Four mutants on the terminal
   table (e.g. reordering `KNOWN_TERMINALS`) satisfy the conjunct while the
   default search path stays one-character-mutable and un-killed. The
   sentence's proximity to "answers every case of that set" implies the
   population guards the branch; the predicate does not.

### 1.4 Falsifications (counterexamples), each constructible from committed bytes

**F1 -- the six-case class that never reaches the branch (the strongest C1
counterexample).** Take the two committed `path-unset` cases
(`pu-abs-work`, `pu-abs-root`, verified below) and clone the
`pu-abs-root` geometry six times with new ids, labels honestly measured (both
`Exec` and `TryExec` absolute, `path: null`). File them under three labels
`path-default-x/y/z`. Add one genuine discriminating case (bare `Exec=sh`,
`path: null` -- oracle resolves `/bin/sh` through the default) so that the
empty-default control disagrees at least once. Every conjunct of
PRED-C1-r100-v1 holds: `default_cases=6`, `default_classes=3`,
`cases_correct==cases_total` (the honest candidate agrees with all frozen
labels), `base_set_default_cases==0`, `control_unset_as_empty_correct =
total-1 < total`. Yet five of six new cases never read the PATH source -- they
return at `gutils.c:331-357` exactly as the r99 pair does -- so the frozen
sentence "a `path-default` class of >=6 cases" of *the default search path*
is false in the only sense that matters, and the axis has not moved: the
branch-reaching case count is 1, not 6. The predicate cannot reject this
set; the prose separations (?1-3) are the only words that forbid it, and the
counter does not enforce them.

Evidence (re-measured this seat, base revision):

```
git show 43309e6a:.ufo/waves/round-99/controls/launchenv-cases-r99.json
  -> 67 cases; exactly 2 with path == null; both carry Exec "{root}/probe.sh"
     (absolute); 0 cases with path == null and a non-absolute Exec.
```

**F2 -- three classes that are one.** `default_classes` counts distinct
`class` strings among the default cases. Splitting one geometry under three
label strings satisfies `>= 3` without separating anything. Criterion 160
enumerates populations in the declaration, never reads them from the data it
judges; here the class minimum *is* read from the judged data, and no frozen
list of the three required classes (one per separation) is pinned anywhere in
the predicate. The declaration *names* three separations in prose but does not
make them three named classes with per-class minima (the M94-2 shape).

**F3 -- the do-nothing control measures a label, not a branch.** The r99 file's
class vocabulary contains no `path-default` label (verified: the 31 distinct
classes are `path-empty-entry`, `tryexec`, `exec-test`, `refuse-shape`, ...).
`base_set_default_cases` is therefore 0 for **any** candidate and **any**
r100 set, by construction of the label vocabulary, before any case is
scored. The control is presented as "the do-nothing control, measured on the
r99 case file" (declaration:45) -- but the do-nothing it inspects is the
*failure to apply a label this round invented*, not the failure to exercise
a branch. A base file that contained a bare-Exec `path: null` case under the
label `prog-bare` would still read `base_set_default_cases == 0` while the
sentence's before-state ("exercised by zero frozen cases") would be false.
The before-state sentence happens to be true (verified above: 0 bare-unset
cases), and it is verified here by direct inspection of the two `path-unset`
cases' `Exec` bytes -- i.e. by the *reviewer's* reading, not by the conjunct.
The narrowing must say so.

**F4 -- the same branch is modelled twice, so the "before" sentence already
repeats the M99-3 error once.** `tools/mado-mime.py` at base line 466
(`find_program`, erratum pointer 172a) already ports
`g_find_program_for_path` with the identical unset default
(`path_env if path_env is not None else "/bin:/usr/bin:."`), and
`tools/mado-launchenv.py` selftest already exercises it at base
(`fp-default-path-has-sh`: `find_program('sh', None, None) is not None`;
`fp-default-path-miss`). Re-measured this seat:

```
git show 43309e6a:tools/mado-mime.py | grep -n 'def find_program'
  -> 466:def find_program(program: str, path_env: str | None, workdir: str | None)
git show 43309e6a:tools/mado-mime.py | sed -n '466,482p'
  -> ... search = path_env if path_env is not None else "/bin:/usr/bin:."
python3 -I tools/mado-launchenv.py --selftest  (at base bytes a63c20c8...)
  -> MADO_LAUNCHENV_SELFTEST: checks=90 failed=0
```

The frozen C1 sentence is carefully worded to claim only *frozen-case*
exercise ("exercised by zero **frozen** cases"), and that wording is true.
But the claim's headline -- "C1 -- coverage: the PATH-unset default search
path of the launch load gate" -- plus the "branch is not cored" close
(declaration:23-24) invite the wider reading, and the wider reading is the
M99-3 failure the plan claims was learned: at base, two lane instruments
already answer the default (`mado-mime.py:466` and `mado-launchenv.py:121,207`),
and the candidate's own selftest (90 checks, green at base bytes) already
hits the unset branch. Nothing in the predicate distinguishes the branch's
*frozen-case* surface from its *selftest* surface; the axis credit will be
read as "the branch becomes covered" (wider) while the instrument proves
"6 labels are added to a file" (narrower). The plan's surface sentence
(plans/round-100.md:15 names "the PATH-unset default branch of the launch
load gate") must be narrowed to the frozen-case surface, or the claim must
carry the selftest surfaces in its before-state.

*(Locator drift, for the records, M99-2 class -- noted, not counted as a
falsification of the sentence's substance: declaration:12 cites
`gutils.c:370-382` for the literal, `.ufo/waves/round-100/claims.json` cites
`gutils.c:376-389` for the same literal, and `tools/mado-launchenv.py:120`
cites `gutils.c:409-421` for the same literal. At most one of the three
ranges contains the literal. The seat could not re-open `gutils.c` from
custody this round (round-99 `fetch/gutils.c` exists at the r99 wave dir and
the L1's ground note asserts 370-382 for the PATH source itself rather than
the literal); the L1 must re-derive all three locators by `grep -n` on the
fetched bytes before filing, per M99-2's rule. None of the three is
predicate-bearing: no conjunct reads a line number.)*

### 1.5 Exact narrowing the L1 must record in plans/round-100.md before filing

Per the pre-file falsification rule (addendum ?8, criterion 172), this seat
states the smallest truthful rewrites -- the L1 must record each in
`plans/round-100.md` with this artifact (`w1/R100MCriticClaims.md`) as the
forcing artifact:

1. Replace "every label measured against the installed `/usr/bin/gio` ... and
   re-measured twice with agreeing results" with: "every case carries a frozen
   `expect` label in the pinned case file; the measurement lineage (oracle
   digest, double measurement) is carried by the wave's measurement receipt,
   not by this predicate."
2. Replace "answers every case of that set in agreement with the oracle" with
   "answers every case in agreement with the frozen labels in the pinned case
   file."
3. Delete "The class must separate the unset default from all three
   neighbouring behaviours, or the branch is not cored" from the frozen
   statement, OR add three predicate conjuncts pinning one named class (and
   its per-class minimum) per separation, with a counter check that the
   paired fixtures differ only in PATH (see F1/F2). Until then, the filed
   sentence must read: "the predicate enforces at least one case whose label
   the empty-default misreading cannot reproduce; the remaining default cases
   are enumerated by label only."
4. "including a seeded fresh leg" -> "including a seeded fresh leg of >=8
   cases of unconstrained class composition; the fresh leg is not a
   default-branch coverage leg."
5. "and a counted mutant population" -> "and a counted mutant population of
   >=4 mutants anchored anywhere in the candidate; the predicate does not
   require a mutant on the default-search-path branch."
6. `base_set_default_cases == 0` must be glossed in the filed sentence as:
   "counts the `path-default` label in the r99 file; branch-reachability of
   the r99 file was established by direct inspection of its two `path-unset`
   cases' absolute `Exec` bytes (this report, ?1.4/F3), not by this conjunct."
7. The plan's surface sentence ("the PATH-unset default branch of the launch
   load gate", plans/round-100.md:15) must be narrowed to "the PATH-unset
   default branch **as exercised by frozen cases** (it is already modelled by
   `tools/mado-mime.py:466` and exercised by `tools/mado-launchenv.py`'s
   selftest at base)."

---

## 2. Sentence vs instrument -- C2 (operability)

### 2.1 The frozen sentence (declaration:68-78)

> At the base revision 43309e6a, the frozen 28-leg harm panel
> (`.ufo/waves/round-99/controls/harm-panel-r99.json`) carries
> `timeout_s: 600` with no per-leg timing and no headroom, and on this host
> two legs (`r92_gate_defects`, `r97c1_filetype`) exceed that cap, so the
> panel reports `mismatches=2` (round 99's C2 honest stop; receipt
> `.ufo/waves/round-99/receipts/c2-measured-r99.txt`). After this round
> `quality/harm-watch.py` reports each leg's measured elapsed milliseconds
> (`LEG <id> rc=... ... elapsed_ms=<n>` on the human line and an `elapsed_ms`
> field per leg in `--json`), the frozen panel
> `.ufo/waves/round-100/controls/harm-panel-r100.json` carries `timeout_s`
> equal to at least twice the largest per-leg elapsed measured on this host
> at committed bytes (timing receipt
> `.ufo/waves/round-100/receipts/panel-timing-r100.txt`, all 28 legs timed),
> and a full-panel run at committed bytes reports `HARM_WATCH:
> legs=28 ... mismatch=0`.

### 2.2 The weakest property PRED-C2-r100-v1 actually enforces (declaration:83-89)

```
panel_legs == 28 AND legs_run == 28 AND mismatches == 0
AND gate_elapsed_emitted == 1   (human LEG line carries elapsed_ms= AND json legs carry elapsed_ms)
AND timing_legs_timed == 28
AND max_elapsed_ms > 600000
AND panel_timeout_s * 1000 >= 2 * max_elapsed_ms
AND control_600s_would_mismatch >= 1  (derived from the same timing receipt)
AND selftest_failed == 0
```

The counting command (declaration:95-99) runs the round's own counter over
the round's own frozen panel and the round's own timing receipt. The counter
is an instrument that spawns git, the gate, and reads pinned files; it is
not itself a modelled candidate (same shape as the r99 counter).

Clause by clause:

- `gate_elapsed_emitted == 1` checks **presence** of `elapsed_ms=` on the
  human line and an `elapsed_ms` field in the JSON. It does not compare the
  printed value against the wall time of any leg the counter itself ran.
  (Shared contract 3, declaration:137-139, additionally requires selftest
  checks for presence, non-negativity, integer-ness, and monotonicity across
  a fixture whose second leg is slower -- but those checks are the gate's
  own code, exercised by `selftest_failed == 0`; see ?5.)
- `timing_legs_timed == 28` and `max_elapsed_ms` are read from the wave's
  timing receipt -- a text file the wave authors -- and pinned by sha. The
  counter counts rows in the receipt and takes their maximum; it does not
  re-derive any elapsed value, and the predicate does not require the
  receipt's maximum to equal (or bound) the elapsed values the counter's own
  full-panel run observes. "On this host at committed bytes" has no
  predicate reading: no conjunct binds the receipt to a host, a revision, or
  a producer (criterion 24's receipt-borne producer fields are absent from
  the predicate).
- `panel_timeout_s * 1000 >= 2 * max_elapsed_ms` is satisfied by any
  sufficiently large `timeout_s`, including `timeout_s = 10^9`. There is no
  upper bound. The predicate therefore rewards the *largest* cap, not the
  *adequate* one; the "measured headroom" discipline of the sentence
  ("at least twice the largest...") is a lower bound the counter can see, while
  the sentence's implication -- the cap is a rational, measured value -- is not
  enforced.
- `control_600s_would_mismatch >= 1` is derived from the **same** timing
  receipt as `max_elapsed_ms`. It is not a 600-second run delivered by the
  counter: no conjunct runs the gate at a 600 s cap and observes a timeout.
  The "control" is an arithmetic consequence of the receipt it controls.
- No conjunct pins the panel's leg identity. `panel_legs == 28` counts rows.
  The eight contract rows-per-leg fields (`id`, `round`, `argv`,
  `expect_rc`, `expect_marker`, `note`) may be rewritten arbitrarily provided
  the census (28 declared ids, each leg's marker occurring in its output)
  still passes. The r99 panel binds legs to rounds (`base`, `r90`-`r97`)
  and ids to arguments (counters, selftests, gates); a panel that swapped
  `r92_gate_defects` (a slow, real counter) for a trivial
  `python3 -I tools/mado-verify.sh --selftest`-shaped leg with the same id
  would still score `panel_legs == 28 AND mismatches == 0`, because the
  counter only asks each leg to match its own frozen expectation. The
  sentence's "the frozen 28-leg harm panel" (which names the r99 set) is
  carried by the `expect-panel-sha256` pin only to the extent the L1 froze
  the pin on the unchanged leg rows; the predicate text itself never says
  so. (Shared contract 3 does say the 28 leg rows "stay byte-identical to
  the round-99 panel", declaration:139-140 -- that sentence, like the C1
  separations, is prose outside the predicate. The L1 must either freeze a
  leg-identity conjunct, e.g. `panel_legs_match_r99 == 28`, or narrow the
  filed sentence to "a frozen 28-leg panel of the same census shape.")
- `max_elapsed_ms > 600000` requires the defect **to persist**: a host or
  leg population fast enough that all 28 legs finish in under 600 s cannot
  satisfy the predicate even with a green panel and a rational cap. The
  predicate does not check "the cap is adequate"; it checks "the cap is
  adequate **and** the old cap was inadequate", where both halves are read
  off the same receipt. The repair narrative (M99-4) is baked in as a
  conjunct, so the instrument can never certify the defect's absence.

### 2.3 Same sentence? No. Exact narrowings (L1 must record in plans/round-100.md)

1. "reports each leg's measured elapsed milliseconds" -> "prints an
   `elapsed_ms` field per leg (human line and `--json`); its being a true
   measurement of that leg is carried by the gate's selftest fixture, not by
   this predicate."
2. "`timeout_s` equal to at least twice the largest per-leg elapsed measured
   on this host at committed bytes" -> "`timeout_s` at least twice the largest
   elapsed value recorded in the wave's timing receipt (whose host/revision
   binding is carried by that receipt, not by this predicate); the predicate
   imposes no upper bound on `timeout_s`."
3. "all 28 legs timed" -> "the timing receipt carries 28 rows; the predicate
   does not require them to equal the elapsed values observed in the
   counter's own panel run."
4. "the frozen 600 s cap is structurally too small on this host: the control
   is measured, not asserted" (declaration:86-88) -> "the 600 s cap would be
   too small for the legs listed in the timing receipt; no 600-second run is
   delivered by this counting command."
5. "a full-panel run at committed bytes reports mismatch=0" -> "the counter's
   own full-panel run at `--rev` reports mismatch=0" (the predicate has no
   committedness conjunct; `--rev` may name the worktree).
6. Delete "the frozen 28-leg harm panel" (definite article, this panel) from
   the filed sentence unless a leg-identity conjunct is added; file
   "a 28-leg frozen panel of the same census shape."

Before-state verification (this seat re-measured, so the narrowing above does
not touch the before-state): at base the gate carries no timing at all
(`run_leg` returns `{id, rc, out, err, detail, legdir}`; the human line is
`LEG %s rc=%s expect=%s marker=%s %s`; `leg_timeout` reads
`panel["timeout_s"]` with default 3600 and the panel carries 600), the panel
carries 28 rows under rounds `base,r90,r92,r93,r94,r95,r96,r97`, and the
round-99 honest-stop receipt reads `mismatches=2` with legs `r92_gate_defects`
and `r97c1_filetype` at `rc=124 timeout-after-600s`. The before-state
sentence is true as written and is not narrowed.

### 2.4 Counterexample: the green predicate with a fabricated receipt

Construct, in scratch, at least twice as cheap as the honest path:

1. Gate edit: wrap each `run_leg` call with
   `t0 = time.monotonic()` / `elapsed_ms = int((time.monotonic()-t0)*1000)`
   and print it (this is honest work, but it is ~8 lines; the selftest
   addition required by shared contract 3 is the bulk of the edit).
2. Panel: copy the r99 panel byte-wise except for `timeout_s`. Set it to
   1_000_000.
3. Timing receipt: type 28 plausible rows (e.g. 26 rows of `elapsed_ms=1000`,
   `r92_gate_defects elapsed_ms=620000`, `r97c1_filetype elapsed_ms=640000`).

Run the round's own counter over these bytes under fleet load: the two slow
legs run under a ~16,000-minute cap, they complete, `mismatches=0`,
`max_elapsed_ms=640000 > 600000`, `1_000_000*1000 >= 2*640000`,
`control_600s_would_mismatch=2 >= 1`, `timing_legs_timed=28`,
`gate_elapsed_emitted=1`, `selftest_failed=0` -- **TARGET_MET**, with the
receipt's numbers having been produced by nobody's measurement of those
legs. (This seat did not execute this construction against a landed r100
counter because the counter and panel do not exist yet -- `controls/` and
`receipts/` for round 100 are empty at base, and the r100 counters are
untracked drafts; the conjunction above is read off the frozen predicate
text, not off a run. The L1 need not reproduce it: the point is that no
conjunct distinguishes this byte set from the honest one.)

The part of the honest path that the predicate *does* enforce is exactly:
the gate prints a field, 28 legs run and match, and a 28-row file exists
whose maximum is above 600 s and below half the panel cap. Every other word
in the frozen sentence (measured, on this host, at committed bytes, twice,
timed) is outside the predicate.

---

## 3. Axes -- does either claim move the axis it names?

### 3.1 C1 (coverage): the precise surface

Precise surface moved: **frozen-case reachability of
`g_find_program_for_path`'s PATH-unset arm (`path == None`, i.e.
`gutils.c:370-382`) through the load gate (R1 `Exec` and R1b `TryExec`, each
resolved with `Path=` as working directory) for non-absolute program names,
with the process cwd equal to the case root** (measured by the L1 this round:
the load gate runs at load time, so `gio launch` resolves `Exec`/`TryExec`
with cwd = case root; the round-99 oracle always launches with `cwd = root`,
`launchenv-probe-r99.py:376`, `env = {LC_ALL, HOME, PROBE_OUT}` plus PATH
only when the case's `path` is non-null -- verified this seat).

The axis question, against the "coverage must name the surface it moves"
rule: the before-state model surface was already held as a capability.
`tools/mado-launchenv.py` (`DEFAULT_SEARCH_PATH`, `find_program` port, 90
selftest checks green at base bytes `a63c20c8...`) and `tools/mado-mime.py`
(`find_program` at :466, identical default) already answer the unset arm.
What was unheld is **oracle-labelled frozen-case reachability** of that arm.
That is a real surface -- 0 labelled cases on a branch the oracle can reach --
and it is what the sentence's "exercised by zero **frozen** cases" names. It
is *not* model coverage (which this round does not move; the candidate's
bytes are unchanged at base: `git show 43309e6a:tools/mado-launchenv.py |
sha256sum` = `a63c20c886a2...` = the worktree blob, re-measured this seat), and
it is *not* uniform launch-path coverage: it covers only the load gate, only
for bare names, only with cwd = case root. A case with `Terminal=true` and a
bare `Exec` does not exercise the load gate's unset arm in that same way
(the terminal walk and R3 each call `g_find_program_for_path` on their own
terms), so the surface is narrower than "the PATH-unset default search path"
as a headline.

Command that would show the surface unmoved (for the L1, run at the
measured revision before filing):

```sh
python3 - <<'PY'
import json
d = json.load(open('.ufo/waves/round-100/controls/launchenv-cases-r100.json'))
bare = [c for c in d['cases']
        if c.get('class') == 'path-default' and c.get('path') is None
        and '/' not in c.get('desktop', {}).get('Exec', '')
        and '/' not in c.get('desktop', {}).get('TryExec', '')]
print('branch-reaching path-default cases:', len(bare), '/', len(d['cases']))
PY
```

If this prints 0 (or < 6), the predicate can still be green whenever a
single discriminating case exists (see F1) while the named surface -- six
cases of the default path, each reaching it -- is unmoved and still scored as
moved. The filed sentence and the plan's surface sentence must therefore
name the discriminating-case threshold, not the label count, or carry the
command above as a census conjunct (`branch_reaching_default_cases >= 6`).

### 3.2 C2 (operability): is the cap change operability work or bookkeeping?

The gate change (printing `elapsed_ms`) is operability work in one narrow
sense: before it, **no instrument in custody could state the largest leg
elapsed**, so no cap could be set rationally (`run_leg` discards timing;
`LEG` line carries no time; the r99 panel's `timeout_s: 600` was chosen at
`e39cd5e0`, below the loaded worst leg). After it, the cap is a reported
function of a measurement. That is the M99-4 repair the round-99 lesson
routed, and the seat does not dispute it.

But the *predicate's* operability content is bookkeeping on three counts:

1. **It measures the knob, not the operation.** The panel's legs still take
   as long as they take under load (the two slow legs still exceed 600 s --
   the predicate *requires* `max_elapsed_ms > 600000`). Nothing in the round
   reduces leg wall time, adds parallelism, bounds the panel's total time,
   or detects load that has changed since the timing sample. `panel_timeout_s
   >= 2*max` says "the budget is generous relative to one sample," which is
   the definition of a less-strict instrument, not a more operable one. A
   panel that ran its legs in parallel, or a gate that retried one leg,
   would be operability work; doubling the deadline is an emissions change.
2. **The measured value is load-indexed and the predicate treats one sample
   as the envelope.** Load average on the host is ~250 on 32 cores and varies
   continuously; a 2x multiple of a single sample is not a stable operating
   point, and the predicate has no re-measurement leg and no upper bound
   (see ?2.2). The command that would show the surface unmoved: re-run the
   full panel at the measured revision under current load; if any leg
   exceeds the new cap, `mismatches >= 1` and the *same* defect reopens
   with a bigger number. The round has replaced "600 s, no measurement" with
   "2x one sample, no stability," and the predicate cannot tell the two
   regimes apart beyond the first sample.
3. **The cap is a function of a self-produced file.** The timing receipt is
   authored by the wave; the panel is authored by the wave; the counter is
   authored by the wave. There is no external timing oracle (unlike C1's
   `/usr/bin/gio`, whose digest is pinned independently of the wave). The
   operability surface "the cross-round harm watch's per-leg cap and its
   timing evidence" (plans/round-100.md:23) is therefore moved only in the
   bookkeeping half: the evidence is now *labelled with a method*, not
   *corroborated by an independent instrument*.

Smallest honest reframing for the filed sentence: "a printed per-leg elapsed
field (the gate edit) plus a re-frozen cap at twice the largest elapsed value
in the wave's timing receipt (bookkeeping); no leg's wall time changes."

---

## 4. No-work controls

### 4.1 C1: the cheapest change that skips the claimed work

**Cheapest change: change nothing in `tools/mado-launchenv.py`, and add six
labels to a case file, of which one is bare-Exec/unset and five are absolute
clones (F1).** The claimed work is usually read as "model the default path";
the modelling is already done (base blob `a63c20c8...`, selftest `90/90` at
base bytes, re-measured this seat). The predicate contains **no conjunct
requiring the candidate's bytes to differ from base** (no
`tool_sha256 != base tool sha256`, no separability leg of the r99 shape --
the r99 counter carried `SETUP_ERROR ... absent at base`; the r100 predicate
carries no such clause because the tool exists at base). A candidate equal
to base, scored over an honestly labelled discriminating set, is
`cases_correct == cases_total` -- the exact outcome the frozen sentence
announces ("answers every case ... in agreement") -- with the tool-side work
product of the round being zero bytes.

Scored: this seat scored the misreading half of the control directly. A
one-line mutation of the base candidate

```
DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'   ->   DEFAULT_SEARCH_PATH = ''
```

(read: treat unset as empty) reads, at the case root:

```
real  find_program('sh', None, None) -> '/bin/sh'
cheat find_program('sh', None, None) -> None        (never reaches /bin)
real  find_program('sh', '', None)   -> None
cheat find_program('sh', '', None)   -> None        (identical)
```

i.e. the misreading model agrees with the honest one on the entire round-99
file. Measured: the r99 file has **0** cases whose behaviour depends on the
default (0 bare + unset), so a candidate that model-folds unset into empty
scores the same `cases_correct` on the base set as the honest candidate,
while scoring 0 bare-unset discriminations on any honest r100 set. The
frozen predicate's `control_unset_as_empty_correct < cases_total` catches
this **only** when the r100 set contains labels the misreading cannot
reproduce; it is indifferent to whether the *candidate* models the branch
or merely happens to share bytes with the r99 tool that does. The control
therefore proves the **case file** discriminates, not that the **candidate**
was repaired -- which is correct for a coverage claim, provided the filed
sentence says so. It currently says (in the plan's surface sentence) that
the branch is the thing moved. The no-work candidate (base bytes, one good
case, five clones) is indistinguishable, by the predicate, from the honest
six-case class, and that indistinguishability -- not the tool's correctness
-- is the defect.

*Note on the L1's ground this round* (load-gate cwd = case root): the oracle
launches with `cwd = root` (verified: `launchenv-probe-r99.py:376`,
`subprocess.Popen(argv, cwd=root, env=env)`, with `env` containing `PATH`
iff `path_string(case)` is non-null -- i.e. `path: null` really yields an
unset PATH in the child). A bare program at the case root is therefore
findable under the default's trailing `.`, and the L1's measured
`launches=1 argv[0]={root}/./probe` is consistent with the oracle's shape.
This seat did not re-run a gio launch (kept to PATH-clean oracle runs only
in scratch design; the r99 oracle's contract is sound as read). The ground
supports the discriminating case's design (separation 3), but it does not
repair F1: it makes *one* discriminating case cheap to build, not six.

### 4.2 C2: the cheapest change that skips the claimed work

**Cheapest change: one printed field + two authored numbers + one panel edit
(?2.4).** The gate edit is unavoidable (`gate_elapsed_emitted == 1` requires
the field on both the human line and `--json`), but it is a printer: a gate
that computes `elapsed_ms` from a real timer *without changing census,
timeout, or leg semantics* satisfies every gate-side conjunct. The timing
evidence (`timing_legs_timed`, `max_elapsed_ms`,
`control_600s_would_mismatch`) and the cap (`panel_timeout_s`) are then
authored files. A candidate whose cap is set to an unmeasured million and
whose receipt lists 28 invented rows scores TARGET_MET while no leg was ever
timed by anybody. The round's claimed work, "the per-leg cap becomes
measured," is a sentence the predicate cannot distinguish from "the per-leg
cap is declared," because `panel_timeout_s * 1000 >= 2 * max_elapsed_ms`
compares two wave-authored numbers against each other and against nothing
else.

Scored: this seat could not execute this control against a landed r100
counter, because the r100 counter, panel, and timing receipt do not exist in
custody yet (`ls` of the round-100 `controls/` and `receipts/` directories
returns empty at base; only the round-99 counterparts exist). The control is
therefore scored by **reading the frozen predicate**, which is sufficient:
every conjunct that mentions timing reads a pinned file or the gate's own
output, and none re-derives one elapsed value independently. If the landed
counter turns out to re-derive `max_elapsed_ms` from its own panel run and
require equality with the receipt, this falsification ?2.4/?4.2 fails on the
equality leg -- and the seat invites the L1 to land that check, since it is
the smallest safe correction (?7).

---

## 5. The harm-watch framing -- self-certification path

The seat was asked: the C2 counter runs the round's own panel -- is there a
self-certification path where the round's instrument is the thing being
measured? Answer: **the path is the predicate; the round-100 C2 predicate is
the round's own panel, timed by the round's own gate, read by the round's
own counter, with every conjunct that could break the circle replaced by a
95%+ self-reference.**

The circle, link by link:

1. **Candidate = instrument.** `quality/harm-watch.py` is both the artifact
   under repair (the claimed work product) and the measuring instrument for
   its own claim (it produces `elapsed_ms`, it enforces `timeout_s`, its
   output `mismatches` is the predicate's verdict). The gate controls the
   legs it times: it spawns them, captures their output, decides `ok`, and
   prints the time. A gate that prints an `elapsed_ms` field and reports
   every leg `ok` is *gate-green* by its own word. In round 99 this was
   guarded: `PRED-C2-r99-v1` required five planted panels each caught with
   their own finding id, a marker-blind gate copy rejected, and an always-OK
   stub flagged -- i.e. the predicate *did not trust the gate's verdict about
   itself*. The round-100 predicate carries **none** of these: no planted
   legs, no stub, no marker-blind conjunct. The round's former
   anti-self-cert legs have been dropped at the exact round the gate becomes
   its own evidence. The declaration's harm-watch note ("the round-99
   counter still runs against 3b69f041 and its pinned bytes are untouched",
   declaration:106-107) guards *cross-round* compat of the old gate; it does
   not re-arm the new counter's discrimination.
2. **The control is derived from the measured thing.** `control_600s_would_mismatch`
   counts rows of the same timing receipt whose value feeds `max_elapsed_ms`.
   A receipt that is self-consistent greens both the measurement and its
   control simultaneously. (Round-99 C2's controls were *different panels*
   run through the *same gate*: the control and the candidate leg were
   distinct executions. Here the control is an arithmetic on the candidate's
   own output.)
3. **The cap is validated against the measurement of the thing the cap
   protects, taken by the thing the cap protects.** `panel_timeout_s` is
   checked against `max_elapsed_ms` from a timing run *executed by the gate
   under repair* (the measurement method is unspecified in the predicate
   beyond "timing receipt ... all 28 legs timed").
4. **The selftest is the gate grading itself.** `selftest_failed == 0`
   runs `quality/harm-watch.py --selftest`, the gate's own fixture suite.
   Shared contract 3 requires selftest checks for `elapsed_ms` (present,
   non-negative, integer, monotone across a fixture whose second leg is
   slower). Those checks are written by the same author as the printing
   code, in the same file, and a gate that prints a well-formed field from
   an honest timer passes them without its *panel* timings ever being
   checked against anything. A gate that times fixture legs honestly and
   would print `elapsed_ms=99999999` for any leg over 60 s (saturating, not
   measuring) passes present/non-negative/integer and -- if the fixture's
   slow leg is slower than the fast leg -- monotone. The selftest therefore
   certifies the *format* of the field, not the *fidelity* of any number
   the panel run prints.
5. **The panel is authored by the round that is measured by it.** Only
   `panel_legs == 28` binds the panel to anything (a census count). The
   legs that fail on this host (`r92_gate_defects`, `r97c1_filetype`) need
   not appear *as those legs* -- only something with those ids that finishes
   under the new cap. The round-99 counter's planted dropped-leg / wrong-
   expect / extra-leg panels are the round-99 answer to exactly this; the
   round-100 counting command does not name `--planted-dir`, and the
   predicate names no planted conjunct.

Named, with locus and locus field (the seat's attacker-side answer to the
framing question):

- **Self-cert path A (gate prints its own verdict):** predicate omits all
  planted/stub/marker-blind conjuncts present in `PRED-C2-r99-v1`; the gate's
  `ok`/`mismatch` lines are taken at face value by the counter.
- **Self-cert path B (control derived from the same receipt):**
  `control_600s_would_mismatch` is an arithmetic consequence of
  `max_elapsed_ms`'s source; no 600 s run is executed by the counting
  command.
- **Self-cert path C (cap validated against self-timed sample):**
  `panel_timeout_s * 1000 >= 2 * max_elapsed_ms` relates two wave-authored
  numbers; no independent timer survives in any conjunct (contrast C1, where
  `/usr/bin/gio`'s digest is pinned independently of the wave -- the
  asymmetry the round should repair in C2 if it wants the same grade).

Impacted axes: the entire C2 axis is implicated. If any of A-C is kept, the
C2 TARGET_MET line certifies that the round's instrument agrees with itself
on the round's panel, which the "operability" rubric (instrument quality)
does not count: the round-99 C2 was graded "unchanged (operability)" for a
*miss*, precisely because the instrument's discrimination was green while
the target was not reached. A round-100 green achieved by paths A-C would be
an operability gain the rubric cannot see but the predicate cannot
distinguish from instrument self-agreement.

---

## 6. Sentences whose words nothing in this round's custody can reject

Each entry names the claim sentence (or clause), says why *no* round-100
instrument can falsify it (the counter, the panel, the receipts, and the
registry carry no reading that would make it false), and classifies the
defect. These are sentences the L1 must either delete, move to a receipt
with a producer field, or leave standing with the criterion-172 narrowing
recorded.

### C1

1. **"every label measured against the installed /usr/bin/gio (sha256
   d2164260...cfc462, glib2 2.90.1-1) and re-measured twice with agreeing
   results"** (declaration:18-20). *Nothing rejects it.* The counter reads
   frozen `expect` bytes and compares the candidate to them; the gio digest
   is an envelope pin inside the file the wave itself freezes. No conjunct,
   receipt field, or committed measurement binds those bytes to a measurement
   event, and "twice" is a count of a process, not a property of any
   committed artifact. Class: **provenance sentence without a producer**
   (M99-1 class; criterion 24 requires the receipt to name its producer --
   this predicate has no producer conjunct and no receipt field for one).
2. **"The class must separate the unset default from all three neighbouring
   behaviours, or the branch is not cored"** (declaration:23-24). *Nothing
   rejects it.* The three separations are prose; `default_classes >= 3`
   counts label strings; `control_unset_as_empty_correct < cases_total`
   thresholds at one discriminating case. No instrument in custody compares
   two fixture geometries, so no instrument can ever say "this class does
   not separate." Class: **gate-checkable adjective outside the gate**
   (criterion 160 class; the predicate reads the population from the data).
3. **"including a seeded fresh leg"** as a property of the default class
   (declaration:21). *Nothing in the predicate rejects a fresh set with
   zero default cases.* `fresh_total >= 8` and `fresh_correct ==
   fresh_total` are the only fresh conjuncts; the generator's class
   composition is unconstrained, and the counter lands in this round without
   a stratification requirement in the predicate text. Class: **unstratified
   population** (the counter as frozen in its command line cannot know it
   must stratify; only the prose could, and prose is not read by the
   counter).
4. **"a counted mutant population"** as a guard on the named branch
   (declaration:21-22, in the clause following "answers every case of that
   set"). *Nothing rejects a mutant set anchored elsewhere in the tool.*
   No conjunct requires a find/replace anchor on the default-search-path
   line or the unset arm. Class: **unanchored population** (a mutant
   population that any member of which may sit on any line guards the tool
   globally, not the branch the claim names).
5. **"or the branch is not cored"** / the plan's "the surface it moves: the
   PATH-unset default branch of the launch load gate" (plans/round-100.md:15).
   *Nothing rejects the headline.* The predicate measures one narrow
   fixture-aid (bare name + unset PATH + cwd = case root at R1/R1b) and the
   headline names the whole branch; no conjunct maps headline to fixtures,
   so both the narrow truth and the wide reading satisfy every instrument.
   Class: **headline overreach** (sentence wider than instrument, M99-3).

### C2

6. **"the largest per-leg elapsed measured on this host at committed bytes"**
   (declaration:75-77). *Nothing rejects it.* The counter reads a 28-row
   receipt's maximum; no conjunct binds that receipt to a host identity, a
   revision, a producer digest, or a producer command. An off-host or
   uncommitted measurement is indistinguishable from an on-host,
   committed-bytes one under every pinned check. Class: **unbound
   measurement** (criterion 24's producer binding, absent).
7. **"all 28 legs timed"** (declaration:77, predicate: `timing_legs_timed ==
   28`). *Nothing rejects a receipt whose 28 rows were typed.* The
   counter's own panel run observes 28 elapsed values (post-edit), but no
   conjunct requires the receipt to equal, bound, or be consistent with
   them. Class: **row count read as a timing claim** (same shape as the
   criterion-160 defect: the population is the data).
8. **"the frozen 600 s cap is structurally too small on this host: the
   control is measured, not asserted"** (declaration:86-88). *Nothing
   rejects the host half.* The control is `control_600s_would_mismatch >=
   1`, derived from the same receipt; no leg is run at the 600 s cap by the
   counting command, and no base-revision panel run under `timeout_s: 600`
   is a conjunct. "Structurally" (as opposed to load-contingently) too
   small is a generalisation from one loaded sample that no instrument
   restates. Class: **derived control passed off as measured control**.
9. **"a full-panel run at committed bytes"** (declaration:77-78). *Nothing
   rejects a worktree run.* The counting command substitutes `--rev
   <MEASURED_REV>`; the predicate carries no committedness conjunct, and the
   round-99 shape ("`--rev worktree` for an uncommitted candidate") is
   inherited by the C1 command and, by shape, by the C2 counter even though
   its command text omits the note. Class: **unbound revision**.
10. **"the frozen 28-leg harm panel"** (definite, declaration:68,75) and
    **shared contract 3's** "the 28 leg rows, their `expect_rc`,
    `expect_marker` and `note` stay byte-identical to the round-99 panel"
    (declaration:139-140). *Nothing in the predicate rejects a panel whose
    legs are rewritten under the same ids.* `panel_legs == 28` is a count;
    census rule (28 declared ids, marker occurring in output) is the only
    leg-identity substitute, and it is satisfied by legs that always pass.
    Class: **count read as identity** (the same class as entry 7, applied to
    the panel itself).

Sentences the seat checked and **does** clear as falsifiable/true (not
narrowed): C1's before-state ("both `path-unset` cases carry an absolute
`Exec`" -- true, re-measured above; "exercised by zero frozen cases" --
true in the frozen-case sense, subject to narrowing 7 in ?1.5 about the
selftest/mime surfaces); C2's before-state (no timing at base, 600 s cap,
`mismatches=2`, re-measured above); C2's "28 legs" census shape at base.

---

## 7. Smallest safe corrections (summary for the L1)

The L1 must record each item it adopts in `plans/round-100.md` **before
filing** (addendum ?8, criterion 172, citing this artifact) or file the
narrowed sentences in ?1.5/?2.3. No action here widens any frozen sentence;
every item either narrows the filed wording or adds a conjunct that the
wave must then satisfy.

**C1 (add conjuncts, or file the narrowed sentence):**

- `branch_reaching_default_cases >= 6`, where a case counts only if
  (`path` is null) AND (`Exec` argv[0] or `TryExec` is non-absolute with no
  `/`-rooted first token) -- a geometry check, not a label count. This is the
  single conjunct that closes F1 without touching the frozen counts.
- One named class (and per-class minimum 1) per separation, or a
  `separations_witnessed == 3` census of paired fixtures (identical except
  PATH / cwd) -- closes F2 and the "not cored" sentence.
- Fresh stratification: `fresh_default_cases >= 1` (or drop "including a
  seeded fresh leg" from the default-branch claim).
- Mutant anchor: `>= 1` mutant anchored on the `DEFAULT_SEARCH_PATH` /
  `path is None` lines (or drop the branch-guard implication).
- Narrowings 1, 2, 6, 7 of ?1.5 (provenance, oracle-agreement, base-control
  gloss, frozen-case surface).

**C2 (add conjuncts, or file the narrowed sentence):**

- Leg identity: `panel_legs_match_r99 == 28` (id, round, argv, expect_rc,
  expect_marker byte-identical except `timeout_s`) -- closes ?6 entry 10
  without freezing a new panel pin that was never verified against r99.
- Timing derivation: the counter measures the maximum itself during its own
  panel run and requires the receipt's maximum to be within a stated
  tolerance of it (or replaces `max_elapsed_ms` with the counter's own
  measure and keeps the receipt as the provenance record) -- closes ?6
  entries 6-7 and paths B-C of ?5.
- A control that is a run: `control_600s_run_observed_mismatch >= 1` (run the
  panel at `timeout_s: 600` under the counting command and observe >= 1
  `rc=124`) -- closes entry 8.
- Anti-self-cert legs restored from `PRED-C2-r99-v1`: at least one planted
  leg whose expectation the gate must flag (e.g. a dropped leg must read
  `PANEL_LEG_MISSING`) -- closes path A of ?5 at the smallest strength.
- Narrowings 1-6 of ?2.3 (printed-not-measured elapsed, unbound receipt,
  derived control, worktree rev, panel identity).

**What must not change:** the frozen predicate text (it is frozen before
scoring, and this seat does not ask the L1 to move a target after the data);
the C1 before-state sentence (true as written); the C2 before-state
sentence (true as written); the prohibition on widening any sentence in
either claim during filing.

---

## Evidence index (commands this seat ran, base revision)

- `git show 43309e6a:tools/mado-launchenv.py | sha256sum` -> `a63c20c8...`
  (base blob; identical to worktree -- candidate unchanged, ?3.1).
- `git show 43309e6a:.ufo/waves/round-99/controls/launchenv-cases-r99.json`
  -> envelope + cases; materialised to a scratch file and counted:
  67 cases, 31 classes, exactly 2 `path: null`, both with
  `Exec "{root}/probe.sh"` (absolute), 0 with a bare `Exec` + unset PATH (?1, F3).
- `git show 43309e6a:tools/mado-mime.py | grep -n 'def find_program'` ->
  `466:...`; body reads the identical unset default (S1.4/F4; pointer per
  erratum 172a).
- `python3 -I tools/mado-launchenv.py --selftest` (base bytes) ->
  `MADO_LAUNCHENV_SELFTEST: checks=90 failed=0` (S1.4/F4).
- Scratch mutant `DEFAULT_SEARCH_PATH = ''` (scratch copy only, never the
  tool): `find_program('sh', None, None)` -> `None` vs base `'/bin/sh'`;
  `find_program('sh', '', None)` -> `None` under both (?4.1).
- `git show 43309e6a:.ufo/waves/round-99/controls/harm-panel-r99.json` ->
  `expect_legs 28`, `timeout_s 600`, rounds `base,r90,r92,r93,r94,r95,r96,r97`
  (?2, ?3.2).
- `git show 43309e6a:.ufo/waves/round-99/receipts/c2-measured-r99.txt` ->
  `TARGET_MISSED ... panel_legs=28 declared_legs=28 legs_run=28 mismatches=2`
  (S2.2).
- `quality/harm-watch.py` at base (read in full): `run_leg` returns
  `{id, rc, out, err, detail, legdir}`; human line
  `LEG %s rc=%s expect=%s marker=%s %s`; no timer anywhere; `leg_timeout`
  reads `panel["timeout_s"]` (default 3600) (S2.2).
- `.ufo/waves/round-99/controls/launchenv-probe-r99.py` (read):
  `env = {LC_ALL, HOME, PROBE_OUT}` + `PATH` iff the case's path is non-null;
  `subprocess.Popen(argv, cwd=root, env=env)` (S3.1, ground note).
- `quality/counters/c2-r99-harm-watch.py` (read in part): PRED-C2-r99-v1's
  planted/stub/marker-blind conjuncts; `run_gate` parses `HARM_WATCH:`
  summary and the trailing JSON line (S5, path A).
- `ls` of `.ufo/waves/round-100/controls/` and `/receipts/` -> empty at base;
  `quality/counters/` carries only the r99 counters (S4.2 scoping).
- `.ufo/waves/round-100/claims.json` vs declaration vs tool source:
  `gutils.c:376-389` vs `gutils.c:370-382` vs `gutils.c:409-421` for the same
  literal (S1.4, locator note).

Scratch: `/fast/scratch/hyaku/mado-r100/R100MCriticClaims/` (this seat's
entire scratch tree, including the one-line `DEFAULT_SEARCH_PATH` mutant,
removed with the seat's own `rm -rf` -- this report is the only surviving
artifact of the seat).

Tool installs/upgrades: none (no files installed; read-only inspection plus
one in-scratch source-text substitution on a copied file).
