# SrcWalkerThemes — walker v2.17.2 default theme documents + theme selection

Seat: MadoR18.SrcWalkerThemes (scout), wave mado-r18-w1, 2026-10-20.
Scope: upstream source at tag v2.17.2 only. No host binary executed; no pacman,
systemctl, walker/elephant, or GUI command was run. Labels: **[OBS]** = read from a
fetched upstream body at the pin; **[INF]** = inference from that body; **[UNK]** =
unresolved. Host binaries stay [UNK]; version identity rests on a file read of
`/var/log/pacman.log` only.

## 0. Pin, receipts, reproducibility

- Upstream repo: `https://github.com/abenz1267/walker`.
- Tag pin: `refs/tags/v2.17.2` → commit **a515085fd39fae80acc086c8fbfd9b7771a9a11d**
  (lightweight tag: querying both `refs/tags/v2.17.2` and `refs/tags/v2.17.2^{}`
  returned only the direct ref). Raw output saved as
  `.ufo/waves/round-18/fetch/MadoR18.SrcWalkerThemes/walker-ls-remote-v2.17.2.txt`.
- Host package basis, **file read only**:
  `/var/log/pacman.log:2929` = `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`;
  `/var/log/pacman.log:3095` = `[2026-10-20T09:31:03-0300] [ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)`.
  A tag proves source, never the host binary [OBS/INF].
- Fetch receipts (R17-V3): **34 receipts**, all `http_status` 200, one JSON line each in
  `.ufo/waves/round-18/fetch/MadoR18.SrcWalkerThemes/receipts.jsonl`; every saved body
  re-hashed byte-equal to its `sha256` field. Largest body 822,620 B (docs.rs source view; under the 1 MiB cap).
  No tool was installed or upgraded for this item.
  All walker URLs are tag-pinned
  `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/<path>`; the tree listing is
  commit-pinned `api.github.com/repos/abenz1267/walker/git/trees/a515085…?recursive=1`
  (`truncated: false`); xdg dependency docs are `docs.rs/xdg/3.0.0/…`, corroborated by the
  crate's source view (`xdg-base-directories-rs.html:2027`, the same doc comment).
- Spot cross-check (read-only) of sibling w1 reports: `SrcWalkerReadme.md`,
  `SrcWalkerConfigPaths.md` and `SrcWalkerDefaultConfig.md` state the same README:219/225,
  `config.toml:9` and `mod.rs:56/66-75` facts; no contradiction found. The drafted
  `walker-route-r18.md:33` cites `docs.rs/xdg/latest`; the version pinned by
  `Cargo.lock:2705-2707` is 3.0.0 and its body here carries the same sentence, so a
  version-pinned row is available if L1 wants one.
- Root of `resources/themes/default/` at the pin: **19 files** [OBS tree]:

| file | bytes | sha256[:16] |
|---|---:|---|
| style.css | 2841 | 5829f472a3a6fc66 |
| layout.xml | 6729 | 55106a1ce3b6a477 |
| keybind.xml | 869 | 1233d0b1a258dc19 |
| preview.xml | 602 | 073a912e3eee9524 |
| item.xml | 2421 | d6dac24c66c6e851 |
| item_actionsmenu.xml | 2577 | ee18aeaa319a34b4 |
| item_aptpackages.xml | 1973 | e9613245a50e92f6 |
| item_archlinuxpkgs.xml | 1973 | e9613245a50e92f6 |
| item_bookmarks.xml | 2638 | 6a3f108d419a8130 |
| item_calc.xml | 2412 | ece4a09405b837a6 |
| item_clipboard.xml | 2174 | b3597b72d3b51ecb |
| item_dmenu.xml | 1572 | 4fe8af0457cdf163 |
| item_dnfpackages.xml | 1973 | e9613245a50e92f6 |
| item_files.xml | 2246 | 8ded6a2cc65c1c8c |
| item_providerlist.xml | 2422 | 4de69a8744729c5a |
| item_symbols.xml | 1733 | 2fae16af71969dca |
| item_symbols_grid.xml | 1152 | 03e6cf15e64e440c |
| item_todo.xml | 1764 | f644e39d569bebdb |
| item_unicode.xml | 1733 | 34ef99fced5e26a3 |

