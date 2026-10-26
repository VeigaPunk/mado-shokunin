# Round 46 — mistakes draft (for `corpus/lessons/round-46.md ## Mistakes`)

Author: `ScrMistakes` (scribe seat, round-46 w1, 2026-10-26). Lane `mado-shokunin`, base
`b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`.
Every count below was re-derived from the lane's own bytes (read-only `git show`/`git grep`/`git ls-files`,
`GIT_OPTIONAL_LOCKS=0 git status`) or from a scratch clone of the freeze at
`/fast/scratch/hyaku/mado-r46/ScrMistakes` (deleted before yield); receipts in
`.ufo/waves/round-46/w1/ScrMistakes/receipts/`. Seat paths (`CritW2Entry/...`, `ExecSerialRule/...`) are relative
to `.ufo/waves/round-46/w1/`. Seat-reported measurements I did not rerun are marked
`[seat receipt]` with the path; everything unmarked is `[observed]` by me at the revision named.
Classes are the mistakes vocabulary (`vacuous`, `survivor`, `stale-premise`, `reference-drift`,
`number-drift`, `scope`, `attribution`, `landing`, `provider`).

## Rows

**M46-1** · class `number-drift` · evidence: the frozen registration states two cross-scope URL repeats
(`.ufo/waves/round-46/registration.md:47`, "The two cross-scope URL repeats"), while the positive-control
tree prints **five** new W04 lines — S317 (with S162, S303), S318 (with S215), S320 (with S158, S307),
S321 (with S182), S324 (with S173): `receipts/census-pos.txt` (14 W04 lines at the positive tree) against
`.ufo/waves/round-46/receipts/census-before.txt` (9 W04 lines at base), and exact-URL row counts in `receipts/url-exact-pos.txt`
(ConfigManager 3 rows, ConfigValues 2, HyprCtl 3, MiscFunctions 2, hyprlang 2) · two independent seats reached
the same five (`CritRegistration.md:16`, F1 "F1 (wrong count)"; `CritPremise.md:20`, "5 duplicate-URL introductions declared as 2") ·
captured-by: QUALITY 10 and 14 — the sentence was hand-written, not emitted by the instrument that measures it ·
fix: the round lesson/errata carries the census delta (five) and names each new row with the held row(s) it
repeats; the frozen registration is not rewritten. Shown able to fail: the census is a command whose W04 line
count moves 9 → 14, so a sentence claiming two disagrees with its own instrument by three rows.

