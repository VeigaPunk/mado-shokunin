# AUD-M11 — round-11 final audit: the closeout's two claims re-derived (the handoff; the frozen revision) and the gate receipt re-run

Lane AUD-M11, 2026-10-14 (round-11 wave, "the final audit"). Window
21:30–21:49Z (local 18:30–18:49 −03:00), single host, bash 5.3.15. Write
scope: **this file only** — every audited object was read, never edited; the
gate was executed from frozen copies under my scratch `/tmp/w11-aud-m11/`.
Read-only throughout: `sha256sum`/`wc`/`grep`/`sed`/`git show`; the gate's own
modes; the tameshi harness consumed read-only; no substrate file written; no
compositor/session mutation (no launcher, no socket connect, no
`omarchy theme set`, no restart); no `git status`/`fetch` on the omarchy
checkout; secrets shape-only; no external site.

Process note (named, not hidden): at 21:36:33Z my battery script's closing
`sha256sum … > gate.sha.after.txt` fell after an internal `cd` and wrote one
scratch line-file into the mado worktree; I removed it at ~21:37:0xZ and the
tree returned to the concurrent ` M SKILL.md` only. The slip is visible in
SCR-M11's poll (samples 21:36:42Z/21:37:02Z, `?? gate.sha.after.txt`); nothing
was committed and no audited byte moved. Recorded because the discipline says
measured, not smoothed.

Objects audited, sha-pinned at my reads (worktree artifacts uncommitted at
write; HEAD `f7bfc9fe149bc94057323964e7cb0411f6f89e25`):

| object | sha256 / size | read |
|---|---|---|
| `tools/mado-verify.sh` (= blob at `f7bfc9f`) | `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095` · 3,231 L / 150,103 B | frozen copy `gate-f7bfc9f.sh`; identical before/after every run |
| `corpus/knowledge/closeout-r11.md` (M11-1 note + M11-3 §8 append; in flight) | `85f6f817…` 234 L / 15,173 B → `979fcade…` 234 L / 15,174 B (1-byte drift mid-read) → `670b5a396ecb8789430709a8e490c93a5672399401e6a8209f26e93645d818a1` 294 L / 19,250 B (with §8) | full text ×2 + §8 |
| `reports/closeout-r11.md` (M11-3 receipt draft) | `581749946068adc429e8fffa80e624b4f14abbca6095223ef574ca68c3a79d50` · 169 L / 11,090 B | full text; appeared 21:39:22Z, gone by 21:40:35Z — folded into the note §8 |
| `plans/completion-evidence.md` (PACK-M pack; in flight) | `e63272c4b555213b1087d8dc7a1d4bf8304265a24ed105eb6d4a850e205db659` · 195 L / 14,551 B | head |
| `corpus/lessons/round-10.md` (M11-2 settlement; in flight) | `d7b4708e864fca29…` · 226 L / 16,423 B | head + `## Gate` |
| arc-synthesis / standing-use / record family at `f7bfc9f` | table in §3.3 | `git show` |
| tameshi `tools/mutate-and-run.sh` (sibling, read-only) | `75ed934d…adc5` (recorded `b56c6e57…` — provenance, not gated) | executed (two replays) |

Tags: **[O]** measured by this lane; **[OBS-record]** cited from a round
record; **[I]** inference; **[U]** unknown.

## 1. Verdict table

