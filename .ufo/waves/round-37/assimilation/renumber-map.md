# Round-37 assimilation — id collision check and renumber map (scratch, by document)

Commands: the prompt's §10 collision block (0–3-space row pattern), run 2026-10-25 against
`corpus/SOURCES.md` at base `b4e47e9` and `merge/mado/SOURCES.append.md`.

- `reg-ids`: 201 ids (S001…S211). `staged-ids`: 147 ids (S203…S349).
- `collisions`: 9 — S203 S204 S205 S206 S207 S208 S209 S210 S211 (the lane's round-35/36
  appends took those ids after the package was built). None of the nine is appended; no
  staged row is appended as-is.
- Guard proof (`guard-proof/`): a scratch registry whose `  | S002 |` row is indented two
  spaces; the 0–3-space pattern finds collision `S002` (n=1), the column-zero pattern finds
  none (n=0). The guard is live.

## Map — the URL / artefact decides the id, never arithmetic

| package reference | document | lane id | action |
|---|---|---|---|
| staged `S214` | `raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp` | **S212** (new) | re-opened 2026-10-25, 41,392 B, sha256 `1e19d926…97d7e9` = package prefix; row rewritten in fleet schema |
| entry merge-note "wave-1 S187" (the compositor's event manager) | `raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/managers/EventManager.cpp` | **S189** (held) | re-opened, byte-identical to `.ufo/waves/round-32/fetch/S189.bin`; `used-by` extended |
| entry merge-note "wave-1 S188" (Waybar's IPC backend) | `raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp` | **S201** (held) | re-opened, byte-identical to `.ufo/waves/round-34/fetch/S201.bin`; `used-by` extended |
| staged `S226` | `/run/user/1000/hypr/efb50993…_1792772698_564628331/hyprland.log` | — | refused: the instance directory no longer exists; the current session's log is a different artefact, measured fresh as S213 |
| staged `S242` | `journalctl --user -u wayland-wm@hyprland.desktop.service` | — | refused: null channel for the markers (S213 receipt, S214 `Logger.cpp:15-16,:48`) |
| — (lane's own) | current-session log + unit journal + `hyprctl getoption debug:*` | **S213** (new, own-work) | receipt `fetch/S213.receipt.txt` |
| — (lane's own) | `raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/debug/log/Logger.cpp` | **S214** (new) | 1,789 B, sha256 `d04e3a2f…f6b868` |

## Quarantine slice (absent-defect register, mado data rows: 13)

Only one slice row names a document an admitted entry rests on: register `round1 S189`
(`EventManager.cpp`, class `payload-absent`, quote ``auto eventString = std::format(...)``).
Hand-checked 2026-10-25: the quote **is present** at line 128 of the re-fetched bytes
(`auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`);
the register's escaped `\"`/`\\n` form is why its check found nothing. Verdict: present,
adopted with the anchor located here (`:128`). The other 12 slice rows (S195, S201-register
[an arXiv paper, not the lane's S201], S205, S224, S228, S199, S200, S209, S222, S223, S225,
S235) name documents no admitted entry cites; they stay quarantined, unappended and unchecked
this round.
