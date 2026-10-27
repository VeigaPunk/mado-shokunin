# SentHost — threat review: host-side tools/commands used by C1/C2 (round 48, wave w2)

Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Surface: every host-side command the C1/C2 instruments, generators, helpers and committed artifacts invoke.
Evidence: `.ufo/waves/round-48/w2/SentHost/gen-run.txt`, `host-surface-1.txt` … `host-surface-8.txt`.
Scratch `/fast/scratch/hyaku/mado-r48/SentHost` (peak 75 344 B, largest file 52 654 B, `ulimit -f 2048` in every
writer shell), removed before return; no install, no package transaction, no service/compositor/input action.

## Verdict

The three invariants the seat was pointed at hold on the committed C1/C2 surface.

| Check | Result | Basis |
|---|---|---|
| Pin invocations carry a print verb | **PASS** | frozen `check_case` refuses print-less `args` **and** `prime.args` (dynamic, below); all 204 fixtures clean; `warmcheck.py` ARGS list is print-only |
| Pin invocations use a scratch `XDG_CACHE_HOME` | **PASS** | every case env is `$ROOT/.rw/...` (dynamic refusal of `/fast/elsewhere`); counter mounts the pin's cache under the case root; fixtures carry 0 host-absolute env values |
| `xkbcli` read-only verbs only | **PASS** | generator + replay use `--version` and `compile-keymap` with `--kccgst`/`--test`/`--verbose`; no `list`/`how-to-type`/`interactive-*`, no write-capable verb |
| No pacman install/query | **PASS** | only `ls -d /var/lib/pacman/local/libxkbcommon-[0-9]* …` (a directory read, generator line 37-38); zero `pacman` invocations in the wave |
| No host write / service / compositor change | **PASS with 3 defects** | `hyprctl`/`systemctl`/`loginctl`/`dbus-send`/`pkill` counts 0; the only out-of-scratch writer is the C2 receipt generator (F3/F4); C1 pin runs are `bwrap --unshare-all` contained |

No frozen predicate is broken by the data bytes: `PRED-C2-r48` clause (r) reproduces — the committed receipt's
`host.keymap` digest `efd487a3…cfce81` is re-obtained by the committed generator on this host, and the full receipt
differs by exactly one line (the `# taken:` timestamp). `PRED-C1-r48`'s containment guards behaved as written when
exercised. Findings F2/F5 are *substrate* defects (they can flip a verdict only on a PATH-polluted or hostile-environment
runner, i.e. not the L1's), F1/F3/F4 are provenance/cleanup defects. Nothing here is a TARGET miss.

## Findings

### F1 — dangling generator locator inside the committed C2 receipt — severity: medium (provenance)
`receipts/xkbcli-compile-keymap-r48.txt:1` says
`… generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh`. No such path exists anywhere: the generator is
`tools/make-xkb-receipt.sh` (`find` over the wave: one hit; `receipts/` holds only the 14 270 B `.txt`; nothing tracked).
`rows-c2.md` S350 names the correct `tools/` path, so the receipt and its own row disagree, and a replay that follows
the receipt's locator finds nothing. The line is emitted by the generator itself (`make-xkb-receipt.sh:29`, a `say`
that hardcodes `receipts/`), so every re-run re-prints the wrong locator.
Impact: the receipt cannot be verified by following its own self-attestation; cost is a dead locator in published data.
Remediation: change the `say` at generator line 29 (and the file header comment at line 3, which makes the same claim)
to `tools/make-xkb-receipt.sh`, regenerate, and replace the receipt + its `fetch/` byte copy. Cost: one byte-identical
re-run (proved below) plus the two copies.

