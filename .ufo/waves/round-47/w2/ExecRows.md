# ExecRows — w2 FALSIFY (round 47, lane mado-shokunin)

Scope: re-opened every candidate SOURCES row of the round — the 13 landed rows S326–S338
(`w1/ScrRows/rows.md`), the 6+6 candidates in `w1/ScoutSpecs/{sources,candidate-rows}.md`, and
`w1/ScoutOmarchy/sources.md` — fetched each URL today, hashed it, compared against the row,
re-checked anchors line by line, checked row shape, then mirrored the corpus, appended the rows
after S325 and ran the census validator.

Artifacts (all under `.ufo/waves/round-47/w2/ExecRows/`):
`findings.md` (full detail, repro commands), `fetch/` (today's bytes + `sha256sums.txt` + `urls.txt`),
`gate/` (census outputs + exits, `clause-c-probe.py` and its `clause-c-probe.out`).
Scratch `/fast/scratch/hyaku/mado-r47/ExecRows` deleted after copying.

## Verdict

The 13 rows are **byte-faithful** — every URL-fetched artifact hashes to the digest the row records,
today, and equals the w1 receipt; host-file rows match the host bytes; all rows have 11 cells with no
`|` inside a cell; the census validator passes. But **nine reproducibility defects** remain before the
data commit (no row can be edited by me — the L1 owns integration):

1. **F1 (false teaches, S326):** the row says an entry is discarded on “a Type it cannot use”. v0.14.3
   never reads `Type`; `check_entry_key` (`xdg-terminal-exec:802-967`) validates only Categories,
   Actions, OnlyShowIn, NotShowIn, X-TerminalArg*/ExecArg*, TryExec, Hidden, Exec, and ends
   `:967 # By default unrecognised keys … ignored`. Repro: `grep -in type <pin>/xdg-terminal-exec`
   (only a URL comment, `find -type f`, value-types comments).
2. **F2 (mislocated anchor, S328):** `:143-149 ENVIRONMENT` — `# ENVIRONMENT` is at `:152`; 140–150 is
   the FILES tail, and the row's own cache-path fact sits at `:150`, outside every cited range. Repro:
   `grep -n 'Cache file\|ENVIRONMENT' xdg-terminal-exec.1.scd` → `149` / `152`.
3. **F3 (S330 URL ≠ artifact, not ref-pinned in the URL):** the MR page returns 92978 B HTML
   (`b13f6999…`), not the recorded 10498 B `c16a717a…`; anchors name `proposals/xdg-terminal-exec.md`
   lines. The raw API URL (already in the ScoutSpecs candidate) is the reproducible one. MR still
   `opened`, head `64c429df…`, updated 2026-07-31 (API).
4. **F4 (S331/S332 `/-/blob/` URLs ≠ recorded digest):** as written they return 39624 B / 39468 B HTML
   (`95a56015…`, `90f7c611…`); the recorded `a1baadee…` / `c44dba06…` are the `/-/raw/` bytes. Use
   `/-/raw/a0eaad5…/…`.
5. **F5 (S334 has no fetch receipt):** `grep -c receipt` on its row = 0 → C2 clause c
   `fetch_receipts=[]`. Its bytes equal `fetch/xdg-terminals.list` and
   `fetch/omarchy/omarchy-xdg-terminals.list`; name one.
6. **F6 (receipt namespace vs frozen C2 counter):** `row_receipts` accepts only
   `.ufo/waves/round-47/fetch/<name>`; the rows name `.ufo/waves/round-47/w1/ScrRows/fetch/<name>`, so
   **all 13 fail clause c as drafted** (`gate/clause-c-probe.out`). After a mechanical repath only
   S326/S327/S328/S331 bind; S329 needs `test/tests.bats`, S330 needs `xdg-terminal-exec-proposal.md`,
   S332 needs `basedir-spec.xml` (absent), S333/S335/S336 need `omarchy/…` pins (two absent), S337/S338
   need `no_url` fixes plus `host/` pins (absent) — `gate/clause-c-probe.out` (repathed pass). The freeze commit
   `d7527d6` holds only three pins; the other six are untracked and must land with the data.
7. **F7 (S337/S338 have no URL):** the frozen counter refuses a cited URL-less row; they are safe only
   if the entry head never cites them.
8. **F8 (S338 inference):** `~/.local/share/omarchy/version` says `3.8.3`, but the checkout HEAD is
   `8fcc9d60…` = tag **v3.8.4**. The four selection files are byte-identical across v3.8.3/v3.8.4
   (fetched both), so S333–S336 pins stand; only “the installed deployment is v3.8.3” overreaches.
9. **F9 (ScoutOmarchy note stale):** `omacom/omarchy` resolves today (raw 200, tags v3.8.3→`6aa2aec1c035`,
   v3.8.4→`8fcc9d60`, plus v4.x), so the landed `omacom/` URLs are valid; do not carry “only
   basecamp resolves” into v2.

Verified clean (details in `findings.md` §A): S326–S338 digests all match today's bytes and the w1
receipts; v0.14.3 tag = `065925df…`; v3.8.3 tag = `6aa2aec1c035`; anchors S326/S327/S329/S331/S332/
S333/S335/S336/S337 land on the stated functions/sections/lines; the six ScoutSpecs candidates hash
(`8b2e39ee`, `3ba22826`, `de638bb4`, `c16a717a`, `ce4b6342`, `3dba162f`) and anchor as stated,
“24 bats tests” is true, and xdg-specs `a0eaad5` is dated 2026-10-19 as S331 says.

## Census gate (mirror + rows after S325)

Mirror `rsync -a --exclude=.git --exclude=.jj <lane>/ $S/mirror/`; 13 rows inserted after S325 (275
registry rows); mirror-only stand-in at `corpus/knowledge/xdg-terminal-selection-r47.md`.

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md --today 2026-10-26`

WITH stand-in — **exit 0**, no E-codes, 17 findings (15 pre-existing + the 2 expected new W04):

```
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
file	W04	S303 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp across scopes
file	W04	S307 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
file	W04	S317 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp across scopes
file	W04	S318 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp across scopes
file	W04	S320 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
file	W04	S321 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp across scopes
file	W04	S324 duplicate url raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp across scopes
file	W04	S326 duplicate url raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec across scopes
file	W04	S327 duplicate url raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md across scopes
file	ok	/fast/scratch/hyaku/mado-r47/ExecRows/mirror/corpus/SOURCES.md
```

WITHOUT the stand-in — **exit 1**, exactly 13 `E11` (`S326`–`S338 missing used-by
corpus/knowledge/xdg-terminal-selection-r47.md`), no other E-code (`gate/validate-no-standin.txt`).
The census does not test URL pinning, digests, receipt paths or anchors, so this clean exit is
necessary but not sufficient — F1–F8 are invisible to it.

## Risks / notes for the L1

- The C2 clause-c failures are integration mechanics, not bad bytes: repath the two cited receipts
  (S326, S327) and cite only rows whose pin actually exists under `.ufo/waves/round-47/fetch/`.
- If the final entry cites S330–S338, the missing pins (`basedir-spec.xml`, the two omarchy scripts,
  the three host files) and the renamed pins (`test/tests.bats`, `xdg-terminal-exec-proposal.md`,
  `omarchy/omarchy-*`) must be fixed in the rows, not in the counter (the counter is frozen).
- S334's missing receipt and S337/S338's missing URLs are the only *structural* row defects the
  census cannot see.

No blockers. No tool installed or upgraded. No lane or host file written outside
`.ufo/waves/round-47/w2/ExecRows/` and this report; host trees read as bytes only; no terminal,
compositor mutation or package transaction.
