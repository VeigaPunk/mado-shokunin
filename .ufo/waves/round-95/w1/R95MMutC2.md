# R95MMutC2 — mutation probe of the round-95 C2 kill-sets and the C2 counter (round 95, w1)

Seat `R95MMutC2` (mutation-tester, leaf — no dispatch). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base rev `4a2af6817024f6ed47084a5217c1825ae247f4fe`. Scratch `S=/fast/scratch/hyaku/mado-r95/R95MMutC2`
(deleted on exit; every cited artefact was copied to `.ufo/waves/round-95/w1/` before deletion).

**Every run in this report is a DRAFT run.** The C2 counter was only ever run with `--draft-kills` (it prints
`DRAFT_*` and exits 3); no `TARGET_*` word is claimed for the lane; nothing was written under
`.ufo/waves/round-95/receipts/`; `quality/`, `build/`, `controls/`, `tools/`, `corpus/` and the declaration were
not modified. The only lane files written are this report and the five `R95MMutC2-*.json` evidence files.

## 0. Objects and pins

| object | sha256 / value |
|---|---|
| gate `quality/check-selftest-strength.py` (round-93 frozen) | `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` |
| `tools/mado-mimeglob.py` (19 selftest checks) | `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453` |
| `tools/mado-portals.py` (28 selftest checks) | `e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021` |
| draft kill-set `build/mado-mimeglob-kills.c2.json` | `f4b80be6ffbbe47d1280edb2858a7528182679d2f232c8c1a4e818de3ab521c7` (17 kills, all 19 labels named) |
| draft kill-set `build/mado-portals-kills.c2.json` | `64b3c10d22da05cd9da5f2200ded96e058fee5d913a07e2d509ff153c8a5c8f4` (27 kills, all 28 labels named) |
| panel `controls/selftest-panel-r95.json` | `635d8ffb62805aaab7accb49d758e6b81a887627266bec0daf5d36a93c76d18b` (24 hand, 6 neutral) |
| C2 counter `quality/counters/c2-r95-selftest-kills.py` (current bytes) | `983d4cbcc0e0965d16e0e27a7d6a1ab44ac7fa98a4279a7ba60b9c3fcf5e873a` (337 lines; the file was revised during the wave — the first measurement used `e021c2c2c97bbbf34c20aa67c01462577605215529ae03586386423c8243dfef`, 332 lines) |

The four objects that matter for part 1 were re-read after the last measurement and are unchanged
(`build/*.c2.json` were read as files, the tools and gate through `git show <base-rev>:<path>`).

## 1. Method

**Weakening catalogue.** For each tool I generated weakenings of its `--selftest` — edits that keep the selftest
**green on the unmutated production code** (`checks=N failed=0`, the identical result line) but weaken an
assertion. Three families, generated per check line of the selftest:

* `all-tautology` — the check's expression replaced by `True` (the expression is no longer even evaluated);
* `or-true` — `expr` → `(expr) or True` (still evaluated, cannot fail);
* semantic per-check weakenings — one component of the asserted tuple dropped or widened:
  mimeglob `(type, uncertain)` → `[0] == type` or `[1] == uncertain` or a widened set; portals
  `(picks, reason)` → `[0] == picks` or `[1] == reason`; plus clause-dropping forms of the compound
  checks (`string list trailing empty dropped` → each conjunct; `bus name validity` → each of the three
  clauses; `parse_keyfile(...) == {...}` → one key; `_raises(...)` → `isinstance(..., bool)`).

