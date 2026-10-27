# S364–S369 — new registry rows (draft) for the C2 dispatcher-dispatch entry

seat: ScrRowsDispatch (round-51 w1, hyaku run 10) · date: 2026-10-27
claim: C2 (coverage, sourced) — `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`
lane base: `6ca8c559a4a3d6d361101592116eea2bc7452437`
revision of every row: Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2)

Status of this file: a **draft**. The rows are table-shaped so the L1 can paste them into
`corpus/SOURCES.md` unchanged; nothing here is committed and no tracked file was edited.

Pin root for these rows: `.ufo/waves/round-51/fetch/` (final path). The bytes were drafted in the
fetch seat's directory `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch/`, which holds all eight pins
(including `Hyprland-SharedDefs.hpp`, its pin #12 of 19); every quote below was verified against
**those** bytes, whose sha256 and byte size are recorded per row and in that directory's
`fetch-manifest.json`. Two pins are byte-equal to round-50 pins
(`Hyprland-KeybindManager.cpp`, `Hyprland-legacy-ConfigManager.cpp`; `cmp` output in §3d).

Rule 1 of the SOURCES contract ("a row is a claim … a ≤25-word quote with its location grounding
`teaches`") is discharged per row in §2; rule 4 ("expansion is knowledge, not rows") bounds the set:
only names a mechanism claim of the C2 entry needs are admitted, and the candidates that would have
grounded a documentation restatement, a held fact or a false grammar are rejected in §4.

## 1. Rows (paste-ready, 11 columns)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S364 | Hyprland 0.56.2 dispatcher map - population, declared type and the press-time call - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp | code | A | how a bind's stored handler name becomes a call: the 71-name population of m_dispatchers in the CKeybindManager constructor, the map's declared type, and the find plus call in handleKeybinds | Hyprland-KeybindManager.cpp:41-113 population, Hyprland-KeybindManager.cpp:602 handleKeybinds, Hyprland-KeybindManager.cpp:782 special-dispatcher list, Hyprland-KeybindManager.cpp:785 find, Hyprland-KeybindManager.cpp:798-812 miss branch and call with the mouse press-state prefix, Hyprland-KeybindManager.cpp:816-823 submap break and submap.reset, Hyprland-KeybindManager.cpp:835-842 success-to-found and passEvent; Hyprland-KeybindManager.hpp:137 map declaration, Hyprland-KeybindManager.hpp:41-42 handler and arg fields @ commit efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp 39334 B sha256:8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40; pin .ufo/waves/round-51/fetch/Hyprland-KeybindManager.hpp 7936 B sha256:cee22c13d413ab389803e0eb87a6fcefadedea885cee4457b56ae351228dd1e0 | a bind's handler is a key into one map filled at construction (71 names, the same set as the translator table) and is looked up and called at press with the stored arg; a submap handler sets found and breaks the remaining matched binds | mined | 2026-10-27 | on-release | corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |
| S365 | Hyprland 0.56.2 legacy dispatcher translator - the implementation table and per-dispatcher argument splitting - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp | code | A | how CDispatcherTranslator::run resolves a dispatcher name to its implementation, and how each implementation splits the single argument string it receives | Hyprland-legacy-DispatcherTranslator.cpp:30-35 run, Hyprland-legacy-DispatcherTranslator.cpp:797-867 m_dispMap (71 assignments, constructor at :796), Hyprland-legacy-DispatcherTranslator.cpp:835 alias focuswindowbyclass to focuswindow, Hyprland-legacy-DispatcherTranslator.cpp:839-840 submap and pass, Hyprland-legacy-DispatcherTranslator.cpp:861 inert accepted name, Hyprland-legacy-DispatcherTranslator.cpp:162 and :189 and :476 and :503 and :532 and :592 and :773 CVarList2 split sites; Hyprland-legacy-DispatcherTranslator.hpp:16-19 signature and map declaration @ commit efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp 35997 B sha256:7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771; pin .ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.hpp 567 B sha256:438c1e662f5c9fa4d5821fbab251113c66562dd452d1844f965c294bb3444e87 | every name m_dispatchers accepts ends in this table: an unknown name answers Bad dispatcher, two names alias one implementation, one accepted name is an inert lambda, and the argument is split inside each implementation with its own CVarList2 separator, comma by default and overridden per call site | mined | 2026-10-27 | on-release | corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |
| S366 | Hyprland 0.56.2 hyprctl dispatch request - the socket path to the same dispatcher map - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | code | A | how the hyprctl dispatch command turns its request text into a dispatcher call, and what it replies | Hyprland-HyprCtl.cpp:1126-1158 dispatchRequest, Hyprland-HyprCtl.cpp:1128 keyword strip, Hyprland-HyprCtl.cpp:1130-1141 lua branch, Hyprland-HyprCtl.cpp:1143-1147 head and arg split with the empty-argument case, Hyprland-HyprCtl.cpp:1149-1151 lookup and Invalid dispatcher, Hyprland-HyprCtl.cpp:1153-1157 call and reply, Hyprland-HyprCtl.cpp:2036 command registration @ commit efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/Hyprland-HyprCtl.cpp 97582 B sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa | dispatchRequest splits at the first space only, resolves the head in the same m_dispatchers map, passes the remainder as the whole argument, answers Invalid dispatcher for an unknown head and ok or the dispatcher error otherwise; on a lua config the text is wrapped as hl.dispatch(in) instead | mined | 2026-10-27 | on-release | corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |
| S367 | Hyprland 0.56.2 submap action and action state - what the submap dispatcher does to the current submap - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp | code | A | what the submap dispatcher does to the current submap name for a reset, an empty and a named argument, and where that name and the press marker live | Hyprland-ConfigActions.cpp:1664-1682 setSubmap, Hyprland-ConfigActions.cpp:1665-1670 reset and empty, Hyprland-ConfigActions.cpp:1672-1679 name must match a registered bind, Hyprland-ConfigActions.cpp:1681 failure text; Hyprland-ConfigActions.hpp:114 m_passPressed and Hyprland-ConfigActions.hpp:118 m_currentSubmap declarations @ commit efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/Hyprland-ConfigActions.cpp 71407 B sha256:a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637; pin .ufo/waves/round-51/fetch/Hyprland-ConfigActions.hpp 6960 B sha256:746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073 | reset or an empty argument clears the current submap and posts an empty submap event; any other name is accepted only when a registered bind already carries that submap, otherwise the dispatcher fails with wasn't registered and the submap is unchanged | mined | 2026-10-27 | on-release | corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |
| S368 | Hyprland 0.56.2 legacy bind dispatcher field - extraction, lowercasing and the parse-time existence check - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | code | A | how a bind line's dispatcher field and its argument are taken and validated at parse time, before any key press | Hyprland-legacy-ConfigManager.cpp:1584-1599 field choice, mouse override, lowercasing and the m_dispatchers check; Hyprland-legacy-ConfigManager.cpp:1624-1631 handler and command stored on SKeybind @ commit efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/Hyprland-legacy-ConfigManager.cpp 90963 B sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b | the dispatcher is the field after mods, key, description and device, forced to mouse for mouse binds, lowercased, and rejected at parse time when absent from m_dispatchers, so a misspelt handler never reaches a press; the next field is stored verbatim as arg | mined | 2026-10-27 | on-release | corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |
| S369 | Hyprland 0.56.2 dispatch result struct - the defaults every dispatcher return starts from - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/SharedDefs.hpp | code | A | the fields a dispatcher's return value carries and the defaults an empty return carries, which decide whether the key event is passed or consumed | Hyprland-SharedDefs.hpp:52-56 struct SDispatchResult, Hyprland-SharedDefs.hpp:53 passEvent default and :54 success default @ commit efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/Hyprland-SharedDefs.hpp 1915 B sha256:0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087 | an empty SDispatchResult is success with passEvent false, so a dispatcher that returns nothing still leaves the key consumed, and passEvent true is the only signal that hands the event back | mined | 2026-10-27 | on-release | corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |

## 2. Quote verification — one ≤25-word quote per row, checked at the cited line

Word count is whitespace tokens of the quoted span (code tokens count as words). Every quote is
free of `|` so the registry table cannot be broken by it.

| id | pin:line | quote | words |
|---|---|---|---|
| S364 | Hyprland-KeybindManager.cpp:785 | const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler); | 9 |
| S364 | Hyprland-KeybindManager.hpp:137 | std::unordered_map<std::string, std::function<SDispatchResult(std::string)>> m_dispatchers; | 3 |
| S365 | Hyprland-legacy-DispatcherTranslator.cpp:32 | return {.success = false, .error = "Bad dispatcher"}; | 8 |
| S365 | Hyprland-legacy-DispatcherTranslator.hpp:19 | std::unordered_map<std::string, std::function<SDispatchResult(const std::string&)>> m_dispMap; | 4 |
| S366 | Hyprland-HyprCtl.cpp:1149 | const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR); | 5 |
| S367 | Hyprland-ConfigActions.cpp:1681 | return std::unexpected(std::format("Cannot set submap {}, submap doesn't exist (wasn't registered!)", submap)); | 11 |
| S368 | Hyprland-legacy-ConfigManager.cpp:1594 | const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER); | 5 |
| S369 | Hyprland-SharedDefs.hpp:53 | bool        passEvent = false; | 4 |

