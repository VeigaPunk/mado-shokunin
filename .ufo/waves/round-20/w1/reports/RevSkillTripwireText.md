# RevSkillTripwireText — E1–E4 require evidence-aware tripwire wording

## Findings

### Moderate — E1: the prose presents every finding as an observed command

`SKILL.md:530-531` calls a finding “an issued command”; `SKILL.md:591-593` says the tool “records commands *issued*”; and `tools/mado-tripwire.py:2-6,27-28` describes classifying commands issued and says issued/refused/successful calls count. Under E1, a `lead` row only establishes that a literal host-command argv was passed to an opaque helper. It does not establish that the helper ran it. The old text collapses that distinction.

Suggested replacements:

- `SKILL.md:530-531`: “Every finding row carries `evidence`: `observed` or `lead`. `observed` means the transcript states both the command and the path that runs it. `lead` means a literal positional host-command argv was handed to a helper whose body is not visible; disclose it as a lead, not as proof the command ran or changed host state. Confirm package transactions against `/var/log/pacman.log` by timestamp (UTC in transcripts, -0300 in the log) using the call's `custom/tool_execution_start` time — a record's own timestamp can be minutes late for provider-history records holding many calls.”
- `SKILL.md:591-593`: “It records observed command paths and literal-argv leads (tool results are ignored): refused and successful observed calls both count; a lead records an opaque-helper handoff, not confirmed command execution.”
- `tools/mado-tripwire.py:2-6`: “Records observed command paths and literal-argv leads in assistant `toolCall` blocks: `bash` (`arguments.command`) and Python `eval` (`arguments.code`: `!` shell lines, `%%bash` cells and literal subprocess/os/tool.bash spawns parsed with `ast`, never executed), including spawn aliases bound in the text and literal argv calls through visible helpers. Each finding carries `evidence: observed|lead`; only `observed` establishes that the transcript states the command and path that runs it.”
- `tools/mado-tripwire.py:27-28`: “Observed means issued, not necessarily executed: `toolResult` records are ignored (a refused and a successful observed call both count). A lead means only that literal host-command argv was passed to an opaque helper.”

E1 also adds integer `observed_findings` and `lead_findings` to the verdict. `SKILL.md:527-530` still asks readers to quote the first line, `counts`, and `unparsed_spawns`; that is not false, but it should additionally name both new counts so the documented reporting step preserves the distinction.

### Moderate — E1: the stated blind spots contradict visible Python aliases and cross-cell helpers

`tools/mado-tripwire.py:31-33` says “aliases” and “helpers defined in one text and called from another” are not analysed. E1 explicitly recognizes spawn aliases bound in the text (`run = subprocess.run`, `partial(...)`, and `from subprocess import run as r`) and visible helper bodies in the same cell or an earlier Python `eval` cell of the same file when no `reset` intervenes. The same-text-only phrasing at `tools/mado-tripwire.py:35-40` remains true for that subset, but omits the new cross-cell, `async def`, lambda, and decorated-helper cases.

Suggested replacement for the affected limitations/capability text: “Python spawn aliases bound in the scanned text and visible `def`/`async def`/lambda helper bodies are followed when called with literal argv in the same cell or an earlier `eval` cell of the same file, unless a `reset` intervenes. Calls with literal host-command argv to an unbound name or an import from outside the known-pure stdlib set whose body is not visible are `lead` findings. Shell functions and shell aliases, Python `-c` bodies, scripts written then run, other tools and other sessions remain outside this analysis.” This also scopes the currently unqualified `aliases` at `SKILL.md:596` to shell aliases, avoiding confusion with the newly covered Python spawn aliases.

### Moderate — E2/E3: Rule B and pure-call prose is no longer an accurate classifier description

