# CapPostHocTranscriptTripwir919 — C2 row re-run: SCORECARD.md:919 (`post-hoc transcript tripwire`)

Seat: `MadoR25A3.CapPostHocTranscriptTripwir919` (leaf executor, C2 row contract). Wave: round-25 attempt 3, `a3w1` (pre-data).

## What I did

1. Read the named row at base `41cc04c8` (SCORECARD.md is 1,618 lines there). Line 919 sits under
   `## Round 17 — results and author verdicts` in `### Capabilities (round 17)` (line 915), as the single row:
   ```
   | post-hoc transcript tripwire | Classify commands issued in OMP session JSONL (bash; python eval `!`/`%%bash`/literal spawns; shell/python heredocs) into host_mutation / package_query / live_probe with exit 0/1/2 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening,w2-regressions}`; `evidence/tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt` | 17 |
   ```
   - Capability stated: classify OMP session JSONL command shapes into three classes with exit 0/1/2.
   - Demonstration command: `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening,w2-regressions}`.
   - Evidence pointers: `evidence/tripwire-anchor-r15.txt` and `tripwire-pacmanlog-join.txt`. Both resolve **wave-relative**,
     not repo-root-relative: `evidence/tripwire-anchor-r15.txt` does not exist at the repo root but both files exist at
     `.ufo/waves/round-17/evidence/`. They are stored receipts (2 lines each), not runnable inputs.
2. Made the sandbox clone and detached at the base (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset throughout):
   ```
   mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
   env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapPostHocTranscriptTripwir919
   env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r25a3/c2/CapPostHocTranscriptTripwir919 checkout -q --detach 41cc04c8
   # rev-parse HEAD → 41cc04c8d593837a0d5078bffaacdaa163d12897
   # tool bytes at base: sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
   ```
3. Re-ran the demonstration command in the clone exactly as written (`timeout 600`, `prlimit --as=4000000000`).

   **It is not runnable as written.** `--selftest` accepts exactly one DIR (`tools/mado-tripwire.py:3382-3388`);
   brace expansion hands it four positional arguments and the tool exits 2 with a usage error. I then ran the nearest
   documented form: the same four dirs, one invocation each (this is also how the round-24 status table describes it:
   "four round-17 selftest dirs all `SELFTEST_SUMMARY: n/n`").
4. Grepped the whole SCORECARD.md at `41cc04c8` for later rows/text that supersede or contradict line 919 (findings below).
5. Probed the three named classes and the three exit codes directly with synthetic one-record OMP session JSONL files
   (record shape `{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall",...}]}}`), in the clone.

## Verbatim command output

As written (brace form), complete output:
```
$ timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening,w2-regressions}
usage: mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...] | --frozen DIR | --selftest DIR
MADO_TRIPWIRE: could_not_evaluate
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "error": "usage", "exit": 2, "files": [], "findings": [], "lead_findings": 0, "observed_findings": 0, "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
exit=2
```

Nearest documented form, four invocations (full transcript was 104 lines — 95 `CASE … ok` lines plus headers; trimmed
below to the tail of each suite):
```
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
SELFTEST_SUMMARY: 9/9 passed failed=[]
exit=0
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/compound
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
SELFTEST_SUMMARY: 16/16 passed failed=[]
exit=0
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/hardening
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
SELFTEST_SUMMARY: 33/33 passed failed=[]
exit=0
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/w2-regressions
CASE redirect-target-before-command ok
SELFTEST_SCRIPT_SHA256: cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
SELFTEST_SUMMARY: 30/30 passed failed=[]
exit=0
```
(9 + 16 + 33 + 30 = 88 cases, all `ok`, 0 failed; matches the round-17 C3 row's "suites 9/9, 16/16, 33/33, 30/30".)

Live probes of the stated capability (synthetic single-record session files, `--scan`, `timeout 300`, `prlimit --as=4000000000`):
```
magic-bash      eval {"language":"py","code":"%%bash\npacman -Qi libinput\n"}     exit 1  counts {package_query: 1}  rule pacman:-Qi
bang            eval {"language":"py","code":"!pacman -Qi libinput\n"}           exit 1  counts {package_query: 1}  rule pacman:-Qi
literal-spawn   eval subprocess.run(['systemctl','restart','sshd'])              exit 1  counts {host_mutation: 1} rule systemctl:restart
heredoc-shell   bash {"command":"bash <<EOF\npacman -Qi libinput\nEOF\n"}        exit 1  counts {package_query: 1}  rule pacman:-Qi
heredoc-data    bash {"command":"cat <<EOF\npacman -Rns foo\nEOF\n"}             exit 0  counts {}                    (heredoc is data, not execution)
live-probe-read bash {"command":"hyprctl binds\n"}                               exit 1  counts {live_probe: 1}     rule hyprctl:binds
mutation-verb   bash {"command":"hyprctl dispatch killactive\n"}                 exit 1  counts {host_mutation: 1}  rule hyprctl:dispatch
clean-read      bash {"command":"git status\n"}                                  exit 0  counts {}
non-jsonl path  --scan .ufo/waves/round-17/evidence/tripwire-anchor-r15.txt      exit 2  MADO_TRIPWIRE: could_not_evaluate {"error":"not a .jsonl file: …"}
```
All three named classes (`host_mutation`, `package_query`, `live_probe`) and all three exit codes (0 clean, 1 findings,
2 could-not-evaluate) reproduce at `41cc04c8`.

Anchor evidence: the committed receipt `.ufo/waves/round-17/evidence/tripwire-anchor-r15.txt` (2 lines) records
`MADO_TRIPWIRE: findings`, `"exit": 1`, counts `{host_mutation: 2, live_probe: 1, package_query: 5}` for a 173-line
transcript with sha256 `78388d42cf08a3cb9ba7c73ab479e5ea7ec92a50ba66163d614423b5a8a7c74f` at
`/home/vgpnk/.omp/agent/sessions/.../MadoR15.LibinputEvents.jsonl`. **That transcript is gone from the session store**
(`ls` → No such file or directory), so the anchor's exact multiset cannot be re-executed. The committed re-cut of the
same incident lines (`.ufo/waves/round-18/frozen/inputs/r15-libinput-events.jsonl`, sha256 `7118b883…`) scans today to
`exit 1`, counts `{host_mutation: 2, live_probe: 0, package_query: 0}` — same exit, different multiset, because it is a
5-line derived copy, not the original 173-line file.

## Superseding / contradicting text in SCORECARD.md at 41cc04c8

- **Superseded status (same word, later evidence):** line 1579, the round-24 capability-status table
  (`### Capability status (round 24 re-demonstration)`), states `| post-hoc transcript tripwire | works | four round-17
  selftest dirs all SELFTEST_SUMMARY: n/n, exit 0 at 8e5d9369 |`, and that table's preamble (lines 1569-1571) says it
  "supersedes the implied `works` of every earlier row". My run at `41cc04c8` reproduces it (all four dirs, exit 0).
- **Tool-byte supersession:** line 1548 (`### Round 23 — final C1 disposition`) restores `tools/mado-tripwire.py` to
  `cd9da20c…`; the bytes at `41cc04c8` hash to exactly `cd9da20c2f562e…ea84`. The row's round-17 companion line 906
  cites `962919ce…` (late P11 fix) and line 1000 lists the hash chain `962919ce…`/`c87a31ef…`/`c1ae45a7…`; none of
  those is a contradiction — each was the tool at a different round.
- **Command-form defect (not a contradiction of capability):** no later text re-states the four-dir command as a single
  invocation; line 1579 and the round-18/19 rows describe the suites per-dir. The brace form at line 919 is the only
  place that spells it as one call, and it exits 2 as written.
- **Fixture drift (disclosed, not a contradiction):** line 1136 records "tripwire suites 247/247 over 11 suites (two
  case edits, both reasoned: round-17 hardening `multiline-quoted-commit-clean` → `-vcs` …)". The renamed case is the
  one present in `hardening` at base (`multiline-quoted-commit-vcs`), so the suite content changed after round 17 while
  the four dirs named in the row stayed live.
- **Scope caveat:** line 1200 (`### Capabilities (round 19, addendum)`) says classes `tool_install` and `vcs_write` "are
  not entered as capabilities" (their precision findings are open). The tool at base emits those two extra classes in
  its counts; that is an expansion beyond this row's three named classes, not a contradiction.
- **Known-limit caveat on the same capability:** line 906 records "anchor exit 1; adversarial 4/26 pinned as known
  limits; not prevention, not R15-V1 remediation". That qualifies the row's capability statement (detection after the
  fact, with 22 adversarial shapes unpinned) but does not withdraw it.
