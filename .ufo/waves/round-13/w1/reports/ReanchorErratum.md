# ReanchorErratum — round-13 seat report

Seat `MadoR13.ReanchorErratum` · wave `mado-r13-w1` · 2026-10-20 · axes: coverage / operability.
Assignment: draft an append-only erratum correcting round 12's wrong gate re-anchor citation, preserving
the old corpus entry; no edits to existing knowledge entries.

Axis result: **operability improved** — the gate re-anchor now resolves to the rule that actually governs
it (`gate-standing-use.md` §5 rule 4), and every in-repo mention of the wrong citation is named with its
disposition. **Coverage neutral** — this seat adds no knowledge row, no `covers:`, and no U4 movement; the
exact-set census milestone is untouched. No harm: no measured value, pin, exemption or shared file moved.

## Deliverables (the only files written by this seat)

| Path | Content | Measured 2026-10-20 |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ReanchorErratum.md` | draft + exact append block | 51 L; append block = 8 L / 3,404 B / sha256 `62a3a9e033e8b4dc480570d6067f50ff2f650dc6ad6d51fe13101d59282b7e37` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/ReanchorErratum.md` | this report | — |

Target preserved, not touched: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md`
at 149 L / 18,289 B / sha256 `a9c6f78b3a50a5688bd452eb935316ee8244fe37fc8628be49c58592f2ffa1b1`
(repo HEAD `7dcb785`, observed 2026-10-20).

## F1 — the wrong re-anchor citation (corrected by the draft)

- `corpus/knowledge/config-drift-r12.md:18`: “The report follows the append-only re-anchor protocol in
  `omarchy-drift-watch.md:284-287`.” The `source:` row at `:3` repeats S015 / lines 284-287 as the entry's
  protocol provenance.
- That protocol scopes itself to the omarchy note's own baseline, `omarchy-drift-watch.md:284-287`:
  “Re-anchor protocol: a MOVED pin is reported first, never smoothed. Changing the baseline (constants in
  §6, table in §2) requires an appended erratum …”. It governs that note's §6 constants and §2 table — not
  `EXPECT`/`LOCAL` in `tools/mado-verify.sh`.
- The governing rule for the gate pin is `gate-standing-use.md` §5 rule 4 at `:222-226`: “Pins are never
  edited to match reality. A MOVED pin reports itself … the response is re-verification and an appended
  erratum”, reinforced by §0 rule 3 at `:34-38` (“A moved pin is *reported first* — the response is
  re-verification plus an appended erratum, never a silent pin update”).
- The defect is already routed: `.ufo/evidence/round-12/l2-reviewer.md:36` diagnoses the wrong instrument;
  `corpus/lessons/round-12.md:105` (R12-b) records it, and the same file's correction at `:109-112` routes
  the citation fix to round 13. `plans/round-12.plan.md:38` had already cited rule 4 for this edit — the
  landed entry dropped it, so the plan is not the defective artifact.
- The draft's append supersedes `:3`/`:18` for future reading while leaving both lines byte-identical:
  S015 remains valid provenance for the append-only *form* (old→new values, reason, re-measure command),
  and remains the governing protocol only for `omarchy-drift-watch.md`'s own §6/§2 baseline.
- Round-13 gate side is already consistent in the working tree: the comment directly above
  `declare -a EXPECT` now says “that erratum cited the drift note's re-anchor protocol, which does not
  govern a gate EXPECT” and names §5 rule 4 (`tools/mado-verify.sh:2297-2300`, observed 2026-10-20 while
  the file was mid-flight under `MadoR13.GateImplement`; anchor by text, not line).

Mentions swept 2026-10-20 with
`grep -rn -E '284-287|re-anchor protocol|re-anchor$' corpus SCORECARD.md plans tools .ufo/evidence/round-12`
(exactly 10 hits):

| Mention | Disposition |
|---|---|
| `corpus/knowledge/config-drift-r12.md:3,18` | corrected by the draft's append; bytes preserved |
| `SCORECARD.md:258-259` (criterion C2, `:256-259`) | historical round-12 pre-registration (“gate baseline erratum per `omarchy-drift-watch.md` re-anchor protocol”); superseded by the append, retained as what was registered, not rewritten |
| `corpus/SOURCES.md:26` (S015 row) | row itself is accurate for the omarchy note's baseline; `used-by` stays method-only. `:57` (“then the gate erratum that applies it”) carries the over-broad reading and is named in the append |
| `corpus/lessons/round-12.md:105,110` | R12-b + its routed correction; the append is the landing pointer |
| `plans/round-12.plan.md:38` | already cited rule 4; no correction needed |
| `tools/mado-verify.sh:2297` | round-13 gate clause already carries the rule 4 citation; single-writer file, untouched |
| `.ufo/evidence/round-12/l2-critic.md:9` | repeats the wrong requirement in a historical evidence record; retained unchanged as data |
| `.ufo/evidence/round-12/l2-reviewer.md:36` | the diagnosis itself; no correction needed |

## F2 — adjacent citation-range defect (found, deliberately not in this append)

`corpus/knowledge/config-drift-r12.md:3` gives S013 as `install.sh:21-36,60-82,88-90`, but the entry body
cites `install.sh:21-36` (Hypr copy/append), `:42-68` (Waybar module insert), `:76-82` (CSS append) and
`:88-90` (reload/configerrors). Re-opened read-only at gkeep `HEAD` `133b867` (commit date 2026-10-18;
`sha256sum install.sh` = `git show HEAD:install.sh | sha256sum` = `f17617de4060b3b18e7aa17a332cb732bd557dd08bf430238ba92de7f5b7db26`):

- `:21-36` — hypr source copy + include append (header range matches body).
- `:42-68` — Waybar `custom/gkeep` insertion (`:42` “if '\"custom/gkeep\"' not in text:”); the header's
  `60-82` starts after this block begins and omits `:42-59`.
- `:76-82` — CSS append (`:78` “if \"#custom-gkeep\" not in style:”).
- `:88-90` — `hyprctl reload` + `configerrors`; `:93-94` also runs `omarchy restart waybar` (uncited).

The header's `60-82` is inconsistent with the body; a faithful shorthand would be `42-82` (or
`42-68,76-82`). Not folded into this erratum: the assigned correction is single-subject (the re-anchor
protocol citation), and adding an S013 range change would also touch the `source:` row's provenance claim.
Recommended owner: L1 routes it as a separate append or an S013 registry-row revision next round.
Flip: if `60-82` is shown to be an intentional coarse span, state that intent in the source row — the
measured block boundaries still do not support it.

## Source opens (contract-compliant; no external URL opened)

All sources are in-repo or operator-project local files; no network source was opened this seat.

| Source (absolute path) | Access | Revision | Tier | Exact ≤25-word quote + location | Admission | Flip |
|---|---|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md` | 2026-10-20 | 149 L / 18,289 B / sha `a9c6f78b…92f2ffa1b1`; repo HEAD `7dcb785` | A (own-work) | “The report follows the append-only re-anchor protocol in `omarchy-drift-watch.md:284-287`.” — `:18` | admitted: the defective citation being corrected | if `:18` is rewritten (append-only) or the protocol scope changes |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/omarchy-drift-watch.md` | 2026-10-20 | 287 L / sha `49f5a9a1…c9a6a1` (unchanged since the round-8 pin) | A (own-work) | “Changing the baseline (constants in §6, table in §2)” — `:284-285` | admitted: proves the protocol's note-local scope | if `:284-287` is edited to name gate lists |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` | 2026-10-20 | 361 L / sha `aaa2e625…894d01a9` (the LOG-held pin) | A (own-work) | “Pins are never edited to match reality. A MOVED pin reports itself” — `:222-223`; “the response is re-verification and an appended erratum” — `:223-224` | admitted: the governing rule | if rule 4 is removed, renumbered or re-scoped |
| `/home/vgpnk/Projects/shokunin/PROTOCOL.md` | 2026-10-20 | 533 L / sha `886e459b…d4411a`; fleet working copy | A (fleet standard) | “A falsified claim in an append-only file gets a named correction entry in the lane's next round” — `:366-367`; “Corrections sweep every mention.” — `:363` | admitted: the correction mechanism and sweep duty | if the clause is removed |
| `/home/vgpnk/Projects/gkeep/install.sh` | 2026-10-20 | HEAD `133b867`, 2026-10-18; worktree sha = `HEAD:install.sh` = `f17617de…b7db26` | A (code) | “if '\"custom/gkeep\"' not in text:” — `:42` | admitted only for F2; rejected from this append (single-subject scope) | if the header range is shown intentional |

