# SourceTrust — data-trust and prompt-injection audit (round 15, w1)

Seat: MadoR15.SourceTrust (sentinel, leaf). Date: 2026-10-20. Axis: coverage.

**Scope:** the trust boundary that upstream docs (S007 / libinput tools, man pages) and archived receipts (R14 evidence,
the R14 outside spot-check) cross on their way into the U6 draft and the R14-V1 correction. The question each finding
answers: does any of this content become an instruction or executable input, rather than quoted data?

**Lane revision:** `ea0446fcb4840089f0e541d96350144506fb5d1d` (HEAD). The worktree also holds staged round-15 spec,
dispatch and census files and an unstaged `SCORECARD.md` that belong to L1. They were not touched.

**Executor outputs:** `input-draft.txt`, `receipt-correction.json` and `round-15/measure.py` had not landed when this
seat read the tree. Those outputs get conditions (§3), not verdicts.

## 1. Findings (most severe first)

### T1 HIGH — the input stack was partially upgraded in the middle of the round, and the install record has no owner

- **Evidence `[OBS]`:**
  - `/var/log/pacman.log:2287-2288` — `[2026-10-18T14:11:00-0300] Running 'pacman -Sy --noconfirm'` synced the package
    database without upgrading.
  - `:2256` — the last full upgrade was 2026-10-16.
  - `:2429-2436` — `[2026-10-20T04:25:16-0300] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`, then
    `upgraded libinput (1.31.3-1 -> 1.32.0-1)` and `installed libinput-tools (1.32.0-1)`.
  - The round-15 dispatch files are timestamped 04:24.
  - `pacman -Qu | wc -l` = **413** pending upgrades, including `hyprland 0.56.2-2 -> 0.56.2-4`,
    `aquamarine 0.15.0-2 -> 0.15.1-1` and `linux 7.2.3 -> 7.2.11`.
  - `pacman -Qo /usr/bin/libinput` gives `libinput-tools 1.32.0-1`.
- **What this means:** a library that the running compositor depends on was moved forward against a database two days
  newer than the rest of the system. This is a partial upgrade in effect, even though the command was `-S` and not
  `-Sy`. The operator rule forbids partial upgrades, and no update-safety-gate record exists.
- **Second effect — new capability:** the same transaction put the `record`, `replay`, `debug-events` and `--grab`
  binaries on the host. Those are exactly the capabilities this round forbids (§T2). No assigned output needs them;
  every authorized use is reading docs or help text.
- **No owner on record:** no landed round-15 report records the install with tool, version, channel and reason.
  ReviewDocsEra F1 and FrontierRecord §4.6 observed it from outside. Seats that read the host before 04:25 have archived
  claims that are now stale:
  - ReviewLibinput :26-27,97 and ReviewQuotes :20-21 say "not installed" / `1.31.3-1`.
  - ReviewSourceTier :25 and DocsVersion :4-6 say `1.31.3-1`.
- **Impact:**
  - Any U6 sentence that names "the installed libinput" is ambiguous between the two versions.
  - ReviewDocsEra F2 reports that the running compositor still maps the deleted 1.31.3 library.
  - A follow-on seat could take "the tools are now installed" as permission to run them.
- **Smallest remediation (L1):**
  1. Name the acting seat, or record the actor as `[UNK]`.
  2. Record the install line in the round report, including that it was not a full upgrade.
  3. Treat every "installed version" statement in a report as time-scoped: `<value> — <command> <time>` (QUALITY 10).
  4. Do not remove the package. That is an operator decision under the update-safety gate.

### T2 HIGH — upstream docs address the reader with directives the lane must never follow; the lane's fence does not name them

