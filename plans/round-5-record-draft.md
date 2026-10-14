# mado round-5 record — scribe prep DRAFT (SCR-M5)

Draft v1 window: 2026-10-14 17:01–17:1xZ (local 14:01–14:1x −03:00). Lane SCR-M5.
**v2/v3 revisions through 17:16Z: read §10 first — it supersedes the ⟨PENDING⟩
slots in §1 and corrects the §0 lane map; the v1 text is kept for provenance.**
State at v3 cut (17:16:49Z, measured): HEAD `3d9ba45`; tree = ` M
corpus/knowledge/province-accuracy-selfaudit.md`, ` M plans/round-5.plan.md`,
`?? corpus/knowledge/walker-deep.md`, `?? plans/round-5-record-draft.md`,
`?? plans/round-6.plan.md`, `?? tools/`; `tools/mado-verify.sh` 1,098 L sha
`d7edaab4bf108625…`; self-audit 345 L `7c0a58208dea60e8…`; `walker-deep.md`
617 L `0982ba066c72575a…`; SKILL.md still 448 L `92462fa7d71b3fed…`;
SHONEN.md still 12 L `f6495fe68f4265e3…` (2×`[x]` / 2×`[~]`); this draft's own
L/sha re-measure at read time — it is edited across the scribe window (last
self-measure 17:21:49Z: 510 L, sha `1ac0fc2533d644db…`).
This file is scribe scratch product for the round-5 finalizer — **not the
record**. Nothing outside this file was written by this lane in the repo;
scratch `/tmp/w5-scr-m5/` (`poll.log`, `anchors.txt`). All probes read-only
(file reads, `sha256sum`/`wc`/`stat`/`git` read verbs, `hyprctl` read verbs,
`pgrep`); no substrate file under `~/.config`/`~/.local` written.
Working tree at v1 (measured 17:03Z): ` M plans/round-5.plan.md` only; HEAD
`3d9ba4559438b4c07d0c56328e1c4b7b5c4d7e1e` (round-4 commit, 2026-10-14
13:57:18 −0300). Round-5 work is uncommitted — landed-means-committed is the
round commit's job.

Reading key: **⟨PENDING⟩** = must be resolved at finalization; every other
number names the command that produced it at v1 time. Counts on `.md` notes
use `wc -l` (those notes end without a trailing newline; editor view = +1);
this draft ends with a newline, so `wc -l` equals its line count.

## 0. Round-5 frame

- Plan (worktree): `plans/round-5.plan.md` — 9 L, 628 B, sha
  `1061fe40b7c2da4e…`, mtime 2026-10-14 13:59:15 −0300, **untracked-modified**
  (the committed 68-L `b588e3ec…` plan from the round-4 commit is superseded
  by it). Axis move: **calibration (close box 4) + operability (first gate)**.
  Claim (a): the box-4 §8 re-run lands with named-verifier closure; claim
  (b): `tools/mado-verify.sh` ships — declared planes vs live bytes + hyprctl
  where available, hermetic selftest on a fixture tree, emits
  `MADO_VERIFY: CLEAN|DIVERGED` + exit map. Anti-claim: any unverifiable
  plane reads UNKNOWN, never a fake CLEAN. Measure: box-4 `[x]` with verifier
  name; gate selftest count + live verdict.
- Box-4 closure contract (as written, not as inferred): the self-audit note
  `corpus/knowledge/province-accuracy-selfaudit.md` §7 (line 187) hands the
  close to "the named non-author verifier": re-run §8's counts read-only,
  spot-check ≥3 claims across evidence classes, and on all-reproduce write
  `[x] <verifier-id>` + pointer **in `SHONEN.md`** — "the only file change
  needed" (§7:201-203). `PROTOCOL.md:63-68` bars self-close; `:419-431`
  fixes the SHONEN seed and the mark rules (one indented evidence line per
  box).
