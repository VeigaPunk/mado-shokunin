# R68ExecGate3 — four standing gates carry the replacement-ref guard

Seat: R68ExecGate3 (leaf executor). Claim: C2 (operability), four of the twelve gate repairs.
Freeze: `e0727cda15621766c35dcf8b70c211b6531aab45`. Base: `510100c81e6cf63fec6be380c2f2f9c670f32cbc`.
Lane HEAD at write time: `40d2bef8964a098ae50f01094fa19e4725952010` (peer commit that added the C1
harness and dispatch evidence only; the four files below are byte-identical at `e0727cda` and
`40d2bef8`, verified with `git show HEAD:quality/<f>.py | sha256sum` against the worktree).

Nothing in this seat is production: drafts live under
`.ufo/waves/round-68/w1/R68ExecGate3/draft/quality/` and the L1 integrates them.

## Axes

- C2 operability: each repaired file moves `guard=no → guard=yes` under the frozen census.
- C1 calibration: untouched (no harness, predicate, control set or recipe was read or changed).

## Files, edits, hashes

Every edit is the guard and nothing else (`env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")`
per call, or one `env[...] = ...` store where the file already builds an env); argv, stdout,
stderr, exit codes and marker texts are unchanged.

| file | object-read sites repaired | diff | draft sha256 |
|---|---|---|---|
| `quality/check-landed-contract.py` | inline `git show` (line 54) | +3/-1 (adds `import os`) | `90bd69e4810c0a084a817a00321fc353c43d161b21e513cb73e3fc1b798dc19a` |
| `quality/check-round-outcome-first.py` | `read_scorecard` `git show` (71), `exists_at` `git cat-file -e` (125) | +3/-1 | `ef0a40b28299cdda12db71e701057a27faceda2c436fc23b08dd3cfbe9894ca3` |
| `quality/check-session-material.py` | `_git` `subprocess.run` (924), `iter_blobs` `cat-file --batch` `Popen` (980) | +2/-0 | `2ca9ee5882fe89b3b798f8a001a0b0acb878cc44d2111970702354a7e118a757` |
| `quality/check-wave-done.py` | `git_env()` (179-189): `env["GIT_NO_REPLACE_OBJECTS"] = "1"` | +1/-0 | `040855fcc82d79e0fdec38e4da4d4fc40586ca6d398201f3de03d42f6b12a28b` |

Committed (pre-draft) sha256, in table order:

```
40f6320c873b3e92e8deedd9db1f130245ab74000f33dbe22cca379a3f8da8fa  check-landed-contract.py
654a8c5e8f91c2e5eb6de0a5840be21d5de1d0dbdf92e52fa6c102d653174597  check-round-outcome-first.py
ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61  check-session-material.py
8fc895b3a01dff64b6da175d6f5aff736b800afbf683389eff6798f453656c33  check-wave-done.py
```

`diff -u` bodies (exactly these hunks, no others):

```diff
--- a/quality/check-landed-contract.py
+++ b/quality/check-landed-contract.py
@@ -17,6 +17,7 @@
 import argparse
+import os
 import re
@@ -52,7 +53,8 @@
     r = subprocess.run(["git", "-C", a.repo, "show", "%s:%s" % (a.frozen_rev, a.frozen)], capture_output=True,
-                       text=True, errors="replace")
+                       text=True, errors="replace",
+                       env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))
--- a/quality/check-round-outcome-first.py
+++ b/quality/check-round-outcome-first.py
@@ -71,6 +71,7 @@
         capture_output=True, text=True,
+        env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),
     )
@@ -123,7 +124,8 @@
     p = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, path)],
-                       capture_output=True, text=True)
+                       capture_output=True, text=True,
+                       env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))
--- a/quality/check-session-material.py
+++ b/quality/check-session-material.py
@@ -924,6 +924,7 @@
         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
+        env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),
     )
@@ -980,6 +981,7 @@
                 stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
+                env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),
             )
--- a/quality/check-wave-done.py
+++ b/quality/check-wave-done.py
@@ -184,6 +184,7 @@
     env["GIT_CONFIG_SYSTEM"] = os.devnull
+    env["GIT_NO_REPLACE_OBJECTS"] = "1"
     env["GIT_OPTIONAL_LOCKS"] = "0"
```

`import os` in `check-landed-contract.py` is the only non-`env` added line: the file had no `os`
import and the guard needs it.

## Choices inside the seat (named, not widened)

1. **`check-session-material.py` "~631" is not a git read.** Line 631 is `host_serials()`'s
   `subprocess.run(list(cmd))` — the sole non-git spawn (`hyprctl monitors all -j`, documented at
   :182). Guarding it would change the environment of a compositor query, outside the claim, so it
   is left byte-identical. The gate's actual object reads are `_git` (:924, used by `show` at :811
   and :905, `rev-parse` :936, `ls-tree` :941) and the `cat-file --batch` `Popen` (:980); both are
   repaired, which also covers those callers.
2. **Selftest fixture builders left unguarded** as permitted: `check-round-outcome-first.py`
   :211-223 (`init`, `rev-parse --show-toplevel`, `add`, `commit`, `rev-parse HEAD`) and
   `check-session-material.py` :1521-1529 / :1773-1776. They are writes or post-write reads of the
   throwaway repo they just created, so there is no replace ref to ignore.
