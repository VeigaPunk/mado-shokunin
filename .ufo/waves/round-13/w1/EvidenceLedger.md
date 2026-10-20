# Mado round 13 — EvidenceLedger (draft, scribe lane)

Seat: `MadoR13.EvidenceLedger` (scribe, leaf; no subagent dispatch, no background jobs).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Status: **draft; no verdict issued.**
Checks not run by this seat: builds, lint, formatters, tests, `--selftest`, `--regression`, live probes, and the census command (no rerun, per lane instruction). No compositor or config writes.

## 1. Axes and this seat's scope

| Axis | Round target (from round-13 assignment) | Evidence in this draft | Verdict |
|---|---|---|---|
| coverage (C1) | sourced U4 protocol-phase + advertised-globals knowledge, 3/7 → 4/7 | U4 covered entries: 0 (§3, read-only grep) | **not decided** — owned by the knowledge-writing seats |
| operability (C2) | exact expected/observed set census for Hypr source and local `*.conf` inventory | census executable and its retained output recorded in §3; gate edits owned by GateImplement | **not decided** |

This seat only records evidence. It does not assign either axis a result.

## 2. Round checklist (drafted from sources, not from a round prompt file)

No round-13 prompt file exists in the lane. The checklist is built from the round-13 assignment text, `SCORECARD.md` (round-12 section: C1–C3 counting commands and harm watch) and `corpus/lessons/round-12.md` (`## Mistakes` M1–M14, `## Gate`, `## Outside spot-check`).

- [ ] Required source census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` must be run and its exit code recorded. Retained output of the initial run: `.ufo/waves/round-13/census-before.txt` (§3). Not rerun by this seat.
- [ ] C1 coverage: an admitted `corpus/knowledge/` entry opens with `source:` citing a `mined` `corpus/SOURCES.md` row and names U4; a `covers: U4` line is present. Baseline in §3: 0 U4 entries. Candidate rows: S005 (wayland-protocols README, queued), S006 (extras.html, queued), S008 (wayland-book, queued), S009 (architecture.html, queued), S010 (wayland.app, queued, discovery-only per its own row).
- [ ] C1 owed anchors: S006, S008, S009, S010 carry a section but no page revision (lesson Search-log errata). A round that mines one must append a superseding row whose `teaches` opens `supersedes S0NN —` with the source commit; the old row is not edited in place.
- [ ] C2 census: expected and observed sets compared; missing and extra members named (QUALITY criterion 14; lesson M13). Gate source list pinned at EXPECT; LOCAL inventory must not be count-only.
- [ ] C2 harm watch (per SCORECARD round-12 rule): selftest stays N/N, `--regression` ends `MADO_REGRESSION: PASS`, navigation counter stays complete, no config tree / compositor state / sibling repo written. **Not run here**; last recorded values are in SCORECARD and are historical, not re-measured.
- [ ] Registry hygiene (SOURCES.md contract): rows append-only; only `status`, `recheck`, `used-by` change in place; each change logged in the round lesson; rejected rows kept (QUALITY criterion 5).
- [ ] URL-duplicate pass before any renumbering merge (lesson, `## Outside spot-check`). See F1.
- [ ] Lesson grounding for new criteria (QUALITY criteria 6–16 each cite a lesson). No new criteria proposed by this seat.

## 3. Measured observations

### 3a. Required census — retained artifact (provenance correction)

Command recorded in the artifact:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`

Retained output, `.ufo/waves/round-13/census-before.txt` (read verbatim by this seat, not re-executed):
```
command: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
revision: 7dcb785b7b943d03703181b218d7860a7b43007b
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```
Result as retained: **exit 0**, with one `W04` finding naming `S030` as a duplicate URL. The `W04` line is a finding, not a failure exit; this seat records it as retained and does not reinterpret the census's own exit semantics.

Provenance note: this seat did **not** execute the census command. The exit-0 value is taken from the retained file. The file's writer and time are not recorded in it beyond the revision line.

### 3b. Tree state (provenance correction)

- `git rev-parse --short HEAD` → `7dcb785` (commit `7dcb785b7b943d03703181b218d7860a7b43007b`).
- The base tree was **clean before MadoR13's round-13 edits** (per the lane's IRC correction). The current uncommitted changes are current authored round-13 work, not inherited debt:
  - ` M SCORECARD.md` (diff +26 lines, round-13 block appended after `SCORECARD.md:325`).
  - `?? .ufo/waves/round-13/` (`census-before.txt`, `measure.py`, `w1/assignments.json`, `w1/dispatch.json`, `w1/spec.json`, `w1/reports/swarm-registry.json`, `w1/EvidenceLedger.md`).
- The earlier "inherited tree is not clean" statement in the first draft was mis-framed: this seat's observation was taken after those edits had landed. It is withdrawn.

### 3c. Supplementary observation — duplicate rows (grep-level, not the census)

Read-only `grep` of `corpus/SOURCES.md`, not a substitute for the required census:
- `corpus/SOURCES.md:28` — S017, status `mined`, URL `https://wiki.hypr.land/Configuring/Basics/Window-Rules/`.
- `corpus/SOURCES.md:41` — S030, status `rejected`, same URL.
- Status counts across the 39 `S0xx` rows: `mined` 27, `queued` 9 (S005–S010, S036, S038, S039), `rejected` 3 (S011, S012, S030).

