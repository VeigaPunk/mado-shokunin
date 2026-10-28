# R55RevQuality — round 55 wave w1, quality reviewer (non-author, read-only)

Report: .ufo/waves/round-55/w1/R55RevQuality.md

## Deliverables

- `.ufo/waves/round-55/w1/R55RevQuality/criterion.md` — draft QUALITY criterion 106 (text only; freeze-order rule, check form, round-54 shown-able-to-fail pointers, declared limit).
- `.ufo/waves/round-55/w1/R55RevQuality.md` — this report.

## What I did

- Read the frozen contract (`claims-frozen.md`, `registration.md`), `corpus/QUALITY.md` criteria 90–105 (and the grouping at 1–89 where they bind), `corpus/lessons/round-54.md` Mistakes M54-1..M54-7, and the round-54 routing in `corpus/lessons/round-54-verifier-spotcheck.md`.
- Ran only read-only git (`show`, `log`, `ls-tree`, `cat-file`, `grep`, `merge-base`, `diff --quiet`, one `status --porcelain`) at lane HEAD `dbc2eefe`, and read-only lane checkers/verifiers listed below. No writes into the lane beyond my two deliverables; no tracked-file edits; no git/jj mutation; no commits; no subagents; no background jobs.
- Host: not read (no `hyprctl`, no `~/.config/hypr/input.conf`). No tool installed or updated (none needed).
- Hold-out: I did not look for, list or open `fixtures/c2-holdout/` or any hold-out path. I did not touch `c2.holdout_commit_sha256` beyond confirming the key exists.
- Scratch: `/fast/scratch/hyaku/mado-r55/R55RevQuality/` created, nothing needed inside it, removed before yield.
- Not run: `quality/check-freeze-order.py` (absent at HEAD; being built by another seat), `quality/check-landed-contract.py` (no landed `tools/mado-kbdopts.py`), the C1/C2/C3 counters and harnesses (other seats' scope), checks 92/93/95 (not applicable to this seat's read-only role; described only).

## Decisive command outputs