There is no `style.scss` in the default theme [OBS tree]. All 19 bodies are in the fetch dir: the five root documents under a `default-` prefix
(`default-style.css`, `default-layout.xml`, `default-keybind.xml`, `default-preview.xml`,
`default-item.xml`) and the 14 provider items under their own names (`item_calc.xml`, …).

## 1. `style.css` — the default CSS document [OBS]

- Starts with five GTK color tokens, `default-style.css:1-5` (first line:
  `@define-color window_bg_color #1f1f28;`).
- No `@import` at all: the default theme is standalone; the file's 2,841 B are
  self-contained rules.
- 45 top-level `selector {` blocks (reproducible crude count:
  `grep -c '^[^ @].*{' default-style.css`). It targets the GTK classes the layout XML
  attaches: `popover`, `.box-wrapper`, `.search-container`, `.input`, `.list`,
  `.item-box`, `.item-quick-activation`, `.item-text-box`, `.item-subtext`,
  `.item-image-text`, `.preview`, `.calc`, `.symbols`, `.todo`, `.keybinds`,
  `.keybind*`, `.error` and others.
- The compiled-in copy is the same file: `src-theme-mod.rs:260` embeds
  `resources/themes/default/style.css` with `include_str!` for the fallback path.

## 2. Layout documents [OBS]

All four are GTK4 builder XML (`<interface><requires lib="gtk" version="4.0">`).

- `layout.xml` (6,729 B) — the whole window, keyed by object id. 15 unique ids:
  `Window`, `BoxWrapper`, `SearchContainer`, `Input`, `ContentContainer`, `Preview`,
  `List`, `Scroll`, `Placeholder`, `Keybinds`, `GlobalKeybinds`, `ItemKeybinds`,
  `ElephantHint`, `Error`. The wrapper fixes size at `layout.xml:19-20`:
  `<property name="width-request">600</property>` and
  `<property name="height-request">570</property>`.
- `keybind.xml` (869 B) — one keybind hint tree: `Keybind` → `KeybindButton` →
  `KeybindLabel`, plus `KeybindBind` (`default-keybind.xml:4`).
- `preview.xml` (602 B) — `PreviewBox` (500×300) → `PreviewStack`
  (`default-preview.xml:4`).
- `item.xml` (2,421 B) — the default list-row layout, ids `ItemBox`, `ItemImageFont`,
  `ItemImage`, `ItemTextBox`, `ItemText`, `ItemSubtext`, `QuickActivation`
  (`default-item.xml:4`).
- 14 `item_*.xml` files ship in the default theme directory, including the two symbols
  variants. `item_symbols.xml`/`item_symbols_grid.xml` are also embedded by the symbols
  provider itself (`src/providers/symbols.rs:21-27`); the other 12 are read only when
  the default theme is loaded from disk in elephant mode (the compiled-in per-provider
  default is `item.xml`, `src/providers/mod.rs:132-138`).

Missing objects are surfaced by the binary as theme errors, not silently: for example
`set_error("Theme: missing 'Keybind' object"…` (`src-ui-window.rs:1430`).

## 3. How a theme is selected [OBS source chain]

1. `startup()` scans raw argv for `-t`/`--theme` and passes the value to `init_ui`
   (`src-main.rs:788-800`, call at `:809`).
2. `init_ui` applies precedence `CLI theme > config theme > literal "default"`
   (`src-main.rs:110-120`):

   ```rust
   let mut theme = if theme.is_empty() {
       get_config().theme.as_str()
   } else {
       theme
   };

   if theme.is_empty() {
       theme = "default";
   }

   set_theme(theme.to_string());
   ```

3. `setup_themes(elephant && !dmenu, get_theme(), is_service());`
   (`src-main.rs:135`). In service mode every theme directory under every root is
   loaded; otherwise only `<root>/<theme>` is tried (`src-theme-mod.rs:91-125`).
4. The CLI option is validated in the `command-line` handler, after startup:
   `has_theme(theme)` → accept, else print and fall back to the literal default
   (`src-main.rs:424-432`):

   ```rust
   cmd.print_literal("theme not found. using default theme.\n");
   set_theme("default".to_string());
   ```

   `available_themes` is the set that `setup_themes` filled via `add_theme`
   (`src-state-mod.rs:539-556`).
