# ScoutJjHelpEmpirical — jj 0.45.1 help/version invocations snapshot nothing (0 ops, dirty working copy preserved); only `jj git push --dry-run` adds a snapshot op, and `jj describe -m --help` errors before touching the repo

Empirical check requested by round 20 (E4 vcs_write help/dry-run carve-out). All work in throwaway `/tmp` repos; no jj/git write of any kind in the lane.

Tool identity: `/home/vgpnk/.local/bin/jj`, `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`, binary sha256
`cd5efc3eb281d606bf9b5523167f79661da0f8c76a5aa32d61c07c7a351b6b44`. `git version 2.56.0`. Measured 2026-10-20T19:45Z.

## Method (scout2, clean run)

`/tmp/jjhelp-r20-scout2`: `jj git init .`, `printf 'base\n' > f.txt`, `jj commit -m base` → 4 ops.

Op counter (exactly the contract counter):

```
jj op log --ignore-working-copy --no-graph -T 'id.short() ++ "\n"' | wc -l
```

Before **every** listed form I appended a fresh line to the tracked file (`f.txt`), so a working-copy snapshot was always pending; delta = ops(after) − ops(before). `--ignore-working-copy` on the counter itself keeps the measurement from snapshotting.

## Table (form → ops before/after → snapshot)

| form | exit | ops before→after | delta | snapshot |
|---|---|---|---|---|
| `jj st --help` | 0 | 4→4 | 0 | no |
| `jj st -h` | 0 | 4→4 | 0 | no |
| `jj describe -h` | 0 | 4→4 | 0 | no |
| `jj help log` | 0 | 4→4 | 0 | no |
| `jj log --help` | 0 | 4→4 | 0 | no |
| `jj git push --help` | 0 | 4→4 | 0 | no |
| `jj --version` | 0 | 4→4 | 0 | no |
| `jj --help` | 0 | 4→4 | 0 | no |
| `jj help git push` | 0 | 4→4 | 0 | no |
| `jj help -h` | 0 | 7→7 | 0 | no |
| `jj help` (bare) | 0 | 7→7 | 0 | no |
| **`jj st` (positive control)** | 0 | 4→5 | **1** | **YES** |
| **`jj log -n 1` (positive control)** | 0 | 5→6 | **1** | **YES** |
| **`jj git push --dry-run`** | 0 | 6→7 | **1** | **YES** |

The positive-control op's own description is `snapshot working copy` (read from `jj op log -T 'description.first_line()'`), i.e. the delta is exactly the working-copy snapshot, not a commit/describe op.

The zero-op result is not an artefact of "nothing pending": each form had one freshly appended line. In the first run (`/tmp/jjhelp-r20-scout`), six zero-op forms followed by the `jj st` control produced a snapshot whose raw diff (`jj diff --ignore-working-copy`) shows exactly the six pending appends plus the control's own line:

```
Modified regular file tracked.txt:
   1    1: base
        2: mod1
        ...
        8: mod7
```

In the same repo, four more zero-op probes (`jj -V`, `jj log --bogus`, `jj boguscmd`, `jj describe -m --help`) left `mod8 mod9 mod21 mod22` pending; the next ordinary command (`jj file show -r @`, no `--ignore-working-copy`) snapshotted them and `@` then contained `base mod1..mod9 mod21 mod22` — the physical file had 13 lines and the recorded tree 12, so the counter and the snapshot indicator agree.

## Error/help dispatch paths (scout1)

| form | exit | delta | observation |
|---|---|---|---|
| `jj st --help` outside any repo (`/tmp/jjhelp-r20-norepo`) | 0 | n/a | help renders; no "no jj repo" error |
| `jj log --help` outside any repo | 0 | n/a | same |
| `jj --version` outside any repo | 0 | n/a | prints version string |
| `jj st` outside any repo | 1 | n/a | `Error: There is no jj repo in "."` |
| `jj log --bogus` (dirty WC) | 2 | 0 | `error: unexpected argument '--bogus' found`; no snapshot |
| `jj boguscmd` (dirty WC) | 2 | 0 | `error: unrecognized subcommand 'boguscmd'`; no snapshot |

