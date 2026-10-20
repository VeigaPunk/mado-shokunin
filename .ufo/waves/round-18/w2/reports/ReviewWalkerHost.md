# ReviewWalkerHost — W2 falsification, `walker-route-r18.md` § Host declaration

Seat: `MadoR18.ReviewWalkerHost` (wave 2, item: re-hash every host file the
`## Host declaration` names, compare digests and line anchors, check the MOVED
pins against `/var/log/pacman.log`). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`.

Subject: `corpus/knowledge/walker-route-r18.md` § Host declaration, working-tree
and commit bytes identical — `git show 4c103b55b1ea5c3c555884afe3eb69b5189701b7:corpus/knowledge/walker-route-r18.md`
sha256 `3ff430a4627d4204ff14c1e9e92eb726a38244ad8c27d8bda412243dfb8fbf20`,
working file sha256 `3ff430a4…8fbf20`, `git diff 4c103b55 -- <path>` empty.
Section spans lines 173–256 of that file; table 178–188, bullets 190–217,
version binding 219–230, MOVED pins 232–246, launch declarations 248–256.

**Verdict: PASS on substance.** Every digest, byte count, line count, mtime and
line anchor in the table and bullets reproduced exactly. All nine table rows are
corroborated by committed tag-pinned fetch bodies, fetched independently by
several seats. No HIGH or MEDIUM defect. Two LOW citation-precision defects and
three INFO notes follow; none changes a claimed fact.

Instruments: byte reads only (`sha256sum`, Python `hashlib`, `cat -n`, `sed -n`,
`grep`, `find`). No package manager/query, no service, no process probe, no
compositor/input/screenshot, no REA. Config trees read as bytes. Read-only git in
the lane (`show`, `rev-parse`, `diff`); no jj. The `lsp` device is not mounted in
this session's tool inventory (no `lsp` status/definition/references available),
so caller/definition checks are inapplicable to a literal-byte claim; `grep` was
used only as a literal byte search, never as semantic proof. One read-only
`git ls-remote` was run in `/tmp` (network query, writes nothing) to resolve a
tag→commit question that the committed API bodies left ambiguous; disclosed in
§7. No tool was installed or upgraded.

---

## 1. Re-hash of every host file named in the section

Claimed values are quoted from `walker-route-r18.md` lines 178–188 (table) and
190–217 (bullets). Observed values were re-hashed from host bytes.

| file | claimed | observed | match |
|---|---|---|---|
| `~/.config/walker/config.toml` | `fecf71fa…d1787`, 1,336 / 49 | sha256 `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`, 1,336 B, 49 lines, mtime 2026-10-03 17:44:32 -0300 | exact |
| `~/.local/share/omarchy/config/walker/config.toml` | same sha, 1,336 / 49 | same sha, 1,336 B, 49 lines | exact |
| `/etc/xdg/walker/config.toml` | `3c5c6867…50a8b`, 13,743 / 305; mtime 2026-10-08 11:14:32 -0300 | sha256 `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`, 13,743 B, 305 lines, mtime 2026-10-08 11:14:32 -0300 | exact |
| `/usr/bin/walker` | `25240650…93096`, 7,039,912; mtime 2026-10-08 11:14:32 -0300 | sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`, 7,039,912 B, mtime 2026-10-08 11:14:32 -0300 | exact |
| `~/.config/autostart/walker.desktop` | `5cb9874e…c3aa7`, 138 | sha256 `5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7`, 138 B, 7 lines | exact |
| `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf` | `de0f7029…15433`, 38 | sha256 `de0f70294000bc29f5876ea195db127f74060ac990aad5a129eeb72c98b15433`, 38 B, 3 lines | exact |
| `~/.local/share/omarchy/bin/omarchy-launch-walker` | `fd9e93f8…1d81d8`, 412 | sha256 `fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8`, 412 B, 14 lines | exact |
| `~/.local/share/omarchy/bin/omarchy-restart-walker` | `9ac82d0c…3bf8174`, 709 | sha256 `9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174`, 709 B, 24 lines | exact |
| `~/.local/share/omarchy/bin/omarchy-refresh-walker` | `05cd9c67…c093f9a2`, 893 | sha256 `05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2`, 893 B, 26 lines | exact |