5. `activate` (entered from `app.activate()` at `src-main.rs:622`) loads CSS for the
   current name: `setup_css(get_theme());` (`src-main.rs:657`) and windows were built per loaded theme at startup
   (`src-ui-window.rs:368-383`); lookup falls back to the `"default"` window
   (`src-ui-window.rs:117-131`, else `println!("default theme not found");` at `:127`).
6. Config key and upstream default (`resources/config.toml:9`):

   `theme = "default"                  # theme to use`

Net precedence: `-t/--theme` if it names a loaded theme; otherwise the `theme` config
value; otherwise `"default"`. A bad `-t` value lands on `"default"`, not on the config
theme [OBS code order; INF].

## 4. Where custom themes live [OBS code + xdg 3.0.0 docs]

- Discovery is one call (`src-theme-mod.rs:56`):

  ```rust
  let dirs = xdg::BaseDirectories::with_prefix("walker").find_config_files("themes");
  ```

- The dependency is `xdg = "3.0.0"` (`Cargo.toml:30`), pinned in `Cargo.lock:2705-2707`.
  Its documented semantics, quoted verbatim from
  `xdg-basedirectories.html:356`:
  "Given a relative path path, returns an iterator yielding absolute paths to existing
  configuration files, in XDG_CONFIG_DIRS and XDG_CONFIG_HOME." and "Paths are produced
  in order from lowest priority to highest."
  And `:310`: "Same as new(), but prefix is implicitly prepended to every path that is
  looked up."
- Therefore the upstream search roots are [OBS-doc + INF of prefix]:
  `${XDG_CONFIG_HOME:-~/.config}/walker/themes/<theme>/` and each
  `${XDG_CONFIG_DIRS:-/etc/xdg}/walker/themes/<theme>/`.
  Later roots win on a name collision because the load loop keeps overwriting the map
  entry and never breaks (`src-theme-mod.rs:91-105`).
- An extra root can be appended (`src-theme-mod.rs:60-63`):

  ```rust
  config_paths.push(PathBuf::from(a.replace("~", &home).to_string()));
  ```

  Key: `additional_theme_location` (`src-config.rs:41,102,306-307`). It is **not**
  mentioned in the fetched `README.md` or `resources/config.toml` (grep: zero hits)
  [OBS absence in those bodies].
- The theme name is the directory basename: non-service `path.push(&theme)`
  (`:96`), service iterates `read_dir` and uses `file_name()` (`:107-125`).
- Recognized documents in a theme directory (`src-theme-mod.rs:66-75`):
  `layout.xml`, `keybind.xml`, `style.scss`, `style.css`, `preview.xml`; plus
  `item_<provider>.xml` when `elephant && !dmenu` is true (`:77-89`).
- Upstream README statements, verbatim:
  - `README.md:213`: "Configuration should be done in `~/.config/walker`."
  - `README.md:219`: "Themes inherit the default theme by default, so if you just want
    to change the CSS, you can just create `themes/yours/style.css`."
  - `README.md:221`: "You can customize rendering of list items for each provider
    individually, f.e. "item_files.xml" will define the layout for items sourced from
    the `files` provider."
  - `README.md:225`: "You can set the default theme in your `config.toml` f.e.
    `theme = "yours"`."
- So a user theme is `~/.config/walker/themes/<name>/` with any subset of those files;
  a system theme is `/etc/xdg/walker/themes/<name>/`; extra roots come only from
  `additional_theme_location` [OBS/INF].

## 5. Inheritance and CSS precedence [OBS code]

- `Theme::default()` is the in-binary base: `layout.xml`, `keybind.xml`, `preview.xml`
  are `include_str!`-embedded (`src-theme-mod.rs:32-34`), and every provider seeds
  `items`/`grid_items` from its compiled-in item template (`:40-49`). Provider trait
  defaults embed `resources/themes/default/item.xml` for both list and grid
  (`src/providers/mod.rs:132-138`); symbols overrides both with
  `item_symbols.xml`/`item_symbols_grid.xml` (`src/providers/symbols.rs:21-27`).
- A directory theme starts from that base and overwrites only present parts:
  `let mut theme = Theme::default();` (`src-theme-mod.rs:147`). This is the mechanism
  behind the README inheritance sentence [OBS].
- The compiled-in `default` theme is inserted only if no directory theme already owns
  the name (`src-theme-mod.rs:132-135`), so a `themes/default/` directory shadows it.
