# ScrLessonSkeleton — round-43 lesson skeleton (final)

Seat: `ScrLessonSkeleton` (scribe, w1). Task: draft `corpus/lessons/round-43.md` — `## Gate`, assimilation decisions, `## Mistakes`.
Every byte this seat wrote is inside its own seat directory; no tracked file was edited, no git/jj mutation was run, nothing outside the lane was
written.

## Artifacts

| path (relative to the lane root) | what |
|---|---|
| `.ufo/waves/round-43/w1/ScrLessonSkeleton/round-43-lesson.md` | the draft the L1 lands as `corpus/lessons/round-43.md` (24,714 B; 26 `<<L1>>` markers) |
| `.ufo/waves/round-43/w1/ScrLessonSkeleton/receipts.txt` | this seat's command receipts (quote checks, registry tokens, mistake evidence) |
| `.ufo/waves/round-43/w1/ScrLessonSkeleton.md` | this report |

Scratch `/fast/scratch/hyaku/mado-r43/ScrLessonSkeleton` was created and deleted in this run (`ls /fast/scratch/hyaku/mado-r43/` no longer lists it).
No tool was installed; no package transaction ran.

## Behavior — what was done

1. Read the frozen registration (`.ufo/waves/round-43/registration.md`), the round-41 lesson and its non-author closure (shape), the round-42
   non-author closure (routed defects), and PRED-C2-r43's docstring (clauses d and i define the Gate grammar).
2. Recomputed all ten pin hashes with `sha256sum` in `.ufo/waves/round-43/fetch/` — they match `receipts/fetch-sha256.txt` exactly, and all ten
   are committed mode `100644` (`git ls-tree -r HEAD .ufo/waves/round-43/fetch/`).
3. Chose one quote per cited id and verified each with a replica of the counter's `norm_receipt`/`quote_at`/word-count rules: 4-15 words,
   word-bounded at both ends, present in its own receipt, absent from every other cited receipt. Start lines: `Hyprland-RegexMatchEngine.cpp:16`,
   `Hyprland-WindowRuleApplicator.cpp:421`, `Hyprland-DefaultFloatingAlgorithm.cpp:56`, `Hyprland-Target.cpp:10`,
   `Hyprland-WindowTarget.cpp:70`, `Hyprland-GeometricMovableAnimated.cpp:19`, `Hyprland-HyprCtl.cpp:427`, `host-gkeep.conf:4`,
   `host-clients-r43.json:4`, `gkeep-ui-excerpt.py:33`.
4. Read all 11 staged gkeep-theme files in `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/` (read-only) and decided one
   ADMIT and four REFUSEs; recorded the other six as not adopted with the reason in the assimilation ledger.
5. Mined round 42's mistakes from the closure's routed items plus this round's freeze disclosures, each with an evidence pointer this seat
   re-opened (see below).
6. Self-checked the draft against the counter's own regexes (`GATE_RE`, `ADMIT_RE`, `REFUSE_RE`): 10 GATE ids, one line each, 0 indented
   `GATE S` lines, 0 `GATE S` lines outside `## Gate`, 1 ADMIT, 4 REFUSE with 16-21 distinct words each, ADMIT target == the entry path.
   **This is a replica check on the draft, not the counter** — the counter scores a committed revision and is the L1's to run.

## Gates (as drafted)

