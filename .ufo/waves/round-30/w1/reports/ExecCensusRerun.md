# ExecCensusRerun — lane census rerun at round-30 tip

Seat: executor (RUNNER; no writes beyond this report). Date: 2026-10-24.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Script: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet repo, read-only use).
Comparison target: `.ufo/waves/round-30/evidence/census-end.txt`
(`sha256 0e661a957ad069839c825a67b56c2436edf8d20baeafab71fdd28b51b7a4d4e4`).

## Measured revision

Census measures `corpus/SOURCES.md`, whose blob is `842ff388d9b9ceeb871b5220187290e7645799e5`
at the data commit `446dc396`, at records tip `92d3c86`, and at the current tip
`d72243e` (a verifier spot-check lesson commit landed while this item ran: it adds only
`corpus/lessons/round-30-verifier-spotcheck.md`, 1 file, +109 lines; SOURCES unchanged).
Base blob at `8f51071b` and freeze `451e8b3c` is `d80441cf5c426cd1eec12d38446c9b5a7bd527c5`
(different, as expected: S185 is the only row delta). All measurements below are at the
lane tip's SOURCES bytes.

## 1. Maintained parser — `validate` (assigned command, verbatim)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
EXIT=0
```

7 W04 warnings (same id set as `census-before.txt`), no E-codes, exit 0.
No new W04 introduced by S185.

Cross-check, maintained `census` mode (same script):

```
mado	rows	185
mado	tier.A	178
mado	tier.B	1
mado	tier.C	6
mado	status.mined	166
mado	status.queued	10
mado	status.rejected	9
FLEET	rows	185
FLEET	tier.A	178 / tier.B 1 / tier.C 6 / tier.invalid 0
FLEET	status.queued 10 / status.mined 166 / status.rejected 9 / status.invalid 0
FLEET	missing	0
EXIT=0
```

Maintained `selftest`: `selftest ok`, 96 `killed …` assertion lines, EXIT=0.

## 2. Four frozen manual census commands (CORPUS.md §Census, verbatim; cwd = lane root)

| Block | Command (as frozen) | Output | Required |
|---|---|---|---|
| rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `185` | match census-end |
| malformed | `awk -F'\|' … NF!=13 …` | `0` | 0 |
| tier histogram | field `$5` | `A=178 B=1 C=6 ` | — |
| status histogram | field `$9` | `mined=166 queued=10 rejected=9 ` | — |
| duplicate ids | `$2 \| sort \| uniq -d` | *(empty)* | empty |
| enum violations | tier/status/kind/community-at-A | *(empty)* | empty |
| mined used-by existence | `$12`, `[ -e "$p" ]` | *(empty)* | empty |

All four requirement-bearing blocks (`rows`, `malformed=0`, `dup ids` empty, `mined
used-by missing` empty) match `census-end.txt` exactly. Histograms are not recorded in
`census-end.txt`; the values above are new measurements and they match the maintained
parser's `census` mode field-for-field (`A=178/B=1/C=6`, `mined=166/queued=10/rejected=9`).

## 3. S185 row verification

Raw row (worktree = tip blob = data blob), `corpus/SOURCES.md:197`:

```
| S185 | Frozen navigation counting command (own-work) — SCORECARD.md section "Fleet round 1 — coverage navigation", literal shell block | own-work | A | The index-completeness semantics this lane's coverage-navigation rubric uses | SCORECARD.md counting-command fence (sha256 of block: 8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88), opened 2026-10-24; prints `indexed=covered/N missing=… coverage=…/10` | Gives the exact row-set semantics an index-completeness gate must implement — every corpus/knowledge note must have exactly one index row in corpus/README.md | mined | 2026-10-24 | 180d | quality/check-index.py, .ufo/waves/round-30/registration.md |
```

| Check | Result |
|---|---|
| Field count NF=13 (11 columns) | **PASS** (`NF=13`) |
| id | `S185`, present exactly once (`grep -c` → 1) |
| kind | `own-work` (valid enum) |
| tier | `A` |
| status | `mined` |
| opened / recheck | `2026-10-24` / `180d` (valid: ISO past-or-present; symbolic-NN cadence) |
| used-by paths exist at tip | **PASS**: `quality/check-index.py` EXISTS, `.ufo/waves/round-30/registration.md` EXISTS |
| used-by paths exist at data commit `446dc396` | **PASS** (both `git cat-file -e`) |
| used-by paths cite S185 | **PASS**: `quality/check-index.py:8` ("S185"); `registration.md:26,38,67,83,101,102` |
| E12 (row outside `## Registry`) | no finding (validate exit 0) |

Base delta (frozen commands at `git show 8f51071b:corpus/SOURCES.md`): rows `184`,
malformed `0`, `A=177 B=1 C=6`, `mined=165 queued=10 rejected=9`, dup ids empty, enum
violations empty, S185 `ABSENT`. Net effect of the data commit: +1 tier-A, +1 `mined`
row, no status/recheck flips on existing rows, no new duplicates.

## 4. Comparison with `.ufo/waves/round-30/evidence/census-end.txt`

