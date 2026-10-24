# ScribeRecords — round-30 record-consistency audit (pre-closure)

Seat: scribe (leaf). Write scope honoured: this report only. No lane byte, index, jj
state, judge, or fleet file was written; every git command was read-only.

Audit surface (committed bytes, not worktree):

| Record | Revision audited | Unchanged to master |
|---|---|---|
| `.ufo/waves/round-30/registration.md` | `451e8b3c` (sole commit touching it) | yes (`git diff 451e8b3c master` empty) |
| `SCORECARD.md` round-30 section | `92d3c86` (records commit) | yes (only later commit `d72243e` adds a lesson file) |
| `LOG.md` round-30 entry | `92d3c86` | yes |
| `corpus/lessons/round-30.md` | `446dc396` (data commit) | yes (`corpus/` blob-identical at `446dc396`, `92d3c86`, `master`) |

Lane master moved during the audit: `92d3c86` → `d72243e` ("round-30 verifier
spot-check (integrator, hyaku)", one path, `corpus/lessons/round-30-verifier-spotcheck.md`
+109). Ancestry, blob-identity and the harm-watch diff were re-checked at `d72243e`.
Frozen counters/gate are byte-identical from `451e8b3c` to `master`
(`git diff --stat 451e8b3c master -- registration.md c2/count.py quality/check-index.py`
empty).

## Verdict

Records are internally consistent on every registered metric (C1, C2, C3, controls,
census, harm watch). Five record-level defects are reported; **none moves a claim
verdict**, and all are repairable by append-only erratum, not by editing frozen or
data-time bytes. One out-of-scope worktree mutation was observed (item X1).

| # | Class | Where | Severity |
|---|---|---|---|
| D1 | receipt under-captures its own claim | `.ufo/waves/round-30/evidence/freeze-smoke-451e8b3c.txt:5-9` vs `LOG.md:1810-1811`, `corpus/QUALITY.md:355` (crit. 49) | defect |
| D2 | "verbatim" overclaim; active criterion text shrunk | `corpus/lessons/round-30.md:13`; `corpus/QUALITY.md:355-357` | defect |
| D3 | off-by-one attribution in frozen registration | `.ufo/waves/round-30/registration.md:61` | erratum |
| D4 | harm-watch revision label / tally without committed receipt | `SCORECARD.md:1924-1928`, `LOG.md:1818-1820` | imprecision |
| D5 | bare relative receipt path does not resolve at repo root | `SCORECARD.md:1915` (`controls/C2K1-donothing.txt`) | imprecision |
| D6 | "fence row-set semantics" wider than the fence (latent) | `quality/check-index.py:29` @ `451e8b3c` vs `SCORECARD.md:78` | claim-fidelity |
| X1 | unregistered worktree mutation of a committed evidence file | `quality/q36-successor-receipts.txt` | out of scope |

## Required checks — results

### 1. Every cited commit hash exists and is an ancestor of master — PASS

`git merge-base --is-ancestor <h> master` → success for `8f51071b5bc4…` (base),
`451e8b3c7ee3…` (freeze), `446dc3966193…` (data), `92d3c8676f48…` (records tip),
`d72243e1fec0…` (spot-check), `20022a652d20…` (cited by the round-30 README row's
`knowledge/workspace-rules-r27.md` frontmatter). The only other hex tokens in the four
records are the S185 block digest `8b59b503…` (verified, below) and `4cfdf858277ad362`,
which the note labels "seed", not a commit (`git cat-file -t` → not an object; correct
labelling).

### 2. Every receipt path exists at the named commit — PASS (with the convention named)

All cited paths exist at the records commit `92d3c86` and at `master`:
`evidence/c1-before-8f51071b.txt`, `evidence/c1-after-446dc396.txt`,
`evidence/c2-before-8f51071b.txt`, `evidence/c2-after-446dc396.txt`,
`evidence/c3-after-446dc396.txt`, `evidence/freeze-smoke-451e8b3c.txt`,
`evidence/census-before.txt`, `evidence/census-end.txt`, `controls/C2K1-donothing.txt`,
`controls/C3K1-base-red.txt`, `controls/C3K2-selftest.txt`. The `*-<rev>.txt` suffix
names the *measured* revision; each receipt's internal `revision=`/`rev=` matches its
filename (verified for C1/C2/C3 and freeze). None of the `*-after-*` receipts can exist
at the revision named in its filename (they postdate it); they are stored at `92d3c86`.
Freeze-time receipts do exist at the freeze commit `451e8b3c`:
`c1-before`, `c2-before`, `census-before`, `C2K1`, `C3K1`, `C3K2`.