```
$ git show -s --format='%H %cI %s' 54dacbd843d64ba744cd3f1bdc2ec622e5010039
54dacbd8… 2026-10-28T18:46:52-03:00 round-55: freeze claims, registration, tables, fixtures, controls and baseline before any dispatch
$ git show -s --format='%H %cI' dbc2eefee5bb1d2c3f42ce56828b99bd9d81c333      (first add of w1-dispatch.json, w1-spec.json, w1/swarm-registry.json)
dbc2eefe… 2026-10-28T18:50:20-03:00
$ git merge-base --is-ancestor 54dacbd8… dbc2eefe…; echo $?        → 0
$ grep '"createdAt"' .ufo/waves/round-55/w1/swarm-registry.json      → "createdAt": "2026-10-28T21:50:15.231Z"   (18:50:15 −03)
$ git --no-optional-locks status --porcelain .ufo/waves/round-55/w1.ready .ufo/waves/round-55/w1.ready.dispatched
?? .ufo/waves/round-55/w1.ready
?? .ufo/waves/round-55/w1.ready.dispatched
$ git diff --quiet 54dacbd8… -- <fetch, fixtures/c2, frozen-tables.json, claims-frozen.md, registration.md, ctl, freeze-verify.py}; echo $?   → 0
$ python3 -I .ufo/waves/round-55/freeze-verify.py | tail -1
FREEZE_VERIFY: bad=0 frozen-tables.sha256=bf46c889…4179490 OK          rc=0
$ python3 -I .ufo/waves/round-48/w1/ScrMistakes/check100.py --spec .ufo/waves/round-55/w1-spec.json
PROSE .ufo/waves/round-55/w1-spec.json ceiling=50 MB
CHECK100: sources=1 enforced=0 prose=1 verdict=PROSE-ONLY            rc=1
$ python3 -I .ufo/waves/round-48/w1/ScrMistakes/check100.py --spec .ufo/waves/round-55/w1-dispatch.json
PROSE .ufo/waves/round-55/w1-dispatch.json ceiling=50 MB
CHECK100: sources=1 enforced=0 prose=1 verdict=PROSE-ONLY            rc=1
$ grep -c ulimit .ufo/waves/round-55/w1-spec.json .ufo/waves/round-55/w1-dispatch.json      → 0 0
$ git show -s --format='%cI' 350d30e4ec5531f65ce99a57efeb8216f38e678a          → 2026-10-27T14:11:10-03:00
$ git log --diff-filter=A --format=%H -- .ufo/waves/round-54/w1-dispatch.json → 350d30e4…  (same commit: freeze and dispatch file in one step)
$ git cat-file -e e25149fe…:.ufo/waves/round-54/registration.md; echo $?   → 128
$ git cat-file -e 350d30e4…:.ufo/waves/round-54/registration.md; echo $?   → 0
$ git log --format='%H %cI' -- .ufo/waves/round-54/w1-results.json        → 9ea87392… 2026-10-27T15:05:36-03:00 (only commit)
$ git show a67195cc…:.ufo/waves/round-54/w1.ready.dispatched | head -1     → 2026-10-27T14:06:21
$ git show 9ea87392…:.ufo/waves/round-54/w1-results.json | sed -n 52p       → "...after w1 dispatch (14:05:25) and ready (14:05:28)..."
$ git show a67195cc…:.ufo/waves/round-54/w1.ready                          → {"lane":"mado","round":54,"wave":"w1",...}  (no instant)
$ git grep -n -E '\bP19\b' 3b55b6e… -- corpus SKILL.md PROVINCE.md         → errata:17 (P19 row); lessons round-52/53/54 mentions
$ sed -n 70p (git show 3b55b6e…:corpus/knowledge/hyprland-input-devices-r46.md) → "...applied per device too but the dump prints none of them ... UNK for this join."
$ git show 3b55b6e…/round-52 fetch ConfigActions.cpp 1554-1576: Q08 "} else {" 1566; Q09 sendKeyboardKey PRESSED 1568; Q10 RELEASED 1569
$ sed -n 1115,1123p legacy ConfigManager.cpp → getConfigValueSafeDevice: `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty()) return m_config->getConfigValuePtr(fallback);`
$ sed -n 1131,1137p legacy ConfigManager.cpp → getDeviceInt: `auto val = getConfigValueSafeDevice(...); return std::any_cast<Hyprlang::INT>(val->getValue());`
$ grep -n -E 'm_min|m_max|\.min|\.max' fetch/*.cpp fetch/*.hpp  → only ConfigValues.cpp declarations (:168+) and dump lines (:54, :68, :82); no enforcement site
$ grep -n -E 'm_min|m_max|\bmin\b|\bmax\b' .ufo/waves/round-46/fetch/hyprlang-config.cpp → std::max/"max iteration" only; no range check
$ grep -n -iE 'out of contract|Also out' registration.md claims-frozen.md             → (no output)
$ grep -c ctl frozen-tables.json                                                       → 0 (ctl/ stubs unhashed)
$ ls quality/__pycache__  → check-session-material.cpython-314.pyc, check-tool-ledger.cpython-314.pyc (gitignored, .gitignore:3)
```

## Criteria per claim: applicability and status

Status words: SATISFIED (by design; unrun unless stated), PARTIAL, MISSED, N/A.

### C1 — keyboard repeat/delay/numlock entry (PRED-C1-r55)

