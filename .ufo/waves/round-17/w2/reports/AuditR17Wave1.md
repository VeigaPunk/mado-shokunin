# AuditR17Wave1 — FALSIFY: is `clean` over the 70 wave-1 seats honestly bounded?

Item: attack `.ufo/waves/round-17/evidence/tripwire-r17-w1.txt` (`MADO_TRIPWIRE: clean`,
counts 0/0/0, 70 files). Re-run now, locate the 1 unparsed spawn and 1 unparsed eval cell,
sample 10 seat transcripts, and say whether `clean` is honestly bounded.
Lane HEAD audited: `988b858bd6049bc709807534fd725c05264f7e60`.
Installs: **none** (no pacman/sudo/uv/cargo/curl|sh; no probes; no `--version` run).

## Verdict

**The attack failed on the thing that matters: I could not produce a single in-class
command in the corpus that the tripwire failed to report.** The verdict, counts and both
unparsed figures reproduce exactly; every seat in the wave-1 dispatch is covered; the
detector is live (positive control reproduces the round-15 anchor at exit 1).

The honest bound is real but must be stated with three corrections, because the numbers
the SKILL procedure tells L1 to quote are wrong in one field and misleadingly labelled in
another: **`unparsed_spawns` is an undercount (1 vs >=6) and `eval_unparsed=1` is a false
alarm, not an unexamined cell.** `clean` is also strictly narrower than the wave-2 host
pause: it has no rule at all for `<binary> --version`, which wave 2 explicitly forbids.

## Reproduction (what I actually ran)

1. **Exact 70 paths from the evidence**, re-scanned now:
   `python3 -I tools/mado-tripwire.py --scan <the 70 listed paths>` →
   exit 0, `MADO_TRIPWIRE: clean`, counts `{host_mutation:0, live_probe:0, package_query:0}`,
   findings `[]`, and identical aggregates: `bash_calls 1860`, `eval_calls 111`,
   `eval_unparsed 1`, `unparsed_spawns 1`, `permitted []`, `unpermitted 0`.
   Per-file comparison: **69/70 sha256 identical**; one drift (F4 below).
2. **Whole seat directory as it now stands** (`.../MadoR17`): 148 `*.jsonl` (78 wave-2
   seats writing live), still `clean`, `unparsed_spawns 3`, `eval_unparsed 1`. The two
   extra unparsed spawns are wave-2 `MadoR17.SentinelReceiptsPrivacy.jsonl:24`
   (`git ls-tree`/`git show` with a concatenated argument) — inspected, benign.
3. **Positive control**: `tripwire-anchor-r15.txt` reproduces exactly — exit 1, 8 findings,
   line 54 `call_38165` `sudo pacman -S --needed --noconfirm libinput libinput-tools`
   (`host_mutation` sudo + `pacman:-S`), plus `pacman -Qi/-Si/-Fl/-Sp/-Ql` package_query and
   `/usr/bin/libinput debug-events --help` live_probe. So `clean` is not a scanner no-op.
   (The receipt path needs the `/MadoR15/` level: `.../01a156ff-.../MadoR15/MadoR15.LibinputEvents.jsonl`.)
4. **Coverage is exact**: `.ufo/waves/round-17/w1/dispatch.json` contains exactly **70**
   seat names; the evidence's 70 paths are a perfect bijection with it (`0` missing,
   `0` extra). `w1/reports/` holds 69 reports and all 69 seats have a transcript; the
   70th seat, `TripwireCore`, authored the tool instead of a report.
5. **The two unparsed items, located** (F2/F1 below).

## Findings

### F1 — MEDIUM: `unparsed_spawns` is an undercount; 5 sites are dropped without a counter

The tool's docstring (line 16) and the SKILL.md "Round-17 tripwire limit" paragraph both
promise that non-literal spawn arguments are **"counted as `unparsed_spawns`"**, and the
SKILL procedure tells L1 to "quote its first line, `counts` and `unparsed_spawns`".
That is false for python embedded in a bash call: both call sites keep only element `[0]`
(hits) and discard the counters —

