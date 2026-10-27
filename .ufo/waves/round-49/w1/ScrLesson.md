# ScrLesson — round 49 / w1 (BUILD): lesson skeleton

Status: complete. Deliverable is the lesson skeleton; no product code, counter, gate, fetch or commit was made.

Artifact: `.ufo/waves/round-49/w1/ScrLesson/round-49.md`
sha256 `506359db7e02fb0def0faf278e6803293fd7a271b0f20b1c5118215e46aa369f`, 366 lines, 16 headings,
49 `TODO-L1` markers. Scratch `/fast/scratch/hyaku/mado-r49/ScrLesson` created and removed; no tool installed.

## 1. What the skeleton holds

Section inventory, in file order (round-48 shape, `corpus/lessons/round-48.md`):

`## Gate` (C1 plane = the pinned how-to-type judge + the keysyms header question; C2 plane = Hyprland `efb50993` key-field
match + the wiki at a pinned commit; held rows named as cite-not-reclaim: `S318`/`S319`, `S326`/`S327`, `S340`-`S351`),
`### Rejected after opening` (three rejection classes the round must state: host binary as its own row, unpinned wiki,
`IKeyboard.cpp` duplicating `S319`), `### Census before → after`, `### Registry changes`, `### Renumber map`,
`### Id guard and quarantine`, `### considerthese`, `### The contract delta line (round-48 D1 paid forward)`,
`### Applications of existing criteria`, `### Conflicts recorded for the judge`, `## Search log`, `## Mistakes`
(+ `### w2 routing`, criterion 52), `## Round-48 closure items` (N1-N5, M48-8, M48-10, M48-13, SentScratch F1-F7,
registration-v2 residuals, the 47 sidecars), `## Spot-check (pending non-author)`, `## Frontier`.

Every pending value is `TODO-L1`; the row-admit block, the reject block, w2 routing rows, the mistake lines and the
considerthese landing are shapes the L1 fills, not drafted findings.

## 2. Measured inputs (command → output, run 2026-10-27)

