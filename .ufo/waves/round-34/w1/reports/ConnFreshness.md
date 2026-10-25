# ConnFreshness — round-34 freshness check on S201 and S202

Read-only freshness check against `corpus/SOURCES.md`, the fetch blobs under
`.ufo/waves/round-34/fetch/`, and the registry's `recheck` convention. Today: **2026-10-24**.

## Rows

| id | opened | recheck | upstream tag named by row | fetch blob commit |
|---|---|---|---|---|
| S201 | 2026-10-24 | `90d` | `Alexays/Waybar` tag `0.15.0` (`src/modules/hyprland/backend.cpp`) | `3420e827bd7b21b1374b23245526554ffd20d096` — 2026-10-24T21:55:08-03:00 |
| S202 | 2026-10-24 | `90d` | `Alexays/Waybar` tag `0.15.0` (`src/modules/hyprland/window.cpp`) | `3420e827bd7b21b1374b23245526554ffd20d096` — 2026-10-24T21:55:08-03:00 |

Both blobs were committed in the same round-34 commit
`3420e827bd7b21b1374b23245526554ffd20d096` ("round-34: freeze C1 and C2 predicates
and pre-data control receipts"), committer date **2026-10-24T21:55:08-03:00**.
Working-tree mtime for both files is 2026-10-24 21:50 (fetch ~5 min before commit).

## Age of `opened`

- `opened` = 2026-10-24 for both rows; today = 2026-10-24.
- Age: **0 days** — opened today. Both rows are fresh; no recheck is due.

## Recheck-form consistency vs lane norm

Registry `recheck` value census (all rows, `corpus/SOURCES.md` field 11):

| value | rows |
|---|---|
| `on-release` | 131 |
| `on-change` | 22 |
| `90d` | 18 |
| `180d` | 15 |
| `on-gate-change` | 2 |
| `on-session-change` | 1 |
| `on-operator-recovery-decision` | 1 |
| `on-compositor-release` | 1 |
| `on-capture-change` | 1 |

`90d` is a normative lane form (18 rows), so S201/S202 are not malformed.
However, the *kind-matched* convention shows a deviation:

- Tag/commit-pinned immutable code+docs siblings overwhelmingly carry `on-release`
  (the dominant form, 131 rows). The same Waybar tag `0.15.0` is already pinned by
  S053 (`waybar-custom.5.scd`) and S054 (`custom.cpp`), both `on-release`. S201/S202
  are the same immutable class — content addressed by tag `0.15.0`, byte-pinned by
  sha256 prefix — yet carry `90d`.
- The `90d` form is otherwise used for *mutable* surfaces: live "Latest git" wiki
  pages (S016, S017, S031, S045, S063, S064), flatpak docs (S032–S034), rendered
  archived wiki (S187, S196), host-state captures (S019, S095), and — notably — the
  other commit-pinned round-34 additions S186, S188, S189 (raw.githubusercontent.com
  @ commit-hash pins), which also carry `90d`.

So `90d` on a hash/tag-pinned source is a *recent* pattern (S186, S188, S189,
S201, S202 this round) that diverges from the established tag-pinned norm of
`on-release` (S053/S054 and the S151–S177 block).

## Finding

- **S201 and S202 are fresh** — opened today (age 0d), fetch blobs committed
  2026-10-24T21:55:08-03:00 in `3420e82`.
- **Recheck flag**: both rows use `90d`, a real lane form but not the form used by
  their same-tag Waybar siblings S053/S054 (`on-release`). For a byte-pinned,
  tag-anchored source, `90d` imposes a wall-clock recheck the immutable content
  does not need; `on-release` is the consistent value. Not a conformance break —
  the same `90d`-on-pinned pattern appears on S186/S188/S189 — but worth a
  consistency pass if the round touches the registry.
- No other row deviates: all `90d`/`180d` values sit on a documented convention
  (mutable docs/host-state → time-bounded; pinned artifacts → event-bounded).

## Commands run

- `git log --format='%H %cI %s' -- .ufo/waves/round-34/fetch/S201.bin .ufo/waves/round-34/fetch/S202.bin`
- `awk -F'|' '/^\| S[0-9]+/ {...print $11}' corpus/SOURCES.md | sort | uniq -c` (recheck census)
- `stat`/directory listing of `.ufo/waves/round-34/fetch/` (blob mtimes 2026-10-24 21:50)
