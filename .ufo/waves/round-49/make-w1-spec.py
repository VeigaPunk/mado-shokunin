#!/usr/bin/env python3
"""Generates .ufo/waves/round-49/w1-spec.json (round 49, wave w1 = BUILD, policy v1, band 32-64).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
w1 builds and probes; nothing is frozen yet, no seat scores a frozen counter. The L1 freezes after w1 returns;
wave w2 (falsify) attacks the frozen instruments.
"""
import collections
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-49"
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r49"
HYPR = "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/"
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
mado round 49 (hyaku run 9, 2026-10-27), wave w1 = BUILD (policy v1). Lane repo: %(L)s (desktop and compositor craft: the Hyprland/waybar/
walker/terminal config plane of this host; axes coverage + operability). Base (lane tip at round start) %(B)s. Nothing is frozen yet: the L1 freezes
predicates, counters, fixtures and controls AFTER this wave returns, and wave w2 attacks the frozen instruments. Your output feeds that freeze.
Declared claims: %(W)s/claims.md (read it first). Previous round's outside check: %(L)s/corpus/lessons/round-48-verifier-spotcheck.md.
- C1 operability (capability acquisition): a NEW read-only tool %(L)s/tools/mado-keysym.py (Python 3 stdlib only; no process, no socket, writes
  nothing). Draft contract: `mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG` prints exactly what the pinned
  `/usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG` prints on STDOUT and exits with ITS exit status
  (libxkbcommon 1.13.2-1; how-to-type binary sha256 f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54; `xkbcli how-to-type` is the
  same program through /usr/bin/xkbcli). Without --disable-compose or --keysym the tool refuses (exit 2): Compose sequences and the
  character/code-point interpretation are out of contract. FILE is a keymap SERIALIZED by the pinned `/usr/lib/xkbcommon/xkbcli-compile-keymap`
  (sha256 43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250) from xkeyboard-config 2.48 RMLVO names (default formats), not raw XKB
  sources with includes. ARG is a keysym name or a numeric keysym value (0x hex / decimal) as how-to-type accepts it. Keysym names <-> values come
  from libxkbcommon 1.13.2 (xkb_keysym_from_name / xkb_keysym_get_name); the header /usr/include/xkbcommon/xkbcommon-keysyms.h (sha256
  13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3, 2659 `#define XKB_KEY_` lines) is the obvious data source - find out whether
  it is sufficient (canonical name choice, deprecated aliases, Unicode U+ names, case) or whether the tool must embed a table generated from it.
  Output: `keysym: <name> (0x%%04x)`, a blank line, `=== Direct access ===`, a blank line, the column header, then one row per (keycode, layout,
  level, modifier mask) as libxkbcommon's tools/how-to-type.c prints them (xkb_keymap_key_get_mods_for_level masks; real and virtual modifier
  names, e.g. `[ Mod5 LevelThree ]`, `[ Shift Lock Mod5 LevelThree ]`). Host sample (L1, 2026-10-27, keymap from `xkbcli compile-keymap --layout br
  --options compose:caps`): `--keysym slash` -> AD01 levels 3/4 with LevelThree masks and AB11 level 1 `[ ]`; `--keysym Return` -> RTRN level 1;
  `--keysym nosuchsym` -> stderr "ERROR: Failed to convert argument to keysym" + usage, rc 2.
  The JUDGE is the real pinned how-to-type: the C1 counter compiles each fixture's keymap at count time with the pinned compile-keymap in a clean
  environment (env -i PATH=/usr/bin, HOME and XDG_CONFIG_HOME in scratch so no user xkb include path exists), runs the judge, runs the tool in a
  bubblewrap sandbox that can see only the keymap file (plus the keysym header if the contract keeps it), and requires the tool's stdout+rc to equal
  the judge's, on fixed fixtures and on nonce-generated (RMLVO, keysym) pairs.
  Why it matters: binds name keysyms (`bind = SUPER, SLASH, ...`); on this host's `br` keymap SLASH is AB11 level 1 AND AltGr+Q (AD01 level 3). Which
  physical key fires a bind is exactly this question.
- C2 coverage (sourced): a new entry %(L)s/corpus/knowledge/hyprland-bind-key-match-r49.md: how Hyprland 0.56.2 (commit efb50993780079460b0cbed1363e2166a2de1d9f,
  host `hyprctl version`) turns the key field of `bind = MODS, KEY, dispatcher, arg` into something a key press matches: key name -> keysym
  (xkb_keysym_from_name with which flags; case handling; `code:N` keycodes; `mouse:N`, `mouse_up/down`, `switch:`, `catchall`), which keysym of a
  pressed key is compared (the layout/state used: translated vs untranslated sym, layout 0 vs the active layout, `input:resolve_binds_by_sym`), how the
  modifier mask is compared (exact equality? ignore_mods flag `i`? Caps/NumLock masked?), and keycode binds vs keysym binds when both exist. Sources
  (rows S352.. opened this round; registry tops at S351): Hyprland sources at %(HY)s (e.g. src/managers/KeybindManager.cpp,
  src/config/ConfigManager.cpp handleBind, src/devices/IKeyboard.cpp - held row S319 already covers IKeyboard.cpp: cite it, never re-register its URL),
  libxkbcommon at %(XKB)s (src/keysym.c), the Hyprland wiki at a pinned commit (Binds / Variables pages), all pinned by sha256 under
  %(W)s/fetch/ by the L1. Live READ-ONLY receipt: `hyprctl binds -j` (192 binds on the host: fields key, keycode, modmask, ...) and
  `hyprctl getoption input:resolve_binds_by_sym -j` (host: int 0, set false). Ground open at base: %(L)s/corpus/knowledge/keybind-rule-semantics.md
  section 2.3 (key forms at [INF-docs] level only) and %(L)s/corpus/knowledge/hyprland-input-devices-r46.md:71 (bind resolution outside the join).
