# CritW2Gate — falsification of `quality/check-session-material.py` (round-45 w2 / closure D1)

Seat: CritW2Gate, round 46 w1, 2026-10-26. Target: the round-45 privacy gate at
`quality/check-session-material.py` (frozen; landed ee6659b90f7bf69aa03283dba804dd90081b7ff5, lane tip
4d22eeb66c2835af8aaa3fac6ad838fa616aa663). Lane HEAD during the attack: `e0be61e4`.

Method: `repro.py` (this directory) plants 22 synthetic "must be flagged" shapes and 6 "must stay clean"
shapes into a throwaway `--shared` clone under `/fast/scratch/hyaku/mado-r46/CritW2Gate/`, commits them
(`rev-parse --show-toplevel` asserted), and prints per-shape verdicts through the gate's own
`scan_blob`, plus probes of its scan caps. Captured output: `receipts.txt`. Locators in this report are
computed by `verify.sh` (all 19 match). **No host session material was used**: every value inside a
planted shape is a placeholder (`Example`, `SERIAL0123456`, `SN00000`, `0x55aa`) or explicitly `FAKE`.

Headline: the gate's own selftest is `passed=22/22 failed=0` while **22 of 22 attack shapes pass it
invisibly** and **5 of 6 legitimate shapes are flagged**; at lane HEAD it exits 1 with 97 findings, of
which **54 are synthetic false positives** and 43 are real session material that was never cleaned.

---

## 1. False negatives — 22/22 shapes invisible

