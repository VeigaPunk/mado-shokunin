author: mado

# Hyprland v0.56.2 bind table from a hyprlang config tree

## Parse and source graph

Hyprlang config lines have the form `COMMAND = VALUE`; variables are option-like values whose later assignments overwrite earlier ones, while commands invoke behavior each time they are defined. [S172, pinned `S172.bin:12,18-21`, quotes: “Every config line is a command followed by a value.”; “commands invoke some behavior every time they are defined.”]

Hyprland registers the legacy `bind` handler with flag suffixes enabled and registers `unbind` and `source` as separate handlers. [S162, pinned `ConfigManager.cpp:607-608,614`, quotes: “m_config->registerHandler(&::handleBind, "bind", {true});”; “m_config->registerHandler(&::handleUnbind, "unbind", {false});”; “m_config->registerHandler(&::handleSource, "source", {false});”]

For `source = PATH`, the handler resolves the path with the current-config-file context and calls `glob` with `GLOB_TILDE`; the source-walk report records that `~` expands through `HOME`, relative paths use the including file's directory, and matches are returned in `strcoll` order. [S162, pinned `ConfigManager.cpp:1816`, quote: “glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE”; observed: `.ufo/waves/round-25/a3w1/reports/ScoutBindSurface.md:18`]

The v4 counter gives each nested case `HOME` as its fresh copied home, so that case's `~` source paths resolve inside the case tree. [observed: `.ufo/waves/round-25/a3w1/reports/RevCounterV4.md:25`]

The handler loops over glob results, temporarily sets the current path to each regular file, synchronously calls `parseFile`, then restores the including file's path; nested sources are therefore traversed depth-first before the parent continues. [S162, pinned `ConfigManager.cpp:1824-1839`, quotes: “for (size_t i = 0; i < glob_buf->gl_pathc; i++)”; “m_configCurrentPath = value;”; “m_config->parseFile(value.c_str());”; observed: `.ufo/waves/round-25/a3w1/reports/ScoutBindSurface.md:19`]

Directories and non-regular matches are skipped, while a glob with no match is reported as an error. [S162, pinned `ConfigManager.cpp:1816-1818,1835-1848`, quotes: “r == GLOB_NOMATCH ? "found no match"”; “std::filesystem::is_regular_file(file_status)”; “source= skipping directory”; “source= skipping non-regular-file”]

## Variables and comments

Hyprlang variable assignments use `$NAME = value`, and values can interpolate references such as `$NAME$SUFFIX`. [S172, pinned `S172.bin:55-67`, quotes: “$VAR = myData”; “greeting = Hello, $NAME$SUFFIX.”]

Hyprlang says `#` starts a comment and `##` escapes a literal hash; the a3w1 source-walk report records that a leading `#` line is a comment, a later unescaped `#` starts an inline comment, and `##` becomes one literal `#`. [S172, pinned `S172.bin:72-77`, quotes: “Comments are started with the `#` character.”; “It will be turned into a single `#`”; observed: `.ufo/waves/round-25/a3w1/reports/ScoutBindSurface.md:20`]

## Bind grammar, modifiers, and keys

The handler obtains suffix flags from the keyword after `bind` and processes them one character at a time. [S162, pinned `ConfigManager.cpp:1514-1517`, quotes: “const auto BINDARGS = command.substr(4);”; “for (auto const& arg : BINDARGS)”]

| Flag suffix | Meaning in `handleBind` |
|---|---|
| `l`, `r`, `e` | locked, release, repeat. [S162, pinned `ConfigManager.cpp:1518-1520`, quote: “case 'l': locked = true; break; case 'r': release = true; break; case 'e': repeat = true; break;”] |
| `m`, `n`, `a`, `t` | mouse, non-consuming, auto-consuming, transparent. [S162, pinned `ConfigManager.cpp:1521-1524`, quote: “case 'm': mouse = true; break; case 'n': nonConsuming = true; break; case 'a': autoConsuming = true; break; case 't': transparent = true; break;”] |
| `i`, `s`, `o` | ignore modifiers, multi-key, long-press. [S162, pinned `ConfigManager.cpp:1525-1527`, quote: “case 'i': ignoreMods = true; break; case 's': multiKey = true; break; case 'o': longPress = true; break;”] |
| `d`, `p` | description field, do not inhibit. [S162, pinned `ConfigManager.cpp:1528-1529`, quote: “case 'd': hasDescription = true; break; case 'p': dontInhibit = true; break;”] |
| `c`, `g` | click and drag; each also sets release. [S162, pinned `ConfigManager.cpp:1530-1536`, quotes: “case 'c': click   = true; release = true;”; “case 'g': drag    = true; release = true;”] |
| `u`, `k`, `x` | submap-universal, per-device, allow input capture. [S162, pinned `ConfigManager.cpp:1538-1540`, quote: “case 'u': submapUniversal = true; break; case 'k': isPerDevice = true; break; case 'x': allowInputCapture = true; break;”] |

A regular bind uses `MOD, KEY, DISPATCHER, ARG`; `d` inserts a description before the dispatcher, `k` adds a device field, and the parser sets its field count from those flags. [S162, pinned `ConfigManager.cpp:1554-1558,1580-1586`, quotes: “const int numbArgs = (hasDescription ? 5 : 4) + sc<int>(isPerDevice);”; “const auto DESCRIPTION = hasDescription ? ARGS[2 + DEVICE_OFFSET] : "";”]

With `m`, the key is a mouse key, the JSON dispatcher becomes `mouse`, and the written action is retained as the argument; mouse mode accepts one fewer argument field than keyboard mode. [S162, pinned `ConfigManager.cpp:1561-1562,1584-1589`, quotes: “const auto COMMAND = mouse ? HANDLER : ARGS[3 + DESCR_OFFSET + DEVICE_OFFSET];”; “if (mouse)”; “HANDLER = "mouse";”; observed: `.ufo/waves/round-25/a3w1/reports/ScoutBindSurface.md:113-118`]

