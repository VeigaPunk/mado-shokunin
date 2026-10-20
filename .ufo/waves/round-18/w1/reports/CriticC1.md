# CriticC1 — is C1 (criteria 24-26) calibration or count inflation?

Seat: MadoR18.CriticC1 (critic, read-only). Baseline `d9a5a18`. I read the drafts
`.ufo/waves/round-18/drafts/QualityDraft.md` and `LessonDraft.md`, plus
`.ufo/waves/round-18/receipt-check.py` and `receipt-claims.json` as they stood
during this review. I ran no lane gate. I made no lane VCS write. I installed no tool.
Every measurement below is a read-only `git show`/grep or a `/tmp` shell repro.

## Verdict

**As drafted, C1 is partly count inflation.**

- Each of the three criteria restates an existing criterion (3, 6, 9, 13, 23) and adds a small new part.
- Two of the three runnable checks do not exercise that new part.
- One check would pass a broken fix.

The score cannot tell the two apart: c1 rises for any appended numbered line that contains `lessons/`.

**What a non-author needs to agree it is calibration.** For each new criterion, show one real artifact from `d9a5a18` that meets two conditions:

- the existing criterion checks accept it (for 23, that check is `label-check.py`);
- the new criterion's check rejects it.

Add a green control that the new check accepts, where today it rejects because of label syntax.

**If C1 is corrected as below, I would accept:**

- 24 as a real change, if it is scoped to receipt presence plus tool identity;
- 25 only if its check runs the pre-tightening instrument;
- 26 only if its check is behavioural, and the census does not gate on zero flags.

## Axes

- **Calibration (claimed):** does each criterion change an admission decision?
- **Operability (harm watch):** the gate and the hermetic 372/372 suite.
- **Provenance integrity:** do re-cut receipts keep their identity?
- **Discernment:** would a non-author agree?

## 1. The instrument rewards appending (strongest general counterexample)

`/tmp` computation on `git show d9a5a18:corpus/QUALITY.md`, using the `measure.py:92-93` regexes:

| text | literal c1 |
|---|---|
| baseline | 15/23 = 6.5217 |
| + three one-line restatements, e.g. `24. Criterion 9 applies to scan receipts too. (lesson: lessons/round-18.md#mistakes M1)` | **18/26 = 6.9231 — target met** |
| + one honest criterion whose citation wraps onto line 2 | 15/24 = 6.25 (**score falls**) |
| k restatements, k = 1/3/5/10 | 6.67 / 6.92 / 7.14 / 7.58 |

Semantic counter (QUALITY 22 asks for it separately): criteria 18-20 cite `lessons/` on continuation lines. That makes the baseline 18/23 = 7.83, and 21/26 = 8.08 after round 18.

**Impact.** The score delta is evidence of nothing beyond format. Only the per-criterion differential check below can carry the claim. The report should state both counters (literal +0.40, semantic +0.25) and should not present the literal rise as a discernment gain on its own.

## 2. Per-criterion analysis

### Criterion 24 (R17-V1/V2 — receipt tool sha + measured_commit)

**Restated parts**

- **"A claimed re-cut is a committed receipt."** This is criterion 2 (no source) plus criterion 13: `lessons/round-17.md:175-176` cites no receipt at all.
- **"A report cites the measured revision's tool sha and labels any later one."** This is criterion 6 ("named revision"). The value `7a98720e…` is the true tool sha at `f71ccbe`; the defect is that it was cited unlabelled, not that a wrong digest was published.
- **Lane precedent.** `QUALITY.md:57-61` (R13-V2/V3) already ruled that "future standalone selftest receipts carry their resolved commit and raw gate digest locally". It explicitly introduced "No duplicate provenance criterion". `QUALITY.md:65-70` (R14-V1) repeats that ruling. A new numbered provenance criterion that does not cite and supersede those paragraphs silently reverses a recorded rejection, which is a criterion 5 problem.

**New part (a real discernment change)**

