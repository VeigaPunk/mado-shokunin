# Seat ExecIndepB — round 46 w1, claim C1 (independent implementation)

Role: second independent implementation of the frozen C1 contract, different author habits from the L1
reference. Everything below is evidence I actually ran; receipt paths are relative to
`mado-shokunin/.ufo/waves/round-46/w1/ExecIndepB/`.

## 1. Deliverable

| item | value |
|---|---|
| tool source | `.ufo/waves/round-46/w1/ExecIndepB/mado-devices.py` (665 lines) |
| sha256 | `5a23dd9336b50071297d63606f0eca428daaa9ca33014bd2123e47cc9e117173` (`receipts/tool-sha256.txt`) |
| scored clone tip | `d224d6f3cd010874be7f9c5268c170308ca8dd62` on base `8c5434c6…` (`receipts/clone-commit.txt`) |
| selftest | `MADO_DEVICES_SELFTEST: 62/62 passed`, exit 0 (`receipts/selftest.txt`) |
| architecture | lexer (`raw_lines`, `cut_comment`, `tokenize`) → `Machine` state machine (stack / selected device / failed-scope status) → render; stdlib only, no subprocess, no socket |

Not installed in the lane (`tools/mado-devices.py` is the L1's integration step); the scored copy is the
committed blob in the throwaway clone at the tip named above.

Structure differs from the reference intentionally: the reference exposes `parse_config`/`State`/`report`
helpers, mine is a token stream (`directive`/`open`/`close`/`assign`) consumed by one `Machine.feed`;
`receipts/tool-shape.txt` is the computed `grep -n '^class \|^def '` listing.

## 2. Frozen-counter score (PRED-C1-r46)

Recipe: shared clone of the lane at `8c5434c6`, tool committed at `tools/mado-devices.py`, then
`c1-r46-devices.py --repo <clone> --rev HEAD --work /fast/scratch/hyaku/mado-r46/ExecIndepB/w --nonce N`.

| nonce | verdict line | receipt |
|---|---|---|
| 46 | `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET … seeds=46,46` | `receipts/c1-r46-nonce-46.txt:95` |
| 3 | same, `seeds=46,3` | `receipts/c1-r46-nonce-3.txt:95` |
| 99 | same, `seeds=46,99` | `receipts/c1-r46-nonce-99.txt:95` |

Clause detail (`receipts/c1-r46-nonce-46.txt`): `clause=a tool=present` (:1); `clause=s rc=0 last='MADO_DEVICES_SELFTEST: 62/62 passed'` (:2);
all 90 `clause=f` lines `pass` (each judged as 46A + 46B + nonce-A); `clause=g generated=150/150` (:93);
`clause=r marker=absent` (:94) — no `hyprctl`/`libinput`/`journalctl`/`udevadm` executed, my tool runs none.

### Failing fixtures and ruling

**None.** 0 of 90 fixtures failed at every nonce, and 0 of 450 generated cases failed (150 × 3 runs).
There is therefore no tool-vs-contract ruling to make for a failing fixture. The only divergence class I
found was found before scoring, by oracle probing, and is reported in §3.2 (ruling: tool).

## 3. Independent differential evidence (beyond the counter)

### 3.1 Oracle probe suite — 40 probes, 40 exact parities

I used the pinned reference as a black-box oracle (probes are subprocess calls) on 35 contract-edge inputs
plus 5 late additions. Design note for the independence claim: I read the reference's docstring (its
contract) and nothing else by hand; the `read` tool's first, non-raw response additionally printed the
file's automatic *declarations* preview — module-level constants, regex names and the names of top-level
functions/classes such as `MAX_BYTES`, `FLOAT_RE`, `State`, `parse_config` — before I switched to raw line
ranges; no function body was read, and no semantics
below come from that preview except where the docstring already states the same value. Receipts:
`receipts/oracle-probes.txt` holds, per probe, the
command, the oracle rc/stdout, and a `PARITY ok` line for my tool. Index with line numbers:
`receipts/probe-index.txt`. `grep -c 'PARITY ok'` = 40, `grep MISMATCH` = none.

### 3.2 Divergence found by probing and fixed in the tool (ruling: tool)

