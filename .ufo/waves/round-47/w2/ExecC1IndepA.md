# ExecC1IndepA — w2 FALSIFY / C1 operability: is the C1 contract executable without oral context?

**Verdict: yes, executable — but not docstring-only.** An implementation written from the contract
(the L1 reference's *docstring*, `.ufo/waves/round-47/l1-draft/mado-terminal.py:2-88`, extracted with
`ast.get_docstring` — I never read its code) plus the pinned resolver's bytes reaches the frozen
target (`TARGET_MET`) on two of the three nonces I scored; the one miss was my own selftest design
(H5), not the model. Two behaviours the model cannot be built without are nevertheless **absent from
the contract** (H1, H2), and the first of them cost me a broken tool: **25/190** fixtures when the
missing fact is read the way the contract's wording invites. A third absent detail (H3) breaks the
option-prepend fixtures for a docstring-only reader. Three further gaps bite only inside the judge's
own harness (H4-H6: selftest minimum count, the selftest sandbox's tmpfs/readdir order, its PATH).

Every locator below is computed (`grep -n`); the whole evidence set is
`.ufo/waves/round-47/w2/ExecC1IndepA/c1-receipt.txt`. Pins/inputs used:
`fetch/xdg-terminal-exec` sha256 `89f2be9a…3127ac`, counter `c1-r47-terminal.py` sha256 `2b9c2d0e…`,
fixtures `c1-r47-fixtures.json` sha256 `4836cc1d…`, L1 reference `762d042c…`.

## 1. What was built and measured

* Candidate: `.ufo/waves/round-47/w2/ExecC1IndepA/mado-terminal.py`, 1453 lines, sha256
  `1a60269be64ded7163fbe5e1f3662cd007b7f38e70a787d918160aa31ab7f60f`. Pure stdlib, no process, no
  socket, no write; `--selftest` has 54 cases whose expectations were produced **by the pinned
  resolver on identical trees** (not by my model).
* Frozen counter, seat recipe, committed blob in a `--shared` scratch clone at
  `d7527d60…` + one `cand` commit (nothing of the lane's index touched):

| run | nonce | result |
|---|---|---|
| 1 (pre-fix selftest) | 7 | `fixtures=190/190 explained=190/190 generated=150/150 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED rev=559fb90f…` — `clause=s last='MADO_TERMINAL_SELFTEST: 51/54 passed'` |
| 2 | 4242 | `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=a9dd9978…` (exit 0) |
| 3 | 20261026 | `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=0626d628…` (exit 0) |

  Run 1's line is quoted from that run's own output (not captured to a file; the candidate no longer
  exists). Runs 2 and 3 are captured verbatim in `c1-receipt.txt` §H7 (`score2.txt`, `score3.txt`).
* Local differential harness (not the judge): my tool vs the pin, per fixture/`gen_case`, root
  normalised — **190/190 fixtures and 200/200 generated cases (seed 424242), 0 diffs**; 6 s per round
  instead of 60-77 s, which is how the two model bugs were found.

## 2. Holes

### H1 — BLOCKING: the application dirs carry a trailing `/`; the contract hides it (and suggests the opposite)

The resolver builds the entries dir as `<data>/applications/` **with** the slash (`pin:168`), so the
`find` start is `<data>/applications/.` (`pin:762`) and both `-path` tests are anchored on
`<data>/applications/./` (`pin:773`). The contract's step 4 says only
"`find -L <dir>/. -type f` over the application dirs" (`DOC:49`) and "a path counts when its part after
`<dir>/./` starts with …" (`DOC:51`), while step 2 ends with "One trailing '/' of a dir is removed."
(`DOC:38`). A reader who builds `…/applications` (no slash) gets **zero** entries: `find -L
…/applications.` cannot even start.

Cost measured (receipt §H1; `notrail.py` was my tool with one string changed —
`sed 's#base + "/applications/"#base + "/applications"#' mado-terminal.py` — run through the
same per-fixture differential harness; both are scratch-only, the frozen fixtures are the judge):

```
$ TOOLX=…/notrail.py NGEN=0 python3 diff2.py
fixtures: 25/190 ok
$ /usr/bin/find -L …/ff/applications. -type f
/usr/bin/find: '…/ff/applications.': No such file or directory
```

What it attacks: clause f (and every clause that needs a selected entry). Fix for v2: state that the
applications entry is `<dir>/applications/` (slash kept), the find start is that string + `.`, and the
`-path` patterns are built from the same string.

### H2 — BLOCKING-ish: `read` with N variables keeps the *raw remainder*, and the contract only says "`read` rules"

`IFS=':' read -r a b c` on `/execarg_default:x:-x:` yields `c=-x:` (trailing delimiter kept) but on
`k:x:y:` yields `c=y` (single trailing delimiter dropped); both forms are pinned by fixtures. The
contract says only "Lines are read like `read -r` …" (`DOC:40`) and "split at the first ':' into id and
action with bash `read` rules" (`DOC:44`); `--app-id=`/`--title=`/`--dir=` use the same construct
(`pin:1238,1246,1254`), and `/execarg_default:<id>:<arg>` (`pin:407`) is exactly where I got it wrong.

Two measured bugs of mine: `--title=x=` produced `x=` instead of `x` (fixture
`l1-title-trailing-equals`, `expect stdout "foot\n--title\nx\n"`), and `a:b:` collapsed to `a:b`
(generated case `g022`). Receipt §H2:

```
$ bash -c 'for s in "k:x:y:" "/execarg_default:kitty.desktop:a:b:" "k:x:y:z:"; do IFS=: read -r a b c <<< "$s"; printf "%-38s [%s][%s][%s]\n" "$s" "$a" "$b" "$c"; done'
k:x:y:                                 [k][x][y]
/execarg_default:kitty.desktop:a:b:    [/execarg_default][kitty.desktop][a:b:]
k:x:y:z:                               [k][x][y:z:]
```

What it attacks: clause f (two fixtures) and clause g on every nonce (the generator emits
`/execarg_default:{id}:a:b:`).

### H3 — the `=<value>` concatenation for TerminalArgDir/Title/AppId is not in the contract

Step 7 prints "`--app-id/--title/--dir/--hold` arguments where the entry defines them" (`DOC:76-77`)
but never says that a TerminalArg* value ending in `=` is concatenated with the option value instead
of taking a separate argv word (`pin:1400-1444`, three `*=` cases). A docstring-only reader emits
`--working-directory= /srv` (two words) and fails fixture `l1-cmd-dir-arg`
(`expect "foot\n--working-directory=/srv\n"`) and the option-prepend group. Reproduce:

```
$ grep -n 'Exec words, then' .ufo/waves/round-47/l1-draft/mado-terminal.py   # DOC:76 — no '=' rule
$ grep -n '\*=\*)' .ufo/waves/round-47/fetch/xdg-terminal-exec                # pin:919 is the key case; +1400-1413 is Dir's '=' test
```

I was not personally bitten because I read the resolver for this section; the contract alone is
insufficient. Attacks clause f.

### H4 — the selftest minimum (30 cases) exists only in the counter

`DOC:26` fixes only the shape: "last line `MADO_TERMINAL_SELFTEST: N/N passed`; exit 0 iff all pass".
The judge requires `N >= 30` (`quality/counters/c1-r47-terminal.py:73 SELFTEST_MIN = 30`, `:402`). A
contract-faithful tool with, say, 8 cases fails clause s with no hint from the contract. Reproduce:
`grep -n SELFTEST_MIN quality/counters/c1-r47-terminal.py`. Attacks clause s.

### H5 — "Hermetic cases built under $TMPDIR": the judge's $TMPDIR is a fresh tmpfs and the PATH has 7 commands

Clause s runs the selftest with `TMPDIR=/tmp` inside bwrap's tmpfs and `PATH=/oracle/bin`
(`counter:13,395`). Readdir order is filesystem-dependent, so a selftest whose *expectations* rely on
the order of its own two-entry trees is not hermetic in the judge's sense. This cost me the whole of
run 1 (51/54 in the sandbox vs 54/54 on the host). Reproduce against the pin itself (receipt §H5):

```
$ python3 orderprobe.py
/fast/…/ord  readdir=['foot.desktop','alacritty.desktop'] -> --print-id rc=0 'alacritty.desktop'
/dev/shm/ord readdir=['alacritty.desktop','foot.desktop'] -> --print-id rc=0 'foot.desktop'
```

What it attacks: clause s (and, for anyone who generates expectations on a different fs, clause f/g).
Fix for v2: say the selftest sandbox's $TMPDIR is a tmpfs and that the expectations must not depend on
readdir order or on host binaries outside the resolver's own externals; better, state `N >= 30`.

### H6 — the contract's `-type f` is wrong (harmless on stdout/rc)

`DOC:49` says `find … -type f` over the application dirs, but find's precedence binds `-type f` only to
the **first** dir group (`-type f ( e1 ) -o ( e2 ) …`), so a *directory* named `x.desktop` under the
2nd+ data dir is printed and registered as an entry. Receipt §H6:

```
$ /usr/bin/find -L …/g1/applications/. …/g2/applications/. -type f '(' -path …g1… ')' -o '(' -path …g2… ')'
$S/ev/g2/applications/./dir.desktop
$S/ev/g2/applications/./real.desktop
```

Observable only in the debug trace and in `TryExec=<that bogus id>`; unobservable for the counter. I
implemented the true precedence anyway.

### H7 — smaller wording gaps (no measured failure)

* `DOC:74` fixes the stderr text but not that the "No valid …" list is the app dirs joined with `:`
  *including* their trailing slashes — stderr is not judged, so cosmetic.
* "(default $HOME/.config)" (`DOC:35`, `DOC:50`) does not say an *empty* `XDG_CONFIG_HOME`/
  `XDG_DATA_HOME` also means the default (`pin:145,167`); fixtures `p1`/`p2` and `p3` pin the
  difference between unset and empty.
* An empty `XTE_EXECARG_COMPAT=`/`XTE_CACHE_ENABLED=` is not "set" in the `check_bool` sense
  (`pin:50-64`) — the contract says only "set in the environment win over any directive" (`DOC:42`).
  No fixture or generated case uses those variables (checked: 0/190 fixtures set any `XTE_*`).

## 3. What the contract got right that a reader could not have guessed (verified, so v2 must keep it)

* "first ':' for the action and the last ':' for the id" (`DOC:55`) — a real trap, stated.
* Key lines matched "against its WHOLE text (so `CategoriesX=` counts as Categories)" (`DOC:59`) —
  verified (my `category-prefixed-key` case is accepted by the pin).
* "A read that ends while the last executed step failed also rejects (POSIX while-loop status)"
  (`DOC:67`) — verified: an entry whose last line is `[Desktop Entry]` under an action request is
  rejected (`rc 1`, empty stdout), while a trailing `[Other]` is accepted (receipt §V1). This is
  unguessable and load-bearing.
* "The last path seen for an id wins (so XDG_DATA_HOME beats XDG_DATA_DIRS)" and "put at the FRONT of
  the fallback list" (`DOC:52-53`) — verified; the fallback order is reverse readdir, which is why
  expectations must not depend on it (H5).
* "'+id' protects id from a later '-id' … first word wins" (`DOC:46-47`) — verified both directions
  with single-entry trees (`+` then `-` → selected; `-` then `+` → excluded, rc 1).
* "`command -v` finds aliases (ids registered in step 4 and not yet tried), the script's own
  functions, bash builtins and reserved words, a path containing '/' … an empty PATH entry is the
  working directory" (`DOC` step 5) — I implemented exactly this list and needed every clause
  (`TryExec=printf`, `TryExec=read_cache`, `TryExec=<id>`, `TryExec=$ROOT/bin/<n>`, `Exec=env …`).
* The cache/out-of-contract paragraph (`DOC:81-86`) is accurate: `--print-id`/`--print-path` alone never
  write the cache, and the cold path is what the judge builds.
* The cited script line ranges are all correct (make_paths 143, gen_hash 179, cache 217-298, list lines
  351-475, entries 754-800, keys 802-968, entry read 970-1018, candidates 1055-1111, options 1224-1322,
  printing 1325-1491) — checked with `grep -n '^[a-z_]*() {'`; the contract's locators are trustworthy.

## 4. Files, risks, blockers

Files written (seat scope only; no tracked file edited, no git/jj mutation in the lane):

* `.ufo/waves/round-47/w2/ExecC1IndepA.md` (this report)
* `.ufo/waves/round-47/w2/ExecC1IndepA/mado-terminal.py` (candidate; **not** `tools/mado-terminal.py` —
  the L1 integrates)
* `.ufo/waves/round-47/w2/ExecC1IndepA/c1-receipt.txt` (every command and output cited here)
* `.ufo/waves/round-47/w2/ExecC1IndepA/probes/{orderprobe,whileprobe}.py` (the two probes, re-runnable
  with `ORACLE=`/`EXT=` pointing at a copy of the pin and its seven externals; recipe in the receipt header)

Risks / limits of this falsification:

* I scored only my own committed candidate (scratch clone HEAD), not the base and not the round tip;
  the base → MISSED and the tip are the parent's runs.
* The `--test` argv variants of clause g could not be verified locally: the host guard allows the
  resolver only with a `--print-*` option, so `--test` output is covered only by the frozen counter's
  own oracle runs (150/150 on two nonces) and by 2 selftest cases derived from `--print-cmd`.
* My tool models the cold path only, as the contract says; a warm cache is out of contract.
* Clause r is satisfied by construction (no `subprocess`, no sockets) and measured `trips=0` on every
  run; clause i needed no work (pure Python, no `/usr/bin` access).
* Nothing to escalate: no blocker, no host mutation, no package install (no tool was installed or
  upgraded for this seat).