| # | planted shape (synthetic values) | realistic origin | gate verdict |
|---|---|---|---|
| 1 | `[{"app_id": "Foot", "caption": "a live window title"}]` | `hyprctl clients -j \| jq` projection with renamed keys | clean |
| 2 | `[{"class": "Foot", "caption": "…"}]` | only the title key renamed | clean |
| 3 | `[{"class": "Foot", "window": {"title": "…"}}]` | title nested one level | clean |
| 4 | `- class: Foot` / `  title: …` | YAML block dump | clean |
| 5 | `- "class": "Foot"` / `  "title": "…"` | YAML with quoted keys | clean |
| 6 | `\tclass: Foot` / `\ttitle: …` | `hyprctl clients` plain text | clean |
| 7 | `address,class,title` CSV | CSV/TSV projection | clean |
| 8 | base64 of the client dump | pasted b64 blob | clean |
| 9 | `- serial: SERIAL0123456` / `  description: …` | YAML monitor dump | clean |
| 10 | `It reported "serial" = "SERIAL0123456", "make" = "Example".` | serial in prose (exactly D2's shape) | clean |
| 11 | `\tserial: SERIAL0123456` / `\tdescription: …` | `hyprctl monitors` plain text | clean |
| 12 | `USER PID %CPU COMMAND` table | `ps aux` | clean |
| 13 | `USER,PID,COMMAND` CSV | `ps` CSV | clean |
| 14 | `users:((\"gnome-keyring-d\",pid=999,fd=9))` | ss output pasted inside a JSON/markdown-escaped receipt | clean |
| 15 | process name 150 chars | long process name | clean |
| 16 | `-rw-r--r-- … /home/someone/d00/f` | `ls -l` of a home tree | clean |
| 17 | `["/home/…", "/home/…"]` | JSON array of paths | clean |
| 18 | `- /home/someone/d00/f` | markdown bullets | clean |
| 19 | `'/home/someone/d00/f'` | quoted paths, one per line | clean |
| 20 | `\x00note\n` + client dump | log with an embedded NUL | clean (whole blob dropped) |
| 21 | client dump encoded UTF-16LE | `iconv`/PowerShell-shaped dump | clean (whole blob dropped) |
| 22 | 20 000 stray `{` + client dump | any file with json-ish noise before the dump | clean, **no truncation signal** |

Root causes, each verified against the frozen source:

- **F1 — literal double-quoted key prefilter.** `scan_json_objects` returns immediately unless the
  literal substrings are present (`:127`, `:136`; call sites `:208-209` and `:222-223`). Dumps that are
  not JSON-with-double-quotes — YAML (4,5,9), plain text (6,11), CSV (7,13), renamed keys (1,2), nested
  title (3) — never reach the predicates. This is the single defect that accounts for 11 of the 22 misses.
- **F2 — JSON-only decoding.** No line-oriented `key: value` fallback exists; `json.loads`/`raw_decode`
  is the only parser (`:127-168`).
- **F3 — whole-blob drops.** `decode()` returns `None` when a NUL byte appears in the first 8192 bytes
  (`:186`) and silently cuts at 16 MiB (`:68`, `:189`): a dump after either boundary is never read
  (20, 21, and the 16 MiB probe in `receipts.txt`).
- **F4 — the object cap counts *failed* decodes.** `examined` increments before the decode attempt
  (`:156`, `:159`), so 20 000 stray `{` exhaust `MAX_OBJECTS = 20000` (`:69`) and the scan stops with
  zero hits; and because a truncation note is only appended when `hits` is truthy (`:211`, `:226`), the
  file is reported as clean with **no** `truncated=True` and no other signal. Measured boundary:
  19 999 strays → flagged, 20 000 → clean (`receipts.txt`, "scan caps"). This is the cheapest evasion:
  a constant prefix, requiring no knowledge of the predicates.
- **F5 — R2's regex is literal.** `PROC_RE` (`:74`) demands `users:(("` with no backslash and caps the
  process name at 128 chars: an ss row pasted with escaped quotes (14) or a long name (15) is invisible.
- **F6 — R4 requires one bare path per line.** `HOME_PATH_RE` is anchored `^/home/…$` (`:75`) and any
  internal whitespace disqualifies the line (`:176`), so every decorated listing (16-19) misses.

## 2. False positives — 5/6 planted shapes, and 54 of 97 findings at lane HEAD

| planted shape (synthetic) | gate verdict | why it is wrong |
|---|---|---|
| docs example `[{"class": "ExampleApp", "title": "Example Window Title"}]` | **R1** | a documentation example of the shape, not session material |
| docs example `[{"serial": "SERIAL0000", "description": "Example Monitor"}]` | **R3** | same |
| docs example `users:(("example-daemon",pid=42,fd=3))` | **R2** | format documentation |
| 12 synthetic `/home/someone/dNN/f` example lines | **R4** | an example layout |
| `lsblk -J` disk inventory (`model` + `serial`) | **R3** | not a monitor at all |
| gate's own `MONITORS_REDACTED` (empty serial) | clean | only the *empty* form is accepted |

**The redaction markers the fleet actually uses are rejected.** `"title": "REDACTED"`,
`"title": "<redacted>"`, `"title": "Example Window Title"`, `"serial": "REDACTED"` are all flagged;
only `""` and `null` are clean (`receipts.txt`, "redaction markers"; predicates `:99`, `_nonempty`).
Precedent in the tree: round-45's own mutant writer emits `"title":"REDACTED"`
(`.ufo/waves/round-45/w1/ScrMistakes/mutants.sh:42`) and the gate flags that **script** as an R1 client
dump. R3 additionally has no monitor signature at all — `serial` + any of `description|make|model`
(`:102-106`) is the shape of every hardware inventory, so a disk/USB/laptop dump trips it.

**Lane HEAD census** (`python3 -I quality/check-session-material.py --repo . --rev HEAD`, run once,
`e0be61e4`): `SESSION_MATERIAL_RULES: R1=23 R2=26 R3=46 R4=2`, `findings=97`, exit 1.

- 54 **false positives on synthetic artifacts**: 45 × `round-45/w1/RevengerOmarchy/fixtures/**/*.json`
  (35 named `mons.json`, 10 named `F01…`/`G01…`/`H01.json`; every one carries
  `"description": "Fake Corp 0x0000 SN00000"` and `"serial": "SN00000"` — the lane's own synthetic
  monitor fixtures), 3 on the seat's copy of the gate itself
  (`round-45/w1/ExecPrivacyGate/check-session-material.py`, i.e. its fixture constants), 1 on the mutant
  writer above, 2 on `round-44/w1/ScrLessonSkeleton/c1-demo/client{1,2}.json` (`"title": "gkeep"`),
  2 on the `FAKE`-socket ss fixtures (`round-37/w1/scratch/CritC2Cheap/handsnap.txt`,
  `.../SimplifyCounters/diff_c2.sh`), and 1 R4 on `round-35/.../S203.scope.txt` — 12 bare lines that are
  **public omarchy install paths** (`/home/vgpnk/.local/share/omarchy/install/…`), an upstream file
  inventory, not a home-directory listing.
- 43 **true positives**: 19 R1 + 1 R4 `round-43/w1/ExecOracleGkeep|ExecLiveHost` (live host dumps and a
  40-path home census), and 23 R2 rows across `round-37|38|39` that carry the real compositor instance id
  and real PIDs (e.g. `pid=1619`, `pid=3173470`, `round-38/receipts/eventq-live-ss.txt` with 715 rows).
  These are genuine leaks that no round has removed.
- There is **no allowlist, baseline or ignore file** (grep for `ignore|allow|exempt|baseline|suppress`
  finds only `shutil.rmtree(…, ignore_errors=True)` at `:646`). So exit 1 at HEAD is structural, not a
  transient: a *new* real leak is one more line in a 97-line wall, and any integration rule that demands
  `exit 0` from this gate is unsatisfiable today. D3 ("triage the 48 pre-existing findings and mark the
  synthetic fixtures") has no mechanism to triage *with*.

## 3. Scope: D2's remedy ("teach the gate a prose rule") cannot work

`list_tree` restricts to the pathspec `-- .ufo` (`:256`), and the selftest enshrines that
(`e2e-outside-ufo-not-scanned`). Proven: `corpus/knowledge/leak-prose.md` containing prose
`"serial" = "SERIAL0123456"`, a full client dump **and** an ss row produced **zero** findings and left
`files=17098` unchanged (`receipts.txt`, "scope"). D2 records the live serial in three held entries under
`corpus/knowledge/` — those files are never opened by this gate, so a prose rule added inside `.ufo`
still misses all three. The D2 leak is invisible twice: outside the scan root, and (inside it) prose
rather than JSON.

## 4. Impacted axes

- **D1 closure / round-45 w2** — this *is* the missing w2 for the gate: the artifact the round-45 L1
  cited as a passing privacy gate fails 22 of 22 adversarial shapes and is permanently red on its own
  repo. It cannot be carried into round 46 as a verdict source.
- **D3 (death of the registry row, if any)** — a gate whose selftest is green while the repo is red, and
  whose selftest contains no fixture for any of the 19 text misses or any cap, is a conformance gap: the
  selftest measures the scanner's fixtures, not the scanner's discrimination.
- **D2** — the routed remedy is insufficient for the reason in §3; fixing it requires a scope decision,
  not a new regex.
- **Round-46 C1/C2** — unaffected mechanically (neither counter invokes this gate), but L1 must not cite
  `check-session-material.py` exit 0 as a receipt this round, and a seat that copies the gate (or its
  fixtures) into its dir adds findings.
- **Operability of the lane's own quality plane** — a checker that is red at every commit trains every
  seat to skim its output; its value as a leak detector is now near zero.

## 5. Smallest safe correction (one change per defect, each with its required fixture)

1. Count only *successful* decodes against `MAX_OBJECTS`, and emit a finding (or a `truncated=True`
   line) when the cap is reached with `hits == 0` (`:156-160`, `:211`, `:226`).
   Fixture: 20 000 stray `{` + dump → must be flagged.
2. `decode()`: on a NUL in the first 8192 bytes fall back to a `latin-1` scan instead of dropping the
   blob; scan the 16 MiB tail in chunks. Fixtures: NUL-prefixed dump, UTF-16LE dump, dump after 16 MiB.
3. Normalise keys before the prefilter: strip surrounding quotes/spaces, accept
   `class|appClass|initialClass|app_id` × `title|initialTitle|caption|windowTitle`, and parse
   `^\s*"?key"?\s*[:=]` lines so YAML/plain/CSV hit the same predicate; for CSV read the header row.
   Fixtures: shapes 1-7, 9, 11, 13 of §1.
4. `PROC_RE`: allow an optional backslash before the quote and drop the 128-char cap (`:74`).
   Fixtures: escaped ss row, 150-char process name.
5. R4: accept a line after stripping a leading `-`/`*`, an `ls -l` prefix, and surrounding quotes; also
   accept a JSON array of paths. Fixtures: 16-19. Additionally require the paths to name *user content*
   (not a single common upstream prefix) so the omarchy inventory stops matching.
6. Recognise redaction markers as empty (`REDACTED`, `<redacted>`, `[redacted]`, `example`, `SN00000`)
   in `_nonempty`/`_monitor_reason` (`:99`, `:102-106`). Fixture: round-45 `mutants.sh:42` content must
   be clean — otherwise the gate punishes the exact redaction form the lanes were taught.
7. R3: require a monitor signature in the same object (`name` plus one of `width|refreshRate|modes`)
   before flagging, so hardware inventories pass. Fixture: `lsblk -J`.
8. A tracked baseline (`quality/check-session-material.allow`, keyed by path+rule) for the 54 synthetic
   findings at HEAD, so `exit 0` becomes achievable and a *new* leak changes the exit code. Without it,
   items 1-7 cannot be verified against a green tree either.

**Tradeoff the judge must rule on, not a defect to fix blind:** widening the scan root past `.ufo/`
(§3). It changes the gate's stated contract and its selftest expectation, and it would immediately raise
the corpus-wide serial count (D2). Either widen the root and re-state the contract, or record in
QUALITY/SKILL.md that `corpus/`, `quality/` and the fleet root are out of scope — and then stop routing
D2 through this gate.

## 6. Not established

- No live compositor read was needed; no `hyprctl`, `ps`, `ss` or `ls` output enters any fixture.
- The git plumbing (`list_tree`, `iter_blobs`, `cat-file --batch`) was exercised only at
  ~17 k files / 97 findings; its performance and deadlock properties were not attacked here.
- The selftest's 22 cases were run (22/22 pass) but not mutated; this report claims only that they do
  not cover the shapes in §1.
