author: hyaku closure (non-author integrator, @m_zfl)

# mado round 87 — verifier spot-check (non-author)

Round report `.ufo/reports/round-87/mado.md`; lane repo `mado-shokunin`; round base
`e4875ba5619053cc3f91bb2f4d819e189df4088c`; content commit `7563452f9b35af0141c49dc4cc7f791968ca0c90`;
measured/counter revision `00c967214e338d8f0ebb02b78f98fd61a542a515`; round tip (closed)
`f4dfd0a9bd54d5bad518e58297c9b222f6be9b62`. I did not author this round; every command below was run by
me against committed bytes on this host, 2026-11-05. Driver digest (closure prompt; verified against
`.ufo/watchdog.log`): `2026-11-05T05:40:47-03:00 launch mado round=87 pgid=2512075 driver=hyaku-inline
attempt=1` / `2026-11-05T07:18:42-03:00 complete mado round=87; hyaku-inline attempt=1`.

## 1. Conformance (step 1)

| item | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-87/mado.md` (fleet repo) | `mado-shokunin <mado@shokunin.local> 21657a662560456c6edbcde3448f0dca22eb4600 round-87: mado report` | pass |
| `SHONEN` heading, one line per box | report `## SHONEN`; `cat SHONEN.md` | heading present; 4 `[~]` lines, one per canonical box, each with a resolvable pointer; `SHONEN.md` seed matches the canonical template, marks confined to box + one evidence line; no `[x]` | pass |
| cited lane commits exist, ancestors of the branch ref | `git cat-file -e` + `git merge-base --is-ancestor <h> master` over `e4875ba5`, `7563452f`, `00c96721`, `f4dfd0a` | all four exist and are ancestors of `master`; `master` = `f4dfd0a…`; commits authored `mado-shokunin <mado@shokunin.local>` | pass |
| no uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain` | `ahead=0 behind=0 tracked=0 untracked=0 head=detached`; status empty | pass |
| prompt carries the template contract | `diff templates/round-prompt.md .ufo/prompts/mado-round-87.md` | only placeholder substitutions (`{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}`) plus the §6 hyaku addendum; §1 mission/axes, §2b frontier, §3 L2 ≥8 batched, §4 report path/sections incl. `SHONEN` + hash citation, §5 commit-then-push, push scope, L0 channel — all verbatim | pass |
| dispatch evidence | `.ufo/watchdog.log` | launch line 2783, complete line 2802, text matches the digest above | pass |

**Conformance defects:** none status-changing. Notes: the frozen declaration's C2 command omitted the
`--expect-figures-sha256` pin (erratum 6, disclosed and fixed before scoring); the C1 case file was
rewritten once during the wave, voiding early-seat findings (erratum 4, disclosed; final bytes scored and
sha-pinned).

## 2. Per-claim re-check

Both claims rest on this round's own counters (`quality/counters/c1-r87-mako-criteria.py`,
`quality/counters/c2-r87-control-fidelity.py`); neither is a registered standing gate in `SKILL.md`
§Gate registry, so I re-ran both as plain measurements (read-only, `--scratch-root` under `/tmp`).
The lane's standing gates (`mado-selftest`, file plane, `quality/check-index.py`,
`quality/check-tool-ledger.py`) I evidence-verified from the committed receipts only — not executed
(§Gate standard, Closure consequence).

**C1 — re-measured.**
`python3 -I quality/counters/c1-r87-mako-criteria.py --repo . --rev 00c967214e338d8f0ebb02b78f98fd61a542a515
--cases .ufo/waves/round-87/controls/mako-cases-r87.json --scratch-root /tmp/mado-closure-r87/c1a`
→ `MADO_MAKO_CRITERIA: TARGET_MISSED rev=00c96721… cases=22 correct=22 mutants=10 killed=5
naive_correct=7 globals_include_correct=8 score=10.0000`, rc 1; survivors M03, M05, M06, M08, M10 —
byte-identical to the report and `receipts/c1-measured-r87.txt`. Case-file sha256 re-hashed:
`0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3` matches. Base re-run at `e4875ba5`:
`SETUP_ERROR … path 'tools/mado-mako.py' … not in 'e4875ba5…'`, rc 2 — matches `receipts/c1-base-r87.txt`.
Verdict: **TARGET_MISSED re-derived** (honest stop; predicate needs all ten mutants killed).

**C2 — re-measured.**
`python3 -I quality/counters/c2-r87-control-fidelity.py --repo . --rev 00c967214e338d8f0ebb02b78f98fd61a542a515
--figures .ufo/waves/round-87/controls/r86-figures-r87.json --expect-figures-sha256 f206a75907e385fc957aef07c8e1e2037b1328d5d1bcbfbd03c7201bc0b46ea6
--scratch-root /tmp/mado-closure-r87/c2a`
→ `MADO_FIGURES: TARGET_MET … n=2 reproduced=1 reconciled=2 score=10.0000`, rc 0; F1 `0/1 → 1/1`
reconciled by the appended correction block (`corpus/knowledge/refusal-records-clause-observations-r86.md:162`),
F2 reproduces — byte-identical to `receipts/c2-after-r87.txt`. Figure-file sha256 re-hashed: matches.
The before state (`receipts/c2-before-r87.txt`, fixture of the base correction blocks: 5.0000
TARGET_MISSED) is committed; the original r86 `0/1` sentence is left in place (append-only correction,
CORPUS.md corrections rule). Verdict: **TARGET_MET re-derived** (before 5.0 → after 10.0).

**Harm watch — evidence-verified from committed receipts, cross-checked where cheap.**
index `107/107 → 108/108` (`receipts/index-*.txt`), ledger `158 → 161, uncovered=0`
(`receipts/ledger-*.txt`), standing gate `MADO_SELFTEST: 460/460` start and measured
(`receipts/gate-selftest-*.txt`), file plane `CLEAN (29 pass, 4 notes)` (`receipts/fileplane-measured-r87.txt`),
census exit 0 with 427 → 428 rows and an identical 55×`W04` + 1×`W01` warning set before and after
(diffed `census-start` vs `census-end`; my own `scripts/sources-census.sh validate --root … mado` also
exits 0 now). `SCORECARD.md` diff `e4875ba5 → f4dfd0a`: appends only (r86 correction block, Round 87
section, named limits, routed-defects-fixed, lesson summary) — no axis score lowered, no retirement.

## 3. Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| coverage (C1) | **unchanged** | the capability move missed its frozen predicate (5/10 mutants killed vs all ten required); no capability row entered; the held 10 stands and nothing regressed — re-measured, honestly failed, not harmed |
| calibration (C2) | **improved** | before 5.0 → after 10.0 re-derived by me; the false r86 figure is superseded by an append-only measured correction that reproduces |

## 4. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-87.md` `## Gate` — one admit, two rejects, plus the new S493 row.
Source re-opened: `zcat /usr/share/man/man5/mako.5.gz` — container sha256 `17ffc88c…`, decompressed text
sha256 `f717848f…` both re-hashed and matching the pins; `pacman -Q mako` → `mako 1.11.0-1`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/mako-criteria-resolution-r87.md` (grammar, refusals, controls) | admit | manual lines 24, 47-48, 431-437, 443, 459, 469-470, 507, 620 — all re-read | **agree** | every sampled rule citation resolves to manual text that states exactly the rule (AND criteria 431-433, last-wins per option 435-437, app-name 443, urgency 459, mode gate 469-470, initial `default` mode 620, no spaces around `=` 507) |
| relative `include=` resolved from the including file | reject (not modelled) | manual lines 47-48 ("The path must be absolute / or otherwise start with `~/`") | **agree** | the manual states absolute-or-`~/` only; refusing relative includes is faithful, and the entry marks the resolver's refusal rather than guessing |
| `#` mid-line as a comment | reject | manual line 24 ("Empty lines and lines that begin with # are ignored.") | **agree** | whole-line `#` only is what the manual states; leaving mid-line `#` UNSTATED (not treated as a comment) is the honest reading |
| S493 row (mako 1.11.0 manual) | new registry row | re-hashed both digests; re-read line 47 | **agree** | quote "Includes a config at the specified path. The path must be absolute" (11 words ≤ 25) is verbatim at line 47 of the pinned text; tier A (installed docs of the running version) is the right scope; `used-by` paths exist; row conforms to contract v1 |

