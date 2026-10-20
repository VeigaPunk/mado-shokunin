# CriticC3W2 — partial: the 6/6 value is admissible as the pre-registered counter reading, but not as a recall capability; the row must say "6/6 on the drafts' 6-line training set; 5/6 without the rule-B guess; 0 held-out package_query positives", and rule B is acceptable only as a lead heuristic with two cheap corrections

Seat `MadoR19.CriticC3W2` (critic, leaf). Scope: rule on C3 at tip `01b80946d92b26370d3012a7da655d00dd135154`
given CriticC3 (w1) overfit critique, and on HelperFn rule B. Worktree = tip for `tools/mado-tripwire.py`,
`.ufo/waves/round-19/frozen`, `tw-recall.py` (`git diff --quiet 01b8094 -- …` → `worktree-equals-tip`).
Scratch only under `/tmp/critc3w2/` (`tip.py` = tip blob `367be947…`, `base.py` = `17661e0` blob `c1ae45a7…`,
`tipnob.py` = tip with the one rule-B line replaced by `pass`, `tipfix.py` = tip with the narrowing in §4,
`fx/dc-*.jsonl` = 12 adversarial fixtures, `corpus.py` driver). No lane edit except this report; no git write,
no jj, no host command.

## Ruling (short)

1. **The number reproduces and is honestly measured.** `tw-recall.py 01b8094` → `detected 6 / 6`,
   `tool_sha256 367be947…`; `tw-recall.py 9c54c56` → `3 / 6`, `c1ae45a7…`. Counter unchanged since
   pre-registration (sha `22090298…` in both receipts).
2. **All three round-evidence companions hold under independent re-run** (§1): class of every former miss
   equals the note-derived class; 0 findings on the 20 control lines; whole-corpus base→tip lost = 0.
3. **But the companions do not cure the overfit; they bound it.** The three new hits are the training
   items by construction. Over the whole corpus, held-out `package_query` gains are **0**: all 3 added
   `package_query` lines are the training lines themselves (§2). The 6th line comes from rule B **alone**
   (tip without rule B = 5/6). Rule B guesses that an undefined callee runs its argv. It fires on
   **12/12** data-only adversarial shapes where base is clean (§3).
4. **Verdict for the row:** not "C3 6/6, improved as declared" unqualified. The admissible reading is
   *"3/6 → 6/6 on the pre-registered 6 incident lines, which are the drafts' own targets (overfit set):
   2 lines by BashCVar literal resolution, 1 line by the rule-B lead heuristic (5/6 without it).
   Class-correct on all 3, 0 control-line findings, 0 lost corpus findings. Held-out recall evidence lies
   outside C3: 6 `live_probe` lines (rule A) + 1 `vcs_write` line (rule B)."* That is CriticC3's
   "improved on a 6-line overfit set" with explicit limits, plus credit for what the new evidence did
   establish: no regression, correct class, and 2/2 real-corpus precision for rule B.
5. **Rule B is acceptable** for a post-hoc tripwire whose docstring calls it a lead (`tools/mado-tripwire.py:41-50`).
   It is acceptable **only** with the corrections in §4. As landed, its output rows cannot be told apart from
   proven executions, and a cheap exemption kills 10 of the 12 false-positive shapes with zero corpus or suite cost.

## 1. Companions re-run independently

**Class of each former miss vs the 9c54c56 known-miss notes**
(`git show 9c54c56:.ufo/waves/round-18/frozen/expected.json`):

| line | note says | tip emits |
|---|---|---|
| `r14-source-safety:2` | "runs `pacman -Q hyprland wayland-protocols wayland-utils` … TwMissBashCVar target" | `package_query / pacman:-Q` |
| `r14-source-safety:3` | "two `pacman -Q hyprland` strings … TwMissBashCVar target" | `package_query / pacman:-Q` |
| `r13-root:4` | "run_record('packages',['pacman','-Q',…],0) … TwMissHelperFn target" | `package_query / pacman:-Q` |

**Round-19 re-pin diff.** Comparing `.ufo/waves/round-19/frozen/expected.json` with the r18 pin, keyed
`(file, line, class, rule)`:
- added = exactly those 3 rows;
- removed = [];
- `known_misses` = [];
- no other key differs.

