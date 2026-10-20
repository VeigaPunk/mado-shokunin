# RevHarmWatch — round-17 harm-watch command audit

Seat: `MadoR17.RevHarmWatch` (reviewer, leaf; no subagents).
Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

State at review: HEAD `0175f13d83dceb9344fd0ecc5f94aa4aac5dfb53`
(pre-registration), tracked tree clean; round-17 wave artifacts are untracked
(15 entries at review close; the two C2 note drafts appeared during this
audit — §1b). **I ran none of the five commands below.** Evidence is
committed receipts plus static reading of the target scripts (`git show`,
`sha256sum`, `grep`). No tool was installed or updated.

## 1. The round's harm-watch commands

Authority: `SCORECARD.md:821-865` (round-17 declared claims; harm watch at
`:863-864`), `SKILL.md:525-545` (gate registry), `AXES.md` rubric changes are
not needed for these checks. All commands run from the lane root.

| # | Literal command | Expected output on success | Exit | Receipt / basis |
|---|---|---|---|---|
| HW1 | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 372/372 assertions passed` (single line) | 0 | `.ufo/waves/round-16/evidence/legacy-selftest.json` — command `["bash","tools/mado-verify.sh","--selftest"]`, measured `9dcf248`, exit 0; gate bytes unchanged (`fba82a66…`, see §5) |
| HW2 | `python3 -I tools/mado-action-plan.py --selftest` | first line `SELFTEST_SCRIPT_SHA256: 226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3`; 52 `SELFTEST PASS …` lines; last line `SELFTEST_SUMMARY: 52/52 passed` | 0 | `.ufo/waves/round-16/evidence/action-selftest-final.json` — measured `1e31681`, exit 0; tool bytes unchanged (`226220ae…`, see §5). Red shape at `9dcf248`: `SELFTEST_SUMMARY: 51/52 passed failed=['frozen-denied-match']`, exit 1 |
| HW3 | `python3 .ufo/waves/round-16/measure.py <REV>` | one JSON object; **`coverage.count == 7`, `coverage.score == 10.0`**, `coverage.items == ["U1".."U7"]`, `coverage.joins` length 7, `coverage.u7_candidates` length 1; `navigation.notes == navigation.indexed == 30` (32 at content), `missing/extra/duplicates` empty. `calibration` is expected to move this round (14/22 at baseline) and is not a harm signal | 0 (also 0 on a low count; see F2) | `.ufo/waves/round-16/evidence/{before,after-final}.json` stdout; corpus/knowledge, SOURCES.md and README unchanged between `1e31681` and `27cd06f` (`git diff --stat`) |
| HW4 | Fleet-round-1 counting command, literal fence `SCORECARD.md:69-90` (body `:70-89`) with `REV=<rev>` exported | `revision=<sha> indexed=30/30 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` (32/32 at content) | 0 (1 if missing/dangling/duplicate) | Published fence body is 20 lines / 1,063 bytes, SHA-256 `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` — recomputed and equal to the recorded wrapper hash at `SCORECARD.md:194` |
| HW5 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | exactly the three historical W04 lines (S030, S042, S045), then `mado\tok\t…/corpus/SOURCES.md`; **no E-code line** | 0 (1 on E/overdue, 2 on usage/missing registry) | `.ufo/waves/round-17/evidence/census-start.txt` (2026-10-20T10:56:14-03:00, exit 0) and `.ufo/waves/round-16/evidence/census-after.json` — identical four lines, measured `9dcf248` |

HW5 baseline text, verbatim:

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

At integration the three W04 lines must persist and no E01–E12 line may
appear. Additional W04 lines are contract-legal (warnings do not affect the
exit) but should be reported, not silently dropped. `validate` does **not**
print row/tier/status counts; the 55-row baseline came from `measure.py`
`source_registry` / the census `census` mode, not from this invocation.

### 1b. Pre-integration snapshot of the two C2 notes (read-only, at review close)

While this audit was open, two untracked drafts landed:
`corpus/knowledge/idle-lock-route-r17.md` (head-15: `surface: P6`, a
`source:` line with repeated `S0xx-pending` tokens, no `covers:` line) and
`corpus/knowledge/terminal-route-r17.md` (head-15: `surface: P4`,
`source:` line with `S056-pending`…`S060-pending`, no `covers:` line).
`corpus/README.md` still has 30 index rows. This is expected pre-integration,
not a defect, but it fixes the required sequence: HW3/HW4 are
**revision-bound** (`git ls-tree <REV>:…`), so the untracked drafts do not
affect the `0175f13` baseline; L1 must assign the reserved S-ids, replace
every `*-pending` token, mine the registry rows with
`used-by: corpus/knowledge/<file>`, add the two README rows, commit, and only
then run HW3/HW4/HW5. The placeholder tokens as written cannot satisfy rubric
V or E11. Note the idle note repeats one `S0xx-pending` token for six distinct
URLs; each must become a distinct registry id (E03 otherwise).

## 2. Host-surface confirmation (none beyond file reads)

### HW1 — `tools/mado-verify.sh --selftest`

- Dispatch: `--selftest` sets `MODE=selftest` (`:3642`); `:3654-3657` runs
  `selftest` and exits **before** `verify` (`:3660`). The live plane is
  `live_plane()` (`:2968`) and is called only from the `else` branch of
  `[ "$LIVE" = 0 ]` at `:2795`, inside `verify()`.
- The selftest's live-requested sub-invocations are all `env PATH=…`-staged:
  `:685-686`, `:736-737`, `:748-749`, `:765-766`, `:776-777`, `:783-785`,
  `:793-794`, `:993-994`, `:1433`. The staging dirs are built from fixed
  coreutils lists (`:677`, `:990`, `:1013`, `:1031`) plus, only in the OM
  cases, fixture stubs for `omarchy` and `git` (`:673-709`). None of them
  stages `hyprctl`, `systemctl`, `waybar`, `walker`, `pgrep`, `busctl`,
  `printenv`. Entering `live_plane` with any such PATH stops at
  `! have hyprctl` (`:2970`) and emits `live.plane UNKNOWN`; no command runs.
- Even if a later guard were reached, every live executable is `have`-guarded:
  `hyprctl :2970`, `pgrep :3117/:3158`, `printenv :3126`, `waybar :3146`,
  `busctl :3194`, `walker :3207`, `systemctl :3218`, `omarchy :3232`.
  `have` is `command -v` (`:120`), not execution.
- The selftest body (`:393-1542`) contains **zero** `pacman`/`systemctl`
  calls and only two `hyprctl` occurrences, both comments (`:987`, `:1371`).
  It reads no `$HOME`, `/var`, `/proc`, `/sys`, `/run` or compositor state
  (grep over the same range). Scratch is `/tmp/w5-mado-m52-selftest.*`
  (`:395`) and snapshots under `$T/snap` (`:1372`); fixtures are removed on
  success (`:1534`).
- Verdict: file/process reads only — the script itself, fixture trees under
  `/tmp`, coreutils/python3, and fixture stubs. **No hyprctl, pacman,
  systemctl, service, compositor or input call.** Maintenance invariant: the
  hermeticity of the `MADO_VERIFY_LIVE=yes` cases depends on the per-case
  PATH scrub; any future case must keep it (F7).

### HW2 — `tools/mado-action-plan.py --selftest`

- `run_selftest` (`:532`) snapshots its own bytes into a
  `tempfile.TemporaryDirectory(prefix="mado-plan-selftest-")` (`:702-713`)
  and invokes that copy through `_self_invoke` (`:522-530`):
  `sys.executable -I`, `shell=False`, `stdin=DEVNULL`, `timeout=60`,
  `cwd=<temp>`, environment containing only `PATH`. No plan argv is executed;
  the classifier is a static JSON evaluator. The only environment read in the
  whole tool is `os.environ.get("PATH")` (`:525`).
- Verdict: temp-file reads/writes under the tempdir only; no host command.

### HW3 — `.ufo/waves/round-16/measure.py <REV>`

- Imports: `hashlib, json, pathlib, re, subprocess, sys`; the only subprocess
  is `git -C REPO …` (`:63-65`) via `show`/`ls-tree` (`:70-78`). It hashes
  `tools/mado-verify.sh` but records `gate_executed: false` (`:384`);
  safety artifacts are observed for presence/bytes and `executed: false`.
  The result object is `:378-431`, printed as JSON at `:433`, and it exits 0
  at `:436`.
- Verdict: committed-object reads + stdout only. No gate, host, device or
  config access.

### HW4 — Fleet-round-1 counting command

- Inline `python3` importing only `os, re, subprocess`; calls
  `git ls-tree --name-only <rev>:corpus/knowledge` and
  `git show <rev>:corpus/README.md`; prints the revision line and exits.
  No writes, no host commands. The published block's bytes hash to the
  recorded wrapper SHA (§1 HW4).

### HW5 — `scripts/sources-census.sh validate …`

- Header contract (`:7`): read-only; parses `shokunin.conf` textually, never
  sources it; writes only stdout or `--out`. The round invocation has no
  `--out`, so stdout only.
- `validate` uses `gawk`, `date`, `realpath`, coreutils; it contains no
  `pacman|yum|paru|systemctl|hyprctl|git|curl|wget|ssh` call (grep over the
  whole script returns no match) and no shell `source`. E11 (`:560-568`) only
  tests `[ -e "$dir/$path" ]` for each `used-by` path.
- Verdict: file reads + stdout. Note it is **working-tree-bound**, not
  revision-bound: run it only on the intended integration tree.

Adjacent (not one of the five): the new `.ufo/waves/round-17/measure.py`
(untracked at review, SHA-256 `7e37b6bc95614b4522f56db7e85bb51d58e8d87939fd5cf46d8e68612b4d858b`)
also uses only `git show`/`ls-tree`; I read its source and found no
`open(..., "w")`, `os.system` or network imports. `tools/mado-tripwire.py`
was **absent** at review, so C3's selftest surface cannot be inspected yet.

## 3. Findings (severity order)

### F1 — medium (evidence labeling): the round-16 closure cites a jq key the probe never emits

`corpus/lessons/round-16-verifier-spotcheck.md:53-54` states:

```text
$ python3 .ufo/waves/round-16/measure.py 32c4fda… | jq .c1.count,.c1.score → 6, 8.5714
$ python3 .ufo/waves/round-16/measure.py 4bfb236… | jq .c1.count,.c1.score → 7, 10.0
```

The only committed revision of that probe (`9dcf248`, SHA-256
`ea3db43fdc75634b02c3fd4f1bc7aa1e54700b2e2d1ae2261e4b78ec1782c73c`,
identical at HEAD) emits a **`coverage`** object, not `c1`. Its recorded
receipts confirm this: `.ufo/waves/round-16/evidence/before.json` stdout has
top-level keys `revision, revision_sha, measure_inputs, source_registry,
coverage, navigation, safety_artifacts, calibration` and
`coverage.count = 6`, `coverage.score = 8.5714`; `after-final.json` has
`coverage.count = 7`, `coverage.score = 10.0`. The cited command as written
prints `null`, `null` (jq exit 0). The **numbers and the coverage verdict are
correct**; only the cited path is wrong. This is the same defect class as
R16-V1 (doc cites a receipt for a token it does not carry) but in a different
document and field. Recommended: append-only correction in the next lesson/
erratum; do not rewrite the closure or this receipt.

### F2 — medium (harm-watch trap): “U 7/7” must be read from `coverage.count`, not the exit code

`measure.py` exits 0 even when coverage is low (`:436`); the harm-watch line
`SCORECARD.md:864` says only “U 7/7 … via .ufo/waves/round-16/measure.py”.
If L1 copies the closure's `.c1.*` path (F1), the check prints `null` and
silently “passes”. The check must assert
`coverage.count == 7` / `coverage.score == 10.0` / `coverage.items ==
["U1"…"U7"]`, plus `navigation.notes == navigation.indexed` at the content
revision. Do not use process exit as the signal.

### F3 — low (wrong revision): the published navigation counter defaults to the fleet-round-1 baseline

The fence is `${REV:-bb08dd57f4b48bfb001a178e57b9c25e7040447f}`. A bare run
therefore measures the fleet-round-1 baseline (`indexed=8/22`, missing 14,
exit 1), not the round — a red result for the wrong revision that invites the
wrong diagnosis. The round invocation must export `REV` (`27cd06f` at
baseline, the integration commit afterwards). The fence body's SHA-256
matches the recorded corrected wrapper (verified, §1 HW4), so this is a usage
trap, not a script drift.

### F4 — low (integration invariant): the two new notes must be indexed once each

The counter requires every `corpus/knowledge/*.md` note to appear exactly
once as a ``| `knowledge/<file>` `` row in `corpus/README.md`. The round's C2
probe (`.ufo/waves/round-17/measure.py`) does **not** require that, so C2 can
read 4/6 while navigation exits 1 (or vice versa). Also keep the P-notes free
of a new `covers: U<N>` line: the round-16 probe admits a U item only when a
note carries exactly one `covers: U1..U7`, so an accidental extra `covers:`
line would disturb the U-side census the harm watch is protecting.

### F5 — informational: the 372/52 counts are receipt-based and byte-conditional

`fba82a66…` (gate) and `226220ae…` (classifier) are unchanged at `27cd06f`
and at HEAD, so the recorded counts (372/372 at `9dcf248`; 52/52 at
`1e31681`) are the correct expectations. Any edit to either file in this
round invalidates the number even if the suite still passes; re-measure after
integration. The counts are host-dependent (python3/coreutils present); this
host's recorded value is the one the round claims.

### F6 — informational / verification gap: C3's new tool is absent at review

`tools/mado-tripwire.py` does not exist yet; its selftest expected tally
cannot be checked. It is not one of the five harm-watch commands. Its item
(`TripwireCore`) binds it to stdlib-only reading of given JSONL paths and
`/tmp` fixtures; the OMP red anchor is read-only by the named seats
(`OracleR15`, `IncidentTimeline`). No action for this report beyond noting
the gap.

### F7 — informational (maintenance risk): HW1 hermeticity is enforced per case, not globally

The gate's live plane would read the compositor if reached with an ambient
PATH. The selftest reaches it only in `MADO_VERIFY_LIVE=yes` cases and only
with a staged PATH that lacks `hyprctl`. A future edit adding a live-requested
case without that staging would turn `--selftest` into a live probe. Keep the
“every live-requested sub-invocation sets `PATH=`” rule; today the property
holds at `:685-686, :736-737, :748-749, :765-766, :776-777, :783-785,
:793-794, :993-994, :1433`.

### F8 — informational: census `validate` cannot prove the row delta

HW5's four lines are the whole verdict. The 55 → N row/tier/status movement
must be read from the probe's `source_registry` or the census `census` mode;
`validate` only emits E/W codes. New rows must also pass E04 (no duplicate
URL+scope without `supersedes`), E08 (opened not future; 2026-10-20 is
accepted), E09 (valid recheck) and E11 (every mined `used-by` path exists
on disk, as `corpus/knowledge/<entry>.md`). Same URL in another scope is only
W04 and keeps exit 0.

## 4. Residual risk and verification gaps

- **No command was executed here.** All five expected outputs are receipt-
  and byte-based; L1's single post-integration run is the confirming
  measurement. This report cannot detect a runtime failure that differs from
  the recorded receipts.
- Host package/service state is not observed or cleared: the R15-V1 pause
  remains binding, and none of these commands queries it (`pacman -Q` is
  still prohibited; HW5 reads only `SOURCES.md` text and file existence).
- `measure.py` counts only committed bytes for HW3 but the census is
  working-tree-bound for HW5; run HW5 after the integration content is on
  disk, and record the exact stdout.
- The gate/classifier counts remain valid only while their digests do. No
  wave item at review time edits either file; confirm after integration.
- U-coverage and navigation are separate invariants with separate commands;
  C2's rubric-V probe does not substitute for either.
- The `census`/navigation commands are read-only but `git` reads must be
  pinned by `REV`; a default run measures the wrong commit (F3).

## 5. Digests and anchors used

| Object | Value |
|---|---|
| HEAD / baseline | `0175f13d83dceb9344fd0ecc5f94aa4aac5dfb53` |
| `tools/mado-verify.sh` | `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` (working tree, `27cd06f`, HEAD) |
| `tools/mado-action-plan.py` | `226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3` (working tree, `27cd06f`, HEAD) |
| `.ufo/waves/round-16/measure.py` | `ea3db43fdc75634b02c3fd4f1bc7aa1e54700b2e2d1ae2261e4b78ec1782c73c` (`9dcf248` = HEAD) |
| Published navigation fence | `SCORECARD.md:69-90` (body `:70-89`), body 1,063 B / 20 lines, SHA-256 `8b59b503…` (recomputed) |
| `.ufo/waves/round-17/measure.py` | `7e37b6bc95614b4522f56db7e85bb51d58e8d87939fd5cf46d8e68612b4d858b` (untracked at review) |
| `tools/mado-tripwire.py` | absent at review |
| Census baseline receipt | `.ufo/waves/round-17/evidence/census-start.txt`, 2026-10-20T10:56:14-03:00 |
| Classifier green receipt | `.ufo/waves/round-16/evidence/action-selftest-final.json` (52/52, exit 0) |
| Gate green receipt | `.ufo/waves/round-16/evidence/legacy-selftest.json` (372/372, exit 0) |
| U / navigation receipt | `.ufo/waves/round-16/evidence/after-final.json` (`coverage` 7/10.0, navigation 30/30) |
| Closure mis-citation | `corpus/lessons/round-16-verifier-spotcheck.md:53-54` (`.c1.*`; tool emits `coverage.*`) |

**Verdict for the assignment:** all five harm-watch commands are host-safe
(file reads, git object reads, and `/tmp`-only fixture scratch; no
hyprctl/pacman/systemctl/service/input calls), with the exact expectations
above. Two reporting defects need L1 attention before the harm-watch run:
F1 (closure jq path) and F2 (measure the `coverage` field, not the exit
code); F3 (export `REV`) and F4 (index the new notes once) are the other
ways this harm watch can silently misreport.
