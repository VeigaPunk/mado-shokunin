# MeasureMutantsRerun — non-author re-run of the R17-V5 mutant receipts

Seat: `MadoR18.MeasureMutantsRerun`, wave 2 (FALSIFY), 2026-10-20. Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Read-only in the lane: no git/jj
write, no package/service/compositor/input command, no network fetch, no tool
install. The only lane byte written is this report.

## Artifact under test

Claim C1 / QUALITY 25 (R17-V5): six rubric-V tightenings each have a committed
mutant in which the loose instrument credits what the tight instrument rejects,
6/6 bite, `no_bite []`.

```
$ sha256sum .ufo/waves/round-18/measure-mutants.py
075815bd5bbcf80fbf00a80ac9400ff9ec82082562a6691c1f5cc290da601d73
$ git show 4c103b55:.ufo/waves/round-18/measure-mutants.py | sha256sum   → 075815bd…
$ git show abfbf35b…:.ufo/waves/round-18/measure-mutants.py  | sha256sum   → 075815bd…
$ git show f52f43f8:.ufo/waves/round-17/measure.py           | sha256sum   → a280b3ab…d3508e
$ git show d9a5a18e:.ufo/waves/round-17/measure.py           | sha256sum   → de4c422b…17cfcdc
```

Harness bytes, its `harness.sha256`, and both instrument pins agree at the
worktree, at the integration commit and at the receipts commit. The harness
re-asserts each instrument sha before every run (`run_instrument`) and aborts on
drift, so a mutated instrument cannot silently produce these numbers.

Naming note: the harness default output is the lane evidence file. A bare rerun
would rewrite that committed artifact (new `generated_at`, `started_at`,
`workdir`, commit ids). I used the documented `--out` option and wrote both
runs to `/tmp/mado-r18-w2/`; the lane evidence file was not touched
(worktree sha256 `58929eea…bb133e5` equals the blob at `abfbf35` and that blob
is byte-identical at `4c103b55`, blob id `d52050e8…`, so the receipts commit did
not re-cut this artifact either).

## Commands run and exit codes

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-18/measure-mutants.py \
  --out /tmp/mado-r18-w2/measure-mutants-rerun.json \
  --keep --workdir /tmp/mado-r18-w2/mutants
→ EXIT=0        (wall 2.04 s; 6 BITES, 6 expectations, no unexpected tight-only)
```

Repeated once from a clean workdir:

```
python3 -I .ufo/waves/round-18/measure-mutants.py \
  --out /tmp/mado-r18-w2/measure-mutants-rerun2.json \
  --keep --workdir /tmp/mado-r18-w2/run2