| # | claim (source) | my re-derivation (method) | result | verdict |
|---|---|---|---|---|
| C1 | **The round-10 handoff** — closeout note §4 (a10)/(b10)/(c10), stage (a) | `git show f7bfc9f:<path> \| sha256sum` + `wc -lc` per artifact; `grep -c PENDING`; `git show --stat/--numstat` | (a10) **yes** `arc-synthesis.md` `a5b4833141461810…` / 387 / 30,796; (b10) **yes** `gate-standing-use.md` `aaa2e625253e881e…` / 361 / 22,931; (c10) **partly** — landed: SCORECARD 22 L `5f1df3f4…`, LOG 301 L `81c60ea8…`, SKILL 1,424 L `e9e67efe…` (**+89/−1** by numstat; the note's "+90/−1" cell off by one — F2); not landed at `f7bfc9f`: README 8 rows / 21 notes → **13 unrowed**, lessons 0 (→ `round-10.md` landing in flight), drafts ⟨PENDING⟩ **13/19/19/22**, walker-deep §10/§11 errata, AGENTS pointer | **PASS** — every measured cell agrees; one delta cell named (F2) |
| C2 | **The frozen revision + its whole row** — closeout §2/§8 | gate blob hash chain `de22dfd`→`f7bfc9f`; my own battery from a frozen copy + repo regression; own snapshot pair; own r5 rung replay | gate `93e43f8f…` / 3,231 / 150,103 identical at both commits and before/after every run of mine; selftest **268/268** rc 0; `--no-live` **CLEAN** (29/4) rc 0; live **DIVERGED** (3/49) rc 1 — the three waybar rows, session move (F3); regression **PASS** (`match=10/10`, flips 0, restore OK, target `dc7c4141…`, spec `c7ee75b9…`); snapshot pair → `MADO_DIFF: SAME` (rows 60→60) rc 0 | **PASS** |
| R1 | the gate receipt: `--selftest` | frozen copy | `MADO_SELFTEST: 268/268 assertions passed` rc 0 | PASS |
| R2 | the gate receipt: `--no-live` | frozen copy | `CLEAN (29 pass, 4 notes)`, `pass=29 fail=0 unknown=0 skip=8 note=4`, boundary `bb2639d9a980…`, rc 0 | PASS |
| R3 | the gate receipt: live | frozen copy | `DIVERGED (3 fail, 0 unknown, 49 pass)` rc 1; first fail `live.waybar.process`; boundary `bb2639d9a980…` PASS | **NAMED** (session move, not smoothed; identical across the wave's lanes) |
| R4 | the gate receipt: `--regression` | repo worktree; gate sha checked before/after | `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=dc7c4141…)` rc 0; `REGRESSION_TABLE … match=10/10 … flips=0`; spec pin `c7ee75b9…` matches; `MUTATE_RESTORE: OK`; harness `75ed934d…` provenance | PASS |
| R5 | the ladder (five revisions) | `git show <c>:tools/mado-verify.sh` + each blob's own `--selftest` (my runs) | 5/5 byte-exact: `d7edaab4…` 1,098 / **28/28** · `c4c1afb7…` 1,186 / **53/53** · `90d50cdd…` 1,755 / **89/89** · `7da4ec50…` 2,887 / **217/217** · `93e43f8f…` 3,231 / **268/268**; all rc 0 | PASS |
| R6 | the kill ladder's bottom rung (r5 4/10) | my spec extraction from the frozen gate heredoc + tameshi replay | spec = 2,141 B / 10 `@defect` / `c7ee75b9…1dd8`; `killed=4 survived=6 inconclusive=0` (**40 %**), control GREEN, `MUTATE_RESTORE: OK` | PASS |
| R7 | the snapshot pair → `MADO_DIFF` | own pair (scratch only) | `MADO_SNAPSHOT: WRITTEN` ×2 (rows=60 pass=49 fail=3 note=8); `MADO_DIFF: SAME (rows 60→60; … all counters 0)` rc 0 | PASS |

## 2. Re-run detail (commands and receipts)

- **Freeze.** `cp tools/mado-verify.sh /tmp/w11-aud-m11/gate-worktree.sh`;
  `git show f7bfc9f:tools/mado-verify.sh > gate-f7bfc9f.sh` — all three sha
  `93e43f8f…bc00095`; `git diff de22dfd..f7bfc9f -- tools/mado-verify.sh` →
  empty (round 10 opened no gate edit).
- **Battery** (frozen copy; logs in scratch). `bash gate-f7bfc9f.sh
  --selftest` → 268/268 rc 0; `--no-live` → CLEAN (29 pass, 4 notes) rc 0;
  `gate-f7bfc9f.sh` (live) → DIVERGED (3 fail, 49 pass) rc 1; `cd repo &&
  bash tools/mado-verify.sh --regression` → PASS rc 0, `REGRESSION_DATE
  2026-10-14T21:35:31Z`, `REGRESSION_SWEEP … killed=10 survived=0
  inconclusive=0 kill-rate=100%`.
- **Ladder.** `git show <c>:tools/mado-verify.sh | sha256sum` + `wc -lc` per
  commit (five rows above); each blob's own `--selftest` re-run from the
  frozen copies (28/53/89/217/268); `f7bfc9f` row = `93e43f8f…` unchanged.
- **r5 rung.** Spec: heredoc body between the `MADO_R7_SPEC_EOF` markers,
  trailing newline stripped as `mado_r7_spec_write` does → `c7ee75b9…1dd8`,
  2,141 B, 10 defects. `bash <tameshi>/tools/mutate-and-run.sh --target
  hist-eead56b.sh --defects spec.txt --suite 'bash "$MUTANT" --selftest'
  --label mado-verify-r5-audit-m11 --timeout 30` → killed=4 survived=6
  inconclusive=0 kill-rate=40 %; CONTROL GREEN; `MUTATE_RESTORE: OK`. The
  round's §2 carries the r5 rung as [OBS-record: AUD-M10]; it now has a
  second independent re-derivation, this one.
- **Snapshot pair (scratch only).** `--snapshot` ×2 → WRITTEN (rows=60,
  rc 1 — a DIVERGED run still writes); `--snapshot-diff snapA snapB` →
  `MADO_DIFF: SAME` rc 0. The round's own worked example (file-plane 41 →
  live 60, rc 1) is in the note §8; read, not re-run by me.
- **Pins.** Gate sha identical before/after every run of mine
  (`gate.sha.before.txt` / `gate.sha.after.txt`); the worktree was only ever
  ` M SKILL.md` + the wave's untracked artifacts at my status reads.
- **Closeout note reads.** Three pins recorded mid-flight: `85f6f817…`
  (234 L) → `979fcade…` (234 L, 1-byte drift) → `670b5a39…` (294 L, with the
  M11-3 §8 append; stable from 21:40:35Z to my close). Content consumed in
  full at each read.

## 3. Spot-checks (three, all re-run 2026-10-14)

1. **The battery + pins.** 268/268; CLEAN 29/4 with boundary
   `bb2639d9a980…`; DIVERGED 3/49 with the same boundary row green;
   regression PASS with target `dc7c4141…f8fd` and spec `c7ee75b9…1dd8`
   matching the recorded pins; gate sha `93e43f8f…` identical before and
   after the whole battery; M11-1's three live runs byte-identical (md5
   `cd658a90…` — "diverged identically" verified, not recited).
