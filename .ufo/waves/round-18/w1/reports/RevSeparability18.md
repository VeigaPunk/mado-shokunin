# RevSeparability18 — causal separability attack on C1/C2/C3

Seat `MadoR18.RevSeparability18`, round 18 (hyaku phase 2), 2026-10-20.
Read-only review; no lane gate was run and no lane file was written. All lab
work is in `/tmp/r18sep` (ephemeral; results transcribed here). Baselines:
`d9a5a18` (bytes) and `d3a0000` (pre-registration). Two snapshots: (a) wave
worktree 12:47–12:52 UTC−03 (instrument `.ufo/waves/round-17/measure.py`
sha256 `de4c422b55c6…`, 11963 B; `tools/mado-tripwire.py` `c87a31ef…`, 1181 L;
`tools/mado-verify.sh` `c9fb0cef…`); (b) **integration commits `4c103b5`
(tree) and `abfbf35` (receipts)**, re-run at 13:0x and reported in §7. The
pre-integration sections are retained as the design analysis; §7 supersedes
their numbers where the two differ.

Labels: `[OBS]` observed command output, `[LAB]` observed on a `/tmp` clone or
fixture, `[INF]` inference from read bytes.

## 0. Axes

- **A1 causal separability** — does each claim survive removal of the other
  two claims' paths, with the instrument re-run?
- **A2 instrument honesty** — does `measure.py` read what the claim says, and
  does the claim's own runnable check exist and match its tool?
- **A3 coupling** — shared producers, shared oracles, shared acceptance steps
  between claims, or between a claim and a routed fix.

Kept moves: removal tests at baseline in a clone; frozen-mode isolation run
with `env -i` in an empty cwd; static review of every check script against the
claim text. Discarded moves: none (every candidate was cheap).

## 1. Verdict

**The instrument is separably partitioned; the claims are not yet, because
their non-instrumented acceptance layers cross.** `measure.py` reads three
disjoint file sets: c1 only `corpus/QUALITY.md`; c2 only `corpus/SOURCES.md`
plus `corpus/knowledge/*.md`; c3 only `tools/mado-tripwire.py` (presence and
sha). Removal tests confirm exact independence at that layer. The integrated
tree `4c103b5`/`abfbf35` reaches the declared targets (**c1 18/26 = 6.9231,
c2 6/6 = 10.0**), but two acceptance layers are still broken at that commit:
criterion 24's receipt checker cannot parse its own green receipts, and the
fetch bodies are not committed (§7).

| Lab commit | c1 | c2 | c3 tool | u_routes |
|---|---|---|---|---|
| **integrated `4c103b5`/`abfbf35`** `[OBS]` | **18/26 = 6.9231** | **6/6 = 10.0** | `c87a31ef…` | 7 |
| baseline `d3a0000` `[LAB]` | 15/23 = 6.5217 | 4/6 (P1,P2,P4,P6) | `962919ce…` | 7 |
| C1 only (actual `QualityDraft.md` text appended) `[LAB]` | **18/26 = 6.9231** | 4/6 = 6.6667 | `962919ce…` | 7 |
| C2 only (both real notes + real drafted rows, ids S072–S095) `[LAB]` | 15/23 = 6.5217 | **6/6 = 10.0** | `962919ce…` | 7 |
| theme note only `[LAB]` | 15/23 | 5/6 (P5) | `962919ce…` | 7 |
| walker note only `[LAB]` | 15/23 | 5/6 (P3) | `962919ce…` | 7 |
| C3 only (final tool + frozen snapshot, no repo in cwd) `[LAB]` | not read (no repo) | not read (no repo) | `c87a31ef…` (behavioral run) | n/a |

Three couplings are real and must be resolved before the closure sentence is
written (K1–K3 below); six more are integration hazards (K4–K9). Two claims
are **not instrumented at all**:

1. C3's claim is behavioral. `measure.py`'s `c3` field is presence+sha and was
   already true at `d9a5a18` (`962919ce…`). `c3` cannot score the capability;
   the frozen replay must be run and its exit map recorded.
2. C1's "runnable check shown able to fail" and C2's R17-V3 receipts are
   manual/probe layers. `measure.py` will happily count a criterion whose
   check does not exist, and a note whose rows have no receipt. The counter
   cannot detect either defect.

## 2. Path partition (exact)

