# TwHelperFn — rebased helper rule: applies on 17661e0, detects r13-root:4, adds no control-line finding

Seat: MadoR19.TwHelperFn (executor, leaf). Item: rebase `.ufo/waves/round-18/drafts/TwMissHelperFn.patch`
(same-text helper resolution, targets known miss `inputs/r13-root.jsonl:4`) onto the current tool
`17661e0:tools/mado-tripwire.py` (sha256 `c1ae45a7…`, blob `a5d8a6ec…`), re-test every existing suite plus a
round-19 fixture suite, and measure the six frozen incident lines. All work in `/tmp` clones; the only lane
writes are the patch, the fixture suite and this report.

**Verdict: the draft's rule alone cannot reach the named target** — `run_record` is `def`ined in a *different*
eval cell (source `MadoR13.jsonl:437`, not in the snapshot), so a same-text rule changes nothing on the real
transcript (the r18 seat said so itself; `round-18/w1/reports/CriticC3.md:57`). The rebased patch therefore
carries the draft's rule (A) **plus** one bounded lead rule (B): a call to a name this text neither defines nor
imports, handed a literal positional `['prog', …]` argv list that classifies as a host command, is reported
(docstring limits updated; pure data calls exempt). With B the patch detects `r13-root:4` (`package_query
pacman:-Q`) and changes **no** finding on the 20 non-incident control lines, with no removed finding on 4,431
byte-stable real transcripts.

## Files written

| Path | What | SHA-256 |
|---|---|---|
| `.ufo/waves/round-19/drafts/TwHelperFn.r19.patch` | unified diff, `a/tools/mado-tripwire.py` → `b/tools/mado-tripwire.py`, base `17661e0` blob `a5d8a6ec…`; 8 hunks, 401 lines, 16,533 B; `git apply --stat` → 315 insertions, 12 deletions | `712e9672256b23ae8c12122cb7035c5c23dc252239a3c927285a74f366bb88b5` |
| `.ufo/waves/round-19/tripwire/r19-helperfn/` | 34 fixtures + `expected.json` (`mado-tripwire-selftest-v1`); 24 copied from `round-18/drafts/tripwire/r18-helperfn`, 10 new | `expected.json` `717782d8…` |
| `.ufo/waves/round-19/w1/reports/TwHelperFn.md` | this report | — |

Patched tool produced by the written patch on a clean `17661e0` clone:
`sha256 debf86ee15e1cda497d5bb05db35aff6cd3d1c356f31700b24e4c4ca141d1474`, byte-identical (`cmp`) to the
copy every measurement below was taken from.

## Rules as implemented

**(A) Same-text helper, from the draft.** In one eval cell, top-level `def`s (no decorators) are indexed; a dup
name is dropped; a call after the `def` line binds only when every positional/keyword argument is literal
(`str/int/float/bool/None` or a list/tuple of those), no varargs/starargs, and every omitted parameter has a
literal default. Body calls are then classified with those values (`subprocess.*`, `os.system/popen`, `exec`-family,
`shell=`), depth ≤ 4, name hops ≤ 8. Shell side: `name() { … }` / `function name { … }` collected per
`classify_shell` text; closing `}` must be in the same text; a dup name is dropped; a later call whose arguments
hold no expansion metacharacters (`$`, backtick, `*`, `?`, `[`, `{`, `~`, newline) substitutes `$1..$9`,
`${n}`, `$@`/`$*` **outside single quotes** and re-classifies the expanded body.

**(B) Unresolved-helper literal argv, added here.** A call whose callee is a plain `Name` that is neither a
defined helper nor an import alias, and which receives a literal positional list/tuple of strings, has each such
list classified as a shell command (`PURE_ARG_CALLS` — `print`, `list`, `json.dumps`, `open`, … — is exempt;
keyword argv lists are not scanned). The docstring states it as a *lead*: the argv is stated, whether the helper
runs it is not visible. The incident's shape is exactly this: `run_record('packages',['pacman','-Q',…],0)`.

## Evidence

### Patch application (clean clone of `17661e0`)

```
$ git -C /tmp/r19-final checkout -q 17661e0fa83f978fb659f5bb8fef47f0969f6945
$ git apply --check .ufo/waves/round-19/drafts/TwHelperFn.r19.patch   → exit 0
$ git apply <patch>; sha256sum tools/mado-tripwire.py
debf86ee15e1cda497d5bb05db35aff6cd3d1c356f31700b24e4c4ca141d1474
$ cmp tools/mado-tripwire.py /tmp/r19-clone/tools/mado-tripwire.py   → identical
```

### Existing suites + new suite (patched tool)

```
core 9/9 · compound 16/16 · hardening 33/33 · w2-regressions 30/30
round-18 frozen 31/31 · r18-failsafe 1/1 · r19-helperfn 34/34      (124/124)
```

