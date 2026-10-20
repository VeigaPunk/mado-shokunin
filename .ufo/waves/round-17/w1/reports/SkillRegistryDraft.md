# SkillRegistryDraft report — round 17 (w1)

Seat: `MadoR17.SkillRegistryDraft` (scribe, leaf member, no subagent dispatch).
Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. No commits, no git or jj mutation, no
product-file edits.

## Deliverable

- Wrote ONLY: `.ufo/waves/round-17/drafts/SkillRegistryDraft.md` (draft for L1 integration).
- Wrote this report: `.ufo/waves/round-17/w1/reports/SkillRegistryDraft.md`.
- Draft contents: two registry rows in the 8-column shape of SKILL.md lines 532-545
  (name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value
  path | write scope | owner), plus a five-line limit paragraph.
  - `mado-tripwire` (gate): entry `python3 -I tools/mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...]`;
    exit 0 clean, 1 unpermitted finding, 2 could-not-evaluate (exit 2 wins over 1), per the Tripwire
    interface in the round-17 context. Self-test spelled `python3 -I tools/mado-tripwire.py --selftest
    .ufo/waves/round-17/tripwire/core` and `.../compound`.
  - `mado-label-check` (probe): entry `python3 -I .ufo/waves/round-17/label-check.py`; exit 0 all claims ok,
    1 any MISMATCH, 2 could-not-evaluate, per the TabiR16/gen_w1 executor spec. No self-test is defined
    for it in the round-17 spec, so the row records the seeded red control (R16-V1 at round-16 lesson
    line 131, expected `snapshot_tampered`, receipt records `frozen_error`) and a green control.
- Insertion point for L1: after SKILL.md line 545 (`mado-round16-measure`), before the blank line at 546.

## Behaviour and gates

- Actions: read SKILL.md lines 519-575, read `.ufo/waves/round-17/` tree listings, grepped
  `.ufo/waves/round-17/gen_w1.py` and `w1/spec.json` for the label-check and tripwire spec text.
- Commands run: `read`, `ls`, `grep`, `sed -n` on lane files only.
- Not run: no pacman, yay, paru, sudo, systemctl, hyprctl, libinput, evtest, wayland-info, hypridle,
  hyprlock, alacritty, waybar, walker, omarchy-*, notify-send, screenshot, device or input probe, no
  `.omp/agent/agent.db*` or credential access, no omp CLI, no selftest or gate execution.
- Tool installs or upgrades: none (none needed for a drafting task).

## Findings and caveats

1. Producer paths do not exist yet at drafting time: `tools/mado-tripwire.py`,
   `.ufo/waves/round-17/tripwire/core/`, `.ufo/waves/round-17/tripwire/compound/`,
   `.ufo/waves/round-17/label-check.py`, `.ufo/waves/round-17/label-claims.json`,
   `.ufo/waves/round-17/evidence/session-index.json`. The draft uses the spec'd paths and flags them
   as pending. L1 must confirm each path after the producing seats land before integrating the rows.
2. `mado-label-check` has no defined self-test in the spec, so its row shows `—` in the self-test
   column, following the existing probe-row convention (SKILL.md line 539-545). If L1 wants a
   self-test column entry, the label-check executor must add a `--selftest` mode; this draft does not
   assume one.
3. Limit paragraph covers: post-hoc only; only bash/eval `toolCall` commands the assistant issued
   (tool results, user text, thinking/text not inspected); transcripts are mutable host files bound by
   `session-index.json` digests (a changed file fails its digest, is not proven clean); not
   interception, prevention, or host repair; registration is not verification.
4. Finite-pattern boundary (round-16 classifier-limit precedent, SKILL.md lines 547-553): unlisted wrappers or interpreters are not classified, and a clean scan is not "no host mutation". The draft's limit paragraph now states both (draft line 21). L1 may expand the wording in the final SKILL.md text.

## Out of scope / not touched

- SKILL.md, corpus/*, SCORECARD.md, LOG.md, PROVINCE.md and all lessons: untouched (L1-owned).
- tools/mado-tripwire.py, label-check.py, tripwire fixtures, session-index.json: not created by this
  seat (owned by other executors).

## Artifact paths

- Draft: `.ufo/waves/round-17/drafts/SkillRegistryDraft.md`
- Report: `.ufo/waves/round-17/w1/reports/SkillRegistryDraft.md`