The modifier string is passed to `stringToModMask`; a nonempty string that produces mask zero is rejected. [S162, pinned `ConfigManager.cpp:1575-1576,1601-1604`, quotes: “const auto MOD = g_pKeybindManager->stringToModMask(ARGS[0]);”; “if (MOD == 0 && !MODSTR.empty())”]

The a3w1 walk observed empty modifiers as legal mask zero and describes `stringToModMask` as uppercasing then substring-matching tokens, making token order immaterial; those observations cover the walked host tree, not every alias or separator spelling. [observed: `.ufo/waves/round-25/a3w1/reports/ScoutBindSurface.md:83,185`]

`parseKey` maps a bare decimal string to a keycode only when its value is greater than 9, maps `code:N` when `N` is decimal, recognizes `catchall`, and otherwise preserves the key string. [S162, pinned `ConfigManager.cpp:1481-1489`, quotes: “if (isNumber(key) && std::stoi(key) > 9)”; “else if (key.starts_with("code:") && isNumber(key.substr(5)))”; “else if (key == "catchall")”; “return {.key = key};”]

## Rejected declarations and unbind

Unknown flag letters are rejected; `e` conflicts with `r` and `o`, mouse mode conflicts with repeat/release/locked, and `c` conflicts with `g`. [S162, pinned `ConfigManager.cpp:1541-1552`, quotes: “default: return "bind: invalid flag";”; “flags e is mutually exclusive with r and o”; “if (mouse && (repeat || release || locked))”; “flags c and g are mutually exclusive”]

Too few or too many fields, an unknown dispatcher, an invalid nonempty modifier string, and `catchall` outside a submap are rejected before a bind is added. [S162, pinned `ConfigManager.cpp:1559-1562,1594-1604,1616-1624`, quotes: “return "bind: too few args";”; “return "bind: too many args";”; “Invalid dispatcher, requested”; “Invalid mod, requested mod”; “Catchall not allowed outside of submap!”; “g_pKeybindManager->addKeybind”]

`unbind = all` clears the keybind lists; an ordinary `unbind` parses its modifier and key and calls `removeKeybind`, so it changes the table at its place in the config traversal. [S162, pinned `ConfigManager.cpp:1657-1673`, quotes: “if (ARGS.size() == 1 && ARGS[0] == "all")”; “g_pKeybindManager->m_keybinds.clear();”; “g_pKeybindManager->removeKeybind(MOD, KEY);”; observed: `.ufo/waves/round-25/a3w1/reports/ScoutBindSurface.md:19`]

Hyprland passes each accepted bind to `addKeybind`; the a3w1 walk observed repeated `(modmask, key, keycode)` identities retained as separate table rows, so a resolver must preserve multiple binds on one chord. [S162, pinned `ConfigManager.cpp:1624`, quote: “g_pKeybindManager->addKeybind(SKeybind{”; observed: `.ufo/waves/round-25/a3w1/reports/ScoutBindSurface.md:9,143-149`]

## JSON table and counter oracle

The pinned hyprctl documentation says `binds` lists registered binds and `-j` selects JSON output. [S167, pinned `WikiUsingHyprctl.bin:249,292-295`, quotes: “binds                - lists all registered binds”; “j` - output in JSON”]

The 18 fields used for exact table comparison are `locked`, `mouse`, `release`, `repeat`, `longPress`, `non_consuming`, `auto_consuming`, `has_description`, `modmask`, `submap`, `submap_universal`, `key`, `keycode`, `catch_all`, `description`, `allow_input_capture`, `dispatcher`, and `arg`. [observed: `.ufo/waves/round-25/a3w1/reports/K4EmptyArray.md:30`; cross-reference: `.ufo/waves/round-25/a3w1/reports/RevCounterV4.md:21`]

Counter v4 copies each case tree, removes standalone exec directives from the oracle copy, appends non-bind `ecosystem` options, starts nested Hyprland with `-c` pointing to the case root, waits for instance discovery, polls `hyprctl -i <signature> binds -j` until three consecutive results match, and kills the nested process group. [observed: `.ufo/waves/round-25/a3w1/reports/RevCounterV4.md:20-25`]

Hyprland accepts `--config FILE` and hands the validated explicit path to the compositor; hyprctl `-i` selects an instance by signature or index and routes the request through that instance's runtime socket. [S171, pinned `SrcHyprlandMain.bin:120-144,263-264`, quote: “g_pCompositor->m_explicitConfigPath = configPath;”; S169, pinned `S169.bin:427-435,493-520,227-235`, quotes: “ARGS[i] == "--instance" || ARGS[i] == "-i"”; “instanceSignature = overrideInstance;”; “getRuntimeDir() + "/" + instanceSignature + "/.socket.sock”]

The nested read depends on a backend being available: Aquamarine's startup returns false if no backend implementation starts. [S170, pinned `S170.bin:121-151`, quote: “if (implementations.empty() || started <= 0)”]

The a3w1 sentinel records a source-based, unexecuted boundary: because v4 removes standalone `exec` directives, a command launched by one that adds a bind through the `hyprctl keyword` API can create a runtime bind absent from the stripped oracle table. [observed: `.ufo/waves/round-25/a3w1/reports/SentOracleBoundary.md:7,36`]

That boundary is about standalone exec directives, not a normal bind whose dispatcher is `exec`; the sentinel says `bind = ..., exec, ...` is not matched by the strip rule. [observed: `.ufo/waves/round-25/a3w1/reports/SentOracleBoundary.md:36`]
