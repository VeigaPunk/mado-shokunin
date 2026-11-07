# R94MReviewC2 — review of C2 (two kill-sets, counter, panel, controls) round 94, wave w1

Seat R94MReviewC2 (reviewer, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`; base rev
`a3de997289014e7dbf1d73ae206be1d6f8cdadd0`, lane HEAD during review `5a164538` (w1 dispatch evidence).
Scratch `S=/fast/scratch/hyaku/mado-r94/R94MReviewC2` (deleted on exit; nothing left on disk).
**Every run below is a DRAFT run**: nothing here is a measurement, no `TARGET_*` word is claimed for the lane,
nothing was written under `.ufo/waves/round-94/receipts/`, and the only lane file I wrote is this report. No
installs, no network, no pacman, no git/jj mutation (read-only `git show`/`cat-file` only). C2 only: no C1 file,
tool or counter was read.

Axes: **C2 operability** (does gate + two kill-sets + panel + counter catch a weakened, still-green selftest
assertion of `tools/mado-xdgmime.py` and `tools/mado-mime.py`?) and **predicate fidelity** (does the counter
measure the sentence PRED-C2-r94-v1 froze?).

## 0. Artifacts reviewed (two revisions seen; C2 was a moving draft during w1)

| artifact | sha256 reviewed | note |
|---|---|---|
| `quality/check-selftest-strength.py` | `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` | round-93 frozen gate, unchanged; equals `git show a3de9972:…` |
| `tools/mado-xdgmime.py` | `4e7fff9efbd32d101d1383099566008fc49ba626be5bcc53a20766d71bc7fd88` | unchanged; equals `git show a3de9972:…` |
| `tools/mado-mime.py` | `2532ccb57cf9d67f6590e4aac2e8d0a9f9eb011b25eb42e45118a6ff51871a5e` | unchanged; equals `git show a3de9972:…` |
| `.ufo/waves/round-94/build/mado-xdgmime-kills.c2.json` | `126b508aa1841ba99fa17ecaef46a5a79cdee99956ac2a605479b96122f09ea9` | 12 kills |
| `.ufo/waves/round-94/build/mado-mime-kills.c2.json` | `d930689e6ff82e51722195e0c8d209fe46fb4697fd10f01f33cec30e98e81601` | 15 kills |
| `.ufo/waves/round-94/controls/selftest-panel-r94.json` | `2727794c0f8a0bc27d8c7d16f517be6bc17fe6647e6265f2dedb3f1cf6288f3f` | 12 hand + 6 neutral; earlier revision `0dd9be00…` (see §6.2) |
| `quality/counters/c2-r94-selftest-kills.py` | `9c65bf86a3c9d356a4f62286228f113ed482cdddee5c25e1d5749f6b698d35a1` | 300 ln; earlier revision `2ee36e5e…` (see §5.3, F1) |

`git cat-file -e a3de9972:.ufo/waves/round-94/build/mado-xdgmime-kills.c2.json` → **rc 128 (absent)**, so at the
base rev the counter must stop `SETUP_ERROR` (separability) — measured in §5.4.

`.gitignore` covers only `.ufo/interactive-sessions/`, `.ufo/state/`, `__pycache__/`; both kill-sets are
committable, and the freeze must commit them at the counter's read paths (§9 F7).

## 1. Ground truth: the two selftests and their labels (runtime-derived, DRAFT)

```
$ TMPDIR=$S python3 -I tools/mado-xdgmime.py --selftest   -> MADO_XDGMIME_SELFTEST: checks=12 failed=0   rc=0
$ TMPDIR=$S python3 -I tools/mado-mime.py    --selftest   -> MADO_MIME_SELFTEST:    checks=17 failed=0   rc=0
$ TMPDIR=$S python3 -I quality/check-selftest-strength.py --selftest
                                                          -> SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0 rc=0
```

Runtime dump (copy of each tool with `import json as _j; print('LABELS:'+_j.dumps([n for n,ok in checks]))`
inserted before the `failed = [...]` line) — 29 labels, all unique:

```
xdgmime 12: m03 list: second id installed | m05 desktop-specific file first | m09 only a file's first matching
 line counts; the next file is read | m16 CR kept in the id | d09 Exec=true is a builtin: not installed |
 f06 unanchored grep in mimeinfo.cache | f09 a cache value -n is an echo option | b02 InitialPreference picks |
 s01 LXQt: rc 3 | s05 no slash: rc 1 | s08 --version | type outside RFC 6838 refused
mime 17: cache addition is default | hidden and unloadable dropped from lists | subdir id | alias unaliased |
 parent in registered not recommended | unloadable only -> none | hidden default accepted | desktop list wins |
 desktop list additions ignored | other desktop ignores it | removal blocks lower addition | added group is read
 before removed whatever the file order | unloadable list skipped | masked lower addition skipped, hidden one
 taken | default from masked id still loads in a lower dir | desktops | fgets chop
```

**Label-derivation hazards** (the "robust to both selftest shapes" clause):

* xdgmime builds 11 checks as tuples in `            checks += [` (grep `^            ("` = 11) and the 12th as
  `checks.append(("type outside RFC 6838 refused", False))` at :787 **repeated** at :789 in the `except` arm. A
  derivation that reads only the tuple body yields 11; one that also reads `checks.append` yields **13** raw
  entries with one duplicate. Either way the count != `checks=12` unless the duplicate is folded.
* mime builds all 17 through the local helper `def chk(name, cond): checks.append((name, cond))` (:845-846); the
  labels are the first argument of 17 `chk("…", …)` calls (:869-898). Two labels (:873, :894) carry their
  condition on the following line — a single-line regex requiring `", …)` fails those two.
* `    failed = [n for n, ok in checks if not ok]` occurs **exactly once in each file** and **0 times** in the
  non-selftest prefix of each (`text[:text.find("def selftest(")]`), so the neutralisation line can never serve
  as a kill `find`: fed as one, the gate prints
  `SELFTEST_STRENGTH: SETUP_ERROR kill inside find occurs 0 times in non-selftest code` rc 2 (measured).

## 2. Gate semantics the kill-sets and the counter rely on (measured, DRAFT)

`python3 -I quality/check-selftest-strength.py --tool <copy> --kills <json> --scratch-root $S/g --timeout 20
[--allow-sha-drift]`

| probe (xdgmime) | output | rc |
|---|---|---|
| kill `find` inside `def selftest` | `SETUP_ERROR kill inside find occurs 0 times in non-selftest code` | 2 |
| kill `find` 15× in production (`    def `) | `SETUP_ERROR kill twice find occurs 15 times in non-selftest code` | 2 |
| crash mutant (`raise SystemExit(9)` early in `query`) | `SURVIVED crash` + `SELFTEST_STRENGTH: WEAK … survived=1` | 1 |
| empty kill-set on a neutralised selftest | `SELFTEST_STRENGTH: OK … kills=0` | 0 |

So kills must land once in production (`pre = text[:text.find("def selftest(")]`, gate:151-158), a crash is
`SURVIVED` (never held), and list `must_fail` is compared exact-set via `sorted(fails) != sorted(must_fail)`
(gate:178-181). The claim's `before` leg (`0/29` with no kill-set) is honest: an empty kill-set makes the gate
say OK even on a neutralised check.

## 3. Kill-set `build/mado-xdgmime-kills.c2.json` (`126b508a…`) — verified line by line

Header `tool_sha256=4e7fff9e…` = the tool at base rev (MATCH); `selftest_checks=12`; both prefixes the tool's own.
Independent verifier (`verify_kills.py`: apply `find`/`replace`, run the mutated copy's `--selftest`, compare the
FAIL list with `must_fail`):

```
[xdgmime] tool_sha256 ok=True   unmutated rc=0 MADO_XDGMIME_SELFTEST: checks=12 failed=0
  x01-m03-second-id            g=1 pre=1 rc=1 fails=1 exact=True
  x02-m05-desktop-file-first   g=1 pre=1 rc=1 fails=1 exact=True
  x03-m09-last-line-wins       g=1 pre=1 rc=1 fails=1 exact=True
  x04-m16-cr-stripped          g=1 pre=1 rc=1 fails=1 exact=True
  x05-d09-builtins-dropped     g=1 pre=1 rc=1 fails=1 exact=True
  x06-f06b02-grep-anchored     g=1 pre=1 rc=1 fails=2 exact=True
  x07-f09-echo-flags-kept      g=1 pre=1 rc=1 fails=1 exact=True
  x08-b02-initialpref-ignored  g=1 pre=1 rc=1 fails=1 exact=True
  x09-s01-lxqt-branch-dead     g=1 pre=1 rc=1 fails=1 exact=True
  x10-s05-no-slash-rc0         g=1 pre=1 rc=1 fails=1 exact=True
  x11-s08-version-string       g=1 pre=1 rc=1 fails=1 exact=True
  x12-rfc-guard-off            g=1 pre=1 rc=1 fails=1 exact=True
[xdgmime] kills=12 valid=12 union=12
```

* Every `find` occurs exactly once **in the whole file** (hence also outside `def selftest`); every `replace` is a
  production change; every `must_fail` is the observed FAIL set exactly; the union is the 12 runtime labels.
* 11 kills are singleton; `x06` names two (`b02`, `f06`) and `x08` still gives `b02` a singleton — the set is
  not blast-shaped.
* Positive leg, **without** `--allow-sha-drift`:
  `SELFTEST_STRENGTH: OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` rc 0.
* 12/12 single-check neutralisations (`failed = [… if not ok and n != X]`, selftest still
  `checks=12 failed=0`) → `WEAK` rc 1: `m03 m05 m09 m16` → `SURVIVED`; `f06` → `WRONG_CHECK` (x06 loses only
  `f06`); `b02` → `SURVIVED` (x08) + `WRONG_CHECK` (x06). No OK.

**But the set is dimension-partial for `s01` and this is exploitable — F2, §8.3.**

## 4. Kill-set `build/mado-mime-kills.c2.json` (`d930689e…`) — verified line by line

Header `tool_sha256=2532ccb5…` = the tool at base rev (MATCH); `selftest_checks=17`.

```
[mime] tool_sha256 ok=True   unmutated rc=0 MADO_MIME_SELFTEST: checks=17 failed=0
  a01-default-additions-off        g=1 pre=1 rc=1 fails=6 exact=True
  a02-lists-keep-hidden            g=1 pre=1 rc=1 fails=3 exact=True
  a03-subdir-prefix-flat           g=1 pre=1 rc=1 fails=4 exact=True
  a04-alias-never-resolves         g=1 pre=1 rc=1 fails=1 exact=True
  a05-no-parent-fallback           g=1 pre=1 rc=1 fails=1 exact=True
  a06-default-first-holder         g=1 pre=1 rc=1 fails=2 exact=True
  a07-default-rejects-hidden       g=1 pre=1 rc=1 fails=3 exact=True
  a08-mimeapps-before-desktop-list g=1 pre=1 rc=1 fails=1 exact=True
  a09-desktop-list-additions-on    g=1 pre=1 rc=1 fails=1 exact=True
  a10-hyprland-read-always         g=1 pre=1 rc=1 fails=1 exact=True
  a11-removals-ignored             g=1 pre=1 rc=1 fails=1 exact=True
  a14-mask-off                     g=1 pre=1 rc=1 fails=1 exact=True
  a15-default-first-holder-load    g=1 pre=1 rc=1 fails=1 exact=True
  a16-desktops-filter-loose        g=1 pre=1 rc=1 fails=1 exact=True
  a17-fgets-empty-line             g=1 pre=1 rc=1 fails=1 exact=True
[mime] kills=15 valid=15 union=17
```

All 15 `find`s unique in the whole file and in production; all `must_fail` exact; union = the 17 runtime labels.
Positive leg OK rc 0; 17/17 neutralisations `WEAK` rc 1 (measured by the counter run in §5.2, cross-checked by my
own per-label loop).
Sharpness: 9 singleton kills; `a01` (6 labels), `a03` (4), `a02`/`a07` (3). The note is honest — narrow
attempts for `added group is read before removed whatever the file order` "survived and were dropped", so that
label is guarded **only** by the 6-label blast `a01` (F8, §8.3). I tried a singleton myself (group-order swap in
`DesktopDir._read`) — it leaves the selftest green (rc 0, no fails), confirming the label has no easy narrow kill.

## 5. Counter `quality/counters/c2-r94-selftest-kills.py` (`9c65bf86…`) — fidelity to PRED-C2-r94-v1

### 5.1 Conjunct map (code read against the declaration sentence)

| PRED clause | implementation | verdict |
|---|---|---|
| gate frozen, both kill-sets frozen | `gate_pin` (:198), `kills_pin` (:199, comma pair) in `met` (:281) | implemented |
| (i) gate OK rc 0 per tool, no drift | `pos_j` jobs with `drift=False`; compared as `OK:0` (:281) | implemented |
| (i) `tool_sha256` = tool at rev | `tool_pin` (:200) in `met` | implemented |
| (ii) labels from the checks tuples, count == `checks=N` | `labels_of` (:89-98) + `len(lbs) != n or len(set(lbs)) != n` → SETUP_ERROR (:212-214) | implemented after F1 fix |
| (ii) neutralise each label → `WEAK:1`, 29 | `neutralise` (:84-87) = the context's exact line replacement; `nflag == len(neut_j)` (:282) | implemented |
| (iii) hand weakenings → `WEAK:1` | `weak_j`; `hflag == weak_total - len(neut_j)` | implemented |
| (iv) neutral edits → `OK:0` | `nonw_j`; `zok == len(nonw_j)` | implemented |
| variants green first (`checks=N failed=0`, same line) | :216-219 → SETUP_ERROR | implemented |
| (v) do-nothing < (ii)+(iii) | `dn < weak_total` (:283) | implemented |
| (v) always-OK flags none | `aok < weak_total` (:283) | **loose — F4** (should be `aok == 0`) |
| (v) always-WEAK fails (i) | `all(v != "OK:0" for v in aw)` | implemented |
| (v) sha-diff fails (iv) | `sd_zok < len(nonw_j)` | implemented |
| (vi) gate `--selftest` rc 0 | `gs_ok` (:276) | implemented |
| rc-aware verdicts | `Run.gate` returns `VERDICT:rc`, all checks compare `"OK:0"`/`"WEAK:1"` | implemented |
| DRAFT mode | `--draft-kills` → `DRAFT_` prefix, rc 3 (:299-300) | implemented |

### 5.2 DRAFT run of the current bytes with the frozen candidates (`--rev HEAD`)

```
$ python3 -I quality/counters/c2-r94-selftest-kills.py --repo . --rev HEAD \
    --panel …/selftest-panel-r94.json --expect-panel-sha256 2727794c… \
    --expect-gate-sha256 2d6f1219… --expect-kills-sha256 126b508a…,d930689e… \
    --workers 8 --scratch-root $S/c6 \
    --draft-kills …/build/mado-xdgmime-kills.c2.json,…/build/mado-mime-kills.c2.json
rc=3
MADO_SELFTEST_KILLS: DRAFT_TARGET_MET pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2
  checks=29 positive=OK:0,OK:0 neutralised_flagged=29/29 hand_flagged=12/12 neutral_ok=6/6
  do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6
  gate_selftest=ok tool_pin=ok,ok kill_paths=quality/selftest-kills/mado-xdgmime.json,quality/selftest-kills/mado-mime.json
  gate_sha256=2d6f1219… kills_sha256=126b508a…,d930689e…
```

All probes: `T1 pos OK:0`, 12 `T1 N:… WEAK:1`, 6 `T1 W:… WEAK:1`, 3 `T1 Z:… OK:0`, `T2 pos OK:0`, 17
`T2 N:… WEAK:1`, 6 `T2 W:… WEAK:1`, 3 `T2 Z:… OK:0` (49 probes: 2 pos + 29 N + 12 W + 6 Z, all as expected).

### 5.3 Finding F1 (HIGH, was blocking; fixed in the reviewed bytes) — label double count

The revision `2ee36e5e0e82f6affd30929e79868c4d71dd15344414b892e8a1a53932fa0158` (300 ln, 03:29) derived labels without folding the
if/else pair, so `labels_of(text, 0)` returned **13** entries (12 unique). Measured end-to-end with the real
kill-sets and panel:

```
$ python3 -I quality/counters/c2-r94-selftest-kills.py … --draft-kills <build>/mado-xdgmime-kills.c2.json,<build>/mado-mime-kills.c2.json
rc=2
MADO_SELFTEST_KILLS: SETUP_ERROR pred=PRED-C2-r94-v1 tools/mado-xdgmime.py: labels enumerated 13 (unique 12) != checks=12
```

i.e. the counter could not emit any verdict at all. The reviewed bytes fix it exactly as I independently
derived (`if lb not in out` fold in :94-97, docstring updated at :25-26). Verified: `labels_of` now returns
12/17 unique, and the run in §5.2 reaches `DRAFT_TARGET_MET`. **Recorded as fixed; no action needed except that
the freeze must land `9c65bf86…`.**

### 5.4 Negative arms (current bytes, DRAFT)

| arm | output | rc |
|---|---|---|
| no kill-sets at `--rev a3de9972` (C1-commit separability) | `SETUP_ERROR … absent at a3de9972: quality/selftest-kills/mado-xdgmime.json, quality/selftest-kills/mado-mime.json …` | 2 |
| panel sha wrong | `SETUP_ERROR … panel sha256 2727794c… != pinned` | 2 |
| panel entry that breaks the selftest (hand[0] expected id → `zzz.desktop`) | `SETUP_ERROR … variant T1 W:xdg-w01-m03-id-observed does not keep the selftest green: rc=1 'MADO_XDGMIME_SELFTEST: checks=12 failed=1'` | 2 |
| `--expect-gate-sha256` wrong (`0…0`) | `DRAFT_TARGET_MISSED … gate_pin=FAIL` (draft rc 3; non-draft would be rc 1 by `return 0 if met else 1`) | 3 |

The `gate_pin` behaviour is a *documented* choice (R94MExecCounterC2.md:18: "a pin mismatch is TARGET_MISSED, not
a setup stop, because PRED says TARGET_MET iff the gate is the frozen gate"). It deviates from the seat wording
"pins → SETUP_ERROR rc 2" but matches the frozen predicate; I record it as an observation (F5), not a defect.

## 6. Panel `controls/selftest-panel-r94.json` (`2727794c…`)

### 6.1 Verified properties

* All 18 `find`s occur **exactly once** in the named tool (global count, not just the prefix).
* All 18 variants keep the selftest green with the byte-identical result line → the counter's green gate passes
  them (no SETUP_ERROR; §5.2).
* Hand (12): gate `WEAK:1` for every one. My independent strength test (apply the weakening, then each candidate
  kill, compare FAIL sets with the unweakened run) shows a kill lost for all 12, e.g.

```
xdg-w01-m03-id-observed          green=True held_before=12 after=11 lost=['x01-m03-second-id']
xdg-w02-m05-id-observed          green=True held_before=12 after=11 lost=['x02-m05-desktop-file-first']
xdg-w03-s01-rc-observed          green=True held_before=12 after=11 lost=['x09-s01-lxqt-branch-dead']
xdg-w04-s08-version-observed     green=True held_before=12 after=11 lost=['x11-s08-version-string']
xdg-w05-f06-id-observed          green=True held_before=12 after=11 lost=['x06-f06b02-grep-anchored']
xdg-w06-d09-id-observed          green=True held_before=12 after=11 lost=['x05-d09-builtins-dropped']
mime-w01-cache-addition-observed green=True held_before=15 after=14 lost=['a01-default-additions-off']
mime-w02-hidden-list-observed    green=True held_before=15 after=14 lost=['a02-lists-keep-hidden']
mime-w03-subdir-id-observed      green=True held_before=15 after=13 lost=['a01…','a03-subdir-prefix-flat']
mime-w04-alias-widened           green=True held_before=15 after=12 lost=['a01…','a03…','a04-alias-never-resolves']
mime-w05-desktops-observed       green=True held_before=15 after=14 lost=['a16-desktops-filter-loose']
mime-w06-fgets-observed          green=True held_before=15 after=14 lost=['a17-fgets-empty-line']
```

* Neutral (6): gate `OK:0` for all; each is a comment or a reorder of independent checks (three comments, two
  reorders, one docstring), and no kill's `find` overlaps a neutral's edited bytes, so no kill's FAIL set can
  move. Strength preserved by construction and by observation (`shadiff_neutral_ok=0/6` also shows the sha-diff
  control cannot pass this panel).

### 6.2 Revision note (evidence that the panel moved, and what it hid)

The earlier panel revision `0dd9be0057c75074d3e4718281210454fae1d7a967d08c9d392c15eeafd9ae7f` had `xdg-w03` as
`… == (None, q(…)[1])` ("expected rc replaced by the observed rc; the id arm kept"). Running that panel against
**my scratch copy of the counter with only the F1 dedupe fix** (the then-committed counter `2ee36e5e…` could not
reach the probes at all) gave `hand_flagged=11/12 … DRAFT_TARGET_MISSED`, with the `xdg-w03` probe `OK:0`,
because the only kill that reaches `s01` (`x09`, a dead-branch mutant) still changes the **id** arm. The panel
was then revised to the current full tautology `… == q(…)`, which `x09` does catch, making the composed run
`DRAFT_TARGET_MET`.

That revision makes the predicate pass **without fixing the kill-set gap it exposed**: the `s01` rc arm is still
guarded by nothing (§8.3). If the L1 wants the guard rather than the green light, add the kill in F2, not the
stronger weakening.

Panel coverage is also thin as a *witness set*: 12 of 29 labels have a hand weakening, and 5 of the 6 mime
entries are the same class ("expected value replaced by the observed value"). Class-diversity is left to the
mutation-tester's brief.

## 7. Controls (all DRAFT, from the §5.2 verdict line)

| control | predicate requirement | measured |
|---|---|---|
| do-nothing (flag iff result line changes) | fewer than (ii)+(iii) = 29+12 = 41 | `do_nothing_flagged=0` — fails ✔ |
| always-OK gate | flags none | `always_ok_flagged=0` — fails ✔ |
| always-WEAK gate | fails (i) | `always_weak_positive=WEAK:1,WEAK:1` — fails ✔ |
| sha-diff gate | fails (iv) | `shadiff_neutral_ok=0/6` — fails ✔ |

The pre-freeze control also holds in the other direction: an *incomplete* kill-set produces
`DRAFT_TARGET_MISSED` (R94MExecCounterC2.md:38 records `neutralised_flagged=2/29 hand_flagged=2/12`), and the
earlier panel revision produced `11/12 → DRAFT_TARGET_MISSED` in my own run (§6.2). So the counter can say MISSED
as well as MET.

## 8. Forgery: (i)+(ii) are satisfied by kill-sets that isolate nothing

### 8.1 Construction (DRAFT)

Predicate (ii) reduces to *union coverage* once (i) pins each kill's exact FAIL set: neutralising X removes X from
a mutant's FAIL list, so the gate answers `WEAK` iff some kill names X. Nothing forces a kill to be narrow.

* xdgmime forgery — one kill from a **blast** mutant that disables `query`:
  `find` = `    def query(…):\n        if mime in (b"--help", b"--manual"):\n            raise Unsupported(…)`
  (1× in production), `replace` = `    def query(…):\n        return b"x", 0`.
  Selftest: `checks=12 failed=12` → `must_fail` = all 12 labels (measured).
* mime forgery — five blast mutants (`default`→None, `app_info_new`→False, `_get_app`→(True,False),
  `current_desktops`→[], `_pairs_from_text`→[("a","b")]) with FAIL sets 10/2/5/2/3 → union = 17 (measured).

Both kill-sets pin `tool_sha256` correctly and their `find`s occur exactly once in production. Taken through the
**current counter** with the frozen panel:

```
$ … --draft-kills $S/forged-xdgmime-kills.json,$S/forged-mime-kills.json
rc=3
MADO_SELFTEST_KILLS: DRAFT_TARGET_MET … checks=29 positive=OK:0,OK:0 neutralised_flagged=29/29
  hand_flagged=12/12 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0
  always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6 gate_selftest=ok tool_pin=ok,ok
  kills_sha256=b1b33379…,2f9da818…
```

**Answer to the ticket's question: the predicate does not reject the forgery.** A pair whose kills each fail many
checks scores `29/29` and `12/12`, because every hand weakening is of the "make the check always true" kind, and
any kill that fails that check catches it. The panel therefore cannot tell isolation from blast.

### 8.2 Why it matters (what the blast kills cannot see)

A loosening that keeps the weakened check falsified by the blast stays invisible. Measured on xdgmime with the
**forged** set: `("s01 …", q(…) == (None, 3))` → `("s01 …", q(…)[0] is None)` (rc arm dropped) is green
(`checks=12 failed=0`) and the forged set reports `OK:0`.

### 8.3 The same gap in the *real* candidates (F2/F8, actionable)

Because coverage is by union only, a label whose kills do not isolate its dimensions escapes whenever a
weakening targets the uncovered dimension:

```
xdgmime, frozen set (126b508a…)
  W_rc  ("s01 LXQt: rc 3", q(…, XDG_CURRENT_DESKTOP="LXQt") == (None, q(…)[1]))
        green checks=12 failed=0 ; gate -> SELFTEST_STRENGTH: OK … kills=12 held=12  rc 0    <- ESCAPE
  W_id  ("s01 LXQt: rc 3", q(…, XDG_CURRENT_DESKTOP="LXQt")[0] is None)
        green checks=12 failed=0 ; gate -> OK … kills=12 held=12                       rc 0    <- ESCAPE
  witness mutant: `            return None, 3` -> `            return None, 0` (1× in production)
        on the original : FAIL ['s01 LXQt: rc 3']      (the behaviour both weakenings stop observing)
        on W_rc / W_id  : FAIL []                      (rc 0, no FAIL lines)
```

`x09` (dead-branch) mutates the **id** arm, so it holds under both weakenings; the rc arm has no kill at all.
**Repair (verified):** add
`{"id": "x13-s01-lxqt-rc0", "find": "            return None, 3", "replace": "            return None, 0",
"must_fail": ["s01 LXQt: rc 3"]}` — `find` occurs once in production. Measured with the extended set:
positive `OK … kills=13 held=13` rc 0, `W_rc` and `W_id` both `WEAK:1` (`SURVIVED x13-s01-lxqt-rc0`), 12/12
neutralisations still `WEAK:1`, and the composed counter run reaches `DRAFT_TARGET_MET` (with the earlier panel
revision too).

mime, frozen set: the label `added group is read before removed whatever the file order` is named only by `a01`
(6 labels). A widening of its expected value —
`R().default("text/plain") == "a.desktop"` → `… in ("a.desktop", "b.desktop")` — is green
(`checks=17 failed=0`) and the gate reports `OK … kills=15 held=15`, because `a01` drives `default` to `None`,
which the widened check still rejects. I did not find a singleton mime kill for this label (the obvious
group-order swap in `DesktopDir._read` leaves the selftest green), so the repair belongs to the mutation-tester /
L1; the *class* is identical to F2.

**Recommended predicate repair for a later freeze:** for every label X require at least one kill with
`must_fail == [X]`, or bound `|must_fail| < N` and require the singleton kills to cover the labels. Without it,
(i)+(ii) certify union coverage, not strength.

## 9. Findings by severity

**F1 (HIGH; was blocking, fixed in the reviewed bytes).** `labels_of` double-counted xdgmime's if/else
`checks.append` pair (13 vs `checks=12`); every counter run stopped `SETUP_ERROR` (measured, rc 2, revision
`2ee36e5e…`). Fixed at `9c65bf86…` (:94-97); re-verified (`DRAFT_TARGET_MET`).

**F2 (HIGH; open).** The frozen xdgmime kill-set cannot see either single-arm weakening of `s01`
(`… == (None, q(…)[1])`, `… [0] is None`): both green, gate `OK rc 0` (§8.3). This is the concrete instance of
the union-coverage gap; the earlier panel revision even *found* it (`hand_flagged=11/12`, `DRAFT_TARGET_MISSED`)
and it was closed by strengthening the panel weakening instead of adding the kill. Fix: add `x13-s01-lxqt-rc0`
(find `            return None, 3` → `            return None, 0`, `must_fail ["s01 LXQt: rc 3"]`), verified.

**F3 (MEDIUM; open, predicate-level).** (i)+(ii) are satisfied by non-isolating kill-sets: the forged pair
(blast kills) scores `29/29` and `12/12` through the counter (`DRAFT_TARGET_MET`, §8.1). Repair: require
singleton kills per label (or bound `|must_fail|`).

**F4 (LOW; open).** `met` uses `aok < weak_total` (:283); the declaration says an always-OK gate "flags none".
A gate that flags 40 of 41 weakenings would pass. Should be `aok == 0` (inherited from round 93).

**F5 (LOW; observation).** A gate/kill-set sha mismatch yields `TARGET_MISSED` (`gate_pin=FAIL`) rather than
`SETUP_ERROR` rc 2, contra the seat wording "pins → SETUP_ERROR rc 2". The counter's docstring (R94MExecCounterC2.md
:18) argues from the PRED sentence; both readings are defensible, but the lane should pick one before the freeze.

**F6 (LOW; open).** The verdict line prints `kill_paths=quality/selftest-kills/…` even in draft mode, where it
actually read the `--draft-kills` files — misleading provenance (the `kills_sha256=` field is correct). The
draft-mode rev is also printed as `rev=draft`, losing the measured `<rev>`.

**F7 (HAZARD; freeze input).** The counter reads the kill-sets at `quality/selftest-kills/mado-xdgmime.json` and
`quality/selftest-kills/mado-mime.json` (:68), but the candidates exist only under `.ufo/waves/round-94/build/`.
The freeze must land them **byte-identically** (`126b508a…`, `d930689e…`) at those two paths, or every run stops
`SETUP_ERROR … absent at <rev>` (measured at the base rev). `.gitignore` does not exclude `.ufo/waves/…`, so
committing the build copies is possible too, but the counter's constant decides.

**F8 (INFO).** mime's `added group is read before removed whatever the file order` has no singleton kill
(only the 6-label `a01`); a widening weakening of it escapes (§8.3). Not a predicate failure by itself — it is
the same class as F2 and should be closed with a narrow kill.

## 10. Residual risk / verification gaps

* **The candidate state is green only as a composition.** `DRAFT_TARGET_MET` holds for the exact triple
  (gate `2d6f1219…`, kill-sets `126b508a…`/`d930689e…`, panel `2727794c…`) at the exact counter `9c65bf86…`.
  Any byte change to any of the four invalidates the pins; in particular a further kill-set edit changes
  `--expect-kills-sha256`, and a panel edit changes `--expect-panel-sha256`.
* **Multi-check weakening is not tested** by design: (ii) neutralises one label at a time. Union coverage happens
  to catch any subset of *neutralisations* (a kill naming a neutralised label loses it), but nothing tests a
  simultaneous rewording of several checks.
* **The kill-sets were verified against the working-tree tools**, which equal the base-rev tools byte-for-byte
  (§0), so the `tool_sha256` pins will hold at the freeze — provided the freeze does not touch the tools.
* **`DRAFT` everywhere.** No run here is a measurement; the L1's freeze commit and the non-draft invocation are
  the only things that can produce a `TARGET_MET`/`TARGET_MISSED` for the lane, and the non-draft path reads
  `quality/selftest-kills/…` (F7) which does not exist yet.
* I did not run the counter's non-draft path (it needs the kill-sets committed) and did not exercise the
  `--timeout`/`NONE:timeout` arms of `Run.gate`; both are code-read only.
* I did not read C1 artifacts, the declaration's C1 rows, or any sibling lane file.

## 11. Commands run (all DRAFT; exit codes as observed)

```
python3 -I tools/mado-xdgmime.py --selftest                rc 0   checks=12 failed=0
python3 -I tools/mado-mime.py --selftest                   rc 0   checks=17 failed=0
python3 -I quality/check-selftest-strength.py --selftest   rc 0   checks=11 failed=0
python3 -I quality/check-selftest-strength.py --tool <copy> --kills <json> --scratch-root $S/g --timeout 20
     (positive legs, 29 neutralisations, panel variants, 4 control stubs, forged kill-sets; rc 0/1/2 as quoted)
python3 -I verify_kills.py <xdgmime kills> <mime kills>    rc 0   12/12 and 15/15 exact, unions 12 and 17
python3 -I quality/counters/c2-r94-selftest-kills.py --repo . --rev HEAD --panel … --workers 8 \
     --scratch-root $S/cN --draft-kills <x>,<m>
     frozen candidates  rc 3  DRAFT_TARGET_MET  29/29 12/12 6/6
     forged pair        rc 3  DRAFT_TARGET_MET  29/29 12/12 6/6
     rev a3de9972, no kills  rc 2  SETUP_ERROR absent at a3de9972
     wrong panel sha         rc 2  SETUP_ERROR panel sha256 … != pinned
     panel entry not green   rc 2  SETUP_ERROR variant T1 W:xdg-w01… does not keep the selftest green
     wrong gate sha          rc 3  DRAFT_TARGET_MISSED gate_pin=FAIL
     earlier counter 2ee36e5e…  rc 2  SETUP_ERROR tools/mado-xdgmime.py: labels enumerated 13 (unique 12) != checks=12
git show a3de9972:<path> | sha256sum   (gate 2d6f1219…, xdgmime 4e7fff9e…, mime 2532ccb5…)
git cat-file -e a3de9972:.ufo/waves/round-94/build/mado-xdgmime-kills.c2.json   rc 128 (absent)
```

Scratch `$S=/fast/scratch/hyaku/mado-r94/R94MReviewC2` held only copies (tool variants, kill-set revisions,
patched counter copy, forged sets) and was deleted on exit.