| Criterion | Applies because | Status and evidence |
|---|---|---|
| 93 clean-state receipt for a gate | counter + harness are gates | SATISFIED by design (`good=ok`, 7 named-leg controls). No clean receipt at a final revision yet; only `receipts/before.txt` (0/0/0). |
| 95 writes only under `--work`; inventory | counter reads git objects, writes scratch | PARTIAL. Contract says "honour --work" but has no before/after `find -newer` inventory leg, and `python3 -I` does not imply `-B`. `quality/__pycache__` already holds two cpython-314 pyc files (gitignored), the class 95 was written for. |
| 97 corpus-to-corpus locator | entry will cite `corpus/knowledge/hyprland-input-devices-r46.md:70` | PARTIAL. The one locator the contract cites resolves and is verbatim at base (line 70 checked above). Entry prose locators are not frozen and no check99 leg is wired. |
| 100 host-consequence cites the setter | "device value if the user set it" | MISSED. The model rests on the read `!VAL->m_bSetByUser` at legacy ConfigManager.cpp:1119; the setter of `m_bSetByUser` is in no pin. `std::max(0,…)` at InputManager.cpp:1282-1283 is a clamp, not a state-setter claim. No STATE_CLAIM list exists, so 100 is not run. |
| 104 sentence-to-pin | K/H proposition sentences | MISSED by design. Contract freezes pin/line/quote, propositions only as "≥40 chars". Declared limit hands this to the w2 audit. freeze-verify checks substring-in-line only. |
| 105 falsification grammar | seven controls | SATISFIED by design. Each control names the leg it must trip; the harness reads `missed=` lines and treats absence as failure (answers M54-6). Not run by me. |
| 15 label by version/era | pins are tag `efb50993` (0.56.2) and cite `src/config/legacy/` | PARTIAL. The era boundary (main has no `src/config/legacy/` and drops the device block past 0.56.x) lives in `corpus/knowledge/hyprland-input-devices-r46.md:14`, not in the frozen C1 text. |
| 90, 91 | C1 routes nothing; H rows cite pin bytes, not run receipts | N/A (91 becomes live if the entry adds `hyprctl` output as a receipt). |

### C2 — `tools/mado-kbdopts.py` (PRED-C2-r55)

| Criterion | Applies because | Status and evidence |
|---|---|---|
| 96 landed contract not narrower than frozen | tool is landed later against a frozen grammar | MISSED (instrument vacuous). The frozen text enumerates no `Out of contract:` / `Also out of contract:` list (grep above: none), so `quality/check-landed-contract.py` cannot register any delta and would report added=0 removed=0 by construction. Out-of-model rule exists only as prose ("everything outside it is unsupported"). [Reading of the 96 grammar; the script was not run because the tool is not landed.] |
| 100 model cites what sets the state | "out-of-range → unsupported +1, line ignored" cites ConfigValues.cpp:277-280 | MISSED. In the pins, 277-280 is a `MS<Int>` declaration with `.min/.max`; no enforcement site exists in `fetch/` or in the round-46 hyprlang pin (grep above). The reject-and-ignore behaviour is a modelled choice, not a sourced host consequence. |
| 104 + 15 declared limit | "hyprlang 0.6.8 as Hyprland 0.56.2 reads it" | MISSED. Declared limit omits that Hyprland main drops the `device {}` form (r46 entry line 14), so the tool's grammar is era-bound and the contract does not say so. |
| 95 read-only, writes nothing | registration says so | PARTIAL. Stated in text; no inventory leg. |
| 105 falsification grammar | three controls + eight hold-out | SATISFIED by design. `holdout_commit_sha256` key exists in `frozen-tables.json`. Hold-out not examined. |
| 93 | harness is a gate | SATISFIED by design (as C1). |
| 98 | seats run the dispatch | see Freeze and dispatch below. |

### C3 — append-only correction of P19 (PRED-C3-r55)

