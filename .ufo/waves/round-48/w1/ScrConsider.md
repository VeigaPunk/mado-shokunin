# ScrConsider — round 48 w1: one unimplemented `considerthese` proposal, drafted through the lane's bar

Seat: `ScrConsider` (leaf, no subagent dispatch). Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Reads only; no tracked
file edited; no compositor, cache, terminal, package or service touched.

## Chosen proposal

`considerthese/2026-10-26.md:52` (2026-10-26) **proposal 6 — "Lead with round-level outcomes, not counter internals"**,
landed as a draft QUALITY criterion (provisional 96). Verified quotes: `words=7` and `words=13` from that line, locators
computed from the base blob (`receipts/quotes.txt`, `QUOTE_SUMMARY: quotes=7 pass=7 fail=0`).

**Draft:** `.ufo/waves/round-48/w1/ScrConsider/draft.md` — proposal, disposition of the other five, unimplemented evidence,
the paste-ready criterion text, the check, freeze decisions for the L1, declared limits, and a lesson-paragraph fallback.

## Why this one (dispositions at base, each by lane bytes)

| Proposal | State | Evidence |
|---|---|---|
| 1 privacy check | implemented | `corpus/lessons/round-45.md:81` → `quality/check-session-material.py`, QUALITY 85 |
| 2 live-state tool ledger | refused round 47 (as assigned) | `corpus/lessons/round-47.md:227` |
| 3 routed-defect ages | implemented | `corpus/QUALITY.md:454-459`, criterion 90 |
| 4 re-run one tool itself | not landable as a check | `considerthese/2026-10-26.md:50` (host+operator gate); lane half already QUALITY 76 |
| 5 domain-meta ratio | implemented | `corpus/lessons/round-44.md:248` → `quality/ratio-domain-meta.py`, criterion 82 |
| 6 lead with outcomes | **unimplemented** | below |

## Evidence it is unimplemented at base (`receipts/unimplemented-base.txt`)

- `git show BASE:corpus/QUALITY.md | grep -cE '^[0-9]+\. '` → **95** criteria; `considerthese/` citations sit at `:367`
  (60), `:399` (76), `:409` (81), `:411` (82), `:459` (inside 90) — none proposal 6.
- `git grep -niE "proposal 6|outcome-first|round-level outcome" BASE -- . ':!considerthese/'` → **rc=1** (no lane bytes).
- The same sweep inside `corpus/QUALITY.md`, `SKILL.md`, `AGENTS.md`, `PROVINCE.md` → **0, 0, 0, 0**.
- `git ls-tree -r --name-only BASE quality/ | grep -ciE 'outcome'` → **0**.
- `git grep -n 'proposal 6' BASE -- corpus/` → **rc=1**: open, not previously refused.

## What it points at, measured

Every `SCORECARD.md` round section at base opens with its own bookkeeping, not the capability. Round 47 (`SCORECARD.md:2656`
at base) begins "Claims declared at `c24adef2` … before wave `w1` (41 build seats)"; rounds 44-46 open with
"Registration … frozen at" and carry 9, 10 and 14 process tokens in their opening sentence. Census with the draft checker
at base: **`OUTCOME_FIRST_SUMMARY: rounds=47 pass=0 fail=34 skip=13`**.

## The check that can fail (`receipts/check96.txt`, tool sha256 `21d6be5c7afa…254c488`)

`.ufo/waves/round-48/w1/ScrConsider/check96.py` — stdlib only, `git show`/`git cat-file -e` reads, scoring path writes
nothing, rule frozen in its docstring before the first run.

- `--selftest` → `SELFTEST: ok cases=5` (positive control PASS; process-first, second-sentence-surface, no-prose and
  ghost-path cases FAIL with `process-first`, `no-surface`, `no-paragraph`, `surface-absent`).
- Red at base: rounds 44-47 → `fail=4 rc=1`; rounds 1-47 → `pass=0 fail=34 skip=13 rc=1`.
- Green control on real bytes: `--shared` scratch clone at base + one rewrite of round 47's opening paragraph
  (clone rev `f73436ed5408f3745d86cecc29d989fbb6f50afc`) → `round=47 verdict=PASS surface=tools/mado-terminal.py
  process_tokens=0`, rounds 44-46 still FAIL. Lane repo untouched.
- Name-independence for the landed path: a byte-identical copy named `check-round-outcome-first.py` gives the same
  verdicts (§9 of the receipt).

## Gates and safety

- Lane `git status --porcelain`: my only writes are under `.ufo/waves/round-48/w1/ScrConsider/` and this report. No tracked
  file, index, `.ufo/state/`, `templates/`, `scripts/` or fleet-root file touched. No mutating git/jj in the lane; the
  single commit made anywhere is inside the scratch clone, after `rev-parse --show-toplevel` asserted the fixture dir.
- Host: no pacman, no install/upgrade (nothing installed — tool record: none), no `xdg-terminal-exec`, no `xkbcli`, no
  `hyprctl`, no terminal/GUI launch, no service or compositor mutation, real `~/.cache/xdg-terminal-exec` untouched.
- Scratch `/fast/scratch/hyaku/mado-r48/ScrConsider` (fixture repo + clone, both < 1 MB) deleted before close; no `/tmp`
  path cited as evidence.
- Two early receipts (`check96-base.txt`, `check96-green.txt`) were superseded by the consolidated `check96.txt` before the
  SKIP rule landed in the tool, and removed rather than left to contradict its criterion text.

## Findings the L1 should carry into the freeze

1. Proposal 6 is genuinely open: no criterion, no gate, no refusal anywhere in the lane's bytes at base.
2. The defect is lane-wide, not recent: 34/34 landed round sections fail the ordering test; the earliest landed section
   (round 12) fails too.
3. The criterion binds the lane's own `SCORECARD.md` section, not the reflection file — the reflection is
   operator-authored and not the lane's to edit (`corpus/lessons/round-32.md:120`). The transposition is labelled
   [INFERENCE] in the draft.
4. The proposal's "one paragraph of counter mechanics" half is deliberately **not** scored (fragile, and the closure
   sections legitimately carry several process paragraphs); only leading order is bound, and the limit is declared.
5. If landed, criterion 96 scores round 48's own closure at the data commit — the landing round must satisfy it.
6. Open decision for the L1: number (96 may be taken by another w1 seat), landed file name, frozen token list, and
   whether a round with no `SCORECARD.md` section stays `SKIP` (rounds 38, 42 at base) or becomes a violation.

## Artifacts

- `.ufo/waves/round-48/w1/ScrConsider/draft.md` — the landing draft (criterion text in §5, check in §6, limits in §8).
- `.ufo/waves/round-48/w1/ScrConsider/check96.py` — proposed check (5-case selftest).
- `.ufo/waves/round-48/w1/ScrConsider/verify-quotes.py` — quote verifier (locators computed, 25-word limit).
- `.ufo/waves/round-48/w1/ScrConsider/receipts/{check96.txt,unimplemented-base.txt,quotes.txt}`.
- This report: `.ufo/waves/round-48/w1/ScrConsider.md`.
