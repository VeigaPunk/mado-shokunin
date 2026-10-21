# OraclePureShlex

Axis: C1 precision.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/PureShlex.json` contains one inert Python eval transcript and expects no findings. Its assigned shape `shlex.join(["pacman", "-Q", "r21"])` is executed at module level.

- `f` is the visible subprocess-spawning function (`subprocess.run(["pacman", "-Q", "r21"])`). It is never invoked: its only reference is the body of `C.cmd`, which is never called.
- `C` defines only the specifically relevant unused method `cmd` — the dormant relay to `f` — and no `__init__`. `C()` therefore constructs an instance through inherited `object` initialization, which spawns nothing and invokes no instance method; the class statement itself executes only its body, which binds `cmd`.
- The executed shape is pure: per CPython v3.14.8 (S107, `corpus/SOURCES.md:119`), `shlex.join` concatenates and shell-escapes the token list and returns a `str`; it has no execution path, so the argv-shaped literal is data, not a command. The same argv also sits dormant inside `f`, so any scan that folds a literal argv into a command pattern would false-positive on the data argument — this is the precision surface the fixture pins.
- No visible body falls in a swept-lead category: `f` and `cmd` are not handed on as values, decorated, returned closures, or dunders of the constructed class; nothing in the executed text references them. The swept and no-row categories are stated in `corpus/knowledge/tripwire-precision-r20.md:29-30`.

## Why the negative is semantically right, not forced

Had the fixture called `f()` (or `C().cmd()`), the transcript would really start `pacman -Q r21` through `subprocess.run`, and an empty expectation would be wrong; such a proposal would have been rejected with that reason instead of written. As composed, every spawn path stays dormant (deferred body of `f`, unused method `cmd`, no `__init__`) and the only executed call is a pure string formatter, so `want: []` is the true expectation — derived from Python execution semantics and CPython shlex semantics, independent of any tool outcome.

## Provenance for the shape

Round-20 precision evidence records argv-as-data misread as a command: the `P-CasePureBuiltins-*` cases in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/evidence/precision-1f7f995.txt` (e.g. `print(['pacman', '-Q', 'hyprland'])` reported as `package_query` rule `pacman:-Q`), and the round-20 knowledge entry pins S107 `shlex.join` on the no-row side. That is provenance for the shape's defect class, not authority for the expected result.

## Verification

Static reasoning only, as assigned. The transcript was not executed and was handled as data throughout; no tripwire run, classifier/gate measurement, build, test, formatter, or lint was performed; no host, package, service, compositor, or VCS state was touched and pacman transactions stayed paused. Tool installations: none.

Report: .ufo/waves/round-21/w1/reports/OraclePureShlex.md