### F2 — the C1 isolation boundary is resolved through inherited `PATH` — severity: medium (substrate trust)
`c1-r48-terminal-cache.py:254-255` `self.bwrap = shutil.which("bwrap")`, `self.strace = shutil.which("strace")`, while
the fixture externals three lines later are pinned: `:260` `shutil.which(n, path="/usr/bin")`. Both isolation binaries
are the judge's only containment and its read-only proof. Exploit path: a runner with a writable directory ahead of
`/usr/bin` (a seat scratch on `PATH`, a wrapper dir) supplies a `bwrap` that execs the pin with no namespaces and a
`strace` that writes nothing; clause (w) then runs the real resolver against fixture trees with the host visible, and
clause (r) passes vacuously (`check_trace` sees an empty file as "no trip", `:361`). Every printed line still says
`pass` and the final line still says `TARGET_MET`.
Remediation: `shutil.which(x, path="/usr/bin")` for both, plus one fail-closed sanity check (e.g. refuse when
`bwrap --version` is absent, and refuse a trace file with no `execve` of the sandboxed python). 2-line change.

### F3 — the committed C2 receipt is not reproducible at its cited location, and re-running it writes into the lane — severity: medium (provenance + lane write)
`tools/make-xkb-receipt.sh:7-8`: `HERE=$(cd "$(dirname "$0")" && pwd)`, `OUT="$HERE/xkbcli-compile-keymap-r48.txt"`.
Run from `tools/`, the generator writes `tools/xkbcli-compile-keymap-r48.txt` — not `receipts/…`, the path every row
and clause cite. Demonstrated on a scratch copy: the run wrote the receipt *beside the script* (14 270 B, same size as
the committed one, same `host.keymap` digest), leaving a byte artifact inside the lane tree and nothing at the cited path.
The committed receipt itself proves the drift chronologically: receipt mtime 21:08 local, generator mtime 22:10 local
(after the receipt), so the frozen generator bytes are not the ones that produced the frozen receipt — harmless here
because the command set is deterministic (diff = timestamp only), but unverifiable from the artifacts alone.
Remediation: `OUT="$HERE/../receipts/xkbcli-compile-keymap-r48.txt"` (or an explicit `--out`), and record the
generator's sha256 in the receipt header so drift is detectable.

