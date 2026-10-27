# SentHostState — operator-owned host state across round 50 (w1)

author: seat `SentHostState` (leaf, no dispatch), mado round 50 w1, 2026-10-27.
target: no writes to operator-owned host state by the round's instruments — the frozen counters, the
controls, the candidate tool and the gate — plus a fresh read-only comparison of the round-49 and
round-50 operator-state ledgers (carried item of round-49 w2, routed by the round-49 closure D1).
every receipt named here is under `receipts/` beside this file; every locator is `grep -n`/`sed -n`
computed; `~` stands for the home directory throughout; no home value beyond a digest is printed.

## Verdict

- **No ledgered operator file changed.** Four files carry the same `sha256`/`size`/`mtime` in
  r49-before, r49-after, r50-before and a fresh read taken before and after every run below
  (`receipts/ledger-compare.txt`, `receipts/fresh-state.txt`, `receipts/fresh-vs-r50-before.txt`).
- **No instrument writes home state.** One full frozen-counter run under a fake `HOME`: 3,872 write-ish
  syscalls, all resolved inside the seat scratch, fake home untouched; the tool cannot open a file for
  writing at all; the `hyprctl` read verb makes zero write syscalls (`receipts/counter-writes-confined.txt`,
  `receipts/dirfd-check.txt`, `receipts/hyprctl-readonly.txt`, `receipts/c1-frozen-counter-fakehome.txt`).
- **One prior-round host delta, unattributed:** `~/.local/bin` 106 (r49-before) → 103 (now), directory
  mtime `2026-10-27T02:20:02-03:00`, inside the round-49 w1 window; the r49-after receipt *dropped that
  line*, so the pair never recorded it (§2).
- **One instrument defect that shapes the w2 attack:** under ANY outer tracer the frozen counter reports
  a false `TARGET_MISSED` (§5). Fix belongs in `PRED-C1-r50` before the freeze.

## 1. Ledger comparison (three lane receipts + a fresh read)

| path (operator-owned) | r49-before 01:27:21 | r49-after 02:34:33 | r50-before 02:49:30 | fresh (this seat) |
|---|---|---|---|---|
| `~/.cache/xdg-terminal-exec` | `ddd94f6b…b3d5` 190 B m=1793069967 | same | same | same |
| `~/.config/hypr/input.conf` | `3769c92a…7bf4` 1584 B m=1791060272 | same | same | same |
| `~/.config/hypr/bindings.conf` | `e574a1ed…0581` 2879 B m=1791060272 | same | same | same |
| `~/.config/hypr/hyprland.conf` | `ce7483f3…f8365` 1329 B m=1792267376 | same | same | same |
| `~/.local/bin` entry count | **106** | **line absent** | **103** | **103**, dir mtime 02:20:02 |

`receipts/ledger-compare.txt` prints `identical across the three ledgers: True` per file and shows the
count line as `106 / ABSENT / 103`. `receipts/fresh-vs-r50-before.txt` prints `SAME` on all five fields.

*Changed digest: none.* Four files, four digests, zero change across round 49, the round-49 closure and the
round-50 start. The lane's own subject plane agrees: `receipts/home-window-sweep.txt` counts
`~/.config/{hypr,waybar,walker,foot,alacritty,kitty}` at 15/11/1/2/2/2 files with **0 changed since
2026-10-27T01:27:21** — no compositor config file was touched by round 49.

## 2. The one changed field: `~/.local/bin` 106 → 103

Facts (read-only): count now 103 (`ls -la | wc -l`, i.e. 100 entries), directory `mtime=ctime=1793078402`
= `2026-10-27T02:20:02-03:00`; no file *inside* the directory has an mtime in the round-49 window, so three
entries were removed, none modified (`receipts/fresh-state.txt`).

Likely writers, in the order the evidence supports:

1. **Not this lane's instruments.** §3–§4: the frozen counter's write syscalls are all under `--work`;
   the candidate tool cannot open for writing; the only live verb (`hyprctl getoption`) writes nothing.
