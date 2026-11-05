# R86 sentinel — boundary and safety review of the two round-86 instruments

Seat: **R86Sentinel** (leaf, no dispatch). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round-86 declaration read first: `.ufo/waves/round-86/claims-declaration-r86.md`.
Instruments reviewed: `quality/counters/c1-r86-refusal-records.py` (674 lines) and
`quality/counters/c2-r86-clause-observations.py` (962 lines); control sets
`.ufo/waves/round-86/controls/c1-cases-r86.json` (sha256 `f6dd9cde…`) and
`c2-cases-r86.json` (sha256 `a87f0ea4…`); every receipt under `.ufo/waves/round-86/receipts/`.

Declared freeze revision: `237ecf4e69a4986108f719f3beeafe111adaa033`. Working tree at review time:
`b33afc08…` (lane `master`), dirty (see F4/F5).

Nothing was edited except this file. No mutating git/jj command was run. Scratch was
`/fast/scratch/hyaku/mado-r86/R86Sentinel/` and was removed (`trap 'rm -rf -- "$S/run"' EXIT`);
no `/tmp` file was used. No tool was installed.

All commands below assume:

```sh
S=/fast/scratch/hyaku/mado-r86/R86Sentinel
cd /home/vgpnk/Projects/shokunin/mado-shokunin
export TMPDIR=$S
```

## Verdict in one paragraph

Both counters are **read-only in what they execute**: every argv in the frozen C2 control set is a
read verb (`hyprctl` getters, `pgrep`, `busctl list/introspect/get-property`, `systemctl is-active`,
`makoctl mode`, `omarchy version|theme current|menu keybindings --print`, `jq`/`awk`/`cut`/`head`/
`cat`/`sort`, `sh` over committed fixtures, `python3 -I tools/mado-barfoot.py` over committed
fixtures); no redirect, no `$(…)`/backtick, no network client. C1 executes only `git show`/`git
rev-parse`, `python3 -I` on extracted copies, and writes exclusively under its mktemp workroot.
Setup errors (rc 2) never print a verdict token. **But four boundary defects matter for a gate:**
C2's own counter bytes are not bound to `--rev`, so `rev=` + `tree=bound` overclaims provenance (F2);
C2 hands its `git` child the *whole* caller environment and resolves `git` through `PATH`, which makes
the tree-binding redirectable and exposes ambient credentials (F1); `--no-mutants` returns **rc 0**
while the kill clause is unexercised, contradicting both documents' exit maps (F3); and the frozen C1
counter was edited **after** the freeze (F4).

## Findings

| # | Sev | File:line | Finding |
|---|---|---|---|
| F1 | **High** | `c2-r86-clause-observations.py:272-283` | `git` child inherits the whole environment and is resolved via `PATH`; ambient `GIT_DIR` overrides `-C repo`, so `tree=bound` (lines 828-848) can bind a different repository |
| F2 | Medium | `c2-r86-clause-observations.py:829-831`, `:942-951` | the counter's own bytes are not bound to `--rev`; receipt says `rev=f72bba01` while the executed bytes are the repaired/frozen `c8331700` |
| F3 | Medium | `c1:644-651`, `c2:941,951-952` | `--no-mutants` exits 0 with `killed=0`; in C1 the branch returns 0 without evaluating `target` at all |
| F4 | Medium | `quality/counters/c1-r86-refusal-records.py:16` | frozen instrument edited after the freeze (docstring `mutants=53`→`51`, mtime 00:15:58, after the freeze commit at 00:00:51 and after every receipt); the disclosure (`instrument-repair-r86.md` "Repair 4") is itself uncommitted |
| F5 | Medium | `receipts/c1-r86.txt:129` | the only green C1 receipt is stamped `rev=f72bba01…`, not the declaration's `rev=<freeze>`; no receipt records the exit status of either target run |
| F6 | Low | `c2:829-833` | at the freeze rev the C2 target command no longer runs (`SKILL.md` moved at `b33afc08`); it fails **closed** with rc 2, so nothing is misgraded, but the declared target is not reproducible from the current tree |
| F7 | Low | `c1:548-554`, `c2:793-799` | scratch-root symlink refusal covers only the final path component (an intermediate symlink is accepted); TOCTOU between `islink` and `makedirs` |
| F8 | Low | `c1:554`, `c2:799` | mktemp prefixes `c1-r82-`/`c2-r82-` in round-86 instruments (cosmetic, harmless) |
| F9 | Low | `c2:236-244` | when `HYPRLAND_INSTANCE_SIGNATURE` is absent the counter *guesses* an instance (first sorted `/run/user/<uid>/hypr/*` with a socket), so the measured surface can differ from the caller's |
| F10 | Low | `receipts/census-start-r86.txt:57`, `census-end-r86.txt:57` | the only absolute home path in any receipt is the lane path `…/mado-shokunin/corpus/SOURCES.md` |
| F11 | Low | `c1:610-612`, `c2:924-930` | mutant accounting cannot distinguish "measured a miss" from "never ran": a crashed mutant prints the same `matched=0/37 killed=yes` as a behavioural 0/37 |

