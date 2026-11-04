source: S438 — git v2.56.0 `Documentation/git.adoc` (tag v2.56.0, fetched 2026-11-03, sha256 050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79, 47005 bytes) — the documented statement that `--no-replace-objects` *is* exporting `GIT_NO_REPLACE_OBJECTS`, and that the variable acts when it is "setting and exporting" — the ground for reading a guard as an environment that must reach the child, not a string that merely occurs in the file
verified-at: 2026-11-03
recheck: 90d — re-fetch the tag's `git.adoc` and re-hash it; also when the host git leaves 2.56.0, when the census population regex or the frozen control set changes, or when the repaired gate set moves

# Lane gate guards: key position, dominance, and what a guard mention does not prove (MADO-R69-1)

## Scope

Lane-tooling scope only. This entry explains the mechanics behind round-69 claim
C2 (`claims-declaration-r69.md`, C2 §): which environment constructions the lane's
guard census now accepts as carrying `GIT_NO_REPLACE_OBJECTS` into a git child, why a
key in *value* position or a construction that never reaches a launch is not a guard,
where the counted population begins and ends, and what a green census line does not
establish. It is not a desktop claim, not a state-cell truth claim, and not an
authenticity claim about repository objects. The replacement rule and the object-read
surface stay in the held rows S436 and S437; this entry opens S438 for the sentence
that says the guard is the *exported environment*, and states which sentence comes from
which source.

Host git measured for the fetch: `git --version` → `git version 2.56.0`.

## 1. The documented ground (`[INF-docs]`, tag v2.56.0)

Two passages in `git.adoc` carry the whole argument. The option entry says the flag
is not a mode of its own:

> "--no-replace-objects:: Do not use replacement refs to replace Git objects. This is
> equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable with any
> value." (S438:178-181)

and the environment-variable entry says what makes it act:

> "`GIT_NO_REPLACE_OBJECTS`:: Setting and exporting this environment variable tells Git
> to ignore replacement refs and do not replace Git objects." (S438:927-929)

The SYNOPSIS lists the option on the top-level `git` invocation (S438:14), so the
option and the variable name are the same switch at two layers. The consequence the
census turns on is documentary, not behavioural: what disables replacement is the
environment the child *receives*. A mapping that is constructed, then dropped,
overwritten, or built in a function nobody calls, is not an environment any child sees.
That is the whole difference between the round-68 rule and this one; the runtime effect
of a guarded environment is a separate, unmeasured claim (see §5).

## 2. Key position

The round-68 classifier accepted any occurrence of the key's *string* as a descendant
of an env-named binding or an `env=` value. A dictionary with the key as a **value** —
`{"PATH": "/usr/bin", "LABEL": "GIT_NO_REPLACE_OBJECTS"}` — passes that rule while
constructing no guard at all (control `value-position-only`, measured `7/11` for the
round-68 rule in `.ufo/waves/round-69/control-baseline-r69.txt`).

The round-69 rule accepts the key only in **key position**: a dict-literal key, a
subscript store `env[KEY] = …`, an `update`/`setdefault` keyword, or a `dict(KEY=…)`
keyword. Value position, an f-string fragment, a comment and a docstring are not
guards. This is a bounded syntactic rule — it does not evaluate what the value is, so
`GIT_NO_REPLACE_OBJECTS="0"` is counted as a guard and in fact disables replacement.

## 3. Dominance — the guard must reach a `git` launch

