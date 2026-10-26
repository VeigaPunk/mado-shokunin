# CritClaimWords — wording of the claims, kill rules and the report's likely sentences

Seat `CritClaimWords`, wave `w2`, round 41 (hyaku run 7), lane `mado-shokunin`.
Data `07f2641696b5ac73de1404ea737a9f27e9819aa1`, base `ab2bfaab661c846d1de9d58c01651cd156a13949`, v2 freeze
`294c667901a8c7b7165ba849d03cba9a24c14fa4`, v1 freeze `60c3914154333180450d5da27ba222d5763cc56a`.
Full sentence-by-sentence table with every reproduction: `.ufo/waves/round-41/w2/CritClaimWords/wording.md`.
No tracked file was edited; no scratch tree was created (read-only `git show/grep/ls-tree` + `printf|grep` only). No tool installed.

**Verdict: 4 DATA defects (fixable before the round lands), 4 frozen-wording defects (report as open, no third registration), 3 report
sentences that must be rewritten before they are written, 6 attacks with no defect found.** The scored numbers themselves hold:
`fixtures=39/39 TARGET_MET` and `admitted=1/1 TARGET_MET` at the data commit are reproduced by the committed receipts, and both base
scores are `0`.

---

## A. DATA defects — the L1 can fix these in the closure commit

### F1. The lesson's base-absence command cannot match anything (`corpus/lessons/round-41.md:44`, data commit)

Attacks: the C2 "the lane holds no focus-grab text at base" evidence line — the command that is supposed to establish it.

```
$ printf 'focus_grab\nfocus-grab\nfocus grab\n' | grep -Ei 'focus_grab\|focus-grab\|focus grab'; echo $?
1
$ printf 'focus_grab\nfocus-grab\nfocus grab\n' | grep -Ei 'focus_grab|focus-grab|focus grab'; echo $?
0
$ git grep -lEi 'focus_grab|focus-grab|focus grab' ab2bfaa -- corpus PROVINCE.md SKILL.md tools; echo $?
1
```

Under `-E`, `\|` is a literal pipe, so the lesson's pattern searches for the literal string `focus_grab|focus-grab|focus grab`. The
conclusion is still true (corrected ERE at base exits 1) — this is an evidence-line defect, not a false claim.

**Smallest safe correction:** replace the command with `git grep -lEi 'focus_grab|focus-grab|focus grab' ab2bfaa -- corpus
PROVINCE.md SKILL.md tools` (verified rc=1). The entry's own command (`grep -rli '…\|…'`, BRE) is correct and needs no change.

Impacted axis: coverage (C2 evidence chain).

### F2. Entry §5 asserts a base fact that is false (`corpus/knowledge/hyprland-focus-grab-r41.md:109`)

Attacks: "The lane holds no focus-rule knowledge either." — falsified at base:

```
$ git show ab2bfaa:corpus/knowledge/keybind-rule-semantics.md | grep -niE 'no_focus|stay_focused|focus_on_activate|no_follow_mouse'
189:3. `windows.conf:9` `no_focus on` (6 props: …)
229:  `tag` (throughout), `no_focus` (`windows.conf:9`), …
231:  `geforce.conf`, `moonlight.conf`), `focus_on_activate off` (`telegram.conf:2`),
232:  `no_follow_mouse` (`jetbrains.conf`), `stay_focused` (davinci orphan only),
$ git show ab2bfaa:corpus/knowledge/config-health-report-r3.md | grep -ci focus
1        # `misc:focus_on_activate`
```

The entry's three checked files are clean (verified: `window-rule-effects-getprop.md` 0 focus lines, `workspace-rules-r27.md` 0,
`rule-attribution-r24.md:81` only `jetbrains-focus`) — the defect is that `keybind-rule-semantics.md` was not checked. The entry then
contradicts itself: line 124 says "S287 plus the held rule entries (§5)" while §5 names none.

**Smallest safe correction (line 109, no new `S###` token, so clauses b/g/h are untouched):** "**INF** The lane holds no focus-grab
protocol text at base; it does hold focus-rule facts (`keybind-rule-semantics.md`: `no_focus`, `focus_on_activate off`,
`stay_focused`), so this section re-sources held rule semantics and adds only the tracker record." **Line 124 cell:** "S287 plus the
held rule rows named above (`keybind-rule-semantics.md`: `no_focus`, `focus_on_activate off`)".

