# ConnCrossClaim — cross-claim pattern scan: do C1 and C2 lean on the same unverified assumption?

Seat: ConnCrossClaim (connector, leaf). Round 46 w1. Date 2026-10-26.
Method: read the frozen registration (`.ufo/waves/round-46/registration.md`), the C1 reference contract
(`.ufo/waves/round-46/l1-draft/mado-devices.py`, docstring + body), the C2 draft entry
(`.ufo/waves/round-46/l1-draft/entry.md`), both counter docstrings, both controls receipts
(`receipts/ctl-c1.txt`, `receipts/ctl-c2.txt`), the fixture list and generator constants
(`quality/counters/c1-r46-fixtures.json`, `quality/counters/c1-r46-devices.py`), and all ten pins under
`.ufo/waves/round-46/fetch/`. Every entry locator cited below was re-verified against the pinned bytes by line
(`grep -n` / `sed -n`), not typed from memory. Round-45 comparison used `tools/mado-monitors.py`,
`corpus/knowledge/hyprland-monitor-rule-r45.md`, `.ufo/waves/round-45/registration-v2.md` (the w1 failure
classes) and `corpus/lessons/round-45-verifier-spotcheck.md` §6.

## 1. Shared factual assumptions — both claims rely on them, and all are pin-backed

| # | Assumption | C1 use | C2 use | Pin support (verified) |
|---|---|---|---|---|
| A | Per-key name resolution: device block value counts only when the block SETS the key, else global `input:` fallback | expected_names() (reference `:364-375`) | entry step 3 | `Hyprland-ConfigManager.cpp:1119` `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`; getters at `Hyprland-InputManager.cpp:1226-1231` |
| B | Global defaults: layout `us`, the other four empty | expected_names default branch | entry step 3; census `default_layout=us` | `Hyprland-ConfigValues.cpp:272` (`MS<String>("input:kb_layout", …, "us",`); device defaults `Hyprland-ConfigManager.cpp:518-540` |
| C | FALLBACK = reported layout `us` + four empties, written only by the failed-keymap reset | FALLBACK verdict (`:410-412`) | entry step 4; census `fallback_layout=us` | `Hyprland-IKeyboard.cpp:109-113` — the only writers of `m_currentRules` in the pin are `:66` (store input) and `:109-113` (reset; quote `:113` `m_currentRules.layout  = "us";`) |
| D | The dump prints stored rules and `scrollFactor` with two decimals; unset prints -1 | reported names; `%.2f` compare | entry step 5; census `json_scroll_decimals=2` | `Hyprland-HyprCtl.cpp:785-802` (keyboard fields), `:769` (`"scrollFactor": {:.2f}`), `:773` `m->m_scrollFactor.value_or(-1))` |
| E | Pointer factor = device block `scroll_factor` clamped 0..100 only when explicitly set; global `input:scroll_factor` never reaches the field | mouse expected factor (`:424-425`) | entry step 5; census `scroll_factor_max=100` | `Hyprland-InputManager.cpp:1380` `std::clamp(…getDeviceFloat(devname, "scroll_factor", …), 0.F, 100.F)` under `deviceConfigExplicitlySet` at `:1379`; the fallback arg is dead in that branch; separate global at `Hyprland-ConfigValues.cpp:290` |
| F | Virtual keyboards: name starts `hl-virtual-keyboard`; client keymap overrides; rules printed are not a keymap witness | VIRTUAL verdict | entry step 6; census `virtual_prefix=hl-virtual-keyboard` | `Hyprland-protocols-VirtualKeyboard.cpp:12` `std::string name = "hl-virtual-keyboard";`; `:41` `m_keymapOverridden = true;` (`Hyprland-VirtualKeyboard.cpp:41`); early return `Hyprland-IKeyboard.cpp:60-64` |
| G | Device names: lower-cased, space/newline/comma → `-`, `-N` dup suffix; block lookup compares the stored key exactly (case-sensitive) | MATCHED/NO_SUCH_DEVICE; `case-exact-dump-name` fixture | entry step 7 | `Hyprland-MiscFunctions.cpp:782` `case ',': return '-';` (`:777-789`); `Hyprland-InputManager.cpp:2124` dup suffix; exact `!=` in `hyprlang-config.cpp:1112-1124` (`getSpecialConfigValuePtr`/`specialCategoryExistsForKey`); space→`-` at `Hyprland-ConfigManager.cpp:1198` |
| H | hyprlang 0.6.8 line grammar: backslash continuation, `##` escape with two-char resume, bracket-name cut, first-value-must-be-the-key error, current special key reset at last close | parse_config (`:240-302`), cut_comment (`:220-228`), join_continuations (`:206-218`) | entry steps 1-2 | `hyprlang-config.cpp:44-66` (continuation, `MULTILINE_SPACE_CHARSET = " \t"` at `:32`); `:684-706` (`##` loop, resume `lastHashPos = commentPos + 2`); `:291-320` (bracket cut); `:435` error message; `:885-899` (reset at close) |
| I | Stored `[[EMPTY]]` reads as the empty string | EMPTY sentinel in expected_names | entry step 3 | `Hyprland-ConfigManager.cpp:1156-1168` (`if (VAL == STRVAL_EMPTY) return "";`) |
| J | A non-empty kb_file is tried before the names compile | kb_file=`set|-` info field | entry step 4 | `Hyprland-IKeyboard.cpp:87-96` (file branch precedes `xkb_keymap_new_from_names2` at `:99`) |

