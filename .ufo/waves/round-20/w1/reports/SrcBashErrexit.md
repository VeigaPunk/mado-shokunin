# SrcBashErrexit — bash 5.3 names the exact `&&`-list exemption that let round 19's failed `mount` reach a real `hyprctl`; one A-tier row drafted

**Axes (godspeed).** (1) identity — is the quote pinned to immutable bytes; (2) locality — is the sentence a `file:line` fact; (3) explanatory sufficiency — does the sentence actually account for the round-19 script not stopping; (4) consumability — row shape plus a usable instruction for QUALITY 29 / `isolate.sh`; (5) harm — none: reads only, no lane writes, no protected command, no payload executed.

## 1. Source identity (observed)

Five objects agree byte-for-byte on `doc/bashref.texi` at tag `bash-5.3`:

| Object | Identity |
|---|---|
| savannah tag | `git ls-remote https://git.savannah.gnu.org/git/bash.git refs/tags/bash-5.3` → `b8c60bc9ca365f8261fa97900b6fa939f6ebc303 refs/tags/bash-5.3`, **no `^{}` line** (lightweight tag) |
| tag commit | shallow clone `--branch bash-5.3` HEAD = `b8c60bc9ca365f8261fa97900b6fa939f6ebc303`, authored `2025-07-03T16:15:36-04:00` |
| git blob | `git show bash-5.3:doc/bashref.texi` sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`, 415,804 B |
| cgit plain body | `.ufo/waves/round-20/fetch/SrcBashErrexit/bashref.texi`, same sha256, same size (receipt line 1) |
| GNU tarball member | `bash-5.3.tar.gz` sha256 `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`; its `doc/bashref.texi` extracts to the same sha256 (receipt line 2) |

cgit returned **502** on the first attempt, 200 for both URL forms (`?h=bash-5.3`, `?h=refs/tags/bash-5.3`) on retry, and a later re-fetch **timed out after 60 s with 0 bytes** (the stored body was left unmodified; sha256 re-verified afterwards). The accepted body's hash equals the tag blob and the tarball member, so the flaky transport introduces no identity ambiguity. Host shell is `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)`.

## 2. The sentence (observed, verbatim)

`doc/bashref.texi` `@item -e` block `:5929-5958`. The sentence spanning `:5936-5944` (rendered; `@code{}`/`@option{}` markup stripped):

> The shell does not exit if the command that fails is part of the command list immediately following a `while` or `until` reserved word, part of the test in an `if` statement, **part of any command executed in a `&&` or `||` list except the command following the final `&&` or `||`**, any command in a pipeline but the last (subject to the state of the `pipefail` shell option), or if the command's return status is being inverted with `!`.

The load-bearing clause is `:5940-5941`; 20 words:

> part of any command executed in a && or || list except the command following the final && or ||

(That is the clause embedded in the drafted row; the full sentence is quoted above for the reader.) The man page carries the same clause at `doc/bash.1:11411`.

A second sentence is needed to explain the *loop* returning non-zero without stopping — `:5945-5947`:

> If a compound command other than a subshell returns a non-zero status because a command failed while -e was being ignored, the shell does not exit.

And the `ERR` trap inherits the identical conditions — `:4797-4808`, closing at `:4807-4808`: "These are the same conditions obeyed by the errexit (-e) option." So replacing `set -e` with `trap … ERR` would not have caught the round-19 failure either.

## 3. Why the round-19 chain did not stop the script (observed)

The pre-fix harness bytes survive in the round-19 transcript **as data** (never executed): `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19/MadoR19.SentinelGatePath.jsonl:33`, heredoc body 441 B sha256 `b09e07723c09a65d14f1c81c51fc58177afae214794e804e63dc73f92357e75f`:

```bash
#!/bin/bash
set -e
for p in /usr/bin/hyprctl ... /home/vgpnk/.local/bin/jj; do
  [ -e "$p" ] && mount --bind /tmp/sgp/tripwire.sh "$p" && echo "armed $p"