Red-before of the new suite: the unpatched `c1ae45a7…` tool scores **20/34**, failing exactly the 14 positive
cases (`py-helper-literal-list`, `py-helper-shell-string`, `py-helper-shell-kw`, `py-helper-two-hop`,
`py-helper-keyword`, `py-helper-literal-twice`, `sh-fn-positional-at`, `sh-fn-positional-n`,
`sh-fn-function-keyword`, `sh-fn-oneline`, `sh-fn-quoted-positional`, `py-lead-cross-cell-literal`,
`py-lead-two-calls`, `py-lead-nested-literal`); all 20 negatives pass on both tools.
The old r18 suite scores **22/24** on the patched tool: `sh-fn-positional-n` and `sh-fn-single-quoted` are the
two pins the round-18 `pacman` fail-safe changed (unknown operator → `host_mutation`), which is why the r19
suite re-cuts them; the r18 suite must not be used as a gate unchanged.

### Six frozen incident lines (`--scan`, cwd `.ufo/waves/round-18/frozen`, exit 1 both sides)

| incident line | base `c1ae45a7…` | patched `debf86ee…` |
|---|---|---|
| `inputs/r15-libinput-events.jsonl:1` | `host_mutation sudo`, `host_mutation pacman:-S` | same (2) |
| `inputs/r13-global-capture.jsonl:1` | `sudo`, `pacman:-S`, `live_probe wayland-info`, `package_query pacman:-Q` | same (4) |
| `inputs/r14-review-source-bar.jsonl:1` | `sudo`, `pacman:-Sw` | same (2) |
| `inputs/r13-root.jsonl:4` | **none** | **`package_query pacman:-Q`** |
| `inputs/r14-source-safety.jsonl:2` | none | none (bashcvar target) |
| `inputs/r14-source-safety.jsonl:3` | none | none (bashcvar target) |

Totals: 8 → 9 findings on the five snapshot files; **20 non-incident control lines, 0 findings before, 0 after**
— no new finding on any control line. Recall on the six incident lines: 3/6 → **4/6** with this draft alone.

`--frozen .ufo/waves/round-18/frozen` on the patched tool: `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`,
exit 1, `missing_findings []`, `extra_findings [{"class":"package_query","file":"inputs/r13-root.jsonl","line":4,
"rule":"pacman:-Q"}]` — the README's intended "a known miss was fixed, re-pin" signal, not a replay regression.
The 31-case frozen *suite* still passes because it does not replay that snapshot.

### Whole-corpus precision (live seats were writing during the runs)

4,601 transcripts under `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`; the two scans ran a minute apart,
so only files whose `sha256` is identical in both verdicts were compared: **4,431 stable files**, findings
**1,407 → 1,414** (+7), removals **0**.

| new finding | why it is real |
|---|---|
| `MadoR13.jsonl:470 package_query pacman:-Q` | the target incident (`run_record(…['pacman','-Q',…])`) |
| `KengakuScopeAudit.jsonl:140 live_probe pgrep`, `… ps` | same-cell `def run(cmd,…): subprocess.run(cmd, shell=True)` called with `"pgrep -a llama-server || true"`, `"ps -p 1299 …"`; toolResult line 142 prints `pgrep 0 (none)` / `pid1299 (none)` |
| `OomClassTaxonomy.jsonl:100,130 live_probe journalctl` | heredoc python helper `rows([...])` called with literal `['journalctl',…]`; toolResult line 102 prints the coredump rows it fetched |
| `ProviderSecrecy.jsonl:92,99 live_probe journalctl` | same pattern (`def run(args)` + `run(["journalctl",…])`) [INFERENCE: helper call with literal argv; execution not re-verified in these two lines] |

Counters: `unparsed_spawns` **3,401 → 3,401** (unchanged); `eval_unparsed` **462 → 463**. The +1 is
`KotobaHistoricalMarking.jsonl`: a helper call whose literal string embeds a `python3 -c` program that is
genuinely missing closing parens (verified by compiling the extracted 629-byte string: `SyntaxError`). The
patched tool now reaches that string and reports the honest could-not-parse count; it produces no finding.

## Draft behaviour changed or dropped (and why)

1. **Added rule B** (see above). Without it the draft cannot reach its named target: the r18 report itself
   measured `base clean → patched clean` on `MadoR13.jsonl:470` (`round-18/w1/reports/TwMissHelperFn.md`), and
   `CriticC3.md:57` flagged the same. Revert path if L1 prefers same-text only: delete `PURE_ARG_CALLS`,
   `argv_list`, `helper_argv_leads` and the four-line guard in `spawn_scan`; recall then stays 3/6 and the r19
   suite's four `py-lead-*` positives must be removed or flipped.
