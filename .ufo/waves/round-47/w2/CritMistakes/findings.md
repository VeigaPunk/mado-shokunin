# CritMistakes — findings (round 47, wave w2, FALSIFY)

Seat: CritMistakes · lane: mado-shokunin · date 2026-10-26 · lane tip read `9bddd6ac` · base `60edb66e`.
Task: audit `w1/ScrMistakes/mistakes.md` (rows M47-1..M47-6, proposed criteria 91-95): is every fix shown
able to fail? Is the class right? Add this round's already-made mistakes (seat runaway write, host cache
rewrite, misrooted SentHost dir, w1 draft C2 counter coupling). Corrected table below. Every claim names a
path:line, a command + its output, or a hash; verification receipts are in `receipts/` of this seat.

## 0. Method and verification receipts

All checks were re-run read-only in the lane (no mutating git/jj, no host writes, XDG_CACHE_HOME never
used; the resolver was not executed). Receipts:

| receipt | what it shows |
|---|---|
| `receipts/verify-check91.txt` | check91 red (`verdict=DIFFER`, exit 1) on the r46 entry at `1001bda`, green (`verdict=AGREE`, exit 0) on `corrected-entry.md` |
| `receipts/verify-check92.txt` | check92 at HEAD: `ExecStofOracle` now `uncommitted=0 verdict=OK`, `ExecSerialRule`/`ExecSupersede` OK (the w1 red case was fixed by L1 R2; see M47-2) |
| `receipts/verify-session-gate.txt` | `check-session-material.py` at `c24adef2`: `findings=115 … exit=1`; at HEAD: `findings=118 … exit=1` |
| `receipts/verify-footprint.txt` | copy of `w1/ScrErrataCal/receipts/footprint.txt` (untracked `.ufo/waves/round-47/SentHost/` at rev `c24adef2`) |
| `receipts/verify-scratch-sizes.txt` | `du -sh` of `/fast/scratch/hyaku/mado-r47/*` (19:39): `CritC2Forgery` 2.5G > 2G cap |
| `receipts/verify-quotes-grep.txt` | each quoted fragment verified by `grep -F` at its locator |

## 1. Corrected mistakes table

