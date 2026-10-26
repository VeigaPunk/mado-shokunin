# w1/ScrSkill — SKILL.md section and PROVINCE.md refinement for `tools/mado-devices.py` (round 46)

Seat `ScrSkill`, round-46 w1 (hyaku run 9), 2026-10-26. Freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base
`b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`.

**Deliverable:** `.ufo/waves/round-46/w1/ScrSkill/skill.md` — append-ready text, two required blocks plus one optional
pair of table rows, each naming the exact line it goes after. No `SKILL.md` and no `PROVINCE.md` edit: the L1 is the
integrator (`git status --porcelain -- SKILL.md PROVINCE.md` empty at this seat's start; the lane working tree carries
only untracked seat material).

## Behavior

Read (not edited): `SKILL.md` (2102 lines; round-45 section `:2100-2102` is the tail; Claim-first routing
`:142-158`; Read-only probes `:204-225`), `PROVINCE.md` (100 lines; tool table `:24-32`, coverage sentence `:34`,
round-45 refinement `:100`), the reference `.ufo/waves/round-46/l1-draft/mado-devices.py` (566 lines; 88-line
docstring), `.ufo/waves/round-46/l1-draft/entry.md` (census at `:53`), the frozen counters
`quality/counters/c1-r46-devices.py` and `c2-r46-input-device-entry.py`, all ten pins under
`.ufo/waves/round-46/fetch/`, the L1 receipt `.ufo/waves/round-46/receipts/live-devices-host-l1.txt`, and the host
config files the draft names (`~/.config/hypr/{hyprland,input}.conf`, the omarchy default `input.conf`, the theme and
toggles files).

Wrote, in the SKILL file's existing shapes:

- **Block 1** — new § "Input-device rules versus running devices (round 46)", appended after `SKILL.md:2102`: the exact
  host command, a "pass every file yourself" paragraph grounded on this host's `source =` chain, the join model with
  pin locators, a **13-row decision table** (`verdict | where it prints | what it means | next read-only step`), the
  exit map in the docstring's tested order, a four-bullet **read-only boundary** (reads / writes / process and socket /
  session material), five licence notes, the host run and known limits.
- **Block 2** — the PROVINCE.md refinement, appended after `:100`, plus one **conditional** tool-table row after `:32`:
  the owned input-device plane statement, the two round-46 counters as record instruments (bubblewrap, 90 fixtures ×
  3 runs, 150 nonce cases, the four PATH decoys for the fixture and generated runs with clause r's real scope
  stated; the C2 census line and 28 surfaces), the entry as source-read
  knowledge, declared limits. Alongside it, an insertion note on a **pre-existing** gap (finding F6).
- **Block 3** (optional) — the Claim-first routing row (after `:158`) and the Read-only-probes row (after `:225`) for
  the same tool, in the two tables' exact column shapes, because round 45 gave `mado-monitors.py` both and a section
  with no route to it is inert.
- **Block 4** — a locator receipt table (not SKILL text) for the integrator's re-check, and the quote list.

## Gates run by this seat

| gate | command | result |
|---|---|---|
| draft truth (91 checks) | `python3 -I .ufo/waves/round-46/w1/ScrSkill/verify.py` (cwd = lane) | `VERIFY: checked=91 failed=0`, rc 0 — every cited `pin:line`, docstring line and counter line re-opened and searched for the promised token; the census line byte-equal to `entry.md:53`; the draft's exit order equal to the docstring's parsed order; 13 table rows with four cells; every verdict token present; six quotes ≤ 25 words and present in source **and** draft; no `/home/` path and no session-material key; the `tools/mado-devices.py` absence claim still true; both host summary lines and the virtual-keyboard line present in the draft and in their receipts; 14 observed behaviours checked in the receipts; the three clause-r scope tokens present and their two counter locators re-opened. `receipts/verify.txt` |
| reference selftest | `python3 -I .ufo/waves/round-46/l1-draft/mado-devices.py --selftest` | `MADO_DEVICES_SELFTEST: 48/48 passed` (`receipts/locators.txt` §D) |
| host chain run | `hyprctl devices -j \| python3 -I <reference> --devices - --config <omarchy default input.conf> --config ~/.config/hypr/input.conf` | `MADO_DEVICES: keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK`, rc 0 (`receipts/host-runs.txt`); the same run with only the user file reproduces the L1's line |
| follow-up verbs the table prescribes | `hyprctl getoption input:kb_layout -j` → `{"option": "input:kb_layout", "str": "br", "set": true }`; `input:scroll_factor` → `{"…", "float": 1.000000, "set": false }`; `xkbcli compile-keymap --layout br --variant '' --options compose:caps` → rc 0, `--variant nosuchvariant` → rc 1 with `Failed to compile xkb_symbols` | `receipts/host-runs.txt` |
| reference on ten hand-built fixtures | ten runs over synthesised dumps | `verdict=` FALLBACK / VIRTUAL / NO_SUCH_DEVICE / MATCHED / DIFFER / NO_KEYBOARDS / NOT_COMPARED / STALE_BLOCK and `SETUP bad_json` all observed with their exit codes (`receipts/synthetic-verdicts.txt`) |