- CSS order in `setup_css` (`src-theme-mod.rs:234-261`): `style.scss` compiled with
  grass using the theme directory as load path (`:241-246`), else `style.css` loaded by
  `gio::File` (`:257`), else the embedded default stylesheet (`:260`).
- Three code-level caveats (unexercised, noted for the route note):
  - `style.scss` and `style.css` slots are assigned for a theme directory whether or
    not the files exist (`:165-174`), so the embedded-CSS `else` branch is reachable
    only for the compiled-in default entry (`css = None`). A directory theme without
    `style.css` points `load_from_file` at a missing path [OBS code; INF runtime].
  - A `style.scss` parse error prints `SCSS parse error: {err}` and returns before the
    CSS / embedded fallbacks (`:249-252`) [OBS].
  - The config `theme` value is never validated (`handle_command_line` checks only the
    CLI value, `src-main.rs:424-432`). If a config-selected directory is absent,
    `setup_css` finds no map entry and takes no CSS branch (`src-theme-mod.rs:235-237`),
    while `with_window` falls back to the default window (`src-ui-window.rs:117-131`);
    the plausible result is an unstyled default layout [OBS code; INF runtime].
- Two theme-directory names cannot be loaded at this pin: plain `item.xml` and
  `item_<provider>_grid.xml`. Both have match arms (`:160-164`, `:190-207`) but never
  appear in the `files`/`combined` vectors (`:66-89`), so a theme directory cannot
  supply them at v2.17.2 [OBS list construction; INF effect]. Per-provider item templates are also only read
  when the first `setup_themes` argument is true, i.e. `elephant && !dmenu`
  (`src-main.rs:122-135`) [OBS].

## 6. Host declaration (P3/P5 note material)

- Walker package version on this host: `2.17.2-1`, read as bytes from
  `/var/log/pacman.log:2929` (upgrade at 2026-10-20T09:16:46-0300). Elephant companion:
  `2.22.1-1`, `/var/log/pacman.log:3095`. No package query was run (host pause).
- Whether the packaged `/etc/xdg/walker/themes/…` tree and the host
  `~/.config/walker/config.toml` values match this source contract was not inspected by
  this seat: **[UNK]** here; see the lane's host-surface seats (`SrcWalkerConfigPaths.md`
  and `SrcWalkerReadme.md` carry file-read observations of the host theme bases). Do not
  promote the tag to a binary claim.

## 7. Suggested source rows for the two C2 route notes (drafts: `S0xx-pending`)

L1 assigns S072-S099; these are field-complete proposals, each with a raw-body
receipt line in `fetch/MadoR18.SrcWalkerThemes/receipts.jsonl` (bodies on disk for L1
to commit). Proposed tier: A (upstream code/docs).

For `corpus/knowledge/walker-route-r18.md` (`surface: P3`):

