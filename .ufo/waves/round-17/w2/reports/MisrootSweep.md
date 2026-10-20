# MisrootSweep — fleet-root status census: what names mado/round-17, and whether any of it is a misroot

Seat `MadoR17.MisrootSweep`, scout, leaf (no subagent dispatch). Assignment: run
`git -C /home/vgpnk/Projects/shokunin status --porcelain`, list every untracked/modified path,
say for each whether its **content** names mado/round-17, move/delete nothing, write only this
report. Everything below is observed read-only from file bytes, git's index, and code.

**Verdict up front.** The attack failed: **no mado round-17 artifact is misrooted at the FLEET
root.** `git status --porcelain` at the fleet root returns 10 driver-owned paths — 1 modified
(`.ufo/watchdog.log`) and 9 untracked (`state/<lane>.report-baseline`) — plus one path that
appeared *during* this sweep (a concurrent agent's `scripts/hyaku/jj-lane.sh.new` staging file,
§1.1), which also does not name mado. Of those 11, only `watchdog.log` names mado and round 17,
and it is the driver's own append-only log. Two **instrument** facts did land (worth carrying to
the tripwire/claims work): the fleet census is structurally blind inside the lane
(`!! mado-shokunin/`) and is a moving target while other lanes run; and a fleet-root path tree
named after a shell error string already exists, invisible to `--porcelain`.

## 1. The enumeration (authoritative)

Command, re-run independently three times (plain, `-uall`; identical):

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/watchdog.log
?? .ufo/state/kaidoku.report-baseline
?? .ufo/state/kake.report-baseline
?? .ufo/state/kama.report-baseline
?? .ufo/state/mado.report-baseline
?? .ufo/state/mori.report-baseline
?? .ufo/state/souji.report-baseline
?? .ufo/state/tabi.report-baseline
?? .ufo/state/tameshi.report-baseline
?? .ufo/state/tsukuroi.report-baseline
```

`--porcelain -uall` returns the same 10 and `grep '^?? .*/\$'` is empty: no collapsed `?? dir/`
entry, so this listing is exhaustive at **file** granularity for non-ignored paths.

| # | Path | Kind | Bytes | mtime (-0300) | Content names mado? | round-17? |
|---|---|---|---|---|---|---|
| 1 | `.ufo/watchdog.log` | ` M` | 34562 | 2026-10-20 11:52:26.39 | **YES** (12 × `mado`, incl. line 480) | **YES**, `round=17` |
| 2 | `.ufo/state/kaidoku.report-baseline` | `??` | 68 | 2026-10-20 10:14:09.85 | no | no; round field `17` |
| 3 | `.ufo/state/kake.report-baseline` | `??` | 68 | 2026-10-20 05:51:50.28 | no | no; round field `21` |
| 4 | `.ufo/state/kama.report-baseline` | `??` | 68 | 2026-10-20 11:52:24.44 | no | no; round field `17` |
| 5 | `.ufo/state/mado.report-baseline` | `??` | 68 | 2026-10-20 10:51:17.87 | no | no; round field `17` |
| 6 | `.ufo/state/mori.report-baseline` | `??` | 68 | 2026-10-20 05:44:36.28 | no | no; round field `16` |
| 7 | `.ufo/state/souji.report-baseline` | `??` | 68 | 2026-10-20 10:51:16.37 | no | no; round field `16` |
| 8 | `.ufo/state/tabi.report-baseline` | `??` | 68 | 2026-10-20 10:51:14.32 | no | no; round field `16` |
| 9 | `.ufo/state/tameshi.report-baseline` | `??` | 68 | 2026-10-20 10:14:08.42 | no | no; round field `16` |
| 10 | `.ufo/state/tsukuroi.report-baseline` | `??` | 68 | 2026-10-20 05:43:24.11 | no | no; round field `16` |
| 11 | `scripts/hyaku/jj-lane.sh.new` | `??` | 29726 | 2026-10-20 11:56:20.48 | **no** (0 hits) | no |

Content test as run: `grep -c -i 'mado'` and `grep -c 'round-17'` over each file. All nine
baselines return `mado:0 round-17:0`. Their entire content is two whitespace-separated tokens,
`<round> <sha256>`, e.g. row 5 is literally:

```
17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

So the honest answer to "does its content name mado/round-17" for rows 2-10 is: **no string
match**; row 5 carries the numeric round `17` in field 1 and no lane name at all. Lane identity
lives only in the **filename**.

