# ReviewProvinceTruth: C3 truth check of the PROVINCE.md tool table

Pin: `2f1134f38930fc8b067d2d7f5bba126338faabdd` (lane tip named in the assignment). Table: `PROVINCE.md` lines 24–28 (header line 22; Round-23 refinement paragraph line 20). Scope: the Reads and Writes cells of the five rows, checked against each tool's source at that commit. I did not edit the lane and ran no git or jj write verb.

**Result.** Rows 1–4 are accurate on their core Reads and Writes. They omit minor items: per-case child-process counts and self-reads of their own source. For tripwire, the omissions also include a recursive directory walk and the `--selftest DIR` reads (F6). Row 5 (`tools/mado-verify.sh`) materially understates what it reads, writes and executes, and one Writes clause is false. C3's calibration claim does not hold for row 5 as written. The presence-based counter reads 0 only because all five names are present; it does not test these cells.

## 1. Row verdicts

| Row (PROVINCE line) | Reads cell | Writes cell | Verdict |
|---|---|---|---|
| `tools/mado-action-plan.py` (24) | accurate | accurate (selftest temp dir removal verified) | Accurate. Child-count nit (F7). |
| `tools/mado-tripwire.py` (25) | understated, minor | accurate: no write call anywhere | Minor understatement (F6). |
| `tools/mado-assessment.py` (26) | accurate | accurate | Accurate. Per-case child and self-read omitted (F8). |
| `tools/mado-evidence-audit.py` (27) | accurate, including the selftest-only inventory re-hash | accurate | Accurate. Per-case child and self-read omitted (F8). |
| `tools/mado-verify.sh` (28) | materially understated (F2, F4) | materially understated; one clause false (F1, F3, F4) | Understated. Not calibrated. |

Confidence tags: [src] = read in the pinned source; [dyn] = also reproduced in a sandboxed run (section 5).

## 2. Findings

**F1 (material) [src][dyn]. verify Writes omits the `--snapshot FILE` write.**
- Source: the mode is documented at 2383–2392, and its discipline at 2411–2415 says "the snapshot write is the only write this mode makes, only to the named FILE". Argument parsing 2479–2483; a destination that exists is refused 2501–2504; the gate runs as a child, `"$bash_bin" "$MADO_R8_SELF"`, at 2506; the only guard refuses a destination inside `<root>/.config`, and only when that directory exists (2591–2603); the write is `printf '%s' "$content" >"$dest"` at 2621; a partial file is removed on a failed write or read-back (2622, 2631).
- Dynamic: with `--no-live --root <empty scratch dir> --snapshot <scratch file>` the tool wrote a 4,498-byte, 40-row file at the scratch path and left the root empty.
- The Writes cell ("no config bytes; scratch only under /tmp…") and the header (lines 22–24, "no file is written") are both wrong for this mode.
- Effect: the guard covers only `<root>/.config`. A new file can be created anywhere else the operator names, including inside the omarchy checkout that the Round-19 refinement treats as read-only evidence. An existing file is never overwritten.

**F2 (material) [src]. verify Reads and execution: "`hyprctl` read verbs only" is the only command named.**
- The hyprctl invocations are all read verbs: version, `-j instances`, configerrors, `-j getoption` (eight calls), `-j binds`, `-j monitors`, `-j layers`. The cell's list is accurate for hyprctl.
- The default run also executes these programs, none of which the cell names:
  - `omarchy version` (3781); `omarchy theme current` (3642, 3945); `omarchy commands --json --all` (3905).
  - `git -C <~/.local/share/omarchy>`: `rev-parse --git-dir` (3774), `symbolic-ref -q HEAD` (3813), `for-each-ref refs/heads` (3823), `rev-parse --verify` (3827, 3829, 3830, 3848), `describe --tags --exact-match` (3858), `show HEAD:default/omarchy-skill/SKILL.md` (3886).
  - `walker --version` (3373); `systemctl --user is-active` (3384–3385); `waybar --version` (3576); `pgrep -x` for hypridle and waybar (3545, 3587); `busctl --user get-property` (3624); `printenv` (3557, 3563).
  - `python3` heredocs and `-c` blocks, `timeout`, `readlink -f` (3726, 4008), `sha256sum` (3742, 3888), `find`.
- File reads also go beyond "declared config planes":
  - `~/.local/share/omarchy/version` and `.git` (3696, 3773); the omarchy skill link and SKILL.md (3686–3687, 3742).
  - `~/.local/state/omarchy/toggles/hypr/*` (2968, 3155); the hypr source census checks the declared `~/.local/share/omarchy/default/hypr/*.conf` (2952–2961).
  - `~/.config/mako/config` (4100); `~/.config/swayosd/style.css` (4059–4060).
  - `~/.config/omarchy/hooks`, by directory listing (3955–3957).
