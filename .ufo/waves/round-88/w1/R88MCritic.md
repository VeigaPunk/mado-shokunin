# R88M — critic, round 88 wave w1

Seat: critic. Scope: attack `claims-declaration-r88.md` (C1 coverage capability, C2 operability), not the code.
No candidate scoring was run: no `c1-r88-mako-fields.py` / `c2-r88-include-containment.py` invocation was made over
either authored case file. What I ran is listed in §5 with exit codes. Scratch `S=/fast/scratch/hyaku/mado-r88/R88MCritic`
was created for fixtures and removed at exit (and is gone when this file is read).

Bottom line: **C1 WEAKENED, C2 WEAKENED**. Neither FALLS. I could not construct a cheap control that reaches either
frozen target, and both before→after moves are real and independently observable on the host. The weaknesses are
predicate/control-completeness and two unmeasurable sentences, all cheap to fix before the freeze.

---

## C1 — coverage capability: mako criteria fields + upstream boolean grammar

### (a) Cheapest do-nothing control, and whether the predicate covers it

**Named control: `flags-accepted-ignored`** — the r87 resolver with the round-88 argparse flags added and all
notification inputs discarded (`resolve(..., inputs={}, flags={})`). It represents a resolver that accepts the new
CLI surface and resolves nothing new. It is **not in the predicate's control list**
(`naive-toplevel`, `globals-include`, `base-tool`), and no control in `quality/counters/c1-r88-mako-fields.py`
implements it.

Second finding, sharper: **the `base-tool` control is CLI-contaminated and proves nothing about resolution.**

```text
python3 -I $S/mado-mako.base.py --config ~/.config/mako/config --home /home/vgpnk --category work
mado-mako.py: error: unrecognized arguments: --category work            rc=2
```

`c1-r88-mako-fields.py::run_tool` puts every supplied new field on argv, and `R87.tool_verdict` fails any run whose
rc != 0 (counter line `if proc.returncode != 0: return False, f"exit={...}"`). At `--base-rev 24ba2a9` the tool has no
`--app-icon/--summary/--body/--category/--desktop-entry/--actionable/--expiring`, so **every case that exercises a new
field is auto-failed by argparse**, not by a wrong resolution. `base_correct < N` is therefore guaranteed by the flag
surface. The declaration's sentence "The command that would show this unmoved: the C1 counter's base-tool control …
on the same cases" overstates what that control shows.

The genuine guard against `flags-accepted-ignored` is the mutant battery, not the controls: M11 `string-mismatch-ignored`,
M12 `string-missing-input-matches`, M15 `bool-criteria-inverted`, M16 `bool-missing-input-matches`. A case set on which
the ignored-flags tool scores N would leave all four alive, so TARGET_MISSED. That guard exists but is stated nowhere.

**Minimal fix (a):** either (i) add `flags-accepted-ignored` as a fourth control — the candidate evaluated with
`inputs={}, flags={}` through `evaluate()`, exactly as the C2 counter runs `refuse-all-includes` — or (ii) one sentence in
the predicate: "M11, M12, M15 and M16 are the guard against an ignored-inputs control; a case set on which that control
reaches N kills none of them", plus "`base-tool` is a CLI-surface control: at the base revision the new flags do not
parse, so it exits 2 on every new-field case."

### (b) Is the axis named by the surface, or by the number produced?

The surface move is real and independently observable, and it is not produced by the case file:

- Manual L443-469 lists twelve first-pass criteria fields; `build/mado-mako.c2.py:94-95,91` supports all but `summary~`,
  `body~`, i.e. 10/12 as declared. Verified line numbers: `zcat /usr/share/man/man5/mako.5.gz | sed -n '440,530p'`.
- Host evidence, not case evidence — the round-87 tool cannot resolve the host's DND state, the candidate can:

```text
base  24ba2a9 … --mode do-not-disturb  → invisible=0  refusals=9   (refuses core.ini:15 invisible='true',
                                                                     :18 invisible='false')
c2 cand.      … --mode do-not-disturb  → invisible=1  refusals=8
```

  `~/.local/share/omarchy/default/mako/core.ini:15` is `invisible=true` and `:18` is `invisible=false`, both under
  `[mode=do-not-disturb]`. Upstream `types.c parse_boolean` is `strcasecmp("true") || strcmp("1")`, matching
  `mado-mako.c2.py:166-173` exactly.

**But the counter measures correctness over a case set; the axis is field coverage, and nothing binds the two.** No
assertion requires that each of the ten supported field names, each boolean literal form (`true`, `false`, `1`, `0`, bare,
`!`), and both case outcomes appear in at least one case. On the current machinery a tool could be a no-op on, say,
`desktop-entry` and still reach N/N if no case names it (the mutants kill only what the cases exercise).
A closure could call C1 "quality" — the r87 survivors are re-scored inside the same atomic predicate — and the
declaration gives it no way to see the coverage mass.

Also: one of the ten counted fields is value-incomplete. Upstream `types.c parse_urgency` accepts `high` as an alias for
`critical` (`strcasecmp(string, "high") == 0 → MAKO_NOTIFICATION_URGENCY_CRITICAL`), and `criteria.c:apply_criteria_field`
routes the `urgency` value through `parse_urgency`. The candidate refuses it:

```text
config: [urgency=high]\nwidth=444   with --urgency critical
  → width 300 (default), refusal: "urgency 'high' is not low, normal or critical"
config: [urgency=critical]\nwidth=444 → width 444, refusals []
```

Reproduced at `build/mado-mako.c2.py:341` (`if key == "urgency" and value not in URGENCIES`). A field count of ten is
honest as a field count; it is not a claim that the urgency field is fully modelled. Name it, as `summary~`/`body~` are named.

**Minimal fix (b):** (i) state the case-set split explicitly (how many of the 40–64 cases exercise the seven added fields,
how many the five r87 survivors) so the coverage mass is visible; (ii) add a mechanical, cheap coverage assertion to the
counter's selftest or `run()` — every name in `STRING_INPUT_FIELDS + BOOLEAN_FIELDS` appears in ≥1 case's `args`, and each
of `true/false/1/0/bare/!` appears in ≥1 criteria header; (iii) add `urgency=high` to the named limits, or accept it.

### (c) Universal clauses, unmeasurable words, declaration-vs-docstring divergence

Checks that pass:

- The predicate sentence is **literatim identical** between the declaration §C1 and the counter docstring
  (`c1-r88-mako-fields.py:3-6`): same N, same M, same carried count, same three control names, same "strictly below N".
- Receipt label `MADO_MAKO_FIELDS` matches the counter's printed label.
- Mutant sha pin `40645a28…761d49b` == `sha256sum .ufo/waves/round-88/controls/mako-mutants-r88.json`; the file carries
  exactly 19 mutants, M01–M10 carrying r87's anchors.
- `CARRIED_CASES = 22` equals the round-87 case count (`len(.ufo/waves/round-87/controls/mako-cases-r87.json["cases"]) == 22`).
- All 19 anchors occur exactly once in **both** `build/mado-mako.c1.py` and `build/mado-mako.c2.py`, so the C1 harm-check
  re-run at B is well-formed and does not degrade into `setup-error count=0` lines. (M11–M19 occur 0× in the base tool,
  as the declaration says.)

Two real defects:

1. **A missing mutant anchor is scored as a capability miss, not a setup error.** `evaluate()` does
   `results.append({"status": f"setup-error count={count}", "killed": False})` and continues, so the run exits 1
   `TARGET_MISSED`. The predicate's clause "all M mutants are killed" presupposes the mutants exist on the measured tool.
   The C2 counter gets this right for its forgery anchor (`if tool_text.count(FORGERY_OLD) != 1: raise SetupError`).
   Under the freeze-before-scoring rule, a build-seat edit that renames an anchor would leave a *scored* run that reads
   like a capability failure. **Fix:** raise `SetupError` on `count != 1` for the measured tool (exit 2), as C2 does.