The pinned primary source for these quotes is `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`:
- sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`
- tag `1.32.0`, peeled `5cf833b572f5a33663888da321dce0ba1abd82a2`

**Upstream imperatives, each tagged `[INF-docs]` and each rejected as an instruction here:**

| rst line | Directive (quoted) | What following it would do here |
|---|---|---|
| :31 | "Most of the tools must be run as root" | the `sudo` path (root plus reading `/dev/input/event*`) |
| :146 | "When submitting a bug report, always use the ``--verbose`` flag" | verbose kernel event capture |
| :261 | "Reproduce the bug, ctrl+c and attach the output file to a bug report." | record keystrokes, then exfiltrate them off-host |
| :281 | "Users are advised to always replay a recorded event sequence" | :276 "creates a new virtual device" — uinput **injection** |
| :322 / :326 | "Attach the **last recording**" / "**second-to-last recording**" | exfiltration via autorestart |

**The upstream privacy assurance is narrower than it reads `[OBS]`:**
- tools.rst :262 says "obscures key codes by default, any alphanumeric key shows up as letter 'a'".
- The installed `libinput-record(1)` (1.32.0, read with `man -P cat`) is narrower:
  - "By default, common keys are obfuscated".
  - `--show-keycodes` turns obfuscation off.
  - `--with-hidraw` says "DO NOT TYPE SENSITIVE DATA", and "HID reports are not obfuscated and a sufficiently motivated
    person could recover the key strokes".
  - `--grab` "will prevent events from being delivered to the host system", which disrupts the session.
- `libinput-debug-events(1)` says key events are only "partially obfuscated".
- `libinput-replay(1)`: "needs to run as root to create a device and/or replay events."

**The lane's fence does not name these routes:**
- SKILL.md:225 rule 2 covers "keystroke injection" and dispatchers.
- SKILL.md:234 rule 4 makes session material shape-only, but names no kernel input events.
- QUALITY 16 (`corpus/QUALITY.md:22`) limits upstream docs to dated `[INF-docs]` *claims*.
- None of the three says that a doc's reader-addressed commands are not lane procedure. A sweep of SKILL.md, the
  corpus docs and AGENTS/README/PROVINCE for `untrusted|as data|directive|inject|instruction` found no such rule.
- The nearest pattern is SKILL.md:363-380: the omarchy skill instructs the *editing actor*, and mado only quotes it.

**Exploit path:**
1. InputDraft quotes a `sudo libinput record …` block into the U6 note.
2. L1 admits the note.
3. A later seat treats `SKILL.md` and knowledge notes as "instructions executable by an agent" (SHONEN.md:8). Under the
   tooling directive it then runs the doc's procedure, because the binary is now present (T1).

Result: root keystroke capture, an off-host "attach", or a uinput virtual device on the operator's live seat.

**Smallest remediation, inside the U6 note (no new tooling, no new criterion):**
- Wrap every quoted libinput command in `[INF-docs 1.32.0]` with a "documented upstream route — not authorized in this
  lane" marker.
- Name `record`, `replay`, `debug-events`, `debug-gui`, `measure`, `--grab`, `--show-keycodes` and `--with-hidraw`
  under `[UNK]` / operator-only.
- Reuse the omarchy phrasing: "upstream instructs the bug reporter; mado quotes."
- The note's `recheck:` line may only reopen pinned bytes (sha256) and installed `man`/`--help`/`--version`. It never
  runs a subcommand.

### T3 MED — archived receipts embed shell that would run sibling code if anyone replayed them

**Evidence `[OBS]`:**
- `round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt:1` each read
  `command: bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh … --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-r14-recut-0blumi29/…`.
- The `/tmp` workdirs no longer exist.
- The harness runs the suite as `bash -c "$SUITE"` (`frozen/harness.sh:51,185,395`).
- The live gate's `--regression` mode runs the sibling harness from `$MADO_VERIFY_HARNESS` or a path derived from its
  own location (`tools/mado-verify.sh:1854-1859`). Its sha is printed as "provenance, not gated" (`:1597-1600,1866-1867`).

**Today the harness matches the record:** its current sha256 is
`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, the same value as each receipt's `MUTATE_TOOL`
line (last commit `606716f`, 2026-10-14). But nothing enforces that match.

**Contrast:** `frozen/verify.py:79-109` hashes `gate.sh` and `harness.sh` against `expected.json` and refuses with
`snapshot_tampered` *before* it runs `subprocess.run` (`:113`). That is the lane's safe replay pattern.

**Exploit path:** ReceiptCorrection or a later auditor "re-derives" R14-V1 by pasting a `command:` line.

Result:
- It runs whatever the sibling repo holds at that time, with a caller-controlled `bash -c` suite.
- It also violates the round contract (no tests, gates or live runs).

**Remediation for this round:** do not replay. The correction maps headers using only `git show <sha>:<path> | sha256sum`
and the recorded `MUTATE_TARGET`, GREEN and restore lines. If a future replay is ever authorized, it goes through
`frozen/verify.py`, never through the `command:` line.

### T4 MED — the outside R14-V1 request is a directive; adopt it only through the lane's own append-only rules

**Source:** `corpus/lessons/round-14-verifier-spotcheck.md:169`, author hyaku, a non-author integrator. Its directive:
"Append an explanatory correction mapping each provisional header to its committed derived target; keep historical
bytes, and bind future standalone mutation receipts directly. Route is status-neutral; admission does not require
rewriting these records."

- **Legitimate channel:** the request arrives as a routed defect in a committed lesson, and the round context classifies
  it as an unscored, lesson-backed correction. So it is admissible as a request.