Clean results that the claim depends on are recorded in §1–§4 below (argv inventory, scratch and
child-env discipline for the data rows, receipt leak scan, and the observed rc↔verdict map including
an independent full C2 mutant sweep).

---

## 1. Every argv the two counters execute

### C1 — constructed by the counter, all from `--rev`/`--base-rev`

`c1:238` runs exactly these shapes (nothing else is spawned anywhere in the file):

| argv | where | verdict |
|---|---|---|
| `git -C <repo> rev-parse <rev>` | `resolve()`, `c1:517-525` | read |
| `git -C <repo> show <rev>:tools/mado-barfoot.py` | `extract()`, `c1:510-515` | read |
| `python3 -I <workroot>/mado-barfoot.py --selftest` | `c1:585` | the tool's own in-memory selftest; its one write is inside `tempfile.TemporaryDirectory()` (`tools/mado-barfoot.py:1388`) |
| `python3 -I <tool> --config … --layers … --monitors … [--rules …] [--surfaces …] [--allocation …] [--monitor …]` | `run_cases()`, `c1:388-397` | read; the tool's parser (`tools/mado-barfoot.py:1674-1682`) has no write flag |

Every case artifact is written by the counter into `<workroot>/<label>-NN/` before the run
(`case_files()`, `c1:288`), i.e. inside `/fast/scratch/…`, never in the tree.

### C2 — the frozen control set

```sh
jq -r '[.cases[]|.argv[0]]|group_by(.)|map({verb:.[0],n:length})' \
  .ufo/waves/round-86/controls/c2-cases-r86.json
# [{"verb":"/bin/sh","n":31},{"verb":"busctl","n":2},{"verb":"python3","n":4}]
```

Pipeline-stage verbs across all 37 rows:

```sh
jq -r '.cases[]|.argv|if .[0]=="/bin/sh" then .[2] else join(" ") end' \
  .ufo/waves/round-86/controls/c2-cases-r86.json | sed 's/; */\n/g; s/ | /\n/g' | awk '{print $1}' | sort | uniq -c
#   2 awk   5 busctl   3 cat   2 cut   5 head  14 hyprctl   8 jq   1 makoctl
#   5 omarchy  2 pgrep  4 python3   5 sh   1 systemctl  (+ 20× `set` opening the guarded rows)
```

`hyprctl` subcommands, exhaustively: `activeworkspace`, `binds`, `clients`, `configerrors`,
`getoption`(×3), `layers`(×2), `monitors`(×3), `version`, `workspaces` — all getters. No `dispatch`,
`keyword`, `reload`, `kill`, `output`, or `setcursor` anywhere in the set:

```sh
grep -nE 'dispatch|keyword |reload|kill|pkill|mv |rm |cp |curl|wget|http|git (add|commit|push)' \
  .ufo/waves/round-86/controls/c2-cases-r86.json | grep -v '"skill_anchor"' || echo NONE
# NONE        (the only hits are the frozen skill_anchor strings quoted back at me)
```

- `busctl`: `--user list`, `--user introspect …`(×2), `--user get-property …`(×2) — D-Bus reads on
  the session bus; not network.
- `python3 -I tools/mado-barfoot.py --config/--layers/--monitors …` (4 rows) — the read-only scorer
  over committed fixtures; the argv is byte-equal to the SKILL.md row it is bound to (enforced at
  `c2:866-871`).
- `sh <committed fixture>.sh` (5 rows) — `pipefail-guard.sh`, `failing-producer.sh`,
  `status-ok.sh`, `status-exit7.sh`, `status-sigpipe.sh`: each prints to stdout, redirects only to
  `/dev/null`, and writes no file.