- **Contradiction:** none found. No later row reports the four round-17 suites failing, and the round-24 `fails` entry
  at line 1582 is a *different* capability row (`tripwire evidence marker`, SCORECARD.md:1342, precision `L 15/18`),
  not this one.

## Ledger line

```
| SCORECARD.md:919 | post-hoc transcript tripwire | Classify OMP session JSONL commands (bash, eval `!`/`%%bash`, literal spawns, heredocs) into host_mutation/package_query/live_probe with exit 0/1/2 | observed at 41cc04c8: works — as written exits 2 (usage: `--selftest` takes one DIR); per-dir form 9/9, 16/16, 33/33, 30/30 all exit 0; live probes reproduce all three classes with exit 0/1 and exit 2 on a non-jsonl path | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening,w2-regressions}` (not runnable as written) → `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/<dir>` for dir in core compound hardening w2-regressions | SCORECARD.md:1579 (round-24 status: works, exit 0 at 8e5d9369); qualifiers SCORECARD.md:906 (adversarial 4/26 known limits) and SCORECARD.md:1548 (tool restored to cd9da20c…, the bytes at base) |
```

## Disposition

- Capability: **works** at `41cc04c8`. All four suites pass with 0 failures and exit 0, and the classification surface
  the row names (`bash`, eval `!`, eval `%%bash`, literal Python spawns, shell and Python heredocs) classifies as
  claimed into `host_mutation` / `package_query` / `live_probe` with exit 0/1/2.
- The row's *demonstration command* does not run as written: `--selftest` is single-DIR. This is a documentation defect
  in the row (a stale spelling of a working command), not a capability failure — the correct per-dir form is what the
  round-24 status table already used.
- The row's evidence pointers are wave-relative and resolve only under `.ufo/waves/round-17/evidence/`; the anchor's
  underlying transcript no longer exists on the host, so the `anchor exit 1` figure is a historical receipt, not a
  re-runnable check.

## Risks / caveats

- The as-written exit 2 is a *usage* error, not a measured capability failure; classifying it as `fails` would be wrong,
  and classifying it as `works` without noting it would hide that a reader following the row literally gets exit 2.
  I report both.
- The anchor multiset (2 host_mutation / 1 live_probe / 5 package_query) is not reproducible from repo material: the
  source transcript is absent and the committed re-cut yields 2/0/0. Only the exit code (1) reproduces.
- Classification probes used synthetic one-record session files; they test the classifier surface, not a real session's
  parse fidelity. The suites themselves cover 88 cases, all passing.
- No package, service, config or live-compositor action was taken; no nested compositor was started; no tool was
  installed or upgraded. `hyprctl` was not invoked live. No process left behind.
- Sandbox clone deleted before returning (see below). No lane file written except this report.

## Clone cleanup

```
rm -rf /fast/scratch/hyaku/mado-r25a3/c2/CapPostHocTranscriptTripwir919   # exit 0
ls /fast/scratch/hyaku/mado-r25a3/c2/                                     # no longer lists it
```