The C2 census line (`hyprland input-device default_layout=us fallback_layout=us device_keys=47
scroll_factor_max=100 json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard`) recomputes from the pins
(counter clause h): `device_keys=47` verified — 47 lines carry `addSpecialConfigValue("device", "` in
`Hyprland-ConfigManager.cpp` (lines 518-565, last at `:565`); the other five tokens verified above.

## 2. Assumptions only the reference carries (no pin backs them) — flagged

**F1 (the one that matters): special `scroll_factor` values are "unsupported", but the pins say Hyprland
handles them.** The reference's `read_float` (`l1-draft/mado-devices.py:230-242`) returns `unsupported` for
an inf/nan/hex prefix (`SPECIAL_RE`), for an f32-infinite value, and for a nonzero value below `2**-126`
(`FLT_MIN`), and `unset` for a non-matching prefix. The pins show different reality:

- `hyprlang-config.cpp:467` `VALUEIT->second.setFrom(std::stof(value));` — `std::stof` *accepts* `inf`,
  `nan`, `0x10` (=16) and returns them without throwing;
- `hyprlang-config.cpp:513` `VALUEIT->second.m_bSetByUser = true;` runs only after a successful parse
  (every failure path returns earlier), so those values ARE set-by-user;
- `Hyprland-InputManager.cpp:1380` then clamps: inf → 100.00, 16 → 16.00, nan → nan printed (bare `nan`,
  which is not even JSON).

So for `scroll_factor = inf` the compositor's answer is defined (100.00) while the contract's answer is
NOT_COMPARED (exit 5). This is conservative — it never produces a false AGREE — and it is disclosed in the
docstring, but it is a reference-only assumption: the fixtures and clause g freeze it (the generator's
FACTORS list at `quality/counters/c1-r46-devices.py:153-154` literally includes `"nan", "inf", "0x10",
"1e39", "1e-40"`), so any tool implementing the real stof behavior is judged wrong against the reference.
The C2 entry never mentions these forms, so C1 and C2 do not *contradict* each other — but "std::stof is
the parser" is pinned while "these forms are uncomparable" is reference-only, and that split is the shared
soft spot: neither counter clause can see it (g's oracle is the reference itself).
  Independent confirmation — the stof-differential probe has already been run **on the host library** by
  RevengerHyprlang (`.ufo/waves/round-46/w1/RevengerHyprlang/out/floats.txt`; report §3.9; one fresh hyprlang
  CConfig per literal linked to `/usr/lib/libhyprlang.so.0.6.8`): `inf,-inf,infinity,NAN,nan` and `0x10,
  0X1p4` are ACCEPTED with `m_bSetByUser` set; `empty,1e40,1e-45,true` throw `"failed parsing a float: stof"`
  and fall to the default -1. So the throw boundary is stof's own (1e-45 is on the throw side on this host —
  my F2 approximation is settled empirically), and F1's direction is confirmed: inf/nan/hex are accepted by
  hyprlang, not unsupported.
  **Dump-format corner (RevengerHyprlang):** downstream, `std::clamp` passes NaN through (both comparisons false)
  and `std::format("{:.2f}", nan)` prints bare `nan` — real hyprctl output with a `scroll_factor = nan` config is
  **not valid JSON**, so the reference's `parse_devices` (`json.loads`) exits `SETUP bad_json` (2) on a real nan
  dump; the contract's "specials → NOT_COMPARED (5)" bucket is only reachable with synthetic dumps (Python
  `json.dumps` emits parseable `NaN`). A v2 should fixture both spellings. ExecIndepB's oracle probes agree
  (invalid-after-valid stays counted, `-0` prints `-0.00`, `0.335`→`0.34`; 3400-case fuzz, 0 mismatches).

