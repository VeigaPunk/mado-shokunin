# Receipts — independent fetch + quote locations (seat R56W2ScoutRows4, 2026-10-28)

## Independent upstream fetch (curl, scratch)

```
$ curl -sSL --max-time 90 -o up-MiscFunctions.cpp -w 'HTTP %{http_code} %{size_download}B\n' \
    'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp'
HTTP 200 29785B
$ sha256sum up-MiscFunctions.cpp && wc -lc up-MiscFunctions.cpp
065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9  up-MiscFunctions.cpp
  844 29785 up-MiscFunctions.cpp

$ curl -sSL --max-time 90 -o up-HyprCtl.cpp -w 'HTTP %{http_code} %{size_download}B\n' \
    'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp'
HTTP 200 97582B
$ sha256sum up-HyprCtl.cpp && wc -lc up-HyprCtl.cpp
798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa  up-HyprCtl.cpp
 2346 97582 up-HyprCtl.cpp
```

## Lane pin blobs at the scored commit (read-only git)

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 28fc86ac2359ec27406d8a2c63bef82ea6e947ed:.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp | sha256sum
065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9  -        (844 lines, 29785 B)
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 28fc86ac2359ec27406d8a2c63bef82ea6e947ed:.ufo/waves/round-56/fetch/Hyprland-HyprCtl.cpp | sha256sum
798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa  -        (2346 lines, 97582 B)
```

Pin == upstream byte-for-byte; equals row anchor sha256 and frozen-tables-v2.json `c1.pin_sha256`.

## Gate quotes located in the upstream bytes (exact line, substring match)

S388 (gate.md claims pin lines 65 and 68):
```
65:        static const char* const ENVHOME = getenv("HOME");
68:        auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));
```
S389 (gate.md claims pin lines 1223 and 1276):
```
1223:    if (COMMAND.contains("misc:disable_autoreload"))
1224:        Config::watcher()->update();
1276:    Config::mgr()->reload();
```
E-row lines also verified present:
```
66:        value.replace(0, 1, std::string(ENVHOME));          (E01, S388)
1190:    std::string retval = mgr->parseKeyword(COMMAND, VALUE); (E04, S389)
```

## Context showing anchor-locator bounds and branch shape

MiscFunctions.cpp 61-80 (absolutePath): `~` test at 64, HOME getenv at 65, leading-char replace at 66,
relative branch at 67, currentDir cut at last slash at 68, currentDir used as base at 74-79.
HyprCtl.cpp: keywordRequest handler 1185-1258 (parseKeyword 1190, contains-check 1223 -> watcher update 1224);
reloadRequest 1260-1279: `if (request.ends_with("full-reset"))` at 1262, full-reset branch returns "ok" at 1273,
fall-through (not full-reset) reaches `Config::mgr()->reload();` at 1276, returns "ok" at 1278.

## Anchor-locator EOF bound (registration-v2 E3 rule: len(blob.split(b"\n")))

```
pin-Hyprland-MiscFunctions.cpp split-lines: 845   max locator: 68    past-eof: False
pin-Hyprland-HyprCtl.cpp     split-lines: 2347   max locator: 1276  past-eof: False
```

## Census validate (scratch copy of registry at 28fc86ac)

```
$ TMPDIR=<scratch> /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file <scratch>/SOURCES-at.md
lines mentioning the attacked rows:
  W04  S388 duplicate url .../src/helpers/MiscFunctions.cpp across scopes   (partners: S182, S321)
  W04  S389 duplicate url .../src/debug/HyprCtl.cpp across scopes           (partners: S158, S307, S320, S366)
  E11  S388 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
  E11  S389 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
```
E11 is a `--file` scratch-mode artifact: the script tests `[ -e "$dir/$path" ]` relative to the
registry copy's directory, so EVERY mined row E11s (S001 through S391). The used-by blob exists at
the scored commit: `git cat-file -e 28fc86ac:corpus/knowledge/hyprland-config-autoreload-r56.md` -> EXISTS.
Full output: `census-validate.out` (this directory). Rerun byte-identical (cmp exit 0); exit code
nonzero (1) in this mode because of the artifact E11s.
