# R74ScoutFrontier — what the next round can stand on

author: R74ScoutFrontier (leaf seat, round 74 wave 1)
read at: 2026-11-04, after the freeze `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` and during the
closure write; lane base `bd5a971532f37df85a78f6f566dd1e649b79de11`. No counter, gate or live
probe was executed (the only instrument invocation was `check-session-material.py --help`, rc 0).
No file outside this seat directory and its `/fast` scratch was written.

**Read-time state, stated once.** The closure files were being written while this sweep ran
(`git status --porcelain` moved between reads). Facts below are pinned by path and line; items
marked *working tree* were uncommitted at the last read (`M LOG.md SCORECARD.md SKILL.md
PROVINCE.md QUALITY.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md
quality/tool-ledger.md`; untracked `corpus/knowledge/*-r74.md`, `corpus/lessons/round-74.md`,
`.ufo/waves/round-74/{measurement-*,receipts/,fetch/,w1/}`). Anything a reader needs as evidence
depends on the closure commit landing those bytes unchanged.

## 1. `considerthese/` sweep — the newest file (2026-10-28) and the one proposal that fits

Six proposals at `considerthese/2026-10-28.md:52-57`. Status at read time, with the sweep that
settles each:

| # | proposal (line) | status | evidence |
|---|---|---|---|
| 1 | never miss a day silently (`:52`) | unimplemented | `ls considerthese/` has no `2026-10-27.md`; no placeholder rule exists. Reflection-scheduling, **not** instrument ground |
| 2 | re-check the privacy risk daily (`:53`) | **already executed** | `LOG.md:3267-3269` (round 67): gate run at the pre-r67 tip, exit 1, `files=33466 findings=280`, `waived 49/47`, the r37/r38 socket tables carry 5 and 715 proc rows — routed to L0 as an operator history/redaction decision. Residue operator-owned, not unimplemented |
| 3 | streak line in each reflection (`:54`) | unimplemented | no `streak` line in any `considerthese/*.md`; reflection header, not instrument ground |
| 4 | live-tool table with `last live run` (`:55`) | **unimplemented — instrument ground** | self-admitted at `:47` ("the last-live-run column is still open") and `LOG.md:2595` ("last-live-run freshness is not claimed"); repeated `SCORECARD.md:2795` |
| 5 | separate "relayed" from "re-measured" (`:56`) | unimplemented for reflections | `corpus/QUALITY.md:399` (criterion 76) already fixes the exact `relayed:` marker **for mining notes** ("because the reflection is a pointer, not evidence"); the open half is a reflection convention, not instrument ground |
| 6 | flag adopted proposals (`:57`) | implemented | the same file carries the adoption table at `:47` |

**Pick: proposal 4, the `last live run` cell.** Quote, `considerthese/2026-10-28.md:55`: "**Keep a
live-tool table.** There are now 8 live-state tools. One row each (question answered, last live
run, verdict, who ran it) would show which ones João can run himself today." The lane's own record
locates the open half in the ledger, not in prose: `:47` "the last-live-run column is still open".

Bar grounding (both quotes re-read, not relayed):

- `PROVINCE.md:147` fixes the lane's dated-observation row form: "Each row: the PROVINCE-declared
  surface group, its state **on this host**, the observation date, and the read-only probe that
  re-derives the state." The register it heads (`PROVINCE.md:145-153`) is the precedent: a dated
  row per declared surface, state + date + re-deriving probe. A live-tool row is that same form
  applied to the eight `tools/` live modes.
- `corpus/QUALITY.md:409` (criterion 81) fixes the named-channel discipline: a closure's counts
  come "each from a named channel", with cleanliness "from a receipt committed at the revision the
  round closes on". A last-live-run cell must name its channel the same way (date + revision or
  receipt), never a remembered run.
- Instrument ground today: the ledger's enforced row grammar is three cells only — path,
  description, pointer (`quality/check-tool-ledger.py:18-22`; data rows 130 at
  `quality/tool-ledger.md`), so the ledger cannot state freshness, and `LOG.md:2595` /
  `SCORECARD.md:2795` record that gap across rounds 51→73.

Next-round shape that fits without harming the frozen ledger: a **separate dated register**
(e.g. `quality/live-tool-runs.md`, one row per live-state tool: question, last live run
date + revision/receipt, verdict, who ran it) plus a checker; `quality/check-tool-ledger.py` and
every held instrument stay byte-identical, and offline counters read `offline`. A column bolted
onto the ledger would change the checker's frozen contract and is the wrong cut.

## 2. Routed defects D1–D7 vs the round-74 tree

Source: `corpus/lessons/round-73-verifier-spotcheck.md` § Routed defects (D1–D7). "Closed" means a
file in this round's tree now carries the repair; all such files were **uncommitted** at read time.

