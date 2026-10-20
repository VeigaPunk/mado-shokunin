# NoteTerminal — P4 terminal documentary route (round 17)

Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. Date 2026-10-20.

## Behavior

Drafted the P4 sourced documentary route note `corpus/knowledge/terminal-route-r17.md`
(head: `source:`, `verified-at:`, `recheck:`, `surface: P4`; sections
`## Upstream contract`, `## Host declaration`, `## Safe observation`,
`## Unexercised behavior`) and the SOURCES row draft with gate quotes,
per-source SHA-256 and rejected candidates
(`.ufo/waves/round-17/drafts/NoteTerminal-rows.md`). Route is documentary only; no
observed behaviour is claimed.

## Sources (tag-pinned, opened 2026-10-20)

| Id | Source | Pin | SHA-256 |
|---|---|---|---|
| S056-pending | xdg-terminal-exec README.md | tag v0.14.3, ref 065925df9f419008159258ae169018bfd23df71b | c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40 |
| S057-pending | xdg-terminal-exec script | tag v0.14.3 | 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac |
| S058-pending | Alacritty extra/man/alacritty.5.scd | tag v0.17.0, tag object dc946285396bd3e251b6942af7e9961b74f76bee, commit 94e7c8874e526b1e67b349d9ba30ddf81669119e | e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107 |
| S059-pending | host bindings.conf, xdg-terminals.list, alacritty.toml (bytes) | host files | e574a1ed…0581 / d035da57…ceb71b / 695301c8…24f8 |
| S060-pending | host /usr/share/xdg-terminal-exec/xdg-terminals.list | host file; byte-identical digest to upstream v0.14.3 list | a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034 |

Rejected (search snippet only, not opened): S061-pending Ubuntu manpage (0.14.0
distro build, rendered page); S062-pending GitHub master blob (mutable branch
ref). Flip conditions recorded in the rows draft.

Raw fetched bytes are in /tmp/mado-r17-nt/ (outside the lane; not committed).

## Findings

- Upstream: selection files `${desktop}-xdg-terminals.list` / `xdg-terminals.list`;
  first valid entry wins after the applicability check (README.md:153-166);
  system-data list is lowest priority. Alacritty is named as a compliant example
  (README.md:264), which is not a version or behaviour claim.
- Alacritty v0.17.0 docs: imports load in order and missing files are skipped;
  `live_config_reload` defaults to true (alacritty.5.scd:35-37, 57-61).
- Host declares the chain: `bindings.conf:2` launches `xdg-terminal-exec --dir=…`;
  `~/.config/xdg-terminals.list:3` names `Alacritty.desktop`; `alacritty.toml`
  imports an omarchy theme file. Host system list at
  `/usr/share/xdg-terminal-exec/xdg-terminals.list` is byte-identical to upstream
  v0.14.3's list. No desktop-prefixed selection file or /etc/xdg list present.
- The host `alacritty.toml` has no `live_config_reload` key (grep count 0).

## Unexercised ([UNK] in note)

Which terminal actually launches; installed Alacritty version vs v0.17.0 tag;
whether the host Alacritty desktop entry sets TerminalArgDir/TerminalArgExec;
reload effects on this host; the validity of `omarchy-cmd-terminal-cwd` output.

## Gates and constraints observed

- Host paused: no pacman, sudo, systemctl, hyprctl, omarchy-*, alacritty,
  xdg-terminal-exec, notify or input command was run. Host reads were file bytes
  only (sha256sum, cat, grep, stat, find -maxdepth 1 on ~/.config).
- Remote reads: curl to raw.githubusercontent.com; `git ls-remote` for tag refs
  (run from the lane root, network read; no git or jj mutation). GitHub API
  returned 403 and was not relied upon.
- Quotes checked: each ≤25 words and copied verbatim from the fetched bytes;
  word counts corrected in the rows draft before handoff.
- No tool installed or updated in this route.
- Files touched: `corpus/knowledge/terminal-route-r17.md` (new),
  `.ufo/waves/round-17/drafts/NoteTerminal-rows.md` (new), this report. Nothing
  else in the lane was written. L1 owns SOURCES.md, README, SKILL, SCORECARD, LOG,
  PROVINCE and all lessons; no edits to those.

## Out of scope

No executor or test run (none assigned). No SOURCES.md edit; ids remain
`S0xx-pending` for L1 to assign on integration.

## Checks for the main agent

- Re-run the five SHA-256 checks and the note's named-line reads after
  integration (`recheck:` in the note).
- Assign S-ids (S056-S060 suggested) and merge the rows; confirm the note's
  `source:` line cites the assigned ids.
