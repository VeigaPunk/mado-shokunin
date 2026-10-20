# Existing theme notes — claims the P5 note must not contradict, stale lines, documentary openings

Round 18, wave 1, seat `MadoR18.ExistingThemeNotes` (leaf; no dispatch). Scope:
read `corpus/knowledge/theme-wallpaper-plane.md` (M7-2, 394 L), `gate-standing-use.md`
§6, and the `theme` rows in `tools/mado-verify.sh`; list (a) claims a new
`corpus/knowledge/theme-route-r18.md` (`surface: P5`) must not contradict, (b) stale
claims, (c) unknowns a documentary route can narrow. No file outside this report was
written. No web source was opened (zero fetch receipts). No tool installed.

Method: file bytes only (`cat/sed/stat/readlink/sha256sum/find/ls/wc/grep/od` reads of
`~/.config/**`, `~/.local/share/omarchy/**`, `/etc/chromium/policies/managed/`,
`/var/log/pacman.log`, lane sources), plus read-only git (`show`, `status`,
`diff --stat`, `diff -U0`). No language server is mounted in this seat's toolset,
so symbol tracing is literal (grep + exact-line reads of the definition), never
presented as semantic resolution; every code claim below names the line whose bytes
were read.
No pacman/yay/expac, no sudo/systemctl/journalctl/loginctl, no hyprctl/walker/elephant/
swaybg/waybar/alacritty/hypridle/hyprlock/omarchy-* invocation, no notify-send,
no screenshots, no `~/.omp/agent/agent.db*`, no lane git/jj write.

**Probe caveat, load-bearing for re-derivation:** this harness's shell shadows
`sed` with a builtin reporting `sed 0.1.1` that does **not** implement GNU `\u`;
`printf 'matte-black' | sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g'` there yields
`umatte ublack`. `/usr/bin/sed` is **GNU sed 4.10** and yields `Matte Black`
(`stat`/`--version` read). Every evidence script that reproduces the reader rule
must call `/usr/bin/sed`, never bare `sed` [OBS].

Tags below: `[OBS]` re-measured 2026-10-20 this seat · `[O-hist]` earlier lane
measurement, not re-runnable under the host pause · `[INF]` inference from measured
bytes · `[UNK]` unresolved · confidence in braces.

---

## 1. Host claims re-validated today — the new note may reuse these verbatim

All paths under `$HOME`; `C=~/.config`, `O=~/.local/share/omarchy`,
`th=$C/omarchy/current/theme`.