### 1.1 The census is volatile — row 11 appeared mid-sweep

At 11:56:20, seconds after my first census and my own report write, a **11th** path appeared:
`scripts/hyaku/jj-lane.sh.new`, 29726 B, owner `vgpnk`, `??`, not ignored. Facts:

- It is a staging rewrite of the **tracked** fleet helper `scripts/hyaku/jj-lane.sh`
  (12142 B, mtime 11:08, `git ls-files` = YES); `diff -q` says the two differ. The `.new`
  convention implies a same-directory atomic-replace in progress by another agent working on
  fleet tooling.
- Content: `grep -c -i 'mado'` = **0** and no `round-17`/`MadoR17` match. Its header describes
  lane-repo commits through Jujutsu; nothing in it is mado-specific.
- Its mtime is a single stable stamp (re-stat after ~1 min returned the identical
  `11:56:20.477205108`), so it is a completed staging write, not a file still growing.
- It is the only member of the staging class in status (`grep -E '\.(new|tmp|orig|rej|bak)$'` =
  this one line).

Within the same window other lanes committed (`tabi-shokunin/.git/{index,COMMIT_EDITMSG,}`,
`souji-shokunin/.git/*`, `souji-shokunin/tools/souji-seat-audit.py` all newer than 11:55). Those
are invisible to the fleet census for the reason in §4(a). **Consequence for any "the sweep shows
only …" claim: it must carry its timestamp and be re-run at the moment of assertion.** A fleet
census taken while siblings run is a snapshot, not an invariant — mine changed inside three
minutes. Row 11 is not mine, not mado's, and I left it untouched.

`watchdog.log` is the single content hit. Its uncommitted hunk is `@@ -472,3 +472,13 @@`
(10 appended lines), including line 480:

```
2026-10-20T10:51:22-03:00 launch mado round=17 pgid=2433501 driver=hyaku-inline attempt=1
```

plus the neighbouring `launch kama round=17...`, `launch souji round=16...`, `launch tabi
round=16...`, `launch mado round=17`, `complete kaidoku round=17`. Nothing else in the file's
diff names mado.

## 2. The one "YES" is driver provenance, not a seat write

Every one of the 10 driver paths (rows 1-10) is produced by `scripts/shokunin-watchdog.sh`:

- `:47` `UFO="$SHOKUNIN_ROOT/.ufo"` — the driver's `.ufo` is the **fleet** `.ufo` (root derived at
  `:35-46` from the script's own directory, `scripts/..`).
- `:120-138` `record_report_baseline()` writes `state="$UFO/state/$1.report-baseline"` with
  `printf '%s %s\n' "$n" "$digest"` through a `.tmp.$$` + `mv -fT` atomic replace — exactly the
  `"<round> <sha256>\n"` 68-byte shape observed. One field separator, one trailing newline:
  68 bytes for every file, including the one whose round is two digits.
- Call sites: `:203` inside `launch_lane` and `:364` on the advance-blocked retry path.
- `.ufo/watchdog.log` is the same script's `log()` sink; the appended lines are its `launch`/
  `complete` records.

Four independent checks that these are the driver's bytes and not a seat's:

1. **Code order matches mtime order.** In `launch_lane`, baseline is written at `:203`, the child
   `exec setsid` spawns at `:~216`, and `log "launch $lane round=$n pgid=$pid"` fires at `:221`.
   So baseline mtime must be *earlier* than the launch log stamp. Observed: mado baseline
   `10:51:17.871` vs `launch mado round=17` at `10:51:22` (+4s); kaidoku `10:14:09.85` vs launch
   `10:14:11`; tabi `10:51:14.33` vs `10:51:16`; souji `10:51:16.38` vs `10:51:17`; tameshi
   `10:14:08.43` vs launch `10:14:09`. All five interlock in the predicted direction.
