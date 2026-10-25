# CritClaimWording (w1, round 40) — claim-wording attack on the frozen registration

Target: overreach in `.ufo/waves/round-40/registration.md` (freeze `5e7e885`, base `9fc511d`).
Method: each quoted sentence is tested against the counter/control/harness code that is supposed to
back it, and against the host where a claim is about the host. I edited nothing in the lane.
Proposed edits are text for the L1, not applied.

Two findings are blocking: **F1** (a closed four-form enumeration the host falsifies) and **F2**
(the census receipt is produced by the throwaway reference while clause h stamps it with the
delivered tool's sha256).

---

## F1 — BLOCKING. "the four native forms" is a closed set; the host answers a fifth (`vec2`)

**Registration text attacked** (`registration.md:33-34`, `:42`, `:68`):

> Native replies are compared in their native forms (`int`, `float`, `str`, `custom`)
> … that emits only the four native forms and `no such option`
> … what the compositor answers to `getoption -j` (the four native forms and `no such option`)

**Counterexample (run now, allowed read-only verb):**

```
$ hyprctl getoption -j input:tablet:region_position
{"option": "input:tablet:region_position", "vec2": [0,0], "set": false }
$ hyprctl getoption -j input:tablet:region_size
{"option": "input:tablet:region_size", "vec2": [0,0], "set": false }
$ hyprctl getoption -j input:tablet:active_area_size
{"option": "input:tablet:active_area_size", "vec2": [0,0], "set": false }
$ hyprctl getoption -j input:tablet:active_area_position
{"option": "input:tablet:active_area_position", "vec2": [0,0], "set": false }
```

Captured verbatim in `w1/CritClaimWording/vec2-probe.txt` (host `Hyprland 0.56.2 … efb50993`,
rc=0 for each). `input:tablet:absolute_region_position` answers `int`, so the fifth form is not a
blanket property of `input:tablet:*`.

Source anchors, both in the lane's own frozen fetch:
- `fetch/hyprlang-config-v0.6.8.bin:474` — `case CConfigValue::eDataType::CONFIGDATATYPE_VEC2: {`
  (the enum has a member the four-form list omits; `:492-496` shows `STR`/`CUSTOM` beside it).
- `fetch/config-manager-efb5099.bin:549-554` — `addSpecialConfigValue("device", "region_position",
  Hyprlang::VEC2{0, 0})` etc.

**This is not only a form-space claim — it is a reachable *declared key*.** A tree that declares
the option yields a declared key in the delivered table:

```
$ D=$(mktemp -d); mkdir -p $D/.config/hypr
$ printf 'input {\n    tablet {\n        region_position = 1, 2\n    }\n}\n' > $D/.config/hypr/hyprland.conf
$ python3 -I tools/mado-options.py --home $D
[{"key": "input:tablet:region_position", "value": "1, 2", "owner": ".config/hypr/hyprland.conf",
  "layer": "root", "line": 3, "set": true}]
```

So a legitimate declaration produces a live reply with no known form. The counter's own contract
(`c1-r40-live.py:40-43`) says "an answer with no known form, exits 5 with the key" — i.e. the
delivered tool reports a **compositor failure for a healthy compositor** on a valid config. The
70-key census never sees it because the static table of this host declares none of the vec2 keys.

**Impacted axes:** C1 operability (the deliverable's own failure taxonomy), C2 coverage (the entry
would state a four-form ground that is false as written).

**Smallest safe correction:** do not touch the frozen counter (`FORMS` at `c1-r40-live.py:99` and
`capture_ok`'s `len(lines) != 70` at `:603` make a fifth form a new predicate). Narrow the claim and
disclose the gap.

Replace `:33-34` `Native replies are compared in their native forms (int, float, str, custom),`
with:

> Native replies are compared in the four forms the host's 70 declared keys answer (`int`, `float`,
> `str`, `custom`; the census receipt's counts), converted per …

Replace `:68` `answers to getoption -j (the four native forms and no such option)` with:

> answers to `getoption -j` (the four forms the 70 declared keys answer, the `no such option` text
> for an unknown key, and the fifth form `vec2` — `input:tablet:region_position|region_size|
> active_area_size|active_area_position`, observed 2026-10-25 rc=0 — which no declared key of the
> census exercises and which the tool treats as an unknown form, exit 5)

Replace `:42` `that emits only the four native forms and no such option` with:

> that emits only the four native forms and `no such option` (the stub's answer space; the host also
> answers `vec2`, which no fixture exercises)

If the L1 prefers to *cover* vec2 rather than disclose it, that is a new predicate
(`PRED-C1-r40-v2`) and the claim fails as declared — the freeze sentence (`:6-7`) already says so.

---

## F2 — BLOCKING. False provenance: clause h stamps the delivered tool's sha onto a receipt the reference produced

**Registration text attacked** (`:73-76`, `:77-79`, `:61-63`, `:94-95`):

> an own-work row for the live census receipt … clause h binds the own-work receipt to the
> committed tool sha256 … the live host receipt (`70/70` under the reference model, `w1`) …
> Residual (declared): a fabricated self-consistent set passes; committed bytes cannot prove the
> receipt is what the location served or what the compositor answered.

**Evidence — the receipt says it is not the delivered tool's work**
(`w1/ExecLiveCensus/census-receipt.txt`):

```
# command: python3 -I mado-options-ref.py --home $HOME --live   (exit 0)
# tool: throwaway reference .ufo/waves/round-40/c1/ctl-ref-tool.py.txt
tool-reference sha256 f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa
tool sha256 <TOOLSHA>
…
- `tool sha256 <TOOLSHA>` is a placeholder: the delivered tools/mado-options.py
  sha256 at REV replaces it; this receipt is produced from the throwaway reference.
```

Clause h (`c2-r40-forms-entry.py:209-224`) requires
`hashlib.sha256(tool).hexdigest() in rtext` where `tool = show(repo, rev, TOOL)` — the delivered
`tools/mado-options.py`. The only way to satisfy it is to write the delivered tool's sha into a
receipt whose counts came from `ctl-ref-tool.py.txt` (sha `f96d9e0a…`). That is a provenance
substitution, and `registration.md:61-63` confirms the numbers are "under the reference model".
The delivered tool does not exist yet: `tools/mado-options.py` at `e2b51d3` has only
`--home/--getoption/--selftest` (no `--live`), so no census *can* have been produced by it.

**Impacted axes:** C2 coverage (the entry's own-work row and its two count lines), and C1's residual
(F5 below) which leans on the same receipt.

**Smallest safe correction** — one of two, and the registration must say which:

(a) Re-run the census with the delivered tool once `--live` lands, regenerate the receipt with
`tool sha256 <the delivered sha>`, and keep clause h. Then replace `:61-63`'s "under the reference
model" with "under the delivered tool". This is the only path that keeps the claim honest and
clause h satisfied.

(b) Keep the reference receipt: bind its own `tool-reference sha256 f96d9e0a…` line, keep the
`<TOOLSHA>` placeholder *and its note*, and state in the entry that the counts are the reference
model's. Clause h as frozen then fails (`sha256(tool) not in rtext`) → C2 misses as declared.

Either way, replace `:94-95` with:

> **Residual (declared):** a fabricated self-consistent set passes; committed bytes cannot prove
> the receipt is what the location served, what the compositor answered, or **which program
> computed the label counts** — clause h binds the receipt to the delivered tool's sha256, so a
> receipt whose numbers came from the reference must carry the reference's sha and the entry must
> say so, or the census must be re-run with the delivered tool.

---

## F3 — HIGH. The census sentence: undefined star, a conditional zero, an unnamed "native model"

**Registration text attacked** (`:72-73`):

> and the host census (62 agreement / 8 agreement*, 0 mismatch under the native model — the number
> the receipt states)

Three separate overreaches:

1. **`agreement*` is never defined in the registration.** The counter defines it
   (`c1-r40-live.py:36`): "`agreement*` (equal, set, more than one declarer)". The receipt
   repeats the definition (`census-receipt.txt`: "agreement* = native value matches and the key has
   >1 declarer") and lists the 8 keys. Read without it, "8 agreement*" looks like eight partial
   agreements — it *understates* the evidence (all 8 are exact matches).
2. **`0 mismatch` is conditional on the angle-inheritance rule, not evidence for it.** The same
   receipt's own control: `variant-noinherit labels agreement=62 agreement*=6 mismatch=2`, flipped
   at `general:col.active_border` and `group:col.border_active` — the two keys the rule was fitted
   to. The census confirms the rule on its own fitting data; it is not an independent test.
3. **"the number the receipt states"** is true, but the counter does not verify the values. Clause h
   (`c2-r40-forms-entry.py:209-224`) checks that a `labels agreement=…` line exists, that
   `forms` sum == `labels` sum (70), and that the exact line appears in the entry. `62/8/0` could be
   any self-consistent split. And "native model" names no program — the labels come from the
   reference.

**Proposed replacement for `:72-73`:**

> and the host census the receipt states — 62 `agreement` / 8 `agreement*` (defined as: the native
> string matches and the key has more than one declarer) / 0 `mismatch` / 0 `config-only` /
> 0 `live-default` over the 70 declared keys. The zero is conditional on the angle-inheritance rule:
> the same receipt's no-inheritance variant reads 62/6/2, flipping the two keys the rule was fitted
> to, so the census corroborates that rule on its fitting data and does not test it independently.
> Clause h binds the line's presence and the forms/labels sums, not the values.

---

## F4 — HIGH. "C1 shares no file with C2" is false

**Registration text attacked** (`:98`): `and C1 shares no file with C2.`

Both counters read the same delivered file: `c1-r40-live.py:84` `TOOL = "tools/mado-options.py"`
(behaviour), `c2-r40-forms-entry.py:53` `TOOL = "tools/mado-options.py"` (clause h's sha256).
They share no *evidence artifact* (C1: `c1/native-capture.jsonl`; C2: `fetch/`), which is the
intended point — but as written it is falsified by two constants, and it hides a real coupling:
a late edit to the tool fails C2's clause h as well as C1's fixtures, so C2's verdict depends on
C1's file bytes.

**Proposed replacement for `:96-98`:**

> **Separability:** C1 is judged by the tool and a stub compositor; C2 by entry/registry/receipt
> bytes. C2's counter passes a dummy tool (control P) without C1's verdict, and the two counters
> share no evidence artifact. They do share one input: both read the delivered
> `tools/mado-options.py` — C1 by behaviour, C2 by sha256 — so a post-receipt edit to that file
> fails C2's clause h independently of C1.

---

## F5 — MEDIUM. C1 residual: the "out-of-distribution check" checks the wrong program

**Registration text attacked** (`:61-63`):

> a tool that hardcodes the reference model's conversion tables for this generator's value space
> passes the fixtures; the live host receipt (`70/70` under the reference model, `w1`) is the
> out-of-distribution check and is reported, not scored.

The residual names the exact cheat (hardcoding the reference tables) and then names a check that
cannot catch it: the host census was produced **by the reference model** (`census-receipt.txt`), so
a tool that hardcodes those tables agrees with it by construction. The check exercises the
reference, not the delivered tool. Nothing in round 40 scores the delivered tool against the host.

**Proposed replacement for `:61-63`:**

> **Residual (declared):** a tool that hardcodes the reference model's conversion tables for this
> generator's value space passes the fixtures. The live host census (w1) is *not* a mitigation: it
> was produced by the throwaway reference, so it cannot distinguish the delivered tool from a copy
> of those tables. Nothing in this round scores the delivered tool against the host; the residual is
> held by review, not by evidence.

---

## F6 — MEDIUM. "exit 5 on a compositor failure naming the key" — the missing-program tree names no key

**Registration text attacked** (`:36`): `Exit 5 on a compositor failure naming the key`.

`score_fail` (`c1-r40-live.py:547-558`) asserts `victim in err` for the nonzero-exit and malformed
trees. `score_missing` (`:560-563`) asserts only `rc == 5 and "hyprctl" in err` — the key is not on
stderr because no key was attempted. The counter's own docstring (`:40-43`) makes the same
overreach: "the compositor program missing or exiting non-zero … exits 5 with the key on stderr".

**Proposed replacement for `:36`:**

> Exit 5 on a compositor failure — with the key on stderr for a per-key failure (nonzero exit,
> non-JSON, unknown form) and with `hyprctl` on stderr when `--hyprctl` is missing — exit 2

---

## F7 — MEDIUM. "standard library only; no write" states more than the counter observes

**Registration text attacked** (`:37`): `standard library only; no write.`

- Clause g (`c1-r40-live.py:584-595`) is an **allowlist** (`STDLIB_ALLOW`, 25 modules) plus six
  denied network modules. It is not "the standard library": a stdlib module outside the list
  (e.g. `logging`, `datetime`, `unittest`) fails it.
- "no write" is verified only as `tree_listing(home)` before/after (`:481-497`) — the config root.
  A write to `/tmp`, `$HOME` outside the root, or a sibling path is unobserved.
- Nothing observes programs other than `--hyprctl`: the stub logs only invocations of itself, so
  `subprocess.run(["curl", …])` is stdlib, passes clause g, and is invisible.

**Proposed replacement for `:37`:**

> for a hostile probe key (no program run); imports inside a fixed stdlib allowlist with the network
> modules denied; the config root unchanged across the run (the only write check). Nothing else
> about the process's side effects is observed.

---

## F8 — MEDIUM. "at the data commit and the tip" — the tip is unbounded

**Registration text attacked** (`:48-49`): `exit 0, at the data commit and the tip.`

The counting command takes one `--rev`. "The tip" is whatever HEAD is when a later reader runs it;
round 41 moves it. A later reading can narrow this to "the target failed at the tip" for a change
this round did not make.

**Proposed replacement:**

> exit 0, at the data commit and at the round-40 close commit (the tip at the time this claim is
> made; later rounds are out of scope).

---

## F9 — MEDIUM. The reachability control's revision is not recorded, and fixtures are seeded by REV

**Registration text attacked** (`:52-56`): `The reachability control … scores 13/13 on the fixtures
… so the fixtures are reachable`.

- `ctl/run-c1-controls.py:21` — `REV = os.environ.get("MADO_CTL_REV", "master")`.
- `:63-75` — `score()` returns `last.split(": ", 1)[-1].split(" rev=")[0]`: the rev is **parsed off
  and discarded**. `receipts/ctl-c1.txt` therefore records no rev for any of the 18 controls.
- `c1-r40-live.py:522` — `seed = sha256("%s:%d" % (rev, i))`: the eight generated trees are a
  function of REV. 13/13 at an unrecorded rev is not the same fixture set as 13/13 at the data rev.
- `ctl/run-c1-controls.py:86-89` — the BASE-tool control reads `master:tools/mado-options.py`,
  **not** the declared `BASE_DEFAULT`; `0/13` is a statement about master-at-run-time.

**Proposed replacement for `:52-56`:**

> The reachability control (`c1/ctl-ref-tool.py.txt`, a throwaway reference, never delivered)
> scores `13/13` on the fixtures at the rev the harness ran (recorded as `<rev>`; the harness's
> `MADO_CTL_REV` default is `master` and its receipt drops the rev, so the number is bound to that
> rev — the trees are seeded by `sha256(REV:i)`). It is `TARGET_MISSED` overall: at that rev clause
> b (selftest 71) and clause k (the capture lands only in the freeze commit) both fail; at the data
> rev only clause b would.

Also record the rev in the control receipt (`rev=` kept) so the number is re-runnable.

---

## F10 — MEDIUM. Mutant #16 is described by its patch in the registration and by a different name in the harness

**Registration text attacked** (`:59`): `… angle inheritance absent, probe default masked)`.

The harness key is `M16-probe-key-without-argv-check` (`ctl/run-c1-controls.py:56-58`), but its
patch is `if rec is None: rec = ("str", "", False)` — it fabricates a record when the compositor
answers `no such option`, i.e. it **masks the probe default**. The registration's description is
the accurate one; the harness name is not. A reader who matches the two lists by name concludes the
run is a different mutant set (16 names, 15 matching).

**Proposed edit:** append the patch, not the key, e.g. `… angle inheritance absent, probe default
masked (harness key `M16-probe-key-without-argv-check`, whose patch fabricates a record when the
compositor answers `no such option`))`. Do not renumber the frozen harness.

---

## F11 — MEDIUM. "held S162 … re-opened" is not what clause c verifies

**Registration text attacked** (`:73-74`):

> Cited rows: held S162 (ConfigManager.cpp gradient handler, re-opened) and S173 (hyprlang
> config.cpp `configStringToInt`, re-opened)

Clause c (`c2-r40-forms-entry.py:143-159`) requires, for an id present at base,
`old[0][:10] == cells[:10]` — the held row's first ten cells must be **byte-identical**. A
per-row re-opening mark cannot live there. The only recheck the counter reads is the entry-level
`recheck:` line in the first 20 lines, and `RECHECK_RE` (`:61`) accepts `3d`, `7d`, `on-merge` —
not necessarily a date. So "re-opened" is a token, not a verified act.

**Proposed replacement for `:73-74`:**

> Cited rows: held S162 (ConfigManager.cpp gradient handler) and S173 (hyprlang config.cpp
> `configStringToInt`), re-read this round and left byte-identical in their first ten cells (the
> entry's `recheck:` line records the re-read; the counter does not verify per-row re-opening),

---

## F12 — LOW. "every published axis ties at its maximum" covers three axes, not C2's

**Registration text attacked** (`:13-16`):

> `MADO_AXIS: checked=3 mismatched=0` … every published axis ties at its maximum, so each is a
> lowest axis; C1 works operability, C2 works coverage.

`quality/check-axis-scores.py:32` — `AXES = ("navigation", "calibration", "operability")`. Coverage
is **not** one of the three; the receipt (`receipts/axis-base.txt`) says nothing about it. And the
gate's rule is `published == derived` (`:72`), not a ceiling: 56/56 is all rows verified, not a
maximum row count. With all three at 1.0 the lowest-axis rule selects nothing, which is why two
claims are routed — that is a choice, and should read as one.

**Proposed replacement for `:13-16`:**

> … `MADO_AXIS: checked=3 mismatched=0` (`receipts/axis-base.txt`) — the gate checks three axes
> (navigation, calibration, operability) and each reads published == derived at 1.0, so it selects
> no single lowest axis; the round routes C1 to operability and C2 to the coverage sub-axis family,
> which this gate does not score.

---

## F13 — LOW. "Any later change to a counter, a control, the capture or a declared target is a new predicate and the claim it belongs to then fails as declared"

**Registration text attacked** (`:6-7`). No counter reads a control harness or a control receipt:
`grep -n "ctl-c1\|ctl-c2\|run-c1-controls\|receipts/"` over both counters returns **nothing**. A
later edit to `ctl/run-c1-controls.py` or `receipts/ctl-c1.txt` fails no claim mechanically; it only
makes the recorded control run stale. Changing the registration's *target text* alone likewise
fails nothing — the target lives in the counter's `TOTAL`/`MIN_SELFTEST`.

**Proposed replacement:**

> A later change to a counter or to the native capture is a new predicate (clause k reads the
> capture) and the claim it belongs to then fails as declared. A later change to a control harness
> or a control receipt leaves the counter's verdict untouched and only makes the recorded control
> run stale: re-run it, never re-read it.

---

## F14 — LOW. `no such option` is not in the native capture, and cannot be

`capture_ok` (`c1-r40-live.py:598-616`) requires exactly 70 non-blank lines, each a JSON object with
exactly one of the four forms (`:603`) — a `no such option` line would fail clause k. The capture
(`c1/native-capture.jsonl`, 70 lines: int 44 / float 5 / str 8 / custom 13, verified) therefore
contains no `no such option` evidence. Its ground is a separate probe
(`w1/ConnSourcePatterns.md:13`: `hyprctl getoption -j misc:bogus_xyz_notreal` → `no such option`,
rc=0). Registration `:68` groups the two as one answer space.

**Proposed edit** (fold into F1's replacement): "… the four forms the 70 declared keys answer
(captured), the `no such option` text for an unknown key (probed separately; the capture holds only
JSON replies) …".

---

## F15 — LOW. "only the C2 entry adds a row (baseline 56/56)"

**Registration text attacked** (`:118`). Baseline verified now:
`python3 -I quality/check-index.py --repo . --rev master` → `MADO_INDEX: rev=master indexed=56/56
missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0. But the gate is completeness, not a
count, and the assimilation slice can legitimately admit a new note (≥1 admit is required), which
must add its own row. The "only" is a prediction a sibling can falsify without harming anything.

**Proposed replacement:**

> `quality/check-index.py` complete at the close (baseline 56/56; any note admitted by the
> assimilation slice adds its own row — the gate checks completeness, not the count).

---

## Checked and holds (do not "correct" these)

- Freeze commit `5e7e885` contains exactly the 14 named files (`git show --stat`): registration,
  both counters, both harnesses, five receipts, the capture, the reference tool.
- Base has no `--live`; base selftest is **71/71** (`git show 9fc511d:tools/mado-options.py` run
  from /tmp); base counter run is `fixtures=0/13 … verdict=TARGET_MISSED`, exit 1, matching
  `receipts/c1-before-base.txt` and `:46-47`.
- Capture: 70 lines, 44/5/8/13, one form per line, all four forms — `capture_ok`'s own conditions.
- `CTL_C1: controls=18 correct=18/18` and `CTL_C2: controls=21 correct=21/21` reproduce as
  recorded; M10/M11/M16 sit at 12/13, still `<13` as `:57-59` claims.
- The 20 C2 mutant descriptions at `:86-90` match the harness keys one-for-one (only C1's #16
  diverges — F10).
- Hostile probe: exit 2, no program run — verified by `score_hostile` using a fresh stub dir, so
  `calls.log` is empty (`:570-582`).
- One call per declared key, exact argv, no duplicates — `check_live:511-518` compares
  `sorted(flat) == sorted(need | probes)` and rejects any extra argv.
- `receipts/census-before.txt`: exit 0, seven W04 (S030/S042/S045/S097/S119/S120/S121) + one W01
  (S277) — `:102`.
- `receipts/axis-base.txt`: 3 axes, `mismatched=0`, at base `9fc511d`.
- Stagnation: `SCORECARD.md:283` declares `N = 3`; `SCORECARD.md:2450-2454` is the round-39
  `### Capabilities` row (config-option ownership table) — the nudge waiver at `:15-16` holds.
- `62/8` split vs the host's real declarers: spot-checked `col.inactive_border` (one declarer,
  `looknfeel.conf:16`) — labelled `agreement`, consistent. No measurement error found in the split
  itself; F3 is about the wording, not the count.

## Tooling

No installs; no package transaction; no write outside this seat directory. Compositor verbs used:
`hyprctl version`, `hyprctl getoption -j <key>`, `hyprctl descriptions -j` (read-only).
Scratch tree under `mktemp -d`, removed after the one parse test.