### F4 — generator scratch root and probe setup are not fail-closed — severity: low-medium (evidence integrity)
`make-xkb-receipt.sh:10-13`: `S=${XKB_R48_SCRATCH:-/fast/scratch/…}` (env-overridable, unvalidated — a caller can aim
it at the lane or the home tree), `mkdir -p "$S"` (never removed; a run leaves an empty dir, demonstrated), and
`trap … EXIT INT TERM` only, so SIGHUP/SIGKILL leaves the probe tree behind. Script uses `set -u` **without** `set -e`,
and the include-path probes (`:122-131`) do `mkdir -p` / `cp` and then print `rc=$?` of the *xkbcli* call: if the fixture
copy fails, the receipt records a probe failure that is indistinguishable from a measured negative result ("neither user
path present: rc=1"). That is the one place in the C2 surface where setup failure can be read as evidence.
Remediation: assert the three probe files exist before each probe (`test -s … || { echo SETUP-FAIL; exit 1; }`), add
`HUP QUIT` to the trap, and `rmdir "$S"` at the end.

### F5 — C2 replay builds its child environment from the whole caller environment and takes `TMPDIR` unvalidated — severity: medium (verdict can flip)
`c2-r48-xkb-entry.py:815` `tempfile.mkdtemp(dir=os.environ["TMPDIR"], …)`, `:817` `env = dict(os.environ)` with only
`HOME`/`XDG_CONFIG_HOME`/`XDG_CACHE_HOME` rewritten and `:823-825` popping the five `XKB_DEFAULT_*` names. Everything
else is inherited — notably `XKB_CONFIG_ROOT`, `XKB_CONFIG_EXTRA_PATH`, `XDG_DATA_DIRS`, `XDG_CONFIG_DIRS`, `PATH`
(`:810` `shutil.which("xkbcli")`). Two consequences: (i) a runner exporting `XKB_CONFIG_ROOT` changes the replayed
keymap, so clause (r) reports `positive_replay_failed` — a *false miss* on a correct tree — or, aimed the other way,
lets a tree other than the host's produce the receipt's digest; (ii) with `TMPDIR` pointed inside the lane, the counter
creates and `shutil.rmtree`s `c2r-*` inside the repository, which `c1`'s counter explicitly forbids for `--work`
(`c1-r48-terminal-cache.py:1003-1008`, `under()` at `:891`). C1 is correct here; C2 is not.
Remediation: build the replay env from a fixed allowlist (`PATH=/usr/bin:/bin`, `LANG`, `HOME`, `XDG_CONFIG_HOME`,
`XDG_CONFIG_DIRS`, `XDG_DATA_DIRS`, `XDG_CACHE_HOME` all under `S`), drop every `XKB_*`, and refuse `TMPDIR` inside
the repo/lane with the existing `under()` helper. ~8 lines.

### F6 — `c2-mirror.sh` deletes an argv-supplied path with no containment, and leaves its scratch — severity: medium (destructive prefix)
`l1-draft/c2-mirror.sh:8-9`: `S=${2:-/fast/scratch/…}` then `rm -rf "$S"; mkdir -p "$S/m"`. No prefix/sentinel check
(grep for containment: 0 hits), no `trap` (0 traps in the file), and no cleanup at the end, so a run leaves a full
`--shared` clone plus the `corpus` mirror under `/fast`; a mistyped second argument deletes whatever it names.
`c1-score.sh:8-9` is the same shape but its `S` is prefix-fixed (`…/L1c1-$TAG`), so it is bounded; it also cleans only
on the success path (`:21`), leaving the clone and work dir on an early `set -eu` exit.
Remediation: `case "$S" in /fast/scratch/hyaku/mado-r48/*) ;; *) exit 2;; esac` before the `rm -rf`, plus one
`trap 'rm -rf -- "$S"' EXIT` in each helper.

### F7 — documented AGREE recipe leaks a temp dir; helper probe leaves an orphan on timeout — severity: low (cleanup)
`mado-terminal.py:22` documents `XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-path --print-cmd`:
print verbs and a scratch cache are correct, but nothing removes the `mktemp` dir, so the recipe the tool hands to readers
leaks one empty directory per run, and `mktemp -d` without `-p` lands outside any seat scratch root.
`warmcheck.py:53-56` runs the pin through `sh -c '…; wait'` with `timeout=20`; on timeout `subprocess.run` kills the
`sh`, and the resolver's forked background `save_cache` grandchild is not signalled — it can still write a cache into a
tree the harness `rmtree`s at `:146/:155`. Bounded to `WORK`, but it is an unreaped child.
Remediation: `d=$(mktemp -d); trap 'rm -rf "$d"' EXIT` in the documented recipe; run warmcheck's pin under
`start_new_session=True` and `killpg` on timeout.

### F8 — `/tmp` fallback in a C2 generator — severity: low
`add-replay-clause.py:39` `tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or "/tmp", …)`. The frozen counter refuses to
replay without `TMPDIR`; this generator silently falls back to `/tmp`, which the wave's scratch rule forbids and which is
the one directory an unprivileged writer must not target here. It also writes the patch into the counter path (`:88`)
with no scratch bound.
Remediation: require `TMPDIR` as the counter does, and refuse a path inside the lane.

### F9 — `l1-draft/__pycache__/` inside the freeze tree — severity: low (cleanup)
Two ignored bytecode blobs sat in the draft dir during the freeze window (`lsemu.cpython-314.pyc` at 20:45,
`mado-terminal.cpython-314.pyc` at 22:25). Lane `.gitignore:3` is `__pycache__/`, so they cannot enter the freeze commit
(`git check-ignore` confirms), but they are lane-tree contamination while seats read the tree, and they are
interpreter-version-specific. A probe of mine wrote a third (`c1-r48-terminal-cache.cpython-314.pyc`, 22:27) — removed;
the frozen counter's bytes are untouched (`sha256 2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4`,
mtime 22:08:27). `l1-draft/__pycache__/` should be removed before the freeze commit.

## Accidental sensitive values in committed artifacts (classes only)

