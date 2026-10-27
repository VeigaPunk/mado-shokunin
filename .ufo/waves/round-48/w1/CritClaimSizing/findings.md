# CritClaimSizing — cheap-pass survey of the C1/C2 predicates (round-48 w1)

Seat: CritClaimSizing (leaf; no subagent dispatch). Purpose: attack the declared C1/C2 predicate designs for cheap
passes, before the L1 freezes the instruments in `registration.md` after this wave. Inputs: `round-48/claims.md`
(declared claims, lines 12-27), the fixture-schema v2 draft in the round prompt, the r47 frozen counters and registration
(`quality/counters/c1-r47-terminal.py`, `c2-r47-terminal-entry.py`, `c2-r46-input-device-entry.py`,
`.ufo/waves/round-47/registration.md`), and `w1-spec.json` (this seat's prompt).

Axes named (godspeed): (A) C1 judge fidelity — the warm-cache judge must discriminate a faithful implementation from a
cheap one; (B) C2 sourcedness + coverage — the XKB entry must be earned, not quoted, and must cover the claimed surface;
(C) freeze robustness — every recommendation lands as a registrable clause or fixture, not prose; (D) judge-mechanics
reliability — the prime/cache choreography must be deterministic before anything else is scored.

All locators below are computed (`grep -n`), not typed. Measured evidence is saved beside this file: `prime-cache-sample.txt`
(real cache written by the pinned script), `ls-probes.txt` (GNU ls byte/format probes), `xkbcli-*` (read-only live receipts).

---

## 1. C1 warm-cache — cheapest artifacts that meet the draft predicates without the capability

Draft contract (claims.md:17-21): given the tree, environment and an existing cache file the tool predicts the resolver's
stdout and exit status (hit, miss, invalid, disabled), still starting no process and opening no socket; `explain` names the
cache verdict. Judge = the real pinned script: a cold `--print-cmd` prime, wait for the background save, post-prime
mutations, warm run, tool stdout+rc == warm run.

### 1.1 Lookup table keyed by fixture id — NOT STOPPED (the largest hole)

Cheapest artifact: a static map from `(fixture id, env, args)` to the warm output. Every fixture is fixed: id (stable
string), tree bytes, env, args, prime sequence and post-prime mutations are all deterministic, and `expect` is recorded by
running the real script (claims.md:19-20). A table built once from a local run of the prime + warm oracle reproduces every
warm and invalid verdict with zero selection logic and zero ls emulation.

Which clause stops it: **none**. The r47 counter's `g` clause (150 nonce cases judged by the oracle at count time,
`c1-r47-terminal.py:29-31,44-45`) is not carried into the C1 draft: the draft describes only fixtures (claims.md:19-20).
The live-oracle comparison (tool vs warm run) does not stop a table either — the oracle's behavior is itself fixed per
fixture. Non-determinism, not comparison, is the stopper.

Proposed clause/fixture (freeze text): *"a g clause: >= 100 generated warm cases at count time, drawn from `--nonce`
(fresh CSPRNG, printed), where tree contents, env, args, cache literal and `mtime` epochs are drawn at random, including:
valid caches (hash-correct by construction: compute them with the real script on the generated tree), stale by each
invalidation dimension (mtime/size/name/dir/desktop/exec-gone), malformed literals (missing terminator, line >= 50, bad
hash, less than 11 lines), the hash-preserving edit class, env-disabled, and mtimes sampled uniformly across [-2y, +30d]
relative to now so the HH:MM/year display boundary is always in range. The judge runs the tool and the warm oracle on
separate but identical trees and compares stdout+rc (r47 clause f shape)."* Belt: static inspection banning embedded
case→output or hash→output maps (as recommended to r47, `w1/CritClaimSizing/findings.md` 1.3).

### 1.2 Trust-any-cache (parse the cache, skip `gen_hash`) — stopped ONLY by the invalidation families

Cheapest partial tool: read the cache file, validate only structure (10 header lines + terminator, <= 49 lines) and
`command -v` on line 2, and print from the cached fields. It passes every warm-hit fixture without computing the hash
(including the hash-preserving "size and mtime minute kept" edits — those are exactly the cases where the cache stays
valid), and it fails exactly the invalidation families.

