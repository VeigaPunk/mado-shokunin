# R56CritChronology — round 56 wave w1 chronology attack

Seat: R56CritChronology (critic, leaf, no subagents). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Verdict on the claim "the freeze was committed before this wave": **supported by committed objects and filesystem birth times, with three defects in the checker and contract text** (below). Nothing in the freeze was edited after launch on this lane (checked). The hold-out is **not** sealed in the way the contract describes: its path is named in the frozen contract, in the wave dispatch sent to a seat, and a prior round's hold-out is committed in-repo.

## 1. Timeline (all from committed objects, reflog, filesystem)

| event | time (-03:00 unless noted) | source |
|---|---|---|
| base 13f0acbe (protocol-shokunin, "round-55 verifier spot-check") | committer 20:59:32 | `git log`, reflog |
| freeze files born on disk | frozen-tables.json 21:14:50; freeze-verify.py 21:18:15; registration.md 21:17:03; claims-frozen.md 21:18:52; receipts/witness.txt 21:19:11 | `stat -c %w` |
| **freeze commit 3423ae285676** (parent 13f0acbe) | committer 21:19:17 (= 00:19:17Z); reflog master 21:19:17 | `git log`, reflog |
| registry `swarm-registry.json` born; its `createdAt` | birth 21:22:47.635; createdAt 2026-10-29T00:22:47.615Z (= 21:22:47.615) | `stat`, `git show 2aa347b:…/swarm-registry.json` |
| wave commit 2aa347b (mado-shokunin) | author = committer 21:22:53; reflog 21:22:54 | `git log`, reflog |
| first seat artifact born (R56ScribeEntryC) | 21:23:56 | `stat -c %w` |
| w1.ready (untracked, not in any commit) | mtime 21:23:05 | `stat` |
| w1.ready.dispatched (untracked) | content and mtime 2026-10-28T21:27:02 | `cat`, `stat` |

Margins: freeze commit precedes registry createdAt by 3 min 30 s, the wave commit by 3 min 36 s, the first seat artifact by 4 min 39 s, and the recorded dispatch by 7 min 45 s.

`git -C … log -3 --format='%H %an %cI %s' master`:
```
2aa347b1175cded6628465acf335f9232183d40c mado-shokunin 2026-10-28T21:22:53-03:00 round-56: wave 1 spec, dispatch, registry
3423ae285676c2a10273000f4519163472b443db mado-shokunin 2026-10-28T21:19:17-03:00 round-56: freeze claims, registration, frozen tables, fixtures, controls, pins, baselines
13f0acbe3a15da2d9c08357a576d91dcadc85273 protocol-shokunin 2026-10-28T20:59:32-03:00 round-55 verifier spot-check (integrator, hyaku): non-author admit/reject
```
Freeze commit parent is 13f0acbe. Freeze commit has no gpgsig, no tag, and the repo has only `origin` (github, not consulted; no remote evidence was read).

## 2. Checks requested

- **No round-56 `.ready` at the freeze commit.** `git ls-tree -r 3423ae… --name-only | grep -E '\.ready'` returns matches only for rounds 39–55 (rc 0 because of those). Restricted to round 56: **zero matches** at the freeze commit, and zero round-56 `.ready` paths in any commit (`git log --all -- '.ufo/waves/round-56/*.ready*'` empty). See defect D4: the literal command as written does not test round 56.
- **frozen-tables.json sha256 at freeze** = `d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af` — **match**.
- **fixtures/c2 commitment recomputed at freeze** (script `commit_c2.py`, reads `git ls-tree -r -z` and `git cat-file blob` only; sorted relpath, `<relpath>\0<f|l>\0<sha256>\n`, 119 entries: 116 regular, 3 symlinks mode 120000): `a9f552511cc4939e3c83190e7ca55a09d5f01dd520c59b3a6feeba2e0c4647d6` — **match** with `c2.fixture_commit_sha256` in the committed tables (`committed_count` 18). Same value at the wave tip 2aa347b (no change to fixtures).
- **Freeze paths unchanged between freeze and tip**: `git diff --stat 3423ae 2aa347b -- <claims, registration, tables, fixtures, ctl, fetch, receipts, freeze-verify.py>` empty. `git status --porcelain -- .ufo/waves/round-56` shows only untracked entries; no tracked round-56 file modified in the working tree. Working-tree and tip sha256 equal for w1-spec.json and w1-dispatch.json.
- **Freeze-order checker** (`quality/check-freeze-order.py`, read in full; run with `env -i`, `--work` scratch):
  - `--rev master`: `MADO_FREEZE_ORDER: round=56 wave=w1 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T00:22:47.615Z verdict=OK reason=ok` rc 0.
  - `--rev 3423ae…`: `… launch=none verdict=FAIL reason=no_registry` rc 1 (expected; the registry is not in the freeze commit).
  - `--selftest`: `MADO_FREEZE_ORDER_SELFTEST: OK`, rc 0 (its 11 cases pass in the scratch dir).

