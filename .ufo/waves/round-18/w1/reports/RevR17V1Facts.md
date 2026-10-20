# RevR17V1Facts — R17-V1 measured against git, receipt bytes and the round-17 transcript

Seat `MadoR18.RevR17V1Facts`, 2026-10-20T15:44Z.
Measured revision: `refs/heads/master` = `d3a00003e6ef0b1e3c7b4faf52d592eb293857ba`
(round-18 pre-registration). The artifacts under test are from `f71ccbe` and
`0ab1ccc`; `tools/mado-tripwire.py` at master is byte-identical to `0ab1ccc`
(sha256 `962919cec38ab8…`). I ran no lane gate, edited no lane file, wrote only
this report, installed nothing, and used no pacman/systemctl/hyprctl/probe.

## 1. Answer

The 0ab1ccc re-cut **did run**: one Eval cell at `2026-10-20T15:17:25.987Z`
(transcript line 539), executed after the P11 fix cell at `15:17:13.800Z`,
invoking `python3 -I tools/mado-tripwire.py` under tool sha `962919ce…`, and it
rewrote `tripwire-r13..r16.txt` and `tripwire-anchor-r15.txt` with
**byte-identical** output.

R17-V1 nevertheless survives, with a corrected shape: **no committed scan
receipt names its producer or measured revision**, so the re-cut is
unreceiptable from committed artifacts even though it happened. It is an
attribution defect, not a false claim that a re-cut happened.

## 2. Clause-by-clause

| Routed clause | Verdict | Evidence |
|---|---|---|
| Receipts carry no tool sha or `measured_commit` | **TRUE** | 0 byte hits for `962919ce` or `7a98720e` in each of the six; verdict keys are `counts, exit, files, findings, permitted, schema, unpermitted` (§3) |
| `tripwire-r13..r16`, `anchor`, `pacmanlog-join` last changed f71ccbe | **TRUE** | `git log -1 -- <path>` = `f71ccbe 2026-10-20T12:09:20-03:00` for all six (§3) |
| … "under tool `7a98720e…`" | **TRUE for the committed blob** | `git show f71ccbe:tools/mado-tripwire.py` sha256 = `7a98720ed3c0ea16…`. The worktree bytes were later rewritten byte-identically at 12:17:26-03 under `962919ce…` (§4) |
| `lessons/round-17.md:175-176` claims a re-cut under `962919ce…` | **TRUE, verbatim** | quote in §2.1; `git blame -L 173,176` = `0ab1ccc` for all four lines |
| Git records no change to those files at 0ab1ccc | **TRUE** | `git show --name-only 0ab1ccc` excludes all six; its 18-file stat lists only `tripwire-r17.txt`, the four selftest receipts, `vs-oracles`, w2 fixtures, tool, `SCORECARD`, `SKILL`, `round-17.md`, `SimplifyTripwire.md` |
| "so the re-cut is unreceipted" | **TRUE as written** (no receipt names it); **FALSE** if read as "the re-cut did not happen" | §4 shows the run, its output and the resulting mtimes |

### 2.1 The lesson lines, verbatim

`corpus/lessons/round-17.md` (block authored in `0ab1ccc`):

```
173:  - Wave-2 fix regression (SimplifyTripwire P11): moving comment handling to a
174:    post-shlex `#`-token break hid commands after a quoted or escaped `#`
...
175:    real comment) — `tripwire/w2-regressions` 30/30; tool sha256 `962919ce…`;
176:    all real-transcript receipts re-cut with identical counts.
```

Line 175 is true (`w2-regressions` 30/30 is in the P11 cell result). Line 176 is
true of counts and bytes, but nothing in the committed receipt proves it.

## 3. Receipt byte facts

```
$ git log --format='%h %cI' -- .ufo/waves/round-17/evidence/tripwire-r1[3-6].txt \
    …/tripwire-anchor-r15.txt …/tripwire-pacmanlog-join.txt