Which clause stops it: the draft already names the families ("mtime/size/name/dir change, XDG_CURRENT_DESKTOP change,
exec[0] gone, missing terminator, line limit, bad hash", claims.md:19-20). **Stopped, but only if those families are
frozen as required, present fixtures with a warm answer that differs from the cold answer, and are scored.** A trust-any
tool cannot distinguish hit from stale by any cheaper channel: the cache holds only an md5 (line 1), and equality of the
hash requires computing md5 over exactly the current `ls -LRl` bytes — there is no trustable proxy (no tree mtime is
consulted by `read_cache`, `fetch/xdg-terminal-exec:217-298`). So the byte-exact ls emulation is load-bearing for every
invalid fixture; the honest-but-shallow path cannot pass them.

Proposed freeze additions:
1. Required families, one fixture each, with the counter-side assertion: *"for every warm-hit fixture, the counter must
   verify the warm answer differs from the cold answer on the same tree (run the oracle once with the cache and once with
   the cache file removed); a fixture where they are equal is a setup error."* Without this, a tool that ignores the cache
   entirely (the r47 tool) passes the warm class.
2. The hash-preserving edit class explicitly: content edit that keeps size and mtime minute (edit the cached entry's
   `Exec=` so a cold run would select differently) — this pins the requirement that warm output comes from the cache bytes,
   not from re-reading the tree.

### 1.3 Vendored or ported pin logic — satisfied every letter; nothing stops it (carry-over)

Cheapest *correct* tool: embed the pinned script and interpret it in-process (pure-Python POSIX-sh interpreter), or port
the pin's logic byte-for-byte (including `ls` formatting). Stdlib-only, no process, no socket, writes nothing — every
letter of the draft contract holds, and the orphan matches the real script on every warm and invalid case because it runs
the same program. This is the r47 finding 1.2 restated for the warm world (`.ufo/waves/round-47/w1/CritClaimSizing/
findings.md` 1.2); it also means the "hard part" of the round (byte-exact md5 over `ls -LRl`) is hard only for an
independent implementation.

Which clause stops it: **none**. The r47 residual declared an emulator/interpreter "an implementation of it"
(`registration.md:52-53`), so a Python interpreter for the embedded script is already inside the declared residual.
Proposed freeze decision (either branch, explicitly): (a) authorship clause — *"the tool must not contain the pinned
script or a byte-level transcription of it (verbatim source, token stream, or contiguous runs of its text longer than 40
chars, excluding standard XDG variable/option names); the selection logic must be authored in Python for this round"*
(enforceable statically, longest-common-substring vs the pin); or (b) declare the vendored-interpreter path a permitted
residual. Silence leaves an exploit whose cost at judging time is zero.

### 1.4 Subprocess/exec of `ls`, `md5sum` or the pin — stopped by clause r + "no process"

Cheapest honest shortcut: `subprocess.run(["ls", ...])` or `os.execv`/`posix_spawn`/`ctypes` libc calls to delegate the
byte-exact listing. Which clause stops it: clause r (strace `execve/execveat/socket/socketpair/connect` after the
sandboxed python3's execve, `c1-r47-terminal.py:46-49`) and the contract's "NO process". Wording suggestion (from r47
1.1): state "by any API (subprocess, os.exec*, posix_spawn, ctypes/libc calls)" so dynamic loading cannot route around
the tripwire. Note the oracle run is not straced; only tool runs are.

### 1.5 Cold-ignore tool (r47 behavior) — stopped only by warm≠cold enforcement

A tool that keeps the r47 cold semantics (never look at the cache) reproduces every invalidation fixture (the oracle goes
cold too) and fails every warm-hit fixture. Same fix as 1.2 proposal 1: counter-side warm≠cold assertion makes the warm
class discriminating.

### 1.6 Exfiltration — mostly closed by the sandbox, explain verdict still table-able

The r47 exfiltration hole (reading the manifest/oracle) is structurally closed here as it was in r47: the tool's sandbox
exposes only the case root, the environment, stubs and Python (`SentC1Sandbox.md` F1-F4 found no lane/repo/oracle reach),
and the tool runs after the oracle, which leaves no readable output behind. The cache file itself is the legitimate answer
sheet for warm hits (the resolver honors it), so parsing it is not a cheat. What remains table-able is the *verdict* in
`explain` (`cache=<absent|hit|stale|invalid|disabled>`): the oracle never prints its cache verdict, so clause x can only
check the tool's verdict against the fixture's authored class — which a table reproduces trivially. Again, only generated
cases (1.1) close this. Residual to declare again: sandbox detection (r46/r47 accepted).

### 1.7 Judge-mechanics defect: the prime's background save dies with the bwrap namespace (MEASURED) — freeze a fix

Mechanism: the pin writes the cache from a backgrounded subshell (`save_cache "$1" &`, `fetch/xdg-terminal-exec:1457`).
Under the r47 sandbox recipe (`bwrap --unshare-all --die-with-parent ...`, `c1-r47-terminal.py:137-156`), when the
foreground `--print-cmd` exits, bwrap tears the pid namespace down and the orphaned save is killed before it writes.

Measured (receipt `prime-cache-sample.txt`, scratch `CritClaimSizing/prime/`): cold `--print-cmd` under the r47 bwrap
argv with the same env/tree → rc 0, stdout `foot`, **no cache file after 2 s**. Same environment with an in-namespace
grace (`/bin/bash -c '/oracle/xdg-terminal-exec --print-cmd; sleep 3'`, `sleep` bound into `/oracle/bin`) → cache exists:
11 lines, 183 bytes, line 1 md5, line 2 `foot`, line 3 path with the `/./` find marker, line 11 `foot` + `\x1e` +
`END_OF_EXEC_USEP`. Host-side prime (no bwrap) also writes it.

Impact: as drafted, every warm fixture degenerates to cold (the judge's oracle sees no cache), so the warm class cannot be
scored at all; and if the judge instead waits only for process exit, the cache race is nondeterministic. Proposed freeze
(or one of): (a) prime command = `sh -c '/oracle/xdg-terminal-exec --print-cmd; <grace>'` with a bound `sleep` (or a
bash-builtin poll loop `until [ -f "$XDG_CACHE_HOME/xdg-terminal-exec" ] || ! read -t 0.05 _; do :; done` bounded to ~2
s), then assert completion: file exists, >= 11 lines, last line ends with the `\x1e` terminator, and content stable over
two reads 200 ms apart; (b) prime on the host (outside bwrap) with the same env/PATH, then copy the cache bytes into both
trees. Either way the completion assertion must be part of the judge, else the suite is flaky.

### 1.8 Env-disabled vs `/disable_cache`, and the empty-value trap — freeze the semantics

Three distinct states must be pinned, they are not symmetric:
- `XTE_CACHE_ENABLED` env (checked BEFORE any list read, `fetch/xdg-terminal-exec:1179`): `false|no|0|...` → cache not
  read at all, cold path, and `save_cache` removes any existing file (`fetch/xdg-terminal-exec:335-338`). Verdict: `disabled`.
- The `/disable_cache` list directive (`fetch/xdg-terminal-exec:380-385`): only parsed during a cold `read_config_paths`,
  i.e. AFTER the `:1179` read decision and only when the cache was NOT a hit — so on a warm run with a valid cache the
  directive is never seen by the resolver; it only stops the *write* on a cold run. A tool that reports `disabled` because
  a list contains `/disable_cache` is wrong whenever the cache hits.
- Empty `XTE_CACHE_ENABLED=""`: the default is `${XTE_CACHE_ENABLED-true}` (`fetch/xdg-terminal-exec:1172`) — parameter
  expansion `-`, not `:-`, so an empty env value stays set and `check_bool ""` warns to stderr and returns false; but note
  the *default* fires only when the variable is unset. Freeze fixtures for each of: unset, empty, `TRUE `, garbage, `0`,
  `false`.
Proposed contract text: `explain` verdict mapping `absent` (no cache file) / `hit` (read succeeds) / `stale` (parse ok,
hash or `command -v` fails, `fetch/xdg-terminal-exec:274,287`) / `invalid` (malformed: no terminator, or line 50 reached,
`fetch/xdg-terminal-exec:223,239-242,291`) / `disabled` (env gate false before read, `fetch/xdg-terminal-exec:335-338`).

### 1.9 The byte-exact `ls -LRl` floor — measured crib sheet for the executor

The drafted claim makes `md5("4\n"+desktop+"\n"+ls_bytes)` the trust gate (`fetch/xdg-terminal-exec:179-215`). Measured
GNU coreutils behavior (host `/usr/bin/ls` = the binary the counter copies; receipts `ls-probes.txt`):
- Multiple operands are displayed **files first, then directories, each group alphabetic** (byte order in C locale),
  regardless of command order; `ls -LRl d1 plainfile d2` and `ls -LRl plainfile d2 d1` both print plainfile, then d1, then d2.
- Blocks are separated by an empty line; a single directory operand starts with its `path:` header and no leading blank; a
  file operand has no header; a missing operand prints nothing to stdout (error to stderr, dropped by `2>/dev/null`) and
  makes the process exit 2 without changing stdout.
- Recursion: each directory's own listing (entries sorted, dotfiles hidden — `.hidden` excluded), then children dirs
  recursed in sorted order, each with a leading blank and `path:` header. With `-L`, a symlink-to-dir entry displays as a
  directory and is recursed under the link's own name (`dp/rel:`); a symlink-to-file entry displays the target's
  metadata with the link's name and no arrow; a dangling symlink operand prints nothing on stdout and rc=2.
- `total N` = sum of `st_blocks`/2 (512-byte units) over displayed entries; empty dir → `total 0`.
- Columns: mode, nlink, user, group, size, date, name; numeric uid/gid when no passwd/group entry resolves (always in the
  sandbox, no `/etc`); date `Mon dd HH:MM` iff `now - 6mo < mtime <= now`, else `Mon dd  YYYY` (two spaces). Measured
  boundary: 182 days ago → time; 183 days ago → year; +1 day (future) → year. The L1 draft `l1-draft/lsemu.py:8,57-64`
  encodes `SIX_MONTHS = 31556952 // 2` with strict `<` and `<= now` — matches all measured points.
This is the floor the executor must reach; the generated-case mtime sampling (1.1) plus the required invalidation families
(1.2) guarantee the boundary and every dimension are exercised.

### 1.10 Carry-over: counter-robustness (F4) — do not re-freeze the `obs_dir` abort

The r47 w2 finding stands: a tool that creates `<root>/.rw/obs` before the counter's `os.makedirs(obs_dir)`
(`c1-r47-terminal.py:279`) aborts the count with no verdict (`SentC1Sandbox.md` F4, lines 135-152). Re-apply the fix in
the warm counter: `tempfile.mkdtemp(dir=rt+"/.rw")` + `os.open(..., O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW)` and treat any
OSError there as a fixture failure, not an abort. The tool's "writes nothing" contract is not enforceable by clause r
(execve/socket only), so this is also the only tool-write guard that matters.

---

## 2. C2 XKB entry — cheapest entries that "close" the claim

Draft claim (claims.md:22-27): `corpus/knowledge/xkb-keymap-compile-r48.md` — which `kb_rules/kb_model/kb_layout/
kb_variant/kb_options` compile on this host (libxkbcommon 1.13.2, xkeyboard-config 2.48), rules→components, include-path
order, which unknown names fail vs are dropped with a warning, multi-layout variant alignment, and how a failed compile
maps onto Hyprland 0.56.2's fallback (held: r46 step 4, rows S318/S319 — cite, never re-claim). Rows S340.. new.
The entry counter will presumably mirror `c2-r47-terminal-entry.py` clauses a-i / `c2-r46-input-device-entry.py` clauses
a-j (T1-T5); the cheap artifacts below are checked against those clause families.

### 2.1 Typed receipt / restated L1 facts — stopped only by a REPLAY clause (propose it)

Cheapest: write the entry from the L1-provided host facts (rc table) with a receipt file fabricated for each (never run),
or reuse a sibling seat's live receipt. The r46/r47 counters verify receipt form, sha256, size, existence and quote
fidelity — not that the command was ever run ("a capture can be typed rather than produced by the resolver",
`registration.md:76`; `c2-r47-terminal-entry.py:86-93` declares the parallel truth-of-sentence residual). So a typed
receipt passes every existing clause.

Proposed freeze clause (new, cheap for the counter): *"replay: for every receipted `xkbcli compile-keymap` command quoted
in the entry, the counter re-runs the exact command on the host (read-only, stdout to a pipe) and requires stdout bytes
equal to the receipt's recorded stdout and rc equal to the receipt's rc; for claims about stderr messages, the message
substrings must appear in the receipt's recorded stderr."* Measured support: `xkbcli compile-keymap --layout br --options
compose:caps` twice → sha256 `efd487a3...` both times, `cmp` identical, so replay is stable. Environment note: run the
replay with the same `LANG`/`LC_ALL`/`HOME`/`XDG_CONFIG_HOME` the receipt records (the "3 include paths could not be
added" line embeds `$HOME` paths — verified absent on this host today, `xkbcli-zz.err`). Under replay, copying a sibling
seat's receipt becomes harmless (truth is re-verified); only the "author ran it" property is unverifiable — declare it a
residual, as r47 did.

### 2.2 Quote-in-pin but unsupported claim — partially blocked; the runtime messages make fabrication fail naturally

The r46/r47 clauses bind every quoted span to a verbatim occurrence at a locator in a pinned source
(`c2-r47-terminal-entry.py` clause d; `c2-r46-input-device-entry.py` clause g: every unfenced line naming a cited id
carries that id's Gate quote and locator). But a *true quote at a true locator can stand beside a claim it does not
support* (`c2-r47-terminal-entry.py:89-90`) — the truth-of-sentence residual. For the compile-failure and warning claims
this residual is self-healing: the messages are runtime stderr, present in no upstream doc, so an entry that fabricates
"`xkbcli` prints ..." cannot anchor it to any pin; the only honest source is a live receipt. Measured canonical messages
(receipts `xkbcli-*.err`; quoted <= 25 words):
- layout unknown: `xkbcommon: ERROR: [XKB-338] Couldn't find file "symbols/zz" in include paths` … `[XKB-661] Couldn't
  process include statement for 'zz'` … `ERROR: Couldn't create xkb keymap` (rc 1, empty stdout).
- variant unknown: `[XKB-661] Couldn't process include statement for 'br(nope)'` (rc 1).
- option unknown: `[XKB-595] Unrecognized RMLVO option "nope:nope" was ignored` on stderr, rc 0, stdout byte-identical to
  the no-options run (both 73043 bytes).
- model unknown: rc 0, stdout byte-identical to the valid-model run (both 73043 bytes), no stderr — the model is dropped
  silently; a model claim must therefore be a receipt, not a quote.
- rules unknown: `[XKB-338] Couldn't find file "rules/nope" in include paths` … `[XKB-595] Cannot load XKB rules "nope"`
  … `[XKB-822] Couldn't look up rules 'nope', model 'pc105', layout 'br', variant '(null)', options '(null)'` (rc 1).
- include paths: `1 include paths searched: /usr/share/xkeyboard-config-2` and `3 include paths could not be added:
  /home/vgpnk/.config/xkb /home/vgpnk/.xkb /etc/xkb` (from the `zz` run; all three absent on the host).
- multi-layout alignment: `--layout br,us --variant nope,` fails on `'br(nope)'`; `--variant ,nope` fails on
  `'us(nope)'`; `--variant ','` and 3 layouts with `',,'` compile — variants align positionally, missing slots allowed,
  any non-empty unknown element fails. Freeze at least one fixture per direction.

### 2.3 Minimal-content entry — stopped only by enumerated surface coverage (propose the list)

Cheapest content: the five host-fact bullets with receipts, nothing else. It satisfies rows/quote/receipt clauses but
leaves the claim's middle clauses unearned (include-path order, multi-layout alignment, fallback mapping). The r46 counter
already has the pattern: clause j enumerates surfaces (anchor text + keyword + locator window, `c2-r46-input-device-entry.
py:55-67`). Propose the r48 surface list mirroring claims.md:22-27: (1) rules→components resolution (a successful
compile's `xkb_keymap` header names); (2) include-path order — searched root vs the three "could not be added" user
paths; (3) failure classes layout/variant/rules with their rc and messages; (4) warning-dropped classes (option XKB-595
vs model silent) with byte-equality evidence; (5) multi-layout variant alignment both directions; (6) Hyprland fallback
citation — must cite r46 step 4 (`hyprland-input-devices-r46.md:33`, "fallback to us after an error overlay") and rows
S318/S319 (`hyprland-input-devices-r46.md:5-6,42-43`), phrased as citation, never re-claim.

### 2.4 Re-claim of held ground — make the citation mechanical

A line asserting the `us` fallback without citing r46 would pass "new ground" clauses but violates the round prompt's
"cite, never re-claim" (claims.md:25). The r46 counter's clause g already turns this into a mechanical gate (every line
naming a cited id carries its quote and locator, `c2-r46-input-device-entry.py:37-40`); freeze S318/S319 into the held
set (like r47's HELD S056-S060, `c2-r47-terminal-entry.py:116`) so the rows must be present, cited, and quoted.

### 2.5 Registry/rows mechanics

Rows S340.. must exist at REV as new rows (mined, opened 2026-10-26, used-by the entry) with valid recheck cells
(clause b/c shape, `c2-r47-terminal-entry.py:26-49`); the census tops at S339 (receipt `census-before.txt`), so the new
rows are entirely new. Cheap pass "cite S340 before it exists" is stopped by the ghost-id check (clause b).

---

## 3. Residuals the freeze should declare

- Carry-over (r47): sandbox detection; a true quote at a true locator can stand beside an unsupported claim (C2, kept);
  clause e/s count steps/terms, not truth; selftest is a printed line.
- New: warm-hit fixtures are only meaningful under the judge-side warm≠cold assertion (1.2); the oracle never prints its
  cache verdict, so explain's `cache=` verdict can only be checked against authored classes — generated cases are the only
  discriminator (1.1/1.6); the prime must be made to complete (1.7); env-disabled vs `/disable_cache` asymmetry (1.8).
- New: "no process / no socket / stdlib-only" are anti-wrapper clauses, not pro-fidelity clauses; the fidelity clauses are
  the generated cases, the warm≠cold assertion, the invalidation families, and the authorship decision (1.3).

## 4. Priority for the freeze

1. C1 1.1 — generated warm cases + fresh nonce + anti-table static check (without this, every other C1 clause is bypassable by a table).
2. C1 1.7 — prime completion fix (without this, the warm class cannot be scored at all).
3. C1 1.2 — required invalidation families + warm≠cold assertion.
4. C1 1.3 — vendoring decision (clause or declared residual).
5. C1 1.8 — cache verdict semantics (absent/hit/stale/invalid/disabled; env vs directive asymmetry).
6. C1 1.10 — F4 obs-dir fix.
7. C2 2.1 — replay clause (typed receipts are otherwise undetectable).
8. C2 2.3 — enumerated surface coverage; 2.4 held-row gate.
9. C2 2.2 — stderr-message receipts as the only anchor for runtime behavior.

## Evidence index (all under `.ufo/waves/round-48/w1/CritClaimSizing/`)

| artifact | what it is |
|---|---|
| `prime-cache-sample.txt` | the real cache file the pinned script wrote (11 lines, 183 bytes, `\x1e` terminator) — the prime-completion proof |
| `ls-probes.txt` | GNU `ls -LRl` probes: operand order, headers, blank separators, dotfile exclusion, dates at 178-190 days + future, nested symlink `-L` |
| `xkbcli-br.out`, `xkbcli-*.err` | live `xkbcli compile-keymap` stdout/stderr for br, zz, br(nope), nope:nope, model nope, rules nope, multi-layout alignments |
| `xkbcli-hashes.txt` | determinism: two `br` runs sha-identical |
