# mado round 78 — the margined band and a churn-resistant runbook (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — the margined auto exclusive-zone composition becomes a modelled join
(client auto zone + compositor edge margin; 18 frozen cases, 7/7 mutants, held r77 model 8/18);
**C2 operability** — the read-only runbook binds its volatile rows by shape and survives committed
churn (17/17 executed and matched, 12 shape-bound, held fixed-value rule 5/17). Freeze `b8508bd9`;
pre-wave amendment `44a36b64`; measured `d27c5ff4`. Declaration:
`.ufo/waves/round-78/claims-declaration-r78.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M78-1 | frozen fixture defect: three margined cases paired a width-spanning live box with a margin-narrowed declaration (`x=0/w=1920` and `x=0/w=3440` where the declaration gives `x=4/w=1912` and `x=4/w=3432`), so the correct tool reported `box=DIFFER` | the freeze measurement `cases=18 correct=15` (15/18) reproduced by the wave connector at `.ufo/waves/round-78/w1/R78ConnSiblings/receipt-freeze-controls-c1.txt`; corrected set at `receipts/measurement-c1-r78.txt` → 18/18 | the counter itself — a wrong expectation cannot become a green measurement (the same class as round-77 M77-5) | generator boxes corrected before the wave (`44a36b64`), no expectation moved; the old fixtures still produce `correct=15`, the new ones `18`. |
| M78-2 | frozen fixture defect: one churn sample `wallpaper,waybar,walker` is not in sorted order, so the `sorted_unique` rule correctly rejected it and the case failed | first C2 measurement `matched=16/17`; connector reproduction `.ufo/waves/round-78/w1/R78ConnSiblings/receipt-freeze-controls-c2.txt` | the churn clause of the counter (a sample the rule rejects is not a tolerated variant) | sample re-sorted to `walker,wallpaper,waybar`; the old sample still scores 16/17. |
| M78-3 | privacy: the C2 receipt quoted the raw `hyprctl monitors -j` output, including the output's real serial and description (serial-shaped token; value redacted here) | `quality/check-session-material.py --rev 90fc8d84` → `FINDING … rule=R5_SERIAL_PROSE tokens=1`; after the fix 291 findings at both base and tip, none on a round-78 path | the lane's session-material gate (R5), not a reading of the receipt | JSON-shaped probes print `json-bytes=` instead of the text; the receipt and capture were regenerated; the monitors capture is a reduced derivation (no serial/description). Re-running the gate on the old receipt reproduces the finding. |
| M78-4 | scoring: the C2 anchor leg was a file-wide substring test (`anchor in SKILL.md`), so deleting the named table row still scored `anchors=17/17` | wave connector: 11 of 13 anchors occur more than once in `SKILL.md`; `'hyprctl version'` survives deletion of its row | the wave connector (the lane's own reviewer of the claim, per §3) | the check now requires the anchor in a table row's command cell; three selftest assertions pin prose and non-command cells as refusals (34 → 37 assertions), and the deleted-row fixture goes red. |
| M78-5 | ledger row shape: the r78 edit to the `tools/mado-barfoot.py` row inserted newlines, so the row had two cells and the instrument read `uncovered` | `check-tool-ledger.py --rev b8508bd9` and `--rev 44a36b64` → `verdict=TARGET_MISSED uncovered=1 dangling=1`; `fa6f3fda` → `142/142 TARGET_MET` | the tool-ledger gate, on the freeze commit | the row is one physical line; the malformed shape is reproducible by re-wrapping it. |
| M78-6 | provenance drift: the declaration names generators as `controls/make-*.py` (they live under `.ufo/waves/round-78/controls/`), the fetch directory landed after the freeze commit, and the receipts committed at `44a36b64` carry `rev=b8508bd9` | wave connector §3: three links do not resolve as written | the connector's provenance-chain check | an append-only `## Provenance notes` block in the declaration names the full paths and the landing revisions; the final measurement receipts are committed at the measured revisions. |
| M78-7 | stale present-tense claims about the tool: the r77 registry row (`SKILL.md`, `mado-r77-barfoot`) still printed 18/18 and `NOT_MODELLED`, the r77 index row said "the margined exclusive zone stays `NOT_MODELLED`", and the r77 entry's §3/§4 described the old instrument | wave connector §2.2–§2.3 (`SKILL.md:746`, `corpus/README.md:176`, `corpus/knowledge/bar-footprint-r77.md:47,51`) | the connector's record scan, and the lane's own "corrections sweep every mention" rule | registry row corrected in place (22/22, new exit map, both frozen sets); index row corrected; r77 entry received an appended erratum; the r77 body stays the record of the r77 instrument. |
| M78-8 | time-bound citation: the r77 SCORECARD row's parenthetical "at `a83e9bee` (its instrument's last change)" became false when this round changed the same tool path | `quality/check-cited-revisions.py` on `SCORECARD.md:4416` → `RESULT red claims=1 mismatched=1` (connector receipt) | the lane's cited-revision probe | an append-only `### Corrections (round 78)` block names the time-bound phrase; the r77 measurement stays valid for the r77 bytes. |

Corrections: the M78-3 row first quoted the monitor serial it was redacting; the token is
removed here in place (a privacy fix outranks append-only) and the round-78 harm-watch receipt
carries the gate's finding count before and after. No other serial-shaped string appears in the
round's committed files.

