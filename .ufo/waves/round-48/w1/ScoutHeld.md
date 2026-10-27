# ScoutHeld - held-ground check, round 48 w1 (base 579f694b45c797a9c39761fdb4f9e0a1b71b3585)

Method: `git grep` / `git show` at the base commit (read-only). Quotes are from the base tree. Commands: `git grep -n -i <pat> 579f694 -- corpus/`; `git show 579f694:<path> | sed -n`.
Lane HEAD at check time printed 5ff16742..., so every locator below is the BASE tree, not the working tree.

## 1. C1 - what the lane already holds about the resolver cache

### 1.1 Held statements (do NOT re-claim)
| # | where | what is held | class |
|---|---|---|---|
| H-a | corpus/knowledge/xdg-terminal-selection-r47.md:43 ("The cache, separately") | on by default (`XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}`, :1172); tried first (:1179); on hit skips steps 1-5; README `Valid cache bypasses reading of any other file.` (README.md:300-301); key = md5 over literal `4` (:194), `$XDG_CURRENT_DESKTOP`, `ls -LRl` of config+applications paths (:179-215, :200); file = ten positional lines (hash, command, path, id, action, execarg, appidarg, titlearg, dirarg, holdarg) + USEP-joined words ended by RS+`END_OF_EXEC_USEP` (:217-298 reader, :300-340 writer); accepted only if hash matches AND cached cmd on PATH (:274); saved on a non-cached run past the print bail-out (`--print-cmd`, `--test`, launch) in background (`save_cache "$1" &`, :1455-1458), `$XDG_CACHE_HOME` created (:303), `umask 0077`; `--print-id/--print-path` only exits before (:1378-1384), writes nothing; newline guard :312-317 fires only if the whole concatenation is exactly a newline | documentary (reading of script + README; no warm run executed in the entry) |
| H-b | same file :43 end | "a warm cache hides the list files from the run entirely, and a `--print-cmd` probe refreshes the cache it was meant to observe - both why a tool that must answer 'why' models a cold cache" | documentary + rationale for the cold-only design |
| H-c | same file :25 (claims table) | cache row: "sourced; out of the C1 contract" | scope statement |
| H-d | same file :83 | "Two runs disagreeing although no file changed usually means the first run wrote a cache the second used (cache section); compare under a fresh `XDG_CACHE_HOME`." | advice |
| H-e | same file :76 | hotkey run reads host cache first (:1179); `.ufo/waves/round-47/w2/RevengerCache.md` "recomputed its key read-only and found it current and naming the same entry, so today the cached and the cold answer agree" | one executed observation (hash equality, host), cited by pointer only |
| H-f | same file :70 census | `cache_header_fields=10 cache_hash_format=4` | counted from the pin |
| H-g | corpus/knowledge/terminal-route-r17.md:51-53 | "the resolver caches its choice by default (`XTE_CACHE_ENABLED` default true, :1172), reads it first (:1179) and saves it only after a fresh selection (`save_cache`, :300-302, :1455-1457)" | documentary (r17, thinner than r47: says nothing of the hash, validity, --print-id) |
| H-h | corpus/knowledge/terminal-route-r17.md:123-127 | [OBS, bytes] host cache `~/.cache/xdg-terminal-exec` 190 B, sha256 dd26ec4e..., mtime 2026-10-20 09:57:18, records `alacritty`, `/home/vgpnk/.local/share/applications/./Alacritty.desktop`, four `X-TerminalArg*` values; "test/print modes also write the cache" | observed bytes of the HOST cache on 2026-10-20; STALE by now (round-47 RevengerCache records host cache sha256 f497ed05..., 190 B, mtime 2026-10-26 17:42:25, hash d27b6b70...). Do not cite as current. |
| H-i | tools/mado-terminal.py:82-85 (docstring "Cache (out of contract)") | resolver tries `$XDG_CACHE_HOME/xdg-terminal-exec` (default `$HOME/.cache`), valid while md5 of XDG_CURRENT_DESKTOP and `ls -LRl` of every list+application path unchanged (x:179-298); `--print-cmd` (not --print-id/--print-path alone) rewrites it in background (x:1455-1458); "This tool always models the cold path; `explain` says whether a cache file exists." Also out of contract there: -h/--help, HOME unset, FIFO named like a desktop file, symlink loops, empty-string argument, ':' in XDG dirs/HOME, glob/quote chars, \u/\U escapes, odd locale file names -> `MADO_TERM_OUT_OF_CONTRACT: <reason>` stderr, exit 2 | scope statement (code) |
| H-j | tools/mado-terminal.py:19,852-861,876 | MADO_TERM line today: `cache=<absent|present|disabled>`; `present` = `os.path.isfile(r.cache_file)`; `disabled` when `check_bool(cache_enabled)` false. Cache env handled at :716-723 (`XTE_CACHE_ENABLED`, `cache_configured`; `cache_file = (XDG_CACHE_HOME or HOME/.cache)+"/xdg-terminal-exec"`); /enable_cache,/disable_cache list directives at :449-452 | executed (tool selftest 43/43 per goal) but only existence is tested |
| H-k | quality/counters/c1-r47-terminal.py:52-57 docstring | "the cache path of the resolver (a warm cache) and -h/--help are outside the contract" (declared residual); round-47 RevengerCache.md:122-123: no fixture seeds a cache or sets XDG_CACHE_HOME/XTE_CACHE_ENABLED; "C1 cannot catch a candidate that reads `XDG_CACHE_HOME` itself" | scope + known gap |
| H-l | .ufo/waves/round-47/w2/RevengerCache.md (NOT corpus; wave receipt) | sections 1 chain-as-coded, 2 independent md5 recompute `{ echo 4; echo Hyprland; LANG=C LC_ALL=C ls -LRl <CONFIGS> <APPS>; } | md5sum` == line 1 of host cache (d27b6b70...), 3 warm vs cold identical for the hotkey shapes, **4 H1** (key is metadata-only: content edit with same size/mtime invisible), **H2** (cached content trusted beyond hash; validated field `command -v` :274 is not the executed field), 5 limits | executed ground for H1/H2 exists but only in a wave note, never promoted to corpus |

