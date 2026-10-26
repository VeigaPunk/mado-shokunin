# CritClaimSizing — round-46 claim sizing against prompt §6 item 9

Seat: `CritClaimSizing` (leaf critic, mado round 46, w1). Assignment: attack the registration's claim
sizing — (a) can a do-nothing control reach each target, (b) universal clauses the counters do not
enumerate, (c) axis named by the surface, (d) the same predicate sentence in registration, counter code
and receipt label, (e) C1/C2 separability and distinct axes.

Read: `.ufo/waves/round-46/registration.md` (freeze `8c5434c6`), `.ufo/prompts/mado-round-46.md:464-480`
(§6 item 9), both frozen counters, both controls runners, `receipts/ctl-c1.txt`, `receipts/ctl-c2.txt`,
`receipts/axis-base.txt`, both before receipts, `SCORECARD.md`, `quality/check-axis-scores.py`.
Scored on scratch clones of the freeze (recipes below); receipts in this directory.

**Bottom line.** Both targets are reachable by controls that skip the claimed work. C1 is
`TARGET_MET` (exit 0) for a tree whose only change is `cp .ufo/waves/round-46/l1-draft/mado-devices.py
tools/mado-devices.py` — and the frozen control matrix never scored that control. C1 is also
`TARGET_MET` for a 12-line tool that implements no contract at all and only execs the frozen reference
found in a non-hidden path, which falsifies the counter's printed claim that the model is invisible.
C2 is `TARGET_MET` for a tree produced by running one frozen script (`l1-draft/build-pos.py`); the
registration scores that as control `P` and declares it, but §6 item 9 says a skip-work control that
meets the target means the counter or target is wrong — declaring it does not discharge it.

Every quote below is verified by `quotes-check.sh` → `quotes-check.txt` (16/16 located).

---

## F1 — C1 target reached by copying the frozen reference; the cheapest skip-work control was never scored. **HIGH**

Attacks: registration C1 target (`registration.md:25-26`) and its control set (`registration.md:30-35`).

- The control runner enumerates `REF, BASE, STUB, MONITORS-COPY` plus `V01-V20`
  (`.ufo/waves/round-46/ctl/run-c1-controls.py:83-84`); `receipts/ctl-c1.txt:25` records
  `controls scoring TARGET_MET: 0 of 23`.
- Control I built (scratch clone at the freeze, one file added):
  `cp .ufo/waves/round-46/l1-draft/mado-devices.py tools/mado-devices.py`, commit → counter gives
  `PRED-C1-r46: fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present
  verdict=TARGET_MET rev=ded5347e03a1ddc0dc9c50b1f5e128d5a5d2abd1 seeds=46,2730344552`, exit 0
  (`receipt-c1-refcopy.txt`). The tool blob is byte-identical to `MODEL_SHA256`
  (`quality/counters/c1-r46-devices.py:68`), so clause g compares the model with itself.
- §6 item 9: "A target must be one a do-nothing control cannot reach" (`prompt:473`) and "if it meets
  the target, the counter or target is wrong" (`prompt:476`). The registration's residual "a tool
  holding a model of the contract is an implementation of it" (`registration.md:36`) names the class; it
  does not score the control, and §6 item 9 requires the receipt before freeze.
- Adding it as a 24th control flips the suite: `ok = ref_met and met_controls == 0`
  (`ctl/run-c1-controls.py:99`) → FAIL. That is the true signal, not an artefact.

Impacted axis: operability (capability acquisition) — the counter cannot distinguish "the round
acquired the capability" from "the freeze's reference was installed".

Smallest safe correction (no counter/target edit after seats scored — `prompt:479`): score REF-COPY,
commit its `TARGET_MET` receipt, and restate C1's after-state as *the frozen reference is installed at
`tools/mado-devices.py` and its counter line reproduces*; attribute the capability to the freeze's
in-round authoring (the L1 wrote it this round), not to a seat's independent work. Do not present a
seat's copy as capability evidence.

## F2 — "the model is invisible to the tool (clause i)" is false; a zero-work delegator is TARGET_MET. **HIGH**

Attacks: `quality/counters/c1-r46-devices.py:38` and the registration's clause-i sentence
(`registration.md:20-21`).

- `hidden_paths()` hides exactly three paths — the scored repo, the counter's lane, that lane's parent
  (`c1-r46-devices.py:241`); the sandbox is `--ro-bind / /` (`sandbox()` same file), so `/fast` stays
  readable. The wave's own write-scope/SCRATCH directive puts a lane clone (or any copy of the lane) at
  `/fast/scratch/hyaku/mado-r46/<Seat>/`, which contains
  `.ufo/waves/round-46/l1-draft/mado-devices.py`.
