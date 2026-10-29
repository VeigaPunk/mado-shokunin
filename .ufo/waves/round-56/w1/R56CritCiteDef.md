# R56CritCiteDef — attack on the C3 citation definition (round 56, wave w1)

Seat: R56CritCiteDef (critic, leaf, no delegation). Base: `13f0acbe3a15da2d9c08357a576d91dcadc85273`, read only through `git show` / `git ls-tree` on the lane. No tracked file, index, commit or host state was touched. Deliverables: this file and `w1/R56CritCiteDef/` (`pairs-65.tsv`, `c3-base-own-reimpl.txt`, `c3-mechanical-fill-own-reimpl.txt`, `rule-candidates-vs-labels.txt`, `c3count.py`, `fill.py`, `rules.py`, `labels.py` is in scratch only; `pairs-65.tsv` carries its content).

## 0. Bottom line

- The 65 base pairs are real token mentions, but **about one third of them would make `used-by` false** if added: 18 clearly (28%), 21 counting the three leaning-wrong cases (32%). 44 (68%) are supported by the citing text (strict reading: 37, 57%).
- **Eight pairs sit on rows that are rejected or queued.** Filling them gives six rejected rows and two queued rows a back-reference. One of them (S132) is on a `source:` line whose sentence says it "stays queued and supports nothing".
- `missing=0` is reachable mechanically and I demonstrated it: a script that reads no entry prose and copies the regex output into `used-by` gives `missing=0 extra=0 dangling=0 TARGET_MET` (own re-implementation of §C3, §4 below). So the metric measures token-consistency between two derivations of one regex. It cannot separate reliance from name-only mention. Calling it "calibration" overstates it. The honest label is "registry back-reference consistency with token-level mentions".
- Verdict on the claim: the `missing=0` fix is a partial real improvement (about 44 pairs) and a mechanical overstatement (about 21 pairs). The round must disclose both numbers.

## 1. Method

1. Computed the base pairs with my own implementation of registration §C3 (`c3count.py`; fenced-code skip, `(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])`, 11-cell registry rows, `used-by` regex). Base: `entries=70 rows=319 missing=65 extra=0 dangling=0`, matching `claims-frozen.md`.
2. Read the citing line(s) of **all 65 pairs** in context (nearest heading, full text for 15 ambiguous lines). Per pair I recorded status, tier, cited line numbers and a basis sentence in `pairs-65.tsv`.
3. Labels:
   - **U**: the entry uses the row's content as evidence, a line pointer, a receipt, a held file it reads, or a scope statement about what the row retained.
   - **N**: name-only. Id mapping of another document, registry bookkeeping, supersession/rejection/contrast, "not substituted", "stays queued and supports nothing", errata pointers, neighbour pointers.
   - **R**: cited as a source while the row is rejected.
   - **M-U / M-N**: ambiguous; I lean to the label shown.
4. Built a scratch fixture (base tree + the 65 pairs filled into `used-by`) and ran the same definitions on it.
5. Tested three candidate counter-rules against the labels (§5).

## 2. Results

| label | pairs | would `used-by` be right? |
|---|---|---|
| U | 37 | yes |
| M-U | 7 | probably yes (errata or method attribution) |
| M-N | 3 | probably no |
| N | 17 | no |
| R | 1 | no (rejected source) |

Totals: 44 right-leaning, 21 wrong-leaning (18 clear + 3 M-N). Status of the 65 pairs: 57 mined, 6 rejected, 2 queued. The eight non-mined pairs are all N, R or M-N.

Pairs in each group (numbers are rows of `pairs-65.tsv`):

