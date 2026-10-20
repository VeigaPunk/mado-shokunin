# AtkPtrWalkerDeepR9 — partial

Target: the appended block `## Freshness pointer (round 19, 2026-10-20)`,
`corpus/knowledge/walker-deep-r9.md:401-408` at tip `01b80946…`. Worktree bytes equal the tip
blob (`sha256 502cb61dd7aea3935178db4cd8b14172255fcc1e0b1d6598a79291c4df2ebb75`,
`git status --porcelain` empty for the file). Read-only git; no lane writes except this report.

## (a) Pre-existing bytes beyond the documented `source:` swap — HOLDS

```text
$ git -C <lane> diff 9c54c56a… 01b80946… --stat -- corpus/knowledge/walker-deep-r9.md
 corpus/knowledge/walker-deep-r9.md | 11 ++++++++++-
 1 file changed, 10 insertions(+), 1 deletion(-)

$ python3  # git show of both blobs
base len 24391 tip len 25976
base is prefix of tip: True
extra bytes: b'\n\n## Freshness pointer (round 19, 2026-1'

$ grep -c 'source:'   # both revs -> 0
$ sha256sum worktree vs git show 01b80946:… -> identical, 502cb61d…
```

The whole baseline blob is a byte-exact prefix of the tip; the only addition is one `0x0a`
after the former last line (the file ended without LF) plus 1,585 B of block. The `1 deletion`
in `--stat` is only the `\ No newline at end of file` marker moving. **This file never had a
`source:` head** at either rev, so the documented head swap cannot apply to it; the swap is in
`corpus/knowledge/walker-route-r18.md:1` (its own correction at `walker-route-r18.md:327`
records S084 → S098). The worktree confirms it: the only dirty corpus files are exactly
`walker-route-r18.md` and `theme-route-r18.md`, each with a `-U0` hunk at `:1` (the head
`source:` token) and a tail append; `walker-deep-r9.md` is clean against the tip blob. No
pre-existing byte in `walker-deep-r9.md` changed.

## (b) Live/runtime claims and "re-verified" claims — HOLDS with one misattribution

- No sentence asserts a live/runtime fact about 2.17.2. The block's last bullet
  (`walker-deep-r9.md:408`) explicitly keeps behaviour `[UNK]`, and the S096 citation
  (`:403`) is a static file-bytes read.
- The one re-hash claim is genuine and reproduces (walker never executed):

```text
$ stat/sha256sum /usr/bin/walker
/usr/bin/walker 7039912 2026-10-08 11:14:32 -0300
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
$ python3 find
2.17.2 -> 856302 ; 2.17.0 -> -1
ctx …struct Action with 6 elementsversion2.17.2\ntoggle exact search…
$ sed -n '2929p' /var/log/pacman.log
[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
```

  Both match `corpus/SOURCES.md:108` (S096) and `:102` (S090) exactly.
- **Caveat**: `walker-deep-r9.md:404` puts "printed `--version` bytes" in the set
  "superseded for the host by S090 line 2929". A log line cannot carry a printed-output pin —
  S090's own row says "a log line is not a running-binary fact" (`SOURCES.md:102`). The block
  never states a new printed value, and `:408` keeps behaviour `[UNK]`, so this is
  misattribution, not a live-fact overclaim. `[INFERENCE]` the compiled literal plus §2.3's
  printed==literal argument make `2.17.2\n` near-certain, but it remains unobserved.

## (c) Cited line numbers — HOLDS

`git show 01b80946…:corpus/knowledge/walker-deep-r9.md | nl -ba`; `grep -n '2\.17\.0'`
returns exactly the ten cited lines plus the pointer body:

| line | content |
|---|---|
| 30 | §0 claim, "walker 2.17.0's version/shape" |
| 58 | §1 printed-version row `2.17.0\n` |
| 60 | §1 package row `walker 2.17.0-1` |
| 78 | §2.1 printed shape |
| 103 | §2.2 identity chain, package DB `2.17.0-1` |
| 110-111 | §2.3 literal provenance (`version` + `2.17.0` + LF) |
| 305 | §5.1 spot-check |
| 316-317 | §5.4 spot-check (`b.find(b'2.17.0')`, `…version2.17.0\n…`) |

Section refs also resolve: §1 line 59 = help-family row; §2.1-2.3; §5.1 at :304, §5.2 at
:307, §5.3 at :310, §5.4 at :314, §5.6 at :321, §5.9 at :330; "§1 config layers" is the table
row at :64. No off-by-one.

## (d) S### support — HOLDS

Only S090 and S096 are cited. Both rows exist at the tip and support their sentences:
S090 (`SOURCES.md:102`) lists line 2929 and I read that line; S096 (`SOURCES.md:108`) is
exactly the compiled literal + package identity and matches the current bytes above.
The printed-output caveat from (b) is the sole overreach; it is a wording/attribution defect,
not an unsupported row.

## Findings — what it overclaims

### F1 (main): the superseded set is incomplete; §3.3/§5.5 stay stale with no marker

`:404` names only the "rodata literal offset 847,791" among binary offsets as superseded. But
the note's §3.3 (`walker-deep-r9.md:175-184`) and §5.5 (`:320`) are equally version-bound, and
every one moved. Independent census of the current binary (`python3` find/re.finditer on
`/usr/bin/walker`):

