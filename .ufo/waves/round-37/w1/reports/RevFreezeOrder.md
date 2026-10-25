# RevFreezeOrder — reviewer report, mado round 37 wave 1

Seat: `L1Mado37-2.RevFreezeOrder` (reviewer, leaf). Assignment: `.ufo/waves/round-37/w1/prompts/RevFreezeOrder.md`.
Scratch outputs: `.ufo/waves/round-37/w1/scratch/RevFreezeOrder/` (every quoted run below is saved there).
Sandboxes: `/dev/shm/mado37-RevFreezeOrder/{v1,v2}` (`git clone -q --no-local` of the lane, detached at
8f0a9e3 / 893a8aa), removed after the run. Lane state after all runs: `git status --short` shows only
untracked seat reports and `w1/scratch/`; no lane file was written. Tools installed: none.

## Verdict summary

| Item | Verdict |
|---|---|
| 1. Freeze chronology | PASS on committer date and reflog; finding F4 on the author date the prescribed command prints |
| 2. Targets absent at 8f0a9e3 and 893a8aa | PASS |
| 3. v2 amendment append-only over v1 | PASS (19 additions, 0 deletions); finding F3 on reconciliation with the freeze rule |
| 4. v1 receipts kept | PASS (same blob ids at 8f0a9e3, 893a8aa, 80b83c8) |
| 5. QUALITY criterion 61 (commands run verbatim, output committed) | PARTIAL: the counters, the axis check and the v2 controls reproduce; findings F1, F2, F5, F6, F7 |

## 1. Chronology

```
$ git -C LANE log --format='%H %ad %s' --date=iso -5 master
80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b 2026-10-25 09:12:46 -0300 round-37: the inherited round-36 DistillerFindings seat report (spot-check R1), and the wave-1 spec, prompts, dispatch and registry (38 seats)
893a8aadc80ab19bc163e366d674a8ac32feacd0 2026-10-25 09:08:02 -0300 round-37: re-freeze both counters as v2 before any data — ...
8f0a9e3f78120d00e5e9f32c909618d549f976b4 2026-10-25 05:45:07 -0300 round-37: freeze — registration, the two counters, controls (12/12) and the re-opened source receipts, before any data
b4e47e980bfb0cbc8a4e788f59a41db858751fd8 2026-10-25 05:45:07 -0300 round-36 verifier spot-check (integrator, hyaku): non-author admit/reject
a5aaa09ad38bfd90c13d76ccf371e36c45a2697e 2026-10-25 05:40:09 -0300 round-36: ...
```

Author and committer dates (`--format='%H author=%an %ad commit=%cn %cd'`):
- 8f0a9e3: `author=... 2026-10-25 05:45:07 -0300` and `commit=... 2026-10-25 09:05:49 -0300`
- 893a8aa: author and commit both `09:08:02`; 80b83c8: both `09:12:46`; b4e47e9: both `05:45:07`

Reflog (`git reflog --date=iso -8 master`): `b4e47e9 master@{05:45:07}` → `8f0a9e3 master@{09:05:49}` →
`893a8aa master@{09:08:02}` → `80b83c8 master@{09:12:46}`, all `export from jj`.

Working-tree mtimes of the receipts (all clean against HEAD): census-before 08:56; controls.txt 09:04;
axis-base, before-c1, before-c2 09:05; v2 receipts 09:07. These are consistent with the committer dates.

Ordering is base 05:45:07, then v1 freeze 09:05:49, then v2 re-freeze 09:08:02 (2 min 13 s later), then
wave-1 dispatch 09:12:46. At 8f0a9e3 and 893a8aa the tree holds no `w1/` path (`w1=0`); at 80b83c8 it holds
`w1=39`. **PASS**: the dispatch comes after both freezes.

## 2. Target files absent at both freeze commits

