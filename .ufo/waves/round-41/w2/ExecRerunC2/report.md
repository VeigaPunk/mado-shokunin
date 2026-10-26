# ExecRerunC2 — attack on the C2 data-tip claim (PRED-C2-r41-v2, admitted=1/1)

Seat: `ExecRerunC2` (w2, leaf). Target: the C2 data-tip claim — `PRED-C2-r41-v2`
at the DATA commit `07f2641696b5ac73de1404ea737a9f27e9819aa1` reaches
`admitted=1/1 verdict=TARGET_MET` (base `ab2bfaab661c846d1de9d58c01651cd156a13949` = `0/1`).

No tools were installed (none were needed; the generic-rules install directive had nothing
to act on). Nothing was written outside the seat dir and the trailer path; the lane's git
state was read-only (log/show/status/ls-tree only). Scratch was `/tmp` + `mktemp -d`
and is cleaned up.

## 1. Baseline reproduction (committed bytes, lane repo)

Commands (run from the lane root):

```
python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo . --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1
python3 -I quality/counters/c2-r41-focus-entry.py --repo . --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1
```

Output (both, abbreviated to the clause/final lines):

- v2: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1` →
  `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET rev=07f264…` rc 0.
- v1 (superseded): `PRED-C2-r41-v1: admitted=1/1 verdict=TARGET_MET rev=07f264…` rc 0.

The data-tip claim reproduces exactly as registered. The superseded v1 predicate also
admits at the tip (expected: v2 was written after w1 falsified v1 on **forgeries**, not
on this landed data).

## 2. Mutation battery (scratch clone, 30 single-purpose edits)

Harness: `D=$(mktemp -d)`, `git -C "$D" init -q`, fetch `07f2641` by hash from the
lane (`git -C "$D" rev-parse --show-toplevel` == `$D`; base `ab2bfa…` resolves), worktree
at the data commit. Each edit was applied to committed bytes only, committed (`git -C
"$D" … commit` with a scratch identity inside the fixture), scored with the **frozen** v2
counter (`--repo "$D" --rev <mutant rev>`), then `git -C "$D" reset --hard HEAD~1` back to
pristine. Baseline re-run on the pristine mutbase after the battery: still
`admitted=1/1 TARGET_MET` rc 0.

Targets (all committed data): entry `corpus/knowledge/hyprland-focus-grab-r41.md`,
lesson `corpus/lessons/round-41.md` (`## Gate`, lines 25-36), registry
`corpus/SOURCES.md` rows S037/S283-S289 (lines 49, 232-239), `corpus/README.md` line 70,
receipt `.ufo/waves/round-41/fetch/xdph-journal.txt`.

| # | mutation | admitted | clauses | rc |
|---|---|---|---|---|
| M1 | S283 quote word-mangled: "whitelist of surfaces" -> "whitelist of surface" (entry line 19 + GATE line 25) | **1/1** | all 1 | 0 |
| M2 | swapped S283/S284 header source captions (entry lines 3-4) | **1/1** | all 1 | 0 |
| M3 | re-pointed GATE S287 quote to "fixed in b09f157" (lesson line 29 only; no entry edit) | **1/1** | all 1 | 0 |
| M4 | entry recheck `90d` -> `1999-01-01` (entry line 12) | **1/1** | all 1 | 0 |
| M5 | dropped GATE S288 line | 0/1 | d:0 e:0 g:0 | 1 |
| M6 | indented GATE S283 line | 0/1 | d:0 e:0 g:0 | 1 |
| M7 | ghost GATE S999 outside the `## Gate` section | 0/1 | d:0 | 1 |
| M8 | journal census `adverts=78` -> 79 (entry line 63) | 0/1 | h:0 | 1 |
| M9 | journal census line wrapped in a fence | 0/1 | h:0 | 1 |
| M10 | journal census line duplicated | 0/1 | h:0 | 1 |
| M11 | S283 row recheck -> invalid date `2026-02-30` | 0/1 | c:0 | 1 |
| M12 | S284 used-by drops the entry | 0/1 | c:0 | 1 |
| M13 | README index row deleted (line 70) | 0/1 | f:0 | 1 |
| M14 | ghost id S291 appended in entry body | 0/1 | b:0 | 1 |
| M15 | `verified-at:` moved below line 20 | 0/1 | b:0 | 1 |
| M16 | one byte flipped in `xdph-journal.txt` | 0/1 | d:0 g:0 h:0 | 1 |
| M17 | S283 location loses its `.` | 0/1 | e:0 | 1 |
| M18 | S285 opened -> `2026-10-24` | 0/1 | c:0 | 1 |
| M19 | S286 registry row duplicated | 0/1 | c:0 | 1 |
| M20 | S289 kind `own-work` -> docs | 0/1 | h:0 | 1 |
| M21 | both REFUSE reasons < 20 chars | 0/1 | i:0 | 1 |
| M22 | ADMIT staged path outside STAGED allowlist | 0/1 | i:0 | 1 |
| M23 | S037 (held) evidence cell mutated | 0/1 | c:0 | 1 |
| M24 | S283/S284 registry row bodies swapped | 0/1 | e:0 | 1 |
| M25 | ghost GATE inside a fenced block in the `## Gate` section | **1/1** | all 1 | 0 |
| M26 | S284 gate quote mangled (not in receipt) | 0/1 | d:0 g:0 | 1 |
| M29 | BOOT line removed from journal receipt | 0/1 | d:0 g:0 h:0 | 1 |
| M34 | ADMIT `as` target renamed to a different entry | 0/1 | i:0 | 1 |
| M37 | duplicate `source: S283` line below line 20 | 0/1 | b:0 | 1 |