→ EXIT2=0       (wall 2.34 s; identical summary)
```

Run exit code is meaningful: `main` returns 0 only when
`bites == mutants`, `expectations_met == mutants` and
`unexpected_tight_only == []`; otherwise 1.

## Per-mutant comparison, committed @abfbf35 vs rerun

Values are (committed → rerun); `lo`/`ti` are `c2.count` from
`compare.loose_count` / `compare.tight_count`.

| id | tightening | diff_sha256 committed = rerun | lo c→r | ti c→r | bites c→r | expectation_met | verdict |
|---|---|---|---|---|---|---|---|
| M1 | exact surface line | `e9f712a5f88ca88f646eb961e96beb9ce847e542b0947dce994d433ae1af21b5` = | 4→4 | 3→3 | True→True | True | MATCH |
| M2 | legacy credit pinned to three paths | `cf76218f577ccf30a7ed40bd1e06e2e5ea1a642c0858ed01a26ba188cad19eb2` = | 4→4 | 4→4 | True→True | True (unanchored, see F2) | MATCH |
| M3 | upstream https docs/spec/code row naming the surface | `6a0fcaf898cb083e2a0f78c7b227331afaa7e70782bb4d60b41994fbd019a3e9` = | 5→5 | 4→4 | True→True | True | MATCH |
| M4 | three-line section floor | `1bf73ed9392de649ae9183a0c1354574d2eb83b6969b3b80f92c12ec218ba16c` = | 5→5 | 4→4 | True→True | True | MATCH |
| M5 | registry-only parse | `700d022a9b18fb322d95ae2b3fb8e389723f80100859549c5b3cd195f2a299b2` = | 5→5 | 4→4 | True→True | True | MATCH |
| M6 | duplicate ids fail | `d62bfcd81afb60154e28c67e885ba3a0ffd51714d6b79d73154a6b9b5dd6e474` = | 5→5 | None→None | True→True | True | MATCH |

`loose_only` / `tight_only` sets, `basis` strings, `tight_refused`, `diff` text,
mutant `exit` codes, mutant `stderr` and every parsed `c2` object (count, score,
`covered` path lists, `rejected` reason strings, `u_routes`, `c1`, `c3_present`)
are byte-identical between the committed record and both reruns. `tight_only`
is `{}` in all six, so the summary's `unexpected_tight_only: []` is measured, not
asserted.

Summary equality:

```
committed : mutants 6, bites 6, no_bite [], expectations_met 6, expected_but_unmet [], unexpected_tight_only [], baselines_agree true
rerun 1   : identical JSON
rerun 2   : identical JSON
```

Baseline (pre-mutant) runs in every fresh repo: loose and tight both exit 0,
both `count` 4, both cover exactly `P1, P2, P4, P6`, equal covered lists, and
`c1 = 6.5217` (15/23) — matching the scorecard's axis re-derivation. The
harness's `baseline_assert` is what would abort on drift; it did not fire.

## The one observed difference: stdout bytes, and its proof

Twelve recorded `stdout_sha256` values (mutant runs, both instruments) differ
from the committed record; M6/tight is the twelfth and is equal. The harness
stores `stdout_sha256` over the instrument's raw stdout. `measure.py` emits
`"rev": rev` and `"commit": rev_sha` (tight instrument lines 307-308; loose
instrument lines 263-264), and the harness passes the throwaway repo's commit
id, which cannot repeat across runs because `git commit` stamps the current
second. Reconstructing each committed stdout by swapping **only** those two
tokens in my rerun stdout reproduces the committed `stdout_sha256` exactly:

| mutant | side | committed stdout_sha256 | rerun stdout_sha256 | status |
|---|---|---|---|---|
| M1 | loose | `ec7f72b21c219a91c55938306043da7c8e2b767c773a5d80ca2d358828d20f8a` | `4468962d851d114a4ccf4a6502185cae83db74c0929f5834922a1638fbc1ebbd` | token-swap reproduces committed |
| M1 | tight | `4b180d0282052d6cb74f23efc0bed68dc622b2a0dd733ba92b1a8ef8aee5c6d5` | `2bc31d60c39da6f6d5bb4cd9ead2cd29403a4e69525a3d0af1b79b63432ba6b8` | token-swap reproduces committed |
| M2 | loose | `876fc2e1f05c60d509092f2271e21b09ed55f47de52bca0ac5a2f1449861fb8b` | `c1caf8ed8290c1c472b7beab64515fdde2b723aca257d60006744be7a4decee1` | token-swap reproduces committed |
| M2 | tight | `65cc65aea48f7277cbae92e3309d9e07e24a6852ba464b2e136d50df56f0be86` | `a93b8228dec35fa275455cff7942c15b1bc0b5105c44545368204391fd37fe5e` | token-swap reproduces committed |
| M3 | loose | `456ffdd3d23a032cd2583e4a4472d8ec9964a96e1613cb8ba879d40981f74fb0` | `60c6fc4cd95a26a30561ca48e8f214273dc896e64ffea41f193f3571a024ba7f` | token-swap reproduces committed |
| M3 | tight | `ae5183263e60da17051ecc898214ca884c0a24fc154889bd3527c6a3287f088a` | `c5230a8380e0f62d4d7882f2543c4d9137a0c925e90de7914896c321b5f8f385` | token-swap reproduces committed |
| M4 | loose | `d63003f803abb5e9b89a65d6a51aca336fb180f1ec933c34a85a01e738f0fd4f` | `15f32bb15796db98a96805f565abac8d7c0464df3be5621b2fdfe9aa4bbfada0` | token-swap reproduces committed |
| M4 | tight | `a071cbb1654d2cc69d457604144e17ab2ad4d65950f39f9f265cdbd48fe732f5` | `82f1a7ed75b6d5a95bad14c4dee51a797745a50b94581b792415dc4cec965d3c` | token-swap reproduces committed |
| M5 | loose | `60e22ec3fa04f37f313c3b04912d7b8d6ea512c9a8e04f91ec8fe00ca6725885` | `dc92b3f4e5560f8361e59e673304008604fe70f073885ae6b663443adae0ca02` | token-swap reproduces committed |
| M5 | tight | `329350b2f98b4e59fe94421987d98d7f879582ba9fc5beea7be6e8ca4ee94a4f` | `8a614ac390b03d76a37d2bf6f4a731a0086c8c16b4a2ab2c7959a1110ab30db5` | token-swap reproduces committed |
| M6 | loose | `60f8ecbc79155470f4672493810e23b12714068aff47d74b39d476b3641f8932` | `0dd87de98dbfb36a4af50c0739bbaf90f0742556bf20c3cc546c4a5374b8bec5` | token-swap reproduces committed |
| M6 | tight | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | equal (stdout empty; exit 2) |

Method: re-run each staged instrument at that repo's recorded mutant commit
(reproducing the rerun sha exactly, so the recorded value is a function of the
kept repo), then replace the rerun `rev`/`commit` token with the committed
mutant/baseline ids and hash. The swap reproduces the committed sha in 12/12
cases; M6/tight contains zero tokens because the tight instrument writes only
`duplicate SOURCES id S016` to stderr and nothing to stdout. No semantic byte
differed.

Commit ids differ as expected and are the only identity fields that do:
e.g. M1 committed baseline/mutant `452e92e1…`/`4efe919d…` vs rerun
`e77e6c12…`/`861802f0…`; M5 committed `a8f37842…`/`02be7a4c…` vs rerun
`070ad298…`/`8bb2cb9b…`. Diff digests are hash-committed over `git diff`
output, which carries blob ids and no commit ids, and they match.

## Independent corroboration from the committed run's own kept repos

The committed run used `--keep --workdir /tmp/mado-r18-mutants-run`, and that
tree still exists on this host. I did not rely on that path for the rerun, but
it lets the committed record be checked without trusting the harness:

```
for each Mx:  git -C /tmp/mado-r18-mutants-run/Mx/repo rev-parse HEAD
              git -C … rev-parse HEAD^
              git -C … diff --no-color HEAD^ HEAD | sha256sum
