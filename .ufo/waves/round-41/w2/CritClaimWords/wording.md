# Wording attack — every claim sentence a hostile closure reader can call false

Seat `CritClaimWords`, wave `w2`, round 41. Lane `mado-shokunin`. Data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`, base
`ab2bfaab661c846d1de9d58c01651cd156a13949`, v2 freeze `294c667901a8c7b7165ba849d03cba9a24c14fa4`, v1 freeze
`60c3914154333180450d5da27ba222d5763cc56a`. All commands below were run from the lane root; every claim is either a command with its
output or is marked `[INFERENCE]`.

Verdict key: **FALSE** (a counterexample exists) · **OVERBROAD** (true only in a narrower form) · **UNVERIFIABLE** (no committed
observable at the data tip) · **TRUE** (reproduced; wording still improved).

---

## 1. "Before: the lane has no tool that reads the compositor's advertised protocol set" — OVERBROAD evidence

`registration.md:17-18` (carried into v2 by "the claims … are unchanged").

The claim is **TRUE**, but the parenthesis that carries it (`ls tools/` holds ten files, none for globals) proves only that no
*filename* matches. It does not exclude a tool that reads the set under another name.

```
$ git ls-tree -r --name-only ab2bfaa tools/ | wc -l
10
$ git grep -lEi 'Got interface' ab2bfaa -- tools/
$ echo $?
1
$ git grep -liE 'globals' ab2bfaa -- tools/
ab2bfaa:tools/mado-tripwire.py        # :80, :1293, :1490 — Python builtins globals()/locals()/vars()
ab2bfaa:tools/mado-verify.sh          # :50, :3198, :3202 — waybar `bar_globals`
```

The two journal readers are named and harmless to the claim: `tools/mado-eventq.py:68,242` reads
`wayland-wm@hyprland.desktop.service` (a different unit, `-o cat`), and `tools/mado-tripwire.py:268` only allowlists
`wayland-info` as a live-probe binary name.

**Corrected sentence:** "Before: no lane tool parses the portal's ADVERT grammar or reports per-global versions —
`git ls-tree ab2bfaa tools/` = 10 files, `git grep -lEi 'Got interface' ab2bfaa -- tools/` exits 1; the two journal readers read a
different unit (`mado-eventq.py:68,242`) and only allowlist `wayland-info` (`mado-tripwire.py:268`)."

## 2. "the lane holds none of it" — FALSE

`registration.md:30` (C2; the v2 registration says "the claims, their axes and the base are unchanged", so this sentence still
governs C2). "It" is defined on the same line as four components, the last of which is "the rule-level counterpart". The lane
**does** hold the rule-level counterpart at base:

```
$ git show ab2bfaa:corpus/knowledge/keybind-rule-semantics.md | grep -niE 'no_focus|stay_focused|focus_on_activate|no_follow_mouse'
189:3. `windows.conf:9` `no_focus on` (6 props: …)
229:  `tag` (throughout), `no_focus` (`windows.conf:9`), …
231:  `geforce.conf`, `moonlight.conf`), `focus_on_activate off` (`telegram.conf:2`),
232:  `no_follow_mouse` (`jetbrains.conf`), `stay_focused` (davinci orphan only),
$ git show ab2bfaa:corpus/knowledge/config-health-report-r3.md | grep -niE 'focus'
526:| `misc:focus_on_activate` | 1 | set | agreement |
```

The protocol half of the claim survives: `git grep -lEi 'focus_grab|focus-grab|focus grab' ab2bfaa -- corpus PROVINCE.md SKILL.md
tools` exits 1, and `git grep -licE 'grab' ab2bfaa -- corpus/knowledge/` exits 1 (no base knowledge file mentions "grab" at all).

**Corrected sentence:** "the lane holds no text about the focus-grab *protocol* (corrected ERE at base exits 1; no base knowledge
file contains `grab`); the *rule-level* counterpart is already held (`keybind-rule-semantics.md`: `no_focus`, `focus_on_activate off`,
`stay_focused`), so the entry's rule section re-sources held semantics instead of adding coverage."

## 3. "strictly stronger than v1 on every point it touches (nothing loosened except the b2 sample's name-substring exclusion, replaced by an exact one)" — FALSE, four ways

`registration-v2.md:9-10`.

**(a) The named exception is a tightening, not a loosening.** v1 excluded functions named `*selftest*`, `*_check*`, `*_run*`,
`*_write*`, `main`, `usage` (`quality/counters/c1-r41-globals.py`, clause b2); v2 excludes exactly `selftest`, `main`, `usage` and
functions defined inside `selftest` (`c1-r41-globals-v2.py`, clause b2). The exclusion set shrank, so more sites are mutable.

**(b) Undisclosed loosening — clause g's stdlib allowlist gains `select` and `time`.** v1: "argparse collections itertools os re
shutil stat subprocess sys tempfile"; v2 adds `select` and `time`. The data tool imports both:

```
$ git show 07f2641:tools/mado-globals.py | grep -nE '^(import|from) '
29:import select
34:import time
$ grep -n 'PRED-C1-r41-v1 clause=b2' -A0 .ufo/waves/round-41/receipts/c1-v1-after-data.txt | tail -1   # (see next)
$ tail -3 .ufo/waves/round-41/receipts/c1-v1-after-data.txt
PRED-C1-r41-v1 clauses=a:1 b:1 b2:1 g:0
```

So the landed tool satisfies v2's g only because the allowlist was widened; under v1's g it cannot pass.

**(c) Undisclosed loosening — C2 clause c stops the base-row byte-equality at cell 9.** Cell 10 is `recheck` (S037 row: cell 9 =
`2026-10-19`, cell 10 = `on-release`, cell 11 = used-by):

```
$ grep -n 'old\[0\]' quality/counters/c2-r41-focus-entry.py        # v1
218:                and old[0][:10] == cells[:10]
$ grep -n 'old\[0\]' quality/counters/c2-r41-focus-entry-v2.py     # v2
333:                and old[0][:9] == cells[:9] and recheck_ok(cells[9]) is not None
```

v1 required a held row's `recheck` cell to stay byte-equal; v2 only requires it to be *valid*, so a held row's recheck may be
rewritten (e.g. to a far-future ISO date). v2 does add a used-by retention check on cell 11, so the net is mixed, not strictly
stronger.

**(d) [INFERENCE] clause d's HTML normalization is not comparable.** v1: "tags, scripts, styles stripped, entities decoded,
whitespace collapsed"; v2: "HTML receipts: tags replaced by a space, scripts and styles dropped". `<p>foo</p><p>bar</p>` normalizes
to `foobar` under v1 and `foo bar` under v2, so a Gate quote `foo bar` matches v2 and not v1. No counterexample on the data; the
point is that "every point it touches" is unproven for clause d.

**Corrected sentence:** "v2 is stronger on the points w1 falsified; three changes are not strengthenings and are disclosed here —
clause g's stdlib allowlist gains `select` and `time` (the tool imports both, `tools/mado-globals.py:29,34`), clause c's
byte-equality over a held row now stops at cell 9 so its `recheck` may be rewritten, and clause d's HTML normalization replaces tags
with a space instead of stripping them, so a quote spanning two blocks is matchable where v1 required it contiguous. The b2
name-substring exclusion change is a tightening, not a loosening."

## 4. The counts — 47 TRUE-as-total / 98 FALSE / 67 TRUE

| count | claimed where | what the receipts say | verdict |
|---|---|---|---|
| 47 | v1 C1 | `CTL_C1: controls=47 correct=47/47` = 1 reference + 3 do-nothing + 39 mutants (`M01`–`M39`) + 4 g-cheats (`C1-cheat-exec` … `C4-cheat-counter-name`) | **TRUE as a control total**, FALSE as "47 mutants" |
| 98 | `registration-v2.md:50` names `receipts/ctl-c1-v2.txt` and the w2 context says "98 controls" | that receipt prints `CTL_C1V2: controls=95 correct=95/95`; `ctl-c1-v2-extra.txt` prints `controls=3 correct=3/3`; 98 rows across both, **97 distinct names** (`K10-file-path-name` runs in both, nonces `2159ee01e553d9ad` and `40f4231f4ca399c8`) | **FALSE for the named receipt**, and double-counted |
| 67 | C2 v2 | `CTL_C2V2: controls=67 correct=67/67`; 65 non-P rows all `observed=admitted=0/1 ok=1` | **TRUE** |

```
$ head -1 .ufo/waves/round-41/receipts/ctl-c1-v2.txt
CTL_C1V2: skipped-patterns-absent=4 W1-N14-empty-file-expect-ok W1-N24-ver-5-digits-max W1-N35-read-only-max-bytes W1-N42-live-no-timeout
$ cat receipts/ctl-c1-v2.txt receipts/ctl-c1-v2-extra.txt | grep -oE 'control=[^ ]+' | wc -l   # 98
$ cat receipts/ctl-c1-v2.txt receipts/ctl-c1-v2-extra.txt | grep -oE 'control=[^ ]+' | sort -u | wc -l   # 97
```

**Corrected sentence:** "C1 v2: 98 control *runs* of 97 distinct controls — `ctl-c1-v2.txt` 95/95 and `ctl-c1-v2-extra.txt` 3/3
(`K10-file-path-name` runs in both). C1 v1: 47 controls (1 reference, 3 do-nothing, 39 mutants, 4 clause-g cheats). C2 v2: 67/67."

## 5. "the 42 `ExecC1ExtraMutants` mutants each score below MET" — FALSE

`registration-v2.md:50`. The receipt's own first line reports four patterns absent, and only 38 `W1-N*` rows exist:

```
$ grep -c 'control=W1-N' .ufo/waves/round-41/receipts/ctl-c1-v2.txt
38
```

`K11-ver-5-digits` and `K12-live-no-timeout` (`ctl-c1-v2-extra.txt`) re-express `W1-N24` and `W1-N42`;
`W1-N14-empty-file-expect-ok` and `W1-N35-read-only-max-bytes` are exercised by no control at all in v2.

**Corrected sentence:** "38 of the 42 `ExecC1ExtraMutants` mutants ran and each scored below MET; 4 patterns are absent from the
v2 reference (`skipped-patterns-absent=4`, first line of `ctl-c1-v2.txt`), two are re-expressed as `K11`/`K12` in
`ctl-c1-v2-extra.txt`, and `W1-N14`/`W1-N35` are not exercised by any control."

## 6. "the v1 single-defect mutants (patterns re-derived for v2)" — FALSE twice

`registration-v2.md:50`. (a) The lesson at the same data commit proves `M09` is a two-site mutant: "M41-1 - two single-edit mutants
of the reference were equivalent" (`corpus/lessons/round-41.md`, §Mistakes). (b) The sentence omits the four v1 clause-g cheats that
the receipt still runs (`C1-cheat-exec`, `C2-cheat-os-system`, `C3-cheat-socket-import`, `C4-cheat-counter-name`), so "the v1
mutants" is not the 43 v1 rows (39 M + 4 C).

**Corrected sentence:** "the 39 v1 mutants and the 4 v1 clause-g cheats, patterns re-derived for v2 (M09 stays a two-site mutant,
M41-1)".

## 7. "every other control scores 0/1 … so each is killed by its own clause" — TRUE, attribution overstated

`registration-v2.md:51`. 65/65 non-P rows are `observed=admitted=0/1 ok=1`. But its own clause is not the only one that fires:
clause `g` is zero in 24 of the 65 rows, and 21 rows are killed by `d` and `g` together (`F1-invented-receipts`, `N03-gate-sha-wrong`,
`W12`…`W17`). A forged receipt breaks the entry's quote binding, so the receipt-provenance clause is not isolated for those rows.

**Corrected sentence:** "every other control scores 0/1 (65/65); its own clause is among the failing ones, and clause g co-fires in
24 of them because a forged receipt also breaks the entry's quote binding, so receipt provenance is not isolated for those rows."

## 8. "v1's C1 reads 6/24 because the contract changed" — TRUE, and now provable by partition

The receipt truncates `got`/`want` to the same 120-character prefix, so the receipt alone cannot show *where* the lines differ.
The partition does:

- the 6 passes are exactly the six v1 fixtures that emit no final `MADO_GLOBALS:` line — `unreadable0`, `usage0`, `badexpect0`,
  `livefail0`, `livewritable0`, `livelarge0` (`receipts/c1-v1-after-data.txt`, `ok=1 ok`);
- all 17 fixtures that compare a final line fail (`gen0`–`gen7`, `diff0`, `diff1`, `expect0`, `expectmiss0`, `nosess1`, `toolarge0`,
  `live0`, `live1`, `liveenv0`), because the v2 final line carries `ignored=<n>` and the v1 grammar has no such field
  (`c1-r41-globals.py:45` vs `c1-r41-globals-v2.py:66`; tool template `tools/mado-globals.py:162`);
- `nosess0` fails `rc=4 want=3` — the v2 `UNRECOGNIZED_FORMAT` verdict;
- clause `g` fails on the widened allowlist (item 3b): `clauses=a:1 b:1 b2:1 g:0`.

No fixture fails on behaviour the two contracts share. **Corrected sentence:** "v1 reads 6/24 at the data tip: the 6 passes are
exactly the fixtures that emit no final `MADO_GLOBALS:` line; 17 fail on the v2-only `ignored=` field, `nosess0` on the v2
`UNRECOGNIZED_FORMAT` verdict (rc 4 vs 3), and clause g on the widened allowlist (`select`, `time`)."

## 9. "no axis harmed" — UNVERIFIABLE at the data commit

No tip axis transcript exists at `07f2641`:

```
$ git ls-tree -r --name-only 07f2641 quality/receipts/
quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt     # round 36
quality/receipts/red-axis-publication-stale-at-data-commit.txt
```

The lesson itself says the tip receipt is still owed (`corpus/lessons/round-41.md` D2 and M41-4). What does exist:
`receipts/axis-base.txt` (navigation 58/58, calibration 55/55, operability 12/12, `mismatched=0 rev=ab2bfaa…`) and
`receipts/census-after-data.txt`, whose warning set is byte-identical to `census-before.txt` (`diff` exit 0, `exit=0`).

**Corrected sentence:** "No axis is touched by either counter's inputs; at the data commit the evidence is the base receipt
(`axis-base.txt`, `mismatched=0`) and an unchanged census (`census-after-data.txt` identical to `census-before.txt`, exit 0). The tip
`MADO_AXIS` receipt is owed at closure (M41-4)."

## 10. Separability — TRUE, no defect found

`registration-v2.md:46`. Verified by the counters' own path constants and by cross-reference counts:

```
$ grep -c 'mado-globals' quality/counters/c2-r41-focus-entry-v2.py        # 0
$ grep -c 'hyprland-focus-grab' quality/counters/c1-r41-globals-v2.py     # 0
$ grep -c 'corpus' quality/counters/c1-r41-globals-v2.py                  # 0
$ grep -nE 'ENTRIES|LESSON|FETCH|SOURCES.md|README' quality/counters/c2-r41-focus-entry-v2.py
102:ENTRIES = ("corpus/knowledge/hyprland-focus-grab-r41.md",)
103:LESSON  = "corpus/lessons/round-41.md"
104:FETCH   = ".ufo/waves/round-41/fetch/"
488/489: corpus/SOURCES.md (rev and base)   491: corpus/README.md
```

Do **not** reintroduce v1's extra sentence "Each is verifiable without the other having landed" unless it is tested: the statement
above is what the code supports (C2 reads the freeze's `fetch/` artifacts, which are not C1 output, so the stronger sentence is
probably true — but "probably" is not a receipt).

## 11. Entry §5 "The lane holds no focus-rule knowledge either." — FALSE, and self-contradictory

`corpus/knowledge/hyprland-focus-grab-r41.md:109` (data commit). Falsified by item 2's evidence
(`keybind-rule-semantics.md:189,229,231,232`). Its own sub-claims about the three files it *did* check are true:

```
$ git show ab2bfaa:corpus/knowledge/window-rule-effects-getprop.md | grep -ci focus   # 0
$ git show ab2bfaa:corpus/knowledge/workspace-rules-r27.md | grep -ci focus          # 0
$ git show ab2bfaa:corpus/knowledge/rule-attribution-r24.md | grep -ni focus
81:`windowrule`, 3 block `windowrule`, 2 `layerrule`); 3 named block rules (`geforce`, `jetbrains-focus`,
```

and the entry's own command is correct BRE (`grep -rli 'a\|b'`, where `\|` *is* alternation) — the defect is the conclusion, not
the command. Line 124 then contradicts line 109: "| How is ordinary window focus decided instead? | S287 plus the held rule entries
(§5) |" — §5 names no held entry.

**Corrected line 109:** "**INF** The lane holds no focus-grab protocol text at base; it does hold focus-rule facts
(`keybind-rule-semantics.md`: `no_focus`, `focus_on_activate off`, `stay_focused`), so this section re-sources held rule semantics
and adds only the tracker record." **Corrected line 124 cell:** "S287 plus the held rule rows named above (`keybind-rule-semantics.md`:
`no_focus`, `focus_on_activate off`)".

## 12. The lesson's base-absence command is vacuous — DATA defect

`corpus/lessons/round-41.md:44` (data commit): `git grep -lEi 'focus_grab\|focus-grab\|focus grab' ab2bfaa -- corpus PROVINCE.md
SKILL.md tools` — under `-E`, `\|` is a **literal pipe**, so the pattern matches the literal string `focus_grab|focus-grab|focus grab`.

```
$ printf 'focus_grab\nfocus-grab\nfocus grab\n' | grep -Ei 'focus_grab\|focus-grab\|focus grab'; echo $?
1
$ printf 'focus_grab\nfocus-grab\nfocus grab\n' | grep -Ei 'focus_grab|focus-grab|focus grab'; echo $?
0
```

The conclusion still holds (corrected ERE at base exits 1), so this is a one-line evidence defect, not a false claim.

**Corrected command:** `git grep -lEi 'focus_grab|focus-grab|focus grab' ab2bfaa -- corpus PROVINCE.md SKILL.md tools` (rc=1).

## 13. Provenance contradiction: r28 is REFUSEd and assimilated — DATA defect

- entry `:15` `assimilated-from: … focus-control-surfaces-r28.md (sections 1, 2 and 4; its section 3 is … not cited here)`;
- entry `:136` "the entry rests only on the rows above";
- lesson Gate: `REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md reason=section 3 rests on a localized
  (Japanese) documentation channel, outside PROVINCE.md`;
- `registration.md:58` (Frontier step §2b): "the Japanese-channel section of `focus-control-surfaces-r28`" — the
  section, not the file.

A reader cannot tell whether the file is refused or partly admitted. **Corrected REFUSE line** (keeps the STAGED basename so clause i
still matches, ≥ 20 characters, ≥ 4 distinct words): `REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md
reason=section 3 only, the localized Japanese documentation channel, is outside PROVINCE.md; sections 1, 2 and 4 are assimilated`.
**Corrected entry `:136`:** "The entry rests on the rows above; r28's sections 1, 2 and 4 are unrowed corroboration and its section 3
is not a source."

---

## Sentences that survive a hostile read unchanged

| sentence | why |
|---|---|
| `fixtures=39/39 verdict=TARGET_MET` / `admitted=1/1` at `07f2641` | `receipts/c1-v2-after-data.txt`, `c2-v2-after-data.txt`, exit 0 |
| base `0/39 tool=absent` / `0/1` | `c1-v2-before-base.txt`, `c2-v2-before-base.txt` |
| "no `tools/mado-globals.py`, no entry, no registry row, no lesson at `60c3914`" | `git ls-tree -r --name-only 60c3914 \| grep -E 'mado-globals\|hyprland-focus-grab\|lessons/round-41'` → rc=1 |
| "S290 is not cited by the entry and has no row" | registry grep 0, entry grep 0 |
| "39 fixtures = 24 + 15" | v2 docstring fixture list; 24 + 15 named classes |
| C2 v2 67/67 | receipt |