### 1.2 What is documentary only (no executed warm-cache run held anywhere in corpus/)
- Everything in H-a/H-g: the reader/writer line semantics, `<=49 lines`/"line 11+" layout (the lane holds only "ten lines ... followed by the command words", not the 49-line cap or the terminator behaviour), accept rule, directives.
- No held statement says what a warm `--print-*` run PRINTS from cached id/path/action/exec/arg values vs. the cold answer, nor how `--dir/--title` interact with cached arg names; the only warm-run claims are H-e (agreement today) and H-l H1/H2 (wave note).
- No held ls-emulation claim at all: `grep -c` for `ls -LRl` / `gen_hash` in corpus/ tools/ quality/ gives only the r47 entry's md5 sentence and the tool's `SCRIPT_FUNCTIONS` name list (tools/mado-terminal.py:107); no emulation of total lines, column widths, dates, uid/gid.

### 1.3 New executed ground the warm-cache tool would add (claim safe to make)
1. tool `print` == real pinned script stdout+rc under a primed (cold `--print-cmd` + background save) warm cache, on fixtures where warm differs from cold (same-size/same-minute edit, removed TryExec stub with exec[0] still resolving, changed --dir/--title over cached arg names).
2. cache states hit / stale / invalid / disabled, each executed against the real script (mtime, size, name, dir change; XDG_CURRENT_DESKTOP change; exec[0] gone; missing terminator; line limit; bad hash) - extends H-a "accepted only when hash matches and command on PATH" from documentary to executed.
3. byte-exact `LC_ALL=C LANG=C ls -LRl` emulation inside a sandbox with numeric ids (entirely new; H-l is a one-host md5 recompute with a real `ls`, not an emulation).
4. `explain` `cache=` goes from 3 values {absent, present, disabled} (tool :852-861) to 5 {absent, hit, stale, invalid, disabled}; `present` disappears - a clean cutover must edit :19 docstring, :852-861, :876 and any selftest/counter that matches `present`.
5. HOME unset -> pin exit 1, empty stdout (round-47 closure D1; today the tool exits 2 out-of-contract per :85).
6. Promotes H1/H2 (RevengerCache.md:83,91) from a wave note to a tool-reproduced, counter-judged fact.

