# SentC1Sandbox — clause i (bwrap allowlist root) — w2 falsify

Surface: clause `i` of PRED-C1-r47 as written at `quality/counters/c1-r47-terminal.py:39-45` and
`.ufo/waves/round-47/registration.md:36`, built by `Box.argv` (`quality/counters/c1-r47-terminal.py:137-172`).
Method: a relay probe (`probe-tool.py`, sha256 `45c8543d8509bdcb9391509328c65027de941de7a5c612e67c40885cef0394aa`)
scored as `tools/mado-terminal.py` by the frozen counter itself at `d7527d6`, plus the same probe run through the
counter's own `Box`/`materialize`/`case_env`/`explain_case` so the mounts are the counter's, not a copy.

**Verdict.** The isolation the clause is *for* holds for all five named targets: the oracle tree, the pin, the
fixtures file, the lane and the host home are all unreachable (ENOENT inside). The clause's *wording* is falsified on
three counts (F1-F3) — the sandbox root is not "without /fast"; it contains `/fast/...` as a writable stub chain and
hands out host paths and the host hostname — and a tool write does reach a later counter run (F4: uncaught
`FileExistsError`, count aborted with no verdict line). No false MET is reachable. Two findings are re-registration
material before data (claim text F1-F3); F4 is a counter-robustness defect that also re-registers.

## 1. How this was produced (reproducible)

Probe scored by the real counter (probe hash above is the scored artifact; `counter-probe-full.txt`):

```
S=/fast/scratch/hyaku/mado-r47/SentC1Sandbox; L=/home/vgpnk/Projects/shokunin/mado-shokunin
D=$(mktemp -d -p $S/w2count); git clone -q --shared --no-checkout "$L" "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
cp "$L/.ufo/waves/round-47/w2/SentC1Sandbox/probe-tool.py" "$D/tools/mado-terminal.py"
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand
mkdir -p $S/w2count/work
cd "$L" && python3 -I quality/counters/c1-r47-terminal.py --repo "$D" --rev HEAD --work $S/w2count/work --nonce 47
```

Result (`counter-probe-run.txt`, exit 1): `clause=s rc=0 last='PROBE-SELFTEST-INSIDE pid1=/usr/bin/bwrap ... uid=1000
mounts=19'`, `clause=x explained=0/190`, `clause=g generated=0/150`, `clause=r trips=0`,
`fixtures=0/190 ... selftest=fail readonly=ok tool=present verdict=TARGET_MISSED rev=d489bca... nonce=47`.
The probe is not the contract tool, so the miss is expected; what it proves is that the counter's own bwrap argv ran
the probe 721 times (1 selftest + 190x2 fixtures + 190 explain + 150 generated) with `trips=0` (no exec, no socket),
and the clause-f FAIL lines carry the probe's report prefix
(`counter-probe-full.txt:3` and following). The same probe run through the counter's `Box` produced
`sandbox-probe.json` (19 mounts, root listing, env, fds, /proc, write battery); runner `run-probe.py`.

Second, independent receipt for F4 (`counter-dos-run.txt`): the same clone/commit recipe with `probe-dos.py`
(sha256 `1e6d0361e13087c7c80532e7826bcc0692e74a5ecf79548ab787008b586a3ebb`), then the same counting command.

## 2. What the tool actually sees (sandbox-probe.json)

Identity: `uid/euid/gid=1000`, `uid_map` `1000 0 1` (bwrap's nested map; host-side owner of a tool-created file is
`vgpnk:vgpnk`, so the effective host uid is 1000 — verified: `.rw/probe/marker` is `1000 1000`), `CapEff=0`,
`CapBnd=0`, `NoNewPrivs=1`, `Seccomp=0`, net ns `lo` only, cgroup ns `0::/`, **`hostname=plazir27` (host)**.

Root of the namespace, `ls /`: `bin dev fast lib lib64 oracle proc tmp usr` — plus `/usr/bin`, `/fast/scratch/...`,
and the parent chain of the case root, all as empty tmpfs stubs created by bwrap for the bind mountpoints.

19 mounts (`/proc/self/mountinfo`, verbatim rows in `sandbox-probe.json` -> `mounts`):