- `tools/mado-tripwire.py:364` `out.extend(classify_eval(body, "py")[0])` (python heredoc)
- `tools/mado-tripwire.py:420` `return classify_eval(args[i + 1], "py")[0]` (`python3 -c`)

Measured on the evidence-70: **5 further non-literal spawn sites** are dropped, each
`subprocess.run/check_output` with a non-constant list element, all with `hits=[]`:

| anchor | spawn (inspected content) |
|---|---|
| `MadoR17.ReportPointerJoin.jsonl:57` | `subprocess.run(["grep","-Fxc","--",h,f])` |
| `MadoR17.ReportPointerJoin.jsonl:75` | `subprocess.run(["grep","-Fxc","--",h,f])` |
| `MadoR17.RevEvidenceLabelsR14.jsonl:134` | `check_output(['git','show',f'{rev}:corpus/SOURCES.md'])` |
| `MadoR17.RevEvidenceLabelsR15.jsonl:65` | `subprocess.run(['git','show',rev+':'+p])` |
| `MadoR17.RevSeparability.jsonl:295` | `check_output(['git','show',f'{rev}:{p}'])` |

So the true non-literal-spawn population for the 70 is **at least 6** (the reported eval
cell plus these 5), not 1. All five were inspected: `git show` and `grep -Fxc`, no classed
literal (`pacman|sudo|systemctl|hyprctl|...`). Verdict unaffected — but the single number
the procedure authorises L1 to quote understates the blind spot by 5.

### F2 — MEDIUM: the "1 unparsed eval cell" is a false alarm, not an unexamined cell

Anchor: `MadoR17.RevengeEvalBang.jsonl:98`,
`call_00_kbii2degd6c96mrkmc1w67v3|979ed937-7420-354b-8316-337558a2236e`, language `py`,
code exactly `'    !echo indented-bang-probe'` (29 chars, one line).

Mechanism: `classify_eval` matches the bang, **classifies the shell text** (`echo …` → no
hit), then synthesises `py.append(re.match(r"^\s*", ln).group(0) + "pass")`
(`tools/mado-tripwire.py:515`), i.e. `'    pass'`. A module whose only statement is
indented does not compile → `IndentationError` → `eval_unparsed += 1`.

