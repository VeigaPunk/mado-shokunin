# R55W2RevC1Code — correctness review of the C1 counter and harness

Scope: `quality/counters/c1-r55-kbd-entry.py` and `quality/r55_ctl_c1.py` at lane revision
57584ed67716340b3d466fa04333ac0bab3fb79e (tracked files identical to lane HEAD 721ba9c for these paths).
Not style. Every row below names the exact input, the command, and the observed output. All
mutations were applied to scratch copies of the lane (`/fast/scratch/hyaku/mado-r55/R55W2RevC1Code/`);
the lane was never written. Fixtures were built in scratch git repos (toplevel asserted before commit,
`-c user.name=ctl -c user.email=ctl@ctl`). The scratch tree is removed before yield; receipts are in
`receipts/` and the fix diffs in `fixes/`.

Common command prefix (lane path `L`, scored rev `R=57584ed6…`):
`python3 -I $L/quality/counters/c1-r55-kbd-entry.py --repo <repo> --rev <rev> --work <scratch>`
and `python3 -I $L/quality/r55_ctl_c1.py --repo <repo> --rev <rev> --work <scratch>`.

## Defect table

Severity: High = a wrong green/red verdict on a frozen leg; Medium = wrong verdict or a violated
rc/stdout contract needing a specific but non-exotic input; Low = contract/doc/robustness.