- Round-5 lane map (**v2 — corrected by the artifacts' own self-labels**):
  **M5-1** → the box-4 §8 re-run receipt, appended to
  `province-accuracy-selfaudit.md` ("Round-5 addendum … (M5-1, box-4 close
  evidence)"; scratch `/tmp/w5-mado-m5-1/`); **M5-2** → the gate
  `tools/mado-verify.sh` (its herder self-labels "round 5 / M5-2"); **M5-3** →
  `corpus/knowledge/walker-deep.md` (self-label "Walker deep-note … (M5-3)";
  probe scratch `/tmp/w5-m5-3-probe/`); **M5-4** → SKILL.md round-5 append,
  draft at `/tmp/w5-mado-m5-4/draft-append.md` (2,240 B, 14:02 local);
  **VER-M4B** → the named verifier seat (scratch `/tmp/w5-ver-m4b-work/`,
  `/tmp/w5-ver-m4b-poll/`; its poller cap runs 17:03Z → ~17:28Z);
  **SCR-M5** → this file. The pollers had M5-1/M5-2 swapped (M5-4's poller
  watched "M5-1 (tools/mado-verify.sh) and M5-2 (box-4 note)"; the artifacts
  say the reverse) — a lane-attribution ambiguity to state in the record, not
  a defect of either product.
- Also newly present in the worktree at 17:04Z: `?? plans/round-6.plan.md`
  (another lane's prep; not round-5 content — do not fold in).

## 1. Deliverables measured at v1 time

D1 — M5-2 gate `tools/mado-verify.sh`: **landed 17:06Z, iterated live, and
green on both halves at 17:14Z.** Revisions observed (all runs read-only,
mine): `3b592b374cf25500…` 1,095 L @17:06:25Z → `7f019a302f90ae9c…` 1,097 L →
`5811b5f6050e6d43…` 1,096 L → `33e805720cf4c1e3…` 1,095 L @17:07:45Z →
`d711528e795d21dd…` 1,098 L @17:08:48Z → `d7edaab4bf108625…` **1,098 L**
@17:14Z. Header declares the exit map (0 CLEAN / 1 DIVERGED / 2 tool-error),
modes `--selftest` (hermetic fixtures under `/tmp/w5-mado-*`), `--no-live`,
`--root DIR`, and the read-only discipline.
**Mid-round state (must be stated, not hidden): at `5811b5f6…`/`7f019a30…`
the selftest was RED — `MADO_SELFTEST: FAILED — 19 passed, 9 failed`, rc=2,
tampered fixture → fake `CLEAN`** (the plan's anti-claim), with the failing
block printing fixture root `…/clean` where `…/broken` is expected
(transcripts `gate-selftest.log`, `gate-selftest2.log`).
**Final observed state (v2):** at `d7edaab4bf108625…` (1,098 L) —
`MADO_SELFTEST: 28/28 assertions passed`, rc=0 (`gate-selftest3.log`) and the
live run → `MADO_VERIFY: CLEAN (35 pass, 4 notes; file + live planes verified
read-only)`, rc=0 (`gate-live2.log`), `gate boundary.readonly PASS — config
plane byte-identical before/after (combined sha bb2639d9a980…)`; the earlier
live run at `5811b5f6…` was also CLEAN (35/0/0/0 + 4 notes,
`gate-live.log`). The red→green transition happened inside the round and is
recorded as history: the round-1 operability ceiling is retired **only** if
the file's final revision at commit still passes both runs — re-measure then.

D2 — M5-1 box-4 §8 re-run receipt: **landed ~17:07Z as an append** —
`corpus/knowledge/province-accuracy-selfaudit.md` gains "Round-5 addendum —
§8 re-run receipt (M5-1, box-4 close evidence) [OBS] `[~]`": all 25 §8 rows
re-executed, every durable row byte-equal, three era-caused moves named
(commit count 4→5 = the round-4 commit `3d9ba45` itself; secret-scan hits
14→33 = repo growth, matching VER-M4's 33; omarchy `.git`-dir metadata move),
4 cross-class spot-checks, U6–U8 added, base revision verified pre-append.
File measured post-append: **345 L, sha `7c0a58208dea60e8…`** (was 264 L /
`3014a84060c95710…`; diff +82/−1, `git diff --stat`). The append itself notes
§7 step 2 (the `[x] <verifier-id>` write in SHONEN.md) stays
verifier-scoped — matching §3's branch below.

D3 — M5-4 SKILL.md round-5 append: **draft exists, not landed**. SKILL.md
re-measured 17:08Z: 448 L, sha `92462fa7d71b3fed…` — still identical to the
round-4 commit's frozen value, so the append has not been applied. Draft file
`/tmp/w5-mado-m5-4/draft-append.md` (2,240 B) is variant B ("pointer-based",
by its own header) and still carries `<TIME>` placeholders — the finalizer
must re-measure whatever SKILL text actually lands, not the draft. Its gate
pointer text ('the placeholder path `:426` (`corpus/scripts/`) is superseded
by `tools/mado-verify.sh`') matches the current state: `corpus/scripts/`
still absent, `tools/mado-verify.sh` present.

D4 — VER-M4B verdict (box 4): **FILED 17:09Z — the box CLOSES.** Verdict file
`/tmp/w5-ver-m4b-work/VERDICT.md`, 8,625 B, sha256
`f70fc3c70a11e91e2a2af421ae1b14fac6508bfff2fb518b7587e6159f013cf7…`
(scratch; hashed 17:14Z). Verdict: "`[x] VER-M4B` — box 4 CLOSES"; all 25 §8
rows re-derived with its own harness (`rerun8.log` [A]–[I]); its own boundary
before/after pins equal; 4 cross-class spot-checks; moved values all cause-named
(commits 4→5 = `3d9ba45`; omarchy `.git` metadata-only move; secret-hit count
growth 14→33/34→40 era-stamped, 0 key-shaped; `ai-usage/selected` 5→6 B
timer-written; hypridle era; timer LAST). It verified the v4 addendum as a
**byte-prefix append** (`head -c 17856` = `3014a840…`), so no province claim
text changed; PROVINCE.md unchanged since mint. It also flags the seat-label
swap (its U4) — §0/§10 of this draft already record it. Closure write in
SHONEN.md is the lane/finalizer edit (§3 line below).

D5 — M5-3 `corpus/knowledge/walker-deep.md`: **landed 17:07Z**. 617 L by
`wc -l`, 38,403 B, sha `0982ba066c72575a…`, self-labeled "Walker deep-note —
config semantics end-to-end (M5-3)"; 14 `##` sections + append-only errata
section (empty); probe window 17:00–17:25Z UTC, substrates read-only with
before/after re-hash §13, sockets stat'd-not-connected, one probe outlier
(a bare `elephant` start/exit) recorded. Treat as a depth-note deliverable for
the round record (SCORECARD depth row + README coverage row) if the finalizer
counts it in-scope — `plans/round-5.plan.md`'s two claims do not name it, so
it rides as an extra deliverable (same pattern as round-4's M5-3-style
extras).

## 2. Carried debt from round 4 (the round-4 record draft was not applied)

The round-4 commit landed the work products and a terse LOG/SCORECARD line,
but **none of the round-4 draft's record blocks** (§4a full LOG entry, §4b
README rows, §4c SCORECARD rows, §4d SHONEN regeneration). The round-4 draft
itself is committed (`plans/round-4-record-draft.md`, 474 L by `wc -l`, sha
`c690a931c396266b…`) and is the durable source for the missing text. Round 5
must resolve, not re-discover:

1. **SHONEN.md is stale.** Measured 17:03Z: 12 L, sha `f6495fe68f4265e3…`,
   mtime 2026-10-14 12:51:00 −0300 — unchanged since before the round-4
   commit. Marks: box 1 `[x]` MADO-R3-4, box 2 `[~]`, box 3 `[x]`
   MADO-R3-4, box 4 `[~]`. The round-4 LOG entry (LOG.md:294) says "box-3
   CLOSED (VER-M3: config-health report reproduces)" — under the round-4
   plan's numbering (3 = e2e task = SHONEN item 2) that mark never reached
   the file. VER-M3's verdict file is still alive in scratch
   (`/tmp/w4-ver-m3/VERDICT.md`, 19,930 B, sha `69ca88ce4d1ac66b…`,
   re-measured 17:04Z).
2. **`corpus/README.md` has 8 coverage rows** (19 L total, sha
   `2dd274f5e270e65b…`) — missing rows for `idle-lock-plane.md` (MADO-R4-2)
   and `province-accuracy-selfaudit.md` (M4-3 product). The ready-to-apply
   row text is `plans/round-4-record-draft.md` §4b (committed, lines
   300–309).
3. **`SCORECARD.md:16` is a stub row** (`| 4 | depth + calibration | round-3
   state | idle/lock plane (355 L) | wave-4 32-lane; VER-M3 |`) — the
   round-4 draft §4c (committed, lines 311–319) holds three measured rows
   that replace/extend it.
4. **`plans/round-5.plan.md` supersession**: the committed blob at
   `3d9ba45` is the 68-L operability plan (sha `e1496b75a2ecc04b…`); the
   worktree file is the 9-L two-move plan (sha `1061fe40b7c2da4e…`). The
   round-5 commit lands the 9-L file and should say the 68-L text was
   superseded (its gate name `corpus/scripts/verify-plane.sh` is dead; the
   round-5 gate path is `tools/mado-verify.sh`).
5. Owed lane errata still unapplied after round 4 (VER-M3's filed items,
   round-4 draft §4e): `keybind-rule-semantics.md` §2.3 dispatcher-tail
   prose (five ×4 incl. `swapwindow`, five ×2 — `swapwindow` still present
   at line 151); corrected runner V2/V3 (binds summary `n= 1`; 16-char pin
   vs 64-char comparator — the corrected copy is still scratch-only:
   `/tmp/w4-m4-1-repro/repro-r3.sh`, sha `389a1bb79f7661f9…`, re-measured);
   K2's "29/29" scope wording.

## 3. SHONEN box attributions expected this round

Mark rules (`PROTOCOL.md:419-431`): marks confined to the box character plus
ONE indented evidence line per box; `[x]` only with a named non-author
verifier. Mechanical check at finalization: extract the seed from
`PROTOCOL.md:419-431`, substitute `mado-shokunin`, diff — only changed box
chars and the indented evidence lines may differ.

Box 2 (e2e task) — earned in round 4, not yet written:

```
- [x] At least one end-to-end domain task executed and logged in LOG.md
  VER-M3 (non-author reviewer seat) — REPRODUCES: P1 29/29 pins clean + stock-6 sha match; P2 57/57 getoption rows 0 mismatch, binds 192 with the full flag/modmask census, animations/sources/rules/bind-source counts equal; P3 F1–F10 all reproduced (F1 via the documented state move); the kit's late addendum executed, every expectation holds — evidence `/tmp/w4-ver-m3/VERDICT.md` (19,930 B, sha `69ca88ce4d1ac66b…`; ephemeral), cited at the round-4 LOG entry
```

Box 4 (PROVINCE accuracy) — **CLOSED this round: `[x] VER-M4B` (verdict filed
17:09Z; evidence half = the §8 re-run append, verdict half = D4).** The line
to write:

```
- [x] No cross-domain bleed (PROVINCE.md still accurate)
  VER-M4B (non-author verifier seat, round 5) — §8 re-run reproduces: all 25 §8 rows re-derived · durable pins byte-equal (13/13 hypr, 4/4 terminals, waybar ×2, walker, mako, PROVINCE.md `7aad7b863dc3c10b…`) · 4 cross-class spot-checks (file bytes / live reads / repo+boundary scan / process timeline) · moved values all cause-named (commits 4→5 = the round-4 commit `3d9ba45`; omarchy `.git` metadata-only move; secret-hit count era-stamped growth with 0 key-shaped) · v4 addendum proven a byte-prefix append over v3 (`head -c 17856` = `3014a84060c95710…`) so no province claim text changed — evidence `/tmp/w5-ver-m4b-work/VERDICT.md` (8,625 B, sha256 `f70fc3c70a11e91e…`; ephemeral) + durable §8 receipt `corpus/knowledge/province-accuracy-selfaudit.md` round-5 addendum (345 L, sha `7c0a58208dea60e8…`) — closure per that file's §7
```

Re-check at finalization: re-hash the verdict and the self-audit; if either
moved, re-verify the cited text still matches (VER-M4B's own U3 rule: a later
self-audit revision re-opens only the appended delta).

- Hold-open fallback, only if VER-M4B's verdict is withdrawn or a
  non-reproduction is filed before commit: keep `[~]` and update the evidence
  line to name the failing claim, command, and observed value per §7:204-205;
  do **not** mark `[x]`. The landed §8 receipt alone cannot close the box — a
  self-run receipt is not a named non-author verdict (`PROTOCOL.md:63-68`),
  and its own text says so.

Do not cite the round-4 VER-M4 verdict as a second closure attempt: the
round-4 LOG entry recorded the box as left open ("§8 re-run needed per the
named verifier"), and whichever reading of VER-M4's own file is taken, round
5's closure rests on VER-M4B.

## 4. Record text to apply

### 4a. LOG.md round-5 entry (append after the round-4 entry, LOG.md:294)

```
- 2026-10-14 — round 5: calibration + operability — box-4 close attempt via
  the §8 re-run with a named non-author verifier (VER-M4B), and the lane's
  first executable gate `tools/mado-verify.sh` (dispatch per
  `plans/round-5.plan.md`, 9 L, sha `1061fe40b7c2da4e…`; the 68-L round-5
  plan committed at 3d9ba45 is superseded). Anti-claim: any unverifiable
  plane reads UNKNOWN, never a fake CLEAN; a gate that does not land green on
  this host leaves the move unproved. Deliverables:
  M5-2 gate → `tools/mado-verify.sh` (1,098 L, sha `d7edaab4bf108625…` at
  17:14Z; exit map 0 CLEAN / 1 DIVERGED / 2 tool-error; read-only; hermetic
  `--selftest`). Round history, in order: mid-round revisions were
  **selftest-RED** (`MADO_SELFTEST: FAILED — 19 passed, 9 failed` — tampered
  fixture → fake CLEAN at 1,096-L `5811b5f6…`); the final observed revision
  is green on both halves — `MADO_SELFTEST: 28/28 assertions passed` rc=0 and
  `MADO_VERIFY: CLEAN (35 pass, 4 notes; file + live planes verified
  read-only)` rc=0, config plane byte-identical before/after; transcripts
  `/tmp/w5-scr-m5/gate-selftest*.log`, `gate-live*.log` ⟨fill: re-run at the
  file's commit revision; if red there, this row reads `unproved`⟩.
  M5-1 §8 re-run receipt → `corpus/knowledge/province-accuracy-selfaudit.md`
  round-5 addendum (all 25 §8 rows re-derive; durable rows byte-equal; 3
  era-caused moves named — commits 4→5, secret-hit growth (14→33/34/40,
  era-stamped), omarchy `.git` metadata; 4 cross-class spot-checks; U6–U8
  added): 264→**345 L**, sha `7c0a58208dea60e8…`; diff +82/−1; scratch
  `/tmp/w5-mado-m5-1/`.
  M5-3 → `corpus/knowledge/walker-deep.md` (617 L, sha `0982ba066c72575a…`;
  walker/elephant config semantics end-to-end, 14 sections; before/after
  substrate re-hash §13; sockets stat'd-not-connected; one probe outlier
  recorded).
  ⟨fill: M5-4 SKILL.md append — before→after `wc -l` + sha, section name⟩
  Verifier attribution (SHONEN box 4): **VER-M4B CLOSES** — all 25 §8 rows
  re-derived independently; pins byte-equal; 4 cross-class spot-checks; moved
  values cause-named; the v4 addendum proven a byte-prefix append (`head -c
  17856` = `3014a840…`); verdict `/tmp/w5-ver-m4b-work/VERDICT.md` sha256
  `f70fc3c70a11e91e…` (ephemeral) + durable receipt in the addendum.
  Carried record debt fixed in this commit: SHONEN.md regenerated (box 2 `[x]`
  VER-M3 per the round-4 LOG entry; box 4 `[x]` VER-M4B); corpus/README.md +2
  round-4 rows (idle-lock-plane, province-accuracy-selfaudit) +1 row per
  round-5 note; SCORECARD.md round-4 stub row replaced from the round-4 draft
  §4c + round-5 rows.
  Scribe verification (this entry; commands re-run at finalization, raw log
  `/tmp/w5-scr-m5/`): ⟨fill: final re-run values⟩ — at v2: PROVINCE.md 18 L /
  `7aad7b863dc3c10b…`; 13/13 hypr confs; `hyprland.conf`
  `4f52854a3c143dcf…`; waybar `8316c08ceaa7e3f0…`/`07f7d663106b72e4…`;
  walker `fecf71fa4253803e…`; mako `95bf0c86c955cc81…`; terminals 4/4 pins;
  `grep -c '^source'` 17; omarchy skill 392 L; declared-tree `find -newermt`
  0 hits; Hyprland 0.56.2 `efb50993…`; binds 192; `hypridle` absent rc=1;
  gate selftest 28/28 + live CLEAN at `d7edaab4…`; VER-M4B verdict sha
  `f70fc3c70a11e91e…`; self-audit 345 L `7c0a58208dea60e8…`.
  Observations: ⟨fill from §6⟩. Unknowns: ⟨fill from §7⟩. Falsifiable
  next-iterations: ⟨fill from §8⟩.
```

### 4b. corpus/README.md — coverage map rows

Apply **verbatim** the two round-4 rows from `plans/round-4-record-draft.md`
§4b (committed, lines 305–306): `knowledge/idle-lock-plane.md` (MADO-R4-2)
and `knowledge/province-accuracy-selfaudit.md` (M4-3 product / box-4
evidence). Then append one row per round-5 note as it lands (composition
follows round-4 draft §4b's shape: note → holds → sources with probe window;
the finalizer writes the round-5 rows from the measured artifacts, not from
this draft). Round-5 note rows must name the gate artifact too if
`tools/mado-verify.sh` is referenced from SKILL.md.

### 4c. SCORECARD.md — move-log rows

Replace the round-4 stub (`SCORECARD.md:16`) and append round-5 rows. Ready
text for round 4 is `plans/round-4-record-draft.md` §4c (committed, lines
311–317 — three rows: calibration, depth, freshness). Round-5 rows
(move-log columns: Round | Axis | Before | After | Evidence):

```
| 5 | calibration | box 4 `[~]` since round 3; round-4 LOG left it open ("§8 re-run needed per the named verifier"); self-audit §7 names the closure procedure (`[x] <verifier-id>` in SHONEN.md) | box 4 `[x]` VER-M4B: all 25 §8 rows re-derived, durable pins byte-equal, 4 cross-class spot-checks, moved values cause-named, v4 addendum a byte-prefix append (no claim text changed) | verdict `/tmp/w5-ver-m4b-work/VERDICT.md` sha256 `f70fc3c70a11e91e…` (ephemeral); durable receipt `corpus/knowledge/province-accuracy-selfaudit.md` round-5 addendum 345 L sha `7c0a58208dea60e8…`; `head -c 17856` = `3014a84060c95710…`; spot-checks: `hyprland.conf` 1,273 B/29 L/`4f52854a3c143dcf`, `hyprctl version` 0.56.2 `efb5099…`, `binds` 192, declared-tree `find` 0 |
| 5 | operability | round-1 ceiling still standing after 4 rounds: `find corpus -name '*.sh'` → 0, no `corpus/scripts/`, no committed verdict gate | round-1 ceiling retired: `tools/mado-verify.sh` ships — declared planes vs live bytes + hyprctl read verbs, exit map 0/1/2, hermetic `--selftest`, read-only boundary check; green on this host: selftest 28/28 assertions + `MADO_VERIFY: CLEAN (35 pass, 4 notes)` | `wc -l tools/mado-verify.sh` → 1,098; sha `d7edaab4bf108625…`; selftest transcript `/tmp/w5-scr-m5/gate-selftest3.log`; live transcript `gate-live2.log`; mid-round red history: `MADO_SELFTEST: FAILED — 19 passed, 9 failed` at `5811b5f6…` (recorded, not smoothed) |
```

⟨The operability row is written only for the gate's **final** revision at
commit — re-run both halves then; if red, the row reads "unproved" with the
failing command (the plan's anti-claim), and the mid-round red history above
stays in the entry.⟩

### 4d. SHONEN.md regeneration

Regenerate per `PROTOCOL.md:419-431` (seed + one indented evidence line per
box): box 1 and box 3 byte-identical to the current file; box 2 →
`[x] VER-M3` (§3 template); box 4 → `[x] VER-M4B` with the §3 line. Result:
**4/4 `[x]`** — the first full SHONEN in the lane's history; the report is
then the operator/integrator's promotion decision (`PROTOCOL` Promotion
gates), not this round's claim. Keep the header
`# mado-shokunin — Promotion checklist` and the seed's middle line. After
writing: `sha256sum SHONEN.md`, then the mechanical seed diff (§3 preamble) —
only box chars + evidence lines may differ from the seed shape.

### 4e. Errata status

- **Owed (round 5)**: the §2.5 items — `keybind-rule-semantics.md` §2.3
  dispatcher-tail prose; runner V2/V3 receipts; K2 "29/29" scope wording.
  Owner: the lanes that authored them if present; otherwise an errata sweep
  lane this round or next (append-only blocks; nothing applied at v1 time).
- **Applied in round 4 by ERR-M** (do not restate): the five errata blocks
  (`config-health-report-r3.md` E2/E3, `hyprctl-verification-layer.md` E2,
  `waybar-walker-plane.md` R4-E1–E8, `waybar-walker-semantics.md` E1,
  `idle-lock-plane.md` E2) — `grep -n 'Errata (round 4)' corpus/knowledge/*.md`
  → headers at config-health 553, hyprctl-verification 283, idle-lock 358,
  waybar-plane 412, waybar-semantics 460 (line numbers at v1 time).
- **Candidates not yet applied**: self-audit `Errata (append-only)`
  E-candidates 1–2 (`province-accuracy-selfaudit.md:260-265`) — wrong-file
  candidates by scope (they name `config-health-report-r3.md` and
  `waybar-walker-semantics.md`), so an errata lane must append there, not
  here; leave the self-audit's own section as-is unless VER-M4B files an
  erratum.

## 5. Scribe measurements and spot-checks (v1, executed)

1. **Repo/pins** (17:03Z): `wc -l`/`sha256sum` — LOG.md 294 L
   `7bd1ae21a936d8c7`; SCORECARD.md 16 L `f38487e6e0339828`; SHONEN.md 12 L
   `f6495fe68f4265e3`; SKILL.md 448 L `92462fa7d71b3fed`; corpus/README.md
   19 L `2dd274f5e270e65b`; PROVINCE.md 18 L `7aad7b863dc3c10b`; plans/
   round-5.plan.md 9 L `1061fe40b7c2da4e`.
2. **Self-audit §8 re-run spot set** (read-only; the verifier's job is the
   full table — this is a scribe cross-check): `git log --format='%h %ci' --
   PROVINCE.md` → `74d3b7b 2026-10-14 09:50:45 -0300` (1 commit); 13/13 hypr
   `.conf` (+bak) hashes; `hyprland.conf` `4f52854a3c143dcf`; waybar
   `style.css` `8316c08ceaa7e3f0` / `config.jsonc` `07f7d663106b72e4`;
   walker `fecf71fa4253803e`; mako `95bf0c86c955cc81`; terminals alacritty
   `695301c86577c808` / foot `3e88354476f2682e` / kitty `f875291ecfe64ebc` /
   ghostty `cb828c044b07d4fd`; `grep -c '^source'` → 17; omarchy skill 392 L;
   declared-tree `find ~/.config/{hypr,waybar,walker,alacritty,foot,kitty,
   ghostty,mako,omarchy} ~/.local/state/omarchy ~/.agents/skills/omarchy
   -newermt "2026-10-14 09:40"` → 0 hits (the 320 raw `~/.config` hits are
   all non-surface app caches: chromium 113, obsidian 94, Grok Bot 42,
   1Password 24, devin 10, BraveSoftware 8, …).
3. **Live read verbs** (17:03–17:06Z): `hyprctl version` → 0.56.2
   `efb50993780079460b0cbed1363e2166a2de1d9f`; `instances` → one, pid
   1203316, `wl_socket "wayland-1"`; `layers` namespaces `wallpaper`,
   `waybar`; `binds` → 192; `getoption general:gaps_out` →
   `{"custom":"0 0 0 0","set":true}`; `clients` → 2, both tags
   `['default-opacity*','terminal*']` (F2 reproduces on the new session);
   `pgrep -x hypridle` → rc=1 (absent; `systemctl --user is-active` →
   `inactive`, rc=3 — only the `pgrep` half discriminates); `pidof hyprlock`
   → rc=1.
4. **Gate runs (v2, executed; the artifact is the moving target named in D1):**
   at sha `7f019a302f90ae9c…` (17:07:01Z) and again at `5811b5f6050e6d43…`
   (17:07:26Z) — `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST:
   FAILED — 19 passed, 9 failed`, rc=2, fixtures kept (`…/clean` 32 files,
   `…/broken` 31 files), failing block prints root `…/clean` for the broken
   scenario and reports `MADO_VERIFY: CLEAN` (fake clean — the plan's
   anti-claim); at the same revision `bash tools/mado-verify.sh` (live) →
   `MADO_VERIFY: CLEAN (35 pass, 4 notes; file + live planes verified
   read-only)`, rc=0, `gate boundary.readonly PASS — config plane
   byte-identical before/after (combined sha bb2639d9a980…)`. Transcripts
   `gate-selftest.log`, `gate-selftest2.log`, `gate-live.log`. My runs'
   fixture dirs are under `/tmp/w5-mado-selftest.*` (ephemeral).
5. **Boundary**: read-only throughout; no mutating `hyprctl` verb, no
   consumer started/stopped, no network command; substrate hashes equal
   before/after (spot set re-run at the end of v1 window; see `anchors.txt`).

## 6. Observations (v1)

(a) The round-4 record draft's blocks were not applied — the round-4 commit
    kept a terse LOG line and a SCORECARD stub, and left SHONEN.md untouched.
    Round 5 inherits three record debts (README rows, SCORECARD row, SHONEN
    regeneration) that are cheap to fix from the committed draft.
(b) Box 4's closure is written down unambiguously in the artifact itself
    (`province-accuracy-selfaudit.md` §7) — this round's job is to execute
    that procedure, not to invent one. The round-4 draft's "E1 branch" is
    moot; VER-M4's own verdict says no erratum append is required.
(c) Lane attribution improved then muddled: three round-5 artifacts carry
    self-labels (addendum "M5-1", gate header "round 5 / M5-2", `walker-deep.md`
    "(M5-3)"), but the round's own pollers assumed the opposite M5-1/M5-2
    mapping, and VER-M4B's verdict names the same discrepancy. Net: the record
    should attribute by artifact + self-label, and note the swap once.
    M5-4's SKILL append still carries no lane label at v2 time.
    (Supersedes v1's "no lane self-labels yet".)
(c2) The gate's selftest went red→green inside the round (19/9 fake CLEAN at
    `5811b5f6…` → 28/28 at `d7edaab4…`). Worth one line in the record as the
    round's clearest "measure, don't trust" instance: the live run was green
    throughout, so only the self-test could have caught it.
(d) Two plan generations coexist for round 5 (committed 68-L operability plan
    vs worktree 9-L two-move plan). The 68-L text's gate path
    (`corpus/scripts/verify-plane.sh`) is dead; SKILL.md's :426 pointer to
    `corpus/scripts/` is the stale text M5-4's draft flags as superseded.
(e) `plans/round-6.plan.md` appeared (untracked) at ~17:04Z while round 5 was
    live — evidence the fleet is running ahead; the round-5 commit should not
    absorb it.
(f) Durability: the round-4 verdict files are still in `/tmp` at v1 time
    (VER-M3 sha `69ca88ce4d1ac66b…`, VER-M4 sha `1101c7bff5e6f6ee…`) — the
    hashes are already in LOG; the files themselves remain reap-able. VER-M4B's
    evidence will be scratch-only too unless the finalizer copies key text
    into the record.

## 7. Unknowns (v1 list, resolved status shown)

1. ~~Whether VER-M4B's verdict lands inside its cap~~ — **RESOLVED**: filed
   17:09Z, `[x] VER-M4B`; box 4 closes (§3, D4).
2. ~~Whether M5-1's gate lands, selftest/live state~~ — **RESOLVED at v3**:
   landed; final observed revision green on both halves; the release-candidate
   state must still be re-run at the commit revision (§9 step 3).
3. ~~Whether M5-2's §8 re-run is a note or an append~~ — **RESOLVED**: an
   append (v4); all 25 rows re-derive.
4. ~~M5-3's product and scope~~ — **RESOLVED as artifact**: `walker-deep.md`
   landed; **still open** whether the finalizer counts it as the round's depth
   deliverable (the plan does not name it).
5. Which lane authored M5-4's SKILL append (unlabeled) and the final SKILL sha
   (freeze at commit) — open.
6. Whether the operator/integrator wants the round-4 record debt (README
   rows, SCORECARD row, SHONEN box 2) folded into the round-5 commit — this
   draft assumes yes (cheapest correct state), flagged for the finalizer.
7. Residual seat-label ambiguity (M5-1/M5-2 swap): record by artifact
   self-label; whether the fleet's assignment map has the swap too — `[UNK]`
   from inside this lane.
8. Whether the gate author's remaining iterations change the exit map or the
   selftest count before commit — re-measure, don't carry these numbers.

## 8. Falsifiable next-iterations (carry + new)

- Box 4 closed by VER-M4B; SHONEN → 4/4 `[x]` once the regeneration lands —
  promotion itself stays the operator/gate decision per PROTOCOL.
- Land the gate + its SKILL wiring; then the round-1 operability ceiling is
  retired (or the row records why it stands again).
- Apply the owed round-4/5 errata (runner V2/V3, §2.3 dispatcher-tail text,
  K2 scope) as append-only blocks.
- `corpus/lessons/round-{1..5}.md` — the lessons ledger is empty a fifth
  round (`ls corpus/lessons` → 0 entries); the round-1 promise keeps failing.
- Durability convention for verifier evidence (fold verdict hashes + the
  load-bearing text into LOG/SHONEN; scratch files do not survive).
- Retire the stale `corpus/scripts/` pointer in SKILL.md once the gate lands
  (M5-4's draft already marks it superseded).

## 9. Finalization checklist (mechanical, ordered)

1. Re-measure the v1 anchors in §5.1 (all seven) and diff against the table;
   re-run §5.2 spot set; note any drift as a freshness observation.
2. Re-hash VER-M4B's verdict (`f70fc3c70a11e91e…`) and the §8 receipt
   (`7c0a58208dea60e8…`); if either moved, re-verify the §3 line's cited text
   (VER-M4B's U3 rule: a later revision re-opens only the appended delta) and
   confirm the box-4 closure still holds.
3. Read the gate's final revision: header exit map, `--selftest` transcript,
   live-run transcript; re-run both at the revision being committed; fill
   §4a/§4c placeholders from those runs; a red selftest at that revision
   writes the "unproved" row instead.
4. Apply 4a (LOG), 4b (README rows incl. the two round-4 rows), 4c
   (SCORECARD: replace the stub + append round-5 rows), 4d (SHONEN
   regeneration + seed diff + sha).
5. Land `plans/round-5.plan.md` (9 L) and this draft; note the 68-L
   supersession in the LOG entry; do not commit `plans/round-6.plan.md`.
6. Commit the round under the lane identity; freeze the SKILL sha after the
   final write; re-check every frozen sha appears in the entry.
7. If box 4 stays open at commit, keep this draft as the record's ancestry
   and state the open condition + what VER-M4B observed in the LOG entry's
   unknowns.

## 10. v2/v3 update (17:0x–17:2xZ) — what moved since v1, and what still must

Supersedes the ⟨PENDING⟩ slots and stale wording above; v1 text is kept for
provenance. Every number below names the command that produced it at v2/v3
time.

- **§0 lane map corrected (v2)**: M5-1 = §8 re-run receipt (self-labeled in the
  append); M5-2 = `tools/mado-verify.sh` (self-labeled in the script header;
  its scratch `/tmp/w5-mado-m52/` appeared at 17:08Z); M5-3 =
  `corpus/knowledge/walker-deep.md` (self-labeled). The pollers' assumed
  M5-1/M5-2 mapping was inverted. VER-M4B's verdict flags the same swap
  independently (its U4/U6) — record it once, as a lane-labeling observation,
  not a defect of any product.
- **§1 D1 (gate) — v3**: present, iterated live, and green on both halves at
  the last revision I ran: `d7edaab4bf108625…` 1,098 L →
  `MADO_SELFTEST: 28/28 assertions passed` rc=0 + `MADO_VERIFY: CLEAN
  (35 pass, 4 notes; file + live planes verified read-only)` rc=0. The
  mid-round RED selftest (19/9, fake CLEAN at `5811b5f6…`) stays in the
  history and in the LOG entry — it is evidence of a real defect being found
  and fixed inside the round, and of why the round's own selftest discipline
  matters. Re-run at the file's commit revision; an `unproved` row if red.
- **§1 D2 (receipt) — v2**: landed as an append; self-audit 264 → 345 L, sha
  `7c0a58208dea60e8…`; all 25 rows re-derive; no falsification.
- **§1 D4 (verdict) — v3**: VER-M4B filed 17:09Z, `[x] VER-M4B` — box 4
  CLOSES; sha256 `f70fc3c70a11e91e…`; §3 carries the line to write.
- **§1 D5 (new, v2)**: `walker-deep.md` landed (617 L, `0982ba066c72575a…`).
- **§5**: gate transcripts added (item 4 — including the red ones); all v1
  measurements stand unchanged (before/after pass in
  `/tmp/w5-scr-m5/anchors.txt`).
- **Still open at v3 cut**: the M5-4 SKILL.md append (SKILL.md still 448 L
  `92462fa7d71b3fed…` at 17:08Z; re-measure at commit); the gate's final
  revision + both runs at that revision; the round commit itself.
  The box-4 verdict and the §8 receipt are no longer open.
- **Boundary restated**: this lane wrote only this file in the repo; all
  writes in `/tmp/w5-scr-m5/` (plus the gate's own `/tmp/w5-mado-selftest.*`
  fixture dirs, created by running its selftest). No substrate file touched;
  no session disturbed (hypridle/lock state untouched; no mutating `hyprctl`
  verb; no network command).