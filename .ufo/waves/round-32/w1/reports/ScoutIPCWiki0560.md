# ScoutIPCWiki0560 — re-open S187 (wiki.hypr.land/0.56.0/IPC/)

**Fetch:** success. `curl -sSL --fail-with-body` on `https://wiki.hypr.land/0.56.0/IPC/` → HTTP 200.

- Fetched bytes: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/scratch/ScoutIPCWiki0560/IPC-0.56.0.html`
- Byte length: **268731**
- sha256 prefix (first 16 hex): **`136e5511fba5524a`**
- Access date: **2026-10-24**
- Page revision stamp: `Last updated on` + `datetime="2026-05-02T03:38:58.000Z"` (matches staged "May 2, 2026").

## Located items (line numbers in fetched HTML)

| # | Item | HTML line | Section heading |
|---|------|-----------|-----------------|
| 1 | `.socket.sock` request socket | **2847** (`<h2>` anchor `xdg_runtime_dirhyprhissocketsock`) | `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock` |
| 2 | `.socket2.sock` event socket | **2861** (`<h2>` anchor `xdg_runtime_dirhyprhissocket2sock`) | `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock` |
| 3 | Event framing | **2864** (under the `.socket2.sock` h2, immediately above `Events list`) | — |

## Verbatim quotes (≤25 words each)

- Request socket (under h2 `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`):
  > "Used for hyprctl-like requests. See the Hyprctl page for commands." (10 words)
  > "basically, write [flag(s)]/command args." (5 words)

- Event socket (under h2 `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock`):
  > "Used for events. Hyprland will write to each connected client live events like this:" (14 words)

- Event framing (same section):
  > "EVENT>>DATA\n (\n is a linebreak)" (5 words)
  > "e.g.: workspace>>2"

- Freeze rule (under `.socket.sock`, `Note` callout):
  > "any unclosed connections will cause Hyprland to freeze until the five-second timeout is reached" (14 words)

## Event catalogue count

The published catalogue is an HTML **table** (not `<li>` list items), under h2
`Events list` (HTML 2866–3097). Counted the table's item rows:

```bash
f=IPC-0.56.0.html
end=$(awk 'NR>2866 && /<\/table>/{print NR; exit}' "$f")   # → 3097
sed -n "2866,${end}p" "$f" | awk '/<tbody>/,/<\/tbody>/' | grep -c '<tr'   # → 44
```

Result: `<thead>` = 1 row (`name | description | data`), `<tbody>` = **44 rows** =
**44 events**. Cross-checked with a Python `html.parser` first-`<td>` extraction:
44 names: workspace, workspacev2, focusedmon, focusedmonv2, activewindow,
activewindowv2, fullscreen, monitorremoved, monitorremovedv2, monitoradded,
monitoraddedv2, createworkspace, createworkspacev2, destroyworkspace,
destroyworkspacev2, moveworkspace, moveworkspacev2, renameworkspace,
activespecial, activespecialv2, activelayout, openwindow, closewindow, kill,
movewindow, movewindowv2, openlayer, closelayer, submap, changefloatingmode,
urgent, screencast, screencastv2, windowtitle, windowtitlev2, togglegroup,
moveintogroup, moveoutofgroup, ignoregrouplock, lockgroups, configreloaded,
pin, minimized, bell.

## Comparison against S186 — "identical event vocabulary across the 0.56→0.57 boundary"?

- S186 (pinned upstream `_index.md` @ `c04680a`, re-fetched by sibling seat — see
  `w1/reports/ScoutIPCWikiCurrent.md`, 44 event rows, md table lines 38–81).
- This fetch (0.56.0 published page): **44 events**.
- Name-set diff (Python, both sets of 44): `only in S186: []`, `only in S187: []` → **IDENTICAL**.

**Verdict: AGREE.** The staged row's claim holds: both sides carry exactly 44 events
with identical names — none added, none removed across the 0.56 → 0.57 boundary.

## Staged-entry faithfulness

Staged row S187 (`SOURCES.append.md:8`) claims: § `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`,
§ Events list, `EVENT>>DATA\n` framing @ "Last updated on May 2, 2026", 268731 B.

| Staged item | This re-open |
|---|---|
| socket path anchor | ✓ h2 anchors present at HTML 2847/2861 |
| `EVENT>>DATA\n` framing | ✓ verbatim at HTML 2864 |
| "Last updated on May 2, 2026" | ✓ `datetime="2026-05-02T03:38:58.000Z"` |
| 268731 B | ✓ exact |
| 44-event identical vocabulary | ✓ counted + set-diffed identical |

No discrepancy found.