`git ls-tree -r <c> -- corpus/knowledge/event-delivery-limits-r26.md corpus/knowledge/event-queue-observability-r37.md tools/mado-eventq.py corpus/lessons/round-37.md`
prints nothing with rc=0 at both 8f0a9e3 and 893a8aa. A recount by name gives `targets=0` at 8f0a9e3,
893a8aa and 80b83c8. In the working tree, `ls` returns `No such file or directory` for all four files and
for the C2 live snapshot `receipts/eventq-live-ss.txt`, which is also absent at all three commits
(`live-ss=0`). **PASS**.

The ground-unheld tokens are also absent. `git grep -l -F <token> <rev> -- corpus/knowledge | wc -l` gives
`files=0` for `MAX_QUEUED_EVENTS`, `overflowed event queue`, `debug:disable_logs` and `m_logsEnabled` at
b4e47e9, 8f0a9e3, 893a8aa and master (`scratch/RevFreezeOrder/gitgrep.txt`; the `rc=` column in that file
is a pipeline artifact and should be ignored).

## 3. Amendment is append-only

`git diff 8f0a9e3 893a8aa -- .ufo/waves/round-37/registration.md` has one hunk, `@@ -99,3 +99,22 @@`. A count
of `+` and `-` lines gives `19 +` and no `-`. `--numstat` gives `19 0 .ufo/waves/round-37/registration.md`.
**PASS**.

The rest of the v2 commit (`--numstat`):
- `controls.py 8/6`: `entry(..., stated=False)` adds `**OBS**` quote lines; `c1-golden` is renamed to `c1-token-stub` (expect MISSED) and `c1-golden-v2` is added (expect MET).
- Counters: `c1 13/5`, `c2 36/13`.
- New receipts: `before-c1-v2.txt`, `before-c2-v2.txt`, `controls-v2.txt`.

`git diff --quiet 8f0a9e3 893a8aa -- .ufo/waves/round-37/fetch .ufo/waves/round-37/assimilation` prints
`FETCH_ASSIM_UNCHANGED_v1_to_v2`.

## 4. v1 receipts kept

The `git ls-tree -r <c> -- .ufo/waves/round-37/receipts` blob ids are the same at 8f0a9e3, 893a8aa and 80b83c8:
`before-c1.txt 96c6cfa…`, `before-c2.txt 051845e…`, `controls.txt 045f72e…`, `axis-base.txt f49d2f3…` and
`census-before.txt 15f73c5…`. The v2 commit only adds the `-v2` files. **PASS**.

The two v1 "before" receipts also reproduce byte-for-byte with the v1 counter bytes. In the sandbox at
8f0a9e3, `python3 -I quality/counters/c1-r37-event-ground.py --repo . --rev b4e47e9…` and the C2
equivalent, diffed against `tail -n +2` of the receipt, print `V1_C1_BEFORE_IDENTICAL` and
`V1_C2_BEFORE_IDENTICAL`.

## 5. QUALITY criterion 61 (`corpus/QUALITY.md:369`)

> "Every command a registration names is run verbatim at the freeze and its output committed with the
> registration … Check: copy each command out of the registration and run it unchanged; a
> `SETUP_ERROR`/exit 2 is a freeze defect, not a reader error."

Commands named by `registration.md`, each run unchanged:

| Line | Command | Run | Result vs receipt |
|---|---|---|---|
| 11 | `python3 -I quality/check-axis-scores.py --repo . --rev master` | in the lane | exit 0, `navigation 50/50`, `calibration 48/48`, `operability 12/12`, `MADO_AXIS: checked=3 mismatched=0 rev=80b83c8…`. The values match line 11 and `axis-base.txt`, but the receipt ran `--rev b4e47e9…`, not `--rev master` (F5). Run with the base sha it is byte-identical: `AXIS_BASE_IDENTICAL` |
| 23 | `git grep -l -F <token> master -- corpus/knowledge` (×4 tokens) | in the lane | empty at base, both freezes and master. No committed receipt (F5) |
| 37 | `cd LANE && python3 -I quality/counters/c1-r37-event-ground.py --repo . --rev <rev>` | in the lane, rev = base | byte-identical to `before-c1-v2.txt` (`C1_BEFORE_V2_IDENTICAL`): `PRED-C1-r37-v2 admitted=0/2 verdict=TARGET_MISSED … exit=1`. At 8f0a9e3, 893a8aa and master: `admitted=0/2 verdict=TARGET_MISSED`, exit 1 |
| 63 | `cd LANE && python3 -I quality/counters/c2-r37-eventq.py --repo . --rev <rev>` | in the lane, rev = base | byte-identical to `before-c2-v2.txt` (`C2_BEFORE_V2_IDENTICAL`): `fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED`, exit 1. Same result at 8f0a9e3, 893a8aa and master |
| 77 | `python3 -I .ufo/waves/round-37/controls.py --out .ufo/waves/round-37/receipts/controls.txt` | **sandbox only** (from the lane it would overwrite a committed receipt; see F1) | at 893a8aa, three runs. Run 1: exit 1, `controls=13 correct=12/13`, with `control=c2-stub-socket … rc=2 ok=0 :: PRED-C2-r37-v2 SETUP unresolvable revision` (F6). Runs 2 and 3: exit 0, and identical to `controls-v2.txt` once the sandbox `rev=` hashes are normalised (`CONTROLS_V2_IDENTICAL_MOD_SANDBOX_REV`). At 8f0a9e3 (the v1 script): exit 1, `controls=12 correct=11/12`, with `control=c1-golden expect=TARGET_MET rc=1 ok=0 :: PRED-C1-r37-v2 admitted=0/2` (F2) |
| 55 | `hyprctl getoption debug:disable_logs -j` (a read verb, named as a C2 live default) | host | `{"option": "debug:disable_logs", "int": 1, "set": false }`, exit 0. This matches the S213 quote in `controls.py` QUOTES and supports the key finding that markers are not observable on this host |

Not run: `ss -xpa` and `journalctl --user -u wayland-wm@hyprland.desktop.service` (line 54). They are live
defaults of a tool that does not exist yet, not freeze measurements, and the journal falls under the
privacy bound. No Hyprland socket was connected to.

## Findings by severity

**F1 — medium. Running the registered controls command verbatim destroys the v1 record, and the v2 controls receipt has no named command.**
- Registration line 77 names `--out .ufo/waves/round-37/receipts/controls.txt`. Amendment 1 (lines 118–120) keeps the counting commands "unchanged" and promises that `receipts/controls.txt` "stay[s] as the v1 record", with v2 receipts carrying a `-v2` suffix.
- Under criterion 61 a reader copies line 77 and runs it unchanged from the lane. That overwrites the committed v1 `controls.txt` (blob 045f72e) with v2 output.
- The receipt that was actually committed, `controls-v2.txt`, comes from an invocation that no registration line names.
- Unlike `before-*.txt` and `axis-base.txt`, neither controls receipt starts with a `$ <command>` header, so the receipts do not record their own invocation either.
- Fix: an amendment line naming `--out .ufo/waves/round-37/receipts/controls-v2.txt`, plus a `$` header line in the receipt.

**F2 — medium. `controls.py` scores with the lane's working-tree counters, not the counters frozen in its own commit, so `controls.txt` cannot be reproduced from 8f0a9e3.**
- `git show 8f0a9e3:.ufo/waves/round-37/controls.py` has `17:LANE = "/home/vgpnk/…/mado-shokunin"` and `21:C1 = os.path.join(LANE, "quality/counters/c1-r37-event-ground.py")` (same for C2 at line 22). The 893a8aa version is identical in this respect.
- Run today at 8f0a9e3, the v1 script therefore scores with the v2 counter: `PRED-C1-r37-v2` lines, `c1-golden … ok=0`, `correct=11/12` (`scratch/RevFreezeOrder/controls-v1script-rerun.txt`; 140-line diff in `controls-v1-diff.txt`).
- The same coupling means any later edit to a lane counter silently changes what the frozen v2 controls measure.
- Fix: resolve the counters from the script's own directory or from `git show <freeze>:` blobs. The C1/C2 v1 "before" receipts do reproduce (item 4), because there the counter is invoked from the sandbox at 8f0a9e3.

