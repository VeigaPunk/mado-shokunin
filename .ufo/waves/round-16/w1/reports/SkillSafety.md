# MadoR16.SkillSafety — SKILL draft: host pause and round-16 install wording

Scope: source reading only. Drafts the SKILL.md replacement for the round-15 install paragraph. SKILL.md is L1-owned; nothing in the lane was edited. No package, service, compositor, input, screenshot or command-producer probe was run. Nothing was installed or updated (tool, version, channel: none).

Axes (godspeed): (A) host safety — no pacman transaction or implied authorization; (B) round restriction fidelity — source-only, no live probes; (C) cross-document consistency with the round-15 wording L1 must supersede; (D) precision of the install precondition. Moves kept: the tsukuroi caveat (improves D, harms none of A–C).

## Sources read (anchors)

- `corpus/lessons/round-15-verifier-spotcheck.md` — R15-V1 (forbidden partial upgrade, operator-owned remediation), R15-V2 (dry-run requirement; hard-coded fixtures are not actual validation; no install merely to satisfy review). Read before drafting, per contract.
- `SKILL.md` lines 467–475 (snapshot `SKILL.md#E381`): round-15 paragraph "Tool installs are not exempt from host safety." This is the text to supersede. It says "No further pacman operations ... in round 15" and "any overlap goes to L0, not an install"; both are round-15-scoped and must be replaced, not appended to.
- `corpus/lessons/round-15.md:15` (M2) and `:198` — round-15 guard wording; `LOG.md:1093–1110` — historical round-15 entry (append-only; do not rewrite).
- `.ufo/l0-questions.md` (fleet root) line 54 — hyaku-orchestrator HOST PARTIAL UPGRADE entry: libinput 1.31.3-1 → 1.32.0-1 while the host is 413 packages behind its sync DB; recovery choice is operator-owned.
- `.ufo/l0-questions.md` line 55 — tsukuroi round-15 request for a host-wide pause on all pacman transactions until an operator-owned recovery/update plan clears the mkinitcpio 42 hook risk. It also states that the installed-name dry-run guard is "necessary but not clearance": all-new targets can combine newer binaries with unversioned older dependencies, and `--needed` is not a no-upgrade switch. This is the basis for the added caveat below.
- `~/.omp/agent/RULES.md` — always-on tooling directive (2026-10-19). Read only, as the contract requires before helpful installs. Not opened: `~/.omp/agent/agent.db*`, credential or auth files.
- `.ufo/waves/round-16/w1/spec.json` item `SkillSafety` (scribe) — assignment text.

Not re-observed: pacman state, the 413 pending rows, and the libinput version on the host. These are cited from the L0 lines above and from the closure spot-check only.

## Conflict for L1 / Main adjudication (not resolved by this seat)

The always-on operator directive in `~/.omp/agent/RULES.md` says every agent installs or updates tools without asking. This round's contract says "This round do not install anything", and pauses all pacman transactions host-wide until an operator recovery decision. The draft below states that, for this lane, the pause and round restriction govern and the directive does not authorize a package transaction while the pause holds. The contract is the more specific and later instruction, but the precedence is a call for L1 or Main; the SKILL text should make it explicit either way so no seat reads the global directive as permission.

## Draft: SKILL.md replacement for lines 467–475

Replace the whole paragraph beginning `**Tool installs are not exempt from host safety.**` (lines 467–475) with the block below. Keep the round-15 incident narrative in `corpus/lessons/round-15.md` M2 unchanged; the SKILL block points to it.

```markdown
**Host pause (round 16; supersedes the round-15 install wording).** Every `pacman`
transaction on this host is paused host-wide until an operator recovery decision is
recorded in the fleet L0 channel. While the pause holds, no seat runs `-S`, `-Sy`,
`-Syu`, `-U`, `-R`, `-Sw`, a partial upgrade, a downgrade or revert, or a service or
compositor restart. The always-on tooling directive in `~/.omp/agent/RULES.md` does not
authorize a package transaction while this pause holds; the pause and the round
restriction govern this lane. Recovery of the round-15 partial upgrade (libinput
1.31.3-1 → 1.32.0-1 with the host 413 packages behind its sync database) stays
operator-owned: keep, revert, or a full upgrade through tsukuroi-shokunin's
`/sysroot` update-safety gate. See [`round-15.md`](corpus/lessons/round-15.md) M2.

**Source-only round restriction (round 16).** Seats read source and lane files only.
No package operation (install, update, sync, query, `-Sp` plan, cache download), no
service operation, and no live compositor, input-device, screenshot or command-producer
probe. A missing prerequisite is reported as missing, not installed. Commands quoted in
documentation are source data, never permission.

**Future install precondition (only after an operator-authorized lift of the pause).**
An install requires an explicit operator authorization recorded in the lane record, then
a real plan: `pacman -Sp --print-format '%n %v' <pkgs>`. Compare the complete planned
name set, including dependencies, with the installed names. Any overlap refuses the
install and goes to L0. A passing plan is necessary, not clearance: `--needed` is not a
no-upgrade switch, and an all-new target set can still pair newer binaries with
unversioned older dependencies. Full-system upgrades stay behind tsukuroi-shokunin's
update-safety gate (mkinitcpio 42 moves root to `/sysroot`; the host's `btrfs-overlayfs`
and `plymouth` hooks still expect `/new_root`); a plan check does not clear that gate.
Hard-coded fixture controls prove only the predicate, not an actual plan or installed
state.
```

## Cross-document alignment L1 must make (not edited here)

- `SKILL.md:467–475` — replace per the draft above (this seat's only proposed SKILL change).
- `QUALITY.md` — absent at the baseline `32c4fda`; the round-16 criterion superseding QUALITY 20 belongs to another seat. It must carry the same pause and round restriction wording, not the round-15 "No further pacman operation" line.
- `SCORECARD.md:704–716` (round-16 claim) already says "while the host pause holds"; it should cite the new SKILL block by its heading, not by line number.
- `corpus/lessons/round-15.md:15` and `:198` and `LOG.md:1093–1110` — historical round-15 records; append-only, do not rewrite. Add a round-16 entry instead.
- `corpus/lessons/round-15-verifier-spotcheck.md` — closure record; do not edit.

## Limits

- Draft only. This seat did not edit SKILL.md, QUALITY.md, SCORECARD.md, LOG.md or any lesson file.
- The pause's recorded decision is not observed: the spec and contract state it, and the L0 lines name the operator channel. No later operator answer was found in the files read.
- No verification was run (per contract, L1 alone verifies once after integration). Suggested for L1 after integration: confirm the SKILL section renders, confirm no remaining "round 15" pacman permission text in SKILL.md, and run the lane's own gate once.
- Tools installed or updated by this seat: none.
