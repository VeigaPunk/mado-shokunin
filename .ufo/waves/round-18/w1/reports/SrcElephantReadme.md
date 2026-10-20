# SrcElephantReadme — upstream elephant @ v2.22.1: README, wire contract, provider and config inventory

Seat: SrcElephantReadme (leaf scout, round 18 wave 1). Lane root `mado-shokunin`.
Method: HTTP GET of tag/commit-pinned raw files only; `git ls-remote` for tag→commit;
host facts by FILE READ (`/var/log/pacman.log`, config trees, `/usr/lib/elephant`) only.
No host binary was executed; no pacman/yay/systemctl/hyprctl/walker/elephant/omarchy
command was run; HOST PAUSE respected. All 16 fetched bodies and their receipts are
staged under `.ufo/waves/round-18/fetch/SrcElephantReadme/` (300 KB).

Deliverable answers: tag→commit, README sha256, what elephant does, how walker talks to
it, provider list, config location. One documentation defect found (socket path).

## 1. Upstream identity (observed)

Repository: `https://github.com/abenz1267/elephant` (Go, GPLv3 per README L5).

Tag → commit, measured 2026-10-20 (UTC) with:

```
$ git ls-remote https://github.com/abenz1267/elephant \
    'refs/tags/v2.22.1' 'refs/tags/v2.22.1^{}'
8f1e21d6efe40b8b3953f95b9574f99f717caf91	refs/tags/v2.22.1
```

Only one line: `v2.22.1` is a **lightweight tag**, so the tag ref is the commit
`8f1e21d6efe40b8b3953f95b9574f99f717caf91`. Control: the same query for `v2.22.0`
returned both the annotated tag object `e5cdc169062496475d393e02d54b230cb1ba5cf8` and
its peel `8e77c59ca5b7fd28c0a168535f1a1c000e6b5389`, so the absence of a `^{}` line for
`v2.22.1` is evidence, not truncation.

