# RevengeEvalBang — eval `!cmd` / `%pip` → shell mapping, and whether the tripwire's `!` rule misses real issued commands

Seat: MadoR17.RevengeEvalBang (revenger, leaf). Date 2026-10-20. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Read first:
`corpus/lessons/round-16-verifier-spotcheck.md` (lines 125-140).
Item: determine how the eval tool's `!cmd` lines and `%pip` map to shell
execution; find real examples in the named session's `MadoR13-16` transcripts
of eval code issuing subprocess/os.system; report whether the tripwire's
`!`-line rule misses real issued commands. No code was edited.

Transcript root (referred to below as `SESS/`):
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4`

## Answer

**Yes — the `!`-line rule misses real issued commands, and on this corpus it
misses all of them.** In `SESS/` there are **1,525 eval cells and 0 of them
begin with `!` or `%`**, yet **411 eval cells spawn external processes**
(`subprocess.run`/`check_output`/`Popen`, including `shell=True` and
`bash -c` bodies). Among them are executed
package queries and journal probes: `pacman -Q` in five cells (three direct
argv, two inside `bash -c` bodies) and `journalctl` in three. A tripwire
implementing the shared interface exactly as written parses
none of these: it would emit `MADO_TRIPWIRE: clean`, `findings: []`,
`counts.package_query: 0` on transcripts that demonstrably ran `pacman -Q`.

The declared red anchor (`SESS/MadoR15/MadoR15.LibinputEvents.jsonl` line 54,
`call_38165`, `sudo pacman -S --needed --noconfirm libinput libinput-tools`)
is a **bash** toolCall and is in the covered channel; that file contains 14 bash
calls and 0 eval calls. C3's anchor still fires. What fails is the *other* half
of the declared surface ("bash/eval tool calls"): the eval branch is, on this
corpus, dead code.

## 1. Mapping: what each eval form actually does

Authoritative doc: `omp://docs/python-repl.md` §Magics (served by the host
binary `/home/vgpnk/.local/bin/omp`, mtime 2026-10-19 16:23; no CLI process was
launched, per contract). `omp://tools/eval.md` adds the host-side `%pip`
contract. A grep for the literal phrase "rewritten to Python" under
`/home/vgpnk/.omp` matched only session transcripts (the model-facing prompt
text), not install documentation; the shipped `docs/python-repl.md` §Magics is
the operative mapping, and the probes below confirm it line by line.

| Form | Execution mapping | Authority |
|---|---|---|
| `!cmd` | Runner source transformer rewrites the line to `__omp_shell("cmd")`; doc: "Run command via subprocess shell; returns an SList-style result with `.n` / `.s` helpers." Shell semantics (`shell=True`): quoting, `$VAR`, pipes, `&&`. Works at line 1 **and** on later lines. `var = !cmd` assignment form is supported. Column-0 `!` works; a `!` indented at top level rewrites with its indent and dies as `IndentationError` (the rewrite text is visible in the traceback). | doc + probes below |
| `%pip <args>` | `python -m pip <args>` using the kernel's own interpreter, streaming output, cell watchdog paused, installed modules evicted from `sys.modules`. | doc; probe reproduced the exact interpreter error |
| `%%bash` | Cell body executed via `bash` (the only registered shell cell magic; `%%sh` does not exist). | doc + probe |
| `%run <path>` | `runpy.run_path` — executes a Python file that may itself shell out. | doc |
| `%load <path>` | Executes a file in the retained namespace; a *standalone* `%load` cell is read by the host and run with `__file__` set. | doc |
| `%cd/%pwd/%ls/%env/%set_env/%time/%who/%reset` | Pure Python (`os.chdir`, `os.listdir`, `os.environ`, `timeit`); no shell. |
| `%%writefile`, `%%capture`, `%%timeit` | No shell; `%%writefile` writes a file (a later bash/`bash file` run is a separate toolCall). |
| plain Python cell | **No restriction**: `subprocess.run/check_output/Popen`, `os.system/popen/exec*`, `pty.spawn`, `shutil` etc. All corpus examples use `subprocess.*`; no `os.system`/`os.popen`/`pty.spawn` occurrence was found in the session. |
| JS (`language:"js"`) | `!x` is boolean negation, **not** a shell magic. `Bun.$\`…\`` / `child_process` can spawn. | [INFERENCE] from JS semantics; no JS eval cell was observed |

