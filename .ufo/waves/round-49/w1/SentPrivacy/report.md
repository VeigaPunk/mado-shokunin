# SentPrivacy — privacy of the round-49 receipts

Seat `SentPrivacy` (sentinel, leaf), mado round 49 / wave w1 (BUILD), base `03e4ae76aff7a4be59cb69970dd553baa319695a`,
lane tip at scan time `5f37c1b87b3ce5e438d19284e32b2e46fd548a92`. Assignment: which host material this round's receipts could
carry (bind exec commands with home paths and private script names, bind descriptions, device names, keymap text, ls/home
listings), whether `quality/check-session-material.py` (v2, sha256 `82c9053a…2dfa6f`, 1643 lines, selftest `passed=69/69`) and
`w1/ExecSessionShapes/check-session-material.py` (v3 draft, in flight: measured at sha256 `2c72df3f…0f9f` and re-measured at `ffdc9d62…bb61`, identical fixture verdicts) catch each class, and which
classes they miss.

Everything below is measured. Every probe value is synthetic (`example`, `synthetic-*`, `Fake`) or runtime-derived and masked;
no host value is printed here. Tool installs/upgrades: **none** (no package or tool transaction was run).

---

## 0. Verdict

- **The live instance already exists.** `.ufo/waves/round-49/w1/ScrSkill/receipts/binds-raw.json` is the complete
  `hyprctl binds -j` capture — 90,401 bytes, sha256 `9a47199e…00c779`, i.e. the *same* blob `ExecBindsLive` explicitly
  declined to commit (`binds-shape.txt:6,8`). It carries 192 bind records, **136 distinct non-empty `arg` values** (10 with
  URLs, 4 with shell chains, 9 with quoted regexes), **190 non-empty descriptions** (185 distinct) and **two `switch:on/off:`
  keys whose suffix is a non-empty switch device name**. Both gates report **0 findings** on it (v2 `scan_blob` → `[]`;
  v3 `scan_blob` → `[]`). Standing rule: input-device names and the config plane stay shape-only — this blob is neither.
  **S2.**
- **The gate catches none of the 16 craft-plane shapes this round's seats can produce** (`material_missed=16`,
  `material_caught=0`; `probe.txt`), while its four historic positives still fire. Its rules are the round-45 shapes — client
  dump, `ss` row, monitor identity, a *bare* home listing — and this round's plane (binds, keysyms, keymap, input config)
  produces none of them. **S2 for the instrument** (published privacy predicate, `corpus/QUALITY.md`).
- **The v3 draft fixes the scope defect and 4 of the 16 shapes**, but still reports nothing on the live raw-binds blob and its
  own declared-limits paragraph does not name the bind record, keymap text or input config as uncovered.
- **Scope:** v2's default `.ufo` excludes both claim deliverables (`tools/mado-keysym.py`,
  `corpus/knowledge/hyprland-bind-key-match-r49.md`) and the C2 counter (`quality/counters/`); measured on a fixture repo of
  the round's layout, v2 read `files=1` of 6 and returned `findings=0` while two identical caught payloads sat in `tools/` and
  `corpus/` (`scope-test.txt`). v3 defaults to `all` (`check-session-material.py:217`) — fixed.
- **Red at base, delta 0**: v2 `findings=159` at both base and tip under `.ufo` (`167` under `--scope all`), same per-rule
  tally, so "gate passes" is not an available signal for the freeze (`gate-base-and-tip.txt`).
- Per missed class, S3 — except the raw-binds instance above, which carries a device name.

---

## 1. Method

1. Read v2 (rules R1–R6, marker/waiver W1–W4, scope) and ran its selftest (`passed=69/69`); read v3's R7–R9 and its
   declared-limits paragraph.
2. Scored 24 synthetic fixtures — 16 in this round's carrier shapes, 4 controls the seats are told to produce, 4 historic
   positives — through each gate's own `scan_blob()` (`probe.py` → `probe.txt`, `probe-results.json`, `v3-scan.txt`, `v3-scan-account.txt`). The four
   positives are assembled from parts, as the gates' selftests do, so the probe file is itself clean under both gates.
3. Tested scope on a throwaway git fixture laid out like the lane (`scope-test.sh` → `scope-test.txt`).
4. Tested the waiver namespace both ways (`waiver-test.sh` → `waiver-test.txt`).
5. Ran v2 at base and tip, both scopes (`gate-base-and-tip.txt`); censused the live round tree with v2's rules plus a
   per-class counter (`census.py` → `census.txt`, `census.json`); scored the live raw-binds capture with both gates.