| id | status | closing evidence in this round's tree | residue |
|---|---|---|---|
| D1 S448 digest false | **closed append-only (working tree)** | `corpus/SOURCES.md` S452 row supersedes S448 and states the true digest `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` (208,655 B); § Round 74 prose at `corpus/SOURCES.md:877-882`; `corpus/lessons/round-74.md:81-92` ("closing round-73 D1 append-only"), M74-3 at `:45`; criterion 122 at `corpus/QUALITY.md:853`. S448's own cell keeps the false digest by design | **the "sweep every mention" half is not done**: `corpus/lessons/round-73.md:72` still prints the false digest with no erratum; the three round-74 fetch receipts agree on the true bytes |
| D2 post-repair selftest tallies have no committed run | **open** | — | `grep -rn '26/26\|78/78' .ufo/waves/round-73/receipts/` → empty; `.ufo/waves/round-74/receipts/` holds only `m74-1-red.txt`, `m74-2-red.txt`; `corpus/lessons/round-73.md` tail still states 26/26 and 78/78. The 26/26 / 78/78 claims remain evidence-free |
| D3 a receipt overwritten in place | **open** | — | `.ufo/waves/round-73/measurement-c{1,2}-r73.txt` each carry one contract line (`grep -c` = 1); last touched `422ba69a` (round-73 closure). The `1459cca1` run survives only inside `84fc266a`'s version; nothing appended |
| D4 QUALITY 118/119 in the root fragment | **closed (working tree)** | `corpus/QUALITY.md` now ends at criterion **123** (118 at `:807`, 119 `:820`, 120 `:832`, 121 `:843`, 122 `:853`, 123 `:861`); root `QUALITY.md` keeps 118–119 plus a redirect note ("read `corpus/QUALITY.md`"); criterion 123 makes placement the rule; M74-4 records red (`grep -c '^118\.'` → 0) and green (→ 1) | none; the root fragment stays as history, as declared |
| D5 S446 has no ≤25-word located quote | **closed** | `corpus/lessons/round-74.md:94-102` re-opens the reject with a 23-word located quote, `stdtypes.rst:5525-5527` (`setdefault`): "If key is in the dictionary, return its value. If not, insert key with a value of default and return default." | none |
| D6 `verified-at:` names the pre-repair commit | **open (note)** | — | `corpus/knowledge/control-set-mutant-kill-r73.md:3` and `guard-carrier-global-environ-r73.md:3` still name `1459cca1…`; no entry refresh this round (the two r74 entries are new files, not refreshes) |
| D7 stale routing sentence vs `task.agentModelOverrides` | **operator-owned** | — | carried from r72; the prompt names the config as authority and passes no model (`round-73-verifier-spotcheck.md` item 7). Not lane debt |

Net: two closures the declaration promised (D1, D5) landed, plus the unplanned D4 repair; D2 and
D3 — the two evidence gaps the spot-check called medium — remain exactly as routed; D6 needs the
next entry refresh; D7 stays with the operator. The declaration's own sentence "D3 … by appending
both runs" and "D2 … by committing the post-repair selftest receipts" are not yet satisfied.

## 3. `corpus/README.md` § Frontier (round 73) and `SCORECARD.md` § Planned (round 74)

- `corpus/README.md:134` (round-73 bullet): round 73 measures the control set rather than the rule
  (four named mutations separated 4/4 against the held 2/4) and extends the guard census's carrier
  grammar to a `global`-declared store and a mutated-`os.environ` copy. Round 74 is its successor
  bullet at `:133` (witness credit; two-hop and `os.environ`-alias carriers; S450–S452, S452
  superseding S448).