| # | Claim (as in `theme-wallpaper-plane.md`) | Re-measurement 2026-10-20 | Status |
|---|---|---|---|
| 1 | §1 `current/theme.name` = `matte-black`, 12 B, mode 644 | `cat` → `matte-black`; `stat` 12 B / 644; sha256 `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b` | [OBS] unchanged |
| 2 | §1 `current/background` symlink, 71 B link, absolute target `…/theme/backgrounds/0-ship-at-sea.jpg` | `readlink` exactly that; `stat -c %s` 71 | [OBS] unchanged |
| 3 | §1/§2 `current/theme/` = 24 regular files + `backgrounds/` (4 files), `du -sb` 3,718,129 | `find -maxdepth 1 -type f` 24; `backgrounds` 4; `du -sb` 3,718,129; modes all 644; mtimes 2026-10-03 17:49:02.54–.60 −03 | [OBS] unchanged |
| 4 | §2.1 eight ★ pins (alacritty, colors, hyprland, hyprlock, mako, swayosd, walker, waybar) | all eight sha256 values equal §2.1 exactly | [OBS] unchanged |
| 5 | §2 `backgrounds/0-ship-at-sea.jpg` sha `55fa691a…`, 1,681,677 B; `omarchy.png` sha `63d002b2…`, 4,491 B | both equal; sizes equal; the other two 1,033,920 / 482,067 B equal | [OBS] unchanged |
| 6 | §3 wallpaper declaration `default/hypr/autostart.conf:5` = `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill` | line 5 identical | [OBS] unchanged |
| 7 | §4 chain anchors `hypr/hyprland.conf:13`, `hypr/hyprlock.conf:1`, `waybar/style.css:1`, `alacritty/alacritty.toml:1` | all four lines identical (`source = ~/.config/omarchy/current/theme/…`; `@import "../omarchy/current/theme/waybar.css";`; `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]`) | [OBS] unchanged |
| 8 | §4 walker `config.toml:3-4` `theme = "omarchy-default"` + `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`; package `style.css:1` imports `…/current/theme/walker.css` | lines 3-4 identical; package line 1 identical | [OBS] unchanged |
| 9 | §4 `swayosd/style.css:1` imports the theme css; `mako/config` symlink (50 B) → `…/theme/mako.ini` | identical | [OBS] unchanged |
| 10 | §4 `btop/themes/current.theme` symlink (52 B) → `…/theme/btop.theme`; `btop.conf:5` `color_theme = "current"` | identical | [OBS] unchanged |
| 11 | §4 `envs.conf:3` sources `gum.env.conf`; file declares `env = FOREGROUND,##bebebe` and `env = GUM_CONFIRM_PROMPT_FOREGROUND,##e68e0d` | both lines present (`gum.env.conf:2`, `:8`); the *live* `printenv` leg is [O-hist] | [OBS] file leg only |
| 12 | §4 `nvim/lua/plugins/theme.lua` symlink (52 B) → `…/theme/neovim.lua` | identical | [OBS] unchanged |
| 13 | §4 share-picker `config.yaml:4` lists the theme stylesheet | line 4 identical | [OBS] unchanged |
| 14 | §4 `chromium.theme` `18,18,18` and policy `/etc/chromium/policies/managed/color.json` 65 B, `{"BrowserThemeColor": "#121212", "BrowserColorScheme": "device"}` | file content `18,18,18`; policy 65 B, mtime 2026-10-03 17:49, bytes identical | [OBS] unchanged |
| 15 | §4 `icons.theme` `Yaru-red`; `vscode.json` 65 B carrying `"name": "Matte Black"`; `keyboard.rgb` `#e68e0d` | all identical | [OBS] unchanged |
| 16 | §4 elephant provider anchors `omarchy_themes.lua:31-33`, `omarchy_unlocks.lua:49` | `find_preview_path` at :31-33 reads `preview.png`; unlocks reads `preview-unlock.png` near :49 | [OBS] unchanged |
| 17 | §5 writer `omarchy-theme-set:17` = strip tags, lowercase, spaces→hyphens; reader `omarchy-theme-current:9` = the `sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g'` rule | both lines byte-equal; reader reproduced with `/usr/bin/sed` (`matte-black`→`Matte Black`) | [OBS] unchanged |
| 18 | §3 writer semantics from `omarchy-theme-bg-next`: user+theme dirs (`:7-10`), `find -L … -type f` + `sort -z`, wrap-around index (`:20-36`), `ln -nsf` + `pkill -x swaybg` + `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill` (`:44-50`), zero-background branch `--color '#000000'` (`:16-17`) | all lines as stated; `CURRENT_BACKGROUND_LINK` = `$HOME/.config/omarchy/current/background` (`:9`) | [OBS] unchanged |
| 19 | §4.2 template renderer: `omarchy-theme-set-templates` globs `*.tpl` (`:37`), skips existing outputs (comment `:42`, guard `:43`), `COLORS_FILE=next-theme/colors.toml` (`:9`); 17 `*.tpl` under `default/themed/` | 17 count; all anchors as stated | [OBS] unchanged |
| 20 | §4.2 `omarchy-hook:25` skips `*.sample`; `~/.config/omarchy/themes/` has 0 entries; `~/.config/omarchy/backgrounds/` absent | hook line identical; 0 user themes; dir absent (`ls` error) | [OBS] unchanged |
| 21 | §3 `theme-set` always runs bg-next unless `OMARCHY_THEME_SKIP_BACKGROUND=1` (`:48-50`) | lines 48-50 identical | [OBS] unchanged |
| 22 | Host versions (a *log-line* fact, never a binary fact) | `/var/log/pacman.log`: swaybg `1.2.2-1` installed `:1158` (2026-10-03T17:44:27−0300); mako `1.11.0-1` `:1024`; waybar `0.15.0-3` `:1944`; walker `2.17.2-1` `:2929`; elephant `2.22.1-1` `:3095`; `grep -c hyprpaper` = **0** | [OBS] log bytes |
| 23 | omarchy checkout identity | `.git/packed-refs` carries `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` for **both** `refs/heads/master` and `refs/tags/v3.8.4`; `.git/config:7` remote `https://github.com/basecamp/omarchy.git`; `.git/HEAD` = `ref: refs/heads/master` | [OBS] tag == master commit |

