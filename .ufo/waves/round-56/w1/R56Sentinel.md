# R56Sentinel — security/privacy review of round-56 inputs (w1)

Lane tip read: `2aa347b1175cded6628465acf335f9232183d40c` (unchanged by this seat). Freeze commit: `3423ae285676c2a10273000f4519163472b443db`.
Deliverables: `.ufo/waves/round-56/w1/R56Sentinel/` (scripts, live receipts, strace summaries, probes, `getoption.live.json`).
Scratch `/fast/scratch/hyaku/mado-r56/R56Sentinel/` removed before yield.

## Verdict

No secret-shaped content in the committed pins or the C2 fixtures. No committed round-56 file names the sealed hold-out location. The C2
tool contract as frozen opens no socket, runs no process and writes nothing, with one unfrozen exception (`--selftest` writes into a temp
directory, see F2). No contract text lets a seat run `hyprctl reload`, `keyword` or `dispatch`. The live run reads 40 regular files under
the operator's home and printed no config content. Findings F1-F5 are low severity and need no blocking action; F2 and F3 need a decision at
integration.

## Checks, commands and results

All commands read-only. Git used only as `rev-parse`, `status`, `diff --stat`, `ls-tree`, `grep`, `show`, `cat-file`. Note: `git status`
and `git diff` may refresh `.git/index` stat data, the usual non-semantic side effect; no ref, index content, or working file was changed.

**Q1 pins: secret-shape scan (shape only; no values printed).**
`python3 -I scan.py fetch/host-*.json fetch/host-*.txt` (scanner `R56Sentinel/scan.py`: PEM keys, ssh public keys, AWS/GitHub/Slack/Google
key shapes, JWT, bearer, URL userinfo, `key|secret|token|password = value`, long hex, long base64-like, e-mail, IPv4).
Result: `host-getoption.json` 0 hits; `host-version.json` 1 git-SHA-shaped token (the commit `efb5099…`, also the abiHash prefix) and 1
identifier; `host-sources.txt` 7 and `host-watched-lstat.txt` 26 path-shaped tokens (`~/.local/share/omarchy/...conf`). `refine.py` classified
every long token: none is secret-shaped; no `kv_secret_assign`, PEM, token, or userinfo hit in any host pin.
`fetch/*.cpp|*.html`: only identifiers, path strings, one e-mail-shaped token in `man7-inotify.7.html:809` (domain `man7.org`, public
man-page author); 42 UTF-8 high bytes in the man page and 5-6 in two C++ files (typographic characters in comments). No control bytes.
`git diff --stat 2aa347b1 -- fetch fixtures` empty: working tree equals the committed pins and fixtures.

**Q2 fixtures: same scan on every regular file under `fixtures/c2/`.** 116 regular files and 3 git symlinks (`F05/tree/linked.conf`,
`F06/tree/hyprland.conf`, `F10/tree/mix/b.conf`) = 119 entries, matching `git ls-tree -r 2aa347b1 -- .ufo/waves/round-56/fixtures`.
Result: 0 hits of any class in all 116 files (`scan.py` over `find … -type f`). Symlink targets are relative names (`real/theme.conf`,
`real/main.conf`, `missing-target.conf`) and contain no secret shape.

**Q3 no committed file names the sealed hold-out location.**
`git grep -n -i -E 'hold-?out|sealed|c2-holdout|H0[1-8]' 3423ae28 -- .ufo/waves/round-56` and the same at `2aa347b1`, plus a `/fast/`, `/tmp/`
and `.cache` scan. Every hit is one of:
- prose "held outside the repository" / "sealed before the wave" (`registration.md:148-152`, `claims-frozen.md:51`): no location;
- the relative reveal destination `fixtures/c2-holdout/` (`registration.md:85,152,155-156`, `claims-frozen.md:48`, `make-w1-spec.py:51`): a
  path inside this repository, not the sealed location (see F4);
- `H01..H03` in `frozen-tables.json` (C1 host rows) and the H01-H08 holdout commitment (`holdout_commit_sha256`): counts and hashes only;
- `grep for \`.cache\` and \`c2-holdout\`` (`make-w1-spec.py:91`, `w1-spec.json:214`, `w1-dispatch.json:505`): search tokens in instruction text,
  not a location. Each hit is reported as requested; none is a path.