Also noted: the round accepted the attack seats' findings as errata (pin label, F2 wrap, "Not held"
withdrawal, `$HOME` fallback removal) instead of defending the draft — consistent with a calibrated gate.

## 5. Trend verdicts

- **expansion — improved.** One admitted knowledge entry on ground no held note resolved (mako
  effective settings), `source:` cites mined S493; census 427 → 428 rows verified by my own grep counts
  at base and tip; the entry's provenance trio and recheck are present. No capability credit (C1 missed) —
  expansion stands on the admitted entry, not the capability.
- **quality — improved.** The false r86 figure (`0/1`, entry line ~112) is superseded by an append-only,
  measured correction (`1/1`, block at `:162`) that my re-run reproduces; wave-found tool defects (D1–D3)
  fixed before scoring and disclosed as errata; no admitted entry failed a re-check; the entry/SCORECARD
  original sentences were not rewritten.
- **improved, and superseding the report's `unchanged`:** **discernment — improved.** The report recorded
  `unchanged` only because the non-author spot-check was pending at filing time. With this closure's
  spot-check agreeing with the gate on the sampled admit and both sampled rejects (and the new row
  verifying), LEARNING.md's `improved` observable — "the spot-check agrees with the gate on admits and
  rejects" — is met. Evidence: §4 above.

## 6. Routed defects (round 88)

1. **R1 (carried, C1).** Superseding frozen case set killing M03 (relative include accepted), M05
   (initial mode), M06 (defaults), M08 (missing input match), M10 (unterminated quote); the r87 frozen
   predicate is not rewritten.
2. **R2 (carried).** A symlinked `include=` escaping HOME is read; the manual states no containment rule —
   the entry/SKILL should name the containment stance explicitly (refuse, or read with the caller's
   declared trust boundary).
3. **R3 (carried).** Correction blocks are matched on figure id + literal value, not reasoning; the r86
   selftest pinning its own model (`c2-r86-clause-observations.py:736-737`) is outside the C2 predicate.
4. **R4.** Declaration hygiene: carry the sha pin in the declared command from the freeze, so no erratum
   is needed (r87 erratum 6); keep case files frozen before attack seats read them (r87 erratum 4).

**Operator note (promotion, step 6):** all four SHONEN boxes are `[~]` with pointers I found resolvable
(SKILL.md carries decision tables/error patterns/checklists and a gate registry; LOG.md logs end-to-end
rounds; the r87 knowledge entry + tool header are executable without oral context; PROVINCE refined and
file-plane CLEAN). Nothing bars a non-author promotion review; promotion is operator-owned — I wrote no
`[x]`.
