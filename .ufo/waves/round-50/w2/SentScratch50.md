# SentScratch50 — w2 FALSIFY: TMPDIR/--work refusal surface of the round-50 instruments

Date 2026-10-27 (hyaku run 10, attempt 2), wave w2, lane `mado-shokunin`, attacked tip
`b4a79843cc2545bbe800db9322e58f6e00436629` (data `906178b6`, freeze `470bfd77`).
Role: sentinel/leaf, probe-only. No tracked file touched; all mutation in
`/fast/scratch/hyaku/mado-r50/SentScratch50` (deleted at exit).

## Target

Every committed round-50 instrument honours `TMPDIR`/`--work` and refuses `/tmp`, `/var/tmp`,
`/dev/shm`, home and inside-repo scratch roots; no committed tool hardcodes `/tmp` for >50 MB writes.

## Verdict

**TARGET MISSED on 4 of 5 instruments and on 2 of 5 refusal dimensions**, with the sharpest hole in
the evidence-privacy gate itself. The two counters still score their predicates correctly (both read
`TARGET_MET` at the attacked tip when run with a legal scratch root), so this is not a counter-bytes
defect: it is a *containment* defect in the instruments a seat runs by hand.

| # | sev | instrument | missing refusal | proved by |
|---|---|---|---|---|
| F1 | **HIGH** | `quality/check-session-material.py` | all five: no `--work` at all, no `TMPDIR` refusal | `csm-tmpdir-*` (rc 0, 94/94, writes there) |
| F2 | MEDIUM | `quality/check-wave-done.py` | inside-repo | `wd-work-inrepo` (rc 0, 58/58, writes there) |
| F3 | MEDIUM | `quality/counters/c2-r50-session-gate.py` | inside-repo | `c2-work-inside-repo-full` (rc 0, `TARGET_MET`, 87 fixture git repos inside the scored repo at peak) |
| F4 | MEDIUM | `quality/counters/c2-r50-session-gate.py` | home is `$HOME`-keyed → `env -u HOME` bypass | `c2-work-home-nohomevar` (rc 0, writes under home) |
| F5 | LOW-MED | `quality/counters/c1-r50-bind-entry.py` | home | `c1-tmpdir-home-fake-exists`: TMPDIR accepted, clauses a-j ran (rc 2 only later, at the live-env SETUP) |
| F6 | NOTE | `tools/mado-hostguard.py` | inside-repo is location-derived (`repo_root(__file__)`) | `hg-copy-inrepo` (out-of-repo copy: rc 0, writes in a repo) |

What holds (positive evidence, all rc 2 and nothing created): c1 refuses absent, `/tmp`,
`/var/tmp`, `/dev/shm`, inside-repo, symlinked-to-`/tmp` and `TMPDIR=.` inside the repo; c2 refuses
the three tmp roots, symlink and relative paths resolved from `/tmp`; check-wave-done refuses the
three tmp roots plus home (`$HOME` **and** passwd home) and absent; hostguard refuses all five
dimensions (its own selftest asserts them, 45/45).

## Instrument integrity at the attacked tip

`sha256sum` of the five files equals the freeze values exactly: c1 `e162d671…`, c2 `1d52a62c…`,
check-wave-done `10f4359a…`, check-session-material `ffdc9d62…`, mado-hostguard `fdaa5c2e…`.
The lane was read at `b4a79843`; every scoring run used a `git clone -q --shared` in scratch
(`rev-parse --show-toplevel` = the clone), never the lane tree.

## F1 (HIGH) — `check-session-material.py --selftest` writes wherever `TMPDIR` points

`quality/check-session-material.py:2078`:
`scratch = tempfile.mkdtemp(prefix="csm-selftest-", dir=os.environ.get("TMPDIR") or None)`.
There is no `--work` option (`:2091-2119`) and no `TMPDIR` validation anywhere in the file — `grep -n '/tmp'`
returns **zero** hits, because the fallback `or None` silently means `/tmp`.

