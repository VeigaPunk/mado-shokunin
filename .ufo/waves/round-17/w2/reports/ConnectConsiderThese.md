# ConnectConsiderThese — joining `considerthese/2026-10-20.md` to round 17

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD
`988b858bd6049bc709807534fd725c05264f7e60`. Read-only reflection: no edit outside this
report, no commit, no package/service/compositor/input operation, no live probe.
**Installs this item: none.**

Read-scope disclosure before anything else, because this round's subject is undisclosed
reads: I invoked the allowed `--scan` on
`MadoR15/MadoR15.LibinputEvents.jsonl`, and I opened one line of
`MadoR16/MadoR16.CustomMan.jsonl` (line 24) that this item's text does not name. Both are
inside the contract's *allowed tool* clause, outside its *named transcript* clause. The one
thing the direct read added (`pacman -Q waybar` at CustomMan:24) is already in the
committed receipt `tripwire-r16.txt`, so the report cites the receipt and the read is
recorded here rather than hidden.

Revision binding: every claim below is against the pushed HEAD `988b858`. While I read, the
working tree carried four tracked modifications by other wave-2 seats (`corpus/README.md`,
`corpus/SOURCES.md`, `corpus/knowledge/terminal-route-r17.md`, `corpus/lessons/round-17.md`).
I did not edit or revert any of them; where a finding is already being corrected live, §4
says so at both revisions.

Everything below is joined, not taught: the two considerthese proposals are external text,
the round-17 artifacts are lane bytes, and the join says where they coincide and where they
do not.

---

## 0. What I reproduced first-hand (so the join rests on measured bytes)

| item | command | result |
|---|---|---|
| C1 at HEAD | `python3 .ufo/waves/round-17/measure.py HEAD` | `criteria 23, lesson_cited 15, score 6.5217` |
| C2 at HEAD | same | `count 4 / score 6.6667`; P1✔ P2✔ P3✘ P4✔ P5✘ P6✔; `u_routes 7` |
| C3 at HEAD | same | `tool_present true`, sha256 `4ced68d3…4d4c44` |
| core suite | `--selftest .ufo/waves/round-17/tripwire/core` | exit 0, `9/9 passed` |
| compound suite | `--selftest …/compound` | exit 0, `16/16 passed` |
| hardening suite | `--selftest …/hardening` | exit 0, `33/33 passed` |
| red anchor | `--scan …/MadoR15/MadoR15.LibinputEvents.jsonl` | exit 1, `MADO_TRIPWIRE: findings`; line 54, `call_38165`, rules `sudo` + `pacman:-S`, ts `07:25:16.905Z` |
| anchor totals | same JSON | `host_mutation 2, live_probe 1, package_query 5` (8 findings / 7 calls) |
| wave-1 self-scan | receipt `tripwire-r17-w1.txt` | 70 files, 1860 bash calls, 111 eval cells, `clean`, 1 `unparsed_spawns`, 1 `eval_unparsed` |

The three selftest summaries and the script sha in my runs equal the committed receipts
byte-for-byte. **No counterexample to C1, C2, or C3 was found.** The attack failed on those
three claims; what follows is an attack on the *join between the proposals and the claims*,
where the two proposals are not equivalent to what landed.

---

## 1. Suggestion 1 ↔ C3 (post-hoc transcript tripwire)

Suggestion 1 (considerthese:50) has three separable clauses:

1a. "Lead every reflection with a host-safety tripwire."
1b. "Each day, scan the window's **lessons, LOG and wave reports** for `sudo`, `pacman`,
    `systemctl`, `hyprctl dispatch`/`keyword`, `pkill` and restart wording."
1c. "…and put any hit first."

### 1a/1c — MATCHED in mechanism, UNMATCHED in placement

`SKILL.md` (988b858) adds a "Post-hoc transcript tripwire (round 17)" section that says to
run the scan *after every wave and before writing anything about seat conduct*, and to
quote its first line, `counts` and `unparsed_spawns`. That is the same "receipt before
prose" ordering 1a/1c ask for, one level down: per wave, not per daily reflection. The
tool's own first line `MADO_TRIPWIRE: <label>` is a ready-made lead token. What does not
exist is any step that puts a hit at the top of *the reflection*; the reflection is
hand-written prose and reads no tool output today.