A line whose LHS is empty (`" = kb_layout"`, `" = $x"`, `" =\t"`) is **ignored outright** by the reference:
inside a device block it neither selects, nor stores, nor adds to `unsupported`, even when the RHS holds
`$` or `{{`. Proof: `receipts/oracle-probes.txt:299` (`empty-lhs-inside-block-ignored`, `unsupported=1`
only from the other line), `:308` (`empty-lhs-dollar-not-counted`, `unsupported=0`), `:317`
(`empty-lhs-expression-not-counted`), while `:326` (`flat-device-empty-field-counted`) shows the
non-empty `device:` LHS *is* counted.

My first build modelled the joined `device:` KEY and counted those lines; the differential fuzz caught it
(12/400 mismatches, all `unsupported` over-counts). Ruling: **tool** — the reference behaviour is right and
the docstring simply never says it (§4 A9); I added `if not lhs: return` to `Machine.assign` and fuzz went
to 0/400. The pre-fix fuzz output was dev-loop output and is not retained as a receipt; the citable fact is
the oracle probe receipt above.

### 3.3 Randomised differential fuzz

`receipts/oracle-fuzz.txt:2` → `FUZZ cases=400 mismatches=0` (grammar: continuation joins, `##` escapes,
CR/VT, brackets with spaces/empties, nested blocks, directives, `$`/`{{`, `[[EMPTY]]`, the whole `FACTORS`
list, booleans/strings/absent fields, `belongsTo`/`touch` lists).
`receipts/oracle-fuzz.txt:5` → `FUZZ2 cases=3000 mismatches=0 model_exceptions=0` (wider grammar incl.
`device: = x`, `device[x]:name`, `\u000b` separators, `1e-400`, `5e-324`, `--3`, `0X1P1`, missing
`mice`, non-list `keyboards`, and `Setup`/`bad_json` parity). Both compare full `(stdout lines, rc)`.

### 3.4 One deliberate, out-of-contract divergence (ruling: tool; contract gap)

A JSON integer `scrollFactor` beyond double range (`10**400`) makes the reference raise
`OverflowError: int too large to convert to float` (traceback, no contract output); my tool prints
`reported=? verdict=DIFFER` and rc 1. Receipt: `receipts/robustness-huge-int.txt`. No fixture or generated
case (all `scrollFactor` values are floats from the fixed list) reaches this, so it is not a scoring risk.
Ruling: the tool behaviour is the defensible one; see §4 A12 for proposed wording.

## 4. Ambiguous contract sentences and proposed wording

Locators are computed `grep -n` hits saved in `receipts/contract-locators.txt` (the docstring is lines 2–89
of `.ufo/waves/round-46/l1-draft/mado-devices.py`). "Probe" = a probe name inside
`receipts/oracle-probes.txt` with its line in `receipts/probe-index.txt`.

### A1 — "with a bracket name N and KEY `device:F`" (L52): what is F?
Read literally, F is one segment. The reference instead takes everything after `device:` as F, and its
behaviour depends on that: a bracket line whose cut KEY is `device:<a>:<b>` creates N, ignores the field,
and adds **no** `unsupported`. Evidence: probe `bracket-inside-block-field-not-device-key` (`:1`) →
`name="X" keys=0`, `unsupported=0`; `three-part-key-in-fresh-scope` (`:272`) → `unsupported=1` (only the
following line); `flat-device-key-no-current` (`:60`) → `unsupported=1`.
Proposed wording: "with a bracket name N and a KEY that starts with `device:`: device N is created if
absent; the text after `device:` is F and may contain `:`; F exactly one of the DEVICE KEYS sets that key of
N; F exactly `name` adds one to `unsupported`; any other F is ignored. A bracket line never touches the
current device, the per-scope status, or `unsupported` in any other way."

### A2 — is the bracket cut from the KEY or from the LHS? (L46–47)
L46 says the KEY is stack and LHS joined with `:`; L47 says the BRACKET NAME is cut out of the KEY. The
reference cuts the **joined** KEY. So `[X]:kb_layout` inside a `device {` block becomes
`device::kb_layout` (field `:kb_layout`, ignored), not `device:kb_layout`. Evidence: probe
`bracket-inside-block-field-not-device-key` (`:1`) — `keys=0` — against `bracket-top-level-stores` (`:11`)
— `keys=1`; also `bracket-name-with-space` (`:252`) keeps the inner space.
Proposed wording: "The BRACKET NAME is cut out of the joined KEY, before the relevance test: cutting `[N]`
out of `device:[N]:kb_layout` leaves `device::kb_layout`, whose F is `:kb_layout`."

