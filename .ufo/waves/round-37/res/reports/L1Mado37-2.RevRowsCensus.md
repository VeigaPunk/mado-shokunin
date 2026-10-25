# L1Mado37-2.RevRowsCensus — SOURCES.md registry change review (3f42425)

Reviewed `corpus/SOURCES.md` change from base `b4e47e980bfb0cbc8a4e788f59a41db858751fd8` to data commit `3f424257a1ea69cd2655770259ba00b423293f4f`. The lane worktree matches the commit for `corpus/SOURCES.md` (`git diff 3f42425 -- corpus/SOURCES.md` empty; `HEAD` = 3f42425), so all checks ran against the committed content.

## 1. Diff shape — PASS

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff b4e47e980bfb0cbc8a4e788f59a41db858751fd8 3f424257a1ea69cd2655770259ba00b423293f4f --stat
corpus/SOURCES.md | 10 ++++++++--
1 file changed, 8 insertions(+), 2 deletions(-)
```

Cell-level diff (per-cell comparison of both revisions of the file, 11 cells per row):
- added ids: `S212, S213, S214, S215, S216, S217` (six appended rows)
- removed ids: none
- changed ids: `S189, S201`, and only their used-by cell changed:
  - S189 used-by: `corpus/knowledge/ipc-contract-r25.md` → `corpus/knowledge/ipc-contract-r25.md, corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md`
  - S201 used-by: `corpus/knowledge/waybar-module-text-route-r25.md` → `corpus/knowledge/waybar-module-text-route-r25.md, corpus/knowledge/event-delivery-limits-r26.md`

Exactly six appended rows and two used-by extensions; nothing else touched.

## 2. Row shape — PASS

Every reviewed row (`S189, S201, S212–S217`) parses to exactly 11 cells: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by.

## 3. Enums (kind/tier/status) — PASS

- kind (`^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$`): `code` (S189, S201, S212, S214, S215, S216, S217), `own-work` (S213).
- tier (`^[ABC]$`): `A` for all eight.
- status (`^(queued|mined|rejected)$`): `mined` for all eight.

No E05/E06/E07 emitted by the census (below).

## 4. recheck — PASS

Bare cadence tokens, no decoration: `90d` (S189, S201, S212, S214, S215, S216, S217), `on-change` (S213). No E09 emitted.

## 5. used-by paths exist and cite the row — PASS

No E11 (dangling used-by) emitted; all four cited knowledge files exist at the commit and cite their rows:

| file (at 3f42425) | cites |
| --- | --- |
| `corpus/knowledge/ipc-contract-r25.md` | S189 (lines 11, 27, 62–68) |
| `corpus/knowledge/event-delivery-limits-r26.md` | S189 (3, 14–39), S201 (3, 44–60), S212 (3, 44, 46) |
| `corpus/knowledge/event-queue-observability-r37.md` | S189 (15, 70), S213 (3, 37, 43, 47, 51, 63), S214 (3, 28, 51, 63), S215 (3, 21, 63), S216 (3, 33), S217 (3, 24, 51) |
| `corpus/knowledge/waybar-module-text-route-r25.md` | S201 (7, 12, 18) |

## 6. Anchors match the fetched bytes — PASS

sha256 prefixes of the committed `fetch/` files (via `git show 3f42425:…`) vs the row claims, and every cited anchor line verified in the fetched bytes:

| row | fetch file | sha256 prefix (computed) | claim | bytes |
| --- | --- | --- | --- | --- |
| S189 | S189.bin | `eea605dfe5ce09e1` | `eea605dfe5ce09e1` | 6479 ✓ |
| S201 | S201.bin | `799bf02f6d18ae04` | `799bf02f6d18ae04` | 6550 ✓ |
| S212 | S212.bin | `1e19d92638e7923f` | `1e19d92638e7923f` | 41392 ✓ |
| S213 | S213.receipt.txt | `1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58` (full) | same full hash | 1814 ✓ |
| S214 | S214.bin | `d04e3a2fe5c73ad8` | `d04e3a2fe5c73ad8` | 1789 ✓ |
| S215 | S215.bin | `a76f05079454e1f6` | `a76f05079454e1f6` | 59222 ✓ |
| S216 | S216.bin | `74833ecbf0e2b6f8` | `74833ecbf0e2b6f8` | 38550 ✓ |
| S217 | S217.bin | `aeb07ba1ba1fd5cf` | `aeb07ba1ba1fd5cf` | 1767 ✓ |

Anchor-line checks inside the fetched bytes:
- S189 `EventManager.cpp`: `:14` AF_UNIX SOCK_STREAM, `:21` `.socket2.sock`, `:35` `listen(..., 10)`, `:126` `formatEvent`, `:128` `data.substr(0, 1024)`, `:129` `'\n'`→`' '` ✓
- S201 `backend.cpp:38` `$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr` ✓
- S212 `workspaces.cpp`: `:803` `registerIpc`, `:804-815` twelve unconditional `registerForIPC` calls, `:817-821` `windowtitlev2` only when rewrite rule/taskbar uses title ✓
- S213 receipt: sections `session log` (line 4), `compositor unit journal` (19), `live options` (27) present ✓
- S214 `Logger.cpp`: `:14-16` `log` returns when `!m_logsEnabled`; `:21-24` rolling-log follower/file write after that return; `:37` `config.reloaded` listener → `recheckCfg`; `:42` reads `debug:disable_logs`; `:48` `m_logsEnabled = !*PDISABLELOGS` ✓
- S215 `ConfigValues.cpp`: `:629` `debug:disable_logs ... true`; `:632` `debug:enable_stdout_logs ... false` ✓
- S216 `Compositor.cpp`: `:298` `Log::logger->initCallbacks()`; `:304-307` aquamarine `CLoggerConnection` ✓
- S217 `Logger.hpp`: `:20-33` template `log` overload returns while `!m_logsEnabled`; `:42` `m_logsEnabled = true` ✓

## 7. Census validation — PASS (exit 0)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
EXIT=0
```

The seven W04 duplicate-url warnings are pre-existing: the identical set is reproduced at base `b4e47e9` in a sandbox clone (`sources-census.sh validate --root /dev/shm/…/base-fleet mado` → same seven W04, `mado ok …`, exit 0). None of the changed/new row ids appear in the warning set. No E05–E11 findings for the new/changed rows.

## Verdict

All review items PASS; no findings. Residual: the pre-existing W04 duplicate-url warnings are outside this change's scope.