Routed round-48 closure items (non-claim work; %(L)s/corpus/lessons/round-48-verifier-spotcheck.md section 6): N1 untracked count 47 not 52;
  N2 `host_cache_untouched` digest = the w2 mutant's bytes; N3 stale "five gate decisions" at corpus/lessons/round-48.md:425; N4 text matrix shows
  96 of 98 variants (%(L)s/.ufo/waves/round-48/receipts/v2/); N5 GitLab `-/raw/` anti-bot page, files API serves pinned bytes; M48-8 session-material
  gate %(L)s/quality/check-session-material.py red at the tip (`findings=159`, .ufo/waves/round-48/receipts/a4/session-material-tip.txt) and blind
  to 16 of 19 synthetic /home/<user> shapes (.ufo/waves/round-48/w1/SentPrivacy.md) with scope `.ufo/` only; M48-10 a round-48 w2 mutant wrote the
  operator's real ~/.cache/xdg-terminal-exec (corpus/lessons/round-48.md M48-10); M48-13 the residual call's 1 MiB file cap broke clones, so the owed
  clause-r mutant attack and the gate both-ways demonstration never ran; w2/SentScratch (.ufo/waves/round-48/w2/SentScratch.md F1-F7: counters
  accept a /tmp work dir); registration-v2 residuals (.ufo/waves/round-48/registration-v2.md:103-110). Also: 47 untracked `*.synthetic` sidecars under
  .ufo/waves/round-45/w1/RevengerOmarchy/ and round-46/w1/ (written by round-48 w1 ExecSessionMarker outside its seat dir; digests in
  .ufo/waves/round-48/w1/ExecSessionMarker/SHA256SUMS) - L1 decides commit vs remove.
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin outside the lane), sibling lanes, templates/, scripts/,
  MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout (READ-ONLY; never run a campaign tool there), or the lane's jj/git
  index. Never run mutating git/jj in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus your Report file. Never edit an existing tracked file and never
  create files elsewhere in the lane (round-48 incident: a seat wrote 47 sidecars into round-45/46 dirs); the L1 is the only integrator. Write your
  Report file FIRST (a short status), then refine it; a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>. Your tools start at the fleet root: use absolute paths only.
- SCRATCH (operator directive 2026-10-25): every clone, venv, build, fixture tree and work dir lives under %(S)s/<YourSeatName>/ (mkdir -p; pass it
  explicitly as TMPDIR/--work/dir=, never rely on an inherited TMPDIR); /tmp only for files under 50 MB; keep it under 2 GB; start every writer
  shell with `ulimit -f 65536` (64 MiB per file: the lane's largest tracked file is 4.2 MB, so a `git clone -q --shared %(L)s "$D"` checkout fits;
  round-48 M48-13: a 1 MiB cap broke clones) and bound every loop; never `yes`, never an unbounded redirect, never write into a FIFO or device;
  copy receipts into your seat dir first, then delete your scratch dir before you finish (`trap 'rm -rf -- "$S"' EXIT`). A /tmp or scratch path is
  never citable evidence. Committed code must honour TMPDIR / --work and REFUSE a work dir under /tmp (SentScratch), never hardcode /tmp.
- HOST GUARD (operator note, round-48 M48-10): NEVER write the operator's real ~/.cache, ~/.config, ~/.local or any other home state. Every probe,
  mutant, counter or judge run that could write home state runs with HOME, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME and XDG_STATE_HOME set
  to dirs under your scratch (and preferably inside bwrap with the real home not bound). A mutant that writes must target a path inside the sandbox.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input
  injection, never launch a terminal or any GUI program. xkbcli: ONLY `compile-keymap`, `how-to-type`, `list` (stdout only, clean env), never
  `interactive-*` or `dump-keymap*`. Allowed compositor reads: `hyprctl version`, `hyprctl binds -j`, `hyprctl getoption <opt> -j`, `hyprctl devices -j`
  (device names are session material: never commit them); NEVER `dispatch`, `keyword`, `reload`, `setprop`, `switchxkblayout`, `--batch`, `output`,
  `plugin`, `kill`. Host config trees and binaries are READ-ONLY. Session material stays shape-only: never commit window titles, monitor
  serials/descriptions, input-device names, process tables or home listings; write `~` for the home directory in receipts.
- Git fixtures (run-6 incident): any fixture repo is `D=$(mktemp -d -p %(S)s/<YourSeatName>)` then `git -C "$D" init -q` (or `git clone -q --shared
  %(L)s "$D"`), every later git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the first commit; never
  `git commit` with a throwaway identity anywhere else.
- Tooling authorization (operator, 2026-10-19): you and every seat may install/upgrade tools that help the task - read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20):
  ALL pacman transactions are PAUSED host-wide until the operator resolves the host-recovery L0 question - use uv tool / uv pip into a scratch venv /
  npx / an official binary in ~/.local/bin; never -Sy, -Syu, -U, -R, a downgrade, or a restart of a host service.
- You are a leaf: no subagent dispatch, no background jobs, no spawning (an executor MAY spawn one read-only labrat probe).
- Every finding names what it attacks or supports (a path:line, a command and its output, or a hash). Never fabricate: an unrun check has not passed.
  Quotes lifted from a source are <= 25 words, located (file:line), and verified by a script that greps your receipt; locators are computed
  (grep -n), never typed. Pins you fetch go to your seat dir with their sha256 and the URL they came from (tag or commit URLs, never a branch).