- Control I built: `tools/mado-devices.py` is 12 lines, no parsing, globs
  `/fast/scratch/hyaku/mado-r46/*/*/.ufo/waves/round-46/l1-draft/mado-devices.py` and `os.execv`s the
  first hit (`control-delegator.py`). Result:
  `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET
  rev=d37668f8685866d06830985a380e19cdbf2a7ea4 seeds=46,1008143892`, exit 0
  (`receipt-c1-delegator.txt`).
- This is a real do-nothing control: the tool implements none of the contract, and it passes every
  clause because the contract's reference is byte-reachable outside the denylist.

Impacted axis: operability; also the declared isolation residual ("a tool may detect the sandbox by
means not varied in environment B", `registration.md:36-37` — this is not detection, it is reading the
oracle).

Smallest safe correction: hide the scratch root (`--tmpfs /fast/scratch` plus binds for the tool and
work dirs), or enumerate every path a copy can live at and say so; add a DELEGATE control to the matrix.
If neither is done before seats scored, the round report must record the clause-i visibility sentence as
false in this environment.

## F3 — C2 target reached by replaying the frozen draft (`build-pos.py`); declared, not discharged. **HIGH-MEDIUM**

Attacks: registration C2 controls (`registration.md:52-55`) and target (`registration.md:50-51`).

- `ctl-c2.txt:2` records control `P` admitted (`admitted=1/1 verdict=TARGET_MET rev=07d52c2…`);
  `registration.md:55` says "control, not the data", `registration.md:54` names the source of P
  (`l1-draft/build-pos.py` on a clone of the freeze).
- My reproduction: clone at the freeze, run the frozen `build-pos.py`, commit →
  `PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=ac5baaaa450d24f63bb616fa62e6a05eb1fc24ae`, exit 0,
  and the tree contains no `tools/mado-devices.py` (`receipt-c2-buildpos-replay.txt`). The data the
  round must author is byte-derivable from the freeze by one committed script.
- §6 item 9 (`prompt:473-477`): a control that skips the claimed work and meets the target means the
  counter or target is wrong. The registration's resolution is a label change, not a fix.

Impacted axis: coverage (sourced entry).

Smallest safe correction: restate C2's after-state as *the frozen draft is landed (replay)* and
attribute the entry's authorship to the freeze; the round report must not credit the data commit with
coverage work the freeze already contains. Any tightening of clause c/d/g after seats scored is not the
claim's rule (`prompt:479`).

## F4 — the lowest-axis discharge cites a calibration instrument, not a ranking. **MEDIUM**

Attacks: `registration.md:11-12` ("Lowest-axis rule … so each is a lowest axis").

- `receipts/axis-base.txt` is produced by `quality/check-axis-scores.py`, whose own docstring is "the
  lane's published axis table must not be stale" (`check-axis-scores.py:2`). Its cells are instrument
  fractions — navigation 62/62 (indexability), calibration 73/73 (resolved/active), operability 12/12
  (`quality/check-index.py --selftest`), see `check-axis-scores.py:11-14` — not the lane's 0-10 axis
  scores.
- `MADO_AXIS: checked=3 mismatched=0` therefore proves published == derived; it cannot rank axes, and it
  covers 3 of the lane's six axes. The scored rubrics live elsewhere (e.g. coverage/sourced
  `SCORECARD.md:247`, last recorded value 7.1429/10 at `SCORECARD.md:528`; operability is a different
  instrument, `SCORECARD.md:248`).
- Consequence: §2.2's lowest-scoring-axis obligation is not attested by the evidence the registration
  cites, and the phrase is copied from the round-44/45 sections (`SCORECARD.md:2566`, `:2596`).

Impacted axes: the claim-to-axis attribution for both claims.

Smallest safe correction: name the lowest rubric by score and the claim that moves it (if the nudge is
invoked, record the waiver); delete the "so each is a lowest axis" inference.

## F5 — after-states omit the SCORECARD record §2.4/§2.6 require. **MEDIUM**

Attacks: `registration.md:25-26` (C1 target) and `registration.md:50-51` (C2 target).

- §2.4 requires per claim "the score delta, evidence pointer, counting command, and measured commit";
  §2.6 requires a capability-acquisition claim's row to enter the SCORECARD capabilities table "in the
  same round" (`AXES.md` §Capabilities: "Rows enter only through a round that demonstrates the
  capability running").
