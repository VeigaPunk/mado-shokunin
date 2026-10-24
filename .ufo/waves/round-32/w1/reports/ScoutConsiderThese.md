# ScoutConsiderThese — `considerthese/2026-10-23.md` proposals 1–7: implemented/unimplemented audit + one grounded recommendation

Leaf scout report. Read-only over the lane; this file is the only write. No commits, no delegation, no host/package/service/compositor operation. Reflection file read only (never edited). Access date for all opens: **2026-10-24**.

Inputs actually read: `considerthese/2026-10-23.md` (full), `considerthese/2026-10-24.md` (full — the decisive evidence: whether each proposal practice was adopted the next day), `corpus/SOURCES.md` rows S153–S184, `corpus/QUALITY.md` criteria 27/36–54, `corpus/README.md` index rows :51–54, `corpus/lessons/round-26.md` §Gate + errata, `corpus/lessons/round-26-verifier-spotcheck.md` M26-9/M26-10 rulings, `SCORECARD.md` current-state ledgers, `.ufo/waves/round-17/w1/reports/ConsiderTheseJoin.md` + `w2/reports/ConnectConsiderThese.md` (prior considerthese disposition), one `curl` fetch of the S177 pinned URL.

## 0. Precedent that binds the verdicts

`considerthese` is a reflection file, not operator teaching — established by the round-17 connector seat (`.ufo/waves/round-17/w1/reports/ConsiderTheseJoin.md:13-17`: "operator-identity commits of a reflection, not a teaching body"; `LEARNING.md` operator-lesson slot is empty). Its proposals can be *adopted* (same practice observed in a later file) or *implemented in the lane* (a corpus artifact carries it). I judge both.

## 1. Per-proposal table

| # | Proposal | Verdict | Evidence (what I found) |
|---|---|---|---|
| 1 | Flag host-impact events to João the same day; top of message, separate from capability news | **PARTIALLY adopted** | `2026-10-24.md:5` bottom line carries "Host safety held: Hyprland coredumps stayed at 1338 on every oracle receipt" — surfaced early but inline, not a separate lead block. Prior form: 2026-10-20 S1 twin was judged "adjacent, not adopted" (`w1/reports/ConsiderTheseJoin.md:48`; `w2/reports/ConnectConsiderThese.md:52-67,318-321`: the tripwire implements receipt-before-prose per wave, but "what does not exist is any step that puts a hit at the top of *the reflection*"). Corpus: host-safety is already receipt-level (66 `HOST_SAFETY delta=0` hits, round-26 spotcheck §2.3); the reflection-level scan habit itself has no corpus artifact. |
| 2 | Track admission streaks and pivots, not just rounds | **IMPLEMENTED** (adopted by the author) | `2026-10-24.md:5` bottom line is exactly the pivot/streak line: "one real desktop capability landed … then the lane spent rounds 28–31 hardening its own counters"; debt table :37 adds the running line "Domain drift — No `tools/` or `corpus/knowledge/` change since round 27". Corpus-side precedent: 2026-10-20 S3 (metrics trend line) was judged "open" then (`ConsiderTheseJoin.md:50`); SCORECARD records per-round verdicts, not streaks, so the streak signal lives only in the reflection — and now does. |
| 3 | Re-open one cited line from a landed tool's public pin, read-only (e.g. S177) | **UNIMPLEMENTED — recommended, grounded below** | `2026-10-24.md:50` re-proposes it verbatim as proposal 5: "Verify one cited fact first-hand per day, read-only … so each reflection has at least one claim I checked myself rather than relayed" — self-declared not acted on. No corpus lesson records a daily first-hand re-open outside a round's own Gate. |
| 4 | Watch for "trade" rulings; keep a short accepted-trades list; check routed fixes landed | **PARTIALLY adopted** | `2026-10-24.md:48` — the author did the follow-up once ("Yesterday I flagged M26-10; today I could confirm it landed at `b6650d5`") but kept the *standing list* as a new proposal ("I should keep a short carried list"). The trade itself: M26-10 ruled "a disclosed trade inside the tool's scope, not an axis harm" (`round-26-verifier-spotcheck.md:107`), routed fix landed — `SCORECARD.md:1807` carries the `b6650d5` environment-limit paragraph; commit `b6650d583924d670c9e98594ffb1c6f25e8e7682` exists, author `mado-shokunin`, 2026-10-23T07:38:49-03:00 (verified `git show --stat`). |
| 5 | Read in-progress rounds at the registration level | **UNIMPLEMENTED** | `2026-10-24.md:3` still describes the method as re-reading "the lane's own receipts as re-checked in the hyaku non-author spot-checks"; no `registration.md` content of the in-flight round (32) is quoted or analyzed. Corpus has registration content only as round evidence, e.g. `SCORECARD.md:1752` quotes round-27's registration *after* closure — post-hoc, not mid-flight. |
| 6 | Handle commit-list caps explicitly (page fully or note the cap) | **UNIMPLEMENTED** | `2026-10-24.md:3` gives an exact count "42 commits after `0a9ea77`" with no cap note; today's window is below the 100-commit cap so nothing exercised it — the *habit* (note the cap / page through) is absent. No corpus hit for cap/pagination practice on commit lists. |
| 7 | Offer operator-actionable "what your config resolves to" note | **UNIMPLEMENTED; not lane-bar implementable alone** | The capability exists — round-26 closure ran both resolvers on the operator's config tree vs live `hyprctl` (`round-26-verifier-spotcheck.md:11`). But the proposal's own text says "With his OK" — it requires an operator act, same class as 2026-10-20 S6 which the r17 join ruled "operator-gated" (`ConsiderTheseJoin.md:96`). |