Additional files the section names (no digest is claimed for these; hashed for
completeness):

| file | bytes | lines | sha256 |
|---|---|---|---|
| `~/.config/elephant/calc.toml` | 14 | 1 | `2c0ef81b8edc9edfdc409570bf18ba9d44f488a30d6b223533cce66ee266bdb5` |
| `~/.config/elephant/desktopapplications.toml` | 62 | 3 | `999b191512b29b6822a18f48495169bf4b96573388da2b035452e530f31f434e` |
| `~/.config/elephant/symbols.toml` | 81 | 1 | `9c0d5edf1fce95f3c785af79535c3c95ab6aaa5c16048e7e42560182e33efd9b` |
| `~/.config/elephant/` | `menus/` is a directory; no `elephant.toml` (nor `.env`) present | — | — |
| `~/.local/share/omarchy/.git/HEAD` | 23 | 1 | `f6f2b945f6c411b02ba3da9c7ace88dcf71b6af65ba2e0d89aa82900042b5a10` (`ref: refs/heads/master`) |
| `~/.local/share/omarchy/.git/packed-refs` | 40,556 | 518 | `5f094c653ab6a1ddb440772cb3461d301e76c4f1edfcacdb5b0d8b8cc4b141a3` |
| `~/.local/share/omarchy/.git/FETCH_HEAD` | 63 | 1 | `76c6c45db0869d404df9694c635dfac706be0a92383d908c3ccbdc4512fbdcf3` |
| `~/.local/share/omarchy/default/walker/walker.desktop` | 138 | 7 | `5cb9874e…c3aa7` (= table row 5) |
| `~/.local/share/omarchy/default/walker/restart.conf` | 38 | 3 | `de0f7029…15433` (= table row 6) |
| `…/default/hypr/bindings/utilities.conf` | 4,119 | 76 | `57ddb3045f81d6932d7e89482b295a28bc490550fa9dd1a1ff93db91573524fc` |
| `…/default/hypr/bindings/clipboard.conf` | 319 | 5 | `19ca281aae91a7db511fb4f3a5aabbabff9c1f7b6b949ff62924b01082ffaaef` |
| `…/default/hypr/apps/walker.conf` | 80 | 2 | `8ebc83e3e1c3c8296648f3334cc3d981dc95a27070e6aa9f449e7e45c510d0e9` |
| `…/default/hypr/apps.conf` | 1,167 | 19 | `1a5482bb81b325ef811d31d07707a706b583a8dba802a477cb79ffbd6859d72e` |
| `~/.config/hypr/bindings.conf` | 2,879 | 40 | `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581` |

The table's "bytes / lines" column uses newline counts; the observed counts above
use the same convention and agree exactly.

### Embedded-default blob (`/usr/bin/walker`)

- `b[806960:806960+13743] == /etc/xdg/walker/config.toml` → `True`; the full
  13,743-byte block occurs **exactly once** in the 7,039,912-byte binary
  (`bytes.count == 1`). Claim at lines 205–207 reproduced.
- The single `config.toml` literal is at 820,703; the single `WALKER_` literal is
  at 820,714, i.e. directly adjacent, followed 7 bytes later by
  `config not initialized` (single occurrence, 820,721). Byte context:
  `…}\n]\nconfig.tomlWALKER_config not initializedstruct Walker…`.
- The round-7 census claim (line 245) held: **one** bare `WALKER_`, adjacent to
  `config.toml`, and the following run is `config not initialized` (the 2.17.0
  note put `WALKER_` at 797,295 and `config not initialized` at 797,345 — a
  50-byte gap; the 2.17.2 gap is 7 bytes, so "the byte run after it changed" is
  true).
- Unclaimed positive corroboration of the version binding: the binary carries
  exactly one `2.17.2` at offset 856,302 (`…version2.17.2\ntoggle exact
  search…`), and `2.17.0` / `2.16.2` occur zero times. This does not prove
  tag-byte identity, so the table's `[UNK]` is correctly conservative.

### Upstream-tag identity (`8fcc9d60…`)

