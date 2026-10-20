# ReviewReadme — `corpus/README.md` at the round-18 integration

Seat: `MadoR18.ReviewReadme`, wave 2 (FALSIFY), 2026-10-20. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Read-only in the lane: no git/jj
write, no package/service/compositor/input/socket command, no network fetch,
no tool install (nothing installed or upgraded). The only lane byte written is
this report.

## Artifact under test

```
corpus/README.md                         blob c0fa8462… sha256 8cd18d32…d60d10
corpus/SOURCES.md                        blob 2b8dd7c0… sha256 9552071c…4f26de
corpus/QUALITY.md                        blob ac8f8805… sha256 82712444…8546ec
corpus/knowledge/walker-route-r18.md     blob c2056f3f… sha256 3ff430a4…8fbf20
corpus/knowledge/theme-route-r18.md      blob 49d2231f… sha256 b080bc47…a19f23
SCORECARD.md                             blob 28107ec6… sha256 7a4252c6…ca5117
```

README diff `d9a5a18 → 4c103b55` is `9 0` (numstat): exactly the two new index
rows (README:44-45) and the seven-line round-18 Frontier bullet (README:129-135).
No other README byte moved. Worktree `corpus/*` equals the rev
(`git diff --stat 4c103b55 -- corpus/README.md corpus/SOURCES.md corpus/QUALITY.md`
is empty).

## Commands run and exact output

### 1. SCORECARD fleet-round-1 navigation Counting command

Block extracted byte-exactly from `4c103b55:SCORECARD.md` (`### Counting command`,
fence body lines 70-89, sha256
`8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`; identical
at `d9a5a18`, so the instrument did not move) and run with `REV` exported:

```
$ REV=4c103b55b1ea5c3c555884afe3eb69b5189701b7 bash -s < counting-block
revision=4c103b55b1ea5c3c555884afe3eb69b5189701b7 indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
$ echo $?
0

$ REV=d9a5a18e17cd3a68b52148fcc01c4a30e340ba98 bash -s < counting-block
revision=d9a5a18e17cd3a68b52148fcc01c4a30e340ba98 indexed=32/32 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
$ echo $?
0
```

Expected 34/34 exit 0: **confirmed**. `34` = 34 `corpus/knowledge/*.md` at the
rev (`git ls-tree …:corpus/knowledge | wc -l` → 34); the two additions are the
only new notes (`git diff --name-status d9a5a18 4c103b55 -- corpus/knowledge`
→ `A theme-route-r18.md`, `A walker-route-r18.md`).

### 2. Source-id ranges: bidirectional check

```
$ grep -oE 'S0[0-9]{2}' walker-route-r18.md | sort | uniq -c
 1 S015
 1 S072 … 1 S091        (each of S072–S091 exactly once)
$ grep -oE 'S0[0-9]{2}' theme-route-r18.md | sort | uniq -c
 1 S092  1 S093  1 S094  1 S095
```

Both notes' own `source:` front-matter lines carry the same ids as the index
cells (walker line 1 = S072…S091, 20 ids; theme line 1 = S092…S095, 4 ids).
`S015` (mado drift protocol) appears once in the walker note at :234, only as
the protocol under which the moved pins are reported; it is a method row, not
evidence, and the note's own `source:` line excludes it — the same convention
as earlier index rows. No walker citation reaches S092-S095 and no theme
citation reaches S072-S091.

SOURCES at the rev has 95 rows (71 at `d9a5a18`; `grep -cE "^\| S0[0-9]{2} \|"`
→ 71 → 95, exactly 24 new, last id S095). Every row S072-S095 is
`kind ∈ {docs,code}`, `tier A`, `status mined`, and its `used-by` names the
matching note; no row in the range is unused and no id is skipped:

```
S072-S091 → corpus/knowledge/walker-route-r18.md   (20 rows)
S092-S095 → corpus/knowledge/theme-route-r18.md    ( 4 rows)
```

### 3. Fetch receipts (R17-V3 / M6)

`NoteWalker/receipts.jsonl` (27 lines) and `NoteTheme/receipts.jsonl`
(17 lines), identical at `4c103b55`, at `abfbf35` and in the worktree
(sha256 `a244ddc1…e7130a` / `ed9ce52f…74027c`). Every line was parsed:

* all nine `mado-fetch-receipt-v1` fields present on every line;
* every `body` exists in the seat directory, its **sha256 equals the receipt
  `sha256` and its byte count equals `bytes`** — 27/27 and 17/17 OK;
* statuses are what the notes say (three 404s: `swaybg/doc` tree and
  `doc/swaybg.1.scd`, and the `themes/matte-black/theme.name` probe), and the
  theme note discloses them as non-credited (theme route :130).

