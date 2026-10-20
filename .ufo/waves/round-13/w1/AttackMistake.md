# AttackMistake — critic review of the source-collision QUALITY criterion (round 13, w1)

Seat: `MadoR13.AttackMistake` (critic, leaf). Date: 2026-10-20. I attacked the approach, not its author.
Target: the MistakeFix assignment as written in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/spec.json`: "reject duplicate URL+overlapping scope without supersedes, distinguish historical rejected rows", plus a QUALITY criterion grounded in a lesson.
State at review time: no `MistakeFix.md` or `MistakeFix.py` existed under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/` (glob, 2026-10-20). This review therefore attacks the specified design and the fleet census it extends. It sets the fixtures any draft must pass. I sent the key points to MistakeFix (and the supersedes point to GlobalDocs) by peer message.

Axes I named: **coverage** (C1: U4 rows such as the planned S042 `supersedes S006`) and **operability** (C2: checks stay valid and discriminate red from green).
Evidence class: local repository reads only. I opened no external source and made no source rows, so no URL/quote/tier block applies. No tools were installed or upgraded.
Replica method: [OBS] I ran a Python replica of `sources-census.sh` `url_of` plus the E04/W04 logic (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:600-605,643-654`) over `git show <rev>:corpus/SOURCES.md`. The replica is analysis, not the census itself. L1 should confirm the real census at the end (see the check list).

---

## Counterexample 1 — the existing census can't tell the incident from its fix (operability, blocking)

- **Evidence.** Replica results:
  - `5174e15`: S030 `mined`. Output `W04 S030 wiki.hypr.land/Configuring/Basics/Window-Rules`, no E04.
  - `8dbfc93` and `HEAD`: S030 `rejected`. Output identical.
  - This matches the retained real-census result in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/EvidenceLedger.md:40,44`: W04 S030, exit 0.
- **Cause.** E04 keys on the exact scope string (`scope_key=u SUBSEP scope`, `sources-census.sh:643`). The two scopes differ:
  - S030: "Current Lua window-rule syntax" (`corpus/SOURCES.md:41`)
  - S017: "Current latest-git Lua-era syntax and documented effect semantics, scoped to that wiki era" (`:28`)
- **Consequence.** A check that copies the census definition of "duplicate" (same URL and same scope text) would have admitted S030 again. The duplicate the orchestrator disagreed with (`corpus/lessons/round-12.md:116`) is invisible to exact-scope keying. Overlapping scopes can't be decided from free-text strings.
- **Smallest safe correction.**
  - Key collisions on the normalized URL among non-rejected rows only.
  - The selftest must include a **red-before/green-after pair built from real history**:
    - S017 + S030 exactly as at `5174e15` (both `mined`) must FAIL and name the pair `S017,S030`.
    - The same pair as at `HEAD` (S030 `rejected`) must PASS.
  - Without this pair, the criterion counts as a description, not a prevention.

## Counterexample 2 — permanent false positive on the historical rejected row S030 (operability)

- **Evidence.**
  - S030 is `rejected` (`corpus/SOURCES.md:41`). Its `teaches` still reads "Provides a current Lua example…", not `REJECTED: …; flip: …`.
  - Only `status`, `recheck` and `used-by` may change in place (`corpus/SOURCES.md:6`; `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49-51`).
  - The rejection reason is kept outside the row, at `corpus/SOURCES.md:91` and `corpus/lessons/round-12.md:122`.
  - The fleet census already raises a non-failing W04 on S030 forever, because W04 ignores status (`sources-census.sh:644-645`).
- **Failure modes.**
  - A check that flags every repeated URL, ignoring status, stays red with no allowed fix. The only "fix" would be editing an immutable cell: a historical-cell mutation.
  - A rejected-row format check that requires the `REJECTED:` prefix flags S030 for the same reason.
  - `EvidenceLedger.md:80` already leaves "whether that is a pass or fail" open. That invites someone to "fix" S030.
- **Smallest safe correction.**
  - A `rejected` row is never the erroring side of a collision.
  - The prefix requirement applies only to rows rejected when written. Rows rejected in place are satisfied by a logged pointer: a lesson post-review row with old→new status.
  - Treat the W04 on S030 as a known historical warning, not a C2 failure.

## Counterexample 3 — supersedes is accepted unbound and anywhere in the text (operability; would let a duplicate through)

- **Evidence.** The census skips E04 when `teaches !~ /supersedes S[0-9]{3}/` fails (`sources-census.sh:648`). Replica cases:
  - **CE1:** a new row on S017's URL and exact scope with `teaches` "supersedes S005 — …" (an unrelated row) produces no E04.
  - **CE2:** `teaches` "unlike what supersedes S017 implies, …" produces no E04.
  - **Rule text:** the contract requires `teaches` to **open** with `supersedes S0NN —` (`SOURCES-CONTRACT-v1.md:50-51`).
  - **Ids of four or more digits:** `S[0-9]{3}` matches a prefix of a longer id.
- **Smallest safe correction.**
  - Accept supersedes only via the anchored pattern `^supersedes (S[0-9]{3,}) —`.
  - The captured id must be one of the earlier rows that share the normalized URL.
  - Anything else counts as no supersedes.

## Counterexample 4 — explicit supersedes must not be flagged; the round-12 deferral rested on a false premise (coverage)

- **Evidence.**
  - `corpus/SOURCES.md:92` defers the owed anchors (S006/S008/S009/S010). Its reason: a superseding row on the same URL "reads as a duplicate to the fleet census (E04/W04) until the supersedes link is recognised".
  - The census already recognises the link for E04 (`sources-census.sh:646-649`).
  - W04 fires only when the scope text differs, and it is non-failing (selftest `W04-does-not-fail-validation`, `sources-census.sh:364-365`).
- **Consequence.**
  - The deferral reason is false, so the owed-anchor work this round (S042 `supersedes S006`, the C1 path) was never blocked by the census.
  - A new lane check that flagged S042 → S006 would make the premise true after the fact, and would block C1.
- **Smallest safe correction.**
  - Required selftest fixture: S006 queued, then S042 on `https://wayland.freedesktop.org/extras.html` whose `teaches` opens `supersedes S006 —`. It must PASS with zero errors, whether or not the scope text is identical.
  - Append a round-13 lesson erratum correcting the `:92` rationale. `:92` itself stays untouched (append-only).

## Counterexample 5 — the S030 flip must stay reachable without false provenance (coverage, tradeoff)

- **Evidence.** S030's flip reads "a distinct anchor at a pinned revision not covered by S017" (`corpus/lessons/round-12.md:122`). A row that meets that flip shares S017's URL, because URL fragments are stripped (`sources-census.sh:602`), yet it supersedes nothing.
- **Failure mode.** A hard rule of "same URL ⇒ must supersede" leaves the author two options, both false provenance:
  - `supersedes S017`, which wrongly retires a valid mined row;
  - `supersedes S030`, which "supersedes" a rejection.
- **Smallest safe correction.** Compare anchor section tokens: `#fragment` or a quoted heading, case-insensitive.
  - Overlapping or unparseable sections → FAIL. At `5174e15`, S030's “Syntax” overlaps S017's `#syntax`, so it still fails.
  - Disjoint sections → named WARN for human review, recorded in the lesson's `## Gate`.
  - This is a tradeoff the judge must accept knowingly: fail-closed by default, with an explicit way out.

## Counterexample 6 — a rejected-first re-entry without a link brings back the duplicate authority (operability, tradeoff)

- **Evidence.**
  - The census suppresses E04 when every earlier same-key row is rejected (`url_scope_nonrejected`, `sources-census.sh:647,653`). Fixture S031 (rejected) followed by S032 (queued) is expected `ok` (`:374-381`).
  - Replica CE3: a queued row on S012's URL with no link produces no E04.
  - The registry then holds two contradictory verdicts on one page with no link. That is the S030 class (two rows, one page, no link), just reversed.
- **Smallest safe correction (lane-local; the fleet stays unchanged).** A non-rejected row that collides only with rejected rows gets a named WARN unless its `teaches` opens `supersedes <rejected id> —`. That records the flip as a correction (contract rule 2) without turning rejected rows into blockers.

## Counterexample 7 — the lesson's prevention is a merge step, but the specified script checks the merged table (operability)

- **Evidence.**
  - Root cause: "the merge renumbered five seat fragments without a cross-fragment URL check … next merge runs a URL-duplicate pass before renumbering" (`corpus/lessons/round-12.md:116`).
  - The step that renumbers is round-12 plan step 3 (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/plans/round-12.plan.md:55`).
  - Nothing runs a sources check today: `grep -nE 'SOURCES|sources-census' tools/mado-verify.sh` printed nothing (2026-10-20).
  - The script is specified as "isolated", run only by L1.
  - Fragments carry placeholder or ART ids (`corpus/SOURCES.md:90`), so a check keyed on ids after renumbering can't name the seats that collided.
- **Smallest safe correction.**
  - The script accepts one or more fragment files, or the merged registry, and reports collisions with each row's origin file.
  - The QUALITY criterion names the trigger: "before renumbering source fragments, and before committing `corpus/SOURCES.md`".
  - The lesson records the red-at-`5174e15` / green-at-`HEAD` receipt as the evidence of prevention.

## Counterexample 8 — row quantity is being used as a quality signal (coverage, Goodhart)

- **Evidence.**
  - The contract says there is "no row quota" (`SOURCES-CONTRACT-v1.md:56-58`).
  - Yet the S012 search-log stop rationale reads "further opens would not change the registry (≥2 rejected rows already met)" (`corpus/SOURCES.md:67`), a quota-style stopping rule. The round-12 connector named this anti-pattern (`.ufo/evidence/round-12/l2-connector.md:21`).
  - Rejected rows went from 2 to 3 (S011,S012 → S011,S012,S030) between `5174e15` and `HEAD` (replica status histogram). The admission mistake *raised* the "taste evidence" tally.
- **Score risk.** A criterion counted toward the "N criteria from mined mistakes" score (`corpus/lessons/round-12.md:107`, 11/16 vs 9/16) earns credit from its count unless it carries the discriminating receipt. Precedent: R12-a and M5 were routed to gate maintenance, not QUALITY (`corpus/lessons/round-12.md:17,104`).
- **Smallest safe correction.**
  - The criterion text says a duplicate rejected in place is a *correction*, not taste evidence. It is tallied separately (e.g. `rejected: duplicate`), never toward any rejected-row count.
  - Criterion 17 counts as "from a mined mistake" only with the receipt from counterexample 1.

## Documented limits a draft must state (not defects)

- 10 rows have no `http(s)` URL (S001–S004, S011, S013–S015, S019, S020). The URL check covers none of them. Two rows citing the same local file (e.g. S020's `windows.conf`) would never collide.
- Only the first URL in a source cell is checked (`url_of` uses `match`, `sources-census.sh:601`).
- Query strings and `www.` are not normalized (replica CE5: a `?v=1` variant of S017 raises nothing).
- Revision-pinned blob URLs (`/-/blob/<sha>/`) count as different URLs. A supersedes row that switches to a commit URL therefore produces no collision, so the binding check must still resolve the superseded id.
- Fork: two rows that both supersede S006 pass the census (replica CE6). The lane check should name a second live superseder of one id as a WARN.

## Required selftest fixtures (in-memory)

| # | rows | expected |
|---|---|---|
| T1 | S017 + S030 exactly as at `5174e15` (both mined, paraphrased scopes, “Syntax” vs `#syntax`) | FAIL, names `S017,S030` |
| T2 | same pair, S030 `rejected` (as at `HEAD`) | PASS, 0 errors |
| T3 | S006 + S042 same URL, `teaches` opens `supersedes S006 —` | PASS |
| T4 | as T3 but `supersedes S005 —` | FAIL (unbound) |
| T5 | as T3 but supersedes in mid-text | FAIL (not opening) |
| T6 | rejected S012 + later queued same URL, no link | WARN named; PASS with `supersedes S012 —` |
| T7 | S017 + new row, same URL, disjoint anchor section (S030's flip) | WARN named (review), not FAIL |
| T8 | two rows superseding S006 | WARN named (fork) |
| T9 | full `HEAD` registry | PASS (0 errors) — existing checks stay valid |

## Verdict guidance for the judge

- **Fixable defects:**
  - unbound or unanchored supersedes (CE3);
  - rejected-row false positives (CE2);
  - the missing red/green historical pair (CE1);
  - a merged-table-only trigger (CE7).
- **Tradeoffs to accept knowingly:** fail-closed anchor overlap (CE5) and the rejected-first WARN (CE6).
- **Reject the draft if:** T1 passes; or T2, T3 or T9 fail; or the draft edits any immutable cell of S030 or `corpus/SOURCES.md:92`.

## Checks for L1 (not run by this seat)

1. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` — expect exit 0, one W04 S030.
2. `python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/MistakeFix.py --selftest` once it lands — cover T1–T9.
3. Run the MistakeFix check on `git show 5174e15:corpus/SOURCES.md` (expect FAIL S017/S030) and on `git show HEAD:corpus/SOURCES.md` (expect PASS).

## Addendum — the integrated rows (2026-10-20, after GlobalDocs reported integration)

I reread the uncommitted working tree (`git status`: `corpus/SOURCES.md` modified, `corpus/lessons/round-13.md` untracked). Real census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → three W04 lines (S030, S042, S045), `ok`, exit=0 [OBS, 2026-10-20].

**A1 — the search-log count is hard-coded, not counted (operability; criterion 10; blocking for the count only).** At `corpus/SOURCES.md:116`, the "Counting command" is `python3 -c 'a=["S005","S017"]+[f"S{i:03}" for i in range(40,46)]; print(len(a),len(a)-1,1)'`.
- The included count is `len(a)-1` and the rejected count is the literal `1`. Both are assumed rather than read from the registry.
- This is the same class as the round-12 portal-note defect at `corpus/SOURCES.md:90`: `printf '%s' '' | wc -l` reported as "excluded 0".
- **Correction:** derive both counts from the rows. Example: `awk -F'|' '$2~/S0(05|17|4[0-5])/{gsub(/ /,"",$9);n[$9]++}END{for(k in n)print k,n[k]}' corpus/SOURCES.md`, or a script over status cells plus the S017 used-by diff. Otherwise label the count as asserted.

**A2 — S045 adds a fourth rejected row and a second permanent W04 for one mistake (coverage; CE8 confirmed; tradeoff).**
- S045 (`corpus/SOURCES.md:57`) is `rejected`. Its `teaches` cell opens `supersedes S030 — REJECTED: …`. That link is correctly bound (S030 shares the URL) and opens the cell.
- Problems:
  - (a) The rejection reason now lives in three places: `SOURCES.md:91`, `lessons/round-12.md:122`, and S045. The contract's in-place rule had already satisfied it through the lesson log (rule 2), so S045 is not required.
  - (b) A tier-A `docs` row whose scope is "Duplicate current-wiki source admission" scopes the page's authority to a registry meta-claim the page does not teach.
  - (c) The status histogram's rejected count is now 4, up from 2 before the mistake. That inflation is exactly what the contract warns against.
- Mitigations that already exist:
  - `lessons/round-13.md:22`: "not evidence that more rejections is better".
  - `SOURCES.md:128`: "not a source-volume or rejection-quota signal".
- **Smallest safe correction:** keep S045 only if no metric counts rejected rows. Report the histogram as `rejected 4 (2 duplicate-correction: S030, S045)`. Otherwise drop S045, because the lesson log already discharges rule 2. It is still uncommitted, so removing it violates nothing that is append-only.

**A3 — S042 narrows scope while claiming to supersede all of S006 (coverage; fixable).**
- S006 scope: "compositor globals, protocol dumps", with anchor §Compositor features + §Protocol dumpers.
- S042 scope and anchor: §Compositor features only (`SOURCES.md:18` vs `:54`). Its `teaches` opens `supersedes S006 —` with no qualifier.
- A reader retiring S006 loses the §Protocol dumpers anchor. `lessons/round-13.md:48` says S006 "stays queued", which contradicts a full supersede.
- GlobalDocs reports the narrowing was deliberate (W04 accepted). The binding is valid, and the census and my CE3 rule both pass.
- **Correction (uncommitted, so editable):** qualify the supersede, e.g. `supersedes S006 — §Compositor features only; §Protocol dumpers stays owed on S006 —`. Alternatively, record that partial scope in the round-13 lesson.

**A4 — what the integration got right (no change needed).**
- S042 binding is valid.
- The `:92` erratum is appended at `SOURCES.md:123-128`; it does not overwrite `:92`.
- S030's cells are unchanged.
- The S045 shape is accepted by MistakeFix's selftest (`MistakeFix.md:178`).
- S043 needs no supersede row, given GlobalDocs' byte-identity report against upstream `93c04ad`. I did not reverify that report.

**Addendum resolution (GlobalDocs reply, 2026-10-20).**
- **A1:** confirmed. The 7 mined + 1 rejected statuses are true but were never derived. The note should derive them from the status cells and call them "candidate row actions", because S005 and S017 are existing rows.
- **A2:** I withdraw the drop option. Contract rule 2 prescribes a correction row when a `teaches` cell is immutable, so keeping S045 is correct. Tag it as a duplicate-correction in the round-13 lesson's histogram note, not in the registry.
- **A3:** extending S042's anchor to `§Compositor features + §Protocol dumpers` is acceptable only together with three other changes. Otherwise the anchor covers ground the scope and teaches don't claim:
  - (a) widen the scope cell to cover protocol dumps; using S006's exact scope string also removes the S042 W04;
  - (b) make `teaches` name the dumper content;
  - (c) add a ≤25-word §Protocol dumpers quote with its location to `lessons/round-13.md` § Gate (rule 1).
  
  If any of (a)–(c) is missing, use the qualifier fallback: "§Compositor features only; §Protocol dumpers stays owed on S006".
- **A3 package (GlobalDocs, 2026-10-20):** conditions (a)–(c) are encoded in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/GlobalDocs.md` §6.
  - (a) The scope cell uses S006's exact scope string.
  - (b) `teaches` names wayland-tracker, wayland-tracer and wlanalyzer, and separates inventory from traffic.
  - (c) The Gate quote is "When using `export WAYLAND_DEBUG=1` (or …) is not enough, the following tools may help." It is 16 words (I counted), at `extras.html:36-39`.
  
  I did not reopen the page bytes to check the quote. The package is routed to L1, because no seat owns `corpus/SOURCES.md`; the qualifier fallback is kept if a cell can't change. **For L1:** after applying it, rerun the census and expect the S042 W04 to disappear (only S030 and S045 remain); then reopen the extras.html revision `8923a199…` and confirm the quote's text and location.
- **Independent check of the A3 quote (AttackMistake, non-author, 2026-10-20) [OBS]:**
  - `curl -fsSL https://wayland.freedesktop.org/extras.html | sha256sum` gives `97467f81afe4f303…`.
  - `curl -fsSL https://gitlab.freedesktop.org/wayland/wayland.freedesktop.org/-/raw/8923a19916635c21a3577b616f650a7e45d70fa9/extras.html | sha256sum` gives the same `97467f81afe4f303…`.
  - In the served page, `grep -n 'is not enough'` finds line 38, inside a link within the sentence at lines 36-39. That matches GlobalDocs.
  
  The census rerun is still L1's job. (Both pages were read inside the same round, so this is not outside-lane verification.)
