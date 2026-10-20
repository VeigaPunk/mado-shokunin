# MadoR19.AtkReadmeFrontier — partial

Attack target: the round-19 bullet in `corpus/README.md` `## Frontier`
(`corpus/README.md:136-149` at `01b80946d92b26370d3012a7da655d00dd135154`),
the new `## Paths` entry (`corpus/SOURCES.md:148-156`) and the round-19
Search-log note (`corpus/SOURCES.md:296-306`). Worktree `corpus/` was clean
against the tip (`git status --porcelain corpus/` empty; `git diff --stat`
against the tip for both files empty).

Verdict: **partial**. Every fact I could re-derive from file bytes and fresh
fetches holds — S096 reproduces to the byte, the 13-file denominator is exact,
the Paths ordering matches the cited rows, and S097/S098 are durable,
content-addressed replacement rows. Two statements do not hold at the tip:
(a) two of the "13 pointed files" say S096 is *not* recorded, contradicting
the same bullet and the row it points at, and the C2 checker scores those
false lines green; (b) the "same-morning moves the walker sweep does not
cover" parenthetical names 3 of the 10 moved package classes its own cited
source lists.

## Axes tried

1. Count recut: enumerate the C2 denominator independently at `9c54c56`.
2. Byte recut: re-hash `/usr/bin/walker`, its rodata literal, `.rodata`
   bounds, pacman `desc`/`mtree`, and every S090 log line.
3. Upstream recut: fresh `curl` of the tagged walker Cargo.toml/lock/tarball,
   config default, xdg crate, omarchy tag/tree/colors, docs.rs 3.0.0 page.
4. Pointer semantics: read every pointer line the checker accepts, against
   the row-status it claims.
5. Supersession: S094/S084 statuses, propagation into the routing notes,
   and the `Paths`/Search-log claims about them.

## Findings that break or overclaim

### F1 — two of the 13 "dated pointers" deny the row they point at (false at the tip)

`corpus/README.md:137-140` says walker's binary bytes are "a mined host row
(S096 …)" and that "the 13 owned files that said `2.17.0` carry dated pointers
to S090/S091/S096 or a re-pinned value". At the same commit:

- `corpus/knowledge/remaining-planes-census.md:338`:
  “… on 2026-10-20 the host package moved to 2.17.2 per
  `/var/log/pacman.log:2929` (S090); the binary-bytes row S096 **is reserved
  and not yet recorded**.”
- `corpus/knowledge/walker-live-surface.md:305`:
  “… the host binary bytes **are reserved as S096 (row pending, not re-read
  this round)**.”

But `corpus/SOURCES.md:108` records S096 with status `mined`, and its
`used-by` names exactly those two files:

```
$ git show 01b8094:corpus/SOURCES.md | sed -n 108p | rev | cut -c1-260 | rev
...| mined | 2026-10-20 | on-change | corpus/knowledge/walker-deep.md,
corpus/knowledge/walker-deep-r9.md, corpus/knowledge/walker-live-surface.md,
corpus/knowledge/remaining-planes-census.md, tools/mado-verify.sh, SKILL.md |
```

The contradiction was created by the same commit that added the row, and never
repaired:

```
$ git log --oneline -S'S096 is reserved' -- corpus/knowledge/remaining-planes-census.md
df84807 round-19: wave-1 integration (... S096-S098 rows, S084/S094 rejected; walker pointers; ...)
$ git log --oneline -S'row pending, not re-read this round' -- corpus/knowledge/walker-live-surface.md
df84807 round-19: wave-1 integration (...)
$ git diff --stat df84807 01b8094 -- corpus/knowledge/remaining-planes-census.md corpus/knowledge/walker-live-surface.md
(empty)
```

The wave-1 seat reports show why: they wrote the pointers at `17661e0` when
S096 did not exist (`PtrWalkerLiveSurface.md:18`, `PtrRemainingPlanesCensus.md:24`,
`PtrArcSynthesis.md:35`, `QualityDraft.md:39` all say “S096 is reserved”), and
integration added the row without updating the pointer text.