| Criterion | Applies because | Status and evidence |
|---|---|---|
| 4 (admission bar) errata append-only | P19 correction | SATISFIED by design. `prefix` leg is byte-identity to base blob `3b55b6e`; `base_blob_ref` is frozen. |
| 90 routed-defect identity and age | contract says "routed defect 1 of the r54 closure; M54-5" | MISSED. First locator exists (`corpus/lessons/round-54-verifier-spotcheck.md:61` P19 row; `:73` routing, owner mado) but the frozen claim cites neither line nor age (age = 1 round at R55). |
| 104 sentence-to-pin | P23 proposition | PARTIAL. The `p23` leg checks token presence (`m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED`, one of `otherwise`/`any other`/`else`). A P23 that contains every token and still states the else arm sends only PRESSED passes the leg. Pin facts for the audit: Q08 `} else {` :1566; Q09 keyboard PRESSED :1568; Q10 keyboard RELEASED :1569. Semantic gate is w2 only (declared). |
| 28 present-tense supersession sweep | P19 is superseded by P23 | PARTIAL. The readme leg covers `corpus/README.md` only. P19 text is stated in the errata row (which append-only rules keep as bytes) and quoted in round-52/53/54 lessons. The integrator should check every owned file that still states the old value. |
| 93, 95 | counter/harness | as C1. |

### Freeze order and dispatch (the mistake-fix item; QUALITY 106 draft in `criterion.md`)

| Criterion | Applies because | Status and evidence |
|---|---|---|
| 106 (draft) freeze strictly before launch record, and the record names the freeze | M54-2, M54-4 | Round 55 green arm: freeze 18:46:52 −03 < registry `createdAt` 18:50:15 −03; `54dacbd` is an ancestor of `dbc2eefe` (rc 0); `w1-dispatch.json` contains `54dacbd`; frozen paths unchanged since freeze (`diff --quiet` rc 0). Expected OK by hand. Round 54 red arm: freeze and dispatch first-added in the same commit `350d30e4` (14:11:10) and the committed launch instants are 14:06:21 and 14:05:25 (conflicting). Expected LATE by hand. Checker not delivered, so not run. |
| 98 wave scratch bound enforced by the dispatch | `w1-spec.json` and `w1-dispatch.json` are writer dispatches | MISSED. `check100.py` reads PROSE-ONLY, rc 1, for both files (`enforced=0 prose=1`, "ceiling=50 MB" in prose); `ulimit`/RLIMIT/`max_file_bytes`/`--size-cap` count 0. This is the M48-5 pattern on the live wave. |
| 7 hash from `git show <commit>:<path>` | `freeze-verify.py` is the proof of pins and fixtures | PARTIAL. `freeze-verify.py` reads working-tree bytes (`open(f"{W}/fetch/{f}","rb")`), not commit bytes. Equality with the freeze holds now (frozen paths `diff --quiet` rc 0), but the script itself does not prove it. The `ctl/*.py` stubs are not hashed by `freeze-verify.py` or recorded in `frozen-tables.json` (`grep -c ctl` → 0); they rest on git tamper-evidence only. |
| 9 bind verdict to commit or frozen-copy sha | `FREEZE_VERIFY` line | SATISFIED-with-note. Line binds `frozen-tables.json` sha256 only, not a commit sha. |
| 13 committed evidence | `.ready` is the launch record | PARTIAL. `w1.ready` and `w1.ready.dispatched` are untracked at `dbc2eefe` (`??`). Launch evidence committed for round 55 is `w1-dispatch.json` + `swarm-registry.json`. |
| 102 / 103 closure | round report | N/A at this seat (no `w1-results.json` at HEAD yet); applies at closure. |
| 99 closure section leads with outcome | SCORECARD | N/A to seats. |

### Criteria 90–105 applicability summary

- Apply strongly: 90 (C3), 93 (C1/C2/C3 gates), 95 (all counters), 96 (C2), 97 (C1), 98 (dispatch), 100 (C1, C2), 104 (C1, C3), 105 (C1, C2), 106 (freeze order), plus 7, 9, 13, 15, 28 by reference.
- Not applicable to a seat: 91 (no run receipt about a landed surface in the contract), 92 and 99–103 (closure).

## Defects and ambiguities (each with its input)