Rows S364, S365 and S367 each carry two pins (a `.cpp` plus its `.hpp` at the same revision), the
pattern held row S355 uses (`.c` plus `.h`); the row-level quote is the `.cpp` one and the extra
header lines are verified as second anchors.

## 3. Transcripts (raw tool output, unedited)

### 3a. `grep -nF` of every quote against the pin bytes

Run in `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch/` on 2026-10-27, all eight greps against the
pins the L1 will move to `.ufo/waves/round-51/fetch/`. Full copy, unedited, in `quote-greps.txt`
(same directory as this file).

```
$ grep -nF -- "const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);" Hyprland-KeybindManager.cpp
785:        const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);

$ grep -nF -- "std::unordered_map<std::string, std::function<SDispatchResult(std::string)>> m_dispatchers;" Hyprland-KeybindManager.hpp
137:    std::unordered_map<std::string, std::function<SDispatchResult(std::string)>> m_dispatchers;

$ grep -nF -- "return {.success = false, .error = "Bad dispatcher"};" Hyprland-legacy-DispatcherTranslator.cpp
32:        return {.success = false, .error = "Bad dispatcher"};

$ grep -nF -- "std::unordered_map<std::string, std::function<SDispatchResult(const std::string&)>> m_dispMap;" Hyprland-legacy-DispatcherTranslator.hpp
19:        std::unordered_map<std::string, std::function<SDispatchResult(const std::string&)>> m_dispMap;

$ grep -nF -- "const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);" Hyprland-HyprCtl.cpp
1149:    const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);

$ grep -nF -- "Cannot set submap {}, submap doesn't exist (wasn't registered!)" Hyprland-ConfigActions.cpp
1681:    return std::unexpected(std::format("Cannot set submap {}, submap doesn't exist (wasn't registered!)", submap));

$ grep -nF -- "const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);" Hyprland-legacy-ConfigManager.cpp
1594:    const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);

$ grep -nF -- "bool        passEvent = false;" Hyprland-SharedDefs.hpp
53:    bool        passEvent = false;
```

