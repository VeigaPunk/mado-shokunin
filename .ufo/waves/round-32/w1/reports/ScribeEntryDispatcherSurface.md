# ScribeEntryDispatcherSurface — re-grounded draft of dispatcher-surface-and-request-grammar-r26 (round 32, w1)

Leaf scribe; no subagents dispatched. No writes outside `.ufo/waves/round-32/`.

## Deliverable

Draft: `.ufo/waves/round-32/scratch/ScribeEntryDispatcherSurface/dispatcher-surface-and-request-grammar-r26.md` (6,664 bytes).
`corpus/` untouched; `shokuknow` read-only, per charter.

## Upstream-input status

`w1/reports/ScoutDispatchers0560.md` **does not exist** — the scout process is
still running (log: `w1/logs/ScoutDispatchers0560.log`, "Working..." at
20:03). Its fetched bytes **do** exist:
`.ufo/waves/round-32/scratch/ScoutDispatchers0560/dispatchers-0.56.0.html`,
sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`,
297,863 bytes, byte-identical to `.ufo/waves/round-32/fetch/S196.bin`, mtime
2026-10-24 20:03. I verified the staged entry directly against those
re-opened bytes (plus `fetch/S188.bin` ≡ `scratch/ScoutDispatchersWiki/dispatchers.md`
for the cross-page check). One live re-fetch: the guessed 404 URL.

## Name-by-name diff — verified 0.56.0 list vs the staged entry's printed list

**Verified 0.56.0 dispatcher name set** (extracted from the five tables,
§§ General/Window/Workspace/Group/Cursor): **45 distinct names** —
`active, alter_zorder, center, clear_tags, close, cycle_next,
deny_from_group, dpms, drag, event, exec_cmd, exec_raw, exit, float, focus,
force_idle, force_renderer_reload, fullscreen, fullscreen_state, global,
kill, layout, lock, lock_active, move, move_to_corner, move_window, next,
no_op, pass, pin, prev, pseudo, release_input_capture, rename, resize,
send_key_state, send_shortcut, set_prop, signal, submap, swap,
swap_monitors, tag, toggle, toggle_special, toggle_swallow`.

**Differences vs what the staged entry prints:**

1. Staged §1 prints a 3-item "includes" list (`exec_cmd`, `dpms`, `event` —
   all three verbatim-correct against the 0.56.0 table, signatures included)
   plus an 8-keyword presence claim (`force_idle`, `dpms`, `event`,
   `exec_cmd`, `pass`, `fullscreen`, `exit`, `exec` "documented on both
   pages"). Verified: **7 of 8 correct; `exec` is wrong.** On S196 `exec`
   appears only inside keybind-syntax prose (`exec, uwsm stop`,
   `exec, loginctl terminate-user`) — never as an `hl.dsp.*`/`exec_cmd`-style
   dispatcher row. On S188 the token `exec` as a standalone word has **zero
   occurrences**. Neither page documents an `exec` dispatcher.
2. Staged §1 INF claims "the same dispatcher vocabulary" across 0.56.0 and
   current-git. Verified name sets: 0.56.0 = 45, current = 46 —
   **current-only: `reload_config`**; nothing exists only on 0.56.0. The
   claim is wrong by one name. Draft rewrites it: almost-stable set, one
   post-0.56 addition.
3. Signature-level drift found while diffing (kept in draft as OBS):
   current-git rows lead with `window?` (e.g. `fullscreen({ window?, … })`
   vs 0.56.0 `fullscreen({ mode?, action?, layout_aware?, window? })`), and
   0.56.0 carries a separate bare `resize()` row that current-git folds into
   `resize({ keep_aspect_ratio? })`. Row counts therefore differ even where
   name sets match.

## Other staged-claim dispositions

- 404 guessed URL — **re-verified live** 2026-10-24 (HTTP 404); kept.
- §2 S018 claims (`HyprCtl.cpp`, m_dispatchers registry, "Invalid
  dispatcher", batch `;` split, flag stripping, `hl.dispatch` wrap) —
  **not re-verified**: S018 bytes are not in this lane's round-32 scratch and
  the contract bounds the draft to re-opened bytes. Kept verbatim under an
  explicit "not re-opened in round 32" flag rather than silently asserted.
- `flags` zero hits in S196 bytes → recorded as UNK support, not claimed.
- "Last updated on July 15, 2026" — footer quote added to `## Gate`.
- Provenance trio updated: `verified-at: 2026-10-24`; recheck note carries
  the new sha256 prefix. Gate block added per contract (URL + access date
  2026-10-24 + two located quotes ≤25 words each).

## Risks

- If ScoutDispatchers0560 lands a different extraction, reconcile before
  commit — its report was absent at draft time (above).
- The §2 block retains staging-era S018 citations; a future round should
  re-open the tagged file before editing those claims.
