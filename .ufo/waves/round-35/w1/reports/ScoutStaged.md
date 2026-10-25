# ScoutStaged — merge-package source audit (round-35, 2026-10-24)

Scoped read-only audit of the three merge-package knowledge entries this round adopts:
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/idle-lock-never-asked-r12.md`,
`idle-lock-chain-armed-r14.md`, `idle-lock-offered-in-the-bar-r15.md`.
For every `source:` line: the document named, whether it resolves on this host, and the
package id it lands on. Package register read: `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md`
(140 rows, S197–S342). Lane register read: `corpus/SOURCES.md` (rows through S202).

## 1. `source:` lines, documents, host resolution

| Entry | Cited id | Document named | Resolves on this host? |
|---|---|---|---|
| r12 | S309 | `lanes/mado/round12/fetch/host-omarchy-first-run.txt` | YES — at `/home/vgpnk/Projects/shokuknow/lanes/mado/round12/fetch/host-omarchy-first-run.txt` |
| r12 | S310 | `lanes/mado/round12/fetch/host-idle-lock-never-asked.txt` | YES — same root |
| r14 | S321 | `lanes/mado/round14/fetch/host-idle-lock-chain-state.txt` | YES — same root |
| r15 | S329 | `/home/vgpnk/.config/waybar/config.jsonc` | YES |
| r15 | S330 | `/home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh` | YES (sha256 `6d8d2c11…f1750`, per ScoutS207 re-open) |
| r15 | S331 | `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu` | YES |
| r15 | S334 | `lanes/mado/round15/fetch/host-waybar-dated-backups-sweep.txt` | YES — same root |
| r15 | S336 | `lanes/mado/round15/fetch/host-omarchy-toggles-state-sweep.txt` | YES — same root |

All eight documents resolve. Notes on path base:

- The five `lanes/mado/…` payloads resolve only under the **shokuknow root**
  (`/home/vgpnk/Projects/shokuknow/`). The merge package dir (`merge/mado/`) contains
  `knowledge/` and `amendments/` subtrees only — the fetch payloads are **not** carried
  in the package. The lane root `mado-shokunin/` has no `lanes/` dir.
- All resolution checks run at write time (`test -e`), 2026-10-24.

## 2. Package ids: cited id ≠ package-register id

The entries' `source:` headers carry the **pre-renumber** ids. Per
`/home/vgpnk/Projects/shokuknow/lanes/mado/ID-REMAP.md`, staged rows were renumbered at
packaging time (lane registry ends at S202; first staged id = S203). The correct package
rows for the cited documents are at the **remapped** ids:

| Entry | Cited id | Package id (remap) | Package row at remapped id names |
|---|---|---|---|
| r12 | S309 | **S315** (r12: S309→S315) | `host-omarchy-first-run.txt` — same document |
| r12 | S310 | **S316** (r12: S310→S316) | idle-lock never-asked fetch — same document |
| r14 | S321 | **S327** (r14: S321→S327) | `host-idle-lock-chain-state.txt` — same document |
| r15 | S329 | **S335** (r15: S329→S335) | `config.jsonc` — same document |
| r15 | S330 | **S336** (r15: S330→S336) | `idle.sh` — same document |
| r15 | S331 | **S337** (r15: S331→S337) | `omarchy-menu` — same document |
| r15 | S334 | **S340** (r15: S334→S340) | dated-backups sweep — same document |
| r15 | S336 | **S342** (r15: S336→S342) | toggles-state sweep — same document |

**Literal-id reads mis-resolve.** If a gate or reviewer reads an entry's `source:` id
literally against `SOURCES.append.md`, every one of the eight lands on a *different*
document: S309→round11 journal lifecycle, S310→round11 gkeep rule, S321→ArchWiki CN
wikitext, S329→PortalManager.cpp, S330→Quickshell grab.cpp, S331→hyprland-protocols
README, S334→Japanese X11/Wayland article, S336→idle.sh. The last is a wrong-document
hit that still points at an idle-lock file — the most misleading cell of the eight.

## 3. Sharing with the lane's own S201/S202 rows

Lane `corpus/SOURCES.md:203-204`:

- **S201** — Waybar 0.15.0 `hyprland/backend.cpp` @ tag 0.15.0, 6550 B, sha256 `799bf02f6d18ae04`
- **S202** — Waybar 0.15.0 `hyprland/window.cpp` @ tag 0.15.0, 8324 B, sha256 `5df496eb3cfe5cae`

**No adopted entry cites any package id the lane uses for S201/S202** — the entries' id
range (S309–S336 cited; S315–S342 effective) is numerically disjoint from S201/S202.

The sharing that does exist is **document-level, one id-layer up**: the same two
upstream Waybar sources are already registered in the package as rows **S207** (=
staging S201, remapped) and **S208** (= staging S202, remapped) — same URLs, same tag
`0.15.0`, same byte sizes, same sha256 prefixes (`799bf02f6d18ae04`, `5df496eb3cfe5cae`).
Row text differs only in anchor/verdict prose and recheck fields (lane: `90d`,
mined 2026-10-24; package: `on-release — re-pull`, mined 2026-10-23). No knowledge
entry in the package cites S207/S208.

Implication: the lane's S201/S202 are not new documents to the merge — the package's
S207/S208 are the same blobs. Adoption can register the lane rows verbatim (no
duplicate-source defect, different register), or treat S207/S208 as the package-side
canonical rows for the same documents.