- The tool's own omarchy-plane comment (3666–3670) lists the omarchy and git verbs and says "Never `git status`/`fetch`". The code matches its own comment; the PROVINCE cell does not.
- Not executed by me. Read-only is the tool's own claim for these verbs; I did not check it.

**F3 (medium) [src][dyn]. verify Writes: regression scratch is not "removed unless --keep".**
- Source: the root is removed only on PASS without `--keep` (2309–2313). It is kept on FAIL (2317–2320) and on SETUP (2322–2325). Early SETUP exits after the root exists also keep it (2268, 2276, 2286).
- Dynamic: a stub harness that exits 2 gave exit code 2 and `REGRESSION_WORKDIR: /tmp/mado-verify-regression.28M0cR (kept)`. The directory kept its spec, target copy and `case/sweep.log`. I deleted it afterwards.

**F4 (medium) [src]. verify Writes and execution: `--regression` runs an external program and deletes selftest directories.**
- The harness defaults to `<fleet>/tameshi-shokunin/tools/mutate-and-run.sh` (2034–2035, 2245). The environment variable `MADO_VERIFY_HARNESS` replaces that path with any path. The tool runs it with `bash` (2150–2151). The Writes cell says the spec is "handed to tameshi's mutate-and-run.sh read-only".
- The harness runs each suite as `bash -c` with `MUTANT` exported (tameshi copy, 453–454). Mado's suite is `bash "$MUTANT" --selftest` (2292–2293), run per recorded mutant (10 entries, TABLE_MADO at 2033). So this tool's own selftest runs on each mutant copy. Each run creates `/tmp/w5-mado-m52-selftest.*` (418), which is removed only on PASS (1875). On failure the path is printed as "fixtures kept" (1881).
- After the sweep, the tool deletes every `/tmp/w5-mado-m52-selftest.*` directory that the harness evidence names (2296–2303, prefix-guarded). The Writes cell does not say so.
- The harness's own writes stay under the `--workdir` that mado passes (`$root/case/sweep`; tameshi copy 479–514, 537), so the scratch claim is right for those.
- Scenario F also deletes its own nested kept selftest directory (1376–1382). Minor.

**F5 (minor) [src]. verify header lines 22–24 claim "no file is written"; the Writes cell inherits it.** F1, F3 and F4 contradict it.

**F6 (minor) [src]. tripwire Reads and child count.**
- Not stated in the Reads cell:
  - A directory argument to `--scan` is walked recursively with `os.walk(followlinks=False)`, and every `.jsonl` below it is scanned (3016–3023). Symlinked files are refused at 3046.
  - `--selftest DIR` reads `DIR/expected.json` (3519) and runs one child per case over the fixtures under DIR (3540–3546, 3556).
  - The `--frozen` verdict includes the tool's own sha256, computed by reading its source (3189–3194, 3204). The selftest also reads its own source (3612).
- Writes/execution: "a `--selftest` child process of itself" should read "one child process per selftest case, 120 s timeout each" (3556).
- Confirmed: there is no write-mode open anywhere. The six `open` calls (3050, 3191, 3407, 3455, 3519, 3612) are reads. Output goes to stdout (3155–3157), and usage errors go to stderr (3623–3624).

**F7 (minor) [src][dyn]. action-plan child count.**
- Source: the temp directory is created at 702, writes stay inside it (711–787), and `_self_invoke` (522–529) runs at 741 (per case) and 845 (per frozen case).
- Dynamic: `--selftest` gave exit 0 and `SELFTEST_SUMMARY: 52/52 passed`, left zero entries in its private TMPDIR, and created no `__pycache__` in `tools/`.
- "Runs a copy of itself as a child process" understates the count: 52 children in this run. The Owner claim "never executes the supplied argv" holds: the only subprocess call runs the tool's own script copy.

**F8 (minor) [src]. assessment and evidence-audit: per-case child and self-read omitted.**
- Each selftest case spawns one child of the tool (assessment 194–195, timeout 10 s; evidence-audit 244–245, timeout 15 s). Each selftest also hashes the tool's own source for its output (assessment 206; evidence-audit 228).
- Otherwise accurate. Reads are bounded to 2 MiB (assessment 41–46; evidence-audit 56–66) and path checks refuse symlinks and escapes. The evidence-audit `--check` path does not re-hash the inventory (check() at 121–162). The re-hash happens only in `--selftest` (226 and 257), as the cell says.

**F9 (minor) [src]. verify: hooks listing, and the refinement's "never gating it".**
- `~/.config/omarchy/hooks` is probed by listing names (`find -maxdepth 1 -name '*.d'`, 3955–3957). No bodies are read. The Reads cell should say "names only".
- The refinement paragraph (line 20) says verify "consumes tameshi's mutate-and-run.sh read-only … never gating it". The harness's revision is indeed not gated (2257–2258, "provenance, not gated"). Its sweep table does decide the regression verdict (2290–2327), so "never gating it" needs narrowing.

