# AtkPtrWaybarWalkerSemantics — partial

Attack on the round-19 appended block at the tail of
`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/waybar-walker-semantics.md`
(`## Freshness pointer (round 19, 2026-10-20)`, worktree = tip `01b80946`, lines 464–472;
the note has 472 lines with no final newline, so `wc -l` says 471 — no worktree/tip drift:
`git diff 01b80946 -- <file>` is empty and the worktree sha is `8412646f…`, the w1 "after"
hash).

**Answers to the four questions, each falsified where possible:**

- **(a) Pre-existing bytes — holds.** No pre-existing byte changed. The 38,083-byte baseline
  blob is an exact prefix of the tip blob; the sole `-` line in `git diff` is the formerly
  newline-less final line re-emitted with its new `\n`. No head `source:` token exists in this
  note to swap (`grep '^source:'` = 0 hits); the two documented head swaps are in
  `walker-route-r18.md:1` (S084→S098) and `theme-route-r18.md:1` (S094→S097), confirmed by
  `git diff` of those files.
- **(b) Live/runtime 2.17.2 claims — holds for live fact, breaks on provenance.** No sentence
  claims a live or runtime fact about the 2.17.2 binary; the only behaviour sentence is
  explicitly `[UNK]` (`:472`), and no sentence says "re-verified". But two sentences say the
  *opposite* of the round-19 evidence — "not re-checked against 2.17.2" (`:468`) and "not
  re-hashed this round" (`:470`) — and both are false at this tip; see F3/F4. One further
  sentence contradicts the block itself (`:471`, "§1-§5 make no walker-version claim").
- **(c) Cited line numbers — all correct.** Line 4 = "Measured 2026-10-14…"; line 23 = the
  walker row `walker --version` → `2.17.0`; pkg `2.17.0-1`; line 24 = elephant row pkg
  `2.21.0-1`; §6.1 table `:234` carries "298 lines"; `:47` and `:112` are the packaged-config
  anchors at `:248` and `:253`; §6.2/§6.3/§6.4/§6.5/§6.6/§6.7/§6.8 start at 238/257/269/279/294/316/344;
  §9 item 7 is `:417`; the §10 sha is `:445`. All verified with `nl -ba` on the worktree.
- **(d) S-row support — holds as far as it goes, sourcing is thinner than C2 declares.**
  S090 is the only row cited, and it supports both sentences verbatim (`corpus/SOURCES.md:102`
  lists `2929` walker `2.17.0-1 -> 2.17.2-1` and `3095` elephant `2.21.0-1 -> 2.22.1-1`; I read
  both log lines directly). But the note contains **zero** `S096`/`S091` tokens
  (`grep -c` = 0), while C2's declared text asks each pointer to cite "a SOURCES row opened
  this round for the host walker bytes (binary rodata version literal + file digest, read as
  bytes) and the upstream release" (`SCORECARD.md:1099-1104`). The file is credited only by
  the weaker mechanical rule (`2.17.2` + an `S###`). The w1 seat's stated reason ("S096 has no
  row yet") is stale at tip: `corpus/SOURCES.md:108` now carries S096.

## Commands and outputs

```text
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --numstat \
    9c54c56a6a7528675027b7f628f97a1b8d1b8e8d 01b80946d92b26370d3012a7da655d00dd135154 \
    -- corpus/knowledge/waybar-walker-semantics.md
10	1	corpus/knowledge/waybar-walker-semantics.md

$ sha256sum /tmp/base-knowledge-walker.md /tmp/tip-knowledge-walker.md
b92bee2cc69c95b921da8172b2bf15bca7248c40ef72f7b4acb12d9ab179e263  /tmp/base-knowledge-walker.md   (38083 B, last byte '.', no \n)
8412646f40b660f161ec1080e03c467d186b5573b947261bae79ef4179f860d6  /tmp/tip-knowledge-walker.md    (39539 B)
$ head -c 38083 /tmp/tip-knowledge-walker.md | sha256sum
b92bee2cc69c95b921da8172b2bf15bca7248c40ef72f7b4acb12d9ab179e263  -      ← prefix identity

$ awk 'NR==2929||NR==3095{print NR": "$0}' /var/log/pacman.log
2929: [2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
3095: [2026-10-20T09:31:03-0300] [ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)

$ sha256sum /etc/xdg/walker/config.toml /home/vgpnk/.config/walker/config.toml
3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b  /etc/xdg/walker/config.toml
fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787  /home/vgpnk/.config/walker/config.toml
$ wc -l /etc/xdg/walker/config.toml /home/vgpnk/.config/walker/config.toml
  305 /etc/xdg/walker/config.toml
   49 /home/vgpnk/.config/walker/config.toml
$ sed -n '22p;24,27p;174p;250p' /etc/xdg/walker/config.toml
blur_corner_radius = 20            # blur region radius on GTK older than 4.24; GTK 4.24+ uses the theme's .box-wrapper border-radius
[niri]
launch_on_empty_workspace = false # … requires walker to run as a service
launch_on_startup = false         # …
cmd_on_esc = ""                   # …
  { action = "edit", bind = "ctrl e" },
  { action = "remove", bind = "ctrl d", after = "SimpleDelete" },

$ grep -c "S091\|S096" corpus/knowledge/waybar-walker-semantics.md
0
$ grep -n "S0[0-9][0-9]" corpus/knowledge/waybar-walker-semantics.md
467:… moved to 2.17.2: `/var/log/pacman.log:2929` (S090). Current routing: …/walker-route-r18.md.
469:… S090 records elephant 2.21.0-1 -> 2.22.1-1 at `/var/log/pacman.log:3095`; …
```

