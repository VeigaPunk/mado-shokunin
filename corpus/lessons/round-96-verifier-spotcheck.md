# round-96 verifier spot-check — mado

author: hyaku closure (non-author integrator, @m_zfl)

- Date: 2026-11-07. Lane repo `mado-shokunin`, branch `master`; round base
  `9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d` → round tip `0caf246510fb7b849edd5217aef0eb6087592e4b`
  (the report cites `c20f060d83f7dc595be58f15c5144dc805f1cd70` as the tip when it was written; the erratum
  `0caf2465` landed 51 s after the report commit).
- Report: `.ufo/reports/round-96/mado.md` (fleet repo, commit `e26f8a5ff10d2bb48717784ed825a00b409774ea`).
- This file is my only lane write; I did not author, improve or edit any lane artifact, and I did not write
  `[x]` into `SHONEN.md`. The lane's gates were not executed as closure evidence (§Gate standard: the
  integrator verifies committed evidence). A read-only replay in scratch of both round counters at the tip
  is recorded below as corroboration; every verdict rests on the committed receipts and my own plain
  measurements over committed bytes.

## 1. Step-1 conformance

| item | observed | verdict |
|---|---|---|
| report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-96/mado.md` → `mado-shokunin e26f8a5f` (committer 2026-11-07T13:13:32-03:00) | pass |
| report lands last | report committer time 13:13:32-03 is after the cited lane tip `c20f060d` (13:13:14-03); the cited tip is an ancestor of `master` | pass |
| `SHONEN` heading, one line per box | `## SHONEN` present; four `[~]` lines = the four boxes of `SHONEN.md`; no `[x]`; each line carries a pointer | pass |
| cited commits exist and are ancestors of `master` | `09db97c3`, `b056290d`, `5dd921b3`, `f54def27`, `8a0aadb0`, `c20f060d` — `git merge-base --is-ancestor <h> master` rc 0 each; `0caf2465` (erratum, after the report) is the branch tip | pass |
| lane repo clean and pushed | `jj-lane.sh state` → `branch=master local=0caf2465 remote=0caf2465 ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` = `0caf2465` | pass |
| prompt carries the template contract | `.ufo/prompts/mado-round-96.md` §1–§5 diffs against `templates/round-prompt.md` only in the working-dir substitution (`{{LANE}}`=mado, `{{ROUND}}`=96, `{{FLEET_ROOT}}`, axes `coverage + operability (desktop and compositor craft)`); all five child-lane items present (report path, `SHONEN` heading, commit-hash citation, commit-then-report §5, write scope); §6 hyaku addendum present | pass |
| L2 floor and round shape | one v1 wave `w1`, 14 seats in one dispatch record (`.ufo/waves/round-96/w1-dispatch.json` counts `spawn 14`, `w1-spec.json` `maxLanes 16`), 6 executor + 2 mutation-tester + 2 reviewer + 1 critic + 1 scout + 1 connector + 1 scribe; attack 5/14 = 36 % (≥25 %); no residual call; every seat has a report under `.ufo/waves/round-96/w1/` | pass |
| marker vs report | real report: named commits, receipts, every required section, checkable hash citations | report, not a marker |

Dispatch/complete digest carried into the closure notes (`.ufo/watchdog.log`, mutable, copied):

```
2026-11-07T11:15:07-03:00 launch mado round=96 pgid=1870448 driver=hyaku-inline attempt=1
2026-11-07T13:15:13-03:00 complete mado round=96; hyaku-inline attempt=1
```

Conformance defects (status-neutral; routed in §6): the dispatch prompt was committed under the lane
identity `f9e7b713` by the driver (attribution pattern); the prompt's quoted run-15 route map is stale
against the live `task.agentModelOverrides`, while the prompt names the host route table as the authority
(operator-side addendum, not a lane defect); the report's role census says 4 executors where the wave
registry holds 6 (D9); three post-report commits are not in the Landed-changes table (D13).

## 2. Claim re-checks

Legend: **re-measured** = I ran the count myself over committed bytes; **evidence-verified** = I read the
committed receipt/frozen evidence (self-test tally, frozen-run verdict, revision measured); **replayed** =
corroborating re-run of the lane counter in scratch, not closure evidence.

### C1 — coverage, new surface (capability): the TEXT MIME database's magic step