"""


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(B)s", BASE), ("%(P)s", PKG), ("%(S)s", SCR), ("%(HY)s", HYPR),
                 ("%(XKB)s", XKB)):
        t = t.replace(k, v)
    return t.replace("%%", "%")


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({
        "name": name, "role": role,
        "prompt": sub(GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() + "\n")})


# ------------------------------------------------------------ executors (20)
seat("ExecRefKeysymA", "executor",
     "C1 reference A: a complete draft of tools/mado-keysym.py at your seat dir (never at the tracked path).",
     """Write %(W)s/w1/ExecRefKeysymA/mado-keysym.py per the draft contract: parse the serialized keymap (xkb_keycodes names/aliases, xkb_types with
modifiers/map/level names, xkb_compat (virtual modifier mapping), xkb_symbols with group names, explicit and default key types, multiple groups,
modifier_map/vmodmap), resolve the keysym argument, and print the how-to-type table byte-exactly. Include a hermetic --selftest (>= 25 cases, last line
`MADO_KEYSYM_SELFTEST: N/N passed`, exit 0 iff all pass, writes nothing outside a private temp dir under $TMPDIR). Self-check against the REAL judge
on >= 40 keymaps (single/multi layout, variants, options) x >= 60 keysyms each, with keymaps compiled in a clean env (HOME/XDG in scratch). Write
receipts/agree.txt (keymap rmlvo, keysym, ours==theirs) and list every disagreement with the libxkbcommon source line you traced it to.""")
seat("ExecRefKeysymB", "executor",
     "C1 reference B: an independent implementation (do not read ExecRefKeysymA's files).",
     """Independently implement %(W)s/w1/ExecRefKeysymB/keysym_ref.py with functions parse_keymap(text), keysym_from_arg(arg), how_to_type(km, ks)