| mountpoint | fstype | flags | source / mount_root |
|---|---|---|---|
| `/` | tmpfs | `rw,nosuid,nodev` | bwrap root |
| `/usr/lib` | btrfs | `ro,nosuid,nodev` | `/dev/mapper/root`, `/@/usr/lib` (whole host /usr/lib) |
| `/bin/sh`, `/bin/bash` | btrfs | `ro` | host `/usr/bin/bash` |
| `/oracle/bin` | xfs | `ro` | `<work>/bin-*` (7 copies: tr find awk ls md5sum mkdir rm) |
| `/oracle/tool.py` | xfs | `ro` | `<work>/tool.py` |
| `/dev` | tmpfs | `rw,nosuid,nodev` | bwrap; `/dev/{null,zero,full,random,urandom,tty}` are **host devtmpfs** binds (`source=dev`), `/dev/core -> /proc/kcore` |
| `/dev/pts` | devpts | `rw,nosuid,noexec` | fresh instance, only `ptmx` |
| `/proc` | proc | `rw,nosuid,nodev,noexec` | fresh pid ns: pids `1` (bwrap), `2` (python) |
| `/tmp` | tmpfs | `rw,nosuid,nodev` (no `noexec`) | fresh per invocation |
| `<case root>` | xfs | `ro` | `<work>/tree/t/r` |
| `<case root>/.rw` | xfs | `rw` | same, host-backed |
| `/usr/bin/python3` | btrfs | `ro` | host `/@/usr/bin/python3.14` |

Observed inside the root (probe output): `/etc /home /root /run /var /sys /opt /srv /mnt /media /usr/share` all
ENOENT; `/bin = [bash, sh]`; `/usr = [bin, lib]`; `/usr/bin = [python3]`; `/oracle = [bin, tool.py]`; `/oracle/bin`
and `/oracle/xdg-terminal-exec` as above (the pin is **not** bound in a tool run: ENOENT); `/lib` and `/lib64` are
symlinks to `usr/lib`; `/usr/lib/os-release` readable (host distro);
`/usr/lib/python3.14/site-packages` holds 225 host entries (PySide6, PIL, ...).

Env seen by the tool = the case env exactly, plus **`PWD`**, which bwrap itself injects on `--chdir` (verified with a
bare bwrap run: `--clearenv --chdir /tmp` yields `{LANG, PWD}`) — so `--clearenv` is not literally "the case env
only", it is "the case env + PWD".

fds: `0 /dev/null`, `1,2 pipes` (the capture), nothing else. `/dev/tty` open = **ENXIO** (no controlling terminal,
`--new-session` holds); `/dev/core` open = EACCES.

Pid 1 is the bwrap supervisor, visible from inside: `/proc/1/cmdline` is the **complete bwrap argv** including the
host bind sources (`<work>/bin-*`, `<work>/tree/t/r`, the tool, `/usr/lib`, `/usr/bin/bash`), and `/proc/1/fd` shows
`0 /dev/null, 1,2 pipes, 4 anon_inode:[eventfd]`, `/proc/1/environ` = `PATH=/usr/bin`.

## 3. Reachability of the five named targets — all negative

| target | probe | result |
|---|---|---|
| oracle tree (`o/r`) | `ls` of sibling, `/oracle/xdg-terminal-exec` stat | sibling not created (`parent=['r']`, `grandparent=['t']`); pin ENOENT |
| pin (`fetch/xdg-terminal-exec`) | stat `/oracle/xdg-terminal-exec`, lane path | ENOENT / ENOENT (tool runs get `/oracle/bin` only) |
| fixtures file | stat `quality/counters/c1-r47-fixtures.json` | ENOENT |
| lane | stat of lane root, counter, `l1-draft/mado-terminal.py` | ENOENT (all three) |
| host home | `/home`, `/home/vgpnk`, `/home/vgpnk/.ssh`, `~/.config` | ENOENT; `HOME=<root>/home` |
| host /tmp, /dev/shm | host-side listing after runs | `[]` / `[]`; `/dev/shm` is a plain dir in the `/dev` tmpfs (no mount) |

## 4. Findings

