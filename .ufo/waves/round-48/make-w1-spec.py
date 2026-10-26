#!/usr/bin/env python3
"""Generates .ufo/waves/round-48/w1-spec.json (round 48, wave w1 = BUILD, policy v1, band 32-64).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
w1 builds and probes; nothing is frozen yet, no seat scores a frozen counter. The L1 freezes after w1 returns;
wave w2 (falsify) attacks the frozen instruments.
"""
import collections
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-48"
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
R47TIP = "d40189c924e01dc1cbe290474eb4256d343590d4"
R47DATA = "0c69960510bcd30705d222873cd9b860aa9329ba"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r48"
XKB = "https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/"
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls "
    "concurrently in large batches. Do not serialize what can run in "
    "parallel. Do not output philosophical reasoning or verbose plans. Act "
    "directly via tool calls.\n\n")

CONTEXT = """# Goal
mado round 48 (hyaku run 9, 2026-10-26), wave w1 = BUILD (policy v1). Lane repo: %(L)s (desktop and compositor craft: the Hyprland/waybar/
walker/terminal config plane of this host; axes coverage + operability). Base (lane tip at round start) %(B)s. Nothing is frozen yet: the L1 freezes
the predicates AFTER this wave returns, and a second wave w2 attacks the frozen instruments. Your output feeds that freeze.
Declared claims: %(W)s/claims.md (read it first).
- C1 operability (capability acquisition): extend the landed read-only tool %(L)s/tools/mado-terminal.py (round 47; selftest 43/43; models a COLD
  cache only, cache out of contract at tools/mado-terminal.py:82-85) to the WARM-CACHE path of xdg-terminal-exec v0.14.3 (host /usr/bin/xdg-terminal-exec,
  sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac = pin %(L)s/.ufo/waves/round-47/fetch/xdg-terminal-exec). The resolver reads
  $XDG_CACHE_HOME/xdg-terminal-exec (default $HOME/.cache) BEFORE reading any list or entry (script :1179), parses it (:217-298: <=49 lines, line 11+
  until the 0x1e"END_OF_EXEC_USEP" terminator), and trusts it iff gen_hash (:179-215: md5 of "4\\n$XDG_CURRENT_DESKTOP\\n" + `LC_ALL=C LANG=C ls -LRl`
  of the colon-split XTE__CONFIGS:XTE__APPLICATIONS_DIRS operands, stderr dropped) equals line 1 AND `command -v <line 2>` succeeds; then the print
  modes use the cached entry id/path/action/exec/arg values. Only a cold run that reaches :1455 (print-cmd or a launch) writes the cache, in the
  BACKGROUND (`save_cache "$1" &`). Draft contract for the extended tool: `print`, `explain` and `--observed` keep their round-47 meaning, but now
  with the cache file that exists in the environment honoured exactly as the resolver honours it (hit / out-of-date / invalid / disabled via
  XTE_CACHE_ENABLED or /disable_cache), so `print` reproduces the resolver's stdout+exit status with a warm cache too; `explain` reports
  `cache=<absent|hit|stale|invalid|disabled>` in its MADO_TERM line; HOME unset is modelled as the pin does (round-47 closure D1: pin exit 1, empty
  stdout); still Python 3 stdlib only, NO process, NO socket, writes nothing (it never writes the cache the resolver would save).
  The emulation of `LANG=C ls -LRl` (operand sorting files-then-dirs, `total` lines, column widths, mode strings, nlink, numeric uid/gid when no
  passwd entry resolves, sizes, C-locale dates: recent "Mon dd HH:MM" vs old "Mon dd  YYYY", recursion headers, -L symlink following) is the hard
  part: it must be byte-exact to the md5, inside the counter's sandbox (bwrap, no /etc visible, so ls prints numeric ids).
  The JUDGE is the real pinned script: the C1 counter primes it (a cold `--print-cmd` run, then wait for the background save), applies a fixture's
  post-prime mutations, runs it again and requires the tool's stdout+rc to equal that warm run, on fixtures where the warm answer DIFFERS from the
  cold one (edits that keep size and mtime minute, a removed TryExec stub while exec[0] still resolves, changed --dir/--title args applied over cached
  arg names, ...) and fixtures where the cache is invalidated or malformed (mtime/size/name/dir change, XDG_CURRENT_DESKTOP change, exec[0] gone,
  missing terminator, line limit, bad hash).
- C2 coverage (sourced): a new knowledge entry %(L)s/corpus/knowledge/xkb-keymap-compile-r48.md: which kb_rules/kb_model/kb_layout/kb_variant/kb_options
  names compile on this host (libxkbcommon 1.13.2, xkeyboard-config 2.48): RMLVO rules -> KcCGST components, the include-path order
  ($XDG_CONFIG_HOME/xkb, $HOME/.xkb, /etc/xkb, then the xkeyboard-config root), which unknown names fail the compile (layout, variant, rules: exit 1
  "Couldn't find file symbols/zz", "Couldn't process include statement for 'br(nope)'") and which are dropped with a warning (unknown option: XKB-595
  "Unrecognized RMLVO option ... was ignored", rc 0; unknown model: rc 0), multi-layout variant alignment, and how a failed compile maps onto Hyprland
  0.56.2's fallback to `us` (held: corpus/knowledge/hyprland-input-devices-r46.md step 4, rows S318/S319 - cite, never re-claim). New SOURCES rows S340..
  (registry 276 rows, tops at S339). Ground open at base: hyprland-input-devices-r46.md:69 ("The XKB compile itself is not reproduced"), README :112.
  A live READ-ONLY receipt: `xkbcli compile-keymap` (/usr/bin/xkbcli; /usr/lib/xkbcommon/xkbcli-compile-keymap) for the host's names
  (kb_layout = br, kb_options = compose:caps; ~/.config/hypr/input.conf) - it compiles a keymap to stdout and touches no compositor.
Host facts (L1, 2026-10-26): libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1 installed; `xkbcli compile-keymap --layout br --options compose:caps`
  rc 0; `--layout zz` rc 1; `--layout br --variant nope` rc 1; `--layout br --options nope:nope` rc 0 + XKB-595 warning; `--layout br --model nope` rc 0;
  `--rules nope --layout br` rc 1. include paths searched: /usr/share/xkeyboard-config-2 (three user paths could not be added: absent).
Fixture schema v2 (DRAFT interface for C1; the L1 freezes the final form): the round-47 schema (read the docstring of
  %(L)s/quality/counters/c1-r47-terminal.py and %(L)s/quality/counters/c1-r47-fixtures.json: id, class, env with $ROOT, files, exec, args, expect)
  plus optional "mtime" (epoch seconds applied to every materialized file and dir, so ls dates are deterministic), "prime": {"args": [...]}
  (a cold run before the scored run; wait for the background save to finish), "after": {"files": {"<path>": "<text>" | null}, "exec_add": [...],
  "exec_remove": [...], "env": {...}, "mtime": <epoch>} (mutations applied after priming, then mtimes re-pinned), "cache": "<literal cache text, $ROOT
  substituted>" (for malformed caches; no priming). `expect` is ALWAYS produced by running the real pinned script (never typed), 3 identical runs.
Routed round-47 closure items (%(L)s/corpus/lessons/round-47-verifier-spotcheck.md section 6): D1 (contract narrowed after freeze: lesson line +
  HOME unset modelled), D2 (session-material number without receipt), D3 (readdir-order blind spot: two valid candidates in one dir), D4 (erratum:
  xdg-terminal-selection-r47.md Limits cites terminal-route-r17.md:150-151, text sits at :149-150), R3 (session-material synthetic marker: drafts
  %(L)s/.ufo/waves/round-47/w1/ExecSessionMarker/, attacked by round-47 w2 MutSessionMarker/RevSessionMarker if present), R4b (round-45 errata in a
  form that keeps the frozen round-45 counter verdict: %(L)s/.ufo/waves/round-47/w2/ExecErrataR45.md H1), M47-10 (fixture schema v2: H1/H2 cases,
  %(L)s/.ufo/waves/round-47/w2/ExecC1Diff.md), %(L)s/.ufo/waves/round-47/w2/CritC1Explain.md (explain cmd= not compared), w2/SentC1Sandbox.md F1-F4.
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin outside the lane), sibling lanes, templates/, scripts/,
  MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout (READ-ONLY; never run a campaign tool there), or the lane's jj/git
  index. Never run mutating git/jj in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus your Report file. Never edit an existing tracked file; the L1 is
  the only integrator. Write your Report file FIRST (a short status), then refine it; a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>.
- SCRATCH (operator directive 2026-10-25): every clone, venv, build, fixture tree and work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it
  explicitly as TMPDIR/--work/dir=, never rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB AND bound every loop and
  every write (round-47 incident: a seat streamed ~590 GB into a FIFO-named path; never `yes`, never an unbounded redirect, never write into a FIFO or
  device; cap generated files at 1 MB); copy receipts into your seat dir first, then delete your scratch dir before you finish
  (`trap 'rm -rf -- "$S"' EXIT`). A /tmp or scratch path is never citable evidence. Committed code must honour TMPDIR / --work, never hardcode /tmp.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input
  injection, never launch a terminal or any GUI program. xdg-terminal-exec may be run ONLY with a --print-* option (never without one: that launches
  a terminal) and ONLY with XDG_CACHE_HOME pointing into your scratch dir. Never touch the host's real ~/.cache/xdg-terminal-exec (read it only if a
  task says so; never write or delete it). xkbcli: only `compile-keymap` / `dump-keymap` style read verbs writing to stdout, never `interactive-*`.
  Allowed compositor reads: `hyprctl version`, `hyprctl ... -j` read verbs; NEVER `dispatch`, `keyword`, `reload`, `setprop`, `switchxkblayout`,
  `--batch`, `output`, `plugin`, `kill`. Host config trees (~/.config, ~/.local/share) and binaries are READ-ONLY. Session material stays shape-only:
  never commit window titles, monitor serials/descriptions, input-device names beyond what a task asks, process tables or home listings.
- Git fixtures (run-6 incident): any fixture repo is `D=$(mktemp -d -p %(S)s/<YourSeatName>)` then `git -C "$D" init -q` (or `git clone -q --shared
  %(L)s "$D"`), every later git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the first commit; never
  `git commit` with a throwaway identity anywhere else.
- Tooling authorization (operator, 2026-10-19): you and every seat may install/upgrade tools that help the task - read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20):
  ALL pacman transactions are PAUSED host-wide until the operator resolves the host-recovery L0 question - use uv tool / uv pip into a scratch venv /
  npx / an official binary in ~/.local/bin; never -Sy, -Syu, -U, -R, a downgrade, or a restart of a host service.
- Seat tool state: your tools start at the fleet root, not the lane: use absolute paths everywhere.
- You are a leaf: no subagent dispatch, no background jobs, no spawning (an executor MAY spawn one read-only labrat probe).
- Every finding names what it attacks or supports (a path:line, a command and its output, or a hash). Never fabricate: an unrun check has not passed.
  Quotes lifted from a source are <= 25 words, located (file:line), and verified by a script that greps your receipt; locators are computed
  (grep -n), never typed. Pins you fetch go to your seat dir with their sha256 and the URL they came from (tag or commit URLs, never a branch).
"""


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(B)s", BASE), ("%(R47T)s", R47TIP), ("%(R47D)s", R47DATA),
                 ("%(P)s", PKG), ("%(S)s", SCR), ("%(XKB)s", XKB)):
        t = t.replace(k, v)
    return t


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({
        "name": name, "role": role,
        "prompt": sub(GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() + "\n")})