Sweep for a ninth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c1-r78-margins.py quality/counters/c2-r78-runbook.py` → no output.

## Gate (sources opened this round)

No new registry row was written this round: the seven rows the claims cite already exist and were
re-opened 2026-11-04 with fresh pinned fetches (`.ufo/waves/round-78/fetch/`, `sha256-r78.txt`; the
six code files are byte-identical to the round-77 copies, `waybar(5)` is a fresh render of the
installed page). Row statuses stay `mined`; `used-by` gained
`corpus/knowledge/bar-footprint-margins-r78.md` (old → new for S457, S458, S459, S460, S461, S462,
S463 and S464 — the rejected S463 included, because the new entry cites its rejection).

| row | source and locator (opened 2026-11-04) | status | located quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S457 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp — `applyExclusive` `:2529-2585`, add `:2577` | mined | `*edges[i].positive_axis += exclusive + edges[i].margin;` | the compositor adds the anchored edge's margin to the exclusive zone; it does not name the client's contribution |
| S458 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/debug/HyprCtl.cpp` — `:281-282` | mined | `sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top())` | the `reserved` print order; it does not say which surface set a band |
| S459 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/desktop/reserved/ReservedArea.cpp` — `:19-35` | mined | `m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());` | the parent/child band arithmetic; not a per-consumer attribution |
| S460 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/protocols/wlr-layer-shell-unstable-v1.xml` — `:152-190` | mined | `The exclusive zone includes the margin.` | the protocol contract for the zone; it is not host behaviour |
| S461 | installed `waybar(5)` 0.15.0, `BAR CONFIGURATION` (`S461.txt:91`) | mined | `Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&` | the declared placement keys; not what the compositor does with them |
| S462 | `https://raw.githubusercontent.com/Alexays/Waybar/90b209add8937514d0a987aa842e701bd8f1232e/src/bar.cpp` — `:178-222`, `:357-361`, `:390-424` | mined | `gtk_layer_auto_exclusive_zone_enable(gtk_window);` | the auto-zone call under the exclusive mode; not gtk-layer-shell's arithmetic |
| S464 | `https://raw.githubusercontent.com/wmww/gtk-layer-shell/v0.10.1/src/layer-surface.c` — `:264-292` | mined | `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` | the client adds the unanchored edge's margin; not the compositor's addition |
| S463 | `https://wayland.app/protocols/wlr-layer-shell-unstable-v1` as served 2026-11-04 | rejected (re-confirmed) | `wlr layer shell protocol` | REJECTED again: no protocol/compositor revision pin, so it cannot ground a 0.56.2 claim; flip = a commit/tag pin for the rendered protocol. |

Admit/reject sample for the non-author spot-check: admit S457/S464 (the two rules the claim rests
on), reject S463 (same reason as round 77).

## Wave findings (append-only; written as the seats settle)

- **R78ExecC1Cases (executor, independent re-derivation).** Re-derived all eighteen expectations
  from the two source rules before running the tool: 18/18 agree, the held r77 tool on the same
  fixtures 8/18 (equal to `base_correct`), and it confirmed the arithmetic identity
  `expected = extent + margins[opposite edge]`. No defect found; receipt under
  `w1/R78ExecC1Cases/receipt-c1-cases-tool-run.txt`.
- **R78ScribeEntry (scribe).** Its draft entry supplied the structure the landed entry uses
  (per-case worked table, line-anchored decision table, explicit "no live observation" limits);
  the landed version adds the round's live join (reduced capture) and the corrected mutant scores.
- **R78ScribeSources (scribe).** Confirms the registry delta: 401 rows before and after, no id
  change, exactly eight rows differ and only in `used-by`; quotes located byte-exactly; census exit
  0 with only the standing W04/W01 warnings. F1 (the fetch manifest had six lines when an entry
  sentence named it) is resolved — the manifest now pins seven files and `sha256sum -c` is OK. F2
  (thirteen untracked `S465…S477` files in `fetch/`) is a seat write-scope deviation: the files
  were gathered by the scout into a committed directory instead of its own write dir; they are
  relocated to `w1/R78ScoutMargins/fetch/` and never committed as registry evidence.
- **R78ExecC2Shapes (executor, attack).** Six weak-shape negatives were accepted by the r78 rule:
  an rc-0 error line beginning with a version token (`version` regex), newline-only
  `configerrors`, padded integers (`"1720 "`, `"\t3"`, `" 7"`), an object with extra keys, and a
  padded list part in `sorted_unique`. Repairs that touch no case: the integer rule now accepts
  bare digits only and `sorted_unique` refuses padded parts (selftest 34 → 40 assertions, mutants
  still 5/5). The `version`, extra-key and empty-output shapes are named case-level limits in the
  declaration's `## Known limits`. The seat's PATH-shim run proves the general limit: a runbook
  cannot authenticate the binary it calls; it certifies the answer's shape, not the pins' truth.
- **R78ConnSiblings (connector).** No sibling lane claims the layer-shell plane, the band or the
  runbook (one shared read verb with game-dev-2d). It broke the anchor leg (M78-4), found the
  ledger-red freeze (M78-5), the provenance drift (M78-6), and the stale registry/index/entry
  claims (M78-7) — all repaired this round; M78-8 is the time-bound r77 citation, recorded
  append-only in SCORECARD.
