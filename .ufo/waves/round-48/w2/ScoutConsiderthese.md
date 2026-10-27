# ScoutConsiderthese — round 48 w2: falsify the consideration and assimilation dispositions

Seat: `ScoutConsiderthese` (leaf, no dispatch). Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; lane re-read at
HEAD `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d` (freeze v1) with the uncommitted l1-draft integration bytes in the
working tree. Reads only; every recompute ran in `/fast/scratch/hyaku/mado-r48/ScoutConsiderthese` (removed before
yield, 294 MB peak from one aborted full clone, all working outputs ≤ 300 KB; `ulimit -f 2048` on every writer shell).
No pacman, no install, no lane/fleet tracked write, no git/jj mutation in the lane (fixture commits only inside
scratch, toplevel asserted). Full command outputs: `.ufo/waves/round-48/w2/ScoutConsiderthese/`.

## Verdict

**Both dispositions survive independent falsification.** §10 counts recompute byte-identical to the w1 artifacts
(reg 276 / staged 147 / collisions 84 / quarantine 13; all four sha256 equal); the guard's indented-row proof
replicates; the staged `merge/mado` package holds no XKB/keymap/xkbcommon and no xdg-terminal-exec/terminal-cache
theme and is byte-unchanged since round 40; `considerthese/2026-10-26.md` proposal 6 is verified present, still
unimplemented at base, and the w1 `ScrConsider` evidence (selftest, red-at-base, green control, quote locators)
reproduces exactly. Assimilation: none is the only defensible posture. The proposed QUALITY criterion disposition
is sound; the L1 still owes the freeze decisions ScrConsider lists (number, token list, SKIP policy).

## 1. §10 id/collision/quarantine — independent recompute

