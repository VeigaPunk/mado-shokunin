# ConnStalePinsSweep — corrections sweep for walker 2.17.0 / elephant 2.21 / packaged-config `5b4e47b7` (round 18, wave 2)

Seat: `MadoR18.ConnStalePinsSweep`, wave 2 (FALSIFY), 2026-10-20. Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Write scope: this report only.
Read-only lane: no git/jj write, no package query, no service/process/socket/
compositor/input probe; host config trees read as bytes.

## Verdict

The corpus notes have absorbed the move; the operating manual has not. Two claim
sites are present-tense and now false: **`SKILL.md:23`** (the global pin line,
`walker 2.17.0`) and **`SKILL.md:114`** (plane-map launcher row, `walker 2.17.0`
and packaged table `298 L`). Both need an erratum. Every other hit is either an
explicitly dated measurement (the 2026-10-14 pass) or an explicit old-value
record inside the round-18 authority; none needs an erratum. Several dated lines
are copy-paste recipes or window-local conclusions whose expected output or reach
is now different and should be re-baselined before reuse, but that is a citation
hazard, not a claim.

## Authority and independent confirmation

`corpus/knowledge/walker-route-r18.md` §Host declaration (`:173`) and §MOVED pins
(`:232`) record old → new. I re-read the same host bytes on 2026-10-20; they
reproduce the new values exactly:

| artifact | old (2026-10-14 notes) | new (host, read 2026-10-20) | authority |
|---|---|---|---|
| walker package | `2.17.0-1` | `2.17.2-1` | `walker-route-r18.md:222`, `/var/log/pacman.log:2929` |
| elephant package | `2.21.0-1` | `2.22.1-1` (the `elephant-*` splits listed at `pacman.log:3095-3119` moved in the same run) | `walker-route-r18.md:226`, `pacman.log:3095-3119` |
| `/etc/xdg/walker/config.toml` | 13,220 B / 298 L / `5b4e47b7…` / mtime 2026-07-26 | **13,743 B / 305 L / `3c5c6867…` / mtime 2026-10-08** | `:237-239` + sha/`wc` read below |
| `/usr/bin/walker` | 6,661,264 B / `64826a85…` / mtime 2026-07-26 | **7,039,912 B / `25240650…` / mtime 2026-10-08** | `:240-241` + sha/`stat` read below |
| embedded default config offset | 784,064 | 806,960 | `:242` |
| `~/.config/walker/config.toml` | 1,336 B / 49 L / `fecf71fa…` | unchanged, same sha | independent read |
| help shas, BuildID, version-literal offset | `ca4820a8…`, `b513c43f…`, `0945536c…`, BuildID `a22452d1…`, literal 847,791 | not recorded in the r18 note; `[UNK]` here | — |

Commands and observed output (read-only):

```
$ sha256sum /etc/xdg/walker/config.toml /usr/bin/walker ~/.config/walker/config.toml
3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b  /etc/xdg/walker/config.toml
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker
fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787  /home/vgpnk/.config/walker/config.toml
$ wc -lc /etc/xdg/walker/config.toml
305 13743
$ stat -c '%n %s %y' /etc/xdg/walker/config.toml /usr/bin/walker
/etc/xdg/walker/config.toml 13743 2026-10-08 11:14:32.000000000 -0300
/usr/bin/walker 7039912 2026-10-08 11:14:32.000000000 -0300

$ grep -n 'upgraded walker\|upgraded elephant' /var/log/pacman.log
1943:[2026-10-11T16:14:39-0300] [ALPM] upgraded walker (2.16.2-1 -> 2.17.0-1)
2929:[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
3095:[2026-10-20T09:31:03-0300] [ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)
```

The `walker-restart.hook` runs at `pacman.log:3062` (09:18:25) and `:3123`
(09:31:04), but no process probe is permitted, so running-binary identity is
`[UNK]` (see § Limits). The mtimes are package build times, not install times;
do not date the move by mtime, date it by `pacman.log:2929/3095`.

## Classification rule applied

- **D — dated**: the containing file or section carries a pass date or
  verification stamp (`Measured 2026-10-14…`, `verified-at:`, `Probe window:`,
  `Appended 2026-10-14 18:48Z`) and the line is that pass's measurement.
  Historical; cite with the date. No erratum.
- **D-h — dated, hazard**: as D, but the line is a copy-pasteable recipe whose
  expected output or offset is now different, or a window-local conclusion that
  reads as standing. No claim erratum; re-baseline or re-date before reuse.
- **PT — present-tense**: the containing section advertises itself as the current
  pin set or current operating table, with no pass date. Now false. Erratum
  required.