Why the C2 number does not catch it: `fresh-pins.py` asks only for a line that
holds `2.17.2` and an `S###` token (`POINTER = re.compile(r"2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2")`),
and both stale lines satisfy it via `2.17.2 … (S090)` — census `:338` even
carries the literal `S096` inside the denial. The tool therefore reports both
files `current`, giving the green 13/13:

```
$ python3 -I .ufo/waves/round-19/fresh-pins.py 01b80946d92b26370d3012a7da655d00dd135154
 "denominator": 13, "current": 13, "score": 10.0
 rows: walker-live-surface.md current=true pointer_lines [305]
       remaining-planes-census.md current=true pointer_lines [338, 340]
```

So the sentence "the 13 owned files … carry dated pointers to S090/S091/S096"
is mechanically true (each line carries the tokens), but two of the pointers
assert S096 does not exist while `README:137` and `SOURCES:108` assert it does.
At the tip the census/live-surface text is the false half. This is a
false-green in the measure the README cites, not a miscount. [INFERENCE] the
intent of the bullet ("pointer layer is current") is not met for 2/13.

### F2 — the uncovered same-morning moves list is incomplete against its cited source

`corpus/README.md:146-148`: “the same-morning moves the walker sweep does not
cover (elephant 2.21.0 → 2.22.1, uwsm 0.26.7 → 0.27.1, hyprland pkgrel
0.56.2-2 → -4; w1 `PacmanLogMoves`)”. The three named moves are real — log
lines `:3095`, `:2926`, `:2733` respectively — but the cited w1 report lists
more:

```
PacmanLogMoves.md:1  "22 province packages upgraded (incl. 12 elephant plugins),
hyprwayland-scanner removed, and the C2 counter sees only one of them"
PacmanLogMoves.md §2 table: hyprtoolkit :2729 0.5.4-5 -> 0.6.0-1 (minor),
hyprland-guiutils :2730, hyprland-preview-share-picker :2736,
omarchy-nvim :2895, xdg-terminal-exec :2935, hyprwayland-scanner :3156 removed
PacmanLogMoves.md §3.5 "Moved packages with no corpus statement": the seven
above (hyprtoolkit 0.6.0 first)
```

Direct log check of the omitted entries:

```
$ sed -n '2729p;2730p;2736p;2895p;2935p;3156p' /var/log/pacman.log
[2026-10-20T09:16:38-0300] [ALPM] upgraded hyprtoolkit (0.5.4-5 -> 0.6.0-1)
[2026-10-20T09:16:38-0300] [ALPM] upgraded hyprland-guiutils (0.2.2-3 -> 0.2.2-4)
[2026-10-20T09:16:38-0300] [ALPM] upgraded hyprland-preview-share-picker (0.2.1-1 -> 0.2.1-3)
[2026-10-20T09:16:45-0300] [ALPM] upgraded omarchy-nvim (2026.8.13-1 -> 2026.9.21-5)
[2026-10-20T09:16:46-0300] [ALPM] upgraded xdg-terminal-exec (0.14.3-1 -> 0.14.3-2)
[2026-10-20T09:39:21-0300] [ALPM] removed hyprwayland-scanner (0.4.6-1)
```

`git grep hyprtoolkit -- corpus SKILL.md PROVINCE.md` at the tip = 0 hits, so
those moves genuinely have no corpus statement. Reading the parenthetical as
the set of uncovered moves is therefore an under-enumeration; it omits a
minor bump (`hyprtoolkit 0.5.4 → 0.6.0`) and a removal. If the intended scope
was "moves that left a stale corpus pin" the text does not say so.
[INFERENCE — high on the reading; the three named lines are individually
accurate.]

## What I could not break (verified, not recited)

### S096 as a mined host row — reproduces byte-for-byte

