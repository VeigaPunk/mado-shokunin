# R100MScoutPath - C1 surface reconnaissance (read-only)

Seat: scout (leaf; no subagents dispatched). Lane `mado-shokunin`, base `43309e6a`
(branch `master`). Read-only: the candidate `tools/mado-launchenv.py` was **not** touched; the
oracle was driven only as an instrument (it spawns `/usr/bin/gio` under an env with no host PATH).

## 0. Ground re-measured by this seat (nothing inherited)

| fact | value | how |
|---|---|---|
| glib2 | `2.90.1-1` | `pacman -Q glib2` |
| `/usr/bin/gio` sha256 | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` | `sha256sum`; the oracle re-hashes it on every run and prints `MADO_LAUNCHENV_PROBE_META.gio_sha256` |
| round-99 oracle sha256 | `cbfff7a4b64e63f3e6861d29d1c5639de2c25abe2f6875088918abb45d129199` | `sha256sum`; matches the frozen pin in `claims-declaration-r100.md` |
| base-rev tool bytes | `tools/mado-launchenv.py` @ `43309e6a` = sha256 `a63c20c886a2bd840d80966d531e055e9c4f5d3accb431e4b0e317e04523eb16` | `git show 43309e6a:tools/mado-launchenv.py \| sha256sum` |
| base-rev sibling bytes | `tools/mado-execargv.py` @ `43309e6a` = sha256 `49f7fecdc3bef99a077fe73ac12f5fe211d7ae8c41df5ddc949daf685405f713` | same |
| oracle legs measured | 27 ad-hoc cases (10 + 8 + 3 + 2 + 4) | driven through the **oracle module** (`measure_case`, `runs=2`), each `agreed=True`, total wall 30.6 s + 23.0 s + 9.3 s + 15.5 s |

## 1. Every branch of the program lookup in `tools/mado-launchenv.py` (file:line)

Base-rev file (954 lines, sha `a63c20c8`). Line numbers below are from the **base-rev** bytes;
the landed `219e14f4` copy adds 27 selftest lines at `:615+` and shifts nothing above `:615`.

| branch | file:line | produces |
|---|---|---|
| `DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'` | `:121` (comment at `:120`) | the literal the C falls back to |
| `PROCESS_PATH` sentinel | `:126`, resolved at `:297-298` (`os.environ.get('PATH')`) | `None` when the model process has no `PATH` key; `''` when the key is present but empty |
| `--path ""` (set-but-empty) | `:471-476` (`parse_cli` takes the next argv verbatim) | `path_env = ''` -> one **empty** PATH entry (cwd), **no** `./` in argv0 |
| working-dir join (pre-walk) | `:196-197` | `program = join(working_dir, program)` when `working_dir` is set and `program` is relative - this is `gutils.c:322-327` |
| absolute-or-slash branch | `:198-204` | `gutils.c:331-357`: absolute program -> tested and returned as-is (`:200-201`); relative-but-contains-`/` -> joined to cwd (`:202`); absolute-but-missing -> `None` (`:203-204`) |
| `path is None` -> default | `:205-207` | the `DEFAULT_SEARCH_PATH` fallback (`gutils.c:370-389`) - **the branch C1 cores** |
| empty-entry rule | `:214-215` (`if entry == '': startp = program`) | `gutils.c:471-475`: an empty entry yields the **bare** program name, so argv0 has no `./` |
| `.` entry | `:216-217` (`startp = entry + '/' + program`) | `gutils.c:476-477` + the walk's own `name` buffer: argv0 keeps the `./` |
| relative hit -> absolute | `:220-223` (`_join2(os.getcwd(), startp)`) | `gutils.c:490-497`: the returned string is cwd-joined, and a `.` entry keeps `./` |

### argv0 string per branch (measured)

