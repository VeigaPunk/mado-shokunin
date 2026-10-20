# FixtureDesign — C2 exact-set Hypr census: final review, fixture contract, residual ledger

Axes: **coverage** (each in-bound false-negative has a hermetic killer) and **operability**
(red rows name both sides; row ids/status semantics stable). Advisory only — no gate edit, no
test/build/lint/formatting run by this seat.

Residual numbering is aligned to the gate owner's ledger (`reports/GateImplement.md` §6) so the
two artifacts cannot disagree. This file previously used its own R-1…R-4/P1–P4 labels; the
mapping is stated where it matters.

## 0. Binding, evidence, revision

| Item | Value |
|---|---|
| Target | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` |
| Baseline read | sha256 `ea798ad0…`, 3245 L |
| Final read | sha256 `784c4e90ef25cce79773c89ef23c2396bf4dec155ddba34deb5cf22e66269081`, 3458 L, 2026-10-20 |
| Derived target (statically reproduced with the gate's own `sed`) | sha256 `87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39`, 2161 L; `PIN_MADO` untouched by design |
| Concurrent owner | `MadoR13.GateImplement`; all anchors below are textual |
| Host probe (names only) | `~/.config/hypr/*.conf` → 13 names; contents not read |
| External sources opened | none — no URL quote table owed |
| Tool installs/updates | none |

Static checks (no gate run): embedded defect spec = 2141 B, sha256 `c7ee75b9…` = `SPEC_SHA`
(recorded tameshi case); clean fixture writes all 13 local confs including gkeep; `EXPECT` = 18.

Governing lesson: `corpus/lessons/round-12.md:25` — “A census compares expected and observed sets
and names both missing and extra members; pin module membership where it is a claim.” [OBS],
lesson row M13. Maintenance rules: `corpus/knowledge/gate-standing-use.md:199` (no widening
without a covering mutant), `:205` (pins never edited to match reality).

Planner bound accepted: **C2 = four predeclared hermetic cases + exact declaration/local
regular-file sets**; everything wider is a named residual.

## 1. Landed behaviour (final bytes)

| Landed case | Mutation | Asserted outcome |
|---|---|---|
| N1 | add `$H/extra.conf` | exit 1; local FAIL `extra: extra.conf`; include_graph PASS; sources_resolve PASS |
| N2 | swap one source line for an existing default-tree path, count equal | exit 1; include_graph FAIL `missing:` + `extra:`; sources_resolve FAIL `missing:` + `extra:`, no `unresolved:`; local PASS |
| N3 | `xdph.conf` → `extra.conf` | exit 1; local FAIL `missing: xdph.conf` + `extra: extra.conf`; include_graph PASS |
| N4 | remove `gkeep.conf` | exit 1; local FAIL `missing: gkeep.conf`; sources_resolve FAIL naming the target; include_graph PASS |
| N7 (K2) | append `source =` | exit 1 with a verdict; include_graph FAIL `extra: ''`; sources_resolve FAIL `extra: ''`; no bad-subscript |
| N8 (K1) | `# hyprlang if/endif` around a source line | exit 1; orchestrator FAIL `unsupported hyprlang directive at line N`; include_graph PASS |

Soundness points verified by source read:

- `EXPECT` 18, `LOCAL` 13 as the byte-verbatim 12-name base + `LOCAL+=(gkeep)`, so the recorded
  `@defect D6` anchor stays byte-identical; D6 now dies on the exact-set guard (observed
  `xdph.conf` becomes an extra in the clean fixture).
- Empty members are guarded in `seen`/`tseen`, and the extra loops emit `extra: ''` explicitly;
  no empty associative-key lookup remains.
- Local names are `%q`-quoted in the detail; normal names render unchanged.
- `~` expansion is explicit (`'~'* → "$ROOT${t#\~}"`), same semantics as before.
- `# hyprlang` is checked before the generic non-source check, so a conditional fails the
  orchestrator by name instead of judging an unmodellable config.
- Header wording fixed: `:35-37` now reads “judged as an exact set of regular files … no
  undeclared `*.conf` file present”, matching the `[ -f ]` census and the narrowed comment.
  (This closes the item previously reported here as R-4.)

## 2. Residual ledger (aligned with `reports/GateImplement.md` §6; not new scope)

### R-1 — Target-shape pinning (`[ -e ]` literal, `compgen -G` glob)

A directory named like a conf satisfies both checks. If the only toggle is replaced by a
directory named `window-no-gaps.conf`, the gate reads **CLEAN**: `sources_resolve` PASS via
`compgen -G`, `hypr.toggle.no_gaps` NOTE (never flips). Non-glob directory targets keep the
verdict red only through the declaration move (include_graph), while `sources_resolve` PASSes.
Fix when widened: nullglob + `[ -f ]` for glob matches, `[ -f ]` for literal targets.

### R-2 — Duplicate source declarations

A repeated declared line fails the count/order test but the duplicate occurrence is not named:
append duplicate → only `19 source lines (expected 18)`; stable-count duplicate → `missing:` for
the removed member, no clause for the repeated one. `sources_resolve` is deliberately
membership-valued and its PASS text no longer claims a count. Fix when widened: per-path counts +
`duplicate: <path> (xN)` in `include_graph`.

### R-3 — Order-swap fixture (this artifact previously labelled it P1)

A pure permutation (swap source lines 11/12) produces `include_graph` FAIL `line 11: got …
want …` with **no** `missing:`/`extra:` clause, because membership is equal; `sources_resolve`
and local PASS. Order sensitivity is therefore asserted only indirectly (N2 failure direction,
T3 isolation). No dedicated fixture per the planner bound; the source trace above is the retained
proof that a swap cannot read CLEAN.

### R-4 — hyprlang conditional semantics

Presence FAILs the orchestrator row, but which lines would actually load under a condition is
unmodelled; `# hyprlang noerror` over-matches deliberately (fail-closed).

### R-5 — General hyprlang grammar (`include=`, variables, nested conditions)

Unparsed; the gate judges only the literal `source` list. This is the declared syntax boundary,
not a defect.

### R-6 — Source-member display

Source members are single lines by construction (awk line split), so `%q` is applied only to local
filenames, which have no such guarantee. No action.

## 3. K8 trace (no fixture added, per gate owner)

Commented-out gkeep source line, file kept: the extraction regex ignores the comment, so
`got` = 17 vs `EXPECT` = 18 → `include_graph` FAIL `17 source lines (expected 18)` +
`missing: ~/.config/hypr/gkeep.conf`; `sources_resolve` FAIL `missing:` with **no** `unresolved:`
(the file exists); local PASS. Verified against the extraction/regex code, not executed. This is
behaviourally covered by the existing census; a dedicated case would not add coverage inside the
bound.

## 4. Remaining out-of-bound fixture proposals (no implementation change; L1 only)

| Case | Mutation | Expected | Value |
|---|---|---|---|
| Q1 | delete the gkeep source line, keep file (K8 variant) | as §3 | makes the K8 trace hermetic if the bound ever widens |
| Q2 | add a second toggle `*.conf` | exit 0 CLEAN; all rows PASS | expansion cardinality is not part of the declaration set |
| Q3 | remove the only toggle | exit 1; sources_resolve FAIL `unresolved:`; toggle NOTE | covers the declared no-match-glob policy |
| Q4 | swap source lines 11/12 | R-3 behaviour | the dedicated case R-3 records as not landed |

## 5. Stable assertion matrix (landed)

Legend: assert row id + status; detail assertions use only fixed tokens (`missing:`, `extra:`,
`unresolved:`), `EXPECT`-form `~` paths, and the PASS signatures (local
`13/13 active local confs, set exact`; sources `declared targets exist, member set exact` — no
count claimed). Never pin whole detail strings, `ROOT`-expanded paths, or positional ordinals.

| Case | Delta from clean A | Exit | Verdict | include_graph | sources_resolve | local.inventory | Other |
|---|---|---|---|---|---|---|---|
| A | none | 0 | CLEAN | PASS set exact | PASS member set exact | PASS 13/13 | zero FAIL/UNKNOWN; counts agree |
| H | append undeclared source | 1 | DIVERGED | FAIL | PASS | PASS | status-only assertion stays valid |
| N1 | add `$H/extra.conf` | 1 | DIVERGED | PASS | PASS | FAIL `extra: extra.conf` | — |
| N2 | same-count source swap, target exists | 1 | DIVERGED | FAIL `missing:`+`extra:` | FAIL `missing:`+`extra:`, no `unresolved:` | PASS | — |
| N3 | `xdph.conf`→`extra.conf` | 1 | DIVERGED | PASS | PASS | FAIL `missing: xdph.conf`+`extra: extra.conf` | — |
| N4 | remove `gkeep.conf` | 1 | DIVERGED | PASS | FAIL names gkeep | FAIL `missing: gkeep.conf` | — |
| N7 | append `source =` | 1 | DIVERGED | FAIL `extra: ''` | FAIL `extra: ''` | PASS | no bad-subscript |
| N8 | `# hyprlang` conditional | 1 | DIVERGED | PASS | PASS | PASS | orchestrator FAIL names the directive |

Out-of-bound cases (R-1/R-2/Q1–Q4) must not be asserted as PASS/FAIL expectations before their
implementation decision; they are recorded, not landed.

## 6. Accepted syntax vs unsupported scope

Accepted: one `source`/line, lowercase, whitespace around `=`; `~`-rooted literal path
(whitespace-trimmed, `~`→ROOT for existence); one final-component `*.conf` glob; blank/`#` lines
except `# hyprlang…`; multiplicity one in the expected state, order fixed; local regular `*.conf`
(or symlink to one) directly under `$H`, no recursion, backups excluded.

Unsupported, fail-closed: quotes, `$VAR`/env, inline comments, internal spaces,
mid-path/`?`/`[]`/brace globs, recursive includes, glob enumeration, CRLF/continuations,
case-folding, full directive grammar, `# hyprlang` (any comment whose first token is `hyprlang`),
empty `source =` (guarded, named `extra: ''`).

## 7. Obligations for L1

- `PIN_MADO='538d178b…'` is untouched; the derived target is now `87910c39…` (2161 L), statically
  reproduced. Recut from the measured sweep; expect one pre-recut selftest failure (R10 stale pin)
  and `MADO_REGRESSION: PASS` only after the recut.
- D6 keeps its recorded anchor; `TABLE_MADO` expects `D6:KILLED` and the clean-fixture extras now
  witness it.
- Append-only corrections: `corpus/knowledge/config-drift-r12.md:86-87`,
  `corpus/knowledge/gate-mutation-proof.md:60`, `corpus/knowledge/gate-mutation-sweep-r8.md:63`;
  record R-1/R-2/R-3 and the K8 trace in the round-13 entry.
- Run `bash tools/mado-verify.sh --selftest` once after the recut (not run here).

## 8. Tooling

No tool installed, upgraded, or configured.