**F2: the `FLT_MIN` threshold approximates libstdc++ behavior the pins do not cover.** Whether
`std::stof("1e-40")` throws (glibc sets ERANGE for subnormals; libstdc++ `stof` throws on ERANGE) or
returns a denormal, and whether `std::stof("1e39")` throws vs returns inf, is a libstdc++/glibc detail.
Neither is pinned. The reference's `2**-126` cut is an unverifiable-from-pins approximation of the same
branch hyprlang models at `hyprlang-config.cpp:467-471` (the `catch` returns before `:513`).

**F3: "only writer" completeness claims rest on single pinned files.** `m_scrollFactor` is written only at
`Hyprland-InputManager.cpp:1380/1382` and `m_currentRules` only at `Hyprland-IKeyboard.cpp:66,109-113`
*within the pinned files*; no other translation unit is pinned. C2's step-5 sentence "and neither does
`input:touchpad:scroll_factor`" (`l1-draft/entry.md:34`) carries **no locator of its own** — it rides
entirely on this absence-of-other-writers argument plus the separate-global citation. It is the
weakest-cited sentence in the entry (the host live run cannot cover it: the 4 pointers in
`receipts/live-devices-host-l1.txt` are all mouse interfaces, no touchpad).

**F4: pure output contract** (line formats, verdict order NOT_COMPARED→DIFFER→NO_KEYBOARDS→STALE_BLOCK→OK,
exit map 5/1/3/4/0, 1 MiB cap, JSON shape, `belongsTo` matching for MATCHED) — self-defined, no pin needed
by design; both claims treat it identically. Not a risk, listed for completeness.

**F5 — partially corrected mid-scan: the directive regex is NOT word-boundary only.** `parseComment`
(`hyprlang-config.cpp:568-616`) trims then `starts_with("hyprlang")`, and the args loop treats any token at
`args[1]` as `noerror/endif/if` — so the glued form `#hyprlangx if X` is an **active directive** in hyprlang:
variable `X` unresolved → `newIfData.failed = true` (`:611-615`) → all following lines are skipped until `endif`
(`:682-684`). The reference's `#[ \t]*hyprlang\b` does not match the glued form, so the tool models it as a plain
comment and can emit DIFFER where the real state is NOT_COMPARED (CritToolSemantics end-to-end: `fallback=1
stale=1 unsupported=0 verdict=DIFFER`). My scan pass cleared the one-token shape (`#hyprlangfoo` — truly inert);
the two-token shape is a real, unmodelled divergence. Generators/fixtures emit only the spaced standard form
(`c1-r46-devices.py:211`), so this is reference-only — invisible to f and g.
  V22 precision (CritToolSemantics harness, `receipts/h2.out,h3.out`): do not build the control with `if true` —
  the argument is resolved as a config/env variable name, so even `#hyprlang if true` skips the following line;
  use an unset condition (`#hyprlangX if X`). The argument loop splits on whitespace including tabs, so
  `#\thyprlang\tif\tfalse` also skips. The bare one-token shape `#hyprlangx` (no keyword) applies the next line —
  confirming only the two-token form diverges.

## 3. Round-45 w1 failure classes — would they recur here?

Source of classes: `.ufo/waves/round-45/registration-v2.md:13-16` (C1) and `:44` (C2).

