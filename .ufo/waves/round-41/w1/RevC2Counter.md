# RevC2Counter — attack the frozen C2 counter (w1, round 41)

Status: DONE. Full findings (severity-ranked, with line refs and reproductions):
`.ufo/waves/round-41/w1/RevC2Counter/findings.md`.

## Headline answers
- **Which docstring sentence has no mutant that kills it?** No clause *letter* is unkilled (a–i
  each have ≥1 killing mutant in the 40-mutant suite), but six *sentences* have no dedicated
  mutant: b-recheck, b-first-20-lines, c-"(at least 3)", d-quote-lower-bound, h-"not a tool's
  report", i-REFUSE/ADMIT-binding. Three are enforced by code but never exercised by any control
  (b-recheck, b-window, d-lower); three are contract words the code does not implement (c-≥3,
  h-tool-report, i-binding). A fixture with exactly 2 new ids passes (c doc says ≥3); a REFUSE
  for an unrelated path and an ADMIT for a non-staged package both pass; a "tool report" with a
  preamble passes h.
- **Can a fabricated entry with real-looking receipts pass? What is the cheapest forgery?** Yes —
  that is the declared residual. The suite's control P is 13,860 committed bytes; a minimal
  fabricated self-consistent set (invented 2-session/40-advert/20-interface/1-focus_grab journal,
  three invented 512+B receipts, invented quotes) **passes at 9,220 committed bytes / 9 files**
  (measured via the control runner's own `score()`).
- **Is clause i's localized-channel test a substring heuristic a rename defeats?** Yes. It is
  `amgsk.dev|zhihu|/zh|/ja` substring checks on the *whole cell* (title+location) of cited ids:
  a rename to `https://zenn.dev/...` passes; benign `/zhang-project` and `/ja`-in-title are false
  positives that reject valid entries.
- **Does clause h's parser agree with the C1 predicate grammar?** Yes — `ADV_RE`/`BOOT_RE`
  byte-identical to C1's (`dc1-r41-globals.py:170-174`); both are stricter than their own
  docstrings (`TS` unconstrained in prose; ISO-with-timezone + exactly-two-spaces in code), and
  the runner's test double uses a third, looser grammar. The real fetched journal parses to
  (2, 78, 63, 1) matching the registration.

## Top findings (H1–H4)
- H1: the entire validation surface is anchored to the entry's first 20 lines; citations past
  line 20 (including a ghost `S999` with no row/gate/receipt) are admitted.
- H2: clause b's head scan uses raw text, not `unfenced`; fenced `source:` lines count,
  contradicting the docstring.
- H3: minimal forgery 9,220 B (above).
- H4: clause-i substring heuristic defeat/false positives (above).
Plus M1–M5 (doc-vs-code gaps) and L1–L3 (low-severity parsing leniencies) in findings.md.

## Method
Frozen counter verified identical to HEAD (`git diff 60c3914 HEAD` empty). All reproductions ran
the control runner's own `score()`/`commit_all()` on temp git repos in /tmp (git init with
toplevel check, throwaway identity, cleaned up); the lane was only ever read. No tools installed;
nothing outside the seat dir was written.

Report trailer: `.ufo/waves/round-41/w1/RevC2Counter/findings.md`