2. **The carried set is read at `REV`, unpinned.** `carried_count(cases, git(repo, "show", f"{commit}:{R87_CASES_PATH}"))`.
   The r87 counter run pinned the r87 case file at `0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3`
   (round-87 spot-check §2). Without that pin, "the 22 frozen round-87 cases are carried unchanged" is
   relative to whatever the r87 file says at the measured revision — a second authority for "frozen".
   **Fix:** add `--expect-r87-cases-sha256` and compare, exactly as `--expect-cases-sha256` works.

Minor, worth one line each: the base-tool control's CLI contamination (see (a)); "the candidate tool's correct count equals N"
is measured, fine.

### (d) Causal separability as declared

Holds, and it is stronger than the declaration argues: **the two case schemas cannot express each other's surface.**
`c1-r88-mako-fields.py` has `ARG_NAMES = STRING_ARGS + ("urgency",) + BOOL_ARGS + ("mode",)` and rejects any other key
(`{cid}.args: unknown or non-object args`) — there is no `read-root`; its `run_tool` never passes `--read-root`.
The C2 schema has `files/config/home/read_roots/expect` and no notification-arg key at all. So "C1 needs no C2 byte /
C2 needs no C1 byte" is a construction fact, checkable by reading two dicts, and it is true.

One gap in wording: the declaration states separability as a property of the cases but measures C2's before-state at A
(C1 already landed). "C2 needs no C1 byte" is therefore an argument, not a measurement. **Fix:** say "by case-schema
construction (the C1 schema has no `--read-root` key; the C2 schema has no criteria key)" instead of leaving it to be
read as measured.

### (e) not applicable to C1 — see C2(e) for the host include chain.

### (f) Is "capability acquisition" earned if C1 meets its predicate?

**Yes, per AXES.md §Capabilities** — "Rows enter only through a round that demonstrates the capability running; a
capability without a passing demonstration in the round report is pre-claiming and does not enter the table."
TARGET_MET is exactly a demonstration (N/N over a 40–64 case set, 19/19 mutants killed, three controls strictly below N),
and the host-chain probe corroborates it independently of the case file. The nudge analysis is also correct: the last
capability rows are round 82 (`SCORECARD.md:4787-4788`), the window is N=3 (`SCORECARD.md:282-284`), so r83–r87 exceed it.

Two conditions on the row:
- The row's one line must carry the named limits (`summary~`, `body~` refused; `urgency=high` refused) or it over-claims
  a fields-complete resolver.
- The declaration should state the failure consequence explicitly: **if C1 misses, the round has no capability move and
  the nudge obligation is unmet** — it currently says only "Capability row on TARGET_MET only", which leaves the reader
  to infer that a miss is still a capability round. (This is the r87 failure repeated.)

---

## C2 — operability: include= containment under declared read roots

### (a) Cheapest do-nothing / cheap control, and coverage

**Covered, and I could not beat it.** The case file that landed during this seat
(`.ufo/waves/round-88/controls/containment-cases-r88.json`, K=17) is 9 `refusals: present` and 8 `refusals: none`.
The cheapest do-nothing control is the base tool: it has no `--read-root`, so `k13-outside-under-read-root` and
`k14-symlink-into-read-root` exit 2, and it satisfies no escape case (`missing-refusal`). The cheapest *blanket* control
is the declared `refuse-all-includes` forgery: it passes exactly the nine refuse-cases and fails all eight positives →
9/17 < 17. The counter's own selftest asserts the boundary case ("without positive cases refuse-all forgery reaches K →
TARGET_MISSED", `c2-r88-include-containment.py` selftest), so a future case file with zero positives cannot pass.
This is the correct construction and it is measurably better than the r85/r86 pattern the declaration cites.

### (b) Operability moved by the surface or by the number?

