# Seat CritC2Cheat — report (round 43, w1, inline v1)

**Assignment.** Forge C2 entry+registry+lesson sets that `PRED-C2-r43` admits while the claim is
not grounded; name the clause that should have caught each, and a tightening that still admits
control P. Counter not edited.

**Verdict.** The frozen counter admits **16 forged sets** at `admitted=1/1 verdict=TARGET_MET`
(exit 0). One negative control (locator naming the second occurrence) is correctly rejected, so
the counter is not simply blind. **7 of the 16 are mechanical** and closed by P-safe tightenings I
ran; **5 are the declared residual** (claim binding); **1 is a tradeoff that rejects control P**;
**1 needs a fixture grammar**; the remainder are scope gaps of the same family. Details, fixture
deltas, verdicts and probe results: `.ufo/waves/round-43/w1/CritC2Cheat/forgeries.md`.

Counter identity: `quality/counters/c2-r43-gkeep-entry.py`
sha256 `4b5751fe7010400a5a7e4132dafc3f297132d443f2389a61f0b89032c669016c`.
After every run, `git status --porcelain` over `quality/counters`, `.ufo/waves/round-43/ctl`,
`.ufo/waves/round-43/fetch`, `registration.md` is empty: the freeze, the counter, the controls and
the pins are untouched. All fixtures are built by the frozen controls' own helpers in scratch
(`git -C "$D" init -q`, toplevel asserted `== $D`), with the real pre-wave pins as receipts, so
every forged quote is a genuine quote at its genuine counter-computed line.

## Findings, ranked

1. **Control P is itself a wallpaper entry** (`H1`, residual, widest). P's admitted entry is a
   header + eleven `**OBS** <id> <quote> (<file>:<line>).` lines + the three census lines: it makes
   no claim about the gkeep chain. Adding the sentence *"Nothing here is determined by the sources
   below; the compositor picks the size on its own."* is still `admitted=1/1`. The declared
   residual ("a real receipt can be cited for a claim it does not support") assumes a claim exists;
   mid-wave, none needs to. C2 as frozen certifies quotation bookkeeping, not coverage.
2. **Census contradiction computed and ignored** (`A2`). The entry claims "the only gkeep client is
   mapped, floating and reports the rule size" with the chromium object as evidence
   (`host-clients-r43.json:49`), while clause h computes `total=4 floating=0 gkeep=0` on the same
   revision. `admitted=1/1`. Residual; a fixed-form conclusion line would close it but P lacks one.
3. **Occurrence ambiguity** (`B1`, mechanical). `const auto& expr = std::get<Math::SExpressionVec2>(value);`
   is at `Hyprland-WindowRuleApplicator.cpp:174,203,414,422`; the counter forces the first line
   (`:174`, MAX_SIZE) and the entry claims the size branch (`:422`). `admitted=1/1`; the honest
   `:414` variant is rejected. Fix: require exactly one word-bounded occurrence (P-safe).
4. **Comment cited as code** (`C1`, `C2`, mechanical). `// TODO: not very OOP, is it?`
   (`Hyprland-DefaultFloatingAlgorithm.cpp:105`) and
   `// Reserved area must be updated before this is called` (`Hyprland-WindowTarget.cpp:102/126`)
   are accepted as evidence of behaviour. Fix: strip comments per extension (P-safe).
5. **Assimilation provenance is basename-only** (`F1`, mechanical, cheapest). ADMIT/REFUSE may name
   `merge/mado/not-a-real-dir/gkeep-size-to-real-size-r11.md`; `admitted=1/1`. Fix: require the
   theme directory prefix (P-safe, one constant).
6. **REFUSE needs four distinct words, not a flip condition** (`F2`, mechanical-with-vocabulary).
7. **PROVINCE markers are scanned in registry rows only** (`X2`, mechanical). Chinese text in the
   entry prose is admitted; fix: apply BAD_LOC to the entry's unfenced lines (P-safe).
8. **No source chain required** (`X3`, mechanical). An entry citing only the three own-work
   receipts and the held id — zero Hyprland receipts — is `admitted=1/1`, although PINS enumerates
   all seven. Fix: require every PINS basename to be cited (P-safe).
