# ScrSkill — round 47, wave w1 (BUILD) — SKILL.md section draft for `tools/mado-terminal.py`

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`.
Role: leaf scribe (no subagent dispatch). Wrote only inside this seat dir; nothing tracked was edited; no git/jj
mutation; scratch under `/fast/scratch/hyaku/mado-r47/ScrSkill/` was removed at the end.

## Deliverable

`section.md` (76 lines) — the pasteable `## Terminal selection (round 47)` section, shaped after the r46 input-device
section (`SKILL.md:2105-2143`): intro with the contract, three operator command blocks, an exit-status sentence, a
verdict/exit table (7 rows), a `symptom → which file/key` table (6 rows, the four required symptoms plus action and
cache), and a closing notes paragraph (debug cross-check, session-material shape, `uwsm-app` boundary, the two keys
that are *not* rules, `--print-content` boundary).

Sha256 of the artifacts:

    section.md      66e80113e29d61bf0187f79c6f1c3cda5a25ccc9eb8a2b6a1235eb3b7e1281ff
    live-print.txt  9bdd74c7e638aa7e625886af78824539fefbe49b2b2656589fc7769dd4a300f0
    probes.txt      f8201c4d02b25e2bb53862c8a11c5acda60d6607ee402066152b8fb167055590
    locators.txt    f9b623533a4fdd864b562c6911c8ea209b736744a5ab808b0e47a7c940059b0d

Receipts, all produced this run by `drive.sh` (scratch, deleted): `live-print.txt` (three cold-cache print captures on
the host, the resolver's own config list from `XTE_DEBUG=1`, the live list files), `probes.txt` (16 hermetic cases under
`$ROOT`, `$ROOT` substituted), `locators.txt` (computed `grep -n` line numbers + the pin hashes).

## What the section claims, and what backs each claim

| claim in `section.md` | evidence |
|---|---|
| pinned resolver sha256 `89f2be9a…27ac`, byte-equal to upstream v0.14.3 | `sha256sum /usr/bin/xdg-terminal-exec` = pin; `cmp` with `.ufo/waves/round-47/w1/ScoutSpecs/pins/xdgte-xdg-terminal-exec` → BYTE-EQUAL (`locators.txt:2-3`) |
| host resolves `Alacritty.desktop` → user override path → `alacritty` | `live-print.txt` capture 1 (rc 0); `--dir=/tmp -- htop` capture 2; all-four-modifiers capture 3 |
| `--dir` becomes `--working-directory=<dir>` only because the entry has `X-TerminalArgDir` | user override `~/.local/share/applications/Alacritty.desktop:17`; capture 2 shows the argument, the system copy at `/usr/share/applications/Alacritty.desktop` has no `X-TerminalArg*` |
| argument order Exec, app-id, title, dir, (hold), exec-arg, command | capture 3 output order; code `xdg-terminal-exec:1390-1464` |
| list-file order (`<desktop>-…` per dir then plain; config dirs then data-dir `xdg-terminal-exec/` copies) | resolver's own `D: XTE__CONFIGS=` line in `live-print.txt`; code `:143-163` |
| duplicate data-dir ID resolved to the user dir; fallback = last-registered | probes G (dup: user `Exec=alacritty` beat system `Exec=sh`), M (fallback `zzz` over `aaa`); code `:782,790` |
| list order decides before fallback; prefixed file read before plain in one dir | probes H, I |
| `OnlyShowIn`/`NotShowIn` apply to fallback only | probes K (fallback rejected `OnlyShowIn=GNOME`), L (listed entry accepted) |
| `Hidden`, missing `TerminalEmulator`, off-PATH `TryExec`/`Exec[0]` each reject the candidate | probes C, D, E, F (stderr `No valid terminal entry was found in:`, rc 1) |
| `Type=` and `NoDisplay=` are never read | grep: no `'Type'`/`NoDisplay` pattern in the script; probes A (`Type=Link` selected), B (`NoDisplay=true` selected) |
| action must be listed in `Actions`; argv cannot pick one; action id/path carry `:action` | probes S (list line `aaa.desktop:New` → id/path with `:New`, cmd from the action group), T (unlisted action → candidate skipped, fallback), N (`--print-id aaa.desktop:New` leaves the token as a command, output `zzz.desktop`); code `:829-845, 1055-1111` |
| print order id → path → cmd, separate delimiters, `\n` terminates | probe P (`--print-cmd= --print-delimiter=|` → `id|path|cmd` with no newline); code `:1325-1383, 1470-1490` |
| `--print-cmd` rewrites the cache in the background | `live-print.txt` "cache files written by the run: 1 (dir discarded)"; `save_cache "$1" &` at `:1457`; `--print-id` alone exits earlier (`:1368`) and writes nothing |
| cache key = version `4` + `XDG_CURRENT_DESKTOP` + `ls -LRl` of list+data paths | code `:179-215` |

Every `xdg-terminal-exec:NNN` locator in the section was re-checked against the file after the draft (`:754-800`,
`:816-968`, `:829-845`, `:1087-1101`, `:1415-1427`, `:1494-1496`, `:179-215, 1457`); all four are function or check
boundaries, computed with `grep -n`, not typed.

## Findings for the freeze (each names what it attacks)