## Findings

### F1 — (a) no pre-existing bytes changed (holds)
Baseline blob `b92bee2c…` (38,083 B) is an exact prefix of tip `8412646f…`; the appended
block begins after `\n\n`. The diff's `1 deletion` is only git re-emitting the old final line
because the old file ended without a newline (`corpus/knowledge/waybar-walker-semantics.md:463`
is byte-identical in both blobs). The sole head `source:` edits in round 19 are
`walker-route-r18.md:1` and `theme-route-r18.md:1`, as documented.

### F2 — (c) line numbers and section refs correct (holds)
`nl -ba` at tip: `:4` measurement date, `:23` walker pin, `:24` elephant pin, §6.1 at 230
(298-line row at 234), §6.2 at 238 (`:248` carries packaged `:47`, `:253` carries packaged
`:112-298`/`:112`), §6.3 at 257, §6.4 at 269, §6.5 at 279, §6.6 at 294, §6.7 at 316, §6.8 at
344, §9 item 7 at 417, §10 sha at 445. `§1` spans 18–65, so `:23` is inside `§1` (see F5).

### F3 — (b) `:468` "not re-checked against 2.17.2" is false; the packaged-default pin is known stale
Round-19 w1 measured exactly this: `.ufo/waves/round-19/w1/reports/DeltaWalkerConfig.md:107`
— "`waybar-walker-semantics.md:467-470` freshness pointer | flags 298/`:47`/`:112` as 'not
re-checked against 2.17.2' | measured: **305 L; `:53`; `:118`** — pointer's stale list is now
superseded"; headline `:1` "host L1 is now 305 L / 13,743 B / 3c5c6867 and the five notes' L1
pins are stale"; actionable `:200` "Re-pin L1 everywhere to `305 L … 3c5c6867…` (… semantics
234)". My own independent reads reproduce it: `/etc/xdg/walker/config.toml` = 305 lines,
sha256 `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`, with the four
2.17.2 semantics at `:22`, `:24-27`, `:174`, `:250`. So the note's 298 (`:234`) is not merely
unchecked — it is superseded, and the pointer names neither the new value (305) nor a row that
carries it. Against `corpus/QUALITY.md:183` ("carries … a pointer naming the new value and the
SOURCES row that superseded it") the *version* supersession (2.17.0→2.17.2) is named with
S090, but this value's replacement is not. [INFERENCE] on whether the line count counts as a
swept "present-tense value" under 28; it is a present-tense cell in §6.1 either way.

### F4 — (b) `:470` "not re-hashed this round" is false
The same round re-hashed the file to the same value:
`.ufo/waves/round-19/w1/reports/DeltaWalkerConfig.md:144-146` — "`~/.config/walker/config.toml`
**re-measured**: 49 L / 1,336 B / `fecf71fa…`, mtime 2026-10-03 17:44:32.097633418 -03";
`.ufo/waves/round-19/w1/reports/DeltaWalkerCli.md:237` — "L2 user `fecf71fa…`, 1,336 B |
UNAFFECTED | **re-read today**: same sha and size"; `.ufo/waves/round-19/w1/reports/RecheckSweep.md:98`
— "S091 … 3/3 digests match: `~/.config/walker/config.toml` `fecf71fa…`". My own
`sha256sum`/`wc` agree. The recorded sha is right; the provenance sentence is wrong (it
understates, and hides that §10's pin was confirmed unchanged at tip).

### F5 — `:471` "Waybar sections §1-§5 make no walker-version claim" is false on the block's own terms
The block's first bullet (`:467`) locates "the walker version pin … (line 23 only)" — and line
23 is inside §1 (18–65). One of the two sentences must be wrong; as written, §1 *does* carry a
walker-version claim (the pin). A reader taking `:471` at face value would treat §1–§5 as
walker-free on a future pass.

### F6 — `:471` "version-independent of the walker package" is wrong for the theme files' meaning
The theme files' *bytes* are omarchy-owned (`§6.6`), and w1 reports their pins unchanged
(`DeltaWalkerConfig.md:150-153`), but walker 2.17.2's change A moves the blur radius into the
theme on GTK ≥4.24: the new comment at `/etc/xdg/walker/config.toml:22` says "GTK 4.24+ uses
the theme's .box-wrapper border-radius", the host's gtk4 moved to 4.24.1 in the same
transaction (`DeltaWalkerCli.md:9-12`), and `§6.6:302-303` records `.box-wrapper` =
`alpha(@base,0.95)` + 2px `@border` — exactly the property that now sets the blur radius. So
the theme files' *interpretation* is version-coupled, the very distinction `:470` draws for
the user config. [INFERENCE] — the sentence is at best ambiguous; the `[INFERENCE]` tag is
correctly present but the conclusion is not supported.

### F7 — omission: superseded live state in §6.7/§6.8 is not flagged
`§6.7:318` ("`walker --gapplication-service` (PID 1808)") and `§6.8:348` ("Running? which
argv? sockets? … **OBS**") are 2026-10-14 point samples. S090 records `walker-restart.hook`
at `/var/log/pacman.log:3062` and `:3123` after the 2.17.2 install (`corpus/SOURCES.md:102`),
so PID 1808 cannot be current. The block folds §6.8 into "version-bound" and names only
scripts/keybinds for §6.7; it never marks the running-state claims superseded, unlike sibling
pointers that wrote "current PID `[UNK]`" (e.g. `.ufo/waves/round-19/w1/reports/PtrConfigHealthReportR3.md:11`).
The block makes no false live claim, but it leaves a known-superseded live claim unflagged.
[INFERENCE] on the restart replacing the PID.

### F8 — (d) S090 supports; but the pointer lacks the host-bytes/release sourcing C2 declares
S090 (`corpus/SOURCES.md:102`) is the only cited row and it supports both sentences (I read
`/var/log/pacman.log:2929` and `:3095` — exact match). However the note carries no `S096` or
`S091` token at all, and `SCORECARD.md:1099-1104` (C2) requires each pointer to cite "a SOURCES
row opened this round for the host walker bytes (binary rodata version literal + file digest,
read as bytes) and the upstream release"; `SCORECARD.md:1133`'s "Every credited line cites
S090/S091/S096" is satisfied only in the weak union sense. This file passes `fresh-pins.py`
on `2.17.2` + `S090` alone, so the metric does not enforce the declared sourcing shape. The
w1 seat's reason ("S096 … has no row in corpus/SOURCES.md yet",
`.ufo/waves/round-19/w1/reports/PtrWaybarWalkerSemantics.md:26`) no longer holds at tip:
`corpus/SOURCES.md:108` is the S096 row.

## Limits

- The item names no command to re-run; the independent checks were byte hashing/prefix
  identity, direct log-line and host-file reads (read-only file bytes under the host pause),
  and reading the w1 reports. No walker, gate, pacman, systemd or hyprctl command was run;
  no file in the lane was edited.
- Worktree = tip for this file was confirmed (`git diff 01b80946` empty; sha `8412646f…` =
  the w1 "after" hash). Nothing else in the lane was audited.
- Did not verify w1's theme-pin hashes; `DeltaWalkerConfig.md` contradicts itself there
  (":157-158 … sha256-compared all 16 … 16/16 identical" vs ":217 Packaged theme contents
  were compared by path list only"), so I relied only on its user-config, packaged-default
  and pointer-superseded statements, which are backed by my own reads.
- Whether 298/`:47`/`:112` are separate "values" under QUALITY 28 is [INFERENCE]; the
  lane's `supersessions.json` ledger sweeps only the version string `2.17.0 → 2.17.2`.
- §6.7/§6.8 live-state supersession (F7) is [INFERENCE] from the restart hooks; the post-hook
  PID is unobservable here (host pause).

## Installs

None. No tool was installed or upgraded.
