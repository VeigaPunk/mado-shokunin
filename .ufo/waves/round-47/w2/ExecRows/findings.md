# ExecRows — w2 falsify: re-opened SOURCES candidates (round 47)

Scope: the 13 landed candidate rows S326–S338 (`.ufo/waves/round-47/w1/ScrRows/rows.md`), the 6+6
candidate rows of `.ufo/waves/round-47/w1/ScoutSpecs/{sources,candidate-rows}.md`, and the
`ScoutOmarchy/sources.md` candidates. Every URL below was fetched 2026-10-26; the fetched bytes,
their sha256 and the URL list are in `fetch/` (`sha256sums.txt`, `urls.txt`). Host files were read
as bytes only; no compositor, terminal or network service was started.

All seat commands used `S=/fast/scratch/hyaku/mado-r47/ExecRows` (deleted at the end).

## A. What holds (re-verified today, no hole)

| row | artifact | bytes | sha256 | verdict |
|---|---|---|---|---|
| S326 | xdg-terminal-exec v0.14.3 script | 44020 | 89f2be9a…3127ac | match; tag v0.14.3 = commit `065925df9f419008159258ae169018bfd23df71b` (`git ls-remote --tags`) |
| S327 | README.md v0.14.3 | 14762 | c7a1a8bb…a9d40 | match |
| S328 | xdg-terminal-exec.1.scd | 6071 | 3dba162f…876ec59 | match (anchors: see F2) |
| S329 | test/tests.bats | 8181 | ce4b6342…986b311 | match; 24 `@test` cases present |
| S330 | proposals/xdg-terminal-exec.md @ MR head | 10498 | c16a717a…ca8375a | match via the raw API URL; MR still `opened`, head `64c429df…`, updated 2026-07-31 (API) |
| S331 | desktop-entry-spec.xml @ a0eaad5 | 71116 | a1baadee…29f8f8f81 | raw bytes match; URL mismatch see F4. xdg-specs a0eaad5 committed 2026-10-19 (API), matching the row's date |
| S332 | basedir-spec.xml @ a0eaad5 | 15498 | c44dba06…c8029ae | raw bytes match; URL mismatch see F4 |
| S333 | omarchy v3.8.3 Alacritty.desktop | 452 | 713703ba…d057683 | match; tag v3.8.3 = `6aa2aec1c035` (ls-remote, both `omacom/` and `basecamp/`) |
| S334 | omarchy v3.8.3 xdg-terminals.list | 127 | d035da57…ceb71b | match; = host `~/.config/xdg-terminals.list` (same digest, S059) |
| S335 | omarchy-default-terminal | 1173 | 42e42225…d26ead91 | match |
| S336 | omarchy-cmd-terminal-cwd | 565 | 1c262a80…d7f3c | match |
| S337 | host user / system Alacritty.desktop | 452 / 374 | 713703ba… / d420b0f4… | match; system entry has no `X-TerminalArg*`, has `X-Desktop-File-Install-Version=0.28` (read whole file) |
| S338 | host omarchy version + 2 files | 6 / 452 / 127 | 0a5c2952… / 713703ba… / d035da57… | version file is `3.8.3\n`; both files equal the tag bytes — but see F8 |

Structural checks (all 13 rows, plus all 12 ScoutSpecs candidate rows): 11 cells per row, no cell
containing a `|` (every row parses to exactly 11 cells; `python3` split check), status `mined`/`queued`
and `opened 2026-10-26` as the census requires.

Anchors spot-checked line by line against the fetched pins (first/last line of every range):

- S326: 143 `make_paths()`, 179 `gen_hash()`, 217 `read_cache()`, 351 `read_config_paths()`, 754
  `find_entry_paths()`, 802 `check_entry_key()`, 970 `read_entry_path()`, 1055 `find_entry()`,
  1387 `# option prepend`…1499 `exec "$@"` — all inside the 1499-line file.
- S327: 257 `# Notes`, 268 performance, 282 compat mode, 295 `### Cache`, 320 Exec parsing, 333
  `## Other implementations` — exact.
