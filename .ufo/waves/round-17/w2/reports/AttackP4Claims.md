# AttackP4Claims — round 17 wave 2 (critic)

Target: `corpus/knowledge/terminal-route-r17.md` at lane HEAD `988b858` (working copy
byte-identical: sha256 `9877b537…4fb8` both). Attacked: Alacritty-only scope against a
four-tree surface, inferred selection vs observed launch, user-local desktop-entry facts,
pacman.log version binding, and the honesty of "surface: P4 covered".

Axes: coverage (does the label claim more than the note sources), calibration (do `[UNK]` and
evidence labels match the evidence available), depth (missing route hops).

## Verdict

The note's body is mostly honest: it says "it covers Alacritty only, not foot, kitty or ghostty"
(`:16`) and does not claim a launch. The attack still succeeds on four points:

1. The README Frontier wording overclaims beyond what the note says.
2. Two `[UNK]`s were reachable from durable host bytes that nobody read. One of these
   counterexamples is strong.
3. The note gives the wrong anchor for what the applicability check reads.
4. The version binding is incomplete in both directions.

Under the declared rubric V, `surface: P4` counts mechanically, and 4/6 holds as a rubric count.
It is not honest to describe it as "P4 terminal-emulator configs" covered. Wording must change in
README, the SCORECARD C2 result, and the note itself. No change to the count is required.

## Counterexample 1 (strong): the launch selection is recorded on disk, not `[UNK]`

xdg-terminal-exec v0.14.3 caches every fresh resolution. Upstream script lines (fetched with curl,
tag v0.14.3, sha256 `89f2be9a…27ac`):
- Cache is on by default: `:1172` `XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}`.
- The cache file is `${XDG_CACHE_HOME}/xdg-terminal-exec` (`:173`).
- `save_cache` is defined at `:300-332`. The line format is at `:221-235` (1 hash, 2 cmd, 3 entry
  path, 4 entry ID, 6 execarg, 7 appidarg, 8 titlearg, 9 dirarg).
- It is called at `:1455-1457` after resolution and before the test-mode or exec branch.

I read the host file as bytes only (`stat`, `cat -A`, `sha256sum`):
- `~/.cache/xdg-terminal-exec`: regular file, 190 B, mtime `2026-10-20 09:57:18.89 -0300`,
  sha256 `dd26ec4e224bf38fdbd4842850ec9d6215b4aed51b9c5014998e8b37cbb1868a`.
- Contents:

```
6def15f66da26fd1cc77db99e6db79b9
alacritty
/home/vgpnk/.local/share/applications/./Alacritty.desktop
Alacritty.desktop

-e
--class=
--title=
--working-directory=

alacritty^^END_OF_EXEC_USEP
```

The note's `[UNK]` at `:110-112` ("Which terminal actually launches") and at `:123-124` ("whether
the resolver actually picks that entry over the system one") were narrowable to an observed fact:
- At 09:57:18 the resolver selected the **user-local** `Alacritty.desktop` (not
  `/usr/share/applications/Alacritty.desktop`).
- The selected command was `alacritty`, with dirarg `--working-directory=`.

What the cache does NOT show:
- That the process started. Test mode and `--print-cmd` also reach `save_cache`, at `:1457`
  before `:1460`.
- Who invoked it. The mtime is 13 s before the round-17 session directory timestamp
  (`2026-10-20T12-57-31Z` = 09:57:31 -0300). It is consistent with an operator launch, not a lane
  command `[INFERENCE]`.
- Which selection was used on later cache hits (`:1179`).

Depth gap: the note's "Upstream contract" omits the cache layer entirely. Its causal sentence at
`:103-104` ("launch `Alacritty.desktop` if it passes the applicability check") is incomplete. On a
cache hit (`:1179`, md5 over `ls -LRl` of config and application dirs plus `XDG_CURRENT_DESKTOP`,
`:179-215`), entry resolution is skipped.

## Counterexample 2: "shadows" is asserted, then called `[UNK]`, and its source is not cited

Table row `:74` states as fact that the user-local entry "shadows `/usr/share/applications/Alacritty.desktop`".
Then `:123-124` says it is `[UNK]` whether the resolver picks it. Both cannot hold as labels.

The precedence is in fact documented upstream, in lines the note does not cite:
- `:165-168` builds the application-directory list "in ascending order of preference", with
  `XDG_DATA_HOME` prepended first, so it ends up last.
- `:779-781` says "Entries are checked in ascending order of preference, so use last found if
  duplicate".

