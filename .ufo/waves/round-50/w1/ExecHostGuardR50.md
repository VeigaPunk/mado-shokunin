# ExecHostGuardR50 — mado round 50, w1: D7 (M48-10) install-ready host-state guard, demonstrated both ways

Seat `ExecHostGuardR50`, leaf, wave `w1` = BUILD + ATTACK, base `8ae47b957034ae21012bbf09173cca2c48be345e` (lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`). Routed item: round-49 spot-check §6 D7 ("M48-10 host guard drafted, not
installed"). Draft started from `.ufo/waves/round-49/w1/ExecMutantSandbox/hostguard.py`
(sha256 `4329050cba9f5be468588da1e1633e480cee647ecfac4a6f92a8d408aa085052`, 431 lines) and its `demo.sh`
(`16ce3d98…5198`, 261 lines) — the freeze that was never attacked in round 49.

Nothing tracked was edited; no tracked lane file, no fleet file, no `tools/` write, no git/jj mutation, no pacman, no
network, no GUI, no compositor call, no subagent. Writes are only `.ufo/waves/round-50/w1/ExecHostGuardR50/` and this
report. Scratch `/fast/scratch/hyaku/mado-r50/ExecHostGuardR50/` was created under `ulimit -f 65536` and removed by the
driver's `trap` (verified gone after the last run; no scratch path is cited as evidence, only values emitted inside the
receipts).

| path (lane-relative) | role | sha256 | lines |
|---|---|---|---|
| `.ufo/waves/round-50/w1/ExecHostGuardR50/mado-hostguard.py` | draft for `tools/mado-hostguard.py` | `fdaa5c2ec297ebfdddc1238d0dfe693ba0ae75ed2310939843cf14b024b7b47e` | 1158 |
| `.ufo/waves/round-50/w1/ExecHostGuardR50/demo.sh` | demonstration driver (fake home only) | `44cb01d39e7629fb53a8cec9c4f471e79cc886e22c8bb1b09f88506363bfbf68` | 345 |
| `.ufo/waves/round-50/w1/ExecHostGuardR50/receipts/` | 16 receipts + `SHA256SUMS` | `SHA256SUMS` = `69470c1e8bbcf99e7fa89ebf1e79ac476b78343bfd81a8d1020c05484c315c8a` | 197 lines |
| `.ufo/waves/round-50/w1/ExecHostGuardR50.md` | this report | — | — |

Run pin (`receipts/00-setup.txt:1-5`): `lane=mado-shokunin guard_rel=.ufo/…/mado-hostguard.py`,
`guard_sha256=fdaa5c2e…`, `demo_sha256=44cb01d3…`, `python=Python 3.14.8 bwrap=bubblewrap 0.13.1 ulimit_f=65536`.
Tool installs: **none**. `sha256sum -c receipts/SHA256SUMS` → `sums_ok`.

---

## 1. What the tool is

Python 3 stdlib only (no third-party import), runs under `python3 -I -E -s` (`--help` rc 0; the selftest runs isolated).
Three surfaces:

- `digest --declare PATH… [--declare-file FILE] [--json] [--no-redact-home]` — **read-only**: `lstat` + full sha256,
  one record per path (`label kind= size= mtime_ns= ino= dev= sha256= path=`, plus `link=` for a symlink), exit 0.
  This is the only surface a seat may point at real operator state.
- `run --work DIR … -- COMMAND` — digest, run COMMAND with `HOME`/`XDG_*`/`TMPDIR` redirected into `--work`, digest
  again, exit 3 if any declared record moved. `--sandbox bwrap` adds `--mask DIR` (empty tmpfs over each masked path)
  and `--ro-root` (host read-only except `--work`).
- `--selftest [--work DIR]` — 45 hermetic cases; last line `MADO_HOSTGUARD_SELFTEST: 45/45 passed`; exit 0 iff all pass.

Exit codes are the guard's, never the child's: `0` unchanged, `2` usage/refused path, `3` a declared path changed,
`4` prerequisite missing (`bwrap`, a `--mask` that is not a directory), `5` child failed (non-zero, signalled, or past
`--timeout`), `6` internal error. A child that exits 3 with nothing changed reads 5 (`mado-hostguard.py:359` is the
`--timeout` refusal; the child-status separation is case `child_exit3_not_propagated`).

Fixed refusals (no flag overrides them): a work/home/XDG/TMPDIR directory under `/tmp`, `/var/tmp`, `/dev/shm`
(`mado-hostguard.py:94,151`), or inside the invoking uid's home **from passwd, not `$HOME`** (`:151-161`), or inside
the repository the script lives in; a `--declare`/`--mask` directory, FIFO, device or socket; a `--mask` covering
`--work`/`--cwd`; `--mask`/`--ro-root` without `--sandbox bwrap` (`:362,364`); `--env-keep`/`--env-set` of the six
managed names (`:268,283-294`); a `--timeout ≤ 0` (`:359`); no declaration or more than 64 after de-duplication (`:253`).

---

## 2. What the attack on the round-49 draft changed

Each row is a defect I reproduced against the round-49 bytes, the round-50 behaviour, and the case that now pins it
(selftest name; receipts in §3). "fix" = round-49 behaviour was wrong; "add" = missing surface; "pin" = correct and
now locked.

| # | kind | round-49 draft | consequence | round-50 (`mado-hostguard.py`) | case |
|---|---|---|---|---|---|
| a | fix | `--mask` consumed only inside `bwrap_prefix` (`hostguard.py:249`), no refusal elsewhere | `run --sandbox none --mask $HOME` silently **not** masked; a driver believes it is contained | refused, exit 2 (`:362`) | `mask_requires_bwrap` |
| a′ | fix | `--ro-root` same shape | `--ro-root` without bwrap silently not read-only | refused, exit 2 (`:364`) | `ro_root_requires_bwrap` |
| b | fix | `env_keep` applied after `env["HOME"]=home` (`hostguard.py:205`) | `--env-keep HOME` puts the **ambient** HOME back: a mutant derived from `$HOME` writes the real home while the guard reports "ok" if that path is undeclared | the six managed names are the guard's; `--env-keep`/`--env-set` of them refused (`:283-294`) | `env_keep_home_refused`, `env_set_tmpdir_refused` |
| c | fix | `Popen(prefix+cmd, …)` inherits fd 1 (`hostguard.py:351`), also in `--json` mode | a chatty child appends its own stdout to the JSON object: the machine-readable receipt is unparseable | `--json` takes the child's stdout from stderr (`:384`): stdout is exactly one object | `json_run_violation`; `receipts/g-json.txt:4` |
| d | fix | `read_declare_file` opens unguarded (`hostguard.py:185`); any `OSError` → exit 6 "internal error" | a mistyped `--declare-file` reads as a tool crash, not as a caller error | refused, exit 2 with the reason | `declare_file_missing` |
| d′ | fix | an unreadable declared file (`lstat` ok, `open` EACCES) → exit 6 | same | refused, exit 2 (`:218`) | `digest_unreadable_refused` |
| e | add | no de-duplication | the same path declared twice consumes the 64 cap and prints two records | de-duplicated by resolved path before the cap (`:253`) | `declare_dedupe` |
| f | fix | `fmt` printed no `link=` (`hostguard.py:180-182`) | a symlink record's target — the thing actually digested — was invisible in the table (JSON only) | `link=` appended (`:236`) | `digest_symlink` |
| g | fix | `--timeout 0` reached `proc.wait(timeout=0)` | an immediate `TimeoutExpired`, reported as "child failed" (5) | refused, exit 2 (`:359`) | `timeout_nonpositive_refused` |
| h | fix | `sys.exit(4)` inside `bwrap_prefix` (`hostguard.py:230,237`) | the prerequisite path cannot be returned, so no in-process test can pin it | raises `Prerequisite` (`:104`), `main` returns 4 | `mask_not_a_dir_exit4` |
| i | fix | refusal messages printed the raw path (`check_write_dir`) | `--home ~/…` prints a home path into a committed receipt (session material) | every printed path is redacted to `~` (`:138`); `--no-redact-home` opts out | `receipts/e-refusals.txt:9` (`--home ~`) |
| j | add | the round-49 driver post-processed its own receipt (`sed -i "s|$HOME|~|g"`) | redaction lived in one driver, not in the tool | redaction is the default in `digest`, `run` and `--json` | `caseD_home_path_redacted`, `caseD2_home_path_redacted` |
| k | add | no `--selftest` | the instrument had no hermetic check; a counter had nothing to score it with | 45 cases, fd-level capture so a `run` case's child output cannot escape the case | `receipts/f-selftest.txt:48` |
| l | pin | `--work` resolving under `/tmp` via symlink already refused (realpath) | could regress unnoticed | unchanged, now locked | `work_symlink_to_tmp_refused` |

Round-49 bytes are untouched: this is a round-50 erratum-plus-rebuild of a **draft**, not a rewrite of landed work.

---

## 3. The demonstration, both ways (`demo.sh`, all on a fake operator home)

Fixture: `<scratch>/fakehome/.cache/xdg-terminal-exec`, 331 B, sha256 `8e607b28…5307b`, mtime_ns
`1793047345000000000` (`receipts/00-setup.txt:6`) — the shape of the round-47/48 records with content that cannot be
mistaken for the operator's file. Every child in the driver runs with `HOME`/`XDG_*`/`TMPDIR` exported into that
scratch tree; `run` is never pointed at the real home. Index: `receipts/00-case-exits.txt:1` `fails=0`, 29 `OK` lines.

| case | child, guard mode | receipt | observed |
|---|---|---|---|
| A | mutant writing `$HOME/.cache/xdg-terminal-exec`, `--home <fake home>`, no sandbox | `a-unsandboxed-caught.txt:2` | **caught**: `exit=3`, `CHANGED … fields=sha256,size,mtime_ns`, `size=331->10`, `status=violation` |
| A2 | same, payload of the original size, original mtime restored by the mutant | `a2-same-size-mtime-restored.txt:2` | `exit=3`, `fields=sha256` only, `size=331->331`, `mtime_ns=…000->…000` |
| B | **the same mutant** under `run --sandbox bwrap --mask <fake home>` | `b-sandboxed-contained.txt:1-2` | **contained**: `exit=0`, `changed=0 status=ok`, sha256 before = after = `8e607b28…5307b`, and the mutant reports `WROTE … size=13` — the write succeeded *inside* and left nothing behind |
| B2 | `--sandbox bwrap --ro-root` | `b2-ro-root.txt:1-2,16` | `WRITE_BLOCKED errno=30` (EROFS), `TMPDIR_WRITE_OK size=1` (scratch still writable), `caseB2_exit=0` |
| C | control, child `/bin/true` | `c-control-no-change.txt:14` | `exit=0`, `changed=0 status=ok`, `sha_unchanged=yes` |
| E1-E3 | `--work` under `/tmp`, `/var/tmp`, `/dev/shm` | `e-refusals.txt:1-3` | `exit=2` each, `/tmp` named in the reason, `E10_/tmp_dir_created=no` (`:10`) |
| E4 | `--work` inside this lane (`…/ExecHostGuardR50/tmpwork`) | `e-refusals.txt:4` | `exit=2` — refused by the **operator-home** rule, because this lane lives under the operator home; `E12_lane_tmpwork_created=no` (`:12`) |
| E5 | the guard **copied into a throwaway repo**, `--work` inside that repo | `e-refusals.txt:5` | `exit=2` "the guard writes only to external scratch"; `E11_repo_w_dir_created=no` (`:11`). This is the only way to reach the repo rule on this host — see §6 |
| E6-E8 | `--mask` without bwrap, `--ro-root` without bwrap, missing `--declare-file` | `e-refusals.txt:6-8` | `exit=2` each, reason named |
| E9 | `--home <passwd home>` while `$HOME` is the fake home | `e-refusals.txt:9` | `exit=2`, reason prints `--home ~` (redacted) — the refusal is keyed on passwd, not `$HOME` |
| F | `--selftest --work <scratch>/selftest` | `f-selftest.txt:48` | `MADO_HOSTGUARD_SELFTEST: 45/45 passed`, `selftest_exit=0` |
| F2 | `--selftest` with `TMPDIR=/tmp`, no `--work` | `f2-selftest-tmp-refused.txt:1-2` | `exit=2`, `/tmp` refusal, `0/45 passed` — the instrument applies its own rule to itself |
| G | `--json`, chatty mutant | `g-json.txt:3-4` | parses as one object: `JSON status=violation child_rc=0 changed_fields=sha256,size,mtime_ns`; `JSON child_stdout_went_to_stderr=True` |
| I | the guard wrapped in an **outer tracer**: `strace -f -e trace=execve` around `run --sandbox bwrap --mask <fake home>` (SentHostState R-SHS-3 shape) | `i-outer-tracer.txt:1-6` | verdict unchanged: `exit=0`, digest before = after, `bwrap_execve_lines=1`, `ptrace_failures=0`, the mutant's write still contained — the guard starts no tracer of its own, so an outer one cannot make it miss |
| H | footprint | `h-footprint.txt:1-25` | exactly what the guard created under `--work` (`work/tmp/ok`) and what the selftest created; the fake home holds only case G's 8 bytes |

Both directions are measured, not assumed: in A the declared bytes move and the guard says 3; in B the same child
reports a successful write and the declared bytes are byte-identical.

---

## 4. The one real-state read (read-only, values only)

`receipts/d-operator-digest.txt` — four paths, printed as `~`, compared line by line with
`.ufo/waves/round-50/receipts/operator-state-before.txt` (sha256 + size + mtime seconds):

| path | sha256 (reproduced = receipt) | size | mtime_s |
|---|---|---|---|
| `~/.cache/xdg-terminal-exec` | `ddd94f6bca4bcd42c426da9bbeb9955ca5d77b8778b4e290fcfffcc984a1b3d5` | 190 | 1793069967 |
| `~/.config/hypr/input.conf` | `3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4` | 1584 | 1791060272 |
| `~/.config/hypr/bindings.conf` | `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581` | 2879 | 1791060272 |
| `~/.config/hypr/hyprland.conf` | `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` | 1329 | 1792267376 |

`COMPARE summary paths=4 mismatched=0` (`d-operator-digest.txt:11`), one `COMPARE MATCH` per path (`:7-10`). The
before-receipt's fifth line is a count, not a file; measured with the same command shape (`ls -la | wc -l`) it is
`local_bin_ls_la_lines=103 (before receipt: 103) same=yes` (`:6`).

The same digest is taken **again after every case** — `receipts/d2-operator-digest-after.txt:10` reads
`COMPARE summary paths=4 mismatched=0`: the whole demonstration, including the two mutants, changed no operator state.
That is the both-ways receipt D7 asks for, plus the no-write side. No receipt contains a home path or the account name
(a sweep of all 15 receipts for `/home/` and the account name returns nothing; findings i/j above are what makes that
true).

---

## 5. Hermetic selftest — 45 cases

`MADO_HOSTGUARD_SELFTEST: 45/45 passed` (`receipts/f-selftest.txt:48`), rc 0, ~1.2 s, all fixtures generated in-process
under `--work`, no network, no host state read except passwd and the presence of `bwrap`. Names, in run order:

`digest_absent`, `digest_unreadable_refused`, `digest_dir_refused`, `digest_fifo_refused`, `digest_symlink`,
`digest_json_ok`, `digest_no_declare`, `digest_too_many`, `declare_file_comments`, `declare_file_missing`,
`declare_dedupe`, `work_tmp_refused`, `work_vartmp_refused`, `work_devshm_refused`, `home_real_refused`,
`cwd_real_home_refused`, `work_in_repo_refused`, `work_symlink_to_tmp_refused`, `work_prefix_mismatch`,
`control_true_exit0`, `mutant_unsandboxed_caught`, `same_size_same_mtime_sha_only`, `absent_then_created`,
`file_then_absent`, `sandbox_bwrap_contained`, `ro_root_write_blocked`, `child_exit3_not_propagated`,
`missing_binary_exit5`, `timeout_kill_exit5`, `env_clean`, `env_keep`, `env_keep_home_refused`,
`env_set_tmpdir_refused`, `ambient_home_is_not_operator_home`, `env_set_bad`, `mask_requires_bwrap`,
`ro_root_requires_bwrap`, `mask_not_a_dir_exit4`, `mask_covers_work_refused`, `json_run_violation`,
`timeout_nonpositive_refused`, `unit_redact_home`, `unit_under_prefix`, `unit_changed_fields`.

Namespace cases have a bwrap-absent branch (`exit 4` asserted instead), so the count is 45/45 with or without bwrap —
the count never silently drops. `digest_file_sha` pins the fixture digest `d3523f5a0a34…`; `env_clean` proves the
child sees exactly `PATH=/usr/bin:/bin`, the five redirected homes and `TMPDIR` under `--work`, and no ambient variable.

---

## 6. What it does not do (stated, not hidden)

- With `--sandbox none` the guard is a **detector**: it proves "no declared path changed across the run", never "the
  child caused it" (a concurrent operator write reads as a violation), and it cannot stop a write it reports.
  Prevention needs `--sandbox bwrap --ro-root` or `--mask`.
- Attribution is out of scope, same limitation N2 recorded for the old `host_cache_untouched` field.
- Singleton paths only: a directory, FIFO, device or socket is refused, not walked. Up to 64 declarations, each read in
  full (no size cap — declarations are meant for small state files).
- bwrap needs user namespaces; without `bwrap` the run exits 4 and never silently degrades to unsandboxed. `--mask`
  and `--ro-root` are Linux-only.
- It contains where a command may write, not what it may do: it is not a seccomp profile and says nothing about a child
  that escapes its mount namespace.
- The repo rule is **shadowed by the home rule on this host**, because the lane itself lives under the operator home:
  `--work` anywhere in the lane is refused as "inside the operator home" (E4). The repo rule is real and demonstrated
  (E5, `work_in_repo_refused`), it just never gets to fire first here. If a future lane lives outside `~`, the repo rule
  takes over with the same exit code.
- `--no-redact-home` exists: a counter that needs the raw path must pass it explicitly and then own the receipt's
  privacy. Default is redacted.

---

## 7. Adoption shape the L1 can freeze into the counters

Mutant or any command that may write (M48-10's shape), `$WORK` the counter's own scratch root:

```sh
python3 tools/mado-hostguard.py run \
    --work "$WORK/guard" --work-prefix /fast/scratch \
    --sandbox bwrap --mask "$HOME" --declare "$HOME/.cache/xdg-terminal-exec" \
    --env-keep LANG -- <env-scrubbed command ...>
```

Read-only judge (`xkbcli`, a scored tool):

```sh
python3 tools/mado-hostguard.py run --work "$WORK/guard" --work-prefix /fast/scratch \
    --sandbox bwrap --ro-root --declare "$HOME/.cache/xdg-terminal-exec" -- <judge argv>
```

Machine-readable consumers add `--json` and read `status`, `changed[].fields`, `child_rc`, `env`, `mask`; stdout is one
object (case G). Selftest, for the freeze: `python3 -I tools/mado-hostguard.py --selftest --work "$WORK/selftest"` →
last line `MADO_HOSTGUARD_SELFTEST: 45/45 passed`, rc 0. `$HOME` in the snippets is substituted by a fake home in this
seat's receipts; a real counter with the real home under `--mask` is the intended production shape.

---

## 8. Reproduce

```sh
cd mado-shokunin/.ufo/waves/round-50/w1/ExecHostGuardR50 && sh ./demo.sh   # exit 0, last line "fails=0" in 00-case-exits.txt
( cd receipts && sha256sum -c SHA256SUMS )                                # 15/15 OK
```

`demo.sh` needs only `/bin/sh`, `python3`, `bwrap`, and a writable `/fast/scratch`: it exits 9 if that scratch root
cannot be created, exports a fake `HOME`/`XDG_*`/`TMPDIR` before any child starts, and removes its scratch on `EXIT`.

---

## 9. For the L1

- **Install**: copy `mado-hostguard.py` to `tools/mado-hostguard.py` unchanged (`sha256 fdaa5c2e…b47e`); the copy is the
  one that was selftested and demonstrated (the demo's `guard_rel` is the seat file, byte-identical).
- **Freeze candidate**: `PRED-D7-r50` = `--selftest` 45/45 at the revision **and** the two-way demonstration
  (`a:*` exit 3 with named fields, `b:*` exit 0 with the digest unchanged, `c:*` exit 0) **and** `digest` reproducing
  the four sha256 values in `.ufo/waves/round-50/receipts/operator-state-before.txt`. Pin the receipt digests, not the
  scratch paths.
- **Tracer parity (measured, routed R-SHS-3)**: `SentHostState` reports that wrapping the round-49 C1 counter in any
  outer tracer makes it read a false `TARGET_MISSED`, because that counter runs `strace … bwrap …` itself and the
  nested ptrace is refused. This guard runs no tracer; case I measures the same wrap and the verdict is unchanged
  (`receipts/i-outer-tracer.txt:1-6`, `ptrace_failures=0`). A counter that adopts the guard can still be wrapped.
  Unlike the round-50 instruments SentHostState surveyed, this one **does** refuse a scratch root under a home
  (`--work`/`--home`/XDG/TMPDIR inside the passwd home → exit 2), so a SIGKILL cannot leave it writing into a home.
- **What w2 should attack**: `--env-keep`/`--env-set` of the six managed names (case b), `--mask` without bwrap (a), the
  `--json` stdout contract (c), `--work` reached through a symlink (l), and the un-shadowed repo rule (E5). The weakest
  point I know of and did not fix: with `--sandbox none`, a child that writes an **undeclared** path inside the fake
  home is not a violation by contract (only declarations and `--ro-root`/`--mask` cover that) — a counter must declare
  the paths it cares about.
- Round-49 hygiene: the round-49 draft and driver remain untouched at `4329050c…` / `16ce3d98…`; §2 is the erratum
  content if the lane wants it recorded under `corpus/lessons/`.