- S329: 6 `setup()`, 127 hidden, 137 TryExec, 147 desktop-specific config, 158 Turkish collation,
  173 ShowIn, 217 quoting — exact.
- S331: 147 `sect2 desktop-file-id`, 184 basic-format, 264 value-types, 446 recognized-keys, 486
  Type, 568 Hidden, 582 OnlyShowIn, 636 TryExec, 649 Exec, 681 Actions, 800 exec-variables, 1196
  extra-actions — exact.
- S332: 136 DATA_HOME, 207–210 the precedence sentence, 279–287 the lookup example — inside the cited 136–215 / 264–320.
- S333/S337: `X-TerminalArg*` keys at lines 14–17 of the 21-line file — exact.
- S335: 7–17 read-current, 19–28 name map, 30–34 heredoc — exact. S336: 6, 7, 10–11, 14 — exact.

Teaches claims verified in the pin: S326 "listed IDs first, ShowIn off; fallback after, ShowIn on"
(`xdg-terminal-exec:1057-1072`), Cache key `md5` + `XDG_CURRENT_DESKTOP` + `ls -LRl` (`:179-215`),
discard on Category/TryExec/Hidden/Exec[0]/Actions (`:816-821, 829, 933-935, 938-942, 962-966`
within `check_entry_key`); S327 compat-mode default and `/execarg_default` (`README.md:282-293`), Exec
expanded twice and invalidating (`:320-331`), cache bypass (`:295-318`); S328 first-listed-valid and
fallback order (`xdg-terminal-exec.1.scd:86-92`), print order id/path/content/cmd (`:58-63` and
`proposals/…:214-232`).

Candidate rows (ScoutSpecs x2, identical sets): digests match today's fetch (8b2e39ee basedir@373ecf4,
3ba22826 desktop-entry@d0589e0, de638bb4 menu@7860a23, c16a717a MR3 file, ce4b6342 tests.bats,
3dba162f man); anchors land on the described sections (menu :385 / :2000 TerminalEmulator row /
:2418 glossary; basedir :127 relative paths, :138 DATA_HOME, :144 CONFIG_HOME, :186 DATA_DIRS,
:197 CONFIG_DIRS, :214 CACHE_HOME; desktop-entry :150, :235, :298, :486, :572, :582, :636, :811,
:957, :1211). "24 bats tests" is true (`grep -c '^@test'` = 24).

## B. Holes found (each with a reproducible command)

### F1 — S326 teaches a rule the resolver does not implement (`Type`)

S326 teaches: "an entry is discarded on … a **Type it cannot use** …". v0.14.3 never inspects `Type`.

```
grep -in 'type' <pin>/xdg-terminal-exec
# 503,766,887,899,907,914,921,928 only (URL comment, `find -type f`, "value-types" comments) —
# no 'Type' key case
sed -n '802,969p' <pin>/xdg-terminal-exec | grep -n "^	'"
# Categories, Actions, OnlyShowIn, NotShowIn, X-TerminalArgExec|TerminalArgExec, X-ExecArg|ExecArg,
# X-TerminalArgAppId, X-TerminalArgTitle, X-TerminalArgDir, X-TerminalArgHold, TryExec, Hidden, Exec
sed -n '967p' <pin>/xdg-terminal-exec
# # By default unrecognised keys, empty lines and comments get ignored
```
Impact: the row is cited by the C2 entry (`source: S326`), so a false validation claim sits under the
claim's own cited row. Fix: delete "a Type it cannot use" (or move it to a "spec says, script does
not" note). This is the only teaches sentence I could falsify; the rest of S326's list is in
`check_entry_key`.

### F2 — S328 anchor mislocates ENVIRONMENT; the cache-path fact falls outside every cited range

Row: `xdg-terminal-exec.1.scd:123-141 FILES, xdg-terminal-exec.1.scd:143-149 ENVIRONMENT`.

