# ScrLesson — round-47 w1 seat report

Seat: `ScrLesson` (leaf; no subagent dispatch). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD when read
`c24adef2632672325a4eef3e3492f6716ccb6d14`, round base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`; the only commit between them is
the roll-out `c24adef2` ("claims declared, w1 build spec and dispatch (41 seats, policy v1), census before"), so every count below is
the base state plus nothing but that round's setup. Read-only seat: nothing
committed, no tracked file edited, no product code, no counter/fixture/pin/registration edit, no host or compositor mutation, no
terminal launched, no `xdg-terminal-exec` run (not even a `--print-*` one). No tool installed or upgraded. No scratch dir created,
so nothing to delete.

## Deliverable

`.ufo/waves/round-47/w1/ScrLesson/lesson.md` — 281 lines, the round-47 lesson skeleton, drafted from the round-46 structure
(`corpus/lessons/round-46.md`: header paragraph → `## Gate` → `## Registry changes` → `## Search log` → `## Mistakes` →
`### Applications of existing criteria` → `### Conflicts recorded for the judge` → closure items → `## considerthese` →
`## Assimilation`) plus the two sections the round's own contracts require: `## Routed-defect ledger` (QUALITY 90) and
`## Frontier` (frontier step §2b).

Sections and their line numbers (`grep -n '^## \|^### '`, `receipts.txt` tail):

| line | section | state |
|---|---|---|
| 15 | `## Gate` | shape fixed; held ground and the host-binary rejection class written; admitted rows, GATE lines and the rejected list are `<AFTER>` (they are `w1/ScrRows` / `w1/ScoutSpecs` / `w1/ScoutHeld` output) |
| 61 | `## Registry changes` | counts filled from base measurements; row deltas `<AFTER>` |
| 74 | `### Census before → after` | **before pasted verbatim** from `.ufo/waves/round-47/receipts/census-before.txt`; after is `<AFTER>` |
| 103 | `## Search log` | question, where-searched, registry screen and stop/re-open triggers written; identified/screened/included/excluded counts `<AFTER>` |
| 137 | `## Mistakes` | `<AFTER>` from `w1/ScrMistakes`; the mandatory-mined-mistake rule stated, plus three known-now candidates named as candidates, not mistakes |
| 151 | `### Applications of existing criteria` | two mappings stated as forced (criterion 90; criterion 24 via M46-5); the rest `<AFTER>` |
| 161 | `### Conflicts recorded for the judge` | conflict 1 **written and resolved by command**; conflict 2 slot left |
| 173 | `## Round-46 closure items` | R1-R4 table with seat + planned landing, plus a drafted acceptance (command + expected observation + fail condition) per item |
| 211 | `## Routed-defect ledger` | 15 rows, ages computed at round 47, three re-measured at base |
| 238 | `## considerthese` | proposal 3 (now QUALITY 90) recorded; proposals 2 and the rest pointed at their seats with `<AFTER>` dispositions |
| 245 | `## Assimilation` | `<AFTER>` with the expected outcome stated so the section cannot land blank |
| 253 | `## Frontier` | the five frontier-step parts with the README `## Frontier` bullet **fully drafted** and its provenance |

`<AFTER>` markers: **33** (`grep -c '<AFTER>' lesson.md`), each a value that cannot exist before the freeze or before a w1 seat
returns. No `<AFTER>` stands for something this seat could have measured.

## Gates / contracts this draft is shaped against

- Frontier-step contract `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-47.md:42-75` (curate rows only after opening the
  source this round; census before → after with exit 0 at round end; one mined mistake, sweep pasted if none; one sourced claim;
  README frontier bullet). The skeleton carries a `## Frontier` section numbering all five.
- QUALITY 90 (`corpus/QUALITY.md:454-461`) — every routed defect gets one identity, a first locator and an age; a third deferral
  without landing is mined as a `landing` mistake. Implemented as `## Routed-defect ledger`.
- CORPUS rule 2 (append-only supersession) — reflected in the R4a row of the registry table and in the R1/R4b/R4c acceptance
  ("appended erratum", "nothing above rewritten").
- Round shape from `.ufo/waves/round-47/claims.md:3-7` (two v1 waves, w1 = 41 seats, nothing frozen until after w1).

## Registries before (measured, no value typed)