| Claim | Instrument reads (only) | Claim evidence / check paths | Owner |
|---|---|---|---|
| C1 | `corpus/QUALITY.md` | `corpus/lessons/round-18.md` (citation target, not read); `corpus/lessons/round-17.md` erratum (optional); `.ufo/waves/round-18/{receipt-check.py,receipt-claims.json,receipt-fixtures/,measure-mutants.py,evidence/measure-mutants.json,pipe-rc-census.py,recut-receipts.sh,evidence/tripwire-*-recut.txt}` | seats draft; L1 applies `QUALITY.md`, lessons, commits receipts |
| C2 | `corpus/SOURCES.md` + `corpus/knowledge/*.md` | `corpus/knowledge/walker-route-r18.md`, `theme-route-r18.md`; `.ufo/waves/round-18/fetch/{NoteWalker,NoteTheme}/**` (10 MB, 323 files, all ≤1 MiB) and every other seat's cited receipts; `.ufo/waves/round-18/fetch-verify.py` | notes by seats; rows/ids/used-by by L1 |
| C3 | `tools/mado-tripwire.py` | `.ufo/waves/round-18/frozen/{expected.json,inputs/*.jsonl,provenance.json,README.md}` (integrated path; the contract text says `frozen-tripwire`, see F0; `expected_sha256` 4f3534ae…; 5 inputs, 8 findings, 3 known misses); `.ufo/waves/round-18/tripwire/frozen/` (17-case selftest); `.ufo/waves/round-18/frozen-provenance-check.py` (default root `HERE/frozen`, line 64); `SKILL.md` registry row | TwFrozen* + L1 (`SKILL.md`) |

Disjointness holds for the **counter's** inputs. The only shared objects are:

- `tools/mado-tripwire.py` — C3 writes it; C1's re-cut receipts and
  `receipt-claims.json` name it as the measured tool (revision-pinned, K1).
- `.ufo/waves/round-17/evidence/tripwire-*` — C3 derives `expected_findings`
  from these round-17 receipts; C1 marks the same files red
  (`MISSING_PROVENANCE`). Both consume the same count oracle (K7).

There is no file that both c1 and c2 read, and no file that c3's frozen run
reads outside its own DIR (proved at K3).

## 3. Exact removal tests

Preconditions: a clone (the lane is jj-colocated; clone writes only under
`/tmp`), the instrument sha must remain `de4c422b…` (assert), and **each
reverted tree must be committed in the clone** because `measure.py` reads
committed revisions only (`git show`/`ls-tree`), never the worktree. `FREEZE`
is the round-18 integration commit; run these after it exists.

```bash
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
T=$(mktemp -d /tmp/sep18.XXXXXX)
git clone -q --no-hardlinks "$LANE" "$T/repo"
cd "$T/repo"
git checkout -q "${FREEZE}"
git config user.name sep18; git config user.email sep18@local

# exact revert of named path prefixes to a revision (A -> delete, else restore)
sep_revert() {
  local keep="$1"; shift
  git diff --name-status --no-renames "$keep" HEAD -- "$@" |
  while IFS=$'\t' read -r st p; do
    case "$st" in
      A) git rm -q -f -- "$p" ;;
      *) git checkout -q "$keep" -- "$p" ;;
    esac
  done
}
measure() { python3 .ufo/waves/round-17/measure.py HEAD; }
```

The C1 instrument is the clone's copy; `measure.py` resolves `REPO` from
`__file__` (`parents[3]`). Do not run the lane copy against the clone.

### T-C1 — C1 survives removal of C2 and C3

```bash
git checkout -q "$FREEZE" -B t-c1
sep_revert d9a5a18 corpus/SOURCES.md corpus/knowledge \
  .ufo/waves/round-18/fetch tools/mado-tripwire.py \
  .ufo/waves/round-18/frozen .ufo/waves/round-18/tripwire \
  .ufo/waves/round-18/frozen-provenance-check.py SKILL.md
git add -A && git commit -q -m 'sep: revert C2+C3 paths'
measure   # expect c1={'criteria':26,'lesson_cited':18,'score':6.9231}
          #        c2.count=4, covered P1,P2,P4,P6, u_routes=7
          #        c3.sha256 = 962919ce… (reverted tool)
```

C1's own checks on the same reverted commit (all clone-runnable):

```bash
python3 .ufo/waves/round-18/measure-mutants.py --lane "$T/repo" --out "$T/mm.json"
# [LAB] rc 0; summary {"mutants":6,"bites":6,"no_bite":[],"expectations_met":6};
# instruments loose a280b3ab…, tight de4c422b… (only f52f43f + d9a5a18 blobs)
python3 .ufo/waves/round-18/pipe-rc-census.py --repo "$T/repo" HEAD
# [LAB] rc 1, 12 sites / 3 checked / 9 unchecked, VERDICT RED — see K2:
# this check cannot be the criterion-26 green; use the gate OM9 scenario.
python3 .ufo/waves/round-18/receipt-check.py \
  "$T/repo/.ufo/waves/round-18/receipt-claims.json"
# LANE = __file__.parents[3] (receipt-check.py:41), so the clone's copy reads the clone.
# [OBS] today: EXPECT_SUMMARY 9/15, rc 2 (six PENDING re-cut claims). At FREEZE
# with the six revs filled: 15/15, rc 0. The receipts and their measured_commits
# are historical blobs, so reverting the tool in the worktree does not break them.
```

Pass condition for T-C1: c1 exactly 18/26, c2 exactly 4/6, c3 exactly the
baseline tool sha, and every C1 check evaluating only revision-pinned inputs.

### T-C2 — C2 survives removal of C1 and C3