Checked for credentials/tokens/keys/IPs/private-key blocks: none. The classes present:

1. **Workstation user name in absolute paths** — 17 occurrences in `receipts/xkbcli-compile-keymap-r48.txt` and the same
   17 in its `fetch/` byte copy (home config paths, include-path probe paths, `sha256sum` output lines).
2. **Verbatim host configuration content** — 9 lines copied out of two dotfiles by the `grep -n 'kb_'` step, plus 2
   `sha256sum` digest lines over the same files. The digests are stable host fingerprints of files outside the repo.
3. **Host identity** — one kernel release line (`# host: Linux <release> <arch>`), one UTC capture timestamp; the
   timestamp is also the only line that makes the receipt non-byte-reproducible.
4. **Absolute scratch/fleet paths** — 9 receipts in the freeze set (`receipts/`) contain `/fast/scratch/...`;
   4 contain `/home/<user>/Projects/...` (`census-before.txt`, `census-after.txt`, `m48-revived-r47-seat-edit-2.diff`,
   the XKB receipt).
5. **Package-database paths and exact package versions** (pacman DB directory listing) — intentional, low.

Classes 1-3 got in through `make-xkb-receipt.sh`'s `grep`/`sha256sum`/`uname`/`date` lines rather than by decision; a
corpus receipt that publishes a knowledge claim does not need the user name or the host's dotfile bodies. If the L1
wants them gone: run the two file reads under `HOME=$T` with copies of the config snippets, and print paths relative to
`$HOME`. Predicate impact: none (clause f/r do not read those lines).

## What was executed (and what was only read)

Executed, bounded, inside `/fast/scratch/hyaku/mado-r48/SentHost`:
- the committed generator copied to scratch and run (`XKB_R48_SCRATCH` redirected): rc 0, 14 270 B receipt, `host.keymap`
  digest equal to the committed receipt's, `diff` = the `# taken:` line only; empty scratch-root dir left → F3/F4.
- the frozen `check_case` imported from a scratch copy and probed: print-less `args` → `Setup … args would launch a
  terminal`; print-less `prime.args` → same; `XDG_CACHE_HOME=/fast/elsewhere` → `Setup … must be under $ROOT/.rw`;
  `$ROOT/.rw/cache` and a conforming `--print-cmd` case → accepted. (First probe ran against the lane file and wrote a
  `.pyc`; removed, and re-run from scratch with `PYTHONDONTWRITEBYTECODE=1`, evidence `host-surface-5.txt`.)
- an independent pass over all 204 fixtures: 0 non-print argvs (args or prime), 0 `XDG_CACHE_HOME` outside
  `$ROOT/.rw`, 0 host-absolute env values; class histogram `WARM-DIFFERS 48 / WARM-INVALID 34 / MALFORMED 31 /
  WARM-SAME 26 / H2 13 / H1 12 / HOME-UNSET 10 / READDIR 10 / …` totals 204, matching the registration's count.
- verb censuses over `l1-draft/` + `tools/` (hyprctl, systemctl, loginctl, dbus-send, pkill, pacman, absolute-path
  redirects, mutating git subcommands → 0 / 0 / 0 / 0 / 0 / 2 (an `ls` of the pacman DB) / 0 / 0).

Read only: `registration.md`, `claims.md`, both frozen counters, the C2 entry/rows/README row/gate rows, the w1 harness
and probe scripts (`ExecRefCacheA/harness`, `ExecRefCacheB/probe_pin*.py`, `run_probe.sh`). The w1 pin probes take their
argv from `ARGS_*`/literal `--print-*` lists and always run inside `bwrap --unshare-all` with the cache under the case
`root/.rw`; the reference harness has no print-only assertion of its own (the counter does), which is why the counter's
guard, not the harness, is the thing worth freezing.

**No predicate change is requested.** F1/F3 are the two the L1 can fix at zero risk before the freeze (one `say` line +
one `OUT` path, regenerate); F2/F5 harden the two judges and cost fewer than ten lines each.