The cache record (CE1) agrees.

Correction: cite `xdg-terminal-exec:165-168,779-781` for "shadows" as `[INF-docs]`. Replace the
`:123-124` `[UNK]` with the cache observation and its limits.

## Counterexample 3: wrong anchor for what the applicability check reads

`:119-123` says the user-local entry carries `TerminalEmulator`, `X-TerminalArgExec=-e` and
`X-TerminalArgDir`, "the keys the applicability check and `--dir=` mapping read
(xdg-terminal-exec:919, 402-413)". Against v0.14.3:

- Applicability per README `:166-171` is the `TerminalEmulator` category plus Desktop Entry
  Specification validation. In the script that means:
  - Categories → `XTE__IS_TERMINAL` at `:807-822`.
  - `TryExec` at `:933-937`.
  - `Hidden` at `:938-942`.
  - The check is enforced at `:1090`.
- `X-TerminalArgExec` is read at `:885`. It is not an applicability input, and the default
  execarg is `-e` anyway (`:746`).
- `:402-413` handles `/execarg_default:` directives in **list files**, not desktop-entry keys.

The note leaves out the key that actually gates applicability for this entry:
`TryExec=alacritty` (user entry `:3`). Its target exists: `/usr/bin/alacritty` is a regular file,
8630080 B (stat only). The note also ignores the two `Hidden=true` foot stubs in
`~/.local/share/applications/` (`footclient.desktop`, `foot-server.desktop`, 28 B each). These are
P4 entries the same resolver discards at `:938-942`.

## Counterexample 4: version binding is truncated and over-hedged

pacman.log lines (file read; `grep -n`):
- `:639` `installed alacritty (0.17.0-1)` 2026-10-03. There is no later alacritty line. ✓ matches
  the note.
- `:1214` `installed xdg-terminal-exec (0.14.0-1)` 2026-10-03. **Omitted.**
- `:1946` `upgraded xdg-terminal-exec (0.14.0-1 -> 0.14.3-1)` 2026-10-11. **Omitted.**
- `:2935` `upgraded xdg-terminal-exec (0.14.3-1 -> 0.14.3-2)` 2026-10-20 09:16. ✓ The command line
  at `:2462` is `pacman -Syu --needed --noconfirm nvme-cli …`. The "non-lane" attribution is not
  derivable from the log `[INFERENCE]`.

The omitted lines matter. The host ran 0.14.0 from 2026-10-03 to 10-11, so the companion inventory
`terminals-and-omarchy.md` (2026-10-14) sat in the 0.14.3-1 era. "Matches the last logged pkgver"
hides the era boundary.

Over-hedge: `sha256sum /usr/bin/xdg-terminal-exec` = `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`,
44020 B. This equals the upstream v0.14.3 tag script (S057). For xdg-terminal-exec, which is a
shell script, the installed executable file is byte-identical to the tag. Arch `-2` packaging did
not change it. Keeping "[UNK] … Arch packaging changes" for this file under-claims. The `[UNK]`
stays valid for the Alacritty ELF: a tag man page cannot be byte-joined to the binary.

## Counterexample 5: "P4 covered" is broader than the note — README overclaims

- SCORECARD `:844` defines P4 as "terminal-emulator configs". The companion inventory
  (`terminals-and-omarchy.md:10-19`) has four trees. All four still exist with the same sizes
  (foot.ini 516 B, kitty.conf 954 B, ghostty/config 1325 B; `ls -la`). By stat,
  `/usr/bin/foot`, `/usr/bin/kitty` and `/usr/bin/ghostty` are absent.
- Even the Alacritty tree is only partly sourced. S058 anchors only `general.import` and
  `live_config_reload`. The keys the file actually sets are not given an upstream meaning:
  `[env] TERM`, `[terminal] osc52`, font, `window.padding`/`decorations`, and keyboard bindings
  (`alacritty.toml:3-28`).
- README Frontier `:119-121` says "Round 17 moves … P4 terminal-emulator configs onto
  **documentary** sourced ground". That claims the surface, not one route, and contradicts note
  `:16`.
- The README index row `:43` and SCORECARD `:851` ("P4 terminal") do not say "Alacritty only".
  The disclosure exists only inside the note body.
- Rubric mechanics (`measure.py:182-188`): the surface line must be exactly `surface: P4`. A
  qualifier on that line would be `MALFORMED`, so the scope must be disclosed on another head line.
  Coverage is existential per surface: one route flips P4. This is a property of the declared
  rubric, not a defect in the note. The judge should treat C2's +2 as "two surfaces gained one
  sourced route each", not "two surfaces covered".

