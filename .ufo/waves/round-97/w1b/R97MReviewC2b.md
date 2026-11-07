# R97MReviewC2b -- reviewer attack on C2 (counter self-invocation), round 97 wave w1b

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision
`e6152b589c2c6a28426c28263c4bcc3c46398be4`. Scratch `/fast/scratch/hyaku/mado-r97/R97MReviewC2b`,
deleted before yield. Every probe is read-only against the lane; every fixture repository is a
`git clone --no-hardlinks` of the lane under scratch, committed only inside scratch
(`git -C <clone> rev-parse --show-toplevel` asserted equal to the clone before each commit). No lane
file was written by this seat; nothing was installed (no pacman/uv/npx activity). Status markers:
**[MEASURED]** = command + output in this file; **[INFERENCE]** = reasoning.

**Final state measured**: C2 landed as commit `65ff5591c40c13ae7686b30587d202086353c165` ("C2 lands the
two round-96 counters' --selftest mode, the C2 counter, the SKILL registry rows ..."), and the counting
command reaches **TARGET_MET** on it when the panel is the working tree's `87ba2f41…` (section 9). The
commit itself still carries the older w1-anchored panel `95f86861…` at both panel paths -- that is the one
remaining landing gap (F1b).

```
at 65ff5591:
  quality/counters/c1-r96-magictext.py         4f6783848ded9c63f934c68a24da856369895987651d0f66fdd6920f07aaa64d
  quality/counters/c2-r96-selftest-kills.py    54143b8a28f2be4b2f1361c443d32156a68fd088c7cdb9c9030ca7415002217b
  quality/counters/c2-r97-counter-selftest.py  abb17a019141c57635f1c9771ad449a4348dfdc75a0bb57af3776075fe06b879
  SKILL.md                                     fab1ff74944e9ecc3f9f4ef52e31e1af899ee9588a9c0a41ee29545ce3ce944e
  quality/tool-ledger.md                       fb0f2f3c818c81978fe35814697c44764a6b31796ea8baa0290406df7559d624
  .ufo/waves/round-97/selftest-fixtures-v2/    33 files (24 payload + pins.json + ...)
  controls/counter-selftest-panel*.json        95f86861… at HEAD (committed by 78e9ccdd, w1-anchored);
                                               the working tree holds 87ba2f41… (uncommitted)
working tree at 15:16:
  controls/counter-selftest-panel-r97.json     87ba2f4149ff5fbcd7dfe7179bc87b1bd50cd083867f736b62f02796cfa9b4ba
  controls/counter-selftest-panel-v2.json      87ba2f4149ff5fbcd7dfe7179bc87b1bd50cd083867f736b62f02796cfa9b4ba  (same bytes)
```

Base bytes for the diff legs: `quality/counters/c1-r96-magictext.py` sha `9d3e1e76…a42a7f7` (64752 B),
`quality/counters/c2-r96-selftest-kills.py` sha `2bd9e562…b4eb895` (20512 B). At base, `--selftest` on
either is an argparse usage error: rc 2, no `MADO_COUNTER_SELFTEST` line (measured in the runner's exact
form: `env -i PATH=/usr/bin:/bin HOME=… TMPDIR=… LC_ALL=C.UTF-8 python3 -I <copy> --selftest`, cwd = the
copy's dir). [MEASURED]

## 1. Item 1 -- strip the added block and diff against the base bytes

The counters carry no BEGIN/END markers; they document their own protocol in the block's header comment:
"delete everything from the marker line to EOF and append exactly `if __name__ == "__main__":` /
`    sys.exit(main())` to recover the base production bytes", where the marker line is
`# ===== mado counter self-invocation (added round-97 C2, seat R97MExecC2b) …`. I applied exactly that
protocol (marker cut + the two base lines re-appended) and diffed against `git show e6152b58:<path>`:

```
c1: block_lines=310  prod_added=0 prod_removed=0  IDENTICAL=True
c2: block_lines=288  prod_added=0 prod_removed=0  IDENTICAL=True
```

So at the landed bytes the production path is **byte-identical** to the base counter -- not merely
"behaviourally unchanged". Both files are ASCII-only (0 non-ASCII bytes). [MEASURED]

Counter-generation caveat, measured: the *other* selftest generation left on disk
(`build/c1-r96-magictext-selftest.py` sha `dd9b5a0b…`, `build/c2-r96-selftest-kills-selftest.py` sha
`d4689f5a…`, the dead w1 path) does **not** satisfy this: with its `# === MADO-COUNTER-SELFTEST-BEGIN ===`
markers stripped, 14 production lines remain added (the `--selftest` dispatch at the top of `main()` plus
the two argparse flags), `prod_added=14 prod_removed=0`, for both counters. Landing that generation would
falsify the declaration's "production path is byte-unchanged". It did not land. [MEASURED]

## 2. Item 2 -- `--selftest` green, then break the fixture three ways

Green, in the layout the runner builds (`<root>/quality/counters/<name>.py` +
`<root>/.ufo/waves/round-97/selftest-fixtures-v2/`, cwd = root, empty-ish env), on the landed bytes:

```
c1  rc=0  MADO_COUNTER_SELFTEST: checks=10 failed=0
c2  rc=0  MADO_COUNTER_SELFTEST: checks=10 failed=0
```

cwd-independence holds: the same green lines from cwd = the layout root, from cwd = `/`, and with
`--fixture-dir <tree>` / `--fixtures <tree>` (all four cells measured). Resolution order is the explicit
flag (terminal) then a walk from `__file__`; cwd is never consulted, and the hard-coded absolute lane path
that the w1 bytes carried is gone (the w1 probe that read the live lane now fails case A). [MEASURED]

Three-way break (one fixture tree, three breakages; `python3 -I <counter> --selftest`, cwd per case):

```
                         c1 (4f678384)                          c2 (54143b8a)
baseline (cwd=repo)      rc=0  checks=10 failed=0  ids=[]       rc=0  checks=10 failed=0  ids=[]
A rename fixture dir     rc=1  checks=10 failed=10 ids=ALL(10)   rc=1  checks=10 failed=10 ids=ALL(10)
B cwd=/tmp               rc=0  checks=10 failed=0  ids=[]       rc=0  checks=10 failed=0  ids=[]
C rename pins.json       rc=1  checks=10 failed=10 ids=ALL(10)   rc=1  checks=10 failed=10 ids=ALL(10)
A ids == C ids: True (both counters)
```

`ALL(10)` = st-fixture-dir, st-tool-pin, st-gate-target-met, st-result-line-format, st-scratch-clean,
st-setup-missing-input, st-setup-wrong-pin, st-setup-wrong-rev, st-target-missed-case,
st-target-missed-mutant. [MEASURED]

Reading: **A and C produce identical id sets on both counters** -- the stability property item 2 asks for
holds for fixture breakage. **B is green because nothing is broken**: moving cwd with the fixture tree
intact leaves the selftest green, which is correct cwd-independence, not a pass-through. If the sentence is
meant to demand failing ids from a cwd move as well, it is unsatisfiable for a counter that resolves
fixtures from `__file__`; the honest receipt wording is "a renamed fixture dir and a renamed pinned input
fail with the same 10 ids; a cwd move changes nothing".

## 3. Item 3 -- the frozen panel, a corrected panel, and stub substitution

### 3.1 Panel history (this is why the finding below changed twice) -- [MEASURED]

```
f380e7ef…  15:0x  r97 path, w1-era: 8 checks/counter, 3 broken rows with NO "counter" field,
                 expect_exit 2, expect_line = the RUNNER's vocabulary, duplicate ids
                 -> runner: SETUP_ERROR "broken row 'missing-input' malformed" (rc 2)
95f86861…  15:04  v2 path (R97MMutC2b's first freeze): 7 checks/counter, w1-era finds
                 -> 14/14 finds unique in the DEAD .py bytes, 2/14 in the landed bytes
                 -> with the .py pair: TARGET_MET; with the landed pair: SETUP_ERROR on the
                    mutated-tool path (c1-mutants.json not under the invoked root)
bc480ed1…  15:07  r97 path: still 7 w1-era checks, paths moved to c1/mutants-mini.json
                 -> would be TARGET_MISSED at negative_ids=2/14
729532a8…  15:13  both paths: 9 checks/counter, correctly anchored (negative_ids=18/18 measured),
                 but missing-input declared expect_exit 2 while the counter exits 1
                 -> TARGET_MISSED, broken_modes=4/6 (broken_c1=2/3, broken_c2=2/3)
87ba2f41…  15:15  both paths: 9 checks/counter, 6 broken rows all at expect_exit 1, all 18 finds
                 unique in the landed bytes -> TARGET_MET (section 9). Owner-confirmed: this is the
                 10-row set minus st-target-missed-case, same anchors (a strict subset).
```

The measured broken-mode facts that the final panel uses (reproduced with the runner's own constructions:
counter alone with `--fixture-dir <absent>`; full layout with every fixture file 0 bytes; full layout with
`\n# mutated-tool probe\n` appended to the named fixture):

```
c1  missing-input  rc=1  "FIXTURES: UNRESOLVED" + all 10 FAIL ids + checks=10 failed=10
c1  wrong-rev      rc=1  9 FAIL ids (all but st-fixture-dir) + checks=10 failed=9
c1  mutated-tool   rc=1  st-tool-pin only + checks=10 failed=1        (path c1/mado-mimetext.py)
c2  missing-input  rc=1  all 10 ids + checks=10 failed=10
c2  wrong-rev      rc=1  9 ids + checks=10 failed=9
c2  mutated-tool   rc=1  st-tool-pin, st-gate-target-met, st-result-line-format + checks=10 failed=3
                                                                     (path c2/dummy-tool.py)
```

Every broken mode exits **1**; none exits 2. The 729532a8 panel's `expect_exit=2` for missing-input is
exactly the mismatch that made it 4/6. [MEASURED]

### 3.2 A correctly anchored panel makes the landed pair TARGET_MET -- [MEASURED]

I also built a reviewer probe panel the way a panel should be built (one neutralisation per check id, each
`find` verified to occur exactly once in the landed bytes, each replacement verified to make that check
evaluate False, each application verified live to exit 1 and print
`MADO_COUNTER_SELFTEST_FAIL: <id>`): 8 checks per counter (all single-line `add(...)` calls;
`st-result-line-format`'s call spans two lines and my single-line generator could not build a clean
neutralisation for it). On a scratch clone of the landed bytes it reached `TARGET_MET` with
`negative_ids=16/16 broken_modes=6/6 stub_uncredited=16/16 registry=1->3 ledger_members=2/2`. That run is
what separated "the runner is broken" from "the panel is mismatched": the runner was never broken.

### 3.3 Stub substitution -- the structural clauses catch a no-work counter -- [MEASURED]

Fixture: the same landing-shaped clone, but `quality/counters/c2-r96-selftest-kills.py` replaced by a stub
that prints `MADO_COUNTER_SELFTEST: checks=8 failed=0` and exits 0 without running a check (the panel
`find` strings embedded verbatim as comments so each still occurs exactly once). Same panel, same runner:

```
selftest c1 rc=0 checks=10 failed=0 green=True
selftest c2 (stub) rc=0 checks=8 failed=0 green=True          <-- the stub passes leg (i)
SURVIVED … st-tool-pin / st-gate-target-met / st-scratch-clean / st-setup-missing-input /
           st-setup-wrong-pin / st-setup-wrong-rev / st-target-missed-case / st-target-missed-mutant
MADO_COUNTER_SELFTEST_COUNT: TARGET_MISSED … negative_ids=8/16 broken_modes=3/6
broken_c1=3/3 broken_c2=0/3 base_refuse=ok stub_uncredited=16/16                       rc=1
```

The stub **passes the green leg on its own printed line** and is caught by (ii) (`negative_ids=8/16`, all
eight c2 neutralisations SURVIVED) and by (iii) (`broken_c2=0/3`: a no-work counter cannot fail its broken
scenes). That is the structural catch the seat asks to confirm; it lives in (ii)+(iii), never in (i), so a
green result line alone must never be read as evidence of a real selftest. [MEASURED]

## 4. Item 4 -- registry and ledger re-derived

Registry, with the counter's own derivation (a line whose first non-blank character is `|` that contains
the artifact path), at `git show e6152b58:SKILL.md` (sha `6a8754df…`, 469 table rows):

```
tools/mado-mimetext.py                              rows=1  (line 887)
quality/counters/c1-r96-magictext.py                rows=0
quality/counters/c2-r96-selftest-kills.py           rows=0
quality/selftest-kills/check-receipt-presence.json  rows=0
TOTAL named-artifact rows = 1
```

At the landed revision `65ff5591` (`SKILL.md` sha `fab1ff74…`, 475 table rows):

```
tools/mado-mimetext.py                              pairs=2  (887 its own row, 2973 the mado-filetype row
                                                             names it as a neighbour dependency)
quality/counters/c1-r96-magictext.py                pairs=1  (2975)
quality/counters/c2-r96-selftest-kills.py           pairs=1  (2976)
quality/selftest-kills/check-receipt-presence.json  pairs=3  (879 amended strength row, 2976 the c2
                                                             counter row's prose, 2977 its own gate row)
artifacts covered = 4 (3 instruments + the kill-set)
```

The declaration was revised at 14:24 to count **three instruments** (the kill-set is "a pinned input named
inside the existing `mado-selftest-strength` row's population, not a registry row" -- R97MCritic C2-2) and
to move **1 -> 3**. Both numbers are right under that derivation: base 1 (`mado-mimetext`), after 3 (plus
the two counters). The landed run prints `registry=1->3` and the per-artifact pair counts above. [MEASURED]

The pair-count hazard is real and measured: the landed `SKILL.md` names the kill-set JSON three times, and
would name it twice under the four-artifact form -- which is why the covered-count derivation was adopted.
I built the four-artifact after-state from the base `SKILL.md` plus the scribe's draft rows and amendment
in scratch: `TOTAL=5` pairs over 4 artifacts, kill-set `rows=2` (line 879 amended strength row, line 3000).

Ledger membership:

```
git show e6152b58:quality/tool-ledger.md | grep -n -E 'c1-r96-magictext|c2-r96-selftest-kills'
  225:| `quality/counters/c1-r96-magictext.py` | Read-only C1 counter (round 96): …
  226:| `quality/counters/c2-r96-selftest-kills.py` | Read-only C2 counter (round 96): …
python3 -I quality/check-tool-ledger.py --repo . --rev e6152b58
  LEDGER: population=188 ledger_rows=188 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 \
          verdict=TARGET_MET rev=e6152b589c2c6a28426c28263c4bcc3c46398be4     rc=0
at 65ff5591: population=191 ledger_rows=191 uncovered=0 … verdict=TARGET_MET  (the +3 are the round-97
                                                                              instruments)
```

Both counters satisfy `is_population` (`quality/counters/[^/]+\.py`, check-tool-ledger.py:172-175) and
both are ledger rows at base and at the landed revision, with resolving pointers. **Clause (v) is an
invariant, not a movement**: it is true before and after C2. The runner reads the ledger at `--rev`
(`ledger row <path> present=True`, `ledger_members=2/2`) and separately runs the gate
(`uncovered=0`). [MEASURED]

Unrelated working-tree edit: `quality/tool-ledger.md` changes `tools/mado-mimetext.py` "`--selftest` 20
checks" to "50 checks". The correction is right (the tool is byte-identical to base, `d5f174fc…b857cbd`,
and prints `MADO_MIMETEXT_SELFTEST: checks=50 failed=0`), but it is outside C2's declared change and
outside this seat's write scope. [MEASURED]

## 5. Item 5 -- clause-by-clause falsifiability of PRED-C2-r97-v1

| clause | falsifiable? | how I falsified it, and what it returned |
|---|---|---|
| (i) both `--selftest` green, `failed=0`, rc 0, `checks >= 6` each | yes | run each counter the way the runner does (layout root, empty-ish env) and parse the result line: `checks=10 failed=0` rc 0 for both on the landed bytes; base bytes give rc 2 with no line. A renamed fixture dir / renamed pinned input turns it red with 10 FAIL ids (section 2). A stub that prints the line passes it (3.3). |
| (ii) every frozen neutralisation flagged with its declared id (`negative_ids == panel`) | yes | apply `find`->`replace`, rerun, require rc 1 and a line-anchored `MADO_COUNTER_SELFTEST_FAIL: <id>`. Landed bytes + final panel: 18/18. Reviewer panel: 16/16. Intermediate panels: 18/18 (729532a8) and 2/14 (the w1-anchored ones). Stub substitution: 8/16 (3.3). |
| (iii) every broken mode carries its counter, >=3 per counter, declared id + exit 1 or 2 (`broken_modes == broken`) | yes | the runner validates `counter`/mode/exit and runs the row against its own counter. Final panel: 6/6 (3/3 per counter) at rc 1. The 729532a8 panel: 4/6 because it declared `expect_exit=2` for missing-input. The f380e7ef panel: SETUP_ERROR at validation. |
| (iv) controls: base bytes refuse (rc 2, 0/2 green); a stub printing the result line and every panel id is credited with none (`stub_uncredited=<panel>/<panel>`); registry 1 -> 3 re-derived at `--base-rev` and `--rev` | yes | base refusal measured (`rc=2 green=False` twice); `stub_uncredited=18/18` measured on the landed run; registry 1 -> 3 measured at both revs (section 4), and 1 -> 4 under the four-artifact form. |
| (v) both counters are ledger rows at `--rev` (`ledger_members=2/2`) and the gate prints `uncovered=0` | yes, but it is an invariant | measured true at base and at the landed rev (section 4); it cannot separate C2 from do-nothing and should stay declared as "stays covered, population +0". |

Clause wording that does not match the measured vocabulary (declaration edits still needed):

- (iii) says "makes that counter print its declared `SETUP_ERROR`/`TARGET_MISSED` id and exit 1 or 2".
  The counters print `MADO_COUNTER_SELFTEST_FAIL: <st-id>` at rc 1 in all three broken scenes, and the
  missing-input scene additionally prints `checks=10 failed=10`. `SETUP_ERROR` is the *runner's*
  vocabulary and `TARGET_MISSED` is the *counter's production* verdict; neither appears in the selftest's
  broken-mode output. Restate as "prints its declared FAIL id at exit 1 or 2".
- The C2 section's "Before -> after" paragraph still ends "registry 0 -> 4 rows", contradicting the
  revised predicate's `1 -> 3`.
- Change (1) still says fixtures are "committed under `.ufo/waves/round-97/selftest-fixtures/`"; the
  landed pair uses `selftest-fixtures-v2/` (and the old tree is still on disk -- see F7).

## 6. Findings by severity

**HIGH**

- **F1a -- panel anchoring: RESOLVED at 15:15.** The panel now at both paths (sha `87ba2f41…`) has 9
  checks per counter, all 18 finds unique in the landed bytes, 6 broken rows at `expect_exit=1`; the
  landed run is `TARGET_MET` (section 9). The earlier states were genuinely broken and are recorded in
  3.1 because they show what a mismatched panel does: `f380e7ef` -> SETUP_ERROR; `95f86861`/`bc480ed1`
  -> 2/14 finds in the landed bytes; `729532a8` -> 18/18 neutralisations but 4/6 broken rows
  (`expect_exit=2` for missing-input).
- **F1b -- the landed commit pins the WRONG panel (blocking for the receipt).** At `65ff5591` both
  panel paths hold `95f86861…` (committed by `78e9ccdd`, the w1-anchored panel: 7 checks per counter, 2 of
  14 finds in the landed bytes), while the working tree holds the correct `87ba2f41…` (9 checks per
  counter, 18/18 finds). A replay from a clean checkout of `65ff5591` therefore scores SETUP_ERROR /
  TARGET_MISSED; only a checkout that also carries the uncommitted working-tree panel reaches
  `TARGET_MET` (section 9). The L1 must commit `87ba2f41…` (or its successor) and pin that sha in the
  freeze.
- **F2 -- declaration/implementation wording drift.** (iii)'s "SETUP_ERROR/TARGET_MISSED id" and the
  stale "registry 0 -> 4" sentence do not describe the measured behaviour (section 5). The predicate
  sentence is the contract; it must be rewritten before the freeze, not after.
- **F3 -- artifact flux.** The counters changed at least four times
  (`03096af2`/`86e0e260` -> `9f24dee0`/`19d5952a` -> `4f678384`/`54143b8a`), the runner five times, and
  the panel five times in ten minutes (`f380e7ef` -> `95f86861` -> `bc480ed1` -> `729532a8` ->
  `87ba2f41`). Every change invalidates every pin; the freeze must pin the final bytes or the receipt
  will not replay.

**MEDIUM**

- **F4 -- the dead `.py` generation does not satisfy item 1.** Stripped of its marked block it leaves 14
  production lines (dispatch + argparse) per counter; "production byte-unchanged" is false for it. It is
  still on disk next to the landed pair; a directory-wide landing would take it.
- **F5 -- `wrong-rev` is not a revision stimulus.** The mode truncates every fixture file to 0 bytes and
  runs `--selftest`; the counter is never given a revision. Measured rc 1 / 9 ids. The receipt must name
  the stimulus as "zero-length fixtures".
- **F6 -- `ledger_members` is a substring test.** `any(p in ln for ln in ledger_text)` counts a row that
  merely mentions the path in prose (the landed c2 counter row names the kill-set, which is why the
  kill-set's pair count is 3). The gate's `uncovered=0` is the real membership proof.
- **F7 -- two fixture trees on disk.** `selftest-fixtures/` (8 files, w1 layout; its 14:35
  `hostdb-manifest.json` pointed `source.dir` at `c1/hostdb` while the files live in `c1/hostdb/mime`,
  which made the c1 selftest red until 14:37) and `selftest-fixtures-v2/` (33 files incl. `pins.json`,
  landed). Only the latter belongs to the landed pair.

**LOW**

- **F8 -- exact line formats.** Green requires `^MADO_COUNTER_SELFTEST: checks=N failed=0$` and no
  `MADO_COUNTER_SELFTEST_FAIL:` anywhere; a failing check requires
  `^MADO_COUNTER_SELFTEST_FAIL: <id>\s*$` with the id terminal. Trailing prose on either line fails every
  leg silently.
- **F9 -- `--min-checks`.** The runner accepts `--min-checks N` (default 6). The published counting
  command must not pass it.
- **F10 -- registry derivation is fence-blind.** It counts `|`-lines inside ``` fences too. `SKILL.md`
  has 0 fenced table rows today, so this is latent, not live.

## 7. Residual risk and verification gaps

- **The neutralisation set is the wave's design set.** My 16 neutralisations are reviewer-built
  (force-each-check-false) and prove the ids are reachable; they do not prove the frozen panel's
  *weakenings* are semantically meaningful. The panel's 9-per-counter set (owner-confirmed as the 10-row
  design minus st-target-missed-case) was verified for uniqueness and for the declared broken-mode ids,
  not for semantic depth; the dropped id means st-target-missed-case has no neutralisation in the frozen
  panel. Owner-confirmed composition: 8 rows per counter edit the artifact's own `_ST_*` anchors, and
  `st-fixture-dir` uses `add("st-fixture-dir", False)` because its anchor (`_ST_PINS_REL`) cascades to all
  ten checks -- so 2 of the 18 rows are forced-false edits that prove the id is reachable, not that the
  check detects a real fault.
- **`st-result-line-format` has no neutralisation from my generator** (its `add(...)` spans two lines);
  the frozen panel carries one.
- **Mini runs are not production runs.** The counters' selftests rebind census floors (`MIN_CASES=2`,
  `MIN_HOST_PATHS=3`, `HOST_DB_FILES=2`, ...) and build tiny temp repos; they exercise the production
  code paths at fixture scale, not the round-96 scoring run. The declaration's named limit says this.
- **Cost.** One full runner pass over a 18-row panel takes ~1.5-7 minutes on this host depending on the
  panel size and the mini-run cost; the freeze's measurement should budget for it.
- **Base-revision availability.** The runner's base control needs `e6152b58` to be an object in the
  measuring repo; a shallow clone without it makes the leg `SETUP_ERROR` (correct, but the replay
  environment must be a full clone).

## 8. Artifact flux log (shas seen on disk)

```
14:00  c1 .py e492c46d / cc39301e / 377a34fe / dd9b5a0b   c2 .py 2bd9e562(==base) / 861883b3 / d4689f5a
14:34  c1 .v2 af3ac3b7                                   c2 .v2 205693ae
14:38  c1 .v2 03096af2                                   c2 .v2 86e0e260
14:42  c1 .v2 9f24dee0                                   c2 .v2 19d5952a
14:52  c1 .v2 4f678384 (frozen, landed)                  c2 .v2 54143b8a (frozen, landed)
15:03  commit 65ff5591 lands the counters, the runner, SKILL.md, the ledger row
runner: 5bb9a8b6 (w1) -> e46d50e6 -> 45847d4b -> 291d7087 -> abb17a01 (landed)
panels: f380e7ef -> 95f86861 -> bc480ed1 -> 729532a8 -> 87ba2f41 (both paths, 15:15)
```

## 9. End-to-end verification at the landed revision -- [MEASURED]

Clone of `65ff5591` in scratch (full history, so `--base-rev e6152b58` resolves), runner
`build/c2-r97-counter-selftest.v2.py` (sha `abb17a01…`), panel `87ba2f41…`, every pin as listed in the
header:

```
MADO_COUNTER_SELFTEST_COUNT: TARGET_MET pred=PRED-C2-r97-v1 rev=65ff5591c40c13ae7686b30587d202086353c165
  base=e6152b589c2c6a28426c28263c4bcc3c46398be4 counter_pin=ok,ok selftest_green=2/2 checks=10,10
  negative_ids=18/18 broken_modes=6/6 broken_c1=3/3 broken_c2=3/3 base_refuse=ok always_ok_flagged=0
  stub_uncredited=18/18 registry=1->3 ledger_members=2/2 ledger_uncovered_ok=True     rc=0
```

with every broken row `rc=want=1 line_ok=True ok=True`, `base-control … rc=2 green=False` twice, the
per-artifact registry pairs `mimetext base=1 rev=2`, `c1 base=0 rev=1`, `c2 base=0 rev=1`,
`registry artifacts covered base=1 rev=3`, and `LEDGER: population=191 ledger_rows=191 uncovered=0
dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=65ff5591…`.

The same command with the intermediate panel `729532a8…` returned `TARGET_MISSED` with
`negative_ids=18/18 broken_modes=4/6` -- the only difference being `expect_exit=2` on the two
missing-input rows (the counters exit 1). That is the whole margin between MISSED and MET at this
revision, and it is a panel declaration, not a counter or runner defect.

## Report

Report: .ufo/waves/round-97/w1b/R97MReviewC2b.md
