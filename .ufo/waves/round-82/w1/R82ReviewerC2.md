# R82ReviewerC2 — C2 (operability: the tray plane in the runbook), read-only attack

Seat: `R82ReviewerC2`. Scope: the C2 claim only (`busctl --user set` law row class: tray-owner,
tray-interface, tray-methods), its 29-case control set, its counter, and the runbook section it
binds. Read-only: no file in the lane was written except this report; no commit, no mutating git/jj
verb, no subagent. No tool was installed or upgraded (nothing was needed).

## 0. Baselines — the tree moved twice under this review

Two byte sets matter; every finding below was re-checked on both. `SKILL.md` and
`tools/mado-barfoot.py` — the two files the counter binds by sha256 — are **byte-identical** at
all three revisions named (`56f9d09b…` / `93cd54a8…`), so the measurement is byte-equivalent
across the rev-label change.

| set | counter sha256 | controls sha256 | bound bytes |
|---|---|---|---|
| **A** — claim-pinned / seat-spec frozen list (at `b6146ee6`) | `1e8eb49928bf…` | `f64d7d5db40f…` | SKILL `56f9d09b…`, tool `93cd54a8…` |
| **B** — current `HEAD` `57789ab6` (erratum E1 at `89acb06c6…`) | `a87bceabd185…` | `07599b24dadd…` | same two blobs |

Reproduction (run from the lane root, scratch root under `/fast/scratch/hyaku/mado-r82/R82ReviewerC2`):

```sh
python3 -I quality/counters/c2-r82-runbook.py --repo . \
  --rev <REV> --controls .ufo/waves/round-82/controls/c2-runbook-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c2-runbook-cases-r81.json --scratch-root DIR
```

* Set A at `--rev 780c30fc…`: `cases=29 executed=29 matched=29 shapes=24/24 anchors=29/29
  rows=29/29 control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET tree=bound`, rc 0, 11.66 s.
* Set B at `--rev 89acb06c…`: the same line with `rev=89acb06c…`; **all 56 verdict entries
  (29 probes + 25 mutants + control + runbook) are identical to the committed receipt** — the only
  diff is the rev field.
