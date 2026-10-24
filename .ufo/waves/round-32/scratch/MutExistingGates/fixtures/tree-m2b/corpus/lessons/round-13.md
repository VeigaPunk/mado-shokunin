# Round 13 — bounded protocol knowledge and exact-set diagnostics

Date: 2026-10-20. Baseline: `7dcb785b7b943d03703181b218d7860a7b43007b`.
Claims: C1 coverage, U1–U3 → U1–U4; C2 operability, complete named-set diagnostics in four isolated negative cases. They are independently verifiable. Motivating record: `LOG.md` round-12, `SCORECARD.md` round-13 plan, round-12 M13/R12-b and the outside S030 disagreement in `round-12-verifier-spotcheck.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | scope / duplicate evidence | Outside reviewer disagreed with S030 admission; `round-12-verifier-spotcheck.md`, `round-12.md` § Outside spot-check; S017 and S030 use the same current-wiki URL with overlapping syntax scope. The shared census reports only W04 because scope strings differ. | none specific before criterion 17; source-row identity requires human scope review | `QUALITY.md` criterion 17 screens repeated active URLs before merge/renumbering. A conservative lane-local collision screen exercises the actual historical admitted pair versus the corrected rejected S030; its committed red/green evidence is part of the round-13 measurement record. S045 supplies the explicit rejection correction without editing immutable S030 cells. |
| M2 | vacuous census | Round-12 M13; baseline `tools/mado-verify.sh` `sources_resolve` iterates EXPECT on disk and `local.inventory` checks only fixed-list presence. A separate positional include check already catches source substitution; this was never zero overall detection. | QUALITY 14 | Compare expected/observed declaration strings and local regular-file names; name missing/extra members; preserve source order and target resolution. The same four isolated cases run against baseline and delivered revision with both overall exits and owning-row results. Expanded toggle-glob membership is not claimed. |
| M3 | reference-drift | Round-12 R12-b's final correction; `config-drift-r12.md` originally cites omarchy-specific drift rules as authority for gate EXPECT. | QUALITY 8; gate-standing-use §5 rules 2/4 | Append the actual gate-rule citation in `config-drift-r12.md`, record S044 and correct the gate comment. Historical omarchy-source S015 is not rewritten. This is a source-location correction, not an additional scored capability. |
| M4 | session-data boundary | `.ufo/waves/round-13/w1/Safety.md` F1: GlobalCapture retained unfiltered Wayland output in world-readable scratch during the wave. | SKILL safe-probe rule 4 and the wave's explicit data fence | Owner removed both raw files and corrected its report; Safety confirmed removal. Retain only interface/version projection, stream-filter future captures and never treat scratch as durable evidence. This was a real in-round defect, not a clean initial capture. |
| M5 | unexercised helper defect | `evidence/frozen-selftest.txt` under `.ufo/waves/round-13/`: first self-invocation raised UnboundLocalError before a verdict. | the required self-invocation test, not source inspection | Main added `failed` to the nested counter's nonlocal declaration; identical `--selftest` then passed 12/12, exit 0 (`frozen-selftest-corrected.txt`). The observed red is retained. |

## Gate

### Candidate decisions

- **Admit:** `knowledge/wayland-protocol-boundaries-r13.md`, U4. Primary phase/governance and registry semantics plus a sanitized host advertisement sample support the scoped diagnostic decision table. Advertisement, client binding and feature behavior are explicitly separate. No per-interface phase crosswalk, output/colour behavior, virtual input, capture or lock experiment is admitted.
- **Reject:** “staging is a frozen stable API”; README's staging/major-version rules contradict it. Flip only with a stronger exact-protocol authority at a named revision.
- **Reject:** “advertised output/color manager proves HDR or monitor-management behavior”; a registry observation does not exercise the feature. Flip requires separately authorized end-to-end evidence.
- **Reject:** S030 as distinct current-wiki evidence; S045 records the same-page/overlapping-scope reason and a distinct-pinned-scope flip. This is correction of a prior bad admit, not evidence that more rejections is better.
- **Not admitted:** U5–U7, arbitrary source grammar, expanded toggle filename inventory, broad host-health or promotion claims.

### Opened sources and located quotes

Each quotation below is at most 25 words. Access date for every row: **2026-10-20**. Source rows remain scoped, not global trust labels.

| row | opened source / revision | located quote | disposition |
|---|---|---|---|
| S005 (reopened) | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/3dac056d83ad8947eed6eb621f346e91da736efd/README.md | §Protocol phases: “Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase.” | queued → mined; source-page SHA-256 e81ad629e8d7beba23cf4d99d0c58e4af662a7df9564d2423fff19a1eed65548 independently reopened by SourceRevision/ReviewPhases |
| S017 (reopened) | https://wiki.hypr.land/Configuring/Basics/Window-Rules/; Latest git, modified 2026-08-26 | Introductory Note: “Since Hyprland 0.55, hyprlang is deprecated in favor of lua.” | existing source remains mined; full historical S030 mapping corrected append-only in the U2 note |
| S040 (new) | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/GOVERNANCE.md | §2.1.1: “Experimental protocols begin with the "xx" namespace and do not include any relation to namespaces specified in section 2.1.” | mined; governance is not host support |
| S041 (new) | `.ufo/waves/round-13/w1/globals.json`; captured_utc 2026-10-20T04:10:03Z; Hyprland efb50993780079460b0cbed1363e2166a2de1d9f | `.globals` record: `"interface": "wl_compositor", "version": 6` | mined; sanitized own-work advertisement, not behavior; committed digest rebind is in final measurements |
| S042 (new, supersedes S006) | https://wayland.freedesktop.org/extras.html; source extras.html @ 8923a19916635c21a3577b616f650a7e45d70fa9 | §Compositor features: “Running wayland-info will list all global interfaces advertized by the compositor.” | mined; supplies missing source-revision anchor without changing S006 |
| S043 (new) | `/usr/share/wayland/wayland.xml`, Wayland 1.26.0-1; https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry | XML:143-144, bind: “Binds a new, client-created object to the server using the specified name as the identifier.” | mined; announcement/bind/removal distinction |
| S044 (new) | `corpus/knowledge/gate-standing-use.md` §5 rule 4, :222-226 | “the response is re-verification and an appended erratum.” | mined; actual gate re-anchor authority, not the omarchy-specific baseline |
| S045 (new, supersedes S030) | https://wiki.hypr.land/Configuring/Basics/Window-Rules/; Latest git, modified 2026-08-26 | Introductory Note: “Since Hyprland 0.55, hyprlang is deprecated in favor of lua.” | rejected duplicate-admission correction; same page/overlapping current syntax, not new knowledge |
| S046 (new) | https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c; tag 1.3.0 @ d01edd68961ca01779dcb96afe56c2d99ff79067 | :2744, colour-manager output query: `wp_color_manager_v1_get_output(` | mined after AttackCoverage A1; upstream diagnostic-client code performs bindings/detail queries; retained headers are not the whole probe execution |

### Registry mutations — old → new

| row | field | old | new | reason |
|---|---|---|---|---|
| S005 | status | queued | mined | U4 now cites the reopened, revision-anchored phase source |
| S005 | used-by | — | corpus/knowledge/wayland-protocol-boundaries-r13.md | source-to-entry reciprocal join |
| S017 | used-by | corpus/knowledge/window-rule-effects-getprop.md, corpus/knowledge/hyprland-config-era-r12.md | corpus/knowledge/window-rule-effects-getprop.md, corpus/knowledge/hyprland-config-era-r12.md, corpus/lessons/round-13.md | reopened source and duplicate lesson |

No other existing status/recheck/used-by cell changes. Original opened dates, tiers, anchors and teaches cells remain untouched. S006 stays queued historical metadata; S042 supersedes its deficient anchor. S030 stays rejected historical metadata; S045 makes its rejection reason/flip explicit. The old “supersedes not recognized” census rationale is corrected in the new search-log note, not silently deleted.

### Advisory review and outside spot-check

One validated 32-seat authoring wave; L1 is the canonical planner, PlanningWalk is a connector-routed bounded data walk. Seat reports under `.ufo/waves/round-13/w1/` are advice, not independent promotion clearance. AttackClaims' baseline-overstatement concern is adopted: report overall failing runs separately from named-set diagnostics. ReviewCensus' toggle-glob limit and Safety's client-binding/data-fence caveats are retained.

**Outside spot-check/admission: pending.** The parent orchestrator explicitly schedules a fresh non-author closure only after the pushed lane and landed report, including source reopens and at least one admit and one reject. This round does not wait for or fabricate that verdict. SHONEN stays four author assertions.

Adopted AttackCoverage A1/A2: the U4 note now distinguishes diagnostic
execution (bindings and detail queries in S046) from retained evidence
(registry headers in S041). Its three-facet table is checked alongside
the revision-bound source join; four provenance lines alone do not count
as the U4 body. Core XML digest and main-versus-master website branch are
explicit. S041's added session_binding is a later, non-atomic correlation,
not a fabricated simultaneous capture.

## Exercised verification (L1, after all seats finished)

- `evidence/before.txt`: revision-bound baseline is U1–U3 (3/7),
  navigation 26/26, complete named-set diagnostics 0/4, but overall
  failing runs already 3/4.
- `evidence/gate-selftest.txt`: 310/310, exit 0.
- `evidence/gate-file-plane.txt`: 29 PASS, 0 FAIL, 0 UNKNOWN, exit 0;
  live rows skipped, boundary hash equal before/after this run.
- `evidence/regression-recut.txt`: original spec preserved, 10/10
  KILLED and restore OK; `evidence/covering-mutants.txt`: new 8/8 KILLED,
  restore OK, no pin-only masking in the derived target.
- `evidence/frozen-regression.txt`: both input digests verified first,
  historical table match 10/10, `frozen_match`, exit 0;
  `frozen-selftest-corrected.txt`: 12/12, exit 0.
- `evidence/collision-selftest.txt`: 25/25; actual historical bad admit
  exits 1 and names S017/S030 (`collision-red-corrected.txt`);
  current registry exits 0 (`collision-green-corrected.txt`).
  L1's initial positional-argument attempts were CLI misuse (argparse 2),
  not counted as rejection evidence; the actual option is `--registry`.
- `evidence/census-after.txt`: required maintained census exit 0, with
  W04 warnings for S030, S042 and S045, explicitly retained as historical
  or superseding same-URL records.
- `evidence/globals-recheck.txt`: missing WAYLAND_DISPLAY correctly
  yielded UNKNOWN; `globals-recheck-bound.txt` supplies the prior
  correlated socket explicitly and reproduces 72 objects / 71 interfaces
  and digest `9569d02f…`, exit 0. No raw output persisted.

All shortened evidence paths in this section are under
`.ufo/waves/round-13/`. Final content-revision measurement and commit
binding live in SCORECARD and the appended LOG closure entry.
