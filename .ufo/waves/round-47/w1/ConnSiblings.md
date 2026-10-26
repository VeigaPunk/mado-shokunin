# ConnSiblings — sibling-overlap scan: terminal-selection plane

Seat: ConnSiblings-6 · Round 47 · wave w1 (BUILD) · 2026-10-26
Task: read sibling lanes' PROVINCE.md (+ SKILL.md) under
`/home/vgpnk/Projects/shokunin/*-shokunin/` and mado's own; name who else claims
xdg-terminal-exec, XDG desktop entries, default applications (xdg-mime), uwsm,
omarchy launchers; propose a PROVINCE.md refinement line for mado (or none).

## Method (all read-only)

- `glob /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` → 21 lanes (20 siblings + mado).
- `grep` (case-insensitive, gitignore=false) over all 21 PROVINCE.md **and** their
  SKILL.md for contested vocabulary:
  `xdg-terminal-exec|uwsm|omarchy|xdg-mime|mimeapps|default application|desktop-file|desktop entry|applications/|launcher|\.desktop|xdg-menu`.
- `grep` over every sibling `corpus/` and mado `corpus/` for `uwsm|xdg-terminal-exec|xdg-mime|mimeapps` (latent prior art / event records).
- Read province heads (Domain/Owns/Refuses/Out-of-province) and the relevant knowledge rows.

## Finding 1 — no sibling claims the terminal-selection subject

No lane other than mado claims xdg-terminal-exec selection semantics, XDG desktop
entries/application dirs, default applications (xdg-mime), or uwsm: zero matches
for those strings in any sibling PROVINCE.md/SKILL.md. The only "launcher" hits
are unrelated tool launchers:

- RE tooling launchers — kaidoku PROVINCE.md:170-171,268 (Hopper/REA launcher paths).
- llama-server/install-tree launcher — kama SKILL.md:638-642,655-659.
- OMP native launcher — kumitate SKILL.md:263-266,304-314.
- chromium launcher flag injection — tabi SKILL.md:2803-2807.
- r44 control "launcher blob" — chousa SKILL.md:110.

"MIME" appears only as web-metadata og:image checks (kake PROVINCE.md:195-199);
"xdg-*" only as app-cache paths (kagi PROVINCE.md:33-34) and session scope names
(below). "desktop entry"/".desktop"/"xdg-menu": no matches anywhere.

## Finding 2 — adjacent boundaries that must be stated

1. **tsukuroi — package state/provenance and systemd units.** Owns pacman state
   (repo provenance, foreign-pkg census) and systemd user units/timers
   (tsukuroi PROVINCE.md:8-11,25-28). Its corpus names `xdg-terminal-exec` among
   the 36 omarchy-repo packages (tsukuroi corpus/knowledge/aur-risk-plane.md:199),
   tracks the walker/omarchy-walker update path and dead channel
   (tsukuroi SKILL.md:100-102,734,755), and records
   `app-Hyprland-xdg-terminal-exec-…scope` OOM/service events
   (tsukuroi corpus/knowledge/boot-plane.md:101). The pinned script bytes are host
   fact for mado's tool input; package version/channel/update-path and unit health
   stay tsukuroi's. Precedent for this carve-out already exists in mado
   PROVINCE.md:28 (walker-unit rows sit next to tsukuroi's unit-health ground).
2. **mori — fleet/host liveness event records with the same scope-name strings.**
   Kill/OOM catalog from user/system journals (mori PROVINCE.md:3-10); guards
   against attributing an unrelated desktop OOM to another demand (mori
   corpus/knowledge/observability-census-r1.md:93-97,142-146). "Which terminal
   launches" ≠ kill records; shared strings only, no ownership overlap.
3. **tameshi — verification-fixture method.** Owns the reusable method; each
   lane's gate stays its own; never edits a sibling's gate code (tameshi
   PROVINCE.md:3-17). mado's fixture schema and counters are an application of
   the method, not a claim over it.
4. **kotoba — skill craft.** Inventories production skill files incl. omarchy
   verbatim (kotoba SKILL.md:517-520). mado treats the omarchy skill as read-only
   documentation (mado PROVINCE.md:10-12) and never authors it. The omarchy CLI at
   `omarchy-cmd-terminal-cwd` in the bind stays operator-owned tool surface; its
   runtime effect on the launch remained [UNK] at round 17
   (terminal-route-r17.md:103-107) — C1 models xdg-terminal-exec, not the helper.
5. **Homonyms to guard:** kengaku "Terminal-Bench 2.0" is a benchmark subject
   (kengaku SKILL.md:233-236); mori's `tools/mori-seat-terminal.py` reads session
   transcripts (mori PROVINCE.md:103-107), not desktop terminals. Neither touches
   the terminal-selection plane.

## Finding 3 — mado's own prior art (what the freeze covers is unclaimed elsewhere)

mado's P4 chain evidence is self-contained: SOURCES rows S056-S071
(SOURCES.md:68-72,83), `knowledge/terminal-route-r17.md` (bindings.conf:2 chain at
:81,103-107; the [UNK] this round closes at :144-145), `terminals-and-omarchy.md`,
`waybar-walker-semantics.md:337-341`, `hyprland-config-plane.md:83-84`. No sibling
holds an analogous record.

## Contested-scope verdict

**No direct contention.** One genuine gap: uwsm runtime/session mechanics have no
claiming lane (only package state in tsukuroi, plus envelope observations inside
mado's chain docs). The proposed line keeps that unclaimed rather than inventing
ownership.

## Proposed PROVINCE.md refinement line for mado (append after line 115; append-only; no new write surface)

> **Round-47 refinement (append-only; terminal-selection plane; no new write surface):**
> which terminal `SUPER+RETURN` launches and why is owned here as knowledge and
> analysis: the executed selection chain of xdg-terminal-exec v0.14.3 (list files
> and order per XDG_CURRENT_DESKTOP, desktop-file IDs across data dirs, entry
> validation, actions, exec-arg composition, print modes, cold-cache model) is
> recorded in `corpus/knowledge/xdg-terminal-selection-r47.md` and modelled by
> `tools/mado-terminal.py` (read-only; prints; starts no process, opens no
> socket). This closes the round-17 [UNK] at
> `corpus/knowledge/terminal-route-r17.md:144-145`. Boundaries: package
> version/provenance/update path of `xdg-terminal-exec` and terminal-emulator
> packages, uwsm and unit state stay tsukuroi's; live scope/OOM event records stay
> mori's; the fixture/verification method stays tameshi's; the omarchy
> skill/CLI (incl. `omarchy-cmd-terminal-cwd`) stays read-only documentation/tool
> surface, never authored. The keybind itself remains part of the owned bind
> plane.

## Risks

- "No sibling claims" is true at current heads for the exact strings scanned; a
  claim could still sit in a corpus file without those strings. Mitigation: the
  corpus grep for the three rarest terms (`uwsm|xdg-terminal-exec|xdg-mime`)
  returned only event/package records, never ownership statements.
- The tsukuroi boundary wording mirrors the existing precedent at mado
  PROVINCE.md:28, so it introduces no new convention.
- No mutating git was run; nothing outside the seat dir and this report trailer was
  written.