- `SCORECARD.md:4091` `### Planned (round 74; intent only)`:
  - **Lands** — item 1: C1's stale/replay class as frozen negatives once a witness can be grounded;
    this round grounds it on `secrets.token_hex` (S450) and ships four replay cases (12 cases,
    `17c95774…`), held 8/12 → candidate 12/12.
  - **Lands** — item 2: C2's two-hop store and one-hop `os.environ` alias, each with its own
    negatives (36 cases, `4db4cc70…`; held 32/36 → 36/36; the four new positives are exactly the
    held classifier's misses).
  - **Does not land** — item 3: the `summary_fraction()` first-vs-summary ambiguity (a successor
    contract field reporting the summary fraction and flagging disagreement) has no instrument,
    case or tree file this round; it is carried into the round-74 block's own
    `### Planned (round 75; intent only)` item 3 (`SCORECARD.md:4158+`).
  - **Does not land** — item 4: the open L0 questions (r57–r60, the L2 floor, the host-recovery
    pacman pause, the r37/r38 session-material history question) stay operator-owned; the round
    probes no host plane.
- Bookkeeping gap worth one line in the next round: the **canonical** `## Planned` section
  (`SCORECARD.md:215-217`) still reads "no entries declared by this conformance rollout". Every
  recent round's plan lives inside the previous round's block (`:4091`, now `:4158`), so a reader
  who goes to the section the AXES contract names finds nothing for round 74.

## 4. Sibling overlap (read-only sweep of `/home/vgpnk/Projects/shokunin/*-shokunin/corpus`)

Method: `grep -rl` for `nonce`, `challenge`, `witness`, `GIT_NO_REPLACE_OBJECTS`, `guard census`,
then inspection of the same-ground files only. Counts (files): kotodama 210, game-dev-3d 128,
tabi 127, tameshi 80, kengaku 70, mori 69, mado 54, chousa 46, kaidoku 43, kumitate 38, kama 36,
kake 32. Most hits are the words in unrelated senses; the lanes that hold the ground are:

| lane | path | shared ground | what it already holds |
|---|---|---|---|
| kumitate-shokunin | `corpus/knowledge/invocation-attestation.md:27-31`; `corpus/knowledge/receipt-identity-canonicalization.md` | nonce / challenge / replay | a 128-bit per-receipt nonce and nonce ledger; the frozen predicate's **probe-issued challenge arms** (A2c/A3c/A4c/A3d); `RECEIPT: REPLAY` on nonce reuse. The closest existing instrument to mado C1's witness |
| mori-shokunin | `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md:27-39`; `corpus/knowledge/verdict-machine-r5.md`; `corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md` | per-run challenge echo | the measured statement mado's C1 limit restates: "Echoing a per-run secret authenticates freshness, not measurement" (`:37`), with two forgers still at 28/28 |
| kake-shokunin | `corpus/knowledge/receipt-integrity.md:10` | replay / rebinding | "the file is then evidence of *some* run, not of *this* one, and 'witnessed' becomes a statement about a directory" |
| tabi-shokunin | `corpus/SOURCES.md:157` (S143); `corpus/lessons/round-37.md:14,35-36`; `corpus/knowledge/receipt-authenticity-signing-round-43.md` | `GIT_NO_REPLACE_OBJECTS` guard + authenticity | an admitted git-replace/GNRO source row; a C2 counter that pins `GIT_NO_REPLACE_OBJECTS=1` on every git read plus a `refs/replace/*` enumeration refusal |
| kotodama-shokunin | `corpus/lessons/round-80.md:19-22` | GNRO guard | replace-ref refusal + GNRO pin as round-79 hardening (`MutPath F6`) |
| souji-shokunin | `corpus/lessons/round-23.md:128,157-158` | GNRO guard | counter hardened with GNRO; a `git replace` counterexample now refuses |
| kama-shokunin | `corpus/lessons/round-30.md:78` | GNRO guard | control arm `GIT_NO_REPLACE_OBJECTS=1`; replace refs did not move the counter ("replace refs do not prove authenticity" family) |
| chousa-shokunin | `corpus/knowledge/env-pin-capture-r38.md` | environment as evidence | a bare `env` child delivered exported shell functions — env capture, not the alias census |

`guard census` as a term is **mado-only** (0 hits outside this lane): the census instrument and its
carrier vocabulary are not contested. The ground mado shares is narrower and real — the
nonce/challenge/replay *rule* (kumitate, mori, kake) and the `GIT_NO_REPLACE_OBJECTS` *carrier*
(tabi, kotodama, souji, kama). No sibling writes; no sibling report read.

## 5. What the next round can stand on

- **Sources**: S450 (`secrets.token_hex`, 21-word quote, `289ff11e…`), S451 (`simple_stmts.rst`
  attribute reference, 24 words, `d4320642…`), S452 (`os.environ`, 16 words, `2d0f2892…`) are
  admitted with three byte-identical fetches each and located quotes in
  `corpus/lessons/round-74.md:56-92`; criterion 122 makes the digest re-derivation a rule.
- **Instruments**: `quality/counters/c1-r74-witness-rule.py` (21/21), `c1-r74-replay-witness.py`
  (21/21), `c2-r74-shapes.py` (86/86) — registered in `SKILL.md`'s Gate registry and in
  `quality/tool-ledger.md:166-168`. Contract lines read from the committed receipts:
  `cases=12 correct=12 base_correct=8 verdict=TARGET_MET`,
  `population=20 readers=13 guarded=13 unguarded=0 controls=36/36 base_controls=32/36
  verdict=TARGET_MET`, both `rev=b73db773…`.
- **Bar**: criteria 120 (the fixture lane is the mutated lane), 121 (labels scored by the
  do-nothing control before freeze), 122 (digest re-derived, superseding row), 123 (criteria land
  at `corpus/QUALITY.md`) now sit at the contract path — directly reusable by the next round.
- **Standable open work**: D2/D3 evidence (two committed receipt runs, append-only), D6 entry
  refresh, the live-run register (proposal 4), and the round-75 planned items 1–3 (wire the
  witness rule into a successor landing harness; the generic `del env[KEY]` / `dict(alias, KEY=…)`
  spellings; the `summary_fraction()` field).
- **Open unknowns**: the closure commit and whether it lands the working-tree bytes exactly as
  read; the wave seats' own reports (not read here); whether S448's stale mention in
  `corpus/lessons/round-73.md:72` is swept by an erratum or accepted as append-only history. No
  claim here is evidence for a counter verdict — none was executed.