- **OK**: the line is the round-18 authority itself, a `pacman.log` line, or an
  explicit old-value record.

Borderline calls are named in § Contradictions.

## Present-tense — erratum required

| path:line | stale claim (verbatim fragment, ≤25 words) | why present-tense |
|---|---|---|
| `SKILL.md:22-23` | "Version pins for all claims below: … walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified `hyprctl version`)." | Top-of-manual binding pin, no date of its own; the note says "all claims below" |
| `SKILL.md:114` | "packaged table `/etc/xdg/walker/config.toml`, 298 L — MADO-R3-1 §6" … "walker 2.17.0 via `app-walker@autostart.service`" | Current plane-map row (scope picker), no date; both the version and the line count are stale |

Stale facts and replacements: walker `2.17.0` → `2.17.2` (pkg `2.17.2-1`); packaged
table `298 L` → `305 L` / `13,743 B` / `3c5c6867…`; elephant is absent from the
pin line entirely (the moved `2.21.0` → `2.22.1` is invisible in `SKILL.md`).

## Dated inventory — every other hit line

### `SKILL.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 1075 | `2.17.0`; `64826a85…` | round-7 append "Appended 2026-10-14 18:48Z", stage (c) | D |
| 1473 | `64826a85…` | §Walker findings — M9-2 digest (round-9 append) | D |
| 1475 | `2.17.0-1` | same M9-2 digest | D |
| 1476 | `2.17.0` literal | same M9-2 digest | D |

### `corpus/README.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 135 | "2.17.0-era" | explicit "dated, not current" disclaimer | OK |

### `corpus/knowledge/arc-synthesis.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 229 | `2.17.0`; `64826a85…` | round-10 ledger, walker row cites `(r9)`; header "verified-at: 2026-10-14" | D |

### `corpus/knowledge/closeout-r11.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 43 | `2.17.0` | `verified-at: 2026-10-14 21:23–21:35Z`, every number re-run at that revision | D |

### `corpus/knowledge/config-health-report-r3.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 900 | expected `2.17.0` in a command comment | "Probe window: 2026-10-14 14:40–14:48 UTC"; runnable recipe | D-h |

### `corpus/knowledge/remaining-planes-census.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 246 | `walker 2.17.0-1` | round-6 probe window; §5 "Era caveat: all PIDs/timers are point samples" | D |

### `corpus/knowledge/walker-deep-r9.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 30 | `2.17.0` | header "Measured 2026-10-14 19:59:02–20:01:39Z" | D |
| 57 | `6,661,264`; `64826a85…` | §1 binary row | D |
| 58 | `2.17.0` | §1 printed version | D |
| 60 | `2.17.0-1` | §1 package row | D |
| 64 | `13,220`; `5b4e47b7…` | §1 config layers | D |
| 69 | `784,064` | §1 embedded-default re-check | D |
| 78 | `2.17.0` | §2 literal | D |
| 103 | `2.17.0-1` | §2 identity chain | D |
| 110 | `2.17.0` | §2 rodata run | D |
| 111 | `2.17.0` | §2 literal | D |
| 122 | `64826a85…` | §3 unknown 1 | D |
| 180 | `784,064` | §4 census table | D |
| 291 | `784,064` | §7 "**identical; no pin MOVED**" (true only for the 2026-10-14 window) | D-h |
| 305 | `2.17.0` | §9 recipe 1 | D-h |
| 316 | `2.17.0`; offset 847,791 | §9 recipe 4 | D-h |
| 317 | `2.17.0` | §9 recipe 4 | D-h |
| 334 | `784064` | §9 recipe 9 | D-h |
| 344 | `64826a85…` | §10 stability table | D |
| 345 | `5b4e47b7…` | §10 stability table | D |
| 369 | `64826a85…` | § Unknowns 4 | D |

### `corpus/knowledge/walker-deep.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 27 | `2.17.0`; `2.17.0-1` | "§1 Live snapshot (this pass)"; header measured 2026-10-14 17:00–17:25Z | D |
| 28 | `2.21.0`; `2.21.0-1` | same live snapshot | D |
| 68 | `784,064` | §2.1 layer table | D |
| 69 | `298 L`; `13,220`; `5b4e47b7…` | §2.1 layer table | D |
| 587 | `5b4e47b7…`; `13,220` | §12 identity table | D |
| 604 | `784064` | §12 recipe 1 | D-h |