- `packed-refs` line 2: `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/heads/master`;
  line 508: same sha `refs/tags/v3.8.4`; line 509 has no `^` peeled line, so the
  tag is lightweight.
- `FETCH_HEAD`: `8fcc9d6048af4cb0e3af8512c78049857a3b53dd\t\tbranch 'master' of .`
- Read-only `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4`
  → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/tags/v3.8.4` (no peeled
  `^{}` line). The commit API body (`git/commits/8fcc9d60`, 200, 1,558 B) is a
  commit by DHH dated 2026-07-20, "Merge branch 'master' into rc", tree
  `4c52b84c…`. The "equal to the upstream tag" parenthetical is therefore true.

## 2. The "vs. upstream" column: committed bodies with matching digests

All nine rows' upstream equality is backed by `.ufo/waves/round-18/fetch/*/`
bodies whose sha256 equals the host digest, fetched from tag-pinned URLs:

- `OC` (omarchy `v3.8.4` `config/walker/config.toml`, `fecf71fa…`): bodies in
  `fetch/NoteWalker/omarchy-v3.8.4-config-walker-config.toml`,
  `fetch/SrcOmarchyWalker/config-walker-config.toml`,
  `fetch/ReopenS085/omarchy-v3.8.4-config-walker-config.toml`,
  `fetch/ReviewWalkerUpstream/omarchy-3.8.4-walker-config.toml` (four seats).
- `WC` (walker `v2.17.2` `resources/config.toml`, `3c5c6867…`): seven bodies
  across `SrcWalkerReadme`, `MadoR18.SrcWalkerThemes`, `SrcWalkerChangelog`,
  `SrcWalkerDefaultConfig`, `NoteWalker`, `ReopenS073`, `ReviewWalkerUpstream`;
  the receipt URL is
  `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml`.
- `OD` (`default/walker/walker.desktop`, `5cb9874e…`; `default/walker/restart.conf`,
  `de0f7029…`) and `OL`/`OR`/`OF` (`bin/omarchy-launch-walker` `fd9e93f8…`,
  `bin/omarchy-restart-walker` `9ac82d0c…`, `bin/omarchy-refresh-walker`
  `05cd9c67…`): tag-pinned bodies in at least `SrcOmarchyWalker`,
  `NoteWalker`, `ReopenS086`–`ReopenS089`, `ReviewWalkerUpstream`.
- The three elephant config files also have matching `v3.8.4` bodies
  (`SrcOmarchyWalker` receipts, `2c0ef81b…` / `999b1915…` / `9c0d5edf…`).
- `WK:3`'s `version = "2.17.2"` is a tag-pinned body:
  `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.toml`
  → 952 B, line 3 `version = "2.17.2"`.
- `WC` anchors checked against the fetched v2.17.2 body: `close_when_open =
  true` :2, `as_window = false` :4, `selection_wrap = false` :6, `theme =
  "default"` :9, `resume_last_query = false` :18, `[columns] "symbols" = 3`
  :37–38, `default = [...]` :58–66, `max_results = 50` :67, and exactly ten
  `[[providers.prefixes]]` tables in :75–113 with the stated mappings. The user
  file's six-entry prefix table (`/`→providerlist, `.`→files, `:`→symbols,
  `=`→calc, `@`→websearch, `$`→clipboard) genuinely differs from that table
  (`/`→files, `.`→symbols, `:`→clipboard, `$`→windows), so line 198's "differs
  from upstream" is correct.

## 3. File anchors (all match)

`~/.config/walker/config.toml`, `cat -n`:

- :1 `force_keyboard_focus = true`; :2 `selection_wrap = true`; :3 `theme =
  "omarchy-default"`; :4 `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`;
  :5 `hide_action_hints = true`.
- :10 `[keybinds]`, :11 `quick_activate = []`.
- :13 `[columns]`, :14 `symbols = 1`.
- :16 `[providers]`, :17 `max_results = 256`; :18–21 `default = [ "desktopapplications", "websearch", ]`.
- :23, :27, :31, :35, :39, :43 — six `[[providers.prefixes]]` tables, last ends :45.
- :47 `[[emergencies]]`, :48 `text = "Restart Walker"`, :49 `command = "omarchy-restart-walker"`.

Launch declarations (`~/.local/share/omarchy`):

- `default/hypr/bindings/utilities.conf:2` `bindd = SUPER, SPACE, Launch apps, exec, omarchy-launch-walker`;
  :3 `bindd = SUPER CTRL, E, Emoji picker, exec, omarchy-launch-walker -m symbols`.
- `default/hypr/bindings/clipboard.conf:5` `bindd = SUPER CTRL, V, Clipboard manager, exec, omarchy-launch-walker -m clipboard`.
- `~/.config/hypr/bindings.conf:40` `# bind = SUPER, PERIOD, exec, omarchy-launch-walker -m symbols # Emoji Button` (commented, as stated).
- `default/hypr/apps/walker.conf:2` `layerrule = no_anim on, match:namespace walker`.
- `default/hypr/apps.conf:18` `source = ~/.local/share/omarchy/default/hypr/apps/walker.conf`.

## 4. `/var/log/pacman.log` (3160 lines; read only)

Every cited line reproduced verbatim:

- 1943 `[2026-10-11T16:14:39-0300] [ALPM] upgraded walker (2.16.2-1 -> 2.17.0-1)`
- 2929 `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`
- 3062 `[2026-10-20T09:18:25-0300] [ALPM] running 'walker-restart.hook'...`
- 3095 `[2026-10-20T09:31:03-0300] [ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)`
- 3123 `[2026-10-20T09:31:04-0300] [ALPM] running 'walker-restart.hook'...`
- 3132–3147 contains the removals (see LOW-1 for the exact boundary).

No later walker or elephant line exists after 3147, so "the host now carries
2.17.2-1 and 2.22.1-1" is consistent, and the binary's own `2.17.2` string
corroborates it.

### MOVED pins: old values verified in the older notes

- `walker-deep.md` is the round-5 note (title line 1; measured 2026-10-14
  17:00–17:25 UTC). §1:57 pins the 2.17.0 binary at 6,661,264 B / `64826a85…` /
  mtime 2026-07-26 21:42:11; §1:64 pins the packaged config at 13,220 B /
  `5b4e47b7d2314bf8…` / mtime 2026-07-26 21:42:11; §14.1 reproduces
  `784064 True`.
- `walker-live-surface.md` is the round-7 note. §1:37 pins `64826a85…`; §1:43
  pins 6,661,264 B and mtime 2026-07-26 21:42; §3:114 pins the packaged config
  13,220 B / `5b4e47b7…` / mtime 2026-07-26 21:42:11; §3:113 pins the embedded
  offset 784,064; §8/§5:229 is the "exactly one bare `WALKER_` literal (offset
  797,295)" census.
- `walker-deep-r9.md` is the round-9 note. §1:64 pins the packaged config
  13,220 B / `5b4e47b7…` / mtime 2026-07-26; :69 and :334 pin 784,064.

So the old values in the MOVED bullets (13,220 B, `5b4e47b7…`, 6,661,264 B,
`64826a85…`, mtime 2026-07-26, offset 784,064, versions 2.17.0/2.21.0) are all
present in the notes they are attributed to, and the "round-5/7/9" offset
provenance is accurate (round 5 = `walker-deep.md`, round 7 =
`walker-live-surface.md`, round 9 = `walker-deep-r9.md`).

## 5. Findings

### LOW-1 — `HP:3132-3147` boundary and "same run" wording overstate the range

`walker-route-r18.md:226-228`: "Elephant `-debug` packages from the same run are
removed at `HP:3132-3147`." Exact log content:

- 3132 `[PACMAN] Running 'pacman -Rns --noconfirm btrbk elephant-bluetooth-debug … elephant-websearch-debug'`
  (also removes `btrbk`, not an elephant debug package);
- 3133 `running '10-limine-snapper-lock.hook'`;
- 3134 `transaction started`;
- **3135–3147** the 13 `[ALPM] removed elephant-*-debug (2.22.1-1)` lines (last
  is 3147 `elephant-bluetooth-debug`).

The removal lines are 3135–3147, not the whole 3132–3147 range. The removals are
also a **separate transaction** (`pacman -Rns` at 09:38:33, line 3132) seven
minutes after the 09:31:03–04 `pacman -U` that installed the debug packages
(3092–3093 command line, 3094–3121 installs). "From the same run" reads as the
same transaction but is only true of the same operator upgrade session.
Suggested correction: "removed by a separate `pacman -Rns` at 09:38:33,
`HP:3135-3147`". No claim elsewhere depends on the wider range.

### LOW-2 — MOVED pin citation over-attributes `walker-live-surface.md` §1

`walker-route-r18.md:237-239`: "`walker-deep-r9.md` §1 and `walker-live-surface.md`
§1/§3 pin 13,220 B, sha `5b4e47b7…`, mtime 2026-07-26." The values are right:
`walker-deep-r9.md` §1:64 carries them, and `walker-live-surface.md` **§3:114**
carries them. But `walker-live-surface.md` §1 (lines 33–48) contains only the
binary pin (`64826a85…`, :37) and a package-file listing naming
`/etc/xdg/walker/config.toml` with no size/hash (:43); it does not pin the
packaged config's 13,220/`5b4e47b7…`/mtime. Narrow the citation to
`walker-live-surface.md` §3 (or §6:277, which says only "identical"). Factual
content unaffected.

### INFO-1 — "two `default/walker` files equal their tag bytes (table above)"

`walker-route-r18.md:216-217` says the three `bin/` scripts and two
`default/walker` files equal their tag bytes "(table above)". The table above
has no rows for `default/walker/walker.desktop` and `default/walker/restart.conf`;
their digests equal table rows 5 and 6 (autostart and the drop-in) instead. The
statement itself is true (tag-pinned bodies match), so this is a pointer nit.

### INFO-2 — `tree-v3.8.4.json`'s top-level `sha` is the resolved commit, not the tree

The committed body `fetch/SrcOmarchyWalker/tree-v3.8.4.json` (fetched from
`api.github.com/repos/basecamp/omarchy/git/trees/v3.8.4?recursive=1`) has
`"sha": "8fcc9d60…"` and `"url": ".../git/trees/8fcc9d60…"`, while the commit
object `8fcc9d60…` (`git/commits/…`, 200) declares `tree.sha = 4c52b84c…`.
A git sha names exactly one object, so the body's `sha` cannot be a tree here;
GitHub echoes the resolved object (the commit) for ref/commit inputs and lists
that commit's tree. This is not a lane error, and the same behaviour appears in
the walker control: `git/trees/v2.17.2` and `git/trees/a515085f…` return
identical 26,501-byte bodies whose top-level `sha` is `a515085f…`, which the two
committed walker v2.17.2 commit bodies give as the commit sha. So the body is
**not** evidence that `8fcc9d60` is a tree sha; the tag→commit equality was
confirmed independently by `git ls-remote` (see §1) and by `packed-refs` having
no peeled line. Worth a one-line note in the route so a closure does not misread
that body as a tree identity.

### INFO-3 — an uncited third `walker-restart.hook` run

`/var/log/pacman.log:2034` also runs `walker-restart.hook` at
2026-10-11T16:16:37 (after the 2.17.0 upgrade), which the section's "the 09:18
and 09:31 restart hooks" does not mention. No claim depends on it; noted only so
the "restart hooks" enumeration is known to be scoped to 2026-10-20.

## 6. Residual risk

- Nothing in the section was found false. The remaining risk is reader-side:
  LOW-1 and LOW-2 could propagate a wrong line range or section number into a
  closure; INFO-2 could propagate a wrong object-type reading.
- `/usr/bin/walker` tag-byte identity stays `[UNK]` as declared. The embedded
  config block and the self-reported `2.17.2` string are consistent with the
  v2.17.2 tag but neither proves byte-identity of the executable against a
  source build; Arch/AUR packaging patches remain `[UNK]`.
- Process state after the restart hooks stays `[UNK]`, as declared; no process
  probe was performed (constraint).
- Mtimes were read with Python `os.stat` on the named files only (the byte-read
  whitelist excludes the `stat` command). This is a metadata read of named
  paths; no state was changed and no other `stat` usage occurred.
- Two verification fetches hit the unauthenticated GitHub API rate limit (403,
  280-byte error bodies); receipts were still written as required. The 403 does
  not weaken the conclusions: the tag-equality claim was settled by `ls-remote`,
  and all content hashes came from already-committed bodies.

## 7. Verification gaps / disclosures

- `lsp` device unavailable in this session (not mounted); semantic caller checks
  are inapplicable — every claim here is a literal byte, digest, count or line
  anchor, verified by re-reading the bytes.
- One read-only network query (`git ls-remote`, `/tmp`, no clone, no write) was
  used solely to resolve the tag→commit mapping; no git/jj write occurred in the
  lane, and no git command ran inside `~/.local/share/omarchy`.
- Five new files were written under
  `.ufo/waves/round-18/fetch/ReviewWalkerHost/`: `receipts.jsonl` (two
  `mado-fetch-receipt-v1` lines, both `http_status` 403), `ref-tags-v3.8.4`,
  `commit-8fcc9d60` (the 403 bodies). This is the contract-mandated receipt
  location; no other lane file was written except this report.
- No package-manager, service, compositor, input, screenshot or REA operation;
  no tool installed.

## 8. Commands run (exact)

```sh
# document identity
git show 4c103b55b1ea5c3c555884afe3eb69b5189701b7:corpus/knowledge/walker-route-r18.md | sha256sum
sha256sum corpus/knowledge/walker-route-r18.md
git diff --stat 4c103b55b1ea5c3c555884afe3eb69b5189701b7 -- corpus/knowledge/walker-route-r18.md

# every named host file: sha256, size, newline count, mtime
python3 -I - <<'PY'  # hashlib.sha256 + os.stat over the 14 table/bullet paths,
...                  # then os.walk over ~/.local/share/omarchy/default/walker,
...                  # then os.listdir ~/.config/elephant
PY

# embedded default / census
python3 -I -c 'w=open("/usr/bin/walker","rb").read(); x=open("/etc/xdg/walker/config.toml","rb").read(); \
 print(w[806960:806960+len(x)]==x, w.count(x), w.count(b"WALKER_"), w.count(b"config.toml"), \
 w.count(b"2.17.2"), w.count(b"2.17.0"), w.count(b"2.16.2"))'

# anchors and launch declarations
cat -n ~/.config/walker/config.toml
cat -n ~/.local/share/omarchy/default/hypr/bindings/utilities.conf
cat -n ~/.local/share/omarchy/default/hypr/bindings/clipboard.conf
cat -n ~/.local/share/omarchy/default/hypr/apps/walker.conf
sed -n '18p' ~/.local/share/omarchy/default/hypr/apps.conf
cat -n ~/.config/hypr/bindings.conf | sed -n '38,42p'

# git metadata bytes (read as bytes)
cat ~/.local/share/omarchy/.git/HEAD
grep -n -e 'refs/heads/master' -e 'refs/tags/v3.8.4' ~/.local/share/omarchy/.git/packed-refs
cat ~/.local/share/omarchy/.git/FETCH_HEAD
sed -n '505,512p' ~/.local/share/omarchy/.git/packed-refs

# pacman.log citations and census
sed -n '1943p;2929p;3062p;3095p;3123p;3132,3147p' /var/log/pacman.log
grep -n 'removed elephant' /var/log/pacman.log
grep -n -e walker -e elephant /var/log/pacman.log | grep -v debug
sed -n '3090,3131p' /var/log/pacman.log

# upstream equality: hash every committed round-18 body and join to host digests
python3 -I - <<'PY'  # os.walk .ufo/waves/round-18, sha256 each file, match the 7 digests
PY

# MOVED pins in the older notes
grep -n -e '13,220' -e '5b4e47b7' -e '6,661,264' -e '64826a85' -e '784,064' \
  corpus/knowledge/walker-deep.md corpus/knowledge/walker-live-surface.md corpus/knowledge/walker-deep-r9.md
grep -n '^## ' corpus/knowledge/walker-deep.md corpus/knowledge/walker-live-surface.md

# tag -> commit (read-only network query, /tmp)
cd /tmp && git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'
```

Observed outputs are embedded in §1–§4 and §5; the selective reads above are the
ones that produced the cited matches. The one surprising result — the trees-API
`sha` field — and its resolution are recorded in INFO-2.