2. **The closeout's own findings, reproduced.** **F1** `…a5171`:
   `grep -rn a5171 --include='*.md'` (excluding the note itself) →
   **34 occurrences / 13 files** — the note's count exact (37/14 including
   the note). **F2** `snapshot-diff-receipt-r9.md:33` reads `dc7c4141…db62`
   (the *previous* pin's tail) vs the re-cut `…c0514cb6f8fd`. **F3**
   `walker-deep-r9.md:296` "round 8 ended at 2,837 L" vs the measured r8
   gate 2,887 L / 131,612 B. **F4** note `:13` path
   `corpus/knowledge/ten-round-synthesis.md` (never landed; landed path
   `arc-synthesis.md`). **F5** `SKILL.md:1313-1314` cites AUD-M9 as
   `7ad8eccdd8d213a5…`; the landed blob reads `866272eeda09bc08…` (166 L /
   15,580 B, `git show HEAD:` + `sha256sum`). All five reproduce [O].
3. **The handoff bytes.** Synthesis §1.1 sampled: `config-health-report-r3.md`
   `acf59f9b…`/1005, `walker-deep-r9.md` `a5acfe01…`/398,
   `snapshot-diff-receipt-r9.md` `73b1466b…`/196 — byte-exact to the table;
   README 8 rows vs 21 notes; drafts 13/19/19/22; the M11-4 SKILL append
   (worktree `b9134091c0…` / 1,545 L) carries the F5 correction append-only
   with both values.

## 4. Findings (named, not smoothed)

- **F1 — the closeout note's landed name vs its referenced name.** The note
  landed as `corpus/knowledge/closeout-r11.md` (untracked at my read). The
  round-11 plan §(c), the M11-4 SKILL append (`:1458`, `:1473`, `:1529`,
  `:1544`), VER-M11's poll and SCR-M11's poll all cite
  `corpus/knowledge/arc-closeout.md`; the note itself states no path. Naming
  class — the arc-synthesis precedent (`ten-round-synthesis.md` →
  `arc-synthesis.md`) shows a landed-name supersession is legitimate but
  must be recorded; at my close it is not. Both values carried here.
- **F2 — one numeric cell off by one.** Closeout §4: "SKILL round-10 append
  (+90/−1 at commit)". Measured: `git show f7bfc9f --numstat` → `89 1
  SKILL.md` (the diffstat's "90" is total churn; total commit churn
  +2,312/−1 checks out). The round-10 lesson (M11-2) states it as +89/−1;
  the closeout note's cell should match. Both values carried.
- **F3 — the live move (waybar), named.** Five independent runs across the
  wave's lanes (M11-1 ×3, M11-3, M11-4, mine) read the same three FAILs;
  `pgrep -fl waybar` → none; the absence was already in AUD-M10's window
  (F2, 20:59Z) — it is not this round's first, and it is not smoothed here.
  Class: session state, not a gate defect and not a config drift (boundary
  row green in every run; `bb2639d9a980…` is the invariant).
- **F4 — harness provenance.** `mutate-and-run.sh` moved since the
  recording: live `75ed934d…` vs recorded `b56c6e57…`; the gate prints it
  as provenance, not gated — and both my replays (regression PASS; r5 4/10,
  control GREEN) reproduce under the moved bytes.
- (My own scratch-glide slip is named in the preamble, not hidden.)

## 5. Unknowns

- **U1 — the settlement and the arc-end commit.** At my close the settlement
  is in flight: `corpus/lessons/round-10.md` landed (`d7b4708e…`),
  `plans/completion-evidence.md` (`e63272c4…`) and the note are untracked;
  README / SCORECARD / LOG / the round-11 lesson / the draft closure blocks
  / walker-deep errata are not yet on disk; HEAD is `f7bfc9f`, no round-11
  commit. Every state above binds to `f7bfc9f` and my read times; re-derive
  from the commit.
- **U2 — the closeout note moved during my window** (`85f6f817…` →
  `979fcade…` → `670b5a39…`, incl. the §8 append); my content audit binds to
  the reads; a later edit re-opens it.
- **U3 — live point samples.** One session; waybar's absence spans at least
  20:59Z → 21:36Z across two rounds' windows; whether it returns before the
  close is outside my window; PIDs move on restart.
- **U4 — single host / toolchain / window** (bash 5.3.15; window
  21:30–21:49Z). The historical suites were re-run by me at today's
  toolchain only.
- **U5 — coverage.** I re-derived C1/C2 whole, the receipt battery, the
  ladder (hash + each selftest) and the r5 rung; I sampled the synthesis's
  §1.1 ledger (3 notes) and the note's F1–F5, and did not re-measure the
  synthesis §3/§5/§6 member sets or the VER-M11 ladder report cell-by-cell
  (peer lane, in flight).