-> (stdout, rc), built from libxkbcommon 1.13.2's tools/how-to-type.c, src/keymap.c (xkb_keymap_key_get_mods_for_level), src/keysym.c (fetch at
%(XKB)s, pin sha256). Prove it against the real judge on >= 3000 (keymap, keysym) pairs drawn at random from `xkbcli list` RMLVO names and the
header's keysyms (clean env, scratch HOME). receipts/diff.txt with seeds. Report each behaviour that surprised you, with the source line.""")
seat("ExecKeysymNames", "executor",
     "The keysym argument and header line: name/number -> keysym -> printed name, exactly as how-to-type does.",
     """Map how-to-type's argument path for --keysym (tools/how-to-type.c at %(XKB)s: which parse of the argument, xkb_keysym_from_name flags,
numeric forms, '0'..'9', U+/0x Unicode keysyms, leading/trailing spaces, empty string, overflow, NoSymbol) and the header `keysym: NAME (0x%%04x)`
(xkb_keysym_get_name: canonical name among aliases; names of keysyms with no name, e.g. 0x1000000+ Unicode and unnamed values). Write
%(W)s/w1/ExecKeysymNames/keysyms.py (stdlib) deriving the tables from /usr/include/xkbcommon/xkbcommon-keysyms.h if that suffices, else a generator
that embeds them; prove against the judge for EVERY name in the header and for >= 2000 numeric values (receipts/names-diff.txt). State whether the
tool must read the header at run time (counter sandbox must then expose it) or can embed a table, and the exit status/stdout/stderr of each error.""")
seat("ExecModsLevel", "executor",
     "The MODIFIERS column: xkb_keymap_key_get_mods_for_level and the mask printing, re-implemented exactly.",
     """From src/keymap.c and tools/how-to-type.c at %(XKB)s (pin them), write %(W)s/w1/ExecModsLevel/mods.py: given a parsed key type (modifiers,
map entries with mods and level, preserve) return the ordered masks how-to-type prints for a level (level 1 implicit empty mask? masks of entries whose
level matches? Lock combinations - why does `[ Lock Mod5 LevelThree ]` appear?), and the printing of a mask (order of real vs virtual modifier names,
which virtual modifiers are named: those whose mapping is a subset? exactly the type's vmods?). Differential vs the judge over every key of >= 30
keymaps (types ONE_LEVEL, TWO_LEVEL, ALPHABETIC, FOUR_LEVEL*, KEYPAD, PC_*, CTRL+ALT, multi-group). receipts/mods-diff.txt; report the rule set.""")
seat("ExecKeymapParse", "executor",
     "A robust parser of the SERIALIZED keymap text (compile-keymap output), with a census of the syntax actually emitted.",
     """Compile >= 200 keymaps from random RMLVO (xkbcli list; clean env, scratch HOME) with the pinned compile-keymap and census the serialized syntax
the tool must parse: sections, `name[GroupN]`, key blocks with type/symbols/actions/repeat/vmods, `type[GroupN]=`, explicit vs inferred types, group
counts, `modifier_map`, virtual_modifiers lines, comments, escapes in strings, keysym spellings in symbols (names vs 0x hex vs Unicode). Write
%(W)s/w1/ExecKeymapParse/parse.py and receipts/census.txt (construct -> count) and prove parse.py extracts the same key->(group,level)->keysym table
as the judge implies for 20 keymaps (e.g. by inverting how-to-type over all symbols present). Name every construct you declare out of contract.""")
seat("ExecOracle", "executor",
     "C1 judge harness: compile a fixture keymap and run the pinned how-to-type, deterministically, in a clean sandbox.",
     """Write %(W)s/w1/ExecOracle/oracle.py: oracle(rmlvo, arg, work) -> (keymap_bytes, stdout, stderr, rc) running the pinned
/usr/lib/xkbcommon/xkbcli-compile-keymap then /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG with env -i
PATH=/usr/bin HOME=<scratch> XDG_CONFIG_HOME=<scratch>/cfg LC_ALL=C (prove whether locale changes anything), verifying both binaries' sha256 first.
Show 3 identical runs on >= 50 cases, the cost per call, behaviour with XKB_CONFIG_ROOT / XKB_DEFAULT_* set (must not leak: env -i), and with a
keymap file the tool cannot parse (truncated, extra comment) - what the judge does. Exact argv in your report.""")
seat("ExecFixtures", "executor",
     "C1 fixture set: >= 300 (RMLVO, keysym) cases with expect from the judge, in classes.",
     """Build %(W)s/w1/ExecFixtures/fixtures.json: [{"id","class","rmlvo":{"rules","model","layout","variant","options"},"arg","expect":{"stdout","rc"}}]
with expect from 3 identical runs of the pinned judge (clean env). Classes: HOST (layout br, options compose:caps - the host's names), MULTI (2-4
layouts e.g. br,us / us,ru,de with variants), VARIANT (nodeadkeys, thinkpad, abnt2, intl, dvorak...), OPTIONS (lv3:ralt_switch, grp:alt_shift_toggle,
caps:escape, compose:*, altwin:swap_lalt_lwin, ctrl:nocaps), LETTERS, DIGITS, PUNCT (slash, question, backslash, bar, at), DEAD (dead_* keys),
KEYPAD (KP_*), FUNCTION (F1-F35, Return, Tab, BackSpace, Escape), XF86 (XF86Audio*, XF86MonBrightness*), MODIFIER keysyms (Shift_L, ISO_Level3_Shift,
Super_L, Caps_Lock), ABSENT (valid keysym not in the keymap -> what is printed), NUMERIC (0x2f, 47, 0x1000e9), CASE (return vs Return, SLASH vs
slash: how-to-type's lookup is case-sensitive? record), INVALID (rc 2 path), BIND (every distinct keysym the host's `hyprctl binds -j` keys name,
upper-case as Hyprland writes them - read the binds read-only, keep only the key strings). Report class counts and the share of cases whose stdout
has >= 2 table rows.""")
seat("ExecGen", "executor",
     "C1 clause g: a nonce generator of (RMLVO, keysym) cases judged at count time.",
     """Write %(W)s/w1/ExecGen/gen.py: gen_case(rng) -> case drawing rules evdev, models/layouts/variants/options from a frozen snapshot of
`xkbcli list` (store it in your seat dir with its sha256) and keysyms from the header (weighted to keysyms present in the keymap). Run 400 generated
cases against the judge 3x (determinism) and report how many of them a naive tool (first match only, no modifiers) gets right (it must be few).""")
seat("ExecCounterC1", "executor",
     "C1 counter draft quality/counters/c1-r49-keysym.py (at your seat dir), derived from the round-48 C1 counter's sandbox and tripwire.",
     """Read %(L)s/quality/counters/c1-r48-terminal-cache-v2.py (bwrap sandbox, write/fork tripwire, clauses, receipts) and write
%(W)s/w1/ExecCounterC1/c1-r49-keysym.py: --repo --rev --work --nonce; refuses a --work or TMPDIR under /tmp (exit 2; SentScratch); git-reads the
tool at REV (never the working tree); compiles keymaps with the pinned compile-keymap in a clean env (HOME/XDG_* in work); judge = pinned how-to-type;
tool run in bwrap with only the keymap (and header if needed) bound read-only, no network, a fork/exec tripwire (the tool must start no process) and
a write tripwire; clauses: f fixtures (stdout+rc equal), g generated nonce cases, s selftest at REV, r readonly/no-process, t tool present.
Final line `PRED-C1-r49: fixtures=K/F generated=G/N selftest=.. readonly=.. tool=.. verdict=TARGET_MET|TARGET_MISSED` exit 0/1, setup error exit 2.
Run it at %(B)s (tool absent: must MISS) and against ExecRefKeysymA's draft if it exists when you finish (a scratch clone with the draft committed
under a fixture identity, toplevel verified). Receipts in your seat dir.""")
seat("ExecCounterC2", "executor",
     "C2 counter draft quality/counters/c2-r49-bind-entry.py (at your seat dir), from the round-48 C2 counter.",
     """Copy %(L)s/quality/counters/c2-r48-xkb-entry-v2.py to %(W)s/w1/ExecCounterC2/c2-r49-bind-entry.py and adapt it to
corpus/knowledge/hyprland-bind-key-match-r49.md: a entry new at REV (absent at %(B)s); b provenance head (source: >= 3 S### >= S352 rows, mined,
opened 2026-10-27, used-by the entry; verified-at; recheck); c every cited row pin-bound (copy under .ufo/waves/round-49/fetch/, sha256 equal,
tag/commit URL, no branch); d every quote verbatim in its pin at its stated line range, <= 25 words; e >= 6 numbered steps each with a source locator;
f a committed live receipt (hyprctl binds -j shape + getoption resolve_binds_by_sym) whose stated values the entry repeats; g held S319 cited not
re-registered; h Limits section; i lesson Gate rows for every new row. Keep the round-48 fixes (pin mode, quote length, clean-env replay where one
exists). Refuse /tmp TMPDIR. Final line `PRED-C2-r49: clauses=... admitted=N/1 verdict=..`. Run at %(B)s (must MISS). Receipts.""")
seat("ExecControlsC1", "executor",
     "Do-nothing and cheat controls for the C1 counter draft (section 9: a control that meets the target means the counter is wrong).",
     """Build >= 12 control tools in %(W)s/w1/ExecControlsC1/controls/: absent tool; header-only; first-match-only; no-modifiers; a tool that execs
xkbcli/how-to-type (must be stopped by the no-process tripwire); a tool reading a cached answer table keyed by (keymap sha, keysym) built from the
fixture file; a tool reading the fixture file from the repo at run time; a tool that writes a file; a tool that opens a socket; a tool correct on
fixtures but wrong on generated cases (overfit); a selftest-only stub. Score each with ExecCounterC1's draft if it exists (else describe the clause
that must stop it). receipts/controls.txt: control, verdict, the clause that stopped it. Any control scoring TARGET_MET is a finding.""")
seat("ExecControlsC2", "executor",
     "Do-nothing and forgery controls for the C2 counter draft.",
     """Build >= 10 control entries in %(W)s/w1/ExecControlsC2/controls/ (stub with head + one sentence; the round-46 keybind section pasted under a
round-49 head; quotes forged by one word; a branch URL pin; a pin whose digest is edited in both row and file; a live receipt typed by hand;
locators off by one; held S319 re-registered as a new row; steps without locators; a registry row not used by the entry) and score each with
ExecCounterC2's draft (or name the clause that must stop it). receipts/controls.txt.""")
seat("ExecHyprSrc", "executor",
     "Pin and trace Hyprland 0.56.2's bind-key path in source, with computed locators.",
     """Fetch from %(HY)s (commit URL, never a branch) the files that handle binds: src/config/ConfigManager.cpp (handleBind / the key field parse),
src/managers/KeybindManager.cpp (onKeyEvent / handleKeybinds / the keysym used for matching, resolve_binds_by_sym, modmask comparison, keycode binds),
src/managers/KeybindManager.hpp (SKeybind fields), src/config/ConfigDescriptions.hpp (resolve_binds_by_sym description) and anything else the trace
needs; sha256 each into %(W)s/w1/ExecHyprSrc/fetch/ with SHA256SUMS and URLS. Produce trace.md: numbered steps from the bind line to a match, each
with file:line (grep -n computed) and a <= 25-word verbatim quote verified by a script. Note which keysym of a keycode is compared (xkb_state of
which layout, with or without modifiers) and what case-insensitivity applies.""")
seat("ExecXkbSrc", "executor",
     "Pin libxkbcommon 1.13.2's keysym-name and how-to-type sources with computed locators.",
     """Fetch %(XKB)stools/how-to-type.c, src/keysym.c, src/keymap.c, include/xkbcommon/xkbcommon.h (XKB_KEYSYM_CASE_INSENSITIVE docs) into
%(W)s/w1/ExecXkbSrc/fetch/ with SHA256SUMS and URLS; byte-compare the header with the host /usr/include/xkbcommon/xkbcommon.h. Extract located
<= 25-word quotes (verified) for: case-insensitive lookup rule, get_name canonical choice, mods_for_level semantics, how-to-type's table loop and
format strings. Write quotes.md.""")
seat("ExecBindsLive", "executor",
     "Read-only live receipts for C2 and a host join demo for the C1 tool.",
     """Capture, read-only: `hyprctl version` (first line), `hyprctl getoption input:resolve_binds_by_sym -j`, and from `hyprctl binds -j` ONLY the
fields key, keycode, modmask, mouse, catch_all, submap per bind (never description/arg/dispatcher text beyond the dispatcher name), with counts by key
form (named keysym, code:, mouse, switch). Write %(W)s/w1/ExecBindsLive/receipts/binds-shape.txt with a header (command, time, sha256 of the raw JSON,
not the JSON itself). Then, with a keymap compiled from the host's kb names (read ~/.config/hypr/input.conf read-only) and the pinned how-to-type,
list for every distinct keysym the binds name: the keycodes/levels/modifier masks that produce it (receipts/bind-keys.txt) and flag binds whose
keysym is reachable only at level >= 2 or not at all on the host keymap. No device names in any receipt.""")
seat("ExecSessionTriage", "executor",
     "M48-8 part 1: triage every finding of the session-material gate at the base, both scopes.",
     """Run %(L)s/quality/check-session-material.py read-only at %(B)s with --scope ufo and --scope all (from a scratch `git clone --shared` or with
--repo on the lane: it reads git objects only - verify). For EVERY finding (file, rule) classify: SYNTHETIC (fixture/generated material, name the seat
that generated it and the evidence), REAL (host session material: name the class only, never the value), FALSE-POSITIVE (shape match on non-session
text). Check the 47 untracked `*.synthetic` sidecars: what each marks, whether its target is tracked, whether committing it (with a waiver-registry
row per the gate's marker contract) would waive the finding, and whether the sidecar contract accepts it at the tip. Output triage.tsv (file, rule,
count, class, evidence), proposed waiver rows, and a list of REAL files with a remediation proposal (remove from the tip with a digest receipt, or
redact) and the evidence pointers in LOG/SCORECARD/lessons that cite each (so a removal can be judged for harm).""")
seat("ExecSessionShapes", "executor",
     "M48-8 part 2: gate v3 draft - the 16 missed /home/<user> shapes and scopes beyond .ufo/, shown able to fail both ways.",
     """Read %(L)s/.ufo/waves/round-48/w1/SentPrivacy.md (the 16 of 19 missed shapes) and %(L)s/quality/check-session-material.py. Draft
%(W)s/w1/ExecSessionShapes/check-session-material.py (v3) that detects those shapes (classes, e.g. ls -l owner/group columns with the account name,
home paths inside ls/find output with prefixes, cache text) without flagging `~`-written paths or paths quoted in prose sentences, and whose default
scope covers the whole tracked tree (or state why not). Keep every v2 selftest case passing and add one red case per new shape and one green
counter-case per shape; show each new rule fails on its red fixture with the rule removed (mutation) - 'able to fail' receipts. Run v3 at %(B)s
(both scopes) and report the finding counts by rule vs v2.""")
seat("ExecMutantSandbox", "executor",
     "M48-10: a host-state guard for mutants and counters, shown able to fail on a FAKE operator home.",
     """Write %(W)s/w1/ExecMutantSandbox/hostguard.py: run a command with HOME/XDG_CACHE_HOME/XDG_CONFIG_HOME/XDG_DATA_HOME/XDG_STATE_HOME pointed at a
scratch dir (or under bwrap with --tmpfs on the home path), digest a declared list of operator-owned paths before and after (sha256, size, mtime,
labelled `operator-owned`), and fail (exit 3) if any digest changed. Demonstrate it ONLY on a fake operator home you create under your scratch: a
mutant that writes <fake-home>/.cache/xdg-terminal-exec is caught when the guard is pointed at the fake home and run unsandboxed, and is contained
when sandboxed. NEVER point it at the real home for the mutant run; you may run a read-only digest of the real ~/.cache/xdg-terminal-exec once (stat +
sha256, label operator-owned). Receipts + the exact usage the counters should adopt.""")
seat("ExecN4Matrix", "executor",
     "N4: a complete 98-row text receipt of the round-48 C2 v2 matrix, from its committed summary, without rewriting any frozen file.",
     """Read %(L)s/.ufo/waves/round-48/receipts/v2/ (c2v2-revc2counter-matrix.txt and its summary.json) and the generator that wrote them (find it).
Produce %(W)s/w1/ExecN4Matrix/c2v2-matrix-full.txt with one row per variant (98), the two missing ones (a-entry-at-base, a-rev-base-direct) included,
values taken from summary.json, and a check script that asserts row count 98 and set equality with summary.json. Report why the text dropped two.""")
seat("ExecCloneRecipe", "executor",
     "M48-13: the seat clone recipe under a file-size cap, and the owed clause-r mutant attack on the round-48 C1 counter.",
     """(1) Measure which recipes work under `ulimit -f 2048` (1 MiB) and `ulimit -f 65536`: `git clone --shared`, `--no-checkout` + `git archive
<rev> <paths> | tar -x`, sparse checkout, `git --git-dir=%(L)s/.git show REV:path`; record the failing file for each. (2) The owed clause-r mutant
attack: in a scratch clone, build mutants of tools/mado-terminal.py that write a file, fork a child, open a socket (each writing ONLY inside the
sandbox/scratch: HOME and XDG_* in scratch, never the real home) and score them with %(L)s/quality/counters/c1-r48-terminal-cache-v2.py --nonce 4848
(work dir under your scratch); each must read readonly=fail / TARGET_MISSED. Before/after digest of the real ~/.cache/xdg-terminal-exec (read-only
stat+sha256, labelled operator-owned) around the whole attack. Receipts.""")

