# RevDocstring — partly falsified: 4 docstring sentences are false for the code at 28c6837 (1 under-detection lead gap, 1 misstated limit that the code actually exceeds, 2 shell-def sentences); the remaining exercised claims held under 203 `--scan` probes plus the committed `--frozen`/`--selftest` suites.

Seat: MadoR20.RevDocstring (wave 2, FALSIFY). Target: `tools/mado-tripwire.py` docstring at 28c6837.

## Canonical identity

- Clone `a4046a8` (clone HEAD, `git log --oneline -1` = `a4046a8 round-20: lesson R19-V2 sentence carries S096 on its tally line`). `git diff --stat 28c6837 a4046a8 -- tools/mado-tripwire.py` is **empty**: the tip worktree bytes under test are byte-identical to 28c6837.
- `sha256sum tools/mado-tripwire.py` = `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` — matches the claimed repair digest `9613f510…`.
- The tool also self-reports `SELFTEST_SCRIPT_SHA256: 9613f5100540…` when running `--selftest`.

Method: every docstring sentence was mapped to a probe. 158 table-driven cases (round 1, `/tmp/mado-r20w2-RevDocstring/probes/harness.py`), 36 CLI/frozen/selftest/depth cases (round 2, `probes/r2.py`), and 9 mechanism/boundary probes (rounds 3–4). All in a private `/tmp/mado-r20w2-RevDocstring` clone; no lane writes, no git/jj writes outside the clone.

## Findings (by severity)

### F2 — HIGH, under-detection: "imported external callable … is a `lead`" is false for the `module.attr` form

Docstring `tools/mado-tripwire.py:42-44`: *"A literal positional `['prog', ...]` argv passed to an unresolved bare name or imported external callable is a `lead`, not an observed execution."*

The module-qualified imported-external form produces **no finding at all** — not even a lead, and not even an `unparsed_spawns` count:

```
$ python3 -I tools/mado-tripwire.py --scan a4.jsonl   # eval py: import lib / lib.run(['pacman','-S','hyprland'])
MADO_TRIPWIRE: clean
{"... "findings": [], "unparsed_spawns": 0 ...}        (exit 0)
```

Probes: `import lib; lib.run(['pacman','-S','hyprland'])` → clean (a4); string form `lib.run('pacman -S hyprland', shell=True)` → clean (a5); non-literal `lib.run(mk())` → clean with `unparsed_spawns: 0` (a6). Contrast: the bare-name form (`run(['pacman','-S','x'])` → lead) and the from-import form (`from lib import run; run([...])` → lead) both behave as documented (g4-lead-bare, g4-lead-fromimport pass).

Root cause: `helper_argv_leads` is only invoked when the callable is an `ast.Name` — `tools/mado-tripwire.py:1823-1828` (`if info.get("kind") in ("unresolved", "external", ...) : if isinstance(node.func, ast.Name): hits.extend(helper_argv_leads(...)); continue`). An `ast.Attribute` call on an external module binding (kind `"external"`, assigned in `callable_info`, `tools/mado-tripwire.py:1500`) falls through the branch silently.

A command-shaped literal argv handed to `somemodule.run(...)` is entirely invisible. The docstring promises a lead for exactly this shape.

Suite gap: `grep -rl "import lib|from lib import|lib\.run"` over `.ufo/waves/round-20/precision/` and `precision-heldout/` finds **no case** — the 175-case precision suite does not cover the module.attr form either, so C1's 172/175 does not measure this hole. [INFERENCE] The likely intent was the bare/from-import name form; the sentence as written is broader than the code.

### F3 — MEDIUM, over-detection: "Uncalled helpers do not establish an execution path" is false for shell functions

Docstring `tools/mado-tripwire.py:40-41`: *"`$1..$9` and `$@/$*` are substituted for shell functions. Uncalled helpers do not establish an execution path."*

A shell function that is defined but **never called** yields an observed finding from the definition line itself:

```
$ python3 -I tools/mado-tripwire.py --scan a1.jsonl   # bash: f() { pacman -S hyprland; }
MADO_TRIPWIRE: findings
{"rule": "pacman:-S", "evidence": "observed", ...}    (exit 1)
```

Also multi-line `f() {\n  pacman -S hyprland\n}` uncalled → finding (r3a); two uncalled defs → findings (r3e). For Python the sentence holds: `def f(): subprocess.run(['pacman','-S','x'])` never called → clean (r3d, and g3-uncalled in round 1).

