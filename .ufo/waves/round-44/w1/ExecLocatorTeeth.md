# w1 ExecLocatorTeeth — the locator checker's numbers and its 12 surviving mutants (closure D6)

**Verdict: candidate successor delivered and measured.** `.ufo/waves/round-44/w1/ExecLocatorTeeth/check-locators.py`
(sha256 `66e048338cfcc10adce824f3d32f75735c9e683e131af70dd684d71d5c7643a9`, 482 lines, stdlib only) keeps the CLI and
every output line shape, compares numeric atoms as well as identifiers, and kills **36 of 37** MutCheckLocators mutants
(pristine: 25). The one survivor is `no-re-escape`, proven equivalent by construction and by enumeration (554,079 tokens,
0 differences). On the mandated prose the two checkers are **byte-identical** (`diff` 0 bytes); on a 125-file census
also 0 bytes. The lane file was not touched.

## 1. Target, baseline, and the reproduced mutation baseline

Closure D6 (`corpus/lessons/round-43-verifier-spotcheck.md` §6): "`quality/check-locators.py` compares identifiers, not
numbers, and 12 of 37 of its mutants survive its selftest." The lane file is byte-identical to the round-43 data-commit
bytes: `sha256sum quality/check-locators.py` → `c1ea52ad5db21fdf81022d0425e7cad42fc3e34dd5083915b127a46ab948a27e`,
copied verbatim to `pristine.py` in this seat dir.

Baseline (`python3 -I pristine.py --selftest`, `selftest-baseline.txt`): `SELFTEST: cases=18 passed=18 locators=19
miss=6` / teeth `flips=11 ok_to_miss=4 miss_to_ok=5` / `SELFTEST: PASS`, rc 0.

The mutant set is **not retyped**: `mutrun44.py` imports the 37 `(name, category, pattern, replacement)` triples from the
frozen round-43 harness `.ufo/waves/round-43/w2/MutCheckLocators/mutrun.py` (`spec_from_file_location`, read-only) and
applies each with `re.subn(..., count=1)`. Two detectors per mutant, compared against the *same base's own* output:
D1 `--selftest`, D2 the round-42 LOG control (`git show a35cfdf:LOG.md` → `LOG-r42.md`, sha256
`f6c27a3650c7bf4b7f95688978b2979d2c9a39f262686525352c63ae8bc416e2`, 2483 lines; `--fetch .ufo/waves/round-42/fetch`).
Reproduction on pristine: `pristine: 37 mutants, 25 killed, 12 survived` with the round-43 survivor list verbatim
(`out/matrix-pristine.tsv`, `out/BASE-pristine.*`, `mutrun-pristine.txt`) — the harness is faithful before it is used.

## 2. What the candidate changes

Path: `.ufo/waves/round-44/w1/ExecLocatorTeeth/check-locators.py`. Unchanged: `--fetch DIR`, `--selftest`, `--explain`,
positional prose, exit 0/1/2, and the line shapes `LOC <file>:<n> <locator> fragments=<k> supported=<j>
verdict=OK|MISS|NOFRAG`, `CHECK_LOCATORS: locators=<n> miss=<m>`, `SKIP/ATTR/FRAG`. `--help` differs only in
`sys.argv[0]` (`usage: pristine.py …` vs `usage: check-locators.py …`).

1. **Numbers are compared** (`NUM_RE` :71, `fragment_numbers` :121, `number_occurs` :126, candidates carry them :148,
   support is AND-ed with the numeric test :172). A numeric atom must occur as a whole number — `(?<![0-9])N(?![0-9])` —
   in the union of the cited lines, so `set_default_size(640, 720)` is not supported by `420, 500`.
2. **Candidacy is unchanged**: a fragment still needs an identifier token (`` `:448` `` pointers and bare numbers stay
   unscored — declared limit, §6). This is also what keeps `id-re-digit-lead` observable (§3). The boundary expression is
   the one the round-43 prototype used for its C4 (`patchedcheck.py:127-128`, same `(?<![0-9])N(?![0-9])`); unlike that
   prototype this candidate applies it to every same-line fragment, so `supported=<j>` keeps its documented meaning, and
   it adopts **none** of the prototype's C1/C2/C3 tightenings — those change landed verdicts and are L1 policy (§6).
