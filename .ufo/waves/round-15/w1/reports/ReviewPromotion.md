# ReviewPromotion — round 15 (mado-r15-w1), U6 integration risk

Advisory reviewer output. Not admission, not promotion, not a SHONEN mark, not a discernment verdict. Lane-dispatched seat, so it is lane evidence by the rules cited below.

Scope: adversarial review of the risk that lane-owned seats supply nonauthor SHONEN or discernment agreement for the U6 input-debugging route (claim C1, coverage U1–U5 5/7 → U1–U6 6/7).

Tooling: none installed or updated. Read-only file inspection only. No git, tests, gates, builds, live probes, input reads, or credential/agent.db access.

## Verdict

Lane seats cannot supply the nonauthor agreement. The round may still claim the structural coverage count, but only as lane-asserted evidence until a non-lane closure lands. Discernment cannot be scored `improved` or `unprovable-but-better` this round from lane output. SHONEN stays four `[~]`.

## Findings by severity

1. **High — lane seats are the lane.** Canonical rules: a subagent the lane dispatched is still the lane; `[x]` needs a named non-author verifier; a lane-dispatched seat stays `[~]`.
   - `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:42-46` (`A subagent the lane dispatched is still the lane`); `:48-50` (exploratory `unprovable-but-better` admitted only via a named non-author reviewer).
   - `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:63-68` (`only a non-author <id> may write [x]`; `[x]` without a named non-author is author attestation counting as `[~]`).
   - `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:18` (criterion 12: lane-dispatched seat remains `[~]`).
   - `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:39-42` (L2s are the authoring lane; none supply promotion authority).
   - Wave seat: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/spec.json:202-205` (ReviewPromotion, role reviewer, inside the mado-r15 wave). Its own role says a verdict is a recommendation, never an admission.

2. **High — round-14 precedent is not a template for round 15 as written.**
   - The round-14 discernment record (`improved`) lives in a separate closure file, `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:3-5, 161-165`. The round-14 lesson still says the spot-check is pending: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14.md:104-107, 211-214`. LEARNING.md:44-46 requires the agree/disagree record in the round's lesson, so the two files disagree.
   - The closure says two "fresh read-only reviewer seats" audited the work (`round-14-verifier-spotcheck.md:45`) but does not name who dispatched them. If the lane dispatched them, the closure's independence rests on lane seats. This is `[UNK]` in the record and must be named in round 15.
   - The closure's own adjudication is the only non-lane content (`:5`: "did not author the round … or alter lane-authored records or SHONEN marks"). Treat that as the model, not the reviewer seats' output.

3. **High — discernment has no round-15 sample.** Canonical sample: at least one admit and one reject, drawn from this round's gate decisions, with agree/disagree and reasons (LEARNING.md:42-46). The round-14 closure sampled round-14 items. Reusing it for round 15 is invalid.
   - Current SCORECARD discernment row is `unprovable-but-better` with the outside spot-check absent (`SCORECARD.md:133-134`). Carrying that forward without a new sample is not admitted.

