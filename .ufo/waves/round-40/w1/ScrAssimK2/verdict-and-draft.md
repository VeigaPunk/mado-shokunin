# ScrAssimK2 — K2 (`host-producer-outputs-r29`) scope / held / quality check, verdict, and re-grounded draft

Seat: mado round-40 w1 `ScrAssimK2` (leaf; no dispatch, no background jobs, no package transaction).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Written 2026-10-25. Read-only on the host and on
`shokuknow`.

Candidate read (read-only, never written):
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md`
(the path the task names as `merge/mado/corpus/knowledge/…` does not exist; the merge package keeps
knowledge under `merge/mado/knowledge/corpus/knowledge/`, and that is the file read — 66 lines, ends
`---`).

Governing bytes read: `PROVINCE.md`, `corpus/QUALITY.md` (criteria 1–64 as applicable),
`corpus/knowledge/waybar-walker-semantics.md` (held, 478 lines), `corpus/SOURCES.md` (214 rows),
`corpus/README.md` (index), `.ufo/waves/round-40/registration.md`,
`.ufo/waves/round-40/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}`,
`quality/counters/c2-r40-forms-entry.py` docstring (clauses a–h; quote band 3–25 words).

Executor receipts this draft is allowed to rest on:
- `.ufo/waves/round-40/w1/ExecK2HostReads/host-reads.txt` (7796 B, host capture, 2026-10-25)
- `.ufo/waves/round-40/w1/ExecFetchK2Sources/quotes.md` (8837 B, located quotes + carry check)
- `.ufo/waves/round-40/fetch/omarchy-v3.8.4-{screen-recording,notification-silencing}.bin` +
  their `.bin.http.txt`; `.ufo/waves/round-40/fetch/host-indicator-{screen-recording,notification-silencing}.bin`;
  `.ufo/waves/round-40/w1/ExecFetchK2Sources/v3.8.3-{screen-recording,notification-silencing}.bin`

Seat-side checks I ran myself (read-only, cited inline below; none is evidence for the entry unless the
entry names it): `cmp`/`sha256sum` over the six fetched/copied script files; `python3` census of the two
waybar configs; `cat -n` of the host `idle.sh`; `pgrep -a -x hypridle`; `grep` of the lane registry and
index. No compositor verb was run by this seat; no socket was opened by this seat.

---

## §1 Scope check (province) — the producer set is in, the packages behind it are not

`PROVINCE.md:3,11` owns `~/.config/waybar/` and the bar plane; `PROVINCE.md:11` sets the standing
posture: config trees READ-ONLY, probe/measure/recommend, never mutate compositor state.

The candidate's subjects are **bar exec producers**: scripts the bar runs on an interval or signal. That
surface is already practised as chain evidence in the held entry — `waybar-walker-semantics.md:135-149`
reads `weather.sh`, `omarchy-update-available`, `omarchy-voxtype-status`, the three `indicators/*.sh`,
and `~/.local/bin/ai-usage` internals (`:149` quotes `ai-usage:2`, `:2383`, `:2534`, `:406-408`). So the
producer *contract* is IN as the bar's chain, by precedent, not by a new grant.

Boundary, and it bites twice:

- **gkeep package internals are OUT.** `corpus/knowledge/config-drift-r12.md:109` rules: "gkeep remains
  outside this lane's province; report the adjacent change, do not absorb it into mado-owned
  configuration or remediate it." The bar execs `~/.local/bin/gkeep waybar`, so the **shim bytes and the
  producer's declared output contract** are chain evidence (same footing as `ai-usage`); the package's
  own behaviour, install state and window rules are not.
- **Network-dependent producers are OUT of any measured claim.** `weather.sh` → `omarchy-weather-icon`
  curls `wttr.in` (`host-reads.txt:137-138`); `omarchy-update-available` runs `git ls-remote`
  (`host-reads.txt:141-142`). Their live text stays UNK. No external site is contacted by this seat.

Both host-local producers resolve **outside** the owned config plane, and this matters for the anchor
form: `~/.local/bin/gkeep` → `/home/vgpnk/Projects/gkeep/bin/gkeep` and `~/.local/bin/ai-usage` →
`/home/vgpnk/Projects/omarchy-usage-tray/bin/ai-usage` (`host-reads.txt:36-42`, confirmed by
`readlink -f`). The candidate calls both a "host file" at the `~/.local/bin` path without naming the
resolution; QUALITY criterion 18 requires following file symlinks and naming the regular target.

**Scope verdict: the ground is in province, narrowly.** A census of the bar's declared exec producers +
their output contracts + the two host-local producers' shims is admissible. Everything the candidate
does beyond that (the "current outputs" framing built on a volatile cache field, and any statement about
the gkeep package or the network producers' values) is either already held or out.

---

## §2 Held check (duplication) — most of §1 is already held, verbatim in substance

`waybar-walker-semantics.md` (round 3, measured 2026-10-14) already holds the candidate's first two
subjects, including their **measured current outputs**:

| candidate statement | held row |
|---|---|
| S237 probe `pgrep -f "^gpu-screen-recorder"` and "the recorder chip … render[s] empty text" | `:138` — `→ pgrep -f "^gpu-screen-recorder"` (`screen-recording.sh:3`); **RUN** `{"text": ""}` → inactive (no recorder running, `pgrep` empty) |
| S238 probe `makoctl mode \| grep -q 'do-not-disturb'` and "the do-not-disturb chip … empty text" | `:140` — `→ makoctl mode \| grep -q do-not-disturb` (`:3`); **RUN** `{"text": ""}` → DND off; `makoctl mode` → `default` |
| S240 "waybar reads cache only" + cache path | `:149` — chip is **cache-only** (`ai-usage:2`, argparse help `:2534`); cache `~/.cache/ai-usage/status.json` refreshed by `ai-usage.timer` every 5 min |
| "the `custom/ai-usage` producer … renders a Waybar chip" | `:149`, `:163` (`alt` discussion), and the index row `corpus/README.md:17` |
| "`custom/voxtype` … current outputs were not determined — their scripts were located but not read" | `:137` — the script *is* read and its RUN payload measured: `omarchy-voxtype-status:5` `trap 'kill 0' EXIT`, **RUN** `{"alt": "", "tooltip": ""}` |

So four of the candidate's seven OBS blocks restate held rows, and one of its three UNKs
(`custom/voxtype` "scripts located but not read") is **stale against held ground** — the held entry read
that script and measured its payload. QUALITY criterion 17's duplicate screen and criterion 14's census
rule both apply: the candidate is not a new entry, it is a paraphrase of `waybar-walker-semantics.md`
§3.2/§3.3 plus two new producer rows (`gkeep`, and the shim/docstring contracts).

What is genuinely **not held** (and is what a re-grounded entry may add):

1. the **host-vs-upstream byte identity** of the two indicator scripts (candidate never claims it; the
   registration lists it as unheld);
2. the **`custom/gkeep` producer** — exec, interval, signal 12, payload contract (`config-drift-r12.md:35`
   records only its rail position; `waybar-walker-semantics.md` never lists the module);
3. the **resolved shim targets and their shas/sizes** for both host-local producers;
4. a **producer census with a denominator** over the host config bytes.

---

## §3 Quality check (admission bar) — five defects, one of them fatal to the headline claim

**D1 (fatal, criteria 10/14/15): the producer count is the upstream set, not the host set.**
The candidate says "the bar's five JSON producers" (line 37) and "the AI-usage chip is the fourth
decidable case" (line 32). Measured:

- host `~/.config/waybar/config.jsonc`, 6354 B, sha256
  `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829`, mtime 2026-10-17
  (`host-reads.txt:19-24`): **8 modules declare `exec`** and **7 declare `"return-type": "json"`** —
  `custom/weather`, `custom/screenrecording-indicator`, `custom/idle-indicator`,
  `custom/notification-silencing-indicator`, `custom/voxtype`, `custom/gkeep`, `custom/ai-usage`
  (`host-reads.txt:28-30`; re-derived by this seat with `json.loads` after stripping `//` comments).
- the **stock upstream** config (`~/.config/waybar/config.jsonc.bak.1791314470`, 5114 B — the byte size
  the registration already holds as the upstream side) declares **exactly 5** json producers: the same
  list minus `custom/gkeep` and `custom/ai-usage`.

So "five" is the *stock/upstream* producer set substituted for the *host* set — QUALITY criterion 15
(label the layer) and criterion 16 (upstream bytes are not host facts) at once — and the config bytes
that falsify it have been unchanged since 2026-10-17, i.e. before the candidate's own 2026-10-23
measurement. Under criterion 10 the sentence needs `<n> — <command> <date>`; it has neither.

**D2 (fatal, criteria 3/10): the "three … render empty" sentence contradicts its own third member, and
the idle chip's stated reason is inverted on today's host.**
Candidate: "Three of the bar's five JSON producers currently render **empty text**: the recorder chip (no
recorder running), the do-not-disturb chip (mode `default`), and — from round 3 — the idle chip's
counterpart, **which instead shows "Idle lock disabled"** because no `hypridle` runs."

- A member that "instead shows Idle lock disabled" is not a member of a set defined as rendering empty
  text; the sentence cannot be true as written (criterion 3: observation and inference are not separated
  — the count is inference over three mixed observations).
- On this host `hypridle` **runs**: `pgrep -a -x hypridle` → `1680 /usr/bin/hypridle`
  (`host-reads.txt:16`; seat re-check agrees). The script is
  `idle.sh:3` `if pgrep -x hypridle >/dev/null; then` / `:4` `echo '{"text": ""}'` / `:6` the
  `Idle lock disabled` branch (sha256 `6d8d2c11…d10f0f1750`). With hypridle running the **then** branch
  fires, so the idle chip renders **empty**, for the *opposite* reason the candidate gives. The held row
  (`waybar-walker-semantics.md:139`, "glyph shown = lock disabled … `pgrep -x hypridle` empty") was true
  on 2026-10-14; the host state has since changed, and round-35's S205 already recorded hypridle running
  as pid 1667 (`corpus/SOURCES.md` S205 row).
- The corrected census: **three of the seven json producers render empty today** (recorder, DND, idle),
  and they are the three *indicator* chips; `voxtype` renders `{"alt": "", "tooltip": ""}` (invisible,
  different branch), `gkeep` renders its count chip, `ai-usage` renders from cache, `weather` is UNK.

**D3 (fatal for a quote, criteria 6/27): the S241 quote is a rotating volatile value, and it has
already rotated.**
Candidate line 35 quotes `"updated_at": "2026-10-23T22:52:44Z",`. The same field now reads
`"updated_at": "2026-10-25T20:47:13Z",` (`ExecFetchK2Sources/quotes.md:100`, verdict **DIFFERENT**). The
cache is rewritten on a ~5-minute cadence: receipt captured 29865 B at 17:47:21 (`host-reads.txt:114-115`),
this seat observed 29877 B at 17:52. A quote of this field cannot survive any recheck interval, and the
candidate's `recheck: 90d` is unsatisfiable for it. It is also **2 words**, below the campaign's 3–25-word
quote band (`quotes.md:113-114`). This is the same class the round-39 lesson corrected (D2 in the
registration: a rotated volatile timestamp mislabeled).

**D4 (criterion 2 + registry contract): the candidate's five source ids are not in this lane's registry.**
`grep -cE '^\| S(237|238|239|240|241) ' corpus/SOURCES.md` → `0`; the lane's ids run to S277 with gaps,
and `.ufo/waves/round-40/assimilation/{reg-ids,collisions}` show S237–S241 **free** (collisions lists only
S203–S221, S253, S258, S277). The candidate's rows are the merge package's numbering: no lane row confers
them, no `opened`, no `recheck`, no `used-by`, no anchor digest. As written, the entry carries sources
the lane cannot resolve.

**D5 (criteria 6/18): two anchors are symlinks named as "host file", one pinned size has drifted, and the
host-file anchors carry only an access date.**
`~/.local/bin/gkeep` and `~/.local/bin/ai-usage` are symlinks (`host-reads.txt:36-42`); the candidate names
them as files with "read 2026-10-23" and no sha256. The `ai-usage` program's stated size, `134 777 B`, is
**114 246 B** today at the resolved target (`host-reads.txt:45`; `quotes.md:115-116`). The quotes still
reproduce (`quotes.md:99,101,102` — REPRODUCED at `:2`, `:9`, `:64`), so this is anchor drift, not
fabrication.

Non-defects worth recording: the S237/S238 quotes reproduce verbatim (`quotes.md:97-98`), the entry's
OBS/INF/UNK tagging is otherwise disciplined, and its §3 UNKs for `weather`/`update` are correct.

---

## §4 Verdict slot

```
VERDICT (candidate host-producer-outputs-r29.md, as written): REFUSE
VERDICT (re-grounded successor, §5 below):                   ADMIT — conditional on the five gates in §6
RECOMMENDATION:                                              reject the candidate entry; admit the
                                                             re-grounded census entry drafted in §5
```

**Why REFUSE, in one line each:** D1 counts the upstream producer set as the host set (fatal, criteria
10/14/15); D2's headline sentence is internally false and its idle-chip reason is inverted on the host
(criteria 3/10); D3 quotes a value that rotates every ~5 minutes and has already rotated (criteria 6/27);
D4 cites five ids the lane registry does not hold (criterion 2); D5 names symlinks as files and pins a
drifted size (criteria 6/18). Four of its seven observations restate `waybar-walker-semantics.md`.

**Why ADMIT a successor:** the unheld ground is real, receipt-backed and in province — the host/upstream
byte identity of the two indicator scripts, the `custom/gkeep` producer row, the two host-local shims'
resolved identity, and a producer census with a correct denominator (7 json / 8 exec over the host config
bytes). That is an *amendment* to `waybar-walker-semantics.md`'s producer rows, not a new entry about the
same rows.

This pairing also discharges the registration's assimilation gate requirement (≥1 admit and ≥1 reject
recorded) from one candidate, without inventing a second candidate.

---

## §5 Re-grounded draft (successor entry) — statements tied to receipts, `<<QUOTE>>` slots

Proposed path: `corpus/knowledge/host-bar-producer-census-r40.md` (L1 names it; this seat writes no
`corpus/` file). Proposed registry ids: **S237–S241** — free in the lane registry per
`assimilation/collisions` + `assimilation/reg-ids`, and the same five subjects the package numbers S237–S241,
so the numbering does not fork if the package is later merged. L1 must mint the five rows (11 cells, status
`mined`, `opened 2026-10-25`, `used-by` naming this entry) — no row is appended as-is.

Slot convention: `<<QUOTE <receipt>:<line> | <n> words | <verbatim text>>>`. Every slot is 3–25 words, is
`grep -F`-verified against the named receipt by the executor, and must be bound in the round-40 lesson
`## Gate` as `GATE <id> receipt=<path> sha256=<64hex> quote="<q>"`. Values that are **not** 3–25 words
(`default`, `1680 /usr/bin/hypridle`, `makoctl_rc=0`, `pgrep_rc=1`) are stated as OBS naming a receipt line
and are **never** used as a Gate quote.

The fenced block below is the entry text as it would land; its own section numbers restart at §1, and the
outer sections of this file continue after it at §6.

```markdown
# The bar's exec producers: a host census, their output contracts, and what each chip renders today

source: S237 — omarchy v3.8.4 `default/waybar/indicators/screen-recording.sh` — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/screen-recording.sh — `§ line 3` — tag `v3.8.4`, 169 B, sha256 `28491cd3fdaaea78143432d6e2d5b609f06f90e420874d8bdd83a25a199bc63c`; receipt `.ufo/waves/round-40/fetch/omarchy-v3.8.4-screen-recording.bin` (+ `.http.txt`: HTTP 200, CURL_EXIT 0)
source: S238 — omarchy v3.8.4 `default/waybar/indicators/notification-silencing.sh` — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/notification-silencing.sh — `§ line 3` — tag `v3.8.4`, 174 B, sha256 `312900d1a9ca772e944e626d86cb54af6dec4dd5619510ecb262562da9d6de69`; receipt `.ufo/waves/round-40/fetch/omarchy-v3.8.4-notification-silencing.bin` (+ `.http.txt`: HTTP 200, CURL_EXIT 0)
source: S239 — host `custom/gkeep` producer shim — `/home/vgpnk/Projects/gkeep/bin/gkeep` (reached as the symlink `~/.local/bin/gkeep`) — `§ line 9` — 252 B, mode 755, sha256 `c1b147a07f0c34af9fdafd184252c6cd97f4a26073d75aa88a72f97c748cfbf8`; receipt `.ufo/waves/round-40/w1/ExecK2HostReads/host-reads.txt` §2, §2a
source: S240 — host `custom/ai-usage` producer — `/home/vgpnk/Projects/omarchy-usage-tray/bin/ai-usage` (reached as the symlink `~/.local/bin/ai-usage`) — `§ line 2, line 64` — 114 246 B, mode 755, sha256 `0ccd33ab7e83edd0141bfec722488cc7518c70f64122b1198470d144c50a0254`; receipt `.ufo/waves/round-40/w1/ExecK2HostReads/host-reads.txt` §2, §2b
source: S241 — own-work: the round-40 producer census and host reads (measured on this host, 2026-10-25) — `.ufo/waves/round-40/w1/ExecK2HostReads/host-reads.txt` — `§1, §4, §5, §7`
verified-at: 2026-10-25
recheck: 90d — re-read `~/.config/waybar/config.jsonc`, re-run `pgrep -f '^gpu-screen-recorder'`,
`pgrep -x hypridle`, `command -v voxtype`; the cache's `updated_at` **value** is never quoted or pinned
ground: amends `knowledge/waybar-walker-semantics.md` §3.2/§3.3 (its producer rows, measured 2026-10-14):
adds the producer census with its denominator, the host-vs-upstream byte identity of the two indicator
scripts, the `custom/gkeep` producer, and the resolved identity of the two host-local shims. No Frontier
row is moved.

Lane: mado-shokunin, round 40. Read-only: config trees were read, bytes copied into receipts; the bar's
producers were **not** executed by the lane; the ai-usage cache was opened for key names only (no provider
value, credential or token was read or printed). No compositor verb beyond `hyprctl version`; no socket
was connected by the seat that produced the upstream half. Receipts:
`.ufo/waves/round-40/fetch/omarchy-v3.8.4-screen-recording.bin` (+ `.http.txt`),
`…-notification-silencing.bin` (+ `.http.txt`), `.ufo/waves/round-40/fetch/host-indicator-screen-recording.bin`,
`…-notification-silencing.bin`, `.ufo/waves/round-40/w1/ExecFetchK2Sources/v3.8.3-{screen-recording,notification-silencing}.bin`,
`.ufo/waves/round-40/w1/ExecK2HostReads/host-reads.txt`.

## §1 The census (S241)

**OBS** The host bar config is 6354 B at sha256
`a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829`, mtime 2026-10-17 17:02:56 -0300
(S241 `:19-24`): <<QUOTE host-reads.txt:24 | 3 words | size=6354 mtime=2026-10-17 17:02:56.289420985 -0300>>

**OBS** Of its modules, **7 declare `"return-type": "json"`** (S241 `:28-30`):
<<QUOTE host-reads.txt:28 | 6 words | modules with "return-type": "json" = 7:>>
The seven json producers are `custom/weather`, `custom/screenrecording-indicator`, `custom/idle-indicator`,
`custom/notification-silencing-indicator`, `custom/voxtype`, `custom/gkeep`, `custom/ai-usage`.

**OBS** The census has no missing and no extra member against the config's own declaration: the expected
set (modules declaring `return-type: json`) and the observed set are the same seven keys, read from the
same bytes. An eighth module, `custom/update`, declares `exec` without `return-type` and renders text
(S241 `:141`); a seat re-derivation of the same bytes also counts **8** modules declaring `exec` — that
count is the seat's, not the receipt's, and L1 either re-derives it with the command in the seat report §6 G5 or drops it.
A count of producers is layer-dependent in any case: the **stock upstream** config on this host declares a
smaller json set (seat census, same command, G5), so any sentence of the form "the bar's N JSON producers"
must name which layer N counts.

## §2 The two indicator producers and their byte identity (S237, S238)

**OBS** The recorder chip is a process probe (S237):
<<QUOTE fetch/omarchy-v3.8.4-screen-recording.bin:3 | 6 words | if pgrep -f "^gpu-screen-recorder" >/dev/null; then>>
and its negative branch is an empty payload (S237 line 6): <<QUOTE fetch/omarchy-v3.8.4-screen-recording.bin:6 | 3 words | echo '{"text": ""}'>>

**OBS** The notification chip is a single read-only query, tested as a **substring**, not as an equality on
the mode name (S238): <<QUOTE fetch/omarchy-v3.8.4-notification-silencing.bin:3 | 8 words | if makoctl mode | grep -q 'do-not-disturb'; then>>
Its negative branch is byte-identical to S237's: <<QUOTE fetch/omarchy-v3.8.4-notification-silencing.bin:6 | 3 words | echo '{"text": ""}'>>

**OBS** Host and upstream are the **same bytes** for both scripts: `cmp` rc=0 in four comparisons (upstream
vs host copy, host tree vs upstream), identical sizes and sha256 — 169 B `28491cd3…a199bc63c` and 174 B
`312900d1…9d6de69` (S241 `:127-131`; seat re-ran `cmp` and `sha256sum` over the six files, all rc=0). The
upstream **v3.8.3** tag serves the same two sha256 (`w1/ExecFetchK2Sources/v3.8.3-*.bin`), so the identity
is not an artifact of the tag choice. This is the opposite of the config plane, where host and upstream
differ (6354 B vs 5114 B).

**INF** Because the scripts are byte-identical, every behaviour the held entry attributes to them
(`waybar-walker-semantics.md:138,140`) is an upstream behaviour on this host as well; no host-local edit
exists to diverge. Basis: the four `cmp` rc=0 results and the two sha256 pairs above.

## §3 What each json producer renders today (S241)

The three *indicator* chips render empty right now, all three for a measured reason:

- **recorder** — `pgrep -f '^gpu-screen-recorder'` exits 1 with no output (S241 `:103-104`); the binary is
  installed, no recorder is running, so S237's negative branch fires. **OBS**, time-varying.
- **notification-silencing** — `makoctl mode` prints `default` and exits 0 (S241 `:105-107`); the substring
  `do-not-disturb` is absent, so S238's negative branch fires. **OBS**, time-varying. (This value is one
  word and is not usable as a Gate quote; it is stated from the receipt line.)
- **idle** — `pgrep -a -x hypridle` prints `1680 /usr/bin/hypridle` (S241 `:16`), so
  `idle.sh:3` `if pgrep -x hypridle >/dev/null; then` is true and its **then** branch `echo '{"text": ""}'`
  (`idle.sh:4`, sha256 `6d8d2c11…d10f0f1750`) fires. The chip is empty **because the idle lock is armed** —
  the inverse of the round-3 reading, which held the host with no hypridle running. **OBS**, time-varying.

The other four:

- **`custom/voxtype`** — `command -v voxtype` exits 1 (absent, S241 `:108-109`), so
  `omarchy-voxtype-status` takes its else branch and emits `{"alt": "", "tooltip": ""}` (S241 `:143-144`):
  a payload with no icon key, i.e. an invisible module. **OBS** for the branch, **INF** for the rendering.
- **`custom/gkeep`** — renders `{text: ICON + count}` from the local note store (S239, §4 below). **OBS**
  contract; the count itself is operator data and is reported dated, not pinned.
- **`custom/ai-usage`** — renders from its cache only (S240, §4). Its current payload was **not** read:
  the receipt extracted key names and the freshness predicate only. **UNK** by policy.
- **`custom/weather`** — network (`omarchy-weather-icon` curls `wttr.in`, S241 `:137-138`). **UNK**; not
  fetched, not run.

**INF** Decidability splits the seven cleanly and without remainder: 5 are decidable offline from a local
process or file (recorder, DND, idle, voxtype, gkeep), 1 is decidable offline but its payload is withheld
by the no-values policy (ai-usage), and 1 is not decidable offline (weather). `custom/update` is the eighth
exec producer and is also network-bound (`git ls-remote`, S241 `:141-142`). Basis: the seven branches above.

## §4 The two host-local producers (S239, S240)

**OBS** Both `~/.local/bin` entries are **symlinks**; the producers are regular files elsewhere
(S241 `:36-45`): `gkeep` → `/home/vgpnk/Projects/gkeep/bin/gkeep`, 252 B, mode 755, sha256
`c1b147a0…c748cfbf8`; `ai-usage` → `/home/vgpnk/Projects/omarchy-usage-tray/bin/ai-usage`, 114 246 B, mode
755, sha256 `0ccd33ab…4c50a0254`. An earlier record's size for `ai-usage` (134 777 B) is superseded by this
measurement.

**OBS** The `custom/gkeep` producer is a shim onto an installed package (S239):
<<QUOTE w1/ExecK2HostReads/host-reads.txt:57 | 4 words | from gkeep.cli import main>>
and its bar payload is declared by the package (S241 `:145`):
<<QUOTE host-reads.txt:145 | 10 words | One-line JSON for a waybar custom module. Local count only.>>
The payload is `{text, tooltip, class}` computed from `list_notes()` over
`$XDG_DATA_HOME/gkeep/notes.json` (S241 `:145-148`): no network, so the chip is decidable offline. The
store's shape is `[notes, version]` with `notes` a list of dicts keyed `[body, created, id]`; note **bodies
were not read**. The producer's *config block* is `exec: ~/.local/bin/gkeep waybar`, `interval: 30`,
`signal: 12`, `format: "{}"`, `on-click: … gkeep capture`, `on-click-right: … gkeep list`
(S241 `:77-86`, verbatim). **Signal 12 is a consumer the held signal table (`waybar-walker-semantics.md` §4,
7–11) does not carry.**

**OBS** The `custom/ai-usage` producer declares its own contract (S240):
<<QUOTE w1/ExecK2HostReads/host-reads.txt:64 | 14 words | """Cache AI CLI usage windows and render a Waybar chip. waybar reads cache only.""">>
and resolves its cache path from the environment (S240):
<<QUOTE w1/ExecK2HostReads/host-reads.txt:152 | 5 words | return Path(os.environ.get("AI_USAGE_CACHE", Path.home() / ".cache/ai-usage/status.json"))>>
`cmd_waybar()` reads `load_cache()` only, and `load_cache()` is `json.loads(cache_path().read_text())`
(S241 `:150-151`) — cache-only, no network, no CLI call on the render path. Its config block adds
`escape: false`, `exec-on-event: false` and four click/scroll verbs (S241 `:87-101`, verbatim).

## §5 Freshness without quoting a value (S241)

**OBS** The cache is 29 865 B at mtime 2026-10-25 17:47:21 -0300, sha256 `e7f45d27…b57dd0438f` at capture
(S241 `:113-116`), and its top-level keys are (S241 `:118`):
<<QUOTE host-reads.txt:118 | 6 words | top-level keys: providers, selected, updated_at, version>>
The freshness field's type is (S241 `:121`): <<QUOTE host-reads.txt:121 | 5 words | updated_at: type str, ISO-8601 "Z">>
and at capture it was within 24 h (age 0.04 h, S241 `:122`). Twelve provider sub-keys exist; no provider
value, credential or token was read.

**OBS** The `updated_at` **value rotates**: the candidate quoted `…-10-23T22:52:44Z` and the same field
read `…-10-25T20:47:13Z` on 2026-10-25 (`w1/ExecFetchK2Sources/quotes.md:100`, verdict DIFFERENT); the
cache is rewritten on a ~5-minute cadence by `ai-usage.timer` (held,
`waybar-walker-semantics.md:149`), and the seat observed its size move 29 865 → 29 877 B within minutes of
the capture. **This entry therefore quotes the field's name and type, never its value**, and a 90-day
recheck can re-derive only the predicate.

**INF** A stale chip is distinguishable from a fresh one only by reading the cache's own `updated_at`
against the wall clock — the bar does not display it. Basis: the key set above plus the cache-only render
path (§4). The threshold the producer applies to that field is **UNK** (not read this round).

## §6 UNK

**UNK** The live `custom/weather` icon: network, not fetched, not run.
**UNK** The live `custom/update` text: `git ls-remote` against the checkout's origin; not run.
**UNK** The `custom/ai-usage` chip's current payload: withheld by the no-values policy (key names only).
**UNK** The rendered pixels of any chip: no screenshot this round; a payload is not a rendering
(`waybar-observation-boundaries-r16.md`).
**UNK** The gkeep note bodies and any note-derived tooltip text: not read.
**UNK** The threshold at which `ai-usage` calls a cache stale.
**UNK** Whether `makoctl mode`'s socket read is admissible for a lane seat: one executor ran it (S241 `:105-107`)
and another declared it barred (`ExecFetchK2Sources/quotes.md:124`). The receipt is what this entry cites;
the conduct question is not this entry's.
```

---

## §6 Reject list and flip conditions for the successor

The draft deliberately does **not** carry these candidate statements; each is rejected with its flip
condition, per QUALITY criterion 5 (a rejection is kept, not dropped):

1. **"the bar's five JSON producers"** — rejected (D1). Flips only if the sentence names its layer
   (`5` upstream json producers / `7` host json producers / `8` host exec producers) and prints the
   counting command and date, per criterion 10.
2. **"Three of the bar's five JSON producers currently render empty text … the idle chip's counterpart,
   which instead shows 'Idle lock disabled'"** — rejected (D2). Flips to a true statement once the idle
   member is stated with its branch (`hypridle` running ⇒ empty) and the denominator is the host's 7.
3. **the `updated_at` value quote and the `recheck: 90d` that depends on it** — rejected (D3). Flips only
   to a *predicate* claim (name + type + age at capture), never to a value quote.
4. **"the AI-usage chip is the fourth decidable case"** — rejected as arithmetic over a wrong denominator;
   replaced by the 5/1/1 split in §3 of the draft.
5. **"the `custom/update` and `custom/voxtype` producers' current outputs were not determined — their
   scripts were located but not read"** — rejected as stale against held ground (`waybar-walker-semantics.md:137`
   reads the voxtype script and measures its payload). Flips only with a receipt showing the script unread.
6. **"134 777 B"** for `ai-usage` — superseded by 114 246 B at the resolved target.
7. **"host file /home/vgpnk/.local/bin/gkeep, read 2026-10-23"** — superseded by the symlink resolution and
   the target sha256.
8. **the gkeep package's own Waybar output** — stays OUT (province, `config-drift-r12.md:109`). Flips only
   on an explicit ownership transfer.

**Admission gates for the successor (all five must hold before L1 appends it):**

- **G1** the five registry rows exist with the draft's anchors (S237–S241 free per
  `assimilation/collisions`; `opened 2026-10-25`; `used-by` naming the entry), each 11 cells;
- **G2** a `## Gate` line per cited id, receipt committed under `.ufo/waves/round-40/fetch/` with the
  sha256 the Gate names, quote 3–25 words and present in the receipt's normalized text. The two
  `host-reads.txt` receipts currently live under `w1/ExecK2HostReads/`, not `fetch/` — L1 either copies
  them into `fetch/` (they are the executors' bytes; this seat does not write another seat's files) or the
  lesson's Gate shape must admit the committed seat path. **This is the one open mechanical dependency.**
- **G3** `ExecK2HostReads/host-reads.txt:145` and `:152` are verbatim *quotes* of `gkeep/waybar.py` and
  `ai-usage:64` only as the receipt renders them; if L1 wants them as Gate quotes for S239/S240, the Gate
  receipt must be a file whose normalized text contains those lines — `host-reads.txt` does (`:145`, `:152`),
  and the S240 line at `:152` is the receipt's `cache_path(): line 64` rendering. L1 should prefer the
  `quotes.md` lines (`:101`, `:102`) which are `grep -F`-verified against the resolved targets.
- **G4** exactly one column-zero index row in `corpus/README.md` for the entry, naming the amends target
  (`knowledge/waybar-walker-semantics.md`) and the receipts.
- **G5** the two **seat re-derivations** in the draft's §1 — the `exec`-module count (8) and the stock
  upstream config's json count (5) — are re-derived by L1 with this command and committed as a receipt, or
  the clauses are dropped. They are the only statements in the draft that rest on this seat rather than on
  an executor receipt. Run as one `-c` block:

  ```
  python3 -c 'import json,re,sys
  for p in sys.argv[1:]:
      s=re.sub(r"//[^\n]*","",open(p).read()); d=json.loads(s)
      m={k:v for k,v in d.items() if isinstance(v,dict)}
      print(p,"exec=",len([k for k,v in m.items() if "exec" in v]),"json=",len([k for k,v in m.items() if v.get("return-type")=="json"]))' \
      ~/.config/waybar/config.jsonc ~/.config/waybar/config.jsonc.bak.1791314470
  ```

  This seat ran exactly this and got `exec= 8 json= 7` for the host config and `exec= 6 json= 5` for the
  stock backup.

---

## §7 Conflicts reported verbatim (for the canonical judge; not resolved here)

1. **`makoctl mode` admissibility.** `w1/ExecFetchK2Sources/quotes.md:124`: "`makoctl mode` was **not**
   run: it opens the mako daemon socket, and this seat is barred from socket connects of its own."
   Against `w1/ExecK2HostReads/host-reads.txt:105-107`:
   ```
   $ makoctl mode ; echo makoctl_rc=$?
   default
   makoctl_rc=0
   ```
   Both are executor receipts. The draft cites the second; which reading binds is the judge's call.
2. **`hypridle` state.** Candidate (`host-producer-outputs-r29.md:37-40`): "no `hypridle` runs" /
   "Idle lock disabled". Against `host-reads.txt:16`: `1680 /usr/bin/hypridle` (seat re-check agrees).
   Also `corpus/SOURCES.md` S205 (round 35) recorded pid 1667 — the daemon has run across at least two
   rounds, so the round-3 "no PID" state has been superseded for some time.
3. **`ai-usage` size.** Candidate `134 777 B` vs `host-reads.txt:45` `size=114246`.
4. **`updated_at`.** Candidate `2026-10-23T22:52:44Z` vs `quotes.md:100` current `2026-10-25T20:47:13Z`.
5. **Producer count.** Candidate "five" vs `host-reads.txt:28-30` `7` json / `8` exec on the host config,
   and `5` json in the stock 5114 B config (seat census).

---

## §8 What this seat wrote, ran, and did not do

Wrote (inside the lane, only): `.ufo/waves/round-40/w1/ScrAssimK2/verdict-and-draft.md` (this file) and
`.ufo/waves/round-40/w1/ScrAssimK2.md` (the seat report). No tracked file edited; no `corpus/`, `tools/`,
`quality/`, `scripts/`, `templates/`, `MANIFEST.json`, `.ufo/state/` write; no git/jj mutation anywhere.

Ran (read-only): `read`/`grep`/`glob` over the lane and the merge package; `cmp` and `sha256sum` over the
six fetched/copied indicator files (all rc=0, host == v3.8.4 == v3.8.3); `python3` (comment-stripped
`json.loads`) over `~/.config/waybar/config.jsonc` and its 5114 B stock backup to census exec/json modules;
`cat -n` and `sha256sum` of `~/.local/share/omarchy/default/waybar/indicators/idle.sh`;
`pgrep -a -x hypridle`; `ls`/`stat` on the two `~/.local/bin` symlinks and the cache file. No compositor
verb; no socket; no `makoctl`; no package transaction; no tool installed.

Not done (declared gaps): I did not run any producer, did not read the ai-usage cache's values, did not
read gkeep note bodies, did not fetch weather or the update origin, and did not verify the S241 Gate
receipt placement under `fetch/` (G2) — that is L1's integration step.