```bash
git checkout -q "$FREEZE" -B t-c2
sep_revert d9a5a18 corpus/QUALITY.md corpus/lessons/round-18.md \
  tools/mado-tripwire.py .ufo/waves/round-18/frozen \
  .ufo/waves/round-18/tripwire .ufo/waves/round-18/frozen-provenance-check.py SKILL.md
git add -A && git commit -q -m 'sep: revert C1+C3 paths'
measure   # expect c1 15/23=6.5217, c2.count=6, covered P1..P6, u_routes=7,
          # c3.sha256 962919ce…
python3 .ufo/waves/round-18/fetch-verify.py \
  --fetch-root "$T/repo/.ufo/waves/round-18/fetch" \
  --sources "$T/repo/corpus/SOURCES.md" \
  --rows <the https rows cited in the two note heads>
# [LAB] all 21 web rows of the landed drafts: receipted, rc 0.
```

Do **not** put host-file rows in that `--rows` list until K3 is fixed: the
walker host row (`/var/log/pacman.log`) is `UNRECEIPTED` [LAB]. The theme host
row is reported `receipted` only by a digest coincidence [LAB] and should not
be relied on.

Pass condition: c2 exactly 6/6 with `rejected` empty and `u_routes` still 7,
c1 exactly 15/23, and fetch-verify green on exactly the set the claim says is
credited (see K3).

### T-C3 — C3 survives removal of C1 and C2

```bash
git checkout -q "$FREEZE" -B t-c3
sep_revert d9a5a18 corpus/QUALITY.md corpus/lessons/round-18.md \
  corpus/SOURCES.md corpus/knowledge .ufo/waves/round-18/fetch
git add -A && git commit -q -m 'sep: revert C1+C2 paths'
measure   # [OBS at abfbf35] c1 15/23, c2 4/6, c3.tool_present true, c3.sha256=c87a31ef…
SNAP=.ufo/waves/round-18/frozen   # integrated path; the wave contract text says frozen-tripwire (F0)
[ -f "$SNAP/expected.json" ] || {
  echo "C3 path drift: the claim contract name has no expected.json; see F0"; exit 1; }
python3 -I tools/mado-tripwire.py --frozen "$SNAP"
# [OBS at abfbf35] rc 0, first line 'MADO_TRIPWIRE_FROZEN: frozen_match'
cp -a "$SNAP" "$T/tamper"
for f in "$T"/tamper/inputs/*.jsonl; do printf ' ' >> "$f"; done
python3 -I tools/mado-tripwire.py --frozen "$T/tamper"
# expect rc 2, first line 'MADO_TRIPWIRE_FROZEN: snapshot_tampered'
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen
# expect SELFTEST_SUMMARY 17/17
for s in core compound hardening w2-regressions; do
  python3 -I tools/mado-tripwire.py --selftest ".ufo/waves/round-17/tripwire/$s"
done  # expect 9/9, 16/16, 33/33, 30/30
```

Strongest form, already run `[LAB]` with the final tool `c87a31ef…` against a
copy of the landed snapshot: from an empty cwd with `env -i PATH=/usr/bin:/bin`,
`--frozen <copy>` returned rc 0 `frozen_match` (5/5 inputs ok). This proves the
frozen replay has **no repo dependency at all** — reverting C1/C2 cannot affect
it, and neither can a missing `corpus/` tree.

Pass condition: the frozen outcomes above, the five suite tallies, and the
measure fields unchanged except `c3.sha256` (which becomes `FREEZE`'s tool
sha, not `962919ce…`).

Strict variant: to remove *every* other claim's files (not only the paths the
counter reads), extend the `sep_revert` argument lists with the other claim's
evidence scripts (`fetch-verify.py` for C2; `receipt-check.py`,
`receipt-claims.json`, `receipt-fixtures/`, `measure-mutants.py`,
`evidence/measure-mutants.json`, `pipe-rc-census.py`, `recut-receipts.sh` and
the re-cut receipts for C1; `frozen-provenance-check.py` for C3). The measured
fields cannot move, because `measure.py` reads none of them; only the
non-instrumented check availability changes, and that is the point of the
strict variant.

## 4. Coupling register

### K1 [High, C1↔C3] Re-cut receipts name C3's file as their measured tool

`receipt-claims.json` binds `tool: tools/mado-tripwire.py` and verifies
`tool_sha256 == sha256(git show <measured_commit>:<tool>)`
(`receipt-check.py:41-…`). `recut-receipts.sh` refuses unless the *working
tree tool sha equals `git show REV:tools/mado-tripwire.py` (script :9-12,
:134-140), then stamps `tool_sha256` and `measured_commit=<REV>`.

Consequences:

- The green C1 evidence is not in place today: no
  `.ufo/waves/round-18/evidence/tripwire-*-recut.txt` exists, and
  `receipt-check.py` reports six `PENDING` claims, `EXPECT_SUMMARY: 9/15`,
  **rc 2** `[OBS]`. The check currently cannot exit 0, so criterion 24's
  "runnable check shown able to fail" has a red state but no green state yet.
- After C3's edit, the lane worktree tool is `c87a31ef…`; the re-cut must
  therefore run with `REV=<FREEZE>` and will stamp `c87a31ef…`, **not**
  `962919ce…`. If the round-18 lesson/report says "re-cut under 962919ce…",
  that sentence is false unless the run is made from a pristine `d9a5a18`
  worktree (e.g. `git archive d9a5a18`), which is the only way the script's
  equality guard can pass for a pre-C3 tool.
