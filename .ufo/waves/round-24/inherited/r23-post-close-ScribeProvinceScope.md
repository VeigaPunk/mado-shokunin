# MadoR23.ScribeProvinceScope — C3 append-only PROVINCE refinement naming the four undeclared lane tools

Seat: scribe (advice + evidence only). Lane: `mado-shokunin`, branch `master`.
Base read: `a28e4815aabfa85f55274884000fb2608355f8cf` (the C3 counter's v1 commit). The counter of
record was tightened mid-round to **v2** in lane commit `4de44647f93bfd25ed5c979f61ff016b50456549`
("round-23: tighten C2/C3 counters and record registration clarifications (before any
after-measurement)"), which I used for every measurement below.

Scope: draft the append-only `PROVINCE.md` refinement text for C3, naming
`tools/mado-action-plan.py`, `tools/mado-assessment.py`, `tools/mado-evidence-audit.py` and
`tools/mado-tripwire.py`, each with one plain sentence stating what bytes it reads, what it
outputs, that it writes no host state, and why it is a lane-own safety/evidence instrument rather
than a new desktop surface. **I did not edit `PROVINCE.md`** — the draft text is in this report for
L1 to land. The only file I wrote is this report.

No tools were installed or updated (no pacman / uv / npx / cargo activity); nothing on the host was
changed (read-only probes only — no display, input, compositor, service or `~/.config` change).

## Behavior (what was done)

1. Read `.ufo/waves/round-23/registration.md` (claims C1/C2/C3, counters, guards).
2. Read `PROVINCE.md` in full (20 lines, sha256 `1b25bb1e980925b356663602d002c1c15307a0dfac8bfafd9988bd4d8df7464b`,
   last changed `61eaa07` round-19 wave-2) and the round-19 refinement paragraph that sets the style
   precedent (`git show df84807 -- PROVINCE.md` shows that paragraph was itself appended as a new
   paragraph above the closing `**Out of province → report, never absorb.**` line, leaving lines
   1–16 byte-identical).
3. Read each of the four tools' docstring and CLI (`python3 -I TOOL --help`, read-only), and each
   tool's own source for its write surface (AST walk for write-mode `open`, `os.makedirs`,
   `os.symlink`, `os.mkfifo`, `tempfile.*`, `subprocess` calls).
4. Read each tool's adding round from lane git history (`git log --diff-filter=A -- <path>`).
5. Read the current counter of record `.ufo/waves/round-23/c3/count.py` **v2** and its before receipt
   `evidence/c3-before-v2-e33ea304.json`.
6. Built the draft, then measured it with the **real v2 counter** against a scratch clone — not a
   re-implementation — and confirmed append-only byte preservation by diff.

## Landing status (final, 2026-10-22 — tip `8e5d936`) — **C3 IS met on committed bytes**

