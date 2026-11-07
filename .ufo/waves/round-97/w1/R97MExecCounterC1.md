# R97MExecCounterC1 - w1 report (round 97, seat C1 counter)

Seat: executor, counter draft for PRED-C1-r97-v1. Artifact:
`.ufo/waves/round-97/build/c1-r97-filetype.py`
sha256 `6536b0aea7e6d5891488b3ebe8fb6261f23bed498f4b240d99ad9b8107a1c872` (754 lines, final bytes).

## Deliverable evidence (as the seat demands)

- CLI: exactly the declared 21 flags (`--repo --rev --base-rev --cases --expect-cases-sha256
  --mutants --expect-mutants-sha256 --genseed --expect-genseed-sha256 --host-list
  --expect-host-list-sha256 --host-db --expect-host-db-sha256 --expect-tool-sha256
  --expect-mimeglob-sha256 --expect-mimesniff-sha256 --expect-mimetext-sha256 --expect-gio-sha256
  --forgery --expect-forgery-sha256 --scratch-root`), all required, plus `-h/--help` (rc 0, prints the
  predicate reference). `--selftest` is deliberately NOT a counter mode (that is C2's business).
- Syntax: `ast.parse` and `py_compile` both clean; no `__pycache__` left in build/.
- `--help`: printed (evidence in the transcript), rc 0.
- Dry run 1 (the declaration's counting command with placeholder pins against the current lane):
  `MADO_FILETYPE_COUNT: SETUP_ERROR pred=PRED-C1-r97-v1 id=setup-cases-missing .ufo/waves/round-97/controls/filetype-cases-r97-frozen.json missing`, rc 2 - stops at the first missing input.
- Dry run 2 (six synthetic control inputs in scratch with their true sha pins): passes existence and
  sha checks, prints `base: tools/mado-filetype.py absent at base-rev e6152b58... (declared before
  0/0)`, then `id=setup-tool-missing-at-rev tools/mado-filetype.py absent at e6152b58...`, rc 2.
  Both runs cleaned their scratch temps (work/secret removed in `finally`).
- Functional smoke (scratch, draft candidate e68150b5... + worktree siblings): static_findings=none;
  three oracle-labelled cases (hermetic text-db follow, nofollow symlinks, host-db `/usr/share` cache
  with chardev) scored ok/ok/ok under the audit launcher with 0 audit denials; mutant mechanics
  verified (attr-token flip -> all `wrong` = kill; broken identifier -> all `crash` =
  crashed_not_killed); name-only shim scored wrong on all three (control behind); naive model 2/3;
  candidate `--selftest` green under the launcher (`checks=25 failed=0`, rc 0, 0 denials).

## Behaviour implemented (seat letters a-i)

(a) materialises `tools/mado-filetype.py` + the three siblings from `git show <rev>:<path>` into
scratch only; sha-pins all four + `/usr/bin/gio` (`tool_pin=ok sibling_pins=ok,ok,ok`); base-rev must
NOT contain the tool (`setup-base-has-tool` grounds the 0/0 before-state); prints
`pacman -Q glib2 shared-mime-info xdg-utils file`.
(b) builds each frozen case root in scratch from base64 `files` (rejects `..`, absolute members,
undecodable b64); materialises dirs/symlinks (`{root}` substitution in targets)/fifos/AF_UNIX
sockets/unreadable(mode 0); chardev/blkdev are declared absolute host paths, lstat-verified, never
created; envelope + census validation (15 classes in order, >=8/class, >=120 cases).
(c) every candidate run goes through the generated audit launcher with `PATH=<empty dir>`, audit hook
denying opens outside the allow set, process spawn (except `ldconfig` for libc discovery), connect,
and non-libc dlopen; one `spec_from_file_location` per sibling with declared attribute lists; prints
`audit_denials=<n>` (must be 0 on candidate runs).
(d) per-path scoring: type/attr/mode tokens, esc-reversible `path=` spelling, per-case
`MADO_FILETYPE_DIRS: db=` value (derived per case: hermetic roots from the declared files, declared
host roots from the live filesystem), exit code exactly 0 or exactly-2-iff-ERROR; lines matched per
kind in path order (the candidate prints ERROR lines during the stat loop and the rest after it);
missing/extra line = wrong, non-{0,2} rc = crash.
(e) mutants: find/replace applied to the pinned candidate bytes (whole-file-unique anchor, unique
across mutants, SETUP_ERROR otherwise); kill = >=1 case wrong; crash = `crashed_not_killed`;
`killed == mutants` and `class_kills == 15/15` (case-class credit, r96 semantics).
(f) fresh leg: frozen generator run inside the counter (`--seed HEX --dir D --out F --count 140`,
PATH starting /usr/bin so its gio is the pinned binary), JSONL stdout validated (contract 2 + fresh
rules: no ERROR labels, >=120 cases), tool scored against same-run labels; seed drawn at measurement
(os.urandom hex) or the `MADO_R97_FRESH_SEED` env override, printed `fresh_seed=...`.
(g) host leg: fail-closed credential guard first (below), then the frozen `--host-db` manifest (mode
text: copy+verify named files into scratch, no loadable cache in the copy; mode cache: declared source
dir read-only, its mime.cache must be loadable), then every frozen host path scored by live gio vs
candidate; `host=<ok>/<total> host_paths=<n>`, `>=1500`.
(h) controls: `control_nameonly=<n>/<cases>` from the generated name-only shim (pinned r94 guess for
every path, scored through the same parser, must be < cases); `control_fastproxy` (candidate run with
--fast on every case, informational); naive extension table with the six fixed inode names
(in-counter, must be < cases); memoriser keyed by case fingerprint with sentinel on miss
(`memoriser_fresh == 0` required); forgery run under the launcher, rejected iff audit denies or the
static conjunct flags it.
(i) counter `--help` only; the candidate's `--selftest` leg requires
`MADO_FILETYPE_SELFTEST: checks=N failed=0`, N>=20, rc 0. Verdict line
`MADO_FILETYPE_COUNT: TARGET_MET|TARGET_MISSED pred=PRED-C1-r97-v1 ...` with all atoms; rc 0/1/2.

## Findings and decisions this wave

1. Host-db cases (MutC1's cross-check, confirmed by my own smoke): the frozen set declares absolute
host roots (`XDG_DATA_DIRS=/usr/share`) on 14 cases. My first draft rejected those envs and derived
db=none from the files map alone - both wrong. Now: env segments may be `{root}/...` templates or
absolute host roots (credential-guarded), and db mode for host roots is derived from the live
filesystem; the roots are admitted read-only to the audit allow so the candidate opens exactly what
gio labels against. Measured end-to-end green.
2. AF_UNIX carve-out (measured on the candidate draft): the candidate imports `errno` (EPERM modelling)
and `socket` (its `--selftest` builds an AF_UNIX fixture for the inode/socket branch). The declared
import allowlist admits both; the audit hook admits `socket.__new__` for AF_UNIX only and denies
connect/connect_ex and every network family. The frozen predicate sentence stays verbatim in the
docstring; the carve-out is documented as a counter note to keep with the receipt.
3. Fresh generator interface: adopted R97MExecHostC1's frozen CLI/JSONL contract (they announced it
mid-wave); no separate re-label leg - labels are same-binary same-run, the gio sha is pinned before
the generator runs. My counter-side requirements (labels as one-element lists, pure JSONL stdout,
PATH pinning) were messaged to the seat.
4. Credential guard (L1 r56 order): host-list entries AND case-declared host roots are refused with
`MADO_FILETYPE_COUNT: SETUP_ERROR pred=PRED-C1-r97-v1 credential-shaped host path: <path>
credential_guard=<n>` (exit 2) before any host byte is read; `credential_guard=0` printed on the
green path. The current host-list DRAFT contains credential-shaped paths (per the L1) - the guard
will refuse it at measurement until the L1 freezes a scrubbed list. That is the intended fail-closed
behaviour, not a counter defect.
5. Mutant semantics (R97MMutC1 coordination): kill = parsed wrong answer (type/attr/mode/dirs/
path-spelling/rc) or a missing line; crash is never a kill. Escaping-scheme mutants (esc->raw) stay
invisible on all-ASCII paths; I recommended freezing >=1 case whose scored path carries a
non-printable/backslash/non-ASCII byte. Mutants schema frozen with the seat: no equivalents list - a
frozen non-killer fails the wave.
6. Lane-state observation (L1 domain): worktree siblings (mimeglob `65f80a6c...`, mimesniff
`4ef019c6...`, mimetext `d5f174fc...`) differ from the base-rev blobs (`fa91abc.../0ac29fc.../
4a764d0...`) - the lane worktree is jj-materialised ahead of what `git show <base>:...` returns.
The counter pins bytes at `--rev` via `git show`; the L1 must freeze a measured rev whose git objects
hold the bytes actually intended (a jj-colocated commit).
7. Model risk flagged to the tool seat (unconfirmed there): readerr cases require the sniff-open
EPERM failure to keep the name-only answer INSIDE `answer()`; an OSError escaping to the main loop
would print `ERROR stat` and mis-score those cases (glocalfileinfo.c:1366-1378).

## Tools installed

None. Nothing beyond stdlib + in-repo tooling was needed; the pacman pause was respected (no
transactions, no sudo, no host service touched).

## Write scope and cleanup

Wrote only: `.ufo/waves/round-97/build/c1-r97-filetype.py` (my seat file) and this report. Scratch
`/fast/scratch/hyaku/mado-r97/R97MExecCounterC1` (probe, smoke, synth, dry-run trees) deleted before
yield. No lane/corpus/quality/git-index/jj writes; no commits; read-only git only (`rev-parse`,
`ls-tree`, `cat-file`, `show`, `status`).

## Risks / what the L1 should watch at measurement

- First run will land `credential-shaped host path: ...` if the host list keeps its current draft
  content (scrub before freeze, keep the guard).
- SETUP order is: pin formats -> input existence -> scratch -> input shas -> rev checks -> git
  materialisation -> gio -> cases envelope/census -> mutant anchors -> host-list parse + guard ->
  host-db manifest. Stable `id=setup-*` tokens on every line.
- If the freeze moves any candidate import or sibling attribute outside the declared lists, the
  verdict is `static_structural=FAIL` (TARGET_MISSED), not SETUP - coordinate before freezing
  (messaging done).
