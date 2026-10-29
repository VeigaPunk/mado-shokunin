# R56W2Sentinel — security review at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

Scope: `tools/mado-watchplan.py`, `quality/counters/c1-r56-autoreload-entry.py`, `quality/counters/c3-r56-used-by.py`, `quality/r56_ctl_c1.py`, `quality/r56_ctl_c2.py`, `quality/r56_ctl_c3.py`, `quality/check-r56-controls.py`. Scored at the committed revision (`git archive` into scratch; the working tree was not read). Leaf seat, no subagents. No lane file was written; no git mutation of the lane.

Deliverables (in this seat directory):
- `probes/` — every probe script and the committed tool copy (`mado-watchplan.at-28fc86ac.py`); `cheat_answer_key_v5.py` is the answer-key replay tool used in F1; `r56_ctl_c2_NOBWRAP_SIMULATION.py` is a copy of the C2 harness with `_BWRAP = None` (simulation of a host without bwrap).
- `receipts/` — `c1.out`, `c2.out`, `c3.out` and the stderr of each harness run at 28fc86ac; `c2-fake-holdout-H01-only.out`.

Tools: none installed. Python 3.14.8 (`/usr/bin/python3`), bwrap at `/usr/bin/bwrap`, GNU tar 1.35, git 2.56.0. No `sudo`, no pacman, no `~/.local/bin` writes. No host reads beyond the scratch tree; no Hyprland or compositor interaction.

## Verdict summary

| # | item attacked | severity | one line |
|---|---|---|---|
| F1 | C2 answer-key isolation: bwrap is the only barrier, silent fallback | blocking the C2 claim on any host without bwrap; not reproduced as a failure on this host | a replay tool that walks up from its argument paths scores 18/18 + 8/8 `TARGET_MET` when bwrap is absent |
| F2 | watchplan output injection via filenames (newline, control bytes) | weakens | a filename with `\n` forges a `MADO_WATCH: DONE` line; ESC/BEL and non-UTF-8 bytes reach stdout raw |
| F3 | unbounded event and watch output; MAX_ENTRIES caps only regular-file entries | weakens | 80 KB config, 500-dir glob: 2.5 M events, 412 MB stdout, 1.44 GB peak RSS |
| F4 | no aggregate read budget | weakens | 200 matched 1 MiB regular files: 201 paths, 24.5 s; cap admits ~256 GiB of reads (extrapolated, not run) |
| F5 | self-source chain admitted up to the cap | weakens (low) | depth 16 × 2 lines: 262143 entries, 34 MB stdout, 4.3 s; N=3 → `too_large` |
| F6 | MAX_ENTRIES `too_large` not in the docstring divergence list | weakens (disclosure) | the entry cap is a fourth `too_large` cause that the registration-v2 E8 list does not name |
| F7 | C3 harness scratch: full lane tree per control; D1 declaration is false | weakens (cost) | peak scratch 3.72 GB during the c3 run; D1 says corpus-only, 3 MB |
| F8 | text outside the display root echoed via `source =` ERROR lines | low | a token in a readable file outside the root appears in stdout |
| F9 | `--counter` / `--holdout` as arbitrary code and path inputs | by design, cosmetic | `--counter` runs an arbitrary file with user privileges, unsandboxed; `--holdout` tar-copies a tree |

Null results (clean checks, with the command that found nothing) are listed under "Checked, no defect found".

## F1 — C2 answer-key isolation depends on bwrap (blocking the claim on hosts without bwrap)

Attack: a tool that never parses a config. `probes/cheat_answer_key_v5.py` derives the fixture id (`[FH]\d\d`) from its argv, walks up from its cwd and from its absolute arguments, finds `expected.out` and `expected.rc` under the export in `--work`, and replays them.

Commands and output (the cheat tool committed at a scratch clone, then run through the harness):

