# SrcWalkerConfigPaths — walker v2.17.2 user config/theme path resolution

Seat: MadoR18.SrcWalkerConfigPaths (scout). Assignment: at walker's 2.17.2 tag, locate
the source that resolves the user config/theme paths and fetch that raw file with a
receipt; record sha256 and exact lines. No behaviour exercised, no host binary opened.

All line anchors below are lines of the fetched bodies in
`.ufo/waves/round-18/fetch/SrcWalkerConfigPaths/` (byte-equal to the clone of the tag:
`sha256sum` of clone files matches both receipts).

## Tag → commit

- `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'`
  (run 2026-10-20) returned only `refs/tags/v2.17.2` = `a515085fd39fae80acc086c8fbfd9b7771a9a11d`;
  no peeled `^{}` line, i.e. an annotated-tag indirection is absent (lightweight tag).
- `git log -1` in a `--depth 1 --branch v2.17.2` clone in /tmp: commit
  `a515085fd39fae80acc086c8fbfd9b7771a9a11d`, 2026-10-08, subject
  `fix: GTK 4.24 blur handling causing crash`.
- Dependency pin read from `Cargo.toml:30`: `xdg = "3.0.0"` (crate tarball fetched, see receipts).

## Observed facts (code, at a515085…)

**F1 — user config file lookup.** `src/config.rs:218-223`:

```
    if let Some(user_config_path) =
        xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")
```

Quote (F1, ≤25 words): "xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")"
— a single `Option<PathBuf>`; builtins are loaded first from
`include_str!("../resources/config.toml")` (`src/config.rs:8`), then the user file is merged
(`config.rs:225-231`), then `WALKER_`-prefixed environment variables merge last
(`config.rs:234-240`, `Environment::with_prefix("WALKER").separator("_")`).

**F2 — theme directory lookup.** `src/theme/mod.rs:53-58`:

```
pub fn setup_themes(elephant: bool, theme: String, is_service: bool) {
    ...
    let dirs = xdg::BaseDirectories::with_prefix("walker").find_config_files("themes");

    let mut config_paths: Vec<PathBuf> = dirs.collect();
```

Quote (F2, ≤25 words): "let dirs = xdg::BaseDirectories::with_prefix("walker").find_config_files("themes");"
— plural iterator over *existing* `walker/themes` paths, one per searched config base.

**F3 — extra theme location.** `src/theme/mod.rs:60-63`:

```
    if let Some(a) = &get_config().additional_theme_location
        && let Ok(home) = env::var("HOME")
    {
        config_paths.push(PathBuf::from(a.replace("~", &home).to_string()));
```

Quote (F3, ≤25 words): "config_paths.push(PathBuf::from(a.replace("~", &home).to_string()));"
— textual replacement of every `~` with `$HOME`, not shell tilde expansion; the extra path is
appended **after** the XDG paths, and the loop inserts into a `HashMap` keyed by theme name,
so a later path wins over an earlier one with the same theme name.

**F4 — how each collected path is used.** `src/theme/mod.rs:91-130`:
non-service branch pushes the requested theme name onto each base
(`path.push(&theme)`, `mod.rs:95`) and loads it if it exists; service branch
(`is_service`, `mod.rs:107-129`) `fs::read_dir` each base and loads every subdirectory as a
theme named after the directory. `setup_theme_from_path` returns `None` when
`!path.exists()` (`mod.rs:140-145`). The five per-theme files are `layout.xml`,
`keybind.xml`, `style.scss`, `style.css`, `preview.xml` (`mod.rs:66-72`), plus
`item_<provider>.xml` only when `elephant && !dmenu` (`mod.rs:74-89`; call site `src/main.rs:135`).

**F5 — theme *name* selection.** `src/main.rs:110-120`: empty CLI theme falls back to
`get_config().theme`, then to the literal `"default"`. `src/main.rs:349-356` registers
`-t/--theme` ("theme to use"); `src/main.rs:424-432` accepts it only if `has_theme(theme)`,
otherwise prints `theme not found. using default theme.` and sets `"default"`. Builtin
default `resources/config.toml:9`: `theme = "default"`.

**F6 — xdg crate 3.0.0 semantics actually linked** (fetched tarball, extracted read-only in
/tmp; `src/base_directories.rs`):

- `with_prefix(prefix)` sets `user_prefix = prefix.join(profile)` and `shared_prefix = prefix`;
  `profile` is `""` here (`base_directories.rs:236-238`, `:326-329`).
- `find_config_file` checks `config_home/user_prefix/path` first, then each
  `config_dir/shared_prefix/path`, returning the **first** existing (`:757-777`, `:449-457`).
- `find_config_files` builds search dirs as `config_dirs.iter().rev()` followed by
  `config_home`, i.e. lowest priority first, user last (`:786-804`); it yields a candidate when
  `path_exists` — `fs::metadata(path).is_ok()`, so directories qualify (`:753-755`, `:807-818`).
  Doc quote (≤25 words): "returns an iterator yielding absolute paths to existing configuration
  files, in XDG_CONFIG_DIRS and XDG_CONFIG_HOME" (`:459-462`).
- Defaults when env vars are unset/relative: `config_home = $HOME/.config`,
  `config_dirs = [/etc/xdg]` (`:308-310`, `:321-323`).