The new P5 note may cite any row above as `[O]` with the same anchor. It must **not**
upgrade them to "live" (row 11's `printenv` leg, §3's running swaybg argv, §4's PIDs
are all `[O-hist]` 2026-10-14, see §3 below).

---

## 2. Gate claims the P5 note must not contradict

Two revisions are named here because the gate is under concurrent edit in this
worktree [OBS]: **baseline HEAD** `tools/mado-verify.sh` sha256
`fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` (3,711 L), and
the **in-flight worktree** sha256
`2bdf5e8afbb617142e4a881943084f94c9513327b1de25170ad71db113983925` (3,768 L,
`git status` = ` M`, `git diff --stat` +63/−6). `git diff -U0 -- tools/mado-verify.sh
| grep '^[-+].*theme'` returns **no line**: theme semantics are untouched; only
line numbers shift (cumulative +48 by the `live.theme.current` rows — hunks at
`:665`, `:668`, `:800` — and +57 below the `:3405` hunk). Anchors below are
baseline; worktree equivalents are given where they move.

1. **The theme plane is landed, file-plane only.** `theme_plane()` at `:3593`,
   called from `verify()` at `:2947`. It emits exactly **10 row ids**:
   `theme.name.read`, `theme.chain.hypr_include`, `theme.chain.hyprlock`,
   `theme.chain.waybar_css`, `theme.chain.alacritty`, `theme.chain.mako_link`,
   `theme.chain.walker_css`, `theme.chain.swayosd_css`, `theme.wallpaper.link`,
   `theme.parts.declared_only` (`:3593-3635`; helpers `:3493-3591` at baseline;
   worktree +57: `theme_plane()` `:3650`, helpers `:3550-3648`, plane call `:2995`).
2. **The two live rows did not land.** `grep -c 'wallpaper.live\|display_agree'
   tools/mado-verify.sh` → **0**; `theme.choice` → 0. `live.theme.current` still
   exists but under plane **`hypr-live`**, `:3233`/`:3237` (worktree `:3281`/`:3285`),
   always NOTE
   ("operator-owned; not a verdict input"). `gate-standing-use.md:257` calls the two
   absent rows "exempted by name (round 9)" — still true today. The new note must not
   describe either as a gate row or a verdict input.
3. **`theme.parts.declared_only` is narrower than note §4.1.** The loop
   (`:3629-3635` baseline) tests only `foot:foot.ini kitty:kitty.conf ghostty:ghostty.conf
   helix:helix.toml code:vscode.json asusctl:keyboard.rgb` via `have`; it does **not**
   cover `obsidian.css` — the seventh §4.1 row, whose absence has a different cause
   (see S7). Note §6's spec says "NOTE listing the
   §4.1 parts"; the landed row lists six of the seven, only the binary-gated ones.
   Do not repeat "the row lists every declared-only part".
4. **Theme clauses still have no covering mutant.** Gate comment `:1593-1596` baseline (`:1641-1644` worktree):
   "The newly landed theme rows carry no defect of their own yet: a covering mutant
   for the theme clauses is owed by the sweep lane (round-6 reading rule 2)" [OBS].
   `gate-standing-use.md` §6 carries the same debt. The P5 note must not claim mutant
   coverage for theme rows.
5. **Plane-id registry has 8 ids** at `:407`, `:411`, `:432-436`:
   `hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate`. The note's §6 prediction
   "plane ids 6 → 7" is stale on both sides (an `omarchy` id exists too).
6. **Chain-row semantics the note must match.** `theme_chain_row` requires the
   *first* grep match to sit on the declared line and the target to exist
   (`:3493-3514`); `theme_symlink_row` requires `readlink -f` inside the named
   directory and non-empty when asked (`:3516-3544`); walker/swayosd helpers degrade
   to NOTE when the consumer config is absent (`:3546-3591`). Any P5 note sentence
   that paraphrases the check (e.g. "imports anywhere in the file") would contradict
   the code.

