# RevPreRegistration — round-17 pre-registration review

Seat: `MadoR17.RevPreRegistration` (reviewer, leaf; no delegation).
Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Reviewed object: the committed pre-registration at `0175f13` —
`SCORECARD.md:821-865` plus `.ufo/waves/round-17/evidence/census-start.txt` —
against baseline `27cd06f`.
Secondary (in-flight, untracked) evidence read as **current state only, not as
pre-registered commitment**: `.ufo/waves/round-17/measure.py`,
`label-check.py`, `label-claims.json`, `w1/spec.json`, the two
`corpus/knowledge/*-r17.md` notes, and `git status` untracked entries.

Host pause compliance: no `sudo`, `pacman`/`yay`/`paru` (not even `-Q`/`-Si`),
`systemctl`, `hyprctl`, compositor/input/screenshot or service command was run.
Config trees were read as bytes only. No tool was installed or upgraded. No
lane writes outside this report (two `/tmp` scratch lists only, for a README
membership check); no commits; no `jj`; no delegation. Transcript reads were
limited to the R15 set named by the red anchor.

## 1. Answers to the four questions

| Question | Answer |
|---|---|
| Are C1-C3 falsifiable? | **C1: partially.** The literal fraction is falsifiable, but the measured predicate does not entail the declared R16-V1 routing, and the label check has no predicate in the committed text. **C2: as a count, yes; as a rule, no** — the counting rule in the committed text is weaker than the instrument that will measure it, and "admitted"/"new"/"route" are not in the predicate. **C3: no** — `N/N` and an unpinned transcript assertion admit a vacuous pass. |
| On distinct axes? | **Yes at rubric-family level:** calibration (QUALITY.md), coverage (rubric V over knowledge notes + SOURCES), operability capability (tripwire). Two caveats: if V is scored, the lowest active scored row is coverage/V, so C1's "(lowest axis)" label is wrong; and C1/C3 can share the QUALITY.md denominator (§3 H5). |
| Causally separable? | **Not as claimed.** `SCORECARD.md:862-863` says "C3 needs no note or criterion", but the in-flight `QualityDraft` plans criterion 23 *and* candidate criterion 24 for the tripwire. If 24 lands, C3 appends to the file C1 measures and C1's denominator moves from 23 to 24. C2 is genuinely independent of both measured counters. |
| Is calibration genuinely the lowest active axis under QUALITY22? | **Not established as written.** I re-derived 14/22 = 6.3636 at both `27cd06f` and `0175f13`, and it is lowest among the four rows the paragraph lists (U 7/7, freshness 29/29, operability 372/372 all = 10). But the same pre-registration declares rubric V at 2/6 = **3.3333**; unless V is expressly non-scored, V is the lowest active scored row and `C1 calibration (lowest axis)` is false. The paragraph never states V's axis status. |

## 2. Re-derived facts