## 2. Recommendation: proposal 3 — first-hand re-open of a pinned source line, executed here

### S177 registry status (the prompt's caveat, resolved)

S177 **is** in this lane's registry — `corpus/SOURCES.md:189`:

> `| S177 | hyprutils v0.14.2 animation config tree — https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp | code | A | … | src/animation/AnimationConfig.cpp:9-70 @ tag v0.14.2, sha256:dbb5d50a27f80ea947db92050af40ee87e0e9e0718add0520cbc96e32abe268e, 2354 B | … | mined | 2026-10-23 | on-release | corpus/knowledge/animation-table-r26.md |`

Nearest neighbors if it had been absent: S176 (AnimationTree.cpp, row :188) and S178 (workspace-rules wiki, row :190) — same pin discipline.

### What I opened (first-hand, this session)

- Command: `curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp`
- Fetched body: **2354 bytes, sha256 `dbb5d50a27f80ea947db92050af40ee87e0e9e0718add0520cbc96e32abe268e`** — byte-identical to the S177 anchor (both digest and size match).
- Located line — `src/animation/AnimationConfig.cpp:63-64`, verbatim:

  ```cpp
  63:        if (anim->pParentAnimation == PANIM && !anim->overridden) {
  64:            // if a child isnt overridden, set the values of the parent
  ```

- Matches the round-26 Gate quote (`corpus/lessons/round-26.md:44`: "if a child isnt overridden, set the values of the parent" at `:63-64`) and the reflection's paraphrase (`2026-10-23.md:24`). Anchor honest: line numbers, comment text, file size, tag `v0.14.2` all reproduce. Nothing drifts; S177 stays `mined`, no erratum needed.

**Why this one:** it is the only proposal that is (a) still unimplemented, (b) executable read-only through the lane's own bar with no operator gate and no host contact, and (c) already partially institutionalized — round-13/18/26 lessons record per-round source re-opens by a non-author seat in a `## Gate` table; what's missing is the *carried* habit, not the mechanism. P1/P4 are partially adopted and are reflection-process (no corpus landing slot — the r17 join rules the reflection must not be cited as authority and kept out of QUALITY/PROVINCE). P5/P6 are likewise reflection-process. P7 is operator-gated.

### Landing form: a lesson (a `## Gate` "source re-open" row), not a QUALITY criterion and not a SOURCES row

- **Not a SOURCES row:** the re-open produced no new source; the registry contract permits only `status`/`recheck`/`used-by` to change in place and none of those moved (recheck cadence `on-release` unchanged). A duplicate row for the same URL is a W04 violation (precedent: S030/S045 rejected duplicates).
- **Not a QUALITY criterion:** the bar governs claim admission; a daily-reflection habit is not an admission rule, and `ConsiderTheseJoin.md:21-25` rules the reflection is a lead, never authority.
- **Yes a lesson:** the lane's existing convention for recording a verified source re-open is the `## Gate` "Sources opened / re-opened" table in the round's own lesson file — `corpus/lessons/round-26.md:36-44` (columns: id, URL, verbatim ≤25-word quote, decision). The equivalent entry for this re-open lands in the current round's lesson at `corpus/lessons/round-32.md` (does not exist yet; latest landed lesson is `round-30.md` — `round-31.md` was never filed, only its spot-check exists). Suggested row text:

  `| S177 (re-open, reflection proposal) | https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp | "if a child isnt overridden, set the values of the parent" (:63-64) | agree — sha256 dbb5d50a… 2354 B = row anchor, accessed 2026-10-24 |`

  If the recurring *daily* habit (rather than this single re-open) is what a round wants to bind, the honest bar-compatible form is a mistake table entry in that same lesson noting a reflection-level claim that went unchecked — not a numbered criterion.

## 3. Limits

- Proposals 1, 5, 6 judge *practice*, which only the reflection files show; a 2026-10-25 file could falsify P5/P6 verdicts.
- P1's "partially" is a judgment call: the host-safety line sits in the bottom line but is not structurally separate from capability news.
- I did not re-run any lane counter, gate, or oracle; all receipts cited are committed bytes.