6. Re-ran the census and v3 scan at the end of the seat's run; the tree grows while seats write, so every total is a
   snapshot.

Text encodings: `P*` = material, `K*` = receipt the seats are told to produce (must be clean), `C*` = historic positive.

---

## 2. Class table — what this round can carry × what the gates see

| id | class (no values) | round-49 carrier | v2 | v3 |
|----|-------------------|------------------|----|----|
| R49-01 | `binds -j` object with a non-empty `arg` (exec command) carrying `~/…`, `/home/…` or a private script name | **live**: `ScrSkill/receipts/binds-raw.json` | **MISSED** (P01) | **MISSED** (P01, live blob) |
| R49-02 | the same rows projected into a Markdown/TSV table (`modmask \| key \| dispatcher \| arg`) | a de-JSON'd capture | **MISSED** (P02) | **MISSED** (P02) |
| R49-03 | bind `description` free text (private project/script names) | **live**: 190 non-empty descriptions | **MISSED** (P03) | **MISSED** (P03) |
| R49-04 | `key` field in `switch:on:<name>` / `switch:off:<name>` form — a *device name*, not a keysym | **live**: 2 such keys | **MISSED** (no rule reads a JSON value by key) | **MISSED** |
| R49-05 | `submap` values (user-chosen strings) | shape receipts keep `submap`; empty on this host | **MISSED** | **MISSED** |
| R49-06 | `devices -j` element (`name` + `address` (+`layout`)) — input-device identity | C2 fallback; `input.conf` `device { name = … }` | **MISSED** (P04, P06) | **MISSED** (P04, P06; v3 names this as future R10/R11) |
| R49-07 | device names in prose (a "keyboard list" sentence) | a C2 note on which device has which layout | **MISSED** (P18) | **MISSED** (P18) |
| R49-08 | compiled keymap text (`xkb_keymap { … }`) | any seat pasting the 73 KB compile output | **MISSED** (P15; K03 clean by design) | **MISSED** (P15) |
| R49-09 | `compile-keymap --verbose` diagnostics carrying `~/.config/xkb` include paths | the C1/C2 include-order evidence | **MISSED** (P05) | **CAUGHT** (R7 `diag`) |
| R49-10 | `hyprland.conf` bind lines as text (`bind = MODS, KEY, exec, ~/…`) | C2 examples pasted verbatim | **MISSED** (P14) | **MISSED** (P14) |
| R49-11 | `input.conf` content (`kb_layout`, `kb_options`, per-device blocks) | host-keymap provenance note | **MISSED** (P06) | **MISSED** (P06) |
| R49-12 | inline absolute home paths in prose/commands (`$ git -C /home/…`, `path=/home/…`, `…:LINE: text`) | every seat receipt that shows a command | **MISSED** (P09) | **PARTIAL** — `grep -n` prefix and `ls` header caught (R7), `path=/home/…` and prose still missed (P09 caught; the live digest line I-2 missed) |
| R49-13 | `~`-written / `$HOME`-masked paths (the lane's own privacy practice) | masked receipts | **MISSED** (P08) | **MISSED by design** (P08) |
| R49-14 | flat listing: one directory header + data rows | a fixture/applications inventory | **MISSED** (P10) | **CAUGHT** (R7 `header`) |
| R49-15 | `ls -l` owner/group **account name** columns (no `/home` at all) | any `ls -l`/`stat` receipt | **MISSED** (P07) | **CAUGHT** by R8 when the account resolves (`--account` or invoking account; inert otherwise — measured both modes, `v3-scan-account.txt`) |
| R49-16 | cache text / cache-file paths (`~/.cache/<tool>`, `--title=`, `--dir=`) | the M48-10 operator-cache digest; a terminal-resolver cache | **MISSED** (P11) | **PARTIAL** — two column-0 cache fields caught (R9), a `path=… size=…` digest line missed (live I-2) |
| R49-17 | paths rooted outside `/home` (`/fast/scratch/…`, `/run/user/<uid>/…`) | every counter run and every sandbox receipt | **MISSED** (P16) | **MISSED** (P16) |
| R49-18 | process table in a non-`ss` dialect (`ps`, `pgrep -a`, `strace` ladders) | "no process started" proofs, `SentHost` traces | **MISSED** (P17) | **MISSED** (P17) |
| — | `>10` distinct **bare** `/home/…` lines; `class`+`title` JSON; `ss` `users:((` row; `serial`+identity; serial-shaped token | round-45..48 residue | **CAUGHT** (C01–C04) | **CAUGHT** (C01–C04) |

Probe totals: **24 fixtures, 16 material — v2 0/16 caught, v3 4/16 caught (`P05 P07 P09 P10`); 4 controls caught; 4
intended-clean receipts clean under both** (`probe.txt`, `v3-scan-account.txt`).

The desired-clean receipts (`K01` shape-only binds with a sha256 header, `K02` keysym↔keycode table, `K03` compiled keymap,
`K04` keysym header fragment) score `NONE` — correct: they carry no host identity. The risk is the *unmasked* variant one edit
away (`P01`, `P04`, `P08`), and neither gate tells the two apart.

---

## 3. Instrument defects (measured)

**D-A v2's default scope excludes both claim deliverables** — `--scope ufo` default (`quality/check-session-material.py:1606`),
paths `:790`. Fixture repo of the round's five trees: default `files=1 findings=0`; `--scope all` `files=6 findings=2` on
payloads the default cannot see (`scope-test.txt`). v3 closes this (`DEFAULT_SCOPE = "all"`, `:217`).

**D-B R4 is one shape, one root, one threshold.** `HOME_PATH_RE` (`:168`) matches only a line that is *only* an absolute
`/home/<user>/…` path; `scan_home_listing` (`:319-329`) skips any line containing whitespace (`:324`) and fires above
`DEFAULT_HOME_LIMIT = 10` (`:162`). Measured: 12 inline `path:LINE: text` lines → 0 (P09); 12 `~/.config/…` lines → 0 (P08);
12 `ls -l` rows with owner columns → 0 (P07); one `ls -lR` header + 12 data rows → 1 distinct path, 0 (P10); `/fast/scratch/…`
listing → 0 (P16); `/home/…` inside a Markdown table → 0 (P02). v3's R7 covers four *anchored* forms (`grep -n` prefix,
`ls` header, lowercase-program quoted diagnostic, `ls -l` row) and R8 the owner column, so it catches P05/P07/P09/P10 — but a
`path=/home/… size=…` digest line and a Markdown table cell are still invisible (both live instances, §4).