README artifact (the assignment's primary fetch):

| field | value |
|---|---|
| url | `https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md` |
| http | 200, final URL identical |
| bytes | 6969 (278 lines, 189 non-blank) |
| sha256 | `aa19a7e2d1c07bf1852b65fd38ca24a6b04bba0dacfd9f6cb02ada0ee0b61389` |
| body | `fetch/SrcElephantReadme/README.md.body` |
| receipt | `fetch/SrcElephantReadme/receipts.jsonl` line 1 (schema `mado-fetch-receipt-v1`) |

Secondary identity used only to answer "how walker talks to it": walker
`https://github.com/abenz1267/walker` tag `v2.17.2` → commit
`a515085fd39fae80acc086c8fbfd9b7771a9a11d` (same `ls-remote` form; also a single line,
lightweight). Walker README is 7926 bytes / 233 lines, sha256
`9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456`.
Walker `Cargo.toml` L15 pins `protobuf = "3.7.2"`.

Receipt ledger (16 lines, every `http_status` 200, one body per line):
`README.md.body`, `walker-README.md.body`, `tree.json.body`, `walker-tree.json.body`,
`elephant-comm.go.body`, `elephant-handlers-common.go.body`,
`elephant-handlers-query.go.body`, `elephant-providers-load.go.body`,
`elephant-common-config.go.body`, `elephant-common-files.go.body`,
`elephant-common-util.go.body`, `elephant-provider-menus-README.md.body`,
`walker-Cargo.toml.body`, `walker-src_data.rs.body`, `walker-build.rs.body`,
`walker-src_protos_mod.rs.body`.
Full sha256 per body is in the receipts file and repeated in §9.

Not receipted (404 probes, never credited): `docs/config.md` and root `Cargo.toml` both
404 at this tag — elephant is Go, and config docs are generated, not shipped (§6).

## 2. What elephant is (verbatim, ≤25 words each)

- `README.md:3` — "**Elephant** - _cuz it's phat_ - is a powerful data provider service
  and backend for building custom application launchers and desktop utilities."
- `README.md:9` — "Elephant acts as a unified backend service that aggregates data from
  various sources (desktop applications, files, clipboard history, etc.)".
- `README.md:200` — "Elephant uses Unix domain sockets for IPC and Protocol Buffers for
  message serialization."
- `README.md:202-205` — four message classes: Query, Activation, Menu, Subscribe
  ("**Subscribe Messages**: Listen for real-time updates").
- `README.md:211` — "Connect to the Unix socket (typically at `/tmp/elephant.sock`)"
  (see §4: this sentence is stale against the code at the same tag).

Reading of the README alone: elephant is a passive provider daemon; it does not draw UI.
Its documented consumers are "frontend applications like custom launchers, productivity
tools, or desktop widgets" (`README.md:9`). It never names walker — the word "walker"
does not occur anywhere in the 278-line file (grep, 0 hits).

## 3. How walker talks to it (observed in code, both sides)

The relationship is frontend→daemon, not peer-to-peer:

- walker `README.md:13` — "The following Elephant providers are implemented by default:"
  (the feature list that follows is elephant providers).
- walker `README.md:59` — "make sure elephant is running before starting Walker".
- walker `README.md:23` — "Create custom menus with elephant and let walker display them".
- walker `README.md:163` — "**Make sure `elephant` is running and you have providers
  installed. `elephant-providerlist` and f.e. `elephant-desktopapplications`.**"

Transport and addressing:

- Client: walker `src/data.rs:148-169` `init_socket()` builds the socket path from
  `env::var("XDG_RUNTIME_DIR")` (fallback `env::temp_dir()`), pushes `"elephant"` then
  `"elephant.sock"`, then `wait_for_file(...)` (`:164`) before `UnixStream::connect`
  (`:169`). Walker opens separate connections per concern: query `CONN`
  (`data.rs:182`), menu `MENUCONN` (`:194`, same socket path at `:185`), and
  `BLUETOOTHCONN` when the bluetooth provider is present (`:196-208`).
- Server: elephant `internal/comm/comm.go:38-45` computes exactly the same path —
  `$XDG_RUNTIME_DIR/elephant/elephant.sock`, falling back to
  `$TMPDIR/elephant/elephant.sock` only when `XDG_RUNTIME_DIR` is empty; `:47`
  `os.MkdirAll(dir, 0o755)`; `:61-63` `net.ListenUnix("unix", {Name: Socket})` after
  `os.Remove(Socket)` at `:59`.

Request frame (elephant reads it at `comm.go:85-127`): `[type:u8][format:u8][len:u32 BE]
[payload]`. Registry positions at `comm.go:27-35`: `0 Query`, `1 Activate`, `2 Subscribe`,
`3 Menu`, `4 State`; formats `0 Protobuf`, `1 JSON` (`:33-34`).

What walker actually sends (type,format literals in `src/data.rs`):

| walker call site | bytes | meaning |
|---|---|---|
| `query()` `data.rs:589` | `vec![0,0]` + BE len + payload | Query, protobuf |
| `set_state()` `:668`, `activate()` `:785` | `vec![1,0]` | Activate |
| `subscribe_menu()` `:807`, `subscribe_bluetooth()` `:829` | `vec![2,0]` | Subscribe, `req.provider = "menus"` / `"bluetooth"` |
| `get_provider_state()` `:690` | `vec![4,0]` | State |

Note: in the read client paths walker never sends type `3` (Menu). Its menu feature is a
*subscription*: `subscribe_menu()` sets `req.provider = "menus"` (`data.rs:803-810`) and
sums the result in `listen_menus_loop()` as `SubscribeResponse` (`:319-345`). Consistent
with this, walker's `build.rs` compiles only `query`, `activate`, `subscribe`,
`providerstate`; there is no `menu.proto` in walker's `src/protos/` tree, while elephant
ships `pkg/pb/menu.proto` and a Menu handler at position 3.

Response frame (walker reads it at `sync` paths): `[status:u8][len:u32 BE][payload]`.
Walker `listen_loop()` `data.rs:368-440` dispatches on `header[0]`:
`255` QueryDone (no payload read), `254` no results (`clear_items`), `253` ignored,
`230` ignored, `3` ProviderState (payload → `ProviderStateResponse`), `2`
ActivationFinished (no payload read), default (`0` QueryItem / `1` QueryAsyncItem →
`QueryResponse`).
Elephant's status constants are `internal/comm/handlers/queryrequesthandler.go:25-31`:
`QueryDone=255`, `QueryNoResults=254`, `StatusDone=253`, `QueryItem=0`,
`QueryAsyncItem=1`, `ActivationFinished=2`, `ProviderState=3`.
`handlers/common.go:8-15` `writeStatus()` writes the status byte plus four zero length
bytes; item frames write status + big-endian length + protobuf payload
(`queryrequesthandler.go:66-74` for async items, `:230-237` for sync items).

Startup ordering: walker blocks until the socket file exists (`wait_for_file`,
`data.rs:847+`) and retries `connect`; the README's "make sure elephant is running"
(`walker README.md:59,163`) is therefore a hard prerequisite, not a style note.

Protocol version handshake: none observed in either README or the read code; the pair is
coupled by the fixed frame layout and protobuf schema copies. [INFERENCE, from absence
within the files read]

## 4. Defect: README's documented socket path contradicts the code at the same tag

- Documented: `README.md:211` — "Connect to the Unix socket (typically at
  `/tmp/elephant.sock`)".
