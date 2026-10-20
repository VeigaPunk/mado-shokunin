# Mado round 13 — AttackClaims (critic, leaf)

Seat `MadoR13.AttackClaims`. Scope: whether C1 (coverage, U4) and C2 (operability, exact-set census) can be separated causally, plus their local score rubrics.
Axes judged: coverage, operability. Observed 2026-10-20 (gate snapshot 04:11:21Z).
Not run by this seat: builds, lint, formatters, `--selftest`, `--regression`, live gate, host config reads. The only computations were read-only: `git show`, `sha256sum`, `grep`/`awk`, and one Python mapping of `globals.json` interface names against the installed protocol XML under `/usr/share`.
Tools installed or updated by this seat: none. (`wayland-utils 1.3.0-1` was already present. `pacman -Qi` reports Install Date 2026-10-20 01:06:49 −03, Install Reason "Explicitly installed". Recording it belongs to `MadoR13.GlobalCapture`.)

Anchors:
- Claims: `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:329-353`. Uncommitted: `git diff --stat` shows +26; file sha256 `23641363…`.
- Baseline gate: `git show 7dcb785:tools/mado-verify.sh`, sha256 `ea798ad078f139f3…`.
- In-flight gate: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`, sha256 `3fb2a695…`, 3,384 L. It is **in-flight** (QUALITY criterion 9) and was owned and being edited by `MadoR13.GateImplement`.

---

## Verdict summary

| # | Finding | Kind | Axis hit |
|---|---|---|---|
| A1 | The in-flight edit rewrites recorded defect D6 inside the pinned tameshi spec. `SPEC_SHA` no longer matches, so the selftest's R11 assertion fails and `--regression` returns SETUP. Repinning `SPEC_SHA` would relabel a self-written defect as "the recorded case". | **fixable defect** (identity change / false provenance) | operability (harm watch) |
| A2 | The C2 baseline is not 0/4. By static reading of `7dcb785`, 2 of the 4 declared cases already fail with a stable row id and named members. A third is detected but only half-named. A "0/4 → 4/4 = 10.0" report would inflate the score. | **fixable rubric defect** | operability |
| A3 | C2's 4-case, self-chosen denominator steps in 2.5 increments. Reaching 10 crosses the 9.0 saturation line in the same round the sub-axis was invented. That is premature saturation. | **tradeoff → reject a saturation claim** | operability |
| A4 | C2 bundles a SKILL registry row that does not move its own score. | fixable (scope hygiene) | operability |
| A5 | C1's rubric is one boolean per U item. The three facets the claim names (phases, advertised globals, unexercised behavior) are invisible to the count. | **fixable rubric defect** | coverage |
| A6 | 27 of the 71 advertised interfaces are outside the wayland-protocols phase system (6 core, 21 outside the installed registry). A note that phase-classifies all of them would be false provenance. | **counterexample** to a likely C1 overreach | coverage |
| A7 | The C1 count prints U-ids even when the source join fails. Count and join are separate commands (`after-measure.sh:23-25`). | fixable | coverage |
| A8 | Causal separability holds at code level, but the harm watch leaves out freshness. C2 changes the semantics of rows that freshness 29/29 counts. | **fixable gap** (hidden regression channel) | operability, freshness (harm) |
| A9 | `globals.json` carries `set_sha256`, but its membership is a multiset: 72 globals, 71 unique, `wp_drm_lease_device_v1` appears twice. It is also scoped to this hardware and session. | fixable labeling | coverage |

---

## A1 — The D6 rewrite breaks the recorded spec identity (in-flight)

**Counterexample.**
- In the baseline, the spec heredoc (`tools/mado-verify.sh` @ `7dcb785`, `mado_r7_spec_write`) with its trailing LF stripped hashes to `c7ee75b97c38ac8f…`. That equals `SPEC_SHA`, now at `tools/mado-verify.sh:1393`.
- The in-flight heredoc hashes to `00fddeae4297cf11…`.
- The changed lines are `tools/mado-verify.sh:1452-1454`:
  - `@defect D6 | clause D: gkeep dropped from the 13-conf local inventory`
  - `@old (… ai-usage gkeep autostart envs xdph)`
  - The recorded D6 was "xdph dropped from the 12-conf local inventory".

**Evidence that this fails.**
- The selftest asserts `R11: the embedded spec is byte-identical to the recorded case` against `SPEC_SHA` (baseline `tools/mado-verify.sh:567-569`).
- `--regression` refuses with `MADO_REGRESSION: SETUP (embedded spec sha256 … != recorded …)` (baseline `:1529-1530`).
- The header contract (baseline `:1223-1233`) says: "Case (recorded, not re-derived) … the recorded spec, written verbatim from the heredoc below and re-checked against SPEC_SHA".
- Re-cut records for rounds 8 and 9 (`:1249-1271`) moved `PIN_MADO` only. `SPEC_SHA` and the defect texts never moved.
- The GateImplement assignment does say "Existing mutation D6 anchor must be updated to match new LOCAL once L1 recuts" (`spec.json`, item GateImplement).

**Impact.**
- Either selftest drops from N/N to N−1/N, or L1 repins `SPEC_SHA`.
- A repin turns `TABLE_MADO`'s `D6:KILLED` into a claim about a different, self-written defect. It would still be labelled as tameshi's recorded round-6 case `c7ee75b9…` (`corpus/knowledge/gate-mutation-proof.md` §1). That is false provenance, and the regression would no longer replay what it says it replays.

**Smallest safe correction.**
1. Restore the heredoc byte-for-byte to `7dcb785`. `SPEC_SHA` then holds at `c7ee75b9…`.
2. Keep the `LOCAL=(hyprland … ai-usage autostart envs xdph)` line byte-identical to baseline `:2263`.
3. Add gkeep on its own line: `LOCAL+=(gkeep)`, with the round-13 erratum comment.

Effects:
- D6's `@old` matches exactly one site again (today `grep -F` finds 0 code matches; the 12-name string appears only at `:1454` as `@new`).
- D7's `@old` still matches exactly one code line (`:2339`) — that check is clean today.
- Under exact-set semantics, the recorded D6 mutant (xdph removed from the expected set) makes the fixture's `xdph.conf` an *extra* member. Scenario A turns FAIL, so the mutant is still killed [INFERENCE from the fixture loop, baseline `:265`; L1's re-cut measures it].
- Only `PIN_MADO` needs L1's measured re-cut, which is the established practice.

Message sent to `MadoR13.GateImplement` at 04:11Z.

## A2 — The C2 baseline already detects some of its "negative" cases

The claim (`SCORECARD.md:339-344`) reads: four isolated cases "fail with stable row ids and named missing/extra details, versus the same cases at the baseline. Score = 10 × detected cases / 4."

Static derivation against `7dcb785` [INFERENCE from code; L1 must measure by running the new fixtures against `git show 7dcb785:tools/mado-verify.sh`]:

| Declared case | Baseline row(s) and detail | Stable id FAIL? | Missing named? | Extra named? | Meets criterion at baseline? |
|---|---|---|---|---|---|
| extra local (`foo.conf` added) | `hypr.local.inventory` PASS `12/12` — presence loop `:2266-2268` ignores unlisted files | no | — | no | **no** |
| missing+extra local (`xdph.conf`→`foo.conf`) | `hypr.local.inventory` FAIL `missing: xdph.conf` (`:2272`) | yes | yes | no | **no** (half) |
| same-count source replacement (one `source =` value swapped) | `hypr.root.include_graph` FAIL `line k: got '<extra>' want '<missing>'` (`:2230,2235`) | yes | yes | yes | **yes** |
| missing gkeep (`gkeep.conf` removed) | `hypr.root.sources_resolve` FAIL `unresolved: ~/.config/hypr/gkeep.conf` (`:2243-2254`). The selftest already asserts it: `:951` "B (round 12: removed gkeep.conf)" | yes | yes | n/a | **yes** |

**Honest baseline:** 2/4 = 5.0 under the declared criterion, or 3/4 = 7.5 counting detection alone. It is not 0/4. A report of "0 → 4/4" would overstate the improvement by 2–3 cases.

**Correction:**
- Measure the baseline column by running the round-13 fixtures against the `7dcb785` bytes.
- Report "baseline k/4 → after m/4" using the measured k.
- Make the cases discriminating. "Same-count source replacement" is already covered at baseline, *except* that the baseline loop `break`s at the first mismatch (`:2231`). Two simultaneous substitutions name only the first. Use that two-substitution case.

## A3 — A 4-case all-or-nothing scale with same-round saturation

- The case list is written in the same round as the fix.
- One case moves the score by 2.5. "4/4 = 10.0" passes the 9.0 saturation line (`SCORECARD.md:272`) the round the sub-axis is created.
- Fleet round 1 already recorded the same trap for a finite denominator: "Completing navigation can reach 10 on this finite corpus without saturating the province's broader coverage axis" (`SCORECARD.md:52-53`).

**Proposed measurable count (replaces the /4 score; no new axis).** Report it under operability as cells satisfied out of total cells, with the baseline measured per cell. A cell is satisfied only when all four hold:
- (i) the owning stable row id is FAIL;
- (ii) *every* missing member is named;
- (iii) *every* extra member is named;
- (iv) no other hypr row changes verdict (isolation).

| Cell | Set | Perturbation | Owning row | Baseline (static) |
|---|---|---|---|---|
| S1 | root `source =` list | delete one line | include_graph | no — count only `17 … (expected 18)` (`:2226`) |
| S2 | root list | add one new line | include_graph | no — count only |
| S3 | root list | one same-count substitution | include_graph | yes |
| S4 | root list | two same-count substitutions | include_graph | no — first only (`:2231`) |
| S5 | root list | duplicate an existing line (+1) | include_graph | no — count only; a pure *set* compare would miss it, so keep multiset/count (D7's anchor) |
| S6 | root list | swap two lines (order only) | include_graph FAIL; set rows must stay PASS | yes for include_graph; checks that order and membership verdicts stay separate |
| L1 | `$H/*.conf` names | remove `xdph.conf` | local.inventory | yes |
| L2 | `$H/*.conf` | add `foo.conf` | local.inventory | no |
| L3 | `$H/*.conf` | `xdph.conf`→`foo.conf` | local.inventory | no (extra unnamed) |
| L4 | `$H/*.conf` | remove `gkeep.conf` | local.inventory (+ sources_resolve) | no at local row; yes at sources_resolve |
| T1 | source targets | remove `gkeep.conf` | sources_resolve | yes |

Static baseline: S3, S6, L1 and T1 = **4/11**.
- The four claimed cases become L2, L3, S4 (or S3) and L4/T1.
- The headline stays bounded: "11 cells, baseline 4, after N". Saturation on this finite list does not retire broader operability.

Rules to state in the rubric:
- **Glob scope.** `EXPECT` holds the declared string `~/.local/state/omarchy/toggles/hypr/*.conf`. Set membership compares declared strings; expansion is only checked as "≥1 match" (`:2247`). State this, otherwise a toggle-file swap reads as covered when it is not.
- **Detail-text drift.** The in-flight PASS details change, e.g. `"13/13 active local confs, set exact"` (`:2406`, `:929`). Snapshot-diff receipts that compare detail strings will report CHANGED against round-12 snapshots. Record that as an expected, cause-named delta, not as drift.

## A4 — The registry row inside C2 is unscored scope

"Register the existing verdict instrument at its SKILL registry home" (`SCORECARD.md:346-347`) does not change detection cells. It was planned as a separate operability/calibration item (`SCORECARD.md:322-323`).

**Correction:** list it as unscored hygiene, with a pass/fail check: "row present and its fields resolve". C2's verdict must not depend on it, and it must not be counted as an operability improvement.

## A5 — C1 is one boolean per U item

The rubric (`SCORECARD.md:237`) counts `^covers: U[1-7]` in the first 15 lines of an entry whose `source:` cites an S-id. A one-paragraph note with `covers: U4` and one mined row scores the same 4/7 as a full note. The three facets the claim names (`SCORECARD.md:336-337`) are not visible to the count.

**Proposed measurable sub-counts (reported beside 4/7, not replacing it; no new axis):**
- **F-count, out of 3.** One per named facet: (f1) phase semantics, (f2) advertised-globals observation, (f3) unexercised boundary. A facet counts only when it carries ≥1 claim row with an S-id that joins to a `mined` row, plus an exact quote and location at a pinned revision. f3 counts only when stated as an explicit `[UNK]`/unexercised list, never as behavior.
- **Classification count: interfaces with a provenance class at pinned revisions, out of 71 unique.** The classes are core (`wayland` XML), stable, staging, unstable-legacy, and outside-registry. Baseline 0/71. My read-only mapping against installed `wayland-protocols 1.49-1` and `wayland 1.26.0-1` (`/usr/share/wayland-protocols/{stable,staging,unstable}`, `/usr/share/wayland/*.xml`) gives:

| Class | Count |
|---|---|
| staging | 27 |
| stable | 5 |
| unstable | 12 |
| core | 6 |
| not found | 21 |

  The 21 not found are all `hyprland_*` (8), `zwlr_*` (8), `org_kde_kwin_server_decoration_manager`, `vicinae_hotkey_manager_v1`, `wl_drm`, `zwp_input_method_manager_v2` and `zwp_virtual_keyboard_manager_v1`.
  The installed package ships no `experimental/` directory, so 0 interfaces map to "experimental" from local data.
  These are measurement aids for L1. They are not admitted facts.

## A6 — Counterexample: phase vocabulary applied outside its domain

The experimental/staging/stable triad (S005, wayland-protocols README) governs only the wayland-protocols repository. Per A5's mapping, 27 of the 71 advertised interfaces are outside it:
- 6 core `wl_*` from `wayland.xml`;
- 21 vendor or unregistered interfaces (Hyprland, wlroots, KDE, Mesa `wl_drm`, a third-party `vicinae_*`).

Name-shape inference also fails:
- `zwp_linux_dmabuf_v1` keeps the legacy `z` prefix but sits under `stable/` in the local tree [OBS: mapping run].
- `wp_viewporter` is stable with no `_vN` suffix.

**Correction:**
- The U4 note must assign phases only by directory membership at a pinned package or upstream revision.
- Interfaces outside the registry must be named as outside the phase system.
- "Advertised" (`globals.json`) must be kept apart from "phase" (registry) and "exercised" (no client exercised them; `[UNK]`).
- Advertised version numbers above the XML version in the installed package must be reported, not explained away.

## A7 — The C1 count does not require the join

At `.ufo/evidence/round-12/after-measure.sh:23-25`, the U-id count (`:24`, `… | sort -u`) and the join diagnostic (`:25`, prints errors then `join-done`) are separate commands. A U4 entry that cites an unmined or misnamed S-id still prints `covers: U4`. The round-12 verdict relied on a person reading an empty error list.

**Correction:** one command that emits a U-id only for entries whose every cited S-id has a `mined` row whose `used-by` names that entry path. It should exit non-zero on any join error. Count unique U-ids from its output.

## A8 — Separability holds in code; the harm watch misses freshness

**Confirmed separable.**
- The gate does not read `corpus/`. Every `corpus/` mention in `tools/mado-verify.sh` is a comment (`:32`, `:1224` baseline, `:2197`, `:2778`).
- C1 touches no gate code.
- C2 needs no U4 note.
- The only shared surfaces are integration files: `SOURCES.md`/`corpus/README.md` (C1), `SKILL.md` (C2 registry row, plus any C1 pointer), `SCORECARD.md`, `LOG.md`. That is an ordering matter, not a causal one.

**Gap.**
- The round-13 harm watch (`SCORECARD.md:350-352`) lists the suite, regression, navigation and read-only checks. It leaves out freshness / file-plane agreement (round 12: `--no-live` 29/29, `SCORECARD.md:287`).
- C2 changes the semantics of `hypr.local.inventory` and `hypr.root.sources_resolve`, both counted in that 29.
- Any host `*.conf` outside the new 13-name expected set flips them to FAIL and lowers freshness to 28/29. A cross-axis harm like that would go unreported.

**Correction:**
- Add "`bash tools/mado-verify.sh --no-live` PASS/(PASS+FAIL+UNKNOWN) unchanged, row ids unchanged" to the harm watch.
- Before landing, take the expected local set from `MadoR13.LocalSurface`'s observed set.

## A9 — `set_sha256` over a multiset scoped to one session

`globals.json` reports `global_count` 72, `unique_interface_count` 71, and `wp_drm_lease_device_v1` twice (also one `wl_output`).

[INFERENCE] Output and DRM-lease globals depend on the attached hardware, so a monitor or GPU change would move the hash without any compositor change.

**Correction:**
- Define the hash input as a sorted multiset of `interface@version`.
- Scope the claim as "this host, this session, Hyprland 0.56.2 `efb50993…`, captured 2026-10-20T04:08:06Z".
- Never word it as "Hyprland advertises".

---

## Smallest safe correction set (for L1)

1. **A1:** restore the spec heredoc byte-verbatim and use `LOCAL+=(gkeep)` on its own line. Re-cut `PIN_MADO` only, never `SPEC_SHA`.
2. **A2/A3:** measure the baseline per cell against `7dcb785`. Report the 11-cell count (baseline 4/11 static) instead of a /4 score. Make no saturation claim on a list written this round.
3. **A4:** move the SKILL registry row out of C2's scored verdict.
4. **A5/A7:** keep 4/7 as the headline. Gate it on a single join-enforcing command, and report F-count k/3 and the classified-interfaces count n/71 beside it.
5. **A6/A9:** assign phases only by registry membership at a pinned revision. Name the 27 out-of-phase interfaces explicitly. Scope the globals capture to this host and session, and treat it as a multiset.
6. **A8:** add freshness `--no-live` agreement to the harm watch.

## Addendum — A1 status re-checked (2026-10-20T04:20:28Z, gate sha256 `d6d17641…`, still in-flight)

`MadoR13.GateImplement` reported adopting A1. Read-only re-check by this seat:
- Embedded spec heredoc (LF-stripped) sha256 → `c7ee75b97c38ac8f…` = `SPEC_SHA` (`tools/mado-verify.sh:1430`). R11 identity restored.
- D6 `@old` 12-name literal: exactly one code site, `:2449` (plus the spec line `:1490`), and `LOCAL+=(gkeep)` on its own line at `:2455`.
- D7 `@old` count test: exactly one code site, `:2387` (plus spec `:1494`).
- `PIN_MADO` is unchanged (`538d178b…`, `:1429`). L1's re-cut is still owed. Until then, R10 and `--regression` read SETUP by design.

A1 is **resolved pending L1's measured re-cut**. That re-cut must show `TABLE_MADO` with 10/10 KILLED, including D6 killed via the xdph-extra path. A2–A9 are unchanged.