3. **Case table 18 → 32** (`CASES`, 14 new cases), each one the round-43 survivor's own distinguishing input:
   `` `epsilon` at `rec.cpp:9` `` (receipt's last line), `` `foo` at `rec.cpp:2` `` (3-char floor from above),
   `` `lpha` at `rec.cpp:2` `` (lower boundary), `` `alpha`rec.cpp:2 `` and ``rec.cpp:2`alpha` `` (flush attribution both
   sides), ``value `123` at `plain.conf:2` `` (digit-led token), `-rec.cpp:2` and `` `alpha` at rec.cpp:2x `` (locator
   look-behind/look-ahead), plus six numeric cases (`420/500` OK vs `640/720` MISS, the red-before line MISS, its
   corrected form OK, `width 4200` OK vs `width 420` MISS).
4. **The teeth bars and the tally are probed** — a bar that no input can reach is a latent mutant, so each bar is now
   callable and asserted on a degenerate input: `_table_short` :334 (bar `if k != ok or k < 12:` :336) with probes :360
   and :362; `_teeth_broken` :340 (bar `if flips == 0 or ok_to_miss == 0 or miss_to_ok == 0:` :342) with probes :403,
   :405, :407; the tally line is read back from `main()`'s stdout and compared :420-423.
5. `--explain`'s `FRAG` line lists identifier tokens **then** numeric atoms (:193) — same line shape, and a numeric MISS
   is now diagnosable.

## 3. Kill counts, before and after

`python3 -I mutrun44.py pristine pristine.py` → `37 mutants, 25 killed, 12 survived`.
`python3 -I mutrun44.py successor check-locators.py` → `37 mutants, 36 killed, 1 survived: no-re-escape`
(`mutrun-pristine.txt`, `mutrun-successor.txt`, `out/matrix-{pristine,successor}.tsv`, full table `matrix-delta.md`).

Eleven mutants that survived the shipped selftest are now killed, **all by a selftest assertion** (no new crash-kills):
`range-slice-offbyone`, `token-len-4`, `token-lower-boundary`, `attr-before-inclusive`, `attr-after-exclusive`,
`id-re-digit-lead`, `locator-no-lookbehind`, `locator-no-lookahead`, `summary-swapped`, `teeth-one-direction`,
`selftest-min-cases-dropped`. Observed failure text (`out/successor-<mutant>.selftest.txt`):

- `summary-swapped` — `SELFTEST: FAIL tally line expected 'CHECK_LOCATORS: locators=31 miss=11' got ['CHECK_LOCATORS: locators=11 miss=31']`
- `teeth-one-direction` — `SELFTEST: FAIL teeth: the flip bar must refuse a one-directional table`
- `selftest-min-cases-dropped` — `SELFTEST: FAIL teeth: the table bar must refuse a 5-case table`
- `range-slice-offbyone` — `SELFTEST: FAIL miss count expected 11 got 14`
- `id-re-digit-lead` — `SELFTEST: FAIL miss count expected 11 got 12`

**No regression:** all 25 previously killed mutants are still killed, and `summary-dropped` is now killed by the selftest
as well as the control. The mutants killed by a traceback (`cited-offbyone`, `comma-to-semicolon`, `nofrag-renamed`,
`resolve-always`, `selftest-allows-args`, `verdict-lowercase-ok`, `verdicts-regex-nofrag`) are the *same seven* as in
round 43 (`grep -l Traceback out/*.selftest.txt out/*.control.txt` over both seats) — inherited, not introduced.

**The one survivor is equivalent, not unasserted.** `no-re-escape` replaces `re.escape(tok)` with `tok` in
`token_occurs`; `token_occurs` receives only `fragment_tokens` output (ID_RE matches, strings over `[A-Za-z0-9_]`) and
`fragment_numbers` output (strings over `[0-9]`). `equiv-no-re-escape.py` (rerunnable) enumerates
`[A-Za-z0-9_]{1,3}` exhaustively (254,079) plus 300,000 random tokens of length 4-24, and scans 392,239 ID/num matches
of the lane's prose and its round-43 pins: `re_escape_differs=0 pattern_differs=0 non_word_char=0` →
`EQUIV no-re-escape: PROVEN EQUIVALENT` (`equiv-no-re-escape.txt`). No input can distinguish the mutant, so no case can
kill it; killing it would need a token alphabet with regex metacharacters, i.e. a different contract.

## 4. It can fail: red-before on a line the old checker passes, green after

Two real prose lines of the landed round-43 entry, each in a wrong-number and a corrected form (four inputs, eight runs;
all in this seat dir).

| input (derived from) | old checker | successor |
|---|---|---|
| `red-before.md` = entry `:62` with `set_default_size(640, 720)` | `…fragments=3 supported=1 verdict=OK` / `CHECK_LOCATORS: locators=1 miss=0` / rc 0 | `…fragments=3 supported=0 verdict=MISS` / `locators=1 miss=1` / rc 1 |
| `red-after.md` = entry `:62` verbatim (`420, 500`) | `verdict=OK`, rc 0 | `verdict=OK`, `locators=1 miss=0`, rc 0 |
| `red-before-rule.md` = entry `:32` with `size 640 720` | `host-gkeep.conf:4 … verdict=OK`, rc 0 | `…verdict=MISS`, `locators=1 miss=1`, rc 1 |
| `red-after-rule.md` = entry `:32` verbatim (`size 420 500`) | `verdict=OK`, rc 0 | `verdict=OK`, rc 0 |

Observed failure text (verbatim, `red-before.new.txt`):
`LOC .ufo/waves/round-44/w1/ExecLocatorTeeth/red-before.md:1 gkeep-ui-excerpt.py:33-34 fragments=3 supported=0 verdict=MISS`
/ `CHECK_LOCATORS: locators=1 miss=1`, rc 1.

**The round-43 M1 attack now dies.** `mut-entry-m1.md` is the whole entry with the two central numbers changed
(`size 640 720`, `set_default_size(640, 720)`; the exact attack CritLocatorGate ran): old `CHECK_LOCATORS: locators=11
miss=0`, rc 0; successor `locators=11 miss=2`, rc 1, both MISSes at the mutated lines (`mut-entry-m1.old.txt`,
`mut-entry-m1.new.txt`).

**CritLocatorGate's own numeric counterexamples now MISS too** (`.ufo/waves/round-43/w2/CritLocatorGate/adv-real.md`,
its A5/A6 "FALSE-OK numbers" inputs, run against the round-43 fetch): old `locators=11 miss=1`; successor
`locators=11 miss=3`, the two new MISSes being `adv-real.md:11 gkeep-ui-excerpt.py:33-34 supported=0` and
`adv-real.md:12 host-gkeep.conf:4 supported=0` (`adv.old.txt`, `adv.new.txt`).