done
set +e
"$@"
```

Binding the manual to it:

1. `mount` is **not** the command following the final `&&` (`echo` is), so its EPERM failure falls under `:5940-5941` and `set -e` never fires — the whole arm silently no-ops.
2. The `for` compound then returns non-zero, and `:5945-5947` says the shell still does not exit.
3. `set +e` on the next line disables errexit for `"$@"` explicitly — but the setup was already non-fatal before it ran. The payload (`/usr/bin/hyprctl probe`) therefore executed against the real binary (corroborating `.ufo/waves/round-19/w2/reports/SentinelGatePath.md:77`, and the host-pause breach at `corpus/lessons/round-19-verifier-spotcheck.md:124` and R19-V4 at `:152`).

The live run output is also retained, as data, at transcript `:35` (toolResult of the `:33` call): **exactly 16** `mount: <path>: must be superuser to use mount.` lines — one per armed target, none succeeded — followed by `unknown request` and `rc=0`. That fixes the causal chain as observed: all 16 bind mounts failed EPERM, the `&&` chain swallowed each failure, `set -e` never fired, and the wrapped `/usr/bin/hyprctl probe` executed against the real binary.

The fixed script now on disk, `/tmp/sgp/inns.sh` (742 B, sha256 `59b234934b266861ba89f764d8f37ca5e1911cbbf6f61ce53867e8d3e107ac80`), is **byte-identical** to the replacement written at transcript `:36` (740 B heredoc + newline) and replaces the chain with `[ -e "$p" ] || continue`, `mount … || { echo "ARM FAILED…"; exit 99; }`, `cmp -s … || { echo "ARM NOT VISIBLE…"; exit 98; }`, `exec unshare … "$@"`.

## 4. Canary matrix (observed; bash 5.3.20, `/tmp/mado-errexit-canary`, `cp` as the failing-command stand-in for `mount`)

Every cell is `bash -c "set -e; <shape>"`; "payload" is a trailing `echo PAYLOAD`.

| shape | rc | payload ran |
|---|---|---|
| exact r19 loop (`[ -e "$p" ] && cp stub "$p" && echo armed` in a `for`, then `set +e`, payload) | 0 | **yes** |
| `for …; do [ -e "$p" ] && false; done; payload` (no `set +e`) | 0 | **yes** |
| `for …; do true && cp stub <absent-dir>/x; done; payload` (failing command is final in the list) | 1 | no |
| `f(){ [ -e X ] && false; }; f; payload` | 1 | no |
| `{ [ -e X ] && false; }; payload` | 0 | **yes** |
| `( [ -e X ] && false ); payload` | 1 | no |
| `if [ -e X ] && false; then :; fi; payload` | 0 | **yes** |
| `[ -e X ] && false; payload` (top level) | 0 | **yes** |

Reading: the exemption attaches to **which command failed**, not to where the list sits. A failing test at the head of a chain never trips `-e`, even when the list's own status is 1. `{ …; }` and `for` bodies survive (manual `:5945-5947`); a subshell aborts ("compound command **other than a subshell**", `:5945`). The bare function call aborting is consistent with a function call being a simple command whose own non-zero status is not exempt — the manual does not spell that asymmetry out, so [INFERENCE] for the *documented* reason, observed for the *behaviour*.

## 5. Drafted row (L1 assigns the id; 11-column SOURCES shape)

| S1xx-pending | GNU Bash 5.3 Reference Manual — §The Set Builtin, `-e` (`doc/bashref.texi`) | docs | A | exact `set -e` (errexit) exception set for the 5.3 release: which failing commands do not terminate a non-interactive shell | `doc/bashref.texi:5929-5958` @ tag `bash-5.3` commit `b8c60bc9ca365f8261fa97900b6fa939f6ebc303` (415,804 B sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`; identical to `doc/bashref.texi` inside the official `bash-5.3.tar.gz`, sha256 `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`); quote `bashref.texi:5940-5941`: "part of any command executed in a && or &#124;&#124; list except the command following the final && or &#124;&#124;" | a failing command that is not the last element of an `&&` or `&#124;&#124;` list is exempt from `-e`, and a compound command (`for`, `{ …; }`, `if`) whose non-zero status comes from such an exempt command does not stop the shell (`:5945-5947`); the `ERR` trap obeys the same conditions (`:4797-4808`) — so `[ -e ] && mount && echo` can arm nothing and still run its payload; each setup step needs an explicit exit-on-failure guard, not errexit | mined | 2026-10-20 | on-release | `.ufo/waves/round-20/w1/reports/SrcBashErrexit.md` (consumer: QUALITY 29 / `.ufo/waves/round-20/isolate.sh`) |