GATE lines: S290-S299, one per pinned receipt, sha256 as computed by this seat. ADMIT
`merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md` as `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (four of its five
sources are this round's pins S302-S305 ↔ S292-S295; its host receipt is re-grounded as S297/S298). REFUSE: `gkeep-size-rule-application-r10.md`
(its "the client decides the reported size" inference is overturned by the pinned path), `gkeep-geometry-unobservable-r8.md` (superseded, its
receipt path not held in this lane), `gkeep-observation-route-r11.md` (single-source restatement), `gkeep-element-rules-r30.md` (its 875×600
rests on a config comment, no measured source). Flip conditions are in the ledger table for every refusal.

Every new row carries `opened 2026-10-26`; the entry header carries `verified-at: 2026-10-26` (stated in the draft's access-date paragraph and
required by clauses b and c). No held row's `status` or `recheck` changes; the old→new log section states the used-by edits and leaves the
landed form to the L1.

## Findings (each names what it attacks)

**F1 — clause e collides for S291 and S296 (attacks the registration's id→receipt assignment vs PRED-C2-r43 clause e).** The lane already holds
`S155` with last cell-1 token `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp`
and `S158` with `…/efb5099…/src/debug/HyprCtl.cpp` (`receipts.txt`: "registry tokens for existing rows"). Clause e requires a new id's location
(fragment stripped) to appear in no other row, so S291/S296 cannot reuse those strings. The draft's Gate caveat gives both admissible
resolutions — tag address (`…/Hyprland/v0.56.2/<path>`, the form S018 and the staged package already use) or citing held S155/S158 and opening
only eight new rows — and the L1 decides before the data commit (`registration.md:72-73` permits a v2). The GATE lines themselves are
location-independent and stand either way; under the held-row resolution the S291/S296 lines must be deleted, not left dead.

**F2 — `registration.md:5` says `w1` is 37 seats; the dispatch is 38 (attacks the freeze line).** `.ufo/waves/round-43/w1-spec.json` `items`
length is 38 (`python3 -c "…len(d['items'])"` → 38) and `5add5b4` is "round-43: w1 spec, dispatch and validator registry (38 seats)". The
draft's shape paragraph discloses it and leaves the disposition to the L1. Same class as round-41 M41-5.

**F3 — the round-42 report the closure cites does not resolve in this repo (attacks the closure's decisive bytes).** The closure reads
`git log --format='%an %H' -- .ufo/reports/round-42/mado.md` → `mado-shokunin da384db4…`; `git cat-file -t da384db4d4848186ade6810a6718f5b24e909bdf`
→ "could not get object info", `git log --all -- .ufo/reports/round-42/` → empty, and `.ufo/reports/` at HEAD holds only `round-1`. So round 42's
report bytes are unavailable to a later seat: every round-42 report claim in the lesson is cited through the closure, never through the report.
This also limits M43-1: the `Hyprland-RegexMatchEngine.cpp:10-16` string could not be re-opened in the report; the HyprCtl locator was re-opened
in `LOG.md:2483` and round-42 `registration.md:61`.

**F4 — the pins are what the registration says, verified, not relayed.** The seven Hyprland pins are byte-identical to
`.ufo/waves/round-42/fetch/` (same sha256 for all seven), `host-gkeep.conf` is byte-identical (`3726e488…`), `host-clients-r43.json` is a new
capture (4 clients: Alacritty, zcode, grok-bot, chromium; all `floating: false`, all mapped) and `gkeep-ui-excerpt.py` is regenerated
(`3695b788…` vs round 42's `48a5c92f…`).

**F5 — `receipts/live-geometry-host.txt` is a wave-time receipt, not a freeze receipt (attacks any claim that the base holds a live run).**
Its own first line dates it `2026-10-26T04:17:54-03:00` (after the freeze commit) and it hashes `tools/mado-geometry.py` at `e3c2e471…`, a
working-tree file that does not exist at the base (`receipts/c1-before-base.txt` reads `tool=absent`). It is a good pointer for the SHONEN box
(M43-3) and it is reported, not scored.

**F6 — round 42's wrong locators are reproducible from the pinned bytes (supports M43-1).** `grep -n 'GEOMETRIC_GOAL'
.ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp` → 426, 427, 428, 447, 448 (never 394-395 or 412-413);
`Hyprland-RegexMatchEngine.cpp` has `starts_with("negative:")` at 7-8 and `FullMatch` at 16 (never 10-16).

## Mistakes drafted (`## Mistakes`, evidence re-opened by this seat)

- **M43-1** wrong prose locators — `LOG.md:2483` / round-42 `registration.md:61` vs the receipt's 427-428, 448, 7-8, 16; captured-by: none.
- **M43-2** C1 tally stated three ways — closure `:85` vs `receipts/ctl-c1.txt:1` (`controls=46`), `:50` (`0 of 47`), 38 `M*` of 48 `ok`
  lines, and `run-c1-controls.py:139` (`controls=%d` = `len(jobs) - 2`); captured-by: none.
- **M43-3** SHONEN box 2 pointed at a LOG.md entry never written — `git grep -n NO_MATCHING a62f2e0 -- LOG.md` → no hit; the string lives in
  the tool, the controls, the counter, `w1-spec.json` and round-42 `registration.md:24`, never in a run receipt; captured-by: the closure (`:66`).
- **M43-4** no round-42 lesson — `git ls-tree -r --name-only a62f2e0 -- corpus/lessons/ | grep -c round-42` → 0 (closure `:57`); captured-by:
  the closure's step-1 read; fix tested by clause d.
- **M43-5** excerpt header named lines 446-495 of a 488-line file and carried one extra blank line —
  `diff <(tail -n +3 .ufo/waves/round-42/fetch/gkeep-ui-excerpt.py) <(sed -n '446,$p' ~/Projects/gkeep/gkeep/ui.py)` → `44d43` (an empty line);
  the same diff on the round-43 excerpt is empty. This is the one mistake whose fix has a demonstrated discriminating control.
- **M43-6** a driver `complete` line and a clean `git status` read as round success — fleet digest `:1462` vs 29 files / 0 seat reports / no
  `w1-results.json` under `.ufo/waves/round-42/`, closure `:28`, `:88`, `:21`. Mined at `ScrConsiderthese`'s request for its proposal-2 criterion;
  the id was sent to that seat.

## Out of scope (deliberately not done)

- No counter was executed: both predicates score a committed revision, and committing is the L1's. The 26 `<<L1>>` markers are exactly the run
  results, the census after the data commit, the landed registry form, and the controls other seats owe (e.g. `ExecLocatorGate` for M43-1).
- No registry row, no `LOG.md` correction entry, no entry file, no `corpus/README.md` index row, no SHONEN box was written by this seat.
- No live compositor read was needed or taken; no oracle, no host mutation.
- The staged package was read only; nothing under `/home/vgpnk/Projects/shokuknow` was written.

## Known limits

- My Gate self-check is a replica of the counter's regexes and normalization, run over the draft file, not the counter over a revision. It shows
  the lines are well-formed and the quotes bind; it does not show `admitted=1`.
- The quote choices and the REFUSE reasons are this seat's; the entry seat must carry the ten quotes verbatim (or the L1's Gate lines will not
  bind clause g).
- A lesson quote should support the row's `teaches`, and that binding is the non-author closure's job, not this seat's.
