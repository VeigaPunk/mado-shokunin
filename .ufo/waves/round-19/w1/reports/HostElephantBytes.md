# HostElephantBytes — host elephant bytes carry 2.22.1 (pkg 2.22.1-1); three knowledge notes still state 2.21.0

Read-only byte read of `/usr/bin/elephant`, its pacman metadata, and the pacman
log. Nothing was executed: no `elephant`, no `pacman`, no process probe.

## 1. Binary identity — /usr/bin/elephant

| Field | Value | Evidence |
|---|---|---|
| size | 23,460,760 B | `stat -c '%n %s %y %A'` |
| sha256 | `b0761ff7b7cc8d211693b2b691e44d12aef2745e304c8b38f1c35bd71b5cc8ea` | `sha256sum /usr/bin/elephant` |
| mtime | 2026-10-20 09:29:41 -0300 = 2026-10-20T12:29:41Z | `stat` |
| mode/owner | 755 `-rwxr-xr-x`, `root:root` | `ls -l` |
| format | ELF 64-bit LSB executable, x86-64, dynamically linked, stripped; GNU BuildID `690f855fa5bd8c5451de22a65d40df7cc94de35a` | `file`; `readelf -n` (`.note.gnu.build-id`) |

## 2. Compiled-in version literals (byte scan, no execution)

Python `open('/usr/bin/elephant','rb')`, regex `(?<![\d.])2\.\d{1,2}\.\d{1,2}(?![\d.])`:

- `2.22.1` — **exactly 1 occurrence**, at byte offset 13,132,144:
  `... disable version install systemd startup [%[1]s] integer boolean 2.22.1 \n nil ...`
  (context shows the literal immediately after the `version` token in the string blob; the nearest `2.x.y` neighbours otherwise are crate versions 2.0.2/2.4.3/etc.).
- `2.21.0` — **0 occurrences**.
- `v2.22.1` — 0 occurrences; Go buildinfo main-module line is
  `mod github.com/abenz1267/elephant/v2 (devel)` (buildinfo magic at offset 23,061,280; `go1.27.2-X:nodwarf5`; main path `github.com/abenz1267/elephant/v2/cmd/elephant`).

[INFERENCE] With the module stamped `(devel)`, the `2.22.1` string is the
ldflags-injected runtime version of this build, not a module-toolchain stamp;
its adjacency to the `version` token supports that reading. This is still a
static-byte claim, not a `--version` execution claim.

## 3. Package metadata

`/var/lib/pacman/local/elephant-2.22.1-1/desc` (file bytes):

```
%NAME% elephant
%VERSION% 2.22.1-1
%BASE% elephant
%URL% https://github.com/abenz1267/elephant
%BUILDDATE% 1792499381   -> 2026-10-20T12:29:41Z  (== binary mtime)
%INSTALLDATE% 1792499463 -> 2026-10-20T12:31:03Z
%SIZE% 23495909
%REASON% 1
%VALIDATION% none
```

`%SIZE%` corroborates the payload: `du -cb /usr/bin/elephant /usr/share/licenses/elephant/LICENSE`
= 23,460,760 + 35,149 = **23,495,909 B** total. `files` lists only
`usr/bin/elephant` and that LICENSE (7 `usr/` lines); provider plugins are the
separate `elephant-*` packages, whose local desc dirs (all `2.22.1-1`) agree.
The 12 `/usr/lib/elephant/*.so` files are mtime 2026-10-20 09:29–09:31.

## 4. pacman log (read as file bytes)

- `/var/log/pacman.log:1096` — `[2026-10-03T17:44:26-0300] [ALPM] installed elephant (2.21.0-1)` (the round-5 pin).
- `/var/log/pacman.log:3092` — `pacman -U ... /home/vgpnk/.cache/yay/elephant/elephant-2.22.1-1-x86_64.pkg.tar.zst ... elephant-debug-2.22.1-1 ...` (2026-10-20T09:31:03-0300).
- `/var/log/pacman.log:3095` — `[2026-10-20T09:31:03-0300] [ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)`; provider packages upgraded at `:3097-3120`.
- `/var/log/pacman.log:3123` — `running 'walker-restart.hook'`; debug packages removed at `:3132-3147`.

## 5. Notes under corpus/knowledge that state an elephant version

| Note:line | Stated | vs host bytes |
|---|---|---|
| `walker-deep.md:28` | `elephant version` → `2.21.0`; pkg `2.21.0-1` (2026-10-14 snapshot) | **DISAGREES** with the installed bytes (2.22.1); dated pin |
| `waybar-walker-semantics.md:24` | pkg `2.21.0-1` | **DISAGREES**; same note `:469` already says S090 records `2.21.0-1 -> 2.22.1-1` |
| `walker-live-surface.md:298-299` | “Elephant version/identity was not re-measured … round-5 §1 pins it at 2.21.0” | **DISAGREES** as a current-host pointer (stale by reference) |
| `walker-deep-r9.md:63` | elephant version “**not** re-measured — round-7 §8.4 stands” (i.e. 2.21.0 by reference) | **DISAGREES** as a current-host value; correctly labels itself unmeasured |
| `walker-route-r18.md:228-229, 245-246` | host now carries `2.22.1-1`; notes describe the old `2.21.0` round-5 pin | **AGREES** with bytes and pkg |
| `waybar-walker-plane.md:469, 481` | elephant `2.21.0` → `2.22.1` per S090; “not pinned in this note” | **AGREES** (records the supersession, not a live pin) |
| `arc-synthesis.md:229` | walker 2.17.0 row only; no elephant version | n/a |

Corpus-level corroboration: `corpus/SOURCES.md:102` (S090) asserts host elephant
`2.21.0-1 -> 2.22.1-1` at `pacman.log:3095`; `SOURCES.md:92-95` (S080-S083) are
pinned to upstream tag `v2.22.1`, matching the installed package version.

**Net:** host bytes and package metadata are internally consistent at
**elephant 2.22.1-1**; the only disagreeing knowledge text is the round-5
`2.21.0` pin and its by-reference restatements, all of which post-date as
“host was 2.21.0 then”. No edit made (input for a later freshness round).

## Limits

- Running-process version is **[UNK]**: no `pgrep`/`systemctl`/`elephant` probe
  was run (host pause). The restart hook at `pacman.log:3123` and
  `omarchy-restart-walker` semantics make a post-upgrade elephant restart
  plausible but unverified (`[INFERENCE]`, log line ≠ running binary).
- Only `/usr/bin/elephant` was byte-scanned; the 12 provider `.so` files were
  listed by size/mtime but not scanned for their own version literals.
- The `2.22.1` literal is a static string; no `--version` output was executed.
- No upstream source was fetched this pass; tag↔commit evidence for v2.22.1 is
  S080-S083/S090 as already recorded, not re-derived here.
- pacman/`expac` queries were not run (host pause); only `desc`/`files` reads.

## Installs

none
