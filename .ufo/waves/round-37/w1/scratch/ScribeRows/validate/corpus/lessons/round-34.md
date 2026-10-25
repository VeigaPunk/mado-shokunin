# Round 34 lesson

Author: Kimi fresh L1. Date: 2026-10-24. This file does not rewrite the
round-32 or round-33 reports, and it does not amend the round-33 counters
(`.ufo/waves/round-33/c1/count.py`, `.ufo/waves/round-33/c1/frozen.json`,
`.ufo/waves/round-33/c2/count.py`); their blob ids are unchanged between the
round-33 freeze `9a46ccf3282117f960b8d53cd71599a91f388ee3`, the round-33 tip
`69f72100bee31a60b811f8fbbe7796db883e17b3` and this round's tip.

## Gate

The round-33 coverage counter was killed by a symlink crib before any corpus
append. This round froze a NEW counter, `PRED-C1-r34-v1`, at
`3420e827bd7b21b1374b23245526554ffd20d096` with pre-data receipts, and landed
data only afterwards at `fa7ba11346116672352b5d41494141c5c4d738d0`. The
predicate was not rewritten after seats scored it. The assimilation package is
`.ufo/waves/round-34/assimilation/`: `append-block.md` (two rows),
`quarantine-slice` (thirteen register rows), `reg-ids` vs `staged-ids`
(190 vs 140 ids, `collisions` empty), and the indented-collision proof
`controls/indented-guard.txt` (`spaced=S197 column_zero='' collisions='S197'`).
Fetch digests agree three ways — committed blob, `corpus/SOURCES.md`,
`c1/frozen.json` — re-run in
`.ufo/waves/round-34/w1/reports/ExecFetches.md`.

- Admit (appended `corpus/SOURCES.md:203-204` at
  `fa7ba11346116672352b5d41494141c5c4d738d0`):
  - `S201` — `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp`,
    opened 2026-10-24, 6550 B, sha256
    `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e`.
    Located quote (line 38; authority is the gate-quote line of
    `corpus/knowledge/waybar-module-text-route-r25.md`):
    `$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr` —
    8 words, a contiguous substring of the committed blob.
  - `S202` — `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp`,
    opened 2026-10-24, 8324 B, sha256
    `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846`.
    Located quote (line 27; same authority):
    `m_ipc.registerForIPC("activewindow", this);` — a contiguous substring
    of the committed blob.
  Both are in-province: Waybar is named in `PROVINCE.md` and the lane already
  absorbs compositor C++ at S189 — see
  `.ufo/waves/round-34/w1/reports/CritProvince.md` (verdict IN PROVINCE). The
  registry jumps S196 → S201; S197–S200 stay unallocated and the never-reuse
  rule bars filling that gap later.
- Refuse (assimilation package `quarantine-slice`, twelve of thirteen rows;
  no locator of those rows was fetched this round and none is needed to
  refuse them):
  - `S195`, `S205`, `S228` — localization surfaces (SJTU arch-wiki-docs-zh-cn
    package, Arch-wiki interwikimap JSON, `cn-export-hyprland.html`).
    Documentation localization is outside PROVINCE.md, the same rule that
    refused `two-literature-drift-r26.md` in round 33. Flip: a
    desktop/compositor surface cited only from tier A or B, opened by this
    lane.
  - `S201` of the register — the register's id space is the campaign's
    pre-remap staging ids, not this lane's registry ids, so its "S201" is a
    different document (`https://arxiv.org/abs/2604.18860`, now packaged as
    S212/S274/S319). The lane's S201 is unambiguous inside this repo and the
    arXiv URL is absent from the registry; no renumber is warranted. Flip:
    fetched bytes under a fresh id plus an in-province desktop/compositor
    claim — never under the lane's S201. Evidence:
    `.ufo/waves/round-34/w1/reports/CritDupIdSpace.md`.
  - `S224` — `/home/vgpnk/.cache/ai-usage/status.json` is a transient host
    cache file, not a source; its `updated_at` quote is stale on every read.
    Flip: reclassify as own-work probe output under `.ufo/evidence/`, or a
    durable published artifact.
  - `S199`, `S200` — CSDN locators (tier C) never fetched; `unreachable` is
    not fabrication and is not a locator this lane opened. Flip: a
    desktop/compositor surface cited only from tier A or B, opened by this
    lane.
  - `S209`, `S222`, `S223`, `S225`, `S235` — the register cites only a
    `## Gate — Snnn` prose anchor; no locator was ever named, so the row is
    unverifiable, not fabricated. Flip: a resolvable URL or path naming the
    row's claimed bytes, opened by this lane.
- Quarantine hand-check this round (scout, thirteen rows,
  `.ufo/waves/round-34/scratch/ScoutQuarantineA/table.md` and
  `.../ScoutQuarantineB/table.md`): the register's `S189` row is
  IN-REGISTRY-SAME-ID — the register's quoted span is the `formatEvent`
  `eventString` assignment, which sits at **line 128** of the pinned
  `EventManager.cpp` (6479 B, sha256
  `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`), so the
  register's `payload-absent` mark on that row is a false negative. The
  queue-cap constant is a different quote at **line 169**
  (`const size_t MAX_QUEUED_EVENTS = 64;`). Both line numbers are correct for
  their own quote; the round-33 closure's routed correction conflated the two.
  S189 was adopted in round 32 and is not re-appended. Every other slice row
  is NOT-IN-REGISTRY by URL.
