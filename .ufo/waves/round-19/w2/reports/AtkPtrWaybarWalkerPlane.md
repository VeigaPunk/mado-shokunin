# MadoR19.AtkPtrWaybarWalkerPlane — holds

Target: the round-19 appended block in `corpus/knowledge/waybar-walker-plane.md`
(committed lines 477-484), tip
`01b80946d92b26370d3012a7da655d00dd135154`. All note bytes were read with
`git cat-file blob 01b8094:corpus/knowledge/waybar-walker-plane.md` (29,796 B,
sha256 `0cea1d3d8d2ca4adbddf1d5f4da0d8e8e4449096910a05890ab3b144410cb616`);
`git status --porcelain -- corpus/knowledge/waybar-walker-plane.md` is empty, so
worktree == tip for this file. No gate, no walker/waybar invocation, no
process/systemd/compositor inspection; read-only git and file-byte reads only.

## (a) Pre-existing bytes and the documented head `source:` swap

Commands and outputs:

- `git diff --unified=0 9c54c56 01b8094 -- corpus/knowledge/waybar-walker-plane.md`
  yields exactly one hunk, `@@ -475 +475,10 @@`; the sole `-` line is the old
  final line with `\ No newline at end of file`, re-emitted with a newline.
- Old blob: 28,392 B, sha256 `c5d7a3ebff9e68ac47ab462de1bfa7ee229c98a8e3a80df5ac5924dd62e77bfa`.
  New blob: 29,796 B, sha256 `0cea1d3d…410cb616`.
  `git cat-file blob 01b8094:<file> | head -c 28392 | sha256sum` →
  `c5d7a3eb…e62e77bfa` (equal to the old blob). `cmp -l old new` prints nothing:
  the old file is a strict byte prefix of the new one; the append adds 1,404 B.
- This note has **no** `source:` head line (`grep -n '^source:'` → no match), so
  there is no head token that could have been swapped here. The documented swaps
  are confined to the two route notes, verified by line-1 sha256 and token grep:
  `walker-route-r18.md:1` S084 replaced by S098 (`c6f1b9e9…` → `57601ed7…`; the
  old token survives only inside the new parenthetical `supersedes S084, round
  19`), `theme-route-r18.md:1` S094 replaced by S097 (`1b11642c…` → `52c8efd8…`;
  S094 survives only in `supersedes S094, round 19`).

**Answer (a): no pre-existing content byte was changed.** The only byte-level
effect on the old body is the EOF newline the old file lacked; it is inserted
between the old final `.` and the new heading and is recorded by the writer as an
edit-tool side effect (`w1/reports/PtrWaybarWalkerPlane.md:24`). The new file
again ends without a trailing newline (last bytes `…stays [UNK].`).

**Provenance defect F1 (wave-level, not a false sentence).** The committed append
is not the byte sequence the w1 seat hashed:
`PtrWaybarWalkerPlane.md:20` records after = 29,729 B / sha `69d1096c7b68…85f9aa`
and `:23` records the append as 1,337 B / tail sha `0a2d0f2664…289329`; committed
are 29,796 B, sha `0cea1d3d…10cb616`, append 1,404 B, tail sha
`339398a41d1279f2e1b77d723627ad2f27fe9815df997ce34716bdc27dfa0558`. The eight
sibling notes whose blocks I cross-checked all have committed sha256 equal to
their w1 report hash (`walker-deep`, `walker-deep-r9`, `waybar-walker-semantics`,
`walker-live-surface`, `remaining-planes-census`, `config-health-report-r3`,
`arc-synthesis`, `closeout-r11`); this note is the sole mismatch.

The 67-byte delta is exactly the two CriticC2-directed hedges
(`w1/reports/CriticC2.md:37-42`, `:126`):

- `not valid for 2.17.2` (20 B) → `not re-verified on 2.17.2` (25 B): **+5**
- `make that PID stale` (19 B) → `make that PID likely stale [INFERENCE: S090
  records hook runs, not process state]` (81 B): **+62**
- sum **67** = 29,796 − 29,729, with line/newline count unchanged (484 lines,
  483 newlines) — [INFERENCE] those two substrings are the only edits; no other
  sentence in the block moved. The w1 receipt was not re-cut after the fix, so the
  committed block has no matching receipt of its own. This does not falsify any
  sentence: both replacement clauses are true (walker was not run this round;
  S090 is a log-line row).

## (b) Live/runtime claims and "re-verified"

- `grep -n 're-verified'` over the block returns only the negative
  (`:480`), and `:484` explicitly leaves 2.17.2 behaviour `[UNK]`. No sentence
  calls anything re-verified or re-measured.