`git ls-tree -r 446dc396 -- .ufo/waves/round-30/` contains **none** of the after
receipts, `freeze-smoke`, `census-end`, `w1-spec.json`, `w1-plan.json` — consistent with
them landing in the records commit (`git diff --name-status 446dc396 92d3c86`: 5
evidence files + 2 wave files + `LOG.md` + `SCORECARD.md`; no corpus path).

D5: `SCORECARD.md:1915` cites `controls/C2K1-donothing.txt` without the
`.ufo/waves/round-30/` prefix; no repo-root `controls/` exists, so the path resolves by
precedent only (same shape as round 29).

### 3. Literal vs resolved metrics reported side by side (criterion 22) — PASS

- `SCORECARD.md:1915`: "literal 28/40, resolved-active 31/39" → "literal 40/52,
  resolved-active 40/40 = 1.0000".
- `LOG.md:1799-1804`: same pair both sides, plus "literal and resolved metrics reported
  side by side per criterion 22".
- `corpus/lessons/round-30.md:50-52`: "literal 28/40 → 40/52, resolved-active 31/39 →
  40/40".
- Registration axis table + target line (`:61`) carry both fractions.
- Receipts match: `c2-before` `literal lines=28/40 fraction=0.7000`,
  `active=39 resolved_active=31 fraction=0.7949`; `c2-after` `literal lines=40/52
  fraction=0.7692`, `active=40 resolved_active=40 fraction=1.0000`.
- C1 and C3 report a single metric each; no literal/semantic pair exists to report.

Independent count from committed bytes: `corpus/QUALITY.md` at `8f51071b` has 40
criterion lines / 28 citing `lessons/`; at `446dc396` 52 / 40. Superseded set
`{1,2,3,4,5,18,19,20,32,38,39,40}` = 12, active 40, matching the receipt.

### 4. No claim text changed after data — PASS

- `corpus/README.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-30.md`
  are byte-identical at `446dc396`, `92d3c86` and `master` (blob shas compared).
- Data diff base→data is append-only: 0 deletions in all three corpus files.
- Registration: one commit (`451e8b3c`), byte-identical to master.
- After `92d3c86`, the only commit is `d72243e`, touching only a new non-author lesson.
- Caveat of interpretation: `SCORECARD.md`/`LOG.md` results text is necessarily added in
  the records commit; the *claim definitions* (predicates, targets, controls) live in the
  frozen registration and match the receipts. D2's "verbatim" wording is a data-time
  claim/evidence mismatch, not a post-data edit.

## Additional verified consistency

- Receipt values match every quoted number: C1 `41/43 missing=2` exit 1 → `43/43
  missing=0 dangling=0 duplicates=0` exit 0; C3 tip/base/selftest block; freeze smoke C1
  and C3 legs; `census-before` 184 rows exit 0, `census-end` 185 rows exit 0.
- Registry tallies `SCORECARD.md:1932`: A 177→178, mined 165→166, rows 184→185 —
  independently recounted from `corpus/SOURCES.md` at both revisions (`grep -c`).
  `SOURCES.md` diff base→data is exactly `+ S185` one line (no status/recheck flips),
  status `mined`, tier `A`.
- S185 block digest: sha256 of the fenced block content at `SCORECARD.md:70-89` is
  exactly `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`.
- Citation anchors spot-checked at `446dc396`: `M4` (round-14), `M1` (round-14), `M13`
  (round-21), `M28-1/2/3` (round-28), `M30-1/M30-2` (round-30) all present in their
  cited files.
- `README.md:53-54` rows quote the notes' own scope/source sets (S178–S182/S158/S162;
  S183) and `verified-at`/`recheck` pointers that exist; content matches the note bodies
  (schema, merge-in-place, on-created-empty; conditional-score/survivor/denominator
  limits).
- Harm watch `git diff --stat 8f51071b master -- tools/ corpus/knowledge/ SKILL.md
  PROVINCE.md` is empty (re-run at `d72243e`). Gate present at `451e8b3c`, absent at
  `8f51071b`; `quality/` diff base→master is the single new file (+219).
- The seven W04 ids in both census receipts match the lesson's list
  (`S030/S042/S045/S097/S119/S120/S121`), exit 0 both ends.

## Defects, with path:line