## 3. Hold-out path sweep (`grep`, text only; no hold-out file was opened or hashed)

`grep -F '.cache'` over `.ufo/waves/round-56` (working tree, excluding fixtures/): hits only in the chronology instruction text itself —
- make-w1-spec.py:91, w1-spec.json:214, w1-dispatch.json:505.

`grep -F 'c2-holdout'` over the same tree (excluding fixtures/), each hit:
- registration.md:85, :152, :155, :156 (frozen contract, committed at 3423ae; same lines at 3423ae and tip)
- make-w1-spec.py:51, :91 (spec generator)
- w1-spec.json:69, :214 and w1-dispatch.json:360, :505 (wave dispatch text, committed at 2aa347b)
- w1/R56ExecWatchplanHarness/r56_ctl_c2.py:28 (`HOLDOUT = WAVE + "/fixtures/c2-holdout"`, a seat's untracked file)
- w1/R56ExecWatchplanHarness/__pycache__/r56_ctl_c2.cpython-314.pyc (binary match of the same string)
- w1/R56ExecWatchplanHarness.md:7, :23 (seat notes)

`grep -rl` under `.ufo/waves/round-56/fixtures/`: no hit names (no fixture file contains either string).

Committed tip tree, `git grep -F -e .cache -e c2-holdout 2aa347b -- .ufo/waves/round-56`: the same registration.md, make-w1-spec.py, w1-spec.json, w1-dispatch.json hits; no round-56 `c2-holdout` path is committed (names only checked via `ls-tree`).

**Out-of-round hits, reported and not used:** `git ls-tree -r` at the freeze commit and at the tip lists `.ufo/waves/round-55/fixtures/c2-holdout/H01..H08` (args.json, c1.conf, expected.out, expected.rc, getoption.json for H06) plus `round-55/w1/R55CritHoldout/…`, `R55ExecC2Harness/receipts/standin-holdout-commit.txt`, `round-55/w2/R55W2CritToolIsolation/receipts/demo-*-holdout-commit.txt`. These were introduced in `ebd66fbf` (2026-10-28T20:16:27-03:00, "sealed hold-out revealed"). I did not open or hash them; I did not compare them with the round-56 commitment `65dc9d3e…` (`c2.holdout_commit_sha256`). That comparison is open for the integrator (see D2).

## 4. Defects, ambiguities, and what the checker would do

**D1. The hold-out location is disclosed to seats and to the contract (sealing defect).** Registration §C2 says the hold-out is "held outside the repository" and "seats are not told where it is held and do not look for it". But the frozen contract (registration.md:85, :152, :155–156) names `fixtures/c2-holdout` as the harness default, and the dispatch to the C2 harness seat (w1-dispatch.json:360, seat R56ExecWatchplanHarness) states "the hold-out (from --holdout, or .ufo/waves/round-56/fixtures/c2-holdout at --rev when present, else `absent`)". That seat's code (r56_ctl_c2.py:28) hard-codes the same path. Registration wins by instruction; the disagreement is recorded here. Consequence: a seat knows where round 56's hold-out would sit *inside* the repo at `--rev`, which contradicts "held outside the repository". The commitment check still stands (it depends on bytes, not location), but the sealing claim as worded is false.

**D2. Prior hold-out is committed in-repo under the same naming.** `round-55/fixtures/c2-holdout/H01..H08` is in the tip tree, revealed in `ebd66fbf`. Round 56's H01–H08 are said to be generated "before the wave", and their commitment is 65dc9d3e…. Whether round 56's H01–H08 are distinct from round 55's is **not verified** by this seat. The integrator should compare commitments (tree hash only) before using the round-56 hold-out. I did not do that comparison because the instruction forbids using the hold-out path.

**D3. The freeze-order checker's FREEZE set does not cover the whole freeze.** `check-freeze-order.py` hashes only `claims-frozen.md`, `registration.md`, `frozen-tables.json`. The claims text (claims-frozen.md, "Frozen" paragraph) says `freeze-verify.py`, `receipts/*`, `fixtures/c2/`, `ctl/` and `fetch/` are in the freeze commit "checked by quality/check-freeze-order.py". The tables cover fixtures/c2 (commitment) and fetch (c1 `pin_sha256`), but **not** `ctl/`, `receipts/`, or `freeze-verify.py` (tables keys inspected: c1 has no ctl, c2 has no ctl; no receipt or freeze-verify hashes). Demonstrated in a scratch repo (`rc=0 reason=ok`):
```
commit freeze (committer 2026-10-27T10:00-03), registry createdAt 14:00Z, commit ctl/stub.py edit at 15:00-03  → MADO_FREEZE_ORDER: … freeze_time=2026-10-27T10:00:00-03:00 … verdict=OK reason=ok  rc=0
commit freeze-verify.py edit at 16:00-03                                                                         → same OK, rc=0
```
So a post-launch edit to a `ctl/` stub or to `freeze-verify.py` passes the checker. The round-56 tip has no such edit (diff empty), so the verdict for this round is not affected by D3; the claim text overstates the checker.

**D4. The literal chronology command does not test round 56.** The prompt's `git ls-tree … | grep -E '\.ready'` returns round 39–55 `.ready` paths (rc 0). Round-56 is checked only by filtering on `round-56`. Suggested fix: `grep -E 'round-56/.*\.ready'`.

**D5. Round-56 `.ready` markers are untracked, unlike rounds 39–55.** `w1.ready` and `w1.ready.dispatched` are not in any commit (rounds 39–55 are). "No `.ready` at the freeze commit" is therefore true by convention, not by evidence of order. The order evidence is birth times, reflog and `createdAt`.

**D6. Forgeable channels and what they change here.**
- Committer date (checker's verdict input): settable with `GIT_COMMITTER_DATE`. A backdated freeze reads OK (the checker's own selftest case 7b shows this). Reflog `master@{…}` says "export from jj" and was written by the same toolchain, so it is not an independent clock against a forged date. Kernel birth times of the freeze files (21:14:50–21:19:11) are independent of git env and all precede 21:19:17; they corroborate the committer date but a `touch` could forge them too.
- `createdAt`: a field the registry tool writes. It is 20 ms before the registry file's birth time (21:22:47.615 vs 21:22:47.635), so it looks like a real write timestamp, not a plan time. The checker's docstring calls it "plan time"; the actual dispatch was 21:27:02 (`.ready.dispatched`), four minutes later. Using dispatch as launch would only widen the margin.
- Direction: a forged late `createdAt` helps a late freeze pass. Here `createdAt` is already after the freeze, so forging it does not help a late freeze. A backdated committer date does. The only hard anchor is that 2aa347b names 3423ae in its commit hash (the wave spec states "committed at 3423ae… (BEFORE this wave)"), which makes the freeze's content and committer date fixed once 2aa347b exists. 2aa347b itself is a local commit with no signature; no external timestamp (remote push record, signed tag, timestamping) was found.
- For this round the verdict is **not** sensitive to these channels at the margins shown (4–8 minute gaps), but the checker alone is not evidence against a deliberate backdate.

**D7. Author date of the freeze commit.** Author date 20:59:32 equals the base commit's committer time to the second (13f0acbe, 20:59:32). The checker ignores author date. Plausible honest cause: a jj change created right after the base export; not verified.

**D8. Base lane tip is a commit by another lane.** registration.md: "lane tip 13f0acbe" (base). That commit is authored by protocol-shokunin ("round-55 verifier spot-check (integrator, hyaku)"). Not a chronology defect, but the "base" is a sibling lane's commit in this repo; a reader should not assume it is this lane's own work.

## 5. Not verified

- Hold-out commitment `c2.holdout_commit_sha256` = 65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183: **not recomputed** (sealed; instruction forbids use). Also not compared with the round-55 tree (D2).
- Remote push history (origin github): not consulted (no network use, read-only lane).
- Kernel birth times and reflog are local; not cross-checked against any external source.
- `freeze-verify.py`, receipts/*, ctl/* contents were not re-run or read beyond existence and blob identity (the lane's own verifiers are other seats' scope).

## 6. Host and tooling

No tool installed or upgraded. No git mutation in the lane or fleet repo (read-only `log`, `show`, `ls-tree`, `cat-file`, `grep`, `reflog show`, `status`, `diff --stat`). Scratch-only repos were created under `/fast/scratch/hyaku/mado-r56/R56CritChronology/` for the D3 demonstration and removed. Receipts copied to `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56CritChronology/`: `commit_c2.py` (commitment recompute) and `freeze-order-tip.txt` (checker output).
