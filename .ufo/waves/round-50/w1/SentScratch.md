# round-50 w1 / SentScratch — scratch containment of the round-49 frozen instruments

Seat `SentScratch` (sentinel, leaf; no subagent dispatch). Retarget of the round-49 w2 item
`.ufo/waves/round-49/w2-items.json` (`w2/SentScratch`, never dispatched — round-49 closure D1).

Targets, all at `13631f24050f22db92bf5bd33e0f4d014192992e` (lane tip when this seat ran), each file's
committed bytes verified byte-equal to the worktree before any probe
(`receipts-src-hashes.txt`):

| file | sha256 |
|---|---|
| `quality/counters/c1-r49-keysym.py` | `2597c204abf1e9e7c625d98cf83f0b340a0d82897da4986c550e35c5dff5db62` |
| `quality/counters/c2-r49-bind-entry.py` | `bc171714c5349dbe980b84f5c434126965cc8a6e8226704c28604d10cff28c69` |
| `tools/mado-keysym.py` | `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265` |

Method: read the three instruments' gate/write/cleanup code at those bytes, compute every locator with
`grep -n` (`receipts-gate-lines.txt`), then execute bounded probes from committed bytes in
`/fast/scratch/hyaku/mado-r50/SentScratch` with `HOME`/`XDG_*` pinned inside the scratch tree:
every `--work`/`TMPDIR` refusal (each with its exit code and message), a cleanup probe that exits through
`Setup` *after* the scratch tree is created, an isolated evaluation of c2's own `tmp_root()` primitive, one
end-to-end c2 run inside `bwrap` where `/var/tmp` is a tmpfs, an `strace` write audit of the tool, and two
single-line mutants of the tool scored by c1. No lane file was written; no round-50 predicate is scored
here (one full c1 run appears below only because the compliant-path probe needed a passing gate — last row of
the refusal table).

## Verdict

**c1's scratch containment is sound; c1's "read-only" clause is not.** Every `/tmp`, `/var/tmp`, `/dev/shm`,
`/run`, `/proc`, repo, lane and fleet-root work path is refused with exit 2, symlinks are resolved before the
test, and a `Setup` exit that happens after the scratch tree exists leaves 0 entries. But the clause-r
write excuse for the `--selftest` run is path-scoped to `/tmp` on the strength of a false statement in the
tool's own usage text, and a mutant tool that writes to `/tmp` during `--selftest` scores **TARGET_MET**
(S1).

**c2's scratch gate is half a gate.** It refuses `/tmp` and nothing else: `/var/tmp`, `/dev/shm`, the scored
repository, the lane and the fleet root are all accepted as replay roots, and the counter has no `--work`
argument and no repo/lane containment primitive at all (S2) — the round-48 F1 residual, minus its `/tmp`
half.

**The tool writes nothing.** 163 traced `open*` calls across `--selftest` and one `how-to-type` run, zero
carrying `O_WRONLY`/`O_RDWR`/`O_CREAT`, zero `creat`/`mkdir`/`unlink`/`rename`/`truncate`, zero `/fixture`
opens; `TMPDIR` and the scratch `HOME` stay empty; identical results with `TMPDIR` unset and `HOME=/nonexistent`.
Its usage line 23 nevertheless advertises `$TMPDIR` scratch (S3).

| instrument | refuses `/tmp` | `/var/tmp` | `/dev/shm` | host `/tmp` hardcoded | unbounded write | cleanup on `Setup` exit |
|---|---|---|---|---|---|---|
| `c1-r49-keysym.py` | yes, rc 2 | yes, rc 2 | yes, rc 2 (`/dev`) | no (sandbox `--tmpfs /tmp` only) | trace file, uncapped (S4) | yes, 0 residue |
| `c2-r49-bind-entry.py` | yes, rc 2 | **no** | **no** | no | none (5-dir tree) | yes, 0 residue |
| `tools/mado-keysym.py` | n/a (writes nothing) | n/a | n/a | none | none | n/a |

## 1. S1 — Medium — c1 clause r: a tool that writes to `/tmp` during `--selftest` scores TARGET_MET

`quality/counters/c1-r49-keysym.py:658`

```
    rc, out, _err = box.run(None, ["--selftest"], timeout=120, writes_ok=True)
```

`writes_ok=True` hands `check_trace` the excuse at `:143-147`, whose whole reach is paths under `/tmp`:

```
143:def tmp_write(rest):
147:    return bool(absolute) and all(p == "/tmp" or p.startswith("/tmp/") for p in absolute)
```

The docstring justifies it on the tool's documentation (`:50-51`): "it is documented as writing its cases
under $TMPDIR (a fresh tmpfs)". That documentation line — `tools/mado-keysym.py:23`, "Hermetic cases under
$TMPDIR" — is false: the selftest serves keymaps from an in-memory dict (`tools/mado-keysym.py:1957`) and the
tool's own header (`:4-5`) says it "writes no file".

Measured, both directions (`receipts-c1-mutants.txt`, `receipts-c1-excuse.txt`, `receipts-c1-fix-both-ways.txt`):

```
mutant-A(/tmp) rc=0 | PRED-C1-r49: fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET
  clause-r line: PRED-C1-r49 clause=r trips=0
mutant-B(/var/tmp) rc=1 | PRED-C1-r49: fixtures=633/633 ... readonly=fail tool=present verdict=TARGET_MISSED
  clause-r line: PRED-C1-r49 clause=r trips=1 write:openat(AT_FDCWD, "/var/tmp/ss-mutB", O_WRONLY|O_CREAT|O_TRUN
```

The two mutants are one injected line each inside `selftest()` in a fixture clone of the lane
(`open("/tmp/ss-mutA","w")` / `open("/var/tmp/ss-mutB","w")`); everything else is the committed tool. So the
predicate "read-only tool" is, for one of its three runs, a predicate about paths other than `/tmp`.

Impact: the freeze's clause r (`readonly=ok iff trips=0 over all runs`) can be satisfied by a write-capable
tool. No host state is at risk (the sandbox `/tmp` is a tmpfs), so this is a predicate-integrity defect, not
a containment breach — but it is exactly the property `registration.md` cites when it says the tool is
read-only.

Smallest remediation (both-ways receipt, done): drop the argument —
`box.run(None, ["--selftest"], timeout=120)` — and delete `tools/mado-keysym.py:23`. With the excuse removed
and the tool unchanged:

```
real tool @13631f24                rc=0 | ... selftest=ok readonly=ok tool=present verdict=TARGET_MET
                                   clause-r: PRED-C1-r49 clause=r trips=0
mutant-A (/tmp writer)             rc=1 | ... readonly=fail tool=present verdict=TARGET_MISSED
                                   clause-r: PRED-C1-r49 clause=r trips=1 write:openat(AT_FDCWD, "/tmp/ss-mutA", O_WRONLY|O_CREAT
```

The patched counter differs from the committed bytes by that one line (`diff` in the receipt) and was run
from a lane-shaped scratch tree so its own `lane_root()` resolves; it reads the lane read-only.

## 2. S2 — Medium — c2 refuses only `/tmp`; `/var/tmp`, `/dev/shm`, the repo and the fleet root are replay roots

`quality/counters/c2-r49-bind-entry.py:1028-1038` is the entire gate:

```
1028:def tmp_root():
1030:    t = os.environ.get("TMPDIR")
1032:        raise Setup("TMPDIR required for replay scratch")
1034:    if rp == "/tmp" or rp.startswith("/tmp/"):
1035:        raise Setup("TMPDIR under /tmp refused: %s" % rp)
1037:        raise Setup("TMPDIR is not a directory: %s" % rp)
```

Evaluated with the counter's own `tmp_root()` from committed bytes (`receipts-c2-primitive.txt`):

```
TMPDIR (unset)                 REFUSED TMPDIR required for replay scratch
TMPDIR =/tmp                   REFUSED TMPDIR under /tmp refused: /tmp
TMPDIR =/var/tmp               accepted root='/var/tmp'
TMPDIR =/dev/shm               accepted root='/dev/shm'
TMPDIR =<fleet root>           accepted root='~/Projects/shokunin'
TMPDIR =<lane root>            accepted root='~/Projects/shokunin/mado-shokunin'
TMPDIR =<symlink -> /tmp>      REFUSED TMPDIR under /tmp refused: /tmp
TMPDIR =<symlink -> /var/tmp>  accepted root='/var/tmp'
```

Symlinks are resolved (`realpath`), so the gate cannot be dodged — it is simply narrower than the rule it
claims to implement. The docstring states the gap as the contract (`:117-118`): "TMPDIR is REQUIRED and a
TMPDIR under /tmp is REFUSED".