- **Presence.** Criterion 23 binds the revision only "When the receipt records a `measured_commit`". `label-check.py:133` reads `measured_commit` as optional. So a sentence citing `tripwire-r13.txt` with the token `findings` passes 23. The receipt's first line is `MADO_TRIPWIRE: findings`, and its JSON keys are `counts, exit, files, findings, permitted, schema, unpermitted`. Neither a tool sha nor a revision is present (grep at `d9a5a18`: 0 × `962919ce`, 0 × `7a98720e`, 0 × `measured_commit` in all six receipts). Under 24 the same citation is rejected. This is a real differential (derived from reading the code; I did not run label-check on it).
- **Tool identity resolution.** `receipt-check.py:99-103` hashes `git show <measured_commit>:<tool>`. I measured with rc captured: `f71ccbe → 7a98720ed3c0ea16…`; `0ab1ccc` and `d9a5a18 → 962919cec38ab81d…`.

**Counterexamples and defects in the draft check**

1. **The interface disagrees with the file.** QualityDraft line 4 describes `checks/receipt-check.py RECEIPT...` with `RECEIPT_SUMMARY: 0/4`. The file that exists is `.ufo/waves/round-18/receipt-check.py`, which reads a claims JSON and prints `EXPECT_SUMMARY`. `checks/` does not exist. Criterion 8 means the criterion must cite the landed path and output.
2. **A false red inflates "able to fail".** QualityDraft's red set includes `label-check-final.txt`. That file does carry `measured_commit=f71ccbe525c7…` (40-hex, line 11) and the tool digest in `sha256sum` format (line 12, `a6512a01…  .ufo/waves/round-17/label-check.py`). `HDR_SHA` accepts only a `tool_sha256=` label, so the check reports a provenance-complete receipt as MISSING. It should be a **green control**: accept a `sha256sum` line whose path equals the claim's tool, or drop the file from the red set and say why.
3. **False tool identity for the join.** `receipt-claims.json` binds `tripwire-pacmanlog-join.txt` to `tools/mado-tripwire.py`. The join's own header says it was produced by L1's `awk … /var/log/pacman.log` over tripwire findings. Its PENDING-L1 re-cut expects `ok`, which means stamping the tripwire's sha onto a receipt the tripwire did not produce. That is false provenance. Bind it to its real producer (a committed join script) or to `{tool: awk-join, inputs: [tripwire receipt sha, pacman.log line range]}`.
4. **R17-V2 is mislabelled and has no red.** The anchor-r15 claim's note says "R17-V2", but R17-V2 is the **report sentence** at `.ufo/reports/round-17/mado.md:76`. That file is in the fleet repo, and no claim exercises it. The only `SHA_MISMATCH` red is an authored fixture. A real-defect red is cheap: add a label-check-style claim with token `7a98720e`, the sentence at line 76 and the revision it describes (tip `0ab1ccc`). It must fail.
5. **The re-cut half stays unverifiable.** The round-17 sentence claims "identical counts". The receipts carry `files[].sha256` and `counts`. Only a comparison of old and new receipts can verify or falsify the claim: equal `files[].sha256`, equal `counts`/`findings`, and a tool sha that differs (7a98720e → 962919ce). `receipt-check.py` checks only the header.
6. **Identity risk.** If the re-cut overwrites `round-17/evidence/tripwire-r1*.txt`, every round-17 sentence bound to those bytes at `f71ccbe` loses its referent. Criterion 4 (append-only) and the round-15 note ("Never stamp a later full-gate measured commit onto a pre-commit mutation run") require new files under `round-18/evidence/`. The old receipts must stay labelled "measured at f71ccbe, tool 7a98720e (derived from git, not recorded)".
7. **The population is author-chosen.** The check sees only receipts listed in `receipt-claims.json`. To avoid premature saturation, derive the population from every evidence path cited in the round-18 lesson, report and SCORECARD. That is criterion 14: expected set vs observed set.