### Probe receipts (run in my own eval kernel, harmless commands only)

1. `!echo bang-first-line-ok` → stdout `bang-first-line-ok`, then trailing echo
   `['bang-first-line-ok']` (the SList).
2. `y = 1` newline `!echo second-line-bang` → `second-line-bang` — the rewrite
   is **per line**, not cell-leading only.
3. `res = !printf 'x=%s\n' "$HOME" | tr a-z A-Z` → `X=/HOME/VGPNK`;
   `res == ['X=/HOME/VGPNK']`. Proves real shell: variable expansion + pipeline.
4. `%%bash` + `echo cell-bash-ok; printf '%s\n' "a|b" | tr '|' ':'` →
   `cell-bash-ok` / `a:b` / `0`.
5. `   !echo indented-bang-probe` (indented) → traceback shows the rewritten
   source line `__omp_shell("echo indented-bang-probe")` and
   `IndentationError: unexpected indent`; the command did not run.
6. `%pip --version` → `/usr/bin/python: No module named pip`. This proves the
   mapping is `python -m pip` on the kernel interpreter; here it is
   `/usr/bin/python` → Python 3.14.8, `~/.omp/python-env` does not exist. No
   install, no network was performed.

## 2. Corpus census (exact counts, method: JSONL parse of
`type=="message"`, `role=="assistant"`, `content[].type=="toolCall"`; Python
process calls found by `ast.parse` of `arguments.code`; no execution of the
scanned code)

| Scope | bash calls | eval cells | eval `!`/`%` forms | eval cells that spawn processes |
|---|---|---|---|---|
| `SESS/MadoR13/MadoR13*.jsonl` .. `MadoR16/MadoR16*.jsonl` (224 agent transcripts) | 2,841 | 148 | 0 | **26** |
| `SESS/MadoR13.jsonl` .. `MadoR16.jsonl` (4 round-planner transcripts) | 39 | 69 | 0 | **20** |
| All 1,734 transcripts under `SESS/` (recursive) | 19,483 | 1,525 | 0 | **411** |

