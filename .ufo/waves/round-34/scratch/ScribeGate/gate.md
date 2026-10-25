## Gate

Opened and appended this round under PRED-C1-r34-v1, frozen at
`3420e827bd7b21b1374b23245526554ffd20d096` with pre-data receipts; the
round-33 counter was killed by a symlink crib and was not replaced. The
append landed `fa7ba11346116672352b5d41494141c5c4d738d0`. The predicate
was not rewritten after seats scored it. The assimilation package is
`.ufo/waves/round-34/assimilation/`: `append-block.md` (two rows),
`quarantine-slice` (thirteen register rows), `staged-ids` vs `reg-ids`
(136 vs 190 ids, `collisions` empty). Fetch digests agree three ways —
blob, `corpus/SOURCES.md`, `c1/frozen.json` — re-run in
`.ufo/waves/round-34/w1/reports/ExecFetches.md`.

- Admit (appended `corpus/SOURCES.md:203-204` at
  `fa7ba11346116672352b5d41494141c5c4d738d0`):
  - `S201` — `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp`,
    opened 2026-10-24, 6550 B, sha256
    `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e`.
    Located quote (line 38; authority the gate-quote line of
    `corpus/knowledge/waybar-module-text-route-r25.md`):
    "$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr" —
    8 words, contiguous substring of the committed blob.
  - `S202` — `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp`,
    opened 2026-10-24, 8324 B, sha256
    `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846`.
    Located quote (line 27; same authority):
    `m_ipc.registerForIPC("activewindow", this);` — contiguous substring
    of the committed blob.
  Both in-province: Waybar is named in `PROVINCE.md:3-4` and the lane
  already absorbs compositor C++ at S189
  (`.ufo/waves/round-34/w1/reports/CritProvince.md`). The registry jumps
  S196 → S201; S197–S200 stay unallocated — the append commit reserves
  the gap and the never-reuse rule bars filling it later.
- Refuse (assimilation package `quarantine-slice`, 12 of 13 rows; none of
  their locators was fetched this round, and none is needed to refuse):
  - `S195`, `S205`, `S228` — localization surfaces (SJTU
    arch-wiki-docs-zh-cn package, Arch-wiki interwikimap JSON,
    `cn-export-hyprland.html`). Documentation localization is outside
    PROVINCE.md, the same rule that refused `two-literature-drift-r26.md`
    in round 33. Flip: a desktop/compositor surface cited only from tier
    A or B, opened by this lane.
  - `S201` of the register (`https://arxiv.org/abs/2604.18860`) — id
    collision: the lane's S201 now binds `backend.cpp`, and the arXiv URL
    is absent from the registry. Flip: fetched bytes under a fresh id
    plus an in-province desktop/compositor claim; never under S201.
  - `S224` — `/home/vgpnk/.cache/ai-usage/status.json` is a transient
    host cache file, not a source; its `updated_at` quote is stale on
    every read. Flip: reclassify as own-work probe output under
    `.ufo/evidence/`, or a durable published artifact.
  - `S199`, `S200` — CSDN locators (tier C) never fetched; `unreachable`
    is not fabrication and is not a locator the lane opened. Flip: a
    desktop/compositor surface cited only from tier A or B, opened by
    this lane.
  - `S209`, `S222`, `S223`, `S225`, `S235` — the register cites only a
    `## Gate — Snnn` prose anchor; no locator was ever named, so the row
    is unverifiable, not fabricated. Flip: a resolvable URL or path
    naming the row's claimed bytes, opened by this lane.
- Quarantine hand-check this round (scout, thirteen rows): `S189` PRESENT
  — the register's payload-absent mark is a false negative; the quoted
  span sits at line 128 of the pinned `EventManager.cpp` (6479 B, sha256
  `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`
  confirmed). C2's calibration re-open measured line 169 as
  `const size_t MAX_QUEUED_EVENTS = 64;` and SCORECARD publishes
  `r34-s189-line: line=169`. S189 was adopted in round 32; it is not
  re-appended.
- considerthese/2026-10-24.md proposals 1–6 carry the file's own marking
  "proposals only; not acted on" — all not implemented. The seat
  recommendation (#4, #1, #3) is a pointer, not a decision. Mined, not
  edited.
