# mado round-6 record — scribe prep DRAFT (SCR-M6)

Draft v1 window: 2026-10-14 17:38–17:44Z (local 14:38–14:44 −03:00). Lane SCR-M6.
**v2a/v2b (17:43–17:44Z): read §10 first.** Two round-6 notes landed:
`corpus/knowledge/remaining-planes-census.md` (333 L `710e3e289643f2ff…`,
lane M6-3; the plan's working name was `remaining-planes-live.md`) and
`corpus/knowledge/omarchy-drift-watch.md` (283 L `0a76a0f19cd7b73b…`, lane
M6-2 — a companion note + paste-ready arm spec, **not** a gate edit).
Self-measure at 17:45:02Z: 455 L, sha
`8e05dc1c5f4564bede97a1f3a4fbe0f4ff07de610d664896dcc8ceaead10cc14` (full);
this header line was written after that measure — re-measure at finalization.
**Headline prep: the gate-can-fail story — now pre-measured, with two
selftest gaps found.** At the round-5 gate revision the scribe preflight (same
tool, same suite line as lane (a)) got one mutant KILLED and two SURVIVED:
the gate can fail, and its selftest does not protect every declared clause.
Lane (a)'s ≥8-defect sweep remains the round's authoritative table; §3 is the
clause map that table must cover.
State at v1 cut (measured): HEAD `c03c249`; tree clean at 17:38Z (`git
status --porcelain=v1` → empty; by 17:44Z four untracked round-6 files —
the two notes above, this draft, `plans/round-7.plan.md`); gate
`tools/mado-verify.sh` 1,098 L (`wc -l`; 1,099
editor/git view) sha `d7edaab4bf108625…`; SKILL.md 518 L `5a2cd1f8f90527dc…`;
SHONEN.md 12 L `edace65e13c8ad20…` (4/4 `[x]`); SCORECARD.md 17 L
`2de41f5a71e31cbb…`; corpus/README.md 19 L `2dd274f5e270e65b…` (8 rows);
LOG.md 295 L `109ad5c8bcfde62b…`; PROVINCE.md 18 L `7aad7b863dc3c10b…`;
plans/round-6.plan.md 53 L `00d4072821cbb15e…`. **Round-6 artifacts**:
the two notes (see §10); `gate-mutation-proof.md` **absent**; gate
unrevisioned (mtime/size unchanged at 14:08 local through 17:45Z).
This file is scribe scratch product for the round-6 finalizer — **not the
record**. Nothing outside this file was written by this lane in the repo;
scratch `/tmp/w6-scr-m6/` (`anchors.txt`, `selftest.log`, `live.log`,
`preflight-spec.txt`, `preflight-work/`, `preflight2-spec.txt`,
`preflight2-work/`, `mutate-tool-selftest.log`). All probes read-only (file
reads, `sha256sum`/`wc`/`stat`/`git` read verbs, `pgrep`/`command -v`,
`omarchy version`/`theme current`, the gate's own hyprctl read verbs); no
substrate file under `~/.config`/`~/.local` written; no live session
disturbed; no network command.

Reading key: **⟨PENDING⟩** = must be resolved at finalization; every other
number names the command that produced it at v1 time. Tags: **[OBS]** measured,
**[INF]** inference from measured code/selftest, **[UNK]** unknown. Counts on
`.md` notes use `wc -l` (notes without a trailing newline show editor view =
+1). This draft currently ends **without** a trailing newline (`tail -c 1` →
`0xa9`), so `wc -l` counts one fewer than the editor view; re-measure both at
finalization (self-measure 17:45:02Z: `wc -l` 455).

## 0. Round-6 frame

- Plan (worktree, committed): `plans/round-6.plan.md` — 53 L, sha
  `00d4072821cbb15e…`, written ~17:04Z. Axis move: **operability** — ONE move,
  three ordered stages: (a) mutation-proof the round-5 gate via tameshi's
  harness (consumed read-only — a needed change is a recommendation to
  tameshi, never a patch); (b) omarchy version-drift watch arm (new declared
  plane in the gate); (c) remaining-planes live-surface arms (new note,
  working name `remaining-planes-live.md`). Ordering: **(b) and (c) are gated
  on (a)** — "if the gate cannot be mutation-proven, the round stops at (a)
  and says why."
- Claim (a) defect spec = **one mutant per declared contract clause, ≥8
  defects**: verdict token CLEAN|DIVERGED, the UNKNOWN-never-CLEAN arm, the
  exit map, the declared-plane census, sha comparison, reader fallback (§3
  maps each to gate lines). Suite = the gate's own hermetic selftest
  exercising `$MUTANT`: `--suite 'bash "$MUTANT" --selftest'`. Evidence =
  `corpus/knowledge/gate-mutation-proof.md`: per-defect
  KILLED/SURVIVED/INCONCLUSIVE + kill-rate headline + control green +
  `MUTATE_RESTORE: OK` (target sha256 before/after). A red control, an
  unrunnable suite, or target drift is a **SETUP refusal (exit 2) — no
  headline**.
- Claim (b) — declared baseline vs live, same verdict vocabulary; per-pin
  MOVED|HELD; any MOVED reads DIVERGED naming the pin; an unavailable probe
  reads UNKNOWN, never "clean"; **the baseline is never edited to match
  reality**. Read verbs only — no `git status` on the checkout.
- Claim (c) — declared-vs-live rows where a pair exists, runtime rows
  otherwise. Idle transitions stay UNKNOWN by constraint (MADO-R4-2) — not
  widened.
- Anti-claim (as written): **a surviving mutant is a FINDING** (selftest gap,
  recorded, not smoothed); any unverifiable check reads UNKNOWN, never CLEAN;
  no widening ships unproven. Measure: kill-rate table + restore proof +
  target sha; per-pin drift verdict; per-plane live rows; gate census
  before→after.
- Draft-time baseline pins for (b) — the watch's INPUT, measured 17:39Z
  (re-measure at dispatch; do not treat as output): `omarchy version` →
  `3.8.3`; `git -C ~/.local/share/omarchy describe --tags` → `v3.8.4`
  (`git rev-parse --short HEAD` → `8fcc9d60`); omarchy skill
  `~/.agents/skills/omarchy/SKILL.md` → 392 L / 14,908 B / sha256
  `becd149e4d1c0767…` / mtime 2026-10-03 17:42:32 −03:00; `omarchy theme
  current` → `Matte Black`. **Anchor: HEAD `8fcc9d60` is byte-identical to
  the round-1 pin** (`hyprland-config-plane.md:176-177`) → HELD since round 1;
  the two-value caveat (CLI `3.8.3` vs checkout `v3.8.4`) persists from
  round 3 (`waybar-walker-semantics.md` §8).
- Boundary: this lane is scribe — writes only this draft. The harness was
  consumed read-only (never edited; its sha pinned in §3); its sweeps ran
  against a **byte copy** of the gate in my scratch (sha equal to the repo
  file), so the repo artifact was never the mutation target from this lane.

## 1. Pre-state at v1 (round 5 landed; round 6 in flight)

- Round-5 commits: `eead56b` (14:33:30 −03:00, round-5 landing) + `c03c249`
  (14:34:46 −03:00, SHONEN boxes 3–4 evidence lines). `git show --stat
  eead56b`: LOG +1, SCORECARD +1, SKILL +72/−70, self-audit +83,
  walker-deep.md +618, round-5 draft +512, plans +76/+54, gate +1,099.
- Gate revision is the round-5 landing: `tools/mado-verify.sh` 1,098 L
  (`wc -l`), sha `d7edaab4bf108625…`, mtime 14:08 local. This is the plan's
  mutation target ("the round-5 gate as landed" — the older draft-path
  `corpus/scripts/verify-plane.sh` is absent; `corpus/scripts/` does not
  exist).
- SHONEN.md: 4/4 `[x]` (boxes 2 and 4 carry `VER-M3` / `VER-M4B` evidence
  lines) — PROBATION COMPLETE stands; **no box move is expected in round 6**.
- SKILL.md: round-5 append landed at `SKILL.md:451` ("Round-5 — verdict gate
  & box-4 closure status (append, M5-4)") incl. the gate usage block
  (`:460-468`); file 518 L `5a2cd1f8…`.
- **Record debt carried into round 6** (measured, cheap to repay):
  1. `corpus/README.md` — 8 coverage rows; missing `idle-lock-plane.md` (r4),
     `province-accuracy-selfaudit.md` (r4), `walker-deep.md` (r5); round-6
     notes will add 1–2 more. Ready text: `plans/round-4-record-draft.md`
     §4b (committed) for the two r4 rows (self-audit row needs a bracketed
     round-5 update: now 345 L `7c0a58208dea60e8…`).
  2. `SCORECARD.md:14` (round-4 row) and `:15` (round-5 row) are **stubs**;
     the full rows sit in the committed drafts (§4c of round-4 at lines
     ~311-319, and round-5 draft §4c).
  3. LOG.md:295 — the round-5 entry is a one-line summary; the round-5
     draft's fuller entry was not applied.
  4. Owed errata (round-5 draft §4e): `keybind-rule-semantics.md` §2.3
     dispatcher-tail prose (the `swapwindow` row is still at `:151`), runner
     V2/V3 receipts, K2 "29/29" scope wording. `grep -n 'Errata (round'`
     shows only round-2 and round-4 blocks — no round-5/6 block exists.

## 2. Deliverables and ⟨PENDING⟩ slots

### D1 (a) — mutation proof `corpus/knowledge/gate-mutation-proof.md` ⟨PENDING⟩

Must carry, per plan: per-defect KILLED/SURVIVED/INCONCLUSIVE; kill-rate
headline; control green; `MUTATE_RESTORE: OK` with target sha before/after
(= `d7edaab4…` unless lane (a) re-targets and says so); the tameshi tool sha
and the exact suite line; any SETUP refusal stated as such (no headline).
Harness contract facts (read from `tameshi-shokunin/tools/mutate-and-run.sh`,
r4-2, 1,001 L, sha `597e141989065e03…` — live value at 17:41Z, consumed
read-only): verdict vocabulary KILLED|SURVIVED|INCONCLUSIVE; exit map 0 done ·
1 done-with-inconclusive (DEGRADED) · 2 setup/refusal · 64 usage;
`MUTATE: SETUP (<reason>)` on refusal; kill-rate bands are a report
convention, not a gate.

**SCR-M6 pre-measured pilot [OBS]** (same tool sha, same suite line; target =
byte copy of the gate at `d7edaab4…`; workdirs in my scratch):

- Preflight 1 — 1 defect, `CLEAN_TOKEN_NOLIVE` (gate:1088, no-live CLEAN
  token → GREEN): `CONTROL: GREEN` (28/28), defect **KILLED** (exit 2; mutant
  selftest `FAILED — 27 passed, 1 failed`, `A: CLEAN verdict (missing:
  MADO_VERIFY: CLEAN)`), `MUTATE_RESTORE: OK`,
  `MUTATE: DONE defects=1 killed=1 survived=0 kill-rate=100%`. Workdir
  `/tmp/w6-scr-m6/preflight-work`.
- Preflight 2 — 2 defects, selftest-gap watch: `CONTROL: GREEN`;
  `PY_ABSENT_UNKNOWN_ARM` (gate:602, python3-absent waybar parse arm
  UNKNOWN→PASS) **SURVIVED**; `BOUNDARY_ALWAYS_PASS` (gate:738, boundary FAIL
  arm made unreachable) **SURVIVED**; restore OK; kill-rate 0%.
  Workdir `/tmp/w6-scr-m6/preflight2-work`.
- Interpretation [OBS+INF]: **the gate can fail** (headline provable) **and**
  its selftest has ≥2 unprotected clauses at the round-5 revision. Per the
  plan's anti-claim these survivors are findings for the record, not a
  failure of the round — the (a) lane's full sweep decides the final table
  (my two are candidates it may reproduce, extend, or contradict).
- Side effect recorded: a killed mutant's selftest keeps its fixtures
  (`/tmp/w5-mado-m52-selftest.uYJgkC` from preflight 1; outside this lane's
  namespace, left as evidence). PASS runs self-clean.

### D2 (b) — version-drift watch arm ⟨PENDING⟩

Gate census **before** [OBS]: 39 rows — hypr 9, hypr-live 20, waybar 4,
walker 1, terms 4, gate 1; statuses 35 PASS + 4 NOTE (0 FAIL/0 UNKNOWN);
`boundary.readonly PASS`; live verdict `MADO_VERIFY: CLEAN (35 pass, 4
notes; file + live planes verified read-only)` rc=0; selftest
`MADO_SELFTEST: 28/28 assertions passed` rc=0 (logs
`/tmp/w6-scr-m6/{selftest,live}.log`). After: ⟨PENDING — gate sha
`d7edaab4…` → ??; census 39 → 39+N; new plane/row ids; selftest count;
per-pin verdicts vs the §0 baseline⟩. Record must state which revision was
mutated if the gate is widened in-round (the mutation target is the round-5
revision; the widened revision needs its own selftest re-run).

### D3 (c) — `corpus/knowledge/remaining-planes-live.md` ⟨PENDING⟩

Draft-time spot-checks [OBS] (17:39Z; lane (c) re-measures and owns the
rows): alacritty processes `pgrep -x -c` → **3** (plan noted 2 at ~17:04Z —
re-measure; one may be this wave's own session terminal [UNK]); swaybg
consumer pid 1203358 `/usr/bin/swaybg -i
/home/vgpnk/.config/omarchy/current/background -m fill`; `~/.config/mako/config`
→ `/home/vgpnk/.config/omarchy/current/theme/mako.ini` (symlink); hyprsunset
binary `/usr/bin/hyprsunset` present, not running (`pgrep -x hyprsunset` rc=1
— identity profile); xdg-desktop-portal-hyprland pid 1203662 (consumer);
monitors already covered r2. Idle transitions stay UNKNOWN (MADO-R4-2).

### D4 — record debt repayment (record work, not a new claim)

README rows (≥3 + round-6 rows), SCORECARD rows 4/5 replacement + round-6
row(s), LOG round-6 entry. See §4.

## 3. The gate-can-fail dossier — clause → anchor → selftest coverage

Selftest scenarios (gate:338-430): A clean fixture → CLEAN/0; B broken
fixture → DIVERGED/1; C live requested, no hyprctl → UNKNOWN blocks CLEAN;
D usage contract. 28 assertions.

| # | Clause (plan's list) | Gate anchor | Selftest exercise [OBS from code] | Status at v1 |
|---|---|---|---|---|
| 1 | verdict token CLEAN (no-live) | :1088 | A expects it | **KILLED** (preflight 1) [OBS] |
| 2 | verdict token CLEAN (live) | :1090 | no scenario reaches a live CLEAN | [INF] untested arm → survivor candidate |
| 3 | verdict token DIVERGED | :1098 | B, C expect it | [INF] killable via token edit |
| 4 | UNKNOWN never CLEAN | :1086 (`FAIL=0 && UNKNOWN=0`) | C expects exit 1 + no CLEAN | [INF] killable (drop the UNKNOWN arm) |
| 5 | exit map CLEAN 0 | :1092 | A | [INF] killable |
| 6 | exit map DIVERGED 1 | :1099 | B, C | [INF] killable |
| 7 | exit map usage/bad-arg 2 | usage()/arg parse (:71-84) | D | [INF] killable |
| 8 | declared include-graph census + exact order | :463-497 | A (PASS), B (PASS isolation) | [INF] killable at `-ne`; a count-only (`-lt`) variant is a survivor candidate (never asserted against an extra source) |
| 9 | declared-plane row census | :645-663 (walker), :594-643 (waybar), :663-725 (terms) | A asserts specific rows | [INF] killable by dropping a row |
| 10 | sha comparison (boundary) | :735-742 | A asserts PASS only | **SURVIVED** when FAIL arm unreachable (preflight 2) [OBS] |
| 11 | sha comparison (record pin) | :571-578 (NOTE-only) | no assertion on the note | [INF] record-only impact; verdict-neutral by design |
| 12 | reader fallback (python3 absent → UNKNOWN) | :114-116, :602-604, :650-651, :667-669 | C's PATH sandbox re-links python3 when present → arm not exercised | **SURVIVED** (preflight 2) [OBS] |
| 13 | row_from_rc UNKNOWN mapping (rc 6) | :102-108 | B/C partially | [UNK] |
| 14 | anti-claim `live.plane UNKNOWN` | :763 | C | [INF] killable |
| 15 | boundary hash basis | :204-212 | A (fixture unchanged) | [INF] |
| 16 | worker/session hygiene (no session material) | header :28-30 | not selftest-checked | [INF] out of suite scope |

The two measured survivors name concrete selftest gaps: (10) no scenario
mutates the plane during a run, so the boundary FAIL arm is unprotected; (12)
the python3-absence UNKNOWN arm is never exercised. The (a) lane's ≥8-defect
spec must cover the plan's six named clause families; expect further survivors
in the [INF]/[UNK] rows — record them as findings with the mutant's @old/@new
text, never smoothed.

## 4. Record text to apply

### 4a. LOG.md round-6 entry (append after LOG.md:295)

```
- 2026-10-14 — round 6 (training r5): operability — the round-5 gate is
  mutation-proven falsifiable (tameshi harness `mutate-and-run.sh` sha
  `597e141989065e03…`, consumed read-only): ⟨fill: control GREEN, defects=M,
  killed=K, survived=S, kill-rate=K/M% , MUTATE_RESTORE: OK, target sha
  `d7edaab4bf108625…` before/after⟩. Survivors recorded as findings (selftest
  gaps), not smoothed: ⟨fill: per-survivor @old/@new + clause line⟩.
  SCR-M6 preflight before the sweep: 1/1 killed on the no-live CLEAN token
  (:1088) and 2/2 survived on the boundary FAIL arm (:738) + the python3-absent
  UNKNOWN arm (:602) — workdirs `/tmp/w6-scr-m6/preflight{,-2}-work`.
  ⟨If the sweep's table differs, the sweep governs; the preflight stays as
  ancillary evidence.⟩
  Version-drift watch arm: declared baseline vs live, per-pin MOVED|HELD —
  ⟨fill: pin table verdicts; any MOVED = DIVERGED naming the pin; UNKNOWN for
  unavailable probes⟩. Gate census 39 rows → ⟨fill⟩; gate sha `d7edaab4…` →
  ⟨fill⟩; selftest ⟨fill⟩ + live verdict ⟨fill⟩ at the committed revision.
  Remaining-planes note `corpus/knowledge/remaining-planes-live.md`
  ⟨fill: L / sha / rows: terminals runtime, swaybg, mako symlink, hyprsunset,
  xdph; idle transitions stay UNKNOWN (MADO-R4-2)⟩.
  Record debt repaid: README +⟨fill⟩ rows; SCORECARD round-4/5 stubs replaced
  + round-6 rows; ⟨errata applied? if any: list with block headers⟩.
  Boundary: gate + harness read-only; no substrate file written; no live
  session disturbed.
- ⟨If (a) fails or does not land: replace the first paragraph with the SETUP
  refusal text and stop — (b)/(c) do not ship (plan ordering).⟩
```

### 4b. corpus/README.md — coverage map rows

Apply the two committed round-4 rows from `plans/round-4-record-draft.md` §4b
(idle-lock-plane, province-accuracy-selfaudit; the self-audit row needs the
round-5 update: now **345 L** `7c0a58208dea60e8…`, addendum = M5-1/VER-M4B
receipt), then the round-5 row for `walker-deep.md` (617 L
`0982ba066c72575a…`, M5-3), then one row per round-6 note as measured
(gate-mutation-proof.md, remaining-planes-live.md). Append round-4-draft
§4b's round-4 addenda sentences only if the finalizer also repays the
errata-status lines (they describe ERR-M results) — otherwise keep rows to
the notes named here and let the round-6 commit state debt status.

### 4c. SCORECARD.md — move-log rows

Replace the two stub rows (`SCORECARD.md:14-15`) with the committed full rows
(round-4 draft §4c, round-5 draft §4c, re-measured at commit — the round-5
operability row must cite the gate at the committed revision), then append
round 6:

```
| 6 | operability | round-5 gate selftest-green but never mutation-tested (a broken gate would block all widening) | gate mutation-proven: ⟨fill: M defects, K killed, S survived⟩ + restore proof; selftest gaps found (⟨fill: the SURVIVED clause lines⟩) recorded as findings; version-drift plane added (⟨fill: pins HELD/MOVED⟩); remaining-planes note landed (⟨fill: L, sha⟩) | `MUTATE: DONE killed=⟨fill⟩ kill-rate=⟨fill⟩`; `MUTATE_RESTORE: OK` target `d7edaab4…`=after; tool sha `597e1419…`; gate census 39→⟨fill⟩, sha `d7edaab4…`→⟨fill⟩; drift pins: `omarchy version` ⟨fill⟩ / describe ⟨fill⟩ / skill sha ⟨fill⟩ / theme ⟨fill⟩; SCR preflight `/tmp/w6-scr-m6/preflight{,-2}-work` |
```

⟨If stage (a) fails: the round-6 row reads the refusal (SETUP reason, exit 2)
and states (b)/(c) did not ship — no kill-rate claim.⟩

### 4d. SHONEN.md

No box move expected: 4/4 `[x]` since round 5; promotion remains the
operator/integrator decision. If the finalizer edits any evidence line,
re-apply the seed-diff check (`PROTOCOL.md:419-431`); otherwise the file
stays byte-identical at `edace65e13c8ad20…`.

### 4e. Errata status

Still owed (append-only when applied): the round-5 §4e list — `keybind-rule-
semantics.md` §2.3 dispatcher-tail prose (`swapwindow` row at :151), runner
V2/V3 receipts, K2 "29/29" scope. No round-5/round-6 errata block exists as
of v1 (`grep -n 'Errata (round'` → round-2 + round-4 blocks only). Any
mutation-sweep recommendation to tameshi (harness changes) is a
recommendation to that lane — record it in this repo's LOG unknowns, never
as a patch.

## 5. Scribe measurements and spot-checks (v1, executed)

1. **Repo pins** (17:38–17:40Z): LOG 295 L `109ad5c8…`; SCORECARD 17 L
   `2de41f5a…`; SHONEN 12 L `edace65e…`; SKILL 518 L `5a2cd1f8…`; README
   19 L `2dd274f5…` (8 rows); PROVINCE 18 L `7aad7b86…`; round-6 plan 53 L
   `00d40728…`; gate 1,098 L `d7edaab4bf108625…`; walker-deep 617 L
   `0982ba06…`; idle-lock 381 L `a0597be9…`; self-audit 345 L `7c0a58208…`;
   round-4 draft 474 L `c690a931…`.
2. **Gate runs** (read-only): `bash tools/mado-verify.sh --selftest` →
   `MADO_SELFTEST: 28/28 assertions passed` rc=0; live → `counts: pass=35
   fail=0 unknown=0 skip=0 note=4` + `MADO_VERIFY: CLEAN (35 pass, 4 notes;
   file + live planes verified read-only)` rc=0; row census 39 (§3/D2);
   logs `/tmp/w6-scr-m6/{selftest,live}.log`.
3. **Harness + preflights**: tool selftest `MUTATE_SELFTEST: 37/37 pass` /
   `VERDICT: PASS`; tool sha `597e1419…`; preflight 1 KILLED + restore OK;
   preflight 2 two SURVIVED + restore OK; workdirs in `/tmp/w6-scr-m6/`.
4. **Draft-time pins** (17:39Z): omarchy `3.8.3`; describe `v3.8.4`; HEAD
   `8fcc9d60` (= round-1 pin → HELD); theme `Matte Black`; skill 392 L /
   14,908 B / `becd149e4d1c0767…` / mtime 2026-10-03 17:42:32 −03:00.
5. **Live surface** (17:39Z): alacritty ×3; swaybg 1203358; mako symlink →
   theme `mako.ini`; hyprsunset present/not running (rc=1); xdph 1203662.
6. **Boundary**: read-only throughout; writes = this draft + `/tmp/w6-scr-m6/`
   + tool-owned selftest fixtures (self-clean on pass; the one from preflight
   1 kept by the gate's own failure branch).

## 6. Observations (v1)

(a) The round's headline is now two-sided and pre-measurable: **the gate can
    fail** (1/1 killed on the verdict-token clause) **and the selftest has
    gaps** (2 survivor candidates at the round-5 revision). Both are exactly
    what the plan's ordering wanted before widening — and the survivors are
    the kind of finding the anti-claim reserves room for.
(b) The round-5 commit left record debt (README 8 rows; SCORECARD stubs 4/5;
    terse LOG). The round-6 commit can repay all of it from committed drafts
    — cheaper than another discovery round.
(c) My preflight mutated a byte copy (sha equal), not the repo path — lane
    (a)'s sweep is authoritative; **do not cite the preflight as the round's
    mutation proof**.
(d) The drift watch's first input is stable: HEAD `8fcc9d60` matches the
    round-1 pin; only the CLI-vs-checkout two-value caveat is outstanding
    (record it as HELD/INFO, not MOVED).
(e) Runtime counts drift intra-day (alacritty 2→3 between the plan and my
    pass; cause [UNK], possibly this wave's own terminals). Lane (c) must
    timestamp every runtime row and name the probe command.
(f) The plan's target-resolution note (draft path vs landed path) resolves
    clean: `corpus/scripts/` absent, `tools/mado-verify.sh` present;
    mutation target = `d7edaab4…`.

## 7. Unknowns (v1)

1. Whether lane (a)'s ≥8-defect sweep lands in-window; its kill-rate headline
   and survivor list (my 2 are candidates only).
2. Whether the gate's final committed revision still equals `d7edaab4…`; if
   (b) widens it, which revision the mutation table cites (must be stated).
3. Whether (b)/(c) ship at all (gated on (a)); if (a) refuses (SETUP), the
   round stops and the record says why — no deprecation of rounds 5's values.
4. Round-6 lane labels/attributions: scratch dirs `/tmp/w6-mado-m61`,
   `m6-3`, `m6-4` observed; no assignment map visible from inside this lane
   [UNK] — record by artifact self-label (round-5 lesson).
5. Whether a named verifier seat (VER-M6) exists this round — none seen at
   v1 cut; SHONEN needs no move either way.
6. Whether the finalizer folds D4 (record debt) into the round-6 commit
   (this draft assumes yes — cheapest correct state).
7. Whether tameshi's service `--regression` ever covers the mado case (not
   this round; mado only consumes the tool).

## 8. Falsifiable next-iterations (carry + new)

- Land the ≥8-defect sweep; if survivors ≠ my 2, say which (and whether mine
  reproduce); if 0 survivors, say how the two preflight arms got covered.
- Version-drift plane ships with per-pin HELD/MOVED + census delta; no claim
  before it is in the gate.
- `remaining-planes-live.md` rows; idle transitions remain UNKNOWN.
- Repay record debt (README/SCORECARD/LOG); apply the three owed errata as
  append-only blocks.
- `corpus/lessons/round-6.md` — the lessons dir is still empty (`ls
  corpus/lessons` → 0 files); round-1 promise keeps failing through round 6
  unless a lane is chartered.
- Durability: fold the mutation workdir headline + tool sha + target sha into
  the record (scratch does not survive).

## 9. Finalization checklist (mechanical, ordered)

1. Re-measure §5.1 anchors + §5.4 pins; note any drift as freshness rows.
2. Read lane (a)'s `gate-mutation-proof.md`; verify its target sha equals the
   gate revision it names; copy control/kill-rate/restore lines into §4a/§4c;
   list survivors with their clause anchors.
3. Read the gate's final revision; re-run `--selftest` + live at the revision
   being committed; compute the census before→after; fill D2/§4a/§4c.
4. Fill (b) pin verdicts from the committed revision (HELD/MOVED/UNKNOWN per
   pin; MOVED ⇒ DIVERGED naming the pin).
5. Apply 4a (LOG), 4b (README rows incl. the two committed r4 rows), 4c
   (SCORECARD: replace stubs + append round 6), 4d (SHONEN — likely no-op),
   4e status.
6. Commit under the lane identity; freeze every cited sha in the entry; check
   the gate/harness/note shas appear.
7. If (a) refused or is red at commit: record the SETUP/refusal text, mark
   (b)/(c) unsent, and keep this draft as the record's ancestry.

## 10. v2 update — artifacts landing during the scribe window

**v2a (17:43Z): lane (c) landed the remaining-planes note — and the name
moved.** `corpus/knowledge/remaining-planes-census.md`, **333 L** (`wc -l`),
sha `710e3e289643f2ff…`, mtime 14:43 local, self-labeled "round 6, lane
M6-3". It supersedes every `remaining-planes-live.md` reference above (the
plan's working name); read D3's expected rows against the landed file:
§0 coverage ledger (what each PROVINCE surface already had vs this adds), §1
theme/wallpaper declared-file census, §2 consumers (incl. the walker/waybar
css import chains), §3 terminal runtime rows, §4 display/session shape
(session/portal/OSD), idle transitions stay UNKNOWN (MADO-R4-2). It **adds
no gate rows** by design: at its probe time no mutation-proof artifact
existed, so the plan's ordering was honored; the note says so itself. It
also carries an append-only errata already: **E2** — the mako
`notifications` layer surface is not permanently mapped (two point samples,
17:39:32Z vs re-run ~17:43Z; cause `[UNK]`), a live finding the record
should keep visible. Probe window 17:39:02–17:41:45Z; read verbs only; no
theme command run; no session mutated. [OBS]
For the record text: 4a's note line reads this file + these measures; 4b's
round-6 row is this artifact; D3 is otherwise closed as "landed".

**Still open at v2a**: (a) mutation proof (absent; the (b) drift lane and my
D2 slots stay ⟨PENDING⟩), gate revision unchanged (`d7edaab4…`, mtime/size
unchanged through 17:43Z).

**v2b (17:44Z): lane (b) landed the drift arm as a NOTE + SPEC, not as a
gate edit — a plan-vs-landing divergence the record must state.**
`corpus/knowledge/omarchy-drift-watch.md`, **283 L**, sha `0a76a0f19cd7b73b…`,
self-labeled "(M6-2, round 6)"; probe scratch
`/tmp/w6-mado-omarchy-drift/`. Its §5 records the call and the reasons:
write scope (one output file per lane), the plan's (b)-gated-on-(a) ordering
(a gate edit now would move the frozen target sha the mutation proof needs),
and selftest plumbing (the selftest's row-count regex hard-codes six plane
ids, `mado-verify.sh:352,356`). Its reason 3 also claims the landed selftest
"invokes the committed path `"$BASH_BIN" "$0"`" — for the mutation suite
that is exactly why `bash "$MUTANT" --selftest` works (my preflight killed a
mutant through it [OBS]), so read reason 3 as "the selftest's plane-id
fixture plumbing needs widening", not as an unusable suite. §6 is a
paste-ready arm spec (plane `omarchy`: rows `omarchy.version.cmd`,
`omarchy.git.tag`, `omarchy.git.head`, `omarchy.skill.link`,
`omarchy.skill.sha`, `omarchy.skill.vs_head`, `omarchy.cmd.groups`,
`omarchy.theme`; HELD→PASS / MOVED→FAIL naming the pin; unavailable→UNKNOWN;
selftest scenarios A/B/C sketched; open decision D-1 = whether the theme row
prints HELD|MOVED as a NOTE or is verdict-affecting). §3 drift classes C1–C7;
§4 docs-vs-live register; §7 probes not run; §8 OBS/INF/UNK; append-only
errata section present. [OBS]
Record consequences: (i) D2's "gate census 39 → ⟨PENDING⟩" now reads
**39 → 39** unless the finalizer lands §6's rows (then re-measure the
widened gate's selftest/census); (ii) the round's (b) claim is met as
**spec + baseline measured**, with the landing deferred to ride (a) — state
that plainly rather than claiming a shipped plane; (iii) if the finalizer
lands the arm, the mutation table's target revision and the widened revision
differ — say which was mutated (my §7.2 already flags this).
Also at 17:44Z: `plans/round-7.plan.md` appeared (untracked, 127 L
`6e62d0b5d935ab89…`) — another lane's prep; do not fold into the round-6
commit (same pattern as round-5 obs (e)).

⟨Further updates: append v2c+ here if `gate-mutation-proof.md` or a gate
revision change lands before the finalizer reads this. v1 numbers above stay
for provenance; tag each update with its own measurement time.⟩