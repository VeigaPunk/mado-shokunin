# MutC2Replay — w2 falsification: PRED-C2-r48 clause r replay-channel bypass

Seat: MutC2Replay · round 48 wave w2 (FALSIFY) · lane `/home/vgpnk/Projects/shokunin/mado-shokunin` · base `579f694b45c797a9c39761fdb4f9e0a1b71b3585` · instruments at lane tip `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d` (counter draft `l1-draft/c2-r48-xkb-entry.py` byte-identical to `quality/counters/c2-r48-xkb-entry.py`, sha256 prefix `4a0e6924eada`).

## Claim attacked

Registration, C2 residuals: "*replay independently proves the live compiler output and negative behavior*" (clause r, counter lines 780-871). Seat target: does clause r measure the host's real pinned `xkbcli`, or does it accept a fake selected via executable/path or via the child process environment?

## Detector (bounded, identical across all runs)

`TMPDIR=<scratch>/replay python3 -I quality/counters/c2-r48-xkb-entry.py --repo <replay-tree> --rev HEAD`, judged on the `clause=r` line and the final `PRED-C2-r48: admitted=… verdict=…` line. Baseline first, then mutated bytes in a disposable scratch clone, then the same tree with the attack vector removed (control).

## Replay tree

Built per `l1-draft/c2-mirror.sh` but plumbing-only (no worktree, git index of the full base tree exceeds the 1 MiB/file bound): `git clone --shared --no-checkout`, then `git mktree` surgery — base tree + overlay (entry, rows S340+, README row, round-48 fetch pins/receipt/tools from tip) → commit `--rev HEAD`. Verified: base checkout exists, `rev-parse --show-toplevel` = clone root before every tree mutation.

## Mutants and results

### Mutant A — PATH shim accepts a fake `xkbcli` (clause r judge is caller-controllable)