## 5. The mandated runs: `LOG.md` + `corpus/knowledge/hyprland-gkeep-geometry-r43.md`

Command (both checkers, same `--fetch`):
`python3 -I <checker> --fetch .ufo/waves/round-43/fetch LOG.md corpus/knowledge/hyprland-gkeep-geometry-r43.md`

- old: `locators=16 miss=3`, rc 1 (`run-mandated.old.txt`)
- successor: `locators=16 miss=3`, rc 1 (`run-mandated.new.txt`)
- `diff -u` → **0 bytes** (`run-mandated.diff`, `run-mandated.rc.txt`: `old_rc=1 new_rc=1 diff_rc=0 diff_bytes=0`).

So no landed verdict changes: the three MISSes are `LOG.md:2483` (the round-42 text, real and permanent by append-only),
`LOG.md:2494` (the bullet that *quotes* the wrong `Hyprland-WindowRuleApplicator.cpp:426` locator, so its `SExpressionVec2`
fragment is correctly absent from :426) and `LOG.md:2495` — the last is a **real landed defect, not a checker limit**: it
attributes `setBox` to `Hyprland-GeometricMovableAnimated.cpp:45`, where the pin has
`    *m_realSize     = x.size();`, while `setBox` is declared at `:43` (`grep -n setBox
.ufo/waves/round-43/fetch/Hyprland-GeometricMovableAnimated.cpp` → `43:void CGeometricMovableAnimated::setBox(...)`).
Both checkers report it; neither creates or fixes it — it is worth routing to the L1 as a round-44 closure item.