End-to-end, without touching host `/var/tmp` — `bwrap ... --ro-bind / / --tmpfs /var/tmp` and a `strace` of
`mkdir` (`receipts-c2-vartmp-e2e.txt`):

```
counter-rc=2
PRED-C2-r49 SETUP hyprctl binds -j rc=4
mkdir lines naming a /var/tmp/c2r- path: 6
mkdir("/var/tmp/c2r-21qux6o1"
mkdir("/var/tmp/c2r-21qux6o1/home"   (+ xdg_cache_home, xdg_config_home, xdg_data_home, xdg_state_home)
tree left at /var/tmp after exit: 0
```

On this host `/var/tmp` is the root filesystem, not a tmpfs (`df -h`: `/dev/mapper/root 930G … /`), so a
`TMPDIR=/var/tmp` run writes to persistent storage with 591 G free — the ceiling the 2026-10-25 rule exists
to remove. `TMPDIR=<repo>` is the round-48 F1 residual in a sharper form: `mkdtemp(dir=<repo>)` plants
`c2r-*` inside the scored tree (transiently dirty; `finally` at `:1093` removes it — observed 0 residue and
`git status --porcelain` = 0 dirty files after the run, `receipts-c2-refusals.txt`).

Reachability caveat, measured: in the honest round-49 state the gate is **unreachable** — `score()` returns at
`clause=a entry_absent` (`:1144-1148`) before clause r ever calls `tmp_root()`. Both full-run refusals above therefore
used a fixture clone whose HEAD carries the round-49 candidate entry (entry absent at base 8ae47b95 in the
fixture: `entry-present-at-base=no`). The gate is dormant only because C1 never landed; the round-50 C1 port
makes it live again.

Smallest remediation: give c2 the c1 shape — `--work` (required) plus `under()`-based containment against
`{repo, lane_root(), dirname(lane_root())}`, the tmpfs family `/tmp`, `/var/tmp`, `/dev/shm`, and
`/run`, `/proc`, `/dev`; print the resolved replay root on the clause-r line. Until then the freeze should
quote c2's rule as "refuses `/tmp` only", not as "refuses a `/tmp` work dir".

## 3. S3 — Low — the tool's usage line advertises `$TMPDIR` scratch it does not use

`tools/mado-keysym.py:23` — "Hermetic cases under $TMPDIR" — against `:4-5` ("writes no file (`--selftest`
serves its keymaps from memory, so it writes nothing either)") and `:1957` (`files = {"/fixture/selftest-%d.kmap" …}`,
an in-memory dict). The fake `/fixture/...` paths at `:1957`/`:1964` are never opened: the trace for the
selftest has 0 opens of a `/fixture` path (`receipts-tool-writes.txt`). This line is the sole premise of S1's
excuse, so removing it is part of S1's remediation; it is a doc defect on its own because "grep hardcoded
path" now matches a path that never exists, and the tool is what other seats copy.

Measured (`receipts-tool-writes.txt`):

```
tool sha256 dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265
selftest  rc=0 last=MADO_KEYSYM_SELFTEST: 38/38 passed
          write-flag/creat/unlink/mkdir/rename/truncate lines in trace: 0 (traced opens: 81)
howto     rc=0 last=<xkbcli how-to-type output>
          write-flag/creat/unlink/mkdir/rename/truncate lines in trace: 0 (traced opens: 82)
entries left in TMPDIR=<scratch>: 0
```

A `/tmp`-mtime delta taken around the same runs caught two foreign entries (`c55-qt-596sc5f9`,
`hg-last.txt`, 03:04:19-20) created by other live seats; the strace — 0 write-flag syscalls in 163 traced
opens — is the decisive evidence, not the glob.

## 4. S4 — Low — c1's trace file is the one uncapped write (round-48 F7 carried)

`quality/counters/c1-r49-keysym.py:551` mints the trace inside `--work` and `:565` reads it back whole:

```
551:        fd, trace = tempfile.mkstemp(dir=self.work, prefix="trace-")
565:            lines = open(path, encoding="latin-1").read().splitlines()
```