### `corpus/knowledge/walker-live-surface.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 19 | `2.17.0` | claim opens the note; header measured 2026-10-14 18:20:44–18:23:13Z | D |
| 37 | `2.17.0-1`; `64826a85…` | §1 binary row | D |
| 38 | `2.17.0` | §1 version row | D |
| 43 | `6,661,264` | §1 package files | D |
| 113 | `784,064` | §3 layer table | D |
| 114 | `5b4e47b7…`; `13,220` | §3 layer table | D |
| 258 | `784064` | §7 recipe 3 | D-h |
| 277 | `5b4e47b7…` | §7 stability table | D |
| 299 | `2.21.0` | §8 unknown 4 | D |
| 301 | `64826a85…` | §8 unknown 5 | D |

### `corpus/knowledge/waybar-walker-plane.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 38 | `2.17.0` | header "Measured 2026-10-14 on host `vgpnk`" | D |
| 197 | `2.17.0` | same dated pass, help/version section | D |
| 405 | `2.17.0` | same dated pass, summary line | D |

### `corpus/knowledge/waybar-walker-semantics.md`

| line | stale value(s) | frame | class |
|---|---|---|---|
| 23 | `2.17.0`; `2.17.0-1` | header "Measured 2026-10-14 on host `plazir27`" | D |
| 24 | `2.21.0-1` | same dated pass | D |

### `corpus/knowledge/walker-route-r18.md` (the authority — no erratum)

| line | value | role | class |
|---|---|---|---|
| 13 | `2.17.0` | historical reference to the older notes it supersedes | OK |
| 60 | `2.17.0` | help text is the older measurement | OK |
| 221 | `2.16.2-1 -> 2.17.0-1` | quoted `pacman.log:1943` | OK |
| 222 | `2.17.0-1 -> 2.17.2-1` | quoted `pacman.log:2929` | OK |
| 226 | `2.21.0-1 -> 2.22.1-1` | quoted `pacman.log:3095` | OK |
| 238 | `13,220`; `5b4e47b7…` | §MOVED pins, old side | OK |
| 240 | `6,661,264`; `64826a85…` | §MOVED pins, old side | OK |
| 242 | `784,064` | §MOVED pins, old offset | OK |
| 243 | `2.17.0`; `2.21.0` | §MOVED pins, old side | OK |

## Contradictions, scope gaps, and non-claims

1. **Intra-repo contradiction.** `corpus/README.md:44` advertises "Walker v2.17.2
   and elephant v2.22.1", while `SKILL.md:23/114` — the first document a fresh
   agent reads — says `2.17.0`. Nothing in `SKILL.md` points to the round-18
   route, so the manual itself has no path out of the stale pin.
2. **The disclaimer is narrower than the moved set.** `README.md:135` says "the
   2.17.0-era pins in the round-5/9 Walker notes are dated, not current." It does
   not name `SKILL.md` (the present-tense sites), and it names a narrower set
   than the notes that carry the pins:
   `walker-live-surface.md` is round 7 and `waybar-walker-plane.md` is MADO-2.
   Both are dated by their own headers, and `walker-route-r18.md:237-241` binds
   the round-7 note explicitly, but the README sentence alone would let a reader
   think the round-7 note is current.
3. **"Recorded, not edited" leaves the erratum unowned.** `walker-route-r18.md:232`
   says the moved pins are "recorded, not edited here" (S015 protocol). That is
   correct for the dated notes, but it means the `SKILL.md` correction has no
   carrier in this round; this report is the inventory for it.
4. **`walker-deep-r9.md:291` is a citation trap, not a false claim.** "**identical;
   no pin MOVED**" is true only for the 2026-10-14 19:59–20:01Z re-check. Quoted
   without its date it reads as a standing conclusion and directly contradicts
   `walker-route-r18.md:237-244`.
5. **Dated recipes will now return different bytes.** `config-health-report-r3.md:900`
   (`walker --version` → `2.17.0`), `walker-deep-r9.md:305/316-317/334`,
   `walker-live-surface.md:258`, `walker-deep.md:604` are literal commands with
   pinned output. The method still works (the embedded config is still findable by
   the `force_keyboard_focus = false` marker), but the offsets and version bytes
   moved. Re-baseline, do not rewrite as history.
6. **Elephant is a gap, not a stale claim.** No present-tense `2.21` claim exists
   in `SKILL.md`; the only `2.21.0` mentions are dated notes
   (`walker-deep.md:28`, `waybar-walker-semantics.md:24`,
   `walker-live-surface.md:299`) and the `pacman.log` line in the r18 note. If
   `SKILL.md` is corrected, add `elephant 2.22.1-1` once, or state it as `[UNK]`
   because no process probe was run.
7. **Running state is not established.** The restart hooks at
   `pacman.log:3062/3123` fired, but the process state after them is `[UNK]` (no
   `pgrep`, no `/proc`, no socket). The erratum must say packaged/binary identity,
   never "the running launcher is 2.17.2".
