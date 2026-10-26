# Round 47 SCORECARD section + LOG entry — draft (seat ScrScorecard, wave w1)

Status: DRAFT for the L1. Nothing here is measured; every literal below is either (a) verified at base this seat
(section D says how) or (b) a `<FREEZE>` / `<AFTER>` placeholder. The L1 integrates after the freeze and the data
commit; do not paste a placeholder into a published record.

Placeholder legend (the only two tokens used):

- `<FREEZE>` — a value the L1 fixes in `.ufo/waves/round-47/registration.md` after w1 returns: freeze commit, fixture
  count, generated-case count, control count, seat count and spec of w2, counter versions, predicate ids, pins.
- `<AFTER>` — a value produced only by running something after that freeze: base receipts, the data commit, counter
  stdout, census, gate exit codes, closure receipts, axis values.

Instrument paths (`quality/counters/c1-r47-terminal.py`, `quality/counters/c2-r47-terminal-entry.py`) follow the lane's
naming convention (a `-v2`/`-v3` suffix appears only when the freeze is superseded); the L1 confirms them with the
freeze. Receipt paths follow the round-45/46 names (`axis-base.txt`, `c1-before-base.txt`, `c1-after-data.txt`,
`c2-before-base.txt`, `c2-after-data.txt`, `ctl-c1.txt`, `ctl-c2.txt`, `axis-data.txt`).

---

## A. SCORECARD.md — Round 47 section (paste-ready)

## Round 47 - mado-terminal and the terminal-selection entry (2026-10-26, attempt 1)