**F3 — low. The amendment does not reconcile with the registration's own freeze rule.**
- Registration lines 4–7 say: "any later change to a counter is a new predicate and the claim it belongs to then fails as declared."
- 893a8aa changes both counters. Read literally, `PRED-C1-r37-v1` and `PRED-C2-r37-v1` therefore fail as declared.
- Amendment 1 registers v2 predicates before any data. That is legitimate: no `w1/` path, target file or live snapshot existed at 893a8aa (items 1 and 2). But it never states that the v1 claims are withdrawn or failed under that rule.
- The closure and scorecard should record v1 as withdrawn before data, not silently replaced.

**F4 — low. The prescribed `%ad` log shows a misleading freeze time.**
- `%ad` prints 8f0a9e3 at `05:45:07`, the same as its parent b4e47e9. That is jj's change-creation author stamp.
- It also places the freeze before the "Attempt 1 (06:05–06:46 -03)" window that the frozen registration text itself describes.
- The real landing is the committer date and reflog entry `09:05:49`.
- Chronology claims should cite `%cd` or the reflog. The order is valid either way (item 1).

**F5 — low. Several registration commands do not pin a revision, and one has no receipt.**
- Line 11 uses `--rev master`, a moving ref; the receipt used the base sha. Run verbatim today it reports `rev=80b83c8`.
- Line 23 uses `master` and a `<token>` placeholder, and no output was committed.
- Lines 37 and 63 use a `<rev>` placeholder; the receipts substitute the base sha, which is reasonable.
- Every value reproduces, but criterion 61's "output committed" is unmet for line 23.

**F6 — low. `controls.py` ignores git failures, so the controls receipt is not deterministic.**
- `sh()` (lines 39–40) discards return codes from `git clone`, `checkout`, `add` and `commit`.
- One of three v2 runs scored `c2-stub-socket` as `SETUP unresolvable revision` (rc=2), giving `correct=12/13` and exit 1. The other two runs gave 13/13.
- It fails closed (rc=2 is never `ok=1`), so it cannot produce a false MET. But a re-run receipt can disagree with the committed one for infrastructure reasons.
- [INFERENCE] The cause is a transient sandbox clone failure under concurrent seat load. stderr was empty because `sh()` captures it.

**F7 — info.** `receipts/census-before.txt` is committed in the freeze, but no registration line names its producing command (`rg census-before` hits only old LOG and lesson text).

## Residual risk and verification gaps

- The v1 `controls.txt` was not reproduced, and cannot be under F2 without restoring the v1 counters at the lane path. That would mean writing to the lane, which is forbidden; a sandbox patch of `LANE` in a copied script would no longer be a verbatim run. Its content is internally consistent with the v1 counter (all `PRED-C1-r37-v1` lines, 12/12) but is not independently reconfirmed.
- The F6 root cause is inferred, not observed.
- Byte identity of the controls reruns holds only after normalising the sandbox commit hashes (`rev=` fields), which depend on commit timestamps by construction.
- The working-tree check in item 2 is a point-in-time observation. By the end of this seat, `git status --short` showed changes from other actors, none written by this seat: `M corpus/SOURCES.md`, `?? fetch/S215.bin`, `?? fetch/S216.bin`, `?? corpus/knowledge/event-delivery-limits-r26.md` and `?? corpus/knowledge/event-queue-observability-r37.md`. The committed-tree results (both freeze commits and 80b83c8) are unaffected. S215 and S216 are not among the rows the registration names (S189, S201, S212–S214), so the closure should check whether the entries cite them.
