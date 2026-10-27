# R53Three28 — bounded work item 28: executable counter/fixture behaviour for C1 and C2

Seat `R53Three28` (executor, leaf). Round 53, lane `mado-shokunin`, base
`ad4bf2059bcfafe63671d262222908ee1fe8001c`. Axes named: **operability** (C1) and
**coverage** (C2). No tracked lane file was written; no dispatch, background job, git/jj
mutation, package query or live probe was issued; no network source was opened this round
(the C2 pins are the round-52 committed fetch bytes, re-verified by digest). Scratch:
`/fast/scratch/hyaku/mado-r53/R53Three28` (5.6 MB) was used only for the two counter drafts and
their fixtures and is deleted; no `/tmp` residue.

Predicates attacked, quoted from `.ufo/waves/round-53/claims-frozen.md`:

> **C1** — "a newly committed, scratch-aware counter with explicit selftest returns TARGET_MET
> on the production ledger, TARGET_MISSED on a no-work control and each frozen forgery
> fixture, with exact population coverage and non-self pointers."
>
> **C2** — "append-only correction clearly repairs those three propositions against opened
> pinned source bytes; a frozen counter rejects the old bytes and accepts corrected entry with
> quote/pin/proposition bindings; independent reviewer checks source truth."

This seat built both counter drafts in scratch and scored them on the lane's committed bytes.
Nothing here is an admission: no byte was committed, no non-author review is claimed, and the
counters are drafts for L1 to land (C1) or to re-cut as the frozen C2 counter.

## 1. C1 — operability: accountable instrument-ledger counter (scratch draft)

### 1.1 Re-measured baseline at the base rev (never the working tree)

```
$ git -C <lane> show ad4bf20:quality/tool-ledger.md | ...   # fence-aware parse
population 82         # tools/** + quality/*.py + quality/counters/*.py at ad4bf20
ledger fenced-skip rows 82
naive `^\| \`` rows    83    # the +1 is the ledger's own grammar example inside a fence
```

`quality/tool-ledger.md` two rows are thin on instrument context and still pass every check
below: `quality/check-tool-ledger.py` (3 informative tokens, 1 present in its bytes) and
`quality/counters/c1-r51-ledger.py` (4 / 2). The counter was calibrated to admit them — see
§1.5 for why the floor cannot be raised without amending the production ledger.

### 1.2 Draft predicate as implemented (`c1-r53-ledger.py`, sha256 `ac21694d…`)

Scored at `--rev`; `--ledger FILE` substitutes the ledger bytes; `--work` is the only write
surface and is refused inside the scored repo (measured: `C1_R53 error=work-inside-repo`,
exit 2). Final line: `C1_R53: population=… ledger_rows=… uncovered=… dup=… dangling=…
bad_pointer=… self_pointer=… empty_desc=… generic_desc=… selftest=… verdict=… rev=…`.

Non-self pointers are decided by **normalized identity**, not string equality: leading `./`
and `/` stripped, repeated slashes collapsed, case folded, `#fragment` and arbitrary `:<suffix>`
stripped, trailing `)`/`,`/`;` stripped, bare basenames compared to the ledger/row basename, and
git symlinks (mode 120000) resolved through the tree before comparison. A valid accountable
pointer must resolve to a regular blob at the rev, must not be the ledger, the row's own file
or another population instrument, and its bytes must name the row's basename as a name. The
description check is: ≥10 words, not a verbatim duplicate of another row, and ≥1 token outside
{function words, ledger vocabulary, own-name tokens} that occurs in the instrument's own bytes.

### 1.3 Measured results — production, no-work control, frozen fixtures

All runs: `python3 -I c1-r53-ledger.py --repo <lane> --rev ad4bf2059… --work <scratch>`
(plus `--ledger <fixture>`), exit captured directly.

```
$ python3 -I c1-r53-ledger.py --repo <lane> --rev ad4bf2059…
  C1_R53: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 \
          empty_desc=0 generic_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059…   (exit 0)
```