**Option (C3-adjacent, harm-watched):** have `--scan` emit `"tool_sha256"` in its own JSON, as the frozen-verdict schema already does. A receipt then cannot be hand-stamped. The risk: the four selftest suites must stay all-pass if any of them compare whole JSON.

### Criterion 25 (R17-V5 — committed mutant receipt for instrument tightenings)

**Restated part:** "seat-attested or `/tmp` lab runs are not credit" is criterion 13 verbatim ("`/tmp` records provenance only"). Round 17 already self-disclosed the breach (`lessons/round-17.md:156-158`). R17-V5 is an enforcement failure of 13, not a gap in the bar.

**New part (only if the check enforces it):** "bites" is counterfactual. The pre-tightening instrument must **credit** the mutant, and the tightened one must **reject** it. The measure.py history is `f52f43f` (bind) → `ab0bc9b` (tighten: exact surface line, pinned legacy…) → `f71ccbe` (wave-2: `## Registry`-only parse, duplicate-id fail).

**Counterexamples**

1. **The draft check is shape-only.** `mutant-check.py` (QualityDraft:7) accepts any JSON with six keys, two 64-hex shas, a 40-hex commit and `loose_output != tight_output`. An invented receipt passes. This is R17-V3's "fetched vs invented" problem in another form.
2. **Only the tight side is run.** LessonDraft M2 runs only the tightened instrument ("Green: every mutant is MISMATCH under the tightened instrument"). Take a mutant SOURCES row lacking `surface:` entirely: both `ab0bc9b` and `d9a5a18` reject it, so it counts green while proving no tightening.
3. **The mutant run cannot be reproduced from lane bytes as planned.** `measure.py` reads every input through `git show REV:path` (`measure.py:57-60`), so a mutant must be a commit. Lane git writes are forbidden, so mutants live in a `/tmp` clone. Unless the check rebuilds that clone deterministically from committed inputs (base rev + mutant file bytes/patch) and re-runs both instruments, the round-18 receipt repeats R17-V5 exactly: it bites only in a `/tmp` lab.
4. **Self-application.** If 25 governs "instrument tightening", then 24's and 26's own "shown able to fail" claims are the same kind of claim. Their red runs need committed receipts carrying both the checker sha and `measured_commit`. As drafted they exist only as prose.

**Smallest correction:** the check itself re-executes `git show <loose_rev>:…/measure.py` and `<tight_rev>`. It runs each on each committed mutant in a scripted, reproducible `/tmp` clone. It requires loose = credit, tight = reject, and compares the result with the recorded receipt. If it cannot do that, drop 25 and record R17-V5 as a criterion 13 application, following the round 14/15 precedent.

### Criterion 26 (JjAuditMado F10 — producer status on piped digests)

**Restated part:** a FAIL "local edit" verdict built on an unread blob merges *unknown* into *observation*. That is criterion 3. Criterion 7 says hash from `git show` but is silent on rc. `QUALITY.md:24` says the bar "governs claim admission only", while 26 as drafted is a coding rule. Phrase it as an admission rule: "a digest/count verdict is admitted only with the producer's observed status; `e3b0c442…` without a recorded legitimately-empty source is UNKNOWN".

**Grounding is latent.** `git grep e3b0c44298fc d9a5a18` finds only two seat reports:

- `round-17/w1/reports/SrcTerminalAlternates.md:38` — a 404 fetch honestly labelled `404 | 0 | e3b0…`. This is a natural **green control**.
- `round-17/w2/reports/MisrootSweep.md:58` — a fleet `.ufo/state/*report-baseline` whose content is `17 e3b0…`. [INFERENCE] This may be a real-world empty-read baseline. It is outside lane authority and is only an indicator.

No lane receipt ever admitted a false `vs_head` FAIL, and JjTrialMado has no F10 hit. Label the provenance the way `QUALITY.md:26-30` did for 15-16: a latent instrument defect from an outside audit, not an admitted false claim.

**Strongest counterexample: the recommended fix is broken, and the planned lint passes it.** `/tmp` repro:

```
old idiom:  blob=e3b0c442…b855  [ -z "$blob" ] guard = unreachable            (F10 confirmed)
audit fix:  out=$(git -C /nonexistent show HEAD:x | sha256sum | cut …); grc=${PIPESTATUS[0]}
            → grc=0 while git rc=128   (PIPESTATUS after $(…) is the assignment's, not git's)
working:    $(… | sha256sum | cut …; exit "${PIPESTATUS[0]}")  → $?=128
```

- JjAuditMado `:350` recommends the broken form, and LessonDraft M3 repeats "or use `${PIPESTATUS[0]}`".
- QualityDraft's `pipe-rc-lint.py` passes any line with "`PIPESTATUS` in the next two lines", so it goes green on exactly this broken fix. That is a hidden regression certified by the criterion's own check.
- I sent this to MadoR18 for GateRcFix.

**Over-reach and saturation**

- QualityDraft says the lint reports `PIPE_RC_FLAGS: 9` and passes only at 0. Sites 244, 942, 944, 1377 and 1383 are `find|sort|xargs sha256sum|sha256sum` fixture/boundary hashes, guarded by `[ -d ]` preconditions (e.g. `boundary_hash` `:238`). Sites 1133, 2788 and 3474 are `find … | wc -l` counts. Some may be real siblings: a missing `$H` yields `nbak=0`.
- Gating 26 on 0 flags forces either nine edits to the harm-watched gate, plus a PIN_MADO re-cut and hermetic re-cut, or a criterion that is red at close.
- LessonDraft M3 says the red lists only `:3406`, while QualityDraft says 9. The drafts disagree.

**What a non-author needs**

- The gate's own OM scenario. Extend the selftest git stub with a per-verb rc (F14: the current stub ignores its arguments and exits 0) so that `show` exits 128 with no output, and assert `omarchy.skill.vs_head UNKNOWN`. It must be red on `d9a5a18`'s gate (row FAIL `…!= HEAD blob e3b0c44298fc…`) and green after the fix.
- The census exits 0 when every flagged site carries a disposition (fixed / precondition-guarded at line N / open debt), not when flags = 0.

## 3. Smallest safe correction (for L1)

1. **For each of 24-26, add a "Differential" sentence** that names the existing criterion (3/6/9/13/23) and the one real `d9a5a18` artifact the old checks accept and the new check rejects:
   - 24: `tripwire-r13.txt` (23 passes, 24 fails);
   - 25: a duplicate-id SOURCES mutant (credited by `ab0bc9b`, rejected by `d9a5a18`);
   - 26: the `:3406` stub-rc scenario (gate FAIL, should be UNKNOWN).

   Commit each red/green as a receipt carrying the checker sha and `measured_commit`.
2. **24:** cite and supersede `QUALITY.md:57-61,65-70` explicitly. Drop the R17-V2 sentence into a criterion 6 application, and add a real-sentence red claim for `.ufo/reports/round-17/mado.md:76` instead. Add `label-check-final.txt` as a green control. Fix the join receipt's producer. Write re-cuts to new files under `round-18/evidence/`, with an old-vs-new `files[].sha256`/`counts` equality check. Derive the claim population from cited paths.
3. **25:** run both loose and tight instruments in a scripted, reproducible clone. Otherwise fold it into 13 with no new criterion.
4. **26:** use admission wording, a behavioural stub scenario, and a disposition-complete census. Reject `grc=${PIPESTATUS[0]}`-after-`$(…)` fixes. Label it a latent outside-audit defect.
5. **Report both counters.** If any criterion is folded, C1 lands below 18/26. That outcome is honest; meeting the target with a restatement is not.

## Impacted axes

- **Calibration:** the claim's validity. Inflation risk on every criterion.
- **Operability:** the F10 fix regression; the gate rewrite if the lint gates on 0.
- **Provenance:** join-receipt identity; round-17 receipt overwrite.
- **Discernment:** the non-author differential.

Each item in §3 is a fixable defect, not a tradeoff the judge must reject. The exception is shipping 25 as shape-only: the judge should reject that as restatement.
