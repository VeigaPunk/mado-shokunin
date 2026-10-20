# MadoR19.AtkPtrRemainingPlanesCensus — breaks

Seat: `MadoR19.AtkPtrRemainingPlanesCensus` (wave 2, FALSIFY). Target: the round-19
appended block at `corpus/knowledge/remaining-planes-census.md:336-343`, tip
`01b80946d92b26370d3012a7da655d00dd135154`, baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.
All reads below are committed bytes (`git show <tip>:<path>`) or host file bytes; no lane edit,
no gate run, no live probe, no jj command.

Verdict in one line: the append-only byte discipline holds and no live walker-2.17.2 claim is
made, but two sentences are false against the same commit's own bytes (S096 "not yet recorded";
"were not re-measured this round") and one enumerates six packages on the wrong line.

---

## (a) Pre-existing bytes — HOLDS (EOF-only change)

Command:

```
git show 9c54c56:corpus/knowledge/remaining-planes-census.md | sha256sum
git show 01b8094:corpus/knowledge/remaining-planes-census.md | sha256sum
git show 01b8094:corpus/knowledge/remaining-planes-census.md | head -c 20512 | sha256sum
```

Output (OBS):

```
710e3e289643f2ff1ebb21522f662c31302bf06c6d467b3e110f49f0bb859f06  -   (old, 20,512 B)
b1016a4b6b36172021b3d3b2f9357dd8ea1926d19c9d1f07606be6e16b1e6d78  -   (new, 22,211 B)
710e3e289643f2ff1ebb21522f662c31302bf06c6d467b3e110f49f0bb859f06  -   (new[0:20512])
```

A byte-prefix scan found the common prefix is exactly 20,512 bytes = the full old blob
(OBS). The old last line had no trailing newline; the new file adds `\n\n` and 9 new lines
(`git diff --numstat` = `10 1`). No content byte above EOF changed. This note carries **no**
`source:`/`verified-at:` head at all (`grep -n '^source:\|^verified-at:'` on the tip blob →
rc=1), so the documented head-token swap does not apply to it. The two files that do carry the
documented in-place swap are correct at tip (OBS): `theme-route-r18.md` head `S094` → `S097`
and `walker-route-r18.md` head `S084` → `S098`, each with an append-only "Round-19 corrections"
block whose first bullet states the in-place head replacement.

[INF] The `1` deletion in numstat is only the no-newline marker; no pre-existing sentence,
number or hash was edited.

## (b) Live/runtime walker-2.17.2 claims — NO WALKER RUNTIME CLAIM (but two false provenance claims)

Honest attempt to find one: the block's walker sentences are log/registry statements. It says
"the host package moved to 2.17.2 per `/var/log/pacman.log:2929` (S090)" — the cited line
really reads `upgraded walker (2.17.0-1 -> 2.17.2-1)` (OBS, direct byte read), and S090 is an
accepted `mined` row whose locator lists exactly `2929, 3062, 3123` (`corpus/SOURCES.md:102`).
It explicitly refuses runtime claims: ":340 … no live walker process fact is re-asserted",
":343 … behaviour of the 2.17.2 binary stays [UNK]". The list in `:342` is true of the note:
`grep -n '25240650\|64826a85\|--help\|--version\|wc -l'` on the tip blob → rc=1, and the §1.3
table counts bytes, not lines (header `| File | B |`, `:80`). So no sentence claims a
2.17.2 runtime fact and nothing walker-runtime is called re-verified.

Two claims about *what was measured* are still false:

### B1 (hard) — "the binary-bytes row S096 is reserved and not yet recorded" (`:338`)

`corpus/SOURCES.md:108` at the tip is a live, accepted row:

```
| S096 | host walker version binding — `/usr/bin/walker` … + `/var/lib/pacman/local/walker-2.17.2-1/desc` … | code | A | … 7,039,912 B sha256 `25240650686fe…`, … literal `2.17.2\n` at file offset 856,302 … | … | mined | 2026-10-20 |
```

and `corpus/SOURCES.md:148` names it as the provenance-chain head:
`Walker version provenance (P3, round 19) — S096 → S090 → S078 → S079 → S098` (OBS).

The contradiction is self-inflicted in one commit (OBS):