```
grep -n 'Cache file\|ENVIRONMENT\|^# ' <pin>/xdg-terminal-exec.1.scd
# 124:# FILES   149:Cache file:   152:# ENVIRONMENT   160:# EXTERNAL LINKS
```
So 143–150 is the FILES tail (Desktop Entry dirs at 140–147, `Cache file:` at 149, the cache path at
150); ENVIRONMENT is 152–159. The row's own fact "the cache file is XDG_CACHE_HOME/xdg-terminal-exec"
lives at :150, one line past the cited 149. Also scope "58-121 configuration and directives" starts in
the print-order list (58 "Selected data is printed in order", 60–63 the order, 65 `# CONFIGURATION`). Fix: `124-150
FILES`, `152-159 ENVIRONMENT`, `58-63` print order / `65-121` configuration.

### F3 — S330's URL is not the artifact and is not ref-pinned in the URL

Source cell = `…/-/merge_requests/3`; fetching it yields 92978 B of HTML, sha256
`b13f699990c31afcc52e2aeb563b8bca40a874be50cbf53bc68b7a94b53eb67f`, not the recorded `c16a717a…`
(10498 B `proposals/xdg-terminal-exec.md`). The anchor `proposals/xdg-terminal-exec.md:25-52` is
unreadable from that URL. The frozen C2 counter tolerates it (ref-less URL + a recorded 40-hex commit
`64c429df…` + digest), but the row is only reproducible through the raw API URL that the ScoutSpecs
candidate already carried. Fix: put the raw API URL in the source cell.

### F4 — S331/S332 cite `/-/blob/` pages whose bytes are not the recorded digest

```
curl -sSL '<row URL>' | sha256sum
# desktop-entry: 39624 B HTML 95a560152eca052c1b52745e04eb005f87d4cb32f9d8e09705203737694aaeb5
#                (row/receipt: 71116 B a1baadee9676a2e333377907b3eb7fb06df91976db9a013d29d338fa429f8f81)
# basedir:       39468 B HTML 90f7c6111e6704678aff3531c25fb11e30e0f5326bb61ecf63c876578beb5758
#                (row/receipt: 15498 B c44dba06041dcfa53c676071615c73b7407242841feadc2affd777b76c8029ae)
```
The digests are correct for `…/-/raw/a0eaad5…/…`. Fix: use the `/-/raw/` URL (or state the page and
the raw receipt separately), so a reader following the row gets the hashed bytes.

### F5 — S334 carries no fetch receipt; C2 clause c cannot bind it

`sed -n '22p' rows.md | grep -c receipt` → `0`. The counter requires exactly one
`.ufo/waves/round-47/fetch/<name>` receipt per cited row (`row_receipts`), so S334 reports
`fetch_receipts=[]` (see `gate/clause-c-probe.out`). Its bytes are pinned by digest only and equal to
both `fetch/xdg-terminals.list` and `fetch/omarchy/omarchy-xdg-terminals.list`. Fix: add one of
those receipt paths.

### F6 — every drafted receipt path is outside the C2 counter's pin namespace

Counter: `row_receipts` matches only `.ufo/waves/round-47/fetch/<name>`; the rows name
`.ufo/waves/round-47/w1/ScrRows/fetch/<name>`. Evidence: `gate/clause-c-probe.out` (run `gate/clause-c-probe.py`) — all 13 rows
fail `fetch_receipts=[]`, plus `no_url` for S337/S338. With a purely mechanical repath
(`w1/ScrRows/fetch/` → `fetch/`), the same probe's `repathed` pass shows only S326 (9 ranges), S327 (6),
S328 (5), S331 (1) bind; the rest still fail:

| row | failure after repath | needed pin |
|---|---|---|
| S329 | `pin_missing=tests.bats` | name must be `test/tests.bats` |
| S330 | `pin_missing=spec-xte-proposal.md` | pin is `xdg-terminal-exec-proposal.md` |
| S332 | `pin_missing=basedir-spec.xml` | absent from `.ufo/waves/round-47/fetch/` (lane working tree and freeze commit) |
| S333 | `pin_missing=om/applications_Alacritty.desktop` | pin is `omarchy/omarchy-Alacritty.desktop` |
| S335 | `pin_missing=om/bin_omarchy-default-terminal` | no pin in `fetch/` |
| S336 | `pin_missing=om/bin_omarchy-cmd-terminal-cwd` | no pin in `fetch/` |
| S337 | `no_url`, `pin_missing=host/Alacritty.desktop.user` | no URL in the row; no `fetch/host/` |
| S338 | `no_url`, `pin_missing=host/omarchy-version` | no URL in the row; no `fetch/host/` |

Because the counter applies clause c only to ids named by `source:` lines in the entry head, the C2
entry can still pass with S326+S327 alone — but only if those two receipts are repathed. The freeze
commit `d7527d6` itself contains just three pins (`git ls-tree -r d7527d6 -- .ufo/waves/round-47/fetch/`:
README.md, xdg-terminal-exec, xdg-terminals.list); the other six are untracked working-tree files and
must be committed with the data or clause c has nothing to bind.

### F7 — S337/S338 have no URL (C2 `no_url`)

Both rows are host-path evidence. The frozen counter refuses a cited row with no URL, and no pin
exists for them. Either they stay uncited by the entry head (fine) or the row must gain a ref-pinned
URL plus a committed pin.

### F8 — S338's "installed deployment is v3.8.3" is contradicted by the checkout HEAD

```
git -C ~/.local/share/omarchy rev-parse HEAD   # 8fcc9d6048af4cb0e3af8512c78049857a3b53dd
git -C ~/.local/share/omarchy describe --tags  # v3.8.4
od -c ~/.local/share/omarchy/version           # 3 . 8 . 3 \n
```
The version file says 3.8.3 while the checkout is v3.8.4; the four selection files are byte-identical
at v3.8.3 and v3.8.4 (I fetched 8fcc9d60: 713703ba…, d035da57…, 42e42225…, 1c262a80… — same digests),
so every S333–S336 pin survives. Only the wording "the installed deployment is v3.8.3" overreaches:
say "the version file claims 3.8.3; the checkout is v3.8.4 and the pinned files are unchanged between
the two tags".

### F9 — ScoutOmarchy's "only basecamp/omarchy resolves" is stale

`ScoutOmarchy/sources.md` says the `omarchy/omarchy` org URL 404s and only `basecamp/omarchy`
resolves. Today `curl -sS -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/config/xdg-terminals.list`
→ `200` (no redirect), and `git ls-remote --tags https://github.com/omacom/omarchy.git` lists
`v3.8.3 → 6aa2aec1c035…`, `v3.8.4 → 8fcc9d60…` (same SHAs as basecamp) plus `v4.0.x…v4.5.0-rc1`.
So the landed rows' `omacom/` URLs are valid and canonical; the stale note should not be carried into
v2. Its other claim (checkout HEAD 8fcc9d60) is true.

## C. Census gate (required deliverable)

Mirror: `rsync -a --exclude=.git --exclude=.jj <lane>/ $S/mirror/`, the 13 rows inserted after S325 in
`corpus/SOURCES.md` (275 registry rows total), a mirror-only stand-in at
`corpus/knowledge/xdg-terminal-selection-r47.md` so `used-by` resolves.

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
     --file $S/mirror/corpus/SOURCES.md --today 2026-10-26
```
- without the stand-in: **exit 1**, exactly 13 `E11` (one per new row) — `gate/validate-no-standin.txt`.
- with the stand-in: **exit 0**, no E-codes, 17 findings = 15 pre-existing (`W01 S277`, 14 × `W04`) +
  the two expected `W04` on S326/S327 (same URL as S057/S056) — `gate/validate-with-standin.txt`.

The census does not check URL pinning, digests, receipt paths or anchors (see
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:24-33, 592-660`), so a clean exit here is
necessary but not sufficient; F1–F8 are the census-invisible failures.
