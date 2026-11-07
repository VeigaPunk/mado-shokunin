# R95MReviewC2 — review of the C2 claim (round 95, w1)

Seat: R95MReviewC2 (reviewer, leaf). Report path: `.ufo/waves/round-95/w1/R95MReviewC2.md`.
Scratch `S=$HYAKU_SCRATCH/mado-r95/R95MReviewC2` (default `/fast/scratch/hyaku/...`), created,
used and **removed**; cited bytes copied to the three `R95MReviewC2-*` files beside this report.
No lane file was edited. No install, no pacman, no mutating git outside the fixture repo, no host
mime database touched. Every run below is **DRAFT** (nothing under `receipts/`).

Objects reviewed (bytes at review time):

| object | sha256 |
|---|---|
| gate `quality/check-selftest-strength.py` | `2d6f1219…598da61b` (unchanged) |
| `tools/mado-mimeglob.py` | `65f80a6c…076e2453` (19 checks) |
| `tools/mado-portals.py` | `e46a861e…b2ac021` (28 checks) |
| landed draft counter `quality/counters/c2-r95-selftest-kills.py` | `e021c2c2c97bbbf34c20aa67c01462577605215529ae03586386423c8243dfef` |
| landed panel `.ufo/waves/round-95/controls/selftest-panel-r95.json` | `635d8ffb62805aaab7accb49d758e6b81a887627266bec0daf5d36a93c76d18b` |

Evidence: `R95MReviewC2-evidence.txt` (sha256 `8d23173e…f3421d3`, 442 lines) plus the two forged
kill-sets `R95MReviewC2-forged-mimeglob.json` (`43f8a9e3…59887ba5`) and
`R95MReviewC2-forged-portals.json` (`b146a2fa…e44cddca`). Each command below names its exit code.

## Findings, by severity

### F1 (medium, claim strength) — PRED-C2-r95-v1 is met by two blanket kills; 47/47 does not certify 47 logic-coupled mutants

Built (in scratch, `forge.py`): one kill per tool whose `find` is a production line and whose
`replace` injects a pre-`def selftest` block that *rebinds the production objects every check calls*,
so every check fails without a crash:

- mimeglob, find `def esc(b: bytes) -> str:` → replacement adds
  `Resolver.__init__` / `Resolver.guess` / `xdgmime_dirs` rebindings returning `x/forge` answers;
  mutated `--selftest` rc 1, FAIL = **19/19** labels, set equal to the derived labels.
- portals, find `def report(r: Resolver, ifaces: list[str], as_json: bool) -> None:` → replacement
  adds `Resolver.__init__/resolve/find/find_all/_gtk` and `parse_keyfile`, `current_desktops`,
  `string_list`, `is_bus_name` rebindings; mutated `--selftest` rc 1, FAIL = **28/28**.

Each kill's `must_fail` is the exact all-label list, `selftest_checks` is 19/28, and the gate holds
both (positive `OK:0`). Running the **landed** draft counter in DRAFT mode with these two kill-sets
and the **landed** panel:

```
python3 -I quality/counters/c2-r95-selftest-kills.py --repo <lane> --rev master \
  --panel .ufo/waves/round-95/controls/selftest-panel-r95.json \
  --expect-panel-sha256 635d8ffb… --expect-gate-sha256 2d6f1219… \
  --expect-kills-sha256 43f8a9e3…,b146a2fa… \
  --control-kills <empty mimeglob>,<empty portals> \
  --expect-control-kills-sha256 bcd5023e…,aa56d62a… \
  --draft-kills <forged mimeglob>,<forged portals> --scratch-root <S> --workers 8 --timeout 60
rc=3
MADO_SELFTEST_KILLS: DRAFT_TARGET_MET pred=PRED-C2-r95-v1 rev=draft gate_pin=ok kills_pin=ok,ok
  tools=2 checks=47 positive=OK:0,OK:0 neutralised_flagged=47/47 hand_flagged=24/24 neutral_ok=6/6
  do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6
  gate_selftest=ok control_hand_flagged=0/24 singleton_labels=0/47 ...
```

So a **two-kill** set (0/47 singleton labels) satisfies every conjunct: (i) both positives OK;
(ii) 47/47 neutralisations WEAK; (iii) 24/24 landed hand weakenings WEAK; (iv) 6/6 neutral edits OK;
(v) all controls; (vi) gate selftest ok; (vii) 0 < 24. This is not a gate bug — the gate's documented
contract is exact FAIL-set equality, and QUALITY 156 (`corpus/QUALITY.md:1178`) explicitly accepts
one mutant caught by several checks. It is a limit of the claim: (ii) proves *each check exists and
fires under a single global sabotage*, not that each check is coupled to the production logic it
names. Recommendation for the freeze: either add a conjunct the lane can defend (e.g. a lower bound
on `singleton_labels`, or that the counted kill count ≥ some pre-declared N), or state in the claim
that 47/47 is neutralisation-detection only. Note a singleton bound must not reintroduce round 93's
uniqueness failure (QUALITY 156); "singleton where one exists" is the safer form.