| # | Fact | Command / anchor | Observed |
|---|---|---|---|
| 1 | QUALITY criteria and literal lesson citations at baseline | `git show 27cd06f:corpus/QUALITY.md \| grep -cE '^[0-9]+\. '` / `… \| grep -cE '^[0-9]+\. .*lessons/'` | 22 / 14 = 6.3636; identical at `0175f13` |
| 2 | Semantic (whole-block) citation counter | awk block walk over `corpus/QUALITY.md` | 17/22 = 7.7273 (only criteria 1-5 lack any `lessons/` in their block) |
| 3 | R16-V1 anchor is real | `git show 27cd06f:corpus/lessons/round-16.md \| sed -n '131,132p'`; `.ufo/waves/round-16/evidence/frozen-tampered.json` | Lesson says "Input tamper control returns **2 snapshot_tampered**… `frozen-tampered.json`"; receipt records `measured_commit 9dcf248…`, `exit 2`, stdout `finding: frozen_error`; token absent. Receipt file added at `1e31681`, not at `9dcf248`. |
| 4 | Tripwire absent at baseline | `git cat-file -e 27cd06f:tools/mado-tripwire.py` | fatal: not in revision. `tools/` holds only `mado-action-plan.py`, `mado-verify.sh`. |
| 5 | Red anchor exact | `sed -n '54p' …/MadoR15/MadoR15.LibinputEvents.jsonl` | `type:message`, `role:assistant`, `toolCall id call_38165`, `name:"bash"`, `arguments.command:"sudo pacman -S --needed --noconfirm libinput libinput-tools"`, timestamp `2026-10-20T07:25:16.905Z`. Matches the claim exactly. |
| 6 | R15 set shape | `MadoR15.jsonl` + `MadoR15/*.jsonl` | 65 JSONL files; 0 occurrences of an eval shell-mode code line (`"code":"!"` with optional space) across the set. The anchor is a bash call; the eval branch of the shared interface is not exercised by R15. |
| 7 | U-route census at baseline | `git grep -hE '^covers: U[1-7]$' 0175f13 -- corpus/knowledge \| sort \| uniq -c` | U1…U7 one each = 7. |
| 8 | C2 baseline reproduced by hand | entry heads + SOURCES rows | P1: `window-rule-effects-getprop.md` source line 3 cites S002/S016/S018/S019/S020 (all tier A, `mined`, `used-by` names the note) and `hyprland-config-era-r12.md` cites S021-S029; `covers: U1`/`U2` → P1. P2: `waybar-observation-boundaries-r16.md` line 1 cites S053/S054 (tier A, `mined`, `used-by` names it), `covers: U7` → P2. Covered {P1,P2} = **2/6 = 3.3333**. Matches the claim. |
| 9 | Surface reality | file reads | `~/.config/{alacritty,foot,kitty,ghostty}` all exist; `~/.config/xdg-terminals.list` exists and its line 3 is `Alacritty.desktop`; `~/.config/hypr/hypridle.conf` and `hyprlock.conf` both exist. `PROVINCE.md` contains **no** `P1`..`P6` tokens (read in full, 17 lines). |
| 10 | Instruments post-date the claim | `git cat-file -e 0175f13:.ufo/waves/round-17/measure.py`; `git status --porcelain` | fatal — absent at `0175f13`; untracked now. Same for `label-check.py`, `label-claims.json`, `w1/spec.json`, fixtures, both r17 notes. |
| 11 | Implemented C1 predicate | `measure.py:87-93` | same line-based regex as the SCORECARD command; no diff/append-only check. |
| 12 | Implemented C2 predicate | `measure.py:123-229` | `source:` tokens `S\d{3}` in first 15 lines; each must resolve to a row with `status=mined`, `tier=A`, `used-by` containing the exact path; entries declaring `surface:` must also contain exact headings `## Upstream contract`, `## Host declaration`, `## Safe observation`, `## Unexercised behavior` with `[UNK]` in the last; legacy `covers:` entries skip the facet check but still need the source join; **no** admission, newness or content check; score `10*count/6`. |
| 13 | Implemented label check | `label-check.py:78-116`, `label-claims.json` | doc window must contain receipt basename + token; receipt at `rev_receipt` must contain token in `stdout/stderr/finding/detail/verdict`. Red claim: `round-16.md:131-132`, `frozen-tampered.json@1e31681`, token `snapshot_tampered` → receipt-stage MISMATCH. Green claim: `action-frozen-final.json@4bfb236`, token `frozen_match`. The checker does **not** compare the receipt's `measured_commit` with any cited revision. |
| 14 | Census-start receipt | `.ufo/waves/round-17/evidence/census-start.txt` | three W04 duplicate-URL warnings (S030/S042/S045) retained, `mado ok …/corpus/SOURCES.md`, `exit=0`, timestamp `2026-10-20T10:56:14-03:00` — agrees with the pre-registration's "census exit 0". Navigation 30/30 was not re-derived. |

## 3. Findings

### H1 — C1's measured predicate does not entail the declared fix; append-only is unmeasured

`SCORECARD.md:836-841` declares the work as routing R16-V1 into the lesson and
"an append-only lesson-cited QUALITY criterion", then measures only
`^[0-9]+\. .*lessons/` over `^[0-9]+\. `. Nothing in the counter distinguishes
an appended R16-V1 criterion from (a) a lesson-cited criterion about anything
else, or (b) in-place edits of existing criteria.

Exploit a closure can run now:
- Criteria 18, 19 and 20 already carry a `lesson:` citation on
  **continuation** lines (`corpus/QUALITY.md:43,50,72`; 18/19 cite round-14,
  20 cites round-15). Moving that citation
  onto each criterion's first line yields 17/22 = 7.7273 — well over the target
  — with zero new criteria and no R16-V1 routing.
- Appending criterion 23 with a first-line citation to round-17 **M2** (tripwire)
  yields 15/23 = 6.5217 and satisfies the stated target without routing R16-V1.

Tightening: require the closure to cite
`git diff 27cd06f..REV -- corpus/QUALITY.md` and show (i) no changed or deleted
line among criteria 1-22, (ii) exactly one added `^[0-9]+\. ` line, (iii) that
line's first line names `lessons/round-17.md#mistakes M1` and R16-V1.

### H2 — C3 is not falsifiable as written: `N/N` and an unpinned assertion

