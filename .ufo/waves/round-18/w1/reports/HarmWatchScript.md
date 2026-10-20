# HarmWatchScript — round-18 harm-watch receipt runner

Seat: `MadoR18.HarmWatchScript` (executor, leaf). Item: write only
`.ufo/waves/round-18/harm-watch.sh`; run it only with a `/tmp` OUTDIR; no live
gate; no package/service/compositor probe. Snapshot `2026-10-20T15:49:07Z`.

Files written (both untracked; L1 commits):

| File | sha256 | Note |
|---|---|---|
| `.ufo/waves/round-18/harm-watch.sh` | `a256d28c7b43ad28c24c0bf97bffda57ba2ff5feadbf6c042686c180779db6c7` | 348 lines, mode 755, `bash -n` clean, `shellcheck -S warning` clean |
| `.ufo/waves/round-18/w1/reports/HarmWatchScript.md` | this file | report |

No lane VCS write occurred; every `git` call the script makes and that I made
while testing is read-only (`rev-parse`, `cat-file`, `show`). The only git
writes were inside the throwaway `/tmp/hw-lane` clone. No default-OUTDIR run:
`.ufo/waves/round-18/evidence/` was not touched by this seat. No live gate, no
pacman/systemctl/journalctl/hyprctl/walker/swaybg/omarchy invocation, no
install or upgrade.

---

## 1. Behavior

    REV=<rev> [OUTDIR=<dir>] bash .ufo/waves/round-18/harm-watch.sh
    bash .ufo/waves/round-18/harm-watch.sh <rev>        # --help supported

`REV` resolves once to a commit SHA (`rev-parse --verify REV^{commit}`); unknown
or missing REV and an uncreatable OUTDIR exit 2 (tested). OUTDIR defaults to
`.ufo/waves/round-18/evidence`; each command overwrites its own file in it, so a
re-run at a new commit replaces stale receipts. `harm-watch-summary.txt` and
`harm-watch-pins.txt` are rewritten at start.

Every command file has exactly this shape: line 1 a receipt, then combined
stdout/stderr, then one final `exit=<rc>` (`exit=skipped` when the pin did not
assert and the command did not run).

    RECEIPT tool=<abs path> tool_sha256=<hex> measured_commit=<rev-sha> \
            utc=<ISO-8601 Z> cwd=<lane root> argv=<shell-quoted words>

Pin discipline (this is also the R17-V1/V2 / JjAuditMado F10 class inside the
harness): worktree bytes are hashed, then the REV object is proven present with
`git cat-file -e` and materialised with `git show > tmpfile` **before** hashing.
A failed `git show` can never become the empty-input digest `e3b0c442…`; it is
`state=rev_read_failed`. Only on `worktree_sha256 == rev_sha256` does the
receipt carry `measured_commit=<REV>` and the command run. On
`mismatch`/`missing_*` the receipt carries `measured_commit=UNVERIFIED`, the two
digests, `status=skipped:pin_mismatch`, and the aggregate exits 1. Worktree tools
must equal the named commit; that is the point of the receipt.

Commands and output files (suite set discovered at run time):

| File | argv | Pinned tool |
|---|---|---|
| `harm-gate-selftest.txt` | `bash tools/mado-verify.sh --selftest` | `tools/mado-verify.sh` at REV |
| `harm-action-plan-selftest.txt` | `python3 -I <ROOT>/tools/mado-action-plan.py --selftest` | `tools/mado-action-plan.py` at REV |
| `harm-tripwire-<round>-<suite>.txt` | `python3 -I <ROOT>/tools/mado-tripwire.py --selftest <ROOT>/.ufo/waves/<round>/tripwire/<suite>` | `tools/mado-tripwire.py` at REV |
| `harm-measure-u.txt` | `python3 <ROOT>/.ufo/waves/round-16/measure.py REV` | `round-16/measure.py` at REV |
| `harm-nav-fleet-round-1.txt` | `REV=<sha> bash -s` on the `### Counting command` block extracted byte-exactly from `REV:SCORECARD.md` | block sha256 (e.g. `8b59b503…`) |
| `harm-census-validate.txt` | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | fleet repo `HEAD` |