* Counter selftest: `MADO_R82_RUNBOOK_SELFTEST: 90/90` under both byte sets (matches the
  declaration's stated `selftest 90/90`).

E1 changed only: counter `+8/−1` (`SCRATCH_ROOT` + `TMPDIR = SCRATCH_ROOT or cwd`), controls 12
lines (tray-owner fixture **strings** only), generator 16 lines. Constants, expectation kinds,
`value`s, argv, anchors, sample/negative counts are unchanged (verified case-by-case).

---

## 1. Constructed outputs: two that SHOULD NOT match, one that SHOULD, per new row

`shipped` = `special_matches()` of the current counter (identical under A and B). "wrong matcher
survives" = a plausible weakened matcher that passes **all** frozen samples and is accepted by
**none** of that row's frozen negatives, i.e. the fixture set cannot falsify it.

### 1.1 `tray-owner` — `busctl --user list`, `kind=regex`, value `(?m)^org\.kde\.StatusNotifierWatcher\s+[1-9][0-9]*\s`

| probe | output | should | shipped | note |
|---|---|---|---|---|
| P | `org.kde.StatusNotifierWatcher 4242 waybar user :1.99 user@UID.service - -` (rc 0) | match | **True** | plus both frozen samples pass |
| F1 | `org.kde.StatusNotifierWatcher 4194305 waybar …` (rc 0) | reject | **True** | **false green** — see D1 |
| F1b | `org.kde.StatusNotifierWatcher 999999999 …` (rc 0) | reject | **True** | same; no negative pins a ceiling |
| F2 | `org.kde.StatusNotifierWatcher2 4242 …` (name prefix collision) | reject | False | `\s` after the name is load-bearing |
| F3 | header-only listing (watcher absent) | reject | False | killed for any wrong matcher that requires content |
| F4 | `:1.99 4242 org.kde.StatusNotifierWatcher 4242 …` (name in a non-NAME column) | reject | False | anchored `^` is load-bearing |

Negative coverage (4): PID `0`, foreign bus name, `-` in the PID column, correct line at rc 1.
They kill name-only, PID-0-blind, any-numeric-column and rc-blind weakenings. They do **not**
cover the out-of-range PID (F1) or the non-first-column name (F4). The plausible `re.search`
without `^` survives 0/4 negatives and accepts F4 — not producible by the real command (the NAME
column is first), so no live exposure; it is a mutation-coverage hole (G2), not a live false green.

### 1.2 `tray-interface` — `busctl --user introspect … /StatusNotifierWatcher --no-pager`, `kind=regex`, value `(?m)^org\.kde\.StatusNotifierWatcher\s+interface\s`

| probe | output | should | shipped |
|---|---|---|---|
| P | `…\norg.kde.StatusNotifierWatcher interface - - -` (rc 0) | match | **True** |
| F1 | `org.freedesktop.DBus.Properties interface - - -\norg.freedesktop.DBus.Peer interface - - -` (only foreign interfaces; watcher interface absent) | reject | False |
| F2 | `.org.kde.StatusNotifierWatcher interface - - -` (member line, not an interface row) | reject | False |
| F3 | `org.kde.StatusNotifierWatcher property - - -` (right name, wrong type) | reject | False (frozen negative 1) |

Negative coverage (3): wrong type with the right name; a method row only; the right line at rc 2.
**Gap (G1):** the complementary pair is missing — *right type, wrong name*. The plausible
"type-only" matcher `^\S+\s+interface\s` passes 2/2 samples, is accepted by **0/3 negatives**, and
accepts F1. So the fixture set cannot demonstrate the rule's failure on the exact census the row
exists to reject (a census without the watcher interface). The shipped matcher is correct.

### 1.3 `tray-methods` — `… | awk '$2=="method"'`, `kind=lines_shape`, `^\.[A-Za-z]+\s+method\s+`, `min_lines=2`

| probe | output | should | shipped |
|---|---|---|---|
| P | `.RegisterStatusNotifierHost method s - -\n.RegisterStatusNotifierItem method s - -` | match | **True** |
| F1 | one method line (census of one) | reject | False (negative 2) |
| F2 | method line + interface line (mixed census) | reject | False (negative 1) |
| F3 | two method lines separated by a blank line | reject | False (empty line fails the grammar) |
| F4 | non-dotted member names `org.freedesktop…Get method …` | reject | False |
| F5 | two method lines at rc 1 | reject | False (negative 3) |
| **F6** | **the six standard-interface methods only**: `.Introspect`, `.GetMachineId`, `.Ping`, `.Get`, `.GetAll`, `.Set` (rc 0) | reject (it is not the tray's table) | **True** |

**Live census (read-only, shape-only):** 8 method rows = 6 standard (`org.freedesktop.DBus.*`)
+ 2 watcher register methods; the interface census has 4 interface rows including the watcher
interface; the bus-name owner row exists with a numeric PID. So F6 is producible: the census can
lose both watcher methods and the row still passes. This is **consistent with the claim's own
text** ("every line `.Name method`, at least two lines"), so it is a named limit (O1), not a
divergence — but the row proves the census's grammar, not the tray's method surface.

Grammar narrowing, false-red only: `.Get2` and `.Get_All` are rejected by `[A-Za-z]+` although the
claim's `.Name` admits them. Wrong matchers surviving the negatives: "all lines contain
` method `" and `words[1]=="method"` (the latter accepts F4); both are unexposed by live output
(members are dotted) but untested by mutation. The row's `rc 0` clause is vacuous: the pipe
returns awk's status, so the rc is 0 even when `busctl` fails — the `min_lines=2` + all-lines rule
carries the failure (empty input cannot produce two method lines). That is fail-closed, and the
floor-dropping mutants are killed; but the rc clause should not be read as evidence that the
introspect succeeded.

---

## 2. Row-binding rule

**Extraction.** `command_rows()` (`quality/counters/c2-r82-runbook.py:248`) scans only the
`### Executable runbook rows (round 82)` section up to the next `### `, splits on unescaped
pipes (`\|` → literal `|`), takes cell 2, strips backticks. On the current SKILL.md it returns
exactly 29 rows; indices 26/27/28 are the three new rows and are **identical** to the
`documented` rendering of each case's argv:

```
26  busctl --user list
27  busctl --user introspect org.kde.StatusNotifierWatcher /StatusNotifierWatcher --no-pager
28  busctl --user introspect org.kde.StatusNotifierWatcher /StatusNotifierWatcher --no-pager | awk '$2=="method"'
```

The third command's row cell escapes the pipe as `\|`; the extracted cell is the plain `|` string
and equals `argv[2]`. The two non-shell rows are compared by `" ".join(argv)`; no argv element in
any case contains a space outside the shell branch, so that rendering is faithful here.

**Bijection.** The counter enforces `len(rows)==29`, each case's anchor hits exactly one row, no
row is double-bound, and `len(bindings)==29` (`:681–690`), and then re-checks each case's argv
against its anchor (`:692–696`), which is what prevents a permutation of bindings. I exercised
the four failure modes on the real section text:

| mutation | result |
|---|---|
| an old row's command cell replaced by a new command (orphan + duplicate) | `ERROR anchor 'makoctl mode' for mako-mode binds 0 rows` → rc 2 |
| one row duplicated | `ERROR the runbook section carries 30 command rows` → rc 2 |
| one row dropped | `ERROR the runbook section carries 28 command rows` → rc 2 |
| section header renamed, rows untouched | `ERROR carries 0 command rows` → rc 2 |

**Rename did not orphan an old row.** r81's section (`(round 81)`) carried 26 rows; r82's
(`(round 82)`) carries those same 26, in the same order, plus the 3 new ones — verified by
parsing both revs: `prefix_identical=True`. SKILL.md contains exactly one
`### Executable runbook rows` section, so nothing is silently stranded in an ignored section.

**Two limits of the binding:**
1. Only the **command** cell is bound. The outcome cell and the count cell are prose, never read
   by the counter — which is how D1 and D2 below survive a green run.
2. For non-shell argv the check is string identity (`" ".join(argv)`), not argv identity. Not
   exploitable in this set (no space-bearing element), and any exec-shape change would fail at
   exec (Setup), but the guarantee is "the row's text equals the documented rendering", not "the
   executed argv equals the row".

---

## 3. Constants and `control_new=0/3`

| constant | frozen | measured | verdict |
|---|---|---|---|
| `CASES` | 29 | 29 cases in the control set | ✔ enforced (`:621`) |
| `CARRIED` | 26 | 26 in r81 set; the first 26 new cases are field-identical to r81 except `skill_anchor` (`:632–641`) | ✔ |
| `SHAPES` | 24 | 24 cases whose `kind ∈ SHAPE_KINDS`; all 24 matched | ✔ (guards the kind census; given `matched=29` it cannot fail independently) |
| `MUTANTS` | 25 | `len(MUTATIONS)==25`; 25/25 killed, per-mutant `matched` counts identical to the receipt | ✔ |

`control_new=0/3` is **construction, not accident**: `held_rule()` returns `False` immediately
when `"frozen" not in case` (`:438–443`), and none of the three new cases carries `frozen`
(only 15 of the 29 do, all carried). The printed clause says so
(`held=fixed-value(no-frozen-value-for-the-new-rows)`), and `control_new == 0` is in the target,
so a new row that carried a matching frozen value would fail the run.

Corroboration that the clause is not vacuous: I added `frozen` = the exact live bytes to the three
new cases in a scratch copy of the controls and re-ran. `control_new` moved to **2/3** (the
`busctl --user list` output is volatile across runs: 1 of 119 lines changed between consecutive
runs, so its captured bytes did not reproduce; the other two are byte-stable) and the verdict
became `TARGET_MISSED`, rc 1. So the 0 is structural and the predicate would catch an overfit new
row.

Redundancy, for the record: `shapes=24/24` and `anchors=29/29`/`rows=29/29` are derived from
`matched=29` and the same `len(bindings)`. They are honest but add no independent evidence.

---

## 4. Mutation map (computed, all 25)

Every one of the 29 cases kills at least one mutant — no dead case. Which cases kill what:

* `tray-methods` kills **5**: `rc-blind`, `lines-any-line`, `lines-min-lines-dropped`,
  `lines-shape-floor-dropped`, `lines-shape-any-line` (the most load-bearing new row).
* `tray-owner` and `tray-interface` kill **1 each: `rc-blind` only** — the global exit-status
  gate, not any part of their own regex.
* `rc-blind` alone kills 10 cases; the two new regex rows have **no dedicated mutant**. There is
  no mutant on the `regex` branch at all (`:315`), so `re.search` vs `re.match`, the `^` anchor,
  and `(?m)` are untested by mutation: the two name/type rows are validated only by their
  negative fixtures, and one of those directions is missing (§1.2, G1).

---

## 5. Findings

### F0 — frozen control set superseded without amending the declaration (provenance; needs an L1 decision)
`.ufo/waves/round-82/claims-declaration-r82.md:96` pins the C2 controls at sha256 `f64d7d5d…`.
Erratum E1 (`89acb06c6…`) rewrote that file to `07599b24…` (tray-owner fixture token redaction)
and the counter to `a87bceab…`, and **the declaration was not amended**: `git diff
b6146ee6..HEAD -- …/claims-declaration-r82.md` is empty; the only "erratum" text in it is a
round-80 clause (`:132`). The declaration is the frozen contract seats may not edit, so its
hash clause now points at bytes that no longer exist in the tree. The receipt is coherent with
the instruments again as of `57789ab6` (`sha256=07599b24… rev=89acb06c…`, committed), so the
evidence chain is repaired; what remains open is the contract's hash pin and the supersession
record. The erratum itself is benign for C2 semantics — constants, matchers and all verdicts
reproduce identically — and it removed a redaction breach in the superseded bytes (an account
name and a UID-derived systemd unit token appeared in the tray-owner fixtures; current controls
and receipt contain 0 occurrences of the account name, the home path or the unit token). **Not
fatal to the claim's numbers; fatal to the contract as written until the L1 appends an erratum
note/supersession with the new hashes.** A seat must not repair this.

### D1 — `tray-owner`: the documented PID ceiling is not enforced (defect, low)
The claim (declaration `:83`) and the runbook cell (`SKILL.md:274`) both say the owner line's PID
column is "a decimal in **1..4194304**". The frozen `value` is
`(?m)^org\.kde\.StatusNotifierWatcher\s+[1-9][0-9]*\s` — lower bound enforced (no zero, no dash, no
leading zero), **no upper bound**. Evidence: the shipped matcher returns `True` for
`… 4194305 …` and for `… 999999999 …`, and no frozen negative contains an out-of-range PID. Live
exposure is nil (the PID column is the name owner's kernel PID, bounded by
`/proc/sys/kernel/pid_max` = 4194304), so this is a rule/documentation divergence rather than an
observable live false green — but it is exactly the class the wave's own convention forbids
(`waybar-process`/`pid_state` rows enforce the same 4194304 ceiling; the sibling cells mirror
their `value`s exactly). Fix (L1's call, instrument frozen): add the ceiling to the regex/int
check and a negative with an out-of-range PID, or strike "1..4194304" from the claim and the cell.

### D2 — runbook count cells are wrong and nothing checks them (defect, low)
The third column is "Churn / negative samples". Two cells do not match the frozen cases:
* `SKILL.md:276` (`tray-methods`) says **`1 / 3`**; the case has **2** samples and 3 negatives.
  New this round.
* `SKILL.md:270` (`keybindings-chords`, carried) says **`2 / 7`**; the case has 2 samples and
  **8** distinct negatives. Pre-existing in r81 (same cell there) and carried unchanged.

The other 27 cells match. Because the counter never reads that cell (§2), the wave cannot catch
this class. Low severity, but it is a false statement in the artifact a human re-runs.

### G1 — `tray-interface` negatives do not falsify a type-only census (coverage gap, named limit)
Right-type/wrong-name is absent from the fixture set; a matcher that only requires *some*
`… interface` line passes all samples, blocks none of the negatives, and accepts
`org.freedesktop.DBus.{Properties,Peer} interface - - -`. The shipped matcher rejects that
census, so the rule is right; the *control* cannot demonstrate its failure. Candidate negative
for the L1: `org.freedesktop.DBus.Properties interface - - -\norg.freedesktop.DBus.Peer interface - - -`
at rc 0 (would kill the type-only matcher).

### G2 — no mutant on the `regex` branch (coverage gap, named limit)
The 25 mutants cover refusal, `lines_shape`, `chord_shape`, `is_active`, `action_column`,
`pid_state`, `int_range`, `json_object_fields`, `sorted_unique` and `empty`; the two new rows are
`regex`, which has none. Their only kill is `rc-blind`, shared by 10 cases. Anchoring/MULTILINE
weakening therefore rests entirely on the negatives — and G1 shows one direction missing.

### O1 — `tray-methods` cannot fail for the loss of the tray's methods (named limit, see §6)
The ≥2 floor is below the six standard-interface methods the census always carries (live: 6
standard + 2 watcher). A watcher that lost `RegisterStatusNotifierHost`/`RegisterStatusNotifierItem`
still yields 6 method lines and the row passes. Consistent with the claim's text; it bounds what
the row proves.

Minor, non-blocking: `EXACT_KINDS` (`:146`) is defined and never used (dead code);
`observed()` prints only the first 100 chars, so the receipt's evidence for the two regex rows is
the table header, not the matched line (a reader must re-run to see the match); the counter does
not verify its own bytes against `--rev`, and *prints* the controls sha256 rather than asserting
it — the chain relies on the declaration's pin (currently F0).

---

## 6. Strongest single objection

**The strongest objection is F0**: the wave's frozen control set and counter were rewritten by
erratum E1 while the declaration still pins the superseded control hash, so the frozen contract no
longer identifies the instrument that produced the green. **Verdict: fatal to provenance as
written, not fatal to the claim's numbers** — the numbers reproduce byte-for-byte on the new bytes,
and the erratum is a net improvement (a redaction breach removed, `TMPDIR` kept out of the
measured tree). It needs an L1 erratum note/supersession; a seat cannot fix it.

If F0 is set aside as an L1 matter, the strongest C2-rule objection is **O1 + G2**: the third tray
row's ≥2-line floor is satisfied by the six standard-interface methods alone, and the two `regex`
rows have no mutant, so the tray-plane rules are validated only in the directions their negatives
chose. That is a **named limit, not fatal**: the shipped matchers are correct for every direction
tested, the live surface was measured (4 interface rows incl. the watcher interface; 8 method rows;
numeric owner PID), and the record states the shapes honestly. D1/D2 are low-severity defects that
should be corrected with the next instrument revision.

---

## 7. Verification gaps / residual risk

* Receipt evidence for the two `regex` rows is truncated to 100 chars (the header), so the
  receipt alone does not show the matched line; re-running is required.
* The counter's controls-hash is printed, not asserted, and it does not hash itself; the
  provenance rests on the declaration's pin — which F0 shows can go stale.
* `tray-methods`'s `rc 0` is vacuous (pipeline returns awk's status); the length/all-lines rule
  is the load-bearing clause, and it is fail-closed on empty input.
* My wrong-matcher battery is a set of plausible weakenings, not an exhaustive mutant space; the
  two that survive (unanchored owner, type-only interface) are both rejected by the shipped
  matcher and were checked against all frozen samples and negatives.
* Live outputs were captured shape-only; no account name, home path, unit token, monitor identity
  or serial appears in this report or in anything saved under my seat directory.

Defects named: D1 — `tray-owner` documents a 1..4194304 PID ceiling its frozen `value` does not
enforce (controls `c2-runbook-cases-r82.json` tray-owner `value`; `SKILL.md:274`;
`claims-declaration-r82.md:83`). D2 — two runbook count cells are false (`SKILL.md:276`
tray-methods `1 / 3` vs 2/3; `SKILL.md:270` keybindings-chords `2 / 7` vs 2/8). F0 —
`claims-declaration-r82.md:96` still pins the superseded controls hash `f64d7d5d…` after erratum
E1 (`89acb06c`) and needs an L1 decision.

STATUS: defect