Secondary anchors (mentions, not claim sources): `SCORECARD.md` sha `23641363…d188bd81`;
`corpus/SOURCES.md` sha `9b175fa9…40e07e23`; `corpus/lessons/round-12.md` sha `2fa66f4d…280d8654`;
`plans/round-12.plan.md` sha `e4414f1a…941a4bf8`; `.ufo/evidence/round-12/l2-reviewer.md` sha
`6c44f84c…c2a0a166`; `.ufo/evidence/round-12/l2-critic.md` sha `251cd53d…03b66b8f`;
`tools/mado-verify.sh` sha `240f5091…2337026d` (mid-flight, implementation-owned).

## Verification the parent should run after applying (not run by this seat)

From `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
# 1. exact block identity (pre-apply)
awk '/^````markdown$/{f=1;next} /^````$/{f=0} f' .ufo/waves/round-13/w1/ReanchorErratum.md | sha256sum
# expect 62a3a9e033e8b4dc480570d6067f50ff2f650dc6ad6d51fe13101d59282b7e37

# 2. append-only application
awk '/^````markdown$/{f=1;next} /^````$/{f=0} f' .ufo/waves/round-13/w1/ReanchorErratum.md \
  >> corpus/knowledge/config-drift-r12.md

# 3. preservation + block landed
head -n 149 corpus/knowledge/config-drift-r12.md | sha256sum   # expect a9c6f78b…92f2ffa1b1
tail -n 8   corpus/knowledge/config-drift-r12.md | sha256sum   # expect 62a3a9e0…282b7e37
```

No build, test, lint, formatter or smoke run was executed; no tool was installed or upgraded.

## Risks and blockers

- No blocker. The one moving target is `tools/mado-verify.sh`, which `MadoR13.GateImplement` is editing;
  the draft anchors that fact by comment text and `declare -a EXPECT`, not by line number.
- `SCORECARD.md` and `corpus/SOURCES.md` mentions are historical/shared and were not edited; the erratum
  defines how to read them, which is the append-only correction route.
- The append's re-measure anchors (`:222-226`, `:34-38`, `:284-287`) are line-based; they stay valid while
  `gate-standing-use.md` (`aaa2e625…`) and `omarchy-drift-watch.md` (`49f5a9a1…`) remain at the digests above.
  If either digest moves, re-anchor those two ranges before applying.