Registration `.ufo/waves/round-47/registration.md` (freeze `<FREEZE>`, base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`),
frozen after wave `w1` (41 build seats, spec `c24adef2`) and before wave `w2` (falsification) and any data commit — the
lane's usual order inverted: the instruments freeze on the build wave's output, then `w2` attacks them; `<FREEZE>` for a
superseding registration if `w2` meets the frozen instruments. Data commit `<AFTER>`. Lowest-axis rule: every published
axis tied at its maximum at base (`receipts/axis-base.txt`).

| Claim / axis | Before -> after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **operability** (capability acquisition) - `tools/mado-terminal.py` | `fixtures=0/<FREEZE> generated=0/<FREEZE> selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` exit 1 at base (`receipts/c1-before-base.txt`) -> `fixtures=<AFTER> generated=<AFTER> selftest=ok readonly=ok tripwire=<AFTER> tool=present verdict=<AFTER>` exit `<AFTER>` at `<AFTER>` (`receipts/c1-after-data.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r47-terminal.py --repo . --rev <rev> --work <scratch>` (`PRED-C1-r47`; controls `receipts/ctl-c1.txt` PASS 0 of `<FREEZE>`) | **<AFTER>** |
| C2 **coverage** (sourced) - `corpus/knowledge/xdg-terminal-selection-r47.md` | `admitted=0/1` exit 1 at base (`receipts/c2-before-base.txt`) -> `admitted=<AFTER> verdict=<AFTER>` exit `<AFTER>` at `<AFTER>` (`receipts/c2-after-data.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r47-terminal-entry.py --repo . --rev <rev>` (`PRED-C2-r47`; controls `receipts/ctl-c2.txt` PASS wrong 0 of `<FREEZE>`) | **<AFTER>** |

Separable: `w1/ConnClaims.md` (tool-only tree: C1 `<AFTER>`, C2 `0/1`; data-only tree: C1 `MISSED`, C2 `<AFTER>`).

### Capabilities (round 47)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| terminal-route selection versus the resolver | answer "which terminal does SUPER+RETURN launch, and why" by re-implementing the xdg-terminal-exec v0.14.3 selection in Python 3 stdlib with **no process started and no socket opened**: the `$XDG_CURRENT_DESKTOP`-prefixed list then the unprefixed list, desktop-file IDs resolved across `$XDG_DATA_HOME` then each `$XDG_DATA_DIRS` element with the user's override first, per-entry validation (`Type=Application`, `Hidden`, `TerminalEmulator`, `TryExec`/`Exec` on `PATH`, show-in rules), actions, exec-arg composition (`--dir`, `--title`, `--app-id`, `--hold`, trailing command args) and the four `--print-*` modes against a cold cache; `explain` prints every candidate with its rejection reason and, with `--observed`, `MADO_TERM: selected= path= verdict=OK\|AGREE\|DIFFER\|NO_TERMINAL` (exit 0 OK/AGREE, 1 DIFFER, 3 NO_TERMINAL, 2 usage); judged against the pinned host script (`/usr/bin/xdg-terminal-exec`, sha256 `89f2be9a…`, byte-equal to upstream tag v0.14.3) as oracle, with a `strace -f` execve count of 0 and a socket tripwire | `tools/mado-terminal.py` (selftest `<AFTER>`/`<AFTER>`); `quality/counters/c1-r47-terminal.py` `<AFTER>` pinned + `<AFTER>` nonce cases at `<AFTER>`; tripwire `<AFTER>`; live host run `receipts/live-terminal-host-r47.txt` (`selected=<AFTER>`, override `path=<AFTER>`, `cmd=<AFTER>`, verdict `<AFTER>`, exit `<AFTER>`) | 47 |

### Sources, saturation, planned

Sources 262 -> `<AFTER>` rows (S326-S`<AFTER>`, tier A, `mined`, opened 2026-10-26; `<AFTER>` repeat held URLs under new
scopes: census W04). Knowledge entries 63 -> 64. Assimilation: `<FREEZE>` (no `merge/mado/` theme sits on this plane
unless the w1 connector opens one). considerthese `2026-10-26.md` proposal `<FREEZE>` -> `<AFTER>`. Mistakes
M47-1..`<AFTER>`; QUALITY 91-`<AFTER>`. Routed round-46 closure: R1 erratum for
`corpus/knowledge/hyprland-input-devices-r46.md:57` `<AFTER>`; R2 digest of the untracked 3.3 MB
`ExecStofOracle/receipts/out.json.rows.tsv` `<AFTER>`; R3 synthetic-fixture marker for
`quality/check-session-material.py`, shown able to fail both ways `<AFTER>`; R4 S290-S297 supersession and the round-45
(F1-F4) and round-44 `w2/ConnCalibration` errata `<AFTER>`. Saturation 9.0 / N=3 `<AFTER>`; retired: `<AFTER>`.

Axis table re-derived at `<AFTER>` (`receipts/axis-data.txt`): navigation `<AFTER>`/`<AFTER>`; calibration
resolved-active `<AFTER>`/`<AFTER>`; operability selftest `<AFTER>`/`<AFTER>`.

### Planned (round 48; intent only)

1. The warm cache: `XDG_CACHE_HOME` cache read/write and its invalidation are out of the round-47 contract by design (the
   tool models a cold cache); a round-48 claim would model the cache file and prove cold and warm modes agree with the
   pinned script.
2. The hotkey's other half: `uwsm-app --` in `~/.config/hypr/bindings.conf:2` (systemd unit naming, activation
   environment) sits outside the resolver contract, which stops at the exec-arg vector; the round-17 route asked what
   launches, not what the launcher does next.
3. The selected terminal's own config plane (`~/.config/alacritty/alacritty.toml`, and the same join for kitty, foot and
   ghostty) — new ground beyond the held `terminals-and-omarchy.md`; `terminal-route-r17.md` (documentary route, rows
   S056-S060) and `terminal-trees-r23.md` are held ground and are not re-claimed.
4. Routed items left open by this round: `<AFTER>`, with their age from the round-46 ledger (`w1/ScrRoutedAges/ages.md`,
   15 open, oldest 8 rounds at R38-3) — R1-R4 close only against their receipts, and M46-16 closes only if the
   S290-S297 supersession lands.
5. The `w2` falsification findings of this round: `<AFTER>` (contract defects and their closures; a v2 re-registration
   if `w2` meets the frozen instruments).

## B. LOG.md — Round 47 entry (skeleton, bullets replaced in place)

## Round 47 (2026-10-26, hyaku run 9, attempt 1)

- Protocol load; claims declared in `.ufo/waves/round-47/claims.md` (intent only: predicates freeze after `w1`); census
  before `receipts/census-before.txt` exit 0 (15 finding rows: 14 W04 duplicate-url rows and 1 W01 row); base
  `60edb66e`.
- Wave `w1` (BUILD, 41 seats, policy v1, spec `c24adef2`; executor 16, scribe 10, scout 5, critic 4, connector 2,
  sentinel 2, reviewer 1, revenger 1; `<AFTER>` reports, `<AFTER>` dead): `<AFTER>` (which rebuilds met the draft
  contract, which cheats/delegators met it, which contract forms the critics falsified, which forgeries met C2, and the
  R1-R4 closure receipts run inside this wave).
- Freeze `<FREEZE>` after `w1` and before any data: `PRED-C1-r47` (frozen fixture schema — env/files/exec/args/expect,
  `expect` always produced by the pinned script —, `<FREEZE>` pinned fixtures, `<FREEZE>` nonce-generated cases,
  bubblewrap isolation, `strace -f` execve and socket tripwires, `<FREEZE>` hermetic selftests under `$TMPDIR`);
  `PRED-C2-r47` (rows S326.., the round-17 `[UNK]` closure clause, `<FREEZE>` surfaces); controls `receipts/ctl-c1.txt`
  `<FREEZE>`, `receipts/ctl-c2.txt` `<FREEZE>`.
- Wave `w2` (falsify, `<FREEZE>` seats, spec `<FREEZE>`): `<AFTER>`.
- Data `<AFTER>`: tool `tools/mado-terminal.py`, entry `corpus/knowledge/xdg-terminal-selection-r47.md`, rows
  S326-S`<AFTER>`, lesson, README row + Frontier, SKILL/PROVINCE rows, QUALITY 91-`<AFTER>`, live receipt. Measured: C1
  `fixtures=<AFTER> generated=<AFTER> ... <AFTER>`, C2 `admitted=<AFTER> <AFTER>`; census `<AFTER>`; session-material
  gate `<AFTER>`.
- Routed round-46 closure: R1 erratum `<AFTER>`, R2 digest `<AFTER>`, R3 marker `<AFTER>` (shown failing both ways),
  R4 S290-S297 supersession plus the round-45 F1-F4 and round-44 `w2/ConnCalibration` errata `<AFTER>`.
- Freshness: host script re-hashed `89f2be9a…` = the claim's pin at base; upstream tag v0.14.3 and upstream main
  `<AFTER>` (a moved upstream or a new tag is a new row, not a re-point).
- Not run: `<AFTER>`.

---

## C. What each placeholder stands for, and who fills it

| Token in A/B | Stands for | Filled by | Receipt it must point at |
|---|---|---|---|
| `<FREEZE>` in the registration line | freeze commit of `registration.md` | L1, after w1 | `git rev-parse` of the freeze commit |
| `<FREEZE>` in C1 before/after ids | pinned fixture count, nonce-case count, control count, tripwire counts, selftest count | L1, after w1 | `registration.md` §C1 |
| `<FREEZE>` in C2 row | control count and surface count | L1, after w1 | `registration.md` §C2 |
| `<FREEZE>` in w2 bullets | w2 seat count and spec commit | L1, after the freeze | `w2-dispatch.json`, spec commit |
| `<AFTER>` in every counter cell | counter stdout at base and at the data commit | L1, at data | `receipts/c1-before-base.txt`, `c1-after-data.txt`, `c2-before-base.txt`, `c2-after-data.txt` |
| `<AFTER>` in `tools/mado-terminal.py` evidence | selftest line, counter run, tripwire, live host run | L1, at data | seat receipts under `.ufo/waves/round-47/w1/` + `receipts/live-terminal-host-r47.txt` |
| `<AFTER>` in the sources paragraph | row count and last S number, repeat-URL count, knowledge-entry count, considerthese proposal, Mistakes range, QUALITY range, saturation, retirement | L1, at data | `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-47.md` |
| `<AFTER>` in the axis line | the three axis pairs at the data commit | L1, at data | `receipts/axis-data.txt` |
| `<AFTER>` in R1-R4 | each closure's own receipt or its carried-open age | L1, at data | the receipts named in `corpus/lessons/round-46-verifier-spotcheck.md` §6 |
| `<AFTER>` in `Planned` 4-5 | open items and w2 findings | L1, at data | `w2/` seat reports + the round-47 lesson |

## D. Grounding for every non-placeholder literal in A/B (computed this seat, base `60edb66e`)

| Literal | Command (cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`) | Output |
|---|---|---|
| base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` is a commit and the lane tip at round start | `git cat-file -t 60edb66e2f1cb90acc6e9442fc93ded0ca42d750`; `git log --oneline -2` | `commit`; `60edb66e round-46 verifier spot-check …`, then `c24adef2 round-47: claims declared, w1 build spec and dispatch (41 seats, policy v1), census before` |
| spec `c24adef2` (the round's spec identity, as `e0be61e4` was in round 46) | `git log --format='%H %s' -1 c24adef2`; the round-46 precedent is that LOG's `spec e0be61e4` is the commit naming the spec and dispatch (`git log --oneline -1 e0be61e4f6e3…` -> `round-46: controls at freeze …, w1 spec and dispatch (66 seats, policy v2)`) | `c24adef2632672325a4eef3e3492f6716ccb6d14 round-47: claims declared, w1 build spec and dispatch (41 seats, policy v1), census before` |
| 41 build seats and the family counts | `python3 -c` over `.ufo/waves/round-47/w1-dispatch.json` `registry.members` (41 keys), counting seat-name prefixes | `Exec 16, Scr 10, Scout 5, Crit 4, Conn 2, Sent 2, Rev 1, Revenger 1` = 41; `counts.spawn=41` |
| census before exit 0, 15 finding rows = 14 W04 + 1 W01 | `awk -F'\t' '$1=="mado"{print $2}' .ufo/waves/round-47/receipts/census-before.txt \| sort \| uniq -c`; `tail -1` | `14 W04`, `1 W01`, `1 ok`; last line `exit=0` |
| host script sha256 `89f2be9a…` | `sha256sum /usr/bin/xdg-terminal-exec` | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac  /usr/bin/xdg-terminal-exec` (the claim's pin, byte-for-byte) |
| hotkey at `~/.config/hypr/bindings.conf:2` | `grep -n 'SUPER, RETURN' ~/.config/hypr/bindings.conf` | `2:bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"` |
| C1/C2 base cells `tool=absent`, `admitted=0/1` | `test -e tools/mado-terminal.py; echo "rc=$?"` and the same for `corpus/knowledge/xdg-terminal-selection-r47.md`; `grep -n xdg-terminal-exec tools/mado-tripwire.py` | `rc=1` for both paths (absent); the resolver's name appears once at `tools/mado-tripwire.py:272` as a watched **process** name (`"pidof", "xdg-terminal-exec", "wpctl", "brightnessctl",`), not as a selection model — no lane tool resolves the route at base |
| Sources 262 -> …; registry top S325 | `grep -cE '^\| S[0-9]+ ' corpus/SOURCES.md`; `grep -oE '^\| S[0-9]+ ' corpus/SOURCES.md \| grep -oE 'S[0-9]+' \| sort -V \| tail -1` | `262`; `S325` (so S326 is the next row) |
| Knowledge entries 63 -> 64 | `ls corpus/knowledge/*.md \| wc -l` | `63` |
| QUALITY 91-… | `grep -nE '^90\. ' corpus/QUALITY.md`; `tail -c 200 corpus/QUALITY.md` | `454:90. Every routed defect keeps one id …`, the last item in the file |
| round-46 ledger shape cited in `Planned` 4 | item 90 of `corpus/QUALITY.md` starts at `:454`; the figures are at `:457` | `42 rows, 15 open, oldest 8 rounds at R38-3` (`grep -nF`, receipt `w1/ScrScorecard/quote-check.txt`) |
| R1-R4 definitions cited in A | `corpus/lessons/round-46-verifier-spotcheck.md` §6 (read at `:105-` this seat) | R1 `:57` mis-attributed receipt; R2 3.3 MB tsv; R3 `findings=115`/18 seat files; R4 S290-S297 + F1-F4 + `ConnCalibration` |

## E. Conflicts and open questions this draft does not decide (for the L1)

1. The scorecard's historical rows carry a `tripwire=` token; rounds 45/46 did not. Round 47's contract names the
   tripwire as part of the judged surface, so A keeps the token and leaves its count to the freeze — drop it if the
   freeze reports the tripwire inside `readonly=ok`.
2. `Separable` names `w1/ConnClaims.md`; the round-45/46 precedent was a dedicated cross-claim seat (`ConnCrossClaim`).
   If `ConnClaims` does not emit the two-tree split, the line must be replaced or removed rather than implied.
3. `Planned` 1 (warm cache) is out of contract by design, not a defect; if the operator wants warm-cache agreement
   inside round 47, the C1 contract must say so before the freeze — after the freeze it is a round-48 claim.
4. `tools/mado-tripwire.py:272` already lists `xdg-terminal-exec` among the processes it watches. It models no
   selection, so C1's "surface moved: no lane tool resolves the terminal at base" survives, but the freeze should say
   which of the two tools owns the name if a future claim extends either — otherwise a w2 reviewer will read the list
   entry as a prior capability.