| case | branch taken | argv0 produced |
|---|---|---|
| `Exec=probe`, program at the case root, PATH **absent** | default `/bin:/usr/bin:.` -> `.` entry -> relative hit | `{root}/./probe` |
| same, PATH **set empty** (`path: []` / `--path ""`) | single empty entry -> bare name | `{root}/probe` |
| same, `--path /bin:/usr/bin:.` | explicit `.` entry | `{root}/./probe` |
| `Exec=env` (only in `/usr/bin`), PATH absent | default -> `/bin` hit first | `/bin/env` |
| `Exec=env`, `--path /usr/bin` | explicit dir entry | `/usr/bin/env` |
| `Exec=env`, PATH set empty | empty entry -> cwd -> miss | refusal `load` / `exec-argv0` |
| `Exec=probe` in `{root}/bin`, PATH absent | default does not know the case-private dir | refusal `load` |
| `Exec=probe` in `{root}/bin`, `--path {root}/bin` | explicit entry | `{root}/bin/probe` |
| `Exec=probe` in `{root}/work`, `Path={root}/work`, PATH absent | **pre-walk working-dir join** (`:196-197`) short-circuits the PATH entirely | `{root}/work/probe` |
| `Exec=probe` in `{root}/work`, `Path={root}/work`, PATH set empty | same pre-walk join | `{root}/work/probe` (identical) |

The two rows that differ most sharply: **`{root}/./probe` vs `{root}/probe`** (the `.`-entry rule
vs the empty-entry rule) and **found vs refused** (default `/bin:/usr/bin:.` reaching a host
program vs the empty entry not reaching it).

## 2. The two round-99 `path-unset` cases cannot reach `gutils.c:370-382`

`.ufo/waves/round-99/controls/launchenv-cases-r99.json` - 67 cases, 31 classes; **2** carry
`"path": null`, both `class: "path-unset"`, and **both carry an absolute `Exec`**:

| id | `Exec` | `Path` | why it never reaches the PATH source |
|---|---|---|---|
| `pu-abs-work` | `"{root}/probe.sh"` | `"{root}/work"` | `original_program` is absolute -> `gutils.c:332` `g_path_is_absolute(program)` is true -> the absolute-or-slash branch at `:338-357` returns before `:368` resets `program` and before `:370` reads `path` |
| `pu-abs-root` | `"{root}/probe.sh"` | absent | same: absolute `Exec` -> returns at `:357` |

Measured confirmation: driving the **oracle** on both cases with `path: null` gives
`launches=1` and `argv [["{root}/probe.sh"]]` - byte-identical to driving the **candidate**
with `PATH` absent and with `PATH=""` (the r99 counter leg). Both legs agree, so neither case
can distinguish unset from empty: their answer is PATH-independent. **Zero** frozen round-99
cases reach `gutils.c:370-382`; the class census confirms it - only 13 of 67 cases carry a
slash-free `Exec`, and every one of those has an explicit `path` list, never `null`.

## 3. `gutils.c` sentences that fix the default, the empty entry and the absolute-or-slash short-circuit

Committed bytes: `.ufo/waves/round-99/fetch/gutils.c` (glib 2.90.1).

**The default (`:370-389`)** - note the *literal* is at `:388`, not `:382`:

```
370:  if G_LIKELY (original_path == NULL)
371:    path = g_getenv ("PATH");
372:  else
373:    path = original_path;
374:
375: #if defined(G_OS_UNIX)
376:  if (path == NULL)
377:    {
378:      /* There is no 'PATH' in the environment.  The default
379:       * search path in GNU libc is the current directory followed by
380:       * the path 'confstr' returns for '_CS_PATH'.
381:       */
382:
383:      /* In GLib we put . last, for security, and don't use the
384:       * unportable confstr(); UNIX98 does not actually specify
385:       * what to search if PATH is unset. POSIX may, dunno.
386:       */
387:
388:      path = "/bin:/usr/bin:.";
389:    }
```

**The empty-entry rule and the absolute-or-slash short-circuit** - these live *outside*
`:359-389`, at `:471-477` and `:329-366`:

```
329:  /* If it is an absolute path, or a relative path including subdirectories,
330:   * don't look in PATH.
331:   */
332:  if (g_path_is_absolute (program)
333:      || strchr (original_program, G_DIR_SEPARATOR) != NULL
334: #ifdef G_OS_WIN32
335:      || strchr (original_program, '/') != NULL
336: #endif
337:      )
338:    {
339:      if (g_file_test (program, G_FILE_TEST_IS_EXECUTABLE) &&
340:          !g_file_test (program, G_FILE_TEST_IS_DIR))
...
357:          return g_steal_pointer (&out);
358:        }
359:      else
360:        {
361:          g_clear_pointer (&program_path, g_free);
362:
363:          if (g_path_is_absolute (original_program))
364:            return NULL;
365:        }
366:    }
```

```
471:      if (p == path)
472:        /* Two adjacent colons, or a colon at the beginning or the end
473:         * of 'PATH' means to search the current directory.
474:         */
475:        startp = name + 1;
476:      else
477:        startp = memcpy (name - (p - path), path, p - path);
```

`:475` (`name + 1`) is the **empty**-entry rule: the bare program name, no `./`. `:477` copies
the entry text (e.g. `.`) ahead of the separator, which is why the `.` entry yields `./probe`.
The `:471` comment is the C's own statement of the empty-entry rule.

**Locator discrepancy worth flagging to the L1.** The declaration and the tool disagree with
the committed bytes about where the default lives:

- `claims-declaration-r100.md:12` and `claims.json:12` say `gutils.c:370-382`.
- The committed bytes put the `if (path == NULL)` guard at `:376` and the **literal
  `"/bin:/usr/bin:."` at `:388`** - outside `:370-382`. `claims.json` says `:376-389`, which is
  right; `claims-declaration-r100.md` says `:370-382`, which stops 6 lines short of the literal.
- The **candidate tool itself** carries the same drift: `tools/mado-launchenv.py:120` reads
  `# gutils.c:409-421: PATH unset in the environment -> this search path.` - but `:409-421` is
  the **Windows** branch (`g_strconcat (windir, ";", path, ...)`), not the Unix default. The
  correct locator is `:376-389`. (The declaration's `:370-382` is the *nearest* of the three,
  but still misses the literal.)
- The tool's docstring at `:192-193` cites `:479-482` and `:489-496` for the walk's working-dir
  join and the relative-hit absolutisation; the committed bytes put those at `:479-484` and
  `:490-497` - close, but the walk's `if (working_dir && ...)` opens at `:479` and the
  absolutisation block is `:489-497`.

