# R56ScoutHyprlang — hyprlang v0.6.8 source verification (round 56, wave w1)

Seat: read-only research. Scope: fetch hyprlang v0.6.8 `src/config.cpp`, verify the registration §C2 model's
hyprlang-language rules against SOURCE (not against registration.md), answer (a)–(d), classify every model rule.

## Provenance

- Fetched `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp` (1158 lines,
  sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`).
- The round-46 pin `.ufo/waves/round-46/fetch/hyprlang-config.cpp` has the SAME sha256; `diff -u` exit 0.
  **The pin is byte-identical to tag v0.6.8** and is valid evidence for this round. All `config.cpp:N` below cite both.
- Hyprland side read from the frozen wave pins `fetch/Hyprland-legacy-ConfigManager.cpp` and `fetch/Hyprland-ConfigValues.cpp` (pinned commit per claims-frozen: `efb50993…`, Hyprland v0.56.2).
- No tooling installed or upgraded (curl/tar/grep only). No pacman transaction. No hyprctl call at all. No host writes. Scratch was `/fast/scratch/hyaku/mado-r56/R56ScoutHyprlang/`, removed before yield; receipts copied to the deliverable dir (see receipts.txt).

## (a) Is `source` handled by a Hyprland-registered handler, by hyprlang itself, or both?

**Answer: by the Hyprland-registered handler ONLY. Not by hyprlang itself; not "both".**

Evidence:

- `grep -rn -i 'source' hyprlang-0.6.8/src hyprlang-0.6.8/include` over the full v0.6.8 tree (7 source files) returns
  exactly one hit, a doc comment: `hyprlang.hpp:366: recommended to use for stuff like source = path.conf` — the
  documentation OF `registerHandler`. Zero code occurrences of `source` in hyprlang.
- Hyprland registers it: `Hyprland-legacy-ConfigManager.cpp:614: m_config->registerHandler(&::handleSource, "source", {false});`
  (wrapper `:359-363`; body `:1810-1850` — matches the registration's cited range exactly).

**Handler call order for a `source = path` line** (hyprlang `CConfig::parseLine`, config.cpp:669-912):

1. `line = trim(line)` (672); if first char is `#` the whole line is a comment/directive — `parseComment` handles
   `# hyprlang …` directives (676-682, 570), others are silently skipped.
2. If the innermost `# hyprlang if` block is failed, the line is skipped entirely (683-685).
3. Comment stripping on the rest: a lone `#` cuts the line there; `##` collapses to one literal `#` and scanning
   continues after it (687-705); re-trim (706); empty → done.
4. FIRST `=` split; LHS/RHS trimmed (711, 722-723).
5. `$var` expansion loop over known variables (LHS not expanded if LHS itself is a variable) and `{{expr}}`
   evaluation in RHS, up to 100 rounds (737-820).
6. `$`-LHS → `parseVariable`, never a handler (730, 806).
7. RHS backslash unescaping of `{`/`}` (821-829).
8. `configSetValueSafe(LHS, RHS)` runs FIRST (832). It builds `valueName` = category stack joined `:` + `:` + LHS
   (282-285). `source` is not a registered value; at depth 0 `valueName` has no `:` → early return `{false, result}`
   with no error (356). Inside a category (`cat:source`) it errors "config option <cat:source> does not exist."
   (447) and still returns `found=false`.
9. Only if `!found`: handler loop (839) in registration order; an unscoped handler (name without `:`, 844) matches
   when its name equals LHS exactly, regardless of category scope (866); `ret = h.func(LHS, RHS)` (872). No `break`
   — every matching handler runs, last result wins.
10. Hyprland's `handleSource` then: `rawpath.length() < 2` → "bogus" (pin :1810-1813); `glob(absolutePath(rawpath,
    m_configCurrentPath), GLOB_TILDE)`; nonzero rc → error ("found no match" on GLOB_NOMATCH) (:1821-1827); per match
    in `gl_pathv` order: `absolutePath` again, `std::filesystem::status` failure → "inaccessible" and RETURN, i.e. the
    rest of the matches are skipped (:1830-1838); regular file → `m_configPaths.emplace_back(value)` BEFORE
    `m_config->parseFile(value)` recursion (same `m_config` object → shared category stack), `m_configCurrentPath`
    saved/restored (:1840-1842); directory → skip WARN; non-regular → skip WARN (:1843-1849).

This order matches the §C2 model's source chain (append BEFORE parse, rest-skip on inaccessible, bogus/nomatch/
inaccessible/directory/nonregular) — pin-verified at :1810-1850.

## (b) Comments and `configStringToInt`

- **Where `#` starts a comment:** after trim, a `#` at position 0 makes the whole line a comment (676). Elsewhere,
  the first UNESCAPED `#` cuts the line (697-698). `#` has no string-quoting concept in hyprlang; it is cut before
  the `=` split, so an RHS can never contain a bare `#`.
