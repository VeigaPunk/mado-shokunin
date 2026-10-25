# ScribeGate — `## Gate` draft for corpus/lessons/round-34.md

**Scope:** draft only, at
`.ufo/waves/round-34/scratch/ScribeGate/gate.md`. The L1 writes the lesson;
no corpus file was edited. House style follows `corpus/lessons/round-33.md`
§ Gate: opening ledger line, then admit bullets (quotes located in the
fetched bytes), refuse bullets (reason + flip), quarantine hand-check, and
the considerthese mined-not-edited note.

## The set

**Admits (2, from `assimilation/append-block.md`):**

- `S201` — `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp`,
  opened 2026-10-24. Quote `"$XDG_RUNTIME_DIR/hypr does not exist, falling
  back to /tmp/hypr"` (8 words) is a contiguous substring of the committed
  blob at line 38 — verified by `ExecQuoteLint` (`grep -anF` on
  `.ufo/waves/round-34/fetch/S201.bin`, sha256 `799bf02f…f9e`, 6550 B) and
  re-located by `ScoutS201` under `IPC::getSocketFolder`.
- `S202` — `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp`,
  opened 2026-10-24. Quote `m_ipc.registerForIPC("activewindow", this);` is
  a contiguous substring at line 27 (sha256 `5df496eb…9846`, 8324 B).
  Three-way digest agreement (blob / `SOURCES.md` / `c1/frozen.json`):
  `ExecFetches.md`, all AGREE.

Both appended at `fa7ba11346116672352b5d41494141c5c4d738d0`
(`ExecAppendAudit`: zero field diffs, schema pass). Province check IN:
`CritProvince.md`.

**Refuses (12, from `assimilation/quarantine-slice`; 13th row S189 is
PRESENT, not refused):**

| rows | reason | flip |
|---|---|---|
| S195, S205, S228 | localization surfaces outside PROVINCE.md (same rule as r33's `two-literature-drift-r26.md` refuse) | tier-A/B desktop/compositor source opened by this lane |
| register S201 (arXiv) | id collision — lane S201 binds `backend.cpp`; arXiv URL absent from registry | fetched bytes under a fresh id + in-province claim; never under S201 |
| S224 | transient host cache file, not a source | reclassify as own-work probe output under `.ufo/evidence/` or a durable artifact |
| S199, S200 | CSDN locators, tier C, never fetched; `unreachable` ≠ fabrication | tier-A/B desktop/compositor source opened by this lane |
| S209, S222, S223, S225, S235 | register cites only a `## Gate — Snnn` anchor; no locator ever named → UNVERIFIABLE | resolvable URL/path naming the claimed bytes, opened by this lane |

Classifications per `ScoutQuarantineA` (payload-absent slice) and
`ScoutQuarantineB` (prose slice); all checked against `SOURCES.md` 2026-10-24.
Requirement met: ≥1 admit and ≥1 reject, both drawn from the assimilation
package.

## Notes recorded in the draft

- C2's S189 re-open: line 169 carries `MAX_QUEUED_EVENTS = 64` (`ScoutS189`);
  SCORECARD publishes `r34-s189-line: line=169`. Adopted r32, not re-appended.
- considerthese/2026-10-24.md: six proposals, all marked "proposals only;
  not acted on" (`ScoutConsiderA`); mined, not edited.
- ID gap S196 → S201 named as deliberate reservation (`ExecAppendAudit`
  observation), not a copy error.
- Caveat the draft does not hide: the registry `teaches` cells are prose
  paraphrases, not verbatim spans (`ExecQuoteLint` finding); the gate-quote
  lines in `corpus/knowledge/waybar-module-text-route-r25.md` are the
  located-quote authority.

Lane bounds: leaf member — no subagents dispatched.