# ------------------------------------------------------------ scribes (7)
seat("ScrEntry", "scribe",
     "C2 entry draft: corpus/knowledge/hyprland-bind-key-match-r49.md (at your seat dir).",
     """Open the Hyprland sources yourself at %(HY)s (src/config/ConfigManager.cpp, src/managers/KeybindManager.cpp/.hpp,
src/config/ConfigDescriptions.hpp) and libxkbcommon %(XKB)ssrc/keysym.c; draft %(W)s/w1/ScrEntry/hyprland-bind-key-match-r49.md in the lane's
entry shape (read %(L)s/corpus/knowledge/xkb-keymap-compile-r48.md first: provenance head source:/verified-at:/recheck:, numbered steps each with a
locator and <= 25-word verbatim quote, a host section, Limits). Use placeholder row ids S352.. in order of first citation and list them. Every quote
verified by a script against your own pinned copy; locators computed. Cite held S319 for IKeyboard.cpp, never a new row for it.""")
seat("ScrRows", "scribe",
     "SOURCES rows S352.. for C2 (and C1 if the tool cites sources), with Gate lines.",
     """Read %(L)s/corpus/SOURCES.md (registry tops at S351; 11 columns; no '|' inside a cell) and the round-48 rows S340-S351 as the format model.
For each source C2 needs (Hyprland files at efb50993, libxkbcommon 1.13.2 files, the Hyprland wiki Binds page at a pinned commit of hyprwm/hyprland-wiki
- find the commit that matches 0.56.x), OPEN it, then draft the row and a Gate line (URL, access date 2026-10-27, located <= 25-word quote, the
teaches it grounds). Also draft the rejects you hit (unpinned wiki URLs, ArchWiki pages that do not state 0.56.2 behaviour, held-duplicate URLs) with
reason and flip. Write %(W)s/w1/ScrRows/rows.md and gate.md; run the census on a scratch copy of the registry with your rows appended
(/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch copy>) and paste the result.""")
seat("ScrLesson", "scribe",
     "Round-49 lesson skeleton corpus/lessons/round-49.md (at your seat dir).",
     """Using %(L)s/corpus/lessons/round-48.md as the shape (## Gate, ### Rejected after opening, ### Census before -> after, ### Registry changes,
### Id guard and quarantine, ### considerthese, ## Search log, ## Mistakes, ## Spot-check (pending non-author), ## Frontier), draft
%(W)s/w1/ScrLesson/round-49.md with every section the round needs (C1 keysym tool, C2 bind entry, routed items N1-N5, M48-8, M48-10, M48-13,
SentScratch, the 47 sidecars) and placeholders marked TODO-L1 where data is pending. The spot-check shape line must name the counts the Gate will
really hold (round-48 N3: a template said 'five' while the Gate held fifteen) - write it as a computed count, not a typed number.""")
seat("ScrCorrections", "scribe",
     "N1, N2, N3, N5: append-only correction lines, each with its counting command or located evidence.",
     """Draft %(W)s/w1/ScrCorrections/corrections.md: (N1) the untracked count is 47 (`git -C %(L)s status --porcelain -uall | wc -l` at %(B)s -
run it now and paste; 45 under round-45/w1, 2 under round-46/w1); (N2) a lesson line saying that `host_cache_untouched_sha256` in
.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4 equals `printf 'r48-w2\\n' | sha256sum` (verify) i.e. the w2 mutant's bytes, not an
untouched operator cache; (N3) a correction for corpus/lessons/round-48.md:425 (compute the Gate's admit/reject counts with a command); (N5) the
GitLab files-API fallback URL form for S346/S347 (fetch both through the API, sha256 equal to the row digests - paste). Each line names its target
file:line, is append-only, and carries its command and output.""")
seat("ScrSkill", "scribe",
     "SKILL.md section draft: binds, keysyms and the keymap (round 49).",
     """Read %(L)s/SKILL.md sections 'XKB keymap compile (round 48)' and 'Terminal cache (round 48)' (grep -n) as the shape. Draft
%(W)s/w1/ScrSkill/skill-section.md: a decision table 'a bind on keysym X does not fire on layout L: check ...' and an error-pattern table, each row
citing a source locator (Hyprland/libxkbcommon files you open at %(HY)s and %(XKB)s) or a live receipt; plus the usage lines of
tools/mado-keysym.py how-to-type. No sentence without a locator.""")
seat("ScrToolLedger", "scribe",
     "considerthese 2026-10-26 proposal 2 (refused round 47 because ledger rows were wrong): a live-state tool ledger whose every row is verified.",
     """Read %(L)s/considerthese/2026-10-26.md proposal 2 and the round-47 refusal (%(L)s/.ufo/waves/round-47/w2/ExecToolLedger.md if present;
grep the round-47 lesson). For every tool under %(L)s/tools/ that reads live state, draft a row: tool, the question it answers, its last committed
live-run receipt (path at %(B)s, verified to exist with git ls-tree), the verdict line in that receipt (quoted verbatim, verified), the round. Write
%(W)s/w1/ScrToolLedger/ledger.md and a check script that re-verifies every row from git objects (exit 1 on any wrong row).""")
seat("ScrQuality", "scribe",
     "Candidate QUALITY.md criteria 100+ from the round-48 mistakes and closure (M48-8, M48-10, N2, N4, M48-13).",
     """Read %(L)s/corpus/QUALITY.md (criteria 1-99; the criterion format with lesson citation and instrument) and the round-48 lesson ## Mistakes and
closure section 6. Draft %(W)s/w1/ScrQuality/criteria.md: one criterion per uncaptured class (host-write by a mutant; a receipt field whose name
misdescribes its value; a text receipt that drops rows its summary holds; an instrument's coverage envelope narrower than its registry wording), each
citing its lesson line and naming an instrument that can fail (command + the red state it would show).""")

