# CritLocatorGate — the locator gate checks identifiers, not facts (round 43, w2)

**Item attacked:** `quality/check-locators.py` (sha256 `c1ea52ad…`, byte-identical to the w1 deliverable) and QUALITY
criterion 77 (`corpus/QUALITY.md:401`), at the data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`.
**Full evidence:** `.ufo/waves/round-43/w2/CritLocatorGate/findings.md` + the 17 run receipts it lists.

**Verdict: defect, not a tradeoff.** The checker is honest about many of its limits and it kills the round-42 defect it was
built for; but 20 of the 22 inputs I built are judged wrongly, **a mutated copy of the landed entry passes (`miss=0`,
exit 0)**, and criterion 77's own bytes fail criterion 77. The landed *data* is nevertheless clean: all 14 `OK` verdicts carry
the attributed quote verbatim and every digit of it in the cited range (`strict-r43.txt`, `ok_but_weak=0`).

## Runs at the data commit

| run | result |
|---|---|
| `--selftest` | `cases=18 passed=18`; `teeth flipped_table_broken=yes`; `SELFTEST: PASS`, exit 0 (`selftest.txt`) |
| 62 prose files (`SKILL.md`, `LOG.md`, `corpus/knowledge/*.md`), `--fetch .ufo/waves/round-43/fetch` | `locators=16 miss=1`, exit 1 (`run-r43-fetch.txt`) |
| same, `--fetch .ufo/waves/round-42/fetch` | `locators=15 miss=1`, exit 1 (`run-r42-fetch.txt`) |
| entry alone | `locators=10 miss=0`, exit 0 |
| auxiliary `corpus/lessons/round-43.md` | `locators=22 miss=5` — 15 of the 22 are `NOFRAG` (`lesson43-run.txt`) |

## Counterexamples (each is the checker's own output; inputs in `adv-real.md`, `adv-synth.md`, `mut/`)

1. **Numbers are never compared.** `window.set_default_size(640, 720)` at `gkeep-ui-excerpt.py:33-34` → `verdict=OK`
   (`:33` reads `420, 500`); in the landed entry the round's central numbers can be changed to `size 640 720` and
   `set_default_size(640, 720)` with `CHECK_LOCATORS: locators=10 miss=0`, exit 0 (`mut-runs.txt`, `M1`). `ID_RE` has no digit
   class; 0 of the 18 selftest cases contains a digit inside a fragment.
2. **Statement is a token set.** `FullMatch(*m_regex, other)` passes against the receipt's `FullMatch(other, *m_regex)`
   (`M7`, `miss=0`); so does `m_realSize->value(); case … return m_realSize->goal()` against lines 19-20 (`A9`, `OK`).
3. **A locator past EOF passes when its line has no fragment.** `Hyprland-GeometricMovableAnimated.cpp:999` (file has 24
   lines) → `NOFRAG`, no miss — both with the quote wrapped on the previous line (`A3`) and with no backticks at all (`A4`). The
   landed `SKILL.md:257` is exactly this shape: `fragments=0 verdict=NOFRAG` for the entry's central goal/value fact.
4. **The "shared word" defect criterion 77 forbids is `OK`.** `size` at `Hyprland-HyprCtl.cpp:394-395,412-413` → `OK`
   (`supported=1`): the cited lines are JSON template text, and the shared word `size` is the only support. The `MISS` on
   `LOG.md:2483` happens only because that line's fragment happens to be the longer code expression.
5. **False MISS on correct prose.** The lesson's pointer line ("re-derived all three from `host-gkeep.conf:2-4`,
   `host-clients-r43.json` and `gkeep-ui-excerpt.py:6,33`") gets two `MISS` because a bare file name becomes a "fragment" and
   both locators are attributed to it; a skipped locator span (`round-42-verifier-spotcheck.md:84`, `receipt.txt:60`) is
   likewise used as a fragment. Qualified prose against an unqualified source also MISSes (`A7`), while the reverse
   abbreviation passes (`A8`) — the asymmetry is backwards.
6. **Coverage: 2.1%.** 779 locator-shaped tokens in 16 679 lines, **16 resolved**; 763 skipped over 165 names; 32 `.ufo/…:N`
   citations the regex cannot match (leading-dot lookbehind); 919 bare `:N` continuations unscored; 111 lane-document
   locators (`LOG.md:…`, `PROVINCE.md:…`) all `SKIP` (`coverage-census.txt`, `coverage-skipped.txt`).
7. **Criterion 77 fails itself.** Its worked example says "the appended correction `LOG.md:2487`" — `LOG.md` has 2483 lines at
   the data commit; the criterion's own paragraph through its own checker prints `locators=2 miss=2`, exit 1 (`q77-run.txt`).
   And "a locator with no backticked fragment is `NOFRAG`, not a pass" (`corpus/QUALITY.md:401`) contradicts the command,
   which exits 0 over `NOFRAG` — the data commit lands one at `SKILL.md:257`, the lesson lands 15.

## Every MISS, triaged

- `LOG.md:2483` — **real**, and not round-43 data: byte-identical at the base (`sha256` of the line `418a2949…`). It is the
  round-42 text kept append-only, so **the whole-file command exits 1 permanently**; the close-out must scope the run to the
  round-43 lines (the correction lands at `LOG.md:2487` at HEAD, absent at the data commit).
- lesson:115, :124 — real by design (they quote the round-42 wrong locator and a checker output); :118 — right verdict, wrong
  reason (a skipped locator span decided it); :216 ×2 — **false**, checker limit. `w2/ExecHarmTip.md` F4 reads all five as
  "prose that *quotes* the defective locators" or a previous-line fragment and concludes the gate is "red on the lesson by its
  own declared limit"; on :216 ×2 that reading is wrong: the deciding "fragment" is the bare file name `host-clients-r43.json`,
  so a correct pointer list is refused, and criterion 77 calls a `MISS` a violation — the harm is a false violation, not a limit.

## Impacted axes

- **Coverage (evidence quality).** A "criterion 77 met" line at this rev would be premature saturation: the gate supports
  "16 locators naming one fetch dir were checked; 14 hold their quote", not "every source locator in prose".
- **Operability: not affected.** No C1/C2 file is touched; the checker reads no counted file.

## Smallest safe correction (prototype measured, `patchedcheck.py`)

Four tightenings, **no landed verdict changes**: mandated set `16 → ok=14 miss=1 nofrag=1` (only `LOG:2483`, still `MISS`);
entry `10 ok`; lesson `miss 5 → 2` (the two false MISSes become `NOFRAG`); `M1` → 2 `MISS`, `M7` → `MISS`,
`A10`/`A11` → `MISS`.

1. **order** — the fragment's identifiers must occur in the cited text in the fragment's order (keeps the lane's abbreviation
   style, kills the argument swap).
2. **range** — refuse `:0`, any member outside `1..len`, and a reversed range (no silent widening).
3. **siblings** — drop every `LOCATOR_RE`-shaped backticked span from the candidate set, resolved or not; a bare fetch-file
   name is a pointer, not a fact.
4. **digits** — every digit run of the fragment must occur in the cited text.

Policy items the L1 must decide, not code: count `NOFRAG` and single-identifier fragments in a named `weak=` bucket and say in
the criterion what happens to them; widen the check to lane documents (`git show <rev>:<path>`) if "every source locator" is
meant; fix the `LOG.md:2487` example to a locator true at the revision that carries it; add the six missing selftest cases
(numeric fragment, wrapped locator, out-of-file line with no fragment, qualified name, reversed range, sibling file name) —
without one, a future tightening cannot be regression-tested. Comment support is currently *pinned* by selftest case 7
(`gamma` at a `//` line expected `OK`), so a comment-aware comparison cannot pass the shipped table.

**Not claimed:** the fetch directory's bytes are the declared trust root and I left them alone; A1/S1/S3 (a generic identifier
or a comment supporting a fact) is a reading limit no token test closes, reported as `weak`, not as a bug; criterion 77's
`LOG.md:2487` is true at HEAD — I report only that it is false at the data commit.