XKB = "https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/"

# ------------------------------------------------------------ executors (17)
seat("ExecRefCacheA", "executor",
     "C1 reference A: warm-cache path in a copy of tools/mado-terminal.py (draft at your seat dir, never at the tracked path).",
     """Copy %(L)s/tools/mado-terminal.py to %(W)s/w1/ExecRefCacheA/mado-terminal.py and extend it per the draft contract in the context: read_cache
(:217-298), gen_hash (:179-215) with a byte-exact Python emulation of `LC_ALL=C LANG=C ls -LRl <operands>` (no process!), the `command -v` check
of line 2, cache-enable rules (XTE_CACHE_ENABLED, /enable_cache, /disable_cache - note the directives are read only on the cold path), and the print
composition from cached values; HOME unset as the pin. Keep the round-47 selftest passing and add >= 12 warm-cache selftest cases. Self-check against
the REAL script on >= 60 warm cases you build (prime with a cold --print-cmd run in a sandbox/env with XDG_CACHE_HOME in your scratch, wait for the
background save, mutate, run again; bwrap like the round-47 counter so ls sees no /etc). Write receipts/agree.txt (case, ours, theirs) and report
every disagreement with the script lines and every ls edge class you had to handle.""")
seat("ExecRefCacheB", "executor",
     "C1 reference B: an independent warm-cache implementation (do not read ExecRefCacheA's files).",
     """Independently of any other seat, implement the warm-cache path as a standalone module %(W)s/w1/ExecRefCacheB/warmcache.py exposing
ls_lRL(operands) -> bytes, gen_hash(desktop, configs, appdirs) -> str, read_cache(path) -> parsed|reason, and a patch of a copy of
%(L)s/tools/mado-terminal.py at %(W)s/w1/ExecRefCacheB/mado-terminal.py. Prove gen_hash against the real script by priming caches (the hash is line 1
of the saved cache) on >= 80 random trees (random names, sizes, nested subdirs, symlinks to files and dirs, empty dirs, missing operands, old and
recent mtimes) inside bwrap without /etc. receipts/hash-agree.txt (tree seed, ours, theirs). Report each ls behaviour that surprised you.""")
seat("ExecLsEmu", "executor",
     "The hard core of C1: a byte-exact Python emulation of GNU `LC_ALL=C LANG=C ls -LRl a b c 2>/dev/null` with no process.",
     """Write %(W)s/w1/ExecLsEmu/lsemu.py (stdlib only, function ls_lRL(operands, now=None) -> bytes) and a differential fuzzer
%(W)s/w1/ExecLsEmu/fuzz.py that compares it against the host's /usr/bin/ls (GNU coreutils; record `ls --version`) on >= 2000 random trees, both on the
host and inside a bwrap root without /etc (numeric ids). Cover: operand order (non-existent operands dropped with stderr; files listed first, sorted,
then each dir block "name:" header, "total N" in 1K blocks rounded up, the blank line between blocks), column width alignment per block (nlink, owner,
group, size; major,minor for devices), mode strings incl. setuid/sticky, -L symlink following (dangling link inside a dir prints a `l?????????` line?
verify), directory loops ("not listing already-listed directory"), recent vs old dates (6-month rule, future mtimes), names with spaces/unicode/
newline (quoting when not a tty), sorting in C locale. Write receipts/fuzz.txt (N cases, mismatches, seeds) and a table of edge classes with
'emulated exactly' or 'declare out of contract' and why.""")
seat("ExecOracleV2", "executor",
     "C1 judge harness for warm cases: prime the pinned script, wait for the background save, mutate, re-run - deterministically, in bwrap.",
     """Starting from the oracle code in %(L)s/quality/counters/c1-r47-terminal.py (clause i sandbox), write %(W)s/w1/ExecOracleV2/oracle2.py that
materializes a fixture-v2 case (context schema: mtime, prime, after, cache), runs the pin to prime (find out how to wait for `save_cache "$1" &`:
with --unshare-pid the background job may die when the script exits - run `sh -c '<pin> ...; wait'` or poll for the file; prove which works), applies
`after` with mtimes re-pinned (dirs too), runs the scored warm run, and returns stdout/rc plus the cache bytes before and after. Show: 3 identical
runs per case on >= 30 cases; two roots give identical results after $ROOT substitution (the hash includes path names in ls headers - does a
different root change the hash? it must: then the tool tree must be primed separately or the cache rewritten; decide and prove the scheme that lets
the tool see an equivalent cache at its own root). Receipts and the exact bwrap argv in your report.""")
seat("ExecFixturesV2", "executor",
     "C1 fixture set v2: warm-divergent, warm-invalidated, malformed-cache, HOME-unset, readdir-order (D3) and H1/H2 (M47-10) classes.",
     """Build %(W)s/w1/ExecFixturesV2/fixtures-v2.json (schema v2 in the context) with >= 120 NEW cases and their `expect` from 3 runs of the pin (use
ExecOracleV2's approach or your own priming harness in bwrap; record which): classes WARM-HIT-DIFFERS (warm stdout != cold stdout: same-size same-
minute Exec edit, TryExec stub removed while exec[0] resolves, list file edited same size/minute, --dir/--title/--app-id/--hold args over cached
arg names, XTE_EXECARG_COMPAT changed, entry deleted?? (deletion changes the listing -> invalid; prove)), WARM-INVALID (mtime/size/name changes in
config and data dirs, subdir added, XDG_CURRENT_DESKTOP changed, XDG_DATA_DIRS changed, exec[0] stub removed, cache disabled by env), MALFORMED
(no terminator, 50-line limit, terminator at line 11 vs later, empty hash, extra bytes after terminator, wrong field count), HOME-UNSET, READDIR
(two valid candidates in one application dir whose winner depends on readdir order; record the expected order and the filesystem), H1 (-type f binds
to the first application dir only), H2 (`command -v -p` exits 0; option-like Exec/TryExec words). For every warm case also record the COLD answer
(same tree, no cache) so the L1 can count how many warm cases differ from cold. Report class counts and the differ count.""")
seat("ExecGenWarm", "executor",
     "C1 clause g v2: a nonce generator of warm-cache cases judged by the pin at count time.",
     """Read gen_case() in %(L)s/quality/counters/c1-r47-terminal.py and write %(W)s/w1/ExecGenWarm/gen_warm.py: gen_warm_case(rng) producing a v2
case (prime + random after-mutations drawn so that about half keep the hash and about half break it; random malformed caches). Run 300 generated
cases against the pin 3x for determinism (receipts/determinism.txt) and against the round-47 tool (cold-only) to show how many it misses
(receipts/base-tool-miss.txt). Report the hit/stale/invalid mix.""")
seat("ExecCounterC1", "executor",
     "C1 counter draft quality/counters/c1-r48-terminal-cache.py (at your seat dir), from the round-47 counter.",
     """Copy %(L)s/quality/counters/c1-r47-terminal.py to %(W)s/w1/ExecCounterC1/c1-r48-terminal-cache.py and extend: fixture schema v2 (prime/after/
cache/mtime) with oracle and tool on separate trees, a warm clause (fixtures of class WARM-* and MALFORMED) and keep the round-47 cold clause on the
round-47 fixture file (harm watch, unchanged), clause x compares cmd= too (round-47 w2/CritC1Explain.md) and the new cache= field against the oracle's
actual behaviour (did the warm run use the cache? derive it from the oracle: e.g. cache file bytes before == after AND output != cold, or a debug
trace with XTE_DEBUG? find the script's debug switch and use it only for the oracle), clause g with warm generated cases, the tool's sandbox gains
read access to the case cache file only. Fix the counter-wording findings F1-F4 of %(L)s/.ufo/waves/round-47/w2/SentC1Sandbox.md. Final line
`PRED-C1-r48: cold=K/F warm=W/V explained=X/T generated=G/N selftest=.. readonly=.. tool=.. verdict=..`. Run it against the round-47 tool at %(B)s
(must MISS: warm cases) and against ExecRefCacheA's draft if it exists when you finish. Receipts.""")
seat("ExecCounterC2", "executor",
     "C2 counter draft quality/counters/c2-r48-xkb-entry.py (at your seat dir), from the round-47 C2 counter.",
     """Copy %(L)s/quality/counters/c2-r47-terminal-entry.py to %(W)s/w1/ExecCounterC2/c2-r48-xkb-entry.py and adapt it to the C2 entry
corpus/knowledge/xkb-keymap-compile-r48.md: a entry new at REV; b provenance head with >= 3 `source: S###` >= S340, rows mined/opened 2026-10-26/
used-by the entry; c every cited row pin-bound (copy under .ufo/waves/round-48/fetch/, digest equal; tag or commit URL, no branch); d every quote
verbatim inside its pin at its stated range; e >= 6 numbered steps with a source locator each; f a committed live receipt of `xkbcli compile-keymap`
(receipt names the xkbcli/libxkbcommon version, the RMLVO names, rc, and the sha256 of the keymap text) that agrees with the entry's host sentence,
plus >= 3 negative probes (unknown layout rc 1, unknown variant rc 1, unknown option rc 0 with the warning) whose rc the entry states; g one README
index row; h the held rows S318/S319 and the round-46 entry byte-equal to base; i census terms (pick terms absent under corpus/ at %(B)s, e.g.
`xkb_keymap_new_from_names`, `XKB-595`, `compile-keymap`, `xkeyboard-config-2`; prove git grep exit 1 at base) >= 2 present at REV. Never run any lane
tool. Build controls: POS minimal entry-only tree admitted; BASE, QUOTE, BRANCH, HELD, RECEIPT-absent, RECEIPT-contradicts, NOSTEPS, RANGE, PIN
rejected each on its clause. Receipts.""")
seat("ExecControlsC1", "executor",
     "C1 controls: cheap tools that skip the claimed work must MISS the C1 counter draft.",
     """Build %(W)s/w1/ExecControlsC1/controls/ (each a full tools/mado-terminal.py variant) and a runner run-controls.py that runs ExecCounterC1's
draft (when present; else the fixture-v2 file with your own pin-judged loop) on each: BASE (round-47 tool, cold only), TRUST-ANY (uses any well-formed
cache whose line 2 resolves, no hash), HASH-NAMES (hash over names only, no ls -l columns), HASH-NO-DATE, HASH-NO-TOTAL, ALWAYS-COLD-BUT-HOME,
CACHE-IGNORES-ENABLE (ignores XTE_CACHE_ENABLED=false), NO-LINE-LIMIT, DELEGATE-LS (calls /usr/bin/ls via subprocess: tripwire), MD5-SUBPROC,
EXPLAIN-CACHE-CONST (cache=hit always), and one-rule-undone mutants of ExecRefCacheA's draft. Every control must MISS; report which clause catches
each and any control that MEETS (that is a fixture gap: propose the fixture that kills it).""")
seat("ExecXkbLive", "executor",
     "C2 live receipt: read-only xkbcli compile matrix on this host.",
     """Write %(W)s/w1/ExecXkbLive/probe.sh (bounded, read-only) and receipts/xkb-live.txt: `xkbcli --version`/libxkbcommon version, the host names
from ~/.config/hypr/input.conf (only the kb_* values), `xkbcli compile-keymap --layout br --options compose:caps` rc + sha256 of the keymap text +
line count; negative matrix: unknown layout, unknown variant, unknown option, unknown model, unknown rules, two layouts with one variant (`us,br`
`,abnt2`), more variants than layouts, a layout:variant pair valid in another layout, an option group that exists (grp:alts_toggle), the commented
`us,dk,eu` + `intl` lines of input.conf; record rc and the first XKB-### code of stderr each. Then include paths: with XDG_CONFIG_HOME and HOME pointed
at a scratch dir holding xkb/symbols/mado48 (a tiny valid symbols file), show `--layout mado48` compiles only through that path, and record
`--include`/`--include-defaults` behaviour. Also capture `hyprctl devices -j` keyboards' layout/variant/options/active_keymap (no device names in the
committed receipt: replace names by kbd1..n).""")
seat("ExecXkbSource", "executor",
     "C2 sources: pin libxkbcommon 1.13.2 and xkeyboard-config 2.48 files and locate the lines behind each behaviour.",
     """Fetch (tag URLs only) the libxkbcommon xkbcommon-1.13.2 files that implement: RMLVO rules matching and the 'Unrecognized RMLVO option ... was
ignored' warning (XKB-595), the default include paths and their order (context.c / context-priv.c / the XKB_CONFIG_ROOT, XKB_CONFIG_EXTRA_PATH env),
the failure on a missing symbols file or section (XKB-338, XKB-661, 'Failed to compile keymap'), and xkb_keymap_new_from_names; plus the
xkeyboard-config 2.48 rules (gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config tag xkeyboard-config-2.48: rules/base.xml.in or the generated
evdev.xml? find what the host's /usr/share/xkeyboard-config-2/rules/evdev is built from) and symbols/br. Base URL hint: %(XKB)s. Save pins under
%(W)s/w1/ExecXkbSource/fetch/ with sha256 and URL, compare host files byte-for-byte where the host ships them, and write located.md: behaviour ->
file:line -> <=25-word quote, verified by a script (verify.sh) that greps the pins.""")
seat("ExecHomeUnset", "executor",
     "Round-47 closure D1: HOME unset, FIFO entries and other refusals - pin behaviour vs the landed tool.",
     """Run the pin and %(L)s/tools/mado-terminal.py side by side (sandboxed, XDG_CACHE_HOME in scratch) on: HOME unset with and without XDG_* set,
HOME empty, a FIFO named *.desktop in a later application dir (BOUNDED: never write into it; give the pin a 10 s timeout), symlink loops, an
unreadable entry. Record pin rc/stdout, tool rc/stdout. Draft the D1 lesson line (the delta between the frozen round-47 reference
%(L)s/.ufo/waves/round-47/l1-draft/mado-terminal.py docstring and the landed docstring) and the round-48 contract text: which of these the round-48 tool
models like the pin and which stay declared out of contract. Receipts.""")
seat("ExecSessionMarker", "executor",
     "Routed R3: install the synthetic-material marker for quality/check-session-material.py - final bytes, shown able to fail both ways.",
     """Read %(L)s/quality/check-session-material.py, the round-47 drafts %(L)s/.ufo/waves/round-47/w1/ExecSessionMarker* and any round-47 w2 attack
on them (MutSessionMarker, RevSessionMarker, if present), and the round-46 drafts named there. Deliver in %(W)s/w1/ExecSessionMarker/: the exact
new file contents to land (gate patch and/or marker registry), a run at %(B)s on a scratch clone (`git clone -q --shared`) with and without the marker,
receipts showing (a) synthetic fixture material marked -> not counted, (b) the same bytes unmarked -> counted (fails), (c) a real-looking value under a
forged marker in a non-fixture path -> still counted, (d) findings count before/after naming the revision. Never print a serial or other session value.""")
seat("ExecD2Receipt", "executor",
     "Routed D2: the round-47 report's 'findings=128 at the tip (115 at base)' has no receipt.",
     """Run %(L)s/quality/check-session-material.py (read-only; see its usage) at %(R47T)s, at the round-47 base 60edb66e2f1cb90acc6e9442fc93ded0ca42d750
and at %(B)s, on scratch clones if it needs a worktree. Write receipts naming the revision and the exact command, and a one-paragraph correction
line for the round-48 report if 128/115 do not reproduce. Never print the matched values (counts and classes only).""")
seat("ExecErrataR45", "executor",
     "Routed R4b: the round-45 errata in a form that keeps the frozen round-45 counter's verdict.",
     """Read %(L)s/.ufo/waves/round-47/w2/ExecErrataR45.md (H1: the drafted block drops the entry out of PRED-C2-r45) and its scripts. Produce
%(W)s/w1/ExecErrataR45/block.md: an append-only erratum block for corpus/knowledge/hyprland-monitor-rule-r45.md carrying all six confirmed
corrections, worded so the frozen round-45 counters still print TARGET_MET. Prove it on a scratch clone: append, commit there (fixture identity, -C
the clone only), run the round-45 C2 counter(s) named in the round-45 registration at that commit -> receipts showing MET before and after, plus the
round-48 locator check of every line the block cites.""")
seat("ExecIdGuard", "executor",
     "Assimilation id guard + quarantine slice for round 48 (scratch in the wave dir).",
     """Run the id-collision commands of the round prompt section 10 exactly (A=%(W)s/assimilation; registry %(L)s/corpus/SOURCES.md; staged
%(P)s/SOURCES.append.md) -> reg-ids, staged-ids, collisions; prove the guard once on a scratch registry with an indented `  | S002 |` row that the
staged set collides with (nonempty collisions). Then the quarantine slice with the awk command of section 10 on
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md -> %(W)s/assimilation/quarantine-slice. Report counts and
whether any staged entry in %(P)s/knowledge/ touches XKB, keymaps, xkbcommon or the terminal cache (grep, list hits).""")
seat("ExecAxisBase", "executor",
     "Base receipts of the lane's published axis table.",
     """Run `cd %(L)s && python3 -I quality/check-axis-scores.py --rev %(B)s --repo .` and each instrument it names, on a scratch clone if needed;
write %(W)s/w1/ExecAxisBase/receipts/axis-base.txt with exit codes and the summary lines. Also run the round-47 C1 and C2 counters at %(B)s (they
must still print TARGET_MET there: harm-watch baseline; --work under your scratch) and record the output.""")