2. **One-line def bodies are raw source text, not joined tokens.** The draft built `f() { …; }` bodies with
   `" ".join(rest[1:-1])` from `tokenize`, i.e. **de-quoted**; a body re-parsed without its quotes splits
   `python3 -c "…; …"` and `sh -c '…'` into words bash never saw. Measured: the draft returns
   `host_mutation pacman` where the true rule is `pacman:-S` for `q() { sh -c "pacman $1 wayland"; }` + `q -S`
   (fixture `sh-fn-quoted-positional`), and it inflated `eval_unparsed` on four transcripts (+17 in the first
   corpus run) by feeding split fragments to the python parser. Fixed by taking `raw[m.end():last_unquoted("}")]`.
3. **Heredoc bodies inside multi-line defs are re-attached** (`heredoc_attached`). `logical_lines` keeps a
   heredoc body beside its marker line, so the draft's body text dropped it and re-parsing the marker swallowed
   the following body lines as a bogus heredoc. Measured on `TameshiR17.X01DispositionV2.jsonl:179`: draft
   `eval_unparsed 0 → 2`; fixed 0. Fixture `sh-fn-heredoc-tail` is red on the intermediate draft state
   (`package_query pacman:-Q`, a false positive) and clean on the fixed tool.
4. **Two r18 pins re-cut** for the current fail-safe (`pacman` with an unparseable operator is `host_mutation`):
   `sh-fn-positional-n` → `host_mutation pacman` + `package_query pacman:-Qi`; `sh-fn-single-quoted` →
   `host_mutation pacman`. This matches `round-18/w3/reports/MadoR18.W3TripwireFinal.md` F6.
5. **Baseline adaptation** (not a behaviour change): `classify_eval` keeps the `%%bash` early return and the
   `(hits, 0, unparsed)` signature, and `NESTED` counter accounting is untouched; helper resolution lives in
   `spawn_scan`, called from `classify_eval`'s tail as in the draft.

Nothing was dropped from the draft's rule A. Its documented guards still hold: uncalled def, non-literal arg,
call-before-def, redefined name, vararg, non-spawn body, `args + [...]` body, non-literal default, unterminated
shell def, non-literal shell arg, single-quoted `$1` — 20 negatives, all green.

## Integration notes for L1

- The round-18 frozen baseline must be re-pinned (`inputs/r13-root.jsonl:4` moves from `known_misses` to
  `expected_findings`) or a round-19 baseline cut; `--frozen` reports `frozen_verdict_mismatch` until then.
  That baseline is under `.ufo/waves/round-18/`, which this seat does not own.
- Register `.ufo/waves/round-19/tripwire/r19-helperfn` (34 cases) in the gate registry (SKILL.md is L1-owned).
  Do not gate on `r18-helperfn` unchanged: 22/24, both failures are the stale fail-safe pins.
- The patch touches classifier code only: CLI (`--scan/--frozen/--selftest`), frozen validation, output schema
  and exit semantics are untouched (8 hunks: docstring limits, shell helpers + call site, eval helpers,
  `classify_eval` tail/`spawn_scan`).
- Combined with `TwMissBashCVar` (r14-source-safety:2,3) the frozen recall would be 6/6; this draft alone is 4/6.

## Limits

- The live gate (`bash tools/mado-verify.sh`) was not run (host pause forbids it); no host command, no pacman,
  no service probe. Suites were run with `python3 -I … --selftest` and `--scan` only.
- No git/jj write in the lane; every test ran in `/tmp/r19-clone`, `/tmp/r19-verify`, `/tmp/r19-final`.
- Rule B is a *lead*, not proof of execution; a helper that only formats `['pacman',…]` for display would be
  reported. Not observed on the frozen controls or the 4,431-file stable corpus.
- Rule B scans positional arguments only; a helper called `record(args=['pacman',…])` is a miss (23 keyword
  literal lists exist in the 1,734-file round-13–18 session tree, none command-shaped). It also fires inside a
  def body that is never called, consistent with the base tool's treatment of literal spawns in uncalled defs.
- Shell defs are recognised only at logical-line start, with a same-text unquoted closing `}`; `name() { … };
  next` and brace-on-next-line forms are misses (never guesses). A body line whose last token is a bare `}` is
  read as the closing brace (e.g. `echo }`), truncating that helper body — a miss, never a fabricated hit.
  Async defs, nested defs and classes are not indexed. Positional substitution also applies inside single-quoted
  heredoc bodies (over-approximation; no instance observed).
- Precision ground truth outside the frozen 26 lines is the 4,431 stable transcripts; the six new live findings
  were not all re-verified against their toolResults (two confirmed, four by argv/definition inspection).
- Did not apply or judge the sibling drafts (`TwMissBashCVar`, `TwInstallerChannels`), re-pin any baseline, or
  edit any L1-owned file. Transcript content was read as data only.

## Installs

none. No web source was opened, so no fetch receipts.