Every weakening was verified green through the tool itself (`python3 -I <copy> --selftest`, rc 0, result line
identical to the pristine tool's). Result: **79 green weakenings for `mado-mimeglob.py`, 112 for
`mado-portals.py` (191 total, 191/191 green)** — both above the 60 the seat asks for.

**Escape.** A weakening escapes when the frozen gate, run with the **draft** kill-set, still prints
`SELFTEST_STRENGTH: OK … survived=0 wrong_check=0` rc 0 on the weakened tool:

```
python3 -I quality/check-selftest-strength.py --tool <weakened copy> --kills <draft kill-set> \
    --scratch-root $S/<d> --timeout 60 --allow-sha-drift
```

(`--allow-sha-drift` because the weakening changes the tool's sha256; every verdict is compared as `VERDICT:rc`,
never the word alone. Baseline on the unweakened tools: `OK` rc 0, all kills held — quoted in §2.)

**Closing kill.** A production mutant `M` (find/replace inside the tool's non-selftest code, occurring exactly
once) together with `must_fail` = M's exact FAIL-label set on the pristine tool, chosen so that on the *weakened*
tool M no longer produces that set (the weakened check has lost the ability to see M). Each closer was verified in
both directions: the gate with **draft kill-set + the closer** prints `WEAK` rc 1 on the weakened tool **and**
`OK` rc 0 on the pristine tool (i.e. the closer holds at full strength). Closing files use the kill-set schema, so
the L1 can append `kills` directly.

**Mutant pool.** 74 candidate production mutants were catalogued (per tool); 64 are usable (find unique in the
non-selftest prefix, selftest fails with a non-empty label set): 23 mimeglob, 41 portals. Rejected entries —
3 crash the selftest with no FAIL line (a crash is `SURVIVED`, never a kill) and 7 kill nothing (equivalent on the
selftest): `g04`, `g10`, `g13`, `g15`, `g16`, `g21`, `p02`. Each usable mutant's exact FAIL set is recorded; every
label of both tools is covered by ≥1 mutant (`19/19`, `28/28`).

## 2. Part 1 — escapes from the draft C2 kill-sets

Baseline (unmodified tools, draft kill-sets):

* mimeglob — `SELFTEST_STRENGTH: OK tool=tools/mado-mimeglob.py kills=17 held=17 survived=0 wrong_check=0` rc 0
* portals — `SELFTEST_STRENGTH: OK tool=tools/mado-portals.py kills=27 held=27 survived=0 wrong_check=0` rc 0

| tool | draft kills | weakenings tried | green | flagged | **escaped** | escaped + closer verified |
|---|---|---|---|---|---|---|
| mimeglob | 17 | 79 | 79 | 60 | **19** | 19/19 |
| portals | 27 | 112 | 112 | 89 | **23** | 22/23 |

**42 weakenings keep the selftest green and are not flagged by the gate with the draft kill-sets.**
Every one is a *component* weakening, not a label gap: the draft kill-sets name all 47 labels, so a total
tautology of any check is always flagged; what escapes is "the check still fails on *its* kill, but no longer
constrains the other component of its assertion".

Escapes, by class:

| tool | class | rows | what the weakened check no longer constrains |
|---|---|---|---|
| mimeglob | `drop-type` (10) | t01,t02,t03,t07,t08,t10,t11,t13,t16,t17 | the returned type (only `uncertain` is compared) |
| mimeglob | `drop-uncertain` (8) | t02,t03,t05,t06,t08,t09,t12,t14 | the `uncertain` flag (only the type is compared) |
| mimeglob | `any-non-unknown` (1) | t09 | everything but "not application/octet-stream" |
| portals | `drop-picks` (12) | 599,601,603,604,611,614,629,632,645,649,651,653 | the backend list (only the reason string is compared) |
| portals | `drop-reason` (7) | 604,611,613,617,621,629,647 | the reason string |
| portals | `len-only`/`drop-first`/`drop-short`/`drop-wellformed` (4) | 622,623,624×2 | the value/order/one of the three clauses |

The full rows (id, label, class, `find`, `replace`, the gate line that shows `OK:0`, the closer, its `must_fail`,
and both verification lines) are in `R95MMutC2-escapes-mimeglob.json` and `R95MMutC2-escapes-portals.json`.

Representative rows (the pair is the whole reproduction; each `find` occurs once in the selftest):

| id | find → replace | gate on the weakened tool |
|---|---|---|
| `mimeglob-605-drop-type` | `("t01 simple suffix", g(b"a.txt", ["a/mime"]) == ("text/plain", 0)),` → `("t01 simple suffix", g(b"a.txt", ["a/mime"])[1] == 0),` | `OK:0` |
| `mimeglob-609-drop-uncertain` | `… == ("app/hi", 1)),` → `…[0] == "app/hi"),` | `OK:0` |
| `portals-599-drop-picks` | `chk("default list first backend", r.resolve(SS) == (["hyprland"], "default config"))` → `chk(… , r.resolve(SS)[1] == "default config")` | `OK:0` |
| `portals-614-drop-picks` | `chk("no backend", r.resolve(IMPL + ".Secret") == ([], "no-backend"))` → `chk(…, r.resolve(IMPL + ".Secret")[1] == "no-backend")` | `OK:0` |
| `portals-624-drop-short` | `chk("bus name validity", is_bus_name("org.a.b") and not is_bus_name("org") and not is_bus_name("org.1a"))` → same without the last clause | `OK:0` |
| `portals-623-drop-first` | `chk("string list trailing empty dropped", string_list("a;b;") == ["a", "b"] and string_list("a;;b") == ["a", "", "b"])` → the second conjunct only | `OK:0` |

## 3. Closing kills (merge-ready)

| file | kills | closes | verification |
|---|---|---|---|
| `R95MMutC2-closing-mimeglob.json` | 5 | 19 escapes | each: `WEAK:1` on the weakened tool, `OK:0` on the pristine tool with the same kill-set |
| `R95MMutC2-closing-portals.json` | 13 | 22 escapes | same |

Five closers suffice for mimeglob because one mutant whose FAIL set spans ten single-type checks (`g30`: the
single-type branch answers `application/octet-stream`, so the type is wrong and `uncertain` right) breaks every
`drop-type` escape at once; `g02`/`g31`/`g32` cover the `drop-uncertain` family (uncertainty wrong, type right);
`g18` covers the three `drop-type` rows of the "unknown" checks. Example entries:

| closer | production defect | `must_fail` | closes |
|---|---|---|---|
| `r95m-close-g30-single-unknown` | `guess`: the single-type branch answers `UNKNOWN` instead of the found type | the 10 `uncertain=0` checks | 7 rows |
| `r95m-close-g31-multi-certain` | `guess`: the multi-type branch answers `uncertain 0` | t05, t12 | 2 `drop-uncertain` rows |
| `r95m-close-p35-default-picks-first` | `find`: the "default config" answer names the first sorted backend instead of the one the list picked | 8 checks | 5 `drop-picks` rows |
| `r95m-close-p04-usein-any` | `_usein`: any backend with a `UseIn` line matches every desktop | 6 checks | 4 rows |

All 32 closers hold at full strength on the pristine tools (verified), so appending them to the frozen kill-sets
does not turn the gate WEAK on the unmutated tools.

## 4. The one escape no single production mutant can close — `portals-629-drop-picks`

Weakening: `chk("Encoding other than UTF-8 in the first group voids the file", r.resolve(FC) == (["gtk"],
"gtk-last-resort"))` → `… r.resolve(FC)[1] == "gtk-last-resort"`.

In that fixture (`base | {"kde.portal": kde + "Encoding=ISO-8859-1", "portals.conf": "[preferred]\ndefault=kde"}`,
desktop `XFCE`) the KDE backend is voided by the Encoding rule, so the only backend left that supports
`FileChooser` is `gtk`, and `_gtk` requires `i.supports(iface)`. Therefore **whenever the reason is
`gtk-last-resort` the picks are `["gtk"]`** — the reason implies the picks on this fixture, and no production
mutant can make the reason right while the picks are wrong. The whole 41-mutant portal catalogue was tried and
none closes it; every mutant that changes the fallback backend (`p34`) also fails the four sibling
`gtk-last-resort` checks *and never enters this check's fail set*, so it cannot serve as this check's kill.

This is a **latent** escape, not a live one: it can only be exploited by a fixture change (a second
`FileChooser`-capable backend in the same fixture). Recommendation to the L1: keep the check, do not chase a
closer; if the point matters, add a check whose fixture has two `FileChooser` backends (then the reason does not
determine the picks and `p34`-class mutants become closers).

## 5. Part 2 — counter mutants of the draft C2 counter

16 mutations of `quality/counters/c2-r95-selftest-kills.py` (each `find` occurs exactly once in the current
bytes — re-checked after the counter was revised mid-wave, which added conjuncts (viii)
`singles[0] + singles[1] >= MIN_SINGLETON_LABELS` (36) and (ix) `all(len(panel_n[t]) >= 2 …)`), run in **draft
mode** over a 15-probe matrix: P0 the real draft kill-sets with the round panel (baseline `DRAFT_TARGET_MET`); P1 empty
kill-sets; P2/P3/P5/P10 pin drifts (kills / gate / tool / control); P6 control = the strong kill-set; P7 a panel
whose "neutral" entry is a real weakening; P8 panel sha drift; P9 a panel whose neutrals are byte-identical;
P11 a scratch fixture repo (created, committed and verified with `git -C`) whose gate prints the right verdicts
and exits 1 on the real tool's non-drift (positive) invocation only, leaving its own `--selftest` green; P12 a panel whose hand entry is one of §2's escaping weakenings; P13
a kill-set covering only the panel's 24 hand labels; P14 the reviewer's blanket union-covering forgery
(`R95MReviewC2-forged-*.json`, one kill naming every label — it *holds* at full strength on both pristine tools,
`kills=1 held=1`, measured); P19 a panel with one neutral edit per tool; P20 the draft kill-sets minus their
multi-label kills. A mutant is **KILLED** when the probe's `DRAFT_*` line or rc differs from the unmutated
counter's line on the same probe, **SURVIVED** otherwise. Every probe was run against the unmutated counter first:
exactly one (`P0`) prints `DRAFT_TARGET_MET`; all others print `DRAFT_TARGET_MISSED` or `SETUP_ERROR`, so each
mutant is compared to a probe baseline that already discriminates. (The 14 original mutants were first measured
against the earlier counter revision over the full matrix; every row below was re-measured against the current
bytes on its witness probe, and the one verdict that changed — C05 — is recorded as such.)

| mutant | change | conjunct that catches it | witness probe | verdict |
|---|---|---|---|---|
| C01-gate-pin-true | `gate_pin = sha(gate_b) == …` → `True` | (i) `gate_pin` | P3 | KILLED |
| C02-kills-pin-true | `kills_pin = [...]` → `[True, True]` | (i) `all(kills_pin)` | P2 | KILLED |
| C03-tool-pin-true | `tool_pin = [...]` → `[True, True]` | (i) `all(tool_pin)` | P5 | KILLED |
| C04-positive-prefix | `p == "OK:0"` → `p.startswith("OK")` | (i) positive | P11 | KILLED |
| C05-nflag-vacuous | `nflag == len(neut_j)` → `nflag >= 0` | (ii) neutralised | P13, P20 | **SURVIVED** (see below) |
| C06-hflag-vacuous | `hflag == weak_total - len(neut_j)` → `>= 0` | (iii) hand_flagged | P12 | KILLED |
| C07-zok-vacuous | `zok == len(nonw_j)` → `zok >= 0` | (iv) neutral_ok | P7 | KILLED |
| C08-dn-vacuous | `dn < weak_total` → `True` | (v) `dn` arm — **no witness exists** | — | SURVIVED |
| C09-aok-lax | `aok < weak_total` → `aok <= weak_total` | (v) `aok` arm — **no witness exists** | — | SURVIVED |
| C10-shadiff-lax | `sd_zok < len(nonw_j)` → `<=` | (v) `sd_zok` arm | P9 | KILLED |
| C11-alwaysweak-lax | `all(v != "OK:0")` → `all(v != "SETUP_ERROR:2")` | (v) always-WEAK arm — **no witness exists** | — | SURVIVED |
| C12-control-lax | `ctl_h < …` → `ctl_h <= …` | (vii) control | P6 | KILLED |
| C13-ctl-pin-off | control kill-set sha pin dropped | the **setup guard** (not a conjunct) | P10 | KILLED |
| C14-neutralise-off | `neutralise()` returns the text unchanged | (ii) (and everything) | P0 | KILLED |
| C15-singleton-floor-off | `singles[0] + singles[1] >= MIN_SINGLETON_LABELS` → `>= 0` | (viii) singleton floor | P14 | KILLED |
| C16-panel-neutral-floor-off | `all(len(panel_n[t]) >= 2 …)` → `and True` | (ix) panel-neutral floor | P19 | KILLED |

Reading of the survivors. **C08/C09/C11 are equivalent mutants, and that is the finding.** In the counter,

* `dn` is computed over variants that the setup step has already forced to have the *identical* result line, so
  `dn == 0` on every run the counter can reach ⇒ `dn < weak_total` is a constant (true);
* `aok` is the number of weakenings that the hardcoded `ALWAYS_OK` stub marks `WEAK:1`, i.e. always 0 ⇒
  `aok < weak_total` is a constant;
* `aw` is the hardcoded `ALWAYS_WEAK` stub on the pristine tools, i.e. always `WEAK:1` ⇒
  `all(v != "OK:0" …)` is a constant.

So conjunct (v) of PRED-C2-r95-v1 has **one live arm** (`sd_zok < len(nonw_j)`) and three decorative ones.
Deleting any of the three changes no verdict on any input the counter accepts (C08/C09/C11 each survived the 9
probes they were run on, including the fixtures built to expose them). This is a statement about the predicate, not a hole the
kill-sets could close.

Also measured, and worth the L1's attention:

* **P13** (a kill-set covering only the panel's 24 hand labels) is now rejected by **(viii)** (24 singleton labels
  < 36) as well as by (ii) (`neutralised_flagged=24/47`); at the earlier revision it was rejected by (ii) alone.
* **P12** (a panel whose hand entry is one of §2's escaping weakenings) is rejected by (iii) with
  `hand_flagged=23/24` on a kill-set that names all 47 labels. The two parts of this seat meet here: an escaping
  weakening *is* what a hand weakening looks like when the kill-set is label-complete.
* A **blanket union-covering forgery** (R95MReviewC2's single kill whose `must_fail` names all 19 / all 28
  labels) *holds* at full strength on the pristine tool (`gate … kills=1 held=1` rc 0, measured) and flags every
  weakening, so escape analysis alone cannot reject it. The counter rejects it through **(viii)**: the forgery has
  0 singleton labels (P14 baseline `DRAFT_TARGET_MISSED`), and with (viii) deleted the same input prints
  `DRAFT_TARGET_MET` (C15).

## 6. Findings for the L1

1. **The draft kill-sets are label-complete but component-blind.** 42 of 191 green weakenings escape (19/79
   mimeglob, 23/112 portals). The mechanism is uniform: `must_fail` matches a *label*, and every escape keeps the
   label failing on its own kill while dropping one component of the assertion. A kill-set cannot see this; only
   per-check weakenings (the panel) can — and the panel's hand entries are exactly this class.
2. **32 closing kills are ready to merge** (5 mimeglob for 19 rows, 13 portals for 22 rows), verified
   `WEAK:1`/`OK:0` in both directions. Merging them does not disturb the pristine baseline.
3. **One escape (`portals-629-drop-picks`) is unclosable** by any single production mutant: on that fixture the
   reason string determines the picks. It is latent, not live; no kill should be invented for it.
4. **Conjunct (v) is 3/4 decorative** (C08, C09, C11 survive every probe; each arm is a constant of the
   hardcoded stubs and of the green-variant rule). If the L1 wants (v) to mean something, the arms must be
   computed from something that can vary.
5. **(ii) is the arm that rejects a hand-only kill-set; (iii) rejects a hand weakening that escapes; (vii) does
   not subsume either.** Measured at P13 and P12 respectively.
6. **Escape analysis cannot reject the blanket forgery**; it flags everything, so it is "strong" by construction
   (measured: `SELFTEST_STRENGTH: OK … kills=1 held=1` on both pristine tools). The counter's new conjunct (viii)
   *does* reject it — C15 is the measurement: delete the singleton floor and the blanket set becomes
   `DRAFT_TARGET_MET`. Keep (viii); it is the only surviving guard against a union-covering kill-set now that
   escape analysis is blind to it.
7. **New conjunct (ix) is live and load-bearing** (C16, witness P19), and **(ii) is now hard to isolate** once
   (viii) exists (C05): the two arms overlap on every kill-set the draft can generate. If the L1 wants (ii) to be
   independently observable, the panel or the singleton floor should be arranged so that coverage and singleton
   count can be varied independently.

## 7. Evidence files (written this seat, all under `.ufo/waves/round-95/w1/`)

| file | sha256 | content |
|---|---|---|
| `R95MMutC2-escapes-mimeglob.json` | `3fdd524ab1e24c5124207da40f53f048583c952022107fb37d201bc2b4842cb2` | 79 rows, 19 escapes with find/replace, gate lines, closers |
| `R95MMutC2-escapes-portals.json` | `b86ad6ca9d6d26eb9f57b4f37e9c62f59e62beedc3b684770a0f60cf04f16a63` | 112 rows, 23 escapes, 22 closed, 1 unclosable |
| `R95MMutC2-closing-mimeglob.json` | `559b0e451fe9ff3239d587d7e0950cd339cdd2361b531a0d9a7784396a2f2f64` | 5 closing kills (kill-set schema) |
| `R95MMutC2-closing-portals.json` | `3f30d9e39ea6d84bb0a18e01e722109b2c67b4942a6086e899bc6febd1cdab93` | 13 closing kills + the `unclosable` note of §4 |
| `R95MMutC2-counter-mutants.json` | `f2fa4e94382a8c5438442616d0aafc371a304be0f49607828a13147e0e167e81` | 17 rows (16 mutations; C05 measured on two probes): 12 killed, 3 equivalent, 1 uninhabitable with this probe set; per row: conjunct, witness probe, `find`/`replace`, baseline and mutant `DRAFT_*` lines |

The two escapes files carry, per row: `id`, `label`, `case`, `find`, `replace`, `green`, `gate` (the `OK:0`
verdict), `gate_line`, `closer.{id,find,replace,must_fail,source_mutant}`, `closer_fails_weakened`,
`close_gate`/`close_line`, `pristine_gate`/`pristine_line`.

## 8. Commands run (all from `$S`, `TMPDIR=$S`, absolute paths for every lane file)

| command (abridged) | exit |
|---|---|
| `python3 -I tools/mado-mimeglob.py --selftest` (baseline) | 0 — `checks=19 failed=0` |
| `python3 -I tools/mado-portals.py --selftest` (baseline) | 0 — `checks=28 failed=0` |
| `python3 weaken.py --verify-only` (191 weakenings) | 0 — 191/191 green |
| `python3 pool.py` (74 candidate mutants) | 0 — 64 usable, 19/19 + 28/28 labels covered |
| `python3 escape2.py --tool mimeglob --kills draft-glob.json` | 0 — 79/60/19, closed 19/19 |
| `python3 escape2.py --tool portals --kills draft-port.json` | 0 — 112/89/23, closed 22/23 |
| `python3 -I quality/counters/c2-r95-selftest-kills.py … --draft-kills draft-glob.json,draft-port.json` | 3 (DRAFT) — `DRAFT_TARGET_MET … neutralised_flagged=47/47 hand_flagged=24/24 control_hand_flagged=21/24` |
| `python3 counter_mut*.py` (mutant matrices, first revision) and `python3 lean.py` (re-measurement at `983d4cbc…`) | 0 |
| `git -C <fixture> init/add/commit`, `git -C <fixture> rev-parse --show-toplevel` | 0 — the toplevel was checked against the fixture dir before the first commit (both fixture repos, `fxPsGKIs` and the re-run's `fx*`); the fixture is the only repo this seat mutated |

No installs (nothing fetched, no package manager run, nothing added to any PATH directory). No host writes: no
`update-mime-database`, no `xdg-*` command, no service or sysctl touched, no home file read. Scratch
`$S=/fast/scratch/hyaku/mado-r95/R95MMutC2` (including the fixture repo `fxPsGKIs`) was deleted after the
evidence files were copied out.

## 9. Named limits

* The weakening catalogue is **generated from the two selftests as they stand**; a weakening class I did not
  generate cannot be reported as an escape (or as flagged). 191 rows over 47 checks: 2–4 per check plus the
  shared forms.
* A "closer" is only as good as the 64-mutant pool: §4's unclosable claim is a claim about that catalogue plus the
  fixture reasoning given there, not a proof over all programs.
* The counter mutants were measured on **my** probe matrix (14 probes) — with the real draft kill-sets for P0 and
  the round panel for every panel probe — not on a frozen measurement matrix (the counter freezes later).
* Every verdict here is a DRAFT verdict; the frozen kill-sets/panel may differ from the drafts analysed.