| draft row | source (https, tag-pinned) | body:anchor | used-by | scope cell (names walker) |
|---|---|---|---|---|
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md` | `readme-md.txt:213,219-225` | walker-route-r18.md | walker launcher config/theming (`~/.config/walker`, `theme=`) |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs` | `src-theme-mod.rs:53-138` | walker-route-r18.md | walker theme discovery roots + `walker/themes` loading |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/main.rs` | `src-main.rs:110-135,424-432,657,788-809` | walker-route-r18.md | walker theme selection precedence and validation |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml` | `walker-config-toml.txt:9` | walker-route-r18.md | walker default `theme = "default"` |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/ui/window.rs` | `src-ui-window.rs:117-131,368-383` | walker-route-r18.md | walker per-theme window and default fallback |
| S0xx-pending | `https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html` | `xdg-basedirectories.html:310,356` | walker-route-r18.md | XDG config-root lookup used by walker |

For `corpus/knowledge/theme-route-r18.md` (`surface: P5`):

| draft row | source (https, tag-pinned) | body:anchor | used-by | scope cell (names theme) |
|---|---|---|---|---|
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/themes/default/style.css` | `default-style.css:1-5` | theme-route-r18.md | walker GTK4 theme CSS color tokens and classes |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/themes/default/layout.xml` | `default-layout.xml:1-20` | theme-route-r18.md | walker theme layout XML object ids and size |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/themes/default/keybind.xml`, `preview.xml`, `item.xml` | `default-keybind.xml:4`; `default-preview.xml:4`; `default-item.xml:4` | theme-route-r18.md | walker theme layout fragments (keybind/preview/item) |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md` | `readme-md.txt:219-225` | theme-route-r18.md | theme inheritance and `theme = "yours"` selection |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs` | `src-theme-mod.rs:29-51,140-232,234-261` | theme-route-r18.md | theme inheritance, part overrides, scss/css precedence |
| S0xx-pending | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/providers/mod.rs` + `src/providers/symbols.rs` | `src-providers-mod.rs:132-138`; `src-providers-symbols.rs:21-27` | theme-route-r18.md | default theme item templates |

Note for the scribes: C2 needs the note's first 15 lines to carry `source:` lines whose
used-by names the note, and at least one upstream https docs/spec/code row naming
walker/elephant (P3) or theme/wallpaper/swaybg (P5) in its source **or scope** cell —
the rows above satisfy the source-cell half via the `walker` path segment; keep the P5
scope cell word "theme" so it satisfies the other half.

## 8. Quote/anchor index (each quote ≤25 words, verbatim)

| quote | anchor |
|---|---|
| "Configuration should be done in `~/.config/walker`." | `readme-md.txt:213` |
| "Themes inherit the default theme by default, so if you just want to change the CSS, you can just create `themes/yours/style.css`." | `readme-md.txt:219` |
| "You can set the default theme in your `config.toml` f.e. `theme = "yours"`." | `readme-md.txt:225` |
| `let dirs = xdg::BaseDirectories::with_prefix("walker").find_config_files("themes");` | `src-theme-mod.rs:56` |
| "Given a relative path path, returns an iterator yielding absolute paths to existing configuration files, in XDG_CONFIG_DIRS and XDG_CONFIG_HOME." | `xdg-basedirectories.html:356` |
| "Paths are produced in order from lowest priority to highest." | `xdg-basedirectories.html:356` |
| "Same as new(), but prefix is implicitly prepended to every path that is looked up." | `xdg-basedirectories.html:310` |
| `config_paths.push(PathBuf::from(a.replace("~", &home).to_string()));` | `src-theme-mod.rs:63` |
| `cmd.print_literal("theme not found. using default theme.\n");` | `src-main.rs:430` |
| `theme = "default"                  # theme to use` | `walker-config-toml.txt:9` |
| `<property name="width-request">600</property>` | `default-layout.xml:19` |
| `<property name="height-request">570</property>` | `default-layout.xml:20` |
| `println!("default theme not found");` | `src-ui-window.rs:127` |
| `"theme '{}' not found. falling back to default"` | `src-ui-window.rs:1417` |

## 9. Verification (runnable by L1; no host services touched)

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/fetch/MadoR18.SrcWalkerThemes
# 1. every receipt body is byte-identical to its digest, all 200s
python3 - <<'PY'
import json,hashlib
rs=[json.loads(l) for l in open('receipts.jsonl')]
assert all(r['http_status']==200 for r in rs)
for r in rs:
    assert hashlib.sha256(open(r['body'],'rb').read()).hexdigest()==r['sha256'], r['body']
print(len(rs),'receipts verified')
PY
# 2. tag pin
git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'
# 3. quote anchors (read-only)
sed -n '213p;219p;225p' readme-md.txt
sed -n '56p;60,63p;66,75p;132,135p;147p;165,174p;234,261p' src-theme-mod.rs
sed -n '110,120p;135p;424,432p;657p' src-main.rs
```

## 10. Remaining unknowns

- [UNK] GTK4 handling of the `@import` relative climb used by the host's omarchy theme
  (`walker.css`): upstream default has no `@import`; not exercised (no walker run).
- [UNK] grass SCSS compile output for a theme that ships `style.scss`; read only.
- [UNK] service-mode runtime theme switching: who calls `setup_css`/`set_theme` from the
  menus provider, and runtime confirmation of the no-CSS outcome for a config-selected
  theme name that has no directory.
- [UNK] host `~/.config/walker/config.toml` theme/additional_theme_location values and
  the packaged `/etc/xdg/walker/themes` tree (not inspected by this seat).
- [UNK] whether the Arch package build patches any of these paths or embeds a different
  default theme than the tag (AUR PKGBUILD not fetched).
- [INF, unexercised] two upstream oddities above: missing-`style.css` directory themes
  and the unreachable `item.xml`/`item_*_grid.xml` directory overrides.