The surface is a new `--read-root` flag plus a refusal reason — a runnable artefact. But the declaration's before→after
is given only as a counter verdict (`Before: the counter at the C1 content revision (no containment) → TARGET_MISSED`).
AXES.md defines operability as "a checklist item can be run and produces the stated outcome"; a closure reading this
declaration cannot see the stated outcome without running the counter. **Minimal fix:** quote the two runnable commands
and their outputs (the same pair the case set encodes), e.g.
`--config <esc>/config.ini --home <home>` → rc 0, `applied: []`, refusal naming `… -> <outside>/secret.ini`;
and the in-home control → rc 0, `applied: ["include:…"]`, `refusals: []`. Cheap, and it makes the axis name re-derivable.

Also: the stance's **cost** is stated in the C2 defect paragraph ("mako itself opens any absolute include … so this is a
lane stance") but appears nowhere as a named limit and has **no case**. A mako-valid absolute include outside the roots is
refused by the candidate where mako would read it. Name it as a limit the way C1 names `summary~`/`body~`, and add the
case (`mako-valid absolute include outside roots → refused`, `refusals: present`), so the cost is measured rather than
asserted.

### (c) Universal clauses, unmeasurable words, declaration-vs-docstring divergence

Passing: predicate sentence is literatim identical in declaration §C2 and `c2-r88-include-containment.py:3-8`; label
`MADO_MAKO_CONTAINMENT` matches; mutants sha `49373eee…c6a084a85` matches `sha256sum`; five mutants K1–K5 match
`DECLARED_MUTANTS = 5`; K1–K5 anchors each occur exactly once in the candidate (`K1-containment-skipped` is the same
anchor as the forgery — 1×, so the forgery substitution and the mutant substitution cannot collide); a missing forgery
anchor raises `SetupError` (exit 2) — correct.

Three defects:

1. **"refused before it is stat'ed or opened" is literally false and unmeasurable.** `build/mado-mako.c2.py:420` calls
   `os.path.realpath(target)` *before* the check, which resolves each component with `lstat`/`readlink`; the containment
   test is what the stats are for. No case can observe syscall order (cases read stdout only). **Fix:** "refused before its
   contents are opened; the path is resolved only to test containment."
2. **The credential-material parenthetical is unmeasured and misleading.** "which also serves mado's credential-material
   rule" reads as credential protection; the stance is root containment. Demonstrated counterexample inside a declared root:

```text
home/.ssh/id_test contains "format=LEAKED-FROM-HOME-SSH"
config: include=~/.ssh/id_test   (--home <home>)
candidate → applied ["global-section", "include:…/home/.ssh/id_test"], format='LEAKED-FROM-HOME-SSH', refusals []
```

   The file is read and its content becomes effective state. The sentence is literally true only in its parenthesis
   ("never reads outside the boundary the operator named"). **Fix:** narrow it to "bounds the read set to the declared
   roots; it does not classify credential material inside a root, so a root that contains secrets is read as declared."
3. **Case-set gaps against the declared surface:** (i) the host's actual shape is a *config symlink* —
   `readlink -f ~/.config/mako/config` → `~/.config/omarchy/current/theme/mako.ini` — and no case exercises
   `--config` itself being a symlink (k15 covers only config-outside-home); (ii) no credential-shaped in-root case, per
   defect 2. Both are one case each.

### (d) Causal separability as declared

Holds by schema (see C1(d)): the C2 counter never passes a notification input, so no C1 byte can change a C2 verdict;
the C2 stance code is reachable without any criteria-field code. The `--config`/`--home`/`--read-root` argv surface is
identical at A and B. No measurement is missing for the claim as written; the "C2 needs no C1 byte" sentence should be
labelled a construction argument (see C1(d)).

### (e) Operability gain or a refusal that makes the tool less useful? Does the host chain resolve?

**The host chain resolves. Verified read-only.**

