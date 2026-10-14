# VER-M11 — round-11 closeout verification: the arc's gate-revision ladder completed to the frozen revision, and the landed closeout note compared cell-for-cell (one arc claim)

Lane VER-M11, 2026-10-14 (round-11 wave, "the closeout verifier"). Dispatch
contract: re-derive one arc claim independently, poll with a 25-min cap, do
not edit. Window: dispatch ~21:31Z; poll `/tmp/w11-ver-m11-poll/poll.sh` →
`poll.log` (20 s cadence, 76 samples, 21:33:09Z → `POLL_END 21:58:09Z`).
**Read-only on every artifact**: the gate, the repo, the sibling trees were
only read; the gate's own read-only modes were run; no repo file other than
**this report** was written by this lane. No socket opened; no
compositor/session mutation; no external site; secrets shape-only. Marks:
**[O]** measured, **[I]** inference, **[U]** unknown. File path follows the
VER-M8/VER-M9/VER-M10 convention (`reports/r10-ver-m10.md`); the dispatch
named no path.

## Claim under verification (one)

The arc's **gate-revision ladder** — the chain of `tools/mado-verify.sh`
revisions across the arc as the round-11 closeout must carry it
(`plans/round-11.plan.md` §(a)(ii)/(iv), §(c)(iii); VER-M10's claim for round
10) — now **completed to the frozen revision**: (1) per-commit git-blob
sha256 / bytes / `wc -l`; (2) the per-revision selftest count; (3) the pin
lineage (`PIN_MADO`, `SPEC_SHA`, `TABLE_MADO`). Every cell re-derived one
level below the records: `git show <commit>:tools/mado-verify.sh` piped to
`sha256sum`/`wc -c`/`wc -l`; byte-copies of each revision re-run `--selftest`
from scratch; pins read from the gate's own source per revision. Extended for
the final round: the **frozen revision's whole row re-run** on the worktree
file (`--no-live`, live, `--regression`, boundary), and the round-11
artifacts landed in the poll window compared **cell-for-cell** against it.

## 1. Revision chain re-derived [O]

Creation commit = round 5 (`git log --diff-filter=A -- tools/mado-verify.sh`
→ `eead56b` 14:33:30 −03); rounds 0–4 (mint `74d3b7b` 09:50:45 … `3d9ba45`
13:57:18, five commits) carry no gate file at all.

| arc commit | date (−03) | gate blob sha256 | bytes | `wc -l` | selftest re-run |
|---|---|---|---|---|---|
| `74d3b7b` … `3d9ba45` (r0–r4, 5 commits) | 09:50:45–13:57:18 | — no `tools/mado-verify.sh` in tree | — | — | — |
| r5 `eead56b` (creation) | 14:33:30 | `d7edaab4bf108625d213393b…e32d0e13` | 45,334 | 1,098 | **28/28** rc 0 |
| `c03c249` (SHONEN commit) | 14:34:46 | `d7edaab4…` (identical blob) | 45,334 | 1,098 | (same bytes; one run covers both) |
| r6 `c8f6667` | 15:17:26 | `c4c1afb75dd1c8aa4d8ff9b8…1a625171` | 50,126 | 1,186 | **53/53** rc 0 |
| r7 `0c20a76` | 16:06:31 | `90d50cdd4d18410bd1e4222e…a3100bd` | 75,771 | 1,755 | **89/89** rc 0 |
| r8 `12c8f08` | 16:55:09 | `7da4ec5013583c9194253898…25f2f4f` | 131,612 | 2,887 | **217/217** rc 0 |
| r9 `de22dfd` | 17:47:30 | `93e43f8fe8b9bdd48c895ccc…bc00095` | 150,103 | 3,231 | **268/268** rc 0 |
| r10 `f7bfc9f` | 18:28:23 | `93e43f8f…` (identical to r9 — r10 adds **no gate edit**) | 150,103 | 3,231 | (same bytes; the r9 run is its run) |

The six byte-copies' own `sha256sum` equal the git-blob shas
(`/tmp/w11-ver-m11-ladder/<rev>.sh`); `f7bfc9f.sh` ≡ `de22dfd.sh` ≡
`93e43f8f…bc00095`. **The frozen revision is the r9 blob** — the ladder's
last distinct row — and the worktree file reads identical to it
(`sha256sum tools/mado-verify.sh` = `93e43f8f…bc00095` before and after every
run below; also unchanged at the cap 21:58:15Z).

## 2. Selftest column and pin lineage re-derived [O]

