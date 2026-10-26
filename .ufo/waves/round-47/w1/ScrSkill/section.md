## Terminal selection (round 47)

`python3 tools/mado-terminal.py` answers "which terminal does SUPER+RETURN launch, and why" without launching one: it
re-implements in Python 3 stdlib the selection of `xdg-terminal-exec` v0.14.3 (`/usr/bin/xdg-terminal-exec`, sha256
`89f2be9a…27ac`, byte-equal to upstream tag v0.14.3), starting no process and opening no socket. `print`
reproduces the pinned script's print modes byte for byte on stdout and exit status — the real script is the judge, and
the tool never calls it; `explain` shows the chain; `--selftest` runs the tool's own cases. The resolver's cache is out
of contract: the tool models a cold cache, so every capture redirects `XDG_CACHE_HOME` (a run that includes
`--print-cmd` rewrites the cache, in the background). On this host the hotkey (`~/.config/hypr/bindings.conf:2`) resolves
to `Alacritty.desktop` at the user copy under `~/.local/share/applications/`: `~/.config/xdg-terminals.list` lists it,
and a duplicate ID is won by the entry registered last — the user data dir is searched last, so it wins
(`live-print.txt`, `probes.txt`). Use it when the hotkey opens the wrong terminal or none, after editing a
`*-xdg-terminals.list` or a terminal entry, or before writing down what the hotkey resolves to.
Ground: `corpus/knowledge/xdg-terminal-selection-r47.md` (rows S326..).

    # the selection: the pinned resolver's answers on this host, which print must reproduce
    # (print mode only — no terminal is started; the cache goes to a throwaway dir)
    $ python3 tools/mado-terminal.py print --print-id --print-path --print-cmd
    Alacritty.desktop
    /home/vgpnk/.local/share/applications/Alacritty.desktop
    alacritty

    # the hotkey's composition: --dir becomes an argument only because the entry carries X-TerminalArgDir
    $ python3 tools/mado-terminal.py print --print-id --print-path --print-cmd --dir=/tmp -- htop
    Alacritty.desktop
    /home/vgpnk/.local/share/applications/Alacritty.desktop
    alacritty
    --working-directory=/tmp
    -e
    htop

    # the chain: the list file and line that selected it, every rejected candidate and why, then the verdict line
    $ python3 tools/mado-terminal.py explain
    … trace lines (the tool's docstring fixes their prefixes) …
    MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop verdict=OK

    # the same question to the resolver itself, captured cold, then compared with the tool
    $ XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-path --print-cmd > term.observed
    $ python3 tools/mado-terminal.py explain --observed term.observed
    … MADO_TERM: … verdict=AGREE

    # the tool's own cases, built under $TMPDIR
    $ python3 tools/mado-terminal.py --selftest
    MADO_TERMINAL_SELFTEST: N/N passed        # N >= 30

Exit status: `print` carries the script's own (0 a selection was printed, 1 nothing valid); `explain` prints 0 for OK or
AGREE, 1 for DIFFER, 3 for NO_TERMINAL, 2 for usage. `print` with no `--print-*` flag is a usage error: the tool never
launches a terminal, so the script's launch path is outside the contract.

| verdict | where it prints | what it means | next read-only step |
|---|---|---|---|
| `OK` | `MADO_TERM:` line of `explain` | a selection was computed from the files and nothing was compared | read the trace above the line: it names the list file and line that selected, and every rejected candidate with its reason |
| `AGREE` | `MADO_TERM:` line of `explain --observed` | the tool's print for this environment equals the captured file byte for byte — same id, same path, same command arguments in the same order | none for the selection; if the *host* still behaves differently, look at the wrapper (`uwsm-app --`) or the environment, not at the resolver |
| `DIFFER` | `MADO_TERM:` line, rc 1 | capture and tool did not see the same environment or argv: a missing `--dir`/command argument, a different `XDG_*` value, or a warm cache | re-capture with the exact command above and the same trailing arguments, then diff line by line — id, then path, then one argument per line |
| `NO_TERMINAL` | `MADO_TERM:` line, rc 3 | no candidate survived validation | the trace names every rejection; fix the entry the list names, or name one that is valid |
| print rc 0 | stdout, nothing else | id, then path, then the command arguments, in the fixed order id → path → cmd whatever order the flags came in; `--print-delimiter` separates the statements, `--print-cmd[=seq]` separates arguments (`\n` each by default, and a `\n` also terminates the output) | — |
| print rc 1 | stdout empty; the resolver's stderr carries `No valid terminal entry was found in:` and the applications dirs | nothing valid was found | see "nothing launches" below |
| usage rc 2 | one line | a bad invocation of the tool itself (unknown mode, unreadable `--observed`) | fix the argument; it is not a verdict |

| symptom | first read | the rule behind it | next step |
|---|---|---|---|
| a different terminal launches than the list names | the list files in order: in `XDG_CONFIG_HOME` then each `XDG_CONFIG_DIRS` entry, `<desktop>-xdg-terminals.list` for every lower-cased `XDG_CURRENT_DESKTOP` item, then `xdg-terminals.list`; then the same pair under `<data dir>/xdg-terminal-exec/` for each `XDG_DATA_DIRS` entry | the first listed entry that validates wins; a listed entry that fails validation is skipped silently; with no valid listed entry the fallback takes the ID registered last — user data dir before the system dirs, and inside one directory the reverse of the order `find` lists it (`xdg-terminal-exec:754-800`) | `explain` names the file:line that selected; then read that entry's keys |
| nothing launches | each candidate's `Categories`, `Hidden`, `TryExec`, `Exec`, `X-TerminalArgExec` | one failed key drops the candidate: no `TerminalEmulator` in `Categories`, `Hidden=true`, `TryExec` or the first `Exec` word not on `PATH`, no `Exec` in `[Desktop Entry]` or in the action group, and in strict mode no `X-TerminalArgExec` (`xdg-terminal-exec:816-968, 1087-1101`); `Type=` and `NoDisplay=` are never read | `explain` lists each rejection; the script itself exits 1 with `No valid terminal entry was found in:` and the applications dirs |
| `--dir` is ignored | the entry's `X-TerminalArgDir` | without that key no directory argument is composed; at launch the script changes its own working directory before `exec` instead (`xdg-terminal-exec:1494-1496`) | `print --dir=/tmp --print-cmd` and look for a `--working-directory` line: absent means the key is missing. Alacritty has it, and the hotkey's directory comes from `omarchy-cmd-terminal-cwd` — a wrong directory there is not the resolver |
| the title is ignored | the entry's `X-TerminalArgTitle` | the same rule (`xdg-terminal-exec:1415-1427`); an empty `--title=` value composes nothing | grep the entry for `X-TerminalArg`; the key carries the option and often its `=`, e.g. `--title=` |
| an action does not take effect | the list line `id:action`, the entry's `Actions`, the `[Desktop Action x]` group | an action not listed in `Actions` rejects that candidate and its group is ignored (`xdg-terminal-exec:829-845`); argv cannot choose one — the first non-option is always the command | put the action on the list line; `explain` names the candidate it rejected |
| a change has no effect | `$XDG_CACHE_HOME/xdg-terminal-exec` | the cache is keyed by `XDG_CURRENT_DESKTOP` and an `ls -LRl` of the list and data paths, and a `--print-cmd` run rewrites it (`xdg-terminal-exec:179-215, 1457`) | capture with `XDG_CACHE_HOME=$(mktemp -d)`; the tool models the cold cache by contract |

Notes: `explain` is the tool's reading of the same files, not the resolver's own debug output — for that one use
`XTE_DEBUG=1 XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id` (debug goes to stderr), never without a
`--print-*` flag, which would launch a terminal. A trace prints absolute config paths, so keep its lines out of receipts
that the session-material gate counts (a single path quoted in prose is fine). The hotkey's `uwsm-app --` wrapper is not
modelled: it is not a selection input. `Type=` and `NoDisplay=` are not rules of 0.14.3 — a `Type=Link` entry with the
right category and `Exec` is selected (`probes.txt` A/B) — so an `explain` trace that claims those rejections is wrong;
the `OnlyShowIn`/`NotShowIn` checks apply to fallback candidates only, never to a listed one (probes K/L).
`--print-content` is a script mode the draft contract does not cover: treat the docstring as authoritative and prefer
id/path/cmd.