So the circular re-pin (README: "`expected_findings` is the tool's own output") happens to equal the
note-derived expectation. CriticC3 §6 correction 3, adjusted for a 6th hit, is satisfied **post hoc**. The
check itself is not committed; it lives only in this report and in TwMerge §4/§5.

**Replays:**
- `--frozen .ufo/waves/round-18/frozen` → `frozen_verdict_mismatch`, `missing []`, extra = the 3 rows.
- `--frozen .ufo/waves/round-19/frozen` → `frozen_match` exit 0.

**Control lines.** `--scan inputs/*.jsonl` (cwd `round-18/frozen`, tip tool): 26 lines in total. The only
finding lines are the 6 incident lines. Per-file `unparsed_spawns` and `eval_unparsed` are 0 everywhere.
Controls = **20**. Side note: TwMerge §4 and CriticC3 w1 §1 say "21 control lines"; 5+5+5+6+5 = 26 and
26 − 6 = 20, as the lesson's M7 has it.

**Whole-corpus base→tip** (`/tmp/critc3w2/corpus.py base tip`): 4,821 files, 4,803 sha-stable between the two
scans, keyed `(file, line, class, rule)`:
- base 1,455 → tip 6,225; added 4,770; **lost 0**.
- added by class: `vcs_write` 4,677, `tool_install` 84, `live_probe` 6, `package_query` 3.
- `unparsed_spawns` −601; `eval_unparsed` +1 (the KotobaHistoricalMarking string TwMerge explains).

Every added line outside the two new classes:

| file:line | class/rule | source of the hit |
|---|---|---|
| `KengakuScopeAudit:140` | live_probe/pgrep, ps | rule A (same-text helper) |
| `OomClassTaxonomy:100` | live_probe/journalctl | rule A |
| `OomClassTaxonomy:130` | live_probe/journalctl | rule A |
| `ProviderSecrecy:92` | live_probe/journalctl | rule A |
| `ProviderSecrecy:99` | live_probe/journalctl | rule A |
| `MadoR13:470` | package_query/pacman:-Q | **training line** (`r13-root:4` source), rule B |
| `MadoR14.SourceSafety:152` | package_query/pacman:-Q | **training line** (`r14-source-safety:2`), BashCVar |
| `MadoR14.SourceSafety:155` | package_query/pacman:-Q | **training line** (`r14-source-safety:3`), BashCVar |

This agrees with TwMerge §6 at line granularity. (TwMerge's row-level table has 13 rows because it also
counts extra argv rows on already-flagged lines.)

## 2. What the companions do NOT show

- **Held-out recall for C3's class is zero.** The corpus holds no `package_query`/`host_mutation`
  positive outside the 6 lines that any round-19 mechanism newly recovers. C3's movement (+3) is
  therefore 100% training-set. Recovering a line you were written for proves the mechanism can see that
  shape, nothing more. CriticC3 w1 §4 reached the same conclusion with a lexical oracle. The round adds no
  contrary evidence.
- **The 6th hit is the guess, and only the guess.** Isolation run:
  `tipnob.py` (tip minus `hits.extend(helper_argv_leads(node, env))`, line 1433) gives these finding lines
  on the frozen inputs: `r13-global:1, r14-review:1, r14-source-safety:2, :3, r15:1` = **5/6**.
  `r13-root:4` comes from rule B and nothing else. CriticC3's "honest ceiling 5/6 without guessing" still
  stands, measured on the landed tool.
- **Rule B on the real corpus = exactly 2 lines** (`corpus.py tip tipnob`, 4,805 stable files,
  row-level multiset diff; nothing lost; unparsed counters unchanged):
  - `MadoR13.jsonl:470 package_query pacman:-Q`, the training line;
  - `MadoR18/MadoR18.CriticC2W2.jsonl:56 vcs_write git:checkout`. `run(['git','checkout','-q','4c103b55…'])`
    with `run` defined in an earlier cell; the toolResult (line 58) prints `4c103b5 round-18: wave-1
    integration …`, so the checkout really ran. This is a **true held-out positive** for rule B.
    It sits outside C3's class, and probably in a `/tmp` clone [INFERENCE].

  So rule B has real-data precision **2/2**, of which held-out is 1/1.