1. **Round-54 M54-2 evidence is internally inconsistent.** Committed `w1.ready.dispatched` (a67195cc) says `2026-10-27T14:06:21`; the committed `w1-results.json` (9ea87392, line 52) says dispatch 14:05:25 and ready 14:05:28. The lesson's "w1-results.json records 14:05:25" points at a file first committed 54 minutes after the freeze (9ea87392, 15:05:36 −03), so the lesson's pointer is itself a later commit. The verdict (freeze after launch) survives every reading; the cited instant does not. Criterion 106's `src=` field exists for this reason.
2. **Round 54: freeze and dispatch are the same commit.** `350d30e4` first-adds `w1-dispatch.json`; the launch record cannot name the freeze sha. Shown by `git log --diff-filter=A`.
3. **Round 55 wave has no committed scratch ceiling.** `check100.py` PROSE-ONLY rc 1 on `w1-spec.json` and `w1-dispatch.json`; `grep -c ulimit` 0 on both. Criterion 98 red for the live wave.
4. **C2 out-of-contract list absent.** No `Out of contract:` / `Also out of contract:` line in `registration.md` or `claims-frozen.md`; criterion 96's instrument reads nothing and cannot detect narrowing.
5. **C2 out-of-range rule is unsourced.** ConfigValues.cpp:277-280 declares `.min/.max`; no enforcement site appears in any committed pin (`fetch/`, `round-46/fetch/hyprlang-config.cpp`). "Unsupported +1, line ignored" is a model choice the contract presents as sourced.
6. **C2 era boundary missing from declared limit.** `corpus/knowledge/hyprland-input-devices-r46.md:14`: "Hyprland main has no src/config/legacy/ … drops the `device { }` block form"; the frozen C2 limit does not mention it.
7. **C1 setter not cited.** "Device value if the user set it" rests on `m_bSetByUser` read at legacy ConfigManager.cpp:1119; its setter is not pinned (criterion 100).
8. **C3 routed-defect locator and age absent from the frozen text** (criterion 90). The locators exist at `corpus/lessons/round-54-verifier-spotcheck.md:61,73`.
9. **C3 p23 leg is a keyword check.** A P23 proposition with all tokens can still misstate the else arm (`ConfigActions.cpp:1566-1569`, Q08–Q10). The semantic check is the w2 audit only (declared; consistent with 104's limit, but the leg reads as stronger than it is).
10. **freeze-verify.py reads working-tree bytes, not committed bytes** (criterion 7) and does not hash `ctl/*.py`. Current tree equals the freeze commit for all frozen paths (`git diff --quiet 54dacbd …` rc 0), so no present defect, but the proof is not self-contained.
11. **Launch markers untracked.** `w1.ready` and `w1.ready.dispatched` are `??` at HEAD `dbc2eefe`. Committing them after the freeze is the intended order; committing them before the freeze would break criterion 106 leg (a).
12. **Pre-existing bytecode in the scored tree.** `quality/__pycache__` (gitignored, `.gitignore:3`) holds `check-session-material.cpython-314.pyc` and `check-tool-ledger.cpython-314.pyc` dated 2026-10-27. The contract's `python3 -I` does not prevent this (criterion 95's exact class); `-B` or `PYTHONDONTWRITEBYTECODE` plus an inventory leg would.

## Not verified

- `quality/check-freeze-order.py`: absent at HEAD; the round-54 and round-55 verdicts in `criterion.md` are hand-derived from the git objects above and must be re-run when the checker lands.
- The C1, C2, C3 counters and harnesses, `check-landed-contract.py`, `check-r55-controls.py`, `check92`, `check93`, `check95`: not run by this seat (other seats' scope, or the tool does not exist yet).
- Host: not read.
- Hold-out fixtures: not used, not located, not opened.
- The `legacy` source-path identity for 0.56.2 (`src/config/legacy/ConfigManager.cpp`) is taken from the pinned file header and the r46 entry; I did not independently fetch the tag.
- Lane tool installs: none; no pacman transaction; no hyprctl call.

## Tooling record

None installed, updated, or invoked beyond `python3 -I` on read-only lane scripts (`freeze-verify.py`, `check100.py`) and standard git read verbs. No package manager touched.

Report: .ufo/waves/round-55/w1/R55RevQuality.md