**[INFERENCE]** (documented crate defaults applied to F1/F2 — not measured on a running binary):
effective config path `$XDG_CONFIG_HOME/walker/config.toml` (default
`~/.config/walker/config.toml`), theme bases `/etc/xdg/walker/themes` then
`$XDG_CONFIG_HOME/walker/themes`, then `additional_theme_location` (highest precedence).

## Host declaration (file-read only; nothing executed)

Read as file bytes on 2026-10-20; no walker/pacman/systemctl invocation:

- `/var/log/pacman.log:2929`: `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`
  — host package version 2.17.2-1, matching the tag's version string; **the installed binary's
  contents are [UNK]** (no binary/`--version` read; a tag is never proof of binary identity).
- `/home/vgpnk/.config/walker/` exists; only `config.toml` inside
  (sha256 `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`);
  `~/.config/walker/themes` **absent**.
- `config.toml:3`: `theme = "omarchy-default"   # theme to use`
- `config.toml:4`: `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`
- `/etc/xdg/walker/themes` exists with `default`; `/home/vgpnk/.local/share/omarchy/default/walker/themes/omarchy-default`
  exists (contains `layout.xml`, `style.css`).
- [INFERENCE] with this host config the only theme base containing `omarchy-default` is the
  extra location; the `/etc/xdg` `default` theme supplies the fallback name only. Whether the
  running walker resolved them this way is **unexercised** ([UNK]).

## Unexercised behavior / remaining unknowns

- `[UNK]` no walker process was started or queried; resolution order above is source+crate
  reading, not an observed resolution.
- `[UNK]` the installed binary at 2.17.2-1 may not be byte-equivalent to tag a515085… (distro
  patch/build flags unknown; `python -I` not run against it, no package file read).
- `[UNK]` effect of a theme directory that exists but lacks `layout.xml`/`style.css`
  (only `path.exists()` is checked at `mod.rs:139-146`; per-file failure paths not traced).
- `[UNK]` whether `WALKER_THEME` env key actually maps to `theme` (env merge is generic,
  `config.rs:235-242`; not tested).
- Not opened: any walker README/docs page (sibling seats cover those); host `/etc/xdg/walker/config.toml`.

## Receipts

Directory `.ufo/waves/round-18/fetch/SrcWalkerConfigPaths/`; one JSON line per fetch in
`receipts.jsonl` (`mado-fetch-receipt-v1`), curl 8.23.0:

| body | url | http | bytes | sha256 |
|---|---|---|---|---|
| `theme-mod.rs` | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs | 200 | 9364 | `93287a1c389a4b1856e2736e16246cef90691074023f57521fbb1422a61e0349` |
| `config.rs` | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs | 200 | 19675 | `93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469` |
| `xdg-3.0.0.crate` | https://static.crates.io/crates/xdg/xdg-3.0.0.crate | 200 | 15821 | `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5` |

The `.crate` body is a gzip tar; member anchors quoted above come from
`xdg-3.0.0/src/base_directories.rs` after extraction into `/tmp/xdg3` (no lane write).

## Proposed SOURCES rows (L1 assigns ids; `S0xx-pending`)

Row A — walker themes source:
source `walker v2.17.2 theme path resolution — https://github.com/abenz1267/walker/blob/v2.17.2/src/theme/mod.rs`;
kind `code`; tier `A`; scope "walker config-XDG theme-directory resolution and
`additional_theme_location` precedence, not host behaviour"; anchor
`setup_themes :53-127, find_config_files :56, ~→$HOME :60-63` @ v2.17.2 a515085fd39fae80acc086c8fbfd9b7771a9a11d
(raw sha256 93287a1c389a4b18…); teaches "theme bases are existing `walker/themes` under
XDG config dirs with the user dir last, extra location appended last, name from
`--theme`→`config.theme`→`default`"; status `mined`; recheck `on-release`; used-by `—` (L1/route seat decides).

Row B — walker config file source:
source `walker v2.17.2 config load — https://github.com/abenz1267/walker/blob/v2.17.2/src/config.rs`;
kind `code`; tier `A`; scope "single `config.toml` resolution and env merge order";
anchor `DEFAULT_CONFIG :8, find_config_file("config.toml") :218-223, WALKER_ env :235-242` @ a515085…;
teaches "one user config file, XDG_CONFIG_HOME ahead of XDG_CONFIG_DIRS, merged over builtin
defaults then WALKER_* env"; status `mined`; recheck `on-release`; used-by `—`.

Row C (optional, supports A/B semantics): `xdg 3.0.0 crate source — https://static.crates.io/crates/xdg/xdg-3.0.0.crate`,
kind `code`, tier `A`, scope "documented search order and default config base for the pinned
dependency", anchor `base_directories.rs:236-238, 308-310, 321-323, 449-471, 753-818`, raw
sha256 `2fb433233f2df934…`; teaches the exact precedence the walker calls inherit. Use only if
L1 wants the crate-level anchor as its own row rather than folded into A.

## Limits

Tag-pinned raw files come from the GitHub mirror of the tag; lightweight tag means the commit
binding rests on GitHub's `refs/tags/v2.17.2` advertisement (recorded above), no signature
verification and no tarball checksum from upstream releases. No source claim here is evidence
of host binary contents or of any observed theme load.