| fixture (round-52 committed bytes) | rc | measured | wanted |
|---|---|---|---|
| `controls/c1-do-nothing.md` | 1 | `ledger_rows=0 uncovered=82` | TARGET_MISSED ✔ |
| `controls/c1-row-context-control.md` | 1 | `uncovered=81 dup=1 generic_desc=2` | MISSED ✔ |
| `w1/C1Simplify/control-B-row-selfpointer.md` | 1 | `self_pointer=82 generic_desc=82 bad_pointer=82` | MISSED ✔ |
| `control-C-ledger-selfpointer.md` | 1 | `self_pointer=82 bad_pointer=82` | MISSED ✔ |
| `control-D-generic-desc.md` | 1 | `generic_desc=82` | MISSED ✔ |
| `control-E-one-selfpointer.md` | 1 | `self_pointer=1 bad_pointer=1` | MISSED ✔ |
| `control-F3-forged.md` | 1 | `generic_desc=82` | MISSED ✔ (the r52 reference counter passed this one) |
| `control-G-legit-ledger-reader.md` | 0 | all zero, `TARGET_MET` | MET ✔ (no false self-pointer for a row that *describes* reading the ledger) |
| `control-H-minimal-forgery.md` | 1 | `generic_desc=1` | MISSED ✔ |
| `w2/Attack01/controls/F-all-forged.md` | 1 | `generic_desc=82` | MISSED ✔ (r52 "reproduced and extended" 82/82 bypass) |
| `H2n-verify.sh-forged.md` / `H3n-c2r51-forged.md` / `H4n-nameonly-forged.md` | 1 | `generic_desc=1` each | MISSED ✔ |
| `w2/Attack01/production-ledger-nofence.md` | 0 | `TARGET_MET` | MET ✔ (fence handling does not depend on the fence) |

### 1.4 Measured results — the nine r52 self-pointer laundering spellings (rebuilt on a 3-instrument fixture repo)

`replay-attack02.py` rebuilds each Attack02 shape and scores it; `git rev-parse --show-toplevel`
was asserted by the counter's own `Repo` constructor before any run.

```
REPLAY: P01-green                  want=TARGET_MET   got=TARGET_MET   rc=0
REPLAY: P03-bare-ledger-basename   want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P04-own-basename           want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P05-dotslash               want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P06-trailing-paren         want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P07-nonnumeric-anchor      want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P19-double-slash           want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P20-leading-slash          want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P21-case-fold              want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P09-symlink-own            want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
REPLAY: P10-symlink-ledger         want=TARGET_MISSED got=TARGET_MISSED rc=1 self_pointer=1
```

Every r52 laundering spelling that produced `TARGET_MET self_pointer=0` now yields
`self_pointer=1` and the right verdict.

### 1.5 Explicit selftest (runs inside every scored invocation)

```
$ python3 -I c1-r53-ledger.py --selftest --work <scratch>
C1_R53_CASE: green / no-work / dup-row / dangling / bad-pointer / self-full / self-basename /
             self-dotslash / self-dslash / self-leading-slash / self-case / self-paren /
             self-anchor / self-own-basename / self-symlink-own / self-symlink-ledger /
             peer-pointer / fenced-example / short-desc / duplicate-desc / name-only-desc /
             empty-desc / shared-registry
C1_R53_SELFTEST: 23/23 passed
```

A scored run prints `selftest=ok` only when those 23 cases pass; a failing selftest forces
`TARGET_MISSED` whatever the ledger looks like.

### 1.6 Declared ceilings (measured, not inferred)

1. **Long generic forgery passes.** A 20-word semantically empty description that copies one
   real instrument token measures `TARGET_MET` on a production ledger with that single row
   replaced (`forgery-long.md`, sha256 `80ef8379…`: `Mentions sendKeyboardMods inside a longer
   generic sentence for the module and carries nothing else specific at all.`). The frozen
   fixtures are all ≤8 words, so the 10-word floor separates them, but a motivated
   long-form forgery is **not** caught. This is a bounded structural check, never semantic
   accountability.