```text
readlink -f ~/.config/mako/config           → /home/vgpnk/.config/omarchy/current/theme/mako.ini   (config is a symlink)
grep -n include …/mako.ini                  → 1:include=~/.local/share/omarchy/default/mako/core.ini
readlink -f ~/.local/share/omarchy/…/core.ini → itself (no symlink)
python3 -I .ufo/waves/round-88/build/mado-mako.c2.py --config ~/.config/mako/config --home /home/vgpnk \
        --app-name x --urgency normal
   → rc 0, resolved=37, refusals=5 (all five are `summary~` "outside the model" at core.ini:24,27,30,33,36)
   → applied ["global-section", "include:/home/vgpnk/.local/share/omarchy/default/mako/core.ini"]
```

The symlinked `--config` is carried by the declared exemption, the `~/` include resolves inside `--home`. So the stance is
an operability **gain** on the measured surface, not a blanket refusal: escapes are refused with a reason that names the
fix (`declare it with --read-root to read it`), and I verified the refusal fires for the symlink escape and for the
`<home>-evil` prefix sibling:

```text
include=~/cfg/escape.ini (→ <S>/fx/outside/secret.ini)  → applied [], refusal "…resolves outside the declared read roots…"
include=<S>/fx/home-evil/x.ini                          → applied [], refusal "…resolves outside the declared read roots…"
```

The one loss is real and recoverable: an absolute include outside the roots (mako-valid) is refused unless `--read-root`
names it. That is a tradeoff, not a defect — but it must be declared as a limit and have a case (see (b)).

### (f) not applicable (C2 declares no capability row).

---

## Verdicts and the minimal change before the freeze

| claim | verdict | reason |
|---|---|---|
| C1 coverage capability | **WEAKENED** | Surface move is real and host-corroborated, but the cheapest control (`flags-accepted-ignored`) is unlisted, `base-tool` is CLI-contaminated so its low score carries no semantic information, the counter measures correctness while the axis is field coverage (nothing binds 10/12 to the case set), a missing mutant anchor scores as a capability miss instead of a setup error, the carried r87 set is read at `REV` unpinned, and `urgency=high` is refused though upstream maps it to critical. |
| C2 operability (containment) | **WEAKENED** | Predicate, controls and mutant pins are sound (9 negatives / 8 positives; forgery ≤ 9/17; no-positive runs proven to fail), and the host chain resolves; but "refused before it is stat'ed" is false, the credential-material parenthetical is unmeasured and demonstrably not what the stance does, and the case set omits the host's config-symlink shape and the stance's stated cost. |

Neither claim FALLS: no cheap control reaches either target under the frozen predicate as written, both surfaces are
demonstrably moved, and every control the predicate does name is genuinely below N.

**Minimal edits, in priority order, all cheap:**

1. C1 counter: `SetupError` on `count != 1` for a mutant anchor of the measured tool (mirror the C2 forgery-anchor rule).
2. C1 counter + command: `--expect-r87-cases-sha256` pinned to `0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3`.
3. C1 predicate: add `flags-accepted-ignored` as a fourth control **or** the one sentence naming M11/M12/M15/M16 as its guard,
   plus the sentence that `base-tool` is a CLI-surface control (rc 2 on new flags at `24ba2a9`).
4. C1 declaration: state the case-set split (new-field cases vs r87-survivor cases) and add `urgency=high` to the named limits
   (or accept it); add the "if C1 misses, the nudge obligation is unmet" sentence.
5. C2 declaration: replace "before it is stat'ed or opened" with "before its contents are opened"; narrow the
   credential-material parenthetical to root containment; add the cost sentence (mako-valid absolute include outside the
   roots is refused; `--read-root` recovers it).
6. C2 case file (still in w1, so still cheap): add `config-is-a-symlink` (host shape) and `credential-shaped file inside
   `--home` is read` as a declared limit case; add the outside-roots cost case. Re-pin `--expect-cases-sha256` afterwards.
7. Both declarations: quote one runnable before/after command pair per claim, so the axis name is re-derivable without
   running the counter.

---

## 5. Commands run (with exit codes)

