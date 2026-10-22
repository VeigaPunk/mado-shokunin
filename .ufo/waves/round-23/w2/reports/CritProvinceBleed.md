# CritProvinceBleed — wave 2 attack on C3 (PROVINCE refinement at `2f1134f3`)

Seat: `MadoR23.CritProvinceBleed` (critic, leaf). Landed tip under attack:
`2f1134f38930fc8b067d2d7f5bba126338faabdd` (lane `master` resolves to the same commit).
Axis judged: calibration. Advice and evidence only. I edited no lane file other than this report.

**Verdict: the counter value holds, but PROVINCE.md is still not accurate.** C3's after-value of
**0** re-derives exactly, and the refinement takes over no sibling's ground and opens no write
surface. But the claim that SHONEN box 4 ("PROVINCE.md still accurate") now matches the repo is
**falsified at the landed tip**:

- One of the five new rows is materially inaccurate.
- One owner cell overclaims what the tool does for secrets.
- The section heading certifies "no cross-domain bleed" by itself, on a read surface it shares with
  mori.

The counter cannot see any of these, because it counts tool names and never checks what a row
says. These are defects that an append-only correction can fix. They are not a reason to reject the
round. However, the judge should not read 5→0 as evidence that box 4 is now calibrated.

## 1. What I did (commands and outputs)

All lane reads used read-only `git show` and `git ls-tree` on committed bytes, copied into `/tmp/cpb/`.

1. **Re-ran the counter of record** (`python3 -I .ufo/waves/round-23/c3/count.py REV`; script
   sha256 `4828d7b8…`, last changed at `4de4464`):
   - base `e33ea304` gave `count 5` (`mado-action-plan.py`, `mado-assessment.py`,
     `mado-evidence-audit.py`, `mado-tripwire.py`, `mado-verify.sh`), exit 1.
   - tip `2f1134f3` gave `count 0` with an empty mismatch list, exit 0.

   This matches `evidence/c3-before-v2-e33ea304.json` and `evidence/c3-after-2f1134f3.json`.
2. **Checked the commit shape.** `git show --stat 2f1134f3` shows `PROVINCE.md | 10 ++++++++++`
   (10 insertions, 0 deletions), so the change is append-only and doc-only. SHONEN.md, SCORECARD.md
   and SKILL.md are untouched between `2e592af` and `2f1134f3`. The tripwire at the tip has
   sha256 `41489991…`, matching C1.
3. **Read the sibling provinces in full:** `mori-shokunin`, `tsukuroi-shokunin`,
   `tameshi-shokunin` and `kagi-shokunin` `PROVINCE.md`. I also searched the mori, tsukuroi, kagi,
   tameshi and kumitate lanes for `mado-tripwire` (no hit) and for mado in the mori and kagi
   provinces (no hit).
4. **Statically audited every tool against its new row.**
   - For the Python tools I searched for every write, temporary-file, filesystem-change and
     subprocess call.
   - For `mado-verify.sh` I enumerated every external command the live code path runs, every
     `mktemp` and `/tmp` site, and the `--regression` call into tameshi's harness.
   - In tameshi's `mutate-and-run.sh` I checked every place it writes.
5. **Tested the counter with three synthetic repos** in `/tmp/cpb/synth`. Each repo holds a
   byte-copy of `count.py` at the same relative depth, the tip `SHONEN.md`, and a fixture
   `tools/writer.sh`. That fixture is text only and was never executed.
6. **Tested the tripwire's redaction regexes** in a standalone `python3 -I` script. It holds a
   byte-copy of `SECRET_PATTERNS`/`redact()` from `tools/mado-tripwire.py:301-327`. The
   classifier itself was not run.
7. **Read-only host probes:** `ls ~/.omp/agent/sessions | wc -l` returned `45`. I also read
   `~/.local/share/omarchy/bin/omarchy-theme-current`.

No tool was installed or updated.

## 2. Does the refinement absorb another lane's ground? No absorption, but two unrouted overlaps

The refinement adds nothing to **Owns**. It frames the five tools as "lane-internal instruments"
and names an adjacent owner on each row. Checked lane by lane:

### tameshi (mutation testing): clean