```
git log --oneline 9c54c56..01b8094 -- corpus/knowledge/remaining-planes-census.md
  df84807 round-19: wave-1 integration (… S096-S098 rows …)
git show df84807:corpus/SOURCES.md | grep -c 'S096 | host walker version binding'   → 1
git show df84807:corpus/knowledge/remaining-planes-census.md | grep -n 'S096 is reserved' → 338
git log --oneline df84807..01b8094 -- corpus/knowledge/remaining-planes-census.md | wc -l → 0
```

So the row landed and the "not yet recorded" sentence landed in `df84807`, and no later commit
reconciled it. The w1 lane's own report confirms the draft predated the row:
`.ufo/waves/round-19/w1/reports/PtrRemainingPlanesCensus.md` §Limits — "The S096 binary-bytes
row does not exist yet; the block states it as reserved." The sibling `walker-live-surface.md:305`
carries the same stale wording ("reserved as S096 (row pending)"), so this is systemic, but the
census copy is the one under attack.

"reserved" is also not a registry state: `grep -n 'reserved\|reservation' corpus/SOURCES.md
corpus/README.md corpus/CONNECTIONS.md` yields only the substring inside `Preserves` in the S023
row — nothing reserves a row id (OBS). The intended meaning (host binary bytes were read by a
different lane, not by this note) is expressible without a false registry claim.

### B2 (hard) — "were not re-measured this round" (`:339`) is false, and two values it dates are host-stale

Host bytes, read directly (OBS):

```
2733 [2026-10-20T09:16:38-0300] [ALPM] upgraded hyprland (0.56.2-2 -> 0.56.2-4)
2926 [2026-10-20T09:16:46-0300] [ALPM] upgraded uwsm (0.26.7-1 -> 0.27.1-1)
2929 [2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
```

The same wave measured exactly the packages bullet 2 says were not re-measured:
`.ufo/waves/round-19/w1/reports/PacmanLogMoves.md:27` (uwsm `2926`), `:36` ("No move in the
window … waybar 0.15.0-3 (:1944), alacritty 0.17.0-1 (:639), hypridle 0.1.8-2 (:1792), hyprlock
0.9.6-3 (:1798), hyprsunset 0.4.0-3 (:855), mako 1.11.0-1 (:1024)…"), `:86` (census `:244`
hyprland `0.56.2-2` → `0.56.2-4`), and `:76-78` §3.3, titled "uwsm (`0.26.7` → `0.27.1`; **no
pointer anywhere**)", which names `remaining-planes-census.md:246` verbatim. That report is in
the same integration commit `df84807`.

Consequence at tip: the block itemises as "2026-10-14 pins" two host-false values —
`:244` `hyprland 0.56.2-2` (host `0.56.2-4`) and `:246` `uwsm 0.26.7-1` (host `0.27.1-1`) —
while denying the round that found them. The other eight in the list are confirmed unmoved, so
the word "not" is the whole defect: had it said "measured unchanged this round except …", the
bullet would be both true and useful.

## (c) Line numbers — numeric refs correct; line attribution wrong

Correct (OBS): note `:246` really holds `0.15.0-3 · walker 2.17.0-1 …`; `/var/log/pacman.log`
`:2929`, `:3062`, `:3123` are the walker upgrade and the two `running 'walker-restart.hook'…`
lines exactly as cited.

Wrong (OBS, `nl -ba` of the tip blob with `cat -A` to see the wraps):

```
244  - **Packages (shape).** hyprland 0.56.2-2 · hypridle 0.1.8-2 · hyprlock
245    0.9.6-3 · hyprsunset 0.4.0-3 · swaybg 1.2.2-1 · mako 1.11.0-1 · waybar
246    0.15.0-3 · walker 2.17.0-1 · alacritty 0.17.0-1 · uwsm 0.26.7-1 · sddm
247    0.21.0-7.
```