- Five byte-copies re-run `bash <rev>.sh --selftest` (15.6 s total battery):
  `MADO_SELFTEST: 28/28 / 53/53 / 89/89 / 217/217 / 268/268 assertions
  passed`, five rc 0 — every count identical to the records
  (`gate-mutation-proof.md:148/:150`; `LOG.md:297`;
  `snapshot-diff-receipt-r9.md:28-33`) and to the landed synthesis §2.1.
  Logs `/tmp/w11-ver-m11-ladder/<rev>.log`.
- Pins read from source per revision (`git show <rev>:… | grep -n`):
  - r7 `:749` `PIN_MADO=c4c1afb75dd1c8aa…d067cff1a625171` / `:750`
    `SPEC_SHA=c7ee75b97c38ac8f…12df1dd8` / `:752` `TABLE_MADO` 10/10 `KILLED`.
  - r8 `:1107` `PIN_MADO=d2bcdb31daea5d68…44ad327db62` / `:1108` · `:1110`.
  - r9 `:1290` `PIN_MADO=dc7c4141449891cd…b9c0514cb6f8fd` / `:1291` · `:1293`.
  - Lineage `c4c1afb7…1a625171` → `d2bcdb31…27db62` → `dc7c4141…cb6f8fd`;
    `SPEC_SHA` constant r7–r9.
- `VERSION_STR` reads `mado-verify.sh v1 (mado-shokunin round 5 / M5-2)` at
  **all six revisions including the frozen one** — the named base-residual,
  unchanged.

## 3. The frozen revision's whole row re-run [O]

Run 21:32:50–21:34:06Z against the worktree file (≡ frozen blob), cwd the
repo; gate sha identical before and after (`GATE_BEFORE`/`GATE_AFTER`
`93e43f8f…bc00095 UNCHANGED`). Logs `/tmp/w11-ver-m11-ladder/frozen-*.log`.

- `--no-live` rc 0 — `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only)`,
  `counts: pass=29 fail=0 unknown=0 skip=8 note=4`; boundary `PASS`
  (combined sha `bb2639d9a980…`). **Matches** the record (plan freeze,
  synthesis §2.2, M10-1 `nolive.log`).
- live rc 1 — `MADO_VERIFY: DIVERGED (3 fail, 0 unknown, 49 pass)`; fails
  `live.waybar.process` (no waybar process), `live.waybar.layer` (no layer
  surface), `live.waybar.tray` (rc 1); `counts: pass=49 fail=3 unknown=0
  skip=0 note=8`; boundary `PASS`, sha `bb2639d9a980…` (read-only held).
  **MOVED against the record's `CLEAN (52 pass, 8 notes)`** → finding F0.
- `--regression` rc 0 — `MADO_REGRESSION: PASS (case=mado-verify-hardened;
  target=dc7c4141449891cd…cb6f8fd)`; `REGRESSION_TABLE … match=10/10
  recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`;
  `REGRESSION_CASE … PASS (control=green restore=ok)`; `MUTATE_RESTORE: OK`;
  `REGRESSION_SPEC c7ee75b9…1dd8 (recorded pin matches)`;
  `REGRESSION_HARNESS 75ed934dc86360f5…19adc5` (78,904 B; recorded revision
  `b56c6e57…` — provenance, not gated); workdir
  `/tmp/mado-verify-regression.D3Pnk2` removed on PASS. **Matches** the
  record.
- The closeout's own M11-3 append re-ran the same battery at
  21:33:40–21:36:01Z — inside this lane's window — with identical counts
  (see §5): two lanes, same revision, same verdicts, concurrently [O].

## 4. Findings

