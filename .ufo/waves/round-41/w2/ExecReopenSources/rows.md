# ExecReopenSources — rows S283–S289 + S037 re-open attack

Seat: ExecReopenSources (w2, round 41). Date: 2026-10-25. Data commit read: `07f2641696b5ac73de1404ea737a9f27e9819aa1`.
Each row was re-opened: raw URLs named in `corpus/SOURCES.md` re-fetched with `curl -sSL` (all HTTP 200), sha256 compared
against the fetch receipt and the row; S287 = issue page re-fetch; S289 = saved journal re-read + read-only
`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` snapshot; S037 = read-only
`cat /var/lib/pacman/local/xdg-desktop-portal-hyprland-*/desc` + GitHub API tag/release check.

## Table

| row | re-opened (HTTP, sha256 equal?) | quote located at line | anchor checked | tier ok | verdict |
|---|---|---|---|---|---|
| S283 | HTTP 200; fresh sha256 `0bc60c14…` == receipt == row (5447 B) | 1/6 byte-exact (`doesn't destroy existing focus grab objects` @55); other 5 are wrapped XML prose (@33-35, 62-63, 66-69, 72-73), exact under newline normalization | `:33-37` desc (text 33-35), `:39-58` manager (38-58), `:60-77` grab desc (61-77), `:79-127` requests/event — all fit | spec/A = spec, primary | no defect; note N1 (5 normalized-only quotes incl. the Gate quote) |
| S284 | HTTP 200; fresh sha256 `53b762f7…` == receipt == row (6242 B) | 3/7 byte-exact (`m_grab->m_keyboard = true;` @20, `setCallback…finish(true); });` @22, `called with no committed surfaces. This should never happen.` @110); 4 are C++ statements split across lines (49-50, 62-63, 68-69, 137-141), exact under normalization | `:15-29` ctor, `:31-33` dtor, `:47-56` start, `:58-71` finish, `:94-111` refocusKeyboard, `:113-143` commit, `:149-173` bindManager/onCreateGrab — all verified | code/A = source at host commit | no defect; note N1 |
| S285 | HTTP 200; fresh sha256 `6f7cecf1…` == receipt == row (2568 B) | 1/3 byte-exact (comment @78); 2 statements split (67-68, 83-86), exact under normalization | `:21-58` addWindow defers, `:66` add_surface, `:75` commit in sync, `:78-86` comment+activated emit, `:98-101` cleared handler — all verified | code/B = third-party client code, B allowed (community never A, B is fine) | no defect; note N1 |
| S286 | HTTP 200; fresh sha256 `15c3e39c…` == receipt == row (24182 B) | 2/2 byte-exact (`| Got interface: {} (ver {})` log @88; `if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)` @99) | `:85-88` log before branches, `:90-129`+`:247-259` bind branches, `:300-301` registry callbacks — verified; **anchor branch list omits the `foreign_toplevel` branch @249** (entry lists all 10 correctly) | code/A = upstream tag source | finding F1 (anchor enumeration incomplete; scope "nine it binds" counts only the 9 direct `wl_registry_bind` sites) |
| S287 | HTTP 200; fresh sha256 `cb60a026…` ≠ receipt `148a9053…` — dynamic page, first diff at byte 26145 = `fetch-nonce` meta, size 475169 vs 475170; all content claims verified in both | 4/5 byte-exact (`windowrule…` @644/645/656/898/917, `When the new window opens…` @644/645/661, `Tried to set workspace silent rule…` @644/686/706, `fixed in b09f157` @644); expected-behavior sentence exists only with markdown backticks (`silent`) and a longer tail — entry quote is the backtick-stripped truncated fragment (note N2) | receipt lines 686 & 706 both hold the quoted log block; Expected/Actual sections present; state CLOSED + COMPLETED ×3, created 2022-08-23T14:03:55Z ×4, 2022-08-25 ×18 — all in receipt and fresh | community/B = never A, B ok | no content defect; notes N2 (markup-normalized quote), N4 (dynamic nonce) |
| S288 | HTTP 200; fresh sha256 `3c700763…` == receipt == row (1903 B) | 1/2 byte-exact (`for grabbing input focus, primarily for complex context menus` @17); bridge/“maintain a set” sentence wraps @5 and @8-9 (normalized only) | `:5` bridge sentence, `:13-23` Finished list, `:17` focus-grab bullet, `:22` input-capture bullet — all verified | docs/A = upstream README at commit | no defect; note N1 |
| S289 | journal snapshot re-run today is byte-identical to receipt (153 lines, 19130 B, sha256 `bf8fa91a…`); `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso \| wc -l` = 153 | 6/6 byte-exact: `Stopped Portal service (Hyprland implementation).` @76, `-- Boot` @78, `Starting Portal service (Hyprland implementation)` @79, `XDG_CURRENT_DESKTOP set to Hyprland` @82, `Gathering exported interfaces` @83, `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` @117 (pid 1952, `2026-10-25T13:36:24-03:00`) | whole-file anchor verified; census recomputed: sessions=2, adverts=78, latest=63 distinct, focus_grab=1, first session=15; `focus` occurs exactly once in the journal | own-work/A = lane's own measured output (CORPUS.md A includes “the lane's own re-runnable gate output”) | no defect; note F3 (recheck=`on-change` outside enumerated cadences) |
| S037 | package record re-read: `%NAME% xdg-desktop-portal-hyprland`, `%VERSION% 1.4.1-2`; desc sha256 `7bf2f8be…` matches receipt output; API: tag v1.4.1 → object `cc8e5ef8fb2acef3db488b9a33b0c48c2a4ee204` (commit), release published `2026-07-29T21:06:01Z` — row anchor confirmed | entry quote `%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2` is composed from two separate desc fields (no single line contains it) — note N3 | row anchor `v1.4.1`/`Changes`, tag commit `cc8e5ef`, released 2026-07-29 — verified | docs/A = upstream release page; used-by now includes `corpus/knowledge/hyprland-focus-grab-r41.md` | no defect; note N3 |