| note | note value | current binary |
|---|---|---|
| `reload` offset | 791,458 (`:175`) | **814,881** |
| `Reload` count / first offset | 52 / 732,314 (`:176`) | **51 / 753,642** |
| `Reload` rows range | `:117-296` (`:176`) | **`:123-303`** (w1 DeltaWalkerConfig:83) |
| `FileSource` offsets | 732,448 / 822,835 (`:179`) | **753,808 / 836,239** |
| `failed to set loaded config` | 784,031 (`:180`) | **`Failed…` 806,884** (lowercase form absent) |
| `config not initialized` | 797,345 (`:181`) | **820,721** |
| `config.toml` / `WALKER_` | 797,284 / 797,295 (`:182`) | **820,703 / 820,714** |
| config-file error templates | 742,953 / 761,944 (`:183`) | **773,735 / 793,806** |
| `unknown_fields` | 828,369 (`:184`) | **870,078** |
| `(?i)notif` MIME offsets | 782,612 / 906,660 / 926,116 (`:173`) | **763,828 / 936,708 / 956,164** |
| `refresh` | 7 (`:177`) | **10 case-sensitive / 12 `(?i)`** |
| §5.5 spot-check "`Reload`=52" | `:320` | **51** |

w1 `DeltaWalkerConfig.md:169-188` says exactly this: "These … are now false and will be read as
false alongside §4 unless re-pinned", and lists the same old→new values; my census reproduces
all of them. The block is the file's only freshness marker, and the C2 counter cannot catch it:
`python3 -I .ufo/waves/round-19/fresh-pins.py 01b80946…` → `13 / 13`, score `10.0`, row
`corpus/knowledge/walker-deep-r9.md True [403]` — `POINTER` is a single-line regex
(`fresh-pins.py:19-23`), so line 403 alone credits the file. Lesson M3
(`corpus/lessons/round-19.md:18`) names that file-level limit and delegates the content check
to "reviewers read each pointer"; this is that read, and the pointer leaves a dozen
version-bound numbers looking current. (Side note, pre-existing: `:180`'s lowercase token is a
transcription error even for 2.17.0 — `DeltaWalkerConfig.md:191-196` — which the pointer also
does not flag.)

### F2 (secondary): "Not version-bound" understates voided host state

`:406` classes "PIDs, socket stat, layer rows" as not version-bound, dated 2026-10-14 and "not
re-measured this round". The 2.17.2 transaction and a reboot voided them:

```text
$ sed -n '3061,3064p;3122,3125p' /var/log/pacman.log
3062 [2026-10-20T09:18:25-0300] [ALPM] running 'walker-restart.hook'...
3063 [2026-10-20T09:18:26-0300] [ALPM-SCRIPTLET] Running as unit: run-p236822-i284703.service…
3123 [2026-10-20T09:31:04-0300] [ALPM] running 'walker-restart.hook'...
3124 [2026-10-20T09:31:04-0300] [ALPM-SCRIPTLET] Running as unit: run-p371567-i306456.service…

$ cat /etc/pacman.d/hooks/walker-restart.hook
Target = walker / walker-debug / elephant*
Exec = /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker

$ python3  # /proc/stat btime + /proc/<pid>/stat starttime
btime 1792501016 2026-10-20 09:56:56 -0300
walker PID 1858 start 09:57:12.8 ; elephant PID 1861 start 09:57:12.8
$ stat sockets
walker.sock 2026-10-20 09:57:13.737056297 -0300
elephant.sock 2026-10-20 09:57:13.715056299 -0300
```

The note's PIDs 1203471 / 1203474 (`:61`, `:63`), socket mtimes 13:11:09.144/.110 (`:65`), the
preamble's Hyprland session PID 1203316 (`:6`), the layer PIDs 1203358 / 1203352 (`:66`) and
the unit `ExecMainStartTimestamp` (`:62`) are all gone. The block does warn "not re-measured
this round", so it never asserts they are current; the defect is the category — the same S090
row it cites records the restart hook (`SOURCES.md:102` lines 3062/3123), and a reboot
replaced the session, so these are **void**, not merely unverified. `[INFERENCE]` on the exact
replacement path: the hook Exec + transient units + new PIDs/btime prove replacement; whether
the hook restarted `app-walker@autostart.service` itself versus a transient walker unit was not
observed.

## What I could not break

- The ten-line list is exact and complete for the `2.17.0` literal (grep is exhaustive).
- S090 line 2929 and S096's binary/literal/package bytes reproduce exactly.
- The block's unverified-but-checkable values are still right: user config sha
  `fecf71fa…` and autostart desktop sha `5cb9874e…` match current `sha256sum` output.
- The version-bound flags at `:405` are right: current `/etc/xdg/walker/config.toml` is
  13,743 B / `3c5c6867…`; current embedded offset is 806,960 (not 784,064).
- `:407`'s mechanism claim matches w1 `DeltaWalkerCli.md:268/:272` ("`src/config.rs` diff only
  adds merge arms for `[niri]`/`blur_corner_radius`"; "still one-shot") and
  `walker-route-r18.md:91-102`, including the whole-tree tarball search (S079).
- `[UNK]`: whether 2.17.2's `--version` bytes are `2.17.2\n` was not observed (walker barred).

## Limits

- Host pause honoured: no walker/elephant/pacman/systemctl/busctl/hyprctl execution; host
  surfaces read as file bytes only (`sha256sum`, `stat`, `python3 open`, `/proc/stat`,
  `/proc/<pid>/{comm,stat}`, socket stat). No gate run, no `jj`, no lane write except this
  report. Read-only git inside the lane.
- `[INFERENCE]` markers above for the restart→PID replacement and the printed-version value.
- F1's moved values are my own measurement plus w1's report; the note's row-range change
  (`:117-296` → `:123-303`) is w1-sourced only.

## Installs

none