# ------------------------------------------------------------ scouts (4)
seat("ScoutHyprKeymap", "scout",
     "C2: how Hyprland 0.56.2 (efb5099) builds its keymap through libxkbcommon.",
     """In hyprwm/Hyprland at commit efb50993780079460b0cbed1363e2166a2de1d9f (the host's build; `hyprctl version`), find where the xkb_context is
created (flags: default includes? XKB_CONTEXT_NO_ENVIRONMENT_NAMES?), how the five names reach xkb_keymap_new_from_names (or _names2), the error
path, and whether XKB_CONFIG_ROOT / XDG_CONFIG_HOME include paths apply to the compositor (so a ~/.config/xkb layout would work in Hyprland).
Commit-pinned raw URLs, line numbers computed, <=25-word quotes. Note which lines rows S318/S319 already hold (%(L)s/corpus/SOURCES.md) so the entry
cites held rows rather than duplicating them. Write %(W)s/w1/ScoutHyprKeymap/report.md.""")
seat("ScoutXkbSpecs", "scout",
     "C2 source candidates: libxkbcommon docs, xkeyboard-config registry, rules format.",
     """Open and evaluate candidate sources for the C2 entry: libxkbcommon doc/rules-format.md and doc/user-configuration.md at tag
xkbcommon-1.13.2, the xkbcli-compile-keymap man page (host /usr/share/man), xkeyboard-config 2.48 rules (base.xml / evdev.xml registry entry for
br and the compose:caps option), the xkeyboard-config README on rules, the Arch wiki 'X keyboard extension' (English channel only). For each: URL
(tag/commit), access date 2026-10-26, a <=25-word located quote, recommended tier and scope, or a reject with reason (generic, duplicate, branch-only,
localized channel). Write %(W)s/w1/ScoutXkbSpecs/report.md with draft rows in the registry's 11-column format (see %(L)s/corpus/SOURCES.md header).""")
seat("ScoutShokuknow", "scout",
     "Assimilation scan: does %(P)s hold a theme for this round's planes (XKB/keymap, terminal cache)?",
     """Read %(P)s/MERGE-REPORT.md and list %(P)s/knowledge/; name any staged entry on XKB, keymaps, input methods, xdg-terminal-exec or its cache,
with its cited rows, and say admit-candidate or refuse (PROVINCE.md scope, held ground). Also list the latest-dated considerthese proposals in
%(L)s/considerthese/2026-10-26.md that are still unimplemented at %(B)s (proposal 2 was refused in round 47, proposal 3 landed as QUALITY 90 in
round 46; check 1, 4, 5, 6 against the lane: e.g. quality/ratio-domain-meta.py, quality/check-session-material.py). Write
%(W)s/w1/ScoutShokuknow/report.md.""")
seat("ScoutHeld", "scout",
     "Held-ground check for both claims at %(B)s.",
     """(1) C1: quote what the lane already holds about the resolver cache - %(L)s/corpus/knowledge/xdg-terminal-selection-r47.md (cache section),
terminal-route-r17.md:123-127, tools/mado-terminal.py:82-85 - so the C1 claim does not re-claim held statements; list what is documentary there and
what is new executed ground for a warm-cache tool. (2) C2: git grep at %(B)s under corpus/ for xkb_keymap_new_from_names, XKB-595, XKB-338,
compile-keymap, xkeyboard-config-2, rules/evdev, include path -> show exit codes; quote every held XKB sentence (hyprland-input-devices-r46.md,
idle-lock-plane.md, keybind-rule-semantics.md). Write %(W)s/w1/ScoutHeld/report.md.""")

