author: hyaku closure (non-author integrator, @m_opus)

# mado round 48 — non-author closure spot-check

Lane HEAD before `579f694b45c797a9c39761fdb4f9e0a1b71b3585`, after `b361c8466bd203cda8ce38add796883cf8f97302`.
Driver digest (`.ufo/watchdog.log`, mutable — copied here):
`2026-10-26T20:34:11-03:00 launch mado round=48 pgid=2182744 driver=hyaku-inline attempt=1` /
`2026-10-26T21:58:35-03:00 lane-dead-no-report mado round=48; retry same round (hyaku-inline attempt=1: unspecified)` /
`2026-10-26T21:58:37-03:00 launch … attempt=2` / `2026-10-26T22:35:09-03:00 lane-dead-no-report … (attempt 2 exited incomplete, no report)` /
`2026-10-26T22:35:12-03:00 launch … attempt=3` / `2026-10-27T00:16:15-03:00 lane-dead-no-report … (attempt 3 L1 MadoR48-5 died in the
orchestrator session exit 2026-10-26 23:57:36 -03, SIGHUP during an operator omp update; salvaged to cf3deeec; NOT counted toward MAX_ATTEMPTS)` /
`2026-10-27T00:16:28-03:00 launch mado round=48 pgid=890225 driver=hyaku-inline attempt=4` /
`2026-10-27T01:04:49-03:00 complete mado round=48; hyaku-inline attempt=4`.

