# SkillRegistryDraft — round-18 report

## Behavior
Drafted replacement registry text for `SKILL.md` (no `SKILL.md` edit):

- Row A replaces `SKILL.md:562` `mado-tripwire`: kind moves `probe` to `gate`;
  adds the `--frozen .ufo/waves/round-18/frozen-tripwire` entry with exit map
  0 `frozen_match`, 1 `frozen_verdict_mismatch`, 2 `snapshot_tampered` /
  `unpinned_legacy` / `frozen_error`, other could-not-evaluate, placed beside
  the unchanged scan entry; self-test spelling adds
  `.ufo/waves/round-18/tripwire/frozen`; pinned path
  `.ufo/waves/round-18/frozen-tripwire/expected.json`.
- Row B adds five probe rows after `SKILL.md:564`: `mado-receipt-check`,
  `mado-fetch-verify`, `mado-pipe-rc-census`, `mado-measure-mutants`,
  `mado-frozen-provenance`, in the eight-column shape of `SKILL.md:548`.

Draft file: `.ufo/waves/round-18/drafts/SkillRegistryDraft.md` (8,052 bytes,
written by `write`; no digest computed).

## Gates
None run. Assignment says L1 verifies once after integration. No `|` in any cell.

## Touched surfaces
- Written: `.ufo/waves/round-18/drafts/SkillRegistryDraft.md`,
  `.ufo/waves/round-18/w1/reports/SkillRegistryDraft.md`.
- Read only: `SKILL.md:530-603`, `.ufo/waves/round-18/w1/spec.json`,
  `.ufo/waves/round-18/` directory listing.
- Not touched: `SKILL.md`, `tools/`, any other lane file. No git/jj, no
  pacman or host probe, no fetch, no tool install.

## Findings
1. Five round-18 scripts named in the drafts do not exist yet
   (`receipt-check.py`, `fetch-verify.py`, `pipe-rc-census.py`,
   `measure-mutants.py`, `frozen-provenance-check.py`), and neither does
   `.ufo/waves/round-18/tripwire/frozen` or `frozen-tripwire/`. Their exit maps
   and CLI forms are transcribed from the seat specs and are marked in
   Draft C.1 as needing reconciliation at landing.
2. `tools/mado-tripwire.py` has no `--frozen` yet (grep found none), so the
   `--frozen` entry in Row A describes the specified interface, not landed code.
3. The `mado-tripwire` self-test count for the new frozen suite is left as `N`
   until `TwFrozenSelftest` lands; no number was invented.
4. Row A's frozen entry reads only the pinned `DIR/inputs` snapshot, so the
   pin cannot be bypassed by live transcripts. This is the only behavioural
   claim in the draft that depends on the tool's implementation.

## Out of scope
- Writing `SKILL.md`, the mado-verify OM scenario (a gate change), and
  `corpus/` rows.
- Tool installs or updates: none were needed or made.

## Artifact paths
- `.ufo/waves/round-18/drafts/SkillRegistryDraft.md`
- `.ufo/waves/round-18/w1/reports/SkillRegistryDraft.md`