## 3. Checked and found accurate (no finding)

- **Network.** None in any of the five. For the Python tools I searched for socket, urllib, http, requests, ssl, ftplib, smtplib, getaddrinfo, urlopen, curl, wget, nc and ssh, and confirmed that every subprocess call is a self-invocation of the tool. For verify.sh and the harness I also searched for ls-remote, fetch, clone, pull, push and gh. The only `curl` in action-plan is a string in a test fixture (578). The verify.sh matches are comments (3668, 3808).
- **Python write APIs.** No calls to `shutil`, `os.system`, `os.popen`, `mkdtemp`, `write_text` or `write_bytes` in any Python tool. Tripwire names `os.system`, `os.popen` and similar only as strings in its classifier tables (297–299). `tempfile` is used only in action-plan's selftest (702).
- **Write-mode opens.** Only action-plan's selftest opens files for writing, all inside its TemporaryDirectory (711–787).
- **`~/.config`.** No Python tool touches it. verify.sh reads the declared planes, and writes only inside its selftest fixture roots (`build_fixture`, called only from selftest at 643).
- **verify default and `--no-live` runs.** No shell write (redirect to a file, mkdir, cp, mv, rm, ln, chmod, touch, tee, sed -i) in lines 2639–4195, or in lines 1–415 outside `build_fixture`. The grep range selector was checked with a pattern known to match in that range (`2>/dev/null` hits at 3135–3617).
- **action-plan Reads.** Only `_read_regular` (150–181: O_NOFOLLOW, O_NONBLOCK, O_NOCTTY, regular-file-only via fstat, 16 MiB bound). It is used for policy (391), plan (395), and frozen plan, policy and expected (463, and `_load_json`).
- **tripwire Writes.** No write call of any kind.
- **hyprctl verbs.** Every invocation is a read verb.

## 4. Suggested cell text (advice to the lane owner; apply by append-only refinement)

- **verify Reads:** the file bytes of the declared config planes (hypr, waybar, walker, terminal, omarchy-theme; the mako and swayosd chain consumers; `~/.local/state/omarchy/toggles/hypr/*`); the omarchy checkout version file, `.git` metadata and HEAD blob; the skill link and SKILL.md; `~/.config/omarchy/hooks` directory names only. Executed read-only probes: `hyprctl` (version, instances, configerrors, getoption, binds, monitors, layers), `omarchy` (version, theme current, commands --json --all), `git -C <checkout>` (rev-parse, symbolic-ref, for-each-ref, describe, show), `walker --version`, `waybar --version`, `systemctl --user is-active`, `busctl --user get-property`, `pgrep -x`, `printenv`, `readlink`, `sha256sum`, `python3`. `--regression` executes the tameshi harness under bash (path from `MADO_VERIFY_HARNESS`, else the fleet default).
- **verify Writes:** nothing on the default or `--no-live` run. `--snapshot FILE` writes one new file at the named path; it refuses an existing path, and a path inside `<root>/.config` when that directory exists, and removes its file if the write or read-back fails. `--snapshot-diff` writes nothing. `--selftest` scratch is `/tmp/w5-mado-m52-selftest.*`, removed only on PASS. `--regression` scratch is `/tmp/mado-verify-regression.*`, removed only on PASS without `--keep` (kept on FAIL and SETUP). `--regression` also runs the harness, which runs this tool's `--selftest` on mutant copies, and deletes the `/tmp/w5-mado-m52-selftest.*` directories the harness names.
- **tripwire Reads (add):** a directory argument is walked recursively for `*.jsonl` (symlinks refused); `--selftest DIR` reads `DIR/expected.json` and the fixtures under it through child processes; output includes the tool's own source hash.
- **tripwire Writes:** nothing; one child process per selftest case.
- **action-plan Writes:** "…runs a copy of itself as one child process per selftest case."
- **assessment and evidence-audit:** "…one child process per selftest case; selftest output includes the tool's own source hash."
- **verify header (source file, not a PROVINCE cell):** lines 22–24 should drop "no file is written" and name the `--snapshot` and `--regression` writes.

## 5. What I ran