| r45 w1 class | r46 state | Recurs? |
|---|---|---|
| 8 cheats each narrowing one semantic to the fixtures (11/11 met v1) | f: 90 fixtures pinned sha256 × 3 runs; g: 150 nonce-drawn cases judged by the sha256-pinned reference (`c1-r46-devices.py` clauses f, g) | Low for pure cheats. **Hybrid replay+model is declared-accepted in both rounds** ("a tool holding a model of the contract is an implementation of it", registration.md C1 residuals) — a tool embedding the 90 fixture answers and computing the rest passes every clause; only the non-author reading + live run bound it. Same deliberate boundary as r45 v2, carried verbatim. |
| environment gate cheat | i: bubblewrap, two environments A/B | **Recurs as declared residual, verbatim**: "a tool may detect a sandbox by means not varied in environment B" appears unchanged in registration.md C1 residuals. **Confirmed live mid-scan by SentTool F1/F2 — see §3a.** |
| seed-45 answer table | fixtures are frozen bytes, but g draws from the nonce | Dead for pure tables; see hybrid note above. |
| scorer oracle reading `/proc/<ppid>/cmdline`; parent-process reader (5 do-nothings met v1) | r: PATH markers for hyprctl/libinput/journalctl/udevadm; g judges in-process against the pinned reference; i hides the counter's lane | Low in the tool direction — the r45 v2 harness (0 of 45 met) is re-cut unchanged for r46 (`c1-r46-devices.py` head: "the round-45 v2 harness … re-cut for this tool"). **But the marker clause itself is bypassable — SentTool F2 scored TARGET_MET with an exec'ing tool; see §3a.** |
| **contract wrong against Hyprland** (r45 v1: 6+ forms — transform `07`, stoi addreserved, 0x0 sentinel, modeline, CR lines, desc: long-only, NaN/Infinity accepted) | **Live class.** r46's own freeze caught one instance: a pre-freeze control run met V03 case-insensitive names, fixture `case-exact-dump-name` added (`registration.md:34-35`; `receipts/ctl-c1.txt:5`). F1/F2 above are current instances in the *safe* direction (false NOT_COMPARED, never false AGREE — the mirror of r45's unsafe NaN acceptance). The V01-V20 controls protect the contract as written, not against the contract itself; fixtures+g are generated from the reference, so they cannot see reference-vs-Hyprland drift. **This is exactly the class w1 attack seats exist to hunt.** | **Yes — the vector survives registration.** |
| 9 C2 forgeries (fence table, receipt-refuting sentence, free README ids, spaced census, supersession row) | T1-T5 carried into `c2-r46-input-device-entry.py`; 14 controls incl. R45-COPY all rejected (`receipts/ctl-c2.txt` PASS, wrong=0 of 15) | Low. |
| 4 entry facts with no pin (r45) | Every factual sentence in the r46 entry re-verified against a pin locator (table in §1; entry steps 1-7 + OBS S316-S325 all locate). Residue: F3's single-file completeness and step 5's uncited touchpad clause. | Low, softened to F3. |
| D1 wave shape (w1-only, planned w2 never ran) | This round runs the r45 w2 falsification as routed work, but is itself **one v2 wave w1** — no post-data falsification wave is scheduled for the r46 claims inside this round. | Structurally recurs at round level; not a claim defect. |

## 3a. Update — harness/verification-surface findings from across the wave (verified)

Safety-review seat `SentTool` published `.ufo/waves/round-46/w1/SentTool/findings.md` (F1-F7) mid-scan; eight
further seats sent carry-overs over IRC. Every load-bearing claim below was re-verified against frozen bytes by
this seat before integration. The unifying pattern across all of them: **both counters trust artifacts that sit
inside the scored commit's (or the sandbox's) own reach** — C1 trusts that the pinned reference/fixtures are
secret, C2 trusts receipts authored by the scored revision — so the two claims share one verification-surface
assumption: *the evidence a counter reads is unreachable or unforgeable by the scored tree.* It is neither.

**C1 side (all scored TARGET_MET against the frozen counter; this seat verified the code lines and receipt tails):**