---

## 3. Stale claims (do not copy; if needed, add errata rather than restating)

The note is append-only (§10 has only E1), so several standing lines are now false.
Each item is a hazard for a P5 note that quotes the note as current.

**S1 — note §0 gate pin, high.** "gate v1 (`tools/mado-verify.sh`, 1,186 L, sha256
`c4c1afb75dd1c8aa…` — round-6 landed revision, unchanged this pass)". Baseline-HEAD gate is
`fba82a66…` (3,711 L); the worktree copy is mid-edit at `2bdf5e8a…` (3,768 L).
Either way §0's pin is stale.

**S2 — note §6 "`theme` prefix: 0 row sites", high.** Opened with "The theme appears
only as one record-level NOTE: `live.theme.current` (`:1102-1108` …)". False since
round 9: 10 `theme.*` rows exist (§2 item 1 above). The `:1102-1108` anchor is also stale
(current `live.theme.current` at `:3233`/`:3237` baseline, `:3281`/`:3285`
worktree).

**S3 — note §6 row spec for `theme.wallpaper.live` and `theme.name.display_agree`,
high.** Both are tabulated as if landable; round 9 exempted them by name and they
never landed. A P5 note must not assume a live wallpaper/name row exists.

**S4 — note §6 "Census impact when landed: plane ids 6 → 7", medium.** Current registry
is 8 ids (S2.5). The four selftest regex sites moved again (`:407/:411/:432-436`).

**S5 — note §1 "theme.name … is the *only* file the theme-set ritual writes at the
root", medium.** `bin/omarchy-theme-set:45` writes `theme.name`, but the ritual then
runs `omarchy-theme-bg-next` (`:48-50`), which retargets `current/background`
(`bg-next:46`), and `:41-42` replaces `current/theme` (`rm -rf` + `mv`). Correct
form: "the only *regular file* the ritual writes into `current/`; the sibling
`background` symlink and the `theme/` directory are the other root entries it
changes".

**S6 — note §5 digit caution, high (false example).** Text: "the reader rule
uppercases **letters only**, so a name containing digits does not naively round-trip
through a lower/space-swap — `[INF]` example from the payload's own names:
`retro-82` displays `Retro 82`." Measured today: `retro-82` → `Retro 82` →
(writer) `retro-82`, i.e. it **does** round-trip; all 19 shipped names round-trip
under `/usr/bin/sed` (table in §4.3). The genuine non-round-trip class is a name
containing uppercase (writer lowercases, unrecoverable), e.g. a user theme dir
`myTheme-x`: reader `MyTheme X`, writer `mytheme-x` ≠ input. Do not repeat the digit
example as a boundary.

**S7 — note §4.1 obsidian row, high.** "1 vault, `.obsidian/` present, `themes/Omarchy`
absent — the sync never landed in this vault". The setter (`bin/omarchy-theme-set-obsidian`)
only syncs vaults listed in `~/.config/obsidian/obsidian.json` (`:9`, `jq -r
'.vaults | values[].path'`), skips paths without `.obsidian` (`:10`), and exits early
if `obsidian.css` is absent (`:7`). That registry is 121 B, mtime **2026-10-19
00:50:13 −03**, i.e. **after** the last theme-set artifacts (all 2026-10-03 17:49);
`theme.name` mtime is still 2026-10-03, so no theme set ran after registration
[OBS; INF that a set-on-Oct-3 skipped the then-unregistered vault]. The absence is
consistent with timing, not a failed sync. The note's wording implies a failure; the
new note must state the precondition chain instead (see §4.2).

**S8 — note §11.4 restart guards, medium.** "…which of the restarts actually respawned
a process (vs `pgrep` guard skips, e.g. btop absent) is `[UNK]`". Documentarily, the
guards are knowable: `theme-set:53-55` guards only **waybar**; `omarchy-restart-waybar`
is `pkill -9 -x waybar` + `setsid` (respawn); `omarchy-restart-btop` is
`pkill -SIGUSR2 btop` (signal, no respawn); `omarchy-restart-swayosd` is a
`systemctl --user` stop/enable sequence plus `pkill`; `omarchy-restart-terminal`
`touch`es `alacritty.toml` and signals only kitty/ghostty under `pgrep` guards;
`omarchy-restart-hyprctl` is `hyprctl reload`; helix/opencode are `pgrep`-guarded
signalers. So "which *actions are conditional*" is documented; "which actually
executed" stays `[UNK]`.