**D1 — the committed freeze-smoke receipt is a condensed excerpt, not the full output.**
`.ufo/waves/round-30/evidence/freeze-smoke-451e8b3c.txt:5-9` shows the C2 leg as 4
content lines (`UNRESOLVED criterion 39`, `40`, `LINE 20 superseded excluded`,
`PRED-C2-r30 verdict=TARGET_MISSED`) with no `counter=`, no `METRIC` tally lines, no
`EXIT=`, and 6 of 8 `UNRESOLVED` lines silently elided (no elision marker). The C2
counter's base output is 14 lines (`.ufo/waves/round-30/evidence/c2-before-8f51071b.txt`,
same corpus bytes). `LOG.md:1810-1811` states "all three counters run at the freeze
commit `451e8b3c` and print real tallies (`evidence/freeze-smoke-451e8b3c.txt`)"; the
cited receipt evidences no C2 tally, and the round adopts `corpus/QUALITY.md:355`
(criterion 49: "its full output is committed") as its basis. The full three-section
output does exist, but only in the uncommitted wave report
`.ufo/waves/round-30/w1/reports/ExecFreezeSmoke.md`. Verdict impact: none — the same C2
output is committed for the same bytes at `c2-before-8f51071b.txt` and
`controls/C2K1-donothing.txt`; the defect is receipt completeness.

**D2 — "verbatim" is false for rows 49–51, and three concrete evidence parentheticals
left the active text.** `corpus/lessons/round-30.md:13` says "Rows 41–51 supersede the
ungrounded criteria verbatim", repeated at `corpus/lessons/round-30-verifier-spotcheck.md:44`.
Byte diff of base→data criteria: rows 49/50/51 (`corpus/QUALITY.md:355-357`) delete,
respectively, the M28-1 pin pair "`count.py:100` … `3d7d301f…` vs committed
`635ae788…`" (`8f51071b:corpus/QUALITY.md:332`), the M28-2 receipt name
"`ReviewerSuiteMonotone.md`" (`:334`), and the M28-3 mutant pair "`ref-chk-no-anchor`
survived; `ref-chk-unreadable-exit-one` … killed" (`:336`). Rows 41–45 likewise add
substantive ground prose, so they are not verbatim either. Record survives (the
superseded lines remain in the append-only file; pin hashes and the receipt name remain
in `corpus/lessons/round-28.md:12-13`; the mutant id remains in
`.ufo/waves/round-28/c1/refpub/ref-chk.json:9`), but the active criteria lost their own
concrete pointers and the wording overstates the edit.

**D3 — registration off-by-one (frozen; route as erratum).**
`.ufo/waves/round-30/registration.md:61`: "12 lines superseded by rows 41–51". Rows
41–51 supply 11 `Supersedes criterion N` statements (1–5, 18, 19, 32, 38, 39, 40); the
twelfth line (20) is superseded by pre-existing row 21. `SCORECARD.md:1915` states the
superseded set correctly; only the registration parenthetical misattributes row 21's work.

**D4 — harm-watch revision label and an uncommitted tally.** `SCORECARD.md:1924` heads
the harm watch "at `446dc396`", yet the `MADO_SELFTEST: 460/460` and the
`git diff … master` were taken at the records tip (`92d3c86`, re-run `d72243e`), not at
the data commit. No committed receipt carries the 460/460 value; it is corroborated only
by the uncommitted wave report `.ufo/waves/round-30/w1/reports/ExecSelftest.md`. The
number is consistent with the registration's unchanged N/N base value and with
`ScoutAxisScores.md`, so no measurement is in doubt; the label and the missing receipt
are the defects.

**D5 — bare relative control path.** See check 2 above: `SCORECARD.md:1915`
`controls/C2K1-donothing.txt` resolves only under `.ufo/waves/round-30/`; no repo-root
`controls/` exists. Precedent-consistent with round 29, but not a valid repo-relative path.