Every fetched row S072-S089 and S092-S094 has at least one receipt; the SOURCES
digests recorded in those rows are present in the receipts (checked every
64-hex token in S072-S095: all match a receipt sha except the three host-only
digests — `/usr/bin/walker 25240650…`, `theme.name 48749715…`,
`background target 55fa691a…` — which have no receipt by nature; S090 has no
digest at all).

### 4. Host rows (S090, S091, S095), re-hashed

```
$ sha256sum ~/.config/walker/config.toml            fecf71fa…d1787   (1,336 B)
$ sha256sum /etc/xdg/walker/config.toml             3c5c6867…50a8b   (13,743 B)
$ sha256sum /usr/bin/walker                         25240650…93096   (7,039,912 B)
$ sha256sum ~/.config/autostart/walker.desktop      5cb9874e…c3aa7
$ sha256sum ~/.config/systemd/user/app-walker@autostart.service.d/restart.conf
                                                    de0f7029…15433
$ sha256sum ~/.local/share/omarchy/bin/omarchy-{launch,restart,refresh}-walker
                                                    fd9e93f8… / 9ac82d0c… / 05cd9c67…
$ sha256sum ~/.local/share/omarchy/default/walker/themes/omarchy-default/style.css
                                                    481267af…500b0
$ sha256sum ~/.config/omarchy/current/theme.name    48749715…55c3b
$ sha256sum ~/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
                                                    55fa691a…39ac
$ readlink ~/.config/omarchy/current/background
/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
$ sed -n '1943p;2929p;3062p;3095p;3123p' /var/log/pacman.log
[2026-10-11T16:14:39-0300] … upgraded walker (2.16.2-1 -> 2.17.0-1)
[2026-10-20T09:16:46-0300] … upgraded walker (2.17.0-1 -> 2.17.2-1)
[2026-10-20T09:18:25-0300] … running 'walker-restart.hook'...
[2026-10-20T09:31:03-0300] … upgraded elephant (2.21.0-1 -> 2.22.1-1)
[2026-10-20T09:31:04-0300] … running 'walker-restart.hook'...
```

Every host digest in the two notes' tables and in S090/S091/S095 matches the
host bytes as of this review; the theme note's 24-file theme tree and 4
backgrounds also match (`find … -maxdepth 1 -type f | wc -l` → 24, 4).

### 5. Anchor spot-checks against the fetched bodies

Walker: `WS:212-219` (embedded default + `find_config_file("config.toml")`),
`WT:56-63` (`~`→`$HOME` literal replace), `WD:156-161` (socket path),
`EC:38-47` (elephant listen path + 0755), `OL:1-14` (elephant/stervice launch
+ `exec walker --width 644 …`), `XD:302/306/356-358` (XDG defaults and
"searches XDG_CONFIG_HOME and then XDG_CONFIG_DIRS") — all as cited. The tag
tarball's `Cargo.lock` pins `xdg 3.0.0`, `notify 8.2.0`.

Theme: `OT:17-19`, `OT:41-45`, `OT:48-50`, `OB:46,49-50`, `OS:21,24-25`,
`OA:5`, `OP:43`, `SW:19-31`, `SM:575-577` — all as cited.

### 6. Launch-declaration host bytes (see F1)

```
$ sed -n '2,3p' ~/.local/share/omarchy/default/hypr/bindings/utilities.conf
bindd = SUPER, SPACE, Launch apps, exec, omarchy-launch-walker
bindd = SUPER CTRL, E, Emoji picker, exec, omarchy-launch-walker -m symbols
$ sed -n '5p' …/bindings/clipboard.conf   → bindd = SUPER CTRL, V, … -m clipboard
$ cat -n …/apps/walker.conf               → :2 layerrule = no_anim on, match:namespace walker
$ sed -n '18p' …/apps.conf                → source = …/apps/walker.conf
$ sed -n '40p' ~/.config/hypr/bindings.conf
# bind = SUPER, PERIOD, exec, omarchy-launch-walker -m symbols # Emoji Button
```

The note's assertions are correct; the files are simply not under any SOURCES
row (see F1).

## Findings by severity

### F1 — medium-low: host bytes cited by the walker note have no SOURCES row

