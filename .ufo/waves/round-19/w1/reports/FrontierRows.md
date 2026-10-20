# FrontierRows — round 19 advances two frontier statements and retires two unnamed record-debt items; one walker-provenance study path drafted

Seat `MadoR19.FrontierRows`, 2026-10-20. Read-only (host files as bytes; no
walker, pacman, systemctl, compositor or probe command). Draft delivered at
`.ufo/waves/round-19/drafts/FrontierRows.md` (14.3 KB): paste-ready Frontier
bullet, one ordered `## Paths` line, a round-19 `## Leads (unopened)` block, and
five coupling items L1 must land with them.

## 1. Which frontier statements move (README.md as at `9c54c56`)

| Frontier text | Item | Verdict |
|---|---|---|
| `corpus/README.md:129-135` "Host binaries stay `[UNK]`; the 2.17.0-era pins in the round-5/9 Walker notes are dated, not current" | S096 + 13-file pin sweep | **superseded for the pin clause** (owned set only, conditional on 13/13); **narrowed for the binary clause** — bytes are mined (digest, `desc` `2.17.2-1`, literal at 856,302), the running process and `--version` print stay `[UNK]` |
| `corpus/README.md:121-128` "Compiled host binaries stay `[UNK]` (a pacman.log pkgver is a log line, not a running-binary fact)" | S096 | **narrowed**: first half now has a file-byte row for walker; the parenthetical stays true and stays in the text |
| `corpus/README.md:91-93` "Historical errata and record debt remain dated: … §5/F1–F5; Walker candidate errata in r9 §8" | S097 (R18-V1), S098 (R18-V4) | **partial, outside the bullet's named sets** — the two retirements must be named in the new round-19 bullet; the bullet itself is not closed |
| `corpus/README.md:88-90` "Note rows do not make proposed gate rows executable" | gate `live.walker.version` re-pin | **no advance** — moving a pin is not a new landable row |
| `corpus/README.md:82-84` rendered UI / Waybar text / Walker socket protocol / dispatcher | none | **no advance**; S096 runs and connects to nothing |
| `corpus/README.md:129-135` "Still open: runtime theme application … rendered UI" | S097/S098 | **no advance** — both repairs are durability, not behaviour |
| `:85-87`, `:94-96`, `:97-120` | none | unchanged |

Leads: the current `## Leads (unopened)` block holds only round-12 seat notes and
says nothing about walker, so round 19 appends the first walker block (draft §5).

## 2. Ordered study path (drafted `## Paths` line)

`S096 → S090 → S078 → S079 → S098 → S073 → S091` — host bytes at the moved pin,
then the log line that dates the move (never a binary fact), then the tag's
declared version and whole-tree tarball, then the dependency that tag's own
`Cargo.lock` checksums, then the packaged default table that is byte-equal to the
host `/etc/xdg` file, then the host user-config bytes. Every step is a file or tag
digest; the running process, `--version` print and provider behaviour stay `[UNK]`.

Verified for that path (all read-only):

- S098 is real and strictly stronger than S084: `xdg 3.0.0` crate tarball
  `https://static.crates.io/crates/xdg/xdg-3.0.0.crate` → 200, **15,821 B**,
  sha256 `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`,
  **equal to walker v2.17.2 `Cargo.lock:2708` checksum**
  (`.ufo/waves/round-18/fetch/MadoR18.SrcWalkerThemes/cargo-lock.txt:2705-2708`).
  Extracted in `/tmp`, the claimed search order is documented in-crate at
  `src/base_directories.rs:447-449` ("Searches `XDG_CONFIG_HOME` and then
  `XDG_CONFIG_DIRS`"), i.e. S084's `teaches` cell survives verbatim under a pinned
  body. Receipt: `.ufo/waves/round-19/fetch/FrontierRows/receipts.jsonl`.
- S096's anchor (from the sibling draft `drafts/HostWalkerBytes-row.md`): literal
  `2.17.2\n` at **856,302**, package `desc` `%VERSION%` `2.17.2-1`, binary sha256
  `2524065…`, `/var/log/pacman.log:2929`. `/usr/bin/walker` re-hashed here:
  `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`.
- The default-table delta `v2.17.0 → v2.17.2` is 9 changed lines
  (`blur_corner_radius`, `[niri]` table, `edit` binding, clipboard `remove`
  `after = "SimpleDelete"`); every default the round-5/9 notes cite
  (`close_when_open`, `theme`, `max_results`, prefixes) is unchanged in value —
  so the pin sweep is a date/pointer fix, not a value rewrite. [OBS from the
  round-18 bodies in `fetch/SrcWalkerChangelog/`]

## 3. Facts L1 should not miss

1. **S094's scope cell is literally false**: `ls -1 ~/.local/share/omarchy/themes/
   | wc -l` → **19** payload dirs (matte-black … white); "the only theme on this
   host" is true only for the *applied* theme. The theme note already qualifies it
   (`corpus/knowledge/theme-route-r18.md:162`); S097's scope must say "applied
   theme", not copy the old cell.
2. **Coverage-map shorthand breaks with S098/S097**: `corpus/README.md:44`
   (`source:` S072–S091) and `:45` (S092–S095) become non-contiguous ranges after
   the support rows change; draft §6 gives the replacement strings.
3. **The note's `XD` anchor key still points at docs.rs `latest`**
   (`corpus/knowledge/walker-route-r18.md:36`). Landing S098 without switching the
   note's `source:` header, `XD` key and `recheck:` leaves an unpinned support
   line behind a fixed-looking registry.
4. **`fresh-pins.py` accepts any `S\d{3}`**: closure review must require the
   pointer row to be S090/S091/S096 (matches `gen_w1.py`'s `RevFreshPinsCounter`
   brief), otherwise a wrong citation scores as current.
5. **New lead worth holding**: `/etc/pacman.d/hooks/walker-restart.hook` — named at
   `pacman.log:3062`/`:3123` but absent from every package file list
   (`grep -l walker-restart /var/lib/pacman/local/*/files` → no hit), so it is
   operator-local and unread; it is the only artifact that could say what the
   upgrade did to the service. Host theme count and hook path were read as file
   bytes/dir listings only.

## Limits

- S097/S098 row text was not available to check (only S096's draft existed on
  disk); ids are cited as the round contract reserves them.
- The frontier bullet's "every owned file carries …" is conditional on the sweep
  measuring 13/13; paste the measured form only.
- Did not read the pacman hook's bytes, did not fetch omarchy tree object ids,
  did not run rubric V, the census, or any gate mode.
- README/SOURCES line numbers are as at `9c54c56` and shift with any insert above.

## Installs

none.
