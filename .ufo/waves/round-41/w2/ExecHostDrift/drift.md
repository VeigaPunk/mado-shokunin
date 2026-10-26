# ExecHostDrift — host-drift attack on the entry's dated host claims (round 41 w2)

Attack target: "the entry's host claims are a dated measurement — has the host moved?"
Entry: `corpus/knowledge/hyprland-focus-grab-r41.md` at DATA commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`.
Result: **no defect found — the host has not moved on any read-only axis.** Every dated host statement re-verified today (2026-10-25) is still true.

## Evidence

### 1. Journal re-capture vs fetch receipt (S289 source)
Command (same as the receipt's grammar):
```
journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso > xdph-journal-now.txt
```
- `wc -l -c` now: 153 lines / 19130 bytes — identical to `.ufo/waves/round-41/fetch/xdph-journal.txt` (153 / 19130).
- `sha256sum` now: `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7` — identical to the fetch receipt (entry line 9 pins this exact hash).
- No new sessions, no adverts, no restarts since the fetch (portal unit active since `Sun 2026-10-25 13:36:24`, Main PID 1952 — still the live PID today; `pgrep -af xdg-desktop-portal-hyprland` → `1952 /usr/lib/xdg-desktop-portal-hyprland`).
- `journalctl --list-boots`: boot -1 `0a3785aac7104585a914f6cda41795a7` (Sat 2026-10-24 20:57:12 → Sun 13:35:39) and boot 0 `7ab69ee4149c4811a3faf6c08c9d119b` (13:36:19 → 20:53:58). The two journal sessions map to these two boots; no third boot/service restart appeared.

### 2. Delivered tool on both journals (`--journal-file`)
Tool = `tools/mado-globals.py` at DATA commit (extracted to `tool-datacommit.py`; sha256 `286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`, byte-identical to working tree and to the v2 freeze reference `.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`).
```
python3 -I tool-datacommit.py --journal-file fetch/xdph-journal.txt          # exit 0, verdict=OK
python3 -I tool-datacommit.py --journal-file w2/ExecHostDrift/xdph-journal-now.txt   # exit 0, verdict=OK
```
Both runs produce identical output:
- `MADO_GLOBALS_SESSION: n=1 boot=- pid=1918 first=2026-10-25T13:16:45-03:00 last=… interfaces=8 adverts=15`
- `MADO_GLOBALS_SESSION: n=2 boot=7ab69ee4149c4811a3faf6c08c9d119b pid=1952 … interfaces=63 adverts=63`
- `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=… focus-grab:1 … expected_missing=- ignored=0 verdict=OK`
- `--expect hyprland_focus_grab_manager_v1 --expect hyprland_input_capture_manager_v1` → `expected_missing=-`, OK, exit 0.

### 3. Compositor identity
```
hyprctl version
```
→ `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean` — the exact string the entry (line 77) quotes. Unchanged.

### 4. Installed portal package record (S037)
```
sha256sum /var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc
```
→ `7bf2f8beeadf189be54460a72700f81722d9be78884a0a8ee56a46a70c9445a5` — identical to `.ufo/waves/round-41/fetch/xdph-installed-version.txt`; still the only installed package dir, version `1.4.1-2`. Unchanged.

### 5. Entry internal counts, reproduced on the fresh capture
- `grep -c 'Got interface:'` = 78 (15 + 63) — matches the entry census line `adverts=78`.
- `grep -ic 'focus'` = 1, occurring only on line 117 (`Got interface: hyprland_focus_grab_manager_v1 (ver 1)`) — matches entry line 71 ("in the whole journal the string `focus` occurs exactly once, on the advert line itself").
- Notebook note: both captures carry a torn line 74 (`… [core] dmabufFeedbackMa`, boot -1 tail) — a pre-existing journal-side artifact, not drift; it contains no `Got interface:` and does not affect the census.

## Time-bound entry statements — status
| Entry line | Statement | Re-verified today | Still true |
|---|---|---|---|
| 9 (S289) | journal receipt, sha256 bf8fa91a… | sha identical | yes |
| 10 (S037) | installed package 1.4.1-2 | package desc sha identical | yes |
| 11 | `verified-at: 2026-10-25` | today | yes |
| 61 | latest session pid 1952 @ 13:36:24, one advert, ver 1 | journal + live unit state | yes |
| 63 | census sessions=2 adverts=78 interfaces=63 focus_grab=1 | tool re-run on fresh capture | yes |
| 65 | two sessions (pid 1918 slice, pid 1952 whole), `-- Boot` marker | journal identical | yes |
| 71 | "focus" occurs exactly once, on the advert line | grep | yes |
| 73 | installed package record read | desc sha identical | yes |
| 77 | `hyprctl version` dated read (0.56.2 @ efb50993…) | verbatim | yes (and the entry itself labels it a dated measurement, not a registry row) |
| 79 | UNK which process binds the manager | still unobserved (no client run, read-only) | yes |

The journal is byte-identical after ~7 h: **no new sessions/adverts appeared**, so the census remains representative of the host today.
`§7`'s own caveats (one host, one day, two portal sessions; re-run the census; never reuse the counts) are honored and remain accurate.

Tools installed: none (python3 present; no package transactions, no pacman).