3. **`check-wave-done.py`'s single `git_env()` store also covers its fixture env** (`Fixture.env =
   git_env(home)`, :583). Consequence is nil on a fixture with no replace refs; the selftest count
   stays 62/62.

## Proof (a) — census in a scratch repo, drafts applied

```
S=/fast/scratch/hyaku/mado-r68/R68ExecGate3
D=$(mktemp -d "$S/fixture.XXXX")                  # /fast/scratch/hyaku/mado-r68/R68ExecGate3/fixture.orsu
mkdir -p "$D/quality"; cp quality/check-*.py "$D/quality/"   # 20 files, worktree == HEAD verified
cp draft/quality/check-{landed-contract,round-outcome-first,session-material,wave-done}.py "$D/quality/"
git -C "$D" init -q && git -C "$D" rev-parse --show-toplevel   # == $D, asserted before first commit
git -C "$D" add -A && git -C "$D" -c user.name=r68 -c user.email=r68@example.invalid commit -q -m "r68 gate3 drafts"
# fixture head c207b866415ff97ee4b28d3be0a5660c038ac467
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r68-reader-guard.py \
  --repo "$D" --rev HEAD \
  --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-68/controls/c2-controls.json
```

My four lines:

```
MADO_R68_READER file=quality/check-landed-contract.py reader=yes guard=yes
MADO_R68_READER file=quality/check-round-outcome-first.py reader=yes guard=yes
MADO_R68_READER file=quality/check-session-material.py reader=yes guard=yes
MADO_R68_READER file=quality/check-wave-done.py reader=yes guard=yes
```

Final contract line, rc 1 (`TARGET_MISSED` is expected at seat scope — 8 unguarded files belong to
sibling seats; 5 = my 4 + `check-tool-ledger.py`):

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=5 unguarded=8 controls=11/11 verdict=TARGET_MISSED rev=c207b866415ff97ee4b28d3be0a5660c038ac467
```

Control fixture (same 20 committed files, **no drafts**; `dcc0414d256fc9ad3002f8ec07176da0a58a635b`),
rc 1 — reproduces the frozen baseline line exactly, so the 1→5 delta is my four files alone:

```
MADO_R68_READER file=quality/check-landed-contract.py reader=yes guard=no
MADO_R68_READER file=quality/check-round-outcome-first.py reader=yes guard=no
MADO_R68_READER file=quality/check-session-material.py reader=yes guard=no
MADO_R68_READER file=quality/check-tool-ledger.py reader=yes guard=yes
MADO_R68_READER file=quality/check-wave-done.py reader=yes guard=no
MADO_R68_READER_GUARD: population=20 readers=13 guarded=1 unguarded=12 controls=11/11 verdict=TARGET_MISSED rev=dcc0414d256fc9ad3002f8ec07176da0a58a635b
```

Direct `c2-r68-reader-guard.classify()` on the four drafts: `(True, True)` each (reader, guard).

## Proof (b) — selftest / compile / live read-only run

| file | mode | rc | output |
|---|---|---|---|
| `check-landed-contract.py` | no `--selftest`; `py_compile` (cfile in scratch) | 0 | n/a |
| `check-landed-contract.py` | live: `--repo <lane> --frozen-rev HEAD --frozen .ufo/waves/round-48/l1-draft/mado-terminal.py --landed <same>` | 0 | `CHECK96: frozen=9 landed=9 added=0 removed=0 unregistered=0 verdict=OK` |
| `check-round-outcome-first.py` | `--selftest` (TMPDIR in scratch) | 0 | `SELFTEST: ok cases=5` |
| `check-round-outcome-first.py` | live: `--repo <lane> --rev HEAD --round 67` | 1 (pre-existing) | `OUTCOME_FIRST_SUMMARY: rounds=1 pass=0 fail=1 skip=0` |
| `check-session-material.py` | `--selftest` (TMPDIR in scratch) | 0 | `SELFTEST: passed=94/94 failed=0` |
| `check-session-material.py` | live: `--repo <lane> --rev HEAD` | 1 (pre-existing findings) | `SESSION_MATERIAL: files=33545 findings=280 rev=40d2bef8964a098ae50f01094fa19e4725952010` |
| `check-wave-done.py` | `--selftest --work <scratch>` | 0 | `MADO_WAVE_DONE_SELFTEST: 62/62 passed` |
| `check-wave-done.py` | live: `--repo <lane> --rev HEAD --round 67` | 0 | `MADO_WAVE_DONE: round=67 waves=1 settled=1 verdict=OK` |

Every live invocation was run twice — committed file and draft, identical argv — and compared:
`rc_committed == rc_draft` and stdout/stderr sha256 equal for all four. No output difference.

## Risks / limits

- The census classifies committed source text, not runtime behaviour: the guard is presence-tested.
  A branch that never runs would still read as guarded; a helper fed its env from elsewhere is read
  by construction, not by dataflow.
- The replace-ref hazard probe (planted `refs/replace`, base reads forged bytes vs repaired reads
  real bytes) is the measurement seat's item, not this seat's; not run here.
- `check-session-material.py`'s non-git `hyprctl` spawn remains unguarded by design (choice 1).
  No compositor/surface was probed by this seat.
- Values are byte-identical to the committed files except the listed hunks; `check-wave-done`'s
  fixture env now also carries the key (nil effect, 62/62).

## Environment

No tool installed, no package manager transaction, no `pacman`. Scratch
`/fast/scratch/hyaku/mado-r68/R68ExecGate3/` and both fixture repos removed before yield.
No lane file, sibling lane, fleet file, `MANIFEST.json`, `.ufo/state` or config was written; no git
mutation ran in the lane or fleet (fixtures only, toplevel asserted).