Suite discovery: each direct child of `.ufo/waves/round-17/tripwire` and
`.ufo/waves/round-18/tripwire` that contains `expected.json`; a dir without one
and an absent root are summary `NOTE`s, not failures. Each command runs under
`timeout ${HARM_TIMEOUT:-1800}`; a non-zero/timeout rc is recorded and counted,
and the run continues.

Two deliberate choices:

* The navigation block is executed from `REV:SCORECARD.md`, not the worktree,
  so an in-flight SCORECARD edit cannot skew the command. Its bytes are the
  pinned tool (`tool=<REV>:SCORECARD.md#Counting-command`).
* The census helper lives in the fleet root repo, outside the lane. It is
  pinned against that repo's `HEAD` and the receipt says
  `measured_commit=fleet:<sha>` — never a lane REV that does not contain it.

Summary line format: `OK|FAIL|SKIP <exit=…> <file> <argv>`, then
`HARM_WATCH: PASS` or `HARM_WATCH: FAIL failures=N` plus rev/outdir/counts.
Exit: 0 all asserted+green, 1 any failure or pin skip, 2 usage/revision.

---

## 2. Evidence

### 2.1 In-flight lane run — the pin assertion bites (exit 1)

`OUTDIR=/tmp/harm-watch-test bash .ufo/waves/round-18/harm-watch.sh d3a0000`
(2026-10-20T15:44:12Z, 1.8 s). The lane tools had already moved off the
baseline, so six commands were skipped instead of being mislabelled as
`d3a0000` measurements:

    RECEIPT tool=/home/…/tools/mado-verify.sh tool_sha256=1dbbfe78… measured_commit=UNVERIFIED utc=2026-10-20T15:44:12Z cwd=/home/…/mado-shokunin argv=bash tools/mado-verify.sh --selftest
    pin_assert=mismatch worktree_sha256=1dbbfe78890b3a917641d5584b1d93d3f08c0ca02779b450d0cf19fb39a0f760 rev_sha256=fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207
    status=skipped:pin_mismatch
    exit=skipped

Tripwire likewise: worktree `593b3aaf…` vs `d3a0000`'s `962919ce…`, five
suite skips (core, compound, hardening, w2-regressions, and the then-new
`round-18/tripwire/frozen`). The remaining four commands ran green at that
instant: action-plan `52/52`; measure `U 7/7`, score 10.0 (its JSON shows
`"count": 7`, calibration 15/23 = 6.5217 on the committed bytes); navigation
`indexed=32/32 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0;
census exit 0 with three `W04` same-URL warnings and `mado ok`.
Summary ended `HARM_WATCH: FAIL failures=6`.

### 2.2 Pinned PASS run on identical-logic clone (exit 0)

To exercise the assert-then-run path I cloned the lane to `/tmp/hw-lane`
(read-only clone; all test git writes confined there), committed the current
tool/suite bytes at test commit `23eed62f522b50405648fc87ca6f85ac47dc0d11`,
re-pinned `PIN_MADO` to the derived `20714096…` inside that clone only (the
in-flight gate had not yet carried its recut), and replaced `ROOT=` in the
copied script with `/tmp/hw-lane`. The ship script's logic is otherwise
byte-identical. `OUTDIR=/tmp/hw-final … 23eed62` → `HARM_WATCH: PASS`,
exit 0, 10 commands:

| Check | Retained result |
|---|---|
| gate selftest | `MADO_SELFTEST: 389/389 assertions passed`, exit 0 |
| action-plan selftest | `SELFTEST_SUMMARY: 52/52 passed` |
| tripwire core / compound / hardening / w2-regressions | 9/9 · 16/16 · 33/33 · 30/30 |
| tripwire round-18 frozen | `SELFTEST_SUMMARY: 17/17 passed failed=[]` |
| measure U | `u_count 7 score 10.0` (`U1..U7`) |
| navigation | `indexed=32/32 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0 |
| census | exit 0; `mado ok …/corpus/SOURCES.md`; W04 ×3 |

