# RevengerCache — R48 w1: why xdg-terminal-exec's cache is built the way it is

Seat: `RevengerCache` (round 48, w1 BUILD, leaf). Target: reverse-engineer the *intent* of the resolver cache in
`xdg-terminal-exec` v0.14.3, say which invalidation gaps are known/accepted upstream, and scope the C1 warm-cache
contract from that.

**Verdict.** The cache is a deliberately content-blind, one-command shortcut. Its author's stated trade is: hash the
*listing* of everything relevant in one `ls -LRl` call, never read a file, and accept invalidation sensitivity
(false invalidation) as the price. The cache file's content is trusted once the hash matches and the cached command
name resolves; that is the whole validation. Consequently the upstream *known and accepted* gaps are: unrelated app
churn invalidating the cache (accepted, named), a `/disable_cache` line being ignored while a valid cache exists
(accepted, documented), and apps that change the default terminal without touching a list file (issue closed, no
change, default stays on). The gaps this seat measures but upstream never discusses are the metadata blind spots —
same-size edits inside one displayed minute, whole-day resolution for files older than six months, `PATH` identity,
and entry-level conditions (`TryExec`, `Categories`) that the warm path never re-checks. For C1 that means the tool
must reproduce *the resolver's* verdict, not an idealized one: `disabled` is what the resolver concludes, and with a
valid cache in place the resolver never reads the lists at all.

Pin under study: `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (verified equal to `/usr/bin/xdg-terminal-exec`
this run), upstream tag **v0.14.3** = commit `065925df9f419008159258ae169018bfd23df71b` (2026-07-29), which is also
upstream `HEAD` (0 commits after the tag). README in the same fetch dir: sha256
`c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40` = `v0.14.3:README.md`.

## 1. Method and provenance

- Upstream history read from a full clone in scratch (`git clone https://github.com/Vladimir-csp/xdg-terminal-exec`,
  237 commits, .git 396K) and pinned by full SHA in `receipts/upstream-history.txt`: commit bodies, tag containment
  (`git describe --tags --contains`), and the per-tag value of the cache-format literal.