2. **Round field agrees with the lane's last log event** for all nine lanes — kake 21/`complete
   kake round=21`, kama 17/`launch kama round=17`, kaidoku 17/`complete kaidoku round=17`, mado
   17/`launch mado round=17`, mori 16, souji 16, tabi 16, tameshi 16, tsukuroi 16, each matching
   that lane's last `launch`/`complete` line. A stale or hand-made file would have to reproduce
   all nine exactly.
3. **The digest is the empty-stream sentinel.** `e3b0c442…5b855` is `sha256("")`
   (`printf '' | sha256sum`, verified). That is precisely what `report_digest()` (`:108-118`)
   returns for a report that does not exist: "a missing report is the empty byte stream". So the
   baselines disclose **no** report bytes — there was nothing to hash. It also confirms mado's
   round-17 report did not exist at 10:51:17.
4. **First-time state, not tampering.** `.ufo/state` is tracked (64 files) and
   `git ls-files .ufo/state | grep report-baseline` is empty: no baseline was ever committed, so
   all nine are new driver artifacts rather than edits of tracked state.

Not exploitable as a completion signal: `report_of()` (`:142-163`) requires a `SHONEN` heading
**and** `MIN_REPORT_BYTES=400` (`:54`), so a missing/empty report can never satisfy it — the
empty-stream digest is a safe sentinel, not a free pass. (The digest alone does conflate "absent"
with "present but empty"; the byte floor and heading check remove the consequence.)

## 3. The misroot hypothesis, tested at every plausible root

| Probe | Result |
|---|---|
| `test -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-17` | **NO** — no fleet-root wave tree for this round |
| `test -e /home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mado.md` | **NO** — expected: mado r17 is still open (last mado log event is the 10:51:22 `launch`; `complete mado round=16` at 06:06:30) |
| lane `.ufo/reports/round-17` | **NO** — the lane's only report is `.ufo/reports/round-1/mado.md`; driver reports are fleet-side by design |
| `find . -maxdepth 4 -newermt '2026-10-20 10:00' -type f` outside the lane | 40 files: driver prompts (`.ufo/prompts/mado-round-17.md`, `.ufo/prompts/closure/*`), driver reports (`.ufo/reports/round-16,kama,tameshi`, `round-17/kaidoku.md`), the 6 new baselines, `watchdog.log`, `.ufo/waves/hyaku/PHASE2.md`, `.ufo/l0-questions.md`, plus other lanes' `kaidoku-shokunin/**`. **No mado seat artifact.** |
| `grep -rl 'MadoR17' .tower` | no match |

`RevengeM4Misroot`'s control observation ("`/home/vgpnk/Projects/shokunin/.ufo/waves/round-17/`
does not exist") is therefore **confirmed independently**, now with wave-2 seats already writing.

Files touched today that *do* name mado but are **not** in the status list, and why:
`.ufo/prompts/mado-round-17.md` (21322 B) and `.ufo/prompts/closure/mado-round-16.md` are
**tracked and unmodified** (`git ls-files --error-unmatch` = YES; last commits `5a228cd` and
`a6b8df5`, both 2026-10-20). Their fresh mtimes are checkout/commit artifacts, not working-tree
changes — so an auditor must not read their absence from `status` as "the prompt was never
generated".

## 4. Two instrument limits that DID land

These do not accuse any seat; they bound what a fleet census can conclude.

**(a) The fleet census cannot see inside the lane.** `.gitignore:1:*-shokunin/` matches
`mado-shokunin`, and `git check-ignore -v mado-shokunin` → `mado-shokunin`. With `--ignored=matching`
the entry appears as `!! mado-shokunin/`. Consequences: a fleet-rooted `status` proves nothing
about lane contents (either direction), and without `--ignored` the lane's existence is not even
reported. The lane must be censused separately — I ran `git -C mado-shokunin status --porcelain`:
5 untracked paths, all expected round-17 roots (`drafts/`, `evidence/measure-c3.json`,
`gen_w2.py`, `w1/reports/`, `w2/`), and no `round-17` under the lane's `.ufo/reports`. No stray.

**(b) Ignored strays are invisible to the assigned command — and one exists.** 37 ignored entries;
the only one naming mado is `!! mado-shokunin/`. But the list contains a genuine fleet-root path
tree whose **name is a shell error string**:

```
bash: /home/vgpnk/Projects/shokunin/souji-shokunin/
  bash: .../souji-shokunin/tests
    bash: .../souji-shokunin/tests/tools
      bash: .../tests/tools/souji-verify.sh: No such file or directory
```

mtime `2026-10-18 14:01:47.32`, i.e. **two days before round 17 launched**; the leaf is an empty
directory, and `grep -rl -i -E 'mado|round-17'` over the tree returns nothing. Its owner is
souji, not mado ([INFERENCE] from the path text). This is the M4 class in its purest form — a
command string becoming a filesystem path with no error — and `--porcelain` cannot show it,
because `*-shokunin/` swallows it. Per instruction I moved and deleted nothing; it belongs to
another lane's sweep.

## 5. False-positive trap to preempt (for tripwire and claims reviewers)

`.ufo/reports/round-N/<lane>.md` at the FLEET root is **canonical driver state**, not a misroot:
`shokunin-watchdog.sh:121` computes `f="$UFO/reports/round-$2/$1.md"` and `:199`
`mkdir -p "$UFO/reports/round-$n"`. Round 13, 14, 15, 16 each contain `mado.md`. Round 17 already
contains seven **other** lanes' files (`kagi`, `kake`, `kasegi`, `kotoba`, `kotodama`, `kumitate`,
`kaidoku`; `kaidoku.md` 14301 B, mtime 11:51, matching `complete kaidoku round=17` at 11:51:47) and
no `mado.md` because this round is open.

A containment rule that flags any fleet-root write to `.ufo/reports/**` would therefore
false-positive on the driver's own lifecycle, including the eventual `round-17/mado.md`. The M4
signature is narrower: a **lane-seat** write to `.ufo/waves/round-N/wK/reports/**` resolved
against the fleet cwd.

## 6. The hazard is still live in wave 2 (trailer form)

My own dispatch tail, read from `.ufo/waves/round-17/w2/dispatch.json`, is relative:

```
Report: write your scoped findings to .ufo/waves/round-17/w2/reports/MisrootSweep.md
```

`gen_w2.py:19` supplies the correction in Context only ("Every `Report:` trailer path is relative
to {LANE} — write it at {LANE}/<that path>. A relative path resolves to the FLEET root and is a
misroot"), and the fleet prompt discusses the same fix at `.ufo/prompts/mado-round-17.md:237-238`.
So `RevengeM4Misroot` **D2 still holds**: the last action-shaped sentence a seat reads is relative,
and containment depends on the seat also honoring a prose sentence. I wrote this file with the
absolute lane path. No misroot appeared this wave, but that is compliance, not prevention.

## 7. Compliance

- Installs: **none**. No `pacman`/`yay`/`paru` in any form (not even `-Q`/`-Si`/`-Sp`), no `sudo`,
  no `systemctl`/`loginctl`/`journalctl`/`hyprctl`/`libinput`/`evtest`/`wayland-info`/`hypridle`/
  `hyprlock`/`alacritty`/`waybar`/`walker`/`omarchy-*`, no `pgrep`/`pidof`, no `<binary> --version`,
  no device/compositor probes, no screenshots.
- Git: read verbs only (`status`, `diff`, `check-ignore`, `ls-files`, `log`). No add/commit/rm/mv,
  no `jj`. Nothing was moved or deleted; the only file written is this report.
- No delegation, no sibling files touched, no transcript or `~/.omp/agent/agent.db*` access.
- Commands run: the census above, `stat`/`cat`/`grep`/`find`/`sed -n` on driver code and state,
  `sha256sum`/`printf '' | sha256sum`. All read-only.

## 8. Confidence and remaining unknowns

| Claim | Confidence | Basis |
|---|---|---|
| The status list is complete at file granularity for its timestamp | high | four runs (10, 10 with `-uall`, 10, 11 after row 11 appeared), no collapsed `?? dir/`; completeness is per-instant only (§1.1) |
| Rows 1-10 are driver-owned, none a seat write; row 11 is fleet-tooling staging, not mado | high | writer function `:120-138`, call sites `:203`/`:364`, code-order vs mtime interlock, nine-way round agreement, `sha256("")` sentinel; row 11 has 0 `mado` hits and rewrites a tracked helper |
| No mado round-17 artifact at the fleet root | high for the probes named; medium for "nowhere at all" | `test -d` on the wave tree, `test -e` on the driver report, `find -maxdepth 4 -newermt`, `.tower` grep |
| Fleet census is blind inside the lane | high | `.gitignore:1:*-shokunin/`, `check-ignore`, `!! mado-shokunin/` |
| The bash-named fleet-root tree is souji's, pre-round-17 | medium ([INFERENCE]) | path text, mtime 2026-10-18, empty leaf |

Unknowns: whether any seat wrote **outside** both roots (`/tmp`, `$HOME`, elsewhere) — not
observable by this sweep and out of my item's scope; the `find` was bounded at depth 4, so a
deeper fleet-root file touched today would not appear (the git census would still catch it if
unignored); and `round-17/mado.md` does not exist yet, so its eventual path and bytes cannot be
compared against the trailer contract from this seat.