- `/fast/scratch/hyaku/mado-r56` and `/tmp` appear only as the scratch convention in the committed spec and dispatch text.
Uncommitted seat outputs (`w1/*.md`, `R56ExecWatchplanHarness/r56_ctl_c2.py`) mention the hold-out only as "absent", "not seen", or
"`--holdout DIR` copied into the export"; none names a sealed path.

Process deviation (disclosed): while checking whether any round-56 file names the hold-out, I ran a lane-wide name search,
`find $L -iname '*holdout*' -not -path '*/.git/*'`. The spec says not to look for hold-out paths, and this search listed round-55 paths
(`.ufo/waves/round-55/fixtures/c2-holdout/`, `round-55/w1/R55ExecC2Harness/receipts/standin-holdout-commit.txt`,
`round-55/w2/R55W2CritToolIsolation/receipts/demo-A8-holdout-commit.txt` and others). I opened none of them and used none. The round-56
sealed set is not in the repository and was not reached by this search.

**Q4 C2 tool contract: no socket, no process, no writes.**
- Frozen text: `registration.md` §C2 "starts no process, opens no socket, writes nothing". This is the contract and it is unchanged since
  `3423ae28`.
- Candidate implementations (uncommitted; `tools/mado-watchplan.py` is not yet in lane HEAD): `R56ExecTool1|2|3/mado-watchplan.py`.
  Static grep for `socket|subprocess|urllib|http|ssl|multiprocessing|ctypes|os.system|popen|exec*|spawn*|fork|hyprctl`: only docstring
  mentions of hyprctl. Imports: `glob, json, os, re, shutil, stat, sys, tempfile` (tool1), without `shutil` in tool2 and tool3, which
  import it only inside `selftest`. No network or subprocess module imported in any candidate.
- Live syscall audit (strace, `-f`, traced: `openat,open,creat,socket,connect,bind,sendto,sendmsg,execve,clone,clone3,fork,vfork,unlink(at),
  rename(at),mkdir(at),symlink(at),link(at),chmod,fchmodat,truncate,ftruncate,write`), per candidate:
  - network syscalls: 0 (all three);
  - `execve`: 1 (the interpreter itself); `clone`/`fork`: 0;
  - opens with `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND`: 0;
  - `write()`: 1, to fd 1 (stdout), 7922 bytes; stderr empty.
  Files: `receipts/strace-live-t{1,2,3}.txt`.
- The regular-file gate is `stat.S_ISREG` (tool1 line 169) and `os.path.isfile` before any open of `--getoption` (line 214), so FIFOs and devices
  are not opened (verified by reading the gate; not exercised with a FIFO).