`tameshi PROVINCE.md:29-38` lists mado `tools/mado-verify.sh` as a measured primary surface of
tameshi's method. `mado-verify.sh:2245-2251,2150-2151` runs tameshi's harness with
`--workdir "$cwd/sweep"` inside `mktemp -d /tmp/mado-verify-regression.XXXXXX`.

The harness writes only inside that workdir (`mutate-and-run.sh:479-552`) and never modifies its
target; it copies the target into the workdir first. The sha is printed as provenance and is not
gated. The row's claim holds.

One wording point: "consumed read-only" really means "executed, bytes unmodified". The harness is
`bash`-executed and runs the mutants' `--selftest`. That is not a bleed.

### kagi (secrets): no absorption, but an overclaim

`kagi PROVINCE.md:67` already treats each lane's "own secret-shaped tripwires over their outputs"
as hygiene filters rather than vault operations. A redaction filter in the tripwire is therefore
not kagi ground.

The overclaim is in the refinement's wording. It says the tripwire "redacts secret-shaped
substrings … instead of reporting their content", and the row's owner cell says "secret-shaped
substrings are redacted, not reported". The code redacts exactly three fixed patterns: URL
userinfo, `AKIA` plus 16 characters, and runs of 32 or more `[A-Za-z0-9_-]`. Output of the
standalone copy:

```
aws_secret_with_slashes -> AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY aws s3 ls
short_password_flag -> sshpass -p 'Tr0ub4dor&3' ssh host
mysql_inline -> mysql -uroot -pS3cr3tPassw0rd2026 -e 'select 1'
bearer_jwt_dots -> curl -H 'Authorization: Bearer eyJhbGciOi.eyJzdWIiOiIx.SflKxwRJSMeKKF2QT4' https://x
ghp_token -> GH_TOKEN=<redacted> gh pr list
url_userinfo -> git clone https://<redacted>@example.com/r.git
```

Four of the six common secret shapes reach stdout as content. This also cuts against mado's own
Refuses line, `PROVINCE.md:14`: "secrets in configs (shape-only, → kagi)". The output behaviour
predates this round; the inaccurate description of it is new at `2f1134f3`.

### mori (transcript observation): a shared read surface the refinement does not name

Mori's Core includes "passive terminal-at-scan transcript observation (`tools/mori-seat-terminal.py`)
… Version-3 regular transcript files" (`mori PROVINCE.md:103-107`). The mado tripwire reads the
same bytes, OMP session `.jsonl`.

The refinement says "transcript observation stays with mori" while documenting a mado tool whose
whole input is transcript observation. The two lanes take different views of the same bytes: mori
tallies status, the tripwire classifies issued commands. That is a shared surface, and
`AXES.md:17` (adjacency) says such scope should be named as contested so the integrator can
arbitrate. Instead the section heading self-certifies "no cross-domain bleed". No mori file
mentions mado's tripwire.

The "lane-local only" boundary is usage policy, not something the tool enforces:

- `refuse_path()` (`mado-tripwire.py:2995-3009`) refuses only `~/.omp/agent` outside `sessions/`.
- `discover()` walks any directory it is given (`:3012-3039`).
- So `--scan ~/.omp/agent/sessions` would scan every session directory on the host (45 at probe
  time). That would include sibling seats.

I found no evidence that this has happened. Every tracked `.jsonl` (2889 files) uses a mado or
fixture name, none uses a sibling-lane name, and `LOG.md:1273-1278` scans mado's own seats only.
The rows should still say that the scope is unenforced.

### tsukuroi (package and unit state): a real overlap the row hides

`tsukuroi PROVINCE.md:8-10` owns "systemd user units & timers (`systemctl --user` …)". ADJ-03
(`:48`) says tsukuroi retains "User-manager/unit … health; an active unit does not prove the UI
works".

`tools/mado-verify.sh:3380-3391` runs `systemctl --user is-active app-walker@autostart.service`
and `elephant.service`, and turns the result into a verdict row, `live.walker.services PASS|FAIL`.
That is a unit-health verdict.

The C3 row for `mado-verify.sh` omits this read and names only tameshi as adjacent. Meanwhile the
rows for `mado-action-plan.py` and `mado-tripwire.py`, which never read package or unit state,
name tsukuroi. The adjacency cells sit on the wrong tools.