## Counterexample 6 (minor): unsourced hop and anchor slip

- The declared chain at `:91-94` drops `uwsm-app --` (`bindings.conf:2-3`). It is a real hop
  (uwsm upgraded 0.26.7-1 -> 0.27.1-1 at pacman.log `:2926`, same transaction). It has no source
  row and no `[UNK]`.
- Table `:72` and S059 say `alacritty.toml:1-27` / "lines 3-27". The file has 28 lines, and line
  28 `]` closes the `[keyboard]` bindings array. The correct anchor is `:1-28` / `3-28`.

## Smallest safe corrections (wording only; count unchanged)

1. **Note head** (any of lines 5-15; NOT the `surface:` line): add
   `scope: Alacritty launch route + general.import/live_config_reload only; foot, kitty, ghostty trees and other alacritty.toml keys unsourced`.
2. **Note `:110-112` and `:123-124`**: replace with an `[OBS]` cache bullet giving path, size,
   mtime, sha256 `dd26ec4e…868a`, and the selected entry path, cmd and dirarg, with anchors
   `xdg-terminal-exec:173,221-235,300-332,1455-1457`. Keep these as `[UNK]`: process start,
   invoker, later cache hits.
3. **Note `:74`**: cite `xdg-terminal-exec:165-168,779-781` for "shadows", labelled `[INF-docs]`.
4. **Note `:119-123`**: the applicability inputs are Categories (`:807-822`), `TryExec`
   (`:933-937`, target `/usr/bin/alacritty` present by stat) and `Hidden` (`:938-942`), checked at
   `:1090`. `X-TerminalArgExec` is at `:885`. Drop `402-413` from this sentence.
5. **Note upstream contract**: add the cache layer (`:1172`, `:1179`, `:179-215`) as a route
   element.
6. **Note version binding `:113-118`**: add pacman.log `:1214` and `:1946`. Add
   `/usr/bin/xdg-terminal-exec` sha256 = S057 tag digest, so the script file is bound to the tag.
   Keep `[UNK]` for the alacritty binary only.
7. **Note `:91`**: insert `uwsm-app --` into the chain and add `[UNK] uwsm-app launch semantics
   (unsourced)`.
8. **README `:119-121`**: change to "Round 17 puts one P4 route — Alacritty's launch route and
   config-import contract — on documentary sourced ground; foot, kitty and ghostty trees and
   Alacritty's other keys remain unsourced". Add "(Alacritty only)" to index row `:43`.
9. **SCORECARD C2 result**: state that rubric V counts P4 on one Alacritty-only route
   (existential per surface), not P4 coverage.
10. **Note `:72` and S059**: change the anchor to `alacritty.toml:1-28`.

Judge note (tradeoff, not fixable by wording): rubric V lets one route stand for a surface with
four config trees. Any C2 sentence claiming P4 "covered" without the Alacritty-only qualifier
should be rejected.

## Operation record

- Host reads as file bytes or stat only:
  - `sha256sum`/`cat -n` of `bindings.conf`, `xdg-terminals.list`, both `Alacritty.desktop`
    entries, and `alacritty.toml`.
  - `sha256sum` of the theme import, the `.bak` file, `/usr/share/xdg-terminal-exec/xdg-terminals.list`
    and `/usr/bin/xdg-terminal-exec`.
  - `ls -la` / `stat` of `/usr/bin/{alacritty,foot,kitty,ghostty,xdg-terminal-exec}`,
    `~/.config/{foot,kitty,ghostty}` and `~/.local/share/applications`.
  - `stat` / `cat -A` / `sha256sum` of `~/.cache/xdg-terminal-exec`.
  - `grep`/`sed` of `/var/log/pacman.log`.
- All eight hashes in the note's table re-match. The system entry hashes to `d420b0f4…43d8` and
  has 0 `X-Terminal` keys ✓.
- Upstream: curl of the v0.14.3 `README.md` (`c7a1a8bb…9d40` ✓) and script (`89f2be9a…27ac` ✓)
  into `/tmp/ap4`.
- Nothing was executed from the route: no xdg-terminal-exec, alacritty, uwsm, omarchy, pacman,
  sudo, systemctl, hyprctl or probe. No lane file other than this report was written. No git
  mutation, no jj.
- Installs: none.
