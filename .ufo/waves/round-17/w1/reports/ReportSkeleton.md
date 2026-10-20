# ReportSkeleton — round 17 (mado-r17-w1), scoped findings

## Behavior

Drafted the fleet round-report skeleton at `.ufo/waves/round-17/drafts/ReportSkeleton.md` (placeholders only). Sections, in order: Work performed; Landed changes; Before → after measurements; Sources & frontier; Trend verdicts; SHONEN; Stale-lane; Tool installs; Wave seat counts, role mix, dead seats; Misroot sweep; L0. Shape taken from `.ufo/reports/round-16/mado.md` (Work performed, Landed changes, Before→after table, Sources & frontier, Trend verdicts, SHONEN, Stale-lane, Open L0) and the SHONEN checklist in `SHONEN.md` (four boxes, `[~]`/`[x]`).

No product, corpus, registry, or lesson file was edited. Only two files were written: the draft above and this report.

## Gates

No gate, test, build, census, or measurement was executed. Every observation below comes from a read-only file view (`read`, `glob`, `grep`) or a `read ?q=` jq filter over the wave's own registry copy.

Host constraints were honored. No pacman, yay, paru, sudo, systemctl, hyprctl, omarchy-*, live probe, or package query ran. The lane was not touched with git or jj. No agent was messaged and no subagent was dispatched.

## Touched surfaces

- Written: `mado-shokunin/.ufo/waves/round-17/drafts/ReportSkeleton.md`
- Written: `mado-shokunin/.ufo/waves/round-17/w1/reports/ReportSkeleton.md` (this file)
- Read only: `SHONEN.md`, `.ufo/reports/round-16/mado.md`, `corpus/lessons/round-16-verifier-spotcheck.md`, `corpus/SOURCES.md`, `.ufo/waves/round-17/w1/dispatch.json`, `.ufo/waves/round-17/w1/reports/swarm-registry.json`, fleet `.ufo/` listings, fleet `.ufo/l0-questions.md`

## Wave census (observed)

Source: `.ufo/waves/round-17/w1/reports/swarm-registry.json`, the populated copy. The dispatch's own `registry.members` copy in `w1/dispatch.json` has `agentId: null` for every member; the reports-dir copy has an id for all 70.

- Members: **70** (dispatch `counts`: spawn 70, resume 0, total 70)
- agentIds recorded: **70/70** in the reports-dir registry
- Role mix: scout 22; executor 11; reviewer 10; scribe 9; connector 8; revenger 4; critic 4; sentinel 2. Total 70.
- Seat reports present in `w1/reports/` at the time of reading: **0** (only the registry file). Wave reports were not yet written, so dead seats cannot be counted yet. Dead seats: **[UNK]**, to be filled by L1 at integration.
- Observation: `w1/reports/swarm-registry.json` has mode `-rw-------`, while sibling directories are `644`. This is a permission-model difference, not a fault.
- The fleet-wide L0 file records earlier dead-seat and routing precedent in another lane (`kaidoku`, round 16, L0 lines 56–57). It is not this lane's wave and is cited only as precedent.

## Misroot sweep (observed)

- Fleet `.ufo/waves/round-17/` does not exist. Nothing mado-r17 was written under the fleet root.
- Fleet `.ufo/reports/round-17/` holds `kotodama.md`, `kake.md`, `kasegi.md`, `kotoba.md`, `kumitate.md`, `kagi.md`. None is a mado report.
- Fleet `.ufo/prompts/mado-round-17.md` exists. This is the prompt, not a report or misroot.
- Lane-root `.ufo/waves/round-17/` holds `gen_w1.py` (dispatch generator), `drafts/` (empty at reading time, now holding this draft), `evidence/census-start.txt`, `w1/`. Lane-relative placement is correct.
- Verdict at time of reading: **no misroot found**. The sweep covers only the paths listed above; it is not a full-filesystem proof.

## L0 (observed, not appended)

Existing fleet L0 lines in `.ufo/l0-questions.md` that bear on this round, all owned by their lanes or the operator. This skeleton adds no L0 line, to avoid duplicates:

- L54 `hyaku-orchestrator | 2026-10-20 | HOST PARTIAL UPGRADE during mado r15`. Still the controlling host-recovery entry. The round-17 pacman pause is stated in the context and is not a new L0.
- L55 `tsukuroi | round-15 | Host recovery and tooling-policy decision`. Requests a host-wide pacman pause until an operator-owned recovery plan clears.
- L56–57 `kaidoku | round-16`. Dead-seat and routing precedent in another lane.

## Stale-lane

The lane's git or jj state was **not** checked, by instruction: no git or jj commands ran in the lane. Round-17 baseline `27cd06f` and pre-registration `0175f13` are taken from the context and are not verified. Lane HEAD for round 17: **[UNK]**.

## Tool installs

None by this seat. No installation or update was attempted, and none is evidenced in the files read. The operator tooling directive names `sudo pacman -S` as a channel; it is paused host-wide and was not used.

## Out-of-scope items

- `SHONEN.md` is unchanged. Its four boxes are referenced only for the draft's shape; no box was judged.
- No claim, score, source count, or verdict was computed. Those are L1's integration job, and the draft holds them as placeholders.
- The seat-report-level data (seat outcomes, falsification results, tripwire output) is not in this seat's scope and was not read.

## Findings

1. The skeleton is complete, in the required section order, and placeholder-only.
2. The wave holds 70 registered members with 70 agent ids; role mix is as listed above.
3. No seat report exists in `w1/reports/` at the reading time, so the dead-seat line stays `[UNK]` until integration.
4. No misroot was found in the fleet sweep.
5. The existing L0 host-recovery line is still the controlling entry; no new L0 was added.

## Artifact paths

- `mado-shokunin/.ufo/waves/round-17/drafts/ReportSkeleton.md`
- `mado-shokunin/.ufo/waves/round-17/w1/reports/ReportSkeleton.md`