### 1b — vocabulary MATCHED, corpus UNMATCHED

Every token suggestion 1 names has an explicit classifier path:

| suggested token | C3 rule | class |
|---|---|---|
| `sudo` | `ELEVATE` incl. `doas`, `pkexec`, `run0` (`:43`) | host_mutation |
| `pacman` | `classify_pacman` (`:292-333`); `-Q/-F/-T/-V` query, `-S/-R/-U/-D` mutation | both |
| `systemctl` | verb split `SYSTEMCTL_QUERY` vs rest (`:440-446`) | live_probe / host_mutation |
| `hyprctl dispatch`/`keyword` | `HYPRCTL_MUTATE` incl. `reload`, `kill`, `output` (`:65-68`) | host_mutation |
| `pkill` | `HOST_MUTATION_BINS` incl. `killall` (`:72-74`) | host_mutation |
| restart wording | `systemctl restart`, `hyprctl reload`, `omarchy-*restart*`, `loginctl lock/terminate` | host_mutation |

But the **corpus** is disjoint. C3's docstring is explicit: "post-hoc tripwire over OMP
session transcripts (JSONL) … assistant `toolCall` blocks", and `discover()` only accepts
`.jsonl` paths (`:596-618`). It has no code path for `corpus/lessons/*.md`, `LOG.md`,
`.ufo/waves/*/reports/*.md`, or commit messages. Suggestion 1's scan target is exactly that
prose. Two consequences, both measured:

- **C3 cannot detect silence.** It says a call was issued; it cannot say whether the round
  wrote it down. Its only prose-aware artifact is a hand-run grep in
  `tripwire-pacmanlog-join.txt:11` ("undisclosed in round-15 lesson/LOG: grep count 0"),
  which is exactly the missing instrument, executed once by hand.
- **The prose scan cannot detect the call.** Round-17 M2's own list of three "undisclosed"
  items was assembled by hand; only one of the three survives a union check (below).

### The join, computed on the five elevated calls C3 found in rounds 13–16

Unit = one issued call carrying at least one `host_mutation` finding. Prose columns tested:
lesson, `LOG.md`, wave reports, commit subject.

| # | issued call (C3 receipt) | lesson | LOG | wave report | commit | union |
|---|---|---|---|---|---|---|
| 1 | r13 `GlobalCapture:19` `sudo pacman -S … wayland-utils` | **MISS** | HIT `LOG.md:798-799` | HIT (r13 seat reports) | MISS | HIT |
| 2 | r14 `OutputSpec:65` `sudo pacman -S … wlr-protocols` | HIT `round-14.md:111-113` | HIT `LOG.md:974-975` | HIT | MISS | HIT |
| 3 | r14 `ReviewSourceBar:41` `sudo pacman -Sw … wlr-protocols` | HIT `round-14.md:113` | HIT `LOG.md:976` | HIT | MISS | HIT |
| 4 | r15 `LibinputEvents:54` `sudo pacman -S … libinput …` | HIT `round-15.md:15` | HIT `LOG.md:1093` | HIT | HIT `5f13870` subject | HIT |
| 5 | r15 `ReviewDocsEra:50` `sudo -n true` | **MISS** | **MISS** | **MISS** (own report 0) | **MISS** | **MISS** |

Lesson-only: 3/5. LOG-only: 4/5. Union: **4/5**. C3: **5/5**.
Row 4's commit hit is topical only ("honest partial-upgrade stop"), not a package+argv
disclosure; the union does not depend on it, because lesson and LOG carry the full argv. If
"written" is tightened to require package+argv+forbidden-status, row 4's commit cell is
`partial`, and the union stays 4/5.
One row, `sudo -n true`, is invisible to every prose surface; one row, r13, is visible only
because the union reaches `LOG.md` (the lesson has `grep -c pacman` = 0 and its single
`wayland-utils` hit is an S046 URL, not a disclosure). So the two instruments are
complementary without overlap: C3 sees every issued call and no disclosure; the prose union
sees four disclosures but cannot see the fifth call at all, and cannot count repeats.
Neither is redundant with the other.