f71ccbe 2026-10-20T12:09:20-03:00 round-17: wave-2 corrections (…)
988b858 2026-10-20T11:50:30-03:00 round-17 C3: post-hoc transcript tripwire (…)
```

Per file, `git log -1`: r13, r14, r15, r16, anchor, join → **f71ccbe**;
`tripwire-vs-oracles.json` → **0ab1ccc**.

Producer/attribution grep per file: `grep -c '962919ce\|7a98720e'` = **0** for
r13, r14, r15, r16, anchor, join. `measured_commit` appears in no tripwire
receipt (`grep -rl measured_commit .ufo/waves/round-17/evidence/` returns only
`frozen-tampered-recut.json`, `label-check*.txt`, `harm-*selftest.txt`).

Verdict keys (parsed JSON, all six scan receipts):
`counts, exit, files, findings, permitted, schema, unpermitted`;
`schema` = `mado-tripwire-verdict-v1`. There is **no** producer field. The
receipts do bind their *inputs*: `files[].sha256` for `MadoR13.jsonl` is
`21126251c6154d5c…` and for `MadoR16.jsonl` `70e28f60c0185fde…`, both equal to
the live transcript digests today — input binding exists, producer binding does
not.

The asymmetry is in the tool itself: `emit()` is the single success path
(`tools/mado-tripwire.py:829`) and its payload has no tool sha. The selftest
path, by contrast, stamps `SELFTEST_SCRIPT_SHA256: 962919ce…` into all four
`tripwire-selftest-*.txt`. So the capability needed for the fix already exists
in the same file; only the scan verdict omits it.

`tripwire-pacmanlog-join.txt` is not tool output at all: it was written by hand
via `cat > … <<'EOF'` at transcript line 381 (`2026-10-20T14:50:16.916Z`), and
its own header documents the `awk` extraction command. Its 4 joins are
source-line assertions, not a scan receipt; "re-cut" never applied to it.

## 4. Did the 0ab1ccc re-cut run? Yes — exact chain

Transcript (read-only, named by my item):
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl`

1. **Line 464** defines the shared runner: `run(args)` =
   `subprocess.run(['python3','-I','tools/mado-tripwire.py']+args, cwd=L, …)`,
   with `E = L/'.ufo/waves/round-17/evidence'`.
2. **Line 536**, `2026-10-20T15:17:13.800Z`, Eval title "Quote-aware comment
   stripping fix": writes the tool (`p.write_text(t)`) and runs all four suites.
   Result at **line 538** (15:17:15.674Z):
   `core 9/9`, `compound 16/16`, `hardening 33/33`, `w2-regressions 30/30`.
3. **Line 539**, `15:17:25.987Z`, Eval title "Regenerate real-transcript
   receipts". It executes, in order:
   - `--selftest` for `w2/{adversarial,false-positive}` → writes receipts;
   - `--scan …/MadoR15/MadoR15.LibinputEvents.jsonl` → writes
     `tripwire-anchor-r15.txt`;
   - `--scan` MadoR13, R14, R15, R16 (transcript + subdir) → writes
     `tripwire-r13.txt` … `tripwire-r16.txt` and collects `res`;
   - writes `tripwire-vs-oracles.json` with
     `tool_sha256 = sha256(L/'tools/mado-tripwire.py')`;
   - `--scan` MadoR17 → writes `tripwire-r17.txt`;
   - prints `sha256(L/'tools/mado-tripwire.py')`.
   It does **not** write `tripwire-pacmanlog-join.txt`.
4. **Line 541**, `15:17:29.253Z`, its output:
   `anchor 1 {host_mutation: 2, live_probe: 1, package_query: 5}`;
   `13 {2, 12, 19}`; `14 {4, 0, 46}`; `15 {3, 29, 177}`; `16 {0, 0, 2}`;
   oracle deltas `13 26 [] 3`, `14 25 [] 0`, `15 131 [] 18`, `16 2 [] 0`;
   `r17 … {0, 1, 0} 149 139`; final line
   `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`.