Verbatim receipts from that run (paths are the clone because the receipt names
the bytes actually executed):

    RECEIPT tool=/tmp/hw-lane/tools/mado-verify.sh tool_sha256=c6cd3e78… measured_commit=23eed62f… utc=2026-10-20T15:48:15Z cwd=/tmp/hw-lane argv=bash tools/mado-verify.sh --selftest
    RECEIPT tool=/tmp/hw-lane/tools/mado-tripwire.py tool_sha256=593b3aaf… measured_commit=23eed62f… utc=2026-10-20T15:48:30Z cwd=/tmp/hw-lane argv=python3 -I /tmp/hw-lane/tools/mado-tripwire.py --selftest /tmp/hw-lane/.ufo/waves/round-18/tripwire/frozen
    RECEIPT tool=/tmp/hw-lane/.ufo/waves/round-16/measure.py tool_sha256=ea3db43f… measured_commit=23eed62f… utc=2026-10-20T15:48:31Z cwd=/tmp/hw-lane argv=python3 /tmp/hw-lane/.ufo/waves/round-16/measure.py 23eed62f…
    RECEIPT tool=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh tool_sha256=3fb72615… measured_commit=fleet:534852203d551f38c68e3a1efd26b6fbe7663267 utc=2026-10-20T15:48:31Z cwd=/tmp/hw-lane argv=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado

`harm-watch-pins.txt` records each assertion, e.g.
`PIN tools/mado-tripwire.py 23eed62… worktree=593b3aaf… rev=593b3aaf… state=ok`.

### 2.3 Edge cases exercised

| Case | Result |
|---|---|
| `--help` | prints header/usage, exit 0 |
| no REV | `harm-watch: REV is required (arg or $REV)`, exit 2 |
| unresolved REV `deadbeef` | `cannot resolve revision … `, exit 2 |
| `OUTDIR=/proc/nonexistent` | `cannot create … `, exit 2 |
| round-18/tripwire removed in clone | `NOTE tripwire root absent: …`, `HARM_WATCH: PASS`, `commands=9` |
| pin mismatch | SKIP receipt + aggregate exit 1 (§2.1) |

---

## 3. Risks and notes for L1

1. **Run it at the integrated commit with a clean tool worktree.** Any diff in
   `tools/mado-verify.sh`, `tools/mado-action-plan.py`,
   `tools/mado-tripwire.py`, or `.ufo/waves/round-16/measure.py` is a SKIP and
   exit 1 by design — that is the anti-R17-V1/V2 behaviour, not a fault.
2. **Gate R10 currently bites when the gate moves** (observed while testing):
   gate bytes `1dbbfe78…` with the old `PIN_MADO=cd1d73d7…` produced
   `MADO_SELFTEST: FAILED — 388 passed, 1 failed` and `got 20714096… want
   cd1d73d7…`. The lane has since advanced to `tools/mado-verify.sh`
   `c9fb0cef…` / `mado-tripwire.py` `c87a31ef…` and `PIN_MADO=20714096…` at
   `:1704` (15:49Z read). Harm watch will truthfully report FAIL until the
   gate's own recut is committed and its selftest is green at the measured
   commit.
3. **measure.py emits a Python 3.14 `SyntaxWarning`** (`"\."` invalid escape at
   `:41`) on stderr, interleaved before the JSON. The JSON is intact: parse
   from the first line equal to `{` through the line before `exit=`. This is a
   pre-existing cosmetic defect in the round-16 counter, not observed as a
   scoring change.
4. **Census is pinned to the fleet repo, not the lane.** Its receipt shows
   `measured_commit=fleet:<sha>`. Demanding lane REV there would be a false
   claim; the helper is not in the lane tree.
5. **Tripwire suite set is dynamic.** `round-18/tripwire/frozen` was picked up
   automatically as `harm-tripwire-round-18-frozen.txt` once TwFrozenSnapshot
   landed it; no script edit is needed for a frozen baseline or a tampered-copy
   case. An absent/empty root is a NOTE, not a failure.
6. **Receipt files are logs, not pure JSON**; `exit=` is always the last line,
   and `measured_commit=UNVERIFIED` means the command did not run. The summary
   and pins files are the quick audit.

Blockers: none. Tool installs/upgrades: none.
