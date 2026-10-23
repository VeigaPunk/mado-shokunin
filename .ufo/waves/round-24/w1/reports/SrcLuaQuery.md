# C1 source opener: Lua query bindings

## Finding

**Observation (source bytes, `LuaBindingsQuery.cpp:62-123,392-411`):** `hl.get_windows` accepts a table of filters. Its parser reads monitor, workspace, floating, mapped, class, title, and tag fields; `mapped` defaults to true. A matching window with a requested tag is rejected if it has no rule applicator or the tag-keeper check is false. Passing windows are pushed as `CLuaWindow` objects. The query-binding registration block lists the query functions, including `get_windows`, `get_window`, and `get_layers`.

**Scope-limited negative observation:** The complete registration block in this file has no function named for `getprop`, properties, rules, or matched rules. The tag check is in the query predicate, not a result identifying a matched rule.

**Inference:** This source supports selecting windows by tag (and other filter fields); it does not show which rule produced a tag, which rule matched, or which effect was applied. The returned `CLuaWindow` wrapper may expose other values through bindings outside this file; this opener did not inspect those bindings. This is not evidence of host runtime behavior. Host behavior remains [UNK].

## Provenance and exact work

Pinned source: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsQuery.cpp` (Hyprland v0.56.2, pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f`).

Fetched with:

```text
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsQuery.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin
```

Observed output: `af0d274b5616ae69b8f62bdf2534a29586eab2a3d20b28c1b0e620d313ca66db  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin`; `12451 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin`.

Source anchors: `62-65` (tag predicate), `83-123` (query fields, default, matching and wrapping), and `392-411` (registered query functions).

Sweep command (read-only search over the complete fetched file): `functions.grep(pattern="Internal::setFn\\(L,|m_ruleApplicator|m_tagKeeper|isTagged|getprop|matched.?rules?|rule.?matches?", path="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin", case=false, gitignore=false, skip=0)`. Output: tag predicate at lines 62-65; registration lines 392-411 list `get_windows`, `get_window`, `get_active_window`, `get_urgent_window`, `get_workspaces`, `get_workspace`, `get_active_workspace`, `get_active_special_workspace`, `get_monitors`, `get_monitor`, `get_active_monitor`, `get_monitor_at`, `get_monitor_at_cursor`, `get_layers`, `get_workspace_windows`, `get_cursor_pos`, `get_last_window`, `get_last_workspace`, and `get_current_submap`. No other lines matched the searched terms.

Quote check for claim A1: `timeout 10s python3 -I -c 'import pathlib,re,sys; text=pathlib.Path(sys.argv[1]).read_bytes().decode("utf-8"); collapse=lambda s: re.sub(r"\s+", " ", s).strip(); q="query.className = Internal::tableOptStr(L, idx, \"class\"); query.title = Internal::tableOptStr(L, idx, \"title\"); query.tag = Internal::tableOptStr(L, idx, \"tag\");"; print(collapse(q) in collapse(text), len(collapse(q).split()))' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin` produced `True 15`.

Quote check for claim A2: `timeout 10s python3 -I -c 'import pathlib,re,sys; text=pathlib.Path(sys.argv[1]).read_bytes().decode("utf-8"); collapse=lambda s: re.sub(r"\s+", " ", s).strip(); q="if (!w->m_ruleApplicator || !w->m_ruleApplicator->m_tagKeeper.isTagged(*query.tag, true)) return false;"; q=collapse(q); print(q in collapse(text), len(q.split()))' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin` produced `True 7`. Both quotes are whitespace-collapsed substrings of the fetched UTF-8 bytes; each is under 25 words and contains the topic word `tag`.

## Proposed claim rows

| A1 | The parser reads `query.className` plus title and tag as string values from the window-query table. | S? | "query.className = Internal::tableOptStr(L, idx, "class"); query.title = Internal::tableOptStr(L, idx, "title"); query.tag = Internal::tableOptStr(L, idx, "tag");" |
| A2 | The tag filter rejects a window if no rule applicator exists or its `m_tagKeeper` check is false. | S? | "if (!w->m_ruleApplicator || !w->m_ruleApplicator->m_tagKeeper.isTagged(*query.tag, true)) return false;" |

## Proposed SOURCES row

| S? | Lua query bindings — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsQuery.cpp | code | A | Lua window query filters and query-binding registrations | src/config/lua/bindings/LuaBindingsQuery.cpp:62-65,83-123,392-411 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:af0d274b5616ae69b8f62bdf2534a29586eab2a3d20b28c1b0e620d313ca66db, 12451 B | `get_windows` filter inputs and tag-match behavior; no matched-rule result is listed in this file's query bindings | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Scope and verdict

Affected files: created the required fetched-byte receipt `.ufo/waves/round-24/fetch/w1/SrcLuaQuery-1.bin` and this report `.ufo/waves/round-24/w1/reports/SrcLuaQuery.md`. No product or corpus file was changed. No packages or tools were installed. No tests, runtime checks, or host-state commands were run. C2 is out of scope.

**Verdict:** usable C1 source evidence for window tag/property filtering; this file does not evidence rule-to-effect attribution or runtime host behavior. `S?` is provisional for the integration owner to assign.