Probes (all `python3 -I …/check-session-material.py --selftest`, `HOME`/XDG under scratch):

| probe | TMPDIR | rc | result |
|---|---|---|---|
| `csm-tmpdir-tmp` | `/tmp` | 0 | `SELFTEST: passed=94/94 failed=0`, tree created under `/tmp` |
| `csm-tmpdir-vartmp-exists` | `/var/tmp/x` | 0 | 94/94, tree created under `/var/tmp/x` |
| `csm-tmpdir-devshm-exists` | `/dev/shm/x` | 0 | 94/94, tree created under `/dev/shm/x` |
| `csm-tmpdir-inrepo-exists` | `<clone>/tmp` | 0 | 94/94, tree created **inside the scored repo** |
| `csm-tmpdir-homefake-exists` | `<home>/csm` | 0 | 94/94, tree created **under a home** |
| `csm-tmpdir-absent` | unset | 0 | 94/94 in the default temp dir (`/tmp`) |

(The first sweep used non-existent parents and produced a raw `FileNotFoundError` traceback, rc 1 —
`csm-tmpdir-vartmp`/`-devshm`/`-inrepo`/`-homefake`; re-run with the parents present, hence the
`-exists` names. Either way: no refusal, just an uncaught traceback.)

Exploit path: a seat or the L1 runs the gate's selftest from a shell that inherits `TMPDIR`, or from a
lane wrapper that sets `TMPDIR=$HOME/scratch`; the gate builds up to 24 temp git repositories at peak
(measured, probe `csm-max-git-dirs=24`; each with `git init` + commits, `:1525`, `:1776`) there. A
SIGKILL leaves them in home state — the exact hazard
round-48 M48-10 forbids — and the gate's *own* committed fixture text (e.g. `:1200`
`/fast/scratch/run/t/home/someone/xdg-terminals.list`) is then living outside any scan boundary.
Impact is bounded by size (measured peak scratch 4476 KB, probe `csm-peak-kb=4476`), not by
correctness of the gate's verdicts: the 94 cases still pass, so nothing here falsifies C2's
`selftest=94/94` receipt — it falsifies the instrument-hygiene claim around it.

Smallest remediation: give `--selftest` a `--work DIR` (or validate `TMPDIR` through the same
`TMPDIR`-refusal helper `c1-r50-bind-entry.py:1051-1066` uses) and refuse absent/`/tmp`/`/var/tmp`/
`/dev/shm`/home/inside-repo roots with exit 2 before `mkdtemp`. Also convert the uncaught
`FileNotFoundError` into that exit-2 refusal (it is currently a traceback).

## F2 (MEDIUM) — `check-wave-done.py --selftest --work <repo>/…` is accepted

`quality/check-wave-done.py:525-543` (`resolve_work`) checks `REFUSED_WORK_PREFIXES` (`:156`) and
`home_roots()` (`:535`), then `os.makedirs(real)` — there is **no** repository-root rule anywhere in
the file (`grep -n 'repo_root\|REPO_ROOT'` → no hits; `.git` appears only inside fixture code, `:561`).

Probes:
- `wd-work-inrepo` = `--selftest --work <clone>/wd` → **rc 0, `MADO_WAVE_DONE_SELFTEST: 58/58 passed`**, and
  `<clone>/wd` exists afterwards. During the run it creates fixture repositories with commits under
  that dir.
- Controls that hold: `wd-work-tmp`, `wd-work-vartmp`, `wd-work-devshm`, `wd-work-home`,
  `wd-tmpdir-tmp`, `wd-work-symlink-tmp` → rc 2 with the refusal text; `wd-tmpdir-absent` → rc 2;
  `wd-ok` → 58/58.

Exploit path: `--work` mistyped as a path inside the lane (e.g. `<lane>/.ufo/tmp`) writes committed
fixture git repos into the scored repository; under `.ufo/` the same tree is inside the default scope
of the session-material gate, so the next gate run scans fixtures the gate itself produced.