A construction counts only when the guarded environment reaches a call that launches
`git` (the call's argv literal, or a name bound to one, contains `git`). Three flows are
accepted, all inside one module:

| flow | shape | example in the population |
|---|---|---|
| a — inline | `env=<guarded mapping>` at the git call | `quality/check-deliverables.py:96` (`dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")`) |
| b — binding | an env-named name bound to a guarded mapping or to a local *producer* function that returns one, used as `env=` or as an argument at the call, with no intervening rebinding to a mapping without the key | `quality/check-axis-scores.py:97-102`; `quality/check-evidence-pointers.py:71-72` (module constant); `quality/check-freeze-order.py:42-60` (producer + `env=env`) |
| c — one hop | the guarded name passed as an argument to a locally defined function whose env-named parameter is passed as `env=` at the call | `quality/check-anchor-cover.py:23-27` with the `env` argument at `:105` |

Constructions inside a literal-false branch (`if False:` / `while False:`) are excluded
by line. A guarded binding that is overwritten before its first use is excluded; an
*unused* helper that builds a guard does not make the file guarded, because the guard
never reaches the reader call. Those three exclusions are the four cases the round-68
rule accepted and this one rejects:

| rejected shape | why the round-68 rule accepted it | r69 verdict |
|---|---|---|
| value position only | the string was a descendant of the env mapping | `(reader, no guard)` |
| `if False:` guard, plain env at the call | the dead assignment is still an AST assignment | `(reader, no guard)` |
| uncalled helper returns a guarded env | the helper's assignment is a guard somewhere in the file | `(reader, no guard)` |
| guarded env overwritten before use | the construction exists, so it was counted | `(reader, no guard)` |

The two flows the round-68 rule missed for the same reason (a name, not a literal, was
handed over) are accepted now: a *producer* function (`env = git_env(work)` then
`env=env`) and an argv bound to a name (`cmd = ["git", …]` then
`subprocess.run(cmd, env=git_env())`). `quality/check-freeze-order.py` and
`quality/check-wave-done.py` are those shapes.

## 4. Population boundary

Population: every tracked `quality/check-[^/]+\.py` file at the measured revision — 20
files at `5fc29ae7`. Readers: 13 (git token + a frozen object-read verb); guarded: 13;
unguarded: 0. The guard shapes among the 13 are not uniform, which is why the flow table
matters:

| shape | files |
|---|---|
| inline `env=dict(os.environ, …)` | `check-deliverables.py`, `check-landed-contract.py`, `check-round-outcome-first.py`, `check-session-material.py` |
| local env name + subscript store, `env=env` | `check-axis-scores.py`, `check-control-receipts.py`, `check-index-rows.py`, `check-index.py`, `check-tool-ledger.py` |
| module constant | `check-evidence-pointers.py` |
| producer function | `check-freeze-order.py`, `check-wave-done.py` |
| one-hop argument | `check-anchor-cover.py` |

Outside the population: the shell instrument `quality/landing-counters.sh:8` (a shell
`export`), the older `quality/counters/*.py` instruments
(`quality/counters/c3-r56-used-by.py:95`, `quality/counters/c1-r56-autoreload-entry.py:67`),
`tools/mado-receipt-citecheck.py`, and every file that mentions git without an object-read
verb. Those constructions are dominant at runtime and invisible to this census — a declared
population boundary, not a claim that they are unguarded. The r67 wider lexical reader set stays
outside this census; the population regex is frozen in the counter.

## 5. What the green line does not prove

- It does not prove the guard *takes effect*: the value is not interpreted, and
  `GIT_NO_REPLACE_OBJECTS=0` also disables replacement. It proves the environment that
  reaches the launch carries the key.
- It does not authenticate objects, and it does not repair a repository whose objects
  were already rewritten; it refuses the documented replacement channel (S436:20-24).
- It is a syntactic approximation: one module, one hop, no alias (`e = env`), no
  attribute-carried env, no container or `**{KEY: "1"}` splat flow, no cross-module
  producer, no path-sensitivity beyond a literal-false branch, and a name bound to an
  argv counts globally rather than per scope.
- It scores committed source text at a revision; a dead but *reachable* guard still
  counts, and a guard wired into a call that never runs at runtime still counts.
- It says nothing about the four unread `quality/` scripts or about other lanes'
  instruments, which are read only by the round's connector seat.

## Evidence rows

One row per proposition this entry turns on. S438 rows pin the fetched bytes at tag
`v2.56.0` (sha256 `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`,
47005 B, 1212 lines); held rows pin the earlier entries' bytes as they were fetched
there, not re-fetched here.

| id | claim the row grounds | source | locator |
|---|---|---|---|
| K01 | The top-level `git` invocation takes `--no-replace-objects`, so the switch exists at the command layer. | S438 | git.adoc:14 |
| K02 | The option "Do not use replacement refs to replace Git objects". | S438 | git.adoc:179 |
| K03 | The option "is equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable with any value" — the documented identity of flag and environment. | S438 | git.adoc:180 |
| K04 | The variable acts on Git when it is "setting and exporting" — the environment the child receives, not a string in the source. | S438 | git.adoc:928 |
| K05 | Replacement refs are used "by default by all Git commands" except reachability traversal, which is why a guard is needed at all. | S436 | git-replace.adoc:20 |
| K06 | A replacement ref is named for the replaced object and redirects reads of it. | S436 | git-replace.adoc:22 |
| K07 | The one documented `cat-file` mode that bypasses replacement is `--batch-all-objects`; the census therefore guards the ordinary read forms. | S437 | git-cat-file.adoc:198 |
| K08 | The object-read verb family is the `cat-file` contents/type/size surface the reader rule keys on. | S437 | git-cat-file.adoc:21 |

## 6. Recheck and provenance

- Fetch: `curl -sSfL -o git.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`
  (2026-11-03) → sha256 `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`,
  47005 bytes, 1212 lines; tag `v2.56.0`; host `git version 2.56.0`.
- Line numbers were checked against those bytes; the `--no-replace-objects` block is
  L178-182 and the environment entry L927-929.
- Control set: `.ufo/waves/round-69/controls/c2-controls-r69.json`, sha256
  `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`, 11 cases.
- Before/after: the round-68 rule scores `controls=7/11` on the same frozen set and the
  round-69 rule `11/11`; both lines are in `.ufo/waves/round-69/control-baseline-r69.txt`
  and re-measured at the measured content in `measurement-c2-r69.txt`.
- The guard-shape table in §4 was derived from the census's own per-file `MADO_R69_READER`
  lines at the measured content, not from reading the files by hand a second time.
- Cadence: 90d. Re-fetch and re-hash the adoc; re-check the population regex and the
  control JSON if either moves; re-run the classification cases when a gate's env
  construction changes.