- Actual: `comm.go:38-45` — `$XDG_RUNTIME_DIR/elephant/elephant.sock`; the `/tmp`
  fallback is `os.TempDir() + "/elephant/elephant.sock"` = `/tmp/elephant/elephant.sock`
  (a directory plus file name), never a flat `/tmp/elephant.sock`.
- Walker agrees with the code, not the README: `data.rs:156-161` uses `XDG_RUNTIME_DIR`
  or `temp_dir()`, then `elephant/elephant.sock`.

Consequence for a route note: the socket path must be cited to `comm.go` (and
`data.rs`), never to the elephant README; the README sentence is a documentation-only
claim that fails against its own tag. This is a clean example of docs-vs-code drift at a
pinned revision and can be stated without any host observation.

## 5. Provider inventory (three views; keep them distinct)

5a. Upstream code, tree at commit `8f1e21d6…` (GitHub trees API, 553 entries,
`truncated:false`): **25 provider directories**, each with a README:
`1password, aptpackages, archlinuxpkgs, bitwarden, bluetooth, bookmarks, calc,
clipboard, desktopapplications, dnfpackages, files, menus, niriactions, nirisessions,
playerctl, protonpass, providerlist, runner, snippets, symbols, todo, unicode,
websearch, windows, wireplumber`.

5b. Upstream README feature headings (`README.md` lines): Desktop Applications :15,
Files :20, Bluetooth :25, Clipboard :31, Runner :36, Symbols/Emojis :40,
Calculator/Unit Conversion :44, Custom Menus :48, Provider List :52, Websearch :55,
Archlinux Packages :58, Todo List :63, Bookmarks :68, Unicodes :72, Windows :75,
Snippets :78, Niri Sessions :81, 1Password :84 = **18 headings**. The README list is a
marketing subset and uses display names: `calc`→Calculator, `archlinuxpkgs`→Archlinux
Packages, `desktopapplications`→Desktop Applications, `menus`→Custom Menus,
`providerlist`→Provider List, `unicode`→Unicodes, `symbols`→Symbols/Emojis. It omits
`aptpackages, dnfpackages, niriactions, playerctl, protonpass, wireplumber` entirely.

5c. Host declaration (file read, no execution): `/usr/lib/elephant/` contains exactly 12
provider plugins — `bluetooth.so, calc.so, clipboard.so, desktopapplications.so,
files.so, menus.so, providerlist.so, runner.so, symbols.so, todo.so, unicode.so,
websearch.so` (sizes 24.4 MB–148.1 MB; `symbols.so` is 148,143,800 bytes).
`/usr/lib/elephant/providers`, `/usr/share/elephant`, `/usr/lib/walker` do not exist.
`/var/log/pacman.log` records 12 provider packages at `2.22.1-1` plus the core package
(upgrade block starting `:3095`), installed with `pacman -U` from `~/.cache/yay/...`
(`:3092`) → AUR/yay build, not an official-repo package.