- **SentTool F2 — clause r is a PATH marker.** Selftest runs `env={"PATH": "/usr/bin:/bin", …}` with no fake bin
  (`c1-r46-devices.py:375`, verified); `sandbox()` is `--ro-bind / /` plus tmpfs over only {repo, lane, lane-parent}
  (`:241-257`, verified). Two bypasses scored MET at nonce 46 — absolute-path `/usr/bin/hyprctl`, and bare-name
  under `--selftest`. Receipt tail verified: `clause=r marker=absent` then
  `readonly=ok … verdict=TARGET_MET rev=3d96dcd… exit=0`
  (`.ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-absolute-path.txt`).
- **SentTool F1 — the sandbox-detection residual, made concrete.** `hidden_paths()` hides three paths; `$HOME`,
  `/run/user/<uid>`, sibling scratch stay visible, and a unix socket on a read-only bind is still connectable
  (`evidence/socket-ro-bind.txt`) — a scored tool can reach the live `.hyprland.sock`. This is the operational
  content of the declared residual "a tool may detect a sandbox by means not varied in environment B", plus a
  host-safety surface outside both counters' vision.
- **CritC1Cheat routes** (receipts verified by this seat and corrected by their author: `score-A-ambient.txt`
  is cheat A, ambient-oracle delegation for clause i — 67 pinned-sha artifacts reachable under
  `/fast/scratch/hyaku/mado-r46` (`receipts/oracle-inventory.txt`); its tail `clause=r marker=absent …
  TARGET_MET rev=65b6d4a0 seeds=46,4601` holds only because nothing tripped the marker): (1) *ambient oracle* —
  the pinned reference and fixture corpus stay reachable inside the sandbox, so a scanner execs the reference for
  clause g and scores MET; (2) *marker unlink* — the marker file lives in the tool's own writable bind, so the
  four binaries can run and then unlink it (`clause=r marker=absent … rev=170fa429` in `score-B2.txt`; no-unlink
  control `readonly=fail marker=present … rev=ccfa1f60` in `score-Ctl2.txt`; side-log proofs
  `tripwire-proof-{B,Ctl}.txt`); (3) *no parity clause* — a tool keyed on `/proc/1/cmdline=bwrap` reaches MET
  and prints SETUP usage on the host (`score-C-ambient.txt` rev `e7a64bf3`; `host-parity-C.txt` rc=2 on the
  host).
  Plus: clause f is exactly table-satisfiable from the **public** pinned 90-fixture corpus
  (`score-D-ambient.txt`: f=90/90, g=0/150, with a forged selftest line — registration itself declares "clause s
  is a printed line"). So f+g together do not force an independent implementation unless the sandbox actually
  hides the oracle.
- **LabDupNames semantic gap** (verified from the pinned fixtures bytes): no fixture pairs a block name with a
  dump device name that extends it (0 prefix co-occurrences in `c1-r46-fixtures.json`), so a tool that resolves a
  device to its longest block-name prefix passes 90/90 on clause f and is caught only by clause g. The reference
  itself separates the shape (exact dict lookup in `expected_names`), so one fixture (`block foo` vs dump
  `foo-1`) would close it.

**C2 side (mechanism verified in the frozen counter by this seat):**

- **RevW2Counters' forged-receipt route carries verbatim into c2-r46.** Clause d's docstring says a new id's
  receipt "must be one of PINS", but the code at `c2-r46-input-device-entry.py:532-534` computes
  `pin_ok = PINS.get(os.path.basename(path)) in (None, digest) and …` — a receipt whose basename is **not** in
  PINS makes `PINS.get` return `None`, and `None in (None, digest)` is True, so a receipt the scored commit
  itself authors under `FETCH/<non-pin-name>` passes. And clause T4 (`:673-680`) binds verdict tokens to
  `.ufo/waves/round-N/receipts/<file>` bytes read from the **scored rev** (`show(repo, rev, locs[0])`), so a
  commit can self-certify its own verdict tokens. Their r45 demonstration: forged S316 admitted at rev
  `1de0bb53`; probe-carrying tool on c1-r45 at `64e41df4` (`.ufo/waves/round-46/w1/RevW2Counters.md`).
- **SentW2Privacy's two v2 hygiene classes** (received, evidence at `.ufo/waves/round-46/w1/SentW2Privacy.md`):
  bake live device strings into fixtures (round-45's vendor/model regression landed in 6 committed files — use a
  sentinel synthetic vendor), and receipt command lines leak account paths (651 occurrences in 151 of 741 r45
  files; an R4-shaped whole-line rule scores 0).
- **SentW2Privacy S1 (high-severity, outside the masterPattern):** the *published corpus itself* carries the
  host's real monitor serial, outside the gate's `.ufo` scope — `corpus/knowledge/config-health-report-r3.md:149`,
  `hyprctl-verification-layer.md:153`, `hyprland-config-plane.md:184` (and `:183` model). Verified by
  SentW2Privacy against one live `hyprctl monitors all -j`; locators pass in
  `SentW2Privacy/receipt-quotes.txt`. Not introduced by round-45 (its six hits are vendor/model only). S2/S1 are
  only checkable against a live dump, so **no v2 counter can certify its own fixtures** — the check belongs in a
  seat or the gate, not in clause g.
- **MutC2Counter killing-control confirmation** (`.ufo/waves/round-46/w1/MutC2Counter.md` M3 corrected; evidence
  `probe-sharedquote-{pristine,m3}.txt`): the `pin_ok` None-membership route is not just theoretical — a
  SHARED-QUOTE control (P + new id S326 gated on a self-authored non-PINS receipt sharing S319's gate quote,
  self-consistent sha, ≥256 B, 100644) is REJECTED by the pristine counter solely on the quote-uniqueness
  sub-check (`clause=d id=S326 gates=1 bound=0`), and ADMITTED by the M3 mutant that drops that sub-check
  (a:1..j:1, same rev `b7901912`). So quote-uniqueness is the only barrier between the route and admission;
  the non-PINS receipt passed every pin-rooted binding check in both runs.
- **RevengerHyprlang's modelling point** (received; consistent with my §2): the whole parse plane is modelable
  offline against `/usr/lib/libhyprlang.so.0.6.8` (their probe does exactly that), so if a v2 leaves any live
  dump/socket/config reachable, clause r intact cannot distinguish "read the live plane" from "read a stashed
  dump".

**Where the in-flight v2 stands (untracked `quality/counters/c1-r46-devices-v2.py`, `c1-r46-fixtures-v2.json`,
`c2-r46-input-device-entry-v2.py`; lines verified):** the v2 C1 counter closes the selftest-PATH shape (fake bin
first in the selftest env at `:403`), replaces the file marker with a pipe tripwire (`:154-159`), and switches to
an allowlist root of `/usr` + `/etc` read-only (`:30-31, :279-287`) — which closes F1's socket/home reach by
construction (nothing else is bound). But its own docstring admits at `:52` that "an absolute /usr/bin path runs
the real binary", and ScrMistakes' source read confirms the stub is PATH-only — so **the absolute-path escape
survives the v2** unless the stub is bound over `/usr/bin/<name>` or execve is logged. The C2 v2's treatment of
the `pin_ok None`-membership hole was not verified by this seat.

**Second-order effects on the frozen artifacts (SentTool F3-F7):** the v1 counter's `load_model()` writes
`__pycache__/*.pyc` into the frozen lane (`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc`
exists), so the pin-trust chain both claims rest on is only as good as the sha256 gate; plus the unbounded
writable marker dir, `--work` acceptance outside the seat-scratch rule, unquoted marker interpolation at
`:146` (verified), and the reference's O(n²) `cut_comment` (8.9 s on a 1 MiB `##` line).

**Cross-claim tie-in and recurrence read.** This is §3's r45 classes showing up live: the environment-gate
class (F2 + marker-unlink + bwrap-key), the scorer-oracle class (ambient pinned reference under `/fast/scratch`),
the answer-table class (clause f publicly table-satisfiable), and the declared residuals (sandbox detection,
"clause s is a printed line") all confirmed at the frozen counter in the same wave that froze it. C2 is
mechanically untouched by the C1 harness holes, but shares the master pattern via the forged-receipt/`pin_ok`
route and T4 self-certification. Registration.md's C1 kill rule permits a pre-data v2 re-freeze; the window is
open while the v2 set is untracked, and the absolute-path escape plus the C2 `pin_ok` hole are the two items a
v2 freeze must close to make clauses r/i (C1) and d/i (C2) mean what their docstrings say.
**Post-integration updates.** `SentHost` H9/H10 (verification: the v2 C1 counter at
`quality/counters/c1-r46-devices-v2.py:278-286` builds the allowlist root, `:154-160` pipe tripwire, `:403`
selftest fake bin): the v2 closes F1 by construction (no `/run`, no `$HOME` bound), so an absolute-path
`/usr/bin/hyprctl` exec remains possible but inert — it cannot reach a compositor because
`XDG_RUNTIME_DIR=/run/user/<uid>` does not exist inside the allowlist root; the clause wording "no hyprctl run"
is stronger than what it certifies. H10 is about the v2 itself: as of 18:05 the v2 counter/fixtures and
`.ufo/waves/round-46/v2/` are untracked, the v2 docstring asserts `.ufo/waves/round-46/registration-v2.md`, and
that file does not exist — **v1 remains the only citable line until a v2 freeze exists** (shell result: no such
file). `CritToolSemantics` adds four *model* findings that carry into any v2: DIRECTIVE_RE misses the glued
`#hyprlangx if X` directive (real: skips lines — see corrected F5); `source =` **inside** a device block should
be unsupported (the sourced file inherits the block and clears the stack at EOF — `ConfigManager.cpp:1839`,
hyprlang `parseFile` :1052); `kb_file` suppresses the us+empties reset and makes AGREE silent about the keymap;
the virtual-keyboard rationale is creation-time apply, not (only) override; "printed us+empty" has three
producers. They add V21-V24 controls for these and their constraint (a) matches my §4: regenerate the reference
*with* the fixes before a v2 freeze, otherwise clause g keeps certifying the broken model.

## 4. One bounded move (synthesis)

The **stof-differential probe has already been run**, by RevengerHyprlang on the host library itself
(`RevengerHyprlang/out/floats.txt`, report §3.9), and its results are folded into F1 above (inf/nan/hex
accepted by hyprlang; overflow/underflow throw; bare `nan` in the real dump is invalid JSON). What remains is
the **binding** step: ScrEntryDraft has already drafted the C2 Limits sentence (records that
`scroll_factor` is handed to `std::stof` at `hyprlang-config.cpp:465-471` with clamp at `InputManager.cpp:
1379-1382`, while the join counts inf/nan/hex/infinite/denormal as unsupported at `mado-devices.py:62-66` ⇒
NOT_COMPARED, never a false AGREE) and the round-46 lesson should carry the divergence table from the probe's
receipt. A v2 should fixture both nan spellings (Python `NaN` synthetic vs bare `nan` real) and the A12
overflow-crash shape.

- Axis effect: **calibration** — the declared residual "whether the contract matches Hyprland beyond the
  pins" (registration.md C1 residuals) is now a measured quantity with a host-linked receipt, the exact role r45's
  ExecScaleOracle played for scales; **coverage** — the entry gains the pinned Limits fact (drafted, 42 locators
  verified, counter still admitted=1/1 at scratch rev fbc38d36).
- No harm: C1 contract bytes, fixtures and verdicts unchanged (NOT_COMPARED preserved — the probe documents
  reality, it does not widen the compared domain mid-round); C2 clauses a-j all still pass; both counters read
  only committed paths, the probe lives in seat scratch.
- Risk: the measured reality *differs* from the contract on inf (→100.00) and on the nan-dump format (real
  dump exits 2, not 5); that is a lesson/entry fact for the next round's registration, not a violation of this
  one — the kill rule protects the contract as frozen.
- If a v2 freeze proceeds (the v2 set is untracked and no registration-v2.md exists yet), this seat's
  finding set is additive and has a fixed ordering: the harness items first (v2 already closes F1 and the
  selftest-PATH shape; the absolute-path exec stays possible but inert, and the C2 `pin_ok` hole + T4
  self-certification are still open), then the model items with the reference regenerated *with* them
  before re-freezing (CritToolSemantics' constraint a — otherwise clause g certifies the broken model):
  F1 special-float semantics, F5 glued-directive form, `source =` inside a block, and the V21-V24 control
  shapes (including the LabDupNames foo/foo-1 fixture). v1 remains the only citable line until that freeze.

## Evidence index (all opened this session)

- `.ufo/waves/round-46/registration.md` (frozen claims; pre-freeze V03 note at `:34-35`)
- `.ufo/waves/round-46/l1-draft/mado-devices.py` (contract docstring `:1-89`; read_float `:230-242`; parse_config `:240-302`; report/verdicts `:395-440`; selftest `:446-`)
- `.ufo/waves/round-46/l1-draft/entry.md` (steps 1-7, OBS S316-S325, census, Limits)
- `quality/counters/c1-r46-devices.py` (docstring clauses a-s-f-i-r-g; FACTORS at `:153-154`; MODEL_SHA256 `:68`)
- `quality/counters/c2-r46-input-device-entry.py` (clauses a-j, T1-T5, 28 surfaces, census patterns)
- `quality/counters/c1-r46-fixtures.json` (90 fixtures, one per semantic dimension incl. `case-exact-dump-name`, `fallback-not-when-declared-us`)
- `receipts/ctl-c1.txt` (PASS, 0 of 23, reference MET, V01-V20 lines), `receipts/ctl-c2.txt` (PASS, 0 of 15)
- `receipts/live-devices-host-l1.txt` (9 AGREE, 1 VIRTUAL, 4 pointers at -1.00, OK; no touchpad present)
- Pins, quotes verified at: `fetch/Hyprland-InputManager.cpp:1226-1231,1270-1280,1282-1295,1376-1383,2124`;
  `fetch/Hyprland-ConfigManager.cpp:518-565,1115-1123,1125-1168,1196-1201`; `fetch/Hyprland-ConfigValues.cpp:271-300`;
  `fetch/Hyprland-IKeyboard.cpp:60-116`; `fetch/Hyprland-HyprCtl.cpp:765-802` (:769, :773);
  `fetch/Hyprland-MiscFunctions.cpp:777-789` (:782); `fetch/Hyprland-VirtualKeyboard.cpp:36-44` (:41);
  `fetch/Hyprland-protocols-VirtualKeyboard.cpp:11-30` (:12); `fetch/hyprlang-config.cpp:32,44-66,291-320,420-440,467-471,513,568-570,674-706,885-899,1083-1124`; `fetch/wiki-Keywords.md:64-79` (:67)
- Round-45 classes: `.ufo/waves/round-45/registration-v2.md:13-16,44`; `corpus/lessons/round-45-verifier-spotcheck.md` §6 (D1-D6); `tools/mado-monitors.py:1-83`; `corpus/knowledge/hyprland-monitor-rule-r45.md:1-43`
- Mid-scan integration (verified, not re-run): `.ufo/waves/round-46/w1/SentTool/findings.md` F1-F7; `evidence/clause-r-bypass-absolute-path.txt` (tail: `clause=r marker=absent … TARGET_MET rev=3d96dcd`); counter lines re-verified at `quality/counters/c1-r46-devices.py:146,243,249-257,375`; `CritC1Cheat/receipts/score-A-ambient.txt` tail (`TARGET_MET rev=65b6d4a0 seeds=46,4601`); fixture-bytes check for block-prefix pairs (0 co-occurrences); `c2-r46-input-device-entry.py:532-534,673-680` (pin_ok None-membership; T4 self-certification); `MutC2Counter/evidence/probe-sharedquote-{pristine,m3}.txt` (killing control, rev `b7901912`); v2 set line-reads: `c1-r46-devices-v2.py:30-31,52,154-160,278-287,403`; RevengerHyprlang host-library probe `out/floats.txt` (28/28 quotes; FLOAT/INT literal table); further carry-overs cited as received: `ScrMistakes/receipts/c1-v2-carryover.txt`, `SentHost/checks.txt:181-223` (H9/H10), `ScrSkill/skill.md` F8, `CritToolSemantics.md` F1-F5+V21-V24, `LabDupNames/evidence/variant-prefix.txt`, `ScrEntryDraft` (Limits draft; 42 locators; rev fbc38d36), `SentW2Privacy.md` (S1-S3); `registration-v2.md` absent at `.ufo/waves/round-46/` (shell result)
