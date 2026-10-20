# TwRecutScript — R17-V1 re-cut tooling

Seat: `MadoR18.TwRecutScript` (executor). Item: R17-V1 fix tooling. Scope: one new
script plus this report. No claim was judged; no lane gate was run.

## Files changed

- `.ufo/waves/round-18/recut-receipts.sh` — new, 19,087 bytes, 478 lines, mode 0755,
  sha256 `d4a9eafd8c4f0fd247faf09ffcb281926ac5d49f73828e710fedc01e043d46ff`.
- `.ufo/waves/round-18/w1/reports/TwRecutScript.md` — this report.

Nothing else in the lane was written. `.ufo/waves/round-18/evidence/` was **not**
touched by this seat: every test used `--outdir` / `OUTDIR` pointing into `/tmp`, as
instructed. The files now in that directory are other seats' work.

No tool was installed. Host pause honoured: no pacman/yay/paru/sudo/systemctl/
loginctl/journalctl/hyprctl/libinput/walker/elephant/swaybg/hyprpaper/waybar/omarchy-*
command was run. `/var/log/pacman.log` was read as bytes only. Git in the lane was
read-only (`rev-parse`, `show`); all git writes happened inside throwaway `/tmp` clones.

## What the script does

```
recut-receipts.sh REV [--outdir DIR]        # OUTDIR=/dir recut-receipts.sh REV also works
```

- `REV` is resolved with `git rev-parse REV^{commit}`; `measured_commit` is the full hash.
- The working-tree `tools/mado-tripwire.py` sha256 is compared with the blob digest from
  a real pipeline `git -C <lane> show REV:tools/mado-tripwire.py | sha256sum`, reading
  `PIPESTATUS[0]` (git) and `PIPESTATUS[1]` (sha256sum). A failed read is refused; it is
  never digested as the empty-input sha256 `e3b0c442…`, and that digest is separately
  refused. A digest mismatch is refused. Exit 2, nothing written.
- The round-17 receipts record the scanned paths but **no command** (the R17-V1 defect).
  The script reads each receipt's `files[].path` list and re-runs
  `python3 -I tools/mado-tripwire.py --scan <paths in recorded order>` for the five
  receipts `tripwire-r13.txt`, `tripwire-r14.txt`, `tripwire-r15.txt`,
  `tripwire-r16.txt`, `tripwire-anchor-r15.txt`. No `--permit`: all old receipts record
  `"permitted": []`.
- After the scans the tool is re-digested. A mid-run change refuses and discards the
  staged receipts, so no header pins code that did not run.
- Receipts are staged in a `mktemp -d`; the pacman.log join is re-derived from the
  staged fresh receipts; `recut-summary.json` is written; only then are all seven files
  copied into `OUTDIR`. A failure therefore leaves no partial evidence.
- Receipt layout: line 1
  `RECEIPT tool=tools/mado-tripwire.py tool_sha256=<hex> measured_commit=<full hash> utc=<date -u> cmd=<exact argv>`,
  then the tool stdout verbatim, then `exit=<N>` (a non-empty tool stderr would appear
  as a `stderr:` block before `exit=`; none of the runs produced any).
- `recut-summary.json` (`schema: mado-recut-summary-v1`): per receipt the round-17 and
  re-cut verdict line, exit, counts, file count, finding multiset, permitted set, header
  check, both receipt digests and an `identical` boolean; plus `all_counts_identical`,
  `all_receipts_identical` and the join summary.
- Exit: 0 all five identical; 1 any difference (named on stderr and in the summary);
  2 refused or could-not-evaluate.
- `shellcheck -S info` and `bash -n` are clean.

The pacman.log join is re-derived by file read only: the round-17 window
(`^\[2026-10-(19T2|20T0[0-6])`) and `[PACMAN] Running` lines with a short `-S/-U/-R`
operation are parsed from `/var/log/pacman.log`; the join key is the call start from
each transcript's `custom/tool_execution_start.data.startedAt` converted UTC-3h (the
line/record timestamp is deliberately not used), matched to the log's `-0300` time.
No package manager, sudo or network call is made.

## Evidence

All test outputs below were produced by this seat; the `/tmp` trees are disposable and
the quoted lines are the retained evidence.

### E1 — refusal on a dirty working tree (exit 2, nothing written)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ .ufo/waves/round-18/recut-receipts.sh HEAD --outdir /tmp/recut-out-refuse
recut-receipts.sh: REFUSED: tool digest mismatch: working tree c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb
  != d3a00003e6ef0b1e3c7b4faf52d592eb293857ba:tools/mado-tripwire.py 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