## Findings

- **F1 — S286 anchor enumeration incomplete (minor, row-level).** The row anchor names nine bind branches and omits the
  `zwlr_foreign_toplevel_manager_v1` branch at `src/core/PortalManager.cpp:249` (`else if (INTERFACE == zwlr_foreign_toplevel_manager_v1_interface.name) { m_sHelpers.toplevel = std::make_unique<CToplevelManager>(…); }`). The entry's own §3 lists all ten branches correctly. The journal proves the branch binds (`[toplevel] Activated, bound to 55cc6bdd08d0`, receipt line 12), so scope/teaches “which nine it binds” is a selective count of the nine direct `wl_registry_bind` sites and understates the handler set. Not fabricated content; recommend the anchor list all ten branches (or say “nine direct registry binds plus a foreign-toplevel manager”).
- **F3 — S289 recheck=`on-change` is outside CORPUS.md's enumerated cadences** (`90d`, `180d`, `on-release`; CORPUS.md:105-106). Same known minor class flagged in earlier rounds (round-17 ReopenS065 D3); accepted by validator policy (symbolic cadences are reported, never judged overdue). Note, not a new defect.

## Notes (quote precision, no content misquote)

- **N1 — wrapped/multiline quotes.** 12 of the entry's 31 checked quotes are not byte-verbatim substrings of their sources
  because the source wraps the text (XML prose, C++ statements split across lines, README wrapped sentences). Each is exact
  after whitespace normalization (newlines/collapsed runs → single space) and ≤25 words. This includes the lesson's GATE
  quotes for S283. Faithful, but not byte-verbatim; the strict reading of CORPUS.md rule 1 (“a ≤25-word quote”) is
  satisfied only under normalization.
- **N2 — S287 expected-behavior quote is markup-normalized.** `If a workspace windowrule contains silent then matching windows
  should not get focus` appears in the issue text as `If a workspace windowrule contains \`silent\` then matching windows
  should not get focus, unless that window's workspace is already the active one.` — the entry quote strips the markdown
  backticks and truncates before the trailing conditional clause. The words are the reporter's, verbatim modulo backticks.
- **N3 — S037 gate quote is composed.** `%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2` joins two separate `desc`
  fields (`%NAME%`/`%VERSION%` blocks, blank-line separated); no single line contains the string. All five tokens appear
  verbatim in the package record.
- **N4 — S287 page is dynamic.** The only difference between receipt and fresh fetch is the `fetch-nonce` meta token (first
  diff byte 26145) plus a 1-byte size delta; every content claim (quotes, state, dates) survives in the fresh page.

## Reproduction (all read-only)

- `curl -sSL -o <seat>/fresh/<f> '<raw URL>'` for S283/S284/S285/S286/S288 (HTTP 200, sizes 5447/6242/2568/24182/1903 B)
  and S287 (`issue-565.html`); `sha256sum` per file — see table.
- `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso > <seat>/fresh/xdph-journal-current.txt && cmp -s … xdph-journal.txt` → IDENTICAL; `wc -c -l` → 153 / 19130; `sed -n '78p;117p'` → boot marker / advert.
- `cat /var/lib/pacman/local/xdg-desktop-portal-hyprland-*/desc`; `sha256sum` → `7bf2f8beeadf189be54460a72700f81722d9be78884a0a8ee56a46a70c9445a5`.
- `curl -sSL 'https://api.github.com/repos/hyprwm/xdg-desktop-portal-hyprland/releases/tags/v1.4.1'` → published_at `2026-07-29T21:06:01Z`, tag `v1.4.1`; `…/git/refs/tags/v1.4.1` → object `cc8e5ef8fb2acef3db488b9a33b0c48c2a4ee204` commit.
- `python3 quote_check.py` (seat dir): exact-vs-normalized matching for all 31 quotes; word counts all ≤25 (max 17).
- `hyprctl version` → `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f` — matches S284 pin and the entry's INF.
- `grep -cin 'focus' fresh/PortalManager.cpp` → 0, rc 1; `grep -ocin 'focus' <journal>` → 1 (only the advert).

## Installs

None. Used only pre-installed `curl`, `python3` (stdlib), `git` (read-only), `journalctl` (read-only), `sed`/`grep`/`cmp`/`nl` (coreutils). No pacman/package transaction; no host service or compositor mutation.