- **F0 — the live plane moved: waybar is gone from the session (new this
  round).** `journalctl --user`: waybar was (re)started 18:12:34 −03 under
  `app-Hyprland-waybar-0a322a3a.scope`; at **18:21:17 −03 (21:21:17Z)
  `systemd-coredump`: "Process 3036215 (waybar) of user 1000 dumped core."**
  and the scope exits ("Consumed 2.188s CPU time over 8min 42.315s wall
  clock"). Alive at the 20:51Z receipts (prep `live.log` pid 3501967 / M10-1
  `live.log`, both `CLEAN (52 pass, 8 notes)`); absent at this lane's first
  live sample **21:32:50Z** and on direct re-probe 21:35:15Z (`pgrep -a
  waybar` → none; `hyprctl -j layers` level 2 → `[]`; tray query rc 1).
  Session otherwise pinned: walker 1203471, elephant 1203474, swaybg 1203358
  — the same PIDs as the round-11 plan's 20:54Z freeze sample; `wayland-1`
  socket mtime 13:11:08.394 −03 (plan: 13:11:09); Hyprland 0.56.2
  `efb5099…`; `wl_socket` `"wayland-1"` → **no session restart** [O].
  Cause of the crash **[U]** (core dumped; journal carries stack frames
  only; the crash precedes this lane's first sample by ~11 min — the live
  move is **not** an effect of this lane's runs, and the boundary line shows
  the gate left the config plane byte-identical). The closeout independently
  reached the same reading (its §2: "three consecutive live runs … diverged
  identically"; §8 re-ran it; disposition operator-owned). Consequence:
  every `52 pass` live figure in the records (synthesis §2.2, standing-use
  note, prep/M10-1 logs) is **stale as of 21:21:17Z**; the closeout's live
  re-sample reads `DIVERGED (3 fail)` unless waybar returns, and records the
  window (plan: "a MOVED reading is the round's first finding, never an edit
  of the baseline").
- **F1 — carried and still live: the `…a5171` tail is a prose corruption.**
  Correct tail `…1a625171` (last6 `625171`); the r7 PIN cell fails
  re-derivation. This lane's repo-local census [O]: synthesis
  `arc-synthesis.md:129` (table cell) + `:167` (lineage) = ×2; round-10
  record draft `:238` + `:267` = ×2; historical `LOG.md:297` = ×1 — five
  occurrences in-repo. The closeout note **registers** F1 with both values
  (its §5; wider count: "34 places across 13 files") yet its own ladder cells
  — `closeout-r11.md:77` (PIN cell) and `:83` (lineage) — print the bad tail
  again: **×2 new occurrences in the round-11 artifact set**. Correction
  owed as an appended erratum (the note itself says so); nothing was
  editor-fixed, per discipline.
- **F2 — carried and still live: one wrong pin tail in the round-9 receipt.**
  `snapshot-diff-receipt-r9.md:33` reads "`PIN_MADO` re-cut to
  `dc7c4141…db62`"; the actual re-cut (`de22dfd:…:1290`) ends
  `…c0514cb6f8fd`; `db62` is the r8 pin's tail. Blob `73b1466b6f876924…`
  unchanged; **not propagated** (the round-10 artifacts' `db62` uses are the
  r8 pin's correct tail). The closeout registers it likewise.
- **F3 — not propagated.** Among the artifacts this lane swept (synthesis,
  round-10 record draft, standing-use, LOG, SCORECARD, both r10 reports,
  round-11 plan, closeout note) `2,837` appears only in
  `reports/r10-ver-m10.md` (×3, as the flagged wrong value) **[O]**. The
  original wrong value stands in `walker-deep-r9.md:296` ("round 8 ended at
  2,837 L"; round 8 = 2,887 L / 131,612 B) — confirmed by this lane's grep
  and registered by the closeout.
- **F4 (this lane's numbering) — the synthesis's ladder still lacks the
  round-10 row / epilogue at the cap.** `arc-synthesis.md` blob
  `a5b4833141461810…` / 387 `wc -l` **unchanged all window**; no r10 row, no
  r11 row, no F1 erratum appended. Plan §(b) charters that terminal
  epilogue ("append, never edit"); the closeout note's §5 unknown list does
  not name it explicitly. Status at cap: **owed** — flagged for the
  settlement lane (M11-2) / the arc-end record; a mismatch here is a finding
  for the final commit, not an edit by this lane.

## 5. The landed artifacts compared [O]

- **`corpus/knowledge/closeout-r11.md`** (M11-1 §1–§7 + M11-3 §8 append),
  294 L by `wc -l`, sha256 prefix `670b5a396ecb8789…`, **stable
  21:47:49Z → 21:58:15Z**; untracked (uncommitted) at the cap. Landed name ≠
  the plan's predicted `arc-closeout.md`; this lane's poll watched the
  predicted name and kept `closeout=-` — detection came from the `git status`
  samples (dirty 4→5 at 21:47:49Z) [O]. The round-10 pattern (landing under
  a renamed path) repeats.
  - Ladder cells r5–r10: **match this lane's re-derivation** — sha16 / L / B
    / selftest / PIN for every row including r10 `f7bfc9f` (its r1–r4
    "(empty blob, 0 L)" is the same fact as this lane's "no gate file", the
    piped command's empty-blob result). PIN cells: r7 `…a5171` = F1
    (in-round ×2), r8/r9 correct.
  - Battery receipts: **identical line-for-line** to this lane's independent
    re-run (§3): nolive `29/4` + boundary `bb2639d9a980…`; regression PASS
    target `dc7c4141…f8fd`, table 10/10 flips 0, spec `c7ee75b9…1dd8`,
    harness `75ed934d…`; live `DIVERGED (3 fail, 49 pass)` first fail
    `live.waybar.process`; frozen revision `93e43f8f…` at HEAD `f7bfc9f`.
  - Kill ladder r5 `4/10 (40 %)`: receipt-validated by this lane
    (`/tmp/w10-m10-1/mut-r5.log`: `killed=4 survived=6 kill-rate=40%`,
    `MUTATE_RESTORE: OK`, target pristine `d7edaab4…`); not re-run here (AUD
    territory) **[U]** as an independent measurement.
  - Not re-derived by this lane (scope): the note's snapshot-pair worked
    example (`MADO_DIFF: CHANGED/SAME`, M11-3 §8), its (a10)/(b10)/(c10)
    handoff table, its F4/F5 (standing-use stale path; `SKILL.md:1314`
    citation), the terminal disposition ledger, §8's snapshot rows.
- **Round-11 landings observed in-window [O]**: ` M SKILL.md` +122/−1 (lane
  M11-4's "Round-11 — the arc's end: final pointers" append; dirty from
  21:34:09Z, still dirty at cap); `closeout-r11.md` (above);
  `corpus/lessons/round-10.md` (note: round **10**'s lesson, not round 11's);
  `plans/completion-evidence.md`; `reports/r11-aud-m11.md`. The gate was
  untouched all window (`93e43f8f…` at every sample); the synthesis
  untouched (F4).
- **No commit by the cap**: HEAD `f7bfc9f` at every one of the 76 samples;
  `git status --porcelain` at 21:58:15Z = ` M SKILL.md` + 4 untracked
  (closeout note, `corpus/lessons/`, `plans/completion-evidence.md`,
  `reports/r11-aud-m11.md`).

## 6. Spot-checks (3, named)

1. **Ladder complete** — 12 arc commits walked; 5 distinct gate blobs + the
   two identity rows (`c03c249` = r5 blob; `f7bfc9f` = r9 blob); r5–r9
   sha/bytes/lines/selftest cells 20/20 reproduce, the r10 row (4/4)
   reproduces, `c03c249` identity ✓; of the three PIN cells, r8/r9 reproduce
   and r7 fails (F1).
2. **Selftest column + frozen row** — five byte-copies re-run, five rc-0
   runs, counts 28/53/89/217/268 reproduce; frozen row `--no-live` ✓,
   `--regression` ✓ 10/10 flips 0, **live MOVED** → F0; gate sha unchanged
   before/after the whole battery; the closeout's M11-3 append re-ran the
   same battery in-window with identical results.
3. **Live-plane move + closeout cell-for-cell** — crash line + scope receipt
   from `journalctl --user`; live-pin probes (pgrep / layers / tray / PIDs /
   socket mtime); boundary `bb2639d9a980…` PASS in every run; the landed
   closeout note's §2/§8 readings match this lane's, cell-for-cell.

## Unknowns

- [U] **The round-11 commit**: not landed at the cap (HEAD `f7bfc9f`; five
  dirty/untracked paths). The closeout note, this report, and the record
  family's settlement land later; every row above binds to `f7bfc9f` and
  moves only with the gate (`93e43f8f…`).
- [U] Waybar's crash cause (core dumped; stack frames only in the journal)
  and whether it returns before the settlement's live re-sample — the live
  receipt depends on it; restart is operator-owned (the closeout agrees).
- [U] Whether M11-2 / the arc-end record appends the synthesis epilogue and
  the F1 erratum as chartered (F4) — outside this lane's scope (no edit).
- [U] If the settlement edits the gate, the frozen revision re-cuts; this
  report names the pre-move bytes `93e43f8f…bc00095`.
- [U] Harness state is live-sibling: read `75ed934d…19adc5` (78,904 B) at
  21:33Z; printed as provenance, not gated.
- [U] Historical suite counts were re-run on one toolchain (bash 5.3.15),
  one host; another toolchain was not tested.

Boundary: repo read-only; no commit; no edit; the single written file is
this report; scratch `/tmp/w11-ver-m11-poll/` (`poll.sh`, `poll.log`,
`report-draft.md`) and `/tmp/w11-ver-m11-ladder/` (6 byte-copies, 5 selftest
logs, 3 frozen-row logs); substrates (`~/.config`, `~/.local`, omarchy
checkout, tameshi harness) touched only by the gate's own read verbs; no
socket opened; no external site.