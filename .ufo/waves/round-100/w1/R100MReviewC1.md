# R100MReviewC1 -- adversarial review of C1 (declaration section C1)

Seat: R100MReviewC1 (reviewer). Round mado 100 (hyaku run 15, attempt 1),
wave w1. Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. Base
revision 43309e6a (branch master, HEAD at review time = base, worktree
dirty only in corpus/QUALITY.md and corpus/lessons/round-99.md errata for
172a; tools/mado-launchenv.py and quality/ identical to base).
Contract read first: .ufo/waves/round-100/claims-declaration-r100.md
(predicate sentences frozen before any case scored).
Also read: corpus/lessons/round-99.md, corpus/lessons/round-99-verifier-
spotcheck.md (routed defects 1-5; C1 A8 residual is addressed here),
corpus/QUALITY.md (round-90..99 sections, criteria 160-172a),
SKILL.md (registry), quality/harm-watch.py, tools/mado-launchenv.py,
quality/counters/c1-r99-launchenv.py,
.ufo/waves/round-99/controls/launchenv-cases-r99.json,
.ufo/waves/round-99/controls/launchenv-probe-r99.py,
.ufo/waves/round-99/controls/launchenv-fresh-r99.py,
.ufo/waves/round-99/controls/launchenv-mutants-r99.json,
.ufo/waves/round-99/fetch/gutils.c, plans/round-100.md (amendments still
empty at review time), .ufo/waves/round-100/w1/R100MCriticClaims.md
(peer critic, landed during this review), .ufo/waves/round-100/w1/
R100MLabratUnset.md + receipts/labrat-unset-r100.txt (peer labrat,
landed during this review).

Scope of this seat: section C1 only (coverage of the PATH-unset default).
Every factual claim about current committed bytes was re-measured this
seat (command outputs pasted in Sec. 9); peer artifacts landed mid-review
are cited by path and their measurements were checked, not re-run, except
where stated. No candidate code was written; scratch fixtures used the
committed r99 oracle module by import and the committed candidate by
path (instruments, not candidates).

Axes (Godspeed step 1): C1 moves one surface -- frozen-case reachability
of g_find_program_for_path's PATH-unset arm (path==NULL -> PATH ->
/bin:/usr/bin:., gutils.c:370-389) through the load gate. This seat moves
the frontier only by attacking; it improves no axis itself. Axes harmed:
none (read-only; scratch deleted before yield).

## Standing verdicts (one per frozen claim, per the seat spec)