- `omarchy menu keybindings --print` — verified read-only in the implementation:
  `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu-keybindings:243-251` dispatches `--print` to
  `output_keybindings` only; `walker` is reached solely in the interactive `else` branch.
- No command substitution and no shell variable expansion in any argv:
  `jq -r '.cases[]|.argv|join(" ")' … | grep -nE '\$\(|`|\$\{|\$[A-Za-z_]'` → `NONE`.
- Fixture references in argv equal the declared `fixtures` lists (the only extra reference is
  `tools/mado-barfoot.py`, bound separately at `c2:829`), and all 17 fixture files exist.

**No mutating command, no network call, and no write outside the scratch root** was found in either
counter's executed surface. The one class of write that does occur is the counters' own
workroot (mktemp) plus files the counters generate there.

## 2. Scratch handling and the child environment

| Check | C1 | C2 |
|---|---|---|
| `--scratch-root /` refused | `c1:548` — observed rc 2, `ERROR (stage=setup refusing / as the scratch root)` | `c2:793` — same, rc 2 |
| final-component symlink refused | `c1:549` | `c2:794` — observed rc 2, `refusing a symlinked scratch root` |
| intermediate-component symlink | not checked | not checked — **accepted** (F7): `--scratch-root $S/link/sub` with `$S/link → $S/real` returned rc 0 and created `$S/real/sub` |
| mktemp inside the root | `c1:554` `mkdtemp(prefix="c1-r82-", dir=args.scratch_root)` | `c2:799` `mkdtemp(prefix="c2-r82-", dir=args.scratch_root)` |
| cleanup | `c1:668-670` `shutil.rmtree(workroot, ignore_errors=True)` in `finally` | `c2:956-958`, same |
| hardcoded `/tmp` | none (the only `/tmp` occurrence in either file is a comment, `c2:222`) | none |
| `TMPDIR` for children | `c1:235` `"TMPDIR": cwd` | `c2:231` `env["TMPDIR"] = SCRATCH_ROOT or cwd`; `SCRATCH_ROOT` is set to the mktemp workroot at `c2:800-801`, so every row and every mutant lands in scratch |

Two `TMPDIR` details worth recording (neither is a live defect):

- `c1`'s `resolve()`/`extract()` pass `cwd=repo` (`c1:510-525`), so those `git` children get
  `TMPDIR=<measured tree>`. Both are read verbs (`rev-parse`, `show`), so nothing is written there,
  but the comment at `c1:233-234` ("keep its throwaway dir inside caller scratch") does not describe
  the git path.
- `c2`'s comment at `c2:230` says `TMPDIR` is "the caller's scratch root"; it is the mktemp
  **workroot inside** it. Stricter than the comment, so harmless.

### Which variables reach a child

C2's data rows (probed by loading the frozen module and calling its own `run()` with `env`):

```
DBUS_SESSION_BUS_ADDRESS, HOME, HYPRLAND_INSTANCE_SIGNATURE, LANG, LC_ALL, LOGNAME, OMARCHY_PATH,
PATH, PYTHONDONTWRITEBYTECODE, TMPDIR, USER, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_DIRS,
XDG_DATA_HOME, XDG_RUNTIME_DIR   (+ PWD/SHLVL/_ from /bin/sh itself)
```

No token, no credential, no session file. `PATH` is the caller's `PATH` with `/usr/local/bin`,
`/usr/bin`, `/bin`, `~/.local/bin`, `~/.local/share/omarchy/bin` appended if absent (`c2:252-258`).

C1's children get five keys only — `PATH`, `LC_ALL`, `LANG`, `PYTHONDONTWRITEBYTECODE`, `TMPDIR`
(`c1:228-240`) — better isolation than C2 on this axis (no `HOME`, no D-Bus, no secrets).

### F1 — the exception: C2's `git` child (High)

`git_bytes`/`git_show` (`c2:272-283`) call `subprocess.run(["git", …])` **without `env=`**, so that
child inherits the entire caller environment, and `git` itself is resolved through `PATH`.

Evidence 1 — environment inheritance and PATH resolution (shim on `PATH`):

```sh
printf '#!/bin/sh\nenv | sort > '"$S"'/git-env.txt\nprintf "shim\\n"\n' > $S/bin/git; chmod +x $S/bin/git
python3 - <<'PY'   # loads the frozen c2 and calls its own git_bytes with $S/bin first on PATH
…  c2.git_bytes("<lane>", "HEAD", "SKILL.md")
PY
# the recorded env contains, among ~180 variables:
#   OPENAI_CODEX_TOKEN=eyJhbGciOiJSUzI1NiIs…
#   OP_SERVICE_ACCOUNT_TOKEN=ops_eyJzaWduSW5BZGRyZXNz…
#   XAI_OAUTH_TOKEN=eyJ0eXAiOiJhdCtqd3Qi…
#   SSH_AUTH_SOCK=/run/user/1000/ssh-agent.socket
```

Evidence 2 — the tree-binding is redirectable by an ambient `GIT_DIR` (no fixture commit needed;
an empty `git init -q` repo was used as the `-C` argument):

```
baseline bytes: 301876
SUBSTITUTED: -C repo ignored; read 301876 bytes of the lane's SKILL.md via ambient GIT_DIR
GIT_OBJECT_DIRECTORY broke the read: cannot read SKILL.md at HEAD: fatal: not a git repository …
```

So `git -C repo show rev:path` does not necessarily read `repo`: with `GIT_DIR` set in the caller's
environment, every binding at `c2:828-848` (`SKILL.md`, `tools/mado-barfoot.py`, and every declared
fixture) and every `git_show(repo, rev, "SKILL.md")` can be answered from another repository,
while the receipt still prints `tree=bound`. Impact: the provenance of the executed rows is only as
strong as the caller's environment; accidentally-set `GIT_DIR`/`GIT_OBJECT_DIRECTORY` (common when a
harness runs inside a hook) produces a *silent* misbinding, and ambient credentials are exposed to
whatever `git` the `PATH` resolves to. Smallest remediation: build the git child's env exactly like
`run()` does (drop every `GIT_*`), and resolve `git` by absolute path; optionally `--no-replace-objects`
and `GIT_CONFIG_NOSYSTEM=1`.