5. **Line 542–544**: docs edited, then commit output
   `0ab1ccccaac5421f6e8ff2fe0cd2bcbd4e5bff4c` at `15:17:36Z`
   (12:17:36-03), 7 seconds after the cell.

Counts printed by the re-cut equal the committed receipts exactly
(r13 2/12/19, r14 4/0/46, r15 3/29/177, r16 0/0/2, anchor 2/1/5).

Two independent corroborations that the bytes did not change:

- `git diff --stat f71ccbe -- <the six>` prints nothing (rc 0);
  `git diff --quiet f71ccbe -- tripwire-r13.txt tripwire-r16.txt` → 0,
  i.e. worktree bytes are byte-identical to the `f71ccbe` blobs.
- Filesystem mtimes (`ls --time-style=full-iso`), all `-0300`:

```
tripwire-anchor-r15.txt   2026-10-20 12:17:26.655
tripwire-r13.txt          2026-10-20 12:17:26.911
tripwire-r14.txt          2026-10-20 12:17:27.108
tripwire-r15.txt          2026-10-20 12:17:27.389
tripwire-r16.txt          2026-10-20 12:17:27.830
tripwire-vs-oracles.json  2026-10-20 12:17:27.831
tripwire-r17.txt          2026-10-20 12:17:29.251
tripwire-pacmanlog-join.txt 2026-10-20 12:09:20.665   (= f71ccbe commit time; not rewritten)
```

The write order matches the cell's statement order (anchor first, then
r13→r16, then vs-oracles, then r17), so the mtimes are not a checkout artifact.

Tool-at-run-time is pinned by three equal values: the cell's printed sha
(`962919ce…`), the `0ab1ccc` blob sha, and the master worktree sha. The tool was
written at 15:17:13.8 and not touched again before the 15:17:36 commit.

## 5. The surviving defect

A committed scan receipt cannot answer "which tool, measured against which
revision". Consequences today:

- The only committed `962919ce` attribution for the r13–r16 scans is
  `tripwire-vs-oracles.json`'s single `tool_sha256` field, which changed by
  exactly one line at 0ab1ccc (`7a98720e…` → `962919ce…`). A one-line text edit
  would be indistinguishable from the real regeneration that in fact occurred.
  That file also carries no per-receipt digest and no receipt path, so it is not
  a binding of the `.txt` bytes.
- A byte-identical re-cut is invisible to `git diff`; without a producer stamp
  on the receipt, "we re-cut and the bytes are unchanged" is unfalsifiable from
  the committed tree in either direction.
- `tripwire-pacmanlog-join.txt` is a hand-authored join (heredoc), not tool
  output; it should be labelled as a derived assertion, not read as a scan
  receipt.

## 6. What C1 can honestly claim, and runnable failing checks

Recommended round-18 Mistakes wording (append-only), which this transcript
supports and which a reviewer cannot falsify:

> Round-17 scan receipts carried no producer stamp (`tool_sha256`) or
> `measured_commit`; the post-P11 re-cut did run (transcript cell, identical
> counts and identical bytes) but is attested nowhere in the committed tree, so
> the claim "re-cut with identical counts" is unverifiable from the lane.

Suggested criterion (append-only, lesson-cited), with the check I ran:

**Producer stamp.** Every `MADO_TRIPWIRE:` scan receipt names the tool sha256
that produced it; a scan receipt without it is unreceipted.

Check A (ran at master, fails today):

```python
import glob,json,sys
bad=[]
for p in sorted(glob.glob('.ufo/waves/round-*/evidence/tripwire-*.txt')):
    lines=open(p).read().splitlines()
    if len(lines)<2 or not lines[0].startswith('MADO_TRIPWIRE:'): continue
    d=json.loads(lines[1])
    miss=[k for k in ('tool_sha256','measured_commit') if k not in d]
    if miss: bad.append((p,','.join(miss)))
print('unstamped:',len(bad),bad); sys.exit(1 if bad else 0)
```