rc=2
```

`/tmp/recut-out-refuse` does not exist. `c87a31ef…` was the in-flight sibling
(`SimplifyTripwire`) worktree at test time; HEAD `d3a0000`'s blob is `962919ce…`.

### E2 — refusal when `git show` fails (the F10 class), exit 2

```
$ .ufo/waves/round-18/recut-receipts.sh 27cd06f --outdir /tmp/recut-out-refuse2
fatal: path 'tools/mado-tripwire.py' exists on disk, but not in '27cd06f5067c3d3540ab9aa7cc734eb8eee162cc'
recut-receipts.sh: REFUSED: git show '27cd06f5067c3d3540ab9aa7cc734eb8eee162cc:tools/mado-tripwire.py' failed rc=128
  (no digest accepted; the empty-input digest e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 is never evidence)
rc=2
```

`/tmp/recut-out-refuse2` does not exist. This is precisely the
`tools/mado-verify.sh:3406` defect: the producer rc is examined instead of the empty
digest being compared as if it were content.

### E3 — positive re-cut in a /tmp clone (exit 0, all identical)

Harness `/tmp/mado-recut-lane`: `tools/mado-tripwire.py` copied from
`git show d3a0000:tools/mado-tripwire.py` (sha256
`962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`), the five round-17
receipts copied byte-identically, the script at the same relative path, committed as
`85cfd5bdd810601f4efeffcceff0ef8ea36cc852`.

```
$ /tmp/mado-recut-lane/.ufo/waves/round-18/recut-receipts.sh 85cfd5b --outdir /tmp/recut-out-final
RECUT tripwire-r13.txt         identical exit 1->1 counts {"host_mutation": 2, "live_probe": 12, "package_query": 19}->{"host_mutation": 2, "live_probe": 12, "package_query": 19}
RECUT tripwire-r14.txt         identical exit 1->1 counts {"host_mutation": 4, "live_probe": 0, "package_query": 46}->{"host_mutation": 4, "live_probe": 0, "package_query": 46}
RECUT tripwire-r15.txt         identical exit 1->1 counts {"host_mutation": 3, "live_probe": 29, "package_query": 177}->{"host_mutation": 3, "live_probe": 29, "package_query": 177}
RECUT tripwire-r16.txt         identical exit 1->1 counts {"host_mutation": 0, "live_probe": 0, "package_query": 2}->{"host_mutation": 0, "live_probe": 0, "package_query": 2}
RECUT tripwire-anchor-r15.txt  identical exit 1->1 counts {"host_mutation": 2, "live_probe": 1, "package_query": 5}->{"host_mutation": 2, "live_probe": 1, "package_query": 5}
RECUT_DONE outdir=/tmp/recut-out-final measured_commit=85cfd5bdd810601f4efeffcceff0ef8ea36cc852 tool_sha256=962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072 receipts=5 all_identical=yes
rc=0
```

Summary facts: `all_counts_identical: true`, `all_receipts_identical: true`; per
receipt `identical: true`, `receipt_header_ok: true`, run exit 1 and round-17 exit 1
(round-17 receipts carry no `exit=` line, so the verdict JSON's `exit` is used as the
fallback); file sets identical to round 17 (33, 33, 65, 97, 1) and finding multisets
identical (33, 50, 209, 2, 8). The recorded path sets equal today's on-disk sets
(checked separately): listed=33/33, 33/33, 65/65, 97/97, anchor 1/1, no unlisted
`.jsonl` in the round-13..16 subdirectories.

Receipt shape (`tripwire-anchor-r15.txt`, 4 lines):

```
1: RECEIPT tool=tools/mado-tripwire.py tool_sha256=962919ce… measured_commit=85cfd5b… utc=Tue Oct 20 15:49:46 UTC 2026 cmd=python3 -I /tmp/mado-recut-lane/tools/mado-tripwire.py --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR15/MadoR15.LibinputEvents.jsonl
2: MADO_TRIPWIRE: findings
3: {"counts": {"host_mutation": 2, "live_probe": 1, "package_query": 5}, "exit": 1, …}
4: exit=1
```

Join re-derivation (`/tmp/recut-out-final/tripwire-pacmanlog-join.txt`):

```
pacman.log:2410 01:06:49-0300 pacman -S --needed --noconfirm wayland-utils <-> MadoR13.GlobalCapture.jsonl:19 (2026-10-20T04:06:49.766Z call_2a68aff4b6984128b91f75d2) sudo + pacman:-S
pacman.log:2422 02:41:25-0300 pacman -Sw --noconfirm wlr-protocols <-> MadoR14.ReviewSourceBar.jsonl:41 (2026-10-20T05:41:25.147Z toolu_01FMx7MBA7B79Bh4sTwA7baH) sudo + pacman:-Sw
pacman.log:2423 02:41:32-0300 pacman -S --needed --noconfirm wlr-protocols <-> MadoR14.OutputSpec.jsonl:65 (2026-10-20T05:41:32.451Z 0_tool_e3c0da30-7b31-4da4-8a77-252140b90) sudo + pacman:-S
pacman.log:2429 04:25:16-0300 pacman -S --needed --noconfirm libinput libinput-tools <-> MadoR15.LibinputEvents.jsonl:54 (2026-10-20T07:25:16.905Z call_38165) sudo + pacman:-S
# unmatched transaction: pacman.log:2416 2026-10-20T01:07:12-0300 pacman -S --needed --noconfirm man-pages
# result: 4/5 mado-window package transactions joined to a tripwire host_mutation line by call start; 0 finding group(s) without a log transaction
```

This reproduces the four round-17 joins and the wave-2 correction: `OutputSpec:65`
joins at its call start `05:41:32.451Z`, not its record timestamp `05:45:52.190Z`.
`:2416 man-pages` is reported as an unmatched transaction, consistent with round-17's
note that it belongs to a sibling lane's transcript, not the scanned mado files.

### E4 — the comparison bites (exit 1)

A copy of the harness with the old `tripwire-r13.txt` counts inflated
(`host_mutation` 2 → 3) and the same tool/commit:

```
RECUT tripwire-r13.txt         DIFF exit 1->1 counts {"host_mutation": 3, "live_probe": 12, "package_query": 19}->{"host_mutation": 2, "live_probe": 12, "package_query": 19}
RECUT_DONE … all_identical=no
rc=1
```

`recut-summary.json`: `counts_identical: false`, `identical: false`,
`all_receipts_identical: false`.

### E5 — mid-run tool change (exit 2, nothing written)

A `python3` shim prepended to `PATH` appends one line to the harness tool on each call,
i.e. after the pre-scan digest check and before the post-scan one:

```
recut-receipts.sh: REFUSED: tool file changed during the re-cut (962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072 -> 0caef0785771d15cfd80f14e95b7ed21c2da99a9bb8f3c80f7df5408cd2c0a3c); receipts discarded
rc=2
```

The OUTDIR was not created.

### E6 — `OUTDIR` env override

```
$ OUTDIR=/tmp/recut-out-env /tmp/mado-recut-lane/.ufo/waves/round-18/recut-receipts.sh 85cfd5b
RECUT_DONE outdir=/tmp/recut-out-env … receipts=5 all_identical=yes
rc=0
```

### E7 — usage refusal

```
$ .ufo/waves/round-18/recut-receipts.sh
usage: recut-receipts.sh REV [--outdir DIR]   (or OUTDIR=/dir recut-receipts.sh REV)
recut-receipts.sh: REFUSED: missing REV
rc=2
```

## R17-V1 / JjAudit F10 mapping

- Every new scan receipt names the tool sha256, the full measured commit, the UTC time
  and the exact argv — the three items R17-V1 found missing.
- The receipt is produced only after `git show`'s producer rc is checked via
  `PIPESTATUS`, the empty-input digest is explicitly refused, the working-tree and blob
  digests are equal, and the tool did not change during the scans. A failed
  `git show` cannot turn into a false "local edit" digest comparison (F10).
- The unreceipted "re-cut with identical counts" claim in `lessons/round-17.md:175-176`
  is now reproducible by one command that either reproduces the counts (exit 0) or
  names the difference (exit 1), instead of a hand-run scan whose command was lost.

## Limits and risks

1. **Round-17 receipts recorded paths, not commands.** The script reconstructs argv
   from `files[].path` in recorded order (tripwire `discover()` preserves argv order,
   de-duplicating by realpath). Today that reconstruction is exactly the on-disk set
   for all five receipts; if the OMP store gains files later, the explicit list keeps
   the round-17 scope instead of silently widening it, and the summary shows a file-set
   difference. The new receipts remove this ambiguity by recording `cmd=`.
2. **Only the tool is pinned.** Transcript contents are not compared with round-17
   digests by this script (the verdict's `files[].sha256` records them). A transcript
   or classification change surfaces as exit 1 with the receipt named; the summary is
   the adjudication surface.
3. **Live-lane positive run not possible at report time.** The worktree
   `tools/mado-tripwire.py` was `c87a31ef…` (sibling `SimplifyTripwire` in flight)
   while HEAD `d3a0000`'s blob is `962919ce…`; the script correctly refuses. The
   positive path was exercised in the `/tmp` clone pinned to `962919ce…`. After
   integration, run the script at the landed commit; if that commit's tool classifies
   differently from round 17, expect exit 1 (that is the instrument doing its job, not
   a script failure).
4. `cmd=` joins argv with spaces; safe for OMP session paths (no whitespace). A path
   containing whitespace would make the header line ambiguous.
5. The join filter is the round-17 mado window plus short `-S/-U/-R` operations and
   assumes the log's `-0300` offset, as the round-17 derivation did; it is not a
   general package-log audit, and it never invokes a package manager.

## Blockers

None. Integration run for L1 (writes the real receipts only when invoked without an
override):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
./.ufo/waves/round-18/recut-receipts.sh <landed-rev>
```

Default OUTDIR is `.ufo/waves/round-18/evidence`; expect exit 0 with
`all_identical=yes` and five receipts, the pacman.log join and `recut-summary.json`;
exit 1 names the differing receipt and counts; exit 2 is a refusal (most likely the
worktree tool not matching the blob at `<landed-rev>` — the R17-V1 pin working).