`walker-route-r18.md:248-256` (§ Launch declarations) asserts host content
from `~/.local/share/omarchy/default/hypr/bindings/utilities.conf:2-3`,
`…/bindings/clipboard.conf:5`, `…/apps/walker.conf:2`, `…/apps.conf:18` and
`~/.config/hypr/bindings.conf:40`. None of these files is in any SOURCES row:
the only rows touching that tree are S020 (`default/hypr/windows.conf` and
`apps/terminals.conf`) and S095 (`hyprland.conf`, `hyprlock.conf`), and a
grep of `SOURCES.md` for `utilities.conf|clipboard.conf|apps/walker.conf|apps.conf|bindings/`
returns only a prose line (SOURCES:204). The round-18 Gate itself admits
"host file bytes as host rows" (`lessons/round-18.md:31-32`), and the round
created host rows for the other host reads (S090, S091, S095).

Consequence: the walker index row's `source:` cell (README:44, "S072-S091")
does not cover the whole note; a closure that walks every claim back to a row
will find five host files with no row. The content is verified correct (above),
so this is provenance, not truth. Fix: a host row for these files (or name
them in the row's Sources cell and in the note's § Host declaration table).

### F2 — low: the Sources cells promise fetch receipts for host rows that cannot have one

README:44 and :45 end with "fetch receipts under `.ufo/waves/round-18/fetch/`".
That is true for the 21 web rows but S090 (`/var/log/pacman.log`), S091 (host
walker bytes) and S095 (host theme state) have no fetch receipt. SCORECARD:961-965
(C2) literally says "each new credited row backed by a committed raw fetch
receipt … so a closure can tell a fetched row from an invented one"; the lesson
is precise ("every round-18 credited **web** row", `lessons/round-18.md:21`).
A closure applying the C2 sentence to all 24 new rows will flag exactly three
rows that are legitimate host rows. The round-17 rows set the better precedent
— README:42 and :43 name host bytes by sha256 in the Sources cell. Fix: extend
the round-18 cells to "web rows by fetch receipt; S090/S091(/S095) host bytes
by sha256 in § Host declaration".

### F3 — low: S084 is inside the claimed range yet outside the round's own admission rule

S084 is `docs.rs/xdg/latest` — an HTML page at an unversioned URL — and it is
the row behind the note's XDG search-order sentence (`walker-route-r18.md:77-81`,
cites `XD:356-358`). The round-18 Gate rejected/left unrowed "HTML pages as
sole support" and "unversioned docs sites as version-specific support"
(`lessons/round-18.md:32-34`). Mitigations that keep the note honest: the saved
body is committed and hashes (`0291cfe6…`), the tag's own lock pins
`xdg 3.0.0` (verified in the S079 tarball), and the note already labels the
`/etc/xdg` fallback `[INF]` with an explicit UNK for unexercised search order
(`:290-292`). So this is an admission-policy inconsistency, not a false claim;
either the Gate text or the row needs a sentence.

### F4 — nit: Frontier names "round-5/9" while the moved pins are round-5/7/9

README:134 says "the 2.17.0-era pins in the round-5/9 Walker notes are dated".
The note's moved-pin ledger (`:232-246`) also names the round-7
`walker-live-surface.md` §1/§3 (binary size/sha and `/etc/xdg` size/sha). Not
false, but "round-5/9" reads as excluding round 7; "walker-deep /
walker-live-surface / walker-deep-r9" would be exact.

### F5 — nit: the "choose a surface" table does not route to the new notes

README:61-67: the Walker row (:63) lists only `walker-deep.md`,
`walker-live-surface.md`, `walker-deep-r9.md`; the Themes row (:65) lists only
`theme-wallpaper-plane.md` and the census. The new routes are reachable only
from the coverage table and the Frontier bullet. Round 16 did add its note to
the Waybar row (:62), while round 17's two routes are likewise absent from
this table, so it is a carried pattern — but a reader who starts from the
surface table lands on the older, dated notes with no pointer to the round-18
documentary route.

## Frontier bullet vs the notes' Unexercised sections

**No contradiction found.** Each of the bullet's claims is supported:

| Frontier (README:129-135) | Note evidence |
|---|---|
| "documentary sourced ground" | both notes open "Documentary route only… not observed"; index row Limits repeat it; README:8 already says a new row does not close a behavioral gap |
| "superseding the round-17 … 'P3 Walker and P5 theme/wallpaper sourced routes' open item" | the quoted words are verbatim the round-17 bullet (README:124-127); the r17 bullet remains as written and the r18 bullet supersedes only that clause, the established pattern of rounds 15-16 |
| "runtime theme application" open | theme :139 (consumers loaded the current bytes) |
| "wallpaper reload" open | theme :137 (running swaybg re-reading the retargeted link) |
| "Walker provider behaviour" open | walker :306-308 (elephant provider loading, `provider_hosts`/`before_load` effects, `ProviderConfig`) |
| "the elephant service and wire schema" open | walker :309-310 (socket protocol and walker→elephant message set); documented service mgmt is `[ER:177-178, 129]`, runtime state not claimed |
| "rendered UI" open | walker :318; theme :140 |
| "Host binaries stay `[UNK]`" | walker :288-289; theme :143 |

