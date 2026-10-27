# R54Seat08 — source/lesson prose recon (C2 uwsm pins + frozen quotations + host-join limits)

- Seat: `R54Seat08`, role `scribe`, wave `w1`, assigned item **8** (`w1-spec.json` item 8 prompt: verify opened
  uwsm pins and frozen C2 quotations from committed files, identify host join evidence limits, report exact
  quote/lines; do not draft committed entry).
- Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`; base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
  `HEAD` moved **during** the seat to `350d30e4` (freeze/dispatch commit) — timeline in § A and § D.
- Governing text: `.ufo/waves/round-54/claims-frozen.md` (PRED-C2-r54), `.ufo/waves/round-54/registration.md`
  (§ C2 fixture inventory, § C2 frozen controls).
- Predicate attacked: **PRED-C2-r54 clauses (a)–(c)** — specifically the leg that no other seat in this wave is
  chartered to attack: *can the frozen sentence be satisfied by the correct, faithfully transcribed source
  text?* (forged-input attacks are the mutation-testers' item; this seat attacked the **achievable-input
  boundary** and the **judge determinism**).
- Method: static only — read-only git plumbing, in-lane counters/gates, pinned bytes under
  `.ufo/waves/round-54/fetch/`. No host read, no domain/network read, no package query, no screenshot, no
  producer run, no git/jj mutation, no commit, no delegation/background job, no tool install.
- **This seat made no lane edit.** Everything below is observation.

## Axes named (godspeed)

1. **Coverage** — does the C2 prose claim (uwsm-app environment/launch contract) rest on pins and quotations that
   are *checkable* rather than recited?
2. **Operability** — can one deterministic command judge the frozen sentence `MADO_UWSM_ENTRY: … verdict=TARGET_MET`
   without inventing an unstated normalization or a host read?

Cheap probes were run in parallel batches (pins hashes, quote matching matrix, row/entry parse, gate runs) and only
moves that improved an axis without harming the guard (host/lane-write fence) were kept.

## A. Provenance of the frozen artifacts at base (finding F1)

```
$ git rev-parse HEAD
e25149fec8152a3aabd2b18a0ee8663b23cf65aa
$ git status --porcelain            # 14:05, before any sibling landing
?? .ufo/waves/round-54/
$ git ls-tree -r --name-only e25149fe .ufo/waves/round-54 | wc -l
0
$ git cat-file -e e25149fe:.ufo/waves/round-54/fetch/uwsm-0.27.1-README.md; echo "exit=$?"
fatal: path '.ufo/waves/round-54/fetch/uwsm-0.27.1-README.md' exists on disk, but not in 'e25149fec8152a3aabd2b18a0ee8663b23cf65aa'
exit=128
```

Contrast — the round-52 pins **are** committed at the same rev:

```
$ git ls-files .ufo/waves/round-52/fetch | wc -l
6
$ git cat-file -e e25149fe:.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp; echo "exit=$?"
exit=0
```

Consequence: `claims-frozen.md`, `registration.md` **and all three C2 pins** exist only as untracked working-tree
files at base. Therefore (i) registration's own statement "committed before wave 1 dispatch" is not satisfied at
`e25149fe`; (ii) any reader that resolves inputs from git objects at `--rev` (the round-52 pattern the C2 counter is
modelled on) cannot see the pins, the freeze, or the scored tree; (iii) an untracked pin can be silently replaced
between waves without any git-visible diff. Round-52's committed pins are revision-stable; round-54's were not at
the frozen base.

They became revision-stable **after** the wave had dispatched (observed mid-seat):

```
$ git log -1 --format='%H%n author:%ai%n commit:%ci%n %s'
350d30e4ec5531f65ce99a57efeb8216f38e678a
 author:2026-10-27 13:42:45 -0300
 commit:2026-10-27 14:11:10 -0300
 round-54: freeze claims, registration, source pins and wave one dispatch