### 1.4 Wording traps for the claim
- Do not say "the cache is out of contract" as new: tools/mado-terminal.py:82-85 and c1-r47-terminal.py:56 say so; C1 r48 CHANGES that, so the docstring at :82-85, the counter docstring line 56 residual, and xdg-terminal-selection-r47.md:25 (claims-table row) / :43-end (the "why a tool models a cold cache" sentence) become stale on landing (L1 owns the edit).
- Do not re-cite terminal-route-r17.md:123-127 as the host cache state (superseded by RevengerCache sha f497ed05... / d27b6b70...).
- xdg-terminal-selection-r47.md:43's "ten lines" is the header count; "<=49 lines" is the reader's cap (draft goal cites script :217-298) - not held in corpus; treat as new only after the real script is read/executed.
- D4 erratum confirmed (computed): corpus/knowledge/xdg-terminal-selection-r47.md:95 (Limits) cites `terminal-route-r17.md:150-151`; `git show 579f694:corpus/knowledge/terminal-route-r17.md | grep -n 'Whether the `--dir=`'` -> line 149 (bullet runs 149-150).

## 2. C2 - held XKB ground at base (git grep under corpus/)

Absence proof (each `git grep -c -i -e <pat> 579f694 -- corpus/` exits **1** = no match):
`xkb_keymap_new_from_names` rc=1; `XKB-595` rc=1; `XKB-338` rc=1; `compile-keymap` rc=1; `xkeyboard-config-2` rc=1; `rules/evdev` rc=1; `include path` rc=1; `xkbcli` rc=1.
`xkbcommon` rc=0, exactly one hit: corpus/SOURCES.md:20 (S008 Wayland book row: "libinput/xkbcommon/libdrm/GBM/KMS roles named - concept ground for U4/U6, never a host fact").
`xkeyboard-config` (no `-2`): the only corpus hits are the r46 entry :69 and README :112 (below) plus S319-adjacent lines; no row, no package version, no path held.
=> libxkbcommon 1.13.2 / xkeyboard-config 2.48, RMLVO->KcCGST, include-path order, the exit codes 0/1, XKB-595, unknown-model rc 0: ALL are new ground. No held row for libxkbcommon source or xkeyboard-config source; SOURCES.md tops at S339 (276 data rows; `grep -c -E '^\| S34[0-9]'` = 0) so S340.. is free.

### 2.1 Held XKB sentences (cite, never re-claim)
corpus/knowledge/hyprland-input-devices-r46.md:
- :22 claims row: "which value of `kb_layout`, `kb_variant`, `kb_options`, `kb_model`, `kb_rules`, `kb_file` a keyboard gets | the chain below, steps 1-4 | sourced at the host's revision".
- :26 "which keymap a virtual keyboard really uses | the dump's `active_keymap` names its active layout (step 5); the rest of the keymap is UNK | partly observable".
- :33 step 4 (the sentence C2 must cite for the fallback): "The five names go to setKeymap as the keyboard's current rules (Hyprland-InputManager.cpp:1282-1295...), which stores them before any compile. A non-empty kb_file ... is tried first and the names only when no keymap came from the file (Hyprland-IKeyboard.cpp:87-99...)... If no keymap results, the stored rules are reset to layout `us` with every other name empty and an error overlay names the rejected names (Hyprland-IKeyboard.cpp:101-116, fallback to us after an error overlay), which is why a typo in `kb_layout` shows up in the dump as `us`, not as the typo; a comma list of layouts collapses to that single `us`."
- :34 step 5: dump prints stored rules; `active_keymap` is "named in XKB's words such as `Portuguese (Brazil)`, not the config's `br`".
- :42 **OBS** S318 `MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",` at Hyprland-ConfigValues.cpp:272 (built-in layout; other five names default to empty marker, row S318).
- :43 **OBS** S319 `m_currentRules.layout = "us";` at Hyprland-IKeyboard.cpp:113.
- :57 host: nine keyboards AGREE on layout `br`, options `compose:caps`.
- :63 reading note: "A keyboard that prints `us` and empty names while its config names something else most likely failed to compile its keymap (step 4); Hyprland also queues an error overlay naming the rejected names."
- :64 "`hyprctl switchxkblayout` changes the active layout index, not the stored names..."
- :69 (Limits; the open ground): "The XKB compile itself is not reproduced: whether a given layout/variant pair exists in xkeyboard-config is not checked; only the stored names are compared."
- :53 census line `hyprland input-device default_layout=us fallback_layout=us ...`.
corpus/README.md:112 (round-46 bullet; the stated open item): "Still open: the XKB compile itself (whether a layout/variant pair exists in xkeyboard-config)".
corpus/SOURCES.md S318 row (`input:kb_layout` default us, receipt .ufo/waves/round-46/fetch/Hyprland-ConfigValues.cpp, sha256 a76f0507...) and S319 row (IKeyboard.cpp:60-145 setKeymap, :101-116 fallback; "on a compile failure they reset to layout us with the rest empty; an overridden keymap ignores new names"; receipt .ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp sha256 8a800efe...).
Other held host-name facts (cite, not re-claim): hyprland-config-plane.md:139 and hyprctl-verification-layer.md:120-124,159 (`input:kb_layout` = `br` from input.conf:10 over default `us`; `kb_options` = `compose:caps`; `kb_variant`/`kb_model`/`kb_rules` empty; "8 keyboard nodes, all `active_keymap: Portuguese (Brazil)`" at that round); hyprctl-getoption-native-forms-r40.md:78 (S279: `input:kb_layout`, `input:kb_options` agree with an earlier declarer shadowed); hyprland-input-devices-r46.md round-46 verifier note (`kb_layout = br`->`de` scratch test gives DIFFER).
Round-46 verifier: .ufo/waves/round-46 w2 note C2 re-checked "`layout = "us"` after a failed compile" (corpus/lessons/round-46-verifier-spotcheck.md:51, row "C2 entry head and pins") - agrees; this is the Hyprland half only.