2. **Shared registry / cross-row cycle passes.** One `docs/registry.md` naming every basename
   (`shared-registry` case) and A→B/B→A document cycles satisfy "non-self, resolvable, names
   the basename". Measured green; disclosed, not claimed closed.
3. **The frozen no-work control is rejected as shape, not as named defect.** `c1-do-nothing.md`
   is a 4-cell table with an unbackticked first cell; the counter's grammar is the production
   ledger's 3-cell grammar, so it parses 0 rows and fails on `uncovered=82`. Direction is
   correct and can never be green; the self-pointer/no-work signal is exercised instead by
   control-B/C/E and the 11 Attack02 replays. Relaxing the parser to arbitrary table shapes
   would re-open the all-cell false positive that control-G is designed to guard.
4. **Integration burden.** Committing the counter at `quality/counters/c1-r53-ledger.py` adds
   one file to the population (82 → 83), so the same commit must add its own ledger row.
   The committed companion gate does not measure the new signals and is narrower than the
   frozen claim (measured at base, `--work` under scratch):

   ```
   $ python3 -I quality/check-tool-ledger.py --selftest --work <scratch>
   LEDGER_SELFTEST: 50/50 passed                                   (exit 0)
   $ python3 -I quality/check-tool-ledger.py --repo <lane> --rev ad4bf2059…
   LEDGER: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=ad4bf2059…
   ```

   Its six fields carry no `dup`, `self_pointer` or `generic_desc`, so the C1 counter must not
   delegate the self-pointer/context verdict to it; either the gate is re-cut or a fresh
   companion is published before the counter can be called accountable.

## 2. C2 — coverage: proposition-bound repair of the indexed r52 entry

### 2.1 Pinned bytes re-verified (no new source opened)

```
$ cd .ufo/waves/round-52/fetch && sha256sum -c SHA256SUMS
Hyprland-ConfigActions.cpp: OK      Hyprland-ConfigActions.hpp: OK
Hyprland-KeybindManager.cpp: OK     Hyprland-legacy-DispatcherTranslator.cpp: OK   README.txt: OK
```

Source rows S370–S373 are already `mined`, opened `2026-10-27`, at
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/…`
(`corpus/SOURCES.md:320-323`); the entry is indexed at `corpus/README.md:80`. No fetch this
round — `[OBS]` from committed bytes only.

### 2.2 The three defects, re-measured on those bytes

```
$ grep -F 'g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);' Hyprland-ConfigActions.cpp
(no match, rc=1)                                    # P16 quote is spliced, not contiguous
$ sed -n '1554p;1556p;1557p;1558p;1576p' Hyprland-ConfigActions.cpp
    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);      # 1554
    if (S.m_passPressed == 1) {                              # 1556
        if (!isMouse)                                        # 1557
            g_pSeatManager->sendKeyboardKey(…PRESSED);       # 1558  (branch-conditioned)
    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);            # 1576