24 of 30 edits are rejected by the v2 predicate (each by the clause that names the edited
property). Six edits are admitted; five are findings/observations below, one (M25) is a
by-design fence behavior.

## 3. Findings — admitted defective edits (against the predicate)

**F1 (M1) — clause d quote containment is substring-based, so a quote can end inside a
word and still pass.** Attacked: `quality/counters/c2-r41-focus-entry-v2.py:378`
(`nq in norm_receipt(blob)` — a plain substring test on the whitespace-collapsed quote).
Edit: "This interface restricts input focus to a specified whitelist of **surfaces**" ->
"…whitelist of **surface**" in both the GATE line (`corpus/lessons/round-41.md:25`) and
the entry line (`corpus/knowledge/hyprland-focus-grab-r41.md:19`). Still admitted 1/1.
Verified by script (git show at 07f2641): `norm_receipt(focus-grab-v1.xml)` contains the
mangled q ("whitelist of surface" is a prefix-subtoken of "whitelist of surfaces") while
the mangled q != original q. Consequence: the data can carry a quote the receipt does not
literally contain (truncated mid-word), and the counter cannot tell. Open predicate defect.

**F2 (M2) — header `source:` captions are not bound to their ids.** Attacked: entry lines
3-4 (S283's caption swaps with S284's caption, ids kept). Still admitted 1/1: clause b
counts only the id tokens, clauses c-g bind via rows/gates, and no clause reads the caption
prose against the id or its receipt. Consequence: two ids can silently trade their source
descriptions without any clause noticing. Open predicate defect (misattribution class).

**F3 (M3) — a GATE quote can be re-pointed to any other substring of the same receipt
that already sits on an id-only entry line.** Attacked: lesson line 29 only — GATE S287
quote "Tried to set workspace silent rule to a nofocus window!" -> "fixed in b09f157"
(verified present in `issue-565.html`; entry line 101 already carries it). Still admitted
1/1 with zero entry edits. The predicate binds quote<->receipt, not quote<->the claim it
supports; this is the declared residual "a real receipt can be cited for a claim it does
not support" — confirmed reachable by a one-line edit inside an otherwise fully consistent
set. Open (declared residual, now demonstrated).

**F4 (M4) — `recheck:` has no sanity bound beyond calendar validity.** Attacked: entry
line 12 `90d` -> `1999-01-01` (valid ISO date). Still admitted 1/1. Any calendar-valid
date passes `recheck_ok`; a recheck dated before the measurement is accepted. Minor, open.

**O1 (M25) — fenced content is invisible to every clause, and extra column-zero GATE
lines for non-cited ids inside the `## Gate` section are unchecked.** A ghost GATE S999
inside fences is admitted (by design: `unfenced` strips fences). Note also: a col-0 GATE
for a non-cited id inside the section (first M7 variant) is admitted — clause d constrains
only cited ids. By-design observations, not defects.

## 4. Verdict

- The data-tip claim as stated is confirmed: `PRED-C2-r41-v2` scores `admitted=1/1
  verdict=TARGET_MET` (rc 0) at `07f2641…`; base `0/1`; the superseded v1 counter also
  scores `1/1` at the tip.
- The committed data (entry, lesson, registry rows S283-S289 + S037, README row, receipts)
  is internally consistent and passes every clause; none of the findings above corresponds
  to a defect in the landed data.
- Findings F1-F4 are predicate-level open defects (no third registration per round rules).
  F1 (mid-word quote truncation) is the strongest: it defeats the quote-verification
  intent of clause d with a two-byte edit.

Evidence anchors: all quoted strings verified against `git -C <lane> show
07f2641:<path>`; the battery was run with the frozen counter binary
`quality/counters/c2-r41-focus-entry-v2.py` (506 lines) against scratch commits; no lane
file was modified.
