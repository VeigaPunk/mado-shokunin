# Lessons — mado, round 39

Round intent (frozen in `.ufo/waves/round-39/registration.md`, freeze commit
`457d1b125932c1e0d797061a2156b917bcd7edaa`, base `08be4eb7fd13358ed29b096e8924005d46ac409c`):
three claims — **C1** (re-registration of the repaired round-38 discrimination
pair: re-frozen manifest `.ufo/waves/round-39/c1/manifest.json` + unchanged
counters `c1-r38-event-ground.py`/`c2-r38-eventq.py` must score
`controls=19 correct=19/19 verdict=TARGET_MET` at the freeze commit), **C2**
(operability/capability acquisition: `tools/mado-options.py` + counter
`quality/counters/c3-r39-options.py`), **C3** (coverage/sourced:
`corpus/knowledge/config-option-table-r39.md` + SOURCES rows S218/S219 + counter
`quality/counters/c4-r39-options-entry.py`).

## Gate

Candidates considered this round: the three new admitted rows (S218, S219,
S220) and the four package entries that stay refused from round 38 (their
refusal reasons are unchanged and re-recorded below).

Refused package entries (stay refused — same grounds as round-38 lesson `:40-43`,
re-opened and agreed by the round-38 verifier spot-check `:50`):

| Staged id | Refusal reason (stay refused) |
| --- | --- |
| event-queue-host-measurement-r28.md | "never overflowed" leans on a null channel (`debug:disable_logs=1`); corrected by round-37's `event-queue-observability-r37.md` |
| event-queue-journal-measurement-r29.md | same null channel; its journal reading (21 core-logger lines, zero markers) is observability-r37.md's measurement |
| socket-client-contract-measurements-r29.md | "requests capped at 64 KiB" is chonkstep's own request cap (S277 `:61`), not upstream's follow-queue bound; its socket census is superseded by S258's stat and round-37's live census |
| socket-modes-and-request-read-r30.md | frozen registration declines the package's successor chain; the request-socket facts are covered by the adopted S158/S187/S253 entries |

Admitted rows (access date 2026-10-25 for all three; every new-row quote ≤25 words and located):

```
GATE S218 receipt=.ufo/waves/round-39/w1/ExecAssimFetches/S218.bin sha256=400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801 quote="You are allowed multiple hl.config() invocations, each one will update just what you pass into it."
GATE S219 receipt=tools/mado-options.py@data-tip sha256=9787b53b298216aee93ec1193814e2972d9fef9125656ce9ed0bd03ed7fbcf59 quote="mado-options.py - static resolver of the config-tree option table."
GATE S220 receipt=.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin sha256=f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2 quote="Their purpose is to be fed into hl.bind() or hl.dispatch()."
```

Row facts:

- S218 — Hyprland configuration/hyprlang option-syntax documentation (Variables
  page, 0.56.0) — `https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/`
  — opened 2026-10-25 — quote located at §Syntax, first prose paragraph after the
  `hl.config ({ category = { value = ... } })` syntax example (page revision
  "Last updated on July 17, 2026"). Grounds the last-declarer option-syntax
  claim: repeated `hl.config()` invocations merge, each updating only what is
  passed.
- S219 — own-work row for the options tool (`tools/mado-options.py`) — no URL
  (own-work); receipt is the tool bytes committed at the data tip (worktree
  sha256 at draft finalization `cee78d99…9ce61e`). Quote is the tool's docstring first
  line (`tools/mado-options.py:2`).
- S220 — 0.56.0 Dispatchers page —
  `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/` — opened
  2026-10-25 — quote located in the opening section (`#dispatchers`), page
  revision "Last updated on July 15, 2026". Cited by the round-39 amendment to
  `dispatcher-surface-and-request-grammar-r26.md`.

### Spot-check results