**The tip moved twice more after the refinement landed; `PROVINCE.md` did not change with it.**
Current lane HEAD is `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` ("round-23 verifier spot-check
(integrator, hyaku): non-author admit/reject"), after `fa819d5` ("round-23: large raw wave receipts")
and `3df1062` ("round-23: withdraw C1 classifier to base bytes (honest stop), lesson, records, wave
evidence"). `git log --oneline 3732c7a..HEAD -- PROVINCE.md` is **empty** — the refinement has not
been touched since `3732c7a`, so every measurement below still holds at HEAD.

Counter at the current HEAD:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-23/c3/count.py HEAD
```

→ exit **0**, `"counter_version": 2`, `"accounted_rows"` = all five tracked tools,
**`"mismatches": []`, `"count": 0`**. The working tree is clean for `PROVINCE.md`,
`.ufo/waves/round-23/evidence/` and `LOG.md`.

**Round outcome context (outside this thread, recorded because it bears on the round, not on C3).**
`3df1062` withdrew the C1 candidate: the production classifier is restored to base bytes
`cd9da20c…`, and `LOG.md:1569` records "### Round 23 — C1 withdrawn (append-only) … The production
classifier is restored to base bytes `cd9da20c…`; the candidate stays as evidence. C1 is an honest
stop at 6/12." C3 (calibration) is unaffected: it measures PROVINCE coverage of the tracked tools,
not classifier repair.

**L1's item list is down to one optional item: the souji line.** The `LOG.md` entry is committed
(`3df1062`, C3 paragraph at `LOG.md:1561`) and all six after-receipts are tracked
(`git status --porcelain .ufo/waves/round-23/evidence/` empty).

---

## Earlier landing note (superseded by the one above, kept for the record)

### Landing status at `3732c7a` — **C3 IS met on committed bytes**

**The tip has moved since my first landing note.** L1 landed the refinement at `2f1134f3`, then
landed a **wave-2 correction** at `3732c7a73244fab87558c704107418e5de01436c` ("round-23: wave-2
corrections to PROVINCE rows and terminal-trees note (append-only)", `PROVINCE.md` +2 / −0). That
commit adds a "Round-23 wave-2 correction" paragraph at line 30, so the closing line moves from 30
to 32.

**C3 still holds at the new tip.** Measured on committed bytes:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-23/c3/count.py 3732c7a73244fab87558c704107418e5de01436c
```

→ exit **0**, `"counter_version": 2`, `"accounted_rows"` = all five tracked tools,
**`"mismatches": []`, `"count": 0`**. The lane's committed after-receipt
`.ufo/waves/round-23/evidence/c3-after-3732c7a7.json` holds the same JSON.

**The wave-2 correction revises claims my own draft made** (L1's paragraph cites
`CritProvinceBleed` and `CritSeparability`), so my draft rows are no longer the whole truth and the
correction is what governs:

- my `tools/mado-verify.sh` row said its reads were "the file bytes of the declared config planes
  and `hyprctl` read verbs only" — the correction records that it **also runs live read-only
  probes** (`systemctl --user is-active` on the two Walker units, `busctl --user get-property`,
  `pgrep`, `walker --version`, `waybar --version`, three `omarchy` read subcommands, read-only git on
  the omarchy checkout), and that its unit-state rows sit next to tsukuroi's unit-health ground,
  which stays tsukuroi's;
- my `tools/mado-tripwire.py` row said secret-shaped substrings "are redacted, not reported" — the
  correction records that the tool **redacts only its three fixed secret patterns** and that other
  secret shapes can reach its stdout, so secret handling stays kagi's and its output is treated as
  possibly sensitive;
- the correction also states the tripwire's read surface (OMP session files) is **shared with mori's
  transcript observation**, names that overlap for the integrator rather than self-certifying it as
  no bleed, and records that the tool is run on mado's own seats' transcripts **by policy, not by
  enforcement**. My draft's phrasing — "its findings are lane-local evidence about issued commands,
  never a fleet-wide or sibling-lane conduct verdict" — is consistent with that, but L1's phrasing
  is the governing one now.

**L1's wave-2 correction also corrected my paragraph's opening clause**: the inventory "covers every
tracked file under `tools/`, not 'every tracked tool it runs'" — because the lane also tracks scripts
under `.ufo/waves/**` that are round evidence and not inventoried. My draft said "every tracked tool
it runs"; the correction supersedes that wording.

**Original landing note (superseded, kept for the record).** L1 committed the refinement as lane
commit `2f1134f38930fc8b067d2d7f5bba126338faabdd` ("round-23: C3 PROVINCE refinement accounts for
every tracked lane tool"), the only file in that commit being `PROVINCE.md` (+10 / −0).

**After-value at the landed tip** (registration clarification 10 — measured on committed bytes, not
the working tree):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-23/c3/count.py 2f1134f38930fc8b067d2d7f5bba126338faabdd
```

→ exit **0**, `"counter_version": 2`, `"accounted_rows"` = all five tracked tools,
**`"mismatches": []`, `"count": 0`**.

Lane's own after-receipt for that measurement:
`.ufo/waves/round-23/evidence/c3-after-2f1134f3.json` — same JSON, `count: 0`, but **still
untracked**, so the measured after-value is not yet durable in the lane. **C3 = 0 is met.** The
before-value at the immediately preceding commit `4de4464` was `count: 5`, exit 1
(`evidence/c3-before-v2-e33ea304.json`, which *is* tracked).

| | value |
|---|---|
| landed commit | `2f1134f3` ("round-23: C3 PROVINCE refinement accounts for every tracked lane tool") |
| `PROVINCE.md` at that commit | sha256 `78bca86de7c0cc2088260138891b25ba745bc4e14f3151a745a575c89b65ec9d`, 30 lines |
| diff shape | `+10 / −0`, single hunk `@@ -19,0 +20,10 @@` — lines 1–19 byte-identical, the closing `**Out of province …**` line moves from 20 to 30, not edited |
| landed content | my **pre-souji** draft verbatim; contains **no** `souji` mention |
| counter at `2f1134f3` | exit **0**, `count: 0`, `mismatches: []` |

**Correction to my own earlier claim, recorded because it was wrong twice.** My first draft of this
section said the refinement was "LANDED BY L1" and that "C3 = 0 is met on the landed bytes" — an
overclaim: at that moment the text was in the working tree only and the committed counter still gave
5. My second draft said "not yet met on any committed revision" — correct at 08:44, superseded at
08:49 when the commit landed. The landed state is the one measured above.

**One optional wording item remains open for L1 (not a counter problem).** The landed tripwire owner
cell omits **souji**, whose `tools/souji-seat-audit.py` also classifies every recorded tool call (from harness-rendered transcript exports, coverage possibly partial)
(ConnSibling's finding; verified in `souji-shokunin/tools/souji-seat-audit.py:2-9` and
`souji-shokunin/SKILL.md:200`). **C3 does not depend on it**: the landed text already measures
`count: 0`.

**The amendment must be append-only — ConnSibling's correction to my draft.** My draft block in this
report bakes souji into the tripwire owner cell, but that cell is now a *committed* line: pasting
that block would rewrite a committed cell and break append-only. The correct form is a **new dated
line after the table**, leaving every row, cell and column byte-identical.

**Re-measured at the new tip `3732c7a`** (the earlier check was against `2f1134f3`, and the tip has
moved): applying the line to the committed `3732c7a:PROVINCE.md` gives **3 lines inserted, 0
deleted, 0 replaced**, all five landed table rows byte-identical, and the counter still **exit 0 /
`count: 0` / `mismatches: []` / `accounted_rows` = 5**. The file grows from 32 to 35 lines.

**Placement has moved with the tip:** the line now goes **after line 30** (L1's wave-2 correction
paragraph) and **before line 32** (the closing `**Out of province → report, never absorb.**`),
i.e. after the table *and* after the wave-2 correction, so it reads as the latest append.

```markdown
**Round-23 addition (C3 adjacency completeness; append-only; no row, column or cell is edited):** the `tools/mado-tripwire.py` row above names mori, tsukuroi and kagi as adjacent lanes; souji is adjacent too, because `souji-shokunin/tools/souji-seat-audit.py` also classifies every recorded tool call (from harness-rendered transcript exports, coverage possibly partial) against the wave contract. The two ask different questions — mado's tripwire asks which class of command was issued (post-hoc source shape, lane-local evidence), souji's asks whether the seat broke the wave contract (write scope, forbidden surfaces) — so souji's seat-contract audit is named as an adjacent owner and no row of the table is changed. No other tool, row, cell or lane boundary is altered by this line. The two ask different questions — mado's tripwire asks which class of command was issued (post-hoc source shape, lane-local evidence), souji's asks whether the seat broke the wave contract (write scope, forbidden surfaces) — so souji's seat-contract audit is named as an adjacent owner and no row of the table is changed. No other tool, row, cell or lane boundary is altered by this line.
```

Place it after the table and before the closing `**Out of province → report, never absorb.**` line.
It would need its own commit and its own after-value measurement at that commit.

**L1's three items, as of `3732c7a` (superseded by the final note above) — two were then closed, one remains:**

1. **`LOG.md` entry — DONE.** `LOG.md` now carries a round-23 entry (section "## 2026-10-22 — round
   23: repair-first recovery (operator ruling D11)", with a "C3 (calibration)" paragraph reading
   "Append-only PROVINCE refinement with a five-row table, then a wave-2 correction of the
   `mado-verify.sh` reads, the tripwire redaction scope and the mori/tsukuroi overlaps. Counter
   `c3/count.py` v2 5 → 0 at `3732c7a7`."), committed in `3df1062`.
2. **The after-receipts — DONE.** All six are now tracked
   (`git ls-files .ufo/waves/round-23/evidence/` lists `c2-after-2f1134f3.json`,
   `c3-after-2f1134f3.json`, `repair-after-2f1134f3.json` and `c2-after-3732c7a7.json`,
   `c3-after-3732c7a7.json`, `repair-after-3732c7a7.json`); `git status --porcelain
   .ufo/waves/round-23/evidence/` is empty. The after-value is durable.
3. **The souji line — STILL OWED, and now superseded by L1's wave-2 correction.** The committed
   `PROVINCE.md` at `3732c7a` contains **zero** `souji` mentions. L1's wave-2 paragraph already
   names the tripwire's overlap with **mori** and the `mado-verify.sh` overlap with **tsukuroi**;
   souji is the remaining adjacency. The proposed dated line below was re-measured at the new tip.

## The exact paragraph text (paste-ready; lands between the round-19 paragraph and the closing line)

Insert as a new paragraph immediately **after** the round-19 refinement paragraph and **before**
`**Out of province → report, never absorb.**` — the same insertion point round-19 used. Lines 1–18
and the closing line stay byte-identical.

````markdown
**Round-23 refinement (C3 lane-tool inventory; no new write surface, no cross-domain bleed):** the lane's own analysis instruments are named here so the province accounts for every tracked tool it runs. `tools/mado-action-plan.py` reads the JSON bytes of a caller-supplied declared action plan and a JSON safety policy (regular files only; symlinks, FIFOs and devices are refused), prints one `MADO_PLAN:` line and one JSON verdict, writes no host state (its `--selftest` writes only ephemeral fixtures inside a private temporary directory and runs a copy of itself as a child process), and is therefore a lane safety gate over declared plans rather than a new desktop surface. `tools/mado-tripwire.py` reads the `.jsonl` bytes of OMP session transcripts it is pointed at, treating assistant command text as data it never executes, prints one `MADO_TRIPWIRE:` or `MADO_TRIPWIRE_FROZEN:` line and one JSON verdict, writes no file at all (its `--selftest` only re-invokes itself), and is therefore a lane evidence instrument over issued-command text rather than a new desktop surface. `tools/mado-assessment.py` reads an assessment bundle and the population and expectation files it names under `--root` (bounded, symlink- and traversal-refused), prints one JSON verdict object, writes no file at all (its `--selftest` only re-invokes itself), and is therefore a lane integrity gate over the lane's own paperwork rather than a new desktop surface. `tools/mado-evidence-audit.py` reads an evidence bundle, the snapshot it names and the inventoried files under `--root` whose digest and size it compares, prints one JSON verdict object, writes no file at all (its `--selftest` only re-invokes itself), and is therefore a lane evidence gate over artifact arithmetic rather than a new desktop surface. OUT (report, never absorb): these instruments own no config tree and no host state; the tripwire's transcript bytes are read as data and its findings are lane-local evidence about issued commands, never a fleet-wide or sibling-lane conduct verdict (transcript observation stays with mori, seat-contract audit of rendered tool calls with souji); package state stays with tsukuroi; secret-shaped values stay with kagi (the tripwire redacts secret-shaped substrings from the command text it prints instead of reporting their content); and the reusable mutation-testing method stays with tameshi (`tools/mado-verify.sh` consumes tameshi's `mutate-and-run.sh` read-only and prints its revision as provenance, never patching it and never gating it).

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| `tools/mado-action-plan.py` | the JSON bytes of a caller-supplied declared action plan and a JSON safety policy (regular files only; symlinks, FIFOs, devices and directories refused), or in `--frozen` the pinned `plan.json`, `policy.json` and `expected.json` of a snapshot directory | no host state; `--selftest` writes only ephemeral fixtures inside a private temporary directory it removes on exit, and runs a copy of itself as a child process | mado (declared-plan safety gate; it never executes the supplied argv), tsukuroi (package and service state), operator applies any resulting change |
| `tools/mado-tripwire.py` | the `.jsonl` bytes of OMP session transcripts it is pointed at — assistant `toolCall` blocks only (bash `arguments.command`, python eval `arguments.code`), text treated as data and never executed; symlinks, `agent.db`-named files and paths under `~/.omp/agent` outside `sessions/` are refused; `--frozen` also reads the pinned `expected.json` and `inputs/*.jsonl` | nothing — no file is created or modified; stdout only, plus a `--selftest` child process of itself | mado (lane-local evidence about issued commands only; never a fleet or sibling-lane conduct verdict), souji (seat-contract audit of rendered tool calls, `tools/souji-seat-audit.py`), mori (transcript observation), tsukuroi (package state), kagi (secret-shaped substrings are redacted, not reported) |
| `tools/mado-assessment.py` | the JSON bytes of an assessment bundle and, under `--root`, the population and `expected.json` files that bundle names (bounded to 2 MiB each; symlinks, path traversal and escaping paths refused); `--selftest` reads the sealed round-21 fixtures | nothing — no file is created or modified; stdout only, plus a `--selftest` child process of itself | mado (artifact-assertion integrity gate over the lane's own paperwork; no admission, closure or promotion authority) |
| `tools/mado-evidence-audit.py` | the JSON bytes of an evidence bundle and the snapshot that bundle names under `--root`; `--selftest` additionally reads the sealed round-22 fixture manifest and re-hashes every inventoried file, comparing each sha256 and size against the pinned inventory | nothing — no file is created or modified; stdout only, plus a `--selftest` child process of itself | mado (artifact arithmetic and evidence-label audit only; not execution truth, chronology, admission or promotion) |
| `tools/mado-verify.sh` | the file bytes of the declared config planes (hypr, waybar, walker, terminal and omarchy-theme trees) and `hyprctl` read verbs only (version, instances, configerrors, getoption, binds, monitors, layers); `--regression` writes the embedded defect spec (byte-identical to tameshi's recorded case) into scratch, hashes the harness and its own bytes, and hands the spec to tameshi's `mutate-and-run.sh` read-only | no config bytes; scratch only under `/tmp/w5-mado-m52-*` (selftest) and `/tmp/mado-verify-regression.*` (regression, removed unless `--keep`) | mado (config-plane verdict gate; the operator applies changes), tameshi owns the mutation-testing method — `mutate-and-run.sh` is consumed read-only and its revision is printed as provenance, not gated |
````

## Why this shape, and the two facts that force it

**The counter of record (v2) does not accept prose.** `4de4464` rewrote
`.ufo/waves/round-23/c3/count.py` from "bare filename mention" to:

> "A tool is accounted for only by a Markdown table row in PROVINCE.md whose first cell names the
> tool's repo path in backticks and which has at least four non-empty cells (tool, what it reads,
> what it writes, owner and adjacent lanes). A bare mention in prose does not count. The
> pre-existing gate `tools/mado-verify.sh` is held to the same rule."

Two consequences, both load-bearing for L1:

1. A prose-only paragraph would leave the counter at **4**, not 0. The paragraph alone is necessary
   (it carries the per-tool sentences and the OUT clause) but not sufficient; the table is what the
   counter reads.
2. Under v2 the base value is **5**, not 4 — `tools/mado-verify.sh` was credited by a bare prose
   mention under v1 and is now a mismatch too. So the append must carry **five** rows, not four.
   Registration clarification item 4 records this: "Under v2 the base value is **5**
   (`mado-verify.sh` was credited by a bare mention under v1) … Target stays **0**."

The four-column table matches the counter's own cell vocabulary (tool / reads / writes / owner and
adjacent lanes), which is also what registration clarification item 6 asks the refinement to state:
"call the tools lane-internal instruments, state the actual reads and writes (subprocess children
and selftest temp dirs included) and name adjacent owners (mori for transcript observation,
tsukuroi for package state)."

## Per-tool facts, each with its source

### `tools/mado-action-plan.py` — round-16, `9dcf248` ("round-16: source-only Waybar route and bounded action classifier")

- **Reads** the JSON bytes of a caller-supplied declared action plan and a JSON safety policy.
  `--frozen` instead reads a snapshot's pinned `plan.json`, `policy.json` and `expected.json`.
  Inputs are regular files only — `_read_regular` (`:150`) opens with `O_NOFOLLOW`, rejects
  symlinks/FIFOs/devices/dirs/sockets, and bounds the read; the docstring adds that malformed
  UTF-8, duplicate JSON keys and non-finite numbers all fail closed with exit 2.
- **Outputs** one `MADO_PLAN: <finding>` line plus one JSON verdict object
  (`_emit`, `:134`; schema `mado-action-plan-verdict-v1`); exit 0 `plan_safe`, 1 blocked/denied/
  unknown, 2 could-not-evaluate.
- **Writes no host state.** The only write-mode `open`, `os.makedirs`, `os.symlink` and `os.mkfifo`
  calls in the whole file live inside `run_selftest` / `write_frozen` (AST walk: lines 702, 737,
  739, 763) and every one of them is under a `tempfile.TemporaryDirectory(prefix="mado-plan-selftest-")`
  that the context manager removes on exit. `--selftest` also spawns a child process
  (`_self_invoke`, `:522` → `subprocess.run([sys.executable, "-I", script, ...], shell=False, cwd=tmp)`).
- **Why lane-own safety instrument, not a new desktop surface**: it classifies a *declared* plan's
  `kind` labels and the lexical basename of `argv[0]` only — "supplied executables are never
  resolved, executed, or probed" (docstring) — and it reads no config tree (grep for
  `.config|hypr|waybar|walker|kitty|ghostty|foot|alacritty|omarchy|hyprland` in the tool matches
  only its own pinned deny-list *names* and selftest fixtures, never a path it opens).

### `tools/mado-tripwire.py` — round-17, `988b858` ("round-17 C3: post-hoc transcript tripwire capability, suites and real-transcript receipts")

- **Reads** the `.jsonl` bytes of OMP session transcripts it is pointed at, parsing assistant
  `toolCall` blocks only (bash `arguments.command`; python eval `arguments.code` — `!` shell lines,
  `%%bash` cells, literal subprocess/os/tool.bash spawns parsed with `ast`). "Transcript text is
  data. Nothing in it is followed or executed." (docstring, `:138`). `refuse_path` (`:2758`)
  refuses symlinks, refuses any path under `~/.omp/agent` that is not under `sessions/`, and
  refuses `agent.db`-named files; only `.jsonl` files are opened. `--frozen` also reads the pinned
  `expected.json` and `inputs/*.jsonl`.
  **Per L1's note (via ConnSibling, round-22 `ConnProvince.md:19-22`):** the tool reads *any* OMP
  session JSONL it is pointed at, as data — round 20 ran it over the whole fleet's session
  transcripts. The draft therefore says "OMP session transcripts it is pointed at", and the OUT
  clause explicitly refuses the fleet-wide reading ("never a fleet-wide or sibling-lane conduct
  verdict"), matching the round-22 connector's finding CP-U1.
- **Outputs** one `MADO_TRIPWIRE: clean|permitted_only|findings|could_not_evaluate` line (or
  `MADO_TRIPWIRE_FROZEN: …`) plus one JSON verdict; exit 0/1/2, 2 wins over 1. Printed command
  text is redacted (`redact`, `:323`) against `SECRET_PATTERNS` (`:301`) — credential-shaped
  substrings are replaced with `<redacted>`, not reported.
- **Writes no file at all.** There is no write-mode `open`, `os.makedirs`, `os.remove` or
  `tempfile.*` in the file (grep returns none); `--selftest` spawns only a child process of itself
  (`subprocess.run(argv, …)`, `:3320`).
- **Why lane-own evidence instrument, not a new desktop surface**: it is a post-hoc source-shape
  classifier over seat-issued command text — "not interception, prevention, a sandbox or host
  repair" (docstring) — with no config-tree read and no live probe.

### `tools/mado-assessment.py` — round-21, `843d301` ("round-21: implement bounded tripwire repair and independent assessment gate")

- **Reads** an assessment bundle JSON and, under `--root`, the population and `expected.json` files
  that bundle names. Reads are bounded to 2 MiB (`MAX_BYTES`, `:20`); `rooted()` (`:46`) refuses
  symlinks, absolute paths, `..` traversal and paths escaping the root.
- **Outputs** one JSON verdict object on stdout (`code`, `result`, `finding_ids`,
  `actual_inputs`, `actual_expectations_sha256`, `authority`); exit 0 clean / 1 failed / 2
  could-not-evaluate. Its own `authority` string: "artifact assertions only; no authenticated
  chronology, authorship, semantic proof or promotion authority".
- **Writes no file at all.** The only `open` calls are `path.open('rb')` (`:42`); `--selftest`
  spawns only a child process of itself (`subprocess.run(cmd, …)`, `:183`).
- **Why lane-own evidence instrument, not a new desktop surface**: "Read-only artifact assertion
  gate, not independent authentication of its author… No classifier, transcript evaluation, Git,
  host state or network is consulted." (docstring). It reads no config tree — grep for
  `.config|hypr|waybar|walker|kitty|ghostty|foot|alacritty|omarchy|hyprland` returns nothing.

### `tools/mado-evidence-audit.py` — round-22, `330de68` ("round-22: implement bounded lifetime repair and independent evidence audit")

- **Reads** an evidence bundle JSON and the snapshot that bundle names under `--root`
  (`check()`, `:124`); `--selftest` additionally reads the sealed round-22 fixture manifest and
  re-hashes every inventoried file, comparing each sha256 and size against the pinned inventory
  (`inventory()`, `:172`). Bounded to 2 MiB per file; symlinked roots, symlinked inventory
  ancestors and non-regular entries are refused.
- **Outputs** one JSON verdict object on stdout (`code`, `result`, `finding_ids`, `authority`,
  `actual_counts`, `actual_snapshot_sha256`); exit 0 consistent / 1 contradicted / 2
  could-not-evaluate. Its `authority` string: "artifact arithmetic and evidence labels only; not
  semantic correctness, authentication, admission or promotion".
- **Writes no file at all.** The only `open` calls are `path.open('rb')` (`:60`, `:110`);
  `--selftest` spawns only a child process of itself (`subprocess.run(…)`, `:243`).
- **Why lane-own evidence instrument, not a new desktop surface**: "Audit artifact arithmetic and
  explicit evidence labels, never execution truth… No classifier, host probe, Git, network,
  authenticated chronology, admission or promotion authority is consulted." (docstring). Reads no
  config tree (same grep → nothing).

### `tools/mado-verify.sh` — the pre-existing gate, now also a v2 mismatch

- **Reads** the file bytes of the declared config planes and `hyprctl` read verbs only ("READ-ONLY
  on every substrate", header `:22`); `--regression` writes the embedded defect spec (byte-identical
  to tameshi's recorded case, pinned by `SPEC_SHA`) into scratch, hashes the harness and its own
  bytes, and hands the spec to tameshi's `mutate-and-run.sh` read-only.
- **Outputs** one `MADO_VERIFY: CLEAN|DIVERGED (...)` verdict line; exit 0/1/2.
- **Writes** no config bytes; scratch only under `/tmp/w5-mado-m52-*` (selftest) and
  `/tmp/mado-verify-regression.*` (regression, removed unless `--keep`).
- **Why it is a lane-own safety instrument, not a new desktop surface**: it is the gate *for* the
  declared planes; it verifies them and never edits them. It already appears in the round-19
  paragraph (`tools/mado-verify.sh`) — v2 simply demands a table row.

## Cross-domain checks (Refuses list) — what the draft does and does not claim

- **Secrets stay kagi's.** The draft states that secret-shaped values stay with kagi and that the
  tripwire redacts them from what it prints. This is a claim about the tripwire's *own* redaction
  (`redact()`, `SECRET_PATTERNS`), verified in source, not a claim that mado handles secrets. No
  secret value is read or printed by the draft.
- **Mutation-testing method stays tameshi's.** The draft says the reusable method stays tameshi's
  and that `tools/mado-verify.sh` consumes `mutate-and-run.sh` read-only, printing its revision as
  provenance and never gating it. That matches the tool's own discipline comment
  (`tools/mado-verify.sh:1938-1940`: "the harness … is consumed read-only — a needed change is a
  recommendation to tameshi, never a patch; its revision is printed as provenance, not gated").
- **Model endpoints → kama, model quality → kengaku** (existing Refuses lines) — the draft touches
  neither and does not name either, so no bleed.
- **New write surface?** None. The draft asserts each tool writes no host state, and the OUT clause
  says "these instruments own no config tree and no host state". No `~/.config` tree, no compositor
  state, no installed program is added to the Owns list.
- **Fleet-wide scope?** Explicitly refused in the OUT clause, per L1's note and round-22 CP-U1.
  Transcript observation is named as mori's; package state as tsukuroi's.
- **Seat-contract audit belongs to souji.** ConnSibling flagged (and I verified) that
  `souji-shokunin/tools/souji-seat-audit.py` is the one sibling tool that also classifies seat
  tool calls — "reads the harness-rendered transcripts of every seat in one wave (one text file per
  seat, `<SeatName>.txt`, exported from `history://<lane>.<SeatName>`) and classifies every
  **recorded** tool call (`→ tool(args…) ⇒ status`) against the wave contract" (its docstring,
  `:2-9`), with its own gate row at `souji-shokunin/SKILL.md:200`. Note the wording: **recorded**,
  not *issued* — souji sees only the rendered exports it is given, and its own registry row states
  "possibly partial coverage (inspect missing_transcripts)". It is therefore not a claim about every
  call a seat made. The tripwire row therefore names
  **souji (seat-contract audit of rendered tool calls, `tools/souji-seat-audit.py`)** alongside mori,
  tsukuroi and kagi, and the OUT clause names souji next to mori. (That is what **this draft** says;
  the committed text at `2f1134f3` contains **zero** `souji` mentions — the addition is owed to L1
  as the dated line above.) The two ask different questions —
  mado's tripwire asks *which class of command was issued* (post-hoc source shape, lane-local
  evidence); souji's asks *did the seat break the wave contract* (write scope, forbidden surfaces) —
  so naming souji is adjacency, not a claim over souji's ground.

## Checks run (read-only)

### CK1 — the four tools' CLI surface and docstrings (read-only; `--help` only)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I tools/mado-action-plan.py --help
python3 -I tools/mado-assessment.py --help
python3 -I tools/mado-evidence-audit.py --help
python3 -I tools/mado-tripwire.py --help
```

Observed usage strings (exit 0 for the first three; the tripwire prints its usage verdict to stdout
and exits 2 because `--scan`/`--frozen`/`--selftest` are all required):

```
usage: mado-action-plan.py [-h] (--plan PATH | --frozen DIR | --selftest) [--policy PATH]
usage: mado-assessment.py [-h] (--check CHECK | --selftest SELFTEST) [--root ROOT]
usage: mado-evidence-audit.py [-h] (--check CHECK | --selftest SELFTEST) [--root ROOT]
usage: mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...] | --frozen DIR | --selftest DIR
```

### CK2 — write-surface audit of the four tools (AST + grep, source only)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
for f in tools/mado-action-plan.py tools/mado-assessment.py tools/mado-evidence-audit.py tools/mado-tripwire.py; do
  echo "=== $f"; grep -nE "open\([^)]*['\"][waxr]\+?['\"]|write_text|write_bytes|mkdir|makedirs|unlink|remove\(|shutil\.|tempfile\.|NamedTemporary|mkstemp|os\.remove" "$f" | head -30
done
```

Observed: `mado-action-plan.py` matches only inside `run_selftest` (all under its
`TemporaryDirectory`); `mado-assessment.py` and `mado-evidence-audit.py` match nothing at all (their
only `open` calls are `path.open('rb')`); `mado-tripwire.py` matches only the *string* `"remove"`
inside a verb list (`:1066`), not a call. AST walk confirms write-mode `open`/`os.makedirs`/
`os.symlink`/`os.mkfifo`/`tempfile.*` occur in `mado-action-plan.py` only, and only in
`run_selftest`/`write_frozen`.

### CK3 — the counter of record, run for real against a scratch clone (not a re-implementation)

The real script `.ufo/waves/round-23/c3/count.py` (v2, from `4de4464`) was copied into a scratch
git repo whose `tools/` holds the five tracked tools and whose `PROVINCE.md` is the current lane
file with the draft paragraph + table inserted; then:

```sh
python3 -I /tmp/mado-r23-provscope/lane/.ufo/waves/round-23/c3/count.py $(git -C /tmp/mado-r23-provscope/lane rev-parse HEAD)
```

Result — **exit 0**, `counter_version: 2`, `"count": 0`, `"mismatches": []`, and
`"accounted_rows"` listing all five:

```json
{
 "rev": "e2fd2e3783bdd065eef2fff5d8e2d0107b638781",
 "counter_version": 2,
 "self_assessment": "- [~] No cross-domain bleed (PROVINCE.md still accurate)",
 "tracked_tools": ["tools/mado-action-plan.py","tools/mado-assessment.py","tools/mado-evidence-audit.py","tools/mado-tripwire.py","tools/mado-verify.sh"],
 "accounted_rows": ["tools/mado-action-plan.py","tools/mado-assessment.py","tools/mado-evidence-audit.py","tools/mado-tripwire.py","tools/mado-verify.sh"],
 "mismatches": [],
 "count": 0
}
```

Control (same script, same scratch repo, draft removed): exit **1**, `"count": 5`,
`"mismatches"` = all five tracked tools, `"accounted_rows": []`. So the drop is caused by the
draft, and only by the draft.

### CK3b — the working-tree bytes, counted in a scratch clone (content check only)

The lane's `PROVINCE.md` working copy was **read** (never written by me), copied into a scratch git
repo and committed there, then measured with the real v2 script:

```sh
python3 -I /tmp/mado-r23-provscope/landed/.ufo/waves/round-23/c3/count.py $(git -C /tmp/mado-r23-provscope/landed rev-parse HEAD)
```

→ exit **0**, `"count": 0`, `"mismatches": []`, `"accounted_rows"` = all five tracked tools.

This proves the **content** is correct. It is **not** a landed-value measurement: the scratch commit
is not the lane's revision, so this does not and cannot satisfy the claim. The lane's own after-value
is CK6 below.

### CK6 — the lane's committed bytes at HEAD (the value that counts; measured 08:44)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-23/c3/count.py 4de44647f93bfd25ed5c979f61ff016b50456549
```

→ exit **1**, `"counter_version": 2`, `"accounted_rows": []`, `"mismatches"` = all five tracked
tools, **`"count": 5`**.

Cross-check over every revision that ever touched `PROVINCE.md` (v2 counter, committed bytes):

| revision | count | note |
|---|---|---|
| `74d3b7b` (round 0) | — | **exit 2**, `{"error": "SHONEN box 4 self-assessment not found"}` — that commit's `SHONEN.md` has no box 4, so the counter cannot evaluate |
| `df84807`, `b455b9e`, `848d1ff`, `562a8a1`, `d4d9596`, `95ac146`, `61eaa07` | **3** | only three tracked tools existed then |
| `4de4464` (HEAD) | **5** | five tracked tools; none accounted by a table row |
| working tree | **0** (content check) | uncommitted; the counter of record cannot see it |

**No committed revision reaches 0.** The registered target C3 = 0 is unmet until L1 commits the
refinement; registration clarification 10 requires the after-value to be taken at the landed tip.

### CK4 — append-only byte preservation

Two measurements, two different files — kept distinct because they differ by one blank line:

- **The landed commit `2f1134f3`:** `git show 2f1134f3 --numstat -- PROVINCE.md` → **10 added, 0
  deleted**, single hunk `@@ -19,0 +20,10 @@`. `git show 2f1134f3:PROVINCE.md | head -19` diffed
  against `git show 4de4464:PROVINCE.md | head -19` → **identical**; lines 1–19 are byte-unchanged
  and the closing `**Out of province …**` line moves from 20 to 30 without being edited.
- **My scratch variant** (the block in this report, which carries the souji addition and one
  trailing blank line): `difflib.SequenceMatcher` over the original 20 lines → **11 lines inserted,
  0 deleted, 0 replaced blocks**.

Both are append-only in the sense that matters: no existing line is deleted or rewritten, and the
whole original text is preserved verbatim.

### CK5 — lane base state, read-only

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --oneline -3
```

→ `4de4464` (round-23: tighten C2/C3 counters …), `a28e481` (round-23: C3 self-assessment
mismatch counter …), `6b383c4` (round-23: registration, frozen repair set and before receipts …).
The lane working copy has only untracked `.ufo/waves/round-23/w1*` files; `PROVINCE.md` is unmodified
at sha256 `1b25bb1e…`.

## Conflicts to report to the canonical Rust judge (verbatim)

1. The task text for this seat asks for "an append-only PROVINCE.md refinement **paragraph** naming
   the four lane tools", but the counter of record (v2, `4de4464`) counts a tool only through a
   **Markdown table row** with ≥4 non-empty cells and the tool path in backticks as the first cell:
   "A bare mention in prose does not count." A prose-only paragraph leaves the counter at 4.
2. The task text names **four** tools; the counter of record's population is **five** tracked tools
   (`git ls-tree -r --name-only REV tools/`), and registration clarification item 4 records the v2
   base as **5**: "Under v2 the base value is **5** (`mado-verify.sh` was credited by a bare mention
   under v1)". A four-row append cannot reach 0.
3. The task text says the paragraph should "state for each … one plain sentence"; the counter's cell
   vocabulary asks the same facts in table form. The draft does both — prose sentences per tool
   (read / output / no host write / why lane-own) plus the five-row table the counter reads. If L1
   prefers one form only, the table is the one the counter scores.
4. **ConnSibling's v2 correction agrees with mine** (it appended a dated correction to
   `.ufo/waves/round-23/w1/reports/ConnSibling.md`): v2 at `4de4464` gives count 5 / exit 1 at both
   `e33ea304` and `a28e4815`, and `tools/mado-verify.sh` was credited only under v1. My draft
   already carried five rows for that reason. One gap it raised is addressed **in this draft** —
   souji is named in the tripwire owner cell — but it is **not** in the committed text at
   `2f1134f3`, which has zero `souji` mentions; landing it needs the dated line above (see below).
5. **ConnSibling's landing-status correction was right, and it corrected an overclaim of mine.** I
   had written that the refinement was "LANDED" and that "C3 = 0 is met on the landed bytes" when it
   was in the working tree only; the counter reads committed bytes and still gave 5 / exit 1 at
   `4de4464`. My CK3b (commit the same bytes in a scratch clone → exit 0) is a content check, not a
   landed-value measurement; it is now labelled as such, with CK6 for the committed value and the
   landed-tip measurement added. **Resolved:** L1 committed the refinement as `2f1134f3` at 08:49:46
   and the after-value at that commit is **count 0 / exit 0**.

## Touched surfaces

- **Written by me:** `.ufo/waves/round-23/w1/reports/ScribeProvinceScope.md` (this file) only.
- **Written by L1, not by me:** lane commit `2f1134f3` landed the `PROVINCE.md` refinement
  (+10 / −0). I did not write, edit, stage, commit or revert `PROVINCE.md`; my only lane write is
  this report. The refinement existed in the working tree from 08:38:28 (not my write) and was
  committed at 08:49:46.
- **Read (read-only):** `PROVINCE.md`, `SHONEN.md`, `AGENTS.md`, `SKILL.md` (gate-registry rows only),
  `LOG.md` (tool rows only), `corpus/knowledge/province-accuracy-selfaudit.md`,
  `corpus/lessons/round-22.md`, `tools/mado-{action-plan,assessment,evidence-audit,tripwire}.py`,
  `tools/mado-verify.sh` (header and write sites), `.ufo/waves/round-23/{registration.md,c3/count.py}`,
  `.ufo/waves/round-23/evidence/c3-before-v2-e33ea304.json`,
  `.ufo/waves/round-22/w1/reports/ConnProvince.md`, sibling `PROVINCE.md` files
  (mori, tsukuroi, kagi, tameshi, kumitate) for adjacent-owner wording, and lane git history
  (read-only `git log`/`show`/`ls-tree`/`status`; one `jj --ignore-working-copy log`).
- **Scratch (outside the lane):** `/tmp/mado-r23-provscope/` (draft text, scratch lane clone,
  simulated PROVINCE files). Nothing was written under `/home/vgpnk/Projects/shokunin` outside the
  lane, and nothing under `/home/vgpnk/Projects/shokunin/mado-shokunin` except this report.

## Out of scope (deliberately not done)

- **`PROVINCE.md` was not edited.** The draft text is in this report; landing it is L1's.
- No `tools/` change, no `corpus/`, `SKILL.md`, `LOG.md`, `SCORECARD.md` or `SHONEN.md` change.
- No `LOG.md` entry: AGENTS.md requires one per change, but this seat changed no lane file; L1 adds
  it when the append lands (recording the new `wc -l` and sha256, as round-19 did).
- No jj command was run in the lane except read-only `jj --ignore-working-copy log`; no git write
  command was run in the lane; no push, no clone, no patch.
- No tool was executed in a mode that writes to the host: only `--help` was run on the four tools,
  and the counter was run against a scratch clone.
- No round-20 fleet sweep was re-run and no fleet transcript was opened; the tripwire's read scope
  is described from its own source and docstring.

## Findings (one-line verdicts)

- **Counter v2 needs a table, not prose:** the C3 counter of record credits a tool only via a
  backticked path in the first cell of a ≥4-cell Markdown table row; prose mentions do not count.
- **The population is five, not four:** under v2 the base value is 5 (`mado-verify.sh` joins the
  four), so the append must carry five rows to reach the registered target 0.
- **All four undeclared tools write no host state:** verified in source — `mado-action-plan.py`
  writes only inside a self-removing `TemporaryDirectory` during `--selftest`; the other three open
  files read-only and spawn only a child process of themselves.
- **None of the four opens a desktop surface:** none reads a `~/.config` tree, a compositor state or
  a live probe; they are gates and evidence instruments over declared plan JSON, transcript bytes
  and lane paperwork.
- **The draft content passes the real counter:** exit 0 / `count: 0` on the actual v2 script
  against a scratch clone with the draft applied; exit 1 / `count: 5` without it; 11 lines inserted,
  0 deleted, 0 replaced. Re-verified after the souji adjacency addition: still exit 0 / `count: 0`.
  (Scratch-measurement figures for the draft variants, not the lane's committed value — that is the
  next bullet.)
- **C3 is met on committed bytes at the landed tip:** the tip is now `8e5d936`, and the counter at
  HEAD gives **count 0, exit 0**, `mismatches: []`, `accounted_rows` = all five; the before-value at
  `4de4464` was **count 5, exit 1**. `PROVINCE.md` has not changed since `3732c7a`, so the
  refinement commit `2f1134f3` and the wave-2 correction `3732c7a` still carry the whole claim.
  Committed receipts: `c3-after-2f1134f3.json` and `c3-after-3732c7a7.json`, both tracked.
- **C1 is an honest stop at 6/12** (`3df1062` restored the classifier to base bytes `cd9da20c…`;
  `LOG.md:1569`). This is C1's outcome, not C3's — C3 measures PROVINCE coverage of the tracked
  tools and is met.
- **L1's item list is now one item, not three:** the `LOG.md` entry is landed (committed in
  `3df1062`) and all six after-receipts are tracked; only the **souji line** remains, still owed.
  The committed `PROVINCE.md` at `3732c7a` has zero souji mentions; the proposed dated line (after
  line 30, before line 32) measures 3 inserted / 0 deleted / 0 replaced with the counter still at
  `count: 0` at the new tip.
- **L1's wave-2 correction supersedes parts of my own table rows**: `mado-verify.sh` also runs live
  read-only probes (not "hyprctl read verbs only"), the tripwire redacts only its three fixed secret
  patterns (other shapes can reach stdout), the tripwire's read surface is *shared with* mori and
  that overlap is named for the integrator rather than self-certified, and the inventory covers every
  tracked file under `tools/` rather than "every tracked tool it runs". My draft rows are therefore
  no longer the whole truth; L1's paragraph governs.
- **Souji is an adjacent lane for the tripwire row, and it is NOT yet named in the committed
  text** (raised by ConnSibling, verified in `souji-shokunin/tools/souji-seat-audit.py:2-9` and
  `souji-shokunin/SKILL.md:200`): the committed `PROVINCE.md` at `2f1134f3` contains **zero**
  `souji` mentions, and its tripwire owner cell names only mori, tsukuroi and kagi. The proposed
  **new dated line after the table** (given above) would name souji there; it is still owed to L1
  and is not done.

## Artifacts

- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ScribeProvinceScope.md`
- Draft text (paste-ready, same bytes as the block above):
  `/tmp/mado-r23-provscope/para.txt` (scratch; the block in this report is authoritative)
- Souji adjacency verified against: `/home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-seat-audit.py`
  (docstring `:2-45`) and `/home/vgpnk/Projects/shokunin/souji-shokunin/SKILL.md:200`
- Counter of record: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/c3/count.py`
  (v2, lane commit `4de4464`)
- v2 before receipt:
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/evidence/c3-before-v2-e33ea304.json`
- v1 before receipt:
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/evidence/c3-before-e33ea304.json`
- Scratch lane clone used for the measurement: `/tmp/mado-r23-provscope/lane`
- Append-only souji-amendment clone, re-measured at the new tip `3732c7a` (amendment applied,
  measured): `/tmp/mado-r23-provscope/amend2`
- Earlier amendment clone (measured against `2f1134f3`): `/tmp/mado-r23-provscope/amend`
- Proposed append-only souji amendment text: `/tmp/mado-r23-provscope/amend.txt` (the block in this
  report is authoritative)
- L1's committed after-receipts (C3 after-value): `.ufo/waves/round-23/evidence/c3-after-2f1134f3.json`
  and `.ufo/waves/round-23/evidence/c3-after-3732c7a7.json` (both now tracked)

## Verdict

DRAFTED AND LANDED — C3 = **0** on committed bytes. One append-only `PROVINCE.md` refinement
paragraph plus the five-row table the v2 counter of record actually reads, landed by L1 as
`2f1134f3` (+10 / −0, lines 1–19 byte-identical) and corrected by a wave-2 paragraph at
`3732c7a` (+2 / −0). `PROVINCE.md` has not changed since `3732c7a`. After-value at the current tip
`8e5d936`, measured on committed bytes per registration clarification 10:
`python3 -I .ufo/waves/round-23/c3/count.py HEAD` → **exit 0, `count: 0`, `mismatches: []`,
`accounted_rows` = all five**; before-value at `4de4464` was 5 / exit 1; committed receipts
`c3-after-2f1134f3.json` and `c3-after-3732c7a7.json`, both tracked. **I did not edit, stage or
commit `PROVINCE.md`** — my only lane write is this report.
One optional item remains for L1: the landed tripwire owner cell omits **souji** (whose
`tools/souji-seat-audit.py` also classifies every **recorded** tool call, from harness-rendered
transcript exports, coverage possibly partial). It must be added as a **new dated line**, after line
30 and before line 32, since editing a committed cell would break append-only; the proposed line is
given above and measures 3 inserted / 0 deleted / 0 replaced at the new tip with the counter still
at `count: 0`. The `LOG.md` entry and the after-receipts are done (committed in `3df1062` and
tracked respectively).
Separately and outside this claim: **C1 is an honest stop at 6/12** (`3df1062` restored the
classifier to base bytes `cd9da20c…`).
Six conflicts are reported above for the judge: the counter requires a table where the task text
says paragraph; the population is five tools where the task text says four; the prose/table
duplication is deliberate because the counter scores the table; souji's seat-contract audit is an
adjacency the tripwire row now names; a working-tree change is not a landed value (my own
overclaim, corrected here); and souji's tool classifies every **recorded** tool call, not every
tool call a seat **issued** — my first draft of the amendment used mado's "issued" vocabulary on
souji's tool and overstated its coverage, which ConnSibling caught and which is corrected
throughout this report.