Observed: 14 receipts scanned, **7 unstamped**, exit 1 —
`tripwire-anchor-r15.txt`, `tripwire-r13.txt`, `tripwire-r14.txt`,
`tripwire-r15.txt`, `tripwire-r16.txt`, `tripwire-r17.txt`,
`tripwire-r17-w1.txt`. The class is wider than R17-V1's six: `r17` and
`r17-w1` are unstamped too.

Check B (producer binding passes only after a stamped re-cut):

```python
d=json.loads(open('.ufo/waves/round-17/evidence/tripwire-r16.txt').read().splitlines()[1])
assert d['tool_sha256'] == hashlib.sha256(open('tools/mado-tripwire.py','rb').read()).hexdigest()
```

Observed today: `FAIL: receipt names no producer`, exit 1 (KeyError).

If L1 wants a third criterion specifically for the identical-bytes case, the
distinguishing rule is: a re-cut whose bytes do not change must be attested by a
producer-stamped receipt (or a committed byte-equality assertion over the
receipt set), because `git diff` is necessarily empty in that case. The fix
itself is small and already patterned in-tree: add `tool_sha256` (and
`measured_commit` when committed) to the `emit()` payload at
`tools/mado-tripwire.py:829`, mirroring `SELFTEST_SCRIPT_SHA256` and the
round-18 `--frozen` verdict schema; then re-cut the seven unstamped receipts.

## 7. Out-of-lane fact (R17-V2's object, recorded not touched)

`/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mado.md` (fleet report,
outside the lane; mtime Oct 20 12:17):

- line 3: "…`0ab1ccc` fixes a wave-2 regression … tool sha `962919ce…`,
  receipts re-cut with identical counts".
- line 76 (C3 row): "present, sha256 `7a98720e…`; 9/9, 16/16, 33/33, 30/30 …".

Same report, two different tool shas; `7a98720e` is the `f71ccbe` blob. The
lane-owned `SCORECARD.md` capability row cites `962919ce…` and is correct. This
is R17-V2; I did not edit the fleet report (lane bound).

## 8. Limits

- I did not re-run the tripwire or any suite (seat bounds); all facts come from
  git bytes, committed receipt bytes, filesystem mtimes and the transcript.
- Mtimes are filesystem state: strong corroboration, not committed evidence, and
  a checkout would reset them. The transcript is data; its claims here are
  corroborated independently by byte identity and the 0ab1ccc file list.
- I did not verify the six receipts' finding-level correctness against oracles;
  only their counts, input digests, producer fields and re-cut provenance.
- The re-cut cell's sha print is computed after the scans in the same cell; the
  tool was not modified between 15:17:13.8 and the 15:17:36 commit, so the scans
  ran under `962919ce` (an edit inside that 4-second window is excluded by the
  commit blob).

## 9. Reproduction

```
git -C <lane> log --format='%h %cI' -- .ufo/waves/round-17/evidence/tripwire-r1[3-6].txt \
  .ufo/waves/round-17/evidence/tripwire-anchor-r15.txt \
  .ufo/waves/round-17/evidence/tripwire-pacmanlog-join.txt
git -C <lane> show --name-only --format='' 0ab1ccc
git -C <lane> show f71ccbe:tools/mado-tripwire.py | sha256sum      # 7a98720e…
git -C <lane> show 0ab1ccc:tools/mado-tripwire.py | sha256sum      # 962919ce…
git -C <lane> diff --quiet f71ccbe -- <the six>; echo $?            # 0 = identical
ls -la --time-style=full-iso <lane>/.ufo/waves/round-17/evidence/tripwire-r1[3-6].txt
```

Transcript: lines 464 (runner), 536/538 (P11 fix + 9/9,16/16,33/33,30/30),
539/541 (re-cut call + counts + `962919ce…`), 542/544 (commit `0ab1ccc`).