`tools/mado-tripwire.py:41-50` describes leads as calls to a bare name that is not a same-text helper or spawn function, then identifies only `print`/`json.dumps`-style `PURE_ARG_CALLS` as exemptions. It does not limit leads to opaque callees, omits the expanded pure set and visible no-spawn callables, and makes no mention that exemptions depend on the binding at the call site. Under E2, pure builtins/stdlib and visible no-spawn classes/functions can be exempt; under E3, rebinding removes the exemption, the latest preceding binding wins across cells, and `del`/`reset` unbinds the name.

Suggested replacement for `tools/mado-tripwire.py:41-50`: “A literal positional host-command argv handed to an unbound name, or to a name imported from outside the known-pure stdlib set, is a `lead` only when the callee body is not visible. An unrebound Python builtin is pure; known-pure stdlib callables are `collections.*`, `shlex.join`/`quote`/`split`, `json.dumps`, `pprint.pformat`/`pprint`, `textwrap.*`, `dataclasses.*`, `itertools.*`, `operator.*`, `string.*`, `enum.*`, `typing.NamedTuple`, and `functools.*` except `partial`/`wraps` over a spawn. A visible class, dataclass, `NamedTuple`/`namedtuple`, lambda or function is exempt when its body has no spawn and makes no call that would be observed or lead (transitively, to depth 4). Attribute/method calls such as `' '.join(argv)` remain unflagged. A visible helper call whose literal argv reaches a spawn is `observed`, not a lead. Binding is call-site sensitive: the latest preceding `def`, lambda, assignment or import wins across cells; `del` or `reset` unbinds the name, after which a literal-argv call to it is a lead. Only literal positional argv lists are inspected; keyword `args=[...]` remains outside this rule.”

The round-19 note at `SKILL.md:1877-1878` (“heuristic lead, not a proof of execution”) remains true as a historical statement about round 19. It should not be rewritten as though round 19 already had E1–E3 behavior; add a round-20 note describing the current evidence and binding rules instead.

### Moderate — E4: the `vcs_write` description omits help-only and dry-run exclusions

`tools/mado-tripwire.py:59-68` says git write subcommands are covered and jj subcommands snapshot unless `--ignore-working-copy`, with only `help` and `--version` excepted. This overstates findings for help-only invocations and dry runs, including `git add -n`, `git commit --dry-run`, `git push -n`, jj help flags, and `jj git push --dry-run`.

Suggested replacement for the `vcs_write` paragraph: “`vcs_write` covers actual version-control writes and jj working-copy snapshots. Git write verbs are `add`, `commit`, `stash`, `checkout`, `switch`, `reset`, `pull`, `push`, `restore`, `rebase`, `merge` and `cherry-pick`; do not report help-only `git <sub> -h|--help`, `git --help <sub>` or `git help ...`, or dry-run `git commit --dry-run`, `git add -n|--dry-run` and `git push -n|--dry-run`. `git commit -n` remains a write (`--no-verify`), and `-m --help` treats `--help` as the option value. For jj, retain the mutating-subcommand and implicit-snapshot rules, except do not report `jj ... -h|--help` when the token is a flag (not an option value), `jj help ...`, or `jj git push --dry-run`. A `jj-lane.sh` helper invocation remains clean.”

## Residual risk and verification gaps

- `git diff -- SKILL.md tools/mado-tripwire.py` and `git diff --cached -- SKILL.md tools/mado-tripwire.py` produced no output, so these two files have no current staged or unstaged diff; this is a contract-vs-current-text audit, not review of landed E1–E4 edits.
- `SKILL.md` SHA-256: `41287d7ee07bafb425445e69dfe1162f5753fdcdd6fa15e0875f8fa8e19d1b84`. `tools/mado-tripwire.py` SHA-256: `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.
- No `lsp` device is mounted (`read xd://lsp` returned “No such tool”); used literal grep/read output as text evidence, not semantic proof. No tests or runtime checks were run.

## Limits

Reviewed only the requested tripwire prose in `SKILL.md` and the `tools/mado-tripwire.py` module docstring against E1–E4. Did not audit implementation behavior or the wider gate registry.

## Installs

none