| row | receipt sha256 | quote words | verbatim in receipt | note |
| --- | --- | --- | --- | --- |
| S218 | `400d1819…2801` (sha256sum of S218.bin) | 16 | rendered-verbatim | the sentence is contiguous in the rendered text; the raw HTML carries `<code>hl.config()</code>` inline tags |
| S219 | `cee78d99…9ce61e` (sha256sum of worktree `tools/mado-options.py` at draft finalization) | 9 | verbatim at `tools/mado-options.py:2` | receipt not yet committed; the tool file changed after the first draft hash (`9787b53b…` → `cee78d99…`); the data commit must bind the final bytes (re-hash at data tip: `git show <data-tip>:tools/mado-options.py | sha256sum`) |
| S220 | `f9b51362…6e2` (sha256sum of S220.bin) | 10 | rendered-verbatim | raw HTML carries `<code>hl.bind()</code>`/`<code>hl.dispatch()</code>` inline tags; the fully bytes-verbatim alternative "Dispatchers return tables that describe an action you want to make." (11 words) is also present at raw offset 262669; S220 duplicates S196's URL → one added W04 duplicate-URL warning expected, census still exit 0 |

Quote floor honored: all new-row quotes ≤25 words (16/9/10). All quotes are
located (row/§ anchor or file line).

C1 spot-check (measured, not inferred):

- Red-before (frozen pair, base): `receipts/c1-redbefore.txt` →
  `controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1; sole failure
  `c1-duprow` (`expected=TARGET_MISSED observed=TARGET_MET`).
- After at freeze commit and at tip: `ExecC1After/after-freeze.txt`,
  `after-tip.txt` → `controls=19 correct=19/19 verdict=TARGET_MET`, exit 0
  (both 1672 B, identical; freeze == tip `457d1b1`). Manifest byte-copy: sha256
  `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`, `cmp`
  exit 0 vs `.ufo/waves/round-38/controls/manifest.json` at base.

## Assimilation (touched-row record)

The adoption amendment (`ScrDispatcherAmendment/dispatcher-amendment-section.md`)
re-opens S018 (`HyprCtl.cpp@efb5099`, held receipt
`.ufo/waves/round-24/fetch/S158.bin`, sha256 `798b7c6c…`) and S220, and is
appended as a dated section to the held
`corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` (held text
untouched). Staged register stays unassimilated; only cited rows are appended.

Status / recheck / used-by changes old→new for rows touched this round:

| row | status old→new | recheck old→new | used-by old→new |
| --- | --- | --- | --- |
| S218 | none → mined | none → on-release | none → `corpus/knowledge/config-option-table-r39.md` |
| S219 | none → mined (own-work) | none → on-release | none → `corpus/knowledge/config-option-table-r39.md` |
| S220 | none → mined | none → on-release | none → `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` |
| S018 | mined → mined (unchanged) | on-release → on-release (unchanged) | `corpus/knowledge/window-rule-effects-getprop.md` → + `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` |

## Mistakes

| class | evidence pointer | captured-by | fix (red-before shown) |
| --- | --- | --- | --- |
| Closure / worktree hygiene (inherited-dirty closure) | round-38 verifier spot-check defect row: working tree carried 3 modified seat reports at closure — `.ufo/waves/round-38/w1/reports/{RevEntryBound,RevRegistry,ScoutS253}.md`, +187/−7 (round-38-verifier-spotcheck.md `:17`); routed in registration §Routed-defects item 4 | spot-check flagged at closure; registration item 4 named them; freeze commit `457d1b1` folded them in | committed in the round-39 freeze commit and named in this round's report. Red-before: at base `08be4eb` the reports' final bytes were not in any commit (worktree-only); `git show 457d1b1 --stat` folds +53/+8/+133, −7 under the freeze |
| Reporting (refuted addendum-5 refinement) | fleet round-38 report addendum 5 (`9386c91f`, 11:26:06) repeated RevCensusBefore's "frozen pair 19/19 at freeze rev" refinement (RevCensusBefore.md `:110`) | lane errata `c46f868` (11:35:43 dispute record between RevFrozenClaims and RevCensusBefore — closure adjudicates) and `f551b70` (12:25:59 freeze-pair resolution: frozen counter × frozen manifest = 18/19; `859d0cf` verdict no-op) | this round's report carries an erratum naming the superseded text; C1 re-registration measures the true pair. Red-before: `receipts/c1-redbefore.txt` → `controls=19 correct=18/19 verdict=TARGET_MISSED` (exit 1), sole failure `c1-duprow` |