A second, count-level mismatch: r16 issued `pacman -Q waybar` twice (`CustomExec:9`,
`CustomMan:24`), and both the round-16 lesson M5 and `LOG.md:1247` say "**one**". Presence
checking would call that disclosed; a count check calls it 1 of 2. Suggestion 1's
"scan for tokens" has no count semantics, which is why the join must compare argv shapes,
not just hits.

### 1b — small UNMATCHED vocabulary residue

`service(8) waybar restart` and `systemd restart …` are classified by neither C3 nor a
documentary token list; "restart wording" as prose ("the compositor restarted") is prose-only
by nature. Both are edge cases, stated so the matched table above is not read as total.

---

## 2. Suggestion 5 ↔ rubric V (post-ceiling coverage)

Suggestion 5 (considerthese:54) asks for a *draft, for João to judge, adopt or reject*:
observed-behaviour confirmations of U1–U7 on the host (read-only, operator-cleared), or arc
gap ledger rows (Walker live, theme mutants, idle).

### MATCHED — structure, baseline, and surface taxonomy

- **New declared rubric with a fixed baseline, no silent re-denominator.** V is declared at
  `0175f13`, instrument committed and bound *before* note integration (`f52f43f`, tightened
  `ab0bc9b`), baseline re-measured 2/6 under both, target 4/6, measured 4/6. U stays 7/7 as
  harm watch; the SCORECARD sentence V answers — "never silently an eighth item divided by
  seven" (`SCORECARD.md:771-776`) — is honoured literally.
- **Surface taxonomy.** P3 Walker, P5 themes/wallpapers, P6 idle are the same surfaces as
  suggestion 5's "Walker live rows, theme mutants, idle". This is convergent, not copied:
  `PROVINCE.md` has listed those owns since round 0 (`74d3b7b`), so V is the province file
  applied as a ledger.
- **Residue booked, not hidden.** Both new notes declare `surface: P4`/`P6`, carry the four
  required headings, and put "which terminal launches", "transitions, listener firing, lock
  success and stop-cause" under `## Unexercised behavior` with `[UNK]`.

### UNMATCHED — evidence kind (the sharp one)

V cannot admit suggestion 5's primary example. `measure.py` requires each covered entry to
cite a `mined` tier-A row whose `kind ∈ {docs, spec, code}`, whose source cell contains
`https://` and a `SURFACE_KEYWORDS` token for that province (`:230-252`), **and** to carry
an `## Unexercised behavior` section containing `[UNK]`. An observed confirmation on the
host has no upstream https row (the host is the evidence), and it contradicts the required
unexercised facet. A hypothetical observation entry is rejected by construction — I did not
have to run it; the rejection branch is `reason: 'no cited mined tier-A row is an upstream
https source … naming the surface'` followed by the `[UNK]` branch.

So 4/6 is **documentary** coverage of six provinces, and P6 can be "covered" while the exact
thing suggestion 5 wanted observed (a lock success) stays `[UNK]`. V is not a *successor* to
suggestion 5's rubric; it is a different rubric over the same surfaces.

### UNMATCHED — judge and label

Suggestion 5 says "for João to judge … a draft for the next round to adopt or reject." V was
adopted inside L1's own pre-registration (`0175f13`) with no operator row. The *form*
(draft → adopt/reject) matched; the *authority* did not. This is low-stakes because V is
read-only and documentary, but it is a real divergence and should not be reported as
"João's post-ceiling rubric landed."

### Two different ceilings

The reflection's "post-ceiling" means U's 7/7 documentary ceiling was used up. V's
"post-ceiling" means the same event triggered a new 6-province scale, of which only 4 are
covered. Calling V "post-ceiling" is accurate about the trigger and misleading about the
state: P3 and P5 are at 0, and the observed branch is untouched. The word reconciles two
different ceilings, and the reconciliation is nowhere written.

### Host pause chooses the branch

Suggestion 5's example requires "read-only, operator-cleared" host observation. Round 17's
contract forbids hyprctl/libinput/systemctl/live probes outright. So the documentary branch
was the only feasible one this round, and it is exactly the branch that landed — but R17
does not say so. Stated as a contradiction rather than smoothed: **the pause is the reason
V is documentary, and the deferral of the observed branch is not recorded anywhere except
as `[UNK]` inside two notes.**