Same class, weaker: **C1** resolves `git` through the inherited `PATH` (`c1:230`). Demonstrated:

```
C1 extract returned 'POISONED-GIT-OUTPUT\n' -> tool_sha256=45a4d93123831da07810beee9022b5f67c697bb2d1bd2841302ba02adac1a6df
```

A `PATH`-resident `git` replaces the measured tool source and therefore `tool_sha256`. C1 does *not*
have the `GIT_DIR` hole (its env is fixed), so this is PATH-integrity only.

## 3. Receipts — leak scan

```sh
cd .ufo/waves/round-86/receipts
grep -niE 'serial|description|make=|model=|manufacturer' *.txt *.md      # NONE
grep -niE 'token|secret|password|api[_-]?key|bearer|ghp_|AKIA|PRIVATE' *.txt *.md   # NONE
grep -cE '^\{"|^\[|"levels"' *.txt                                     # 0 in every file
grep -nE 'desc:|1920x|2560x|DP-|HDMI-|eDP-' *.txt                      # NONE
grep -n '/home/\|/Users/\|\.local/share' *.txt *.md
# census-end-r86.txt:57:mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
# census-start-r86.txt:57: (same line)
```

- No monitor serial, model, description, resolution, or make appears in any receipt.
- No secret, token, or credential appears in any receipt.
- No raw JSON dump of a live surface appears in any receipt. This is by construction for C2:
  `observed()` (`c2:596-598`) reduces a row to `rc=<n> stdout-bytes=<n>`, and every
  `MADO_R86_PROBE` line carries only name/row/kind/match/clause counts. C1 prints case names and
  fixture-derived geometry only.
- The single absolute home path is the lane's own `corpus/SOURCES.md` in the census receipts (F10) —
  a workspace path, not operator data; still worth making lane-relative.
- Note (not a defect): live host values (versions, monitor names, keybinding rows) live in the
  **committed control set** (`c2-cases-r86.json` `frozen`/`samples` fields) by design; they are
  dense in that frozen input, not in the receipts.

## 4. Exit-map honesty (observed, not inferred)