- Literature reject RESTATED against the opened file's own ids.
  `two-literature-drift-r26.md` cites **S206, S209, S210, S211** — `S199`
  appears nowhere in it, and S195/S198/S199 in the round-32 lesson were ids
  from the staged row register, not from the file. Its community tier-C rows
  are **S210 and S211** (CSDN posts), so the reject rests on two grounds
  that still hold: documentation localization is outside PROVINCE.md, and
  tier C community sources may not be the sole support. Flip: a
  desktop/compositor surface cited only from tier A or B, opened by this
  lane. Evidence: `.ufo/waves/round-34/w1/reports/CritLiterature.md`.
- considerthese/2026-10-24.md proposals 1–6 carry the file's own marking
  "proposals only; not acted on". ONE was mined this round — item 4 (propose
  the next Hyprland config table) — and grounded through the lane's own bar:
  `hyprctl windowrules -j`, `layerrules -j` and `rules -j` all print
  `unknown request` on this host's v0.56.2, so the r25–r27 predict-table
  method does not transfer to the window-rule table; `hyprctl monitors -j`
  does answer. It lands as a lesson (planning knowledge about oracle
  availability), not as a QUALITY.md criterion and not as a SOURCES row. The
  reflection is a pointer, not evidence. Evidence:
  `.ufo/waves/round-34/w1/reports/ScribeConsider.md` and
  `.ufo/waves/round-34/scratch/ScribeConsider/note.md`. The considerthese
  directory was mined, never edited.

## Mistakes

- class: instrument. evidence: `.ufo/waves/round-33/w1/reports/CriticC1Junk.md`
  and `.ufo/waves/round-33/controls/c1-symlink-fix-demo.txt` — the round-33
  frozen counter printed `TARGET_MET` on a symlink crib. captured-by: the
  round-33 pre-data control set did not include a symlink to the real fetch
  blobs. fix: this round's `PRED-C1-r34-v1` does not follow symlinks, pins
  the fetch digest, and walks every path component; its committed
  pre-data receipts show the symlink crib, the symlinked-parent tree, the
  symlinked-entry tree, the symlinked-sources tree, the hardlink tree, the
  entries-only tree, the rows-only tree, the used-by-prefix tree and the
  do-nothing control all printing `TARGET_MISSED` (exit 1), while a
  regular-file golden tree prints `TARGET_MET` (exit 0). Shown able to fail.
- class: instrument. evidence: `.ufo/waves/round-34/w1/reports/MutC1Drop.md` —
  clause-drop mutants of the round-34 counter. captured-by: the mutation
  suite, which the round-33 round did not run on its own counter. fix: the
  per-component path walk and the whole-token used-by equality are
  load-bearing (their mutants wrongly meet `controls/extra/symlink-parent`
  and `controls/extra/used-by-prefix`); the sha256 pin and the nlink check
  are load-bearing against scratch cribs. Two clauses are honestly redundant
  under this frozen spec: the 1–25 word bound cannot fail once
  `found == quote` holds, and the `S_ISLNK`/`O_NOFOLLOW` pair is only
  TOCTOU protection that no static tree can kill. Both are recorded rather
  than hidden.
- class: ledger. evidence: the round-32 SCORECARD C1 row said target met at
  `cited_entries=3` while the frozen counter printed 7, and the round-33
  lesson cited the register's S189 quote at "line 128" without saying which
  quote that was. captured-by: none at write time (the row and the lesson
  line were written before the falsifier). fix: the appended calibration
  line, which `PRED-C2-r34-v1` accepts and a `line=128` card rejects, and
  this round's appended correction in `corpus/lessons/round-33.md` naming
  both lines and both quotes. The false round-32 row was corrected by
  appending, never by rewriting.
- class: id-space. evidence: the campaign's
  `absent-defect-register.md` names an `S201` that is not this lane's
  `S201`, and the merge package carries the lane's S186–S189 URLs again as
  S199/S200/S260. captured-by: the id-collision guard, which only compares
  the lane registry against the staged ids and cannot see the register's
  separate id space. fix: the guard was re-proved able to fail on the
  indented `  | S002 |` fixture before the first append
  (`controls/indented-guard.txt`), and the register's id space is now named
  as the campaign's pre-remap staging ids, with the remap base ("registry
  ends at S196") recorded as stale. The lane renumbers nothing; the burden
  is on the package. Evidence:
  `.ufo/waves/round-34/w1/reports/CritDupIdSpace.md`.
- class: hygiene. evidence: the round-33 closure found 19 untracked paths
  (twelve seat scratch trees, six control fixture trees, and
  `scratch/ExecK2Receipts` at 495,961,904 bytes) that no round report named.
  captured-by: none — the lane committed receipts without their fixture
  inputs, so the receipts could not be re-derived from committed bytes
  alone. fix: the six control fixture trees and the twelve seat scratch
  trees are committed this round, so every round-33 receipt is re-derivable
  from committed bytes; `ExecK2Receipts` is three throwaway git clones whose
  outputs are already pasted verbatim into the committed
  `.ufo/waves/round-33/w1/reports/ExecK2Receipts.md`, and it was moved out of
  the lane tree to `/fast/scratch/mado-r33-k2-receipts/` rather than swept.
  Named dispositions, not a silent sweep.