- **What it does not authorize:**
  - rewriting receipts;
  - a score move;
  - new generic tooling (QUALITY:57-61 records that a generic wrapper was rejected).

**Baseline for the no-mutation check (`[OBS]`):** `git diff --quiet HEAD -- <three receipts>` returned rc 0. The HEAD
blob digests are:

| Receipt | sha256 at HEAD |
|---|---|
| `regression-recut.txt` | `d54626345fa0a37efc4ad1f58cc51520a4e8bd5922d717128f4d5cd19199b75b` |
| `regular-target-mutants.txt` | `267de2b54b41a7575716d56fcf4433f44d92b6d2f53b8c05e46d701c4762745f` |
| `retained-census-mutants.txt` | `57c462c29984d0e878c4c986ca205bee73dd6e3119b802915be31e5f4b549d81` |

Headers checked `[OBS]`:
- Line 3 of each is `input_binding: provisional worktree snapshot`.
- Line 4 is `gate_sha256: ef50e262…` in `regression-recut.txt`, and `d6d5eb27…` in the other two.
- `MUTATE_TARGET` is `cd1d73d7…` in all three, the same value as `tools/mado-verify.sh:1639` `PIN_MADO`.

### T5 MED — the docs anchor is a moving URL, and the versioned HTML URL does not exist

- **Moving page:** S007 (`corpus/SOURCES.md:19`) cites `…/libinput/doc/latest/tools.html`.
  - It returned HTTP 200 on 2026-10-20, with sha256 `524c177681d1eb0be28424e54d1c346c6de993e1b9c4e98c8ec409a849d6872f`
    and title "libinput 1.32.0 documentation".
  - Those bytes can change under the row without notice.
- **Versioned HTML is not served:** `…/doc/1.32.0/tools.html` returned **HTTP 404** (curl rc 22).
  - Spec items LibinputTools, LibinputList, LibinputEvents and LibinputRecord all say "official libinput 1.32.0 …".
  - A seat that cites `latest` as "1.32.0" therefore binds a page title, not bytes.
- **Immutable anchor:** the tag-raw rst listed in T2, `53264328…`. It contains the same three marker phrases checked in
  `latest`: root, attach, obscures.
- This agrees with ReviewDocsEra F3/F4, ReviewSafety F1 and ReviewCensus F5.
- **Remediation:** any S051 row cites the tag-raw URL with its sha256, and opens `teaches` with `supersedes S007 —`
  (QUALITY 17). S007's cells stay unchanged.

### T6 LOW — two seats made live reads that the round contract does not allow

- ReviewLibinput ran `hyprctl version` (its :98).
- ReviewDocsEra read `/proc/1706/maps` and ran `pgrep` (its :20-21,76).

Neither read is a mutation, and SKILL rule 4 bans `/proc/*/environ`, not `maps`. But the wave context says "no … live
probes". Their outputs are archived as evidence.

**Remediation:** L1 labels these observations as out-of-contract `[OBS]`, and does not cite them as a sanctioned
recipe. In particular, no recheck line should include `/proc/<pid>/maps`.

### T7 LOW — gitignored session transcripts contain text shaped like system messages

`.ufo/interactive-sessions/**/*.jsonl` (gitignored, `.gitignore:1`) contains `<system-notice>` and `<advisory …>`
envelopes from an earlier agent session (for example `…/20261015T050057Z/…jsonl:149-150`). A seat that greps `.ufo/`
with ignore rules off ingests this text, which looks authoritative.

Revision-bound readers are not exposed: `measure.py` uses `git show`, so it never sees these files.

**Remediation:** source and evidence sweeps exclude `.ufo/interactive-sessions/`, and treat any hit there as untrusted
data.

### T8 INFO — boundaries that hold

- **considerthese:** `considerthese/2026-10-19.md:32` labels its items "proposals only; not acted on".
- **round-14 `measure.py`** (`:30-33,52-60`):
  - It resolves the revision before reading anything, and reads every input with `git show`.
  - It parses `SOURCES.md` as cells (`:96-99`, guarded by `len(cells)==13`).
  - It runs only lane-committed gate bytes from that revision, with `--root <fixture> --no-live`.
- **Injection markers:** a sweep of the lane for `ignore (all|previous)`, `system prompt`, `disregard` and
  `curl … | sh` found no injected directive in committed corpus or receipt content. The hits were:
  - `curl | sha256sum` digest recipes;
  - a `disregarded` inside a governance quote (ProtocolPhases.md:136);
  - T7's transcripts.
