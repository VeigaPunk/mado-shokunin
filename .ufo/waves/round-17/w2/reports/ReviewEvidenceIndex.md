# ReviewEvidenceIndex — round 17 wave 2 (FALSIFY): cited-receipt index audit

Seat: `MadoR17.ReviewEvidenceIndex` (reviewer, leaf). Audited commit:
`988b858bd6049bc709807534fd725c05264f7e60` (lane HEAD at audit start).
Docs under audit: `corpus/lessons/round-17.md` (blob `2e11f717…`),
`SKILL.md` (`dda70e42…`), `SCORECARD.md` (`c1b200ce…`), all read with
`git show 988b858:<path>`.
Installs/updates by this seat: **none**. No pacman/yay/paru/sudo/systemctl/
hyprctl/live probe. Commands run: read-only `git show|log|diff|cat-file|
ls-tree|hash-object`, `sha256sum`, `cat/sed/grep`, the three permitted
hermetic instruments (`mado-tripwire.py --scan/--selftest`, `label-check.py`,
`measure.py`), and `/var/log/pacman.log` as file bytes.

## Axes (godspeed)

1. **Existence** — every cited receipt resolves at `988b858`.
2. **Token fidelity (QUALITY 23)** — each attested verdict token is on the
   receipt's outcome side, not want-side/prose/`matched_exit`.
3. **Arithmetic** — every count/score in the three docs re-derives from
   committed bytes; receipts reproduce when the instrument re-runs.
4. **Binding** — receipt `measured_commit`, gate/script sha256, and the
   cited revision agree.
5. **Citation integrity around receipts** — non-token sentences attached
   to a receipt (disclosure claims, revision lines) survive a counterexample
   search.

Each move below was kept only where it added a check that could fail.
The frontier I walked: instrument output → receipt bytes → doc sentence →
aggregate (oracle/session) → upstream revision.

## Verdict summary

- All **24** committed files under `.ufo/waves/round-17/evidence/` exist at
  `988b858`; every evidence receipt cited by the three docs by name, range,
  or brace form resolves. **No cited evidence receipt is missing.**
- Every verdict token the three docs attribute to an evidence receipt is on
  that receipt's outcome side at the revision cited. **No QUALITY-23 token
  misattribution found in round 17's own docs.**
- Every number re-derived (C1 14/22→15/23; C2 2/6→4/6; C3 absent→present;
  selftests 9/9, 16/16, 33/33; anchor 8 findings/7 calls; join 4/4;
  oracle agreement 0 oracle-only; 21 tripwire-only; 70 seat files;
  228/228 transcript digests) **reproduced exactly**.
- Four concrete defects found — one Medium (F1), one Medium-low (F2), two
  Low (F3, F4) — none of them a receipt-token mismatch; plus one benign
  transcript-drift note (F5) and one worktree coordination risk (O1).

## Findings (severity order)

### F1 (Medium, existence at HEAD) — M4's cited seat report is not in the commit

`corpus/lessons/round-17.md:17` (M4, evidence-pointer cell) cites
`w1/reports/SentinelHostPause.md` H1-H3. At `988b858` that path does not
exist:

```
$ git ls-tree -r --name-only 988b858 -- .ufo/waves/round-17/w1
.ufo/waves/round-17/w1/dispatch.json
.ufo/waves/round-17/w1/record.json
.ufo/waves/round-17/w1/spec.json
$ git ls-tree -r --name-only 988b858 -- .ufo/waves/round-17/w1/reports | wc -l
0
```

All 70 wave-1 seat reports are untracked (`git status`: `?? .ufo/waves/
round-17/w1/reports/`). The same applies to the Gate paragraph's cited
reports `SrcIdleNotifyProto`, `SrcHyprlockLockProto`, `SrcLogindLock`
(lesson lines 34-36): all three are present only in the worktree.