**D-C no rule reads the binds object.** R1 requires `class`+`title`; R3 requires `serial`+identity; R4 is line-shaped; R5 is
serial-shaped; v3 adds R7–R9 (path forms, owner column, cache fields) — none of them is keyed on a JSON field. So
`{"modmask":…,"key":…,"dispatcher":"exec","arg":…,"description":…}` is invisible in both gates (P01), and so is
`"key": "switch:on:<name>"` and `"submap"`. v3's declared-limits paragraph (`check-session-material.py:185-198`) enumerates
what it still misses and does **not** name the bind record, keymap text or input config; the file has zero occurrences of
`keybind`/`"arg"`/`bind record`.

**D-D the waiver namespace makes a real-account fixture unwaivable — correctly.** W4 (`:572`) refuses a `kind=fixture` marker
whose home user is not reserved (`SYNTH_HOME_USER_RE`, `:226`). Measured both ways: `/home/example/…` + marker + registry →
`WAIVER … kind=fixture`, `findings=0`; the same file under the real account → `WAIVER_REJECTED … reason=value-not-synthetic:home-user-not-synthetic`,
`findings=1`, rc 1 (`waiver-test.txt`). Freeze consequence: seat fixtures must use a reserved user, and a fixture that leaks in
an *inline* form needs no waiver at all — the marker path cannot be used to notice it either.

**D-E red at base, delta 0 at tip.** `files=22012 findings=159` / `files=22019 findings=159` under `.ufo`;
`files=22278 findings=167` / `files=22285 findings=167` under `--scope all`; identical per-rule tally
(`R1=38 R2=38 R3=58 R4=3 R5=22`, waived 3 of 1 file) at both revisions (`gate-base-and-tip.txt`). A new true positive is
indistinguishable from the 159 — and the round's current receipts add none, not because they are clean but because every
class they carry is missed.

**D-F untracked receipts are invisible by construction.** Both gates read `git ls-tree -r <rev>` blobs (`:9-15`, `:714`); during
w1 every seat receipt is untracked. The census below therefore uses each gate's own `scan_blob()` on the files, which is
strictly stronger than the invocation the L1 will run.

