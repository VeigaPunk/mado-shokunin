# Reopen S066 — `hypridle src/core/Hypridle.cpp @ v0.1.8`

Lane: `mado-shokunin` @ `988b858bd6049bc709807534fd725c05264f7e60` (read only).
Assignment: re-open S066, verify URL / anchor quote / digest / tier / status / verdict, and
verify every claim the citing note (`corpus/knowledge/idle-lock-route-r17.md`) makes from
this source at the anchors it gives.

**Result: FALSIFIED — one hard defect.** The recorded SHA-256 is wrong by exactly one hex
character, in both `corpus/SOURCES.md:78` and `corpus/lessons/round-17.md:53`. Every other
checked facet (URL, quote at [HC:473], kind/tier/status/recheck, scope coverage, and all 25
unique `[HC:*]` anchors (28 citations) in the citing note) holds against the fetched bytes.

## Fetch — raw bytes

```
curl -sSL -o /tmp/hypridle-018.cpp \
  https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp
sha256sum /tmp/hypridle-018.cpp        # 2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75
wc -c /tmp/hypridle-018.cpp            # 29880
wc -l /tmp/hypridle-018.cpp            # 735
```

29880 bytes, 735 lines, LF only (a CRLF-normalized copy hashes identically). Four independent retrieval
channels plus eight archived copies agree:

| channel | bytes | sha256 |
|---|---|---|
| `raw.githubusercontent.com/.../v0.1.8/src/core/Hypridle.cpp` (tag) | 29880 | `2dd4d73d6f5cd…2b2d75` |
| `github.com/hyprwm/hypridle/raw/refs/tags/v0.1.8/...` (same tag, different host) | 29880 | `2dd4d73d6f5cd…2b2d75` (`cmp` identical) |
| `raw.githubusercontent.com/.../main/src/core/Hypridle.cpp` (today; main == tag bytes) | 29880 | `2dd4d73d6f5cd…2b2d75` |
| member `*/src/core/Hypridle.cpp` of `hypridle v0.1.8` tarball (`/tmp/hypridle-v0.1.8.tar.gz`, sha `08703613…`) | 29880 | `2dd4d73d6f5cd…2b2d75` |
| eight pre-existing seat copies under `/tmp` (`noteidle/`, `src-hypridle-v018/`, `p6q/`, `p6g/`, `p6att/`, `ap6/`, `ct17/`, `vb-Hypridle.cpp.bin`) | 29880 each | all `2dd4d73d6f5cd…2b2d75` |

No copy under `/tmp` or in the lane hashes to the recorded value.

## Hard defect — digest

- Recorded (`corpus/SOURCES.md:78`, anchor cell; `corpus/lessons/round-17.md:53`, gate):
  `2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`
- Observed: `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`
- Difference: one nibble at hex position 9 (0-based index 8): recorded `4`, actual `6`.
  63 of 64 hex characters are identical.

This is a transcription error, not a different byte-state. Any different content (tag move,
re-fetch divergence) produces an unrelated 64-hex digest; 63/64 identical nibbles cannot
arise from different bytes without a sha256 near-collision. `v0.1.7` hashes
`4f222dac…ac9a` (wholly different), and today's `main` equals the tag bytes.

Provenance of the typo — the correct value was computed and recorded upstream of the note:

- `.ufo/waves/round-17/w1/reports/SrcHypridleSrc.md:19-20` records 29880 B / 735 lines /
  `2dd4d73d6f5cd…2b2d75`, from a fetch repeated with `cmp` clean.
- `.ufo/waves/round-17/w1/reports/SrcIdleNotifyProto.md:87` records the same correct digest
  and `cmp`-equality with the tag tarball member.
- The one-character corruption appears in `.ufo/waves/round-17/drafts/NoteIdle-rows.md:15`
  and `:25` ("raw SHA-256 2dd4d73d4f5cd…") — the earliest artifact read that carries it
  (ordering is [INFERENCE]; creation times were not read) — then propagates to `corpus/SOURCES.md:78`,
  `corpus/lessons/round-17.md:53`, `.ufo/waves/round-17/gen_w2.py:50`, and the sealed w2
  prompt (which supplied the same wrong value to this check).

Consequences:
1. The round's own criterion — `lessons/round-17.md:39` "New rows (all opened 2026-10-20;
   quote ≤25 words; raw SHA-256)" — is not met for S066.
2. The row cannot byte-pin its source. A recheck that follows the note's own instruction
   (`recheck:` line: "re-fetch … compare raw SHA-256 with corpus/SOURCES.md S063-S069")
   fails today on S066.
3. The error is self-consistent between the brief, the draft, the row and the gate, so a
   brief→row comparison passes while both are wrong against the bytes. Only recomputation
   finds it.

## Facets that hold

