# RevLeadExitSemantics — DECISION: lead rows stay inside `findings` (exit 1, label `findings`); the verdict adds `observed_findings`/`lead_findings` integer counts. A separate `leads` list with exit 0 is inadmissible this round: it silently fails the pre-registered recall guard and makes precision regressions invisible to the pre-registered counter.

Reviewed at lane HEAD `e629f73` (tool `tools/mado-tripwire.py` sha256 `367be947…`, byte-identical working tree, `git status --porcelain -- tools/` empty). Pre-harm baseline `9c54c56` (tool `c1ae45a7…`) re-verified by `git show <rev>:tools/mado-tripwire.py | sha256sum`. Axes used to judge the two designs: **A1 recall-counter honesty** (unmodified registered instruments stay truthful), **A2 precision restorability** (the counter must distinguish "row removed" from "row demoted"), **A3 consumer compatibility** (every verdict consumer, enumerated, breaks or holds), **A4 marker honesty** (a lead must never read as clean). Findings ordered by severity.

## F1 (decisive, block-level): the only rule-B-detected incident line is necessarily a lead; a separate `leads` list forces tw-recall 5/6 and breaks the C1 admission guard

`tw-recall.py` (`.ufo/waves/round-19/tw-recall.py:74`) computes the numerator from `verdict.get("findings", [])` only — no `leads` key is read. The six frozen incident lines include `inputs/r13-root.jsonl:4`, detected at round 19 **only** by HelperFn rule B (closure, §C3: "Without B that last line is unrecognized, giving 5/6"). I read every eval cell of that file: lines 2, 3, 4 (verified by extracting all `toolCall eval` cells). Line 4 calls `run_record('packages', ['pacman','-Q','wayland-utils',…], 0)` — and `run_record` is **defined nowhere in the file** (no `def` in any cell). Under the round-20 target semantics (E1: lead = literal argv to an unbound bare name) that row is necessarily `evidence: "lead"`. Therefore:

- **Design A (leads in findings):** the row stays a findings row; `tw-recall.py` run unchanged prints detected=6 → guard "tw-recall.py 6/6 unchanged" holds.
- **Design B (separate `leads` list, exit 0):** the row leaves `findings`; the unchanged instrument reads 5/6 → C1 **fails its own pre-registered admission guard**.
- Amending `tw-recall.py` to also count a `leads` list is not an escape: it changes a registered instrument after its round-19 result is known — the exact move R19-V1 forbids ("Do not … retroactively redefine the target"), and it would also change the output schema `mado-tw-recall-r19-v1` that the closure's receipts bind.

Note the guard's independence property, which Design A preserves and B destroys: recall honesty does **not** depend on whether any row is classified observed vs lead — only on lead rows remaining findings rows.

## F2 (decisive, block-level): under Design B the P/H "want clean" cases can no longer detect demotion — the counter could not tell a fix from a relabel

`tw-precision.py` (working-tree draft, `.ufo/waves/round-20/tw-precision.py:72-91`) normalizes rows read from the verdict's `findings` list, `evidence = row.get("evidence", "observed")` restricted to `("observed","lead")`, and compares exit + the multiset of `(class, rule, line, evidence)`. Under Design B, a tool that keeps the round-19 frozenset false positive verbatim but moves it to a `leads` list and exits 0 would read **pass** on every P case (exit 0 == 0, findings multiset empty == empty) — the counter never reads `leads`. Same for H (help/dry-run) cases. Design A catches the same lazy tool immediately (row present → exit 1 ≠ want 0 and a nonempty multiset). The pre-registration's no-approximation clause — "every P case also passes at 9c54c56 (**the pre-harm reading is restored, not approximated**)" — is only enforceable if demoted rows remain visible to the counter. Design B does not merely complicate consumers; it voids the guard's discriminating power. This is the same failure shape round 19 was rejected for (a marker that hides the harm), inverted.

## F3 (high): the harm mechanism is confirmed in code as an *unmarked ordinary finding*, and the fix that restores pre-harm precision is E2 row-removal, not lead placement

`tools/mado-tripwire.py`: `helper_argv_leads` (line 1379) feeds literal argv through `classify_shell(shlex.join(vals))` into the same findings stream as real spawns — no marker, no separate list; the docstring's "reported as a lead" (lines 42-48) is prose only. The gate is `name not in PURE_ARG_CALLS` (line 1432), and `PURE_ARG_CALLS` (lines 1252-1258) is a closed 30-name set: `print, list, tuple, set, dict, sorted, …` — **`frozenset` is absent**, which is exactly why `BLOCK=frozenset(['pacman','-Q','hyprland'])` became `package_query/pacman:-Q`, exit 1 (closure's empirical run reproduced at `9c54c56` exit=0 vs `b435568` exit=1). Consequence for the decision: **neither lead placement restores precision by itself**; E2's generalized purity (un-rebound builtins, known-pure stdlib, visible pure bodies, transitive depth ≤ 4) must remove the row. Placement decides only what happens to the *surviving* genuinely-uncertain rows. A report claiming "lead tagging fixes the frozenset harm" would be false and must not be written.

## F4 (high): consumer census — every registered consumer projects findings; Design A breaks none, Design B breaks at least five

All verified by reading committed bytes at `e629f73` (or, for round-20 drafts, the working tree — see F6):