Re-ran the §10 blocks verbatim (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` on `corpus/SOURCES.md` and
`$SK/merge/mado/SOURCES.append.md`, `comm -12`; and the quarantine awk on the absent-defect register).
Evidence: `id-collision-recompute.txt`, `quarantine-slice.txt`.

| quantity | my recompute | w1 artifact (`.ufo/waves/round-48/assimilation/`) | match |
|---|---|---|---|
| `reg-ids` (freeze commit HEAD) | 276 lines, S001–S339 | 276 | sha256 equal (`aa4c1956…`) |
| `staged-ids` | 147 lines, S203–S349, contiguous | 147 | sha256 equal (`079d7538…`) |
| `collisions` (HEAD) | 84 lines, S203–S221 + S253, S258, S277–S339 | 84 | sha256 equal (`8d3561a1…`) |
| `quarantine-slice` | 13 rows (6 payload-absent S189/S195/S201/S205/S224/S228 + 7 never-checked S199/S200/S209/S222/S223/S225/S235), every line carries an S-id | 13 | sha256 equal (`d9ea803d…`) |

Additional measurements the w1 report did not fix:
- Registry at base `579f694b` is already 276 rows (the 262 → 276 +14 drift is round-47 growth; ExecIdGuard compared
  against round-47's prompt-time base — consistent, not an error).
- **Working tree (l1-draft bytes staged, not yet committed): registry 287 rows (+S340–S350, the C2 rows), collisions
  vs staged 94** (+10 = S340–S349 now collide with the package's fixed S203–S349 range). Once data lands, the lane's
  own rows occupy S340–S350 — a later package merge would need renumbering by document. This is a forward hazard for
  the lesson's Gate block, not a defect in this round's posture.
- Staged append sha256 `684efe8c…7a27c0`, package mtime 2026-10-24 23:33 — byte-unchanged since round 40, as w1 claimed.

**Guard replication** (`guard-proof.txt`): scratch registry with S001, S100 (column-zero) and one indented
`  | S203 |` row against a scratch staged set holding S203 → 0–3-space extractor collisions = `S203` (nonempty,
indented collision caught); column-zero-only extractor collisions = 0 (false green). Matches ExecIdGuard's §10 proof
and the `CORPUS.md:152-153` census clause (0–3 leading ASCII spaces accepted; 4+ is code).

## 2. Staged merge/mado package — XKB / terminal-cache theme scan

Independent `grep -rilE` over the whole package plus `SOURCES.append.md` row inspection
(`package-theme-scan.txt`):

- `xkb|keymap|libxkbcommon|keyboard-layout|compose:caps`: **no hits** anywhere in the package.
- `xdg-terminal-exec|terminal.*cache|warm.?cache|XDG_CACHE_HOME`: **no hits**.
- Only "cache" rows in the staged registry: S240/S241 — the host AI-usage *waybar* cache (`~/.cache/ai-usage/
  status.json`), a bar-producer cache, not the resolver warm cache.
- Nearest keymap-adjacent staged rows remain the refuse-by-scope near-misses w1 `ScoutShokuknow` named: S343
  (fcitx5-wetypex doc — window rules/sizes, fcitx5 as app name only), S344–S349 (JP/CN Hyprland wiki: input
  capture, keybind flags). Nothing to admit for C1 or C2; C2's ground is primary fetches + the live xkbcli receipt,
  which is what the l1-draft rows S340–S350 actually cite (libxkbcommon ×9, xkeyboard-config ×2, mado host receipt ×1 —
  verified against the working-tree `corpus/SOURCES.md`; they are lane-authored, not staged bytes).

## 3. considerthese proposal 6 — status against base bytes and ScrConsider evidence

`proposal6-verify.txt`, `check96-verify.txt`, `green-control.txt`.

**Text and currency.** `considerthese/2026-10-26.md` is the latest file (`ls considerthese/`); proposal 6 is at
`:52`: "Lead with round-level outcomes, not counter internals." — verified verbatim, with "the useful signal for
João is what his desktop tooling can now do" on the same line. Six proposals present at `:45–52`.

**Unimplemented at base, independently re-derived** (all greps re-run, not relayed):
- 95 criteria at base; the five `considerthese` citations inside `QUALITY.md` are :367 (criterion 60, 2026-10-24
  proposal 1), :399 (criterion 76), :409 (criterion 81, 2026-10-25 proposal 2), :411 (criterion 82, 2026-10-25
  proposal 5), :459 (criterion 90, 2026-10-26 proposal 3) — none is proposal 6.
- `git grep -niE 'proposal 6|outcome-first|round-level outcome' BASE -- . ':!considerthese/'` → rc=1;
  `QUALITY/SKILL/AGENTS/PROVINCE` → 0/0/0/0; `quality/` gate named `outcome` → 0; lessons naming proposal 6 → rc=1.
  So it is open (neither implemented nor refused), exactly the state the one-proposal rule requires for mining.

**Sibling dispositions** (ScrConsider's §2 table re-verified): p1 implemented — criterion 85
`check-session-material.py` + this round's `w1/SentPrivacy`; p2 refused round 47 with flip condition
(`corpus/lessons/round-47.md:227` at base, verbatim read); p3 implemented — criterion 90; p4 not landable now —
its lane-side half already in criterion 76 (`QUALITY.md:399`), its other half is operator-owned; p5 implemented —
criterion 82 `ratio-domain-meta.py`. Only p6 remains minable, and `ScrConsider` is the sole seat mining it
(one-proposal rule holds — the other w1 `considerthese` mentions are this same seat, the lesson Gate note, the
Scorecard placeholders, and `ScrMistakes` controls that quote the *round-47* refusal text).

**ScrConsider's evidence re-run** (tool sha256 matches its receipt `21d6be5c…`; stdlib only, subprocess limited to
`git show`/`git cat-file -e`):
- `--selftest` → `SELFTEST: ok cases=5` (all five want/got pairs match).
- Red at base, rounds 44–47 → identical to its receipt: FAIL, lines 2566/2596/2627/2656, process_tokens 9/10/14/11.
- Red at base, rounds 1–47 → `OUTCOME_FIRST_SUMMARY: rounds=47 pass=0 fail=34 skip=13`. Reason distribution:
  23 × `no-surface,process-first`, 11 × `no-surface`, 13 × `no-section`. No FAIL at base names a surface — the
  check never fires on an outcome-shaped sentence in history, so the frozen-token strictness has no observed
  false-positive in the 47-round corpus (it remains a frozen-list tradeoff for the L1, §4 below).
- Green control replicated **on real base bytes**: scratch repo holding the base `SCORECARD.md` + base
  `tools/mado-terminal.py`, only round 47's opening sentence (line 2656) rewritten outcome-first naming
  `tools/mado-terminal.py` (fixture rev `c8be5864…`) → `round=47 verdict=PASS surface=tools/mado-terminal.py
  process_tokens=0`, rounds 44–46 stay FAIL. Satisfiable by editing the lane's own prose; the round-47 opening
  at base is the freeze-hash sentence ScrConsider quotes.

## 4. Disposition findings for the L1

**Assimilation: none — confirmed and now double-sourced.** Three independent legs: (i) §10 counts show the staged
set is unappendable without renumbering (collisions nonempty: 84 at freeze, 94 against the working tree; the
guard catches indented rows the naive pattern misses); (ii) the theme scan finds nothing on this round's two
planes (XKB compile, terminal cache) — nearest staged items are refuse-by-scope near-misses, and the package has
not moved since round 40; (iii) the quarantine register's 13 mado rows stay quarantined (6 payload-absent,
7 never-checked; 4 of the ids already belong to different lane registry rows, so blind adoption would mis-bind
citations). No staged byte appears in the working-tree integration: the +11 registry rows are the lane's own C2
ground, and the only touched knowledge files are the r45/r47 errata targets.

**Proposed criterion disposition — proposal 6 as QUALITY 96 (`check-round-outcome-first.py`) is admissible.**
The proposal is open at base, the check can fail (red 34/34) and can pass (green on real bytes), its rule is frozen
in the tool docstring, and its mechanism is stdlib `git show`/`cat-file` only — no network, no writes on the
scoring path. Conditions the L1 must still satisfy at freeze, all flagged by ScrConsider itself and re-confirmed
here: (a) **number** — criteria 91–95 landed in round 47 so 96 is free at base, but `ScrMistakes` is mining M48
mistakes into 96+ candidates this same round; the number and the `quality/` path must match whatever the freeze
commits (QUALITY 64 guards the path-exists half); (b) **frozen token list** — the draft's list (`registration`,
`frozen`/`freeze`, `Claims declared`, `PRED-`, `TARGET_MET`/`TARGET_MISSED`, `fixtures=`, `seat`/`seats`, `wave`,
`attempt=`, `receipts/`, `counter`) makes the first sentence unable to mention e.g. "wave" at all — no historical
false shape, but the strictness is a real tradeoff once frozen; (c) **SKIP policy** — 13 skip rounds at base
(38, 42 and the never-landed); the criterion must state skip≠fail as drafted, or the skips become violations;
(d) **self-application** — the round that lands the criterion must open its own `SCORECARD.md` section
outcome-first (`fail=0` at the round-48 data commit), which binds this round's closure prose, not just future ones.

No defect found that would break the frozen predicate, counters, fixture set, claims or target; nothing here
requires re-registration.

## Evidence index (seat dir `.ufo/waves/round-48/w2/ScoutConsiderthese/`)

| file | contents |
|---|---|
| `id-collision-recompute.txt` | §10 id block, HEAD vs working-tree vs base counts, sha256 comparisons, staged-append hash/mtime |
| `quarantine-slice.txt` | exact §10 awk, 13 rows, sha256 equality with w1 artifact |
| `guard-proof.txt` | indented-S203 scratch guard replication (0–3-space catches, column-zero false-greens) + CORPUS.md:152-153 clause |
| `package-theme-scan.txt` | theme greps over `merge/mado`, S240/S241 cache rows, near-miss list |
| `proposal6-verify.txt` | proposal 6 line, unimplemented greps at base, proposals 1–5 dispositions |
| `check96-verify.txt` | tool sha256, imports, selftest, red-at-base 44–47 and 1–47, reason distribution, FAIL-with-surface scan |
| `green-control.txt` | green replication on real base bytes (fixture rev, edit, run output) |

Largest output file written: 1,048,576 bytes (ulimit cap hit only by the aborted full-lane clone in scratch,
deleted unused; all cited evidence ≤ 300 KB). Tooling installs/updates: none. Scratch
`/fast/scratch/hyaku/mado-r48/ScoutConsiderthese` removed before yield.