- **N (17):** #9-11 `S187`, `S188`, `S214` in `event-delivery-limits-r26.md:80` (`package S187 → S189, S188 → S201, S214 → S212`, an id mapping); #20-21 `S357`, `S358` in `hyprland-bind-key-match-r50.md:3` ("S357/S358 serve that tool only", bookkeeping); #26 `S045` in `hyprland-config-era-r12.md:139` (errata, S045 rejected); #30 `S007` in `input-debugging-boundaries-r15.md:10` ("S051 supersedes queued S007"); #31 `S043` at `:11` ("distinct from S043's registry scope"); #33 `S040` in `output-colour-boundaries-r14.md:20,106` ("do not apply S040's … governance"; "Reject"); #34 `S005` at `:65` ("Neither the S005 README's earlier commit … is substituted"); #41 `S132` in `terminal-trees-r23.md:1` ("S132 stays queued and supports nothing"); #43 `S094` in `theme-route-r18.md:158-167` (errata; S094 replaced in place by S097, rejected); #45-47 `S119`, `S116`, `S120` in `tripwire-precision-r20.md:146` (supersession and "(S116–S120)" pointer); #56 `S084` in `walker-route-r18.md:327` ("Head source: token S084 … replaced in place by S098", rejected); #61 `S056` in `xdg-terminal-selection-r47.md:11` ("held neighbours … (rows S056-S060)").
- **R (1):** #25 `S030` in `hyprland-config-era-r12.md`. It is on the entry's `source:` line (line 3) and in 10 distinct body lines (12 occurrences). S030 is `rejected` (duplicate of S017). The round-12 lesson moved S030's `used-by` to S017 and removed this entry (`corpus/lessons/round-12.md:123`: `S030 | used-by | hyprland-config-era-r12.md | — | moved to S017`). The base pair is the residue of that decision. A fill would reverse it.
- **M-N (3):** #29 `S359` at `hyprland-dispatcher-dispatch-r51.md:20` (appears only in a "held (cited…)" enumeration); #39-40 `S061`, `S062` in `terminal-route-r17.md:152` ("Source rows: … S061-S062 (rejected)"). Both are rejected and the sentence declares them as the entry's source rows.
- **M-U (7):** #6 `S044` (`config-drift-r12.md:160`, "round-13 S044 cites the actual gate-maintenance rule"); #16-19 `S175`, `S177`, `S158`, `S162` (`hyprctl-verification-layer.md:306`, errata "table from the directives (S175–S177, S158, S162)"); #44 `S113` (`tripwire-binding-boundaries-r21.md:34`, "S113's quoted `os` fact is retained" plus a supersession); #55 `S015` (`walker-route-r18.md:236`, "Per the S015 protocol").
- **U (37):** freshness pointers that cite `pacman.log:2929` (S090) or host file bytes (S091/S096) for the 2.17.2 move (≈20 pairs); event/trace line pointers (`hyprctl-flags-r28`, `request-limits-upstream-r31`, `event-queue-observability-r37`); held file reads (`hyprland-bind-key-match-r50`, `hyprland-dispatcher-dispatch-r51`, `xkb-keymap-compile-r48`, `xdg-terminal-selection-r47` L74); scope/receipt statements (`S041`, `S046`, `S350`, `S057`, `S073`, `S277`).

## 3. Is `missing=0` a calibration improvement?

Argument that it is mechanical and overstates reliance:

1. **Derived, not judged.** `used-by` is checked against the same token regex that defines CITE. A script that never reads prose reaches TARGET_MET. Scratch fixture (base + `used-by` filled from the 65 pairs), own re-implementation:
   ```
   base:  MADO_USED_BY: rev=13f0acbe… entries=70 rows=319 missing=65 extra=0 dangling=0 verdict=TARGET_MISSED missed=missing
   fill:  MADO_USED_BY: rev=853c0f2b… entries=70 rows=319 missing=0 extra=0 dangling=0 verdict=TARGET_MET missed=none
   ```
   The fill touched 45 rows. After it, S030, S045, S061, S062, S084, S094 (rejected) and S007, S132 (queued) each carry a `used-by` entry. Example: `S132 | queued | … | used-by: corpus/knowledge/terminal-trees-r23.md`, while the entry says "S132 stays queued and supports nothing".
2. **The controls do not catch it.** Control 2 (fill-all) is caught only by `extra`. No control covers name-only or rejected-row back-references, so the predicate is satisfiable by the 21-pair wrong state. The harness cannot tell `TARGET_MET` from "correct" here.
3. **Consequence.** `missing=0` means "the registry mirrors token mentions". It does not mean "each back-reference records reliance". About 44 pairs are true improvements. About 21 are false reliance records, and the counter cannot say which.
4. **Declared-limit gap.** `claims-frozen.md` gives C1 a declared-limit paragraph (quote identity, not entailment). C3 has none. It needs one that names the N/R classes above.

## 4. Other defects and ambiguities (with the input that shows them)

