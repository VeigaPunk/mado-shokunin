# ReviewNoteHost: C2 host re-derivation of terminal-trees-r23.md

- Seat: `MadoR23.ReviewNoteHost` (leaf reviewer, wave 2). Judged on: coverage.
- Subject: `corpus/knowledge/terminal-trees-r23.md` (read tag `#2BBC`), sections `## Host declaration` and `## Safe observation` only.
- Mode: read-only. No host state changed. No lane file touched. This report is the only file written.
- Window: 2026-10-22 11:57:24Z to 12:01:16Z (`date -u` stamps below).
- Installs or updates: none made, none needed. `pacman` was used only as `pacman -Q`. No `-S`, `-Sy`, `-Syu`, `-U`, or `-R`.

## Summary

- 29 note claims re-derived. 27 reproduce. 1 is a mismatch (M1). 1 is unverifiable (M3).
- Of the 27 that reproduce, one (row B3, ghostty backup identity) matches in bytes but carries a label caveat (M2).
- Every size, every sha256 prefix, every byte-identity claim, every live-diff claim, every consumer check, the timestamp claim, and the selection-list claim reproduces exactly.

## Findings

### M1. Live Alacritty client count is 1, the note says 2 (mismatch, live state)

- Note, Host declaration, paragraph after the table: "the live clients are Alacritty (HostGhostty: `hyprctl -j clients` read-only, 2 Alacritty clients)."
- Source of the 2: `w1/reports/HostGhostty.md` §3 lines 80-83: `$ hyprctl -j clients` / `client_count=2` / `classes= {'Alacritty': 2}`. The report header does not give the read time, so I cannot date that read.
- My reads (`hyprctl -j clients`, session `HYPRLAND_INSTANCE_SIGNATURE`, `XDG_RUNTIME_DIR=/run/user/1000`):
  - Read 1, after 11:57:24Z: 1 client, class `Alacritty`, initialClass `Alacritty`, pid 2487, workspace id 1, mapped, not hidden, not XWayland.
  - Read 2, 12:00:32Z: 1 client, same pid. `hyprctl -j workspaces` count 1.
- Process cross-check: exactly one `alacritty` process (pid 2487) in the `/proc` scan. No other Alacritty process.
- The class claim holds (only Alacritty; no ghostty, kitty, or foot client). The count does not.
- Advice to L1: state the count with its read time (for example, "2 at the HostGhostty read; 1 at 2026-10-22T12:00Z"), or drop the count.

### M2. "omarchy 3.8.3 checkout" label is ambiguous (label, bytes hold)

- The checkout's `version` file reads `3.8.3`, so the label matches that file. Evidence: `read ~/.local/share/omarchy/version` gives `1:3.8.3`. `git show HEAD:version` also gives `3.8.3`.
- The git ref is different. HEAD is `8fcc9d604` (commit date 2026-07-20T14:05:35-07:00), which is the commit tagged `v3.8.4` (`git describe --tags --always` gives `v3.8.4`). Tag `v3.8.3` is `6aa2aec1c` (2026-07-13T15:56:11-07:00).
- Working tree is clean: `git status --porcelain=v1` prints nothing.
- The three terminal defaults are blob-identical at both tags. Their sha256 prefixes are `8afc9646c61e58e6` (foot), `95eed20aaedb0962` (kitty), and `e47630125605cb19` (ghostty). `git diff --stat v3.8.3 HEAD -- config/foot config/kitty config/ghostty` prints nothing.
- So the byte-identity claim holds whichever tag is meant. Only the label needs qualifying.
- Advice to L1: "omarchy version file 3.8.3; checkout HEAD is tag v3.8.4; terminal defaults identical at both."

### M3. "L1 re-ran these at 2026-10-22T11:55Z" has no receipt (unverifiable)

- `_grep` for `3e88354476f2682e|8afc9646c61e58e6|f875291ecfe64ebc|95eed20aaedb0962|cb828c044b07d4fd|e47630125605cb19|11:55Z|2026-10-22T11:55` across `.ufo/waves/round-23` (gitignore off) found the six hash prefixes in the wave-1 host reports (HostFoot, HostKitty, HostGhostty, SrcFoot, SrcGhostty, ScoutSkillTerminal). All agree with my values.
- The only matches for `11:55Z` or `2026-10-22T11:55` in the round-23 tree are `w2-record.json` `"updatedAt": "2026-10-22T11:55:13.347Z"` (a registry update, not a host run) and `w1/reports/ConnSibling.md` "Addendum 3 (2026-10-22 ~11:55Z, C3 landed)".
- The values reproduce at 11:57-12:01Z, so the content is right. The timestamp has no receipt behind it.
- Advice to L1: cite a receipt path for the host re-run, or drop the time.