## 3. Does it open a write surface? No

Every write site I found matches its row:

- **`mado-action-plan.py`:** writes only in `--selftest`, inside
  `tempfile.TemporaryDirectory(prefix="mado-plan-selftest-")` (`:702-763`, including the FIFO and
  symlink fixtures). It runs a copy of itself as a child.
- **`mado-tripwire.py`, `mado-assessment.py`, `mado-evidence-audit.py`:** no write or `mkdir`
  calls, and no `open` in a write mode. The only subprocess in each is a `sys.executable -I`
  self-invocation (`tripwire:3545-3556`, `assessment:194-195`, `audit:244`).
- **`mado-verify.sh`:** the only `mktemp` sites are `/tmp/w5-mado-m52-selftest.XXXXXX` (`:418`)
  and `/tmp/mado-verify-regression.XXXXXX` (`:2251`). No config bytes are written. The `hyprctl`
  verbs in live code are exactly version, instances, configerrors, getoption, binds, monitors and
  layers, as the row says.

The commit itself changes documentation only.

## 4. Is PROVINCE.md accurate at the tip? No

These defects survive a counter value of 0. Each was observed in committed bytes.

1. **The `mado-verify.sh` row misstates what the tool reads.** The row says the tool reads "the
   file bytes of the declared config planes … and `hyprctl` read verbs only". Its live code path
   also runs the following:

   | Command | Location |
   |---|---|
   | `systemctl --user is-active …` (tsukuroi-owned unit state) | `:3384-3385` |
   | `busctl --user get-property fr.arouillard.waybar /StatusNotifierWatcher …` (D-Bus) | `:3624` |
   | `pgrep -x hypridle` and `pgrep -x waybar` (process table) | `:3545`, `:3587` |
   | `walker --version` and `waybar --version` | `:3373`, `:3576` |
   | `omarchy version`, `omarchy theme current`, `omarchy commands --json --all` | `:3781`, `:3642`/`:3945`, `:3905` |
   | `git -C <omarchy checkout>` with rev-parse, symbolic-ref, for-each-ref, describe and show | `:3774-3886` |

   All of these are reads. `omarchy-theme-current` just prints `theme.name` through `sed`. They are
   still not the reads the row declares.
2. **The kagi cell overclaims redaction** (section 2 above).
3. **The mori overlap is self-certified instead of named** (section 2 above).
4. **The heading uses a universal clause.** It says "the province accounts for every tracked tool
   it runs". The counter enumerates only `tools/**`. The lane also tracks 130 `.py`/`.sh` files
   outside `tools/` (`git ls-tree -r $R | grep -E '\.(py|sh)$' | grep -v ^tools/ | grep -v
   /snapshot/ | wc -l` gave `130`), including measurement harnesses it runs, such as
   `.ufo/waves/round-2*/*/measure.py` and `round-22/replay.py`. `lane-addendum.md:205-206`
   forbids universal clauses unless the counting command enumerates the full set.
5. **The new rows contradict mado's own Refuses line.** `PROVINCE.md:16` still says "every claim is
   file-byte- or screenshot-verified". The rows now document live `hyprctl` IPC queries, and the
   real tool adds D-Bus, process-table and unit-state probes. Neither is file bytes or a
   screenshot, and the refinement does not reconcile this.

## 5. Does C3's counter measure what the hyaku calibration rule requires? Only in letter

The rule (`scripts/hyaku/lane-addendum.md:207-208`): "A calibration claim must count mismatches
between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state. It cannot be an
assertion."

**It passes in letter.** It is a command, not an assertion. It is gated on box 4 being asserted
(`[~]`/`[x]`; exit 2 when unticked or absent). One side is genuinely observed repo state: the
tracked `tools/**` list from `git ls-tree`. It re-derives from committed bytes.

**It fails in substance.** Box 4 is two promises (`PROTOCOL.md:72-73`): it "bars cross-domain
bleed and keeps `PROVINCE.md` accurate". The counter tests neither. It tests one necessary
condition: does a backticked four-cell table row exist for each tool path? The synthetic runs show
it is blind to content:

| Synthetic case (tool text: writes `~/.config/hypr/hyprland.conf`, runs `sudo pacman -Syu`) | count |
|---|---|
| A: the only row sits inside a ```` ``` ```` fence, cells `x \| y \| z` | `0`, accounted `['tools/writer.sh']` |
| B: the row says "writes nothing — no file is created or modified" | `0` |
| C: the tool is deleted and its stale row kept | `0`, tracked `[]`, accounted `['tools/writer.sh']` |

The counter has three blind spots:

- It never compares a row's claims to the tool's behaviour, so case B and the real `mado-verify.sh`
  row both pass.
- It counts only in one direction: a stale row is never a mismatch (case C).
- It ignores Markdown context: fenced or refused-section rows count (case A).

The "observed" side is just the file list, and everything the self-assessment actually claims
lives in rows that the same edit writes. So the target is reached by editing the document the
counter reads, and the result says nothing about whether the province is accurate.

**Axis-identity risk.** What the counter measures is literally the coverage signal in `AXES.md:13`,
"PROVINCE.md lists every surface". Registration finding 5 asserts that C3 is not coverage, but
the measured quantity matches the coverage definition more closely than the calibration one.
`AXES.md:23-24` says two claims on one axis count as one. The judge should decide whether C3 and
C2 (coverage) are on distinct axes.

## 6. Defects versus tradeoffs

- **Fixable defects.** Sections 4.1 to 4.5 can be corrected by an append-only paragraph in
  PROVINCE.md without touching tools or targets.
- **Construct-validity limit.** The counter's blindness to row content is not fixable this round:
  under the no-narrowing rule the counter cannot change after landing. The judge should credit C3
  as "the inventory gap closed, 5→0, measured". It should not credit "box 4 now matches observed
  state", because the defects in section 4 contradict that.
- **No bleed or write-surface rejection.** Nothing in C3 absorbs a sibling's Owns or creates a
  write path.

**Impacted axes:**

- Calibration (primary): new overclaims were added to the very file the claim certifies.
- Adjacency: the mori surface is unrouted, and tsukuroi's unit state is hidden in the
  `mado-verify.sh` row.
- Coverage: axis-identity risk with C2.

## 7. Smallest safe correction

The L1 decides whether to land this. It is an append-only "Round-23 correction" paragraph in
`PROVINCE.md`, with no tool change and no counter change:

1. **Fix the `mado-verify.sh` row.** Add the live reads to its Reads cell:
   - `systemctl --user is-active` on `app-walker@autostart.service` and `elephant.service`;
   - `busctl --user get-property` on the StatusNotifierWatcher;
   - `pgrep -x hypridle` and `pgrep -x waybar`;
   - `walker --version` and `waybar --version`;
   - `omarchy version`, `omarchy theme current`, `omarchy commands --json --all`;
   - read-only `git -C ~/.local/share/omarchy` verbs.

   Add **tsukuroi** to its owner cell: unit health stays tsukuroi's, and mado records unit state
   only as launcher evidence.
2. **Narrow the kagi cell.** State that redaction covers three fixed shapes (URL userinfo, AKIA ids,
   runs of 32 or more `[A-Za-z0-9_-]`) and that other secret values in issued commands can reach
   stdout.
3. **Name the mori overlap.** OMP session JSONL is a read surface shared with mori
   (`mori-seat-terminal.py`). The tripwire accepts any path under `~/.omp/agent/sessions`, so
   lane-local scope is usage policy, not enforcement. Mark it contested for integrator
   arbitration, and drop the "no cross-domain bleed" self-certification from the heading.
4. **Tighten the heading wording.** Change "every tracked tool it runs" to "every tracked file under
   `tools/`".
5. **Reconcile the Refuses line** (`PROVINCE.md:16`, "file-byte- or screenshot-verified") with
   the live IPC, D-Bus, process and unit probes that are now documented.

For a future round, re-registered rather than changed now: make the counter two-directional (stale
rows count), skip fenced blocks, and add one behavioural check per row. For example, the set of
executables a tool spawns must be a subset of the executables named in its Reads cell.

**Scratch:** `/tmp/cpb/` held the extracted bytes and the synthetic repo; I removed it after
writing this report. I wrote nothing in the lane except this report.
