# MutC1V2 — mutation-test PRED-C1-r44-v2's new gates (round 44, w2)

**Verdict: 25 mutants, 548 detector runs — 1 survivor (M01 admits the X2 control), 13 gate-broken, 10 killed, 1 equivalent. The landed data is not invalidated: the survivor is a counter-robustness hole (key drift inside the b5 hook), reachable only by editing the counter itself, not by any tool-side cheat. The landed tool scores TARGET_MET under 24 of 25 mutants and under all 20 controls for every mutant that keeps the reference passing.**

## 1. Protocol

- Target: a COPY of `quality/counters/c1-r44-geometry-states-v2.py` (sha256 `0d872405bb41dd88a9265bb46bfd39c7a92d7738d01f9d91927c9a49a0e9977b`) in scratch; lane bytes never edited. 25 mutants, one behavior-bearing single edit each; every replacement asserted to match exactly once at build time (25 pairs, 0 non-unique; one build fix: M03's `\n` is literal — it sits inside a string literal, counter:356-362).
- Detector (identical for pristine, every mutant, restored rerun): `python3 -I <counter> --repo LANE --rev <rev> --nonce mutc1w2a --work <scratch/work>` + subject args, cwd = lane root. Subjects per counter: **LANDED** `--tool tools/mado-geometry.py` (must stay TARGET_MET), **BASE-tool** at `e2289516a9a857f55cda7be635933e89b931c3da` (no `--tool`), **ABSENT** at `62dd798bb08401a8697383552edcc36f109344fa`, and the 18 VARIANTS regenerated in scratch from the FROZEN `.ufo/waves/round-44/ctl/run-c1-controls-v2.py` (sha256 `07d300745dc06c012c481dc58fd29052121a89cdb9fa29d488c7a609bf319391`; imported for `VARIANTS`/`PAD_LINES`/`CUT_*`, its scoring loop never run). All 20 controls must stay TARGET_MISSED. The REF subject is not run separately: `c1/ctl-ref-tool-v2.py.txt` is byte-identical to the landed tool (sha256 `1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4`, cmp(1) equal), so the LANDED run is the REF run.
- Anchor: the pristine counter also ran the registered counting command at the data commit (`--rev e46789213830597348fe96a351ae004d10587385`, no `--tool`).
- Baseline (pristine, nonce `mutc1w2a`): LANDED@data `rc=0 fixtures=26/26 TARGET_MET`, clauses `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` — same pattern as frozen `receipts/c1-after-data.txt`; LANDED@e2289516 `rc=0 fixtures=26/26 TARGET_MET`; all 20 controls `rc=1 TARGET_MISSED` with the frozen receipt's clause pattern (e.g. X1 `e:0`, X2 `b5:0`, K13 `b:0 b4:0 b5:0`). Fixture shares differ from the frozen receipts only through the nonce, verdicts identical — corroborating registration-v2's "the lattice share varies with the nonce, the verdict does not".
- Run count: 22 pristine + 25 x 21 + 1 restored rerun = 548 counter runs, 14-way parallel (w1 MutC1CounterGates house method), 456.7 s wall for the mutant phase. Fixed nonce `mutc1w2a` so every body is judged on the same sgen lattice.
- Survivor: a mutant whose counter run **admits a bad control** (control TARGET_MET) or **rejects the landed tool** (TARGET_MET -> TARGET_MISSED, or crash).

## 2. Results (observed; pre-registered predictions kept, deltas marked)

| id | target | edit (old -> new, abridged) | LANDED | controls admitted | verdict |
|---|---|---|---|---|---|
| M01-b5-rename-wrong-key | b5 hook key | hook renames `floating` instead of `fullscreen` | 26/26 MET | **X2-padded-selftest** | **SURVIVOR** (predicted KILLED — wrong, see §3) |
| M02-b5-key-never-matches | b5 rename key | `k == 'fullscreen'` -> `k == 'Fullscreen'` | 26/26 missed, b5:0 | none | GATE-BROKEN |
| M03-b5-hook-dropped | b5 prefix | `k['object_hook'] = _b5_hook` -> `pass` | 26/26 missed, b5:0 | none | GATE-BROKEN |
| M04-b5-prefix-before-shebang | b5 placement | shebang offset `k = 1 if ...` -> `k = 0` | 26/26 MET | none | KILLED (predicted KILLED) |
| M05-b5-dead-test-weakened | b5 failure test | `dead = rc != 0 or not has or k_ != n` -> `dead = rc != 0` | 26/26 MET | none | KILLED (predicted KILLED) |
| M06-b5-dead-always-false | b5 failure test | `dead = ...` -> `dead = False` | 26/26 missed, b5:0 | none | GATE-BROKEN |
| M07-b5-unchanged-copy | b5 binding | hooked `text` -> unhooked `src` (counter:368) | 26/26 missed, b5:0 | none | GATE-BROKEN |
| M08-b4-kill-gt-0 | b4 failure test | `return killed >= need` -> `return killed > 0` (counter:331) | 26/26 MET | none | KILLED (predicted KILLED) |
| M09-inv-drop-fsclient0 | INVARIANCE set | drop `fsclient0` (counter:374) | 26/26 MET | none | KILLED (predicted KILLED) |
| M10-inv-only-fs0 | INVARIANCE set | set -> `("fs0",)` | 26/26 MET | none | KILLED (predicted KILLED) |
| M11-e-drop-stdout-eq | clause e compare | drop `out1 == out2` | 26/26 MET | none | KILLED (predicted KILLED) |
| M12-e-env-inherited | clause e env | GIT_-strip dict -> `env = None` | 26/26 MET | none | EQUIVALENT (predicted EQUIVALENT) |
| M13-e-timeout-cliff | clause e timeout | `timeout=30` -> `timeout=0.001` (counter:392) | 26/26 missed, e:0 | none | GATE-BROKEN (predicted GATE-BROKEN) |
| M14-r-timeout-unguarded | clause r timeout | `timeout=1800` -> `timeout=None` (counter:341) | 26/26 MET | none | KILLED/EQUIVALENT here (predicted same; w1/RevC1Counter LOW-3 residual stands) |
| M15-judge-inverted-stderr | judge_v2 | `... and err:` -> `... and not err:` (counter:182) | 19/26 missed | none | GATE-BROKEN (predicted GATE-BROKEN) |
| M16-judge-stderr-disabled | judge_v2 | gate -> `if False and ...` | 26/26 MET | none | KILLED (predicted KILLED) |
| M17-model-nc-drop-agree | NOT_COMPARED | drop `t["AGREE"] == 0` (counter:160) | 24/26 missed | none | GATE-BROKEN (predicted GATE-BROKEN) |
| M18-model-differ-suppressed | NOT_COMPARED order | DIFFER branch guarded by not-NC (counter:156) | 24/26 missed | none | GATE-BROKEN (predicted GATE-BROKEN) |
| M19-model-nc-exit6 | NOT_COMPARED exit | `, 5` -> `, 6` (counter:161) | 19/26 missed | none | GATE-BROKEN (predicted GATE-BROKEN) |
| M20-model-states-always | summary gate | `if max+fs > 0:` -> `if True:` (counter:165) | 13/26 missed | none | KILLED (predicted ADMITS-K02 — wrong, see §4) |
| M21-judge-patch-removed | judge_v2 install | `old.judge = judge_v2` -> comment (counter:187) | 26/26 MET | none | KILLED (predicted KILLED) |
| M22-model-bool-is-mode | fsmode model guard | `type(f) is int` -> `isinstance(f, int)` | 24/26 missed | none | KILLED (predicted ADMITS-K03 — wrong, see §4) |
| M23-min-state-sites-60 | b4 floor | `MIN_STATE_SITES = 6` -> `60` (counter:77) | 26/26 missed, b4:0 | none | GATE-BROKEN |
| M24-r-verdict-check-weak | clause r check | `" verdict=TARGET_MET "` -> `" verdict="` (counter:347) | 26/26 MET | none | KILLED (predicted KILLED) |
| M25-e-loop-no-skip | INVARIANCE loop | skip-guard -> `if False:` (counter:381) | crash rc=1, `KeyError: 'maxfloat0'` | none | GATE-BROKEN (predicted GATE-BROKEN) |

Evidence: `evidence/results.tsv` (548 rows: mutant, subject, rc, secs, rev, clauses, fixtures, verdict), `evidence/matrix.json`, `evidence/b5-probe.txt`, `evidence/locators.txt` (grep -n computed).

## 3. Finding 1 (the survivor) — OPEN predicate-adjacent defect: b5's X2-tooth hangs on one string literal

**Mutant M01** (counter:356): the b5 hook renames `floating` instead of `fullscreen`. **Outcome: the landed tool still passes (26/26 MET) but control X2-padded-selftest reaches TARGET_MET** (rc=0, clauses `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1`, fixtures 26/26 — `evidence/results.tsv` row `M01-b5-rename-wrong-key X2-padded-selftest`).

Mechanism (measured, `evidence/b5-probe.txt`):

| hooked copy | selftest | consequence |
|---|---|---|
| REF + pristine hook | rc=1, 86/94 | b5 holds for the reference (correct) |
| REF + M01 hook | rc=1, 79/94 | b5 still holds for the reference |
| X2 + pristine hook | rc=0, **103/103 passes** | b5 fails -> X2 missed (caught) |
| X2 + M01 hook | rc=1, 98/103 | b5 holds -> **X2 admitted** |

X2 is not "reference + extra checks": the frozen runner's PAD construction replaces the selftest's whole state-assertion block — `def fs(...)` through `chk("fsmode-absent", ...)` at ref:438-472, 21 state chks — with 30 trivially-passing pad checks (`text[:i] + PAD_LINES + text[j:]`, run-c1-controls-v2.py:60, name at :34). So X2's selftest asserts **no state verdict through the JSON path** (103/103 under the pristine hook), which is precisely what clause b5 must catch; its fixtures are 26/26 and clause r passes, so b5 is its only net. Under M01's mis-aimed hook, X2's *remaining* floating-dependent assertions (round-43 behavior through the JSON path) fail 98/103, so b5 holds and nothing holds X2 back.

**Why it matters.** The b5 gate's protection of X2 rests entirely on the literal `'fullscreen'` in `B5_PREFIX` (counter:356). A one-word counter-side drift (wrong key, dropped hook, case change) either breaks the reference outright (M02, M03 — caught at scoring time) or — the M01 class — keeps the reference passing while silently admitting X2. No registered control or clause detects that drift class. Severity: LOW-MEDIUM — it requires mutating the counter, not the tool, so it cannot inflate the landed C1 claim; but the control corpus has no second net under X2.

**Candidate guard (for the L1 to decide; not landed by me — no re-registration after data).** A hook-liveness unit assertion inside `state_blind`: run `B5_PREFIX` plus `assert list(json.loads('{"fullscreen": 2}')) == ['_b5_fullscreen']` in a throwaway interpreter before scoring the tool; it kills the M01/M02/M03 drift classes without touching the contract. A cheaper partial: also assert the hook renames *nothing else* (e.g. `{"floating": true}` keeps its key), which kills M01 specifically.

## 4. Finding 2 — structural: the control corpus's admission surface is {X1 -> e, X2 -> b5, K13 -> b/b4/b5}

K01-K16 all fail clause r (the unmutated round-42 regress, counter:341-347), so **v2-model mutations cannot admit them**: I ported three control defects into the oracle — M20 (K02's always-printed state fields), M22 (K03's bool-as-mode), M17/M18/M19 (NOT_COMPARED drifts) — and every one still missed all 20 controls (K02 stays missed via r:0, K03 via r:0). Consequence: the v2 model's NOT_COMPARED/summary/fsmode semantics are pinned against the landed tool by the 26 fixtures, but the *control corpus* cannot detect model drift in a counter that keeps the landed tool passing. The only controls a counter mutation can admit are the three r-clean ones: X1 (held only by clause e), X2 (held only by clause b5), K13 (held by b/b4/b5). Severity: LOW — the landed-tool run is the real net for model drift, and bad-tool rejection is double-covered by r; but control-set coverage claims should be read through this lens.

## 5. Killed mutants that are coverage notes (unexercised counter assertions)

No control or fixture exercises these, so their drift is invisible to the corpus (each verified by the mutant run: landed MET, 0 admitted):
- **M08** — b4's 75% margin (`killed >= need`, counter:331) is not load-bearing; `killed > 0` passes everything. Matches w1's v1 finding (K14/K15 KILL_FRACTION not load-bearing).
- **M09/M10** — clause e's five-fixture set is not minimally load-bearing: `("fs0",)` alone still catches X1 (fs0 flips rc 5 -> 1 outside the sandbox).
- **M11** — the `out1 == out2` term of clause e is unexercised (X1 flips rc as well as stdout).
- **M16/M21** — judge_v2's rc5-stderr assertion (counter:182) is unexercised: the r42 judge checks stderr only for want_rc in (0, 1, 3, 4) (c1-r42-geometry.py:449-459), and no fixture/control produces stderr on rc 5.
- **M24** — the r verdict-word check (`" verdict=TARGET_MET "`, counter:347) is unexercised: no control passes r42 with a wrong verdict word.
- **M05** — b5's `not has or k_ != n` terms (counter:369) are unexercised: no corpus body exits 0 with a broken summary line.
- **M04** — the shebang-offset branch (counter:366) is dead code for the teeth: copies run via `python3 -I <tool>` (c1-r42-geometry.py:200-210), so placement before or after `#!` is equivalent.
- **M12** — the GIT_-strip env dict (counter:389-390) is equivalent to `env = None` on this corpus.
- **M14** — `timeout=None` on the regress subprocess (counter:341): no hang on this corpus; the unguarded-hang residual (w1/RevC1Counter LOW-3) remains open and unobservable in bounded runs.

## 6. Gate-broken mutants (fragility cliffs, not holes)

These reject the landed tool — a counter regression class the landed scoring would catch immediately, listed for completeness: M02, M03, M06, M07 (b5 inert -> b5:0); M13 (clause e breaks for any timeout below tool startup — the 30 s value is load-bearing); M15 (19/26), M17/M18/M22 (24/26), M19 (19/26), M20 (13/26) (model/fixture mismatches); M23 (b4 floor 60 > 16 sites -> b4:0); **M25 — robustness defect: the clause-e loop crashes with `KeyError: 'maxfloat0'` (counter:381-383) instead of failing a clause or printing a clean SETUP line, rc=1 with no final line** — an unexpected fixture name in FIXED turns the counter into a crash rather than a diagnosis.

## 7. Restoration and hygiene

- Lane bytes never touched; before/after sha256 identical: `c1-r44-geometry-states-v2.py` `0d872405bb41dd88a9265bb46bfd39c7a92d7738d01f9d91927c9a49a0e9977b`, `c1-r42-geometry.py` `ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99`, `tools/mado-geometry.py` `1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4`, `run-c1-controls-v2.py` `07d300745dc06c012c481dc58fd29052121a89cdb9fa29d488c7a609bf319391`.
- Restored-bytes detector run after the matrix: LANDED@data rc=0, `fixtures=26/26 … verdict=TARGET_MET` (mutdrive `final`).
- Scratch `/fast/scratch/hyaku/mado-r44/MutC1V2` deleted at seat close (evidence copied to `evidence/` first); no result cited from scratch. No pacman transactions, no tools installed (system python 3.14, bwrap present), no host-service or compositor mutation, no subagents, no mutating git/jj anywhere.
- Prediction honesty: 22/25 pre-registered predictions correct; M01 (predicted KILLED, observed ADMITS-X2), M20/M22 (predicted ADMITS, observed KILLED via clause r — Finding 2).

## 8. Reproduction

    S=/fast/scratch/hyaku/mado-r44/MutC1V2   # scratch (deleted; rebuild per driver)
    python3 $S/mutdrive.py verify && python3 $S/mutdrive.py subjects && python3 $S/mutdrive.py mutants
    python3 $S/mutdrive.py baseline && python3 $S/mutdrive.py mutrun && python3 $S/mutdrive.py final
    python3 $S/summarize2.py

Driver and summarizer lived only in scratch; the mutant table above is reproducible from `evidence/results.tsv` (one row per run) plus the frozen lane files.