| check (command) | observed | matches report |
|---|---|---|
| `git cat-file -e 9f029f46:tools/mado-mimetext.py` | absent at base (rc 128: "exists on disk, but not in '9f029f46'") — the declared 0/0 | yes |
| `sha256sum tools/mado-mimetext.py` at the tip | `d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd` = the freeze pin | yes (re-measured) |
| `sha256sum` of cases / mutants / oracle / fresh gen / host list / host DB / forgery | `4b3645ae…f1d565` / `448150e2…bc440` / `99df35f8…d124a` / `32d38edf…815da` / `9d5947a7…ba87` / `9c411d2a…ddd7` / `06800cd1…fd97` — all equal the freeze block | yes (re-measured) |
| host text-DB manifest vs the live host | all 8 `/usr/share/mime/{magic,globs,globs2,aliases,subclasses,icons,generic-icons,XMLnamespaces}` match the manifest's bytes and sha256; `/usr/share/mime/mime.cache` exists on the host, and the counter copies only the 8 text files to scratch (no cache reachable) | yes (re-measured) |
| `receipts/c1-measured-r96.txt` | `MADO_MAGICTEXT_COUNT: TARGET_MET … rev=5dd921b3 tool_pin=ok cases=284 correct=284 classes=16/16 fresh=268/268 host=9822/9822 host_paths=4911 mutants=84 killed=84 crashed_not_killed=0 class_kills=16/16 static_no_external_resolver=ok audit_denials=0 selftest=ok checks=50 failed=0`, controls do-nothing 0/259 text-mode (20/20 none), name-only 32/284, naive 101/284, memoriser 0/40, forgery rejected | yes (evidence-verified) |
| `receipts/c1-at-c2-r96.txt` (separability) | `TARGET_MET` at `f54def27`, same legs (fresh 283/283 at its seed) | yes (evidence-verified) |
| replay at the tip (corroboration) | `MADO_MAGICTEXT_COUNT: TARGET_MET … rev=0caf2465 base_rev=9f029f46 … cases=284 correct=284 classes=16/16 fresh=272/272 (its own seed) host=9822/9822 host_paths=4911 mutants=84 killed=84 class_kills=16/16 selftest=ok checks=50 failed=0`, controls identical, rc 0 | yes (replayed, not closure evidence) |
| index and entry landed | `python3 -I quality/check-index.py --repo . --rev 0caf2465` → `indexed=117/117 missing=0 dangling=0 duplicates=0`; `corpus/knowledge/*.md` count 117; entry frontmatter opens with `source:` (S524, S525, S505, S520–S523), `verified-at:`, `recheck:` | yes (re-measured) |
| SOURCES census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, rc 0; rows `458 → 460` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), tier histogram `A=442 B=10 C=8`, malformed 0, duplicate ids none; S524/S525 `mined`, used-by paths exist | yes (re-measured) |

Before → after confirmed: **0/0 (no tool; the r95 tool refuses text mode) → 284/284 frozen cases, 16/16
classes, 9822/9822 host pairs, 84/84 counted mutants, 50/50 selftest**. Verdict: **coverage improved**
(capability demonstrated: `tools/mado-mimetext.py`, first-working round 96).

### C2 — operability: the last gate-compatible tool becomes guardable and guarded