## Findings

**F1 — the virtual keyboard flaps, so `keyboards=` and `virtual=` are not constants.** Two runs of the exact host
command, recorded moments apart within this seat, disagree: the earlier capture printed
`MADO_DEVICES: keyboards=9 agree=9 differ=0 fallback=0 virtual=0 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0
verdict=OK` (no `hl-virtual-keyboard` element in that dump), and the next capture of the same command printed
`keyboards=10 … virtual=1` with `hl-virtual-keyboard-fcitx5` present (`receipts/host-runs.txt`, section "the virtual
keyboard flaps across captures"). Attacks: any reading of `virtual=0` as a defect, and any comparison of `keyboards=`
across captures. Supports: the `VIRTUAL` decision row and the known-limits paragraph. Note the L1 receipt is a third
observation, also `keyboards=10 virtual=1`.

**F2 — `NOT_COMPARED` outranks `DIFFER`, and `DIFFER` outranks `STALE_BLOCK`; the table says so because it was
observed.** A `$` in one `scroll_factor` RHS plus a mouse that also differs prints `mice_differ=1 unsupported=1` and
exits 5 (`NOT_COMPARED`); a stale block plus a differing mouse prints `stale=1 mice_differ=1` and exits 1
(`DIFFER`); `STALE_BLOCK` (rc 4) appears only when the stale block is the *only* problem
(`receipts/synthetic-verdicts.txt`). Attacks: the first draft's flat assumption that a stale block always surfaces as
rc 4. Supports: the exit-map sentence and the `STALE_BLOCK` row's "reachable only in that clean case".

**F3 — a `device { }` block whose first key is not `name` never reaches a comparison.** `device {\n scroll_factor =
0.5\n}` produces `blocks=0 unsupported=1` and `NOT_COMPARED` (rc 5): the tool counts the line instead of modelling
Hyprland's "keeps reading the block into a device it names itself" behaviour (`mado-devices.py:58-60`). So the block
is never checked and only the `unsupported` count witnesses it. Attacks: the assumption that every `device` block the
file shows is compared. Supports: the `NOT_COMPARED` row's grep-the-files next step (the count is not line-attributed).

**F4 — a hand-trimmed dump reads `DIFFER`, not `AGREE`.** A keyboard object holding only `name` prints
`differ=layout,variant,options,model,rules verdict=DIFFER`, because a missing name never equals an expected one
(`mado-devices.py:71`). Attacks: any workflow that prunes a dump "to the fields I need" and then expects agreement.
Supports: the "a sparse dump reads DIFFER, not AGREE" licence note.

**F5 — `VIRTUAL` beats `DIFFER`, so a virtual keyboard can never fail a run.** A `device` block setting
`kb_layout = de` for `hl-virtual-keyboard-fcitx5`, against a dump printing `us` with four empty names, prints
`differ=layout verdict=VIRTUAL` and the run exits **0** with `verdict=OK` (`receipts/synthetic-verdicts.txt`).
Attacks: reading `differ=` on a virtual keyboard line as a host disagreement. Supports: the `VIRTUAL` row and the
licence note.

**F6 — `PROVINCE.md:34`'s coverage claim is already false, and my row does not repair it.** The sentence "the inventory
above covers every tracked file under `tools/`…" sits above a table of nine rows (`:24-32`) while `tools/` holds
thirteen files; `mado-eventq.py`, `mado-options.py`, `mado-wsrules.py` and the round-45 `mado-monitors.py` have no row
(`tools/mado-monitors.py` is tracked at the tip, `100755`, blob `551eceef…`). Adding the round-46 row makes ten of
thirteen. This is pre-existing, outside this seat's write scope, and recorded here with the insertion note so the L1
decides between four more rows and rewording the sentence. Attacks: the coverage claim's literal reading. Supports:
the round-23 wave-2 correction's own distinction between "every tracked file" and "every tracked tool it runs".

**F7 — the input chain this host builds is two files, and the later one wins.** `~/.config/hypr/hyprland.conf:11`
sources `~/.local/share/omarchy/default/hypr/input.conf` (`kb_layout = us` at `:3`) and `:17` sources
`~/.config/hypr/input.conf` (`kb_layout = br` at `:10`); the theme file (`:13`) and the toggles glob (`:23`) carry no
`input`/`device`/`kb_`/`scroll_factor` line (0 matches each, `receipts/host-runs.txt`). Because the tool follows no
`source =`, the L1's single-file run and this seat's two-file run agree today only because the user file overrides
every value the omarchy default sets. Supports: the "pass every file yourself" paragraph and the exact host command in
Block 1. Attacks: the reading that `--config ~/.config/hypr/input.conf` alone models the host chain.

**F8 — clause r is a PATH-lookup check, and the province text now says exactly that.** The w1 seat `SentTool`
reported (`.ufo/waves/round-46/w1/SentTool/findings.md` F1/F2, receipts `SentTool/evidence/clause-r-bypass-*.txt`)
that clause r's marker decoys can be bypassed; I re-opened the frozen counter and confirmed the two lines myself:
the `--selftest` run is launched with `env={"PATH": "/usr/bin:/bin", …}` (`c1-r46-devices.py:374-375`), so a bare-name
`hyprctl` there resolves to the real binary and leaves no marker, and `hidden_paths()` returns only
`realpath(repo)`, the lane root and its parent (`:241-243`), so the tmpfs set hides no `$HOME` and no
`/run/user/<uid>` — under `--ro-bind / /` the live compositor socket stays reachable for an AF_UNIX connect. Block 2
therefore now states what the decoys guard (the fixture and generated runs), that the selftest run's PATH is
`/usr/bin:/bin`, and that clause r is not a sandbox against absolute execs or a socket. Attacks: the reading that a
green clause r means "the scored tool ran nothing". Supports: SentTool's F1/F2 (I did not run their payloads; the
receipts are cited as received, the two counter lines are mine). This does not change C1's verdict and is not a
counter edit — the counter is frozen and the L1 decides whether a v2 re-cuts the harness.