Host-vs-upstream gap (documentary only): the host has no package or `.so` for the
README-documented `archlinuxpkgs, bookmarks, windows, snippets, nirisessions, 1password`,
nor for the code-only `aptpackages, bitwarden, dnfpackages, niriactions, playerctl,
protonpass, wireplumber` — 12 of 25 upstream providers are present. Why those 12: AUR
packaging/build selection; PKGBUILDs were not opened. [INFERENCE for the cause; the
absence itself is observed file state]

## 6. Config location (README claim, code behaviour, host state)

README `:183-190` documents:

```
~/.config/elephant/
├── elephant.toml        # Main configuration
├── .env                 # Environment variables
└── <provider>.toml      # Provider config
```

plus `:141` `elephant --config /path/to/config` (custom directory), `:192-194`
`elephant generatedoc [provider]` for Markdown docs (this is why no config docs exist in
the repo), and `:110-116` the source-build recipe that copies provider plugins into
`~/.config/elephant/providers/`.

Code (same commit) sharpens this:

- `pkg/common/files.go:28-55` `ConfigDirs()`: an explicit dir (`--config`) wins
  (`:31-33`); otherwise `os.UserConfigDir()/elephant` if it exists, then each
  `$XDG_CONFIG_DIRS/elephant` if it exists. So the effective set is entirely
  existence-gated.
- `pkg/common/files.go:65-77` `ProviderConfig(provider)`: first
  `<configdir>/<provider>.toml` that exists; no file → `ErrConfigNotExists`.
- `pkg/common/config.go:41-73` `LoadGlobalConfig()` → `LoadConfig("elephant", ...)` →
  `elephant.toml`; then for every config dir, `.env` is loaded with godotenv
  (`:50-67`), with `OverloadLocalEnv` selecting `Overload` vs `Load` (`:56-59`).
- `internal/providers/load.go:42-73`: provider plugin search list is
  `/usr/lib/elephant`, `/usr/lib64/elephant`, `/usr/local/lib/elephant`,
  `/usr/local/lib64/elephant`, `/lib/elephant`, `/lib64/elephant`; `ELEPHANT_PROVIDER_DIR`
  replaces the whole list (`:60-63`), otherwise the config dirs are appended (`:65`);
  `ELEPHANT_DEV=true` narrows the list to `/tmp/elephant/providers` (`:71-73`). Plugins
  are `.so` Go plugins (`:96-106`).

Host state (file read): `~/.config/elephant/` exists but holds only `calc.toml` (14 B,
sha256 `2c0ef81b8edc9edf…`), `desktopapplications.toml` (62 B, `999b191512b29b68…`),
`symbols.toml` (81 B, `9c0d5edf1fce95f3…`) and a `menus/` directory. There is **no**
`elephant.toml`, **no** `.env`, **no** `providers/` dir. `~/.config/walker/config.toml`
exists (49 lines, 1336 B, sha256 `fecf71fa4253803e…`; walker's own config per
`walker README.md:213`).

## 7. P5 bridge found while inventorying config (pointer, not a claim)

`~/.config/elephant/menus/` contains three symlinks into omarchy's checkout:

| link | target | target bytes | target sha256 |
|---|---|---|---|
| `omarchy_background_selector.lua` | `~/.local/share/omarchy/default/elephant/omarchy_background_selector.lua` | 2076 | `292c7deb0ddc0d00…` |
| `omarchy_themes.lua` | `.../omarchy_themes.lua` | 2922 | `d997d5a4c27ffc10…` |
| `omarchy_unlocks.lua` | `.../omarchy_unlocks.lua` | 2746 | `b577869246d8050f…` |