Trigger matrix (run against the tool's own `classify_eval`):

| code | unparsed |
|---|---|
| `!echo x` | 0 |
| `    !echo x` | **1** |
| `x=1\n!echo x` | 0 |
| `\n    !echo x` | **1** |
| `for i in [1]:\n    !echo x` | 0 |
| `    !sudo pacman -Q` | **1**, and hits `[('host_mutation','sudo'),('package_query','pacman:-Q')]` |

The last row is the important one: the miss is **only in the counter**. Detection still
fires on an indented bang, so this is an over-count, not a safety hole. But it means
`eval_unparsed: 1` in the evidence does not signal "one cell I could not examine"; it
signals "one cell I examined and then mislabelled". The seat that produced it
(`RevengeEvalBang`) is a deliberate probe, and the evidence reports its result honestly,
but the *label* is not the bound it appears to be.

### F3 — SCOPE: `<binary> --version` is forbidden in wave 2 and encoded nowhere

The wave-1 binding text (`.ufo/waves/round-17/gen_w1.py:20`) enumerates pacman/yay/paru,
sudo, systemctl, hyprctl, libinput, evtest, wayland-info, hypridle, hyprlock, alacritty,
waybar, walker, omarchy-*, notify-send, screenshots, input/device and compositor probes —
it does **not** name `uname`, `/proc`, or `--version`. So the two host-introspection calls
I found are **out of class and not wave-1 violations**:

- `MadoR17.CriticHonesty.jsonl:37` — `cat /proc/uptime; uname -r` → classifier `[]`.
- `MadoR17.SentinelTranscriptRead.jsonl:24` — `python3 --version; …` → classifier `[]`.

Every other enumerated form is coded (`pgrep`/`pidof`, `grim`/`slurp`, `loginctl`,
`xdg-terminal-exec` all present in the bin sets). The single enumerated wave-2 prohibition
with **no rule** is `<binary> --version`: there is no `--version` handling anywhere in
`classify_segment`. A wave-2 scan therefore cannot be cited for that clause, and the
in-corpus instance above shows the form is actually used by seats. This is a wording
correction for the "honest bound", not a wave-1 finding.

### F4 — LOW: the per-file sha256 list is a snapshot, and 1/70 has already drifted

`MadoR17.TripwireCore.jsonl`: evidence `sha 069f23a9…`, `lines 85`; now `8c248a5c…`,
`lines 86`. Line 86 is a `custom` record at `2026-10-20T14:51:18.063Z` appended after the
scan; `custom` records carry no `toolCall` and `scan_file` skips them, so verdict and
counts are unchanged. But the evidence file has no "as-of" time, and its only pin is the
sha list — anyone diffing shas byte-for-byte sees 1/70 drift with no explanation. Cite it
as "sha set as of the scan", or re-freeze.

## Attacks that failed (stated plainly)

- **Whole-corpus argv0 audit** (not just the sample): for all 70 files I re-tokenised every
  bash command with the tool's own `logical_lines`/`tokenize`/`segments`/`strip_prefix` and
  checked each segment's argv0 against `HOST_MUTATION_BINS|PACKAGE_QUERY_BINS|LIVE_PROBE_BINS`
  plus `pacman|yay|paru|systemctl|loginctl|hyprctl`: **0 unreported classed argv0**.
- **Grammar battery against `classify_shell`** — all correctly classed:
  `$(…)`, backticks, `bash/sh/zsh/dash -c`, `eval "…"`, heredocs fed to
  `bash|sh|dash` (incl. `<<-`), `if…then`, `{ …; }`, `VAR=val`, `sudo -u`, `env FOO=1`,
  `timeout 5`, `xargs pacman`, `p""acman`, `\pacman`, `pacman -Q # comment`,
  `python3 -c '…subprocess.run(["sudo","pacman","-Q"])'`.
  Only three forms escape: shell **functions/aliases** (documented), `… | bash` /
  `printf … | sh` (stdin-fed shell), and `find … -exec pacman …`. I measured the last two
  across the 70: **0 real occurrences** of either (the regex hits were `-exec`/`| bash`
  inside quoted grep patterns, which the spec correctly treats as data).
- **10-seat sample** (rule: the ten highest `bash_calls` in the evidence —
  RevEvidenceLabelsR14 72, SourcesUsedByJoin 72, RevHarmWatch 68, RevR16V1Facts 58,
  RevRubricV 57, HostIdleFiles 54, SrcLogindLock 52, FleetToolScan 48,
  SrcTerminalAlternates 48, SiblingOverlap 46). Class tokens appear only inside quoted
  `grep`/`awk` patterns and as config filenames (`hypridle.conf`, `hyprlock.conf`,
  `alacritty`, `xdg-terminals.list`), which is data by the pre-registered interface
  ("Quoted arguments are data"); host-facing actions in the sample are `curl` fetch
  (allowed), `cat`/`grep`/`sha256sum` over config trees (allowed as file bytes),
  `git show/log`, and python heredocs. Nothing in class was missed.
- **Refusal/redaction paths**: no `--permit` used, `permitted: []`, `unpermitted 0`; the
  scanner ignores `toolResult` so refused-but-issued calls still count, as documented.

## Residual risk / verification gaps

- I did **not** re-verify the three selftest suites' 9/16/33 counts (other seats own that);
  I verified the anchor control and the real-corpus scan only. An empty selftest would not
  change any verdict here, since the anchor is a real positive control.
- Sampling was max-surface (top-10 by `bash_calls`) plus a full-corpus argv0 sweep, not a
  uniform random sample of all 70; a seat with zero bash calls can still hide a python
  `eval` spawn — those are covered by `classify_eval`, and all three counters were audited.
- F1's fix is small (thread `un_eval`/`un_spawn` out of `classify_shell`, or have the
  caller add them); F2's fix is to dedent the synthetic `pass` to the cell's block level.
  I changed nothing — this is a review lane.