| Run | Command shape | rc | Printed |
|---|---|---|---|
| C1 usage error | `c1-frozen.py --repo .` | **2** | `MADO_R86_REFUSALS: ERROR (stage=setup usage)` |
| C1 bad `--rev` | `--rev deadbeef…` | **2** | `ERROR (stage=setup cannot extract tools/mado-barfoot.py at deadbeef…` |
| C2 usage error | `c2-frozen.py --repo .` | **2** | `MADO_R86_RUNBOOK: ERROR (stage=setup usage)` |
| C2 bad `--rev` | `--rev deadbeef…` | **2** | `ERROR (stage=setup cannot read SKILL.md at deadbeef…` |
| C2 at the freeze rev | `--rev 237ecf4e …` | **2** | `ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)` |
| C1 `--no-mutants` at the freeze rev | full frozen argv | **0** | `cases=75 correct=75 mutants=0 killed=0 … verdict=MUTANTS_SKIPPED` |
| C2 `--no-mutants` at HEAD | `--rev b33afc08` | **0** | `matched=37 … mutants=0 killed=0 verdict=MUTANTS_SKIPPED tree=bound` |
| C2 full sweep at HEAD | `--rev b33afc08`, 37 mutants | **0** | `verdict=TARGET_MET`, 37× `killed=yes`, 0× `killed=no` |
| C2 with one non-carried case broken | `value:\"[0-9]+\"→\"^9$\"` on `border-size-int` | **1** | `matched=36 … verdict=TARGET_MISSED` |

Conclusions:

1. **Setup (rc 2) is never a verdict.** Verified four ways; each emits `ERROR (stage=setup …)` and
   no `verdict=` token. C2 additionally fails closed on a moved measured file.
2. **rc 0/1 ↔ TARGET_MET/TARGET_MISSED** holds for full runs: rc 0 was observed on an independent
   full C2 sweep (frozen bytes `1283df22…`, 37/37 kills, 42 s wall) and rc 1 was observed on a
   deliberately broken case. C1's rc-1 branch (`c1:664`) was **not** exercised — see "not run".
3. **F3:** `--no-mutants` violates the exit map in both files. `c1:644-651` prints and `return 0`
   *before* `target` is computed, so a `--no-mutants` run with a wrong `correct` count would still
   exit 0; `c2:941` makes `killed == MUTANTS` unconditional, so `killed=0` still yields 0. The
   declaration says rc 0 iff `killed == 51` / `killed == 37`, and both module docstrings say
   "rc 0 iff every executable clause holds". A gate keyed on exit status accepts a run that never
   exercised the kill clause and (C1) never evaluated the honest run either.
4. The receipts record no exit status for any target or control run: `grep -n '^rc=' receipts/*.txt`
   returns only `selftest-c1`, `selftest-c2`, `census-start`, `census-end`. The rc→verdict mapping
   is therefore not evidenced by the receipts themselves.

## F2/F4/F5 — provenance of the numbers

```sh
git ls-tree 237ecf4e -- quality/counters/c1-r86-refusal-records.py quality/counters/c2-r86-clause-observations.py SKILL.md
# c1 893d903d…   c2 c8331700…   SKILL.md e3eb4656…
git ls-tree f72bba01 -- <same>
# c1 893d903d…   c2 013c0c6f…   SKILL.md e3eb4656…
sha256sum quality/counters/c1-r86-refusal-records.py          # 4ff50ac2…  ← ≠ 893d903d (F4)
git diff 237ecf4e -- quality/counters/c1-r86-refusal-records.py
# -Contract: … mutants=53 killed=53 …      (one docstring line, only)
```

- C1's `TARGET_MET` receipt (`c1-r86.txt:129`) is stamped `rev=f72bba01…`. The C1 blob is identical
  at `f72bba01` and at the freeze, so the *measurement* is the frozen instrument's; the **rev label
  is not the freeze** the declaration names (`rev=<freeze>`), and no receipt re-runs it at
  `237ecf4e` (F5). The re-run at the freeze rev exists only as `control-c1-r86.txt` with
  `--no-mutants` (`verdict=MUTANTS_SKIPPED`).
- C2's `TARGET_MET` receipt (`c2-repaired-r86.txt`) is stamped `rev=f72bba01… tree=bound`, but the
  executed counter bytes are the repaired file that the freeze later committed as `c8331700`,
  whereas `f72bba01` carries `013c0c6f`. The `tree=bound` check covers only `SKILL.md`,
  `tools/mado-barfoot.py` and declared fixtures (`c2:829-848`) — never the counter itself. So the
  receipt's `rev=` does not describe the instrument that produced it (F2). The measured inputs
  (`SKILL.md` `e3eb4656`, `barfoot` `929f7b3f`, fixtures) are byte-identical at both revs, so the
  numbers are sound; the provenance sentence is not.