- Neither target clause reads `SCORECARD.md`: `grep -n SCORECARD quality/counters/c1-r46-devices.py
  quality/counters/c2-r46-input-device-entry.py` → empty. A closure can score both claims `TARGET_MET`
  with no capability row and no coverage delta recorded.

Smallest safe correction: add one re-derivable clause to each target (a `grep` for the round-46
capability row / move-log row at the data commit), or state in the registration that §2.4/§2.6 rows are
reported but not part of the claim's after-state.

## F6 — the kill rule pre-authorizes a v2 re-freeze after w1 seats have scored. **MEDIUM-HIGH**

Attacks: `registration.md:27-29`.

- "A hole wave `w1` finds before any data commit may re-register as v2 with a new freeze and new
  controls" (`registration.md:28`). Every w1 seat scores the frozen counter *before* any data commit —
  this seat's three runs above are exactly that, and the wave recipe instructs all 66 seats to score.
- §6 item 9: "A rule changed after any seat has scored is not the claim's rule" (`prompt:479`). Local
  precedent for the pattern the rule forbids: `SCORECARD.md:2596` records round 45's v2 supersession
  "after wave `w1` (41 seats) met PRED-C1-r45 with 16 cheat/do-nothing tools", and `:2566` the same for
  round 44.
- As written, the registration licenses the exact kumitate-r42 move: a post-score re-freeze whose new
  predicate would be treated as the claim's rule.

Smallest safe correction: restrict re-registration to "before any seat has scored under the frozen
predicate"; if a v2 freeze is taken anyway, the report must state that the w1 scoring is non-claim
evidence and cannot be the basis of a verdict.

## F7 — universal clauses the counter does not enumerate: clause r and "any nonce". **MEDIUM**

Attacks: `registration.md:26` ("under any nonce") and the registration's clause r
(`registration.md:21`).

- One run samples one nonce: `--nonce` defaults to `os.urandom(4)`
  (`quality/counters/c1-r46-devices.py:423-424`), and clause f/g each use it once. "Under any nonce" is
  a universal over an unenumerated set; §6 item 9 forbids exactly that (`prompt:467`).
- Clause r is a PATH marker: `make_fakebin` writes four executables into a fake PATH dir
  (`c1-r46-devices.py:141`), and `readonly` is the marker file's existence
  (`c1-r46-devices.py:400`). The tool can exec `/usr/bin/hyprctl` (or `libinput`, `journalctl`,
  `udevadm`) by absolute path — the sandbox `--ro-bind / /` keeps them executable — and no marker is
  created. The counter's own docstring concedes it: "the read-only clause catches PATH lookups only"
  (`c1-r46-devices.py:44`); the registration's residual list does not carry this residual
  (`registration.md:36-39`).

Smallest safe correction: change the target sentence to "with the drawn nonce (default)" or enumerate a
fixed nonce set; add the PATH-only residual to the registration; if the read-only property is meant
literally, test it (e.g. a stub `hyprctl` at an absolute path, or a ptrace/seccomp-free
exec-audit) rather than a PATH marker.

## F8 — clause i has no receipt label; the predicate's clause set ≠ the printed label set. **LOW-MEDIUM**

Attacks: `registration.md:18-22` (clause list a,s,f,i,r,g) vs the counter's clause lines.

- The counter prints `clause=a` (`c1-r46-devices.py:359`), `clause=s` (`:384`), `clause=f` (`:395`),
  `clause=g` (`:398`), `clause=r` (`:401`). `grep -n "clause=i" quality/counters/c1-r46-devices.py`
  exits 1. A missing `bwrap` is `SETUP` exit 2 (`c1-r46-devices.py:428`), not a clause line.
