# CritTheme — is the idle-lock control-surface theme mado's province?

Round 35, wave 1. Attack seat: argue the theme out of province; report the verdict
the files actually support. Substrates untouched; every citation below is a lane or
fleet file read.

## Verdict

**In province — admit.** The attack fails on PROVINCE's own text: the theme is a
measurement of surfaces the charter names or has already absorbed, exercised under
the lane's standing read-only discipline. The strongest wrong-fit reading exists
and is stated below — it loses because the lane's own recorded precedent already
draws the line the theme sits inside of.

## The theme as registered

`registration.md` C1 defines the surface: the bar's idle-indicator module, the
desktop menu's `Idle Lock` entry, the indicator's two-state vocabulary, the armed
screensaver/lock chain, and the setup path that never asks. Evidence is S203–S210:
`waybar/config.jsonc` + dated backups, `indicators/idle.sh`, `omarchy-menu`,
`omarchy-first-run`, `toggles/hypr/` contents, `pgrep`/`is-active`/journal reads,
and `hypridle.conf` timeouts — all read-only.

## For admission — what PROVINCE already owns

1. **Named surface.** `PROVINCE.md:9` owns "screen/idle behavior (hypridle/hyprlock
   where present)". `hypridle.conf` lives inside the owned `~/.config/hypr/` tree
   (`:6`); the `custom/idle-indicator` module is inside the owned
   `~/.config/waybar/` tree (`:7`). S206, S209 and the hypridle half of S205 are
   owned bytes verbatim.
2. **Precedent, not novelty.** `corpus/knowledge/idle-lock-plane.md` §2b already
   inventories eleven `~/.local/share/omarchy/bin/omarchy-*` actuator scripts —
   including `omarchy-toggle-idle`, `omarchy-launch-screensaver`,
   `omarchy-system-lock/-wake` — with per-file hashes; §5 anchors their bodies
   line-by-line; §8 is titled "Toggle & indicator surface" and already covers
   `idle.sh`, `omarchy-toggle-idle`, and the `toggles/` flag directory that S210
   re-reads. The theme extends a plane the lane catalogued two probe passes ago;
   nothing in it is a new kind of read for this lane.
3. **Checkout as ratified evidence.** The round-19 refinement
   (`PROVINCE.md:18`) declares `~/.local/share/omarchy/**` "read-only source
   evidence for this chain." `omarchy-menu` (S208) and `omarchy-first-run` (S203)
   are bodies of that same checkout. The refinement's own list already treats
   script bodies the same way (`omarchy-refresh-config`, `-menu` cited at
   idle-lock-plane §8) — bodies of the chain are read, never run.
4. **Unit-state probes have a recorded boundary.** S205's `is-active` and journal
   reads sit exactly where `PROVINCE.md:32` already put `mado-verify.sh`'s:
   "its unit-state rows sit next to tsukuroi's unit-health ground, which stays
   tsukuroi's." Reading unit/journal state *as evidence about the desktop's
   declared chain* is the established convention, not new reach.
5. **Refuses un-tripped.** No secret content (hyprlock's PAM path is already
   marked "credentials surface; out of province" at `idle-lock-plane.md` §4),
   no endpoints, no model quality (`PROVINCE.md:14-16`).

## The wrong-fit case — and why it loses

The best attack: PROVINCE's owns list is *declared config planes*; the theme reads
a live process (`pgrep`), unit state (`is-active`), journal rows
(`journalctl --user`), two *program* bodies (`omarchy-menu`, `omarchy-first-run`),
and asserts runtime state ("the chain is armed"). Under a files-only reading,
S204/S205 and half the adopted surface are host-state reads — journal and
systemd ground belong to tsukuroi (systemd units/timers, journal/boot triage per
`tsukuroi-shokunin/PROVINCE.md`), journal observability to mori.

It loses on three grounds:

- **The discriminator isn't file-vs-process.** It's *the desktop's declared idle
  chain vs host state for its own sake*. `idle-lock-plane.md` §7 already recorded
  `systemctl --user status`, `loginctl`, `hyprctl monitors` and `ps` as a dated
  `[OBS]` point sample under an explicit operator-presence constraint (§0); the
  round-23 PROVINCE correction ratified that pattern for the lane's tools. If
  process/journal probes about the idle chain were a bleed, the standing corpus
  note would already be one — and the charter's correction history shows the
  opposite ruling.
- **The claims stay on the desktop side of the sibling lines.** S205's claim is
  "the daemon runs, the declared chain is armed" — a display-behavior fact.
  `idle-lock-chain-armed-r14.md` §2 does the boundary-correct thing with the
  unit probe: it records `is-active → inactive` *disagreeing* with the pid and
  names the unit read a probe artifact, i.e. it reports the discrepancy rather
  than asserting unit health. That is precisely the shape "report, never absorb"
  (`PROVINCE.md:34`) prescribes for adjacent ground.
- **No sibling owns the question.** The theme asks whether the *desktop* offers
  and remembers the idle-lock choice. No rostered lane's domain covers
  desktop-presentation semantics; mori owns fleet-liveness/kill-OOM journal
  classes, not per-user toggle invocations; tsukuroi owns unit health, not
  whether a compositor-facing toggle exists.

## What a sibling would have to own for this to be a cross-domain bleed

A bleed requires the theme's *claims* to land on another lane's owned ground, not
merely to cite it. Concretely, a sibling would need one of:

- **Unit/service health as its own end** → tsukuroi. If the theme concluded
  "hypridle.service is misconfigured/should be enabled," that is tsukuroi's
  ground; the theme instead treats unit reads as evidence about a desktop
  behavior and flags the artifact.
- **Journal forensics as a domain** → mori (fleet classes) / tsukuroi (boot
  triage). If the theme reconstructed *why* hypridle stopped on 2026-10-14 from
  journal history, that is triage, not display craft. `idle-lock-plane.md` §7
  already files that cause as `[UNK]`, correctly unclaimed.
- **Credential/auth surfaces** → kagi. Auditing `omarchy-system-lock`'s
  `1password --lock` arm or hyprlock's PAM path would bleed; both are already
  fenced out in the lane's notes.
- **Installer/first-run mechanics as a domain** → unowned on this roster
  (MANIFEST 13 lanes; shokunin.conf adds mado, tsukuroi, tabi, mori, chousa,
  kotodama, souji, audio, game-dev — none owns installer UX). S203's finding is
  about whether the desktop *asks* — desktop-behavior semantics read from a
  checkout body — so no live sibling claim exists to bleed into.

## Residual risk the lane must hold

The theme's farthest edge is S203/S204: "the setup path never asks" reads
installer machinery, one step beyond the owned display planes. It is defensible
as *read evidence* for a desktop question (the same checkout-body precedent),
but the lane should keep the claim scoped exactly as `idle-lock-never-asked-r12`
§3 does — the *setup path*, not "the desktop" — and never slide into installer
correctness. That file already does so; the boundary holds.