### 3b. `verify-quotes.py` — verbatim, word count, pin size and sha256 per pin

`python3 .ufo/waves/round-51/w1/ScrRowsDispatch/verify-quotes.py .ufo/waves/round-51/w1/ExecFetchDispatch/fetch .ufo/waves/round-50/fetch`
(the second directory is the round-50 fetch set, passed so a pin name that repeats across rounds is
`cmp`-checked)

```
S364 Hyprland-KeybindManager.cpp:785 bytes=39334 sha256=8d8f35fc84c4a2f8 meta=ok
  line: const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);
  quote(9w): const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);
  verbatim=YES words_ok=YES pipe_free=YES
S364 Hyprland-KeybindManager.hpp:137 bytes=7936 sha256=cee22c13d413ab38 meta=ok
  line: std::unordered_map<std::string, std::function<SDispatchResult(std::string)>> m_dispatchers;
  quote(3w): std::unordered_map<std::string, std::function<SDispatchResult(std::string)>> m_dispatchers;
  verbatim=YES words_ok=YES pipe_free=YES
S365 Hyprland-legacy-DispatcherTranslator.cpp:32 bytes=35997 sha256=7248cbb89f898c78 meta=ok
  line: return {.success = false, .error = "Bad dispatcher"};
  quote(8w): return {.success = false, .error = "Bad dispatcher"};
  verbatim=YES words_ok=YES pipe_free=YES
S365 Hyprland-legacy-DispatcherTranslator.hpp:19 bytes=567 sha256=438c1e662f5c9fa4 meta=ok
  line: std::unordered_map<std::string, std::function<SDispatchResult(const std::string&)>> m_dispMap;
  quote(4w): std::unordered_map<std::string, std::function<SDispatchResult(const std::string&)>> m_dispMap;
  verbatim=YES words_ok=YES pipe_free=YES
S366 Hyprland-HyprCtl.cpp:1149 bytes=97582 sha256=798b7c6c4c168455 meta=ok
  line: const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);
  quote(5w): const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);
  verbatim=YES words_ok=YES pipe_free=YES
S367 Hyprland-ConfigActions.cpp:1681 bytes=71407 sha256=a83abeb57175e659 meta=ok
  line: return std::unexpected(std::format("Cannot set submap {}, submap doesn't exist (wasn't registered!)", submap));
  quote(11w): return std::unexpected(std::format("Cannot set submap {}, submap doesn't exist (wasn't registered!)", submap));
  verbatim=YES words_ok=YES pipe_free=YES
S368 Hyprland-legacy-ConfigManager.cpp:1594 bytes=90963 sha256=9db68cf44048d865 meta=ok
  line: const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);
  quote(5w): const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);
  verbatim=YES words_ok=YES pipe_free=YES
S369 Hyprland-SharedDefs.hpp:53 bytes=1915 sha256=0b40cc83f827587f meta=ok
  line: bool        passEvent = false;
  quote(4w): bool        passEvent = false;
  verbatim=YES words_ok=YES pipe_free=YES
cmp Hyprland-KeybindManager.cpp: .ufo/waves/round-51/w1/ExecFetchDispatch/fetch/Hyprland-KeybindManager.cpp vs .ufo/waves/round-50/fetch/Hyprland-KeybindManager.cpp byte_equal=True
cmp Hyprland-legacy-ConfigManager.cpp: .ufo/waves/round-51/w1/ExecFetchDispatch/fetch/Hyprland-legacy-ConfigManager.cpp vs .ufo/waves/round-50/fetch/Hyprland-legacy-ConfigManager.cpp byte_equal=True
ROWS=6 CHECKS=8 BAD=0 verdict=OK
```