| check (command) | observed | matches report |
|---|---|---|
| base has no kill-set | `git cat-file -e 9f029f46:quality/selftest-kills/check-receipt-presence.json` rc 128; absent at `5dd921b3` too (separability) | yes (re-measured) |
| base tool is not guardable as it stood | `git show 9f029f46:quality/check-receipt-presence.py` FAIL lines are `FAIL {name} rc=… out=…` / `FAIL {name} absent=…` / `FAIL fixture {exc}` (detail strings, not labels; `def selftest` at line 122 of 327) | yes (re-measured) |
| gate unchanged | `quality/check-selftest-strength.py` sha256 `2d6f1219…da61b` at base and tip; `git diff base tip -- quality/check-selftest-strength.py` empty | yes (re-measured) |
| tool and kill-set pins | `be716a63…ca962` (tool) and `305d735f…a495` (kill-set) = the freeze pins; kill-set holds 7 kills, `selftest_checks: 6`, six distinct labels | yes (re-measured) |
| `receipts/c2-measured-r96.txt` | `MADO_SELFTEST_KILLS: TARGET_MET … rev=f54def27 gate_pin=ok kills_pin=ok tool_pin=ok checks=6 labels=6/6 labels_covered=6/6 singleton_labels=6/6 positive=OK:0 neutralised_flagged=6/6 hand_flagged=31/31 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1 gate_selftest=ok control_hand_flagged=19/31 r90_leg=TARGET_MET r90_met=83/83 r90_killed=28/28` | yes (evidence-verified) |
| `receipts/c2-at-c1-r96.txt` (separability) | `SETUP_ERROR … quality/selftest-kills/check-receipt-presence.json` absent at `5dd921b3` | yes (evidence-verified) |
| tool selftest at the tip | `python3 -I quality/check-receipt-presence.py --selftest` → `RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0` | yes (re-measured) |
| replay at the tip (corroboration) | `MADO_SELFTEST_KILLS: TARGET_MET … rev=0caf2465 gate_pin=ok kills_pin=ok tool_pin=ok checks=6 labels=6/6 … hand_flagged=31/31 neutral_ok=6/6 … r90_leg=TARGET_MET r90_met=83/83 r90_killed=28/28`, rc 0 | yes (replayed, not closure evidence) |
| harm watch | `receipts/harm-final-r96.txt`: 22 legs, 21 rc 0 and `r90c1_portal_routing` rc 2 (its declared expectation since round 93); spot re-runs: `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed`; `check-selftest-strength.py --selftest` → `checks=11 failed=0`; `check-tool-ledger.py --repo . --rev 0caf2465` → `population=188 ledger_rows=188 uncovered=0`; `mado-mimetext`/`mimesniff`/`mimeglob` selftests green (50/26/19) | yes (evidence-verified + spot re-measured) |
| no owned axis harmed | `git diff base tip -- SCORECARD.md` = 40 added lines, 0 removed; no tool/quality bytes changed after `f54def27`; the only deleted lines in the round diff are the six rewritten SOURCES rows and the moved selftest block | yes (re-measured) |

Before → after confirmed: **hand weakenings flagged 0/31 → 31/31, single-check neutralisations 0/6 → 6/6,
singleton labels 0/6 → 6/6**, under the unchanged round-93 gate, with the round-90 main-path leg green
(83/83, 28/28). Verdict: **operability improved**.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | C1: a surface the coverage map did not hold (text `mime/magic`) enters core with an admitted entry, index 117/117, S524/S525 tier A, and a capability row demonstrated at 284/284 + 9822/9822 + 84/84 |
| operability | **improved** | C2: the last gate-compatible tool gains six labels, the selftest block after `main()`, and a 7-kill kill-set under the unchanged gate (31/31, 6/6, 6/6) |
| depth | unchanged | no separate depth claim; the new entry's §1–§7.3 are source-per-line, but §7.4 is stale (D2) |
| freshness | unchanged | S505/S523 digests re-fetched byte-identically; no entry-level re-verification claimed |
| calibration | unchanged | claims and SCORECARD rows match the receipts; post-report erratum `0caf2465` is append-only but the defect class is not yet mined (D12) |
| adjacency | unchanged | R96MConnector swept all 21 sibling `PROVINCE.md`s; no sibling claims the text MIME database; `update-mime-database`/`~/.local/share/mime` stay operator-owned |

## 4. Discernment spot-check (LEARNING.md, "checked from outside")

Re-opened live, 2026-11-07, from this session:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S524 — GLib 2.90.1 `xdgmimemagic.c` (new row, admit) | admit | `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimemagic.c` HTTP 200, 18289 B, sha256 `fcb1eafe748d3dc18f7f405d1078c8a32e313d23d2fab86b0f12e609ac2ce742` = the row's pin; the lesson quote `if (memcmp ("MIME-Magic\0\n", header, 12) == 0)` sits at line 814 exactly | **agree** | the row's anchor, digest and located quote reproduce; the scope (text magic parser/matcher) is what the file holds |
| S525 — shared-mime-info spec §2.5 (new row, admit) | admit | `https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html` HTTP 200, 59208 B, sha256 `e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e`; the quote `The file starts with the magic string "MIME-Magic\0\n".` is at line 387 | **agree** | exact quote, exact line; the duplicate URL against S523 is the expected W04 and is declared in the row and the lesson |
| `ar01s03.html` (reject) | reject | same host, `ar01s03.html` HTTP 200, 7048 B, `grep -c 'MIME-Magic'` → 0 | **agree** | the rejected page carries no format text, so it cannot ground the §2.5 claim; keeping it as a rejected row is correct taste |
| contract sentence "word size (1\|2\|4 only)" (reject as a model fact) | reject | `xdgmimemagic.c:432-448`: the parser accepts `word_size == 0` (only `!=0 && !=1 && !=2 && !=4` is an error); `:469` gates swap/modulo on `word_size > 1`, so 0 compares as single bytes | **agree** | the C's set is 0/1/2/4; the reject and the entry's correction are right |
| new-row quote length (SOURCES rule 1 / freeze contract) | — | S524 quote 9 words, S525 quote 10 words | **agree** | both ≤25 words, both located |