### F2 (medium) — the (vii) control is count-only and is satisfiable by construction

PRED (vii) requires `control_hand_flagged < hand`. In F1 I passed an **empty** kill-set as the
control (`kills=[]`): every weakened variant stays `OK:0`, so `control_hand_flagged=0/24 < 24` and
(vii) holds. A forger authors both the frozen set and the "first draft", so (vii) cannot show the
frozen set is strong; it only shows two sets differ. The real protection is R95MMutC2's escape list
and the 24-edit panel, not (vii). Recommendation: make (vii) named-subset (the control must miss a
declared list of hand weakenings the frozen set catches) or record the control's actual first-draft
origin (hash of the R95MExecKillsC2 candidate) in the claim.

### F3 (low, confirmed limit) — label derivation matches both result lines exactly; duplicates and f-strings fail closed

Replicated the counter's `labels_of` (`c2-r95-selftest-kills.py:96-105`) and compared with runtime
labels by forcing every check false (`failed = [n for n, ok in checks]`, one edit in a scratch copy):

- mimeglob: raw source tuples **20**, unique **19**, result `checks=19`; printed FAIL labels
  `printed=19 derived=19 same_multiset=True same_order=True`. The duplicate is
  `t15 truncated multi-byte glob refused`, appended in *mutually exclusive* `if/else` arms, so
  dedupe equals the runtime count (verified by the all-fail print).
- portals: **28** raw, **28** unique, result `checks=28`, `same_multiset=True same_order=True`.
- f-string labels: **none** in either tool. A synthetic tool with `f"sy{i} check"` yields
  derivation `[]` vs `checks=2`, i.e. the landed counter's
  `len(lbs) != n or len(set(lbs)) != n` guard (`:230`) stops **SETUP_ERROR** — a refusal, never a
  false pass. Same for a runtime-duplicated label (unique < N). No defect; the guard must survive
  any later edit of that line.

Residual heuristic risk: the mimeglob pattern `^[ \t]+\("…"` matches *any* string-leading tuple in
the selftest body, not only checks. A future non-check tuple there would make the count mismatch and
SETUP_ERROR (fail-closed), not a false accept.

### F4 (low) — gate string `must_fail` accepts a superset; exact lists are load-bearing

`gate()` holds a string `must_fail` when the label is *among* the FAIL lines; only a list demands set
equality (`quality/check-selftest-strength.py:187-190`). A string kill that fails `{A,B}` and names
`A` is accepted even though it does not pin `B`. This is not a PRED bypass: a label is only counted
in (ii) if the kill-set *names* it, so coverage still requires naming every label, and neutralising
an unnamed co-failing label leaves the verdict OK (that label is simply not counted). The check is
at `quality/check-selftest-strength.py:179-180`. The frozen
kill-sets should nevertheless use the exact list, as R95MExecKillsC2's item requires; verify at
freeze that no kill uses a string `must_fail` where the mutant fails more than that one label.

### F5 (confirmed) — (3) the gate's own selftest is not kill-set guardable; the cut is line 73

`non_selftest_prefix` (`quality/check-selftest-strength.py:66-74`) does `text.find("def selftest(")`.
On the gate's own source that first occurrence is the **string literal at line 73**
(`    idx = text.find("def selftest(")`): `idx=2863`, `line=73`, prefix length 2863, prefix tail
`    idx = text.find("`. Consequences measured: `def gate(` and `def run_selftest(` are **not** in
the prefix; the real selftest at line 233 is excluded too. A kill whose `find` is gate() production
`    return 1 if verdict == "WEAK" else 0` is refused by the frozen gate:
`rc=2, SELFTEST_STRENGTH: SETUP_ERROR kill gate-rc-flip find occurs 0 times in non-selftest code`.
The declaration's sentence is confirmed. (The two tools are unaffected: first `def selftest(`
occurrence is the real definition, `tools/mado-mimeglob.py:585`, `tools/mado-portals.py:575`.)

Smallest gate change that would allow a kill-set for the gate's own selftest (**drafted in scratch,
not landed**): replace line 73 with

```
    idx = text.find("\ndef selftest(")
    idx = idx + 1 if idx >= 0 else text.find("def selftest(")
```

- New gate sha256 `2c548f06943f8143b132b39ac85bdd5775d5ba4f3f156a1eb575c1fd8ba3758d`.
- New cut: line **205**, inside the gate's own `SELFTEST_FAKE_OK` fixture string (the first
  `\n`-anchored `def selftest():` is the fake tool). This still excludes the real selftest (line 233)
  and the whole harness; `def gate(` and `def run_selftest(` are now in the prefix.