- §6 item 9 requires the same label in the receipt (`prompt:465-466`, "the same sentence … the same
  label in the receipt"). Isolation failure and setup failure are indistinguishable in the receipt.

Smallest safe correction: print `PRED-C1-r46 clause=i bwrap=ok hide=<n>` once the sandbox is up (or
move i to the harness and drop it from the registered clause list).

## F9 — C2's "new rows S316-S325" is not in the predicate. **LOW**

Attacks: `registration.md:47` vs C2 clause c.

- The plan names ten new rows; the counter requires only "ids absent at BASE (>= 3)"
  (`c2-r46-input-device-entry.py`, clause c docstring). A tree citing S316-S318 only would admit while
  contradicting the registered sources — the after-state sentence in the plan and the condition in the
  code are not the same sentence.

Smallest safe correction: bind S316-S325 by name (10 ids) in clause c, or restate the Sources line as
"at least three new ids".

## F10 — separability is asserted at freeze and deferred to w1. **LOW (partly discharged here)**

Attacks: `registration.md:61-63` ("A tool-only tree meets C1 and misses C2; a data-only tree misses C1
and meets C2 (to be shown by a w1 seat on scratch trees)").

- Code level it holds: C1's counter reads no `corpus/` path and C2's reads no `tools/` path (grep on
  both files).
- My C2 replay receipt (`receipt-c2-buildpos-replay.txt`, rev `ac5baaa`) is a C2 `TARGET_MET` on a tree
  with no `tools/mado-devices.py` — the "data-only" direction is now demonstrated. The "tool-only"
  direction follows from clause a alone (`receipts/c1-before-base.txt:1`, base tree with no tool →
  `tool=absent`, exit 1).
- So the property holds; the defect is only that the registration asserts it and schedules its proof
  outside the freeze.

No correction needed beyond citing both controls in the round report.

---

## What the registration gets right (supports)

- C1 and C2 sit on distinct axes (operability / coverage) and their counters cross-read nothing
  (see F10) — not one claim.
- Predicate and receipt label agree for the final lines: `receipts/ctl-c1.txt:1` is byte-equal to the
  registered target prefix (`registration.md:25-26`), and `ctl-c2.txt:2` matches
  `registration.md:50-51`. Clause i is the only unlabeled clause (F8).
- Fixtures pin holds: `sha256sum quality/counters/c1-r46-fixtures.json` =
  `027ed50877b345e34b27e38b4a865be4b23f94c0cc0067ac42265ca1778e3fc1` = `FIXTURES_SHA256`
  (`c1-r46-devices.py:66`); the file holds exactly 90 entries.
- C2's surface count matches: 28 SURFACES entries in code = registration's "28 surfaces"; pins are the
  ten named files; census line and locator width match the code.
- Base receipts match the registration's before-lines (`receipts/c1-before-base.txt:1-2`,
  `receipts/c2-before-base.txt:2`).
- Controls landed one commit after the freeze (`e0be61e4`), still pre-data — recorded, not a defect.

## Reproduction recipes (trees were scratch and are deleted)

```
S=/fast/scratch/hyaku/mado-r46/<Seat>; D=$S/repro-refcopy
git clone -q --shared --no-checkout <lane> "$D"; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach 8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
cp "$D/.ufo/waves/round-46/l1-draft/mado-devices.py" "$D/tools/mado-devices.py"
git -C "$D" add -A; git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m refcopy
python3 -I <lane>/quality/counters/c1-r46-devices.py --repo "$D" --rev HEAD --work "$S/w"
```
Delegator control: same clone, `tools/mado-devices.py` = `control-delegator.py` in this directory, plus
one lane clone left at `$S/visible-lane` (any non-hidden clone works).
C2 replay control: same clone, run `<lane>/.ufo/waves/round-46/l1-draft/build-pos.py "$D"`, commit, then
`python3 -I <lane>/quality/counters/c2-r46-input-device-entry.py --repo "$D" --rev HEAD --base <base>`.

## Receipts in this directory

| file | content |
|---|---|
| `receipt-c1-refcopy.txt` | full counter output, REF-COPY control, `TARGET_MET`, rev `ded5347e` |
| `receipt-c1-delegator.txt` | full counter output, DELEGATE control, `TARGET_MET`, rev `d37668f8` |
| `receipt-c2-buildpos-replay.txt` | C2 counter output, build-pos replay, `TARGET_MET`, rev `ac5baaaa` |
| `control-delegator.py` | the 12-line zero-work tool source |
| `quotes-check.sh` / `quotes-check.txt` | every quote above located (16/16) |

Tooling: none installed (no pacman/uv/npx use). Scratch: `/fast/scratch/hyaku/mado-r46/CritClaimSizing`
(1.1 GB, under the 2 GB cap), deleted after the receipts were copied here.

## Verdict for the L1

C1's and C2's targets are not do-nothing-proof as frozen: REF-COPY and the build-pos replay reach both
targets with zero contract/entry authorship, and the DELEGATE control falsifies the clause-i invisibility
sentence. All four non-author findings F4-F8 are repair-by-sentence defects that change no evidence that
already exists. Because w1 seats have scored, no counter or target edit now can be the claim's rule
(`prompt:479`): report C1/C2 as *installation/landing of freeze-authored artifacts plus verification*,
score REF-COPY and DELEGATE as `TARGET_MET` receipts, and let the closure rule on whether operability
and coverage credit survives that reading.