9. **Location cell carries no provenance — in P too** (`G1`, `G2`, tradeoff). All seven code rows of
   control P carry `https://example.org/...` (`run-c2-controls.py:38-49`) while the registration
   records the true raw URL. Requiring the real prefix rejects P (`e:0`). The canonical judge must
   choose: true URLs in a v2 fixture, or declare the cell decorative.
10. **Id cited on one line, contradicted on another** (`E1` mechanical via an every-naming-line
    rule; `E2` residual when the id is omitted). Index-row lie (`X1`) is the same family but needs
    a row grammar.

## Impacted axes

* **Coverage (C2)** — every forgery above inflates it; admission is decided by citation shape, not
  by the theme being covered (H1, X3, A2, D1).
* **Province / §3 report content** — X2: the localized-documentation exclusion is enforced on
  registry rows only, not on the entry the knowledge lands in.
* **§2b assimilation (frontier step, part of C2's registration)** — F1/F2: the ADMIT/REFUSE pair
  can name a non-existent package path and a reason with no flip condition.
* **Operability (C1)** — not touched. C2 never runs C1's tool; all fixtures here use C2's own
  parsers over pinned receipts.

## Smallest safe correction

Seven string-local counter tightenings, each verified on a scratch copy of the counter against
both control P and its forgery (P `1/1`, forgery `0/1`): `unique-occurrence`,
`quote-not-in-comment`, `every-naming-line-bound`, `package-path-exact`, `refuse-flip-marker`,
`bad-loc-in-entry`, `all-pins-cited` (`probes/`, `receipts-probes-sha256.txt`, `run-probes.log`,
`run-more.log`). Taken together they close B1, C1, C2, E1, F1, F2, X2, X3 without changing the
accepted fixture set. They do not close A1/A2/D1/E2/H1: those need a claim grammar or a
fixed-form conclusion line that control P does not carry, i.e. a v2 fixture. G1/G2 need a decision
on whether the location cell is provenance or decoration.

Because no C2 data commit exists yet (round 42 never ran a seat; w1 has no data at review time),
the registration's own rule applies: pre-data holes re-register as v2 with a new freeze naming both
predicates — not a post-data report. My recommendation is v2 with (a) the seven tightenings, (b) a
required fixed-form `host census …` conclusion line so A2/D1 become mechanical, (c) at least one
required claim line per cited id so H1 cannot be admitted claim-free, and (d) true raw URLs in the
fixture if the location cell is to mean anything.

## Evidence inventory (all under `.ufo/waves/round-43/w1/CritC2Cheat/`)

* `forgeries.md` — the deliverable: per-forgery fixture delta, observed verdict line, clause,
  classification, tightening and probe result.
* `run-forgeries.log` — 15 fixtures (P + 14) scored by the frozen counter; `14/15` admitted, `B2`
  rejected; counter sha256 on line 1.
* `run-more.log` — X1/X2/X3 (all admitted) and the `refuse-flip-marker`, `bad-loc-in-entry`,
  `all-pins-cited` probes.
* `run-probes.log` — `unique-occurrence`, `quote-not-in-comment`, `every-naming-line-bound`,
  `package-path-exact`, and the negative `url-exact` probe that rejects P.
* `run-verify.log` — `VERIFY PASS`: every quotation checked as a substring at its
  `file:line` (22 quote checks), every cited log line re-grepped (20 checks), the real staged path
  present and the forged one absent.
* `fixtures/<tag>/` — the changed files of each forged fixture (entry, `corpus/SOURCES.md`,
  `corpus/lessons/round-43.md`, `corpus/README.md`).
* `forge.py`, `more.py`, `probes.py`, `verify.py` — drivers; `probes/*.py` — the patched counter
  copies, sha256 in `receipts-probes-sha256.txt`.

Not run: any host compositor read, any oracle, any package transaction. Tools: `python3 3.14.8`,
`git 2.56.0` — nothing installed.

Scratch `/fast/scratch/hyaku/mado-r43/CritC2Cheat` removed after the receipts above were copied
into the seat dir.
