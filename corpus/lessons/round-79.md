# mado round 79 — the static reserve under the band, and a per-row runbook (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — the static `monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT`
reserve composes with the bar's own band (23 frozen cases 23/23, twelve mutants killed 12/12, held
r78 tool 18/23, the eighteen r78 cases carried byte-identically); **C2 operability** — the read-only
runbook executes per-row bindings, four documented model refusals and the keybindings shape row
(22 rows / 22 distinct anchors, 22/22 matched, `control_new=0/5`, nine matcher mutants killed).
Freeze `5eb8f20f`; measured `5eb8f20f`. Declaration:
`.ufo/waves/round-79/claims-declaration-r79.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M79-1 | evidence command: the round-78 filed "before" command was not replayable — the counter mutates the candidate source, so at the base revision it exits 2 (`mutant opposite-margin-dropped anchor occurs 0 times`) instead of printing a verdict | round-78 closure D2; the filed command at `f597eccb` exits 2, while the receipt's `mutants=0 killed=0` line is the `--no-mutants` path | QUALITY 118 (replay the declared command once before filing) did not catch it: the declaration printed only the after-command, and the before-command was a report sentence | the r79 C1 counter treats an absent anchor as `not killed` and prints `reason=anchor-absent`, so one argv yields a verdict at both ends. Shown able to fail: `receipts/control-c1-r79-at-base.txt` prints `killed=4`, `verdict=TARGET_MISSED`, rc 1 at `e4b153df`, where the r78 counter's filed command still exits 2. |
| M79-2 | instrument defect found pre-freeze by a sandbox dry run: the C2 counter's mutant child invocation omitted its `cwd`, and two mutation anchors were written against source lines that do not exist (`anchor occurs 0 times`) | the pre-freeze dry run on `/fast/scratch/hyaku/mado-r79/l1-c2`: `TypeError: run() missing … 'cwd'`, then `ERROR (stage=setup mutant refusal-stage-blind anchor occurs 0 times, not once)` | the counter's own anchor guard (fails loudly, never a silent zero) plus a dry run against a scratch clone before the freeze commit | `cwd` passed; the anchors re-cut to the `refusal_matches` and `lines_shape` bodies; the fixed set kills 9/9 (`receipts/measurement-c2-r79.txt`). The pre-fix bytes are reproducible: re-running the old anchors prints the same setup error. |
| M79-3 | record drift: the frozen round-78 counter's contract example still prints `tool_selftest=22/22`, the tracked tool's `VERSION` said `r78-v1` while the report called the repaired bytes `r78-v2`, and the r77 erratum's "the tracked tool is `r78-v1` … selftest is 22/22" is a present-tense sentence about a moving path | round-78 closure D1; the base receipt `receipts/control-c1-r79-at-base.txt` prints `tool_selftest=28/28` at `e4b153df` while `quality/counters/c1-r78-margins.py:15` still says `22/22` | the round-79 base measurement (the only thing that reads the r78 bytes and prints their own tally) | the r79 generation sets `VERSION = "r79-v1"` and every r79 row prints the measured tally (`43/43`); the frozen r78 counter's bytes are **not** rewritten (that would break the r78 receipt's sha) and its example is recorded as time-bound here; the r77 entry's sentence is corrected by an appended erratum. Shown able to fail: the base receipt prints 28/28 against the 22/22 example. |
| M79-4 | generator residue: the first C2 case generator carried an unused `churn` key on the four refusal cases (the schema's keys are `samples`/`negatives`), so the intended churn sample was silently not scored | `make-c2-cases-r79.py` first run; the generated JSON had `churn` and one `samples` entry | the generator's own schema check (a key the counter never reads is dead weight) plus the counter's carried-field assertion, which would have compared it in later rounds | key removed; the surviving `samples` entry is the churn sample and the refusal rule scores it (`measurement-c2-r79.txt`). Re-adding the key changes no count — which is exactly the defect: a sample that never runs. |

Sweep for a fifth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c1-r79-reserve.py quality/counters/c2-r79-runbook.py` → no output.
Second sweep (dead keys in the new control sets): `python3 -c "…set(case)-{'name','config',…}"` → the only keys are the ones the counter reads.

## Gate (sources opened this round)