- **What `##` does:** mid-line, `##` is an escape for one literal `#`: `line = line.substr(0, commentPos + 1) +
  line.substr(commentPos + 2)` (701) — the second `#` is deleted, the first is kept, scanning resumes after
  (`commentPos = line.find('#', lastHashPos)`, 702). At line START (post-trim) `##` is just a comment line (the
  `commentPos == 0` early return at 676 fires before the escape loop). Note `###` mid-line: first pair collapses,
  the surviving `#` is then re-scanned; `####` nets out to two literal `#` (traced byte by byte; intricate but
  deterministic).
- **`configStringToInt` prefix rules (config.cpp:185-268):** order is `0x` → hex stoll base 16 (195); `rgba(…)`/`rgb(…)`
  color forms (198-257); then `starts_with("true")||starts_with("on")||starts_with("yes")` → 1 (259); then
  `starts_with("false")||starts_with("off")||starts_with("no")` → 0 (261); then empty-or-`!isNumber(VALUE,false)` →
  error (265); else `std::stoll` decimal (267-273). Prefix (`starts_with`) semantics are real: `onyx` → 1,
  `notebook` → 0. `isNumber(str,false)` (hyprutils v0.7.1 String.cpp:25-45) = every char `isdigit`, `-` tolerated
  only at index 0, no float dot — i.e. `-?[0-9]+`. **The model's true/on/yes / false/off/no / `[0-9]+` rules agree
  with source for every input the model accepts** (the `0x`/rgba/rgb branches precede the booleans but no model-
  accepted string starts with those). Edge divergences listed below (D5-D7).

## (c) Category nesting and `misc:disable_autoreload` addressing

- `}` branch: requires the line to be EXACTLY `}` (`line != "}"` → "Invalid config line" error, 884); pops
  `impl->categories` (893); stray `}` → "Stray category close" (889). Category-open branch: requires
  `line.ends_with("{")` (901, else "Invalid category open, garbage after {" 902); pushes the trimmed text before
  `{` (907-908).