4. **Medium — U6 coverage is blocked on sourcing, not on seats.** The counter requires a `mined` row, a single `covers: U6`, and a reciprocal `used-by` join (`SCORECARD.md:237`; round-14 recipe `round-14-verifier-spotcheck.md:49-78`).
   - Candidate rows are still `queued` and cannot be sole support: S007 libinput tools (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:19`), S008 Wayland book high-level design (`:20`), S009 architecture (`:21`). `queued` rows are "not citable as sole support" (`SOURCES.md:115`; S006/S008/S009/S010 owed anchors).
   - S007 also lacks a source-repository revision (access date only), the same gap that `SOURCES.md:115` names. A mined row needs a revision-bound anchor or a superseding row with the owning commit.
   - The U6 note's lane-side count is structural only. Semantic accuracy needs a non-lane reopen of the exact anchors, as the round-14 closure did (`round-14-verifier-spotcheck.md:88-104, 132`).

5. **Medium — input boundary.** S007 says most libinput tools need root and `/dev/input/event*` (`SOURCES.md:19`). The round contract forbids input reading, recording or replay (`spec.json` contract text). U6 must stay documentary. Any sentence that states observed libinput, delivery, IME or kernel behavior is outside scope and unsupported. Unexercised facets must be marked `[UNK]`, consistent with `corpus/knowledge/wayland-protocol-boundaries-r13.md:8`.

6. **Low — U6 cannot move SHONEN boxes.** Box 1 needs decision tables and error patterns, box 2 an executed end-to-end task, box 3 no-oral-context instructions, box 4 PROVINCE accuracy (`/home/vgpnk/Projects/shokunin/mado-shokunin/SHONEN.md:5-12`). A coverage note on input debugging provides none of that. Any round-15 `[x]` is out of scope.

## Acceptance conditions (all must hold to credit U6 and any discernment move)

- **A1 — lane-asserted coverage.** The lane may record `U1–U6 6/7` using the structural counter, labelled lane-asserted and pending non-author closure, as round 14 did. The counter must print exact command output.
- **A2 — non-lane closure identity.** A closure file names a verifier outside the MadoR15 roster and not committed as `mado-shokunin <mado@shokunin.local>`. It names the dispatcher of every reviewer seat it cites. It reopens the new U6 anchors itself (sha256 or revision) rather than copying lane seat rows.
- **A3 — round-15 sample.** At least one admit and one reject drawn from round-15 `corpus/lessons/round-15.md ## Gate`, each with `agree` or `disagree` and reasons, recorded in that lesson. The lesson may only point to the closure verbatim. It must not restate a lane seat's "agree" as the record.
- **A4 — verdict selection.** Discernment may be `improved` only if the closure agrees on all sampled items, or any disagreement becomes a grounded QUALITY criterion citing a lesson (LEARNING.md:35). `unprovable-but-better` only if the closure names the change better with reasons. Otherwise `unchanged`, stated as "no non-author sample this round."
- **A5 — SHONEN unchanged.** `SHONEN.md` retains four `[~]` unless a non-lane closure checks a box with evidence in that box's own scope. U6 evidence is not in any box's scope, so the expected diff is empty.
- **A6 — counter join.** The U6 note carries exactly one `covers: U6`, opens with `source:` naming at least one `mined` row with a revision-bound anchor, and that row's `used-by` lists the note path. Queued rows (S007/S008/S009 unless mined) are not sole support.
- **A7 — input boundary.** The note marks delivery/IME/kernel facets `[UNK]`, makes no observed-host input claim, and the lane transcript shows no `/dev/input` or libinput execution.

## Rejection conditions (any one rejects the U6 credit or discernment move)

- **R1.** Any `[x]` in `SHONEN.md` or any "checked" box whose verifier is a MadoR15 seat (ReviewPromotion, ReviewSeat, AttackX, ReviewX, etc.).
- **R2.** A discernment verdict of `improved` or `unprovable-but-better` whose only agreement is lane seat output, including any reviewer or source-bar "agree" row (`.ufo/waves/round-14/w1/reports/ReviewSourceBar.md:33-36` is proposed rows for the integrator, not a verdict).
- **R3.** A closure whose reviewer seats have no named dispatcher, or whose dispatcher is the lane.
- **R4.** A discernment sample drawn from round-14 or earlier items to support round 15.
- **R5.** A sampled disagreement left unlearned, or a new QUALITY criterion with no lesson behind it (LEARNING.md:35).
- **R6.** U6 claimed `mined` or counted while its only candidate rows are `queued` (S007/S008/S009), or a `mined` row whose used-by does not include the note.
- **R7.** Any statement of observed input delivery, IME, libinput or kernel behavior, or any input capture command.
- **R8.** Any SHONEN checkbox changed in round 15 without a non-lane closure whose evidence is in that box's scope.

## Evidence pointers

- `/home/vgpnk/.omp/agent/RULES.md` (tooling directive, read first)
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:35, 42-50`
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:63-68`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SHONEN.md:5-12`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:39-42, 133-134, 237`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:18`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:19-21, 70, 82, 115`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14.md:104-107, 211-214`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:3-5, 45, 49-78, 88-104, 132, 161-165, 175`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/spec.json:202-205`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/ReviewSourceBar.md:33-36`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md:8`

## Residual risk and verification gaps

- Round-15 lesson `## Gate` and any U6 note do not exist yet. Every acceptance condition above must be re-checked against the landed bytes.
- The round-14 closure's reviewer-seat dispatcher is `[UNK]`; I did not verify it, and the closure's own text does not name it.
- I did not run the counter, the closure's Python recipe, or any git command. Structural counts above are taken from prior recorded outputs and the rubric text, not re-measured.
- The S007 revision gap is inferred from its anchor text. It is not confirmed against a fetched revision.
- Round-15 seat outputs (ReviewSeat, AttackX, etc.) were not read. This review does not cover them.
- No check of the R14-V1 ancillary receipt correction, which is out of this assignment's scope.
