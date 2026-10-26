# ScoutScriptMap report (round 47, w1)

Status: DONE. Deliverable: `.ufo/waves/round-47/w1/ScoutScriptMap/map.md` (function map with line ranges, `--print-id` main flow, env vars, external commands, exit statuses, quirks).

- Pin: `/usr/bin/xdg-terminal-exec` sha256 == upstream tag v0.14.3 raw file sha256 == `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (`sha256.txt`, `upstream-xdg-terminal-exec`). 1499 lines, 23 functions, bash 5.3.20 as /bin/sh.
- Anchors: `verify-anchors.txt` re-greps 103 cited (line, snippet) pairs: 103/103 OK.
- Probes (`probes/`): print-only / `--test` / `-h` runs of the real script, scratch `XDG_CACHE_HOME`, outputs in `probes/run*.out`.

Findings that change what the tool and its fixtures must cover (details map.md sections 2-8):
1. errexit is suppressed inside `check_entry_key ... && continue`, so tokenizer / field errors do not discard an entry: Exec is truncated at the error (`foo --a "$X" bar` -> `foo --a`) or keeps `%f %f` fields.
2. `reset_keys` runs only on a failed key: a parsed-but-skipped candidate (no Exec / not a terminal) leaks Exec, TerminalArg*, EXECARG into the next candidate.
3. `--print-id`/`--print-path`/`--print-content` exit at 1383/1376 before `save_cache`: no cache write; `--print-cmd` and `--test` write it (background `&`).
4. Fallback order within a directory is `find -L` readdir order, prepended (last found tried first); `os.scandir` order equalled find order on xfs scratch.
5. No `Type=` check (the draft `explain` text "wrong Type" has no counterpart in the script); `NoDisplay`, `Hidden=True` ignored; only exact `Hidden=true` rejects.
6. Last line without a trailing newline is never read (entry files and config lists).
7. Empty-string argument in the option loop never terminates (needs a timeout / is out of fixture space); `-h` anywhere before `--` prints help.
8. `%b` printf semantics for delimiters, `--print-cmd=` empty vs `\n` trailing-newline rule, `/./` marker removal drops the middle when the data dir contains `/./`, empty `:` fields in XDG_CURRENT_DESKTOP produce `-xdg-terminals.list`.
9. External commands in the selection path: `tr` (1144), `find` (795), `awk` (797) only; `ls`, `md5sum`, `mkdir`, `rm` only through gen_hash/save_cache.

Tooling installed: none. Scratch removed. No writes outside the seat dir and this report.