Sampled decision agreement: 4/4 (two admits, two rejects). The Gate section's per-row claims were checked
against the C source: the `mime.cache` validity test quoted in QUALITY 166 matches `xdgmimecache.c`
(≥40 bytes, version 1.1/1.2) as the frozen case seat's relabelling describes. One statement in the same
Gate section is false as committed — "S505, S519, S520, S521, S522, S523: `used-by` only, each appended"
(D1) — which is a record defect, not a gate decision.

## 5. Trend verdicts

- **expansion — improved.** A new admitted entry (`corpus/knowledge/mime-textdb-magic-r96.md`) on ground
  the coverage map did not hold (index 117/117), citing two new tier-A rows (S524, S525) plus the held
  GLib rows; capability row entered with a demonstrated run (284/284, 9822/9822, 84/84). No row quota was
  padded: rows 458 → 460.
- **quality — improved.** C1's instrument supersedes the round-95 refusal with a measured answer
  (284/284 frozen, 84/84 counted mutants, 16/16 class kills, four controls behind); C2 replaces "no
  instrument" with 31/31 hand weakenings, 6/6 neutralisations and 6/6 singletons under the unchanged gate;
  the harm watch stays green over every prior counter. The entry's §7.4 stale cells (D2) are a defect, not
  a falsified held entry: the table is self-labelled a placeholder, and the values it contradicts are
  correct in the receipt and in its own adjacent row. **Escalation:** if D2 is still unmarked at round 97,
  the entry becomes "found false or stale and left unmarked" and quality grades `harmed`.
- **discernment — improved.** Two L1 sentences were reversed by the wave before the freeze (the
  `mime.cache` proxy → five mislabelled cases; the word-size set and the indent rule) and both are mined
  as `QUALITY.md` 166/167 with a fail-shown fix. My outside sample agrees on 4/4 admits/rejects, and the
  one disagreement I found (D1) was not a gate decision.

## 6. Routed defects (status-neutral; the lane fixes them, priority order)

1. **D1 — the six `used-by` appends landed outside the table cell.** `corpus/SOURCES.md` rows S505,
   S519, S520, S521, S522, S523 end `… round-95.md |,corpus/knowledge/mime-textdb-magic-r96.md`: the path
   is after the closing pipe, so the cell still omits the entry and each row carries stray text. The
   report (§Sources "used-by only, appended …"), `LOG.md`, `SCORECARD.md` and the lesson all assert the
   change. The census's malformed-row check is blind to it (`NF` stays 13). Fix: move the path inside the
   used-by cell on all six rows; add a tail-of-line/`NF`-plus-trailing-text read-back to the registry
   check (`awk -F'|' '{ if ($NF != " ") … }'` or a `grep -E '\|[^|]*$'` row test).
2. **D2 — the admitted entry's measurement table is stale draft.** `mime-textdb-magic-r96.md` §7.4 says
   `265` frozen cases (receipt 284; its own next row says 284) and `97` mutants (receipt 84 killed / 84
   counted; the population is 84 + 13 not-observable + 13 equivalents) and closes with "Every cell above
   is a placeholder …". `corpus/README.md` repeats `265 frozen cases` (index row and frontier line) and
   `97 mutants`; `quality/tool-ledger.md` says the tool's `--selftest` is "20 checks" (it prints 50). Fix:
   replace §7.4 with the receipt's cells, delete the placeholder paragraph, sweep 265 → 284 and 97 →
   84/13/13 in README + ledger and grep every touched file for the superseded values.
3. **D3 — Gate standard §Registry.** No `SKILL.md` row exists for `quality/counters/c1-r96-magictext.py`
   or `quality/counters/c2-r96-selftest-kills.py` (rounds 93–95 each registered theirs), and the new pair
   (`quality/check-receipt-presence.py`, `quality/selftest-kills/check-receipt-presence.json`, 7 kills) is
   not in `mado-selftest-strength`'s (TOOL, KILLSET) list. Add name, gate|probe, entry command, verdict
   map, self-test spelling, pin path, write scope, owner.