**F9 — a v2 counter set appeared in the lane while this seat ran, and it is neither read for semantics nor cited.**
`quality/counters/` gained untracked `c1-r46-devices-v2.py` (mtime 17:57:20, 23999 B, sha256 `19d00e66…`),
`c1-r46-fixtures-v2.json` and `c2-r46-input-device-entry-v2.py` (17:59:56) after this seat's counter reading. Its
v1 citations stand as written; Block 2 carries an explicit note that a landed v2 requires re-reading the sandbox,
selftest-PATH, count and census cells against the landed bytes. Attacks: any silent substitution of v2 behaviour into
this draft. Supports: ConnCrossClaim-3's broadcast; nothing here runs or scores either version.

## Touched surfaces

- `.ufo/waves/round-46/w1/ScrSkill.md` (this report)
- `.ufo/waves/round-46/w1/ScrSkill/skill.md` (deliverable: Block 1 SKILL section, Block 2 PROVINCE refinement + row,
  Block 3 optional routing/probe rows, Block 4 locator table)
- `.ufo/waves/round-46/w1/ScrSkill/verify.py` (88-check verifier, stdlib only, re-runnable as written)
- `.ufo/waves/round-46/w1/ScrSkill/receipts/{locators.txt,host-runs.txt,synthetic-verdicts.txt,verify.txt}`
- Scratch `/fast/scratch/hyaku-mado-r46-ScrSkill-*` (four `mktemp -d` trees for fixtures and raw dumps): all removed;
  no `/tmp` file used, no raw `hyprctl devices -j` dump left anywhere.
- Not touched: `SKILL.md`, `PROVINCE.md`, the reference, the counters, fixtures, controls, registration, pins,
  `corpus/`, `quality/`, any git/jj index, any host config byte, any package manager.

## Out of scope (deliberate)

- Installing `tools/mado-devices.py` or scoring `c1-r46-devices.py` / `c2-r46-input-device-entry.py`. This seat drafts
  prose; the counters belong to the C1/C2 seats and the L1. No bubblewrap run, no clone, no counter invocation here.
- The entry `corpus/knowledge/hyprland-input-devices-r46.md` and rows S316-S325 — the entry seats' business.
- Round-45 closure D2-D6 (the gate's prose serial rule, the 48 pre-existing findings, the untracked results file).
  Only D1's *tool* is adjacent to this seat, and only as prose.

## Limits

- The decision table's expected side is the tool's own model of the per-device lookup, so every `differ=` label is
  `[INF]` while the printed side is `[OBS]`. Nothing in this seat says Hyprland's real lookup agrees with the model
  beyond the pins the entry cites.
- The host has no `device` block (`blocks=0`), so `MATCHED`, `NO_SUCH_DEVICE`, `STALE_BLOCK`, `block=yes` and every
  mouse `DIFFER` are exercised only by the reference's fixtures and by this seat's ten synthesised dumps, never by a
  live host run.
- `getoption` was run for four options only; no per-device `getoption` path is claimed, because none was run.
- The `xkbcli` step reproduces a *compile* failure, not the compositor's reaction to it; the fallback→`us` shape is
  sourced from the pin (`Hyprland-IKeyboard.cpp:101-116`), not observed on this host (nothing falls back here).
- Tooling: nothing installed, nothing upgraded, no pacman transaction. `python3 -I` and host `grep`/`hyprctl` reads
  only.

## Artifact paths

- `.ufo/waves/round-46/w1/ScrSkill/skill.md`
- `.ufo/waves/round-46/w1/ScrSkill/verify.py`
- `.ufo/waves/round-46/w1/ScrSkill/receipts/locators.txt`
- `.ufo/waves/round-46/w1/ScrSkill/receipts/host-runs.txt`
- `.ufo/waves/round-46/w1/ScrSkill/receipts/synthetic-verdicts.txt`
- `.ufo/waves/round-46/w1/ScrSkill/receipts/verify.txt`
- `.ufo/waves/round-46/w1/ScrSkill.md`