- **TwMerge overstates rule B's evidence.** TwMerge §9 says "Rule-B precision rests on 13 inspected
  rows … 10 of them are helper/lead rows the base tool could not see at all". By the isolation above, only
  **one** of those 13 rows (MadoR13:470, the training line) comes from rule B. The rest are rule A or
  BashCVar. Rule A (same-text binding, no guessing) earned the Kengaku/Oom/ProviderSecrecy credit. That
  credit must not be cited for rule B. *Impacted axis: honesty/provenance.*
- **Adversarial seats are not evidence yet.** `.ufo/waves/round-19/w2/reports/` holds only
  `RerunFetchVerify.md` and the registry at the time of writing. The AdvHelperFn/MutMergedTripwire reports
  do not exist, so "adversarial seats" cannot be counted toward admissibility. [UNK] what they will find.
  I sent AdvHelperFn the §3 fixture paths.
- **No committed C3 after-receipt or companion artifact.** `evidence/` holds `tw-recall-before*.txt`
  and `harm/harm-tw-recall.txt`. The harm file is a harm-watch receipt, not a claim receipt carrying the
  companions. Lesson M7 (`corpus/lessons/round-19.md:22`) promises the companions "reported beside recall".
  They currently exist only in seat prose.

## 3. Counterexample: rule B fires on 12/12 data-only shapes (base clean on all 12)

Each fixture is one assistant `eval` toolCall line in the r19-helperfn fixture format. None of them runs a
command. `python3 -I {base,tip}.py --scan fx/<n>.jsonl`:

| fixture (code shape) | base | tip |
|---|---|---|
| `@dataclass class Case` + `Case('mut1',['sudo','pacman','-S','--noconfirm','foo'])` | clean | host_mutation sudo + pacman:-S |
| `Case=namedtuple(...)`; `Case('m',['sudo','pacman','-Syu'])` | clean | host_mutation sudo + pacman:-Syu |
| `from shlex import join; print(join(['sudo','pacman','-S','foo']))` | clean | host_mutation sudo + pacman:-S |
| `fmt=lambda argv: ' '.join(argv)`; `print(fmt(['sudo','systemctl','restart','elephant']))` | clean | host_mutation sudo + systemctl:restart |
| `@functools.cache def show(argv): return ' '.join(argv)`; `show((...'pacman','-S'...))` | clean | host_mutation sudo + pacman:-S |
| `from tripwire_mod import classify_argv; assert classify_argv(['sudo','pacman','-S','foo'])==…` | clean | host_mutation sudo + pacman:-S |
| `BLOCK=frozenset(['pacman','-Q','hyprland'])` | clean | package_query pacman:-Q |
| `write_case('m7.jsonl',['sudo','pacman','-S','foo'])` (cross-cell fixture builder) | clean | host_mutation sudo, pacman:-S, hyprctl:reload |
| `deque(['systemctl','--user','restart','walker'])` | clean | host_mutation systemctl:restart |
| `expect(['pacman','-Qi','walker'],'package_query')` | clean | package_query pacman:-Qi |
| `async def show(argv): print(argv)`; `await show([... 'pacman','-S' ...])` | clean | host_mutation sudo + pacman:-S |
| duplicate `def check(...)` (printing only); `check('x',[... 'pacman','-S' ...])` | clean | host_mutation sudo + pacman:-S |

Mechanism (tip line numbers):
- `funcs` indexes only top-level, undecorated, non-duplicate `ast.FunctionDef` (`:1369-1372`).
- The lead fires whenever `helper is None and name not in PURE_ARG_CALLS` (`:1431-1433`).
- Classes, dataclasses, namedtuples, lambdas, decorated/async/duplicate defs, and **imports from any module
  other than subprocess/os/asyncio** all count as "undefined", which is much broader than "a helper whose
  body is elsewhere".
- `PURE_ARG_CALLS` (`:1252-1257`) omits `frozenset`, `deque`, `Counter`, etc.