### A3 — what exactly does the failed-device state do, and when does it end? (L55, L58–60)
L58–60 says a `device:F` line with no current device adds one to `unsupported` and that later `device:` lines
"go the same way until the stack empties"; L54–55 defines `name` selection only for the no-current case and
says nothing about a *second* `name`. The reference treats a second `name` (a rename) as entering the same
failed state: every later `device:F` line — including `name` — adds one to `unsupported`, nothing is
selected or stored, and the state (like the current device) survives inner `}` pops and only clears when a
`}` empties the stack. Evidence: probe `rename-poisons` (`:79`) → `unsupported=3`, block keys 0;
`rename-then-name-does-not-select` (`:89`) → third `name` does not select; `block-first-not-name-poisons`
(`:99`); `broken-survives-inner-close` (`:118`); `second-block-starts-fresh` (`:127`).
Proposed wording: "A rename (a `name` line while a device is selected) adds one to `unsupported` and puts
the scope in the failed state. In the failed state every later `device:F` line without a bracket name —
including `name` — adds one to `unsupported`; no device is selected or written. The failed state and the
current device are forgotten only when a `}` pops the last stack entry, or at the start of the next file."

### A4 — "until the stack empties" applied to a `}` on an already-empty stack (L55)
A `}` that pops nothing leaves a flat-selected device selected. Evidence: probe
`close-on-empty-stack-keeps-binding` (`:108`) → `device:name = kbd`, `}`, `device:kb_layout = fr` still
gives `kbd keys=1`.
Proposed wording: "Only a `}` that actually pops a non-empty stack can empty it; the current device and the
failed state are then forgotten. A `}` on an already-empty stack changes nothing."

### A5 — "leaves the key unset" for a later bad `scroll_factor` (L64)
Ambiguous between "no value this line" and "remove any earlier value". The reference keeps the earlier
value and keeps the key counted. Evidence: probe `scroll-invalid-after-valid-keeps-value` (`:137`) →
`keys=1` with `scroll_factor=1.00`.
Proposed wording: "leaves the key exactly as it was: a value set by an earlier line stays set and stays
counted in `keys`; only the current line contributes nothing."

### A6 — scope of the `[[EMPTY]]` marker (L66)
The sentence sits in the `scroll_factor` paragraph but applies to every stored `kb_*` value, and never to
device names. Evidence: probe `empty-marker-in-name-is-literal` (`:177`) → block named literally
`[[EMPTY]]`; `empty-marker-kb-file` (`:187`) → `kb_file=-` (reads as `""`).
Proposed wording: "Every stored `kb_*` value equal to `[[EMPTY]]` is stored as `""`. A device name taken
from `name =` or from a bracket is stored literally, including `[[EMPTY]]`."

### A7 — `kb_file=<set|->` is printed but never defined (L81)
The output spec names the field; the only place the meaning appears is the reference's own selftest
(locator `contract-locators.txt`, pattern `kb_file=set`, hit at L508). The rule is: `set` iff the expected
`kb_file` is non-empty. Evidence: probe `empty-marker-kb-file` (`:187`) → `-`; fixture `kb-file` → `set`.
Proposed wording: "`kb_file=set` when the expected kb_file (device block first, else the global) is not the
empty string, else `kb_file=-`."

### A8 — ordering of `usage|unreadable|too_large|bad_json` (L29–31)
The sentence gives the reason vocabulary, not the precedence. The reference reads *all* inputs before it
validates JSON: usage → `--devices` read → each `--config` read in order → JSON validation. Evidence: probe
`precedence-bad-dump-plus-missing-config` (`:344`) → `SETUP unreadable`;
`precedence-bad-dump-plus-big-config` (`:350`) → `SETUP too_large`;
`precedence-big-dump-plus-missing-config` (`:356`) → `SETUP too_large`;
`precedence-missing-devices-plus-big-config` (`:362`) → `SETUP unreadable`.
Proposed wording: "After a usage check, read the `--devices` input and then every `--config` input in
argument order, raising the first read failure; only then decode and validate the devices JSON. Read
failures therefore outrank `bad_json`."

