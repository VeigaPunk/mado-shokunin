# Seat ScrQualityCriteria — report

**Status: complete.** Drafted QUALITY criteria 69–72 from four round-40 defects that a verifier
routed, each with a runnable `Check:` executed in both directions this seat. `corpus/QUALITY.md` was
**not** edited (the L1 owns the append; counters, controls, registration and reference are frozen).

## 1. What was asked and what landed

| asked | delivered |
|---|---|
| read the QUALITY tail (60–68) and the pre-wave state | `corpus/QUALITY.md:355-383` (ends at 68, `wc -l` = 383); `.ufo/waves/round-41/registration.md`; `.ufo/waves/round-41/receipts/` (8 files) |
| four criteria from real, evidenced mistakes | criteria **69** (tip-revision receipts), **70** (wave-control markers), **71** (seat report path), **72** (equivalent mutant from redundant code) |
| a `Check` that can fail | `check69.py`, `check70.sh`, `check71.py`, `check72.py` — each run fail-side and pass-side |
| the control/fixture that shows it can fail | committed round-40 instances named per criterion + a `mktemp` fixture for 70; measured survivor for 72 |
| write `…/w1/ScrQualityCriteria/criteria.md` | written (digest below) |

## 2. The four criteria and their grounds

Every ground is a routed round-40 defect, not a hypothesis. Quotes are ≤ 25 words, located, and
verified by `verify-quotes.py` (word counts in `receipts.txt`).

