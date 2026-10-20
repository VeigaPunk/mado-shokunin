# FrontierRows — round 19 draft (frontier rows, study path, leads)

Seat `MadoR19.FrontierRows`, 2026-10-20. Read: `corpus/README.md` `## Frontier`
and the coverage-map rows, `corpus/SOURCES.md` `## Paths` / `## Leads (unopened)` /
rows S072–S095, `corpus/lessons/round-18.md` §Mistakes + §Gate, the round-18
spot-check §4–§6, `corpus/knowledge/walker-route-r18.md` and
`corpus/knowledge/theme-route-r18.md` head/tail, `.ufo/waves/round-19/gen_w1.py`,
`SCORECARD.md` "Round 19 — declared claims", and the S096 row draft already on
disk (`.ufo/waves/round-19/drafts/HostWalkerBytes-row.md`). Read-only; nothing
executed on the host.

## 1. Verdict

The four planned items advance **two** Frontier statements and **retire two
registry-durability defects that the Frontier section never names**:

- advance: the round-18 clause "Host binaries stay `[UNK]`" and the round-17
  parenthetical "(a pacman.log pkgver is a log line, not a running-binary fact)"
  — S096 turns walker's *binary bytes* into a mined host fact while leaving the
  parenthetical true;
- advance: "the 2.17.0-era pins in the round-5/9 Walker notes are dated, not
  current" — for the fixed owned set only, and only if the sweep reaches 13/13;
- retire (record debt, not surface): S097 for S094's per-fetch HTML digests
  (R18-V1) and S098 for S084's docs.rs `latest` alias (R18-V4);
- **no advance**: rendered UI, Waybar module text, Walker socket protocol,
  dispatcher behavior, provider behavior, the elephant service/wire schema,
  theme application and wallpaper reload. S096 never starts or queries anything.

## 2. Frontier bullets this round touches

| `corpus/README.md` | Front text (quoted, trimmed) | Round-19 item | Effect | Wording consequence |
|---|---|---|---|---|
| :82-84 | "Rendered UI, Waybar module text, Walker socket protocol, dispatcher behavior …" | none | no advance | unchanged; S096's own limits say no process, socket or screenshot |
| :85-87 | "Idle/lock transitions and daemon stop-cause" | none | no advance | unchanged |
| :88-90 | "Unlanded theme/Walker live rows … Note rows do not make proposed gate rows executable" | gate `live.walker.version` re-pin (C2) | no advance | unchanged; a pin move is not a new executable row, and must not be written as one |
| :91-93 | "Historical errata and record debt remain dated: … §5/F1–F5; Walker candidate errata in r9 §8 …" | S097, S098 | partial — retires two items **outside** this bullet's named sets | name the two retirements in the new round-19 bullet; do not claim this bullet closed (F1–F5, r9 §8 untouched) |
| :94-96 | "Outside-lane promotion verification remains unestablished" | none | no advance | unchanged |
| :97-120 | rounds 12–16 surfaces | none | no advance | unchanged |
| :121-128 | "Compiled host binaries stay `[UNK]` (a pacman.log pkgver is a log line, not a running-binary fact)" | S096 | **narrowed** | binary *file bytes* are now mined; the parenthetical stands verbatim in meaning |
| :129-135 | "Host binaries stay `[UNK]`; the 2.17.0-era pins in the round-5/9 Walker notes are dated, not current" | S096 + pin sweep + S097 + S098 | **superseded for the pin clause, narrowed for the binary clause** | split the sentence: bytes mined (S096) / running process + `--version` print `[UNK]`; pin clause replaced by "every owned mention carries a dated pointer (counter-checked)" |
| :129-135 | "Still open: runtime theme application and wallpaper reload, Walker provider behaviour, the elephant service and wire schema, rendered UI" | none | no advance | keep the list verbatim — it is still exactly right |

Also true and worth carrying: SOURCES **S094's scope cell** says "the only theme
on this host". That is literally false — `ls -1 ~/.local/share/omarchy/themes/ | wc -l`
→ **19** payload dirs (matte-black … white). The phrase is true only for the
*applied* theme (`current/theme.name` = `matte-black`), which the round-18 note
already qualifies (`corpus/knowledge/theme-route-r18.md:162`). **S097's scope must
say "the applied theme on this host"**; do not copy the old scope cell forward.

## 3. Draft — `corpus/README.md` `## Frontier`, append after :135

Paste only after (a) S096, S097 and S098 are admitted rows with their drafts
landed and (b) the sweep is measured; if the counter lands at 12/13 rather than
13/13, replace "each carries" with the measured fraction and name the missing file.

