# WaybarVersion — historical installed-version anchors and retained equivalence limits

**Seat:** `MadoR16.WaybarVersion` (scout, leaf; no subagent dispatch)
**Date:** 2026-10-20
**Baseline:** `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`; the L1 integration tree
(`corpus/SOURCES.md`, the round-16 note and lesson) was uncommitted at report time.
**Scope:** U7 is **tagged-source only**. This report returns the historical installed-version
anchors and the retained tag/source limits. It claims **no installed binary/source
equivalence** and asks for no note change.
**Posture:** this seat ran no host or package query and no
package/service/compositor/input/screenshot/command-producer probe, and no install or
upgrade. Repo reads plus read-only HTTPS source reads only. Installed nothing.

---

## 1. Historical installed-version anchors

Every value below is a *recorded sample* with its own date. None was re-measured this round.

| # | Anchor | Date | Recorded fact | Provenance in the artifact | Establishes | Does not establish |
|---|---|---|---|---|---|---|
| A1 | `corpus/knowledge/waybar-walker-plane.md:37` | 2026-10-14 | `waybar --version` → `Waybar v0.15.0` | MADO-2 (`LOG.md:18`); note header `:3-4`; re-measured in R2-E4 | the then-running binary's upstream version string | pkgrel, package identity, build/source provenance |
| A2 | `corpus/knowledge/waybar-walker-plane.md:400-407` | 2026-10-14 | R2-E4 re-measure (`:405`): `versions v0.15.0 / 2.17.0 / v0.1.8 / v0.9.6 / 0.3.2` | append-only errata block | repeat stability of A1 on the same host sample | anything about the package revision |
| A3 | `corpus/knowledge/waybar-walker-semantics.md:22` | 2026-10-14 | `waybar --version` → `Waybar v0.15.0`; pkg `0.15.0-3` | round-3 MADO-R3-1; method `:434` lists `man 5 waybar*`, `pacman -Ql/-Qi` | **both** the binary self-report and the pacman version in one note | that the binary was built from that package revision; the exact `-Qi` fields |
| A4 | `corpus/knowledge/remaining-planes-census.md:246` | 2026-10-14, 17:39:02–17:41:45Z | package census: `waybar 0.15.0-3` | §4; verb list `:19` includes `pacman -Q`; probe window `:14` | independent package-version observation | origin/repository/packager/signature; the binary self-report |
| A5 | `corpus/knowledge/config-health-report-r3.md:900` | 2026-10-14, 14:40–14:48 UTC | command block `waybar --version; …` annotated `v0.15.0` | end-to-end pass; probe window `:3-4` | a third binary self-report inside a broader health pass | package identity or pkgrel |
| A6 | `SKILL.md:22-23`, `:112` | standing pin | "waybar v0.15.0"; `:112` repeats it and "no IPC/query verb in 0.15.0" | cites MADO-1 §9 / MADO-2 §1 | the lane's reuse pin for claims below | pkgrel; tag/source identity |
| A7 | `.ufo/evidence/round-12/l2-scout.md:3` | 2026-10-19 | `pacman -Q` → "Waybar 0.15.0-3" | round-12 evidence file (outside `corpus/knowledge/`) | the **freshest** installed-package observation in the lane | a `--version` re-run; package origin; corpus-note status |
| A8 | `arc-synthesis.md:228,301`; `closeout-r11.md:42`; `corpus/README.md:17`; `SCORECARD.md:14`; `LOG.md:167,245`; `plans/round-8-record-draft.md:345` | derived | restate `v0.15.0` / `0.15.0-3` / "no IPC verb" | restatements, not new commands (the plan draft is an assertion) | propagation of the pin | independent evidence |

**Corpus gap.** No corpus note re-measures `waybar --version` after 2026-10-14, and the
freshest installed-*package* observation (A7, 2026-10-19) is evidence, not knowledge. The
landed round-16 note deliberately makes no host-version claim; it lists "installed
binary/source equivalence" as `[UNK]` (`waybar-observation-boundaries-r16.md:73-74`).

**Two strings, two identities.** `Waybar v0.15.0` is the upstream version string compiled into
the binary; it cannot show an Arch `pkgrel`. `0.15.0-3` is the pacman identity
`pkgver-pkgrel`; only a package query records it. Substituting one for the other is the first
equivalence error this lane can make.

---

## 2. Provenance of the already-opened tagged sources (not installed equivalence)

- `refs/tags/0.15.0` is a lightweight tag at commit `90b209add8937514d0a987aa842e701bd8f1232e`
  (`https://api.github.com/repos/Alexays/Waybar/git/ref/tags/0.15.0`, read 2026-10-20).
- Fetched at that commit, `man/waybar-custom.5.scd` is 6656 B / 250 lines, sha256
  `efb6a63a…`, and `src/modules/custom.cpp` is 8746 B / 292 lines, sha256 `2232f7f7…` —
  exactly the digests in `.ufo/waves/round-16/evidence/source-bindings.json`.
- Therefore the recorded S053/S054 digests are **commit-bound**, not merely ref-name-bound.
  The tag is lightweight, so the commit SHA is the immutable identity; a future row may cite it
  beside "tag 0.15.0" (L1-owned).