**D-G inherited, unchanged (not re-claimed):** 16 MiB prefix for every rule (`MAX_TEXT`, `:160`, `decode()` `:333`); binary
blobs skipped (NUL in first 8 KiB); no secret-shape rule (a URL/credential-shaped `arg` would be caught by neither gate);
R1 blind to `jq -r` projections of `class`+`title`; R2 blind to `ps`/`pgrep`. Round-48 `PR-01..PR-19` already carries the
reasoning; the round-49 census shows the same carriers (`/fast/scratch` paths, owner columns) in this round's receipts.

---

## 4. Live measurement (counts and classes only; snapshot at end of seat)

`census.txt` / `census.json` over `.ufo/waves/round-49/`:

- `files=652` (602 text-scannable); `home_path_files=72`; `home_path_lines=286`; `distinct_home_paths=10`;
  `tilde_files=33` / `tilde_lines=94`; **account-name occurrences `277`**; files carrying bind-record JSON keys `23`,
  `"address"` keys `3`, keymap text `8`
  (most of those are fetched Hyprland/xkbcommon *sources*, not host material).
- **v2 verdict on the same bytes: `gate_files=1`, `gate_findings=3` — and that one file is the v3 gate draft itself**
  (`w1/ExecSessionShapes/check-session-material.py`, its own R1/R2/R3 selftest constants). Every other file, including the raw
  binds capture, is clean. (v3 over the same tree at `ffdc9d62`: the same single file, `v3-scan.txt`.)
  The round therefore already has one producer-side obligation for the L1: the v3 draft's constants need a marker whose W4
  check passes (`kind=fixture` with reserved values — `kind=gate-copy` cannot apply, it is not byte-identical to the gate).
- Path categories (masked): lane/project paths 284 + 55 bare `/home/<user>`, reserved-fixture paths 21, `~/.config/…` 18,
  `~/.local/…` 15, `~/.omp/…` 4, `~/.cache/…` 4, `~/.xkb/…` 4. (`share`/`state`/`xkb`/`XCompose` tops are masked scratch
  placeholders `…/home/.local/share` in `SentHost`/`ExecMutantSandbox` receipts — the correct form.)
- My own seat dir is clean under both gates (0 findings; re-checked after every receipt was written).

Three live instances, cited by shape:

- **I-1** `.ufo/waves/round-49/w1/ScrSkill/receipts/binds-raw.json` (90,401 B, sha256 `9a47199e…00c779`) — the *whole*
  `hyprctl binds -j`: 192 records, 24 dispatchers, 136 distinct non-empty `arg` values (10 URLs, 4 shell chains, 9 quoted
  regexes), 190 non-empty descriptions (185 distinct), 2 `switch:on/off:<name>` keys with a non-empty device name, 0 `submap`
  values, 0 `/home/` and 0 `~/` in args. Same sha256 as the blob `ExecBindsLive` refused to commit (`binds-shape.txt:6,8`).
  The owning seat's own report describes the read as "192 binds, tallied" (`w1/ScrSkill.md:22`), so this is working material
  left in the receipts directory with no `.synthetic` sidecar and no waiver-registry line. **v2 → `[]`, v3 → `[]`** (with
  `account` resolved as well).