- Recommendation: run `recut-receipts.sh <FREEZE>` after the tool is final
  (sole writer TwFrozenMode is done per its report), commit the six receipts,
  fill the six `PENDING` revs with the receipts commit, and label the tool
  correctly — `962919ce…` (the tool whose receipts the snapshot expects) vs
  `c87a31ef…` (the tool that performed the re-cut). Criterion 24's own label
  rule demands exactly this.
- The receipt pin is revision-bound, not worktree-bound: reverting the tool in
  T-C1 does not invalidate correctly stamped receipts. Only re-running the
  script in a mismatched worktree would refuse.

### K2 [High, C1 internal × routed fix] Criterion 26's drafted check cannot go green

`QualityDraft.md:10` promises `checks/pipe-rc-lint.py tools/*.sh` "passes only
at `PIPE_RC_FLAGS: 0`" and lists lines 244, 942, 944, 1133, 1377, 1383, 2788,
3406, 3474. The landed check is `.ufo/waves/round-18/pipe-rc-census.py
[--repo DIR] REV`; at `d9a5a18` it prints `SITE … unchecked` for **640, 942,
944, 962, 1377, 2788, 3406, 3444, 3474** and `SUMMARY … unchecked=9` /
`VERDICT RED`, rc 1 `[OBS]` — four of the drafted line numbers are wrong and
the token `PIPE_RC_FLAGS` does not exist.

Worse, after GateRcFix's current bytes (`c9fb0cef…`) the *fixed* site at
`tools/mado-verify.sh:3477` is still classified `unchecked`: `_flags_at()` in
`pipe-rc-census.py:325-333` only scans for `set` **before** the substitution,
while the fix correctly puts `set -o pipefail;` inside the substitution body
(`blob=$(set -o pipefail; tmo git … | sha256sum | cut -d' ' -f1); grc=$?`).
`[LAB]` census on a clone with the fixed gate: 9 unchecked, rc 1, site 3477
still `unchecked`. Even if the census learned the in-body idiom, eight other
unchecked sites remain, so a whole-file green is unreachable this round.

Exact fix: criterion 26's runnable check should be the gate's OM9 scenario
(`STUB_GIT_SHOW_RC=128` → `omarchy.skill.vs_head UNKNOWN`, detail names path
and `rc=128`, no "local edit"; red-before in
`evidence/gate-rc-redbefore.txt`). The census stays as a *screen* whose output
is quoted with its 8 known residuals, or it is extended to accept the
in-substitution pipefail and the criterion is scoped to the one site. Do not
append the criterion with a green state that cannot be produced.

Method note: while re-deriving shas I reproduced F10's class by hand —
`$(git show rev:path) | sha256sum` strips the trailing newline (yielding
`6f82dafc…` instead of the true `de4c422b…`). Hash receipt bytes via
`git show … > file; sha256sum file`, never through a command substitution.

### K3 [High, C2 × R17-V3] The counter credits host-file rows that R17-V3 cannot receipt

`measure.py` lists every cited row that is mined/A/used-by in `ok_sources`, and
that list is the counter's "credited" set. The landed notes cite host-file
rows in their head `source:` line:

- theme note: `S0xx-pending-D` = host P5 theme state/consumers;
- walker note: `S0xx-pending` (18th token) = `/var/log/pacman.log`.

`[LAB]` after simulating L1's id assignment (theme S072–S075, walker
S076–S095): measure credits `[…S093,S094]` for P3 and `[S072..S075]` for P5.
`fetch-verify --rows S075,S094` prints `ROW S075 receipted` and
`ROW S094 UNRECEIPTED` (rc 1). S075 is a false positive: its anchor contains a
host `style.css` digest that happens to equal the fetched upstream
`omarchy-default/style.css` body (`fetch-verify.py:229` matches `sha in
anchor` before URL equality).

So "each new credited row has a committed raw fetch receipt" is not
satisfiable as written. Two clean fixes, recommended together:

1. Move host-file rows out of the head `source:` line; keep host bytes and
   their sha256 anchors in `## Host declaration` (the round-17
   `idle-lock-route-r17.md` head cites only web rows). Measure coverage is
   unchanged: the upstream rows in the same head already satisfy the
   surface-relevance gate (verified `[LAB]`: removing D/S094 leaves P5/P3
   covered).
