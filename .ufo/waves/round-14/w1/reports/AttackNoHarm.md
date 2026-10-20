# AttackNoHarm — rendered report (round 14 / w1)

**Seat:** critic, leaf, read-only. **Axes:** coverage, operability. Nothing was executed (no gate,
selftest, mutants or counter), so every kill or survival below is predicted `[INFERENCE]`.
Full findings: `.ufo/waves/round-14/w1/AttackNoHarm.md`.

**Reviewed:** gate working tree sha256 `0a2bf860e713…6948` (GateImplement mid-flight, +162/−11 over
committed `037b05dc…6569`).

**Upstream bound:** Hyprland v0.56.2 at `efb50993780079460b0cbed1363e2166a2de1d9f` (2026-08-05),
`src/config/legacy/ConfigManager.cpp` L1843-1849. Quote: "source= skipping directory {}" … `continue;`.
This tag matches the installed hyprland 0.56.2-2. Admitted as a wording bound. Flip if upstream
starts making directory matches config errors.

## Verdict: no harm; four gauge gaps to fix before C2 is claimed as measured

Preserved:
- The `sources_resolve` row id and its byte-identical PASS text.
- The `missing:`/`extra:` naming, the include_graph order walk, glob ≥1-match semantics, and the
  `unresolved:` class for absent and dangling direct targets.
- The 29-row denominator, the read-only fence, and the live PASS (all 17 direct targets and both
  toggle matches are regular files, by read-only `stat`).
- P3, P4, D7, RT1 and RT2 each still occur exactly once in the derived target.
- N9–N12 sit outside the excised R8 block. PIN/SPEC are untouched and the re-cut is owed to L1, as
  the gate documents.
- N12 is labeled a preservation control, not new detection.

| # | Counterexample | Axis | Smallest correction |
|---|---|---|---|
| F1 | An over-refusing resolver emits `non-regular: …/dir.conf …/window-no-gaps.conf`. The N11 not-has check (:1246) never matches, and `measure.py:240-243` never checks the regular sibling, so C2 still scores 3/3 | operability | Row-scoped absence of `window-no-gaps.conf` in N11 (or a dir name that sorts after it). Add `'window-no-gaps.conf' not in src_detail` to the measure mixed case |
| F2 | Mutant `[ -e "$x" ]`→`true` (:2572) relabels absent targets `non-regular:`. N4 only checks a substring, so the mutant survives | operability | Add to N4: `sources_resolve FAIL "unresolved: ~/.config/hypr/gkeep.conf"` |
| F3 | Mutants on the dangling-match arm (:2566) and the zero-match arm (:2562) survive; neither has a fixture | coverage (claims) | One fixture each, or mark both unexercised |
| F4 | "Link to file passes / link to dir refused" (:40-42, :2532) has no fixture and no live instance. The mutant `-f && ! -L` survives | coverage (claims) | Add a windows.conf→regular-file symlink fixture expecting PASS, or downgrade the wording |
| F5 | Hyprland skips directory and non-regular matches with a WARN and no config error, so `configerrors` stays empty | false-provenance guard | Prose must say "refuses what Hyprland silently skips", never "Hyprland rejects" |
| F6 | A `\n` in a regular filename makes `mapfile` split it: a false `non-regular:` plus a CWD-dependent fragment (the old code passed) | operability (exotic) | Record as a limit, or classify non-`-e`/non-`-L` fragments as `unresolved:` |

**Hand-off checks (for L1):**
- `--selftest` and `--no-live`.
- The re-cut.
- A sweep of `regular-target.spec` plus the F2–F4 mutants against the derived target.
- A re-sweep of `round-13/covering.spec`.

Tools installed/updated: none. The read-only scratch clone `/tmp/hl-src-ahn` has been removed.