8. **Borderline calls, stated so L1 can disagree cheaply.** `walker-live-surface.md:19`
   ("on this host `walker` 2.17.0 is installed") and `walker-deep.md:27` (§1 "Live
   snapshot (this pass)") use present-tense phrasing, but each sits under a dated
   2026-10-14 measurement stamp and is that pass's observation; classified D. If
   the lane's rule is instead "any present-tense verb needs the date on the same
   line", they become PT and the cheap fix is a date citation, not a value
   rewrite. `arc-synthesis.md:229` is a synthesis but its header binds it to the
   round-10 window and the walker row cites `(r9)`; `SKILL.md:1475-1476` is a
   digest of a dated note inside an otherwise current manual — both classified D
   on the same rule. Only `SKILL.md:23` and `:114` lack any date or pass frame.

## Proposed move (bounded, for L1 — not applied; `SKILL.md` is outside my write scope)

Replace the pin fragment at `SKILL.md:22-23` (keep the surrounding sentence):

```
walker 2.17.2 (pkg 2.17.2-1; `/usr/bin/walker` sha256 `25240650…`; elephant 2.22.1-1;
moved 2026-10-20, `/var/log/pacman.log:2929,3095`; the 2.17.0 pin of MADO-1 §9 and
MADO-2 §1, and the 2.21.0 pin of the round-5 note, are dated; running process `[UNK]`)
```

Replace the two stale facts in the `SKILL.md:114` row:

```
`~/.config/walker/config.toml` (49 L, `fecf71fa…`; packaged table
`/etc/xdg/walker/config.toml`, 305 L / 13,743 B, `3c5c6867…` — MADO-R3-1 §6's
298 L / `5b4e47b7…` superseded 2026-10-20) | walker 2.17.2 via
`app-walker@autostart.service` + `elephant.service` (`elephant` 2.22.1-1) …
```

Optional precision, not an erratum: extend `README.md:135` from "round-5/9" to
"round-2/5/7/9" (or "pre-round-18") and name `walker-route-r18.md` §Host
declaration as the current pin. If the lane insists on append-only for
`SKILL.md`, add the dated erratum block **and** a one-line pointer at `:22`
("pins moved 2026-10-20 — see §Round-18 erratum"), because a reader who stops at
the top of the manual is the failure mode.

Do **not** edit the dated notes to the new values: that would turn a dated
measurement into an undated one and break the evidence chain. The r18 note's
old/new table is the correct form.

## Axes and risk

- **Affected axes**: calibration (the manual's pin text is claim-bearing; C1's
  lesson citations can inherit it), freshness (this is the file-plane pin drift
  the round-18 walker note detected), coverage (a P3 route is being joined to a
  host declared at a version the manual denies). Operability, depth and
  adjacency are untouched: no tool, gate or capability changes.
- **Risks**: (a) scope — only L1 can apply this; (b) over-claiming running
  identity; (c) fixing the version but leaving `298 L` (or vice versa) splits the
  row; (d) a blanket replacement of `2.17.0` would rewrite the dated round-7/9
  append lines and the recipes; the replacement is only `:23` and `:114`.

## Verification for the erratum

Before: `grep -n '2\.17\.0\|298 L' SKILL.md` → `23`, `114`, `1075`, `1475`,
`1476` (the last three are dated history and must remain).

After the proposed edit, expect: no `2.17.0` at `23` or `114`; `2.17.2` at both;
`305 L` at `114`; and `grep -n '2\.17\.0' SKILL.md` still returns `1075`, `1475`,
`1476` (proving the edit did not touch history). Re-check the new values against
`sha256sum /etc/xdg/walker/config.toml` (`3c5c6867…`), `wc -lc` (`305 13743`) and
`/var/log/pacman.log:2929/3095`.

## Limits

- `[UNK]`: running walker/elephant binaries. No process, socket, service or
  package-query probe was run; `pacman.log` lines and file bytes are the only
  basis.
- `[UNK]`: the 2.17.2 BuildID, help-blob shas and version-literal offset. The r18
  note does not record them and I did not fetch or execute the binary.
- No upstream re-fetch: tag-pinned values are taken from the r18 note, which
  carries the committed receipts; I did not re-download them here.
- Scope was exactly `SKILL.md`, `corpus/README.md`, `corpus/knowledge/*.md`.
  `SCORECARD.md`, `LOG.md`, `reports/` and `corpus/SOURCES.md` were not swept and
  may carry the same strings.
- No file other than this report was written. No package manager, `sudo`,
  `systemctl`, `journalctl`, `hyprctl`, `walker`, `elephant`, `omarchy-*`,
  socket connect or screenshot/input probe ran; no git/jj command ran in the lane.
