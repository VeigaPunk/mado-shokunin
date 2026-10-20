# ReanchorErratum — round-13 draft (append-only correction)

Seat: `MadoR13.ReanchorErratum` · wave `mado-r13-w1` · 2026-10-20.
Target document (not edited by this seat): `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md`.
Current bytes observed 2026-10-20 at repo HEAD `7dcb785`: 149 lines / 18,289 bytes / sha256 `a9c6f78b3a50a5688bd452eb935316ee8244fe37fc8628be49c58592f2ffa1b1`; file ends with `\n`.

Defect being corrected: `corpus/knowledge/config-drift-r12.md:3` and `:18` cite
`omarchy-drift-watch.md:284-287` as the report's re-anchor protocol, but that protocol scopes itself to
the omarchy note's own baseline (`constants in §6, table in §2`), not to the gate's `EXPECT`/`LOCAL`
lists in `tools/mado-verify.sh`. Routed as `corpus/lessons/round-12.md:105` (R12-b) and corrected in
round 13. The governing rule for a moved gate pin is `gate-standing-use.md` §5 rule 4 (`:222-226`),
reinforced by §0 rule 3 (`:34-38`).

The block below is the exact content to append at EOF of the target document. It begins with one
blank line; nothing above it changes. Do not reflow, renumber or edit the existing body or its
`## Errata (round 12, post-integration)` section.

<!-- APPEND-BEGIN -->
````markdown

## Erratum (round 13, append-only) — R12-b gate re-anchor citation

- **Corrected citation.** `:3` and `:18` above cite `omarchy-drift-watch.md:284-287` as this report's re-anchor protocol. That protocol scopes itself to “the baseline (constants in §6, table in §2)” of `omarchy-drift-watch.md` — its own constants and table, not the gate's `EXPECT`/`LOCAL` lists in `tools/mado-verify.sh`. The gate re-anchor recorded in “Gate re-anchor and residual blind spots” is governed by `gate-standing-use.md` §5 rule 4 (`:222-226`) — “Pins are never edited to match reality. A MOVED pin reports itself” … “the response is re-verification and an appended erratum” — reinforced by §0 rule 3 (`:34-38`). `plans/round-12.plan.md:38` already cited rule 4 for this edit; the landed entry dropped it (`.ufo/evidence/round-12/l2-reviewer.md:36`; `corpus/lessons/round-12.md:105` R12-b).
- **Preserved, not rewritten.** The measurements, the gate facts at `:84-90`, and the `:3`/`:18` bytes above are unchanged; this section is the named correction entry required by `PROTOCOL.md` §“Evidence standard” (“A falsified claim in an append-only file gets a named correction entry in the lane's next round”), not a rewrite. Read `:3`/`:18` through this erratum: S015's lines 284-287 remain valid provenance for the append-only *form* (old→new values, reason, re-measure command), and they remain the governing protocol only for `omarchy-drift-watch.md`'s own §6/§2 baseline.
- **Mentions swept (2026-10-20; `grep -rn -E '284-287|re-anchor protocol|re-anchor$' corpus SCORECARD.md plans tools .ufo/evidence/round-12`).** `SCORECARD.md:256-259` registered “gate baseline erratum per `omarchy-drift-watch.md` re-anchor protocol” (quote at `:258-259`); it is the historical pre-registration, superseded by this erratum and retained as what was registered. `corpus/SOURCES.md:26` (S015 row) and `:57` (“then the gate erratum that applies it”) carry the same over-broad reading: S014 applied the lane's append-only discipline under `gate-standing-use.md` §5 rule 4, not S015's note-local protocol. `corpus/lessons/round-12.md:105` and its correction at `:109-112` already name this defect and route the citation fix to this round; this append is its landing pointer. `plans/round-12.plan.md:38` already cited rule 4. The gate comment directly above `declare -a EXPECT` already records the same correction in its round-13 clause — “that erratum cited the drift note's re-anchor protocol, which does not govern a gate EXPECT” — and names §5 rule 4; that file is single-writer, so this append does not touch it. `.ufo/evidence/round-12/l2-critic.md:9` repeats the wrong requirement in the round-12 evidence record and is retained unchanged as historical data.
- **No value, pin or exemption moved.** This append changes no measured value, gate pin or named exemption; rule 4's “Exemptions are by name and counted” clause is not invoked.
- **Re-measure.** `grep -n 'omarchy-drift-watch.md' corpus/knowledge/config-drift-r12.md` → `:3` and `:18` only; `awk 'NR>=284 && NR<=287' corpus/knowledge/omarchy-drift-watch.md` → the sentence “Changing the baseline (constants in §6, table in §2)”; `awk 'NR>=222 && NR<=226' corpus/knowledge/gate-standing-use.md` → rule 4; `awk 'NR>=34 && NR<=38' corpus/knowledge/gate-standing-use.md` → §0 rule 3 — 2026-10-20.
````
<!-- APPEND-END -->

## Apply and verify (operator/integrator step, not run by this seat)

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
awk '/^````markdown$/{f=1;next} /^````$/{f=0} f' \
  .ufo/waves/round-13/w1/ReanchorErratum.md >> corpus/knowledge/config-drift-r12.md
head -n 149 corpus/knowledge/config-drift-r12.md | sha256sum   # must print a9c6f78b…92f2ffa1b1
```

The `head -n 149` digest proves the append-only property: the pre-append 149-line prefix is
byte-identical. The appended block's own digest and size are recorded in the seat report
(`.ufo/waves/round-13/w1/reports/ReanchorErratum.md`) so the applied bytes can be compared.

## Scope boundaries

- No repository file outside this draft and the seat report was written by this seat; the only other write is scratch `/tmp/reanchor-append.check` for byte verification.
- `corpus/knowledge/config-drift-r12.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/lessons/round-12.md`
  and `tools/mado-verify.sh` are untouched; the last is round-13's single-writer implementation file,
  owned by `MadoR13.GateImplement`.
- No build, test, lint, formatter or smoke run was executed, per the wave contract.