Substance check, off-commit: the working-tree `SentinelHostPause.md` does
contain H1-H3 as M4 describes — H1 harness-appended tooling directive
(`sudo pacman -S` channel one; `dispatch.json` 0/70 tasks contain it),
H2 npx/uv channels, H3 bare `tools/mado-verify.sh` live `hyprctl` path. So
the report is real; the defect is that a reader at the audited commit cannot
resolve the citation, and QUALITY 23's "citation is to committed bytes"
fails for this pointer. Fix: commit the wave-1 reports with the round, or
cite a committed artifact.

### F2 (Medium-low, false parenthetical at HEAD) — "only the r13 spot-check names it"

`corpus/lessons/round-17.md:20` (M2) says:

> r13 wayland-utils install (only the r13 spot-check names it)

Counterexample: `LOG.md:798-799` names it explicitly:

```
**Tool install:** wayland-utils **1.3.0-1**, pacman extra,
`sudo pacman -S --needed --noconfirm wayland-utils`, to obtain the assigned
`wayland-info` diagnostic route
```

and `corpus/lessons/round-13-verifier-spotcheck.md:211` also names it
("Lane installation verified ... wayland-utils 1.3.0-1"). The load-bearing
half of the sentence is true — `corpus/lessons/round-13.md` does not
disclose the install (grep: no install/sudo line) — but "only" is false at
`988b858`. Note: the worktree already holds an uncommitted correction
replacing the parenthetical with "disclosed in LOG.md:798-799 and seat
reports, absent from `round-13.md`", so this is a HEAD-state defect only.

### F3 (Low, receipt provenance) — label-check receipt's revision line names a commit without the instrument

`evidence/label-check.txt` (blob `499ce9f8…`) ends:

```
exit=1
245fd1149dc1dbee1cc1db849b43035ba5ff54c5
b890a5ca…  .ufo/waves/round-17/label-check.py
2e28fc84…  .ufo/waves/round-17/label-claims.json
```

`245fd11` is `git rev-parse 245fd11` → the wave-1 "want-side mutant fixture"
commit, whose tree contains only `label-fixtures/want-only.json`
(`git show --stat 245fd11`). At that revision:

```
$ git cat-file -e 245fd11:.ufo/waves/round-17/label-check.py
fatal: path ... exists on disk, but not in '245fd11'
$ git cat-file -e 245fd11:.ufo/waves/round-17/label-claims.json
fatal: ... not in '245fd11'
```

The instrument and claims were committed one commit later (`3722ba4`,
`git show --stat 3722ba4`). The receipt's sha256 lines *do* match the
committed bytes (`b890a5ca…` / `2e28fc84…` = HEAD blobs), and re-running at
HEAD reproduces the tool's output lines verbatim (`LABEL_SUMMARY 4/7`,
`EXPECT_SUMMARY 7/7`, exit 1), so the tokens are sound. The wart is
that the receipt cannot be reproduced by checking out the revision it names:
it was produced from an uncommitted worktree. QUALITY 23 is not literally
violated (the citing sentence names no revision and the receipt has no
`measured_commit` field), but the revision line is misleading next to
"citation is to committed bytes only".

### F4 (Low, instrument provenance) — label-check reads its claims from disk, not `git show`

`label-check.py` opens the claims file with `open(claims_path)` while docs
and receipts go through `git_show(root, rev, path)`. The SKILL registry row
(`SKILL.md:558`, write-scope/pinned-value column) says "`git show` of
committed bytes only". At audit time `label-claims.json` is unmodified
(`git status` clean for it; `git hash-object` = HEAD blob `2e28fc84…`), so no
current verdict is affected. But a worktree edit to the claims file changes
the verdict without a commit. This is a divergence between the registry
claim and the code; flagged for the label-check code owner.

### F5 (Info, benign drift) — one r17-w1 transcript grew after the receipt