### O1. Omission, not an error: the same 19:02:29 pass also wrote the Alacritty tree

- `~/.config/alacritty/alacritty.toml.bak.20261003-190229` (873 B) sha256 `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a`. This equals `~/.local/share/omarchy/config/alacritty/alacritty.toml` (same sha256).
- `~/.config/alacritty/alacritty.toml` (876 B) sha256 `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8`. `diff` default to live: one hunk, `13c13`, `size = 9` to `size = 12.5`.
- Both files have mtime and ctime `2026-10-03 19:02:29.838995642 -0300`. That is one millisecond before the foot and kitty stamps (`.839995618`) and the ghostty stamp (`.840995595`).
- This supports the note's `[INFERENCE] one scripted pass` across four trees. The note scopes Alacritty out, so this is optional corroboration, not a correction.

### O2. Method caveat: `ps` in this shell is a builtin

- `type -a ps` prints `ps is a shell builtin` then `ps is /usr/bin/ps`. The builtin rejects `-C` (`ps: unsupported option '-C'`).
- `/usr/bin/ps -C foot,kitty,ghostty -o pid=,comm=` exits 1 with no output. A repeat of the process check using bare `ps` gives a false error. The note names no process command. `/proc` and `/usr/bin/ps` both show no terminal process.

### O3. Other observations (no effect on note values)

- `~/.config/xdg-terminals.list` is 127 B, mtime `2026-10-03 17:44:32.097678467 -0300`. That is before the 19:02:29 pass. `/etc/xdg/xdg-terminals.list` does not exist (`ls` exit 2), so no competing list.
- Each of `~/.config/{foot,kitty,ghostty}` holds exactly the two declared files, with no hidden or extra entries.
- The omarchy checkout's `.git` root has mtime `2026-10-22 08:03:58.173569259 -0300`. `FETCH_HEAD`, `ORIG_HEAD`, and `config` are dated `2026-10-20 09:49:22 -0300`, and `packed-refs` is dated `2026-10-20 09:14:47 -0300`. The HEAD reflog has one entry only: `HEAD@{2026-07-21 00:09:35 +0000}: clone`. The `.git` root stamp predates my first git call in this session. I did not cause it and did not investigate further.
- The first `hyprctl` attempt from the eval kernel returned rc 1 with no output, because that kernel lacks the Hyprland instance variable. The re-run with the session's signature succeeded (instance directory `/run/user/1000/hypr/` exists).
- Two `/proc` entries (pids 3313542 and 3313546) vanished mid-scan (`FileNotFoundError`). Both were transient. Neither scan matched a terminal name.

## Full re-derivation table

Note values are from `terminal-trees-r23.md`. Observed values are from this session.