```
python3 -I ex/quality/check-r56-controls.py --claim c2 --repo <scratch clone of cheat> --rev db3dbfcac233619f549bcf358ca85c3c2c460e79 --work <w>/cheat5bw
MADO_R56_C2: rev=db3dbfcac233619f549bcf358ca85c3c2c460e79 fixtures=0/18 holdout=0/8 holdout_commit=ok controls=4/4 verdict=TARGET_MISSED     (rc=1; bwrap present at /usr/bin/bwrap)

python3 -I probes/r56_ctl_c2_NOBWRAP_SIMULATION.py --repo <scratch clone of cheat> --rev db3dbfcac233619f549bcf358ca85c3c2c460e79 --work <w>/cheat5nb
MADO_R56_C2: rev=db3dbfcac233619f549bcf358ca85c3c2c460e79 fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET     (rc=0)
```

Earlier variants: v3 (derive id, look in `fixtures/c2` under the args' ancestors) and v4 (also `.ufo/waves/round-56/fixtures/c2`) scored 0/18 with bwrap and 15/18 + 7/8 without it.

The no-bwrap run is a simulation: a copy of the harness with `_BWRAP = None`, which drives the fallback branch `run_program(...)`. I did not hide bwrap on the host. On a host where `shutil.which("bwrap", path=SAFE_PATH)` is None, the harness falls back silently to an unsandboxed run, prints nothing about the mode, and the replay tool reaches TARGET_MET.

Why the layout fails. registration-v2 E6 says expected bytes live only in the harness process memory, and that the stage cwd is not an ancestor of the export or of any `expected.*`. The harness exports to `ex = mkdtemp(dir=work)` and stages each run at `work/stage-N/<id>` with cwd `work/cwd-N`. A tool that walks up from its argument path reaches `work`, which contains `c2-export-*/fixtures/c2/F*/expected.out`. The letter of E6 holds (nothing named `expected.*` under `<work>/run`, `<work>/cwd` or `<work>/tool`); its intent does not, because the answer key sits one directory above the stage.

With bwrap the replay fails. bwrap binds only the stage and the tool; its ancestor directories are empty mount points, so the export is invisible (`probes/probe_bwrap2.py`: `key blocked`; listing of the parent shows only `probe.py` and `stage-1`). Under bwrap, v3, v4 and v5 all score 0/18.

Severity: blocking the C2 claim on any host without bwrap, because the harness then certifies a replay as operability. Not reproduced as a failure on this host. Smallest remediation: (a) fail closed with a setup error when bwrap is absent rather than falling back; (b) place the export outside every ancestor of the stage (a sibling mkdtemp, not under `--work`), or remove `expected.*` from the export before the staged runs; (c) print the sandbox mode on stderr.

## F2 — watchplan output injection through filenames (weakens)

Attack: a file name containing a newline, ANSI escapes or BEL, or non-UTF-8 bytes, matched by a `source =` glob. The tool prints the path verbatim (`show()`, and `.encode("utf-8","surrogateescape")` in `main()`).

Commands and output:

```
probes/probe_inject3.py   (name = "bad\nMADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE\nx.conf", source = *.conf)
MADO_WATCH: config=$ROOT/hyprland.conf autoreload=off disable_autoreload=1 paths=35 unsupported=2 errors=0
MADO_WATCH: DONE watches=0 unsupported=2 errors=0 live=NONE          <- a forged DONE line; the real DONE follows at the end

probes/probe_inject4.py   (same name, file content "x = 1", autoreload stays on)
MADO_WATCH: n=2 role=primary path=$ROOT/bad
MADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE
x.conf type=file mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=$ROOT/hyprland.conf:1

probes/probe_ansi.py   (name "a\x1b[31mRED\x1b[0m\x07b.conf")
... path=$ROOT/a\x1b[31mRED\x1b[0m\x07b.conf ...          (raw ESC and BEL bytes on stdout)

probes/probe_nonutf8b.py / probes/probe_nu3.py   (name b"sec-\xff\xfe-retweird.conf")
... path=.../sec-\xff\xfe-retweird.conf type=file ...      (raw bytes on stdout)
```

Consequence: a file name forges `MADO_WATCH` lines; a consumer that reads "the DONE line" or counts lines gets the wrong value. The C2 harness compares bytes, but no committed fixture uses odd names, so it cannot catch this. Severity: weakens. Smallest remediation: escape control bytes and newlines in every printed path (`\n`, `\x1b`, `\xff`) so each record stays one line.

## F3 — unbounded event and watch output (weakens)

Attack: `MAX_ENTRIES` (262144) bounds only regular-file entries. SKIP and ERROR events and the watch lines are never counted. A glob over a directory of subdirectories, repeated over many source lines, multiplies output.

Commands and output:

```
probes/probe_rss.py: config 80000 bytes (5000 × "source = wide/*"), wide/ = 500 subdirectories
rc=0 elapsed=12.0s stdout=411.9 MB peak_child_RSS=1442 MB; SKIP events: 2500000
probes/probe_events.py (20000 dirs, 5000 lines): rc=0 elapsed=12.82s stdout=211.9 MB peak_child_RSS=878.2 MB events=2500000
probes/probe_events2.py (200 dirs, 5000 lines): stdout 84.8 MB, 1000000 SKIP events, 3.5 s
```

RSS grows with the number of events, not with the input size. Severity: weakens (local operator tool; a config or a directory tree the operator does not control can exhaust memory). Smallest remediation: count events and watch lines against a budget and fail with `too_large`, as for entries, or cap matches per source line.

## F4 — no aggregate read budget (weakens)

Attack: `source = dir/*` where `dir` holds many regular files, each just under 1 MiB. Each match is parsed (`parse_file`) and read up to `MAX_BYTES`. No total byte or time budget exists; cost is files × 1 MiB, bounded only by the 262144-entry cap.

Measured: 200 regular files of 1048000 bytes each, one source glob: `rc=0 elapsed=24.55s paths=201`. Extrapolated (not run): 262144 files means about 256 GiB of reads, bounded only by the cap. Severity: weakens. Smallest remediation: a total-bytes budget for the whole run, failing with `too_large`.

## F5 — self-sourcing chain (weakens, low)

Attack: `source = hyprland.conf` repeated. Depth 16 with two lines gives 2^16 chains.

Measured: `N=2`: `rc=0 elapsed=4.27s stdout=33967657 bytes`, `paths=262143 unsupported=131072`. `N=3`: `SETUP too_large` in 2.40 s. Bounded, but a 36-byte config admits 34 MB of output and 4 s of CPU. Severity: weakens (low). Same remediation as F3.

## F6 — MAX_ENTRIES `too_large` not in the docstring divergence list (weakens, disclosure)

The code comment says "Defensive cap, not in the registration", and it reports the same string `too_large` that registration-v2 defines as "any file the tool reads larger than 1048576 bytes". The divergence list in the docstring (registration-v2 E8, seven items) does not name the entry cap. Severity: weakens (disclosure gap, not an exploit). Smallest remediation: add the entry cap to the docstring divergence list.

## F7 — C3 harness scratch cost; the D1 declaration is false (weakens, cost)

`r56_ctl_c3.py` declares D1: "the scratch repo is built from `git archive REV -- corpus .ufo/waves/round-56/frozen-tables.json` (3 MB), not from the whole 389 MB". The code does not do that. `build_scratch()` runs `git clone --shared --no-checkout`, then `git checkout --detach rev_sha`, which materialises the whole lane tree (measured at 28fc86ac: 27734 files, 365635795 bytes = 348.7 MB). Every control clone is kept until the `finally` at the end of `execute()`, so all of them coexist.

Measured (`du -sm` every 5 s during `--claim c3`, same command as `receipts/c3.out`):

```
t=5s 149MB; t=30s 1281MB; t=60s 2366MB; t=90s 3722MB (peak, 11 top-level dirs); t=130s 0MB
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK     (Wall time 142.17 s)
```

Severity: weakens (cost, and a mis-stated declaration; a larger lane would need tens of GB of scratch). Smallest remediation: `git archive` the paths the counter reads, or a sparse checkout, and remove each clone right after its run.

## F8 — echo of text outside the display root (low)

The `source =` RAW string is printed in ERROR lines. The tool reads any readable regular file the source chain reaches, so a `source =` line inside a file outside the root is echoed.

```
probes/probe_content.py (secret2.conf inside the tree, value SUPERSECRETVALUE-abc123): SECRET in stdout? True
probes/probe_content.py (notes.txt outside the root, content "source = TOKEN-XYZ-outside-root"):
MADO_WATCH: ERROR via=.../p4/outside/notes.txt:1 source=TOKEN-XYZ-outside-root reason=nomatch
```

Only the RHS of lines whose key is `source` is echoed, so the exposure is narrow. Severity: low. Remediation: print RAW only for `bogus` and `nomatch` errors on lines of the config tree, or drop RAW from ERROR lines for files outside the root.

## F9 — harness inputs as code and path (by design, cosmetic)

- `--counter PATH` (`r56_ctl_c1.py` around line 552; `r56_ctl_c3.py` `execute()`) copies and runs the named file as `python3 -I` with the user's privileges and no sandbox. This is the stated purpose (the counter under test) and the operator supplies it.
- `--holdout DIR` (`r56_ctl_c2.py`) tar-copies DIR into the export with symlinks preserved. Tested: a crafted tar that stores symlink `a -> victim` followed by `a/secret.txt` (`tt3`): GNU tar 1.35 refused (`Cannot open: Not a directory`, rc 2) and `victim/secret.txt` was unchanged. Not run: other tar implementations, and a hold-out tree with absolute symlinks (under bwrap these are not visible; under the no-bwrap fallback the staged tool could read a link target; the tool prints no content of regular files, so the exposure is limited to F8).
- Cosmetic: the C1 and C3 harnesses create `--work` and leave it in place (empty) after a run; their subtrees are removed.

## Checked, no defect found

- No `shell=True`, `os.system`, `os.popen`, `exec` or `call` in the seven artifacts: `grep -n "shell=True\|os\.system\|os\.popen\|subprocess\.call\|exec("` over the seven files returns nothing. Every subprocess call is an argv list.
- FIFO or device as a glob match: `probes/probe_fifo2.py` with `source = *.*` over a FIFO and `/dev/zero`, `/dev/null` symlinks: `rc=0 elapsed=0.08s`; the FIFO and devices are `SKIP reason=nonregular`; no hang. FIFO or device as `--config`: `rc=0`, no hang. FIFO as `--getoption`: `SETUP unreadable`, rc 2, no hang.
- Symlink to a device as `--config` (`/dev/zero`): canonical watch on `/dev/zero` is listed; nothing is read from it (not regular, not parsed).
- Path traversal: `source = ../../...` resolves by the registered `absolutePath` (`probes/probe_paths35.py`); only regular files are read; the tool writes nothing.
- `--selftest`: `MADO_WATCH_SELFTEST` `82/82 assertions passed`, rc 0 (under scratch TMPDIR).
- MAX_BYTES: selftest accepts exactly 1048576 bytes and rejects 1048577 with `too_large`; a three-line self-source is `too_large` (F5).
- Non-UTF-8 config bytes decode with replacement and do not crash (`probes/probe_nonutf8.py`; selftest "non-utf8 bytes").
- Scratch cleanup: after the C2 run no `c2-export-*` or `stage-*` remain; after the C1 run `work/c1` is empty (`find work/c1 -mindepth 1` returns nothing).
- Harness results at 28fc86ac (receipts): C1 `MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK`; C2 `MADO_R56_C2: ... fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET` (`receipts/c2.out`); C3 `good=ok controls=9/9 verdict=OK`. Fake hold-out (only `H01` present, same shape, wrong bytes): `holdout=0/8 holdout_commit=bad verdict=TARGET_MISSED` (`receipts/c2-fake-holdout-H01-only.out`).
- Dispatcher: `--claim bogus` prints `MADO_R56_CONTROLS: SETUP usage` on stdout with rc 2. The usage text differs from the harnesses' stderr setup messages (cosmetic).
- Lane integrity: `git rev-parse 28fc86ac…^{tree}` still `d83d2ebe…`; `git fsck --connectivity-only` reports only dangling objects; the lane's working tree has modified and untracked entries that I did not create (I wrote nothing into the lane).

## Could not verify

- The no-bwrap path on a host without bwrap (F1 is a simulation by patching `_BWRAP`).
- F4's 256 GiB figure is an extrapolation; the 200-file measurement is the observed number.
- F8 with absolute symlinks in a `--holdout` tree (not run).
- The FIFO TOCTOU race (`stat` then `open` in `read_limited`): a file swapped to a FIFO between the check and the open would block. Not reproduced; theoretical for an operator-owned config tree.
- Other tar implementations under the `--holdout` path.
- Whether any real host config reaches the fan-out scales in F3–F5 (the probes are synthetic).

## Tools installed or updated

None.