### F1 — clause text falsified: `/fast` IS in the root, writable, and host paths are readable (LOW-MEDIUM, claim)
Registration says `a bwrap allowlist root without /usr/bin, /usr/share, /etc, /home, /fast`
(`registration.md:36`); docstring: `No /usr/bin,` `… /usr/share, /etc, /home, /fast, /run or /var of the host is
visible.` (`quality/counters/c1-r47-terminal.py:43-44`). Probe output (`sandbox-probe.json`):
`top=['bin','dev','fast','lib','lib64','oracle','proc','tmp','usr']`, `dirs['/fast']=['scratch']`,
`writes['fast']='WROTE'` (the tool created `/fast/probe-sentc1`), `writes['tmpfs_top']='WROTE'` (created
`/probe-sentc1` at the namespace root), `writes['parent']='WROTE'`, `writes['usr_bin']='WROTE'`.
So: no host *content* under `/fast` is bound (nothing else exists there), but the path exists, mirrors the host path of
`--work`, and is writable; and the same host path is readable as a string in `/proc/1/cmdline` and
`/proc/self/mountinfo` (`source=/dev/nvme1n1p2, mount_root=/scratch/hyaku/mado-r47/<Seat>/...`), together with
`/dev/mapper/root`, `/@/usr/lib`, `/@/usr/bin/python3.14`.
**Impact:** an isolation test written as "path X absent" fails; the tool can detect and write into a mirror of the
host layout. No capability gain (per-invocation tmpfs: a second probe run sees `top` and `/usr/bin` unchanged,
`/tmp=[]`). **Smallest remediation:** state clause i as the enumerated mount set plus "no host path outside it is
*bound*", test the mount list (fstype/source/mountpoint/`ro`) rather than path absence; optionally bind the case root
at a neutral mountpoint (e.g. `/case`) and substitute that for `$ROOT`, which removes the `/fast` chain and the
host path from file contents (mountinfo will still name the source — kernel, not fixable).

### F2 — clause-i enumeration incomplete: `/usr/bin` present and writable, `/dev` is host devtmpfs + a devpts mount (LOW)
Docstring: `fresh root holding only: /usr/lib (read-only), /bin/sh and /bin/bash = the host bash, /oracle/bin = copies`
(`quality/counters/c1-r47-terminal.py:40`). Observed extra: `/usr/bin` exists (mountpoint of the python bind) and is
writable (`writes['usr_bin']='WROTE'`), so the sentence on `:43-44` contradicts the `/usr/bin/python3` bind it grants
two lines later; `/dev/pts` is a separate `devpts` mount (`rw,nosuid,noexec`, only `ptmx`); `/dev/*` device nodes are
**host** devtmpfs binds; `/dev/core -> /proc/kcore` (open EACCES); `/lib`, `/lib64` are extra names for host
`/usr/lib`; one extra env var `PWD`. **Impact:** none for isolation beyond F1 (the extra directories are empty stubs);
it makes the clause text wrong and makes a literal reading of "only" untestable. **Remediation:** same as F1 — list
the observed set (including stub dirs, `/dev/pts`, `/dev/core`) and say which entries are host bytes.

### F3 — host identity in the root: hostname, kernel/CPU, whole host `/usr/lib` (INFO)
`hostname=plazir27` (the host UTS name is inherited; bwrap sets no `--hostname`), `/proc` (fresh pid ns) still exposes
`cpuinfo`, `meminfo`, `version`, `kallsyms` (zeroed addresses), `/dev/core`; `/usr/lib` is the full host subtree
(`site-packages` with 225 entries). No lane/home/pin bytes. **Remediation:** if host identity matters, add
`--hostname` to the argv and say in clause i that the host library tree is a declared read surface; otherwise record it
as an accepted residual.

### F4 — a tool write reaches a later counter run: `<root>/.rw/obs` aborts the count (MEDIUM, robustness)
`quality/counters/c1-r47-terminal.py:279` `os.makedirs(obs_dir)` runs **after** the tool's `explain` run, in the tool's
own tree, on a host-backed writable bind (`<root>/.rw`, xfs, `rw`). A tool that creates `<root>/.rw/obs` (it knows its
root from `XDG_CACHE_HOME`) makes that call raise. Receipts:
* imported `explain_case` (`sandbox-run.txt`): `RAISED FileExistsError ... /fx-.../t/r/.rw/obs`;
* the real counter (`counter-dos-run.txt`): traceback `main -> score:439 -> explain_case:279 -> os.makedirs(obs_dir)`,
  `FileExistsError: [Errno 17]`, exit 1, **no `PRED-C1-r47:` verdict line**.