Mechanism: `(` `)` are shlex punctuation so tokens are `['f','()','{','pacman','-S','hyprland',';','}']`; `segments()` splits at `;` giving `['{','pacman','-S','hyprland']`; `{` and `}` are in `KEYWORDS` and stripped by `strip_prefix` (`tools/mado-tripwire.py:427-431`, KEYWORDS table includes `{`,`}`), so the def body is classified as a standalone executed command. The docstring nowhere states that definition bodies are classified.

### F4 — MEDIUM: "`git` subcommands hidden in aliases, shell functions or scripts are outside the class" is false for shell functions

Docstring `tools/mado-tripwire.py:68-70`. Probe:

```
$ python3 -I tools/mado-tripwire.py --scan a3.jsonl   # bash: g() { git add x; }   (never called)
MADO_TRIPWIRE: findings
{"class":"vcs_write","rule":"git:add","evidence":"observed"}   (exit 1)
```

Same root cause as F3. Also `case $x in a) git add .;; esac` → `git:add` (r3f) — not a helper at all, and the branch body need not execute. The alias member holds: `alias ga='git add'; ga .` → clean (a2, r4b). The scripts member holds: `printf '%s\n' 'pacman -S hyprland' > s.sh; bash s.sh` → clean (r4a).

### F1 — MEDIUM, misstated limit (code is stricter than documented): "python -c bodies … are not analysed"

Docstring `tools/mado-tripwire.py:31-33`: *"`clean` means no finding in the covered forms. It never means 'no host command ran': … python -c bodies, other tools and other sessions are not analysed."*

The code **does** analyse `python -c` bodies:

```
$ python3 -I tools/mado-tripwire.py --scan a7.jsonl   # bash: python3 -c 'import os; os.system("pacman -S hyprland")'
MADO_TRIPWIRE: findings
{"argv0":"pacman","rule":"pacman:-S","evidence":"observed"}    (exit 1)
```

Root cause: `classify_segment`'s python branch runs `nested_eval(code)` on `-c` bodies — `tools/mado-tripwire.py:1106-1111` and the legacy path at `:1121-1124`. Direction of error: over-detection (safe direction), but the stated limit is factually wrong for the code. The same bullet's "aliases not bound in the scanned text" member is misleading in the same way: a same-text alias use is also not expanded (`alias ga='git add'; ga .` → clean, r4b) — the qualifier implies bound ones would be, and none ever are. [INFERENCE] this bullet predates the r20 `-c` analysis and was not updated.

### F5 — LOW, boundary ambiguity: "followed through its body up to four nested helper calls"

Docstring `tools/mado-tripwire.py:36`. Pinned boundary (helper chain f1→…→fk, spawn in fk, call f1; `depth < 4` at `tools/mado-tripwire.py:1823`): chains of 4 total helpers (entry + 3 nested) reach the spawn (k=4 observed); 5–7 total do not (no finding). The sentence is true only under the reading that the entry helper counts as one of the "four nested helper calls"; under the strict reading (four nested below the entry) it overstates by one. Report as ambiguity, not falsehood.

## Claims that held (probe-verified)

Every item below has at least one passing probe; probes are reproducible from the cited scripts (`/tmp/mado-r20w2-RevDocstring/probes/harness.py`, `r2.py`); 204 scan cases total, all findings across every probe carried `evidence` ∈ {`observed`,`lead`} (asserted globally, zero violations).