- **Tooling directive:** the canonical spec context (`round-15/w1/spec.json:3`) only says "Tooling authorization … read
  /home/vgpnk/.omp/agent/RULES.md first". The longer "passwordless sudo" text appears in neither `spec.json` nor
  `dispatch.json`; `grep -c 'Tooling directive'` returned 0 for both. It reaches seats through the harness's system
  rules.

## 2. Zero-mutation check for the R14-V1 correction (adversarial)

A correction that rejects or refuses something must leave every protected byte unchanged. Accept the correction only if
all of these hold:

1. **Receipts untouched:** after the landing commit, each of the three receipts still hashes to the T4 digests at the new
   HEAD, and `git diff --quiet ea0446f HEAD -- <three receipts>` returns rc 0.
2. **Other protected files untouched:** the diff across `corpus/lessons/round-14*.md`, `tools/mado-verify.sh` and
   `.ufo/waves/round-14/frozen/*` is empty.
3. **Location:** the correction lives only in `.ufo/waves/round-15/receipt-correction.json` and in L1's append-only
   SCORECARD/LOG/lesson tail.
4. **Derivation:** the correction's mapping comes from `git show`, using the recorded header hash and `cd1d73d7…`. Its
   own text does not run, or name for running, any `command:` line or the sibling harness.
5. **Score:** no coverage/operability score field changes because of R14-V1.

## 3. Conditions for executor landings (not yet on disk)

### `input-draft.txt` / U6 note

**Accept only if all hold:**
- (a) Every libinput quote cites the tag-raw rst with its sha256 and line number, or `man <page>` with the version
  `1.32.0-1`. Each quote is ≤25 words.
- (b) The T2 directive lines appear only inside an "upstream instructs the bug reporter; not authorized here" block.
- (c) The privacy text uses the *man* scope ("common keys", "partially obfuscated", "HID reports are not obfuscated"),
  not the tools.rst phrase "any alphanumeric key".
- (d) The installed version is time-scoped per T1. The runtime library is `[UNK]`, or carries the `(deleted)` caveat
  as ReviewDocsEra's out-of-contract `[OBS]` (T6).
- (e) `recheck:` uses static digests and help/man/version only.

**Reject on any of:**
- a runnable `sudo libinput …`, `record`, `replay`, `debug-events` or `--grab` line outside a quoted-and-refused block;
- any claim that recording is privacy-safe;
- `doc/latest` cited as host behavior;
- any instruction to "attach", upload or share.

### `receipt-correction.json`

Accept per §2. Reject if:
- any receipt byte or historical hash value is rewritten in place;
- any field instructs a replay via `mutate-and-run.sh`;
- a new generic wrapper is introduced.

### `round-15/measure.py`

**Accept only if all hold:**
- Inputs are read via `git show <resolved sha>` (same as R14 `:52-60`).
- No `.ufo/interactive-sessions` path is read.
- No path outside the repo is read.
- No libinput or Wayland binary is run.
- If the gate is run, it uses only `--root <fixture> --no-live`.
- A U6 facet check, if added, matches headings and labels as data. It never runs commands quoted in the note.

## 4. Sources opened this seat

**Docs (read-only):**
- Read with the `read` tool: `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (full page).
- Fetched with curl, `set -o pipefail`, to stdout or a `$$` temp file that was removed (absence confirmed):
  - `…/doc/latest/tools.html`
  - `…/doc/1.32.0/tools.html` (404)
  - `gitlab …/raw/1.32.0/doc/user/tools.rst`
  - `git ls-remote … refs/tags/1.32.0*`

**Installed man pages:** `man -P cat`, grep only — `libinput-record`, `libinput-debug-events`, `libinput-replay`,
`libinput-list-devices`.

**Package metadata (read-only):**
- `pacman -Q libinput wayland`, `pacman -Qi libinput`, `pacman -Qo /usr/bin/libinput`
- `pacman -Qu` (local sync DB; no sync performed)
- `/var/log/pacman.log` (grep)

**Lane files:**
- SKILL.md:208-243 and the grep sweeps
- QUALITY.md, AGENTS/PROVINCE/MINT/SHONEN/README, considerthese
- spec.json, the R14 lesson spot-check
- R14 `measure.py`, `frozen/verify.py`
- `tools/mado-verify.sh` (grep)
- the R14 receipts
- landed round-15 reports (grep)
- the sha256 of the sibling harness file, read only

**Not opened:** credentials or auth files, `~/.omp/agent/agent.db*`, `RULES.md` (no install was made).

## 5. Tooling, and what this seat wrote

**Tooling:** nothing was installed or upgraded, and no sync or upgrade was run. No libinput subcommand ran (only `man`).
No Wayland client, hyprctl, gate, test or measure run happened.

**Writes:** this file only.