**D6 — C3's "implements the frozen fence's row-set semantics" is wider than the fence
(latent, no effect on measured values).** Gate `quality/check-index.py:29` @ `451e8b3c`:
`ROW_RE = re.compile(r"^\|\s*`knowledge/([^`]+\.md)`", re.M)`. Fence `SCORECARD.md:78`:
`^\| `knowledge/([^`]+\.md)``. The gate's `\s*` is a strict superset (accepts zero
spaces, tabs, and a newline between pipe and backtick). This wording appears at
`LOG.md:1805-1806`, `registration.md:67-68`, `SCORECARD.md:1922`. No indented or
no-space row exists at `8f51071b` or `446dc396`, and the committed counts equal the
fence's output (`41/43`, `43/43`), so C1/C3's predicates are unaffected; the divergence
is unmeasured, not proven safe. Related, verified in the gate: member symlinks are refused
in `--root` mode (`load_root`, `:67`) but the `--selftest` symlink case (`:167-177`) only
exercises a dangling *knowledge-directory* symlink, so "symlink-refused" in the 6/6
receipt is evidenced for one shape only. Peer reports (uncommitted) claim additional
latent divergences (`--root` empty tree green vs `--rev` exit 2; space-bearing note names
via `split()`; non-ASCII git path quoting); those are **peer-observed only** — I verified
the `ROW_RE`, the `load_root` member-symlink refusal and the selftest cases myself.

**X1 — out-of-scope worktree mutation of a committed evidence file (report, do not
restore).** `quality/q36-successor-receipts.txt` is modified in the worktree
(`git status --porcelain` → ` M quality/q36-successor-receipts.txt`; mtime
2026-10-24 04:08:10), outside the wave's registered write scope. Diff: 4 lines changed,
only ephemeral run-dir paths (`/tmp/mado-r28-q36-ge5zx30t` → `…-g3nfq53x`, and
`/fast/scratch/…/run.gR7SQoLa` → `run.Kv8n49Ha`); all `rc=`, `expected=`, `PASS` fields
unchanged. No committed byte moved (the file is byte-identical at `446dc396`, `92d3c86`,
`master`). First reported by peer `RevC1Fence` at mtime 04:06:46; I confirmed the current
state independently. This is exactly the ephemeral-bytes class criterion 50 addresses,
and it invalidates a naive "worktree clean" reading of the harm watch taken after the wave
started.

## Commands run (read-only)

```
git log --oneline -12; git branch -avv; git rev-parse master
git merge-base --is-ancestor {8f51071b,451e8b3c,446dc396,92d3c86,d72243e,20022a65} master
git diff --stat 451e8b3c master -- .ufo/waves/round-30/registration.md .ufo/waves/round-30/c2/count.py quality/check-index.py
git diff --stat 451e8b3c 92d3c86 -- .ufo/waves/round-30/registration.md
git ls-tree -r --name-only {446dc396,92d3c86} -- .ufo/waves/round-30/
git diff --name-status 446dc396 92d3c86; git show --stat 446dc396
git show {92d3c86}:.ufo/waves/round-30/evidence/*.txt | head -n; wc -l
git show {8f51071b,446dc396}:corpus/QUALITY.md | grep -cE '^[0-9]+\. ' | grep -cE '^[0-9]+\. .*lessons/'
git show 446dc396:corpus/SOURCES.md | grep -cE '\| A \||\| mined \||^\| S[0-9]+'
git diff --stat 8f51071b master -- tools/ corpus/knowledge/ SKILL.md PROVINCE.md   # empty (also at d72243e)
git diff --stat 8f51071b d72243e -- tools/ corpus/knowledge/ SKILL.md PROVINCE.md  # empty
python3 - <<'PY'  # sha256 of the SCORECARD fenced block -> 8b59b503… MATCH
grep -cF 'indexed=$covered/$total' SCORECARD.md   # 0; 'revision=$rev' -> 0
git diff -- quality/q36-successor-receipts.txt; git status --porcelain=v1
```

No tool was installed or updated (no pacman, uv, npx, cargo, npm transaction was run).

## Affected / touched surfaces

Written: `.ufo/waves/round-30/w1/reports/ScribeRecords.md` (this file) only. Read-only:
the four audit records, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
`quality/check-index.py` @ `451e8b3c`, `.ufo/waves/round-30/{c2/count.py,controls/*,evidence/*}`,
`.ufo/waves/round-30/w1/reports/*` (peer reports, uncommitted), `corpus/lessons/round-28.md`,
`corpus/lessons/round-30-verifier-spotcheck.md`.

## Known limits

- No counter, fence, gate, census or selftest was re-executed (no re-derivation, no
  decoration). Metric values come from committed receipts and from direct inspection of
  committed data bytes (criterion counts, supersedes set, tier tallies, blob identity,
  digest re-computation).
- The "verbatim" byte comparison covers 18/19/32/38/39/40 → 46/47/48/49/50/51. Rows
  41–45 vs base 1–5 were read as text but not char-diffed; they are visibly additive, so
  the "verbatim" falsification does not depend on them.
- Peer wave reports (`ExecFreezeSmoke.md`, `ExecSelftest.md`, `ExecCensusRerun.md`,
  `ExecC1Rerun.md`, `MutC3Gate.md`, `RevC1Fence.md`) were uncommitted and still being
  written during the audit; where I rely on them I say so explicitly, and every
  code-level fact I report was re-read from committed bytes.
- Worktree state is dynamic (peers writing under `.ufo/waves/round-30/w1/`, plus X1). The
  committed record at `92d3c86`/`d72243e` is unaffected by that churn.
- I did not invoke the canonical Rust judge, any acceptance process, or any other runtime.
  Conflicts above are stated for that judge verbatim, not adjudicated.
