# RevIndexGate — reviewer report (mado round 36, wave 1)

Seat: `L1Mado36.RevIndexGate`. Scope: run `quality/check-index.py` and
`quality/check-index-rows.py` with `--repo .`, record summary lines, exit
codes, and the `master` knowledge-note count. All commands run read-only at
`cd /home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD
`dbf8b579aeac0f023aaf595770f1cb0049e4baa2` ("round-36: freeze both predicates,
the control manifest, the cribs and the before receipts"). Worktree carries
only untracked round-36 wave files; no production file touched.

## 1. Existence check — PASS (both present)

```
-rwxr-xr-x 1 vgpnk vgpnk 19007 Oct 24 04:18 quality/check-index-rows.py
-rwxr-xr-x 1 vgpnk vgpnk 14428 Oct 24 04:20 quality/check-index.py
```

## 2. Literal assigned invocation — both fail setup (FINDING)

```
$ python3 -I quality/check-index.py --repo .
SETUP_ERROR: --rev or --root is required      (stderr, exit 2)

$ python3 -I quality/check-index-rows.py --repo .
SETUP_ERROR: --rev or --root is required      (stderr, exit 2)
```

The assigned command (mirroring registration.md:156's harm-watch line
`python3 quality/check-index.py --repo .`) cannot run as written: `--repo` only
qualifies `--rev` mode (`check-index.py:338` `default="."`;
`check-index.py:353-355` refuses `--repo` alone). The gate's own help text
documents the real contract: `--rev REV`, `--repo REPO` (for `--rev` mode),
`--root ROOT` (filesystem mode).

Verdict: **exit 2 both** — not a gate failure of the index, a stale command
shape in the harm-watch/assignment text. `registration.md` means "the index
gate stays complete"; the correct one-word fix is `--root .` or adding
`--rev HEAD`.

## 3. Intended invocation — both PASS

```
$ python3 -I quality/check-index.py --repo . --rev HEAD
MADO_INDEX: rev=HEAD indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
EXIT=0

$ python3 -I quality/check-index-rows.py --repo . --rev HEAD
MADO_INDEX_ROWS: rev=HEAD rows=50 errors=0 warns=3
WARN cited-glob-nomatch: `.ufo/evidence/round-12/getprop-*.txt` in row knowledge/window-rule-effects-getprop.md
WARN cited-glob-nomatch: `.ufo/evidence/round-12/drift-*.txt` in row knowledge/config-drift-r12.md
WARN cited-glob-nomatch: `.ufo/waves/round-24/fetch/S###.bin` in row knowledge/rule-attribution-r24.md
EXIT=0

$ python3 -I quality/check-index.py --root .
MADO_INDEX: root=. indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
EXIT=0

$ python3 -I quality/check-index-rows.py --root .
MADO_INDEX_ROWS: root=. rows=50 errors=0 warns=0
EXIT=0
```

## 4. Knowledge notes at `master` — 50


```
$ git ls-tree --name-only master:corpus/knowledge | wc -l
50
```

Directory listing confirms 50 `.md` notes (animation-table-r26.md …
xdg-portal-routing-r12.md), matching both gates' `indexed=50/50` /
`rows=50`. Consistent: index complete, zero missing/dangling/duplicate rows.

## 5. FINDING — rev-mode `exists_glob` is broken under host git (warns=3 are false positives)

`check-index-rows.py:96-98` runs:

```py
_git(repo, "-c", "core.quotepath=off", "ls-tree", "-r", "-z",
     "--name-only", "--format=%(path)", sha, "--",
     os.path.dirname(pattern) or ".")
```

On the host's git 2.56.0 this dies immediately:

```
$ git -c core.quotepath=off ls-tree -r -z --name-only "--format=%(path)" HEAD -- .ufo/evidence/round-12
fatal: --format can't be combined with other format-altering options
```

`exists_glob` swallows the `CalledProcessError` and returns `False`
(`check-index-rows.py:101-102`), so **every** glob-pattern citation in any
rev-mode run reports `cited-glob-nomatch`. Proof the warnings are spurious:
`.ufo/evidence/round-12/getprop-help.txt` and `getprop-measure.txt` are
committed at HEAD (`git ls-tree -r HEAD .ufo/evidence/round-12/` lists both),
`drift-hypr.txt`/`drift-precedence.txt` likewise, and `S###` re-patterned to
`S[0-9][0-9][0-9]` matches the 16 committed members of
`.ufo/waves/round-24/fetch/` at HEAD (`S153.bin`…`S168.bin`; 17 files on disk,
one untracked). `--root .` mode resolves the same three
citations cleanly: `warns=0`.

Severity: **low-but-real instrument drift**. Warns are non-fatal (exit 0), so
the gate does not falsely fail anyone — but it cannot currently *confirm* any
glob citation in rev mode; every glob is silently downgraded to a warning. If a
future gate promoted these warns to errors, rev mode would go false-red.
Fix direction (not applied — read-only seat): drop `--name-only` when
`--format` is given (the format already emits `%(path)`), or stop passing
`--format` entirely and use `--name-only` output.

## 6. Summary table

| Item | Command | Output | Exit | Verdict |
|---|---|---|---|---|
| check-index.py exists | `ls -la quality/check-index.py` | 14428 bytes, executable | — | PASS |
| check-index-rows.py exists | `ls -la quality/check-index-rows.py` | 19007 bytes, executable | — | PASS |
| Literal assigned cmd | `python3 -I quality/check-index.py --repo .` | `SETUP_ERROR: --rev or --root is required` | 2 | finding: stale invocation text |
| Literal assigned cmd | `python3 -I quality/check-index-rows.py --repo .` | `SETUP_ERROR: --rev or --root is required` | 2 | same |
| Index gate, rev mode | `--repo . --rev HEAD` | `indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 | PASS |
| Rows gate, rev mode | `--repo . --rev HEAD` | `rows=50 errors=0 warns=3` (all glob warnings spurious) | 0 | PASS with instrument bug |
| Index gate, root mode | `--root .` | `indexed=50/50 … coverage=10.0000/10` | 0 | PASS |
| Rows gate, root mode | `--root .` | `rows=50 errors=0 warns=0` | 0 | PASS |
| Note census | `git ls-tree --name-only master:corpus/knowledge \| wc -l` | `50` | 0 | 50 notes |

## Residual risk / gaps

- Did not run the gates' `--selftest` (outside the assigned command set;
  flag available if a later seat wants fixture-level coverage).
- The rev/root `warns` divergence (3 vs 0) is fully explained by the
  `--name-only`+`--format` git incompatibility; no second cause needed, but a
  gate that treats warns as errors would inherit the failure.
- `registration.md`'s harm-watch phrasing `--repo .` should be read as
  "the index gate in its working invocation"; the bytes as written exit 2.

No tools installed this seat (none needed; pacman untouched). No writes
outside this report.