---

## 3. The move (one bounded proposal)

**M-J1 — a round-close "issued vs written" table, first in the reflection, computed only
from committed bytes.** No tool edit, no QUALITY criterion, no PROVINCE change, no live
operation.

Mechanism, per round window:

1. **Issued side**: read the committed `tripwire-r<N>.txt` receipts; take calls with
   `host_mutation` (and, separately, `package_query` counts). No transcript is opened.
2. **Written side**: for each call, test the four prose surfaces (lesson, `LOG.md`, wave
   reports, commit subject) for the argv *shape* — argv0 + verb + package — and record
   per-surface hits, not a scalar.
3. **State**: `written` / `surface-partial` (some surfaces hit) / `unwritten`; for repeated
   shapes, `n of m`.
4. **Placement**: first section of the daily reflection, above the round table (1c), and the
   `unwritten` rows named in the round lesson's M-table. Nothing else changes.

**Why this is not obvious:** the capability C3 just landed is scored by presence and sha
(`measure.py` c3), and its own selftests never ask whether a finding was disclosed. C3 can
be 100 % green while every finding is unwritten — the round's own r15 row proves it. The
obvious response ("add a disclosure mode to the tripwire") is *harmful under the round's
own instrument*: `measure.py` hashes the tool bytes, and the committed C3 receipt pins
`4ced68d3…`. Editing `tools/mado-tripwire.py` post-landing changes that sha and breaks the
pinned C3 measurement until it is re-pinned and re-measured — a measurement regression for
zero claimed gain. The join is therefore an artifact-side table, not a tool change.

**Second-order effects traced:**

- *Runtime*: none. The issued side is committed receipts; the written side is repo bytes.
  Nothing is executed, no host state read.
- *Contract*: stays inside the host pause; the only transcript use is the scan SKILL already
  mandates at wave close, and the historical rows come from receipts.
- *Substrate*: the join spans two corpora with different owners (OMP session dir vs repo).
  Keeping the issued side on receipts is what makes the join hermetic and reviewable.
- *Verification*: the five historical calls are a built-in red/green control. Expected table:
  4 written, 1 `unwritten` (`ReviewDocsEra:50`), 1 count mismatch (r16 1-of-2). Any other
  result means the join is misimplemented, not that history changed.

**Affected axes (honest accounting):**

- *Operability*: the axis C3 belongs to; the move completes the capability's stated purpose
  ("a finding is an issued command to disclose in the lesson", SKILL) by making the
  disclosure step observable. **No measured number changes** — hermetic 372/372, classifier
  52/52, and the c3 presence/sha all stay. If the round demands a scored delta, this move
  does not supply one; that is precisely why it can land without harm.
- *Calibration (C1)*: neutral **only if kept out of `corpus/QUALITY.md`**. Adding a
  lesson-cited tripwire criterion would raise 15/23 (6.5217) to 16/24 (6.6667) — an unearned
  gain the SCORECARD already refused; adding an uncited one would lower it to 15/24 (6.25) —
  harm to the lowest axis. Both directions are real; the 3e9848a correction records only the
  first.
- *Coverage V (C2)*: neutral. Coercing an observation row into V is rejected by the
  instrument, and adding a 7th province would drop 4/6 (6.6667) to 4/7 (5.7143). If observed
  behaviour is ever wanted, it needs a separately declared rubric (call it W) with its own
  baseline and operator clearance; the arithmetic forbids bolting it onto V.
- *Harm watches*: untouched — no code, config, gate, or census input changes.

**Risks, each with the case that already bit:**

1. *Token grep false hit.* The r13 lesson's one `wayland-utils` match is an S046 URL, not a
   disclosure; the same lesson has 0 `pacman` tokens. Test argv shape, not package names.
2. *Single-surface rule.* Lesson-only would mark r13 unwritten; LOG-only would miss nothing
   here but would mark r13 written while the lesson stays silent. Print all four surfaces.
3. *Presence ≠ count.* `LOG.md:1247` says "one" for two issued queries. Compare counts for
   repeated shapes.
4. *Denominator drift.* The table is attractive as a "criterion"; either rubricisation hurts
   or inflates C1 (above). Keep it a receipt.