# ------------------------------------------------------------ scribes (10)
seat("ScrEntry", "scribe",
     "C2 entry draft corpus/knowledge/xkb-keymap-compile-r48.md (at your seat dir).",
     """Draft %(W)s/w1/ScrEntry/xkb-keymap-compile-r48.md in the shape of %(L)s/corpus/knowledge/hyprland-input-devices-r46.md (head: title, source:
lines S340.. with a scope each, verified-at, recheck, ground; a question table; numbered steps each with a file:line locator; OBS lines with located
quotes; host section; decision table 'symptom -> cause -> check'; Limits with [UNK]). Use the facts in the context; fetch the libxkbcommon 1.13.2
sources yourself (tag URLs) to locate lines; use <S340>.. placeholders for row ids and <LIVE> only for values the L1 fills from the committed
xkbcli receipt. Cite held rows S318/S319 for Hyprland's fallback; do not restate the round-46 steps.""")
seat("ScrRows", "scribe",
     "C2 SOURCES rows S340.. and their Gate lines.",
     """Open each source the C2 entry will cite (libxkbcommon 1.13.2 files and docs, xkeyboard-config 2.48 rules/symbols, Hyprland files only if not
held) and draft %(W)s/w1/ScrRows/rows.md: registry rows in the 11-column format of %(L)s/corpus/SOURCES.md (status mined, opened 2026-10-26, recheck a
valid ISO date / NNd / symbolic cadence, used-by the entry, no `|` inside any cell) and gate-lines.md (one Gate line per row: URL, access date,
<=25-word located quote) plus >= 2 rejected candidates with reason and flip condition. Check every URL against the registry for duplicates (census
W04/E04) and list them.""")
seat("ScrLesson", "scribe",
     "Round-48 lesson skeleton corpus/lessons/round-48.md.",
     """Draft %(W)s/w1/ScrLesson/round-48.md in the shape of %(L)s/corpus/lessons/round-47.md: ## Gate (candidates, admitted, rejected with reasons,
census before -> after with <AFTER> marks, renumber map if any, id-guard and quarantine results, considerthese verdict, the D1 delta line),
## Mistakes (leave slots for ScrMistakes), ## Spot-check (pending non-author). Census before: %(W)s/receipts/census-before.txt.""")
seat("ScrMistakes", "scribe",
     "Mine mistakes: round-47 closure D1-D4 and any earlier unmined class.",
     """Read %(L)s/corpus/lessons/round-47-verifier-spotcheck.md, %(L)s/corpus/lessons/round-47.md ## Mistakes and %(L)s/corpus/QUALITY.md (tops at
criterion 95). Draft %(W)s/w1/ScrMistakes/mistakes.md: rows M48-1.. (class, evidence pointer, captured-by, fix) for D1 (post-freeze contract
narrowing), D2 (unreceipted number in a report), D3 (unrouted seat finding), D4 (locator off by one) and the round-47 runaway scratch write (M47-7:
check it was mined), each with a proposed QUALITY criterion (96..) whose check can FAIL - give the failing input for each. Never duplicate a
criterion that already exists (grep QUALITY.md and cite the near-duplicates).""")
seat("ScrErrataD4", "scribe",
     "Routed D4: erratum line for corpus/knowledge/xdg-terminal-selection-r47.md.",
     """Verify by grep -n that %(L)s/corpus/knowledge/xdg-terminal-selection-r47.md cites terminal-route-r17.md:150-151 and that the cited text sits
at :149-150; sweep every other terminal-route-r17.md locator in that entry and in the round-47 lesson the same way. Draft the append-only erratum
block (one line per wrong locator) in %(W)s/w1/ScrErrataD4/erratum.md with the sweep receipt.""")
seat("ScrSkill", "scribe",
     "SKILL.md sections for the round's two planes.",
     """Read the tail of %(L)s/SKILL.md (sections from rounds 45-47) and draft %(W)s/w1/ScrSkill/section.md: 'XKB keymap compile (round 48)' (symptom
-> cause -> check table: keyboard prints us; option silently ignored; custom layout in ~/.config/xkb; variant count mismatch) and 'Terminal cache
(round 48)' (when SUPER+RETURN can start a stale command; how to check with `tools/mado-terminal.py explain`; how to clear: operator-owned). Facts
only from the context and the drafts' receipts; mark <AFTER> where a landed value is needed.""")
seat("ScrScorecard", "scribe",
     "SCORECARD.md Round 48 section draft and the README coverage row + Frontier bullet.",
     """Draft %(W)s/w1/ScrScorecard/draft.md in the shape of the Round 47 section of %(L)s/SCORECARD.md (claim table with <AFTER> placeholders,
capabilities row for the warm-cache path, sources/saturation/planned, the axis-table publication line with <AFTER> values) and the README index row
for the new entry plus the Frontier bullet (%(L)s/corpus/README.md:108-116 shape).""")
seat("ScrConsider", "scribe",
     "considerthese: one still-unimplemented proposal, grounded through the lane's bar.",
     """From %(L)s/considerthese/2026-10-26.md 'Self-improvement suggestions' pick ONE proposal still unimplemented at %(B)s (not 2: refused round 47;
not 3: QUALITY 90). Open what it points at, and draft its landing in %(W)s/w1/ScrConsider/draft.md as a QUALITY criterion, a lesson paragraph or a
SOURCES row, citing `considerthese/2026-10-26.md` + date, with the evidence that it is unimplemented (grep) and a check that can fail.""")
seat("ScrCacheDoc", "scribe",
     "C1 docstring: the warm-cache contract text with script line references.",
     """From /usr/bin/xdg-terminal-exec :143-340 and :1160-1190, :1325-1460, draft the replacement for the 'Cache' paragraph of
%(L)s/tools/mado-terminal.py (:82-85) and a new 'Out of contract' list for round 48 - every statement with script line ranges (computed). Also
draft the PROVINCE.md round-48 refinement line (the tool now reads the resolver cache file: name it; writes nothing). Write
%(W)s/w1/ScrCacheDoc/docstring.md.""")
seat("ScrD1Line", "scribe",
     "Routed D1/D3: the lesson lines that record the round-47 post-freeze contract delta and the unrouted readdir blind spot.",
     """Diff the docstring of %(L)s/.ufo/waves/round-47/l1-draft/mado-terminal.py (frozen reference at d7527d608ad2b2e3cc398fdde34db7947b254a1a) against
%(L)s/tools/mado-terminal.py at %(B)s; draft one appended lesson line per out-of-contract item added after the freeze (HOME unset, FIFO, symlink
loops, anything else), each with both locators, and one line routing D3 (%(L)s/.ufo/waves/round-47/w2/ExecC1Determinism.md:10). Write
%(W)s/w1/ScrD1Line/lines.md.""")