**M46-2** · class `vacuous` · evidence: the C2 control battery's first cut stopped before scoring — its
FALSE-URL fixture asserted global uniqueness of a URL the corpus holds twice
(`.ufo/waves/round-46/ctl/run-c2-controls.py:17`, "the first cut's single-occurrence assertion stopped the runner
before any score"; the assertion survives at `:126`, `assert reg.count(url) == 1`) · measured on the positive
tree (`receipts/harness-assert-demo.txt`): the MiscFunctions URL occurs **2** times (S182, S321) so the assertion
raises, while the protocols/VirtualKeyboard.cpp URL occurs **1** time (S323) so it holds; `receipts/url-exact-pos.txt`
shows both rows · why vacuous: a battery that stops after seven of its fifteen controls prints no `CTL_C2` verdict, so the
fifteen controls produced **no** evidence, and a relaxed `>= 1` would have rewritten a held row's URL (S182)
alongside the new row's — a control mutating outside its subject · captured-by: QUALITY 59 is adjacent (a
control that fails for a setup reason is not a kill) but it names the environment, not a corpus premise ·
fix: address the mutation by row identity (the row's own location cell) and assert on that cell, never a global
string count; the committed control mutates S323's unique URL and the counter rejects it
(`.ufo/waves/round-46/receipts/ctl-c2.txt:9`, "CTL_C2 FALSE-URL want=rejected got=rejected rc=1 ok", clause `e:0`).
Shown able to fail: `check87.py` scores the committed receipt `PASS` (15 controls, verdict present) and the
aborted shape `FAIL` (`scored=7 want=15 verdict_line=absent`, `receipts/check87-run.txt`).

**M46-3** · class `survivor` · evidence: a reference variant that undoes one modelled semantic — case-insensitive
device-name matching (V03) — met PRED-C1-r46 before the freeze (`registration.md:34`, "A pre-freeze run met V03
(case-insensitive names)"), i.e. the fixture lattice had no case-sensitivity class; the separating fixture was
added before data (`.ufo/waves/round-46/receipts/ctl-c1.txt:7`, "V03-case-insensitive-names rc=1 … fixtures=89/90
… verdict=TARGET_MISSED"; the fixture is `quality/counters/c1-r46-fixtures.json` index 22, label
`case-exact-dump-name`, file sha256 `027ed508…` = the counter's `FIXTURES_SHA256`, `receipts/fixtures-pin.txt`) ·
the pre-freeze run itself has no committed receipt — the evidence is the registration's sentence plus the
post-freeze control line, and `CritRegistration.md` §4 records that limit · captured-by: QUALITY 65 (fixtures from
a lattice on the tree index, one single-defect mutant per class; a survivor is a missing class) ·
fix: the case class is a fixture, not a comment. Shown able to fail: V03 scores 89/90 at the freeze and the
mutant matrix flips V03 to MET only when clause f's exactness is weakened (`MutC1Counter.md:33`, "V03
(case-insensitive names): fixture `case-exact-dump-name` FAIL in all three runs"; `:78`, "The control set's only
load-bearing channel is clause f's exactness") `[seat receipt]`.

**M46-4** · class `vacuous` · evidence: PRED-C2-r46 admits 10 of 12 crafted revisions a reader rejects, and
**six are undeclared** (`CritC2Forgery.md:10`, "10 were admitted"; `:14`, "6 admitted forgeries are NOT declared";
per-revision counter lines `CritC2Forgery/forge.out:3-15`) `[seat receipt]`. The two sharpest: F7 — the revision
authors its own live receipt under `.ufo/waves/round-46/receipts/` and cites it, clause i reading cited receipts at
REV; F10 — the whole chain replaced by 28 surface bullets while clause j stays `1`. Code paths (computed,
`receipts/c2-counter-sites.txt`): the duplicate-URL guard is keyed on the scope cell (`quality/counters/c2-r46-input-device-entry.py:587`),
the anchor cell is read for range shape only (`:610`), T3 walks fenced blocks only (`:423-430`), clause j binds a
locator and a keyword per surface (`:387`, `:417`) · captured-by: QUALITY 55 (a shape counter names the cribs that
fake its result) — the docstring names three residuals (`:70-74`) but not these six cribs ·
fix: seven tightening candidates A–G (`CritC2Forgery/tighten.py`, `tighten.out`): the positive control passes all
seven and each undeclared forgery fails the intended check (F5d fails two: `E=0 F=0`) (pos `A=1 B=1 C=1 D=1 E=1 F=1 G=1 PASS`; F4
`B=0`; F6 `A=0`; F7 `C=0`; F8 `D=0`; F5d `E=0 F=0`; F10 `G=0`). The frozen counter cannot be edited this round;
the candidates are the next counter's clauses. Shown able to fail: `check88.py` reads `PASS` on
forge.out+tighten.out with the declared set (F1,F2,F3,F9) and `FAIL` when only the positive line is committed
(`admitted_uncovered=F10,F4,F5d,F6,F7,F8`) and when no residual is declared (`admitted_passing=F1,F2,F3,F9`)
(`receipts/check88-run.txt`).

**M46-5** · class `provider` · evidence: the round-45 entry attributes the landed tool's live run to the L1
*reference's* receipt — entry `corpus/knowledge/hyprland-monitor-rule-r45.md:96` at `4d22eeb` cites
`.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`, whose header at `:4` records tool sha256 `c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be`,
while the landed tool at `4d22eeb` hashes
`2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609` (`git show 4d22eeb:tools/mado-monitors.py | sha256sum`) and its own receipt records that hash
(`.ufo/waves/round-45/receipts/live-monitors-host-r45.txt:4`; both bound in
`CritW2Entry/receipts/tool-hash-binding.txt`) · `CritW2Entry/report.md:64` (F2, "false provenance, claim true") `[seat receipt]` ·
captured-by: QUALITY 24 (a sentence that relies on a run receipt cites one whose own bytes name its producer);
the C2 counter cannot see it (declared residual, clause j binds a locator and a keyword, not the truth of the
sentence) · fix: cite `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt`, or say "the reference reported…"; the entry is
landed data, so the correction is an appended erratum. Shown able to fail: one `git show <rev>:<tool> | sha256sum`
against each receipt's header line separates the two receipts (they differ).

**M46-6** · class `attribution` · evidence: the round-45 entry cites, for the mechanism that keeps a disabled
output out of the active list, the branch that *returns before* the event — entry `:84` cites
`Hyprland-Monitor.cpp:264` and `:389`; `:264` returns at `:271`, the only emit site is `:389`, and the veto is
`:275-287` (`CritW2Entry/report.md:40`, "the real gate is uncited (mis-located)"; the ledger's computed 262-290
dump in `CritW2Entry/receipts/verify-quotes.txt`) `[seat receipt]` · captured-by: **none** — `quality/check-locators.py`
(QUALITY 77) passes because the emit fragment occurs at the other cited line, so a range that contains the
identifier is not a range that carries the mechanism · fix: cite `275-287` and `389`. Shown able to fail: the
w2 sentence ledger (`CritW2Entry/receipts/verify-quotes.txt`, 71 probes, `found=71 not_found=0`) is the instrument
that caught it and is re-runnable on the corrected locator `[seat receipt]`.

**M46-7** · class `vacuous` · evidence: the round-45 privacy gate's own selftest passes while the shapes it exists
to catch pass invisibly — `CritW2Gate.md:14` ("the gate's own selftest is `passed=22/22 failed=0` while **22 of 22
attack shapes pass it"), the receipt's per-shape lines (`CritW2Gate/receipts.txt:21`, "caught 0/19", plus three
further misses = 0/22) and the legitimate-shape side (`:28`, "caught 5/6"; `CritW2Gate.md:15`, "5 of 6 legitimate
shapes are flagged"); scan caps: 20 000 stray braces make a dump clean with no truncation signal (`CritW2Gate/receipts.txt:36-39`);
the redaction markers the fleet uses are themselves flagged (`CritW2Gate/receipts.txt:45-52`); the receipt's own lane census reads
`files=17098 findings=102` (`:60`) `[seat receipt]`. M45-1 credited this gate as "shown able to fail" from two
projected files · captured-by: QUALITY 30 (a detector credited for recall is admitted only beside its precision
evidence) — a detector's own selftest is not that evidence · fix: the marker layer makes the false positives
triageable (base 97 findings → 48 with 49 waived; a planted real dump still flagged; a tampered waived fixture
re-flagged, `ExecSessionTriage.md` §3) `[seat receipt]` but does **not** close the 22-shape recall gap; the gate's
claim is narrowed to a policy instrument and `CritW2Gate/repro.py` is its recall measurement. Shown able to fail:
the frozen gate catches 0/22 attack shapes while its selftest reads 22/22 — the two numbers are one receipt apart.

**M46-8** · class `landing` · evidence: round-45 D4's remedy is half-done — `results.json` is gone from
`.ufo/waves/round-45/w1/MutC1Counter/`, but the 282 B replacement digest is itself untracked:
`receipts/d4-d5-state.txt` (`GIT_OPTIONAL_LOCKS=0 git status --porcelain` → `?? .ufo/waves/round-45/w1/MutC1Counter/results.digest.txt`;
`git ls-files` lists four files, not the digest) · `CritRegistration.md:55` (F3, "F3 (stale pointer)") · captured-by:
QUALITY 13 (evidence meant to outlive a round is a committed path) · fix: commit the digest in the round-46 data
commit. Shown able to fail: `git cat-file -e <data-rev>:<digest>` — the path is absent from the tree at the
revision a closure reads until it is committed.

**M46-9** · class `provider` · evidence: the round-45 wave results file is not evidence — 41 seats, 41
`output: null` (`receipts/d4-d5-state.txt`: `seats 41 n 41 null_outputs 41`); the seat report files are the only
record (`corpus/lessons/round-45-verifier-spotcheck.md:116`, D5) · captured-by: QUALITY 79 (a pointer that asserts
a run names a committed receipt) · fix: the wave README or the lesson says the seat `.md` files are the record, not
`w1-results.json`. Shown able to fail: the results rows carry no output, so no claim can cite them, while each seat
report is a committed path.

**M46-10** · class `number-drift` · evidence: M45-2 says the host monitor serial is in one held entry; it is in
**three** held entries and 21 wave copies — `receipts/d2-serial-count.txt`: the token common to the three cited
lines equals a live `monitors all -j` serial field (compared in-process; the value is never written), 24 tracked
files carry it, 3 under `corpus/` (`config-health-report-r3.md`, `hyprctl-verification-layer.md`,
`hyprland-config-plane.md`) and 21 under `.ufo/` · the corrected gate copy flags all 24 carriers
(`ExecSerialRule/receipts/base-scope-all-r5-r6.txt:49`, "R5_SERIAL_PROSE=24 R6_SERIAL_EXACT=24") `[seat receipt]` ·
captured-by: QUALITY 10 and 14 (a count names its command; a census names both sets) · fix: appended erratum
naming the three paths (removal from pushed history stays the operator's), plus the gate's R5/R6 prose rules.
Shown able to fail: base 24 findings → projected tree 0
(`ExecSerialRule/receipts/projected-scope-all-r5-r6.txt:1`, "findings=0 rev=cb46276e"), 45/45 selftest cases `[seat receipt]`.

**M46-11** · class `reference-drift` · evidence: the C2 draft entry's model of the parser and of the dump
drifted from the pins in the places the frozen clauses cannot see — a flat `device:kb_layout = x` is a hard config
error, not a silent no-op (`CritEntryContent.md:67`, "is a hard config error, not a silent no-op"; the entry's
step 2 concludes that the flat key has no device to land on), the UNK row is wrong because the dump prints `active_keymap`
(`CritEntryContent.md:46`, H2), and the `47 values` count is not inside its own cited range
(`ExecC2Census.md:151`, "count is not witnessed by its cited range": 519-565 carries the 47 registrations, 518-540
covers 22) `[seat receipt]`. A fourth unit omits a dump field the same file prints — `main`, which on this host is
true only for the virtual keyboard (`CritEntryContent.md:26`, H1) `[seat receipt]` · captured-by: **none** for the
mechanism sentences (clause j binds a locator and a keyword per surface, not the truth of the sentence); QUALITY 77
catches the narrow locator only because the count's identifier is outside the cited range · fix: the L1 corrects the
entry before the data commit (step 2's conclusion, the UNK row, the 47-value locator split into `518-540` +
`541-565` or dropped from the sentence, and one line on `main`). Shown able to fail: the two seats' own locator
scripts re-derive the counterexamples (`CritEntryContent/locators.txt`, 66 locator rows;
`ExecC2Census/independent-derivation.txt`), and both print the pin lines the draft sentence contradicts
`[seat receipt]`.

**M46-12** · class `vacuous` · evidence: C1's clause r ("no `hyprctl`/`libinput`/`journalctl`/`udevadm` run") is
a PATH-marker test, not an execution test — the marker stubs exist only on environments A/B's PATH, the selftest is
launched with `env={"PATH": "/usr/bin:/bin"` and no fake bin (`quality/counters/c1-r46-devices.py:375`), and
`sandbox()` binds no stub over `/usr/bin` (`:251-257`). Two tools that run `/usr/bin/hyprctl` — one by absolute path
on every run, one by bare name under `--selftest` — score `readonly=ok tool=present verdict=TARGET_MET` at nonce 46
(`SentTool/evidence/clause-r-bypass-absolute-path.txt:96-97`, `clause-r-bypass-selftest-path.txt:95-96`) `[seat receipt]` ·
captured-by: QUALITY 56 (a clause that cannot fail under its own spec is dead code) and 67 (a read-only claim is
stated over every argv element — here the *scored tool's* argv, which the clause never sees) ·
fix: bind the four stubs over their `/usr/bin` paths inside `sandbox()`, give the selftest environment A's PATH, and
fail the clause on any `execve` beyond the tool's own (`strace -f -e trace=execve`); the two committed bypass tools
are the red state and the green (both read `marker=present` → `readonly=fail`) has not been run — the next counter
must score them. Shown able to fail: today's receipt prints `clause=r marker=absent` for a tool that ran hyprctl, so the
clause's own observable is the defect. The in-flight v2 (`quality/counters/c1-r46-devices-v2.py`, untracked, 17:57)
closes two of the three shapes — the selftest env carries the fake bin first (`:403`) and a pipe tripwire replaces
the file marker (`:154-159`) — but `/usr` is still bound read-only (`:280`) with the stub only on PATH, so the
absolute-path shape stays open as written; binding the stub over `/usr/bin/<name>` or logging `execve` is still
needed (`receipts/c1-v2-carryover.txt`, a source reading, not a scored run).

**M46-13** · class `landing` · evidence: the counter promises "nothing in the lane is" written
(`quality/counters/c1-r46-devices.py:9`), while `load_model()` imports the pinned reference through `importlib`
(`spec.loader.exec_module(mod)`, `:99-101`) with no bytecode guard (`dont_write_bytecode`/`PYTHONDONTWRITEBYTECODE` absent,
`receipts/senttool-verify.txt`), so CPython writes
`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc` — 40172 B, present in the frozen tree
(2026-10-26 17:23), hidden from `git status` by `.gitignore` · captured-by: **none** (criteria 13 and 63 govern
committed evidence, not a counter's own writes into the tree it scores) · fix: `sys.dont_write_bytecode = True` plus
`PYTHONDONTWRITEBYTECODE=1` in every env, and load the model with `compile(pinned_bytes, …)` + `exec` instead of
`importlib`. Shown able to fail: a tree observable of the two directories around one scoring run — today the run
gains a `.pyc` (the file is already there), after the fix it gains none; the red is visible in the frozen tree, the
green is not run here.

**M46-14** · class `scope` · evidence: clause i's isolation hides exactly three paths — `hidden_paths()` returns
`{realpath(repo), lane root, dirname(lane root)}` (`quality/counters/c1-r46-devices.py:241-243`) — so a scored tool
reaches `$HOME`, `/run/user/<uid>` and 25 sibling scratch dirs, and a unix socket on a `--ro-bind` is still
connectable: `sock_count=1`, `read_hypr_conf=yes`, `list_seat_scratch=25 other_seat_dirs_visible`, and `CONNECT_OK`
under both `--ro-bind` and `--bind` (`SentTool/evidence/sandbox-reachability.txt:6-10`, `socket-ro-bind.txt:3-5`)
`[seat receipt]` · captured-by: QUALITY 29's declared limit ("fail-closed setup is not containment") — clause i is
true as written and the safety sentence built on it is wider · fix: add `~` and `/run/user/<uid>` to `hidden_paths()`
so `sandbox()` tmpfs-mounts them (two lines, no contract change). Shown able to fail: the same reachability probe
under the fixed argv must print `sock_count=0` and `read_hypr_conf=no`; the red is the seat's receipt, the green is
not run here. The in-flight v2's allowlist root (no `/home`, `/run`, `/fast`; `:280-287`) is that fix in source form
(`receipts/c1-v2-carryover.txt`, a source reading, not a scored run).

## Applications of existing criteria (no new number)

- M46-1 and M46-10 → criteria 10 and 14 (a count is re-derived from its instrument; a census names both sets).
- M46-3 → criterion 65 (fixture lattice, one mutant per class).
- M46-4 → criterion 55 (a shape counter names the cribs that fake it); criterion 84 already covers pinning every
  receipt read and is the F7-shaped hazard one step over.
- M46-5 and M46-9 → criterion 24 (producer identity) and 79 (a pointer names a committed receipt).
- M46-6 → criterion 77 is adjacent but **does not catch it** (the identifier is in the other cited range); the
  non-author reading is the only instrument, which is why M46-6 is recorded as captured-by none.
- M46-7 → criterion 30 (precision evidence beside a recall claim).
- M46-8 → criterion 13 (evidence outliving a round is a committed path).
- M46-12 → criteria 56 (a clause that cannot fail under its own spec is dead code) and 67 (a read-only claim over
  every argv element — extended here to the *scored tool*); criterion 86 hides the judge, not the host.
- M46-14 → criterion 29's declared limit: fail-closed setup is not containment.
- M46-13 → no numbered criterion; a counter's own write into the tree it scores is the gap criteria 13/63 leave.

## Proposed QUALITY.md criteria (last numbered criterion in `corpus/QUALITY.md` is 86)

87. A control battery's receipt is complete or it is no evidence: every declared control is scored exactly once, a
    final verdict line is present, and a fixture addresses its mutation by row identity — never by a global string
    count over a corpus that legitimately holds the same value twice. A battery that aborts on its own precondition
    has produced no control evidence, whatever its exit code. Check: `python3 -I
    .ufo/waves/round-46/w1/ScrMistakes/check87.py --receipt <round>/receipts/ctl-c2.txt --controls 15` — it reads
    the receipt's `controls=` header, the distinct `CTL_* <NAME> want=` rows, the verdict line and the `ok`/`WRONG`
    marks. Shown able to fail: the committed receipt reads `verdict=PASS` (15/15); the aborted shape reads
    `verdict=FAIL scored=7 want=15 verdict_line=absent` (`.ufo/waves/round-46/w1/ScrMistakes/receipts/check87-run.txt`).
    (lesson: lessons/round-46.md#mistakes M46-2)

88. A counter that reads tree shape carries a committed forgery suite — revisions a reader rejects — and a
    tightening candidate is admitted only when the positive control passes every candidate and each **undeclared**
    admitted forgery fails the intended one (F5d fails two); a forgery the counter's own docstring declares is named as declared and not
    counted as a kill. Check: `python3 -I .ufo/waves/round-46/w1/ScrMistakes/check88.py --forge
    .ufo/waves/round-46/w1/CritC2Forgery/forge.out --tighten .ufo/waves/round-46/w1/CritC2Forgery/tighten.out
    --positive-rev 072da817379c2bdf5403ceca39e973301fc2d907 --declared F1,F2,F3,F9`. Shown able to fail: it reads
    `verdict=PASS` on the attack seat's own two receipts and `verdict=FAIL admitted_uncovered=F10,F4,F5d,F6,F7,F8`
    when only the positive control's candidate line is committed, and `FAIL admitted_passing=F1,F2,F3,F9` when no
    residual is declared (`.ufo/waves/round-46/w1/ScrMistakes/receipts/check88-run.txt`). The instrument is a seat
    instrument (provenance, not credit under criterion 25); the round registers the rule, the next round owns the
    lane instrument. (lesson: lessons/round-46.md#mistakes M46-4)

89. A harness that scores untrusted code contains it and tests "runs nothing" by execution: the live session's
    IPC endpoints, the user's home and peer scratch are hidden (tmpfs, not merely read-only — a unix socket on a
    read-only bind is still connectable), and the clause fails on any `execve` beyond the tool's own rather than on a
    PATH marker. Check: score the two committed bypass tools
    (`.ufo/waves/round-46/w1/SentTool/evidence/bypass-commits.txt`, revs `3d96dcd` and `ef072a7`) under the fixed
    harness and require `clause=r marker=present` / `readonly=fail`; the reachability probe must read
    `sock_count=0`. Shown able to fail: under the frozen harness both tools print `readonly=ok … verdict=TARGET_MET`
    (`.ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-*.txt`) and the probe prints `sock_count=1`. The
    green run is owed by the next counter; the seat receipts are provenance, not credit under criterion 25.
    (lesson: lessons/round-46.md#mistakes M46-12)

Candidate, not proposed for registration: the must-flag half of M46-7 (a detector credited with catching a class
carries a committed must-flag suite beside criterion 30's must-stay-clean negatives). Criterion 30 names the
negatives only; `CritW2Gate/repro.py` measures the positive side but is a seat instrument, and writing a lane
checker for "any detector, any suite" would move this round's target. Recorded as the gap M46-7 exposes.

Second candidate, not proposed: M46-13 (a tool's "writes nothing" claim measured by a before/after tree observable
rather than by its docstring). No lane instrument exists for "any counter, any write"; the row carries the red
state (the `.pyc` in the frozen tree).

## Conflicts recorded verbatim (for the canonical judge)

1. **False positives on the privacy gate, same revision, two readings.** `CritW2Gate.md:15` — "5 of 6 legitimate
   shapes are flagged" (documentation examples of the dump shapes, must-stay-clean) — against
   `ExecSessionTriage.md:47` — "False positives: **0**. Every match is a genuine dump-shaped object" (classified by
   provenance, synthetic vs real). Both measured at `4d22eeb`. The two seats count different populations (planted
   documentation examples vs the lane's existing findings); neither number refutes the other, and the lesson must
   name which population it quotes.
2. **Whether the anchor cell's shape read is a declared residual.** `CritC2Forgery.md:14` lists F6 (anchor cell
   naming the right file and the wrong lines) as **not** declared, while the counter's docstring says
   "registry cells 3-6 of a new row are not read except the scope cell" and then names the anchor ranges
   (`quality/counters/c2-r46-input-device-entry.py:72`). The seat reads "read" as "checked against the claim"; the
   docstring reads it as "parsed for range shape". The rule in M46-4's fix (candidate A) settles it for the next
   counter, not for this one.

## Routed items not mined as rows

- **D1** (round-45 ran 41 seats, below the 64-seat floor, and never ran its w2) — discharged in substance this
  round, not by a mistake row: the w2 ran. The round-45 tool holds under five fresh nonces and 22 hand-written
  adversarial configs (`ExecW2Monitors/c1-nonces.txt:10`, "fixtures=81/81 generated=150/150";
  `ExecW2Monitors/adversarial.txt:200`, "ADVERSARIAL: 22/22 match my reading of the pins") `[seat receipt]`; the
  w2's product is the entry's six non-supported sentence units (two mis-located, one wrong, three unpinned —
  `CritW2Entry.md:8-10`) of which M46-5 and M46-6 are two, and the gate's recall/precision picture (M46-7). The D1 lesson belongs in the closure section: a
  round that skips its attack wave ships citation defects its own counter cannot see.
- **D3's registry row** — `ExecSessionTriage` drafted the `SKILL.md` row (`skill-row.md`, `mado-session-material`
  shape) and the marker layer; the row is the L1's to land. Not a mistake row: the defect is recorded as M46-7's
  fix, and the registry row is a landing action.
- **D6** (S290-S297 supersession, carried twice) — drafted this round as S326-S333 by `ExecSupersede`
  (`ExecSupersede/rows.md`, eight rows, seven opening `supersedes S29N —`), census-clean on six mirror runs. Not
  mined as a row: the debt is already recorded in round-44 D6 and round-45 §6 item 6, and the draft is not yet
  landed. If it slips a third time it becomes a `landing` row with the age count the registration's considerthese
  proposal 3 asks for.

## Limits

- The pre-freeze V03 run (M46-3) has no committed receipt; I re-derived the post-freeze line and the separating
  fixture, not the pre-freeze verdict.
- `ExecW2Monitors` and `ExecSerialRule`/`ExecSupersede` were still writing when this draft was taken; their
  numbers are cited as seat receipts and must be re-read at the wave tip before the lesson lands.
- M46-7's lane census number is quoted from the attack receipt's own line (`files=17098 findings=102`); the seat's
  prose reports 97 findings at `e0be61e4`. The two runs are not reconciled here.
- The three C1-harness rows (M46-12/13/14) rest on `SentTool`'s committed bypass and reachability receipts; I
  verified the code facts (`c1-r46-devices.py:9`, `:99-101`, `:241-243`, `:251-257`, `:375`), the receipts' verdict
  lines and the `.pyc` in the frozen tree, but I did not re-run the two bypass tools or the probe.
- The in-flight `c1-r46-devices-v2.py` / `c1-r46-fixtures-v2.json` / `c2-r46-input-device-entry-v2.py` are untracked
  and were read, not scored; the v2 statements in M46-12/M46-14 are source readings at 17:57 and may change before
  the L1 freezes them.
- I did not run the C1 or C2 counters against the lane, the w2 counters at the round-45 tip, or any host probe
  beyond the reads the seat brief allows (`hyprctl monitors all -j` inside one in-process comparison for M46-10,
  value never written).