1. **Data-dir precedence wording in the C1 prompt is inverted.** `w1-spec.json` (ExecRefA/ExecRefB prompts) says
   "desktop-file IDs across XDG_DATA_HOME then XDG_DATA_DIRS (applications/ subdir -> '-' joined ID, first wins)".
   The script registers `find -L` output in the order `/usr/share`, `/usr/local`, *then* the user dir and overwrites
   the alias each time (`:782,790`), so a duplicate ID is won by the **user** dir — which is exactly the host case
   (system `Alacritty.desktop` is a different file from the user override). Probe G. A faithful-to-the-prompt
   implementation prints the system path and DIFFERs on the live case. Messaged ExecRefA and ExecRefB; both replied
   that their independent models agree (ExecRefA names `make_paths`'s prepend at `:196` plus the overwrite at `:782`),
   which is their report, not a run of mine. The section states the script's rule. **Attacks C1 fidelity.**
2. **The contract's rejection vocabulary lists "wrong Type", which is not a 0.14.3 rule.** `Type=` is never matched in
   the script (grep for `'Type'` returns nothing) and probe A selects a `Type=Link` entry; `NoDisplay=` is likewise
   never read (probe B). An `explain` trace that reports those two reasons fabricates a rule; the section lists the
   real ones and says so. **Attacks C1's `explain` credibility (and any C2 sentence copied from it).**
3. **`print` with no `--print-*` flag is undefined.** The reported contract only fixes byte-identity for print modes;
   with no print flag the script `exec`s a terminal, which the tool must never do. The section declares a usage error
   (exit 2, the tool's own code) — the L1 should freeze that choice explicitly, or the counter should require the tool
   to refuse. **Attacks C1's boundary, not its fidelity.**
4. **`--print-content` is a script mode the draft contract omits.** The section notes it and points at the docstring;
   if the freeze wants it judged, it must be added to the enumerated options, otherwise leave it out of the tool.
5. **`explain` trace grammar is not frozen** (only the tokens and the final `MADO_TERM:` line are). The section
   deliberately does not quote invented trace prefixes; it quotes the token line and describes the content. If the L1
   wants the trace machine-readable, that grammar has to be frozen now, not after integration.
6. **Two selection inputs sit outside the resolver** and must be said out loud where the tool's answer is used: the
   hotkey wraps it in `uwsm-app --` (`~/.config/hypr/bindings.conf:2`) and supplies `--dir="$(omarchy-cmd-terminal-cwd)"`
   (`:2`, `:3`). The section marks the wrapper as unmodelled and the directory source as not-the-resolver.
7. **Cache writes are asynchronous.** A capture containing `--print-cmd` leaves the cache file behind ~0.3 s later
   (receipt); `--print-id` alone does not write it. The contract already requires redirecting `XDG_CACHE_HOME`; the
   receipt explains *why* the capture command is written that way. Messaged ExecCache, which reports (its own receipts
   under `.ufo/waves/round-47/w1/ExecCache/`) the write gate at 41/41 and the fork race at 30/30 by +50 ms — peer
   evidence, not re-run here.

## Axis notes (godspeed)

Axes for this seat: (A) parity with the r45/r46 section shape — a reader who used those finds the same slots; (B)
truth of every operator step against the pinned resolver; (C) freeze-usefulness — each row names a file or key an
operator can open, and each claim carries a locator or a probe. The kept moves improved all three: the r46 column set
(verdict / where it prints / what it means / next step) is reused, every command is a read-only print-mode invocation,
and the two tables are keyed to files (`*-xdg-terminals.list`, the entry's `X-TerminalArg*`, `$XDG_CACHE_HOME/…`)
rather than to symptoms alone. Dropped: a per-branch trace walkthrough (grammar unfrozen) and a cache-mtime table
(out of contract).

## Touched surfaces

    mado-shokunin/.ufo/waves/round-47/w1/ScrSkill/section.md      new
    mado-shokunin/.ufo/waves/round-47/w1/ScrSkill/live-print.txt  new
    mado-shokunin/.ufo/waves/round-47/w1/ScrSkill/probes.txt      new
    mado-shokunin/.ufo/waves/round-47/w1/ScrSkill/locators.txt    new
    mado-shokunin/.ufo/waves/round-47/w1/ScrSkill.md              new (this report)

No tracked file edited; `SKILL.md` untouched (the L1 integrates). No host config or binary touched; `xdg-terminal-exec`
was run only with `--print-*` and a scratch `XDG_CACHE_HOME`; no compositor verb was needed.

## Out of scope / not done here

- The tool itself (`tools/mado-terminal.py`), the fixtures, the counters, the C2 knowledge entry and the round-46
  closure items — other seats.
- No `--selftest` run (the tool does not exist yet); the section prints `N/N` with `N >= 30` rather than an invented
  number.
- No session-material gate run on these files: `quality/check-session-material.py` reads tracked `.ufo/` files at a
  revision, and this seat's files are untracked. Shape checked by hand instead: `section.md` 0 standalone absolute
  `/home/` lines, `live-print.txt` 3 (limit 10), `probes.txt` 0, `locators.txt` 0.

## Tooling

No tool installed or upgraded (no pacman; nothing added to `~/.local/bin`).