| fact | command | output |
|---|---|---|
| base revision | `git log --oneline -1 03e4ae76`; `git merge-base --is-ancestor 03e4ae76 HEAD` | `round-48 verifier spot-check (integrator, hyaku)`; ancestor yes |
| lane HEAD | `git rev-parse HEAD` | `5f37c1b8…` (the round-49 L1 prep commit: claims, w1 spec + dispatch, census-before, operator-state-before) |
| `tools/` | `git ls-tree --name-only 03e4ae76 tools/ \| wc -l` | `15` |
| `corpus/knowledge/` | `git ls-tree --name-only 03e4ae76 corpus/knowledge/ \| wc -l` | `65` |
| `corpus/lessons/` | `git ls-tree --name-only 03e4ae76 corpus/lessons/ \| wc -l` | `72` |
| registry rows / top | `git show 03e4ae76:corpus/SOURCES.md \| grep -cE '^\| *S[0-9]{3,} *\|'`; same with `grep -oE … \| tail -1` | `288` / `| S351` |
| QUALITY criteria | `git show 03e4ae76:corpus/QUALITY.md \| grep -cE '^[0-9]+\. '` | `99` |
| README Frontier bullets | `git show 03e4ae76:corpus/README.md \| grep -cE '^- Round [0-9]+ moves'` | `13` |
| w1 seats | `python3 -I -c "import json;print(len(json.load(open('.ufo/waves/round-49/w1-spec.json'))['items']))"` | `45` |
| census before | `.ufo/waves/round-49/receipts/census-before.txt` | 19 lines: 17 `W04` + 1 `W01` + `mado ok`, `exit=0` |
| staged band / collisions | set intersection of registry ids at `03e4ae76` against `.ufo/waves/round-48/assimilation/staged-ids` (that slice and round-47's are both 147 lines; the tree holds 19 `staged-ids` paths, `find .ufo -name staged-ids \| wc -l`) | staged 147 ids (`S203`-`S349`); collisions `94` (round 48 reported 84 on 276 ids; delta = `S340`-`S349`) |
| untracked sidecars | `git status --porcelain -uall \| grep -c 'synthetic'` | `47`, all `*.synthetic`, 45 under `.ufo/waves/round-45/`, 2 under `.ufo/waves/round-46/` (matches N1's corrected count) |
| round-49 assimilation | `find .ufo/waves/round-49/assimilation -type f \| wc -l` | `0` |
| latest considerthese | `ls considerthese/ \| tail -1` | `2026-10-26.md` (no `2026-10-27` file) |
| axis at round-48 tip | `.ufo/waves/round-48/receipts/axis-tip-final.txt` | `MADO_AXIS: checked=3 mismatched=0 rev=627914f6…` |
| round-48 Gate decisions | pipeline from §3 below, on `corpus/lessons/round-48.md` | `T=15`, `A=12`, `R=3` |

The census block pasted into the lesson was byte-compared against the committed receipt by a small `python3 -I` script:
`block == receipt` → `True` (20 lines each).

## 3. N3 handled as a computed count

`corpus/lessons/round-48.md:425` typed a decision count in words that did not match its own `## Gate`. The round-49 shape
line therefore carries no typed number — it names the pipeline the closure must run:

```
T=$(sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-49.md | grep -cE '^- \*\*(S[0-9]+ admit|REJECT)')
A=$(sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-49.md | grep -cE '^- \*\*S[0-9]+ admit')
R=$(sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-49.md | grep -cE '^- \*\*REJECT')
```

with `T = A + R`, sample size `max(min(T, 6), 3)`, and at least one reject when `R > 0`.

Pipeline exercised twice: on `corpus/lessons/round-48.md` it reproduces `15`/`12`/`3` (the correction's numbers), and on the
skeleton it reads `0`/`0`/`0` — the admit and reject lines are the L1's to paste, so the template cannot satisfy the count.

## 4. Self-checks actually run on the draft

| check | how | result |
|---|---|---|
| census block fidelity | `python3 -I` extract of the fenced block vs `receipts/census-before.txt` | equal, 20 lines each |
| N3 pipeline | run the three `sed`/`grep` commands on `round-48.md` (control) and on the draft | `15`/`12`/`3` and `0`/`0`/`0` |
| seat names | every `w1/<Name>` and bare seat token cross-checked against `w1-spec.json`'s 45 `name` values | only historical round-47/48 seat names and the `RevengerOmarchy` path resolve outside the spec, each flagged in the text (notably: no `ExecIdGuard` seat this round, so the guard section names round 48's as the precedent and leaves assignment to the L1) |
| base counts | each `13`/`15`/`65`/`72`/`99`/`288`/`S351` re-derived at `03e4ae76` with `git ls-tree`/`git show` | as tabulated in §2 |
| held-row ids | `S030`/`S045` confirmed as the two `wiki.hypr.land` Window-Rules rows (`grep` of `corpus/SOURCES.md`), `S303`/`S317` as the **legacy** `ConfigManager.cpp`, `S351` as `src/keymap.c` | corrected one wrong id (`S042` was the Wayland extras page) before landing the draft |
| cited paths | `ExecSessionMarker/SHA256SUMS`, `w2/SentScratch.md`, `registration-v2.md:103-110`, `receipts/axis-tip-final.txt`, both round-49 receipts | all exist; the registration residual text at `:103-110` names the receipt-generator path and the uncited meson pin as summarised |
| digest | `sha256sum` of the draft after the last edit | `506359db…a369f`, the value quoted at the top |

## 5. Limits and what this seat did not do

- The candidate row set named in `## Gate` is drawn from the files the w1 fetch sets held at draft time (`ls` of
  `.ufo/waves/round-49/w1/{ExecHyprSrc/fetch,ExecXkbSrc,ExecKeysymNames,ExecKeymapParse}`), not from seat findings: those
  seat reports were still stubs when read, so no finding, quote, sha256 or count from a peer seat is asserted here.
- No `xkbcli`, `hyprctl`, counter, gate or network call was made by this seat; every host behaviour in the skeleton is either
  a pin declared in `claims.md` or a `TODO-L1`.
- Unverified by design: the freeze hash, the row ids and count, the admit/reject sets, the census-after block, the
  considerthese landing, the w1 defect lines, the w2 routing table, the round total, and every `TODO-L1` in the report table
  of `## Round-48 closure items` (each has its seat and its acceptance written).
- Out of scope by instruction: no edit to any tracked file, no commit/push, no judge invocation, no sibling-lane or
  fleet-root write. Only `.ufo/waves/round-49/w1/ScrLesson/round-49.md` and this report were written.