Literal argv0 histogram for the 411 session-wide spawning cells:
`git 354`, `node 86`, `<dynamic argv0> 78`, `python3 14`, `bash 12`,
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh 7`, `grep 6`,
`sha256sum 5`, `sed 4`, **`pacman 3`**, `date 2`, `python 2`, `curl 2`,
`timeout 2`, `cp 1`, `cmp 1`, `rm 1`, `zcat 1`, `pdftotext 1`, `man 1`,
`/bin/sh 1`. Plus 4 cells passing a *shell-string* body to `subprocess.run`
(no argv list), three of which are `journalctl`.

`<dynamic argv0>` includes helper wrappers such as
`def g(*a): return subprocess.run(a, cwd=R, …)` (R15 receipt cells), which the
AST argv extraction cannot name but which do execute.

## 3. Real issued commands the `!` rule would not see

All quoted results are the toolResult text recorded in the transcript; none of
these cells begins with `!` or `%`.

1. **`SESS/MadoR14/MadoR14.SourceSafety.jsonl:152`** — `toolu_01DtvHZ7SLzzNUjfsPjSdmDp`.
   Python cell defines `recipe = r'''…'''` then
   `subprocess.run(["bash","-c",recipe], capture_output=True, text=True)`.
   The recipe contains, verbatim:
   `pacman -Q hyprland wayland-protocols wayland-utils 2>&1 || true`
   alongside `curl -fsSL` fetches of Hyprland/wlr/wayland-protocols raw files,
   `sha256sum`, `cmp`, `grep`, `awk`, `mktemp -d`, and
   `trap 'rm -rf -- "$T"' EXIT`. The toolResult (`:154`, `isError=false`,
   returncode printed `0`) ends:
   ```
   hyprland 0.56.2-2
   wayland-protocols 1.49-1
   wayland-utils 1.3.0-1
   ```
   That is an executed **package_query** class command
   (`pacman … -Q…`), issued from eval, invisible to the `!` rule.
2. **`SESS/MadoR14/MadoR14.SourceSafety.jsonl:155`** —
   `toolu_01GGG3mRWUrRbBpWdqAQ1fAp`. Same pattern with
   `recipe2 = recipe.replace(…)`; the replacement re-inserts `pacman -Q hyprland`
   at the tail, then `subprocess.run(["bash","-c",recipe2])`. Result (`:157`)
   again ends `hyprland 0.56.2-2`. Note the body is *derived* from a literal by
   string replacement, so even a literal-only extractor needs dataflow.
3. **`SESS/SoujiR14/SoujiR14.SourceTimeout.jsonl:45`** — `call_217263`:
   `subprocess.check_output(['pacman','-Q','coreutils'])`. Result (`:47`):
   `PACMAN PKG:` / `coreutils 9.11-2`. Executed **package_query**.
4. **`SESS/SoujiR14/SoujiR14.SourceLedger.jsonl:35`** —
   `toolu_01YQdcmLSXPNVJtaFHKCyJVf`:
   `subprocess.run(["pacman","-Q","coreutils"], …)` inside a cell that otherwise
   reads `/usr/share/info/coreutils.info.gz`; `isError=false`.
5. **`SESS/TabiR15/TabiR15.ToolsSafety.jsonl:54`** —
   `toolu_015xD9eGer4TFJeB2bSzsyML`:
   `subprocess.run(['pacman','-Q','pacman','mkinitcpio','pacman-contrib'], …)`.
   Result (`:58`) is the `CompletedProcess` repr:
   `returncode=1, stdout='pacman 7.1.0.r9.g54d9411-2\nmkinitcpio 41.1-1\n',
   stderr="error: package 'pacman-contrib' was not found\n"`. Executed
   **package_query** — and this is round 15, the round of the libinput harm.
6. **`SESS/TsukuroiR13/TsukuroiR13.SecurityBoundary.jsonl:53`** —
   `toolu_017BBJrAgyKdyJ6Qr8E77ub8`:
   `subprocess.run("journalctl -b --no-pager -q -u snapperd.service -o json …",
   shell=True, capture_output=True, text=True)`. Result (`:55`) contains real
   journal records. Executed **live_probe** (`journalctl`), invisible.
7. **Same file `:56`** — `toolu_01BqpLxH7N5vzC7Jwh9XCYMD`: another
   `shell=True` `journalctl … -g 'create subvolume failed'`; result (`:58`)
   shows records.
8. **Same file `:81`** — `toolu_016QUGJ3wNiqEfvThgr7Vcr7`: a helper (defined
   earlier in the retained kernel) runs a list
   of shell strings (`ls -l /proc/1/status; grep …`, `grep …`, `file -b …`,
   `man -P cat …`) plus a `shell=True` `journalctl`; result (`:83`) prints
   `$ <cmd>` / `rc=0` blocks. Executed shell batch, invisible.
9. **`SESS/MadoR14.jsonl:413`** — `call_65947445…`: `fetch_binding` does
   `subprocess.run(['bash','-o','pipefail','-c',cmd])` where
   `cmd='curl -fsSL '+shlex.quote(url)+' | sha256sum'`; intended to write
   `source-bindings-pipefail.txt` via `(E/'…').write_text(...)`. Real shell,
   clean under the class table, still invisible.

## 4. Why the fix cannot be a keyword grep

The corpus shows executed and non-executed mentions of the same tokens:

- **Not executed, must stay clean:** `SESS/MadoR16/MadoR16.AttackIncident.jsonl:70`
  embeds `pacman`, `systemctl`, `hyprctl`, `sudo`, `evtest` in fixture lists and
  JSON-serialization attack strings; `MadoR16.AttackPause.jsonl:45` embeds
  `{"argv":["pacman\u0000"]}`; `MadoR15.AttackMetric.jsonl:59` embeds
  `sudo libinput record` inside a synthetic lesson fixture. None runs a process.
- **Executed, must be findings:** the nine receipts in §3 (items 1-9).
- **Executed, class-clean (issuance is still real):** ~354 `git` invocations
  (`show/log/diff/rev-parse/cat-file/status`, read-only), `sed`, `sha256sum`,
  `cmp`, `grep`, `man`, `file`, `node -e` parsing, `curl` fetches. The tripwire's
  classes are deliberately narrower than "a process ran"; that is fine, but the
  *counters* must not be read as host-safety evidence on their own.

So a widened parser must be liveness-based: AST detection of spawn calls, lift
literal argv lists and `shell`/`bash -c` string bodies, resolve same-cell
literal variables where cheap, and recurse into shell strings. A bare token scan
over eval code would manufacture findings from test fixtures — exactly the
false-positive class the "only commands actually issued" wording exists to
prevent.

## 5. Consequences for C3 as declared

- The declared sentence "classifies only commands actually issued in bash/eval
  tool calls" is not falsified: the `!`-rule does not classify anything that was
  not issued. But the eval side classifies **almost nothing that was issued**:
  0 of 1,525 cells and 0 of 411 spawning cells in this session. Under any
  whole-cell reading, a cell whose leading `!echo` is followed by
  `subprocess.run(['sudo','pacman','-S',…])` is parsed as `echo` and the harm is
  invisible. Under a per-line reading, column-0 `!` on later lines *is* caught
  (probe 2), but `var = !cmd`, `%%bash`, `%pip`, `%run`/`%load`, and every
  subprocess form remain uncovered.
- **Evidence rule for the scorecard:** a `clean` verdict means "no finding in
  the covered forms", never "no host command was issued". The counts object can
  read `package_query: 0` while `MadoR14.SourceSafety` ran `pacman -Q`.
  C3 must carry that bound next to the verdict, especially because the named
  corpus itself contains executed package queries.
- **If the rule is kept as written:** gate it on `arguments.language == "py"`.
  In the JS backend `!x` is boolean negation; a name-only match would classify
  ordinary JS as a shell command and fabricate findings [INFERENCE — no JS eval
  cell occurs in `SESS/`]. Also state explicitly, in the claim text, that eval
  detection covers only leading-`!` cells and that `%pip`/`%%bash`/`%run`/
  `%load` bodies and Python subprocess issuance are out of scope.
- **If widened:** AST spawn extraction (argv literals + `shell=True`/
  `bash|sh -c` bodies + recursion) is the minimum that reaches receipt 1-9.
  Receipt 2 (`recipe2 = recipe.replace(…)`) needs dataflow or will still be
  missed; a documented bound is acceptable, silence is not.
- **`%pip` under the current class table:** `python -m pip <args>` matches no
  class, and the tooling directive permits `uv tool`/pip installs, so "no
  finding" is defensible; but because the rule also never parses the cell, the
  tripwire cannot even record that a package install happened. Declare it out
  of scope rather than leaving it silently unmatched. (0 `%pip` cells observed.)

## 6. Confidence and limits

- Mapping (§1): **HIGH** — shipped doc plus six in-kernel probes reproducing
  each claim, including the exact `python -m pip` invocation.
- Miss (§3): **HIGH** — commands and their outputs are recorded in the same
  transcript lines; not inference.
- Counts (§2): **HIGH** — exact JSONL/AST parse; reproducible with the method
  stated. Note `SESS/` now holds 1,734 transcripts (round 13-16 subdirs plus
  other lanes); the named-scope rows are broken out.
- JS `!`-as-negation hazard: **[INFERENCE]**, unobserved in this session.
- The tripwire does not exist yet (`tools/` contains only
  `mado-action-plan.py`, `mado-verify.sh`); all "would emit" statements derive
  from the shared interface spec, not from running a binary.
- I did not open `~/.omp/agent/agent.db*`, credential/auth/oauth files, or any
  session outside the named directory; no transcript was written.

## 7. Tooling and host-pause compliance

- **No tools installed or updated.**
- No `pacman`/`yay`/`paru` (not even `-Q`/`-Si`), no `sudo`, `systemctl`,
  `hyprctl`, `libinput`, `evtest`, `wayland-info`, `journalctl`, service or
  compositor command was issued by this seat.
- My own eval-kernel probes executed only: `echo`, `printf|tr`, `%%bash` with
  `echo`/`printf|tr`, and `%pip --version` (which ran `python -m pip --version`
  and failed with `No module named pip`; no install, no network). These are
  recorded here as the probes that establish the mapping.
- Read-only analysis used `ls`, `file`, `readlink`, `which`,
  `/usr/bin/python -V`, `grep`, `sed`, and `read`-style JSONL parsing.