```markdown
- Round 19 narrows the round-17/18 "host binaries stay `[UNK]`" sentence to what
  was read, not run: walker's **binary bytes** are a mined host row now (S096 —
  digest, package `desc` `2.17.2-1`, compiled-in literal `2.17.2` at file offset
  856,302), and every owned file that still said `2.17.0` carries a dated forward
  pointer or re-pinned value to S090/S091/S096 (checked by
  `python3 -I .ufo/waves/round-19/fresh-pins.py REV`). The running process and the
  `--version` print stay `[UNK]`: no walker, pacman or service query. S097
  supersedes S094's per-fetch GitHub HTML digests with tag-pinned content
  identities, and S098 replaces the docs.rs `latest` alias with the xdg 3.0.0
  crate tarball whose sha256 is walker v2.17.2's own `Cargo.lock` checksum —
  durability repairs, not new behaviour. Still open: runtime theme application
  and wallpaper reload, Walker provider behaviour, the elephant service and wire
  schema, rendered UI. A moved gate pin (`live.walker.version`) is a pin, not a
  measurement.
```

Line discipline: one bullet, ≤ 15 lines, holds `2.17.2` + `S096` + `S097` + `S098`,
supersedes the round-18 pin clause explicitly, and leaves the "still open" list
word-for-word. No statement about a running binary, a socket, pixels or a service.

## 4. Draft — `corpus/SOURCES.md` `## Paths`, append after the round-17 entry

```markdown
- **Walker version provenance (P3, round 19)** — S096 → S090 → S078 → S079 → S098
  → S073 → S091: start from the host's own bytes at the moved pin (binary digest,
  package `desc` `2.17.2-1`, compiled-in literal at file offset 856,302), then the
  log line that dates the move (S090 — a log line is never a binary fact), then
  the upstream tag's declared version and whole-tree tarball, then the dependency
  that tag's own `Cargo.lock` checksums (xdg 3.0.0; crate tarball sha256
  `2fb43323…` equals the lock checksum), then the packaged default table that is
  byte-equal to the host `/etc/xdg` file, and last the host's user config bytes.
  Every step is a file or tag digest; the running process, the `--version` print
  and provider behaviour stay `[UNK]`.
```

Order rationale (state it in the Paths prose, as the older entries do): host
identity before upstream identity, because a digest alone cannot say what the
bytes mean; the log line second because it dates the move but proves nothing about
the binary; the tag before its dependency because the lockfile checksum is only
meaningful as the tag's own pin; the packaged default before the host config
because byte-equality is the join between them.