Impacted axis: coverage (the entry's novelty claim is the axis).

### F3. r28 is REFUSEd and assimilated in the same round (entry `:15`/`:136` vs lesson Gate line)

Attacks: provenance. Entry `:15` declares `assimilated-from: … focus-control-surfaces-r28.md (sections 1, 2 and 4)`, `:136` says "the
entry rests only on the rows above", and the lesson's Gate says `REFUSE …/focus-control-surfaces-r28.md reason=section 3 rests on a
localized (Japanese) documentation channel, outside PROVINCE.md` — while `registration.md:58` (Frontier step §2b, carried into v2 by "the claims … are unchanged") names the refuse target as "the
Japanese-channel section of `focus-control-surfaces-r28`". A reader cannot tell whether the file is refused or partly admitted.

**Smallest safe correction (Gate line still satisfies clause i: basename in STAGED, ≥ 20 chars, ≥ 4 distinct words, target ≠ every
ADMIT):** `REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md reason=section 3 only, the localized Japanese
documentation channel, is outside PROVINCE.md; sections 1, 2 and 4 are assimilated`. Entry `:136` → "The entry rests on the rows
above; r28's sections 1, 2 and 4 are unrowed corroboration and its section 3 is not a source."

Impacted axis: coverage (sourced-claim provenance).

### F4. `registration.md:30` "the lane holds none of it" survives into v2 by reference and is false

Attacks: the C2 claim sentence (`registration-v2.md`: "the claims, their axes and the base are unchanged"). "It" includes "the
rule-level counterpart", which the lane holds (F2's evidence). Protocol half is true: `git grep -licE 'grab' ab2bfaa --
corpus/knowledge/` exits 1.

**Smallest safe correction:** "the lane holds no text about the focus-grab *protocol* (corrected ERE at base exits 1); the rule-level
counterpart is already held (`keybind-rule-semantics.md`: `no_focus`, `focus_on_activate off`, `stay_focused`), so the entry
re-sources it." (Because `registration-v2.md` is frozen, the closure report must carry this correction rather than the registration.)

Impacted axis: coverage.

---

## B. Frozen-wording defects — report as open (no third registration)

### F5. `registration-v2.md:9-10` "v2 is strictly stronger than v1 on every point it touches (nothing loosened except the b2 sample's name-substring exclusion, replaced by an exact one)" — FALSE, four ways

- **(a) the named exception is a tightening, not a loosening.** v1 excluded `*selftest*`, `*_check*`, `*_run*`, `*_write*`, `main`,
  `usage`; v2 excludes exactly `selftest`, `main`, `usage` and functions inside `selftest`. The exclusion set shrank.
- **(b) undisclosed loosening — clause g's stdlib allowlist gains `select` and `time`.** `git show 07f2641:tools/mado-globals.py |
  grep -nE '^(import|from) '` → `29:import select`, `34:import time`. This is exactly why v1's clause g fails at the data tip:
  `receipts/c1-v1-after-data.txt` → `clauses=a:1 b:1 b2:1 g:0`. The landed tool passes v2's g **only because the allowlist was
  widened**.
- **(c) undisclosed loosening — C2 clause c's base-row equality stops at cell 9.** v1 `old[0][:10] == cells[:10]`
  (`c2-r41-focus-entry.py:218`); v2 `old[0][:9] == cells[:9] and recheck_ok(cells[9]) is not None`
  (`c2-r41-focus-entry-v2.py:333`). Cell 10 is `recheck` (S037 row cells: 9=`2026-10-19`, 10=`on-release`, 11=used-by), so a held
  row's recheck may now be rewritten to any calendar-valid value. (v2 adds a used-by retention check on cell 11 — mixed, not
  strictly stronger.)
- **(d) [INFERENCE] clause d's HTML normalization changed from "tags stripped" to "tags replaced by a space"**, so `<p>foo</p><p>bar</p>`
  → `foobar` (v1) vs `foo bar` (v2): a Gate quote `foo bar` matches v2 and not v1. No counterexample on the data; "every point it
  touches" is unproven for clause d.

**Corrected sentence:** "v2 is stronger on the points w1 falsified; three changes are not strengthenings and are disclosed: clause g's
allowlist gains `select`/`time`; clause c's byte-equality over a held row stops at cell 9, so its `recheck` may be rewritten; clause
d's HTML normalization replaces tags with a space instead of stripping them. The b2 exclusion change is a tightening, not a
loosening."

Impacted axis: operability (clause g is the C1 sandbox boundary) and coverage (clause c is the registry-integrity check).

### F6. `registration-v2.md:50` "the 42 `ExecC1ExtraMutants` mutants each score below MET" — FALSE

```
$ head -1 .ufo/waves/round-41/receipts/ctl-c1-v2.txt
CTL_C1V2: skipped-patterns-absent=4 W1-N14-empty-file-expect-ok W1-N24-ver-5-digits-max W1-N35-read-only-max-bytes W1-N42-live-no-timeout
$ grep -c 'control=W1-N' .ufo/waves/round-41/receipts/ctl-c1-v2.txt
38
```

`K11-ver-5-digits` and `K12-live-no-timeout` (`ctl/run-c1-v2-controls.py:107-108`, `ctl-c1-v2-extra.txt`) re-express W1-N24 and
W1-N42; `W1-N14` and `W1-N35` are exercised by **no** control in v2 (the only mention of `empty-file|read-only|toolarge` in either
receipt is the skipped header). `K10-file-path-name` is a v2-specific `__file__` cheat, not a replacement.

**Corrected sentence:** "38 of the 42 ran and each scored below MET; 4 patterns are absent from the v2 reference, two are re-expressed
as K11/K12 in `ctl-c1-v2-extra.txt`, and W1-N14/W1-N35 are not exercised by any control."

Impacted axis: operability (C1 kill coverage).

### F7. `registration-v2.md:50` "the v1 single-defect mutants" — FALSE twice

(a) The same data commit's lesson says M09 is a two-site mutant (M41-1). (b) The sentence omits the four v1 clause-g cheats the
receipt still runs (`C1-cheat-exec`, `C2-cheat-os-system`, `C3-cheat-socket-import`, `C4-cheat-counter-name`), so "the v1 mutants" is
not the 43 v1 rows (39 M + 4 C).

**Corrected sentence:** "the 39 v1 mutants and the 4 v1 clause-g cheats, patterns re-derived for v2 (M09 stays a two-site mutant,
M41-1)".

### F8. "98 controls" — FALSE for the receipt it names, and double-counted

`registration-v2.md:50` names `receipts/ctl-c1-v2.txt`, which prints `CTL_C1V2: controls=95 correct=95/95`. The extra receipt prints
`controls=3 correct=3/3`. Across both: **98 rows, 97 distinct names** — `K10-file-path-name` runs in both
(nonces `2159ee01e553d9ad`, `40f4231f4ca399c8`), same mutation (`ctl/run-c1-v2-controls.py:109`).

```
$ cat receipts/ctl-c1-v2.txt receipts/ctl-c1-v2-extra.txt | grep -oE 'control=[^ ]+' | wc -l   # 98
$ cat receipts/ctl-c1-v2.txt receipts/ctl-c1-v2-extra.txt | grep -oE 'control=[^ ]+' | sort -u | wc -l   # 97
```

**Corrected sentence:** "98 control runs of 97 distinct controls: `ctl-c1-v2.txt` 95/95 and `ctl-c1-v2-extra.txt` 3/3 (K10 runs in
both)." The composition of the main receipt is 1 reference + 3 do-nothing + 39 mutants + 4 g-cheats + 10 K + 38 W.

Impacted axis: operability.

### F9. `registration-v2.md:51` "so each is killed by its own clause" — TRUE but overstated

65/65 non-P rows are `observed=admitted=0/1 ok=1` (verified). But clause `g` is zero in **24 of 65** rows and `d`+`g` co-fire in 21
(`F1-invented-receipts`, `N03-gate-sha-wrong`, `W12`…`W17`): a forged receipt also breaks the entry's quote binding, so receipt
provenance is not isolated for those rows.

**Corrected sentence:** "every other control scores 0/1 (65/65); its own clause is among the failing ones, and clause g co-fires in 24
because a forged receipt also breaks the entry's quote binding."

---

## C. Report sentences that must not be written as planned

### F10. "no axis harmed" — UNVERIFIABLE at the data commit

```
$ git ls-tree -r --name-only 07f2641 quality/receipts/
quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt   # round 36
quality/receipts/red-axis-publication-stale-at-data-commit.txt
```

No tip transcript exists (the lesson's own D2/M41-4 says it is owed). What exists: `receipts/axis-base.txt` (navigation 58/58,
calibration 55/55, operability 12/12, `mismatched=0 rev=ab2bfaa…`) and `receipts/census-after-data.txt`, byte-identical warning set
to `census-before.txt` (`diff` exit 0, `exit=0`).

**Write instead:** "No axis is touched by either counter's inputs; at the data commit the evidence is the base receipt
(`axis-base.txt`, `mismatched=0`) and an unchanged census (`census-after-data.txt` identical to `census-before.txt`, exit 0). The tip
`MADO_AXIS` receipt is owed at closure (M41-4)."

### F11. "v1's C1 reads 6/24 because the contract changed" — TRUE, but the receipt cannot show it

`c1-v1-after-data.txt` truncates `got`/`want` to the same 120-character prefix, so the difference is invisible in the receipt. The
partition proves it: the 6 passes are exactly the six fixtures that emit **no** final `MADO_GLOBALS:` line (`unreadable0`, `usage0`,
`badexpect0`, `livefail0`, `livewritable0`, `livelarge0`); all 17 final-line fixtures fail on the v2-only `ignored=` field
(`c1-r41-globals.py:45` vs `-v2:66`; tool template `tools/mado-globals.py:162`); `nosess0` fails `rc=4 want=3`
(`UNRECOGNIZED_FORMAT`); clause g fails on the widened allowlist (F5b). No fixture fails on shared behaviour.

**Write instead:** the three named contract changes, not the bare phrase "the contract changed" — and note that the same widening is
what F5b calls a loosening, so the sentence cannot be used as evidence that v2 is strictly stronger.

### F12. "before: the lane has no tool" — TRUE, evidence under-proves it

`ls tools/` = 10 files proves only filenames. The semantic claim needs `git grep -lEi 'Got interface' ab2bfaa -- tools/` (rc=1) and
the naming of the two journal readers: `mado-eventq.py:68,242` reads `wayland-wm@hyprland.desktop.service`; `mado-tripwire.py:268`
only allowlists `wayland-info`. The `globals` hits in base tools are Python builtins (`mado-tripwire.py:80,1293,1490`) and waybar
config (`mado-verify.sh:50,3198,3202`).

**Write instead:** "no lane tool parses the portal's ADVERT grammar or reports per-global versions (`git grep -lEi 'Got interface'
ab2bfaa -- tools/` exits 1; `mado-eventq.py` reads a different unit)".

---

## D. Attacks with no defect found

| attack | command | result |
|---|---|---|
| **Separability** (`registration-v2.md:46`) | `grep -c 'mado-globals' c2-…-v2.py` → 0; `grep -c 'hyprland-focus-grab' c1-…-v2.py` → 0; `grep -c corpus c1-…-v2.py` → 0; C2 path constants are `ENTRIES`, `LESSON`, `FETCH`, `corpus/SOURCES.md`, `corpus/README.md` only | holds as written. Do not reintroduce v1's stronger "each is verifiable without the other having landed" unless tested — the code supports the weaker sentence, not that one |
| **C2 67 controls** | `tail -1 receipts/ctl-c2-v2.txt`; 65 non-P rows `observed=admitted=0/1 ok=1` | 67/67 reproduced |
| **Kill rule** ("anything else is a miss, no narrowing") | both receipts' final lines `TARGET_MET`, exit 0, rev `07f2641` | no narrowing found: clause set `a:1 b:1 b2:1 b3:1 g:1` / `a:1…i:1`, fixture count 39 = 39 |
| **Base scores** | `c1-v2-before-base.txt` `fixtures=0/39 tool=absent`; `c2-v2-before-base.txt` `admitted=0/1` | reproduced |
| **"no data path at the v1 freeze"** | `git ls-tree -r --name-only 60c3914 \| grep -E 'mado-globals\|hyprland-focus-grab\|lessons/round-41'` → rc=1 | reproduced |
| **S290 uncited / no row** | registry grep 0, entry grep 0 | reproduced |
| **39 fixtures = 24 + 15** | v2 docstring fixture list; 24 + 15 named classes | reproduced |
| **clause i's ">= 4 distinct words"** | `c2-…-v2.py:120` `REFUSE_RE … reason=(.{20,})` **and** `:459 len(set(…split())) >= 4`; controls `A04-refuse-reason-one-word`, `A09-refuse-reason-filler` both 0/1 | implemented, not docstring-only — no defect |
| **clause c ">= 3 new ids"** | `c2-…-v2.py:343 len(new_ids) >= 3` | implemented |

---

## Impact summary

- **operability (C1):** scored claim intact (`39/39`); the *control inventory* sentence is wrong twice (F6, F8) and the clause-g
  allowlist widening (F5b) is the one change that makes the landed tool pass v2 and fail v1 — it must be disclosed, not hidden inside
  "nothing loosened".
- **coverage (C2):** scored claim intact (`1/1`); the entry's rule-layer sentence (F2), the refused-and-assimilated provenance (F3) and
  the registration's "holds none of it" (F4) are all false-or-overbroad claims about the lane, and F2 is the one a non-author closure
  reader is most likely to catch, because the counterexample is a base knowledge file.
- **evidence chain:** the lesson's only base-absence command is vacuous (F1) and the tip axis receipt is still missing (F10) — both are
  one-command fixes, neither changes a score.

---

## Quote and tool state

Every quote above is ≤ 25 words and was verified by a script against its source (whitespace-normalized, because the counter
docstrings and the registrations wrap lines): `.ufo/waves/round-41/w2/CritClaimWords/quote-check.txt` →
`QUOTE_CHECK: quotes=21 failures=0 max_words=11`. Sources: `git show 07f2641:<path>` for the lesson and the entry,
`git show ab2bfaa:<path>` for the base knowledge files, and the working-tree files for the two counters and the two registrations.

No tool was installed, no package transaction was run, no git/jj mutating command was issued, no scratch tree was created or left
behind, and no file outside `.ufo/waves/round-41/w2/CritClaimWords/` and this report was written.