- No sentence claims a 2.17.2 runtime fact. Positive current-state claims and
  their support:
  - "the host package moved to 2.17.2" — `/var/log/pacman.log:2929`
    `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`;
    `/var/lib/pacman/local/walker-2.17.2-1/desc` `%VERSION%` = `2.17.2-1`; no
    later walker package line after `:2929` (only the two `walker-restart.hook`
    runs at `:3062`, `:3123`). This is package/log state, not runtime state.
  - "walker-route-r18.md records the same sha prefix … on 2026-10-20 as a
    file-bytes read" — route note exists (25,722 B), head source URLs are
    v2.17.2, `verified-at: 2026-10-20` ("host bytes read with cat/sha256sum/stat/
    grep only"), and its Host declaration row gives the full
    `fecf71fa4253803e…3d1787` (1,336 B / 49) at `walker-route-r18.md:180`.
    I independently re-hashed the host file: `sha256sum
    ~/.config/walker/config.toml` → `fecf71fa…3d1787`, 1,336 B, 49 lines,
    mtime 2026-10-03 17:44:32; it matches the note's `:21` row and bullet `:482`.
  - "Current routing: corpus/knowledge/walker-route-r18.md" — the file exists and
    is the v2.17.2 documentary route.
- The only live-state sentence is hedged as required: PID 1808 "likely stale
  [INFERENCE: S090 records hook runs, not process state]" (`:481`). The note's own
  R4 errata at `:410-412` already says the round-1 PIDs no longer resolve, so
  "superseded" does not rest on this round's observation at all.
- The w1 DeltaWalkerCli work shows the `walker --version` print and the rendered
  `--help` bytes were not re-run (host pause), so "not re-verified" is accurate.

**Minor classification defect F3.** Bullet `:480` groups the `walker --help`
*flag list* (`:196-197`) under "Version-bound". `w1/reports/DeltaWalkerCli.md` §3
proves the 23-flag set is byte-identical across the releases (838-byte
description run, sha256 `e429efc3…`, at 2.17.0 offset 819,030 and 2.17.2 offset
832,855); what can move is the rendered help framing, which is GLib-bound
(glib2 2.88.3-1→2.90.1-1, `pacman.log:2554`). The flag list is therefore
version-independent; only the rendered output is environment-bound. The
sentence's operative clause ("not re-verified") stays true, so this overstates
version dependence rather than asserting a false target fact.

## (c) Line numbers cited by the block

Measured on the committed blob (`grep -n '2\.17\.0'` pre-existing hits are
exactly 38, 197, 405; `awk` dump of each cited line):

| cited | actual content at that line | verdict |
|---|---|---|
| `:38`, `:197`, `:405` | `2.17.0` literal (continuation; end of help OBS; R2-E4 version list) | correct |
| `:196-197` | `walker --help` exposes `--provider`, `--set`, `--inputonly`, … | correct |
| `:31-33` | `ps … 1707,1706,1808,1815`, PIDs, `STARTED Tue Oct 13 11:02:07 2026` | correct |
| `:172` | `Main PID: 1808 (walker)` | correct |
| `:404` | `PIDs 1707/1706/1808/1815 all STARTED Tue Oct 13` | correct |
| `:181` | `systemctl --user is-enabled elephant.service` → `enabled` | correct |
| `:21` | user config row: 49 L / 1336 B / `fecf71fa4253803e` | correct |
| `:37-40` | version prints 37-39 (waybar/walker/hypridle/hyprlock/swayosd); `:40` is mako | superset (F2) |
| `:169-188` | contains launcher `:178-180` and restart `:182-185`, but starts at the systemd-unit OBS `:169` and its `Main PID` `:172` | superset (F2) |

No cited line is wrong. **F2 (minor):** `:169-188` begins in the unit/process
state that bullet `:481` itself classifies as dated (the launcher/restart anchors
are `:178-185`), and `:37-40` includes mako at `:40`; both ranges are over-broad
but contain the claimed anchors.

## (d) S-row support

The block cites exactly one row, S090, four times. `corpus/SOURCES.md:102`:
scope "host /var/log/pacman.log (walker and elephant upgrade lines)", grade A,
status `mined`, anchors `1943`, `2929`, `3062`, `3123`, `3095`, support note "a
log line is not a running-binary fact". Host file bytes at those lines:

- `:2929` walker `2.17.0-1 -> 2.17.2-1` (2026-10-20T09:16:46-0300)
- `:3062` / `:3123` `running 'walker-restart.hook'...` (09:18:25 / 09:31:04)
- `:3095` elephant `2.21.0-1 -> 2.22.1-1` (09:31:03)

Every citation lands exactly, and the block's `[INFERENCE: S090 records hook
runs, not process state]` mirrors the row's own limit. "Elephant 2.21.0 to 2.22.1
… is not pinned in this note" is true: the note contains no `2.21`/`2.22` string
(`grep` → only the block's own clause), and `w1/reports/HostElephantBytes.md:70`
records the same conclusion. No S094/S084/S096 token appears in the block, so the
rejected/pending-row hazards do not apply here.

## Verdict

**holds** — I could not falsify a single sentence in the appended block. The
pins are correctly located, the version moves are correctly attributed to S090
and the host log, every cited line number resolves, and the two runtime-adjacent
clauses are explicitly dated/`[INFERENCE]`/`[UNK]`. Findings are confined to
provenance and precision:

- **F1** (medium, wave provenance): committed block ≠ w1-verified bytes
  (29,796 vs 29,729 B; sha mismatch); the 67-byte delta is exactly the two
  CriticC2 hedge fixes, so no unaccounted text changed, but the seat receipt was
  not re-cut and no blob of the old 29,729-B state exists in the object database
  (scan of blobs of that size containing "Freshness pointer" → none; therefore
  the mapping is arithmetic inference, not a recovered diff).
- **F2** (minor): over-broad line ranges `:169-188`, `:37-40`.
- **F3** (minor): "version-bound" applied to the `--help` flag list is
  contradicted by DeltaWalkerCli's byte-identical flag set; the rendered help is
  GLib-bound, so only the "not re-verified" hedge is defensible.

## Limits

- Host pause honoured: no `ps`/systemd/compositor/walker/waybar invocation; PID
  1808's live state was not observed, so the `[INFERENCE]` in the note is neither
  confirmed nor refuted here. No gate run.
- The 67-byte attribution to the two CriticC2 edits is [INFERENCE] from exact
  byte arithmetic plus the critic's explicit fix list; the pre-edit blob is not
  recoverable from the lane's git objects.
- `walker-route-r18.md`'s host declaration was checked for sha/date provenance and
  the config file was independently re-hashed, but the route note's other host
  rows were not re-read (out of scope).
- Only read-only git was used; nothing in the lane was modified except this
  report.

## Installs

none