Census at round start `e4b153df` → 401 registry rows, `sources-census.sh validate --root …
mado` exit 0 (standing W04 duplicate-URL warnings); at round end → 404 rows, exit 0. Two rows
added and one rejected row added; four `used-by` cells moved in place. Both new rows were fetched
this round at the pinned commit and are byte-identical to earlier pins (`fetch/sha256-r79.txt`).

| row | source and locator (opened 2026-11-04) | status | located quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S465 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/output/Monitor.cpp — `applyMonitorRuleSoft` `:653-655`, `logicalBoxMinusReserved` `:1772-1774`; sha256 `9cf88e15…`, 112738 B | mined (new) | `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea);` | the applied rule's reserve becomes the monitor's static band, and the layer plane starts from the reduced box; it does not say how a dynamic band is added |
| S466 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/desktop/reserved/ReservedArea.cpp — `calculate` `:43-51`, `setStatic` `:69-74`, `addType` `:101-112`; sha256 `0a52e145…`, 3339 B | mined (new) | `m_bottomRight += e.bottomRight;` | the static initial box and every dynamic contribution are summed; it does not name which surface contributed |
| S457 | `…/src/render/Renderer.cpp` — `arrangeLayersForMonitor` `:2673-2700` (reset `:2680`, parent `:2682`, add `:2696`) | mined (re-opened, byte-identical) | `const CBox ORIGINAL_USABLE_AREA = PMONITOR->logicalBoxMinusReserved();` | the layer delta is measured against the static-reduced box; not a per-consumer attribution |
| S458 | `…/src/debug/HyprCtl.cpp` — monitors `reserved` print `:281-282` | mined (re-opened, byte-identical) | `sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top())` | the print order `[left, top, right, bottom]`; not which contributor set a band |
| S459 | `…/src/desktop/reserved/ReservedArea.cpp` — parent/child ctor `:19-35`, `apply` `:53-60` | mined (re-opened, byte-identical) | `m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());` | the parent/child delta arithmetic; not the sum with the static term |
| S303 | `…/src/config/legacy/ConfigManager.cpp` — `handleMonitor` `:1299`, `addreserved` `:1319-1341` | mined (re-opened, byte-identical) | `area = {std::stoi(std::string{ARGS[2]}), std::stoi(std::string{ARGS[5]}), std::stoi(std::string{ARGS[3]}), std::stoi(std::string{ARGS[4]})};` | the written field order TOP, BOTTOM, LEFT, RIGHT and the same-selector rule write; not the apply path |
| S461 | installed `waybar(5)` 0.15.0 (`S461.txt:91`) | mined (re-opened, byte-identical render) | `Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&` | the declared placement keys; not the compositor's arithmetic |
| S462 | `…/Waybar/90b209ad…/src/bar.cpp` — the raw URL returned 404 when re-fetched 2026-11-04; the r78 byte-identical pin (sha256 `120eb913…`) is reused | mined (pin reused, not re-fetched) | `gtk_layer_auto_exclusive_zone_enable(gtk_window);` (from the committed pin) | the auto-zone call; the claim does not rest on it this round and the pin is unchanged |
| S464 | `…/gtk-layer-shell/v0.10.1/src/layer-surface.c` — `:264-292` | mined (re-opened, byte-identical) | `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` | the client's unanchored-edge addition; not the compositor's |
| S467 | https://wiki.hypr.land/Configuring/Monitors/ as committed at `.ufo/waves/round-45/fetch/wiki-Monitors.md:179`; the live URL **404s** on 2026-11-04 | rejected (new) | `monitor = name, addreserved, TOP, BOTTOM, LEFT, RIGHT` | REJECTED: documents the line syntax only, not the static-plus-dynamic summation the entry claims, and the live page no longer resolves; flip = a resolving page with a revision pin that states the composition. |

Admit/reject sample for the non-author spot-check: admit S465 and S466 (the two rules the claim
rests on), reject S467 (same reason as filed).

## Wave findings (append-only; written as the seats settle)

Seats: 14 in one v1 wave (`w1-spec.json`, `w1-dispatch.json`, `w1.ready`). Findings land here
as the wave reports; a seat that settles without a report is disclosed, never backfilled.