# ------------------------------------------------------------ scouts (4)
seat("ScoutHowToType", "scout",
     "How-to-type's exact output contract at libxkbcommon 1.13.2.",
     """Read %(XKB)stools/how-to-type.c in full; enumerate every stdout/stderr string, column widths/format strings, sort/iteration order (keycodes
ascending? layouts? levels? masks order?), the Compose section path, error exits and their codes, and the arg parsing (--keysym, numeric forms).
Write %(W)s/w1/ScoutHowToType/contract.md with file:line for each, and the list of behaviours the tool must reproduce under --disable-compose.""")
seat("ScoutHyprBinds", "scout",
     "Hyprland docs and issues on bind key matching, layout dependence and resolve_binds_by_sym.",
     """Find the hyprland-wiki commit that documents 0.56.x binds (hyprwm/hyprland-wiki; pages Configuring/Binds, Variables input section) and read
it at that commit: key names, `code:`, keysym case, `resolve_binds_by_sym`, layout notes. Search Hyprland issues/discussions for binds failing on
non-latin or non-us layouts, keysym case, `code:` advice (record queries, counts, inclusions; pinned URLs). Write %(W)s/w1/ScoutHyprBinds/report.md
with pinned URLs and located quotes (verified against your fetched copy).""")
seat("ScoutShokuknow", "scout",
     "Assimilation check for this round (read-only package).",
     """Read %(P)s/MERGE-REPORT.md and %(P)s/knowledge/ (READ-ONLY; run no campaign tool). Is there any theme on binds, keysyms, keymaps or input?
Run the id-collision guard into %(W)s/w1/ScoutShokuknow/ (reg-ids from %(L)s/corpus/SOURCES.md, staged-ids from %(P)s/SOURCES.append.md, both with
the 0-3 leading space pattern `^ {0,3}\\|[[:space:]]*S[0-9]{3,}`; collisions = comm -12) and prove the guard once on a scratch registry with an
indented `  | S002 |` row (nonempty collisions). Derive the quarantine slice from
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data rows with lane `mado`, a round cell and an S-id).
Write report.md with both id lists' counts, collision count, guard proof and slice.""")
seat("ScoutHeld", "scout",
     "What the lane already holds on bind keys and keysyms (so C2 does not re-claim held ground).",
     """grep %(L)s/corpus/knowledge, SKILL.md, corpus/README.md and corpus/SOURCES.md at %(B)s for keysym, resolve_binds_by_sym, code:, xkb_keysym,
KeybindManager, handleBind; list every held sentence with path:line and whether it is [OBS]/[INF-docs]/sourced; list held rows that cite Hyprland
bind sources (URL + id). Write %(W)s/w1/ScoutHeld/held.md, ending with the exact sentences a new entry must not restate as new.""")

