# ScoutS201 — Waybar 0.15.0 `hyprland/backend.cpp` re-fetch

## Fetch & integrity

- Source: `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp`
- Saved to: `.ufo/waves/round-34/scratch/ScoutS201/backend.cpp`
- `curl -fsSL` succeeded (exit 0).
- sha256: `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e` — **match**
- Byte length: `6550` — **match**

## Substring location

Substring `$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr`:

- **Line (1-based):** 38 — `spdlog::warn("$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr");`
- **Enclosing function:** `std::filesystem::path IPC::getSocketFolder(const char* instanceSig)` (opens line 19)

### Three lines before (35–37)

```cpp
  if (!xdgRuntimeDir.empty() && std::filesystem::exists(xdgRuntimeDir / "hypr")) {
    socketFolder_ = xdgRuntimeDir / "hypr";
  } else {
```

### Three lines after (39–41)

```cpp
    socketFolder_ = std::filesystem::path("/tmp") / "hypr";
  }

  socketFolder_ = socketFolder_ / instanceSig;
```

## Notes

- Occurrence count: 1 (grep -F, whole file).
- Semantics: when `XDG_RUNTIME_DIR` unset/empty or `$XDG_RUNTIME_DIR/hypr` missing, Waybar falls back to `/tmp/hypr/<instanceSig>` for the Hyprland IPC socket folder.