I did not author the round. I re-checked committed bytes with `git show`/`git ls-tree`/`git grep` at the cited revisions. I re-fetched
the upstream pins on 2026-10-27 and ran the host checks read-only. The deliverable ran from committed bytes. The resolver ran only with
`--print-*` flags and `XDG_CACHE_HOME` in scratch, so no terminal was launched. `xkbcli compile-keymap` ran in a clean environment.
I did not execute lane counters or gates (§Gate standard, Closure consequence); I verified their committed receipts instead. Three
read-only reviewer seats I dispatched (C1, C2, harm/conformance) did part of the re-checking. Their findings are folded in below and
marked "seat". Scratch `/fast/scratch/hyaku/closure-mado-r48` was removed.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-48/mado.md` (fleet) | `mado-shokunin a72080e7706d5a9ecd4c7bff1c8d2ca3d8f6d7d7`; committer 01:03:55, after lane tip 01:03:22 and before the complete line 01:04:49 (author date 00:59:15 is the jj snapshot that opened the change) (seat) | ok |
| SHONEN heading | `grep -n '^## SHONEN'` on the report | `:74`; 4 lines `[~]` for the 4 boxes | ok |
| cited commits exist and are ancestors | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for 5ff16742, 3e6c848a, 02165600, cf3deeec, e5d0130d, d8e3d600, f029de3a, 627914f6, b361c846 | all 9 `ok` | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain` | `local=remote=b361c846… ahead=0 behind=0 head=detached tracked=0 untracked=47`; all 47 untracked are inherited `*.synthetic` under `.ufo/waves/round-45/` and `round-46/` (`grep -v synthetic` → empty); `ls-remote origin refs/heads/master` = b361c846 | ok (see N1) |
| prompt carries the contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/mado-round-48.md)`; canonical template `diff` → identical | placeholder substitutions only; §3 L2 floor `:80`, §4 report contract + SHONEN `:99`/`:118`, §5 commit/push/L0 `:131-138`, §6 hyaku addendum `:141`, §7 scratch `:603`. Four prompt commits (57f9064e, b2c82b9c, 27732f55, 4acc8b87): §1-5 byte-identical; only §6 routing text and the attempt counter changed (seat) | ok |
| commits authored by lane identity | `git log --format='%an <%ae> %cn' 579f694b..b361c846` | 9 commits, all `mado-shokunin <mado@shokunin.local>` | ok (see A1) |

Attribution note A1 (status-neutral): `cf3deeec` is the orchestrator's salvage of attempt 3's uncommitted drafts, committed under the
lane identity. Its subject discloses this. Attempt 4 re-verified it: counters and fixtures were unchanged since the v2 freeze, and the
tool sha `14382047…` equals the bytes the v2 controls scored. My seat confirms `git diff --stat 02165600 b361c846 -- quality/counters`
is empty. The admitted data therefore rests on salvaged bytes that the lane re-verified, not on bytes it authored in the same session.

## 2. Per-claim re-check

**C1 — operability (capability acquisition): the warm-cache path of `tools/mado-terminal.py`.** Re-measured plainly, plus evidence-verified counter.
- Tool identity: `git show b361c846:tools/mado-terminal.py | sha256sum` → `1438204764…f34`, identical at cf3deeec, e5d0130d,
  f029de3a, 627914f6. This equals `receipts/v2/ctl/FINAL.txt:1` and `receipts/live-terminal-cache-r48.txt:3` (seat).
- Selftest from committed bytes: `python3 -I t.py --selftest` → `MADO_TERMINAL_SELFTEST: 70/70 passed`, rc 0 (seat; SCORECARD says 70/70).
- Live, against the real resolver: `sha256sum /usr/bin/xdg-terminal-exec` → `89f2be9a…27ac` = pin. With a fresh scratch `XDG_CACHE_HOME`,
  the resolver and the tool produce byte-identical stdout and rc 0 in four cache states. `explain --observed` gives `cache=absent verdict=AGREE`
  for the cold state and `cache=hit verdict=AGREE` once the resolver saved its cache (188 B). Zeroing line 1's hash gives
  `cache=stale verdict=AGREE`. Breaking the terminator gives `cache=invalid verdict=AGREE`. In both edited states the tool left the
  cache bytes unchanged (sha before = after); the resolver repaired its own copy (seat).
- HOME unset (round-47 D1): with `env -i PATH=/usr/bin:/bin`, HOME and XDG_CACHE_HOME unset, the resolver gives rc 1 with 0 bytes of
  stdout, and so does the tool; `cmp` shows identical output (seat). The round-47 narrowing is now modelled as the pin behaves.
- Fixtures (committed `c1-r48-fixtures-v2.json`): 228 entries; 204 in v1; 24 new by id; 10 `v2-hu-*`; 10 class `READDIR`
  (round-47 D3). The class tally sums to 228 (seat). These match the report and registration-v2.
- Counter (evidence-verified, not executed): `receipts/v2/ctl/BASE.txt` `warm=149/228 … selftest=fail … TARGET_MISSED exit=1`, with
  `tool_sha256=b84d5c4f…` = `git show 579f694b:tools/mado-terminal.py`. Its `rev=f3e3e46e` is the scratch-clone revision; the tool sha
  binds it to base. `c1-after-data.txt` `rev=e5d0130d … warm=228/228 explained=418/418 generated=230/230 selftest=ok readonly=ok TARGET_MET exit=0`.
  The same MET line appears in `a4/c1v2-at-salvage.txt` (cf3deeec), `c1-tip.txt` (f029de3a) and `c1-tip-final.txt` (627914f6). v1 beside it:
  `warm=204/204 … TARGET_MET`. Controls `v2/ctl-c1v2.txt`: `PASS (controls scoring TARGET_MET: 0 of 66 …)`. Do-nothing controls
  `a4/ctl-do-nothing.txt`: 149/228 and 154/228, both `TARGET_MISSED` (seat).
- Ruling: **verified**. The registered before→after holds on committed receipts. My seat's live runs agree in every cache state the
  claim names. The read-only guarantee was observed directly: the operator cache mtime `1793069967` did not move during the re-check.

**C2 — coverage (sourced): `corpus/knowledge/xkb-keymap-compile-r48.md`.** Re-measured plainly, plus evidence-verified counter.
- Presence: absent at 579f694b, present at b361c846. `git ls-tree --name-only <rev> corpus/knowledge/ | wc -l` → 64 → 65. The entry
  opens with `source:` (S340-S351), `verified-at: 2026-10-26` and `recheck:` (seat).
- Ground at base: `git show 579f694b:corpus/knowledge/hyprland-input-devices-r46.md | sed -n 69p` → "- The XKB compile itself is not
  reproduced…". Base `corpus/README.md:112` reads "Still open: the XKB compile itself". The tip adds the round-48 Frontier bullet at
  `:112`, which answers that sentence rather than restating it (seat).
- Rows: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 276 at base, 288 at tip (report: 276 → 288). The base→tip
  SOURCES diff has +12 lines and 0 removed. All 12 rows have 11 cells, tier A, `mined`, used-by the entry. Held S318/S319 are untouched.
- Pins: all 12 upstream files were re-fetched (libxkbcommon `xkbcommon-1.13.2` raw; xkeyboard-config 2.48 through the GitLab files API,
  because the `-/raw/` URL now returns an anti-bot HTML page). Each sha256 equals its `fetch/` pin and the digest in its row (seat; I
  re-did rules.c `04dfd934…`, messages-codes.h `4e721d31…`, symbols/br `8cf65550…` myself). Host `symbols/br` and `rules/evdev` are
  byte-equal to the pins. Seat checked 21 of the entry's locators verbatim against the fresh bytes.
- Live probes (`env -i PATH=/usr/bin xkbcli compile-keymap`; `pacman -Q` libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1):
  - `--layout br --options compose:caps` → rc 0, keymap digest `efd487a39920…`, 73079 B (= entry/receipt);
  - unknown layout → rc 1 (XKB-338/661);
  - unknown variant → rc 1 (XKB-661);
  - unknown option → rc 0 + `[XKB-595] Unrecognized RMLVO option … was ignored`;
  - unknown model → rc 0, silent, `pc(pc104)`;
  - unknown rules → rc 1.
  All six match the entry's failure table (seat).
- Counter (evidence-verified): `a4/c2v2-before-base.txt` `admitted=0/1 verdict=TARGET_MISSED rev=579f694b… exit=1`.
  `c2-after-data.txt` (e5d0130d), `c2-tip.txt` (f029de3a) and `c2-tip-final.txt` (627914f6) all read `admitted=1/1 TARGET_MET exit=0`.
  v1 beside it is MET. Matrix `v2/c2v2-revc2counter-matrix.txt`: 11 MET + 84 MISSED shown. The named flips `c-pin-mode-S340` and
  `x-quote-600-invisible` read rc 1 `TARGET_MISSED`, as `registration-v2.md:85-86` states (seat).
- Ruling: **verified**. No sampled sentence is false. The Limits keep the compositor half on held S318/S319 and mark the
  rules.in→evdev generation `[UNK]`.

Re-measured vs evidence-verified: tool sha, selftest, live resolver AGREE in four states, HOME-unset parity, fixture census, entry
presence, base ground, rows, pins, locators, `xkbcli` probes, census and the plain count re-derivations were re-measured by me or my
seats. The PRED-C1-r48-v2/PRED-C2-r48-v2 verdicts, controls, do-nothing controls, axis check, round-47 harm-watch counters and the
session-material gate were verified from committed receipts.

Harm watch: `git diff 579f694b b361c846 -- SCORECARD.md LOG.md` is a pure append (SCORECARD +31, LOG +10, 0 deleted). The whole round
deletes 67 lines, all in three files:
- `SKILL.md` (1): the `mado-session-material` registry row, replaced by a superset row (verdict 2 widened, waivers added);
- `quality/check-session-material.py` (31): the gate v2 rewrite, R3;
- `tools/mado-terminal.py` (35): the D1 rewrite, where the old `raise OutOfContract("HOME unset")` became the pin-modelled path.

No held claim was removed or weakened (seat). Corpus files are append-only: SOURCES +12/0, `hyprland-monitor-rule-r45.md` +51/0,
`xdg-terminal-selection-r47.md` +27/0, `round-47.md` +109/0. Axis receipts (evidence-verified):
- `axis-tip.txt` (f029de3a), `a4/axis-at-scorecard.txt` (d8e3d600) and `axis-tip-final.txt` (627914f6) all read `checked=3 mismatched=0`,
  navigation 65/65, calibration 86/86, operability 12/12.
- Round-47 frozen counters at d8e3d600: `PRED-C2-r47 admitted=1/1 MET`. `PRED-C1-r47` is MET on 3 of 4 runs. The fourth run's only
  clause-r trip is a lone `???( <detached ...>` strace line (`a4/c1-r47-at-tip.txt:196`). That is bwrap attach noise, and the bytes
  support it (seat).
- Frozen `PRED-C2-r45-v2` still `admitted=1/1` (`a4r1/MadoA4CritSalvage.md:9`).

QUALITY criteria 95 → 99 (+96..99), lessons 70 → 71 (seat). No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1: base tool `warm=149/228 TARGET_MISSED` → `228/228 TARGET_MET` (receipts); selftest 70/70 from committed bytes; live AGREE against the real resolver in absent/hit/stale/invalid states; HOME-unset parity rc 1/empty; capability row with live capture |
| coverage | improved | C2: entry 0 → 1; knowledge 64 → 65; rows 276 → 288; base open ground (`hyprland-input-devices-r46.md:69`, `README.md:112`) answered; pins byte-equal on re-fetch; six live `xkbcli` probes agree; PRED-C2-r48-v2 MET (receipts) |
| depth | unchanged | SKILL.md gains "XKB keymap compile (round 48)" and "Terminal cache (round 48)" (`SKILL.md:2226`, `:2294`, 25 table rows in that span); not a declared claim; no held table re-graded |
| freshness | unchanged | new rows pinned and re-fetched byte-equal today; no held SKILL claim re-verified as stale and fixed in place |
| calibration | unchanged | axis stays at its max (86/86, `checked=3 mismatched=0`); the lane self-corrected M48-11 (222→228, false "L0 question filed") and M48-12 instead of reporting them green; one report count does not reproduce (N1) |
| adjacency | unchanged | `w1/ConnSiblings.md`: no sibling claims the resolver cache or the XKB compile; held Hyprland rows S318/S319 cited, not re-claimed |

## 4. Discernment spot-check (`corpus/lessons/round-48.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `S340 admit` (tier A, code) | admit | `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/rules.c` re-fetched: sha256 `04dfd93468369de2…` = `fetch/xkbcommon-rules.c`, 2125 lines; `:1259` reads `/* No index provided: match only if single layout */` | **agree** | Tagged primary source of the exact library on the host (1.13.2-1). It is the right authority for how layout/variant names are consumed. The quote is verbatim at the stated line and ≤25 words. |
| `S347 admit` (tier A, code) | admit | `https://gitlab.freedesktop.org/api/v4/projects/xkeyboard-config%2Fxkeyboard-config/repository/files/symbols%2Fbr/raw?ref=xkeyboard-config-2.48` (the row's `-/raw/` URL now serves an anti-bot page): sha256 `8cf65550e08b5984…`, 19592 B, 368 lines = row; `:47` `xkb_symbols "nodeadkeys" {`; `grep -c 'xkb_symbols "'` → 11; `cmp` with `/usr/share/xkeyboard-config-2/symbols/br` → equal | **agree** | The row's `teaches` ("br has eleven") reproduces exactly. Tag bytes equal host bytes, so the variant-name rule is grounded for this host. |
| `S349 admit` (tier A, code) | admit | `…/xkbcommon-1.13.2/src/messages-codes.h` re-fetched: sha256 `4e721d31ebd9b897…` = pin, 9554 B/214 lines = row; `:150` `XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,`, `:116` `= 338`, `:162` `= 661` | **agree** | The registry is the authority for the XKB-NNN ids, and the seat's live probes emit exactly 338/595/661. The row's "ids, not severities" scoping is correct: 595 prints under `ERROR:` while the compile still succeeds. |
| REJECT ArchWiki `Xorg/Keyboard_configuration` | reject | page re-fetched (HTTP 200, title "Xorg/Keyboard configuration - ArchWiki"): `setxkbmap` ×21, `xkbcommon` ×0, `xkbcli` ×0, `1.13.2` ×0, no include-path or XKB-595 text | **agree** | The page covers Xorg/setxkbmap configuration and pins no library behaviour. It cannot ground host libxkbcommon 1.13.2 compile semantics that the tag sources already state. |
| REJECT `https://xkbcommon.org/doc/current/index.html` | reject | re-fetched (HTTP 200): a Doxygen index ("libxkbcommon 1.13.2", "Generated by 1.17.0"), only navigation links; `include path` ×0, `595` ×0, `XKB_DEFAULT` ×0 | **agree** | The `current` URL moves with every release, and this index states none of the behaviour the entry claims. The rejection reason ("not version-pinned and does not itself state the RMLVO/include/error behavior") holds. |
| REJECT Hyprland `efb50993…/src/devices/IKeyboard.cpp` | reject | `git show b361c846:corpus/SOURCES.md` row S319: same URL, same commit | **agree** | A new row would duplicate held S319 with no new scope; citing the held row is the right decision. |

SOURCES row re-opened for its quote: S349. The gate quote `XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,` (5 tokens, ≤25 words) is at `:150`
of the re-fetched file. S347's quote `xkb_symbols "nodeadkeys" {` is at `:47`. Census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` gives the following, exit 0:
- `W04` ×17: S030, S042, S045, S097, S119, S120, S121, S303, S307, S317, S318, S320, S321, S324, S326, S327, S332;
- `W01` S277;
- `mado ok`.

This equals `receipts/census-after.txt` and the report's "W04 ×17, W01 ×1". No new row repeats a held URL.

## 5. Trend verdicts

- **expansion: improved.** One knowledge entry lands on ground held open at base (`hyprland-input-devices-r46.md:69`, `README.md:112`),
  and knowledge goes 64 → 65. Rows go 276 → 288; all 12 are opened, mined, and byte-equal to upstream today. One capability row
  (warm-cache terminal selection) was shown running by my seat's live AGREE from committed bytes.
- **quality: improved.** The C1 deliverable is judged against the real pinned resolver on 228 warm fixtures, and my seat reproduced
  agreement in four cache states plus HOME-unset parity. Every round-47 routed item is closed with committed evidence (seat):
  - D1: HOME unset modelled;
  - D2: findings receipted;
  - D3: ten READDIR fixtures;
  - D4: erratum appended at `xdg-terminal-selection-r47.md:98`;
  - R3: gate v2, selftest 69/69;
  - R4b: round-45 errata append-only, frozen verdict kept.

  QUALITY gains 96-99, each with an instrument.

  Limits:
  - the session-material gate is red at the tip (`findings=159` at d8e3d600, `a4/session-material-tip.txt`), up from 128;
  - its coverage gap M48-8 is routed, not fixed;
  - a w2 mutant overwrote the operator's resolver cache during the round (M48-10, N2);
  - the clause-r mutant attack and the gate both-ways demonstration did not run (M48-13).

  None of these is an axis harm. Each is named in a committed lesson.
- **discernment: improved.** All 6 sampled gate decisions (3 admits, 3 rejects) agree on outside re-reading. The lane repaired its v1
  counters before data after w2 broke their own control rule (M48-9), and it disclosed that v2 is not blind to w2.
  Attempt 4 caught two transcribed facts (M48-11) and a flaky harm-watch read (M48-12) instead of passing them.
  Against it: one report count does not reproduce (N1). The live receipt's `host_cache_untouched` field records the overwritten
  operator cache without saying so (N2).

Closure: status `ok`, **admitted=true**, verdict `admitted`. Both claims verify, and no axis is harmed.

## 6. Routed defects (lane fixes next round)

1. **N1** (report `.ufo/reports/round-48/mado.md:37`): "the 52 untracked `*.synthetic` files" does not reproduce.
   `git -C mado-shokunin status --porcelain -uall | wc -l` → 47 (45 under round-45/w1, 2 under round-46/w1), all synthetic. The
   "nothing else untracked" part holds. Fix: correct the number in the next report and cite the counting command.
2. **N2** (`.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4`): `host_cache_untouched_sha256=c8b104e695a9cfcc…` equals
   `printf 'r48-w2\n' | sha256sum`. So at the 23:20:44 capture the operator's `~/.cache/xdg-terminal-exec` still held the w2 M-WRITE
   mutant's 7 bytes (M48-10), and the field name "untouched" reads as clean. Today the file is 190 B, sha `ddd94f6b…`, mtime 1793069967
   (the 23:59:27 resolver rewrite). Fix: append a lesson line naming what the digest is. In the round-49 M48-10 work, record a
   before/after digest pair labelled as operator-owned state.
3. **N3** (`corpus/lessons/round-48.md:425`): the spot-check shape asks for "the five gate decisions above (three admits, two
   rejects)". The `## Gate` holds 12 admits and 3 rejects. Fix: stale template text; append a correction line.
4. **N4** (`receipts/v2/c2v2-revc2counter-matrix.txt`): the text matrix shows 96 of the 98 variants. `a-entry-at-base` and
   `a-rev-base-direct` appear only in `summary.json` (seat). Fix: emit every variant row in the text receipt.
5. **N5** (`corpus/SOURCES.md` S346/S347): the anchored `gitlab.freedesktop.org/…/-/raw/…` URLs now return an anti-bot HTML page to
   non-browser fetchers; the GitLab files API (`/api/v4/projects/<id>/repository/files/<path>/raw?ref=<tag>`) returns the pinned
   bytes. Fix: note the API fallback for the next freshness re-fetch (append-only; no row edit).
6. Carried, as the report and lesson say:
   - M48-8: the session-material gate's 16-shape gap and `.ufo/` scope; the gate is red, `findings=159`;
   - M48-10: mutants must write only inside the sandbox;
   - `w2/SentScratch`: counters must refuse a `/tmp` `--work`;
   - M48-13: the residual dispatch cap vs clone recipe, so the clause-r mutant attack and the gate both-ways demo are still owed;
   - the `registration-v2.md` residuals: receipt generator path and the uncited meson pin.

SHONEN boxes remain `[~]` (the closure writes no `[x]`). For the operator: box 2 (end-to-end task) is reproducible by a non-author —
my seats reproduced the live warm-cache AGREE and the `xkbcli` receipt's rc/digest from committed bytes. Box 3 also held for my seat:
the tool's docstring usage (`--selftest`, `print`, `explain --observed`) ran as written without oral context. Box 1 (`SKILL.md:2226`,
`:2294`, real tables with cited rows) is checkable. Box 4 was not independently swept this pass. Promotion review is operator-owned.
Operator note: M48-10 overwrote an operator-owned file (`~/.cache/xdg-terminal-exec`) during w2. The resolver regenerated it at
23:59:27, and no decision is open, but the host-write class should stay on the lane's routed queue until M48-10's sandbox fix lands.