- New gate `--selftest`: rc 0, `checks=11 failed=0` (unchanged).
- Kill anchoring in gate(): find `    return 1 if verdict == "WEAK" else 0`, replace `…else 1`.
  Mutated gate `--selftest` rc 1, FAIL labels
  `['selftest OK','selftest sha drift allowed rc0','selftest list must_fail exact set held rc0','selftest checks pin']`.
  Frozen gate as the gate: rc 2 SETUP_ERROR (find occurs 0). New gate as the gate, kill-set with
  those exact labels: **rc 0, `SELFTEST_STRENGTH: OK … kills=1 held=1`**. The change does what is
  claimed.
- The draft is deliberately cut at 205, not 233; an AST-based cut at the module-level `selftest`
  definition is the exact alternative if the lane wants the literal definition line. The two-line
  form is fail-closed: if `\ndef selftest(` is absent it falls back to the old search, and a match
  at offset 0 yields an empty prefix (every kill SETUP_ERROR).

Earlier frozen counters it would break (QUALITY 153 `corpus/QUALITY.md:1148`, QUALITY 155 `:1170`):

- `quality/counters/c2-r93-selftest-strength.py` pins the gate sha (`:5` predicate, `:192`
  `--expect-gate-sha256`) and `quality/counters/c2-r94-selftest-kills.py` does the same (`:5`,
  `:159`); the r95 counter does too (`:5`, `--expect-gate-sha256`). Each predicate says "the gate is
  the round-93 frozen gate", so a new gate is a re-anchored carry, not a re-pin.
- Measured on a fixture repo (`git init` in S, `git archive master` + one commit changing only the
  gate; toplevel asserted): base `070a07d6…` → round-94 counter **rc 0 TARGET_MET, gate_pin=ok**;
  changed rev `77b006c6…` → **rc 1 TARGET_MISSED, gate_pin=FAIL**, with every other leg identical
  (`positive=OK:0,OK:0 neutralised_flagged=29/29 hand_flagged=91/91 neutral_ok=6/6 gate_selftest=ok`).
  So the change is behaviorally invisible to the tools and breaks only the sha pin — exactly
  QUALITY 153/155. Landing it requires the new round to carry c2-r93 and c2-r94 on the new bytes as
  legs; this review only drafts it.

## (1) the three named forgery shapes, run against the frozen gate

| forgery | run | result |
|---|---|---|
| one kill, `must_fail` = every label, natural single edit | mimeglob `N_MIMES = 10`→`0`; portals `GTK_DBUS = IMPL + ".desktop.gtk"`→`…gtkX` | mutant fails only **11/19** and **6/28**; gate `rc=1 WRONG_CHECK`, `SELFTEST_STRENGTH: WEAK … wrong_check=1` — refused |
| same shape, blanket rebinding (F1) | mimeglob/portals rebind blocks | mutant fails **19/19** and **28/28**; gate `rc=0 OK held=1`; counter DRAFT_TARGET_MET — **accepted** |
| kills that edit comments | mimeglob `# xdgmimeint.c _xdg_utf8_skip_data`→ comment + text; docstring sentence edit | selftest unchanged; gate `rc=1 SURVIVED … WEAK` — refused (fails PRED (i)) |
| `find` inside a string | functional: `types = ["inode/directory"]`→`["inode/dir"]` | fails `['t09 trailing slash']`; mislabels `must_fail`→`WRONG_CHECK rc1`; exact label→`OK rc0` (a normal kill, not a bypass) |
| `find` inside a docstring | prefix docstring sentence | `SURVIVED`, gate WEAK — refused |

So "one kill lists every label" is accepted **only when the mutation genuinely fails every check**;
the exact-set rule is what refuses the naive version. The blanket route (F1) is the real shortcut and
it is the finding above. Union-covering kills (one failing `{alpha,beta}`, one failing `{gamma}`) also passed a synthetic 3-check gate
(`OK`, all 3 neutralisations WEAK) — consistent with QUALITY 156 and with F1.

## Residual risk and verification gaps

- The two frozen kill-sets (`build/mado-mimeglob-kills.c2.json`, `build/mado-portals-kills.c2.json`)
  and the landing paths `quality/selftest-kills/mado-{mimeglob,portals}.json` were **absent** at my
  cutoff (build/ listed only `l1-findings-r95.md` and the two c1 candidates). My counter run is
  therefore a DRAFT run with forged sets against the landed counter and panel; the real leg (iii)
  on the real candidate sets, and their singleton coverage, remain to be run by the L1/MutC2 after
  the sets land. Re-check F1 against the real sets: `singleton_labels` is printed, not a conjunct.
- The landed counter's docstring hard-codes 47/19+28; the runtime derives them (`checks=47` in the
  run above), so a tool change would SETUP_ERROR rather than silently read 47.
- Nothing here measures a frozen revision; no receipt was written.
- Commands and exit codes: both tools `--selftest` rc 0 (19/28); gate `--selftest` rc 0 (11/11);
  F-A/F-B/F-B2/F-C gate runs rc 1/1/1/1 (F-C exact rc 0); synthetic all-label rc 0; F1 counter rc 3
  (DRAFT_TARGET_MET); fixture r94 counter rc 0 at base and rc 1 at the changed-gate rev.