| # | command | rc | observed |
|---|---|---|---|
| 1 | `readlink -f ~/.config/mako/config` | 0 | `/home/vgpnk/.config/omarchy/current/theme/mako.ini` (config is a symlink) |
| 2 | `grep -n include` on that file and on `~/.local/share/omarchy/default/mako/core.ini` | 0 / 1 | include line at mako.ini:1; no include in core.ini |
| 3 | `readlink -f ~/.local/share/omarchy/default/mako/core.ini` | 0 | itself (no symlink); 38 lines |
| 4 | `python3 -I .ufo/waves/round-88/build/mado-mako.c2.py --config ~/.config/mako/config --home /home/vgpnk --app-name x --urgency normal` | 0 | `resolved=37 refusals=5`, all five `summary~` refusals |
| 5 | `git show 24ba2a9:tools/mado-mako.py > $S/mado-mako.base.py`, then same invocation | 0 | resolved, `refusals=7` |
| 6 | base tool with `--category work` | 2 | `unrecognized arguments: --category work` |
| 7 | base vs candidate with `--mode do-not-disturb` | 0 / 0 | base `invisible=0 refusals=9`; candidate `invisible=1 refusals=8` |
| 8 | `python3 -I quality/counters/c1-r88-mako-fields.py --selftest --scratch-root $S` | 0 | `SELFTEST: passed=15/15` |
| 9 | `python3 -I quality/counters/c2-r88-include-containment.py --selftest --scratch-root $S` | 0 | `SELFTEST: passed=12/12` |
| 10 | `python3 -I .ufo/waves/round-88/build/mado-mako.c2.py --selftest --scratch-root $S` | 0 | `checks=45 failed=0` |
| 11 | anchor-count script over the 19 C1 and 5 C2 anchors × {c1, c2, base} | 0 | all 19 unique in c1 and c2, 0 in base for M11–M19; K1–K5 unique in c2 (K1 0× in c1); forgery anchor 1× |
| 12 | `sha256sum` on both mutant files | 0 | `40645a28…1d49b`, `49373eee…84a85` — both equal the declared pins |
| 13 | `jq`/`json` counts: r87 cases, r88 mutants, K cases | 0 | 22 / 19 / 17 (9 present, 8 none) |
| 14 | candidate on `[urgency=high] width=444` with `--urgency critical` | 0 | `width 300`, refusal `urgency 'high' …`; `[urgency=critical]` control → `width 444` |
| 15 | candidate on `include=~/.ssh/id_test` with `format=LEAKED-FROM-HOME-SSH` | 0 | `applied` contains the include, `format='LEAKED-FROM-HOME-SSH'`, `refusals []` |
| 16 | candidate on symlink escape and `<home>-evil` prefix sibling | 0 / 0 | both `applied []` with the "outside the declared read roots" refusal |

UPSTREAM CROSS-CHECKS (network, read-only): `https://raw.githubusercontent.com/emersion/mako/v1.11.0/types.c` —
`parse_boolean` is `strcasecmp("true") || strcmp("1")` / `strcasecmp("false") || strcmp("0")`, matching
`mado-mako.c2.py:166-173`; `parse_urgency` accepts `high` → `MAKO_NOTIFICATION_URGENCY_CRITICAL`.
`…/criteria.c` — `match_criteria` uses `strcmp` for app-name/app-icon/category/desktop-entry/summary/body, and
`validate_criteria` refuses `summary` + `summary~` (which is what carried case `c22` encodes).

## 6. Blocked / unavailable

**.ufo/waves/round-88/controls/mako-cases-r88.json was still absent** at the end of this seat (three 60 s polls plus
earlier checks; `test -s` → absent). I could therefore not test the C1 case set against (a)/(b) directly — the
`flags-accepted-ignored` argument above is structural (from the case schema and the mutant list), not a run. The C2 case
file appeared during the seat and is covered.

**Not done, deliberately:** no c1-r88/c2-r88 run over either authored case file (freeze rule); no `tools/`, `quality/`,
`corpus/`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` or declaration write; no git/jj mutation; no install.

## 7. Scratch

`/fast/scratch/hyaku/mado-r88/R88MCritic` held only the base-tool extraction and two fixture trees; removed on exit.