The bullet is a **summary**, not a retirement: it names ~6 subjects, while the
two notes carry **25** `[UNK]` bullets (walker 15 at :283-321, theme 10 at
:134-145). Named or partially named: W2, W10, T2, T4, T5, T8 (6), partial W1,
W9, W14. **Not named (16):** walker config first-hit / `/etc/xdg` reachability
(:290), `WALKER_*` overlay name map (:293), array merge semantics (:297),
`notify` reachability (:299), syntax-error panic (:301), `[[emergencies]]`
(:304), `omarchy-refresh-config` overwrite (:311), `/tmp/elephant.sock` README
line (:313), Hyprland bindings/layerrule activity (:316), pause/restart state
(:320); theme swaybg process identity/argv (:136), which process started it
(:138), the 16 rendered files not re-derived (:141), the seven payload files
not tag-compared (:142), `OMARCHY_THEME_SKIP_BACKGROUND` (:144), preview-image
and `icons.theme`/`vscode.json`/`neovim.lua`/`chromium.theme` consumers (:145).

Six of the unnamed items are **documentary** holes, not runtime ones (array-merge
body unread, `emergency.rs` unread, comm handlers unread, `omarchy-refresh-config`
unfetched, 16 renders not re-derived, 7 payload files not tag-compared). The
bullet's framing ("moves … onto documentary sourced ground. Still open:
<runtime list>") can be read as "the documentary part is complete". The index
row's walker Limit similarly omits "theme resolution order for partial themes"
(`:318`) although its Holds cell advertises "theme lookup". Recommend one
clause in the bullet: the notes' Unexercised sections list unread sub-documents.

## Answers to the three questions

1. **Source ids S072-S091 / S092-S095: accurate.** Exact bidirectional match
   with the notes' own `source:` lines and bodies; all 24 rows are `mined`
   tier A with the correct `used-by`; range endpoints are the true boundaries
   and no S096 exists. Caveats F1 (five host files unrowed inside the walker
   note), F2 (three host ids have no fetch receipt), F3 (S084 is a policy
   outlier, not an id error).
2. **Frontier bullet vs Unexercised: consistent, subset.** No overclaim found;
   the "still open" list covers the headline runtime gaps and omits 16 named
   UNK bullets (six of them documentary). "Supersedes" is correct for the
   round-17 sourced-route clause only.
3. **Counting command with `REV=4c103b55…`: `indexed=34/34 … coverage=10.0000/10`,
   exit 0**; baseline control `32/32`, exit 0; the fence body is byte-identical
   (`8b59b503…`) at both revisions.

## Residual risk and verification gaps

* No live evidence was gathered or re-checked (host pause): no process, socket,
  consumer reload or screenshot; every behavioural question above stays `[UNK]`
  exactly as the notes say. Host-binary identity to the tags remains open.
* Wave-2 scout receipt directories for some re-opened rows (`ReopenS074`,
  `075`, `076`, `077`, `078`, `079`, `082`, `084`-`089`, `093`, `094`) had no
  `receipts.jsonl` on disk at review time; I did not rely on them and did not
  treat their absence as evidence. This review verifies the committed
  `NoteWalker`/`NoteTheme` receipts, byte-identical at `4c103b55`, `abfbf35`
  and the worktree.
* `docs.rs/latest` cannot be re-pinned by URL; only the committed body can be
  re-hashed. S090's log lines can only be re-read, never re-fetched.
* The counter counts navigation only (its own fence comment); it does not test
  the truth or freshness of either note, and it cannot detect an invented row
  (M6) — that is why the receipt and host-hash checks above matter.

## Seat disclosure (misroot, corrected)

The first `write` of this report used the relative path
`.ufo/waves/round-18/w2/reports/ReviewReadme.md`; the session cwd is the fleet
root, so the file landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-18/w2/reports/ReviewReadme.md`
(a fleet wave-2 directory that also held another seat's
`ConnScorecardNumbers.md` when inspected). It was copied byte-for-byte into the lane path
(sha256 `a31960fd…95235` on both sides at that moment; later edits, including this disclosure, changed the lane copy) and the fleet-root copy was removed in
the same command; `git -C /home/vgpnk/Projects/shokunin ls-files --error-unmatch`
had shown the path was not tracked, so no committed fleet byte was clobbered,
and the sibling `ConnScorecardNumbers.md` was not touched. Every other command in this
report ran with cwd inside the lane root or /tmp and wrote no lane byte except this
report.