```
$ sha256sum /usr/bin/walker
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker
$ stat -c '%s %y' /usr/bin/walker
7039912 2026-10-08 11:14:32.000000000 -0300
$ readelf -n /usr/bin/walker | grep 'Build ID'
    Build ID: 19200fe47eb6c90fc4956f0d52d0c7c84bb89e99
$ readelf -SW /usr/bin/walker | grep .rodata
[12] .rodata PROGBITS 00000000000b6900 0b6900 074654 ...
$ grep -abo '2\.17\.2' /usr/bin/walker ; grep -abo '2\.17\.0' /usr/bin/walker | wc -l
856302:2.17.2
0
$ sha256sum /var/lib/pacman/local/walker-2.17.2-1/desc
5c0d9d89d3e8d6c433b89ebaf2bb8f11056e15cfaed69a430333e0b8d50b0928
$ grep -A1 '^%VERSION%' .../desc
2.17.2-1
```

Offset 856,302 lies inside `[0x0b6900, 0x0b6900+0x074654)` = `[747776, 1224532]`.
`desc` carries no `%SHA256SUM%`, but the package `mtree` does, and it equals
the on-disk binary: `./usr/bin/walker … size=7039912
sha256digest=25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`.
The row's “dates agree” clause also holds: `%BUILDDATE% 1791468872` =
`2026-10-08T14:14:32Z` = binary mtime; `%INSTALLDATE% 1792498606` =
`2026-10-20T12:16:46Z` = `pacman.log:2929` (09:16:46-0300).

### The 13-file denominator and the 2/13 → 13/13 move — exact