### 3d. C1 baseline (round-12 counting commands, unchanged; read-only)

- `for f in corpus/knowledge/*.md; do head -n 15 "$f" | grep -qE '^source:.*\bS[0-9]{3,}\b' && echo "$f"; done | wc -l` → `4` (sourced entries).
- `grep -cE '^covers: U[1-7]' corpus/knowledge/*.md` summed → `3` (U1, U2, U3 in `window-rule-effects-getprop.md`, `hyprland-config-era-r12.md`, `xdg-portal-routing-r12.md`).
- `grep -lE '^covers:.*U4' corpus/knowledge/*.md | wc -l` → `0`. U4 is uncovered; the C1 target 4/7 is **not yet met** at this observation.
- Rubric (SCORECARD, `10 × covered U / 7`): 3/7 → 4.2857. No new row is claimed by this seat.

### 3e. Gate bytes (identity only, not re-run)

`sha256sum tools/mado-verify.sh` → prefix `ea798ad078f139f3…`, matching the round-12 final bytes recorded in SCORECARD. GateImplement may change the file concurrently; this is a snapshot.

### 3f. Lesson-entry cross-check

`corpus/lessons/round-12.md:84` (S030 gate line) and `:71` (S017 gate line) cite the same URL. The round-12 outside spot-check (`## Outside spot-check`) recorded an orchestrator **disagreement** on S030's admission; the post-review flip is in-place and logged (`## Post-review registry changes`).

## 4. Findings (anchored, no verdict)

1. **F1 — S030 duplicate URL is present in the registry.** `corpus/SOURCES.md:28` (S017) and `:41` (S030) share one URL; S030 is `rejected` (flip recorded at `corpus/SOURCES.md:91` and `corpus/lessons/round-12.md:120-124`). The retained required-census output reports it as `W04`. Whether that is a pass or fail for C2 is the integrator's decision, not this seat's.
2. **F2 — Census exit recorded as 0 in retained artifact.** `.ufo/waves/round-13/census-before.txt` ends `exit=0` with a `W04` S030 finding. Provenance: the file, not a rerun by this seat. The first draft's "exit 1" came from a one-off grep-level checker that is not the required command; that result is withdrawn and no longer used as census evidence.
3. **F3 — Tree state at the base was clean.** `7dcb785` was clean before MadoR13's round-13 edits; the current `SCORECARD.md` diff and untracked `.ufo/waves/round-13/` are authored round-13 work. The first draft's "inherited tree not clean" framing is withdrawn.
4. **F4 — U4 remains uncovered.** 0 `covers: U4` lines; 4 sourced entries, 3 of them covering U1–U3. S005–S010 are `queued`, so they are not citable as sole support. S006, S008, S009 and S010 still lack page revisions.
5. **F5 — Set-blind operability gap is named, not measured here.** Lesson M13 (`corpus/lessons/round-12.md:25`) states the gate's include/target/local checks compare counts and presence, not sets. QUALITY criterion 14 names the required exact-set form. Current gate status of that fix is unknown to this seat (GateImplement owns it).

## 5. Out of scope / not done

- No gate, registry, knowledge, or QUALITY edits. No verdict on C1 or C2.
- No census rerun, tests, builds, lint, formatters, selftest, regression, or live `hyprctl`/waybar probes.
- No commit, no push. Single output file: this draft. The duplicate `reports/EvidenceLedger.md` created earlier was removed.
- No reads of `~/.config`, `~/.local/share`, `~/.local/state`, sibling repos (other than the census script path named by the assignment), logs, or session data.

## 6. Tooling record

- Installs or upgrades by this seat: **none.** Used only `git`, `grep`, `sha256sum`, `python3`, `head`, `cut`, `awk`, `sort`, `rm` already present on the host.

## 7. Checks the main agent should run

1. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` — confirm exit code and the `W04` S030 finding against the retained `census-before.txt` (F1, F2).
2. `git status --short` — confirm the round-13 authored changes listed in §3b, nothing else.
3. Re-run C1 counts after any U4 entry lands: sourced entries, `covers:` lines, and `grep -lE '^covers:.*U4'`.
4. Harm watch per SCORECARD round-12 rule (selftest, `--regression`, navigation counter) — after all seats land, once.
