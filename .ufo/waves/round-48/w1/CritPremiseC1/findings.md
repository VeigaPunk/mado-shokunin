# CritPremiseC1 — Falsify C1's premise before the freeze (round 48, w1)

Seat: `CritPremiseC1` (leaf; no subagents). Target: `.ufo/waves/round-48/claims.md` C1 (lines 12-21).
Assigned questions: (Q1) is the warm-cache path *new executed ground* vs the round-47 cache text; (Q2) can a warm
answer really differ from a cold one on this resolver (build the cheapest such case and run it); (Q3) is
stale-but-valid reachable on a real host (mtime minute resolution, editors that keep size); (Q4) which do-nothing
or cheap tool could reach a warm target (trust-every-well-formed-cache; shell-out).

## Verdict

The C1 premise **holds** on the phenomena it asserts (warm answers can and do differ from cold ones; the stale-but-valid
mechanism is real and host-reachable), but the draft fixture mechanics *as written* cannot produce those phenomena:
**(F2)** priming inside the judge's bwrap sandbox silently never writes the cache (`--die-with-parent` kills the
backgrounded `save_cache`), and **(F3)** a cache primed on the host never validates inside the sandbox (hash input
formatting differs: resolved names vs numeric uid/gid). Both are fixable and must be frozen into the schema, or every
warm fixture degenerates to a cold run and C1 becomes vacuous. Q1: yes — *for the tool/instrument* (nothing executes the
warm path today); the resolver's cache *mechanism* is already documented. Q4: both cheap classes fail the full matrix
only if the counter keeps strace clause `r` on warm runs and the fixture mix is discriminative.

---

## F1 — warm ≠ cold is real, and the cheapest case is a same-size list swap (Q2)

Measured twice: on the host, and inside the counter's exact bwrap sandbox.

Cheapest case (host, tree under scratch): `conf/xdg-terminals.list` holds `TermA.desktop\nTermB.desktop\n`; two valid
entries `TermA.desktop`/`TermB.desktop` in `data/applications` (Exec stub `termA`/`termB` on PATH). Run 1 (cold):
`--print-cmd` → `termA`, rc 0, and the background `save_cache` writes `$XDG_CACHE_HOME/xdg-terminal-exec`. Then swap the
two list lines *in place* (identical byte length) and re-pin all mtimes (`touch -d @1700000000`). The `ls -LRl` input to
`gen_hash` is byte-identical before/after (receipts `ls-before.txt`/`ls-after.txt`, 304 bytes each, `cmp` equal) and the
reconstructed md5 is unchanged. Now: warm run (cache present) prints `termA`; cold run (fresh cache dir) prints `termB`.
Same happens inside the bwrap sandbox once the cache is seeded correctly (receipts `sb-warm-hit-num-out.txt`,
`sb-warm-stale-num-out.txt`, `sb-cold-num-out.txt`): warm-hit `TermA.desktop … termA`, warm-stale still
`TermA.desktop … termA`, cold `TermB.desktop … termB`, rc 0 everywhere. With an unchanged tree, warm == cold
(`prime-out.txt` == `warm-out.txt`).

This confirms the claim's mechanism end-to-end (xdg-terminal-exec:272-274 trust gate; :1450-1458 background save) and that
the warm answer *can* differ from the cold answer on this resolver.

## F2 — priming inside the judge's sandbox is impossible (harness mechanics)

The counter's oracle runs use `bwrap --unshare-all --die-with-parent …` (`quality/counters/c1-r47-terminal.py:139`).
`save_cache "$1" &` (xdg-terminal-exec:1457) forks a background child; when the main script exits, bwrap tears the
namespace down and kills it **before it writes** — so a cold `--print-cmd` oracle run inside the sandbox leaves **no**
cache file (receipt `bwrap-oracle-cache.txt`: `exists=no size=NA`; matrix `bwrap-bg-matrix.txt`: A with `--die-with-parent`
→ no file, B without → cache written 175 bytes mode 600, C host control → written). The draft schema's “prime: a cold run
before the scored run; wait for the background save to finish” therefore cannot run inside the graded sandbox; the warm run
would read nothing and all warm fixtures silently become cold.