**S9 — SKILL.md round-9 anchors, high for citation work.** SKILL says `theme_plane()`
at `:3113` (called `:2465`) and live NOTE `:2753`/`:2757`; current values are `:3593`,
`:2947`, `:3233`, `:3237` (baseline) and `:3650`, `:2995`, `:3281`, `:3285`
(worktree). SKILL:1083 ("theme = 1 NOTE … no `theme.*` rows") is
scoped to the round-8 census table and is no longer a current statement.

**S10 — "P5" token collision, medium.** `SKILL.md:845` uses "P5" for the *symlink
probe* in the pin table (`P5 link topology`); `SCORECARD.md:844/926/944/962` uses
P1–P6 for the rubric-V surfaces; `corpus/README.md:42-43` uses `surface: P4/P6`.
`PROVINCE.md` itself contains **no** `P1`–`P6` token (grep 0). The map is rubric V in
`SCORECARD.md` plus the README rows, not PROVINCE.md. A note writing `surface: P5`
is correct for themes/wallpapers; a reader grepping "P5" in SKILL gets the pin.

**S11 — "P5 open" statements are baseline-true, not note-contradicting.** `README.md:124`
and `corpus/lessons/round-17.md:74` say P5 has no sourced route; true at baseline
`d9a5a18` and only superseded when the new note is integrated (L1 owns README/lessons).
The note must not claim P5 was covered earlier.

**S12 — `gate-standing-use.md` §6 pin, low.** The ledger is pinned at
`93e43f8f…` (round 9). Its theme-live-rows row still measures true today (grep 0),
but the pin line is historical; the P5 note should cite the current gate sha, not
that table's.

**S13 — note §2 "`vscode.json` 65 B" with `"name": "Matte Black"`, re-checked, still
true** (65 B, pretty-printed). Listed only so the P5 note does not "correct" it.

---

## 4. Unknowns a documentary route can narrow

`theme-wallpaper-plane.md` §11 numbered the open list. Mapping below states what a
docs/code-only route can honestly narrow and what remains `[UNK]` no matter how much
documentation is read.

### 4.1 U1 (live render of running consumers) — **partially** doc-narrowable
- Not narrowable: whether today's bytes are rendered by the running walker, swayosd,
  waybar, alacritty, btop. That needs an open/inspect/restart (fenced).
- Narrowable to a *contract*: each consumer's documented reload trigger. Alacritty's
  `live_config_reload` is already sourced (S058); a P5 note can cite the swaybg
  invocation semantics (`-i/--image`, `-m/--mode fill`, `--color`) from a tag-pinned
  swaybg source to say what the declaration *asks for* (fill+scale, not stretch) and
  that a missing image is an error path — still not a host render claim.
- Result vocabulary: `[INF-docs] what the consumer is asked to do`; `[UNK] what it
  renders`.

### 4.2 U3 (obsidian chain) — **strongly doc-narrowable, and half-answered already**
Mechanism, all file bytes [OBS]: `omarchy-theme-set:69` calls
`omarchy-theme-set-obsidian` unconditionally at every theme set; the setter exits 0
if `current/theme/obsidian.css` is missing (`:7`), enumerates **only** vaults in
`~/.config/obsidian/obsidian.json` (`:9`; `jq` is present on PATH at probe), skips
entries without `<vault>/.obsidian` (`:10`), then `mkdir -p <vault>/.obsidian/themes/Omarchy`,
writes `manifest.json` once, and copies `obsidian.css` → `theme.css` (`:13-27`).
Host facts: one vault (`~/Documents/shokoknowledge/.obsidian`) and registry mtime
2026-10-19 00:50 **later** than the last set (2026-10-03 17:49). Signature:
"not run since registration", not "sync failed". The residual `[UNK]` is only *why*
the vault was registered on 10-19 (operator action; out of lane) and whether a future
set would materialize it (would, per code) — no execution allowed.