- F4: the frozen C1 counter is dirty in the worktree (`4ff50ac2`, docstring `mutants=51`), edited at
  00:15:58 — after the freeze commit (00:00:51) and after every receipt (latest 00:13:55). The
  disclosure that explains it, "Repair 4" in `instrument-repair-r86.md`, was written at 00:16:12 and
  is itself uncommitted (`13bddbd1` at the freeze and at HEAD, `9cc69a24` in the worktree). The
  written rule is "the instruments are FROZEN; you may read and run them; you may NOT edit them";
  a verifier who reads the worktree runs non-frozen bytes whose diff is exactly the population the
  kill rule names.

## F9/F11 — two smaller measurement-provenance weaknesses

- F9: `c2:236-244` — if `HYPRLAND_INSTANCE_SIGNATURE` is not in the caller env, the counter walks
  `/run/user/<uid>/hypr/` and takes the **first sorted** instance directory containing a socket.
  With two live compositor sessions the row set can be executed against a surface that is not the
  caller's. Failing closed (skip the hypr rows as setup) would be more honest than guessing.
- F11: `c1:610-612` (`dead = mcorrect < CASES`) and `c2:924-930` (`mmatched = 0` when the summary
  line is missing; `dead = mrc != 0 and (mm is None or mmatched < CASES)`) both count a **crashed**
  mutant as killed. For C2 the printed line is identical for a crash and a behavioural 0/37. This
  round it does not change anything — every mutant in the receipt and in my own sweep printed a
  summary line with a partial score — but the receipt cannot prove it. Recording `summary=yes|no`
  (or the mutant rc) would make the kill evidence self-describing.

## Independent checks I did run, with results

```sh
python3 -I $S/c1-frozen.py --repo . --rev 237ecf4e --base-rev 2b6dd76b… \
  --controls .ufo/waves/round-86/controls/c1-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c1-cases-r85.json --scratch-root $S/c1 --no-mutants
# MADO_R86_REFUSALS: cases=75 correct=75 mutants=0 killed=0 base_correct=75/75 carried=72/72
#   tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=MUTANTS_SKIPPED
#   rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce…      rc 0   (F3)

python3 -I $S/c2-frozen.py --repo . --rev b33afc08 \
  --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root $S/c2
# MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37
#   clauses_observed=37/37 … mutants=37 killed=37 verdict=TARGET_MET … tree=bound   rc 0
#   37 × MADO_R86_MUTANT … killed=yes, 0 × killed=no
```

The two lowest-scoring mutants were regenerated by hand from the frozen bytes to confirm the kills
are behavioural rather than crashes (they reproduce the receipt's numbers exactly and do print a
summary line):

```
negatives-skipped rc=1  MADO_R86_RUNBOOK: cases=37 executed=37 matched=0 shapes=0/27 … clauses_observed=0/37
samples-skipped   rc=1  MADO_R86_RUNBOOK: cases=37 executed=37 matched=5 shapes=0/27 … clauses_observed=5/37
```

This reproduces `c2-repaired-r86.txt`'s `matched=0/37` and `matched=5/37` and shows the four round-85
survivors die by measurement, not by import error.

## What I could not run, and why

- **C1's rc-1 path and the full 51-mutant sweep.** Another seat owns the C1 counter run, and C1 has
  no `--no-mutants`-free way for me to reach `rc 1` without changing a *carried* case: the guarded
  branch compares `cases[:72] == carried` (`c1:577-581`) and raises Setup on any edit, while the
  three non-carried cases (72-74) are all `error`-typed, so a field mismatch in them is ignored by
  `expected_ok`'s early return. My probe (`expect.band = 999999` on case 74) accordingly still
  scored 75/75. The rc-1 mapping is therefore reported **from code** (`c1:664`) and *not* observed.
- **C2 at the freeze rev with mutants.** It refuses to start (F6): the worktree `SKILL.md` at HEAD is
  `48419a14` while `237ecf4e` carries `e3eb4656`. The full sweep was run at `b33afc08`, whose C2 blob
  is the freeze's `c8331700`.
- No fixture git repository was created and no commit was made anywhere; the `GIT_DIR` substitution
  proof needed no fixture history (an empty `git init -q` repo served as the `-C` argument).

## Residual risk I could not remove

If the caller's environment carries `GIT_DIR`, `GIT_OBJECT_DIRECTORY` or a poisoned `PATH`, `tree=bound`
and `tool_sha256` can be satisfied against bytes the lane never committed (F1). Until that is fixed,
`tree=bound` should be read as "the `git` this process resolved agreed with the worktree", not as
"the committed bytes".