Fix (smallest): prime *outside* the graded run — a host run of the pinned script with a scratch `XDG_CACHE_HOME` produces
authentic cache bytes (`prime-cache.txt`), or the counter synthesizes them (see F3) — then place that file at
`<root>/.rw/cache/xdg-terminal-exec` before the warm oracle run. Warm runs never rewrite it (`CACHE_USED=true`, so the
seeded file stays stable across a fixture's warm runs). Also relevant for the tool model: the write side is never visible
to the tool, so the tool never needs to emulate `save_cache` output — only the read/trust side.

## F3 — a host-primed cache never validates inside the sandbox: numeric vs resolved ids (Q3 adjacent, schema-critical)

`gen_hash` hashes `ls -LRl` output (xdg-terminal-exec:200). Inside the counter's sandbox there is no `/etc/passwd`, so
`ls` prints **numeric** uid/gid (`1000 1000`), while on the host the same files print resolved names (`vgpnk vgpnk`).
Measured: host-style reconstructed hash for the fixture tree `b83835631d261ca9f7cfbed0fd445b3f`; in-sandbox numeric
listing hash `00b8e5c594576c750556c1499dda5724` (receipts `sandbox-host-hash.txt`, `sandbox-num-hash.txt`). A cache
seeded with the host hash is read and rejected (`invalid cache data`/out-of-date in `debug-warm-hit-err.txt`), and the
oracle falls back to cold. With the hash computed from the in-sandbox listing, the warm hit, the stale-but-valid hit, and
the cold control all behave exactly as on the host (F1 receipts).

Fix options: (a) the counter computes seed hashes from an in-sandbox-style listing (numeric ids are deterministic: the
sandbox maps the fixture files to uid/gid 1000), or (b) bind a minimal `/etc/passwd` (e.g. `vgpnk:x:1000:1000:…`) into
the sandbox so host and sandbox listings coincide — but that changes clause-i's allowlist and must be frozen explicitly.
Without one of these, *any* primed warm fixture is untestable.

## F4 — the byte-exact `ls -LRl` emulation: measured shape (informs the tool's hard part)

Ground truth from tracing the resolver's own `ls` child (`strace-execve.txt`, execve argv):
- Operand order = config-list *files* (six slots, preference order) then applications *directories* **with trailing `/`**
  (`usr-share/applications/`, `data/applications/` — the debug `paths:` line confirms the trailing slashes). Missing paths
  produce stderr-only errors, dropped; only existing operands contribute.
- GNU `ls` prints non-directory operands first (bare long lines), then directory operands in operand order, each with a
  `<path>:` header and `total N` block line (N = Σ st_blocks/2, filesystem-dependent; both oracle/tool trees are
  materialized on the same FS).
- Within a directory listing, entries are sorted by name (C locale), **files and subdirectories interleaved by name** — the
  “files-then-dirs” phrasing in the draft contract holds at the *operand* level, not inside a directory; recursion visits
  subdirs in that sorted order after the parent's listing.
- Column widths (size / uid / gid) are computed **per listing block**; C-locale dates: `Mon dd HH:MM` for recent files,
  `Mon dd  YYYY` for old ones (year) — both observed. Numeric ids in the sandbox (F3). `total 0` on empty dirs.
- `-L` follows symlinks; a dangling symlink operand reports to stderr (dropped) and contributes no stdout line.

This is the genuinely hard part the claim names, and the fixtures (`mtime` epoch pinning) make it deterministic: the
`total` block count is the one host/FS-dependent byte and must be produced by the real host `ls` (copy of `/usr/bin/ls`)
in the sandbox, never hardcoded.

## F5 — cheap-tool analysis (Q4)

- **Shell-out tool** (runs the real pinned script, or `ls`/`md5sum`) would trivially match every warm and cold output.
  It is defeated only by clause `r`'s strace trip rule (`c1-r47-terminal.py:46-49,174-195`): any `execve/execveat/
  socket/…` after the sandboxed python3 starts is a trip → `readonly=fail`. **The freeze must keep clause `r` and apply it
  to the warm fixtures too**; output-only judging would admit the cheater.
- **Trust-every-well-formed-cache tool** (parse the cache, skip hashing) passes all warm-hit fixtures but fails every
  stale/invalid/disabled fixture where the resolver falls back to cold — so those classes must be present and must
  *differ* in output (invalid/stale → cold answer; the F1 fixture gives that).
- **Do-nothing (cold-only) tool** fails every warm-differ fixture, so the warm-differ class is the one that forces real
  work; a fixture set made mostly of warm-hit cases discriminates nothing.
- The *only* full-matrix implementation is the full emulation (F4 + parse + trust gate); no stdlib shortcut avoids the
  `ls` byte-exactness because freshness is decided solely by that md5.

## F6 — stale-but-valid reachability on a real host (Q3)

Ordinary in-place editing is enough: same-size replacement (e.g. `sed -i` with an equal-length substitution, or vim
keeping size) within one wall-clock minute leaves `ls -l`'s minute-resolution stamp unchanged, so `gen_hash` input is
identical. Measured: `minute-probe.txt` (same `ls -l` line before/after, content changed `AAAA`→`BBBB`, size 4 both).
The schema's `mtime` pinning is therefore an optional determinism aid, not a necessity for host reachability.

## F7 — small facts worth freezing into the contract wording

- Terminator byte is **0x1e** (`\x1eEND_OF_EXEC_USEP`), *not* 0x1f (USEP) (xdg-terminal-exec:250-251; cache bytes in
  `prime-cache.txt`). A seed using 0x1f yields `invalid cache data` (first version of this seat's seed did).
- Valid cache shape: 10 header lines (hash, cmd, entry path, id, action, execarg, appidarg, titlearg, dirarg, holdarg)
  + the exec-USEP line with the terminator appended on the same line; max 49 lines (line-number 50 is rejected, xdg-terminal-exec:239-242). Mode 0600 (`umask 0077`, xdg-terminal-exec:319-321).
- The cached entry path keeps the `/./` find marker (line 3 in `prime-cache.txt`) — `save_cache` stores
  `XTE__ENTRY_PATH` unmodified; only `--print-path` strips it at print time (xdg-terminal-exec:1340-1343).
- `--print-cmd` and `--test` reach `save_cache` (xdg-terminal-exec:1455-1458); `--print-id`, `--print-path`,
  `--print-content` alone exit earlier (xdg-terminal-exec:1376-1384) and never write a cache.
- Disabled via `XTE_CACHE_ENABLED=false` works in the sandbox (cold answer; receipt `disabled-out.txt`) but the cache
  *removal* side of `save_cache` (xdg-terminal-exec:336-338) is also lost to the background-kill (F2) — harmless for a
  single scored run, relevant if a fixture tree is reused across runs.
- D1 HOME-unset reproduced: exit 1, empty stdout, stderr `HOME: unbound variable` at xdg-terminal-exec:148 (receipt
  `homeunset2-out.txt`); note XDG_* must also be unset to trigger it.

## Q1 — is it new executed ground?

Yes, for the instrument: `tools/mado-terminal.py:82-85` declares the cache out of contract; no shipped tool executes the
warm path. The resolver's *mechanism* is already documented (`corpus/knowledge/xdg-terminal-selection-r47.md:25` —
“sourced; out of the C1 contract”, cache section lines 41-43, and line 83's “two runs disagreeing … cache” hint), and
`corpus/README.md:110` lists the warm-cache path as still open. The claim's wording (“At base the tool models a cold cache
only …”, “Surface moved: the cache edge class, frontier → core”) is accurate; novelty is execution, not discovery.

## Smallest safe corrections to the claim wording

1. Replace the priming description with: *“prime outside the graded run (host run with a scratch XDG_CACHE_HOME, or
   counter-synthesized cache bytes per the numeric in-sandbox listing), then place the cache at `<root>/.rw/cache/
   xdg-terminal-exec` before the warm oracle run; never rely on the sandboxed resolver writing its own cache (the
   backgrounded `save_cache` is killed at bwrap teardown).”*
2. Require the seeded hash to be computed from the *in-sandbox* `ls` formatting (numeric uid/gid) — or amend clause `i`
   to bind a minimal passwd mapping — otherwise no warm fixture can hit.
3. State that discriminative fixtures must cover, with *differing* expected output: stale-but-valid (same-size mutation),
   out-of-date (hash or `command -v` fail), invalid parse, disabled (env and directive), absent — warm-hit alone
   discriminates nothing.
4. Keep clause `r` (strace trips) on warm tool runs; note that output-only judging would admit a shell-out implementation.
5. Precision edits: terminator byte 0x1e; `--print-cmd` and `--test` write the cache, `--print-id/--print-path/
   --print-content` never do; cache mode 0600; the cached entry path retains `/./`.

## Evidence

All receipts in this seat dir `receipts/` (copied from scratch; paths inside receipts are scratch paths by design and are
not citable as values — re-run the drivers in the seat's scratch to regenerate): `prime-cache.txt`, `prime-out.txt`,
`warm-out.txt`, `warm-after-mut-out.txt`, `cold-after-mut-out.txt`, `hash-before.txt`, `hash-after.txt`, `ls-before.txt`,
`ls-after.txt`, `ls-cmp.txt`, `sandbox-host-hash.txt`, `sandbox-num-hash.txt`, `sb-num-postmut-hash.txt`,
`sb-warm-hit-num-out.txt`, `sb-warm-stale-num-out.txt`, `sb-cold-num-out.txt`, `bwrap-oracle-cache.txt`,
`bwrap-bg-matrix.txt`, `disabled-out.txt`, `homeunset2-out.txt`, `minute-probe.txt`, `strace-execve.txt`,
`debug-warm-hit-err.txt`.

Safety: no lane/fleet writes outside this seat dir and the Report; no pacman, no terminal/GUI launch (the pin ran only with
`--print-*` and scratch `XDG_CACHE_HOME`), no compositor verbs, no git/jj mutation, no tool installs (only `cp` of the
seven externals into scratch for bwrap runs).