`SCORECARD.md:857-859`: "hermetic selftest N/N exit 0, and the real round-15
transcripts return the libinput `sudo pacman -S` call as host_mutation".
`N` is a free variable. A one-case selftest is `N/N`; so is a selftest that
omits every class the interface defines. The transcript assertion names neither
the scan set (65 JSONL files exist under the R15 set), nor the expected finding
tuple, nor whether extra findings are failures.

Exploit: ship a three-case selftest (all clean) plus a scan of the one anchor
file; report "3/3 exit 0" and "the libinput call is host_mutation" — C3 passes
while `eval` handling, `sudo`-recursion, `bash -c` recursion, quoted-data
cleanliness and exit-2 semantics are untested.

Tightening: pin `N ≥ 12` and the required cases (incident replica; package
query only; live probe only; permit class; clean quoted data; `bash -c`
recursion; `$(…)` recursion; `env`/`timeout`/`xargs` wrappers; eval `!` line;
invalid JSON line → exit 2; missing directory → exit 2; unparsed fallback),
the verdict schema, and the exact anchor tuple
`(MadoR15.LibinputEvents.jsonl, 54, call_38165, host_mutation)`.

### H3 — The lowest-axis justification is contradicted by the round's own rubric V

`SCORECARD.md:829-834` lists "calibration literal 14/22 = 6.3636 (lowest active
scored); coverage U-route 7/7 …" and omits the row the same pre-registration
declares twenty lines later: V baseline 2/6 = **3.3333** (`:851`). Under the
recorded `10*count/denominator` rule, 3.3333 < 6.3636. Either:

- V is a scored row → the lowest active axis is coverage/V, `C1 calibration
  (lowest axis)` is mislabeled, and C2 is the lowest-axis claim; or
- V is a supplementary census, not an axis row → this must be said, and the
  coverage axis score stays U 7/7 = 10.

The text states neither. A closure can therefore claim "calibration was the
lowest axis, per QUALITY22" (C1 compliance) and, in the same report, score
coverage on V (3.3333 → 6.6667) — while a reviewer applying the axis row would
see coverage fall from 10.0000 to 6.6667, i.e. harm by redefinition. This is
the row-omission/rule-change failure QUALITY22 guards against when it requires
re-deriving every active row before selecting the lowest.

Tightening: one sentence in the pre-registration — "V is / is not an axis row;
the coverage axis score remains / becomes V" — plus, if V is scored, the
lowest-axis sentence naming coverage/V at 3.3333 and C1 restated as a
second-axis claim.

### H4 — C2's instrument post-dates the claim and is stricter than the committed rule

`python3 .ufo/waves/round-17/measure.py REV` is the declared command
(`:850`), but no `measure.py` exists at `0175f13` (fact 10). The in-flight tool
also adds a predicate the pre-registration does not state: four exact section
headings and `[UNK]` in the last (fact 12), versus the committed text's
"first 15 lines carry `source:`… and declares `surface:`" (`:845-849`). A
closure can measure under either reading, and neither is the other.

Mitigation already true: the baseline does reproduce by hand (fact 8), and the
wave item pins the expected `14/22` and `2/6` outputs. That makes the baseline
checkable ex post, not pre-registered.

Tightening: append the exact predicate (including the facet requirement and
the `S\d{3}` token rule) to the pre-registration, or commit `measure.py` with
its SHA-256 in the same append-only erratum, and paste its `27cd06f` /
`0175f13` outputs into `evidence/`.

### H5 — Separability claim is stronger than the round's own plan

`SCORECARD.md:862-863`: "Separable: C1 counts QUALITY text only; C2 needs no
tool or criterion; C3 needs no note or criterion." The in-flight `QualityDraft`
item asks for criterion 23 **and** "a candidate criterion 24 (lesson M2) for
transcript tripwire use". If 24 is admitted, C3 adds a QUALITY criterion and
C1's denominator becomes 24; if 24 is drafted but not admitted, the lesson M2
must not present it as active. The pre-registration must settle which.

Tightening: "Criterion 23 only; criterion 24 is a draft, not admitted this
round" (or restate C1's target with a denominator rule).

### M1 — C1's label check has no pre-registered predicate, and the checker's predicate is narrower than the planned criterion

`SCORECARD.md:838-839` says "a label check shown to fail on the round-16 lesson
line" without a command, receipt path, expected output or pass/fail predicate.
The in-flight check is red for the right reason (receipt-stage token absence),
but it tests "receipt at `rev_receipt` carries the token", not the planned
criterion's "records that token **at the revision it describes**" — it never
compares the receipt's `measured_commit` to `rev_receipt` or to the revision the
document describes (fact 13).

