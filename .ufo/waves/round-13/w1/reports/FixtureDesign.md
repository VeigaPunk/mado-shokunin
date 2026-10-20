# FixtureDesign — report (round 13, C2 exact-set Hypr census; closure review)

Axes: coverage, operability. Advisory: no gate edits, no tests/builds/lint/formatting run.
Full artifact: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/FixtureDesign.md`.

## Binding

- Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`.
- Baseline `ea798ad0…` (3245 L) → final `784c4e90ef25cce79773c89ef23c2396bf4dec155ddba34deb5cf22e66269081` (3458 L), 2026-10-20.
- Derived target independently reproduced with the gate's own `sed`: sha256 `87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39`, 2161 L. `PIN_MADO='538d178b…'` untouched (recut is L1's).
- Names-only host probe: 13 `~/.config/hypr/*.conf`; no contents read. No external sources opened; no URL quote table owed. Tooling: none.
- Static evidence: embedded spec 2141 B sha256 `c7ee75b9…` = `SPEC_SHA` (recorded case); clean fixture writes all 13 local confs; `EXPECT` = 18.

## Closure confirmations

- **R-4 wording fixed and verified** at `:35-37`: header now reads “judged as an exact set of
  regular files … no undeclared `*.conf` file present”, matching the `[ -f ]` census and the
  narrowed `LOCAL` comment. No remaining wording mismatch found.
- **K8 (commented-out gkeep source) needs no fixture**: verified against the extraction regex —
  a commented line is not extracted, so `got` 17 vs `EXPECT` 18 → include_graph FAIL
  `17 source lines (expected 18)` + `missing: ~/.config/hypr/gkeep.conf`; sources_resolve FAIL
  `missing:` with no `unresolved:` (file exists); local PASS. The behaviour is covered by the
  census; only a hermetic case would be added, which the bound excludes.
- **Order-swap** is recorded as residual R-3 (no dedicated case). Retained source-level proof: a
  pure permutation yields include_graph FAIL `line 11: got … want …` with **no** missing/extra
  clause (membership equal); sources_resolve and local PASS. It cannot read CLEAN.

## Residual ledger (aligned to `reports/GateImplement.md` §6)

| ID | Residual | Consequence |
|---|---|---|
| R-1 | Target-shape pinning (`[ -e ]` literal, `compgen -G` glob) | A directory named like the sole toggle yields **false CLEAN** (resolve PASS, toggle NOTE); non-glob directory targets keep the verdict red only via include_graph |
| R-2 | Duplicate source declarations | count/order FAIL but the repeated occurrence is unnamed; sources_resolve stays membership-valued and no longer claims a count |
| R-3 | Order-swap fixture | order asserted only indirectly (N2 failure direction, T3 isolation) |
| R-4 | hyprlang conditional semantics | presence FAILs the orchestrator; loaded-line semantics unmodelled, `# hyprlang noerror` over-matches by design |
| R-5 | General hyprlang grammar (`include=`, variables, nesting) | unparsed; literal source list only |
| R-6 | Source-member display | source members are single lines; `%q` only for local filenames |

Mapping from this seat's earlier numbering: duplicate → R-2; target-shape (old R-2/R-3) → R-1;
order-swap (old P1) → R-3; old header-wording R-4 is closed.

## Landed assertion matrix (verified by source read, not executed)

| Case | Mutation | Exit/verdict | include_graph | sources_resolve | local.inventory | Other |
|---|---|---|---|---|---|---|
| A | none | 0 CLEAN | PASS set exact | PASS `declared targets exist, member set exact` | PASS `13/13 … set exact` | zero FAIL/UNKNOWN |
| H | append undeclared source | 1 DIVERGED | FAIL | PASS | PASS | status-only assertion valid |
| N1 | add `$H/extra.conf` | 1 DIVERGED | PASS | PASS | FAIL `extra: extra.conf` | — |
| N2 | same-count source swap, target exists | 1 DIVERGED | FAIL `missing:`+`extra:` | FAIL `missing:`+`extra:`, no `unresolved:` | PASS | — |
| N3 | `xdph.conf` → `extra.conf` | 1 DIVERGED | PASS | PASS | FAIL `missing: xdph.conf`+`extra: extra.conf` | — |
| N4 | remove `gkeep.conf` | 1 DIVERGED | PASS | FAIL names gkeep | FAIL `missing: gkeep.conf` | — |
| N7 | append `source =` | 1 DIVERGED | FAIL `extra: ''` | FAIL `extra: ''` | PASS | no bad-subscript |
| N8 | `# hyprlang` conditional | 1 DIVERGED | PASS | PASS | PASS | orchestrator FAIL names the directive |

Out-of-bound proposals (recorded, not landed): Q1 K8 hermetic variant; Q2 second toggle (CLEAN);
Q3 only-toggle removal (`unresolved:` + toggle NOTE); Q4 dedicated order swap (R-3).

## Assertion-stability rules

1. Row id + status only; never whole-detail equality.
2. Pin only `missing:`, `extra:`, `unresolved:`, `EXPECT`-form `~` paths, and the two PASS
   signatures. Never pin `ROOT`-expanded paths or positional ordinals.
3. Every red case: `st_not_has … "MADO_VERIFY: CLEAN"` + `st_counts_agree`.
4. Isolation = untouched sibling row stays PASS.

## Syntax boundary (final)

Accepted: one `source`/line, lowercase, whitespace around `=`; `~`-rooted literal path
(whitespace-trimmed, `~`→ROOT for existence); one final-component `*.conf` glob; blank/`#` lines
except `# hyprlang…`; multiplicity one, order fixed; local regular `*.conf` (or symlink to one)
directly under `$H`. Unsupported, fail-closed: quotes, `$VAR`/env, inline comments, internal
spaces, mid-path/`?`/`[]`/brace globs, recursive includes, glob enumeration, CRLF/continuations,
case-folding, full directive grammar, `# hyprlang` (any comment whose first token is `hyprlang`),
empty `source =` (guarded, named `extra: ''`).

## Obligations for L1

- Recut `PIN_MADO` from the measured sweep (expect one pre-recut selftest failure, R10 stale pin;
  `MADO_REGRESSION: PASS` only post-recut). Do not hand-edit.
- D6 anchor stays byte-verbatim via `LOCAL+=(gkeep)`; `TABLE_MADO` expects `D6:KILLED` and the
  clean-fixture extras witness it.
- Append-only corrections: `corpus/knowledge/config-drift-r12.md:86-87`,
  `corpus/knowledge/gate-mutation-proof.md:60`, `corpus/knowledge/gate-mutation-sweep-r8.md:63`;
  record R-1/R-2/R-3 and the K8 trace in the round-13 entry.
- Run `bash tools/mado-verify.sh --selftest` once after the recut (not run here).