- C1 sentence wide than its conjunct set (defect class M99-3, last five
  autopsies): **falsifies-wording**. Two findings in Sec. 1: (1a) the
  three prose separations (declaration:26-34, "the class must separate
  ... or the branch is not cored") appear in **zero** conjuncts and one
  of them (separation 3) is factually false for every fixture shape the
  schema can express (Sec. 1a); (1b) the before-state locators name three
  different line ranges for the same literal, one of them not containing
  it (Sec. 8).
- C1 number bag (`default_cases >= 6`, `default_classes >= 3`,
  `cases_correct == cases_total`, `fresh_total >= 8`,
  `mutants_counted >= 4`): **falsifies-number** (weakly). The numbers do
  not bound the property they are presented as measuring: (2) a 6-case
  set with 5 never-reaching clones satisfies every numeric conjunct
  (Sec. 2, constructed counterexample, peer critic F1 independently);
  (3) `base_set_default_cases == 0` counts a label the r99 vocabulary
  does not contain, so the control is 0 by construction (Sec. 4);
  (4) no conjunct binds a separation to a named neighbour: the only
  separation-sensitive conjunct is a one-case threshold, and a wrong
  model (dot-first, and swap-bin on this symlink host) survives every
  fixture this seat measured (Sec. 5.2).
- Residual conjunction (measurability): **neutral**, conditionally.
  Verdicts (d) and the measurable half of (a) cannot pass or fail until
  the r100 counter, case file, fresh generator and mutant file exist;
  at review time none do (Sec. 6). What can be settled now is stated as
  neutral-with-gaps and the gaps are pinned to exact future artifacts.

Each finding below names the artifact path under
.ufo/waves/round-100/ that carries the counterexample, per the spec.
The round-100 paths that existed when this review opened were
claims-declaration-r100.md, claims.json, plans/round-100.md and the
wave dir; the C1 artifacts it attacks do not exist yet (Sec. 6); the
counterexample *fixtures* this seat built lived in scratch (deleted) and
are carried in full as pasted oracle/candidate outputs in Sec. 9, with
their reproducing recipes, so the L1 can re-run them after integrating
the executor seats' case files.

## 1. (a) The conjunct set does not enforce the stated sentence

### 1a. The three separations are prose, not conjuncts -- and the "(3)" sentence is false

Declaration C1 (lines 23-34) requires the class to "separate the unset
default from all three neighbouring behaviours, or the branch is not
cored", then enumerates (1) unset != empty, (2) unset != case-private
PATH, (3) the trailing `.` is real. PRED-C1-r100-v1 (lines 39-47) has
seven conjuncts; none of the three separations is one of them, and the
only separation-adjacent conjunct is
`control_unset_as_empty_correct < cases_total`, a **one-case** threshold.
This is the exact shape of M99-3 (lesson round-99.md:54-74, QUALITY
criterion 172): a sentence a reader re-derives differently from the
instrument. The peer critic (w1/R100MCriticClaims.md Sec. 1.2-1.3) reached
the same conclusion by reading; it is confirmed here by construction
(Sec. 2) and by measurement (Sec. 5).

Moreover separation (3) as written is **not merely unenforced, it is
false** for every fixture expressible in the frozen schema. The
sentence: "A bare program present only in the launch working directory
is found with PATH unset, and is not found by the same fixture under
PATH="" when the working directory differs from the process cwd."
The launch working directory is the process cwd (= case root; oracle
measure_once runs Popen(cwd=root), probe:376; the schema's launch_cwd
field is validated by the r99 counter (counter:455-460) but **ignored**
by the oracle, which has no launch_cwd handling -- grep
.launch_cwd in the probe returns nothing). "Working directory" in the
second clause is Path=. With Path={root}/work set, a bare Exec/TryExec
name is first tested as working_dir+program (gutils.c:322-327) and,
if that fails, the PATH walk re-joins each candidate to working_dir
(gutils.c:479-482, tool find_program:218-219). I measured six shapes
through the committed oracle (scratch, deleted; recipes and outputs in
Sec. 9, "sep3"):

- Path={root}/work, work/probe present, Exec=probe, **PATH=""**:
  launches=1 argv=[{root}/work/probe] -- FOUND. The sentence predicts
  not-found.
- Same fixture, **PATH unset**: launches=1 argv=[{root}/work/probe] --
  identical. No separation at all.
- Probe only at root (not in work), Path={root}/work, **PATH=""**:
  error=load; **PATH unset**: error=load -- identical miss under both.
- TryExec=helper in work/, Path={root}/work, **PATH=""** and **unset**:
  both launch (argv=[{probe}]).

So with an ABSOLUTE Path= the two PATH states agree in every fixture;
with Path unset there is no "working directory differs" to write.

One relative-Path= shape does separate, and it is the correct rewrite
of (3) (measured; oracle and committed candidate agree, outputs in
Sec. 9.12): Path=work (relative), work/probe present, Exec=probe.
- PATH unset -> launches=1 argv=[{root}/work/./probe]
- PATH=""     -> launches=1 argv=[{root}/work/probe]
The program is found in BOTH states; what differs is the argv0, because
the unset walk's '.' entry appends `./` inside the relative working
directory (gutils.c:478-482 re-join) while the empty entry walks the
bare name. So separation (3)'s "is not found by the same fixture under
PATH="" is false in every expressible geometry; its true content is
"the trailing '.' is visible as an extra './' in argv0 when Path= is
relative", a lexical separation exactly like (1)'s success arm. The
reachable neighbours the class can actually separate are the shapes in
Sec. 5 (rootprog './probe' vs 'probe', private-bin miss vs set-PATH hit,
TryExec-in-/usr/bin vs empty). A counter conjunct that pins one named fixture
per separation (peer critic narrowings 3) would still fail as written
against (3); the sentence must be rewritten, not merely conjuncted.

Counterexample artifact path:
.ufo/waves/round-100/claims-declaration-r100.md (lines 32-34 + 39-47).

### 1b. "Every label measured ... twice with agreeing results" has no conjunct

The frozen sentence (declaration:18-19) promises oracle measurement
against /usr/bin/gio (sha pinned) *and* double measurement with
agreement. The predicate's only file-side conjuncts are counts over
the pinned case file. Agreement-with-file is enforced (cases_correct);
agreement-with-oracle is not observed by the counter at all (the r99
counter, whose contract the r100 counter inherits per declaration
Shared contract 2, never opens /usr/bin/gio; the sha is an envelope
pin -- counter check: envelope-gio). The r99 oracle does measure twice
(measure_case, runs=2, agreed flag, probe:427-440) and the labrat
re-ran 7 cases through it with agreed=True (receipt
labrat-unset-r100.txt:12-15), so the *practice* is real; but the
*predicate* cannot distinguish an oracle-measured file from a
hand-typed one that agrees with the candidate (M99-1 class: a claim
about bytes no checker re-derives). Filed sentence must carry the
measurement lineage by receipt, not by the predicate (peer critic
narrowing 1, agreed).

Counterexample artifact path:
.ufo/waves/round-100/claims-declaration-r100.md (lines 18-19 vs 39-47).

## 2. (a)/(b) Number bag: a 6-case class that never reaches the branch passes

The strongest C1 counterexample (peer critic F1, independently verified
here against committed bytes) was re-checked against the r99 file:

- r99 file: 67 cases, 31 classes; exactly 2 with path==null
  (pu-abs-work, pu-abs-root), both Exec="{root}/probe.sh" (absolute),
  no TryExec, Terminal unset. Sec. 9 output proves no other case can
  reach the default through another door (every other case has path
  set; the only other bare-Exec cases carry a list PATH).
- Clone pu-abs-root six times under three labels path-default-x/y/z
  (absolute Exec, path:null -- they return at gutils.c:332-357 before
  the PATH source is read at :370-371) and add ONE
  genuine discriminating case (Exec=sh bare, path:null -> oracle
  resolves /bin/sh via the default; this seat's own measurement:
  pd-unset-tryexec-true launches under unset, error=load under PATH="")
  so control_unset_as_empty_correct = total-1 < total. Then
  default_cases=6, default_classes=3, cases_correct==cases_total,
  base_set_default_cases==0, control conjunct holds. Fresh (>=8 of any
  class -- r99 fresh generator defaults path to ["{root}/bin"] and has
  **no** path:null shape at all, fresh:51,63 -- can be 100% prog-abs)
  and mutants (>=4 terminal-table mutants, r99 mutants file shape)
  are equally satisfied. Five of six new cases never read the PATH
  source; the branch-reaching count is 1, not 6, and the axis does not
  move. The predicate cannot reject this set; only the prose (3)
  forbids it. Filed sentence must read as the peer critic drafted:
  "at least one case whose label the empty-default misreading cannot
  reproduce; the remaining default cases are enumerated by label only"
  -- unless each of (1)(2)(3-as-rewritten) gets a pinned per-class
  minimum with a paired-fixture check (PATH differs, geometry identical).

Counterexample artifact path:
.ufo/waves/round-100/claims-declaration-r100.md (lines 17-21 vs 39-47);
corroborated in .ufo/waves/round-100/w1/R100MCriticClaims.md Sec. 1.4/F1.

## 3. (a) default_classes >= 3 counts label strings, not behaviours

`default_classes` is computed from the class key of cases in the
pinned file (r99 shape: classes_ok over distinct class keys). Three
identical geometries under three names satisfy >=3. The declaration
names three separations in prose but does not pin three named classes
with per-class minima (the M94-2 shape; peer critic F2). Until the
counter lands, the conjunct in fact only asserts "the file contains
>=3 distinct strings in its class field among the >=6 default cases".
This is the same defect class as (b)'s label-count shortcut. Finding:
**falsifies-number** for this conjunct standing alone; it survives only
as part of the narrowed sentence in Sec. 2.

Counterexample artifact path:
.ufo/waves/round-100/claims-declaration-r100.md (lines 40-41).

## 4. (c) base_set_default_cases == 0 is 0 by vocabulary construction

Question: is the conjunct true of the round-99 case file, or does some
existing case reach the default through another door?

Measured (this seat, Sec. 9): the r99 file has exactly two path-null
cases and both are absolute-Exec; a full 67-case scan for
PATH-unset + bare lookup (Exec bare, TryExec bare, Terminal=true walk)
finds **zero** doors to the default. The before-state sentence
("exercised by zero frozen cases", declaration:14) is **true** as
written -- verdict on the before-state is **neutral** (no falsification).

But the **conjunct** `base_set_default_cases == 0` as stated counts
something else: cases carrying the r100-invented label `path-default`
in the r99 file. The r99 vocabulary (31 classes, enumerated in Sec. 9)
contains no such label, so the conjunct is 0 for **any** candidate and
**any** r100 set, before any case is scored -- the do-nothing control
measures the failure to apply a label this round invented, not the
failure to exercise a branch (peer critic F3, confirmed). Formally: a
hypothetical r99 file containing a bare-Exec path:null case under the
existing label `prog-bare` would read base_set_default_cases==0 while
the before-state sentence would be false. The sentence's truth was
established by direct inspection of the two pu-* Exec bytes (this
seat and the peer critic), not by the conjunct.

Why this matters beyond wording: the conjunct is **falsifies-number**
as a control -- it cannot fail, so it cannot discriminate. If the L1
keeps it, the filed sentence must gloss it per peer critic narrowing 6
(counts the label; branch-reachability of the r99 file established by
inspection, not by this conjunct). If the L1 wants a real control it
must define base_set_default_cases geometrically (path:null AND
non-absolute load-gate lookup -- Exec argv0, TryExec, or Terminal walk)
and pin that number; the measured value over the r99 file is then 0
for the true reason.

Two further observations this seat adds to the peer critic's F3:

- **Ambient/terminal door (c) extended.** Even with path set, Terminal=
  true cases reach `g_find_program_for_path` through the terminal walk
  (tool _resolve_terminal, gdesktopappinfo.c:2797-2806) using the
  process PATH. In the r99 set all Terminal cases carry path=["{root}/bin"],
  so the walk reads the case dir, not the default. No door found. But the
  same door is a **hazard** for the r100 file: a frozen Terminal=true
  case with path:null would search the default for a known terminal,
  and this host has /usr/bin/xdg-terminal-exec (verified present)
  which would launch a real terminal. The oracle env (no host PATH) does
  **not** protect this: the walk intentionally consults the default
  /usr/bin. Case design must avoid Terminal=true under unset, or the
  executor's measurement will start a host terminal. I did not run a
  Terminal=true+unset oracle case beyond the one accidental hit
  (pd-unset-term: setup-error via winit, Sec. 9) and will not repeat it.
- **The same branch is already modelled twice at base** (peer critic
  F4, verified): tools/mado-mime.py:466 ports find_program with the
  identical `"/bin:/usr/bin:."` default, and the candidate's own selftest
  at base bytes exercises it (`fp-default-path-has-sh`,
  `fp-default-dot-entry-keeps-dot-slash`, MADO_LAUNCHENV_SELFTEST:
  checks=90 failed=0, re-run this seat). The filed sentence is careful
  ("exercised by zero *frozen* cases") and that is true; the headline
  "the PATH-unset default search path of the launch load gate" plus
  "or the branch is not cored" invites the wider reading (indeed the
  branch *was* already modelled and selftest-covered). Per
  criterion 172 the filed surface must be "the PATH-unset default branch
  **as exercised by frozen cases**" (peer critic narrowing 7).

Counterexample artifact path:
.ufo/waves/round-100/claims-declaration-r100.md (line 45 conjunct);
before-state corroboration: .ufo/waves/round-99/controls/launchenv-cases-r99.json.

## 5. (b) Do new cases separate unset / empty / case-private PATH? -- scored wrong models

The r100 case file does not exist yet (controls/ holds only
harm-panel-r100.json); separation must therefore be judged by (i) what
the frozen prose demands, (ii) whether **any** schema-expressible case
set can separate the three neighbours, and (iii) scoring the committed
candidate plus five wrong-model copies against oracle-measured fixtures
this seat built (scratch, deleted; outputs in Sec. 9). The labrat
independently measured the same separation fixtures from the other side
(w1/R100MLabratUnset.md + receipt labrat-unset-r100.txt:7 cases, 7/7
agree) and is consistent with every fixture below.

### 5.1 What separates what (oracle-measured, this seat)

Fixtures (all cwd=root, env LC_ALL/HOME/PROBE_OUT only +/- PATH):

- pd-unset-rootprog: path=null, Exec=probe (probe at root) ->
  launches=1 argv=[{root}/./probe]
- pd-empty-rootprog: path=[""], Exec=probe (probe at root) ->
  launches=1 argv=[{root}/probe]
  => success-region separation exists, **but only in the argv0 string**
  (./probe vs probe); launches/cwd/env identical. A status-only
  expectation calls these identical. Any frozen expect must carry the
  argv vector, not just launches/rc. (Labrat (a): same conclusion.)
- pd-unset-private: path=null, Exec=helper (helper only in
  {root}/bin) -> error=load; pd-set-private: path=["{root}/bin"] ->
  launches=1 argv=[{root}/bin/helper]. => (2) separates cleanly.
- pd-unset-tryexec-true: path=null, Exec={root}/probe.sh,
  TryExec=true -> launches=1 argv=[{probe}]; pd-empty-tryexec-true:
  path=[""] -> error=load. => (1)'s /usr/bin-only arm separates ONLY
  through TryExec (or path-relative tricks below), because a successful
  bare-Exec launch of a host program (true) produces no probe record
  and the oracle grades it setup-error (my pd-unset-usrbin Exec=true:
  error=setup-error, Sec. 9). The case designers must be told this:
  frozen success labels need the case's own probe script, so the (1)
  arm must be fired through the TryExec door, or through a same-name
  collision (./x probe vs host /usr/bin/x -- see Sec. 5.3).
- Separation (3) (Path differs): no separation (Sec. 1a).

### 5.2 Wrong-model scoring (this seat; final run with the oracle's canon order, Sec. 9)

Five mutants of the committed candidate (string replacement of
DEFAULT_SEARCH_PATH), scored against the 7 fixtures with strict argv
comparison (canon order: probe path first, then root -- the oracle's
canon), candidate cwd=root, PATH unset = env without a PATH key:

| mutant | pd-unset-rootprog | pd-empty-rootprog | pd-unset-private | pd-set-private | pd-unset-tryexec-true | pd-empty-tryexec-true | pd-unset-usrbin-pathwd |
|---|---|---|---|---|---|---|---|
| committed (correct) | OK | OK | OK | OK | OK | OK | OK |
| unset-as-empty ('') | KILLED (argv /probe vs /./probe) | survive | survive | survive | KILLED (load) | survive | survive |
| unset-drop-dot ('/bin:/usr/bin') | KILLED (load) | survive | survive | survive | **survive** ('true' is in /bin) | survive | survive |
| unset-dot-first ('.:/bin:/usr/bin') | **survive** | survive | survive | survive | **survive** | survive | survive |
| unset-swap-bin ('/usr/bin:/bin:.') | **survive** | survive | survive | survive | **survive** | survive | survive |
| unset-as-colon (':') | KILLED (argv) | survive | survive | survive | KILLED (load) | survive | survive |

(This table is the corrected run; an earlier pass of mine used the
reverse canon order and reported false KILLED cells for dot-first and
swap-bin on tryexec-true. Output in Sec. 9.11. The committed tool is
7/7 OK under the oracle canon -- the one initial WRONG was my harness.)

Reading, each point measured, not inferred:

- **The trailing `.` is observable only through a root-only program
  case.** unset-drop-dot keeps /bin and /usr/bin, so it survives the
  /usr/bin-only TryExec arm (`true` lives in /bin) and the private-bin
  arm; it dies solely on pd-unset-rootprog (program only at the case
  root, found via '.'). A frozen set without that one shape cannot see
  the (rewritten) separation (3), and a set with only it cannot see (1).
  The predicate's `control_unset_as_empty_correct < cases_total` and
  `mutants_killed == mutants_counted` are satisfied in both
  compositions, so neither conjunct pins which neighbour was separated.
- **unset-dot-first is a wrong model no fixture here kills.** It agrees
  with the correct default on every shape: membership is the same, and
  order is unobservable unless a case creates a same-name collision
  between the case root and a host PATH directory (e.g. a probe script
  named `ls` with Exec=ls: dot-first spawns the case's ./ls and its
  argv0 is {root}/./ls, bin-first spawns the host /usr/bin/ls which
  writes no record -> the oracle grades setup-error). Distinguishing
  '.' from '/usr/bin' order therefore requires a deliberately
  collision-named fixture; none of the 7 shapes above is one.
- **unset-swap-bin is observationally equivalent on this host and
  thereby unkillable by any case.** /bin is a symlink to usr/bin
  (readlink -f /bin = /usr/bin; /bin/true and /usr/bin/true share
  inode 13516892; /bin/sh = /usr/bin/sh, Sec. 9.7). A mutant file that
  lists this as expect:kill makes `mutants_killed == mutants_counted`
  unsatisfiable for **every** candidate including the committed one:
  TARGET_MET becomes unreachable regardless of target-ness. The frozen
  predicate has no conjunct requiring a mutant to be killable in
  principle, so this failure mode is invisible to the predicate text.
- **unset-as-empty is killed, but only lexically (rootprog argv0) and
  through the TryExec door.** Both kills require the frozen expect to
  carry the argv vector and the TryExec arm; a set of
  launches-only or Exec-only expectations would let the misreading
  survive in the success region. The predicate's `< total` threshold
  cannot tell which of these killed it.
- **Comparator sensitivity is a first-class risk.** My own harness
  produced a false WRONG for the committed tool on pd-unset-tryexec-true
  through the {probe} vs {root} canon order alone (Sec. 7(2), Sec.
  9.11). The r100 counter must be scored against the oracle's canon
  order, and any mutant whose kill depends on a host binary name
  (`true`, `sh`) must be re-run through the landed counter, not a
  re-implementation.

Counterexample artifact paths:
.ufo/waves/round-100/claims-declaration-r100.md (lines 29-34);
scoring inputs above are carried in Sec. 9 of this report (scratch
deleted); independent corroboration: .ufo/waves/round-100/receipts/
labrat-unset-r100.txt.

### 5.3 The frozen-set requirement this implies

To make the prose true the frozen set must contain, as **distinct
labelled classes with minima** and paired fixtures differing only in
PATH:

1. unset + bare Exec=probe at root (expects {root}/./probe) **and** its
   empty twin (expects {root}/probe) -- separates (1)-success lexically;
2. unset + TryExec=<host-program-in-/usr/bin> (expects launch) **and**
   its empty twin (expects load) -- separates (1)-/usr/bin-arm;
   naming the host program `true`/`sh` is load-bearing and must be
   re-measured, not transcribed;
3. unset + Exec=<private-only> (expects load) **and** its
   PATH={root}/bin twin (expects launch) -- separates (2);
3b. unset + Path=work (relative) + Exec=probe with work/probe
   (expects {root}/work/./probe) **and** its PATH="" twin
   (expects {root}/work/probe) -- the corrected separation (3);
4. **No** frozen Terminal=true case with path:null (real-terminal
   hazard, Sec. 4) and **no** separation-(3) fixture claiming a
   Path-effect (false geometry, Sec. 1a);
5. A same-name collision case (case file named like a host program,
   e.g. `ls`) if order mutants are counted; otherwise order mutants
   must be excluded from mutants_counted.

None of these is checkable until the files land; that is Sec. 6's gap.

## 6. (d)/(e) Fresh leg and mutant population: what can and cannot be judged yet

At review time the round-100 controls directory contains only
harm-panel-r100.json. **There is no c1-r100 counter, no
launchenv-cases-r100.json, no launchenv-fresh-r100.py and no
launchenv-mutants-r100.json** (ls output in Sec. 9). The following
therefore records (i) what the r99 instruments do (the template the r100
ones inherit), (ii) the specific lines on which the r100 versions must
be reviewed when they land, and (iii) verdicts that are neutral *only*
for lack of artifacts -- the L1 must not file TARGET_MET until these are
read.

### 6.1 (d) Fresh generator: measures, does not transcribe; seed at measurement (r99)

- **Measures through the oracle.** launchenv-fresh-r99.py loads the
  probe module by path (spec_from_file_location("lprobe_fresh",
  PROBE_PATH)), calls P.measure_case(cand, args.dir, pin, runs=2)
  (line 243) and checks pin == P.GIO_SHA256 (line 228). Where the
  generator's own roots are transient, the counter rebuilds roots
  itself (fresh_cases canon-gap repair). Labels are not transcribed
  from cases; they are produced by the instrument. The r100
  generator must preserve this (import + measure_case + pin check),
  not embed a label table.
- **Seed taken at measurement.** The counter draws the seed at run time
  (seed = os.environ MADO_R99_FRESH_SEED or os.urandom(8).hex(),
  counter fresh leg) and passes it to the generator
  (--seed HEX, --count 60, FRESH_COUNT="60"). The generator's
  random.Random(int(seed,16)) selects every shape decision ("same seed
  builds byte-identical cases"). The predicate's "(fresh_total >= 8,
  seeded at measurement)" matches this pattern; note the floor is 8
  while the r99 implementation runs 60 -- the floor is weak by design
  and the sentence must not be read as "8".
- **Coverage hole inherited by default (the (d) gap).** The r99
  generator *never* emits path:null: bcase defaults path to
  ["{root}/bin"] and build_case never assigns None (fresh:51,63;
  the only empty-ish shape is path ["{root}/bin", ""]). Its exec
  shapes are abs/bare/bare-first/dir/missing/dot/sub/exec644/
  empty-entry/dot-entry -- all with a **list** PATH. So a fresh leg
  generated by a copy of this generator covers the default branch
  **zero** times even at 60 cases, and `fresh_correct == fresh_total`
  would certify a branch never exercised. The predicate's fresh
  conjunct does not require any fresh case to carry path:null
  (peer critic point 5). The r100 generator must either add a
  path-null shape (with its paired empty twin) or the filed sentence
  must say "fresh leg of unconstrained composition" (peer critic
  narrowing 4). Verdict on (d) as it stands: **neutral** (r99-pattern
  verified; r100 file does not exist to judge).

Counterexample/gap artifact paths:
.ufo/waves/round-99/controls/launchenv-fresh-r99.py (template);
the decision point is still to be frozen in
.ufo/waves/round-100/controls/launchenv-fresh-r100.py (absent at review).

### 6.2 (e) Mutant population: two classes of defect, both reachable

The r99 mutants file (69 mutants, find/replace anchors in the
candidate's non-selftest prefix -- counter non_selftest_prefix trims at
`def selftest(`) has two failure modes the frozen r100 predicate cannot
distinguish, each with a concrete exhibit this seat built:

- **Unkillable / equivalent mutant (correct model cannot kill).**
  DEFAULT '/bin:/usr/bin:.' -> '/usr/bin:/bin:.' (swap). On this host
  /bin -> usr/bin, same inode; the two entries name one directory, so
  every program has the same hit/miss under both. No case can see
  this mutant. If the r100 file counts it as expect:kill,
  mutants_killed==counted fails for the committed candidate itself
  (Sec. 5.2). The r99 file's order mutants over KNOWN_TERMINALS have no
  such equivalent, but the r100 file is unwritten.
- **Spuriously-killed / surviving wrong model.** unset-dot-first
  ('.:/bin:/usr/bin') and unset-swap-bin survive every Exec-only fixture
  in Sec. 5.2; they are visible only through narrow doors (TryExec
  /usr/bin arm, or a same-name collision). If the mutant file carries
  them but the case file lacks those doors, a *wrong* candidate is
  scored as killing them wherever they differ from its own baseline
  for other reasons (comparator sensitivity, Sec. 5.2), while a
  *correct* candidate's mutant copy survives. The frozen predicate's
  `mutants_killed == mutants_counted (mutants_counted >= 4)` -- with
  **no anchoring requirement to the default branch** (peer critic: four
  terminal-table mutants satisfy it) -- cannot tell these apart.
- **The mirror image: a wrong baseline kills the correct default
  spuriously.** Kills are scored relative to the candidate's own
  baseline (r99 mutant leg: mutant wrong AND candidate ok). From the
  Sec. 5.2 rows, take the wrong candidate `as empty` as baseline and
  submit the TRUE default (`'/bin:/usr/bin:.'`) as a "mutant": on
  pd-unset-rootprog it answers {root}/./probe vs baseline {root}/probe
  and on pd-unset-tryexec-true it launches while the baseline refuses
  load -- it is duly counted "killed" by a wrong model. The frozen
  conjunct `cases_correct == cases_total` prevents that path from
  reaching TARGET_MET (a wrong baseline fails first), so this is a
  risk only to a reader who treats the mutant leg as a discrimination
  claim on its own; the filed sentence must not let that reading stand
  (the mutant conjunct proves the population died under a correct
  baseline, nothing more).
- **Crash-not-kill hygiene.** The r99 counter's mutant leg counts
  new crashes as crashed_not_killed, never kills (wrong_ids must be
  new-wrong vs baseline-ok). The r100 counter must keep this; a mutant
  that crashes the tool (traceback, rc not in {0,2}) is not a kill.

Verdict on (e): **neutral** (no r100 mutant file exists to falsify;
the exhibited killable/killed-by-wrong-model/equivalent classes are
pinned above for the L1 to screen the landed file against). Artifact
until landed: .ufo/waves/round-100/controls/launchenv-mutants-r100.json.

## 7. (f) argv0 shape {root}/./probe vs {root}/probe: fragility assessment

Re-measured (L1 ground confirmed; labrat receipt consistent):

- PATH absent, Exec=probe at case root (cwd=root): argv[0]={root}/./probe.
- PATH="", same fixture: argv[0]={root}/probe.
- PATH={root}/bin, helper in bin: argv[0]={root}/bin/helper.
- Candidate from correct cwd with no PATH in env: {root}/./probe; with
  --path "": {root}/probe. Reference outputs in Sec. 9 (caseF2 with
  absolute /usr/bin/python3).

Fragility findings (each names a failure mode the r100 case design must
avoid; enumerations only, no verdict unless the frozen expectation
shape is known):

1. **Lexical, not semantic, discrimination.** {root}/./probe and
   {root}/probe name the same file. The counter compares argv strings
   exactly after {root}/{probe} substitution (r99: sorted(parsed argv)
   == sorted(norm argv); no normpath/realpath on argv -- grep confirms
   realpath is used only for arg-escape containment). So the unset-vs-
   empty separation in the success region is a **lexical** distinction
   './' carried in the string. It is real (GLib builds it via the dot
   entry, gutils.c walk) and it is *not* fragile in the sense of being
   wrong -- but it means a candidate that normalises ('./probe' ->
   'probe') or an oracle that canonicalises would cross the kill line.
   Labrat's 04 vs 05 (ARGV0 {root}/./probe vs {root}/probe) recognises
   this; the frozen expects must carry the argv vector verbatim.
2. **{probe} vs {root}/probe.sh double token.** A case with
   Exec={root}/probe.sh and no bare file measures argv {probe} (oracle
   canon replaces the probe path first). A case with Exec=probe (bare)
   and file probe measures argv {root}/./probe (root alone). The counter
   must reverse both tokens in its exact inverse order (counter
   _subst: {root} first, then {probe}; oracle canon: probe first, then
   root). My own scorer got one cell wrong through this order (Sec. 5.2)
   -- re-running the r100 mutant table through the landed counter (not a
   re-implementation) is mandatory before claiming any kill.
3. **CWD sensitivity.** The argv {root}/./probe form depends on the
   process cwd == case root at load time (join os.getcwd() + './probe')
   and on the walk's re-join to working_dir when Path is set. Any
   harness that runs the candidate with a different cwd (e.g. fleet
   root, from which the committed tool in my first runs answered
   load/exec-argv0 for a correct fixture) manufactures a false miss.
   The r99 shared-contract env runs the candidate with cwd=root
   (materialise_case + run_tool cwd=cwd) -- the r100 counter must
   preserve it, and the L1 must reject any TARGET_MET receipt whose
   candidate leg did not run cwd=root.
4. **The shared-contract env landmine (new, not in peer critic).** The
   r99 counter's run_tool always runs the candidate with
   env={"PATH": "", "LC_ALL": "C", "HOME": ...} (counter:304-310) and
   omits --path exactly when the case path is null. With no --path the
   tool falls back to os.environ.get("PATH") (tool run:297-298) --
   which under that env is the empty string, **not** unset. I proved
   the two differ for the same fixture (Sec. 9, empty.json vs
   unset.json): PATH=""-in-env + no --path answers {root}/probe;
   no-PATH-in-env + no --path answers {root}/./probe. Under the r99
   counter's env, every path:null case in a future r100 file would be
   scored with the candidate behaving as unset==empty, so the correct
   tool would score wrong on its own branch. The r100 counter must
   branch its env: omit the PATH key entirely for path:null cases
   (like the oracle does, probe:369-371). The frozen predicate does not
   mention this; it is a counting-command correctness requirement,
   and a TARGET_MET run under the r99 env would be vacuous (it would
   certify the empty model as the unset model). The L1 must obtain the
   r100 counter's run_tool diff for this line before scoring. Note the
   fix must omit the PATH key (contract: no --path and no PATH =
   unset); passing `--path "/bin:/usr/bin:."` explicitly would answer
   the same walk while bypassing the tool's None branch, i.e. it would
   pass the case without exercising the modelled default.
5. **Trailing-slash / dot canonicalisation of GDF and cwd.** Not
   argv0, but adjacent: GIO_LAUNCHED_DESKTOP_FILE is the canonicalised
   absolute path (tool _canonicalise_arg). The frozen expects must
   carry it in the same canonical form the counter reverses; a case
   with rel_desktop changes this value's relativity between oracle and
   candidate legs (r99 schema_notes). Avoid rel_desktop on new default
   cases unless the pair is paired.

Counterexample artifact paths:
.ufo/waves/round-100/claims-declaration-r100.md (Shared contract 2,
lines 123-131: oracle must run env -i with no PATH for path:null --
"verify the oracle does this before trusting a label"; the symmetric
requirement for the candidate leg is unstated);
the sentinel env line is at quality/counters/c1-r99-launchenv.py:307
(inherited contract, not yet a round-100 artifact).

## 8. Locator drift (M99-2 class -- recorded, not a predicate falsification)

Peer critic noted it; independently re-derived this seat:

- claims-declaration-r100.md:12 cites gutils.c:370-382 for the literal;
- claims.json C1 frozen text cites gutils.c:376-389 for the same literal;
- tools/mado-launchenv.py:120 cites gutils.c:409-421 for the same literal.

Measured on the fetched bytes (.ufo/waves/round-99/fetch/gutils.c, via
grep -n + awk, Sec. 9): the literal path = "/bin:/usr/bin:." is at
line 388; the PATH-source read (path = g_getenv("PATH")) is at 371;
the absolute/relative early return is at 332-357; the g_return at 320.
So: declaration 370-382 contains the PATH source (371) but **not** the
literal (388); claims.json 376-389 contains both the `if (path == NULL)`
(376) and the literal (388) and is the only range that contains the
cited literal; the tool's 409-421 contains neither (it is past the
# else / Windows arm). The L1 must re-derive all three locators by
grep -n on the fetched bytes before filing (M99-2's rule, lesson
round-99.md M99-2). No conjunct reads a line number, so this is not a
sentence falsification -- but it is a record inaccuracy of exactly the
kind criterion 172a/172 police, and all three cannot be filed
unchanged.

Counterexample artifact paths:
.ufo/waves/round-100/claims-declaration-r100.md (line 12);
.ufo/waves/round-100/claims.json (line 12);
tools/mado-launchenv.py (line 120, committed input, not waved).

## Residual risk and verification gaps (what this seat did NOT settle)

- C1 r100 counter, case file, fresh generator, mutant file, and
  measurement receipts **do not exist** at review time (controls/ has
  only harm-panel-r100.json). Every verdict marked neutral becomes
  un-neutral only when the L1 reads those files against Sec. 5.3, Sec.
  6 and Sec. 7(4). The frozen predicate's numbers (fresh >=8,
  mutants >=4, classes >=3) are floors with no per-separation minima;
  the landed artifacts' contents -- not the predicate -- determine
  whether any separation actually holds.
- The Sec. 5.2 table is settled for the seven fixtures I built (Sec.
  9.11 final run under the oracle canon order: dot-first and swap-bin
  survive everything, drop-dot dies only on rootprog). It is not a
  substitute for scoring the landed r100 file: the kills the predicate
  counts depend on the r100 case composition, and the table's
  host-binary-dependent cells (`true`) must be re-run through the landed
  counter at committed bytes. The equivalence of /bin<->/usr/bin order
  on this symlink host does not depend on the comparator and stands.
- This seat did not run a Terminal=true + PATH-unset fixture beyond the
  accidental pd-unset-term hit (host /usr/bin/xdg-terminal-exec present;
  oracle returned setup-error). The hazard warning in Sec. 4 rests on
  /usr/bin/xdg-terminal-exec being executable and on the walk consulting
  the default; I did not launch it again.
- Peer artifacts landed during this review (critic 55KB, labrat 7KB,
  review-C2) were read in full (critic Sec. 1) or in full (labrat) and
  are consistent with this seat's measurements; this seat did not
  re-execute the critic's F1 construction (it is a construction over
  committed bytes, verified by inspection) and did not re-run the
  labrat fixtures (they agree with this seat's 7+ oracle runs).

## Hygiene

- Scratch: /fast/scratch/hyaku/mado-r100/R100MReviewC1 (fixtures,
  five mutant copies, oracle roots, probe script) created with mkdir -p,
  passed explicitly; deleted before yield. /tmp not used.
- No tool install or upgrade (nothing needed; no pacman/uv/npx run).
- No host application launched; every gio/oracle invocation ran under
  env -i without a host PATH (LC_ALL/HOME/PROBE_OUT, plus the case's own
  PATH where set). No terminal spawned; the one accidental Terminal=true
  + PATH-unset oracle case hit /usr/bin/xdg-terminal-exec and returned
  setup-error (winit), recorded in Sec. 4 as a hazard, not repeated.
- No lane file written except this report; no git/jj mutation
  (git log/show/ls-tree/diff/rev-parse only). No ~/.config, ~/.ssh,
  ~/.gnupg or credential read.
- Wall times: each oracle measure pass 3-13 s (single runs, 1.5 s quiet
  wait each); total instrument wall under ~70 s on the loaded host
  (load average ~250/32 cores).

## 9. Evidence (verbatim command outputs behind every finding)

All commands run in /home/vgpnk/Projects/shokunin/mado-shokunin (cwd
fleet root for git; scratch runs cd'ed into the fixture root), host
paths read-only, every gio/oracle launch with env -i and no host PATH
(LC_ALL/HOME/PROBE_OUT only, plus case PATH where set). Scratch dir
deleted before yield (rm -rf /fast/scratch/hyaku/mado-r100/R100MReviewC1).

### 9.1 Base state (before-state inputs)

```
$ git log --oneline -15 | head
43309e6a round-99 verifier spot-check (integrator, hyaku): non-author admit/reject
0e8f39f5 round-99: the pre-file plan ...
$ sha256sum /usr/bin/gio
d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462  /usr/bin/gio
$ git rev-parse HEAD
43309e6af9a3b57f1bc839a826bef1f8eb7495e4
$ git diff --stat HEAD -- tools/mado-launchenv.py quality/
(empty -- tool/quality at base)
$ git ls-tree 43309e6a tools/mado-launchenv.py
100755 blob dfc0976e... tools/mado-launchenv.py  (present at base)
$ git show 43309e6a:tools/mado-launchenv.py | grep -n 'DEFAULT_SEARCH_PATH'
33: ... "/bin:/usr/bin:." (R6); PATH set but EMPTY walks one
121:DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'
179:    of the process PATH (None = unset -> the /bin:/usr/bin:. default). Returns
207:        path = DEFAULT_SEARCH_PATH
$ python3 -I tools/mado-launchenv.py --selftest
MADO_LAUNCHENV_SELFTEST: checks=90 failed=0
$ grep -n 'def find_program' on mado-mime at base (peer F4, verified):
466:def find_program(program: str, path_env: str | None, workdir: str | None) -> bool:
```

### 9.2 r99 file scan (Sec. 4, (c))

```
$ python3: r99 file total=67
classes: {'arg-conv':3,'cwd-empty':3,'cwd-missing':2,'cwd-path':2,'env-gdf':3,
 'exec-test':4,'multi-term':3,'path-empty-entry':5,'path-unset':2,'prog-abs':2,
 'prog-bare':2,'prog-dir':2,'prog-missing':2,'prog-notfound':1,'prog-rel':2,
 'refuse-shape':4,'term-color-xterm':1,'term-dtterm':1,'term-kgx':2,'term-konsole':1,
 'term-mate':1,'term-none':2,'term-nxterm':1,'term-order':2,'term-path':2,
 'term-rxvt':1,'term-tilix':1,'term-xfce4':1,'term-xte':3,'term-xterm-row':1,'tryexec':5}
path-null cases (2 of 67):
  pu-abs-work path=None  Exec='{root}/probe.sh' Path='{root}/work'
  pu-abs-root path=None  Exec='{root}/probe.sh'
all other 65 cases: path is a list (PATH set, possibly [""] or ["."]).
path-empty-entry pe-* etc: path lists containing '' -- set-but-empty, not unset.
=> 0 bare-lookup + path-null cases. Before-state TRUE (neutral).
```

### 9.3 gutils.c locators (Sec. 8)

```
$ grep -n 'bin:/usr/bin\|g_getenv ("PATH")' fetch/gutils.c
371:    path = g_getenv ("PATH");
388:      path = "/bin:/usr/bin:.";

$ awk 'NR>=300 && NR<=395':
300: g_find_program_for_path (...)
320:   g_return_val_if_fail (program != NULL, NULL);
322:   /* Use the working dir as program path if provided */
332:   if (g_path_is_absolute (program) || strchr (original_program, ...) )
...
357:           return g_steal_pointer (&out);
370:   if G_LIKELY (original_path == NULL)
371:     path = g_getenv ("PATH");
376:   if (path == NULL)   /* #if defined(G_OS_UNIX) */
...
388:       path = "/bin:/usr/bin:.";
396: extern ... (~395 Windows arm begins)
=> declaration 370-382: contains 371, misses 388. claims.json 376-389:
contains 376+388. tool 409-421: neither (Windows arm region).
```

### 9.4 Oracle fixtures (Sec. 5.1; labrat agrees 7/7)

```
pin d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462
pd-unset-rootprog  path=None Exec=probe        -> launches=1 argv=[{root}/./probe]
pd-empty-rootprog  path=['']  Exec=probe        -> launches=1 argv=[{root}/probe]
pd-unset-private   path=None Exec=helper@bin    -> error=load (rc 1)
pd-set-private     path=['{root}/bin'] helper    -> launches=1 [{root}/bin/helper]
pd-unset-usrbin    path=None Exec=true (host)    -> error=setup-error (rc0, no record)
pd-empty-usrbin    path=['']  Exec=true          -> error=load (rc1)
tryexec door:
pd-unset-tryexec-true  path=None Exec={root}/probe.sh TryExec=true
  -> launches=1 argv=[{probe}] rc0
pd-empty-tryexec-true  path=[''] same           -> error=load rc1
pd-unset-tryexec-missing / pd-empty-tryexec-missing -> error=load both
pd-unset-term  path=None Terminal=true
  -> error=setup-error rc0, stderr: winit 0.30.13 OsError (host xdg-terminal-exec walk)
pd-empty-term  path=[''] Terminal=true          -> error=no-terminal rc1
```

### 9.5 Separation-(3) false geometry (Sec. 1a; scratch sep3, 9.15s)

```
s3-exec-empty-pathwork (Path={root}/work, work/probe, Exec=probe, PATH="")
  -> launches=1 argv=[{root}/work/probe]  (sentence predicts not-found: FALSE)
s3-exec-unset-pathwork (PATH unset, same)  -> launches=1 argv=[{root}/work/probe]
s3-exec-empty-pathwork-rootonly (probe only at root, Path={root}/work, PATH="")
  -> error=load
s3-exec-unset-pathwork-rootonly (PATH unset, same) -> error=load  (identical)
s3-tryexec-empty (TryExec=helper@work, PATH="")  -> launches=1 argv=[{probe}]
s3-tryexec-unset (PATH unset, same)              -> launches=1 argv=[{probe}]
```

### 9.6 unset vs empty argv0 (Sec. 7; cwd=root, absolute python)

```
caseF2 (probe at root, Exec=probe, cwd=case root):
$ env -i PATH='' ... tool --json
{"launches": 1, ..., "argv": [[".../caseF2/probe"]]}            # empty
$ env -i (no PATH) ... tool --json
{"launches": 1, ..., "argv": [[".../caseF2/./probe"]]}         # unset
diff empty.json unset.json: .../probe vs ..././probe (1c1)
$ direct: find_program('probe', None, None) -> .../caseF2/./probe ; find_program('probe','',None) -> .../caseF2/probe
# hence run_tool env {"PATH":""} + omitted --path == empty model (Sec.7(4))
$ oracle cwd=OTHER (case rooted elsewhere, path null, Exec=probe):
gio: Unable to load application information for '.../case.desktop' rc=1  (L1 critical, confirmed)
```

### 9.7 /bin vs /usr/bin identity (Sec. 5.2)

```
$ readlink -f /bin /usr/bin
/usr/bin
/usr/bin
$ ls -i /bin/true /usr/bin/true
13516892 /bin/true
13516892 /usr/bin/true
$ ls -l /bin | head
lrwxrwxrwx ... /bin -> usr/bin
$ ls /usr/bin/xdg-terminal-exec
-rwxr-xr-x 1 root root 44020 ... /usr/bin/xdg-terminal-exec  (Terminal hazard)
```

### 9.8 Fresh generator r99 (Sec. 6.1)

```
$ grep -n '"path"' launchenv-fresh-r99.py
51: kw.setdefault("path", ["{root}/bin"])
63: path = ["{root}/bin"]
110: path = ["{root}/bin", ""]   (empty-entry shape; still a list)
(no assignment of path=None anywhere; exec shapes: abs/bare/bare-first/dir/missing/dot/sub/exec644/empty-entry/dot-entry)
$ grep -n 'measure_case\|measure_once\|P\.' launchenv-fresh-r99.py
39: spec_from_file_location("lprobe_fresh", PROBE_PATH)
243: expect_i, _metas, agreed = P.measure_case(cand, args.dir, pin)
227: pin = P.gio_sha256(); 228: if pin != P.GIO_SHA256: (raise)
$ counter fresh leg (c1-r99): seed = os.environ.get("MADO_R99_FRESH_SEED") or os.urandom(8).hex()
  --seed HEX --count "60" (FRESH_COUNT="60"), env PATH=/usr/bin:/usr/sbin:/bin for generator
```

### 9.9 Missing round-100 C1 artifacts (Sec. 6)

```
$ ls -la .ufo/waves/round-100/controls/ .ufo/waves/round-100/build/
controls/: harm-panel-r100.json   (only)
build/:    c2-r100-harm-watch.py, harm-watch.py   (C2 only; no C1 counter/cases/fresh/mutants)
$ ls .ufo/waves/round-100/controls/*fresh* 2>&1
ls: cannot access '.ufo/waves/round-100/controls/*fresh*': No such file or directory
$ ls quality/counters/c1-r100-launchenv-path.py 2>&1
ls: cannot access 'quality/counters/c1-r100-launchenv-path.py': No such file or directory
```

### 9.10 Peer w1 status at yield

```
w1/: swarm-registry.json, R100MCriticClaims.md (925 lines, C1 Sec.1 + C2 Sec.2),
     R100MExecGate.md (C2 gate; placeholder timeout_s 3600, L1 to finalize),
     R100MLabratUnset.md (H1 NOT FALSIFIED, 7+7), R100MReviewC2.md
receipts/: c2-gate-r100.txt, c2-panel-r100.txt, labrat-unset-r100.txt
C1 verdicts of peers: critic F1-F4 (Sec.2 above), labrat H1 stands
```

### 9.11 Final wrong-model table, oracle canon order (Sec. 5.2; scratch final-*, 3.78 s)

```
EXPECT pd-unset-tryexec-true {'launches': 1, 'argv': [['{probe}']], 'cwd': '{root}', 'env_gdf': '{root}/case.desktop'}
EXPECT pd-empty-tryexec-true {'error': 'load'}
--- committed ---
  pd-unset-tryexec-true OK(survive) {'argv': [['{probe}']], ...}
  pd-empty-tryexec-true OK(survive) {'error': 'load', 'detail': 'try-exec'}
--- unset-dot-first ---
  pd-unset-tryexec-true OK(survive)  pd-empty-tryexec-true OK(survive)
--- unset-swap-bin ---
  pd-unset-tryexec-true OK(survive)  pd-empty-tryexec-true OK(survive)
--- unset-as-empty ---
  pd-unset-tryexec-true KILLED rc=2 {"error": "load", "detail": "try-exec"}
  pd-empty-tryexec-true OK(survive)
--- unset-drop-dot ---
  pd-unset-tryexec-true OK(survive)  pd-empty-tryexec-true OK(survive)
--- unset-as-colon ---
  pd-unset-tryexec-true KILLED rc=2 {"error": "load", "detail": "try-exec"}
  pd-empty-tryexec-true OK(survive)
```
Combined with the 5.1-door rows (rootprog kills as-empty/drop-dot/colon;
private kills none; set-private kills none; pathwd kills none), the full
matrix of Sec. 5.2 follows: dot-first and swap-bin survive all seven
fixtures; drop-dot survives six of seven (dies only on rootprog).

### 9.12 Relative-Path separation (the corrected (3)); oracle + candidate agree

```
$ oracle (scratch sep3rel, cwd=root, pin d2164260...):
relpath-unset  Path=work, work/probe, Exec=probe, PATH absent
  -> launches=1 argv=[{root}/work/./probe] rc=0
relpath-empty  same fixture, PATH=""
  -> launches=1 argv=[{root}/work/probe] rc=0
relpath-unset-rootonly (probe only at root, Path=work) -> error=load
relpath-empty-rootonly                                  -> error=load
$ committed candidate (scratch relchk, cwd=root; no PATH key / --path ""):
relpath-unset ORACLE [{root}/work/./probe]  CAND {root}/work/./probe  rc=0
relpath-empty ORACLE [{root}/work/probe]   CAND {root}/work/probe   rc=0
```

## Recommendations for the L1 (ordered; each is a pre-file narrowing)

1. **Narrow the separations.** Replace declaration (3) with a true
   sentence or delete it. The measured true content (Sec. 1a/9.12): "with
   a relative Path=, the trailing '.' is visible as an extra './' in
   argv0 ({root}/work/./probe under unset vs {root}/work/probe under
   PATH=''); the program is found in both states, so (3) is a lexical
   separation, not a reachability one." Keep (1) and (2)
   but attach them to the fixture shapes that actually fire them (Sec.
   5.1: (1)-/usr/bin via TryExec=host-program; (2) private-bin miss vs
   set-PATH hit). Record with this artifact and peer critic
   narrowings 1-7 (plans/round-100.md, currently empty).
2. **Fix the candidate-leg env.** The r100 counter's run_tool must omit
   the PATH key for path:null cases (Sec. 7(4)); obtain the exact diff
   before scoring and re-derive TARGET_MET under it. Add a selftest
   leg that fails a candidate reading process-PATH when --path is
   omitted (the r99 design intent, counter:304-310) *in the direction
   the unset contract needs*.
3. **Add per-separation minima or admit they are enumerated labels.**
   Either pin three named classes (one per rewritten separation) with
   per-class minimum >=1 and a paired-fixture check, or file the
   honest sentence: "a class of >=6 cases, of which at least one
   separates each named neighbour; the predicate enforces one
   discriminating case total."
4. **Gloss base_set_default_cases==0** as "counts the path-default label
   in the r99 file (0 by construction); branch-reachability of the r99
   file was established by inspection of its two pu-* Exec bytes (this
   report Sec. 4), not by this conjunct" -- or replace the conjunct with
   a geometric count (path:null AND non-absolute load-gate lookup).
5. **Re-derive the gutils locators** (Sec. 8): literal at 388, PATH at
   371, early return at 332-357. File one range per fact, verified by
   grep -n on the fetched bytes (M99-2 rule).
6. **Forbid the hazard shapes in the frozen set:** no Terminal=true
   with path:null (real-terminal walk via /usr/bin/xdg-terminal-exec),
   no Path=-involving separation-(3) fixtures (false geometry).
7. **Screen the mutant file before scoring:** exclude equivalent
   mutants on this symlink host (any /bin<->/usr/bin order change),
   require at least one mutant anchored on the
   DEFAULT_SEARCH_PATH / path-is-None branch, and require the kill log
   to identify the killing case for each mutant.

Report: .ufo/waves/round-100/w1/R100MReviewC1.md
