# ReopenS169 — re-verification of SOURCES row S169

## Scope

Re-open SOURCES row S169 (`corpus/SOURCES.md` line 181; drafted by a3w1 seat
`SrcHyprctlInstance`, report `.ufo/waves/round-25/a3w1/reports/SrcHyprctlInstance.md`):
fresh fetch of the row's URL, sha256/byte-count check against the row's anchor
cell, verbatim check of every located quote at its stated line, and an audit of
the row's `teaches` cell against the fetched bytes.

Row under test:

```
| S169 | Hyprland v0.56.2 hyprctl client — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/hyprctl/src/main.cpp | code | A | CLI instance selection, instance inventory, and IPC socket path for the C1 oracle readback | hyprctl/src/main.cpp:81-90,100-161,222-235,351-379,427-520,577-579 @ efb50993780079460b0cbed1363e2166a2de1d9f; sha256:f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f; 17168 B | Shows instance discovery and PID filtering, signature or numeric `-i` selection, environment fallback, and runtime-directory/signature socket construction | mined | 2026-10-23 | on-release | corpus/knowledge/bind-table-r25.md |
```

## Fresh fetch and anchor check

Command:

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/reopen && timeout 60 curl -fsSL --max-time 50 \
  -o /fast/scratch/hyaku/mado-r25a3/reopen/S169.bin \
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/hyprctl/src/main.cpp \
  && /usr/bin/sha256sum /fast/scratch/hyaku/mado-r25a3/reopen/S169.bin && /usr/bin/wc -c /fast/scratch/hyaku/mado-r25a3/reopen/S169.bin
```

Output:

```
f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f  /fast/scratch/hyaku/mado-r25a3/reopen/S169.bin
17168 /fast/scratch/hyaku/mado-r25a3/reopen/S169.bin
```

- sha256 `f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f` — **matches** the anchor cell.
- Byte count `17168` — **matches** the anchor cell.
- Content identity vs the a3w1 retained artifact: `.ufo/waves/round-25/fetch/a3w1/SrcHyprctlInstance.bin`
  hashes to the same `f6b0d1fc…c93f`, so today's fetch is byte-identical to the seat's.
- Line count 583 (`wc -l` on identical bytes), matching the seat's report.

## Located-quote check

Whitespace-collapsed-substring check (Python `str.split`-join on both quote and
line; quote must be a substring of the stated line). Result per quote, plus the
set of all lines containing each quote:

| stated line | quote (collapsed) | at stated line | lines containing |
|---|---|---|---|
| `main.cpp:89`  | `return std::string{XDG} + "/hypr";` | True | [89] |
| `main.cpp:157` | `std::erase_if(result, [](const auto& el) { return kill(el.pid, 0) != 0 && errno == ESRCH; });` | True | [157] |
| `main.cpp:510` | `instanceSignature = INSTANCES[INSTANCENO].id;` | True | [510] |
| `main.cpp:230` | `std::string socketPath = getRuntimeDir() + "/" + instanceSignature + "/.socket.sock";` | True | [230] |

All four quotes are verbatim at their stated lines and are the only occurrences
of each string in the file. The seat's own claim ("all four checks returned
True") reproduces under an independent recheck.

## `teaches` cell audit

`teaches` cell: "Shows instance discovery and PID filtering, signature or
numeric `-i` selection, environment fallback, and runtime-directory/signature
socket construction." Each clause verified directly in the fetched bytes:

- **instance discovery** — `instances()` at 141–161 iterates
  `getRuntimeDir()`; `parseInstance` at 100–139 requires `hyprland.lock`,
  parses line 1 as PID and line 2 as `wlSocket`, and rejects malformed records
  (extra non-empty line rejected at 134–135).
- **PID filtering** — line 157 `erase_if` drops entries where
  `kill(pid, 0) != 0 && errno == ESRCH`; line 159 sorts by `SInstanceData::time`
  ascending.
- **signature or numeric `-i` selection** — `-i`/`--instance` consume the next
  arg into `overrideInstance` at 429–436; at 493–510 `overrideInstance.contains("_")`
  → used as signature, else `isNumber` check + `stoi` + bounds check
  (`< 0 || >= size()` → `no such instance`, returns 1) + `INSTANCES[INSTANCENO].id`.
- **environment fallback** — at 511–519, with no override the client reads
  `HYPRLAND_INSTANCE_SIGNATURE` and exits 1 if unset. `instances` is
  HIS-independent: comment at 482, early return at 483–486, before the
  signature/fallback block.
- **runtime-directory/signature socket construction** — `getRuntimeDir()` at
  81–90 returns `$XDG_RUNTIME_DIR/hypr` or falls back to `/run/user/<uid>/hypr`
  (86–87); `request()` builds `<rtdir>/<signature>/.socket.sock` at 230 and
  `connect()`s at 234. Unhandled ordinary requests route to `request()` at the
  main-dispatch `else` block, lines 577–579.

Every clause is grounded; nothing in the cell overclaims. The anchor cell's
cited ranges (81-90, 100-161, 222-235, 351-379, 427-520, 577-579) each exist
and contain the relevant code — including 351–379 (`instancesRequest` text/JSON
output of id, time, pid, wl_socket) that grounds the seat's listing-output
claim. The seat's secondary findings (zero-based numeric index, timestamp-ascending
sort before indexing at line 159, negative/out-of-range → `no such instance`)
all check out against the bytes.

## Bounds and tooling

- No lane files modified other than this report; fetch written only to
  `/fast/scratch/hyaku/mado-r25a3/reopen/S169.bin`.
- No installs or updates; used stock `curl`, `sha256sum`, `wc`, `python3`.
- No hyprctl verbs, no compositor or counter interaction, no git/jj writes.

## Verdict

REOPEN S169: agree
