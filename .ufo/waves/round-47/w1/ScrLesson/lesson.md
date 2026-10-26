# Round 47 lesson — the terminal selection chain (2026-10-26, hyaku run 9)

Lane mado-shokunin. Claims: C1 operability (capability acquisition) `tools/mado-terminal.py`, judged by `PRED-C1-r47-<AFTER>`;
C2 coverage (sourced) `corpus/knowledge/xdg-terminal-selection-r47.md`, judged by `PRED-C2-r47-<AFTER>`; registration
`.ufo/waves/round-47/registration.md` (freeze <AFTER>). Base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`. Round shape: two v1
waves — `w1` build (41 seats), then `w2` falsify against the frozen v1 instruments (`.ufo/waves/round-47/claims.md:3-7`); no seat
scores a frozen counter in w1.

**Draft status.** This file is the w1 skeleton, written by seat `ScrLesson` before the freeze and before any data commit. Every
`<AFTER>` marker below is a value that cannot exist yet: freeze commit ids, predicate names, counter and fixture paths, control
counts, row ids and quotes (which come from `w1/ScrRows`), census-after, and every mistakes row (from `w1/ScrMistakes`). Nothing
in this draft is evidence for a claim; the L1 integrates the frozen values around this prose. Gate rows, GATE lines and registry
counts are written by the seats named beside them and verified by the L1, not by this seat.

## Gate

Candidates considered: the pinned resolver script at tag `v0.14.3`
(`https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec`, byte-equal to the host
`/usr/bin/xdg-terminal-exec`, sha256 `89f2be9a…27ac`, pinned at `w1/ScoutScriptMap/upstream-xdg-terminal-exec` with
`w1/ScoutScriptMap/sha256.txt`); its README, man page, `Makefile` and test suite at the same tag
(`w1/ScoutSpecs/pins/xdgte-*`); the three spec texts the resolver implements (Desktop Entry 1.5, XDG Base Directory 0.8,
Menu 1.1 — `w1/ScoutSpecs/pins/html-*`, `xdgspecs-spec-revs.toml`); the omarchy v3.8.4 list and desktop file
(`w1/ScoutOmarchy/`); and the host's own declaration files, read as bytes. Screening and the admitted/rejected split are
`w1/ScoutSpecs` + `w1/ScoutHeld` + `w1/ScrRows` output; this draft fixes only the shape and the rules.

Admitted: new rows `S326`-<AFTER>, tier <AFTER>, status `mined`, opened 2026-10-26, used-by
`corpus/knowledge/xdg-terminal-selection-r47.md`, continuing the registry after `S325` (262 rows at base). GATE lines are
emitted by `w1/ScrRows/gate-lines.md` in the round-46 shape — receipt path, sha256, and a ≤25-word quote located by a computed
line number — and pasted here by the L1:

```
<AFTER>: one GATE line per admitted row, in S-number order, from w1/ScrRows/gate-lines.md
```

Quote discipline for this round: each quote is ≤25 words, word-bounded, and unique in its receipt; where the counter's rule is
whitespace-collapsed matching, the lesson states the collapsing exactly as round 46 did (`corpus/lessons/round-46.md:8-10`).
<AFTER>: the list of rows whose quote spans or de-spaces source lines, with the start line.

Held ground, deliberately not re-claimed (named here so a later reader can see the overlap is a decision, not an omission):

- `corpus/knowledge/terminal-route-r17.md` — the documentary route, on rows `S056`-`S060` (`corpus/SOURCES.md:68-72`) plus
  rejected `S061`-`S062` (`terminal-route-r17.md:152`). Its subject is the declaration plane (which file says which terminal, the
  option and lookup code at `xdg-terminal-exec:106,148-162`); this round's subject is the executed *selection* chain — list order,
  desktop-file ID resolution across data dirs, entry validation, actions, exec-arg composition, print modes. The new rows are new
  scopes on repeated URLs (census W04, not an error), and the round-17 `[UNK]` at `terminal-route-r17.md:144-145` is closed by
  observation, not by rewriting the entry.
- `corpus/knowledge/terminal-trees-r23.md` (rows `S123`-`S152`) — foot/kitty/ghostty config trees. No terminal is installed
  (`terminal-trees-r23.md` §); this round never opens those trees again.
- `corpus/knowledge/terminals-and-omarchy.md` (MADO-3 inventory, 2026-10-14) — the four config trees and their key settings. It is
  the host declaration surface; the resolver's behaviour is not its subject.
- `S071` (`corpus/SOURCES.md:83`) already holds the host user-local `Alacritty.desktop` bytes — the entry the resolver selects — so
  the C2 entry cites that row instead of opening the same file again; a new row for the same path would be a duplicate with no new
  scope.

Rejected: <AFTER> — one `REJECT <source>` bullet per screened-and-refused candidate, each naming the decisive line and a flip
condition, from `w1/ScoutSpecs`/`w1/ScoutHeld`. The one rejection class this round must state explicitly, because it is the
round's whole premise: a row on the *host's* `/usr/bin/xdg-terminal-exec` as a separate source from the upstream tag would cite
the same bytes, so the host binary is a pin comparison (`sha256sum` equality), not its own row. <AFTER>: whether that is settled
by `S0NN`-style byte equality or by a host-file row.

## Registry changes

| surface | old (base `60edb66e`) | new |
|---|---|---|
| `corpus/SOURCES.md` | 262 rows, top `S325` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `262`) | 262 + <AFTER>; rows `S326`-<AFTER> appended after the last `S` row, 11 cells each, tier <AFTER>, `mined`, opened `2026-10-26`, used-by the entry |
| `corpus/README.md` | 63 knowledge-index rows | 64 (one three-cell row after the round-46 row at `:74`) |
| `corpus/knowledge/` | 63 files | 64 (`xdg-terminal-selection-r47.md`) |
| `corpus/lessons/` | 68 files | 69 (this lesson) |
| `tools/` | 14 files, `mado-devices.py` the newest | 15 (`mado-terminal.py`; C1's surface, no registry row) |
| held rows `S056`-`S060` | cells 1-10 unchanged | unchanged; only the census gains the W04 lines for the repeated URLs (<AFTER>: which rows) |
| `quality/check-session-material.py` + its marker registry (R3) | gate tracked, no synthetic marker, no registry file | <AFTER>: tracked gate + marker layer + registry path, plus the `SKILL.md` gate-registry row text |
| supersession rows (R4a) | none; `S290`-`S297` carried as-is across four rounds | <AFTER>: new rows `S346`+ with the `supersedes` opener, or in-place `status`/`recheck` changes per `CORPUS.md` rule 2 — id space above `S345` is reserved for the C2 rows, so the block must not take `S326`-`S345` |

### Census before → after

Before (`.ufo/waves/round-47/receipts/census-before.txt`, base `60edb66e`, exit 0) — 14 `W04` lines and 1 `W01` line:

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
mado	W04	S303 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp across scopes
mado	W04	S307 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
mado	W04	S317 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp across scopes
mado	W04	S318 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp across scopes
mado	W04	S320 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
mado	W04	S321 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp across scopes
mado	W04	S324 duplicate url raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

After (<AFTER>): the same command at the round tip must exit 0; the new W04 lines are the repeated URLs (`xdg-terminal-exec`
script and README, the host list files) and are listed here by row id; `W01` count is <AFTER>.

Command (both ends): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.

## Search log

Question: how does `xdg-terminal-exec` v0.14.3 turn `XDG_CURRENT_DESKTOP` plus a user list plus desktop files across data dirs
into the one command line that `--print-cmd` writes — which list file, which line, which entry, which rejection — and what must a
row cite to bind each step?

Where searched: the script at the tag (`w1/ScoutScriptMap/`), its README/man page/Makefile/test suite at the same tag
(`w1/ScoutSpecs/pins/`), the Desktop Entry 1.5, basedir 0.8 and menu 1.1 texts, the omarchy v3.8.4 list and desktop file
(`w1/ScoutOmarchy/`), the lane registry `corpus/SOURCES.md`, and the host read-only (the two list files, `~/.config/hypr/bindings.conf`
as bytes, and `xdg-terminal-exec --print-*` runs whose cache is redirected into scratch).

Identified: <AFTER> — the script's function/line map (`w1/ScoutScriptMap/`), the number of candidate sources opened, and the
candidate rejections.

Screened: <AFTER> — each candidate read at its decisive lines.

Included: <AFTER> — the admitted rows `S326`-<AFTER>, one per step the tool re-implements: list-file discovery and order,
per-desktop list prefixes, desktop-file ID lookup across data dirs, entry validation (`Type`, `Hidden`, `TerminalEmulator`,
`TryExec`/`Exec` on PATH, show-in rules), actions, exec-arg composition, print modes, and the cache file the print modes write.

Excluded: <AFTER> — with the decisive line for each, in the Gate's Rejected block.

Registry screen: the P4 terminal chain already holds `S056`/`S057` (README, script), `S058` (Alacritty manual), `S059`/`S060`
(host declarations and system list) and `S071` (host user-local `Alacritty.desktop` bytes), with `S061`/`S062` as rejected rows
(`corpus/SOURCES.md:68-72,70,73-74,83`), and the round-17 route paragraph names them as documentary only (`:306-310`). No row cites
a freedesktop specification text (`grep -c 'specifications.freedesktop.org\|spec.freedesktop.org' corpus/SOURCES.md` → `0`), so the
Desktop Entry / basedir / menu rows are first-use URLs and the repeats are the `xdg-terminal-exec` script and README plus the host
list files. <AFTER>: the exact held-row collision list for the new URLs.

Stop: every step the tool re-implements has a pinned line and every step is exercised by the oracle (the real script) under the
C1 counter; re-open the search when the host resolves a different terminal than the tool predicts, when `xdg-terminal-exec` leaves
0.14.3 (the packaging line is already `0.14.3-2`, `terminal-route-r17.md:135`), when the omarchy lists change, or when the
resolver's cache semantics matter to a claim (this round models a cold cache only).

## Mistakes

<AFTER>: `M47-1`..`M47-N`, drafted by `w1/ScrMistakes`, in the round-46 shape — class · evidence (a path:line, a command and its
output, or a hash) · captured-by (criterion number or `none`) · fix, where a fix counts only once shown able to fail. At least one
mined mistake is mandatory this round (frontier step §3, `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-47.md:42-75`); if the
sweep finds none, the sweep command and its output are pasted here instead.

Known-now candidates the round already exposes, for `ScrMistakes` to confirm or refute (not mistakes until a seat shows them):

- the round-46 lesson contradicts itself on R45-D4 (see the first conflict below);
- the inherited routed ledger counts R45-D4 open at round 46 while the digest is tracked at base (same conflict);
- an erratum that cites the wrong receipt is exactly M46-5's class, and R1 is that class recurring one round later — if R1 lands
  without a receipt-identity check, the recurrence is the mistake.

### Applications of existing criteria

<AFTER>: `M47-n` → criterion number(s) and the sentence saying why the criterion captures it. Two mappings are already forced by
this round's construction and are stated here so the L1 does not have to re-derive them:

- the routed-defect table below is criterion 90 in operation (`corpus/QUALITY.md:454-461`: one identity, an age, and a `landing`
  mistake at the third deferral — which is why R4a is mined as M46-16);
- R1 is criterion 24's class (`corpus/lessons/round-46.md`, M46-5: a run receipt names its producer) applied to the lane's own
  entry one round after it was mined.

### Conflicts recorded for the judge

1. **R45-D4, same lesson, two readings.** `corpus/lessons/round-46.md` D4 states the digest line "is committed beside
   `summary.txt`" while **M46-8 in the same file** states the 282 B digest is untracked. At base the question is settled by one
   command: `git ls-files .ufo/waves/round-45/w1/MutC1Counter/` lists `results.digest.txt` (five files, no `results.json`) — the
   digest is tracked, M46-8 described the state at its own draft time, and D4 is right at the landing revision. The ledger below
   therefore carries R45-D4 as closed in round 46. Reported as a conflict rather than silently resolved because two seats read the
   same file differently.

2. <AFTER>: any pair of w1 seats that measured the same thing with different numbers, verbatim, with the population each counted —
   the round-46 lesson's first conflict (`corpus/lessons/round-46.md`, §Conflicts 1) is the shape to follow.

## Round-46 closure items (`corpus/lessons/round-46-verifier-spotcheck.md` section 6)

R1-R4 are non-claim work; each has its own seat, receipt and acceptance below. Rulings are the closure's (`:107-118`); the
acceptance commands are drafted here so the next closure has a fixed target, and the L1 may tighten them.

| item | closure locator | what it is | seat (w1) | planned landing |
|---|---|---|---|---|
| R1 | `round-46-verifier-spotcheck.md:107` | erratum for `corpus/knowledge/hyprland-input-devices-r46.md:57` (the live join cites the L1 reference's receipt, not the landed tool's) | `ScrErrataR1` | an appended erratum block at the end of the entry — the entry body is not rewritten |
| R2 | `:111` | digest of the untracked 3.3 MB `.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv` | `ExecR2Digest` | a tracked digest line beside the seat's committed `out.json`, or a stated retention |
| R3 | `:113` | `mado-session-material` red at the round-46 data commit (`findings=115`, 18 in round-46 seat files); install the drafted synthetic marker + prose serial rule, shown able to fail both ways | `ExecSessionMarker` | tracked gate + marker registry + `SKILL.md` gate-registry row |
| R4a | `:116` | `S290`-`S297` supersession (open since round 43; M46-16, `corpus/lessons/round-46.md:307`), re-verified today | `ExecSupersede` | rows `S346`+ (or in-place status/recheck changes), census-clean on a mirror |
| R4b | `:116` | the round-45 entry's six non-supported sentence units (`CritW2Entry.md` F1 `:84b`, F2 `:96`, F3 `:98`, F4 `:18b`/`:106`/`:107`) | `ScrErrataR45` | one appended erratum per confirmed unit, `REFUTED` + reason for any unit that does not hold |
| R4c | `:116` | the round-44 `w2/ConnCalibration` mismatches (six findings, drafted as E1-E6 at `.ufo/waves/round-46/w1/ScrErrata/errata.md`) | `ScrErrataCal` | append-only `SCORECARD.md` erratum lines |

What the next closure needs to see for each (drafted acceptance — command and expected observation):

- **R1.** The entry's tail carries an erratum block that (a) quotes what `:57` says, (b) names
  `.ufo/waves/round-46/receipts/live-devices-host-r46.txt` as the corrected citation, (c) names the producer hash the receipt itself
  prints (`3a803689…` for the landed tool, against `b229efd0…` for the L1 reference), and (d) states the two-config ordering.
  Check: the entry diff is append-only (`git diff --numstat <base> <rev> -- corpus/knowledge/hyprland-input-devices-r46.md` shows
  the deletion count `0`), and every hash in the erratum is greppable in the receipt it names. Fails if the erratum cites
  `live-devices-host-l1.txt`.
- **R2.** A tracked path under `.ufo/waves/round-46/w1/ExecStofOracle/` holds the digest (sha256, bytes, lines, header, class
  counts) and matches `sha256sum` of the tsv as measured; `git status --porcelain` no longer lists the tsv, or the seat's report
  states its retention and why. Fails if the digest is itself untracked (M46-8's shape).
- **R3.** Five demonstrations, each with its receipt: (1) current gate exit 1 with its findings count; (2) gate + registry marking
  only the synthetic files → the residual list is exactly the real ones (the serial-bearing files routed to the operator);
  (3) a planted real dump in an unmarked file → exit 1; (4) a planted real dump inside a *marked* file → still exit 1 (the marker
  waives a file, never a shape); (5) a registry entry naming a file that carries a real serial → exit 1. Fails if the marker is a
  path-only waiver. The serial value itself is never printed.
- **R4a.** On a corpus mirror: census exits 0; the block deletes no row (`diff` append-only); each new row's `supersedes` opener
  names its predecessor; each predecessor's `teaches` defect is named with a computed locator. Fails if a row id lands inside
  `S326`-`S345` (the C2 range) or if the mirror census emits a new error class.
- **R4b.** Six units, six rulings, each with the pin line that settles it; a unit that does not hold is `REFUTED` with the reason
  rather than quietly dropped. Fails if the errata restate the closure's wording instead of re-deriving it.
- **R4c.** Six lines, one per finding, each naming what it attacks and the command that shows the truth; nothing above rewritten.
  Fails if an erratum edits an earlier `SCORECARD.md` line.

## Routed-defect ledger (criterion 90)

Ages are `47 − first_routed_round`, the convention of `.ufo/waves/round-46/w1/ScrRoutedAges/ages.md:14-18`. State is inherited from
that table (Table 2, `:76-93`) unless a command in this round's seats re-derives it; the three spot-checks below were re-run at base
and are marked so. Round-46 items enter at age 1.

| id | defect (short) | first routed | age at r47 | state at base / this round |
|---|---|---|---|---|
| R38-3 | 190,816 B `ss -xpa` table in the public tree, unmentioned in `LOG.md` | S38:86 | 9 | still open: `stat -c %s .ufo/waves/round-38/receipts/eventq-live-ss.txt` → `190816` (re-measured) |
| R38-4 | 10-id instrument-residual composite never reconciled | S38:87 | 9 | open; no lesson r39-r46 names the ids (inherited) |
| R40-2 | `fb49621` tip axis receipt never committed | S40:92 | 7 | open: `.ufo/waves/round-40/receipts/` holds one `axis` file, the base (re-measured) |
| R40-3 | fresh-nonce re-run of both v2 counters never committed | S40:93 | 7 | open (inherited) |
| R41-2 | C1/C2 predicate tightening | S41:78 | 6 | open; rebuilt for new counters only (inherited) |
| R41-3a | `S041` held-row citation | S41:79 | 6 | open, carried verbatim (inherited) |
| R41-3b | tool ergonomics O1-O5 | S41:79 | 6 | open (inherited) |
| R41-4 | `PROVINCE.md:75` → `75-76` in the lesson citation | S41:80 | 6 | open: `corpus/lessons/round-41.md:48` still writes `PROVINCE.md:75` (re-measured) |
| R43-D2 | `S290`-`S297` supersession / `S293` title | S43:100 | 4 | **routed again as R4a**; third deferral already mined as M46-16 |
| R44-D7 | `w2/ConnCalibration.md` content mismatches | S44:118 | 3 | **routed again as R4c** |
| R45-D2 | serial-copy undercount | S45:105 | 2 | count corrected (M46-10); removal from three held entries and 21 wave files is operator-owned |
| R45-D3 | gate has no `SKILL.md` row; findings untriaged | S45:110 | 2 | row landed in round 46 (closure §1, `SKILL.md:770`); the marker layer is **routed again as R3** |
| R45-D4 | `results.json` / digest commit | S45:114 | closed r46 | digest tracked: `git ls-files .ufo/waves/round-45/w1/MutC1Counter/` lists `results.digest.txt` (conflict 1) |
| R45-D5 | `output: null` seats are not evidence | S45:116 | closed r46 | stated in the round-46 lesson's D5 line |
| R46-R1..R4 | this section's closure items | S46:107,111,113,116 | 1 | open at the start of this round; each has a seat above |

<AFTER>: any row closed this round, with the command that closes it, and any new routed item this round creates (with its first
locator computed from the round-47 spot-check, not typed).

## considerthese

`considerthese/2026-10-26.md` — proposal 3 (track routed defects until they close) landed last round as QUALITY 90 and is the table
above. Proposal 2 (a running ledger of the lane's live-state tools) is drafted this round by `w1/ScrToolLedger` as a README section;
<AFTER>: admitted or refused, and the reason. Proposals 1, 4, 5 and 6 are screened by `w1/ScoutShokuknow`; <AFTER>: their
dispositions. No newer `considerthese/` file exists than `2026-10-26.md` (`ls considerthese/`).

## Assimilation

<AFTER>: `w1/ScoutShokuknow` screens the staged `merge/mado/` themes for terminals, xdg-terminal-exec, desktop entries and the
session-material gate; `w1/ExecIdGuard` runs the id-collision guard against `merge/mado/SOURCES.append.md` into
`.ufo/waves/round-47/assimilation/`. Expected outcome, stated so the section cannot be left blank: no staged theme touching the
selection chain is admitted unless it carries bytes the lane has not opened; the guard's verdict and the id collision count go
here.

## Frontier

The frontier step (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-47.md:42-75`) runs every round inside the 1-3 claim cap and
is not a fourth claim. Its four contract items plus the README bullet, as they stand:

1. **Registry curation** — `corpus/SOURCES.md` rows `S326`-<AFTER> added, held rows unchanged; the census before → after block above
   is the record. <AFTER>: the `status`/`recheck`/`used-by` changes logged old→new.
2. **Census** — before: 14 `W04` + 1 `W01` + `mado ok`, exit 0; after: <AFTER> (must exit 0).
3. **Mined mistake** — <AFTER> (see `## Mistakes`; mandatory).
4. **Sourced claim** — C2 rests on rows opened this round: the entry cites `S326`-<AFTER> for the selection chain, and the C1
   counter's oracle is the pinned script those rows hold.
5. **README frontier** — one new bullet inserted above the round-46 bullet in `corpus/README.md` `## Frontier` (`:107`, round-46
   bullet at `:109`), drafted here in the section's existing voice and left for the L1 to reconcile with what actually landed:

> - Round 47 moves the terminal *selection* chain onto sourced ground ([terminal selection](knowledge/xdg-terminal-selection-r47.md),
>   rows S326-<AFTER>): how `XDG_CURRENT_DESKTOP` plus the user and system lists plus desktop files across the data dirs become the
>   one command line `xdg-terminal-exec --print-cmd` writes — list order, entry validation, actions, exec-arg composition, print
>   modes, and the cache those print modes leave — with a read-only resolver (`tools/mado-terminal.py`) that re-implements the
>   selection and starts no process and opens no socket. Round-17 `[UNK]` closed: the resolver on this host selects the user-local
>   `Alacritty.desktop` under `~/.local/share/applications/` over the system entry, observed read-only. Still open: whether `uwsm-app`
>   in the SUPER+RETURN bind changes what the resolver sees, the `--dir=` value `omarchy-cmd-terminal-cwd` would produce at launch
>   (round-17 `[UNK]`, `terminal-route-r17.md:149-151`), any warm-cache path (the tool models a cold cache), the terminal binary's own
>   behaviour (no terminal was launched), and packaging drift past `0.14.3-2`.

Provenance of that bullet, so the L1 can check it before pasting: the hotkey is `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`
(`~/.config/hypr/bindings.conf:2`, held as bytes at `S059`); the host print-mode fact is the L1's 2026-10-26 observation; the
`[UNK]` locators are computed on `corpus/knowledge/terminal-route-r17.md`. <AFTER>: the "still open" list must be reduced to what the
round actually did not touch — delete any item this round closes, and never widen the bullet to a launch observation (no terminal was
started, by rule).
