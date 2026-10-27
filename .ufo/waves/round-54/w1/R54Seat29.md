# R54Seat29 — mechanical baseline (scribe, item 29)

Base: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (`git rev-parse HEAD` at 14:04-03:00; `--show-toplevel`
= `/home/vgpnk/Projects/shokunin/mado-shokunin`). Read-only: no lane tracked edits, no git/jj mutation, no host
reads, no network, no producer runs, no installs/upgrades (tool report §9). All commands below were run with an
explicit `cd` into the lane root or an absolute path.

Axes named for this seat: (A) baseline reproducibility (operability) — can the frozen `receipts/before.txt`
be re-derived by an independent seat? (B) fixture satisfiability (coverage) — do the frozen quote/anchor/range
fixtures admit the pinned bytes? (C) wave-shape conformance — does the dispatched wave match the registration's
declared shape?

Attacked predicates: PRED-C1-r54 and PRED-C2-r54, attacked through their *fixtures and baseline*, not by running
counters (none exists at either rev — §1.3). Distinct input from other seats: I re-derived the baseline receipt
twice (rev-pinned vs filesystem) across a live working-tree mutation **and** a HEAD move, and I tested the
*counting commands themselves* for cross-tool reproducibility. No other w1 report re-ran the baseline receipt.

---

## 1. Baseline receipt (independent, rev-pinned)

### 1.1 Command/output table

| # | command (exact) | output | L1 `receipts/before.txt` | match |
|---|---|---|---|---|
| 1 | `git ls-tree -r --name-only e25149fe -- quality/counters \| grep -c r54` | `0` | `-- r54 counters present: 0` | ✓ |
| 2 | `ls quality/counters \| grep -c r54` (working tree, 14:04) | `0` (grep exit 1) | — | ✓ |
| 3 | `git cat-file -e e25149fe:corpus/knowledge/uwsm-app-environment-r54.md` | rc `128` (absent) | `-- r54 entry present: 0` | ✓ |
| 4 | `git show e25149fe:corpus/README.md \| grep -cE` on the index-row fence (column-0 pipe, backticked `knowledge/` name) | `69` | `-- index count: 69` | ✓ |
| 5 | `git ls-tree -r --name-only e25149fe -- corpus/knowledge \| grep -c '\.md$'` | `69` | `-- knowledge files: 69` | ✓ |
| 6 | `git show e25149fe:corpus/SOURCES.md \| grep -cE '^\| S[0-9]+ \|'` | `311` | `-- registry rows: 311` | ✓ |
| 7 | `git show e25149fe:corpus/SOURCES.md \| grep -oE '^\| S[0-9]+' \| tail -1` | `\| S374` | `-- last row id: S374` | ✓ |
| 8 | `git ls-tree -r --name-only e25149fe -- corpus/lessons \| grep -c r54` | `0` | `-- r54 lesson present: 0` | ✓ |
| 9 | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed` (real 13.874s) | same | ✓ |

`receipts/before.txt` (7 content lines + selftest line) re-derives **7/7 + selftest**, no mismatch.

### 1.2 Gates run at base

```
$ python3 -I quality/check-index.py --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa
MADO_INDEX: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa indexed=69/69 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0