### 2.2 idle-lock-plane.md, keybind-rule-semantics.md (assigned by the task)
- corpus/knowledge/idle-lock-plane.md:188 `hyprctl switchxkblayout all 0`; :205-206 "`hyprctl switchxkblayout all 0` targets index 0 and every keyboard already reports `layout=br` with only `br` configured (`input.conf:10`; default `us` at `default/hypr/input.conf:3` is overridden) - a no-op today, not a guarantee." (Index-0-of-one-layout; touches XKB only through the layout index, NOT the compile; (also idle-lock-route-r17.md:106, waybar-walker-plane.md:246).)
- corpus/knowledge/keybind-rule-semantics.md:106 only: "Named keysym | `RETURN`, `F`, ... | `[INF-docs]` use the segment after `XKB_KEY_`". No compile/RMLVO statement. (Hyprland 0.56.2 keybind keymap: hyprland-input-devices r46 REJECT note at nd-46 "KeybindManager.cpp:296-313 compiles the global `input:kb_*` options into the keybind translation state" - a rejected row, held only as a screening note in .ufo/waves/round-46 w1 report.)

### 2.3 Exit codes held
None. No corpus statement holds any `xkbcli`/libxkbcommon exit code. The only held "failure" behaviour is Hyprland-side: after a failed compile -> rules reset to layout `us`, others empty (r46:33,43). All of rc 0/1, "Couldn't find file symbols/zz", "Couldn't process include statement", XKB-595 are new.
Host facts supplied by L1 (NOT yet held in corpus; executed receipt needed): `xkbcli compile-keymap --layout br --options compose:caps` rc 0; `--layout zz` rc 1; `--layout br --variant nope` rc 1; unknown option rc 0 + XKB-595; unknown model rc 0; `--rules nope` rc 1; include dirs: /usr/share/xkeyboard-config-2 (user paths absent).

### 2.4 Mapping to the Hyprland fallback (do not re-claim)
C2 must cite r46:33/:43 + S319 for "compile fails -> `us`, other names empty, error overlay". It may NEW-claim which names fail the compile (layout, variant, rules) vs warn (option) vs pass silently (model), per the libxkbcommon source. Caveat for C2 wording: whether Hyprland's own call (xkb_keymap_new_from_names flags / rule-name handling, an empty `kb_rules` -> libxkbcommon default rules) is the same as `xkbcli compile-keymap` defaults is not in the held tree (S319 fetch covers IKeyboard.cpp:60-145 only; I did not open the receipt) - mark INF unless the call site is read.

## 3. Conflicts / stale items found
- r17:123-127 host cache bytes are stale (see H-h).
- tools/mado-terminal.py:82-85 + c1-r47-terminal.py:56 + xdg-terminal-selection-r47.md:25,:43 become stale on C1 landing.
- hyprland-input-devices-r46.md:69 and README.md:112 are the ground C2 closes - both need a "closed by r48" edit by L1.
- No evidence of an existing xkb knowledge entry; target file corpus/knowledge/xkb-keymap-compile-r48.md does not exist at base (`git cat-file -e 579f694:corpus/knowledge/xkb-keymap-compile-r48.md` -> fatal: does not exist, rc 128).
