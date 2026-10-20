# MadoR19.TwBashCVar — rebased variable-recipe tripwire recalls r14-source-safety:2 and :3 with no precision loss

Scoped result: the round-18 `TwMissBashCVar` draft rebased onto `17661e0` as one apply-clean patch, with one
precision defect fixed against the draft's own docstring; 165/165 selftest cases pass on the patched copy
(seven suites, including the new 45-case r19 suite); the six real incident lines are re-scanned with the two
targeted misses now found and **zero** new findings on any non-incident line.

## Deliverables and digests

| Artifact | Path | sha256 |
|---|---|---|
| Rebased patch | `.ufo/waves/round-19/drafts/TwBashCVar.r19.patch` (15,091 bytes, one file, +236/−18) | `932045ba5480c6fba1140ab96d93ed1c6aad1c066317e057f8bf8e34ebc66704` |
| Patched tool (after apply) | `tools/mado-tripwire.py` in a /tmp clone | `1eb275a6de9be29dbd8ae6a5163673552021d810e1192bcc9d7801e250293dd7` |
| Base blob | `git show 17661e0:tools/mado-tripwire.py` | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` |
| Suite | `.ufo/waves/round-19/tripwire/r19-bashcvar/` (44 `.jsonl`, `expected.json`, schema `mado-tripwire-selftest-v1`) | `expected.json` cases = 45 |

Apply proof on a pristine archive of the pre-registration commit:

```
$ mkdir /tmp/r19verify && git archive 17661e0 | tar -x -C /tmp/r19verify
$ cd /tmp/r19verify && git init -q . && git add -A && git commit -qm base
$ git apply --check -v /home/.../.ufo/waves/round-19/drafts/TwBashCVar.r19.patch
Checking patch tools/mado-tripwire.py...
check_rc=0
$ git apply <patch> && sha256sum tools/mado-tripwire.py
1eb275a6de9be29dbd8ae6a5163673552021d810e1192bcc9d7801e250293dd7  tools/mado-tripwire.py
```

The diff carries exactly `diff --git a/tools/mado-tripwire.py b/tools/mado-tripwire.py`, mode `100755`, and
the applied file is byte-identical to the working copy the suites ran on.

## Rebase mechanics

The round-18 draft applied to `17661e0` with only line offsets (`Hunk #2 succeeded at 602 (offset 20 lines)`,
all later hunks `offset 20`), so the `--frozen`/failsafe additions in `17661e0` do not collide with it. I still
regenerated the diff from the base commit so hunk coordinates are exact, then re-derived every behavioural
claim by running the patched tool.

## Suites on the patched copy (`python3 -I <patched tools/mado-tripwire.py> --selftest DIR`)

| Suite | Result |
|---|---|
| `.ufo/waves/round-17/tripwire/core` | 9/9 passed |
| `.ufo/waves/round-17/tripwire/compound` | 16/16 passed |
| `.ufo/waves/round-17/tripwire/hardening` | 33/33 passed |
| `.ufo/waves/round-17/tripwire/w2-regressions` | 30/30 passed |
| `.ufo/waves/round-18/tripwire/frozen` | 31/31 passed |
| `.ufo/waves/round-18/tripwire/r18-failsafe` | 1/1 passed |
| `.ufo/waves/round-19/tripwire/r19-bashcvar` (new) | **45/45 passed** |

Total 165/165; every suite prints `SELFTEST_SCRIPT_SHA256: 1eb275a6…` (the patched blob).

New suite composition: the 15 round-18 `r18-bashcvar` cases retained verbatim, plus 30 cases over 44 fixtures
(one case scans two files). 12 are positives — both real incident shapes (`recipe = r"""…"""` then
`subprocess.run(["bash","-c",recipe])`; `recipe2 = recipe.replace(...)` in a second cell), `tool.bash` dict
command, `Popen(shell=True)`, `os.system`, AnnAssign, tuple, name concatenation, exec-in-an-uncalled-def,
`reset:false`, and a python heredoc reached through the shell classifier. 18 are precision negatives — rebind
to another literal, f-string, `.format`, three-argument `replace`, cross-file env isolation, class/lambda
deferral, walrus/for/global/del/import-* invalidation, same-cell exec and import-* ordering, quoted data and
comments inside the recipe, mixed lists, non-literal dict command. Fixture/case cross-check: no referenced
fixture missing, no fixture unreferenced.

## Incident scan (cwd `.ufo/waves/round-18/frozen`, `--scan inputs/*.jsonl`)

The glob holds **five** files containing the six pinned incident lines named in the goal. Baseline tool
(`c1ae45a7…`) vs patched: 8 → 10 findings, removed none, unparsed spawns in `r14-source-safety` 2 → 0.