- **I-2** `w1/ExecMutantSandbox/receipts/d-operator-cache-digest.txt:1,4,5` — the operator-owned cache-file path
  (`~/.cache/<terminal-resolver>`) three times with `size`/`mtime`/`inode`/`dev`/`sha256` (M48-10's file). v2 clean; v3 clean
  (the `path=…` form is not one of R7's four anchors, and it is not R9 cache text).
- **I-3** `w1/ScoutShokuknow/quarantine-slice.md:5` — a second tool's cache path (`~/.cache/<tool>/status.json`) inside a
  Markdown table cell. v2 clean; v3 clean (Markdown cell is not an anchor).

Producer-side positives to freeze as the pattern: `ExecBindsLive/receipts/binds-shape.txt:8-9` states the raw JSON is *not*
committed because it "carries dispatcher args, descriptions and the switch device name", keeps only
`key,keycode,modmask,mouse,catch_all,submap` + the dispatcher name, masks the switch device to `<name>` (lines 12, 177-178), and
has zero `"arg"`/`"description"` occurrences (grep count 0 across its three receipts); `SentHost` strace ladders carry only
scratch-rooted synthetic homes.

---

## 5. Exploit path (read-only; no host value used)

1. A C2 seat needs a committed live receipt whose stated values the entry repeats, and the cheapest artifact is the raw
   `hyprctl binds -j` — it is already on disk as I-1, 90 KB, with the exact sha256 another seat published.
2. The L1 commits it under `.ufo/waves/round-49/w1/…` (default scope), runs the gate at the tip: `findings=159`, unchanged
   from base; v3 likewise returns nothing for that file.
3. The published blob lists what every key does on this host (136 distinct argument strings, 190 descriptions), includes two
   switch-device names, and — because `bind = MODS, KEY, exec, …` args are the operator's own command lines — the shape of
   every private script, URL shortcut and regex macro in the desktop config.
4. Same for a `devices -j` paste (P04) if a seat needs per-device layout, and for `input.conf` text (P06) that a provenance
   note already cites by line (`bind-keys.txt:6`).
5. Nothing in either gate reports; the freeze records a green delta.

Impact: an inventory of the host's keybinding plane and device identity in a public repo, with both privacy predicates
silent — and, unlike the round-48 classes, this one is already realised on disk.

---

## 6. Smallest remediation (ranked; each checkable)

1. **Decide I-1 now, before it is tracked**: either drop it for the shape+counts artifact `ExecBindsLive` already wrote
   (`binds-shape.txt`, 23,881 B, no args/descriptions, switch name masked) and keep the 90 KB blob out of the repo, or reduce
   it to counts + sha256. One `git status` at commit time is the whole check.
2. **Freeze the predicate as a delta with a recorded baseline**, not an exit status: `findings(rev) \ findings(base)` with the
   base tally (`R1=38 R2=38 R3=58 R4=3 R5=22`, `findings=159` `.ufo` / `167` all) in the freeze. One wrapper around `run()`.
3. **Add `R10_BIND_RECORD`** — a JSON object carrying `"modmask"` (or `"keycode"`) together with a non-empty
   `"arg"`/`"description"` is a keybind record: count objects, never values. Fixture: I-1 must go red, `K01` must stay green;
   one extra green case for a `binds -j` projection that keeps only the six shape fields.
4. **Add `R11_DEVICE_IDENT`** — object with `"name"`+`"address"` (+`"layout"`) and the `switch:(on|off):<name>` form in a `key`
   value (fixtures P04, P18). v3's own limits paragraph already reserves this number; the binds blob shows it is not
   hypothetical.
5. **Widen R7 to the unanchored path forms**: a `key=/home/…`/`path=/home/…`-style field (I-2) and a path in a table cell
   (I-3), or declare Markdown/field-prefix forms out of scope explicitly. Fixtures: I-2 and I-3 shapes red; the `~`-form and
   a path quoted in a prose sentence stay green (the lane's masking practice).
6. **Producer-side, free**: `submap` masked in the shape receipt (empty today, so a no-op but cheap); the C2 counter spec
   phrased as "shape + counts", not "stated values".
7. **Keymap/config text (R49-08/10/11)**: either one rule for `xkb_keymap {` plus an `input {` block with a `device { name = …`
   subsection, or an explicit out-of-scope sentence in the freeze — today both are silent and both are one paste away.

---

## 7. Receipts (all under `.ufo/waves/round-49/w1/SentPrivacy/`)

| file | what it shows |
|------|---------------|
| `probe.py`, `probe.txt`, `probe-results.json` | 24 synthetic fixtures through v2's `scan_blob()`: 16 material (all missed), 4 historic positives (all caught), 4 intended-clean receipts (clean) |
| `v3-scan.txt` | v3's snapshot sha256/rules/default scope, v3 on the live raw-binds blob (`[]`), plus a full v3 scan of the round tree and of this seat |
| `v3-scan-account.txt` | v3's 16 material shapes in both `account` modes (R8 inert vs resolved): 4/16 caught in each, the same four fixtures |
| `scope-test.sh`, `scope-test.txt` | fixture repo of the round's five trees: v2 default `files=1 findings=0`, `--scope all` `files=6 findings=2` |
| `waiver-test.sh`, `waiver-test.txt` | reserved-user fixture waived; the identical shape under the real account name refused `value-not-synthetic` |
| `census.py`, `census.txt`, `census.json` | live round tree: 652 files (602 text-scannable), 72 with absolute home paths (286 lines, 10 distinct), 277 account-name occurrences, v2 `findings=3` (the v3 draft's own constants) |
| `gate-base-and-tip.txt` | v2 at base and tip, `.ufo` and `all`: 159/159 and 167/167, same per-rule tally |

Scratch `/fast/scratch/hyaku/mado-r49/SentPrivacy/` is deleted at the end; nothing here cites a scratch path as evidence.
