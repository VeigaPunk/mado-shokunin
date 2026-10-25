# SenBoundary — host-boundary receipt (round 39, w1)

**Verdict: NO HOST MUTATION EVIDENCED — boundary holds.**
Severity: none found. No socket connect, no service/compositor command, no config-tree/file write
on the host was performed by this round; all host paths captured in SctHostTree's manifest hash
identically now.

## 1. Host-tree hash diff (manifest vs re-read)

Source manifest: `.ufo/waves/round-39/w1/SctHostTree/manifest.sha256` (53 paths under `$HOME`
relative: `.config/hypr/*`, `.config/omarchy/current/theme/{gum.env,hyprland,hyprlock}.conf`,
`.local/share/omarchy/default/hypr/**`, `.local/state/omarchy/toggles/hypr/{flags,window-no-gaps}.conf`;
captured 2026-10-25 16:10:24, mtime `1792955423`).

Command:
```
MAN=.ufo/waves/round-39/w1/SctHostTree/manifest.sha256
awk '{print $2}' "$MAN" | while read -r p; do f="/home/vgpnk/$p"; \
  [ -f "$f" ] && sha256sum "$f" | sed 's#  /home/vgpnk/#  #' || echo "MISSING  $p"; done \
  | sort -k2 > /tmp/host-now.txt
sort -k2 "$MAN" > /tmp/manifest-sorted.txt
diff /tmp/manifest-sorted.txt /tmp/host-now.txt; echo "diff_exit=$?"
```
Output: `diff_exit=0`; `53 / 53` lines identical. No MISSING entries (all 53 paths exist and
hash-equal to the capture). → host config/state tree byte-identical to capture.

Capture-timing note: manifest was written at 16:10:24, i.e. before the wave's host-touching
**reads** (ExecOptionsRealTree run-static 16:11:04; ExecOptionsTool static `--home /home/vgpnk`
run 16:11:11) and after only in-lane writes (C1 after 16:08:48, knowledge entry 16:09:30). No
host write preceded or followed the capture; the diff therefore covers all host access the wave did.

## 2. Capture fidelity / copy preservation

- In-lane mirror `SctHostTree/real-tree/` (53 files) vs manifest: `diff` exit 0 (53/53) — the
  captured mirror equals the host snapshot exactly.
- `ExecOptionsRealTree/host-src.sha256.norm` vs `host-dst.sha256.norm` (49 paths): `diff` exit 0 —
  the evidence copy is byte-faithful; read-only copy path.

## 3. No host file additions/deletions during the wave

Inventory of the four covered roots (`.config/hypr`, `.config/omarchy/current/theme`,
`.local/share/omarchy/default/hypr`, `.local/state/omarchy/toggles/hypr`) vs mirror: the only host
files outside the 53-path mirror are pre-round artifacts — theme assets mtime 2026-10-03
17:49:02 (`1791060542`), `.bak` files 2026-10-13/2026-10-17 (`1791942509`, `1792267376`). No file
mtime falls in the wave window (2026-10-25 16:00–16:15).

## 4. No socket connects

All seat reports affirm none:
- ExecOptionsTool.md: "no host service mutation, no socket connects, no git/jj mutation" (line 131–132).
- ScrDispatcherAmendment.md: "no socket connect; no compositor or host config mutation" (line 60).
- `ScrDispatcherAmendment/dispatcher-amendment-section.md`: "no request was sent, no dispatcher
  dispatched, and no socket was connected" (§3, line 101); "read-only: no compositor, socket,
  service or config tree was touched" (line 4).
- `ScrKnowledgeEntry/config-option-table-r39.md`: "does not contact a compositor, socket, or network".
- ExecEventqSnapshot.md: the only socket sighting is a **read-only census** of the eventq socket's
  listener/server rows (`eventq-live-census.txt`); no full `ss -xpa` table committed (registration
  §6.3 harm-watch), no connect performed (2 clients listed with their existing fds; write_fail=0).

## 5. No service / compositor commands ran

Deep scan of all round-39 reports/docs (`**/*.md`, txt, json, err) for executed commands
(`systemctl`, `hyprctl`, `journalctl`, `hostnamectl`, `loginctl`, `ss -xpa`, `pkill`, etc.):
zero executions recorded. All hits are **content**, not commands run this round: `hyprctl`/
`systemctl` lines inside the host config files' own bindings/autostart text (data), `loginctl`
inside the fetched S220 page HTML, and `ss -xpa` as the text of the registration item describing
what is NOT committed. `w1-run.err` is empty. pacman: paused host-wide per dispatch; no package
transaction in any seat report (ExecOptionsTool: "No pacman/package transactions (none needed)").

## 6. Boundary receipt

```
host hash diff (manifest vs now): 53/53 identical, diff_exit=0
mirror vs manifest:                53/53 identical, diff_exit=0
copy src vs dst norm:              49/49 identical, diff_exit=0
host-only files (non-manifest):    theme assets 2026-10-03 + .bak 2026-10-13/17 — pre-round
socket connects:                   none (seat affirmations)
service/compositor commands:        none executed
pacman/package transaction:         none
```
No remediation required. No host path was written by this sentinel; the only file written this
seat is this report.