**69 — tip-revision receipts.** Ground: round-40's report cites `MADO_AXIS checked=3 mismatched=0 at
fb49621` (`corpus/lessons/round-40-verifier-spotcheck.md:19` at `cd950ec`, defect (b)) while no
committed receipt under `.ufo/waves/round-40/receipts/` names `fb49621`; the only axis receipt is
`axis-base.txt` at `rev=9fc511d`. Check: extract `rev=`/`rev `/`at ` hex tokens from a report and
require a committed receipt in that round's `receipts/` whose bytes carry each token.
*Fail side:* `MISSING fb49621 … FAIL 1/1`, exit 1. *Pass side:* round-41 freeze `60c3914`,
`ab2bfaa…` found in `receipts/axis-base.txt`, `PASS 1/1`, exit 0.

**70 — wave-control markers.** Ground: `one untracked .ufo/waves/round-40/w1.ready.dispatched
(dispatch marker, no round work)` (`…spotcheck.md:15` at `cd950ec`; routed item §6.1).
Check: compare markers on disk to the **revision's** tree (`ls-tree`) plus a `git status` leg.
*Fail side:* at `fb49621` → `UNTRACKED .ufo/waves/round-40/w1.ready.dispatched`,
`VERDICT: DIRTY_MARKER`, exit 1. *Pass side:* the same wave at `cd950ec` (dispatch commit tracked the
marker) → `VERDICT: CLEAN`, exit 0; the `mktemp` fixture reads CLEAN with both markers committed and
`DIRTY_MARKER` once a third marker is left on disk.

**71 — seat report path.** Ground: M40-6, `ConnCrossClaim` returned
`report: .ufo/waves/round-49/w1/ConnCrossClaim.md` (`corpus/lessons/round-40.md:135`).
Check: each row's `report` must match `^\.ufo/waves/round-<N>/w1/<Seat>\.md$`, name its own seat,
and exist at the revision. *Fail side:* at `fb49621`, `FOREIGN ConnCrossClaim … round-49` **and**
`FOREIGN ScoutOptionTypes returned /home/…/w1/ScoutOptionTypes.md` (absolute path — see §4),
`RESOLVED ok=33 bad=2 … exit 1`. *Pass side:* the same file with only those two rows dropped →
`PASS`, exit 0 (so the check is not failing on the other 33 seats).

**72 — equivalent mutant from redundant code.** Ground: M40-1's reply-cap survivor —
`the reply cap (the mutant kept a post-check -> the control now removes both)`
(`corpus/lessons/round-40.md:88-89`). The property is enforced at three sites in
`tools/mado-options.py:942-951`. Check: every mutant named in a controls file has a receipt row below
target, and every "equivalent mutant" declaration names a committed receipt or a code site.
*Fail side, measured:* a copy patched to drop only the read bound
(`partial-m38.patch.txt`; `too_long = len(raw) > REPLY_CAP` kept) scores
`fixtures=19/19 … verdict=TARGET_MET`, exit 0, under the frozen round-40 v2 counter
(`quality/counters/c1-r40-live-v2.py --repo . --rev 91f0a2b --tool <patched copy> --nonce
41a1b2c3d4e5f607`, 45.9 s) — i.e. the mutant survives because of the redundant post-check; the check
reads `SURVIVOR M38-partial-readcap-only … FAIL 1 defect(s)`, exit 1. *Pass side:* committed
`ctl-c1-v2.txt` (57 rows; `M38-reply-cap-dropped` = `fixtures=18/19 … TARGET_MISSED`, line 46; `M43`
declared with `receipts/f32-equivalence.txt`; `X15` with `splitlines()`) and `ctl-c2-v2.txt` (33 rows)
each read `PASS`, exit 0.

## 3. Verification the main agent should run

```
bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w1/ScrQualityCriteria/run-checks.sh
```
Read-only (`git -C … show/grep/cat-file/ls-tree/status`, `GIT_OPTIONAL_LOCKS=0` in the marker check);
writes only a `mktemp -d` fixture, which it removes and asserts absent. Expected: 9 check runs (plus the 2 fixture runs) with
the exits quoted above, the fixture block, and `VERDICT: PASS` from `verify-quotes.py`.

## 4. Findings beyond the draft (each names what it attacks)

1. **A second path-discipline instance in round 40.** `ScoutOptionTypes` returned an **absolute**
   report path (`w1-results.json:344-346`) that is tracked at `fb49621` — the same class as M40-6
   (root-dependent rather than dead), and the reason criterion 71's pattern anchors at
   `.ufo/waves/round-<N>/`. Attacks: the assumption that M40-6 was a single occurrence.
2. **The round-40 leftover is now tracked, which stales the spot-check's own reading.**
   `w1.ready.dispatched` is absent at `fb49621` but tracked at `cd950ec`, so
   `git status --porcelain` (what the spot-check used) can no longer see it. This is why criterion 70
   compares disk presence to the *revision*'s tree. Attacks: `status`-based leftover checks.
3. **`X15`'s equivalence is argued, not measured.** `ctl/run-c2-v2-controls.py:247` justifies it with
   the counter's own parse rule (`splitlines()`); `M43` has a swept receipt
   (`receipts/f32-equivalence.txt`: `0 of 999`). Criterion 72 accepts both and records the site form
   as the weaker one. Attacks: any claim that "declared equivalent" always means measured.
4. **29 of round-40's 64 seat rows returned no `report` key at all** (`RESOLVED … no-report=29`).
   Not judged by criterion 71 — a path rule does not decide whether a seat owes a report file — but
   the L1 may want a separate criterion if that is a defect class.

## 5. Non-actions and limits

- No edit to `corpus/QUALITY.md`, the counters, controls, registration, reference, receipts, fetch
  bytes, `SOURCES.md`, or any other tracked file. `GIT_OPTIONAL_LOCKS=0 git status --porcelain -uall`
  over the lane shows only `?? .ufo/waves/round-41/…` paths.
- No pacman, no package transaction, no journal verb, no compositor/Wayland connection, no mutating
  git in the lane. The one counter run is sandboxed (`bwrap`) by the counter itself and reads the
  lane read-only; its `--tool` was a `/tmp` copy, now removed.
- Limits stated inside the criteria: 69 pins the citation, not the arithmetic; 70 cannot tell a
  marker never written from one deleted; 71 does not judge missing reports; 72 accepts a named site
  as a source-level argument.
- `corpus/lessons/round-41.md` does not exist yet, so all four criteria cite round-40 sources that
  resolve today. If the L1 records `M41-n`, **extend** the parenthetical, do not replace it
  (criterion 54 resolves each `file#anchor` against its own file).

## 6. Artifacts (all under `.ufo/waves/round-41/w1/ScrQualityCriteria/`)

`criteria.md` (the draft), `check69.py`, `check70.sh`, `check71.py`, `check72.py`, `run-checks.sh`,
`verify-quotes.py`, `receipts.txt` (full transcript + quote verification), `partial-m38.patch.txt`,
`partial-m38-score.txt`, `digests.txt`, `scratch/` (the four inputs the checks read). Digests in
`digests.txt`; `criteria.md` = `eb0e668fb3b8ef6cd476e3f9cf332009914efa66078836379e4b13d8fac98b83`.

Tool state: no installs, no upgrades this seat (Python 3.14.8, git 2.56.0, `/usr/bin/bwrap` present).