| Consumer | Reads | Under Design A | Under Design B |
|---|---|---|---|
| `tw-recall.py` (r19, registered) | `findings[].file/line` (`:74`) | 6/6 unchanged | **5/6 — guard fails** |
| `tw-precision.py` (r20 counter) | `findings[]` + `evidence` default observed (`:72-105`) | L cases measurable (lead rows in findings) | **L cases unmeasurable; P/H demotion invisible** |
| `tw-recall-split.py` (r20 split) | `findings[]` + `evidence`, `unmarked` for old tools | reports the required observed/lead split | split splittable, but fed by a findings list that no longer contains leads |
| `corpus-diff.py` (r20 guard) | `findings[]` + `_evidence` default observed (`:127-137`) | sees and classes the added lead row on real corpus data | **lead surface invisible; "classes every added row" vacuous** |
| `--selftest` (11 suites) | projects `(class, rule, line[, basename])` (`:2040-2046`) — **ignores evidence** | all green with zero case edits (old `want_findings` have no evidence key) | **every case whose row becomes a lead fails** — r19-helperfn alone carries ≥8 such cases (`py-lead-cross-cell-literal`, `py-lead-two-calls`, `py-lead-nested-literal`, `py-helper-literal-list`, `py-helper-shell-string`, `py-helper-two-hop`, `py-helper-literal-twice`, … each expecting exit 1 + a package_query/host_mutation row) |
| `--frozen` (r18 + r19 baselines) | projects `(file, line, class, rule)` (`:1960-1965`) | round-19 `frozen_match` holds **without re-pin** (evidence key not projected; exit/label unchanged) | r13:4 leaves `got` → `missing` → `frozen_verdict_mismatch` on the baseline round 19 just pinned (`50d2a45e…`) → forced re-pin of both baselines |
| `verdict_of` label (QUALITY 24 citations) | `label = "clean" if not findings else ("findings" if unpermitted else "permitted_only")` (`:1621`) | a lead reads `MADO_TRIPWIRE: findings`, exit 1 — "evidence to adjudicate" | a lead-only transcript prints **`clean`/exit 0**, silently widening what a cited `clean` verdict bounds |

`counts`/`unpermitted` (computed over `findings`, `:1615-1616`) stay inclusive under A; receipts that assert exact counts over transcripts containing lead shapes will legitimately move and get re-cut producer-bound with the new tool sha — normal lane practice, not a defect.

## F5 (medium): what each choice must say — the report obligations

**If Design A (the decision):** the round report must state (a) the frozenset harm is repaired by purity-based row *removal* (E2), evidenced by the P family passing at both `9c54c56` and final with zero rows — never by tagging; (b) surviving leads remain findings rows with `evidence: "lead"`, exit 1, label `findings`, and the verdict gains `observed_findings`/`lead_findings` counts (E1), with the split over the frozen six reported by `tw-recall-split.py` beside the unchanged `tw-recall.py` 6/6 — r13-root:4 expected `lead`, the three baseline lines and r14:2,3 per the tool's BashCVar classification ([UNK] which of observed/lead for r14:2,3 — their recipe strings' execution path is not fully visible to me; the recall guard is insensitive to that classification, which is F1's point); (c) the corpus-diff receipt classes the added lead row(s) explicitly; (d) round-19 frozen replay is recorded and, on the projection above, needs **no** re-pin unless the tool changes firing on pinned inputs.

**If Design B were chosen anyway:** honesty would require, before any measurement: a new counter schema (the registered one cannot see leads), a re-registered recall instrument with re-pinned expectations and re-pinned r18+r19 frozen baselines, case edits across ≥ 3 suites (≥ 8 helperfn cases + frozen expectations), and a fresh pre-registration written **before** the tool edit — i.e., a restart of the round's C1 registration. Adopting B inside this round's registration would fail R19-V1's standard (target/instrument redefinition after results are known) and should be reported as an admission breach, not a design preference.

## F6 (medium, integration-order): the round-20 instruments are still uncommitted

`git ls-tree e629f73 --name-only .ufo/waves/round-20/` returns only `evidence/` — `tw-precision.py`, `tw-recall-split.py`, `corpus-diff.py`, `harm-watch.sh` exist only as working-tree drafts. The pre-registration binds the counter as "written in wave 1, **committed before any tool edit**". No tool edit has landed (`tools/` clean at `367be947…`), so the ordering is still satisfiable — L1 must commit these instruments before integrating any tool change, or C1's own provenance rule is broken. (Note for the L-family cases.json: under the decision, L cases carry `want_exit: 1`; a `want_exit: 0` L case would encode Design B and mismatch the registered counter.)

## Residual risk and verification gaps

- I did not run any round-20 tool (none exists yet); all Design-A/B behavior claims about the future tool are derived from the registered contract plus the committed r19 code paths cited above. [INFERENCE] where marked.
- r14-source-safety.jsonl:2,3 observed-vs-lead outcome under the final tool: not determined here ([UNK]); the recall and precision guards are insensitive to it by construction (rows stay findings rows either way).
- The observed/lead split reporter's `unmarked` bucket (for old-tool rows) is a draft-seat choice I did not audit beyond its findings-list read.
- The selftest case census quoted (≥8 helperfn lead-shape cases) is from `.ufo/waves/round-19/tripwire/r19-helperfn/expected.json`; I did not enumerate the other 10 suites case-by-case for additional lead-affected entries — the breakage count under Design B is therefore a lower bound.

## Limits

Read-only: no lane file was edited by this seat; no fixture code was executed (transcript and fixture bytes read as data only); no gate/selftest/scan of live transcripts was run beyond `git show`/`sha256sum`/`python3` parsing of committed bytes and the two frozen input files; no pacman/sudo/systemctl/hyprctl or any host-paused command; no installs.

## Installs

none.