Optional, only if L1 wants the S097 supersession routed in `## Paths` too (not
required by the round's claims):

```markdown
- **Theme payload durability (P5, round 19)** — S094 → S097: read the retired
  row's reject reason first, then the superseding row's tag-pinned content
  identities. The payload's *application* is not in this path.
```

## 5. Draft — `corpus/SOURCES.md` `## Leads (unopened)`, append as a new block

Keep the section's standing sentence ("A lead is not evidence and never a row")
above; prefix the block so it is not read as a round-12 seat.

```markdown
Round 19 (2026-10-20), from the `FrontierRows` seat:

- walker's v2.17.0 → v2.17.2 changed surface: seven commits over twelve files (new
  `src/niri.rs` +399, `src/config.rs` +44, `src/main.rs` +79/−14, `Cargo.lock`
  +306/−193), bodies present under `.ufo/waves/round-18/fetch/SrcWalkerChangelog/`
  but admitted by no SOURCES row. The packaged-default delta is four edits
  (`blur_corner_radius`, a `[niri]` table, an `edit` action binding, clipboard
  `remove` `after = "SimpleDelete"`); every default the round-5/9 notes cite
  (`close_when_open`, `theme`, `max_results`, prefixes) is unchanged in value. A
  round wanting the delta as evidence must row the tag-pinned raw side it needs
  (v2.17.0 body sha256 `5b4e47b7…`; v2.17.2 side = S073) — the GitHub
  compare/release JSON is discovery, not a digest anchor (lesson M7).
- `/etc/pacman.d/hooks/walker-restart.hook` — the hook named at
  `/var/log/pacman.log:3062` and `:3123` (S090) appears in no package's file list
  (`grep -l walker-restart /var/lib/pacman/local/*/files` → no hit) and was never
  read. It is the only artifact that could say what the upgrade did to the
  service; its bytes are readable evidence, and even then it could not establish
  that a process is running.
- walker's niri IPC integration (commit `c299cd8d0`, `src/niri.rs` added in the
  v2.17.0 → v2.17.2 range) — the round-18 note cites the file once, as a
  notify-search hit (`walker-route-r18.md:102`); no row scopes its provider
  behaviour. This host is Hyprland, so the surface is both unopened and off-host.
```

Two candidate sources do **not** belong in Leads: docs.rs `latest` (retired by
S098) and GitHub tree HTML (retired by S097 and lesson M7). The round-18 Gate
already classes them as "reject or leave unrowed"; round 19 applies that class in
the registry rather than queueing it.

## 6. Coupling L1 must land with the above (bookkeeping, not new claims)

1. `corpus/README.md:44` (coverage row for `walker-route-r18.md`) says
   `source:` **S072–S091**. If S098 becomes the note's XDG support, the range
   shorthand becomes false: write `S072–S083, S085–S091, S098` (S084 keeps its
   row but no longer carries that claim).
2. `corpus/README.md:45` (theme row) says `source:` **S092–S095**. After S094
   flips to `rejected` with `used-by` moved and S097 carries the claim, write
   `S092–S093, S095, S097`.
3. The walker note's own anchor key **`XD`** (`walker-route-r18.md:36`) is
   `https://docs.rs/xdg/latest/…` saved HTML. S098 does not fix that line by
   itself: the note's `source:` header, the `XD` key and its `recheck:` must point
   at the crate tarball + `Cargo.lock` checksum, or the note keeps an unpinned
   support line while the registry looks fixed.
4. `fresh-pins.py`'s pointer regex accepts **any** `S\d{3}`. Review rule for the
   closure (per `RevFreshPinsCounter` in `gen_w1.py`): a pointer line must cite
   **S090, S091 or S096**; count any other row as not current. Do not silently narrow the pre-registered
   instrument — record the review check in the receipt or amend the counter
   openly.
5. The S096 row draft on disk already carries the load-bearing anchor
   (`2.17.2\n` at **856,302**, package `desc` sha256 `5c0d9d89…`, `%VERSION%`
   `2.17.2-1`, log line 2929). Use those exact values in the Paths prose and the
   frontier bullet; do not restate the round-9 offset 847,791 as comparable — a
   file offset is not stable across builds (the draft says so itself).

## 7. Evidence (commands run, read-only)

```
$ python3 -I .ufo/waves/round-19/fresh-pins.py 9c54c56 | jq -c '{denominator,current,score}'
{"denominator":13,"current":2,"score":1.5385}          # 11 files with no 2.17.2+S### line
$ ls -1 ~/.local/share/omarchy/themes/ | wc -l
19
$ ls -1 ~/.local/share/omarchy/themes/ | tr '\n' ' '
catppuccin catppuccin-latte ethereal everforest flexoki-light gruvbox hackerman
kanagawa lumon matte-black miasma nord osaka-jade retro-82 ristretto rose-pine
tokyo-night vantablack white
$ sed -n '2929p' /var/log/pacman.log
[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
$ sed -n '1,6p' /var/lib/pacman/local/walker-2.17.2-1/desc
%NAME% walker … %VERSION% 2.17.2-1 … %URL% https://github.com/abenz1267/walker
$ sha256sum /usr/bin/walker
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
$ grep -n '^name = "xdg"' -A 3 .ufo/waves/round-18/fetch/MadoR18.SrcWalkerThemes/cargo-lock.txt
2705:name = "xdg" / 2706:version = "3.0.0" /
2708:checksum = "2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5"
$ curl -sSL --max-time 60 -o xdg-3.0.0.crate -w '%{http_code} %{url_effective}'
https://static.crates.io/crates/xdg/xdg-3.0.0.crate → 200, 15,821 B
$ sha256sum xdg-3.0.0.crate
2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5   # = lock checksum
$ grep -n 'pub fn find_config_file' -B 2 /tmp/xdgcrate/xdg-3.0.0/src/base_directories.rs
447: /// configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then
448: /// `XDG_CONFIG_DIRS`.
449: pub fn find_config_file<P: AsRef<Path>>(&self, path: P) -> Option<PathBuf> {
$ find /usr/share/libalpm/hooks /etc/pacman.d/hooks -maxdepth 1 -iname '*walker*'
/etc/pacman.d/hooks/walker-restart.hook        # operator-local path, unread
$ diff .ufo/waves/round-18/fetch/SrcWalkerChangelog/walker-v2.17.{0,2}-resources-config.toml
+blur_corner_radius = 20 ; +[niri] (3 keys) ; +{ action = "edit", bind = "ctrl e" } ;
-{ action = "remove", … after = "AsyncClearReload" } / +… after = "SimpleDelete"   # 9 changed lines
$ python3 -c '…compare JSON…'   # .ufo/waves/round-18/fetch/SrcWalkerChangelog/
total_commits 7; files 12; src/niri.rs added +399; src/main.rs modified +79/-14;
Cargo.lock +306/-193; resources/config.toml +8/-1; src/config.rs +44/-0
```

Fetch receipt for the crate body:
`.ufo/waves/round-19/fetch/FrontierRows/receipts.jsonl`
(`https://static.crates.io/crates/xdg/xdg-3.0.0.crate`, 200, 15,821 B,
sha256 `2fb43323…`, `curl 8.23.0`).

## 8. Limits

- Did not verify S097 or S098 row text: only S096's draft existed on disk; the
  reserved ids are cited as the round contract declares them.
- Did not read `/etc/pacman.d/hooks/walker-restart.hook` bytes, did not fetch the
  omarchy tree object ids, did not run rubric V or the census, did not measure
  the post-sweep 13/13 end state.
- The frontier bullet's "every owned file carries …" is conditional on the sweep
  landing; L1 must paste only the measured form.
- README/SOURCES line numbers are as at `9c54c56`; any insert above shifts them.
- No host process, socket, service, compositor or package operation was
  performed; all host facts above are file bytes.

## Installs

none.