None of this changes a modelled behaviour - the tool's bytes are right and its selftest is
green (`MADO_LAUNCHENV_SELFTEST: checks=95 failed=0`). It is a **citation** defect only
(M99-2's class: a locator inferred from a range rather than produced by `grep -n`), and it
should be corrected append-only, not silently.

## 4. Case classes that separate unset from its three neighbours

The oracle's `path_string` (`:195-201`) decides what each case can express:

```
197:    entries = case.get("path", [])
198:    if entries is None:
199:        return None            # -> the child env carries NO PATH key
200:    probe = os.path.join(root, "probe.sh")
201:    return ":".join(sub_placeholders(e, root, probe) for e in entries)
```

`path: null` -> `None` -> `measure_once` (`:369-371`) omits `PATH` from the child env entirely.
`path: []` -> `""` -> `env["PATH"] = ""` (set but empty). **The oracle can express both**; the
r99 case file simply never used the second (`"path": []` occurs 0 times; `"path": null` twice).

| # | neighbour to separate from | class | case shape | measured oracle label | expressible by the r99 oracle? |
|---|---|---|---|---|---|
| 1 | `PATH=""` (set-but-empty) | `path-default-sysbin` | `TryExec=sh`, `Exec={root}/probe.sh` | unset -> **found** (in `/bin`), `path: []` -> **refused** `load` | **yes** - `path: null` vs `path: []` |
| 2 | the ambient search (a case-private dir) | `path-default-private` | program only in `{root}/bin` | unset -> **refused** `load`; `path: ["{root}/bin"]` -> **found** `{root}/bin/probe` | **yes** - `path: null` vs `path: ["{root}/bin"]` |
| 3 | the working-dir join | `path-default-cwd` | `Path={root}/work`, program in `{root}/work` | unset -> `{root}/work/probe`; `path: []` -> `{root}/work/probe` (**identical** - the pre-walk join at `:196-197` short-circuits the PATH) | **yes** - but note it separates the *join*, not unset-vs-empty |
| 4 | the `.` entry vs the empty entry | `path-default-dot` | `Exec=probe` at the case root | unset -> `{root}/./probe`; `path: []` -> `{root}/probe` | **yes** - `path: null` vs `path: []` |

**Requirement 3 is the one that does *not* separate unset from empty by itself.** With
`Path=` set, the tool's pre-walk working-dir join (`:196-197`, i.e. `gutils.c:322-327`) makes
`program` absolute *before* the PATH is consulted, so the PATH value is irrelevant: measured
oracle labels for `path: null` and `path: []` are byte-identical (`{root}/work/probe` both
times). The class still earns its keep - it shows the join dominating - but the *unset vs
empty* separation has to come from classes 1 and 4.

## 5. Consumers of `tools/mado-launchenv.py` and their sha256 pins

The tool's bytes are pinned in **five** places, all to the same value at the base rev:

| consumer | file:line | pin |
|---|---|---|
| `SKILL.md` registry row `mado-r99-launchenv` (the gate row) | `SKILL.md:2984` | `--expect-tool-sha256 a63c20c886a2bd840d80966d531e055e9c4f5d3accb431e4b0e317e04523eb16` |
| `SCORECARD.md` (the C1 row) | `SCORECARD.md:5625` | same value |
| `.ufo/waves/round-99/claims-declaration-r99.md` (counting command) | `:167` | same value |
| `.ufo/waves/round-99/claims.json` (counting command) | `:17` | same value |
| `.ufo/waves/round-99/controls/launchenv-mutants-r99.json` (`candidate_sha256`) | `:4` | same value |
| `.ufo/waves/round-99/build/mado-launchenv.py` (the r99 candidate draft) | - | byte-identical to the landed base (`sha256sum` confirms) |
| `.ufo/waves/round-99/build/c1-r99-launchenv.py` (the r99 counter draft) | - | byte-identical to `quality/counters/c1-r99-launchenv.py` (`52abbbaa78e358ef646f3e7e92c1bd36516196540d4bb0221f38edd368801ecd`) |

Hard consumers (code that reads the tool's bytes at run time):

| consumer | how it consumes | pin |
|---|---|---|
| `quality/counters/c1-r99-launchenv.py` | `git show <rev>:tools/mado-launchenv.py` (`:846`), sha-checked at `:855`; the tool's sibling `tools/mado-execargv.py` likewise at `:841` | `--expect-tool-sha256` / `--expect-execargv-sha256` |
| `.ufo/waves/round-99/build/c1-r99-launchenv.py` | the same counter, pre-landing draft | same |
| `quality/tool-ledger.md:234` | a **ledger row** (population/ledger gate `quality/check-tool-ledger.py`), not a sha | none (name + pointer only) |
| `SKILL.md:2983` | the registry **probe** row `mado-launchenv` (the CLI contract) | none (no sha) |
| `.ufo/waves/round-99/controls/launchenv-fresh-r99.py` | consumes the **oracle** (`launchenv-probe-r99.py`), not the tool | `oracle_sha256` in the envelope |

The r99 counter is also a **structural** consumer: it drives the oracle by `importlib` from
beside the `--cases` file (`:895-906`) and pins the renderer's sha256 twice (envelope
`oracle_sha256` and `renderer_sha256`, both `cbfff7a4...d129199`). A change to the tool's bytes
therefore breaks the r99 gate's `--expect-tool-sha256` **and** the r99 mutant file's
`candidate_sha256` - the two pins move together.

### The round-99 counter leg cannot see the unset branch (the load-bearing finding)

`quality/counters/c1-r99-launchenv.py:331` builds the candidate argv as
`["--path", pstr] if pstr is not None else []`, and `:307` runs the tool with
`env = {"PATH": "", "LC_ALL": "C", "HOME": home}`. For a `path: null` case `pstr is None`, so
**no `--path` is passed** - and the tool then reads its own process `PATH` (`:297-298`), which
the counter has forced to `""` (set-but-empty), not absent. Measured, same case, same tool:

```
env PATH="" , no --path   -> argv0 {root}/probe      <- the EMPTY-entry answer
env with NO PATH key      -> argv0 {root}/./probe     <- the DEFAULT answer
```

So under the round-99 leg a `path: null` case is scored against the **empty** answer even
though the oracle measured the **unset** answer - the two are exactly the pair
`{root}/probe` vs `{root}/./probe`. The r99 case file escapes this only because both of its
`path-unset` cases carry an **absolute** `Exec`, whose answer is PATH-independent. The
round-100 counter must therefore run a `path: null` case with **no `PATH` key in the child env
and no `--path`** (contract 1: "no `--path` and no `PATH` in the model process's environment =
PATH unset").

*(The landed round-100 counter `219e14f4` implements exactly this - `.ufo/waves/round-100/build/
c1-r100-launchenv-path.py:316-327` has a `path_unset` flag that drops the `PATH` key, and `:28-32`
documents it. The finding was independently reproduced before that landing; see section 0.)*

## 6. What this seat measured vs what it inferred

**Observed** (measured on this host, this session): every table row in section 1 and section 4; the two
`path-unset` labels in section 2; the `gutils.c` line numbers and quotes in section 3 (by `grep -n` on the
committed bytes); the five sha256 pins in section 5; the counter-leg gap in section 5; the candidate's
selftest green at `checks=95 failed=0`.

**Inferred** (labelled as such): that the landed `219e14f4` counter is green end-to-end - I did
**not** run the round-100 counting command (it is the L1's job, and it takes >300 s under the
current load). The r100 artifacts I read are landed bytes, not my measurements.

**Unknown / not established**: whether `/usr/bin/env` and `/bin/env` are the same inode on
every host (they are here - `/bin` is a symlink to `usr/bin`; `ls -la` shows the same size and
the `/bin -> usr/bin` symlink). A case that depends on `/bin` vs `/usr/bin` ordering would be
host-specific; the r100 `path-default-sysbin` class uses `TryExec=sh` and an **absolute** `Exec`,
so it does not depend on that ordering.

## 7. Lane bounds and hygiene

- Only the two named files were written: this report and
  `.ufo/waves/round-100/receipts/scout-path-r100.txt`.
- The candidate `tools/mado-launchenv.py` was **not** modified (base bytes
  `a63c20c8...eb16` unchanged at the base rev; the later `219e14f4` landing is the L1's).
- No git/jj command was run that mutates anything; `git show`/`git diff`/`git log` only.
- No subagent dispatched (leaf seat).
- The oracle was used as an **instrument** (it spawns `/usr/bin/gio`); every launch ran under an
  env with **no host PATH** - the oracle's own `env` dict is `LC_ALL`/`HOME`/`PROBE_OUT` (+`PATH`
  only when the case names one), so no real terminal was ever started. The `Terminal=true`
  probe I ran was the **candidate tool** (which spawns nothing) - it predicted
  `terminal=xdg-terminal-exec` from the host's `/usr/bin/xdg-terminal-exec`, and I did **not**
  execute that prediction against the host.
- No pacman transaction, no sudo, no host service, no sysctl, no `~/.config` write, no
  credential read. **No tool was installed or upgraded** (none needed; stock `python3` 3.14 +
  stdlib).
- Scratch `$HYAKU_SCRATCH/mado-r100/R100MScoutPath` was removed before this yield (verified
  absent).