| Evidence line | census-end.txt | Rerun at tip | Verdict |
|---|---|---|---|
| `rows` | `185` | `185` | MATCH |
| `malformed` | `0` | `0` | MATCH |
| `dup ids` | *(empty)* | *(empty)* | MATCH |
| `mined used-by missing` | *(empty)* | *(empty)* | MATCH |
| validate body | 7×W04 + `mado ok …/corpus/SOURCES.md` | byte-identical 8 lines | MATCH (`diff` clean; only my appended `EXIT=0` is extra) |
| validate exit code | **not recorded** | `EXIT=0` | evidence gap (see below) |

`diff -u` of the evidence's 8 validate lines vs the rerun's 8 lines: identical; the only
difference is the `EXIT=0` line this rerun appends. `census-before.txt` records
`EXIT=0`, but `census-end.txt` omits an explicit exit-code line for `validate` — the
assigned "capture full output + exit code" is satisfied by this rerun (`EXIT=0`), not by
the stored receipt.

## 5. Observations / risks (non-blocking)

1. **`census-end.txt` omits the validate exit code.** Rows/malformed/dup/used-by checks
   are recorded, but the exit status is only implicit. Rerun establishes `EXIT=0`; a
   future receipt should print `EXIT=$?` for `validate` as `census-before.txt` does.
2. **S185 `used-by` shape vs SOURCES contract.** Contract §Shape defines `used-by` as
   "repo-relative paths of the knowledge entries or lessons citing the row". S185 lists
   `quality/check-index.py` (a gate script) and `.ufo/waves/round-30/registration.md` (a
   wave file), neither a `corpus/knowledge/` entry nor a `corpus/lessons/` file. The row
   is in fact cited by `corpus/lessons/round-30.md:18,24,33`, which is *not* listed.
   Both listed paths exist and textually cite S185, so no parser finding fires
   (`validate` E11 only checks existence; contract's `mined` predicate is "cited by ≥1
   path in used-by"), but the cell is contract-foreign in type and incomplete in the
   corpus sense. Flagged for the L1; not a kill-rule trigger for this item.
3. **Intervening commit `d72243e`** (verifier spot-check, `corpus/lessons/round-30-verifier-spotcheck.md`)
   landed mid-item. SOURCES blob unchanged (`842ff388` at `92d3c86`, `446dc396`, and
   `d72243e`), so every census number above holds at both tips. The spot-check lesson
   independently records the same S185 `used-by` existence result.
4. **W04 set stable.** Same 7 warnings at base and tip (S030/S042/S045/S097/S119/S120/S121);
   counts unchanged, so the data commit neither introduced nor cleared W04 under
   criterion 17's re-check.
5. **Histograms have no stored baseline in this round's evidence.** Only `census-end.txt`
   (rows/malformed/dup/used-by) exists; the two histogram values emitted here are the
   first recorded r30 figures. Maintained parser and frozen awk agree exactly, so the
   two independent implementations corroborate each other.

## 6. Scope, writes, tooling

- Writes: this report only
  (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-30/w1/reports/ExecCensusRerun.md`).
  No lane corpus byte, counter, gate, git/jj state, fleet-repo or sibling-lane file touched.
  At item close `git status --porcelain` also showed
  `M quality/q36-successor-receipts.txt`, which is *not* this seat's write — see §7.
- Tool installs/upgrades: none needed (bash/coreutils/gawk + maintained script already present).
- Verification run: census `validate` exit 0 and all four frozen blocks at tip; base blob
  re-measured from `git show` (read-only), never from the worktree, for the delta row.
- Blockers: none.

## 7. Live worktree observation (post-measurement, reported by `RevC1Fence`, verified here)

`git status --porcelain` at 04:06+ shows a dirty committed evidence file:

```
 M quality/q36-successor-receipts.txt      (mtime 2026-10-24 04:06:46, size 3105)
?? .ufo/waves/round-30/w1/
```

Verified shape (`git diff -U0`, `git show HEAD:…` vs worktree):

- 4 changed lines (`8f8e74a..d032704`), all four in the q36 successor-receipt record.
- The only token changes are ephemeral run-directory identifiers:
  `/tmp/mado-r28-q36-ge5zx30t` → `/tmp/mado-r28-q36-g3nfq53x`, and
  `/fast/scratch/hyaku/mado-r28/ExecQ36Runner/run.gR7SQoLa` →
  `…/run.Kv8n49Ha`. Every `rc=`, `expected=` and `PASS` token is unchanged: 8 verdict
  tokens at HEAD and 8 in the worktree; no verdict moved.
- Cause is consistent with an active q36 runner re-executing `check-control-receipts.py`
  and regenerating the receipt with its new run dir (the `ExecQ36Runner` scratch path).
  This seat did not run q36, did not write the file, and did not restore it — restoring a
  committed evidence file is a git-state mutation outside this runner's remit.
- No effect on this item: the census reads `corpus/SOURCES.md` (blob `842ff388`, unchanged)
  and never reads `quality/`; all §1–§4 numbers stand. The L1 should adjudicate the dirty
  worktree before any closure commit (either accept the regenerated receipt as a fresh
  run record or restore it; both are writer decisions, not this runner's).