| surface | command | output |
|---|---|---|
| rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `262` |
| top id | `grep -oE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md \| tr -dc '0-9\n' \| sort -n \| tail -1` | `325` |
| knowledge | `ls corpus/knowledge/*.md \| wc -l` | `63` |
| lessons | `ls corpus/lessons/*.md \| wc -l` | `68` |
| tools | `ls tools/ \| wc -l` / `ls tools/ \| grep -c mado-terminal.py` | `14` / `0` |
| README index rows | `grep -cE '^\|[[:space:]]*`?knowledge' corpus/README.md` | `63` |
| census before | `grep -c W04 …` / `grep -c W01 …` on `receipts/census-before.txt` | `14` / `1`, file ends `mado ok …`, `exit=0` |

The C2 row range therefore starts at `S326`; the supersession block (R4a) is bounded above it in the draft (`S346`+, per the seat
prompt's id-space note), which is written into the registry table so the L1 cannot land it inside the C2 range by accident.

## Round-46 closure items R1-R4 — how each is planned

| item | closure locator | seat fielded this round | draft's acceptance (compressed) |
|---|---|---|---|
| R1 erratum for `hyprland-input-devices-r46.md:57` | `round-46-verifier-spotcheck.md:107` | `ScrErrataR1` | appended block quotes `:57`, cites `.ufo/waves/round-46/receipts/live-devices-host-r46.txt`, names producer hashes `3a803689…` vs `b229efd0…`, states the two-config order; append-only diff (`--numstat` deletions `0`); fails if it cites `live-devices-host-l1.txt` |
| R2 digest of the untracked 3.3 MB tsv | `:111` | `ExecR2Digest` | tracked digest (sha256/bytes/lines/header/class counts) matching the file, tsv gone from `git status` or retention stated; fails if the digest is itself untracked (M46-8 shape) |
| R3 synthetic-fixture marker + prose serial rule | `:113` | `ExecSessionMarker` | five demonstrations: current gate exit 1; marked tree leaves only the real findings; planted real dump unmarked → exit 1; planted real dump in a marked file → exit 1; registry naming a real-serial file → exit 1. Fails if the marker waives by path only. Serial value never printed |
| R4a `S290`-`S297` supersession | `:116`, M46-16 at `round-46.md:307` | `ExecSupersede` | mirror census exit 0, append-only, `supersedes` opener names the predecessor, computed locators; fails if a row lands in `S326`-`S345` |
| R4b round-45 entry's six units (F1 `:84b`, F2 `:96`, F3 `:98`, F4 `:18b`/`:106`/`:107`) | `:116` | `ScrErrataR45` | six rulings each with the settling pin line; a unit that does not hold is `REFUTED` with reason |
| R4c round-44 `ConnCalibration` (E1-E6 drafted) | `:116` | `ScrErrataCal` | six append-only `SCORECARD.md` lines, each with its command; fails if an earlier line is edited |

The acceptance text is a draft: the closure's own wording is quoted for the defect (`:107-118`), the command/observation pairs are
this seat's construction and the draft says so ("the L1 may tighten them").

## Findings

**F1 — the round-46 lesson contradicts itself on R45-D4; resolved at base by one command.** `corpus/lessons/round-46.md` D4 says the
digest line "is committed beside `summary.txt`" while M46-8 in the same file says the 282 B digest is untracked. At base,
`git ls-files .ufo/waves/round-45/w1/MutC1Counter/` lists `results.digest.txt` among five tracked files (no `results.json`), so D4
holds at the landing revision and M46-8 described its own draft time. Recorded as conflict 1 in the draft rather than silently
resolved, and the ledger carries R45-D4 as closed in round 46. (Observed; receipt in `receipts.txt`.)

**F2 — the inherited routed ledger needs three state corrections at round 47, and two of them are re-measured.** R38-3:
`stat -c %s .ufo/waves/round-38/receipts/eventq-live-ss.txt` → `190816`, still in the tree. R40-2: `.ufo/waves/round-40/receipts/`
still holds exactly one `axis` file (the base), so the tip receipt is still uncommitted. R41-4: `corpus/lessons/round-41.md:48`
still writes `PROVINCE.md:75`. R45-D4 and R45-D5 close in round 46; R45-D3's registry half landed (`SKILL.md:770`, closure §1) and
its marker half is R3 this round. Ages at round 47 are computed with the round-46 convention
(`.ufo/waves/round-46/w1/ScrRoutedAges/ages.md:14-18`): R38-3/R38-4 = 9, R40-2/R40-3 = 7, R41-2/R41-3a/R41-3b/R41-4 = 6,
R43-D2 = 4, R44-D7 = 3, R45-D2/D3 = 2, R46-R1..R4 = 1.

**F3 — the frontier step's "still open" list for round 47 can be written now without a launch.** The round-17 `[UNK]` closes
(`terminal-route-r17.md:144-145`, the resolver picking the user-local entry over the system one); what stays open is bounded by the
contract, not by missing data: `uwsm-app` in the bind, the `--dir=` value from `omarchy-cmd-terminal-cwd` (`:149-151`), any warm-cache
path (the tool models a cold cache by contract), the terminal binary's own behaviour (no terminal may be launched), and packaging
drift past `0.14.3-2` (`:135`). The drafted README bullet is in the file at `:261-269`, with its provenance (hotkey line
`~/.config/hypr/bindings.conf:2`, held as bytes at `S059`) beside it.

**F4 — the round's row-id space is stated in the draft to prevent a collision.** C2 opens at `S326`; the R4a supersession block must
not take `S326`-`S345` (the seat prompt for `ExecSupersede` says the same). Written into the registry table's supersession row so the
L1 sees the constraint where it applies, not only in a seat prompt.

**F5 — the gate's held-ground block is the round's premise and is written, not deferred.** `terminal-route-r17.md` (S056-S060 +
rejected S061-S062 at `:152`), `terminal-trees-r23.md` (S123-S152) and `terminals-and-omarchy.md` are named as not re-claimed, each
with its subject, so a reader cannot read the absence as an oversight. The repeated-URL rows (`xdg-terminal-exec` script and README,
the host list files) are expected census `W04`, as in rounds 45/46.

**F6 — the host user-local desktop entry is already a row, so the C2 entry must cite it.** `S071`
(`corpus/SOURCES.md:83`, tier A, `code`) holds the bytes of `~/.local/share/applications/Alacritty.desktop` with the scope cell
"the desktop entry xdg-terminal-exec resolves for `Alacritty.desktop` on this host (bytes only)". A round-47 row for the same path
would be a duplicate with no new scope; the entry and the frontier bullet should cite `S071`. The draft says this in the Gate's
held-ground list. (Found by correcting a false first-draft claim; see Limits.)

## Limits

- This seat measured only the lane's own files and one host config file (`~/.config/hypr/bindings.conf:2`), read once to confirm
  the hotkey line the frontier bullet quotes. No `hyprctl`, no resolver run, no process start.
- Peer outputs (`w1/ScrRows`, `w1/ScrMistakes`, `w1/ScoutSpecs`, `w1/ExecSessionMarker`, …) were **not** read as evidence; the draft
  points at their directories as landing targets and nothing more. Where a peer's value must enter, the draft carries `<AFTER>`.
- The acceptance criteria for R1-R4 are this seat's construction from the closure's wording; they are labelled as such in the file.
- The draft is not the landing: the L1 owns integration, the freeze, the census after, and every `<AFTER>` value.
- Locators cited in the draft were computed with `grep -n` (all in `receipts.txt`); five first-draft locators were corrected after
  measurement (`round-46.md:9-11`→`:8-10`, `terminal-route-r17.md:154`→`:152`, `:135-139`→`:135`, `ages.md:15-18`→`:14-18`,
  Table 2 `:78-93`→`:76-93`).
- One first-draft **claim** was corrected after measurement: the registry-screen paragraph asserted that no other registry row names
  `xdg-terminal-exec`, which is false — `S071` (`corpus/SOURCES.md:83`) already holds the host user-local `Alacritty.desktop` bytes,
  and `S056`/`S057`/`S060` plus three route paragraphs carry the token (7 hits, `receipts.txt` §"registry-screen correction"). The
  paragraph and the Gate's held-ground list now name `S071`, and the first-use claim is narrowed to the freedesktop spec texts
  (`grep -c 'specifications.freedesktop.org\|spec.freedesktop.org' corpus/SOURCES.md` → `0`).

## Evidence

- `.ufo/waves/round-47/w1/ScrLesson/lesson.md` — the deliverable.
- `.ufo/waves/round-47/w1/ScrLesson/receipts.txt` — 229 lines, 34 commands with output and exit code (base
  counts, census before, held rows, every cited locator, the routed-ledger re-measurements, the hotkey line, and the draft's section
  map).
- `.ufo/waves/round-47/receipts/census-before.txt` (base, exit 0) — quoted verbatim in the draft's census block.

Report path (relative to the lane): `.ufo/waves/round-47/w1/ScrLesson.md`.