# ------------------------------------------------------------ critics (5)
seat("CritPremiseC1", "critic",
     "Attack C1's premise and judge.",
     """Is how-to-type a deterministic judge (locale, env, compose tables, keymap format default 2 vs compile-keymap's output format)? Can the
serialized keymap carry constructs the draft contract cannot honestly cover? Is parity with how-to-type meaningful for binds, given Hyprland's own
matching (ScoutHyprBinds)? Does the do-nothing control (absent tool) and a first-match tool really miss? Run probes (clean env, scratch HOME).
Write %(W)s/w1/CritPremiseC1/findings.md, each with a command and output.""")
seat("CritPremiseC2", "critic",
     "Attack C2's premise: is the ground open at base and in province, and can the entry be grounded at 0.56.2?",
     """Check %(L)s/corpus/knowledge/keybind-rule-semantics.md section 2.3, hyprland-input-devices-r46.md:71, SKILL.md and README for held bind-key
ground; check sibling lanes' PROVINCE/README (read-only) for the same ground; check that 0.56.2 sources (commit efb50993) contain the logic the entry
will claim (not a later refactor). Write %(W)s/w1/CritPremiseC2/findings.md.""")
seat("CritClaimSizing", "critic",
     "Section 9 sizing: cheats and universal clauses in both draft predicates.",
     """Read claims.md and whatever counter drafts exist in %(W)s/w1/ExecCounterC1 and ExecCounterC2 when you start (re-read before finishing).
List >= 10 cheats per claim (table-lookup tool, subprocess judge call, fixture-file read, a judge-output cache left in the sandbox, a typed live
receipt, quote-in-pin but unsupported claim, a step citing a line that says something else, ...), say which clause stops each or that none does,
and propose the clause or fixture. Write %(W)s/w1/CritClaimSizing/findings.md.""")
seat("CritRoutedItems", "critic",
     "Are the round-48 routed items still open at base, and do the proposed fixes close them?",
     """For N1-N5, M48-8, M48-10, M48-13, SentScratch F1-F7 and the registration-v2 residuals, check at %(B)s whether each is open (command +
output), what the minimal honest fix is, and what would show the fix able to fail. One section each. Write %(W)s/w1/CritRoutedItems/findings.md.""")
seat("CritSidecars", "critic",
     "The 47 untracked *.synthetic sidecars: commit or remove?",
     """Inspect the 47 untracked `*.synthetic` files under %(L)s/.ufo/waves/round-45/w1/RevengerOmarchy/ and round-46/w1/ (git status --porcelain
-uall), their sha256 against %(L)s/.ufo/waves/round-48/w1/ExecSessionMarker/SHA256SUMS, what the gate does with them at the tip if committed (score a
scratch mirror), and whether committing them would waive REAL material (attack: a sidecar that marks a file holding real session data). Recommend
commit (with which waiver rows) or remove (with which digest receipt), with evidence. Write %(W)s/w1/CritSidecars/findings.md.""")