- Design discussion read through the GitHub API at 2026-10-26 and frozen into `receipts/issues-flattened.txt`
  (issue #36 "Cache", #47, #64, PR #43 with its comments; raw JSON kept beside it).
- Behaviour checked against the real pinned script with `--print-cmd` only, `XDG_CACHE_HOME` in scratch, in four
  probes (`probes/*.sh`, outputs in `receipts/`). No terminal was launched; no host cache was read, written or
  deleted; no compositor verb, no pacman.
- Every quote in this report is ≤25 words and carries a computed `file:line`; `python3 verify-quotes.py` re-reads
  each cited line and re-checks the substring and its ≤25-word bound — **39/39 verified** this run.

## 2. Timeline (commit-pinned; full SHAs in `receipts/upstream-history.txt`)

| when | commit | what it settled | first release |
|---|---|---|---|
| 2023-11-30 | `080c5ec896d5d20755fd23c8332ba37e40569d00` "working cache" | `read_cache`/`save_cache` appear; `gen_cache` becomes `gen_hash` | v0.9.0 |
| 2023-11-30 | `520535c4bb2cb9e993f41ee8ce2daa3ee422c4c1` "save cmd late, invalidate cache by missing cmd early" | 4th header line = the command name; validity gains `command -v` | v0.9.0 |
| 2023-11-30 | `64ca1e8a47e10e1f5ac26492dc479dcbf39cbafe` "drop cache on missing command" | first attempt: delete the cache when the launch target is missing (later superseded — no such block survives in v0.14.3) | v0.9.0 |
| 2023-12-01 | `a2ef630fa623ab041b2940e3dc3660d37d4675c5` "Cache tweaks, stricter entry IDs from configs" | cache save is **forked**: "fork save_cache" | v0.9.0 |
| 2023-12-05 | `aae04a3705aa4663a6d0ddafbe5b39328098fdde` "Add XDG_CURRENT_DESKTOP to cache" | the desktop name enters the hash stream | v0.9.0 |
| 2023-12-08 | `d8b7a31590717200e7213c2ead021b5cca1162a2` "improve debug, comments" | records *why md5*: `.ufo/waves/round-47/fetch/xdg-terminal-exec:181` | v0.9.0 |
| 2023-12-12 | `05c46a912a8d8a1da87b79724bef52484f604829` "set umask when saving cache" | the cache is written under `umask 0077` | v0.9.0 |
| 2023-12-18 | `a09da6999c269bc7145232ed299f14dbace34a4b` "Document cache behavior caveat" | #47 resolved as documentation, not code | v0.9.0 |
| 2024-06-11 | `0913e283d2d396bc87718438969a70ff6528b0ae` "Enable cache by default, closes #36" | default flips to on | **v0.10.0** |
| 2024-10-06 | `ce0a03b765a7c51529c3d33376c3d6fa96f183e6` "String escape expander and Exec tokenizer" | cache-format literal `3`, 50-line limit, `RSEP END_OF_EXEC_USEP` terminator | v0.12.0 (~3 commits later) |
| 2025-06-07 | `6d64ac1479ed2fce0060a90ce88538490362eae4` "Implement scripting options" | literal `3`→`4`; `entry_path`/`entry_id`/`entry_action` cached | **v0.13.0** |
| 2026-07-29 | `e0577b639d9bbf8d9c03f6024b0a463789827694` "fix: Avoid locale-dependent pattern matching (#76)" | `gen_hash` re-invokes itself under `LC_ALL=C` | **v0.14.3** |

The cache-format literal by tag (computed, `receipts/upstream-history.txt`): `none` for v0.9.0–v0.11.1, `3` for
v0.12.0–v0.12.4, `4` for v0.13.0 through v0.14.3.

Canonical URLs (tag/commit, never a branch):

- tag: <https://github.com/Vladimir-csp/xdg-terminal-exec/tree/v0.14.3> (commit `065925df…`)
- cache introduction: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/080c5ec896d5d20755fd23c8332ba37e40569d00>
- validity gains `command -v`: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/520535c4bb2cb9e993f41ee8ce2daa3ee422c4c1>
- background save: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/a2ef630fa623ab041b2940e3dc3660d37d4675c5>
- `XDG_CURRENT_DESKTOP` in the key: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/aae04a3705aa4663a6d0ddafbe5b39328098fdde>
- md5 rationale: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/d8b7a31590717200e7213c2ead021b5cca1162a2>
- `umask 0077`: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/05c46a912a8d8a1da87b79724bef52484f604829>
- #47 documentation: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/a09da6999c269bc7145232ed299f14dbace34a4b>
- default on: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/0913e283d2d396bc87718438969a70ff6528b0ae>
- format literal `3` + 50-line limit + terminator: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/ce0a03b765a7c51529c3d33376c3d6fa96f183e6>
- literal `4` + scripted fields: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/6d64ac1479ed2fce0060a90ce88538490362eae4>
- `LC_ALL=C` for the hash: <https://github.com/Vladimir-csp/xdg-terminal-exec/commit/e0577b639d9bbf8d9c03f6024b0a463789827694>
- design thread: <https://github.com/Vladimir-csp/xdg-terminal-exec/issues/36>, <https://github.com/Vladimir-csp/xdg-terminal-exec/issues/47>, <https://github.com/Vladimir-csp/xdg-terminal-exec/issues/64>, <https://github.com/Vladimir-csp/xdg-terminal-exec/pull/43>, <https://github.com/Vladimir-csp/xdg-terminal-exec/pull/76>

## 3. The intent, decision by decision

Each decision below is stated with the evidence that fixes it; "why" quotations are the author's own words in the
design thread, not inference.

**D1 — a cache exists because the hotkey had to be fast, and the cost was accepted as one file plus one listing.**
The thread opens with the goal: "Speed up things by caching selected" `Exec`, `ExecArg`
(`receipts/issues-flattened.txt:3`). README states the cost model exactly: it caches "for fast read at a cost of
reading one file" (`.ufo/waves/round-47/fetch/README.md:297-298`). Measured on this host, same filesystem, 300 synthetic
entries: warm hit median **5.5 ms**, cold median **14.5 ms**, ratio **2.6x** (`receipts/latency-300.txt`). At 3
entries the ratio is 1.0x — the cache pays off in proportion to tree size, which is why the fixture must be large
enough for the measurement to mean anything.

**D2 — the key is a *listing*, not content, on purpose: no file is ever read to validate.**
The rejected alternative was per-entry checksums; the author's objection is that it would "actually read files. Both
when creating and checking the cache." (`receipts/issues-flattened.txt:108`), and that a checksum cannot see a *new*
terminal. The chosen invariant is stated as: this way it is "content-agnostic and does not read any files" — and the counter-argument is conceded in the
same paragraph, "In order to differentiate entries of terminals, one has to read them."
(`receipts/issues-flattened.txt:113`). A single `ls -LRl` over all operands is the mechanism, justified as being "done
in a single call for everything" (`receipts/issues-flattened.txt:115`).

**D3 — false invalidation is the accepted cost; false validation was not on the table.**
"In order to differentiate entries…" above is followed by the author's own risk statement: the method "is quite
sensitive and may be prone to false positives" (`receipts/issues-flattened.txt:113`), and he names the two plausible
ones — "installation/removal/upgrade of unrelated apps" and "generation of new entries, i.e. by a browser"
(`receipts/issues-flattened.txt:117-118`). The design therefore *intends* to err toward re-resolving. What it does not
budget for is the opposite error (a real change the listing cannot show); see §6.

**D4 — md5, explicitly not for security.** "md5 is 4x faster than sha*, and there is no need for cryptography here"
(`.ufo/waves/round-47/fetch/xdg-terminal-exec:181`, introduced by `d8b7a31`). The consequence is load-bearing for C1:
the hash is a *cache key*, not an integrity check, and the file's content is trusted once the key matches.

**D5 — `XDG_CURRENT_DESKTOP` is part of the key because it selects which list files are read.**
Added by `aae04a3` right after the first design round: the config list contains per-desktop filenames
(`<desktop>-xdg-terminals.list`), so the same trees can yield a different answer under a different desktop name.

**D6 — the format literal is a manual invalidation lever, not a migration mechanism.**
The line is commented "cache 'version', change to invalidate when format changes"
(`.ufo/waves/round-47/fetch/xdg-terminal-exec:193`). It entered the stream in `ce0a03b` as `3`, and was bumped to `4`
by `6d64ac1` in the same change that started caching `entry_path`/`entry_id`/`entry_action` for the scripting options.
Because the literal is *inside* the hashed stream, a format change invalidates by arithmetic — every old cache's line 1
simply stops matching. (It is not a version *check*: nothing compares the literal separately.)

**D7 — the warm path is engineered to bail out early.** `read_cache` "tries to bail out as soon as possible if
something does not fit" (`.ufo/waves/round-47/fetch/xdg-terminal-exec:220`): file must exist, the command section must stay under
line 50 (i.e. a cache is at most 49 lines), the terminator must appear, then `gen_hash`, then `command -v` of the
cached command name. Every one of those is a cheap negative.

**D8 — the cache is written after the answer is produced, and out of the caller's way.**
`saves or removes cache, forked out of the way` (`.ufo/waves/round-47/fetch/xdg-terminal-exec:1456`), from `a2ef630`
whose subject is "fork save_cache". Measured lag parent-exit → cache visible: **1-2 ms** over five runs
(`receipts/save-lag.txt`). Two consequences for C1: the judge must *wait* for the background write (a poll with a
bound), and the writer is a child that survives the caller's exit.

**D9 — the cache is parsed, never sourced, and written private.** The suggestion to `source` the file was answered by
keeping a strict read loop: "Source is to be considered, but currently cache read is a rather strict and fail-early
type of algorithm." (`receipts/issues-flattened.txt:195`; the mock-up author had himself offered to change `source`ing
"to `read` loop", `receipts/issues-flattened.txt:210`). The write is wrapped in `umask 0077` (`05c46a9`; pin
`:319-320`). The
alternative cache design (PR #43, still open, never merged) was rejected on exactly the D1 axis: the maintainer notes
that with it "exec line is read directly from the cache" only in the *current* design
(`receipts/issues-flattened.txt:218`), i.e. the current one avoids the entry read altogether.

**D10 — on by default, for unattended fastness.** `0913e28` flips the default, deleting the line "The plan is to
eventually enable it by default for unattended fastness." and changing `CACHE_ENABLED=${XTE_CACHE_ENABLED-false}` to
`...-true}` (`receipts/diff-0913e28-readme.txt:29,44-45`; v0.14.3 still reads
`XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}` at pin `:1172`). This is the decision that makes the warm path the
*normal* path on this host, and hence makes C1 a real gap rather than an edge case.

**D11 — the key is locale-independent by construction (only since v0.14.3).** `e0577b6` (PR #76) wraps `gen_hash` in a
self re-invocation under `LC_ALL=C`, alongside the same treatment for `read_config_paths`, `read_entry_path` and
`find -L`: "Run code dealing with character ranges in `LC_ALL=C` context."
(`receipts/upstream-history.txt:67`). Reason: under `tr_TR.UTF-8` collation the ASCII `i` did not sort inside `a-z`,
making ids containing `i` undiscoverable. For C1 this is not cosmetic — the tool must compute the hash under `LC_ALL=C`
regardless of the caller's locale, or it will "disagree" with the resolver on a host with a non-C locale.

**D12 — validity is hash *plus* resolvability, and only of the command name.** `520535c` added
`command -v "$xte__cached_cmd"` to the validity test to catch an uninstalled terminal cheaply. It is a *name*
resolution check: the earlier, stronger idea of dropping the cache when the launch target turns out missing
(`64ca1e8`) does not survive in v0.14.3 — grep finds no such block in the pin.

## 4. What upstream documents as the contract

- The man page states the invalidation rule in one clause: the cache is used "until changes are detected in the
  listing of Desktop Entry files" or config files, and is "enabled by default"
  (`.ufo/waves/round-47/fetch/xdg-terminal-exec.1.scd:110`). That is precisely the listing-only promise of D2.
- The v0.14.3 README's `### Cache` section is `README.md:295-319`; it states the payoff: "Valid cache bypasses" reading of any other file
  (`.ufo/waves/round-47/fetch/README.md:300`; sentence continues on `:301`).
- README states the one caveat upstream admits in prose: if the cache was enabled only by a truthy env value, "the
  script will not know that the cache is" disabled until the file is removed, something invalidates it, or a falsy run
  happens (`.ufo/waves/round-47/fetch/README.md:315`).
- The pin restates the reasoning in a comment above the read gate: "Editing config to disable cache should invalidate
  the cache." (`.ufo/waves/round-47/fetch/xdg-terminal-exec:1171`). That sentence is the *assumption* that §5 K1
  breaks.

## 5. Known and accepted upstream gaps

| # | gap | evidence | status upstream |
|---|---|---|---|
| K1 | `/disable_cache` in a list file is invisible while a valid cache exists: the cache is read first, so the list is never parsed | issue #47 "Cache can end up being used even when disabled in" (`receipts/issues-flattened.txt:224`); README caveat (`README.md:315`); reproduced this run, `receipts/warm-divergence.txt` class 5 (`cache is actual`, file kept) | **accepted**: resolved as "4. document this behavior" (`receipts/issues-flattened.txt:247`), code unchanged (`a09da69`) |
| K2 | false invalidation on unrelated app install/removal or browser-generated entries | `receipts/issues-flattened.txt:117-118` | **accepted, named**; not fixed, argued as rare versus terminal launches |
| K3 | apps that change the default terminal without touching a list file do not invalidate the cache (GNOME Terminal / Ptyxis "set as default" buttons) | issue #64: "that won't work unless the apps explicitly clear the cache" (`receipts/issues-flattened.txt:265`) | **closed without code change**; maintainer answer was that a default-terminal change is a config change and should invalidate (`receipts/issues-flattened.txt:276`); the env default is still `true` in v0.14.3 (pin `:1172`) |
| K4 | anyone who can write the cache can redirect the hotkey: content is trusted, and the checked field (line 2) is not the executed field (line 11) | round-47 `w2/RevengerCache.md` §4 H2 (forgery fixtures), not re-run here | **never discussed upstream**; [INFERENCE] consistent with a same-user threat model, but not stated anywhere I found |
| K5 | an old cache with a different format is invalidated only if its literal differs; format versions before v0.12.0 were unversioned (`none` for v0.9.0-v0.11.1) | `receipts/upstream-history.txt` per-tag table | **accepted**: structural checks (line count, terminator) are the pre-versioning fallback (pin `:229-252`) |

## 6. Gaps the design cannot see, that upstream never discusses

These are mechanism facts, each with a probe receipt; upstream's silence is silence, not consent.

| # | gap | why the code cannot see it | receipt |
|---|---|---|---|
| G1 | a **same-size content edit with the mtime minute unchanged** leaves the hash identical, so a warm run answers from the stale cache | the stream carries name, size and mtime only (pin `:200`); an edit inside the displayed minute with equal byte count is invisible | `receipts/hash-blindness.txt` (a: IDENTICAL), `receipts/warm-divergence.txt` class 1 (warm `termA --flag`, cold `termC --flag`) |
| G2 | for a file **older than ~6 months**, `ls -l` prints only the year, so the resolution degrades from minutes to **whole days** | `ls` date format switches to `Mon dd  YYYY`; a same-day, same-size edit is invisible | `receipts/hash-blindness.txt` (c: same-minute IDENTICAL; d: same-day-old IDENTICAL; e: month change CHANGED) |
| G3 | `PATH` is not in the key; only *name* resolution is re-checked, so the same name resolving to a different binary is accepted | validity is `command -v` of line 2 (pin `:274`); ordering and identity are not compared | `receipts/warm-divergence.txt` class 7: primed under one dir, run under another, `cache is actual` and identical stdout. **Not a C1 fixture class** — the cached field is the name, so a different binary with the same name cannot change stdout |
| G4 | entry-level conditions are not re-checked on a hit: removing a `TryExec` stub (or changing `Categories`, `ShowIn`, the entry file itself within G1) changes the cold answer and not the warm one | the warm path never opens the entry; `command -v` covers only `exec[0]` | `receipts/warm-divergence.txt` class 2: warm `termA --flag` (stub gone), cold `termB --flag` |
| G5 | a **hit never rewrites** the cache, and a **stale/invalid cache is not deleted** on read | `save_cache` only runs `if [ "$XTE__CACHE_USED" = "false" ]` (pin `:1455`); the failure branches `debug` and return (pin `:287-295`) | `receipts/warm-divergence.txt` class 3 (mtime unchanged across a warm run) |
| G6 | `XTE_CACHE_ENABLED=false` **deletes** the file, while `/disable_cache` in a list does **not** (K1) — two different "disabled" meanings | `save_cache` removes the file when the feature is off (pin `:336-337`), and never runs on a hit | `receipts/warm-divergence.txt` classes 4 and 5 |

## 7. What this fixes for the C1 contract

Scoping only — the L1 freezes the predicates; these are the consequences of the intent above that a warm-cache tool
either honours or silently mispredicts.

1. **`disabled` must mean what the resolver concludes, not what the configs say.** With a valid cache present the
   resolver reports `cache is actual` and never parses `/disable_cache` (K1, G6). A tool that scans configs first and
   labels the run `disabled` would disagree with the pin on exactly the fixture where the cache is warm. Into the
   `explain` line, `cache=disabled` should therefore only arise when `check_bool` on the effective
   `XTE_CACHE_ENABLED` is false (env, or the directive on a run that actually reached the cold path) — and on a hit
   the verdict is `hit`, full stop.
2. **`stale` and `invalid` are behaviourally identical, and both leave the file alone.** Parse failure (no terminator,
   a 50th line) and hash mismatch both fall through to the cold path; neither deletes the file, neither changes stdout
   versus "absent". They differ only in the debug line (`:287` vs `:291` vs `:295`). The fixture schema should keep
   them distinct for diagnosis, but the judge must not expect an observable difference.
3. **The hash stream is exact and locale-fixed.** Line 1 = md5 of: `4`, then `$XDG_CURRENT_DESKTOP` (empty line if
   unset), then `LANG=C ls -LRl` over the colon-split `XTE__CONFIGS:XTE__APPLICATIONS_DIRS` operands with stderr
   dropped — computed under `LC_ALL=C` (D11) and hashed over the literal bytes, including `ls`'s own trailing newlines.
   Note `echo` for the first two lines versus `ls`'s own output: the emulation must not "normalise" either.
4. **The emulation must reproduce `ls` quirks, not an idealized listing.** Measured this run
   (`receipts/ls-shape.txt`): `-L` renders a broken symlink as `l????????? ? ?     ?      ?            ? <name>`; the
   `total` line is the sum of `st_blocks` in KiB (it changes from `total 8` to `total 4` when `-L` cannot stat, and
   doubles under `POSIXLY_CORRECT`); operands are listed files-first then directories, each alphabetically; directory
   headers echo the operand spelling verbatim (`.../o/../d:`), so `./` and `..` survive into the hash; a nonexistent
   operand contributes nothing after `2>/dev/null`; and `ls`'s exit status is irrelevant because only stdout is
   hashed (a broken symlink makes `ls` exit 1 and the resolver still accepts the hash).
5. **The cache's line map is part of the contract** (pin `:229-252`): 1 hash, 2 command name, 3 entry path, 4 entry id,
   5 entry action, 6 exec arg, 7 app-id arg, 8 title arg, 9 dir arg, 10 hold arg, then the command as
   `$XTE__USEP`-separated words concatenated with newlines and terminated by `$XTE__RSEP` + `END_OF_EXEC_USEP`.
   A command containing newlines legitimately spans several lines; the tool must reconstruct exactly as `read_cache`
   does. Args 6-10 are cached *names* (e.g. `--title`), which is why a CLI `--title=`/`--dir=` value still applies on
   a warm run — that is the third fixture class in the claim, not a counter-example.
6. **The tool must predict the save but never perform it.** Save runs only on a cold-path run that reaches argument
   composition (pin `:1455`), from a forked child (D8), under `umask 0077`, and *removes* the file when the feature is
   off. For the judge this means: prime with a cold `--print-cmd`, then **poll for the file** (measured 1-2 ms after
   parent exit; a bounded poll, not a sleep), then apply the mutations, then compare.
7. **The fixture schema needs the mtime pin it already has** — and needs it *twice*: after materialisation and again
   after `after.files` edits, or `ls` will render a fresh date and the warm answer will diverge for the wrong reason.
   Same for `TZ`: `ls` renders local time, so the cold and warm runs must share the environment's zone (the emulator
   must not convert to UTC).
8. **`HOME` unset is conditional, and the pin's own failure mode is the model.** With `HOME` *and* `XDG_*` unset the
   pin dies under `set -u` at its first `${HOME}` default: rc 1, **0-byte** stdout, stderr
   `xdg-terminal-exec: line 148: HOME: unbound variable` (`receipts/warm-divergence.txt` class 6). With `XDG_CONFIG_HOME`,
   `XDG_DATA_HOME`, `XDG_DATA_DIRS` and `XDG_CACHE_HOME` set, unsetting `HOME` alone is harmless (rc 0, 13-byte
   stdout). Round-47's D1 wording ("pin exit 1, empty stdout") is correct only for the sandbox's unset-XDG shape; the
   tool must key on the same condition the pin keys on, i.e. whether a `${HOME}` default ever gets expanded.
9. **`command -v` in the sandbox is PATH-only, over the fixture's exec dirs** — the tool must resolve a *name* to
   "exists and is executable", not to a path, and must not treat a resolvable name as proof that the cached command is
   the one a cold run would have picked (G3). When the name stops resolving the resolver simply re-resolves —
   `cache is out-of-date`, cold path, no message about the cache (`receipts/warm-divergence.txt` class 8).

## 8. Confidence and what was not established

- **High**: the timeline and rationale (§2, §3) — full SHAs from a clone, subject lines and bodies re-read, tag
  containment computed. The pin's own semantics (§4, §6) — each gap is either a code path re-read or a probe against
  the real binary.
- **Medium**: the "accepted" readings of upstream *silence* (K2-K5, G1-G4). The threads show what was discussed; I
  found no upstream statement about same-minute resolution, PATH identity, or entry-level re-checks. I mark those as
  never-discussed rather than tolerated-by-design.
- **Not established**: (a) numeric uid/gid rendering inside the counter's bwrap sandbox — my probes ran where passwd
  resolves, so the "numeric when no passwd entry" branch is unexercised here and needs the executor's own receipt;
  (b) whether any distro patches the cache logic (no distro patch file inspected); (c) the real host tree's hash on a
  non-C locale (round-47 w2 recomputed the host hash; this seat did not re-run it); (d) latency numbers are this host
  plus scratch filesystem, not a universal ratio.

## 9. Reproduce

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/RevengerCache
python3 verify-quotes.py                       # 39/39 verified, re-reads every cited line
sh probes/probe-hash-blindness.sh              # G1, G2 -> receipts/hash-blindness.txt
sh probes/probe-warm-divergence.sh             # warm vs cold, classes 1-8 -> receipts/warm-divergence.txt
sh probes/probe-ls-shape.sh                    # ls emission quirks -> receipts/ls-shape.txt
sh probes/probe-latency.sh                     # 300-entry warm/cold -> receipts/latency-300.txt
```

Upstream history: `git clone https://github.com/Vladimir-csp/xdg-terminal-exec`,
`git log -1 --format='%H %ad %s' <sha>` and `git describe --tags --contains <sha>`; the dumped output is
`receipts/upstream-history.txt`, the design thread is `receipts/issues-flattened.txt` with its raw JSON beside it.

Safety of this seat: read-only on the host. `xdg-terminal-exec` ran only with `--print-cmd`, always with
`XDG_CACHE_HOME` inside `/fast/scratch/hyaku/mado-r48/RevengerCache`; the host's `~/.cache/xdg-terminal-exec` was
neither read nor written; no terminal, compositor verb, pacman, input injection, git/jj mutation, subagent or
background job. Scratch was removed after the receipts were copied here. No tool was installed or upgraded.
