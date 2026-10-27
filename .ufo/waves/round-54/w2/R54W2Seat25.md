# R54W2Seat25 — w2 falsification: item 25, C2 host join matching (literal full path:line vs basename)

Wave: round-54 w2. Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (verified ancestor of lane HEAD
`350d30e4ec5531f65ce99a57efeb8216f38e678a` via `git merge-base --is-ancestor`; prints
`base-is-ancestor-of-HEAD=yes`). No predicate, registration, lane, sibling or source file touched.

## Axes

- **Coverage** — does frozen clause (c) ("entry carries at least two host join citations among the
  frozen host set", `claims-frozen.md:63-65`; host set `registration.md:73-76`) pin a judge tight
  enough that two honest readers cannot disagree, and that a forged entry cannot pass?
- **Operability** — can a w2 seat re-run the pinned detector for this leg at the scored revision?
  (Answer: no — the pinned counter is absent at base and at HEAD; see NOT RUN below.)

## Frozen contract lines under attack

- `claims-frozen.md:63-65` — clause (c): "the entry carries at least two host join citations among
  the frozen host set of `registration.md`". No matching algorithm is frozen.
- `registration.md:73-76` — the frozen host set, written as eight full `~`-prefixed identifiers with
  line-shorthand: `~/.local/share/omarchy/default/hypr/autostart.conf:1`, `:2`, `:3`, `:4`, `:5`,
  `:6`; `~/.config/hypr/bindings.conf:2`; `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`.
- `registration.md:78-90` — the six C2 controls. Only `C2-CTL-6` (line 87: "entry text carries none
  of the frozen host set" → clause (c) fails) touches clause (c), and it pins only the **all-zero**
  case. No control distinguishes literal full-path from basename matching, citation context, or
  distinct-vs-occurrence counting.

## Pinned spans re-verified (existing pinned command, read-only)

`sha256sum -c SHA256SUMS.txt` in `.ufo/waves/round-54/fetch/` → all three pins `OK`, exit 0:
`uwsm-0.27.1-README.md: OK`, `uwsm-0.27.1-main.py: OK`, `uwsm-0.27.1-uwsm-app.1.scd: OK`.
The frozen pin spans hold at those bytes: `README.md:117-118` carries "Difference between
environment state before and after preparation is exported / into systemd user manager (and D-Bus
activation environment if reference D-Bus implementation is used)"; `uwsm-app.1.scd:60` carries
"*uwsm-app* client sends arguments to uwsm's app daemon via a pipe."; `main.py:3714` carries
`unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"`.
So the S375–S377 quote legs are sound; the attacked leg (c) is disjoint from the pins — host joins
cite `~` host paths, and **no tracked lane path begins with `~`** (`git ls-tree -r <base> --name-only
| grep -c '~'` → `0`): clause (c) is verifiable only as string presence, never against pinned bytes
(same structural limit as w1 `R54Seat08` F8, report line 351).

## NOT RUN — pinned C2 counter absent (no invented results)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa
python3: can't open file '.../quality/counters/c2-r54-uwsm-entry.py': [Errno 2] No such file or directory
$ echo $?
2
```
`ls quality/counters/ | grep -c r54` → `0` at HEAD; `git ls-tree e25149fe... quality/counters/ |
grep -c r54` → `0` at base. This matches the frozen Before state (`claims-frozen.md`, C2 Before), so
no host-join leg of any real counter could be re-run: **counter: NOT RUN/absent**. All results below
are a reference probe, not the frozen counter.

## Probe: two plausible judges of clause (c) disagree

Reference probe `clause_c_probe.py` (scratch-only, synthetic entry text, no lane bytes):
- **literal** judge — substring match of each full frozen identifier (shorthand `:2`–`:6` expanded);
- **basename** judge — match of `basename:line` (the relaxation w1 used).

Clause (c) passes iff ≥2 distinct identifiers match. Output (exit 0):

```
variant                 literal distinct  basename distinct  literal(c)  basename(c)
V1_literal_full_form                   2                  2        PASS        PASS
V2_basename_form                       0                  2        FAIL        PASS
V3_home_expanded                       0                  2        FAIL        PASS
V4_range_phrase                        0                  1        FAIL        FAIL
V5_disclaimed_example                  2                  2        PASS        PASS
V6_duplicate_single                    1                  1        FAIL        FAIL

VERDICT FLIP under judge choice: V2_basename_form
VERDICT FLIP under judge choice: V3_home_expanded
probe_exit=0 flips=2
```

### Findings

- **F25-1 (verdict flip, high).** Identical two-join content in basename form (V2) or `$HOME`-
  expanded form (V3) is clause-(c) FAIL under a literal judge and PASS under a basename judge. The
  frozen sentence and the six controls leave the mode unpinned, so `TARGET_MET` vs `TARGET_MISSED`
  for the same entry is implementation-defined. W1 independently measured the flip on real drafts:
  `R54Seat08` report line 230 — "exact frozen strings: **0/8**; basename:line relaxed: **2/8**
  … → **judge-dependent** (F7)"; `R54Seat30` §C4 (report lines 397-412) — "matched verbatim : 0/8,
  matched by basename:line only : 3/8 … a counter that requires the full path scores the honest
  entry 0/8 → clause (c) fails → TARGET_MISSED".
- **F25-2 (basename referent ambiguity, high).** Basename matching is not merely relaxed — it is
  ambiguous inside the lane itself. At base, tracked files with basename `autostart.conf`: **5**
  (`.ufo/waves/round-18/fetch/ReopenS093/autostart.conf`,
  `.ufo/waves/round-39/w1/ExecOptionsRealTree/host-tree/.config/hypr/autostart.conf`,
  `.../host-tree/.local/share/omarchy/default/hypr/autostart.conf`,
  `.ufo/waves/round-39/w1/SctHostTree/real-tree/.config/hypr/autostart.conf`,
  `.../real-tree/.local/share/omarchy/default/hypr/autostart.conf`); basename `bindings.conf`: **4**
  (same four round-39 trees); `omarchy-toggle-idle`: **0** tracked (corroborates `R54Seat07`'s w1
  finding "no committed omarchy-toggle-idle bytes"). A `autostart.conf:1` citation therefore denotes
  at least five different in-repo candidates plus the uncommitted host file — the judge cannot tell
  which, and none is byte-verifiable in-round. The literal judge removes this ambiguity but at the
  cost of F25-1's false negatives.
- **F25-3 (both judges admit disclaimed examples, medium).** V5 carries two exact frozen strings
  only inside an express disclaimer ("NOT asserted as joins (examples only)") and **both** judges
  pass clause (c). Presence-based matching cannot see citation context. This is w1 `R54Seat21`'s
  counterexample ("two distinct frozen host file:line strings occur only in an expressly disclaimed
  example, yet a string-presence counter may count them as two joins", `w1-results.json` entry
  R54Seat21; report lines 7-15) reproduced here under both candidate judges. No registered control
  (`registration.md:78-90`) covers incidental/negated occurrences.
- **F25-4 (range prose counts as zero, low/consistent).** V4 ("the six exec-once lines at lines
  1-6 … idle re-arm wired at omarchy-toggle-idle:9") yields 1 basename match, 0 literal → FAIL under
  both. Matches `R54Seat08` line 230: "`autostart.conf:1..6` appear only as the phrase 'at lines
  1–6' → 0/6 under any `name:<line>` matcher". The freeze does not say whether a range phrase
  expands (also flagged by `R54Seat30` §C5).
- **F25-5 (distinct vs occurrence counting, low).** V6 (one identifier twice) fails under
  distinct-counting; an occurrence-counting judge would pass it. W1 `R54Seat22` found the same
  repeated-citation ambiguity; recorded here because neither judge choice is frozen.
- **F25-6 (gameability corroboration, from w1).** `R54Seat30`'s route N-2 (`w1-results.json` entry
  R54Seat30): "the recycled body already carries one frozen full-path host join
  (`~/.config/hypr/bindings.conf:2`), so one appended string reaches hosts≥2" — a literal judge is
  satisfiable by a recycled round-47 body plus one string; clause (c) bounds forgery only weakly in
  either mode.

## Verdict

**Ambiguity confirmed — clause (c) is judge-dependent.** The frozen predicate does not specify
literal vs basename matching, citation-context handling, range expansion, or distinct-vs-occurrence
counting; its only clause-(c) control (C2-CTL-6) pins the zero case. Two honest counter
implementations return opposite verdicts on the same entry (F25-1/F25-3). Per the freeze rules
(`claims-frozen.md:5-8`) this cannot be fixed by editing the frozen files post-score; it is an
admission-ambiguity finding for the round record, not a license to change the contract.

## Mutation-tester bookkeeping

- Mutant/probe: synthetic entry-text variants in scratch (V1–V6) against two reference judges;
  no lane, sibling, fixture-tree or git object mutated — the absent counter left nothing to mutate.
- Expected detector: `python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev <rev>`
  printing `MADO_UWSM_ENTRY: … verdict=…` — **expected run NOT EXECUTED, counter absent** (exit 2
  receipt above); baseline/mutant/restored counter outputs therefore do not exist.
- Restoration evidence: no tracked lane bytes were opened for write at any point; working tree
  before and after this seat differs only by other seats' pre-existing state
  (` M corpus/SOURCES.md` and untracked wave/report files, observed, untouched). Scratch
  `/fast/scratch/hyaku/mado-r54/R54W2Seat25` (probe script only, 3759 bytes) is removed before
  yield; no scratch remaining, no ENOSPC observed.

## Report trailer

Lane-relative: `.ufo/waves/round-54/w2/R54W2Seat25.md`. Commands re-run (all read-only):
`sha256sum -c` over `.ufo/waves/round-54/fetch/SHA256SUMS.txt` (exit 0), pinned-span extraction
(`sed -n` on the three fetch pins), absent-counter invocation (exit 2, receipt above),
`git merge-base --is-ancestor`, `git ls-tree`/`git ls-files` basename census. No installs or tool
updates. No subagent dispatch; no git/jj mutation; no live host reads, package queries, screenshots,
producer execution, or host/config/service/compositor mutation.