# ------------------------------------------------------------ connectors (2), sentinels (2), reviewers (2), revenger (1), mutation-tester (2)
seat("ConnSiblings", "connector",
     "Sibling-overlap scan for both claims.",
     """Scan sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: PROVINCE.md, corpus/README.md, corpus/SOURCES.md) for
keysym/keymap/bind/input ground. Report contested scope (report, never absorb) and propose a PROVINCE.md refinement line for mado (or none).
Write %(W)s/w1/ConnSiblings/report.md.""")
seat("ConnClaims", "connector",
     "Cross-claim pre-freeze checklist from the round-48 closure.",
     """Read %(L)s/corpus/lessons/round-48-verifier-spotcheck.md, %(L)s/.ufo/waves/round-48/registration-v2.md and QUALITY 91-99; produce a
pre-freeze checklist for round 49: what the freeze commit must contain (counters, fixtures, pins, references, controls, base receipts), separability
proofs, which closure defects recur (post-freeze narrowing, unreceipted numbers, mislabelled receipt fields, incomplete text receipts, host writes)
and how to make each impossible this round. Write %(W)s/w1/ConnClaims/report.md.""")
seat("SentHost", "sentinel",
     "Host safety of this round's probes and counters.",
     """Review what this round runs: xkbcli compile-keymap / how-to-type (do they read user include paths ~/.config/xkb, ~/.xkb, /etc/xkb, env
XKB_*; can they write anything; compose tables under ~/.XCompose), hyprctl binds/getoption/devices (read verbs only), bwrap sandboxes, mutants of
round-48 tools. Propose exact guards (env, bwrap binds, tripwires) for counters and seat prompts. Read-only probes only. Write
%(W)s/w1/SentHost/report.md.""")
seat("SentPrivacy", "sentinel",
     "Privacy of this round's new receipts.",
     """Which host material could the round's receipts carry (bind exec commands with home paths and private script names, bind descriptions,
device names, keymap text, ls/home listings)? Check the gate (%(L)s/quality/check-session-material.py and ExecSessionShapes' v3 draft if present)
catches them; list classes it misses (classes only, never values). Write %(W)s/w1/SentPrivacy/report.md.""")
seat("RevR48", "reviewer",
     "Review the round-48 closure's routed items against the lane at base.",
     """Read %(L)s/corpus/lessons/round-48-verifier-spotcheck.md and verify N1-N5 and the carried items with commands (git show, grep -n, sha256sum).
List any defect the closure missed (e.g. other receipts whose field names misdescribe values, other text receipts dropping rows). Write
%(W)s/w1/RevR48/review.md.""")
seat("RevRegResiduals", "reviewer",
     "The round-48 registration-v2 residuals: receipt generator path and the uncited meson pin.",
     """Read %(L)s/.ufo/waves/round-48/registration-v2.md:103-110 and verify each residual at %(B)s: where the receipt generator really is vs what the
receipt header names; whether fetch/xkbcommon-meson.build is cited by any row or entry (git grep). Propose the minimal append-only fix for each
(errata line, or a row) without editing frozen bytes. Write %(W)s/w1/RevRegResiduals/review.md.""")
seat("RevengerHowToType", "revenger",
     "Intent and history of how-to-type and xkb_keymap_key_get_mods_for_level upstream.",
     """Reverse-engineer why how-to-type prints what it prints: upstream commits (github.com/xkbcommon/libxkbcommon, commit URLs) that introduced
how-to-type, the --keysym option, the Lock-combination masks, the canonical keysym name selection, the 1.13 keymap format 2 default. Which outputs
changed across 1.11-1.13 (so the pin matters)? Write %(W)s/w1/RevengerHowToType/report.md with commit-pinned citations.""")
seat("MutGate", "mutation-tester",
     "The owed gate both-ways demonstration and a mutation run of the session-material gate.",
     """Mutate %(L)s/quality/check-session-material.py in a scratch copy (each rule's predicate, the scope switch, the waiver/sidecar acceptance, the
summary arithmetic): >= 20 mutants; run its --selftest per mutant; list survivors. Then the both-ways demonstration on a scratch fixture repo
(toplevel verified): a red state (real-shaped synthetic material unmarked -> findings > 0, exit 1) and a green state differing only by the marker ->
waived, exit 0. Receipts in %(W)s/w1/MutGate/.""")
seat("MutCounterC1Draft", "mutation-tester",
     "Mutation-test the C1 counter draft's clauses as soon as it exists (re-read %(W)s/w1/ExecCounterC1/ until it appears; if it never appears, mutate the round-48 C1 counter's sandbox/tripwire code instead).",
     """For each clause (f, g, s, r, t) build a mutant of the counter that weakens it and a tool that exploits the weakened clause; a clause whose
weakening no exploit notices is a finding. HOME/XDG_* in scratch for every run. Receipts in %(W)s/w1/MutCounterC1Draft/.""")

n = len(items)
assert 32 <= n <= 64, n
assert len({i["name"] for i in items}) == n
print(n, dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-49/w1", "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