| # | Note claim | Observed | Result |
|---|---|---|---|
| A1 | `~/.config/foot/foot.ini`, 516 B, sha256 `3e88354476f2682e…` | 516 B; `3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60` | match |
| A2 | `~/.config/foot/foot.ini.bak.20261003-190229`, 513 B, `8afc9646c61e58e6…` | 513 B; `8afc9646c61e58e67f244e50a9ce5d4a45546920511a06b47f7443a3998da602` | match |
| A3 | `~/.config/kitty/kitty.conf`, 954 B, `f875291ecfe64ebc…` | 954 B; `f875291ecfe64ebc4ddc588282bcdb20fb883769e9938148411efa378d7f1e70` | match |
| A4 | `~/.config/kitty/kitty.conf.bak.20261003-190229`, 953 B, `95eed20aaedb0962…` | 953 B; `95eed20aaedb09627e00e3ff504919b585a54799aa41cb45bba5e17b91c8dd44` | match |
| A5 | `~/.config/ghostty/config`, 1325 B, `cb828c044b07d4fd…` | 1325 B; `cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667` | match |
| A6 | `~/.config/ghostty/config.bak.20261003-190229`, 1322 B, `e47630125605cb19…` | 1322 B; `e47630125605cb19c6b2c9bc33d767a0f3f1b5bf04cd4f36a2bb910897e24f78` | match |
| B1 | foot backup byte-identical to omarchy default | `~/.local/share/omarchy/config/foot/foot.ini` 513 B, same sha256 `8afc9646…`; `diff` exit 0 | match |
| B2 | kitty backup byte-identical to omarchy default | `config/kitty/kitty.conf` 953 B, same sha256 `95eed20a…`; `diff` exit 0 | match |
| B3 | ghostty backup byte-identical to omarchy default ("omarchy 3.8.3 checkout") | `config/ghostty/config` 1322 B, same sha256 `e4763012…`; `diff` exit 0 | match in bytes; label caveat M2 |
| C1 | foot live differs by one font line | one hunk `4c4`: `font=JetBrainsMono Nerd Font:size=9` to `…size=12.5`; live vs backup shows the same single hunk | match |
| C2 | kitty live differs in `font_size` | one hunk `6c6`: `font_size        9.0` to `font_size        12.5` | match |
| C3 | ghostty live differs only in `font-size` | one hunk `7c7`: `font-size = 9` to `font-size = 12.5` | match |
| D1 | foot: no binary on PATH | `command -v foot` exit 1, no output | match |
| D2 | foot: `pacman -Q foot` not found | `error: package 'foot' was not found`, exit 1 | match |
| D3 | foot: no process | no `comm` or `cmdline` match in `/proc` (2403 pids); `/usr/bin/ps -C` exit 1 | match |
| D4 | kitty: no binary on PATH | `command -v kitty` exit 1; `kitten` exit 1 | match |
| D5 | kitty: `pacman -Q kitty` not found | `error: package 'kitty' was not found`, exit 1 | match |
| D6 | kitty: no process | none | match |
| D7 | ghostty: no binary on PATH | `command -v ghostty` exit 1 | match |
| D8 | ghostty: `pacman -Q ghostty` not found | `error: package 'ghostty' was not found`, exit 1 | match |
| D9 | ghostty: no process | none | match |
| E1 | all three backups and font edits share one timestamp, 2026-10-03 19:02:29 | all six files: mtime = ctime = `2026-10-03 19:02:29 -0300` (epoch 1791064949); nanoseconds `.839995618` (foot, kitty), `.840995595` (ghostty) | match |
| F1 | `~/.config/xdg-terminals.list` names only `Alacritty.desktop` | 127 B; only non-comment line is line 3, `Alacritty.desktop` | match |
| F2 | live clients are Alacritty | hyprctl class set `{Alacritty}` in both reads | match |
| F3 | "2 Alacritty clients" | 1 client (pid 2487) in read 1 (after 11:57:24Z) and read 2 (12:00:32Z) | MISMATCH (M1) |
| G1 | `command -v foot kitty ghostty` exit 1, nothing found | exit 1, no output | match |
| G2 | `pacman -Q foot kitty ghostty` gives three "not found" | three `error: package '…' was not found` lines, exit 1 | match |
| G3 | `grep -v '^#' ~/.config/xdg-terminals.list` gives `Alacritty.desktop` | `_grep` with pattern `^[^#]` returns line 3 only; file has no blank lines, so this is equivalent | match |
| H1 | "L1 re-ran these at 2026-10-22T11:55Z with the values above" | no receipt bearing that time; values reproduce at 11:57-12:01Z | UNVERIFIABLE (M3) |

The `sha256sum` and `stat -c '%n %s'` bullet in Safe observation is covered by rows A1-A6. The re-hash at about 12:00Z was identical to the first pass.

Extra checks, not in the note (informational):

- X1: Alacritty pair, see O1.
- X2: full `pacman -Q` list (1399 entries) filtered on `foot|kitty|ghostty|alacritty`. Only `alacritty 0.17.0-1` matches. No alternate-named package for the three.
- X3: `/etc/xdg/xdg-terminals.list` absent.

## Commands run (all read-only)

Shell:

1. `sha256sum` on `/home/vgpnk/.config/{foot/foot.ini,foot/foot.ini.bak.20261003-190229,kitty/kitty.conf,kitty/kitty.conf.bak.20261003-190229,ghostty/config,ghostty/config.bak.20261003-190229}`. Repeated at about 12:00Z.
2. `stat -c '%n | size=%s | mtime=%y | ctime=%z | owner=%U:%G | mode=%a | type=%F'` on the six files. `stat -c '%n | size=%s | ctime_epoch=%Z | mtime_epoch=%Y'` on the six plus the three omarchy defaults.
3. `ls -la --time-style=full-iso` on `~/.config/foot`, `~/.config/kitty`, `~/.config/ghostty`, `~/.config/alacritty`, `~/.local/share/omarchy/config/{foot,kitty,ghostty}`, `~/.local/share/omarchy`, and `/etc/xdg/xdg-terminals.list`.
4. `sha256sum /home/vgpnk/.local/share/omarchy/config/foot/foot.ini /home/vgpnk/.local/share/omarchy/config/kitty/kitty.conf /home/vgpnk/.local/share/omarchy/config/ghostty/config`.
5. `diff <omarchy default> <backup>` for each of the three (exit 0). `diff <backup> <live>` for each (exit 1, one hunk). `diff <omarchy default> <live>` for each (exit 1, same hunks). Also `diff` for Alacritty default vs live (exit 1, line 13).
6. `command -v foot`, `command -v kitty`, `command -v ghostty`, `command -v kitten`, `command -v footclient` (each exit 1). `command -v foot kitty ghostty` (exit 1, no output). `type -a ps`.
7. `pacman -Q foot kitty ghostty` (exit 1, three not-found errors).
8. `/usr/bin/ps -C foot,kitty,ghostty -o pid=,comm=` (exit 1, no output).
9. `sha256sum` on `~/.config/alacritty/alacritty.toml.bak.20261003-190229`, `~/.config/alacritty/alacritty.toml`, and `~/.local/share/omarchy/config/alacritty/alacritty.toml`.
10. `date -u +%Y-%m-%dT%H:%M:%SZ` (returned 11:57:24Z and 12:01:16Z).
11. Omarchy checkout, `git --no-optional-locks -C /home/vgpnk/.local/share/omarchy …`: `describe --tags --always` (`v3.8.4`); `log -1 --format='%H %cI %s'`; `show HEAD:version` and `show v3.8.3:version` (both `3.8.3`); `for-each-ref --format=… refs/tags/v3.8.3 refs/tags/v3.8.4`; `status --porcelain=v1` (empty); `reflog -n 6 --date=iso` (one clone entry); `rev-parse --verify -q v3.8.3^{commit}`; `diff --stat v3.8.3 HEAD -- config/foot config/kitty config/ghostty` (empty); `ls -la --time-style=full-iso .git`.

Read and search tools:

12. `read ~/.config/xdg-terminals.list` (three lines). `_grep` with pattern `^[^#]` on the same path (line 3 only).
13. `_grep` for the six hash prefixes and `11:55Z|2026-10-22T11:55` across `.ufo/waves/round-23`, with gitignore off. Hits are cited in M3.
14. `read …/w1/reports/HostGhostty.md:1-30` and `_grep` for `Alacritty|clients|hyprctl` in the same file, for the client claim in M1.

Python standard library, via eval, read-only:

15. `subprocess.run(["hyprctl","-j","clients"])` and `["hyprctl","-j","workspaces"]`, with `HYPRLAND_INSTANCE_SIGNATURE` set to the session value and `XDG_RUNTIME_DIR=/run/user/1000`. The JSON was parsed and only class, pid, workspace, and state fields were printed.
16. `/proc` scan: read `/proc/<pid>/comm` for each pid, and `cmdline` for non-matching comm. Match `foot|kitty|kitten|ghostty` (and list `alacritty` separately). Printed only pid, comm, and matched token. The first scan also printed the Alacritty command line (`alacritty --working-directory=/home/vgpnk`).
17. `subprocess.run(["pacman","-Q"])` with regex filter `foot|kitty|ghostty|alacritty`. Also `git show <rev>:<path>` for `v3.8.3` and `HEAD` on the three terminal default files, hashed with `hashlib` (read-only).

## Verdict

VERDICT: 27 of 29 note claims reproduce exactly (row B3 reproduces in bytes but carries the M2 label caveat). 1 mismatch: M1, live Alacritty client count, note says 2, observed 1 at two reads (after 11:57:24Z and at 12:00:32Z). 1 unverifiable: M3, the L1 re-run at 2026-10-22T11:55Z has no receipt. No host state was changed.