Two output defects make this worse:
- **A lead is emitted at full severity with no lead marker.** The `dc-dataclass` verdict row is
  `{"argv0":"sudo","class":"host_mutation","command":"sudo pacman -S --noconfirm foo","rule":"sudo",…}`. It
  has the same keys and values as a proven `sudo` execution. The `r13-root:4` row is likewise
  indistinguishable from an observed `pacman -Q`. The docstring says "reported as a lead"
  (`:41-46`); the JSON does not.
- **The docstring contradicts itself.** `:32` still lists "helpers defined in one text and called from
  another" among things that "are not analysed". `:41-46` now analyses exactly that case as a lead.

None of the 12 shapes occurs in the current corpus (§2: rule B corpus delta = 2 lines, both real). These
are therefore *synthetic* false positives. They matter because this lane's own mutation-tester and
fixture-builder seats write exactly these shapes (case dataclasses, cross-cell `write_case`, imported
classifier asserts). A post-round corpus scan will meet them. The r19-helperfn suite has no negative for any
of the 12. Its lead negatives are `pure-print`, `nonliteral-var`, `literal-nonargv`, `defined-nonliteral`,
`string-arg`. Its main lead positive, `py-lead-cross-cell-literal`, is **the training line verbatim**
(`MadoR13:470` text).

## 4. Smallest safe correction (and proof that it costs nothing measured)

`/tmp/critc3w2/tipfix.py` is a scratch probe, not a patch for the lane. It changes rule B as follows:
- names **bound anywhere in the same text** emit no lead. This covers any `Store` name, def/async def/class
  names (decorated included), and import aliases;
- 5 container constructors are added to the exemption (`frozenset, deque, Counter, OrderedDict, namedtuple`).

Results:
- **12 fixtures:** 10/12 now clean. Still fired: `write_case(...)` cross-cell and `expect([...])`. These are
  the irreducible guess, and they are shape-identical to the incident.
- **All suites:** 9/9, 16/16, 33/33, 30/30, frozen 31/31, failsafe 1/1, bashcvar 45/45, helperfn 34/34,
  installers 18/18, vcs 17/17, frozen-f1f2 13/13 = **247/247**.
- **Frozen inputs:** identical 11 finding rows, including `r13-root:4 package_query pacman:-Q` → C3 stays **6/6**.
- **Corpus `tip` vs `tipfix`:** 4,804 stable files, row-level diff **∅ both ways**. Both real rule-B hits are kept.

Recommended (L1 / a tool owner, not this seat):
- (a) The exemption above, implemented as a parameter of `spawn_scan`, not a global like my probe.
- (b) Mark rule-B rows, e.g. `"basis": "lead"` or a `/lead` rule suffix. A lead must not be indistinguishable
  from an observed command. This changes the round-19 frozen pin for `r13-root:4` (re-pin once).
- (c) Fix docstring `:32`.
- (d) Add the 12 shapes as r19-helperfn negatives, with the 2 irreducible ones pinned as *documented
  lead false positives*.

None of this moves C3. It moves only rule B's precision on shapes the lane itself produces.

## Impacted axes

- **operability / C3:** value 6/6 reproduces. Interpretation overclaims if stated as recall; 5/6 without the
  guess; held-out gain in C3's class = 0.
- **honesty / provenance:** rule-B evidence borrowed from rule A rows (TwMerge §9); lead rows not marked as
  leads; docstring `:32` vs `:41-46`; companions not committed as a claim receipt.
- **harm watch:** none found. 247/247, lost 0, controls 0. Rule-B false-positive exposure is synthetic only so far.

## Limits

- Corpus is live: 16–18 files changed between paired scans and were excluded. Counts are as of
  2026-10-20 ~18:10–18:20Z.
- True/false-positive labels: I read the one new rule-B corpus hit (CriticC2W2:56) at its toolResult. The
  other added lines I took from TwMerge's inspection plus my line-level reproduction; I did not re-read each
  source.
- The 12 counterexamples are author-made (by me). Their realism is argued from lane practice
  [INFERENCE], not mined.
- `tipfix.py` is a probe to price the correction. It is not reviewed code, and its global-variable
  plumbing is not a proposed implementation.
- Did not run the gate, `frozen-repin.py`, or `measure.py`; did not audit BashCVar/Installers/Vcs beyond
  their effect on C3 lines and the corpus diff.
- Adversarial w2 seat reports were not yet written [UNK].

## Installs

none.
