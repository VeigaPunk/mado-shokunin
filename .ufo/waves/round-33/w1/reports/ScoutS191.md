# ScoutS191 — window.cpp re-fetch and staged-row check

Scope: re-fetch `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp` to `.ufo/waves/round-33/scratch/ScoutS191/S191.bin`, verify sha256, locate `m_ipc.registerForIPC("activewindow", this);`, list the other `registerForIPC` names in the constructor, and check whether the staged S191 row's markup claim is in the bytes.

## Fetch and hash — CONFIRMED

```
$ curl -fsSL -o .ufo/waves/round-33/scratch/ScoutS191/S191.bin https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp && sha256sum .ufo/waves/round-33/scratch/ScoutS191/S191.bin
5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846  .ufo/waves/round-33/scratch/ScoutS191/S191.bin
```

Matches the frozen digest `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846` (c1/frozen.json S191 entry). `wc -c` reports **8324 B**, matching the staged row's "8324 B".

## Target line — PRESENT at line 27

```
$ grep -nF 'm_ipc.registerForIPC("activewindow", this);' .ufo/waves/round-33/scratch/ScoutS191/S191.bin
27:  m_ipc.registerForIPC("activewindow", this);
```

## Constructor registerForIPC names (Window::Window, lines 20–38)

```
27:  m_ipc.registerForIPC("activewindow", this);
28:  m_ipc.registerForIPC("closewindow", this);
29:  m_ipc.registerForIPC("movewindow", this);
30:  m_ipc.registerForIPC("changefloatingmode", this);
31:  m_ipc.registerForIPC("fullscreen", this);
```

Besides `activewindow`: **`closewindow`, `movewindow`, `changefloatingmode`, `fullscreen`** — five registrations total. (`unregisterForIPC` at line 42 is the destructor.) The staged row's phrase "subscribes to `activewindow` and `closewindow`" is true but understates: three more events are registered in the same block.

## Markup claim — IN THE BYTES

Staged S191 row (SOURCES.append.md line 12) claims: text built from `title`, `initialTitle`, `class`, `initialClass` placeholders, rewrite rules applied, result set as GTK markup. Verified:

```
$ grep -n 'set_markup\|rewriteString\|fmt::format' .ufo/waves/round-33/scratch/ScoutS191/S191.bin
58:    label_text = waybar::util::rewriteString(
59:        fmt::format(fmt::runtime(format_), fmt::arg("title", windowName),
60:                    fmt::arg("initialTitle", windowData_.initial_title),
61:                    fmt::arg("class", windowData_.class_name),
62:                    fmt::arg("initialClass", windowData_.initial_class_name)),
63:        config_["rewrite"]);
64:    label_.set_markup(label_text);
76:          fmt::format(fmt::runtime(tooltip_format), fmt::arg("title", windowName),
```

All four placeholders (lines 59–62), `rewriteString` over `config_["rewrite"]` (58, 63), and `label_.set_markup` (64) are present. Verdict: **PRESENT**.

## Cited line ranges

Row cites `window.cpp:22-28` (IPC registration) and `:54-64` (fmt + rewriteString + set_markup). Lines 27–28 sit inside 22–28; the `movewindow`/`changefloatingmode`/`fullscreen` registrations at 29–31 fall just outside the cited range but inside the same constructor block. The 54–64 range covers `windowData_.title` assignment through `set_markup` exactly.

## Verdicts

- sha256: MATCH (`5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846`)
- `m_ipc.registerForIPC("activewindow", this);`: line **27**
- Other constructor registrations: `closewindow`, `movewindow`, `changefloatingmode`, `fullscreen`
- Markup claim in bytes: **PRESENT**
