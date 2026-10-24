
# The dispatcher surface on the host's release line, and how the request socket resolves a dispatcher

Lane: mado-shokunin. Round: corpus-expansion-2, round 2; re-grounded round 32, wave 1. Substrates READ-ONLY: two upstream pages were re-fetched this round; no dispatcher was executed and no socket was connected.

source: S196 — https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/ — `§ General` — 0.56.0 docs revision, page footer "Last updated on July 15, 2026"
verified-at: 2026-10-24
recheck: on-compositor-release — re-fetch the 0.56.0 page and re-diff the dispatcher list (sha256 of 2026-10-24 fetch: `f9b51362f2440e02…`, 297,863 bytes)
ground: F1 — "dispatcher behavior" in arc-synthesis §6 U1

### §1 The version-matched surface exists, at a different path than the queue guessed

**OBS** The queue's guessed URL
`https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/`
answers **404** (re-checked 2026-10-24); the real path for the 0.56.0 docs is
`/0.56.0/Configuring/Basics/Dispatchers/` (S196), and it is linked from the
0.56.0 wiki's own navigation sidebar.

**OBS** The 0.56.0 page documents the dispatcher surface as a Lua API —
`hl.dsp.` — the same family the current-git page documents (S188). Its
dispatcher table includes (S196, `§ General`):

> "exec_cmd(cmd, rules?)"

> "dpms({ action?, monitor? })"

> "event(string)"

**OBS** The full dispatcher *name* set on the 0.56.0 page, extracted from its
five tables (S196, §§ General/Window/Workspace/Group/Cursor), is 45 distinct
names: `active`, `alter_zorder`, `center`, `clear_tags`, `close`, `cycle_next`,
`deny_from_group`, `dpms`, `drag`, `event`, `exec_cmd`, `exec_raw`, `exit`,
`float`, `focus`, `force_idle`, `force_renderer_reload`, `fullscreen`,
`fullscreen_state`, `global`, `kill`, `layout`, `lock`, `lock_active`, `move`,
`move_to_corner`, `move_window`, `next`, `no_op`, `pass`, `pin`, `prev`,
`pseudo`, `release_input_capture`, `rename`, `resize`, `send_key_state`,
`send_shortcut`, `set_prop`, `signal`, `submap`, `swap`, `swap_monitors`,
`tag`, `toggle`, `toggle_special`, `toggle_swallow`.

**OBS** A keyword presence check over both re-opened pages finds `force_idle`,
`dpms`, `event`, `exec_cmd`, `pass`, `fullscreen` and `exit` documented on
**both** the 0.56.0 page (S196) and the current-git page (S188). The staged
draft also listed `exec`; that is wrong name-by-name: on the 0.56.0 page
`exec` appears only inside keybind-syntax guidance (`exec, uwsm stop`) and on
the current page not at all — neither page lists an `exec` dispatcher row.

**OBS** The name sets are **not** identical across the two pages: the
current-git page (S188) carries `reload_config`, which the 0.56.0 page (S196)
does not. Signature rendering also drifted — current-git rows lead with
`window?` (e.g. `fullscreen({ window?, action?, mode?, layout_aware? })` vs
0.56.0's `fullscreen({ mode?, action?, layout_aware?, window? })`), and
0.56.0 lists `resize()` as a separate row where current-git folds it into
`resize({ keep_aspect_ratio? })`. Name-set: 45 (0.56.0) vs 46 (current).

**INF** The dispatcher *name* set is therefore almost stable across the
release line, but "same dispatcher vocabulary" overstates it: `reload_config`
is a post-0.56 addition and `exec` was never a documented dispatcher name on
either page. The frontier's "dispatcher behavior" still needs no version
caveat for the shared names; the delta is one added name and signature-order
drift. Basis: the two pages' extracted name sets.

### §2 How the request socket resolves a dispatcher on the host's version

The claims in this section are attributed to S018 (the tagged
`src/debug/HyprCtl.cpp` at commit `efb50993780079460b0cbed1363e2166a2de1d9f`
for v0.56.2). **S018 was not re-opened in round 32**; these claims carry the
staging campaign's 2026-10-23 read, unchanged, and should be re-verified
before this entry's next edit.

**OBS** The request path is a function per dispatcher family —
`dispatchRequest`, `dispatchKeyword`, `dispatchBatch`, `dispatchGetProp`,
`dispatchSetCursor`, `dispatchPlugin`, `dispatchNotify` — and the dispatcher
*name* is resolved against the keybind manager's registry, not parsed as a
free-form command (S018 file, `:1149`):

> `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);`

**OBS** An unknown name is rejected with a fixed string (S018 file, `:1151`):

> `return "Invalid dispatcher";`

**OBS** The batch form splits on `;` while ignoring semicolons inside brackets
(S018 file, `:1309`):

> `// split by ; ignores ; inside [] and adds ; on last command`

**OBS** Before the dispatcher name is compared, the server strips a leading
flag segment and its separator (S018 file, `:2096`):

> `request = request.substr(sepIndex + 1); // remove flags and separator so we can compare the rest of the string`

**OBS** For Lua callers the request is wrapped rather than matched (S018 file,
`:1132`):

> `std::string evalStr = std::format("return hl.dispatch({})", in);`

**INF** `[flags]/command args` is therefore not a free-form command line: it
is an optional flag segment, a separator, a dispatcher *name* drawn from a
fixed registry, and an optional argument. A client that invents a dispatcher
name gets "Invalid dispatcher" rather than a shell. Basis: the S018
quotations above (not re-opened this round).

### §3 What remains unmeasured

**UNK** The per-flag semantics (the `j`/`r`/`a`/`c`/`f` prefixes) were not
enumerated: the S018 read shows flags being *stripped* before matching, and
the flag table itself lives in the client's own request construction. The
0.56.0 dispatcher page (S196) contains no flag documentation — `flags` has
zero occurrences in its bytes.

**UNK** Whether the host's own configuration uses any flag prefix was not
inspected (the host's Hyprland configuration is read-only for this lane and
was not read this round).

**UNK** The `reload_config` addition is dated to the current-git page only;
which release first shipped it is not pinned by either fetched page.

## Gate

- **S196 URL:** https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/
- **Access date:** 2026-10-24 (HTTP 200; 297,863 bytes; sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`).
- **Located quote (15 words):** "hl.dsp. contains: method description exec_cmd(cmd, rules?) execute a command." — `§ General`, table head and first row.
- **Second located quote (8 words):** "Last updated on July 15, 2026" — page footer.
- **Guessed-URL check:** `https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/` → HTTP 404, re-fetched 2026-10-24.
