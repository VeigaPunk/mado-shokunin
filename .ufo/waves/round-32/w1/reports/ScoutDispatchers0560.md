# Scout report — S196 re-open: Hyprland 0.56.0 Dispatchers page

Round 32 · wave w1 · lane: mado-shokunin · fetch + verify (read-only network).

## Fetch record

- URL: `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/`
- Result: **fetch succeeded** — HTTP 200, `curl --fail`, exit 0.
- Effective URL: `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/` (no redirect).
- Saved to: `.ufo/waves/round-32/scratch/ScoutDispatchers0560/dispatchers-0.56.0.html`
- Byte length: **297,863 bytes**
- sha256: `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2` (prefix `f9b51362f2440e02`)
- Access date: **2026-10-24** (fetch completed 2026-10-24T23:03:46Z, UTC)
- Page revision / "last updated" string as rendered:
  `Last updated on <time datetime="2026-07-15T23:56:15.000Z">July 15, 2026</time>`
  → displayed text: **"Last updated on July 15, 2026"** (datetime `2026-07-15T23:56:15.000Z`).

## Does the page expose the `hl.dsp.*` Lua API?

**Yes.** The whole dispatcher surface on this page is published as the `hl.dsp.*`
Lua API. Page intro (first "Dispatchers" h2): dispatchers "return tables that
describe an action you want to make … Their purpose is to be fed into
`hl.bind()` or `hl.dispatch()`." Member references observed on the page:
`hl.dsp`, `hl.dsp.cursor.`, `hl.dsp.group.` (e.g. `hl.dsp.group.toggle()`),
`hl.dsp.window.`, `hl.dsp.workspace.` — plus `hl.bind` (5 hits) and
`hl.dispatch` (2 hits). There is **no** legacy `dispatcher args` command table
on this page; the dispatcher vocabulary is the union of the five `hl.dsp.*`
group tables below.

## Full dispatcher vocabulary as published — General section

The "General" h3 (anchor `#general`) is the first table under the second
"Dispatchers" h2, introduced as `hl.dsp.` + "contains:". All 21 rows:

1. `exec_cmd(cmd, rules?)`
2. `exec_raw(cmd)`
3. `focus({ direction })`
4. `focus({ monitor })`
5. `focus({ workspace, on_current_monitor? })`
6. `focus({ window })`
7. `focus({ urgent_or_last })`
8. `focus({ last })`
9. `exit()`
10. `submap(name)`
11. `pass({ window? })`
12. `send_shortcut({ mods, key, window? })`
13. `send_key_state({ mods, key, state, window? })`
14. `layout(message)`
15. `dpms({ action?, monitor? })`
16. `event(string)`
17. `global(string)`
18. `force_idle(seconds)`
19. `no_op()`
20. `force_renderer_reload()`
21. `release_input_capture()`

Sibling group tables on the same page (for completeness — `hl.dsp.window.`,
`hl.dsp.workspace.`, `hl.dsp.group.`, `hl.dsp.cursor.`):

- **Window** (30 methods): `close`, `kill`, `signal`, `float`, `fullscreen`,
  `fullscreen_state`, `pseudo`, `move` (7 overloads), `swap` (4 overloads),
  `center`, `cycle_next`, `tag`, `clear_tags`, `toggle_swallow`, `pin`,
  `alter_zorder`, `set_prop`, `deny_from_group`, `drag`, `resize` (3 overloads).
- **Workspace** (4): `rename`, `move`, `swap_monitors`, `toggle_special`.
- **Group** (7): `toggle`, `next`, `prev`, `active`, `move_window`, `lock`,
  `lock_active`.
- **Cursor** (2): `move_to_corner`, `move`.

Distinct dispatcher base names across all `hl.dsp.*` tables: 47. A `Focus`
section also lists `focus` variants (already covered by General's `focus`
rows); `set_prop` and `Fullscreenstate`/`FSMODE_MAX`/`Fullscreen Handlers`
sections document window properties and enum values, not new dispatcher names.

## Verification of staged entry

Staged: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`
(staged claims dated `verified-at: 2026-10-23`; this check: 2026-10-24).

### Item-by-item dispatcher list comparison

The staged entry does **not** enumerate the page's dispatcher list. Staged
sentences checked (verbatim):

> "Its dispatcher list includes (S196): "exec_cmd(cmd, rules?)" "dpms({
> action?, monitor? })" "event(string)""

> "A keyword presence check over both pages finds `force_idle`, `dpms`,
> `event`, `exec_cmd`, `pass`, `fullscreen`, `exit` and `exec` documented on
> **both** the 0.56.0 page and the current-git page."

Checking each staged name against the fetched page:

| Staged name | On page? | Where |
|---|---|---|
| `exec_cmd` | yes | General row 1 (as `exec_cmd(cmd, rules?)`) |
| `dpms` | yes | General row 15 |
| `event` | yes | General row 16 |
| `force_idle` | yes | General row 18 |
| `pass` | yes | General row 11 (as `pass({ window? })`) |
| `fullscreen` | yes | Window group — `hl.dsp.window.fullscreen` |
| `exit` | yes | General row 9 |
| `exec` | **no** | not a dispatcher name on the page; the two bare `exec` tokens appear only inside prose shell snippets ("use `exec, uwsm stop`…", "`exec, loginctl terminate-user`…"), which are keybind-syntax examples, not entries in any dispatcher table |

Page names absent from the staged list — General section: `exec_raw`, `focus`
(7 overloads), `submap`, `send_shortcut`, `send_key_state`, `layout`, `global`,
`no_op`, `force_renderer_reload`, `release_input_capture`. Plus all 43
non-General methods (`close`, `kill`, `move`, `swap`, `resize`, `rename`,
`toggle_special`, `lock`, `move_to_corner`, …).

### Verdicts

- **"list includes" the three quoted signatures — agree.** `exec_cmd(cmd,
  rules?)`, `dpms({ action?, monitor? })`, `event(string)` appear verbatim in
  the General table.
- **"Its dispatcher list" read as the page's list — disagree.** The page's
  General list has 21 rows; the staged entry names 3 and silently omits the
  other 18, so an item-by-item match fails (18 page names missing from the
  staged list; full union: 47 base names, 43 unstaged).
- **Keyword claim — partial disagree.** 7 of 8 staged keywords are present as
  dispatcher names on this page. `exec` is **not** published as a dispatcher
  name on the 0.56.0 page — the staged sentence claiming "`exec` documented on
  both" is not supported by this fetch.
- **Staged §1 OBS "publishes the Lua dispatcher API" — agree.** Page is
  entirely `hl.dsp.*` (consistent with staged §2's `hl.dispatch` quote from
  `HyprCtl.cpp`).

## Scratch artifacts

- `.ufo/waves/round-32/scratch/ScoutDispatchers0560/dispatchers-0.56.0.html` — raw HTML (297,863 B)
- `.ufo/waves/round-32/scratch/ScoutDispatchers0560/curl-stderr.txt` — empty (clean fetch)