Independent enumeration (not the tool's code path): files under
`corpus/knowledge/*.md`, `corpus/README.md`, `SKILL.md`, `PROVINCE.md`,
`tools/*` at `9c54c56` containing `2.17.0` = **13** (SKILL.md, README.md,
arc-synthesis, closeout-r11, config-health-report-r3, remaining-planes-census,
walker-deep-r9, walker-deep, walker-live-surface, walker-route-r18,
waybar-walker-plane, waybar-walker-semantics, tools/mado-verify.sh).
`fresh-pins.py 9c54c56` → `current: 2, score: 1.5385`; at the tip →
`current: 13, score: 10.0`. The tool's own sha256 is
`a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789`
(the pre-registered `a094be01…`). Its `REV` argument is a placeholder; the
literal `… fresh-pins.py REV` exits 2 with `could_not_evaluate: rev REV` —
worth a one-word clarification in the README, not a false statement.

### `## Paths` (SOURCES:148-156) — every stage matches the cited row

Order S096 → S090 → S078 → S079 → S098 → S073 → S091 verified against the
rows and fresh bytes:

- S078 walker Cargo.toml @ v2.17.2: fetched 200, 952 B,
  `d1676045d1101a2d92c5669e54e36e63363d3e79dbc10c561662039ae2453a90`,
  `version = "2.17.2"` (line 3).
- S079 whole-tree tarball: codeload 200, 165,438 B,
  `e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56` —
  equal to the row.
- S098 xdg crate 3.0.0: 200, 15,821 B,
  `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`;
  walker v2.17.2 `Cargo.lock` (fetched 200, 70,247 B,
  `3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315`,
  equal to `fetch/SrcS084/walker-v2.17.2-Cargo.lock`) has the xdg block at
  `:2705-2708` with that checksum at `:2708`. Crate source:
  `find_config_file` doc `:447-448` “Searches `XDG_CONFIG_HOME` and then
  `XDG_CONFIG_DIRS`”, `read_file` `:757-777` checks the home path first then
  each dir, `config_home` default `:308`, `config_dirs` default `:321`;
  walker `src/config.rs:219` is exactly
  `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`
  (sha `93b6bd6f…` = receipt).
- S073 upstream resources/config.toml: 200, 13,743 B,
  `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`
  = host `/etc/xdg/walker/config.toml` (same sha, 305 lines).
- S091 user config `~/.config/walker/config.toml`: 1,336 B, 49 lines,
  `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`.
- S090 log lines all exact: `:1943` walker 2.16.2→2.17.0; `:2929` 2.17.0→2.17.2
  at 09:16:46; `:3062`/`:3123` walker-restart.hook; `:3095` elephant
  2.21.0→2.22.1.

### S097 / S098 durability — content-addressed identities reproduce

- Tag API: `GET /repos/basecamp/omarchy/git/ref/tags/v3.8.4` → `ref`, object
  `type=commit`, sha `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` — so S097's
  “lightweight tag” and commit are right. Tree `3fc08f95…` (fetched JSON,
  2,656 B) is `backgrounds` + 8 files, 9 entries, `truncated=false`.
- Raw colors.toml: 200, 461 B, `dbdd13a6…` = S097/S094 anchor; host
  `current/theme/colors.toml` has the same sha.
- Host state matches S097's scope correction: checkout HEAD `8fcc9d60…`,
  `describe` `v3.8.4`, `~/.local/share/omarchy/version` `3.8.3`,
  `current/theme.name` `matte-black`, 19 dirs under
  `~/.local/share/omarchy/themes`, `~/.config/omarchy/themes` empty;
  `current/theme` has 25 entries, consistent with S097's “12 payload files”
  (8 top-level + 4 background images) + “other 16” non-tag entries.
- S094 and S084 are both `rejected` (`SOURCES.md:96,:106`), and the head
  `source:` tokens were replaced in the routing notes:
  `theme-route-r18.md:167` (S094→S097) and `walker-route-r18.md:327`
  (S084→S098), each stating the rejection. `corpus/QUALITY.md:178-180`
  records the red→green swap (`S094 → S097, S084 → S098`).
- S098 anchors the *same text* at the crate source, not the docs page:
  `walker-route-r18.md:78-79` keeps historical `XD:n` docs line numbers and
  maps them to `base_directories.rs` defaults — I checked the mapping against
  the crate source and it is correct.

### Search-log note (SOURCES:296-306) — every factual clause holds

- “`/usr/bin/walker` holds one `2.17.2` literal and no `2.17.0`”: `grep -abo`
  counts 1 and 0. (Note: S096 itself says “0 hits”, also true.)
- “the walker v2.17.2 `Cargo.lock` named the exact xdg release and its
  checksum”: verified above at `:2705-2708`.
- “the `3.0.0` docs page … markup differs from `latest` and moves the quoted
  lines”: fresh fetch 200, 105,205 B, `adaec7c3…` versus the `latest` digest
  `0291cfe6…`; on the 3.0.0 page `XDG_CONFIG_HOME` default is `:299`
  (`XDG_CONFIG_DIRS` `:303`, `find_config_file` doc `:354`), versus the
  latest-page anchors `:302`/`:306`/`:356-358`. The committed receipts
  (`fetch/HtmlAnchorSweep/receipts.jsonl:11`,
  `fetch/MadoR19.UnpinnedUrlSweep/receipts.jsonl:5`) agree on the 3.0.0
  digest.
- “ArchWiki `oldid` raw URLs returned bot-challenge pages under HTTP 200 and
  were discarded (lesson M6)”: receipts lines 13/14/19 are
  `https://wiki.archlinux.org/index.php?title=Alacritty&oldid=869789&action=raw`,
  status 200, ~7,469 B, three different digests; `WITHHELD.md` names them as
  Anubis challenge bodies moved to `/tmp`, and `lessons/round-19.md` M6
  records the privacy incident. “Discarded” means not committed — the bodies
  were retained outside the lane.
- “For S094 a /tmp clone at the tag gave tree ids, which reproduce where
  GitHub tree HTML does not”: tag commit/tree ids verified above; the HTML
  non-reproduction is documented in `lessons/round-18.md` M7 and
  `HtmlAnchorSweep.md` finding A (7 distinct 200 digests for the tree URL).
- “Leads not opened this round: … `/etc/pacman.d/hooks/walker-restart.hook`
  (operator-local)”: no committed body or receipt for that path; the file
  exists (263 B) and only its log lines are cited. [UNK] whether any seat
  read it without committing — nothing in the committed evidence does.

### Gate sentence (README:148-149) — true as worded

`tools/mado-verify.sh:105` `WALKER_VERSION_PIN="2.17.2"`; the WL selftest
stubs `walker --version` and exercises PASS (2.17.2), FAIL (2.17.1) and
absent-binary arms, including `st_not_has … "2.17.0"`. The live row itself
does run `kv=$(walker --version)` when executed
(`mado-verify.sh:3276-3288`), so the row is a measurement *path*; but the
round-19 change was only the pin constant, and the gate was not run (host
pause), so “the re-pin is a pin, not a measurement” is accurate about the
change. [INFERENCE] a reader could over-read it as “the row measures
nothing”; the text is defensible.

## Limits

- Host pause respected: no gate, no pacman/systemctl/walker/waybar execution,
  no `~/.config/omarchy` hooks/extensions bodies. Host facts are file bytes
  (`sha256sum`, `stat`, `readelf`, `gzip -dc mtree`, log `sed`/`grep`) and
  read-only `git` in the omarchy checkout.
- The gate was not run; its claims here are read from committed bytes.
- Concurrent-drift note: `corpus/` was clean at start (`git status --porcelain
  corpus/ empty`), but at 15:07 local the worktree showed sibling edits to
  `corpus/knowledge/theme-route-r18.md`, `corpus/knowledge/walker-route-r18.md`,
  `corpus/QUALITY.md`, `SCORECARD.md` and `.ufo/waves/round-19/supersessions.json`
  (not mine). Every finding above was read from the `01b8094` blobs with
  `git show`, not from the moving worktree; re-check those two knowledge notes
  against the committed tip before quoting them.
- One GitHub API call returned `301` (232 B) without `-L`; retried with `-L`
  (200). All fetch bodies live under `/tmp/r19atk` only; nothing written to
  the lane except this report.
- “Still open: runtime theme application and wallpaper reload, Walker provider
  behaviour, the elephant service and wire schema, rendered UI”: no round-19
  committed evidence closes any of these (host pause; S097 says rendering/
  template consumption are outside the row). I could not probe otherwise.
- Findings F1/F2 are scope questions the owner must decide: F1 is a factual
  contradiction in the tree; F2 depends on whether the parenthetical was
  meant as examples or as the set.

## Fetch receipts (curl only, no auth; bodies in /tmp)

| url | http | bytes | sha256 | fetched_at (UTC) |
|---|---|---|---|---|
| https://static.crates.io/crates/xdg/xdg-3.0.0.crate | 200 | 15,821 | 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5 | 2026-10-20T18:04:32Z |
| https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.lock | 200 | 70,247 | 3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315 | 2026-10-20T18:04:32Z |
| https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.toml | 200 | 952 | d1676045d1101a2d92c5669e54e36e63363d3e79dbc10c561662039ae2453a90 | 2026-10-20T18:04:32Z |
| https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | 200 | 461 | dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786 | 2026-10-20T18:04:32Z |
| https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2 | 200 | 165,438 | e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56 | 2026-10-20T18:04:32Z |
| https://api.github.com/repos/basecamp/omarchy/git/ref/tags/v3.8.4 | 200 | 368 | a503d17da45fecbe7a5293c41d29a8b88fa0bf0f4b22293ca16f415f7ac9efd9 | 2026-10-20T18:05:22Z |
| https://api.github.com/repos/abenz1267/walker/git/ref/tags/v2.17.2 | 200 | 376 | 14147b773ad295a74e999ed36aded0403e868a4551c20a6d84cd2b4079a547de | 2026-10-20T18:05:22Z |
| https://api.github.com/repos/basecamp/omarchy/git/trees/3fc08f954e5a3f67072a79a7c52d94e0a153b9ec | 200 | 2,656 | 5772bc7c56cb1732657f75e72fec3670c78d60acf4e3384cbd6eab47267f21cf | 2026-10-20T18:05:22Z |
| https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml | 200 | 13,743 | 3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b | 2026-10-20T18:05:22Z |
| https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html | 200 | 105,205 | adaec7c32cc0595f59c154b407cf5a4ca85c6c40adf269a5046ccdd2b08762f6 | 2026-10-20T18:06:32Z |

## Installs

none