4. **D4 — Gate standard §Self-test.** Neither new counter exposes a self-invocation mode over isolated
   fixtures asserting an exit code and a stable finding id (the r93–95 rows say "none" for the same
   reason). Add `--selftest` to both or register them as probes with the standing gap named.
5. **D5 — the declaration body's C1 command carries a stale pin.** Line 76:
   `--expect-mutants-sha256 f8d461e8…b806a`; the freeze block and the file pin `448150e2…bc440`, so a
   verbatim replay of the body command fails SETUP. Append an amendment naming both values (QUALITY 6).
6. **D6 — mutant population prose drift.** The freeze block says "97 mutants … (14 equivalents
   excluded)"; the frozen file holds 84 counted + 13 not-observable + 13 equivalents (110), and the draft
   `magictext-mutants-r96.json` holds 97 + 14 (111), with `indent-skip-current-level` absent,
   `indent-depth-guard-one` added and `indent-depth-guard` reclassified from equivalent to counted. State
   the population as 84/13/13 and name the reclassification (or restore the dropped id with its argument).
7. **D7 — the C2 declaration misquotes round-95 routed defect 3.** That defect names `tools/mado-mako.py`,
   `tools/mado-verify.sh`, `quality/check-receipt-presence.py`; the declaration substitutes
   `tools/mado-mimesniff.py` for the last and then selects receipt-presence as a "remaining tool". The
   landed work is the right item; correct the rationale text.
8. **D8 — the harm receipt was rewritten in place.** `8a0aadb0` committed it red (`ledger rc=1`,
   `mako_selftest rc=2`); `87a7d51` replaced it with the `harm2` rerun (all green) and no correction entry
   names the superseded bytes. The report says "at the final tip", SCORECARD says "at the C2 tip
   `f54def27`", the receipt header says `8a0aadb0`. Append the red-before/harness-fix record and label the
   measured revision `8a0aadb0` (no tool bytes changed after `f54def27`).
9. **D9 — role census drift.** The report says "4 executors"; `w1-results.json` and
   `w1/swarm-registry.json` hold 6 executor seats (14 = 5 attack + 6 executor + scout + connector +
   scribe). Report the census from the registry.
10. **D10 — `PROVINCE.md` has no trailing newline** (`git diff` shows `\ No newline at end of file`).
11. **D11 — the census receipts do not carry the counts cited to them.** `census-start-r96.txt` and
    `census-end-r96.txt` are the validator's warning lines; 458/460 are not in them (I re-derived 458/460).
    Put the count command and its output in the receipt, or cite the count separately.
12. **D12 — the post-report erratum is not mined.** `0caf2465` corrects the entry's claim that the cache
    version sits at bytes 4..7 (it is offsets 0..3, `GET_UINT16(buffer, 0/2)`); the class (an admitted
    sentence contradicted by the round's own frozen `loadable_cache`) is not in the lesson `## Mistakes`.
    Mine it next round (captured-by: none — the counter knew the right offset).
13. **D13 — the Landed-changes table stops at `8a0aadb0`.** `87a7d51` (final harm receipt + end census),
    `c20f060` (w1 results) and `0caf2465` (erratum) are not tied to it; only the first is described
    elsewhere in the report. Tie them in the next report/erratum (append-only).

Carried lane-routed items from the report itself (unchanged): the tool docstring's three line citations
(fixing them changes the frozen tool bytes and re-anchors every mutant); ten case gaps in the
declaration's `not_observable_not_counted`; `tools/mado-mako.py`, `tools/mado-mimesniff.py` and
`tools/mado-verify.sh` stay unguarded pending a gate-predicate change with rounds 93/94/95 counters
re-anchored (QUALITY 153/155). Round-95 routed defects 1, 2, 4 and 5 remain open and are re-flagged.

## 7. Operator notes (not lane defects)

- **SHONEN.** All four boxes look checkable by a non-author from committed evidence: box 1 by the
  `SKILL.md` instrument rows and this round's entry; box 2 by the C1 run and its receipt; box 3 by the
  entry's §5 commands and the registry row; box 4 by R96MConnector's 21-lane `PROVINCE.md` sweep (a
  dispatched seat, so still the lane's own work, but a resolvable pointer). Promotion is operator-owned;
  the lane filed `[~]` only and wrote no `[x]`.
- The round's two claims reproduce at the tip (`0caf2465`) as well as at their landing revisions; the
  capability and the guard both hold. The defects above are record/registry defects, not claim failures.