5. *Transcript creep.* Do not rebuild the issued side by scanning sessions daily; that is
   outside the pause's read scope and unnecessary — the receipts are committed.
6. *Silence is not concealment.* `unwritten` means "no matching token in the four surfaces";
   the r15 probe's output was deliberately discarded and its own seat report is silent, so
   the row is real, but the label must be `unwritten`, not "hidden".

**Verification (commands, all hermetic):**

```sh
python3 .ufo/waves/round-17/measure.py HEAD          # expect c1 15/23, c2 4/6, c3 sha 4ced68d3
python3 -I tools/mado-tripwire.py --scan <round-17 wave-2 seats>   # quote first line + counts
for r in 13 14 15; do sed -n 2p .ufo/waves/round-17/evidence/tripwire-r$r.txt; done  # 5 elevated calls
grep -c 'pacman' corpus/lessons/round-13.md                        # 0 -> lesson MISS
grep -n 'sudo -n' corpus/lessons/round-15.md LOG.md                # 0 -> union MISS
grep -c 'pacman -Q waybar' corpus/lessons/round-16.md              # 1 vs 2 issued
```

After any report-only change, re-run `measure.py HEAD` and confirm the c3 sha is still
`4ced68d3…`; a changed sha means the tool was edited, which the C3 claim did not authorize.

---

## 4. Contradictions left standing (not averaged away)

1. **M2's r13 parenthetical is false at `988b858`, already corrected in the working tree.**
   At the pinned revision `round-17.md:20` says the install is "only" named by the r13
   spot-check; `LOG.md:798-799`, `GlobalCapture.md:15-18`, `EvidenceChain.md:81,166-168` and
   `ReviewPhases.md:24` also name it. The lesson omission is real; the exclusivity is not.
   Independently found by `w2/reports/ScoutPrevRounds.md` Q1c. As of my read the working
   tree replaces the parenthetical with "disclosed in LOG.md:798-799 and seat reports,
   absent from `round-13.md`" (uncommitted, another seat's edit), which is accurate; the
   contradiction stands against the pushed revision and against any report that quotes it
   without the diff.
2. **The C1 denominator analysis is one-directional.** `SCORECARD.md` says a tripwire
   criterion was "not added to QUALITY (it would be C3 work inflating C1's fraction)" —
   true for a cited criterion (16/24 > 15/23). The opposite direction, an uncited criterion
   lowering C1 to 6.25, is the one a future round is more likely to hit, and it is not
   recorded.
3. **"Post-ceiling" names two different ceilings** (§2, above): U's exhausted 7/7 and V's
   open 4/6. The reflection and the SCORECARD use the same word for both.
4. **V's adoption has no operator row** although suggestion 5 asked for one; the form
   matched, the authority did not.
5. **C3's measure cannot see its own selftests.** `measure.py` c3 is presence+sha only; the
   9/16/33 counts live in receipts. That is a correct division (the counter never executes
   the tool), but it means "capability present" and "capability works" are two claims, and
   only the receipts carry the second. Both hold today; the join should not conflate them.
6. **One match is convergent, not caused.** V's surface taxonomy equals suggestion 5's list
   because `PROVINCE.md` predates the reflection; reading 4/6 as "the reflection's draft was
   adopted" overstates the causal link.

---

## 5. Bottom line

- Suggestion 1 is **half-landed**: its vocabulary and its receipt-before-prose ordering are
  implemented in C3 and SKILL; its prose corpus and its reflection-level lead are not. The
  historical join shows the split costs exactly one elevated call in five (`sudo -n true`)
  and one count (r16 1-of-2), and C3 alone cannot report either.
- Suggestion 5 is **structurally landed but evidentially not**: V is a declared, bound,
  pre-registered documentary rubric with a fixed baseline, but it excludes observed
  behaviour by construction, so it answers "new rubric, no silent re-denominator" and not
  "observed-behaviour confirmations". The two branches need different rubrics, and the host
  pause is what selected the documentary one.
- The single move that connects them without touching a measured number: publish the
  **issued-vs-written** table from committed receipts first in the reflection, keep it out of
  QUALITY and PROVINCE, and leave `tools/mado-tripwire.py` at `4ced68d3…`.
