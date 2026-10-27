# SentHost — seat status and receipt index

Status: complete. Read-only seat; host state unchanged (proof in `receipts/01-host-cache-before.txt` and
`receipts/07-host-cache-after.txt`: same size/mode/inode/mtime/sha256 before and after every probe).

- Findings, severity, exploit paths and remediations: `../SentHost.md` (the Report trailer deliverable).
- Copy-paste guard text for the counters and the seat prompts: `guards.md` (G1-G6).
- Probe (re-runnable, bounded, scratch-only): `probe.sh`; receipts under `receipts/`.

| receipt | what it proves |
|---|---|
| `01-host-cache-before.txt` / `07-host-cache-after.txt` | host cache untouched; 190 B, 0600, sha256 `f497ed05…` = the round-47 value |
| `02-prime-race.txt` | a prime that lets the sandbox exit produces **no** cache (3 shapers); the bounded sleep poll produces it 3/3 in 20-25 ms |
| `03-cache-mutation.txt` | a cold run writes; `XTE_CACHE_ENABLED=false` and a `/disable_cache` line **delete**; a warm run does not write; `XTE_DEBUG=1` gives the oracle's own warm/cold verdict on stderr; §6: only `--print-cmd`/`--test-mode`/launch reach the save site (pin :1368-1385), `--print-id`/`--print-path` neither write nor delete |
| `04-xkbcli-env.txt` | `xkbcli compile-keymap` is read-only (0 writes, 0 sockets, 2 execve); `XKB_DEFAULT_*` inert; `XDG_CONFIG_HOME/xkb`, `$HOME/.xkb`, `XKB_CONFIG_EXTRA_PATH`, `XKB_CONFIG_ROOT` all control the include set; numeric `0..10` or the symbolic `critical` suppresses `XKB-595` |
| `05-devices-shape.txt` | `hyprctl devices -j` keysets and counts (no values): `name`/`address` are the material keys |
| `06-host-tooling.txt` | bwrap 0.13.1, strace 7.2, userns available; loader symlinks required; no `/etc` → numeric ids; ambient `XDG_CACHE_HOME=/home/vgpnk/.cache` |
| `08-cache-path-resolution.txt` | the resolver's cache target under ambient / unset / guarded env |
| `09-home-fallback.txt` | `XDG_CACHE_HOME` unset → `$HOME/.cache`; a read-only `HOME` cannot be primed (mkdir fails, rc still 0) |

Top three for the freeze: **F1** prime race (a warm clause that passes without warming), **F2** host cache
deletion/overwrite by any unredirected resolver call, **F4** `xkbcli` include-path and log-level environment
dependence of the C2 receipt.

Writes: this seat dir only (`report.md`, `guards.md`, `probe.sh`, `receipts/*`) plus `../SentHost.md`.
No tracked file edited; no git/jj verb; no package transaction; scratch removed.