`&#124;` is the ASCII vertical bar. The registry is awk-split on `|` (11 columns => `NF=13`), so a literal bar inside a cell raises E01; on merge, keep the entity encoded — decoding it to a literal bar is exactly what raises E01; Markdown renderers display the entity as the bar.

Second candidate row, **not** drafted because it teaches nothing beyond the first: `doc/bash.1:11388-11412` is the same clause in man-page form (would be a duplicate-URL-class row).

## 6. Operational consequence for QUALITY 29 / `isolate.sh`

The IsolationHarness item already says "use explicit `|| exit 125` per step; do not rely on `set -e` inside && lists". The manual gives the precise reason and the boundary:

- a bare `A && B && C` arm sequence is **not** fail-closed under `set -e`; the failing `A`/`B` is exempt;
- the surviving `inns.sh` fix style (`[ -e ] || continue` then `mount … || { …; exit 99; }`, `cmp … || { …; exit 98; }`) is fail-closed — but `[ -e "$p" ] || continue` only skips a missing target, it does not report one; if a missing target must also abort, use `[ -e "$p" ] || { echo "MISSING"; exit 125; }`;
- an `ERR` trap is not a substitute (`:4807-4808`);
- `( … )` subshells *do* abort, `{ …; }` groups and `for` bodies *do not* — so wrapping setup in a group/loop is the dangerous direction.

## 7. Confidence

- **Observed:** all hashes, sizes, line numbers and quotes above; the pre-fix and fixed harness bytes and their shas; the canary matrix outputs on host bash 5.3.20.
- **[INFERENCE]:** only the documented-vs-observed reading of the bare-function-call asymmetry (the manual names *compound command*, and a function call is a simple command). The live failure mode itself is observed (16 `must be superuser` lines + `unknown request` at transcript `:35`).
- **[UNK]:** behaviour of bash 5.0–5.2 on the same matrix (not fetched); whether mount EPERM on those targets is stable across kernels/userns backends (the failing run used `--map-current-user`, the fixed one `--map-root-user`); whether L1 renumbers the row id or changes the tier.

## Limits

- Read only the 5.3 release manual/tarball; no cross-version comparison (5.2, 4.4) and no `bash --posix` / `inherit_errexit` variant testing beyond what is quoted.
- The live re-run of `inns.sh` was not reproduced; the pre-fix bytes are quoted from a session transcript treated as data, and the on-disk `/tmp/sgp/inns.sh` is the **fixed** file (sha-pinned above), not the failing one.
- cgit served one 502, then 200, then a 60 s timeout on a third attempt; only the 200 body is stored and its hash matches the tag blob and tarball member, so no rotating-HTML identity problem remains, but cgit's availability and the stored file's exact fetch second are not independently asserted (receipt `note` states the bound).
- The official `bash-5.3.tar.gz` body was not stored under the fetch dir (11,355,854 B > 1 MiB); its sha256 and its member's sha256 are recorded in the receipt, and the archive remains at `/tmp/bash-5.3.tar.gz` only.
- Shallow clone and all scratch live under `/tmp` (`/tmp/bashgit`, `/tmp/bash-5.3`, `/tmp/mado-errexit-canary`); no git/jj write occurred in the lane, no protected command ran, no fixture or transcript content was executed.

## Installs

none.
