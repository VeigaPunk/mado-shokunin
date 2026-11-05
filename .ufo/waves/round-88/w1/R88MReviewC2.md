# R88MReviewC2 — attack report on C2 (include= containment)

Seat: R88MReviewC2 (reviewer, attack). Scope: candidate `build/mado-mako.c2.py`, counter `quality/counters/c2-r88-include-containment.py`, case file `controls/containment-cases-r88.json`, mutants `controls/containment-mutants-r88.json`.
Constraint honoured: the candidate tool was NOT run (no candidate scoring). Everything about the candidate below is static reading plus stdlib probes.

## Verdict in one line

No high-severity containment bypass found in the candidate's logic on the classes examined. The defects are in the **measurement** (the counter's kill rule and the case/mutant coverage), in **named limits the declaration does not state** (TOCTOU, hardlinks, bind mounts), and in **robustness and expansion details** (NUL crash, `--home ""`, `~//`, trailing slash).

## What was checked and held (static, candidate L259-264, L409-440, L443-460, L636-679)

- Realpath is taken before the containment test (L420-421), and `stat` (L426) and `load` (L439) use `real`, never the unresolved `target`.
- Prefix test uses a separator (L260-263: `root + os.sep`); `real == root` covers the root itself; root `/` yields prefix `/`, correct.
- `--home` and each `--read-root` are `realpath`ed (L446-447), so a symlinked root or symlinked home compares like with like.
- `~` alone, `~user/`, and relative includes are refused before containment (L416-418).
- Include cycles are detected on resolved paths (L434; `stack` seeded with `realpath(config)`).
- `/proc/self/root/...` and `/dev/stdin` are resolved by `realpath` into the real path, so they are checked like any other path. Probe: `realpath('/proc/self/root/etc/hostname') = /etc/hostname`, which is refused for a home-only root.
- A self-loop symlink yields `stat` ELOOP (errno 40) and is refused as unreadable, not read.
- `--config` is `realpath`ed in `main` and not subject to roots, as the stance says.

## Findings

Severity scale: High = escape or false TARGET_MET reachable; Medium = predicate or measurement can pass wrongly / declared class not measured; Low = robustness, divergence, or wording; Info = separability note.

### F1 — Medium — counter counts a crashing mutant as "killed" (predicate integrity)
- Where: `quality/counters/c2-r88-include-containment.py`, `evaluate()`, the line `hit = run_all(mutant, cases, places, gen)[0] != verdicts` (between L176 and L189). `tool_verdict` (r87 counter L228-232) returns False for any non-zero exit, so a crash produces an all-False verdict vector that always "differs".
- Reproduce (in-process, fixture tool only, scratch-rooted): mutant `("import-break", "import argparse, json, os", "import argparse, json, os (")` — a syntax error on a line unrelated to containment — gives `status: killed, killed: 1, correct: 3/3`.
- Impact: the predicate's "all M mutants killed" can be satisfied by any build that crashes on every input, including a broken candidate. K1–K5 are semantic anchors so there is no current exploit, but the metric does not measure what the declaration says it measures.
- Fix: a mutant is killed only when it exits 0 with JSON on every case AND its verdict vector differs. Any crash or timeout is a new status `crashed` that fails the predicate (or at least is reported and not counted). Add a fixture selftest for the import-break mutant that must NOT be killed.

### F2 — Medium — declared escape class not measured: `..` after a symlinked directory
- Stance text says "every symlink and `..` resolved" (declaration C2; candidate L17-19). No case exercises `..` that follows a symlink, which is exactly where lexical and physical resolution diverge.
- Probe (stdlib, scratch): with `home/linkdir -> outside/sub`, `realpath(home/linkdir/../secret.ini) = outside/secret.ini`, but `abspath(...) = home/secret.ini`.
- Repro input (proposed case k18): files `home/config.ini` = `width=118\ninclude=~/linkdir/../secret.ini\n`; `home/linkdir` symlink to `outside/sub`; **decoy** `home/secret.ini` = `width=A`; `outside/sub/../secret.ini` i.e. `outside/secret.ini` = `width=B`. Expect `width=118`, refusals present.
- Why the decoy matters: a `normpath`-before-`realpath` implementation reads `home/secret.ini` (applies A) and diverges from expectation; without the decoy it would just refuse as "missing" and survive.
- Fix: add k18 plus a mutant `K6-normpath-first` (`real = os.path.realpath(os.path.normpath(target))`, anchored on the candidate's L420 line or its neighbourhood, distinct from K2's anchor text).