`shutil.which("xkbcli")` (counter line 810) resolves via the invoking process's `PATH`; the counter runs `python3 -I` (does not scrub `PATH`) and invokes the replay child by that resolved path. A scratch shim placed first in `PATH` faked all four replayed commands (positive compile → forged bytes; probes → rc 1/1/0 with the required `Couldn't find file` / `process include statement` / `XKB-595` stderr markers). Shim preserved at `xkbcli-shim-mutA.sh` (only ever on the scratch `PATH`, never installed).

- forged keymap digest `sha256(b428bd69eb4095961c766adc897d4af0ece3bd8fb8193b4ce9cafb45098d7cd7)` (86 bytes, never produced by `/usr/bin/xkbcli`).
- A (receipt-only forged digest, rev `4df6d38a…` this run), shim first in PATH: `clause=r replay=ok sha=b428bd69eb40 neg=(1,1,0) ver=1.13.2` — **clause r accepted the fake binary's bytes**; overall TARGET_MISSED only via clause f's entry↔receipt digest binding (a separate, text-only defense).
- A2 (same forged digest stated consistently in entry + receipt, rev `7f29e1a4…`), shim first in PATH: **`PRED-C2-r48: admitted=1/1 verdict=TARGET_MET`, exit 0** with clause `r replay=ok sha=b428bd69eb40`.
- A2 control — identical tree, host `PATH`: `clause=r positive_replay_failed rc=0 sha=efd487a39920` → TARGET_MISSED. The kill comes from removing the PATH shim, not from clause r.

**Verdict: SURVIVED (full predicate bypass via executable/path selection).** The replay is not independent of the invoking environment: whoever controls `PATH` controls which bytes clause r compares.

### Mutant B — `XKB_CONFIG_ROOT` passed through to the genuine binary

Counter line ~818 builds the replay child env as `dict(os.environ)` and pops only `HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XKB_DEFAULT_*`. It does **not** pop the compiler data-root variables that pinned libxkbcommon 1.13.2 honors — grounded in the round-48 fetch pins: `XKB_CONFIG_ROOT` (xkbcommon-context.c:231), `XKB_CONFIG_EXTRA_PATH` (:92), `XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH` (:105), `XKB_CONFIG_VERSIONED_EXTENSIONS_PATH` (:119). A nonexistent root merely falls back with a warning (receipt tail "root override falls back to the legacy root"; my probe: `XKB_CONFIG_ROOT=<empty>` → rc 0, empty stderr at default log level), so the bypass uses an **existing** replacement root: a copy of `/usr/share/xkeyboard-config-2` (xml/lst/dtd excluded) with 9 `Portuguese`→`PortugueseX` edits in `symbols/br`.

- data-root keymap digest `sha256(100c006162c92f2fcf4feadf05db6c8a531183fd3ce53d038cabb5a4f5e7977f)` (73080 B; the host root gives `efd487a3…fce81`, 73079 B).
- B (digest stated consistently in entry + receipt, rev `f399add0…`), real `/usr/bin/xkbcli`, `XKB_CONFIG_ROOT=<scratch root>` in the counter's env: **`PRED-C2-r48: admitted=1/1 verdict=TARGET_MET`, exit 0** with `clause=r replay=ok sha=100c006162c9 neg=(1,1,0) ver=1.13.2`.
- B control — identical tree, no `XKB_CONFIG_ROOT`: `clause=r positive_replay_failed rc=0 sha=efd487a39920` → TARGET_MISSED.

**Verdict: SURVIVED (full predicate bypass via environment, with the genuine pinned binary).** Even pinning the executable path would not restore independence; the replayed compile inputs are environment-selectable.

### Baseline (detector green)

Pristine overlay rev this run `f876722f…`: `clause=r replay=ok sha=efd487a39920 neg=(1,1,0) ver=1.13.2`, `TARGET_MET` exit 0 — tree recipe correct; live recompile matches the committed receipt digest `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81` (73 079 B).

## Before/after hashes (mutated points)

| Point | Before | After |
|---|---|---|
| receipt `<sha> host.keymap` line (A/A2) | `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81` | `b428bd69eb4095961c766adc897d4af0ece3bd8fb8193b4ce9cafb45098d7cd7` |
| entry stated digest (A2/B) | `efd487a3…` (then `b428bd69…` for B) | `b428bd69…` (A2) / `100c006162c92f2fcf4feadf05db6c8a531183fd3ce53d038cabb5a4f5e7977f` (B) |
| symbols/br data root (B) | `/usr/share/xkeyboard-config-2` (package) | scratch copy, 9 name edits |

## Restoration evidence

All mutations lived only in `/fast/scratch/hyaku/mado-r48/MutC2Replay/m/clone` (scratch, `trap 'rm -rf -- "$S"' EXIT`), removed on driver exit. Lane untouched throughout: lane `HEAD` identical before/after (`3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`); the committed receipt blob at tip is unchanged (`c54264f63af08a925aac14a0d72d01e29d75715c`); no tracked lane file, sibling lane, fleet file, or system environment modified. No package transactions run (pacman paused per wave policy); no tool installed.

## Named residual (the defect, pre-data)

1. Clause r's judge identity is `shutil.which("xkbcli")` — caller-`PATH`-controllable; no absolute path, no binary digest, no `xkbcli --version` comparison (the receipt's `ver=` is printed but never checked against the live binary — counter lines 810-840).
2. The replay child env inherits `XKB_CONFIG_ROOT`, `XKB_CONFIG_EXTRA_PATH` and the two `XKB_CONFIG_*_EXTENSIONS_PATH` vars (all honored per pinned context.c), so the compiled bytes are environment-selectable even with the real binary.
3. The keymap bytes themselves are never committed (only the digest), so nothing beyond the single digest binds the receipt to any observable output; clause f's entry↔receipt binding is text-only and falls to a consistent forgery (A2/B).
4. Secondary: the counter requires `TMPDIR` but does not constrain who sets it; `LD_PRELOAD`/loader-level channels were not probed (out of seat scope).

Repair direction (L1 decision, pre-data re-registration allowed): resolve the replay executable at an absolute receipt-recorded path (`/usr/bin/xkbcli`), require live `--version` == receipt triple, and pop the four `XKB_CONFIG_*` variables (and `LANG`/`LC_ALL` are harmless here) from the replay env; optionally hash the resolved binary. Per registration, a surviving mutant is a coverage finding — the predicate itself was not narrowed and no data changed.

## Evidence files (this seat dir)

`out-baseline.txt`, `out-A-fake-path.txt`, `out-A-control.txt`, `out-A2-fake-path.txt`, `out-A2-control.txt`, `out-B-xkbroot.txt`, `out-B-control.txt` (full counter outputs incl. per-clause lines), `xkbcli-shim-mutA.sh`, `digest-ledger.txt`, `digestA.txt`, `digestB.txt`, `host-real.keymap`, `host-b.keymap`, `driver.sh` (reproducible driver). Largest output file written: `SOURCES-new.md` 251 414 B (< 1 MiB bound); driver-measured `scratch_total=748K` (pre-B run) plus the ≤ 3.9 MB B-root copy — ≪ 2 GB; cleaned by trap.