(`meta=ok` means the pin's byte size and full sha256 equal the values the script holds and the fetch
manifest records; a re-fetch that changed bytes fails the check. Re-run the same command with the
first directory replaced by `.ufo/waves/round-51/fetch/` after the L1 moves the pins; the expected
values are pinned in the script, so the moved set must reproduce this transcript.)

### 3c. The 71/71 population claim in S364 and S365

```
$ python3 -  # sets of names, KeybindManager.cpp:42-113 vs DispatcherTranslator.cpp:797-867
km names 71 table 71
in km not table []
in table not km []
```

### 3d. Byte identity with the round-50 pins

```
$ cmp Hyprland-KeybindManager.cpp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-50/fetch/Hyprland-KeybindManager.cpp
cmp Hyprland-KeybindManager.cpp: byte-equal
$ cmp Hyprland-legacy-ConfigManager.cpp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-50/fetch/Hyprland-legacy-ConfigManager.cpp
cmp Hyprland-legacy-ConfigManager.cpp: byte-equal
$ cmp Hyprland-SharedDefs.hpp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/w1/ScrDispatchEntry/fetch/Hyprland-SharedDefs.hpp
Hyprland-SharedDefs.hpp: byte-equal
```

Consequence for the entry: S364 cites the same file bytes as held row S352 and S368 the same bytes
as held row S353, so the entry can chain a held fact and a new fact on one file without a
re-fetch discrepancy.

## 4. Rejected candidates (taste record — no rows written)