$ git ls-tree -r --name-only 350d30e4 .ufo/waves/round-54 | wc -l
11
$ git cat-file -e 350d30e4:.ufo/waves/round-54/fetch/uwsm-0.27.1-README.md; echo "exit=$?"
exit=0
$ for f in claims-frozen.md registration.md fetch/SHA256SUMS.txt fetch/README.txt; do \
    a=$(git show HEAD:.ufo/waves/round-54/$f | sha256sum | cut -d' ' -f1); \
    b=$(sha256sum .ufo/waves/round-54/$f | cut -d' ' -f1); echo "$f same=$([ "$a" = "$b" ] && echo yes || echo NO)"; done
claims-frozen.md same=yes
registration.md same=yes
fetch/SHA256SUMS.txt same=yes
fetch/README.txt same=yes
$ stat -c '%y %n' .ufo/waves/round-54/w1-dispatch.json .ufo/waves/round-54/w1.ready
2026-10-27 14:05:25.339613967 -0300 .ufo/waves/round-54/w1-dispatch.json
2026-10-27 14:05:28.669609305 -0300 .ufo/waves/round-54/w1.ready
```

Timeline, all times `-03:00`: draft author date 13:42:45 → `receipts/before.txt` baseline 13:57:27 → w1 dispatch
14:05:25 / ready 14:05:28 → seats reading 14:05–14:08 → freeze+pins **committed** 14:11:10. The freeze bytes are
identical between that commit and the worktree (`sha256`: claims `c72b4a07…`, registration `8eaa8d85…`), so nothing
scored changed — but the freeze was not visible in any git object while the wave was reading it. A `--rev`-faithful
counter could only have scored against `350d30e4` or later, i.e. never against the base the claims name.

Adjacent observation (not item-8 scope, reported once, verbatim): `claims-frozen.md` C1 refers to the round-52 file
`SHA256SUMS.txt`, while the committed round-52 file is `SHA256SUMS` (no `.txt`); the round-54 fetch file *is*
`SHA256SUMS.txt`. A C1 counter hard-coded to either name fails on the other round — for C1 seats to check.

## B. Pin integrity (passes)

```
$ cd .ufo/waves/round-54/fetch && sha256sum uwsm-0.27.1-README.md uwsm-0.27.1-uwsm-app.1.scd uwsm-0.27.1-main.py
1874fb8368f6956ebdadd1db0780ea26104f3dd3bf95cca4609ab7c77c9b597a  uwsm-0.27.1-README.md
3982503d6445017eb55e9b68446c422b0a07a45a5d9a471b02ecc4cdb8a6f5eb  uwsm-0.27.1-uwsm-app.1.scd
7dd6363244c101c7a0e7641684e29b6a13905e98f9fc3a4c81421e536a976c72  uwsm-0.27.1-main.py
$ wc -c uwsm-0.27.1-README.md uwsm-0.27.1-main.py uwsm-0.27.1-uwsm-app.1.scd
 49717 uwsm-0.27.1-README.md
199361 uwsm-0.27.1-main.py
  2309 uwsm-0.27.1-uwsm-app.1.scd
