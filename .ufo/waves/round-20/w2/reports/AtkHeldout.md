# AtkHeldout — partly falsified: every held-out want is semantically right, but the 12 are excluded from the score by a wave-1 EDGE hint, not by the registered contract, and all 12 fail the repaired tool (full-suite precision 172/187 = 9.1979, not 172/175 = 9.8286)

Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`, tip `a4046a8216080d4004de3f268c62cf142095ac07`.
Work done in `/tmp/mado-r20w2-AtkHeldout` (clone of the lane, HEAD observed `a4046a8…`, `origin` removed).
Suite under test: `.ufo/waves/round-20/precision-heldout/` (12 cases), `expected.json`
sha256 `78b168b0db86502df23b6204a5a9a3e1f53189df5cf0257fef6c1d1214b3901a`; immutable from
its first landing `f3da504` through `28c6837` and `a4046a8` (`git show REV:…/precision-heldout/expected.json | sha256sum`).
Tools: `1f7f995` = `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`,
`28c6837` = `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`,
pre-harm `9c54c56` = `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`.
Counter `tw-precision.py` `bd3bdc23…` (only change from `f3da504`'s `1e69be17…` is the
suite pin; `git diff f3da504 28c6837 -- .ufo/waves/round-20/tw-precision.py`).

## Re-scans I ran

All in `/tmp/mado-r20w2-AtkHeldout`; each loads the suite from its pinned commit (`f3da504`)
and the tool from `REV:tools/mado-tripwire.py`, temp copy, `python3 -I`.

| command | result |
|---|---|
| `python3 -I .ufo/waves/round-20/tw-precision.py 28c6837 --heldout` | **0/12**, score 0.0; S 0/3, W 0/6, H 0/3 |
| `python3 -I .ufo/waves/round-20/tw-precision.py 1f7f995 --heldout` | **0/12**, score 0.0 |
| `python3 -I .ufo/waves/round-20/tw-precision.py 9c54c56 --heldout` | **3/12**, score 2.5 (only fx3, fx8, fx9) |
| `python3 -I .ufo/waves/round-20/tw-precision.py 28c6837` (scored) | 172/175, 9.8286; fails `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` |
| `… 1f7f995` / `… 9c54c56` (scored) | 29/175 = 1.6571 / 110/175 = 6.2857 (matches SCORECARD.md:1329) |

If the 12 held-out are added to the same population, `28c6837` is **172/187 = 9.1979**
(P 66/66, S 17/20, W 21/28, H 51/55, L 17/18). The held-out verdicts are *identical* at
`1f7f995` and `28c6837`, i.e. the repair changes none of them.

## Per-case: want vs bash/jj semantics vs both tools

Semantics were measured, not assumed: `pacman`, `sudo` and `jj` were replaced on `PATH` by
`/tmp/mado-r20w2-AtkHeldout/lab/bin/*` stubs that log `$*` and exit 0; each script ran under
`env -i PATH=stub:/usr/bin:/bin HOME=/tmp/… bash -c`. `jj` facts come from real jj 0.45.1 in
`/tmp/r20jj/repo` with `HOME`/`XDG_CONFIG_HOME` redirected; `uv` from 0.13.0 with isolated
`UV_TOOL_DIR`/`UV_CACHE_DIR`; bash 5.3.20, git 2.56.0, Python 3.14.8.

| case | want | what semantics demand (observed) | 1f7f995 | 28c6837 | verdict |
|---|---|---|---|---|---|
| `S-…-a01` | 0, none | `pacman() { echo shadowed; }` + call → function runs, stub log empty, stdout `shadowed` | exit 1: `host_mutation pacman`, `package_query pacman:-Q` | same | want **correct**; tool emits a false positive on the function definition line (`host_mutation pacman`) and on the shadowed call. Pins a known FP. |
| `S-…-a02` | 0, none | `sudo() { echo no; }` + call → stub log empty, stdout `no`; pacman never runs | exit 1: `host_mutation sudo`, `host_mutation pacman:-S` | same | want **correct**; known FP (function shadowing not resolved). |
| `S-…-a15` | 0, none | lone `pacman() { echo shadowed; }` → nothing executes, stub log empty | exit 1: `host_mutation pacman` | same | want **correct**; the row is the definition name misread as a command. Known FP. |
| `W-…-a18` | 1, `package_query pacman:-Q` observed | `f(){ g "$@"; }; g(){ "$@"; }; f pacman -Q wayland-utils` → stub logs `pacman -Q wayland-utils` | exit 0 | exit 0 | want **correct**; known miss (rule A drops the second `def` when it re-parses the expanded body, `mado-tripwire.py:1027-1032`). |
| `W-…-a20` | 1, `host_mutation sudo` + `host_mutation pacman:-S` observed | `b wayland-utils` → `run sudo pacman -S wayland-utils` → stub logs `sudo pacman -S wayland-utils` | exit 0 | exit 0 | want **correct**; known miss (helper chain to `run` not carried into the expansion). |
| `W-…-a24` | 1, `package_query pacman:-Q` observed | `main` defined first, `run` before `main` is called → stub logs `pacman -Q wayland-utils` (bash binds at execution) | exit 0 | exit 0 | want **correct**; known miss (same one-hop loss). |
| `W-…-a13` | 1, `package_query pacman:-Q` observed | `f pacman -Q 'wayland-*'` → stub logs `pacman -Q wayland-*`; the quoted glob is one literal word | exit 0 | exit 0 | want **correct**; known miss caused by `SHELL_EXPANSION` rejecting any arg containing `*` even quoted (`:1029`). Plain-arg variant `f pacman -Q wayland-utils` gives exit 1 and `package_query pacman:-Q`, so the guard is the exact cause. |
| `W-…-p16-xargs-jj` | 1, `vcs_write jj:log` observed | `printf 'log\n' \| xargs jj` → stub logs `jj log`; jj 0.45.1 snapshots on `log` (`JJ_NO_SNAPSHOT = {"help","version"}` only, `:156`; measured `jj log -n 1` added an op) | exit 0 | exit 0 | want **correct**; known miss (stdin substitution not modelled). |
| `W-…-p32-pipe-bash` | 1, `vcs_write jj:commit` observed | `printf 'jj commit -m x\n' \| bash` → stub logs `jj commit -m x`; `commit` is a jj write verb | exit 0 | exit 0 | want **correct**; known miss (pipe-to-shell not modelled). |
| `H-…-fx3-jj-log-version` | 0, none | real jj 0.45.1: `jj log --version` → rc 2, `error: unexpected argument '--version' found`, op count 4→4 with `--ignore-working-copy`; control `jj log -n 1` 4→5 | exit 1: `vcs_write jj:log` | same | want **correct** (no op); tool keeps `jj:log` for a subcommand `--version`. Known FP, and the only one of `jj --version`, `jj --help`, `jj log -h`, `jj log --help`, `jj log --version` that fires (`jj --version`/`--help`/`-h`/`--help` are clean at 28c6837). |
| `H-…-fx8-uv-tool-install-help` | 0, none | uv 0.13.0 `uv tool install --help` → rc 0, help text, `UV_TOOL_DIR`/`UV_CACHE_DIR` remain empty | exit 1: `tool_install uv:tool-install` | same | want **correct**; known FP. |
| `H-…-fx9-pip-install-help` | 0, none | pip is absent here (`/usr/bin/python3: No module named pip`), so only `[INFERENCE]`: standard pip prints help and installs nothing | exit 1: `tool_install pip:install` | same | want **correct** [INFERENCE]; the author's own `why` flags the inference. Known FP; unverified on this host. |

**No want is semantically wrong.** Every `want_exit`/`want_findings`/`evidence` triple
matches bash/jj behaviour and the tool's own class vocabulary, including the `observed`
marker (the executing bodies/paths are visible in the transcript for all six W cases).

## Wrong / vacuous / known-miss expectations

1. **Wrong wants: none.** The 12 are valid negatives/positives; their defect is not the
   expectation but the exclusion.
2. **"A case that cannot fail": all 12, at the claim level.** They live outside
   `.ufo/waves/round-20/precision/` (the path the C1 claim names, SCORECARD.md:1239-1249),
   the counter's default `SUITE` is `precision` only, and the pre-registered admission
   guards (SCORECARD.md:1255-1263) have no held-out condition. `0/12` is reported as a
   guard *result*, never an admission criterion, so no held-out case can fail C1.
3. **Pins a known miss (want findings the tool does not emit):** `a13`, `a18`, `a20`, `a24`,
   `p16`, `p32` — six of the six W cases. Each fails at the repaired tool for a reason the
   case author's `why` already states ("rule A drops defs after one hop"; "stdin
   substitution is not modelled").
4. **Pins a known false positive (want clean, tool emits rows):** `a01`, `a02`, `a15`,
   `fx3`, `fx8`, `fx9` — eight rows over six cases at 28c6837.
5. **Vacuous `before` metadata:** the expected.json note says "`before` is the author's
   reading, re-measured by the counter" (`.ufo/waves/round-20/precision-heldout/expected.json:3`). The counter never
   reads `before` — `grep -n before .ufo/waves/round-20/tw-precision.py` returns nothing;
   `assemble-suite.py:60` copies `c.get("before", {})` verbatim. Worse, `9c54c56` has
   `CLASSES = ("host_mutation","package_query","live_probe")` (`9c54c56:tools/mado-tripwire.py:61`;
   zero `vcs_write` and zero `tool_install` occurrences). Probes at `9c54c56` return rc 0
   (clean) for `jj log`, `jj log --version`, `uv tool install foo`, `uv tool install --help`,
   `pip install foo`, `pip install --help` and `git commit -m x`. So the held-out
   `before["9c54c56"]` values are class-absence artifacts, not verdicts:
   `fx3`/`fx8`/`fx9` "pass" vacuously, `p16`/`p32` "fail" vacuously (the jj class did not
   exist). Only the seven pacman/bash cases (`a01`, `a02`, `a15`, `a13`, `a18`, `a20`,
   `a24`) have a real `9c54c56` reading.
6. **`fx9` is an `[INFERENCE]`** in a suite whose other 11 cases were measured; pip absent
   is confirmed, so its clean want is standard-pip knowledge, not a local observation.

## Held out by contract, or to protect the score?

**By chronology, pre-measurement; by contract, not registered.** The EDGE markers and
`before` values are in the wave-1 author's `cases.json`, committed at `f3da504` (17:09:29
-03), 20 minutes before the tool repair `28c6837` (17:29:03 -03); the author was blind to a
repaired tool that did not yet exist, and the assembler routes on the author's `EDGE`
prefix mechanically (`assemble-suite.py:52`), not on tool output. The commit message
itself says "175 scored + 12 held-out". So this is not post-hoc score manipulation.

But the hold-out is **not in the registered contract**:

- The pre-registration `e629f73` (SCORECARD.md:1239-1284) defines the counter, the five
  families, the score and the admission guards; it never mentions a held-out set or an
  exclusion rule. The pre-measurement corrections block (SCORECARD.md:1285-1316) does not
  add one either. The first SCORECARD mention is in the *results* commit
  (`a4046a8:SCORECARD.md:1321` "12 held out as outside the contract"), i.e. after every
  measurement; LOG.md's round-20 entry omits it entirely.
- The case author invented `EDGE` as a *landing-sequencing* hint ("so L1 can land the core
  subset alone: 40 red + 2 controls", `w1/reports/CaseAdoptW2.md`). `assemble-suite.py`'s
  docstring then calls the exclusion "the round-20 contract (E1-E4 …)" (`:5-9`). That is an
  overreach: E1-E4 are target semantics, not suite-inclusion rules, and the EDGE test is a
  single wave-1 seat's unchecked annotation.
- The label "outside E1-E4" is false for **8 of the 12** on the author's own reasoning and
  the registered family text:
  - `a18`, `a20`, `a24`, `a13`: each `why` starts "**E1**: text states the argv and both
    visible bodies …". E1's `observed` clause explicitly includes bash `command` lines and
    a literal-argv call to a visible body (gen_w1.py:36), and the tool's own docstring
    promises "`$1..$9` and `$@/$*` are substituted for shell functions"
    (`28c6837:tools/mado-tripwire.py:40`) — `a13` is a one-level case that promise should
    already cover.
  - `p16`, `p32`: the registered **W** family is "real wrapper misses (want observed)"
    (SCORECARD.md:1251); `xargs` and `bash` are the wrappers, and both `why`s argue from E1.
  - `fx8`, `fx9`: the registered **H** family is "help/dry-run non-writes (want clean) with
    write negatives" (SCORECARD.md:1251-1253), with no vcs qualifier; installer `--help` is
    exactly a help non-write. Only E4 is vcs-scoped, and E4 is not the family definition.
  - Cleanly outside the literal text: `a01`/`a02` (E3 names Python rebinding; the author
    says "E3 by analogy (bash)"), `a15` (definition only, no rule covers it), `fx3`
    (`--version` is neither help nor a dry run, and E4 names neither).

**Effect, not intent, is protective.** All 12 are red at `28c6837`, so scoring them would
report 172/187 = 9.1979 instead of 9.8286, with H 51/55 (not 51/52) and W 21/28 (not 21/22).
The hold-out removes exactly the tool's blind spots — bash function resolution (4), stdin/
pipe dataflow (2), subcommand `--version` (1), installer help (2), bash shadowing/definition
names (3) — while leaving the scored suite's `172/175` intact. The `0/12 → 0/12` guard line
is true for `1f7f995 → 28c6837`, but it is the only place the residual failures appear, and
it does not name the revision pair or the `9c54c56` 3/12 (which is itself vacuous; see
above). A reader of the C1 row would not learn that the repaired tool still fails 15 of the
187 authored cases (the 12 held out plus the 3 scored failures).

## Other defects found while scanning the 12

- **a13 exposes an undocumented tool limit.** The docstring says shell-function positionals
  are substituted (`:40`), but `:1029` refuses substitution whenever any argument matches
  `SHELL_EXPANSION` (`*`, `?`, `[`, `$`, backtick, `{`, `~`), quoted or not. `a13` is the
  quoted-`*` case; the Limits section (`:23-57`) does not state the guard, so the docstring
  claim is falsified by a one-level, same-text helper. The case correctly pins this as a
  miss, but the tool text should either fix it or list it.
- **The held-out `before` records are vacuous for five cases**: `p16`/`p32` are marked
  `fail` at `9c54c56` and `fx3`/`fx8`/`fx9` are marked `pass`, but the `9c54c56` tool has no
  `vcs_write`/`tool_install` class, so it returned clean for `jj log`/`git commit`/
  `uv tool install foo` before ever looking at the arguments. The `fail`/`pass` labels are
  class absence either way. The same caveat applies to the scored C1 row's "pre-harm
  `9c54c56` 110/175" (H 35/52 there is largely class-absence clean); the pre-registration
  only uses P at `9c54c56`, so the claim's *guard* is safe, but 110/175 is not a precision
  reading and should not be quoted as one.
- **`fx3`'s clean want is confirmed against real jj**, so it is not a pinned miss: the tool
  is wrong. The docstring's "(`help` and `--version` excepted)" (`:67`) is true only for
  bare `jj --version`; the code comment at `:591` ("`jj`, `jj --version`, `jj --help`:
  nothing is touched") confirms the exemption is the no-subcommand form, not
  `jj <sub> --version`.

## Limits

- I did not run pacman/sudo/systemctl/hyprctl or any host command; the bash semantics tests
  used PATH stubs and a fresh `/tmp` cwd. jj/uv ran only in `/tmp` with redirected
  `HOME`/`XDG_CONFIG_HOME`/`UV_*`; no lane write, no jj in the lane.
- `pip` is absent, so `fx9` is `[INFERENCE]` (standard pip `install --help`), as the author
  already states; I did not install it.
- I did not run the 11 existing suites, the whole-corpus diff, the recall/control checks or
  the gate (other seats own those); I did run the scored and held-out counters at the three
  revisions above.
- I did not audit the 175 scored cases beyond reproducing their counts; the three scored
  failures are taken as the counter reports them.
- Facts are for jj 0.45.1, uv 0.13.0, bash 5.3.20, git 2.56.0, Python 3.14.8 only. No web
  fetch was made; no receipts file is required.

## Installs

none.