Exploit: a later doc can cite a receipt at a revision where the token was
added, even though the receipt measured a different commit, and the check stays
green.

Tightening: name `label-check.py`, the red claim id and its exact
`LABEL … MISMATCH` line, and add `measured_commit == rev_receipt` (or have the
claim carry a separate `measured_rev` that must match the receipt field).

### M2 — C1's "target ≥ 15/23" is ambiguous and presumes the wrong denominator

15/23 assumes exactly one added criterion. `QualityDraft` plans criterion 23
and candidate 24, i.e. denominator 24. Then 16/24 = 0.6667 (passes as a ratio,
fails as "15/23") and 15/24 = 0.6250 (a **regression** below 14/22 = 0.6364 if
criterion 24's citation wraps). "≥ 15/23" does not say whether it means the
fraction or the ratio 0.6522, and the denominator is not pinned.

Tightening: "literal fraction strictly greater than 14/22 (≥ 15/23 with exactly
one added, first-line-cited criterion; any second added criterion must also be
first-line-cited or the claim is restated at the new denominator)". Paste both
counts.

### M3 — QUALITY22's semantic counter is not reported

QUALITY22 (criterion 22) says "Report literal versus semantic citation counters
separately rather than silently changing the rubric." C1 reports only the
literal command. Semantic is 17/22 = 7.7273 (fact 2). The pre-registration
therefore neither discharges the criterion that justified the axis selection
nor pins which counter the closure may quote.

Tightening: C1's before/after receipt must carry both counters (literal and
whole-block semantic), with the same commands for each.

### M4 — R16-V1's remediation location is ambiguous

R16-V1 routed the fix as "Append a correction naming the superseded text" in
the round-16 lesson. C1 routes it to a **new** lesson M1 plus a criterion; the
committed text does not require an erratum in `corpus/lessons/round-16.md`.
The in-flight `ErratumDraft` plans exactly that append, but the acceptance does
not. A closure can close R16-V1 while `round-16.md:131` still mislabels the
receipt for every later reader of that lesson.

Tightening: C1 requires (i) the append-only erratum in `round-16.md` quoting
the superseded lines and naming the recut receipt, (ii) the label check red at
`27cd06f` (pre-erratum revision) and green after, (iii) the round-17 M1 row.

### M5 — C2's "admitted", "new" and "documentary route" are not in the predicate

`measure.py` counts any `corpus/knowledge/*.md` at REV that satisfies the
metadata joins (fact 12). It never checks README admission, never checks that
the file is absent at `27cd06f`, and never inspects whether the facet bodies
contain a route. `section_body` returns `''` for an empty section, and only the
last section must contain `[UNK]`.

Exploit: add to the existing `corpus/knowledge/idle-lock-plane.md` and
`terminals-and-omarchy.md` a `source:` line in the head, `surface: P6`/`P4`, four
headings — three empty, the last containing `[UNK]` — and claim P6/P4 covered.
The planned new notes are then optional, and measure.py reports 4/6.

Tightening: require the path to be absent at `27cd06f` (newness), require its
README index line, and require each facet body to carry at least one line
anchor (`path:line`) or a ≤25-word verbatim quote; `## Unexercised behavior`
still requires `[UNK]`.

### M6 — C2's "target 4/6" does not name the surfaces

The sentence names P6 and P4 as the new notes (`:851-852`), but the target is
only "4/6". A closure could cover P3 Walker and P5 themes instead — including
by amending old notes per M5 — and still report 4/6 while the mission's named
surfaces are untouched.

Tightening: attainment = `count == 4` **and** `{P6, P4} ⊆ covered`; the receipt
lists the covered set.

### M7 — Surface coverage is overclaimable for multi-actor surfaces

P4 is declared as four terminal config trees; all four exist on the host
(fact 9). P6 comprises both `hypridle.conf` and `hyprlock.conf`, both present.
One note declaring `surface: P4` or `P6` counts the whole surface, so a report
can say "terminal emulator configs covered" from a single Alacritty route, or
"idle/lock covered" from a hypridle-only note.

Tightening: either define coverage as "at least one documentary route into the
declared surface, not every actor" (and require the report to name the actors
the route covers), or require one note per actor for P4 and P6.

### M8 — C3's acceptance is narrower than the shared interface

`SCORECARD.md:854-856` says the tool "classifies only commands actually issued
as `bash` tool calls". The shared interface also parses `eval` lines whose
stripped text starts with `!` (tool "eval"). The R15 set contains **zero** such
lines (fact 6), so the red anchor cannot detect the omission; the compound
fixture set does contain `!sudo pacman -S foo` (spec item `TripwireFixturesCompound`).
A bash-only implementation satisfies the C3 sentence and fails the interface.

