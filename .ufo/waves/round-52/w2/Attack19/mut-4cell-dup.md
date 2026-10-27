# mado tracked-instrument ledger (draft r51)

Draft for the tracked path `quality/tool-ledger.md` (round 51, claim C1, seat
`ExecLedgerPopulation`). One row per instrument in the C1 population at the round base
`6ca8c559a4a3d6d361101592116eea2bc7452437`: every file under `tools/`, every `quality/*.py` and every
`quality/counters/*.py` (79 files; `__pycache__`, `.pyc`, `.txt` and `.json` excluded,
and `.sh` counted only under `tools/`).


- cell 1 is the instrument's exact repository path, backticked, listed exactly once.
- cell 2 is what the instrument does, read from its own header, never inferred from its name.
- cell 3 is the accountability pointer: a tracked repository file that names the instrument.
  The `:<line>` suffix is where the name occurs at the checked revision and is an annotation;
  the checker strips it, requires the path to exist at the revision, and requires at least one
  pointer in the cell to contain the row's basename in its bytes.

Pointer classes: `PROVINCE.md` (ownership and write scope), `SCORECARD.md` (the capability
row that cites the instrument), `corpus/lessons/round-N.md` and
`corpus/lessons/round-N-verifier-spotcheck.md` (the round that landed or ruled on it),
`corpus/QUALITY.md` (a criterion registration), `corpus/knowledge/*.md` (a recheck trigger)
and `.ufo/waves/round-N/registration.md` (the freeze that registered the predicate).
Five superseded v1 counters have no lane-level document naming them; their registration
is the only tracked file that does, and it is recorded rather than papered over.