$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado   # fleet-root read-only tool
mado	W04	S370 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/DispatcherTranslator.cpp across scopes
… (25 W-lines, identical set to receipts/census-before.txt; diff shows only the receipt's trailing `exit=0` line)
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

Cross-check of every count above with an independent implementation (`python3` regex over `git show` output,
not `grep`): `registry rows 311 last S374`, `index rows 69`, `counters r54 0` — agrees with the host `grep`.

### 1.3 Predicate commands at base (fail by absence)

```
$ python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev e25149fe…
python3: can't open file '…/quality/counters/c1-r54-errata-truth.py': [Errno 2] No such file or directory
exit=2
$ python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev e25149fe…
python3: can't open file '…/quality/counters/c2-r54-uwsm-entry.py': [Errno 2] No such file or directory
exit=2
```

Both claims are TARGET_MISSED by absence at base, as `claims-frozen.md` states. Nothing here scores them.

---

## 2. HEAD moved during the baseline window (B29-1)

`git rev-parse HEAD` at 14:04 → `e25149fe…`. At 14:12:59 → `350d30e4ec5531f65ce99a57efeb8216f38e678a`
(`round-54: freeze claims, registration, source pins and wave one dispatch`, committed `2026-10-27T14:11:10-03:00`).

Two-rev content table (all rev-pinned, `git show`/`git ls-tree`):

| metric | `e25149fe` (frozen base) | `350d30e4` (freeze commit) |
|---|---|---|
| r54 counters | 0 | 0 |
| `corpus/knowledge/uwsm-app-environment-r54.md` | absent (`cat-file -e` rc 128) | absent |
| README `knowledge/` index rows | 69 | 69 |
| `corpus/SOURCES.md` registry rows / last id | 311 / S374 | 311 / S374 |
| `corpus/knowledge/*.md` blobs | 69 | 69 |
| r54 lesson | 0 | 0 |
| `tools/mado-verify.sh` diff base..HEAD | — | 0 lines (identical) |

`git diff --stat e25149fe..350d30e4` = 11 files, 7494 insertions, **all** under `.ufo/waves/round-54/`
(claims, registration, fetch pins + `SHA256SUMS.txt`, `receipts/before.txt`, `receipts/census-before.txt`,
`w1-spec.json`, `w1-dispatch.json`). So the freeze commit lands no content and the baseline receipt stays valid
at both revs.

Consequence for C2: the three C2 pins are **tracked only at ≥ `350d30e4`** (`git ls-tree -r 350d30e4 -- .ufo/waves/round-54/fetch/`
lists `uwsm-0.27.1-README.md`, `-main.py`, `-uwsm-app.1.scd`, `SHA256SUMS.txt`). PRED-C2 clause (b) names those
pins; a counter invoked with `--rev e25149fe…` (the frozen base named in both frozen files) cannot read them, so
the scored revision must be ≥ `350d30e4`. This is a contract fact, not a seat error — but it means "the frozen
base" and "the revision that can satisfy C2" are different commits.

---

## 3. Distinct failure/input: filesystem baseline counts are not reproducible (B29-2)

Measured time series of the same three counting commands, same lane root:

| time (-03:00) | `ls corpus/knowledge \| grep -c r54` | `ls corpus/knowledge \| wc -l` | `grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md` | `grep -cE '^\| `knowledge/' corpus/README.md` |
|---|---|---|---|---|
| 14:04–14:06 | `0` | `69` | `311` | `69` |
| 14:09 | `1` | `70` | `314` | `70` |

Cause, from `git status --porcelain` + `stat` (HEAD still `e25149fe` at that moment):

```
 M corpus/README.md                       mtime 2026-10-27 14:08:05.218379337  76860 B
 M corpus/SOURCES.md                      mtime 2026-10-27 14:08:20.622355686 275334 B
?? corpus/knowledge/uwsm-app-environment-r54.md   mtime 2026-10-27 14:07:00.456476887   2229 B
?? corpus/lessons/round-54.md                    mtime 2026-10-27 14:08:50.955938019
?? .ufo/waves/round-54/…
```

`git diff --stat` at 14:09: `corpus/README.md | 2 ++`, `corpus/SOURCES.md | 5 +++++` (S375–S377 + one prose
line). These are uncommitted round-54 deliverables written into the lane working tree **while the wave was
running** (wave-1 scribe prompts say "draft … to wave dirs"; no lane-landing seat is registered).

Why this matters for a *baseline* seat: `receipts/before.txt` is correct at the rev, but any w2 seat that
re-runs the baseline with the filesystem commands (`ls`, `grep`, `wc` — the form L1 used in the receipt's own
headings) will read 314/70/1 and report a false mismatch against 311/69/0. The receipt is only reproducible
rev-pinned:

```
git show <rev>:corpus/SOURCES.md | grep -cE '^\| S[0-9]+ \|'
git show <rev>:corpus/README.md  | grep -cE '^\| `knowledge/'
git ls-tree -r --name-only <rev> -- corpus/knowledge | grep -c '\.md$'
git ls-tree -r --name-only <rev> -- quality/counters | grep -c r54
python3 -I quality/check-index.py --rev <rev>
```

Recommendation (report-only, L1 decides): the baseline receipt should print the rev it was taken at and the
counting form (`--rev` vs `--root`); w2 baseline re-runs should use `--rev`/`git show` only.

**Second reproducibility trap, same class (B29-3):** the host `grep` is **not GNU grep** —
`grep --version` → `grep (pi-uu-grep) 0.2.0`. Every published receipt in this lane that says "`grep -c`" is
therefore tool-dependent. I cross-checked the four counts above with `python3` regex and they agree, so no
receipt is falsified *here*; but a w2 seat on a GNU-grep host must not assume byte-identical behaviour for
patterns containing `\|` or backticks. (`git 2.56.0`, `python3 3.14.8`, `bash 5.3.20`, `sha256sum 0.8.0`.)

---

## 4. Independent confirmation of frozen-fixture defects (my numbers)

I re-derived these myself; they overlap Seat14's F1/F3 and Seat09's F1 where noted. All judges are mine
(`python3 -I`, stdlib): **J0** exact byte substring; **J1** whitespace runs collapsed to one space on both
sides; **J2** J1 plus `*`/`` ` `` stripped from the pin.

### 4.1 C1: the judge sentence forbids the normalization the pins need

```
== frozen C1 quotes vs round-52 pins, per judge ==
P19 Hyprland-ConfigActions.cpp:1554-1558   J0=MISS J1=HIT
P20 Hyprland-ConfigActions.cpp:1576        J0=HIT  J1=HIT
P21 Hyprland-legacy-DispatcherTranslator.cpp:619-622  J0=MISS J1=HIT
P22 Hyprland-legacy-DispatcherTranslator.cpp:573-574  J0=MISS J1=HIT
```

Under the registration's literal rule ("normalization of interior newlines ONLY where the frozen quote itself
carries a newline; P19/P21/P22 are single logical lines") → **quotes=1/4 → TARGET_MISSED**. Under J1 →
**4/4 → TARGET_MET**. Same fixture, opposite verdict; the counter's author picks the verdict.

The anchors themselves are **exact**, so the defect is only in the judge sentence, not the coordinates:

```
== minimal physical span of each frozen quote (J1) vs stated anchor ==
P19 stated :1554-1558 → minimal (1554,1558)  equal=True   [1555 blank, 1556/1557 indented branch]
P20 stated :1576      → minimal (1576,1576)  equal=True
P21 stated :619-622   → minimal (619,622)    equal=True   [620 blank]
P22 stated :573-574   → minimal (573,574)    equal=True
```

Pin bytes (`sed -n`): `ConfigActions.cpp:1554` `sendKeyboardMods(modMask, 0, 0, 0);` / `1555` blank /
`1556` `if (S.m_passPressed == 1) {` / `1557` `if (!isMouse)` / `1558` `sendKeyboardKey(…PRESSED);`;
`DispatcherTranslator.cpp:619` `auto result = sendshortcut(modifiedArgs);` / `620` blank / `621`
`if (keyState == 2 && result.success)` / `622` `result = sendshortcut(modifiedArgs);`; `:573` `if (!keycode)` /
`:574` `return {.success = false, .error = "sendshortcut: key not found"};`.

### 4.2 C1: committed entry table vs frozen table — no drift

Cell-for-cell, backtick delimiters included: for P19–P22 the entry's `Quote` cell is **byte-identical** to the
registration's `Quote` cell (`quote_equal=True` ×4), and `Pin:anchor` splits at the last `:` to exactly the
frozen pin and anchor (`Hyprland-ConfigActions.cpp` `:1554-1558`; `:1576`; `Hyprland-legacy-DispatcherTranslator.cpp`
`:619-622`; `:573-574`). Only structural difference: the frozen table has separate `Pin file` / `Anchor` columns
wrapped in backticks; the entry has one combined backticked `Pin:anchor` cell. A counter must therefore strip
backticks and split on the last `:` — worth stating in the counter contract.

### 4.3 C2: two of the three frozen quotes are not admitted at their stated locations

```
== frozen C2 quotes vs round-54 pins ==
S375 uwsm-0.27.1-README.md 117-118   J0=MISS J1=MISS@117-118  J1@any=HIT   minimal range from 117 = 117-119  → STATED RANGE TOO SHORT
S376 uwsm-0.27.1-uwsm-app.1.scd 60   J0=MISS J1=MISS          J2@any=HIT   (pin carries `*uwsm-app*`)
S377 uwsm-0.27.1-main.py 3714        J0=HIT  J1=HIT           J1@any=HIT   unique at 3714
```

Pin bytes (`sed -n '117,119p'`): `117` `- Difference between environment state before and after preparation is
exported` / `118` `  into systemd user manager (and D-Bus activation environment if reference D-Bus` /
`119` `  implementation is used)`. The frozen quote needs three lines; registration says `117-118`.

Pin byte (`uwsm-app.1.scd:60`): `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon`.
The frozen quote is `uwsm-app client sends arguments to uwsm's app daemon via a pipe.` — it drops the two
emphasis asterisks. No whitespace-only normalizer admits it; only J2 (markdown-marker stripping) does. If the
counter strips markers to admit S376, the same normalizer must be declared for C1 (where it changes nothing) —
otherwise the two claims use different "verbatim" judges inside one freeze.

Pin digests match `SHA256SUMS.txt` for all three (`1874fb83…`, `3982503d…`, `7dd63632…`); the defect is textual
locators, not bytes. All four round-52 pin digests also match the frozen table (`a83abeb5…`, `746c6f51…`,
`8d8f35fc…`, `7248cbb8…`).

---

## 5. Landed C2 content vs the frozen clauses (measured 14:09–14:12)

Working-tree state (uncommitted, HEAD `350d30e4`): entry `corpus/knowledge/uwsm-app-environment-r54.md`,
lesson `corpus/lessons/round-54.md`, `M corpus/README.md`, `M corpus/SOURCES.md` (S375–S377).

### 5.1 Clause (b) — row quote cells are paraphrases

| row | landed quote cell (`corpus/SOURCES.md:325-327`) | J0@loc | J1@loc | J1@any | J2@any |
|---|---|---|---|---|---|
| S375 | `Difference before and after preparation is exported into systemd user manager` | MISS | MISS | **MISS** | **MISS** |
| S376 | `uwsm-app client sends arguments to uwsm's app daemon via a pipe` | MISS | MISS | MISS | HIT |
| S377 | `unit name includes desktop and command substrings and random hexadecimal text` | MISS | MISS | **MISS** | **MISS** |

S375 and S377 occur **nowhere in their pins under any judge** (S375 drops `between environment state`; S377 is a
prose paraphrase of a code line). S376 survives only under J2. So clause (b)'s quote leg fails for all three rows
as landed. (Confirms Seat09 F1 independently; my added fact is that S375/S377 fail even under markdown-stripping.)

Row shape is otherwise correct: all three rows `kind` docs/docs/code, `tier A`, `status mined`, `opened
2026-10-27`, `recheck on-release`, `used-by corpus/knowledge/uwsm-app-environment-r54.md`, URL carrying
`0727985c9bae655bda488f87f99ea69a6ac1c003`.

### 5.2 Clause (a) — provenance trio present, token leg ambiguous

Entry lines 1–3 are `source:`, `verified-at: 2026-10-27…`, `recheck: on-release…` (trio, correct order). But the
`source:` line reads `source: S375–S377 — …` with an **en dash range**: literal token `S376` is **absent from
the source line** (present only in the body, line 11). A counter scanning the `source:` line for the three ids
fails clause (a); one scanning the whole entry passes. README index row is present — index-row fence match at
`corpus/README.md:82` (the string also appears once more, in the round-54 bullet at `:121`) — and
`check-index.py --root .` → `indexed=70/70 … coverage=10.0000/10`, exit 0.

### 5.3 Clause (c) — host joins

None of the eight frozen host strings appears verbatim in the entry (`~/.local/share/omarchy/default/hypr/autostart.conf:1…:6`,
`~/.config/hypr/bindings.conf:2`, `~/.local/share/omarchy/bin/omarchy-toggle-idle:9` → **0** exact hits). Only
basenames appear: `bindings.conf:2`, `omarchy-toggle-idle:9`, `autostart.conf:1` (as `autostart.conf:1-5`).
Exact-string matcher → clause (c) fails; basename matcher → 3 joins, passes. The freeze does not say which.

### 5.4 The entry now disputes the frozen host set (report verbatim)

The entry was rewritten at `2026-10-27 14:12:23` (2229 → 2632 B) and now asserts:

> "The frozen registration's host set overstates the autostart range: direct file inspection shows
> `autostart.conf:1-5` contain five `uwsm-app` declarations, while `:6` launches the polkit agent; the monitor
> watcher invocation is at `:9`, not `:6`. This entry therefore claims only the observed five `uwsm-app` lines …"

Two independent facts for the canonical judge, not a seat verdict: (i) the paragraph rests on **host file
inspection**, which this round's seat fence forbids and the C2 counter cannot read — the claim is unfalsifiable
by PRED-C2 as frozen; (ii) if the paragraph is right, the frozen host set (`autostart.conf:1`–`:6`, six
`uwsm-app` lines) is wrong, and the C2 fixture inventory is defective independently of the counter. I cannot
verify either way inside my fence (no host reads); flagged for sentinel/L1.

---

## 6. Wave-shape conformance (B29-4)

`w1-spec.json` items = **37**; roles: `executor 10, scribe 7, scout 4, connector 2, reviewer 7, critic 3,
mutation-tester 2, sentinel 1, simplifier 1`. `w1-dispatch.json` `counts` = `{spawn: 37, resume: 0, total: 37}`;
`w1/swarm-registry.json` members = 37.

Registration says: "Attack share = reviewer 5 + critic 3 + mutation-tester 2 = 10/37 (27%)". Actual attack share =
`7 + 3 + 2 = 12/37 = 32.4%`. The registration also lists "sonic runs mechanical baseline receipts" (no `sonic`
role exists in the spec; item 29 is a `scribe` doing that job) and does not mention the one `simplifier`.
Arithmetic that does hold: 37 + 32 = 69 = declared round total.

---

## 7. Harm watch (frozen) — status

| watch item | frozen target | measured |
|---|---|---|
| `bash tools/mado-verify.sh --selftest` | 460/460 | `460/460 assertions passed`, 13.874s, run 14:06 (pre-drift; the suite is hermetic — its own header: "no substrate reads" — and `tools/mado-verify.sh` is byte-identical at `e25149fe` and `350d30e4`, `git diff --stat` → 0 lines) |
| navigation counter | 69/69 → 70/70 after the C2 index row, never fewer | `--rev e25149fe` → `indexed=69/69 coverage=10.0000/10` exit 0; `--root .` (landed row) → `indexed=70/70` exit 0 |
| sources census exit 0 | exit 0 | `mado ok …corpus/SOURCES.md`, exit 0; warning set identical to `receipts/census-before.txt` (diff = only the receipt's trailing `exit=0`); no new W/E code from S375–S377 |
| no config/compositor/service/sibling writes | — | none by me; `git status` shows only peer-authored round-54 content + wave dirs |
| wave-dir reports only | — | this report only, at `.ufo/waves/round-54/w1/R54Seat29.md` |

`/tmp` footprint: my `--selftest` run left no `w5-mado-m52-selftest.*` directory (newest existing one is
`11:10`, ~3 h before my run); I wrote nothing to `/tmp`.

---

## 8. Findings (report-only; no predicate or frozen file edited)

| ID | class | finding | evidence |
|---|---|---|---|
| B29-1 | baseline/freeze | HEAD moved `e25149fe` → `350d30e4` at 14:11:10 during the wave; the freeze commit adds only `.ufo/waves/round-54/` files, so the content baseline is unchanged, but C2's pins exist only at ≥ `350d30e4` while both frozen files name `e25149fe` as the base | §2 `git diff --stat e25149fe..350d30e4` |
| B29-2 | baseline reproducibility | uncommitted lane writes at 14:07–14:08 make filesystem baseline counts non-reproducible (69/0/0/311 → 70/1/1/314); `receipts/before.txt` is correct only rev-pinned | §3 time series, `git status`, `stat` |
| B29-3 | tooling | host `grep` is `pi-uu-grep 0.2.0`, not GNU grep; published `grep -c` receipts are tool-dependent (all four counts re-derived with `python3` agree, so nothing is falsified here) | §3 |
| B29-4 | freeze completeness | registration's attack share (10/37, 27%) ≠ dispatched spec (12/37, 32.4%); `sonic` role absent, `simplifier` unlisted | §6 |
| B29-5 | judge satisfiability (C1) | literal judge → quotes 1/4; whitespace-collapse judge → 4/4; anchors exact in both | §4.1 |
| B29-6 | judge satisfiability (C2) | S375 locator `117-118` too short (needs `117-119`); S376 quote omits the pin's emphasis markers (`*uwsm-app*`), so only a markdown-stripping judge admits it | §4.3 |
| B29-7 | landed content | S375/S377 quote cells are paraphrases (absent under every judge); S376 passes only under markdown-stripping; clause (a) `source:` line carries `S375–S377` (no literal `S376`); clause (c) has 0 frozen host strings verbatim, 3 basenames | §5.1–5.3 |
| B29-8 | out-of-fence claim | the landed entry asserts a direct host-file inspection and disputes the frozen host set (`autostart.conf:1-5` five lines, `:6` polkit, watcher `:9`); unverifiable by the C2 counter and outside this round's seat fence | §5.4 (verbatim) |
| B29-9 | C1 control inventory (attack seed for w2) | the committed round-52 `SHA256SUMS` records **absolute** host paths (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/…`), and no frozen C1 control mutates pin **bytes**; a counter that hashes the sums file's absolute paths never reads the scored tree's pins and still passes C1-CTL-1…6 | `cat .ufo/waves/round-52/fetch/SHA256SUMS`; registration control table |

## 9. Out of scope / not verified

- Running either counter (neither exists at `e25149fe` or `350d30e4`); judging PRED-C1/C2 verdicts.
- Host reads of `autostart.conf`, `bindings.conf`, `omarchy-toggle-idle` (forbidden); upstream tag identity of
  `0727985c…` (network forbidden) — internal consistency only.
- C1/C2 control execution on mutated trees (executors' scope); `w2` dispatch.
- Whether the uncommitted entry/lesson/rows stay as measured (they changed twice during this window).
- Tool report: no installs or updates; tools used read-only — `python3 3.14.8`, `git 2.56.0`, `bash 5.3.20`,
  `sha256sum 0.8.0`, `grep (pi-uu-grep) 0.2.0`. No `sudo`, no package queries.

## 10. Scratch

`/fast/scratch/hyaku/mado-r54/R54Seat29/` held `baseline_check.py`, `c2_matrix.py`, `c1_cells.py`,
`census-now.txt` (all stdlib/read-only); removed before yield. No writes outside this report and that directory.
Read-only git only (`rev-parse`, `show`, `ls-tree`, `cat-file -e`, `diff`, `log`, `status`, `reflog`); no jj, no
commit/push, no subagent dispatch.

Report trailer: `.ufo/waves/round-54/w1/R54Seat29.md`