```

- All three hashes equal `fetch/SHA256SUMS.txt` and equal the sha256 recorded inside the landed rows S375–S377.
- Byte counts equal `fetch/README.txt`'s table (49,717 / 199,361 / 2,309).
- Gap (F2): **PRED-C2-r54 has no pin-hash leg.** Clause (b) checks quotes only; `claims-frozen.md` requires hashes
  for C1 ("each of the four pins' bytes hash to the round-52 recorded sha256") but the C2 predicate never makes the
  round-54 hashes a scored condition. Pins are hash-correct today, but nothing in the frozen sentence would detect a
  substituted pin whose text still contains the three quotes.

## C. Frozen C2 quotation verification — exact results (finding F3, high)

Pins are cited by the frozen `quote location` cells. Matching matrix (strict byte contiguity / whitespace-collapsed /
markdown-emphasis-stripped), computed over whole-pin bytes:

| row | frozen quote words | frozen loc | actual span | strict | ws-normalized | emphasis-stripped |
|---|---|---|---|---|---|---|
| S375 | 24 | `uwsm-0.27.1-README.md:117-118` | **117–119** | FAIL | **PASS** (1 occurrence) | PASS |
| S376 | 11 | `uwsm-0.27.1-uwsm-app.1.scd:60` | 60 | FAIL | **FAIL** | **PASS** |
| S377 | 3 ws-tokens (96 chars) | `uwsm-0.27.1-main.py:3714` | 3714 | **PASS** (1 occurrence) | PASS | PASS |

Exact pin text (raw, `:117-119` and `:60`):

```
117: - Difference between environment state before and after preparation is exported
118:   into systemd user manager (and D-Bus activation environment if reference D-Bus
119:   implementation is used)
```

```
60: *uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon
```

Findings:

- **S375 (F3a, off-by-one + unspecified reflow):** the frozen quote is a single-line cell but the pin carries it across
  three lines with one two-space continuation indent each (`\n  `). Strict byte contiguity fails; it passes only after
  collapsing whitespace, which the freeze never authorizes for C2 (the freeze's normalization note — "single-space
  normalization of interior newlines ONLY where the frozen quote itself carries a newline" — sits in the **C1**
  § Counter form and the frozen C2 cell carries no newline). The frozen location cell `:117-118` is also **wrong**:
  the quote ends on line 119. Location-window enforcement at `:117-118` fails even under whitespace collapse (probe
  T-B below); extending to `117-120` passes.
- **S376 (F3b, unpassable quote as frozen):** pin line 60 renders the subject in scd emphasis — `*uwsm-app*` — while
  the frozen cell reads `uwsm-app client sends arguments…`. The quote is absent under strict **and** whitespace-collapsed
  matching; it appears only if a counter additionally strips `*` from pin bytes. Markdown-emphasis stripping is nowhere
  in the frozen contract. A literal implementation prints `quotes` short for this row and, per the kill rule, a
  `verdict=TARGET_MISSED` non-zero exit — for *correct* source truth.
- **S377 (passes):** strict contiguous substring, exactly one occurrence, at exactly line 3714. Near-duplicate trap:
  line 3716 is `unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}@{random_hex(8)}.{app_unit_type}"`
  (scope vs service, `@`), so only an exact-string judge distinguishes them; a judge that relaxes one character or
  matches on `unit_name = f"app-` alone would accept the wrong line.
- **Fragment collision (S375):** `implementation is used` also occurs at README line 410
  (`implementation is used, this delta is also synched to its activation`). Whole-quote normalized matching is unique
  (1 occurrence); any per-fragment or first-token judge can key on the wrong span.

Net: of the three frozen quotations, **exactly one (S377) is verbatim under the contract as written.** Reaching
`quotes=3/3`/`admitted=1/1 … verdict=TARGET_MET` requires at least two normalizations the freeze does not state
(whitespace collapse for S375; `*`-stripping for S376). PRED-C2-r54 therefore does not pin down its own judge (F3c).

## D. Concurrent lane landing observed mid-seat (finding F4)

First `git status` (14:05) was clean except the wave dir. Between 14:07 and 14:08 three tracked-path changes and one
new note appeared **while this seat was reading** (this seat wrote nothing):

```
$ date -Is
2026-10-27T14:08:09-03:00
$ git rev-parse HEAD
e25149fec8152a3aabd2b18a0ee8663b23cf65aa          # unchanged
$ git status --porcelain
 M corpus/README.md
 M corpus/SOURCES.md
?? .ufo/waves/round-54/
?? corpus/knowledge/uwsm-app-environment-r54.md
$ git diff --stat
 corpus/README.md  | 2 ++
 corpus/SOURCES.md | 3 +++
 2 files changed, 5 insertions(+)
$ stat -c '%y %n' corpus/knowledge/uwsm-app-environment-r54.md corpus/SOURCES.md corpus/README.md
2026-10-27 14:07:00.456476887 -0300 corpus/knowledge/uwsm-app-environment-r54.md
2026-10-27 14:07:28.868434478 -0300 corpus/SOURCES.md
2026-10-27 14:08:05.218379337 -0300 corpus/README.md
```

At the first observation (14:05) the base-state predicates of `claims-frozen.md` held exactly:
`ls corpus/knowledge | grep -c r54` → `0`; `grep -n "^| S37[0-9]" corpus/SOURCES.md | tail` → last row `S374`;
`corpus/README.md` had 69 index rows. At 14:08 the same commands return 1, `S377`, and 70. The landing is
**uncommitted** (HEAD was still `e25149fe` at that moment; the note is untracked), and its author is not attributable
from the artifacts — this seat reports it as observed state, not as a verified sibling action.