Smallest remediation: refuse a resolved `--work` under a repo root (nearest ancestor with `.git`/`.jj`
of the work path, or of `__file__`, as `tools/mado-hostguard.py:161-164` does); add a selftest case so
`SELFTEST_CHECKS` stays honest.

## F3 (MEDIUM) — `c2-r50-session-gate.py --work` inside the scored repository is accepted and used

`quality/counters/c2-r50-session-gate.py:418-436`: `forbidden_root` (`:74`, `FORBIDDEN_WORK`) and the
`$HOME` check, then `prepare_work(work)` — no comparison against the resolved `--repo`.

Probe `c2-work-inside-repo-full` (`--repo <clone> --rev b4a79843… --work <clone>/w --nonce 50117`):
rc 0, `PRED-C2-r50: selftest=94/94 names=69/69 red=42/42 green=44/44 scope=seen verdict=TARGET_MET`,
and at peak the run had created inside the scored repository:
`w/gates`, `w/home/.cache|.config|.local`, `w/tmp/csm-selftest-*`, `w/fixtures-50117` (87 fixture git
repos at peak, probe `c2-work-inside-repo-peakcount`) — the frozen receipt's green predicate is
reproducible *from inside the repo it scores*. `fixtures-50117` is removed at exit; `w/gates`,
`w/home`, `w/tmp` remain, i.e. untracked `w/` in `git -C <clone> status --porcelain`.
`--work <clone>` itself is also accepted (`c2-work-is-repo-root`, rc 2 only later at `rev-parse`),
after `prepare_work` had already created `home/`, `gates/`, `tmp/` at the repository root.

Exploit path: a seat copies the C2 command line and points `--work` at the lane (or a path that only
resolves there); fixture git repos with commits are materialised in the scored tree, and a crash leaves
them. Nothing in the counter refuses it.

Smallest remediation: after `resolve_rev`, refuse `--work` under `os.path.realpath(args.repo)` (and
under the repo that contains `__file__`) with `_die(...)` → rc 2 before `prepare_work`.

## F4 (MEDIUM) — c2's home rule is `$HOME`-keyed and therefore skippable

`quality/counters/c2-r50-session-gate.py:421-427` derives the home root from `os.environ.get("HOME")`
only. `check-wave-done.py:505-522` (`home_roots`) deliberately checks `$HOME` **and** the passwd home
for this exact reason ("A rule that reads only `$HOME` is skippable by unsetting the variable").

Probes (fake home `<scratch>/fakehome`, so nothing real is touched):
`c2-work-home` → rc 2 `--work is under the invoking home (~)`; `c2-work-home-nohomevar` (identical
argv, `HOME` unset) → rc 2 **only** at `rev-parse`, i.e. the work check passed and
`prepare_work`/`child_env` created `fakehome/c2w2/{tmp,gates,home/.cache,home/.config,home/.local}`.
Same substitution with the operator home (`env -u HOME … --work ~/x`) reaches the real home; I did not
execute that form (host guard: never write home state) — the mechanism is identical and is proven on
the fake home.

Smallest remediation: reuse `home_roots()` (env home + `pwd.getpwuid`) instead of `os.environ["HOME"]`.

## F5 (LOW-MED) — `c1-r50-bind-entry.py` has no home rule

`quality/counters/c1-r50-bind-entry.py:1051-1066` (`tmp_root`) refuses absent, `/tmp`, `/var/tmp`,
`/dev/shm` and `REPO_ROOT`, then only checks `os.path.isdir`. No home reference exists in the file
outside the scratch `HOME` it *sets for the child* (`:125`, `:1077-1078`).

Probes: `c1-tmpdir-home-fake` / `c1-tmpdir-home-real` (non-existent dir) → rc 2 but with
`TMPDIR is not a directory`, not a home refusal; `c1-tmpdir-home-fake-exists` (directory present) →
TMPDIR accepted, the run proceeded through clauses a-j to `SETUP XDG_RUNTIME_DIR required for the live
replay`. So a home `TMPDIR` is not refused — it fails or passes on unrelated conditions.

