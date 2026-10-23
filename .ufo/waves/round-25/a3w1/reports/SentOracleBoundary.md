# Sentinel: v4 oracle boundary

SENTINEL v4 boundary: breach: stripping `exec` directives can omit runtime-created binds from the oracle table; the file/socket isolation held in the scored probes.

## Severity, exploit path, impact

**Medium — oracle scope/correctness.** This is a source-based semantic counterexample, not an executed config. `count.py:77-97` removes `exec`, `execr`, `exec-once`, `execr-once`, and `exec-shutdown` lines from the oracle copy. Hyprland v0.56.2 source registers `exec` separately from `bind` (`fetch/a3w1/SrcHandleSource.bin:600-614`) and schedules/spawns the `exec` argument (`:1259-1290`). Its dynamic keyword parser calls `parseDynamic` (`:1089-1091`), where the registered bind handler is available (`:607-608`); the `hyprctl` client routes `keyword` requests (`fetch/a3w1/SrcHyprctlInstance.bin:551-552`). Thus an unstripped config whose exec command adds a bind through the keyword API can produce a bind in Hyprland's unstripped runtime table that the stripped oracle never sees. **[INFERENCE from pinned source; not run, per host-safety bounds.]** The counter's declared stripped-tree predicate is internally consistent, but it is not equivalent to arbitrary unstripped runtime behavior. `ORACLE_CHECK` catches a net difference for the live base snapshot, not this general case.

**Low — availability, inferred only.** `run_tool` has a 60-second timeout and `--die-with-parent`, but no per-tool CPU, memory, or process-count limit; it also mounts an un-sized tmpfs at `/tmp` (`count-v3.py:729-735`). A malicious tool could hog resources or fill that private tmpfs until timeout, delaying this scoring run or competing runs; it cannot thereby change this run's already-captured oracle rows. I did not exercise resource exhaustion.

## Probe commands and receipts

Both probes were run with the v4 counter, `REV=1ed41fa8`, `--jobs 1`, a 4 GB address-space cap, and a 1200-second timeout:

```text
timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /fast/scratch/hyaku/mado-r25a3/sent/oracle-boundary-probe.py --jobs 1
```

Probe source: `/fast/scratch/hyaku/mado-r25a3/sent/oracle-boundary-probe.py`.

- Receipt 1: `artifact://6380`; seed `ace07d5a4054ade5`; probe SHA-256 `07ac26b6a66933d570bba80418b9b77d4d946d4d6a180cfbffdd440073fd1069`; `ORACLE_CHECK base_vs_live missing=0 extra=0` (192 live binds); `PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED`; `exit=1`.
- Receipt 2: `artifact://6909`; seed `a8866a849a2bd63f`; probe SHA-256 `a75faa611abc08fb0630cc771cdbe6bf7177bdbe9f5495c44c5a271f42cc07c8`; same `ORACLE_CHECK` result; `PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED`; `exit=1`.

These are boundary probes, not bind resolvers; the expected 0/41 is not a control verdict. They only open paths (the case-file write check opens with `O_WRONLY|O_APPEND` but writes no bytes) and query `hyprctl instances -j` only. No host file was modified and no write/dispatch/keyword/reload verb was invoked.

## Access and influence findings

**No path escape observed.** In both scored runs the probe reported `cwd=/snap/home`; the direct case config was readable but opening it for write returned `E30` (`EROFS`). Absolute opens of the host home config and lane registration returned `E2` (`ENOENT`); relative host-home/repository opens also returned `E2`. `/run`, `/fast`, and `/run/user/<uid>` were absent; `/tmp/mado-r25-c1v4-*` and slot/runtime globs returned zero, and no host-temp alias, oracle log, or oracle copy was found. `hyprctl instances -j` returned no JSON instance data with either the default environment or a relative `XDG_RUNTIME_DIR` attempt. The clear-env, `--ro-bind home /snap/home`, private `--tmpfs /tmp`, and `--unshare-all` setup is in `count-v3.py:729-735`; the runtime paths are not bound. This supports isolation from host home, the live compositor, nested oracle sockets, host temp files, slot locks, and oracle runtime files for the tested path routes.

The counter finishes every oracle future before it starts the scoring loop (`count.py:241-261`, then `:272-289`). `ORACLE_CHECK` runs before that loop (`:264-271`). Together with the read-only case mount, this means the tool cannot mutate a case tree or alter this run's oracle result after the fact. Timing can delay/timeout scoring and resource pressure can affect concurrent work, but cannot rewrite the stored truth tables. The `--die-with-parent` and 60-second timeout bound the lifetime of the tool process tree.

Normal oracle cleanup sends TERM to the process group, waits, escalates to KILL, closes the log, and removes the known runtime signature directory (`count.py:174-189`); the outer temporary tree is removed in `finally` (`:299-300`). **[INFERENCE, not observed]** if instance discovery never sets `sig`, the `if sig` cleanup skips explicit removal of a possible runtime directory, although the process group is still killed.

## `strip_exec`, `ORACLE_EXTRA`, and `ORACLE_CHECK`

- `strip_exec` is a no-op for exec-free trees. The generated SYNTH/HARD trees use bind directives whose dispatcher can be `exec`; those are `bind = ..., exec, ...`, not standalone `exec =` directives matched by `EXEC_RE` (`count-v3.py:147-177, 383-432, 551-727`). No extra bind effect from stripping was observed in the scored baseline: its stripped-oracle table matched the live capture on both runs. For arbitrary unstripped trees, the source-based exec/keyword counterexample above remains.
- `ORACLE_EXTRA` appends only `ecosystem:no_update_news` and `ecosystem:no_donation_nag` (`count.py:58, 129-131`). The local Hyprland configuration reference describes them as disabling update and donation popups (`round-24/fetch/w1/WikiDebugging-3.bin:761-769`), while the Hyprland source registers bind/unbind separately. **[INFERENCE from docs/source]** these options do not change bind rows; I did not independently rerun an oracle with those lines removed.
- `ORACLE_CHECK` is a real fail-closed base guard: it compares the base oracle result against the live capture as a multiset over the 18 configured fields and exits 2 on any missing/extra row (`count.py:264-271`; `count-v3.py:84-85, 746-751`). Both scored runs observed exact equality for 192 binds. It proves only that this stripped-and-augmented base oracle matched this live capture. It does **not** prove the nested binary's version provenance, that stripping is neutral for every tree, or that generated-case tables match unstripped runtime behavior.

**Smallest remediation:** Keep the oracle from executing arbitrary config commands, but make the measured claim explicitly about the exec-stripped static bind table (or reject/mark unprovable trees whose exec effects matter); do not describe it as the unstripped runtime table. Add per-tool CPU/memory/pid and tmpfs-size limits for availability containment. No counter or lane source was edited.