Exact read-only commands (the lane was not written):

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --verify 2f1134f38930fc8b067d2d7f5bba126338faabdd^{commit}
git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r --long 2f1134f38930fc8b067d2d7f5bba126338faabdd -- tools/
git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive --format=tar 2f1134f38930fc8b067d2d7f5bba126338faabdd -- PROVINCE.md tools | tar -x -C /fast/scratch/hyaku/mado-r23/ReviewProvinceTruth
sha256sum …/ReviewProvinceTruth/PROVINCE.md …/ReviewProvinceTruth/tools/*
git -C /home/vgpnk/Projects/shokunin/mado-shokunin hash-object …/tools/mado-tripwire.py …/tools/mado-verify.sh   (no -w)
```

- Sha256 of the extracted files: PROVINCE.md `78bca86d…`; mado-action-plan.py `226220ae…`; mado-assessment.py `66aefd03…`; mado-evidence-audit.py `277eced2…`; mado-tripwire.py `41489991…` (matches the registration); mado-verify.sh `050efc72…` (matches the `gate-sha256` in the dynamic snapshot).
- Blob ids from `hash-object` match `ls-tree`: tripwire `3f6e1766…`, verify.sh `9113c7c0…`.
- Source checks: the grep tool over the five extracted files, with patterns for write opens, temp APIs, subprocess and exec calls, `os` mutators, shutil, home and `~/.config` paths, network modules and tools, shell writes and external commands. I then read the enclosing code for every I/O, process-spawn and path-resolution hit I could reach, and for the sections cited in the findings. This is not a line-by-line read of any large file. tripwire (3,701 lines; its ast classifier body was not read), verify.sh (4,195 lines) and action-plan (906 lines) were checked by pattern in their unread parts. The tameshi harness was checked by pattern and at the lines cited. verify.sh was re-scanned by line range (1–415, 416–2638, 2639–4195).

Sandboxed dynamic runs. Each ran under `bash -c 'ulimit -v 393216 && …'` (384 MiB address space), in the scratch copy:

1. `TMPDIR=…/dyn/tmp-plan timeout 15 python3 -I tools/mado-action-plan.py --selftest > dyn/plan-selftest.out` → exit 0; `SELFTEST_SUMMARY: 52/52 passed`; TMPDIR empty afterwards; no `__pycache__` in tools/; wall time 1.71 s.
2. `timeout 60 bash tools/mado-verify.sh --no-live --root …/dyn/empty-root --snapshot …/dyn/snap-outside.txt > dyn/verify-snap.out` → exit 1 (DIVERGED on an empty root, expected); `MADO_SNAPSHOT: WRITTEN …/dyn/snap-outside.txt (rows=40 pass=1 fail=14 unknown=7 skip=12 note=6; scope=file-plane)`; the empty root was unchanged.
3. `MADO_VERIFY_HARNESS=…/dyn/stub-harness.sh timeout 120 bash tools/mado-verify.sh --regression > dyn/regress-stub.out`, where the stub is `#!/bin/bash` / `exit 2` → exit 2 (SETUP); `REGRESSION_WORKDIR: /tmp/mado-verify-regression.28M0cR (kept)`. I deleted that directory afterwards.

Receipts: `/fast/scratch/hyaku/mado-r23/ReviewProvinceTruth/dyn/` (`plan-selftest.out`, `verify-snap.out`, `snap-outside.txt`, `regress-stub.out`, `stub-harness.sh`). Extracts are in `/fast/scratch/hyaku/mado-r23/ReviewProvinceTruth/`, outside the lane and the fleet root.

Timeouts: runs 2 and 3 had 60 s and 120 s ceilings, not the 15 s harness cap. Both exited with their own codes (1 and 2), not 124, so neither was killed. I did not measure their wall time.

## 6. Gaps and residual risk

- **No host probes ran.** hyprctl, omarchy, git on the real checkout, walker, waybar, systemctl, busctl, pgrep and printenv are described from source only. I do not know whether omarchy, walker or waybar do I/O beyond what the source shows, including network I/O.
- **Three selftests not run.** tripwire, assessment and evidence-audit selftests were not run, because their fixture trees are not in my extract. Their no-write conclusions rest on the enumerated write APIs.
- **Regression PASS path not run.** The real mutation sweep was not run. The PASS-time removal rule is read from source (2309–2313).
- **Harness read in part; large files not read end to end.** tameshi's `mutate-and-run.sh` was read by pattern and at the cited lines. tripwire's ast classifier body, the unread parts of verify.sh, and the unread parts of action-plan were checked by pattern only. A claim about a file's unread region rests on the absence of matching I/O, process and path patterns, not on a read.

## 7. Tooling record

No installs or updates. No pacman, pip, npm, cargo or uv action. No jj command was run. No lane file was edited. This report is the only file I wrote in the lane. The `.ufo/waves/round-23/w2/` directory is untracked in the lane (`git status` shows `??`); I did not add or commit it.

## Verdict

C3 truth check: rows 1–4 are accurate on their core Reads and Writes, with minor omissions (child-process counts, self-reads of their own source, and for tripwire a directory walk and the `--selftest DIR` reads). Row 5 (`tools/mado-verify.sh`) is understated on reads, writes and executed programs, and its "removed unless --keep" clause is false. The C3 calibration claim does not hold for row 5 as written. Correct it by append-only refinement before C3 is asserted.