### F3 — Medium — the directory-only check class is killed by exactly one case, and no mutant covers it
- Probe: built a hostile fixture tool (in a fixture repo under my scratch, not the candidate) whose check uses `realpath(dirname(target)) + basename(target)` and then opens that path. Result of the counter against it: FAIL k01 only; k02 (symlinked directory) passes it.
- So the class "resolves the directory, not the final component" is caught only by k01. One case is a thin kill, and there is no mutant for it.
- Fix: add mutant `K7-final-component-unresolved` (replace the L420 `realpath(target)` with the dirname-realpath + basename join; anchor it on the two-line block including L421, not on K2's anchor). Keep k01 and add a second case: directory-symlink is not enough, so pair a final-component symlink inside a symlinked directory (`home/linkdir/final.ini -> outside/x`).

### F4 — Medium — declared stance has untested escape classes
Not in `containment-cases-r88.json` (all 17 cases reviewed; k01–k17 listed by ID):
- (a) absolute path containing `..`: `include=@ROOT@/home/../outside/esc.ini` (absolute analogue of k03). Expect width pre-include, refusals present.
- (b) `/proc/self/root` magic path: `include=/proc/self/root@ROOT@/outside/esc.ini`-style, i.e. `/proc/self/root` + absolute outside path. Expect refused. Verified `realpath` resolves it to the plain path.
- (c) second-hop chain leaving home through a symlink chain: `home/l1 -> home/l2 -> outside/esc.ini`. k17 covers only the inside chain.
- (d) symlink self-loop inside home (ELOOP path). Expect refused as unreadable (stat error), refusals present.
- (e) read root given as a symlink, then included via the link path. Expectation is ambiguous (see F9); needs an explicit ruling in the stance before a case is authored.
These are additive; none needs a candidate change to have a defined expectation except (e).

### F5 — Low — NUL byte in an include path crashes the resolver instead of refusing
- Where: candidate L420, `os.path.realpath(target)` is called outside any `try`. Probe: `os.path.realpath("/x\x00y")` raises `ValueError: lstat: embedded null character in path`.
- Repro input: a config file whose include line contains a NUL byte, e.g. `include=~/a\x00b`. Expected under the stance: refusal. Observed (static): uncaught `ValueError`, traceback, exit 1 (no containment breach: nothing is read).
- Fix: wrap the realpath in `try/except ValueError` and refuse. Add a case with `\u0000` in the JSON content so the refusal is measured.

### F6 — Low (named limit missing) — TOCTOU and identity limits are not stated; "resolved path is what is opened" holds only without a concurrent writer
- Where: candidate L420-421 (check), L426 (`os.stat(real)`), L439 (`self.load(real)`). The check, the stat and the open are three separate path-string lookups. A process running as the same user that can write under HOME can replace a path component with a symlink to outside between L421 and the open at L439, or swap the regular file for a FIFO between L426 and the open.
- The counter cannot measure this. A mutant "open `target` instead of `real`" (K-candidate) survives unless a race is injected, so the stance clause "the resolved path is what is opened" is untested as written.
- Hardlinks and bind mounts: a hardlink from inside the root to an outside inode (for example, a credential file under HOME-adjacent paths) is read; `realpath` is path-based and cannot see it. Bind mounts are the same.
- Threat model note: the config's own text cannot create hardlinks or symlinks, so these are outside the attacker model "untrusted config content". They must still be named.
- Fix (choose one, state it in the declaration): (i) named limit: "single-writer HOME assumed; hardlink, bind-mount and TOCTOU identity are not covered"; or (ii) open once with `os.open(real, O_RDONLY|O_NOFOLLOW)`, `os.fstat` for regular-file, and verify `os.path.realpath(f"/proc/self/fd/{fd}")` is inside a root before reading. Option (i) is the honest minimum for this round.

### F7 — Low — `--home ""` and relative `--home` / `--read-root` are accepted and resolved against the process cwd
- `--home ""`: candidate L440-446 and `include()` L411 check `self.home is None`, so `""` passes that check, `roots` becomes empty (`if home else []`), and `~/x` becomes the relative target `x`, resolved against cwd. Containment still holds (only declared roots cover cwd), but the trust boundary is cwd-dependent.
- Relative `--read-root`: `os.path.realpath(root)` (L447) is cwd-relative, so the declared boundary depends on where the tool is invoked.
- Repro: `cd /some/dir && python3 -I tools/mado-mako.py --config C --home ''` with `include=~/x`.
- Fix: `setup_error` when `--home` is given but empty or relative, and when `--read-root` is relative. Document the absolute-path requirement in the usage line (L64).

### F8 — Low — expansion divergences (no containment effect)
- `~//abs`: `os.path.join(home, value[2:])` (candidate L414) discards `home` when `value[2:]` starts with `/`. Probe: `join(home,'/etc/passwd') = /etc/passwd`. Result: `include=~//etc/passwd` is refused (outside), but `include=~//<home-absolute>/x.ini` is read as that absolute path, not as `$HOME//...`. Containment holds; semantics diverge.
- Trailing slash: `include=~/inc.ini/` — probe `realpath(f + '/') = f`, `isfile(f + '/') = False`; the candidate's `stat(real)` then reads the regular file. mako's open would fail with ENOTDIR. The candidate accepts what the manual's model should refuse.
- Fix: refuse `~//` and trailing-slash on non-directories, or join as `home + '/' + value[2:]` and refuse trailing slash. Add cases only after the expectation is sourced (see F9); mako's manual does not define these forms.

### F9 — Low — control fidelity: the `base-tool` control fails three cases for an argparse reason, not a containment reason
- The round-87 resolver has no `--read-root` option. The counter's `run_tool` (counter `run_tool` L129-139) appends `--read-root` for any case that declares roots, so the base tool exits 2 on k07, k13 and k14. `base_tool_correct=8` therefore mixes "reads escapes" with "rejects an unknown flag".
- Measured (my fixture runs, base = r87 text): base_tool_correct=8 and refuse_all_correct=8, both < 17, so the predicate is not wrongly met here. But the control does not measure "candidate minus containment".
- Fix: use `mutant K1 applied` (the candidate with `if not self.within_roots(real):` replaced by `if False:`) as the "no-containment" control. It accepts every flag, reads escapes, and fails for the containment reason. Keep the refuse-all forgery as is.
- Also (ambiguous expectation, see F10): the stance does not rule on a symlinked read root (case e in F4).

### F10 — Ambiguous expectation and stance wording (for the freeze)
- Read root that is itself a symlink: the candidate resolves the root (L447), so an include via the link path is accepted when its target lies under the link's target. The stance says "a declared read root" without saying whether the root is resolved. Rule it explicitly (recommended: resolve roots, as the candidate does, and say so in the stance).
- `k06` expectation (width 206 applied, refusals present): consistent with "content is read at the directive position" (r87 L45-50 semantics); I agree with it. Noted so the L1 does not misread the 206 as a leak.
- The stance's pin for `k03` (path_resolution L141-143) is accurate: L141-142 states the conventional `..` meaning.

### F11 — Info — separability (C1 vs C2) checked
- r87 frozen cases: exactly one `include=` line in `.ufo/waves/round-87/controls/mako-cases-r87.json` (L243 `c13-include-globals-under-home`, `include=~/.config/mako/core.ini`). It is a `~/` include under `--home`; its target lies inside the realpathed home, so it is unchanged under C2. Verified by grep (no run).
- Absolute includes with no `--home` / no roots are now refused (r87 applied them). No frozen case uses this form, so there is no frozen-case regression. The stance requires it.
- Host config chain (metadata only, `~/.config/mako/config`): one line `include=~/.local/share/omarchy/default/mako/core.ini`. Its realpath is itself, it is not a symlink, and it lies inside HOME. Under `--home=$HOME` it resolves under C2, so the host DND include is not blocked by containment.
- C1 case file `mako-cases-r88.json` is not present yet (checked at `.ufo/waves/round-88/controls/`); the claim "C1 cases never pass `--read-root` and every include stays inside `--home`" cannot be verified until it is authored. L1 must check it at freeze.

## Counter and case-file checks (what passed)
- `--selftest --scratch-root $S` (command: `python3 -I quality/counters/c2-r88-include-containment.py --selftest --scratch-root <S>`): exit 0, `SELFTEST: passed=12/12`. Receipt: `.ufo/waves/round-88/w1/R88MReviewC2.c2-selftest.txt`.
- r87 counter sha256 pin verified at load: `4d801c30b302ed5972142415012d8f461109459d9c44e85e0badef57a2ed3645` (matches `R87_COUNTER_SHA256`).
- Case file sha256 (read-only, for the freeze): `3ee0dc9be8b313b788e17bceccd9366b84b74c76adaccf33bf5446e253d766f2`, 17 cases (K in 12..24).
- Mutants file sha256: `49373eeeceef5ae6e76bfc7327f9f511ceef0e9fd4a8b3aadafeee8c6a084a85` (matches the declaration's pin), M=5.
- Mutant anchors, each exactly once in the candidate (`grep -cF`, static): K1 `if not self.within_roots(real):` = 1; K2 `real = os.path.realpath(target)` = 1; K3 `if real == root or real.startswith(prefix):` = 1; K4 `roots.extend(os.path.realpath(root) for root in read_roots)` = 1; K5 `roots = [os.path.realpath(home)] if home else []` = 1. Forgery anchor = K1 anchor (= 1).
- Expectation audit (static, against the stance and path_resolution(7)): all 17 expectations agree with the stance on reading; k01–k09 escape-refuse, k10–k17 positive-apply. path_resolution pins verified: L77-80 (symlink then resolved), L107 (MAXSYMLINKS 40), L141-143 (`..` conventional meanings).

## Counter run against two hostile fixture tools (my own, in a fixture repo under scratch; not the candidate)
Fixture repo verified with `git -C "$D" rev-parse --show-toplevel` = `$D` before commit; throwaway identity used only for those fixture commits; base tool = r87 text.
- H1 `real = os.path.abspath(target)` checked, `realpath(target)` read (lexical check). Counter: FAIL k01 (missing-refusal) and k02 (missing-refusal); correct 15/17; MADO_MAKO_CONTAINMENT: TARGET_MISSED. Shows the set catches the lexical class.
- H2 `real = realpath(dirname(target)) + basename(target)` checked and opened (directory-only check). Counter: FAIL k01 only; correct 16/17; TARGET_MISSED. Shows F3.
- Both fixtures' K2/K4/K5 anchors are absent, so those mutants read `setup-error count=0`; expected for a non-candidate fixture and not a finding.
- Scratch for the fixture repo and counter generations removed (`rm -rf`) after the runs.

## Residual risk and verification gaps
- The candidate was not executed (by constraint). All candidate behaviour above is static reading plus stdlib probes. L1 should confirm F1 (crash-as-kill) and F5 (NUL) by running the freeze-time counter, not from this report.
- F6 (TOCTOU) cannot be measured by the counter; it is a named-limit decision for the declaration.
- Counter predicate `TARGET_MET` was not evaluated on the candidate; no verdict is given here.

## Install and tool record
- No installs or upgrades. Read-only `git show` on the lane base for the r87 tool text (scratch copy); fixture-only git commits in a scratch repo.
- No pacman, no sysctl, no ~/.local/bin changes.

## Receipts
- `.ufo/waves/round-88/w1/R88MReviewC2.c2-selftest.txt` (selftest, 12/12, exit 0).
- Scratch `S=/fast/scratch/hyaku/mado-r88/R88MReviewC2/` removed on exit.
