# ReviewProvinceDraft — PROVINCE round-27 correction & mado-binds.py docstring vs code

Scope: PROVINCE.md last paragraph (Round-27 correction, M26-10) and the
`tools/mado-binds.py` docstring "Environment limit" paragraph, checked against
the tool's code and a scratch probe tree. Leaf seat, no subagents. No compositor
started (coredump delta: n/a — no Hyprland was launched); nothing written in the
lane except this report; probe tree under `/fast/scratch/hyaku/mado-r27/prov/`.

## Findings (by severity)

### None — no actionable defect found

Every claim in both paragraphs matches the code and the observed behavior.

## Claim-by-claim verification

Lane observed at tip `8e72db7` (assignment context said `2fdca5ca`; the lane has
moved — `a496b02a` is an ancestor of the current tip either way:
`git merge-base --is-ancestor a496b02a HEAD` → OK). Commit evidence:
`git show a496b02a -- tools/mado-binds.py` contains the removal
`-        self.env = dict(os.environ)` — i.e. "Since `a496b02a` … does not seed
config variables from `os.environ`" is the right commit attribution.

### 1. "does not read os.environ" — AGREE

- Code: no `os.environ` and no `os.getenv` anywhere in `tools/mado-binds.py`
  outside the docstring (grep: only docstring lines 29–31). `State.__init__`
  seeds `self.variables = []`; `main()` reads only `--home` (no `$HOME` either —
  `HOME[0] = os.path.abspath(home)` comes from argv).
- Runtime probe: the same tree run with `envsrc=…` exported vs `env -i` (no
  variable) produced byte-identical stdout (`diff` empty; receipt
  `/fast/scratch/hyaku/mado-r27/prov/run-withenv.json` and `run-noenv.json`).

### 2. "a `$NAME` supplied only by the environment stays literal" — AGREE

Probe config line `bind = SUPER, E, exec, show $envsrc` (with `envsrc` exported)
yields `"arg": "show $envsrc"` — the literal `$envsrc` survives into the output
bind table.

### 3. "`source = $VAR` using only an environment value is not followed" — AGREE

Probe config line `source = $envsrc`; the target
`prov/outside/envsrc.conf` contains `bind = SUPER, Z, exec,
from-env-source-should-not-appear`. Output has 5 binds, none with key `Z`;
markers `from-env-source-should-not-appear` and `envsrc.conf` are ABSENT from
the JSON. Code path: `parse_line` expands only names in `st.variables`, so
`handle_source` receives `$envsrc`; `absolute_path` gives
`<sourcing dir>/$envsrc`; `glob.glob` matches nothing.

### 4. "Variables declared in the config tree still expand" — AGREE

`$cfgvar = exec-echo-cfg` + `bind = SUPER, C, exec, $cfgvar` →
`"arg": "exec-echo-cfg"`; `$cfgsrc = …/outside/cfg.conf` + `source = $cfgsrc`
is followed (`SUPER, G → from-cfgvar-source` appears, from a file reached only
through the config-declared variable) and `bind = SUPER, F, exec, $cfgsrc`
expands to the full path in the arg.

### 5. "absolute `source =` paths are still followed anywhere" (still leaves DIR) — AGREE

Probe config line `source = /fast/scratch/hyaku/mado-r27/prov/outside/abs.conf`
— outside the probe `--home` tree — is followed: `"key": "A", "arg":
"from-absolute-source"` appears. Code: `absolute_path` returns a `/`-leading
rawpath unchanged (mado-binds.py:757-758) and `handle_source` globs + reads it.
Docstring main body (lines 5–9) documents `~` → DIR, globs, relative joins; the
follows-anywhere absolute behavior is stated in the PROVINCE round-25 residual
paragraph and round-27 keeps it. Bonus probe (same escape family): relative
traversal also leaves DIR — `source = ../../../outside/rel.conf` in
`prov/home2/…/hyprland.conf` produced `SUPER, R → from-relative-traversal`
(`../` handling in `absolute_path`).

## Docstring vs PROVINCE consistency

The docstring "Environment limit (round-27 note, M26-10)" paragraph states
exactly claims 1–4 above and is consistent with the PROVINCE round-27 paragraph
and with the code. No contradiction found between the two texts or either text
and behavior.

## Residual risk / verification gaps

- Stale wording, safe direction only: the round-25 inventory **table row** for
  `tools/mado-binds.py` still reads "no compositor, socket, network or
  environment beyond `HOME`". Since `a496b02a` the tool reads no environment at
  all (not even `$HOME`; `~` maps to the `--home` argument). The round-27
  paragraph supersedes this but does not reword the row; over-claiming a read
  surface is conservative, so not a defect.
- Environment-seeding parity with hyprlang v0.6.8 (which seeds variables from
  the environment) was checked against the tool only, not against a live
  hyprlang 0.6.8 run — the divergence claim ("unlike hyprlang v0.6.8") rests on
  the pinned-source citation in the docstring and is not independently
  re-verified here; it is also outside this item's ask.
- Probe receipts: `/fast/scratch/hyaku/mado-r27/prov/` (tree: `home/`,
  `home2/`, `outside/`, `run-withenv.json`, `run-noenv.json`). All commands
  wrapped in `timeout`, `prlimit --core=0`, `env -i` (no WAYLAND_DISPLAY /
  HYPRLAND_INSTANCE_SIGNATURE anywhere); all started processes exited.

## Verdict

AGREE — PROVINCE.md round-27 paragraph and the mado-binds.py "Environment
limit" docstring paragraph both match the tool's code and observed behavior on
all four checked claims (no os.environ reads; env-only `$NAME` literal;
env-only `source = $VAR` unfollowed; config-declared variables expand; absolute
sources still leave DIR).