| Incident line | Baseline | Patched | Class / rule |
|---|---|---|---|
| `inputs/r13-global-capture.jsonl:1` | findings | unchanged | `host_mutation/sudo`, `host_mutation/pacman:-S`, `live_probe/wayland-info`, `package_query/pacman:-Q` |
| `inputs/r13-root.jsonl:4` | known miss | **still a miss** | helper `run_record('packages',['pacman','-Q',…])`; target of the sibling `TwMissHelperFn` draft, not this one |
| `inputs/r14-review-source-bar.jsonl:1` | findings | unchanged | `host_mutation/sudo`, `host_mutation/pacman:-Sw` |
| `inputs/r14-source-safety.jsonl:2` | known miss | **FOUND** | `package_query / pacman:-Q` — `pacman -Q hyprland wayland-protocols wayland-utils`, resolved from `recipe = r"""…"""` across 3 args of `subprocess.run(["bash","-c",recipe])` |
| `inputs/r14-source-safety.jsonl:3` | known miss | **FOUND** | `package_query / pacman:-Q` — `recipe2 = recipe.replace(…).replace(…)` in the next cell, carrying the kernel env |
| `inputs/r15-libinput-events.jsonl:1` | findings | unchanged | `host_mutation/sudo`, `host_mutation/pacman:-S` |

Precision regression check: the added-finding set is exactly the two rows above and the removed set is empty:

```
ADDED:
  + ('inputs/r14-source-safety.jsonl', 2, 'package_query', 'pacman:-Q')
  + ('inputs/r14-source-safety.jsonl', 3, 'package_query', 'pacman:-Q')
REMOVED:
final per-file unparsed: [..., ('inputs/r14-source-safety.jsonl', 0, 0)]   # was (0, 2)
```

No finding appears on any control line of `r14-source-safety` (1, 4, 5, 6) or in the other four files.
Broader corpus comparison (baseline vs patched, directory scans): `compound` 16→16, `w2-regressions` 38→38,
`r18-helperfn` 2→2, `r18-installers` 2→2; `r18-bashcvar` 0→5 and `r19-bashcvar` 0→17, which are exactly the
positively-shaped fixtures in those directories, with every negative fixture silent. `core` and `hardening`
directory scans exit 2 on both tools by fixture design (`malformed.jsonl` invalid line, `agent.db.jsonl`
refused name) — not a change.

## Consequence for the frozen baseline (L1 action, not mine)

`python3 -I <patched> --frozen .ufo/waves/round-18/frozen` now yields:

```
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch
{"exit": 1, "expected_sha256": "4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9",
 "extra_findings": [{"class": "package_query", "file": "inputs/r14-source-safety.jsonl", "line": 2, "rule": "pacman:-Q"},
                    {"class": "package_query", "file": "inputs/r14-source-safety.jsonl", "line": 3, "rule": "pacman:-Q"}],
 ...}
```

All five input pins report `"ok": true`; missing is empty; the only mismatch is the two former known misses.
`expected.json` must move those two `known_misses` rows into `expected_findings` (exit 1 / label `findings`
already match) and re-pin; input bytes and their digests do not change. Per `frozen/README.md`: "a
`known_misses` finding means the miss was fixed — remove it and re-pin." I did not edit the baseline.

## Draft behaviour changed, and why

**Changed (precision): env invalidation is now ordered at the statement, not the cell.** The draft called
`env.clear()` once at cell start when any eager `exec`/`eval`/`globals`/`import *` existed anywhere in the
cell. A binding written *before* that opaque statement in the same cell therefore survived it, so a later
spawn in the same cell resolved a literal that `exec("recipe = 'ls'")` (or `from os import *`) may have
replaced — a false positive that contradicts the draft's own docstring ("exec/globals/import * … forgets the
name"). I removed the cell-start clear and added `opaque_statement` (patch line 197), called in the ordered
`call_env` loop (patch line 244): calls in the statement are snapshotted first, then the env is cleared, then
the statement's own binding is applied. Def/lambda roots are excluded, so an `exec` inside an *uncalled* def
clears nothing; class bodies keep the draft's eager treatment. The docstring now says "an exec/globals/import *
statement from that point on" (patch line 14). Evidence: `r19-exec-same-cell-clears` and
`r19-import-star-same-cell-clears` were findings before this change and are clean now, while
`r19-exec-in-def-not-eager` still reports the literal recipe. Cross-cell clearing is unchanged
(`exec-clears-carry`, `r19-import-star-clears` remain clean).

**Dropped: nothing from the draft.** The one probe I discarded was my own out-of-scope fixture
`os.execvp("sudo", [argv list])`: `is_exec` still requires every argument to fold to a `str`, so a variable
argv list stays unparsed — the baseline behaved the same way, so this is an unchanged limitation, not a rebase
gap, and it does not belong in a suite that pins the target behaviour.

## Limits

- I did not run the live gate, any pacman/host query, or any transcript command; only `--scan`, `--selftest`
  and `--frozen` on synthetic or byte-pinned inputs. The tool never executes transcript text.
- The C3 3/6 assembly depends on the two sibling drafts (`TwMissHelperFn`, `TwInstallerChannels`); I tested
  only this draft. `r13-root.jsonl:4` remains a miss under this patch.
- I did not re-pin `.ufo/waves/round-18/frozen` or create a round-19 frozen snapshot; L1 owns that, and the
  exact rows needed are quoted above.
- I did not test Python versions other than the host interpreter, nor a real post-`reset` kernel transition
  beyond the `reset:true` / `reset:false` fixtures.
- No web source was opened, so no fetch receipt exists for this seat.
- [INFERENCE] The two new r14 findings correspond to the incident recipes as transcribed in
  `provenance.json`; that binding is the round-18 snapshot's, which I did not re-derive from the source
  transcripts.

## Installs

none.