- Key addressing: `configSetValueSafe` builds `valueName` by `for (auto& c : impl->categories) valueName += c + ':';`
  then `valueName += command;` (282-285). So nested `a { b { key = v } }` → `a:b:key`, and `misc { disable_autoreload
  = 1 }` → `misc:disable_autoreload` — the same name as the flat form `misc:disable_autoreload = 1`, which Hyprland
  registers (`ConfigValues.cpp:492 MS<Bool>("misc:disable_autoreload", … false, {.refresh = REFRESH_CONFIG_WATCHER})`;
  stored as hyprlang INT, so the INT branch at config.cpp:455 runs `configStringToInt` — exactly the model's VALUE chain).
- Stack lifetime: `clearState()` clears the stack once at `parse()` start (1070-1071); each `parseFile` clears leftovers
  at ITS EOF with a "Unclosed category at EOF" error (1048, 1052). During sourcing the stack is SHARED (same `m_config`
  recursed at pin :1842) — equivalent to the model's per-file reset for the depth-0 sourcing the model accepts.

## (d) Is a line with `=` inside a category keyed `category:key`?

**Yes.** config.cpp:282-285 — the colon-joined category stack prefixes every LHS before value lookup
(`valueName += c + ':'; … valueName += command;`). A registered value is found under `category:key`; an unregistered
dotted name errors "config option <cat:key> does not exist." (447).

## Rule-by-rule table vs registration §C2 model

Quote ≤25 words each. `config.cpp` = v0.6.8 `src/config.cpp` (= round-46 pin, sha256 fa1b6898…).

| # | §C2 model rule | Verdict | Source evidence |
|---|---|---|---|
| 1 | Empty line / first char `#` skipped | AGREES | config.cpp:676 `if (commentPos == 0) {` (after `line = trim(line);` :672) |
| 2 | Strip space, tab, CR, LF, VT, FF | AGREES | hyprutils String.cpp:11 `std::isspace(in.at(countBefore))` (C-locale set = those 6) |
| 3 | `=`-split at FIRST `=`, LHS/RHS stripped | AGREES | config.cpp:711 `auto equalsPos = line.find('=');` |
| 4 | RHS cut at its first `#`, stripped | AGREES | config.cpp:697-698 `if (!escaped) { line = line.substr(0, commentPos);` |
| 5 | `##` in RHS → `unsupported` | AGREES (conservative; real = literal `#`) | config.cpp:701 `line.substr(0, commentPos + 1) + line.substr(commentPos + 2)` |
| 6 | LHS starting `$` ignored | AGREES | config.cpp:730,806 `ISVARIABLE = *LHS.begin() == '$'` → `parseVariable` (no value, no handler) |
| 7 | KEY = stack joined `:` + `:` + LHS | AGREES | config.cpp:282-285 `valueName += c + ':';` … `valueName += command;` |
| 8 | true/on/yes prefixes → 1, checked first | AGREES | config.cpp:259 `VALUE.starts_with("true") \|\| VALUE.starts_with("on") \|\| VALUE.starts_with("yes")` |
| 9 | false/off/no prefixes → 0 | AGREES | config.cpp:261 `VALUE.starts_with("false") \|\| VALUE.starts_with("off") \|\| VALUE.starts_with("no")` |
| 10 | `[0-9]+` entirely → decimal integer | AGREES | config.cpp:265 `isNumber(VALUE, false)`; hyprutils String.cpp:34-39 isdigit-only (`-` only at 0) |
| 11 | Anything else → `unsupported`, never guessed | DIVERGES at edges (see D5-D7) | config.cpp:195 `if (VALUE.starts_with("0x"))` real parses hex; :267 stoll throws on int64 overflow |
| 12 | Only KEY `misc:disable_autoreload` matters | AGREES | ConfigValues.cpp:492 `MS<Bool>("misc:disable_autoreload",` (registered, INT branch runs configStringToInt :455) |
| 13 | Exactly `}` pops | AGREES | config.cpp:884 `if (line != "}")` error; :893 `impl->categories.pop_back();` |
| 14 | Line ending `{` pushes stripped text | AGREES | config.cpp:901,907-908 `if (!line.ends_with("{"))` … `impl->categories.push_back(line);` |
| 15 | Any other `=`-less line ignored | DIVERGES (state-identical; real records parse errors) | config.cpp:715/:884 "Invalid config line"; :902 "Invalid category open, garbage after {"; :889 "Stray category close" |
| 16 | Category stack resets at each file's start | AGREES for accepted subset | config.cpp:1071 clearState; :1052 EOF clear per parseFile; shared stack during recursion |
| 17 | `source` handled by Hyprland's handleSource (legacy) | AGREES | legacy-ConfigManager.cpp:614 `registerHandler(&::handleSource, "source", {false});` |
| 18 | `source` with non-empty stack → `unsupported` | DIVERGES (conservative; real handler IS called) | config.cpp:844,866 unscoped handler matches LHS name regardless of scope |
| 19 | len<2 → bogus; absolutePath; glob; nomatch; inaccessible skips REST; append BEFORE parse; dir/nonregular SKIP | AGREES | pin :1810-1813 bogus; :1821-1827 glob; :1834-1838 return on status error; :1840-1842 emplace before parseFile; :1843-1849 skip |
| 20 | Depth cap 16 (declared divergence) | AGREES-as-declared | pin :1840-1842 recursion has no cap in Hyprland |
| 21 | `# hyprlang if` conditional blocks | **DIVERGES (not declared)** | config.cpp:683 `currentFlags.ifDatas.back().failed` skips the whole line; model parses it (D1) |

## Divergences found (byte-level)

- **D1 — `# hyprlang if` blocks (sharp; NOT in the declared divergence list).** config.cpp:683-685 skips every line
  while the innermost `if` block failed; `parseComment` (570) recognises `# hyprlang if|endif|noerror`. The model
  treats directive lines as plain comments and PARSES the body.
  Example: `# hyprlang if NO_SUCH_VAR` / `source = ./extra.conf` / `# hyprlang endif` → real Hyprland: unset var →
  block failed → NO watch on extra.conf; model: watch ADDED. Model over-predicts watches here.
- **D2 — `$var` in a `source` RHS.** Real: variables expand BEFORE the handler call (step 5 above), so
  `$configs/m.conf` (with `$configs = …`) is sourced. Model: no expansion, literal `absolutePath("$configs/m.conf")`
  → glob typically NOMATCH → `ERROR reason=nomatch`. Not guarded as unsupported for source lines.
- **D3 — `{{expr}}` in a `source` RHS.** Real: evaluated (parseExpression); model: literal → nomatch. Same class as D2.
- **D4 — `source` inside a category.** `decoration { source = ./x.conf }` → real: handleSource IS called (unscoped
  handler matches by name, 866) and x.conf is watched with the current file as base; model: `unsupported +1`, no
  watch. Conservative (under-predicts), covered by the subset preamble but real behavior is as stated.
- **D5 — int64 overflow (polarity flip).** `misc:disable_autoreload = 99999999999999999999` → real: `stoll` throws
  (config.cpp:267-273) → parse error, value NOT set, stays default 0 → watches ACTIVE; model: `[0-9]+` → big nonzero
  int → watches EMPTY. The one edge where the model predicts the opposite of reality.
- **D6 — negative values.** `-5` → real: `isNumber` allows `-` at index 0 → -5 → nonzero → off; model:
  `unsupported`. Conservative.
- **D7 — `0x…` / `rgba(…)` / `rgb(…)`.** Real: parsed as int (config.cpp:195-257); model: `unsupported`. Conservative.
- **D8 — `} {` (model-side state divergence).** Model: `=`-less line ending `{` pushes the stripped text before `{`
  → pushes a category named `}` (later `}` pops early, potentially mis-keying subsequent lines). Real:
  `line.contains("}")` && `line != "}"` → "Invalid config line" error, stack unchanged (884). No real-config impact.

## Registration C2 agreement summary

No disagreement found between the wave-item text and registration.md for my scope; registration.md §C2 was used as
the rule list and every rule above was checked against source. 21 rules classified: 16 AGREES, 4 DIVERGES
(#5, #11, #15, #18 — all conservative-subset or state-identical except D5), 1 DIVERGES-not-declared (#21/D1),
0 UNVERIFIED in the table itself.

## Not verified / out of seat

- Host's exact runtime libhyprutils version (hyprlang declares `hyprutils>=0.7.1`, CMakeLists.txt:40; `isNumber`/
  `trim` semantics verified at v0.7.1 only; a newer minor could in principle differ).
- `std::isspace` locale dependence of `trim` (C locale assumed; host locale not read — outside my read allowlist).
- ConfigWatcher masks/ordering, inotify(7) semantics, host `hyprctl getoption` values — other seats; not touched.
- Sealed hold-out H01-H08: not sought, not seen.

## Deliverables

- `.ufo/waves/round-56/w1/R56ScoutHyprlang.md` — this report.
- `.ufo/waves/round-56/w1/R56ScoutHyprlang/receipts.txt` — commands + decisive outputs.
- `.ufo/waves/round-56/w1/R56ScoutHyprlang/hyprlang-v0.6.8-src-config.cpp` — fetched source (sha256 fa1b6898…).
- `.ufo/waves/round-56/w1/R56ScoutHyprlang/hyprlang-v0.6.8-include-hyprlang.hpp` — registerHandler doc (:366).
- `.ufo/waves/round-56/w1/R56ScoutHyprlang/hyprutils-v0.7.1-String.cpp` — isNumber/trim.

Lane untouched (no tracked-file edits, no git/jj mutations). Scratch removed.