Tightening: wording "`bash` and `eval` `!` tool calls", and the selftest must
include the eval-bang case.

### M9 — "Agreeing with an independent oracle" has no pinned content

The oracle is a separate seat (spec items `OracleR15`/`R16`/`R13R14` writing
`evidence/oracle-r15.json` etc.), but the pre-registration names no evidence
path, no finding set and no tolerance. The R15 set is 65 JSONL files and will
yield many findings beyond the libinput call, so "agreement" can be cherry-picked.

Tightening: exact anchor tuple match (`file`, `line`, `tool_call_id`, `class`,
`rule`), plus "any difference in the other findings is listed and resolved".

### L1 — "Hermetic" is undefined
Define as synthetic fixtures only: no real transcript, host command, network
or `$HOME` read; selftest self-invokes with `--scan <fixture dirs>`.

### L2 — The P1-P6 labels are not in PROVINCE.md
`PROVINCE.md` has no `P<n>` tokens; the enumeration exists only in
`SCORECARD.md:843-845`. State that the labels are a rubric numbering over the
PROVINCE prose, or append them to PROVINCE.md (L1-owned).

### L3 — The "re-derivation" paragraph is a value restatement for three of four rows
Only calibration carries a command (`:839-841`). Coverage/U, freshness 29/29
and operability 372/372 are cited values with parenthetical provenance, not
re-derived under QUALITY10's `<n> — <command> <date>` and QUALITY22's
"re-derive". I did not re-run the gate (host pause, seat limits), so I can
confirm only that the recorded SCORECARD values agree with the paragraph
(`:399-400` freshness 10.0000; `:529`, `:797` 372/372). The closure should
paste the U census and (L1-only) the gate receipt.

## 4. Top closure moves the current text permits

1. Editing first-line citations of QUALITY 18-20 → 17/22 = 7.7273, target met,
   no R16-V1 routing (H1).
2. A three-case clean selftest and one anchor scan → "N/N exit 0" and the
   libinput call reported (H2, M8).
3. Metadata-only amendments of `idle-lock-plane.md` / `terminals-and-omarchy.md`
   (source line + `surface:` + four headings) → P6/P4 counted, no new notes
   (M5), even if the covered pair is P3/P5 (M6).
4. Adding a criterion citing any lesson → C1 numerator grows without the
   declared criterion (H1, M2).
5. Citing the label check's receipt-stage MISMATCH as proof the revision-binding
   clause works (M1), or citing the ratio 16/24 as "≥ 15/23" (M2).

## 5. Residual risk and verification gaps

- I did not execute `measure.py`, `label-check.py`, the tripwire or the gate;
  they are not my instruments and the seat rules forbid it. My statements about
  them are from reading their source (facts 11-13), not from running them.
- Freshness 29/29 and operability 372/372 are cited from SCORECARD records, not
  re-derived; the host pause bars the gate and live plane. L1 must verify once
  after integration.
- `measure.py`, `label-check.py`, the spec and the two r17 notes are untracked
  and may change before integration; findings about them are current-state,
  not commitments.
- The R15 transcript set was read only where the anchor and the eval-count
  question required it; no other session, credential or `agent.db*` content was
  opened.
- My baseline C2 reproduction (2/6) is hand-derived from the note heads and
  SOURCES cells; it agrees with the pre-registration and with `measure.py`'s
  declared predicate, but it is not a run of the tool.

## 6. Verdict

The pre-registration is directionally sound: the calibration baseline and the
C2 baseline both reproduce (14/22 = 6.3636; 2/6 = 3.3333), the three claims sit
on different rubric families, and C2 is genuinely independent of C1/C3. It is
not yet closure-proof. C3 as written is not a falsifiable acceptance; C1's
measured predicate does not entail its declared fix and its label check has no
pre-registered predicate; C2's operative instrument post-dates the claim and
adds unstated requirements; and the "calibration is the lowest axis" sentence
is contradicted by the rubric V row the same text declares. A closure can
satisfy all three counters without landing the declared artifacts.

Recommended: L1 appends an append-only pre-registration erratum (QUALITY4)
before integration, carrying the tightenings in §3 — V's axis status, C1's
denominator/ratio and diff gate, C1's label-check predicate, C2's exact
predicate + newness + named surfaces, and C3's case set, anchor tuple and
bash+eval wording. Absent that, the round should be admitted only on the
artifacts, not on the counters.