- **Classes**: host_mutation (`pacman -S`), package_query (`pacman -Qs`), live_probe (`journalctl`), tool_install, vcs_write all fire. Eval forms: `!` shell lines, `%%bash` cells, literal `subprocess.*`/`os.system`/`tool.bash` spawns; JS eval cells → `eval_unparsed` only.
- **tool_install**: all listed channels (uv tool install/run, uv pip install, uvx, pip/pip3, pipx inject, npx, npm exec, npm -g install, cargo install, `python -m pip install`); none of pnpm/yarn/bun/brew/nix/`uv sync`/`uv python install`/go/gem/cargo binstall/deno/`uv run --with`/pnpm dlx/`npm --global=true`/plain download classify; `--permit tool_install` → exit 0 `permitted_only`; `sudo pip install` yields separate host_mutation + tool_install rows; `$UV tool install` invisible; `--user` indistinguishable.
- **Helpers (py)**: def/lambda followed with literal args; async requires direct `await` (async-without-await → no finding); `__init__` and directly resolved methods followed; inherited methods and subscript dynamic dispatch not resolved; cross-cell def following works; `reset` breaks it; uncalled Python defs clean.
- **Variable recipes**: str / `+` / two-arg `str.replace` / lists resolve; earlier-cell persistence; `reset`/`exec`/`from os import *`/`globals()`/rebinding-to-nonliteral all forget (unparsed_spawns); non-literal stays `unparsed_spawns`.
- **Shell helpers**: `$1`, `$@`, `$*` substitution; same-text body followed; cross-text call side not resolved.
- **lead/observed**: bare-name and from-import literal argv → lead; builtins exempt while not rebound, rebinding → lead; leads stay under `findings`; `observed_findings`/`lead_findings` integers correct.
- **vcs_write git**: all 12 write subcommands (`git:<sub>`), `stash list|show` clean, fetch/revert/tag/branch/clean/worktree/gc/config clean; help carve-outs (`--help` anywhere in subcommand options, `git -h|--help <sub>`); commit `--dry-run/--short/--porcelain/--long/-z` clean; add/push `-n/--dry-run` clean; last-wins negations in both directions; `commit -m -h`, `commit -m --dry-run`, `--mess --dry-run`, `--message --dry-run` stay writes; `commit -n` write; `--no-dry` keeps the finding; `commit --no-dry-run` write.
- **vcs_write jj**: mutating set incl. bookmark set/move/delete, op restore, git push/fetch; every-other-subcommand (`jj log`, `jj status`) is a finding; exact `--ignore-working-copy` required (abbreviation `--ignore-working-cop` → finding; before the subcommand works); `help`/`--version`/bare `jj` clean; help after JJ_HELP_VERBS or ahead of the subcommand clean, after a non-listed verb stays a finding, after `--` stays a finding; `describe -m --help` clean vs `-m=--help` write; `jj git push --dry-run` write, with `--ignore-working-copy` clean; `jj-lane.sh …` clean.
- **Boundaries**: toolResult ignored (refused call still counts; result-only command not a finding); canary file never written by any probe (transcript text never executed); only given files scanned; `${IFS}` and shell-variable indirection hide commands (shlex-is-not-bash holds, as stated).
- **CLI**: usage / missing path / no-`.jsonl` dir / invalid line / unknown permit class → exit 2; exit 2 wins over 1; all four `MADO_TRIPWIRE:` labels exercised.
- **--frozen**: the committed round-18 frozen selftest (`.ufo/waves/round-18/tripwire/frozen`, 31 cases) passes in full at 28c6837 (`--selftest` exit 0, `failed=[]`); spot runs confirm `frozen_match`/`snapshot_tampered` (tampered bytes, extra unlisted input, symlink input)/`unpinned_legacy`/`frozen_error` (unreachable line, path traversal)/`frozen_verdict_mismatch` exits and labels exactly as the docstring states.
- **--selftest**: `evidence` in a wanted finding is compared only when specified — a wanted `lead` against actual `observed` fails the case, the same case without `evidence` passes (verified both directions).

## Residual risk

- F2 is the only under-detection gap found: module.attr external calls with literal argv are invisible; a seat (or an attacker-shaped transcript) using `import lib; lib.run([...])` gets a clean verdict where the docstring promises a lead. Recommend L1 either fix the docstring sentence (scope it to bare/from-import names) or extend `helper_argv_leads` to Attribute calls on external bindings; the first is a one-sentence fix, the second touches precision tuning.
- F3/F4 imply precision exposure in the other direction: any transcript that merely *defines* a shell helper with a mutating body is flagged observed. The precision suite has no such case (grep found none), so C1's 172/175 does not price this. [INFERENCE]
- jj snapshot semantics ("every other subcommand snapshots") are jj-behavior claims, not code claims — not verifiable by `--scan` probes here; the code's classification matched every tested form of the stated rule.

## Limits

- Probes are synthetic minimal transcripts (OMP-shaped JSONL built in `/tmp/mado-r20w2-RevDocstring/probes/`); no real session transcript was executed or parsed beyond tool input.
- Not probed: metaclass/descriptor dispatch, `jj` behavior against a real jj binary, git 2.56.0 option tables against the real git, `--frozen` provenance honesty (docstring itself declares it unchecked), redaction patterns (not a docstring claim).
- The round-18 frozen selftest passing at 28c6837 was taken from committed bytes in my clone; I did not re-derive each of its 31 pins by hand — the aggregate pass plus 8 spot runs is the evidence.
- Two round-2 check failures (e1/e2) were bugs in my own assertion indexing, corrected and re-verified manually: the selftest evidence behavior **matches** the docstring.

## Installs

none