This is the only tool-write -> later-run-read channel found (other than the designed same-tree `.rw`, which is
`XDG_CACHE_HOME` for the tool itself: write then read on the same tree = `present=True`; fresh tree = `False`; oracle
tree = `False` — `sandbox-run.txt`). **Impact:** a correct or malicious tool can abort grading after 380 fixture runs
and leave a traceback instead of a verdict; the count cannot be interpreted, and the exit code (1) is the same as a
miss. No false MET. Note the adjacent hole is only *blocked by the crash*: the counter next opens
`<root>/.rw/obs/{good,bad}` with `"wb"` (line 280-284), which would follow a symlink the tool placed under `.rw` if
the tool could get past `makedirs` — it cannot, but the ordering, not a check, is what stops it.
**Smallest remediation:** stop reading from a directory the tool can pre-create: `d = tempfile.mkdtemp(dir=rt+"/.rw")`
then `os.open(os.path.join(d,"good"), os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW, 0o600)` (same for `bad`), and
treat any `OSError` there as a clause-x failure for that fixture, not an abort. (Also worth a `try/except OSError`
around `makedirs` so a tampered tree can never crash the count.)

## 5. What is *not* a hole (checked, negative)

* The oracle never reads a tool tree and a tool never reads the oracle tree: separate roots, and the tool run does not
  bind `o/` (`parent=['r']`). Clause f's separation holds structurally.
* For the three print modes clause x uses, the oracle left `.rw/cache` **empty** (`oracle_tree_after`), which is
  consistent with the pin's `save_cache "$1" &` sitting later in the flow
  (`.ufo/waves/round-47/fetch/xdg-terminal-exec:1457`, after the print bail-out at `:1368`), i.e. the
  "cache" rationale at `quality/counters/c1-r47-terminal.py:19` (`so nothing the oracle run leaves (its cache file) is
  visible to the tool.`) describes a file these runs do not leave; the separation is still correct, just not for that
  reason.
* `/tmp`, `/dev/shm`, `/`, `/usr/bin`, `/fast/...` writes do not survive the invocation (second-run listings
  unchanged; host `/tmp`, `/dev/shm` clean), so they cannot feed a later run.
* `--new-session`: no controlling tty (`/dev/tty` ENXIO), so no host input channel.

## 6. Residuals / not tested

* No write was attempted to any existing `/proc/sys` knob (host-mutation guard); the evidence for proc/sys write
  denial is `CapEff=0`/`CapBnd=0` (the new-file attempt `ENOENT` is procfs semantics, not proof). `Seccomp=0`: the
  allowlist is mount-only; exec/socket are caught solely by clause r's strace (`trips=0` here).
* `/` and `/tmp` are mounted without `noexec`, so tool-written bytes are executable inside; only clause r guards it.
* This seat did not re-derive the pin or re-read the fixtures' `expect`; the probe's report is data produced inside the
  sandbox and is quoted verbatim from `sandbox-probe.json`.
* The `uid_map` string `1000 0 1` is a nested-userns artifact: host-side file ownership of tool-created files is
  1000:1000 (`stat` receipt above), so no host-root mapping.

## 7. Locators and receipts

Quotes with locators: `quotes.txt`; verified by `verify-quotes.sh` (grep of the receipt + grep of the source line),
output `quotes-verified.txt`. Quotes used: `registration.md:36`, `c1-r47-terminal.py:19,40,44,279`,
`fetch/xdg-terminal-exec:1457`.

Files in this seat dir: `probe-tool.py`, `probe-dos.py` (hash above), `run-probe.py`, `sandbox-probe.json`,
`sandbox-run.txt`, `counter-probe-full.txt`, `counter-probe-run.txt`, `counter-dos-full.txt`, `counter-dos-run.txt`,
`quotes.txt`, `verify-quotes.sh`, `quotes-verified.txt`.