Upstream menus provider README (`internal/providers/menus/README.md`, sha256
`0cb9750e8630b741…`) says at `:14` — "Default location for menu definitions is
`~/.config/elephant/menus/`." — and documents TOML menus plus dynamic Lua menus
(`:10`, `:140-142`); its Lua example enumerates a `wallpaper_dir` (`:164-175`). Walker
renders such menus via the `menus` subscription (§3). This gives a documentary bridge
from P5 (theme/wallpaper selection menu) to walker without any host behaviour: omarchy
ships the menu Lua, elephant hosts it, walker displays it. The three Lua files' contents
and effects were NOT read by this seat (theme route owns them): treat as pointer only,
with menu semantics `[UNK]`.

## 8. Host version anchors (file reads only)

| fact | anchor |
|---|---|
| walker upgraded `2.17.0-1 -> 2.17.2-1` | `/var/log/pacman.log:2929`, `2026-10-20T09:16:46-0300` |
| elephant upgraded `2.21.0-1 -> 2.22.1-1` | `/var/log/pacman.log:3095`, `2026-10-20T09:31:03-0300` |
| elephant family installed as `pacman -U ~/.cache/yay/...` | `/var/log/pacman.log:3092` (AUR/yay build) |
| `/usr/bin/elephant` present | 23,460,760 B, mtime 2026-10-20 09:29 (package build time, not exec) |
| `/usr/bin/walker` present | 7,039,912 B, mtime 2026-10-08 11:14 |
| 12 provider `.so` under `/usr/lib/elephant` | directory listing, §5c |

Host binary ↔ upstream tag: version strings match (`2.17.2-1`, `2.22.1-1`) but provenance
is **[UNK]** — the pacman log records package versions only; no PKGBUILD, source commit,
or binary digest was opened, and no binary was executed. Do not state that `/usr/bin/elephant`
is built from `8f1e21d6…`.

## 9. Candidate SOURCES rows (for L1; ids `S0xx-pending` — L1 assigns S072-S099)