So help/version/parse-error paths all terminate in clap before repo open: no snapshot even with pending changes.

## Divergence worth recording for E4: `-m --help` is git-only

E4 says a `-m --help` option value still writes. Measured:

| form | exit | ops delta | effect |
|---|---|---|---|
| `jj describe -m --help` | 2 | 0 | `error: a value is required for '--message <MESSAGE>' but none was supplied`; nothing written |
| `jj describe -m "--help"` | 2 | 0 | same (shell quoting is gone before jj parses; still rejected) |
| `jj describe -m -h` / `jj describe -m "-h"` | 2 | 0 | same |
| `jj log -r --help` | 2 | 0 | `a value is required for '--revision <REVSETS>'` |
| `jj describe -m=--help` | 0 | 2 | description becomes `--help` (snapshot + describe) |
| `jj describe --message=--help` | 0 | 1 | taken as a value; "Nothing changed." (already `--help`) |
| `jj describe -m=-h` | 0 | 2 | description becomes `-h` |
| git `commit -m --help` (`/tmp/jjhelp-r20-gitprobe`) | 0 | n/a | real commit `fefca2347be9996d75ee109dc2791ca446411da1` with subject `--help` |

Reading: jj 0.45.1 refuses a hyphen-leading value in the space-separated position (clap default, no `allow_hyphen_values`), so `jj ... -m --help` is a no-op error, whereas git 2.56.0 consumes `--help` as the message and commits. A text-level scanner cannot see quoting, so the conservative "write" reading of `-m --help` is required for git; applying the same clause to jj over-reports an erroring no-op (a precision loss, not a false negative). The only jj forms that actually write a `--help` message are `-m=--help` / `--message=--help` — the E4 text does not cover those, and a scanner that treats any `--help` token as a help request would classify them as non-writes (a false negative for jj).

Also note `jj git push --dry-run` in a remote-less repo: exit 0, stderr `Warning: No bookmarks/tags found in the default push revset: ... Nothing changed.`, **one snapshot op**. It performs no VCS write (no remote, no bookmark update) but it does mutate the local op store by snapshotting the working copy. Whether E4 calls that a write is a definitional choice; the observable fact is the +1 op. A dry run followed by a real write in the same text is not contradicted by this: the real `jj git push` on the same repo likewise only snapshotted (+1) because there was nothing to push.

## Facts / inference

Observed: all 11 help/version forms above (exit 0, 0 ops, pending change preserved); positive controls `jj st`, `jj log -n 1` each +1 op described `snapshot working copy`; `jj git push --dry-run` +1 op; jj rejects `-m --help` / `-m -h` / `-r --help` with exit 2 and 0 ops; `-m=--help` writes; git `-m --help` commits; help renders outside a repo while `jj st` fails with "no jj repo".

[INFERENCE] Op-count delta is a sound snapshot indicator here because the throwaway repos had no background jj processes, the counter runs with `--ignore-working-copy`, and every positive delta's last op was literally `snapshot working copy`; no other op-producing activity existed in these repos.

[INFERENCE] `jj help <sub>` and `jj <sub> --help` share the same clap help path (identical 0-op/exit-0 behaviour and the same stdout help body as the corresponding `-h` forms).

## Limits

- Did not test `jj git push --dry-run` against a configured remote or with bookmarks/colocated counterparts; the no-remote path only proves the snapshot, not remote-write semantics.
- Did not test `git commit --dry-run`, `git add -n`, `git push -n` or `git help ...` (out of this ticket's scope; the only git probe was `-m --help`, to validate the option-value clause).
- Did not run jj in the lane checkout (prohibited); no lane, fleet, tool or corpus file was read-modified or written except this report.
- No source-code inspection of jj was performed; all claims are CLI observations at the pinned build above. Behaviour of other jj versions is [UNK].

## Installs

none