### 4.3 U5 (generality of the display-name rule) — **strongly doc-narrowable**
Measured over all **19** shipped theme directory names (`$O/themes`), each transformed
with `/usr/bin/sed` and the writer's `tr '[:upper:] ' '[:lower:]-'`:

| input | reader (theme-current) | writer round-trip |
|---|---|---|
| catppuccin | Catppuccin | YES |
| catppuccin-latte | Catppuccin Latte | YES |
| ethereal / everforest / gruvbox / hackerman / kanagawa / lumon / miasma / nord / ristretto / vantablack / white | single capitalized word | YES |
| flexoki-light | Flexoki Light | YES |
| matte-black | Matte Black | YES |
| osaka-jade | Osaka Jade | YES |
| **retro-82** | **Retro 82** | **YES** (contradicts note §5's caution) |
| rose-pine | Rose Pine | YES |
| tokyo-night | Tokyo Night | YES |

- All 19 match the gate's `^[a-z0-9-]+$` (0 failures); no display-name collisions.
- **Second derivation exists.** The elephant providers (`default/elephant/omarchy_themes.lua:69-71`,
  `omarchy_unlocks.lua:52-54`) derive their own label from the *directory* name:
  `gsub("_"," "):gsub("%-"," ")` then word-wise `(%a)([%w_']*)` → first upper, rest
  **lower**. Over the 19 shipped names it agrees with the sed rule (0 disagreements,
  measured); in general it diverges: `2x-theme` → sed `2x Theme` vs elephant
  `2X Theme`; `myTheme-x` → sed `MyTheme X` vs elephant `Mytheme X`. So "the display
  name" is per-consumer, not one global rule — the note should name the consumer.
- Residual `[UNK]`: user theme directories not shipped (none exist today), and
  non-`[a-z0-9-]` names (gate would FAIL `theme.name.read` regardless).

### 4.4 U4 (which restarts fired) — **doc-narrowable to action/guard inventory**
See S8. The P5 note can state the inventory with line anchors and leave "which
executed on 2026-10-03" `[UNK]`; the declarative side is fully readable.

### 4.5 U2 (chromium policy adoption) — **weakly doc-narrowable**
The policy file ↔ `chromium.theme` mapping is file-level solid (65 B, mtime 17:49,
`18,18,18`→`#121212`). Whether a running Chromium adopts it in-session is not
documentary; at best a Chromium policy doc can say *when policies are read*
(startup/refresh), converting "unknown adoption" into "documented read timing +
unverified application". Keep `[UNK]` on adoption.

### 4.6 U6 (landing of the theme rows) — **closed, not an unknown**
Ten file rows landed round 9 (§2 item 1); live rows exempted by name; mutant owed. The P5
note should state this as fact and must not present the §6 spec as pending work.

### 4.7 Newly visible unknowns a P5 route should carry explicitly
- **N1 swaybg semantics source.** No SOURCES row is tag-pinned to swaybg; the
  declared invocation's documented meaning (`-m fill`, `--color`, image error path)
  is unopened. Candidate upstream anchor to assign (unopened here, must be fetched
  with a receipt before citing): tag-pinned raw docs at `swaywm/swaybg` v1.2.2 — the
  version in `pacman.log:1158` is a log line, not proof the running binary is that
  build.
- **N2 upstream omarchy identity.** Local `packed-refs` says tag `v3.8.4` ==
  `master` == `8fcc9d60…` and remote `basecamp/omarchy`; whether that tag exists
  upstream and whether the worktree equals the commit is `[UNK]` (no git command in
  that checkout, per contract). A fetch of a tag-pinned raw omarchy path would pin
  the upstream side; treat the checkout bytes as host, not upstream, until then.
- **N3 wallpaper-link absoluteness.** `bg-next` builds `NEW_BACKGROUND` from
  absolute `find` roots and `ln -nsf`; the link text is therefore an absolute path
  `[INF]`. The gate only requires resolution *inside* `backgrounds/`, not
  absoluteness; a documentary note may state the writer's form, not a gate guarantee.
- **N4 gate regex ↔ round-trip.** `^[a-z0-9-]+$` is exactly a round-trip-safe
  class: every string matching it survives reader→writer unchanged (checked on
  `retro-82`, `foo--bar`, leading/trailing hyphens and all-digit names; double
  hyphens stay two spaces and `tr` maps each back). Non-round-trip input is
  uppercase or a non-`[a-z0-9-]` character — and the gate rejects those before the
  display rule is reached. So the gate's shape rule and the display round-trip agree
  by construction on this host; no `[UNK]` remains here beyond unobserved user names
  that the regex would reject anyway.

---

## 5. Instrument constraints the new P5 note must satisfy (c2, unchanged)

Read from `.ufo/waves/round-17/measure.py` [OBS]; these are the acceptance mechanics
that decide credit, not style guidance:

1. The note's path must be exactly `corpus/knowledge/theme-route-r18.md`; `used-by`
   matching is a strict string compare of comma-split cells (`used_by`, `:124`).
2. First **15** lines must contain a line starting `source:` with `S\d{3}` tokens
   (`:187-189`); at least one cited token must resolve to a row with `status=mined`,
   `tier=A`, and `used-by` naming this exact path (`mined_a`, `:129-132`).
   Non-qualifying tokens are simply ignored (no rejection for them).
3. Exactly one `surface:` line, byte-form `surface: P5` (`re.fullmatch(r'surface: (P[1-6])')`,
   `:197-200`); a second *distinct* `surface:` token is rejected (duplicate
   identical lines collapse into one set member).
4. All four headings must exist exactly (`## Upstream contract`, `## Host
   declaration`, `## Safe observation`, `## Unexercised behavior`), each with ≥3
   non-blank body lines (`FACET_MIN_LINES=3`), and `[UNK]` must appear **inside** the
   `## Unexercised behavior` body (`:205-232`).
5. At least one cited qualifying row must have `kind ∈ {docs, spec, code}`,
   `https://` in its *source* cell, and a P5 keyword (`theme|wallpaper|hyprpaper|
   swaybg`) in source+scope lowercased (`:254-258`, `SURFACE_KEYWORDS`,
   `:145-152`).

**Source-row gap [OBS, blocking for the note]:** `corpus/SOURCES.md` currently has
**no** P5-keyword upstream row (`git status --porcelain -- corpus/SOURCES.md` empty
and no `S072`+ row at this read; re-check at integration if L1's merge adds rows). `grep -c 'theme\|wallpaper\|hyprpaper\|swaybg'`
over the registry returns **1**, and that hit is S059 — a `code`/A row describing
*host* P4 terminal declarations (`bindings.conf`, `xdg-terminals.list`,
`alacritty.toml`, and incidentally the `alacritty.toml` theme import hash
`8c3d1457…`). S059's source cell is a host path, not `https://`, and its `used-by`
is only `corpus/knowledge/terminal-route-r17.md`; registry ceiling is S071. So the
P5 note's upstream leg requires new rows (L1 reserves S072–S099) that are `mined`,
tier A, tag-pinned https `docs|spec|code`, name theme/wallpaper/swaybg in
source/scope, and list `corpus/knowledge/theme-route-r18.md` in `used-by`. L1/connector
must add those rows and the `used-by` edits; the note author cannot satisfy c2 alone.
Candidate upstream anchors (unopened; verify path and record a receipt first):
`raw.githubusercontent.com/swaywm/swaybg/<tag>/…` (N1),
`raw.githubusercontent.com/basecamp/omarchy/<tag>/…` for the theme scripts/skill
(N2), and a Chromium `BrowserThemeColor` policy doc (U2). No fetch was made by this
seat, so there are no receipts to cite and no tag→commit claims here.

---

## 6. Residual unknowns / confidence

- Live-plane values (swaybg/layer PIDs, waybar pid, makoctl mode, gsettings
  icon-theme, session `printenv`, gate verdict counts) were **not** re-measured and
  are not re-measurable under the pause → cite the round-7 window and date them
  `[O-hist]`. {high}
- "No theme set after 2026-10-19" is `[INF]` from `theme.name` mtime +
  re-read of the ritual's write order; a set with `OMARCHY_THEME_SKIP_BACKGROUND=1`
  would still touch `theme.name`, so the inference covers every set, not only ones
  with a background. {high}
- Upstream omarchy tag v3.8.4 existence/identity upstream is `[UNK]`; local bytes
  only prove the checkout state. {medium}
- The note's §11.1 "render unresolved" stays unresolved; documentary work narrows
  vocabulary (what is requested), never pixels. {high}
- Structural hazard the note should avoid: `theme-wallpaper-plane.md` is append-only
  and its §2/§4 are safe to cite, but its §0/§5-caution/§6/§11.4/§4.1-obsidian lines
  are stale or wrong as summarized in §3; a P5 note that cites the file without
  disambiguating the section will inherit the errors. {high}

## 7. In-flight draft cross-check (advisory; not a review verdict)

Read `corpus/knowledge/theme-route-r18.md` at 2026-10-20 12:44:34 −03 (145 L,
17,757 B, untracked; seat `NoteTheme`, rows draft at
`.ufo/waves/round-18/drafts/NoteTheme-rows.md`). At that instant:

- The first 15 lines carry `source:` with four `S0xx-pending-*` tokens (expected —
  L1 has not assigned ids), `verified-at:`, `recheck:`, and a byte-exact
  `surface: P5` at line 4.
- The four required headings exist at `:38` / `:74` / `:123` / `:134`; the
  `## Unexercised behavior` body contains `[UNK]`.
- None of §3's hazards is repeated: no `retro-82`/digit round-trip caution, no
  `wallpaper.live`/`display_agree` row claim, no `theme.choice` row claim.
  `obsidian` appears only as a setter list item (`:45`) and as a template-render
  note (`:115`), not as a failed sync.
- `source:` cites tag-pinned swaybg v1.2.2 and omarchy v3.8.4 bytes and receipts
  under `.ufo/waves/round-18/fetch/NoteTheme/` — the shape c2 needs. Whether those
  rows are later registered `mined`/A with `used-by` naming the note remains the
  blocking dependency in §5.
- The draft is owned and moving (another seat); re-read at integration. This
  section records only what the bytes said at 12:44:34, not approval. One useful
  hand-in: the draft's `:115` says the obsidian setter "was not opened in this
  pass"; §4.2 above carries the exact precondition chain it could adopt.

Re-derivation commands (all read-only; `$O=~/.local/share/omarchy`):

    src=$HOME/.config/omarchy/current/theme
    sha256sum "$HOME/.config/omarchy/current/theme.name" "$src"/{alacritty.toml,colors.toml,hyprland.conf,hyprlock.conf,mako.ini,swayosd.css,walker.css,waybar.css}
    readlink "$HOME/.config/omarchy/current/background"; stat -c %s "$HOME/.config/omarchy/current/background"
    find "$src" -maxdepth 1 -type f | wc -l; find "$src/backgrounds" -maxdepth 1 -type f | wc -l; du -sb "$src"
    sed -n '5p' "$O/default/hypr/autostart.conf"; sed -n '3p' "$O/default/hypr/envs.conf"
    sed -n '7,10p;16,17p;44,50p' "$O/bin/omarchy-theme-bg-next"
    sed -n '17p;41,50p;53,71p' "$O/bin/omarchy-theme-set"
    sed -n '7,10p' "$O/bin/omarchy-theme-set-obsidian"; stat -c '%y %s' "$HOME/.config/obsidian/obsidian.json"
    printf 'matte-black\n' | /usr/bin/sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g'
    ls "$O/themes" | while read -r n; do printf '%s\t%s\n' "$n" "$(printf '%s\n' "$n" | /usr/bin/sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g')"; done
    grep -n 'installed swaybg\|upgraded swaybg\|installed mako\|upgraded mako' /var/log/pacman.log
    grep -c 'wallpaper.live\|display_agree' tools/mado-verify.sh
    grep -oE 'row theme theme\.[a-z_.]+' tools/mado-verify.sh | sort -u
    grep -n 'exempted by name' corpus/knowledge/gate-standing-use.md

No claim in this report rests on an unread byte or an unrun command other than the
`[INF]` rows marked above; the round-7 note's live `[O]` statements are carried as
history, not re-asserted.