# ------------------------------------------------------------ critics (4)
seat("CritPremiseC1", "critic",
     "Falsify C1's premise before the freeze.",
     """Attack %(W)s/claims.md C1: is the warm-cache path new executed ground (vs %(L)s/corpus/knowledge/xdg-terminal-selection-r47.md cache text)? Can
a warm answer really differ from a cold one on this resolver (build the cheapest such case and run it)? Is 'stale-but-valid' reachable on a real host
(mtime minute resolution in ls -l; editors that keep size)? Which do-nothing or cheap tool could reach a warm target (a tool that trusts every
well-formed cache; one that shells out)? Write %(W)s/w1/CritPremiseC1/findings.md with path:line evidence and the fix to the claim wording.""")
seat("CritPremiseC2", "critic",
     "Falsify C2's premise before the freeze.",
     """Attack %(W)s/claims.md C2: is the XKB compile really unheld at %(B)s (grep corpus)? Does xkbcli compile-keymap behave like Hyprland's own compile
(context flags, include paths, environment names XKB_DEFAULT_*; does Hyprland pass NULL names that xkbcommon fills from the environment)? Is the
entry inside PROVINCE.md (input plane of the compositor) or tsukuroi/kotoba ground? Which sentences would be generic xkbcommon documentation rather
than host-plane knowledge? Write %(W)s/w1/CritPremiseC2/findings.md.""")
seat("CritClaimSizing", "critic",
     "Claim sizing and cribs for both counters (round-prompt section 9).",
     """For C1 (warm-cache tool) and C2 (XKB entry), list the cheapest artifact that would meet each draft predicate without the claimed work
(trust-any-cache tool, subprocess ls, md5 table lookup keyed by fixture id, typed receipt, quote-in-pin but unsupported claim, ...), say which clause
stops it or that none does, and propose the clause or fixture. Write %(W)s/w1/CritClaimSizing/findings.md.""")
seat("CritRoutedItems", "critic",
     "Are the routed items still open, and are the drafts stale?",
     """For each routed item (D1-D4, R3, R4b, M47-10, CritC1Explain, SentC1Sandbox F1-F4) check at %(B)s whether it is still open and whether the
round-47 drafts it points at are stale (file changed since). One line each with evidence. Write %(W)s/w1/CritRoutedItems/findings.md.""")