---

## 3. Retained equivalence limits

| Tier | Relation | Status | What it licenses | What it does not license |
|---|---|---|---|---|
| T0 name | installed `pkgver 0.15.0` ↔ tag name `0.15.0` | `[OBS]` string match (A3/A4) | selecting the tag as the upstream release matching the installed version | package revision, origin, byte identity |
| T2 documentation | tag `.scd` ↔ installed `waybar-custom(5).gz` | rendered-text equivalence at cited passages, **not byte equality** | the documented contract at those passages, as `[INF-docs]`/`MAN` history | a full scd↔roff proof; installed-page digest equality |
| T3 binary | tagged source ↔ installed binary | **not established, not needed or claimed** | — | any claim that the installed binary is a build of these bytes |
| T4 live text | tagged source ↔ current bar output | **not established** (U7 boundary; no IPC/query verb) | — | rendered text, tooltips, CSS result |

T2 detail: the tag `.scd` is scdoc **source**; the installed page is scdoc-rendered **gzip**.
A digest of one can never equal a digest of the other; the valid relation is rendered text.
The round-3 installed-man quotes corroborate three loci against the tag text after emphasis
removal: "loops itself" (`semantics:137` ↔ `.scd:42`), the signal range
(`semantics:192` ↔ `.scd:55`), and the JSON field set `text/tooltip/class/percentage`
(`semantics:161-162` ↔ `.scd:154`). `CustomMan.md:189-203` extends that to a passage-level
rendered comparison (scdoc 1.11.5) and states the same non-byte limit. The peer-recorded
installed-man sha256 `c9938e44…` has no recorded projection (gz bytes vs `zcat` text), so it
cannot be hash-compared to the `.scd` or to a rendered page without re-derivation.

---

## 4. Cross-check against the landed round-16 artifacts

- The note states the correct limit: "The historical host version in earlier notes does not
  prove installed-binary source equivalence or current behavior"
  (`waybar-observation-boundaries-r16.md:9-11`), and lists installed binary/source
  equivalence under `## Unexercised rendering` (`:73-74`). **No change is required.**
- The lesson rejects "tagged source as installed binary equivalence"
  (`corpus/lessons/round-16.md:33-34`). That rejection stands; this report does not contest it.
- S054's row scope already says "not installed-binary equivalence" (`SOURCES.md:66`). Correct.
- Optional, L1's call: cite commit `90b209a…` beside "tag 0.15.0" in the S053/S054 anchors.
  The note's blanket `[INF-docs]` label also covers `custom.cpp`; the lane's precedent labels
  tagged implementation code `[SRC]` (`output-colour-boundaries-r14.md:36`) and tagged
  protocol source `[OBS-source]` (`input-debugging-boundaries-r15.md:34-35`). Labeling nuance
  only, not an equivalence defect.
- The reserved ids are S053–S055 and L1 owns the registry; this report adds no row and no
  package-provenance claim.

---

## 5. Remaining unknowns

1. **Installed origin/provenance** — `pacman -Qi waybar` Repository, Packager, Build Date,
   Install Date and Validated By were never retained in the corpus.
2. **Binary integrity/reproducibility** — no `pacman -Qkk waybar`, no installed binary digest,
   no reproducible-build record. T3 stays `[UNK]` and is not claimed.
3. **Installed man projection** — peer digest `c9938e44…` has no command/projection; the
   installed page cannot be hash-compared to the `.scd` by construction (T2).
4. **Current installed version** — last observed `0.15.0-3` at 2026-10-19 (A7); no later
   observation. Package operations are paused host-wide, so drift is unlikely but unobserved.
5. **Tag-era fragility** — `0.15.0` is a lightweight tag; the commit SHA and file digests pin
   it today. Upstream `master` (2026-10-19, `c15ec02…`) documents materially more fields and
   must not be cited as `0.15.0` (era warning in `CustomMan.md:29-34`).

Future authorized recheck (read-only; **none run here**): `pacman -Q waybar`;
`pacman -Qi waybar`; `pacman -Qkk waybar`; `sha256sum` of
`/usr/share/man/man5/waybar-custom.5.gz` and of its `zcat` text with the projection named;
`curl -fsSL https://api.github.com/repos/Alexays/Waybar/git/ref/tags/0.15.0`. A rendered-page
comparison requires the same scdoc version (1.11.5 observed by the peer) and a normalized
text projection.

---

## 6. Tooling and boundary record

- Installed, updated or removed **nothing**; ran no `pacman`, `-S`, `-Sy`, `-Syu`, `-U`, `-R`,
  downgrade or service operation.
- No live compositor, service, input-device, screenshot or command-producer probe. No
  `waybar`, `hyprctl`, `busctl`, signal or producer execution.
- Commands actually used: `grep`, `sed -n`, `wc`, `sha256sum`, `b2sum`, `curl -fsSL` against
  the public URLs above, `git status`/`rev-parse`, and file reads. All source bytes are public
  web content; no host or package state was queried.
- Read `corpus/lessons/round-15-verifier-spotcheck.md` (the assigned
  `.ufo/waves/round-15/...` path does not exist; the file is under `corpus/lessons/`).