$ grep -n '^static SDispatchResult sendshortcut\|^static SDispatchResult sendkeystate' Hyprland-legacy-DispatcherTranslator.cpp
531:static SDispatchResult sendshortcut(const std::string& args) {
591:static SDispatchResult sendkeystate(const std::string& args) {
$ grep -n 'for (xkb_keycode_t kc\|key not found' Hyprland-legacy-DispatcherTranslator.cpp
565:            for (xkb_keycode_t kc = keycode_min; kc <= keycode_max; ++kc) {   # loop closes :571
574:                return {.success = false, .error = "sendshortcut: key not found"};
```

| ID | defect (as routed by round 52) | mechanical anchor now |
|---|---|---|
| P16 | quote splices :1554 with :1558 across the elided guard; "then clears" rests on :1576 outside the quote | `grep -F` of the joined text returns rc 1 |
| P17 | proposition says "`sendshortcut`'s repeat branch"; :619–622 lies inside `sendkeystate` (:591–627), and `sendshortcut` spans :531–589 | enclosing function at :619 is `sendkeystate` |
| P18 | "returns … inside the scan"; the return at :574 executes after the loop closes at :571 | nearest enclosing `for` is :565–571, which excludes :574 |

### 2.3 Draft C2 counter (`c2-r53-proposition-entry.py`, sha256 `aab321bb…`)

Clauses, declared before scoring: (a) entry indexed by basename in `corpus/README.md`;
(b) `source:` rows exist in `corpus/SOURCES.md` as `mined`, dated, 40-hex, and each row's
`pin <path>; … fetch SHA256 <hex>` matches the pinned file's digest at the rev; (c) the
proposition map parses by **header names** (so `| ID | Proposition | Source row | Pin:anchor |
Quote | Support | Why |` works), ≥4 scored rows; (d) quote ≤25 words, whitespace-collapsed
verbatim inside ONE anchor span; (e) if the proposition backticks an identifier that is a
function in the pinned file, the anchor start must lie inside that function's brace body;
(f) "inside the scan/loop" must quote a line inside the innermost `for`/`while` body, and
"after the scan/loop" must quote a line after it closes; (g) `superseded: P16, P17, P18 -- reason`
excludes those ids and requires a reason.

```
$ python3 -I c2-r53-proposition-entry.py --repo <lane> --rev ad4bf2059…            # committed entry
C2_R53_FAIL: d:P16 quote-not-in-span Hyprland-ConfigActions.cpp:1554-1558,1576
C2_R53_FAIL: e:P17 subject-sendshortcut-span-in-sendkeystate
C2_R53_FAIL: f:P18 inside-no-enclosing-loop
C2_R53: props=18 scored=18 superseded=0 table_rows=18 rows_mined=4 failures=3 selftest=ok verdict=TARGET_MISSED rev=ad4bf2059…   (exit 1)

$ python3 -I c2-r53-proposition-entry.py --repo <lane> --rev ad4bf2059… \
      --entry-file candidate-r53.md                                               # append-only repair
C2_R53: props=20 scored=20 superseded=3 table_rows=23 rows_mined=4 failures=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059…     (exit 0)
```

That is exactly the frozen shape: **old bytes rejected on the three defects, corrected entry
accepted with quote/pin/proposition bindings**, selftest `10/10 passed` (green, spliced quote,
unknown-subject, locality-inside, locality-after, superseded, 26-word quote, fabricated quote,
wrong pin file, swapped pin digest).

### 2.4 The append-only repair (scratch candidate, sha256 `414ee5ba…`)

Appended verbatim under the original table; original rows stay as written and are marked by
`superseded: P16, P17, P18 -- …`, so an admitted reader sees the correction without a rewrite:

| ID | Proposition | Pin:anchor | Quote |
|---|---|---|---|
| P16a | The action sends the keyboard modifier mask before any key event. | `Hyprland-ConfigActions.cpp:1554` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` |
| P16b | Only when `m_passPressed` is 1 is the pressed keyboard event delivered. | `:1556-1558` | `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` |
| P16c | After the key branch the modifier state is cleared. | `:1576` | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` |
| P17a | `sendkeystate`'s repeat branch invokes its delegate twice when the first call succeeds. | `Hyprland-legacy-DispatcherTranslator.cpp:621-622` | `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` |
| P18a | After the scan loop closes, an unmatched key returns the `key not found` error. | `:573-574` | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` |

The split of P16 into three rows is what makes the quote continuous: the PRESSED call is
branch-conditioned at :1558, and the clear call at :1576 is a separate sentence, not part of a
single excerpt.

### 2.5 Ceilings

- The counter checks **mapping locality**, not entailment. P15's "before changing it" (writes
  at :614–617, restore :624 outside pin and quote), P12's second clause (:585-586 outside the
  quote) and P07's "known modifier names" generalisation remain partial and still pass; the
  r52 attack registered them as gaps, not falsifications, and they need per-row pins or
  re-worded propositions in the same repair if the lane wants them closed.
- `superseded:` is a declaration the counter trusts; it cannot tell a justified supersede from
  a laundering one. The ≥4-scored-rows floor bounds it; a reviewer must still read the reason.
- With `--entry-file`, the index clause is satisfied by the cited entry's basename; a *new*
  correction filename needs its own `corpus/README.md` row before it can be scored green.
- The old entry stays committed and unmarked at `ad4bf20`: round-52's quality harm is not
  healed by this scratch candidate.

## 3. Routed r52 defects re-read as evidence (no assumptions)

- `corpus/lessons/round-52.md` `## Gate` contains instructions and a "remain pending" sentence
  but **no per-row records** for S370–S373 (checked at the section, lines 5–17); the SOURCES
  contract's Gate requirement is unmet. (r53 defect 1 confirmed.)
- Same file `## Changes` (line 23) still reads "Pending final integration revisions and
  receipts." (r53 defect 2 confirmed.)
- QUALITY 17 distinct-scope review for the reused URLs is not recorded anywhere in the tree
  I read; still owed (defect 3 confirmed as absent, not judged here).

## 4. Axis accounting (bounded, read-only)

| Axis | Move | Evidence |
|---|---|---|
| operability | measured improvement on a drafted counter: every frozen forgery fixture and every r52 laundering spelling now `TARGET_MISSED` with the defects named, production `TARGET_MET`, selftest 23/23 | §1.3–§1.5 |
| coverage | measured improvement on a drafted counter: old entry rejected on exactly P16/P17/P18, append-only candidate accepted, pin digests bound | §2.3–§2.4 |
| depth / freshness / calibration / adjacency | unchanged; no tracked file, scorecard row, capability or corpus row was written by this seat | the only lane path written by this seat is this report; `git status --porcelain` also shows an untracked sibling artifact `corpus/lessons/round-53.md`, not written here |

Neither move is admitted: nothing was committed, and C1's target explicitly requires a
**committed** counter; C2 requires an independent reviewer on source truth. No axis harm found.

## 5. Risks / blockers for L1

1. **Commit burden:** landing `c1-r53-ledger.py` changes the population to 83 and requires the
   ledger row plus a matching `check-tool-ledger.py`; landing the C2 correction requires the
   `corpus/README.md` index decision (same file vs new file) and the Gate records for S370–S373.
2. **Do not over-claim:** the C1 description check is lexical and structural, not semantic; a
   long-form forgery passes (§1.6.1). The C2 counter binds mapping locality, not entailment
   (§2.5). The frozen claims already say this; the receipt must repeat it.
3. **Threshold provenance:** the 10-word / 1-instrument-token floors were calibrated on the
   committed production ledger and the frozen r52 fixtures. If L1 amends either side, re-measure
   before freezing the predicate; do not call these thresholds entailment.
4. **No new source:** C2's "opened this round" credit is unaffected — this seat re-verified
   round-52 pins and claims no expansion credit.

## 6. Scratch disposition and reproducibility

Everything was built under `/fast/scratch/hyaku/mado-r53/R53Three28` (5.6 MB) and is removed;
no `/tmp` residue (checked: `/tmp/c1-r53-*`, `/tmp/c2-r53-*` absent, 0 bytes left). Artifact
digests recorded before removal, Python 3.14.8:

```
ac21694d412e89e25748334046ea11b2061c3962d8a937e5c4c5dd2fb896452d  c1-r53-ledger.py
6cc7fe9b1327e987f4d1e64010213009ad3fdba8936a089f1a117e974c1b2b9b  replay-attack02.py
aab321bb93e7ef92c234e1cacb6f6ce53357ccbaeb5316ef4629244f62ca42da  c2-r53-proposition-entry.py
0c5d3a207b8d663d9a0baf1727aab52b418eabc7cdec7f6f6f8b56ad5233b704  build-candidate.py
414ee5ba1d8a131db83b7ed8edee68249db6be58802a1d3a1d0f192d5feea209  candidate-r53.md
80ef837931cf06c1d8dc6cd7fed5320c94b4ba72d2cf2a9a147cfa0d400a9e49  forgery-long.md (ceiling probe)
```

Tool installs: none. Package transactions: paused, none attempted.

Report: `.ufo/waves/round-53/w1/R53Three28.md`