| ID | Sev | Target | Input (exact) | Observed output (rc) | Expected | Fix verified on a copy |
|---|---|---|---|---|---|---|
| D1 | High | counter (+ harness inherits) | `--repo F/fake --rev <F-commit>`, where F is a git repo whose root tree has **no** `corpus/` but whose `fake/` subtree is a full `git archive 57584ed` copy (F-commit 042cc1d0…). Same result via a symlink to `F/fake`. | `MADO_KBD_ENTRY: rev=042cc1d0… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` (rc 0). Harness: `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` (rc 0). | rc 2 setup error (`--repo` is not a repository top level), no verdict line. | `fixes/D1-D2-D3.diff`: `--show-prefix` must be empty → `c1-r55-kbd-entry.py: setup error: repo is not a repository top level` rc 2 |
| D2 | Medium | counter + harness (git env scrub) | Clean scored tree at 57584ed; in a scratch clone `git replace <oid of entry blob> <oid of a blob with K04 spliced>` (refs/replace/* present). Tree at rev is unmodified; `git ls-tree` still shows the original oid. | counter: `…rows=17/18 … verdict=TARGET_MISSED missed=quote:K04` (rc 1). Harness: `good: bad - verdict=TARGET_MISSED missed=quote:K04`, `controls=1/7 verdict=FAIL` (rc 1). | TARGET_MET (rc 0): the bytes must be the objects of `--rev`, not the replacement. | `GIT_NO_REPLACE_OBJECTS=1` in `git_env` → `TARGET_MET` rc 0 |
| D3 | High | counter (+ harness inherits) | Fence closer with an info string. Fixture commit 7d89bfbe…: the K12 row is removed from its place and appended at the end as `\`\`\`text` / `\`\`\`python` / `<K12 row>` / `\`\`\``. Per CommonMark §4.5 `\`\`\`python` is content (a closing fence "may be followed only by spaces or tabs"), so K12 is inside a code block. `cmark 0.31.2` renders K12 inside `<pre><code>` (checked: `K12 in <pre><code>: True`). | counter: `rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` (rc 0). Harness: `good=ok`, `controls=7/7 verdict=OK` (rc 0). | `verdict=TARGET_MISSED missed=row:K12` (rc 1): a table row inside a fenced block is not "outside fenced code blocks". | `FENCE` closer must be same char, length ≥ opener, nothing but whitespace after → `rows=17/18 … TARGET_MISSED missed=row:K12` rc 1 |
| D4 | Medium | counter `count_new_rows` | Registry fixture b552e1b3…: SOURCES rows S378, S379, S380 (opened 2026-10-28, tier A, mined) have used-by changed from `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` to `…r55.md.orig`. No other row names the entry with opened 2026-10-28. | `… new_rows=3/3 verdict=TARGET_MET missed=none` (rc 0) | `new_rows=0/3 … TARGET_MISSED missed=new_rows` (rc 1): used-by does not name the entry path. The check is `c["entry"] not in cells[10]` (substring). | token equality on the comma-split used-by → `new_rows=0/3 verdict=TARGET_MISSED missed=new_rows` rc 1 |
| D5 | Medium | counter `json.loads` + harness `_body` | `frozen-tables-v2.json` = 200 000 nested `[` then `]` (fixture commit 08f038ca…). | counter: stdout empty, rc 1, `RecursionError: Stack overflow … while decoding a JSON array`. Harness: stdout empty, rc 1, same RecursionError. | rc 2 setup error (stdout empty) or a `TARGET_MISSED … tables_sha` line; never a traceback with rc 1. rc 1 is the verdict-miss code. | `except (ValueError, RecursionError)` → `MADO_KBD_ENTRY: … TARGET_MISSED missed=entry_absent,index,tables_sha` rc 1 (single line, no traceback) |
| D6 | Medium | counter `Repo.git` | `frozen-tables-v2.json` with an extra key `"x\u0000"` in `c1.pin_sha256` (valid shape; `\0` not rejected by `valid_shape`), fixture commit 720dac6b…. | counter: stdout empty, rc 1, `ValueError: embedded null byte` (uncaught; `Repo.git` catches only OSError/SubprocessError). Harness: `good=bad … controls=0/7 verdict=FAIL` rc 1 (handled, via the counter's empty stdout). | rc 2 setup error, stdout empty. | `except (OSError, ValueError, subprocess.SubprocessError)` → `c1-r55-kbd-entry.py: setup error: git failed to run: ValueError` rc 2 |
| D7 | Medium | harness `read_tree` | Non-UTF-8 file `\xff.txt` added inside the pin dir `.ufo/waves/round-55/fetch/` (fixture commit 5653c82b…). | counter: `… verdict=TARGET_MET` rc 0. Harness: stdout empty, rc 1, `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff`. | harness must not crash: either proceed (the counter is green on this tree) or rc 2 setup error. | not fixed on copy; cause is `name.decode("utf-8")` in `read_tree` (use `surrogateescape` as the counter does) |
| D8 | Low | harness `_run` | `--work /proc/nope/x` (unwritable) or `--work <an existing file>`. | Python traceback (FileNotFoundError / FileExistsError from `work0.mkdir`), rc 1, stdout empty. The counter returns rc 2 for the same two inputs (`setup error: FileNotFoundError` / `FileExistsError`). | rc 2 with `MADO_R55_CONTROLS setup error: …` on stderr. | not fixed on copy; wrap `work0.mkdir` in the `Setup` handler |
| D9 | Low | counter `Repo.git` (object-store writes during scoring) | `--repo` = a `git clone --filter=blob:none` partial clone of the scratch clone (missing blobs 20174). | counter: `… TARGET_MET` rc 0; `git rev-list --missing=print` afterwards: missing 20160 — 14 blobs were fetched from the promisor remote into the scored repo. | no writes or network to the scored repo; rc 2 when a needed object is missing. | `GIT_NO_LAZY_FETCH=1` in `git_env` (in `c1-fix.py`): missing stays 20174, output `c1-r55-kbd-entry.py: setup error: git cat-file failed`, rc 2 |
| D10 | Low | counter `--selftest` (docstring contract) | `--selftest` at 57584ed. | 52 stdout lines (`PASS`/`FAIL` rows + summary), rc 0. The docstring states the counter "prints exactly one line (stdout)". | either doc or selftest output to stderr. | not fixed (doc/contract text) |
| D11 | Low | counter `selftest` (code reading only) | An exception inside a `case()` mutator (AssertionError from `edit`, KeyError from `row_of`) escapes `selftest`; `shutil.rmtree(base)` is only on the success path. | NOT triggered: the selftest passes 50/50 at the scored rev, so the mutators never raised. | cleanup in `finally`; a raise is a setup error. | UNVERIFIED-triggered; code reading of `selftest()` only |

Harness rc/stdout contract (`r55_ctl_c1.py`): D5 (harness RecursionError), D7, D8 break "rc 2 on setup error, stdout empty".

## Targets checked and verdicts

Counter `--rev` forms (scored lane, `--repo /home/vgpnk/Projects/shokunin/mado-shokunin`):

| Form | Input | Output (rc) | Verdict |
|---|---|---|---|
| full hash | `57584ed67716340b3d466fa04333ac0bab3fb79e` | `rev=57584ed6… rows=18/18 … TARGET_MET missed=none` (0) | SURVIVES |
| abbreviated | `57584ed67716` | `rev=57584ed67716 … TARGET_MET` (0) | SURVIVES |
| HEAD | `HEAD` | `rev=HEAD … TARGET_MET` (0) | SURVIVES |
| branch (clone) | `r55-branch` | `rev=r55-branch … TARGET_MET` (0) | SURVIVES |
| annotated tag (clone) | `r55-tag` | `rev=r55-tag … TARGET_MET` (0) | SURVIVES |
| lightweight tag (clone) | `r55-lightweight` | `rev=r55-lightweight … TARGET_MET` (0) | SURVIVES |
| `<hash>^{commit}` | `57584ed6…^{commit}` | `rev=57584ed6…^{commit} … TARGET_MET` (0) | SURVIVES |
| tree oid / blob oid / unknown 40-hex | `$R:quality`, blob `quality/r55_ctl_c1.py`, `0123…4567` | `c1-r55-kbd-entry.py: setup error: rev does not resolve to a commit at repo` (2), stdout empty | SURVIVES |
| annotated tag to tree | `r55-tree-tag` | same setup error (2) | SURVIVES |
| `$R:.ufo` (tree-ish path) | `57584ed6…:.ufo` | setup error (2) | SURVIVES |
| empty / option-like | `""`, `-x` | `bad rev` (2); argparse `expected one argument` (2) | SURVIVES |
| unborn HEAD | `git init` + `--rev HEAD` | setup error (2) | SURVIVES |
| ambiguous `--rev` leading `--show-toplevel` (harness) | `--rev=--show-toplevel` | `setup error: git … rev-parse --verify failed` (2) | SURVIVES |

Path handling:

| Target | Input | Output (rc) | Verdict |
|---|---|---|---|
| repo through symlink | `--repo <symlink to clone>` | TARGET_MET (0) | SURVIVES |
| trailing slash / relative `--repo .` and relative `--work` | `--repo "$L/"`; `cd clone && --repo . --work ../w/rel` | TARGET_MET (0); the relative work dir stayed empty | SURVIVES |
| non-directory / empty repo arg | `--repo ""`, `--repo <file>`, nonexistent | `repo is not a directory` (2) | SURVIVES |
| non-repo subdirectory of a repo | `--repo $L/quality` | `TARGET_MISSED missed=entry_absent,index,tables_sha` (1): cwd-relative paths, wrong location | BROKEN → D1 (the same mechanism turns a subdir holding a full corpus into TARGET_MET) |
| symlink to subdirectory of a repo | `--repo <link>/fake` | TARGET_MET (0); harness good=ok 7/7 | BROKEN → D1 |

Git environment and objects:

| Target | Input | Output (rc) | Verdict |
|---|---|---|---|
| `GIT_DIR` / bogus `GIT_DIR` injected in the environment | `GIT_DIR=$D/c/.git python3 -I … --repo $L` and `GIT_DIR=$bogus/.git` | TARGET_MET (0) both: env is replaced by `git_env`, so the outer GIT_* is ignored | SURVIVES |
| replace refs | D2 | D2 | BROKEN |
| lazy fetch | D9 | D9 | BROKEN |
| dirty working tree ignored | selftest `dirty-working-tree-ignored` | PASS | SURVIVES |

`--work` and temporary files:

| Target | Input | Output (rc) | Verdict |
|---|---|---|---|
| counter honours `--work`, nothing under `/tmp` | `find /tmp -newer <marker>` after all counter runs and selftest | empty | SURVIVES |
| counter leaves nothing in `--work` after success | `ls -A w-main` after runs | empty | SURVIVES |
| counter `--work` is a file / unwritable | `--work $C` (a file); `--work /proc/nope/x` | `setup error: FileExistsError` (2); `setup error: FileNotFoundError` (2) | SURVIVES |
| harness `--work` is a file / unwritable | same two inputs | traceback, rc 1, stdout empty | BROKEN → D8 |
| harness leaves nothing after success | `--work $S/w-v/hx` | empty dir | SURVIVES |

Contract and robustness: D5 (counter and harness), D6 (counter), D7, D8 (harness).

Grammar and freeze targets (the fixture recipes are in the report):

| Target | Input | Output (rc) | Verdict |
|---|---|---|---|
| fenced code: K12 moved into an info-string fence | D3 | TARGET_MET (0) | BROKEN |
| HTML comment on one line: `<!-- note --> <!--` before K12, `-->` after | fixture 466beba7… | counter TARGET_MET (0). `cmark` renders K12 as a paragraph `<p>| K12 |…` (visible). Per CommonMark §4.6 HTML block type 2 the block ends on the line containing `-->` (spec.txt "End condition: line contains the string `-->`"), so the first line closes its own block and K12 is outside it. | counter agrees with CommonMark | NOT-REPRODUCED (not a violation at block level; the inline case inside a paragraph was not separately built) |
| used-by substring | D4 | TARGET_MET (0) | BROKEN |
| registry-valid grammar, pin hash, source cell, anchor, quote | selftest 50 cases incl. CTL1–CTL7 | `MADO_KBD_ENTRY_SELFTEST: 50/50 passed` (0) | SURVIVES as a self-check; does not cover D1–D10 |

Harness (`r55_ctl_c1.py`) at 57584ed: `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` (rc 0).
The harness has no independent check of its own: `good` is the counter's green line, so D1 and D3
pass it (receipts/harness.out shows the scored-rev run only).

## Fixes verified on copies (not applied to the lane)

- `fixes/D1-D2-D3.diff` (`c1-fix-D1-D2-D3.py`): D1 → rc 2; D2 → TARGET_MET rc 0; D3 → `rows=17/18 … TARGET_MISSED missed=row:K12` rc 1; lane at 57584ed still TARGET_MET rc 0; selftest 50/50 passed.
- `fixes/D4-D5-D6.diff` (`c1-fix-D4-D5-D6.py`): D4 → `new_rows=0/3 … TARGET_MISSED missed=new_rows` rc 1; D5 → single `TARGET_MISSED … tables_sha`-class line rc 1, no traceback; D6 → rc 2; lane at 57584ed still TARGET_MET rc 0; selftest 50/50 passed.
- D9 (`GIT_NO_LAZY_FETCH=1`) is in `c1-fix-D1-D2-D3.py`: on a fresh partial clone → rc 2, missing count unchanged.

## Notes on input validity (QUALITY 105)

- D1, D2, D3, D4, D9 are inputs that satisfy the frozen grammar (exact rows, exact anchors, exact quotes; D1 a
  registry-valid tree; D4 a registry-valid used-by string). They are verdict falsifications, not syntactic rejections.
  The instrument was unchanged for each (the counter file at the scored rev).
- D5, D6, D7, D8 are crashes (unhandled exceptions), not verdict falsifications. They are reported as contract
  violations; the parser-compatible control is the same counter on a valid tree (`TARGET_MET`, rc 0).
- The harness counts a mutant as "caught" only on the counter's exact line; the 7 controls pass on the scored rev,
  and the D1/D3 trees also pass it. The harness cannot detect the counter's own false greens.