| instrument | description | accountability pointer |
|---|---|---|
| `tools/mado-action-plan.py` | Fail-closed static classifier of a declared JSON action plan against a JSON safety policy; reads only `kind` labels and the lexical `argv[0]` basename, never executes supplied argv. | `PROVINCE.md:20` |
| `tools/mado-anims.py` | Static resolver of a Hyprland v0.56.2 config tree's animation table; prints the `hyprctl animations -j` JSON (35 animation nodes plus the bezier map) from file bytes only. | `PROVINCE.md:30` |
| `tools/mado-assessment.py` | Read-only assertion gate over an assessment bundle (`--check BUNDLE --root ROOT`) that replays the frozen round-21 fixtures under `--selftest`; exit 0 clean, 1 failed, 2 cannot evaluate. | `PROVINCE.md:20` |
| `tools/mado-binds.py` | Static resolver of a Hyprland config tree's bind table: `source`/`$name`/`{{ expr }}` expansion, the legacy bind grammar, `unbind` and `submap` in processing order; prints the 18 `hyprctl binds -j` fields. | `PROVINCE.md:29` |
| `tools/mado-devices.py` | Joins `input`/`device` config lines with `hyprctl devices -j`: per keyboard the five stored XKB names (AGREE/DIFFER/FALLBACK/VIRTUAL), per pointer the block's `scrollFactor` (AGREE/DIFFER). | `PROVINCE.md:105` |
| `tools/mado-eventq.py` | Read-only census of Hyprland's event-socket subscribers from the kernel socket table (`ss -xpa`): subscriber rows, unread bytes, the two drop markers, and whether `debug:disable_logs` could have suppressed them. | `SCORECARD.md:2370` |
| `tools/mado-evidence-audit.py` | Audits artifact arithmetic and explicit evidence labels in a bundle (`--check BUNDLE --root ROOT`); exit 0 consistent, 1 contradicted, 2 could-not-evaluate, consulting no classifier, host probe or Git. | `PROVINCE.md:20` |
| `tools/mado-geometry.py` | Joins window-rule `size W H` lines with `hyprctl clients -j`; names FULLSCREEN/MAXIMIZED clients by the `fullscreen` mode and reports AGREE/DIFFER/TILED/BADSIZE plus its own verdict codes. | `PROVINCE.md:32` |
| `tools/mado-globals.py` | Read-only census of the Wayland globals the compositor advertised, parsed from the portal journal (saved file or `--live`): latest session, fixed class table, `--diff` drift and `--expect NAME` presence. | `PROVINCE.md:31` |
| `tools/mado-hostguard.py` | Pins declared operator-owned paths, runs a command against a scratch HOME (or a bubblewrap-masked one), re-pins and fails if any declared path moved; creates and writes no file of its own. | `SCORECARD.md:2762` |
| `tools/mado-keysym.py` | Answers which key, level and modifier masks type a keysym under an `xkbcli compile-keymap` serialization, byte-equal on stdout and exit status to `xkbcli how-to-type --disable-compose --keysym`. | `SCORECARD.md:2730` |
| `tools/mado-monitors.py` | Joins `monitor =` rules with `hyprctl monitors all -j`: newest-match-per-selector semantics, `desc:` short/long selectors, the 1/120 scale correction; AGREE/DIFFER/DISABLED/UNRULED/NOT_COMPARED. | `PROVINCE.md:100` |
| `tools/mado-options.py` | Static resolver of a config tree's general option table: walks the `source` graph, excludes handler keywords and keyed special categories, resolves the LAST declarer per key with owner file, line and layer. | `SCORECARD.md:2436` |
| `tools/mado-terminal.py` | Predicts which terminal `xdg-terminal-exec` 0.14.3 picks and why, cold and warm cache, reproducing the resolver's stdout and exit status with no process, socket or file write. | `SCORECARD.md:2660` |
| `tools/mado-tripwire.py` | Post-hoc classifier over OMP session transcripts (JSONL) of the commands a seat issued: host_mutation, package_query, live_probe, tool_install, vcs_write; parses, never executes. | `PROVINCE.md:20` |
| `tools/mado-verify.sh` | Config-plane verdict gate (v1): verifies the declared hypr core, waybar, walker and terminals planes against live bytes and prints one `MADO_VERIFY: CLEAN` or `MADO_VERIFY: DIVERGED` line. | `PROVINCE.md:18` |
| `tools/mado-wsrules.py` | Derives the `hyprctl workspacerules -j` JSON array from a config tree's bytes alone, transcribing hyprlang 0.6.8 line continuation, comment, variable and workspace-rule semantics. | `SCORECARD.md:1766` |
| `quality/check-axis-scores.py` | Calibration gate: re-derives the lane's last published axis table with each axis's own committed instrument and fails when the publication no longer matches the repo it describes. | `SCORECARD.md:2081` |
| `quality/check-control-receipts.py` | QUALITY 36 successor: a qualifying control receipt under `.ufo/waves/round-N/controls/` must be committed strictly before the data-wave registry's `createdAt`, with each named shape covered by `--seeds` receipts. | `corpus/lessons/round-25-verifier-spotcheck.md:135` |
| `quality/check-counter-discrimination.py` | Scores admission counters against a frozen manifest of accept and reject controls, so an always-accept, always-reject or crashing instrument cannot reach the target. | `PROVINCE.md:61` |
| `quality/check-deliverables.py` | Seat prototype for QUALITY criterion 101: every deliverable declared under `## Deliverables` or a `Report:` trailer must exist at the cited revision; free-text path tokens are not declarations. | `corpus/QUALITY.md:566` |
| `quality/check-evidence-pointers.py` | Evidence-pointer durability gate: re-derives the round-35 dangling pointers, the inherited uncommitted set, a named scratch disposition with counted size, and a tip-revision axis transcript. | `PROVINCE.md:64` |
| `quality/check-index-rows.py` | Index-row fidelity gate: for each coverage-map row it checks table membership, at least three non-empty cells, defined S-ids, resolvable artifact cites and Holds-versus-note overlap. | `SCORECARD.md:2032` |
| `quality/check-index.py` | Navigation-completeness gate: every admitted `corpus/knowledge/*.md` note must have exactly one index row in `corpus/README.md` at the scored revision, under the literal S185 fence semantics. | `SCORECARD.md:202` |
| `quality/check-landed-contract.py` | QUALITY 96: a landed out-of-contract list must be neither narrower than nor silently different from the frozen reference; every ADDED or REMOVED class must be registered or the verdict is NARROWED/UNDECLARED. | `corpus/lessons/round-48.md:245` |
| `quality/check-locators.py` | Recomputes prose `<receipt>:<line>` locators against a directory of pinned receipts, deciding whether the cited receipt lines carry the identifiers of the backticked fragment the locator is attached to. | `SCORECARD.md:2548` |
| `quality/check-population.py` | QUALITY 37: a predicate's registered metrics and population total must agree with its counter's reported summary fields, CASE-line count and denominator. | `SCORECARD.md:1735` |
| `quality/check-r38-discrimination.py` | Round-38 discrimination gate: clones the lane into a sandbox, applies each manifest write, commits under a sandbox identity and scores the c1/c2 counters only on verdict agreement with `expect`. | `SCORECARD.md:200` |
| `quality/check-round-outcome-first.py` | QUALITY 99: a round's closure section in `SCORECARD.md` must lead with the round-level outcome named by the path that carries it, not with registration, counter ids or seat counts. | `corpus/lessons/round-48.md:187` |
| `quality/check-session-material.py` | Privacy gate v3: every tracked file in scope at a revision is read from the object database and refused if it carries raw session material that SKILL.md rule 4 keeps out of the repo. | `PROVINCE.md:100` |
| `quality/check-state-cite.py` | Seat prototype for QUALITY criterion 100: a claim about which state a compositor reads must cite the line that SETS that state, and the claimed value must agree with the setters that exist. | `corpus/QUALITY.md:560` |
| `quality/check-wave-done.py` | Mechanical WAVE-DONE gate: every committed `<wave>.ready` for the round must have a `<wave>-results.json` in which every seat carries a terminal status; reads committed bytes only. | `SCORECARD.md:2763` |
| `quality/counter-selftest.py` | Suite A behavioural self-test over the round-26 counters: each counter's harness surfaces are replaced with synthetic fakes, so a correct judgement passes and a broken one fails with no hash or pattern pinning. | `SCORECARD.md:1767` |
| `quality/counters/c1-idle-lock.py` | PRED-C1-r36-v1, the repaired round-35 idle-lock counter: `digest-match` binds the declared sha256 to the bytes actually read, and `row-in-registry` scores only rows inside the `## Registry` section. | `PROVINCE.md:56` |
| `quality/counters/c1-r37-event-ground.py` | PRED-C1-r37-v2: counts the frozen target entries that land on event-socket delivery ground the lane did not hold at base, bound to `source:` lines, registry rows and Gate receipts. | `SCORECARD.md:2369` |
| `quality/counters/c1-r38-event-ground.py` | PRED-C1-r38-v3: v2's clauses plus pin binding of every Gate digest, unique registry rows, a quote floor and lineage clauses, repairing the round-37 cribs. | `SCORECARD.md:200` |
| `quality/counters/c1-r40-live-v2.py` | PRED-C1-r40-v2: re-registration after v1 was falsified, closing model-exec, a forged call log, an echo selftest and replayable fixtures; the tool is scored on every declared key. | `SCORECARD.md:2480` |
| `quality/counters/c1-r40-live.py` | PRED-C1-r40-v1, superseded: scores `tools/mado-options.py` merging a live compositor in its native forms through `hyprctl getoption`; falsified by round-40 w2 before any data commit. | `.ufo/waves/round-40/registration.md:38` |
| `quality/counters/c1-r41-globals-v2.py` | PRED-C1-r41-v2: re-registration closing eight cheats and thirteen surviving mutants, including payload readability, a path-only b2, getattr evasions and journal-format drift. | `SCORECARD.md:2502` |
| `quality/counters/c1-r41-globals.py` | PRED-C1-r41-v1, superseded: read-only Wayland-globals census counter, bubblewrap-sandboxed with per-run nonce-mixed fixtures; falsified by round-41 w1 before any data commit. | `corpus/QUALITY.md:393` |
| `quality/counters/c1-r42-geometry.py` | PRED-C1-r42: scores `tools/mado-geometry.py` in a bubblewrap sandbox with RLIMIT_NPROC 1, opaque fixture directories, nonce-mixed fixtures and 37 cases. | `SCORECARD.md:2535` |
| `quality/counters/c1-r44-geometry-states-v2.py` | PRED-C1-r44-v2: re-registration closing sandbox-only state logic, selftest-only state assertions and the hole where an all-state dump printed a clean verdict without comparing anything. | `SCORECARD.md:2570` |
| `quality/counters/c1-r44-geometry-states.py` | PRED-C1-r44, superseded by v2: scores the state-aware geometry extension that names FULLSCREEN and MAXIMIZED clients and ends NOT_COMPARED with exit 5. | `.ufo/waves/round-44/registration.md:27` |
| `quality/counters/c1-r45-monitors-v2.py` | PRED-C1-r45-v2: re-registration against eleven cheat tools and six contract errors, importing v1's fixture helpers and adding 32 more fixtures. | `SCORECARD.md:2600` |
| `quality/counters/c1-r45-monitors.py` | PRED-C1-r45, superseded by v2: scores `tools/mado-monitors.py` on 49 frozen fixtures plus selftest and readonly clauses, each run in a fresh directory under `--work`. | `.ufo/waves/round-45/registration.md:21` |
| `quality/counters/c1-r46-devices-v2.py` | PRED-C1-r46-v2: re-registration against ambient-reference cheats and six contract defects including strtof rounding, hex floats and a final continuation line. | `PROVINCE.md:109` |
| `quality/counters/c1-r46-devices-v3.py` | PRED-C1-r46-v3: v2 with the clause-r tripwire moved onto a unix socket, because v2 failed its own controls (TRIP-ABSOLUTE-PATH, TRIP-SELFTEST-ONLY). | `PROVINCE.md:109` |
| `quality/counters/c1-r46-devices.py` | PRED-C1-r46 v1, superseded: scores `tools/mado-devices.py` with the round-45 v2 harness re-cut for this tool, sandboxed, nonce-mixed and generated-case judged. | `PROVINCE.md:108` |
| `quality/counters/c1-r47-terminal.py` | PRED-C1-r47: scores `tools/mado-terminal.py` against the pinned real xdg-terminal-exec v0.14.3 resolver, with 190 fixtures plus 150 generated cases judged by that resolver. | `SCORECARD.md:2660` |
| `quality/counters/c1-r48-terminal-cache-v2.py` | PRED-C1-r48-v2: closes the tool that attempt-and-swallows the cache save (EROFS) and the warm-hit path that never printed `--print-content`, over 228 warm fixtures. | `SCORECARD.md:2707` |
| `quality/counters/c1-r48-terminal-cache.py` | PRED-C1-r48, superseded by v2: adds the warm-cache path of the terminal-selection prediction to the round-47 scoring. | `corpus/lessons/round-48.md:153` |
| `quality/counters/c1-r49-keysym.py` | PRED-C1-r49: scores `tools/mado-keysym.py` byte-equal to the pinned libxkbcommon 1.13.2 `how-to-type` judge on 633 fixtures plus 150 generated cases; never attacked by a wave 2. | `SCORECARD.md:2736` |
| `quality/counters/c1-r50-bind-entry.py` | PRED-C1-r50: admits the bind-key-match entry through pin-bound rows, registry position and a quote floor; the round-50 wave 2 falsified its novelty claim, not its clauses. | `SCORECARD.md:2754` |
| `quality/counters/c2-ledger.py` | PRED-C2-r36-v1, repaired: the lane's evidence ledger — a pinned live clause set, receipts bound to the control they belong to, and a computed ledger tip instead of prose plus a hardcoded hash. | `PROVINCE.md:59` |
| `quality/counters/c2-r37-eventq.py` | PRED-C2-r37-v2: exports `tools/mado-eventq.py` into a private scratch directory and scores it on ten frozen cases with `fixtures`, `readonly` and `live` clauses. | `SCORECARD.md:2370` |
| `quality/counters/c2-r38-eventq.py` | PRED-C2-r38-v3: v2's ten fixture cases plus clients-first ordering, a two-user server row, whitespace in a subscriber comm, `--expect-client` presence and a lagging-clean assertion. | `SCORECARD.md:2435` |
| `quality/counters/c2-r38-request-ground.py` | PRED-C2-r38-v1: counts the three request-socket contract entries that land on coverage ground the lane did not hold at the round base. | `SCORECARD.md:201` |
| `quality/counters/c2-r40-forms-entry-v2.py` | PRED-C2-r40-v2: closes the round-40 forgeries — one receipt shared by four ids, substring `used-by`, free-text count lines, fence-blind rows and a stale GATE line before the valid one. | `SCORECARD.md:2481` |
| `quality/counters/c2-r40-forms-entry.py` | PRED-C2-r40-v1, superseded: admits the getoption native-forms entry through four or more sources, registry rows, an opened date and pinned receipts. | `.ufo/waves/round-40/registration.md:77` |
| `quality/counters/c2-r41-focus-entry-v2.py` | PRED-C2-r41-v2: closes nine forgeries and 29 surviving mutants, including invented receipts, a localized source behind a redirect and ghost citations past the header window. | `SCORECARD.md:2503` |
| `quality/counters/c2-r41-focus-entry.py` | PRED-C2-r41-v1, superseded: admits the Hyprland focus-grab entry with fenced code removed from the entry and the README before any line is matched. | `corpus/lessons/round-41.md:128` |
| `quality/counters/c2-r42-gkeep-entry.py` | PRED-C2-r42: gkeep-geometry entry admission with word-bounded quotes, a computed locator clause and an own-work census; never scored, because round 42 stopped before its wave. | `corpus/lessons/round-44.md:180` |
| `quality/counters/c2-r43-gkeep-entry-v2.py` | PRED-C2-r43-v2: adds a single-occurrence word-bounded quote clause, a raw.githubusercontent location allowlist and a per-line quote-and-locator coverage clause. | `SCORECARD.md:2536` |
| `quality/counters/c2-r43-gkeep-entry.py` | PRED-C2-r43, superseded by v2: the round-43 re-registration of PRED-C2-r42 as a constants-only re-cut with re-captured own-work pins. | `corpus/lessons/round-43.md:150` |
| `quality/counters/c2-r44-gkeep-size-request-v2.py` | PRED-C2-r44-v2: closes forged receipts, pinned bytes cited under a false URL, prose contradicting the census, census-prefix hiding and quote-only entries. | `SCORECARD.md:2571` |
| `quality/counters/c2-r44-gkeep-size-request.py` | PRED-C2-r44, superseded by v2: the round-43 v2 clauses re-cut for the gkeep size-request entry, with five pins and a staged-file clause. | `corpus/lessons/round-44.md:179` |
| `quality/counters/c2-r45-monitor-entry-v2.py` | PRED-C2-r45-v2: closes nine forged revisions and five unpinned entry facts through five tightenings, five more pins and seven more surfaces. | `SCORECARD.md:2601` |
| `quality/counters/c2-r45-monitor-entry.py` | PRED-C2-r45, superseded by v2: monitor-rule entry admission — the round-44 v2 clauses re-cut with a monitor census and a locator range-width bound. | `.ufo/waves/round-45/registration.md:46` |
| `quality/counters/c2-r46-input-device-entry-v2.py` | PRED-C2-r46-v2: v1 plus clause k against six forgeries outside the declared residuals, and `OK` added to the verdict token list. | `SCORECARD.md:2632` |
| `quality/counters/c2-r46-input-device-entry.py` | PRED-C2-r46, superseded by v2: the round-45 v2 entry counter re-cut for the input-devices entry with new constants, pins, census, surfaces and verdict tokens. | `PROVINCE.md:111` |
| `quality/counters/c2-r47-terminal-entry.py` | PRED-C2-r47: admits the terminal-selection entry, trusting committed fetch pins only when their digests equal the hard-coded xdg-terminal-exec v0.14.3 digests. | `SCORECARD.md:2661` |
| `quality/counters/c2-r48-xkb-entry-v2.py` | PRED-C2-r48-v2: enforces the pin file mode, removes the 600-character quote-drop and replays `/usr/bin/xkbcli` in a clean environment instead of a PATH lookup. | `SCORECARD.md:2708` |
| `quality/counters/c2-r48-xkb-entry.py` | PRED-C2-r48, superseded by v2: admits the XKB-compile entry, binding each committed fetch pin to the digest its citing row records. | `corpus/lessons/round-48.md:153` |
| `quality/counters/c2-r49-bind-entry.py` | PRED-C2-r49: admits the bind-key-match entry through row-bound pins, a quote floor and held-row binding; round 49 ran no wave 2, so it was never attacked. | `SCORECARD.md:2737` |
| `quality/counters/c2-r50-session-gate.py` | PRED-C2-r50: scores the session-material gate a revision installs — its own selftest at 94 or more with every v2 case name present, plus behavioural detection of the covered shapes. | `SCORECARD.md:2755` |
| `quality/counters/c3-r39-options.py` | PRED-C3-r39-v2: scores `tools/mado-options.py` for existence, standard-library-only imports, a selftest floor and behaviour on generated config trees. | `SCORECARD.md:2436` |
| `quality/counters/c4-r39-options-entry.py` | PRED-C4-r39-v1: admits the config-option-table entry through its S218 and S219 rows, registry position, opened date and pinned bytes. | `SCORECARD.md:2437` |
| `quality/population-suite.py` | Offline fixture suite over `quality/check-population.py`: writes each fixture's registration and receipts under `$TMPDIR` and requires the checker's expected exit status per fixture. | `SCORECARD.md:1767` |
| `quality/ratio-domain-meta.py` | Re-runnable domain-versus-meta count over the claim rows of a SCORECARD round window at a revision; read-only, standard library only, `--rule` prints the classification rule. | `SCORECARD.md:2583` |

The round-51 integration adds three population files absent at the base: the checker
`quality/check-tool-ledger.py`, the C1 counter `quality/counters/c1-r51-ledger.py`, and
the C2 counter `quality/counters/c2-r51-dispatch-entry.py`. Their ledger rows point to
the round-51 registration, where each basename is named.

| `quality/check-tool-ledger.py` | Derives the tracked-instrument population at a revision and checks its accountability ledger. | `.ufo/waves/round-51/registration.md` |
| `quality/counters/c1-r51-ledger.py` | PRED-C1-r51: scores completeness of the tracked lane-level tool ledger at a pinned revision. | `.ufo/waves/round-51/registration.md` |
| `quality/counters/c2-r51-dispatch-entry.py` | PRED-C2-r51: scores sourced dispatcher-entry admission and candidate-inclusive lexical overlap. | `.ufo/waves/round-51/registration.md` |
| `tools/mado-verify.sh` | Second row with four cells. | `PROVINCE.md:18` | extra |