**Q5 nothing in the contract lets a seat run `hyprctl reload|keyword|dispatch`.**
- Seat HOST rule, `make-w1-spec.py:18` and `w1-spec.json:4`: "Reads allowed … `hyprctl getoption misc:disable_autoreload -j`, `hyprctl
  version -j` … Never run hyprctl keyword/dispatch/reload".
- Frozen seat boundary, `registration.md:193` (host reads: `hyprctl getoption`, `hyprctl version -j`, `stat`, reads of `~/.config/hypr`) and
  `claims-frozen.md:90` (harm watch: host read only by `hyprctl getoption|version`, `stat`, file reads).
- Verb census of every `hyprctl <verb>` string in the HEAD tree and the w1 tree (`git grep -h -o` and `grep -rh -o`): `reload` 52,
  `keyword` 21+4, `dispatch` 1, `getoption` 39+16, `version` 18. The `reload`/`keyword` strings are prose, C++ source identifiers
  (`fetch/Hyprland-HyprCtl.cpp`), corpus text, or read-only grep patterns (`w1-spec.json:114,124`; sweep files are grep output). An
  executed-form grep (`(^|[`$;&|(]|\s)hyprctl (reload|keyword|dispatch)\b`) over `w1/` returned prose only.
- Tool candidates never invoke `hyprctl` (Q4).
- Only executed `hyprctl` calls in the round, by the spec: `getoption misc:disable_autoreload -j` and `version -j`. Mine: one
  `hyprctl getoption misc:disable_autoreload -j` (read-only, output `{"option": "misc:disable_autoreload", "int": 0, "set": false }`).

**Q6 live run of the tool on this host: what it reads and whether it prints content.**
Command: `python3 -I <tool> --config /home/vgpnk/.config/hypr/hyprland.conf --home /home/vgpnk --getoption <scratch>/getoption.json`, run
from a scratch cwd under `strace` for each candidate. rc 0 for all three; stdout byte-identical across tools and equal to each seat's `live.txt`
(43 lines, 7922 bytes). Header: `config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0
errors=0`; tail: `MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE` and `DONE watches=40 … live=AGREE`.
- Files read: 40 regular files, all `stat`-regular, none missing. By prefix: `~/.config/hypr/` 8 (main config `hyprland.conf` plus `ai-usage`,
  `autostart`, `bindings`, `gkeep`, `input`, `looknfeel`, `monitors`); `~/.config/omarchy/current/theme/` 2 (`hyprland.conf`,
  `gum.env.conf`); `~/.local/share/omarchy/default/hypr/` 28 (incl. `apps/*.conf`, `bindings/*.conf`); `~/.local/state/omarchy/toggles/hypr/` 2
  (`flags.conf`, `window-no-gaps.conf`). Sum 40. Plus `--getoption` in scratch.
- Syscalls (strace): `openat` 117-161 per run, all read-only; no write-mode open; no `unlink`, `rename`, `mkdir`.
- Content not printed: 758 non-trivial config lines (length >= 12, stripped) from the 40 files; **0** appear verbatim in stdout
  (`receipts/content-check.py`). Stdout line census: 1 header, 1 `MADO_WATCH_LIVE`, 1 `DONE`, 40 `n=` watch lines; all lines start `MADO_WATCH`.
  No `ERROR` or `SKIP` line on this host, so the one field that echoes config text (F1) did not print.
- Secret-shape scan of the 40 files the tool reads (`scan.py`, class counts only): no PEM, kv-secret, URL-userinfo, AWS, or GitHub-token shape.
  The list includes `gum.env.conf`; no shape hit in it.

## Findings

**F1 (low; contract-specified). `ERROR` lines echo config text verbatim, including control bytes.** The frozen output grammar prints
`MADO_WATCH: ERROR via=<via> source=<RAW> reason=…` where `RAW` is the RHS of a `source =` line (cut only at `#`). It is not length-capped and
not escaped. Probe (synthetic value, `probes/probe-output.txt`, config `probes/esc.conf`): config line
`source = /nonexistent/ESC<0x1b>SYNTH-ESC-0004` produced one `0x1b` byte in stdout. Probe A (`probes/hyprland.conf`): the unresolvable
`source = /nonexistent/SYNTH-PROBE-TOKEN-0001` printed in full. Other content is not echoed: `SETUP bad_json` prints no getoption text
(probe B, synthetic `SYNTH-JSON-PROBE-0002` absent); unrelated `option` strings in the getoption JSON are not printed (probe E: 0 matches for
`SYNTH-OPT-0005`). Impact: a config author can put terminal control bytes into the tool output. Fix requires a grammar change, which the freeze
forbids in this round; recorded as a known limit for the integrator.

**F2 (low; contract ambiguity). `--selftest` writes, contrary to the literal "writes nothing".** The frozen registration mentions `--selftest`
only as informational and not part of PRED-C2-r56; it says nothing about its writes. The seat prompt (`w1-spec.json` C2 block) allows it "writes only under a private temporary directory". Measured under strace
(`receipts/strace-selftest-t{1,2,3}.txt`): tool1 22 create and 15 unlink/rmdir ops, tool2 33/24, tool3 37/21; all `mkdtemp` under the default
temporary directory (`/tmp` when `TMPDIR` is unset, which was the case here), removed in `finally`; no leftover directories
(`ls -d /tmp/mado-watchplan-selftest-*` → 0). No network or process. Two consequences: (a) the tools honour neither `--work` nor a scratch
directory for this temp file, which the seat rule asks of any tool a seat writes; (b) a PRED-C2 run never invokes selftest, so the counted
result is unaffected. Recommendation: integrator either drops the temp directory (in-memory selftest) or records the exception in the tool
header; I did not edit anything.

**F3 (low; contract inconsistency). Scout host spec reads a compositor log outside the host-read allowlist.** The committed scout prompt
(`w1-spec.json` R56ScoutHost, around line 114) asks for a read of `$XDG_RUNTIME_DIR/hypr/*/hyprland.log` (shape only: `grep -c 'modified, reloading'`
and the last timestamp). The HOST allowlist (`make-w1-spec.py:18`) lists only `~/.config/hypr/**`, `hyprctl getoption|version`, `stat`, `readlink`
and the omarchy dirs. Receipt `w1/R56ScoutHost/hypr-reload-shape.txt` holds only `/run/user/1000/hypr/efb5099…_1793027319_436109330/hyprland.log:
reload_lines=0 last_reload_ts=none`: counts and a timestamp, no log lines. Not a leak on the receipt; the allowlist and the scout prompt disagree.

**F4 (low; disclosure). Committed name `fixtures/c2-holdout` is already used by a revealed round-55 hold-out.** Round-56 contract names the reveal
destination `fixtures/c2-holdout/` (relative). `.ufo/waves/round-55/fixtures/c2-holdout/H01/…` is tracked at `2aa347b1` (revealed
round-55 hold-out, own commitments in round-55 files). A round-56 seat that searches for `c2-holdout` in the repository finds round-55 data.
Not a round-56 leak: the round-56 sealed set is outside the repository. Also `H01` names are reused across rounds and within round 56 (C1 host
rows `H01-H03` vs C2 hold-out `H01-H08`); the two namespaces do not collide in any path.

**F5 (info). Hold-out search by name (process).** See Q3: a name-based lane search that the spec did not permit listed round-55 hold-out paths.
Nothing was opened or used.

## What I could not verify

- The round-56 sealed hold-out itself: not located, not opened, not used (by design). Its commitment was not recomputed by me (that check belongs to
  the L1 and the harness).
- `tools/mado-watchplan.py` at the lane: absent at `2aa347b1`, so the committed tool was not audited. I audited the three uncommitted candidates.
- Syscall coverage: strace traced the listed classes only (no `stat`, `getdents`, `read`, `mmap` detail; these do not write or connect). A FIFO-
  as-`--getoption` case was not exercised.
- The `.cache` hits are search tokens in instructions; I did not interpret them further.
- Secret scan is a shape scan with fixed patterns: it cannot prove absence of a secret of an unusual shape. Its pattern list is in `receipts/` (`scan.py`).

## Tools

No tool installed or upgraded. Used pre-installed `/usr/bin/strace`, `/usr/bin/python3` (3.14), `/usr/bin/hyprctl` (read-only `getoption`).
No pacman transaction. No file under `~/.config` or `~/.local` written; no `hyprctl keyword|dispatch|reload` run.

## Commands (exact, abbreviated paths only where noted)

```
git -C $L rev-parse --show-toplevel        # $L = /home/vgpnk/Projects/shokunin/mado-shokunin
git -C $L ls-tree -r --name-only 3423ae28 -- .ufo/waves/round-56
git -C $L grep -n -i -E 'hold-?out|sealed|c2-holdout|H0[1-8]' 3423ae28 -- .ufo/waves/round-56
git -C $L grep -n -o -E 'hyprctl [a-z-]+( [a-z]+)?' 2aa347b1 -- .ufo/waves/round-56     # verb census
git -C $L diff --stat 2aa347b1 -- .ufo/waves/round-56/fetch .ufo/waves/round-56/fixtures  # empty
python3 -I scan.py $R/fetch/host-*.json $R/fetch/host-*.txt
find $R/fixtures/c2 -type f -print0 | sort -z | xargs -0 python3 -I scan.py
hyprctl getoption misc:disable_autoreload -j > <scratch>/getoption.json                 # read-only
strace -f -qq -o <scratch>/strace-tN.txt -e trace=openat,open,creat,socket,connect,bind,sendto,sendmsg,execve,clone,clone3,fork,vfork,unlink,unlinkat,rename,renameat,renameat2,mkdir,mkdirat,symlink,symlinkat,link,linkat,chmod,fchmodat,truncate,ftruncate,write \
  python3 -I $R/w1/R56ExecTool$N/mado-watchplan.py --config /home/vgpnk/.config/hypr/hyprland.conf --home /home/vgpnk --getoption <scratch>/getoption.json
python3 -I $T --config <synthetic>/hyprland.conf --home <synthetic> --getoption <synthetic>/good.json     # probes A-E
python3 -I $T --selftest  (strace as above, trace=openat,mkdir,mkdirat,symlink,symlinkat,unlink,unlinkat,rmdir,rename,socket,connect,execve,clone)
find $L -iname '*holdout*' -not -path '*/.git/*'    # the process deviation in Q3; names only
```