| facet | claim | check | verdict |
|---|---|---|---|
| URL | `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp` | exact; HTTP 200; tag v0.1.8 exists (not a branch fallback) | holds |
| gate quote | `[HC:473]` `` `if (MEMBER == "Lock") {` `` (5 words, ≤25) | line 473 is exactly `    if (MEMBER == "Lock") {` | holds |
| kind / tier | `code` / `A` | `CORPUS.md:93` defines A as including "source code"; tag-pinned upstream implementation; consistent with sibling code rows S067/S068 | holds |
| status | `mined` | used-by cell names `corpus/knowledge/idle-lock-route-r17.md`; note exists and cites S066 at 25 unique anchors; S066 has no other used-by | holds structurally |
| recheck | `on-change` | consistent with tag-pinned upstream, but the pin value itself is wrong | holds as policy |
| opened | `2026-10-20` | today | holds |
| scope coverage | idle notifications, inhibits, dbus Lock/Unlock, PrepareForSleep, ScreenSaver registration, lock-notify | 70-79 + 298-328; 301/363-396; 465-488; 490-514; 626-666; 89-93/104-107/398-436 | holds |
| teaches | "inhibit gate before on-timeout; on-resume only after fired on-timeout; before/after sleep commands; ignore_dbus_inhibit gates ScreenSaver registration" | 301 before 327; guard 347 + clear 352; 499-510; gate 626 | holds |

No `verdict` column exists in the registry; admission is implied by `mined` + used-by and
the gate's "Admit: documentary P6 and P4 routes" (`lessons/round-17.md:29-30`). On content
the admission is sound; only the digest pin is defective.

## Citing-note claim audit — every `[HC:*]`

`corpus/knowledge/idle-lock-route-r17.md` line 1 lists the functions used from S066
(`setupDBUS`, `handleDbusSleep`, dbus Lock/Unlock, `onIdled`, `onResumed`, `onInhibit`,
`onLocked`, config reads) — all present: `onIdled` 298, `onResumed` 330, `onInhibit` 363,
`onLocked` 398, `onUnlocked` 418, `handleDbusSleep` 490, `setupDBUS` 599 (config values are
read via `g_pConfigManager->getValue` at 58, 109-111, 372, 402, 433, 467-468, 499-500,
600-601; there is no `load()` in this file).

| anchor | note claim | observed at anchor | holds |
|---|---|---|---|
| 58 | `ignore_wayland_inhibit` read in setup | `getValue<...>("general:ignore_wayland_inhibit")` | yes |
| 70 | `l.ignoreInhibit = r.ignoreInhibit` (from rule) | exact | yes |
| 71 | `l.conditionCmd = r.conditionCmd` | exact | yes |
| 74 | branch on `ignore_wayland_inhibit || r.ignoreInhibit` | exact | yes |
| 104-107 | warning text "Compositor is missing hyprland-lock-notify-v1!" / "general:inhibit_sleep=3, general:on_lock_cmd and general:on_unlock_cmd will not work." | both strings exact, 106-107 | yes |
| 120 | `inhibit_sleep` case 2 "auto" | `case 2: { // auto (...)` | yes |
| 128-129 | case 3 waits only `if (m_sWaylandState.lockNotifier)` | exact | yes |
| 301 | inhibit gate `m_iInhibitLocks > 0 && !pListener->ignoreInhibit` | exact | yes |
| 327 | `spawn(pListener->onTimeout)` | exact | yes |
| 346-348 | resume guard + "Skipping onResumed: onTimeout was inhibited for rule" | comment 346, guard 347, log 348 (message verbatim prefix) | yes |
| 352 | flag cleared | `pListener->onTimeoutFired = false;` | yes |
| 402 / 404 | `onLocked` reads `general:on_lock_cmd`, spawns it | read 402, `spawn(*LOCKCMD)` 404 | yes |
| 433 | `onUnlocked` reads `general:on_unlock_cmd` | exact (spawn 435) | yes |
| 473 | `if (MEMBER == "Lock")` | exact | yes |
| 477-478 | `spawn(*LOCKCMD)` if non-empty | guard 476, spawn 478 | yes |
| 480-485 | same pattern on `Unlock` | 480 `else if`, 485 `spawn(*UNLOCKCMD)` | yes |
| 493 | `PrepareForSleep` match | `if (MEMBER != "PrepareForSleep") return;` | yes |
| 504 | `cmd = toSleep ? before : after` | `std::string cmd = toSleep ? *SLEEPCMD : *AFTERSLEEPCMD;` | yes (see note 1) |
| 509-510 | spawned if non-empty | `if (!cmd.empty()) spawn(cmd);` | yes |
| 600 / 626 | `ignore_dbus_inhibit` read; false (default) runs the ScreenSaver registration block | read 600; `if (!*IGNOREDBUSINHIBIT)` 626, registration 627-666 | yes |
| 601 / 617 | `ignore_systemd_inhibit` read; gated | read 601; `if (!*IGNORESYSTEMDINHIBIT)` 617 | yes |

Presentation notes, not falsifications:

1. [HC:504] is rendered in backticks as `cmd = toSleep ? before : after`; the actual line is
   `std::string cmd = toSleep ? *SLEEPCMD : *AFTERSLEEPCMD;`. Semantics identical; the
   rendering is pseudocode, not verbatim.
2. [HC:74] "selects the inhibit-aware idle notification": the code selects
   `sendGetInputIdleNotification` (75-76) vs `sendGetIdleNotification` (79). The branch is
   exact, but "inhibit-aware" is an interpretive adjective; the input-idle request is the
   inhibitor-ignoring one. If read as "honors inhibitors" the gloss is reversed. Reword by
   naming the two requests.

## Weak or false corroboration

1. The citing note's provenance lines are false for S066. `verified-at:` says "raw SHA-256
   per source in `corpus/SOURCES.md` S063-S069", and `recheck:` says to compare raw SHA-256
   against those rows. The fetched copy archived in the note workspace (`/tmp/noteidle/hypridle.src_core_Hypridle.cpp`,
   29880 B; ownership [INFERENCE] from the co-located wiki HTML/README that match S063/S065) hashes `2dd4d73d6f5cd…`, not the recorded `…4f5cd…`. Either the comparison was
   not run for this row or its mismatch was not recorded.
2. `.ufo/waves/round-17/w2/reports/ReopenS067.md:93-94` states the `.cpp` "fetched in the
   same pass digests `2dd4d73d4f5cd…`, which equals S066's recorded digest". No fetched copy
   on this host hashes to that value (eight copies checked, all `…6f5cd…`). That sentence is
   copied from S066's row, not computed, so it is not independent confirmation of the tag
   bytes. (That report's own S067 digest was computed correctly.)

## Soft findings — anchors and tooling

1. `corpus/SOURCES.md:78` anchor set ends at `600-626`. The ScreenSaver registration itself
   (`sdbus::createSessionBusConnection("org.freedesktop.ScreenSaver")`, the `Inhibit` /
   `UnInhibit` vtable, paths) is at 627-666; even the "attempt to register as ScreenSaver"
   comment is line 627, outside the anchor. The scope item "ScreenSaver registration" is not
   inside the row's own anchor set. Extend to `600-666` (or add `626-666`).
2. `.ufo/waves/round-17/gen_w2.py:50` does not reproduce the row's anchors: it lists
   `402-404,433,465-510` where the row has `372-404,433-485,493-510`. The wave-2 prompt
   inherits that list, which drops 372-396 (the `onInhibit` body) — the only range covering
   inhibit bookkeeping other than line 301. The landed row is right; the generator is not
   faithful, and this assignment's anchor list was the generator's, not the row's.
3. The row's `372-404` also excludes `onInhibit` 363-371 (signature, `m_iInhibitLocks += lock
   ? 1 : -1`, negative clamp). Minor: the increment itself is unanchored, though [HC:301]
   anchors the gate it feeds.

## Remaining unknowns

- Whether any artifact outside the lane (handoff, screenshot, chat) repeats the wrong digest.
  Lane grep finds it in exactly: draft `NoteIdle-rows.md:15,25`, `SOURCES.md:78`,
  `lessons/round-17.md:53`, `gen_w2.py:50`, `w2/spec.json`, `w2/dispatch.json` (the latter
  two carry the generated prompt), plus copied lane trees under `/tmp` (`sep-*`, `mado-sep`,
  `simplify-repo`).
- Upstream tag immutability over time. Today's four retrieval channels are identical; what
  wave 1 saw is only observable through its report and archived copy, both of which agree
  with today's `…6f5cd…`.
- No host/running-binary claim: S066 is documentary source code. The pacman.log pkgver
  binding belongs to neighbouring rows and is out of scope here.
- Tier correctness beyond the definition: `CORPUS.md:93` explicitly admits source code as
  tier A; no further authority exists to test against.

## Installs

none. No sudo/pacman/paru/systemctl/hyprctl/libinput/evtest/live probes were run. Only
`curl` (four URLs), local file reads, `sha256sum`, `cmp`, `python3`, `tar -xzO`, `grep`,
`sed`, `awk`, `find` on `/tmp`.

## Reproduction commands

```
curl -sSL -o /tmp/hypridle-018.cpp https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp
curl -sSL -o /tmp/h2.cpp "https://github.com/hyprwm/hypridle/raw/refs/tags/v0.1.8/src/core/Hypridle.cpp"
sha256sum /tmp/hypridle-018.cpp /tmp/h2.cpp
cmp /tmp/hypridle-018.cpp /tmp/h2.cpp && echo IDENTICAL
tar -xzOf /tmp/hypridle-v0.1.8.tar.gz --wildcards '*/src/core/Hypridle.cpp' | sha256sum
grep -n "2dd4d73d" corpus/SOURCES.md corpus/lessons/round-17.md
grep -n "2dd4d73d6f5cd" -r corpus .ufo/waves/round-17/w1/reports
```