### A9 — a line whose LHS is empty (L44–49)
No rule; the reference ignores the line entirely (no KEY built, no relevance test, no `unsupported`).
Evidence: probes `empty-lhs-inside-block-ignored` (`:299`), `empty-lhs-dollar-not-counted` (`:308`),
`empty-lhs-expression-not-counted` (`:317`); contrast `flat-device-empty-field-counted` (`:326`) and
`device-name-field-with-trailing-colon` (`:335`) where the LHS itself is `device:` and *is* counted.
Proposed wording: "A key line whose stripped LHS is empty is ignored entirely (the `$`, `{{` and backslash
checks included)."

### A10 — `differ=` outside the DIFFER clause, and negative-zero clamping (L73, L75–76, L81)
L73 attaches `differ=` to the DIFFER branch, but the output line (L81) requires it for every verdict; the
reference always fills it with the unequal names (`-` when none), including VIRTUAL and FALLBACK. Evidence:
fixture `virtual` (`receipts/c1-r46-nonce-46.txt:30`, `pass`) whose expected line carries
`differ=layout verdict=VIRTUAL`; probe `scroll-negative-zero` (`:147`) → `scroll_factor=-0.00`.
Proposed wording: "`differ=` is always the comma-joined list of unequal names in the order layout, variant,
options, model, rules (`-` when empty), independent of the verdict"; and "the expected value is
`min(max(v, 0.0), 100.0)`, preserving the sign of `-0.0`, and both values are printed with `%.2f`".

### A11 — directive regex anchoring (L40)
"one matching `#[ \t]*hyprlang\b`" does not say whether the match is anchored. It is anchored at the start
of the already left-stripped line: `## hyprlang if X` counts 0. Evidence: probe
`directive-double-hash-not-counted` (`:196`).
Proposed wording: "a line starting with `#` counts as a directive when the text from that first `#` matches
`#[ \t]*hyprlang\b` at the start; a second `#` before `hyprlang` makes it a plain comment."

### A12 — "a finite number (not a boolean)" for `scrollFactor` (L75–76)
The clause does not say what happens to a JSON number that cannot be represented as a double. The reference
crashes (`OverflowError`) on an integer `scrollFactor` of `10**400`; my tool treats it as not comparable.
Evidence: `receipts/robustness-huge-int.txt`. Not reachable from the frozen fixtures or generator.
Proposed wording: "`scrollFactor` is comparable only when it is a JSON number (boolean excluded) that
converts to a finite IEEE-754 double; every other value prints `?` and gives DIFFER."

## 5. Risks

1. **Contract gaps are load-bearing.** Fixtures and generated cases cannot distinguish a docstring-only
   reading from the reference on A1–A5, A9 and A11; my build only matched because I probed the reference.
   A third implementer could be "correct per docstring" and still fail. The wording proposals in §4 are the
   fix; the L1 owns whether to land them (frozen files are untouched here).
2. **Frozen reference crash** on out-of-range integer `scrollFactor` (`receipts/robustness-huge-int.txt`).
   Not reachable from the frozen fixtures/generator; no action available to me (counter and reference are
   frozen).
3. **No live-host run of my tool.** The host session is read-only for this seat and every mutating
   `hyprctl` verb is forbidden, so I did not run `tools/mado-devices.py` against the live dump; the L1's
   live receipt (`receipts/live-devices-host-l1.txt`) is the operability evidence. My tool is a pure join
   and the score path never executes `hyprctl`, so this is a confirmation gap only.

## 6. Hygiene

- Wrote only inside this seat directory: `mado-devices.py`, this report, and `receipts/` (12 files). No lane
  tracked file, no `.ufo/state/`, no fleet-root file, no jj/git index of the lane was touched.
- One throwaway git clone under `/fast/scratch/hyaku/mado-r46/ExecIndepB/` (toplevel asserted before the
  first commit; every git call used `-C "$D"`); scratch deleted after the receipts were copied.
- No package installs, no pacman, no host-service interaction, no compositor mutation. Tool runtime is
  stdlib-only (`json`, `math`, `os`, `re`, `stat`, `struct`, `sys`); clause=r confirms no external binary
  ran.

Report path: `.ufo/waves/round-46/w1/ExecIndepB.md`