# ------------------------------------------------------------ connectors (2), sentinels (2), reviewer (1), revenger (1)
seat("ConnSiblings", "connector",
     "Sibling-overlap scan for both claims.",
     """Scan sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: PROVINCE.md, corpus/README.md, SOURCES.md) for XKB/keymap/input
method ground and for xdg-terminal-exec/cache ground. Report contested scope (report, never absorb) and propose a PROVINCE.md refinement line for mado
(or none). Write %(W)s/w1/ConnSiblings/report.md.""")
seat("ConnClaims", "connector",
     "Cross-claim pre-freeze checklist.",
     """Read the round-47 registration, closure (%(L)s/corpus/lessons/round-47-verifier-spotcheck.md) and QUALITY 85-95; produce a pre-freeze checklist
for round 48: what the freeze commit must contain (counters, fixtures, pins, reference, controls, base receipts), separability proofs, which closure
defects recur (post-freeze narrowing, unreceipted numbers, unrouted findings) and how to make each impossible this round. Write
%(W)s/w1/ConnClaims/report.md.""")
seat("SentHost", "sentinel",
     "Host safety of the round's probes.",
     """Review what this round runs on the host: priming xdg-terminal-exec (writes a cache file: where; can any harness touch the real
~/.cache/xdg-terminal-exec?), xkbcli compile-keymap (reads only? env XKB_* influence), hyprctl devices -j (device names are session material), bwrap/
strace. Propose the exact guards for the counters and seat prompts. Read-only. Write %(W)s/w1/SentHost/report.md.""")
seat("SentPrivacy", "sentinel",
     "Privacy of the round's new receipts.",
     """Which classes of host material could the round's receipts carry (device names, keymap text with user paths, home paths in ls output inside the
cache hash input, cache files with HOME paths)? Check %(L)s/quality/check-session-material.py catches them; list classes it misses (classes only,
never values). Write %(W)s/w1/SentPrivacy/report.md.""")
seat("RevR47", "reviewer",
     "Review the round-47 closure items against the lane at %(B)s.",
     """Read %(L)s/corpus/lessons/round-47-verifier-spotcheck.md and verify each routed defect D1-D4 and the carried items with commands (git show,
grep -n). List any defect not in the closure. Write %(W)s/w1/RevR47/review.md.""")
seat("RevengerCache", "revenger",
     "Why the resolver cache is built the way it is (intent), to scope the C1 contract.",
     """Reverse-engineer the intent of xdg-terminal-exec's cache: read the upstream history (github.com/Vladimir-csp/xdg-terminal-exec: commits that
introduced/changed gen_hash, the cache 'version' 4, ls -LRl, the background save; issues about stale caches) via tag/commit URLs, and the v0.14.3
README cache section. Which invalidation gaps are known/accepted upstream (minute resolution, same-size edits, PATH changes)? Write
%(W)s/w1/RevengerCache/report.md with commit-pinned citations.""")

n = len(items)
assert 32 <= n <= 64, n
assert len({i["name"] for i in items}) == n
print(n, dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-48/w1", "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