All are upstream HTTPS, tier A, `status: mined`, `opened 2026-10-20`, `recheck
on-change`, and each body is already committed-by-content under
`.ufo/waves/round-18/fetch/SrcElephantReadme/` with a receipt line. **They only count
for C2 after L1 commits that fetch directory and the rows** (this seat may not git-write
the lane).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx-pending | elephant README @ v2.22.1 — https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md | docs | A | elephant/walker-adjacent: what the elephant daemon is, its socket+protobuf contract, config dir shape, README provider list | `:3`, `:9`, `:183-190`, `:200-215`; sha256 `aa19a7e2d1c07bf1852b65fd38ca24a6b04bba0dacfd9f6cb02ada0ee0b61389` | the daemon aggregates providers for frontends over unix-socket protobuf; README socket sentence (`:211`) is stale against code at the same tag | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | elephant internal/comm/comm.go @ 8f1e21d6 — .../8f1e21d6efe40b8b3953f95b9574f99f717caf91/internal/comm/comm.go | code | A | elephant/walker wire: socket path derivation, listener, request frame and handler registry | `:27-35`, `:38-47`, `:59-63`, `:85-127`; sha256 `2b4a6f1493be9d4cc453adcc8f26f8488d360679ab8d4342ea6bf4c0edd16e54` | actual path `$XDG_RUNTIME_DIR/elephant/elephant.sock`; request header type+format+BE length; types 0..4 | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | elephant internal/comm/handlers/queryrequesthandler.go @ 8f1e21d6 — .../internal/comm/handlers/queryrequesthandler.go | code | A | elephant/walker wire: response frame, query status codes, item payloads | `:25-31`, `:66-74`, `:230-237`; sha256 `757270921de69d417eb87e03c1329538e9bbdf4d6e7728ab3874b3e6ae91cce0` | response header is status byte + BE length; statuses 0/1/2/3/253/254/255 | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | elephant internal/providers/load.go @ 8f1e21d6 — .../internal/providers/load.go | code | A | elephant provider plugin discovery for the walker surface | `:42-49`, `:60-73`, `:96-106`; sha256 `0b1da69e807b900aa73801d9cdb13578d207ecc26d96ac883ee14a789ebfe287` | .so search list incl. `/usr/lib/elephant`; `ELEPHANT_PROVIDER_DIR` override; dev dir | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | elephant pkg/common/files.go @ 8f1e21d6 — .../pkg/common/files.go | code | A | elephant config directory and per-provider toml lookup | `:28-55`, `:65-77`; sha256 `19492c244d1589df7c2cb208fd3393f9d49d8751773424a30f84db59d47a9bc5` | `--config` override; existence-gated XDG config dirs; `<dir>/<provider>.toml` resolution | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | walker README @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | docs | A | walker↔elephant: walker is an elephant frontend and requires the daemon running | `:13`, `:23`, `:59`, `:163`; sha256 `9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456` | features are elephant providers; start elephant first; menus are elephant-defined | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | walker src/data.rs @ a515085f — .../a515085f39fae80acc086c8fbfd9b7771a9a11d/src/data.rs | code | A | walker↔elephant client: socket path, per-concern connections, request framing, response status dispatch, menu subscription | `:148-169`, `:182-211`, `:319-345`, `:368-440`, `:589-592`, `:803-810`; sha256 `996db119ba61cb1505aa26782a19c7b8db49889874bd87ecbf277c9145cada09` | client computes the same socket path; sends 0/1/2/4 frames; menu data arrives on a `menus` subscription | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
| S0xx-pending | elephant menus provider README @ 8f1e21d6 — .../internal/providers/menus/README.md | docs | A | elephant menus: definition directory, TOML format, dynamic Lua menus incl. wallpaper listing | `:10`, `:14`, `:140-142`, `:164-175`; sha256 `0cb9750e8630b741eadf2c7a59b1128f26949692adac8f7dc256c3a321938bd2` | default menu dir `~/.config/elephant/menus/`; Lua menus run per empty query unless `Cache=true`; example lists a wallpaper dir | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md; corpus/knowledge/theme-route-r18.md (only if that note's scope names the menu bridge) |

If L1 wants the minimum set that still satisfies C2's "one upstream row naming
walker/elephant in source or scope", rows 1 and 6 already name both projects in the
source URL; rows 2/7 carry the wire facts a walker route note needs.

## 10. Confidence, inference, open unknowns

Observed (byte-cited above): tag→commit for both projects; README digests and quotes;
socket path derivation on both sides; request/response frame layouts; status constants;
provider dirs vs README headings vs host `.so` set; config directory resolution; host
package versions and install method; host config inventories and hashes.

[INFERENCE]: (a) walker's `wait_for_file` + retry loop means start order is a hard
contract (code shows the mechanism; no runtime test); (b) the absence of a compiled
`menu.proto` in walker plus the `menus` subscription accounts for walker's menu feature;
(c) the 12 host `.so` files are the providers actually loaded, since `load.go` scans that
directory — load order and arch filtering were not observed; (d) AUR packaging explains
the missing 13 upstream providers.

[UNK]: host binary provenance against the tags (no PKGBUILD read, no binary executed);
runtime presence/state of the socket; whether the AUR build patches upstream; the content
and effects of the three omarchy menu Lua files; compatibility policy between walker
2.17.2 and elephant 2.22.1 (no handshake or version field in either README or the read
code); why walker's reader treats status `230` as a no-payload no-op (constant not found
in elephant's query handler).

## 11. Handoff for L1

1. Commit `.ufo/waves/round-18/fetch/SrcElephantReadme/` (16 bodies + receipts.jsonl)
   before any C2 credit; R17-V3 requires the committed raw receipt.
2. Assign S ids and append the candidate rows in the exact 11-column ledger shape; keep
   `used-by` naming the route notes that actually cite them.
3. When the walker route note states the socket path, cite `comm.go:38-45` +
   `data.rs:156-161`, not `README.md:211`; the README is the drift exhibit, not the
   authority.
4. Do not claim host binaries were built from `8f1e21d6…`; only the version string match
   is documented.