Wider no-harm census (125 files: `SKILL.md`, `LOG.md`, `PROVINCE.md`, `corpus/knowledge/*.md`, `corpus/lessons/*.md`):
old `locators=51 miss=14`, successor `locators=51 miss=14`, `diff` **0 bytes** (`run-wide.{old,new}.txt`,
`run-wide.diff`, `run-wide.rc.txt`). The numeric rule therefore fires only where a number is actually wrong — no landed
line regresses.

## 6. Declared limits and risks (not fixed here)

- **Bare numbers and `:N` pointers are not fragments.** `` `:448` `` (a continuation pointer) and `` `640` `` (no
  identifier) stay unscored, so a numeric fact written as a bare backticked number is still unchecked. Making them
  fragments would create false MISSes on the lane's pointer style (`LOG.md:2487` writes `` `:448` `` for the *previous*
  locator's file), so the limit is deliberate; a `--explain`-only `weak=` bucket is an L1 policy call, not code.
- **Numbers inside identifiers** are extracted as digit runs (`m_realSize2` yields `2`), which is safe (the identifier's
  own occurrence carries the digit) but means a fragment `x500` requires a standalone `500`; measured: no lane line
  affected (§5 census).
- **Everything CritLocatorGate reported that is not D6 remains open**: statement-as-token-set (argument order,
  `FullMatch(*m_regex, other)` vs `FullMatch(other, *m_regex)`), locators past EOF passing as `NOFRAG`, sibling
  file-name/pointer fragments being used as fragments, coverage 2.1 %, and criterion 77's own contradiction
  (`corpus/QUALITY.md:401` says `NOFRAG` is not a pass while the command exits 0 over it). This candidate changes none of
  them; criterion 77's text and the `weak=` policy need the L1.
- **A paraphrased number can false-MISS** (backticked "4 clients" against a cited line that spells "four"). Measured
  effect on the current 125 files: none.
- **The successor is not installed.** `quality/check-locators.py` is the L1's to replace; its sha256 is unchanged at
  `c1ea52ad…` (verified after all runs).

## 7. Files in this seat dir, safety, tools

Files: `check-locators.py` (candidate, `66e0483…`), `pristine.py` (`c1ea52ad…`), `mutrun44.py` (harness, imports the
frozen round-43 mutant set), `out/` (BASE + 37×2×2 detector outputs for both bases, two `matrix-*.tsv`),
`matrix-delta.md`, `mutrun-{pristine,successor}.txt`, `equiv-no-re-escape.py|.txt`, `selftest.txt`,
`selftest-baseline.txt`, `LOG-r42.md` (`f6c27a3…`), `red-before*.md|red-after*.md` + `.old.txt`/`.new.txt` receipts,
`mut-entry-m1.md` + receipts, `adv.old.txt`/`adv.new.txt` (the round-43 adversarial inputs), `run-mandated.*`,
`run-wide.*`.

Safety: writes only to `.ufo/waves/round-44/w1/ExecLocatorTeeth/` and `/fast/scratch/hyaku/mado-r44/ExecLocatorTeeth/`
(deleted at close; mutant sources were written there and removed per run). Read-only git only (`git show
a35cfdf:LOG.md`); no index, no commit, no jj. No pacman, no host-service or compositor verb, no Wayland client. No
subagents. Tools installed: none — Python 3.14.8 stdlib only, which is the checker's own contract.