No `RLIMIT_FSIZE`, no size test anywhere in either counter (`grep -E 'RLIMIT|setrlimit|st_size|getsize|resource\.'`
→ none, `receipts-caps.txt`). The bound is the caller's `ulimit -f` plus `subprocess.run(timeout=…)`; measured
size for one selftest run with the counter's own `TRACE_SET`: 8 181 B / 82 lines. Every trace is unlinked
after reading (`:596`), and all of them live under `--work`. Informational, but the freeze should not call the
trace "bounded".

## 5. S5 — Low — c1's `TMPDIR` refusal constrains a path the counter never uses

`c1-r49-keysym.py:778-780` refuses an ambient `TMPDIR` under `/tmp`, `/var/tmp`, `/dev/shm`. Measured live:
all three refused, rc 2 (`receipts-c1-refusals.txt`). But c1 never reads `TMPDIR` for scratch: all four
`tempfile` calls pass `dir=` (`:444`, `:551`, `:711`, `:786`), the judge children get a fresh env without
`TMPDIR` (`env()` at `:414-417` → `PATH`/`HOME`/`XDG_CONFIG_HOME`/`LC_ALL`), the traced child gets `env={"PATH": "/usr/bin"}`,
and the sandbox sets its own `TMPDIR=/tmp` inside `--tmpfs /tmp` (`:541-543`). So the check is a caller-hygiene
assertion, not a containment property: it cannot prevent a write, only complain. Keep it (it catches the
wave's own mistake class), but the round-50 freeze must not cite it as evidence that c1 cannot write under
`/tmp`.

## 6. S6 — Low — `--work` under `$HOME` passes the gate

The refusal set at `:772-785` is: not-a-directory, `/tmp`, `/var/tmp`, ambient `TMPDIR` family,
repo/lane/lane-parent, `/run`, `/proc`, `/dev`. `$HOME` is not in it. Executed with a work dir inside a
`$HOME` that lay in this seat's scratch (`receipts-c1-refusals.txt`):

```
work=$HOME(<scratch>/probe/home) rc=2 | PRED-C1-r49: SETUP bad rev 'deadbeef' | residue=0
```

The setup gate passed and the run died later on the bogus rev, so a real `--work ~/x` creates (and on exit
removes) scratch under the operator's home tree. This meets the letter of the seat rule (`/tmp`, `/var/tmp`,
`/dev/shm` only) and the fleet-root refusal covers the accident class, but the smallest hardening is to
require `under(work_root, "/fast/scratch")` (or refuse the operator's `HOME`) and print the resolved work
root on `clause=meta`. `finally` (`:790`) does not run on `SIGKILL`, so a home-pointed `--work` can also
*leave* `c1r49-*` behind: measured by the round-50 `SentHostState` seat, not by me — rc 137 with 9 entries
left under its fake home (`.ufo/waves/round-50/w1/SentHostState/receipts/workroot-under-home.txt`).

The same "no scratch rule" reading holds for the C2 instrument (S7 row 3): c1, c2 and the session-material
gate all accept a scratch/replay root under a home; only c1 has a `/tmp` family rule at all.

## Refusal receipts (exit code and message, executed)

`c1-r49-keysym.py`, `--repo <lane> --rev 13631f24 --nonce 1`, `TMPDIR` unset unless stated
(`receipts-c1-refusals.txt`; the `--work <lane>`/`<fleet root>` lines print the lane root because
`under()`/`lane_root()` resolve to it):

| probe | rc | message |
|---|---|---|
| `--work /tmp` | 2 | `PRED-C1-r49: SETUP work dir under /tmp (SentScratch: use a scratch filesystem)` |
| `--work /tmp/ss-nonexistent` | 2 | `PRED-C1-r49: SETUP work dir missing` (isdir precedes the path gate) |
| `--work /var/tmp` | 2 | `PRED-C1-r49: SETUP work dir under /var/tmp (SentScratch: use a scratch filesystem)` |
| `--work /dev/shm` | 2 | `PRED-C1-r49: SETUP work dir under /run, /proc or /dev` |
| `--work /run` | 2 | `PRED-C1-r49: SETUP work dir under /run, /proc or /dev` |
| `--work <symlink -> /tmp>` | 2 | `PRED-C1-r49: SETUP work dir under /tmp (SentScratch: use a scratch filesystem)` |
| `--work <lane>/corpus` | 2 | `PRED-C1-r49: SETUP work dir inside a hidden path <lane root>` |
| `--work <fleet root>` | 2 | `PRED-C1-r49: SETUP work dir inside a hidden path <lane root>` |
| `TMPDIR=/tmp` | 2 | `PRED-C1-r49: SETUP TMPDIR is under /tmp, /var/tmp or /dev/shm (…)` |
| `TMPDIR=/var/tmp` | 2 | same |
| `TMPDIR=/dev/shm` | 2 | same |
| `TMPDIR=<symlink -> /var/tmp>` | 2 | same (realpath before the test) |
| compliant `TMPDIR=<scratch>` | 0 | `PRED-C1-r49: fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` |

That last row is the only full c1 run of this seat (≈40 s): it was needed to show the gate does not
false-positive on a compliant path. Reported because it is a fact about the instrument at `13631f24`
(r49 counter still MET with a `/fast` work dir), not as a round-50 score.

`c2-r49-bind-entry.py`, fixture clone HEAD carrying the round-49 entry so clause r is reachable
(`receipts-c2-refusals.txt`):

| probe | rc | message |
|---|---|---|
| `TMPDIR` unset | 2 | `PRED-C2-r49 SETUP TMPDIR required for replay scratch` |
| `TMPDIR=/tmp` | 2 | `PRED-C2-r49 SETUP TMPDIR under /tmp refused: /tmp` |
| `TMPDIR=<symlink -> /tmp>` | 2 | `PRED-C2-r49 SETUP TMPDIR under /tmp refused: /tmp` |
| `TMPDIR=<scratch>`, bogus instance signature | 2 | `PRED-C2-r49 SETUP hyprctl binds -j rc=4` |
| `TMPDIR=<scratch>`, live read-only capture | 1 | `… clause=r replay=ok sha=9a47199e2297 binds=192 forms=named:142,code:42,mouse:6,switch:2 resolve=0` → `verdict=TARGET_MISSED` (a:1 b:0 c:0 d:0 e:0 f:1 g:1 h:1 i:0 j:0 r:1) |

## Cleanup on setup exit (executed)

| probe | before | after |
|---|---|---|
| c1, `--work <scratch>`, `--rev deadbeef` → `Setup` **after** `mkdtemp(dir=work_root)` (`:786`) | 0 | `rc=2 | PRED-C1-r49: SETUP bad rev 'deadbeef' | work entries before=0 after=0` |
| c1, counter copy outside any lane (its `lane_root()` raises) | 0 | `rc=2 | … SETUP lane root (SKILL.md/tools/quality) not found above … | work entries=0` |
| c2, `TMPDIR=<scratch>`, bogus signature → `Setup` after `mkdtemp` (`:1048`) | 0 | `scratch residue after Setup exit: 0 entries` |
| c2, live capture, normal exit | 0 | `scratch residue after normal exit: 0 entries`; fixture `git status --porcelain` = 0 |

Both counters remove their tree in `finally` (`c1:790`, `c2:1093`) with `ignore_errors=True` — the round-48
F6 class (a mode-000 directory defeats `rm -rf`/`rmtree`) is not reachable from these instruments' own
trees: c1's tree holds `tool-*`, `trace-*`, `judge-*`, `keymaps/`, `refhome-*` at default modes, c2's five
empty directories. A fixture clone this seat orphaned (375 M) was removed with plain `rm -rf`, rc 0.

## Committed code that ignores `TMPDIR` or hardcodes `/tmp` (grep, `receipts-tmpdir-inventory.txt`)

Inventory at `13631f24` over `tools/ quality/ scripts/`: 15 files mention `TMPDIR`, 18 contain a `/tmp`
literal. The three retargeted files are clean of host `/tmp` (c1/c2 use `/tmp` only as the sandbox tmpfs and
as the c2 refusal operand; the tool has no `/tmp` at all). The rest, worst first:

| path:line | what | severity |
|---|---|---|
| `quality/check-round-outcome-first.py:209` | `tempfile.mkdtemp(prefix="check96-")` — no `dir=`, so **always** host `/tmp`, while its docstring (`:48-49`) says "$TMPDIR (never /tmp by preference; tempfile honours TMPDIR)" | Medium-Low: doc contradicts code; gate ignores `TMPDIR` entirely |
| `quality/check-counter-discrimination.py:132` | default mutant root `Path(f"/tmp/mado-r36-mutants-{args.profile}")`, then written (`:148`, `:159`, `:206`, `:210`) | Medium-Low: persistent host `/tmp` writer by default |
| `quality/check-session-material.py:1583` (installed) and `.ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py:2078` (v3 draft) | `mkdtemp(prefix="csm-selftest-", dir=os.environ.get("TMPDIR") or None)` — `/tmp` when `TMPDIR` is unset | Medium: this is C2's instrument; if the round-50 selftest runs with `TMPDIR` unset it writes `/tmp` |
| `tools/mado-verify.sh:418`, `:2251` | `mktemp -d /tmp/…` hardcoded; the file never mentions `TMPDIR` | Medium-Low: lane tool, ignores `TMPDIR` by construction (cleanup is real: prefix-guarded at `:1381`, `:2296-2304`) |
| `tools/mado-terminal.py:1412` | `mkdtemp(…, dir=os.environ.get("TMPDIR") or None)` | Low: `/tmp` fallback |
| `quality/population-suite.py:283` | `for base in (TMPDIR, "/fast/scratch/hyaku/mado-r27", None)` | Low: falls back to `/tmp`; carries a stale round-27 root |
| `quality/counters/c1-r44-geometry-states-v2.py:426` (and `-states.py`) | `parent = args.work or $C1R44_TMP or None` → `mkdtemp` in `/tmp`; no `/tmp` refusal | Low: historical counter |
| `quality/counters/c2-r48-xkb-entry.py:826-828` (and `-v2`) | presence-only `TMPDIR` gate, no refusal | Low: historical counter, superseded by c2-r49 but still installed |
| `quality/check-index.py:299` | `/tmp/x` as a `--rev` operand in a negative test asserting no `/tmp/x:corpus` is created | Informational: never written |

`tools/mado-keysym.py` is the one instrument that **ignores `TMPDIR` on purpose and correctly** (S3 is only
about its usage line).

## Bounds accounting for this seat

- Scratch `/fast/scratch/hyaku/mado-r50/SentScratch`, every writer shell started `ulimit -f 65536`; peak 375 M
  (one `git clone --shared` worktree of the lane), removed at close; no `/tmp` file written by this seat (all
  `HOME`/`XDG_*` pointed inside the scratch tree; the only `/tmp` writes in the receipts are the counters'
  own sandbox tmpfs).
- Fixture repos: five `git clone -q --shared <lane> $D` under the scratch dir (c2 end-to-end refusals,
  c2 `/var/tmp` proof, c2 live capture, c1 mutants, c1 fix receipt), each with
  `git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before the first commit, all removed
  (`chmod -R u+rwX` then `rm -rf`, rc 0; one 375 M orphan from an inline probe was removed mid-session).
- Probes were bounded: every `subprocess.run` in the instruments carries `timeout=`; the longest seat command
  ran 88 s; no loop was unbounded.
- Receipts in this seat dir: `receipts-*.txt` (13 files, ≤2.5 KB each: `c1-refusals`, `c2-refusals`,
  `c2-primitive`, `c2-vartmp-e2e`, `tool-writes`, `c1-excuse`, `c1-mutants`, `c1-fix-both-ways`,
  `tmpdir-inventory`, `gate-lines`, `caps`, `src-hashes`, `host-fs`).

## Residuals

- Every counter run in this report was **unwrapped**: an outer `strace` around the frozen c1 counter makes it
  report a false `TARGET_MISSED` (its own `strace … bwrap` nesting gets `PTRACE_SEIZE: Operation not
  permitted`, so the sandboxed python never execs) — measured by the `SentHostState` seat
  (`.ufo/waves/round-50/w1/SentHostState/receipts/c1-outer-tracer-false-miss.txt`, routed as R-SHS-3). This
  seat's `strace` runs wrapped the **tool** only.
- Counter predicate correctness (fixture content, clause semantics) is other seats' surface; this seat
  attacked containment and the read-only clause only.
- The `/var/tmp` acceptance is proven through the counter's own primitive and one `bwrap` end-to-end run; the
  same acceptance for `/dev/shm` and for `TMPDIR=<repo>` is proven on the primitive only, because running them
  outside a sandbox would itself break the rule this seat audits.
- Session material in receipts is shapes and counts only (the clause-r line carries hashes and aggregate
  form counts, no raw binds JSON, titles, device names or home paths; `/home/<user>` was rewritten to `~`).