`evidence/tripwire-r17-w1.txt` records 70 files; 69 of 70 sha256 values
still match the live transcripts. `MadoR17.TripwireCore.jsonl` was recorded
at 85 lines / `069f23a9…`; live is 86 lines / `8c248a5c…`. The extra record
is `{"type":"custom","customType":"session_exit","data":{"reason":"dispose",
"kind":"normal"}}` at 14:51:18Z — no command. A live re-scan of that file
returns `MADO_TRIPWIRE: clean`, counts all zero, `unparsed_spawns: 0`. The
"clean / 1 unparsed spawn / 1 unparsed eval cell" claim therefore survives
the drift; receipts are snapshots, not live digests.

### O1 (Coordination risk, worktree only, not a HEAD finding) — uncommitted S071 will make the Gate counts stale

At audit time the worktree (not `988b858`) has uncommitted edits to
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/terminal-route-
r17.md`, `corpus/lessons/round-17.md`. `SOURCES.md` gains row **S071**
(host Alacritty desktop entry) and `terminal-route-r17.md` adds `S071` to its
`source:` line, while the working-tree lesson still says
"Rows before→after: 55 → 70; tier A 51 → 63 … mined 43 → 55" and its
"S056-S070" table stops at S070. If those edits are committed as-is, the
committed row count becomes 71 (A 64, mined 56) while the lesson text stays
at 70 — recreating exactly the count-mismatch class this audit checks. The
main agent must update the Gate counts and the new-rows table (or drop S071)
in the same commit.

## Evidence index — every cited receipt, checked

Existence is against `988b858` (`git ls-tree`); hashes are sha256 of the
committed blob. "Reproduced" means this seat re-ran the instrument and
diffed/compared its output to the receipt.

| receipt (HEAD blob sha256) | cited at | sentence tokens checked | verdict |
|---|---|---|---|
| `frozen-tampered-recut.json` `2e44f207…` | lesson M1 (line 15) | exit 2 `snapshot_tampered`; control exit 0 `frozen_match` | PASS — both runs in receipt; `measured_commit` `0175f13` = gate `226220ae…`; pristine digests = `.ufo/waves/round-16/frozen/{expected,plan,policy}.json`; tampered digest `052c03b2…` reproduced from the one-byte `libinput`→`libinpuv` edit |
| `label-check.txt` `499ce9f8…` | lesson M1 | `R16-V1-red` MISMATCH; `want-side-only-mutant` MISMATCH; `superseded-commit-mutant` MISMATCH; greens ok; `EXPECT_SUMMARY: 7/7`; exit 1 | PASS — re-run tool output identical (`LABEL_SUMMARY 4/7`, `EXPECT_SUMMARY 7/7`), shell exit 1; see F3 for the revision line |
| `measure-before.json` `54d3ca…` | SCORECARD line 881 | baseline 2/6 = 3.3333 | PASS — `measure.py 27cd06f` reproduces c1 `{22,14,6.3636}`, c2 `2/3.3333`, c3 absent byte-for-byte in value |
| `measure-instrument.json` `1b675a…` | SCORECARD line 881 | baseline stays 2/6 under the tightened instrument | PASS — `measure.py f52f43f` reproduces the same c1/c2/c3 blocks; receipts differ only in `rev`/`commit` |
| `tripwire-selftest-core.txt` `2a0c1c…` | lesson cap. (81-82), SKILL 557 | 9/9, exit 0 | PASS — re-run 9/9 exit 0; `SELFTEST_SCRIPT_SHA256` `4ced68d…` = HEAD tool |
| `tripwire-selftest-compound.txt` `f899a6…` | same | 16/16, exit 0 | PASS — re-run 16/16 exit 0 |
| `tripwire-selftest-hardening.txt` `61a88b…` | same | 33/33, exit 0 | PASS — re-run 33/33 exit 0; includes `newline-second-line`, `heredoc-into-shell`, `eval-subprocess-list`, `multi-toolcall-line` |
| `tripwire-anchor-r15.txt` `dc3827…` | lesson cap. (82-83), M2 | exit 1; line 54 `call_38165`; host_mutation `sudo` + `pacman:-S`; 8 findings over 7 calls | PASS — re-scan of the live transcript byte-identical to receipt; 8 findings, 7 distinct `tool_call_id`s, line 54 has both rules; file sha `78388d42…`, 173 nonblank lines match |
| `tripwire-r13.txt` `81f063…` | lesson M2, cap. (84) | package_query 19; r13 GlobalCapture:19 wayland-utils | PASS — counts and finding rows match; host_mutation at 19 = sudo + pacman:-S |
| `tripwire-r14.txt` `033bdd…` | lesson M2 | package_query 46; ReviewSourceBar:41 `-Sw`; OutputSpec:65 `-S` | PASS — both install rows present, one call each |
| `tripwire-r15.txt` `fa186d…` | lesson M2 | package_query 177; LibinputEvents:54 libinput; ReviewDocsEra:50 `sudo -n true` | PASS — both rows present (ReviewDocsEra also carries `pacman -Qi hyprland`) |
| `tripwire-r16.txt` `496700…` | lesson M2 | package_query 2; CustomMan:24 second `pacman -Q waybar` | PASS — CustomExec:9 + CustomMan:24, exactly two |
| `tripwire-pacmanlog-join.txt` `ec4e1a…` | lesson M2 | 4/4; pacman.log 2410/2422/2423/2429 | PASS — log lines and UTC↔−0300 timestamps verified; 4 pacman host_mutation transactions in receipts, no fifth (see F2 for the disclosure parenthetical) |
| `tripwire-vs-oracles.json` `b94b14…` | lesson cap. (84-86) | every oracle non-clean row is also a tripwire finding; 21 tripwire-only | PASS — recomputed independently from `oracle-r13-r14.json`, `oracle-r15.json`, `oracle-r16.json`: unique non-clean sets 26/25/131/2 = comparison counts; oracle-only 0 in all rounds; tripwire-only 3+0+18+0 = 21, every tuple present in the round receipts |
| `tripwire-r17-w1.txt` `793bf4…` | lesson cap. (86-88) | 70 seat files, clean, 1 unparsed spawn, 1 unparsed eval cell | PASS — 70 `MadoR17.<Seat>.jsonl`, no `MadoR17.jsonl`; counts `{0,0,0}` exit 0; unparsed_spawns in SentinelTranscriptRead = 1; eval_unparsed in RevengeEvalBang = 1; see F5 for one digest drift |
| `session-index.json` `06c259…` | lesson cap. (88) | transcript digests | PASS — 228/228 recorded sha256 values match the live transcripts now; rounds MadoR13…MadoR16, `generated 2026-10-20` |
| `.ufo/waves/round-16/evidence/frozen-tampered.json` (round-16) | lesson M1 | measured `9dcf248`; exit 2 `frozen_error` | PASS — top-level `finding`/stdout `MADO_PLAN: frozen_error`, `measured_commit 9dcf248…`, exit 2, `matched_exit: true` only |
| `round-16.md:131-132` at `27cd06f` | lesson M1 | `2 snapshot_tampered` + `frozen-tampered.json` | PASS — lines 131-132 exact; erratum appended at HEAD with 0 removed lines |
| `action-selftest.json` / `action-selftest-final.json` (round-16) | lesson M1 parenthetical; round-16 erratum | got-side `snapshot_tampered` | PASS — both carry `frozen-tampered-plan/policy … got 2/snapshot_tampered`; measured `9dcf248` / `1e31681` respectively |
| `legacy-selftest.json` / `action-selftest-final.json` (round-16) | SCORECARD lines 832-833, 863-864 harm-watch numbers | 372/372 and 52/52 | PASS — `MADO_SELFTEST: 372/372 assertions passed`; `SELFTEST_SUMMARY: 52/52 passed` |
| `/var/log/pacman.log` | lesson M5; SCORECARD C3 pins | 13 runs 07:45-09:39; `-Syu` 09:15; mkinitcpio 41.1→42.2; kernel; hyprland 0.56.2-4; 0 lines after 10:51; 2429-2437 | PASS — 13 `[PACMAN] Running` in 2440-3152; versions exact; last line 09:39:21; 2429-2437 is the libinput transaction |

Evidence files present but not cited by the three docs (not defects):
`census-start.txt`, `schema-variants.json`, `measure-c1.json`,
`measure-c2.json`, `oracle-r13-r14.json`, `oracle-r15.json`,
`oracle-r16.json`. `measure-c3.json` is untracked and uncited.

## Claim re-derivations (SCORECARD round-17 declaration/corrections)

| claim | re-derivation | result |
|---|---|---|
| C1 calibration literal 14/22 = 6.3636 → ≥15/23 | `git show REV:corpus/QUALITY.md \| grep -cE '^[0-9]+\. .*lessons/'` over `'^[0-9]+\. '` at 27cd06f and 988b858; `measure.py` at both | 14/22 → 15/23; 6.3636 → 6.5217 |
| C2 rubric V 2/6 = 3.3333 → 4/6 | `measure.py 27cd06f`, `measure.py f52f43f`, `measure.py 988b858` | 2/6 P1,P2 → 4/6 P1,P2,P4,P6; legacy `covers: U2→P1`, `U1→P1`, `U7→P2` present; `u_routes 7` at all three |
| C3 absent at 27cd06f → present | `git cat-file -e 27cd06f:tools/mado-tripwire.py` (fails); HEAD blob sha | absent → `4ced68d…`, same as every selftest receipt |
| instrument binding `f52f43f` `a280b3ab…`, `ab0bc9b` `4023124f…` | `git show <rev>:…/measure.py \| sha256sum` | exact; `measure.py` absent at 0175f13 (fatal) |
| SOURCES rows 55 → 70; A 51→63, B 1, C 3→6; mined 43→55, queued 8, rejected 4→7 | parse 11-column rows at 27cd06f and 988b858 | exact; `git diff 27cd06f 988b858 -- corpus/SOURCES.md` = +15 lines, 0 removals ("no existing row changed" holds) |
| corrections append-only | `git diff 0175f13 988b858 -- SCORECARD.md` | 30 insertions, 0 deletions |
| erratum append-only | `git diff 27cd06f 988b858 -- corpus/lessons/round-16.md` | 0 removed lines |

## Attack log — what I tried and what failed

- **"A cited receipt is absent at HEAD."** Failed for all `evidence/`
  receipts; only the untracked wave-1 seat **reports** cited by M4/Gate are
  absent (F1).
- **"A sentence names a verdict token the receipt does not record."** Failed.
  Every attributed token is on the outcome side at the named revision; the
  one intentional red (`R16-V1-red`) is correctly reported as MISMATCH by
  the label check, and the superseded receipt keeps its true `frozen_error`
  (the erratum never relabels it).
- **"The instrument was not shown able to fail."** Failed as an attack: the
  suite is green *and* red where declared — 3 MISMATCH labels, 0 ok on the
  mutant claims, exit 1; the recut tamper fires `snapshot_tampered` while
  the control returns `frozen_match`.
- **"The anchor / join / oracle claims are receipt-only assertions."**
  Failed: the anchor re-scan is byte-identical; the join's four log lines
  and timestamps check out; independent reconstruction of the oracle sets
  from the three oracle JSONs gives 0 oracle-only rows in every round.
- **"SCORECARD numbers were transcribed, not re-derived."** Failed: all
  counts and both scores reproduce from committed bytes.
- **"QUALITY 23 was never tested on round 17 itself."** Partly succeeded:
  the M2 disclosure parenthetical (F2) and the label-check revision line
  (F3) are the two places where a sentence attached to a receipt does not
  survive its counterexample; neither is a token misattribution.

## Residual risk / verification gaps

- Wave-1 seat reports (`w1/reports/`, 70 files) and `w2/` are untracked. Any
  claim that rests on them (M4 H1-H3, Gate source-seat reports, M3
  "tightenings shown to bite") is unverifiable at `988b858`; I checked the
  worktree copies where they exist, but that is not committed evidence.
- M3's "Tightenings shown to bite" names no receipt. The four tightenings
  are implemented in the `ab0bc9b` instrument (docstring and code), and the
  baseline is unchanged under both instruments, but no committed receipt
  demonstrates each tightening rejecting an otherwise-passing entry. The
  claim is unbound, not false-on-evidence.
- `tripwire-vs-oracles.json`'s key comment says only `clean-data-mention`
  is excluded, while `oracle-r16.json` uses class `clean` for 74 token-as-
  data rows. The comparison's r16 result (2) matches the two real queries,
  so the *cited claim* holds, but the key's wording is imprecise for the
  r16 oracle.
- `SKILL.md:533` "every seat-disclosed breach" was checked against the
  disclosures I could locate in rounds 13-16 lessons: r13 install (found),
  r14 `-S`/`-Sw` (found), r15 libinput and `hyprctl version` (found), r16
  `pacman -Q` (found). The round-13 spot-check's own `pacman -Q wayland
  wayland-utils` disclosure belongs to an outside verifier whose transcript
  is not among the 33 scanned lane files; if "seat" includes outside
  verifiers, the universal is wider than the receipts cover.
- Working tree was dirty under concurrent edits throughout the audit. Early
  state: four tracked corpus files modified (`README.md`, `SOURCES.md`,
  `knowledge/terminal-route-r17.md`, `lessons/round-17.md`) plus untracked
  `w1/reports`, `w2`, `drafts`, `gen_w2.py`, `measure-c3.json`. Later
  `tools/mado-tripwire.py` (sha256 `4ced68d…` → `7a98720e…`), nine evidence
  receipts (`tripwire-anchor-r15.txt`, `tripwire-r1{3,4,5,6}.txt`,
  `tripwire-selftest-{core,compound,hardening}.txt`,
  `tripwire-vs-oracles.json`) and `tripwire/hardening/expected.json` were
  also modified/regenerated by another actor. All findings above are
  computed from `988b858` blobs, not the worktree. A spot-check of the
  regenerated bytes at report time preserves every count/token cited by the
  lesson — 9/9, 16/16, 33/33; anchor `{host_mutation: 2, live_probe: 1,
  package_query: 5}`, 8 findings, line 54 `call_38165` with `sudo` +
  `pacman:-S`; oracle comparison 26/25/131/2 agree, 0/3/18/0 — and only
  `SELFTEST_SCRIPT_SHA256` changed. The lesson/SKILL do not cite the tool
  sha, so this creates no doc-vs-receipt token mismatch; the final commit
  still needs its own receipt audit, and if the regeneration is kept, the
  lesson should name the old `4ced68d…`-era receipts as superseded rather
  than silently replacing them (QUALITY 23's supersede rule). The lesson's
  F2 correction and the S071 addition (O1) are also still uncommitted.

## Handoff checks for the main agent

1. Decide whether F1 is closed by committing `w1/reports/` or by citing a
   committed artifact; either way the lesson's M4 pointer should resolve at
   the next lane HEAD.
2. Confirm the F2 correction now in the worktree is committed with the
   round (and does not reintroduce the "only" claim).
3. If S071 is kept, re-derive and update the lesson Gate counts
   (rows 71, tier A 64, mined 56) and the new-rows table in the same commit.
4. Re-run after integration (single pass):
   `python3 -I .ufo/waves/round-17/label-check.py`;
   `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening}`;
   `python3 .ufo/waves/round-17/measure.py 988b858` (and the next HEAD).