2. **Not a `uv tool` transaction.** `~/.local/share/uv/tools` mtime `1793065330`
   (`2026-10-26T22:42:10`, before the round) and every tool receipt unchanged; a `uv tool uninstall`
   would have touched that tree at 02:20.
3. **Not any round-49 seat's own record.** Every seat that could have installed something says it did
   not: `.ufo/waves/round-49/w1/SentHost/report.md:400` ("None. Every binary used … was already present"),
   `SentPrivacy/report.md:11`, `CritRoutedItems/findings.md:7`, `RevR48/review.md:13`,
   `RevRegResiduals/review.md:15`, `ScoutShokuknow/report.md:59`.
4. **Ambient package-manager activity is the only plausible class** — and it is unattributable from lane
   evidence. Inside the same window the home cache/share trees gained mtimes in bulk:
   `uv` 11,831 files under `~/.cache`, `pnpm` 29,072 under `~/.local/share`, `chromium` 11,223 under
   `~/.cache` (`receipts/home-window-sweep.txt`). A `pnpm`/`uv` global-bin operation at 02:20 is
   consistent; the ledger recorded only a **count**, so the three names are unrecoverable now.

**Lane defect (status-neutral, routed below).** The r49-after receipt is not a like-for-like re-read: it
omits the `~/.local/bin` line entirely, so the pair cannot show the delta it was created to show; and the
round-49 closure describes the pair as "the same five digests"
(`corpus/lessons/round-49-verifier-spotcheck.md:73`) where the after file in fact holds four digests and no
count line. A count is also the wrong field: it cannot say *which* entry changed. Draft replacement line
(computed, not yet adopted — outside this seat's write scope):
`proposed-operator-state-line.txt` → `entries=100 names_sha256=70fc81cd…afdd`.

## 3. Instrument audit — every path that could write home state

| instrument | writes where (locator) | refuses | gap |
|---|---|---|---|
| `quality/counters/c1-r49-keysym.py` (frozen PRED-C1-r49) | only under `--work`: `:786` `mkdtemp(dir=work_root)`, `:406`+`:455` keymaps under it, `:790` `rmtree`; judge/compile env has `HOME` inside the work root (`:416`); sandbox env `HOME=/nonexistent` (`:543`) | `/tmp`, `/var/tmp`, `/dev/shm`, `/run`, `/proc`, `/dev`, and any work root inside the repo, the lane or the lane's parent (`:773-785`, `:786` mkdtemp, `:790` rmtree) | **accepts a work root under a home** (§3.1) |
| `quality/counters/c2-r49-bind-entry.py` (frozen PRED-C2-r49) | scratch from `TMPDIR` only (`:1029`, `:1048`); `HOME`/`XDG_*` under that scratch (`:1050-1054`) | `/tmp` and an absent `TMPDIR` (`:1029-1035`) | `TMPDIR` under a home accepted **but latent at the round-49 tip**: `score()` returns at `clause=a entry_absent` (`:1144-1149`) before clause `r` (`:1250`) reaches `tmp_root()`, so no c2 scratch was created at base; live replay needs `XDG_RUNTIME_DIR` + `HYPRLAND_INSTANCE_SIGNATURE` (`:1044`) — read verbs only, measured zero writes (`receipts/hyprctl-readonly.txt`) |
| `tools/mado-keysym.py` (candidate) | **nowhere**: imports are `base64,json,re,struct,sys,zlib,bisect` (`:98-104`) — no `os`, no `tempfile`; the only `open` is read-only (`:1665`) | n/a | none |
| `quality/check-session-material.py` (v2) and the v3 draft | selftest scratch `TMPDIR or None` (v2 `:1583`, v3 `:2078`), fixture repos + git there; request-list temp file deleted (v2 `:748`/`:781`, v3 `:975`/`:1008`) | nothing: `None` → `/tmp` | **no `/tmp` refusal** — unlike both counters (§3.2) |

### 3.1 Caller-supplied root can be a home (measured, low-medium)

`--work` pointing at a home is accepted: run against a fake home, the frozen counter returned
`verdict=TARGET_MET` and removed its own `c1r49-*` tree (residue-free on the clean path). Killed with
`SIGKILL` (`timeout -s KILL 4`, rc 137) it leaves residue **inside that home**: `c1r49-kcv1wikl/` with
`tool-*`, `judge-home`, `judge-cfg`, `keymaps`, `trace-*` (9 entries; `receipts/workroot-under-home.txt` — clean run leaves 1, the kill probe 9, both cleaned by this seat). The `finally: rmtree` cannot run after a kill,
so the guard must be at admission, not at exit.

```
$ env HOME=$FH TMPDIR=$FH python3 -I quality/counters/c1-r49-keysym.py … --work $FH --nonce 505050
  -> rc=0  verdict=TARGET_MET   fake-home entries 1 -> 1 (the counter rmtree'd its own tree)
$ env HOME=$FH TMPDIR=$FH timeout -s KILL 4 …   -> rc=137, 9 entries left: c1r49-kcv1wikl/{tool-dj70oefl,judge-home,judge-cfg,keymaps,trace-k1ei5z7p}
```
*Smallest remediation:* refuse (SETUP, rc 2) a work root under `os.path.realpath(os.path.expanduser("~"))`,
and the same for `TMPDIR` in the c2 counter and the gate. Two lines each; no behaviour change on scratch.

### 3.2 Gate has no scratch-root rule (low)

`quality/check-session-material.py:1583` (and v3 `:2078`) take `TMPDIR` or `None`; with `TMPDIR` unset the
installed gate builds its fixture git repos and its `NamedTemporaryFile` request list in `/tmp`. It never
touches home, but as the round's C2 instrument it should carry the counters' rule (require a scratch
`TMPDIR`, refuse `/tmp`), otherwise a `w2` run of the installed gate writes `/tmp` by default.

### 3.3 Doc drift in the frozen counter (low)

`quality/counters/c1-r49-keysym.py:50-52` states the `--selftest` "is documented as writing its cases under
$TMPDIR" and clause `r` excuses `/tmp`-only writes for that run (excuse call `:591`, `tmp_write` `:143`). The candidate tool has no
filesystem imports at all, so that allowance is dead code, and `tools/mado-keysym.py:23` ("Hermetic cases
under `$TMPDIR`") is wrong. Harmless today (the allowance is sandbox-`/tmp`, a fresh tmpfs) but it is a
false statement about the tool a `w2` attack will lean on; `PRED-C1-r50` should delete both.

## 4. Strace evidence (one frozen-counter run, fake home, scratch only)

```
$ S=/fast/scratch/hyaku/mado-r50/SentHostState; env HOME=$S/fakehome2 XDG_{CONFIG,CACHE,DATA,STATE}_HOME=$S/fakehome2/... \
    TMPDIR=$S/work2 python3 -I mado-shokunin/quality/counters/c1-r49-keysym.py --repo ... --rev 8ae47b9570… --work $S/work2 --nonce 505050
PRED-C1-r49 clause=f fixtures=633/633
PRED-C1-r49 clause=g generated=150/150
PRED-C1-r49 clause=r trips=0
PRED-C1-r49: fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET   (rc 0, 44 s)
```
Leader-only strace of the same run (`-e trace=open,openat,openat2,creat,mkdir,mkdirat,unlink,unlinkat,
rename,renameat,renameat2,truncate,ftruncate,symlink,symlinkat,link,linkat,mknod,mknodat,connect`):
`3872` write-ish syscalls `{mkdir:180, openat(write flags):2727, unlink:786, unlinkat:179}` → **all 3,872
resolved inside the scratch**; the 179 fd-relative `unlinkat` calls resolve, through their `openat` chain,
to `…/work3/c1r49-*/keymaps/*.xkb` (`dirfd-check.txt`: outside = 0, unresolvable = 0); the trace contains
**0** mentions of the fake home and its 4 `/home/vgpnk` mentions are `O_RDONLY` opens of the counter and its
fixture file; after exit no `c1r49-*` directory remains anywhere (`counter-writes-confined.txt`).

Bytes under measurement (read-only `git show` | `sha256sum`, and the worktree file):
`quality/counters/c1-r49-keysym.py` = `2597c204…db62` at `13631f24`, at the round-50 base `8ae47b95` and in the
worktree (absent at `03e4ae76`); `quality/counters/c1-r49-fixtures.json` = `81836bfb…e393`;
`tools/mado-keysym.py` at the base = `dcc13cce…0265`. So the run above, the round-49 receipts and a future
`PRED-C1-r50` all refer to one instrument identity.

The only live-host dependency of the round's instruments is the hyprctl read path (`PRED-C1-r50`'s live
receipt, `PRED-C2-r49` clause r): `hyprctl getoption input:resolve_binds_by_sym -j` → 0 write syscalls, one
`connect()` to the runtime socket, fake home untouched, reply `"int": 0, "set": false`
(`receipts/hyprctl-readonly.txt`). The compositor side of that socket is operator-owned; the verb set stays
inside the allowed four.

## 5. Attack finding (severity: medium) — outer tracer ⇒ FALSE `TARGET_MISSED`

Any wrapper tracer around the frozen counter makes the sandbox's `python3` never start, and the counter
reports that as a *tool* failure:

```
$ strace -f -qq -e trace=<write set> -o host-trace.txt python3 -I quality/counters/c1-r49-keysym.py --repo … --rev 8ae47b95… --work … --nonce 505050
PRED-C1-r49 clause=s selftest rc=1 last='' fail
PRED-C1-r49 clause=r trips=786 python-execve-not-seen
PRED-C1-r49: fixtures=0/633 generated=0/150 selftest=fail readonly=fail tool=present verdict=TARGET_MISSED   (rc 1)
```
Identical with `-e trace=execve` only, so it is the tracer, not the trace set. Mechanism reproduced without
the counter, in one line (`receipts/c1-outer-tracer-false-miss.txt`):

```
$ strace … strace … bwrap --unshare-all … python3 -c 'print("nested-ok")'
strace: do_test_ptrace_get_syscall_info: PTRACE_TRACEME: Operation not permitted
strace: attach: ptrace(PTRACE_SEIZE, 1232658): Operation not permitted   rc=1
$ strace … bwrap --unshare-all … python3 -c 'print("inner-ok")'
inner-ok   rc=0
```
The counter runs `strace … bwrap …` itself (clause r), so it needs to be the *only* tracer: nested ptrace is
refused and the sandbox dies before execve. Consequences for round 50: a `w2` attacker that instruments the
counter reports a false red, and an L1 that verifies with strace false-fails the frozen claim.

*Smallest remediation for `PRED-C1-r50` (and any counter that nests strace):*
1. pre-check `/proc/self/status` `TracerPid`; measured `0` untraced and non-zero under an outer strace —
   raise `Setup` (rc 2) when non-zero;
2. classify "no execve of the sandboxed python in the trace" (`:595`) as `Setup` (rc 2), never as
   `readonly=fail` + `TARGET_MISSED` — the tool's behaviour was never observed, so no verdict is available;
3. state in the docstring that the counter must not be wrapped in a tracer (a `w2` attacker needs to know
   the allowed instrumentation).

## 6. Routed items (round-50 lesson / freeze fixes; each status-neutral)

| id | finding | fix |
|---|---|---|
| R-SHS-1 | operator-state ledger is asymmetric (r49-after drops the `~/.local/bin` line) and count-only; the round-49 closure's "same five digests" (`round-49-verifier-spotcheck.md:73`) mis-describes the pair | adopt `proposed-operator-state-line.txt` (name-set digest + count), always write the same field set before/after, correct the closure wording in `corpus/lessons/round-50.md` |
| R-SHS-2 | frozen counters + gate accept a scratch root (`--work`/`TMPDIR`) under a home; SIGKILL then leaves `c1r49-*` residue there (c1 measured). c2's half is latent at base (dormant behind `clause=a`, `:1144-1149`) and becomes reachable in `PRED-C2-r50`; `SentScratch` measured it end-to-end (`TMPDIR=/var/tmp`, bwrap `--tmpfs /var/tmp`, `/var/tmp/c2r-*`, 0 left) | refuse a root under `expanduser("~")`, rc 2 (two lines per instrument); test c2 with a fixture whose HEAD carries the entry, since `clause=a` short-circuits the round-49 tip |
| R-SHS-3 | outer tracer ⇒ false `TARGET_MISSED`; the tracer is inside the counter's own tree, so wrapping it in the host guard is not a substitute for the fix. The artifact's signature is `clause=r trips=<n> python-execve-not-seen` plus `selftest rc=1 last=''` (mine: `trips=786`), and it is **not** the same reading as a legitimate scaffold miss, which reports `trips=0` with `readonly=ok` (`ExecDoNothing/receipts/c1-c02-header-only.txt`, `…c11-selftest-only.txt`) — a reader who only compares verdicts cannot tell them apart, which is the case for a `Setup` class rather than a verdict | `TracerPid` pre-check + `Setup` on a missing sandbox execve, in `PRED-C1-r50` and `PRED-C2-r50` if it nests strace |
| R-SHS-4 | gate v2/v3 write `/tmp` implicitly when `TMPDIR` is unset | require a scratch `TMPDIR`, refuse `/tmp` (same rule as the counters) |
| R-SHS-5 | `c1-r49-keysym.py:50` and `tools/mado-keysym.py:23` claim the selftest writes under `$TMPDIR`; the tool has no fs imports | delete both statements in `PRED-C1-r50`; keep the clause-r `/tmp` allowance only if a future tool writes |
| R-SHS-6 | clause `s` pins consistency but no expected total: `:664` requires `passed == total` **and** `total >= SELFTEST_MIN` (`:128`, 25), so a suite that loses cases while staying consistent still passes ([INFERENCE] from `:664` for a reduced suite; and the floor is measured being reached in practice — a 25-case
stub passes clause `s` as `selftest=ok` in `ExecDoNothing/receipts/c1-c11-selftest-only.txt`, which I read; it is
only stopped by the other clauses). The docstring at `:22` words it as `N >= 25 and N == N`, which reads as a tautology and does not describe the code — a wording defect, not a code defect | pin the exact expected total, as `ExecWaveDone/check-wave-done.py:160` does, and fix `:22`'s wording in `PRED-C1-r50`. Coupling for the mutation campaign: with clause `s` satisfiable at the floor, the answer clauses `f`/`g` carry the whole weight (the 25-case stub still reads `fixtures=0/633`, `generated=0/150`), so a weakened `f`/`g` mutant plus a floor-satisfying stub would be admitted; the exact-total pin removes that leg |

### Cross-seat corroboration (each cited file opened by this seat)

- **R-SHS-2 is cheap and now implemented independently in three other seats (verified below).** `…/w1/ExecHostGuardR50/receipts/e-refusals.txt:9`
  reads `E9_home_is_passwd_home exit=2 … refused: --home ~ resolves inside the operator home` (admission, before
  anything is created); `…/w1/ExecLiveR50/make-receipt.py` (sha256 `73b6a7eb…a36`, recomputed here) refuses
  `/home`, `/home/<account>/x`, `/root`, `/Users`, `/tmp`, `/var/tmp`, `/dev/shm` roots with rc 2 and left its
  own receipt bytes unchanged. Neither closes R-SHS-3 (they start no tracer of their own), and the host guard's
  `i-outer-tracer.txt:1-6` (`exit=0`, `ptrace_failures=0`) is exactly what makes the nested-tracer diagnosis
  specific to a counter that runs its own `strace … bwrap …`.
- **A third implementation, in the wave-done gate draft** (`…/w1/ExecWaveDone/check-wave-done.py`): `:533` refuses
  `/tmp`,`/var/tmp`,`/dev/shm` (`REFUSED_WORK_PREFIXES :156`) and `:539` refuses a root inside a home, with homes
  from **both** `$HOME` and the passwd entry (`passwd_home :491`, `home_roots :503`) and an absent/empty `HOME`
  raised as an error (`:512`); the case count is pinned (`SELFTEST_CHECKS = 58`, `:160`). Verified at digest
  `10f4359a…f818c` (47,819 B, 1018 lines): `env -u HOME … --selftest --work <home>/w1` → rc 2, nothing created;
  `HOME=<that home>` → rc 2 `refusing work dir inside the home directory`; `HOME` unset with a clean scratch root
  → rc 2 (the rule may not switch itself off); `HOME` elsewhere with a clean scratch root → rc 0, `58/58 passed`.
  The earlier revision of that gate read `HOME` only, and I measured the bypass it allowed (`env -u HOME` accepted
  a root inside a home at rc 0 **and** silently ran 53 of 55 cases, both green); that seat closed it in this
  revision, which is the strongest form of the R-SHS-2 fix any instrument in this round now carries.

- **c2's latent exposure is measured, not inferred, by `SentScratch`**: its `receipts-c2-vartmp-e2e.txt` names
  `/var/tmp/c2r-*` (7 mentions, none left after exit) and `receipts-c2-primitive.txt` shows `tmp_root()` accepting
  `/var/tmp`, `/dev/shm`, the lane root and the fleet root while refusing only `/tmp`.
- **R-SHS-5 is a self-contradiction inside one file**, so it needs no second seat: `tools/mado-keysym.py:4-5`
  says "writes no file (`--selftest` serves its keymaps from memory, so it writes nothing either)" and `:23` says
  "Hermetic cases under `$TMPDIR`". `grep -c TMPDIR tools/mado-keysym.py` = 1, that docstring line; the module
  imports no `os`/`tempfile`.


## 7. Limits of this seat

- The three removed `~/.local/bin` names are not recoverable: the ledger stored a count, not names, and the
  filesystem keeps no record. The attribution in §2 is by elimination, not by observation.
- Ambient home churn (`uv`, `pnpm`, `chromium`, other lanes' tooling) is outside this seat's instruments and
  was counted, not attributed; this host runs many agents concurrently, so mtime windows alone cannot name
  a writer for a path no instrument touched.
- `hyprctl` itself was traced, not the compositor's own writes into its runtime directory (operator-owned,
  and outside the allowed verb set to inspect).
- **c2 was audited statically, not executed**: at the round-49 tip `score()` returns at `clause=a
  entry_absent` (`:1144-1149`) before clause `r` runs, so `tmp_root()`/`live_binds()` never execute there.
  The c2 scratch/gap statements above are code-level; the end-to-end `TMPDIR=/var/tmp` measurement is
  `SentScratch`'s (`…/w1/SentScratch/receipts-c2-vartmp-e2e.txt`, `receipts-c2-primitive.txt`), cited as that
  seat's evidence, not this one's.
- Round-49 w2 never ran, so this is the first attack on the round-49 C1 freeze; per the round's rule the
  findings above are round-50 errata/fixes, not a rewrite of round-49 bytes.

## 8. Tools installed / updated

None. Everything used (`strace 7.2`, `bwrap 0.13.1`, `python3 3.14.8`, `xkbcli* 1.13.2`, `hyprctl`) was
already present; no package or tool transaction was run, and `pacman` was not invoked.

## 9. Deliverables (each `test -f`-checked before yield)

`SentHostState.md` (this file), `proposed-operator-state-line.txt`,
`receipts/{fresh-state,fresh-vs-r50-before,ledger-compare,home-window-sweep,instrument-audit,
c1-frozen-counter-fakehome,c1-outer-tracer-false-miss,counter-writes-confined,dirfd-check,
hyprctl-readonly,tool-parity,workroot-under-home}.txt`.