```

| mutant | HEAD == recorded mutant_commit | HEAD^ == recorded baseline_commit | diff sha == recorded |
|---|---|---|---|
| M1 | `4efe919d7f88…` ✓ | `452e92e1321a…` ✓ | ✓ |
| M2 | `134c648cb35d…` ✓ | `2a5d21cdbced…` ✓ | ✓ |
| M3 | `39f98005fdfb…` ✓ | `2a5d21cdbced…` ✓ | ✓ |
| M4 | `5adb297833fe…` ✓ | `2a5d21cdbced…` ✓ | ✓ |
| M5 | `02be7a4c4820…` ✓ | `a8f378424ea7…` ✓ | ✓ |
| M6 | `19f4bc4cb179…` ✓ | `a8f378424ea7…` ✓ | ✓ |

Running the staged instruments inside those repos at those commits reproduces
the recorded `mutant.*.c2` objects, exits and the whole `compare` result
(counts, bites, loose_only, tight_only) for all six mutants — the committed
numbers are recoverable from the committed run's own artifacts, not only from
my rerun.

## Negative control: the comparator can say "no"

Using the harness's own `compare()` on the kept rerun repos (same commit, same
instrument on both sides):

```
loose-vs-loose : bites False   loose_only {}   for M1..M6   (0/6)
tight-vs-tight : bites False   loose_only {}   for M1..M5
M6 tight-vs-tight: bites True, tight_refused True — degenerate: the tight
instrument refuses the duplicate-id tree on both sides; the refusal clause,
not a discriminating comparison.
```

So the 6/6 result is produced by an actual loose/tight difference, not by a
comparator that always reports a bite. Combined with the baseline asserts
(identical covered sets at the pre-mutant commit), the receipts are
non-vacuous at this level.

## Findings

**F1 — the claim survives.** Every quantity the assignment names — per-mutant
diff digest, loose count, tight count, bites — matches the committed record at
`abfbf35`, in two independent reruns, and is independently reconstructible from
the committed run's kept repositories. Exit code 0 (`0` also for the second
run). 6/6 bite, `no_bite []`, `tight_only {}` everywhere.

**F2 — `expectations_met: 6` is 5 anchored + 1 unanchored (cosmetic, does not
affect bites).** `expectation_met()` returns True unconditionally when a spec
has neither `reason_contains` nor `error_contains`; M2 has
`reason_contains: None` and no `error_contains`, so its True is by
construction. M1/M3/M4/M5 are anchored on tight rejection reasons
(`surface line must be exactly`, `naming the surface`, `under content floor`,
`token resolves to a mined tier-A`) and M6 on stderr
(`duplicate SOURCES id S016`). The committed JSON has no field distinguishing
anchored from unanchored, so a reader must read the harness source to learn
this. No mutant's bite depends on the field.

**F3 — M2's bite is entry-level only (as the lesson states).** Counts stay
4→4; the discriminator is `P1: loose-only [input-debugging-boundaries-r15.md]`,
i.e. one extra credited path in an already-covered province. The round-18
lesson M2 row says exactly "M2 at entry level"; the JSON's `basis` records the
loose-only path and no count delta. A reader who equated "bite" with a count
drop would misread M2; the recorded basis is not misleading.

**F4 — M6's `loose_only` spans five provinces from a single refusal.** Tight
exits 2 with no `c2`, so `covered_view` is empty and every loose entry is
"loose-only". `basis` states `tight refused (exit 2): duplicate SOURCES id
S016` last, and `tight_count` is `null`; the number five is not five
independent discriminations.

**F5 — the harness writes the lane evidence path by default (operational).**
A bare `python3 -I .ufo/waves/round-18/measure-mutants.py` rewrites the
committed artifact with new timestamps and commit ids. That is how the
committed file was produced under `--keep`; any future rerun intended as a
check should pass `--out` (and `--workdir` if it wants to keep repos).

## Limits

- Direct replay of the committed commit ids depends on
  `/tmp/mado-r18-mutants-run` surviving; it exists now (verified above). If
  `/tmp` is cleared, verification falls back to the rerun path, which still
  matches on all named quantities.
- The instrument-placement adaptation (`measure-loose.py`/`measure-tight.py`
  under `<tmp>/.ufo/waves/round-18/`) is inherited from the committed method.
  I did not re-derive it; I verified the staged files hash to `a280b3ab…` and
  `de4c422b…` (harness asserts this per run) and that the lane blobs at
  `f52f43f` and `d9a5a18` hash to the same pins.
- Environment matched the committed record exactly: Python 3.14.8,
  git 2.56.0, `Linux-7.2.11-arch1-1-x86_64-with-glibc2.44`.
- No claim here about the rubric instrument's real-world coverage beyond these
  six fixtures; this seat only replays R17-V5.

## Artifacts and side effects

- Lane write: this report only. Lane evidence file untouched (bytes
  `58929eea…`, identical to the blob at `abfbf35` and `4c103b55`).
- Rerun outputs retained at `/tmp/mado-r18-w2/measure-mutants-rerun.json`,
  `/tmp/mado-r18-w2/measure-mutants-rerun2.json`, repos under
  `/tmp/mado-r18-w2/mutants/` and `/tmp/mado-r18-w2/run2/`.
- No fetch, no install, no package/service/compositor/input command; only
  read-only git in the lane, plus commits inside the `/tmp` throwaway repos
  created by the harness itself.