Second stage, 14:11:10: HEAD advanced to `350d30e4` ("round-54: freeze claims, registration, source pins and wave one
dispatch") — that commit contains **only** the freeze, registration, pins, receipts and dispatch (11 files, § A). The
entry and rows are still **not** in any commit:

```
$ git rev-parse HEAD ; date -Is
350d30e4ec5531f65ce99a57efeb8216f38e678a
2026-10-27T14:11:21-03:00
$ git status --porcelain
 M corpus/README.md
 M corpus/SOURCES.md
?? .ufo/waves/round-54/w1.ready
?? .ufo/waves/round-54/w1.ready.dispatched
?? .ufo/waves/round-54/w1/
?? corpus/knowledge/uwsm-app-environment-r54.md
?? corpus/lessons/round-54.md
```

`git diff --stat` at that point: `corpus/README.md | 2 ++`, `corpus/SOURCES.md | 5 +++++` (the three rows plus a
round-54 search-note paragraph at `SOURCES.md:585`). So at the end of this seat the C2 artifacts live in three
different places: pins in `350d30e4`, freeze in `350d30e4`, entry/rows/index-row in the uncommitted worktree.
`git status` was also mutating between my own reads (14:08 → 14:11), so any seat's snapshot of "the tree" is
timestamp-bound.

## E. Clause-by-clause reachability of PRED-C2-r54 against the landed artifacts

State read at 14:08 (worktree, uncommitted) and re-checked at 14:11 after HEAD advanced to `350d30e4` — still
uncommitted: entry `corpus/knowledge/uwsm-app-environment-r54.md` (21 lines), rows `corpus/SOURCES.md:325-327`,
index row `corpus/README.md:82`.

| clause | requirement | observed | verdict |
|---|---|---|---|
| (a) | entry exists, indexed, opens with `source:` / `verified-at:` / `recheck:` citing S375, S376, S377 | entry lines 1–3 carry the trio; index row at README:82; `source:` line reads `source: S375–S377 — …` (**U+2013 en dash**, no literal `S376` token on that line; `S376` occurs only in body line 11) | **judge-dependent** (F5) |
| (a) | "at the scored revision" | entry/rows/index-row are untracked or modified at **both** `e25149fe` and `350d30e4` (pins alone are committed at the latter) | **not satisfied at any rev yet** (F1/F4) |
| (b) | rows `mined`, opened `2026-10-27`, URL pinned at `0727985c…` | S375/S376/S377 all `mined`, `2026-10-27`, URL path contains the commit; hashes match actual bytes | **PASS** |
| (b) | "its `teaches`/quote cell's located quote (≤25 words) occurs verbatim in the pin" | `teaches` (cell 4) is prose in all three rows (`preparation environment export…`, `uwsm-app client transport`, `generated app unit-name construction`) → FAIL strict/normalized/emphasis all three. Cell 6: S375 `Difference before and after preparation is exported into systemd user manager` → FAIL all three (drops `between environment state`); S376 → PASS only emphasis-stripped; S377 `unit name includes desktop and command substrings and random hexadecimal text` → FAIL all three | **unimplementable as written** (F6) |
| (b) | anchor line cells | S375 anchor `README.md:117-118` repeats the off-by-one (true 117–119); S376 `uwsm-app.1.scd:60` correct; S377 `uwsm/main.py:3714` correct | 1 of 3 wrong (F3a) |
| (c) | entry carries ≥2 host joins from the frozen set as `file:line` | exact frozen strings: **0/8**; basename:line relaxed: **2/8** (`bindings.conf:2`, `omarchy-toggle-idle:9`, both on entry line 17); `autostart.conf:1..6` appear only as the phrase "at lines 1–6" → 0/6 under any `name:<line>` matcher | **judge-dependent** (F7) |

Note the entry's own citation of the pin repeats the upstream location error: entry line 9 says
"pinned README lines 117–118". The row cell and the entry therefore agree with the frozen cell — and all three are
off by one against the pin.

## F. Host join evidence limits (finding F8)

The frozen host set is `~/.local/share/omarchy/default/hypr/autostart.conf:1`…`:6`,
`~/.config/hypr/bindings.conf:2`, `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`
(`registration.md` § C2 fixture inventory). Limits, in order of force:

1. **Unreadable inside the round by guard.** Host paths are outside the lane and this wave forbids host/domain reads.
   No seat — and therefore no counter run inside the wave — can open those bytes.
2. **No pinned copies.** `fetch/` holds only the three uwsm files plus `SHA256SUMS.txt`/`README.txt`
   (`ls .ufo/waves/round-54/fetch/`). There is no captured copy, no hash and no line dump of `autostart.conf`,
   `bindings.conf` or `omarchy-toggle-idle`. The only record of what L1 saw is `fetch/README.txt` prose (itself
   untracked): "six `exec-once = uwsm-app -- …` lines: hypridle, mako, waybar, fcitx5, swaybg,
   omarchy-hyprland-monitor-watch", "`SUPER, RETURN` → `uwsm-app -- xdg-terminal-exec …`", "`uwsm-app -- hypridle`"
   at `omarchy-toggle-idle:9`.
3. **Partial in-lane corroboration only.** Committed notes corroborate 4 of the 8 frozen citations:
   - `autostart.conf:1` — `corpus/knowledge/idle-lock-route-r17.md:79` ("line 1 `exec-once = uwsm-app -- hypridle`
     (autostart.conf:1)").
   - `autostart.conf:2` — `corpus/knowledge/remaining-planes-census.md:161` (`exec-once = uwsm-app -- mako`).
   - `autostart.conf:5` — `corpus/knowledge/remaining-planes-census.md:160` (`exec-once = uwsm-app -- swaybg …`).
   - `bindings.conf:2` — `corpus/knowledge/terminals-and-omarchy.md:95`, `corpus/knowledge/terminal-route-r17.md:103`,
     `corpus/knowledge/xdg-terminal-selection-r47.md:74`, and held row S059.
   **Uncorroborated anywhere in the committed corpus:** `autostart.conf:3` (waybar), `:4` (fcitx5), `:6`
   (omarchy-hyprland-monitor-watch) and `omarchy-toggle-idle:9`
   (`grep -rn "autostart.conf:3\|autostart.conf:4\|autostart.conf:6" corpus/` → no hits outside the new entry;
   `grep -rn "omarchy-toggle-idle:9"` → new entry only; `config-health-report-r3.md:203` cites a *different* line,
   `omarchy-toggle-idle:13`). The landed entry line 17 is the first lane file to assert the `:3/:4/:6` payload
   mapping and `toggle-idle:9`.
4. **Therefore clause (c) is a citation-of-citation check.** The counter can only see text presence in the entry; the
   *truth* of the join is unverifiable in-round. A wrong payload order (e.g. claiming line 3 = fcitx5) or a wrong
   `toggle-idle:9` claim is undetectable, and could not be caught without a host read the guard forbids.
5. **Upstream pin-commit leg is also unverifiable statically.** The `v0.27.1` ↔ `0727985c9bae655bda488f87f99ea69a6ac1c003`
   association is asserted only by `fetch/README.txt` ("freedesktop GitLab primary carries only tags ≤ v0.27.0 at open
   time, so the mirror tag is the pin"); no network read is permitted in this wave, so this seat cannot confirm it.

## G. Distinct tests run by this seat (item-8 distinctness)

Distinct from forged-quote attacks (the mutation-testers' item): these test whether **correct** text can pass and
whether the judge is determinate. Each is a small, cheap probe; all were run read-only over the pins.

- **T-A markdown-emphasis boundary (S376):** `emphasis_stripped_match=True` for all three rows, while
  `strict=False, norm=False` for S376 → the pass depends entirely on an unstated `*`-strip. Recorded in § C.
- **T-B frozen location-cell window enforcement (S375):** enforcing the frozen `:117-118` as the search window
  rejects the correct quote even whitespace-normalized (`window norm=False`; extended `117-120` → `norm=True`).
  The same window rule applied to S376 (`:60`) and S377 (`:3714`) reproduces the whole-pin result exactly
  (S376 fail, S377 pass, both single-line cells), so the window rule isolates precisely the S375 off-by-one.
- **T-C forged-control sanity (C2-CTL-1 basis):** `"via a socket" in pin` → `False`; `"socket"` occurrences in the scd
  pin → `0`. The frozen C2-CTL-1 mutation is genuinely absent from the pin, so that control stays meaningful.
- **T-D S377 near-duplicate discrimination:** exact quote count `1`; `@`-variant at 3716 distinct → an exact judge is
  sound here, a suffix-relaxed judge is not.
- **T-E S375 fragment collision:** `implementation is used` occurs twice (117–119 and 410) → whole-quote matching is
  unique, fragment matching is not.
- **T-F source-line tokenization (F5):** entry line 1 `source: S375–S377` uses U+2013 (`cat -A` →
  `S375M-bM-^@M-^SS377`); literal token scan of that line: `S375=True, S376=False, S377=True`. The index row
  (`README:82`) contains `S375`×2 and `S377`×2 but **no `S376` token**. A counter that verifies the provenance line or
  the index row for the three ids literally fails clause (a) on text that a human reads as complete.
- **T-G host-join exactness (F7):** 0/8 exact frozen strings; 2/8 relaxed (§ E).

## H. Gates exercised (read-only; no r54 counter exists yet)

```
$ ls quality/counters | grep -c r54
0
$ python3 -I quality/check-index.py --rev e25149fe --repo . ; echo "exit=$?"
MADO_INDEX: rev=e25149fe indexed=69/69 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
$ python3 -I quality/check-index.py --root . ; echo "exit=$?"
MADO_INDEX: root=. indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
$ python3 -I quality/check-index-rows.py --rev e25149fe --repo . ; echo "exit=$?"
MADO_INDEX_ROWS: rev=e25149fe rows=69 errors=2 warns=3
ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52.md at line 80
ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md at line 81
exit=1
$ python3 -I quality/check-index-rows.py --root . ; echo "exit=$?"
MADO_INDEX_ROWS: root=. rows=70 errors=3 warns=0
ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52.md at line 80
ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md at line 81
ERROR row-outside-map: knowledge/uwsm-app-environment-r54.md at line 82
exit=1
$ python3 -I quality/check-index.py --rev 350d30e4 --repo . ; echo "exit=$?"
MADO_INDEX: rev=350d30e4 indexed=69/69 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
$ python3 -I quality/check-index-rows.py --rev 350d30e4 --repo . ; echo "exit=$?"
MADO_INDEX_ROWS: rev=350d30e4 rows=69 errors=2 warns=3
exit=1
```

- Navigation completeness matches the frozen harm-watch baseline: **69/69 at base**, 70/70 in the post-landing
  worktree (a new index row does not shrink it).
- Row **fidelity** was already red at base (`errors=2`, exit 1) because rows at README:80 and :81 sit after the
  coverage-map table's terminating blank line (`sed -n '78,84p'` shows row 79 blank, then 80/81/82). The concurrent
  landing adds a third `row-outside-map` error at line 82 — it does not break a green gate, it extends a red one.
  Owner should place the r54 row inside the map table before any revision-based scoring.
- **Before receipt cross-check:** `receipts/before.txt` (committed at `350d30e4`) records the base state as
  `0` r54 counters, `0` r54 entry, `index count: 69`, `knowledge files: 69`, `registry rows: 311`, `last row id:
  S374`, `MADO_SELFTEST: 460/460 assertions passed`. This matches what this seat observed independently at 14:05
  (`ls corpus/knowledge | grep -c r54` → 0; last SOURCES row S374; 69 index rows), so the *absence* half of the C2
  before-state is confirmed by two independent readers. The selftest figure is quoted from the receipt — this seat
  did not run it.
- Not exercised by this seat (out of item-8 scope, handed to main): `bash tools/mado-verify.sh --selftest` (460/460),
  the sources census, and any `c2-r54-*` counter run (absent).

## I. Findings (severity, evidence pointer)

| id | finding | severity | evidence |
|---|---|---|---|
| F1 | Freeze, registration and the three C2 pins were **untracked at base `e25149fe`** (only round-52 pins are revision-stable there); they became git-visible only at `350d30e4`, committed **14:11:10**, after w1 dispatch (14:05:25 / ready 14:05:28). Registration's "committed before wave 1 dispatch" is false by commit timestamp (author date 13:42:45 is the only pre-dispatch figure). | high (provenance) | § A, `git cat-file -e …` exit 128 at base / exit 0 at `350d30e4`; `git log -1 --format=%ci` |
| F2 | PRED-C2-r54 has **no pin-hash leg** (unlike C1); a substituted pin passes if its text carries the quotes. | medium | § B; `claims-frozen.md` C1(c) vs C2(b) |
| F3a | S375 frozen location `:117-118` is **off by one** (true 117–119); repeated in row anchor and entry line 9. | high | § C, `:117-119:raw` |
| F3b | S376 frozen quote is **not in the pin** under strict or whitespace-collapsed matching (pin has `*uwsm-app*`). Only an unspecified `*`-strip admits it. | high | § C, `:60:raw` |
| F3c | The frozen predicate under-determines its judge: with the contract as written, 1 of 3 quotes verifies → literal counter = TARGET_MISSED on correct text. | high | § C matrix |
| F4 | Lane changed twice mid-seat: entry + rows + index row landed uncommitted 14:07–14:08 (unattributed), then `HEAD` advanced to `350d30e4` at 14:11:10 carrying the freeze only; entry/rows are still uncommitted → clause (a)'s "at the scored revision" is unsatisfied, and any seat's "current tree" snapshot is timestamp-bound. | high (process) | § D, `git status`/mtimes/commit time |
| F5 | Provenance/index tokenization: `source: S375–S377` (en dash) has no literal `S376`; index row has no `S376` token. | medium | § G T-F |
| F6 | Clause (b)'s "`teaches`/quote cell's located quote occurs verbatim" is unimplementable against the landed rows: `teaches` is prose in all three; cell 6 fails for S375 (paraphrase, drops "between environment state") and S377 (claim note, not a quote). | high | § E (b) |
| F7 | Clause (c) host joins: 0/8 exact frozen strings, 2/8 basename-relaxed; `autostart.conf:1..6` carried only as "lines 1–6". Judge unspecified. | high | § E (c) |
| F8 | Host-join truth is structurally unverifiable in-round (no pinned host bytes; guard forbids host reads); 4 of 8 citations corroborated only by older committed notes, `:3/:4/:6` and `toggle-idle:9` by nothing. | medium (claim limit) | § F |
| F9 | Row-fidelity gate is red at base (rows 80/81 outside the map table) and the new row at README:82 inherits it. | medium | § H |

## J. Not done / out of scope

- No committed entry drafted (seat instruction); no lesson text drafted; no row text authored; no lane file created,
  modified or deleted outside this report.
- No counter authored or executed (`quality/counters` has no `r54` file); no C1 work beyond the one-line adjacent note.
- No host read, no network/domain read, no package query, no screenshot, no producer execution, no config/service/
  compositor mutation, no git/jj mutation, no commit/push, no subagent dispatch, no background job.
- Source repo `/home/vgpnk/Projects/shokuknow` untouched.

## K. Tooling

- No installs or updates. Nothing to record (tool/version/channel/reason: n/a).
- Scratch used: `/fast/scratch/hyaku/mado-r54/R54Seat08/` only (`rows-rev.txt`, `rows-root.txt`); no `/tmp` writes;
  scratch cleaned before yield. All repo reads used absolute paths from the fleet-root cwd.

## Attacked predicate, restated

PRED-C2-r54 as frozen requires `… admitted=1/1 rows=3/3 controls=6/6 verdict=TARGET_MET`. On the correct, faithfully
transcribed source text this seat measures: pin hashes 3/3 and bytes 3/3, quote locations 2/3 correct (S375 off by
one), strict verbatim quotes 1/3 (normalized 2/3; emphasis-stripped 3/3), host-join exact citations 0/8 (2/8 relaxed),
revision visibility: pins frozen-in-`350d30e4` only, entry/rows uncommitted at every revision so far. The predicate is
reachable only by a counter that adopts at least three unstated normalizations (S375 whitespace collapse, S376
emphasis strip, relaxed host-join matching) — i.e. the frozen sentence is not self-contained for a `--rev` reader.
That is the honest report; no lane edit and no verdict is asserted by this seat.