1. **`docs/hyprctl.1.rst` @ efb5099** (2,623 B, sha256 `07cd73872e32ec59…`, pin
   `Hyprland-docs-hyprctl.1.rst`). Rejected under rule 4: its `**dispatch**` entry
   (`:22-34`) restates the reply contract that S366 already grounds in the code that produces it
   ("Call a dispatcher with an argument. An argument must be present. … Returns: ok on success, and
   an error message on failure."), and it adds no mechanism. Its two examples are lua-form
   (`dispatch "hl.dsp.exec_cmd('kitty')"`), so it cannot ground a hyprlang spelling either. The
   *documentation* fact it does hold (the page says an argument must be present) is worth a
   sentence in the entry's limits, because the code does not enforce it: `HyprCtl.cpp:1145-1147`
   leaves `DISPATCHARG` empty when no space follows the dispatcher name and still calls it. That
   sentence cites the pin directly; it does not need a registry row.
   Flip: an entry claim about the *documented* contract, or a shipped-page regression sweep.
2. **wiki `content/Configuring/Basics/Dispatchers.md` @ d5f07c60** (13,337 B, sha256
   `39d0747a34bf013d…`, pin `wiki-Dispatchers.md`). Rejected as support for any hyprlang
   dispatcher-string claim: the page opens "Since Hyprland 0.55, hyprlang is deprecated in favor of
   lua." and every dispatcher row is an `hl.dsp.*` table (`:83` `submap(name)`, `:74` `exec_cmd`).
   Citing it for `bind = MODS, KEY, dispatcher, arg` would be attribution drift. Flip: a
   commit-pinned page that documents the hyprlang `dispatcher, arg` form (the 0.54 archive carries
   no commit anchor — round-50 lesson).
3. **wiki `Using-hyprctl.md` @ d5f07c60** (7,859 B, sha256 `3489a75da5f0865d…`). Same reason:
   `:53-61` documents dispatch as "a shorthand for `eval 'hl.dispatch(...)'`", i.e. the lua branch
   only. S366 already grounds both branches.
4. **A row teaching "the dispatcher argument is split on commas at dispatch time" as a global
   grammar.** Rejected as false against these pins: the bind path never splits (`:1586` stores the
   rest of the line verbatim as COMMAND, `KeybindManager.cpp:812` passes `k->arg` whole) and the
   hyprctl path splits at the first space only (`HyprCtl.cpp:1143-1147`). Splitting is per
   dispatcher inside `DispatcherTranslator.cpp` (S365), where a comma is merely the default
   separator of the primitive (`hyprutils VarList2.hpp:18`, `delim = ','`) and several call sites
   override it with a space (`:162`, `:189`, `:773`) or whitespace (`'s'`, `:476`, `:503`). A row
   asserting a global grammar would have licensed a wrong entry claim; the per-call-site reading
   belongs in S365, which is where it now is.
5. **`src/config/ConfigManager.cpp` @ efb5099** (2,597 B, manager selection). Rejected: the
   lua-versus-legacy choice it records is the *trigger* for `HyprCtl.cpp:1130`, which S366 already
   carries, and the config-era rule is held ground in `corpus/knowledge/hyprland-config-era-r12.md`
   (rows S024/S029). A row here would restate a held fact at a new file. Flip: an entry claim about
   startup precedence rather than dispatch.

## 5. Registry effects

- Row count 300 → 306 — `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
  (300 at base `6ca8c559`) plus these six; the next free id at base was S363, so S364-S369 are
  contiguous and no id is reused.
- Shape checked with the contract's own census commands against the six rows extracted from §1:
  rows 6, malformed `NF!=13` 0, tier `A=6`, no enum or tier-inflation violation, opened
  `2026-10-27`, recheck `on-release`, used-by the entry path on every row, no id collision with the
  300 held rows.
- Duplicate-URL-across-scopes warnings (census W04, pre-existing class accepted at round-50
  closure): S364 reuses the S352 URL at a new scope (map population and press-time call, not key
  matching), S368 reuses the S353 URL at a new scope (dispatcher field and validation, not the KEY
  field). Expect exactly two new warnings of that class; no new class.
- **S369's pin:** `Hyprland-SharedDefs.hpp` was missing from the fetch set when this row was
  drafted and is now pin #12 of 19 there (fetch seat: `curl -fsSL`, git blob
  `bb7c601e3b299623f433bf809759f57050eb4c9f` recomputed from the bytes, 1,915 B,
  sha256 `0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087`, `self_row_lines=0`
  in `SHA256SUMS`). If it somehow fails to reach `.ufo/waves/round-51/fetch/`, **drop S369** rather
  than leave a row bound to an absent pin — no other row depends on it.
- Every row is `status=mined`, so its `used-by` path must exist at the C2 freeze:
  `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` (draft today in `w1/ScrDispatchEntry/`).
  The SOURCES census "mined rows whose used-by paths do not exist" sweep flags these six rows if the
  entry is not integrated in the same commit.
- C2 clause (b) is satisfied by S364 and S366 at minimum (two rows, kind code, tier A, `mined`,
  opened 2026-10-27, each bound to a pin under `.ufo/waves/round-51/fetch/` named in the entry's pin
  manifest whose cited line holds the row quote verbatim).

## 6. Known limits

- Tiers are A for the cited revision only. These rows say nothing about 0.57+; `recheck: on-release`
  is the standing obligation, and `Config::Legacy::` is the piece most likely to move when hyprlang
  support is dropped.
- The host's config plane is hyprlang (`ls ~/.config/hypr` on 2026-10-27: `hyprland.conf` present,
  no `hyprland.lua`), so the legacy branch is the one that applies here; the lua branch at
  `HyprCtl.cpp:1130-1141` is in the same function and would take over if a `hyprland.lua` appeared.
  This is a read-only observation, not a row.
- The 71/71 set equality is measured on these two pins only (§3c), not on the whole dispatcher
  surface: names reachable only through the lua bindings (`LuaBindingsDispatchers.cpp`, not a row
  here) are outside this set.
- S369's quote is one member line of a four-line struct: `:52` (the struct head) and `:54-56` (the
  `success` default, `error`, the closing brace) are anchored in the row's anchor cell but not
  quoted, so a reader checking only the quote does not see the `success` default. That default is
  what the entry's "an empty return is success, so the key is consumed" sentence rests on, and the
  fetch seat's `anchors.txt` verifies all four lines.

## 7. Post-draft correction (peer review, 2026-10-27)

`ScrDispatchEntry` re-grepped the S365 pin and found my `m_dispMap` range off: I had written
`:819-861`, which starts inside the table (at `togglegroup`) and stops six entries early. Verified
here against the same pin:

```
$ grep -n 'm_dispMap\[' Hyprland-legacy-DispatcherTranslator.cpp | head -1
797:    m_dispMap["exec"]                           = ::exec;
$ grep -n 'm_dispMap\[' Hyprland-legacy-DispatcherTranslator.cpp | tail -1
867:    m_dispMap["releaseinputcapture"]            = ::releaseInputCapture;
$ grep -c 'm_dispMap\[' Hyprland-legacy-DispatcherTranslator.cpp
71
$ awk 'NR==796' Hyprland-legacy-DispatcherTranslator.cpp
CDispatcherTranslator::CDispatcherTranslator() {
```

Corrected to `:797-867` (constructor at `:796`, closing brace `:868`) in the S365 anchor cell and in
the §3c transcript label. The row's quote (`:32`), its other line anchors (`:835`, `:839-840`,
`:861`) and every gate result in §2-§3 are unchanged — a range fix moves no quote and no digest.
The peer's other reads agree with mine on every line it checked (`ConfigActions.cpp:1681`,
`SharedDefs.hpp:52-56`, `KeybindManager.cpp:785` and `:812`, `HyprCtl.cpp:1143-1147`,
`legacy-ConfigManager.cpp:1584-1599` and `:1624-1631`, `DispatcherTranslator.hpp:19`).

Also from that review, and now stated in §4.4: `CVarList2`'s default separator is `','`
(`hyprutils VarList2.hpp:18`), which is what makes the per-dispatcher overrides meaningful. Checked
at the pins for the two claims the entry keeps as Limits notes (no rows, rule 4):

```
$ awk 'NR>=20 && NR<=21' Hyprutils-VarList.cpp
        if (++idx == lastArgNo) {
            m_vArgs.emplace_back(trim(in.substr(pos)));
$ grep -n 'lastArgNo' Hyprutils-VarList2.cpp
8:CVarList2::CVarList2(std::string&& in, const size_t lastArgNo, const char delim, const bool removeEmpty, const bool allowEscape) :
10:    construct(m_inString, lastArgNo, delim, removeEmpty, allowEscape);
13:CVarList2::CVarList2(std::string_view in, const size_t lastArgNo, const char delim, const bool removeEmpty, const bool allowEscape) : m_inString(in) {
14:    construct(m_inString, lastArgNo, delim, removeEmpty, allowEscape);
17:CVarList2::CVarList2(const char* in, const size_t lastArgNo, const char delim, const bool removeEmpty, const bool allowEscape) : m_inString(in) {
18:    construct(m_inString, lastArgNo, delim, removeEmpty, allowEscape);
21:void CVarList2::construct(std::string_view in, const size_t lastArgNo, const char delim, const bool removeEmpty, const bool allowEscape) {
```

So `CVarList` does implement the last-field remainder, and `lastArgNo` reaches
`CVarList2::construct` only as a parameter: no read of it appears in the body, which is consistent
with the capped-split behaviour being unimplemented there. Both are Limits-note material, not
mechanism claims of the entry, so no S370+ row was added; this seat's numbering budget is S364-S369
and the row set is closed at six.