- **Range blind spot.** CITE reads literal tokens only. `S175–S177` hides `S176`; `S116–S120` hides `S117`, `S118`; `S056-S060` hides `S057`, `S058`. Five (row, entry) pairs are invisible at base: `S176` in `hyprctl-verification-layer.md:306` (probably a use) and four pointers. A range-expanding counter would move base `missing` from 65 to 70.
- **Dangling blind spot.** 20 of 70 entries have no `source:` line in their first 15 lines. 18 of the 65 pairs sit in those entries, so `dangling` cannot see them. `terminal-trees-r23.md:1` puts `S132` on a `source:` line; `dangling` accepts it because S132 is a registered row, and it does not check status.
- **Registration vs claims-frozen wording.** `claims-frozen.md` (C3) quotes the CORPUS rule as "used-by = … the knowledge entries or lessons **citing** the row". Registration §C3 makes "cite" a literal token. The CORPUS contract text was not under `corpus/` at base, so I could not check the quote. Where the two disagree, registration wins, as instructed. The disagreement is exactly the 21 wrong-leaning pairs.
- **Draft id `S243`.** Present at `request-limits-upstream-r31.md:33`, no registry row (`grep -c '^| S243 '` on SOURCES.md = 0). The exclusion stated in the claim holds.
- **Errata counts as citation.** Most N cases are errata, supersession or pointer sentences. The literal rule counts them as citations because it has no notion of sentence role.

## 5. Candidate counter-rules (tested on my labels; not in force)

| candidate | agreement with my labels | failure mode |
|---|---|---|
| lexeme exclusion (drop lines with "supersed", "replaced", "stays", "distinct from", "neighbour", …) | 56/65 (tp 40, tn 16) | 4 false admits (S187, S188, S214, S094); 5 false rejects (S044, S113, S041, S091, S073). **Tuned after labelling, so optimistic.** |
| locator/evidence cue (`:\d`, `§`, `line`, `sha`, `INF`, `held`, …) | 48/65 | 14 false admits (most N errata lines carry locators) |
| `source:`-header only | 20/65 | drops 44 of 45 positives; base count collapses. Not acceptable. |

No regex I tried is precise. A satisfiable, honest rule needs a reviewed exemption list, not a regex. Proposal for a **new versioned registration** (not this round; the frozen rule forbids it now):

- **CITE-v2 = CITE-v1 minus a NAME-ONLY allowlist.** Each entry is keyed by (S-id, entry path, sha256 of the stripped cited line) and carries a reason that quotes the sentence. A key whose line changed or is absent at `--rev` is a setup error (exit 2), so an exemption cannot persist silently.
- **Leg `status`.** For each (S, entry) pair not on the allowlist, the row must be `mined`; violations counted as `cited_nonadmitted`.
- **Expand `Sa–Sb` ranges** before CITE, so the five hidden pairs are seen and classified.
- **Base catch (inference from my labels, not run):** about 46 unresolved pairs under `missing` (44 U/M-U, `S176`, `S359`) and `cited_nonadmitted=3` (`S030`, `S061`, `S062`). Still TARGET_MISSED.
- **Mechanical fill under v2 (inference, not run):** `missing` closes, but `cited_nonadmitted` stays 3. S030 and S061/S062 can only be fixed by editing entry text (replace S030 by S017; drop the rejected rows from "Source rows"), which this round's frozen rule forbids (used-by edits only). That is an honest stop, not a pass.

Limits of this proposal: the allowlist is judgment. A second non-author reader must review it. It does not prove entailment; that stays with the wave-2 sentence-to-pin audit.

## 6. What the report must disclose

1. `missing=0` after a mechanical fill: about 44 real improvements and about 21 pairs that assert reliance the text does not support (18 clear). Eight of the pairs are on rejected or queued rows.
2. The label "calibration" is not earned by TARGET_MET alone. Recommend the lesson say "registry back-reference consistency (token-level)".
3. S030 is cited as a source by a rejected row's duplicate; the round-12 decision to move it to S017 is not reflected in the entry.
4. Labels are one reader's judgment (this seat, non-author). Ten pairs are ambiguous (M-U 7, M-N 3). The per-pair basis is in `pairs-65.tsv`.
5. The lexeme-exclusion agreement (56/65) was tuned after labelling and is optimistic.
6. Range blind spot (5 pairs) and dangling blind spot (18 pairs in 20 entries without `source:`).
7. The C3 declared-limit paragraph is missing.

## 7. Not verified / not run

- I did **not** run the lane's `quality/counters/c3-r56-used-by.py` or `quality/check-r56-controls.py` (not checked for presence at base; C3 controls not executed). All counts above come from my own re-implementation of registration §C3, which reproduces the claimed base numbers (65/319/70).
- The CORPUS contract text was not available under `corpus/` at base; the quoted "citing" rule was not checked against its source.
- The "S030 used-by moved to S017" fact is from `corpus/lessons/round-12.md:123` and `corpus/SOURCES.md:414`; I did not re-verify the whole round-12 lesson.
- The scratch fixture (`853c0f2`) was removed after use; reproduction: `python3 -I c3count.py --repo <fixture> --rev <rev>` with `fill.py` as above.
- Hold-out fixtures were not looked for or used.
- No tools were installed; no host reads were made.