2. In `fetch-verify`, require URL equality (`url`/`final_url` against the
   row's `source` cell) for a row to be `receipted`; use `sha in anchor` only
   as an integrity cross-check. This removes the S075 coincidence.

If L1 keeps host rows in the head, it must scope the closure sentence to
"every credited **web** row" and say how host rows are verified (file bytes +
sha256 in the note), otherwise the R17-V3 wording is false.

### K4 [Med, C2 × L1] The notes are placeholders until L1 substitutes IDs per occurrence

The walker head carries **19 identical `S0xx-pending` tokens in row order**
(draft rows 0–18; row 19, host file bytes, is not cited); the theme head uses
`S0xx-pending-A..D`. `S0xx` does not match `S\d{3}`, so both notes are
rejected by `measure.py` until substitution. A blanket string replace
collapses the walker citations to one id: measure still reports 6/6 (one valid
source suffices) but the note's provenance claim and the row→note join become
false. L1 must substitute per occurrence (walker: first 19 occurrences →
S076–S094 in order) and update `used-by` in the same change.

Also: rows must be inserted **inside `## Registry`** (currently ends at
`## Paths`, SOURCES.md:85). Appending at EOF lands in `## Leads` and
`measure.py` ignores them: `[LAB]` reproduced `count=4`, rejects "no head
`source:` S### token resolves…". A duplicate id makes `measure.py` exit 2
(no c2 output at all), not a lower count; the reserved S072–S099 range must
not be reused.

### K5 [Med, C1 × routed fix] Criteria 24–26 name files and tokens that do not exist

`QualityDraft.md` lines 4, 7, 10 name `.ufo/waves/round-18/checks/
receipt-check.py`, `checks/mutant-check.py RECEIPT.json`, `checks/
pipe-rc-fixture.sh`, `checks/pipe-rc-lint.py`. The landed files are
`.ufo/waves/round-18/{receipt-check.py,measure-mutants.py,pipe-rc-census.py}`
plus `evidence/measure-mutants.json`; there is no `checks/` directory and no
`mutant-check.py`. The drafted output tokens (`RECEIPT_SUMMARY`,
`PIPE_RC_FLAGS`, `guarded: UNKNOWN`) do not occur in the landed tools
(`EXPECT_SUMMARY`, `SUMMARY`, `MADO_TRIPWIRE_FROZEN`). The drafted semantics
also differ: `receipt-check.py` accepts one optional claims path (not
`RECEIPT...`), returns 2 for `PENDING`/`ERROR` rather than counting an
unreadable receipt as a failing one, and `measure-mutants.py` is a generator
whose JSON schema (`instruments.{loose,tight}.sha256`, per-mutant
`baseline_commit`/`mutant_commit`/`baseline`/`mutant`/`compare`/`bites`) does
not use `losoe_output`/`tight_output`/`measured_commit` keys.

This is the exact class of defect C1 is chartered to fix (reference-drift,
number-drift). Appending the criteria as drafted would make criteria 24–26
unrunnable at birth — a criterion-24 violation in the criterion itself. L1
must rewrite the three "Runnable check" sentences to the landed paths,
arguments, output tokens and JSON keys (or commit thin wrappers at the drafted
paths); a one-line `python3 -c` assertion over `measure-mutants.json` is an
acceptable check for 25 if its keys are named exactly.

### K6 [Med, C3 × C1] Frozen provenance has `tool_receipt_sha256` but no `measured_commit`

`frozen/provenance.json` records `tool_receipt_sha256:
962919ce…` and the source index, but neither `expected.json` nor the verdict
carries a `measured_commit`. The frozen verdict prints `tool_sha256` of the
*running* tool (`c87a31ef…`), not the pinned producer. Criterion 24 says a
receipt a sentence relies on carries tool sha256 **and** measured_commit, so a
round-18 report sentence that cites the frozen run as a receipt must either
(a) wrap it with `measured_commit` (harm-watch.sh prefixes receipts, but it
currently has no `--frozen` entry — grep finds zero "frozen" hits — so add one
or capture the frozen run separately),
or (b) state the commit in the sentence and label both tool shas (producer
`962919ce…`, runner `c87a31ef…`). The SKILL row's honesty line ("the pin binds
inputs, not the tool digest") must be kept; do not upgrade `frozen_match` to a
tool-identity claim.

### K7 [Low] C3's expected findings share the round-17 receipt oracle with C1's red receipts

`TwFrozenSnapshot` derives `expected_findings` (8 tuples, 3 known misses) from
`.ufo/waves/round-17/evidence/tripwire-*` cross-checked against the
oracles — the same six files criterion 24 marks `MISSING_PROVENANCE`. There is
no hard dependency (the snapshot does not read C1's round-18 re-cut
receipts), but both claims consume the same counts. Any classifier change
between the pinned production and the replay shifts both: TwFrozenMode's report
states scan parity and the four suites passing on `c87a31ef…` (`[OBS]`
9/9, 16/16, 33/33, 30/30), so the tuples still reproduce. L1 must not re-pin
`expected_findings` from the round-18 re-cut receipts if the re-cut tool differs
in classifier; re-cut counts are evidence that nothing shifted, not a new
oracle.

### K8 [Low] `surface:` lines outside the first 15 lines are invisible

`measure.py:185` slices `head = text.splitlines()[:15]`. `[LAB]`: a second
`surface: P6` inserted at line ~20 left the theme note credited 6/6 with no
reject; a second `surface:` inside the head was rejected ("an entry may
declare exactly one surface"). The "one surface per entry" rule is therefore
head-only. This is not a C1/C2/C3 coupling, but it is a residual gaming avenue
for a future invented-row claim; the notes must keep exactly one `surface:`
line anywhere, and the closure should say the instrument checks the head only.

### K9 [Low, C2 evidence hygiene] Fetch join and body cap

`fetch-verify.py` verifies bytes/sha of every receipt body (301/301 ok at the
last run; the corpus grew from 296 to 301 during the review), but its row join accepts `sha in anchor` (line 229), which produced
the S075 false positive; and it enforces no 1 MiB body cap although
`LessonDraft` M4 says "at most 1 MiB". Current bodies: 10 MB / 323 files, none
>1 MiB. Fetch bodies are untracked and must be committed; `.gitignore` only
adds `.ufo/state/`, so they are not ignored.

## 5. Findings on the landed drafts (severity ordered)

**F0 (Med) — C3 path: the integrated registry/artifact say `frozen/`, the wave contract text says `frozen-tripwire/`.**
The integrated tree `4c103b5` commits the snapshot at
`.ufo/waves/round-18/frozen/`, the SKILL row `mado-tripwire-frozen` runs
`--frozen .ufo/waves/round-18/frozen`, `frozen-provenance-check.py:64`
defaults to `HERE/frozen`, and the README names `frozen`. `expected.json`
sha256 `4f3534ae…` is byte-identical to the pre-rename copy my lab ran.
But the wave contract text and TwFrozenMode/TwFrozenSnapshot reports say
`frozen-tripwire`. A closure that runs the contract's literal path gets
`MADO_TRIPWIRE_FROZEN: frozen_error` rc 2 ("expected.json unreadable"),
which reads as a tamper-class failure. Fix: since the registry, artifact,
README and tool default all agree on `frozen`, keep `frozen` and correct the
contract/report pointer in the closure sentence (do not rename code at this
stage); alternatively rename the dir back and change `DEFAULT_ROOT`, the
SKILL row and README together. My lab numbers transfer because the pinned
bytes are identical.

1. **F1 (High)** Criterion 26's check is incompatible with the landed census
   and with GateRcFix's correct fix (K2). The criterion cannot be shown green;
   its line list is wrong; the fix's site is still flagged. Rewrite the check
   to the gate OM9 scenario or scope it to the fixed site and fix
   `_flags_at` to see in-substitution pipefail.
2. **F2 (High)** Criteria 24–26 name non-existent paths/scripts and wrong
   output tokens; criterion 25's receipt schema does not match the landed
   JSON (K5). Fix before append.
3. **F3 (High)** No round-18 re-cut receipts exist; `receipt-check.py` exits 2
   with six `PENDING` claims (K1). Criterion 24's green state is not yet
   available; `receipt-claims.json`'s `PENDING-L1` placeholders are honest but
   must be filled and the receipts committed.
4. **F4 (Med)** `LessonDraft` M2 cites instrument sha `4023124f…` (the
   `ab0bc9b` intermediate) while the operative tight instrument at `d9a5a18`
   is `de4c422b…` (`measure-before.json`; MeasureMutants `TIGHT_SHA`);
   criterion 25 must use `a280b3ab…` (loose) and `de4c422b…` (tight).
   Separately, `27cd06f:.ufo/waves/round-17/measure.py` does not exist (git rc
   128) and `f52f43f` is not its ancestor, so the round-17 table's "before"
   was measured with a worktree instrument, not a committed one `[INF]`; the
   round-18 report must name an instrument sha **and** a revision that
   contains it (`de4c422b…` at `d3a0000`).
5. **F5 (Med)** C2 placeholder/registry hazards (K4): 19 identical walker
   tokens; two placeholder schemes; registry-only parse; duplicate id exits 2.
6. **F6 (Med)** Host-file rows in note heads vs R17-V3 receipts (K3); the
   theme host row is "receipted" only by a sha coincidence.
7. **F7 (Low)** Frozen provenance lacks `measured_commit` (K6); label the two
   tool shas in the report sentence.
8. **F8 (Low)** `surface:` outside the head is invisible (K8); `fetch-verify`
   has no 1 MiB cap (K9).

## 6. Residual risk and verification gaps

- **Final bytes may differ.** I pinned lab work to tool `c87a31ef…` and gate
  `c9fb0cef…`; both moved during the review (`593b3aaf…→c87a31ef…`,
  `ab956c0…→c9fb0cef…`). L1 must re-run the five tripwire suites, the frozen
  replay, `--frozen` tamper matrix, `measure-mutants.py`, `pipe-rc-census.py`
  and `receipt-check.py` at `FREEZE` and record the final shas. Any later edit
  of `tools/mado-tripwire.py` after the re-cut invalidates nothing (receipts
  are revision-pinned) but does change the `c3` field; do not compare it to
  the re-cut tool sha without the label rule.
- **I did not read the source transcripts** (not named in my item) and did not
  run `frozen-provenance-check.py` or `recut-receipts.sh` (both read those
  transcripts). They are L1/verifier steps. The frozen snapshot's own
  provenance claims 5 inputs with source sha256 values matching
  `session-index.json` and one documented skip (`MadoR14.OutputSpec.jsonl:65`,
  792,861 B > 256 KiB; compensating source named); this must be re-checked by
  the seat allowed to read the transcripts.
- **I did not run lane gates** (`mado-verify.sh --selftest`, action-plan,
  navigation, census). Harm watch: the gate bytes moved (OM9/OM10 add 17
  `st_*` assertions), so the hermetic count is not 372 and must be re-cut
  (`evidence/regression-recut.txt` exists but is a GateRcFix artifact, not the
  final harm-watch run). `harm-watch.sh` has no `--frozen` command (zero
  "frozen" hits), so the C3 behavioral receipt must be captured separately
  with a `measured_commit` prefix, and the C3 path in that receipt must match
  F0's resolution.
- **Lab vs integration.** My C1/C2 numbers use the real drafted criterion text,
  the real note bodies and the real row drafts, but with simulated ids
  (S072–S095). They prove the instrument's behavior and the coupling shapes;
  they are not L1's final ids and must be repeated at `FREEZE`.
- **No counter can verify criterion honesty.** `measure.py` counts lines and
  files; it cannot see that criterion 24's check path is dead, that criterion
  26's green is unreachable, or that a credited row has no receipt. That is
  what F1–F3 are, and why the removal tests above include the checks, not only
  the counts.

## 7. Post-integration re-run (`4c103b5` tree / `abfbf35` receipts, and the live worktree)

The integration commits landed while this review was running. Everything above
that used a simulated tree is re-run here on the integrated bytes; where the
live worktree differs from the commits, both are stated. Clone at `abfbf35`,
instrument `de4c422b…`.

### 7.1 Integrated commit: targets met, separability exact

| Test (clone at `abfbf35`) | c1 | c2 | c3 tool | u_routes |
|---|---|---|---|---|
| integrated, no revert `[OBS]` | **18/26 = 6.9231** | **6/6 = 10.0** (P1..P6, 0 rejected) | `c87a31ef…` | 7 |
| T-C1: revert C2+C3 `[OBS]` | **18/26 = 6.9231** | 4/6 (P1,P2,P4,P6) | `962919ce…` | 7 |
| T-C2: revert C1+C3 `[OBS]` | 15/23 = 6.5217 | **6/6 = 10.0** | `962919ce…` | 7 |
| T-C3: revert C1+C2 `[OBS]` | 15/23 | 4/6 (P1,P2,P4,P6) | `c87a31ef…` | 7 |

T-C3 behavioural run at the same commit: `--frozen .ufo/waves/round-18/frozen`
rc 0 `frozen_match`; a one-byte append to any input rc 2 `snapshot_tampered`;
frozen selftest 17/17; round-17 suites 9/9, 16/16, 33/33, 30/30; the isolated
empty-cwd run (§3) still proves no repo dependency. **The instrumented layer is
causally separable on the integrated commit and both declared targets are met
by the counter.** The receipt layer, however, is not satisfied by the commit.

### 7.2 What the integrated commit does not satisfy

1. **Criterion 24's green is impossible at `abfbf35`.** The committed
   `receipt-check.py` parses `tool_sha256`/`measured_commit` only as whole
   lines (`^\s*tool_sha256…$`, line 47), while the receipts' actual header is
   `RECEIPT tool=… tool_sha256=… measured_commit=… utc=… cmd=…`. The committed
   claims also still carry six `PENDING-L1` revs and stale `*-recut.txt` paths.
   As committed: `EXPECT_SUMMARY: 9/15`, rc 2. With only the paths and revs
   fixed (`rev=abfbf35`): six `MISSING_PROVENANCE`, rc 1. With those plus an
   unanchored parser (lab patch): **15/15, rc 0** `[LAB]`. Both edits are
   required; neither is in `abfbf35`.
2. **Fetch bodies are not committed.** `git ls-tree -r abfbf35 --
   .ufo/waves/round-18/fetch` lists **21 files**, all `receipts.jsonl`; the
   lane worktree has 326 untracked bodies (332 `git status` lines including
   quote files). A fresh clone's `fetch-verify` prints
   `receipts=301 ok=0 bad=301`, every row `UNRECEIPTED`; the lane worktree
   prints `receipts=389 ok=389`, rows 24 `unreceipted=0`. R17-V3's "committed
   raw fetch receipt (body bytes, sha256, byte count, fetch time)" is therefore
   false at the commit: no body digest can be checked from committed bytes.
3. **The live worktree moved after the commit.** At 13:04 UTC−03,
   `receipt-check.py` sha `a2c05fe1…` and `receipt-claims.json` sha
   `175e74cd…` run **21/21 rc 0** `[OBS]`; `fetch-verify.py` sha `07e7ac74…`
   runs `receipts=389 ok=389`, all 24 rows receipted or `host/no-url`
   `[OBS]`. All three are uncommitted (`M`), and the 326 bodies are still
   untracked.
4. **The live `tools/mado-tripwire.py` is mid-rewrite and regresses the frozen
   selftest.** Shas observed within minutes: `c87a31ef…` (integrated; 17/17
   frozen and matching the receipts/snapshot), `f5a4a3c1…`, `3320ed07…`,
   `93622ccd…` (13:04:14). On the `3320ed07…` snapshot (tool and suite copied
   together) the frozen selftest is **11/17**; failures: `verdict-missing-
   finding`, `verdict-extra-finding`, `known-miss-violated`,
   `path-traversal`, `absolute-input`, `verdict-exit-label` (the new harness
   returns an extra tuple element; the path cases now read `frozen_error`
   instead of `snapshot_tampered`). The real snapshot still replays
   `frozen_match`, but do not commit the worktree tool until all five suites
   are green again; if the classifier changed, re-pin `expected.json` and
   `known_misses` and re-run the re-cut before quoting the old counts.

### 7.3 Status of every finding at the integrated/live snapshot

| Finding | Status | Evidence |
|---|---|---|
| F0 path `frozen` vs `frozen-tripwire` | open (Med) | registry/artifact/README/default all `frozen`; wave contract text and TwFrozen* reports say `frozen-tripwire`; the contract path returns `frozen_error` rc 2 |
| F1 criterion 26 check | **resolved in `4c103b5`** | QUALITY 26 uses the OM9/OM10 behavioural bite and labels the census "screen only"; its "nine at `d9a5a18`" matches the census. Residual: the census still lists the fixed site `:3477` unchecked (in-body pipefail not modelled), so the screen over-reports; no longer a blocker |
| F2 criteria paths/tokens | **resolved in `4c103b5`** | criteria 24–26 cite `receipt-check.py`, `measure-mutants.py`, `mado-verify.sh` OM9/OM10; the draft drift is historical |
| F3 criterion 24 green | **open at `abfbf35`; fixed in worktree, uncommitted** | committed 9/15 rc 2 → paths+revs only 6 `MISSING_PROVENANCE` rc 1 → parser patch + paths+revs 15/15 rc 0; live worktree 21/21 rc 0 |
| F4 lesson sha drift | **resolved in `4c103b5`** | lesson M2 uses `a280b3ab…`/`de4c422b…`; the draft's `4023124f…` is historical |
| F5 placeholders/registry | **resolved in `4c103b5`** | walker S072–S091 and theme S092–S095 substituted in notes and rows; measure 6/6, no rejects |
| F6 host rows vs R17-V3 | open in wording; resolved in the live tool | counter credits S090/S091 (P3) and S095 (P5); live `fetch-verify` classifies them `host/no-url` and does not count them unreceipted. The pre-registration says "every new credited row"; lesson M6 says "every credited **web** row" — the closure must use the lesson wording |
| F7 provenance `measured_commit` | resolved for citation | `evidence/tripwire-frozen-match.txt` line 1 has `tool_sha256=c87a31ef…` + `measured_commit=4c103b5…`; `provenance.json` itself still lacks it |
| F8 `surface:` head-only | open residual | unchanged |
| **F9 fetch bodies uncommitted** | **open (High)** | 21 committed files vs 326 untracked bodies; clone `fetch-verify` 0/301, lane 389/389 |
| **F10 live tool mid-rewrite** | **open (High, moving)** | four shas in minutes; `3320ed07…` frozen selftest 11/17; integrated `c87a31ef…` 17/17 |

### 7.4 Closure-blocking list (in order)

1. Freeze `tools/mado-tripwire.py`; run the five suites and the frozen replay;
   fix any failure before commit and record the final sha. If the classifier
   changed, re-run `recut-receipts.sh` at the new revision, re-pin
   `frozen/expected.json` + `known_misses`, and re-run `measure-mutants.py`
   (the six tightenings are instrument-level, not classifier-level, so they
   should still bite — verify).
2. Commit the live `receipt-check.py`, `receipt-claims.json`,
   `fetch-verify.py` (all `M`) and **`git add .ufo/waves/round-18/fetch`**
   (326 bodies, 10 MB). Then in a fresh clone: `receipt-check.py` 21/21 rc 0;
   `fetch-verify.py --rows <web ids>` 0 unreceipted; `measure` unchanged.
3. Re-run the three removal tests on the committed tree (§3 script) and record:
   T-C1 c1 18/26, c2 4/6, c3 `962919ce…`; T-C2 c1 15/23, c2 6/6, c3
   `962919ce…`; T-C3 c1 15/23, c2 4/6, final tool + `frozen_match` + tamper 2
   + suites 9/16/33/30/17.
4. Fix the path sentence: use `.ufo/waves/round-18/frozen` in the closure
   report (or rename the dir and the four references together); do not leave
   `frozen-tripwire` in the claim pointer while the artifact is `frozen`.
5. Scope the R17-V3 sentence to "every credited **web** row"; host rows are
   `host/no-url` and are verified by the note's sha256 anchors, not fetch
   receipts.

### 7.5 What I did not run

- The lane gate `tools/mado-verify.sh --selftest` (a gate; L1 only). The
  integrated `evidence/gate-selftest.txt` and `harm-gate-selftest.txt` exist;
  re-cut after the live tool settles.
- `frozen-provenance-check.py` and `recut-receipts.sh` in the lane: both read
  the restricted transcripts, which my item does not name; L1/verifier must
  run them.
- The live tool against lane inputs; all tool runs above used `/tmp` copies of
  the bytes, never the lane files in place.