`:339` says "The other package versions **on that line** (hyprland, hypridle, hyprlock,
hyprsunset, swaybg, mako, waybar, alacritty, uwsm, sddm)…". Six of the ten are not on line 246:
hyprland and hypridle are on 244; hyprlock's value `0.9.6-3`, hyprsunset, swaybg and mako are on
245; sddm's value is on 247. Line 246 names only walker, alacritty, uwsm, sddm and carries
waybar's value token. Likewise "Version-bound, dated: line 246 only" reads as an inventory claim
while the package-shape list spans 244-247. The trailing "(walker 2.17.0-1 in the package-shape
list)" shows the intent was the walker token (true: `2.17.0` occurs on 246 and then only inside
this block), but the sentence as written attributes the wrong line to six packages.

Section anchors: `:341` "hyprsunset and hyprlock pins (§2, §4)" — §2 has the hyprsunset row
(`:167`) and §4 its night-light bullet (`:239-240`); the hyprlock *file* pin is at §1.3
(`:92`, `:101`) and §6 item 4 (`:315`), not §2/§4; §4 carries only the hyprlock package version
(`:244-245`). [INF] tolerable if "pin" means the version, but a reader seeking the hyprlock byte
pin in §2/§4 will not find it.

## (d) S-row support — S090 supports; S096 contradicts the sentence

- S090: supports both `:338` (`/var/log/pacman.log:2929`) and the `:340` hook lines `:3062`,
  `:3123` — each cited line was read at the stated number with the stated content (OBS).
- S096: cited at `:338` as "reserved and not yet recorded"; its tip row (`SOURCES.md:108`,
  status `A`, plus the `:148` chain) says the opposite. B1 above. This is the one citation in
  the block that fails (d).
- No other S### is cited in the block.

## (e) Additional coverage gap (inference, minor)

`:340` pairs "Walker process and CSS import rows" with "(§2 walker row, §4 clients)". The walker
PID 1203471 is §2 (`:164`); §4's Clients bullet (`:223-226`) contains no walker PID — it asserts
chromium 2552209's `ppid = walker's elephant provider 1203474`. That is a 2026-10-14 live fact the
bullet neither dates nor enumerates, and the same block's S090 evidence (`:3062`, `:3123`, plus
elephant `:3095-3119`) records the 2026-10-20 restart of exactly those processes. [INF] 1203474
is therefore likely gone and §4:224's ppid relation stale; the pointer's supposedly complete
walker-process dating misses the one §4 fact the upgrade invalidates.

## Summary

| Item | Result |
|---|---|
| (a) pre-existing bytes | holds — old blob is a strict byte prefix; only EOF newline + 9 appended lines |
| (b) walker 2.17.2 runtime claims | none made; `[UNK]` stated correctly |
| (b′) provenance claims | **breaks** — B1 (S096), B2 ("not re-measured this round" + two stale values) |
| (c) numeric line refs | correct (246; pacman.log 2929/3062/3123) |
| (c′) line attribution | **breaks** — six of ten packages not on line 246 |
| (d) S### support | S090 holds; S096 contradicted by its own recorded row |

Minimal repair (not applied): replace `:338`'s S096 clause with "S096 records the binary bytes
(sha256 `25240650…`, literal 856,302)"; replace `:339`'s last clause with "measured unchanged in
the 2026-10-20 window except hyprland pkgrel 2→4 (`:244`) and uwsm 0.26.7→0.27.1 (`:246`)
(S090; PacmanLogMoves)"; say "the package-shape list (`:244-247`)" instead of "that line".

## Limits

- Walker itself was never executed (host pause); no live PID, runtime or behaviour check. The
  2.17.2 binary identity is taken from the committed S096 row and the w1 `DeltaWalkerConfig` /
  `HostWalkerBytes` reports, not re-hashed by me.
- `/var/log/pacman.log` was read as file bytes only (python `open`), five cited lines; no pacman
  or log tooling was invoked.
- Host walker config first lines were read as bytes only to identify which `config.toml` §2:164
  anchors (`~/.config/walker/config.toml:3-4`, values match); no walker theme/user file was
  re-hashed here, so the §2/§6 pin currency is inherited from w1, not independently confirmed.
- I did not run `fresh-pins.py`, `tw-recall.py`, the gate or any gate copy; no git/jj writes.
- The "same commit" claim relies on `git log`/`git show` over the lane's refs; unreachable
  wave-1 draft commits outside the branch were not audited.
- [UNK] whether the lane intentionally ships a known-stale pointer and plans a w2 fix; the tip
  bytes are what is falsified here.

## Installs

none