Impact: the replay scratch (`tempfile.mkdtemp(dir=tmp_root())`, `:1075`, holding the `hyprctl binds -j`
capture — 1768 B for the committed analogue `receipts/binds-live-r50.txt`) lands in home state.
Small, but the home dimension is absolute in the frozen target and in M48-10.

Smallest remediation: add the `$HOME` + passwd-home test c1 already has the pattern for elsewhere in
the lane (`check-wave-done.py:505-522`), before `isdir`.

## F6 (NOTE) — hostguard's inside-repo rule is location-derived

`tools/mado-hostguard.py:161-164` uses `repo_root(__file__)`. Installed at
`tools/mado-hostguard.py` this refuses `--work` inside the lane (`hg-work-inrepo`, rc 2 — the home
branch fires first on this host, same refusal, nothing created). But a copy outside any repo loses the
rule: probe `hg-copy-inrepo` (`python3 -I <scratch>/hg-copy.py --selftest --work <clone>/hgc`) → **rc 0,
45/45**, created `<clone>/hgc/mado-hostguard-selftest`. Documented boundary; an explicit
`--repo-root`/`--work-prefix` invocation closes it (the guard refuses `--home` under a fake home only
when it is the passwd home — `hg-work-home` rc 0 is the correct seat-sandbox behaviour, not a defect).

Also informational: c2 checks an inherited `TMPDIR` only against the three tmp roots (`:428-433`);
an inherited home/inside-repo `TMPDIR` is accepted. Not a write path — `child_env` (`:207`) overrides
`TMPDIR` to `<work>/tmp` for every child — so severity INFO.

## No `/tmp` hardcode for >50 MB writes

Full `grep -n '/tmp'` of the five files is in `grep-tmp-raw.txt`, classified hit-by-hit in
`grep-tmp-classified.txt`. Every hit is a refusal constant/docstring, a bwrap `--tmpfs /tmp` (a
deliberate empty mount for the child, `mado-hostguard.py:335`), or one of hostguard's own negative
selftest fixtures that *require* the refusal. `check-session-material.py` has no `/tmp` literal: its
implicit default-temp writes are the SHA request file (bytes, unlinked in `finally`, `:1005-1009`) and
the fixture tree, measured at 4476 KB peak. No instrument performs a >50 MB write into `/tmp`.

## Method / receipts

- Probes: `probes.jsonl` (56 records; each `{probe, argv, env, rc, stdout, stderr}`; home paths written
  as `~`). Driver invariant for every run: `HOME`, `XDG_*` under scratch; `TMPDIR` as per probe;
  `python3 -I`; `ulimit -f 65536` on the writing shell.
- Matrix: `refusal-matrix.txt`.
- `/tmp` classification: `grep-tmp-classified.txt`, raw: `grep-tmp-raw.txt`.
- Clone: `git clone -q --shared` of the lane into scratch, `rev-parse --show-toplevel` = clone,
  read at `b4a79843`. No mutating git anywhere in the lane/fleet; the lane was only read.
- Compositor access: `hyprctl binds -j` read-only, inside c1's own isolated child env (probe
  `c1-live-peak` → rc 0, `clauses=a:1 … r:1 admitted=1/1 verdict=TARGET_MET`); no dispatch, no keyword,
  no GUI program.
- Tools installed/upgraded: **none**.
- Scratch `/fast/scratch/hyaku/mado-r50/SentScratch50` deleted before yield; `test -f` on all four
  seat deliverables done.

## For the L1

These are attack evidence, not admission verdicts. None of F1-F6 changes a C1/C2 counter receipt: both
counters still read their frozen `TARGET_MET` sentences at `b4a79843` when given a legal scratch. The
kill-relevant question they raise is the *instrument-hygiene* sentence in the round-50 target and the
M48-10 home rule — C1/C2 receipts do not cover it, so treating "counters green" as "instruments
contained" would be a fabricated readiness claim.