| id | class | shown able to fail? (red / green) | class right? | corrected note |
|---|---|---|---|---|
| M47-1 | `provider` | YES — `check91.py` red on the entry at `1001bda` (`PRODUCER … producer=l1-draft/mado-devices.py … verdict=DIFFER`, exit 1), green on `corrected-entry.md` (`verdict=AGREE`, exit 0); receipt `verify-check91.txt` | YES — a live run attributed to the draft's receipt is a producer-identity defect (M46-5 class) | the entry at HEAD still cites `live-devices-host-l1.txt` (`corpus/knowledge/hyprland-input-devices-r46.md:57`) — the fix is routed (R1 erratum), not yet applied; check91 does not check the sentence's config-count wording, which the erratum must carry |
| M47-2 | `landing` | YES — red: `out.json.rows.tsv` untracked, 3 282 451 B, at w1 (`verify-check92.txt` in w1 receipts; `git status` in `r2-state.txt`); green: check92 at HEAD now `verdict=OK` because L1 R2 removed the file and committed a digest (`.ufo/waves/round-47/receipts/r2-removed.txt` sha256 `6573f76b…`) | YES — evidence produced in r46, still uncommitted a round later | the instrument still fires on any uncommitted seat file (mechanism generic); the green state today is the fix having landed, not the instrument failing to fire |
| M47-3 | `vacuous` | YES — the waiver sentence is present at `SKILL.md:770` ("no synthetic marker yet, so a red exit is expected until it lands"); the gate is red at `c24adef2` (`findings=115`, exit 1) and still red at HEAD (`findings=118`, exit 1) — receipt `verify-session-gate.txt` | YES — a registry cell that declares its own red exit is a standing waiver (criterion-56 shape) | NEW nuance: at HEAD the gate adds an R3 finding in `w1/ExecSessionMarker/check-session-material.py` (keys=serial+ident) — the wave's own drafted marker material trips the gate. A naive "install marker, re-run to findings=0" cannot reach 0 while the marker seat's committed files carry the very patterns; the fix must scrub/exempt those files. The planted/tampered receipts exist (`w1/ExecSessionTriage/receipts/04-marked-49.txt`, `06-planted-real-dump.txt`, `07-tampered-waived-fixture.txt`) |
| M47-4 | `landing` | YES (red only) — at HEAD: `corpus/SOURCES.md` has 262 rows, last `S325`, 0 `S326+`; `w1/ExecSupersede/rows.md` carries drafted ids S326-S333; receipts `r4-deferral.txt` | YES — a routed item carried past three routings | green state does not exist yet (rows are draft); the two count commands are the red case |
| M47-5 | `number-drift` | YES — ledger rule `ages.md:14-15` (`age = 46 − first_routed_round`) vs cell `ages.md:88` (`**3**`) vs lesson `round-46.md:311` ("age now 4 rounds"); deferral sites r44:93, r45:68, r46:307, spotcheck:116 → four; receipt `age-drift.txt`, `verify-quotes-grep.txt` | YES — hand-carried numbers disagree with the instruments cited | both conventions are internally consistent (exclusive boundaries vs inclusive rounds); neither file states which the sentence uses — the fix must make the ledger emit the sentence |
| M47-6 | `landing` | YES — the pyc is in the frozen tree (`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc`, 40149 B, mtime 18:45:35 after tip `edc14789` 18:26:38, ignored by `.gitignore:3`); guards: `c1-r46-devices.py` 0, `-v2.py` 1, `-v3.py` 1; repro receipts `pyc-state.txt`/`pyc-header.txt` | PARTLY — `landing` names the artifact; the deeper defect is that M46-13's fix landed on only 2 of 3 counters and the gap **survived** — recommend tagging `survivor` as well (round-46.md:275 already classes M46-13 `landing`; the recurrence is the survivor signature) | v1 still imports the pinned model in-process (model-load receipt) — the concrete residual is the v1 counter + the existing pyc |
| N1 | `scope` | YES (red) — `/fast/scratch/hyaku/mado-r47/CritC2Forgery` measured 2.5G > 2G at 19:39 (`verify-scratch-sizes.txt`); the empty-argv spin hazard (resolver never returns) is proven in `w1/ExecFixtures/receipts/empty-arg-spin.txt` and `ExecRefA.md` F4 | class `scope` fits (an unbounded operation exceeded its budget); note the CORPUS vocabulary has no resource-limit class — extend with `bounds` if the taxonomy grows | the ~590 GB runaway is orchestrator-reported; first-party residue: `ExecRefB.md` §6 ("deleted after the receipts were copied here … Nothing was written outside this seat directory") and no surviving `ExecRefB` scratch — the gap is that no instrument measured seat-scratch sizes, so the violation was only visible at disk level. Fix: per-seat scratch cap, per-file caps (`head -c`, `timeout`), and an end-of-round size receipt per seat; the measure above shows the cap is enforceable |
| N2 | `scope` | YES — red: the host cache was actually opened `O_WRONLY|O_CREAT|O_TRUNC` and restored byte-identically (190 B, sha256 `f497ed05…`, mtime 17:42:25; `SentHost/report.md` F2b, receipts `host-cache-observed.txt`, `cache-restored.txt`); trap documented in `cache-write.txt` (unset **and** empty `XDG_CACHE_HOME` fall back to `$HOME/.cache`) and `ambient-cache-env.txt` (`HOME=<scratch>` alone does not redirect the ambient cache) — green: explicit per-run `XDG_CACHE_HOME` redirect writes only into the scratch cache | YES — a write outside the allowed area (host `~/.cache`) | the w2 host guard already freezes "only with XDG_CACHE_HOME pointing into your scratch"; the freeze should also reject the empty-value spelling and assert no resolver `open` under `$HOME` |
| N3 | `scope` | YES — red: untracked `.ufo/waves/round-47/SentHost/` (misrooted, outside `w1/`) at rev `c24adef2`, recorded in `w1/ScrErrataCal/receipts/footprint.txt:11` — green: the path is absent now and the seat report is at the correct `w1/SentHost/report.md` (committed) | YES — a seat wrote outside its own directory (the wave's own rule) | the L1 moved/cleaned it before the freeze; prevent recurrence with an inventory check that flags any seat-named dir directly under `round-47/` (extension of criterion 92) |
| N4 | `scope` | YES — red: the w1 draft `w1/ExecCounterC2/c2-r47-terminal-entry.py` extracts and runs `tools/mado-terminal.py` (docstring line 73 "extracts tools/mado-terminal.py at REV and runs `explain --observed`", `TOOL = "tools/mado-terminal.py"` line 116, tmp write+run lines 629-633) — so C2 depended on C1 and a candidate repo without the tool would setup-fail clause f. Green: the committed `quality/counters/c2-r47-terminal-entry.py` binds clause f to a committed capture (`resolver_sha256=`, `observed=`) and never runs our tool (docstring 68-73; no `TOOL` extraction), and the POS control admits an entry-only tree (receipt `ctl-pos.txt`: `admitted=1/1`, exit 0; build-control.py:259-299 writes only a stub "control double", not the lane tool) | YES — an instrument that scores beyond its own clause (claim coupling), violating the separability rule; it is also a latent `vacuous`-adjacent trap (C2 could neither pass nor fail independently of C1) | registry records the change at `registration.md:25-26`; separability shown both ways at `registration.md:80-84` |

## 2. Proposed criteria 91-95 — audit
| criterion | runnable as written | red (fires) | green (clean) | note |
|---|---|---|---|---|
| 91 | yes (`check91.py`) | yes (M47-1) | yes (corrected-entry) | does not police the config-count sentence (erratum remains manual); reads the entry from the worktree |
| 92 | yes (`check92.py`) | yes (w1 receipt) | yes at HEAD (post-R2 cleanup) | extend to scratch sizes (N1) |
| 93 | yes (`grep -n 'expected until it lands' SKILL.md` prints the waiver) | yes | not yet (post-install) | installation must not add new findings (M47-3 nuance) |
| 94 | no standalone script shipped; the documented one-command read is reproducible | yes (ages.md:88 3 vs round-46.md:311 "4"; four deferral sites) | not yet (L1 must pick the convention) | recommend the ledger emits the sentence |
| 95 | yes in principle (before/after `find -newer` inventory); full counter-run inventory not executed here | yes (pyc present; unguarded import repro) | yes (guarded import leaves no dir) | sub-behavior proven by `pyc-state.txt`/`pyc-header.txt` |

`check88-as-written.txt` (green) and the w1 "Checked and found clean" section stand as-is.

## 3. Residuals and conflicts recorded for the judge

1. M47-5 conflict stands: two self-consistent age conventions; the lesson and ledger disagree by one; neither states its convention.
2. M47-6 class: `landing` vs `survivor` — record both; the actionable residual is v1's unguarded in-process import.
3. N1: the ~590 GB figure has no first-party lane receipt; the fix must make seat-scratch size a measured, committed number.
4. N2: the pre-existing 190-byte cache content at 17:42:25 predates the wave; only the 18:50:55 rewrite is attributed (SentHost F2b).
5. Empty-argv spin: documented hazard, excluded from fixtures by design (`ExecFixtures.md` §14); do not make it a fixture (expect cannot express "never returns").

## 4. Receipt index (this seat)

| file | content |
|---|---|
| `receipts/verify-check91.txt` | check91 red + green, both directions, exit codes |
| `receipts/verify-check92.txt` | check92 on ExecStofOracle / ExecSerialRule / ExecSupersede at HEAD |
| `receipts/verify-session-gate.txt` | session-material gate at `c24adef2` and HEAD (exit codes) |
| `receipts/verify-footprint.txt` | w1 footprint snapshot (`?? .ufo/waves/round-47/SentHost/`) |
| `receipts/verify-scratch-sizes.txt` | `du` of round-47 scratch at 19:39 (one seat > 2G) |
| `receipts/verify-quotes-grep.txt` | `grep -F` verification of every quoted fragment at its locator |
